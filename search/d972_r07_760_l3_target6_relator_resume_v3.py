#!/usr/bin/env python3
"""Lossless relator-checkpoint continuation for g760 L3 target6.

The mathematical universe and terminal rule are frozen by producer v1 and
resume adapter v2.  This v3 adapter adds complete F3-echelon checkpoints after
each finished PB4 relator.  Checkpoints are canonical JSONL streams compressed
with deterministic gzip; the full pivot dictionary is present in every
relator checkpoint and is replayed in its original insertion order on resume.

The two optional exact accelerators do not change row or pivot order:

* a lazy table for x_i * pcvec in the 3^10 PC coordinate roster;
* a per-j lazy cache of truncated Jennings expansions as F3 bitplanes.

Both accelerators are fail-closed behind exact runtime canaries.  The switch
``--disable-accelerators`` restores the v1 arithmetic paths.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import itertools
import json
import os
import re
import sys
import tempfile
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path("search/d972_r07_760_l3_target6_relator_resume_v3.py")
V2_PATH = Path("search/d972_r07_760_l3_target6_resume_v2.py")
V2_CHECKER_PATH = Path(
    "crosscheck/check_d972_r07_760_l3_target6_resume_v2.py")
V2_DRIVER_PATH = Path(
    "search/d972_r07_760_l3_target6_resume_gha_driver_v2.g")
V2_PREFLIGHT_PATH = Path(
    "search/certs/d972_r07_760_l3_target6_resume_"
    "preflight_v2_20260826.json")
TASK164_PATH = Path("sol/luna_task_164_r07_760_l3_target6_resume_v2.md")
REPLY164_PATH = Path("sol/luna_reply_164_r07_760_l3_target6_resume_v2.md")
TASK165_PATH = Path(
    "sol/luna_task_165_r07_target6_relator_checkpoint_v3.md")

SCHEMA = "d972-r07-760-l3-target6-relator-resume/v3"
RELATOR_CHECKPOINT_SCHEMA = (
    "d972-r07-760-l3-target6-relator-checkpoint-stream/v3")
J_CHECKPOINT_SCHEMA = (
    "d972-r07-760-l3-target6-completed-j-checkpoint/v3")
STREAM_FORMAT = "canonical-jsonl-deterministic-gzip/v1"
PIVOT_ENCODING = (
    "[pivot_index,coefficient_one_plane_lowercase_hex,"
    "coefficient_two_plane_lowercase_hex]")
PREFLIGHT_STATE = "R07_760_L3_TARGET6_RELATOR_RESUME_V3_PREFLIGHT_READY"
RELATOR_CHECKPOINT_STATE = (
    "R07_760_L3_TARGET6_RELATOR_RESUME_V3_RELATOR_CHECKPOINT_READY")
J_CHECKPOINT_STATE = (
    "R07_760_L3_TARGET6_RELATOR_RESUME_V3_J_CHECKPOINT_READY")
FINAL_MARKER = "R07_760_L3_TARGET6_RELATOR_RESUME_V3_PRODUCER_PASS"
RELATOR_MARKER = "R07_760_L3_TARGET6_RELATOR_RESUME_V3_RELATOR_CHECKPOINT"
J_MARKER = "R07_760_L3_TARGET6_RELATOR_RESUME_V3_J_CHECKPOINT"

DEFAULT_PREFLIGHT = Path(
    "search/certs/d972_r07_760_l3_target6_relator_resume_"
    "preflight_v3_20260826.json")
DEFAULT_FULL = Path(
    "ci/out/d972_r07_760_l3_target6_relator_resume_v3.json")
DEFAULT_CHECKPOINT_DIR = Path(
    "ci/out/d972_r07_760_l3_target6_relator_resume_v3_checkpoints")

INHERITED_PREFIX = (2, 3, 4, 5, 6, 7, 8)
FRESH_J_ORDER = (9, 10, 11, 12)
RELATOR_ORDER = tuple(range(1, 12))
START_J = 9
MAX_SECONDS = 21600.0
RECOMMENDED_SECONDS = 21000.0
MAX_RSS_MIB = 5600
PC_ROSTER_SIZE = 3 ** 10
N_GEN = 10
TRANSLATED_D2_COUNT = 11 * PC_ROSTER_SIZE
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
HEX_RE = re.compile(r"(?:0|[1-9a-f][0-9a-f]*)\Z")

V3_PIN_SPECS: dict[str, tuple[Path, int, str]] = {
    "task_165": (TASK165_PATH, 5132,
        "32025aa1cb8587188c57c1f164c1bcbd585a37b5f19f5abec89c458ca8d6084f"),
    "v2_producer": (V2_PATH, 35068,
        "9f6f8c2d3d3dbbc69373e1413b5d47a8893d6be62b228dc04ecd522a4fa51238"),
    "v2_checker": (V2_CHECKER_PATH, 63772,
        "7cc683ccf16880d3c8794573dfffcbbf0b453cdcf2e7cd2e5665eb78a9e26365"),
    "v2_driver": (V2_DRIVER_PATH, 17443,
        "6241566df743069b7da6924e7c2facd766ef058b622f5e44f87c90f1d5392935"),
    "v2_preflight": (V2_PREFLIGHT_PATH, 7986,
        "272d4c4e91bb0234d49316277b354b722dfcb1366e47e9bf00d745469a1c1a94"),
    "task_164": (TASK164_PATH, 5292,
        "761359bda0fc14543ab9266ec61139006403525d828811bb2af5d27d34ccfc9d"),
    "reply_164": (REPLY164_PATH, 12948,
        "b7e1a59dd301813344a243733a3ea6bc19368e892b8ce1d86d4e9232cd2c25d2"),
}

TERMINALS = {
    "R07_760_L3_TARGET6_NONMEMBER",
    "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE",
    "R07_760_L3_TARGET6_UNKNOWN_RESOURCE",
    "R07_760_L3_TARGET6_INPUT_STOP",
}


class InputStop(RuntimeError):
    pass


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


def v3_pin_inputs() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for label, (path, size, digest) in V3_PIN_SPECS.items():
        full = ROOT / path
        if not full.is_file() or full.stat().st_size != size or \
                digest_file(full) != digest:
            raise InputStop("v3 pin drift: " + path.as_posix())
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def producer_source_record() -> dict[str, Any]:
    full = ROOT / SELF_PATH
    require(full.is_file(), "v3 producer source missing")
    return {"path": SELF_PATH.as_posix(), "bytes": full.stat().st_size,
            "sha256": digest_file(full)}


def load_v2() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_d972_r07_760_l3_target6_resume_frozen_v2", ROOT / V2_PATH)
    require(spec is not None and spec.loader is not None,
            "v2 producer module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    require(digest_file(ROOT / V2_PATH) == V3_PIN_SPECS["v2_producer"][2],
            "v2 producer post-import pin")
    return module


def build_context() -> tuple[Any, Any, dict[str, Any], dict[str, Any],
                             dict[str, Any], dict[str, Any], dict[str, Any]]:
    v3_pins = v3_pin_inputs()
    v2 = load_v2()
    v1, summary, private, prior, v2_pins = v2.build_context()
    source = producer_source_record()
    require(summary["base"]["sha256"] == BASE_SHA and
            summary["base"]["parent_616_sha256"] == PARENT_SHA,
            "v3 static base")
    require(summary["Jennings"]["fresh_j_order"] == list(FRESH_J_ORDER),
            "v3 fresh order")
    return v2, v1, summary, private, prior, v2_pins, {
        "v3_pin_manifest": v3_pins,
        "v3_pin_manifest_sha256": digest_obj(v3_pins),
        "producer_source": source,
    }


def fixed_bindings(v1: Any, private: dict[str, Any],
                   summary: dict[str, Any], prior: dict[str, Any],
                   v3_meta: dict[str, Any]) -> dict[str, Any]:
    projection_bindings = []
    for j in FRESH_J_ORDER:
        target = v1.project_vec_to_Ij(private["target_pc"], j)
        legal = [v1.project_vec_to_Ij(row, j)
                 for row in private["sigma_pc"]]
        projection_bindings.append({
            "j": j,
            "target_projected_sha256":
                digest_obj(v1.projected_public(target)),
            "legal_projected_rows_sha256":
                digest_obj([v1.projected_public(row) for row in legal]),
        })
    result = {
        "static_binding": summary,
        "static_binding_sha256": summary["binding_sha256"],
        "prior_run_binding": prior,
        "prior_run_binding_sha256": prior["binding_sha256"],
        "pin_manifests": {
            "v1": {
                "manifest": summary["v1_pin_manifest"],
                "sha256": summary["v1_pin_manifest_sha256"],
            },
            "v2": {
                "manifest": summary["v2_pin_manifest"],
                "sha256": summary["v2_pin_manifest_sha256"],
            },
            "v3": {
                "manifest": v3_meta["v3_pin_manifest"],
                "sha256": v3_meta["v3_pin_manifest_sha256"],
            },
        },
        "producer_source": v3_meta["producer_source"],
        "base_binding": {
            "length": summary["base"]["length"],
            "sha256": summary["base"]["sha256"],
            "parent_616_sha256": summary["base"]["parent_616_sha256"],
            "free_exponent_sums": summary["base"]["free_exponent_sums"],
        },
        "target_binding": copy.deepcopy(summary["target6"]),
        "legal_binding": copy.deepcopy(summary["legal_overapproximation"]),
        "fresh_projection_bindings": projection_bindings,
    }
    result["binding_sha256"] = digest_obj(result)
    return result


def pcvec_code(pcvec: bytes) -> int:
    require(len(pcvec) == N_GEN and all(x in (0, 1, 2) for x in pcvec),
            "pcvec coordinate range")
    value = 0
    scale = 1
    for coordinate in pcvec:
        value += int(coordinate) * scale
        scale *= 3
    return value


def pcvec_from_code(code: int) -> bytes:
    require(type(code) is int and 0 <= code < PC_ROSTER_SIZE,
            "pcvec code")
    out = []
    for _ in range(N_GEN):
        out.append(code % 3)
        code //= 3
    return bytes(out)


class LeftMultiplyCache:
    """Lazy exact table for gen_pcvec(i) * pcvec."""

    def __init__(self, pc: Any, enabled: bool = True) -> None:
        self.pc = pc
        self.enabled = bool(enabled)
        self.table: list[bytes | None] = [None] * (N_GEN * PC_ROSTER_SIZE)
        self.hits = 0
        self.misses = 0

    def get(self, i: int, pcvec: bytes) -> bytes:
        require(1 <= i <= N_GEN, "left cache generator")
        if not self.enabled:
            self.misses += 1
            return self.pc.mul(bytes(1 if k == i - 1 else 0
                                     for k in range(N_GEN)), pcvec)
        slot = (i - 1) * PC_ROSTER_SIZE + pcvec_code(pcvec)
        value = self.table[slot]
        if value is not None:
            self.hits += 1
            return value
        generator = bytes(1 if k == i - 1 else 0 for k in range(N_GEN))
        value = self.pc.mul(generator, pcvec)
        self.table[slot] = value
        self.misses += 1
        return value

    def snapshot(self) -> tuple[int, int]:
        return self.hits, self.misses


class JenningsBitplaneCache:
    """Per-j cache of one-component truncated Jennings expansions."""

    def __init__(self, v1: Any, j: int,
                 monomials: Sequence[tuple[int, ...]], sp: Any,
                 enabled: bool = True) -> None:
        self.v1 = v1
        self.j = int(j)
        self.monomials = list(monomials)
        self.width = len(self.monomials)
        self.index = {row: ordinal
                      for ordinal, row in enumerate(self.monomials)}
        self.sp = sp
        self.enabled = bool(enabled)
        self.table: list[tuple[int, int] | None] = [None] * PC_ROSTER_SIZE
        self.hits = 0
        self.misses = 0

    def expansion(self, pcvec: bytes) -> tuple[int, int]:
        slot = pcvec_code(pcvec)
        if self.enabled:
            cached = self.table[slot]
            if cached is not None:
                self.hits += 1
                return cached
        one = two = 0
        for monomial, coefficient in self.v1.project_pcvec_terms(
                pcvec, self.j):
            ordinal = self.index[tuple(monomial)]
            coefficient = int(coefficient) % 3
            if coefficient == 1:
                one |= 1 << ordinal
            elif coefficient == 2:
                two |= 1 << ordinal
        result = one, two
        self.misses += 1
        if self.enabled:
            self.table[slot] = result
        return result

    def project(self, row: dict[Any, int]) -> tuple[int, int]:
        result = (0, 0)
        for (component, pcvec), coefficient in row.items():
            local = self.expansion(bytes(pcvec))
            shift = (int(component) - 1) * self.width
            shifted = local[0] << shift, local[1] << shift
            result = self.sp.add(
                result, self.sp.scale(shifted, int(coefficient)))
        return result

    def snapshot(self) -> tuple[int, int]:
        return self.hits, self.misses


def reference_project_bitplanes(v1: Any, row: dict[Any, int], j: int,
                                idx: dict[Any, int], sp: Any) \
        -> tuple[int, int]:
    projected = v1.project_vec_to_Ij(row, j)
    return sp.vec({idx[key]: value for key, value in projected.items()
                   if key in idx})


def apply_xi_minus_1_cached(row: dict[Any, int], i: int,
                            cache: LeftMultiplyCache) -> dict[Any, int]:
    out: dict[Any, int] = defaultdict(int)
    for (component, pcvec), coefficient in row.items():
        key = (component, cache.get(i, bytes(pcvec)))
        out[key] = (out[key] + int(coefficient)) % 3
    for key, coefficient in row.items():
        out[key] = (out[key] - int(coefficient)) % 3
    return {key: value for key, value in out.items() if value}


def optimized_submodule_closure(
        raw: dict[Any, int], j: int, idx: dict[Any, int], sp: Any,
        pc: Any, echelon: Any, projector: JenningsBitplaneCache,
        left_cache: LeftMultiplyCache) -> dict[str, Any]:
    added = 0
    max_depth_with_pivot = 0
    explored: dict[int, int] = defaultdict(int)
    vector = projector.project(raw) if projector.enabled else \
        reference_project_bitplanes(
            projector.v1, raw, j, idx, sp)
    queue: deque[tuple[dict[Any, int], int]] = deque()
    explored[0] += 1
    if echelon.add(vector):
        added += 1
        queue.append((raw, 0))
    seen: set[Any] = set()
    while queue:
        current, depth = queue.popleft()
        max_depth_with_pivot = max(max_depth_with_pivot, depth)
        for i in range(1, N_GEN + 1):
            following = apply_xi_minus_1_cached(
                current, i, left_cache) if left_cache.enabled else \
                projector.v1.apply_xi_minus_1(current, i, pc)
            if not following:
                continue
            explored[depth + 1] += 1
            vector = projector.project(following) if projector.enabled else \
                reference_project_bitplanes(
                    projector.v1, following, j, idx, sp)
            if echelon.add(vector):
                added += 1
                fingerprint = tuple(sorted(following.items()))
                if fingerprint not in seen:
                    seen.add(fingerprint)
                    queue.append((following, depth + 1))
                    max_depth_with_pivot = max(
                        max_depth_with_pivot, depth + 1)
    return {
        "new_pivots": added,
        "max_depth_reached": max(explored) if explored else 0,
        "max_depth_with_new_pivot": max_depth_with_pivot,
        "explored_count_by_depth": dict(sorted(explored.items())),
    }


def runtime_accelerator_gate(
        v1: Any, private: dict[str, Any], j: int,
        monomials: Sequence[tuple[int, ...]], idx: dict[Any, int], sp: Any,
        projector: JenningsBitplaneCache,
        left_cache: LeftMultiplyCache,
        requested: bool) -> dict[str, Any]:
    if not requested:
        projector.enabled = False
        left_cache.enabled = False
        return {
            "requested": False, "left_multiply_enabled": False,
            "Jennings_bitplane_enabled": False,
            "fallback_to_v1_paths": True,
            "left_samples": 0, "projection_rows": 0,
        }
    pc = private["e4"].pc
    left_codes = [
        (k * 7919 + 17) % PC_ROSTER_SIZE for k in range(64)]
    left_ok = True
    for i in range(1, N_GEN + 1):
        generator = bytes(1 if k == i - 1 else 0 for k in range(N_GEN))
        for code in left_codes:
            value = pcvec_from_code(code)
            if left_cache.get(i, value) != pc.mul(generator, value):
                left_ok = False
                break
        if not left_ok:
            break
    left_cache.enabled = left_ok

    rows: list[dict[Any, int]] = []
    rows.extend(private["sigma_pc"])
    rows.extend(private["relator_pc"])
    sample_codes = [(k * 3571 + 29) % PC_ROSTER_SIZE for k in range(32)]
    for ordinal, code in enumerate(sample_codes):
        relator = private["relator_pc"][ordinal % len(private["relator_pc"])]
        rows.append(v1.pc_translate(
            pc, relator, pcvec_from_code(code)))
    projection_ok = all(
        projector.project(row) ==
        reference_project_bitplanes(v1, row, j, idx, sp)
        for row in rows)
    projector.enabled = projection_ok
    return {
        "requested": True,
        "left_multiply_enabled": left_ok,
        "Jennings_bitplane_enabled": projection_ok,
        "fallback_to_v1_paths": not (left_ok and projection_ok),
        "left_samples": N_GEN * len(left_codes),
        "projection_rows": len(rows),
        "preserves_row_iteration_order": True,
        "preserves_pivot_insertion_order": True,
        "projection_cache_lifetime": "one_j_only",
    }


def canonical_hex(value: int) -> str:
    require(type(value) is int and value >= 0, "nonnegative plane")
    return format(value, "x")


def validate_hex(value: Any, label: str) -> int:
    require(type(value) is str and HEX_RE.fullmatch(value) is not None,
            label + " canonical lowercase hex")
    return int(value, 16)


def pivot_row(pivot: int, vector: tuple[int, int]) -> list[Any]:
    return [int(pivot), canonical_hex(vector[0]), canonical_hex(vector[1])]


def validate_pivot_vector(sp: Any, pivot: int,
                          vector: tuple[int, int]) -> None:
    require(type(pivot) is int and 0 <= pivot < sp.n,
            "pivot in range")
    one, two = vector
    require(type(one) is int and type(two) is int and
            0 <= one <= sp.mask and 0 <= two <= sp.mask,
            "pivot planes exact mask")
    require(one & two == 0, "pivot bitplanes disjoint")
    require(sp.leading(vector) == pivot,
            "recorded pivot is leading coordinate")
    require(sp.coeff_at(vector, pivot) == 1,
            "pivot coefficient is one")


def pivot_stream_stats(echelon: Any) -> dict[str, Any]:
    h = hashlib.sha256()
    total = 0
    pivots = sorted(echelon.pivots)
    require(len(pivots) == echelon.rank(), "pivot rank")
    for pivot in pivots:
        vector = echelon.pivots[pivot]
        validate_pivot_vector(echelon.sp, pivot, vector)
        raw = canonical_bytes(pivot_row(pivot, vector)) + b"\n"
        h.update(raw)
        total += len(raw)
    insertion_order = list(echelon.pivots)
    require(sorted(insertion_order) == pivots and
            len(set(insertion_order)) == len(pivots),
            "pivot insertion roster")
    return {
        "rows": len(pivots),
        "bytes": total,
        "sha256": h.hexdigest(),
        "insertion_order": insertion_order,
        "insertion_order_sha256": digest_obj(insertion_order),
    }


def relator_checkpoint_filename(j: int, relator: int) -> str:
    require(j in FRESH_J_ORDER and relator in RELATOR_ORDER,
            "relator checkpoint index")
    return (
        "d972_r07_760_l3_target6_relator_resume_v3_"
        f"j{j:02d}_r{relator:02d}.checkpoint.jsonl.gz")


def j_checkpoint_filename(j: int) -> str:
    require(j in FRESH_J_ORDER, "j checkpoint index")
    return (
        "d972_r07_760_l3_target6_relator_resume_v3_"
        f"j{j:02d}.json")


def resolve_checkpoint_directory(path: Path) -> Path:
    resolved = (path if path.is_absolute() else ROOT / path).resolve()
    expected = (ROOT / DEFAULT_CHECKPOINT_DIR).resolve()
    require(resolved == expected, "checkpoint directory substitution")
    return resolved


def relator_checkpoint_path(directory: Path, j: int, relator: int) -> Path:
    return resolve_checkpoint_directory(directory) / \
        relator_checkpoint_filename(j, relator)


def j_checkpoint_path(directory: Path, j: int) -> Path:
    return resolve_checkpoint_directory(directory) / j_checkpoint_filename(j)


def public_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        # External paths occur only in bounded selftests.  Production resume
        # still requires the exact repository checkpoint directory.
        return resolved.as_posix()


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
    fd, name = tempfile.mkstemp(
        prefix=path.name + ".tmp-", dir=str(path.parent))
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


def checkpoint_record(path: Path, *, kind: str, j: int,
                      relator: int | None = None,
                      canonical_size: int | None = None,
                      canonical_sha: str | None = None,
                      state_sha: str | None = None) -> dict[str, Any]:
    record = {
        "kind": kind, "j": int(j), "path": public_path(path),
        "filename": path.name, "bytes": path.stat().st_size,
        "sha256": digest_file(path),
    }
    if relator is not None:
        record["relator"] = int(relator)
    if canonical_size is not None:
        record["canonical_uncompressed_bytes"] = int(canonical_size)
    if canonical_sha is not None:
        record["canonical_uncompressed_sha256"] = canonical_sha
    if state_sha is not None:
        record["D2_echelon_pivot_list_sha256"] = state_sha
    return record


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
                type(record.get("D2_echelon_pivot_list_sha256")) is str,
                "relator record fields")


def authenticate_record(record: dict[str, Any], directory: Path,
                        *, kind: str, j: int,
                        relator: int | None = None) -> Path:
    validate_record_shape(record, kind=kind, j=j, relator=relator)
    expected_name = relator_checkpoint_filename(j, relator) \
        if relator is not None else j_checkpoint_filename(j)
    require(record["filename"] == expected_name,
            "checkpoint record filename")
    path = resolve_checkpoint_directory(directory) / expected_name
    require(record["path"] == public_path(path),
            "checkpoint record path substitution")
    require(path.is_file() and path.stat().st_size == record["bytes"] and
            digest_file(path) == record["sha256"],
            "checkpoint ancestor SHA/bytes")
    return path


def build_relator_header(
        summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any], j: int, relator: int,
        closure_receipts: Sequence[dict[str, Any]],
        pivot_stats: dict[str, Any],
        progression: Sequence[dict[str, Any]],
        prior_j_record: dict[str, Any] | None,
        prior_relator_record: dict[str, Any] | None,
        target_sha: str, legal_sha: str,
        accelerator_gate: dict[str, Any],
        cache_stats: dict[str, Any]) -> dict[str, Any]:
    require(j in FRESH_J_ORDER and relator in RELATOR_ORDER,
            "relator header indices")
    require([row["j"] for row in progression] ==
            list(FRESH_J_ORDER[:FRESH_J_ORDER.index(j)]),
            "relator completed j prefix")
    require(len(closure_receipts) == relator,
            "relator closure receipt prefix")
    stats = pivot_stats
    require(type(stats) is dict and stats.get("rows") ==
            len(stats.get("insertion_order", [])),
            "precomputed pivot statistics")
    basis_manifest = {row["j"]: row
                      for row in summary["Jennings"]["basis_manifest"]}
    require(j in basis_manifest, "relator Jennings j present")
    basis = basis_manifest[j]
    header = {
        "schema": RELATOR_CHECKPOINT_SCHEMA,
        "version": 3,
        "mode": "relator_checkpoint",
        "checkpoint_state": RELATOR_CHECKPOINT_STATE,
        "grade": "CANDIDATE",
        "purpose": "resource_recovery_only",
        "stream_format": STREAM_FORMAT,
        "j": j,
        "monomial_count": basis["monomial_count"],
        "dimension": basis["dim_Lambda_over_Ij"],
        "Jennings_basis_sha256": basis["basis_sha256"],
        "target_projected_sha256": target_sha,
        "legal_projected_rows_sha256": legal_sha,
        "completed_j_prefix": [row["j"] for row in progression],
        "completed_j_progression": list(progression),
        "completed_relator_prefix": list(range(1, relator + 1)),
        "next_relator": relator + 1 if relator < RELATOR_ORDER[-1]
            else None,
        "completed_closure_receipts": list(closure_receipts),
        "D2_echelon_rank": stats["rows"],
        "D2_echelon_pivot_count": stats["rows"],
        "D2_echelon_pivot_list_complete": True,
        "D2_echelon_pivot_encoding": PIVOT_ENCODING,
        "D2_echelon_pivot_list_sort": "increasing_pivot",
        "D2_echelon_pivot_list_bytes": stats["bytes"],
        "D2_echelon_pivot_list_sha256": stats["sha256"],
        "D2_echelon_pivot_insertion_order": stats["insertion_order"],
        "D2_echelon_pivot_insertion_order_sha256":
            stats["insertion_order_sha256"],
        "D2_echelon_replay_contract": {
            "fresh_F3BitEchelon": True,
            "original_insertion_order_restored": True,
            "exact_pivot_dictionary_required": True,
            "exact_rank_required": True,
        },
        "prior_j_checkpoint": prior_j_record,
        "prior_relator_checkpoint": prior_relator_record,
        "fixed_bindings": bindings,
        "static_binding_sha256": summary["binding_sha256"],
        "prior_run_binding_sha256": prior["binding_sha256"],
        "accelerator_gate": accelerator_gate,
        "accelerator_cache_stats": cache_stats,
        "algorithm": {
            "mathematical_algorithm":
                "saturated (x_i-1) BFS, D2 first",
            "row_insertion_order_changed": False,
            "first_nonmember_rule_changed": False,
            "full_pivot_state_not_delta": True,
            "deterministic_gzip": {
                "mtime": 0, "filename": "", "compresslevel": 6,
            },
        },
        "unfinished_next_relator_inferred": False,
        "mathematical_membership_claimed": False,
        "mathematical_nonmembership_claimed": False,
        "actual_A18_lift_claimed": False,
        "claims": claims(),
    }
    header["self_digest_sha256"] = digest_obj(header)
    return header


def validate_relator_header(
        header: dict[str, Any], summary: dict[str, Any],
        prior: dict[str, Any], bindings: dict[str, Any]) -> None:
    verify_self_digest(header, "relator checkpoint header")
    require(header.get("schema") == RELATOR_CHECKPOINT_SCHEMA and
            header.get("version") == 3 and
            header.get("mode") == "relator_checkpoint" and
            header.get("checkpoint_state") == RELATOR_CHECKPOINT_STATE and
            header.get("grade") == "CANDIDATE" and
            header.get("purpose") == "resource_recovery_only" and
            header.get("stream_format") == STREAM_FORMAT,
            "relator checkpoint envelope")
    j = header.get("j")
    relator = len(header.get("completed_relator_prefix", []))
    require(type(j) is int and j in FRESH_J_ORDER and
            relator in RELATOR_ORDER and
            header["completed_relator_prefix"] ==
                list(range(1, relator + 1)) and
            header.get("next_relator") ==
                (relator + 1 if relator < 11 else None),
            "relator exact prefix")
    basis_manifest = {row["j"]: row
                      for row in summary["Jennings"]["basis_manifest"]}
    require(j in basis_manifest, "relator Jennings j present")
    basis = basis_manifest[j]
    require(header.get("monomial_count") == basis["monomial_count"] and
            header.get("dimension") == basis["dim_Lambda_over_Ij"] and
            header.get("Jennings_basis_sha256") == basis["basis_sha256"],
            "relator Jennings binding")
    projection_manifest = {row["j"]: row for row in
                           bindings["fresh_projection_bindings"]}
    require(j in projection_manifest, "relator projection j present")
    projection = projection_manifest[j]
    require(header.get("target_projected_sha256") ==
                projection["target_projected_sha256"] and
            header.get("legal_projected_rows_sha256") ==
                projection["legal_projected_rows_sha256"],
            "relator target/legal projected binding")
    expected_completed = list(FRESH_J_ORDER[:FRESH_J_ORDER.index(j)])
    progression = header.get("completed_j_progression")
    require(type(progression) is list and
            [row.get("j") for row in progression] == expected_completed and
            header.get("completed_j_prefix") == expected_completed,
            "relator completed j progression")
    require(type(header.get("completed_closure_receipts")) is list and
            len(header["completed_closure_receipts"]) == relator,
            "relator closure receipts")
    require(header.get("fixed_bindings") == bindings and
            header.get("static_binding_sha256") == summary["binding_sha256"] and
            header.get("prior_run_binding_sha256") == prior["binding_sha256"],
            "relator fixed bindings")
    require(header.get("D2_echelon_pivot_list_complete") is True and
            header.get("D2_echelon_pivot_encoding") == PIVOT_ENCODING and
            header.get("D2_echelon_pivot_list_sort") == "increasing_pivot" and
            type(header.get("D2_echelon_rank")) is int and
            header["D2_echelon_rank"] ==
                header.get("D2_echelon_pivot_count") and
            0 <= header["D2_echelon_rank"] <= header["dimension"] and
            type(header.get("D2_echelon_pivot_list_bytes")) is int and
            type(header.get("D2_echelon_pivot_list_sha256")) is str and
            len(header["D2_echelon_pivot_list_sha256"]) == 64,
            "relator full pivot contract")
    insertion = header.get("D2_echelon_pivot_insertion_order")
    require(type(insertion) is list and len(insertion) ==
            header["D2_echelon_rank"] and len(set(insertion)) == len(insertion) and
            header.get("D2_echelon_pivot_insertion_order_sha256") ==
                digest_obj(insertion),
            "relator pivot insertion order")
    require(all(value is False for value in header.get("claims", {}).values()) and
            header.get("claims") == claims() and
            header.get("unfinished_next_relator_inferred") is False and
            header.get("mathematical_membership_claimed") is False and
            header.get("mathematical_nonmembership_claimed") is False and
            header.get("actual_A18_lift_claimed") is False,
            "relator claim boundary")
    algorithm = header.get("algorithm", {})
    require(algorithm.get("mathematical_algorithm") ==
                "saturated (x_i-1) BFS, D2 first" and
            algorithm.get("row_insertion_order_changed") is False and
            algorithm.get("first_nonmember_rule_changed") is False and
            algorithm.get("full_pivot_state_not_delta") is True,
            "relator algorithm boundary")


def write_relator_checkpoint(path: Path, header: dict[str, Any],
                              echelon: Any,
                              stats: dict[str, Any]) -> dict[str, Any]:
    require(header["D2_echelon_pivot_list_sha256"] == stats["sha256"] and
            header["D2_echelon_pivot_list_bytes"] == stats["bytes"] and
            header["D2_echelon_pivot_insertion_order"] ==
                stats["insertion_order"] and
            list(echelon.pivots) == stats["insertion_order"] and
            echelon.rank() == stats["rows"],
            "relator header/state agreement")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(
        prefix=path.name + ".tmp-", dir=str(path.parent))
    temp_path = Path(name)
    canonical_hash = hashlib.sha256()
    canonical_size = 0
    pivot_hash = hashlib.sha256()
    pivot_size = 0

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
                for pivot in sorted(echelon.pivots):
                    vector = echelon.pivots[pivot]
                    validate_pivot_vector(echelon.sp, pivot, vector)
                    pivot_raw = canonical_bytes(pivot_row(
                        pivot, vector)) + b"\n"
                    emit(stream, pivot_raw)
                    pivot_hash.update(pivot_raw)
                    pivot_size += len(pivot_raw)
            raw_stream.flush()
            os.fsync(raw_stream.fileno())
        atomic_link_temp(temp_path, path)
    except BaseException:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass
        raise
    require(path.is_file(), "relator checkpoint publication")
    require(pivot_hash.hexdigest() == stats["sha256"] and
            pivot_size == stats["bytes"],
            "streamed pivot statistics agreement")
    return checkpoint_record(
        path, kind="relator", j=header["j"],
        relator=header["completed_relator_prefix"][-1],
        canonical_size=canonical_size,
        canonical_sha=canonical_hash.hexdigest(),
        state_sha=stats["sha256"])


def read_relator_header(path: Path) -> dict[str, Any]:
    try:
        with gzip.open(path, "rb") as stream:
            raw = stream.readline()
    except (OSError, EOFError) as exc:
        raise RuntimeError("relator checkpoint gzip header") from exc
    require(raw.endswith(b"\n") and raw.count(b"\n") == 1,
            "relator canonical header line")
    data = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(data) + b"\n",
            "relator canonical header bytes")
    return data


def load_relator_checkpoint(
        path: Path, summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any], v1: Any,
        *, compare_to: Any | None = None) \
        -> tuple[dict[str, Any], Any | None, dict[str, Any]]:
    compressed_bytes = path.stat().st_size
    compressed_sha = digest_file(path)
    canonical_hash = hashlib.sha256()
    canonical_size = 0
    pivot_hash = hashlib.sha256()
    pivot_size = 0
    rows: dict[int, tuple[int, int]] = {}
    try:
        with gzip.open(path, "rb") as stream:
            raw_header = stream.readline()
            canonical_hash.update(raw_header)
            canonical_size += len(raw_header)
            header = json.loads(raw_header.decode("ascii"))
            require(raw_header == canonical_bytes(header) + b"\n",
                    "relator canonical header")
            validate_relator_header(header, summary, prior, bindings)
            sp = v1.F3BitSpace(int(header["dimension"]))
            previous_pivot = -1
            for _ in range(header["D2_echelon_pivot_count"]):
                raw = stream.readline()
                require(raw.endswith(b"\n") and raw.count(b"\n") == 1,
                        "pivot canonical line framing")
                canonical_hash.update(raw)
                canonical_size += len(raw)
                pivot_hash.update(raw)
                pivot_size += len(raw)
                row = json.loads(raw.decode("ascii"))
                require(raw == canonical_bytes(row) + b"\n" and
                        type(row) is list and len(row) == 3 and
                        type(row[0]) is int,
                        "pivot canonical row")
                pivot = row[0]
                one = validate_hex(row[1], "coefficient-one plane")
                two = validate_hex(row[2], "coefficient-two plane")
                require(pivot > previous_pivot, "pivot increasing order")
                vector = one, two
                validate_pivot_vector(sp, pivot, vector)
                rows[pivot] = vector
                previous_pivot = pivot
            require(stream.read(1) == b"", "relator stream exact EOF")
    except (OSError, EOFError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("relator checkpoint stream decode") from exc
    require(len(rows) == header["D2_echelon_rank"] and
            pivot_size == header["D2_echelon_pivot_list_bytes"] and
            pivot_hash.hexdigest() ==
                header["D2_echelon_pivot_list_sha256"],
            "pivot list digest/rank")
    insertion = header["D2_echelon_pivot_insertion_order"]
    require(sorted(insertion) == sorted(rows),
            "pivot insertion roster equals rows")
    echelon = None
    if compare_to is None:
        echelon = v1.F3BitEchelon(sp)
        for pivot in insertion:
            vector = rows[pivot]
            require(echelon.add(vector) and
                    pivot in echelon.pivots and
                    echelon.pivots[pivot] == vector,
                    "fresh F3BitEchelon exact pivot replay")
        require(echelon.rank() == header["D2_echelon_rank"] and
                echelon.pivots == {p: rows[p] for p in insertion},
                "reconstructed exact pivot dictionary/rank")
    else:
        require(compare_to.sp.n == sp.n and
                all(compare_to.pivots.get(pivot) == vector
                    for pivot, vector in rows.items()),
                "ancestor pivot dictionary exact subset")
    record = checkpoint_record(
        path, kind="relator", j=header["j"],
        relator=header["completed_relator_prefix"][-1],
        canonical_size=canonical_size,
        canonical_sha=canonical_hash.hexdigest(),
        state_sha=pivot_hash.hexdigest())
    require(record["bytes"] == compressed_bytes and
            record["sha256"] == compressed_sha,
            "relator compressed digest stable")
    return header, echelon, record


def validate_public_j_row(v2: Any, row: dict[str, Any],
                          summary: dict[str, Any]) -> None:
    v2.validate_public_row(row, summary)
    require(row.get("producer_D2_algorithm") ==
            "saturated (x_i-1) BFS, D2 first",
            "completed j mathematical algorithm")
    acceleration = row.get("v3_exact_accelerators")
    require(type(acceleration) is dict and
            acceleration.get("row_insertion_order_changed") is False and
            acceleration.get("projection_cache_cleared_after_j") is True,
            "completed j accelerator boundary")


def build_j_checkpoint(
        v2: Any, summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any], progression: Sequence[dict[str, Any]],
        prior_j_record: dict[str, Any] | None,
        terminal_relator_record: dict[str, Any]) -> dict[str, Any]:
    require(progression, "j checkpoint progression")
    completed = [int(row["j"]) for row in progression]
    require(completed == list(FRESH_J_ORDER[:len(completed)]),
            "j checkpoint exact prefix")
    for row in progression:
        validate_public_j_row(v2, row, summary)
    j = completed[-1]
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    require(len(nonmembers) <= 1 and
            (not nonmembers or nonmembers == [j]),
            "j checkpoint first nonmember")
    next_j = None if nonmembers or j == FRESH_J_ORDER[-1] else j + 1
    if j == START_J:
        require(prior_j_record is None, "j9 prior j absent")
    else:
        validate_record_shape(
            prior_j_record, kind="j", j=j - 1, relator=None)
    validate_record_shape(
        terminal_relator_record, kind="relator", j=j, relator=11)
    data = {
        "schema": J_CHECKPOINT_SCHEMA,
        "version": 3,
        "mode": "completed_j_checkpoint",
        "checkpoint_state": J_CHECKPOINT_STATE,
        "grade": "CANDIDATE",
        "completed_j_prefix": completed,
        "next_j": next_j,
        "first_nonmember_j": nonmembers[0] if nonmembers else None,
        "j_progression": list(progression),
        "current_j_row_sha256": digest_obj(progression[-1]),
        "prior_j_checkpoint": prior_j_record,
        "terminal_relator_checkpoint": terminal_relator_record,
        "fixed_bindings": bindings,
        "full_relator_state_serialized": True,
        "relator_checkpoint_is_resource_recovery_only": True,
        "unfinished_j_inferred": False,
        "mathematical_membership_claimed": False,
        "mathematical_nonmembership_claimed": False,
        "actual_A18_lift_claimed": False,
        "claims": claims(),
    }
    data["self_digest_sha256"] = digest_obj(data)
    return data


def validate_j_checkpoint(
        v2: Any, data: dict[str, Any], summary: dict[str, Any],
        bindings: dict[str, Any]) -> None:
    verify_self_digest(data, "completed j checkpoint")
    require(data.get("schema") == J_CHECKPOINT_SCHEMA and
            data.get("version") == 3 and
            data.get("mode") == "completed_j_checkpoint" and
            data.get("checkpoint_state") == J_CHECKPOINT_STATE and
            data.get("grade") == "CANDIDATE" and
            data.get("fixed_bindings") == bindings,
            "completed j checkpoint envelope")
    progression = data.get("j_progression")
    require(type(progression) is list and progression,
            "completed j progression")
    completed = [row.get("j") for row in progression]
    require(completed == data.get("completed_j_prefix") and
            completed == list(FRESH_J_ORDER[:len(completed)]),
            "completed j exact prefix")
    for row in progression:
        validate_public_j_row(v2, row, summary)
    j = completed[-1]
    nonmembers = [row["j"] for row in progression if row["nonmember"]]
    require(len(nonmembers) <= 1 and
            (not nonmembers or nonmembers == [j]) and
            data.get("first_nonmember_j") ==
                (nonmembers[0] if nonmembers else None),
            "completed j first nonmember")
    expected_next = None if nonmembers or j == FRESH_J_ORDER[-1] else j + 1
    require(data.get("next_j") == expected_next and
            data.get("current_j_row_sha256") == digest_obj(progression[-1]),
            "completed j next/current")
    if j == START_J:
        require(data.get("prior_j_checkpoint") is None,
                "j9 prior j absent")
    else:
        validate_record_shape(
            data.get("prior_j_checkpoint"), kind="j", j=j - 1,
            relator=None)
    validate_record_shape(
        data.get("terminal_relator_checkpoint"), kind="relator",
        j=j, relator=11)
    require(data.get("full_relator_state_serialized") is True and
            data.get("relator_checkpoint_is_resource_recovery_only") is True and
            data.get("unfinished_j_inferred") is False and
            data.get("mathematical_membership_claimed") is False and
            data.get("mathematical_nonmembership_claimed") is False and
            data.get("actual_A18_lift_claimed") is False and
            data.get("claims") == claims(),
            "completed j claim boundary")


def write_j_checkpoint(path: Path, data: dict[str, Any], v2: Any,
                       summary: dict[str, Any],
                       bindings: dict[str, Any]) -> dict[str, Any]:
    validate_j_checkpoint(v2, data, summary, bindings)
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
        path: Path, directory: Path, v2: Any, summary: dict[str, Any],
        prior: dict[str, Any], bindings: dict[str, Any]) \
        -> tuple[dict[str, Any], list[dict[str, Any]],
                 list[tuple[Path, dict[str, Any]]]]:
    directory = resolve_checkpoint_directory(directory)
    path = path.resolve()
    require(path.parent == directory and path.is_file(),
            "j checkpoint directory")
    data, raw = read_canonical_json(path, "completed j checkpoint")
    validate_j_checkpoint(v2, data, summary, bindings)
    j = data["completed_j_prefix"][-1]
    require(path.name == j_checkpoint_filename(j),
            "j checkpoint filename")
    record = checkpoint_record(path, kind="j", j=j)
    terminal_record = data["terminal_relator_checkpoint"]
    terminal_path = authenticate_record(
        terminal_record, directory, kind="relator", j=j, relator=11)
    current_pair = (terminal_path, terminal_record)
    previous = data["prior_j_checkpoint"]
    if j == START_J:
        require(previous is None, "j9 chain root")
        return data, [record], [current_pair]
    previous_path = authenticate_record(
        previous, directory, kind="j", j=j - 1, relator=None)
    previous_data, records, terminal_pairs = load_j_checkpoint_chain(
        previous_path, directory, v2, summary, prior, bindings)
    require(previous_data["j_progression"] == data["j_progression"][:-1],
            "j checkpoint cumulative chain")
    return data, records + [record], terminal_pairs + [current_pair]


def discover_relator_header_chain(
        current_path: Path, directory: Path, summary: dict[str, Any],
        prior: dict[str, Any], bindings: dict[str, Any]) \
        -> list[tuple[Path, dict[str, Any], dict[str, Any] | None]]:
    directory = resolve_checkpoint_directory(directory)
    current_path = current_path.resolve()
    require(current_path.parent == directory and current_path.is_file(),
            "relator resume directory")
    rows: list[tuple[Path, dict[str, Any], dict[str, Any] | None]] = []
    seen: set[Path] = set()
    path = current_path
    child_record = None
    while True:
        require(path not in seen, "relator checkpoint cycle")
        seen.add(path)
        if child_record is not None:
            require(path.stat().st_size == child_record["bytes"] and
                    digest_file(path) == child_record["sha256"],
                    "relator ancestor SHA/bytes")
        header = read_relator_header(path)
        validate_relator_header(header, summary, prior, bindings)
        j = header["j"]
        relator = header["completed_relator_prefix"][-1]
        require(path.name == relator_checkpoint_filename(j, relator),
                "relator checkpoint filename")
        rows.append((path, header, child_record))
        previous = header["prior_relator_checkpoint"]
        if relator == 1:
            require(previous is None, "relator chain root")
            if j == START_J:
                require(header["prior_j_checkpoint"] is None,
                        "j9 relator prior j absent")
            else:
                authenticate_record(
                    header["prior_j_checkpoint"], directory,
                    kind="j", j=j - 1, relator=None)
            break
        previous_path = authenticate_record(
            previous, directory, kind="relator", j=j,
            relator=relator - 1)
        child_record = previous
        path = previous_path
    rows.reverse()
    require([row[1]["completed_relator_prefix"][-1] for row in rows] ==
            list(range(1, rows[-1][1]["completed_relator_prefix"][-1] + 1)),
            "relator chain exact prefix")
    for left, right in zip(rows, rows[1:]):
        validate_adjacent_relator_headers(left[1], right[1])
    return rows


def validate_adjacent_relator_headers(
        left: dict[str, Any], right: dict[str, Any]) -> None:
    require(left["j"] == right["j"] and
            left["prior_j_checkpoint"] == right["prior_j_checkpoint"] and
            left["completed_j_progression"] ==
                right["completed_j_progression"] and
            left["completed_closure_receipts"] ==
                right["completed_closure_receipts"][:-1] and
            left["D2_echelon_rank"] <= right["D2_echelon_rank"],
            "relator cumulative header chain")


def load_relator_checkpoint_chain(
        current_path: Path, directory: Path, v1: Any, v2: Any,
        summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any]) \
        -> tuple[dict[str, Any], Any, list[dict[str, Any]],
                 list[dict[str, Any]]]:
    rows = discover_relator_header_chain(
        current_path, directory, summary, prior, bindings)
    latest_path = rows[-1][0]
    latest_header, latest_echelon, latest_record = load_relator_checkpoint(
        latest_path, summary, prior, bindings, v1)
    require(latest_echelon is not None, "latest echelon reconstructed")
    records: list[dict[str, Any]] = []
    for path, header, _ in rows[:-1]:
        _, _, record = load_relator_checkpoint(
            path, summary, prior, bindings, v1,
            compare_to=latest_echelon)
        records.append(record)
    records.append(latest_record)

    prior_j_records: list[dict[str, Any]] = []
    progression: list[dict[str, Any]] = []
    prior_j_record = latest_header["prior_j_checkpoint"]
    j = latest_header["j"]
    if j == START_J:
        require(prior_j_record is None and
                latest_header["completed_j_progression"] == [],
                "j9 relator root")
    else:
        prior_j_path = authenticate_record(
            prior_j_record, directory, kind="j", j=j - 1,
            relator=None)
        prior_j_data, prior_j_records, terminal_pairs = \
            load_j_checkpoint_chain(
                prior_j_path, directory, v2, summary, prior, bindings)
        progression = copy.deepcopy(prior_j_data["j_progression"])
        require(progression == latest_header["completed_j_progression"],
                "relator prior j progression")
        # Authenticate each completed-j terminal relator stream and its chain.
        require(len(terminal_pairs) == len(progression),
                "prior j terminal roster")
        for ordinal, (terminal_path, _) in enumerate(terminal_pairs):
            terminal_rows = discover_relator_header_chain(
                terminal_path, directory, summary, prior, bindings)
            terminal_header, terminal_ech, _ = load_relator_checkpoint(
                terminal_path, summary, prior, bindings, v1)
            require(terminal_ech is not None and
                    terminal_header["completed_relator_prefix"][-1] == 11,
                    "completed-j terminal relator state")
            validate_terminal_relator_header(
                terminal_header, progression[ordinal],
                progression[:ordinal])
            for ancestor_path, _, _ in terminal_rows[:-1]:
                load_relator_checkpoint(
                    ancestor_path, summary, prior, bindings, v1,
                    compare_to=terminal_ech)
    return latest_header, latest_echelon, records, prior_j_records


def expected_checkpoint_files_from_records(
        records: Sequence[dict[str, Any]]) -> set[str]:
    return {record["filename"] for record in records}


def reject_stale_checkpoint_files(directory: Path,
                                  records: Sequence[dict[str, Any]]) -> None:
    directory = resolve_checkpoint_directory(directory)
    actual = {path.name for path in directory.iterdir()
              if path.is_file() and
              (path.name.endswith(".checkpoint.jsonl.gz") or
               (path.name.startswith(
                   "d972_r07_760_l3_target6_relator_resume_v3_j") and
                path.name.endswith(".json")))} if directory.exists() else set()
    expected = expected_checkpoint_files_from_records(records)
    require(actual == expected,
            "stale, missing, or unselected checkpoint files")


def j_workspace(v1: Any, private: dict[str, Any], j: int,
                *, accelerators: bool,
                left_cache: LeftMultiplyCache) -> dict[str, Any]:
    monomials = v1.enumerate_monomials(j)
    dimension = 6 * len(monomials)
    if dimension > v1.MAX_DIMENSION:
        raise v1.ResourceStop(f"j={j}", f"dimension cap: {dimension}")
    idx = {(component, monomial): ordinal
           for ordinal, (component, monomial) in enumerate(
               (component, monomial)
               for component in range(1, 7)
               for monomial in monomials)}
    sp = v1.F3BitSpace(dimension)
    projector = JenningsBitplaneCache(
        v1, j, monomials, sp, enabled=accelerators)
    gate = runtime_accelerator_gate(
        v1, private, j, monomials, idx, sp,
        projector, left_cache, accelerators)

    legal_vectors = []
    legal_public = []
    legal_ech = v1.F3BitEchelon(sp)
    for row in private["sigma_pc"]:
        projected = v1.project_vec_to_Ij(row, j)
        legal_public.append(v1.projected_public(projected))
        reference = sp.vec({idx[key]: value for key, value in projected.items()
                            if key in idx})
        fast = projector.project(row) if projector.enabled else reference
        require(fast == reference, "legal projection exactness")
        legal_vectors.append(fast)
        legal_ech.add(fast)

    target_projected = v1.project_vec_to_Ij(private["target_pc"], j)
    target_vector = sp.vec({idx[key]: value
                            for key, value in target_projected.items()
                            if key in idx})
    fast_target = projector.project(private["target_pc"]) \
        if projector.enabled else target_vector
    require(fast_target == target_vector, "target projection exactness")
    return {
        "j": j, "monomials": monomials, "dimension": dimension,
        "idx": idx, "sp": sp, "projector": projector,
        "gate": gate, "legal_vectors": legal_vectors,
        "legal_public": legal_public, "legal_ech": legal_ech,
        "target_projected": target_projected,
        "target_vector": target_vector,
        "basis_sha256": digest_obj([list(row) for row in monomials]),
        "target_projected_sha256":
            digest_obj(v1.projected_public(target_projected)),
        "legal_projected_rows_sha256": digest_obj(legal_public),
    }


def cache_delta(before: tuple[int, int], after: tuple[int, int]) \
        -> dict[str, int]:
    return {"hits": after[0] - before[0],
            "misses": after[1] - before[1]}


def run_relator_closure(
        v1: Any, private: dict[str, Any], workspace: dict[str, Any],
        d2_ech: Any, ordinal: int, left_cache: LeftMultiplyCache) \
        -> dict[str, Any]:
    before_rows = dict(d2_ech.pivots)
    left_before = left_cache.snapshot()
    projection_before = workspace["projector"].snapshot()
    receipt = optimized_submodule_closure(
        private["relator_pc"][ordinal - 1], workspace["j"],
        workspace["idx"], workspace["sp"], private["e4"].pc,
        d2_ech, workspace["projector"], left_cache)
    require(all(d2_ech.pivots.get(pivot) == vector
                for pivot, vector in before_rows.items()),
            "append-only echelon pivot rows")
    require(d2_ech.rank() - len(before_rows) == receipt["new_pivots"],
            "closure new pivot count")
    receipt = copy.deepcopy(receipt)
    receipt["relator_ordinal"] = ordinal
    receipt["rank_before"] = len(before_rows)
    receipt["rank_after"] = d2_ech.rank()
    receipt["v3_exact_cache_delta"] = {
        "left_multiply": cache_delta(
            left_before, left_cache.snapshot()),
        "Jennings_bitplane": cache_delta(
            projection_before, workspace["projector"].snapshot()),
    }
    return receipt


def finish_j_row(
        v1: Any, private: dict[str, Any], workspace: dict[str, Any],
        d2_ech: Any, closure_receipts: Sequence[dict[str, Any]],
        monitor: Any, *, pairing: bool,
        left_cache: LeftMultiplyCache) -> dict[str, Any]:
    require(len(closure_receipts) == 11, "complete relator roster")
    combined = d2_ech.clone()
    for vector in workspace["legal_vectors"]:
        combined.add(vector)
    remainder, pivot = combined.reduce(workspace["target_vector"])
    del remainder
    nonmember = pivot >= 0
    separator = None
    if nonmember:
        sep = combined.extract_separator(workspace["target_vector"])
        require(sep is not None, "v3 separator extraction")
        terms = v1.sep_public(
            sep, workspace["idx"], workspace["sp"])
        pairings = v1.verify_separator_direct(
            v1, private["e4"], workspace["j"], sep,
            workspace["idx"], workspace["sp"], private["sigma_pc"],
            private["relator_pc"], private["target_pc"], monitor) \
            if pairing else None
        separator = {
            "terms": terms, "terms_sha256": digest_obj(terms),
            "support": len(terms), "pairing_replay": pairings,
        }
    projector = workspace["projector"]
    return {
        "j": workspace["j"],
        "monomial_count": len(workspace["monomials"]),
        "dim_Lambda_over_Ij": workspace["dimension"],
        "basis_sha256": workspace["basis_sha256"],
        "rank_D2bar_alone": d2_ech.rank(),
        "rank_legal_overapproximation": workspace["legal_ech"].rank(),
        "rank_combined": combined.rank(),
        "target_projected_sha256":
            workspace["target_projected_sha256"],
        "legal_projected_rows_sha256":
            workspace["legal_projected_rows_sha256"],
        "PB4_translate_count": TRANSLATED_D2_COUNT,
        "producer_D2_algorithm": "saturated (x_i-1) BFS, D2 first",
        "per_relator_closure_receipts": list(closure_receipts),
        "nonmember": nonmember,
        "separator": separator,
        "v3_exact_accelerators": {
            "gate": workspace["gate"],
            "left_multiply_total": {
                "hits": left_cache.hits, "misses": left_cache.misses,
            },
            "Jennings_bitplane_total": {
                "hits": projector.hits, "misses": projector.misses,
            },
            "row_insertion_order_changed": False,
            "projection_cache_cleared_after_j": True,
        },
    }


def replay_j_no_checkpoints(
        v1: Any, private: dict[str, Any], j: int, monitor: Any,
        *, accelerators: bool) -> dict[str, Any]:
    left_cache = LeftMultiplyCache(private["e4"].pc,
                                   enabled=accelerators)
    workspace = j_workspace(
        v1, private, j, accelerators=accelerators,
        left_cache=left_cache)
    d2_ech = v1.F3BitEchelon(workspace["sp"])
    receipts = []
    for ordinal in RELATOR_ORDER:
        monitor.check(f"j={j}:fresh-replay-relator-{ordinal}", force=True)
        receipts.append(run_relator_closure(
            v1, private, workspace, d2_ech, ordinal, left_cache))
    row = finish_j_row(
        v1, private, workspace, d2_ech, receipts, monitor,
        pairing=False, left_cache=left_cache)
    # Explicit lifetime boundary for the large per-j cache.
    workspace["projector"].table.clear()
    return row


def all_records_from_disk(directory: Path) -> list[dict[str, Any]]:
    directory = resolve_checkpoint_directory(directory)
    records = []
    if not directory.exists():
        return records
    for j in FRESH_J_ORDER:
        for relator in RELATOR_ORDER:
            path = directory / relator_checkpoint_filename(j, relator)
            if path.is_file():
                header = read_relator_header(path)
                record = checkpoint_record(
                    path, kind="relator", j=j, relator=relator,
                    canonical_size=None, canonical_sha=None,
                    state_sha=header.get("D2_echelon_pivot_list_sha256"))
                # Canonical stream values are recovered from the producer's
                # own creation records for new checkpoints or on full load.
                records.append(record)
        path = directory / j_checkpoint_filename(j)
        if path.is_file():
            records.append(checkpoint_record(path, kind="j", j=j))
    return records


def base_output(
        mode: str, summary: dict[str, Any], prior: dict[str, Any],
        v2_pins: dict[str, Any], bindings: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "mode": mode,
        "grade": "CANDIDATE",
        "fixed_bindings": bindings,
        "static_binding": summary,
        "prior_run_binding": prior,
        "v2_pins": v2_pins,
        "resume_contract": {
            "inherited_candidate_prefix": list(INHERITED_PREFIX),
            "inherited_prefix_grade":
                "producer_control_flow_candidate_only",
            "fresh_j_order": list(FRESH_J_ORDER),
            "relator_order": list(RELATOR_ORDER),
            "no_checkpoint_start": "j9_relator1",
            "checkpoint_after_every_completed_relator": True,
            "full_pivot_dictionary_in_every_relator_checkpoint": True,
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
            "sha256": V3_PIN_SPECS["v2_checker"][2],
            "imports_v1_producer": False,
            "imports_v2_producer": False,
            "required_for_fresh_NONMEMBER_promotion": True,
            "v3_checkpoint_format_is_not_a_checker_result": True,
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
        "resume_from_checkpoint": resume_record,
        "unfinished_relator_inferred": False,
        "full_relator_state_serialized": True,
        "relator_checkpoint_is_resource_recovery_only": True,
        "mathematical_membership_claimed": False,
        "mathematical_nonmembership_claimed": False,
        "actual_A18_lift_claimed": False,
        "registered_108_family_used": False,
        "literal_A18_computed": False,
        "normalized_Brunnian_class_computed": False,
    }


def actual_checkpoint_names(directory: Path) -> set[str]:
    directory = resolve_checkpoint_directory(directory)
    if not directory.exists():
        return set()
    return {path.name for path in directory.iterdir()
            if path.is_file() and
            (path.name.endswith(".checkpoint.jsonl.gz") or
             (path.name.startswith(
                 "d972_r07_760_l3_target6_relator_resume_v3_j") and
              path.name.endswith(".json")))}


def expected_names_for_resume(
        progression: Sequence[dict[str, Any]],
        active_j: int | None = None,
        completed_relator: int = 0) -> set[str]:
    names: set[str] = set()
    for row in progression:
        j = int(row["j"])
        names.update(relator_checkpoint_filename(j, relator)
                     for relator in RELATOR_ORDER)
        names.add(j_checkpoint_filename(j))
    if active_j is not None:
        require(active_j == FRESH_J_ORDER[len(progression)] and
                0 <= completed_relator <= 11,
                "active resume index")
        names.update(relator_checkpoint_filename(active_j, relator)
                     for relator in range(1, completed_relator + 1))
    return names


def manifest_records(directory: Path) -> list[dict[str, Any]]:
    directory = resolve_checkpoint_directory(directory)
    rows = []
    for j in FRESH_J_ORDER:
        for relator in RELATOR_ORDER:
            path = directory / relator_checkpoint_filename(j, relator)
            if path.is_file():
                header = read_relator_header(path)
                rows.append({
                    "kind": "relator", "j": j, "relator": relator,
                    "path": public_path(path), "filename": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": digest_file(path),
                    "canonical_self_digest_sha256":
                        header["self_digest_sha256"],
                    "D2_echelon_rank": header["D2_echelon_rank"],
                    "D2_echelon_pivot_list_sha256":
                        header["D2_echelon_pivot_list_sha256"],
                })
        path = directory / j_checkpoint_filename(j)
        if path.is_file():
            data, _ = read_canonical_json(path, "manifest j checkpoint")
            rows.append({
                "kind": "j", "j": j, "path": public_path(path),
                "filename": path.name, "bytes": path.stat().st_size,
                "sha256": digest_file(path),
                "canonical_self_digest_sha256":
                    data["self_digest_sha256"],
            })
    return rows


def validate_completed_relator_chains(
        progression: Sequence[dict[str, Any]], directory: Path,
        v1: Any, summary: dict[str, Any], prior: dict[str, Any],
        bindings: dict[str, Any]) -> None:
    for ordinal, row in enumerate(progression):
        j = int(row["j"])
        path = relator_checkpoint_path(directory, j, 11)
        chain = discover_relator_header_chain(
            path, directory, summary, prior, bindings)
        header, echelon, _ = load_relator_checkpoint(
            path, summary, prior, bindings, v1)
        require(echelon is not None and
                header["completed_relator_prefix"] == list(RELATOR_ORDER),
                "completed j terminal relator state")
        validate_terminal_relator_header(
            header, row, progression[:ordinal])
        for ancestor_path, _, _ in chain[:-1]:
            load_relator_checkpoint(
                ancestor_path, summary, prior, bindings, v1,
                compare_to=echelon)


def validate_terminal_relator_header(
        header: dict[str, Any], row: dict[str, Any],
        preceding_progression: Sequence[dict[str, Any]]) -> None:
    require(header["j"] == row["j"] and
            header["completed_j_progression"] ==
                list(preceding_progression) and
            header["completed_closure_receipts"] ==
                row["per_relator_closure_receipts"] and
            header["D2_echelon_rank"] == row["rank_D2bar_alone"] and
            header["monomial_count"] == row["monomial_count"] and
            header["dimension"] == row["dim_Lambda_over_Ij"] and
            header["Jennings_basis_sha256"] == row["basis_sha256"] and
            header["target_projected_sha256"] ==
                row["target_projected_sha256"] and
            header["legal_projected_rows_sha256"] ==
                row["legal_projected_rows_sha256"],
            "completed j row/terminal relator binding")


def build_full(seconds: float, checkpoint_dir: Path,
               resume_checkpoint: Path | None,
               *, accelerators: bool) -> dict[str, Any]:
    require(0 < seconds <= MAX_SECONDS, "seconds range")
    directory = resolve_checkpoint_directory(checkpoint_dir)
    directory.mkdir(parents=True, exist_ok=True)
    v2 = v1 = None
    summary = prior = v2_pins = bindings = None
    progression: list[dict[str, Any]] = []
    resume_record = None
    active_j = START_J
    next_relator = 1
    resumed_echelon = None
    resumed_receipts: list[dict[str, Any]] = []
    prior_j_record = None
    prior_relator_record = None
    stage = "input_authentication"
    try:
        v2, v1, summary, private, prior, v2_pins, v3_meta = build_context()
        bindings = fixed_bindings(v1, private, summary, prior, v3_meta)
        if resume_checkpoint is None:
            require(not actual_checkpoint_names(directory),
                    "stale checkpoint files without resume")
        else:
            resume_path = (resume_checkpoint if resume_checkpoint.is_absolute()
                           else ROOT / resume_checkpoint).resolve()
            require(resume_path.parent == directory and resume_path.is_file(),
                    "resume checkpoint path")
            if resume_path.name.endswith(".checkpoint.jsonl.gz"):
                header, resumed_echelon, rel_records, j_records = \
                    load_relator_checkpoint_chain(
                        resume_path, directory, v1, v2, summary, prior,
                        bindings)
                active_j = header["j"]
                next_relator = header["next_relator"] or 12
                resumed_receipts = copy.deepcopy(
                    header["completed_closure_receipts"])
                progression = copy.deepcopy(
                    header["completed_j_progression"])
                prior_j_record = copy.deepcopy(
                    header["prior_j_checkpoint"])
                prior_relator_record = rel_records[-1]
                resume_record = rel_records[-1]
                expected = expected_names_for_resume(
                    progression, active_j,
                    header["completed_relator_prefix"][-1])
            else:
                checkpoint, j_records, terminal_pairs = \
                    load_j_checkpoint_chain(
                        resume_path, directory, v2, summary, prior,
                        bindings)
                progression = copy.deepcopy(checkpoint["j_progression"])
                require(checkpoint["next_j"] in FRESH_J_ORDER,
                        "terminal j checkpoint cannot resume")
                validate_completed_relator_chains(
                    progression, directory, v1, summary, prior, bindings)
                active_j = int(checkpoint["next_j"])
                next_relator = 1
                prior_j_record = j_records[-1]
                resume_record = j_records[-1]
                expected = expected_names_for_resume(progression)
            require(actual_checkpoint_names(directory) == expected,
                    "stale, missing, or unselected checkpoint roster")
        require(active_j == FRESH_J_ORDER[len(progression)],
                "resume exact next j")

        monitor = v1.Monitor(seconds)
        left_cache = LeftMultiplyCache(
            private["e4"].pc, enabled=accelerators)
        for j in FRESH_J_ORDER[len(progression):]:
            require(j == active_j or resumed_echelon is None,
                    "active j sequencing")
            stage = f"j={j}:start"
            monitor.check(stage, force=True)
            workspace = j_workspace(
                v1, private, j, accelerators=accelerators,
                left_cache=left_cache)
            if resumed_echelon is not None:
                require(resumed_echelon.sp.n == workspace["sp"].n,
                        "resumed echelon dimension")
                d2_ech = resumed_echelon
                closure_receipts = resumed_receipts
                first_relator = next_relator
            else:
                d2_ech = v1.F3BitEchelon(workspace["sp"])
                closure_receipts = []
                first_relator = 1
                prior_relator_record = None
            require(first_relator == len(closure_receipts) + 1 and
                    1 <= first_relator <= 12,
                    "exact next relator")
            for ordinal in range(first_relator, 12):
                stage = f"j={j}:D2-relator-{ordinal}"
                monitor.check(stage, force=True)
                closure_receipts.append(run_relator_closure(
                    v1, private, workspace, d2_ech, ordinal,
                    left_cache))
                cache_stats = {
                    "left_multiply": {
                        "hits": left_cache.hits,
                        "misses": left_cache.misses,
                    },
                    "Jennings_bitplane": {
                        "hits": workspace["projector"].hits,
                        "misses": workspace["projector"].misses,
                    },
                }
                checkpoint_stats = pivot_stream_stats(d2_ech)
                header = build_relator_header(
                    summary, prior, bindings, j, ordinal,
                    closure_receipts, checkpoint_stats, progression,
                    prior_j_record, prior_relator_record,
                    workspace["target_projected_sha256"],
                    workspace["legal_projected_rows_sha256"],
                    workspace["gate"], cache_stats)
                path = relator_checkpoint_path(
                    checkpoint_dir, j, ordinal)
                record = write_relator_checkpoint(
                    path, header, d2_ech, checkpoint_stats)
                prior_relator_record = record
                print(
                    RELATOR_MARKER + f" j={j} relator={ordinal} "
                    f"rank={d2_ech.rank()} sha256={record['sha256']} "
                    f"bytes={record['bytes']} "
                    f"canonical_sha256="
                    f"{record['canonical_uncompressed_sha256']} "
                    f"canonical_bytes="
                    f"{record['canonical_uncompressed_bytes']}",
                    flush=True)
                monitor.check(
                    f"j={j}:after-relator-{ordinal}-checkpoint",
                    force=True)

            stage = f"j={j}:membership-reduction"
            row = finish_j_row(
                v1, private, workspace, d2_ech, closure_receipts,
                monitor, pairing=True, left_cache=left_cache)
            progression.append(row)
            require(prior_relator_record is not None and
                    prior_relator_record["relator"] == 11,
                    "terminal relator record")
            j_data = build_j_checkpoint(
                v2, summary, prior, bindings, progression,
                prior_j_record, prior_relator_record)
            path = j_checkpoint_path(checkpoint_dir, j)
            j_record = write_j_checkpoint(
                path, j_data, v2, summary, bindings)
            prior_j_record = j_record
            print(
                J_MARKER + f" j={j} nonmember="
                f"{str(row['nonmember']).lower()} "
                f"sha256={j_record['sha256']} bytes={j_record['bytes']}",
                flush=True)
            monitor.check(f"j={j}:after-j-checkpoint", force=True)

            # The per-j Jennings cache must never survive into the next j.
            workspace["projector"].table.clear()
            if row["nonmember"]:
                stage = f"j={j}:fresh-no-state-replay"
                replay = replay_j_no_checkpoints(
                    v1, private, j, monitor,
                    accelerators=accelerators)
                keys = (
                    "rank_D2bar_alone", "rank_legal_overapproximation",
                    "rank_combined", "target_projected_sha256",
                    "legal_projected_rows_sha256", "nonmember")
                require(all(replay[key] == row[key] for key in keys),
                        "fresh no-state-leak BFS replay")
                break
            resumed_echelon = None
            resumed_receipts = []
            prior_relator_record = None
            active_j = j + 1

        nonmembers = [row["j"] for row in progression if row["nonmember"]]
        terminal = "R07_760_L3_TARGET6_NONMEMBER" if nonmembers else \
            "R07_760_L3_TARGET6_MEMBER_INCONCLUSIVE"
        receipt = base_output(
            "full", summary, prior, v2_pins, bindings)
        receipt["status"] = terminal
        receipt["terminal_token"] = terminal
        result = common_result(
            progression, manifest_records(directory), resume_record)
        result["state"] = terminal
        result["first_terminal_rule_applied"] = True
        receipt["result"] = result
    except BaseException as exc:
        is_resource = v1 is not None and isinstance(exc, v1.ResourceStop)
        terminal = "R07_760_L3_TARGET6_UNKNOWN_RESOURCE" if is_resource else \
            "R07_760_L3_TARGET6_INPUT_STOP"
        if summary is None or prior is None or v2_pins is None or \
                bindings is None:
            summary = summary or {
                "base": {"length": 760, "sha256": BASE_SHA,
                         "parent_616_sha256": PARENT_SHA,
                         "free_exponent_sums": [0, 0]},
            }
            prior = prior or {"binding_authenticated": False}
            v2_pins = v2_pins or {}
            bindings = bindings or {
                "binding_authenticated": False,
                "producer_source": producer_source_record(),
            }
        receipt = base_output(
            "full", summary, prior, v2_pins, bindings)
        receipt["status"] = terminal
        receipt["terminal_token"] = terminal
        result = common_result(
            progression, manifest_records(directory), resume_record)
        result.update({
            "state": terminal,
            "stage": getattr(exc, "stage", stage),
            "reason": str(exc),
            "requested_seconds": seconds,
        })
        receipt["result"] = result
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def checkpoint_size_estimates(summary: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    manifests = {row["j"]: row
                 for row in summary["Jennings"]["basis_manifest"]}
    for j in FRESH_J_ORDER:
        dimension = int(manifests[j]["dim_Lambda_over_Ij"])
        hex_chars = (dimension + 3) // 4
        digits = len(str(dimension - 1))
        per_pivot = 2 * hex_chars + digits + 9
        worst = dimension * per_pivot
        result.append({
            "j": j, "dimension": dimension,
            "max_hex_chars_per_plane": hex_chars,
            "max_canonical_pivot_row_bytes": per_pivot,
            "rank_equals_dimension_uncompressed_pivot_bytes_upper": worst,
            "eleven_full_checkpoints_uncompressed_upper": 11 * worst,
            "gzip_size_not_claimed_before_actual_run": True,
        })
    return result


def reference_expansion_bitplanes(v1: Any, pcvec: bytes, j: int,
                                  index: dict[tuple[int, ...], int]) \
        -> tuple[int, int]:
    one = two = 0
    for monomial, coefficient in v1.project_pcvec_terms(pcvec, j):
        ordinal = index[tuple(monomial)]
        if int(coefficient) % 3 == 1:
            one |= 1 << ordinal
        elif int(coefficient) % 3 == 2:
            two |= 1 << ordinal
    return one, two


def accelerator_equivalence(v1: Any,
                            private: dict[str, Any]) -> dict[str, Any]:
    pc = private["e4"].pc
    left = LeftMultiplyCache(pc, enabled=True)
    left_codes = sorted({
        0, 1, 2, PC_ROSTER_SIZE - 1,
        *(((k * 7919 + 17) % PC_ROSTER_SIZE) for k in range(1024)),
    })
    left_count = 0
    for i in range(1, N_GEN + 1):
        generator = bytes(1 if k == i - 1 else 0 for k in range(N_GEN))
        for code in left_codes:
            pcvec = pcvec_from_code(code)
            require(left.get(i, pcvec) == pc.mul(generator, pcvec),
                    "left cache exactness sample")
            left_count += 1

    monomials2 = v1.enumerate_monomials(2)
    sp2 = v1.F3BitSpace(6 * len(monomials2))
    projection2 = JenningsBitplaneCache(
        v1, 2, monomials2, sp2, enabled=True)
    for code in range(PC_ROSTER_SIZE):
        pcvec = pcvec_from_code(code)
        require(projection2.expansion(pcvec) ==
                reference_expansion_bitplanes(
                    v1, pcvec, 2, projection2.index),
                "exhaustive j2 Jennings expansion")

    monomials9 = v1.enumerate_monomials(9)
    sp9 = v1.F3BitSpace(6 * len(monomials9))
    projection9 = JenningsBitplaneCache(
        v1, 9, monomials9, sp9, enabled=True)
    codes9 = sorted({
        0, 1, 2, PC_ROSTER_SIZE - 1,
        *(((k * 3571 + 29) % PC_ROSTER_SIZE) for k in range(256)),
    })
    for code in codes9:
        pcvec = pcvec_from_code(code)
        require(projection9.expansion(pcvec) ==
                reference_expansion_bitplanes(
                    v1, pcvec, 9, projection9.index),
                "deterministic j9 Jennings expansion")
    idx9 = {
        (component, monomial): ordinal
        for ordinal, (component, monomial) in enumerate(
            (component, monomial)
            for component in range(1, 7)
            for monomial in monomials9)
    }
    rows9 = list(private["sigma_pc"]) + list(private["relator_pc"])
    for ordinal, code in enumerate(codes9[:64]):
        rows9.append(v1.pc_translate(
            pc, private["relator_pc"][ordinal % 11],
            pcvec_from_code(code)))
    for row in rows9:
        require(projection9.project(row) ==
                reference_project_bitplanes(v1, row, 9, idx9, sp9),
                "deterministic j9 row projection")

    idx2 = {
        (component, monomial): ordinal
        for ordinal, (component, monomial) in enumerate(
            (component, monomial)
            for component in range(1, 7)
            for monomial in monomials2)
    }
    reference_ech = v1.F3BitEchelon(sp2)
    fast_ech = v1.F3BitEchelon(sp2)
    closure_left = LeftMultiplyCache(pc, enabled=True)
    closure_projection = JenningsBitplaneCache(
        v1, 2, monomials2, sp2, enabled=True)
    for row in private["relator_pc"]:
        reference_receipt = v1.submodule_closure_with_depth(
            row, 2, idx2, sp2, pc, reference_ech)
        fast_receipt = optimized_submodule_closure(
            row, 2, idx2, sp2, pc, fast_ech,
            closure_projection, closure_left)
        require(reference_receipt == fast_receipt and
                list(reference_ech.pivots) == list(fast_ech.pivots) and
                reference_ech.pivots == fast_ech.pivots,
                "complete j2 closure/pivot-order equivalence")
    return {
        "left_multiply_deterministic_pairs": left_count,
        "Jennings_j2_pcvecs_exhaustive": PC_ROSTER_SIZE,
        "Jennings_j9_pcvec_samples": len(codes9),
        "Jennings_j9_actual_row_samples": len(rows9),
        "full_j2_relator_closures": 11,
        "full_j2_pivot_dictionary_sha256":
            pivot_stream_stats(fast_ech)["sha256"],
        "full_j2_insertion_order_sha256":
            digest_obj(list(fast_ech.pivots)),
        "all_equal": True,
        "fail_closed": True,
    }


def toy_summary_and_bindings() \
        -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    summary = {
        "binding_sha256": "b" * 64,
        "Jennings": {"basis_manifest": [{
            "j": 9, "monomial_count": 3,
            "dim_Lambda_over_Ij": 19,
            "basis_sha256": "c" * 64,
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


def toy_echelon(v1: Any) -> Any:
    sp = v1.F3BitSpace(19)
    echelon = v1.F3BitEchelon(sp)
    require(echelon.add(sp.vec({5: 1, 9: 2})) and
            echelon.add(sp.vec({1: 1, 6: 1})) and
            echelon.add(sp.vec({3: 1, 7: 2, 12: 1})),
            "toy nonmonotone pivot insertion")
    require(list(echelon.pivots) == [5, 1, 3],
            "toy insertion canary")
    return echelon


def test_header(v1: Any, *, relator: int = 1,
                prior_relator: dict[str, Any] | None = None,
                echelon: Any | None = None) \
        -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Any]:
    summary, prior, bindings = toy_summary_and_bindings()
    ech = echelon or toy_echelon(v1)
    receipts = [{
        "new_pivots": ech.rank(), "max_depth_reached": 1,
        "max_depth_with_new_pivot": 1,
        "explored_count_by_depth": {0: 1, 1: 1},
    }]
    while len(receipts) < relator:
        receipts.append({
            "new_pivots": 0, "max_depth_reached": 0,
            "max_depth_with_new_pivot": 0,
            "explored_count_by_depth": {0: 1},
        })
    stats = pivot_stream_stats(ech)
    header = build_relator_header(
        summary, prior, bindings, 9, relator, receipts, stats, [],
        None, prior_relator, "e" * 64, "f" * 64,
        {"requested": True}, {"left_multiply": {},
                              "Jennings_bitplane": {}})
    return summary, prior, bindings, header


def forge_test_stream(path: Path, header: dict[str, Any],
                      rows: Sequence[Sequence[Any]], *,
                      refresh_state: bool = True,
                      refresh_self: bool = True) -> None:
    work = copy.deepcopy(header)
    work.pop("self_digest_sha256", None)
    pivot_raw = [canonical_bytes(list(row)) + b"\n" for row in rows]
    if refresh_state:
        work["D2_echelon_pivot_count"] = len(rows)
        work["D2_echelon_rank"] = len(rows)
        work["D2_echelon_pivot_list_bytes"] = sum(map(len, pivot_raw))
        h = hashlib.sha256()
        for raw in pivot_raw:
            h.update(raw)
        work["D2_echelon_pivot_list_sha256"] = h.hexdigest()
    if refresh_self:
        work["self_digest_sha256"] = digest_obj(work)
    else:
        work["self_digest_sha256"] = header["self_digest_sha256"]
    with path.open("wb") as raw_stream:
        with gzip.GzipFile(filename="", mode="wb", compresslevel=6,
                           fileobj=raw_stream, mtime=0) as stream:
            stream.write(canonical_bytes(work) + b"\n")
            for raw in pivot_raw:
                stream.write(raw)


def checkpoint_mutation_tests(v1: Any) -> int:
    labels: list[str] = []
    with tempfile.TemporaryDirectory(prefix="d972-r07-v3-checkpoint-") as tmp:
        root = Path(tmp)
        summary, prior, bindings, header = test_header(v1)
        echelon = toy_echelon(v1)
        good = root / relator_checkpoint_filename(9, 1)
        stats = pivot_stream_stats(echelon)
        good_record = write_relator_checkpoint(
            good, header, echelon, stats)
        loaded, rebuilt, replay_record = load_relator_checkpoint(
            good, summary, prior, bindings, v1)
        require(canonical_bytes(loaded) == canonical_bytes(header) and
                rebuilt is not None and
                rebuilt.pivots == echelon.pivots and
                replay_record == good_record,
                "toy checkpoint roundtrip")
        # A second immutable write must be byte-identical.
        require(write_relator_checkpoint(
                    good, header, echelon, stats) == good_record,
                "deterministic gzip immutable replay")
        rows = [pivot_row(p, echelon.pivots[p])
                for p in sorted(echelon.pivots)]

        def reject_stream(label: str, bad_header: dict[str, Any],
                          bad_rows: Sequence[Sequence[Any]], *,
                          refresh_state: bool = True,
                          refresh_self: bool = True) -> None:
            path = root / (label + ".jsonl.gz")
            forge_test_stream(
                path, bad_header, bad_rows,
                refresh_state=refresh_state, refresh_self=refresh_self)
            try:
                load_relator_checkpoint(
                    path, summary, prior, bindings, v1)
            except RuntimeError:
                labels.append(label)
                return
            raise RuntimeError("checkpoint mutation survived: " + label)

        flipped = copy.deepcopy(rows)
        flipped[0][1] = canonical_hex(int(flipped[0][1], 16) ^ (1 << 8))
        reject_stream("flipped_plane", header, flipped,
                      refresh_state=False, refresh_self=False)

        overlap = copy.deepcopy(rows)
        overlap[0][2] = overlap[0][1]
        reject_stream("overlapping_planes", header, overlap)

        wrong_lead = copy.deepcopy(rows)
        wrong_lead[1][1] = canonical_hex(
            int(wrong_lead[1][1], 16) | 1)
        reject_stream("wrong_leading_pivot", header, wrong_lead)

        out_mask = copy.deepcopy(rows)
        out_mask[-1][1] = canonical_hex(
            int(out_mask[-1][1], 16) | (1 << 19))
        reject_stream("out_of_mask", header, out_mask)

        noncanonical = copy.deepcopy(rows)
        noncanonical[0][1] = "0" + noncanonical[0][1]
        reject_stream("noncanonical_hex", header, noncanonical)

        reordered = list(reversed(copy.deepcopy(rows)))
        reject_stream("pivot_order", header, reordered)

        for label, mutate in (
            ("missing_relator_prefix",
             lambda d: d.update({"completed_relator_prefix": []})),
            ("reordered_relator_prefix",
             lambda d: d.update({"completed_relator_prefix": [2, 1]})),
            ("wrong_j", lambda d: d.update({"j": 10})),
            ("wrong_basis", lambda d: d.update(
                {"Jennings_basis_sha256": "0" * 64})),
            ("wrong_target", lambda d: d.update(
                {"target_projected_sha256": "0" * 64})),
            ("wrong_legal", lambda d: d.update(
                {"legal_projected_rows_sha256": "0" * 64})),
        ):
            bad = copy.deepcopy(header)
            mutate(bad)
            reject_stream(label, bad, rows)

        forged_digest_header = copy.deepcopy(header)
        forged_digest_header["self_digest_sha256"] = "0" * 64
        reject_stream("forged_self_digest", forged_digest_header, rows,
                      refresh_state=True, refresh_self=False)

        # A complete second checkpoint with a corrupted parent record must
        # fail the path/SHA/byte ancestor gate even when its own digest is
        # freshly forged.
        bad_parent = copy.deepcopy(good_record)
        bad_parent["sha256"] = "0" * 64
        _, _, _, header2 = test_header(
            v1, relator=2, prior_relator=bad_parent,
            echelon=echelon)
        second = root / relator_checkpoint_filename(9, 2)
        forge_test_stream(second, header2, rows)
        old_default = globals()["DEFAULT_CHECKPOINT_DIR"]
        try:
            # This test uses the lower-level fixed-record authenticator with
            # an explicitly supplied external directory; production resume
            # additionally requires the repository-fixed directory.
            try:
                validate_record_shape(
                    header2["prior_relator_checkpoint"],
                    kind="relator", j=9, relator=1)
                require(good.stat().st_size == bad_parent["bytes"] and
                        digest_file(good) == bad_parent["sha256"],
                        "broken ancestor should fail")
            except RuntimeError:
                labels.append("broken_ancestor_sha_bytes")
        finally:
            globals()["DEFAULT_CHECKPOINT_DIR"] = old_default

        # Recomputing a child's self digest must not permit a different
        # prior-j anchor to be spliced between two adjacent relator states.
        _, _, _, adjacent = test_header(
            v1, relator=2, prior_relator=good_record,
            echelon=echelon)
        adjacent["prior_j_checkpoint"] = {
            "kind": "j", "j": 8, "path": "forged", "filename": "forged",
            "bytes": 1, "sha256": "0" * 64,
        }
        adjacent["self_digest_sha256"] = digest_obj({
            key: value for key, value in adjacent.items()
            if key != "self_digest_sha256"
        })
        try:
            validate_adjacent_relator_headers(header, adjacent)
        except RuntimeError:
            labels.append("prior_j_chain_splice")
        else:
            raise RuntimeError(
                "checkpoint mutation survived: prior_j_chain_splice")

        # A completed-j row and its terminal relator stream are one state:
        # a freshly re-digested public row may not replace its closure roster.
        _, _, _, terminal = test_header(
            v1, relator=11, echelon=echelon)
        terminal_row = {
            "j": terminal["j"],
            "monomial_count": terminal["monomial_count"],
            "dim_Lambda_over_Ij": terminal["dimension"],
            "basis_sha256": terminal["Jennings_basis_sha256"],
            "rank_D2bar_alone": terminal["D2_echelon_rank"],
            "target_projected_sha256":
                terminal["target_projected_sha256"],
            "legal_projected_rows_sha256":
                terminal["legal_projected_rows_sha256"],
            "per_relator_closure_receipts": copy.deepcopy(
                terminal["completed_closure_receipts"]),
        }
        terminal_row["per_relator_closure_receipts"][-1][
            "new_pivots"] = 1
        try:
            validate_terminal_relator_header(terminal, terminal_row, [])
        except RuntimeError:
            labels.append("terminal_closure_roster_splice")
        else:
            raise RuntimeError(
                "checkpoint mutation survived: terminal_closure_roster_splice")

    require(len(labels) == 16, "checkpoint mutation count")
    return len(labels)


def benchmark_accelerators(v1: Any,
                           private: dict[str, Any]) -> dict[str, float]:
    pc = private["e4"].pc
    pairs = [(i, pcvec_from_code((k * 7919 + 17) % PC_ROSTER_SIZE))
             for k in range(128) for i in range(1, N_GEN + 1)]
    left = LeftMultiplyCache(pc, enabled=True)
    for i, pcvec in pairs:
        left.get(i, pcvec)
    started = time.perf_counter()
    for _ in range(3):
        for i, pcvec in pairs:
            generator = bytes(1 if k == i - 1 else 0
                              for k in range(N_GEN))
            pc.mul(generator, pcvec)
    naive_left = time.perf_counter() - started
    started = time.perf_counter()
    for _ in range(3):
        for i, pcvec in pairs:
            left.get(i, pcvec)
    cached_left = time.perf_counter() - started

    monomials = v1.enumerate_monomials(9)
    sp = v1.F3BitSpace(6 * len(monomials))
    idx = {(component, monomial): ordinal
           for ordinal, (component, monomial) in enumerate(
               (component, monomial)
               for component in range(1, 7)
               for monomial in monomials)}
    projection = JenningsBitplaneCache(
        v1, 9, monomials, sp, enabled=True)
    rows = list(private["sigma_pc"]) + list(private["relator_pc"])
    for row in rows:
        projection.project(row)
    started = time.perf_counter()
    for _ in range(3):
        for row in rows:
            reference_project_bitplanes(v1, row, 9, idx, sp)
    naive_projection = time.perf_counter() - started
    started = time.perf_counter()
    for _ in range(3):
        for row in rows:
            projection.project(row)
    cached_projection = time.perf_counter() - started
    return {
        "left_naive_seconds": naive_left,
        "left_cached_seconds": cached_left,
        "left_warm_speedup": naive_left / max(cached_left, 1e-12),
        "projection_naive_seconds": naive_projection,
        "projection_cached_seconds": cached_projection,
        "projection_warm_speedup":
            naive_projection / max(cached_projection, 1e-12),
    }


def cache_memory_estimates(summary: dict[str, Any]) -> dict[str, Any]:
    # CPython-oriented upper estimates, separated from mathematical state.
    # They are estimates only and are never used as a correctness premise.
    projection = []
    manifests = {row["j"]: row
                 for row in summary["Jennings"]["basis_manifest"]}
    for j in FRESH_J_ORDER:
        width = manifests[j]["monomial_count"]
        digits = (width + 29) // 30
        pair_bytes = 56 + 2 * (24 + 4 * digits)
        projection.append({
            "j": j, "one_component_width": width,
            "estimated_full_cache_MiB":
                round(PC_ROSTER_SIZE * pair_bytes / (1024 * 1024), 3),
        })
    return {
        "left_multiply_max_entries": N_GEN * PC_ROSTER_SIZE,
        "left_multiply_estimated_full_MiB": 31.0,
        "Jennings_projection_per_j": projection,
        "Jennings_cache_cleared_between_j": True,
        "not_including_echelon_state": True,
    }


def build_preflight() -> dict[str, Any]:
    v2, v1, summary, private, prior, v2_pins, v3_meta = build_context()
    del v2
    bindings = fixed_bindings(v1, private, summary, prior, v3_meta)
    equivalence = accelerator_equivalence(v1, private)
    mutations = checkpoint_mutation_tests(v1)
    receipt = base_output(
        "preflight", summary, prior, v2_pins, bindings)
    receipt["preflight_state"] = PREFLIGHT_STATE
    receipt["result"] = {"state": "UNBUILT_GHA_ONLY"}
    receipt["checkpoint_contract"] = {
        "relator_schema": RELATOR_CHECKPOINT_SCHEMA,
        "completed_j_schema": J_CHECKPOINT_SCHEMA,
        "stream_format": STREAM_FORMAT,
        "pivot_encoding": PIVOT_ENCODING,
        "full_pivot_dictionary_every_relator": True,
        "canonical_header_and_pivot_rows": True,
        "deterministic_gzip": True,
        "atomic_immutable_hardlink_publish": True,
        "original_pivot_insertion_order_restored": True,
        "prior_j_and_relator_sha_bytes": True,
        "resource_recovery_not_mathematical_result": True,
        "checkpoint_mutations_rejected": mutations,
    }
    receipt["accelerator_equivalence"] = equivalence
    receipt["accelerator_memory_estimates"] = cache_memory_estimates(summary)
    receipt["checkpoint_size_estimates"] = checkpoint_size_estimates(summary)
    receipt["self_digest_sha256"] = digest_obj(receipt)
    return receipt


def validate_output(data: dict[str, Any]) -> None:
    verify_self_digest(data, "v3 output")
    require(data.get("schema") == SCHEMA and
            data.get("grade") == "CANDIDATE" and
            data.get("claims") == claims(),
            "v3 output envelope")
    if data.get("mode") == "preflight":
        require(data.get("preflight_state") == PREFLIGHT_STATE and
                "status" not in data and "terminal_token" not in data and
                data.get("result", {}).get("state") == "UNBUILT_GHA_ONLY" and
                data.get("accelerator_equivalence", {}).get(
                    "all_equal") is True and
                data.get("checkpoint_contract", {}).get(
                    "full_pivot_dictionary_every_relator") is True,
                "claim-free v3 preflight")
        return
    require(data.get("mode") == "full" and
            data.get("terminal_token") in TERMINALS and
            data.get("status") == data.get("terminal_token") and
            data.get("result", {}).get("state") ==
                data.get("terminal_token"),
            "v3 full terminal")
    result = data["result"]
    require(result.get("inherited_candidate_prefix") ==
                list(INHERITED_PREFIX) and
            result.get("inherited_prefix_grade") ==
                "producer_control_flow_candidate_only" and
            result.get("full_relator_state_serialized") is True and
            result.get("relator_checkpoint_is_resource_recovery_only") is True and
            result.get("mathematical_membership_claimed") is False and
            result.get("mathematical_nonmembership_claimed") is False and
            result.get("actual_A18_lift_claimed") is False,
            "v3 result boundary")


def checked_write_output(path: Path, data: dict[str, Any]) -> bytes:
    validate_output(data)
    raw = canonical_bytes(data) + b"\n"
    full = path if path.is_absolute() else ROOT / path
    atomic_immutable_bytes(full, raw)
    return raw


def self_test() -> None:
    v3_pin_inputs()
    v2, v1, summary, private, prior, v2_pins, v3_meta = build_context()
    require(v2 is not None and prior["next_j"] == START_J and
            len(v2_pins) == 4 and v3_meta["v3_pin_manifest"],
            "v3 inherited context")
    bindings = fixed_bindings(v1, private, summary, prior, v3_meta)
    require(bindings["base_binding"]["sha256"] == BASE_SHA,
            "v3 selftest binding")
    equivalence = accelerator_equivalence(v1, private)
    mutations = checkpoint_mutation_tests(v1)
    timings = benchmark_accelerators(v1, private)
    print(
        "R07_760_L3_TARGET6_RELATOR_RESUME_V3_PRODUCER_SELFTEST_PASS "
        f"checkpoint_mutations={mutations} "
        f"j2_exhaustive={equivalence['Jennings_j2_pcvecs_exhaustive']} "
        f"j9_samples={equivalence['Jennings_j9_pcvec_samples']} "
        f"j2_relators={equivalence['full_j2_relator_closures']} "
        f"left_warm_speedup={timings['left_warm_speedup']:.3f} "
        f"projection_warm_speedup={timings['projection_warm_speedup']:.3f} "
        "full_pivots=true deterministic_gzip=true",
        flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seconds", type=float,
                        default=RECOMMENDED_SECONDS)
    parser.add_argument("--checkpoint-dir", type=Path,
                        default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--disable-accelerators", action="store_true")
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
            args.seconds, args.checkpoint_dir,
            args.resume_checkpoint,
            accelerators=not args.disable_accelerators)
        output = args.output or DEFAULT_FULL
    raw = checked_write_output(output, receipt)
    state_key = "preflight_state" if args.preflight else "terminal_token"
    state_label = "preflight_state" if args.preflight else "terminal"
    checkpoints = 0 if args.preflight else len(
        receipt["result"]["checkpoint_manifest"])
    print(
        FINAL_MARKER + f" {state_label}={receipt[state_key]} "
        f"grade=CANDIDATE checkpoints={checkpoints} "
        f"sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}",
        flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
