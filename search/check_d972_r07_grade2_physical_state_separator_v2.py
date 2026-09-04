#!/usr/bin/env python3
"""Independent replay checker for the R07 physical state/separator core.

The checker deliberately has no import or execution edge to the producer.  It
parses the v6 connection parent, replays packed physical rows in insertion
order, and independently recomputes the v536 target reduction and separator.
The live v11 candidate artifact tuple is bound to the exact owner-supplied
receipt below; bounded fixtures are marked fixture-only and cannot be
promoted by this program.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "tochiazuma0510-alt/shadow-atelier"
PHYSICAL_WIDTH = 48384
PHYSICAL_BYTES = PHYSICAL_WIDTH // 4
LOWER_WIDTH = 32260
LOWER_BYTES = LOWER_WIDTH // 4
P1_WIDTH = 8059
P1_BYTES = (P1_WIDTH + 3) // 4
MAX_CONNECTION_OFFERS = 8059
CONNECTION_SCHEMA = "d972.r07.canonical-p1-physical-connection.v6"
CHECKPOINT_SCHEMA = "d972.r07.canonical-p1-physical-connection.checkpoint.v6"
STATE_CHECKPOINT_SCHEMA = "d972.r07.physical-state.checkpoint.v1"
STATE_SCHEMA = "d972.r07.physical-state.v1"
STATE_HEAD_SCHEMA = "d972.r07.physical-state.HEAD.v1"
TARGET_SCHEMA = "d972.r07.targeted-grade2.rho2-v9.acquisition.v1"
TARGET_PAYLOAD_SCHEMA = "d972.r07.a0.fresh-precision2-endpoint-signature.v9"
TARGET_CHECKER_SCHEMA = TARGET_PAYLOAD_SCHEMA + ".checker"
ZERO_HEAD = "00" * 32
LIVE_V11 = {
    "repository": REPOSITORY,
    "workflow": ".github/workflows/d972-r07-canonical-p1-physical-connection-v11.yml",
    "run": "33876776771", "attempt": "1",
    "head": "b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2",
    "job": "101035535909",
    "producer_v6_sha256": "6c450c2d82f7ad5795d9188e2912a4587882ae3fb9351217f33393c96f75526a",
    "checker_v7_sha256": "b5b210f6063a8fed6172417d350510eeccbafa0f60e5e676aa2732fee5e8757e",
    "workflow_sha256": "c7f3c9a8b728fa5ab0bd6be0b550b381e5b33d8ce1f59523dc04fb82b306fb74",
}
LIVE_CONNECTION_COUNTS = {
    "offers": 8059, "rank": 6705, "dependent": 1354,
    "reduction_count": 7665974,
    "final_rolling_head": "3cb1bcf691038d71082b8d4774c5dd8898a239e71ef64da22ec486ba923cb8bd",
}
FINAL_V11_ARTIFACT: dict[str, Any] = {
    "repository": REPOSITORY,
    "run": "33876776771", "attempt": "1",
    "head": "b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2",
    "job": "101035535909", "status": "completed", "conclusion": "success",
    "artifact_id": 9939860701,
    "artifact_name": "d972-r07-canonical-p1-physical-connection-v11-candidate-33876776771-1",
    "archive_bytes": 245546516,
    "digest": "sha256:0c3753d7384a7850aadab41c9ec2755114475862a0b03fd806e875005a72995a",
    "expires_at": "2026-12-03T13:12:28Z",
}
PRODUCER_V6 = {"bytes": 68202, "lf": 690,
               "sha256": LIVE_V11["producer_v6_sha256"]}
CHECKER_V7 = {"bytes": 100990, "lf": 1768,
              "sha256": LIVE_V11["checker_v7_sha256"]}
RHO2_V4_ADAPTER = {
    "schema": TARGET_SCHEMA, "run_id": 33839962829, "run_attempt": 1,
    "head_sha": "17a8439c766d92719d7ae7d35846ea444da598fa",
    "artifact_id": 9925190479,
    "artifact_name": "task640-fresh-rho2-v17-33839962829-1",
    "artifact_archive_bytes": 6049643,
    "artifact_digest": "sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4",
    "adapter_sha256": "ce84baea0bc18380af8a20e32eb8862f9adc20ad596c2012e127f8b7b8341a4b",
}
RHO2_ACQUISITION = {
    "schema": TARGET_SCHEMA,
    "repository": REPOSITORY,
    "run_id": 33839962829,
    "run_attempt": 1,
    "head_sha": "17a8439c766d92719d7ae7d35846ea444da598fa",
    "workflow_path": ".github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml",
    "workflow_id": 349904905,
    "event": "push",
    "conclusion": "success",
    "artifact_id": 9925190479,
    "artifact_name": "task640-fresh-rho2-v17-33839962829-1",
    "artifact_archive_bytes": 6049643,
    "artifact_digest": "sha256:01722bfda081e577195aa6ca9c0bba3425a50dcfd829eca6ac23e33cb5d79ca4",
}
RHO2_PAYLOAD_RECEIPTS = {
    "rho2.bin": {"file": "rho2.bin", "bytes": 12096, "sha256": "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"},
    "rho2-dense.bin": {"file": "rho2-dense.bin", "bytes": 48384, "sha256": "abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e"},
    "lower-dense.bin": {"file": "lower-dense.bin", "bytes": 32260, "sha256": "c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830"},
    "target-dense.bin": {"file": "target-dense.bin", "bytes": 80644, "sha256": "122dca3cf3dc3299214f1ba4c2bc5b82dbe64e510f8aef482329316c2a935ea2"},
    "path-signatures.json": {"file": "path-signatures.json", "bytes": 28393211, "sha256": "ef7fbd1d44647c058b33a1c18894ff5411dcd7870e7cf7e24b6763b68557ab25"},
    "signature-buckets.json": {"file": "signature-buckets.json", "bytes": 46469668, "sha256": "e67876dce3bb144ad6afa4895236c8fc37fbc0488c135f9903d8288039829c43"},
    "authenticated-roots.json": {"file": "authenticated-roots.json", "bytes": 255846, "sha256": "af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5"},
}
RHO2_MANIFEST = {"bytes": 26047, "sha256": "55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488"}
RHO2_VERDICT = {"file": "task640-verdict.json", "bytes": 418, "sha256": "cdf0654738a10acf59844df3b9dda5ab8efdf2e387bba7d69b691a4ad46b2848"}
CLAIM_FALSE = {"ACTUAL_CONNECTION_STATE": False,
               "GRADE2_MEMBER/NONMEMBER": "NOT_DECIDED",
               "A0": "NOT_DECLARED", "COMMON": "NOT_DECLARED",
               "COFINAL_LIFT": "NOT_DECLARED", "FAKE": "NOT_DECLARED",
               "IHARA": "NOT_DECLARED", "cross_checked": False,
               "verified": False}
SOURCE_CLAIM_FALSE = {"A0": False, "COMMON": False,
                      "COFINAL_LIFT": False, "FAKE": False,
                      "IHARA": False, "verified": False}
STATE_MANIFEST_KEYS = {
    "schema", "status", "connection_manifest_sha256", "source_ancestry",
    "p1_identity", "task712", "cursor", "offers", "authenticated_offers",
    "physical_offers", "physical_reduction_bound", "rank", "dependent",
    "skipped", "generation", "physical", "p1_companions", "instructions",
    "candidate_roster", *CLAIM_FALSE,
}


def validate_final_artifact(value: Any) -> None:
    require(FINAL_V11_ARTIFACT is not None and value == FINAL_V11_ARTIFACT,
            "final_v11_artifact_tuple")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path, chunk_bytes: int = 1024 * 1024) -> str:
    hasher = hashlib.sha256()
    with path.open("rb", buffering=0) as stream:
        while True:
            chunk = stream.read(chunk_bytes)
            if not chunk:
                return hasher.hexdigest()
            hasher.update(chunk)


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def digest(value: Any, reason: str) -> None:
    require(isinstance(value, str) and len(value) == 64 and
            all(c in "0123456789abcdef" for c in value), reason)


def _digits(value: int) -> tuple[int, int, int, int]:
    require(0 <= value <= 80, "packed_byte_out_of_range")
    return value % 3, (value // 3) % 3, (value // 9) % 3, (value // 27) % 3


DIGITS = np.asarray([_digits(i) for i in range(81)], dtype=np.uint8)
PACKED_AXPY = np.empty((2, 81, 81), dtype=np.uint8)
for scalar in (1, 2):
    for left in range(81):
        for right in range(81):
            PACKED_AXPY[scalar - 1, left, right] = sum(
                ((int(DIGITS[left, j]) - scalar * int(DIGITS[right, j])) % 3) * 3 ** j
                for j in range(4))
SCALE_TWO = np.asarray([
    sum((2 * int(DIGITS[i, j]) % 3) * 3 ** j for j in range(4))
    for i in range(81)], dtype=np.uint8)
FIRST_TRIT = np.full(81, -1, dtype=np.int8)
FIRST_VALUE = np.zeros(81, dtype=np.uint8)
for value in range(1, 81):
    for position, digit in enumerate(DIGITS[value]):
        if digit:
            FIRST_TRIT[value] = position; FIRST_VALUE[value] = digit; break


def validate_packed(raw: bytes | bytearray | np.ndarray, width: int) -> None:
    expected = (width + 3) // 4
    view = raw.reshape(-1) if isinstance(raw, np.ndarray) else np.frombuffer(raw, dtype=np.uint8)
    require(view.size == expected and not np.any(view > 80), "packed_shape")
    if width % 4:
        require(int(DIGITS[int(view[-1]), width % 4]) == 0, "packed_padding")


def pack(values: Sequence[int] | np.ndarray, width: int) -> bytes:
    array = np.asarray(values, dtype=np.uint8).reshape(-1)
    require(array.size == width and not np.any(array > 2), "pack_shape")
    output = np.zeros((width + 3) // 4, dtype=np.uint8)
    for position in range(4):
        output[:(width + 3 - position) // 4] += (
            array[position::4] * 3 ** position).astype(np.uint8)
    validate_packed(output, width); return output.tobytes()


def unpack(raw: bytes | bytearray | np.ndarray, width: int) -> np.ndarray:
    validate_packed(raw, width)
    packed = raw if isinstance(raw, np.ndarray) else np.frombuffer(raw, dtype=np.uint8)
    output = np.empty(width, dtype=np.uint8)
    for position in range(4):
        output[position::4] = DIGITS[packed, position][:output[position::4].size]
    return output


def first_nonzero(raw: bytes | bytearray | np.ndarray, width: int) -> tuple[int, int] | None:
    validate_packed(raw, width)
    array = raw.reshape(-1) if isinstance(raw, np.ndarray) else np.frombuffer(raw, dtype=np.uint8)
    nonzero = np.flatnonzero(array)
    if not nonzero.size: return None
    byte = int(nonzero[0]); coordinate = 4 * byte + int(FIRST_TRIT[int(array[byte])])
    return None if coordinate >= width else (coordinate, int(FIRST_VALUE[int(array[byte])]))


def packed_trit(raw: np.ndarray, coordinate: int) -> int:
    require(raw.dtype == np.uint8 and 0 <= coordinate < PHYSICAL_WIDTH,
            "checker_packed_trit_shape")
    return int(DIGITS[int(raw[coordinate // 4]), coordinate % 4])


def axpy(destination: np.ndarray, source: np.ndarray, scalar: int) -> None:
    require(scalar in (1, 2) and destination.dtype == np.uint8 and source.dtype == np.uint8 and
            destination.size == source.size, "axpy_shape")
    destination[:] = PACKED_AXPY[scalar - 1, destination, source]


def scale_two(destination: np.ndarray) -> None:
    destination[:] = SCALE_TWO[destination]


def _read_json(path: Path, reason: str) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    try: value = json.loads(raw.decode("ascii"))
    except Exception as exc: raise ValueError(reason) from exc
    require(isinstance(value, dict) and raw == canonical(value), reason + ":canonical")
    return value, raw


def _receipt(path: Path, expected: dict[str, Any], reason: str) -> None:
    require(path.name == expected["file"] and plain_int(expected["bytes"]), reason)
    require(path.is_file() and path.stat().st_size == expected["bytes"] and
            sha_file(path) == expected["sha256"], reason)


def _source_records(root: Path, live_parent: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest, _ = _read_json(root / "manifest.json", "checker_connection_manifest")
    keys = {"schema", "status", "offers", "rank", "dependent", "reduction_count",
             "coefficient", "lower", "top", "instruction", "final_rolling_head",
             "candidate_roster", "source_ancestry", "p1_identity", "task712",
             "A0", "COMMON", "COFINAL_LIFT", "FAKE", "IHARA", "verified"}
    require(set(manifest) == keys and manifest["schema"] == CONNECTION_SCHEMA and
            manifest["status"] == "CANONICAL_P1_PHYSICAL_CONNECTION_CANDIDATE",
            "checker_connection_manifest_shape")
    require(plain_int(manifest["offers"]) and 0 <= manifest["offers"] <= MAX_CONNECTION_OFFERS and
            manifest["rank"] + manifest["dependent"] <= manifest["offers"], "checker_connection_counts")
    require(manifest["candidate_roster"] == ["coefficient.bin", "lower.bin", "top.bin", "instructions.jsonl", "manifest.json"],
            "checker_connection_roster")
    require({p.name for p in root.iterdir() if p.is_file()} ==
            set(manifest["candidate_roster"]), "checker_connection_file_roster")
    require(isinstance(manifest["source_ancestry"], dict) and manifest["source_ancestry"],
            "checker_source_ancestry")
    require(isinstance(manifest["p1_identity"], dict) and manifest["p1_identity"],
            "checker_p1_identity")
    require(isinstance(manifest["task712"], dict) and manifest["task712"],
            "checker_task712_identity")
    instruction = manifest["instruction"]
    require(isinstance(instruction, dict) and
            set(instruction) == {"path", "rows", "bytes", "sha256", "final_lf", "eof", "final_head"} and
            instruction["path"] == "instructions.jsonl" and instruction["final_lf"] is True and
            instruction["eof"] is True, "checker_instruction_receipt_shape")
    for key, value in SOURCE_CLAIM_FALSE.items():
        require(manifest[key] is value, "checker_connection_claim")
    for name in ("coefficient.bin", "lower.bin", "top.bin", "instructions.jsonl"):
        rec = manifest["coefficient" if name == "coefficient.bin" else "lower" if name == "lower.bin" else "top" if name == "top.bin" else "instruction"]
        require(rec["path"] == name and rec["eof"] is True and (root / name).is_file(), "checker_connection_file")
        _receipt(root / name, {"file": name, "bytes": rec["bytes"], "sha256": rec["sha256"]}, "checker_connection_receipt")
    records: list[dict[str, Any]] = []; rolling = ZERO_HEAD
    source_rank = source_connections = 0
    with (root / "instructions.jsonl").open("rb") as stream:
        for offer in range(manifest["offers"]):
            line = stream.readline(); require(line and line.endswith(b"\n"), "checker_instruction_eof")
            value = json.loads(line.decode("ascii")); require(line == canonical(value), "checker_instruction_canonical")
            required = {"offer", "kind", "source", "ell_sha256", "g_sha256", "top", "coefficient", "lower", "reductions", "lead", "sigma", "lower_zero", "rank", "dependent", "rolling_sha256"}
            require(set(value) == required and value["offer"] == offer and value["kind"] in ("pivot", "connection"), "checker_instruction_shape")
            source = value["source"]
            require(isinstance(source, dict) and set(source) == {"node", "instruction_sha256", "p1_sha256", "cache_row_sha256", "predecessor", "ancestry_sha256"} and source["node"] == offer, "checker_source_shape")
            for key in ("instruction_sha256", "p1_sha256", "cache_row_sha256", "predecessor", "ancestry_sha256"): digest(source[key], "checker_source_digest")
            for key in ("ell_sha256", "g_sha256"): digest(value[key], "checker_input_digest")
            for key, row_bytes in (("top", PHYSICAL_BYTES), ("coefficient", P1_BYTES)):
                rec = value[key]; require(set(rec) == {"offset", "length", "sha256"} and rec["offset"] == offer * row_bytes and rec["length"] == row_bytes, "checker_offer_offset"); digest(rec["sha256"], "checker_offer_digest")
            lower = value["lower"]
            require((value["kind"] == "connection") == value["lower_zero"] and
                    (value["lead"] is None) == value["lower_zero"] and
                    (value["sigma"] is None) == value["lower_zero"], "checker_source_kind")
            if value["kind"] == "pivot":
                require(set(lower) == {"offset", "length", "sha256"} and
                        lower["offset"] == source_rank * LOWER_BYTES and
                        lower["length"] == LOWER_BYTES, "checker_lower_offset")
                digest(lower["sha256"], "checker_lower_digest")
            else:
                require(lower == {"offset": None, "length": LOWER_BYTES,
                                  "sha256": None}, "checker_lower_zero")
            if value["kind"] == "pivot":
                require(value["rank"] == source_rank + 1 and
                        value["dependent"] == source_connections, "checker_source_counts")
                source_rank += 1
            else:
                require(value["rank"] == source_rank and
                        value["dependent"] == source_connections + 1, "checker_source_counts")
                source_connections += 1
            check = dict(value); claimed = check.pop("rolling_sha256")
            require(claimed == sha(bytes.fromhex(rolling) + canonical(check)), "checker_source_rolling")
            rolling = claimed; records.append(value)
        require(stream.read() == b"", "checker_instruction_trailing")
    require(rolling == manifest["final_rolling_head"] == manifest["instruction"]["final_head"] and
            manifest["instruction"]["rows"] == len(records), "checker_source_terminal")
    require(source_rank == manifest["rank"] and source_connections == manifest["dependent"] and
            sum(len(record["reductions"]) for record in records) == manifest["reduction_count"],
            "checker_source_counts")
    if live_parent:
        require({key: manifest[key] for key in LIVE_CONNECTION_COUNTS} ==
                LIVE_CONNECTION_COUNTS, "checker_live_connection_counts")
    return manifest, records


def _target(root: Path, live_parent: bool = False) -> tuple[np.ndarray, dict[str, Any]]:
    if live_parent:
        manifest_path = root / "manifest.json"
        manifest_raw = manifest_path.read_bytes()
        require(len(manifest_raw) == RHO2_MANIFEST["bytes"] and
                sha(manifest_raw) == RHO2_MANIFEST["sha256"],
                "checker_rho2_manifest_live_receipt")
        try:
            manifest = json.loads(manifest_raw.decode("ascii"))
        except Exception as exc:
            raise ValueError("checker_rho2_manifest") from exc
        require(isinstance(manifest, dict) and manifest_raw == canonical(manifest),
                "checker_rho2_manifest:canonical")
    else:
        manifest, manifest_raw = _read_json(root / "manifest.json", "checker_rho2_manifest")
    require({"schema", "marker", "dimensions", "lower_all_zero", "rho2", "files"}.issubset(manifest) and
            manifest["schema"] == TARGET_PAYLOAD_SCHEMA and
            manifest["marker"] == "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE" and
            manifest["dimensions"] == {"lower": LOWER_WIDTH, "packed_rho2": PHYSICAL_BYTES, "top": PHYSICAL_WIDTH} and
            manifest["lower_all_zero"] is True and isinstance(manifest["rho2"], dict), "checker_rho2_shape")
    rho2 = manifest["rho2"]
    require(rho2.get("packed_sha256") == RHO2_PAYLOAD_RECEIPTS["rho2.bin"]["sha256"] or not live_parent, "checker_rho2_manifest_packed_hash")
    require(rho2.get("dense_sha256") == RHO2_PAYLOAD_RECEIPTS["rho2-dense.bin"]["sha256"] or not live_parent, "checker_rho2_manifest_dense_hash")
    require(rho2.get("packing_roundtrip") is True, "checker_rho2_manifest_roundtrip")
    raw_files = manifest["files"]
    require(isinstance(raw_files, dict) and
            (set(raw_files) == {"lower_dense", "path_signatures", "rho2_dense", "rho2_packed", "roots", "signature_buckets", "target_dense"} or
             (not live_parent and set(raw_files) == {"lower_dense", "rho2_dense", "rho2_packed"})), "checker_rho2_manifest_files_shape")
    files: dict[str, dict[str, Any]] = {}
    for role, receipt in raw_files.items():
        require(isinstance(receipt, dict) and set(receipt) == {"bytes", "file", "sha256"} and
                isinstance(receipt["file"], str) and receipt["file"] not in files, "checker_rho2_manifest_file_receipt_shape")
        files[receipt["file"]] = receipt
    require(set(files) == set(RHO2_PAYLOAD_RECEIPTS) or
            (not live_parent and set(files) == {"lower-dense.bin", "rho2-dense.bin", "rho2.bin"}), "checker_rho2_manifest_file_roster")
    require((root / "acquisition.json").is_file(), "checker_rho2_acquisition_missing")
    acquisition, _ = _read_json(root / "acquisition.json", "checker_rho2_acquisition")
    fixture = False
    if live_parent:
        require(acquisition == RHO2_ACQUISITION, "checker_rho2_live_acquisition")
    else:
        fixture = acquisition.get("fixture_only") is True
    if fixture:
        require(set(files) == {"rho2.bin", "rho2-dense.bin", "lower-dense.bin"}, "checker_rho2_roster")
    else:
        require(set(files) == set(RHO2_PAYLOAD_RECEIPTS) and
                all(files[name] == expected for name, expected in RHO2_PAYLOAD_RECEIPTS.items()),
                "checker_rho2_live_receipt")
        _receipt(root / "task640-verdict.json", RHO2_VERDICT, "checker_rho2_verdict")
    require({p.name for p in root.iterdir() if p.is_file()} ==
            set(files) | {"manifest.json", "acquisition.json", "task640-verdict.json"},
            "checker_rho2_file_roster")
    for name, rec in files.items(): _receipt(root / name, rec, "checker_rho2_receipt")
    packed = (root / "rho2.bin").read_bytes(); dense = (root / "rho2-dense.bin").read_bytes(); lower = (root / "lower-dense.bin").read_bytes()
    require(len(packed) == PHYSICAL_BYTES and len(dense) == PHYSICAL_WIDTH and len(lower) == LOWER_WIDTH and
            sha(packed) == rho2["packed_sha256"] and sha(dense) == rho2["dense_sha256"] and
            sha(lower) == files["lower-dense.bin"]["sha256"], "checker_rho2_digest")
    decoded = unpack(packed, PHYSICAL_WIDTH)
    require(decoded.tobytes() == dense and not np.any(np.frombuffer(lower, dtype=np.uint8)), "checker_rho2_dense")
    return np.frombuffer(packed, dtype=np.uint8).copy(), manifest


def _replay_connection(root: Path, records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[bytes], list[bytes], dict[str, int]]:
    top_stream = (root / "top.bin").open("rb", buffering=0); coeff_stream = (root / "coefficient.bin").open("rb", buffering=0)
    pivots: list[dict[str, Any]] = []; physical_rows: list[bytes] = []; coeff_rows: list[bytes] = []
    expected: list[dict[str, Any]] = []; dependent = skipped = 0; reductions_total = 0
    try:
        for offer, source in enumerate(records):
            if source["kind"] != "connection":
                expected.append({"offer": offer, "kind": "skipped", "source": source,
                                 "source_kind": source["kind"], "top": source["top"],
                                 "coefficient": source["coefficient"], "reductions": [],
                                 "lead": None, "sigma": None, "lower_zero": False,
                                 "physical_zero": None, "physical_offset": None,
                                 "coefficient_offset": None, "rank": len(pivots),
                                 "dependent": dependent}); skipped += 1; continue
            top_stream.seek(source["top"]["offset"]); top = top_stream.read(PHYSICAL_BYTES)
            coeff_stream.seek(source["coefficient"]["offset"]); coeff = coeff_stream.read(P1_BYTES)
            require(sha(top) == source["top"]["sha256"] and sha(coeff) == source["coefficient"]["sha256"], "checker_offer_hash")
            acc = np.frombuffer(bytearray(top), dtype=np.uint8); coeff_acc = np.frombuffer(bytearray(coeff), dtype=np.uint8); reductions: list[list[int]] = []
            # Sweep each existing pivot's own coordinate in insertion order.
            # A free coordinate before a pivot lead must not terminate this
            # scan; later pivots have already been reduced at earlier leads.
            for pivot_id, pivot in enumerate(pivots):
                scalar = packed_trit(acc, pivot["lead"])
                if scalar == 0: continue
                prow = np.frombuffer(physical_rows[pivot_id], dtype=np.uint8); crow = np.frombuffer(coeff_rows[pivot_id], dtype=np.uint8)
                axpy(acc, prow, scalar); axpy(coeff_acc, crow, scalar); reductions.append([pivot_id, scalar]); reductions_total += 1
            require(all(packed_trit(acc, pivot["lead"]) == 0 for pivot in pivots), "checker_unreduced")
            rem = first_nonzero(acc, PHYSICAL_WIDTH)
            sigma = None if rem is None else (2 if rem[1] == 2 else 1)
            if sigma == 2: scale_two(acc); scale_two(coeff_acc); rem = first_nonzero(acc, PHYSICAL_WIDTH); require(rem is not None and rem[1] == 1, "checker_scale")
            poff = len(physical_rows) * PHYSICAL_BYTES if rem is not None else None; coff = len(coeff_rows) * P1_BYTES if rem is not None else None
            if rem is not None:
                physical_rows.append(bytes(acc)); coeff_rows.append(bytes(coeff_acc)); pivots.append({"offer": offer, "lead": rem[0], "physical_offset": poff, "coefficient_offset": coff});
            else: dependent += 1
            expected.append({"offer": offer, "kind": "physical_pivot" if rem is not None else "physical_dependent", "source": source,
                             "top": source["top"], "coefficient": source["coefficient"], "reductions": reductions,
                             "lead": None if rem is None else rem[0], "sigma": sigma, "lower_zero": True,
                             "physical_zero": rem is None, "physical_offset": poff, "coefficient_offset": coff,
                             "rank": len(pivots), "dependent": dependent})
    finally: top_stream.close(); coeff_stream.close()
    return expected, physical_rows, coeff_rows, {"rank": len(pivots), "dependent": dependent, "skipped": skipped, "reductions": reductions_total}


def _state(root: Path, connection_root: Path, source_manifest: dict[str, Any], source_records: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]], list[bytes], list[bytes]]:
    head, head_raw = _read_json(root / "HEAD", "checker_state_head")
    require(set(head) == {"schema", "generation", "rank", "cursor", "manifest_file", "manifest_sha256", "rolling_head", "eof"} and head["schema"] == STATE_HEAD_SCHEMA and head["manifest_file"] == "manifest.json" and head["eof"] is True, "checker_state_head_shape")
    manifest, manifest_raw = _read_json(root / "manifest.json", "checker_state_manifest")
    require(set(manifest) == STATE_MANIFEST_KEYS and
            sha(manifest_raw) == head["manifest_sha256"] and manifest["schema"] == STATE_SCHEMA and manifest["status"] == "PHYSICAL_STATE_CANDIDATE" and
            manifest["connection_manifest_sha256"] == sha((connection_root / "manifest.json").read_bytes()) and manifest["generation"] == head["generation"] and
            manifest["rank"] == head["rank"] and manifest["cursor"] == head["cursor"] and manifest["instructions"]["final_head"] == head["rolling_head"], "checker_state_head_join")
    require(manifest.get("source_ancestry") == source_manifest["source_ancestry"] and
            manifest.get("p1_identity") == source_manifest["p1_identity"] and
            manifest.get("task712") == source_manifest["task712"],
            "checker_state_source_identity")
    require(manifest.get("candidate_roster") ==
            ["physical.bin", "physical-p1-coeff.bin", "instructions.jsonl", "manifest.json", "HEAD"] and
            {p.name for p in root.iterdir() if p.is_file()} ==
            set(manifest["candidate_roster"]), "checker_state_roster")
    expected, physical_rows, coeff_rows, counts = _replay_connection(connection_root, source_records)
    require(manifest["offers"] == len(source_records) and
            manifest["authenticated_offers"] == len(source_records) and
            manifest["physical_offers"] == counts["rank"] + counts["dependent"] and
            manifest["physical_reduction_bound"] ==
            manifest["physical_offers"] * (manifest["physical_offers"] - 1) // 2 and
            manifest["rank"] == counts["rank"] and
            manifest["dependent"] == counts["dependent"] and
            manifest["skipped"] == counts["skipped"], "checker_state_counts")
    for name, rec in (("physical.bin", manifest["physical"]), ("physical-p1-coeff.bin", manifest["p1_companions"])):
        path = root / name; require(rec["file"] == name and rec["rows"] == counts["rank"] and rec["bytes"] == path.stat().st_size and sha_file(path) == rec["sha256"] and rec["eof"] is True, "checker_state_store")
    require((root / "physical.bin").read_bytes() == b"".join(physical_rows) and (root / "physical-p1-coeff.bin").read_bytes() == b"".join(coeff_rows), "checker_state_rows")
    state_records: list[dict[str, Any]] = []; rolling = ZERO_HEAD
    with (root / "instructions.jsonl").open("rb") as stream:
        for offer, expected_record in enumerate(expected):
            line = stream.readline(); require(line, "checker_state_instruction_eof"); actual = json.loads(line.decode("ascii")); require(line == canonical(actual), "checker_state_instruction_canonical")
            claimed = actual.pop("rolling_sha256"); require(claimed == sha(bytes.fromhex(rolling) + canonical(actual)), "checker_state_instruction_rolling")
            require(actual == expected_record, "checker_state_record")
            actual["rolling_sha256"] = claimed
            rolling = claimed; state_records.append(actual)
        require(stream.read() == b"", "checker_state_instruction_trailing")
    require(rolling == manifest["instructions"]["final_head"] and manifest["instructions"]["rows"] == len(expected) and manifest["instructions"]["eof"] is True, "checker_state_instruction_terminal")
    return manifest, state_records, physical_rows, coeff_rows


def _target_reduction(target: np.ndarray, state: dict[str, Any], state_records: list[dict[str, Any]], physical_rows: list[bytes], coeff_rows: list[bytes]) -> dict[str, Any]:
    acc = target.copy(); expression = np.zeros(P1_BYTES, dtype=np.uint8); pivots = [r for r in state_records if r["kind"] == "physical_pivot"]; reductions: list[dict[str, Any]] = []
    # Match the physical-state rule: inspect every prior pivot lead in
    # insertion order, including when a smaller free coordinate is present.
    for pivot_id, pivot in enumerate(pivots):
        scalar = packed_trit(acc, pivot["lead"])
        if scalar == 0: continue
        row = np.frombuffer(physical_rows[pivot_id], dtype=np.uint8); coeff = np.frombuffer(coeff_rows[pivot_id], dtype=np.uint8); axpy(acc, row, scalar); expression[:] = PACKED_AXPY[(3 - scalar) - 1, expression, coeff]
        reductions.append({"pivot_id": pivot_id, "offer": pivot["offer"], "lead": pivot["lead"], "scalar": scalar, "physical_sha256": sha(bytes(row)), "coefficient_sha256": sha(bytes(coeff))})
    require(all(packed_trit(acc, pivot["lead"]) == 0 for pivot in pivots), "checker_target_unreduced")
    rem = first_nonzero(acc, PHYSICAL_WIDTH)
    return {"schema": "d972.r07.physical-state.target-reduction.v1", "state_generation": state["generation"], "state_head": state["instructions"]["final_head"], "state_rank": state["rank"], "rho2_sha256": sha(target.tobytes()), "reductions": reductions, "remainder_sha256": sha(acc.tobytes()), "remainder": pack(unpack(acc, PHYSICAL_WIDTH), PHYSICAL_WIDTH).hex(), "kind": "ConnectionMember" if rem is None else "Separator", "p1_expression_hex": bytes(expression).hex() if rem is None else None}


def _separator(target: np.ndarray, reduction: dict[str, Any], state_records: list[dict[str, Any]], physical_rows: list[bytes]) -> tuple[dict[str, Any], bytes]:
    rem = unpack(bytes.fromhex(reduction["remainder"]), PHYSICAL_WIDTH); free = first_nonzero(pack(rem, PHYSICAL_WIDTH), PHYSICAL_WIDTH); pivots = [r for r in state_records if r["kind"] == "physical_pivot"]
    require(free is not None and free[0] not in {r["lead"] for r in pivots}, "checker_separator_free")
    functional = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); functional[free[0]] = free[1]; transcript: list[dict[str, Any]] = []
    for index in range(len(pivots) - 1, -1, -1):
        row = unpack(physical_rows[index], PHYSICAL_WIDTH); total = int(np.dot(row.astype(np.uint32), functional.astype(np.uint32)) % 3); value = (-total) % 3; functional[pivots[index]["lead"]] = value
        require(int(np.dot(row.astype(np.uint32), functional.astype(np.uint32)) % 3) == 0, "checker_separator_equation")
        transcript.append({"reverse_index": index, "pivot_id": index, "offer": pivots[index]["offer"], "lead": pivots[index]["lead"], "row_sha256": sha(physical_rows[index]), "lambda_value": int(value), "equation": 0})
    packed = pack(functional, PHYSICAL_WIDTH)
    target_dense = unpack(target, PHYSICAL_WIDTH)
    require(int(np.dot(functional.astype(np.uint32), target_dense.astype(np.uint32)) % 3) == 1, "checker_separator_target")
    return ({"schema": "d972.r07.physical-state.Separator.v1", "kind": "Separator", "state_generation": reduction["state_generation"], "state_head": reduction["state_head"], "state_rank": reduction["state_rank"], "rho2_sha256": reduction["rho2_sha256"], "target_reduction_sha256": sha(canonical(reduction)), "remainder_sha256": reduction["remainder_sha256"], "free_coordinate": free[0], "free_value": free[1], "lambda_sha256": sha(packed), "lambda_bytes": len(packed), "reverse_substitution": transcript, "lambda_rho2": 1, "lambda_physical_pivots": 0, "ACTUAL_CONNECTION_STATE": False, "verified": False}, packed)


def _terminal(root: Path, target: np.ndarray, state: dict[str, Any], state_records: list[dict[str, Any]], physical_rows: list[bytes], coeff_rows: list[bytes], target_manifest_sha: str) -> dict[str, Any]:
    reduction = _target_reduction(target, state, state_records, physical_rows, coeff_rows); reduction["target_parent_manifest_sha256"] = target_manifest_sha; state_sha = sha((root / "manifest.json").read_bytes())
    result = _read_json(root / "../unused", "unused") if False else None
    return {"reduction": reduction, "state_sha": state_sha}


def check_launch(path: Path) -> dict[str, Any]:
    launch, _ = _read_json(path, "checker_launch")
    required = {"schema", "fixture_only", "live_parent", "connection_root", "rho2_root", "state_root", "output_root", "rho2_adapter", "final_artifact", "producer", "checker", "resume"}
    require(set(launch) == required and launch["schema"] == "d972.r07.physical-state-separator.launch.v1" and
            isinstance(launch["fixture_only"], bool) and isinstance(launch["resume"], bool), "checker_launch_shape")
    require(launch["live_parent"] == LIVE_V11 and launch["rho2_adapter"] == RHO2_V4_ADAPTER, "checker_launch_parent")
    if launch["fixture_only"]:
        require(launch["final_artifact"] == {"fixture_only": True}, "checker_fixture_parent")
    else:
        validate_final_artifact(launch["final_artifact"])
    require(launch["producer"] == PRODUCER_V6 and launch["checker"] == CHECKER_V7,
            "checker_source_pin")
    connection = Path(launch["connection_root"]).resolve(); target_root = Path(launch["rho2_root"]).resolve(); state_root = Path(launch["state_root"]).resolve(); output = Path(launch["output_root"]).resolve()
    live_parent = not launch["fixture_only"]
    connection_manifest, source_records = _source_records(connection, live_parent=live_parent)
    target, target_manifest = _target(target_root, live_parent=live_parent)
    state, state_records, physical_rows, coeff_rows = _state(state_root, connection, connection_manifest, source_records)
    reduction = _target_reduction(target, state, state_records, physical_rows, coeff_rows)
    reduction["target_parent_manifest_sha256"] = sha((target_root / "manifest.json").read_bytes())
    expected_kind = reduction["kind"]
    separator_free_coordinate = None
    if expected_kind == "ConnectionMember":
        expected = {"schema": "d972.r07.physical-state.ConnectionMember.v1", "kind": "ConnectionMember", "target_reduction": reduction, "state_manifest_sha256": sha((state_root / "manifest.json").read_bytes()), **CLAIM_FALSE}
        expression = bytes.fromhex(reduction.pop("p1_expression_hex")); ep = output / "member-p1-coeff.bin"; require(ep.is_file() and ep.read_bytes() == expression, "checker_member_expression")
        expected["target_reduction"]["p1_expression"] = {"file": "member-p1-coeff.bin", "bytes": len(expression), "sha256": sha(expression)}
        expected["target_reduction"]["back_substitution"] = [{"pivot_id": x["pivot_id"], "scalar": x["scalar"], "offer": x["offer"]} for x in reduction["reductions"]]
    else:
        expected_separator, lambda_packed = _separator(target, reduction, state_records, physical_rows)
        separator_free_coordinate = expected_separator["free_coordinate"]
        expected = {"schema": "d972.r07.physical-state.Separator.v1", "kind": "Separator", "target_reduction": reduction, "separator": expected_separator, "state_manifest_sha256": sha((state_root / "manifest.json").read_bytes()), **CLAIM_FALSE}
        require((output / "lambda.bin").is_file() and (output / "lambda.bin").read_bytes() == lambda_packed, "checker_lambda_file")
        transcript_raw = (output / "reverse-substitution.jsonl").read_bytes(); require(transcript_raw == b"".join(canonical(x) for x in expected_separator["reverse_substitution"]), "checker_transcript_file")
        expected_separator["lambda_file"] = {"file": "lambda.bin", "bytes": len(lambda_packed), "sha256": sha(lambda_packed)}; expected_separator["transcript_file"] = {"file": "reverse-substitution.jsonl", "bytes": len(transcript_raw), "sha256": sha(transcript_raw)}
    terminal, terminal_raw = _read_json(output / "terminal.json", "checker_terminal")
    result, result_raw = _read_json(output / "result.json", "checker_result")
    require(terminal == expected, "checker_terminal_semantics")
    receipt = result.pop("terminal_receipt", None); require(result == terminal and isinstance(receipt, dict) and receipt == {"file": "terminal.json", "bytes": len(terminal_raw), "sha256": sha(terminal_raw)} and result_raw == canonical({**terminal, "terminal_receipt": receipt}), "checker_result_join")
    for key, value in CLAIM_FALSE.items(): require(terminal[key] == value, "checker_claim_boundary")
    return {"schema": "d972.r07.physical-state-separator.v1.checker-result", "status": "PASS", "kind": expected_kind, "source_offers": len(source_records), "physical_rank": state["rank"], "dependent": state["dependent"], "skipped": state["skipped"], "nonmonotone_insertion": [r["lead"] for r in state_records if r["kind"] == "physical_pivot"] != sorted(r["lead"] for r in state_records if r["kind"] == "physical_pivot"), "reverse_substitution": expected_kind == "Separator", "separator_free_coordinate": separator_free_coordinate, "target_reductions": len(reduction["reductions"]), **CLAIM_FALSE}


def _make_connection(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=False)
    rows: list[tuple[np.ndarray, np.ndarray, bool]] = []
    for offer in range(6):
        top = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); lower_zero = offer in (1, 2, 3, 5)
        if offer == 0: top[7] = 1
        elif offer == 1: top[100] = 1
        elif offer == 2: top[10] = 1
        elif offer == 3: top[10] = 1; top[100] = 1
        elif offer == 4: top[12] = 2
        else: top[300] = 2
        coeff = np.zeros(P1_WIDTH, dtype=np.uint8); coeff[offer] = 1
        rows.append((top, coeff, lower_zero))
    lower_rows = []
    for pivot_index in range(2):
        lower = np.zeros(LOWER_WIDTH, dtype=np.uint8); lower[pivot_index] = 1
        lower_rows.append(pack(lower, LOWER_WIDTH))
    lower_raw = b"".join(lower_rows); zero_lower = pack(np.zeros(LOWER_WIDTH, dtype=np.uint8), LOWER_WIDTH)
    top_raw = b"".join(pack(a, PHYSICAL_WIDTH) for a, _, _ in rows)
    coeff_raw = b"".join(pack(a, P1_WIDTH) for _, a, _ in rows)
    (root / "top.bin").write_bytes(top_raw); (root / "coefficient.bin").write_bytes(coeff_raw); (root / "lower.bin").write_bytes(lower_raw)
    rolling = ZERO_HEAD; lines: list[bytes] = []; rank = dependent = 0
    for offer, (top, coeff, lower_zero) in enumerate(rows):
        h = sha(f"checker-source-{offer}".encode()); source = {"node": offer, "instruction_sha256": h, "p1_sha256": h, "cache_row_sha256": h, "predecessor": ZERO_HEAD, "ancestry_sha256": h}
        top_packed = pack(top, PHYSICAL_WIDTH); coeff_packed = pack(coeff, P1_WIDTH)
        top_rec = {"offset": offer * PHYSICAL_BYTES, "length": PHYSICAL_BYTES, "sha256": sha(top_packed)}
        coeff_rec = {"offset": offer * P1_BYTES, "length": P1_BYTES, "sha256": sha(coeff_packed)}
        if lower_zero:
            ell_raw = zero_lower; kind = "connection"
            lower_rec = {"offset": None, "length": LOWER_BYTES, "sha256": None}
            record_rank, record_dependent = rank, dependent + 1; dependent += 1
        else:
            ell_raw = lower_rows[rank]; kind = "pivot"
            lower_rec = {"offset": rank * LOWER_BYTES, "length": LOWER_BYTES, "sha256": sha(ell_raw)}
            record_rank, record_dependent = rank + 1, dependent; rank += 1
        record = {"offer": offer, "kind": kind, "source": source,
                  "ell_sha256": sha(ell_raw), "g_sha256": sha(top_packed),
                  "top": top_rec, "coefficient": coeff_rec, "lower": lower_rec,
                  "reductions": [], "lead": None if lower_zero else (100 if offer == 0 else 10),
                  "sigma": None if lower_zero else 1, "lower_zero": lower_zero,
                  "rank": record_rank, "dependent": record_dependent}
        body = dict(record); claimed = sha(bytes.fromhex(rolling) + canonical(body)); record["rolling_sha256"] = claimed; rolling = claimed; lines.append(canonical(record))
    instruction_raw = b"".join(lines); (root / "instructions.jsonl").write_bytes(instruction_raw)
    manifest = {"schema": CONNECTION_SCHEMA, "status": "CANONICAL_P1_PHYSICAL_CONNECTION_CANDIDATE", "offers": 6, "rank": 2, "dependent": 4, "reduction_count": 0,
                "coefficient": {"path": "coefficient.bin", "rows": 6, "bytes": len(coeff_raw), "sha256": sha(coeff_raw), "eof": True},
                "lower": {"path": "lower.bin", "rows": 2, "bytes": len(lower_raw), "sha256": sha(lower_raw), "eof": True},
                "top": {"path": "top.bin", "rows": 6, "bytes": len(top_raw), "sha256": sha(top_raw), "eof": True},
                "instruction": {"path": "instructions.jsonl", "rows": 6, "bytes": len(instruction_raw), "sha256": sha(instruction_raw), "final_lf": True, "eof": True, "final_head": rolling},
                "final_rolling_head": rolling, "candidate_roster": ["coefficient.bin", "lower.bin", "top.bin", "instructions.jsonl", "manifest.json"],
                "source_ancestry": {"fixture": "accepted-v6-source-ancestry"}, "p1_identity": {"fixture": "accepted-v6-p1"},
                "task712": {"fixture": "accepted-task712-v4"}, **SOURCE_CLAIM_FALSE}
    (root / "manifest.json").write_bytes(canonical(manifest)); return root


def _make_target(root: Path, target: np.ndarray) -> Path:
    root.mkdir(parents=True, exist_ok=False); packed = pack(target, PHYSICAL_WIDTH); dense = target.tobytes(); lower = bytes(32260); (root / "rho2.bin").write_bytes(packed); (root / "rho2-dense.bin").write_bytes(dense); (root / "lower-dense.bin").write_bytes(lower)
    manifest = {"schema": TARGET_PAYLOAD_SCHEMA, "marker": "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE", "dimensions": {"lower": LOWER_WIDTH, "packed_rho2": PHYSICAL_BYTES, "top": PHYSICAL_WIDTH}, "lower_all_zero": True, "rho2": {"packed_sha256": sha(packed), "dense_sha256": sha(dense), "packing_roundtrip": True}, "files": {"rho2_packed": {"file": "rho2.bin", "bytes": len(packed), "sha256": sha(packed)}, "rho2_dense": {"file": "rho2-dense.bin", "bytes": len(dense), "sha256": sha(dense)}, "lower_dense": {"file": "lower-dense.bin", "bytes": len(lower), "sha256": sha(lower)}}}; (root / "manifest.json").write_bytes(canonical(manifest)); (root / "acquisition.json").write_bytes(canonical({"fixture_only": True})); (root / "task640-verdict.json").write_bytes(canonical({"schema": TARGET_CHECKER_SCHEMA, "marker": "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CHECKER_PASS", "payload_manifest_sha256": sha(canonical(manifest)), "fixture_only": True})); return root


def _fixture_state_and_terminal(base: Path, connection: Path, target: Path, state: Path, output: Path) -> Path:
    source_manifest, source_records = _source_records(connection); expected, physical, coeff, counts = _replay_connection(connection, source_records); state.mkdir(parents=True, exist_ok=False); (state / "physical.bin").write_bytes(b"".join(physical)); (state / "physical-p1-coeff.bin").write_bytes(b"".join(coeff)); rolling = ZERO_HEAD; lines: list[bytes] = []
    for record in expected:
        body = dict(record); claimed = sha(bytes.fromhex(rolling) + canonical(body)); body["rolling_sha256"] = claimed; rolling = claimed; lines.append(canonical(body))
    physical_raw = b"".join(physical); coeff_raw = b"".join(coeff); instruction_raw = b"".join(lines)
    (state / "instructions.jsonl").write_bytes(instruction_raw); manifest = {"schema": STATE_SCHEMA, "status": "PHYSICAL_STATE_CANDIDATE", "connection_manifest_sha256": sha((connection / "manifest.json").read_bytes()), "source_ancestry": source_manifest["source_ancestry"], "p1_identity": source_manifest["p1_identity"], "task712": source_manifest["task712"], "cursor": 6, "offers": 6, "authenticated_offers": 6, "physical_offers": counts["rank"] + counts["dependent"], "physical_reduction_bound": (counts["rank"] + counts["dependent"]) * (counts["rank"] + counts["dependent"] - 1) // 2, "rank": counts["rank"], "dependent": counts["dependent"], "skipped": counts["skipped"], "generation": 6, "physical": {"file": "physical.bin", "rows": counts["rank"], "bytes": len(physical_raw), "sha256": sha(physical_raw), "eof": True}, "p1_companions": {"file": "physical-p1-coeff.bin", "rows": counts["rank"], "bytes": len(coeff_raw), "sha256": sha(coeff_raw), "eof": True}, "instructions": {"file": "instructions.jsonl", "rows": 6, "bytes": len(instruction_raw), "sha256": sha(instruction_raw), "final_head": rolling, "eof": True}, "candidate_roster": ["physical.bin", "physical-p1-coeff.bin", "instructions.jsonl", "manifest.json", "HEAD"], **CLAIM_FALSE}; (state / "manifest.json").write_bytes(canonical(manifest)); head = {"schema": STATE_HEAD_SCHEMA, "generation": 6, "rank": counts["rank"], "cursor": 6, "manifest_file": "manifest.json", "manifest_sha256": sha((state / "manifest.json").read_bytes()), "rolling_head": rolling, "eof": True}; (state / "HEAD").write_bytes(canonical(head))
    target_value, target_manifest = _target(target); reduction = _target_reduction(target_value, manifest, expected, physical, coeff); reduction["target_parent_manifest_sha256"] = sha((target / "manifest.json").read_bytes()); output.mkdir(parents=True, exist_ok=False); state_sha = sha((state / "manifest.json").read_bytes())
    if reduction["kind"] == "ConnectionMember":
        expression = bytes.fromhex(reduction.pop("p1_expression_hex")); (output / "member-p1-coeff.bin").write_bytes(expression); reduction["p1_expression"] = {"file": "member-p1-coeff.bin", "bytes": len(expression), "sha256": sha(expression)}; reduction["back_substitution"] = [{"pivot_id": x["pivot_id"], "scalar": x["scalar"], "offer": x["offer"]} for x in reduction["reductions"]]; terminal = {"schema": "d972.r07.physical-state.ConnectionMember.v1", "kind": "ConnectionMember", "target_reduction": reduction, "state_manifest_sha256": state_sha, **CLAIM_FALSE}
    else:
        sep, packed = _separator(target_value, reduction, expected, physical); (output / "lambda.bin").write_bytes(packed); transcript = b"".join(canonical(x) for x in sep["reverse_substitution"]); (output / "reverse-substitution.jsonl").write_bytes(transcript); sep["lambda_file"] = {"file": "lambda.bin", "bytes": len(packed), "sha256": sha(packed)}; sep["transcript_file"] = {"file": "reverse-substitution.jsonl", "bytes": len(transcript), "sha256": sha(transcript)}; terminal = {"schema": "d972.r07.physical-state.Separator.v1", "kind": "Separator", "target_reduction": reduction, "separator": sep, "state_manifest_sha256": state_sha, **CLAIM_FALSE}
    terminal_raw = canonical(terminal); (output / "terminal.json").write_bytes(terminal_raw); receipt = {"file": "terminal.json", "bytes": len(terminal_raw), "sha256": sha(terminal_raw)}; (output / "result.json").write_bytes(canonical({**terminal, "terminal_receipt": receipt})); return _launch(base, connection, target, state, output)


def _launch(base: Path, connection: Path, target: Path, state: Path, output: Path) -> Path:
    launch = {"schema": "d972.r07.physical-state-separator.launch.v1", "fixture_only": True, "live_parent": LIVE_V11, "resume": False, "connection_root": str(connection), "rho2_root": str(target), "state_root": str(state), "output_root": str(output), "rho2_adapter": RHO2_V4_ADAPTER, "final_artifact": {"fixture_only": True}, "producer": PRODUCER_V6, "checker": CHECKER_V7}; path = base / "launch.json"; path.write_bytes(canonical(launch)); return path


def selftest() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="d972-r07-check-state-v1-") as td:
        base = Path(td); connection = _make_connection(base / "connection"); member_target = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); member_target[[100, 10, 300]] = 1; target = _make_target(base / "target", member_target)
        old_shape = base / "target-old-v1-list"; shutil.copytree(target, old_shape)
        old_manifest = json.loads((old_shape / "manifest.json").read_text("ascii")); old_manifest["files"] = list(old_manifest["files"].values()); old_manifest["lower_zero_coordinates"] = LOWER_WIDTH; old_manifest["rho2_sha256"] = old_manifest["rho2"]["packed_sha256"]; old_manifest["rho2_dense_sha256"] = old_manifest["rho2"]["dense_sha256"]; old_manifest["lower_dense_sha256"] = old_manifest["files"][2]["sha256"]; old_manifest.pop("dimensions"); old_manifest.pop("lower_all_zero"); old_manifest.pop("rho2"); (old_shape / "manifest.json").write_bytes(canonical(old_manifest))
        try: _target(old_shape)
        except ValueError: old_manifest_shape_rejected = True
        else: raise ValueError("old_manifest_shape_accepted")
        state = base / "state"; output = base / "output"; launch = _fixture_state_and_terminal(base, connection, target, state, output); report_member = check_launch(launch); require(report_member["kind"] == "ConnectionMember", "checker_member_fixture")
        # A fresh outside-span target and independently generated state/output
        # exercise the reverse insertion sequence [300,10,100].
        # Coordinate 5 is numerically before existing pivot lead 100; target
        # reduction must still eliminate lead 100 before selecting free=5.
        outside = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); outside[[5, 100]] = 1; target2 = _make_target(base / "target2", outside); state2 = base / "state2"; output2 = base / "output2"; launch2 = _fixture_state_and_terminal(base, connection, target2, state2, output2); report_sep = check_launch(launch2); require(report_sep["kind"] == "Separator" and report_sep["separator_free_coordinate"] == 5 and report_sep["target_reductions"], "checker_separator_fixture")
        # Reach ordinary validation on a coherent-copy mutation, not a dead
        # helper: changing the authenticated top row makes the parent hash
        # fail before any terminal can be accepted.
        bad = base / "bad"; shutil.copytree(base, bad, ignore=shutil.ignore_patterns("bad")); bad_top = bad / "connection" / "top.bin"; raw = bytearray(bad_top.read_bytes()); raw[0] = (raw[0] + 1) % 81; bad_top.write_bytes(bytes(raw)); bad_launch = bad / "launch.json"; bad_launch_text = json.loads(bad_launch.read_text("ascii")); bad_launch_text["connection_root"] = str((bad / "connection").resolve()); bad_launch_text["state_root"] = str((bad / "state").resolve()); bad_launch_text["output_root"] = str((bad / "output").resolve()); bad_launch.write_bytes(canonical(bad_launch_text));
        try: check_launch(bad_launch)
        except ValueError as exc: require(str(exc) in ("checker_connection_receipt", "checker_offer_hash"), "checker_top_mutation")
        else: raise ValueError("checker_top_mutation_accepted")
        def expect_rejection(label: str, mutate: Any, separator: bool = False) -> str:
            work = Path(tempfile.mkdtemp(prefix="d972-r07-mutation-")); case = work / "case"
            try:
                shutil.copytree(base, case)
                launch_path = case / "launch.json"
                launch_value = json.loads(launch_path.read_text("ascii"))
                launch_value["connection_root"] = str((case / "connection").resolve())
                launch_value["rho2_root"] = str((case / ("target2" if separator else "target")).resolve())
                launch_value["state_root"] = str((case / ("state2" if separator else "state")).resolve())
                launch_value["output_root"] = str((case / ("output2" if separator else "output")).resolve())
                mutate(case, launch_value)
                launch_path.write_bytes(canonical(launch_value))
                try:
                    check_launch(launch_path)
                except Exception as exc:
                    return "REJECTED:" + type(exc).__name__ + ":" + str(exc)
                raise ValueError(label + "_accepted")
            finally:
                shutil.rmtree(work, ignore_errors=True)

        def edit_connection_file(name: str) -> Any:
            def mutate(case: Path, launch: dict[str, Any]) -> None:
                path = case / "connection" / name; raw = bytearray(path.read_bytes()); raw[0] = (raw[0] + 1) % 81; path.write_bytes(bytes(raw))
            return mutate

        def edit_source_line(field: str) -> Any:
            def mutate(case: Path, launch: dict[str, Any]) -> None:
                path = case / "connection" / "instructions.jsonl"; lines = path.read_bytes().splitlines(keepends=True); value = json.loads(lines[0].decode("ascii")); value["source"][field] = "0" * 64; lines[0] = canonical(value); path.write_bytes(b"".join(lines))
            return mutate

        def edit_state_line(field: str) -> Any:
            def mutate(case: Path, launch: dict[str, Any]) -> None:
                path = case / "state" / "instructions.jsonl"; lines = path.read_bytes().splitlines(keepends=True); value = json.loads(lines[3].decode("ascii")); value[field] = (2 if field == "sigma" else 999); lines[3] = canonical(value); path.write_bytes(b"".join(lines))
            return mutate

        def edit_head(case: Path, launch: dict[str, Any]) -> None:
            path = case / "state" / "HEAD"; value = json.loads(path.read_text("ascii")); value["generation"] += 1; path.write_bytes(canonical(value))

        def edit_connection_manifest(field: str, value: Any) -> Any:
            def mutate(case: Path, launch: dict[str, Any]) -> None:
                path = case / "connection" / "manifest.json"; manifest = json.loads(path.read_text("ascii")); manifest[field] = value; path.write_bytes(canonical(manifest))
            return mutate

        def edit_target_terminal(field: str) -> Any:
            def mutate(case: Path, launch: dict[str, Any]) -> None:
                path = case / "output2" / "terminal.json"; terminal = json.loads(path.read_text("ascii")); terminal["target_reduction"][field] = "00" if field == "remainder" else 0; path.write_bytes(canonical(terminal))
            return mutate

        def edit_lambda(case: Path, launch: dict[str, Any]) -> None:
            path = case / "output2" / "lambda.bin"; raw = bytearray(path.read_bytes()); raw[0] = (raw[0] + 1) % 81; path.write_bytes(bytes(raw))

        def edit_terminal_kind(case: Path, launch: dict[str, Any]) -> None:
            path = case / "output2" / "terminal.json"; terminal = json.loads(path.read_text("ascii")); terminal["kind"] = "ConnectionMember"; path.write_bytes(canonical(terminal))

        def edit_parent(case: Path, launch: dict[str, Any]) -> None:
            launch["live_parent"]["run"] = "wrong"

        def delete_top(case: Path, launch: dict[str, Any]) -> None:
            (case / "connection" / "top.bin").unlink()

        def add_extra(case: Path, launch: dict[str, Any]) -> None:
            (case / "connection" / "unexpected.bin").write_bytes(b"x")

        def old_target_manifest(case: Path, launch: dict[str, Any]) -> None:
            path = case / "target" / "manifest.json"
            manifest = json.loads(path.read_text("ascii"))
            manifest["files"] = list(manifest["files"].values())
            manifest["lower_zero_coordinates"] = LOWER_WIDTH
            manifest["rho2_sha256"] = manifest["rho2"]["packed_sha256"]
            manifest["rho2_dense_sha256"] = manifest["rho2"]["dense_sha256"]
            manifest["lower_dense_sha256"] = manifest["files"][2]["sha256"]
            manifest.pop("dimensions"); manifest.pop("lower_all_zero"); manifest.pop("rho2")
            path.write_bytes(canonical(manifest))

        def truncate_instructions(case: Path, launch: dict[str, Any]) -> None:
            path = case / "connection" / "instructions.jsonl"; raw = path.read_bytes(); path.write_bytes(raw[:-1])

        mutation_cases = [
            ("top_mutation", edit_connection_file("top.bin"), False),
            ("coefficient_mutation", edit_connection_file("coefficient.bin"), False),
            ("instruction_ancestry_mutation", edit_source_line("ancestry_sha256"), False),
            ("physical_reduction_mutation", edit_state_line("reductions"), False),
            ("scale_mutation", edit_state_line("sigma"), False),
            ("lead_mutation", edit_state_line("lead"), False),
            ("state_head_generation_mutation", edit_head, False),
            ("rho2_mutation", lambda case, launch: (lambda p: p.write_bytes(bytes((bytearray(p.read_bytes())[:1] + bytes([1]) + bytearray(p.read_bytes())[2:]))) )(case / "target" / "rho2.bin"), False),
            ("old_v1_list_manifest_shape", old_target_manifest, False),
            ("target_remainder_mutation", edit_target_terminal("remainder"), True),
            ("target_free_coordinate_mutation", edit_target_terminal("free_coordinate"), True),
            ("lambda_mutation", edit_lambda, True),
            ("terminal_kind_mutation", edit_terminal_kind, True),
            ("wrong_parent_schema", edit_parent, False),
            ("claim_flag_mutation", edit_connection_manifest("A0", True), False),
            ("missing_file", delete_top, False),
            ("extra_file", add_extra, False),
            ("instruction_truncation", truncate_instructions, False),
            ("false_eof", edit_connection_manifest("instruction", {"path": "instructions.jsonl", "rows": 6, "bytes": 0, "sha256": "0" * 64, "final_lf": False, "eof": False, "final_head": ZERO_HEAD}), False),
            ("wrong_manifest_schema", edit_connection_manifest("schema", CONNECTION_SCHEMA + ".wrong"), False),
        ]
        mutation_results = {label: expect_rejection(label, mutate, use_separator)
                            for label, mutate, use_separator in mutation_cases}
        require(all(value.startswith("REJECTED:") for value in mutation_results.values()),
                "mutation_suite_acceptance")
        return {"schema": "d972.r07.physical-state-separator.v2.checker-selftest", "status": "PASS", "independent_fixture": True, "production_manifest_dict": True, "old_v1_list_manifest_shape_rejected": old_manifest_shape_rejected, "member": True, "separator": True, "reverse_insertion": [300, 10, 100], "authenticated_offers": 6, "physical_offers": 4, "physical_reduction_bound": 6, "top_mutation": "REJECTED", "mutation_suite": mutation_results, "all_48384_coordinates": True, "generic_nullspace_solver": False, "final_v11_artifact_tuple": FINAL_V11_ARTIFACT, **CLAIM_FALSE}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__); group = result.add_mutually_exclusive_group(required=True); group.add_argument("--selftest", action="store_true"); group.add_argument("--check-launch", type=Path); return result


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        if args.selftest: print(json.dumps(selftest(), sort_keys=True, separators=(",", ":"))); return 0
        public_launch, _ = _read_json(args.check_launch.resolve(), "checker_launch")
        # Bounded fixtures are exercised through selftest's internal path;
        # the public checker accepts only a live-parent launch and therefore
        # cannot turn a fixture terminal into a public result.
        require(public_launch["fixture_only"] is False,
                "public_fixture_path_disabled")
        print(json.dumps(check_launch(args.check_launch.resolve()), sort_keys=True, separators=(",", ":"))); return 0
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc), "verified": False}, separators=(",", ":")), file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
