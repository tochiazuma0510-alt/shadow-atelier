#!/usr/bin/env python3
"""Lossless, production-only A0-v18 to task193 input adapter (v3).

The accepted object is a dedicated ABI.  It is not a task186 receipt and it
does not evaluate any task193/A5 quantity.  A positive result is possible
only after the pinned A0 checker has replayed the complete COMMON_WORD route.
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
SCHEMA = "d972-r07-history-free-task193-compat-adapter/v3"
ACCEPTED = "R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_A0_REPLAY"
UNKNOWN = "UNKNOWN_INPUT"
A0_SCHEMA = "d972-r07-history-free-positive-fast-resume/v10"
A0_COMMON = "R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V10_COMMON_WORD"
A0_VERDICT_SCHEMA = A0_SCHEMA + "/verdict"
A0_CLAIMS = {"common_word": True, "finite_common_word": True,
             "separator": False, "negative": False, "cofinal_lift": False,
             "fake": False, "ihara_witness": False}
A0_VERDICT_CLAIMS = {"finite_A0_candidate": True, "common_word": True,
                     "separator": False, "negative": False,
                     "cofinal_lift": False, "fake": False,
                     "ihara_witness": False}
A0_PRODUCER_PIN = (
    "search/d972_r07_history_free_positive_fast_resume_v18.py", 2557,
    "55505c6b59ebc9cc61c12c0229668509a2fcf7530ca14dbd791a8b18a95c5433")
A0_CHECKER_PIN = (
    "crosscheck/check_d972_r07_history_free_positive_fast_resume_v18.py", 1317,
    "83ebfe5088388f5c84bbab9e52ef28cb8888fb944fbe417cf98041bab34bfaa9")
MAX_BYTES = 512 * 1024 * 1024


class AdapterStop(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if condition is not True:
        raise AdapterStop(message)


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("self_digest", None)
    body["self_digest"] = digest(body)
    return body


def check_seal(value: dict[str, Any], label: str) -> None:
    claimed = value.get("self_digest")
    body = dict(value)
    body.pop("self_digest", None)
    need(type(claimed) is str and claimed == digest(body), label + " seal")


def resolve(raw: str | Path) -> Path:
    path = Path(raw)
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise AdapterStop("path outside workspace") from exc
    return resolved


def read_physical(raw_path: str | Path, limit: int = MAX_BYTES
                  ) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
    path = resolve(raw_path)
    need(not path.is_symlink(), "physical pathname symlink")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise AdapterStop("physical input open") from exc
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             0 < before.st_size <= limit, "physical input owner")
        raw = bytearray()
        while len(raw) < before.st_size:
            chunk = os.read(fd, min(1 << 20, before.st_size - len(raw)))
            need(bool(chunk), "physical input short read")
            raw.extend(chunk)
        need(not os.read(fd, 1), "physical input long read")
        after = os.fstat(fd)
        need((before.st_dev, before.st_ino, before.st_size, before.st_nlink,
              before.st_mtime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
              after.st_mtime_ns), "physical input changed")
        path_after = os.lstat(path)
        need(not stat.S_ISLNK(path_after.st_mode) and
             (path_after.st_dev, path_after.st_ino, path_after.st_size,
              path_after.st_nlink, path_after.st_mtime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_nlink,
              after.st_mtime_ns), "physical pathname changed")
        raw_bytes = bytes(raw)
        try:
            value = json.loads(raw_bytes.decode("ascii"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise AdapterStop("physical JSON") from exc
        need(type(value) is dict and raw_bytes == canon(value) + b"\n",
             "canonical JSON input")
        return value, raw_bytes, {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(raw_bytes), "sha256": digest_bytes(raw_bytes),
        }
    finally:
        os.close(fd)


def write_exclusive(raw_path: str | Path, value: Any) -> None:
    path = resolve(raw_path)
    need(not path.exists(), "stale output")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canon(value) + b"\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o644)
    try:
        view = memoryview(raw)
        while view:
            view = view[os.write(fd, view):]
        os.fsync(fd)
    finally:
        os.close(fd)


def own_identity() -> dict[str, Any]:
    path = Path(__file__).resolve()
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(raw), "sha256": digest_bytes(raw)}


def load_a0_checker() -> Any:
    path = ROOT / A0_CHECKER_PIN[0]
    raw = path.read_bytes()
    need(len(raw) == A0_CHECKER_PIN[1] and
         digest_bytes(raw) == A0_CHECKER_PIN[2], "A0 checker pin")
    spec = importlib.util.spec_from_file_location(
        "d972_r07_a0_v18_checker_for_adapter_v3", path)
    need(spec is not None and spec.loader is not None, "A0 checker loader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def legacy_sparse_digest(row: list[list[Any]]) -> str:
    """Digest the historical [u32be byte-length, key bytes, coeff] stream."""
    payload = bytearray()
    previous: bytes | None = None
    for item in row:
        need(type(item) is list and len(item) == 2 and
             type(item[0]) is str and type(item[1]) is int and item[1] in (1, 2),
             "sparse row entry")
        try:
            key = bytes.fromhex(item[0])
        except ValueError as exc:
            raise AdapterStop("sparse row hex") from exc
        need(item[0] == key.hex() and
             (previous is None or previous < key), "canonical sparse row")
        previous = key
        payload.extend(len(key).to_bytes(4, "big"))
        payload.extend(key)
        payload.append(item[1])
    return digest_bytes(bytes(payload))


def replay_a0(receipt: dict[str, Any], verdict: dict[str, Any],
              receipt_id: dict[str, Any], verdict_id: dict[str, Any]
              ) -> tuple[list[int], list[int], list[int], list[list[Any]],
                         dict[str, Any], dict[str, Any], dict[str, Any]]:
    check_seal(receipt, "A0 receipt")
    check_seal(verdict, "A0 verdict")
    need(receipt.get("schema") == A0_SCHEMA and
         receipt.get("status") == "COMMON_WORD" and
         receipt.get("terminal") == A0_COMMON and
         receipt.get("claims") == A0_CLAIMS and
         receipt.get("selftest") is None and "checkpoint" not in receipt and
         receipt.get("claim_boundary") ==
         "finite A0 candidate; checker required; no lift/fake/Ihara",
         "A0 COMMON envelope")
    need(verdict.get("schema") == A0_VERDICT_SCHEMA and
         verdict.get("status") == "PASS" and verdict.get("terminal") == A0_COMMON and
         verdict.get("producer_pin") == {
             "path": A0_PRODUCER_PIN[0], "bytes": A0_PRODUCER_PIN[1],
             "sha256": A0_PRODUCER_PIN[2]} and
         verdict.get("claims") == A0_VERDICT_CLAIMS,
         "A0 verdict envelope")
    physical = verdict.get("receipt_physical")
    need(type(physical) is dict and physical.get("bytes") == receipt_id["bytes"] and
         physical.get("sha256") == receipt_id["sha256"],
         "A0 receipt physical binding")
    need(verdict.get("source_snapshots") == receipt.get("source_snapshots"),
         "A0 source snapshot equality")

    checker = load_a0_checker()
    sources = checker.Sources()
    sources.authenticate()
    need(receipt.get("source_snapshots") == checker.Sources.public(),
         "A0 known source roster")
    task176 = checker.validate_task176_authority(sources)
    owners = checker.decode_task176_owners(sources)
    checker.validate_source_transport(receipt, hash_source=True)
    _source_value, source_raw = checker.read_bound_source(receipt)
    runtime = checker.build_checker_light(sources)
    runtime["task176_receipt"] = task176
    runtime["task176_owners"] = owners
    # This is the load-bearing full A0 replay.  SELFTEST is intentionally off.
    derived = checker.validate_common(runtime, receipt, include_selftest=False,
                                      source_raw=source_raw)
    need(derived == verdict.get("derived"), "A0 derived canonical equality")

    c = receipt.get("correction_word")
    f = receipt.get("corrected_word")
    g = receipt.get("g760")
    need(type(c) is list and type(f) is list and type(g) is list and
         all(type(x) is int for x in c + f + g) and len(g) == 760,
         "A0 literal words")
    direct, replay = runtime["model"].direct_column([], c)
    row = checker.public_sparse(direct)
    need(replay == receipt.get("producer_all_seven_replay") and
         replay.get("corrected_word") == f and
         replay.get("eleven_occurrence_replay") is True and
         replay.get("direct_all_seven_replay") is True,
         "A0 direct replay")
    return c, f, g, row, replay, derived, checker.Sources.public()


def accepted(receipt_id: dict[str, Any], verdict_id: dict[str, Any],
             c: list[int], f: list[int], g: list[int], row: list[list[Any]],
             replay: dict[str, Any], derived: dict[str, Any],
             roster: dict[str, Any]) -> dict[str, Any]:
    adapter = own_identity()
    return seal({
        "schema": SCHEMA, "status": "ACCEPTED", "terminal": ACCEPTED,
        "a0_receipt": {k: receipt_id[k] for k in ("path", "bytes", "sha256")},
        "a0_verdict": {k: verdict_id[k] for k in ("path", "bytes", "sha256")},
        "source_roster": roster, "a0_derived": derived,
        "c_exact": list(c), "corrected_word": list(f), "g760": list(g),
        "direct_replay": {
            "row": row, "row_sha256": legacy_sparse_digest(row),
            "replay": replay,
            "direct_all_seven_replay": True,
            "right_g760_multiplication": True,
            "hexagons": True, "pentagon_printed_order": True,
        },
        "source_provenance": {
            "adapter": adapter,
            "a0_producer": {"path": A0_PRODUCER_PIN[0],
                            "bytes": A0_PRODUCER_PIN[1],
                            "sha256": A0_PRODUCER_PIN[2]},
            "a0_checker": {"path": A0_CHECKER_PIN[0],
                           "bytes": A0_CHECKER_PIN[1],
                           "sha256": A0_CHECKER_PIN[2]},
            "replay": "pinned A0 checker validate_common(include_selftest=False) plus direct_column",
        },
        "claims": {"adapter": "A0_REPLAY_ONLY", "lift": "NONE",
                    "fake": "NONE", "Ihara": "NONE"},
    })


def unknown(reason: str, receipt_id: dict[str, Any] | None = None,
            verdict_id: dict[str, Any] | None = None) -> dict[str, Any]:
    return seal({
        "schema": SCHEMA, "status": "UNKNOWN",
        "terminal": UNKNOWN + ":" + reason, "reason": reason,
        "a0_receipt": receipt_id, "a0_verdict": verdict_id,
        "source_provenance": {"adapter": own_identity()},
        "claims": {"adapter": "NONE", "lift": "NONE", "fake": "NONE",
                    "Ihara": "NONE"},
    })


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a0-receipt", required=True)
    ap.add_argument("--a0-verdict", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--attestation-output", required=True)
    args = ap.parse_args(argv)
    try:
        receipt, _rr, receipt_id = read_physical(args.a0_receipt)
        verdict, _vr, verdict_id = read_physical(args.a0_verdict)
        if receipt.get("status") != "COMMON_WORD" or receipt.get("terminal") != A0_COMMON:
            result = unknown("A0:" + str(receipt.get("terminal", "missing")),
                             receipt_id, verdict_id)
        else:
            c, f, g, row, replay, derived, roster = replay_a0(
                receipt, verdict, receipt_id, verdict_id)
            result = accepted(receipt_id, verdict_id, c, f, g, row, replay,
                              derived, roster)
        write_exclusive(args.output, result)
        line = "R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_TERMINAL " + result["terminal"]
        write_exclusive(args.attestation_output, {
            "schema": SCHEMA + "/attestation", "terminal": result["terminal"],
            "line": line,
        })
        print(line, flush=True)
        return 0
    except Exception as exc:
        result = unknown(str(exc))
        try:
            write_exclusive(args.output, result)
            line = "R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_TERMINAL " + result["terminal"]
            write_exclusive(args.attestation_output, {
                "schema": SCHEMA + "/attestation", "terminal": result["terminal"],
                "line": line,
            })
        except Exception:
            pass
        print("R07_HISTORY_FREE_TASK193_COMPAT_ADAPTER_V3_TERMINAL " +
              result["terminal"], flush=True)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
