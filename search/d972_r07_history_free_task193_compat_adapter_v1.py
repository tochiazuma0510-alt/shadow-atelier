#!/usr/bin/env python3
"""Production-only A0-v18 to task193-v1 compatibility adapter.

This bridge authenticates a physical A0 COMMON_WORD receipt and its checker
verdict, then emits the smallest task186-shaped envelope accepted by the
task193-v1 input gate.  It performs the all-seven direct replay through the
independent A0 checker arithmetic; it never runs an A0 search or task193.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SCHEMA = "d972-r07-history-free-task193-compat-adapter/v1"
TASK186_SCHEMA = "d972-r07-normalized-exact-common-word-colgen/v2"
TASK186_COMMON = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"

A0_SCHEMA = "d972-r07-history-free-positive-fast-resume/v10"
A0_COMMON = "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD"
A0_VERDICT_SCHEMA = A0_SCHEMA + "/verdict"
A0_PRODUCER_PIN = (
    "search/d972_r07_history_free_positive_fast_resume_v18.py",
    2557,
    "55505c6b59ebc9cc61c12c0229668509a2fcf7530ca14dbd791a8b18a95c5433",
)
A0_CHECKER_PATH = ROOT / "crosscheck/check_d972_r07_history_free_positive_fast_resume_v18.py"
A0_CHECKER_PIN = (
    "crosscheck/check_d972_r07_history_free_positive_fast_resume_v18.py",
    1317,
    "83ebfe5088388f5c84bbab9e52ef28cb8888fb944fbe417cf98041bab34bfaa9",
)
A0_POSITIVE_CLAIMS = {
    "common_word": True, "finite_common_word": True,
    "separator": False, "negative": False, "cofinal_lift": False,
    "fake": False, "ihara_witness": False,
}
MAX_INPUT_BYTES = 512 * 1024 * 1024


class AdapterStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AdapterStop(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("self_digest", None)
    body["self_digest"] = digest(body)
    return body


def validate_seal(value: dict[str, Any]) -> None:
    claimed = value.get("self_digest")
    body = dict(value)
    body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body), "receipt seal")


def resolve_workspace(raw: str | Path) -> Path:
    path = Path(raw)
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise AdapterStop("path outside workspace") from exc
    return resolved


def read_physical(raw_path: str | Path) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
    path = resolve_workspace(raw_path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise AdapterStop("physical input open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                0 < before.st_size <= MAX_INPUT_BYTES, "physical input owner")
        raw = bytearray()
        while len(raw) < before.st_size:
            chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
            require(chunk, "physical input short read")
            raw.extend(chunk)
        require(not os.read(fd, 1), "physical input long read")
        after = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                 before.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                 after.st_mtime_ns), "physical input changed")
        path_after = os.lstat(path)
        require(not stat.S_ISLNK(path_after.st_mode) and
                (path_after.st_dev, path_after.st_ino, path_after.st_size,
                 path_after.st_nlink, path_after.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size,
                 after.st_nlink, after.st_mtime_ns), "physical pathname changed")
        raw_bytes = bytes(raw)
        try:
            value = json.loads(raw_bytes.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise AdapterStop("physical JSON") from exc
        require(type(value) is dict and raw_bytes == canonical(value) + b"\n",
                "canonical JSON input")
        return value, raw_bytes, {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(raw_bytes), "sha256": digest_bytes(raw_bytes),
            "device": before.st_dev, "inode": before.st_ino,
            "links": before.st_nlink, "mtime_ns": before.st_mtime_ns,
            "single_fd": True, "no_follow": True,
        }
    finally:
        os.close(fd)


def write_exclusive(raw_path: str | Path, value: dict[str, Any]) -> None:
    path = resolve_workspace(raw_path)
    require(not path.exists(), "stale adapter output")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(value) + b"\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o644)
    try:
        view = memoryview(raw)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)


def write_exclusive_bytes(raw_path: str | Path, raw: bytes) -> None:
    path = resolve_workspace(raw_path)
    require(not path.exists(), "stale adapter attestation")
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o644)
    try:
        view = memoryview(raw)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)


def auth_snapshot_files(snapshots: Any) -> None:
    require(type(snapshots) is dict and snapshots, "A0 source snapshot roster")
    for name, item in sorted(snapshots.items()):
        require(type(name) is str and type(item) is dict, "source snapshot entry")
        path_raw = item.get("path")
        size = item.get("bytes")
        expected = item.get("sha256")
        require(type(path_raw) is str and type(size) is int and size >= 0 and
                type(expected) is str and len(expected) == 64,
                "source snapshot identity")
        path = resolve_workspace(path_raw)
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(path, flags)
        except OSError as exc:
            raise AdapterStop("source snapshot open:" + str(name)) from exc
        try:
            before = os.fstat(fd)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                    before.st_size == size, "source snapshot size:" + str(name))
            hasher = hashlib.sha256()
            remaining = size
            while remaining:
                chunk = os.read(fd, min(1 << 20, remaining))
                require(chunk, "source snapshot short read:" + str(name))
                hasher.update(chunk)
                remaining -= len(chunk)
            require(not os.read(fd, 1) and hasher.hexdigest() == expected.lower(),
                    "source snapshot digest:" + str(name))
            after = os.fstat(fd)
            require((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                     before.st_mtime_ns) ==
                    (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                     after.st_mtime_ns), "source snapshot changed:" + str(name))
        finally:
            os.close(fd)


def load_independent_checker() -> Any:
    raw = A0_CHECKER_PATH.read_bytes()
    require(len(raw) == A0_CHECKER_PIN[1] and
            digest_bytes(raw) == A0_CHECKER_PIN[2], "A0 checker pin")
    spec = importlib.util.spec_from_file_location(
        "d972_r07_a0_v18_independent_checker", A0_CHECKER_PATH)
    require(spec is not None and spec.loader is not None, "A0 checker loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_all_seven(receipt: dict[str, Any]) -> tuple[list[list[Any]], dict[str, Any]]:
    """Use helper-nonshared task179/task186 arithmetic, never receipt booleans."""
    checker = load_independent_checker()
    sources = checker.Sources()
    sources.authenticate()
    runtime = checker.build_checker_light(sources)
    g760 = receipt.get("g760")
    require(type(g760) is list and g760 == runtime["g760"], "independent g760 replay")
    correction = receipt.get("correction_word")
    require(type(correction) is list, "A0 literal correction")
    direct, replay = runtime["model"].direct_column([], correction)
    public = [[key.hex(), int(value) % 3]
              for key, value in sorted(direct.items()) if int(value) % 3]
    return public, replay


def validate_a0(receipt: dict[str, Any], receipt_raw: bytes,
                verdict: dict[str, Any], verdict_raw: bytes,
                receipt_identity: dict[str, Any],
                verdict_identity: dict[str, Any]) -> tuple[list[list[Any]], dict[str, Any]]:
    validate_seal(receipt)
    validate_seal(verdict)
    require(receipt.get("schema") == A0_SCHEMA and
            receipt.get("status") == "COMMON_WORD" and
            receipt.get("terminal") == A0_COMMON, "A0 COMMON envelope")
    require(receipt.get("claims") == A0_POSITIVE_CLAIMS and
            receipt.get("selftest") is None and "checkpoint" not in receipt and
            receipt.get("claim_boundary") ==
            "finite A0 candidate; checker required; no lift/fake/Ihara",
            "A0 positive claims")
    require(verdict.get("schema") == A0_VERDICT_SCHEMA and
            verdict.get("status") == "PASS" and
            verdict.get("terminal") == A0_COMMON, "A0 verdict envelope")
    require(verdict.get("producer_pin") == {
        "path": A0_PRODUCER_PIN[0], "bytes": A0_PRODUCER_PIN[1],
        "sha256": A0_PRODUCER_PIN[2]}, "A0 producer pin")
    require(verdict.get("claims") == {
        "finite_A0_candidate": True, "common_word": True,
        "separator": False, "negative": False, "cofinal_lift": False,
        "fake": False, "ihara_witness": False}, "A0 verdict claims")
    physical = verdict.get("receipt_physical")
    require(type(physical) is dict and
            physical.get("bytes") == receipt_identity["bytes"] and
            physical.get("sha256") == receipt_identity["sha256"],
            "A0 receipt physical binding")
    require(verdict.get("source_snapshots") == receipt.get("source_snapshots"),
            "A0 source snapshot equality")
    auth_snapshot_files(receipt.get("source_snapshots"))
    require(type(receipt.get("correction_word")) is list,
            "A0 literal correction binding")
    require(type(receipt.get("corrected_word")) is list and
            receipt.get("corrected_word"), "A0 corrected word")
    require(type(receipt.get("g760")) is list and len(receipt["g760"]) == 760,
            "A0 g760 shape")
    public, replay = independent_all_seven(receipt)
    require(replay.get("corrected_word") == receipt.get("corrected_word"),
            "A0 corrected word replay")
    require(receipt.get("producer_all_seven_replay") == replay,
            "A0 producer all-seven replay")
    body = dict(replay)
    require(body.get("direct_all_seven_replay") is True and
            body.get("eleven_occurrence_replay") is True,
            "A0 replay gates")
    return public, replay


def exponent_pair(word: list[int]) -> tuple[int, int]:
    return (
        sum(1 if int(x) == 1 else -1 if int(x) == -1 else 0 for x in word),
        sum(1 if int(x) == 2 else -1 if int(x) == -2 else 0 for x in word),
    )


def task186_envelope(receipt: dict[str, Any], receipt_raw: bytes,
                     verdict: dict[str, Any], verdict_raw: bytes,
                     receipt_identity: dict[str, Any],
                     verdict_identity: dict[str, Any],
                     row: list[list[Any]], replay: dict[str, Any]) -> dict[str, Any]:
    correction = list(receipt["correction_word"])
    corrected = list(receipt["corrected_word"])
    g760 = list(receipt["g760"])
    require(exponent_pair(correction) == (0, 0), "A0 integer exponent replay")
    require(replay["corrected_word"] == corrected, "task193 corrected binding")
    exact = list(correction)
    expected = {
        "c_star": list(correction), "v0": [], "u0": [], "h": [],
        "c_exact": exact,
    }
    return seal({
        "schema": TASK186_SCHEMA, "status": "COMMON_WORD",
        "terminal": TASK186_COMMON,
        "source": receipt.get("source"),
        "source_snapshots": receipt.get("source_snapshots"),
        "correction_word": list(correction),
        "corrected_word": corrected, "g760": g760,
        "exactification": {
            "source": "authenticated A0 v18 correction_word",
            "positive_receipt": True, "literal": expected,
            "r_words": {}, "A": 0, "B": 0,
            "exponents": {
                "c_star": list(exponent_pair(correction)),
                "v0": [0, 0], "u0": [0, 0], "h": [0, 0],
                "c_exact": list(exponent_pair(exact)),
            },
        },
        "exact_direct_replay": {
            "row": row, "star_row": row,
            "row_sha256": digest(row), "star_row_sha256": digest(row),
            "replay": dict(replay),
            "joint_kernel": True, "right_g760_multiplication": True,
            "hexagons": True, "pentagon_printed_order": True,
        },
        "adapter_provenance": {
            "schema": ADAPTER_SCHEMA, "version": 1,
            "a0_receipt": receipt_identity,
            "a0_verdict": verdict_identity,
            "a0_receipt_self_digest": receipt["self_digest"],
            "a0_verdict_self_digest": verdict["self_digest"],
            "a0_producer_pin": {
                "path": A0_PRODUCER_PIN[0], "bytes": A0_PRODUCER_PIN[1],
                "sha256": A0_PRODUCER_PIN[2],
            },
            "independent_replay": {
                "corrected_word": list(replay["corrected_word"]),
                "producer_all_seven_replay_equal": True,
                "g760_equal": True,
            },
        },
        "claims": {
            "task193_input_compatibility": True,
            "common_word": True, "finite_common_word": True,
            "separator": False, "negative": False, "cofinal_lift": False,
            "fake": False, "ihara_witness": False,
        },
    })


def unknown_envelope(reason: str, receipt_identity: dict[str, Any] | None = None,
                     verdict_identity: dict[str, Any] | None = None) -> dict[str, Any]:
    return seal({
        "schema": ADAPTER_SCHEMA, "status": "UNKNOWN",
        "terminal": UNKNOWN_INPUT + ":" + reason, "reason": reason,
        "a0_receipt": receipt_identity, "a0_verdict": verdict_identity,
        "claims": {
            "task193_input_compatibility": False,
            "common_word": False, "finite_common_word": False,
            "separator": False, "negative": False, "cofinal_lift": False,
            "fake": False, "ihara_witness": False,
        },
    })


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a0-receipt", required=True)
    ap.add_argument("--a0-verdict", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--attestation-output", required=True)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    output = resolve_workspace(args.output)
    attestation = resolve_workspace(args.attestation_output)
    try:
        receipt, receipt_raw, receipt_identity = read_physical(args.a0_receipt)
        verdict, verdict_raw, verdict_identity = read_physical(args.a0_verdict)
        if receipt.get("status") != "COMMON_WORD" or receipt.get("terminal") != A0_COMMON:
            reason = str(receipt.get("terminal", "missing A0 COMMON_WORD"))
            result = unknown_envelope("A0:" + reason, receipt_identity, verdict_identity)
        else:
            row, replay = validate_a0(receipt, receipt_raw, verdict, verdict_raw,
                                      receipt_identity, verdict_identity)
            result = task186_envelope(receipt, receipt_raw, verdict, verdict_raw,
                                      receipt_identity, verdict_identity, row, replay)
        write_exclusive(output, result)
        if result.get("status") == "COMMON_WORD":
            # The task193-v1 producer's authenticated-input gate consumes this
            # exact task186 checker attestation line.
            line = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=" + TASK186_COMMON
        else:
            line = result["terminal"]
        write_exclusive_bytes(attestation, (line + "\n").encode("ascii"))
        print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V1_PRODUCER_TERMINAL " +
              result["terminal"], flush=True)
        return 0
    except (AdapterStop, OSError, ValueError, TypeError) as exc:
        try:
            result = unknown_envelope(str(exc))
            write_exclusive(output, result)
            write_exclusive_bytes(attestation,
                                  (result["terminal"] + "\n").encode("ascii"))
        except Exception:
            pass
        print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V1_PRODUCER_TERMINAL " +
              UNKNOWN_INPUT + ":" + str(exc), flush=True)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
