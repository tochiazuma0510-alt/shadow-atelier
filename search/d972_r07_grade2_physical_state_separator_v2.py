#!/usr/bin/env python3
"""R07 file-backed physical state and v536 separator producer.

This is the bounded implementation boundary for the physical connection
state.  It authenticates a v6 connection parent, keeps packed physical and
P1-companion rows on disk, and constructs either a connection MEMBER
back-substitution or the canonical reverse-insertion-order separator.  The
live v11 artifact receipt is bound to the exact owner-supplied tuple below;
bounded fixtures remain explicitly fixture-only and never masquerade as it.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable, Sequence

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
CHECKPOINT_INTERVAL = 128
CONNECTION_SCHEMA = "d972.r07.canonical-p1-physical-connection.v6"
CHECKPOINT_SCHEMA = "d972.r07.canonical-p1-physical-connection.checkpoint.v6"
STATE_CHECKPOINT_SCHEMA = "d972.r07.physical-state.checkpoint.v1"
STATE_SCHEMA = "d972.r07.physical-state.v1"
STATE_HEAD_SCHEMA = "d972.r07.physical-state.HEAD.v1"
TARGET_SCHEMA = "d972.r07.targeted-grade2.rho2-v9.acquisition.v1"
TARGET_PAYLOAD_SCHEMA = "d972.r07.a0.fresh-precision2-endpoint-signature.v9"
TARGET_CHECKER_SCHEMA = TARGET_PAYLOAD_SCHEMA + ".checker"
ZERO_HEAD = "00" * 32
LIVE_CONNECTION_COUNTS = {
    "offers": 8059,
    "rank": 6705,
    "dependent": 1354,
    "reduction_count": 7665974,
    "final_rolling_head": "3cb1bcf691038d71082b8d4774c5dd8898a239e71ef64da22ec486ba923cb8bd",
}

# These are the immutable live-parent pins.  The final artifact tuple was
# supplied by root after the v11 run completed; it is compared byte-for-byte
# on the ordinary (non-fixture) launch path.
LIVE_V11 = {
    "repository": REPOSITORY,
    "workflow": ".github/workflows/d972-r07-canonical-p1-physical-connection-v11.yml",
    "run": "33876776771",
    "attempt": "1",
    "head": "b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2",
    "job": "101035535909",
    "producer_v6_sha256": "6c450c2d82f7ad5795d9188e2912a4587882ae3fb9351217f33393c96f75526a",
    "checker_v7_sha256": "b5b210f6063a8fed6172417d350510eeccbafa0f60e5e676aa2732fee5e8757e",
    "workflow_sha256": "c7f3c9a8b728fa5ab0bd6be0b550b381e5b33d8ce1f59523dc04fb82b306fb74",
}
FINAL_V11_ARTIFACT: dict[str, Any] | None = {
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
RHO2_V4_ADAPTER = {
    "schema": TARGET_SCHEMA,
    "run_id": 33839962829,
    "run_attempt": 1,
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
    "rho2.bin": {"file": "rho2.bin", "bytes": 12096,
                 "sha256": "b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e"},
    "rho2-dense.bin": {"file": "rho2-dense.bin", "bytes": 48384,
                       "sha256": "abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e"},
    "lower-dense.bin": {"file": "lower-dense.bin", "bytes": 32260,
                        "sha256": "c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830"},
    "target-dense.bin": {"file": "target-dense.bin", "bytes": 80644,
                         "sha256": "122dca3cf3dc3299214f1ba4c2bc5b82dbe64e510f8aef482329316c2a935ea2"},
    "path-signatures.json": {"file": "path-signatures.json", "bytes": 28393211,
                             "sha256": "ef7fbd1d44647c058b33a1c18894ff5411dcd7870e7cf7e24b6763b68557ab25"},
    "signature-buckets.json": {"file": "signature-buckets.json", "bytes": 46469668,
                               "sha256": "e67876dce3bb144ad6afa4895236c8fc37fbc0488c135f9903d8288039829c43"},
    "authenticated-roots.json": {"file": "authenticated-roots.json", "bytes": 255846,
                                  "sha256": "af1b035e0eb0af6e593770affb52a52905609fd9c19e988b0b7e8cf69e7592c5"},
}
RHO2_MANIFEST = {"bytes": 26047,
                 "sha256": "55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488"}
RHO2_VERDICT = {"file": "task640-verdict.json", "bytes": 418,
                "sha256": "cdf0654738a10acf59844df3b9dda5ab8efdf2e387bba7d69b691a4ad46b2848"}
PRODUCER_V6 = {"bytes": 68202, "lf": 690,
               "sha256": LIVE_V11["producer_v6_sha256"]}
CHECKER_V7 = {"bytes": 100990, "lf": 1768,
              "sha256": LIVE_V11["checker_v7_sha256"]}
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

COUNTERS: dict[str, int] = {
    "connection_offers": 0, "physical_reductions": 0,
    "physical_pivots": 0, "physical_dependents": 0,
    "physical_positioned_reads": 0, "p1_positioned_reads": 0,
    "target_reductions": 0, "reverse_substitution": 0,
}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path, chunk_bytes: int = 1024 * 1024) -> str:
    """Hash a store incrementally so authentication has bounded RSS."""
    hasher = hashlib.sha256()
    with path.open("rb", buffering=0) as stream:
        while True:
            chunk = stream.read(chunk_bytes)
            if not chunk:
                return hasher.hexdigest()
            hasher.update(chunk)


def fail(reason: str) -> None:
    raise ValueError(reason)


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def digest(value: Any, reason: str) -> None:
    require(isinstance(value, str) and len(value) == 64 and
            all(c in "0123456789abcdef" for c in value), reason)


def fsync_file(path: Path) -> None:
    # Windows rejects fsync on a read-only descriptor; r+b is also valid for
    # the read-only durability check and keeps the operation portable.
    with path.open("r+b") as stream:
        os.fsync(stream.fileno())


def process_rss_bytes() -> int:
    """Return a small, platform-local resident-set measurement for receipts."""
    if os.name == "nt":
        class Counters(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
                        ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]
        counters = Counters(); counters.cb = ctypes.sizeof(Counters)
        try:
            ok = ctypes.windll.psapi.GetProcessMemoryInfo(
                ctypes.windll.kernel32.GetCurrentProcess(),
                ctypes.byref(counters), counters.cb)
            if ok:
                return int(counters.WorkingSetSize)
        except (AttributeError, OSError):
            pass
    else:
        try:
            pages = int(Path("/proc/self/statm").read_text("ascii").split()[1])
            return pages * int(os.sysconf("SC_PAGE_SIZE"))
        except (FileNotFoundError, IndexError, ValueError, OSError):
            pass
    return 1


def atomic_json(path: Path, value: Any) -> bytes:
    raw = canonical(value)
    temporary = path.with_name(path.name + ".tmp-" + str(os.getpid()))
    temporary.write_bytes(raw)
    fsync_file(temporary)
    os.replace(temporary, path)
    return raw


def write_bytes_durable(path: Path, raw: bytes) -> None:
    path.write_bytes(raw)
    fsync_file(path)


def _digits(value: int) -> tuple[int, int, int, int]:
    require(0 <= value <= 80, "packed_byte_out_of_range")
    return value % 3, (value // 3) % 3, (value // 9) % 3, (value // 27) % 3


DIGITS = np.asarray([_digits(i) for i in range(81)], dtype=np.uint8)
PACKED_AXPY = np.empty((2, 81, 81), dtype=np.uint8)
for _scalar in (1, 2):
    for _left in range(81):
        for _right in range(81):
            PACKED_AXPY[_scalar - 1, _left, _right] = sum(
                ((int(DIGITS[_left, j]) - _scalar * int(DIGITS[_right, j])) % 3) * 3 ** j
                for j in range(4))
SCALE_TWO = np.asarray([
    sum((2 * int(DIGITS[i, j]) % 3) * 3 ** j for j in range(4))
    for i in range(81)], dtype=np.uint8)
FIRST_TRIT = np.full(81, -1, dtype=np.int8)
FIRST_VALUE = np.zeros(81, dtype=np.uint8)
for _value in range(1, 81):
    for _position, _digit in enumerate(DIGITS[_value]):
        if _digit:
            FIRST_TRIT[_value] = _position
            FIRST_VALUE[_value] = _digit
            break


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
    validate_packed(output, width)
    return output.tobytes()


def unpack(raw: bytes | bytearray | np.ndarray, width: int) -> np.ndarray:
    validate_packed(raw, width)
    packed = np.frombuffer(raw, dtype=np.uint8) if not isinstance(raw, np.ndarray) else raw
    output = np.empty(width, dtype=np.uint8)
    for position in range(4):
        output[position::4] = DIGITS[packed, position][:output[position::4].size]
    return output


def first_nonzero(raw: bytes | bytearray | np.ndarray, width: int) -> tuple[int, int] | None:
    validate_packed(raw, width)
    array = raw.reshape(-1) if isinstance(raw, np.ndarray) else np.frombuffer(raw, dtype=np.uint8)
    nonzero = np.flatnonzero(array)
    if not nonzero.size:
        return None
    byte_index = int(nonzero[0])
    coordinate = 4 * byte_index + int(FIRST_TRIT[int(array[byte_index])])
    return None if coordinate >= width else (coordinate, int(FIRST_VALUE[int(array[byte_index])]))


def packed_trit(raw: np.ndarray, coordinate: int) -> int:
    """Read one packed coordinate without expanding the 48,384-trit row."""
    require(raw.dtype == np.uint8 and 0 <= coordinate < PHYSICAL_WIDTH,
            "packed_trit_shape")
    return int(DIGITS[int(raw[coordinate // 4]), coordinate % 4])


def axpy_inplace(destination: np.ndarray, source: np.ndarray, scalar: int) -> None:
    require(scalar in (1, 2) and destination.dtype == np.uint8 and
            source.dtype == np.uint8 and destination.size == source.size,
            "axpy_shape")
    destination[:] = PACKED_AXPY[scalar - 1, destination, source]


def scale_two_inplace(destination: np.ndarray) -> None:
    destination[:] = SCALE_TWO[destination]


class PositionedStore:
    """Unbuffered packed store with one caller-owned reusable read buffer."""
    def __init__(self, path: Path, row_bytes: int, mode: str = "r+b") -> None:
        require(mode in ("w+b", "r+b"), "store_mode")
        self.path, self.row_bytes = path, row_bytes
        self.stream = path.open(mode, buffering=0)

    def append(self, raw: bytes) -> int:
        require(len(raw) == self.row_bytes, "store_append_shape")
        offset = self.stream.seek(0, os.SEEK_END)
        require(self.stream.write(raw) == self.row_bytes, "store_append")
        return offset

    def read_into(self, offset: int, target: np.ndarray) -> None:
        require(offset >= 0 and offset % self.row_bytes == 0 and
                target.dtype == np.uint8 and target.size == self.row_bytes,
                "store_position")
        view = memoryview(target)
        if hasattr(os, "preadv"):
            got = os.preadv(self.stream.fileno(), [view], offset)
        else:
            self.stream.seek(offset)
            got = self.stream.readinto(view)
        require(got == self.row_bytes, "store_eof")

    def sync(self) -> None:
        self.stream.flush()
        os.fsync(self.stream.fileno())

    def close(self) -> None:
        self.stream.close()


def file_receipt(path: Path) -> dict[str, Any]:
    return {"file": path.name, "bytes": path.stat().st_size,
            "sha256": sha_file(path)}


def _receipt_matches(path: Path, receipt: dict[str, Any], reason: str) -> None:
    require(isinstance(receipt, dict) and set(receipt) == {"file", "bytes", "sha256"}
            and receipt["file"] == path.name and plain_int(receipt["bytes"]), reason)
    require(path.is_file() and path.stat().st_size == receipt["bytes"] and
            sha_file(path) == receipt["sha256"], reason)


def _read_json(path: Path, reason: str) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("ascii"))
    except Exception as exc:
        raise ValueError(reason) from exc
    require(isinstance(value, dict) and raw == canonical(value), reason + ":canonical")
    return value, raw


def validate_live_parent(parent: Any) -> None:
    require(parent == LIVE_V11, "live_v11_parent")


def validate_final_artifact(receipt: Any) -> None:
    require(FINAL_V11_ARTIFACT is not None, "final_v11_artifact_tuple_pending")
    require(receipt == FINAL_V11_ARTIFACT, "final_v11_artifact_tuple")


def validate_launch(path: Path) -> dict[str, Any]:
    launch, raw = _read_json(path, "launch")
    required = {"schema", "fixture_only", "live_parent", "connection_root",
                "rho2_root", "state_root", "output_root", "rho2_adapter",
                "final_artifact", "producer", "checker", "resume"}
    require(set(launch) == required and
            launch["schema"] == "d972.r07.physical-state-separator.launch.v1" and
            isinstance(launch["fixture_only"], bool) and isinstance(launch["resume"], bool) and
            launch["live_parent"] == LIVE_V11 and launch["rho2_adapter"] == RHO2_V4_ADAPTER and
            launch["producer"] == PRODUCER_V6 and launch["checker"] == CHECKER_V7 and raw,
            "launch_parent_binding")
    if launch["fixture_only"]:
        require(launch["final_artifact"] == {"fixture_only": True}, "fixture_launch_binding")
    else:
        validate_final_artifact(launch["final_artifact"])
        # The live public path has no independently authenticated resume artifact
        # authority.  Keep resume available to the bounded internal fixture
        # tests, but fail closed for a public live launch.
        require(launch["resume"] is False, "live_resume_not_exposed")
    for key in ("connection_root", "rho2_root", "state_root", "output_root"):
        require(isinstance(launch[key], str) and launch[key], "launch_path")
    return launch


def _validate_connection_manifest(root: Path) -> tuple[dict[str, Any], bytes]:
    manifest, raw = _read_json(root / "manifest.json", "connection_manifest")
    required = {"schema", "status", "offers", "rank", "dependent",
                "reduction_count", "coefficient", "lower", "top",
                "instruction", "final_rolling_head", "candidate_roster",
                "source_ancestry", "p1_identity", "task712",
                "A0", "COMMON", "COFINAL_LIFT", "FAKE", "IHARA", "verified"}
    require(set(manifest) == required and manifest["schema"] == CONNECTION_SCHEMA and
            manifest["status"] == "CANONICAL_P1_PHYSICAL_CONNECTION_CANDIDATE",
            "connection_manifest_shape")
    require(plain_int(manifest["offers"]) and 0 <= manifest["offers"] <= MAX_CONNECTION_OFFERS and
            plain_int(manifest["rank"]) and plain_int(manifest["dependent"]) and
            manifest["rank"] + manifest["dependent"] <= manifest["offers"],
            "connection_manifest_counts")
    require(manifest["candidate_roster"] ==
            ["coefficient.bin", "lower.bin", "top.bin", "instructions.jsonl", "manifest.json"],
            "connection_manifest_roster")
    require({p.name for p in root.iterdir() if p.is_file()} ==
            set(manifest["candidate_roster"]), "connection_file_roster")
    require(isinstance(manifest["source_ancestry"], dict) and manifest["source_ancestry"],
            "connection_source_ancestry")
    require(isinstance(manifest["p1_identity"], dict) and manifest["p1_identity"],
            "connection_p1_identity")
    require(isinstance(manifest["task712"], dict) and manifest["task712"],
            "connection_task712_identity")
    instruction = manifest["instruction"]
    require(isinstance(instruction, dict) and
            set(instruction) == {"path", "rows", "bytes", "sha256", "final_lf", "eof", "final_head"} and
            instruction["path"] == "instructions.jsonl" and instruction["final_lf"] is True and
            instruction["eof"] is True,
            "connection_instruction_receipt_shape")
    for key, value in SOURCE_CLAIM_FALSE.items():
        require(manifest[key] is value, "connection_claim_boundary")
    return manifest, raw


def _validate_connection_parent(root: Path, live_parent: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest, _ = _validate_connection_manifest(root)
    expected = {"coefficient.bin": manifest["coefficient"],
                "lower.bin": manifest["lower"], "top.bin": manifest["top"],
                "instructions.jsonl": manifest["instruction"]}
    for name, rec in expected.items():
        require(rec["path"] == name and rec["eof"] is True, "connection_parent_receipt")
        digest(rec["sha256"], "connection_parent_digest")
        path = root / name
        require(path.is_file() and path.stat().st_size == rec["bytes"],
                "connection_parent_length")
        require(sha_file(path) == rec["sha256"], "connection_parent_hash")
    records: list[dict[str, Any]] = []
    rolling = ZERO_HEAD
    trailing = b""
    seen_pivots = seen_connections = 0
    with (root / "instructions.jsonl").open("rb") as stream:
        for offer in range(manifest["offers"]):
            line = stream.readline()
            require(line and line.endswith(b"\n"), "connection_instruction_eof")
            value = json.loads(line.decode("ascii"))
            require(line == canonical(value), "connection_instruction_canonical")
            required = {"offer", "kind", "source", "ell_sha256", "g_sha256",
                        "top", "coefficient",
                        "lower", "reductions", "lead", "sigma", "lower_zero",
                        "rank", "dependent", "rolling_sha256"}
            require(isinstance(value, dict) and set(value) == required and
                    value["offer"] == offer and value["kind"] in ("pivot", "connection"),
                    "connection_instruction_shape")
            source = value["source"]
            require(isinstance(source, dict) and set(source) ==
                    {"node", "instruction_sha256", "p1_sha256", "cache_row_sha256",
                     "predecessor", "ancestry_sha256"} and source["node"] == offer,
                    "connection_instruction_source")
            for key in ("instruction_sha256", "p1_sha256", "cache_row_sha256", "predecessor", "ancestry_sha256"):
                digest(source[key], "connection_source_digest")
            for key in ("ell_sha256", "g_sha256"):
                digest(value[key], "connection_instruction_input_digest")
            for key, width, row_bytes in (("top", PHYSICAL_WIDTH, PHYSICAL_BYTES),
                                          ("coefficient", P1_WIDTH, P1_BYTES)):
                rec = value[key]
                require(isinstance(rec, dict) and set(rec) == {"offset", "length", "sha256"}
                        and rec["offset"] == offer * row_bytes and rec["length"] == row_bytes,
                        "connection_instruction_row")
                digest(rec["sha256"], "connection_instruction_row_digest")
                _ = width
            lower = value["lower"]
            require(isinstance(lower, dict) and set(lower) == {"offset", "length", "sha256"},
                    "connection_instruction_lower")
            if value["kind"] == "pivot":
                require(lower["offset"] == seen_pivots * LOWER_BYTES and
                        lower["length"] == LOWER_BYTES,
                        "connection_instruction_lower_offset")
                digest(lower["sha256"], "connection_instruction_lower_digest")
            else:
                require(lower == {"offset": None, "length": LOWER_BYTES,
                                  "sha256": None}, "connection_instruction_lower_zero")
            require((value["kind"] == "connection") == value["lower_zero"],
                    "connection_instruction_kind")
            for reduction in value["reductions"]:
                require(isinstance(reduction, list) and len(reduction) == 2 and
                        all(plain_int(x) for x in reduction), "connection_reduction")
            require((value["lead"] is None) == value["lower_zero"] and
                    (value["sigma"] is None) == value["lower_zero"],
                    "connection_instruction_terminal")
            if value["kind"] == "pivot":
                require(value["rank"] == seen_pivots + 1 and
                        value["dependent"] == seen_connections,
                        "connection_instruction_counts")
                seen_pivots += 1
            else:
                require(value["rank"] == seen_pivots and
                        value["dependent"] == seen_connections + 1,
                        "connection_instruction_counts")
                seen_connections += 1
            check = dict(value)
            previous = check.pop("rolling_sha256")
            require(previous == sha(bytes.fromhex(rolling) + canonical(check)),
                    "connection_instruction_rolling")
            rolling = previous
            records.append(value)
        trailing = stream.read()
    require(trailing == b"", "connection_instruction_trailing")
    require(len(records) == manifest["offers"] and
            rolling == manifest["final_rolling_head"] == manifest["instruction"]["final_head"],
            "connection_instruction_terminal")
    require(manifest["instruction"]["rows"] == len(records), "connection_instruction_rows")
    require(seen_pivots == manifest["rank"] and seen_connections == manifest["dependent"],
            "connection_instruction_counts")
    require(sum(len(record["reductions"]) for record in records) ==
            manifest["reduction_count"], "connection_reduction_count")
    if live_parent:
        require({key: manifest[key] for key in LIVE_CONNECTION_COUNTS} ==
                LIVE_CONNECTION_COUNTS, "live_connection_counts")
    return manifest, records


def _open_input_rows(root: Path) -> tuple[PositionedStore, PositionedStore]:
    return (PositionedStore(root / "top.bin", PHYSICAL_BYTES),
            PositionedStore(root / "coefficient.bin", P1_BYTES))


def _read_target_parent(root: Path, live_parent: bool = False) -> tuple[np.ndarray, dict[str, Any]]:
    if live_parent:
        manifest_path = root / "manifest.json"
        manifest_raw = manifest_path.read_bytes()
        require(len(manifest_raw) == RHO2_MANIFEST["bytes"] and
                sha(manifest_raw) == RHO2_MANIFEST["sha256"],
                "rho2_manifest_live_receipt")
        try:
            manifest = json.loads(manifest_raw.decode("ascii"))
        except Exception as exc:
            raise ValueError("rho2_manifest") from exc
        require(isinstance(manifest, dict) and manifest_raw == canonical(manifest),
                "rho2_manifest:canonical")
    else:
        manifest, manifest_raw = _read_json(root / "manifest.json", "rho2_manifest")
    required = {"schema", "marker", "dimensions", "lower_all_zero", "rho2", "files"}
    require(set(required).issubset(manifest) and
            manifest["schema"] == TARGET_PAYLOAD_SCHEMA and
            manifest["marker"] == "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE" and
            manifest["dimensions"] == {"lower": LOWER_WIDTH, "packed_rho2": PHYSICAL_BYTES,
                                        "top": PHYSICAL_WIDTH} and
            manifest["lower_all_zero"] is True and isinstance(manifest["rho2"], dict),
            "rho2_manifest_shape")
    rho2 = manifest["rho2"]
    require(rho2.get("packed_sha256") == RHO2_PAYLOAD_RECEIPTS["rho2.bin"]["sha256"] or
            not live_parent, "rho2_manifest_packed_hash")
    require(rho2.get("dense_sha256") == RHO2_PAYLOAD_RECEIPTS["rho2-dense.bin"]["sha256"] or
            not live_parent, "rho2_manifest_dense_hash")
    require(rho2.get("packing_roundtrip") is True, "rho2_manifest_roundtrip")
    raw_files = manifest["files"]
    require(isinstance(raw_files, dict) and
            (set(raw_files) == {"lower_dense", "path_signatures", "rho2_dense",
                                "rho2_packed", "roots", "signature_buckets", "target_dense"} or
             (not live_parent and set(raw_files) == {"lower_dense", "rho2_dense", "rho2_packed"})),
            "rho2_manifest_files_shape")
    files: dict[str, dict[str, Any]] = {}
    for role, receipt in raw_files.items():
        require(isinstance(receipt, dict) and set(receipt) == {"bytes", "file", "sha256"} and
                isinstance(receipt["file"], str) and receipt["file"] not in files,
                "rho2_manifest_file_receipt_shape")
        files[receipt["file"]] = receipt
    require(set(files) == set(RHO2_PAYLOAD_RECEIPTS) or
            (not live_parent and set(files) == {"lower-dense.bin", "rho2-dense.bin", "rho2.bin"}),
            "rho2_manifest_file_roster")
    fixture = False
    require((root / "acquisition.json").is_file(), "rho2_acquisition_missing")
    acquisition, _ = _read_json(root / "acquisition.json", "rho2_acquisition")
    if live_parent:
        require(acquisition == RHO2_ACQUISITION, "rho2_live_acquisition")
    else:
        fixture = acquisition.get("fixture_only") is True
    if fixture:
        require(set(files) == {"rho2.bin", "rho2-dense.bin", "lower-dense.bin"}, "rho2_roster")
    else:
        require(set(files) == set(RHO2_PAYLOAD_RECEIPTS), "rho2_roster")
        for name, expected in RHO2_PAYLOAD_RECEIPTS.items():
            require(files[name] == expected, "rho2_live_receipt")
        _receipt_matches(root / "task640-verdict.json", RHO2_VERDICT,
                         "rho2_verdict_receipt")
    expected_roster = set(files) | {"manifest.json", "acquisition.json", "task640-verdict.json"}
    require({p.name for p in root.iterdir() if p.is_file()} == expected_roster,
            "rho2_file_roster")
    for name, rec in files.items():
        _receipt_matches(root / name, rec, "rho2_file_receipt")
    packed = (root / "rho2.bin").read_bytes()
    dense = (root / "rho2-dense.bin").read_bytes()
    lower = (root / "lower-dense.bin").read_bytes()
    require(len(packed) == PHYSICAL_BYTES and len(dense) == PHYSICAL_WIDTH and
            len(lower) == LOWER_WIDTH and sha(packed) == rho2["packed_sha256"] and
            sha(dense) == rho2["dense_sha256"] and
            sha(lower) == files["lower-dense.bin"]["sha256"], "rho2_receipts")
    value = unpack(packed, PHYSICAL_WIDTH)
    require(dense == value.tobytes() and not np.any(np.frombuffer(lower, dtype=np.uint8)),
            "rho2_dense_or_lower")
    return np.frombuffer(packed, dtype=np.uint8).copy(), manifest


def _state_file_receipt(path: Path) -> dict[str, Any]:
    return {"file": path.name, "bytes": path.stat().st_size,
            "sha256": sha_file(path)}


STATE_STORE_NAMES = ("physical.bin", "physical-p1-coeff.bin", "instructions.jsonl")


def _state_hashers(stage: Path) -> dict[str, Any]:
    hashers = {name: hashlib.sha256() for name in STATE_STORE_NAMES}
    for name in STATE_STORE_NAMES:
        path = stage / name
        with path.open("rb", buffering=0) as stream:
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                hashers[name].update(chunk)
    return hashers


def _state_receipts(stage: Path, hashers: dict[str, Any]) -> dict[str, Any]:
    return {name: {"file": name, "bytes": (stage / name).stat().st_size,
                   "sha256": hashers[name].hexdigest()}
            for name in STATE_STORE_NAMES}


def _checkpoint_pins(connection_root: Path, manifest: dict[str, Any],
                     live_parent: bool) -> dict[str, Any]:
    pins: dict[str, Any] = {
        "connection_schema": CONNECTION_SCHEMA,
        "connection_checkpoint_schema": CHECKPOINT_SCHEMA,
        "connection_manifest_sha256": sha_file(connection_root / "manifest.json"),
        "source_ancestry": manifest["source_ancestry"],
        "p1_identity": manifest["p1_identity"],
        "task712": manifest["task712"],
    }
    if live_parent:
        pins["live_connection_counts"] = LIVE_CONNECTION_COUNTS
    require("path" not in json.dumps(pins, ensure_ascii=True),
            "checkpoint_pathful_pin")
    return pins


def _write_checkpoint(stage: Path, cursor: int, rank: int, dependent: int,
                      skipped: int, generation: int, rolling: str, previous: str,
                      file_receipts: dict[str, Any], pins: dict[str, Any],
                      started: float) -> None:
    checkpoint = {"schema": STATE_CHECKPOINT_SCHEMA, "status": "UNCHECKED_CONNECTION_PREFIX",
                 "cursor": cursor, "rank": rank, "dependent": dependent,
                 "skipped": skipped,
                 "generation": generation, "rolling_head": rolling,
                 "previous_checkpoint_sha256": previous,
                 "files": file_receipts, "pins": pins,
                 "wall_seconds": max(time.monotonic() - started, 0.0),
                 "rss_bytes": process_rss_bytes(),
                 "eof": False}
    atomic_json(stage / "checkpoint.json", checkpoint)


def _read_checkpoint(stage: Path) -> tuple[dict[str, Any], bytes]:
    value, raw = _read_json(stage / "checkpoint.json", "checkpoint")
    require(set(value) == {"schema", "status", "cursor", "rank", "dependent", "skipped",
                           "generation", "rolling_head", "previous_checkpoint_sha256",
                           "files", "pins", "wall_seconds", "rss_bytes", "eof"} and
            value["schema"] == STATE_CHECKPOINT_SCHEMA and
            value["status"] == "UNCHECKED_CONNECTION_PREFIX" and value["eof"] is False,
            "checkpoint_shape")
    require(isinstance(value["wall_seconds"], (int, float)) and
            not isinstance(value["wall_seconds"], bool) and
            value["wall_seconds"] >= 0 and plain_int(value["rss_bytes"]) and
            value["rss_bytes"] > 0, "checkpoint_measurements")
    return value, raw


def _authenticate_state_prefix(stage: Path, connection: dict[str, Any],
                               records: list[dict[str, Any]],
                               pins: dict[str, Any]) -> tuple[int, int, int, int, str, list[dict[str, Any]]]:
    checkpoint, checkpoint_raw = _read_checkpoint(stage)
    cursor = checkpoint["cursor"]
    require(plain_int(cursor) and 0 <= cursor <= len(records) and
            checkpoint["rank"] + checkpoint["dependent"] + checkpoint["skipped"] == cursor,
            "checkpoint_cursor")
    previous = checkpoint["previous_checkpoint_sha256"]
    require(previous == ZERO_HEAD or (stage / "checkpoint.prev").is_file(),
            "checkpoint_previous_receipt")
    require(checkpoint["pins"] == pins, "checkpoint_pins")
    if previous != ZERO_HEAD:
        require(sha((stage / "checkpoint.prev").read_bytes()) == previous,
                "checkpoint_previous_hash")
    for name, expected in checkpoint["files"].items():
        _receipt_matches(stage / name, expected, "checkpoint_file_receipt")
    instructions = stage / "instructions.jsonl"
    rolling = ZERO_HEAD
    pivots: list[dict[str, Any]] = []
    dependent = skipped = 0
    with instructions.open("rb") as stream:
        for offer in range(cursor):
            line = stream.readline()
            require(line, "checkpoint_instruction_eof")
            record = json.loads(line.decode("ascii"))
            require(record["source"] == records[offer] and
                    record["top"] == records[offer]["top"] and
                    record["coefficient"] == records[offer]["coefficient"],
                    "checkpoint_source_record")
            require(record["rolling_sha256"] == sha(bytes.fromhex(rolling) + canonical(
                {k: v for k, v in record.items() if k != "rolling_sha256"})),
                    "checkpoint_rolling")
            rolling = record["rolling_sha256"]
            if record["kind"] == "physical_pivot":
                pivots.append(record)
            elif record["kind"] == "physical_dependent":
                dependent += 1
            else:
                require(record["kind"] == "skipped", "checkpoint_kind")
                skipped += 1
    require(rolling == checkpoint["rolling_head"] and len(pivots) == checkpoint["rank"] and
            dependent == checkpoint["dependent"] and skipped == checkpoint["skipped"] and
            checkpoint_raw, "checkpoint_replay")
    return cursor, checkpoint["rank"], dependent, skipped, rolling, pivots


def _physical_reduce(acc: np.ndarray, coeff_acc: np.ndarray,
                     pivots: list[dict[str, Any]], physical: PositionedStore,
                     companions: PositionedStore, pbuf: np.ndarray,
                     cbuf: np.ndarray) -> list[list[int]]:
    reductions: list[list[int]] = []
    # Every pivot is already reduced against all earlier pivots.  Therefore a
    # single insertion-order sweep removes each pivot's own lead, even when a
    # free coordinate is numerically smaller than that lead.
    for pivot_id, pivot in enumerate(pivots):
        scalar = packed_trit(acc, pivot["lead"])
        if scalar == 0:
            continue
        physical.read_into(pivot["physical_offset"], pbuf)
        companions.read_into(pivot["coefficient_offset"], cbuf)
        COUNTERS["physical_positioned_reads"] += 1
        COUNTERS["p1_positioned_reads"] += 1
        axpy_inplace(acc, pbuf, scalar)
        axpy_inplace(coeff_acc, cbuf, scalar)
        reductions.append([pivot_id, scalar])
        COUNTERS["physical_reductions"] += 1
    require(all(packed_trit(acc, pivot["lead"]) == 0 for pivot in pivots),
            "unreduced_pivot_coordinate")
    return reductions


def _record_state_instruction(record: dict[str, Any], rolling: str) -> tuple[dict[str, Any], str, bytes]:
    body = dict(record)
    body.pop("rolling_sha256", None)
    new_rolling = sha(bytes.fromhex(rolling) + canonical(body))
    body["rolling_sha256"] = new_rolling
    return body, new_rolling, canonical(body)


def build_physical_state(connection_root: Path, stage: Path,
                         stop_after: int | None = None,
                         resume: bool = False,
                         live_parent: bool = False) -> dict[str, Any]:
    started = time.monotonic()
    manifest, records = _validate_connection_parent(connection_root,
                                                     live_parent=live_parent)
    checkpoint_pins = _checkpoint_pins(connection_root, manifest, live_parent)
    require(not stage.exists() if not resume else stage.is_dir(),
            "fresh_stage_or_resume_stage")
    if not resume:
        stage.mkdir(parents=True, exist_ok=False)
        physical = PositionedStore(stage / "physical.bin", PHYSICAL_BYTES, "w+b")
        companions = PositionedStore(stage / "physical-p1-coeff.bin", P1_BYTES, "w+b")
        instructions = (stage / "instructions.jsonl").open("wb", buffering=0)
        cursor = rank = dependent = skipped = 0
        generation = 0
        rolling = ZERO_HEAD
        previous_checkpoint = ZERO_HEAD
        checkpoint_cursor = 0
        pivots: list[dict[str, Any]] = []
        hashers = {name: hashlib.sha256() for name in STATE_STORE_NAMES}
        _write_checkpoint(stage, 0, 0, 0, 0, 0, ZERO_HEAD, ZERO_HEAD,
                          _state_receipts(stage, hashers), checkpoint_pins,
                          started)
        previous_checkpoint = sha_file(stage / "checkpoint.json")
    else:
        cursor, rank, dependent, skipped, rolling, old_records = _authenticate_state_prefix(
            stage, manifest, records, checkpoint_pins)
        generation = _read_checkpoint(stage)[0]["generation"]
        checkpoint_cursor = cursor
        hashers = _state_hashers(stage)
        pivots = []
        for item in old_records:
            if item["kind"] == "physical_pivot":
                pivots.append({"lead": item["lead"],
                               "physical_offset": item["physical_offset"],
                               "coefficient_offset": item["coefficient_offset"],
                               "offer": item["offer"]})
        physical = PositionedStore(stage / "physical.bin", PHYSICAL_BYTES, "r+b")
        companions = PositionedStore(stage / "physical-p1-coeff.bin", P1_BYTES, "r+b")
        instructions = (stage / "instructions.jsonl").open("ab", buffering=0)
        previous_checkpoint = sha_file(stage / "checkpoint.json")
    pbuf = np.empty(PHYSICAL_BYTES, dtype=np.uint8)
    cbuf = np.empty(P1_BYTES, dtype=np.uint8)
    try:
        for offer in range(cursor, len(records)):
            source = records[offer]
            if source["kind"] != "connection":
                # Authenticate the lower-pivot offer but do not offer it to
                # physical S_0: only exact connection records belong here.
                record = {"offer": offer, "kind": "skipped", "source": source,
                          "source_kind": source["kind"], "top": source["top"],
                          "coefficient": source["coefficient"], "reductions": [],
                          "lead": None, "sigma": None, "lower_zero": False,
                          "physical_zero": None, "physical_offset": None,
                          "coefficient_offset": None, "rank": rank,
                          "dependent": dependent}
                record, rolling, line = _record_state_instruction(record, rolling)
                instructions.write(line); hashers["instructions.jsonl"].update(line)
                cursor = offer + 1; skipped += 1
                COUNTERS["connection_offers"] += 1
                if cursor % CHECKPOINT_INTERVAL == 0 or (stop_after is not None and cursor >= stop_after):
                    physical.sync(); companions.sync(); instructions.flush(); os.fsync(instructions.fileno())
                    old_checkpoint = stage / "checkpoint.json"
                    if old_checkpoint.exists():
                        (stage / "checkpoint.prev").write_bytes(old_checkpoint.read_bytes()); fsync_file(stage / "checkpoint.prev")
                    generation = cursor
                    _write_checkpoint(stage, cursor, rank, dependent, skipped,
                                      generation, rolling, previous_checkpoint,
                                      _state_receipts(stage, hashers),
                                      checkpoint_pins, started)
                    previous_checkpoint = sha_file(stage / "checkpoint.json")
                    checkpoint_cursor = cursor
                if stop_after is not None and cursor >= stop_after:
                    raise RuntimeError("UNKNOWN_RESOURCE:bounded_connection_stop")
                continue
            top_raw = (connection_root / "top.bin").open("rb", buffering=0)
            coeff_raw = (connection_root / "coefficient.bin").open("rb", buffering=0)
            try:
                top_raw.seek(source["top"]["offset"]); top = top_raw.read(PHYSICAL_BYTES)
                coeff_raw.seek(source["coefficient"]["offset"]); coeff = coeff_raw.read(P1_BYTES)
            finally:
                top_raw.close(); coeff_raw.close()
            require(len(top) == PHYSICAL_BYTES and len(coeff) == P1_BYTES and
                    sha(top) == source["top"]["sha256"] and sha(coeff) == source["coefficient"]["sha256"],
                    "connection_offer_receipt")
            validate_packed(top, PHYSICAL_WIDTH); validate_packed(coeff, P1_WIDTH)
            acc = np.frombuffer(bytearray(top), dtype=np.uint8)
            coeff_acc = np.frombuffer(bytearray(coeff), dtype=np.uint8)
            reductions = _physical_reduce(acc, coeff_acc, pivots, physical, companions, pbuf, cbuf)
            remainder = first_nonzero(acc, PHYSICAL_WIDTH)
            kind = "physical_dependent" if remainder is None else "physical_pivot"
            sigma = None if remainder is None else (2 if remainder[1] == 2 else 1)
            if sigma == 2:
                scale_two_inplace(acc); scale_two_inplace(coeff_acc)
                remainder = first_nonzero(acc, PHYSICAL_WIDTH)
                require(remainder is not None and remainder[1] == 1, "state_scale_two")
            physical_raw = acc.tobytes()
            coefficient_raw = coeff_acc.tobytes()
            poff = physical.append(physical_raw) if kind == "physical_pivot" else None
            coff = companions.append(coefficient_raw) if kind == "physical_pivot" else None
            if kind == "physical_pivot":
                hashers["physical.bin"].update(physical_raw)
                hashers["physical-p1-coeff.bin"].update(coefficient_raw)
            if kind == "physical_pivot":
                require(remainder is not None and all(remainder[0] != p["lead"] for p in pivots),
                        "state_duplicate_lead")
                pivot = {"id": rank, "offer": offer, "lead": remainder[0],
                         "physical_offset": poff, "coefficient_offset": coff}
                pivots.append(pivot); rank += 1; COUNTERS["physical_pivots"] += 1
            else:
                dependent += 1; COUNTERS["physical_dependents"] += 1
            record = {"offer": offer, "kind": kind, "source": source,
                      "top": source["top"], "coefficient": source["coefficient"],
                      "reductions": reductions, "lead": None if remainder is None else remainder[0],
                      "sigma": sigma, "lower_zero": True,
                      "physical_zero": remainder is None,
                      "physical_offset": poff, "coefficient_offset": coff,
                      "rank": rank, "dependent": dependent}
            record, rolling, line = _record_state_instruction(record, rolling)
            instructions.write(line); hashers["instructions.jsonl"].update(line)
            cursor = offer + 1
            COUNTERS["connection_offers"] += 1
            if cursor % CHECKPOINT_INTERVAL == 0 or (stop_after is not None and cursor >= stop_after):
                # Checkpoint only after a complete offer.  Hashes are carried
                # incrementally, so this path does not reread growing stores.
                physical.sync(); companions.sync(); instructions.flush(); os.fsync(instructions.fileno())
                old_checkpoint = stage / "checkpoint.json"
                if old_checkpoint.exists():
                    (stage / "checkpoint.prev").write_bytes(old_checkpoint.read_bytes()); fsync_file(stage / "checkpoint.prev")
                generation = cursor
                _write_checkpoint(stage, cursor, rank, dependent, skipped, generation, rolling,
                                  previous_checkpoint, _state_receipts(stage, hashers),
                                  checkpoint_pins, started)
                previous_checkpoint = sha_file(stage / "checkpoint.json")
                checkpoint_cursor = cursor
            if stop_after is not None and cursor >= stop_after:
                raise RuntimeError("UNKNOWN_RESOURCE:bounded_connection_stop")
        physical.sync(); companions.sync(); instructions.flush(); os.fsync(instructions.fileno())
        if checkpoint_cursor != cursor:
            old_checkpoint = stage / "checkpoint.json"
            if old_checkpoint.exists():
                (stage / "checkpoint.prev").write_bytes(old_checkpoint.read_bytes()); fsync_file(stage / "checkpoint.prev")
            generation = cursor
            _write_checkpoint(stage, cursor, rank, dependent, skipped, generation, rolling,
                              previous_checkpoint, _state_receipts(stage, hashers),
                              checkpoint_pins, started)
            previous_checkpoint = sha_file(stage / "checkpoint.json")
            checkpoint_cursor = cursor
        state_manifest = {"schema": STATE_SCHEMA, "status": "PHYSICAL_STATE_CANDIDATE",
            "connection_manifest_sha256": sha((connection_root / "manifest.json").read_bytes()),
            "source_ancestry": manifest["source_ancestry"],
            "p1_identity": manifest["p1_identity"],
            "task712": manifest["task712"],
            "cursor": cursor, "offers": len(records),
            "authenticated_offers": len(records),
            "physical_offers": rank + dependent,
            "physical_reduction_bound": (rank + dependent) * (rank + dependent - 1) // 2,
            "rank": rank,
            "dependent": dependent, "skipped": skipped, "generation": generation,
            "physical": {"file": "physical.bin", "rows": rank,
                          "bytes": rank * PHYSICAL_BYTES,
                          "sha256": hashers["physical.bin"].hexdigest(), "eof": True},
            "p1_companions": {"file": "physical-p1-coeff.bin", "rows": rank,
                              "bytes": rank * P1_BYTES,
                              "sha256": hashers["physical-p1-coeff.bin"].hexdigest(), "eof": True},
            "instructions": {"file": "instructions.jsonl", "rows": cursor,
                             "bytes": (stage / "instructions.jsonl").stat().st_size,
                             "sha256": hashers["instructions.jsonl"].hexdigest(),
                             "final_head": rolling, "eof": True},
            "candidate_roster": ["physical.bin", "physical-p1-coeff.bin",
                                  "instructions.jsonl", "manifest.json", "HEAD"],
            **CLAIM_FALSE}
        manifest_raw = atomic_json(stage / "manifest.json", state_manifest)
        # Checkpoints are private recovery material, not part of the
        # completed publication roster.  Remove them before the atomic HEAD
        # visibility switch so completed states have an exact roster.
        for checkpoint_name in ("checkpoint.json", "checkpoint.prev"):
            checkpoint_path = stage / checkpoint_name
            if checkpoint_path.exists():
                checkpoint_path.unlink()
        # Payload files and manifest are durable before the sole visibility
        # switch.  HEAD carries no filesystem path and is atomically replaced.
        head = {"schema": STATE_HEAD_SCHEMA, "generation": generation, "rank": rank,
                "cursor": cursor, "manifest_file": "manifest.json",
                "manifest_sha256": sha(manifest_raw), "rolling_head": rolling,
                "eof": True}
        atomic_json(stage / "HEAD", head)
        return state_manifest
    finally:
        instructions.close(); physical.close(); companions.close()


def _load_state(state_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], PositionedStore, PositionedStore]:
    head, head_raw = _read_json(state_root / "HEAD", "state_head")
    require(set(head) == {"schema", "generation", "rank", "cursor", "manifest_file",
                          "manifest_sha256", "rolling_head", "eof"} and
            head["schema"] == STATE_HEAD_SCHEMA and head["manifest_file"] == "manifest.json" and
            head["eof"] is True, "state_head_shape")
    state, manifest_raw = _read_json(state_root / "manifest.json", "state_manifest")
    require(set(state) == STATE_MANIFEST_KEYS and
            sha(manifest_raw) == head["manifest_sha256"] and state["schema"] == STATE_SCHEMA and
            state["status"] == "PHYSICAL_STATE_CANDIDATE" and state["generation"] == head["generation"] and
            state["rank"] == head["rank"] and state["cursor"] == head["cursor"] and
            state["instructions"]["final_head"] == head["rolling_head"], "state_head_join")
    require(state["candidate_roster"] == ["physical.bin", "physical-p1-coeff.bin",
                                            "instructions.jsonl", "manifest.json", "HEAD"],
            "state_roster")
    require({p.name for p in state_root.iterdir() if p.is_file()} ==
            set(state["candidate_roster"]), "state_file_roster")
    require(isinstance(state.get("source_ancestry"), dict) and state["source_ancestry"] and
            isinstance(state.get("p1_identity"), dict) and state["p1_identity"] and
            isinstance(state.get("task712"), dict) and state["task712"],
            "state_source_identity")
    require(state["authenticated_offers"] == state["offers"] and
            state["physical_offers"] == state["rank"] + state["dependent"] and
            state["physical_reduction_bound"] ==
            state["physical_offers"] * (state["physical_offers"] - 1) // 2,
            "state_offer_partition")
    for name, rec in (("physical.bin", state["physical"]),
                      ("physical-p1-coeff.bin", state["p1_companions"]),
                      ("instructions.jsonl", state["instructions"])):
        path = state_root / name
        require(path.is_file() and path.stat().st_size == rec["bytes"] and
                sha_file(path) == rec["sha256"], "state_file_receipt")
    records: list[dict[str, Any]] = []
    rolling = ZERO_HEAD
    with (state_root / "instructions.jsonl").open("rb") as stream:
        for offer in range(state["cursor"]):
            line = stream.readline(); require(line, "state_instruction_eof")
            record = json.loads(line.decode("ascii")); require(line == canonical(record), "state_instruction_canonical")
            require(record["rolling_sha256"] == sha(bytes.fromhex(rolling) + canonical(
                {k: v for k, v in record.items() if k != "rolling_sha256"})), "state_instruction_rolling")
            rolling = record["rolling_sha256"]; records.append(record)
    require(rolling == state["instructions"]["final_head"], "state_instruction_head")
    return state, records, PositionedStore(state_root / "physical.bin", PHYSICAL_BYTES), PositionedStore(state_root / "physical-p1-coeff.bin", P1_BYTES)


def _target_reduce(target_packed: np.ndarray, state: dict[str, Any], records: list[dict[str, Any]],
                   physical: PositionedStore, companions: PositionedStore) -> dict[str, Any]:
    acc = target_packed.copy(); expression = np.zeros(P1_BYTES, dtype=np.uint8)
    pivots = [record for record in records if record["kind"] == "physical_pivot"]
    pbuf = np.empty(PHYSICAL_BYTES, dtype=np.uint8); cbuf = np.empty(P1_BYTES, dtype=np.uint8)
    reductions: list[dict[str, Any]] = []
    # The target follows the same insertion-order elimination as S_0.  A
    # numerically smaller free coordinate must not terminate this sweep.
    for pivot_id, record in enumerate(pivots):
        scalar = packed_trit(acc, record["lead"])
        if scalar == 0:
            continue
        physical.read_into(record["physical_offset"], pbuf)
        companions.read_into(record["coefficient_offset"], cbuf)
        COUNTERS["physical_positioned_reads"] += 1
        COUNTERS["p1_positioned_reads"] += 1
        axpy_inplace(acc, pbuf, scalar)
        # The physical accumulator performs ``target -= scalar*pivot``;
        # back-substitution records the original target as a positive sum.
        expression[:] = PACKED_AXPY[(3 - scalar) - 1, expression, cbuf]
        reductions.append({"pivot_id": pivot_id, "offer": record["offer"],
                           "lead": record["lead"], "scalar": scalar,
                           "physical_sha256": sha(bytes(pbuf)),
                           "coefficient_sha256": sha(bytes(cbuf))})
        COUNTERS["target_reductions"] += 1
    remainder = first_nonzero(acc, PHYSICAL_WIDTH)
    require(all(packed_trit(acc, pivot["lead"]) == 0 for pivot in pivots),
            "target_unreduced")
    result = {"schema": "d972.r07.physical-state.target-reduction.v1",
              "state_generation": state["generation"], "state_head": state["instructions"]["final_head"],
              "state_rank": state["rank"], "rho2_sha256": sha(target_packed.tobytes()),
              "reductions": reductions, "remainder_sha256": sha(acc.tobytes()),
              "remainder": pack(unpack(acc, PHYSICAL_WIDTH), PHYSICAL_WIDTH).hex(),
              "kind": "ConnectionMember" if remainder is None else "Separator",
              "p1_expression_hex": bytes(expression).hex() if remainder is None else None}
    if remainder is None:
        require(first_nonzero(acc, PHYSICAL_WIDTH) is None, "member_remainder")
        return result
    return result


def _separator(target_packed: np.ndarray, state: dict[str, Any], records: list[dict[str, Any]],
               target: dict[str, Any], physical: PositionedStore) -> dict[str, Any]:
    remainder = unpack(bytes.fromhex(target["remainder"]), PHYSICAL_WIDTH)
    free = first_nonzero(pack(remainder, PHYSICAL_WIDTH), PHYSICAL_WIDTH)
    require(free is not None and free[0] not in {r["lead"] for r in records if r["kind"] == "physical_pivot"},
            "separator_free_coordinate")
    lambda_dense = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
    lambda_dense[free[0]] = free[1]  # inverse in F3 is itself
    pbuf = np.empty(PHYSICAL_BYTES, dtype=np.uint8)
    pivots = [record for record in records if record["kind"] == "physical_pivot"]
    transcript: list[dict[str, Any]] = []
    for reverse_index, record in reversed(list(enumerate(pivots))):
        physical.read_into(record["physical_offset"], pbuf)
        COUNTERS["physical_positioned_reads"] += 1
        row = unpack(bytes(pbuf), PHYSICAL_WIDTH)
        lead = record["lead"]
        total = int(np.dot(row.astype(np.uint32), lambda_dense.astype(np.uint32)) % 3)
        value = (-total) % 3
        lambda_dense[lead] = value
        check = int(np.dot(row.astype(np.uint32), lambda_dense.astype(np.uint32)) % 3)
        require(check == 0, "separator_row_equation")
        transcript.append({"reverse_index": reverse_index, "pivot_id": reverse_index,
                           "offer": record["offer"], "lead": lead,
                           "row_sha256": sha(bytes(pbuf)), "lambda_value": int(value),
                           "equation": 0})
        COUNTERS["reverse_substitution"] += 1
    lambda_packed = pack(lambda_dense, PHYSICAL_WIDTH)
    require(int(np.dot(lambda_dense.astype(np.uint32), unpack(target_packed, PHYSICAL_WIDTH).astype(np.uint32)) % 3) == 1,
            "separator_target_equation")
    return {"schema": "d972.r07.physical-state.Separator.v1", "kind": "Separator",
            "state_generation": state["generation"], "state_head": state["instructions"]["final_head"],
            "state_rank": state["rank"], "rho2_sha256": target["rho2_sha256"],
            "target_reduction_sha256": sha(canonical(target)),
            "remainder_sha256": target["remainder_sha256"], "free_coordinate": free[0],
            "free_value": free[1], "lambda_sha256": sha(lambda_packed),
            "lambda_bytes": len(lambda_packed), "reverse_substitution": transcript,
            "lambda_rho2": 1, "lambda_physical_pivots": 0,
            "ACTUAL_CONNECTION_STATE": False, "verified": False}, lambda_packed


def materialize_terminal(state_root: Path, rho2_root: Path, output_root: Path,
                         final_artifact: Any = None,
                         live_parent: bool = False) -> dict[str, Any]:
    state, records, physical, companions = _load_state(state_root)
    try:
        target_packed, target_manifest = _read_target_parent(rho2_root,
                                                              live_parent=live_parent)
        target = _target_reduce(target_packed, state, records, physical, companions)
        output_root.mkdir(parents=True, exist_ok=False)
        target["target_parent_manifest_sha256"] = sha((rho2_root / "manifest.json").read_bytes())
        if target["kind"] == "ConnectionMember":
            expression = bytes.fromhex(target.pop("p1_expression_hex"))
            write_bytes_durable(output_root / "member-p1-coeff.bin", expression)
            target["p1_expression"] = {"file": "member-p1-coeff.bin", "bytes": len(expression),
                                       "sha256": sha(expression)}
            target["back_substitution"] = [{"pivot_id": x["pivot_id"], "scalar": x["scalar"],
                                             "offer": x["offer"]} for x in target["reductions"]]
            terminal = {"schema": "d972.r07.physical-state.ConnectionMember.v1",
                        "kind": "ConnectionMember", "target_reduction": target,
                        "state_manifest_sha256": sha((state_root / "manifest.json").read_bytes()),
                        **CLAIM_FALSE}
        else:
            separator, lambda_packed = _separator(target_packed, state, records, target, physical)
            write_bytes_durable(output_root / "lambda.bin", lambda_packed)
            write_bytes_durable(output_root / "reverse-substitution.jsonl",
                                b"".join(canonical(x) for x in separator["reverse_substitution"]))
            separator["lambda_file"] = {"file": "lambda.bin", "bytes": len(lambda_packed),
                                         "sha256": sha(lambda_packed)}
            separator["transcript_file"] = {"file": "reverse-substitution.jsonl",
                                             "bytes": (output_root / "reverse-substitution.jsonl").stat().st_size,
                                             "sha256": sha((output_root / "reverse-substitution.jsonl").read_bytes())}
            terminal = {"schema": "d972.r07.physical-state.Separator.v1",
                        "kind": "Separator", "target_reduction": target,
                        "separator": separator,
                        "state_manifest_sha256": sha((state_root / "manifest.json").read_bytes()),
                        **CLAIM_FALSE}
        # The terminal is a durable payload; its receipt is the final ordinary
        # path binding.  A live artifact tuple, when supplied, must be exact.
        if final_artifact is not None and final_artifact != {"fixture_only": True}:
            validate_final_artifact(final_artifact)
        atomic_json(output_root / "terminal.json", terminal)
        terminal["terminal_receipt"] = _state_file_receipt(output_root / "terminal.json")
        atomic_json(output_root / "result.json", terminal)
        return terminal
    finally:
        physical.close(); companions.close()


def _fixture_connection(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=False)
    rows: list[tuple[np.ndarray, np.ndarray, bool]] = []
    # Lower-nonzero offers are authenticated and skipped; connection offers
    # below produce insertion leads [100, 10, 300], deliberately non-monotone.
    for offer in range(6):
        top = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
        lower_zero = offer in (1, 2, 3, 5)
        if offer == 0:
            top[7] = 1
        elif offer == 1:
            top[100] = 1
        elif offer == 2:
            top[10] = 1
        elif offer == 3:
            top[10] = 1; top[100] = 1
        elif offer == 4:
            top[12] = 2
        else:
            top[300] = 2
        coeff = np.zeros(P1_WIDTH, dtype=np.uint8); coeff[offer] = 1
        rows.append((top, coeff, lower_zero))
    top_raw = b"".join(pack(row[0], PHYSICAL_WIDTH) for row in rows)
    coeff_raw = b"".join(pack(row[1], P1_WIDTH) for row in rows)
    lower_rows = []
    for pivot_index in range(2):
        lower = np.zeros(LOWER_WIDTH, dtype=np.uint8)
        lower[pivot_index] = 1
        lower_rows.append(pack(lower, LOWER_WIDTH))
    lower_raw = b"".join(lower_rows)
    (root / "top.bin").write_bytes(top_raw); (root / "coefficient.bin").write_bytes(coeff_raw)
    (root / "lower.bin").write_bytes(lower_raw)
    rolling = ZERO_HEAD; lines: list[bytes] = []; rank = dependent = 0
    zero_lower = pack(np.zeros(LOWER_WIDTH, dtype=np.uint8), LOWER_WIDTH)
    for offer, (top, coeff, lower_zero) in enumerate(rows):
        source_hash = sha(f"fixture-source-{offer}".encode())
        source = {"node": offer, "instruction_sha256": source_hash,
                  "p1_sha256": source_hash, "cache_row_sha256": source_hash,
                  "predecessor": ZERO_HEAD, "ancestry_sha256": source_hash}
        top_rec = {"offset": offer * PHYSICAL_BYTES, "length": PHYSICAL_BYTES,
                   "sha256": sha(pack(top, PHYSICAL_WIDTH))}
        coeff_rec = {"offset": offer * P1_BYTES, "length": P1_BYTES,
                     "sha256": sha(pack(coeff, P1_WIDTH))}
        if lower_zero:
            ell_raw = zero_lower
            lower_rec = {"offset": None, "length": LOWER_BYTES, "sha256": None}
            kind = "connection"
            record_rank, record_dependent = rank, dependent + 1
            dependent += 1
        else:
            ell_raw = lower_rows[rank]
            lower_rec = {"offset": rank * LOWER_BYTES, "length": LOWER_BYTES,
                         "sha256": sha(ell_raw)}
            kind = "pivot"
            record_rank, record_dependent = rank + 1, dependent
            rank += 1
        record = {"offer": offer, "kind": kind, "source": source,
                  "ell_sha256": sha(ell_raw), "g_sha256": sha(pack(top, PHYSICAL_WIDTH)),
                  "top": top_rec, "coefficient": coeff_rec, "lower": lower_rec,
                  "reductions": [], "lead": None if lower_zero else (100 if offer == 0 else 10),
                  "sigma": None if lower_zero else 1, "lower_zero": lower_zero,
                  "rank": record_rank, "dependent": record_dependent}
        body, rolling, line = _record_state_instruction(record, rolling)
        lines.append(line)
    (root / "instructions.jsonl").write_bytes(b"".join(lines))
    manifest = {"schema": CONNECTION_SCHEMA, "status": "CANONICAL_P1_PHYSICAL_CONNECTION_CANDIDATE",
                "offers": len(rows), "rank": 2, "dependent": 4, "reduction_count": 0,
                "coefficient": {"path": "coefficient.bin", "rows": len(rows), "bytes": len(coeff_raw), "sha256": sha(coeff_raw), "eof": True},
                "lower": {"path": "lower.bin", "rows": 2, "bytes": len(lower_raw), "sha256": sha(lower_raw), "eof": True},
                "top": {"path": "top.bin", "rows": len(rows), "bytes": len(top_raw), "sha256": sha(top_raw), "eof": True},
                "instruction": {"path": "instructions.jsonl", "rows": len(rows), "bytes": sum(map(len, lines)), "sha256": sha(b"".join(lines)), "final_lf": True, "eof": True, "final_head": rolling},
                "final_rolling_head": rolling,
                "candidate_roster": ["coefficient.bin", "lower.bin", "top.bin", "instructions.jsonl", "manifest.json"],
                "source_ancestry": {"fixture": "accepted-v6-source-ancestry"},
                "p1_identity": {"fixture": "accepted-v6-p1"},
                "task712": {"fixture": "accepted-task712-v4"}, **SOURCE_CLAIM_FALSE}
    atomic_json(root / "manifest.json", manifest)
    return root


def _fixture_target(root: Path, target: np.ndarray) -> Path:
    root.mkdir(parents=True, exist_ok=False)
    packed = pack(target, PHYSICAL_WIDTH)
    dense = target.tobytes(); lower = bytes(32260)
    (root / "rho2.bin").write_bytes(packed); (root / "rho2-dense.bin").write_bytes(dense); (root / "lower-dense.bin").write_bytes(lower)
    manifest = {"schema": TARGET_PAYLOAD_SCHEMA,
                "marker": "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CANDIDATE",
                "dimensions": {"lower": LOWER_WIDTH, "packed_rho2": PHYSICAL_BYTES,
                               "top": PHYSICAL_WIDTH}, "lower_all_zero": True,
                "rho2": {"packed_sha256": sha(packed), "dense_sha256": sha(dense),
                         "packing_roundtrip": True},
                "files": {"rho2_packed": {"file": "rho2.bin", "bytes": len(packed),
                                             "sha256": sha(packed)},
                          "rho2_dense": {"file": "rho2-dense.bin", "bytes": len(dense),
                                          "sha256": sha(dense)},
                          "lower_dense": {"file": "lower-dense.bin", "bytes": len(lower),
                                           "sha256": sha(lower)}}}
    atomic_json(root / "manifest.json", manifest)
    atomic_json(root / "acquisition.json", {**RHO2_V4_ADAPTER, "fixture_only": True})
    atomic_json(root / "task640-verdict.json", {"schema": TARGET_CHECKER_SCHEMA,
        "marker": "R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V9_CHECKER_PASS",
        "payload_manifest_sha256": sha(canonical(manifest)), "fixture_only": True})
    return root


def _fixture_launch(root: Path, connection: Path, target: Path, state: Path, output: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    launch = {"schema": "d972.r07.physical-state-separator.launch.v1",
              "fixture_only": True, "live_parent": LIVE_V11,
              "resume": False,
              "connection_root": str(connection), "rho2_root": str(target),
              "state_root": str(state), "output_root": str(output),
              "rho2_adapter": RHO2_V4_ADAPTER,
              "final_artifact": {"fixture_only": True},
              "producer": PRODUCER_V6, "checker": CHECKER_V7}
    path = root / "launch.json"; atomic_json(path, launch); return path


def benchmark() -> dict[str, Any]:
    """Measure the callable packed core on a bounded production-shaped fixture."""
    global COUNTERS
    COUNTERS = {key: 0 for key in COUNTERS}
    with tempfile.TemporaryDirectory(prefix="d972-r07-benchmark-") as td:
        base = Path(td); connection = _fixture_connection(base / "connection")
        state_root = base / "state"
        target_dense = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
        target_dense[[5, 100]] = 1
        target_root = _fixture_target(base / "target", target_dense)
        started = time.perf_counter()
        build_physical_state(connection, state_root)
        state, records, physical, companions = _load_state(state_root)
        try:
            target_packed, _ = _read_target_parent(target_root)
            reduction = _target_reduce(target_packed, state, records, physical, companions)
            require(reduction["kind"] == "Separator", "benchmark_separator")
            _separator(target_packed, state, records, reduction, physical)
        finally:
            physical.close(); companions.close()
        elapsed = max(time.perf_counter() - started, 1e-9)
    operations = (COUNTERS["physical_reductions"] +
                  COUNTERS["target_reductions"] +
                  COUNTERS["reverse_substitution"])
    # Isolate the two hot kernels from temporary-directory and fsync costs.
    packed_destination = np.zeros(PHYSICAL_BYTES, dtype=np.uint8)
    packed_source = np.full(PHYSICAL_BYTES, 1, dtype=np.uint8)
    companion_destination = np.zeros(P1_BYTES, dtype=np.uint8)
    companion_source = np.full(P1_BYTES, 1, dtype=np.uint8)
    repetitions = 64
    started_axpy = time.perf_counter()
    for _ in range(repetitions):
        axpy_inplace(packed_destination, packed_source, 1)
        axpy_inplace(companion_destination, companion_source, 1)
    axpy_seconds = max(time.perf_counter() - started_axpy, 1e-9)
    reverse_row = unpack(packed_source, PHYSICAL_WIDTH)
    reverse_functional = unpack(packed_destination, PHYSICAL_WIDTH)
    started_reverse = time.perf_counter()
    reverse_checksum = 0
    for _ in range(repetitions):
        reverse_checksum += int(np.dot(reverse_row.astype(np.uint32),
                                      reverse_functional.astype(np.uint32)) % 3)
    reverse_seconds = max(time.perf_counter() - started_reverse, 1e-9)
    require(reverse_checksum >= 0, "benchmark_reverse_checksum")
    return {"status": "BOUNDED_ONLY", "offers": 6, "physical_rank": 3,
            "physical_reductions": COUNTERS["physical_reductions"],
            "target_reductions": COUNTERS["target_reductions"],
            "reverse_substitution": COUNTERS["reverse_substitution"],
            "operations": operations, "seconds": elapsed,
            "operations_per_second": operations / elapsed,
            "isolated_repetitions": repetitions,
            "packed_physical_p1_axpy_pairs_per_second": repetitions / axpy_seconds,
            "reverse_row_dot_checks_per_second": repetitions / reverse_seconds,
            "physical_reduction_envelope": 6,
            "live_source_offers": LIVE_CONNECTION_COUNTS["offers"],
            "live_source_connections": LIVE_CONNECTION_COUNTS["dependent"],
            "live_physical_reduction_upper_bound":
                LIVE_CONNECTION_COUNTS["dependent"] *
                (LIVE_CONNECTION_COUNTS["dependent"] - 1) // 2,
            "full_connection_envelope": "c(c-1)/2 + target + reverse",
            "verified": False}


def selftest() -> dict[str, Any]:
    global COUNTERS
    COUNTERS = {key: 0 for key in COUNTERS}
    with tempfile.TemporaryDirectory(prefix="d972-r07-state-v1-") as td:
        base = Path(td); connection = _fixture_connection(base / "connection")
        state = base / "state"; target_member = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8)
        target_member[100] = 1; target_member[10] = 1; target_member[300] = 1
        target = _fixture_target(base / "rho2-member", target_member)
        old_shape = base / "rho2-old-v1-list"
        shutil.copytree(target, old_shape)
        old_manifest = json.loads((old_shape / "manifest.json").read_text("ascii"))
        old_manifest["files"] = list(old_manifest["files"].values())
        old_manifest["lower_zero_coordinates"] = LOWER_WIDTH
        old_manifest["rho2_sha256"] = old_manifest["rho2"]["packed_sha256"]
        old_manifest["rho2_dense_sha256"] = old_manifest["rho2"]["dense_sha256"]
        old_manifest["lower_dense_sha256"] = old_manifest["files"][2]["sha256"]
        old_manifest.pop("dimensions"); old_manifest.pop("lower_all_zero"); old_manifest.pop("rho2")
        (old_shape / "manifest.json").write_bytes(canonical(old_manifest))
        try:
            _read_target_parent(old_shape)
        except ValueError:
            old_manifest_shape_rejected = True
        else:
            raise ValueError("old_manifest_shape_accepted")
        build_physical_state(connection, state)
        member = materialize_terminal(state, target, base / "member")
        require(member["kind"] == "ConnectionMember", "member_fixture")
        # Outside-span target gives the separator and exercises reverse
        # insertion order on leads [100,10,300].
        # Coordinate 5 is numerically before existing pivot lead 100.  The
        # target scan must still visit lead 100 before accepting free=5.
        outside = np.zeros(PHYSICAL_WIDTH, dtype=np.uint8); outside[5] = 1; outside[100] = 1
        target2 = _fixture_target(base / "rho2-separator", outside)
        separator = materialize_terminal(state, target2, base / "separator")
        require(separator["kind"] == "Separator" and
                separator["separator"]["free_coordinate"] == 5 and
                [x["lead"] for x in separator["separator"]["reverse_substitution"]] == [300, 10, 100],
                "separator_reverse_insertion")
        # Stop/resume in a distinct absolute directory and compare terminal
        # payloads byte-for-byte.
        stopped = base / "stopped"
        try:
            build_physical_state(connection, stopped, stop_after=3)
        except RuntimeError as exc:
            require(str(exc) == "UNKNOWN_RESOURCE:bounded_connection_stop", "stop_boundary")
        resumed = base / "resumed"; shutil.copytree(stopped, resumed)
        build_physical_state(connection, resumed, resume=True)
        require((state / "manifest.json").read_bytes() == (resumed / "manifest.json").read_bytes() and
                (state / "physical.bin").read_bytes() == (resumed / "physical.bin").read_bytes(),
                "resume_state_bytes")
        return {"schema": "d972.r07.physical-state-separator.v2.selftest",
                "status": "PASS", "connection_offers": 6,
                "authenticated_offers": 6, "physical_offers": 4,
                "physical_reduction_bound": 6, "physical_rank": 3,
                "nonmonotone_insertion_leads": [100, 10, 300],
                "separator_reverse_leads": [300, 10, 100], "member": True,
                "separator": True, "stop_resume_byte_equal": True,
                "production_manifest_dict": True,
                "old_v1_list_manifest_shape_rejected": old_manifest_shape_rejected,
                "file_backed": True, "generic_nullspace_solver": False,
                "final_v11_artifact_tuple": FINAL_V11_ARTIFACT,
                "ACTUAL_CONNECTION_STATE": False,
                "GRADE2_MEMBER/NONMEMBER": "NOT_DECIDED",
                "cross_checked": False, "verified": False,
                "counters": dict(COUNTERS)}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    group = result.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--run-launch", type=Path, metavar="LAUNCH")
    group.add_argument("--benchmark", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.selftest:
            print(json.dumps(selftest(), sort_keys=True, separators=(",", ":"))); return 0
        if args.benchmark:
            report = benchmark()
            print(json.dumps(report, sort_keys=True, separators=(",", ":"))); return 0
        if args.run_launch:
            launch = validate_launch(args.run_launch.resolve())
            # Fixture launches are test-only and must never be presented as a
            # public producer result.
            require(launch["fixture_only"] is False, "public_fixture_path_disabled")
            connection = Path(launch["connection_root"]).resolve()
            state = Path(launch["state_root"]).resolve()
            target = Path(launch["rho2_root"]).resolve()
            output = Path(launch["output_root"]).resolve()
            live_parent = True
            if launch["resume"]:
                require(state.is_dir() and not (state / "HEAD").exists() and
                        (state / "checkpoint.json").is_file(),
                        "explicit_resume_checkpoint_required")
                manifest = build_physical_state(connection, state, resume=True,
                                                live_parent=live_parent)
            else:
                if live_parent:
                    require(not state.exists(), "live_fresh_state_required")
                    manifest = build_physical_state(connection, state,
                                                    live_parent=True)
                elif state.exists():
                    require((state / "HEAD").is_file(),
                            "fixture_resume_must_be_explicit")
                    manifest = _read_json(state / "manifest.json",
                                          "state_manifest")[0]
                else:
                    manifest = build_physical_state(connection, state,
                                                    live_parent=False)
            result = materialize_terminal(state, target, output,
                                          launch["final_artifact"],
                                          live_parent=live_parent)
            print(json.dumps({"state": manifest, "terminal": result,
                              "verified": False}, sort_keys=True, separators=(",", ":"))); return 0
        raise ValueError("mode")
    except RuntimeError as exc:
        print(json.dumps({"status": "UNKNOWN_RESOURCE", "error": str(exc),
                          "verified": False}, separators=(",", ":")), file=sys.stderr); return 2
    except Exception as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc),
                          "verified": False}, separators=(",", ":")), file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
