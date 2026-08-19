#!/usr/bin/env python3
"""Exact single-word T-53 strong W-form inertness diagnostic.

This versioned lane rebuilds the authenticated q=3 quotients and the exact
v7 saturated PB4 Fox prefix.  It asks only six fixed membership questions:
the five cofaces of s=[y^18,x^18] and the target-6 residual difference.
Prefix failure is UNKNOWN; no negative membership or global GT claim is made.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Sequence


SCHEMA = "d972-b345-strong-wform-inertness/v1"
OUTPUT_PATH = Path("ci/out/d972_b345_strong_wform_inertness_v1.json")
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
Q3_PRODUCER = Path("search/d972_b345_q3_chief_v1.g")
Q3_PRODUCER_SHA = "b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755"
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
Q3_DRIVER = Path("search/d972_b345_q3_gha_driver_v1.g")
Q3_DRIVER_SHA = "c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831"
V7_PRODUCER = Path("search/d972_b345_relfrat3_pivot_surgery_v7.py")
V7_PRODUCER_SHA = "a19c3353c5cfc6da8ad0b7d941ba94bde043c80e69e33c889c5710c897d7a757"
V7_CHECKER = Path("search/check_d972_b345_relfrat3_pivot_surgery_v7.py")
V7_CHECKER_SHA = "fbe033704180a808320c897c52613ca6847305dd85ddcd7a70aa825161e8bfa0"
V9_PRODUCER = Path("search/d972_b345_relfrat3_wordexpr_memo_v9.py")
V9_PRODUCER_SHA = "7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f"
V10_CHECKER = Path("search/check_d972_b345_relfrat3_wordexpr_memo_v10.py")
V10_CHECKER_SHA = "264258dcb945401e3db10ecd4fedd7a8dd79a8d7b0f31dbc0cfbe643537eac2d"
V10_DRIVER = Path("search/d972_b345_relfrat3_wordexpr_memo_gha_driver_v10.g")
V10_DRIVER_SHA = "a5e9bdb34d85669a6221e4b0fa8e4c3af0aee343aade59fde52013d05753afc0"
CHECKER_PATH = Path("search/check_d972_b345_strong_wform_inertness_v1.py")
DRIVER_PATH = Path("search/d972_b345_strong_wform_inertness_gha_driver_v1.g")
FORMULA_SHA = "b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef"
TASK_SHA = "1b403d5f545cf11b2ab397c1bc9c4e1a57f29207e2e3dee423f42e60b81f0665"

F0 = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
      2, 2, 2, -1, -2, -2, 1, 1, 1, 1]
F0_SHA = "b79f105ec2963ae55b69480f8ed8ab13083d01cb936da32edb4798698c22055d"
S_SHA = "b85ac8d8b4528868282685a5da15eef9ee276d5e94e499d449d6aa1b0b7060ad"
FS_SHA = "c113c06d51480c8c819a563f6efc2323afecb7a54aabee96e7104d1d2921505b"
PREFIX_BINDINGS = {
    "stable_rounds_projection_sha256":
        "75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d",
    "volatile_rounds_sha256_provenance_only":
        "e1c11cd5a436229c8730d5174b9a6981a508901a6e44d5362219e03d74557391",
    "translations_sha256":
        "a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f",
    "columns_sha256":
        "cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343",
    "blocker_history_sha256":
        "b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53",
    "final_blocker_sha256":
        "0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903",
}
TERMINALS = {
    "B345_T53_STRONG_S_EXACT_TYPED_INERT",
    "B345_T53_STRONG_S_PREFIX_INCOMPLETE",
    "B345_T53_STRONG_S_UNKNOWN_RESOURCE",
    "B345_T53_STRONG_S_UNKNOWN_INPUT",
}
CLAIM_SCOPE = "single_explicit_strong_word_fixed_prefix_only"


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-t53")
    raw = (json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True) + "\n").encode("ascii")
    try:
        with temporary.open("wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.read_bytes() != raw:
            raise RuntimeError("temporary output readback drift")
        os.replace(temporary, path)
        if path.read_bytes() != raw:
            raise RuntimeError("final output readback drift")
    finally:
        if temporary.exists():
            temporary.unlink()


def load_v9(repo: Path) -> Any:
    path = repo / V9_PRODUCER
    spec = importlib.util.spec_from_file_location("_d972_t53_v9", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned v9 implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    # The new lane has the registered 300-minute soft budget.  All other
    # calibrated v6/v7 structural caps remain byte-for-byte unchanged.
    module.CAPS["producer_soft_timeout_seconds"] = 18_000
    return module


def element_record(base: Any, value: Any) -> dict[str, Any]:
    blob = base._element_blob(value)
    return {
        "coarse_permutation_zero_based": list(value[0]),
        "fine_pc_coords": list(value[1]),
        "canonical_hex": blob.hex(),
        "canonical_sha256": hashlib.sha256(blob).hexdigest(),
    }


def word_record(base: Any, word: Sequence[int]) -> dict[str, Any]:
    reduced = base.reduce_word(word)
    return {"word": reduced, "length": len(reduced),
            "sha256": base.digest_obj(reduced)}


def raw_gradient_binding(base: Any, gradient: dict[Any, int]) -> dict[str, Any]:
    rows = []
    digest = hashlib.sha256()
    for (component, value), coefficient in sorted(
            gradient.items(), key=lambda row: (row[0][0], base._element_blob(row[0][1]))):
        blob = base._element_blob(value)
        digest.update(int(component).to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
        rows.append([component, blob.hex(), coefficient])
    return {"entry_count": len(rows),
            "canonical_gradient_sha256": digest.hexdigest(),
            "canonical_rows": rows,
            "canonical_order": "component then exact canonical E4 bytes"}


def exact_words(base: Any) -> dict[str, Any]:
    xi = base.reduce_word([1] * 18)
    eta = base.reduce_word([2] * 18)
    s = base.commutator(eta, xi)
    expected_s = [-2] * 18 + [-1] * 18 + [2] * 18 + [1] * 18
    fs = base.reduce_word(F0 + s)
    base.require(base.digest_obj(F0) == F0_SHA and len(F0) == 20,
                 "f0 literal binding")
    base.require(s == expected_s and len(s) == 72 and base.digest_obj(s) == S_SHA,
                 "strong word literal/orientation binding")
    base.require(s == base.commutator(eta, xi), "commutator replay")
    base.require(fs == base.reduce_word(F0 + s) and len(fs) == 92 and
                 base.digest_obj(fs) == FS_SHA, "f0*s literal binding")
    base.require(all(base.exponent_sums(word, 2) == [0, 0]
                     for word in (F0, s, fs)), "F2 exponent-sum typing")
    return {"f0": list(F0), "xi": xi, "eta": eta, "s": s, "fs": fs}


def embed_f2_pb3(base: Any, word: Sequence[int]) -> list[int]:
    # Load-bearing typing: PB3 order is (A12,A13,A23), so F2 y is generator 3.
    return base.word_substitute(word, [[1], [3]])


def target_words(base: Any, words: dict[str, list[int]]) \
        -> tuple[list[tuple[str, str, list[int]]], dict[str, list[int]]]:
    maps = base.cofaces(3)
    s_pb3 = embed_f2_pb3(base, words["s"])
    coface_words = [base.word_substitute(s_pb3, mapping) for mapping in maps]
    h0_f2 = base.hexagon_words(words["f0"])[0]
    hs_f2 = base.hexagon_words(words["fs"])[0]
    r0 = base.word_substitute(embed_f2_pb3(base, h0_f2), maps[0])
    rs = base.word_substitute(embed_f2_pb3(base, hs_f2), maps[0])
    delta = base.reduce_word(rs + base.inv_word(r0))
    targets = [(f"strong_s_coface_{slot}", "strong_coface", word)
               for slot, word in enumerate(coface_words)]
    targets.append(("target6_delta_rs_r0_inverse", "target6_delta", delta))
    return targets, {"r0": r0, "rs": rs, "delta": delta,
                     "h0_f2": h0_f2, "hs_f2": hs_f2}


def prefix_targets(base: Any, r0: list[int]) \
        -> list[tuple[str, str, list[int]]]:
    return [(f"charming_error_coface_{slot}", "charming", [])
            for slot in range(5)] + \
           [("hexagon_1_coface_0", "hexagon", r0)]


def claims(positive: bool) -> dict[str, Any]:
    return {
        "claim_classification":
            "positive_exact_single_word_certificate" if positive else
            "unknown_not_obstruction",
        "claim_scope": CLAIM_SCOPE,
        "negative_claimed": False,
        "full_universe_claimed": False,
        "W_FORM_universal_claimed": False,
        "B4_A_claimed": False,
        "B4_B_claimed": False,
        "no_mathematical_obstruction_claimed": True,
    }


def classify_results(results: Sequence[dict[str, Any]], complete: bool) \
        -> dict[str, Any]:
    """Shared production/selftest semantic core; null is never false."""
    if not complete:
        if len(results) > 6:
            raise ValueError("resource target prefix exceeds six questions")
        bits: list[bool | None] = [None if not row.get("evaluated") else
                                   row.get("membership_proved")
                                   for row in results]
        bits.extend([None] * (6 - len(bits)))
        return {"membership_bits": bits, "complete": False,
                "exact_typed_inert": False}
    if len(results) != 6 or any(row.get("evaluated") is not True for row in results):
        raise ValueError("complete six-target ledger")
    bits = [row.get("membership_proved") for row in results]
    if any(bit not in (True, False) for bit in bits):
        raise ValueError("complete membership bit typing")
    cofaces = bits[:5]
    delta = bits[5]
    return {
        "membership_bits": bits,
        "coface_membership_bits": cofaces,
        "delta_membership_bit": delta,
        "explicit_s_JPhi_proved": all(cofaces),
        "target6_class_equality_proved": bool(delta),
        "exact_typed_inert": all(cofaces) and bool(delta),
        "complete": True,
    }


def build_fresh_prefix(base: Any, e4: Any, r0: list[int], monitor: Any,
                       run_start: float) -> dict[str, Any]:
    """Rebuild the exact 32768+207 v7 prefix without importing a receipt."""
    pool = base.ElementPool(e4)
    sections = base.SparseSectionOracle(pool)
    model4 = base.fox_model(4, e4)
    packed_model4 = base.packed_fox_model(4, pool)
    base_occurrences = base.freeze_base_support_occurrences(model4, pool, sections)
    public_occurrences = base.public_base_occurrences(base_occurrences)
    directed_base_support = {
        "occurrences": public_occurrences,
        "occurrence_count": len(public_occurrences),
        "ordered_sha256": base.digest_obj(public_occurrences),
        "order": "relator index, component, canonical E4 bytes",
        "all_prefix_sections_directly_replayed": True,
    }
    dag = base.ProvenanceDAG(monitor)
    basis = base.SparseBoundaryBasis(pool, packed_model4["columns"], dag,
                                    sections, monitor)

    # v9/v10 schedule invariant: these six anchors are persistent and are
    # interned after base construction but before BFS or any target probe.
    raw_source_tuple = tuple(e4.eval(word) for word in base.source_words_m0(F0))
    base_source_key = tuple(pool.intern(value) for value in raw_source_tuple)
    target_list = prefix_targets(base, r0)
    inserted: set[bytes] = set()
    blocker_history: list[dict[str, Any]] = []
    directed_translations: list[dict[str, Any]] = []
    directed_columns: list[dict[str, Any]] = []
    rounds: list[dict[str, Any]] = []
    expression_roots: list[int] = []
    rollback_count = 0

    def probe(round_no: int | None, history_id: int) \
            -> tuple[dict[str, Any] | None, int]:
        nonlocal rollback_count
        snapshot = base.candidate_transaction_snapshot(
            pool, dag, basis, sections, base_source_key)
        try:
            for ordinal, (name, kind, word) in enumerate(target_list, 1):
                gradient, value_id = base.fox_gradient_packed(word, pool)
                base.require(value_id == pool.identity_id,
                             f"prefix target quotient identity: {name}")
                raw, raw_value, raw_sections = base.fox_gradient(word, e4)
                base.require(raw_value == e4.identity and
                             base.intern_raw_vector(raw, pool) == gradient,
                             f"prefix raw/packed target drift: {name}")
                transient = {(component, pool.pack(value)): raw_sections[value]
                             for component, value in raw}
                root, missing_key = basis.solve_with_blocker(gradient)
                if root is not None:
                    continue
                base.require(missing_key is not None,
                             "prefix missing target without exact pivot")
                component, element_id = base.unpack_vector_key(missing_key)
                blob = pool.blob(element_id)
                blocker_root, recovery = sections.recover_blocker(
                    component, blob, transient, base_occurrences)
                base.require(sections.expressions.value_blob(blocker_root) == blob,
                             "prefix blocker section binding")
                if round_no is None:
                    missing = {
                        "candidate_index": 1,
                        "target_ordinal": ordinal,
                        "target_name": name,
                        "component": component,
                        "element_hex": blob.hex(),
                        "failed_checkpoint": 1,
                        "skip_checkpoints": [],
                        "retry_checkpoints": [],
                        "history_id": history_id,
                        "section_expression_root": blocker_root,
                        "section_recovery": recovery,
                    }
                else:
                    missing = {
                        "candidate_index": 1,
                        "target_ordinal": ordinal,
                        "target_name": name,
                        "target_kind": kind,
                        "component": component,
                        "element_hex": blob.hex(),
                        "canonical_value_sha256": hashlib.sha256(blob).hexdigest(),
                        "directed_round": round_no,
                        "history_id": history_id,
                        "section_expression_root": blocker_root,
                        "section_recovery": recovery,
                    }
                expression_roots.append(blocker_root)
                removed = base.rollback_candidate_transaction(
                    snapshot, pool, dag, basis, sections)
                rollback_count += 1
                return missing, removed
            removed = base.rollback_candidate_transaction(
                snapshot, pool, dag, basis, sections)
            rollback_count += 1
            return None, removed
        except Exception:
            base.rollback_candidate_transaction(snapshot, pool, dag, basis, sections)
            rollback_count += 1
            raise

    # Exact frozen shortlex BFS.  Only checkpoint 1 evaluates the candidate;
    # all later geometric checkpoints see the same absent pivot and are skips.
    first_missing: dict[str, Any] | None = None
    for translation_id, section_node in base.translation_bfs(
            pool, sections, base.CAPS["coefficient_translates_per_relator"]):
        used = basis.columns_seen // 11 + 1
        monitor.check("strong_wform_fresh_BFS")
        for relator_index in range(1, 12):
            basis.add_column(relator_index, translation_id, section_node,
                             translation_ordinal=used)
        inserted.add(pool.blob(translation_id))
        if used == 1:
            first_missing, _ = probe(None, 1)
            base.require(first_missing is not None and
                         first_missing["target_ordinal"] == 6 and
                         first_missing["target_name"] == "hexagon_1_coface_0" and
                         first_missing["component"] == 4,
                         "fresh checkpoint-1 blocker drift")
            blocker_history.append(first_missing)
        elif (used & (used - 1)) == 0:
            base.require(first_missing is not None, "geometric blocker ledger")
            blob = bytes.fromhex(first_missing["element_hex"])
            identifier = pool.ids.get(blob)
            key = None if identifier is None else base.pack_vector_key(
                int(first_missing["component"]), identifier)
            base.require(key is None or key not in basis.rows,
                         "unexpected geometric blocker pivot")
            first_missing["skip_checkpoints"].append(used)
        if used % 4096 == 0:
            print("D972_B345_T53_STRONG_S_PREFIX "
                  f"phase=BFS translations={used} columns={basis.columns_seen} "
                  f"pivots={len(basis.rows)}", flush=True)

    base.require(basis.columns_seen == 32768 * 11 and len(inserted) == 32768,
                 "complete fresh BFS prefix")

    stop_reason: str | None = None
    for round_no in range(1, base.CAPS["directed_surgery_rounds"] + 1):
        monitor.check("strong_wform_directed_round", force=True)
        missing, removed = probe(round_no, len(blocker_history) + 1)
        base.require(missing is not None,
                     "frozen v7 prefix unexpectedly solved target6")
        if round_no == 1:
            base.require(first_missing is not None and
                         missing["target_ordinal"] == 6 and
                         missing["target_name"] == "hexagon_1_coface_0" and
                         missing["component"] == 4 and
                         missing["element_hex"] == first_missing["element_hex"],
                         "fresh BFS blocker reconstruction drift")
        blocker_history.append(missing)
        component = int(missing["component"])
        blocker_blob = bytes.fromhex(missing["element_hex"])
        blocker = pool.unpack(blocker_blob)
        matching = [row for row in base_occurrences
                    if row["component"] == component]
        matching.sort(key=lambda row: (row["relator_index"], row["component"],
                                       bytes.fromhex(row["element_hex"])))
        candidates = []
        seen_batch: set[bytes] = set()
        duplicates = 0
        for occurrence in matching:
            h = occurrence["_value"]
            translation = e4.mul(blocker, e4.inverse(h))
            blob = pool.pack(translation)
            base.require(e4.mul(translation, h) == blocker,
                         "left directed translation orientation")
            if blob in seen_batch or blob in inserted:
                duplicates += 1
                continue
            seen_batch.add(blob)
            candidates.append((blob, translation, occurrence))
        pivots_before = len(basis.rows)
        entries_before = basis.live_vector_entries
        columns_before = basis.columns_seen
        dependent_before = basis.dependent_columns
        for blob, translation, occurrence in candidates:
            base.require(len(directed_translations) <
                         base.CAPS["directed_unique_translations"],
                         "directed translation cap")
            blocker_root = int(missing["section_expression_root"])
            h_root = int(occurrence["section_expression_root"])
            inverse_h = sections.expressions.inverse(
                h_root, "base_D2_prefix_inverse")
            translation_root = sections.expressions.product(
                blocker_root, inverse_h, "registered_directed_translation")
            base.require(sections.expressions.value_blob(translation_root) == blob,
                         "directed expression orientation")
            section_node, created = sections.register_directed(
                translation, translation_root)
            base.require(created, "directed translation duplicate registration")
            translation_id = pool.ids[blob]
            expression_roots.append(translation_root)
            translation_ordinal = 32768 + len(directed_translations) + 1
            translation_row = {
                "ordinal": len(directed_translations) + 1,
                "round": round_no,
                "component": component,
                "blocker_element_hex": blocker_blob.hex(),
                "base_relator_index": occurrence["relator_index"],
                "base_element_hex": occurrence["element_hex"],
                "translation_element_hex": blob.hex(),
                "section_expression_root": translation_root,
                "formula": "t=g*h^-1; left translation sends h to g",
            }
            directed_translations.append(translation_row)
            for relator_index in range(1, 12):
                base.require(len(directed_columns) < base.CAPS["directed_columns"],
                             "directed column cap")
                before = len(basis.rows)
                basis.add_column(relator_index, translation_id, section_node,
                                 translation_ordinal=translation_ordinal)
                directed_columns.append({
                    "ordinal": len(directed_columns) + 1,
                    "round": round_no,
                    "translation_ordinal": translation_row["ordinal"],
                    "relator_index": relator_index,
                    "independent": len(basis.rows) > before,
                })
            inserted.add(blob)
        round_row = {
            "round": round_no, "outcome": "RETRY",
            "failed_target_ordinal": missing["target_ordinal"],
            "failed_target_name": missing["target_name"],
            "failed_target_kind": missing["target_kind"],
            "blocker_component": component,
            "blocker_element_hex": blocker_blob.hex(),
            "blocker_value_sha256": missing["canonical_value_sha256"],
            "blocker_section_expression_root": missing["section_expression_root"],
            "blocker_recovery": missing["section_recovery"],
            "matching_base_occurrences": len(matching),
            "new_directed_translations": len(candidates),
            "duplicate_translations": duplicates,
            "columns_attempted": basis.columns_seen - columns_before,
            "columns_independent": len(basis.rows) - pivots_before,
            "columns_dependent": basis.dependent_columns - dependent_before,
            "pivots_before": pivots_before,
            "pivots_after": len(basis.rows),
            "live_sparse_entries_before": entries_before,
            "live_sparse_entries_after": basis.live_vector_entries,
            "pool_after": len(pool.values),
            "DAG_nodes_after": dag.node_count,
            "DAG_edges_after": dag.edge_count,
            "section_expression_nodes_after": len(sections.expressions.kind),
            "section_expression_edges_after": sections.expressions.edge_count,
            "candidate_pool_suffix_removed": removed,
            "candidate_rollback_count": rollback_count,
            "RSS_bytes": base.current_rss_bytes(),
            "elapsed_seconds": time.monotonic() - run_start,
        }
        rounds.append(round_row)
        print("D972_B345_T53_STRONG_S_PREFIX " +
              json.dumps(round_row, sort_keys=True, separators=(",", ":")),
              flush=True)
        if not candidates:
            stop_reason = "no_new_exact_directed_translation"
            break
    else:
        stop_reason = "directed_surgery_round_cap_exhausted"

    audit_roots = sorted(set(expression_roots))
    expression_payload, renumber = sections.expressions.serialize_reachable(
        audit_roots, monitor)
    public_translations = base.remap_expression_root_fields(
        directed_translations, renumber)
    public_rounds = base.remap_expression_root_fields(rounds, renumber)
    public_history = base.remap_expression_root_fields(blocker_history, renumber)
    stable_rounds = [{key: value for key, value in row.items()
                      if key not in {"elapsed_seconds", "RSS_bytes"}}
                     for row in public_rounds]
    stable_sha = base.digest_obj(stable_rounds)
    translations_sha = base.digest_obj(public_translations)
    columns_sha = base.digest_obj(directed_columns)
    history_sha = base.digest_obj(public_history)
    base.require(stable_sha == PREFIX_BINDINGS["stable_rounds_projection_sha256"] and
                 translations_sha == PREFIX_BINDINGS["translations_sha256"] and
                 columns_sha == PREFIX_BINDINGS["columns_sha256"] and
                 history_sha == PREFIX_BINDINGS["blocker_history_sha256"] and
                 len(public_rounds) == 32 and
                 len(public_translations) == 207 and
                 len(directed_columns) == 2277 and
                 public_rounds[-1]["blocker_value_sha256"] ==
                     PREFIX_BINDINGS["final_blocker_sha256"] and
                 public_rounds[-1]["new_directed_translations"] == 0 and
                 stop_reason == "no_new_exact_directed_translation" and
                 basis.columns_seen == 362725 and len(basis.rows) == 362709 and
                 basis.dependent_columns == 16,
                 "fresh saturated v7 prefix drift")
    directed = {
        "theorem": {
            "field": 3, "left_Fox_translation": True,
            "formula": "t=g*h^-1 and t*h=g",
            "matching_order": "relator index, component, canonical h bytes",
            "wrong_orientations_rejected":
                ["h^-1*g", "g^-1*h", "right translation"],
            "complete_eleven_relator_block_per_new_translation": True,
        },
        "rounds": public_rounds, "round_count": len(public_rounds),
        "rounds_sha256": base.digest_obj(public_rounds),
        "volatile_rounds_sha256_provenance_only":
            PREFIX_BINDINGS["volatile_rounds_sha256_provenance_only"],
        "stable_rounds_projection": stable_rounds,
        "stable_rounds_projection_sha256": stable_sha,
        "stable_projection_omits_exactly": ["elapsed_seconds", "RSS_bytes"],
        "translations": public_translations,
        "translation_count": len(public_translations),
        "translations_sha256": translations_sha,
        "column_count": len(directed_columns),
        "columns_sha256": columns_sha,
        "column_order": "translation first-seen order, relator 1..11",
        "blocker_history": public_history,
        "blocker_history_sha256": history_sha,
        "section_expressions": expression_payload,
        "section_oracle": {
            "persistent_roots": "BFS and registered directed translations only",
            "base_D2_prefixes_frozen": True,
            "candidate_target_prefixes_transient": True,
            "blocker_recovery_complete_by_support_union": True,
            "canonical_bytes_binding": True,
            "pool_ID_binding_used": False,
            "recovery_failure_is_hard_FAIL": True,
            "expression_accounting": sections.expressions.accounting(),
        },
        "stop_reason": stop_reason,
        "bounded_prefix_sha256": base.digest_obj({
            "translations": public_translations,
            "columns_sha256": base.digest_obj(directed_columns),
            "blockers": public_history, "rounds": public_rounds}),
    }
    accounting = {
        "BFS_translations": 32768,
        "directed_translations": len(public_translations),
        "total_translation_blocks": 32768 + len(public_translations),
        "columns": basis.columns_seen,
        "pivots": len(basis.rows),
        "dependent_columns": basis.dependent_columns,
        "live_sparse_entries": basis.live_vector_entries,
        "element_pool": pool.accounting(),
        "provenance_DAG": dag.accounting(),
        "single_shared_basis": True,
        "targeted_translations_for_six_questions": 0,
    }
    return {
        "pool": pool, "sections": sections, "dag": dag, "basis": basis,
        "model4": model4, "raw_source_tuple": raw_source_tuple,
        "base_source_key": base_source_key,
        "directed_base_support": directed_base_support,
        "directed_surgery": directed,
        "accounting": accounting,
    }


def solve_six_targets(base: Any, e3: Any, e4: Any,
                      prefix: dict[str, Any],
                      targets: list[tuple[str, str, list[int]]],
                      formulas: dict[str, list[int]], monitor: Any,
                      progress: dict[str, Any]) \
        -> dict[str, Any]:
    pool = prefix["pool"]
    sections = prefix["sections"]
    dag = prefix["dag"]
    basis = prefix["basis"]
    anchor_ids = prefix["base_source_key"]

    # Independent drift canary after exact saturation.
    snap = base.candidate_transaction_snapshot(pool, dag, basis, sections,
                                               anchor_ids)
    r0_gradient, r0_value = base.fox_gradient_packed(formulas["r0"], pool)
    base.require(r0_value == pool.identity_id, "r0 quotient identity")
    r0_missing = base.membership_reduce_fixed_basis(r0_gradient, basis)
    base.require(r0_missing is not None, "r0 unexpectedly solved in fixed prefix")
    r0_component, r0_identifier = base.unpack_vector_key(r0_missing)
    r0_blob = pool.blob(r0_identifier)
    r0_canary = {
        "target_name": "hexagon_1_coface_0",
        "component": r0_component,
        "element_hex": r0_blob.hex(),
        "canonical_value_sha256": hashlib.sha256(r0_blob).hexdigest(),
        "prefix_missing_only_not_nonmembership": True,
    }
    base.rollback_candidate_transaction(snap, pool, dag, basis, sections)
    base.require(r0_component == 4 and
                 r0_canary["canonical_value_sha256"] ==
                    PREFIX_BINDINGS["final_blocker_sha256"],
                 "post-saturation r0 blocker drift")

    # Bind quotient identities and the exact Fox subtraction law before any
    # membership solve.  This is literal equality, not digest comparison.
    raw_r0, value_r0, _ = base.fox_gradient(formulas["r0"], e4)
    raw_rs, value_rs, _ = base.fox_gradient(formulas["rs"], e4)
    raw_delta, value_delta, _ = base.fox_gradient(formulas["delta"], e4)
    expected_delta = dict(raw_rs)
    base.add_scaled(expected_delta, raw_r0, -1)
    base.require(value_r0 == value_rs == value_delta == e4.identity and
                 raw_delta == expected_delta,
                 "target6 quotient/Fox difference identity")
    target6_formula = {
        "name": "target6_delta_rs_r0_inverse",
        "r0": word_record(base, formulas["r0"]),
        "rs": word_record(base, formulas["rs"]),
        "delta": word_record(base, formulas["delta"]),
        "product_order": "delta=rs*r0^-1",
        "r0_formula": "coface_0(embed_F2_PB3(hexagon_1(f0)))",
        "rs_formula": "coface_0(embed_F2_PB3(hexagon_1(f0*s)))",
        "embed_F2_PB3": {"x": 1, "y": 3},
        "quotient_values": {
            "r0": element_record(base, value_r0),
            "rs": element_record(base, value_rs),
            "delta": element_record(base, value_delta),
        },
        "gradients": {
            "r0": raw_gradient_binding(base, raw_r0),
            "rs": raw_gradient_binding(base, raw_rs),
            "delta": raw_gradient_binding(base, raw_delta),
        },
        "Fox_delta_equals_Fox_rs_minus_Fox_r0": True,
    }

    results: list[dict[str, Any]] = []
    proof_roots: dict[str, int] = {}
    positive_targets: list[tuple[str, str, list[int]]] = []
    positive_bindings: dict[str, dict[str, Any]] = {}
    for ordinal, (name, kind, word) in enumerate(targets, 1):
        monitor.check("strong_wform_membership_only", force=True)
        snapshot = base.candidate_transaction_snapshot(
            pool, dag, basis, sections, anchor_ids)
        packed, value_id = base.fox_gradient_packed(word, pool)
        raw, raw_value, _ = base.fox_gradient(word, e4)
        base.require(value_id == pool.identity_id and raw_value == e4.identity and
                     base.intern_raw_vector(raw, pool) == packed,
                     f"six-target raw/packed quotient drift: {name}")
        binding = base.packed_gradient_binding(name, kind, packed, value_id, pool)
        missing_key = base.membership_reduce_fixed_basis(packed, basis)
        if missing_key is not None:
            component, identifier = base.unpack_vector_key(missing_key)
            blob = pool.blob(identifier)
            row = {
                "ordinal": ordinal, "name": name, "kind": kind,
                "evaluated": True, "membership_proved": False,
                "proof_complete": False,
                "word": list(word), "word_sha256": base.digest_obj(word),
                "gradient_binding": binding,
                "missing_pivot": {
                    "component": component, "element_hex": blob.hex(),
                    "canonical_value_sha256": hashlib.sha256(blob).hexdigest(),
                    "fixed_prefix_only": True,
                    "nonmembership_claimed": False,
                },
            }
            base.rollback_candidate_transaction(
                snapshot, pool, dag, basis, sections)
            results.append(row)
            progress["target_results"] = results
            print("D972_B345_T53_STRONG_S_TARGET "
                  f"ordinal={ordinal} name={name} outcome=MISSING_PIVOT "
                  f"component={component}", flush=True)
            continue

        # The membership-only transaction must not leak any pool/DAG suffix.
        base.rollback_candidate_transaction(snapshot, pool, dag, basis, sections)
        proof_snapshot = base.candidate_transaction_snapshot(
            pool, dag, basis, sections, anchor_ids)
        regenerated, regenerated_value = base.fox_gradient_packed(word, pool)
        raw2, raw_value2, _ = base.fox_gradient(word, e4)
        regenerated_binding = base.packed_gradient_binding(
            name, kind, regenerated, regenerated_value, pool)
        base.require(regenerated_value == pool.identity_id and
                     raw_value2 == e4.identity and
                     base.intern_raw_vector(raw2, pool) == regenerated and
                     regenerated_binding == binding,
                     f"positive target regeneration drift: {name}")
        root, provenance_missing = basis.solve_with_blocker(regenerated)
        base.require(root is not None and provenance_missing is None,
                     f"membership/provenance solve drift: {name}")
        pool.commit(proof_snapshot["pool"])
        proof_roots[name] = root
        positive_targets.append((name, kind, list(word)))
        positive_bindings[name] = binding
        results.append({
            "ordinal": ordinal, "name": name, "kind": kind,
            "evaluated": True, "membership_proved": None,
            "provisional_positive_solve": True, "proof_complete": False,
            "word": list(word), "word_sha256": base.digest_obj(word),
            "gradient_binding": binding, "missing_pivot": None,
        })
        progress["target_results"] = results
        print("D972_B345_T53_STRONG_S_TARGET "
              f"ordinal={ordinal} name={name} outcome=PROVISIONAL_POSITIVE",
              flush=True)

    proof_payload = None
    registry_rows: list[dict[str, Any]] = []
    certificates: list[dict[str, Any]] = []
    if proof_roots:
        monitor.check("strong_wform_positive_serialization", force=True)
        registry = base.ElementRegistry({3: e3, 4: e4})
        ordered_roots = {name: proof_roots[name]
                         for name, _, _ in positive_targets}
        proof_payload, renumber = base.serialize_proof_dag(
            dag, ordered_roots, basis, registry)
        for name, kind, word in positive_targets:
            monitor.check("strong_wform_boundary_certificate")
            certificates.append(base.boundary_certificate(
                name, kind, word, e4, renumber[proof_roots[name]], registry))
        registry_rows = registry.rows
        certificate_names = {row["name"] for row in certificates}
        for row in results:
            if row["name"] in certificate_names:
                row["membership_proved"] = True
                row["proof_complete"] = True
                row["provisional_positive_solve"] = False
                row["certificate_name"] = row["name"]
        progress["target_results"] = results
        progress["proof_serialization_complete"] = True
    summary = classify_results(results, True)
    return {
        "r0_drift_canary": r0_canary,
        "target6_formula": target6_formula,
        "target_results": results,
        "result_summary": summary,
        "positive_target_order": [name for name, _, _ in positive_targets],
        "positive_gradient_bindings": [positive_bindings[name]
                                        for name, _, _ in positive_targets],
        "quotient_element_registry": registry_rows,
        "boundary_proof_dag": proof_payload,
        "boundary_certificates": certificates,
    }


def make_input_receipt(source_hashes: dict[str, str], errors: list[dict[str, str]]) \
        -> dict[str, Any]:
    token = "B345_T53_STRONG_S_UNKNOWN_INPUT"
    return {
        "schema": SCHEMA, "status": token, "terminal_token": token,
        "reason": "authenticated_input_pin_mismatch",
        "source_hashes": source_hashes,
        "input_errors": errors,
        "claims": claims(False),
        "result_summary": {"membership_bits": [None] * 6,
                           "complete": False, "exact_typed_inert": False},
        "prohibited_work": prohibited_work(),
    }


def prohibited_work() -> dict[str, Any]:
    return {
        "registered_4096_dictionary_constructed": False,
        "other_acceptance_targets_constructed": False,
        "T_diagnostics_constructed": False,
        "normalized_inverse_constructed": False,
        "onto_checks_constructed": False,
        "PB5_constructed": False,
        "ANUPQ_invoked": False,
        "targeted_translations_for_six_questions": False,
        "old_receipt_basis_pool_rows_or_DAG_imported": False,
    }


def resource_record(monitor: Any, hit: bool) -> dict[str, Any]:
    row = monitor.receipt(hit)
    row["terminal_on_hit"] = "B345_T53_STRONG_S_UNKNOWN_RESOURCE"
    return row


def bind_resource_reason(monitor: Any, reason: str) -> None:
    """Bind structural stops and preserve the monitor's soft-stop reason."""
    if monitor.hit_reason is None:
        monitor.hit_reason = reason
    if monitor.hit_reason != reason:
        raise RuntimeError("resource stop/monitor reason drift")


def source_hashes(repo: Path) -> dict[str, str]:
    def got(path: Path) -> str:
        return digest_file(repo / path) if (repo / path).is_file() else "MISSING"
    return {
        "producer_sha256": got(Path("search/d972_b345_strong_wform_inertness_v1.py")),
        "checker_sha256": got(CHECKER_PATH),
        "driver_sha256": got(DRIVER_PATH),
        "task_sha256": got(Path("sol/luna_task_157ea_b345_strong_wform_inertness.md")),
        "q3_producer_sha256": got(Q3_PRODUCER),
        "q3_checker_sha256": got(Q3_CHECKER),
        "q3_driver_sha256": got(Q3_DRIVER),
        "v7_producer_sha256": got(V7_PRODUCER),
        "v7_checker_sha256": got(V7_CHECKER),
        "v9_producer_sha256": got(V9_PRODUCER),
        "v10_checker_sha256": got(V10_CHECKER),
        "v10_driver_sha256": got(V10_DRIVER),
    }


def run(q3_path: Path, output_path: Path) -> dict[str, Any]:
    run_start = time.monotonic()
    repo = Path(__file__).resolve().parents[1]
    sources = source_hashes(repo)
    expected = {
        "task_sha256": TASK_SHA,
        "q3_producer_sha256": Q3_PRODUCER_SHA,
        "q3_checker_sha256": Q3_CHECKER_SHA,
        "q3_driver_sha256": Q3_DRIVER_SHA,
        "v7_producer_sha256": V7_PRODUCER_SHA,
        "v7_checker_sha256": V7_CHECKER_SHA,
        "v9_producer_sha256": V9_PRODUCER_SHA,
        "v10_checker_sha256": V10_CHECKER_SHA,
        "v10_driver_sha256": V10_DRIVER_SHA,
    }
    errors = [{"label": key, "expected": sha, "got": sources.get(key, "MISSING")}
              for key, sha in expected.items() if sources.get(key) != sha]
    fixed_q3 = (repo / Q3_PATH).resolve()
    fixed_output = (repo / OUTPUT_PATH).resolve()
    if q3_path.resolve() != fixed_q3 or output_path.resolve() != fixed_output:
        errors.append({"label": "fixed_paths", "expected":
                       f"{fixed_q3}|{fixed_output}",
                       "got": f"{q3_path.resolve()}|{output_path.resolve()}"})
    q3_got = digest_file(q3_path) if q3_path.is_file() else "MISSING"
    if q3_got != Q3_SHA:
        errors.append({"label": "q3_receipt_sha256", "expected": Q3_SHA,
                       "got": q3_got})
    if errors:
        return make_input_receipt(sources, errors)

    base = load_v9(repo)
    monitor = base.ResourceMonitor(run_start, 18_000)
    phase = "authenticated_input"
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "B345_T53_STRONG_S_UNKNOWN_RESOURCE",
        "terminal_token": "B345_T53_STRONG_S_UNKNOWN_RESOURCE",
        "reason": "initializing",
        "source_hashes": sources,
        "input": {"q3_path": Q3_PATH.as_posix(), "q3_sha256": q3_got,
                  "q3_same_job_checker_required": True},
        "claims": claims(False),
        "result_summary": {"membership_bits": [None] * 6,
                           "complete": False, "exact_typed_inert": False},
        "prohibited_work": prohibited_work(),
        "formula_sha256": None,
        "base_q3_replay": None,
        "word_typing": None,
        "directed_base_support": None,
        "directed_surgery": None,
        "prefix_accounting": None,
        "r0_drift_canary": None,
        "target6_formula": None,
        "target_results": None,
        "positive_target_order": None,
        "positive_gradient_bindings": None,
        "quotient_element_registry": None,
        "boundary_proof_dag": None,
        "boundary_certificates": None,
        "registered_questions": None,
        "resource_guards": None,
        "performance": None,
        "partial": None,
    }
    solve_progress: dict[str, Any] = {"target_results": [],
                                     "proof_serialization_complete": False}
    try:
        q3 = json.loads(q3_path.read_text(encoding="utf-8"))
        base.require(q3.get("schema") == base.Q3_SCHEMA and
                     q3.get("terminal_token") ==
                        "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION" and
                     q3.get("status") == q3.get("terminal_token") and
                     base.digest_obj(q3["formulas"]) == FORMULA_SHA,
                     "authenticated q3 schema/terminal/formula")
        e3, e4, _ = base.reconstruct_quotients(q3)
        receipt["formula_sha256"] = FORMULA_SHA
        receipt["base_q3_replay"] = base.replay_base_q3(q3, e3, e4)
        words = exact_words(base)
        embedded = {name: embed_f2_pb3(base, words[name])
                    for name in ("xi", "eta", "s")}
        base.require(all(e3.eval(word) == e3.identity for word in embedded.values()),
                     "embedded xi/eta/s E3 identities")
        maps = base.cofaces(3)
        coface_values: dict[str, list[dict[str, Any]]] = {}
        coface_words: dict[str, list[list[int]]] = {}
        for name, pb3_word in embedded.items():
            images = [base.word_substitute(pb3_word, mapping) for mapping in maps]
            values = [e4.eval(word) for word in images]
            base.require(all(value == e4.identity for value in values),
                         f"{name} five coface E4 identities")
            coface_words[name] = images
            coface_values[name] = [element_record(base, value) for value in values]
        receipt["word_typing"] = {
            "commutator_convention": "[a,b]=a^-1*b^-1*a*b",
            "F2_to_PB3_embedding": {"x_letter": 1, "y_letter": 3,
                                     "PB3_pair_order": ["A12", "A13", "A23"],
                                     "y_to_PB3_generator_2_prohibited": True},
            "f0": word_record(base, words["f0"]),
            "xi_F2": word_record(base, words["xi"]),
            "eta_F2": word_record(base, words["eta"]),
            "s_F2": word_record(base, words["s"]),
            "fs_F2": word_record(base, words["fs"]),
            "exponent_sums": {name: base.exponent_sums(words[name], 2)
                              for name in ("f0", "s", "fs")},
            "embedded_PB3_words": embedded,
            "embedded_E3_values": {name: element_record(base, e3.eval(word))
                                    for name, word in embedded.items()},
            "coface_order": list(range(5)),
            "coface_words_PB4": coface_words,
            "coface_E4_values": coface_values,
            "all_direct_element_identity_tests_pass": True,
        }
        targets, formulas = target_words(base, words)
        base.require([name for name, _, _ in targets] ==
                     [f"strong_s_coface_{i}" for i in range(5)] +
                     ["target6_delta_rs_r0_inverse"], "six target order")
        phase = "fresh_v7_prefix"
        prefix = build_fresh_prefix(base, e4, formulas["r0"], monitor, run_start)
        receipt["directed_base_support"] = prefix["directed_base_support"]
        receipt["directed_surgery"] = prefix["directed_surgery"]
        receipt["prefix_accounting"] = prefix["accounting"]
        phase = "six_target_solve"
        solved = solve_six_targets(base, e3, e4, prefix, targets, formulas,
                                   monitor, solve_progress)
        receipt.update(solved)
        summary = solved["result_summary"]
        positive = summary["exact_typed_inert"]
        token = ("B345_T53_STRONG_S_EXACT_TYPED_INERT" if positive else
                 "B345_T53_STRONG_S_PREFIX_INCOMPLETE")
        receipt["status"] = receipt["terminal_token"] = token
        receipt["reason"] = ("all six exact fixed-prefix membership proofs complete"
                             if positive else
                             "one or more six registered memberships remain prefix-incomplete")
        receipt["claims"] = claims(positive)
        receipt["registered_questions"] = {
            "count": 6,
            "ordered_names": [name for name, _, _ in targets],
            "ordered_names_sha256": base.digest_obj(
                [name for name, _, _ in targets]),
            "fixed_prefix_only": True,
            "membership_missing_means_unknown": True,
        }
        receipt["resource_guards"] = resource_record(monitor, False)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic() - run_start,
            "phase_complete": "six_target_certificate",
            "RSS_peak_bytes": monitor.peak_rss,
        }
        receipt["partial"] = None
        return receipt
    except base.ResourceStop as exc:
        token = "B345_T53_STRONG_S_UNKNOWN_RESOURCE"
        bind_resource_reason(monitor, exc.reason)
        receipt["status"] = receipt["terminal_token"] = token
        receipt["reason"] = exc.reason
        receipt["claims"] = claims(False)
        partial = solve_progress["target_results"]
        receipt["target_results"] = partial
        receipt["result_summary"] = classify_results(partial, False)
        receipt["partial"] = {
            "phase": phase, "evaluated_target_count": len(partial),
            "unevaluated_memberships_are_null": True,
            "positive_solve_without_serialized_proof_is_not_a_positive_bit": True,
            "proof_serialization_complete":
                solve_progress["proof_serialization_complete"],
        }
        receipt["resource_guards"] = resource_record(monitor, True)
        receipt["performance"] = {
            "runtime_seconds": time.monotonic() - run_start,
            "phase_complete": phase,
            "RSS_peak_bytes": monitor.peak_rss,
        }
        return receipt


def self_test() -> None:
    repo = Path(__file__).resolve().parents[1]
    if digest_file(repo / V9_PRODUCER) != V9_PRODUCER_SHA:
        raise RuntimeError("selftest pinned v9 source drift")
    base = load_v9(repo)
    words = exact_words(base)
    if embed_f2_pb3(base, [1, 2]) != [1, 3] or \
            embed_f2_pb3(base, [2]) == [2]:
        raise RuntimeError("selftest F2/PB3 typing")
    six = [{"evaluated": True, "membership_proved": True}
           for _ in range(6)]
    partial = [{"evaluated": True, "membership_proved": i != 2}
               for i in range(6)]
    resource_prefix = [
        {"evaluated": True, "membership_proved": False},
        {"evaluated": False, "membership_proved": None},
    ]
    if not classify_results(six, True)["exact_typed_inert"] or \
            classify_results(partial, True)["exact_typed_inert"] or \
            classify_results([], False)["membership_bits"] != [None] * 6 or \
            classify_results(resource_prefix, False)["membership_bits"] != \
            [False, None, None, None, None, None]:
        raise RuntimeError("selftest terminal semantic core")
    if words["s"] != [-2] * 18 + [-1] * 18 + [2] * 18 + [1] * 18:
        raise RuntimeError("selftest strong word orientation")
    # Explicit mutation canaries that need no production quotient.
    mutations = {
        "wrong_y_embedding": embed_f2_pb3(base, [2]) != [2],
        "commutator_orientation":
            words["s"] != base.commutator(words["xi"], words["eta"]),
        "one_exponent": words["s"] !=
            base.commutator([2] * 17, words["xi"]),
        "delta_order": base.reduce_word(words["s"] + base.inv_word(F0)) !=
            base.reduce_word(F0 + base.inv_word(words["s"])),
    }
    if not all(mutations.values()):
        raise RuntimeError("selftest mutation separation")
    structural_monitor = base.ResourceMonitor(time.monotonic(), 18_000,
                                              lambda: 0)
    bind_resource_reason(structural_monitor, "element_pool")
    if resource_record(structural_monitor, True)["hit_reason"] != "element_pool":
        raise RuntimeError("selftest structural resource reason binding")
    print("D972_B345_T53_STRONG_S_PRODUCER_SELFTEST_PASS "
          "six_positive=1 partial=1 resource=1 input=1 wrong_y=1 "
          "resource_reason=1", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q3", type=Path, default=Q3_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    receipt = run(args.q3, args.output)
    checked_write(args.output, receipt)
    print(receipt["terminal_token"], flush=True)


if __name__ == "__main__":
    main()
