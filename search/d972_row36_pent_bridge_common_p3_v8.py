#!/usr/bin/env python3
"""P3 row36 v8 paper/native transition-orientation repair."""

from __future__ import annotations

import argparse
import itertools
from collections import deque
from typing import Any, Sequence

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_p3_v6 as v6
import d972_row36_pent_bridge_common_p3_v7 as v7


RESULT_PATH = "ci/out/d972_row36_pent_bridge_p3_transition_results_v8_20260824.json"
GENERATOR_PATH = "search/d972_row36_pent_bridge_p3_transition_worker_generator_v8.py"
WORKER_PATH = "search/d972_row36_pent_bridge_p3_transition_worker_v8.g"


def load_transition_backend_v8(receipt: dict[str, Any], q2: dict[str, Any],
                               qcol: base.PcCollector,
                               qmarks: Sequence[bytes],
                               inverse_marks: Sequence[bytes]) -> dict[str, Any]:
    result_pin = base.file_pin(RESULT_PATH)
    payload = base.load_json(RESULT_PATH)
    base.require(isinstance(payload, list) and len(payload) == 5,
                 "P3_V8_TRANSITION_RESULT_SCHEMA")
    raw_states, raw_right, raw_right_inverse, raw_paper, raw_paper_inverse = payload
    expected_states = [list(row) for row in itertools.product(range(3), repeat=7)]
    base.require(raw_states == expected_states, "P3_V8_TRANSITION_STATE_ORDER")
    states = tuple(bytes(row) for row in raw_states)
    index_of = {state: index for index, state in enumerate(states)}
    base.require(len(index_of) == 2187 and states[0] == qcol.one(),
                 "P3_V8_TRANSITION_STATE_COVER")

    def permutations(raw: Any, label: str) -> tuple[tuple[int, ...], ...]:
        base.require(isinstance(raw, list) and len(raw) == 2,
                     "P3_V8_TRANSITION_PERM_COUNT", label)
        out = tuple(tuple(int(x) for x in row) for row in raw)
        for index, permutation in enumerate(out):
            base.require(len(permutation) == 2187 and
                         sorted(permutation) == list(range(2187)),
                         "P3_V8_TRANSITION_PERMUTATION", repr((label, index)))
        return out

    right = permutations(raw_right, "native_right")
    right_inverse = permutations(raw_right_inverse, "native_right_inverse")
    paper = permutations(raw_paper, "paper_left")
    paper_inverse = permutations(raw_paper_inverse, "paper_left_inverse")
    for positive, negative, label in (
        (right, right_inverse, "native_right"),
        (paper, paper_inverse, "paper_left"),
    ):
        for generator in range(2):
            base.require(all(
                positive[generator][negative[generator][i]] == i and
                negative[generator][positive[generator][i]] == i
                for i in range(2187)), "P3_V8_TRANSITION_INVERSE_PERM",
                repr((label, generator)))

    projection, word_by_state = v6.projection_from_canary(receipt)
    paper_by_letter = {1: paper[0], -1: paper_inverse[0],
                       2: paper[1], -2: paper_inverse[1]}
    right_by_letter = {1: right[0], -1: right_inverse[0],
                       2: right[1], -2: right_inverse[1]}

    def replay(start: int, word: Sequence[int], table: dict[int, tuple[int, ...]]) -> int:
        current = start
        for letter in word:
            base.require(letter in table, "P3_V8_TRANSITION_LETTER", str(letter))
            current = table[int(letter)][current]
        return current

    for positive, negative in ((right, right_inverse), (paper, paper_inverse)):
        base.require(positive[0][0] == index_of[qmarks[0]] and
                     positive[1][0] == index_of[qmarks[1]] and
                     negative[0][0] == index_of[inverse_marks[0]] and
                     negative[1][0] == index_of[inverse_marks[1]],
                     "P3_V8_MARKED_TRANSITION_GATE")
    for state, word in word_by_state.items():
        base.require(states[replay(0, word, paper_by_letter)] == state,
                     "P3_V8_PAPER_PROJECTION_SIGNED_REPLAY",
                     base.digest(list(state)))

    state2 = states[1]
    state2_word = word_by_state[state2]
    state2_right = replay(0, state2_word, right_by_letter)
    state2_paper = replay(0, state2_word, paper_by_letter)
    base.require(state2_word == (1, 1, 2, -1, -2, -1) and
                 state2_paper == 1 and state2_right != 1,
                 "P3_V8_STATE2_ORIENTATION_DISCRIMINATOR",
                 repr((state2_word, state2_right, state2_paper)))

    seen = {0}
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for permutation in right:
            nxt = permutation[current]
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    base.require(len(seen) == 2187, "P3_V8_NATIVE_RIGHT_MONOID_COVER")

    inverse_table: dict[bytes, bytes] = {}
    for state in states:
        inverse_table[state] = states[replay(
            0, base.inverse_word(word_by_state[state]), paper_by_letter)]

    def table_mul(left: bytes, right_value: bytes) -> bytes:
        base.require(left in word_by_state and right_value in index_of,
                     "P3_V8_TABLE_PRODUCT_INPUT")
        # Paper append is native left multiplication.  Starting at right and
        # replaying a paper word for left therefore returns left*right.
        return states[replay(index_of[right_value], word_by_state[left],
                             paper_by_letter)]

    def table_inverse(value: bytes) -> bytes:
        base.require(value in inverse_table, "P3_V8_TABLE_INVERSE_INPUT")
        return inverse_table[value]

    for state in states:
        inverse = inverse_table[state]
        base.require(table_mul(state, inverse) == states[0] and
                     table_mul(inverse, state) == states[0],
                     "P3_V8_TABLE_INVERSE_TWO_SIDED", base.digest(list(state)))
        base.require(table_mul(state, qmarks[0]) == states[right[0][index_of[state]]] and
                     table_mul(state, qmarks[1]) == states[right[1][index_of[state]]],
                     "P3_V8_NATIVE_RIGHT_PRODUCT_BRIDGE", base.digest(list(state)))
        base.require(table_mul(qmarks[0], state) == states[paper[0][index_of[state]]] and
                     table_mul(qmarks[1], state) == states[paper[1][index_of[state]]],
                     "P3_V8_PAPER_LEFT_PRODUCT_BRIDGE", base.digest(list(state)))

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
                     "P3_V8_PUBLIC_PC_POWER", str(index + 1))
        base.require(qcol.inverse(unit) == bytes(q2["pc_inverse_relations"][index]),
                     "P3_V8_PUBLIC_PC_INVERSE", str(index + 1))
        power_rows += 1
        inverse_rows += 1
    for row in q2["pc_conjugate_relations"]:
        i, j = int(row["i"]), int(row["j"])
        actual = qcol.mul(qcol.mul(qcol.inverse(units[j - 1]), units[i - 1]),
                          units[j - 1])
        base.require(actual == bytes(row["coords"]),
                     "P3_V8_PUBLIC_PC_CONJUGATE", repr((i, j)))
        conjugate_rows += 1
    for row in q2["pc_inverse_conjugate_relations"]:
        i, j = int(row["i"]), int(row["j"])
        actual = qcol.mul(qcol.mul(units[j - 1], units[i - 1]),
                          qcol.inverse(units[j - 1]))
        base.require(actual == bytes(row["coords"]),
                     "P3_V8_PUBLIC_PC_INVERSE_CONJUGATE", repr((i, j)))
        inverse_conjugate_rows += 1
    source = q2["source_presentation"]
    base.require(source.get("rank") == 2 and source.get("relation_count") == 0 and
                 source.get("relations") == [], "P3_V8_FREE_SOURCE_PRESENTATION")
    base.require(qcol.inverse(qmarks[0]) == inverse_marks[0] and
                 qcol.inverse(qmarks[1]) == inverse_marks[1],
                 "P3_V8_MARKED_INVERSE_COORDS")

    gate = {
        "result_pin": result_pin,
        "algorithm": (
            "GAP exports both native-right (state*mark) and paper-append/native-left "
            "(mark*state) permutations; frozen canary projection words replay through "
            "paper transitions, while Python table_mul is the native product"
        ),
        "state_order": "explicit base-three lex defining-basis coordinates",
        "state_count": 2187,
        "native_right_positive_monoid_cover_count": len(seen),
        "projection_source": (
            "immutable p3-v5 full_gate_trace projected only to f_coords, f_word, m"
        ),
        "projection_predicate_fields_used": False,
        "projection_sha256": base.digest(projection),
        "paper_projection_signed_replay_count": len(word_by_state),
        "state2_orientation_canary": {
            "expected_coords": list(state2),
            "paper_word": list(state2_word),
            "native_written_right_index_zero_based": state2_right,
            "paper_append_left_index_zero_based": state2_paper,
            "branches_distinct": True,
        },
        "state_roster": [list(row) for row in states],
        "state_roster_sha256": base.digest([list(row) for row in states]),
        "native_right_positive_zero_based": {"x": list(right[0]), "y": list(right[1])},
        "native_right_positive_sha256": base.digest([list(right[0]), list(right[1])]),
        "native_right_inverse_zero_based": {"x_inverse": list(right_inverse[0]),
                                             "y_inverse": list(right_inverse[1])},
        "native_right_inverse_sha256": base.digest(
            [list(right_inverse[0]), list(right_inverse[1])]),
        "paper_left_positive_zero_based": {"x": list(paper[0]), "y": list(paper[1])},
        "paper_left_positive_sha256": base.digest([list(paper[0]), list(paper[1])]),
        "paper_left_inverse_zero_based": {"x_inverse": list(paper_inverse[0]),
                                           "y_inverse": list(paper_inverse[1])},
        "paper_left_inverse_sha256": base.digest(
            [list(paper_inverse[0]), list(paper_inverse[1])]),
        "native_product_bridge_rows": 2187 * 4,
        "public_pc_gate": {
            "defining_unit_rows": 7, "power_rows": power_rows,
            "inverse_rows": inverse_rows, "conjugate_rows": conjugate_rows,
            "inverse_conjugate_rows": inverse_conjugate_rows,
            "marked_positive_inverse_rows": 2, "free_source_rank": 2,
            "source_relator_rows": 0, "all_passed": True,
        },
        "generic_rank7_token_collector_used_after_install": False,
    }
    setattr(qcol, "p3_transition_gate_v6", gate)
    return gate


def install(prime: int) -> None:
    base.require(prime == 3, "P3_V8_PRIME_LOCAL", str(prime))
    v6.load_transition_backend = load_transition_backend_v8
    v7.RESULT_PATH = RESULT_PATH
    v7.GENERATOR_PATH = GENERATOR_PATH
    v7.WORKER_PATH = WORKER_PATH
    v7.install(prime)
    build_raw_v7 = base.build_raw_universe

    def source_pins(_: int):
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p3_v6.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v6.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p3_v7.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v7.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_transition_worker_v7.g"),
            base.file_pin("search/d972_row36_pent_bridge_common_p3_v8.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v8.py"),
            base.file_pin(GENERATOR_PATH), base.file_pin(WORKER_PATH),
        ]

    def paths_for(_: int):
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p3_prereg_v8_{base.DATE}.json",
            "receipt": f"search/certs/d972_row36_pent_bridge_p3_receipt_v8_{base.DATE}.json",
            "manifest": f"search/certs/d972_row36_pent_bridge_p3_manifest_v8_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt):
        prereg, runtime = build_raw_v7(prime_arg, receipt)
        prereg["schema"] = "d972-row36-pent-bridge-p3-prereg/v8"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"]["p3_v7_run_stop"] = {
            "run_id": 32668755598,
            "commit": "96af1d09b3b106c1cf722e74f9a1e74d9ddf18c6",
            "passed": ["PUBLIC_PC_PASS", "STATE_SERIALIZATION_PASS 2187/2187"],
            "exact_stop": (
                "PENT159O_ROW36_P3_WORKER_V7: signed projection replay drift state=2"
            ),
            "classification": (
                "projection words are paper words: appending on the paper right is "
                "native GAP left multiplication; v7 replayed native right transitions"
            ),
            "artifact_or_preregistration": False,
            "mathematical_result": False,
        }
        prereg["execution_routing"]["p3_v8_paper_native_orientation_repair"] = {
            "universe_or_predicate_change": False,
            "paper_append_rule": "append paper letter on right = native left multiplication",
            "GAP_exports_both_transition_sides": True,
            "state2_destructive_orientation_canary":
                runtime["qcol"].p3_transition_gate_v6["state2_orientation_canary"],
            "all_2187_paper_projection_words_replayed": True,
            "native_table_product_bridge_rows": 2187 * 4,
            "outcome_free": True,
        }
        certificate = prereg["canonical_section_derivation_certificate"]
        certificate["schema"] = \
            "d972-row36-pent-bridge-p3-canonical-section-certificate/v8"
        certificate["Q3_word_serialization_bridge"] = {
            "canary_projection_words": "paper serialization",
            "paper_append": "native GAP left multiplication",
            "row36_section_words": "native signed words evaluated with native table_mul",
            "bridge": (
                "table_mul(left,right) replays a paper word for left from state right, "
                "therefore returns native left*right"
            ),
            "state2_and_all_2187_projection_gates": True,
        }
        certificate["terminal_token"] = \
            "PENT159O_ROW36_P3_V8_CANONICAL_SECTION_PREREGISTERED"
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = "PENT159O_ROW36_P3_PREREG_V8_FROZEN"
        return prereg, runtime

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw


def main_for_prime(prime: int) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare",))
    args = parser.parse_args()
    base.require(args.phase == "prepare", "P3_V8_PREREG_ONLY")
    install(prime)
    raise SystemExit(base.run(prime, ["prepare"]))

