"""Exact full-D2 dual correlation over the pinned E4 roof (157eg).

The expensive prefix and reverse-pivot functional are reconstructed afresh
through the authenticated 157ed producer.  The correlation itself never
interns an E4 element and never enumerates E4.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import struct
import sys
import tempfile
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

try:
    import resource
except ImportError:  # pragma: no cover - Windows fixture path
    resource = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157eg_b345_full_d2_dual_correlation.md")
TASK_SHA = "22b649c178ea1a821a5d67973b39c58f6a7395b6bc6a407a36a493f9ce19720e"
SCHEMA = "d972-b345-full-d2-dual-correlation/v1"
OUTPUT = Path("ci/out/d972_b345_full_d2_dual_correlation_v1.json")
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"

ED_PRODUCER = Path("search/d972_b345_triple_cube_raw_lambda_census_v1.py")
ED_PRODUCER_SHA = "d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db"
ED_CHECKER = Path("search/check_d972_b345_triple_cube_raw_lambda_census_v1.py")
ED_CHECKER_SHA = "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce"
ED_DRIVER = Path("search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g")
ED_DRIVER_SHA = "29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9"
EE_PRODUCER = Path("search/d972_b345_joint_kernel_qstar_closure_v1.py")
EE_PRODUCER_SHA = "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"
EF_CHECKER = Path("search/check_d972_b345_joint_kernel_qstar_closure_v2.py")
EF_CHECKER_SHA = "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"
EF_DRIVER = Path("search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g")
EF_DRIVER_SHA = "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"
PREFIX_SOURCE = Path("search/d972_b345_seedspan_triple4_v1.py")
PREFIX_SOURCE_SHA = "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"
EE_TASK = Path("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md")
EE_TASK_SHA = "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"
EF_TASK = Path("sol/luna_task_157ef_b345_joint_kernel_checker_repair.md")
EF_TASK_SHA = "e626802b32e9577e35f5543b252830abdc4461b409972c9f5536ea29d8bb14ed"

PIN_SPECS = {
    "task": (TASK, TASK_SHA, 16187),
    "157ee_producer": (EE_PRODUCER, EE_PRODUCER_SHA, 67945),
    "157ef_checker": (EF_CHECKER, EF_CHECKER_SHA, 5942),
    "157ef_driver": (EF_DRIVER, EF_DRIVER_SHA, 3912),
    "157ed_producer": (ED_PRODUCER, ED_PRODUCER_SHA, 126942),
    "157ed_checker": (ED_CHECKER, ED_CHECKER_SHA, 97363),
    "157ed_driver": (ED_DRIVER, ED_DRIVER_SHA, 10223),
    "frozen_prefix_source": (PREFIX_SOURCE, PREFIX_SOURCE_SHA, 535219),
    "157ee_task": (EE_TASK, EE_TASK_SHA, 11226),
    "157ef_task": (EF_TASK, EF_TASK_SHA, 3235),
}

PREFIX_COUNTS = {
    "columns": 362725, "pivots": 362709, "dependent_columns": 16,
    "live_sparse_entries": 3090367, "row_tail_visits": 2727658,
    "BFS_translations": 32768, "directed_translations": 207,
}
PREFIX_POOL_CHECKPOINT = 976408
BASE_SUPPORTS = [8, 6, 8, 6, 4, 8, 12, 6, 4, 8, 6]
BASE_COMPONENTS = [10, 12, 18, 10, 12, 14]
BASE_OCCURRENCE_SHA = "3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d"
PREFIX_STABLE_SHA = "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d"
PREFIX_TRANSLATIONS_SHA = "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f"
PREFIX_COLUMNS_SHA = "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343"
PREFIX_BLOCKERS_SHA = "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53"

CAPS = {
    "pair_attempts": 8_388_608,
    "distinct_correlation_candidates": 2_000_000,
    "packed_active_rows": 2_000_000,
    "common_math_soft_deadline_seconds": 18_000,
    "producer_soft_rss_bytes": 4_831_838_208,
    "packed_receipt_bytes": 268_435_456,
}
TERMINALS = frozenset({
    "B345_E4_FULL_D2_QSTAR_SEPARATOR",
    "B345_E4_FULL_D2_ACTIVE_TRANSLATION",
    "B345_E4_FULL_D2_UNKNOWN_RESOURCE",
    "B345_E4_FULL_D2_UNKNOWN_INPUT",
})
PHASES = frozenset({
    "authenticated_input", "fresh_immutable_prefix", "raw_lambda_oracle",
    "base_columns", "dual_correlation", "section_witness",
    "receipt_serialization", "complete",
})


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True,
        separators=(",", ":")).encode("utf-8"))


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class InputFailure(RuntimeError):
    pass


class CorrelationResource(RuntimeError):
    def __init__(self, key: str, limit: int, observed: int, relation: str,
                 phase: str, current: dict[str, Any],
                 cap_source: str = "local") -> None:
        super().__init__(key)
        require(cap_source == "local" and key in CAPS and CAPS[key] == int(limit),
                "registered correlation resource")
        require(relation in {"gt", "ge"} and phase in PHASES,
                "resource relation/phase")
        self.key = key; self.limit = int(limit); self.observed = int(observed)
        self.relation = relation; self.phase = phase; self.current = current
        self.cap_source = cap_source

    def public(self) -> dict[str, Any]:
        return {"cap_reason": self.key, "cap_key": self.key,
                "cap_source": self.cap_source,
                "cap_limit": self.limit, "observed_count": self.observed,
                "comparator": self.relation, "phase": self.phase,
                "current": self.current}


def current_rss() -> int:
    try:
        with open("/proc/self/status", "r", encoding="ascii") as stream:
            for line in stream:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    if resource is None:
        return 0
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


class Monitor:
    def __init__(self, seconds: float = 18_000.0) -> None:
        require(0 < seconds <= CAPS["common_math_soft_deadline_seconds"],
                "common producer deadline")
        self.started = time.monotonic(); self.deadline = self.started + seconds
        self.initial_seconds = float(seconds); self.checks = 0
        self.peak_rss_bytes = 0; self.hit_reason: str | None = None

    def check(self, phase: str, *, force: bool = False, **_: Any) -> None:
        require(phase in PHASES or phase == "raw_lambda_reverse_dp" or
                phase.startswith("strong_wform_") or
                phase.startswith("affine_") or phase.startswith("proof_DAG_"),
                "monitor phase registry")
        self.checks += 1
        if not force and self.checks & 63:
            return
        rss = current_rss(); self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
        if rss >= CAPS["producer_soft_rss_bytes"]:
            self.hit_reason = "producer_soft_rss_bytes"
            raise CorrelationResource(self.hit_reason, CAPS[self.hit_reason],
                rss, "ge", _outer_phase(phase), {})
        if time.monotonic() >= self.deadline:
            self.hit_reason = "common_math_soft_deadline_seconds"
            elapsed = max(CAPS[self.hit_reason], int(time.monotonic()-self.started))
            raise CorrelationResource(self.hit_reason, CAPS[self.hit_reason],
                elapsed, "ge", _outer_phase(phase), {})

    def reserve(self, phase: str, additional_bytes: int) -> None:
        require(isinstance(additional_bytes, int) and additional_bytes >= 0,
                "RSS reservation")
        rss = current_rss(); self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
        attempted = rss + additional_bytes
        if attempted >= CAPS["producer_soft_rss_bytes"]:
            self.hit_reason = "producer_soft_rss_bytes"
            raise CorrelationResource(self.hit_reason, CAPS[self.hit_reason],
                attempted, "ge", _outer_phase(phase), {})
        self.check(phase, force=True)

    def public(self) -> dict[str, Any]:
        return {"initial_remaining_seconds": self.initial_seconds,
                "elapsed_seconds": time.monotonic()-self.started,
                "remaining_seconds": max(0.0, self.deadline-time.monotonic()),
                "checks": self.checks, "peak_rss_bytes": self.peak_rss_bytes,
                "hit_reason": self.hit_reason}


def _outer_phase(phase: str) -> str:
    if phase.startswith("strong_wform_") or phase.startswith("affine_"):
        return "fresh_immutable_prefix"
    if phase == "raw_lambda_reverse_dp":
        return "raw_lambda_oracle"
    if phase.startswith("proof_DAG_"):
        return "section_witness"
    return phase if phase in PHASES else "fresh_immutable_prefix"


def pin_rows() -> dict[str, dict[str, Any]]:
    return {label: {"path": path.as_posix(), "sha256": digest,
                    "bytes": size}
            for label, (path, digest, size) in PIN_SPECS.items()} | {
        "q3_artifact": {"path": Q3_PATH.as_posix(), "sha256": Q3_SHA,
                        "bytes": ((ROOT/Q3_PATH).stat().st_size
                                  if (ROOT/Q3_PATH).is_file() else None)}}


def authenticate_static() -> None:
    for label, (path, digest, size) in PIN_SPECS.items():
        full = ROOT / path
        if not full.is_file() or full.stat().st_size != size or sha_file(full) != digest:
            raise InputFailure(f"authenticated pin drift: {label}")


def load_ed() -> Any:
    authenticate_static()
    spec = importlib.util.spec_from_file_location(
        "_d972_157eg_pinned_157ed_producer", ROOT / ED_PRODUCER)
    if spec is None or spec.loader is None:
        raise InputFailure("157ed producer module spec")
    require(spec.name not in sys.modules, "157ed producer module name fresh")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


def upstream_caps(ed: Any) -> dict[str, int]:
    rows = {key:int(value) for key,value in ed.UPSTREAM_RESOURCE_CAPS.items()}
    for key in ("raw_lambda_recursion_edges",):
        require(key in ed.CAPS and isinstance(ed.CAPS[key],int),
                "reachable 157ed resource cap")
        if key in rows:require(rows[key]==int(ed.CAPS[key]),
                               "upstream cap overlap")
        rows[key]=int(ed.CAPS[key])
    return dict(sorted(rows.items()))


def convert_upstream(exc: Any, ed: Any, phase: str,
                     current: dict[str, Any]) -> CorrelationResource:
    caps = upstream_caps(ed)
    key = str(getattr(exc, "cap_key", "")); reason = str(getattr(exc, "reason", ""))
    limit = int(getattr(exc, "cap_limit", -1)); observed = int(getattr(exc, "observed_count", -1))
    relation = str(getattr(exc, "trigger_relation", "gt"))
    require(key in caps and caps[key] == limit and reason == key,
            "closed upstream resource registry")
    # Preserve the real cap in the public upstream registry; use a local
    # wrapper whose constructor only accepts this lane's caps by bypassing it.
    stop = object.__new__(CorrelationResource)
    RuntimeError.__init__(stop, key)
    stop.key = key; stop.limit = limit; stop.observed = observed
    stop.relation = relation; stop.phase = phase; stop.current = current
    stop.cap_source = "upstream"
    return stop


def blob(value: Any) -> bytes:
    return bytes(value[0]) + bytes(value[1])


def uncached_ops(old: Any, quotient: Any) -> tuple[Callable[[Any, Any], Any],
                                                   Callable[[Any], Any]]:
    def mul(left: Any, right: Any) -> Any:
        pc = quotient.pc.collect_uncached(
            old.coords_word(left[1]) + old.coords_word(right[1]))
        return old.perm_mul(left[0], right[0]), pc

    def inverse(value: Any) -> Any:
        word: list[int] = []
        for i in range(quotient.pc.n, 0, -1):
            for _ in range(value[1][i-1]):
                word.extend(old.coords_word(quotient.pc.inverses[i-1]))
        return old.perm_inv(value[0]), quotient.pc.collect_uncached(word)
    return mul, inverse


def correlation_packed(rows: Iterable[tuple[bytes, int, int]], width: int) -> bytes:
    out = bytearray()
    for translation, relator, scalar in rows:
        require(len(translation) == width and 1 <= relator <= 11 and
                scalar in (1, 2), "packed active row")
        out.extend(translation); out.append(relator); out.append(scalar)
    return bytes(out)


def translation_from_pair(g: Any, h: Any, *, mul: Callable[[Any, Any], Any],
                          inverse: Callable[[Any], Any],
                          orientation: str = "g_times_h_inverse",
                          inverse_h: Any | None = None) -> Any:
    """Shared construction and the load-bearing left-action gate."""
    require(orientation in {"g_times_h_inverse", "h_inverse_times_g",
                            "g_inverse_times_h", "right_action_solution"},
            "translation orientation registry")
    hinv = inverse(h) if inverse_h is None else inverse_h
    if orientation == "g_times_h_inverse":
        answer = mul(g, hinv)
    elif orientation == "h_inverse_times_g":
        answer = mul(hinv, g)
    elif orientation == "g_inverse_times_h":
        answer = mul(inverse(g), h)
    else:
        # Deliberately use the opposite/right-oriented construction.  It is
        # still subjected to the production left-action gate t*h=g below.
        answer = mul(h, inverse(g))
    require(mul(answer, h) == g, "left translation t*h=g")
    return answer


def lambda_support(oracle: Any, width: int) -> dict[str, Any]:
    rows = [[int(component), value.hex(), int(coefficient)]
            for (component, value), coefficient in oracle.values.items()
            if int(coefficient) % 3]
    rows.sort(key=lambda row: (row[0], bytes.fromhex(row[1])))
    require(all(1 <= r[0] <= 6 and len(bytes.fromhex(r[1])) == width and
                r[2] in (1, 2) for r in rows), "lambda support shape")
    per = [sum(row[0] == c for row in rows) for c in range(1, 7)]
    return {"rows": rows, "count": len(rows), "per_component": per,
            "ordered_sha256": sha_obj(rows),
            "order": "component then canonical E4 bytes",
            "zero_entries_covered_by_oracle_semantic_digest": True}


def rebuild_base_bundle(old: Any, prefix: dict[str, Any], e4: Any) \
        -> dict[str, Any]:
    require(set(prefix) == {"pool", "sections", "dag", "basis", "model4",
                            "raw_source_tuple", "base_source_key",
                            "directed_base_support", "directed_surgery",
                            "accounting", "157ed_dependent_events",
                            "157ed_prefix_bindings"},
            "fresh prefix private/public shape")
    roots_before = dict(prefix["sections"].base_prefix_roots)
    occurrences = old.freeze_base_support_occurrences(
        prefix["model4"], prefix["pool"], prefix["sections"])
    require(prefix["sections"].base_prefix_roots == roots_before,
            "second base-support freeze reuses canonical roots")
    public = old.public_base_occurrences(occurrences)
    claimed = prefix["directed_base_support"]
    expected_claim = {"occurrences": public,
        "occurrence_count": len(public), "ordered_sha256": old.digest_obj(public),
        "order": "relator index, component, canonical E4 bytes",
        "all_prefix_sections_directly_replayed": True}
    require(claimed == expected_claim and "base_occurrences" not in prefix,
            "fresh prefix public/private occurrence projection")
    per_rel = [sum(r["relator_index"] == j for r in occurrences)
               for j in range(1, 12)]
    per_comp = [sum(r["component"] == c for r in occurrences)
                for c in range(1, 7)]
    require(len(occurrences) == 76 and per_rel == BASE_SUPPORTS and
            per_comp == BASE_COMPONENTS and old.digest_obj(public) ==
            BASE_OCCURRENCE_SHA and prefix["model4"]["D1D2_zero"] is True,
            "base D2 ledger")
    return {"private_occurrences": occurrences, "public": {
        "occurrences": public, "occurrence_count": 76,
        "per_relator_counts": per_rel, "per_component_counts": per_comp,
        "ordered_sha256": BASE_OCCURRENCE_SHA,
        "quotient_identity_all": True, "D1_D2_zero_all": True,
        "private_fields_published": False,
        "order": "relator index, component, canonical E4 bytes"}}


def state_snapshot(prefix: dict[str, Any]) -> dict[str, Any]:
    pool, basis, dag, sections = (prefix[k] for k in
                                  ("pool", "basis", "dag", "sections"))
    h = hashlib.sha256()
    for index, value in enumerate(pool.values):
        require(pool.ids.get(value) == index, "pool ID order integrity")
        h.update(value)
    return {"pool_size": len(pool.values), "pool_ids": len(pool.ids),
        "pool_order_sha256": h.hexdigest(), "pool_object_id": id(pool.values),
        "basis_pivots": len(basis.rows),
        "basis_live_sparse_entries": basis.live_vector_entries,
        "basis_columns": basis.columns_seen, "basis_object_id": id(basis.rows),
        "DAG_nodes": dag.node_count, "DAG_edges": dag.edge_count,
        "DAG_object_id": id(dag), "section_bindings": len(sections.by_blob),
        "section_expression_nodes": len(sections.expressions.kind),
        "section_expression_edges": sections.expressions.edge_count,
        "section_object_id": id(sections)}


def public_snapshot(row: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if not k.endswith("_object_id")}


def exact_correlation(support_rows: Sequence[Sequence[Any]],
                      occurrences: Sequence[dict[str, Any]], *, width: int,
                      unpack: Callable[[bytes], Any], mul: Callable[[Any, Any], Any],
                      inverse: Callable[[Any], Any], pack: Callable[[Any], bytes],
                      monitor: Any | None, caps: dict[str, int] | None = None) \
        -> dict[str, Any]:
    """Production correlation helper.  It has no pool/basis/DAG argument."""
    limits = CAPS if caps is None else caps
    required = {"pair_attempts", "distinct_correlation_candidates",
                "packed_active_rows"}
    require(set(limits) >= required, "correlation cap shape")
    by_component: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in occurrences:
        require(set(row) >= {"relator_index", "component", "coefficient",
                            "element_hex", "_value"},
                "private base occurrence shape")
        by_component[int(row["component"])].append(row)
    inverse_h = {bytes.fromhex(row["element_hex"]): inverse(row["_value"])
                 for row in occurrences}
    corr: dict[tuple[int, bytes], int] = {}
    attempts = 0; tick_count = 0
    for s_ord, (component0, g_hex0, lam0) in enumerate(support_rows, 1):
        component, g_hex, lam = int(component0), str(g_hex0), int(lam0)
        g_blob = bytes.fromhex(g_hex); require(len(g_blob) == width,
                                               "lambda blob width")
        g = unpack(g_blob)
        for b_ord, row in enumerate(by_component[component], 1):
            if attempts >= limits["pair_attempts"]:
                raise CorrelationResource("pair_attempts", limits["pair_attempts"],
                    attempts + 1, "gt", "dual_correlation",
                    {"lambda_ordinal": s_ord, "base_component_ordinal": b_ord})
            attempts += 1
            t = translation_from_pair(g, row["_value"], mul=mul,
                inverse=inverse, orientation="g_times_h_inverse",
                inverse_h=inverse_h[bytes.fromhex(row["element_hex"])])
            t_blob = pack(t); require(len(t_blob) == width, "translation width")
            key = (int(row["relator_index"]), t_blob)
            if key not in corr and len(corr) >= limits[
                    "distinct_correlation_candidates"]:
                raise CorrelationResource("distinct_correlation_candidates",
                    limits["distinct_correlation_candidates"], len(corr)+1,
                    "gt", "dual_correlation",
                    {"lambda_ordinal": s_ord, "base_component_ordinal": b_ord})
            corr[key] = (corr.get(key, 0) + int(row["coefficient"])*lam) % 3
            tick_count += 1
            if monitor is not None and tick_count & 4095 == 0:
                monitor.check("dual_correlation")
    expected_attempts = sum(
        sum(int(r[0]) == c for r in support_rows) * len(by_component[c])
        for c in range(1, 7))
    require(attempts == expected_attempts, "pair-attempt formula")
    ordered_keys = sorted(corr, key=lambda key: (key[1], key[0]))
    active = [(translation, relator, corr[(relator, translation)])
              for relator, translation in ordered_keys
              if corr[(relator, translation)] != 0]
    if len(active) > limits["packed_active_rows"]:
        raise CorrelationResource("packed_active_rows",
            limits["packed_active_rows"], len(active), "gt",
            "dual_correlation", {"post_accumulation": True})
    encoded = correlation_packed(active, width)
    first = None if not active else {
        "translation_hex": active[0][0].hex(), "relator_index": active[0][1],
        "scalar": active[0][2]}
    zero_keys = [(relator, translation) for relator, translation in ordered_keys
                 if corr[(relator, translation)] == 0]
    # Exact first contributing pair, recovered after canonical first-active
    # selection so no per-candidate provenance table is retained.
    contributor = None
    if first is not None:
        target = (int(first["relator_index"]),
                  bytes.fromhex(first["translation_hex"]))
        choices: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        for component0, g_hex0, lam0 in support_rows:
            component = int(component0); g_blob = bytes.fromhex(str(g_hex0))
            g = unpack(g_blob)
            for row in by_component[component]:
                if int(row["relator_index"]) != target[0]:
                    continue
                t_blob = pack(translation_from_pair(g, row["_value"], mul=mul,
                    inverse=inverse, orientation="g_times_h_inverse",
                    inverse_h=inverse_h[bytes.fromhex(row["element_hex"])]))
                if t_blob == target[1]:
                    candidate = {"component": component,
                        "g_hex": str(g_hex0), "lambda_coefficient": int(lam0),
                        "relator_index": target[0],
                        "h_hex": row["element_hex"],
                        "base_coefficient": int(row["coefficient"]),
                        "translation_hex": target[1].hex(),
                        "formula": "t=g*h^-1",
                        "selection_order":
                            "component,g_blob,h_blob,lambda_coefficient,base_coefficient"}
                    order = (component, g_blob, bytes.fromhex(row["element_hex"]),
                             int(lam0), int(row["coefficient"]))
                    choices.append((order, candidate))
        require(choices, "first active contributor")
        contributor = min(choices, key=lambda item: item[0])[1]
    return {"_candidate_values": corr, "_active_rows": active,
        "_zero_keys": zero_keys, "first_contributing_pair": contributor,
        "public": {"complete": True, "pair_attempts": attempts,
            "candidate_count_before_zero_deletion": len(corr),
            "cancellation_to_zero_count": len(zero_keys),
            "active_count": len(active),
            "scalar_distribution": {"1": sum(r[2] == 1 for r in active),
                                    "2": sum(r[2] == 2 for r in active)},
            "packed_row_width": width + 2,
            "packed_rows_sha256": sha_bytes(encoded),
            "packed_rows_bytes": len(encoded),
            "public_order": "translation blob lexicographic, relator index",
            "first_active": first,
            "candidate_queries_interned": 0,
            "full_E4_enumerated": False}}


def direct_scalar(translation: Any, relator: int,
                  occurrences: Sequence[dict[str, Any]], support_map: dict[tuple[int, bytes], int],
                  *, mul: Callable[[Any, Any], Any], pack: Callable[[Any], bytes]) -> int:
    return sum(int(row["coefficient"]) * support_map.get(
        (int(row["component"]), pack(mul(translation, row["_value"]))), 0)
        for row in occurrences if int(row["relator_index"]) == relator) % 3


def correlation_canaries(correlation: dict[str, Any], support_rows: Sequence[Sequence[Any]],
                         occurrences: Sequence[dict[str, Any]], *, width: int,
                         identity: Any, unpack: Callable[[bytes], Any],
                         mul: Callable[[Any, Any], Any], pack: Callable[[Any], bytes]) \
        -> dict[str, Any]:
    values = correlation["_candidate_values"]
    support_map = {(int(c), bytes.fromhex(str(h))): int(a)
                   for c, h, a in support_rows}
    identity_rows = []
    iblob = pack(identity)
    for relator in range(1, 12):
        direct = direct_scalar(identity, relator, occurrences, support_map,
                               mul=mul, pack=pack)
        accumulated = values.get((relator, iblob), 0)
        require(direct == accumulated, "identity direct correlation")
        identity_rows.append([relator, direct])
    ordered = sorted(values, key=lambda key: (key[1], key[0]))
    require(len(ordered) >= 4, "four deterministic correlation canaries")
    sample_keys = ordered[:4]
    if correlation["_zero_keys"]:
        zero = sorted(correlation["_zero_keys"], key=lambda key:(key[1],key[0]))[0]
        if zero not in sample_keys: sample_keys.append(zero)
    samples = []
    for relator, tblob in sample_keys:
        direct = direct_scalar(unpack(tblob), relator, occurrences, support_map,
                               mul=mul, pack=pack)
        require(direct == values[(relator, tblob)], "sample direct correlation")
        samples.append({"translation_hex": tblob.hex(),
                        "relator_index": relator, "scalar": direct,
                        "cancellation_row": direct == 0})
    first = correlation["public"]["first_active"]
    first_direct = None
    if first is not None:
        first_direct = direct_scalar(unpack(bytes.fromhex(first["translation_hex"])),
            int(first["relator_index"]), occurrences, support_map,
            mul=mul, pack=pack)
        require(first_direct == int(first["scalar"]), "first-active full direct column")
    return {"identity_translation": identity_rows,
        "identity_translation_pass": True, "deterministic_samples": samples,
        "sample_count": len(samples), "cancellation_sample_included":
            (not correlation["_zero_keys"] or any(r["cancellation_row"] for r in samples)),
        "first_active_direct_scalar": first_direct,
        "first_active_full_column_replayed": first is None or first_direct is not None,
        "left_orientation": "t=g*h^-1", "orientation_mutations_rejected": True}


def make_section_witness(old: Any, e4: Any, prefix: dict[str, Any],
                         occurrences: Sequence[dict[str, Any]],
                         correlation: dict[str, Any], monitor: Monitor) -> dict[str, Any]:
    first = correlation["public"]["first_active"]
    if first is None:
        return {}
    pair = correlation["first_contributing_pair"]
    require(pair is not None, "active contributing pair")
    pool, sections = prefix["pool"], prefix["sections"]
    component = int(pair["component"]); g_blob = bytes.fromhex(pair["g_hex"])
    g = pool.unpack(g_blob)
    r0 = old.word_substitute(
        old.embed_f2_pb3(old.hexagon_words(old.FIXED_WORD)[0]), old.cofaces(3)[0])
    raw, value, raw_sections = old.fox_gradient(r0, e4)
    require(value == e4.identity, "base target6 quotient identity")
    target_word = raw_sections.get(g) if (component, g) in raw else None
    u_root = h0_root = None; recovery: dict[str, Any]
    if target_word is not None:
        g_root = sections.expressions.flat(target_word, g_blob,
                                            "full_D2_lambda_support_g")
        recovery = {"method": "base_target6_fox_prefix",
                    "component": component, "g_hex": g_blob.hex(),
                    "source_word_sha256": sha_obj(target_word)}
    else:
        candidates = sorted((r for r in occurrences if r["component"] == component),
            key=lambda r: (r["relator_index"], bytes.fromhex(r["element_hex"])))
        found = None
        for row in candidates:
            h0 = row["_value"]
            u = e4.mul(g, e4.inverse(h0)); u_blob = pool.pack(u)
            registered = sections.by_blob.get(u_blob)
            if registered is not None:
                found = (row, u_blob, registered); break
        require(found is not None, "sparse section recovery invariant")
        row, u_blob, registered = found
        u_root = sections.expression_root(registered, "full_D2_registered_u")
        h0_root = int(row["section_expression_root"])
        g_root = sections.expressions.product(u_root, h0_root,
                                              "full_D2_recovered_g")
        recovery = {"method": "registered_translation_times_base_prefix",
            "component": component, "g_hex": g_blob.hex(),
            "base_relator_index": row["relator_index"],
            "base_h0_hex": row["element_hex"],
            "registered_u_hex": u_blob.hex()}
    require(sections.expressions.value_blob(g_root) == g_blob,
            "recovered g expression")
    h_row = next(r for r in occurrences if r["relator_index"] == pair["relator_index"]
                 and r["component"] == component and r["element_hex"] == pair["h_hex"])
    h_root = int(h_row["section_expression_root"])
    inverse_h_root = sections.expressions.inverse(h_root, "full_D2_inverse_h")
    t_root = sections.expressions.product(g_root, inverse_h_root,
                                          "full_D2_translation_t")
    t_blob = bytes.fromhex(first["translation_hex"])
    require(sections.expressions.value_blob(t_root) == t_blob,
            "section t=g*h^-1")
    requested_roots = [g_root, t_root, h_root, inverse_h_root]
    if u_root is not None: requested_roots.extend([u_root, int(h0_root)])
    roots = list(dict.fromkeys(requested_roots))
    payload, renumber = sections.expressions.serialize_reachable(roots, monitor)
    roles = {"g": renumber[g_root], "t": renumber[t_root],
             "h": renumber[h_root], "inverse_h": renumber[inverse_h_root],
             "u": None if u_root is None else renumber[u_root],
             "h0": None if h0_root is None else renumber[int(h0_root)]}
    g_word = materialize_section_node(old, e4, sections.expressions, g_root)
    t_word = materialize_section_node(old, e4, sections.expressions, t_root)
    require(e4.eval(g_word) == g and e4.eval(t_word) == pool.unpack(t_blob),
            "section word direct replay")
    return {"first_active": first, "contributing_pair": pair,
        "recovery": recovery, "node_roles": roles,
        "section_expressions": payload,
        "direct_replay": {"g_word_length": len(g_word),
            "g_word_sha256": sha_obj(g_word), "t_word_length": len(t_word),
            "t_word_sha256": sha_obj(t_word), "g_value_hex": g_blob.hex(),
            "t_value_hex": t_blob.hex(), "both_exact": True},
        "typed_PRODUCT_INVERSE_only_above_registered_leaves": True,
        "transient_pool_ID_exported": False}


def materialize_section_node(old: Any, e4: Any, expressions: Any,
                             node: int) -> list[int]:
    """Local repair for the frozen predecessor's unreachable inverse typo."""
    require(0 <= node < len(expressions.kind), "local section node")
    memo: dict[int, list[int]] = {}

    def visit(current: int) -> list[int]:
        if current in memo:
            return memo[current]
        kind = int(expressions.kind[current])
        if kind == expressions.IDENTITY:
            word: list[int] = []
        elif kind == expressions.SIGNED_GENERATOR:
            word = [int(expressions.signed_generator[current])]
        elif kind == expressions.FLAT:
            flat = expressions.flat_words[current]
            require(flat is not None, "local flat section")
            word = list(flat)
        elif kind == expressions.INVERSE:
            word = old.inv_word(visit(int(expressions.left[current])))
        else:
            require(kind == expressions.PRODUCT, "local section kind")
            word = old.reduce_word(visit(int(expressions.left[current])) +
                                   visit(int(expressions.right[current])))
        if len(word) > old.CAPS["single_word_or_section_length"]:
            raise old.ResourceStop(
                "single_word_or_section_length",
                cap_key="single_word_or_section_length",
                cap_limit=old.CAPS["single_word_or_section_length"],
                observed_count=len(word), trigger_relation="gt")
        require(prefix_blob(e4, e4.eval(word)) ==
                    expressions.value_blobs[current],
                "local section word/value binding")
        memo[current] = word
        return word
    return visit(node)


def prefix_blob(e4: Any, value: Any) -> bytes:
    result = bytes(value[0]) + bytes(value[1])
    require(len(result) == e4.degree + e4.pc.n, "local section blob width")
    return result


def theorem_boundary() -> dict[str, Any]:
    return {"pinned_E4_roof_only": True, "157ee_joint_kernel_only": True,
        "D2_acting_group_is_PB4_E4_not_joint_correction_J": True,
        "eleven_base_relators_are_orbit_representatives_by_definition": True,
        "prefix_generates_module_or_FC44_assumed": False,
        "coinvariant_shortcut_used": False,
        "full_D2_left_translate_correlation_complete": True,
        "alternate_roofs_exhausted": False, "full_H3_corrections_exhausted": False,
        "global_lift_nonexistence_claimed": False, "B4_A_claimed": False,
        "B4_B_claimed": False, "active_translation_is_not_a_lift": True,
        "producer_only_is_crosschecked": False}


def provenance_row() -> dict[str, Any]:
    return {"run": "32359956713",
        "commit": "1696e7b44792b97c51a435d4160259462963c52d",
        "artifact_id": 9403505687,
        "archive_sha256":
            "9fe43b570dd135c4f26c910dff983e0e58492bb3250beb4cbe01d7e8bcca1192",
        "receipt_sha256":
            "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df",
        "evidence_only_not_imported": True}


TOP_KEYS = {"schema", "task_sha256", "terminal_token", "status", "reason",
    "claim", "phase", "pins", "caps", "upstream_caps", "provenance",
    "base_q3_replay", "normalized_inverse_fibre", "directed_base_support",
    "directed_surgery", "prefix", "lambda_oracle", "lambda_support",
    "base_columns", "correlation", "direct_canaries", "state_no_mutation",
    "section_witness", "theorem_boundary", "resource_guards", "partial",
    "input_errors", "performance"}

TIMED_PHASES = ("authenticated_input", "fresh_immutable_prefix",
    "raw_lambda_oracle", "base_columns", "dual_correlation",
    "section_witness")


def validate_performance(row:dict[str,Any],token:str,phase:str)->None:
    require(set(row) == {"initial_remaining_seconds", "elapsed_seconds",
        "remaining_seconds", "checks", "peak_rss_bytes", "hit_reason",
        "receipt_bytes", "phase_seconds", "pair_loop_cadence",
        "pool_intern_calls_in_correlation",
        "full_sparse_vectors_materialized_in_correlation",
        "full_E4_enumerations"}, "performance exact keys")
    initial=row["initial_remaining_seconds"];elapsed=row["elapsed_seconds"]
    remaining=row["remaining_seconds"]
    require(isinstance(initial,(int,float)) and not isinstance(initial,bool) and
            0<initial<=18_000 and isinstance(elapsed,(int,float)) and
            not isinstance(elapsed,bool) and elapsed>=0 and
            isinstance(remaining,(int,float)) and not isinstance(remaining,bool) and
            0<=remaining<=initial and abs((elapsed+remaining)-initial)<=1.0 and
            isinstance(row["checks"],int) and not isinstance(row["checks"],bool) and
            row["checks"]>=0 and isinstance(row["peak_rss_bytes"],int) and
            not isinstance(row["peak_rss_bytes"],bool) and
            row["peak_rss_bytes"]>=0 and isinstance(row["receipt_bytes"],int) and
            not isinstance(row["receipt_bytes"],bool) and row["receipt_bytes"]>=0 and
            row["pair_loop_cadence"]==4096 and
            row["pool_intern_calls_in_correlation"]==0 and
            row["full_sparse_vectors_materialized_in_correlation"]==0 and
            row["full_E4_enumerations"]==0,"performance numeric contract")
    if token in {"B345_E4_FULL_D2_QSTAR_SEPARATOR",
                 "B345_E4_FULL_D2_ACTIVE_TRANSLATION"}:
        expected=TIMED_PHASES
    elif token=="B345_E4_FULL_D2_UNKNOWN_INPUT":
        expected=()
    else:
        completed={"fresh_immutable_prefix":1,"raw_lambda_oracle":2,
            "base_columns":3,"dual_correlation":4,"section_witness":5,
            "receipt_serialization":6}
        require(phase in completed,"performance resource phase")
        expected=TIMED_PHASES[:completed[phase]]
    timings=row["phase_seconds"]
    require(isinstance(timings,dict) and set(timings)==set(expected) and
            all(isinstance(timings[name],(int,float)) and
                not isinstance(timings[name],bool) and timings[name]>=0
                for name in expected) and sum(timings.values())<=elapsed+1.0,
            "performance phase timings")


def empty_receipt(monitor: Monitor, upstream: dict[str, int]) -> dict[str, Any]:
    return {"schema": SCHEMA, "task_sha256": TASK_SHA,
        "terminal_token": "B345_E4_FULL_D2_UNKNOWN_RESOURCE",
        "status": "B345_E4_FULL_D2_UNKNOWN_RESOURCE", "reason": "initializing",
        "claim": "none", "phase": "authenticated_input", "pins": pin_rows(),
        "caps": CAPS, "upstream_caps": {"registry": upstream,
            "sha256": sha_obj(upstream)}, "provenance": provenance_row(),
        "base_q3_replay": {}, "normalized_inverse_fibre": {},
        "directed_base_support": {}, "directed_surgery": {}, "prefix": {},
        "lambda_oracle": {}, "lambda_support": {}, "base_columns": {},
        "correlation": {}, "direct_canaries": {}, "state_no_mutation": {},
        "section_witness": {}, "theorem_boundary": theorem_boundary(),
        "resource_guards": {"resource_hit": False, "resource": None,
            "atomic_partial": True}, "partial": {}, "input_errors": [],
        "performance": {**monitor.public(), "receipt_bytes": 0,
            "phase_seconds": {}, "pair_loop_cadence": 4096,
            "pool_intern_calls_in_correlation": 0,
            "full_sparse_vectors_materialized_in_correlation": 0,
            "full_E4_enumerations": 0}}


def validate_receipt_schema(receipt: dict[str, Any], *, fixture: bool = False) -> None:
    require(set(receipt) == TOP_KEYS and receipt["schema"] == SCHEMA and
            receipt["task_sha256"] == TASK_SHA and
            receipt["terminal_token"] == receipt["status"] in TERMINALS and
            receipt["phase"] in PHASES, "receipt envelope")
    require(receipt["caps"] == CAPS and set(receipt["upstream_caps"]) ==
            {"registry", "sha256"} and receipt["upstream_caps"]["sha256"] ==
            sha_obj(receipt["upstream_caps"]["registry"]), "cap registries")
    require(receipt["theorem_boundary"] == theorem_boundary(), "claim boundary")
    require(receipt["provenance"] == provenance_row(), "fixed provenance")
    require(set(receipt["resource_guards"]) ==
            {"resource_hit", "resource", "atomic_partial"} and
            receipt["resource_guards"]["atomic_partial"] is True,
            "resource guard schema")
    token = receipt["terminal_token"]
    math_fields = ("base_q3_replay", "normalized_inverse_fibre",
        "directed_base_support", "directed_surgery", "prefix",
        "lambda_oracle", "lambda_support", "base_columns", "correlation",
        "direct_canaries", "state_no_mutation", "section_witness")
    normal_guard = {"resource_hit": False, "resource": None,
                    "atomic_partial": True}
    if token == "B345_E4_FULL_D2_QSTAR_SEPARATOR":
        require(receipt["correlation"].get("complete") is True and
                receipt["correlation"].get("active_count") == 0 and
                receipt["section_witness"] == {} and
                receipt["claim"] == "qstar_separates_base_target6_from_full_D2_for_pinned_E4_roof" and
                receipt["reason"] == "complete_correlation_all_translates_zero" and
                receipt["phase"] == "complete" and
                receipt["resource_guards"] == normal_guard and
                receipt["partial"] == {} and receipt["input_errors"] == [] and
                all(receipt[name] for name in math_fields[:-1]) and
                receipt["performance"]["hit_reason"] is None,
                "separator terminal")
    elif token == "B345_E4_FULL_D2_ACTIVE_TRANSLATION":
        require(receipt["correlation"].get("complete") is True and
                receipt["correlation"].get("active_count", 0) > 0 and
                bool(receipt["section_witness"]) and
                receipt["claim"] == "first_active_full_D2_translation_exported_not_a_lift" and
                receipt["reason"] == "complete_correlation_has_nonzero_translation" and
                receipt["phase"] == "complete" and
                receipt["resource_guards"] == normal_guard and
                receipt["partial"] == {} and receipt["input_errors"] == [] and
                all(receipt[name] for name in math_fields) and
                receipt["performance"]["hit_reason"] is None,
                "active terminal")
    elif token == "B345_E4_FULL_D2_UNKNOWN_RESOURCE":
        resource_row = receipt["resource_guards"]["resource"]
        require(receipt["claim"] == "none" and
                receipt["resource_guards"]["resource_hit"] is True and
                isinstance(resource_row, dict) and
                receipt["reason"] == resource_row["cap_reason"] ==
                    resource_row["cap_key"] and
                resource_row["comparator"] in {"gt", "ge"} and
                receipt["partial"].get("correlation_published") is False,
                "resource terminal")
        key = resource_row["cap_key"]
        source = resource_row["cap_source"]
        require(source in {"local", "upstream"}, "resource cap source")
        registry = (CAPS if source == "local" else
                    receipt["upstream_caps"]["registry"])
        require(key in registry and resource_row["cap_limit"] == registry[key],
                "closed resource cap")
        comparison = (resource_row["observed_count"] > resource_row["cap_limit"]
                      if resource_row["comparator"] == "gt" else
                      resource_row["observed_count"] >= resource_row["cap_limit"])
        require(comparison, "resource observed comparator")
        require(receipt["performance"]["hit_reason"] == receipt["reason"] and
                receipt["input_errors"] == [] and
                set(resource_row) == {"cap_reason", "cap_key", "cap_source", "cap_limit",
                    "observed_count", "comparator", "phase", "current"} and
                receipt["partial"] == {"phase": resource_row["phase"],
                    "current": resource_row["current"],
                    "correlation_published": False,
                    "mathematical_claim": "none", "rollback_required": False,
                    "reason": resource_row["cap_reason"]},
                "resource exact nested schema")
        completed = {
            "fresh_immutable_prefix": 2,
            "raw_lambda_oracle": 5,
            "base_columns": 7,
            "dual_correlation": 8,
            "section_witness": 8,
            "receipt_serialization": 8,
        }
        require(resource_row["phase"] in completed,
                "resource stage registry")
        for index, name in enumerate(math_fields):
            require(bool(receipt[name]) == (index < completed[resource_row["phase"]]),
                    f"resource stage payload: {name}")
        current = resource_row["current"]
        if resource_row["cap_key"] in {"pair_attempts",
                                      "distinct_correlation_candidates"}:
            require(set(current) == {"lambda_ordinal",
                                     "base_component_ordinal"} and
                    all(isinstance(current[k], int) and current[k] >= 1
                        for k in current), "resource pair current")
        elif resource_row["cap_key"] == "packed_active_rows":
            require(current == {"post_accumulation": True},
                    "resource active current")
        else:
            require(current == {}, "resource non-correlation current")
    else:
        require(token == "B345_E4_FULL_D2_UNKNOWN_INPUT" and
                receipt["claim"] == "none" and receipt["input_errors"] and
                receipt["reason"] == "authenticated_input_failure" and
                receipt["phase"] == "authenticated_input" and
                receipt["resource_guards"] == normal_guard and
                receipt["partial"] == {} and
                all(receipt[name] == {} for name in math_fields) and
                receipt["performance"]["hit_reason"] is None,
                "input terminal")
    validate_performance(receipt["performance"],token,receipt["phase"])
    if not fixture:
        require(receipt["pins"] == pin_rows(), "receipt exact pins")


def run(q3_path: Path, *, seconds: float = 18_000.0) -> dict[str, Any]:
    monitor = Monitor(seconds); phase_started = time.monotonic()
    phases: dict[str, float] = {}; phase = "authenticated_input"
    ed: Any = None; old: Any = None; prefix: dict[str, Any] | None = None
    upstream: dict[str, int] = {}
    receipt = empty_receipt(monitor, upstream)

    def close_phase(label: str) -> None:
        nonlocal phase_started
        now = time.monotonic(); phases[label] = now-phase_started; phase_started = now
        print(f"D972_B345_FULL_D2_DUAL_CORRELATION_PHASE {label} "
              f"elapsed_s={phases[label]:.6f}", flush=True)

    try:
        ed = load_ed(); upstream = upstream_caps(ed)
        receipt = empty_receipt(monitor, upstream)
        if q3_path.resolve() != (ROOT/Q3_PATH).resolve() or not q3_path.is_file() or \
                sha_file(q3_path) != Q3_SHA:
            raise InputFailure("q3 artifact path/SHA drift")
        try:
            q3, old = ed.authenticated_input(q3_path)
        except ed.AffineInput as exc:
            raise InputFailure(str(exc)) from exc
        e3, e4, _ = old.reconstruct_quotients(q3)
        receipt["base_q3_replay"] = old.replay_base_q3(q3, e3, e4)
        normalized, raw_source_key, inverse_words = old.normalized_inverse_fibre(q3, e4)
        receipt["normalized_inverse_fibre"] = normalized
        require(e4.degree == 144 and e4.pc.n == 10, "E4 width 154")
        close_phase("authenticated_input")

        phase = "fresh_immutable_prefix"; monitor.check(phase, force=True)
        try:
            prefix, dependent = ed.build_instrumented_prefix(
                old, e4, monitor, raw_source_key)
        except CorrelationResource:
            raise
        except old.ResourceStop as exc:
            raise convert_upstream(exc, ed, phase, {}) from exc
        pool = prefix["pool"]
        require(len(pool.values) == PREFIX_POOL_CHECKPOINT and
                tuple(prefix["raw_source_tuple"]) == tuple(raw_source_key) and
                tuple(pool.value(i) for i in prefix["base_source_key"]) ==
                    tuple(raw_source_key), "prefix pool/source anchors")
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        require(prefix["directed_surgery"]["stable_rounds_projection_sha256"] ==
                    PREFIX_STABLE_SHA and
                prefix["directed_surgery"]["translations_sha256"] ==
                    PREFIX_TRANSLATIONS_SHA and
                prefix["directed_surgery"]["columns_sha256"] ==
                    PREFIX_COLUMNS_SHA and
                prefix["directed_surgery"]["blocker_history_sha256"] ==
                    PREFIX_BLOCKERS_SHA, "fresh directed prefix")
        receipt["prefix"] = {"counts": PREFIX_COUNTS,
            "accounting": prefix["accounting"],
            "basis_gate": old.affine_basis_gate(prefix["basis"], pool),
            "prefix_pool_checkpoint": len(pool.values),
            "dependent_events": dependent,
            "dependent_event_count": len(dependent),
            "dependent_event_sha256": sha_obj(dependent),
            "fresh_not_imported": True,
            "source_sha256": ed.STRONG_SHA}
        close_phase(phase)

        phase = "raw_lambda_oracle"; monitor.check(phase, force=True)
        try:
            qstar = ed.validate_qstar_label(ed.QSTAR_LABEL, 154)
            oracle = ed.RawLambdaOracle(old, prefix, qstar, monitor)
        except CorrelationResource:
            raise
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, ed, phase, {}) from exc
        pivot_zero = []
        for pivot in sorted(prefix["basis"].rows, key=pool.pivot_order):
            row_data = prefix["basis"].rows[pivot]
            row = row_data[0] if isinstance(row_data, tuple) else row_data
            pivot_zero.append(oracle.packed(row))
        require(pivot_zero == [0]*PREFIX_COUNTS["pivots"], "lambda pivots zero")
        dependent_zero = []
        for event in dependent:
            packed: dict[int, int] = {}
            for component, value_hex, coefficient in event["raw_column"]:
                identifier = pool.ids.get(bytes.fromhex(value_hex))
                require(identifier is not None, "dependent pool key")
                packed[old.pack_vector_key(component, identifier)] = coefficient
            require(oracle.packed(packed) == 0, "lambda dependent zero")
            dependent_zero.append(0)
        r0 = old.word_substitute(old.embed_f2_pb3(
            old.hexagon_words(old.FIXED_WORD)[0]), old.cofaces(3)[0])
        r0_raw, r0_value, _ = old.fox_gradient(r0, e4)
        require(r0_value == e4.identity and oracle.sparse(r0_raw) == 2,
                "base target6 lambda value")
        oracle.public.update({"pivot_annihilation_count": len(pivot_zero),
            "pivot_annihilation_sha256": sha_obj(pivot_zero),
            "dependent_annihilation_count": len(dependent_zero),
            "dependent_annihilation_sha256": sha_obj(dependent_zero),
            "base_target6_lambda": 2,
            "base_target6_name": "hexagon_1_coface_0"})
        receipt["lambda_oracle"] = oracle.public
        support = lambda_support(oracle, 154); receipt["lambda_support"] = support
        close_phase(phase)

        phase = "base_columns"; monitor.check(phase, force=True)
        bundle = rebuild_base_bundle(old, prefix, e4)
        receipt["base_columns"] = bundle["public"]
        close_phase(phase)

        phase = "dual_correlation"; monitor.check(phase, force=True)
        before = state_snapshot(prefix); mul, inverse = uncached_ops(old, e4)
        corr = exact_correlation(support["rows"], bundle["private_occurrences"],
            width=154, unpack=pool.unpack, mul=mul, inverse=inverse,
            pack=pool.pack, monitor=monitor)
        canaries = correlation_canaries(corr, support["rows"],
            bundle["private_occurrences"], width=154, identity=e4.identity,
            unpack=pool.unpack, mul=mul, pack=pool.pack)
        after = state_snapshot(prefix)
        require(before == after, "correlation persistent-state neutrality")
        receipt["state_no_mutation"] = {"before": public_snapshot(before),
            "after": public_snapshot(after), "exact_equal": True,
            "helper_signature_excludes_pool_basis_DAG_sections": True,
            "pool_ID_reuse_or_intern_calls": 0, "E4_cache_path_used": False}
        receipt["direct_canaries"] = canaries
        receipt["correlation"] = corr["public"]
        close_phase(phase)

        phase = "section_witness"; monitor.check(phase, force=True)
        try:
            witness = make_section_witness(old, e4, prefix,
                bundle["private_occurrences"], corr, monitor)
        except CorrelationResource:
            raise
        except (old.ResourceStop, ed.ResourceStop) as exc:
            raise convert_upstream(exc, ed, phase, {}) from exc
        receipt["section_witness"] = witness
        active = corr["public"]["active_count"] > 0
        receipt["terminal_token"] = receipt["status"] = (
            "B345_E4_FULL_D2_ACTIVE_TRANSLATION" if active else
            "B345_E4_FULL_D2_QSTAR_SEPARATOR")
        receipt["reason"] = ("complete_correlation_has_nonzero_translation"
                             if active else
                             "complete_correlation_all_translates_zero")
        receipt["claim"] = ("first_active_full_D2_translation_exported_not_a_lift"
                            if active else
                            "qstar_separates_base_target6_from_full_D2_for_pinned_E4_roof")
        receipt["phase"] = "complete"; close_phase(phase)
    except InputFailure as exc:
        if not upstream and ed is not None: upstream = upstream_caps(ed)
        receipt = empty_receipt(monitor, upstream)
        receipt["terminal_token"] = receipt["status"] = \
            "B345_E4_FULL_D2_UNKNOWN_INPUT"
        receipt["reason"] = "authenticated_input_failure"
        receipt["claim"] = "none"; receipt["phase"] = "authenticated_input"
        receipt["input_errors"] = [str(exc)]
    except CorrelationResource as exc:
        # The wrapper may represent either a local or a pinned upstream cap.
        monitor.hit_reason = exc.key
        receipt["terminal_token"] = receipt["status"] = \
            "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
        receipt["reason"] = exc.key; receipt["claim"] = "none"
        receipt["phase"] = exc.phase
        receipt["correlation"] = {}
        receipt["section_witness"] = {}
        receipt["direct_canaries"] = {}
        receipt["state_no_mutation"] = {}
        receipt["resource_guards"] = {"resource_hit": True,
            "resource": exc.public(), "atomic_partial": True}
        receipt["partial"] = {"phase": exc.phase, "current": exc.current,
            "correlation_published": False, "mathematical_claim": "none",
            "rollback_required": False,
            "reason": exc.key}
    receipt["performance"].update(monitor.public())
    receipt["performance"]["phase_seconds"] = phases
    phase = "receipt_serialization"
    validate_receipt_schema(receipt)
    return receipt


def write_checked(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Fixed point for the exact canonical byte-count field.
    for _ in range(8):
        raw = (json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        size = len(raw)
        if receipt["performance"]["receipt_bytes"] == size:
            break
        receipt["performance"]["receipt_bytes"] = size
    raw = (json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    require(len(raw) == receipt["performance"]["receipt_bytes"],
            "receipt byte fixed point")
    if len(raw) > CAPS["packed_receipt_bytes"]:
        raise CorrelationResource("packed_receipt_bytes",
            CAPS["packed_receipt_bytes"], len(raw), "gt",
            "receipt_serialization", {})
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(raw)
    require(temporary.read_bytes() == raw, "receipt readback")
    os.replace(temporary, path)
    require(path.read_bytes() == raw, "receipt final readback")


def finalize_serialization_resource(receipt: dict[str, Any],
                                    exc: CorrelationResource, *,
                                    fixture: bool = False) -> None:
    """Apply the production serialization-RESOURCE terminal transition."""
    require(exc.key == "packed_receipt_bytes" and
            exc.cap_source == "local" and
            exc.limit == CAPS["packed_receipt_bytes"] and
            exc.phase == "receipt_serialization" and exc.current == {},
            "serialization resource selector")
    receipt["terminal_token"] = receipt["status"] = \
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
    receipt["reason"] = exc.key
    receipt["claim"] = "none"
    receipt["phase"] = exc.phase
    receipt["correlation"] = {}
    receipt["section_witness"] = {}
    receipt["direct_canaries"] = {}
    receipt["state_no_mutation"] = {}
    receipt["resource_guards"] = {"resource_hit": True,
        "resource": exc.public(), "atomic_partial": True}
    receipt["partial"] = {"phase": exc.phase, "current": exc.current,
        "correlation_published": False, "mathematical_claim": "none",
        "rollback_required": False, "reason": exc.key}
    receipt["performance"]["hit_reason"] = exc.key
    validate_receipt_schema(receipt, fixture=fixture)


def write_with_resource_fallback(path: Path, receipt: dict[str, Any], *,
                                 fixture: bool = False) -> bool:
    """Write once, or atomically publish the exact serialization RESOURCE."""
    try:
        write_checked(path, receipt)
        return False
    except CorrelationResource as exc:
        finalize_serialization_resource(receipt, exc, fixture=fixture)
        write_checked(path, receipt)
        return True


###############################################################################
# Bounded production-helper self-test
###############################################################################

def _perm_mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def _perm_inv(a: tuple[int, ...]) -> tuple[int, ...]:
    out = [0]*len(a)
    for i, value in enumerate(a): out[value] = i
    return tuple(out)


def _toy_rows() -> tuple[list[list[Any]], list[dict[str, Any]], int]:
    one=(0,1,2); r=(1,2,0); s=(1,0,2)
    values=[one,r,_perm_mul(r,r),s,_perm_mul(r,s),_perm_mul(s,r)]
    support=[]
    for c in (1,2):
        for i,value in enumerate(values):
            if (i+c)%2 == 0: support.append([c,bytes(value).hex(),1+(i%2)])
    support.sort(key=lambda x:(x[0],bytes.fromhex(x[1])))
    base=[]
    for j in range(1,3):
        for c,value,a in ((1,values[j],1),(1,values[j+2],2),
                          (2,values[j+1],1),(2,values[j+3],2)):
            base.append({"relator_index":j,"component":c,"coefficient":a,
                         "element_hex":bytes(value).hex(),"_value":value,
                         "section_word":[j,c]})
    return support,base,3


def expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError):
        return
    raise RuntimeError(f"selftest mutation accepted: {label}")


def self_test() -> None:
    support, base, width = _toy_rows(); one=(0,1,2)
    r=(1,2,0); s=(1,0,2)
    corr = exact_correlation(support,base,width=width,
        unpack=lambda b:tuple(b),mul=_perm_mul,inverse=_perm_inv,
        pack=bytes,monitor=None,caps={"pair_attempts":1000,
        "distinct_correlation_candidates":1000,"packed_active_rows":1000})
    require(corr["public"]["complete"] and
            corr["public"]["candidate_count_before_zero_deletion"] >= 4,
            "selftest active correlation")
    canary=correlation_canaries(corr,support,base,width=width,identity=one,
        unpack=lambda b:tuple(b),mul=_perm_mul,pack=bytes)
    require(canary["sample_count"]>=4,"selftest canaries")
    # Exhaustive separator through the same helper/finalizer/schema path.
    zero=exact_correlation([],base,width=width,unpack=lambda b:tuple(b),
        mul=_perm_mul,inverse=_perm_inv,pack=bytes,monitor=None,
        caps={"pair_attempts":1000,"distinct_correlation_candidates":1000,
              "packed_active_rows":1000})
    monitor=Monitor(30); fixture=empty_receipt(monitor,{})
    fixture["pins"]={}
    for name in ("base_q3_replay","normalized_inverse_fibre",
                 "directed_base_support","directed_surgery","prefix",
                 "lambda_oracle","lambda_support","base_columns",
                 "direct_canaries","state_no_mutation"):
        fixture[name]={"toy":True}
    fixture["correlation"]=zero["public"]
    fixture["terminal_token"]=fixture["status"]="B345_E4_FULL_D2_QSTAR_SEPARATOR"
    fixture["reason"]="complete_correlation_all_translates_zero"
    fixture["claim"]="qstar_separates_base_target6_from_full_D2_for_pinned_E4_roof"
    fixture["phase"]="complete"
    fixture["performance"]["phase_seconds"]={name:0.0 for name in TIMED_PHASES}
    validate_receipt_schema(fixture,fixture=True)
    # Active uses the same terminal selector/schema.  A bounded typed section
    # expression is represented by PRODUCT(INVERSE) over exact toy values.
    fixture2=json.loads(json.dumps(fixture)); fixture2["correlation"]=corr["public"]
    fixture2["terminal_token"]=fixture2["status"]="B345_E4_FULL_D2_ACTIVE_TRANSLATION"
    fixture2["reason"]="complete_correlation_has_nonzero_translation"
    fixture2["claim"]="first_active_full_D2_translation_exported_not_a_lift"
    fixture2["section_witness"]={"toy":True,"PRODUCT":True,"INVERSE":True,
        "value_replay":True}
    validate_receipt_schema(fixture2,fixture=True)
    # True cancellation is required in at least one deterministic fixture.
    cancel_support=[[1,bytes(one).hex(),1]]
    cancel_base=[{"relator_index":1,"component":1,"coefficient":1,
                  "element_hex":bytes(one).hex(),"_value":one},
                 {"relator_index":1,"component":1,"coefficient":2,
                  "element_hex":bytes(one).hex(),"_value":one}]
    cancellation=exact_correlation(cancel_support,cancel_base,width=3,
        unpack=lambda b:tuple(b),mul=_perm_mul,inverse=_perm_inv,pack=bytes,
        monitor=None,caps={"pair_attempts":10,
        "distinct_correlation_candidates":10,"packed_active_rows":10})
    require(cancellation["public"]["cancellation_to_zero_count"]==1 and
            cancellation["public"]["active_count"]==0,"selftest cancellation")
    # Three wrong orientations are distinct from the correct answer and fail
    # the actual t*h=g gate on a noncommuting S4 fixture.
    g=(1,2,3,0); h=(1,0,2,3)
    answers = [_perm_mul(g,_perm_inv(h)), _perm_mul(_perm_inv(h),g),
               _perm_mul(_perm_inv(g),h), _perm_mul(h,_perm_inv(g))]
    require(len(set(answers)) == 4, "selftest orientation values distinct")
    require(translation_from_pair(g,h,mul=_perm_mul,inverse=_perm_inv,
            orientation="g_times_h_inverse") == _perm_mul(g,_perm_inv(h)),
            "selftest correct orientation")
    for orientation in ("h_inverse_times_g","g_inverse_times_h",
                        "right_action_solution"):
        try:
            translation_from_pair(g,h,mul=_perm_mul,inverse=_perm_inv,
                                  orientation=orientation)
        except RuntimeError:
            pass
        else:
            raise RuntimeError(f"selftest accepted orientation {orientation}")
    # Actual inherited serializer plus the owned INVERSE-safe materializer.
    ed=load_ed()
    reachable_caps=upstream_caps(ed)
    require("raw_lambda_recursion_edges" in reachable_caps and
            "single_word_or_section_length" in reachable_caps and
            "packed_receipt_bytes" not in reachable_caps and
            "cube_count" not in reachable_caps,
            "selftest reachable upstream resource registry")
    old=ed.load_pinned_module(ed.OLD_PRODUCER,ed.OLD_PRODUCER_SHA,
                              "_d972_157eg_selftest_prefix_source")
    identity_element=(one,());g_element=(r,());h_element=(s,())
    def toy_blob(value:Any)->bytes:
        require(isinstance(value,tuple) and len(value)==2 and
                isinstance(value[0],tuple) and len(value[0])==3 and
                isinstance(value[1],tuple) and len(value[1])==0,
                "toy production Element shape")
        result=bytes(value[0])+bytes(value[1])
        require(len(result)==3,"toy production blob width")
        return result
    class ToyPC:
        n=0
    class ToyQ:
        degree=3
        def __init__(self)->None:
            self.pc=ToyPC();self.collector=self.pc
            self.identity=identity_element
            self.generators=[g_element,h_element,identity_element,
                             identity_element,identity_element,identity_element]
            self.inverse_generators=[self.inverse(x) for x in self.generators]
        @staticmethod
        def mul(a:Any,b:Any)->Any:
            toy_blob(a);toy_blob(b)
            return (_perm_mul(a[0],b[0]),())
        @staticmethod
        def inverse(a:Any)->Any:
            toy_blob(a)
            return (_perm_inv(a[0]),())
        def eval(self,word:Sequence[int],images:Sequence[Any]|None=None)->Any:
            marked=self.generators if images is None else images;out=self.identity
            for letter in word:
                value=marked[abs(letter)-1]
                out=self.mul(out,value if letter>0 else self.inverse(value))
            return out
    toy_q=ToyQ()
    class ToyPool:
        quotient=toy_q;width=3;identity_id=0
        @staticmethod
        def pack(value:Any)->bytes:return toy_blob(value)
        @staticmethod
        def unpack(value:bytes)->Any:
            require(len(value)==3,"toy pool packed width")
            return (tuple(value),())
        @staticmethod
        def blob(identifier:int)->bytes:
            require(identifier==0,"toy pool identity")
            return toy_blob(identity_element)
    require(toy_q.degree==3 and toy_q.pc.n==0 and ToyPool.width==3 and
            len(ToyPool.pack(identity_element))==toy_q.degree+toy_q.pc.n and
            ToyPool.unpack(ToyPool.pack(g_element))==g_element,
            "selftest production Element/blob contract")
    expect_failure(lambda:ToyPool.pack(r),"bare permutation Element")
    expressions=old.SectionExpressionDAG(ToyPool())
    identity_root=expressions.identity("toy_identity")
    flat_g_root=expressions.flat([1],toy_blob(g_element),"toy_flat_g")
    g_root=expressions.product(identity_root,flat_g_root,
                               "toy_identity_times_g")
    h_root=expressions.flat([2],toy_blob(h_element),"toy_h")
    ih_root=expressions.inverse(h_root,"toy_inverse_h")
    t_root=expressions.product(g_root,ih_root,"toy_g_h_inverse")
    section_monitor=Monitor(30)
    payload,renumber=expressions.serialize_reachable([t_root],section_monitor)
    t_word=materialize_section_node(old,toy_q,expressions,t_root)
    require(toy_q.eval(t_word)==toy_q.mul(g_element,
                                         toy_q.inverse(h_element)) and
            payload["roots"]==[renumber[t_root]] and
            payload["node_count"]==6,"selftest typed section serialization")
    saved_parent=int(expressions.left[ih_root]);expressions.left[ih_root]=g_root
    try:
        expect_failure(lambda:materialize_section_node(
            old,toy_q,expressions,t_root),"inverse parent")
    finally:
        expressions.left[ih_root]=saved_parent
    # Exact public/private projection mutation.
    public={k:v for k,v in base[0].items() if not k.startswith("_")}
    require("_value" not in public and set(public)==
            {"relator_index","component","coefficient","element_hex","section_word"},
            "selftest helper projection")
    saved_pair_cap=CAPS["pair_attempts"]
    CAPS["pair_attempts"]=0
    try:
        try:
            exact_correlation(support,base,width=width,unpack=lambda b:tuple(b),
                mul=_perm_mul,inverse=_perm_inv,pack=bytes,monitor=None,caps=CAPS)
        except CorrelationResource as exc:
            resource_receipt=json.loads(json.dumps(fixture))
            resource_receipt["caps"]=dict(CAPS)
            resource_receipt["terminal_token"]=resource_receipt["status"]= \
                "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
            resource_receipt["reason"]="pair_attempts";resource_receipt["claim"]="none"
            resource_receipt["phase"]="dual_correlation"
            for name in ("correlation","direct_canaries","state_no_mutation",
                         "section_witness"):
                resource_receipt[name]={}
            resource_receipt["resource_guards"]={"resource_hit":True,
                "resource":exc.public(),"atomic_partial":True}
            resource_receipt["partial"]={"phase":"dual_correlation",
                "current":exc.current,"correlation_published":False,
                "mathematical_claim":"none","rollback_required":False,
                "reason":"pair_attempts"}
            resource_receipt["performance"]["hit_reason"]="pair_attempts"
            resource_receipt["performance"]["phase_seconds"]={
                name:0.0 for name in TIMED_PHASES[:4]}
            validate_receipt_schema(resource_receipt,fixture=True)
            for mutate,label in (
                (("reason","forged"),"resource reason"),
                (("phase","section_witness"),"resource phase"),
                (("correlation",{"forged":True}),"resource later payload")):
                bad=json.loads(json.dumps(resource_receipt))
                bad[mutate[0]]=mutate[1]
                expect_failure(lambda bad=bad:validate_receipt_schema(
                    bad,fixture=True),label)
            bad=json.loads(json.dumps(resource_receipt))
            bad["resource_guards"]["resource"]["cap_limit"] += 1
            expect_failure(lambda:validate_receipt_schema(bad,fixture=True),
                           "resource stale cap")
        else:
            raise RuntimeError("selftest resource cap not hit")
    finally:
        CAPS["pair_attempts"]=saved_pair_cap
    # The local receipt cap deliberately collides by name with the smaller
    # pinned-upstream cap.  Source typing, not dict-union order, selects it.
    serialization=json.loads(json.dumps(fixture))
    serialization["terminal_token"]=serialization["status"]= \
        "B345_E4_FULL_D2_UNKNOWN_RESOURCE"
    serialization["reason"]="packed_receipt_bytes"
    serialization["claim"]="none";serialization["phase"]="receipt_serialization"
    for name in ("correlation","direct_canaries","state_no_mutation",
                 "section_witness"):
        serialization[name]={}
    stop=CorrelationResource("packed_receipt_bytes",CAPS["packed_receipt_bytes"],
        CAPS["packed_receipt_bytes"]+1,"gt","receipt_serialization",{})
    serialization["resource_guards"]={"resource_hit":True,
        "resource":stop.public(),"atomic_partial":True}
    serialization["partial"]={"phase":"receipt_serialization","current":{},
        "correlation_published":False,"mathematical_claim":"none",
        "rollback_required":False,"reason":"packed_receipt_bytes"}
    serialization["performance"]["hit_reason"]="packed_receipt_bytes"
    validate_receipt_schema(serialization,fixture=True)
    # Exercise the actual production writer, overflow selector, terminal
    # finalizer, second atomic write, and canonical final-path readback.  The
    # injected cap and file live only inside the bounded system temp fixture.
    saved_receipt_cap=CAPS["packed_receipt_bytes"]
    try:
        CAPS["packed_receipt_bytes"]=65_536
        overflow=json.loads(json.dumps(fixture))
        overflow["caps"]=dict(CAPS)
        overflow["correlation"]["selftest_serialization_padding"]="x"*131_072
        validate_receipt_schema(overflow,fixture=True)
        with tempfile.TemporaryDirectory(
                prefix="shadow-atelier-157eg-write-") as directory:
            output=Path(directory)/"receipt.json"
            require(write_with_resource_fallback(
                output,overflow,fixture=True),
                "selftest production serialization fallback selected")
            final_raw=output.read_bytes()
            final_data=json.loads(final_raw)
            require(final_data==overflow and
                    final_raw==(json.dumps(final_data,sort_keys=True,
                        separators=(",",":"))+"\n").encode("utf-8") and
                    len(final_raw)==final_data["performance"]["receipt_bytes"] and
                    final_data["terminal_token"]==
                        "B345_E4_FULL_D2_UNKNOWN_RESOURCE" and
                    final_data["reason"]=="packed_receipt_bytes" and
                    final_data["resource_guards"]["resource"]["cap_source"]==
                        "local",
                    "selftest production serialization final readback")
            validate_receipt_schema(final_data,fixture=True)
    finally:
        CAPS["packed_receipt_bytes"]=saved_receipt_cap
    upstream=json.loads(json.dumps(serialization));upstream_limit=16_777_216
    upstream["upstream_caps"]={"registry":{"packed_receipt_bytes":upstream_limit},
        "sha256":sha_obj({"packed_receipt_bytes":upstream_limit})}
    upstream["resource_guards"]["resource"]["cap_source"]="upstream"
    upstream["resource_guards"]["resource"]["cap_limit"]=upstream_limit
    upstream["resource_guards"]["resource"]["observed_count"]=upstream_limit+1
    validate_receipt_schema(upstream,fixture=True)
    bad=json.loads(json.dumps(serialization))
    bad["resource_guards"]["resource"]["cap_source"]="upstream"
    expect_failure(lambda:validate_receipt_schema(bad,fixture=True),
                   "resource cap-source collision")
    for local_only in ("common_math_soft_deadline_seconds",
                       "producer_soft_rss_bytes"):
        bad=json.loads(json.dumps(serialization))
        bad["upstream_caps"]={"registry":reachable_caps,
            "sha256":sha_obj(reachable_caps)}
        badrow=bad["resource_guards"]["resource"]
        badrow["cap_source"]="upstream"
        badrow["cap_reason"]=badrow["cap_key"]=bad["reason"]=local_only
        badrow["cap_limit"]=CAPS[local_only]
        badrow["observed_count"]=CAPS[local_only]+1
        badrow["comparator"]="ge"
        bad["partial"]["reason"]=local_only
        bad["performance"]["hit_reason"]=local_only
        expect_failure(lambda bad=bad:validate_receipt_schema(
            bad,fixture=True),"local-only cap upstream masquerade "+local_only)
    bad=json.loads(json.dumps(serialization))
    bad["upstream_caps"]={"registry":reachable_caps,
        "sha256":sha_obj(reachable_caps)}
    badrow=bad["resource_guards"]["resource"]
    badrow["cap_source"]="upstream"
    badrow["cap_reason"]=badrow["cap_key"]=bad["reason"]="cube_count"
    badrow["cap_limit"]=ed.CAPS["cube_count"]
    badrow["observed_count"]=ed.CAPS["cube_count"]+1
    bad["partial"]["reason"]="cube_count"
    bad["performance"]["hit_reason"]="cube_count"
    expect_failure(lambda:validate_receipt_schema(bad,fixture=True),
                   "hard-equality cap masquerade")
    bad=json.loads(json.dumps(fixture));bad["extra"]=True
    try: validate_receipt_schema(bad,fixture=True)
    except RuntimeError: pass
    else: raise RuntimeError("selftest schema mutation")
    for field,value in (("reason","forged"),("phase","section_witness"),
                        ("partial",{"forged":True}),
                        ("resource_guards",{"resource_hit":True,
                          "resource":None,"atomic_partial":True})):
        bad=json.loads(json.dumps(fixture));bad[field]=value
        expect_failure(lambda bad=bad:validate_receipt_schema(
            bad,fixture=True),f"normal terminal {field}")
    bad=json.loads(json.dumps(fixture));bad["provenance"]["run"]="0"
    expect_failure(lambda:validate_receipt_schema(bad,fixture=True),
                   "provenance mutation")
    bad=json.loads(json.dumps(fixture));bad["performance"]["remaining_seconds"]=31.0
    expect_failure(lambda:validate_receipt_schema(bad,fixture=True),
                   "performance remaining mutation")
    bad=json.loads(json.dumps(fixture));bad["performance"]["phase_seconds"][
        "forged_phase"]=0.0
    expect_failure(lambda:validate_receipt_schema(bad,fixture=True),
                   "performance phase mutation")
    unknown=empty_receipt(Monitor(30),{});unknown["pins"]={}
    unknown["terminal_token"]=unknown["status"]= \
        "B345_E4_FULL_D2_UNKNOWN_INPUT"
    unknown["reason"]="authenticated_input_failure"
    unknown["input_errors"]=["toy pin failure"]
    validate_receipt_schema(unknown,fixture=True)
    bad=json.loads(json.dumps(unknown));bad["base_columns"]={"forged":True}
    expect_failure(lambda:validate_receipt_schema(bad,fixture=True),
                   "unknown input math injection")
    print("D972_B345_FULL_D2_DUAL_CORRELATION_PRODUCER_SELFTEST_PASS "
          "production_correlation=1 terminal_schema=1 active=1 separator=1 "
          "cancellation=1 orientations=3 public_shape=1 resource=1 section=1 "
          "cap_sources=2 serialization_finalizer=1 provenance=1 performance=1",
          flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--q3",type=Path,default=ROOT/Q3_PATH)
    parser.add_argument("--output",type=Path,default=ROOT/OUTPUT)
    parser.add_argument("--seconds",type=float,default=18_000.0)
    args=parser.parse_args(argv)
    if args.self_test: self_test(); return 0
    receipt=run(args.q3,seconds=args.seconds)
    write_with_resource_fallback(args.output,receipt)
    print("D972_B345_FULL_D2_DUAL_CORRELATION_PRODUCER_PASS "
          f"terminal={receipt['terminal_token']} output={args.output}",flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
