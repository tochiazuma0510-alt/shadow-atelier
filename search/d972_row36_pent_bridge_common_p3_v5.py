#!/usr/bin/env python3
"""P3-only finite transition backend for the fixed-row36 bridge v5.

The generic rank-seven token collector is not used for Q3 multiplication.
Instead, the immutable p3 canary's complete word/coordinate projection is
authenticated against the explicit class-three Hall law, then two positive
right-Cayley transition permutations are frozen.  Signed steps use only the
permutation inverses.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter, deque
from pathlib import Path
from typing import Any, Sequence

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_v3 as v3


Hall = tuple[int, int, int, int, int]
HALL_ONE: Hall = (0, 0, 0, 0, 0)
HALL_X: Hall = (1, 0, 0, 0, 0)
HALL_Y: Hall = (0, 1, 0, 0, 0)


def choose2(value: int) -> int:
    return value * (value - 1) // 2


def hall_mul(left: Hall, right: Hall) -> Hall:
    """Multiply x^a y^b c^e d^d h^h coordinates.

    Here c=[y,x], d=[c,x], h=[c,y], with x,y of order 9 and
    c,d,h of order 3.  The formula is integral collection before the
    displayed reductions.
    """
    a, b, e, d, h = left
    aa, bb, ee, dd, hh = right
    crossed_c = e + aa * b
    return ((a + aa) % 9,
            (b + bb) % 9,
            (crossed_c + ee) % 3,
            (d + dd + e * aa + b * choose2(aa)) % 3,
            (h + hh + aa * choose2(b) + crossed_c * bb) % 3)


def hall_power(value: Hall, exponent: int) -> Hall:
    base.require(exponent >= 0, "P3_HALL_NEGATIVE_POWER", str(exponent))
    out = HALL_ONE
    current = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            out = hall_mul(out, current)
        current = hall_mul(current, current)
        remaining //= 2
    return out


def hall_inverse(value: Hall) -> Hall:
    # The frozen Q3 receipt pins exponent 9; this is checked before use.
    return hall_power(value, 8)


def hall_eval_signed_xy(word: Sequence[int]) -> Hall:
    out = HALL_ONE
    inverse_x = hall_inverse(HALL_X)
    inverse_y = hall_inverse(HALL_Y)
    images = {1: HALL_X, -1: inverse_x, 2: HALL_Y, -2: inverse_y}
    for letter in word:
        base.require(letter in images, "P3_HALL_WORD_ALPHABET", str(letter))
        out = hall_mul(out, images[letter])
    return out


def hall_conjugate(value: Hall, conjugator: Hall) -> Hall:
    return hall_mul(hall_mul(hall_inverse(conjugator), value), conjugator)


def extract_complete_projection(receipt: dict[str, Any],
                                qcol: base.PcCollector) -> tuple[list[dict[str, Any]], dict[bytes, tuple[int, ...]]]:
    gate = receipt.get("actual_charming_onto_gate", {})
    trace = gate.get("full_gate_trace")
    base.require(isinstance(trace, list) and len(trace) == 19683,
                 "P3_CANARY_PROJECTION_TRACE_COUNT",
                 str(len(trace) if isinstance(trace, list) else -1))
    words: dict[bytes, tuple[int, ...]] = {}
    multiplicities: Counter[bytes] = Counter()
    m_values: dict[bytes, set[int]] = {}
    for index, row in enumerate(trace):
        base.require(isinstance(row, dict) and "f_coords" in row and
                     "f_word" in row and "m" in row,
                     "P3_CANARY_PROJECTION_ROW", str(index))
        coords = qcol.coord(row["f_coords"])
        word = tuple(int(x) for x in row["f_word"])
        base.require(all(x in (-2, -1, 1, 2) for x in word),
                     "P3_CANARY_PROJECTION_WORD", str(index))
        if coords in words:
            base.require(words[coords] == word,
                         "P3_CANARY_PROJECTION_WORD_CONFLICT", str(index))
        else:
            words[coords] = word
            m_values[coords] = set()
        multiplicities[coords] += 1
        m_values[coords].add(int(row["m"]))
    base.require(len(words) == 2187 and len(set(words.values())) == 2187,
                 "P3_CANARY_PROJECTION_BIJECTION",
                 repr((len(words), len(set(words.values())))))
    base.require(all(multiplicities[c] == 9 and m_values[c] == set(range(9))
                     for c in words), "P3_CANARY_PROJECTION_REPEAT_GATE")
    projection = [{"q_coords": list(coords), "signed_xy": list(words[coords]),
                   "word_sha256": base.digest(list(words[coords]))}
                  for coords in sorted(words)]
    return projection, words


def exported_pc_relation_gate(q2: dict[str, Any],
                              q_to_hall: dict[bytes, Hall],
                              hall_to_q: dict[Hall, bytes]) -> dict[str, Any]:
    rank = int(q2["pc_generator_count"])
    base.require(rank == 7 and q2["relative_orders"] == [3] * 7,
                 "P3_EXPORTED_PC_SHAPE")
    units = []
    for index in range(rank):
        row = [0] * rank
        row[index] = 1
        units.append(bytes(row))

    power_pass = 0
    inverse_pass = 0
    conjugate_pass = 0
    inverse_conjugate_pass = 0
    for index, unit in enumerate(units):
        expected_power = bytes(q2["pc_power_relations"][index])
        expected_inverse = bytes(q2["pc_inverse_relations"][index])
        base.require(hall_to_q[hall_power(q_to_hall[unit], 3)] == expected_power,
                     "P3_EXPORTED_PC_POWER", str(index + 1))
        base.require(hall_to_q[hall_inverse(q_to_hall[unit])] == expected_inverse,
                     "P3_EXPORTED_PC_INVERSE", str(index + 1))
        power_pass += 1
        inverse_pass += 1
    for row in q2["pc_conjugate_relations"]:
        i, j = int(row["i"]), int(row["j"])
        actual = hall_conjugate(q_to_hall[units[i - 1]],
                                q_to_hall[units[j - 1]])
        base.require(hall_to_q[actual] == bytes(row["coords"]),
                     "P3_EXPORTED_PC_CONJUGATE", repr((i, j)))
        conjugate_pass += 1
    for row in q2["pc_inverse_conjugate_relations"]:
        i, j = int(row["i"]), int(row["j"])
        actual = hall_conjugate(q_to_hall[units[i - 1]],
                                hall_inverse(q_to_hall[units[j - 1]]))
        base.require(hall_to_q[actual] == bytes(row["coords"]),
                     "P3_EXPORTED_PC_INVERSE_CONJUGATE", repr((i, j)))
        inverse_conjugate_pass += 1
    return {"pc_power_rows": power_pass, "pc_inverse_rows": inverse_pass,
            "pc_conjugate_rows": conjugate_pass,
            "pc_inverse_conjugate_rows": inverse_conjugate_pass,
            "all_exported_pc_rows_replayed": True}


def install_positive_transition_backend(receipt: dict[str, Any],
                                        q2: dict[str, Any],
                                        qcol: base.PcCollector,
                                        qmarks: Sequence[bytes],
                                        qinverse_marks: Sequence[bytes]) -> dict[str, Any]:
    base.require(int(q2["order_decimal"]) == 2187 and
                 int(q2["exponent"]) == 9 and
                 int(q2["nilpotency_class"]) == 3,
                 "P3_HALL_Q3_ORDER_EXPONENT_CLASS")
    projection, projection_words = extract_complete_projection(receipt, qcol)
    q_to_hall: dict[bytes, Hall] = {}
    hall_to_q: dict[Hall, bytes] = {}
    for row in projection:
        coords = bytes(row["q_coords"])
        hall = hall_eval_signed_xy(row["signed_xy"])
        base.require(coords not in q_to_hall and hall not in hall_to_q,
                     "P3_HALL_PROJECTION_DUPLICATE")
        q_to_hall[coords] = hall
        hall_to_q[hall] = coords
    expected_hall = set(itertools.product(range(9), range(9), range(3),
                                          range(3), range(3)))
    base.require(len(q_to_hall) == len(hall_to_q) == 2187 and
                 set(hall_to_q) == expected_hall,
                 "P3_HALL_FULL_COORDINATE_COVER")
    base.require(hall_to_q[HALL_X] == qmarks[0] and
                 hall_to_q[HALL_Y] == qmarks[1] and
                 hall_to_q[hall_inverse(HALL_X)] == qinverse_marks[0] and
                 hall_to_q[hall_inverse(HALL_Y)] == qinverse_marks[1],
                 "P3_HALL_MARKED_POSITIVE_INVERSE_GATE")

    relation_gate = exported_pc_relation_gate(q2, q_to_hall, hall_to_q)
    state_roster = sorted(q_to_hall)
    state_index = {state: index for index, state in enumerate(state_roster)}
    positive: list[list[int]] = []
    for marked_hall in (HALL_X, HALL_Y):
        permutation = [state_index[hall_to_q[
            hall_mul(q_to_hall[state], marked_hall)]] for state in state_roster]
        base.require(sorted(permutation) == list(range(2187)),
                     "P3_POSITIVE_TRANSITION_PERMUTATION")
        positive.append(permutation)
    negative: list[list[int]] = []
    for permutation in positive:
        inverse = [-1] * 2187
        for source, target in enumerate(permutation):
            inverse[target] = source
        base.require(all(value >= 0 for value in inverse) and
                     all(permutation[inverse[index]] == index and
                         inverse[permutation[index]] == index
                         for index in range(2187)),
                     "P3_INVERSE_TRANSITION_PERMUTATION")
        negative.append(inverse)

    identity_index = state_index[hall_to_q[HALL_ONE]]
    seen = {identity_index}
    queue = deque([identity_index])
    while queue:
        current = queue.popleft()
        for permutation in positive:
            nxt = permutation[current]
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    base.require(len(seen) == 2187, "P3_POSITIVE_MONOID_CAYLEY_COVER",
                 str(len(seen)))

    transition_by_letter = {1: positive[0], -1: negative[0],
                            2: positive[1], -2: negative[1]}
    signed_replay_count = 0
    for expected_coords, word in projection_words.items():
        current = identity_index
        for letter in word:
            current = transition_by_letter[letter][current]
        base.require(state_roster[current] == expected_coords,
                     "P3_SIGNED_TRANSITION_WORD_REPLAY",
                     base.digest([list(expected_coords), list(word)]))
        signed_replay_count += 1

    inverse_table = {coords: hall_to_q[hall_inverse(q_to_hall[coords])]
                     for coords in state_roster}
    for coords, inverse in inverse_table.items():
        base.require(hall_mul(q_to_hall[coords], q_to_hall[inverse]) == HALL_ONE and
                     hall_mul(q_to_hall[inverse], q_to_hall[coords]) == HALL_ONE,
                     "P3_HALL_INVERSE_TWO_SIDED")

    def table_mul(left: bytes, right: bytes) -> bytes:
        base.require(left in q_to_hall and right in q_to_hall,
                     "P3_TRANSITION_PRODUCT_INPUT")
        return hall_to_q[hall_mul(q_to_hall[left], q_to_hall[right])]

    def table_inverse(value: bytes) -> bytes:
        base.require(value in inverse_table, "P3_TRANSITION_INVERSE_INPUT")
        return inverse_table[value]

    qcol.mul = table_mul  # type: ignore[method-assign]
    qcol.inverse = table_inverse  # type: ignore[method-assign]
    gate = {
        "algorithm": "complete positive right-Cayley permutations for x,y; negative steps are inverse permutations",
        "state_order": "lexicographic exported seven-coordinate vectors",
        "state_count": 2187,
        "positive_monoid_cover_count": len(seen),
        "signed_word_replay_count": signed_replay_count,
        "projection_source": "immutable p3-v5 canary receipt actual_charming_onto_gate.full_gate_trace, projected only to (f_coords,f_word,m)",
        "predicate_fields_read_or_used": False,
        "projection_sha256": base.digest(projection),
        "Hall_model": "x^a y^b [y,x]^e [[y,x],x]^d [[y,x],y]^h; a,b mod9; e,d,h mod3",
        "Hall_to_exported_coordinate_bijection": True,
        "marked_positive_inverse_match_exported": True,
        "exported_pc_relation_gate": relation_gate,
        "state_roster": [list(state) for state in state_roster],
        "state_roster_sha256": base.digest([list(state) for state in state_roster]),
        "positive_transition_permutations_zero_based": {"x": positive[0],
                                                         "y": positive[1]},
        "positive_transition_sha256": base.digest(positive),
        "inverse_transition_permutations_zero_based": {"x_inverse": negative[0],
                                                        "y_inverse": negative[1]},
        "inverse_transition_sha256": base.digest(negative),
        "generic_rank7_token_collector_used_after_install": False,
    }
    setattr(qcol, "p3_positive_transition_gate", gate)
    return gate


def validate_pc_receipt_v5(prime: int, q2: dict[str, Any], q4: dict[str, Any],
                           qcol: base.PcCollector, q4col: base.PcCollector):
    base.require(prime == 3, "P3_V5_PRIME_LOCAL", str(prime))
    base.require(len(qcol.orders) == 7 and int(q2["order_decimal"]) == 2187 and
                 q2["nilpotency_class"] == 3,
                 "P3_Q3_COLLECTOR_ORDER_CLASS")
    base.require(len(q4col.orders) == int(q4["pc_generator_count"]) and
                 int(q4["order_decimal"]) == 3 ** len(q4col.orders) and
                 q4["nilpotency_class"] == 3,
                 "P3_Q4_COLLECTOR_ORDER_CLASS")
    qmarks = tuple(qcol.coord(row["coords"]) for row in q2["marked_generators"])
    qinverse_marks = tuple(qcol.coord(row["inverse_coords"])
                           for row in q2["marked_generators"])
    q4marks = tuple(q4col.coord(row["coords"])
                    for row in q4["marked_generators"])
    base.require(len(qmarks) == len(qinverse_marks) == 2 and len(q4marks) == 6,
                 "P3_MARK_COUNTS")
    install_positive_transition_backend(_ACTIVE_RECEIPT, q2, qcol,
                                        qmarks, qinverse_marks)
    coarse, _ = base.marked_bfs_map(
        qcol, qmarks, 0, (1, 1), lambda a, b: (a + b) % 3,
        lambda a: (-a) % 3, 2187)
    base.require(len(coarse) == 2187, "P3_MARKED_COARSE_COVER")
    return qmarks, q4marks


_ACTIVE_RECEIPT: dict[str, Any] = {}


def install(prime: int, out_dir: str | None) -> None:
    base.require(prime == 3, "P3_V5_PRIME_LOCAL", str(prime))
    v3.install(prime, out_dir)
    build_raw_v3 = base.build_raw_universe
    execute_v3 = base.execute
    build_manifest_v3 = base.build_manifest

    def source_pins(_: int) -> list[dict[str, Any]]:
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v3.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_p3_v5.py"),
            base.file_pin("search/d972_row36_pent_bridge_p3_producer_v5.py"),
        ]

    def paths_for(_: int) -> dict[str, str]:
        prefix = Path(out_dir).as_posix().rstrip("/") if out_dir else "search/certs"
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p3_prereg_v5_{base.DATE}.json",
            "receipt": f"{prefix}/d972_row36_pent_bridge_p3_receipt_v5_{base.DATE}.json",
            "manifest": f"{prefix}/d972_row36_pent_bridge_p3_manifest_v5_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt: dict[str, Any]):
        global _ACTIVE_RECEIPT
        _ACTIVE_RECEIPT = receipt
        base.validate_pc_receipt = validate_pc_receipt_v5
        prereg, runtime = build_raw_v3(prime_arg, receipt)
        gate = runtime["qcol"].p3_positive_transition_gate
        prereg["schema"] = "d972-row36-pent-bridge-p3-prereg/v5"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"]["p3_inverse_collection_stops"] = [
            {"version": "v3", "elapsed_seconds": 16.6,
             "exact_stop": "PC_COLLECTION_CAP: (25, 7)",
             "phase": "generic marked inverse expansion before Hall/L/Schreier"},
            {"version": "v4", "elapsed_seconds": 12.4,
             "exact_stop": "PC_COLLECTION_CAP: (16, 7)",
             "phase": "dense/positive marked multiplication in attempted inverse BFS"},
        ]
        prereg["execution_routing"]["p3_v5_positive_transition_repair"] = {
            key: gate[key] for key in (
                "algorithm", "state_order", "state_count",
                "positive_monoid_cover_count", "signed_word_replay_count",
                "projection_source", "predicate_fields_read_or_used",
                "projection_sha256", "Hall_model",
                "Hall_to_exported_coordinate_bijection",
                "marked_positive_inverse_match_exported",
                "exported_pc_relation_gate", "state_roster_sha256",
                "positive_transition_sha256", "inverse_transition_sha256",
                "generic_rank7_token_collector_used_after_install")
        }
        prereg["Q3_full_transition_freeze"] = gate
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = "PENT159O_ROW36_P3_PREREG_V5_FROZEN"
        return prereg, runtime

    def execute(prime_arg: int, prereg_pin: dict[str, Any], prereg: dict[str, Any],
                runtime: dict[str, Any], input_pins: list[dict[str, Any]]):
        receipt, extra = execute_v3(prime_arg, prereg_pin, prereg, runtime, input_pins)
        receipt["schema"] = "d972-row36-pent-bridge-p3-receipt/v5"
        receipt["source_pins"] = source_pins(prime_arg)
        receipt["Q3_positive_transition_backend"] = {
            key: runtime["qcol"].p3_positive_transition_gate[key]
            for key in ("algorithm", "state_count", "positive_monoid_cover_count",
                        "signed_word_replay_count", "projection_sha256",
                        "state_roster_sha256", "positive_transition_sha256",
                        "inverse_transition_sha256", "exported_pc_relation_gate")
        }
        receipt["terminal_token"] = \
            "PENT159O_ROW36_P3_PRODUCER_V5_CANDIDATE__CHECKER_REQUIRED"
        return receipt, extra

    def build_manifest(prime_arg: int, prereg_pin: dict[str, Any],
                       receipt_pin: dict[str, Any]):
        manifest = build_manifest_v3(prime_arg, prereg_pin, receipt_pin)
        manifest["schema"] = "d972-row36-pent-bridge-p3-manifest/v5"
        manifest["source_pins"] = source_pins(prime_arg)
        manifest["execution"]["local_command_prepare"] = \
            "python search/d972_row36_pent_bridge_p3_producer_v5.py prepare"
        manifest["execution"]["GHA_command"] = \
            "python3 search/d972_row36_pent_bridge_p3_producer_v5.py execute --out-dir ci/out"
        manifest["terminal_token"] = "PENT159O_ROW36_P3_MANIFEST_V5_FROZEN"
        return manifest

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw
    base.execute = execute
    base.build_manifest = build_manifest


def main_for_prime(prime: int) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "execute"))
    parser.add_argument("--out-dir")
    args = parser.parse_args()
    if args.phase == "prepare":
        base.require(args.out_dir is None, "PREPARE_OUT_DIR_FORBIDDEN")
    else:
        base.require(args.out_dir is not None, "EXECUTE_OUT_DIR_REQUIRED")
        rel = Path(args.out_dir)
        base.require(not rel.is_absolute() and ".." not in rel.parts,
                     "EXECUTE_OUT_DIR_UNSAFE", args.out_dir)
    install(prime, args.out_dir)
    raise SystemExit(base.run(prime, [args.phase]))
