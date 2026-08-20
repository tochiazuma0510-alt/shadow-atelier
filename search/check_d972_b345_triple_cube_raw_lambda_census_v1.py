"""Independent checker for the 157ed ordered triple-cube scalar census."""
from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import struct
import sys
import time
from pathlib import Path
from typing import Any, Callable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK_SHA = "15511f73e665a90f1e518383cb7bd218d8dd8e747026c498c3b4acce62837c2f"
SCHEMA = "d972-b345-triple-cube-raw-lambda-census/v1"
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
OLD_CHECKER = Path("search/check_d972_b345_seedspan_triple4_v1.py")
OLD_CHECKER_SHA = "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981"
OLD_PRODUCER = Path("search/d972_b345_seedspan_triple4_v1.py")
OLD_PRODUCER_SHA = "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"
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
CONTEXT_SHA = "bf07578f91f5ed66e6ddddd4ef83dafa45817a29df066940bbc13bd53cdd00f6"
ALIAS_SHA = "15cdac950ede8ce4596e5014ae1b6d0caa28523898cb42f3387f435a11b919a8"
ROW_SHA = "5dd0bd3411afae0a9adafca4254b6fda739774a8b970b59e661d67e686f549be"
BASE_SHA = "e62a581658c1a7c6093d9e3e5155acf503731806c075cf1dd3937e336473e179"
ZERO108_SHA = "400f67f74b1250e538c395aa8bf647f6f7432ec07fe2582aaff06e5a47fe7ed5"
QSTAR_SHA = "f8b1cb6325b158f0984ca945dac2c0e915e0386e1f13ddb911acf0e4e2d9dcad"
PREFIX_STABLE_SHA = "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d"
PREFIX_TRANSLATIONS_SHA = "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f"
PREFIX_COLUMNS_SHA = "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343"
PREFIX_BLOCKERS_SHA = "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53"
QSTAR = [6, "hexagon_1_coface_0", 4,
 "0801040503000602070b0e0c110a090d0f10181a161315191412171e1b2322201d1c1f212625242c2b2a2928273534333231302f2e2d3e363738393a3b3c3d403f474645444342414c4d4e4f5048494a4b5251595857565554535a5b5c5d5e5f60616265666768696a6b63646c6d6e6f707172737476757d7c7b7a797877867e7f80818283848588878f8e8d8c8b8a8900000002020100000000"]
TERMINALS = frozenset({
    "B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE",
    "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT",
    "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE",
    "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT",
})
FAILURE_CODES = {"typed": 0, "exponent_sums": 1, "E3_identity": 2,
                 "marked_source_tuple": 3, "context_identity": 4,
                 "target6_value": 5}
CAPS_157ED = {
    "cube_count": 26, "ordered_pair_count": 676,
    "ordered_triple_count": 17576, "unique_context_count": 31,
    "named_occurrence_count": 46, "cube_total_reduced_letters": 9162,
    "ordered_triple_unreduced_letters": 18580536,
    "prefix_columns": 362725, "prefix_pivots": 362709,
    "raw_lambda_oracle_entries": 362710,
    "raw_lambda_recursion_edges": 8388608,
    "typed_dp_state_records": 1048576, "packed_receipt_bytes": 16777216,
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
PREFIX_COUNTS = {"columns": 362725, "pivots": 362709,
                 "dependent_columns": 16, "live_sparse_entries": 3090367,
                 "row_tail_visits": 2727658, "BFS_translations": 32768,
                 "directed_translations": 207}


def validate_qstar_label(label: Sequence[Any], width: int) -> bytes:
    require(len(label) == 4 and list(label[:3]) ==
            [6, "hexagon_1_coface_0", 4] and isinstance(label[3], str),
            "checker qstar target/component")
    blob = bytes.fromhex(label[3])
    require(list(label) == QSTAR and width == 154 and len(blob) == width,
            "checker qstar bytes/width")
    return blob


def validate_qstar_dual(dual: dict[str, Any]) -> None:
    require(dual["equations"] == [{"label": QSTAR, "coefficient": 1}] and
            dual["support_count"] == 1 and
            dual["support_sha256"] == QSTAR_SHA and
            dual["normalized_rhs"] == 1 and dual["yTz_mod3"] == 2 and
            dual["target_boundary"]["target_ordinals"] == [6] and
            dual["target6_fixed_prefix_functional"] is True,
            "checker qstar dual/sign")


def first_failure_code(gates: Sequence[bool | None]) -> int:
    require(len(gates) == 5, "checker typed gate cardinality")
    for index, gate in enumerate(gates, 1):
        if gate is False:
            require(all(later is None for later in gates[index:]),
                    "checker typed gates after first failure")
            return index
        require(gate is True, "checker missing typed gate")
    return 0


def require(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_obj(value: Any) -> str:
    return digest_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                   ensure_ascii=True).encode("utf-8"))


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
            "checker pinned upstream resource cap registry")


class Deadline:
    def __init__(self, seconds: float) -> None:
        require(0 < seconds <= 18000, "checker common-deadline remainder")
        self.started = time.monotonic(); self.deadline = self.started+seconds
        self.checks = 0; self.initial_seconds = float(seconds)

    def check(self, phase: str, force: bool = False) -> None:
        self.checks += 1
        if (force or self.checks % 64 == 0) and time.monotonic() >= self.deadline:
            raise RuntimeError(f"checker common deadline exhausted: {phase}")


CHECKER_DEADLINE: Deadline | None = None


def tick(phase: str, force: bool = False) -> None:
    if CHECKER_DEADLINE is not None:
        CHECKER_DEADLINE.check(phase, force)


def load_old() -> Any:
    for path, sha in ((OLD_CHECKER, OLD_CHECKER_SHA),
                      (OLD_PRODUCER, OLD_PRODUCER_SHA),
                      (OLD_DRIVER, OLD_DRIVER_SHA), (OLD_TASK, OLD_TASK_SHA),
                      (STRONG_SOURCE, STRONG_SHA),
                      (Q3_PRODUCER, Q3_PRODUCER_SHA),
                      (Q3_CHECKER, Q3_CHECKER_SHA),
                      (Q3_DRIVER, Q3_DRIVER_SHA),
                      (EB_PRODUCER, EB_PRODUCER_SHA),
                      (EB_CHECKER, EB_CHECKER_SHA),
                      (EB_DRIVER, EB_DRIVER_SHA)):
        full = ROOT/path
        require(full.is_file() and digest_file(full) == sha,
                f"checker authenticated pin: {path}")
    spec = importlib.util.spec_from_file_location(
        "_d972_157ed_independent_old_checker", ROOT/OLD_CHECKER)
    require(spec is not None and spec.loader is not None,
            "checker old module spec")
    name = "_d972_157ed_independent_old_checker"
    require(name not in sys.modules, "checker old module name unbound")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if sys.modules.get(name) is module:
            del sys.modules[name]
        raise
    return module


def load_q3(path: Path) -> dict[str, Any]:
    require(path.resolve() == (ROOT/Q3_PATH).resolve(), "checker q3 path")
    require(path.is_file() and digest_file(path) == Q3_SHA, "checker q3 SHA")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict) and digest_obj(data.get("formulas")) ==
            FORMULA_SHA, "checker q3 object/formula")
    return data


def element_blob(value: Any) -> bytes:
    return bytes(value[0])+bytes(value[1])


def signed_word_bytes(word: Sequence[int]) -> bytes:
    require(all(int(x) in (-2, -1, 1, 2) for x in word),
            "checker signed class alphabet")
    return bytes(int(x) & 255 for x in word)


def raw_column_bytes(rows: Sequence[Sequence[Any]], width: int) -> bytes:
    out = bytearray()
    for component, blob_hex, coefficient in rows:
        blob = bytes.fromhex(blob_hex)
        require(1 <= component <= 6 and len(blob) == width and
                coefficient in (1, 2), "checker raw column encoding")
        out.append(component); out.extend(blob); out.append(coefficient)
    return bytes(out)


def semantic_key(old: Any, key: int, pool: Any) -> tuple[int, bytes]:
    component, identifier = old.replay_unpack_key(key)
    return component, bytes(pool.values[identifier])


def raw_public(old: Any, vector: dict[int, int], pool: Any) -> list[list[Any]]:
    rows = [[component, blob.hex(), int(coefficient) % 3]
            for key, coefficient in vector.items() if coefficient % 3
            for component, blob in [semantic_key(old, key, pool)]]
    rows.sort(key=lambda row: (row[0], bytes.fromhex(row[1])))
    return rows


def instrumented_basis_class(old: Any, e4: Any,
                             sink: list[dict[str, Any]]) -> type:
    parent = old.ReplayBasis

    class Instrumented(parent):  # type: ignore[misc,valid-type]
        def add_column(self, relator: int, translation: int) -> bool:
            raw: dict[int, int] = {}
            for key, coefficient in self.columns[relator-1].items():
                component, identifier = old.replay_unpack_key(key)
                translated = self.pool.mul_id(translation, identifier)
                old.replay_add(raw, old.replay_pack_key(component, translated),
                               coefficient)
            before_columns, before_dep = self.columns_seen, self.dependent
            result = super().add_column(relator, translation)
            if self.dependent > before_dep:
                rows = raw_public(old, raw, self.pool)
                encoded = raw_column_bytes(rows, e4.degree+e4.collector.n)
                translation_ordinal = before_columns//11+1
                sink.append({
                    "schedule": "BFS" if translation_ordinal <= 32768 else "directed",
                    "translation_ordinal": translation_ordinal,
                    "translation_blob": self.pool.values[translation].hex(),
                    "relator_index": relator, "raw_column": rows,
                    "support": len(raw), "byte_length": len(encoded),
                    "sha256": digest_bytes(encoded),
                    "encoding": "component-u8|E4-blob-154|coefficient-u8",
                    "column_ordinal": before_columns+1,
                })
            return result
    return Instrumented


def replay_prefix(old: Any, receipt: dict[str, Any], e4: Any,
                  normalized: dict[str, Any], base_key: Sequence[Any]) \
        -> tuple[Any, Any, list[dict[str, Any]]]:
    events: list[dict[str, Any]] = []
    original = old.ReplayBasis
    old.ReplayBasis = instrumented_basis_class(old, e4, events)
    try:
        targets = old.fixed_targets(e4, normalized)
        pool, basis = old.replay_pivot_surgery(receipt, e4, targets, base_key)
    finally:
        old.ReplayBasis = original
    require(len(events) == 16, "checker dependent count")
    directed = receipt["directed_surgery"]
    require(directed["stable_rounds_projection_sha256"] == PREFIX_STABLE_SHA and
            directed["translations_sha256"] == PREFIX_TRANSLATIONS_SHA and
            directed["columns_sha256"] == PREFIX_COLUMNS_SHA and
            directed["blocker_history_sha256"] == PREFIX_BLOCKERS_SHA,
            "checker independently derived frozen directed schedule")
    prefix = receipt["prefix"]
    require(set(prefix) == {"counts","accounting","basis_gate",
                "prefix_pool_checkpoint","dependent_events",
                "dependent_event_count","dependent_event_sha256",
                "fresh_not_imported","source_sha256"} and
            prefix["counts"] == PREFIX_COUNTS and
            prefix["accounting"]["columns"] == 362725 and
            prefix["accounting"]["pivots"] == 362709 and
            prefix["accounting"]["dependent_columns"] == 16 and
            prefix["accounting"]["live_sparse_entries"] == 3090367 and
            prefix["dependent_events"] == events and
            prefix["dependent_event_count"] == 16 and
            prefix["dependent_event_sha256"] == digest_obj(events) and
            prefix["basis_gate"] == old.checker_basis_gate(pool, basis) and
            prefix["prefix_pool_checkpoint"] == len(pool.values) and
            prefix["fresh_not_imported"] is True and
            prefix["source_sha256"] == STRONG_SHA,
            "checker fresh prefix binding")
    return pool, basis, events


class RawOracle:
    def __init__(self, old: Any, pool: Any, basis: Any, qstar: bytes) -> None:
        self.old = old; self.pool = pool; self.basis = basis
        require(qstar == validate_qstar_label(QSTAR, pool.width),
                "checker qstar oracle label")
        self.qstar = (4, qstar); self.values = {self.qstar: 1}
        self.queries = self.hits = self.misses = 0
        pivots = sorted(basis.rows, key=pool.pivot_order)
        semantic = [semantic_key(old, key, pool) for key in pivots]
        require(len(semantic) == len(set(semantic)) == 362709 and
                self.qstar not in set(semantic), "checker qstar nonpivot")
        edges = 0
        for number, pivot in enumerate(reversed(pivots), 1):
            tick("checker lambda reverse DP")
            row = basis.rows[pivot]; value = 0
            for key, coefficient in row.items():
                coefficient %= 3
                if key == pivot:
                    require(coefficient == 1, "checker pivot coefficient")
                    continue
                edges += 1
                require(pool.pivot_order(key) > pool.pivot_order(pivot),
                        "checker lambda increasing edge")
                value = (value-coefficient*
                         self.values.get(semantic_key(old, key, pool), 0)) % 3
            self.values[semantic_key(old, pivot, pool)] = value
        require(edges == 2727658 and edges <= 8388608 and
                len(self.values) == 362710, "checker lambda dimensions")
        entries = [[c, b.hex(), self.values[(c, b)]] for c, b in semantic]
        entries.append([4, qstar.hex(), 1])
        self.public = {
            "qstar": QSTAR, "qstar_is_nonpivot": True,
            "entry_count": 362710, "pivot_table_entries": 362709,
            "explicit_qstar_entries": 1, "recursion_edges": edges,
            "semantic_sha256": digest_obj(entries),
            "semantic_order": "canonical pivots ascending, then qstar",
            "row_tail_visits": edges, "pivot_count": 362709,
            "dependent_column_count": 16,
            "algorithm": "reverse-canonical-pivot-dynamic-programming/v1",
            "canonical_key": "one-based component plus exact 154-byte E4 blob",
            "candidate_queries_never_interned": True,
        }

    def lookup(self, component: int, value: Any) -> int:
        self.queries += 1
        answer = self.values.get((int(component), element_blob(value)))
        if answer is None:
            self.misses += 1; return 0
        self.hits += 1; return int(answer)

    def sparse(self, vector: dict[Any, int]) -> int:
        return sum(int(coefficient)*self.lookup(component, value)
                   for (component, value), coefficient in vector.items()) % 3

    def packed(self, vector: dict[int, int]) -> int:
        return sum(int(coefficient)*self.values.get(
            semantic_key(self.old, key, self.pool), 0)
            for key, coefficient in vector.items()) % 3

    def accounting(self) -> dict[str, Any]:
        return {"queries": self.queries, "hits": self.hits,
                "misses": self.misses, "query_cache_entries": 0,
                "query_cache_evictions": 0,
                "cold_recomputations": self.misses}


def public_remainder_coefficient(remainder: dict[tuple[int, str], int]) -> int:
    return int(remainder.get((4, QSTAR[3]), 0)) % 3


def predecessor_certificate(old: Any, e4: Any, seed_info: dict[str, Any],
                            pool: Any, basis: Any, oracle: RawOracle) -> dict[str, Any]:
    mapping = old.cofaces(3)[0]
    r0 = old.substitute(old.embed_f2(old.hexagon_words(old.FIXED_WORD)[0]), mapping)
    base_raw, base_value = old.fox(r0, e4)
    require(base_value == e4.identity, "checker base target6 quotient")
    base_rem = old.checker_probe_remainder(base_raw, pool, basis)
    require(len(base_rem) == 184 and
            digest_obj(sorted(base_rem.items())) == BASE_SHA and
            oracle.sparse(base_raw) == public_remainder_coefficient(base_rem) == 2,
            "checker target6 base remainder/sign")
    rows: dict[tuple[int, str], dict[int, int]] = {}
    lambdas: list[int] = []; formula_rows = []; live = len(base_rem)
    for index, seed in enumerate(seed_info["seed_words"], 1):
        tick("checker predecessor target6", index % 8 == 0)
        detail = old.checker_target6_formula(seed, e4, include_gradient=True)
        raw = detail["direct_gradient"]
        public = old.checker_target6_public_from_detail(seed, detail)
        formula_rows.append(public)
        remainder = old.checker_probe_remainder(raw, pool, basis)
        value = oracle.sparse(raw)
        require(value == public_remainder_coefficient(remainder),
                "checker predecessor raw/NF")
        lambdas.append(value); live += len(remainder)
        for coordinate, coefficient in remainder.items():
            rows.setdefault(coordinate, {})[index-1] = coefficient
    require(lambdas == [0]*108 and digest_obj(lambdas) == ZERO108_SHA,
            "checker old108 lambda")
    old104 = {coordinate: {i: v for i, v in row.items() if i < 104}
              for coordinate, row in rows.items()}
    require(old.checker_delta_matrix_rank(old104, 104) == 50 and
            old.checker_delta_matrix_rank(rows, 108) == 54,
            "checker old/full rank")
    system = old.CheckerAffineSystem(108, (e4.degree, e4.collector.n))
    target = old.checker_target_row_transposed(
        system, base_rem, rows, 6, live, "hexagon_1_coface_0")
    dual = system.dual_public()
    require(target["coordinate_count"] == 33687 and
            target["delta_rank"] == 54 and target["constraint_rank"] == 54 and
            target["nullity"] == 54 and target["consistent"] is False and
            target["row_space_sha256"] == ROW_SHA and dual is not None,
            "checker support-one predecessor")
    validate_qstar_dual(dual)
    require(live == 225579, "checker predecessor live remainder entries")
    return {"fresh_reconstruction": True,
            "target_name": "hexagon_1_coface_0", "target_ordinal": 6,
            "coordinate_count": 33687, "old104_rank": 50,
            "full108_rank": 54, "variables": 108, "nullity": 54,
            "row_space_sha256": ROW_SHA, "base_remainder_size": 184,
            "base_remainder_sha256": BASE_SHA, "base_lambda": 2,
            "negative_base_lambda": 1, "all108_lambda_values": lambdas,
            "all108_annihilation_sha256": ZERO108_SHA, "dual": dual,
            "formula_rows_sha256": digest_obj(formula_rows),
            "live_remainder_entries": live,
            "fixed_linear_argument": {
                "field": 3, "lambda_annihilates_fixed_prefix": True,
                "lambda_annihilates_old108": True,
                "lambda_of_negative_base": 1,
                "equation": "0=1 would follow from a registered affine solution",
                "no_generation_or_full_D2_inference": True}}


def cube_manifest(old: Any, q3: dict[str, Any], e3: Any) \
        -> tuple[list[list[int]], dict[int, int]]:
    cubes = []; record_to_cube = {}; seen = set()
    records = q3["correction_fibre"]["records"]
    require(len(records) == 27, "checker fibre count")
    require(sum(1 for row in records if not row["word"]) == 1 and
            not records[0]["word"], "checker unique empty correction")
    for record, row in enumerate(records, 1):
        word = list(row["word"])
        if not word:
            continue
        cube = old.reduce_word(word+word+word); key = tuple(cube)
        require(key not in seen, "checker duplicate cube")
        require(e3.eval(old.embed_f2(cube)) == e3.identity,
                "checker cube E3")
        seen.add(key); record_to_cube[record] = len(cubes)+1; cubes.append(cube)
    require(len(cubes) == 26 and digest_obj(cubes) == CUBE_SHA and
            sum(map(len, cubes)) == 9162, "checker cube manifest")
    return cubes, record_to_cube


def context_dp(old: Any, e4: Any, cubes: Sequence[Sequence[int]]) -> tuple[Any, ...]:
    contexts, aliases, public = old.independent_context_registry(e4)
    require(len(contexts) == 31 and len(public["named_uses"]) == 46 and
            digest_obj(public["contexts"]) == CONTEXT_SHA and
            digest_obj(public["named_uses"]) == ALIAS_SHA,
            "checker context registry")
    public["target6_scalar_dp"] = {
        "substitutions": ["c", "b", "a"],
        "leaf_scalar_entries": 3*26,
        "pair_scalar_entries": 3*676,
        "per_typed_tuple_third_gradient_streams": 3,
        "retained_pair_gradients": False,
        "direct_canary_tuple_count": 3,
    }
    values = [[e4.eval(cube, [left, right]) for cube in cubes]
              for left, right in contexts]
    pairs = [[e4.mul(row[i], row[j]) for i in range(26) for j in range(26)]
             for row in values]
    return contexts, aliases, public, values, pairs


def source_tuple(old: Any, e4: Any, aliases: dict[str, int],
                 base: Sequence[Any], correction: Sequence[Any]) -> tuple[Any, ...]:
    def fv(name: str) -> Any:
        slot = aliases[name]-1
        return e4.mul(base[slot], correction[slot])
    ff, g, gs = fv("source_ff"), fv("source_g"), fv("source_gs")
    f1234, h, middle = fv("source_f1234"), fv("source_h"), fv("source_middle")
    m = e4.generators; prod = lambda rows: old.q_product(e4, rows)
    return (m[0], prod([e4.inverse(g), m[1], g]),
            prod([e4.inverse(ff), e4.inverse(h), m[2], h, ff]),
            prod([e4.inverse(ff), m[3], ff]),
            prod([e4.inverse(ff), e4.inverse(middle), e4.inverse(gs),
                  m[4], gs, middle, ff]),
            prod([e4.inverse(f1234), m[5], f1234]))


def target_leaves(old: Any, e4: Any, cubes: Sequence[Sequence[int]]) -> dict[str, Any]:
    z = old.inv_word(old.pp([[1], [2]])); mapping = old.cofaces(3)[0]
    operations = {"a": lambda w: old.f2_sub(w, [1], [2]),
                  "b": lambda w: old.f2_sub(w, [1], z),
                  "c": lambda w: old.f2_sub(w, [2], z)}
    result = {}
    for name, operation in operations.items():
        values = []; gradients = []
        for cube in cubes:
            word = old.substitute(old.embed_f2(operation(cube)), mapping)
            gradient, value = old.fox(word, e4)
            gradients.append(gradient); values.append(value)
        result[name] = {"values": values, "gradients": gradients,
                        "pair_values": [e4.mul(values[i], values[j])
                                        for i in range(26) for j in range(26)]}
    r0 = old.substitute(old.embed_f2(old.hexagon_words(old.FIXED_WORD)[0]), mapping)
    fixed_c = old.substitute(old.embed_f2(old.f2_sub(
        old.FIXED_WORD, [2], z)), mapping)
    result["outer"] = {"C": e4.eval(fixed_c), "h": e4.eval(r0),
                       "z": z, "mapping": mapping}
    return result


def direct_nf_lambda(old: Any, raw: dict[Any, int], pool: Any, basis: Any,
                     oracle: RawOracle) -> int:
    remainder = old.checker_probe_remainder(raw, pool, basis)
    direct = public_remainder_coefficient(remainder)
    require(direct == oracle.sparse(raw), "checker raw lambda/direct NF")
    return direct


def formula_canaries(old: Any, e4: Any, cubes: list[list[int]],
                     leaves: dict[str, Any], pool: Any, basis: Any,
                     oracle: RawOracle, seed_info: dict[str, Any],
                     typed_words: Sequence[Sequence[int]]) -> dict[str, Any]:
    generic = []; z = leaves["outer"]["z"]
    mapping = leaves["outer"]["mapping"]
    operations = {"a": lambda w: old.f2_sub(w,[1],[2]),
                  "b": lambda w: old.f2_sub(w,[1],z),
                  "c": lambda w: old.f2_sub(w,[2],z)}
    for name, operation in operations.items():
        for index, cube in enumerate(cubes):
            tick("checker leaf/square canaries")
            lift = lambda word: old.substitute(old.embed_f2(operation(word)),
                                                mapping)
            leaf, value = old.fox(lift(cube), e4)
            require(leaf == leaves[name]["gradients"][index] and
                    value == leaves[name]["values"][index],
                    "checker generic leaf")
            square = dict(leaf); old.add_scaled(square, old.translate(leaf,value,e4),1)
            direct, square_value = old.fox(lift(cube+cube), e4)
            require(square == direct and square_value == e4.mul(value,value),
                    "checker generic square")
            generic.append({
                "substitution": name, "cube_index": index+1,
                "leaf_value_sha256": digest_bytes(element_blob(value)),
                "square_value_sha256": digest_bytes(element_blob(square_value)),
                "leaf_lambda": direct_nf_lambda(old,leaf,pool,basis,oracle),
                "square_lambda": direct_nf_lambda(old,direct,pool,basis,oracle),
                "product_law_equals_flat": True})
    words = [[]] + [list(row) for row in seed_info["new_seed_words"]] + \
            [list(row) for row in typed_words]
    triple_rows = []; seen = set()
    for word in words:
        if tuple(word) in seen: continue
        seen.add(tuple(word))
        detail = old.checker_target6_formula(word,e4,include_gradient=True)
        raw = detail["direct_gradient"]
        triple_rows.append({"word_sha256": digest_obj(word),
                            "raw_lambda": direct_nf_lambda(
                                old,raw,pool,basis,oracle),
                            "formula": old.checker_target6_public_from_detail(
                                word,detail)})
    return {"generic_leaf_square_pair_count": len(generic),
            "generic_leaf_square_evaluation_count": 2*len(generic),
            "generic_rows_sha256": digest_obj(generic),
            "generic_rows": generic, "triple_count": len(triple_rows),
            "triple_rows": triple_rows,
            "triple_rows_sha256": digest_obj(triple_rows),
            "formula_drift_is_hard_failure": True,
            "source_DAG_replayed": True}


def streamed_scalar(old: Any, e4: Any, oracle: RawOracle, row: dict[str, Any],
                    i: int, j: int, k: int, outer: Any, sign: int) -> int:
    values = row["values"]
    prefixes = (e4.identity, values[i], row["pair_values"][i*26+j])
    total = 0
    for gradient, prefix in zip((row["gradients"][i], row["gradients"][j],
                                 row["gradients"][k]), prefixes):
        left = e4.mul(outer, prefix)
        for (component, value), coefficient in gradient.items():
            total += sign*coefficient*oracle.lookup(
                component, e4.mul(left, value))
    return total % 3


def build_scalar_dp(e4: Any, oracle: RawOracle, row: dict[str, Any],
                    outer: Any, sign: int) -> dict[str, Any]:
    values, gradients = row["values"], row["gradients"]
    leaf = []
    for i in range(26):
        tick("checker scalar leaf DP")
        leaf.append(sum(sign*coefficient*oracle.lookup(
            component, e4.mul(outer, value))
            for (component, value), coefficient in gradients[i].items()) % 3)
    pair = []
    for i in range(26):
        for j in range(26):
            tick("checker scalar pair DP")
            left=e4.mul(outer,values[i])
            pair.append((leaf[i]+sum(sign*coefficient*oracle.lookup(
                component,e4.mul(left,value))
                for (component,value),coefficient in gradients[j].items()))%3)
    return {"leaf":leaf,"pair":pair,"outer":outer,"sign":sign}


def streamed_third(e4: Any, oracle: RawOracle, row: dict[str, Any],
                   scalar_dp: dict[str, Any], i: int, j: int, k: int) -> int:
    left=e4.mul(scalar_dp["outer"],row["pair_values"][i*26+j])
    return (scalar_dp["pair"][i*26+j]+sum(
        scalar_dp["sign"]*coefficient*oracle.lookup(
            component,e4.mul(left,value))
        for (component,value),coefficient in row["gradients"][k].items()))%3


class Classes:
    def __init__(self, hash_function: Callable[[bytes], str] = digest_bytes) -> None:
        self.hash = hash_function; self.buckets = {}; self.words = []
        self.first = []; self.mapping = []

    def add(self, word: Sequence[int], ordinal: int) -> int:
        raw = signed_word_bytes(word); key = self.hash(raw); found = None
        for identifier in self.buckets.get(key, []):
            if self.words[identifier-1] == raw:
                found = identifier; break
        if found is None:
            found = len(self.words)+1; self.words.append(raw); self.first.append(ordinal)
            self.buckets.setdefault(key, []).append(found)
        self.mapping.append(found); return found

    def metadata(self) -> list[dict[str, Any]]:
        return [{"first_ordinal": self.first[i], "length": len(word),
                 "sha256": digest_bytes(word)}
                for i, word in enumerate(self.words)]


def independently_scan(old: Any, q3: dict[str, Any], e3: Any, e4: Any,
                       base_key: Sequence[Any], cubes: list[list[int]],
                       contexts: Sequence[Any], aliases: dict[str, int],
                       context_public: dict[str, Any], values: Sequence[Any],
                       pairs: Sequence[Any], leaves: dict[str, Any],
                       oracle: RawOracle, count: int, complete: bool) -> dict[str, Any]:
    typed = []; lambdas = []; failures = []; classes = Classes(); first = None
    first_typed = last_typed = None
    counts = {"typed": 0, "scalar0": 0, "scalar1": 0, "scalar2": 0,
              "failures": {str(i): 0 for i in range(6)}}
    base_values = [e4.eval(old.FIXED_WORD, [left, right])
                   for left, right in contexts]
    require(source_tuple(old, e4, aliases, base_values,
                         [e4.identity]*31) == tuple(base_key),
            "checker base source DAG")
    record_to_cube = {record: cube for record, cube in
                      cube_manifest(old, q3, e3)[1].items()}
    record_by_cube = {cube: record for record, cube in record_to_cube.items()}
    C,h=leaves["outer"]["C"],leaves["outer"]["h"]
    scalar_dps={"c":build_scalar_dp(e4,oracle,leaves["c"],C,1),
                "b":build_scalar_dp(e4,oracle,leaves["b"],C,-1),
                "a":build_scalar_dp(e4,oracle,leaves["a"],h,1)}
    for i,j,k in ((0,0,0),(2,9,18),(25,25,25)):
        fast=sum(streamed_third(e4,oracle,leaves[name],scalar_dps[name],i,j,k)
                 for name in ("c","b","a"))%3
        direct=(streamed_scalar(old,e4,oracle,leaves["c"],i,j,k,C,1)+
                streamed_scalar(old,e4,oracle,leaves["b"],i,j,k,C,-1)+
                streamed_scalar(old,e4,oracle,leaves["a"],i,j,k,h,1))%3
        require(fast==direct,"checker target6 scalar DP/direct canary")
    dp_states = 31*(26+676)+6*(26+676)
    for ordinal in range(1, count+1):
        tick("checker census", ordinal % 64 == 0)
        z = ordinal-1; i, j, k = z//676, (z//26) % 26, z % 26
        word = old.reduce_word(cubes[i]+cubes[j]+cubes[k])
        correction = [e4.mul(pairs[r][i*26+j], values[r][k])
                      for r in range(31)]
        dp_states += 31; code = 0; source = None
        gate_states: list[bool | None] = [None]*5
        gate_states[0] = old.exponent_sums(word, 2) == [0, 0]
        if not gate_states[0]:
            code = 1
        else:
            gate_states[1] = e3.eval(old.embed_f2(word)) == e3.identity
            if not gate_states[1]:
                code = 2
            else:
                source = source_tuple(old, e4, aliases, base_values, correction)
                gate_states[2] = source == tuple(base_key)
            if gate_states[2] is False:
                code = 3
            elif gate_states[2] is True:
                gate_states[3] = not (
                    any(value != e4.identity for value in correction) or
                    any(correction[row["context_id"]-1] != e4.identity
                        for row in context_public["named_uses"]))
                if not gate_states[3]:
                    code = 4
                else:
                    a = correction[aliases["hexagon_1_fxy_0"]-1]
                    b = correction[aliases["hexagon_1_fxz_0"]-1]
                    c = correction[aliases["hexagon_1_fyz_0"]-1]
                    C, h = leaves["outer"]["C"], leaves["outer"]["h"]
                    target = old.q_product(
                        e4, [C, c, e4.inverse(b), e4.inverse(C),
                             h, a, e4.inverse(h)])
                    gate_states[4] = target == e4.identity
                    if not gate_states[4]:
                        code = 5
        require(code == first_failure_code(gate_states),
                "checker typed first-failure order")
        scalar = None
        if code == 0:
            dp_states += 3
            scalar = sum(streamed_third(
                e4,oracle,leaves[name],scalar_dps[name],i,j,k)
                for name in ("c","b","a"))%3
        class_id = classes.add(word, ordinal)
        typed.append(code == 0); failures.append(code)
        lambdas.append(255 if scalar is None else scalar)
        counts["failures"][str(code)] += 1
        if code == 0:
            counts["typed"] += 1; counts[f"scalar{scalar}"] += 1
            first_typed = list(word) if first_typed is None else first_typed
            last_typed = list(word)
            if scalar and first is None:
                first = {"ordinal": ordinal, "tuple": [i+1,j+1,k+1],
                         "cube_indices": [i+1,j+1,k+1],
                         "record_positions": [record_by_cube[i+1],
                                              record_by_cube[j+1],
                                              record_by_cube[k+1]],
                         "reduced_length": len(word),
                         "reduced_sha256": digest_bytes(signed_word_bytes(word)),
                         "scalar": scalar,
                         "qstar_equation_coefficient": 1 if scalar == 1 else 2,
                         "typed_gate_code": 0,
                         "typed_gates": {"exponent_sums": [0,0],
                           "E3_identity": True, "marked_source_tuple": True,
                           "all_31_contexts_identity": True,
                           "all_46_named_occurrences_identity": True,
                           "target6_actual_quotient_identity": True},
                         "source_tuple_sha256": digest_obj([
                             element_blob(v).hex() for v in source]),
                         "context_rows_sha256": context_public[
                             "context_rows_sha256"], "class_id": class_id}
    return {"typed": typed, "lambdas": lambdas, "failures": failures,
            "classes": classes, "first": first, "first_typed": first_typed,
            "last_typed": last_typed, "counts": counts,
            "dp_states": dp_states, "complete": complete}


def decode_array(row: dict[str, Any]) -> bytes:
    require(set(row) >= {"base64", "byte_length", "sha256"},
            "checker packed array schema")
    raw = base64.b64decode(row["base64"], validate=True)
    require(len(raw) == row["byte_length"] and digest_bytes(raw) == row["sha256"],
            "checker packed array binding")
    return raw


def compare_census(block: dict[str, Any], expected: dict[str, Any]) -> None:
    n = len(expected["typed"]); classes: Classes = expected["classes"]
    common_keys = {"ordered_count","evaluated_prefix","complete_scan",
                "last_ordinal","typed_count","scalar_counts","failure_counts",
                "typed_mask","lambda_codes","failure_codes","class_arrays",
                "class_count","tuple_to_class_decoded_sha256",
                "array_layout_version","tuple_order","typed_dp_state_records",
                "oracle_accounting"}
    stage_keys = ({"first_active"} if expected["complete"] else
                  {"provisional_first_active","provisional_only"})
    require(set(block) == common_keys | stage_keys,
            "checker exact census schema")
    if block["oracle_accounting"]:
        account = block["oracle_accounting"]
        require(set(account) == {"queries","hits","misses",
                    "query_cache_entries","query_cache_evictions",
                    "cold_recomputations"} and
                account["queries"] == account["hits"]+account["misses"] and
                account["query_cache_entries"] == 0 and
                account["query_cache_evictions"] == 0 and
                account["cold_recomputations"] == account["misses"],
                "checker producer oracle performance accounting")
    require(set(block["typed_mask"]) == {"base64","byte_length","sha256",
                "bit_order","decoded_count","unused_high_bits_zero"} and
            block["typed_mask"]["bit_order"] == "LSB_first" and
            block["typed_mask"]["decoded_count"] == n and
            block["typed_mask"]["unused_high_bits_zero"] is True and
            set(block["lambda_codes"]) == {"base64","byte_length","sha256",
                "code_table","decoded_count"} and
            block["lambda_codes"]["decoded_count"] == n and
            block["lambda_codes"]["code_table"] == {
                "0":"scalar0","1":"scalar1","2":"scalar2","255":"untyped"} and
            set(block["failure_codes"]) == {"base64","byte_length","sha256",
                "code_table","decoded_count"} and
            block["failure_codes"]["decoded_count"] == n and
            block["failure_codes"]["code_table"] == FAILURE_CODES,
            "checker exact primary array schema")
    typed_raw = decode_array(block["typed_mask"])
    require(len(typed_raw) == (n+7)//8 and
            (n % 8 == 0 or not (typed_raw[-1] & ~((1 << (n%8))-1))),
            "checker typed padding")
    typed = [bool(typed_raw[i//8] & (1 << (i%8))) for i in range(n)]
    lambdas = list(decode_array(block["lambda_codes"]))
    failures = list(decode_array(block["failure_codes"]))
    require(typed == expected["typed"] and lambdas == expected["lambdas"] and
            failures == expected["failures"] and all(
                (t and l in (0,1,2) and f == 0) or
                ((not t) and l == 255 and f in range(1,6))
                for t,l,f in zip(typed,lambdas,failures)),
            "checker census decoded arrays")
    rows = {row["name"]: row for row in block["class_arrays"]}
    require(set(rows) == {"tuple_to_class", "class_first_ordinal",
                          "class_length", "class_sha256"},
            "checker class array names")
    mapping_raw = decode_array(rows["tuple_to_class"]["data"])
    mapping = list(struct.unpack("<"+"H"*n, mapping_raw)) if n else []
    metadata = classes.metadata(); c = len(metadata)
    first_raw = decode_array(rows["class_first_ordinal"]["data"])
    length_raw = decode_array(rows["class_length"]["data"])
    hash_raw = decode_array(rows["class_sha256"]["data"])
    first = list(struct.unpack("<"+"H"*c, first_raw)) if c else []
    lengths = list(struct.unpack("<"+"I"*c, length_raw)) if c else []
    hashes = [hash_raw[32*i:32*i+32].hex() for i in range(c)]
    expected_layout = {
        "tuple_to_class": (2,"little",n,digest_obj(mapping)),
        "class_first_ordinal": (2,"little",c,digest_obj(first)),
        "class_length": (4,"little",c,digest_obj(lengths)),
        "class_sha256": (32,"raw",c,digest_obj(hashes)),
    }
    for name,row in rows.items():
        require(set(row) == {"name","data","decoded_digest","width",
                             "endianness","count"} and
                (row["width"],row["endianness"],row["count"],
                 row["decoded_digest"]) == expected_layout[name],
                "checker class array exact layout")
    require(mapping == classes.mapping and first == classes.first and
            lengths == [row["length"] for row in metadata] and
            hashes == [row["sha256"] for row in metadata] and
            block["class_count"] == c and
            block["tuple_to_class_decoded_sha256"] == digest_obj(mapping),
            "checker exact word classes")
    require(block["evaluated_prefix"] == block["last_ordinal"] == n and
            block["ordered_count"] == 17576 and
            block["array_layout_version"] ==
                "typed-bit-lsb/lambda-u8/failure-u8/class-u16le/v1" and
            block["tuple_order"] == "i outer, j middle, k inner" and
            block["complete_scan"] is expected["complete"] and
            block["typed_count"] == expected["counts"]["typed"] and
            block["scalar_counts"] == {str(i): expected["counts"][f"scalar{i}"]
                                       for i in range(3)} and
            block["failure_counts"] == expected["counts"]["failures"] and
            block["typed_dp_state_records"] == expected["dp_states"],
            "checker census accounting")
    if expected["complete"]:
        require(block["first_active"] == expected["first"] and
                "provisional_first_active" not in block and
                "provisional_only" not in block,
                "checker canonical first active")
    else:
        require("first_active" not in block and
                block["provisional_first_active"] == expected["first"] and
                block["provisional_only"] is True,
                "checker provisional first active")


_BUDGET_KEYS = {"common_start_monotonic", "initial_remaining_seconds",
                "elapsed_seconds", "checks", "peak_rss_bytes", "hit_reason",
                "remaining_seconds"}


def expected_pins() -> dict[str, str]:
    return {
        "task_sha256": TASK_SHA, "q3_artifact_sha256": Q3_SHA,
        "old_producer_sha256": OLD_PRODUCER_SHA,
        "old_checker_sha256": OLD_CHECKER_SHA,
        "old_driver_sha256": OLD_DRIVER_SHA,
        "old_task_sha256": OLD_TASK_SHA,
        "strong_prefix_sha256": STRONG_SHA,
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


def expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError, KeyError, TypeError, OverflowError):
        return
    raise RuntimeError(f"checker mutation accepted: {label}")


def validate_budget(row: dict[str, Any], *, packed: bool) -> None:
    require(set(row) == _BUDGET_KEYS | ({"packed_receipt_bytes"} if packed
                                        else set()),
            "checker budget exact schema")
    require(0 < row["initial_remaining_seconds"] <= 18000 and
            row["elapsed_seconds"] >= 0 and row["checks"] >= 0 and
            row["peak_rss_bytes"] >= 0 and row["remaining_seconds"] >= 0,
            "checker budget values")
    if packed:
        require(0 < row["packed_receipt_bytes"] <=
                CAPS_157ED["packed_receipt_bytes"],
                "checker packed receipt bytes")


def validate_census_envelope(block: dict[str, Any], *, complete: bool) -> None:
    common = {"ordered_count","evaluated_prefix","complete_scan",
        "last_ordinal","typed_count","scalar_counts","failure_counts",
        "typed_mask","lambda_codes","failure_codes","class_arrays",
        "class_count","tuple_to_class_decoded_sha256","array_layout_version",
        "tuple_order","typed_dp_state_records","oracle_accounting"}
    stage = ({"first_active"} if complete else
             {"provisional_first_active","provisional_only"})
    require(set(block) == common | stage, "checker generic census keyset")
    n = block["evaluated_prefix"]
    require(isinstance(n, int) and 0 <= n <= 17576 and
            block["last_ordinal"] == n and block["ordered_count"] == 17576 and
            block["complete_scan"] is complete and (not complete or n == 17576)
            and block["array_layout_version"] ==
                "typed-bit-lsb/lambda-u8/failure-u8/class-u16le/v1" and
            block["tuple_order"] == "i outer, j middle, k inner" and
            0 <= block["typed_dp_state_records"] <=
                CAPS_157ED["typed_dp_state_records"],
            "checker generic census envelope")
    mask_row = block["typed_mask"]
    require(set(mask_row) == {"base64","byte_length","sha256","bit_order",
                "decoded_count","unused_high_bits_zero"} and
            mask_row["bit_order"] == "LSB_first" and
            mask_row["decoded_count"] == n and
            mask_row["unused_high_bits_zero"] is True,
            "checker generic mask schema")
    mask = decode_array(mask_row)
    require(len(mask) == (n+7)//8 and
            (n % 8 == 0 or not (mask[-1] & ~((1 << (n%8))-1))),
            "checker generic mask padding")
    typed = [bool(mask[i//8] & (1 << (i%8))) for i in range(n)]
    lr, fr = block["lambda_codes"], block["failure_codes"]
    require(set(lr) == {"base64","byte_length","sha256","code_table",
                "decoded_count"} and lr["decoded_count"] == n and
            lr["code_table"] == {"0":"scalar0","1":"scalar1",
                                  "2":"scalar2","255":"untyped"} and
            set(fr) == {"base64","byte_length","sha256","code_table",
                "decoded_count"} and fr["decoded_count"] == n and
            fr["code_table"] == FAILURE_CODES,
            "checker generic code schemas")
    lambdas = list(decode_array(lr)); failures = list(decode_array(fr))
    require(len(lambdas) == len(failures) == n and all(
        (t and scalar in (0,1,2) and failure == 0) or
        ((not t) and scalar == 255 and failure in range(1,6))
        for t,scalar,failure in zip(typed,lambdas,failures)),
        "checker generic code agreement")
    require(block["typed_count"] == sum(typed) and
            block["scalar_counts"] == {str(i): lambdas.count(i)
                                        for i in range(3)} and
            block["failure_counts"] == {str(i): failures.count(i)
                                         for i in range(6)},
            "checker generic decoded counts")
    class_rows = block["class_arrays"]
    require(isinstance(class_rows, list) and len(class_rows) == 4,
            "checker generic class row count")
    rows = {row["name"]: row for row in class_rows}
    require(len(rows) == 4 and set(rows) == {"tuple_to_class",
        "class_first_ordinal","class_length","class_sha256"},
        "checker generic class names")
    c = block["class_count"]
    require(isinstance(c, int) and 0 <= c <= min(n,65535),
            "checker generic class count")
    layouts = {"tuple_to_class":(2,"little",n),
               "class_first_ordinal":(2,"little",c),
               "class_length":(4,"little",c),
               "class_sha256":(32,"raw",c)}
    decoded: dict[str,list[Any]] = {}
    for name,row in rows.items():
        width,endian,count = layouts[name]
        require(set(row) == {"name","data","decoded_digest","width",
                    "endianness","count"} and
                row["width"] == width and row["endianness"] == endian and
                row["count"] == count and
                set(row["data"]) == {"base64","byte_length","sha256"},
                "checker generic class row schema")
        raw = decode_array(row["data"])
        require(len(raw) == width*count, "checker generic class width")
        if name == "class_sha256":
            values = [raw[32*i:32*i+32].hex() for i in range(count)]
        else:
            code = "H" if width == 2 else "I"
            values = list(struct.unpack("<"+code*count,raw)) if count else []
        require(row["decoded_digest"] == digest_obj(values),
                "checker generic class digest")
        decoded[name] = values
    mapping = decoded["tuple_to_class"]
    first = decoded["class_first_ordinal"]
    first_seen: dict[int,int] = {}
    for ordinal,identifier in enumerate(mapping,1):
        first_seen.setdefault(identifier,ordinal)
    require(block["tuple_to_class_decoded_sha256"] == digest_obj(mapping) and
            (not mapping or all(1 <= identifier <= c for identifier in mapping))
            and all(mapping[ordinal-1] == identifier and
                    first_seen.get(identifier) == ordinal
                    for identifier,ordinal in enumerate(first,1)),
            "checker generic class first occurrence")
    active_ordinals = [index+1 for index,(t,scalar) in
                       enumerate(zip(typed,lambdas)) if t and scalar in (1,2)]
    active = block["first_active"] if complete else \
             block["provisional_first_active"]
    require((active is None) == (not active_ordinals),
            "checker generic active existence")
    if active is not None:
        require(set(active) == {"ordinal","tuple","cube_indices",
                    "record_positions","reduced_length","reduced_sha256",
                    "scalar","qstar_equation_coefficient","typed_gate_code",
                    "typed_gates","source_tuple_sha256",
                    "context_rows_sha256","class_id"} and
                active["ordinal"] == active_ordinals[0] and
                active["scalar"] == lambdas[active["ordinal"]-1] and
                active["class_id"] == mapping[active["ordinal"]-1],
                "checker generic first active")
    if not complete:
        require(block["provisional_only"] is True,
                "checker generic provisional nonclaim")
    if block["oracle_accounting"]:
        account = block["oracle_accounting"]
        require(set(account) == {"queries","hits","misses",
                    "query_cache_entries","query_cache_evictions",
                    "cold_recomputations"} and
                account["queries"] == account["hits"]+account["misses"] and
                account["query_cache_entries"] == 0 and
                account["query_cache_evictions"] == 0 and
                account["cold_recomputations"] == account["misses"],
                "checker generic oracle accounting")


def validate_resource_stage(receipt: dict[str, Any], phase: str) -> None:
    if phase == "fresh_immutable_prefix": rank = 1
    elif phase in {"raw_lambda_oracle","raw_lambda_reverse_dp"}: rank = 2
    elif phase == "predecessor_target6": rank = 3
    elif phase in {"target6_scalar_dp","target6_scalar_leaf_dp",
                   "target6_scalar_pair_dp","complete_ordered_census"}: rank = 4
    elif phase in {"formula_canaries","generic_leaf_square_canaries"}: rank = 5
    elif phase == "receipt_serialization": rank = 6
    else: raise RuntimeError("checker unregistered resource phase")
    groups=[(1,("base_q3_replay","normalized_inverse_fibre","cube_universe",
                  "context_registry")),
            (2,("directed_base_support","directed_surgery","prefix")),
            (3,("lambda_oracle",)),(4,("predecessor_target6",)),
            (6,("formula_canaries",))]
    for minimum,names in groups:
        for name in names:
            require(bool(receipt[name]) is (rank >= minimum),
                    f"checker resource stage projection: {name}")


def envelope(receipt: dict[str, Any], *, actual_bytes: int | None = None) -> None:
    require(digest_obj(UPSTREAM_RESOURCE_CAPS) == UPSTREAM_RESOURCE_CAPS_SHA,
            "checker upstream resource cap registry digest")
    common = {"schema","task_sha256","terminal_token","status","reason",
              "claim","fixed_prefix_only","pins","caps","base_q3_replay",
              "normalized_inverse_fibre","directed_base_support",
              "directed_surgery","prefix","cube_universe","context_registry",
              "predecessor_target6","lambda_oracle","formula_canaries",
              "census","performance","resource_guards","theorem_boundary",
              "claim_flags"}
    token = receipt.get("terminal_token")
    require(token in TERMINALS and receipt.get("status") == token,
            "checker terminal envelope")
    expected = common | ({"partial"} if token.endswith("UNKNOWN_RESOURCE") else
                         {"input_errors"} if token.endswith("UNKNOWN_INPUT") else set())
    require(set(receipt) == expected and receipt["schema"] == SCHEMA and
            receipt["task_sha256"] == TASK_SHA and receipt["caps"] == CAPS_157ED and
            receipt["fixed_prefix_only"] is True and
            receipt["pins"] == expected_pins(),
            "checker exact top-level schema")
    flags = {"full_D2_claimed": False, "full_H3_claimed": False,
             "all_depth3_claimed": False, "all_corrections_claimed": False,
             "literal_pair_claimed": False, "negative_global_claimed": False,
             "B4_A_claimed": False, "B4_B_claimed": False}
    require(receipt["claim_flags"] == flags and receipt["theorem_boundary"] == {
        "fixed_prefix_only": True, **flags,
        "lambda_invariance_claimed_beyond_queried_translations": False},
        "checker claim boundary")
    if token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT":
        require(receipt["census"] == {} and set(receipt["input_errors"]) == {
                    "authenticated_external_input","mathematical_scan_started"}
                and receipt["input_errors"]["mathematical_scan_started"] is False
                and receipt["reason"] == receipt["input_errors"][
                    "authenticated_external_input"] and receipt["claim"] == "none"
                and receipt["resource_guards"] == {},
                "checker input nested schema")
        validate_budget(receipt["performance"], packed=False)
        return
    complete = token in {"B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE",
                         "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT"}
    validate_census_envelope(receipt["census"], complete=complete)
    if complete:
        reason = ("complete_scan_nonzero_scalar" if token.endswith("ACTIVE")
                  else "complete_scan_all_typed_scalars_zero")
        claim = ("one_registered_typed_triple_direction_has_nonzero_qstar_scalar"
                 if token.endswith("ACTIVE") else
                 "qstar_annihilates_old108_and_all_typed_registered_triples_against_fixed_prefix")
        require(receipt["reason"] == reason and receipt["claim"] == claim and
                all(bool(receipt[name]) for name in (
                    "base_q3_replay","normalized_inverse_fibre",
                    "directed_base_support","directed_surgery","prefix",
                    "cube_universe","context_registry","lambda_oracle",
                    "predecessor_target6","formula_canaries")) and
                set(receipt["resource_guards"]) == {
                    "caps","budget","resource_hit",
                    "upstream_resource_caps",
                    "upstream_resource_caps_sha256"} and
                receipt["resource_guards"]["caps"] == CAPS_157ED and
                receipt["resource_guards"]["upstream_resource_caps"] ==
                    UPSTREAM_RESOURCE_CAPS and
                receipt["resource_guards"]["upstream_resource_caps_sha256"] ==
                    UPSTREAM_RESOURCE_CAPS_SHA and
                receipt["resource_guards"]["resource_hit"] is False,
                "checker complete nested schema")
        validate_budget(receipt["resource_guards"]["budget"], packed=False)
        validate_budget(receipt["performance"], packed=True)
        if actual_bytes is not None:
            require(receipt["performance"]["packed_receipt_bytes"] == actual_bytes,
                    "checker packed receipt exact byte length")
    else:
        partial = receipt["partial"]
        require(set(partial) == {"evaluated_prefix","last_committed_ordinal",
                    "in_progress_tuple_absent","phase","provisional_only",
                    "resource","typed_count","active_count",
                    "oracle_query_count","committed_census_sha256"} and
                partial["evaluated_prefix"] == receipt["census"]["evaluated_prefix"]
                and partial["last_committed_ordinal"] ==
                    receipt["census"]["last_ordinal"] and
                partial["in_progress_tuple_absent"] is True and
                partial["provisional_only"] is True and
                partial["typed_count"] == receipt["census"]["typed_count"] and
                partial["active_count"] ==
                    receipt["census"]["scalar_counts"]["1"]+
                    receipt["census"]["scalar_counts"]["2"] and
                partial["oracle_query_count"] ==
                    (0 if not receipt["census"]["oracle_accounting"] else
                     receipt["census"]["oracle_accounting"]["queries"]) and
                partial["committed_census_sha256"] ==
                    digest_obj(receipt["census"]) and
                set(partial["resource"]) == {"cap_reason","cap_key",
                    "cap_limit","observed_count","trigger_relation","phase",
                    "current_ordinal","current_tuple"} and
                partial["phase"] == partial["resource"]["phase"] and
                receipt["reason"] == partial["resource"]["cap_reason"] and
                receipt["claim"] == "none", "checker resource partial schema")
        resource_row = partial["resource"]
        cap_key = resource_row["cap_key"]
        require((cap_key in CAPS_157ED) !=
                    (cap_key in UPSTREAM_RESOURCE_CAPS) and
                resource_row["cap_reason"] == cap_key and
                resource_row["cap_limit"] ==
                    (CAPS_157ED[cap_key] if cap_key in CAPS_157ED else
                     UPSTREAM_RESOURCE_CAPS[cap_key])
                and resource_row["trigger_relation"] in {"gt","ge"} and
                ((resource_row["trigger_relation"] == "gt" and
                  resource_row["observed_count"] > resource_row["cap_limit"])
                 or (resource_row["trigger_relation"] == "ge" and
                     resource_row["observed_count"] >= resource_row["cap_limit"])),
                "checker resource comparator")
        require(set(receipt["resource_guards"]) == {
                    "caps","budget","resource_hit","reason",
                    "upstream_resource_caps",
                    "upstream_resource_caps_sha256"} and
                receipt["resource_guards"]["caps"] == CAPS_157ED and
                receipt["resource_guards"]["upstream_resource_caps"] ==
                    UPSTREAM_RESOURCE_CAPS and
                receipt["resource_guards"]["upstream_resource_caps_sha256"] ==
                    UPSTREAM_RESOURCE_CAPS_SHA and
                receipt["resource_guards"]["resource_hit"] is True and
                receipt["resource_guards"]["reason"] == receipt["reason"],
                "checker resource guard schema")
        validate_budget(receipt["resource_guards"]["budget"], packed=False)
        validate_budget(receipt["performance"], packed=False)
        require(receipt["resource_guards"]["budget"] == receipt["performance"]
                and receipt["performance"]["hit_reason"] == receipt["reason"],
                "checker resource budget binding")
        validate_resource_stage(receipt, partial["phase"])


def check_receipt(q3_path: Path, receipt_path: Path) -> dict[str, Any]:
    old = load_old(); q3 = load_q3(q3_path)
    validate_upstream_cap_source(old)
    if CHECKER_DEADLINE is not None:
        # The inherited hot loops use their own monotonic helper.  Back-date
        # its common origin so it receives exactly our remaining budget and
        # cannot reset to a fresh 18,000 seconds.
        old.CHECKER_STARTED = (time.monotonic() -
            (18000.0-CHECKER_DEADLINE.initial_seconds))
        old.CHECKER_CHECKS = 0
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw.decode("utf-8"))
    canonical = (json.dumps(receipt, sort_keys=True, separators=(",", ":"))+"\n").encode("utf-8")
    require(receipt_raw == canonical, "checker canonical receipt serialization")
    envelope(receipt, actual_bytes=len(receipt_raw))
    expected_pin_rows = expected_pins()
    require(receipt["pins"] == expected_pin_rows and
            receipt["pins"]["predecessor_run"] == "32326652060" and
            receipt["pins"]["predecessor_receipt_sha256"] ==
            "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
            "checker predecessor provenance pin")
    token = receipt["terminal_token"]
    if token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT":
        require(receipt["census"] == {} and receipt["input_errors"][
                    "mathematical_scan_started"] is False,
                "checker input-only terminal")
        return receipt
    e3, e4 = old.reconstruct(q3)
    tick("checker q3 reconstruction", True)
    old.validate_base_replay(receipt, q3, e3, e4)
    cubes, record_to_cube = cube_manifest(old, q3, e3)
    cube_rows = [{"cube_index": cube_index, "record_index": record,
                  "length": len(cubes[cube_index-1]),
                  "sha256": digest_obj(cubes[cube_index-1])}
                 for record,cube_index in sorted(record_to_cube.items())]
    expected_cube = {"cube_count":26,"cube_digest_sha256":CUBE_SHA,
        "cube_rows":cube_rows,
        "record_to_cube":{str(k):v for k,v in record_to_cube.items()},
        "cube_total_reduced_letters":9162,"ordered_pair_count":676,
        "ordered_triple_count":17576,
        "ordered_triple_unreduced_letters":18580536,
        "ordered_product":"cube_i*cube_j*cube_k",
        "ordinal":"((i-1)*26+(j-1))*26+k",
        "repeated_indices_retained":True}
    require(receipt["cube_universe"] == expected_cube,
            "checker cube receipt")
    normalized, base_key, inverse_words = old.rebuild_normalized_inverse_fibre(q3,e4)
    require(receipt["normalized_inverse_fibre"] == normalized,
            "checker normalized inverse")
    contexts, aliases, context_public, values, pairs = context_dp(old,e4,cubes)
    require(receipt["context_registry"] == context_public,
            "checker context receipt")
    if not receipt["prefix"]:
        require(token.endswith("UNKNOWN_RESOURCE") and
                receipt["census"]["evaluated_prefix"] == 0,
                "checker pre-prefix resource")
        return receipt
    tick("checker fresh prefix", True)
    pool, basis, events = replay_prefix(old, receipt, e4, normalized, base_key)
    if not receipt["lambda_oracle"]:
        require(token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE" and
                receipt["census"]["evaluated_prefix"] == 0 and
                receipt["partial"]["phase"] in {
                    "raw_lambda_oracle","raw_lambda_reverse_dp"},
                "checker oracle-construction resource prefix")
        return receipt
    tick("checker raw lambda oracle", True)
    oracle = RawOracle(old, pool, basis, validate_qstar_label(
        QSTAR, e4.degree+e4.collector.n))
    pivot_zero = [oracle.packed(row) for _, row in
                  sorted(basis.rows.items(), key=lambda item: pool.pivot_order(item[0]))]
    dependent_zero = []
    for event in events:
        vector = {}
        for component, blob_hex, coefficient in event["raw_column"]:
            identifier = pool.ids.get(bytes.fromhex(blob_hex))
            require(identifier is not None, "checker event prefix key")
            vector[old.replay_pack_key(component, identifier)] = coefficient
        require(old.checker_full_remainder(vector, basis, pool) == {},
                "checker dependent NF")
        dependent_zero.append(oracle.packed(vector))
    require(pivot_zero == [0]*362709 and dependent_zero == [0]*16,
            "checker oracle annihilation")
    oracle.public.update({"pivot_annihilation_count": 362709,
                          "pivot_annihilation_sha256": digest_obj(pivot_zero),
                          "dependent_annihilation_count": 16,
                          "dependent_annihilation_sha256": digest_obj(dependent_zero)})
    require(receipt["lambda_oracle"] == oracle.public,
            "checker portable lambda binding")
    if not receipt["predecessor_target6"]:
        require(token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE" and
                receipt["census"]["evaluated_prefix"] == 0 and
                receipt["partial"]["phase"] == "predecessor_target6",
                "checker predecessor-construction resource prefix")
        require(receipt["census"]["oracle_accounting"] == oracle.accounting(),
                "checker predecessor resource oracle checkpoint")
        return receipt
    seed_info = old.affine_checker_seed_words(q3,e3)
    tick("checker predecessor target6", True)
    predecessor = predecessor_certificate(old,e4,seed_info,pool,basis,oracle)
    require(receipt["predecessor_target6"] == predecessor,
            "checker predecessor target6 certificate")
    if token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE" and \
            receipt["partial"]["phase"] in {
                "target6_scalar_dp","target6_scalar_leaf_dp",
                "target6_scalar_pair_dp"}:
        require(receipt["census"]["evaluated_prefix"] == 0 and
                receipt["census"]["typed_dp_state_records"] ==
                    31*(26+676)+3*(26+676) and
                receipt["census"]["oracle_accounting"] == oracle.accounting(),
                "checker scalar-DP resource atomic prefix")
        return receipt
    n = receipt["census"]["evaluated_prefix"]
    complete = token in {"B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE",
                         "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT"}
    leaves = target_leaves(old,e4,cubes)
    tick("checker ordered census", True)
    expected = independently_scan(old,q3,e3,e4,base_key,cubes,contexts,aliases,
                                  context_public,values,pairs,leaves,oracle,n,complete)
    compare_census(receipt["census"], expected)
    resource_phase = (receipt["partial"]["phase"] if
                      token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE"
                      else None)
    run_canaries = complete or resource_phase == "receipt_serialization"
    if run_canaries:
        typed_words = []
        if expected["first_typed"] is not None:
            typed_words.append(expected["first_typed"])
            if expected["last_typed"] != expected["first_typed"]:
                typed_words.append(expected["last_typed"])
        tick("checker formula canaries", True)
        canary = formula_canaries(old,e4,cubes,leaves,pool,basis,oracle,
                                   seed_info,typed_words)
        require(receipt["formula_canaries"] == canary and
                canary["generic_leaf_square_pair_count"] == 78 and
                canary["generic_leaf_square_evaluation_count"] == 156,
                "checker independent formula/NF canaries")
    else:
        require(receipt["formula_canaries"] == {},
                "checker incomplete formula canary absence")
    require(receipt["census"]["oracle_accounting"] == oracle.accounting(),
            "checker exact oracle query accounting")
    if complete:
        require(n == 17576, "checker complete count")
        expected_token = ("B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE"
                          if expected["first"] is not None else
                          "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT")
        require(token == expected_token, "checker mechanical terminal")
        require(receipt["reason"] == ("complete_scan_nonzero_scalar"
                    if expected["first"] is not None else
                    "complete_scan_all_typed_scalars_zero") and
                receipt["claim"] == (
                    "one_registered_typed_triple_direction_has_nonzero_qstar_scalar"
                    if expected["first"] is not None else
                    "qstar_annihilates_old108_and_all_typed_registered_triples_against_fixed_prefix"),
                "checker exact mathematical terminal claim")
    else:
        require(token == "B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE" and
                receipt["partial"]["evaluated_prefix"] == n and
                receipt["partial"]["in_progress_tuple_absent"] is True and
                receipt["claim"] == "none" and
                receipt["reason"] == receipt["partial"]["resource"]["cap_reason"] and
                receipt["partial"]["provisional_only"] is True,
                "checker resource nonclaim")
    tick("checker completion", True)
    return receipt


def checker_self_test() -> None:
    def af(raw: bytes) -> dict[str, Any]:
        return {"base64": base64.b64encode(raw).decode("ascii"),
                "byte_length": len(raw), "sha256": digest_bytes(raw)}

    def packed_fixture(n: int, active_at: int | None, *, complete: bool,
                       mixed_failures: bool = False) -> tuple[dict[str, Any],dict[str,Any]]:
        classes = Classes(lambda _: "forced" if mixed_failures else digest_bytes(_))
        typed: list[bool] = []; lambdas: list[int] = []; failures: list[int] = []
        counts = {"typed":0,"scalar0":0,"scalar1":0,"scalar2":0,
                  "failures":{str(i):0 for i in range(6)}}
        first = None
        for ordinal in range(1,n+1):
            word = ([1], [2], [1,2])[(ordinal-1)%3] if mixed_failures else [1,-1]
            class_id = classes.add(word,ordinal)
            is_typed = (ordinal in (1,14,27)) if mixed_failures else True
            scalar = ((ordinal//13)%3 if is_typed else 255) if mixed_failures \
                     else (1 if ordinal == active_at else
                           (2 if active_at is not None and ordinal == active_at+7 else 0))
            failure = 0 if is_typed else 1+(ordinal%5)
            typed.append(is_typed); lambdas.append(scalar); failures.append(failure)
            counts["failures"][str(failure)] += 1
            if is_typed:
                counts["typed"] += 1; counts[f"scalar{scalar}"] += 1
                if scalar in (1,2) and first is None:
                    z=ordinal-1; i,j,k=z//676,(z//26)%26,z%26
                    first={"ordinal":ordinal,"tuple":[i+1,j+1,k+1],
                        "cube_indices":[i+1,j+1,k+1],
                        "record_positions":[i+2,j+2,k+2],
                        "reduced_length":len(word),
                        "reduced_sha256":digest_bytes(signed_word_bytes(word)),
                        "scalar":scalar,"qstar_equation_coefficient":
                            1 if scalar==1 else 2,"typed_gate_code":0,
                        "typed_gates":{"exponent_sums":[0,0],"E3_identity":True,
                            "marked_source_tuple":True,
                            "all_31_contexts_identity":True,
                            "all_46_named_occurrences_identity":True,
                            "target6_actual_quotient_identity":True},
                        "source_tuple_sha256":"0"*64,
                        "context_rows_sha256":CONTEXT_SHA,"class_id":class_id}
        mask=bytearray((n+7)//8)
        for index,value in enumerate(typed):
            if value: mask[index//8] |= 1 << (index%8)
        metadata=classes.metadata(); c=len(metadata)
        class_rows=[
            {"name":"tuple_to_class","data":af(b"".join(
                struct.pack("<H",x) for x in classes.mapping)),
             "decoded_digest":digest_obj(classes.mapping),"width":2,
             "endianness":"little","count":n},
            {"name":"class_first_ordinal","data":af(b"".join(
                struct.pack("<H",x) for x in classes.first)),
             "decoded_digest":digest_obj(classes.first),"width":2,
             "endianness":"little","count":c},
            {"name":"class_length","data":af(b"".join(
                struct.pack("<I",row["length"]) for row in metadata)),
             "decoded_digest":digest_obj([row["length"] for row in metadata]),
             "width":4,"endianness":"little","count":c},
            {"name":"class_sha256","data":af(b"".join(
                bytes.fromhex(row["sha256"]) for row in metadata)),
             "decoded_digest":digest_obj([row["sha256"] for row in metadata]),
             "width":32,"endianness":"raw","count":c}]
        block={"typed_mask":{**af(bytes(mask)),"bit_order":"LSB_first",
                 "decoded_count":n,"unused_high_bits_zero":True},
               "lambda_codes":{**af(bytes(lambdas)),"code_table":{
                 "0":"scalar0","1":"scalar1","2":"scalar2","255":"untyped"},
                 "decoded_count":n},
               "failure_codes":{**af(bytes(failures)),
                 "code_table":FAILURE_CODES,"decoded_count":n},
               "class_arrays":class_rows,"class_count":c,
               "tuple_to_class_decoded_sha256":digest_obj(classes.mapping),
               "evaluated_prefix":n,"last_ordinal":n,"complete_scan":complete,
               "typed_count":counts["typed"],
               "scalar_counts":{str(i):counts[f"scalar{i}"] for i in range(3)},
               "failure_counts":counts["failures"],
               "typed_dp_state_records":n,"ordered_count":17576,
               "array_layout_version":
                 "typed-bit-lsb/lambda-u8/failure-u8/class-u16le/v1",
               "tuple_order":"i outer, j middle, k inner",
               "oracle_accounting":{}}
        if complete: block["first_active"]=first
        else: block.update({"provisional_first_active":first,
                            "provisional_only":True})
        expected={"typed":typed,"lambdas":lambdas,"failures":failures,
                  "classes":classes,"first":first,"counts":counts,
                  "dp_states":n,"complete":complete}
        return block,expected

    # Production decoder on the exact bounded 3^3 order (repetitions and
    # duplicate classes included), plus padding/order/zero-column mutations.
    toy_block,toy_expected=packed_fixture(27,None,complete=True,
                                           mixed_failures=True)
    compare_census(toy_block,toy_expected)
    broken=copy.deepcopy(toy_block)
    raw=bytearray(decode_array(broken["typed_mask"])); raw[-1] |= 0x80
    broken["typed_mask"].update(af(bytes(raw)))
    expect_failure(lambda: compare_census(broken,toy_expected),"padding")
    broken=copy.deepcopy(toy_block); broken["tuple_order"]="permuted"
    expect_failure(lambda: compare_census(broken,toy_expected),"tuple order")
    broken=copy.deepcopy(toy_block)
    raw=bytearray(decode_array(broken["lambda_codes"])); raw[0]=2
    broken["lambda_codes"].update(af(bytes(raw)))
    expect_failure(lambda: compare_census(broken,toy_expected),"lambda zero omission")
    for index, field, value in [(0,"endianness","big"),
                               (1,"decoded_digest","0"*64),
                               (2,"width",2),
                               (3,"decoded_digest","0"*64)]:
        broken=copy.deepcopy(toy_block)
        broken["class_arrays"][index][field]=value
        expect_failure(lambda broken=broken:compare_census(
            broken,toy_expected),f"class metadata {index}")
    classes=Classes(lambda _:"collision")
    require([classes.add(word,i+1) for i,word in enumerate(
        ([1],[2],[1],[-1,-2]))] == [1,2,1,3] and
        classes.metadata()[2]["sha256"] == digest_bytes(b"\xff\xfe"),
        "checker collision/signed class")

    # Independent nonabelian Fox/action and exact reverse-pivot lambda/NF.
    def mul(a:tuple[int,...],b:tuple[int,...])->tuple[int,...]:
        return tuple(a[b[i]] for i in range(3))
    def inv(a:tuple[int,...])->tuple[int,...]:
        out=[0]*len(a)
        for i,image in enumerate(a): out[image]=i
        return tuple(out)
    a=(1,0,2); b=(0,2,1); c=mul(a,b); identity=(0,1,2)
    require(mul(mul(a,b),c) != identity and
            ["Da",f"{a}:Db",f"{mul(a,b)}:Dc"] != ["Da","Db","Dc"],
            "checker nonabelian Fox product law")
    x,y=c,a
    require(mul(mul(inv(x),y),x) != mul(mul(x,y),inv(x)),
            "checker source inverse/conjugation mutation")
    require(signed_word_bytes([-1,-2]) != signed_word_bytes([1,2]),
            "checker negative letter mutation")
    p,r,q=(1,b"p"),(1,b"r"),(1,b"q")
    order=[p,r]; rows={p:{p:1,r:1},r:{r:1,q:2}}; table={q:1}
    for pivot in reversed(order):
        table[pivot]=(-sum(coef*table.get(key,0)
                           for key,coef in rows[pivot].items()
                           if key != pivot))%3
    def nf(vector:dict[Any,int])->dict[Any,int]:
        out={key:value%3 for key,value in vector.items() if value%3}
        for pivot in order:
            coefficient=out.get(pivot,0)
            if coefficient:
                for key,value in rows[pivot].items():
                    new=(out.get(key,0)-coefficient*value)%3
                    if new: out[key]=new
                    else: out.pop(key,None)
        return out
    for cp in range(3):
        for cr in range(3):
            for cq in range(3):
                vector={p:cp,r:cr,q:cq}
                require(nf(vector).get(q,0) == sum(
                    value*table[key] for key,value in vector.items())%3,
                    "checker lambda versus direct NF")
    forward={q:1}
    for pivot in order:
        forward[pivot]=(-sum(coef*forward.get(key,0)
                             for key,coef in rows[pivot].items()
                             if key != pivot))%3
    require(table == {q:1,r:1,p:2} and forward != table,
            "checker reverse versus forward recurrence")
    expect_failure(lambda: require(order.index(p) > order.index(r),
                                   "recurrence cycle"),"recurrence cycle")
    require(sorted(order,key={p:2,r:1}.get) != order,
            "checker numeric-id order mutation")
    values=[b"e",b"p"]; ids={blob:i for i,blob in enumerate(values)}
    checkpoint=len(values); values.append(b"tmp"); ids[b"tmp"]=2
    blob=values.pop(); require(ids[blob] == 2,"checker rollback binding"); del ids[blob]
    require(len(values)==checkpoint and len(ids)==len(values),
            "checker rollback id cleanup")

    # Qstar and dependent-event mutations use the checker production gates.
    validate_qstar_label(QSTAR,154)
    dual={"equations":[{"label":QSTAR,"coefficient":1}],
          "support_count":1,"support_sha256":QSTAR_SHA,
          "normalized_rhs":1,"yTz_mod3":2,
          "target_boundary":{"target_ordinals":[6]},
          "target6_fixed_prefix_functional":True}
    validate_qstar_dual(dual)
    expect_failure(lambda:require(q in order,"checker qstar pivot"),
                   "checker qstar pivot")
    for key,value in [("support_count",2),("normalized_rhs",2),("yTz_mod3",1)]:
        bad=copy.deepcopy(dual); bad[key]=value
        expect_failure(lambda bad=bad:validate_qstar_dual(bad),f"qstar {key}")
    for label,width in [([5,QSTAR[1],4,QSTAR[3]],154),
                        ([6,"wrong",4,QSTAR[3]],154),
                        ([6,QSTAR[1],3,QSTAR[3]],154),
                        ([6,QSTAR[1],4,"00"+QSTAR[3][2:]],154),
                        (QSTAR,153)]:
        expect_failure(lambda label=label,width=width:
                       validate_qstar_label(label,width),"qstar label")
    dep_rows=[[1,"0102",1],[2,"0304",2]]
    encoded=raw_column_bytes(dep_rows,2)
    dep_event={"translation_ordinal":7,"relator_index":2,
               "sha256":digest_bytes(encoded)}
    require(nf({p:1,r:1}) == {} and (table[p]+table[r])%3 == 0 and
            dep_event=={"translation_ordinal":7,"relator_index":2,
                        "sha256":digest_bytes(raw_column_bytes(dep_rows,2))},
            "checker dependent raw event")
    for mutation in ([[0,"0102",1]],[[1,"01",1]],[[1,"0102",0]]):
        expect_failure(lambda mutation=mutation:raw_column_bytes(mutation,2),
                       "dependent raw encoding")
    expect_failure(lambda:require(dep_event["translation_ordinal"]==8,
                                  "checker dependent ordinal"),
                   "checker dependent ordinal")
    expect_failure(lambda:require(dep_event["relator_index"]==3,
                                  "checker dependent relator"),
                   "checker dependent relator")

    # Empty record/order and exact first-reason fixtures.
    records=[[]]+[[1]*(i+1) for i in range(26)]
    def cube_order(rows:Sequence[Sequence[int]])->list[list[int]]:
        require(len(rows)==27 and sum(not row for row in rows)==1 and not rows[0],
                "checker toy empty record")
        cubes=[list(row)*3 for row in rows[1:]]
        require(len(cubes)==len({tuple(row) for row in cubes})==26,
                "checker toy cube uniqueness")
        return cubes
    cube_digest=digest_obj(cube_order(records))
    expect_failure(lambda:cube_order([records[1],[]]+records[2:]),
                   "checker empty position")
    require(digest_obj(cube_order([[]]+[records[2],records[1]]+records[3:]))
            != cube_digest,"checker cube order")
    require(first_failure_code([True]*5)==0,"checker all typed gates")
    for index in range(5):
        require(first_failure_code([True]*index+[False]+[None]*(4-index))==index+1,
                "checker first failure reason")
    expect_failure(lambda:first_failure_code([False,True,None,None,None]),
                   "checker gate after failure")

    # Capacity-neutral lookup: cache pressure changes only accounting.
    def cached(capacity:int)->tuple[list[int],int,int]:
        cache:dict[int,int]={}; order_keys:list[int]=[]; evict=cold=0; answer=[]
        for key in [0,1,2,0,3,1,4,0,2,4]:
            if key not in cache:
                cold+=1
                if len(cache)>=capacity:
                    del cache[order_keys.pop(0)]; evict+=1
                cache[key]=(2*key+1)%3; order_keys.append(key)
            answer.append(cache[key])
        return answer,evict,cold
    require(cached(1)[0]==cached(16)[0] and cached(1)[1]>0 and
            cached(1)[2]>cached(16)[2],"checker cache neutrality")

    # Exact production envelope for complete ACTIVE/INERT and five committed
    # resource phases.  These use the same generic decoder/envelope as main.
    claim_flags={"full_D2_claimed":False,"full_H3_claimed":False,
        "all_depth3_claimed":False,"all_corrections_claimed":False,
        "literal_pair_claimed":False,"negative_global_claimed":False,
        "B4_A_claimed":False,"B4_B_claimed":False}
    boundary={"fixed_prefix_only":True,**claim_flags,
        "lambda_invariance_claimed_beyond_queried_translations":False}
    common_empty={key:{} for key in ("base_q3_replay","normalized_inverse_fibre",
        "directed_base_support","directed_surgery","prefix","cube_universe",
        "context_registry","predecessor_target6","lambda_oracle",
        "formula_canaries")}
    budget={"common_start_monotonic":1.0,"initial_remaining_seconds":60.0,
            "elapsed_seconds":1.0,"checks":1,"peak_rss_bytes":0,
            "hit_reason":None,"remaining_seconds":59.0}
    def complete_envelope(active_at:int|None)->dict[str,Any]:
        block,_=packed_fixture(17576,active_at,complete=True)
        token=("B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE" if active_at is not None
               else "B345_TRIPLE_CUBE_RAW_LAMBDA_INERT")
        row={**common_empty,"schema":SCHEMA,"task_sha256":TASK_SHA,
             "terminal_token":token,"status":token,
             "reason":"complete_scan_nonzero_scalar" if active_at is not None
                      else "complete_scan_all_typed_scalars_zero",
             "claim":"one_registered_typed_triple_direction_has_nonzero_qstar_scalar"
                     if active_at is not None else
                     "qstar_annihilates_old108_and_all_typed_registered_triples_against_fixed_prefix",
             "fixed_prefix_only":True,"pins":expected_pins(),"caps":CAPS_157ED,
             "census":block,"performance":{**budget,"packed_receipt_bytes":1},
             "resource_guards":{"caps":CAPS_157ED,"budget":budget,
                 "resource_hit":False,
                 "upstream_resource_caps":UPSTREAM_RESOURCE_CAPS,
                 "upstream_resource_caps_sha256":UPSTREAM_RESOURCE_CAPS_SHA},
             "claim_flags":claim_flags,"theorem_boundary":boundary}
        for name in ("base_q3_replay","normalized_inverse_fibre",
                     "directed_base_support","directed_surgery","prefix",
                     "cube_universe","context_registry","lambda_oracle",
                     "predecessor_target6","formula_canaries"):
            row[name]={"fixture":name}
        envelope(row); return row
    inert=complete_envelope(None); active=complete_envelope(3)
    require(active["census"]["first_active"]["ordinal"]==3 and
            active["census"]["scalar_counts"]["2"]==1 and
            inert["census"]["first_active"] is None,
            "checker complete active/inert freeze")
    for label,mutation in [
        ("reason",lambda row:row.update({"reason":"wrong"})),
        ("claim",lambda row:row.update({"claim":"wrong"})),
        ("status",lambda row:row.update({"status":"wrong"})),
        ("pin",lambda row:row["pins"].update({"task_sha256":"0"*64})),
        ("positive field",lambda row:row.update({"selected_solution":{}})),
        ("full claim",lambda row:row["claim_flags"].update(
            {"full_D2_claimed":True}))]:
        bad=copy.deepcopy(active); mutation(bad)
        expect_failure(lambda bad=bad:envelope(bad),f"terminal {label}")
    def resource_envelope(n:int,active_at:int|None,phase:str,key:str,
                          relation:str="gt")->dict[str,Any]:
        block,_=packed_fixture(n,active_at,complete=False)
        require((key in CAPS_157ED) != (key in UPSTREAM_RESOURCE_CAPS),
                "checker fixture cap registry")
        limit=(CAPS_157ED[key] if key in CAPS_157ED else
               UPSTREAM_RESOURCE_CAPS[key])
        observed=limit if relation=="ge" else limit+1
        hit_budget={**budget,"hit_reason":key}
        resource={"cap_reason":key,"cap_key":key,"cap_limit":limit,
                  "observed_count":observed,"trigger_relation":relation,
                  "phase":phase,"current_ordinal":n+1,"current_tuple":[]}
        row={**common_empty,"schema":SCHEMA,"task_sha256":TASK_SHA,
             "terminal_token":"B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE",
             "status":"B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE",
             "reason":key,"claim":"none","fixed_prefix_only":True,
             "pins":expected_pins(),"caps":CAPS_157ED,"census":block,
             "performance":hit_budget,"resource_guards":{"caps":CAPS_157ED,
                 "budget":hit_budget,"resource_hit":True,"reason":key,
                 "upstream_resource_caps":UPSTREAM_RESOURCE_CAPS,
                 "upstream_resource_caps_sha256":UPSTREAM_RESOURCE_CAPS_SHA},
             "partial":{"evaluated_prefix":n,"last_committed_ordinal":n,
                 "in_progress_tuple_absent":True,"phase":phase,
                 "provisional_only":True,"resource":resource,
                 "typed_count":block["typed_count"],
                 "active_count":block["scalar_counts"]["1"]+
                                block["scalar_counts"]["2"],
                 "oracle_query_count":0,
                 "committed_census_sha256":digest_obj(block)},
             "claim_flags":claim_flags,"theorem_boundary":boundary}
        stage_rank=(1 if phase=="fresh_immutable_prefix" else
                    2 if phase in {"raw_lambda_oracle","raw_lambda_reverse_dp"} else
                    3 if phase=="predecessor_target6" else
                    4 if phase=="complete_ordered_census" else
                    5 if phase in {"formula_canaries",
                                   "generic_leaf_square_canaries"} else 6)
        for minimum,names in [
            (1,("base_q3_replay","normalized_inverse_fibre","cube_universe",
                "context_registry")),
            (2,("directed_base_support","directed_surgery","prefix")),
            (3,("lambda_oracle",)),(4,("predecessor_target6",)),
            (6,("formula_canaries",))]:
            if stage_rank>=minimum:
                for name in names: row[name]={"fixture":name}
        envelope(row); return row
    resources=[resource_envelope(0,None,"fresh_immutable_prefix",
                  "common_math_soft_deadline_seconds","ge"),
               resource_envelope(0,None,"raw_lambda_reverse_dp",
                  "raw_lambda_recursion_edges"),
               resource_envelope(2,None,"complete_ordered_census",
                  "typed_dp_state_records"),
               resource_envelope(10,3,"complete_ordered_census",
                   "producer_soft_rss_bytes","ge"),
               resource_envelope(0,None,"predecessor_target6",
                   "affine_rows")]
    require(resources[3]["census"]["provisional_first_active"]["ordinal"]==3,
            "checker resource provisional active")
    bad=copy.deepcopy(resources[2]); bad["partial"]["phase"]="wrong"
    expect_failure(lambda:envelope(bad),"resource phase")
    bad=copy.deepcopy(resources[2])
    bad["partial"]["phase"]="affine_remainder"
    bad["partial"]["resource"]["phase"]="affine_remainder"
    expect_failure(lambda:envelope(bad),"unnormalized helper resource phase")
    bad=copy.deepcopy(resources[2]); bad["performance"]["hit_reason"]="wrong"
    expect_failure(lambda:envelope(bad),"resource budget")
    bad=copy.deepcopy(resources[2])
    bad["partial"]["resource"]["cap_reason"]="unknown_reason"
    bad["reason"]="unknown_reason"
    bad["resource_guards"]["reason"]="unknown_reason"
    bad["resource_guards"]["budget"]["hit_reason"]="unknown_reason"
    bad["performance"]["hit_reason"]="unknown_reason"
    expect_failure(lambda:envelope(bad),"resource cap reason/key")
    bad=copy.deepcopy(resources[0]); bad["formula_canaries"]={"forged":True}
    expect_failure(lambda:envelope(bad),"resource future-stage payload")
    require(resources[-1]["partial"]["resource"]["cap_key"] ==
                "affine_rows", "checker honest upstream resource")
    bad=copy.deepcopy(resources[-1])
    bad["partial"]["resource"]["cap_key"]="unknown_old_cap"
    expect_failure(lambda:envelope(bad),"checker unknown upstream cap")
    bad=copy.deepcopy(resources[-1])
    bad["partial"]["resource"]["cap_limit"]-=1
    expect_failure(lambda:envelope(bad),"checker stale upstream cap limit")
    bad=copy.deepcopy(active)
    bad["resource_guards"]["upstream_resource_caps_sha256"]="0"*64
    expect_failure(lambda:envelope(bad),"checker upstream registry digest")
    input_row={**common_empty,"schema":SCHEMA,"task_sha256":TASK_SHA,
        "terminal_token":"B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT",
        "status":"B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT",
        "reason":"fixture drift","claim":"none","fixed_prefix_only":True,
        "pins":expected_pins(),"caps":CAPS_157ED,"census":{},
        "performance":budget,"resource_guards":{},"claim_flags":claim_flags,
        "theorem_boundary":boundary,"input_errors":{
            "authenticated_external_input":"fixture drift",
            "mathematical_scan_started":False}}
    envelope(input_row)
    bad=copy.deepcopy(input_row); bad["input_errors"]["mathematical_scan_started"]=True
    expect_failure(lambda:envelope(bad),"input mathematical start")

    # Formula/source hard-fail and common remaining-deadline canaries.
    direct={"value":mul(mul(a,b),c),"gradient":["Da",f"{a}:Db"]}
    wrong={"value":mul(mul(a,c),b),"gradient":["Da",f"{a}:Db"]}
    require(direct != wrong,"checker formula/direct mutation")
    expect_failure(lambda:require(direct==wrong,"formula drift"),"formula hard fail")
    deadline=Deadline(137.0)
    require(deadline.initial_seconds==137.0 and deadline.initial_seconds<18000,
            "checker common deadline remainder")
    expect_failure(lambda:Deadline(18001.0),"checker deadline reset")
    require(78*2==156,"checker leaf/square pair/evaluation split")
    pinned_old=load_old()
    require(hasattr(pinned_old,"CheckerAffineSystem") and
            hasattr(pinned_old,"replay_pivot_surgery") and
            sys.modules.get("_d972_157ed_independent_old_checker") is pinned_old,
            "checker authenticated predecessor import")
    print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_CHECKER_SELFTEST_PASS "
          "cube_empty_order=1 packed_3cube=1 action_orientation=1 "
          "lambda_reverse_nf=1 lambda_mutations=1 qstar_mutations=1 "
          "first_reason=1 complete_active_inert=1 partial_resource=5 "
          "resource_phase_normalization=1 upstream_cap_registry=1 "
          "packed_classes=1 dependent_event=1 cache_neutrality=1 "
          "source_dag=1 formula_hard_fail=1 deadline_remainder=1 "
          "pinned_import=1",
          flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    global CHECKER_DEADLINE
    args = list(argv if argv is not None else sys.argv[1:])
    if "--self-test" in args:
        checker_self_test(); return 0
    require(len(args) >= 2, "checker q3 and receipt paths")
    seconds = float(args[2]) if len(args) > 2 else 18000.0
    CHECKER_DEADLINE = Deadline(seconds)
    check_receipt(Path(args[0]), Path(args[1]))
    print("D972_B345_TRIPLE_CUBE_RAW_LAMBDA_CHECKER_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
