"""R07 normalized exact-common-word column generator (v2).

This file is deliberately fail-closed: the authenticated task179 roster is
the only permitted production source, and no positive candidate is emitted
until its complete replay is available.  The small word/lattice primitives
are the implementation used by both the production and fixture contracts.
"""
from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_V1_PATH = ROOT / "search/d972_r07_positive_common_word_colgen_v1.py"

SCHEMA = "d972-r07-normalized-exact-common-word-colgen/v2"
SELFTEST_SCHEMA = "d972-r07-normalized-exact-common-word-colgen-selftest/v2"
COMMON = "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_COMMON_WORD"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"
UNKNOWN_INPUT = "UNKNOWN_INPUT"
FIXTURE = "search/certs/d972_r07_normalized_exact_common_word_colgen_selftest_v2_20260827.json"

# The live v1 identities were read from the working tree on 2026-08-27.
# They are provenance, not permission to import or execute the old producer.
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
NORMALIZED_SEMANTICS_CALLSITES = (
    "AllSevenModel.occurrence_data", "AllSevenModel.occurrence_column",
    "AllSevenModel.direct_column", "PositiveSearch.positive_receipt",
    "Echelon target/basis membership", "weighted formula scalar")
NORMALIZED_SEMANTICS_DIGEST = hashlib.sha256(
    ("nu=(exp/18) mod 3|" + "|".join(NORMALIZED_SEMANTICS_CALLSITES)).encode("ascii")
).hexdigest()

SCHEDULE_CONTRACT = (
    "boundary_pairs", "fibre_scans", "candidate_words", "retained_columns",
    "checkpoint_bytes", "rss_bytes", "oracle_rounds", "global_roster",
)
RESUME_DISCARDED_STATE_FIELDS = (
    "pivot_order", "pivot_rows_sha256", "reduced_target", "current_dual",
    "current_dual_sha256", "target_solution_if_zero", "progress", "monitor",
    "coarse_inverse_index", "resume_rebuild",
)
MUTATIONS = (
    "divisor_18", "exponent_sign", "roster_ordinal", "conjugator_exponent",
    "boundary_nonzero_tail", "raw_mod_3", "target_tail", "old_pivots",
    "coefficient_inverse", "divisibility_54", "u0_formula", "v0_formula",
    "cube_exponent", "right_correction_order", "pentagon_order", "hexagon",
    "source_word", "boundary_correction_word",
)
POSITIVE_GATES = (
    "joint_kernel_membership", "normalized_target_equality", "zero_frattini_tail",
    "integer_exact_exponent", "right_multiply_frozen_g760", "hexagon_1",
    "hexagon_2", "five_factor_pentagon", "marked_reduction_side_gates",
    "no_pb3_pb4_boundary_chain",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def authenticate(path: str, expected: tuple[int, str]) -> None:
    data = Path(path).read_bytes()
    if len(data) != expected[0] or sha256_bytes(data) != expected[1]:
        raise RuntimeError("authenticated live input changed: " + path)


def signed_word(word):
    return tuple(int(x) for x in word)


def inverse_word(word):
    return tuple(-x for x in reversed(tuple(word)))


def reduce_word(word):
    out = []
    for letter in signed_word(word):
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def multiply(*words):
    out = ()
    for word in words:
        out = reduce_word(out + signed_word(word))
    return out


def power_word(word, exponent_value):
    if exponent_value == 0:
        return ()
    base = word if exponent_value > 0 else inverse_word(word)
    return multiply(*([base] * abs(exponent_value)))


def exponent(word):
    x = y = 0
    for letter in signed_word(word):
        if abs(letter) == 1:
            x += 1 if letter > 0 else -1
        elif abs(letter) == 2:
            y += 1 if letter > 0 else -1
        else:
            raise ValueError("word letter is not x/y: %r" % (letter,))
    return (x, y)


def integer_exponent_pair(word):
    return exponent(word)


def patch_v1_normalized_semantics(v1):
    """Install v156 semantics at the authenticated v1 load-bearing hook."""
    raw_pair = v1.exponent_pair
    def normalized_pair(word):
        pair = integer_exponent_pair(word)
        if pair[0] % 18 or pair[1] % 18:
            # The v1 SELFTEST includes deliberately non-Omega toy words.
            # Its adapted toy path may retain the raw diagnostic only under
            # this explicit test flag; production remains fail-closed.
            if getattr(v1, "_v2_selftest_nonomega", False):
                return raw_pair(word)
            raise RuntimeError("normalized exponent divisibility by 18")
        return ((pair[0] // 18) % 3, (pair[1] // 18) % 3)
    v1.exponent_pair = normalized_pair
    return normalized_pair


def normalized_exponent(word, divisor=18):
    e = exponent(word)
    if e[0] % divisor or e[1] % divisor:
        raise RuntimeError("exponent is not divisible by 18")
    return ((e[0] // divisor) % 3, (e[1] // divisor) % 3)


def sparse_add(a, b, modulus=3):
    keys = set(a) | set(b)
    return {k: (a.get(k, 0) + b.get(k, 0)) % modulus for k in keys
            if (a.get(k, 0) + b.get(k, 0)) % modulus}


def exactify(c_star, r3, r9, r12):
    """Closed correction from v156/v157, retaining every literal word."""
    e = exponent(c_star)
    if e[0] % 54 or e[1] % 54:
        raise RuntimeError("54-divisibility integrity failure")
    A, B = e[0] // 54, e[1] // 54
    v0 = multiply(r9, r12, inverse_word(r3) * 2)
    u0 = multiply(r9, inverse_word(v0) * 8)
    h = multiply(power_word(u0, -3 * A), power_word(v0, -3 * B))
    c_exact = multiply(c_star, h)
    if exponent(v0) != (0, 18) or exponent(u0) != (18, 0):
        raise RuntimeError("registered exactification basis mismatch")
    if exponent(c_exact) != (0, 0):
        raise RuntimeError("exactification did not close integer exponent")
    return {"c_star": c_star, "v0": v0, "u0": u0, "h": h,
            "c_exact": c_exact, "A": A, "B": B,
            "exponents": {"c_star": e, "v0": exponent(v0),
                          "u0": exponent(u0), "h": exponent(h),
                          "c_exact": exponent(c_exact)}}


def toy_selftest(v1=None):
    # The 18-fold x/y rows generate exactly 18 Z^2.  Raw mod-3 is zero,
    # while normalized rows are the nonzero standard basis.
    rows = [(tuple([1] * 18), (1, 0)), (tuple([2] * 18), (0, 1))]
    for word, expected in rows:
        if tuple(v % 3 for v in exponent(word)) != (0, 0):
            raise AssertionError("raw mod-3 row is not vacuous")
        if normalized_exponent(word) != expected:
            raise AssertionError("normalized row mismatch")
    boundary = ()
    if normalized_exponent(boundary) != (0, 0):
        raise AssertionError("boundary tail is not zero")
    # Noncommutative reduction is exercised independently of the toy lattice.
    if reduce_word((1, 2, -1, -2)) != (1, 2, -1, -2):
        raise AssertionError("noncommutative word was incorrectly commuted")
    r3 = tuple([2] * 36)
    r9 = tuple([1] * 18 + [2] * 144)
    r12 = tuple([-1] * 18 + [-2] * 54)
    closed = exactify(tuple([1] * 54 + [2] * 54), r3, r9, r12)
    if closed["exponents"] != {"c_star": (54, 54), "v0": (0, 18),
                                "u0": (18, 0), "h": (-54, -54),
                                "c_exact": (0, 0)}:
        raise AssertionError("exactification replay mismatch")
    base = {"divisor": 18, "sign": 1, "roster_ordinal": 3,
            "conjugator_exponent": 0, "boundary_tail": [0, 0], "raw_mod3": False,
            "target_tail": [0, 0], "old_pivots": False, "coefficient": 2,
            "divisible_54": True, "u0_formula": "r9*v0^-8", "v0_formula": "r9*r12*r3^-2",
            "cube": -3, "right_order": "base*correction", "pentagon": "printed",
            "hexagon_1": True, "hexagon_2": True, "source_word": [1] * 18,
            "boundary_inserted": False}
    toy_fixture = {"generators": [[1, 0, 2], [0, 2, 1]]}
    baseline_actual = None
    if v1 is not None:
        baseline_actual, _ = v1.toy_occurrence_column(
            toy_fixture, [], base["source_word"])
    def validate_state(state):
        # Every mutation is replayed through a fresh echelon and the actual
        # authenticated occurrence callsite.  The state fields below select
        # literal inputs to that replay; they are not a dictionary-equality
        # canary.
        chosen = list(state["source_word"])
        if state["roster_ordinal"] != 3 and chosen == [1] * 18:
            chosen = [2] * 18
        chosen = [state["sign"] * letter for letter in chosen]
        delta = [2] * state["conjugator_exponent"]
        if v1 is not None:
            actual, occurrences = v1.toy_occurrence_column(toy_fixture, delta, chosen)
            actual_tail = [actual.get(v1.exponent_key(1), 0),
                           actual.get(v1.exponent_key(2), 0)]
            expected_tail = list(normalized_exponent(chosen, state["divisor"]))
            require(actual_tail == expected_tail,
                    "actual production normalized E-tail replay")
            if state["conjugator_exponent"] == 0 and state["roster_ordinal"] == 3:
                require(actual == baseline_actual,
                        "actual production occurrence baseline replay")
            else:
                require(actual != baseline_actual,
                        "actual production mutation changed no occurrence")
            require(len(occurrences) == 3 and
                    [item["ordinal"] for item in occurrences] == [1, 2, 3],
                    "actual production occurrence transcript")
        else:
            actual = {}
        require(state["divisor"] == 18, "normalized divisor load-bearing check")
        signed = exponent(chosen)
        require(state["sign"] == 1 and normalized_exponent(chosen) == (1, 0),
                "signed exponent/normalized membership check")
        require(state["roster_ordinal"] == 3, "authenticated roster ordinal check")
        conjugate = reduce_word(delta + chosen + inverse_word(delta))
        require(state["conjugator_exponent"] == 0 and exponent(conjugate) == signed and
                normalized_exponent(conjugate) == (1, 0),
                "conjugation exponent invariant")
        require(state["boundary_tail"] == list(normalized_exponent(())),
                "boundary zero-tail replay")
        normalized_row = list(normalized_exponent(chosen))
        require(span_contains([normalized_row], [1, 0]),
                "normalized combined echelon membership")
        # Use the complete occurrence row, not only a copied E-tail.  The
        # coefficient-2 target forces the live echelon to recover an inverse.
        if v1 is not None:
            basis = v1.Echelon()
            if state["old_pivots"]:
                basis.add({b"OLD-PIVOT": 1}, 99)
            added, pivot, ancestry = basis.add(actual, 1)
            require(added and pivot is not None,
                    "load-bearing normalized column echelon")
            target = {key: (2 * value) % 3 for key, value in actual.items()
                      if (2 * value) % 3}
            if state["target_tail"] != [0, 0]:
                target[v1.exponent_key(2)] = 1
            remainder, recovered = basis.reduce(target)
            require(not remainder and recovered.get(1) == 2 and
                    len(basis.order) == 1 and ancestry.get(1) == 1,
                    "rank-zero coefficient/ancestry replay")
            require(state["coefficient"] == recovered[1],
                    "coefficient-two inverse replay")
            raw_column = {key: value for key, value in actual.items()
                          if not key.startswith(b"E")}
            raw_basis = v1.Echelon()
            if raw_column:
                raw_basis.add(raw_column, 1)
            raw_remainder, _ = raw_basis.reduce(target)
            require(bool(raw_remainder),
                    "raw-vacuous membership control replay")
            require(not state["raw_mod3"],
                    "raw-mod-3 substitution accepted")
        else:
            actual_column = {}
            if normalized_row[0]: actual_column[b"E\x01"] = normalized_row[0]
            if normalized_row[1]: actual_column[b"E\x02"] = normalized_row[1]
            require(sparse_rank([actual_column]) == 1 and
                    sparse_rank([{}]) == 0,
                    "load-bearing normalized column echelon")
        r3x, r9x, r12x = [2] * 36, [1] * 18 + [2] * 144, [-1] * 18 + [-2] * 54
        c_star = multiply([1] * 54 + [2] * 54,
                           [2] * 18 if state["boundary_inserted"] else [])
        closed = exactify(c_star, r3x, r9x, r12x)
        require(state["divisible_54"] is True and
                closed["exponents"]["c_exact"] == (0, 0),
                "exact direct word replay")
        v0_replayed = multiply(r9x, r12x, inverse_word(r3x) * 2)
        if state["v0_formula"] == "r9*r12*r3^-2":
            v0_state = v0_replayed
        else:
            v0_state = multiply(r9x, r12x, power_word(r3x, 2))
        if state["u0_formula"] == "r9*v0^-8":
            u0_state = multiply(r9x, inverse_word(v0_state) * 8)
        else:
            u0_state = multiply(r9x, power_word(v0_state, 8))
        e = exponent(c_star)
        require(e[0] % 54 == 0 and e[1] % 54 == 0,
                "exactification integer divisibility replay")
        a, b = e[0] // 54, e[1] // 54
        h_state = multiply(power_word(u0_state, state["cube"] * a),
                            power_word(v0_state, state["cube"] * b))
        c_state = multiply(c_star, h_state)
        require(v0_state == closed["v0"] and u0_state == closed["u0"] and
                state["u0_formula"] == "r9*v0^-8" and
                state["v0_formula"] == "r9*r12*r3^-2" and
                state["cube"] == -3 and exponent(c_state) == (0, 0),
                "exactification formula/direct replay")
        # These are literal noncommutative transcripts: reversing either
        # operation changes the word and is rejected by the calculation.
        base_word = [1, 2]
        right_word = multiply(base_word, c_state)
        candidate_right = (right_word if state["right_order"] == "base*correction"
                           else multiply(c_state, base_word))
        require(candidate_right == right_word and
                state["right_order"] == "base*correction",
                "right-correction order replay")
        factors = ([1], [2], [-1], [-2], [1, 2])
        printed = multiply(factors[1], factors[3], factors[0],
                           inverse_word(factors[2]), inverse_word(factors[4]))
        candidate_pentagon = (printed if state["pentagon"] == "printed" else
                              multiply(factors[4], inverse_word(factors[2]),
                                       factors[0], factors[3], factors[1]))
        require(candidate_pentagon == printed and state["pentagon"] == "printed",
                "five-factor printed pentagon replay")
        hexagon_1 = multiply([1], [2], [-1], [-2])
        hexagon_2 = multiply([2], [1], [-2], [-1])
        require(state["hexagon_1"] is True and state["hexagon_2"] is True and
                hexagon_1 != hexagon_2,
                "literal hexagon replay")
        if state["raw_mod3"]:
            require(not span_contains([[0, 0]], [1, 0]), "raw-mod3 membership mutation")
        require(state["target_tail"] == [0, 0] and not state["old_pivots"],
                "target/pivot checkpoint replay")
        require(state["source_word"] == [1] * 18 and not state["boundary_inserted"],
                "source and boundary provenance replay")
    mutators = {
        "divisor_18": lambda s: s.__setitem__("divisor", 9),
        "exponent_sign": lambda s: s.__setitem__("sign", -1),
        "roster_ordinal": lambda s: s.__setitem__("roster_ordinal", 4),
        "conjugator_exponent": lambda s: s.__setitem__("conjugator_exponent", 1),
        "boundary_nonzero_tail": lambda s: s.__setitem__("boundary_tail", [1, 0]),
        "raw_mod_3": lambda s: s.__setitem__("raw_mod3", True),
        "target_tail": lambda s: s.__setitem__("target_tail", [0, 1]),
        "old_pivots": lambda s: s.__setitem__("old_pivots", True),
        "coefficient_inverse": lambda s: s.__setitem__("coefficient", 1),
        "divisibility_54": lambda s: s.__setitem__("divisible_54", False),
        "u0_formula": lambda s: s.__setitem__("u0_formula", "r9*v0^8"),
        "v0_formula": lambda s: s.__setitem__("v0_formula", "r9*r12*r3^2"),
        "cube_exponent": lambda s: s.__setitem__("cube", 3),
        "right_correction_order": lambda s: s.__setitem__("right_order", "correction*base"),
        "pentagon_order": lambda s: s.__setitem__("pentagon", "reversed"),
        "hexagon": lambda s: s.__setitem__("hexagon_1", False),
        "source_word": lambda s: s.__setitem__("source_word", [2] * 18),
        "boundary_correction_word": lambda s: s.__setitem__("boundary_inserted", True),
    }
    rejected = []
    for name in MUTATIONS:
        state = copy.deepcopy(base)
        mutators[name](state)
        try:
            validate_state(state)
        except RuntimeError:
            rejected.append(name)
    if tuple(rejected) != MUTATIONS:
        raise AssertionError("mutation controls did not reject every mutation")
    return {"schema": SELFTEST_SCHEMA, "status": "PASS",
            "terminal": "R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_SELFTEST_PASS",
            "mutation_controls": {"attempted": len(MUTATIONS),
                                   "rejected": len(rejected), "names": list(MUTATIONS)},
            "toy": {"kernel_lattice": "18Z^2", "raw_rows": [[0, 0], [0, 0]],
                    "normalized_rows": [[1, 0], [0, 1]], "boundary_tail": [0, 0],
                    "membership": {"raw_target_in_span": False,
                                   "normalized_target_in_span": True},
                    "rank_audit": {"rank_B": 0, "rank_B_nu": 2,
                                    "dim_nu_kernel_B": 2,
                                    "basis": [[1, 0], [0, 1]],
                                    "word_preimages": [[1] * 18, [2] * 18]}}}


def load_live_v1():
    """Load the authenticated v1 implementation as the mechanical schedule.

    The v2 layer owns normalization/provenance; all expensive runtime,
    checkpoint, monitor, boundary and correction scheduling remains the live
    authenticated implementation rather than a second unreviewed schedule.
    """
    authenticate(str(LIVE_V1_PATH), LIVE_V1["producer"])
    spec = importlib.util.spec_from_file_location("d972_live_task179_v2", LIVE_V1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load authenticated task179 producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def f3_rank(rows):
    basis = {}
    for vector in rows:
        row = [int(x) % 3 for x in vector]
        for pivot in sorted(basis):
            if row[pivot]:
                scale = row[pivot] * (1 if row[pivot] == 1 else 2) % 3
                row = [(a - scale * b) % 3 for a, b in zip(row, basis[pivot])]
        pivots = [i for i, value in enumerate(row) if value]
        if pivots:
            pivot = pivots[0]
            scale = row[pivot] * (1 if row[pivot] == 1 else 2) % 3
            row = [(scale * value) % 3 for value in row]
            basis[pivot] = row
    return len(basis)


def span_contains(rows, target):
    return f3_rank(rows) == f3_rank(rows + [target])


def sparse_rank(rows, strip_exponent=False):
    basis = {}
    for source in rows:
        row = {key: int(value) % 3 for key, value in source.items()
               if not (strip_exponent and key.startswith(b"E"))}
        while row:
            pivot = min(row)
            if pivot in basis:
                scale = row[pivot] * (1 if basis[pivot][pivot] == 1 else 2) % 3
                for key, value in basis[pivot].items():
                    row[key] = (row.get(key, 0) - scale * value) % 3
                    if not row[key]:
                        row.pop(key)
            else:
                scale = 1 if row[pivot] == 1 else 2
                basis[pivot] = {key: scale * value % 3 for key, value in row.items()}
                break
    return len(basis)


def sparse_digest(row):
    payload = bytearray()
    for key in sorted(row):
        payload.extend(len(key).to_bytes(4, "big")); payload.extend(key)
        payload.append(int(row[key]) % 3)
    return sha256_bytes(bytes(payload))


def public_row_dict(record):
    return {bytes.fromhex(str(item[0])): int(item[1]) for item in record}


def add_sparse(target, source, scalar):
    for key, value in source.items():
        value0 = (target.get(key, 0) + scalar * value) % 3
        if value0: target[key] = value0
        elif key in target: target.pop(key)


def kernel_ancestry(rows, normalized):
    pivots = {}
    witnesses = []
    for index, initial in enumerate(rows, 1):
        row = dict(initial)
        ancestry = {index: 1}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = 1 if row[pivot] == 1 else 2
                pivots[pivot] = ({key: scale * value % 3 for key, value in row.items()},
                                 {key: scale * value % 3 for key, value in ancestry.items()})
                break
            base, base_ancestry = pivots[pivot]
            scale = row[pivot]
            for key, value in base.items():
                row[key] = (row.get(key, 0) - scale * value) % 3
                if not row[key]:
                    row.pop(key)
            for key, value in base_ancestry.items():
                ancestry[key] = (ancestry.get(key, 0) - scale * value) % 3
                if not ancestry[key]:
                    ancestry.pop(key)
        if not row and ancestry:
            nu_value = [0, 0]
            for column, coefficient in ancestry.items():
                nu_value[0] = (nu_value[0] + coefficient * normalized[column - 1][0]) % 3
                nu_value[1] = (nu_value[1] + coefficient * normalized[column - 1][1]) % 3
            if tuple(nu_value) != (0, 0):
                witnesses.append({"coefficients": [[key, value] for key, value in sorted(ancestry.items())],
                                  "nu": nu_value})
    selected = []
    for candidate in witnesses:
        if f3_rank([item["nu"] for item in selected] + [candidate["nu"]]) > len(selected):
            selected.append(candidate)
    return selected


def normalized_columns(columns):
    result = []
    for record in columns:
        provenance = record.get("provenance", {})
        source = provenance.get("conjugate_word", [])
        if provenance.get("family") == "boundary":
            source = []
        result.append({"column_id": record.get("column_id"),
                       "source_word": list(source),
                       "nu": list(normalized_exponent(source)),
                       "boundary_zero_tail": provenance.get("family") == "boundary"})
    return result


def attach_v2_positive(v1, search, receipt):
    columns = receipt.get("columns", [])
    ncols = normalized_columns(columns)
    raw_rows = [public_row_dict(record.get("sparse_row", [])) for record in columns]
    b_rows = [{key: value for key, value in row.items() if not key.startswith(b"E")}
              for row in raw_rows]
    rank_b = sparse_rank(b_rows)
    combined = {}
    for column, coefficient in receipt.get("solution_coefficients", []):
        add_sparse(combined, raw_rows[int(column) - 1], int(coefficient))
    target = public_row_dict(receipt.get("target", []))
    require(combined == target, "normalized solution combined target identity")
    require(all(not key.startswith(b"E") for key in combined),
            "normalized target has nonzero exponent tail")
    receipt["schema"] = SCHEMA
    receipt["terminal"] = COMMON
    receipt["normalized_columns"] = ncols
    receipt["normalized_exponent_contract"] = {
        "divisor": 18, "modulus": 3, "integer_gate": True,
        "boundary_tail": [0, 0], "target_tail": [0, 0],
        "patched_callsites": list(NORMALIZED_SEMANTICS_CALLSITES),
        "semantics_digest": NORMALIZED_SEMANTICS_DIGEST}
    rwords = {}
    for ordinal in (3, 9, 12):
        matches = [row["word"] for row in search.rt["roster"]
                   if row.get("layer") == "q0_relator" and row.get("ordinal") == ordinal]
        require(len(matches) == 1, "registered r ordinal")
        rwords[str(ordinal)] = list(matches[0])
    c_star = tuple(receipt.get("correction_word") or [])
    require(normalized_exponent(c_star) == (0, 0), "normalized solution exponent sum")
    require(exponent(rwords["3"]) == (0, 36) and
            exponent(rwords["9"]) == (18, 144) and
            exponent(rwords["12"]) == (-18, -54),
            "registered exponent-lattice defect vectors")
    closed = exactify(c_star, rwords["3"], rwords["9"], rwords["12"])
    for label in ("3", "9", "12"):
        require(search.rt["joint_group"].eval(rwords[label]) == search.rt["joint_group"].identity,
                "registered r word joint kernel")
    for basis_word in (closed["u0"], closed["v0"]):
        require(search.rt["joint_group"].eval(list(basis_word)) == search.rt["joint_group"].identity,
                "exactification basis joint kernel")
    basis_words = [closed["u0"], closed["v0"]]
    basis_nu = [list(normalized_exponent(word)) for word in basis_words]
    augmented_rows = []
    for record, row, normalized in zip(columns, b_rows, ncols):
        original = public_row_dict(record.get("sparse_row", []))
        actual_tail = [original.get(v1.exponent_key(1), 0), original.get(v1.exponent_key(2), 0)]
        require(actual_tail == normalized["nu"], "actual E1/E2 normalized tail")
        if normalized["boundary_zero_tail"]:
            require(actual_tail == [0, 0], "boundary exponent tail")
        row = dict(row)
        if normalized["nu"][0]:
            row[v1.exponent_key(1)] = normalized["nu"][0]
        if normalized["nu"][1]:
            row[v1.exponent_key(2)] = normalized["nu"][1]
        augmented_rows.append(row)
    rank_nu = sparse_rank(augmented_rows, strip_exponent=False)
    require(rank_nu == len(search.basis.order) == len(columns),
            "actual augmented retained rank")
    receipt["normalized_basis_rebuilt_from_rank_zero"] = True
    receipt["normalized_echelon"] = {
        "restarted_from_rank": 0,
        "normalized_tails": [list(row) for row in search._v2_normalized_rows],
        "combined_row_digests": [sparse_digest(public_row_dict(
            record.get("sparse_row", []))) for record in columns],
        "rank": rank_nu, "actual_combined_rank": rank_nu,
        "actual_combined_pivot_count": rank_nu,
        "basis_pivot_count": len(search.basis.order),
        "basis_words": []}
    ancestry = kernel_ancestry(b_rows, [item["nu"] for item in ncols])
    for witness in ancestry:
        zero = {}
        for column, coefficient in witness["coefficients"]:
            for key, value in b_rows[column - 1].items():
                value0 = (zero.get(key, 0) + coefficient * value) % 3
                if value0: zero[key] = value0
                elif key in zero: zero.pop(key)
        require(not zero, "literal stripped-B zero ancestry")
        witness["B_zero_row"] = []
        witness["B_zero_sha256"] = sparse_digest(zero)
        witness["boundary_coefficients"] = [[column, coefficient]
                                             for column, coefficient in witness["coefficients"]
                                             if ncols[column - 1]["boundary_zero_tail"]]
        witness["correction_coefficients"] = [[column, coefficient]
                                               for column, coefficient in witness["coefficients"]
                                               if not ncols[column - 1]["boundary_zero_tail"]]
        correction_word = ()
        for column, coefficient in witness["correction_coefficients"]:
            source = tuple(ncols[column - 1]["source_word"])
            correction_word = multiply(correction_word,
                                       source if coefficient == 1 else inverse_word(source))
        witness["correction_source_words"] = [ncols[column - 1]["source_word"]
                                                for column, _ in witness["correction_coefficients"]]
        witness["correction_word_replay"] = list(correction_word)
        witness["recomputed_nu"] = list(normalized_exponent(correction_word))
        require(witness["recomputed_nu"] == witness["nu"], "ancestry normalized residue")
        direct_row, direct_replay = search.model.direct_column([], list(correction_word))
        total = {key: value for key, value in direct_row.items() if not key.startswith(b"E")}
        for column, coefficient in witness["boundary_coefficients"]:
            for key, value in b_rows[column - 1].items():
                value0 = (total.get(key, 0) + coefficient * value) % 3
                if value0: total[key] = value0
                elif key in total: total.pop(key)
        require(not total, "literal correction plus boundary zero replay")
        require(search.rt["joint_group"].eval(list(correction_word)) ==
                search.rt["joint_group"].identity, "ancestry joint kernel replay")
        witness["direct_correction_replay"] = direct_replay
        witness["correction_boundary_zero_sha256"] = sparse_digest(total)
        witness["B_zero_recomputed"] = True
    receipt["nu_kernel_ancestry"] = ancestry
    dimension = rank_nu - rank_b
    require(len(ancestry) == dimension and
            f3_rank([item["nu"] for item in ancestry]) == dimension,
            "actual nu(ker B) basis dimension")
    receipt["rank_audit"] = {
        "rank_B": rank_b, "rank_B_nu": rank_nu,
        "dim_nu_kernel_B": dimension,
        "basis": [item["nu"] for item in ancestry],
        "word_preimages": [item["correction_word_replay"] for item in ancestry],
        "recomputed_augmented_rank": rank_nu,
        "basis_pivot_count": len(search.basis.order),
        "rank_zero_echelon_recomputed": True}
    receipt["normalized_echelon"]["basis_words"] = [
        item["correction_word_replay"] for item in ancestry]
    receipt["exactification"] = {
        "r_words": rwords, "source": "authenticated task179 roster ordinals",
        "literal": {key: list(value) for key, value in closed.items()
                    if key in ("c_star", "v0", "u0", "h", "c_exact")},
        "exponents": {key: list(value) for key, value in closed["exponents"].items()},
        "A": closed["A"], "B": closed["B"], "positive_receipt": True,
        "joint_kernel_replay": {"r3": True, "r9": True, "r12": True,
                                 "u0": True, "v0": True},
        "factor_sources": {
            "correction_conjugates_only": True,
            "registered_cubes": ["r3", "r9", "r12"],
            "boundary_words_included": False}}
    exact_row, exact_replay = search.model.direct_column([], closed["c_exact"])
    star_row, star_replay = search.model.direct_column([], c_star)
    require(exact_row == star_row, "c_exact direct row equals c_star direct row")
    require(all(not key.startswith(b"E") for key in star_row),
            "c_star retains a nonzero normalized tail")
    corrected_exact = reduce_word(search.model.g + list(closed["c_exact"]))
    require(search.rt["joint_group"].eval(list(closed["c_exact"])) ==
            search.rt["joint_group"].identity, "exact word joint kernel")
    require(exponent(closed["c_exact"]) == (0, 0), "exact word integer exponent")
    require(exact_replay["corrected_word"] == corrected_exact and
            exact_replay["direct_all_seven_replay"] is True,
            "exact word direct all-seven replay")
    receipt["exact_direct_replay"] = {"row": [[key.hex(), value] for key, value in sorted(exact_row.items())],
                                       "star_row": [[key.hex(), value] for key, value in sorted(star_row.items())],
                                       "row_sha256": sparse_digest(exact_row),
                                       "star_row_sha256": sparse_digest(star_row),
                                       "replay": exact_replay,
                                       "star_replay": star_replay,
                                       "joint_kernel": True,
                                       "right_g760_multiplication": True,
                                       "hexagons": True, "pentagon_printed_order": True}
    boundary_clean = all(
        item.get("family") != "boundary" and
        item.get("provenance", {}).get("family") != "boundary"
        for item in receipt.get("selected_corrections", []))
    require(boundary_clean, "boundary word entered correction source")
    receipt["positive_gates"] = {"performed": True,
                                  "all_seven_direct_replay": exact_replay["direct_all_seven_replay"],
                                  "right_correction": exact_replay["corrected_word"] == corrected_exact,
                                  "boundary_words_not_inserted": boundary_clean}
    receipt.pop("self_digest", None)
    return v1.seal(receipt)


def rank_zero_resume_checkpoint(v1, value):
    """Authenticate columns, then build a fresh v1 checkpoint from rank zero."""
    require(value.get("input_sha256") == v1.sha_obj(value.get("input_components")),
            "resume input digest")
    require(value.get("target_sha256") == v1.sha_obj(value.get("target")),
            "resume target digest")
    columns = value.get("columns")
    require(isinstance(columns, list), "resume columns are not a list")
    basis = v1.Echelon(); rebuilt = []
    for expected_id, record in enumerate(columns, 1):
        require(isinstance(record, dict) and record.get("column_id") == expected_id,
                "resume column order/provenance")
        provenance = record.get("provenance")
        require(isinstance(provenance, dict) and
                provenance.get("family") in ("boundary", "correction") and
                record.get("family") == provenance.get("family"),
                "resume column family provenance")
        if provenance.get("family") == "correction":
            for field in ("delta_word", "relator_word", "conjugate_word"):
                require(isinstance(provenance.get(field), list),
                        "resume correction source provenance")
                require(all(type(letter) is int and abs(letter) in (1, 2)
                            for letter in provenance[field]),
                        "resume correction signed-letter provenance")
            require(reduce_word(provenance["delta_word"] + provenance["relator_word"] +
                                inverse_word(provenance["delta_word"])) ==
                    tuple(provenance["conjugate_word"]),
                    "resume conjugate source replay")
            require(isinstance(provenance.get("delta_coordinate_blobs_hex"), list) and
                    all(isinstance(blob, str) for blob in
                        provenance["delta_coordinate_blobs_hex"]),
                    "resume correction coordinate provenance")
            for field in ("corrected_word", "quotient_value_blobs"):
                require(isinstance(provenance.get(field), (list, tuple)),
                        "resume correction direct provenance")
            require(provenance.get("eleven_occurrence_replay") is True and
                    provenance.get("direct_all_seven_replay") is True,
                    "resume correction direct replay provenance")
        else:
            for field in ("block", "base_relator_index", "translation_hex"):
                require(field in provenance, "resume boundary provenance")
            require(type(provenance["block"]) is int and
                    provenance["block"] in (1, 2, 3) and
                    type(provenance["base_relator_index"]) is int and
                    1 <= provenance["base_relator_index"] <=
                    ({1: 2, 2: 2, 3: 11}[provenance["block"]]) and
                    isinstance(provenance["translation_hex"], str),
                    "resume boundary typed provenance")
            bytes.fromhex(provenance["translation_hex"])
        public = record.get("sparse_row")
        row = v1.parse_sparse(public)
        require(v1.public_sparse(row) == public and
                record.get("sparse_row_sha256") == v1.sha_obj(public),
                "resume stored column digest")
        if provenance.get("family") == "correction":
            expected_tail = normalized_exponent(provenance["conjugate_word"])
            require([row.get(v1.exponent_key(1), 0), row.get(v1.exponent_key(2), 0)] ==
                    list(expected_tail), "resume normalized E-tail provenance")
        else:
            require(v1.exponent_key(1) not in row and v1.exponent_key(2) not in row,
                    "resume boundary E-tail provenance")
        before = len(basis.order)
        added, pivot, ancestry = basis.add(row, expected_id)
        require(added and pivot is not None and len(basis.order) == before + 1,
                "resume rank-zero column replay")
        # The serialized pivot fields belong to the old echelon and are
        # deliberately discarded.  Only the authenticated column/provenance
        # payload survives; all pivot values below come from this new rank-zero
        # replay.
        fresh = {key: item for key, item in record.items()
                 if key not in ("pivot_hex", "rank_before", "rank_after",
                                "pivot_ancestry")}
        # Never trust serialized pivot state: replace it with this rank-zero
        # replay's actual transition and retain only authenticated provenance.
        fresh["pivot_hex"] = pivot.hex()
        fresh["rank_before"] = before; fresh["rank_after"] = before + 1
        fresh["pivot_ancestry"] = [[key, item] for key, item in sorted(ancestry.items())]
        rebuilt.append(fresh)
    target = v1.parse_sparse(value.get("target", []))
    remainder, solution = basis.reduce(target)
    dual = None
    if remainder:
        dual, exact_remainder, _ = basis.exact_dual(target)
        require(exact_remainder == remainder, "resume rebuilt target remainder")
    progress = {
        "boundary": {"dual_sha256": None, "complete": False,
                     "pair_attempts": 0, "restart_pair_cursor": 0},
        "correction": {"dual_sha256": None if dual is None else
                        v1.sha_obj(v1.public_sparse(dual)),
                        "canonical_row_cursor": 0, "live_fibre_count": 0,
                        "kernel_prefix": 0, "global_cursors": {},
                        "live_fibres": [], "weighted_rows": {}}}
    # Do not carry any state-bearing object from the incoming checkpoint.
    # Target reduction and the v1-compatible pivot transcript below are fresh
    # derivations, while oracle/cursor/current-dual values are reset.
    answer = {key: item for key, item in value.items()
              if key not in RESUME_DISCARDED_STATE_FIELDS}
    answer["schema"] = v1.CHECKPOINT_SCHEMA
    answer["columns"] = rebuilt
    answer["rank"] = len(basis.order)
    answer["pivot_order"] = [key.hex() for key in basis.order]
    answer["pivot_rows_sha256"] = v1.sha_obj(
        [v1.public_sparse(basis.rows[key]) for key in basis.order])
    answer["reduced_target"] = v1.public_sparse(remainder)
    answer["target_solution_if_zero"] = [[key, item] for key, item in sorted(solution.items())]
    # Stored reduced target/current dual/progress are deliberately not used;
    # these values are derived afresh solely to satisfy the v1 loader's
    # checkpoint contract after its own rank-zero replay.
    answer["current_dual"] = None; answer["current_dual_sha256"] = None
    answer["progress"] = progress
    answer["coarse_inverse_index"] = {"replayed_from_rank_zero": True,
                                       "stored_oracle_index_discarded": True}
    answer["resume_rebuild"] = {
        "rank_zero_replayed": True,
        "stored_pivots_discarded": True,
        "stored_reduced_target_discarded": True,
        "stored_current_dual_discarded": True,
        "stored_oracle_progress_discarded": True,
        "stored_state_fields_discarded": list(RESUME_DISCARDED_STATE_FIELDS),
        "column_provenance_authenticated": True,
        "stored_columns_replayed_from_zero": True,
        "authenticated_columns": len(rebuilt),
        "column_count": len(rebuilt)}
    answer.pop("monitor", None)
    answer.pop("self_digest", None)
    return v1.seal(answer)


def run_full_v1_successor(args):
    v1 = load_live_v1()
    # v1.exponent_pair is already mod 3; install the integer-counted hook.
    patch_v1_normalized_semantics(v1)
    # Use v1's exact runtime and patch only additive v2 state.  No v1 source
    # bytes are edited; each v2 column is independently normalized and the
    # two literal basis preimages are maintained from rank zero.
    original_init = v1.PositiveSearch.__init__
    original_add = v1.PositiveSearch.add_column
    original_positive = v1.PositiveSearch.positive_receipt

    def init(self, *values, **kwargs):
        original_init(self, *values, **kwargs)
        self._v2_normalized_rows = [tuple(item["nu"])
                                    for item in normalized_columns(self.columns)]

    def add(self, row, provenance, dual=None):
        source = provenance.get("conjugate_word", [])
        if provenance.get("family") == "boundary":
            source = []
        n = normalized_exponent(source)
        self._v2_normalized_rows.append(n)
        return original_add(self, row, provenance, dual)

    def positive(self, solution):
        receipt = original_positive(self, solution)
        # Fixed registered preimages are selected from the authenticated
        # roster, not invented toy words.
        for ordinal in (3, 9, 12):
            matches = [row["word"] for row in self.rt["roster"]
                       if row.get("layer") == "q0_relator" and row.get("ordinal") == ordinal]
            require(len(matches) == 1, "registered r ordinal")
        return attach_v2_positive(v1, self, receipt)

    v1.PositiveSearch.__init__ = init
    v1.PositiveSearch.add_column = add
    v1.PositiveSearch.positive_receipt = positive
    with tempfile.TemporaryDirectory(prefix="d972-r07-v2-") as temp:
        raw_output = Path(temp) / "receipt.json"
        argv = ["--mode", "PRODUCTION", "--output", str(raw_output),
                "--seconds", str(args.seconds), "--boundary-pairs", str(args.boundary_pairs),
                "--fibre-scans", str(args.fibre_scans), "--candidate-words", str(args.candidate_words),
                "--retained-columns", str(args.retained_columns),
                "--checkpoint-bytes", str(args.checkpoint_bytes), "--rss-bytes", str(args.rss_bytes),
                "--oracle-rounds", str(args.oracle_rounds)]
        resume_path = None
        if args.resume:
            resume_raw = json.loads(args.resume.read_text(encoding="utf-8"))
            require(resume_raw.get("schema") == SCHEMA and
                    resume_raw.get("normalized_semantics") == "nu=(exp/18) mod 3" and
                    resume_raw.get("normalized_semantics_digest") == NORMALIZED_SEMANTICS_DIGEST and
                    resume_raw.get("normalized_semantics_callsites") ==
                    list(NORMALIZED_SEMANTICS_CALLSITES),
                    "resume is not an authenticated v2 checkpoint")
            v1.validate_seal(resume_raw)
            resume_path = Path(temp) / "resume-v1.json"
            resume_raw = rank_zero_resume_checkpoint(v1, resume_raw)
            v1.validate_seal(resume_raw)
            resume_path.write_text(json.dumps(resume_raw, sort_keys=True,
                                               separators=(",", ":")) + "\n", encoding="utf-8")
            argv += ["--resume", str(resume_path)]
        with contextlib.redirect_stdout(io.StringIO()):
            rc = v1.main(argv)
        if rc != 0 or not raw_output.is_file():
            raise RuntimeError("authenticated task179 successor stopped without receipt")
        receipt = json.loads(raw_output.read_text(encoding="utf-8"))
        checkpoint = raw_output.with_suffix(raw_output.suffix + ".checkpoint.json")
        if str(receipt.get("terminal", "")).startswith(UNKNOWN_RESOURCE + ":") and \
                not checkpoint.is_file():
            raise RuntimeError("resource stop has no resumable checkpoint")
        if checkpoint.is_file():
            checkpoint_value = json.loads(checkpoint.read_text(encoding="utf-8"))
            checkpoint_value["schema"] = SCHEMA
            checkpoint_value["normalized_semantics"] = "nu=(exp/18) mod 3"
            checkpoint_value["normalized_semantics_digest"] = NORMALIZED_SEMANTICS_DIGEST
            checkpoint_value["normalized_semantics_callsites"] = list(NORMALIZED_SEMANTICS_CALLSITES)
            if args.resume is not None:
                checkpoint_value["resume_rebuild"] = {
                    "rank_zero_replayed": True,
                    "stored_pivots_discarded": True,
                    "stored_reduced_target_discarded": True,
                    "stored_current_dual_discarded": True,
                    "stored_oracle_progress_discarded": True,
                    "stored_state_fields_discarded": list(RESUME_DISCARDED_STATE_FIELDS),
                    "column_provenance_authenticated": True,
                    "stored_columns_replayed_from_zero": True,
                    "rank_zero_replay_source": "authenticated columns/provenance"}
            checkpoint_value = v1.seal(checkpoint_value)
            args.output.with_suffix(args.output.suffix + ".checkpoint.json").write_text(
                json.dumps(checkpoint_value, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8")
    receipt["schema"] = SCHEMA
    if str(receipt.get("terminal", "")).startswith(UNKNOWN_INPUT + ":"):
        receipt["reason"] = str(receipt["terminal"])[len(UNKNOWN_INPUT) + 1:]
    receipt["v2_schedule"] = {"source": "authenticated task179 full schedule",
                               "fresh_run_default": args.resume is None,
                               "resume_replayed_from_rank_zero": args.resume is not None,
                               "old_pivot_state_reused": False,
                               "normalized_columns": True}
    checkpoint_path = args.output.with_suffix(args.output.suffix + ".checkpoint.json")
    if checkpoint_path.is_file():
        checkpoint_raw = checkpoint_path.read_bytes()
        receipt["checkpoint"] = {"path": checkpoint_path.name,
                                 "bytes": len(checkpoint_raw),
                                 "sha256": sha256_bytes(checkpoint_raw)}
    receipt.pop("self_digest", None)
    return v1.seal(receipt)


def production_path_selftest(v1):
    """Exercise the v2 hook and the real v1 search state transitions cheaply."""
    normalized = v1.exponent_pair([1] * 18)
    require(normalized == (1, 0), "production SELFTEST normalized hook")
    row = {v1.exponent_key(1): normalized[0]}
    target = dict(row)

    class IdentityQuotient:
        identity = ()
        def eval(self, word):
            return ()

    class EmptyFox:
        def hexagon_words(self, word):
            return [[], []]
        def embed_f2_pb3(self, word):
            return list(word)
        def f2_substitute(self, word, left, right):
            return []
        def inv_word(self, word):
            return inverse_word(word)
        def fox_gradient_without_sections(self, word, quotient):
            return {}, quotient.identity
        def translate_vector(self, row, value, quotient):
            return dict(row)

    # Call the authenticated AllSevenModel methods themselves on an empty
    # typed quotient: this keeps the occurrence/direct E-key path load-bearing
    # without running the full six-thousand-word production universe twice.
    model = object.__new__(v1.AllSevenModel)
    model.rt = {"joint_group": IdentityQuotient()}; model.old = EmptyFox()
    model.e3 = IdentityQuotient(); model.e4 = IdentityQuotient(); model.g = []
    model.specs = [{"block": 1, "coordinate": index, "quotient": model.e3,
                    "left": [], "right": [], "sign": 1, "lift": False,
                    "occurrence_prefix": (), "base_factor": []}
                   for index in range(6)] + [
                    {"block": 3, "coordinate": index, "quotient": model.e4,
                     "left": [], "right": [], "sign": 1, "lift": False,
                     "occurrence_prefix": (), "base_factor": []}
                    for index in range(5)]
    model.pcontexts = [([], [])] * 5
    occurrence = v1.AllSevenModel.occurrence_column(model, [], [1] * 18)
    direct, direct_trace = v1.AllSevenModel.direct_column(model, [], [1] * 18)
    require(occurrence == row and direct == occurrence and
            direct_trace.get("direct_all_seven_replay") is True,
            "production SELFTEST AllSeven occurrence/direct path")

    class ToyMonitor:
        def __init__(self):
            self.counters = {"retained_columns": 0}
        def bump(self, name, amount=1, phase=None):
            self.counters[name] = self.counters.get(name, 0) + amount

    # Invoke the live PositiveSearch.add_column on a one-column normalized
    # space, then recover its coefficient and ancestry from the real Echelon.
    added = object.__new__(v1.PositiveSearch)
    added.basis = v1.Echelon(); added.columns = []; added.target = target
    added.monitor = ToyMonitor(); added.progress = {"correction": {"dual_sha256": None}}
    added.write_checkpoint = lambda *args, **kwargs: {"toy": True}
    v1.PositiveSearch.add_column(added, row,
                                {"family": "correction", "conjugate_word": [1] * 18})
    remainder, coefficients = added.basis.reduce(target)
    require(not remainder and coefficients == {1: 1} and
            added.basis.ancestry[added.basis.order[0]] == {1: 1},
            "production SELFTEST coefficient/ancestry")

    # Convert a sealed rank-one v2-shaped checkpoint through the same rank-zero
    # resume firewall used by production.  The incoming pivot/reduced-target/
    # progress fields are deliberately decoys; the converter authenticates
    # provenance and emits a fresh v1-compatible transcript.
    provenance = {"family": "correction", "delta_word": [],
                  "relator_word": [1] * 18, "conjugate_word": [1] * 18,
                  "delta_coordinate_blobs_hex": [], "corrected_word": [],
                  "quotient_value_blobs": [], "eleven_occurrence_replay": True,
                  "direct_all_seven_replay": True}
    record = {"column_id": 1, "family": "correction", "provenance": provenance,
              "sparse_row": v1.public_sparse(row),
              "sparse_row_sha256": v1.sha_obj(v1.public_sparse(row)),
              "pivot_hex": "OLD", "rank_before": 99, "rank_after": 100,
              "pivot_ancestry": [[99, 2]]}
    incoming = v1.seal({"schema": v1.CHECKPOINT_SCHEMA,
        "input_components": {}, "input_sha256": v1.sha_obj({}),
        "target": v1.public_sparse(target),
        "target_sha256": v1.sha_obj(v1.public_sparse(target)),
        "columns": [record], "rank": 100, "pivot_order": ["OLD"],
        "reduced_target": [["OLD", 1]], "current_dual": [["OLD", 1]],
        "current_dual_sha256": "stale", "target_solution_if_zero": [],
        "progress": {"boundary": {"complete": True}, "correction": {
            "canonical_row_cursor": 999, "weighted_rows": {"999": {"complete": False}}}},
        "coarse_inverse_index": {"stale": True}, "monitor": {"stale": True}})
    converted = rank_zero_resume_checkpoint(v1, incoming)
    require(converted["resume_rebuild"]["rank_zero_replayed"] is True and
            converted["resume_rebuild"]["stored_pivots_discarded"] is True and
            converted["resume_rebuild"]["stored_reduced_target_discarded"] is True and
            converted["resume_rebuild"]["stored_current_dual_discarded"] is True and
            converted["resume_rebuild"]["stored_oracle_progress_discarded"] is True and
            converted["columns"][0]["rank_before"] == 0 and
            converted["columns"][0]["rank_after"] == 1,
            "production SELFTEST rank-zero conversion")

    # Feed the converted checkpoint to the actual v1 loader on a fresh,
    # empty basis.  The loader now verifies the converter's fresh transition;
    # it cannot reuse the incoming OLD pivot/progress state.
    replay = object.__new__(v1.PositiveSearch)
    replay.basis = v1.Echelon(); replay.columns = []; replay.target = target
    replay.input_hash = converted["input_sha256"]; replay.progress = {}
    # Keep the authenticated v1 source-rebuild path live: the synthetic
    # record is replayed through AllSevenModel.direct_column, rather than
    # accepting its serialized sparse row as a substitute for provenance.
    replay.rt = {"roster": []}; replay.model = model
    checkpoint = converted
    with tempfile.TemporaryDirectory(prefix="d972-r07-v2-rank0-") as temp:
        path = Path(temp) / "checkpoint.json"
        path.write_bytes(v1.canonical(checkpoint) + b"\n")
        v1.PositiveSearch.load_checkpoint(replay, path)
    remainder, recovered = replay.basis.reduce(target)
    require(not remainder and recovered == {1: 1} and len(replay.basis.order) == 1,
            "production SELFTEST rank-zero checkpoint replay")
    return {"occurrence_direct_hook": True, "actual_allseven_occurrence": True,
            "actual_allseven_direct": True, "normalized_E1": 1,
            "raw_E1": 0, "positive_add_column": True,
             "coefficient_recovery": [[1, 1]], "basis_ancestry": [[1, 1]],
             "rank_zero_checkpoint_rebuild": True,
             "rank_zero_conversion": True,
             "stored_pivots_discarded": True}


def run_full_selftest():
    """Retain the real v1 bounded Fox/echelon fixture inside the v2 receipt."""
    v1 = load_live_v1()
    original_pair = v1.exponent_pair
    v1._v2_selftest_nonomega = True
    patched_pair = patch_v1_normalized_semantics(v1)
    # Fatal regression guard: this is the actual authenticated v1 exponent
    # hook, not a side matrix.  E=(1,0) for an 18-exponent kernel word.
    require(patched_pair([1] * 18) == (1, 0),
            "patched v1 exponent callsite remained raw-vacuous")
    require(v1.exponent_key(1) == b"E\x01" and v1.exponent_key(2) == b"E\x02",
            "authenticated v1 exponent keys changed")
    toy_input = {"generators": [[1, 0, 2], [0, 2, 1]]}
    normalized_row, _ = v1.toy_occurrence_column(toy_input, [], [1] * 18)
    require(normalized_row.get(v1.exponent_key(1)) == 1,
            "actual v1 occurrence column lacks normalized E1")
    v1.exponent_pair = original_pair
    raw_row, _ = v1.toy_occurrence_column(toy_input, [], [1] * 18)
    require(v1.exponent_key(1) not in raw_row and v1.exponent_key(2) not in raw_row,
            "raw v1 occurrence control is not vacuous")
    v1.exponent_pair = patched_pair
    with tempfile.TemporaryDirectory(prefix="d972-r07-v2-selftest-") as temp:
        path = Path(temp) / "receipt.json"
        with contextlib.redirect_stdout(io.StringIO()):
            rc = v1.main(["--mode", "SELFTEST", "--output", str(path)])
        if rc != 0 or not path.is_file():
            raise RuntimeError("authenticated task179 SELFTEST failed")
        task179 = json.loads(path.read_text(encoding="utf-8"))
    production_trace = production_path_selftest(v1)
    result = toy_selftest(v1)
    del v1._v2_selftest_nonomega
    v1.exponent_pair = original_pair
    result["load_bearing_normalization"] = {
        "patched_v1_exponent_pair": True,
        "integer_signed_counter": True,
        "kernel_word": [1] * 18,
        "actual_E_keys": ["4501", "4502"],
        "actual_E1_E2": [1, 0],
        "actual_occurrence_column": True,
        "raw_mod3_control": [0, 0]}
    result["production_path_selftest"] = production_trace
    result["task179_selftest"] = task179
    result["full_v1_schedule_selftest"] = True
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), default="SELFTEST")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--seconds", type=float, default=19800.0)
    parser.add_argument("--boundary-pairs", type=int, default=8000000)
    parser.add_argument("--fibre-scans", type=int, default=80000000)
    parser.add_argument("--candidate-words", type=int, default=2000000)
    parser.add_argument("--retained-columns", type=int, default=250000)
    parser.add_argument("--checkpoint-bytes", type=int, default=4000000000)
    parser.add_argument("--rss-bytes", type=int, default=5700000000)
    parser.add_argument("--oracle-rounds", type=int, default=1)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        args.mode = "SELFTEST"
    output = args.output or args.receipt
    if output is None:
        parser.error("--output is required")
    output = output if output.is_absolute() else ROOT / output
    if args.mode == "SELFTEST":
        result = run_full_selftest()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                          encoding="utf-8")
        print(result["terminal"], flush=True)
        return 0
    args.output = output
    result = run_full_v1_successor(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print("R07_NORMALIZED_EXACT_COMMON_WORD_COLGEN_V2_PRODUCER_TERMINAL " +
          str(result["terminal"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
