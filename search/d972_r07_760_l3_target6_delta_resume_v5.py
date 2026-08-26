#!/usr/bin/env python3
"""Append-only delta checkpoint continuation for g760 L3 target6.

The mathematical traversal, terminal rule, and two exact caches are imported
from the pinned v3 producer.  This adapter changes resource recovery only:
after each completed D2 relator it stores the newly appended pivot rows, and a
domain-separated state hash commits the authenticated cumulative append log.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path("search/d972_r07_760_l3_target6_delta_resume_v5.py")
V3_PATH = Path("search/d972_r07_760_l3_target6_relator_resume_v3.py")
V3_DRIVER_PATH = Path(
    "search/d972_r07_760_l3_target6_relator_resume_gha_driver_v3.g")
V3_PREFLIGHT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_relator_resume_"
    "preflight_v3_20260826.json")
V2_CHECKER_PATH = Path(
    "crosscheck/check_d972_r07_760_l3_target6_resume_v2.py")
TASK165_PATH = Path(
    "sol/luna_task_165_r07_target6_relator_checkpoint_v3.md")
REPLY165_PATH = Path(
    "sol/luna_reply_165_r07_target6_relator_checkpoint_v3.md")
TASK166_PATH = Path(
    "sol/luna_task_166_r07_target6_delta_checkpoint_v4.md")
V4_PATH = Path("search/d972_r07_760_l3_target6_delta_resume_v4.py")
V4_DRIVER_PATH = Path(
    "search/d972_r07_760_l3_target6_delta_resume_gha_driver_v4.g")
V4_PREFLIGHT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_delta_resume_"
    "preflight_v4_20260826.json")
REPLY166_PATH = Path(
    "sol/luna_reply_166_r07_target6_delta_checkpoint_v4.md")
TASK167_PATH = Path(
    "sol/luna_task_167_r07_target6_postclosure_recovery_v5.md")

SCHEMA = "d972-r07-760-l3-target6-delta-resume/v5"
DELTA_SCHEMA = "d972-r07-760-l3-target6-delta-checkpoint-stream/v5"
J_CHECKPOINT_SCHEMA = (
    "d972-r07-760-l3-target6-completed-j-checkpoint/v5")
STREAM_FORMAT = "canonical-jsonl-deterministic-gzip/v1"
PIVOT_ENCODING = (
    "[pivot_index,coefficient_one_plane_lowercase_hex,"
    "coefficient_two_plane_lowercase_hex]")
STATE_DOMAIN = "d972-r07-760-l3-target6/v5/cumulative-pivot-state/v1"
ORDER_DOMAIN = "d972-r07-760-l3-target6/v5/cumulative-insertion-order/v1"
PREFLIGHT_STATE = "R07_760_L3_TARGET6_DELTA_RESUME_V5_PREFLIGHT_READY"
DELTA_STATE = "R07_760_L3_TARGET6_DELTA_RESUME_V5_DELTA_READY"
J_CHECKPOINT_STATE = "R07_760_L3_TARGET6_DELTA_RESUME_V5_J_READY"
FINAL_MARKER = "R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_PASS"
DELTA_MARKER = "R07_760_L3_TARGET6_DELTA_RESUME_V5_DELTA_CHECKPOINT"
J_MARKER = "R07_760_L3_TARGET6_DELTA_RESUME_V5_J_CHECKPOINT"

DEFAULT_PREFLIGHT = Path(
    "search/certs/d972_r07_760_l3_target6_delta_resume_"
    "preflight_v5_20260827.json")
DEFAULT_FULL = Path("ci/out/d972_r07_760_l3_target6_delta_resume_v5.json")
DEFAULT_CHECKPOINT_DIR = Path(
    "ci/out/d972_r07_760_l3_target6_delta_resume_v5_checkpoints")

INHERITED_PREFIX = (2, 3, 4, 5, 6, 7, 8)
FRESH_J_ORDER = (9, 10, 11, 12)
RELATOR_ORDER = tuple(range(1, 12))
START_J = 9
MAX_SECONDS = 21600.0
RECOMMENDED_SECONDS = 19200.0
MAX_NEW_RELATORS = 44
STOP_TEXT_LIMIT = 240
MAX_RSS_MIB = 5600
PC_ROSTER_SIZE = 3 ** 10
N_GEN = 10
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
HEX_RE = re.compile(r"(?:0|[1-9a-f][0-9a-f]*)\Z")

V5_PIN_SPECS: dict[str, tuple[Path, int, str]] = {
    "v3_producer": (V3_PATH, 105736,
        "0f1ef3bfd341cc5e596b4d84e4122a56b87488dc894dbf58f0561f288ac8a22f"),
    "v3_driver": (V3_DRIVER_PATH, 15861,
        "5784cc29c5dbc24a89867ebb3a275000ffaa698ba2b3c1a6adc4d4b6efdc7870"),
    "v3_preflight": (V3_PREFLIGHT_PATH, 22409,
        "5928b30f0de8c0aa65e141cdb4101b77c412ab20541ee35c0b74e8680b68c59c"),
    "v2_checker": (V2_CHECKER_PATH, 63772,
        "7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365"),
    "task_165": (TASK165_PATH, 5132,
        "32025aa1cb8587188c57c1f164c1bcbd585a37b5f19f5abec89c458ca8d6084f"),
    "reply_165": (REPLY165_PATH, 9628,
        "1e446578e1566e8c95578b50826e673111fd2b7df9c5df50098b4758b38c55e9"),
    "task_166": (TASK166_PATH, 5816,
        "3d861d83017bd26978553f72dc9654e1bfe62393fa3c94124227a2cc404aa7bd"),
    "v4_producer": (V4_PATH, 88429,
        "08f2237ac6aa438dded775c55627f07ffeff74145765b6e9791a898d594d77ef"),
    "v4_driver": (V4_DRIVER_PATH, 16494,
        "274291371fd5548d5cf5505c5b250cb88a7c74e08ab23f5d0b437a58a079e531"),
    "v4_preflight": (V4_PREFLIGHT_PATH, 34608,
        "0a715bcedec3283894461444fa3d7f542255a436780327bb95f87d1a411e4fbf"),
    "reply_166": (REPLY166_PATH, 9216,
        "6ed022217995157752b523cc50aaae86ed494a81bee00f4c811c9816548f09df"),
    "task_167": (TASK167_PATH, 7170,
        "3b885303f4bf512fc7a9a8e3f124f87a91ca4f3c7728920ee420d781dbe23e8c"),
}

TERMINALS = {
    "R07_760_L3_TARGET6_NONMEMBER",
    "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
    "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
    "R07_760_L3_TARGET6_INPUT_STOP",
}


class InputStop(RuntimeError):
    pass


class SafeResourceStop(RuntimeError):
    def __init__(self, stage: str, reason: str, *, after_j: int,
                 after_relator: int, next_j: int, next_relator: int) -> None:
        super().__init__(reason)
        self.stage = stage
        self.after_j = after_j
        self.after_relator = after_relator
        self.next_j = next_j
        self.next_relator = next_relator


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sanitize_stop_text(value: Any) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ")
    text = "".join(ch if 32 <= ord(ch) <= 126 else "?" for ch in text)
    return text[:STOP_TEXT_LIMIT]


def claims() -> dict[str, bool]:
    return {
        "actual_A18_occurrence": False,
        "normalized_Brunnian_class": False,
        "compatible_cofinal_lift": False,
        "ihara_witness": False,
        "all_bases_obstruction": False,
    }


def verify_self_digest(data: dict[str, Any], label: str) -> None:
    require(type(data) is dict and
            type(data.get("self_digest_sha256")) is str,
            label + " self digest field")
    work = copy.deepcopy(data)
    claimed = work.pop("self_digest_sha256")
    require(claimed == digest_obj(work), label + " self digest")


def v5_pin_inputs() -> dict[str, Any]:
    rows = {}
    for label, (path, size, digest) in V5_PIN_SPECS.items():
        full = ROOT / path
        if not full.is_file() or full.stat().st_size != size or \
                digest_file(full) != digest:
            raise InputStop("v5 pin drift: " + path.as_posix())
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def producer_source_record() -> dict[str, Any]:
    full = ROOT / SELF_PATH
    require(full.is_file(), "v5 producer source missing")
    return {"path": SELF_PATH.as_posix(), "bytes": full.stat().st_size,
            "sha256": digest_file(full)}


def load_v3() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_d972_r07_760_l3_target6_relator_resume_frozen_v3", ROOT / V3_PATH)
    require(spec is not None and spec.loader is not None,
            "v3 producer module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    require(digest_file(ROOT / V3_PATH) == V5_PIN_SPECS["v3_producer"][2],
            "v3 producer post-import pin")
    return module


def load_v4() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_d972_r07_760_l3_target6_delta_resume_frozen_v4", ROOT / V4_PATH)
    require(spec is not None and spec.loader is not None,
            "v4 producer module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    require(digest_file(ROOT / V4_PATH) == V5_PIN_SPECS["v4_producer"][2],
            "v4 producer post-import pin")
    return module


def build_context() -> tuple[Any, Any, Any, dict[str, Any], dict[str, Any],
                             dict[str, Any], dict[str, Any], dict[str, Any]]:
    v5_pins = v5_pin_inputs()
    v3 = load_v3()
    v2, v1, summary, private, prior, v2_pins, v3_meta = v3.build_context()
    require(summary["base"]["sha256"] == BASE_SHA and
            summary["base"]["parent_616_sha256"] == PARENT_SHA and
            summary["Jennings"]["fresh_j_order"] == list(FRESH_J_ORDER) and
            v1.MAX_RSS_MIB == MAX_RSS_MIB,
            "v5 inherited universe")
    v3_bindings = v3.fixed_bindings(v1, private, summary, prior, v3_meta)
    return v3, v2, v1, summary, private, prior, v2_pins, {
        "v5_pin_manifest": v5_pins,
        "v5_pin_manifest_sha256": digest_obj(v5_pins),
        "producer_source": producer_source_record(),
        "v3_fixed_bindings": v3_bindings,
        "v3_fixed_bindings_sha256": digest_obj(v3_bindings),
    }


def fixed_bindings(summary: dict[str, Any], prior: dict[str, Any],
                   meta: dict[str, Any]) -> dict[str, Any]:
    v3_bindings = meta["v3_fixed_bindings"]
    result = {
        "static_binding": summary,
        "static_binding_sha256": summary["binding_sha256"],
        "prior_run_binding": prior,
        "prior_run_binding_sha256": prior["binding_sha256"],
        "v3_fixed_bindings": v3_bindings,
        "v3_fixed_bindings_sha256": meta["v3_fixed_bindings_sha256"],
        "v5_pin_manifest": meta["v5_pin_manifest"],
        "v5_pin_manifest_sha256": meta["v5_pin_manifest_sha256"],
        "producer_source": meta["producer_source"],
        "base_binding": copy.deepcopy(v3_bindings["base_binding"]),
        "target_binding": copy.deepcopy(v3_bindings["target_binding"]),
        "legal_binding": copy.deepcopy(v3_bindings["legal_binding"]),
        "fresh_projection_bindings": copy.deepcopy(
            v3_bindings["fresh_projection_bindings"]),
    }
    result["binding_sha256"] = digest_obj(result)
    return result


def resolve_checkpoint_directory(path: Path) -> Path:
    resolved = (path if path.is_absolute() else ROOT / path).resolve()
    expected = (ROOT / DEFAULT_CHECKPOINT_DIR).resolve()
    require(resolved == expected, "checkpoint directory substitution")
    return resolved


def public_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def delta_filename(j: int, relator: int) -> str:
    require(j in FRESH_J_ORDER and relator in RELATOR_ORDER,
            "delta checkpoint index")
    return ("d972_r07_760_l3_target6_delta_resume_v5_"
            f"j{j:02d}_r{relator:02d}.delta.jsonl.gz")


def j_filename(j: int) -> str:
    require(j in FRESH_J_ORDER, "j checkpoint index")
    return f"d972_r07_760_l3_target6_delta_resume_v5_j{j:02d}.json"


def delta_path(directory: Path, j: int, relator: int) -> Path:
    return resolve_checkpoint_directory(directory) / delta_filename(j, relator)


def j_path(directory: Path, j: int) -> Path:
    return resolve_checkpoint_directory(directory) / j_filename(j)


def atomic_link_temp(temp_path: Path, destination: Path) -> None:
    try:
        os.link(temp_path, destination)
    except FileExistsError:
        require(destination.is_file() and
                destination.stat().st_size == temp_path.stat().st_size and
                digest_file(destination) == digest_file(temp_path),
                "immutable checkpoint mismatch")
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def atomic_immutable_bytes(path: Path, raw: bytes) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".tmp-",
                                dir=str(path.parent))
    temp_path = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        atomic_link_temp(temp_path, path)
    except BaseException:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass
        raise
    require(path.read_bytes() == raw, "atomic immutable byte write")
    return raw


def canonical_hex(value: int) -> str:
    require(type(value) is int and value >= 0, "nonnegative plane")
    return format(value, "x")


def validate_hex(value: Any, label: str) -> int:
    require(type(value) is str and HEX_RE.fullmatch(value) is not None,
            label + " canonical lowercase hex")
    return int(value, 16)


def pivot_row(pivot: int, vector: tuple[int, int]) -> list[Any]:
    return [int(pivot), canonical_hex(vector[0]), canonical_hex(vector[1])]


def parse_pivot_row(v3: Any, sp: Any, row: Any) \
        -> tuple[int, tuple[int, int]]:
    require(type(row) is list and len(row) == 3 and type(row[0]) is int,
            "delta pivot row shape")
    pivot = row[0]
    vector = (validate_hex(row[1], "coefficient-one plane"),
              validate_hex(row[2], "coefficient-two plane"))
    v3.validate_pivot_vector(sp, pivot, vector)
    return pivot, vector


def order_commitment(order: Sequence[int]) -> str:
    return digest_obj({"domain": ORDER_DOMAIN, "pivots": list(order)})


def root_state_commitment(*, j: int, dimension: int, basis_sha: str,
                          target_sha: str, legal_sha: str,
                          prior_j_record: dict[str, Any] | None) -> str:
    return digest_obj({
        "domain": STATE_DOMAIN, "kind": "root", "j": j,
        "dimension": dimension, "Jennings_basis_sha256": basis_sha,
        "target_projected_sha256": target_sha,
        "legal_projected_rows_sha256": legal_sha,
        "prior_j_checkpoint": prior_j_record,
    })


def extend_state_commitment(prior_sha: str, *, j: int, relator: int,
                            rank_before: int, rank_after: int,
                            pivot_raw: Sequence[bytes]) -> str:
    require(type(prior_sha) is str and len(prior_sha) == 64,
            "prior state commitment")
    h = hashlib.sha256()
    h.update(STATE_DOMAIN.encode("ascii") + b"\0delta\0")
    h.update(bytes.fromhex(prior_sha))
    h.update(canonical_bytes({
        "j": j, "relator": relator,
        "rank_before": rank_before, "rank_after": rank_after,
        "delta_count": len(pivot_raw),
    }))
    for raw in pivot_raw:
        h.update(len(raw).to_bytes(8, "big"))
        h.update(raw)
    return h.hexdigest()


def delta_stats(v3: Any, echelon: Any,
                new_order: Sequence[int]) -> dict[str, Any]:
    require(len(set(new_order)) == len(new_order), "delta pivot uniqueness")
    raws = []
    for pivot in new_order:
        require(pivot in echelon.pivots, "delta pivot present")
        vector = echelon.pivots[pivot]
        v3.validate_pivot_vector(echelon.sp, pivot, vector)
        raws.append(canonical_bytes(pivot_row(pivot, vector)) + b"\n")
    h = hashlib.sha256()
    for raw in raws:
        h.update(raw)
    return {"count": len(raws), "bytes": sum(map(len, raws)),
            "sha256": h.hexdigest(), "raws": raws,
            "insertion_order": list(new_order)}


def build_delta_header(
        v3: Any, summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any], j: int, relator: int,
        progression: Sequence[dict[str, Any]],
        closure_receipts: Sequence[dict[str, Any]], echelon: Any,
        before_order: Sequence[int], new_order: Sequence[int],
        prior_j_record: dict[str, Any] | None,
        prior_delta_record: dict[str, Any] | None,
        prior_state_sha: str, target_sha: str, legal_sha: str,
        accelerator_gate: dict[str, Any],
        cache_stats: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    require(j in FRESH_J_ORDER and relator in RELATOR_ORDER,
            "delta header indices")
    after_order = list(echelon.pivots)
    require(after_order[:len(before_order)] == list(before_order) and
            after_order[len(before_order):] == list(new_order),
            "append-only insertion-order suffix")
    stats = delta_stats(v3, echelon, new_order)
    rank_before = len(before_order)
    rank_after = len(after_order)
    require(rank_after - rank_before == stats["count"] and
            len(closure_receipts) == relator,
            "delta rank/receipt count")
    require([row["j"] for row in progression] ==
            list(FRESH_J_ORDER[:FRESH_J_ORDER.index(j)]),
            "delta completed j progression")
    basis = {row["j"]: row for row in
             summary["Jennings"]["basis_manifest"]}[j]
    cumulative_state = extend_state_commitment(
        prior_state_sha, j=j, relator=relator,
        rank_before=rank_before, rank_after=rank_after,
        pivot_raw=stats["raws"])
    header = {
        "schema": DELTA_SCHEMA, "version": 5,
        "mode": "append_only_delta_checkpoint",
        "checkpoint_state": DELTA_STATE, "grade": "CANDIDATE",
        "purpose": "resource_recovery_only",
        "stream_format": STREAM_FORMAT,
        "j": j, "monomial_count": basis["monomial_count"],
        "dimension": basis["dim_Lambda_over_Ij"],
        "Jennings_basis_sha256": basis["basis_sha256"],
        "target_projected_sha256": target_sha,
        "legal_projected_rows_sha256": legal_sha,
        "completed_j_prefix": [row["j"] for row in progression],
        "completed_j_progression": list(progression),
        "completed_relator_prefix": list(range(1, relator + 1)),
        "next_relator": relator + 1 if relator < 11 else None,
        "rank_before": rank_before, "rank_after": rank_after,
        "delta_pivot_count": stats["count"],
        "delta_pivot_encoding": PIVOT_ENCODING,
        "delta_pivot_order": "original_insertion_order",
        "delta_pivot_rows_bytes": stats["bytes"],
        "delta_pivot_rows_sha256": stats["sha256"],
        "delta_insertion_order": stats["insertion_order"],
        "cumulative_pivot_count": rank_after,
        "cumulative_insertion_order_sha256": order_commitment(after_order),
        "state_commitment_domain": STATE_DOMAIN,
        "prior_cumulative_state_commitment_sha256": prior_state_sha,
        "cumulative_state_commitment_sha256": cumulative_state,
        "completed_closure_receipts": list(closure_receipts),
        "prior_j_checkpoint": prior_j_record,
        "prior_delta_checkpoint": prior_delta_record,
        "fixed_bindings": bindings,
        "static_binding_sha256": summary["binding_sha256"],
        "prior_run_binding_sha256": prior["binding_sha256"],
        "accelerator_gate": accelerator_gate,
        "accelerator_cache_stats": cache_stats,
        "algorithm": {
            "mathematical_algorithm": "saturated (x_i-1) BFS, D2 first",
            "v3_exact_caches_unchanged": True,
            "row_insertion_order_changed": False,
            "first_nonmember_rule_changed": False,
            "append_only_delta": True,
            "deterministic_gzip": {
                "mtime": 0, "filename": "", "compresslevel": 6},
        },
        "unfinished_next_relator_inferred": False,
        "mathematical_membership_claimed": False,
        "mathematical_nonmembership_claimed": False,
        "actual_A18_lift_claimed": False,
        "claims": claims(),
    }
    header["self_digest_sha256"] = digest_obj(header)
    return header, stats


def validate_record_shape(record: Any, *, kind: str, j: int,
                          relator: int | None = None) -> None:
    require(type(record) is dict and record.get("kind") == kind and
            record.get("j") == j and
            type(record.get("filename")) is str and
            type(record.get("path")) is str and
            type(record.get("bytes")) is int and record["bytes"] > 0 and
            type(record.get("sha256")) is str and
            len(record["sha256"]) == 64,
            "checkpoint record shape")
    if relator is None:
        require("relator" not in record, "j record has no relator")
    else:
        require(record.get("relator") == relator and
                type(record.get("canonical_uncompressed_bytes")) is int and
                type(record.get("canonical_uncompressed_sha256")) is str and
                type(record.get("delta_pivot_rows_sha256")) is str and
                type(record.get("cumulative_state_commitment_sha256")) is str,
                "delta record fields")


def checkpoint_record(path: Path, *, kind: str, j: int,
                      relator: int | None = None,
                      canonical_size: int | None = None,
                      canonical_sha: str | None = None,
                      delta_sha: str | None = None,
                      state_sha: str | None = None) -> dict[str, Any]:
    record = {
        "kind": kind, "j": int(j), "path": public_path(path),
        "filename": path.name, "bytes": path.stat().st_size,
        "sha256": digest_file(path),
    }
    if relator is not None:
        record["relator"] = int(relator)
        record["canonical_uncompressed_bytes"] = int(canonical_size)
        record["canonical_uncompressed_sha256"] = canonical_sha
        record["delta_pivot_rows_sha256"] = delta_sha
        record["cumulative_state_commitment_sha256"] = state_sha
    return record


def authenticate_record(record: dict[str, Any], directory: Path, *,
                        kind: str, j: int,
                        relator: int | None = None) -> Path:
    validate_record_shape(record, kind=kind, j=j, relator=relator)
    expected = delta_filename(j, relator) if relator is not None \
        else j_filename(j)
    require(record["filename"] == expected, "checkpoint record filename")
    path = resolve_checkpoint_directory(directory) / expected
    require(record["path"] == public_path(path),
            "checkpoint path substitution")
    require(path.is_file() and path.stat().st_size == record["bytes"] and
            digest_file(path) == record["sha256"],
            "checkpoint ancestor SHA/bytes")
    return path


def validate_delta_header(header: dict[str, Any], summary: dict[str, Any],
                          prior: dict[str, Any],
                          bindings: dict[str, Any]) -> None:
    verify_self_digest(header, "delta header")
    require(header.get("schema") == DELTA_SCHEMA and
            header.get("version") == 5 and
            header.get("mode") == "append_only_delta_checkpoint" and
            header.get("checkpoint_state") == DELTA_STATE and
            header.get("grade") == "CANDIDATE" and
            header.get("purpose") == "resource_recovery_only" and
            header.get("stream_format") == STREAM_FORMAT,
            "delta header envelope")
    j = header.get("j")
    prefix = header.get("completed_relator_prefix")
    require(type(j) is int and j in FRESH_J_ORDER and
            type(prefix) is list and prefix and
            prefix == list(range(1, len(prefix) + 1)) and
            len(prefix) in RELATOR_ORDER and
            header.get("next_relator") ==
                (len(prefix) + 1 if len(prefix) < 11 else None),
            "delta exact relator prefix")
    relator = len(prefix)
    basis = {row["j"]: row for row in
             summary["Jennings"]["basis_manifest"]}[j]
    require(header.get("monomial_count") == basis["monomial_count"] and
            header.get("dimension") == basis["dim_Lambda_over_Ij"] and
            header.get("Jennings_basis_sha256") == basis["basis_sha256"],
            "delta Jennings binding")
    projection = {row["j"]: row for row in
                  bindings["fresh_projection_bindings"]}[j]
    require(header.get("target_projected_sha256") ==
                projection["target_projected_sha256"] and
            header.get("legal_projected_rows_sha256") ==
                projection["legal_projected_rows_sha256"],
            "delta target/legal binding")
    expected_j = list(FRESH_J_ORDER[:FRESH_J_ORDER.index(j)])
    progression = header.get("completed_j_progression")
    require(type(progression) is list and
            [row.get("j") for row in progression] == expected_j and
            header.get("completed_j_prefix") == expected_j,
            "delta completed j progression")
    receipts = header.get("completed_closure_receipts")
    rank_before = header.get("rank_before")
    rank_after = header.get("rank_after")
    count = header.get("delta_pivot_count")
    require(type(receipts) is list and len(receipts) == relator and
            type(rank_before) is int and type(rank_after) is int and
            type(count) is int and count >= 0 and
            0 <= rank_before <= rank_after <= header["dimension"] and
            rank_after - rank_before == count and
            header.get("cumulative_pivot_count") == rank_after,
            "delta rank/receipt contract")
    last_receipt = receipts[-1]
    require(type(last_receipt) is dict and
            last_receipt.get("relator_ordinal") == relator and
            last_receipt.get("rank_before") == rank_before and
            last_receipt.get("rank_after") == rank_after and
            last_receipt.get("new_pivots") == count,
            "delta terminal closure receipt binding")
    order = header.get("delta_insertion_order")
    require(type(order) is list and len(order) == count and
            len(set(order)) == count and
            header.get("delta_pivot_encoding") == PIVOT_ENCODING and
            header.get("delta_pivot_order") == "original_insertion_order" and
            type(header.get("delta_pivot_rows_bytes")) is int and
            type(header.get("delta_pivot_rows_sha256")) is str and
            len(header["delta_pivot_rows_sha256"]) == 64 and
            type(header.get("cumulative_insertion_order_sha256")) is str and
            len(header["cumulative_insertion_order_sha256"]) == 64 and
            header.get("state_commitment_domain") == STATE_DOMAIN and
            type(header.get(
                "prior_cumulative_state_commitment_sha256")) is str and
            len(header["prior_cumulative_state_commitment_sha256"]) == 64 and
            type(header.get("cumulative_state_commitment_sha256")) is str and
            len(header["cumulative_state_commitment_sha256"]) == 64,
            "delta commitment contract")
    require(header.get("fixed_bindings") == bindings and
            header.get("static_binding_sha256") == summary["binding_sha256"] and
            header.get("prior_run_binding_sha256") == prior["binding_sha256"],
            "delta fixed bindings")
    if relator == 1:
        require(header.get("prior_delta_checkpoint") is None,
                "delta root prior absent")
    else:
        validate_record_shape(header.get("prior_delta_checkpoint"),
                              kind="delta", j=j, relator=relator - 1)
    algorithm = header.get("algorithm", {})
    require(algorithm.get("mathematical_algorithm") ==
                "saturated (x_i-1) BFS, D2 first" and
            algorithm.get("v3_exact_caches_unchanged") is True and
            algorithm.get("row_insertion_order_changed") is False and
            algorithm.get("first_nonmember_rule_changed") is False and
            algorithm.get("append_only_delta") is True,
            "delta algorithm boundary")
    require(header.get("claims") == claims() and
            all(value is False for value in header["claims"].values()) and
            header.get("unfinished_next_relator_inferred") is False and
            header.get("mathematical_membership_claimed") is False and
            header.get("mathematical_nonmembership_claimed") is False and
            header.get("actual_A18_lift_claimed") is False,
            "delta claim boundary")


def write_delta_checkpoint(path: Path, header: dict[str, Any],
                           stats: dict[str, Any],
                           summary: dict[str, Any], prior: dict[str, Any],
                           bindings: dict[str, Any]) -> dict[str, Any]:
    validate_delta_header(header, summary, prior, bindings)
    require(header["delta_pivot_count"] == stats["count"] and
            header["delta_pivot_rows_bytes"] == stats["bytes"] and
            header["delta_pivot_rows_sha256"] == stats["sha256"] and
            header["delta_insertion_order"] == stats["insertion_order"],
            "delta header/rows agreement")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".tmp-",
                                dir=str(path.parent))
    temp_path = Path(name)
    canonical_hash = hashlib.sha256()
    canonical_size = 0

    def emit(stream: Any, raw: bytes) -> None:
        nonlocal canonical_size
        stream.write(raw)
        canonical_hash.update(raw)
        canonical_size += len(raw)

    try:
        with os.fdopen(fd, "wb") as raw_stream:
            with gzip.GzipFile(filename="", mode="wb", compresslevel=6,
                               fileobj=raw_stream, mtime=0) as stream:
                emit(stream, canonical_bytes(header) + b"\n")
                for raw in stats["raws"]:
                    emit(stream, raw)
            raw_stream.flush()
            os.fsync(raw_stream.fileno())
        atomic_link_temp(temp_path, path)
    except BaseException:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass
        raise
    record = checkpoint_record(
        path, kind="delta", j=header["j"],
        relator=header["completed_relator_prefix"][-1],
        canonical_size=canonical_size,
        canonical_sha=canonical_hash.hexdigest(),
        delta_sha=stats["sha256"],
        state_sha=header["cumulative_state_commitment_sha256"])
    return record


def read_delta_checkpoint(
        path: Path, v3: Any, v1: Any, summary: dict[str, Any],
        prior: dict[str, Any], bindings: dict[str, Any]) \
        -> tuple[dict[str, Any], list[tuple[int, tuple[int, int]]],
                 dict[str, Any]]:
    compressed_size = path.stat().st_size
    compressed_sha = digest_file(path)
    canonical_hash = hashlib.sha256()
    canonical_size = 0
    delta_hash = hashlib.sha256()
    delta_size = 0
    parsed_rows = []
    with gzip.open(path, "rb") as stream:
        first = stream.readline()
        require(first.endswith(b"\n"), "delta header newline")
        canonical_hash.update(first)
        canonical_size += len(first)
        header = json.loads(first[:-1].decode("ascii"))
        require(first == canonical_bytes(header) + b"\n",
                "delta header canonical")
        validate_delta_header(header, summary, prior, bindings)
        sp = v1.F3BitSpace(header["dimension"])
        for expected in header["delta_insertion_order"]:
            raw = stream.readline()
            require(raw.endswith(b"\n"), "delta row newline")
            row = json.loads(raw[:-1].decode("ascii"))
            require(raw == canonical_bytes(row) + b"\n",
                    "delta row canonical")
            pivot, vector = parse_pivot_row(v3, sp, row)
            require(pivot == expected, "delta row insertion order")
            parsed_rows.append((pivot, vector))
            canonical_hash.update(raw)
            canonical_size += len(raw)
            delta_hash.update(raw)
            delta_size += len(raw)
        require(stream.read(1) == b"", "delta trailing row")
    require(len(parsed_rows) == header["delta_pivot_count"] and
            delta_size == header["delta_pivot_rows_bytes"] and
            delta_hash.hexdigest() == header["delta_pivot_rows_sha256"],
            "delta row digest/count")
    record = checkpoint_record(
        path, kind="delta", j=header["j"],
        relator=header["completed_relator_prefix"][-1],
        canonical_size=canonical_size,
        canonical_sha=canonical_hash.hexdigest(),
        delta_sha=delta_hash.hexdigest(),
        state_sha=header["cumulative_state_commitment_sha256"])
    require(record["bytes"] == compressed_size and
            record["sha256"] == compressed_sha,
            "delta compressed digest stable")
    return header, parsed_rows, record


def replay_delta_chain(
        current_path: Path, directory: Path, v3: Any, v2: Any, v1: Any,
        summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any]) \
        -> tuple[dict[str, Any], Any, list[dict[str, Any]],
                 list[dict[str, Any]]]:
    directory = resolve_checkpoint_directory(directory)
    path = current_path.resolve()
    require(path.parent == directory and path.is_file(),
            "delta resume directory")
    backwards = []
    seen = set()
    child_record = None
    while True:
        require(path not in seen, "delta checkpoint cycle")
        seen.add(path)
        if child_record is not None:
            require(path.stat().st_size == child_record["bytes"] and
                    digest_file(path) == child_record["sha256"],
                    "delta ancestor SHA/bytes")
        header, rows, record = read_delta_checkpoint(
            path, v3, v1, summary, prior, bindings)
        j = header["j"]
        relator = header["completed_relator_prefix"][-1]
        require(path.name == delta_filename(j, relator),
                "delta checkpoint filename")
        backwards.append((path, header, rows, record))
        previous = header["prior_delta_checkpoint"]
        if relator == 1:
            require(previous is None, "delta chain root")
            break
        previous_path = authenticate_record(
            previous, directory, kind="delta", j=j,
            relator=relator - 1)
        child_record = previous
        path = previous_path
    chain = list(reversed(backwards))
    terminal_relator = chain[-1][1]["completed_relator_prefix"][-1]
    require([row[1]["completed_relator_prefix"][-1] for row in chain] ==
            list(range(1, terminal_relator + 1)),
            "delta chain exact prefix")
    first = chain[0][1]
    j = first["j"]
    prior_j_record = first["prior_j_checkpoint"]
    prior_j_records = []
    progression = []
    if j == START_J:
        require(prior_j_record is None and
                first["completed_j_progression"] == [],
                "j9 delta root")
    else:
        prior_j_path = authenticate_record(
            prior_j_record, directory, kind="j", j=j - 1)
        prior_j_data, prior_j_records = load_j_checkpoint_chain(
            prior_j_path, directory, v3, v2, v1, summary, prior, bindings)
        progression = copy.deepcopy(prior_j_data["j_progression"])
        require(progression == first["completed_j_progression"],
                "delta prior j progression")
        validate_completed_delta_chains(
            progression, directory, v3, v2, v1, summary, prior, bindings)

    sp = v1.F3BitSpace(first["dimension"])
    echelon = v1.F3BitEchelon(sp)
    order = []
    expected_state = root_state_commitment(
        j=j, dimension=first["dimension"],
        basis_sha=first["Jennings_basis_sha256"],
        target_sha=first["target_projected_sha256"],
        legal_sha=first["legal_projected_rows_sha256"],
        prior_j_record=prior_j_record)
    previous_record = None
    previous_receipts = []
    records = []
    for ordinal, (_, header, rows, record) in enumerate(chain, 1):
        require(header["j"] == j and
                header["prior_j_checkpoint"] == prior_j_record and
                header["completed_j_progression"] == progression and
                header["rank_before"] == echelon.rank() and
                header["prior_cumulative_state_commitment_sha256"] ==
                    expected_state and
                header["prior_delta_checkpoint"] == previous_record and
                header["completed_closure_receipts"][:-1] ==
                    previous_receipts,
                "delta cumulative chain")
        require(len(rows) == header["delta_pivot_count"],
                "delta replay row count")
        raw_rows = []
        for pivot, vector in rows:
            require(pivot not in echelon.pivots,
                    "delta rewrites old pivot")
            before = list(echelon.pivots)
            require(echelon.add(vector), "delta row dependent")
            require(list(echelon.pivots) == before + [pivot] and
                    echelon.pivots[pivot] == vector,
                    "delta exact inserted pivot")
            order.append(pivot)
            raw_rows.append(canonical_bytes(pivot_row(pivot, vector)) + b"\n")
        require(echelon.rank() == header["rank_after"] and
                header["cumulative_pivot_count"] == len(order) and
                header["cumulative_insertion_order_sha256"] ==
                    order_commitment(order),
                "delta cumulative order/rank")
        computed_state = extend_state_commitment(
            expected_state, j=j, relator=ordinal,
            rank_before=header["rank_before"],
            rank_after=header["rank_after"], pivot_raw=raw_rows)
        require(computed_state ==
                header["cumulative_state_commitment_sha256"] and
                record["cumulative_state_commitment_sha256"] ==
                    computed_state,
                "delta cumulative state reconstruction")
        expected_state = computed_state
        previous_record = record
        previous_receipts = header["completed_closure_receipts"]
        records.append(record)
    require(list(echelon.pivots) == order and
            echelon.rank() == chain[-1][1]["rank_after"],
            "delta final exact dictionary/rank")
    return chain[-1][1], echelon, records, prior_j_records


def validate_public_j_row(v3: Any, v2: Any, row: dict[str, Any],
                          summary: dict[str, Any]) -> None:
    v3.validate_public_j_row(v2, row, summary)
    append = row.get("v5_append_only_delta")
    require(type(append) is dict and
            append.get("old_pivots_unchanged") is True and
            append.get("insertion_order_prefix_preserved") is True and
            append.get("delta_count_equals_rank_increment") is True and
            type(append.get("terminal_state_commitment_sha256")) is str and
            len(append["terminal_state_commitment_sha256"]) == 64,
            "completed j append-only boundary")


def build_j_checkpoint(
        v3: Any, v2: Any, summary: dict[str, Any], bindings: dict[str, Any],
        progression: Sequence[dict[str, Any]],
        prior_j_record: dict[str, Any] | None,
        terminal_delta_record: dict[str, Any]) -> dict[str, Any]:
    require(progression, "j checkpoint progression")
    completed = [row["j"] for row in progression]
    require(completed == list(FRESH_J_ORDER[:len(completed)]),
            "j checkpoint exact prefix")
    for row in progression:
        validate_public_j_row(v3, v2, row, summary)
    j = completed[-1]
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    require(len(nonmembers) <= 1 and
            (not nonmembers or nonmembers == [j]),
            "j checkpoint first nonmember")
    next_j = None if nonmembers or j == FRESH_J_ORDER[-1] else j + 1
    if j == START_J:
        require(prior_j_record is None, "j9 prior absent")
    else:
        validate_record_shape(prior_j_record, kind="j", j=j - 1)
    validate_record_shape(terminal_delta_record, kind="delta", j=j,
                          relator=11)
    data = {
        "schema": J_CHECKPOINT_SCHEMA, "version": 5,
        "mode": "completed_j_checkpoint", "checkpoint_state": J_CHECKPOINT_STATE,
        "grade": "CANDIDATE", "completed_j_prefix": completed,
        "next_j": next_j,
        "first_nonmember_j": nonmembers[0] if nonmembers else None,
        "j_progression": list(progression),
        "current_j_row_sha256": digest_obj(progression[-1]),
        "prior_j_checkpoint": prior_j_record,
        "terminal_delta_checkpoint": terminal_delta_record,
        "fixed_bindings": bindings,
        "delta_chain_reconstructs_full_relator_state": True,
        "delta_checkpoint_is_resource_recovery_only": True,
        "unfinished_j_inferred": False,
        "mathematical_membership_claimed": False,
        "mathematical_nonmembership_claimed": False,
        "actual_A18_lift_claimed": False,
        "claims": claims(),
    }
    data["self_digest_sha256"] = digest_obj(data)
    return data


def validate_j_checkpoint(v3: Any, v2: Any, data: dict[str, Any],
                          summary: dict[str, Any],
                          bindings: dict[str, Any]) -> None:
    verify_self_digest(data, "completed j checkpoint")
    require(data.get("schema") == J_CHECKPOINT_SCHEMA and
            data.get("version") == 5 and
            data.get("mode") == "completed_j_checkpoint" and
            data.get("checkpoint_state") == J_CHECKPOINT_STATE and
            data.get("grade") == "CANDIDATE" and
            data.get("fixed_bindings") == bindings,
            "completed j envelope")
    progression = data.get("j_progression")
    require(type(progression) is list and progression,
            "completed j progression")
    completed = [row.get("j") for row in progression]
    require(completed == data.get("completed_j_prefix") and
            completed == list(FRESH_J_ORDER[:len(completed)]),
            "completed j exact prefix")
    for row in progression:
        validate_public_j_row(v3, v2, row, summary)
    j = completed[-1]
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    expected_next = None if nonmembers or j == 12 else j + 1
    require(len(nonmembers) <= 1 and
            (not nonmembers or nonmembers == [j]) and
            data.get("first_nonmember_j") ==
                (nonmembers[0] if nonmembers else None) and
            data.get("next_j") == expected_next and
            data.get("current_j_row_sha256") == digest_obj(progression[-1]),
            "completed j terminal/current")
    if j == START_J:
        require(data.get("prior_j_checkpoint") is None, "j9 prior absent")
    else:
        validate_record_shape(data.get("prior_j_checkpoint"),
                              kind="j", j=j - 1)
    validate_record_shape(data.get("terminal_delta_checkpoint"),
                          kind="delta", j=j, relator=11)
    require(data.get("delta_chain_reconstructs_full_relator_state") is True and
            data.get("delta_checkpoint_is_resource_recovery_only") is True and
            data.get("unfinished_j_inferred") is False and
            data.get("mathematical_membership_claimed") is False and
            data.get("mathematical_nonmembership_claimed") is False and
            data.get("actual_A18_lift_claimed") is False and
            data.get("claims") == claims(),
            "completed j claim boundary")


def write_j_checkpoint(path: Path, data: dict[str, Any], v3: Any, v2: Any,
                       summary: dict[str, Any],
                       bindings: dict[str, Any]) -> dict[str, Any]:
    validate_j_checkpoint(v3, v2, data, summary, bindings)
    raw = canonical_bytes(data) + b"\n"
    atomic_immutable_bytes(path, raw)
    return checkpoint_record(path, kind="j",
                             j=data["completed_j_prefix"][-1])


def read_canonical_json(path: Path, label: str) \
        -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    data = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(data) + b"\n", label + " canonical")
    return data, raw


def load_j_checkpoint_chain(
        path: Path, directory: Path, v3: Any, v2: Any, v1: Any,
        summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any]) \
        -> tuple[dict[str, Any], list[dict[str, Any]]]:
    del v1, prior
    directory = resolve_checkpoint_directory(directory)
    path = path.resolve()
    require(path.parent == directory and path.is_file(),
            "j checkpoint directory")
    data, _ = read_canonical_json(path, "completed j checkpoint")
    validate_j_checkpoint(v3, v2, data, summary, bindings)
    j = data["completed_j_prefix"][-1]
    require(path.name == j_filename(j), "j checkpoint filename")
    record = checkpoint_record(path, kind="j", j=j)
    terminal = data["terminal_delta_checkpoint"]
    authenticate_record(terminal, directory, kind="delta", j=j, relator=11)
    previous = data["prior_j_checkpoint"]
    if j == START_J:
        require(previous is None, "j9 chain root")
        return data, [record]
    previous_path = authenticate_record(
        previous, directory, kind="j", j=j - 1)
    previous_data, records = load_j_checkpoint_chain(
        previous_path, directory, v3, v2, None, summary, None, bindings)
    require(previous_data["j_progression"] == data["j_progression"][:-1],
            "j checkpoint cumulative chain")
    return data, records + [record]


def validate_terminal_header(header: dict[str, Any], row: dict[str, Any],
                             preceding: Sequence[dict[str, Any]]) -> None:
    checks = {
        "j": header["j"] == row["j"],
        "progression": header["completed_j_progression"] == list(preceding),
        "closure_receipts": header["completed_closure_receipts"] ==
            row["per_relator_closure_receipts"],
        "rank": header["rank_after"] == row["rank_D2bar_alone"],
        "monomials": header["monomial_count"] == row["monomial_count"],
        "dimension": header["dimension"] == row["dim_Lambda_over_Ij"],
        "basis": header["Jennings_basis_sha256"] == row["basis_sha256"],
        "target": header["target_projected_sha256"] ==
            row["target_projected_sha256"],
        "legal": header["legal_projected_rows_sha256"] ==
            row["legal_projected_rows_sha256"],
        "state": row["v5_append_only_delta"][
            "terminal_state_commitment_sha256"] ==
            header["cumulative_state_commitment_sha256"],
    }
    require(all(checks.values()), "terminal delta/public j binding: " +
            ",".join(key for key, value in checks.items() if not value))


def validate_completed_delta_chains(
        progression: Sequence[dict[str, Any]], directory: Path,
        v3: Any, v2: Any, v1: Any, summary: dict[str, Any],
        prior: dict[str, Any], bindings: dict[str, Any]) -> None:
    for ordinal, row in enumerate(progression):
        path = delta_path(directory, int(row["j"]), 11)
        header, echelon, _, _ = replay_delta_chain(
            path, directory, v3, v2, v1, summary, prior, bindings)
        require(echelon.rank() == header["rank_after"] and
                header["completed_relator_prefix"] == list(RELATOR_ORDER),
                "completed delta terminal state")
        validate_terminal_header(header, row, progression[:ordinal])


def run_relator_closure_append_only(
        v3: Any, v1: Any, private: dict[str, Any],
        workspace: dict[str, Any], echelon: Any, ordinal: int,
        left_cache: Any) -> tuple[dict[str, Any], list[int], list[int]]:
    before_order = list(echelon.pivots)
    before_rows = dict(echelon.pivots)
    receipt = v3.run_relator_closure(
        v1, private, workspace, echelon, ordinal, left_cache)
    after_order = list(echelon.pivots)
    require(all(echelon.pivots.get(pivot) == vector
                for pivot, vector in before_rows.items()),
            "append-only old pivot rows unchanged")
    require(after_order[:len(before_order)] == before_order,
            "append-only insertion order exact prefix")
    suffix = after_order[len(before_order):]
    require(receipt["new_pivots"] == len(suffix) and
            receipt["rank_before"] == len(before_order) and
            receipt["rank_after"] == len(after_order) and
            len(after_order) - len(before_order) == len(suffix),
            "append-only receipt/rank suffix")
    return receipt, before_order, suffix


def actual_checkpoint_names(directory: Path) -> set[str]:
    directory = resolve_checkpoint_directory(directory)
    if not directory.exists():
        return set()
    return {path.name for path in directory.iterdir()
            if path.is_file() and
            (path.name.endswith(".delta.jsonl.gz") or
             (path.name.startswith(
                 "d972_r07_760_l3_target6_delta_resume_v5_j") and
              path.name.endswith(".json")))}


def expected_names_for_resume(
        progression: Sequence[dict[str, Any]], active_j: int | None = None,
        completed_relator: int = 0) -> set[str]:
    names = set()
    for row in progression:
        j = int(row["j"])
        names.update(delta_filename(j, relator)
                     for relator in RELATOR_ORDER)
        names.add(j_filename(j))
    if active_j is not None:
        require(active_j == FRESH_J_ORDER[len(progression)] and
                0 <= completed_relator <= 11,
                "active resume index")
        names.update(delta_filename(active_j, relator)
                     for relator in range(1, completed_relator + 1))
    return names


def manifest_records(directory: Path) -> list[dict[str, Any]]:
    directory = resolve_checkpoint_directory(directory)
    rows = []
    for j in FRESH_J_ORDER:
        for relator in RELATOR_ORDER:
            path = directory / delta_filename(j, relator)
            if path.is_file():
                with gzip.open(path, "rb") as stream:
                    first = stream.readline()
                header = json.loads(first[:-1].decode("ascii"))
                rows.append({
                    "kind": "delta", "j": j, "relator": relator,
                    "path": public_path(path), "filename": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": digest_file(path),
                    "canonical_self_digest_sha256":
                        header["self_digest_sha256"],
                    "rank_before": header["rank_before"],
                    "rank_after": header["rank_after"],
                    "delta_pivot_count": header["delta_pivot_count"],
                    "delta_pivot_rows_sha256":
                        header["delta_pivot_rows_sha256"],
                    "cumulative_state_commitment_sha256":
                        header["cumulative_state_commitment_sha256"],
                })
        path = directory / j_filename(j)
        if path.is_file():
            data, _ = read_canonical_json(path, "manifest j checkpoint")
            rows.append({
                "kind": "j", "j": j, "path": public_path(path),
                "filename": path.name, "bytes": path.stat().st_size,
                "sha256": digest_file(path),
                "canonical_self_digest_sha256": data["self_digest_sha256"],
            })
    return rows


def base_output(mode: str, summary: dict[str, Any], prior: dict[str, Any],
                v2_pins: dict[str, Any], bindings: dict[str, Any]) \
        -> dict[str, Any]:
    return {
        "schema": SCHEMA, "mode": mode, "grade": "CANDIDATE",
        "fixed_bindings": bindings, "static_binding": summary,
        "prior_run_binding": prior, "v2_pins": v2_pins,
        "resume_contract": {
            "inherited_candidate_prefix": list(INHERITED_PREFIX),
            "inherited_prefix_grade":
                "producer_control_flow_candidate_only",
            "fresh_j_order": list(FRESH_J_ORDER),
            "relator_order": list(RELATOR_ORDER),
            "no_checkpoint_start": "j9_relator1",
            "checkpoint_after_every_completed_relator": True,
            "append_only_delta_rows_only": True,
            "authenticated_full_chain_replay_required": True,
            "cross_run_artifact_ingress_implemented": False,
            "resource_stop_claim_free": True,
            "member_is_actual_A18_lift": False,
        },
        "sound_implication": {
            "nonmembership_direction_only": True,
            "membership_is_lift": False,
            "scope": "one explicit g760 prefix, first hexagon coordinate",
        },
        "direct_checker_handoff": {
            "path": V2_CHECKER_PATH.as_posix(),
            "sha256": V5_PIN_SPECS["v2_checker"][2],
            "imports_v1_producer": False,
            "imports_v2_producer": False,
            "required_for_fresh_NONMEMBER_promotion": True,
            "v5_delta_format_is_not_a_checker_result": True,
        },
        "claims": claims(),
    }


def common_result(progression: Sequence[dict[str, Any]],
                  records: Sequence[dict[str, Any]],
                  resume_record: dict[str, Any] | None) -> dict[str, Any]:
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    return {
        "inherited_candidate_prefix": list(INHERITED_PREFIX),
        "inherited_prefix_grade": "producer_control_flow_candidate_only",
        "fresh_j_order": list(FRESH_J_ORDER),
        "fresh_j_order_tested": [row["j"] for row in progression],
        "first_nonmember_j": nonmembers[0] if nonmembers else None,
        "j_progression": list(progression),
        "checkpoint_manifest": list(records),
        "checkpoint_manifest_count": len(records),
        "resume_from_checkpoint": resume_record,
        "unfinished_relator_inferred": False,
        "delta_chain_reconstructs_full_relator_state": True,
        "delta_checkpoint_is_resource_recovery_only": True,
        "cross_run_artifact_ingress_ready": False,
        "mathematical_membership_claimed": False,
        "mathematical_nonmembership_claimed": False,
        "actual_A18_lift_claimed": False,
        "registered_108_family_used": False,
        "literal_A18_computed": False,
        "normalized_Brunnian_class_computed": False,
    }


def build_full(seconds: float, checkpoint_dir: Path,
               resume_checkpoint: Path | None, *, accelerators: bool,
               max_new_relators: int | None = None) \
        -> dict[str, Any]:
    require(0 < seconds <= MAX_SECONDS, "seconds range")
    require(max_new_relators is None or
            (type(max_new_relators) is int and
             1 <= max_new_relators <= MAX_NEW_RELATORS),
            "max new relators range")
    directory = resolve_checkpoint_directory(checkpoint_dir)
    directory.mkdir(parents=True, exist_ok=True)
    v3 = v2 = v1 = None
    summary = prior = v2_pins = bindings = None
    progression = []
    resume_record = None
    active_j = START_J
    next_relator = 1
    resumed_echelon = None
    resumed_receipts = []
    resumed_header = None
    prior_j_record = None
    prior_delta_record = None
    prior_state_sha = None
    new_relators_completed = 0
    safe_stop_pending = False
    stage = "input_authentication"
    try:
        v3, v2, v1, summary, private, prior, v2_pins, meta = build_context()
        bindings = fixed_bindings(summary, prior, meta)
        if resume_checkpoint is None:
            require(not actual_checkpoint_names(directory),
                    "stale checkpoint files without resume")
        else:
            resume_path = (resume_checkpoint if resume_checkpoint.is_absolute()
                           else ROOT / resume_checkpoint).resolve()
            require(resume_path.parent == directory and resume_path.is_file(),
                    "resume checkpoint path")
            if resume_path.name.endswith(".delta.jsonl.gz"):
                header, resumed_echelon, delta_records, _ = replay_delta_chain(
                    resume_path, directory, v3, v2, v1,
                    summary, prior, bindings)
                active_j = header["j"]
                resumed_header = header
                next_relator = header["next_relator"] or 12
                resumed_receipts = copy.deepcopy(
                    header["completed_closure_receipts"])
                progression = copy.deepcopy(
                    header["completed_j_progression"])
                prior_j_record = copy.deepcopy(header["prior_j_checkpoint"])
                prior_delta_record = delta_records[-1]
                prior_state_sha = header[
                    "cumulative_state_commitment_sha256"]
                resume_record = delta_records[-1]
                expected = expected_names_for_resume(
                    progression, active_j,
                    header["completed_relator_prefix"][-1])
            else:
                checkpoint, j_records = load_j_checkpoint_chain(
                    resume_path, directory, v3, v2, v1,
                    summary, prior, bindings)
                progression = copy.deepcopy(checkpoint["j_progression"])
                require(checkpoint["next_j"] in FRESH_J_ORDER,
                        "terminal j checkpoint cannot resume")
                validate_completed_delta_chains(
                    progression, directory, v3, v2, v1,
                    summary, prior, bindings)
                active_j = checkpoint["next_j"]
                prior_j_record = j_records[-1]
                resume_record = j_records[-1]
                expected = expected_names_for_resume(progression)
            require(actual_checkpoint_names(directory) == expected,
                    "stale, missing, or unselected checkpoint roster")
        require(active_j == FRESH_J_ORDER[len(progression)],
                "resume exact next j")

        monitor = v1.Monitor(seconds)
        left_cache = v3.LeftMultiplyCache(
            private["e4"].pc, enabled=accelerators)
        for j in FRESH_J_ORDER[len(progression):]:
            stage = f"j={j}:start"
            monitor.check(stage, force=True)
            workspace = v3.j_workspace(
                v1, private, j, accelerators=accelerators,
                left_cache=left_cache)
            if resumed_echelon is not None:
                require(resumed_echelon.sp.n == workspace["sp"].n,
                        "resumed echelon dimension")
                echelon = resumed_echelon
                receipts = resumed_receipts
                first_relator = next_relator
            else:
                echelon = v1.F3BitEchelon(workspace["sp"])
                receipts = []
                first_relator = 1
                prior_delta_record = None
                prior_state_sha = root_state_commitment(
                    j=j, dimension=workspace["dimension"],
                    basis_sha=workspace["basis_sha256"],
                    target_sha=workspace["target_projected_sha256"],
                    legal_sha=workspace["legal_projected_rows_sha256"],
                    prior_j_record=prior_j_record)
            require(first_relator == len(receipts) + 1 and
                    1 <= first_relator <= 12 and
                    type(prior_state_sha) is str,
                    "exact next delta relator")
            terminal_header = resumed_header if first_relator == 12 else None
            for ordinal in range(first_relator, 12):
                stage = f"j={j}:D2-relator-{ordinal}"
                monitor.check(stage, force=True)
                receipt, before_order, suffix = \
                    run_relator_closure_append_only(
                        v3, v1, private, workspace, echelon,
                        ordinal, left_cache)
                receipts.append(receipt)
                cache_stats = {
                    "left_multiply": {"hits": left_cache.hits,
                                      "misses": left_cache.misses},
                    "Jennings_bitplane": {
                        "hits": workspace["projector"].hits,
                        "misses": workspace["projector"].misses},
                }
                header, stats = build_delta_header(
                    v3, summary, prior, bindings, j, ordinal,
                    progression, receipts, echelon, before_order, suffix,
                    prior_j_record, prior_delta_record, prior_state_sha,
                    workspace["target_projected_sha256"],
                    workspace["legal_projected_rows_sha256"],
                    workspace["gate"], cache_stats)
                path = delta_path(directory, j, ordinal)
                record = write_delta_checkpoint(
                    path, header, stats, summary, prior, bindings)
                authenticate_record(record, directory, kind="delta", j=j,
                                    relator=ordinal)
                prior_delta_record = record
                prior_state_sha = header[
                    "cumulative_state_commitment_sha256"]
                terminal_header = header
                print(
                    DELTA_MARKER + f" j={j} relator={ordinal} "
                    f"rank_before={header['rank_before']} "
                    f"rank_after={header['rank_after']} "
                    f"delta={header['delta_pivot_count']} "
                    f"sha256={record['sha256']} bytes={record['bytes']} "
                    f"state_sha256={prior_state_sha}", flush=True)
                new_relators_completed += 1
                if max_new_relators is not None and \
                        new_relators_completed == max_new_relators:
                    if ordinal < 11:
                        raise SafeResourceStop(
                            f"j={j}:after-relator-{ordinal}-delta-authenticated",
                            "deterministic new-relator allowance reached",
                            after_j=j, after_relator=ordinal,
                            next_j=j, next_relator=ordinal + 1)
                    safe_stop_pending = True
                if not safe_stop_pending:
                    monitor.check(
                        f"j={j}:after-relator-{ordinal}-delta", force=True)

            stage = f"j={j}:membership-reduction"
            row = v3.finish_j_row(
                v1, private, workspace, echelon, receipts,
                monitor, pairing=True, left_cache=left_cache)
            row["v5_append_only_delta"] = {
                "old_pivots_unchanged": True,
                "insertion_order_prefix_preserved": True,
                "delta_count_equals_rank_increment": True,
                "terminal_state_commitment_sha256": prior_state_sha,
            }
            progression.append(row)
            require(prior_delta_record is not None and
                    prior_delta_record["relator"] == 11 and
                    terminal_header is not None,
                    "terminal delta record")
            validate_terminal_header(
                terminal_header, row, progression[:-1])
            j_data = build_j_checkpoint(
                v3, v2, summary, bindings, progression,
                prior_j_record, prior_delta_record)
            path = j_path(directory, j)
            j_record = write_j_checkpoint(
                path, j_data, v3, v2, summary, bindings)
            authenticate_record(j_record, directory, kind="j", j=j)
            prior_j_record = j_record
            print(J_MARKER + f" j={j} nonmember="
                  f"{str(row['nonmember']).lower()} "
                  f"sha256={j_record['sha256']} bytes={j_record['bytes']}",
                  flush=True)
            workspace["projector"].table.clear()
            if safe_stop_pending and not row["nonmember"] and j < 12:
                raise SafeResourceStop(
                    f"j={j}:after-j-checkpoint-authenticated",
                    "deterministic new-relator allowance reached; completed-j finalized",
                    after_j=j, after_relator=11,
                    next_j=j + 1, next_relator=1)
            monitor.check(f"j={j}:after-j-checkpoint", force=True)
            if row["nonmember"]:
                stage = f"j={j}:fresh-no-state-replay"
                replay = v3.replay_j_no_checkpoints(
                    v1, private, j, monitor, accelerators=accelerators)
                keys = ("rank_D2bar_alone", "rank_legal_overapproximation",
                        "rank_combined", "target_projected_sha256",
                        "legal_projected_rows_sha256", "nonmember")
                require(all(replay[key] == row[key] for key in keys),
                        "fresh no-state-leak BFS replay")
                break
            resumed_echelon = None
            resumed_receipts = []
            resumed_header = None
            prior_delta_record = None
            prior_state_sha = None
            active_j = j + 1

        nonmembers = [row["j"] for row in progression if row["nonmember"]]
        terminal = "R07_760_L3_TARGET6_NONMEMBER" if nonmembers else \
            "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE"
        receipt = base_output("full", summary, prior, v2_pins, bindings)
        receipt["status"] = terminal
        receipt["terminal_token"] = terminal
        result = common_result(
            progression, manifest_records(directory), resume_record)
        result["state"] = terminal
        result["first_terminal_rule_applied"] = True
        result.update({
            "max_new_relators": max_new_relators,
            "new_relators_completed": new_relators_completed,
            "safe_stop": False,
        })
        receipt["result"] = result
    except BaseException as exc:
        is_safe = isinstance(exc, SafeResourceStop)
        is_resource = is_safe or (
            v1 is not None and isinstance(exc, v1.ResourceStop))
        terminal = "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" if is_resource else \
            "R07_760_L3_TARGET6_INPUT_STOP"
        if summary is None or prior is None or v2_pins is None or \
                bindings is None:
            summary = summary or {"base": {"length": 760,
                "sha256": BASE_SHA, "parent_616_sha256": PARENT_SHA,
                "free_exponent_sums": [0, 0]}}
            prior = prior or {"inherited_candidate_prefix":
                              list(INHERITED_PREFIX)}
            v2_pins = v2_pins or {}
            bindings = bindings or {"input_authentication_complete": False}
        receipt = base_output("full", summary, prior, v2_pins, bindings)
        receipt["status"] = terminal
        receipt["terminal_token"] = terminal
        result = common_result(
            progression, manifest_records(directory), resume_record)
        stop_stage = sanitize_stop_text(getattr(exc, "stage", stage))
        stop_reason = sanitize_stop_text(exc)
        result.update({
            "state": terminal,
            "stage": stop_stage,
            "reason": stop_reason,
            "stop_stage": stop_stage,
            "stop_reason": stop_reason,
            "stop_reason_sanitized_ascii_bounded": True,
            "requested_seconds": seconds,
            "max_new_relators": max_new_relators,
            "new_relators_completed": new_relators_completed,
            "safe_stop": is_safe,
            "safe_stop_checkpoint_authenticated": is_safe,
            "safe_stop_after_j": getattr(exc, "after_j", None),
            "safe_stop_after_relator": getattr(exc, "after_relator", None),
            "exact_next_j": getattr(exc, "next_j", None),
            "exact_next_relator": getattr(exc, "next_relator", None),
            "safe_stop_completed_j_finalized": is_safe and
                getattr(exc, "after_relator", None) == 11 and
                getattr(exc, "next_j", None) != getattr(exc, "after_j", None),
        })
        receipt["result"] = result
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def toy_summary() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    summary = {
        "binding_sha256": "b" * 64,
        "Jennings": {"basis_manifest": [{
            "j": 9, "monomial_count": 3,
            "dim_Lambda_over_Ij": 19, "basis_sha256": "c" * 64,
        }]},
    }
    prior = {"binding_sha256": "d" * 64}
    bindings = {
        "fresh_projection_bindings": [{
            "j": 9, "target_projected_sha256": "e" * 64,
            "legal_projected_rows_sha256": "f" * 64,
        }],
        "binding_sha256": "0" * 64,
    }
    return summary, prior, bindings


def toy_receipt(ordinal: int, before: int, after: int) -> dict[str, Any]:
    return {
        "relator_ordinal": ordinal, "new_pivots": after - before,
        "rank_before": before, "rank_after": after,
        "max_depth_reached": 1, "max_depth_with_new_pivot": 1,
        "explored_count_by_depth": {0: 1, 1: 1},
        "v3_exact_cache_delta": {
            "left_multiply": {"hits": 0, "misses": 0},
            "Jennings_bitplane": {"hits": 0, "misses": 0}},
    }


def toy_delta_chain(v3: Any, v2: Any, v1: Any, directory: Path) \
        -> dict[str, Any]:
    summary, prior, bindings = toy_summary()
    sp = v1.F3BitSpace(19)
    echelon = v1.F3BitEchelon(sp)
    receipts = []
    prior_record = None
    prior_state = root_state_commitment(
        j=9, dimension=19, basis_sha="c" * 64,
        target_sha="e" * 64, legal_sha="f" * 64,
        prior_j_record=None)
    rows_by_relator = [
        [sp.vec({5: 1, 9: 2}), sp.vec({1: 1, 6: 1})],
        [sp.vec({3: 1, 7: 2, 12: 1})],
        [sp.vec({8: 1, 14: 2})],
    ]
    records = []
    headers = []
    for ordinal, vectors in enumerate(rows_by_relator, 1):
        before_order = list(echelon.pivots)
        before_rows = dict(echelon.pivots)
        for vector in vectors:
            require(echelon.add(vector), "toy delta independent row")
        require(all(echelon.pivots[p] == value
                    for p, value in before_rows.items()),
                "toy old pivot stable")
        suffix = list(echelon.pivots)[len(before_order):]
        receipts.append(toy_receipt(
            ordinal, len(before_order), echelon.rank()))
        header, stats = build_delta_header(
            v3, summary, prior, bindings, 9, ordinal, [], receipts,
            echelon, before_order, suffix, None, prior_record, prior_state,
            "e" * 64, "f" * 64, {"requested": True},
            {"left_multiply": {}, "Jennings_bitplane": {}})
        path = delta_path(directory, 9, ordinal)
        record = write_delta_checkpoint(
            path, header, stats, summary, prior, bindings)
        prior_record = record
        prior_state = header["cumulative_state_commitment_sha256"]
        records.append(record)
        headers.append(header)
    final_header, rebuilt, replay_records, _ = replay_delta_chain(
        delta_path(directory, 9, 3), directory,
        v3, v2, v1, summary, prior, bindings)
    require(final_header["next_relator"] == 4 and
            rebuilt.pivots == echelon.pivots and
            list(rebuilt.pivots) == list(echelon.pivots) and
            replay_records == records,
            "toy multi-delta exact next-relator replay")
    return {
        "summary": summary, "prior": prior, "bindings": bindings,
        "echelon": echelon, "records": records, "headers": headers,
        "paths": [delta_path(directory, 9, i) for i in (1, 2, 3)],
        "next_relator": final_header["next_relator"],
        "final_rank": rebuilt.rank(),
        "final_state_commitment_sha256":
            final_header["cumulative_state_commitment_sha256"],
    }


def toy_delta_replay_receipt(v3: Any, v2: Any, v1: Any) -> dict[str, Any]:
    old_default = globals()["DEFAULT_CHECKPOINT_DIR"]
    with tempfile.TemporaryDirectory(prefix="d972-r07-v5-replay-") as tmp:
        directory = Path(tmp).resolve()
        globals()["DEFAULT_CHECKPOINT_DIR"] = directory
        try:
            toy = toy_delta_chain(v3, v2, v1, directory)
            return {
                "delta_checkpoints_replayed": 3,
                "completed_relator_prefix": [1, 2, 3],
                "exact_next_relator": toy["next_relator"],
                "final_rank": toy["final_rank"],
                "final_insertion_order": list(toy["echelon"].pivots),
                "final_state_commitment_sha256":
                    toy["final_state_commitment_sha256"],
                "exact_pivot_dictionary_reconstructed": True,
                "exact_insertion_order_reconstructed": True,
            }
        finally:
            globals()["DEFAULT_CHECKPOINT_DIR"] = old_default


def postclosure_completed_j_regression(
        v3: Any, v2: Any, v1: Any) -> dict[str, Any]:
    """Exercise the exact relator-11 -> completed-j control path, cheaply."""
    old_default = globals()["DEFAULT_CHECKPOINT_DIR"]
    with tempfile.TemporaryDirectory(prefix="d972-r07-v5-postclosure-") as tmp:
        directory = Path(tmp).resolve()
        globals()["DEFAULT_CHECKPOINT_DIR"] = directory
        try:
            summary, prior, bindings = toy_summary()
            sp = v1.F3BitSpace(19)
            echelon = v1.F3BitEchelon(sp)
            receipts: list[dict[str, Any]] = []
            prior_record = None
            prior_state = root_state_commitment(
                j=9, dimension=19, basis_sha="c" * 64,
                target_sha="e" * 64, legal_sha="f" * 64,
                prior_j_record=None)
            terminal_header = None
            for ordinal in RELATOR_ORDER:
                before_order = list(echelon.pivots)
                before_rows = dict(echelon.pivots)
                require(echelon.add(sp.vec({ordinal - 1: 1})),
                        "postclosure toy independent row")
                require(all(echelon.pivots[p] == value
                            for p, value in before_rows.items()),
                        "postclosure old pivots immutable")
                suffix = list(echelon.pivots)[len(before_order):]
                receipts.append(toy_receipt(
                    ordinal, len(before_order), echelon.rank()))
                terminal_header, stats = build_delta_header(
                    v3, summary, prior, bindings, 9, ordinal, [], receipts,
                    echelon, before_order, suffix, None, prior_record,
                    prior_state, "e" * 64, "f" * 64,
                    {"requested": True},
                    {"left_multiply": {}, "Jennings_bitplane": {}})
                prior_record = write_delta_checkpoint(
                    delta_path(directory, 9, ordinal), terminal_header,
                    stats, summary, prior, bindings)
                authenticate_record(prior_record, directory, kind="delta",
                                    j=9, relator=ordinal)
                prior_state = terminal_header[
                    "cumulative_state_commitment_sha256"]
            require(terminal_header is not None and prior_record is not None,
                    "postclosure terminal delta")
            replay_header, rebuilt, records, _ = replay_delta_chain(
                delta_path(directory, 9, 11), directory,
                v3, v2, v1, summary, prior, bindings)
            require(rebuilt.pivots == echelon.pivots and len(records) == 11,
                    "postclosure terminal delta replay")
            row = {
                "j": 9, "monomial_count": 3,
                "dim_Lambda_over_Ij": 19, "basis_sha256": "c" * 64,
                "rank_D2bar_alone": 11,
                "rank_legal_overapproximation": 0,
                "rank_combined": 11,
                "target_projected_sha256": "e" * 64,
                "legal_projected_rows_sha256": "f" * 64,
                "PB4_translate_count": 649539,
                "producer_D2_algorithm": "saturated (x_i-1) BFS, D2 first",
                "per_relator_closure_receipts": copy.deepcopy(
                    replay_header["completed_closure_receipts"]),
                "nonmember": False, "separator": None,
                "v3_exact_accelerators": {
                    "row_insertion_order_changed": False,
                    "projection_cache_cleared_after_j": True,
                },
                "v5_append_only_delta": {
                    "old_pivots_unchanged": True,
                    "insertion_order_prefix_preserved": True,
                    "delta_count_equals_rank_increment": True,
                    "terminal_state_commitment_sha256": prior_state,
                },
            }
            validate_terminal_header(replay_header, row, [])
            v4 = load_v4()
            v4_typeerror = False
            v4_reason = ""
            try:
                v4.validate_public_j_row(v3, row, summary)
            except TypeError as exc:
                v4_typeerror = True
                v4_reason = sanitize_stop_text(exc)
            require(v4_typeerror and "summary" in v4_reason,
                    "v4 missing-v2 completed-j defect reproduction")
            data = build_j_checkpoint(
                v3, v2, summary, bindings, [row], None, prior_record)
            j_record = write_j_checkpoint(
                j_path(directory, 9), data, v3, v2, summary, bindings)
            authenticate_record(j_record, directory, kind="j", j=9)
            loaded, chain = load_j_checkpoint_chain(
                j_path(directory, 9), directory, v3, v2, v1,
                summary, prior, bindings)
            validate_j_checkpoint(v3, v2, loaded, summary, bindings)
            manifest = manifest_records(directory)
            require(loaded == data and len(chain) == 1 and
                    loaded["next_j"] == 10 and len(manifest) == 12 and
                    manifest[-1]["kind"] == "j",
                    "postclosure completed-j write/reload/manifest/next")
            mutated = copy.deepcopy(row)
            mutated["per_relator_closure_receipts"] = receipts[:-1]
            binding_mutation_rejected = False
            try:
                validate_terminal_header(replay_header, mutated, [])
            except RuntimeError:
                binding_mutation_rejected = True
            require(binding_mutation_rejected,
                    "postclosure terminal/public binding mutation")
            return {
                "v4_defect_reproduced": True,
                "v4_exception_class": "TypeError",
                "v4_exception_mentions_missing_summary": True,
                "v5_completed_j_validated": True,
                "completed_closure_receipts": 11,
                "terminal_relator": 11,
                "terminal_rank": 11,
                "terminal_state_commitment_sha256": prior_state,
                "terminal_header_public_row_bound": True,
                "binding_mutation_rejected": True,
                "immutable_write_reload_equal": True,
                "manifest_entries": 12,
                "manifest_delta_entries": 11,
                "manifest_j_entries": 1,
                "exact_next_j": 10,
            }
        finally:
            globals()["DEFAULT_CHECKPOINT_DIR"] = old_default


def safe_stop_toy_regression(v3: Any, v2: Any, v1: Any) -> dict[str, Any]:
    old_default = globals()["DEFAULT_CHECKPOINT_DIR"]
    with tempfile.TemporaryDirectory(prefix="d972-r07-v5-safe-stop-") as tmp:
        directory = Path(tmp).resolve()
        globals()["DEFAULT_CHECKPOINT_DIR"] = directory
        try:
            summary, prior, bindings = toy_summary()
            sp = v1.F3BitSpace(19)
            echelon = v1.F3BitEchelon(sp)
            receipts: list[dict[str, Any]] = []
            prior_record = None
            prior_state = root_state_commitment(
                j=9, dimension=19, basis_sha="c" * 64,
                target_sha="e" * 64, legal_sha="f" * 64,
                prior_j_record=None)

            def append_one(ordinal: int, current: Any,
                           current_receipts: list[dict[str, Any]],
                           ancestor: dict[str, Any] | None,
                           state: str) -> tuple[dict[str, Any], str]:
                before = list(current.pivots)
                require(current.add(sp.vec({ordinal + 4: 1})),
                        "safe-stop toy independent row")
                suffix = list(current.pivots)[len(before):]
                current_receipts.append(toy_receipt(
                    ordinal, len(before), current.rank()))
                header, stats = build_delta_header(
                    v3, summary, prior, bindings, 9, ordinal, [],
                    current_receipts, current, before, suffix, None, ancestor,
                    state, "e" * 64, "f" * 64,
                    {"requested": True},
                    {"left_multiply": {}, "Jennings_bitplane": {}})
                record = write_delta_checkpoint(
                    delta_path(directory, 9, ordinal), header, stats,
                    summary, prior, bindings)
                authenticate_record(record, directory, kind="delta", j=9,
                                    relator=ordinal)
                return record, header["cumulative_state_commitment_sha256"]

            fresh_count = 0
            for ordinal in (1, 2):
                prior_record, prior_state = append_one(
                    ordinal, echelon, receipts, prior_record, prior_state)
                fresh_count += 1
            require(fresh_count == 2, "safe-stop fresh allowance")
            resumed_header, resumed_echelon, replayed_records, _ = \
                replay_delta_chain(delta_path(directory, 9, 2), directory,
                                   v3, v2, v1, summary, prior, bindings)
            resumed_receipts = copy.deepcopy(
                resumed_header["completed_closure_receipts"])
            resumed_count = 0
            resumed_record, resumed_state = append_one(
                3, resumed_echelon, resumed_receipts, replayed_records[-1],
                resumed_header["cumulative_state_commitment_sha256"])
            resumed_count += 1
            authenticate_record(resumed_record, directory, kind="delta", j=9,
                                relator=3)
            require(fresh_count == 2 and resumed_count == 1 and
                    len(replayed_records) == 2 and
                    len(resumed_receipts) == 3,
                    "safe-stop replayed ancestors excluded")
            return {
                "fresh": {
                    "max_new_relators": 2,
                    "new_relators_completed": 2,
                    "safe_stop_after_j": 9,
                    "safe_stop_after_relator": 2,
                    "exact_next_j": 9,
                    "exact_next_relator": 3,
                    "unfinished_relator_inferred": False,
                },
                "resumed": {
                    "authenticated_ancestors_replayed": 2,
                    "max_new_relators": 1,
                    "new_relators_completed": 1,
                    "ancestors_counted_as_new": False,
                    "safe_stop_after_j": 9,
                    "safe_stop_after_relator": 3,
                    "exact_next_j": 9,
                    "exact_next_relator": 4,
                    "terminal_state_commitment_sha256": resumed_state,
                    "unfinished_relator_inferred": False,
                },
            }
        finally:
            globals()["DEFAULT_CHECKPOINT_DIR"] = old_default


def write_forged_stream(path: Path, header: dict[str, Any], rows: list[Any],
                        *, refresh_stats: bool = True,
                        refresh_state: bool = True,
                        cumulative_order: Sequence[int] | None = None) -> None:
    work = copy.deepcopy(header)
    work.pop("self_digest_sha256", None)
    raws = [canonical_bytes(row) + b"\n" for row in rows]
    if refresh_stats:
        h = hashlib.sha256()
        for raw in raws:
            h.update(raw)
        work["delta_pivot_count"] = len(rows)
        work["delta_pivot_rows_bytes"] = sum(map(len, raws))
        work["delta_pivot_rows_sha256"] = h.hexdigest()
        work["delta_insertion_order"] = [row[0] for row in rows]
        work["rank_after"] = work["rank_before"] + len(rows)
        work["cumulative_pivot_count"] = work["rank_after"]
    if cumulative_order is not None:
        work["cumulative_insertion_order_sha256"] = order_commitment(
            cumulative_order)
    if refresh_state:
        work["cumulative_state_commitment_sha256"] = extend_state_commitment(
            work["prior_cumulative_state_commitment_sha256"],
            j=work["j"],
            relator=work["completed_relator_prefix"][-1],
            rank_before=work["rank_before"], rank_after=work["rank_after"],
            pivot_raw=raws)
    work["self_digest_sha256"] = digest_obj(work)
    with path.open("wb") as raw_stream:
        with gzip.GzipFile(filename="", mode="wb", compresslevel=6,
                           fileobj=raw_stream, mtime=0) as stream:
            stream.write(canonical_bytes(work) + b"\n")
            for raw in raws:
                stream.write(raw)


def delta_mutation_tests(v3: Any, v2: Any, v1: Any) -> int:
    labels = []
    old_default = globals()["DEFAULT_CHECKPOINT_DIR"]
    with tempfile.TemporaryDirectory(prefix="d972-r07-v5-delta-") as tmp:
        directory = Path(tmp).resolve()
        globals()["DEFAULT_CHECKPOINT_DIR"] = directory
        try:
            toy = toy_delta_chain(v3, v2, v1, directory)
            summary = toy["summary"]
            prior = toy["prior"]
            bindings = toy["bindings"]
            paths = toy["paths"]
            originals = {path: path.read_bytes() for path in paths}

            def restore() -> None:
                for path, raw in originals.items():
                    path.write_bytes(raw)
                for path in directory.iterdir():
                    if path.name not in {p.name for p in paths}:
                        path.unlink()

            def reject(label: str, action: Any) -> None:
                restore()
                try:
                    action()
                except (RuntimeError, FileNotFoundError, gzip.BadGzipFile,
                        json.JSONDecodeError):
                    labels.append(label)
                    return
                raise RuntimeError("delta mutation survived: " + label)

            def replay_r2() -> None:
                replay_delta_chain(paths[1], directory, v3, v2, v1,
                                   summary, prior, bindings)

            def bit_flip() -> None:
                header = toy["headers"][1]
                with gzip.open(paths[1], "rb") as stream:
                    stream.readline()
                    row = json.loads(stream.readline())
                row[1] = canonical_hex(int(row[1], 16) ^ (1 << 10))
                write_forged_stream(paths[1], header, [row],
                                    refresh_stats=False,
                                    refresh_state=False)
                replay_r2()

            reject("delta_bit_flip", bit_flip)

            def old_rewrite() -> None:
                header = toy["headers"][1]
                row = pivot_row(5, v1.F3BitSpace(19).vec({5: 1, 10: 1}))
                write_forged_stream(
                    paths[1], header, [row],
                    cumulative_order=[5, 1, 5])
                replay_r2()

            reject("old_pivot_rewrite", old_rewrite)

            def rank_gap() -> None:
                header = copy.deepcopy(toy["headers"][1])
                header["rank_before"] = 3
                row = pivot_row(3, toy["echelon"].pivots[3])
                write_forged_stream(
                    paths[1], header, [row],
                    cumulative_order=[5, 1, 3])
                replay_r2()

            reject("rank_gap", rank_gap)

            def order_change() -> None:
                header = toy["headers"][0]
                with gzip.open(paths[0], "rb") as stream:
                    stream.readline()
                    rows = [json.loads(stream.readline()),
                            json.loads(stream.readline())]
                write_forged_stream(
                    paths[0], header, list(reversed(rows)),
                    cumulative_order=[1, 5])
                replay_r2()

            reject("delta_order_change", order_change)

            def ancestor_delete() -> None:
                paths[0].unlink()
                replay_r2()

            reject("ancestor_deletion", ancestor_delete)

            def ancestor_duplicate() -> None:
                header = copy.deepcopy(toy["headers"][1])
                header["completed_relator_prefix"] = [1, 2, 2]
                header["self_digest_sha256"] = digest_obj({
                    k: value for k, value in header.items()
                    if k != "self_digest_sha256"})
                with gzip.open(paths[1], "rb") as stream:
                    stream.readline()
                    row = json.loads(stream.readline())
                write_forged_stream(paths[1], header, [row],
                                    cumulative_order=[5, 1, 3])
                replay_r2()

            reject("ancestor_duplication", ancestor_duplicate)

            def ancestor_reorder() -> None:
                header = copy.deepcopy(toy["headers"][1])
                forged = copy.deepcopy(header["prior_delta_checkpoint"])
                forged["filename"] = delta_filename(9, 2)
                header["prior_delta_checkpoint"] = forged
                with gzip.open(paths[1], "rb") as stream:
                    stream.readline()
                    row = json.loads(stream.readline())
                write_forged_stream(paths[1], header, [row],
                                    cumulative_order=[5, 1, 3])
                replay_r2()

            reject("ancestor_reordering", ancestor_reorder)

            def prior_j_splice() -> None:
                header = copy.deepcopy(toy["headers"][0])
                header["prior_j_checkpoint"] = {
                    "kind": "j", "j": 8, "path": "forged",
                    "filename": "forged", "bytes": 1,
                    "sha256": "0" * 64}
                with gzip.open(paths[0], "rb") as stream:
                    stream.readline()
                    rows = [json.loads(stream.readline()),
                            json.loads(stream.readline())]
                write_forged_stream(paths[0], header, rows,
                                    cumulative_order=[5, 1])
                replay_delta_chain(paths[0], directory, v3, v2, v1,
                                   summary, prior, bindings)

            reject("prior_j_splice", prior_j_splice)

            def closure_splice() -> None:
                header = copy.deepcopy(toy["headers"][1])
                header["completed_closure_receipts"][0]["new_pivots"] += 1
                with gzip.open(paths[1], "rb") as stream:
                    stream.readline()
                    row = json.loads(stream.readline())
                write_forged_stream(paths[1], header, [row],
                                    cumulative_order=[5, 1, 3])
                replay_r2()

            reject("closure_roster_splice", closure_splice)

            def state_forgery() -> None:
                header = copy.deepcopy(toy["headers"][1])
                header["cumulative_state_commitment_sha256"] = "0" * 64
                header["self_digest_sha256"] = digest_obj({
                    k: value for k, value in header.items()
                    if k != "self_digest_sha256"})
                with gzip.open(paths[1], "rb") as stream:
                    stream.readline()
                    row = json.loads(stream.readline())
                write_forged_stream(paths[1], header, [row],
                                    refresh_state=False,
                                    cumulative_order=[5, 1, 3])
                replay_r2()

            reject("cumulative_state_forgery", state_forgery)

            def noncanonical() -> None:
                header = toy["headers"][1]
                with gzip.open(paths[1], "rb") as stream:
                    stream.readline()
                    row = json.loads(stream.readline())
                row[1] = "0" + row[1]
                write_forged_stream(paths[1], header, [row],
                                    cumulative_order=[5, 1, 3])
                replay_r2()

            reject("noncanonical_delta_row", noncanonical)

            def stale() -> None:
                extra = directory / delta_filename(9, 4)
                shutil.copyfile(paths[2], extra)
                require(actual_checkpoint_names(directory) ==
                        expected_names_for_resume([], 9, 3),
                        "stale injection should fail")

            reject("stale_file_injection", stale)
        finally:
            globals()["DEFAULT_CHECKPOINT_DIR"] = old_default
    require(len(labels) == 12,
            f"delta mutation count: {len(labels)} {labels}")
    return len(labels)


def j2_delta_accounting(v3: Any, v1: Any,
                        private: dict[str, Any]) -> dict[str, Any]:
    monomials = v1.enumerate_monomials(2)
    sp = v1.F3BitSpace(6 * len(monomials))
    idx = {(component, monomial): ordinal
           for ordinal, (component, monomial) in enumerate(
               (component, monomial)
               for component in range(1, 7)
               for monomial in monomials)}
    reference = v1.F3BitEchelon(sp)
    fast = v1.F3BitEchelon(sp)
    left = v3.LeftMultiplyCache(private["e4"].pc, enabled=True)
    projector = v3.JenningsBitplaneCache(
        v1, 2, monomials, sp, enabled=True)
    per_relator = []
    delta_total_count = 0
    delta_total_bytes = 0
    all_raw = []
    for ordinal, raw in enumerate(private["relator_pc"], 1):
        reference_receipt = v1.submodule_closure_with_depth(
            raw, 2, idx, sp, private["e4"].pc, reference)
        before_order = list(fast.pivots)
        before_rows = dict(fast.pivots)
        fast_receipt = v3.optimized_submodule_closure(
            raw, 2, idx, sp, private["e4"].pc, fast,
            projector, left)
        after_order = list(fast.pivots)
        suffix = after_order[len(before_order):]
        require(reference_receipt == fast_receipt and
                reference.pivots == fast.pivots and
                list(reference.pivots) == list(fast.pivots) and
                after_order[:len(before_order)] == before_order and
                all(fast.pivots[p] == vector
                    for p, vector in before_rows.items()) and
                fast_receipt["new_pivots"] == len(suffix),
                "j2 legacy/v5 append-only closure equality")
        stats = delta_stats(v3, fast, suffix)
        delta_total_count += stats["count"]
        delta_total_bytes += stats["bytes"]
        all_raw.extend(stats["raws"])
        per_relator.append({
            "relator": ordinal, "rank_before": len(before_order),
            "rank_after": len(after_order),
            "delta_count": stats["count"],
            "delta_row_bytes": stats["bytes"],
            "delta_rows_sha256": stats["sha256"],
        })
    full_insertion_raw = [
        canonical_bytes(pivot_row(pivot, fast.pivots[pivot])) + b"\n"
        for pivot in fast.pivots]
    require(delta_total_count == fast.rank() == len(full_insertion_raw) and
            delta_total_bytes == sum(map(len, full_insertion_raw)) and
            all_raw == full_insertion_raw,
            "sum delta payload equals final state once")
    return {
        "j": 2, "relators": 11,
        "delta_total_pivot_count": delta_total_count,
        "final_pivot_count": fast.rank(),
        "delta_total_row_payload_bytes": delta_total_bytes,
        "final_insertion_order_row_payload_bytes":
            sum(map(len, full_insertion_raw)),
        "identity_count_equal": True,
        "identity_payload_bytes_equal": True,
        "identity_concatenated_rows_equal": True,
        "final_pivot_dictionary_sha256":
            v3.pivot_stream_stats(fast)["sha256"],
        "final_insertion_order_sha256": digest_obj(list(fast.pivots)),
        "per_relator": per_relator,
    }


def cache_memory_estimates(v3: Any, summary: dict[str, Any]) \
        -> dict[str, Any]:
    return v3.cache_memory_estimates(summary)


def storage_bounds(v3: Any, summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in v3.checkpoint_size_estimates(summary):
        rows.append({
            "j": item["j"], "dimension": item["dimension"],
            "v5_cumulative_delta_pivot_bytes_upper":
                item["rank_equals_dimension_uncompressed_pivot_bytes_upper"],
            "v3_eleven_full_pivot_bytes_upper":
                item["eleven_full_checkpoints_uncompressed_upper"],
            "v3_to_v5_pivot_payload_upper_ratio": 11,
            "headers_additional": True,
            "gzip_size_not_claimed_before_actual_run": True,
        })
    return rows


def build_preflight() -> dict[str, Any]:
    v3, v2, v1, summary, private, prior, v2_pins, meta = build_context()
    bindings = fixed_bindings(summary, prior, meta)
    equivalence = v3.accelerator_equivalence(v1, private)
    accounting = j2_delta_accounting(v3, v1, private)
    replay_receipt = toy_delta_replay_receipt(v3, v2, v1)
    mutations = delta_mutation_tests(v3, v2, v1)
    completed_j = postclosure_completed_j_regression(v3, v2, v1)
    safe_stop = safe_stop_toy_regression(v3, v2, v1)
    receipt = base_output("preflight", summary, prior, v2_pins, bindings)
    receipt["preflight_state"] = PREFLIGHT_STATE
    receipt["result"] = {"state": "UNBUILT_GHA_ONLY"}
    receipt["delta_contract"] = {
        "schema": DELTA_SCHEMA, "completed_j_schema": J_CHECKPOINT_SCHEMA,
        "stream_format": STREAM_FORMAT, "pivot_encoding": PIVOT_ENCODING,
        "append_only_old_rows_unchanged": True,
        "insertion_order_prefix_required": True,
        "delta_rows_original_insertion_order": True,
        "authenticated_ancestor_replay_from_root": True,
        "domain_separated_cumulative_state_commitment": STATE_DOMAIN,
        "deterministic_gzip": True,
        "atomic_immutable_hardlink_publish": True,
        "mutations_rejected": mutations,
        "v4_postclosure_typeerror_reproduced": True,
        "v5_completed_j_path_repaired": True,
        "safe_stop_counts_new_relators_only": True,
        "resource_recovery_not_mathematical_result": True,
    }
    receipt["accelerator_equivalence"] = equivalence
    receipt["accelerator_memory_estimates"] = cache_memory_estimates(
        v3, summary)
    receipt["j2_delta_storage_identity"] = accounting
    receipt["toy_delta_replay_receipt"] = replay_receipt
    receipt["postclosure_completed_j_regression"] = completed_j
    receipt["safe_stop_toy_regression"] = safe_stop
    receipt["storage_bounds"] = storage_bounds(v3, summary)
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def validate_output(data: dict[str, Any]) -> None:
    verify_self_digest(data, "v5 output")
    require(data.get("schema") == SCHEMA and
            data.get("grade") == "CANDIDATE" and
            data.get("claims") == claims(),
            "v5 output envelope")
    if data.get("mode") == "preflight":
        require(data.get("preflight_state") == PREFLIGHT_STATE and
                "status" not in data and "terminal_token" not in data and
                data.get("result", {}).get("state") == "UNBUILT_GHA_ONLY" and
                data.get("accelerator_equivalence", {}).get(
                    "all_equal") is True and
                data.get("j2_delta_storage_identity", {}).get(
                    "identity_concatenated_rows_equal") is True and
                data.get("toy_delta_replay_receipt", {}).get(
                    "exact_pivot_dictionary_reconstructed") is True and
                data.get("toy_delta_replay_receipt", {}).get(
                    "exact_next_relator") == 4 and
                data.get("delta_contract", {}).get(
                    "mutations_rejected") == 12 and
                data.get("postclosure_completed_j_regression", {}).get(
                    "v4_defect_reproduced") is True and
                data.get("postclosure_completed_j_regression", {}).get(
                    "exact_next_j") == 10 and
                data.get("safe_stop_toy_regression", {}).get(
                    "resumed", {}).get("ancestors_counted_as_new") is False,
                "claim-free v5 preflight")
        return
    require(data.get("mode") == "full" and
            data.get("terminal_token") in TERMINALS and
            data.get("status") == data["terminal_token"] and
            data.get("result", {}).get("state") == data["terminal_token"],
            "v5 full terminal")
    result = data["result"]
    require(result.get("inherited_candidate_prefix") ==
                list(INHERITED_PREFIX) and
            result.get("inherited_prefix_grade") ==
                "producer_control_flow_candidate_only" and
            result.get("delta_chain_reconstructs_full_relator_state") is True and
            result.get("delta_checkpoint_is_resource_recovery_only") is True and
            result.get("cross_run_artifact_ingress_ready") is False and
            result.get("mathematical_membership_claimed") is False and
            result.get("mathematical_nonmembership_claimed") is False and
            result.get("actual_A18_lift_claimed") is False,
            "v5 result boundary")
    terminal = data["terminal_token"]
    if terminal == "R07_760_L3_TARGET6_NONMEMBER":
        require(type(result.get("first_nonmember_j")) is int and
                result.get("first_nonmember_j") in FRESH_J_ORDER and
                result.get("safe_stop") is False,
                "v5 NONMEMBER terminal fields")
    elif terminal == "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE":
        require(result.get("first_nonmember_j") is None and
                result.get("fresh_j_order_tested") == list(FRESH_J_ORDER) and
                result.get("safe_stop") is False,
                "v5 MEMBER terminal fields")
    else:
        require(type(result.get("stop_stage")) is str and
                0 < len(result["stop_stage"]) <= STOP_TEXT_LIMIT and
                result["stop_stage"] == sanitize_stop_text(
                    result["stop_stage"]) and
                type(result.get("stop_reason")) is str and
                len(result["stop_reason"]) <= STOP_TEXT_LIMIT and
                result["stop_reason"] == sanitize_stop_text(
                    result["stop_reason"]) and
                result.get("stop_reason_sanitized_ascii_bounded") is True and
                type(result.get("new_relators_completed")) is int and
                result["new_relators_completed"] >= 0,
                "v5 resource/input stop diagnostics")
        if result.get("safe_stop") is True:
            require(terminal == "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" and
                    type(result.get("max_new_relators")) is int and
                    result["new_relators_completed"] ==
                        result["max_new_relators"] and
                    result.get("safe_stop_checkpoint_authenticated") is True and
                    type(result.get("safe_stop_after_j")) is int and
                    type(result.get("safe_stop_after_relator")) is int and
                    type(result.get("exact_next_j")) is int and
                    type(result.get("exact_next_relator")) is int and
                    result.get("unfinished_relator_inferred") is False,
                    "v5 deterministic safe-stop fields")


def checked_write_output(path: Path, data: dict[str, Any]) -> bytes:
    validate_output(data)
    raw = canonical_bytes(data) + b"\n"
    full = path if path.is_absolute() else ROOT / path
    atomic_immutable_bytes(full, raw)
    return raw


def self_test() -> None:
    v3, v2, v1, summary, private, prior, _, meta = build_context()
    bindings = fixed_bindings(summary, prior, meta)
    require(bindings["base_binding"]["sha256"] == BASE_SHA,
            "v5 selftest binding")
    equivalence = v3.accelerator_equivalence(v1, private)
    accounting = j2_delta_accounting(v3, v1, private)
    replay_receipt = toy_delta_replay_receipt(v3, v2, v1)
    mutations = delta_mutation_tests(v3, v2, v1)
    completed_j = postclosure_completed_j_regression(v3, v2, v1)
    safe_stop = safe_stop_toy_regression(v3, v2, v1)
    timings = v3.benchmark_accelerators(v1, private)
    print(
        "R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_SELFTEST_PASS "
        f"delta_mutations={mutations} "
        f"j2_exhaustive={equivalence['Jennings_j2_pcvecs_exhaustive']} "
        f"j9_samples={equivalence['Jennings_j9_pcvec_samples']} "
        f"j2_relators={equivalence['full_j2_relator_closures']} "
        f"delta_count={accounting['delta_total_pivot_count']} "
        f"final_count={accounting['final_pivot_count']} "
        f"payload_bytes={accounting['delta_total_row_payload_bytes']} "
        f"toy_next_relator={replay_receipt['exact_next_relator']} "
        f"toy_rank={replay_receipt['final_rank']} "
        f"postclosure_next_j={completed_j['exact_next_j']} "
        f"safe_resumed_new={safe_stop['resumed']['new_relators_completed']} "
        f"left_warm_speedup={timings['left_warm_speedup']:.3f} "
        f"projection_warm_speedup={timings['projection_warm_speedup']:.3f} "
        "append_only=true exact_replay=true", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seconds", type=float, default=RECOMMENDED_SECONDS)
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--disable-accelerators", action="store_true")
    parser.add_argument("--max-new-relators", type=int)
    args = parser.parse_args()
    require(sum((args.self_test, args.preflight, args.full)) == 1,
            "select exactly one mode")
    if args.self_test:
        require(args.resume_checkpoint is None and
                not args.disable_accelerators,
                "selftest fixed options")
        self_test()
        return 0
    if args.preflight:
        require(args.resume_checkpoint is None and
                not args.disable_accelerators,
                "preflight fixed options")
        receipt = build_preflight()
        output = args.output or DEFAULT_PREFLIGHT
    else:
        receipt = build_full(
            args.seconds, args.checkpoint_dir, args.resume_checkpoint,
            accelerators=not args.disable_accelerators,
            max_new_relators=args.max_new_relators)
        output = args.output or DEFAULT_FULL
    raw = checked_write_output(output, receipt)
    state_key = "preflight_state" if args.preflight else "terminal_token"
    state_label = "preflight_state" if args.preflight else "terminal"
    checkpoints = 0 if args.preflight else len(
        receipt["result"]["checkpoint_manifest"])
    terminal_extra = ""
    if not args.preflight and receipt[state_key] in {
            "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
            "R07_760_L3_TARGET6_INPUT_STOP"}:
        stop_stage = receipt["result"]["stop_stage"]
        stop_reason = receipt["result"]["stop_reason"]
        terminal_extra = (
            f" stop_stage={stop_stage.replace(' ', '_')} "
            f"stop_reason_sha256="
            f"{hashlib.sha256(stop_reason.encode('ascii')).hexdigest()}")
    print(FINAL_MARKER + f" {state_label}={receipt[state_key]} "
          f"grade=CANDIDATE checkpoints={checkpoints} "
          f"sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}" +
          terminal_extra, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
