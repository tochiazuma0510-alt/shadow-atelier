#!/usr/bin/env python3
"""P3 row36 v6 outcome-free GAP-transition preregistration.

The GAP worker exports the complete right-transition permutations for the two
positive marked generators of Q3.  Python authenticates those permutations,
derives the two inverse permutations, replaces the trapped generic rank-seven
collector, and freezes all 34,992 row references together with a replayable
canonical-section derivation certificate.  No row predicate or Dpap value is
evaluated in this version.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, deque
from pathlib import Path
from typing import Any, Sequence

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_v3 as v3


RESULT_PATH = "ci/out/d972_row36_pent_bridge_p3_transition_results_v6_20260824.json"
GENERATOR_PATH = "search/d972_row36_pent_bridge_p3_transition_worker_generator_v6.py"
WORKER_PATH = "search/d972_row36_pent_bridge_p3_transition_worker_v6.g"
PROJECTION_SHA256 = "05a78aaf62e2ff691dbe80a95daebab849df8d9cb0dc7914a797a9e7e7590228"

_ACTIVE_RECEIPT: dict[str, Any] = {}


def projection_from_canary(receipt: dict[str, Any]) -> tuple[list[dict[str, Any]],
                                                              dict[bytes, tuple[int, ...]]]:
    trace = receipt.get("actual_charming_onto_gate", {}).get("full_gate_trace")
    base.require(isinstance(trace, list) and len(trace) == 19683,
                 "P3_V6_PROJECTION_TRACE_COUNT",
                 str(len(trace) if isinstance(trace, list) else -1))
    words: dict[bytes, tuple[int, ...]] = {}
    counts: Counter[bytes] = Counter()
    m_values: dict[bytes, set[int]] = {}
    for index, row in enumerate(trace):
        base.require(isinstance(row, dict) and all(
            key in row for key in ("f_coords", "f_word", "m")),
            "P3_V6_PROJECTION_ROW", str(index))
        coords = bytes(int(x) for x in row["f_coords"])
        word = tuple(int(x) for x in row["f_word"])
        base.require(len(coords) == 7 and all(x in (0, 1, 2) for x in coords),
                     "P3_V6_PROJECTION_COORD", str(index))
        base.require(all(x in (-2, -1, 1, 2) for x in word),
                     "P3_V6_PROJECTION_WORD", str(index))
        if coords in words:
            base.require(words[coords] == word,
                         "P3_V6_PROJECTION_WORD_CONFLICT", str(index))
        else:
            words[coords] = word
            m_values[coords] = set()
        counts[coords] += 1
        m_values[coords].add(int(row["m"]))
    expected = [bytes(row) for row in itertools.product(range(3), repeat=7)]
    base.require(sorted(words) == expected and len(set(words.values())) == 2187,
                 "P3_V6_PROJECTION_BIJECTION")
    base.require(all(counts[c] == 9 and m_values[c] == set(range(9))
                     for c in expected), "P3_V6_PROJECTION_REPEAT_GATE")
    projection = [{"q_coords": list(c), "signed_xy": list(words[c]),
                   "word_sha256": base.digest(list(words[c]))} for c in expected]
    base.require(base.digest(projection) == PROJECTION_SHA256,
                 "P3_V6_PROJECTION_DIGEST", base.digest(projection))
    return projection, words


def load_transition_backend(receipt: dict[str, Any], q2: dict[str, Any],
                            qcol: base.PcCollector,
                            qmarks: Sequence[bytes],
                            inverse_marks: Sequence[bytes]) -> dict[str, Any]:
    result_pin = base.file_pin(RESULT_PATH)
    payload = base.load_json(RESULT_PATH)
    base.require(isinstance(payload, list) and len(payload) == 3,
                 "P3_V6_TRANSITION_RESULT_SCHEMA")
    raw_states, raw_positive, raw_negative = payload
    expected_states = [list(row) for row in itertools.product(range(3), repeat=7)]
    base.require(raw_states == expected_states,
                 "P3_V6_TRANSITION_STATE_ORDER")
    states = tuple(bytes(row) for row in raw_states)
    index_of = {state: index for index, state in enumerate(states)}
    base.require(len(index_of) == 2187 and states[0] == qcol.one(),
                 "P3_V6_TRANSITION_STATE_COVER")

    def validate_permutations(raw: Any, label: str) -> tuple[tuple[int, ...], ...]:
        base.require(isinstance(raw, list) and len(raw) == 2,
                     "P3_V6_TRANSITION_PERM_COUNT", label)
        out = tuple(tuple(int(x) for x in row) for row in raw)
        for index, permutation in enumerate(out):
            base.require(len(permutation) == 2187 and
                         sorted(permutation) == list(range(2187)),
                         "P3_V6_TRANSITION_PERMUTATION",
                         repr((label, index)))
        return out

    positive = validate_permutations(raw_positive, "positive")
    negative = validate_permutations(raw_negative, "negative")
    for generator in range(2):
        base.require(all(
            positive[generator][negative[generator][i]] == i and
            negative[generator][positive[generator][i]] == i
            for i in range(2187)), "P3_V6_TRANSITION_INVERSE_PERM",
            str(generator))

    projection, word_by_state = projection_from_canary(receipt)
    by_letter = {1: positive[0], -1: negative[0],
                 2: positive[1], -2: negative[1]}

    def replay_index(start: int, word: Sequence[int]) -> int:
        current = start
        for letter in word:
            base.require(letter in by_letter, "P3_V6_TRANSITION_LETTER", str(letter))
            current = by_letter[int(letter)][current]
        return current

    base.require(positive[0][0] == index_of[qmarks[0]] and
                 positive[1][0] == index_of[qmarks[1]] and
                 negative[0][0] == index_of[inverse_marks[0]] and
                 negative[1][0] == index_of[inverse_marks[1]],
                 "P3_V6_MARKED_TRANSITION_GATE")
    for state, word in word_by_state.items():
        base.require(states[replay_index(0, word)] == state,
                     "P3_V6_PROJECTION_SIGNED_REPLAY", base.digest(list(state)))

    seen = {0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for permutation in positive:
            nxt = permutation[current]
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    base.require(len(seen) == 2187, "P3_V6_POSITIVE_MONOID_COVER", str(len(seen)))

    inverse_table: dict[bytes, bytes] = {}
    for state in states:
        inverse_table[state] = states[replay_index(
            0, base.inverse_word(word_by_state[state]))]

    def table_mul(left: bytes, right: bytes) -> bytes:
        base.require(left in index_of and right in word_by_state,
                     "P3_V6_TABLE_PRODUCT_INPUT")
        return states[replay_index(index_of[left], word_by_state[right])]

    def table_inverse(value: bytes) -> bytes:
        base.require(value in inverse_table, "P3_V6_TABLE_INVERSE_INPUT")
        return inverse_table[value]

    for state in states:
        inverse = inverse_table[state]
        base.require(table_mul(state, inverse) == states[0] and
                     table_mul(inverse, state) == states[0],
                     "P3_V6_TABLE_INVERSE_TWO_SIDED", base.digest(list(state)))

    qcol.mul = table_mul  # type: ignore[method-assign]
    qcol.inverse = table_inverse  # type: ignore[method-assign]

    units = []
    for index in range(7):
        row = [0] * 7
        row[index] = 1
        units.append(bytes(row))
    power_rows = inverse_rows = conjugate_rows = inverse_conjugate_rows = 0
    for index, unit in enumerate(units):
        base.require(qcol.power(unit, 3) == bytes(q2["pc_power_relations"][index]),
                     "P3_V6_PUBLIC_PC_POWER", str(index + 1))
        base.require(qcol.inverse(unit) == bytes(q2["pc_inverse_relations"][index]),
                     "P3_V6_PUBLIC_PC_INVERSE", str(index + 1))
        power_rows += 1
        inverse_rows += 1
    for row in q2["pc_conjugate_relations"]:
        i, j = int(row["i"]), int(row["j"])
        actual = qcol.mul(qcol.mul(qcol.inverse(units[j - 1]), units[i - 1]),
                          units[j - 1])
        base.require(actual == bytes(row["coords"]),
                     "P3_V6_PUBLIC_PC_CONJUGATE", repr((i, j)))
        conjugate_rows += 1
    for row in q2["pc_inverse_conjugate_relations"]:
        i, j = int(row["i"]), int(row["j"])
        actual = qcol.mul(qcol.mul(units[j - 1], units[i - 1]),
                          qcol.inverse(units[j - 1]))
        base.require(actual == bytes(row["coords"]),
                     "P3_V6_PUBLIC_PC_INVERSE_CONJUGATE", repr((i, j)))
        inverse_conjugate_rows += 1
    source = q2["source_presentation"]
    base.require(source.get("rank") == 2 and source.get("relation_count") == 0 and
                 source.get("relations") == [], "P3_V6_FREE_SOURCE_PRESENTATION")
    base.require(qcol.inverse(qmarks[0]) == inverse_marks[0] and
                 qcol.inverse(qmarks[1]) == inverse_marks[1],
                 "P3_V6_MARKED_INVERSE_COORDS")

    gate = {
        "result_pin": result_pin,
        "algorithm": (
            "complete GAP defining-basis right-transition permutations for positive "
            "x,y; inverse permutations derived by permutation inversion"
        ),
        "state_order": "lexicographic defining-basis Exponents coordinates [0,1,2]^7",
        "state_count": 2187,
        "positive_monoid_cover_count": len(seen),
        "projection_source": (
            "immutable p3-v5 canary full_gate_trace projected only to f_coords, "
            "f_word, and m"
        ),
        "projection_predicate_fields_used": False,
        "projection_sha256": base.digest(projection),
        "projection_signed_replay_count": len(word_by_state),
        "state_roster": [list(row) for row in states],
        "state_roster_sha256": base.digest([list(row) for row in states]),
        "positive_transition_permutations_zero_based": {
            "x": list(positive[0]), "y": list(positive[1])},
        "positive_transition_sha256": base.digest(
            [list(positive[0]), list(positive[1])]),
        "inverse_transition_permutations_zero_based": {
            "x_inverse": list(negative[0]), "y_inverse": list(negative[1])},
        "inverse_transition_sha256": base.digest(
            [list(negative[0]), list(negative[1])]),
        "public_pc_gate": {
            "defining_unit_rows": 7,
            "power_rows": power_rows,
            "inverse_rows": inverse_rows,
            "conjugate_rows": conjugate_rows,
            "inverse_conjugate_rows": inverse_conjugate_rows,
            "marked_positive_inverse_rows": 2,
            "free_source_rank": 2,
            "source_relator_rows": 0,
            "all_passed": True,
        },
        "generic_rank7_token_collector_used_after_install": False,
    }
    setattr(qcol, "p3_transition_gate_v6", gate)
    return gate


def validate_pc_receipt_v6(prime: int, q2: dict[str, Any], q4: dict[str, Any],
                           qcol: base.PcCollector, q4col: base.PcCollector):
    base.require(prime == 3, "P3_V6_PRIME_LOCAL", str(prime))
    base.require(q2.get("pc_generator_count") == 7 and
                 q2.get("relative_orders") == [3] * 7 and
                 int(q2["order_decimal"]) == 2187 and
                 q2.get("exponent") == 9 and q2.get("nilpotency_class") == 3,
                 "P3_V6_Q3_PUBLIC_SHAPE")
    base.require(q4.get("pc_generator_count") == len(q4col.orders) and
                 q4.get("relative_orders") == [3] * len(q4col.orders) and
                 q4.get("nilpotency_class") == 3,
                 "P3_V6_Q4_PUBLIC_SHAPE")
    qmarks = tuple(qcol.coord(row["coords"]) for row in q2["marked_generators"])
    inverse_marks = tuple(qcol.coord(row["inverse_coords"])
                          for row in q2["marked_generators"])
    q4marks = tuple(q4col.coord(row["coords"])
                    for row in q4["marked_generators"])
    base.require(len(qmarks) == len(inverse_marks) == 2 and len(q4marks) == 6,
                 "P3_V6_MARK_COUNTS")
    load_transition_backend(_ACTIVE_RECEIPT, q2, qcol, qmarks, inverse_marks)
    coarse, _ = base.marked_bfs_map(
        qcol, qmarks, 0, (1, 1), lambda a, b: (a + b) % 3,
        lambda a: (-a) % 3, 2187)
    base.require(len(coarse) == 2187, "P3_V6_MARKED_COARSE_COVER")
    return qmarks, q4marks


def decode_g(value: Sequence[Sequence[int]]) -> base.G:
    return tuple((int(row[0]), int(row[1])) for row in value)  # type: ignore[return-value]


def decode_perm(value: Sequence[int]) -> base.Perm:
    return tuple(int(x) - 1 for x in value)


def decode_joint(value: dict[str, Any], qcol: base.PcCollector):
    return (decode_g(value["g36"]), decode_perm(value["psl_one_line"]),
            qcol.coord(value["Qp_coords"]))


def residual_json(value: base.Residual) -> dict[str, Any]:
    return {"psl_one_line": base.encode_perm(value[0]),
            "Q3_coords": list(value[1])}


def replay_path(path: Sequence[int], chosen: Sequence[base.Residual],
                qcol: base.PcCollector) -> base.Residual:
    out: base.Residual = (base.PSL_ID, qcol.one())
    for signed_index in path:
        value = chosen[abs(int(signed_index)) - 1]
        if signed_index < 0:
            value = base.residual_inv(value, qcol)
        out = base.residual_mul(out, value, qcol)
    return out


def canonical_section_certificate(prereg: dict[str, Any],
                                  runtime: dict[str, Any]) -> dict[str, Any]:
    qcol: base.PcCollector = runtime["qcol"]
    qmarks: Sequence[bytes] = runtime["qmarks"]
    words, psl_values, q_values = base.build_g36_transversal(qcol, qmarks)
    base.require(len(words) == 23328, "P3_V6_DERIVATION_BFS_COUNT")
    bfs_rows = [{"G36": base.encode_g(g),
                 "signed_F2_word": list(words[g]),
                 "PSL_replay": base.encode_perm(psl_values[g]),
                 "Q3_replay": list(q_values[g])} for g in words]
    bfs_steps = []
    for letter in (1, -1, 2, -2):
        replay = base.eval_joint((letter,), qcol, qmarks)
        bfs_steps.append({"signed_letter": letter,
                          "G36": base.encode_g(replay[0]),
                          "PSL_one_line": base.encode_perm(replay[1]),
                          "Q3_coords": list(replay[2])})

    trace = prereg["enumeration_contract"]["Schreier_selected_generators"]
    block_rows: list[dict[str, Any]] = []
    blocks: list[tuple[int, ...]] = []
    chosen: list[base.Residual] = []
    for index, row in enumerate(trace, 1):
        word = tuple(int(x) for x in row["kernel_word_signed_xy"])
        replay = base.eval_joint(word, qcol, qmarks)
        residual = (decode_perm(row["residual_psl_one_line"]),
                    qcol.coord(row["residual_Qp_coords"]))
        base.require(replay[0] == base.gid() and
                     (replay[1], replay[2]) == residual,
                     "P3_V6_DERIVATION_BLOCK_REPLAY", str(index))
        inverse_word = base.inverse_word(word)
        inverse_replay = base.eval_joint(inverse_word, qcol, qmarks)
        inverse_residual = base.residual_inv(residual, qcol)
        base.require(inverse_replay[0] == base.gid() and
                     (inverse_replay[1], inverse_replay[2]) == inverse_residual,
                     "P3_V6_DERIVATION_INVERSE_BLOCK_REPLAY", str(index))
        blocks.append(word)
        chosen.append(residual)
        block_rows.append({
            "block_index_one_based": index,
            "positive_signed_F2_preimage_word": list(word),
            "positive_word_sha256": base.digest(list(word)),
            "positive_replay": {"G36": base.encode_g(replay[0]),
                                **residual_json(residual)},
            "negative_signed_F2_preimage_word": list(inverse_word),
            "negative_word_sha256": base.digest(list(inverse_word)),
            "negative_replay": {"G36": base.encode_g(inverse_replay[0]),
                                **residual_json(inverse_residual)},
            "generated_residual_closure_order": int(row["closure_order"]),
        })
    base.require(base.digest([list(word) for word in blocks]) ==
                 prereg["enumeration_contract"]["Schreier_block_roster_sha256"],
                 "P3_V6_DERIVATION_BLOCK_DIGEST")
    expected_residual = prereg["enumeration_contract"][
        "Schreier_residual_expected_order"]
    base.require(trace[-1]["closure_order"] == expected_residual == 504 * 2187,
                 "P3_V6_DERIVATION_RESIDUAL_ORDER")

    kernel_rows = prereg["joint_kernel_roster"]
    word_rows = prereg["canonical_word_roster"]
    base.require(len(kernel_rows) == len(word_rows) == 17496,
                 "P3_V6_DERIVATION_WORD_COUNT")
    derivations: list[dict[str, Any]] = []
    ordered_digests: list[str] = []
    for index, (kernel_row, word_row) in enumerate(zip(kernel_rows, word_rows)):
        base.require(kernel_row["z_index_zero_based"] == index and
                     kernel_row["word_id"] == word_row["word_id"] ==
                     f"W{index + 1:05d}", "P3_V6_DERIVATION_ORDER", str(index))
        final = decode_joint(kernel_row["jstar_z_joint_coords"], qcol)
        base_word = tuple(int(x) for x in word_row["g36_base_word_signed_xy"])
        base.require(base_word == words[final[0]],
                     "P3_V6_DERIVATION_BASE_WORD", str(index))
        base_replay = base.eval_joint(base_word, qcol, qmarks)
        base.require(base_replay == (final[0], psl_values[final[0]],
                                     q_values[final[0]]),
                     "P3_V6_DERIVATION_BASE_REPLAY", str(index))
        needed: base.Residual = (
            base.pinv(psl_values[final[0]]),
            qcol.mul(qcol.inverse(q_values[final[0]]), final[2]),
        )
        path = tuple(int(x) for x in word_row[
            "residual_block_path_signed_indices"])
        base.require(replay_path(path, chosen, qcol) == needed,
                     "P3_V6_DERIVATION_PATH_REPLAY", str(index))
        concatenated = base_word
        for signed_index in path:
            block = blocks[abs(signed_index) - 1]
            concatenated += (block if signed_index > 0 else
                             base.inverse_word(block))
        canonical = base.reduce_word(concatenated)
        base.require(list(canonical) == word_row["canonical_signed_xy"] and
                     base.digest(list(canonical)) == word_row["word_sha256"],
                     "P3_V6_DERIVATION_CANONICAL_WORD", str(index))
        final_replay = base.eval_joint(canonical, qcol, qmarks)
        base.require(final_replay == final,
                     "P3_V6_DERIVATION_FINAL_REPLAY", str(index))
        reduction = [0, base.encode_g(base.reduce_g36(final[0], 9)),
                     base.encode_perm(final[1])]
        base.require(reduction == base.TARGET_KEY,
                     "P3_V6_DERIVATION_ROW36_REDUCTION", str(index))
        ordered_digests.append(word_row["word_sha256"])
        derivations.append({
            "z_index_zero_based": index,
            "word_id": word_row["word_id"],
            "G36_base_word_storage": (
                f"canonical_word_roster[{index}].g36_base_word_signed_xy"),
            "G36_base_word_sha256": base.digest(list(base_word)),
            "signed_residual_path_storage": (
                f"canonical_word_roster[{index}].residual_block_path_signed_indices"),
            "signed_residual_path_sha256": base.digest(list(path)),
            "required_residual_after_base_word": residual_json(needed),
            "concatenation_before_free_reduce_length": len(concatenated),
            "concatenation_before_free_reduce_sha256": base.digest(list(concatenated)),
            "canonical_word_storage": (
                f"canonical_word_roster[{index}].canonical_signed_xy"),
            "canonical_word_sha256": word_row["word_sha256"],
            "canonical_joint_replay_sha256": base.digest(base.encode_joint(final_replay)),
            "exact_row36_reduction": reduction,
        })

    base.require(len(prereg["raw_rows"]) == 34992 and
                 all(prereg["raw_rows"][i]["word_id"] ==
                     word_rows[i % 17496]["word_id"] for i in range(34992)),
                 "P3_V6_DERIVATION_RAW_WORD_BINDING")
    target_replay = base.eval_joint(base.TARGET_WORD, qcol, qmarks)
    w1_replay = base.eval_joint(word_rows[0]["canonical_signed_xy"], qcol, qmarks)
    base.require(target_replay == w1_replay == decode_joint(
                     kernel_rows[0]["jstar_z_joint_coords"], qcol),
                 "P3_V6_DERIVATION_ARCHIVED_SECTION_IMAGE")
    return {
        "schema": "d972-row36-pent-bridge-p3-canonical-section-certificate/v6",
        "scope": "outcome-free derivation of all 17,496 section words and 34,992 row references",
        "archived_word_is_a_row_witness_not_a_required_section_root": True,
        "W00001": {"length": len(word_rows[0]["canonical_signed_xy"]),
                    "sha256": word_rows[0]["word_sha256"],
                    "same_joint_image_as_archived_word": True},
        "archived_word": {"length": len(base.TARGET_WORD),
                           "sha256": base.TARGET_WORD_DIGEST},
        "G36_right_Cayley_BFS": {
            "root": {"G36": base.encode_g(base.gid()), "signed_F2_word": [],
                     "PSL_one_line": base.encode_perm(base.PSL_ID),
                     "Q3_coords": list(qcol.one())},
            "ordered_steps": bfs_steps,
            "multiplication_side": "right",
            "queue": "FIFO",
            "tie_rule": (
                "first discovery wins; vertices in FIFO discovery order, "
                "outgoing signed letters [1,-1,2,-2]"
            ),
            "state_count": len(bfs_rows),
            "ordered_state_roster_sha256": base.digest(
                [row["G36"] for row in bfs_rows]),
            "ordered_full_replay_roster_sha256": base.digest(bfs_rows),
        },
        "ordered_signed_Schreier_block_preimages": block_rows,
        "Schreier_contract": {
            "edge_scan": "G36 BFS discovery order, then [1,-1,2,-2]",
            "selection": "first residual outside closure of prior selected residuals",
            "signed_path_BFS_steps": "+block1,-block1,+block2,-block2,...",
            "residual_order": expected_residual,
            "block_count": len(blocks),
            "block_roster_sha256": base.digest([list(word) for word in blocks]),
        },
        "canonical_section_formula": {
            "formula": (
                "free_reduce(G36_base_word || signed_block(path[1]) || ... || "
                "signed_block(path[n]))"
            ),
            "signed_block_negative": "reverse block and negate each letter",
            "free_reduce": "left-to-right stack cancelling only adjacent a,-a",
            "fully_serialized_storage": {
                "G36_base_words": "canonical_word_roster[*].g36_base_word_signed_xy",
                "signed_residual_paths": (
                    "canonical_word_roster[*].residual_block_path_signed_indices"),
                "result_words": "canonical_word_roster[*].canonical_signed_xy",
            },
        },
        "per_kernel_coordinate_derivation": derivations,
        "ordered_resulting_word_digests": ordered_digests,
        "ordered_resulting_word_digests_sha256": base.digest(ordered_digests),
        "canonical_word_roster_sha256": base.digest(word_rows),
        "raw_34992_row_roster_sha256": base.digest(prereg["raw_rows"]),
        "all_34992_rows_reference_the_frozen_section_word_for_their_kernel_coordinate": True,
        "predicate_outcomes_evaluated": False,
        "independent_helper_disjoint_replay_pending": True,
        "terminal_token": "PENT159O_ROW36_P3_V6_CANONICAL_SECTION_PREREGISTERED",
    }


def install(prime: int) -> None:
    base.require(prime == 3, "P3_V6_PRIME_LOCAL", str(prime))
    v3.install(prime, None)
    build_raw_v3 = base.build_raw_universe

    def source_pins(_: int) -> list[dict[str, Any]]:
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p3_v6.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v6.py"),
            base.file_pin(GENERATOR_PATH),
            base.file_pin(WORKER_PATH),
        ]

    def paths_for(_: int) -> dict[str, str]:
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p3_prereg_v6_{base.DATE}.json",
            "receipt": f"search/certs/d972_row36_pent_bridge_p3_receipt_v6_{base.DATE}.json",
            "manifest": f"search/certs/d972_row36_pent_bridge_p3_manifest_v6_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt: dict[str, Any]):
        global _ACTIVE_RECEIPT
        _ACTIVE_RECEIPT = receipt
        base.validate_pc_receipt = validate_pc_receipt_v6
        prereg, runtime = build_raw_v3(prime_arg, receipt)
        transition_gate = runtime["qcol"].p3_transition_gate_v6
        prereg["schema"] = "d972-row36-pent-bridge-p3-prereg/v6"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"]["p3_prior_preflight_stops"] = [
            {"version": "v3", "exact_stop": "PC_COLLECTION_CAP: (25, 7)",
             "classification": "generic inverse expansion resource trap; no prereg"},
            {"version": "v4", "exact_stop": "PC_COLLECTION_CAP: (16, 7)",
             "classification": "dense inverse BFS resource trap; no prereg"},
            {"version": "v5", "exact_stop": "P3_EXPORTED_PC_CONJUGATE: (3, 1)",
             "classification": "hand-derived Hall law rejected; no prereg or outcome"},
        ]
        prereg["execution_routing"]["p3_v6_GAP_transition_preflight"] = {
            "result_pin": transition_gate["result_pin"],
            "outcome_free": True,
            "GAP_defining_basis_authenticated": True,
            "positive_transition_permutations": 2,
            "inverse_permutations_derived": 2,
            "state_count": 2187,
            "generic_rank7_collector_after_install": False,
        }
        prereg["Q3_full_transition_freeze"] = transition_gate
        prereg["canonical_section_derivation_certificate"] = \
            canonical_section_certificate(prereg, runtime)
        prereg["coverage_freeze"]["predicate_outcomes_not_evaluated"] = True
        prereg["coverage_freeze"]["canonical_section_derivation_serialized"] = True
        prereg["forbidden_promotions"] = {
            "mode_token": None, "K2_name": None, "all_prime_inference": False}
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = "PENT159O_ROW36_P3_PREREG_V6_FROZEN"
        return prereg, runtime

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw


def main_for_prime(prime: int) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare",))
    args = parser.parse_args()
    base.require(args.phase == "prepare", "P3_V6_PREREG_ONLY")
    install(prime)
    raise SystemExit(base.run(prime, ["prepare"]))

