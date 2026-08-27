"""Independent checker for the v2 normalized exact-common-word contract.

The checker duplicates the word and exponent primitives and deliberately does
not import the producer.  It validates receipts as data, with hard failures
for malformed programming state and typed UNKNOWN only for authenticated
input/resource boundaries.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_CHECKER = ROOT / "crosscheck/check_d972_r07_positive_common_word_colgen_v1.py"
LIVE_CHECKER_ID = (73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d")
NORMALIZED_SEMANTICS_DIGEST = hashlib.sha256(
    b"nu=(exp/18) mod 3|AllSevenModel.occurrence_data|AllSevenModel.occurrence_column|"
    b"AllSevenModel.direct_column|PositiveSearch.positive_receipt|Echelon target/basis membership|weighted formula scalar"
).hexdigest()
NORMALIZED_SEMANTICS_CALLSITES = [
    "AllSevenModel.occurrence_data", "AllSevenModel.occurrence_column",
    "AllSevenModel.direct_column", "PositiveSearch.positive_receipt",
    "Echelon target/basis membership", "weighted formula scalar"]

SCHEMA = "d972-r07-normalized-exact-common-word-colgen/v2"
SELFTEST_SCHEMA = "d972-r07-normalized-exact-common-word-colgen-selftest/v2"
COMMON = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
UNKNOWN_RESOURCE_CAPS = {"wall_seconds", "boundary_pairs", "fibre_scans",
                         "candidate_words", "retained_columns", "checkpoint_bytes",
                         "rss_bytes", "oracle_rounds", "global_roster"}
REGISTERED_RESOURCE_PHASE_CAPS = {
    ("task175_reconstruction", "wall_seconds"),
    ("task175_reconstruction", "rss_bytes"),
    ("fine_deletion", "wall_seconds"),
    ("fine_deletion", "rss_bytes"),
    ("Q0_discovery", "wall_seconds"),
    ("Q0_discovery", "rss_bytes"),
    ("A_L_membership_scan", "wall_seconds"),
    ("A_L_membership_scan", "rss_bytes"),
    ("L_subgroup_closure", "wall_seconds"),
    ("L_subgroup_closure", "rss_bytes"),
    ("typed_singleton_equality", "wall_seconds"),
    ("typed_singleton_equality", "rss_bytes"),
    ("Q0_positive_shortlex_section", "wall_seconds"),
    ("Q0_positive_shortlex_section", "rss_bytes"),
    ("coarse_inverse_build", "fibre_scans"),
    ("coarse_inverse_build", "wall_seconds"),
    ("coarse_inverse_build", "rss_bytes"),
    ("positive_boundary_correlation", "boundary_pairs"),
    ("positive_boundary_correlation", "wall_seconds"),
    ("positive_boundary_correlation", "rss_bytes"),
    ("rank_increase", "retained_columns"),
    ("rank_increase", "wall_seconds"),
    ("rank_increase", "rss_bytes"),
    ("positive_correction_candidate", "candidate_words"),
    ("positive_correction_candidate", "wall_seconds"),
    ("positive_correction_candidate", "rss_bytes"),
    ("weighted_eleven_occurrence_formula", "wall_seconds"),
    ("weighted_eleven_occurrence_formula", "rss_bytes"),
    ("weighted_support_fibre", "wall_seconds"),
    ("weighted_support_fibre", "rss_bytes"),
    ("weighted_global_prefix", "global_roster"),
    ("weighted_global_prefix", "wall_seconds"),
    ("weighted_global_prefix", "rss_bytes"),
    ("checkpoint_serialization", "checkpoint_bytes"),
    ("positive_global_fallback", "global_roster"),
    ("positive_correction_dovetail", "oracle_rounds"),
}
AUTHENTICATED_INPUT_REASON_PREFIXES = (
    "module_not_uniquely_pinned:", "module_missing:", "module_pin:",
    "module_loader:", "missing:", "pin:", "task175:not_READY",
    "resume:input_identity", "resume:target", "resume:normalized_semantics")
MUTATIONS = ("divisor_18", "exponent_sign", "roster_ordinal", "conjugator_exponent",
             "boundary_nonzero_tail", "raw_mod_3", "target_tail", "old_pivots",
             "coefficient_inverse", "divisibility_54", "u0_formula", "v0_formula",
             "cube_exponent", "right_correction_order", "pentagon_order", "hexagon",
             "source_word", "boundary_correction_word")
POSITIVE_GATES = ("joint_kernel_membership", "normalized_target_equality",
                  "zero_frattini_tail", "integer_exact_exponent",
                  "right_multiply_frozen_g760", "hexagon_1", "hexagon_2",
                  "five_factor_pentagon", "marked_reduction_side_gates",
                  "no_pb3_pb4_boundary_chain")
LIVE_V1 = {
    "producer": (123870, "47116826e1b94750fa5eaa0c577586aeaec23a476c5f004fc0d5ea83892845c7"),
    "checker": (73780, "de1d821c26cfc24c8069258ed1f19567358c86705dbc99103fff05a98d164c1d"),
    "driver": (12872, "48f95b79cfea29d54f539f25c649465599aac081d647e7ab87d851a2695aa97b"),
    "fixture": (407, "46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78"),
}
PROOF_PINS = {
    "v156": (10409, "2da7903829e6782eb434aad5a254b86f7fa86e8132fd1f0bccb7eb7fab3f4d7d"),
    "v157": (8367, "08e6d0e5fcac68400904c9844b19f1626c663f121a852a26f37a2d71a79a3ab8"),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def validate_outer_seal(value):
    claimed = value.get("self_digest")
    body = dict(value); body.pop("self_digest", None)
    if not isinstance(claimed, str) or claimed != digest(canonical(body)):
        raise RuntimeError("outer v2 receipt seal")


def reject_forbidden_claims(value):
    """The v2 envelope must not smuggle negative/fake/cofinal claims."""
    forbidden = {"negative_claim", "fake_claim", "fake_witness", "fake",
                 "cofinal_claim", "cofinal_lift", "cofinal", "ihara_claim",
                 "ihara_witness"}
    if isinstance(value, dict):
        for key, item in value.items():
            if key in forbidden and item not in (None, False, "", [], {}):
                raise RuntimeError("forbidden negative/fake/cofinal/Ihara claim")
            reject_forbidden_claims(item)
    elif isinstance(value, list):
        for item in value:
            reject_forbidden_claims(item)


def validate_resource_terminal(terminal):
    fields = terminal.split(":")
    if len(fields) != 5 or fields[0] != "UNKNOWN_RESOURCE":
        raise RuntimeError("malformed resource terminal")
    if not fields[1].startswith("phase=") or not fields[2].startswith("cap=") or \
            not fields[3].startswith("value=") or not fields[4].startswith("limit="):
        raise RuntimeError("resource terminal fields")
    phase, cap = fields[1][6:], fields[2][4:]
    if not phase or cap not in UNKNOWN_RESOURCE_CAPS or (phase, cap) not in REGISTERED_RESOURCE_PHASE_CAPS:
        raise RuntimeError("unregistered resource phase/cap")
    try:
        value, limit = float(fields[3][6:]), float(fields[4][6:])
    except ValueError as exc:
        raise RuntimeError("resource terminal numeric fields") from exc
    if not math.isfinite(value) or not math.isfinite(limit) or not value > limit:
        raise RuntimeError("resource terminal is not an exceeded registered cap")


def word(w):
    return tuple(int(x) for x in w)


def inv(w):
    return tuple(-x for x in reversed(word(w)))


def reduce_word(w):
    out = []
    for x in word(w):
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def mul(*ws):
    out = ()
    for w in ws:
        out = reduce_word(out + word(w))
    return out


def power(w, exponent_value):
    if exponent_value == 0:
        return ()
    base = w if exponent_value > 0 else inv(w)
    return mul(*([base] * abs(exponent_value)))


def exp(w):
    ans = [0, 0]
    for x in word(w):
        if abs(x) not in (1, 2):
            raise ValueError("invalid roster letter")
        ans[abs(x) - 1] += 1 if x > 0 else -1
    return tuple(ans)


def install_normalized_checker_semantics(checker):
    """Patch the helper's real exponent callsite before its full replay."""
    def normalized_pair(w):
        integer = exp(w)
        if integer[0] % 18 or integer[1] % 18:
            raise RuntimeError("helper normalized exponent divisibility")
        return ((integer[0] // 18) % 3, (integer[1] // 18) % 3)
    checker.exponent_pair = normalized_pair
    if checker.exponent_pair([1] * 18) != (1, 0):
        raise RuntimeError("helper exponent callsite remained raw-vacuous")
    return normalized_pair


def nu(w, divisor=18):
    e = exp(w)
    if any(x % divisor for x in e):
        raise RuntimeError("nonintegral normalized exponent")
    return tuple((x // divisor) % 3 for x in e)


def exactify(c_star, r3, r9, r12):
    e = exp(c_star)
    if any(x % 54 for x in e):
        raise RuntimeError("54-divisibility integrity failure")
    A, B = e[0] // 54, e[1] // 54
    v0 = mul(r9, r12, inv(r3) * 2)
    u0 = mul(r9, inv(v0) * 8)
    h = mul(power(u0, -3 * A), power(v0, -3 * B))
    c = mul(c_star, h)
    if exp(v0) != (0, 18) or exp(u0) != (18, 0) or exp(c) != (0, 0):
        raise RuntimeError("exactification basis/closure failure")
    return c, v0, u0, h


def sparse_rank(rows):
    pivots = {}
    for initial in rows:
        row = dict(initial)
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = 1 if row[pivot] == 1 else 2
                pivots[pivot] = {key: scale * value % 3 for key, value in row.items()}
                break
            base = pivots[pivot]
            scale = row[pivot]
            for key, value in base.items():
                row[key] = (row.get(key, 0) - scale * value) % 3
                if not row[key]:
                    row.pop(key)
    return len(pivots)


def sparse_digest(row):
    payload = bytearray()
    for key in sorted(row):
        payload.extend(len(key).to_bytes(4, "big")); payload.extend(key)
        payload.append(int(row[key]) % 3)
    return digest(bytes(payload))


def vector_rank(vectors):
    basis = {}
    for vector in vectors:
        row = [int(x) % 3 for x in vector]
        for pivot, base in sorted(basis.items()):
            if row[pivot]:
                scale = row[pivot] * (1 if base[pivot] == 1 else 2) % 3
                row = [(a - scale * b) % 3 for a, b in zip(row, base)]
        pivots = [i for i, value in enumerate(row) if value]
        if pivots:
            pivot = pivots[0]
            scale = 1 if row[pivot] == 1 else 2
            basis[pivot] = [(scale * value) % 3 for value in row]
    return len(basis)


def sparse_rows(receipt):
    rows = []
    for record in receipt.get("columns", []):
        rows.append({bytes.fromhex(str(item[0])): int(item[1]) % 3
                     for item in record.get("sparse_row", [])})
    return [{key: value for key, value in row.items() if not key.startswith(b"E")}
            for row in rows]


def ancestry(rows, nus):
    pivots, found = {}, []
    for index, initial in enumerate(rows, 1):
        row, coeff = dict(initial), {index: 1}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = 1 if row[pivot] == 1 else 2
                pivots[pivot] = ({key: scale * value % 3 for key, value in row.items()},
                                 {key: scale * value % 3 for key, value in coeff.items()})
                break
            base, base_coeff = pivots[pivot]
            scale = row[pivot]
            for key, value in base.items():
                row[key] = (row.get(key, 0) - scale * value) % 3
                if not row[key]: row.pop(key)
            for key, value in base_coeff.items():
                coeff[key] = (coeff.get(key, 0) - scale * value) % 3
                if not coeff[key]: coeff.pop(key)
        if not row and coeff:
            value = [0, 0]
            for column, scalar in coeff.items():
                value[0] = (value[0] + scalar * nus[column - 1][0]) % 3
                value[1] = (value[1] + scalar * nus[column - 1][1]) % 3
            if tuple(value) != (0, 0):
                found.append({"coefficients": [[key, scalar] for key, scalar in sorted(coeff.items())],
                              "nu": value})
    selected = []
    for candidate in found:
        if len(selected) < 2 and vector_rank([item["nu"] for item in selected] + [candidate["nu"]]) > len(selected):
            selected.append(candidate)
    return selected


def validate_roster_exponent_lattice(runtime):
    """Replay the authenticated 6,441-word integer exponent certificate."""
    roster = runtime["obj"].get("roster", [])
    if len(roster) != 6441:
        raise RuntimeError("independent roster cardinality")
    actual = {exp(record["word"]) for record in roster}
    expected = {(0, 0), (-36, 0), (36, 0), (-72, 0), (72, 0),
                (0, -36), (0, 36), (0, -54), (0, 54), (0, -72),
                (-36, -36), (-36, 36), (36, 36), (-72, 36),
                (-18, -54), (18, 144)}
    if actual != expected or len(actual) != 16:
        raise RuntimeError("registered 16-vector exponent set")
    if any(x % 18 or y % 18 for x, y in actual):
        raise RuntimeError("first inclusion exponent lattice")
    # The two registered defect words give the reverse inclusion generators.
    named = {record.get("ordinal"): exp(record["word"]) for record in roster
             if record.get("layer") == "q0_relator" and record.get("ordinal") in (3, 9, 12)}
    if named.get(3) != (0, 36) or named.get(9) != (18, 144) or named.get(12) != (-18, -54):
        raise RuntimeError("named kernel-word exponent vectors")
    v0 = (named[9][0] + named[12][0] - 2 * named[3][0],
          named[9][1] + named[12][1] - 2 * named[3][1])
    u0 = (named[9][0] - 8 * v0[0], named[9][1] - 8 * v0[1])
    if v0 != (0, 18) or u0 != (18, 0):
        raise RuntimeError("reverse inclusion 18Z2 generators")


def check_toy(receipt):
    if receipt.get("schema") != SELFTEST_SCHEMA or receipt.get("status") != "PASS":
        raise RuntimeError("bad selftest schema/status")
    expected = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_SELFTEST_PASS"
    if receipt.get("terminal") != expected:
        raise RuntimeError("bad selftest terminal")
    controls = receipt.get("mutation_controls", {})
    if controls.get("attempted") != 18 or controls.get("rejected") != 18:
        raise RuntimeError("mutation controls are not executed/rejected")
    if tuple(controls.get("names", ())) != MUTATIONS:
        raise RuntimeError("mutation list mismatch")
    base = {"divisor": 18, "sign": 1, "roster_ordinal": 3,
            "conjugator_exponent": 0, "boundary_tail": [0, 0], "raw_mod3": False,
            "target_tail": [0, 0], "old_pivots": False, "coefficient": 2,
            "divisible_54": True, "u0_formula": "r9*v0^-8", "v0_formula": "r9*r12*r3^-2",
            "cube": -3, "right_order": "base*correction", "pentagon": "printed",
            "hexagon_1": True, "hexagon_2": True, "source_word": [1] * 18,
            "boundary_inserted": False}
    live_checker = load_live_checker()
    live_original_pair = live_checker.exponent_pair
    install_normalized_checker_semantics(live_checker)
    toy_input = {"generators": [[1, 0, 2], [0, 2, 1]]}
    baseline_actual, _ = live_checker.independent_toy_column(
        toy_input, [], [1] * 18)
    def valid(state):
        # Drive the same independent occurrence, echelon, coefficient and
        # literal-word calculations as the producer SELFTEST.  Mutated
        # metadata never reaches a flag-only acceptance path.
        chosen = list(state["source_word"])
        if state["roster_ordinal"] != 3 and chosen == [1] * 18:
            chosen = [2] * 18
        chosen = [state["sign"] * letter for letter in chosen]
        delta = [2] * state["conjugator_exponent"]
        actual, occurrences = live_checker.independent_toy_column(
            toy_input, delta, chosen)
        actual_tail = [actual.get(live_checker.exponent_key(1), 0),
                       actual.get(live_checker.exponent_key(2), 0)]
        expected_tail = list(nu(chosen, state["divisor"]))
        if actual_tail != expected_tail:
            raise RuntimeError("actual helper normalized E-tail replay")
        if state["conjugator_exponent"] == 0 and state["roster_ordinal"] == 3:
            if actual != baseline_actual:
                raise RuntimeError("actual helper occurrence baseline replay")
        elif actual == baseline_actual:
            raise RuntimeError("actual helper mutation changed no occurrence")
        if len(occurrences) != 3 or [item["ordinal"] for item in occurrences] != [1, 2, 3]:
            raise RuntimeError("actual helper occurrence transcript")
        if state["divisor"] != 18 or state["sign"] != 1:
            raise RuntimeError("normalized divisor/sign replay")
        if state["roster_ordinal"] != 3 or state["conjugator_exponent"] != 0:
            raise RuntimeError("roster/conjugator provenance replay")
        if nu(chosen, state["divisor"]) != (1, 0):
            raise RuntimeError("normalized source membership replay")
        contains = lambda rows, target: vector_rank(rows) == vector_rank(rows + [target])
        normalized_row = list(nu(chosen))
        if not contains([normalized_row], [1, 0]):
            raise RuntimeError("normalized combined echelon membership")
        space = live_checker.RowSpace()
        if state["old_pivots"]:
            space.add({b"OLD-PIVOT": 1}, 99)
        pivot, origin = space.add(actual, 1)
        target = {key: (2 * value) % 3 for key, value in actual.items()
                  if (2 * value) % 3}
        if state["target_tail"] != [0, 0]:
            target[live_checker.exponent_key(2)] = 1
        remainder, solution = space.reduce(target)
        if remainder or solution.get(1) != 2 or len(space.pivots) != 1 or origin.get(1) != 1:
            raise RuntimeError("rank-zero coefficient/ancestry replay")
        if state["coefficient"] != solution[1]:
            raise RuntimeError("coefficient-two inverse replay")
        raw_column = {key: value for key, value in actual.items()
                      if not key.startswith(b"E")}
        raw_space = live_checker.RowSpace()
        if raw_column:
            raw_space.add(raw_column, 1)
        raw_remainder, _ = raw_space.reduce(target)
        if not raw_remainder or state["raw_mod3"]:
            raise RuntimeError("raw-vacuous membership substitution")
        if state["boundary_tail"] != [0, 0]:
            raise RuntimeError("boundary tail replay")
        r3, r9, r12 = [2] * 36, [1] * 18 + [2] * 144, [-1] * 18 + [-2] * 54
        c_star = mul([1] * 54 + [2] * 54,
                     [2] * 18 if state["boundary_inserted"] else [])
        closed = exactify(c_star, r3, r9, r12)
        if state["divisible_54"] is not True or exp(closed[0]) != (0, 0):
            raise RuntimeError("exact direct word replay")
        v0_replayed = mul(r9, r12, inv(r3) * 2)
        v0_state = (v0_replayed if state["v0_formula"] == "r9*r12*r3^-2"
                    else mul(r9, r12, power(r3, 2)))
        u0_state = (mul(r9, inv(v0_state) * 8)
                    if state["u0_formula"] == "r9*v0^-8"
                    else mul(r9, power(v0_state, 8)))
        e = exp(c_star)
        if e[0] % 54 or e[1] % 54:
            raise RuntimeError("exactification integer divisibility replay")
        a, b = e[0] // 54, e[1] // 54
        h_state = mul(power(u0_state, state["cube"] * a),
                      power(v0_state, state["cube"] * b))
        c_state = mul(c_star, h_state)
        if (v0_state != closed[1] or u0_state != closed[2] or
                state["u0_formula"] != "r9*v0^-8" or
                state["v0_formula"] != "r9*r12*r3^-2" or
                state["cube"] != -3 or exp(c_state) != (0, 0)):
            raise RuntimeError("exactification formula/direct replay")
        base_word = [1, 2]
        right_word = mul(base_word, c_state)
        candidate_right = (right_word if state["right_order"] == "base*correction"
                           else mul(c_state, base_word))
        if candidate_right != right_word or state["right_order"] != "base*correction":
            raise RuntimeError("right-correction order replay")
        factors = ([1], [2], [-1], [-2], [1, 2])
        printed = mul(factors[1], factors[3], factors[0], inv(factors[2]), inv(factors[4]))
        candidate_pentagon = (printed if state["pentagon"] == "printed" else
                              mul(factors[4], inv(factors[2]), factors[0], factors[3], factors[1]))
        if candidate_pentagon != printed or state["pentagon"] != "printed":
            raise RuntimeError("five-factor printed pentagon replay")
        hexagon_1 = mul([1], [2], [-1], [-2])
        hexagon_2 = mul([2], [1], [-2], [-1])
        if state["hexagon_1"] is not True or state["hexagon_2"] is not True or hexagon_1 == hexagon_2:
            raise RuntimeError("literal hexagon replay")
        if state["target_tail"] != [0, 0] or state["old_pivots"] or \
                state["source_word"] != [1] * 18 or state["boundary_inserted"]:
            raise RuntimeError("target/pivot/source boundary replay")
    fields = ("divisor", "sign", "roster_ordinal", "conjugator_exponent",
              "boundary_tail", "raw_mod3", "target_tail", "old_pivots", "coefficient",
              "divisible_54", "u0_formula", "v0_formula", "cube", "right_order",
              "pentagon", "hexagon_1", "source_word", "boundary_inserted")
    for name, field in zip(MUTATIONS, fields):
        state = copy.deepcopy(base)
        if field in ("boundary_tail", "target_tail"):
            state[field] = [1, 0]
        elif field == "source_word":
            state[field] = [2] * 18
        elif field in ("raw_mod3", "old_pivots", "divisible_54", "boundary_inserted",
                       "hexagon_1"):
            state[field] = not state[field]
        elif field == "coefficient":
            state[field] = 1
        elif field in ("divisor", "roster_ordinal", "conjugator_exponent", "cube"):
            state[field] += 1
        elif field == "sign":
            state[field] = -1
        elif field == "right_order":
            state[field] = "correction*base"
        elif field == "pentagon":
            state[field] = "reversed"
        elif field == "u0_formula":
            state[field] = "r9*v0^8"
        elif field == "v0_formula":
            state[field] = "r9*r12*r3^2"
        try:
            valid(state)
        except RuntimeError:
            pass
        else:
            raise RuntimeError("mutation accepted: " + name)
    toy = receipt.get("toy", {})
    if toy.get("kernel_lattice") != "18Z^2":
        raise RuntimeError("kernel lattice claim mismatch")
    if toy.get("raw_rows") != [[0, 0], [0, 0]]:
        raise RuntimeError("raw mod-3 substitution accepted")
    if toy.get("normalized_rows") != [[1, 0], [0, 1]]:
        raise RuntimeError("normalized rows mismatch")
    if toy.get("boundary_tail") != [0, 0]:
        raise RuntimeError("boundary tail is nonzero")
    if toy.get("membership") != {"raw_target_in_span": False,
                                  "normalized_target_in_span": True}:
        raise RuntimeError("raw/normalized membership distinction missing")
    regression = receipt.get("load_bearing_normalization", {})
    if regression.get("patched_v1_exponent_pair") is not True or \
            regression.get("integer_signed_counter") is not True or \
            regression.get("actual_E1_E2") != [1, 0] or \
            regression.get("raw_mod3_control") != [0, 0] or \
            regression.get("actual_occurrence_column") is not True:
        raise RuntimeError("load-bearing normalization regression absent")
    rank = toy.get("rank_audit", {})
    basis = rank.get("basis", [])
    preimages = rank.get("word_preimages", [])
    if (rank.get("rank_B_nu", 0) - rank.get("rank_B", 0) != rank.get("dim_nu_kernel_B") or
            len(basis) != rank.get("dim_nu_kernel_B") or vector_rank(basis) != len(basis) or
            len(preimages) != len(basis) or
            [list(nu(item)) for item in preimages] != basis):
        raise RuntimeError("normalized kernel-rank audit mismatch")
    production_trace = receipt.get("production_path_selftest", {})
    if production_trace.get("occurrence_direct_hook") is not True or \
            production_trace.get("actual_allseven_occurrence") is not True or \
            production_trace.get("actual_allseven_direct") is not True or \
            production_trace.get("normalized_E1") != 1 or \
            production_trace.get("raw_E1") != 0 or \
             production_trace.get("positive_add_column") is not True or \
             production_trace.get("rank_zero_checkpoint_rebuild") is not True or \
             production_trace.get("rank_zero_conversion") is not True or \
             production_trace.get("stored_pivots_discarded") is not True or \
            production_trace.get("coefficient_recovery") != [[1, 1]] or \
            production_trace.get("basis_ancestry") != [[1, 1]]:
        raise RuntimeError("load-bearing production SELFTEST trace absent")
    # Execute the independent normalized and noncommutative checks.
    for w, expected_nu in (([1] * 18, (1, 0)), ([2] * 18, (0, 1))):
        if tuple(x % 3 for x in exp(w)) != (0, 0) or nu(w) != expected_nu:
            raise RuntimeError("independent toy replay failed")
    if reduce_word((1, 2, -1, -2)) != (1, 2, -1, -2):
        raise RuntimeError("free reduction incorrectly commuted letters")
    r3, r9, r12 = [2] * 36, [1] * 18 + [2] * 144, [-1] * 18 + [-2] * 54
    _, v0, u0, h = exactify([1] * 54 + [2] * 54, r3, r9, r12)
    if exp(v0) != (0, 18) or exp(u0) != (18, 0) or exp(h) != (-54, -54):
        raise RuntimeError("independent exactification replay failed")
    task179 = receipt.get("task179_selftest")
    if not isinstance(task179, dict) or receipt.get("full_v1_schedule_selftest") is not True:
        raise RuntimeError("full task179 selftest receipt absent")
    checker = live_checker
    original_pair = live_original_pair
    if checker.exponent_pair([1] * 18) != (1, 0):
        raise RuntimeError("independent helper normalization regression")
    toy_input = {"generators": [[1, 0, 2], [0, 2, 1]]}
    normalized_row, _ = checker.independent_toy_column(toy_input, [], [1] * 18)
    if normalized_row.get(checker.exponent_key(1)) != 1:
        raise RuntimeError("independent helper occurrence E1 replay")
    checker.exponent_pair = original_pair
    raw_row, _ = checker.independent_toy_column(toy_input, [], [1] * 18)
    if checker.exponent_key(1) in raw_row or checker.exponent_key(2) in raw_row:
        raise RuntimeError("independent raw occurrence is not vacuous")
    row = {checker.exponent_key(1): 1}
    space = checker.RowSpace()
    pivot, origin = space.add(row, 1)
    remainder, solution = space.reduce(row)
    if pivot != checker.exponent_key(1) or origin != {1: 1} or remainder or solution != {1: 1}:
        raise RuntimeError("independent rank-zero/coefficient ancestry replay")
    checker.exponent_pair = original_pair
    checker.exponent_pair = original_pair
    with tempfile.TemporaryDirectory(prefix="d972-r07-check-selftest-") as temp:
        raw_path = Path(temp) / "task179-selftest.json"
        verdict = Path(temp) / "task179-selftest.verdict.json"
        raw_path.write_text(json.dumps(task179, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = checker.main(["--mode", "SELFTEST", "--receipt", str(raw_path),
                               "--verdict", str(verdict)])
        if rc != 0:
            raise RuntimeError("independent full task179 SELFTEST rejected")
    return "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS"


def check_production(receipt, helper=None):
    if receipt.get("schema") != SCHEMA:
        raise RuntimeError("bad production schema")
    validate_outer_seal(receipt)
    reject_forbidden_claims(receipt)
    terminal = receipt.get("terminal", "")
    if terminal == COMMON:
        if receipt.get("status") != "COMMON_WORD":
            raise RuntimeError("common terminal/status mismatch")
        checkpoint_ref = receipt.get("checkpoint")
        if checkpoint_ref is not None:
            cp_path = ROOT / "ci" / "out" / str(checkpoint_ref.get("path", ""))
            if not cp_path.is_file():
                raise RuntimeError("common v2 checkpoint missing")
            cp_raw = cp_path.read_bytes()
            if len(cp_raw) != checkpoint_ref.get("bytes") or digest(cp_raw) != checkpoint_ref.get("sha256"):
                raise RuntimeError("common v2 checkpoint identity")
            cp = json.loads(cp_raw.decode("utf-8")); validate_outer_seal(cp)
            if cp.get("schema") != SCHEMA or cp.get("normalized_semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                    cp.get("normalized_semantics_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
                raise RuntimeError("common v2 checkpoint semantic binding")
            if receipt.get("v2_schedule", {}).get("resume_replayed_from_rank_zero"):
                rebuild = cp.get("resume_rebuild", {})
                if rebuild.get("rank_zero_replayed") is not True or \
                        rebuild.get("stored_pivots_discarded") is not True or \
                        rebuild.get("stored_reduced_target_discarded") is not True or \
                        rebuild.get("stored_current_dual_discarded") is not True or \
                        rebuild.get("stored_oracle_progress_discarded") is not True or \
                        rebuild.get("stored_state_fields_discarded") != [
                            "pivot_order", "pivot_rows_sha256", "reduced_target",
                            "current_dual", "current_dual_sha256",
                            "target_solution_if_zero", "progress", "monitor",
                            "coarse_inverse_index", "resume_rebuild"] or \
                        rebuild.get("column_provenance_authenticated") is not True or \
                        rebuild.get("stored_columns_replayed_from_zero") is not True or \
                        rebuild.get("rank_zero_replay_source") !=
                        "authenticated columns/provenance":
                    raise RuntimeError("resume checkpoint retained stale state")
        ncols = receipt.get("normalized_columns")
        if not isinstance(ncols, list) or not ncols:
            raise RuntimeError("normalized columns absent")
        for column in ncols:
            if column.get("nu") is None or column.get("boundary_zero_tail") not in (True, False):
                raise RuntimeError("normalized column provenance")
            source = column.get("source_word", [])
            if column.get("nu") != list(nu(source)):
                raise RuntimeError("normalized column recomputation")
            if column.get("boundary_zero_tail") and source:
                raise RuntimeError("boundary carries a source word")
        if receipt.get("normalized_exponent_contract", {}).get("integer_gate") is not True:
            raise RuntimeError("normalized exponent gate absent")
        audit = receipt.get("rank_audit", {})
        raw_records = receipt.get("columns", [])
        if len(raw_records) != len(ncols):
            raise RuntimeError("normalized/raw column count mismatch")
        b_rows = sparse_rows(receipt)
        rank_b = sparse_rank(b_rows)
        # These are the authenticated helper's actual v1 exponent keys; the
        # v2 layer must not invent a parallel V2-NU namespace.
        exponent_key = helper.exponent_key if helper is not None else (
            lambda index: b"E" + bytes((index,)))
        ekeys = (exponent_key(1), exponent_key(2))
        if ekeys != (b"E\x01", b"E\x02"):
            raise RuntimeError("helper exponent-key contract")
        for record, column in zip(raw_records, ncols):
            raw = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                   for item in record.get("sparse_row", [])}
            actual = [raw.get(ekeys[0], 0), raw.get(ekeys[1], 0)]
            if actual != column.get("nu"):
                raise RuntimeError("receipt E1/E2 tail is not normalized nu")
            if column.get("boundary_zero_tail") and actual != [0, 0]:
                raise RuntimeError("boundary E tail is nonzero")
        augmented = []
        for row, column in zip(b_rows, ncols):
            row = dict(row)
            if column["nu"][0]:
                row[ekeys[0]] = column["nu"][0]
            if column["nu"][1]:
                row[ekeys[1]] = column["nu"][1]
            augmented.append(row)
        rank_nu = sparse_rank(augmented)
        if audit.get("rank_B") != rank_b or audit.get("rank_B_nu") != rank_nu or \
                rank_nu - rank_b != audit.get("dim_nu_kernel_B"):
            raise RuntimeError("rank(B,nu) identity")
        echelon = receipt.get("normalized_echelon", {})
        if echelon.get("restarted_from_rank") != 0 or \
                echelon.get("rank") != rank_nu or \
                echelon.get("actual_combined_rank") != rank_nu or \
                echelon.get("actual_combined_pivot_count") != rank_nu or \
                echelon.get("basis_pivot_count") != len(receipt.get("columns", [])):
            raise RuntimeError("combined normalized echelon audit")
        if echelon.get("normalized_tails") != [column.get("nu") for column in ncols]:
            raise RuntimeError("normalized retained tail transcript")
        expected_digests = []
        for record in receipt.get("columns", []):
            raw = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                   for item in record.get("sparse_row", [])}
            expected_digests.append(sparse_digest(raw))
        if echelon.get("combined_row_digests") != expected_digests:
            raise RuntimeError("combined retained row transcript")
        if receipt.get("normalized_basis_rebuilt_from_rank_zero") is not True or \
                len(audit.get("basis", [])) != audit.get("dim_nu_kernel_B") or \
                len(audit.get("word_preimages", [])) != audit.get("dim_nu_kernel_B"):
            raise RuntimeError("normalized basis provenance")
        contract = receipt.get("normalized_exponent_contract", {})
        if contract.get("semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                contract.get("patched_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
            raise RuntimeError("normalized semantics digest")
        computed_ancestry = ancestry(b_rows, [column["nu"] for column in ncols])
        recorded_ancestry = receipt.get("nu_kernel_ancestry", [])
        if [item.get("coefficients") for item in recorded_ancestry] != [
                item["coefficients"] for item in computed_ancestry]:
            raise RuntimeError("kernel coefficient ancestry mismatch")
        if audit.get("basis") != [item["nu"] for item in computed_ancestry] or \
                audit.get("word_preimages") != [item.get("correction_word_replay", [])
                                                  for item in recorded_ancestry]:
            raise RuntimeError("independent nu-kernel basis provenance")
        if echelon.get("basis_words") != audit.get("word_preimages"):
            raise RuntimeError("normalized echelon basis-word transcript")
        for item in recorded_ancestry:
            if item.get("B_zero_recomputed") is not True:
                raise RuntimeError("kernel B-zero was asserted")
            expected_boundary = []
            expected_correction = []
            correction_word = ()
            for column, coefficient in item.get("coefficients", []):
                if ncols[column - 1].get("boundary_zero_tail"):
                    expected_boundary.append([column, coefficient])
                else:
                    expected_correction.append([column, coefficient])
                    source_word = ncols[column - 1].get("source_word", [])
                    correction_word = mul(
                        correction_word,
                        source_word if coefficient == 1 else inv(source_word))
            if item.get("boundary_coefficients") != expected_boundary or \
                    item.get("correction_coefficients") != expected_correction or \
                    item.get("correction_word_replay") != list(correction_word) or \
                    item.get("recomputed_nu") != list(nu(correction_word)):
                raise RuntimeError("kernel source/coefficient provenance replay")
            zero = {}
            for column, coefficient in item.get("coefficients", []):
                for key, value in b_rows[column - 1].items():
                    value0 = (zero.get(key, 0) + coefficient * value) % 3
                    if value0: zero[key] = value0
                    elif key in zero: zero.pop(key)
            if zero or item.get("B_zero_row") != [] or item.get("B_zero_sha256") != sparse_digest(zero):
                raise RuntimeError("kernel B-zero replay mismatch")
            direct_replay = item.get("direct_correction_replay", {})
            source = item.get("correction_word_replay", [])
            if direct_replay.get("corrected_word") != reduce_word(
                    (receipt.get("g760") or []) + source):
                raise RuntimeError("kernel correction direct replay mismatch")
            if item.get("correction_boundary_zero_sha256") != sparse_digest({}):
                raise RuntimeError("kernel correction-boundary zero digest")
        ex = receipt.get("exactification", {})
        if ex.get("positive_receipt") is not True or set(ex.get("r_words", {})) != {"3", "9", "12"}:
            raise RuntimeError("exactification provenance absent")
        factors = ex.get("factor_sources", {})
        if factors.get("correction_conjugates_only") is not True or \
                factors.get("registered_cubes") != ["r3", "r9", "r12"] or \
                factors.get("boundary_words_included") is not False:
            raise RuntimeError("exactification factor provenance")
        if ex.get("joint_kernel_replay") != {"r3": True, "r9": True, "r12": True,
                                              "u0": True, "v0": True}:
            raise RuntimeError("registered joint-kernel replay evidence absent")
        words = ex["r_words"]
        cstar = receipt.get("correction_word") or []
        closed = exactify(cstar, words["3"], words["9"], words["12"])
        if ex.get("exponents", {}).get("c_exact") != list(exp(closed[0])):
            raise RuntimeError("exactification replay digest/value")
        if receipt.get("boundary_words_not_inserted") is not True:
            raise RuntimeError("boundary correction contamination")
        direct = receipt.get("exact_direct_replay", {})
        if direct.get("joint_kernel") is not True or direct.get("right_g760_multiplication") is not True or \
                direct.get("hexagons") is not True or direct.get("pentagon_printed_order") is not True:
            raise RuntimeError("exact direct replay gates absent")
        literal = ex.get("literal", {})
        exact_word = literal.get("c_exact", [])
        replay = direct.get("replay", {})
        if direct.get("row") != direct.get("star_row"):
            raise RuntimeError("exact direct row differs from c_star row")
        parsed_direct = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                         for item in direct.get("row", [])}
        parsed_star = {bytes.fromhex(str(item[0])): int(item[1]) % 3
                       for item in direct.get("star_row", [])}
        if direct.get("row_sha256") != sparse_digest(parsed_direct) or \
                direct.get("star_row_sha256") != sparse_digest(parsed_star):
            raise RuntimeError("exact direct row digest mismatch")
        if any(bytes.fromhex(str(item[0])).startswith(b"E") for item in direct.get("row", [])):
            raise RuntimeError("exact direct row has normalized tail")
        if replay.get("corrected_word") != reduce_word((receipt.get("g760") or []) + exact_word):
            raise RuntimeError("exact right multiplication replay mismatch")
        if exp(exact_word) != (0, 0):
            raise RuntimeError("exact word integer exponent replay mismatch")
    elif receipt.get("status") == "UNKNOWN" and terminal.startswith((UNKNOWN_INPUT + ":", "UNKNOWN_RESOURCE:")):
        checkpoint = receipt.get("checkpoint")
        if terminal.startswith("UNKNOWN_RESOURCE:"):
            validate_resource_terminal(terminal)
            cap = terminal.split(":")[2][4:]
            limit = float(terminal.split(":")[4][6:])
            monitor = receipt.get("monitor")
            registered_limits = monitor.get("limits", {}) if isinstance(monitor, dict) else {}
            if cap not in registered_limits or limit != float(registered_limits[cap]):
                raise RuntimeError("resource receipt limit is not registered")
            if not checkpoint or not checkpoint.get("path"):
                raise RuntimeError("resource stop lacks resumable checkpoint")
            path = ROOT / "ci" / "out" / str(checkpoint["path"])
            if not path.is_file():
                raise RuntimeError("resource checkpoint file missing")
            raw = path.read_bytes()
            if len(raw) != checkpoint.get("bytes") or digest(raw) != checkpoint.get("sha256"):
                raise RuntimeError("resource checkpoint identity")
            value = json.loads(raw.decode("utf-8"))
            validate_outer_seal(value)
            if value.get("schema") != SCHEMA or value.get("normalized_semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                    value.get("normalized_semantics_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
                raise RuntimeError("resource checkpoint semantic binding")
            if receipt.get("v2_schedule", {}).get("resume_replayed_from_rank_zero"):
                rebuild = value.get("resume_rebuild", {})
                if rebuild.get("rank_zero_replayed") is not True or \
                        rebuild.get("stored_pivots_discarded") is not True or \
                        rebuild.get("stored_reduced_target_discarded") is not True or \
                        rebuild.get("stored_current_dual_discarded") is not True or \
                        rebuild.get("stored_oracle_progress_discarded") is not True or \
                        rebuild.get("stored_state_fields_discarded") != [
                            "pivot_order", "pivot_rows_sha256", "reduced_target",
                            "current_dual", "current_dual_sha256",
                            "target_solution_if_zero", "progress", "monitor",
                            "coarse_inverse_index", "resume_rebuild"] or \
                        rebuild.get("column_provenance_authenticated") is not True or \
                        rebuild.get("stored_columns_replayed_from_zero") is not True or \
                        rebuild.get("rank_zero_replay_source") !=
                        "authenticated columns/provenance":
                    raise RuntimeError("resource resume checkpoint retained stale state")
        else:
            reason = terminal[len(UNKNOWN_INPUT) + 1:]
            if not reason or not any(reason.startswith(prefix)
                                     for prefix in AUTHENTICATED_INPUT_REASON_PREFIXES) or \
                    receipt.get("reason") != reason:
                raise RuntimeError("unauthenticated input UNKNOWN reason")
    else:
        raise RuntimeError("unexpected production terminal")
    return "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_CHECKER_PASS terminal=" + terminal


def load_live_checker():
    data = LIVE_CHECKER.read_bytes()
    if len(data) != LIVE_CHECKER_ID[0] or digest(data) != LIVE_CHECKER_ID[1]:
        raise RuntimeError("authenticated live checker changed")
    spec = importlib.util.spec_from_file_location("d972_live_task179_checker_v2", LIVE_CHECKER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load authenticated live checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def full_independent_production(receipt, receipt_path):
    """Run the complete helper-nonshared v1 replay, then v2-only checks."""
    checker = load_live_checker()
    # The helper also exposes v1's raw mod-3 exponent_pair.  Patch its own
    # runtime before main(), independently of the producer patch.
    install_normalized_checker_semantics(checker)
    with tempfile.TemporaryDirectory(prefix="d972-r07-check-v2-") as temp:
        raw_path = Path(temp) / "v1-receipt.json"
        raw = dict(receipt)
        raw["schema"] = checker.SCHEMA
        if raw.get("terminal") == COMMON:
            raw["terminal"] = checker.COMMON
        checkpoint_ref = receipt.get("checkpoint")
        if checkpoint_ref and checkpoint_ref.get("path"):
            v2_checkpoint_path = receipt_path.parent / str(checkpoint_ref["path"])
            if not v2_checkpoint_path.is_file():
                raise RuntimeError("authenticated v2 checkpoint sidecar missing")
            v2_checkpoint_raw = v2_checkpoint_path.read_bytes()
            if len(v2_checkpoint_raw) != checkpoint_ref.get("bytes") or \
                    digest(v2_checkpoint_raw) != checkpoint_ref.get("sha256"):
                raise RuntimeError("authenticated v2 checkpoint sidecar identity")
            v2_checkpoint = json.loads(v2_checkpoint_raw.decode("utf-8"))
            validate_outer_seal(v2_checkpoint)
            if v2_checkpoint.get("schema") != SCHEMA or \
                    v2_checkpoint.get("normalized_semantics_digest") != NORMALIZED_SEMANTICS_DIGEST or \
                    v2_checkpoint.get("normalized_semantics_callsites") != list(NORMALIZED_SEMANTICS_CALLSITES):
                raise RuntimeError("authenticated v2 checkpoint semantics")
            # The helper firewall consumes the complete v1 checkpoint object,
            # while the outer receipt keeps the v2 path/bytes/SHA metadata.
            v1_checkpoint = dict(v2_checkpoint)
            v1_checkpoint["schema"] = checker.CHECKPOINT_SCHEMA
            v1_checkpoint.pop("normalized_semantics", None)
            v1_checkpoint.pop("normalized_semantics_digest", None)
            v1_checkpoint.pop("normalized_semantics_callsites", None)
            v1_checkpoint = checker.seal(v1_checkpoint)
            if raw.get("terminal") == checker.COMMON:
                raw["checkpoint"] = v1_checkpoint
            else:
                v1_checkpoint_path = Path(temp) / "v1-checkpoint.json"
                v1_checkpoint_path.write_bytes(checker.canonical(v1_checkpoint) + b"\n")
                raw["checkpoint"] = {"path": v1_checkpoint_path.name,
                                     "bytes": v1_checkpoint_path.stat().st_size,
                                     "sha256": digest(v1_checkpoint_path.read_bytes())}
        raw.pop("self_digest", None)
        raw = checker.seal(raw)
        raw_path.write_text(json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
        expected_pins = {name: value for name, value in checker.authenticate().items()
                         if name != "producer"}
        helper_runtime = checker.independent_runtime() if (
            raw.get("terminal") == checker.COMMON or raw.get("checkpoint") is not None) else None
        if raw.get("terminal") == checker.COMMON:
            validate_roster_exponent_lattice(helper_runtime)
            selected_rwords = {}
            for ordinal in (3, 9, 12):
                matches = [record["word"] for record in helper_runtime["obj"]["roster"]
                           if record.get("layer") == "q0_relator" and
                           record.get("ordinal") == ordinal]
                if len(matches) != 1:
                    raise RuntimeError("independent registered r ordinal")
                selected_rwords[str(ordinal)] = list(matches[0])
            receipt_rwords = receipt.get("exactification", {}).get("r_words", {})
            if receipt_rwords != selected_rwords:
                raise RuntimeError("receipt r words are not independently selected")
            cstar = receipt.get("correction_word") or []
            reconstructed_cstar = ()
            for column, coefficient in receipt.get("solution_coefficients", []):
                if type(column) is not int or type(coefficient) is not int or \
                        coefficient not in (1, 2) or not (1 <= column <= len(receipt.get("columns", []))):
                    raise RuntimeError("independent coefficient is not F3 nonzero")
                record = receipt.get("columns", [])[column - 1]
                if record.get("family") == "boundary":
                    raise RuntimeError("boundary factor in reconstructed c_star")
                source = record.get("provenance", {}).get("conjugate_word", [])
                reconstructed_cstar = mul(
                    reconstructed_cstar,
                    source if coefficient == 1 else inv(source))
            if list(reconstructed_cstar) != cstar:
                raise RuntimeError("independent c_star coefficient replay")
            closed = exactify(cstar, selected_rwords["3"], selected_rwords["9"],
                              selected_rwords["12"])
            literals = receipt.get("exactification", {}).get("literal", {})
            expected_literals = {"c_star": list(cstar), "v0": list(closed[1]),
                                 "u0": list(closed[2]), "h": list(closed[3]),
                                 "c_exact": list(closed[0])}
            if literals != expected_literals:
                raise RuntimeError("receipt exactification literals mismatch")
            cstar_exp = exp(cstar)
            if any(value % 54 for value in cstar_exp):
                raise RuntimeError("independent c_star 54-divisibility")
            expected_exponents = {
                "c_star": list(cstar_exp), "v0": list(exp(closed[1])),
                "u0": list(exp(closed[2])), "h": list(exp(closed[3])),
                "c_exact": list(exp(closed[0]))}
            exactification = receipt.get("exactification", {})
            if exactification.get("A") != cstar_exp[0] // 54 or \
                    exactification.get("B") != cstar_exp[1] // 54 or \
                    exactification.get("exponents") != expected_exponents or \
                    exactification.get("source") != "authenticated task179 roster ordinals":
                raise RuntimeError("receipt exactification exponent/provenance mismatch")
        if raw.get("terminal") == checker.COMMON:
            checker.validate_common(helper_runtime, raw, expected_pins)
        else:
            checker.validate_unknown(helper_runtime, raw, expected_pins, raw_path)
        if receipt.get("terminal") == COMMON:
            # Re-run the helper's independently coded direct-correction
            # primitive on c_exact; receipt booleans are not evidence.
            # Replay the independently reconstructed literals, not the
            # receipt's copies (the equality gate above is separate).
            exact_word = list(closed[0])
            star_word = list(cstar)
            star_row, star_replay = checker.direct_correction(helper_runtime, [], star_word)
            direct_row, direct_replay = checker.direct_correction(helper_runtime, [], exact_word)
            expected_row = checker.parse_sparse(receipt.get("exact_direct_replay", {}).get("row", []))
            if checker.public_sparse(direct_row) != checker.public_sparse(expected_row) or \
                    checker.public_sparse(star_row) != checker.public_sparse(direct_row):
                raise RuntimeError("helper direct c_exact row mismatch")
            if direct_replay.get("corrected_word") != receipt.get("exact_direct_replay", {}).get(
                    "replay", {}).get("corrected_word"):
                raise RuntimeError("helper direct c_exact word mismatch")
            for label, literal in receipt.get("exactification", {}).get("r_words", {}).items():
                if helper_runtime["obj"]["joint"].eval(literal) != helper_runtime["obj"]["joint"].identity:
                    raise RuntimeError("helper registered r-word kernel replay:" + label)
            for label in ("u0", "v0"):
                literal = receipt.get("exactification", {}).get("literal", {}).get(label, [])
                if helper_runtime["obj"]["joint"].eval(literal) != helper_runtime["obj"]["joint"].identity:
                    raise RuntimeError("helper exactification basis kernel replay:" + label)
            raw_rows = []
            for record in receipt.get("columns", []):
                raw_rows.append(checker.parse_sparse(record.get("sparse_row", [])))
            for witness in receipt.get("nu_kernel_ancestry", []):
                source = witness.get("correction_word_replay", [])
                replay_row, replay_info = checker.direct_correction(helper_runtime, [], source)
                boundary_sum = {}
                for column, coefficient in witness.get("boundary_coefficients", []):
                    for key, value in raw_rows[column - 1].items():
                        if key.startswith(b"E"):
                            continue
                        value0 = (boundary_sum.get(key, 0) + coefficient * value) % 3
                        if value0:
                            boundary_sum[key] = value0
                        elif key in boundary_sum:
                            boundary_sum.pop(key)
                for key, value in replay_row.items():
                    if key.startswith(b"E"):
                        continue
                    value0 = (boundary_sum.get(key, 0) + value) % 3
                    if value0:
                        boundary_sum[key] = value0
                    elif key in boundary_sum:
                        boundary_sum.pop(key)
                if boundary_sum or replay_info.get("corrected_word") != checker.reduce_word(
                        list(helper_runtime["obj"]["g760"]) + source):
                    raise RuntimeError("helper ancestry correction/boundary replay")
    return check_production(receipt, checker)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    receipt_path = Path(args.receipt)
    if not receipt_path.is_absolute():
        receipt_path = ROOT / receipt_path
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    marker = (check_toy(receipt) if args.selftest else
              full_independent_production(receipt, receipt_path))
    print(marker)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
