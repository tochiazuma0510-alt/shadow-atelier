"""157ed: complete ordered triple-cube raw-lambda census.

This file is deliberately versioned beside, rather than editing, the 157ec
lane.  The frozen 157ec producer is loaded only as an authenticated arithmetic
dependency: no receipt, basis, row, or scalar is imported.  The census,
packed arrays, lambda oracle, and terminal envelope are implemented here.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import os
import struct
import sys
import time
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

try:
    import resource
except ImportError:  # pragma: no cover - Windows-only bounded self-test path
    resource = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
TASK_SHA = "15511f73e665a90f1e518383cb7bd218d8dd8e747026c498c3b4acce62837c2f"
SCHEMA = "d972-b345-triple-cube-raw-lambda-census/v1"
Q3_ARTIFACT = Path("ci/out/d972_b345_q3_chief_v1.json")
OUTPUT = Path("ci/out/d972_b345_triple_cube_raw_lambda_census_v1.json")
Q3_ARTIFACT_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
OLD_PRODUCER = Path("search/d972_b345_seedspan_triple4_v1.py")
OLD_PRODUCER_SHA = "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"
OLD_CHECKER = Path("search/check_d972_b345_seedspan_triple4_v1.py")
OLD_CHECKER_SHA = "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981"
OLD_DRIVER = Path("search/d972_b345_seedspan_triple4_gha_driver_v1.g")
OLD_DRIVER_SHA = "a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4"
OLD_TASK = Path("sol/luna_task_157ec_b345_seedspan_triple4.md")
OLD_TASK_SHA = "1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2"
STRONG_SOURCE = Path("search/d972_b345_strong_wform_inertness_v1.py")
STRONG_SHA = "d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be"
Q3_PRODUCER = Path("search/d972_b345_q3_chief_v1.g")
Q3_PRODUCER_SHA = "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
Q3_DRIVER = Path("search/d972_b345_q3_gha_driver_v1.g")
Q3_DRIVER_SHA = "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"
FORMULA_SHA = "b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef"
EB_PRODUCER = Path("search/d972_b345_seedspan_affine_solver_v1.py")
EB_PRODUCER_SHA = "804414e69155f2b8d9aa2a2412b0120d64eb373945a0fa6163f1214b4673e19a"
EB_CHECKER = Path("search/check_d972_b345_seedspan_affine_solver_v1.py")
EB_CHECKER_SHA = "67ad8d8227f1a8a60e481977fd2d07d819d532deb2651cd28667db997ec46081"
EB_DRIVER = Path("search/d972_b345_seedspan_affine_solver_gha_driver_v1.g")
EB_DRIVER_SHA = "1c7a6169292146ada37007d2e5b9a48f21b7f1ae545fe84a969409d8b9741057"
OLD_SEED_SHA = "e99602b0981251e4bb81ab0d2113791563bc9ec9df2a45828aea2880ec6d2f9e"
CUBE_SHA = "3d26302d01b3c202350fdb8b9ea81badeaf9c62913c9e94be7e049ad7c391463"
PREFIX_ROUNDS_SHA = "bf07578f91f5ed66e6ddddd4ef83dafa45817a29df066940bbc13bd53cdd00f6"
CONTEXT_ALIAS_SHA = "15cdac950ede8ce4596e5014ae1b6d0caa28523898cb42f3387f435a11b919a8"
ROW_SPACE_SHA = "5dd0bd3411afae0a9adafca4254b6fda739774a8b970b59e661d67e686f549be"
BASE_REMAINDER_SHA = "e62a581658c1a7c6093d9e3e5155acf503731806c075cf1dd3937e336473e179"
ALL108_ZERO_SHA = "400f67f74b1250e538c395aa8bf647f6f7432ec07fe2582aaff06e5a47fe7ed5"
QSTAR_SHA = "f8b1cb6325b158f0984ca945dac2c0e915e0386e1f13ddb911acf0e4e2d9dcad"
PREFIX_STABLE_SHA = "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d"
PREFIX_TRANSLATIONS_SHA = "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f"
PREFIX_COLUMNS_SHA = "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343"
PREFIX_BLOCKERS_SHA = "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53"

TERMINALS = frozenset({
    "B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE",
    "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT",
    "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE",
    "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT",
})
FAILURE_CODES = {
    "typed": 0, "exponent_sums": 1, "E3_identity": 2,
    "marked_source_tuple": 3, "context_identity": 4, "target6_value": 5,
}
CAPS = {
    "cube_count": 26, "ordered_pair_count": 676,
    "ordered_triple_count": 17576, "unique_context_count": 31,
    "named_occurrence_count": 46, "cube_total_reduced_letters": 9162,
    "ordered_triple_unreduced_letters": 18580536,
    "prefix_columns": 362725, "prefix_pivots": 362709,
    "raw_lambda_oracle_entries": 362710,
    "raw_lambda_recursion_edges": 8388608,
    "typed_dp_state_records": 1048576,
    "packed_receipt_bytes": 16777216,
    "common_math_soft_deadline_seconds": 18000,
    "producer_soft_rss_bytes": 4831838208,
    "external_job_limit_minutes": 330, "safety_margin_minutes": 30,
}
UPSTREAM_RESOURCE_CAPS = {
    "single_word_or_section_length": 100_000,
    "provenance_dag_nodes": 2_000_000,
    "provenance_dag_edges": 4_000_000,
    "total_sparse_group_ring_keys": 4_194_304,
    "single_sparse_elimination_row": 4_194_304,
    "target_elimination_support": 4_194_304,
    "sparse_pivot_rows": 1_000_000,
    "element_pool": 2_000_000,
    "section_slp_nodes": 65_536,
    "directed_section_expr_nodes": 131_072,
    "directed_section_expr_edges": 262_144,
    "directed_unique_translations": 32_768,
    "directed_columns": 360_448,
    "wordexpr_nodes_per_candidate": 262_144,
    "wordexpr_edges_per_candidate": 1_048_576,
    "wordexpr_flat_leaves_per_candidate": 16_384,
    "wordexpr_expanded_letter_count_per_target": 4_194_304,
    "candidate_live_gradient_entries_total": 1_000_000,
    "candidate_element_pool_suffix": 1_000_000,
    "transaction_trace_records": 100_000,
    "blocker_table": 4_096,
    "affine_rows": 1_000_000,
    "target_live_remainders": 2_000_000,
    "dual_provenance_entries": 128,
    "missing_bounded_inverse_representative": 0,
}
UPSTREAM_RESOURCE_CAPS_SHA = \
    "f78c5df93b518f324f041023ceaa52979a20c1fbaeea051de3d0975789d07329"
PREFIX_COUNTS = {
    "columns": 362725, "pivots": 362709, "dependent_columns": 16,
    "live_sparse_entries": 3090367, "row_tail_visits": 2727658,
    "BFS_translations": 32768, "directed_translations": 207,
}
QSTAR_LABEL = [
    6, "hexagon_1_coface_0", 4,
    "0801040503000602070b0e0c110a090d0f10181a161315191412171e1b2322201d1c1f212625242c2b2a2928273534333231302f2e2d3e363738393a3b3c3d403f474645444342414c4d4e4f5048494a4b5251595857565554535a5b5c5d5e5f60616265666768696a6b63646c6d6e6f707172737476757d7c7b7a797877867e7f80818283848588878f8e8d8c8b8a8900000002020100000000",
]


def receipt_pins() -> dict[str, str]:
    return {
        "task_sha256": TASK_SHA, "q3_artifact_sha256": Q3_ARTIFACT_SHA,
        "old_producer_sha256": OLD_PRODUCER_SHA,
        "old_checker_sha256": OLD_CHECKER_SHA,
        "old_driver_sha256": OLD_DRIVER_SHA,
        "old_task_sha256": OLD_TASK_SHA, "strong_prefix_sha256": STRONG_SHA,
        "q3_producer_sha256": Q3_PRODUCER_SHA,
        "q3_checker_sha256": Q3_CHECKER_SHA,
        "q3_driver_sha256": Q3_DRIVER_SHA, "formula_sha256": FORMULA_SHA,
        "157eb_producer_sha256": EB_PRODUCER_SHA,
        "157eb_checker_sha256": EB_CHECKER_SHA,
        "157eb_driver_sha256": EB_DRIVER_SHA,
        "old_seed_sha256": OLD_SEED_SHA, "cube_sha256": CUBE_SHA,
        "predecessor_run": "32326652060",
        "predecessor_receipt_sha256":
            "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
    }


def validate_qstar_label(label: Sequence[Any], width: int) -> bytes:
    require(list(label[:3]) == [6, "hexagon_1_coface_0", 4] and
            len(label) == 4 and isinstance(label[3], str),
            "qstar target/component label")
    blob = bytes.fromhex(label[3])
    require(width == 154 and len(blob) == width and
            list(label) == QSTAR_LABEL, "qstar canonical bytes/width")
    return blob


def validate_qstar_dual(dual: dict[str, Any]) -> None:
    require(dual["equations"] == [{"label": QSTAR_LABEL, "coefficient": 1}]
            and dual["support_count"] == 1 and
            dual["support_sha256"] == QSTAR_SHA and
            dual["normalized_rhs"] == 1 and dual["yTz_mod3"] == 2 and
            dual["target_boundary"]["target_ordinals"] == [6] and
            dual["target6_fixed_prefix_functional"] is True,
            "support-one predecessor dual")


def first_failure_code(gates: Sequence[bool | None]) -> int:
    require(len(gates) == 5, "typed gate cardinality")
    for index, gate in enumerate(gates, 1):
        if gate is False:
            require(all(later is None for later in gates[index:]),
                    "typed gates evaluated after first failure")
            return index
        require(gate is True, "typed gate missing before decision")
    return 0


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_obj(value: Any) -> str:
    return digest_bytes(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    ).encode("utf-8"))


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def validate_upstream_cap_source(old: Any) -> None:
    inherited = dict(old.AFFINE_INHERITED_CAPS)
    inherited.update({
        "affine_rows": int(old.AFFINE_CAPS["affine_rows"]),
        "target_live_remainders": int(
            old.AFFINE_CAPS["target_live_remainders"]),
        "dual_provenance_entries": int(
            old.AFFINE_CAPS["dual_provenance_entries"]),
        "missing_bounded_inverse_representative": 0,
    })
    require(inherited == UPSTREAM_RESOURCE_CAPS and
            digest_obj(inherited) == UPSTREAM_RESOURCE_CAPS_SHA,
            "pinned upstream resource cap registry")


class AffineInput(RuntimeError):
    pass


class ResourceStop(RuntimeError):
    def __init__(self, reason: str, *, cap_key: str, cap_limit: int,
                 observed_count: int, trigger_relation: str = "gt",
                 phase: str = "unknown", ordinal: int = 0,
                 tuple_value: Sequence[int] = ()) -> None:
        super().__init__(reason)
        self.reason = reason
        self.cap_key = cap_key
        self.cap_limit = int(cap_limit)
        self.observed_count = int(observed_count)
        self.trigger_relation = trigger_relation
        self.phase = phase
        self.ordinal = int(ordinal)
        self.tuple_value = list(tuple_value)

    def public(self) -> dict[str, Any]:
        return {
            "cap_reason": self.reason, "cap_key": self.cap_key,
            "cap_limit": self.cap_limit, "observed_count": self.observed_count,
            "trigger_relation": self.trigger_relation, "phase": self.phase,
            "current_ordinal": self.ordinal, "current_tuple": self.tuple_value,
        }


def normalize_resource_stop(stop: ResourceStop,
                            outer_phase: str) -> ResourceStop:
    """Bind helper-local monitor phases to the committed public phase."""
    require(outer_phase in {
        "fresh_immutable_prefix", "raw_lambda_oracle",
        "predecessor_target6", "target6_scalar_dp",
        "complete_ordered_census", "formula_canaries",
        "receipt_serialization",
    }, "resource outer phase registry")
    return ResourceStop(
        stop.reason, cap_key=stop.cap_key, cap_limit=stop.cap_limit,
        observed_count=stop.observed_count,
        trigger_relation=stop.trigger_relation, phase=outer_phase,
        ordinal=stop.ordinal, tuple_value=stop.tuple_value,
    )


def convert_upstream_resource_stop(exc: Any, outer_phase: str,
                                   ordinal: int,
                                   tuple_value: Sequence[int]) -> ResourceStop:
    """Translate only a pinned, exact old-cap event; unknown/stale is fatal."""
    cap_key = str(getattr(exc, "cap_key", ""))
    cap_limit = int(getattr(exc, "cap_limit", -1))
    reason = str(getattr(exc, "reason", ""))
    require(cap_key in UPSTREAM_RESOURCE_CAPS,
            "unregistered upstream resource cap")
    require(cap_limit == UPSTREAM_RESOURCE_CAPS[cap_key],
            "stale upstream resource cap limit")
    require(reason == cap_key, "upstream resource reason/key drift")
    return ResourceStop(
        reason, cap_key=cap_key,
        cap_limit=cap_limit,
        observed_count=int(getattr(exc, "observed_count", 0)),
        trigger_relation=str(getattr(exc, "trigger_relation", "gt")),
        phase=outer_phase, ordinal=ordinal, tuple_value=tuple_value,
    )


class Budget:
    def __init__(self, seconds: float = 18000.0) -> None:
        require(0 < float(seconds) <= CAPS["common_math_soft_deadline_seconds"],
                "producer remaining common deadline")
        self.started = time.monotonic()
        self.deadline = self.started + float(seconds)
        self.checks = 0
        self.initial_seconds = float(seconds)
        self.peak_rss_bytes = 0
        self.hit_reason: str | None = None

    @staticmethod
    def rss_bytes() -> int:
        try:
            with open("/proc/self/status", "r", encoding="ascii") as stream:
                for line in stream:
                    if line.startswith("VmRSS:"):
                        return int(line.split()[1])*1024
        except (OSError, ValueError, IndexError):
            pass
        if resource is None:
            return 0
        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        return value if sys.platform == "darwin" else value*1024

    def check(self, phase: str, *, force: bool = False,
              ordinal: int = 0, tuple_value: Sequence[int] = ()) -> None:
        self.checks += 1
        if force or (self.checks & 63) == 0:
            rss = self.rss_bytes()
            self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
            if rss >= CAPS["producer_soft_rss_bytes"]:
                self.hit_reason = "producer_soft_rss_bytes"
                raise ResourceStop(
                    self.hit_reason, cap_key=self.hit_reason,
                    cap_limit=CAPS[self.hit_reason], observed_count=rss,
                    trigger_relation="ge", phase=phase, ordinal=ordinal,
                    tuple_value=tuple_value)
            if time.monotonic() >= self.deadline:
                self.hit_reason = "common_math_soft_deadline_seconds"
                raise ResourceStop(
                    self.hit_reason,
                    cap_key="common_math_soft_deadline_seconds",
                    cap_limit=CAPS["common_math_soft_deadline_seconds"],
                    observed_count=max(
                        CAPS["common_math_soft_deadline_seconds"],
                        int(time.monotonic() - self.started)),
                    trigger_relation="ge", phase=phase, ordinal=ordinal,
                    tuple_value=tuple_value,
                )

    def reserve(self, phase: str, additional_bytes: int) -> None:
        """Mirror the pinned prefix builder's fail-closed RSS reservation API."""
        require(isinstance(additional_bytes, int) and additional_bytes >= 0,
                "producer RSS reservation")
        self.checks += 1
        rss = self.rss_bytes()
        self.peak_rss_bytes = max(self.peak_rss_bytes, rss)
        attempted = rss + additional_bytes
        if attempted >= CAPS["producer_soft_rss_bytes"]:
            self.hit_reason = "producer_soft_rss_bytes"
            raise ResourceStop(
                self.hit_reason, cap_key=self.hit_reason,
                cap_limit=CAPS[self.hit_reason], observed_count=attempted,
                trigger_relation="ge", phase=phase)
        if time.monotonic() >= self.deadline:
            self.hit_reason = "common_math_soft_deadline_seconds"
            raise ResourceStop(
                self.hit_reason,
                cap_key="common_math_soft_deadline_seconds",
                cap_limit=CAPS["common_math_soft_deadline_seconds"],
                observed_count=max(
                    CAPS["common_math_soft_deadline_seconds"],
                    int(time.monotonic() - self.started)),
                trigger_relation="ge", phase=phase)

    def public(self) -> dict[str, Any]:
        return {
            "common_start_monotonic": self.started,
            "initial_remaining_seconds": self.initial_seconds,
            "elapsed_seconds": time.monotonic() - self.started,
            "checks": self.checks,
            "peak_rss_bytes": self.peak_rss_bytes,
            "hit_reason": self.hit_reason,
            "remaining_seconds": max(0.0, self.deadline-time.monotonic()),
        }


def load_pinned_module(path: Path, expected: str, name: str) -> Any:
    full = ROOT / path
    if not full.is_file():
        raise AffineInput(f"missing authenticated {path.as_posix()}")
    if digest_file(full) != expected:
        raise AffineInput(f"SHA drift {path.as_posix()}")
    spec = importlib.util.spec_from_file_location(name, full)
    if spec is None or spec.loader is None:
        raise AffineInput(f"import spec {path.as_posix()}")
    module = importlib.util.module_from_spec(spec)
    if name in sys.modules:
        raise AffineInput(f"authenticated module name already bound: {name}")
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if sys.modules.get(name) is module:
            del sys.modules[name]
        raise
    return module


def authenticated_input(q3_path: Path) -> tuple[Any, Any]:
    if q3_path.resolve() != (ROOT / Q3_ARTIFACT).resolve():
        raise AffineInput("q3 artifact path drift")
    if not q3_path.is_file() or digest_file(q3_path) != Q3_ARTIFACT_SHA:
        raise AffineInput("q3 artifact SHA drift")
    for path, sha in (
        (OLD_PRODUCER, OLD_PRODUCER_SHA), (OLD_CHECKER, OLD_CHECKER_SHA),
        (OLD_DRIVER, OLD_DRIVER_SHA), (OLD_TASK, OLD_TASK_SHA),
        (STRONG_SOURCE, STRONG_SHA), (Q3_PRODUCER, Q3_PRODUCER_SHA),
        (Q3_CHECKER, Q3_CHECKER_SHA), (Q3_DRIVER, Q3_DRIVER_SHA),
        (EB_PRODUCER, EB_PRODUCER_SHA), (EB_CHECKER, EB_CHECKER_SHA),
        (EB_DRIVER, EB_DRIVER_SHA),
    ):
        if not (ROOT / path).is_file() or digest_file(ROOT / path) != sha:
            raise AffineInput(f"authenticated input drift: {path.as_posix()}")
    try:
        data = json.loads(q3_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AffineInput(f"q3 artifact JSON drift: {exc}") from exc
    if not isinstance(data, dict):
        raise AffineInput("q3 object schema")
    return data, load_pinned_module(
        OLD_PRODUCER, OLD_PRODUCER_SHA, "_d972_157ed_old_producer")


def pack_key(old: Any, key: int, pool: Any) -> tuple[int, bytes]:
    component, identifier = old.unpack_vector_key(key)
    return int(component), bytes(pool.blob(identifier))


def raw_public(old: Any, vector: dict[int, int], pool: Any) -> list[list[Any]]:
    rows = []
    for key, coefficient in vector.items():
        if coefficient % 3:
            component, blob = pack_key(old, key, pool)
            rows.append([component, blob.hex(), int(coefficient) % 3])
    rows.sort(key=lambda row: (row[0], bytes.fromhex(row[1])))
    return rows


def raw_digest(old: Any, vector: dict[int, int], pool: Any) -> str:
    return digest_obj(raw_public(old, vector, pool))


def raw_column_bytes(rows: Sequence[Sequence[Any]], width: int) -> bytes:
    out = bytearray()
    for component, blob_hex, coefficient in rows:
        blob = bytes.fromhex(str(blob_hex))
        require(1 <= int(component) <= 6 and len(blob) == width and
                int(coefficient) in (1, 2), "raw column canonical encoding")
        out.append(int(component)); out.extend(blob); out.append(int(coefficient))
    return bytes(out)


def subtract_vectors(old: Any, left: dict[int, int],
                     right: dict[int, int]) -> dict[int, int]:
    out = dict(left)
    for key, value in right.items():
        old.add_scaled(out, {key: value}, -1)
    return out


class RawLambdaOracle:
    """Portable support-one functional keyed only by canonical E4 bytes."""

    def __init__(self, old: Any, prefix: dict[str, Any], qstar_blob: bytes,
                 monitor: Budget) -> None:
        self.old = old
        self.pool = prefix["pool"]
        self.basis = prefix["basis"]
        require(bytes(qstar_blob) == validate_qstar_label(
                    QSTAR_LABEL, self.pool.width),
                "qstar oracle label binding")
        self.qstar = (4, bytes(qstar_blob))
        self.values: dict[tuple[int, bytes], int] = {self.qstar: 1}
        self.queries = self.hits = self.misses = 0
        pivots_ascending = sorted(self.basis.rows,
                                  key=self.pool.pivot_order)
        pivot_semantic = [pack_key(old, key, self.pool)
                          for key in pivots_ascending]
        require(len(pivot_semantic) == len(set(pivot_semantic)) ==
                PREFIX_COUNTS["pivots"], "canonical pivot uniqueness")
        require(self.qstar not in set(pivot_semantic),
                "qstar unexpectedly pivot")
        tail_visits = 0
        for number, pivot in enumerate(reversed(pivots_ascending), 1):
            monitor.check("raw_lambda_reverse_dp")
            row_data = self.basis.rows[pivot]
            row = row_data[0] if isinstance(row_data, tuple) else row_data
            value = 0
            for key, coefficient in row.items():
                coefficient = int(coefficient) % 3
                require(coefficient in (0, 1, 2), "lambda coefficient field")
                if key == pivot:
                    require(coefficient == 1, "pivot coefficient")
                    continue
                tail_visits += 1
                if tail_visits > CAPS["raw_lambda_recursion_edges"]:
                    raise ResourceStop(
                        "raw_lambda_recursion_edges",
                        cap_key="raw_lambda_recursion_edges",
                        cap_limit=CAPS["raw_lambda_recursion_edges"],
                        observed_count=tail_visits, phase="raw_lambda_reverse_dp")
                require(self.pool.pivot_order(key) >
                        self.pool.pivot_order(pivot),
                        "lambda edge not strictly increasing")
                value = (value-coefficient*
                         self.values.get(pack_key(old, key, self.pool), 0)) % 3
            self.values[pack_key(old, pivot, self.pool)] = value
        require(tail_visits == PREFIX_COUNTS["row_tail_visits"],
                "lambda row-tail count")
        require(len(self.values) == CAPS["raw_lambda_oracle_entries"],
                "lambda oracle entry count")
        pivot_entries = [[component, blob.hex(), self.values[(component, blob)]]
                         for component, blob in pivot_semantic]
        semantic_entries = pivot_entries + [[4, qstar_blob.hex(), 1]]
        self.public = {
            "qstar": QSTAR_LABEL,
            "qstar_is_nonpivot": True,
            "entry_count": len(self.values),
            "pivot_table_entries": len(pivot_entries),
            "explicit_qstar_entries": 1,
            "recursion_edges": tail_visits,
            "semantic_sha256": digest_obj(semantic_entries),
            "semantic_order": "canonical pivots ascending, then qstar",
            "row_tail_visits": tail_visits,
            "pivot_count": len(self.basis.rows),
            "dependent_column_count": PREFIX_COUNTS["dependent_columns"],
            "algorithm": "reverse-canonical-pivot-dynamic-programming/v1",
            "canonical_key": "one-based component plus exact 154-byte E4 blob",
            "candidate_queries_never_interned": True,
        }

    def key(self, component: int, value: Any) -> tuple[int, bytes]:
        return int(component), bytes(self.old._element_blob(value))

    def lookup(self, component: int, value: Any) -> int:
        self.queries += 1
        answer = self.values.get(self.key(component, value))
        if answer is None:
            self.misses += 1
            return 0
        self.hits += 1
        return int(answer)

    def packed(self, vector: dict[int, int]) -> int:
        total = 0
        for key, coefficient in vector.items():
            if coefficient % 3:
                total = (total + int(coefficient)*
                         self.values.get(pack_key(
                             self.old, key, self.pool), 0)) % 3
        return total

    def sparse(self, vector: dict[Any, int]) -> int:
        total = 0
        for (component, value), coefficient in vector.items():
            if coefficient % 3:
                total = (total + int(coefficient)*
                         self.lookup(component, value)) % 3
        return total

    def accounting(self) -> dict[str, Any]:
        return {"queries": self.queries, "hits": self.hits,
                "misses": self.misses,
                "query_cache_entries": 0, "query_cache_evictions": 0,
                "cold_recomputations": self.misses}


def build_instrumented_prefix(old: Any, e4: Any, monitor: Budget,
                              raw_source_key: Sequence[Any]) -> tuple[
                                  dict[str, Any], list[dict[str, Any]]]:
    strong = load_pinned_module(STRONG_SOURCE, STRONG_SHA,
                                "_d972_157ed_strong_prefix")
    events: list[dict[str, Any]] = []
    original = old.SparseBoundaryBasis

    class InstrumentedBasis(original):  # type: ignore[misc,valid-type]
        def add_column(self, relator_index: int, translation_id: int,
                       section_node: int, translation_ordinal: int = 0) -> None:
            raw = old.translate_vector_packed(
                self.relator_columns[relator_index-1], translation_id, self.pool)
            before_columns = self.columns_seen
            before_dep = self.dependent_columns
            result = super().add_column(
                relator_index, translation_id, section_node,
                translation_ordinal=translation_ordinal)
            if self.dependent_columns > before_dep:
                rows = raw_public(old, raw, self.pool)
                encoded = raw_column_bytes(rows, e4.degree+e4.pc.n)
                derived_ordinal = before_columns//11+1
                require(int(translation_ordinal) == derived_ordinal,
                        "dependent translation ordinal binding")
                event = {
                    "schedule": ("BFS" if translation_ordinal <= 32768
                                 else "directed"),
                    "translation_ordinal": int(translation_ordinal),
                    "translation_blob": self.pool.blob(translation_id).hex(),
                    "relator_index": int(relator_index),
                    "raw_column": rows,
                    "support": len(raw),
                    "byte_length": len(encoded),
                    "sha256": digest_bytes(encoded),
                    "encoding": "component-u8|E4-blob-154|coefficient-u8",
                    "column_ordinal": int(before_columns + 1),
                }
                events.append(event)
            return result

    old.SparseBoundaryBasis = InstrumentedBasis
    try:
        r0 = old.word_substitute(
            old.embed_f2_pb3(old.hexagon_words(old.FIXED_WORD)[0]),
            old.cofaces(3)[0])
        prefix = strong.build_fresh_prefix(
            old, e4, r0, monitor, monitor.started)
    finally:
        old.SparseBoundaryBasis = original
    require(len(events) == 16, "dependent-event count")
    accounting = prefix["accounting"]
    require(accounting["columns"] == PREFIX_COUNTS["columns"] and
            accounting["pivots"] == PREFIX_COUNTS["pivots"] and
            accounting["dependent_columns"] == 16 and
            accounting["BFS_translations"] == 32768 and
            accounting["directed_translations"] == 207 and
            accounting["live_sparse_entries"] ==
                PREFIX_COUNTS["live_sparse_entries"],
            "fresh prefix counts")
    prefix["157ed_dependent_events"] = events
    prefix["157ed_prefix_bindings"] = {
        **PREFIX_COUNTS,
        "dependent_event_count": len(events),
        "event_sha256": digest_obj(events),
        "rounds_sha256": digest_obj(
            prefix["directed_surgery"]["stable_rounds_projection"]),
        "context_rows_sha256": None,
        "context_alias_sha256": None,
    }
    return prefix, events


def cube_words(old: Any, q3: dict[str, Any], e3: Any) -> tuple[
        list[list[int]], dict[int, int], list[dict[str, Any]]]:
    records = q3["correction_fibre"]["records"]
    require(len(records) == 27, "correction fibre count")
    require(sum(1 for row in records if not row["word"]) == 1 and
            not records[0]["word"], "unique empty correction record")
    cubes: list[list[int]] = []
    record_to_cube: dict[int, int] = {}
    seen: set[tuple[int, ...]] = set()
    for index, row in enumerate(records, 1):
        word = list(row["word"])
        if not word:
            continue
        cube = old.reduce_word(word + word + word)
        key = tuple(cube)
        require(key not in seen, "duplicate cube")
        seen.add(key)
        record_to_cube[index] = len(cubes)+1
        cubes.append(cube)
    require(len(cubes) == 26 and digest_obj(cubes) == CUBE_SHA,
            "cube manifest")
    require(sum(map(len, cubes)) == 9162, "cube total length")
    return cubes, record_to_cube, [
        {"cube_index": i+1, "record_index": r,
         "length": len(cubes[i-1]), "sha256": digest_obj(cubes[i-1])}
        for r, i in sorted(record_to_cube.items())
    ]


def context_dp(old: Any, e4: Any, cubes: list[list[int]]) -> tuple[
        list[tuple[Any, Any]], dict[str, int], dict[str, Any], list[list[Any]],
        list[list[Any]]]:
    contexts, aliases, public = old.cheap_context_registry(e4)
    require(len(contexts) == 31 and len(public["named_uses"]) == 46,
            "context cardinalities")
    values: list[list[Any]] = []
    for left, right in contexts:
        values.append([
            # Contexts are literal F2 pairs.  PB3 embedding [A12,A23] is
            # used only by the E3/coface target routes, never here.
            e4.eval(word, [left, right])
            for word in cubes
        ])
    pairs: list[list[Any]] = []
    for row in values:
        pairs.append([
            e4.mul(row[i], row[j]) for i in range(26) for j in range(26)
        ])
    public["context_rows_sha256"] = digest_obj(public["contexts"])
    public["named_use_mapping_sha256"] = digest_obj(public["named_uses"])
    public["target6_scalar_dp"] = {
        "substitutions": ["c", "b", "a"],
        "leaf_scalar_entries": 3*26,
        "pair_scalar_entries": 3*676,
        "per_typed_tuple_third_gradient_streams": 3,
        "retained_pair_gradients": False,
        "direct_canary_tuple_count": 3,
    }
    return contexts, aliases, public, values, pairs


def target_leaf_dp(old: Any, e4: Any, cubes: list[list[int]]) -> dict[str, Any]:
    z = old.inv_word(old.pp_words([[1], [2]]))
    mapping = old.cofaces(3)[0]

    def lift(word: list[int]) -> list[int]:
        return old.word_substitute(old.embed_f2_pb3(word), mapping)

    substitutions = {
        "a": lambda word: old.f2_substitute(word, [1], [2]),
        "b": lambda word: old.f2_substitute(word, [1], z),
        "c": lambda word: old.f2_substitute(word, [2], z),
    }
    result: dict[str, Any] = {}
    for name, operation in substitutions.items():
        vals: list[Any] = []
        grads: list[dict[int, int]] = []
        for cube in cubes:
            gradient, value = old.fox_gradient_without_sections(
                lift(operation(cube)), e4)
            vals.append(value)
            grads.append(gradient)
        pairs = [e4.mul(vals[i], vals[j])
                 for i in range(26) for j in range(26)]
        result[name] = {"values": vals, "gradients": grads,
                        "pair_values": pairs}
    r0 = lift(old.hexagon_words(old.FIXED_WORD)[0])
    fixed_c = lift(old.f2_substitute(old.FIXED_WORD, [2], z))
    result["outer"] = {
        "C": e4.eval(fixed_c), "h": e4.eval(r0),
        "mapping": mapping, "z": z,
    }
    return result


def stream_gradient(old: Any, e4: Any, row: dict[str, Any],
                    i: int, j: int, k: int) -> dict[int, int]:
    values = row["values"]
    grads = row["gradients"]
    out = dict(grads[i])
    old.add_scaled(out, old.translate_vector(grads[j], values[i], e4), 1)
    pair_value = row["pair_values"][i*26+j]
    old.add_scaled(out, old.translate_vector(grads[k], pair_value, e4), 1)
    return out


def pack_bits(flags: Sequence[bool]) -> bytes:
    out = bytearray((len(flags)+7)//8)
    for i, flag in enumerate(flags):
        if flag:
            out[i//8] |= 1 << (i % 8)
    return bytes(out)


def array_field(raw: bytes) -> dict[str, Any]:
    return {
        "base64": base64.b64encode(raw).decode("ascii"),
        "byte_length": len(raw), "sha256": digest_bytes(raw),
    }


def signed_word_bytes(word: Sequence[int]) -> bytes:
    require(all(int(letter) in (-2, -1, 1, 2) for letter in word),
            "signed F2 class alphabet")
    return bytes(int(letter) & 0xff for letter in word)


class WordClassRegistry:
    """First-occurrence exact signed-word classes with collision resolution."""

    def __init__(self, hash_function: Callable[[bytes], str] = digest_bytes) -> None:
        self.hash_function = hash_function
        self.buckets: dict[str, list[int]] = {}
        self.words: list[bytes] = []
        self.first: list[int] = []
        self.mapping: list[int] = []

    def add(self, word: Sequence[int], ordinal: int) -> int:
        raw = signed_word_bytes(word)
        key = self.hash_function(raw)
        found = None
        for identifier in self.buckets.get(key, []):
            if self.words[identifier-1] == raw:
                found = identifier
                break
        if found is None:
            require(len(self.words) < 65535, "class id width")
            found = len(self.words)+1
            self.words.append(raw); self.first.append(int(ordinal))
            self.buckets.setdefault(key, []).append(found)
        self.mapping.append(found)
        return found

    def packed(self) -> tuple[list[int], list[dict[str, Any]]]:
        mapping = list(self.mapping)
        metadata = [{"first_ordinal": self.first[index],
                     "length": len(word), "sha256": digest_bytes(word)}
                    for index, word in enumerate(self.words)]
        for identifier, row in enumerate(metadata, 1):
            require(mapping[row["first_ordinal"]-1] == identifier,
                    "class first occurrence binding")
        map_bytes = b"".join(struct.pack("<H", x) for x in mapping)
        first_bytes = b"".join(struct.pack("<H", x["first_ordinal"])
                               for x in metadata)
        length_bytes = b"".join(struct.pack("<I", x["length"])
                                for x in metadata)
        sha_bytes = b"".join(bytes.fromhex(x["sha256"])
                             for x in metadata)
        return mapping, [
            {"name": "tuple_to_class", "data": array_field(map_bytes),
             "decoded_digest": digest_obj(mapping), "width": 2,
             "endianness": "little", "count": len(mapping)},
            {"name": "class_first_ordinal", "data": array_field(first_bytes),
             "decoded_digest": digest_obj(
                 [x["first_ordinal"] for x in metadata]),
             "width": 2, "endianness": "little", "count": len(metadata)},
            {"name": "class_length", "data": array_field(length_bytes),
             "decoded_digest": digest_obj([x["length"] for x in metadata]),
             "width": 4, "endianness": "little", "count": len(metadata)},
            {"name": "class_sha256", "data": array_field(sha_bytes),
             "decoded_digest": digest_obj([x["sha256"] for x in metadata]),
             "width": 32, "endianness": "raw", "count": len(metadata)},
        ]


def triple_context_values(e4: Any, values: Sequence[Sequence[Any]],
                          pairs: Sequence[Sequence[Any]], i: int, j: int,
                          k: int) -> list[Any]:
    return [e4.mul(pairs[row][i*26+j], values[row][k])
            for row in range(len(values))]


def source_tuple_from_contexts(old: Any, e4: Any, aliases: dict[str, int],
                               base_values: Sequence[Any],
                               correction_values: Sequence[Any]) -> tuple[Any, ...]:
    """Evaluate the actual six marked-source DAG for f=f0*s."""
    def fvalue(name: str) -> Any:
        slot = aliases[name]-1
        return e4.mul(base_values[slot], correction_values[slot])

    ff = fvalue("source_ff"); g = fvalue("source_g")
    gs = fvalue("source_gs"); f1234 = fvalue("source_f1234")
    h = fvalue("source_h"); middle = fvalue("source_middle")
    marked = e4.generators
    product = lambda rows: old.quotient_product(e4, rows)
    return (
        marked[0],
        product([e4.inverse(g), marked[1], g]),
        product([e4.inverse(ff), e4.inverse(h), marked[2], h, ff]),
        product([e4.inverse(ff), marked[3], ff]),
        product([e4.inverse(ff), e4.inverse(middle), e4.inverse(gs),
                 marked[4], gs, middle, ff]),
        product([e4.inverse(f1234), marked[5], f1234]),
    )


def target6_quotient_value(old: Any, e4: Any, aliases: dict[str, int],
                           correction_values: Sequence[Any], outer: dict[str, Any]) -> Any:
    a = correction_values[aliases["hexagon_1_fxy_0"]-1]
    b = correction_values[aliases["hexagon_1_fxz_0"]-1]
    c = correction_values[aliases["hexagon_1_fyz_0"]-1]
    fixed_c, h = outer["C"], outer["h"]
    return old.quotient_product(e4, [
        fixed_c, c, e4.inverse(b), e4.inverse(fixed_c),
        h, a, e4.inverse(h),
    ])


def streamed_gradient_scalar(old: Any, e4: Any, oracle: RawLambdaOracle,
                             row: dict[str, Any], i: int, j: int, k: int,
                             outer: Any, coefficient: int = 1) -> int:
    """Apply outer translation and lambda termwise; retain no triple vector."""
    values, gradients = row["values"], row["gradients"]
    prefixes = (e4.identity, values[i], row["pair_values"][i*26+j])
    answer = 0
    for gradient, prefix in zip((gradients[i], gradients[j], gradients[k]),
                                prefixes):
        left = e4.mul(outer, prefix)
        for (component, value), term in gradient.items():
            translated = e4.mul(left, value)
            answer = (answer + coefficient*int(term)*
                      oracle.lookup(component, translated)) % 3
    return answer


def build_scalar_dp(old: Any, e4: Any, oracle: RawLambdaOracle,
                    row: dict[str, Any], outer: Any, coefficient: int,
                    monitor: Budget) -> dict[str, Any]:
    """Cache only scalar leaf/pair prefixes; never retain pair gradients."""
    values, gradients = row["values"], row["gradients"]
    leaf: list[int] = []
    for i in range(26):
        monitor.check("target6_scalar_leaf_dp")
        total = 0
        for (component, value), term in gradients[i].items():
            total = (total + coefficient*int(term)*
                     oracle.lookup(component, e4.mul(outer, value))) % 3
        leaf.append(total)
    pair: list[int] = []
    for i in range(26):
        for j in range(26):
            monitor.check("target6_scalar_pair_dp")
            left = e4.mul(outer, values[i]); total = leaf[i]
            for (component, value), term in gradients[j].items():
                total = (total + coefficient*int(term)*
                         oracle.lookup(component, e4.mul(left, value))) % 3
            pair.append(total)
    return {"leaf": leaf, "pair": pair, "outer": outer,
            "coefficient": coefficient}


def streamed_third_scalar(e4: Any, oracle: RawLambdaOracle,
                          row: dict[str, Any], scalar_dp: dict[str, Any],
                          i: int, j: int, k: int) -> int:
    left = e4.mul(scalar_dp["outer"], row["pair_values"][i*26+j])
    total = scalar_dp["pair"][i*26+j]
    for (component, value), term in row["gradients"][k].items():
        total = (total + scalar_dp["coefficient"]*int(term)*
                 oracle.lookup(component, e4.mul(left, value))) % 3
    return total


def target6_scalar(old: Any, e4: Any, oracle: RawLambdaOracle,
                   leaves: dict[str, Any], scalar_dps: dict[str, Any],
                   i: int, j: int, k: int) -> int:
    return sum(streamed_third_scalar(
        e4, oracle, leaves[name], scalar_dps[name], i, j, k)
        for name in ("c", "b", "a")) % 3


def public_remainder_coefficient(remainder: dict[tuple[int, str], int]) -> int:
    return int(remainder.get((4, QSTAR_LABEL[3]), 0)) % 3


def predecessor_target6_certificate(old: Any, e4: Any, seed_info: dict[str, Any],
                                    prefix: dict[str, Any], oracle: RawLambdaOracle,
                                    monitor: Budget) -> dict[str, Any]:
    """Freshly reconstruct the exact rank-54 predecessor and its dual."""
    require(len(seed_info["seed_words"]) == 108 and
            digest_obj(seed_info["old_seed_words"]) == OLD_SEED_SHA,
            "old108 seed manifest")
    mapping = old.cofaces(3)[0]
    r0 = old.word_substitute(
        old.embed_f2_pb3(old.hexagon_words(old.FIXED_WORD)[0]), mapping)
    base_raw, base_value = old.fox_gradient_without_sections(r0, e4)
    require(base_value == e4.identity, "target6 base quotient")
    anchors = prefix["base_source_key"]
    base_remainder = old._affine_probe_remainder(
        base_raw, prefix, anchors, monitor)
    require(len(base_remainder) == 184 and
            digest_obj(sorted(base_remainder.items())) == BASE_REMAINDER_SHA,
            "target6 base remainder")
    base_lambda = oracle.sparse(base_raw)
    require(base_lambda == public_remainder_coefficient(base_remainder) == 2,
            "target6 base lambda/sign")
    delta_rows: dict[tuple[int, str], dict[int, int]] = {}
    lambda_values: list[int] = []
    formula_rows: list[dict[str, Any]] = []
    live = len(base_remainder)
    for seed_index, seed in enumerate(seed_info["seed_words"], 1):
        monitor.check("predecessor_target6", force=(seed_index % 8 == 0))
        detail = old.affine_target6_formula(seed, e4, include_gradient=True)
        raw = detail.pop("_direct_gradient")
        require(detail.pop("_direct_value") == e4.identity and
                detail["formula_equals_direct"] is True,
                "target6 formula/direct predecessor")
        formula_rows.append(detail)
        remainder = old._affine_probe_remainder(raw, prefix, anchors, monitor)
        raw_value = oracle.sparse(raw)
        require(raw_value == public_remainder_coefficient(remainder),
                "raw lambda/direct NF predecessor")
        lambda_values.append(raw_value)
        live += len(remainder)
        for coordinate, coefficient in remainder.items():
            delta_rows.setdefault(coordinate, {})[seed_index-1] = coefficient
    require(digest_obj(lambda_values) == ALL108_ZERO_SHA and
            lambda_values == [0]*108, "all108 raw lambda annihilation")
    old104 = {coordinate: {index: value for index, value in row.items()
                            if index < 104}
              for coordinate, row in delta_rows.items()}
    require(old._affine_delta_matrix_rank(old104, 104) == 50,
            "old104 target6 rank")
    require(old._affine_delta_matrix_rank(delta_rows, 108) == 54,
            "full108 target6 rank")
    system = old.AffineSystem(108, coordinate_widths=(e4.degree, e4.pc.n))
    target = old._affine_target_row_transposed(
        system, base_remainder, delta_rows, 6, live, monitor,
        "hexagon_1_coface_0")
    dual = system.dual_public()
    require(target["coordinate_count"] == 33687 and
            target["delta_rank"] == 54 and target["constraint_rank"] == 54 and
            target["nullity"] == 54 and target["consistent"] is False and
            target["row_space_sha256"] == ROW_SPACE_SHA,
            "target6 predecessor matrix")
    require(live == 225579, "target6 predecessor live remainder entries")
    require(dual is not None, "missing predecessor dual")
    validate_qstar_dual(dual)
    block = {
        "fresh_reconstruction": True,
        "target_name": "hexagon_1_coface_0", "target_ordinal": 6,
        "coordinate_count": 33687, "old104_rank": 50,
        "full108_rank": 54, "variables": 108, "nullity": 54,
        "row_space_sha256": ROW_SPACE_SHA,
        "base_remainder_size": 184,
        "base_remainder_sha256": BASE_REMAINDER_SHA,
        "base_lambda": 2, "negative_base_lambda": 1,
        "all108_lambda_values": lambda_values,
        "all108_annihilation_sha256": digest_obj(lambda_values),
        "dual": dual,
        "formula_rows_sha256": digest_obj(formula_rows),
        "live_remainder_entries": live,
        "fixed_linear_argument": {
            "field": 3, "lambda_annihilates_fixed_prefix": True,
            "lambda_annihilates_old108": True,
            "lambda_of_negative_base": 1,
            "equation": "0=1 would follow from a registered affine solution",
            "no_generation_or_full_D2_inference": True,
        },
    }
    return block


def direct_nf_lambda(old: Any, raw: dict[Any, int], prefix: dict[str, Any],
                     oracle: RawLambdaOracle, monitor: Budget) -> int:
    remainder = old._affine_probe_remainder(
        raw, prefix, prefix["base_source_key"], monitor)
    direct = public_remainder_coefficient(remainder)
    require(direct == oracle.sparse(raw), "raw lambda versus direct NF")
    return direct


def formula_canaries(old: Any, e4: Any, cubes: list[list[int]],
                     leaves: dict[str, Any], prefix: dict[str, Any],
                     oracle: RawLambdaOracle, seed_info: dict[str, Any],
                     typed_words: Sequence[Sequence[int]],
                     monitor: Budget) -> dict[str, Any]:
    generic: list[dict[str, Any]] = []
    z = leaves["outer"]["z"]; mapping = leaves["outer"]["mapping"]
    substitutions = {
        "a": lambda word: old.f2_substitute(word, [1], [2]),
        "b": lambda word: old.f2_substitute(word, [1], z),
        "c": lambda word: old.f2_substitute(word, [2], z),
    }
    for name, operation in substitutions.items():
        for index, cube in enumerate(cubes):
            monitor.check("generic_leaf_square_canaries")
            lifted = lambda word: old.word_substitute(
                old.embed_f2_pb3(operation(word)), mapping)
            direct_leaf, leaf_value = old.fox_gradient_without_sections(
                lifted(cube), e4)
            require(direct_leaf == leaves[name]["gradients"][index] and
                    leaf_value == leaves[name]["values"][index],
                    "generic leaf Fox canary")
            predicted_square = dict(direct_leaf)
            old.add_scaled(predicted_square,
                           old.translate_vector(direct_leaf, leaf_value, e4), 1)
            direct_square, square_value = old.fox_gradient_without_sections(
                lifted(cube+cube), e4)
            require(predicted_square == direct_square and
                    square_value == e4.mul(leaf_value, leaf_value),
                    "generic square Fox canary")
            leaf_lambda = direct_nf_lambda(
                old, direct_leaf, prefix, oracle, monitor)
            square_lambda = direct_nf_lambda(
                old, direct_square, prefix, oracle, monitor)
            generic.append({"substitution": name, "cube_index": index+1,
                            "leaf_value_sha256": digest_bytes(
                                old._element_blob(leaf_value)),
                            "square_value_sha256": digest_bytes(
                                old._element_blob(square_value)),
                            "leaf_lambda": leaf_lambda,
                            "square_lambda": square_lambda,
                            "product_law_equals_flat": True})
    triples: list[list[int]] = [[]] + [list(row)
        for row in seed_info["new_seed_words"]] + [list(row) for row in typed_words]
    triple_rows = []
    seen: set[tuple[int, ...]] = set()
    for word in triples:
        key = tuple(word)
        if key in seen:
            continue
        seen.add(key)
        detail = old.affine_target6_formula(word, e4, include_gradient=True)
        raw = detail.pop("_direct_gradient")
        require(detail.pop("_direct_value") == e4.identity and
                detail["formula_equals_direct"] is True,
                "triple target6 formula/direct canary")
        triple_rows.append({"word_sha256": digest_obj(word),
                            "raw_lambda": direct_nf_lambda(
                                old, raw, prefix, oracle, monitor),
                            "formula": detail})
    return {"generic_leaf_square_pair_count": len(generic),
            "generic_leaf_square_evaluation_count": 2*len(generic),
            "generic_rows_sha256": digest_obj(generic),
            "generic_rows": generic,
            "triple_count": len(triple_rows), "triple_rows": triple_rows,
            "triple_rows_sha256": digest_obj(triple_rows),
            "formula_drift_is_hard_failure": True,
            "source_DAG_replayed": True}


class ScanState:
    def __init__(self) -> None:
        self.typed: list[bool] = []
        self.lambdas: list[int] = []
        self.failures: list[int] = []
        self.classes = WordClassRegistry()
        self.first_active: dict[str, Any] | None = None
        self.first_typed_word: list[int] | None = None
        self.last_typed_word: list[int] | None = None
        self.counts = {"typed": 0, "scalar0": 0, "scalar1": 0,
                       "scalar2": 0,
                       "failures": {str(i): 0 for i in range(6)}}

    @property
    def evaluated(self) -> int:
        return len(self.typed)

    def commit(self, word: Sequence[int], typed: bool, scalar: int | None,
               failure: int, active: dict[str, Any] | None) -> None:
        ordinal = self.evaluated+1
        class_id = self.classes.add(word, ordinal)
        self.typed.append(bool(typed)); self.failures.append(int(failure))
        self.lambdas.append(255 if scalar is None else int(scalar))
        self.counts["failures"][str(failure)] += 1
        if typed:
            require(failure == 0 and scalar in (0, 1, 2),
                    "typed committed code")
            self.counts["typed"] += 1
            self.counts[f"scalar{scalar}"] += 1
            self.first_typed_word = (list(word) if self.first_typed_word is None
                                     else self.first_typed_word)
            self.last_typed_word = list(word)
        else:
            require(failure in range(1, 6) and scalar is None,
                    "untyped committed code")
        if active is not None and self.first_active is None:
            active = dict(active); active["class_id"] = class_id
            self.first_active = active


def census_public(state: ScanState, *, complete: bool) -> dict[str, Any]:
    n = state.evaluated
    mapping, metadata = state.classes.packed()
    typed_raw = pack_bits(state.typed)
    if n % 8:
        require(not (typed_raw[-1] & ~((1 << (n % 8))-1)),
                "typed mask zero padding")
    require(all((t and l in (0, 1, 2) and f == 0) or
                ((not t) and l == 255 and f in range(1, 6))
                for t, l, f in zip(state.typed, state.lambdas, state.failures)),
            "typed mask/code agreement")
    block = {
        "ordered_count": CAPS["ordered_triple_count"],
        "evaluated_prefix": n,
        "complete_scan": bool(complete),
        "last_ordinal": n,
        "typed_count": state.counts["typed"],
        "scalar_counts": {str(i): state.counts[f"scalar{i}"]
                          for i in range(3)},
        "failure_counts": dict(state.counts["failures"]),
        "typed_mask": {**array_field(typed_raw), "bit_order": "LSB_first",
                       "decoded_count": n, "unused_high_bits_zero": True},
        "lambda_codes": {**array_field(bytes(state.lambdas)),
                         "code_table": {"0": "scalar0", "1": "scalar1",
                                        "2": "scalar2", "255": "untyped"},
                         "decoded_count": n},
        "failure_codes": {**array_field(bytes(state.failures)),
                          "code_table": FAILURE_CODES,
                          "decoded_count": n},
        "class_arrays": metadata,
        "class_count": len(state.classes.words),
        "tuple_to_class_decoded_sha256": digest_obj(mapping),
        "array_layout_version": "typed-bit-lsb/lambda-u8/failure-u8/class-u16le/v1",
        "tuple_order": "i outer, j middle, k inner",
    }
    if complete:
        block["first_active"] = state.first_active
    else:
        block["provisional_first_active"] = state.first_active
        block["provisional_only"] = True
    return block


_BUDGET_KEYS = {
    "common_start_monotonic", "initial_remaining_seconds", "elapsed_seconds",
    "checks", "peak_rss_bytes", "hit_reason", "remaining_seconds",
}
_ARRAY_KEYS = {"base64", "byte_length", "sha256"}


def _expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError, KeyError, TypeError, OverflowError):
        return
    raise RuntimeError(f"mutation accepted: {label}")


def _decode_array(row: dict[str, Any], label: str) -> bytes:
    require(set(row) >= _ARRAY_KEYS and
            isinstance(row["base64"], str) and
            isinstance(row["byte_length"], int) and
            isinstance(row["sha256"], str), f"{label} array schema")
    raw = base64.b64decode(row["base64"], validate=True)
    require(len(raw) == row["byte_length"] and
            digest_bytes(raw) == row["sha256"], f"{label} array binding")
    return raw


def _validate_census_storage(block: dict[str, Any], *, complete: bool) -> None:
    common = {
        "ordered_count", "evaluated_prefix", "complete_scan", "last_ordinal",
        "typed_count", "scalar_counts", "failure_counts", "typed_mask",
        "lambda_codes", "failure_codes", "class_arrays", "class_count",
        "tuple_to_class_decoded_sha256", "array_layout_version",
        "tuple_order", "typed_dp_state_records", "oracle_accounting",
    }
    stage = ({"first_active"} if complete else
             {"provisional_first_active", "provisional_only"})
    require(set(block) == common | stage, "exact census nested schema")
    n = block["evaluated_prefix"]
    require(isinstance(n, int) and 0 <= n <= CAPS["ordered_triple_count"] and
            block["last_ordinal"] == n and
            block["ordered_count"] == CAPS["ordered_triple_count"] and
            block["complete_scan"] is complete and
            (not complete or n == CAPS["ordered_triple_count"]) and
            block["array_layout_version"] ==
                "typed-bit-lsb/lambda-u8/failure-u8/class-u16le/v1" and
            block["tuple_order"] == "i outer, j middle, k inner" and
            isinstance(block["typed_dp_state_records"], int) and
            0 <= block["typed_dp_state_records"] <=
                CAPS["typed_dp_state_records"], "census scalar envelope")
    mask_row = block["typed_mask"]
    require(set(mask_row) == _ARRAY_KEYS | {
                "bit_order", "decoded_count", "unused_high_bits_zero"} and
            mask_row["bit_order"] == "LSB_first" and
            mask_row["decoded_count"] == n and
            mask_row["unused_high_bits_zero"] is True,
            "typed-mask exact schema")
    mask = _decode_array(mask_row, "typed mask")
    require(len(mask) == (n+7)//8 and
            (n % 8 == 0 or not (mask[-1] & ~((1 << (n % 8))-1))),
            "typed-mask length/padding")
    typed = [bool(mask[i//8] & (1 << (i % 8))) for i in range(n)]
    lambda_row = block["lambda_codes"]
    failure_row = block["failure_codes"]
    require(set(lambda_row) == _ARRAY_KEYS | {"code_table", "decoded_count"}
            and lambda_row["code_table"] == {
                "0": "scalar0", "1": "scalar1", "2": "scalar2",
                "255": "untyped"} and lambda_row["decoded_count"] == n,
            "lambda-code exact schema")
    require(set(failure_row) == _ARRAY_KEYS | {"code_table", "decoded_count"}
            and failure_row["code_table"] == FAILURE_CODES and
            failure_row["decoded_count"] == n,
            "failure-code exact schema")
    lambdas = list(_decode_array(lambda_row, "lambda codes"))
    failures = list(_decode_array(failure_row, "failure codes"))
    require(len(lambdas) == len(failures) == n and all(
        (is_typed and scalar in (0, 1, 2) and failure == 0) or
        ((not is_typed) and scalar == 255 and failure in range(1, 6))
        for is_typed, scalar, failure in zip(typed, lambdas, failures)),
        "census decoded code agreement")
    typed_count = sum(typed)
    scalar_counts = {str(value): sum(1 for scalar in lambdas
                                     if scalar == value)
                     for value in range(3)}
    failure_counts = {str(value): failures.count(value) for value in range(6)}
    require(block["typed_count"] == typed_count and
            block["scalar_counts"] == scalar_counts and
            block["failure_counts"] == failure_counts,
            "census decoded counts")
    class_rows = block["class_arrays"]
    require(isinstance(class_rows, list) and len(class_rows) == 4,
            "class array cardinality")
    rows = {row["name"]: row for row in class_rows}
    require(len(rows) == 4 and set(rows) == {
                "tuple_to_class", "class_first_ordinal", "class_length",
                "class_sha256"}, "class array names")
    c = block["class_count"]
    require(isinstance(c, int) and 0 <= c <= min(n, 65535),
            "class count")
    layouts = {
        "tuple_to_class": (2, "little", n),
        "class_first_ordinal": (2, "little", c),
        "class_length": (4, "little", c),
        "class_sha256": (32, "raw", c),
    }
    decoded: dict[str, list[Any]] = {}
    for name, row in rows.items():
        width, endian, count = layouts[name]
        require(set(row) == {"name", "data", "decoded_digest", "width",
                             "endianness", "count"} and
                row["width"] == width and row["endianness"] == endian and
                row["count"] == count and
                set(row["data"]) == _ARRAY_KEYS, "class row exact schema")
        raw = _decode_array(row["data"], f"class {name}")
        require(len(raw) == width*count, "class row byte width")
        if name == "class_sha256":
            values = [raw[32*i:32*i+32].hex() for i in range(count)]
        else:
            code = "H" if width == 2 else "I"
            values = list(struct.unpack("<"+code*count, raw)) if count else []
        require(row["decoded_digest"] == digest_obj(values),
                "class row decoded digest")
        decoded[name] = values
    mapping = decoded["tuple_to_class"]
    first = decoded["class_first_ordinal"]
    first_seen: dict[int, int] = {}
    for ordinal, identifier in enumerate(mapping, 1):
        first_seen.setdefault(identifier, ordinal)
    require(block["tuple_to_class_decoded_sha256"] == digest_obj(mapping) and
            (not mapping or all(1 <= value <= c for value in mapping)) and
            len(first) == c and all(1 <= ordinal <= n for ordinal in first) and
            all(mapping[ordinal-1] == identifier and
                first_seen.get(identifier) == ordinal
                for identifier, ordinal in enumerate(first, 1)),
            "class first-occurrence binding")
    active_ordinals = [index+1 for index, (is_typed, scalar) in
                       enumerate(zip(typed, lambdas))
                       if is_typed and scalar in (1, 2)]
    active = (block["first_active"] if complete else
              block["provisional_first_active"])
    require((active is None) == (not active_ordinals),
            "first-active existence")
    if active is not None:
        expected_keys = {
            "ordinal", "tuple", "cube_indices", "record_positions",
            "reduced_length", "reduced_sha256", "scalar",
            "qstar_equation_coefficient", "typed_gate_code", "typed_gates",
            "source_tuple_sha256", "context_rows_sha256", "class_id",
        }
        ordinal = active_ordinals[0]
        require(set(active) == expected_keys and active["ordinal"] == ordinal and
                active["scalar"] == lambdas[ordinal-1] and
                active["class_id"] == mapping[ordinal-1],
                "canonical first-active binding")
    if not complete:
        require(block["provisional_only"] is True,
                "partial first-active nonclaim")
    account = block["oracle_accounting"]
    if account:
        require(set(account) == {"queries", "hits", "misses",
                    "query_cache_entries", "query_cache_evictions",
                    "cold_recomputations"} and
                account["queries"] == account["hits"]+account["misses"] and
                account["query_cache_entries"] == 0 and
                account["query_cache_evictions"] == 0 and
                account["cold_recomputations"] == account["misses"],
                "oracle accounting exact schema")


def _validate_budget(row: dict[str, Any], *, packed: bool) -> None:
    require(set(row) == _BUDGET_KEYS | ({"packed_receipt_bytes"} if packed
                                        else set()),
            "budget exact schema")
    require(isinstance(row["common_start_monotonic"], (int, float)) and
            0 < row["initial_remaining_seconds"] <=
                CAPS["common_math_soft_deadline_seconds"] and
            row["elapsed_seconds"] >= 0 and row["checks"] >= 0 and
            row["peak_rss_bytes"] >= 0 and row["remaining_seconds"] >= 0,
            "budget values")
    if packed:
        require(0 < row["packed_receipt_bytes"] <= CAPS["packed_receipt_bytes"],
                "packed receipt performance value")


def _validate_resource_stage(receipt: dict[str, Any], phase: str) -> None:
    if phase == "fresh_immutable_prefix":
        rank = 1
    elif phase in {"raw_lambda_oracle", "raw_lambda_reverse_dp"}:
        rank = 2
    elif phase == "predecessor_target6":
        rank = 3
    elif phase in {"target6_scalar_dp", "target6_scalar_leaf_dp",
                   "target6_scalar_pair_dp", "complete_ordered_census"}:
        rank = 4
    elif phase in {"formula_canaries", "generic_leaf_square_canaries"}:
        rank = 5
    elif phase == "receipt_serialization":
        rank = 6
    else:
        raise RuntimeError("unregistered resource phase")
    groups = [
        (1, ("base_q3_replay", "normalized_inverse_fibre", "cube_universe",
             "context_registry")),
        (2, ("directed_base_support", "directed_surgery", "prefix")),
        (3, ("lambda_oracle",)),
        (4, ("predecessor_target6",)),
        (6, ("formula_canaries",)),
    ]
    for minimum, names in groups:
        for name in names:
            require(bool(receipt[name]) is (rank >= minimum),
                    f"resource stage projection: {name}")


def receipt_schema(receipt: dict[str, Any]) -> dict[str, Any]:
    token = receipt["terminal_token"]
    require(digest_obj(UPSTREAM_RESOURCE_CAPS) == UPSTREAM_RESOURCE_CAPS_SHA,
            "upstream resource cap registry digest")
    common = {
        "schema", "task_sha256", "terminal_token", "status", "reason",
        "claim", "fixed_prefix_only", "pins", "caps", "base_q3_replay",
        "normalized_inverse_fibre", "directed_base_support",
        "directed_surgery", "prefix", "cube_universe", "context_registry",
        "predecessor_target6", "lambda_oracle", "formula_canaries",
        "census", "performance", "resource_guards", "theorem_boundary",
    }
    if token in {"B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE",
                 "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT"}:
        expected = common | {"claim_flags"}
    elif token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE":
        expected = common | {"claim_flags", "partial"}
    elif token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT":
        expected = common | {"claim_flags", "input_errors"}
    else:
        raise RuntimeError("unknown terminal")
    require(set(receipt) == expected and receipt["schema"] == SCHEMA and
            receipt["task_sha256"] == TASK_SHA and
            receipt["pins"] == receipt_pins(),
            "exact top-level receipt schema/pins")
    require(receipt["status"] == token and token in TERMINALS, "terminal binding")
    require(receipt["fixed_prefix_only"] is True, "fixed prefix claim")
    flags = receipt["claim_flags"]
    require(flags == {
        "full_D2_claimed": False, "full_H3_claimed": False,
        "all_depth3_claimed": False, "all_corrections_claimed": False,
        "literal_pair_claimed": False, "negative_global_claimed": False,
        "B4_A_claimed": False, "B4_B_claimed": False,
    }, "claim boundary")
    require(receipt["caps"] == CAPS and receipt["theorem_boundary"] == {
        "fixed_prefix_only": True, "full_D2_claimed": False,
        "full_H3_claimed": False, "all_depth3_claimed": False,
        "all_corrections_claimed": False, "literal_pair_claimed": False,
        "negative_global_claimed": False, "B4_A_claimed": False,
        "B4_B_claimed": False,
        "lambda_invariance_claimed_beyond_queried_translations": False,
    }, "theorem boundary")
    census = receipt["census"]
    if token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT":
        require(census == {} and set(receipt["input_errors"]) == {
                    "authenticated_external_input", "mathematical_scan_started"} and
                receipt["input_errors"]["mathematical_scan_started"] is False and
                receipt["claim"] == "none" and
                receipt["reason"] == receipt["input_errors"][
                    "authenticated_external_input"] and
                receipt["resource_guards"] == {},
                "input terminal schema")
        _validate_budget(receipt["performance"], packed=False)
    else:
        require(isinstance(census, dict) and
                census.get("evaluated_prefix") == census.get("last_ordinal") and
                0 <= census["evaluated_prefix"] <= 17576,
                "census committed prefix")
        complete = token in {
            "B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE",
            "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT"}
        require(census["complete_scan"] is complete and
                (not complete or census["evaluated_prefix"] == 17576),
                "terminal completeness")
        require((token == "B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE") ==
                (complete and census["first_active"] is not None) and
                (token == "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT") ==
                (complete and census["first_active"] is None),
                "terminal mechanical derivation")
        _validate_census_storage(census, complete=complete)
        if complete:
            expected_reason = ("complete_scan_nonzero_scalar" if
                               token.endswith("ACTIVE") else
                               "complete_scan_all_typed_scalars_zero")
            expected_claim = (
                "one_registered_typed_triple_direction_has_nonzero_qstar_scalar"
                if token.endswith("ACTIVE") else
                "qstar_annihilates_old108_and_all_typed_registered_triples_against_fixed_prefix")
            require(receipt["reason"] == expected_reason and
                    receipt["claim"] == expected_claim and
                    all(bool(receipt[name]) for name in (
                        "base_q3_replay","normalized_inverse_fibre",
                        "directed_base_support","directed_surgery","prefix",
                        "cube_universe","context_registry","lambda_oracle",
                        "predecessor_target6","formula_canaries")) and
                    set(receipt["resource_guards"]) == {
                        "caps", "budget", "resource_hit",
                        "upstream_resource_caps",
                        "upstream_resource_caps_sha256"} and
                    receipt["resource_guards"]["caps"] == CAPS and
                    receipt["resource_guards"]["upstream_resource_caps"] ==
                        UPSTREAM_RESOURCE_CAPS and
                    receipt["resource_guards"]
                        ["upstream_resource_caps_sha256"] ==
                        UPSTREAM_RESOURCE_CAPS_SHA and
                    receipt["resource_guards"]["resource_hit"] is False,
                    "complete terminal nested schema")
            _validate_budget(receipt["resource_guards"]["budget"], packed=False)
            _validate_budget(receipt["performance"], packed=True)
        else:
            partial = receipt["partial"]
            require(set(partial) == {"evaluated_prefix",
                        "last_committed_ordinal", "in_progress_tuple_absent",
                        "phase", "provisional_only", "resource",
                        "typed_count", "active_count", "oracle_query_count",
                        "committed_census_sha256"} and
                    partial["evaluated_prefix"] == census["evaluated_prefix"] and
                    partial["last_committed_ordinal"] == census["last_ordinal"] and
                    partial["in_progress_tuple_absent"] is True and
                    partial["provisional_only"] is True and
                    partial["typed_count"] == census["typed_count"] and
                    partial["active_count"] ==
                        census["scalar_counts"]["1"]+census["scalar_counts"]["2"] and
                    partial["oracle_query_count"] ==
                        (0 if not census["oracle_accounting"] else
                         census["oracle_accounting"]["queries"]) and
                    partial["committed_census_sha256"] == digest_obj(census) and
                    set(partial["resource"]) == {"cap_reason", "cap_key",
                        "cap_limit", "observed_count", "trigger_relation",
                        "phase", "current_ordinal", "current_tuple"} and
                    partial["phase"] == partial["resource"]["phase"] and
                    receipt["reason"] == partial["resource"]["cap_reason"] and
                    receipt["claim"] == "none", "resource partial exact schema")
            resource_row = partial["resource"]
            cap_key = resource_row["cap_key"]
            require((cap_key in CAPS) != (cap_key in UPSTREAM_RESOURCE_CAPS) and
                    resource_row["cap_reason"] == cap_key and
                    resource_row["cap_limit"] ==
                        (CAPS[cap_key] if cap_key in CAPS else
                         UPSTREAM_RESOURCE_CAPS[cap_key]) and
                    resource_row["trigger_relation"] in {"gt", "ge"} and
                    ((resource_row["trigger_relation"] == "gt" and
                      resource_row["observed_count"] > resource_row["cap_limit"])
                     or (resource_row["trigger_relation"] == "ge" and
                         resource_row["observed_count"] >= resource_row["cap_limit"])) and
                    isinstance(resource_row["current_tuple"], list),
                    "resource comparator")
            require(set(receipt["resource_guards"]) == {
                        "caps", "budget", "resource_hit", "reason",
                        "upstream_resource_caps",
                        "upstream_resource_caps_sha256"} and
                    receipt["resource_guards"]["caps"] == CAPS and
                    receipt["resource_guards"]["upstream_resource_caps"] ==
                        UPSTREAM_RESOURCE_CAPS and
                    receipt["resource_guards"]
                        ["upstream_resource_caps_sha256"] ==
                        UPSTREAM_RESOURCE_CAPS_SHA and
                    receipt["resource_guards"]["resource_hit"] is True and
                    receipt["resource_guards"]["reason"] == receipt["reason"],
                    "resource guard exact schema")
            _validate_budget(receipt["resource_guards"]["budget"], packed=False)
            _validate_budget(receipt["performance"], packed=False)
            require(receipt["performance"]["hit_reason"] == receipt["reason"] and
                    receipt["resource_guards"]["budget"] ==
                        receipt["performance"], "resource budget binding")
            _validate_resource_stage(receipt, partial["phase"])
    return receipt


def base_receipt(pins: dict[str, str], budget: Budget) -> dict[str, Any]:
    return {
        "schema": SCHEMA, "task_sha256": TASK_SHA,
        "terminal_token": "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE",
        "status": "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE",
        "reason": "initializing", "claim": "none",
        "fixed_prefix_only": True,
        "claim_flags": {
            "full_D2_claimed": False, "full_H3_claimed": False,
            "all_depth3_claimed": False, "all_corrections_claimed": False,
            "literal_pair_claimed": False, "negative_global_claimed": False,
            "B4_A_claimed": False, "B4_B_claimed": False,
        },
        "pins": pins, "caps": CAPS, "base_q3_replay": {},
        "normalized_inverse_fibre": {}, "directed_base_support": {},
        "directed_surgery": {}, "prefix": {},
        "cube_universe": {}, "context_registry": {},
        "predecessor_target6": {}, "lambda_oracle": {},
        "formula_canaries": {},
        "census": {}, "performance": budget.public(),
        "resource_guards": {}, "partial": {},
        "theorem_boundary": {
            "fixed_prefix_only": True, "full_D2_claimed": False,
            "full_H3_claimed": False, "all_depth3_claimed": False,
            "all_corrections_claimed": False, "literal_pair_claimed": False,
            "negative_global_claimed": False, "B4_A_claimed": False,
            "B4_B_claimed": False,
            "lambda_invariance_claimed_beyond_queried_translations": False,
        },
    }


def census(q3_path: Path, *, budget: Budget | None = None) -> dict[str, Any]:
    budget = budget or Budget()
    pins = receipt_pins()
    receipt = base_receipt(pins, budget)
    state = ScanState()
    phase = "authenticated_input"
    current_ordinal = 0
    current_tuple: list[int] = []
    old: Any = None
    oracle: RawLambdaOracle | None = None
    oracle_checkpoint: tuple[int,int,int] | None = None
    dp_states = 0
    try:
        q3, old = authenticated_input(q3_path)
        validate_upstream_cap_source(old)
        try:
            formula_sha = digest_obj(q3["formulas"])
        except (KeyError, TypeError, ValueError) as exc:
            raise AffineInput(f"q3 formula schema drift: {exc}") from exc
        if (q3.get("schema") != old.Q3_SCHEMA or
                q3.get("terminal_token") !=
                "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" or
                formula_sha != old.FORMULA_SHA or formula_sha != FORMULA_SHA):
            raise AffineInput("authenticated q3 schema/formula drift")
        e3, e4, _ = old.reconstruct_quotients(q3)
        receipt["base_q3_replay"] = old.replay_base_q3(q3, e3, e4)
        cubes, record_to_cube, cube_rows = cube_words(old, q3, e3)
        seed_info = old.affine_seed_words(q3, e3)
        require(len(seed_info["seed_words"]) == 108 and
                len(seed_info["new_seed_words"]) == 4,
                "registered predecessor seeds")
        normalized, raw_source_key, inverse_words = \
            old.normalized_inverse_fibre(q3, e4)
        receipt["normalized_inverse_fibre"] = normalized
        contexts, aliases, context_public, context_values, context_pairs = \
            context_dp(old, e4, cubes)
        require(context_public["context_rows_sha256"] == PREFIX_ROUNDS_SHA and
                context_public["named_use_mapping_sha256"] == CONTEXT_ALIAS_SHA,
                "context alias SHA")
        receipt["context_registry"] = context_public
        receipt["cube_universe"] = {
            "cube_count": 26, "cube_digest_sha256": digest_obj(cubes),
            "cube_rows": cube_rows,
            "record_to_cube": {str(k): v for k, v in record_to_cube.items()},
            "cube_total_reduced_letters": 9162,
            "ordered_pair_count": 676, "ordered_triple_count": 17576,
            "ordered_triple_unreduced_letters": 18580536,
            "ordered_product": "cube_i*cube_j*cube_k",
            "ordinal": "((i-1)*26+(j-1))*26+k",
            "repeated_indices_retained": True,
        }
        base_context_values = [e4.eval(old.FIXED_WORD, [left, right])
                               for left, right in contexts]
        identity_corrections = [e4.identity]*31
        require(source_tuple_from_contexts(
                    old, e4, aliases, base_context_values,
                    identity_corrections) == tuple(raw_source_key),
                "base marked source DAG")
        phase = "fresh_immutable_prefix"
        budget.check(phase, force=True)
        print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PHASE fresh_immutable_prefix",
              flush=True)
        prefix, dependent_events = build_instrumented_prefix(
            old, e4, budget, raw_source_key)
        pool = prefix["pool"]
        anchor_ids = tuple(prefix["base_source_key"])
        require(tuple(prefix["raw_source_tuple"]) == tuple(raw_source_key) and
                tuple(pool.value(identifier) for identifier in anchor_ids) ==
                    tuple(raw_source_key),
                "fresh prefix source anchors")
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        require(prefix["directed_surgery"]["stable_rounds_projection_sha256"] ==
                    PREFIX_STABLE_SHA and
                prefix["directed_surgery"]["translations_sha256"] ==
                    PREFIX_TRANSLATIONS_SHA and
                prefix["directed_surgery"]["columns_sha256"] ==
                    PREFIX_COLUMNS_SHA and
                prefix["directed_surgery"]["blocker_history_sha256"] ==
                    PREFIX_BLOCKERS_SHA,
                "fresh directed prefix semantic schedule")
        receipt["prefix"] = {
            "counts": PREFIX_COUNTS,
            "accounting": prefix["accounting"],
            "basis_gate": old.affine_basis_gate(prefix["basis"], pool),
            "prefix_pool_checkpoint": len(pool.values),
            "dependent_events": dependent_events,
            "dependent_event_count": len(dependent_events),
            "dependent_event_sha256": digest_obj(dependent_events),
            "fresh_not_imported": True,
            "source_sha256": STRONG_SHA,
        }
        qstar_blob = validate_qstar_label(QSTAR_LABEL, e4.degree+e4.pc.n)
        require(len(qstar_blob) == e4.degree+e4.pc.n == 154 and
                e4.degree == 144 and e4.pc.n == 10,
                "qstar canonical width")
        phase = "raw_lambda_oracle"
        budget.check(phase, force=True)
        print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PHASE raw_lambda_oracle",
              flush=True)
        oracle = RawLambdaOracle(old, prefix, qstar_blob, budget)
        pivot_zero = []
        for pivot in sorted(prefix["basis"].rows,
                            key=pool.pivot_order):
            row_data = prefix["basis"].rows[pivot]
            row = row_data[0] if isinstance(row_data, tuple) else row_data
            pivot_zero.append(oracle.packed(row))
        require(pivot_zero == [0]*PREFIX_COUNTS["pivots"],
                "pivot row lambda annihilation")
        dependent_zero = []
        for event in dependent_events:
            packed = {}
            for component, blob_hex, coefficient in event["raw_column"]:
                identifier = pool.ids.get(bytes.fromhex(blob_hex))
                require(identifier is not None, "dependent event pool binding")
                packed[old.pack_vector_key(component, identifier)] = coefficient
            remainder = old.affine_full_remainder(
                packed, prefix["basis"], pool, budget)
            value = oracle.packed(packed)
            require(not remainder and value == 0,
                    "dependent event annihilation")
            dependent_zero.append(value)
        require(dependent_zero == [0]*16,
                "dependent lambda vector")
        oracle.public.update({
            "pivot_annihilation_count": len(pivot_zero),
            "pivot_annihilation_sha256": digest_obj(pivot_zero),
            "dependent_annihilation_count": len(dependent_zero),
            "dependent_annihilation_sha256": digest_obj(dependent_zero),
        })
        receipt["lambda_oracle"] = oracle.public
        oracle_checkpoint = (oracle.queries,oracle.hits,oracle.misses)
        phase = "predecessor_target6"
        budget.check(phase, force=True)
        print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PHASE predecessor_target6",
              flush=True)
        predecessor = predecessor_target6_certificate(
            old, e4, seed_info, prefix, oracle, budget)
        receipt["predecessor_target6"] = predecessor
        oracle_checkpoint = (oracle.queries,oracle.hits,oracle.misses)
        leaves = target_leaf_dp(old, e4, cubes)
        dp_states = 31*(26+676) + 3*(26+676)
        phase = "target6_scalar_dp"
        budget.check(phase, force=True)
        scalar_dps = {
            "c": build_scalar_dp(old, e4, oracle, leaves["c"],
                                 leaves["outer"]["C"], 1, budget),
            "b": build_scalar_dp(old, e4, oracle, leaves["b"],
                                 leaves["outer"]["C"], -1, budget),
            "a": build_scalar_dp(old, e4, oracle, leaves["a"],
                                 leaves["outer"]["h"], 1, budget),
        }
        for i, j, k in ((0,0,0),(2,9,18),(25,25,25)):
            fast = target6_scalar(old,e4,oracle,leaves,scalar_dps,i,j,k)
            direct = (streamed_gradient_scalar(
                old,e4,oracle,leaves["c"],i,j,k,leaves["outer"]["C"],1)+
                streamed_gradient_scalar(
                old,e4,oracle,leaves["b"],i,j,k,leaves["outer"]["C"],-1)+
                streamed_gradient_scalar(
                old,e4,oracle,leaves["a"],i,j,k,leaves["outer"]["h"],1))%3
            require(fast == direct, "target6 scalar DP/direct canary")
        dp_states += 3*(26+676)
        oracle_checkpoint = (oracle.queries,oracle.hits,oracle.misses)
        record_by_cube = {cube: record for record, cube
                          in record_to_cube.items()}
        phase = "complete_ordered_census"
        budget.check(phase, force=True)
        print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PHASE complete_ordered_census",
              flush=True)
        for ordinal in range(1, CAPS["ordered_triple_count"]+1):
            zero = ordinal-1
            i, j, k = zero//676, (zero//26) % 26, zero % 26
            current_ordinal = ordinal; current_tuple = [i+1, j+1, k+1]
            budget.check(phase, force=(ordinal % 64 == 0),
                         ordinal=ordinal, tuple_value=current_tuple)
            s = old.reduce_word(cubes[i] + cubes[j] + cubes[k])
            correction_values = triple_context_values(
                e4, context_values, context_pairs, i, j, k)
            next_dp_states = dp_states+31
            if next_dp_states > CAPS["typed_dp_state_records"]:
                raise ResourceStop(
                    "typed_dp_state_records", cap_key="typed_dp_state_records",
                    cap_limit=CAPS["typed_dp_state_records"],
                    observed_count=next_dp_states, phase=phase, ordinal=ordinal,
                    tuple_value=current_tuple)
            code = 0
            gate_states: list[bool | None] = [None]*5
            source: tuple[Any, ...] | None = None
            gate_states[0] = old.exponent_sums(s, 2) == [0, 0]
            if not gate_states[0]:
                code = 1
            else:
                gate_states[1] = (e3.eval(old.embed_f2_pb3(s)) == e3.identity)
                if not gate_states[1]:
                    code = 2
                else:
                    source = source_tuple_from_contexts(
                        old, e4, aliases, base_context_values, correction_values)
                    gate_states[2] = source == tuple(raw_source_key)
                if gate_states[2] is False:
                    code = 3
                elif gate_states[2] is True:
                    named_values = [correction_values[
                        int(row["context_id"])-1]
                        for row in context_public["named_uses"]]
                    gate_states[3] = not (
                        any(value != e4.identity for value in correction_values) or
                        any(value != e4.identity for value in named_values))
                    if not gate_states[3]:
                        code = 4
                    else:
                        gate_states[4] = target6_quotient_value(
                            old, e4, aliases, correction_values,
                            leaves["outer"]) == e4.identity
                        if not gate_states[4]:
                            code = 5
            require(code == first_failure_code(gate_states),
                    "typed first-failure order")
            is_typed = code == 0
            scalar: int | None = None
            active = None
            if not is_typed:
                pass
            else:
                scalar = target6_scalar(
                    old, e4, oracle, leaves, scalar_dps, i, j, k)
                if scalar and state.first_active is None:
                    active = {
                    "ordinal": ordinal, "tuple": [i+1, j+1, k+1],
                    "cube_indices": [i+1, j+1, k+1],
                    "record_positions": [
                        record_by_cube[i+1], record_by_cube[j+1],
                        record_by_cube[k+1],
                    ],
                    "reduced_length": len(s),
                    "reduced_sha256": digest_bytes(signed_word_bytes(s)),
                    "scalar": scalar,
                    "qstar_equation_coefficient": 1 if scalar == 1 else 2,
                    "typed_gate_code": 0,
                    "typed_gates": {
                        "exponent_sums": [0, 0], "E3_identity": True,
                        "marked_source_tuple": True,
                        "all_31_contexts_identity": True,
                        "all_46_named_occurrences_identity": True,
                        "target6_actual_quotient_identity": True,
                    },
                    "source_tuple_sha256": digest_obj([
                        old._element_blob(value).hex() for value in source]),
                    "context_rows_sha256": context_public["context_rows_sha256"],
                }
            state.commit(s, is_typed, scalar, code, active)
            dp_states = next_dp_states + (3 if is_typed else 0)
            if ordinal % 256 == 0:
                print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PROGRESS " +
                      json.dumps({"ordinal": ordinal,
                                  "typed": state.counts["typed"],
                                  "scalar0": state.counts["scalar0"],
                                  "scalar1": state.counts["scalar1"],
                                  "scalar2": state.counts["scalar2"],
                                  "first_active": None if state.first_active is None
                                      else state.first_active["ordinal"],
                                  "oracle_queries": oracle.queries,
                                  "oracle_hits": oracle.hits,
                                  "oracle_misses": oracle.misses,
                                  "cache_entries": 0,
                                  "elapsed": budget.public()["elapsed_seconds"],
                                  "rss": budget.peak_rss_bytes}, sort_keys=True),
                      flush=True)
        require(dp_states <= CAPS["typed_dp_state_records"],
                "typed DP state cap")
        oracle_checkpoint = (oracle.queries,oracle.hits,oracle.misses)
        phase = "formula_canaries"
        budget.check(phase, force=True)
        print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PHASE formula_canaries",
              flush=True)
        typed_canaries = []
        if state.first_typed_word is not None:
            typed_canaries.append(state.first_typed_word)
            if state.last_typed_word != state.first_typed_word:
                typed_canaries.append(state.last_typed_word or [])
        canaries = formula_canaries(
            old, e4, cubes, leaves, prefix, oracle, seed_info,
            typed_canaries, budget)
        receipt["formula_canaries"] = canaries
        oracle_checkpoint = (oracle.queries,oracle.hits,oracle.misses)
        census_block = census_public(state, complete=True)
        census_block["typed_dp_state_records"] = dp_states
        census_block["oracle_accounting"] = oracle.accounting()
        receipt["census"] = census_block
        token = ("B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE"
                 if state.first_active is not None
                 else "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT")
        final_budget = budget.public()
        receipt.update({
            "terminal_token": token, "status": token,
            "reason": ("complete_scan_nonzero_scalar" if state.first_active
                       else "complete_scan_all_typed_scalars_zero"),
            "claim": ("one_registered_typed_triple_direction_has_nonzero_qstar_scalar"
                      if state.first_active else
                      "qstar_annihilates_old108_and_all_typed_registered_triples"
                      "_against_fixed_prefix"),
            "resource_guards": {
                "caps": CAPS, "budget": final_budget,
                "resource_hit": False,
                "upstream_resource_caps": UPSTREAM_RESOURCE_CAPS,
                "upstream_resource_caps_sha256": UPSTREAM_RESOURCE_CAPS_SHA,
            },
            "performance": dict(final_budget),
        })
        receipt.pop("partial", None)
        phase = "receipt_serialization"
        receipt["performance"]["packed_receipt_bytes"] = 1
        encoded_size = -1
        for _ in range(8):
            encoded_size = len(json.dumps(
                receipt, sort_keys=True, separators=(",", ":")).encode("utf-8"))+1
            if receipt["performance"]["packed_receipt_bytes"] == encoded_size:
                break
            receipt["performance"]["packed_receipt_bytes"] = encoded_size
        require(receipt["performance"]["packed_receipt_bytes"] == encoded_size,
                "packed receipt byte fixed point")
        if encoded_size > CAPS["packed_receipt_bytes"]:
            raise ResourceStop(
                "packed_receipt_bytes", cap_key="packed_receipt_bytes",
                cap_limit=CAPS["packed_receipt_bytes"],
                observed_count=encoded_size, phase="receipt_serialization",
                ordinal=state.evaluated)
        return receipt_schema(receipt)
    except ResourceStop as raw_stop:
        stop = normalize_resource_stop(raw_stop, phase)
        budget.hit_reason = stop.reason
        if oracle is not None and oracle_checkpoint is not None and stop.phase in {
                "predecessor_target6", "target6_scalar_dp",
                "target6_scalar_leaf_dp", "target6_scalar_pair_dp",
                "formula_canaries", "generic_leaf_square_canaries"}:
            oracle.queries,oracle.hits,oracle.misses = oracle_checkpoint
        receipt["terminal_token"] = receipt["status"] = \
            "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE"
        receipt["reason"] = stop.reason
        receipt["claim"] = "none"
        receipt["census"] = census_public(state, complete=False)
        receipt["census"]["typed_dp_state_records"] = dp_states
        receipt["census"]["oracle_accounting"] = (
            {} if oracle is None else oracle.accounting())
        receipt["partial"] = {
            "evaluated_prefix": state.evaluated,
            "last_committed_ordinal": state.evaluated,
            "in_progress_tuple_absent": True,
            "phase": stop.phase,
            "provisional_only": True, "resource": stop.public(),
            "typed_count": state.counts["typed"],
            "active_count": state.counts["scalar1"]+state.counts["scalar2"],
            "oracle_query_count": 0 if oracle is None else oracle.queries,
            "committed_census_sha256": digest_obj(receipt["census"]),
        }
        resource_budget = budget.public()
        receipt["resource_guards"] = {
            "caps": CAPS, "budget": resource_budget, "resource_hit": True,
            "reason": stop.reason,
            "upstream_resource_caps": UPSTREAM_RESOURCE_CAPS,
            "upstream_resource_caps_sha256": UPSTREAM_RESOURCE_CAPS_SHA,
        }
        receipt["performance"] = dict(resource_budget)
        return receipt_schema(receipt)
    except AffineInput as exc:
        receipt["terminal_token"] = receipt["status"] = \
            "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT"
        receipt["reason"] = str(exc)
        receipt["claim"] = "none"
        receipt["input_errors"] = {
            "authenticated_external_input": str(exc),
            "mathematical_scan_started": False,
        }
        receipt.pop("partial", None)
        return receipt_schema(receipt)
    except Exception as exc:
        if old is not None and isinstance(exc, getattr(old, "ResourceStop", ())):
            converted = convert_upstream_resource_stop(
                exc, phase, current_ordinal, current_tuple)
            budget.hit_reason = converted.reason
            if oracle is not None and oracle_checkpoint is not None and phase in {
                    "predecessor_target6", "target6_scalar_dp",
                    "formula_canaries"}:
                oracle.queries,oracle.hits,oracle.misses = oracle_checkpoint
            receipt["terminal_token"] = receipt["status"] = \
                "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE"
            receipt["reason"] = converted.reason; receipt["claim"] = "none"
            receipt["census"] = census_public(state, complete=False)
            receipt["census"]["typed_dp_state_records"] = dp_states
            receipt["census"]["oracle_accounting"] = (
                {} if oracle is None else oracle.accounting())
            receipt["partial"] = {
                "evaluated_prefix": state.evaluated,
                "last_committed_ordinal": state.evaluated,
                "in_progress_tuple_absent": True, "phase": converted.phase,
                "provisional_only": True, "resource": converted.public(),
                "typed_count": state.counts["typed"],
                "active_count": state.counts["scalar1"]+state.counts["scalar2"],
                "oracle_query_count": 0 if oracle is None else oracle.queries,
                "committed_census_sha256": digest_obj(receipt["census"])}
            resource_budget = budget.public()
            receipt["resource_guards"] = {
                "caps": CAPS, "budget": resource_budget,
                "resource_hit": True, "reason": converted.reason,
                "upstream_resource_caps": UPSTREAM_RESOURCE_CAPS,
                "upstream_resource_caps_sha256": UPSTREAM_RESOURCE_CAPS_SHA,
            }
            receipt["performance"] = dict(resource_budget)
            return receipt_schema(receipt)
        raise


def affine_self_test() -> None:
    # Nonabelian left-action/product-order canary: permutations in S3.
    e = (0, 1, 2)
    a = (1, 0, 2)
    b = (0, 2, 1)
    c = (2, 1, 0)

    def pmul(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(x[y[i]] for i in range(3))

    def act(g: tuple[int, ...], v: dict[str, int]) -> dict[str, int]:
        return {f"{g}:{key}": value % 3 for key, value in v.items()
                if value % 3}

    def prod(x: tuple[int, ...], dx: dict[str, int],
             y: tuple[int, ...], dy: dict[str, int]) -> tuple[
                 tuple[int, ...], dict[str, int]]:
        out = dict(dx)
        for key, value in act(x, dy).items():
            out[key] = (out.get(key, 0)+value) % 3
        return pmul(x, y), {key: value for key, value in out.items() if value}

    va, da = a, {"a": 1}
    vb, db = b, {"b": 1}
    vc, dc = c, {"c": 1}
    vab, dab = prod(va, da, vb, db)
    _, direct = prod(vab, dab, vc, dc)
    _, step = prod(vab, dab, vc, dc)
    require(direct == step and
            direct != {"a": 1, "b": 1, "c": 1},
            "nonabelian Fox action canary")
    require(digest_obj([1, 2, 3]) != digest_obj([1, 3, 2]),
            "tuple order canary")
    flags = [False]*27
    flags[0] = True; flags[26] = True
    packed = pack_bits(flags)
    require(len(packed) == 4 and packed[3] & 0x80 == 0,
            "packed padding canary")
    oracle = {(1, b"q"): 1, (1, b"p"): 2}
    require(oracle[(1, b"q")] == 1 and oracle.get((1, b"x"), 0) == 0,
            "nonpivot lambda canary")
    for code in FAILURE_CODES.values():
        require(code in range(6), "failure code closure")
    # Exact signed-word collision resolution and first-occurrence order.
    classes = WordClassRegistry(lambda _: "forced-collision")
    require([classes.add(word, n+1) for n, word in enumerate(
                ([1], [2], [1], [-1, -2]))] == [1, 2, 1, 3],
            "class collision canary")
    mapping, rows = classes.packed()
    require(mapping == [1, 2, 1, 3] and rows[3]["data"]["byte_length"] == 96,
            "class packed metadata canary")
    # Registered 3^3 lexicographic ordinal including repetitions.
    triples = [(i,j,k) for i in range(1,4) for j in range(1,4)
               for k in range(1,4)]
    require(len(triples) == 27 and triples[0] == (1,1,1) and
            triples[-1] == (3,3,3) and triples[13] == (2,2,2),
            "toy ordered triple universe")
    # The pure cube-order gate includes one empty record at position one,
    # retains repetitions, and rejects a changed first-occurrence order.
    def toy_cube_manifest(records: Sequence[Sequence[int]]) -> list[list[int]]:
        require(len(records) == 27 and sum(not row for row in records) == 1 and
                not records[0], "toy unique empty-record position")
        rows = [list(row)*3 for row in records[1:]]
        require(len(rows) == len({tuple(row) for row in rows}) == 26,
                "toy cube first-occurrence order")
        return rows
    toy_records = [[]] + [[1]*(index+1) for index in range(26)]
    toy_cubes = toy_cube_manifest(toy_records)
    toy_cube_digest = digest_obj(toy_cubes)
    _expect_failure(lambda: toy_cube_manifest(
        [toy_records[1], []]+toy_records[2:]), "empty record moved")
    reordered_records = [[]] + [toy_records[2], toy_records[1]] + toy_records[3:]
    require(digest_obj(toy_cube_manifest(reordered_records)) != toy_cube_digest,
            "toy cube order mutation")

    # Small semantic triangular prefix.  Reverse canonical recurrence and
    # direct normal form agree for every F3 vector; forward/numeric-id order,
    # recurrence cycles and stale rollback mappings are rejected.
    p, r, q = (1, b"p"), (1, b"r"), (1, b"q")
    pivot_order = [p, r]
    rows = {p: {p: 1, r: 1}, r: {r: 1, q: 2}}
    lambda_table = {q: 1}
    for pivot in reversed(pivot_order):
        row = rows[pivot]; require(row[pivot] == 1, "toy monic pivot")
        require(all(key == pivot or key not in pivot_order or
                    pivot_order.index(key) > pivot_order.index(pivot)
                    for key in row), "toy increasing recurrence")
        lambda_table[pivot] = (-sum(coefficient*lambda_table.get(key, 0)
                                    for key, coefficient in row.items()
                                    if key != pivot)) % 3
    require(lambda_table == {q: 1, r: 1, p: 2},
            "toy reverse lambda table")
    def toy_nf(vector: dict[tuple[int, bytes], int]) -> dict[tuple[int, bytes], int]:
        out = {key: value % 3 for key, value in vector.items() if value % 3}
        for pivot in pivot_order:
            coefficient = out.get(pivot, 0)
            if coefficient:
                for key, value in rows[pivot].items():
                    new = (out.get(key, 0)-coefficient*value) % 3
                    if new: out[key] = new
                    else: out.pop(key, None)
        return out
    for cp in range(3):
        for cr in range(3):
            for cq in range(3):
                vector = {p: cp, r: cr, q: cq}
                direct = toy_nf(vector).get(q, 0)
                recursive = sum(value*lambda_table[key]
                                for key, value in vector.items()) % 3
                require(direct == recursive, "toy lambda versus direct NF")
    forward = {q: 1}
    for pivot in pivot_order:
        forward[pivot] = (-sum(coefficient*forward.get(key, 0)
                               for key, coefficient in rows[pivot].items()
                               if key != pivot)) % 3
    require(forward != lambda_table, "forward recurrence mutation")
    numeric_ids = {p: 2, r: 1}
    require(sorted(pivot_order, key=numeric_ids.get) != pivot_order,
            "numeric pool-id order mutation")
    cycle_rows = copy.deepcopy(rows); cycle_rows[r][p] = 1
    _expect_failure(lambda: require(all(
        key == r or key not in pivot_order or
        pivot_order.index(key) > pivot_order.index(r)
        for key in cycle_rows[r]), "recurrence cycle"), "recurrence cycle")
    pool_values = [b"e", b"p"]; pool_ids = {blob: i for i, blob in
                                             enumerate(pool_values)}
    checkpoint = len(pool_values); pool_values.append(b"tmp"); pool_ids[b"tmp"] = 2
    removed = pool_values.pop(); require(pool_ids.get(removed) == 2,
                                        "rollback id binding")
    del pool_ids[removed]
    require(len(pool_values) == checkpoint and b"tmp" not in pool_ids,
            "rollback-id reuse cleanup")
    stale = dict(pool_ids); stale[b"tmp"] = 2
    _expect_failure(lambda: require(len(stale) == len(pool_values),
                                    "stale rollback id"),
                    "rollback-id reuse mutation")

    # One exact dependent raw column, including its canonical byte layout,
    # zero normal form and zero lambda.  Every registered field mutation is
    # rejected by the same encoding/recurrence primitives.
    dependent = {p: 1, r: 1}
    require(toy_nf(dependent) == {} and
            sum(value*lambda_table[key] for key, value in dependent.items()) % 3 == 0,
            "toy dependent NF/lambda")
    dep_rows = [[1, "0102", 1], [2, "0304", 2]]
    encoded = raw_column_bytes(dep_rows, 2)
    dep_event = {"translation_ordinal": 7, "relator_index": 2,
                 "raw_column": dep_rows, "sha256": digest_bytes(encoded)}
    require(dep_event["translation_ordinal"] == 7 and
            dep_event["relator_index"] == 2 and
            dep_event["sha256"] == digest_bytes(encoded),
            "toy dependent event")
    for mutation, label in [
        ([[0,"0102",1]], "component"), ([[1,"01",1]], "width"),
        ([[1,"0102",0]], "coefficient")]:
        _expect_failure(lambda mutation=mutation: raw_column_bytes(mutation, 2),
                        f"dependent {label}")
    _expect_failure(lambda: require(dep_event["translation_ordinal"] == 8,
                                    "translation ordinal"),
                    "dependent translation ordinal")
    _expect_failure(lambda: require(dep_event["relator_index"] == 3,
                                    "relator index"), "dependent relator")
    _expect_failure(lambda: require(toy_nf({p: 1}) == {}, "dependent NF"),
                    "dependent nonzero NF")
    _expect_failure(lambda: require(lambda_table[p] == 0, "dependent lambda"),
                    "dependent nonzero lambda")

    # Qstar label and support/sign normalization all flow through the same
    # production gates used by oracle and predecessor construction.
    validate_qstar_label(QSTAR_LABEL, 154)
    dual = {"equations": [{"label": QSTAR_LABEL, "coefficient": 1}],
            "support_count": 1, "support_sha256": QSTAR_SHA,
            "normalized_rhs": 1, "yTz_mod3": 2,
            "target_boundary": {"target_ordinals": [6]},
            "target6_fixed_prefix_functional": True}
    validate_qstar_dual(dual)
    qstar_mutations = []
    for key, value in [("support_count", 2), ("normalized_rhs", 2),
                       ("yTz_mod3", 1)]:
        bad = copy.deepcopy(dual); bad[key] = value; qstar_mutations.append(bad)
    bad = copy.deepcopy(dual); bad["equations"][0]["coefficient"] = 2
    qstar_mutations.append(bad)
    bad = copy.deepcopy(dual); bad["target_boundary"]["target_ordinals"] = [5]
    qstar_mutations.append(bad)
    for bad in qstar_mutations:
        _expect_failure(lambda bad=bad: validate_qstar_dual(bad),
                        "qstar dual mutation")
    for bad_label, width in [
        ([5, QSTAR_LABEL[1], 4, QSTAR_LABEL[3]], 154),
        ([6, "wrong", 4, QSTAR_LABEL[3]], 154),
        ([6, QSTAR_LABEL[1], 3, QSTAR_LABEL[3]], 154),
        ([6, QSTAR_LABEL[1], 4, "00"+QSTAR_LABEL[3][2:]], 154),
        (QSTAR_LABEL, 153)]:
        _expect_failure(lambda row=bad_label, width=width:
                        validate_qstar_label(row, width), "qstar label mutation")
    _expect_failure(lambda: require(q in pivot_order, "qstar pivot mutation"),
                    "qstar pivot")

    # Exact first-reason ordering; later gates are not evaluated after a fail.
    require(first_failure_code([True]*5) == 0, "typed gate pass")
    for index in range(5):
        gates: list[bool | None] = [True]*index+[False]+[None]*(4-index)
        require(first_failure_code(gates) == index+1,
                "typed first-reason fixture")
    _expect_failure(lambda: first_failure_code([False, True, None, None, None]),
                    "typed gate after first failure")

    # A bounded cache is acceleration only.  Capacity one forces eviction and
    # cold recomputation but has byte-identical answers to a roomy cache.
    def cached_answers(capacity: int) -> tuple[list[int], int, int]:
        cache: dict[int, int] = {}; order: list[int] = []
        evictions = cold = 0; answers = []
        for key in [0,1,2,0,3,1,4,0,2,4]:
            if key not in cache:
                cold += 1; value = (2*key+1) % 3
                if len(cache) >= capacity:
                    victim = order.pop(0); del cache[victim]; evictions += 1
                cache[key] = value; order.append(key)
            answers.append(cache[key])
        return answers, evictions, cold
    tiny = cached_answers(1); roomy = cached_answers(16)
    require(tiny[0] == roomy[0] and tiny[1] > 0 and tiny[2] > roomy[2],
            "cache capacity neutrality")

    # Production ScanState/census_public/receipt_schema are the sealed paths
    # for complete ACTIVE/INERT and committed-prefix RESOURCE fixtures.
    def active_record(ordinal: int, scalar: int) -> dict[str, Any]:
        zero = ordinal-1; i, j, k = zero//676, (zero//26)%26, zero%26
        return {"ordinal": ordinal, "tuple": [i+1,j+1,k+1],
                "cube_indices": [i+1,j+1,k+1],
                "record_positions": [i+2,j+2,k+2],
                "reduced_length": 2, "reduced_sha256": digest_bytes(b"\x01\xff"),
                "scalar": scalar,
                "qstar_equation_coefficient": 1 if scalar == 1 else 2,
                "typed_gate_code": 0,
                "typed_gates": {"exponent_sums": [0,0], "E3_identity": True,
                    "marked_source_tuple": True,
                    "all_31_contexts_identity": True,
                    "all_46_named_occurrences_identity": True,
                    "target6_actual_quotient_identity": True},
                "source_tuple_sha256": "0"*64,
                "context_rows_sha256": PREFIX_ROUNDS_SHA}
    def make_state(count: int, active_at: int | None = None) -> ScanState:
        result = ScanState()
        for ordinal in range(1, count+1):
            scalar = 1 if ordinal == active_at else (2 if
                     active_at is not None and ordinal == active_at+7 else 0)
            result.commit([1,-1], True, scalar, 0,
                          active_record(ordinal, scalar) if scalar else None)
        return result
    def complete_receipt(state: ScanState, token: str) -> dict[str, Any]:
        budget = Budget(60.0); row = base_receipt(receipt_pins(), budget)
        for name in ("base_q3_replay","normalized_inverse_fibre",
                     "directed_base_support","directed_surgery","prefix",
                     "cube_universe","context_registry","lambda_oracle",
                     "predecessor_target6","formula_canaries"):
            row[name] = {"fixture": name}
        block = census_public(state, complete=True)
        block["typed_dp_state_records"] = state.evaluated
        block["oracle_accounting"] = {"queries": 0, "hits": 0, "misses": 0,
            "query_cache_entries": 0, "query_cache_evictions": 0,
            "cold_recomputations": 0}
        snapshot = budget.public()
        row.update({"terminal_token": token, "status": token,
            "reason": "complete_scan_nonzero_scalar" if token.endswith("ACTIVE")
                      else "complete_scan_all_typed_scalars_zero",
            "claim": "one_registered_typed_triple_direction_has_nonzero_qstar_scalar"
                     if token.endswith("ACTIVE") else
                     "qstar_annihilates_old108_and_all_typed_registered_triples_against_fixed_prefix",
            "census": block,
            "resource_guards": {"caps": CAPS, "budget": snapshot,
                "resource_hit": False,
                "upstream_resource_caps": UPSTREAM_RESOURCE_CAPS,
                "upstream_resource_caps_sha256": UPSTREAM_RESOURCE_CAPS_SHA},
            "performance": {**snapshot, "packed_receipt_bytes": 1}})
        row.pop("partial", None)
        return receipt_schema(row)
    inert_state = make_state(17576)
    active_state = make_state(17576, 3)
    inert_receipt = complete_receipt(
        inert_state, "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT")
    active_receipt = complete_receipt(
        active_state, "B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE")
    require(active_receipt["census"]["first_active"]["ordinal"] == 3 and
            active_receipt["census"]["scalar_counts"]["2"] == 1 and
            inert_receipt["census"]["evaluated_prefix"] == 17576 and
            len(_decode_array(inert_receipt["census"]["lambda_codes"],
                              "zero-column ledger")) == 17576,
            "complete active/inert and lambda-zero ledger")
    for label, mutate in [
        ("terminal reason", lambda x: x.update({"reason": "wrong"})),
        ("terminal claim", lambda x: x.update({"claim": "wrong"})),
        ("terminal status", lambda x: x.update({"status": "wrong"})),
        ("pin", lambda x: x["pins"].update({"task_sha256": "0"*64})),
        ("upstream registry digest", lambda x: x["resource_guards"].update(
            {"upstream_resource_caps_sha256": "0"*64})),
        ("positive field", lambda x: x.update({"selected_solution": {}})),
        ("full claim", lambda x: x["claim_flags"].update(
            {"full_D2_claimed": True}))]:
        bad = copy.deepcopy(active_receipt); mutate(bad)
        _expect_failure(lambda bad=bad: receipt_schema(bad), label)
    for label, mutate in [
        ("tuple order", lambda x: x.update({"tuple_order": "permuted"})),
        ("first active", lambda x: x["first_active"].update({"ordinal": 10})),
        ("lambda omission", lambda x: x["lambda_codes"].update(
            {"byte_length": x["lambda_codes"]["byte_length"]-1})),
        ("class endian", lambda x: x["class_arrays"][0].update(
            {"endianness": "big"})),
        ("class first", lambda x: x["class_arrays"][1].update(
            {"decoded_digest": "0"*64})),
        ("class length", lambda x: x["class_arrays"][2].update(
            {"width": 2})),
        ("class hash", lambda x: x["class_arrays"][3].update(
            {"decoded_digest": "0"*64}))]:
        bad = copy.deepcopy(active_receipt["census"]); mutate(bad)
        _expect_failure(lambda bad=bad: _validate_census_storage(
            bad, complete=True), label)
    partial_padding = make_state(27)
    partial_block = census_public(partial_padding, complete=False)
    partial_block["typed_dp_state_records"] = 27
    partial_block["oracle_accounting"] = {}
    bad_padding = copy.deepcopy(partial_block)
    mask = bytearray(_decode_array(bad_padding["typed_mask"], "padding"))
    mask[-1] |= 0x80
    bad_padding["typed_mask"].update(array_field(bytes(mask)))
    _expect_failure(lambda: _validate_census_storage(
        bad_padding, complete=False), "typed padding")

    def resource_receipt(state: ScanState, stop: ResourceStop) -> dict[str, Any]:
        budget = Budget(60.0); budget.hit_reason = stop.reason
        row = base_receipt(receipt_pins(), budget)
        stage_rank = (1 if stop.phase == "fresh_immutable_prefix" else
                      2 if stop.phase in {"raw_lambda_oracle",
                                          "raw_lambda_reverse_dp"} else
                      3 if stop.phase == "predecessor_target6" else
                      4 if stop.phase == "complete_ordered_census" else
                      5 if stop.phase in {"formula_canaries",
                                          "generic_leaf_square_canaries"} else 6)
        for minimum, names in [
            (1,("base_q3_replay","normalized_inverse_fibre","cube_universe",
                "context_registry")),
            (2,("directed_base_support","directed_surgery","prefix")),
            (3,("lambda_oracle",)),(4,("predecessor_target6",)),
            (6,("formula_canaries",))]:
            if stage_rank >= minimum:
                for name in names: row[name] = {"fixture": name}
        block = census_public(state, complete=False)
        block["typed_dp_state_records"] = state.evaluated
        block["oracle_accounting"] = {}
        snapshot = budget.public()
        row.update({"reason": stop.reason, "claim": "none", "census": block,
            "partial": {"evaluated_prefix": state.evaluated,
                "last_committed_ordinal": state.evaluated,
                "in_progress_tuple_absent": True, "phase": stop.phase,
                "provisional_only": True, "resource": stop.public(),
                "typed_count": state.counts["typed"],
                "active_count": state.counts["scalar1"]+state.counts["scalar2"],
                "oracle_query_count": 0,
                "committed_census_sha256": digest_obj(block)},
            "resource_guards": {"caps": CAPS, "budget": snapshot,
                "resource_hit": True, "reason": stop.reason,
                "upstream_resource_caps": UPSTREAM_RESOURCE_CAPS,
                "upstream_resource_caps_sha256": UPSTREAM_RESOURCE_CAPS_SHA},
            "performance": dict(snapshot)})
        return receipt_schema(row)
    empty_state = ScanState(); mid_state = make_state(2)
    provisional_state = make_state(10, 3)
    resource_rows = [
        resource_receipt(empty_state, ResourceStop(
            "common_math_soft_deadline_seconds",
            cap_key="common_math_soft_deadline_seconds", cap_limit=18000,
            observed_count=18000, trigger_relation="ge",
            phase="fresh_immutable_prefix")),
        resource_receipt(empty_state, ResourceStop(
            "raw_lambda_recursion_edges", cap_key="raw_lambda_recursion_edges",
            cap_limit=CAPS["raw_lambda_recursion_edges"],
            observed_count=CAPS["raw_lambda_recursion_edges"]+1,
            phase="raw_lambda_reverse_dp")),
        resource_receipt(mid_state, ResourceStop(
            "typed_dp_state_records", cap_key="typed_dp_state_records",
            cap_limit=CAPS["typed_dp_state_records"],
            observed_count=CAPS["typed_dp_state_records"]+1,
            phase="complete_ordered_census", ordinal=3, tuple_value=[1,1,3])),
        resource_receipt(provisional_state, ResourceStop(
            "producer_soft_rss_bytes", cap_key="producer_soft_rss_bytes",
            cap_limit=CAPS["producer_soft_rss_bytes"],
            observed_count=CAPS["producer_soft_rss_bytes"],
            trigger_relation="ge", phase="complete_ordered_census",
            ordinal=11, tuple_value=[1,1,11])),
    ]
    require(resource_rows[-1]["census"]["provisional_first_active"][
                "ordinal"] == 3 and
            all(row["claim"] == "none" and
                row["partial"]["in_progress_tuple_absent"] is True
                for row in resource_rows), "resource committed-prefix fixtures")
    inner_stop = ResourceStop(
        "typed_dp_state_records", cap_key="typed_dp_state_records",
        cap_limit=CAPS["typed_dp_state_records"],
        observed_count=CAPS["typed_dp_state_records"]+1,
        phase="affine_transposed_row_absorption")
    normalized_stop = normalize_resource_stop(
        inner_stop, "predecessor_target6")
    require(normalized_stop.phase == "predecessor_target6" and
            normalized_stop.reason == inner_stop.reason and
            normalized_stop.cap_key == inner_stop.cap_key and
            normalized_stop.observed_count == inner_stop.observed_count,
            "resource inner-phase normalization")
    normalized_row = resource_receipt(empty_state, normalized_stop)
    require(normalized_row["partial"]["phase"] == "predecessor_target6",
            "resource normalized receipt phase")
    _expect_failure(lambda: resource_receipt(empty_state, inner_stop),
                    "resource unnormalized helper phase")
    class ToyUpstreamStop:
        reason = "affine_rows"
        cap_key = "affine_rows"
        cap_limit = 1_000_000
        observed_count = 1_000_001
        trigger_relation = "gt"
    converted_upstream = convert_upstream_resource_stop(
        ToyUpstreamStop(), "predecessor_target6", 0, ())
    upstream_row = resource_receipt(empty_state, converted_upstream)
    require(upstream_row["partial"]["resource"]["cap_key"] ==
                "affine_rows" and
            upstream_row["resource_guards"]["upstream_resource_caps_sha256"] ==
                UPSTREAM_RESOURCE_CAPS_SHA,
            "honest upstream UNKNOWN_RESOURCE fixture")
    unknown_upstream = ToyUpstreamStop()
    unknown_upstream.cap_key = unknown_upstream.reason = "unknown_old_cap"
    _expect_failure(lambda: convert_upstream_resource_stop(
        unknown_upstream, "predecessor_target6", 0, ()),
        "unknown upstream cap")
    stale_upstream = ToyUpstreamStop()
    stale_upstream.cap_limit = 999_999
    _expect_failure(lambda: convert_upstream_resource_stop(
        stale_upstream, "predecessor_target6", 0, ()),
        "stale upstream cap limit")
    wrong_reason_upstream = ToyUpstreamStop()
    wrong_reason_upstream.reason = "unknown_old_reason"
    _expect_failure(lambda: convert_upstream_resource_stop(
        wrong_reason_upstream, "predecessor_target6", 0, ()),
        "upstream reason/key drift")
    bad_resource = copy.deepcopy(resource_rows[2])
    bad_resource["partial"]["phase"] = "wrong"
    _expect_failure(lambda: receipt_schema(bad_resource),
                    "resource phase mutation")
    bad_resource = copy.deepcopy(resource_rows[2])
    bad_resource["resource_guards"]["budget"]["hit_reason"] = "wrong"
    _expect_failure(lambda: receipt_schema(bad_resource),
                    "resource budget mutation")
    bad_resource = copy.deepcopy(resource_rows[2])
    bad_resource["partial"]["resource"]["cap_reason"] = "unknown_reason"
    bad_resource["reason"] = "unknown_reason"
    bad_resource["resource_guards"]["reason"] = "unknown_reason"
    bad_resource["resource_guards"]["budget"]["hit_reason"] = "unknown_reason"
    bad_resource["performance"]["hit_reason"] = "unknown_reason"
    _expect_failure(lambda: receipt_schema(bad_resource),
                    "resource cap reason/key mutation")
    bad_resource = copy.deepcopy(resource_rows[0])
    bad_resource["formula_canaries"] = {"forged": True}
    _expect_failure(lambda: receipt_schema(bad_resource),
                    "resource future-stage payload mutation")

    # UNKNOWN_INPUT stays pre-mathematical and uses the same closed envelope.
    input_budget = Budget(60.0)
    input_receipt = base_receipt(receipt_pins(), input_budget)
    input_receipt.update({"terminal_token":
        "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT", "status":
        "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT", "reason": "fixture drift",
        "claim": "none", "census": {}, "resource_guards": {},
        "performance": input_budget.public(), "input_errors": {
            "authenticated_external_input": "fixture drift",
            "mathematical_scan_started": False}})
    input_receipt.pop("partial", None); receipt_schema(input_receipt)
    bad_input = copy.deepcopy(input_receipt)
    bad_input["input_errors"]["mathematical_scan_started"] = True
    _expect_failure(lambda: receipt_schema(bad_input), "input scan mutation")

    # Product/inverse/source-DAG orientation and direct/formula drift canaries.
    def pinv(value: tuple[int, ...]) -> tuple[int, ...]:
        out = [0]*len(value)
        for i, image in enumerate(value): out[image] = i
        return tuple(out)
    x, y = pmul(a, b), a
    correct_conjugate = pmul(pmul(pinv(x), y), x)
    wrong_conjugate = pmul(pmul(x, y), pinv(x))
    require(correct_conjugate != wrong_conjugate,
            "source DAG inverse/conjugation orientation")
    _expect_failure(lambda: require(correct_conjugate == wrong_conjugate,
                                    "deleted inverse source DAG"),
                    "source DAG mutation")
    direct_formula = {"value": pmul(pmul(a,b),c), "gradient": direct}
    bad_formula = {"value": pmul(pmul(a,c),b), "gradient": direct}
    require(direct_formula != bad_formula, "formula/direct hard-failure canary")
    _expect_failure(lambda: require(direct_formula == bad_formula,
                                    "formula drift"), "formula/direct mutation")
    require(signed_word_bytes([-1,-2]) == b"\xff\xfe" and
            signed_word_bytes([-1,-2]) != signed_word_bytes([1,2]),
            "negative-letter encoding")

    # Common-deadline arithmetic cannot reset a measured remainder to 18,000.
    producer_elapsed, overhead = 137, 3
    remaining = CAPS["common_math_soft_deadline_seconds"]-producer_elapsed-overhead
    remainder_budget = Budget(float(remaining))
    require(remainder_budget.initial_seconds == remaining and remaining < 18000,
            "common-deadline remainder")
    _expect_failure(lambda: Budget(18001.0), "common-deadline reset")
    reserve_checks = remainder_budget.checks
    remainder_budget.reserve("proof_DAG_array_bytes", 0)
    require(remainder_budget.checks == reserve_checks+1,
            "prefix monitor reserve compatibility")

    # Exercise the exact authenticated production import path.  Dataclasses
    # require their module to be registered in sys.modules during execution.
    pinned_name = "_d972_157ed_old_producer_selftest"
    pinned_old = load_pinned_module(OLD_PRODUCER, OLD_PRODUCER_SHA, pinned_name)
    require(hasattr(pinned_old, "AffineSystem") and
            hasattr(pinned_old, "affine_seed_words"),
            "authenticated predecessor import")
    require(sys.modules.get(pinned_name) is pinned_old,
            "authenticated predecessor module registration")
    toy_raw_anchors = ((b"a", b""), (b"b", b""))
    toy_values = [toy_raw_anchors[1], toy_raw_anchors[0]]
    toy_anchor_ids = (1, 0)
    require(tuple(toy_values[identifier] for identifier in toy_anchor_ids) ==
                toy_raw_anchors and tuple(toy_anchor_ids) != toy_raw_anchors,
            "prefix source anchor ID decoding")

    print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PRODUCER_SELFTEST_PASS "
          "cube_empty_order=1 fox_nonabelian=1 action_orientation=1 "
          "lambda_reverse_nf=1 lambda_mutations=1 qstar_mutations=1 "
          "first_reason=1 complete_active_inert=1 partial_resource=5 "
          "resource_phase_normalization=1 upstream_cap_registry=1 "
          "packed_classes=1 dependent_event=1 cache_neutrality=1 "
          "source_dag=1 formula_hard_fail=1 deadline_remainder=1 "
          "pinned_import=1 monitor_reserve=1 anchor_decode=1",
          flush=True)


def write_checked(path: Path, receipt: dict[str, Any]) -> None:
    encoded = (json.dumps(receipt, sort_keys=True, separators=(",", ":"))+
               "\n").encode("utf-8")
    if len(encoded) > CAPS["packed_receipt_bytes"]:
        raise RuntimeError("packed receipt exceeds registered cap")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name+f".tmp.{os.getpid()}")
    try:
        with temporary.open("wb") as stream:
            stream.write(encoded); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        require(path.read_bytes() == encoded, "checked receipt readback")
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv: Sequence[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if "--self-test" in args:
        affine_self_test()
        return 0
    q3 = Path(args[0]) if args else ROOT / Q3_ARTIFACT
    output = Path(args[1]) if len(args) > 1 else ROOT / OUTPUT
    seconds = float(args[2]) if len(args) > 2 else 18000.0
    receipt = census(q3, budget=Budget(seconds))
    write_checked(output, receipt)
    print(receipt["terminal_token"], flush=True)
    print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_PRODUCER_EXIT_ZERO", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
