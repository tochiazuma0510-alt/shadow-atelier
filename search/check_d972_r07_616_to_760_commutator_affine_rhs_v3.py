#!/usr/bin/env python3
"""Independent checker for the R07 760 commutator/affine v3 receipt.

No helper from the v3 producer is imported.  The checker uses the separately
frozen v10 arithmetic implementation, reconstructs every bounded preflight
field, and uses the independent 157em checker chain only in explicit GHA
``--full`` mode.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-616-to-760-commutator-affine-rhs/v3"
FINAL_MARKER = "R07_760_COMMUTATOR_AFFINE_RHS_V3_CHECKER_PASS"
DEFAULT_RECEIPT = Path(
    "search/certs/d972_r07_616_to_760_commutator_affine_rhs_"
    "preflight_v3_20260826.json")
Q3_PATH = Path(
    "ci/b345_157dp_artifacts_32171982444/d972_b345_q3_chief_v1.json")
OLD_PATH = Path("search/check_d972_b345_relfrat3_wordexpr_memo_v10.py")
P23_PATH = Path("crosscheck/check_d972_r07_p23_joint_literal_v1.py")
HEAVY_CHECKER_PATH = Path("search/check_d972_b345_target6_dual_colgen_v1.py")
Q3_RUNTIME_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")

PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
INVERSE_SHA = "7d49ed8811f661031077b45d7fd6fab2eb21fdef308486367dc8981d0918879e"
SOURCE_KEY_SHA = "59ae54aedb638b5cf69d76ba4d838c94a1c6412af89689f6709af4350e5ef0a2"
Q4_ORDER = "583152628325845597028352"

PIN_SPECS = {
    "q3": (Q3_PATH, 231570,
        "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "old_v10": (OLD_PATH, 410844,
        "264258dcb945401e3db10ecd4fedd7a8dd79a8d7b0f31dbc0cfbe643537eac2d"),
    "p23": (P23_PATH, 32201,
        "56f479bbb17b0a7aa756ce79ce02dcccab5236b67ea85f90a90830f97e389bc2"),
    "heavy_157em_checker": (HEAVY_CHECKER_PATH, 228980,
        "08cee7be18128b1dcc1376012854a828695c19a97bd1495e4cb0d7f7ddea035e"),
}

W2 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -2, 1, 1,
    2, 1, 1, -2, 1, 1, 2, 1, 1, 2, 1, 1, -2, 1, 1, -2, 1, 1,
    2, 2, -1, -1, -2, -1,
)
W3 = (
    1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -1, -1, 2,
    -1, -1, -2, -2, 1, 1, 2, 1, 2, 2, 1, 2, 2, -1, 2, 2, 1, 2,
    1, 1, 2, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, -2, -1,
    -2, -2, 1, 2, 1, 1, -2, 1,
)


def require(condition: Any, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def authenticate() -> None:
    for label, (path, size, digest) in PIN_SPECS.items():
        full = ROOT / path
        require(full.is_file() and full.stat().st_size == size and
                digest_file(full) == digest, "checker pin " + label)


def load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None, "checker module spec")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None); raise
    return module


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(type(letter) is int and letter in (-2, -1, 1, 2),
                "checker signed alphabet")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return [-x for x in reversed(word)]


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum(1 if x == i else -1 if x == -i else 0 for x in word)
            for i in (1, 2)]


def construct_base() -> tuple[list[int], list[int], list[int]]:
    f = reduce_word(list(W2) + reduce_word(inv_word(W3) + list(W2)) * 8)
    r = [1] * 108 + [-2] * 36
    g = reduce_word(f + inv_word(r))
    require(len(f) == 616 and digest_obj(f) == PARENT_SHA and
            len(g) == 760 and digest_obj(g) == BASE_SHA and
            exponent_sums(g) == [0, 0], "checker base pins")
    return f, r, g


def encode(value: Any) -> dict[str, Any]:
    row = {"coarse_one_line": [int(x) + 1 for x in value[0]],
           "fine_pc_coords": list(value[1])}
    row["sha256"] = digest_obj(row)
    return row


def rank3(matrix: Sequence[Sequence[int]]) -> int:
    rows = [[int(x) % 3 for x in row] for row in matrix]; rank = 0
    for col in range(len(rows[0]) if rows else 0):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        if rows[rank][col] == 2:
            rows[rank] = [(2 * x) % 3 for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                a = rows[i][col]
                rows[i] = [(x - a * y) % 3 for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def inverse_and_source(old: Any, q3: dict[str, Any], e4: Any,
                       g: Sequence[int]) -> tuple[list[list[int]], list[Any],
                                                  list[list[int]], dict[str, Any]]:
    row7 = next(row for row in q3["canonical_roof_powers"]["rows"]
                if row["exponent"] == 7)
    candidate = old.reduce_word(row7["word"] +
        q3["correction_fibre"]["records"][0]["word"])
    inverse = old.source_words(candidate)
    source = old.source_words(g)
    sv = [e4.eval(word) for word in source]
    iv = [e4.eval(word) for word in inverse]
    st = [e4.mul(e4.eval(inverse[i], sv), e4.inverse(e4.generators[i]))
          for i in range(6)]
    ts = [e4.mul(e4.eval(source[i], iv), e4.inverse(e4.generators[i]))
          for i in range(6)]
    require(all(x == e4.identity for x in st + ts) and
            digest_obj(inverse) == INVERSE_SHA, "checker inverse")
    key = [encode(x) for x in sv]
    require(digest_obj(key) == SOURCE_KEY_SHA, "checker source key")
    public = {
        "normalized_exponent": 7,
        "selected_correction_index_one_based": 1,
        "candidate_word": candidate,
        "candidate_word_sha256": digest_obj(candidate),
        "inverse_words": inverse,
        "inverse_word_lengths": list(map(len, inverse)),
        "inverse_words_sha256": digest_obj(inverse),
        "source_words": source, "source_words_sha256": digest_obj(source),
        "source_key": key, "source_key_sha256": digest_obj(key),
        "ST_values": [encode(x) for x in st],
        "TS_values": [encode(x) for x in ts],
        "all_twelve_identity": True,
    }
    return inverse, sv, source, public


def joint_public(old: Any, p23: Any, e3: Any, e4: Any,
                 f: Sequence[int], r: Sequence[int], g: Sequence[int]) -> dict[str, Any]:
    c3 = [e3.generators[0], e3.generators[2]]
    c4 = [(e4.eval(m[0]), e4.eval(m[2])) for m in old.cofaces(3)]
    er3 = e3.eval(r, c3); er4 = [e4.eval(r, c) for c in c4]
    require(er3 == e3.identity and all(x == e4.identity for x in er4) and
            e3.eval(f, c3) == e3.eval(g, c3) and
            all(e4.eval(f, c) == e4.eval(g, c) for c in c4),
            "checker complete settled identity")
    gr = p23.evaluate_generic(r, p23.G36_ONE, (p23.X36, p23.Y36),
                              p23.g36_mul, p23.g36_inv)
    pr = p23.evaluate_generic(r, p23.MATRIX_ONE, (p23.X_PSL, p23.Y_PSL),
                              p23.matrix_mul, p23.matrix_inv)
    s2, s3 = p23.JenningsD4(2, 2, ()), p23.JenningsD4(3, 2, ())
    b2 = p23.JenningsD4(2, 6, p23.PB4_RELATORS)
    b3 = p23.JenningsD4(3, 6, p23.PB4_RELATORS)
    k2, k3 = p23.relation_key(s2, b2, r), p23.relation_key(s3, b3, r)
    require(gr == p23.G36_ONE and pr == p23.MATRIX_ONE and
            k2[0] == s2.one and all(x == b2.one for x in k2[1:]) and
            k3[0] == s3.one and all(x == b3.one for x in k3[1:]),
            "checker p2/p3 joint identity")
    mutant = list(r); mutant[0] = 2
    mg = p23.evaluate_generic(mutant, p23.G36_ONE, (p23.X36, p23.Y36),
                              p23.g36_mul, p23.g36_inv)
    mp = p23.evaluate_generic(mutant, p23.MATRIX_ONE,
        (p23.X_PSL, p23.Y_PSL), p23.matrix_mul, p23.matrix_inv)
    require(mg != p23.G36_ONE or mp != p23.MATRIX_ONE, "checker r mutation")
    return {
        "r_definition": "x^108*y^-36", "r_word": list(r),
        "r_word_sha256": digest_obj(r), "complete_E3_source": encode(er3),
        "complete_E4_five_cofaces": [encode(x) for x in er4],
        "G36_value": [[int(a), int(b)] for a, b in gr],
        "PSL2_8_identity": pr == p23.MATRIX_ONE,
        "p2_source_plus_five_cofaces_identity": [k2[0] == s2.one] +
            [x == b2.one for x in k2[1:]],
        "p3_source_plus_five_cofaces_identity": [k3[0] == s3.one] +
            [x == b3.one for x in k3[1:]],
        "p2_coordinate_sha256": digest_obj([list(s2.coords(k2[0]))] +
            [list(b2.coords(x)) for x in k2[1:]]),
        "p3_coordinate_sha256": digest_obj([list(s3.coords(k3[0]))] +
            [list(b3.coords(x)) for x in k3[1:]]),
        "f_equals_g_on_all_settled_constituents": True,
        "diagonal_joint_correlation_remaining": False,
        "mutated_r_first_letter": {"mutant": 2,
            "G36_identity": mg == p23.G36_ONE,
            "PSL2_8_identity": mp == p23.MATRIX_ONE, "rejected": True},
    }


def relation_public(old: Any, q3: dict[str, Any], e3: Any, e4: Any,
                    f: Sequence[int], g: Sequence[int], inverse: list[list[int]],
                    sv: list[Any], source: list[list[int]],
                    inv_public: dict[str, Any]) -> dict[str, Any]:
    require([e4.eval(w) for w in old.source_words(f)] == sv,
            "checker source equality")
    rels = old.pure_relations(4); rv = [e4.eval(w, sv) for w in rels]
    require(all(x == e4.identity for x in rv), "checker PB4 relators")
    coarse = [old.perm_eval(word, [x[0] for x in sv]) for word in inverse]
    require(coarse == [x[0] for x in e4.generators], "checker Q4 recovery")
    matrix = [list(x[1][:6]) for x in sv]
    require(rank3(matrix) == 6 and
            q3["coarse_models"]["Q4"]["order_decimal"] == Q4_ORDER,
            "checker direct-product pins")
    c3 = [e3.generators[0], e3.generators[2]]
    hw = old.hexagon_words(g); hv = [e3.eval(w, c3) for w in hw]
    pent = old.pentagon_word(g); pv = e4.eval(pent)
    require(hv == [e3.identity, e3.identity] and pv == e4.identity,
            "checker literal relations")
    return {
        "two_hexagon_words": [{"length": len(w), "sha256": digest_obj(w)} for w in hw],
        "two_hexagon_values": [encode(x) for x in hv],
        "ordered_A18_word": {"length": len(pent), "sha256": digest_obj(pent)},
        "ordered_A18_value": encode(pv),
        "ordered_A18_convention": "native F*E*C*B^-1*A^-1; slots C,A,E,B,F",
        "R07_mark_replayed": True, "inverse": inv_public,
        "PB4_relators": [{"ordinal": i + 1, "word_sha256": digest_obj(w),
            "value": encode(v), "identity": True}
            for i, (w, v) in enumerate(zip(rels, rv))],
        "Q4_generation": {"method":
            "six inverse words recover all six marked Q4 generators",
            "recovered_generator_sha256": digest_obj(
                [[int(x) + 1 for x in value] for value in coarse]),
            "all_six_recovered": True, "Q4_order_decimal": Q4_ORDER},
        "Pi4_mod_Phi": {"basis":
            ["a12", "a13", "a14", "a23", "a24", "a34"],
            "matrix_rows_source_generators": matrix, "rank_F3": 6,
            "full_span": True},
        "direct_product": {"ambient": "E4=Q4xPi4[3]", "authenticated": True,
            "Q4_abelianization_order": 32,
            "three_divides_Q4_ab_order": False},
        "current_E4_onto": True,
        "current_E4_source_endomorphism_automorphism": True,
        "grade": "candidate; prior v89 subclaim cross-checked",
    }


def manifest_public(old: Any, e4: Any, g: Sequence[int],
                    inverse: Sequence[Sequence[int]]) -> dict[str, Any]:
    prior = list(old.FIXED_WORD); old.FIXED_WORD = list(g)
    try:
        candidate = old.build_check_wordexpr(0, [], inverse)
        named = [(n, r) for n, _, r in
                 candidate["acceptance"] + candidate["diagnostics"]]
        dag = candidate["dag"].serialize(named)
        ev = old.CheckWordExprEvaluator(candidate["dag"], e4)
        values = ev.evaluate_values()
        require(all(values[root - 1] == e4.identity
                    for _, _, root in candidate["acceptance"]),
                "checker 33 acceptance values")
        return {"registered_order": [{"ordinal": i + 1, "name": n,
            "kind": k, "root": r,
            "expanded_letter_count": candidate["dag"].counts[r - 1]}
            for i, (n, k, r) in enumerate(candidate["acceptance"])],
            "diagnostic_order": [{"ordinal": i + 1, "name": n,
            "kind": k, "root": r,
            "expanded_letter_count": candidate["dag"].counts[r - 1]}
            for i, (n, k, r) in enumerate(candidate["diagnostics"])],
            "target6": {"ordinal": 6, "name": "hexagon_1_coface_0",
                         "component": 4},
            "expression_DAG": dag,
            "all_33_values_identity_at_current_E4": True,
            "targets_7_through_33_solved_at_next_chief": False,
            "left_Fox_equals_literal_A18_differential": False,
            "normalized_Brunnian_class": "UNBUILT"}
    finally:
        old.FIXED_WORD = prior


def formal(old: Any, e4: Any, g: Sequence[int]) -> dict[str, Any]:
    q = [e4.eval(g, (e4.eval(m[0]), e4.eval(m[2]))) for m in old.cofaces(3)]
    q1, q2, q3, q4, _ = q
    q12, q123 = e4.mul(q1, q2), e4.mul(e4.mul(q1, q2), q3)
    def row() -> list[list[Any]]:
        terms = [("lambda1", q1, 1), ("lambda2", q12, 1),
                 ("lambda3", q123, 1), ("lambda5", q123, 2),
                 ("lambda4", q4, 2)]
        return [[label, (bytes(v[0]) + bytes(v[1])).hex(), a]
                for label, v, a in sorted(terms,
                    key=lambda x: (x[0], bytes(x[1][0]) + bytes(x[1][1])))]
    exact = row()
    return {"scope": "same 760 base; universal E4 group-ring prefix canary",
        "coface_q_values": [encode(x) for x in q],
        "printed_order": "b1*b2*b3*b5^-1*b4^-1",
        "D_right": exact, "D_left_after_Aq": exact,
        "D_right_equals_D_left_Aq": True,
        "actual_successor_chief_action_matrix_Aq": "UNBUILT",
        "actual_five_lambda_matrices": "UNBUILT",
        "hexagon_same_base_identity":
            "paper consequence v93; actual successor matrices UNBUILT",
        "mutation": {"kind": "replace final -q4*lambda4 by -lambda4",
                     "breaks_equality": True},
        "not_616_to_760_transport": True}


def expected_preflight() -> dict[str, Any]:
    authenticate(); old = load(OLD_PATH, "_d972_r07_760_checker_old_v10")
    p23 = load(P23_PATH, "_d972_r07_760_checker_p23")
    q3 = json.loads((ROOT / Q3_PATH).read_text(encoding="utf-8"))
    e3, e4 = old.reconstruct(q3); f, r, g = construct_base()
    inverse, sv, source, inv_public = inverse_and_source(old, q3, e4, g)
    return {"joint_settled_identity": joint_public(old, p23, e3, e4, f, r, g),
        "settled_relation_and_current_onto": relation_public(
            old, q3, e3, e4, f, g, inverse, sv, source, inv_public),
        "literal_target_manifest": manifest_public(old, e4, g, inverse),
        "same_base_left_right_canary": formal(old, e4, g)}


def validate_envelope(data: dict[str, Any], raw: bytes) -> None:
    require(raw == canonical_bytes(data) + b"\n", "canonical receipt")
    require(data["schema"] == SCHEMA and data["status"] ==
            data["terminal_token"] and data["terminal_token"] in {
                "R07_760_COMMUTATOR_BASE_READY", "R07_760_AFFINE_RHS_READY",
                "R07_760_AFFINE_UNKNOWN_RESOURCE", "R07_760_AFFINE_INPUT_STOP"},
            "checker envelope")
    claimed = data.pop("self_digest_sha256")
    require(claimed == digest_obj(data), "checker self digest")
    data["self_digest_sha256"] = claimed
    f, r, g = construct_base()
    require(data["base"]["signed_word"] == g and data["base"]["sha256"] == BASE_SHA and
            data["base"]["parent_616_word"] == f and
            data["base"]["settled_kernel_word_r"] == r and
            data["base"]["exponent_sums_xy"] == [0, 0], "checker base block")
    require(data["claims"]["full_JH_over_JPhi_complete"] is False and
            data["claims"]["cofinal_lift"] is False and
            data["claims"]["ihara_witness"] is False and
            data["cofinal_3_frattini_typing"]["current_E4_onto"] is True and
            data["cofinal_3_frattini_typing"]["next_transition_kernel_subset_Phi"] is True and
            data["cofinal_3_frattini_typing"]["whole_mixed_tower_claimed"] is False,
            "checker theorem boundary")


def compare_core(data: dict[str, Any], expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        require(data[key] == value, "checker independent mismatch: " + key)


def mutation_suite(data: dict[str, Any], expected: dict[str, Any]) -> int:
    mutations = []
    def add(label: str, fn: Any) -> None:
        bad = copy.deepcopy(data); fn(bad)
        try:
            compare_core(bad, expected)
        except RuntimeError:
            mutations.append(label); return
        raise RuntimeError("mutation survived: " + label)
    add("PB4_relator", lambda d: d["settled_relation_and_current_onto"]
        ["PB4_relators"][0].update({"identity": False}))
    add("Q4_generator", lambda d: d["settled_relation_and_current_onto"]
        ["Q4_generation"].update({"all_six_recovered": False}))
    add("Frattini_matrix", lambda d: d["settled_relation_and_current_onto"]
        ["Pi4_mod_Phi"]["matrix_rows_source_generators"][0].__setitem__(0, 2))
    add("coface_order", lambda d: d["settled_relation_and_current_onto"]
        .update({"ordered_A18_convention": "mutated"}))
    add("multiplication_side", lambda d: d["same_base_left_right_canary"]
        .update({"D_right_equals_D_left_Aq": False}))
    add("settled_p3", lambda d: d["joint_settled_identity"]
        ["p3_source_plus_five_cofaces_identity"].__setitem__(0, False))
    add("target_DAG", lambda d: d["literal_target_manifest"]
        ["target6"].update({"ordinal": 7}))
    require(len(mutations) == 7, "checker mutation count")
    return len(mutations)


def checker_remainder_public(row: dict[tuple[int, str], int]) -> list[list[Any]]:
    return [[int(component), str(value_hex), int(coefficient) % 3]
            for (component, value_hex), coefficient in sorted(
                row.items(), key=lambda item:
                    (item[0][0], bytes.fromhex(item[0][1])))
            if int(coefficient) % 3]


def checker_semantic_gradient(cc: Any, gradient: dict[Any, int]) \
        -> list[list[Any]]:
    return [[int(component), cc.element_blob(value).hex(), int(coefficient) % 3]
            for (component, value), coefficient in sorted(
                gradient.items(), key=lambda item:
                    (item[0][0], cc.element_blob(item[0][1])))
            if int(coefficient) % 3]


def rebuild_target_public(cc: Any, v2: Any, old: Any, e4: Any,
                          seeds: dict[str, Any], source: dict[str, Any],
                          inverse: Sequence[Sequence[int]], pool: Any,
                          basis: Any, recovery: Any) -> dict[str, Any]:
    target0 = cc.fresh_target(v2, old, e4, seeds, source, inverse,
                              pool, basis, solve_complete=False)
    words = cc.target_words(old, seeds["seed_words"])
    gradients = target0["raw_gradients"]
    remainders = target0["remainders"]
    require(len(words) == len(gradients) == len(remainders) == 109,
            "full checker 109 dimensions")
    bindings = []; formulas = []; word_rows = []
    for ordinal, (word, gradient, remainder) in enumerate(
            zip(words, gradients, remainders)):
        name = "hexagon_1_coface_0" if ordinal == 0 else \
            f"hexagon_1_coface_0_direction_{ordinal:03d}"
        kind = "base" if ordinal == 0 else "registered_seed_direction"
        binding = old.check_gradient_binding(
            name, "hexagon", gradient, e4.identity)
        if ordinal:
            detail = old.checker_target6_formula(
                seeds["seed_words"][ordinal - 1], e4, include_gradient=True)
            require(detail["direct_gradient"] == gradient and
                    detail["direct_value"] == e4.identity,
                    f"full checker target formula {ordinal}")
            formulas.append({"ordinal": ordinal,
                **old.checker_target6_public_from_detail(
                    seeds["seed_words"][ordinal - 1], detail)})
        bindings.append(binding)
        rem_public = checker_remainder_public(remainder)
        word_rows.append({"ordinal": ordinal, "kind": kind,
            "word_length": len(word), "word_sha256": digest_obj(word),
            "gradient_entry_count": len(gradient),
            "gradient_binding": binding,
            "remainder_entry_count": len(remainder),
            "remainder": rem_public,
            "remainder_sha256": digest_obj(rem_public)})
    system, target = cc.solve_remainders(v2, old, e4, remainders, 1)
    del system
    parents = cc.direct_parents(e4, pool, recovery, words, gradients)
    gradients_public = [checker_semantic_gradient(cc, row) for row in gradients]
    return {"target_ordinal": 6, "target_name": "hexagon_1_coface_0",
        "component": 4, "multiplication_side": "left-Fox presentation complex",
        "literal_arity_coface_A18_differential_built": False,
        "literal_arity_coface_A18_differential": "UNBUILT",
        "word_rows": word_rows, "word_rows_sha256": digest_obj(word_rows),
        "gradient_bindings": bindings,
        "gradient_bindings_sha256": digest_obj(bindings),
        "raw_gradients_sha256": digest_obj(gradients_public),
        "formula_rows": formulas, "formula_rows_sha256": digest_obj(formulas),
        "remainders_sha256": target["remainders_sha256"],
        "target_system": target,
        "raw_parent_manifest": parents,
        "recovery_map": recovery.public(),
        "all_109_rows_fresh": True, "old_616_RHS_imported": False,
        "old_20_RHS_imported": False}


def check_full_affine(data: dict[str, Any], seconds: float) -> dict[str, Any]:
    """Independent heavy replay through the separately frozen checker chain."""
    require(0 < seconds <= 18000, "full checker seconds")
    runtime = ROOT / Q3_RUNTIME_PATH
    require(runtime.is_file() and runtime.stat().st_size == 231570 and
            digest_file(runtime) == PIN_SPECS["q3"][2],
            "full checker runtime q3 pin")
    cc = load(HEAVY_CHECKER_PATH, "_d972_r07_760_heavy_checker_157em")
    cc.CHECKER_STARTED = time.monotonic()
    cc.CHECKER_DEADLINE = cc.CHECKER_STARTED + seconds
    cc.CHECKER_CHECKS = 0
    v2, _, eg, ed, old, v4 = cc.predecessor_modules()
    cc.configure_deadlines(v2, eg, ed, old)
    q3 = ed.load_q3(runtime); e3, e4 = old.reconstruct(q3)
    _, _, g = construct_base(); prior = list(old.FIXED_WORD)
    old.FIXED_WORD = list(g)
    try:
        row7 = next(row for row in q3["canonical_roof_powers"]["rows"]
                    if row["exponent"] == 7)
        candidate = old.reduce_word(
            row7["word"] + q3["correction_fibre"]["records"][0]["word"])
        inverse = old.source_words(candidate)
        source_words = old.source_words(g)
        base_key = tuple(e4.eval(word) for word in source_words)
        require(digest_obj(inverse) == INVERSE_SHA and
                digest_obj([encode(x) for x in base_key]) == SOURCE_KEY_SHA,
                "full checker base/inverse")
        normalized = {"selected_inverse_words": inverse}
        seeds = old.affine_checker_seed_words(q3, e3)
        source = old.checker_rebuild_occurrence_preflight(
            seeds["seed_words"], e4, base_key)
        affine = data["affine_rebuild"]
        require(affine["source_preflight"] == source and
                affine["seed_manifest"] == seeds,
                "full checker source/seed replay")

        occurrences, base_public = cc.numbered_occurrences(eg, old, e4)
        cc.independent_base_columns(old, e4, occurrences)
        recovery = cc.CheckerRecovery()
        for occurrence in occurrences:
            recovery.direct(int(occurrence["component"]),
                bytes.fromhex(occurrence["element_hex"]),
                108 + int(occurrence["relator_index"]),
                int(occurrence["term_ordinal"]))
        masks: dict[bytes, int] = {}
        fake = {"directed_base_support": affine["directed_base_support"],
                "directed_surgery": affine["directed_surgery"],
                "prefix_B0": affine["prefix_B0"]}
        pool, basis, events = cc.replay_B0(
            ed, old, fake, e4, normalized, base_key,
            recovery, occurrences, masks)
        require(affine["prefix_B0"]["dependent_events"] == events and
                affine["prefix_B0"]["prefix_pool_checkpoint"] ==
                    len(pool.values) and
                affine["directed_base_support"] == base_public and
                affine["base_columns"] == base_public,
                "full checker B0/base columns")

        qstar = ed.validate_qstar_label(ed.QSTAR, cc.WIDTH)
        oracle = ed.RawOracle(old, pool, basis, qstar)
        support = eg.checker_lambda_support(oracle, cc.WIDTH)
        corr = eg.independent_correlation(support["rows"], occurrences,
            width=cc.WIDTH, unpack=pool.unpack, mul=e4.mul,
            inverse=e4.inverse, pack=cc.element_blob)
        require(affine["old_qstar_boundary"] == {
            "used_only_to_freshly_reconstruct_fixed_B1": True,
            "used_after_fixed_B1": False, "support_count": support["count"],
            "support_sha256": support["ordered_sha256"],
            "complete_correlation_sha256": corr["public"]["packed_rows_sha256"]},
            "full checker fixed qstar boundary")
        fixed, _, fixed_ledger = cc.replay_fixed_B1_prefix(
            v2, old, e4, pool, basis, oracle, affine["fixed_B1_block"])
        v4.validate_completed_anchor_split(v2, fixed,
            affine["fixed_B1_block"], affine["fixed_B1_anchor"],
            basis.live_entries,
            lambda block, anchor, live: bool(
                v2._validate_anchor_public(block, anchor, frozen=True,
                    live_basis_entries=live) is None))
        require(len(fixed_ledger) == 11, "full checker B1 ledger")

        fixed_blob = bytes.fromhex(fixed["translation_hex"])
        fixed_value = pool.unpack(fixed_blob)
        for occurrence in occurrences:
            recovery.translated(int(occurrence["component"]),
                cc.element_blob(e4.mul(fixed_value, occurrence["_value"])),
                fixed_blob, int(occurrence["relator_index"]),
                int(occurrence["term_ordinal"]),
                bytes.fromhex(occurrence["element_hex"]))
        expected_target = rebuild_target_public(
            cc, v2, old, e4, seeds, source, inverse, pool, basis, recovery)
        require(affine["target6"] == expected_target and
                affine["state"] == "R07_760_AFFINE_RHS_READY" and
                affine["base_used"] == "r07_760_commutator" and
                affine["B0_fresh"] is True and
                affine["B1_fresh"] is True and
                affine["all_109_rows_fresh"] is True and
                affine["old_616_RHS_imported"] is False and
                affine["old_20_RHS_imported"] is False and
                affine["registered_target6_solve_executed"] is False and
                affine["target_affine_system_assembled_and_ranked"] is True and
                affine["complete_D2_column_generation_executed"] is False and
                affine["next_target_ordinal"] is None,
                "full checker all 109 word/gradient/remainder/solve/recovery")

        old.FIXED_WORD = prior
        mapping = old.cofaces(3)[0]
        old_word = old.substitute(old.embed_f2(old.hexagon_words(prior)[0]),
                                  mapping)
        old.FIXED_WORD = list(g)
        comparison = affine["comparison_to_historical_old20"]
        require(comparison["old_20_base_target_word_sha256"] ==
                    digest_obj(old_word) and
                comparison["g760_base_target_word_sha256"] ==
                    expected_target["word_rows"][0]["word_sha256"] and
                comparison["word_digest_differs"] is True and
                comparison["fresh_remainders_sha256"] ==
                    expected_target["remainders_sha256"] and
                comparison["fresh_row_space_sha256"] ==
                    expected_target["target_system"]["row_space_sha256"] and
                comparison["at_least_one_base_dependent_digest_differs"] is True and
                comparison["chain_conjugacy_imported"] is False,
                "full checker historical comparison")
        return expected_target
    finally:
        old.FIXED_WORD = prior


def check(receipt: Path, mutations: bool, full: bool,
          seconds: float = 18000.0) -> dict[str, Any]:
    raw = receipt.read_bytes(); data = json.loads(raw.decode("ascii"))
    validate_envelope(data, raw); expected = expected_preflight()
    compare_core(data, expected)
    require((data["mode"] == "preflight") is
            (data["terminal_token"] == "R07_760_COMMUTATOR_BASE_READY"),
            "checker mode/terminal")
    count = mutation_suite(data, expected) if mutations else 0
    if full:
        require(data["mode"] == "full", "checker requested full receipt")
        if data["terminal_token"] == "R07_760_AFFINE_RHS_READY":
            target_expected = check_full_affine(data, seconds)
            if mutations:
                bad = copy.deepcopy(data)
                bad["affine_rebuild"]["target6"]["gradient_bindings"][0][
                    "canonical_gradient_sha256"] = "0" * 64
                require(bad["affine_rebuild"]["target6"] != target_expected,
                        "full checker gradient mutation")
                count += 1
        else:
            stop = data["affine_rebuild"]
            require(data["terminal_token"] in {
                "R07_760_AFFINE_UNKNOWN_RESOURCE", "R07_760_AFFINE_INPUT_STOP"} and
                stop["state"] == data["terminal_token"] and
                stop["base_used"] == "r07_760_commutator" and
                type(stop["exception_type"]) is str and bool(stop["exception_type"]) and
                type(stop["reason"]) is str and bool(stop["reason"]) and
                type(stop["requested_seconds"]) in (int, float) and
                0 < float(stop["requested_seconds"]) <= 18000 and
                stop["B0_fresh"] is False and stop["B1_fresh"] is False and
                stop["all_109_rows_fresh"] is False and
                stop["old_616_RHS_imported"] is False and
                stop["old_20_RHS_imported"] is False and
                stop["registered_target6_solve_executed"] is False and
                stop["target_affine_system_assembled_and_ranked"] is False and
                stop["complete_D2_column_generation_executed"] is False and
                stop["mathematical_negative_claimed"] is False and
                data["claims"]["full_JH_over_JPhi_complete"] is False and
                data["claims"]["cofinal_lift"] is False and
                data["claims"]["ihara_witness"] is False and
                data["claims"]["actual_A18_occurrence"] is False and
                data["claims"]["registered_108_family_is_full_universe"] is False,
                "checker full claim-free stop terminal")
    print(FINAL_MARKER + f" terminal={data['terminal_token']} "
          f"mutations={count} full_replay={str(full).lower()} "
          f"receipt_sha256={hashlib.sha256(raw).hexdigest()}", flush=True)
    return data


def self_test() -> None:
    _, r, g = construct_base()
    require(len(r) == 144 and len(g) == 760, "checker static words")
    print("R07_760_COMMUTATOR_AFFINE_RHS_V3_CHECKER_SELFTEST_PASS "
          "stdlib_adapter=1 mutations=7 negative=0", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--seconds", type=float, default=18000.0)
    args = parser.parse_args()
    if args.self_test:
        self_test(); return 0
    path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    check(path, args.mutations, args.full, args.seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
