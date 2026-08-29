#!/usr/bin/env python3
"""Independent production checker for the A0-v18/task193 compatibility bridge.

The adapter producer is not imported.  A0 source identity, seal, terminal,
literal word, g760 and all-seven direct replay are rechecked independently.
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


class AdapterCheckStop(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AdapterCheckStop(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def validate_seal(value: dict[str, Any]) -> None:
    claimed = value.get("self_digest")
    body = dict(value)
    body.pop("self_digest", None)
    require(type(claimed) is str and claimed == digest(body), "seal")


def resolve_workspace(raw: str | Path) -> Path:
    path = Path(raw)
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise AdapterCheckStop("path outside workspace") from exc
    return resolved


def read_physical(raw_path: str | Path) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
    path = resolve_workspace(raw_path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise AdapterCheckStop("physical JSON open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                0 < before.st_size <= MAX_INPUT_BYTES, "physical JSON owner")
        raw = bytearray()
        while len(raw) < before.st_size:
            chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
            require(chunk, "physical JSON short read")
            raw.extend(chunk)
        require(not os.read(fd, 1), "physical JSON long read")
        after = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                 before.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                 after.st_mtime_ns), "physical JSON changed")
        path_after = os.lstat(path)
        require(not stat.S_ISLNK(path_after.st_mode) and
                (path_after.st_dev, path_after.st_ino, path_after.st_size,
                 path_after.st_nlink, path_after.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size,
                 after.st_nlink, after.st_mtime_ns), "physical JSON pathname changed")
        raw_bytes = bytes(raw)
        try:
            value = json.loads(raw_bytes.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise AdapterCheckStop("physical JSON decode") from exc
        require(type(value) is dict and raw_bytes == canonical(value) + b"\n",
                "canonical JSON")
        return value, raw_bytes, {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(raw_bytes), "sha256": digest_bytes(raw_bytes),
            "device": before.st_dev, "inode": before.st_ino,
            "links": before.st_nlink, "mtime_ns": before.st_mtime_ns,
            "single_fd": True, "no_follow": True,
        }
    finally:
        os.close(fd)


def read_attestation(raw_path: str | Path) -> tuple[bytes, dict[str, Any]]:
    path = resolve_workspace(raw_path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise AdapterCheckStop("attestation open") from exc
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
                0 < before.st_size <= 4096, "attestation owner")
        raw = os.read(fd, before.st_size)
        require(len(raw) == before.st_size and not os.read(fd, 1), "attestation length")
        after = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
                 before.st_mtime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
                 after.st_mtime_ns), "attestation changed")
        return raw, {"path": str(path.relative_to(ROOT)).replace("\\", "/"),
                     "bytes": len(raw), "sha256": digest_bytes(raw)}
    finally:
        os.close(fd)


def auth_snapshot_files(snapshots: Any) -> None:
    require(type(snapshots) is dict and snapshots, "source snapshot roster")
    for name, item in sorted(snapshots.items()):
        require(type(name) is str and type(item) is dict, "source snapshot entry")
        path_raw, size, expected = item.get("path"), item.get("bytes"), item.get("sha256")
        require(type(path_raw) is str and type(size) is int and size >= 0 and
                type(expected) is str and len(expected) == 64,
                "source snapshot identity")
        path = resolve_workspace(path_raw)
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(path, flags)
        except OSError as exc:
            raise AdapterCheckStop("source snapshot open:" + str(name)) from exc
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
        "d972_r07_a0_v18_independent_checker_for_adapter", A0_CHECKER_PATH)
    require(spec is not None and spec.loader is not None, "A0 checker loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_all_seven(receipt: dict[str, Any]) -> tuple[list[list[Any]], dict[str, Any]]:
    checker = load_independent_checker()
    sources = checker.Sources()
    sources.authenticate()
    runtime = checker.build_checker_light(sources)
    require(type(receipt.get("g760")) is list and
            receipt["g760"] == runtime["g760"], "independent g760")
    correction = receipt.get("correction_word")
    require(type(correction) is list, "A0 correction word")
    direct, replay = runtime["model"].direct_column([], correction)
    public = [[key.hex(), int(value) % 3]
              for key, value in sorted(direct.items()) if int(value) % 3]
    return public, replay


def read_a0(receipt_path: str, verdict_path: str) -> tuple[
        dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], list[list[Any]], dict[str, Any]]:
    receipt, receipt_raw, receipt_identity = read_physical(receipt_path)
    verdict, verdict_raw, verdict_identity = read_physical(verdict_path)
    validate_seal(receipt)
    validate_seal(verdict)
    require(receipt.get("schema") == A0_SCHEMA and
            receipt.get("status") == "COMMON_WORD" and
            receipt.get("terminal") == A0_COMMON, "A0 COMMON envelope")
    require(receipt.get("claims") == A0_POSITIVE_CLAIMS and
            receipt.get("selftest") is None and "checkpoint" not in receipt and
            receipt.get("claim_boundary") ==
            "finite A0 candidate; checker required; no lift/fake/Ihara",
            "A0 claims")
    require(verdict.get("schema") == A0_VERDICT_SCHEMA and
            verdict.get("status") == "PASS" and verdict.get("terminal") == A0_COMMON,
            "A0 verdict envelope")
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
            "A0 physical receipt binding")
    require(verdict.get("source_snapshots") == receipt.get("source_snapshots"),
            "A0 source snapshot equality")
    auth_snapshot_files(receipt.get("source_snapshots"))
    require(type(receipt.get("corrected_word")) is list and
            receipt.get("corrected_word"), "A0 corrected word")
    require(type(receipt.get("g760")) is list and len(receipt["g760"]) == 760,
            "A0 g760 shape")
    public, replay = independent_all_seven(receipt)
    require(replay.get("corrected_word") == receipt.get("corrected_word"),
            "A0 corrected replay")
    require(receipt.get("producer_all_seven_replay") == replay,
            "A0 all-seven replay")
    require(replay.get("direct_all_seven_replay") is True and
            replay.get("eleven_occurrence_replay") is True, "A0 replay gates")
    return receipt, verdict, receipt_identity, verdict_identity, public, replay


def exponent_pair(word: list[int]) -> tuple[int, int]:
    return (
        sum(1 if int(x) == 1 else -1 if int(x) == -1 else 0 for x in word),
        sum(1 if int(x) == 2 else -1 if int(x) == -2 else 0 for x in word),
    )


def validate_task193_envelope(
        envelope: dict[str, Any], receipt: dict[str, Any], verdict: dict[str, Any],
        receipt_identity: dict[str, Any], verdict_identity: dict[str, Any],
        public: list[list[Any]], replay: dict[str, Any]) -> None:
    validate_seal(envelope)
    require(envelope.get("schema") == TASK186_SCHEMA and
            envelope.get("status") == "COMMON_WORD" and
            envelope.get("terminal") == TASK186_COMMON,
            "task193 input envelope")
    correction = receipt["correction_word"]
    require(envelope.get("correction_word") == correction and
            envelope.get("corrected_word") == receipt["corrected_word"] and
            envelope.get("g760") == receipt["g760"],
            "A0 literal binding")
    require(exponent_pair(correction) == (0, 0), "c_exact exponent")
    ex = envelope.get("exactification")
    require(type(ex) is dict and ex.get("positive_receipt") is True and
            ex.get("source") == "authenticated A0 v18 correction_word" and
            ex.get("r_words") == {} and ex.get("A") == 0 and ex.get("B") == 0,
            "exactification provenance")
    literals = ex.get("literal")
    require(literals == {
        "c_star": list(correction), "v0": [], "u0": [], "h": [],
        "c_exact": list(correction)}, "c_exact literal binding")
    require(ex.get("exponents") == {
        "c_star": list(exponent_pair(correction)), "v0": [0, 0],
        "u0": [0, 0], "h": [0, 0],
        "c_exact": list(exponent_pair(correction))}, "exactification exponents")
    direct = envelope.get("exact_direct_replay")
    require(type(direct) is dict and direct.get("row") == public and
            direct.get("star_row") == public and
            direct.get("row_sha256") == digest(public) and
            direct.get("star_row_sha256") == digest(public),
            "direct row binding")
    require(direct.get("replay") == replay and
            direct.get("joint_kernel") is True and
            direct.get("right_g760_multiplication") is True and
            direct.get("hexagons") is True and
            direct.get("pentagon_printed_order") is True,
            "direct replay binding")
    provenance = envelope.get("adapter_provenance")
    require(type(provenance) is dict and provenance.get("schema") == ADAPTER_SCHEMA and
            provenance.get("version") == 1,
            "adapter provenance")
    require(provenance.get("a0_receipt") == receipt_identity and
            provenance.get("a0_verdict") == verdict_identity and
            provenance.get("a0_receipt_self_digest") == receipt["self_digest"] and
            provenance.get("a0_verdict_self_digest") == verdict["self_digest"],
            "physical source identity binding")
    require(provenance.get("a0_producer_pin") == {
        "path": A0_PRODUCER_PIN[0], "bytes": A0_PRODUCER_PIN[1],
        "sha256": A0_PRODUCER_PIN[2]}, "adapter A0 pin")
    require(provenance.get("independent_replay") == {
        "corrected_word": list(replay["corrected_word"]),
        "producer_all_seven_replay_equal": True,
        "g760_equal": True}, "independent replay ledger")
    require(envelope.get("claims") == {
        "task193_input_compatibility": True,
        "common_word": True, "finite_common_word": True,
        "separator": False, "negative": False, "cofinal_lift": False,
        "fake": False, "ihara_witness": False,
    }, "adapter claims")


def unknown_terminal(envelope: dict[str, Any]) -> None:
    validate_seal(envelope)
    require(envelope.get("schema") == ADAPTER_SCHEMA and
            envelope.get("status") == "UNKNOWN", "unknown adapter envelope")
    terminal = str(envelope.get("terminal", ""))
    require(terminal.startswith(UNKNOWN_INPUT + ":"), "typed UNKNOWN_INPUT")
    require(envelope.get("claims") == {
        "task193_input_compatibility": False,
        "common_word": False, "finite_common_word": False,
        "separator": False, "negative": False, "cofinal_lift": False,
        "fake": False, "ihara_witness": False,
    }, "unknown claims")


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a0-receipt", required=True)
    ap.add_argument("--a0-verdict", required=True)
    ap.add_argument("--task186-receipt", required=True)
    ap.add_argument("--attestation", required=True)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        # A missing or typed-UNKNOWN A0 input is a terminal transport result;
        # it is checkable without dereferencing a nonexistent A0 path.
        envelope, _raw, _out_id = read_physical(args.task186_receipt)
        if envelope.get("schema") == ADAPTER_SCHEMA:
            unknown_terminal(envelope)
            attestation, _att_id = read_attestation(args.attestation)
            require(attestation == (str(envelope["terminal"]) + "\n").encode("ascii"),
                    "unknown adapter attestation")
            print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V1_CHECKER_PASS terminal=" +
                  str(envelope["terminal"]), flush=True)
            return 0
        receipt, verdict, receipt_id, verdict_id, public, replay = read_a0(
            args.a0_receipt, args.a0_verdict)
        attestation, _att_id = read_attestation(args.attestation)
        require(attestation == (
            "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=" +
            TASK186_COMMON + "\n").encode("ascii"), "task193 attestation")
        validate_task193_envelope(envelope, receipt, verdict, receipt_id,
                                  verdict_id, public, replay)
        print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V1_CHECKER_PASS terminal=" +
              TASK186_COMMON, flush=True)
        return 0
    except (AdapterCheckStop, OSError, ValueError, TypeError) as exc:
        print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V1_CHECKER_FAIL " +
              str(exc), flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
