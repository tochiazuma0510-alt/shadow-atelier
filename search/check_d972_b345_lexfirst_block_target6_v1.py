"""Independent checker for the one-block target-6 affine lane."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Sequence


ROOT = Path(__file__).resolve().parents[1]
TASK = Path("sol/luna_task_157ei_b345_lexfirst_block_target6.md")
TASK_SHA = "cfe0c50046a750e4169c473872c5770ce76c105267353e82c9ed19de01c043f4"
TASK_BYTES = 24179
SCHEMA = "d972-b345-lexfirst-block-target6/v1"
OUTPUT = Path("ci/out/d972_b345_lexfirst_block_target6_v1.json")
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
CURRENT_PRODUCER = Path("search/d972_b345_lexfirst_block_target6_v1.py")
CURRENT_PRODUCER_SHA = \
    "f901cffd73069e78c9cc256e1a6c18c7e7ce6adef6d4de0c4fe68970571476bb"
CURRENT_PRODUCER_BYTES = 143075

EH_CHECKER = Path("search/check_d972_b345_full_d2_dual_correlation_v2.py")
EH_CHECKER_SHA = "881719f18b302afcb5ee25fd22e36ef7d6b50ee38a3562f208a2adb2a6e74060"
EH_CHECKER_BYTES = 21933
EH_PRODUCER = Path("search/d972_b345_full_d2_dual_correlation_v2.py")
EH_PRODUCER_SHA = "6557bcfea70c0846158951fafe3d6ef8790479a5c7010db896ed76540dd5ae5f"
EH_PRODUCER_BYTES = 42449
EH_DRIVER = Path("search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g")
EH_DRIVER_SHA = "5b76b267a36526f4f2d9e325b4b92e36c7b241f6f9d75abec7e08c3c9ff74cde"
EH_DRIVER_BYTES = 13253
EH_TASK = Path("sol/luna_task_157eh_b345_full_d2_monitor_scope_repair.md")
EH_TASK_SHA = "5d8da27e3997b261c004bb2fb4a40e9416bed39536816ab2fca9f3a9935c095e"
EH_TASK_BYTES = 15015
ED_CHECKER = Path("search/check_d972_b345_triple_cube_raw_lambda_census_v1.py")
ED_CHECKER_SHA = "677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce"
ED_CHECKER_BYTES = 97363
FIXTURE_ED_MODULE_NAME = "_d972_157eg_pinned_157ed_checker"
FIXTURE_OLD_MODULE_NAME = "_d972_157ed_independent_old_checker"
EC_PRODUCER = Path("search/d972_b345_seedspan_triple4_v1.py")
EC_PRODUCER_SHA = "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"
EC_PRODUCER_BYTES = 535219
EC_CHECKER = Path("search/check_d972_b345_seedspan_triple4_v1.py")
EC_CHECKER_SHA = "ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981"
EC_CHECKER_BYTES = 574347
EC_DRIVER = Path("search/d972_b345_seedspan_triple4_gha_driver_v1.g")
EC_DRIVER_SHA = "a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4"
EC_DRIVER_BYTES = 9041
EC_TASK = Path("sol/luna_task_157ec_b345_seedspan_triple4.md")
EC_TASK_SHA = "1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2"
EC_TASK_BYTES = 14751
Q3_PRODUCER = Path("search/d972_b345_q3_chief_v1.g")
Q3_PRODUCER_SHA = "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
Q3_DRIVER = Path("search/d972_b345_q3_gha_driver_v1.g")
Q3_DRIVER_SHA = "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"

PIN_SPECS = {
    "157ei_task": (TASK, TASK_SHA, TASK_BYTES),
    "157eh_producer": (EH_PRODUCER, EH_PRODUCER_SHA, EH_PRODUCER_BYTES),
    "157eh_checker": (EH_CHECKER, EH_CHECKER_SHA, EH_CHECKER_BYTES),
    "157eh_driver": (EH_DRIVER, EH_DRIVER_SHA, EH_DRIVER_BYTES),
    "157eh_task": (EH_TASK, EH_TASK_SHA, EH_TASK_BYTES),
    "157ec_producer": (EC_PRODUCER, EC_PRODUCER_SHA, EC_PRODUCER_BYTES),
    "157ec_checker": (EC_CHECKER, EC_CHECKER_SHA, EC_CHECKER_BYTES),
    "157ec_driver": (EC_DRIVER, EC_DRIVER_SHA, EC_DRIVER_BYTES),
    "157ec_task": (EC_TASK, EC_TASK_SHA, EC_TASK_BYTES),
    "q3_producer": (Q3_PRODUCER, Q3_PRODUCER_SHA, None),
    "q3_checker": (Q3_CHECKER, Q3_CHECKER_SHA, None),
    "q3_driver": (Q3_DRIVER, Q3_DRIVER_SHA, None),
}
AUTH_PIN_SPECS = {**PIN_SPECS,
    "157ei_current_producer": (CURRENT_PRODUCER, CURRENT_PRODUCER_SHA,
                               CURRENT_PRODUCER_BYTES)}
TERMINALS = frozenset({
    "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT",
    "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT",
    "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE",
    "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT",
})
CAPS = {"translation_blocks": 1, "relator_columns": 11,
    "affine_variables": 108, "affine_rows": 1_000_000,
    "target_live_remainders": 2_000_000,
    "dual_provenance_entries": 128,
    "common_math_soft_deadline_seconds": 18_000,
    "producer_soft_rss_bytes": 4_831_838_208,
    "packed_receipt_bytes": 268_435_456}
PREFIX_COUNTS = {"columns": 362725, "pivots": 362709,
    "dependent_columns": 16, "live_sparse_entries": 3090367,
    "row_tail_visits": 2727658, "BFS_translations": 32768,
    "directed_translations": 207}
PREFIX_POOL_CHECKPOINT = 976408
PREFIX_STABLE_SHA = "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d"
PREFIX_TRANSLATIONS_SHA = "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f"
PREFIX_COLUMNS_SHA = "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343"
PREFIX_BLOCKERS_SHA = "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53"
BASE_OCCURRENCE_SHA = "3eacd6dc77d62c1799a55923d3c8d5313a37ceab8e78b58b07b45925a28f131d"
FIRST_T_HEX = (
    "0001030608070402050d0a0b0e1011090c0f16131417191a1215181b1c1d1e1f"
    "2021222328272625242c2b2a293534333231302f2e2d3c3d3e363738393a3b4140"
    "3f4746454443424d4c4b4a4948504f4e5951525354555657585b5c5d5e5f606162"
    "5a6867666564636b6a696c74737271706f6e6d75767778797a7b7c7d7e7f808182"
    "838485868788898a8b8c8d8e8f00000200000000000000")
FIRST_T_WORD_SHA = "04813137f271cba21b5fdab6b733f0a0ac8ca9daa6b23323e5de55d2b7edba36"
FIRST_G_WORD_SHA = "5e1880d33973be6d67c31110827daf4db55cddf533c4e88354e0c26fbb74a448"
SECTION_MANIFEST_SHA = "aae5341e2f0586069548360b7441d7ebd4fc9550dd752171a8f59ffa3804b073"
CORRELATION_SHA = "8f69ef922a646c0306f2c9ebcf0c8f03531c84b057e29ad4e580a508911c6551"
SEED_MANIFEST_SHA = "17655b21cf526800e751fc5ce5876934de634f3e32d7ba258119138a9828ed80"
OLD_TYPED_SPLIT_SHA = "96e906aaee06d8748dd5c48c9fb3e9d009a185abdee91d8b66f14d545541f545"
OLD_BASE_GRADIENT_SHA = "788fd8712f76a3ca254bb2179b5498fed3ca00e649ba0321ef297d2d985cc71e"
OLD_TARGET6_ROW_SHA = "e99602b0981251e4bb81ab0d2113791563bc9ec9df2a45828aea2880ec6d2f9e"

_REGISTRY_SOURCE = {
    "authenticated_input": {"authenticated_input"},
    "source_preflight": {"source_preflight", "affine_source_preflight"},
    "fresh_immutable_prefix": {"fresh_immutable_prefix",
        "strong_wform_fresh_BFS", "strong_wform_directed_round",
        "packed_provenance_dag_growth", "packed_pivot_column_elimination",
        "packed_target_sparse_elimination", "proof_DAG_array_bytes",
        "proof_DAG_base64", "proof_DAG_base64_complete"},
    "raw_lambda_oracle": {"raw_lambda_oracle", "raw_lambda_reverse_dp"},
    "base_columns": {"base_columns"}, "dual_correlation": {"dual_correlation"},
    "section_witness": {"section_witness", "proof_DAG_array_bytes",
        "proof_DAG_base64", "proof_DAG_base64_complete"},
    "block_insertion": {"block_insertion", "packed_provenance_dag_growth",
        "packed_pivot_column_elimination", "affine_full_remainder",
        "affine_remainder"},
    "target_reduction": {"target_reduction", "affine_full_remainder",
        "affine_remainder", "affine_transposed_row_absorption"},
    "selected_proof": {"selected_proof", "packed_provenance_dag_growth",
        "packed_target_sparse_elimination", "proof_DAG_pre_serialization_RSS",
        "proof_DAG_reachability", "proof_DAG_compact_serialization",
        "proof_DAG_array_bytes", "proof_DAG_base64",
        "proof_DAG_base64_complete"},
}
MONITOR_REGISTRY = {outer: sorted(inner) for outer, inner in
                    sorted(_REGISTRY_SOURCE.items())}
MONITOR_FROZEN = {outer: frozenset(inner) for outer, inner in
                  _REGISTRY_SOURCE.items()}
MONITOR_SHA = None

CHECKER_STARTED: float | None = None
CHECKER_DEADLINE: float | None = None
CHECKER_CHECKS = 0


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_obj(value: Any) -> str:
    return sha_bytes(json.dumps(value, sort_keys=True,
        separators=(",", ":")).encode("utf-8"))


MONITOR_SHA = sha_obj(MONITOR_REGISTRY)


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def authenticate() -> None:
    for label, (path, digest, size) in AUTH_PIN_SPECS.items():
        full = ROOT/path
        require(full.is_file() and (size is None or full.stat().st_size == size)
                and sha_file(full) == digest, "157ei checker pin: "+label)


def pin_rows(q3_path: Path) -> dict[str, Any]:
    rows = {label: {"path": path.as_posix(), "sha256": digest,
                    "bytes": (ROOT/path).stat().st_size}
            for label, (path, digest, _) in PIN_SPECS.items()}
    rows["q3_artifact"] = {"path": Q3_PATH.as_posix(), "sha256": Q3_SHA,
        "bytes": q3_path.stat().st_size if q3_path.is_file() else None}
    rows["157ec_run_evidence"] = {"run": "32326652060",
        "receipt_sha256":
            "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
        "evidence_only_not_imported": True}
    rows["157eh_run_evidence"] = {"run": "32374248796",
        "commit": "9e1da3ca55133ae17fe6349bf64e7695fdda14f6",
        "receipt_sha256":
            "7c9de4d4aa5dc0facf94cec9c4b2b71d81c1b8cc590e84aa574cace18c1cb7d5",
        "evidence_only_not_imported": True}
    return rows


_EH: Any | None = None


def load_eh_checker() -> Any:
    global _EH
    authenticate()
    if _EH is not None:
        return _EH
    spec = importlib.util.spec_from_file_location(
        "_d972_157ei_frozen_157eh_checker", ROOT/EH_CHECKER)
    require(spec is not None and spec.loader is not None,
            "157ei frozen checker spec")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None); raise
    require(module.SCHEMA == "d972-b345-full-d2-dual-correlation/v2",
            "157ei frozen checker schema")
    _EH = module; return module


def loaded_fixture_checker_modules(
        eg: Any, digest_reader: Callable[[Path], str] = sha_file) \
        -> tuple[Any, Any]:
    """Reuse only the exact checker modules loaded by inherited selftests."""
    authenticate()
    require(eg.ED_CHECKER == ED_CHECKER and
            eg.ED_CHECKER_SHA == ED_CHECKER_SHA and
            eg.PIN_SPECS.get("157ed_checker") ==
                (ED_CHECKER, ED_CHECKER_SHA, ED_CHECKER_BYTES),
            "157ei fixture inherited 157ed checker pin")
    ed = sys.modules.get(FIXTURE_ED_MODULE_NAME)
    ed_path = (ROOT/ED_CHECKER).resolve()
    require(isinstance(ed, type(sys)) and
            getattr(ed, "__name__", None) == FIXTURE_ED_MODULE_NAME and
            isinstance(getattr(ed, "__file__", None), str) and
            Path(ed.__file__).resolve() == ed_path and ed_path.is_file() and
            ed_path.stat().st_size == ED_CHECKER_BYTES and
            digest_reader(ed_path) == ED_CHECKER_SHA and
            getattr(ed, "SCHEMA", None) ==
                "d972-b345-triple-cube-raw-lambda-census/v1" and
            callable(getattr(ed, "load_old", None)) and
            getattr(ed, "OLD_CHECKER", None) == EC_CHECKER and
            getattr(ed, "OLD_CHECKER_SHA", None) == EC_CHECKER_SHA and
            getattr(ed, "OLD_PRODUCER", None) == EC_PRODUCER and
            getattr(ed, "OLD_PRODUCER_SHA", None) == EC_PRODUCER_SHA and
            getattr(ed, "OLD_DRIVER", None) == EC_DRIVER and
            getattr(ed, "OLD_DRIVER_SHA", None) == EC_DRIVER_SHA and
            getattr(ed, "OLD_TASK", None) == EC_TASK and
            getattr(ed, "OLD_TASK_SHA", None) == EC_TASK_SHA,
            "157ei fixture exact loaded 157ed checker")
    old = sys.modules.get(FIXTURE_OLD_MODULE_NAME)
    old_path = (ROOT/EC_CHECKER).resolve()
    require(isinstance(old, type(sys)) and
            getattr(old, "__name__", None) == FIXTURE_OLD_MODULE_NAME and
            isinstance(getattr(old, "__file__", None), str) and
            Path(old.__file__).resolve() == old_path and old_path.is_file() and
            old_path.stat().st_size == EC_CHECKER_BYTES and
            digest_reader(old_path) == EC_CHECKER_SHA and
            getattr(old, "AFFINE_SCHEMA", None) ==
                "d972-b345-seedspan-triple4/v1" and
            callable(getattr(old, "CheckerAffineSystem", None)) and
            callable(getattr(old, "checker_target_row_transposed", None)),
            "157ei fixture exact loaded 157ec checker")
    return ed, old


def tick(phase: str, force: bool = False) -> None:
    global CHECKER_CHECKS
    CHECKER_CHECKS += 1
    if not force and CHECKER_CHECKS & 63:
        return
    require(CHECKER_DEADLINE is not None and time.monotonic() < CHECKER_DEADLINE,
            "157ei checker soft deadline: "+phase)


def theorem_boundary() -> dict[str, Any]:
    return {"pinned_E4_roof_only": True,
        "single_lexfirst_translation_block_only": True,
        "all_old_active_rows_added": False, "full_D2_claimed": False,
        "full_H3_claimed": False, "targets_7_through_33_checked": False,
        "typed_lift_claimed": False, "negative_claimed": False,
        "B4_A_claimed": False, "B4_B_claimed": False,
        "inconsistent_is_not_full_D2_obstruction": True,
        "consistent_is_target6_membership_only": True}


def claim_row(token: str, block_complete: bool) -> dict[str, Any]:
    consistent = token == "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT"
    return {"single_lexfirst_translation_block_only": True,
        "complete_11_relator_block": bool(block_complete),
        "all_old_active_rows_added": False, "full_D2_claimed": False,
        "full_H3_claimed": False, "targets_7_through_33_checked": False,
        "typed_lift_claimed": False, "negative_claimed": False,
        "B4_A_claimed": False, "B4_B_claimed": False,
        "target6_membership_in_full_D2_for_selected_correction": consistent,
        "mathematical_claim": ("one_registered_108_seed_correction_has_"
            "target6_boundary_in_B1_subset_full_D2" if consistent else
            "none" if token.endswith(("UNKNOWN_RESOURCE", "UNKNOWN_INPUT"))
            else "no_registered_108_seed_coefficient_solves_target6_mod_B1")}


COMMON_KEYS = {"schema", "task_sha256", "terminal_token", "status",
    "reason", "phase", "pins", "caps", "upstream_caps", "claims",
    "theorem_boundary", "monitor_scope", "resource_guards", "partial",
    "input_errors", "performance"}
AUTH_FIELDS = {"base_q3_replay", "normalized_inverse_fibre", "seed_manifest"}
SOURCE_FIELDS = {"source_preflight"}
PREFIX_FIELDS = {"directed_base_support", "directed_surgery", "prefix"}
LAMBDA_FIELDS = {"lambda_oracle", "lambda_support"}
BASE_FIELDS = {"base_columns"}
CORRELATION_FIELDS = {"correlation", "direct_canaries", "state_no_mutation"}
SECTION_FIELDS = {"section_witness"}
BLOCK_FIELDS = {"translation_block", "post_block_anchor"}
TARGET_FIELDS = {"target6"}
AFFINE_FIELDS = {"affine_system"}
PHASE_SEQUENCE = ["authenticated_input", "source_preflight",
    "fresh_immutable_prefix", "raw_lambda_oracle", "base_columns",
    "dual_correlation", "section_witness", "block_insertion",
    "target_reduction", "selected_proof"]


def expected_phase_sets(data: dict[str, Any]) -> set[frozenset[str]]:
    token, phase = data["terminal_token"], data["phase"]
    if token.endswith("UNKNOWN_INPUT"):
        return {frozenset()}
    if token.endswith("UNKNOWN_RESOURCE"):
        if phase == "receipt_serialization":
            base = frozenset(PHASE_SEQUENCE[:-1])
            return {base, frozenset(PHASE_SEQUENCE)}
        require(phase in PHASE_SEQUENCE, "checker timing resource phase")
        return {frozenset(PHASE_SEQUENCE[:PHASE_SEQUENCE.index(phase)])}
    require(phase == "complete", "checker timing normal phase")
    return ({frozenset(PHASE_SEQUENCE)} if token ==
            "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT" else
            {frozenset(PHASE_SEQUENCE[:-1])})


def stage_fields_before(phase: str) -> set[str]:
    groups = [AUTH_FIELDS, SOURCE_FIELDS, PREFIX_FIELDS, LAMBDA_FIELDS,
              BASE_FIELDS, CORRELATION_FIELDS, SECTION_FIELDS, BLOCK_FIELDS,
              TARGET_FIELDS, AFFINE_FIELDS]
    boundaries = {"authenticated_input": 0, "source_preflight": 1,
        "fresh_immutable_prefix": 2, "raw_lambda_oracle": 3,
        "base_columns": 4, "dual_correlation": 5,
        "section_witness": 6, "block_insertion": 7,
        "target_reduction": 8, "selected_proof": 10,
        "receipt_serialization": 8}
    require(phase in boundaries, "checker resource phase registry")
    result: set[str] = set()
    for group in groups[:boundaries[phase]]: result |= group
    return result


def expected_keys(data: dict[str, Any]) -> set[str]:
    token = data.get("terminal_token")
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT":
        return set(COMMON_KEYS)
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE":
        return set(COMMON_KEYS) | stage_fields_before(str(data.get("phase")))
    normal = (set(COMMON_KEYS) | AUTH_FIELDS | SOURCE_FIELDS | PREFIX_FIELDS |
              LAMBDA_FIELDS | BASE_FIELDS | CORRELATION_FIELDS | SECTION_FIELDS |
              BLOCK_FIELDS | TARGET_FIELDS | AFFINE_FIELDS)
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT":
        return normal | {"normalized_dual"}
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT":
        return normal | {"selected_proof"}
    raise RuntimeError("checker terminal registry")


def independent_upstream_caps(ed: Any, eg: Any) -> dict[str, int]:
    result = eg.independent_upstream_caps(ed)
    require(isinstance(result, dict) and all(isinstance(v, int)
            for v in result.values()), "checker upstream cap registry")
    return result


def _validate_block_progress_shape(current: dict[str, Any]) -> None:
    attempted = current["attempted_relators"]
    completed = current["completed_relators"]
    raw = current["raw_completed_relators"]
    shadow = current["shadow_completed_relators"]
    rank = current["rank_gain_so_far"]
    relator = current["current_relator"]
    require(all(isinstance(value, int) and not isinstance(value, bool)
                for value in (attempted, completed, raw, shadow, rank)) and
            0 <= attempted <= 11 and 0 <= completed <= 11 and
            0 <= shadow <= raw <= 11 and 0 <= rank <= completed and
            len(current["raw_prefix"]) == raw and
            len(current["shadow_prefix"]) == shadow and
            len(current["scalar_prefix"]) == shadow and
            len(current["block_prefix"]) == completed,
            "checker block progress counts")
    substage = current["substage"]
    if substage == "translation_section":
        require((attempted, completed, raw, shadow, rank) == (0, 0, 0, 0, 0)
                and relator is None and current["block_prefix"] == [],
                "checker translation-section atomic prefix")
    elif substage == "shadow_remainders":
        require(completed == rank == 0 and relator == attempted and
                1 <= attempted <= 11 and attempted in {raw, raw+1} and
                raw-shadow in {0, 1} and current["block_prefix"] == [],
                "checker shadow-remainder atomic prefix")
    elif substage == "persistent_columns":
        require(raw == shadow == 11 and relator == attempted and
                completed <= attempted <= completed+1 and
                1 <= attempted <= 11,
                "checker persistent-column atomic prefix")
    else:
        require(False, "checker registered block substage")


def _validate_completed_block_anchor(block: dict[str, Any],
                                     anchor: dict[str, Any]) -> None:
    keys = {"columns", "pivots", "dependent", "live_sparse_entries",
        "pool_size", "pool_order_sha256", "DAG_nodes", "DAG_edges",
        "section_bindings", "section_expression_nodes",
        "section_expression_edges"}
    pre, post = block["pre_accounting"], block["post_accounting"]
    require(set(pre) == keys and set(post) == keys and
            post["section_bindings"] == pre["section_bindings"]+1 and
            post["columns"] == pre["columns"]+11 and
            post["pivots"] == pre["pivots"]+block["rank_gain"] and
            post["dependent"] == pre["dependent"]+11-block["rank_gain"] and
            all(post[key] >= pre[key] for key in ("pool_size", "DAG_nodes",
                "DAG_edges", "section_expression_nodes",
                "section_expression_edges")),
            "checker complete block accounting relation")
    counts = {key: post[key] for key in
              ("columns", "pivots", "dependent", "live_sparse_entries")}
    require(anchor["basis_columns"] == post["columns"] and
            anchor["basis_pivots"] == post["pivots"] and
            anchor["basis_dependent"] == post["dependent"] and
            anchor["basis_live_sparse_entries"] == post["live_sparse_entries"]
            and anchor["pool_size"] == post["pool_size"] and
            anchor["DAG_nodes"] == post["DAG_nodes"] and
            anchor["DAG_edges"] == post["DAG_edges"] and
            anchor["section_bindings"] == post["section_bindings"] and
            anchor["anchor_semantic_sha256"] == sha_obj({
                "basis_counts": counts, "translation_hex": FIRST_T_HEX,
                "columns_sha256": block["raw_columns_sha256"]}),
            "checker post-block anchor/accounting binding")


def _validate_completed_public_shape(data: dict[str, Any], *,
                                     fixture: bool) -> None:
    """Independent closed shape/digest checks before arithmetic replay."""
    block = data["translation_block"]
    block_keys = {"complete", "translation_ordinal", "translation_hex",
        "section_newly_registered", "section_word_length",
        "section_word_sha256", "columns", "column_count", "column_order",
        "old_qstar_scalars", "raw_columns_sha256",
        "reducer_ledger_sha256", "pre_accounting", "post_accounting",
        "rank_gain", "shadow_rank_mod_B0", "two_rank_computations_equal",
        "relator9_independent", "pivot_count_before_relator9",
        "pivot_count_after_relator9", "lexfirst_active_provenance",
        "all_11_rows_are_D2_columns"}
    require(set(block) == block_keys and block["complete"] is True and
            block["translation_ordinal"] == 32976 and
            block["translation_hex"] == FIRST_T_HEX and
            block["section_newly_registered"] is True and
            block["section_word_length"] == 24 and
            block["section_word_sha256"] == FIRST_T_WORD_SHA and
            block["column_count"] == 11 and
            block["column_order"] == "relator indices 1 through 11" and
            block["two_rank_computations_equal"] is True and
            block["all_11_rows_are_D2_columns"] is True and
            block["raw_columns_sha256"] == sha_obj(
                [row["raw_column"] for row in block["columns"]]) and
            block["reducer_ledger_sha256"] == sha_obj(block["columns"]),
            "checker exact completed block shape/digests")
    column_keys = {"relator_index", "translation_ordinal",
        "translation_hex", "termwise_equals_direct_left_translation",
        "quotient_identity", "D1_D2_zero", "old_qstar_scalar",
        "independent", "pivot", "raw_column"}
    raw_keys = {"entries", "entry_count", "byte_length", "sha256",
                "encoding", "order"}
    for index, column in enumerate(block["columns"], 1):
        require(set(column) == column_keys and
                column["relator_index"] == index and
                column["translation_ordinal"] == 32976 and
                column["translation_hex"] == FIRST_T_HEX and
                column["termwise_equals_direct_left_translation"] is True and
                column["quotient_identity"] is True and
                column["D1_D2_zero"] is True and
                isinstance(column["independent"], bool),
                "checker exact completed block column")
        raw = column["raw_column"]
        require(set(raw) == raw_keys and
                raw["entry_count"] == len(raw["entries"]) and
                raw["entries"] == sorted(raw["entries"],
                    key=lambda row: (row[0], bytes.fromhex(row[1]))) and
                raw["encoding"] ==
                    "component-u8|E4-blob-154|coefficient-u8" and
                raw["order"] == "component then exact canonical E4 bytes" and
                raw["byte_length"] == len(_raw_bytes(raw["entries"], 154)) and
                raw["sha256"] == sha_bytes(_raw_bytes(raw["entries"], 154)),
                "checker exact completed raw column")
        pivot = column["pivot"]
        require((not column["independent"] and pivot is None) or
                (column["independent"] and isinstance(pivot, dict) and
                 set(pivot) == {"component", "element_hex", "reduced_row"}
                 and 1 <= pivot["component"] <= 6 and
                 len(bytes.fromhex(pivot["element_hex"])) == 154 and
                 set(pivot["reduced_row"]) == raw_keys),
                "checker exact completed pivot shape")
    _validate_block_reducer_contract(block["columns"],
        block["old_qstar_scalars"], block["pre_accounting"],
        block["post_accounting"], block["shadow_rank_mod_B0"],
        block["pivot_count_before_relator9"],
        block["pivot_count_after_relator9"], frozen_counts=not fixture)
    _validate_completed_block_anchor(block, data["post_block_anchor"])

    affine = data["affine_system"]
    affine_keys = {"variables", "rank", "nullity", "consistent",
        "equations", "row_space_sha256", "dual_witness",
        "dual_support_cap_noncontact", "complete_all_coordinates",
        "stopped_at_first_contradiction", "coordinate_encoding"}
    require(set(affine) == affine_keys and affine["variables"] == 108 and
            affine["rank"]+affine["nullity"] == 108 and
            isinstance(affine["equations"], int) and affine["equations"] > 0
            and affine["complete_all_coordinates"] is True and
            affine["stopped_at_first_contradiction"] is False and
            affine["coordinate_encoding"] ==
                "one-based component plus exact 154-byte blob",
            "checker exact affine public shape")
    target = data["target6"]
    common_target_keys = {"ordinal", "name",
        "base_is_direct_not_empty_formula",
        "affine_rhs_is_negative_base_remainder",
        "old_B0_remainder_or_dual_imported",
        "post_block_anchor_used_for_all_109", "target_row"}
    require(target["ordinal"] == 6 and
            target["name"] == "hexagon_1_coface_0" and
            target["base_is_direct_not_empty_formula"] is True and
            target["affine_rhs_is_negative_base_remainder"] is True and
            target["old_B0_remainder_or_dual_imported"] is False and
            target["post_block_anchor_used_for_all_109"] is True and
            target["target_row"]["consistent"] is affine["consistent"] and
            target["target_row"]["constraint_rank"] == affine["rank"] and
            target["target_row"]["nullity"] == affine["nullity"] and
            target["target_row"]["row_space_sha256"] ==
                affine["row_space_sha256"] and
            target["target_row"]["affine_equations"] == affine["equations"],
            "checker exact target6/affine binding")
    if fixture:
        expected = common_target_keys | {"base_remainder_sha256",
            "delta_rows_sha256", "noncommutative_formula_canary",
            "first_contradiction_canary"}
        canary = target["noncommutative_formula_canary"]
        contradiction = target["first_contradiction_canary"]
        require(set(target) == expected and
                set(canary) == {"operation", "g", "h", "ordered_value",
                    "reversed_value", "ordered_not_reversed"} and
                canary["operation"] ==
                    "PRODUCT(g,INVERSE(INVERSE(h)))" and
                canary["ordered_value"] != canary["reversed_value"] and
                canary["ordered_not_reversed"] is True and
                set(contradiction) == {"coordinate_ordinal",
                    "rows_after_coordinate", "full_equation_count",
                    "consistent_fixture"} and
                contradiction["coordinate_ordinal"] == 2 and
                contradiction["rows_after_coordinate"] == 107 and
                contradiction["full_equation_count"] ==
                    affine["equations"] == 109,
                "checker exact fixture target6 ledger")
    else:
        expected = common_target_keys | {"kind",
            "empty_formula_is_zero_delta_canary", "base_gradient",
            "base_gradient_sha256", "formula_checks",
            "formula_checks_sha256", "typed_split", "typed_split_sha256",
            "direct_gradient_bindings_sha256", "direct_vs_typed_count",
            "fresh_remainders", "fresh_remainder_count",
            "fresh_remainder_sha256", "old_157ec_comparison"}
        require(set(target) == expected and target["kind"] == "hexagon" and
                target["empty_formula_is_zero_delta_canary"] is True and
                target["base_gradient_sha256"] ==
                    sha_obj(target["base_gradient"]) and
                target["formula_checks_sha256"] ==
                    sha_obj(target["formula_checks"]) and
                target["typed_split_sha256"] ==
                    sha_obj(target["typed_split"]) and
                target["direct_vs_typed_count"] == 108 and
                len(target["typed_split"]) == 108 and
                target["fresh_remainder_count"] == 109 ==
                    len(target["fresh_remainders"]) and
                target["fresh_remainder_sha256"] ==
                    sha_obj(target["fresh_remainders"]) and
                target["old_157ec_comparison"] == {
                    "receipt_sha256":
                        "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
                    "old104_rank": 50, "full108_rank": 54,
                    "old104_comparison_sha256": OLD_TARGET6_ROW_SHA,
                    "evidence_only_not_imported": True},
                "checker exact production target6 ledger")


def validate_envelope(data: dict[str, Any], q3_path: Path,
                      upstream: dict[str, int], raw_length: int,
                      *, fixture: bool = False) -> None:
    require(set(data) == expected_keys(data) and data.get("schema") == SCHEMA and
            data.get("task_sha256") == TASK_SHA and
            data.get("terminal_token") == data.get("status") in TERMINALS and
            data["caps"] == CAPS and data["theorem_boundary"] == theorem_boundary()
            and set(data["upstream_caps"]) == {"registry", "sha256"} and
            data["upstream_caps"]["registry"] == upstream and
            data["upstream_caps"]["sha256"] == sha_obj(upstream),
            "checker exact envelope/contracts")
    if not fixture:
        require(data["pins"] == pin_rows(q3_path), "checker receipt pins")
    scope = data["monitor_scope"]
    require(set(scope) == {"contract", "registry", "registry_sha256",
        "registered_pair_count", "fresh_adapter_detached_after_prefix",
        "post_stage_adapters_detached", "resource_callback",
        "wildcards_or_inference_used", "deadline_or_RSS_epoch_reset",
        "receipt_serialization_is_outside_monitor"} and
        scope["contract"] == "one-clock-exact-outer-inner/v1" and
        scope["registry"] == MONITOR_REGISTRY and
        scope["registry_sha256"] == MONITOR_SHA and
        scope["registered_pair_count"] == sum(map(len, MONITOR_REGISTRY.values()))
        and scope["post_stage_adapters_detached"] is True and
        scope["fresh_adapter_detached_after_prefix"] is ("prefix" in data) and
        scope["wildcards_or_inference_used"] is False and
        scope["deadline_or_RSS_epoch_reset"] is False and
        scope["receipt_serialization_is_outside_monitor"] is True,
        "checker monitor contract")
    token = data["terminal_token"]
    block_complete = bool(data.get("translation_block", {}).get("complete"))
    require(data["claims"] == claim_row(token, block_complete),
            "checker exact claim boundary")
    perf = data["performance"]
    require(set(perf) == {"initial_remaining_seconds", "elapsed_seconds",
        "remaining_seconds", "checks", "peak_rss_bytes", "hit_reason",
        "receipt_bytes", "phase_seconds", "pair_loop_cadence",
        "block_relator_columns", "target6_remainder_probes",
        "full_E4_enumerations", "old_receipt_objects_imported",
        "cross_process_pool_ID_equality_used"} and
        isinstance(perf["initial_remaining_seconds"], (int, float)) and
        0 < perf["initial_remaining_seconds"] <= 18000 and
        perf["elapsed_seconds"] >= 0 and
        0 <= perf["remaining_seconds"] <= perf["initial_remaining_seconds"] and
        abs(perf["initial_remaining_seconds"]-perf["elapsed_seconds"]-
            perf["remaining_seconds"]) <= 2 and
        isinstance(perf["checks"], int) and perf["checks"] >= 0 and
        isinstance(perf["peak_rss_bytes"], int) and perf["peak_rss_bytes"] >= 0 and
        perf["receipt_bytes"] == raw_length and raw_length <=
            CAPS["packed_receipt_bytes"] and
        perf["pair_loop_cadence"] == 4096 and
        perf["block_relator_columns"] == 11 and
        perf["target6_remainder_probes"] == 109 and
        perf["full_E4_enumerations"] == 0 and
        perf["old_receipt_objects_imported"] == 0 and
        perf["cross_process_pool_ID_equality_used"] is False and
        frozenset(perf["phase_seconds"]) in expected_phase_sets(data) and
        all(isinstance(x, (int, float)) and x >= 0
            for x in perf["phase_seconds"].values()),
        "checker performance contract")
    guard = data["resource_guards"]
    require(set(guard) == {"resource_hit", "resource", "atomic_partial"} and
            guard["atomic_partial"] is True, "checker resource guard")
    if token.endswith("UNKNOWN_INPUT"):
        require(data["reason"] == "authenticated_input_failure" and
                data["phase"] == "authenticated_input" and data["input_errors"] and
                data["partial"] == {} and guard == {"resource_hit": False,
                    "resource": None, "atomic_partial": True} and
                perf["hit_reason"] is None, "checker input terminal")
        return
    if token.endswith("UNKNOWN_RESOURCE"):
        row = guard["resource"]
        require(guard["resource_hit"] is True and isinstance(row, dict) and
                set(row) == {"cap_reason", "cap_key", "cap_source", "cap_limit",
                    "observed_count", "comparator", "phase", "current"} and
                data["reason"] == row["cap_reason"] == row["cap_key"] and
                data["phase"] == row["phase"] and row["cap_source"] in
                    {"local", "upstream"} and row["comparator"] in {"gt", "ge"},
                "checker resource row")
        registry = CAPS if row["cap_source"] == "local" else upstream
        require(row["cap_key"] in registry and row["cap_limit"] ==
                registry[row["cap_key"]] and
                (row["observed_count"] > row["cap_limit"] if
                 row["comparator"] == "gt" else
                 row["observed_count"] >= row["cap_limit"]),
                "checker resource bound")
        partial = data["partial"]
        require(set(partial) == {"phase", "reason", "attempted_relators",
            "completed_relators", "raw_completed_relators",
            "shadow_completed_relators", "raw_column_prefix_sha256",
            "shadow_remainder_prefix_sha256", "old_qstar_prefix_sha256",
            "rank_gain_so_far",
            "source_evaluated_seeds", "source_records_prefix_sha256",
            "evaluated_seeds",
            "completed_equations", "current_seed", "block_digest_prefix",
            "block_pre_accounting", "block_post_accounting",
            "target_ledger_prefix_sha256", "completed_target_system",
            "rollback_anchor_after_block", "mathematical_claim"} and
            partial["phase"] == data["phase"] and
            partial["reason"] == data["reason"] and
            partial["mathematical_claim"] == "none" and
            perf["hit_reason"] == data["reason"], "checker resource partial")
        current = row["current"]
        if data["phase"] == "source_preflight":
            require(set(current) == {"current_seed", "evaluated_seeds",
                "records_prefix_sha256"} and
                0 <= current["evaluated_seeds"] <= 108 and
                partial["source_evaluated_seeds"] ==
                    current["evaluated_seeds"] and
                partial["source_records_prefix_sha256"] ==
                    current["records_prefix_sha256"],
                "checker source resource current")
        elif data["phase"] == "block_insertion":
            require(set(current) == {"attempted_relators",
                "completed_relators", "rank_gain_so_far", "block_prefix",
                "block_pre_accounting", "block_post_accounting",
                "current_relator", "substage", "raw_prefix",
                "shadow_prefix", "scalar_prefix", "raw_completed_relators",
                "shadow_completed_relators"},
                "checker block resource current keys")
            _validate_block_progress_shape(current)
            require(
                partial["attempted_relators"] == current["attempted_relators"]
                and partial["completed_relators"] ==
                    current["completed_relators"] and
                partial["raw_completed_relators"] ==
                    current["raw_completed_relators"] and
                partial["shadow_completed_relators"] ==
                    current["shadow_completed_relators"] and
                partial["raw_column_prefix_sha256"] ==
                    sha_obj(current["raw_prefix"]) and
                partial["shadow_remainder_prefix_sha256"] ==
                    sha_obj(current["shadow_prefix"]) and
                partial["old_qstar_prefix_sha256"] ==
                    sha_obj(current["scalar_prefix"]) and
                partial["rank_gain_so_far"] == current["rank_gain_so_far"] and
                partial["block_digest_prefix"] ==
                    (None if not current["block_prefix"] else
                     sha_obj(current["block_prefix"])) and
                partial["block_pre_accounting"] ==
                    current["block_pre_accounting"] and
                partial["block_post_accounting"] ==
                    current["block_post_accounting"],
                "checker block resource current")
        elif data["phase"] == "target_reduction":
            require(set(current) == {"substage", "evaluated_seeds",
                "completed_equations", "current_seed", "typed_split_prefix",
                "remainder_prefix", "completed_target_system"} and
                current["substage"] in {
                    "typed_formula_setup", "base_remainder",
                    "seed_remainder", "affine_absorption"} and
                partial["evaluated_seeds"] == current["evaluated_seeds"] and
                partial["completed_equations"] ==
                    current["completed_equations"] and
                partial["current_seed"] == current["current_seed"] and
                partial["target_ledger_prefix_sha256"] ==
                    sha_obj(current["typed_split_prefix"]) and
                partial["completed_target_system"] ==
                    current["completed_target_system"] and
                ((current["completed_target_system"] is None and
                  current["completed_equations"] == 0) or
                 (isinstance(current["completed_target_system"], dict) and
                  current["completed_equations"] ==
                    current["completed_target_system"]["equations"])),
                "checker target resource current")
            substage = current["substage"]
            if substage in {"typed_formula_setup", "base_remainder"}:
                require(current["evaluated_seeds"] == 0 and
                        current["completed_equations"] == 0 and
                        current["current_seed"] is None and
                        current["typed_split_prefix"] == [] and
                        current["remainder_prefix"] == [] and
                        current["completed_target_system"] is None,
                        "checker target setup/base atomic prefix")
            elif substage == "seed_remainder":
                require(1 <= current["current_seed"] <= 108 and
                        current["evaluated_seeds"]+1 ==
                            current["current_seed"] and
                        len(current["typed_split_prefix"]) ==
                            current["evaluated_seeds"] and
                        len(current["remainder_prefix"]) ==
                            current["evaluated_seeds"]+1 and
                        current["completed_equations"] == 0 and
                        current["completed_target_system"] is None,
                        "checker target seed atomic prefix")
            else:
                require(current["evaluated_seeds"] == 108 and
                        current["current_seed"] is None and
                        len(current["typed_split_prefix"]) == 108 and
                        len(current["remainder_prefix"]) == 109 and
                        current["completed_equations"] in {0,
                            (current["completed_target_system"] or {}).get(
                                "equations", -1)},
                        "checker affine absorption atomic prefix")
            completed_system = current["completed_target_system"]
            if completed_system is not None:
                require(row["cap_key"] == "dual_provenance_entries" and
                    set(completed_system) == {"coordinate_count", "rank",
                        "nullity", "consistent", "equations",
                        "row_space_sha256", "attempted_dual_support_count",
                        "attempted_dual_sha256"} and
                    completed_system["consistent"] is False and
                    completed_system["rank"]+completed_system["nullity"] ==
                        108 and
                    completed_system["coordinate_count"] ==
                        completed_system["equations"] and
                    completed_system["attempted_dual_support_count"] >
                        CAPS["dual_provenance_entries"],
                    "checker completed target dual-cap projection")
        elif data["phase"] == "selected_proof":
            require(current == {} or set(current) == {"evaluated_seeds",
                "completed_equations", "current_seed"},
                "checker selected resource current")
            require(partial["evaluated_seeds"] == 108 and
                    partial["completed_equations"] ==
                        data["affine_system"]["equations"] and
                    partial["current_seed"] is None and
                    partial["completed_target_system"] is None,
                    "checker selected-proof committed target")
        else:
            require(current == {} and partial["evaluated_seeds"] == 0 and
                    partial["completed_equations"] == 0 and
                    partial["current_seed"] is None and
                    partial["target_ledger_prefix_sha256"] is None and
                    partial["completed_target_system"] is None,
                    "checker pretarget/serialization resource current")
        if data["phase"] in {"target_reduction", "selected_proof",
                             "receipt_serialization"}:
            completed_block = data["translation_block"]
            require(partial["attempted_relators"] == 11 and
                    partial["completed_relators"] == 11 and
                    partial["raw_completed_relators"] == 11 and
                    partial["shadow_completed_relators"] == 11 and
                    partial["raw_column_prefix_sha256"] ==
                        completed_block["raw_columns_sha256"] and
                    partial["old_qstar_prefix_sha256"] ==
                        sha_obj(completed_block["old_qstar_scalars"]) and
                    partial["rank_gain_so_far"] ==
                        completed_block["rank_gain"] and
                    partial["block_digest_prefix"] ==
                        sha_obj(completed_block["columns"]) and
                    partial["block_pre_accounting"] ==
                        completed_block["pre_accounting"] and
                    partial["block_post_accounting"] ==
                        completed_block["post_accounting"] and
                    partial["rollback_anchor_after_block"] is True,
                    "checker completed block resource binding")
        callback = scope["resource_callback"]
        if row["cap_source"] == "local" and row["cap_key"] in {
                "common_math_soft_deadline_seconds", "producer_soft_rss_bytes"}:
            require(isinstance(callback, dict) and set(callback) ==
                    {"outer", "inner", "api"} and callback["outer"] == data["phase"]
                    and callback["inner"] in MONITOR_FROZEN[callback["outer"]]
                    and callback["api"] in {"check", "reserve"},
                    "checker resource callback")
        else:
            require(callback is None, "checker nonmonitor callback")
        return
    require(data["phase"] == "complete" and guard == {"resource_hit": False,
            "resource": None, "atomic_partial": True} and data["partial"] == {}
            and data["input_errors"] == [] and perf["hit_reason"] is None,
            "checker normal terminal")
    expected_reason = {
        "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT":
            "complete_target6_affine_system_consistent_with_selected_proof",
        "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT":
            "complete_target6_affine_system_inconsistent_with_normalized_dual",
    }[token]
    require(data["reason"] == expected_reason,
            "checker exact terminal reason")
    _validate_completed_public_shape(data, fixture=fixture)


def _raw_public(old: Any, vector: dict[int, int], pool: Any) \
        -> list[list[Any]]:
    rows = []
    for key, coefficient in vector.items():
        coefficient %= 3
        if coefficient:
            component, identifier = old.replay_unpack_key(key)
            rows.append([component, pool.values[identifier].hex(), coefficient])
    rows.sort(key=lambda row: (row[0], bytes.fromhex(row[1])))
    return rows


def _raw_bytes(rows: Sequence[Sequence[Any]], width: int) -> bytes:
    out = bytearray()
    for component, value_hex, coefficient in rows:
        value = bytes.fromhex(value_hex)
        require(1 <= component <= 6 and len(value) == width and
                coefficient in (1, 2), "checker raw bytes")
        out.append(component); out.extend(value); out.append(coefficient)
    return bytes(out)


def _raw_row(old: Any, vector: dict[int, int], pool: Any) -> dict[str, Any]:
    rows = _raw_public(old, vector, pool); raw = _raw_bytes(rows, pool.width)
    return {"entries": rows, "entry_count": len(rows),
        "byte_length": len(raw), "sha256": sha_bytes(raw),
        "encoding": "component-u8|E4-blob-154|coefficient-u8",
        "order": "component then exact canonical E4 bytes"}


def _semantic_rank(rows: Sequence[Sequence[Sequence[Any]]]) -> int:
    pivots: dict[tuple[int, str], dict[tuple[int, str], int]] = {}
    for public in rows:
        row = {(int(c), str(h)): int(a) % 3 for c, h, a in public if int(a) % 3}
        while row:
            pivot = min(row, key=lambda key: (key[0], bytes.fromhex(key[1])))
            basis = pivots.get(pivot)
            if basis is None:
                factor = 1 if row[pivot] == 1 else 2
                pivots[pivot] = {key: factor*value % 3
                    for key, value in row.items() if factor*value % 3}
                break
            coefficient = row[pivot]
            for key, value in basis.items():
                result = (row.get(key, 0)-coefficient*value) % 3
                if result: row[key] = result
                else: row.pop(key, None)
    return len(pivots)


def _validate_block_reducer_contract(ledger: Sequence[dict[str, Any]],
                                     scalar_rows: Sequence[int],
                                     pre: dict[str, Any],
                                     post: dict[str, Any],
                                     shadow_rank: int,
                                     pivots_before_9: int,
                                     pivots_after_9: int, *,
                                     frozen_counts: bool) -> int:
    require(len(ledger) == len(scalar_rows) == 11 and
            [row["relator_index"] for row in ledger] == list(range(1, 12)) and
            list(scalar_rows[:8]) == [0]*8 and scalar_rows[8] == 1 and
            all(row["old_qstar_scalar"] == scalar_rows[index]
                for index, row in enumerate(ledger)) and
            ledger[8]["independent"] is True and
            pivots_after_9 == pivots_before_9+1,
            "checker shared relator9 block theorem")
    gain = int(post["pivots"])-int(pre["pivots"])
    require(int(post["columns"]) == int(pre["columns"])+11 and
            int(post["dependent"]) == int(pre["dependent"])+(11-gain) and
            gain == shadow_rank and 1 <= gain <= 11,
            "checker shared block rank/accounting")
    if frozen_counts:
        require(pre["columns"] == 362725 and pre["pivots"] == 362709 and
                pre["dependent"] == 16 and post["columns"] == 362736 and
                post["pivots"] == 362709+gain and
                post["dependent"] == 16+(11-gain),
                "checker frozen B0/B1 accounting")
    return gain


def _project_prefix(data: dict[str, Any]) -> dict[str, Any]:
    names = {"counts", "accounting", "basis_gate", "prefix_pool_checkpoint",
        "dependent_events", "dependent_event_count", "dependent_event_sha256",
        "fresh_not_imported", "source_sha256"}
    return {"directed_surgery": data["directed_surgery"],
            "prefix": {name: data["prefix"][name] for name in names}}


def _require_resource_phase(data: dict[str, Any], phase: str) -> None:
    require(data["terminal_token"] ==
            "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE" and
            data["phase"] == phase and data["partial"]["phase"] == phase,
            "checker exact resource stage "+phase)


def _accounting_semantic(row: dict[str, Any]) -> dict[str, int]:
    require(set(row) == {"columns", "pivots", "dependent",
        "live_sparse_entries", "pool_size", "pool_order_sha256",
        "DAG_nodes", "DAG_edges", "section_bindings",
        "section_expression_nodes", "section_expression_edges"} and
        all(isinstance(row[key], int) and row[key] >= 0 for key in
            ("columns", "pivots", "dependent", "live_sparse_entries",
             "pool_size", "DAG_nodes", "DAG_edges", "section_bindings",
             "section_expression_nodes", "section_expression_edges")) and
        (row["pool_order_sha256"] is None or
         isinstance(row["pool_order_sha256"], str) and
         len(row["pool_order_sha256"]) == 64),
        "checker block accounting shape")
    return {key: int(row[key]) for key in
            ("columns", "pivots", "dependent", "live_sparse_entries")}


def _absorb_ordered_block_core(
        raw_rows: Sequence[dict[str, Any]], scalar_rows: Sequence[int],
        shadow_rows: Sequence[Sequence[Sequence[Any]]], pre: dict[str, Any],
        add_column: Callable[[int], tuple[bool, dict[str, Any] | None]],
        accounting: Callable[[], dict[str, Any]], *, frozen_counts: bool,
        trace: dict[str, int] | None = None) \
        -> tuple[list[dict[str, Any]], int, int, int, int, dict[str, Any]]:
    """Independent shared complete-block reducer for main and fixture paths."""
    if trace is not None:
        trace["block_core"] = trace.get("block_core", 0)+1
    require(len(raw_rows) == len(scalar_rows) == len(shadow_rows) == 11 and
            list(scalar_rows[:8]) == [0]*8 and scalar_rows[8] == 1,
            "checker shared block inputs")
    for row in raw_rows:
        require(set(row) == {"entries", "entry_count", "byte_length",
            "sha256", "encoding", "order"} and
            row["entry_count"] == len(row["entries"]) and
            row["encoding"] ==
                "component-u8|E4-blob-154|coefficient-u8" and
            row["order"] == "component then exact canonical E4 bytes" and
            row["entries"] == sorted(row["entries"],
                key=lambda item: (item[0], bytes.fromhex(item[1]))) and
            row["byte_length"] == len(_raw_bytes(row["entries"], 154)) and
            row["sha256"] == sha_bytes(_raw_bytes(row["entries"], 154)),
            "checker shared canonical raw row")
    shadow_rank = _semantic_rank(shadow_rows)
    ledger: list[dict[str, Any]] = []
    before9: int | None = None; after9: int | None = None
    for relator, raw_row in enumerate(raw_rows, 1):
        before = accounting()
        if relator == 9:
            before9 = int(before["pivots"])
        independent, pivot = add_column(relator)
        after = accounting()
        require(after["columns"] == before["columns"]+1 and
                after["pivots"]-before["pivots"] in (0, 1) and
                after["dependent"]-before["dependent"] in (0, 1) and
                independent == (after["pivots"] == before["pivots"]+1) and
                independent == (after["dependent"] == before["dependent"]),
                "checker shared block reducer outcome")
        ledger.append({"relator_index": relator,
            "translation_ordinal": 32976, "translation_hex": FIRST_T_HEX,
            "termwise_equals_direct_left_translation": True,
            "quotient_identity": True, "D1_D2_zero": True,
            "old_qstar_scalar": int(scalar_rows[relator-1]),
            "independent": independent, "pivot": pivot,
            "raw_column": raw_row})
        if relator == 9:
            after9 = int(after["pivots"])
            require(after9 == int(before9)+1 and independent,
                    "checker shared relator9 immediate pivot increment")
    require(before9 is not None and after9 is not None,
            "checker shared relator9 reached")
    post = accounting()
    gain = _validate_block_reducer_contract(
        ledger, scalar_rows, pre, post, shadow_rank, before9, after9,
        frozen_counts=frozen_counts)
    return ledger, gain, shadow_rank, before9, after9, post


def _replay_block(old: Any, e4: Any, pool: Any, basis: Any, oracle: Any,
                  claimed: dict[str, Any] | None, *, completed: int = 11,
                  raw_count: int = 11, shadow_count: int = 11) \
        -> tuple[dict[str, Any], int, list[dict[str, Any]]]:
    require(0 <= completed <= shadow_count <= raw_count <= 11,
            "checker block prefix lengths")
    t_blob = bytes.fromhex(FIRST_T_HEX); t = pool.unpack(t_blob)
    t_id = pool.intern(t)
    pre = {"columns": basis.columns_seen, "pivots": len(basis.rows),
        "dependent": basis.dependent, "live_sparse_entries": basis.live_entries,
        "pool_size": len(pool.values),
        "pool_order_sha256": sha_bytes(b"".join(pool.values))}
    raws = []; shadow = []; scalars = []
    for relator in range(1, raw_count+1):
        tick("checker block raw", True)
        vector: dict[int, int] = {}
        for key, coefficient in basis.columns[relator-1].items():
            component, identifier = old.replay_unpack_key(key)
            old.replay_add(vector, old.replay_pack_key(component,
                pool.mul_id(t_id, identifier)), coefficient)
        # A second termwise pass makes orientation and action independent of
        # ReplayBasis.add_column.
        manual: dict[int, int] = {}
        for key, coefficient in basis.columns[relator-1].items():
            component, identifier = old.replay_unpack_key(key)
            shifted = e4.mul(t, pool.value(identifier))
            old.replay_add(manual, old.replay_pack_key(component,
                pool.intern(shifted)), coefficient)
        require(vector == manual, "checker direct left translated column")
        raw_unpacked = {}
        for key, coefficient in vector.items():
            component, identifier = old.replay_unpack_key(key)
            old.add(raw_unpacked, (component, pool.value(identifier)), coefficient)
        require(old.boundary1(raw_unpacked, e4) == {}, "checker D1D2")
        raws.append(vector)
        if relator <= shadow_count:
            shadow.append([[c, h, a] for (c, h), a in sorted(
                old.checker_full_remainder(vector, basis, pool).items(),
                key=lambda row:(row[0][0], bytes.fromhex(row[0][1])))])
            scalars.append(oracle.packed(vector))
    if shadow_count >= 9:
        require(scalars[:8] == [0]*8 and scalars[8] == 1,
                "checker qstar relator1-9 theorem")
    shadow_rank = _semantic_rank(shadow); ledger = []

    def accounting() -> dict[str, Any]:
        return {"columns": basis.columns_seen, "pivots": len(basis.rows),
            "dependent": basis.dependent,
            "live_sparse_entries": basis.live_entries,
            "pool_size": len(pool.values),
            "pool_order_sha256": sha_bytes(b"".join(pool.values))}

    def add_column(relator: int) -> tuple[bool, dict[str, Any] | None]:
        before = set(basis.rows)
        independent = basis.add_column(relator, t_id)
        added = sorted(set(basis.rows)-before, key=pool.pivot_order)
        require(independent == (len(added) == 1),
                "checker block outcome")
        pivot_row = None
        if independent:
            pivot = added[0]
            component, identifier = old.replay_unpack_key(pivot)
            pivot_row = {"component": component,
                "element_hex": pool.values[identifier].hex(),
                "reduced_row": _raw_row(old, basis.rows[pivot], pool)}
        return independent, pivot_row

    if completed != 11:
        for relator in range(1, completed+1):
            independent, pivot_row = add_column(relator)
            ledger.append({"relator_index": relator,
                "translation_ordinal": 32976, "translation_hex": FIRST_T_HEX,
                "termwise_equals_direct_left_translation": True,
                "quotient_identity": True, "D1_D2_zero": True,
                "old_qstar_scalar": scalars[relator-1],
                "independent": independent, "pivot": pivot_row,
                "raw_column": _raw_row(old, raws[relator-1], pool)})
        post = accounting(); gain = len(basis.rows)-int(pre["pivots"])
        return {"pre_accounting": pre, "post_accounting": post,
                "rank_gain": gain, "old_qstar_scalars": scalars,
                "raw_rows": [_raw_row(old, row, pool) for row in raws],
                "shadow_rows": shadow,
                "shadow_rank_mod_B0": shadow_rank}, t_id, ledger
    require(claimed is not None, "checker complete block receipt")
    raw_rows = [_raw_row(old, row, pool) for row in raws]
    ledger, gain, shadow_rank, before9, after9_actual, post = \
        _absorb_ordered_block_core(raw_rows, scalars, shadow, pre,
            add_column, accounting, frozen_counts=True)
    expected = {"complete": True, "translation_ordinal": 32976,
        "translation_hex": FIRST_T_HEX,
        "section_newly_registered": True,
        "section_word_length": 24, "section_word_sha256": FIRST_T_WORD_SHA,
        "columns": ledger, "column_count": 11,
        "column_order": "relator indices 1 through 11",
        "old_qstar_scalars": scalars,
        "raw_columns_sha256": sha_obj([row["raw_column"] for row in ledger]),
        "reducer_ledger_sha256": sha_obj(ledger),
        "pre_accounting": pre, "post_accounting": post,
        "rank_gain": gain, "shadow_rank_mod_B0": shadow_rank,
        "two_rank_computations_equal": True, "relator9_independent": True,
        "pivot_count_before_relator9": before9,
        "pivot_count_after_relator9": after9_actual,
        "lexfirst_active_provenance": {"component": 4,
            "relator_index": 9, "scalar": 1,
            "translation_hex": FIRST_T_HEX,
            "section_word_sha256": FIRST_T_WORD_SHA},
        "all_11_rows_are_D2_columns": True}
    # ID allocation is not public equality.  Pool size/order and the boolean
    # saying whether the producer inserted a new pool binding are diagnostics;
    # all mathematical fields are compared exactly below.
    producer_projection = copy.deepcopy(claimed)
    checker_projection = copy.deepcopy(expected)
    producer_projection["pre_accounting"] = _accounting_semantic(
        producer_projection["pre_accounting"])
    producer_projection["post_accounting"] = _accounting_semantic(
        producer_projection["post_accounting"])
    for key in ("pre_accounting", "post_accounting"):
        checker_projection[key] = {name: checker_projection[key][name]
            for name in ("columns", "pivots", "dependent",
                         "live_sparse_entries")}
    require(producer_projection == checker_projection,
            "checker complete block semantic ledger")
    return expected, t_id, ledger


def _add(old: Any, left: dict[Any, int], right: dict[Any, int],
         coefficient: int = 1) -> dict[Any, int]:
    out = dict(left); old.add_scaled(out, right, coefficient); return out


def _classify_affine_system(system: Any, variables: int = 108) \
        -> dict[str, Any]:
    dual = system.dual_public()
    require(system.rank()+system.nullity() == variables and
            system.equations >= 1, "checker complete affine rank/nullity")
    if not system.consistent:
        require(isinstance(dual, dict) and dual["normalized_rhs"] == 1 and
                dual["yTz_mod3"] == 2 and
                dual["all_108_annihilation_dimension"] == variables and
                dual["support_count"] <= 109 and
                dual["support_count"] <= CAPS["dual_provenance_entries"],
                "checker normalized B1 dual")
    return {"variables": variables, "rank": system.rank(),
        "nullity": system.nullity(), "consistent": system.consistent,
        "equations": system.equations, "row_space_sha256": system.digest(),
        "dual_witness": dual, "dual_support_cap_noncontact": dual is None or
            dual["support_count"] <= 109 < CAPS["dual_provenance_entries"],
        "complete_all_coordinates": True,
        "stopped_at_first_contradiction": False,
        "coordinate_encoding":
            "one-based component plus exact 154-byte blob"}


def _validate_selected_literal_core(coefficients: Sequence[int],
                                    predicted: dict[Any, int],
                                    actual: dict[Any, int], value: Any,
                                    identity: Any) -> None:
    require(len(coefficients) == 108 and all(x in (0, 1, 2)
            for x in coefficients) and value == identity and
            actual == predicted,
            "checker selected literal affine replay")


def _validate_selected_public_contract(selected: dict[str, Any]) -> None:
    require(set(selected) == {"coefficient_vector",
        "coefficient_vector_sha256", "support", "factor_count",
        "typed_candidate", "target_expression", "direct_gradient",
        "direct_replay", "affine_prediction_equal", "D2_proof",
        "element_registry", "proof_root_node_id",
        "proof_expands_to_selected_gradient", "post_block_anchor_used",
        "targets_7_through_33_not_checked"} and
        len(selected["coefficient_vector"]) == 108 and
        selected["coefficient_vector_sha256"] ==
            sha_obj(selected["coefficient_vector"]) and
        selected["support"] == [index+1 for index, coefficient in
            enumerate(selected["coefficient_vector"]) if coefficient] and
        selected["factor_count"] == sum(selected["coefficient_vector"]) and
        selected["direct_replay"] is True and
        selected["affine_prediction_equal"] is True and
        selected["proof_expands_to_selected_gradient"] is True and
        selected["post_block_anchor_used"] is True and
        selected["targets_7_through_33_not_checked"] is True and
        isinstance(selected["proof_root_node_id"], int) and
        selected["proof_root_node_id"] >= 0,
        "checker selected public proof contract")


def _solve_transposed_target_core(old: Any, system: Any,
                                  base_remainder: dict[Any, int],
                                  delta_rows: dict[Any, dict[int, int]],
                                  live_remainder_entries: int, *,
                                  expected_coordinate_count: int | None = None,
                                  trace: dict[str, int] | None = None,
                                  allow_dual_over_cap: bool = False) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    if trace is not None:
        trace["target_reducer"] = trace.get("target_reducer", 0)+1
    require(all(value in (1, 2) for value in base_remainder.values()) and
            all(row and all(0 <= index < 108 and value in (1, 2)
                for index, value in row.items())
                for row in delta_rows.values()),
            "checker canonical sparse target rows")
    coordinate_count = len(set(base_remainder).union(delta_rows))
    if expected_coordinate_count is not None:
        require(coordinate_count == expected_coordinate_count,
                "checker expected target6 coordinate count")
    row = old.checker_target_row_transposed(
        system, base_remainder, delta_rows, 6, live_remainder_entries,
        "hexagon_1_coface_0")
    require(system.equations == coordinate_count and
            row["affine_equations"] == coordinate_count and
            row["ordinal"] == 6 and
            row["coordinate_count"] == coordinate_count,
            "checker shared target6 coordinate absorption")
    dual = system.dual_public()
    over_cap = (not system.consistent and isinstance(dual, dict) and
                dual["support_count"] > CAPS["dual_provenance_entries"])
    if over_cap:
        require(allow_dual_over_cap,
                "checker dual provenance support cap")
        affine = {"variables": 108, "rank": system.rank(),
            "nullity": system.nullity(), "consistent": False,
            "equations": system.equations,
            "row_space_sha256": system.digest(), "dual_witness": dual,
            "dual_support_cap_noncontact": False,
            "complete_all_coordinates": True,
            "stopped_at_first_contradiction": False,
            "coordinate_encoding":
                "one-based component plus exact 154-byte blob"}
    else:
        affine = _classify_affine_system(system)
    require(row["consistent"] is affine["consistent"] and
            row["constraint_rank"] == affine["rank"] and
            row["nullity"] == affine["nullity"] and
            row["row_space_sha256"] == affine["row_space_sha256"],
            "checker shared target6 classification")
    return row, affine


def _completed_target_system_projection(system: Any,
                                        coordinate_count: int) \
        -> dict[str, Any]:
    dual = system.dual_public()
    require(isinstance(dual, dict),
            "checker completed inconsistent target projection")
    return {"coordinate_count": coordinate_count,
        "rank": system.rank(), "nullity": system.nullity(),
        "consistent": False, "equations": system.equations,
        "row_space_sha256": system.digest(),
        "attempted_dual_support_count": dual["support_count"],
        "attempted_dual_sha256": sha_obj(dual)}


def _selected_replay_and_proof_core(
        coefficients: Sequence[int], selected: dict[str, Any],
        direct_replay: Callable[[], dict[str, Any]],
        proof_validator: Callable[[dict[str, Any]], None], *,
        trace: dict[str, int] | None = None) -> None:
    if trace is not None:
        trace["selected_core"] = trace.get("selected_core", 0)+1
    _validate_selected_public_contract(selected)
    require(selected["coefficient_vector"] == list(coefficients) and
            selected["coefficient_vector_sha256"] == sha_obj(coefficients) and
            selected["support"] == [index+1 for index, value in
                enumerate(coefficients) if value] and
            selected["factor_count"] == sum(coefficients),
            "checker canonical coefficient vector")
    replay = direct_replay()
    require(set(replay) == {"predicted", "actual", "value", "identity",
                            "context"},
            "checker selected replay callback shape")
    _validate_selected_literal_core(coefficients, replay["predicted"],
        replay["actual"], replay["value"], replay["identity"])
    proof_validator(replay)


def _target6(old: Any, e4: Any, seeds: dict[str, Any],
             source: dict[str, Any], inverse_words: Sequence[Any],
             pool: Any, basis: Any, data: dict[str, Any] | None, *,
             evaluated: int = 108, absorb: bool = True,
             allow_dual_over_cap: bool = False) \
        -> tuple[Any | None, dict[Any, int], dict[str, Any]]:
    require(0 <= evaluated <= 108, "checker target prefix count")
    require(len(seeds["seed_words"]) == 108 and
            sha_obj(seeds["seed_words"]) == SEED_MANIFEST_SHA and
            source["supported"] is True, "checker target handoff")
    mapping = old.cofaces(3)[0]
    r0 = old.substitute(old.embed_f2(old.hexagon_words(old.FIXED_WORD)[0]), mapping)
    base_raw, base_value = old.fox(r0, e4)
    base_binding = old.check_gradient_binding(
        "hexagon_1_coface_0", "hexagon", base_raw, base_value)
    require(base_value == e4.identity and sha_obj(base_binding) ==
            OLD_BASE_GRADIENT_SHA, "checker target6 base gradient")
    empty = old.checker_target6_public([], e4)
    empty_detail = old.checker_target6_formula([], e4, include_gradient=True)
    require(empty_detail["direct_gradient"] == {} and
            empty_detail["direct_value"] == e4.identity,
            "checker empty formula delta")
    base_rem = old.checker_probe_remainder(base_raw, pool, basis)
    delta_rows: dict[tuple[int, str], dict[int, int]] = {}
    split = []; remainder_rows = [{"ordinal": 0, "kind": "base",
        "remainder": [[c, h, a] for (c, h), a in sorted(base_rem.items(),
            key=lambda row:(row[0][0], bytes.fromhex(row[0][1])))],
        "sha256": sha_obj(sorted(base_rem.items()))}]
    formula_rows = [empty]; direct_bindings = [base_binding]; live = len(base_rem)
    for index, seed in enumerate(seeds["seed_words"][:evaluated], 1):
        tick("checker target6 seed", index % 4 == 0)
        detail = old.checker_target6_formula(seed, e4, include_gradient=True)
        delta = detail["direct_gradient"]
        require(detail["direct_value"] == e4.identity,
                "checker target6 delta quotient identity")
        formula_rows.append(old.checker_target6_public_from_detail(seed, detail))
        one = [0]*108; one[index-1] = 1
        typed = old.checker_make_typed_positive(one, seeds["seed_words"])
        targets = old.checker_build_typed_target6(typed)
        root = old.checker_select_typed_target_root(targets, 6)
        evaluator = old.CheckWordExprEvaluator(targets["dag"], e4)
        evaluator.evaluate_values([root]); typed_raw = evaluator.gradients([root])[root]
        value = evaluator.values[root-1]
        predicted = _add(old, base_raw, delta)
        require(value == e4.identity and typed_raw == predicted,
                "checker typed target6 formula equality")
        binding = old.check_gradient_binding(
            "hexagon_1_coface_0", "hexagon", typed_raw, value)
        split.append({"seed_index": index, "gradient_sha256": sha_obj(binding),
            "value_identity": True, "direct_replay": True,
            "typed_replay": True})
        direct_bindings.append(binding)
        rem = old.checker_probe_remainder(delta, pool, basis); live += len(rem)
        require(live <= CAPS["target_live_remainders"],
                "checker live remainder cap")
        for coordinate, coefficient in rem.items():
            delta_rows.setdefault(coordinate, {})[index-1] = coefficient
        remainder_rows.append({"ordinal": index, "kind": "delta",
            "entry_count": len(rem), "sha256": sha_obj(sorted(rem.items()))})
    prefix_public = {"typed_split": split, "remainder_rows": remainder_rows,
        "typed_split_sha256": sha_obj(split),
        "remainder_rows_sha256": sha_obj(remainder_rows),
        "evaluated_seeds": len(split), "live_remainder_entries": live}
    if evaluated != 108 or not absorb:
        return None, base_raw, prefix_public
    require(len(split) == 108 and sha_obj(split) == OLD_TYPED_SPLIT_SHA,
            "checker typed split ledger")
    system = old.CheckerAffineSystem(108, (e4.degree, e4.collector.n))
    row, affine = _solve_transposed_target_core(
        old, system, base_rem, delta_rows, live,
        allow_dual_over_cap=allow_dual_over_cap)
    expected_target = {"ordinal": 6, "name": "hexagon_1_coface_0",
        "kind": "hexagon", "base_is_direct_not_empty_formula": True,
        "affine_rhs_is_negative_base_remainder": True,
        "empty_formula_is_zero_delta_canary": True,
        "base_gradient": base_binding,
        "base_gradient_sha256": sha_obj(base_binding),
        "formula_checks": formula_rows,
        "formula_checks_sha256": sha_obj(formula_rows),
        "typed_split": split, "typed_split_sha256": sha_obj(split),
        "direct_gradient_bindings_sha256": sha_obj(direct_bindings),
        "direct_vs_typed_count": 108, "fresh_remainders": remainder_rows,
        "fresh_remainder_count": 109,
        "fresh_remainder_sha256": sha_obj(remainder_rows),
        "old_B0_remainder_or_dual_imported": False,
        "post_block_anchor_used_for_all_109": True, "target_row": row,
        "old_157ec_comparison": {"receipt_sha256":
            "d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d",
            "old104_rank": 50, "full108_rank": 54,
            "old104_comparison_sha256": OLD_TARGET6_ROW_SHA,
            "evidence_only_not_imported": True}}
    if data is not None:
        require(data["target6"] == expected_target,
                "checker target6 full ledger")
    if data is not None:
        require(data["affine_system"] == affine,
                "checker complete affine system")
    return system, base_raw, prefix_public


def _validate_selected(old: Any, e4: Any, inverse_words: Sequence[Any],
                       seeds: Sequence[Any], pool: Any, basis: Any,
                       system: Any, base_raw: dict[Any, int],
                       selected: dict[str, Any]) -> None:
    coefficients = system.canonical_solution()

    def direct_replay() -> dict[str, Any]:
        typed = old.checker_make_typed_positive(coefficients, seeds)
        public = {key: value for key, value in typed.items()
                  if key not in {"dag", "correction_word"}}
        public["correction_word"] = (None if typed["correction_word"] is None
            else list(typed["correction_word"]))
        public["correction_word_sha256"] = sha_obj(
            typed["correction_word"] if typed["correction_word"] is not None
            else {"typed_product_order": typed["typed_product_order"],
                  "coefficient_vector": typed["coefficient_vector"]})
        public["coefficient_vector_sha256"] = sha_obj(coefficients)
        named = [("f0_root", typed["f0_root"]),
                 ("correction_root", typed["correction_root"]),
                 ("candidate_root", typed["candidate_root"])]
        public["expression"] = typed["dag"].serialize(named)
        public["expression_root_names"] = [name for name, _ in named]
        require(selected["typed_candidate"] == public,
                "checker selected typed candidate")
        targets = old.checker_build_typed_target6(typed)
        root = old.checker_select_typed_target_root(targets, 6)
        evaluator = old.CheckWordExprEvaluator(targets["dag"], e4)
        evaluator.evaluate_values([root])
        gradient = evaluator.gradients([root])[root]
        value = evaluator.values[root-1]
        predicted = dict(base_raw)
        for index, coefficient in enumerate(coefficients):
            if coefficient:
                detail = old.checker_target6_formula(
                    seeds[index], e4, include_gradient=True)
                require(detail["direct_value"] == e4.identity,
                        "checker selected delta quotient identity")
                old.add_scaled(predicted, detail["direct_gradient"],
                               coefficient)
        require(selected["target_expression"] == targets["dag"].serialize(
                    [("hexagon_1_coface_0", root)]) and
                selected["direct_gradient"] == old.check_gradient_binding(
                    "hexagon_1_coface_0", "hexagon", gradient, value),
                "checker selected direct replay")
        return {"predicted": predicted, "actual": gradient, "value": value,
            "identity": e4.identity,
            "context": {"targets": targets, "root": root}}

    def proof_validator(replay: dict[str, Any]) -> None:
        gradient = replay["actual"]
        proof = selected["D2_proof"]
        sections = old.decode_section_expressions(
            proof["section_expressions"], e4)
        by_id, reverse = old.validate_registry(
            selected["element_registry"], {4: e4}, sections)

        def leaf(node: dict[str, Any]) -> Any:
            relator = int(node["relator_index"])
            external = int(node["translation_element_id"])
            require(1 <= relator <= 11 and external in by_id and
                    reverse.get((4, by_id[external])) == external,
                    "checker selected proof leaf")
            raw = {}
            for key, coefficient in basis.columns[relator-1].items():
                component, identifier = old.replay_unpack_key(key)
                old.add(raw, (component, pool.value(identifier)), coefficient)
            return old.translate(raw, by_id[external], e4)

        vectors, roots = old.checker_validate_selected_proof_payload(
            proof, ["hexagon_1_coface_0"], leaf,
            {"hexagon_1_coface_0": gradient})
        require(vectors["hexagon_1_coface_0"] == gradient and
                selected["proof_root_node_id"] ==
                    roots["hexagon_1_coface_0"],
                "checker selected proof binding")

    _selected_replay_and_proof_core(
        coefficients, selected, direct_replay, proof_validator)


def _validate_anchor_public(block: dict[str, Any], anchor: dict[str, Any],
                            *, frozen: bool,
                            live_basis_entries: int | None = None) -> None:
    anchor_keys = {"after_complete_block", "basis_columns", "basis_pivots",
        "basis_dependent", "basis_live_sparse_entries", "pool_size",
        "DAG_nodes", "DAG_edges", "section_bindings",
        "translation_retained", "anchor_semantic_sha256",
        "private_anchor_ids_not_exported"}
    require(set(anchor) == anchor_keys and
            anchor["after_complete_block"] is True and
            anchor["translation_retained"] is True and
            anchor["private_anchor_ids_not_exported"] is True,
            "checker post-block anchor shape")
    _validate_completed_block_anchor(block, anchor)
    if frozen:
        require(anchor["basis_columns"] == 362736 and
                anchor["basis_pivots"] == 362709+block["rank_gain"] and
                anchor["basis_dependent"] == 16+(11-block["rank_gain"]) and
                anchor["basis_live_sparse_entries"] == live_basis_entries,
                "checker frozen post-block anchor")


def _validate_completed_core(
        data: dict[str, Any],
        replay_block: Callable[[], dict[str, Any]],
        validate_anchor: Callable[[dict[str, Any]], None],
        replay_target: Callable[[], tuple[Any, dict[Any, int]]],
        validate_selected: Callable[[Any, dict[Any, int]], None],
        validate_dual: Callable[[Any], None], *,
        trace: dict[str, int] | None = None) -> None:
    """Shared normal checker sequence used by production and sealed toys."""
    if trace is not None:
        trace["completed_core"] = trace.get("completed_core", 0)+1
    block = replay_block()
    require(block["complete"] is True and
            block["section_newly_registered"] is True,
            "checker completed core block")
    validate_anchor(block)
    system, base_raw = replay_target()
    require(data["affine_system"]["consistent"] is system.consistent,
            "checker completed core affine branch")
    if data["terminal_token"] == \
            "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT":
        require(not system.consistent and "normalized_dual" in data and
                "selected_proof" not in data,
                "checker completed inconsistent branch")
        validate_dual(system)
    elif data["terminal_token"] == \
            "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT":
        require(system.consistent and "selected_proof" in data and
                "normalized_dual" not in data,
                "checker completed consistent branch")
        validate_selected(system, base_raw)
    else:
        require(False, "checker completed normal terminal")


def check_receipt(q3_path: Path, receipt_path: Path,
                  *, seconds: float = 18_000.0) -> dict[str, Any]:
    global CHECKER_STARTED, CHECKER_DEADLINE, CHECKER_CHECKS
    authenticate(); CHECKER_STARTED = time.monotonic()
    require(0 < seconds <= 18000, "checker deadline seconds")
    CHECKER_DEADLINE = CHECKER_STARTED+seconds; CHECKER_CHECKS = 0
    eh = load_eh_checker(); eg = eh.load_v1_checker()
    ed = eg.load_ed_checker(); old = ed.load_old()
    # One absolute end is propagated to both imported checker layers.
    eg.CHECKER_STARTED = CHECKER_STARTED; eg.CHECKER_DEADLINE = CHECKER_DEADLINE
    eg.CHECKER_CHECKS = 0; eg.configure_deadline_bridge(ed, old)
    raw = receipt_path.read_bytes(); data = json.loads(raw.decode("utf-8"))
    require(raw == (json.dumps(data, sort_keys=True,
            separators=(",", ":"))+"\n").encode("utf-8"),
            "checker canonical JSON")
    upstream = independent_upstream_caps(ed, eg)
    validate_envelope(data, q3_path, upstream, len(raw))
    if data["terminal_token"].endswith("UNKNOWN_INPUT"):
        return data
    if "base_q3_replay" not in data:
        _require_resource_phase(data, "authenticated_input")
        return data
    q3 = ed.load_q3(q3_path); e3, e4 = old.reconstruct(q3)
    tick("checker q3", True)
    old.validate_base_replay(data, q3, e3, e4)
    normalized, base_key, inverse_words = old.rebuild_normalized_inverse_fibre(
        q3, e4)
    require(data["normalized_inverse_fibre"] == normalized,
            "checker normalized inverse")
    seeds = old.affine_checker_seed_words(q3, e3)
    require(data["seed_manifest"] == seeds and
            sha_obj(seeds["seed_words"]) == SEED_MANIFEST_SHA,
            "checker seed universe")
    if "source_preflight" not in data:
        _require_resource_phase(data, "source_preflight")
        count = data["partial"]["source_evaluated_seeds"]
        prefix_source = old.checker_rebuild_occurrence_preflight(
            seeds["seed_words"][:count], e4, tuple(base_key))
        require(prefix_source["supported"] is True and
                len(prefix_source["records"]) == count and
                sha_obj(prefix_source["records"]) ==
                    data["partial"]["source_records_prefix_sha256"],
                "checker source resource prefix")
        return data
    source = old.checker_rebuild_occurrence_preflight(
        seeds["seed_words"], e4, tuple(base_key))
    require(data["source_preflight"] == source and source["supported"] is True,
            "checker source preflight")
    if "prefix" not in data:
        _require_resource_phase(data, "fresh_immutable_prefix")
        return data
    projected = _project_prefix(data)
    pool, basis, events = ed.replay_prefix(
        old, projected, e4, normalized, base_key)
    require(len(pool.values) == PREFIX_POOL_CHECKPOINT and
            data["prefix"]["pool_order_sha256"] == sha_bytes(b"".join(pool.values))
            and data["prefix"]["stable_rounds_projection_sha256"] ==
                PREFIX_STABLE_SHA and data["prefix"]["translations_sha256"] ==
                PREFIX_TRANSLATIONS_SHA and data["prefix"]["columns_sha256"] ==
                PREFIX_COLUMNS_SHA and data["prefix"]["blocker_history_sha256"] ==
                PREFIX_BLOCKERS_SHA, "checker extended fresh prefix")
    if "lambda_oracle" not in data:
        _require_resource_phase(data, "raw_lambda_oracle")
        return data
    oracle = ed.RawOracle(old, pool, basis,
                          ed.validate_qstar_label(ed.QSTAR, 154))
    pivots = [oracle.packed(row) for _, row in sorted(
        basis.rows.items(), key=lambda item: pool.pivot_order(item[0]))]
    require(pivots == [0]*362709, "checker qstar B0")
    oracle.public.update({"pivot_annihilation_count": len(pivots),
                          "pivot_annihilation_sha256": sha_obj(pivots)})
    require(data["lambda_oracle"] == oracle.public,
            "checker lambda oracle")
    support = eg.checker_lambda_support(oracle, 154)
    require(data["lambda_support"] == support and support["count"] == 78 and
            support["per_component"] == [43, 9, 11, 15, 0, 0],
            "checker lambda support")
    if "base_columns" not in data:
        _require_resource_phase(data, "base_columns")
        return data
    bundle = eg.checker_base_bundle(old, e4)
    require(data["base_columns"] == bundle["public"] and
            bundle["public"]["ordered_sha256"] == BASE_OCCURRENCE_SHA,
            "checker base columns")
    if "correlation" not in data:
        _require_resource_phase(data, "dual_correlation")
        return data
    mul = e4.mul; inverse = e4.inverse
    checker_before = {"pool_size": len(pool.values),
        "pool_sha256": sha_bytes(b"".join(pool.values)),
        "basis_columns": basis.columns_seen, "basis_pivots": len(basis.rows),
        "basis_dependent": basis.dependent,
        "basis_live_sparse_entries": basis.live_entries}
    corr = eg.independent_correlation(support["rows"],
        bundle["private_occurrences"], width=154, unpack=pool.unpack,
        mul=mul, inverse=inverse, pack=lambda x: bytes(x[0])+bytes(x[1]))
    canaries = eg.independent_canaries(corr, support["rows"],
        bundle["private_occurrences"], e4.identity, pool.unpack, mul,
        lambda x: bytes(x[0])+bytes(x[1]))
    require(data["correlation"] == corr["public"] and
            data["direct_canaries"] == canaries and
            corr["public"]["packed_rows_sha256"] == CORRELATION_SHA and
            corr["public"]["first_active"] == {"translation_hex": FIRST_T_HEX,
                "relator_index": 9, "scalar": 1} and
            corr["first_contributing_pair"]["component"] == 4 and
            corr["first_contributing_pair"]["relator_index"] == 9,
            "checker complete correlation")
    checker_after = {"pool_size": len(pool.values),
        "pool_sha256": sha_bytes(b"".join(pool.values)),
        "basis_columns": basis.columns_seen, "basis_pivots": len(basis.rows),
        "basis_dependent": basis.dependent,
        "basis_live_sparse_entries": basis.live_entries}
    state = data["state_no_mutation"]
    state_keys = {"pool_size", "pool_ids", "pool_order_sha256",
        "basis_pivots", "basis_live_sparse_entries", "basis_columns",
        "DAG_nodes", "DAG_edges", "section_bindings",
        "section_expression_nodes", "section_expression_edges"}
    require(checker_before == checker_after and
            set(state) == {"before", "after", "exact_equal",
                "pool_ID_or_basis_mutation"} and
            set(state["before"]) == state_keys and
            set(state["after"]) == state_keys and
            state["before"] == state["after"] and
            state["exact_equal"] is True and
            state["pool_ID_or_basis_mutation"] is False,
            "checker independent correlation state neutrality")
    if "section_witness" not in data:
        _require_resource_phase(data, "section_witness")
        return data
    eg.validate_section_witness(old, e4, data,
                                bundle["private_occurrences"], corr)
    require(data["section_witness"]["direct_replay"]["g_word_sha256"] ==
                FIRST_G_WORD_SHA and
            data["section_witness"]["direct_replay"]["t_word_sha256"] ==
                FIRST_T_WORD_SHA and
            data["section_witness"]["section_expressions"]["manifest_sha256"] ==
                SECTION_MANIFEST_SHA, "checker section fixed evidence")
    if "translation_block" not in data:
        _require_resource_phase(data, "block_insertion")
        current = data["resource_guards"]["resource"]["current"]
        completed = int(data["partial"]["completed_relators"])
        partial_block, _, ledger = _replay_block(
            old, e4, pool, basis, oracle, None, completed=completed,
            raw_count=current["raw_completed_relators"],
            shadow_count=current["shadow_completed_relators"])
        require(current["raw_prefix"] == partial_block["raw_rows"] and
                current["shadow_prefix"] == partial_block["shadow_rows"] and
                current["scalar_prefix"] ==
                    partial_block["old_qstar_scalars"] and
                current["block_prefix"] == ledger and
                data["partial"]["block_digest_prefix"] ==
                    (None if not ledger else sha_obj(ledger)) and
                _accounting_semantic(current["block_pre_accounting"]) ==
                    {key: partial_block["pre_accounting"][key] for key in
                     ("columns", "pivots", "dependent",
                      "live_sparse_entries")} and
                _accounting_semantic(current["block_post_accounting"]) ==
                    {key: partial_block["post_accounting"][key] for key in
                     ("columns", "pivots", "dependent",
                      "live_sparse_entries")} and
                current["rank_gain_so_far"] == partial_block["rank_gain"],
                "checker block resource prefix replay")
        return data
    if "target6" in data and data["terminal_token"] in {
            "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT",
            "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT"}:
        def replay_completed_block() -> dict[str, Any]:
            replayed, _, _ = _replay_block(
                old, e4, pool, basis, oracle, data["translation_block"])
            return replayed

        def validate_completed_anchor(replayed: dict[str, Any]) -> None:
            _validate_anchor_public(replayed, data["post_block_anchor"],
                frozen=True, live_basis_entries=basis.live_entries)

        def replay_completed_target() -> tuple[Any, dict[Any, int]]:
            system, base_raw, _ = _target6(
                old, e4, seeds, source, inverse_words, pool, basis, data)
            require(system is not None, "checker complete target system")
            return system, base_raw

        def validate_completed_selected(system: Any,
                                        base_raw: dict[Any, int]) -> None:
            _validate_selected(old, e4, inverse_words, seeds["seed_words"],
                pool, basis, system, base_raw, data["selected_proof"])

        def validate_completed_dual(system: Any) -> None:
            system.verify_dual(data["normalized_dual"])
            require(data["normalized_dual"] ==
                    data["affine_system"]["dual_witness"],
                    "checker normalized dual receipt")

        _validate_completed_core(data, replay_completed_block,
            validate_completed_anchor, replay_completed_target,
            validate_completed_selected, validate_completed_dual)
        tick("checker complete", True)
        return data
    block, translation_id, _ = _replay_block(
        old, e4, pool, basis, oracle, data["translation_block"])
    del translation_id
    anchor = data["post_block_anchor"]
    anchor_keys = {"after_complete_block", "basis_columns", "basis_pivots",
        "basis_dependent", "basis_live_sparse_entries", "pool_size",
        "DAG_nodes", "DAG_edges", "section_bindings",
        "translation_retained", "anchor_semantic_sha256",
        "private_anchor_ids_not_exported"}
    semantic_counts = {"columns": anchor["basis_columns"],
        "pivots": anchor["basis_pivots"],
        "dependent": anchor["basis_dependent"],
        "live_sparse_entries": anchor["basis_live_sparse_entries"]}
    require(set(anchor) == anchor_keys and
            anchor["after_complete_block"] is True and
            anchor["basis_columns"] == 362736 and
            anchor["basis_pivots"] == 362709+block["rank_gain"] and
            anchor["basis_dependent"] == 16+(11-block["rank_gain"]) and
            anchor["basis_live_sparse_entries"] == basis.live_entries and
            all(isinstance(anchor[key], int) and anchor[key] >= 0 for key in
                ("pool_size", "DAG_nodes", "DAG_edges", "section_bindings")) and
            anchor["translation_retained"] is True and
            anchor["private_anchor_ids_not_exported"] is True and
            anchor["anchor_semantic_sha256"] == sha_obj({
                "basis_counts": semantic_counts,
                "translation_hex": FIRST_T_HEX,
                "columns_sha256": block["raw_columns_sha256"]}),
            "checker post-block anchor")
    _validate_completed_block_anchor(data["translation_block"], anchor)
    if "target6" not in data:
        if data["phase"] == "receipt_serialization":
            _require_resource_phase(data, "receipt_serialization")
            return data
        _require_resource_phase(data, "target_reduction")
        current = data["resource_guards"]["resource"]["current"]
        count = int(data["partial"]["evaluated_seeds"])
        _, _, target_prefix = _target6(old, e4, seeds, source,
            inverse_words, pool, basis, None, evaluated=count, absorb=False)
        require(current["typed_split_prefix"] == target_prefix["typed_split"]
                and data["partial"]["target_ledger_prefix_sha256"] ==
                    target_prefix["typed_split_sha256"],
                "checker target resource typed prefix")
        if current["substage"] in {"seed_remainder", "affine_absorption"}:
            require(current["remainder_prefix"] ==
                    target_prefix["remainder_rows"],
                    "checker target resource remainder prefix")
        if data["partial"]["completed_equations"]:
            require(data["reason"] == "dual_provenance_entries" and
                    isinstance(data["partial"]["completed_target_system"],
                               dict),
                    "checker completed-system resource reason")
            full_system, _, _ = _target6(old, e4, seeds, source,
                inverse_words, pool, basis, None, evaluated=108, absorb=True,
                allow_dual_over_cap=True)
            require(full_system is not None and full_system.equations ==
                    data["partial"]["completed_equations"] and
                    _completed_target_system_projection(
                        full_system, full_system.equations) ==
                    data["partial"]["completed_target_system"],
                    "checker target completed-system resource projection")
        else:
            require(data["partial"]["completed_target_system"] is None,
                    "checker incomplete target has no system projection")
        return data
    system, base_raw, _ = _target6(old, e4, seeds, source, inverse_words,
        pool, basis, data)
    require(system is not None, "checker complete target system")
    token = data["terminal_token"]
    if token == "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT":
        system.verify_dual(data["normalized_dual"])
        require(data["normalized_dual"] == data["affine_system"]["dual_witness"],
                "checker normalized dual receipt")
    elif token == "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT":
        require(system.consistent, "checker consistent system")
        _validate_selected(old, e4, inverse_words, seeds["seed_words"], pool,
                           basis, system, base_raw, data["selected_proof"])
    else:
        _require_resource_phase(data, "selected_proof")
        return data
    tick("checker complete", True)
    return data


def _expect_failure(action: Callable[[], Any], label: str) -> None:
    try:
        action()
    except (RuntimeError, ValueError, TypeError, AttributeError):
        return
    raise RuntimeError("157ei checker mutation accepted: "+label)


def _fixture_accounting(columns: int, pivots: int, dependent: int,
                        live: int) -> dict[str, Any]:
    registered = 0 if columns == 0 else 1
    return {"columns": columns, "pivots": pivots, "dependent": dependent,
        "live_sparse_entries": live, "pool_size": 16+pivots,
        "pool_order_sha256": sha_obj([columns, pivots, dependent, live]),
        "DAG_nodes": 1+pivots, "DAG_edges": pivots,
        "section_bindings": registered, "section_expression_nodes": 1,
        "section_expression_edges": 0}


def _fixture_block(trace: dict[str, int]) -> tuple[dict[str, Any], dict[str, Any]]:
    vectors = [{index: 1} for index in range(1, 12)]
    blobs = [(bytes([index])+bytes(153)).hex()
             for index in range(1, 12)]
    raw_rows = [{"entries": [[1, blobs[index-1], 1]],
        "entry_count": 1, "byte_length": 156,
        "sha256": sha_bytes(bytes([1])+bytes.fromhex(blobs[index-1])+
                            bytes([1])),
        "encoding": "component-u8|E4-blob-154|coefficient-u8",
        "order": "component then exact canonical E4 bytes"}
        for index in range(1, 12)]
    shadow = [[[1, blobs[index-1], 1]] for index in range(1, 12)]
    scalars = [0]*8+[1, 0, 0]
    pivots: dict[int, dict[int, int]] = {}; columns = dependent = 0
    pre = _fixture_accounting(0, 0, 0, 0)

    def accounting() -> dict[str, Any]:
        return _fixture_accounting(columns, len(pivots), dependent,
                                   len(pivots))

    def add_column(relator: int) -> tuple[bool, dict[str, Any] | None]:
        nonlocal columns, dependent
        row = dict(vectors[relator-1])
        while row:
            pivot = min(row); prior = pivots.get(pivot)
            if prior is None:
                pivots[pivot] = row; break
            coefficient = row[pivot]
            for key, value in prior.items():
                result = (row.get(key, 0)-coefficient*value) % 3
                if result: row[key] = result
                else: row.pop(key, None)
        independent = bool(row); columns += 1
        if not independent: dependent += 1
        pivot_public = None if not independent else {"component": 1,
            "element_hex": blobs[relator-1],
            "reduced_row": raw_rows[relator-1]}
        return independent, pivot_public

    ledger, gain, rank, before9, after9, post = \
        _absorb_ordered_block_core(raw_rows, scalars, shadow, pre,
            add_column, accounting, frozen_counts=False, trace=trace)
    block = {"complete": True, "translation_ordinal": 32976,
        "translation_hex": FIRST_T_HEX, "section_newly_registered": True,
        "section_word_length": 24, "section_word_sha256": FIRST_T_WORD_SHA,
        "columns": ledger, "column_count": 11,
        "column_order": "relator indices 1 through 11",
        "old_qstar_scalars": scalars,
        "raw_columns_sha256": sha_obj([row["raw_column"] for row in ledger]),
        "reducer_ledger_sha256": sha_obj(ledger),
        "pre_accounting": pre, "post_accounting": post,
        "rank_gain": gain, "shadow_rank_mod_B0": rank,
        "two_rank_computations_equal": True,
        "relator9_independent": True,
        "pivot_count_before_relator9": before9,
        "pivot_count_after_relator9": after9,
        "lexfirst_active_provenance": {"component": 4,
            "relator_index": 9, "scalar": 1,
            "translation_hex": FIRST_T_HEX,
            "section_word_sha256": FIRST_T_WORD_SHA},
        "all_11_rows_are_D2_columns": True}
    counts = {"columns": 11, "pivots": gain, "dependent": 11-gain,
              "live_sparse_entries": gain}
    anchor = {"after_complete_block": True, "basis_columns": 11,
        "basis_pivots": gain, "basis_dependent": 11-gain,
        "basis_live_sparse_entries": gain, "pool_size": 16+gain,
        "DAG_nodes": 1+gain, "DAG_edges": gain, "section_bindings": 1,
        "translation_retained": True,
        "anchor_semantic_sha256": sha_obj({"basis_counts": counts,
            "translation_hex": FIRST_T_HEX,
            "columns_sha256": block["raw_columns_sha256"]}),
        "private_anchor_ids_not_exported": True}
    return block, anchor


def _fixture_affine(old: Any, consistent: bool, trace: dict[str, int]) \
        -> tuple[Any, dict[str, Any], dict[str, Any]]:
    system = old.CheckerAffineSystem(108, (1, 0))
    base: dict[tuple[int, str], int] = {}
    deltas: dict[tuple[int, str], dict[int, int]] = {}
    base[(1, "00")] = 2
    base[(1, "01")] = 2 if consistent else 1
    deltas[(1, "00")] = {0: 1}
    deltas[(1, "01")] = {0: 1}
    for index in range(1, 108):
        deltas[(1, f"{index+1:02x}")] = {index: 1}
    row, public = _solve_transposed_target_core(
        old, system, base, deltas,
        len(base)+sum(len(item) for item in deltas.values()),
        expected_coordinate_count=109, trace=trace)
    require(public["consistent"] is consistent and
            row["coordinate_count"] == 109,
            "checker fixture complete affine solve")
    def mul(left: tuple[int, ...], right: tuple[int, ...]) \
            -> tuple[int, ...]:
        return tuple(left[right[index]-1] for index in range(3))
    g = (2, 3, 1); h = (2, 1, 3); ordered = mul(g, h)
    require(ordered != mul(h, g),
            "checker fixture target noncommutativity")
    target = {"ordinal": 6, "name": "hexagon_1_coface_0",
        "base_is_direct_not_empty_formula": True,
        "affine_rhs_is_negative_base_remainder": True,
        "base_remainder_sha256": sha_obj(sorted(base.items())),
        "delta_rows_sha256": sha_obj(sorted(deltas.items())),
        "target_row": row, "noncommutative_formula_canary": {
            "operation": "PRODUCT(g,INVERSE(INVERSE(h)))",
            "g": list(g), "h": list(h), "ordered_value": list(ordered),
            "reversed_value": list(mul(h, g)), "ordered_not_reversed": True},
        "first_contradiction_canary": {"coordinate_ordinal": 2,
            "rows_after_coordinate": 107,
            "full_equation_count": system.equations,
            "consistent_fixture": consistent},
        "old_B0_remainder_or_dual_imported": False,
        "post_block_anchor_used_for_all_109": True}
    return system, public, target


def _fixture_selected(system: Any, trace: dict[str, int]) -> dict[str, Any]:
    coefficients = system.canonical_solution()

    def mul(left: tuple[int, ...], right: tuple[int, ...]) \
            -> tuple[int, ...]:
        return tuple(left[right[index]-1] for index in range(3))

    identity = (1, 2, 3); g = (2, 3, 1); h = (2, 1, 3)
    require(mul(g, h) != mul(h, g),
            "checker fixture noncommutative selected replay")
    literal = mul(g, h)
    selected = {"coefficient_vector": list(coefficients),
        "coefficient_vector_sha256": sha_obj(coefficients),
        "support": [i+1 for i, value in enumerate(coefficients) if value],
        "factor_count": sum(coefficients),
        "typed_candidate": {"fixture": "ordered-noncommutative-literal",
            "value": list(literal)},
        "target_expression": {"fixture": "typed-target6-product"},
        "direct_gradient": {"fixture": "nonzero-base-direct"},
        "direct_replay": True, "affine_prediction_equal": True,
        "D2_proof": {"roots": [{"name": "hexagon_1_coface_0",
                                  "node_id": 0}]},
        "element_registry": [], "proof_root_node_id": 0,
        "proof_expands_to_selected_gradient": True,
        "post_block_anchor_used": True,
        "targets_7_through_33_not_checked": True}

    def direct_replay() -> dict[str, Any]:
        gradient = {("toy", literal): 1}
        return {"predicted": dict(gradient), "actual": gradient,
            "value": identity, "identity": identity,
            "context": {"literal": literal}}

    def proof_validator(replay: dict[str, Any]) -> None:
        require(replay["context"]["literal"] == literal and
                selected["D2_proof"]["roots"] == [{
                    "name": "hexagon_1_coface_0", "node_id": 0}] and
                selected["proof_root_node_id"] == 0,
                "checker fixture selected proof")

    _selected_replay_and_proof_core(
        coefficients, selected, direct_replay, proof_validator, trace=trace)
    return selected


def _fixture_scope(callback: dict[str, str] | None,
                   *, fresh: bool) -> dict[str, Any]:
    return {"contract": "one-clock-exact-outer-inner/v1",
        "registry": MONITOR_REGISTRY, "registry_sha256": MONITOR_SHA,
        "registered_pair_count": sum(map(len, MONITOR_REGISTRY.values())),
        "fresh_adapter_detached_after_prefix": fresh,
        "post_stage_adapters_detached": True,
        "resource_callback": callback,
        "wildcards_or_inference_used": False,
        "deadline_or_RSS_epoch_reset": False,
        "receipt_serialization_is_outside_monitor": True}


def _fixture_performance(hit: str | None = None,
                         phases: Sequence[str] = ()) -> dict[str, Any]:
    return {"initial_remaining_seconds": 30.0, "elapsed_seconds": 0.0,
        "remaining_seconds": 30.0, "checks": 0, "peak_rss_bytes": 0,
        "hit_reason": hit, "receipt_bytes": 0,
        "phase_seconds": {name: 0.0 for name in phases},
        "pair_loop_cadence": 4096, "block_relator_columns": 11,
        "target6_remainder_probes": 109, "full_E4_enumerations": 0,
        "old_receipt_objects_imported": 0,
        "cross_process_pool_ID_equality_used": False}


def _fixture_common(token: str) -> dict[str, Any]:
    return {"schema": SCHEMA, "task_sha256": TASK_SHA,
        "terminal_token": token, "status": token, "reason": "",
        "phase": "authenticated_input", "pins": {}, "caps": CAPS,
        "upstream_caps": {"registry": {}, "sha256": sha_obj({})},
        "claims": claim_row(token, False), "theorem_boundary": theorem_boundary(),
        "monitor_scope": _fixture_scope(None, fresh=False),
        "resource_guards": {"resource_hit": False, "resource": None,
                            "atomic_partial": True},
        "partial": {}, "input_errors": [],
        "performance": _fixture_performance()}


def _fixture_normal(token: str, block: dict[str, Any], anchor: dict[str, Any],
                    target: dict[str, Any], affine: dict[str, Any],
                    selected: dict[str, Any] | None) \
        -> dict[str, Any]:
    row = _fixture_common(token)
    for name in AUTH_FIELDS | SOURCE_FIELDS | PREFIX_FIELDS | LAMBDA_FIELDS | \
            BASE_FIELDS | CORRELATION_FIELDS | SECTION_FIELDS:
        row[name] = {}
    row["translation_block"] = block; row["post_block_anchor"] = anchor
    row["target6"] = target
    row["affine_system"] = affine; row["phase"] = "complete"
    row["claims"] = claim_row(token, True)
    row["monitor_scope"] = _fixture_scope(None, fresh=True)
    if token.endswith("INCONSISTENT"):
        row["reason"] = \
            "complete_target6_affine_system_inconsistent_with_normalized_dual"
        row["normalized_dual"] = affine["dual_witness"]
    else:
        require(selected is not None, "checker fixture selected receipt")
        row["reason"] = \
            "complete_target6_affine_system_consistent_with_selected_proof"
        row["selected_proof"] = selected
    completed = PHASE_SEQUENCE if token == \
        "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT" else PHASE_SEQUENCE[:-1]
    row["performance"] = _fixture_performance(None, completed)
    validate_envelope(row, ROOT/Q3_PATH, {}, 0, fixture=True)
    return row


def _fixture_block_resource(raw_rows: Sequence[dict[str, Any]],
                            shadow_rows: Sequence[Any]) -> dict[str, Any]:
    token = "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE"
    row = _fixture_common(token)
    for name in stage_fields_before("block_insertion"):
        row[name] = {}
    pre = {"columns": 0, "pivots": 0, "dependent": 0,
        "live_sparse_entries": 0, "pool_size": 16,
        "pool_order_sha256": sha_obj([]), "DAG_nodes": 1,
        "DAG_edges": 0, "section_bindings": 0,
        "section_expression_nodes": 0, "section_expression_edges": 0}
    current = {"attempted_relators": 3, "completed_relators": 0,
        "rank_gain_so_far": 0, "block_prefix": [],
        "block_pre_accounting": pre, "block_post_accounting": pre,
        "current_relator": 3, "substage": "shadow_remainders",
        "raw_prefix": list(raw_rows[:3]),
        "shadow_prefix": list(shadow_rows[:2]),
        "scalar_prefix": [0, 0], "raw_completed_relators": 3,
        "shadow_completed_relators": 2}
    reason = "common_math_soft_deadline_seconds"
    resource = {"cap_reason": reason, "cap_key": reason,
        "cap_source": "local", "cap_limit": CAPS[reason],
        "observed_count": CAPS[reason], "comparator": "ge",
        "phase": "block_insertion", "current": current}
    row.update({"reason": reason, "phase": "block_insertion",
        "claims": claim_row(token, False),
        "monitor_scope": _fixture_scope({"outer": "block_insertion",
            "inner": "block_insertion", "api": "check"}, fresh=True),
        "resource_guards": {"resource_hit": True, "resource": resource,
                            "atomic_partial": True},
        "performance": _fixture_performance(reason,
            PHASE_SEQUENCE[:PHASE_SEQUENCE.index("block_insertion")])})
    row["partial"] = {"phase": "block_insertion", "reason": reason,
        "attempted_relators": 3, "completed_relators": 0,
        "raw_completed_relators": 3, "shadow_completed_relators": 2,
        "raw_column_prefix_sha256": sha_obj(current["raw_prefix"]),
        "shadow_remainder_prefix_sha256": sha_obj(current["shadow_prefix"]),
        "old_qstar_prefix_sha256": sha_obj([0, 0]),
        "rank_gain_so_far": 0, "source_evaluated_seeds": 0,
        "source_records_prefix_sha256": None, "evaluated_seeds": 0,
        "completed_equations": 0, "current_seed": None,
        "block_digest_prefix": None, "block_pre_accounting": pre,
        "block_post_accounting": pre,
        "target_ledger_prefix_sha256": None,
        "completed_target_system": None,
        "rollback_anchor_after_block": False,
        "mathematical_claim": "none"}
    validate_envelope(row, ROOT/Q3_PATH, {}, 0, fixture=True)
    return row


def _fixture_serialization_resource(normal: dict[str, Any]) -> dict[str, Any]:
    """Independent mirror of the checked-write committed-block fallback."""
    row = copy.deepcopy(normal)
    token = "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_RESOURCE"
    reason = "packed_receipt_bytes"
    for name in TARGET_FIELDS | AFFINE_FIELDS | {"selected_proof",
                                                  "normalized_dual"}:
        row.pop(name, None)
    block = row["translation_block"]
    current: dict[str, Any] = {}
    resource = {"cap_reason": reason, "cap_key": reason,
        "cap_source": "local", "cap_limit": CAPS[reason],
        "observed_count": CAPS[reason]+1, "comparator": "gt",
        "phase": "receipt_serialization", "current": current}
    row.update({"terminal_token": token, "status": token, "reason": reason,
        "phase": "receipt_serialization", "claims": claim_row(token, True),
        "resource_guards": {"resource_hit": True, "resource": resource,
                            "atomic_partial": True},
        "performance": _fixture_performance(reason,
            tuple(row["performance"]["phase_seconds"]))})
    row["partial"] = {"phase": "receipt_serialization", "reason": reason,
        "attempted_relators": 11, "completed_relators": 11,
        "raw_completed_relators": 11, "shadow_completed_relators": 11,
        "raw_column_prefix_sha256": block["raw_columns_sha256"],
        "shadow_remainder_prefix_sha256": None,
        "old_qstar_prefix_sha256": sha_obj(block["old_qstar_scalars"]),
        "rank_gain_so_far": block["rank_gain"],
        "source_evaluated_seeds": 0,
        "source_records_prefix_sha256": None, "evaluated_seeds": 0,
        "completed_equations": 0, "current_seed": None,
        "block_digest_prefix": sha_obj(block["columns"]),
        "block_pre_accounting": block["pre_accounting"],
        "block_post_accounting": block["post_accounting"],
        "target_ledger_prefix_sha256": None,
        "completed_target_system": None,
        "rollback_anchor_after_block": True,
        "mathematical_claim": "none"}
    validate_envelope(row, ROOT/Q3_PATH, {}, 0, fixture=True)
    return row


def self_test() -> None:
    authenticate()
    eh = load_eh_checker(); eh.self_test(); eg = eh.load_v1_checker()
    ed, old = loaded_fixture_checker_modules(eg)
    lifecycle_mutations = 0

    def reject_loaded_attr(module: Any, name: str, value: Any,
                           label: str) -> None:
        nonlocal lifecycle_mutations
        original = getattr(module, name)
        setattr(module, name, value)
        try:
            _expect_failure(lambda: loaded_fixture_checker_modules(eg), label)
        finally:
            setattr(module, name, original)
        lifecycle_mutations += 1

    def reject_loaded_digest(path: Path, label: str) -> None:
        nonlocal lifecycle_mutations
        resolved = path.resolve()
        def corrupted(candidate: Path) -> str:
            return "0"*64 if candidate.resolve() == resolved else sha_file(candidate)
        _expect_failure(lambda: loaded_fixture_checker_modules(
            eg, corrupted), label)
        lifecycle_mutations += 1

    def reject_loaded_substitute(name: str, label: str) -> None:
        nonlocal lifecycle_mutations
        original = sys.modules[name]
        sys.modules[name] = object()
        try:
            _expect_failure(lambda: loaded_fixture_checker_modules(eg), label)
        finally:
            sys.modules[name] = original
        lifecycle_mutations += 1

    reject_loaded_attr(ed, "__file__", str(ROOT/EC_CHECKER),
                       "157ed checker loaded path")
    reject_loaded_attr(old, "__file__", str(ROOT/ED_CHECKER),
                       "157ec checker loaded path")
    reject_loaded_digest(ROOT/ED_CHECKER, "157ed checker loaded SHA")
    reject_loaded_digest(ROOT/EC_CHECKER, "157ec checker loaded SHA")
    reject_loaded_attr(ed, "load_old", None, "157ed checker loaded API")
    reject_loaded_attr(old, "checker_target_row_transposed", None,
                       "157ec checker loaded API")
    reject_loaded_substitute(FIXTURE_ED_MODULE_NAME,
                             "157ed checker bare substitute")
    reject_loaded_substitute(FIXTURE_OLD_MODULE_NAME,
                             "157ec checker bare substitute")
    reject_loaded_attr(ed, "OLD_CHECKER_SHA", "0"*64,
                       "157ed checker old pin")
    require(loaded_fixture_checker_modules(eg) == (ed, old) and
            lifecycle_mutations == 9,
            "157ei exact inherited checker lifecycle fixture")
    trace: dict[str, int] = {}
    block, anchor = _fixture_block(trace)
    _validate_completed_block_anchor(block, anchor)
    consistent_system, consistent_public, consistent_target = \
        _fixture_affine(old, True, trace)
    inconsistent_system, inconsistent_public, inconsistent_target = \
        _fixture_affine(
        old, False, trace)
    inconsistent_system.verify_dual(inconsistent_public["dual_witness"])
    selected = _fixture_selected(consistent_system, trace)
    consistent = _fixture_normal(
        "B345_E4_D2_LEXBLOCK_TARGET6_CONSISTENT", block, anchor,
        consistent_target, consistent_public, selected)
    inconsistent = _fixture_normal(
        "B345_E4_D2_LEXBLOCK_TARGET6_INCONSISTENT", block, anchor,
        inconsistent_target, inconsistent_public, None)

    def run_completed_fixture(row: dict[str, Any], want_consistent: bool,
                              run_trace: dict[str, int]) -> None:
        state: dict[str, Any] = {}
        def replay_block() -> dict[str, Any]:
            replayed, replayed_anchor = _fixture_block(run_trace)
            require(replayed == row["translation_block"],
                    "checker fixture completed block equality")
            state["anchor"] = replayed_anchor
            return replayed

        def validate_anchor(replayed: dict[str, Any]) -> None:
            require(state.get("anchor") == row["post_block_anchor"],
                    "checker fixture completed anchor equality")
            _validate_anchor_public(replayed, row["post_block_anchor"],
                                    frozen=False)

        def replay_target() -> tuple[Any, dict[Any, int]]:
            system, public, target = _fixture_affine(
                old, want_consistent, run_trace)
            require(public == row["affine_system"] and
                    target == row["target6"],
                    "checker fixture completed target/affine equality")
            return system, {"fixture": 1}

        def validate_selected(system: Any, base: dict[Any, int]) -> None:
            del base
            replayed = _fixture_selected(system, run_trace)
            require(replayed == row["selected_proof"],
                    "checker fixture completed selected equality")

        def validate_dual(system: Any) -> None:
            system.verify_dual(row["normalized_dual"])
            require(row["normalized_dual"] ==
                    row["affine_system"]["dual_witness"],
                    "checker fixture completed dual equality")

        _validate_completed_core(row, replay_block, validate_anchor,
            replay_target, validate_selected, validate_dual,
            trace=run_trace)

    run_completed_fixture(consistent, True, trace)
    run_completed_fixture(inconsistent, False, trace)
    input_row = _fixture_common(
        "B345_E4_D2_LEXBLOCK_TARGET6_UNKNOWN_INPUT")
    input_row["reason"] = "authenticated_input_failure"
    input_row["input_errors"] = ["toy missing authenticated input"]
    validate_envelope(input_row, ROOT/Q3_PATH, {}, 0, fixture=True)
    resource = _fixture_block_resource(
        [row["raw_column"] for row in block["columns"]],
        [row["raw_column"]["entries"] for row in block["columns"]])
    serialization_resource = _fixture_serialization_resource(consistent)
    require(trace == {"block_core": 3, "target_reducer": 4,
                      "selected_core": 2, "completed_core": 2},
            "checker fixture shared production-core entries")

    mutation_count = 0
    def reject_completed_mutation(row: dict[str, Any],
                                  want_consistent: bool,
                                  label: str) -> None:
        nonlocal mutation_count
        _expect_failure(lambda: run_completed_fixture(
            row, want_consistent, {}), label)
        mutation_count += 1

    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"] = \
        bad["translation_block"]["columns"][:-1]
    reject_completed_mutation(bad, True, "complete block omitted column")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"] = [copy.deepcopy(
        bad["translation_block"]["columns"][8])]
    reject_completed_mutation(bad, True, "relator9-only incomplete block")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][1] = copy.deepcopy(
        bad["translation_block"]["columns"][0])
    reject_completed_mutation(bad, True, "complete block duplicate column")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][0], \
        bad["translation_block"]["columns"][1] = \
        bad["translation_block"]["columns"][1], \
        bad["translation_block"]["columns"][0]
    reject_completed_mutation(bad, True, "complete block reordered columns")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][3]["relator_index"] = 5
    reject_completed_mutation(bad, True, "complete block relator index")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][0]["translation_hex"] = \
        ("00"*154)
    reject_completed_mutation(bad, True, "complete block translation blob")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["columns"][0]["raw_column"]["sha256"] = \
        "00"*32
    reject_completed_mutation(bad, True, "complete block raw digest")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["old_qstar_scalars"][0] = 1
    reject_completed_mutation(bad, True, "relator1 old-qstar nonzero")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["old_qstar_scalars"][8] = 2
    reject_completed_mutation(bad, True, "relator9 old-qstar not one")
    bad = copy.deepcopy(consistent)
    bad["translation_block"]["section_newly_registered"] = False
    reject_completed_mutation(bad, True, "section registration not pool")
    bad = copy.deepcopy(consistent)
    bad["post_block_anchor"]["after_complete_block"] = False
    reject_completed_mutation(bad, True, "pre-block rollback anchor")
    bad = copy.deepcopy(consistent)
    bad["target6"]["base_is_direct_not_empty_formula"] = False
    reject_completed_mutation(bad, True, "formula empty used as base")
    bad = copy.deepcopy(consistent)
    bad["target6"]["affine_rhs_is_negative_base_remainder"] = False
    reject_completed_mutation(bad, True, "affine rhs sign reversal")
    bad = copy.deepcopy(consistent)
    bad["target6"]["old_B0_remainder_or_dual_imported"] = True
    reject_completed_mutation(bad, True, "old B0 remainder import")
    bad = copy.deepcopy(consistent)
    canary = bad["target6"]["noncommutative_formula_canary"]
    canary["ordered_value"] = list(canary["reversed_value"])
    reject_completed_mutation(bad, True, "target noncommutative order")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["first_contradiction_canary"][
        "rows_after_coordinate"] = 0
    reject_completed_mutation(bad, False,
                              "stopped at first contradiction")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["first_contradiction_canary"][
        "full_equation_count"] = 2
    reject_completed_mutation(bad, False,
                              "incomplete contradiction system")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["delta_rows_sha256"] = "00"*32
    reject_completed_mutation(bad, False, "target delta-row digest")
    bad = copy.deepcopy(inconsistent)
    bad["target6"]["target_row"]["row_space_sha256"] = "00"*32
    reject_completed_mutation(bad, False, "target row-space digest")
    bad = copy.deepcopy(consistent)
    bad["selected_proof"]["coefficient_vector"][0] = \
        (bad["selected_proof"]["coefficient_vector"][0]+1) % 3
    reject_completed_mutation(bad, True, "selected coefficient value")
    bad = copy.deepcopy(consistent)
    bad["selected_proof"]["support"] = []
    reject_completed_mutation(bad, True, "selected support")
    bad = copy.deepcopy(consistent)
    bad["selected_proof"]["D2_proof"]["roots"][0]["node_id"] = 1
    reject_completed_mutation(bad, True, "selected proof payload")
    bad = copy.deepcopy(resource); bad["selected_proof"] = selected
    _expect_failure(lambda: validate_envelope(
        bad, ROOT/Q3_PATH, {}, 0, fixture=True),
        "stale positive field in resource")
    mutation_count += 1
    bad = copy.deepcopy(input_row); bad["translation_block"] = block
    _expect_failure(lambda: validate_envelope(
        bad, ROOT/Q3_PATH, {}, 0, fixture=True),
        "stale mathematical field in input")
    mutation_count += 1

    bad = copy.deepcopy(input_row); bad["claims"]["full_D2_claimed"] = True
    _expect_failure(lambda: validate_envelope(
        bad, ROOT/Q3_PATH, {}, 0, fixture=True), "claim mutation")
    rows = [[[1, (bytes([1])+bytes(153)).hex(), 1]],
            [[1, (bytes([1])+bytes(153)).hex(), 2],
             [2, (bytes([2])+bytes(153)).hex(), 1]]]
    require(_semantic_rank(rows) == 2 and _semantic_rank(rows+[rows[0]]) == 2,
            "checker pool-allocation-neutral semantic rank")
    bad = copy.deepcopy(resource)
    bad["resource_guards"]["resource"]["current"]["attempted_relators"] = 5
    _expect_failure(lambda: validate_envelope(
        bad, ROOT/Q3_PATH, {}, 0, fixture=True), "mid-block attempted drift")
    bad = copy.deepcopy(serialization_resource)
    bad["partial"]["completed_equations"] = 109
    _expect_failure(lambda: validate_envelope(
        bad, ROOT/Q3_PATH, {}, 0, fixture=True),
        "serialization committed-boundary target leakage")
    bad = copy.deepcopy(serialization_resource)
    bad["resource_guards"]["resource"]["current"] = {
        "evaluated_seeds": 108}
    _expect_failure(lambda: validate_envelope(
        bad, ROOT/Q3_PATH, {}, 0, fixture=True),
        "serialization resource current injection")
    bad = copy.deepcopy(consistent); bad["selected_proof"][
        "proof_root_node_id"] = 1
    _expect_failure(lambda: _selected_replay_and_proof_core(
        consistent_system.canonical_solution(), bad["selected_proof"],
        lambda: {"predicted": {"x": 1}, "actual": {"x": 1},
                 "value": 0, "identity": 0, "context": {}},
        lambda replay: require(bad["selected_proof"]["proof_root_node_id"] == 0,
                               "checker proof root")), "proof-root drift")
    bad = copy.deepcopy(inconsistent); bad["selected_proof"] = selected
    _expect_failure(lambda: validate_envelope(
        bad, ROOT/Q3_PATH, {}, 0, fixture=True), "stale success field")
    require(mutation_count == 24,
            "checker exact EI-specific mutation coverage")
    print("D972_B345_LEXBLOCK_TARGET6_CHECKER_SELFTEST_PASS "
          f"block_core={trace['block_core']} relator9_independent=1 "
          f"target_reducer={trace['target_reducer']} "
          "consistent_proof=1 inconsistent_dual=1 schemas=4 "
          f"selected_core={trace['selected_core']} "
          f"completed_core={trace['completed_core']} "
          f"ei_mutations={mutation_count} "
          f"lifecycle_mutations={lifecycle_mutations} "
          "independent_pool_schedule=1 monitor_callbacks=1 "
          "serialization_resource=1 inherited_eh=1",
          flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--q3", type=Path, default=ROOT/Q3_PATH)
    parser.add_argument("--receipt", type=Path, default=ROOT/OUTPUT)
    parser.add_argument("--seconds", type=float, default=18_000.0)
    args = parser.parse_args(argv)
    if args.self_test:
        self_test(); return 0
    data = check_receipt(args.q3, args.receipt, seconds=args.seconds)
    print("D972_B345_LEXBLOCK_TARGET6_CHECKER_PASS "
          f"terminal={data['terminal_token']} receipt={args.receipt}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
