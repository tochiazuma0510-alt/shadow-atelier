#!/usr/bin/env python3
"""R07 760-letter commutator rebase and fresh affine-RHS producer v3.

The local ``--preflight`` lane is finite and bounded.  It reconstructs the
literal base, the settled joint identity, the current E4 onto certificate,
the corrected Def. 2.9 target DAG, and the same-base left/right canary.  The
``--full`` lane additionally rebuilds B0, B1 and all 109 target-6 rows; it is
intended for one GHA process and is never required by the local preflight.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-616-to-760-commutator-affine-rhs/v3"
FINAL_MARKER = "R07_760_COMMUTATOR_AFFINE_RHS_V3_PRODUCER_PASS"
DEFAULT_PREFLIGHT = Path(
    "search/certs/d972_r07_616_to_760_commutator_affine_rhs_"
    "preflight_v3_20260826.json")
DEFAULT_FULL = Path("ci/out/d972_r07_616_to_760_commutator_affine_rhs_v3.json")

TERMINALS = {
    "R07_760_COMMUTATOR_BASE_READY",
    "R07_760_AFFINE_RHS_READY",
    "R07_760_TARGET6_REGISTERED_CORRECTION_PASS",
    "R07_760_TARGET6_REGISTERED_FULL_D2_SEPARATOR",
    "R07_760_AFFINE_UNKNOWN_RESOURCE",
    "R07_760_AFFINE_INPUT_STOP",
}

PARENT_SHA = "3680e8bcbac37747467175454b082485b2ae296f1fb05244435d8f44979d4e90"
BASE_SHA = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
INVERSE_SHA = "7d49ed8811f661031077b45d7fd6fab2eb21fdef308486367dc8981d0918879e"
SOURCE_KEY_SHA = "59ae54aedb638b5cf69d76ba4d838c94a1c6412af89689f6709af4350e5ef0a2"
Q4_ORDER = "583152628325845597028352"
Q4_AB_ORDER = 32

Q3_PATH = Path(
    "ci/b345_157dp_artifacts_32171982444/d972_b345_q3_chief_v1.json")
Q3_RUNTIME_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
LEGACY_PATH = Path("search/d972_b345_relfrat3_wordexpr_memo_v9.py")
P23_PATH = Path("crosscheck/check_d972_r07_p23_joint_literal_v1.py")
EM_PATH = Path("search/d972_b345_target6_dual_colgen_v1.py")

PIN_SPECS: dict[str, tuple[Path, int, str]] = {
    "task_v3": (Path("sol/luna_task_162_r07_760_commutator_affine_rhs_v3.md"),
        4053, "8ca38afc6f30e8e6074f191a17541f508f29ba1da58d3b286ba4fcf33406ae21"),
    "proof_v88": (Path("sol/proof_r07_goursat_nakayama_onto_v88.md"),
        4254, "e0d8ff49963ef0cb98312e5ee288ed0744a42fd7d2dd6e0b8450439e28fe329b"),
    "audit_v89": (Path("sol/audit_r07_616_e4_relation_onto_v89.md"),
        4388, "0b965baa8bade54c3e3784df64fdfe6f440824518f2c21174e26122f452d4244"),
    "proof_v92": (Path("sol/proof_r07_joint_derived_commutator_rebase_v92.md"),
        5969, "cc56e2187fac08ffa70fe3753e200627e776b5fa591738dee5da908e4d217387"),
    "proof_v93": (Path("sol/proof_r07_left_right_a18_basechange_v93.md"),
        4578, "5adc49196b7ac0c9d7472f5de0c77af9919b945304f6732e8ea182899308660e"),
    "proof_v94": (Path("sol/proof_r07_frattini_invisible_onto_stability_v94.md"),
        6506, "fee0868727bc027d002d19200a73ac0292d76bb04d95e88553cbfa0e29942840"),
    "q3_artifact": (Q3_PATH, 231570,
        "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "legacy_v9": (LEGACY_PATH, 392086,
        "7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f"),
    "p23_independent": (P23_PATH, 32201,
        "56f479bbb17b0a7aa756ce79ce02dcccab5236b67ea85f90a90830f97e389bc2"),
    "target6_157em": (EM_PATH, 410757,
        "8a3dd09811ec790b90f5f3d16890e9ef534a9fc0399597a0daa892605c58c8fc"),
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


def pin_inputs() -> dict[str, Any]:
    rows = {}
    for label, (path, size, digest) in PIN_SPECS.items():
        full = ROOT / path
        require(full.is_file(), f"missing pin: {path.as_posix()}")
        require(full.stat().st_size == size, f"byte drift: {path.as_posix()}")
        require(digest_file(full) == digest, f"SHA drift: {path.as_posix()}")
        rows[label] = {"path": path.as_posix(), "bytes": size,
                       "sha256": digest}
    return rows


def load_pinned(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None, "module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(name, None)
        raise
    return module


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(type(letter) is int and letter in (-2, -1, 1, 2),
                "signed F2 alphabet")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inv_word(word: Sequence[int]) -> list[int]:
    return [-letter for letter in reversed(word)]


def substitute(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    return reduce_word(letter for x in word for letter in
        (images[abs(x)-1] if x > 0 else inv_word(images[abs(x)-1])))


def exponent_sums(word: Sequence[int]) -> list[int]:
    return [sum(1 if x == i else -1 if x == -i else 0 for x in word)
            for i in (1, 2)]


def construct_base() -> tuple[list[int], list[int], list[int]]:
    discrepancy_inverse = reduce_word(inv_word(W3) + list(W2))
    f = reduce_word(list(W2) + discrepancy_inverse * 8)
    r = [1] * 108 + [-2] * 36
    g = reduce_word(f + inv_word(r))
    require(len(f) == 616 and digest_obj(f) == PARENT_SHA and
            exponent_sums(f) == [108, -36], "parent 616 pin")
    require(len(r) == 144 and exponent_sums(r) == [108, -36], "r pin")
    require(len(g) == 760 and digest_obj(g) == BASE_SHA and
            exponent_sums(g) == [0, 0], "base 760 pin")
    return f, r, g


def encode_element(value: Any) -> dict[str, Any]:
    row = {"coarse_one_line": [int(x) + 1 for x in value[0]],
           "fine_pc_coords": list(value[1])}
    row["sha256"] = digest_obj(row)
    return row


def product(q: Any, values: Sequence[Any]) -> Any:
    out = q.identity
    for value in values:
        out = q.mul(out, value)
    return out


def rank_mod3(matrix: Sequence[Sequence[int]]) -> int:
    rows = [[int(x) % 3 for x in row] for row in matrix]
    rank = 0
    for col in range(len(rows[0]) if rows else 0):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        if rows[rank][col] == 2:
            rows[rank] = [(2 * x) % 3 for x in rows[rank]]
        for i, row in enumerate(rows):
            if i != rank and row[col]:
                a = row[col]
                rows[i] = [(x - a * y) % 3 for x, y in zip(row, rows[rank])]
        rank += 1
    return rank


def inverse_data(old: Any, q3: dict[str, Any], e4: Any,
                 base: Sequence[int]) -> tuple[dict[str, Any], list[list[int]],
                                                list[Any], list[list[int]]]:
    row7 = next(row for row in q3["canonical_roof_powers"]["rows"]
                if row["exponent"] == 7)
    records = q3["correction_fibre"]["records"]
    require(len(records) == 27, "authenticated inverse fibre width")
    candidate = old.reduce_word(row7["word"] + records[0]["word"])
    inverse_words = old.source_words_m0(candidate)
    source_words = old.source_words_m0(base)
    source_values = [e4.eval(word) for word in source_words]
    inverse_values = [e4.eval(word) for word in inverse_words]
    st = [e4.mul(e4.eval(inverse_words[i], source_values),
                 e4.inverse(e4.generators[i])) for i in range(6)]
    ts = [e4.mul(e4.eval(source_words[i], inverse_values),
                 e4.inverse(e4.generators[i])) for i in range(6)]
    require(all(value == e4.identity for value in st + ts),
            "direct E4 two-sided inverse")
    require(digest_obj(inverse_words) == INVERSE_SHA, "inverse tuple SHA")
    encoded_source = [encode_element(value) for value in source_values]
    require(digest_obj(encoded_source) == SOURCE_KEY_SHA, "source key SHA")
    public = {
        "normalized_exponent": 7,
        "selected_correction_index_one_based": 1,
        "candidate_word": candidate,
        "candidate_word_sha256": digest_obj(candidate),
        "inverse_words": inverse_words,
        "inverse_word_lengths": list(map(len, inverse_words)),
        "inverse_words_sha256": digest_obj(inverse_words),
        "source_words": source_words,
        "source_words_sha256": digest_obj(source_words),
        "source_key": encoded_source,
        "source_key_sha256": digest_obj(encoded_source),
        "ST_values": [encode_element(value) for value in st],
        "TS_values": [encode_element(value) for value in ts],
        "all_twelve_identity": True,
    }
    return public, inverse_words, source_values, source_words


def joint_identity(old: Any, p23: Any, q3: dict[str, Any], e3: Any, e4: Any,
                   f: Sequence[int], r: Sequence[int], g: Sequence[int]) \
        -> dict[str, Any]:
    context3 = [e3.generators[0], e3.generators[2]]
    contexts4 = [(e4.eval(mapping[0]), e4.eval(mapping[2]))
                 for mapping in old.cofaces(3)]
    e3_r = e3.eval(r, context3)
    e4_r = [e4.eval(r, context) for context in contexts4]
    require(e3_r == e3.identity and all(x == e4.identity for x in e4_r),
            "r complete E3/E4 identity")
    require(e3.eval(f, context3) == e3.eval(g, context3) and
            all(e4.eval(f, c) == e4.eval(g, c) for c in contexts4),
            "f/g complete settled equality")

    g36_r = p23.evaluate_generic(r, p23.G36_ONE, (p23.X36, p23.Y36),
                                 p23.g36_mul, p23.g36_inv)
    psl_r = p23.evaluate_generic(r, p23.MATRIX_ONE,
                                 (p23.X_PSL, p23.Y_PSL),
                                 p23.matrix_mul, p23.matrix_inv)
    require(g36_r == p23.G36_ONE and psl_r == p23.MATRIX_ONE,
            "r G36/PSL identity")

    source2 = p23.JenningsD4(2, 2, ())
    source3 = p23.JenningsD4(3, 2, ())
    pb42 = p23.JenningsD4(2, 6, p23.PB4_RELATORS)
    pb43 = p23.JenningsD4(3, 6, p23.PB4_RELATORS)
    key2 = p23.relation_key(source2, pb42, r)
    key3 = p23.relation_key(source3, pb43, r)
    require(all(x == source2.one for x in key2[:1]) and
            all(x == pb42.one for x in key2[1:]) and
            all(x == source3.one for x in key3[:1]) and
            all(x == pb43.one for x in key3[1:]), "r p2/p3 joint identity")

    mutant = list(r); mutant[0] = 2
    mutant_g36 = p23.evaluate_generic(mutant, p23.G36_ONE,
        (p23.X36, p23.Y36), p23.g36_mul, p23.g36_inv)
    mutant_psl = p23.evaluate_generic(mutant, p23.MATRIX_ONE,
        (p23.X_PSL, p23.Y_PSL), p23.matrix_mul, p23.matrix_inv)
    require(mutant_g36 != p23.G36_ONE or mutant_psl != p23.MATRIX_ONE,
            "joint r mutation detected")
    return {
        "r_definition": "x^108*y^-36",
        "r_word": list(r), "r_word_sha256": digest_obj(r),
        "complete_E3_source": encode_element(e3_r),
        "complete_E4_five_cofaces": [encode_element(x) for x in e4_r],
        "G36_value": [[int(a), int(b)] for a, b in g36_r],
        "PSL2_8_identity": psl_r == p23.MATRIX_ONE,
        "p2_source_plus_five_cofaces_identity": [x == source2.one
            for x in key2[:1]] + [x == pb42.one for x in key2[1:]],
        "p3_source_plus_five_cofaces_identity": [x == source3.one
            for x in key3[:1]] + [x == pb43.one for x in key3[1:]],
        "p2_coordinate_sha256": digest_obj([list(source2.coords(key2[0]))] +
            [list(pb42.coords(x)) for x in key2[1:]]),
        "p3_coordinate_sha256": digest_obj([list(source3.coords(key3[0]))] +
            [list(pb43.coords(x)) for x in key3[1:]]),
        "f_equals_g_on_all_settled_constituents": True,
        "diagonal_joint_correlation_remaining": False,
        "mutated_r_first_letter": {
            "mutant": 2, "G36_identity": mutant_g36 == p23.G36_ONE,
            "PSL2_8_identity": mutant_psl == p23.MATRIX_ONE,
            "rejected": True,
        },
    }


def relation_and_onto(old: Any, q3: dict[str, Any], e3: Any, e4: Any,
                      f: Sequence[int], g: Sequence[int]) \
        -> tuple[dict[str, Any], list[list[int]], list[Any], list[list[int]]]:
    inverse, inverse_words, source_values, source_words = inverse_data(
        old, q3, e4, g)
    f_values = [e4.eval(word) for word in old.source_words_m0(f)]
    require(f_values == source_values, "616/760 source tuple equality")
    relators = old.pure_relations(4)
    rel_values = [e4.eval(word, source_values) for word in relators]
    require(len(relators) == 11 and all(x == e4.identity for x in rel_values),
            "eleven PB4 relators")
    coarse_recovery = [old.eval_perm_word(word, [x[0] for x in source_values])
                       for word in inverse_words]
    require(coarse_recovery == [x[0] for x in e4.generators],
            "Q4 marked-generator recovery")
    matrix = [list(value[1][:6]) for value in source_values]
    require(rank_mod3(matrix) == 6, "Pi4 Frattini rank")
    require(q3["groups"]["PB4"]["generator_count"] == 10 and
            q3["groups"]["PB4"]["order_decimal"] == "59049" and
            q3["coarse_models"]["Q4"]["order_decimal"] == Q4_ORDER,
            "direct-product finite pins")

    context3 = [e3.generators[0], e3.generators[2]]
    hex_words = old.hexagon_words(g)
    hex_values = [e3.eval(word, context3) for word in hex_words]
    pent = old.pentagon_word(g)
    pent_value = e4.eval(pent)
    require(hex_values == [e3.identity, e3.identity] and
            pent_value == e4.identity, "760 literal relations")
    return ({
        "two_hexagon_words": [{"length": len(word),
            "sha256": digest_obj(word)} for word in hex_words],
        "two_hexagon_values": [encode_element(x) for x in hex_values],
        "ordered_A18_word": {"length": len(pent), "sha256": digest_obj(pent)},
        "ordered_A18_value": encode_element(pent_value),
        "ordered_A18_convention": "native F*E*C*B^-1*A^-1; slots C,A,E,B,F",
        "R07_mark_replayed": True,
        "inverse": inverse,
        "PB4_relators": [{"ordinal": i + 1, "word_sha256": digest_obj(word),
            "value": encode_element(value), "identity": True}
            for i, (word, value) in enumerate(zip(relators, rel_values))],
        "Q4_generation": {
            "method": "six inverse words recover all six marked Q4 generators",
            "recovered_generator_sha256": digest_obj(
                [[int(x) + 1 for x in value] for value in coarse_recovery]),
            "all_six_recovered": True, "Q4_order_decimal": Q4_ORDER,
        },
        "Pi4_mod_Phi": {
            "basis": ["a12", "a13", "a14", "a23", "a24", "a34"],
            "matrix_rows_source_generators": matrix,
            "rank_F3": 6, "full_span": True,
        },
        "direct_product": {
            "ambient": "E4=Q4xPi4[3]", "authenticated": True,
            "Q4_abelianization_order": Q4_AB_ORDER,
            "three_divides_Q4_ab_order": False,
        },
        "current_E4_onto": True,
        "current_E4_source_endomorphism_automorphism": True,
        "grade": "candidate; prior v89 subclaim cross-checked",
    }, inverse_words, source_values, source_words)


def target_manifest(old: Any, e4: Any, g: Sequence[int],
                    inverse_words: Sequence[Sequence[int]]) -> dict[str, Any]:
    prior = list(old.FIXED_WORD)
    old.FIXED_WORD = list(g)
    try:
        candidate = old.build_wordexpr_candidate(0, [], inverse_words)
        named = [(name, root) for name, _, root in
                 candidate["acceptance"] + candidate["diagnostics"]]
        payload = candidate["dag"].serialize_reachable(named)
        evaluator = old.WordExprEvaluator(candidate["dag"], e4,
            {"base_kind": "r07_760_commutator", "correction": []})
        values = evaluator.evaluate_values()
        acceptance_identity = [values[root - 1] == e4.identity
                               for _, _, root in candidate["acceptance"]]
        require(len(acceptance_identity) == 33 and all(acceptance_identity),
                "33 acceptance target values")
        return {
            "registered_order": [{"ordinal": i + 1, "name": name,
                "kind": kind, "root": root,
                "expanded_letter_count": candidate["dag"].expanded_count[root - 1]}
                for i, (name, kind, root) in enumerate(candidate["acceptance"])],
            "diagnostic_order": [{"ordinal": i + 1, "name": name,
                "kind": kind, "root": root,
                "expanded_letter_count": candidate["dag"].expanded_count[root - 1]}
                for i, (name, kind, root) in enumerate(candidate["diagnostics"])],
            "target6": {"ordinal": 6, "name": "hexagon_1_coface_0",
                         "component": 4},
            "expression_DAG": payload,
            "all_33_values_identity_at_current_E4": True,
            "targets_7_through_33_solved_at_next_chief": False,
            "left_Fox_equals_literal_A18_differential": False,
            "normalized_Brunnian_class": "UNBUILT",
        }
    finally:
        old.FIXED_WORD = prior


def formal_vector_public(row: dict[tuple[str, bytes], int]) -> list[list[Any]]:
    return [[label, blob.hex(), coefficient]
            for (label, blob), coefficient in sorted(row.items())
            if coefficient % 3]


def add_formal(row: dict[tuple[str, bytes], int], label: str,
               value: Any, coefficient: int) -> None:
    key = (label, bytes(value[0]) + bytes(value[1]))
    new = (row.get(key, 0) + coefficient) % 3
    if new:
        row[key] = new
    else:
        row.pop(key, None)


def left_right_canary(old: Any, e4: Any, g: Sequence[int]) -> dict[str, Any]:
    contexts = [(e4.eval(mapping[0]), e4.eval(mapping[2]))
                for mapping in old.cofaces(3)]
    q = [e4.eval(g, context) for context in contexts]
    q1, q2, q3, q4, q5 = q
    q12 = e4.mul(q1, q2); q123 = e4.mul(q12, q3)
    left_aq: dict[tuple[str, bytes], int] = {}
    right: dict[tuple[str, bytes], int] = {}
    for row, terms in ((left_aq, (("lambda1", q1, 1),
                                  ("lambda2", q12, 1),
                                  ("lambda3", q123, 1),
                                  ("lambda5", q123, 2),
                                  ("lambda4", q4, 2))),
                       (right, (("lambda1", q1, 1),
                                ("lambda2", q12, 1),
                                ("lambda3", q123, 1),
                                ("lambda5", q123, 2),
                                ("lambda4", q4, 2)))):
        for label, value, coefficient in terms:
            add_formal(row, label, value, coefficient)
    require(left_aq == right, "formal D_R=D_L A_q")
    mutant = dict(right)
    mutant.pop(next(key for key in mutant if key[0] == "lambda4"))
    add_formal(mutant, "lambda4", e4.identity, 2)
    require(mutant != left_aq, "side-prefix mutation detected")
    return {
        "scope": "same 760 base; universal E4 group-ring prefix canary",
        "coface_q_values": [encode_element(x) for x in q],
        "printed_order": "b1*b2*b3*b5^-1*b4^-1",
        "D_right": formal_vector_public(right),
        "D_left_after_Aq": formal_vector_public(left_aq),
        "D_right_equals_D_left_Aq": True,
        "actual_successor_chief_action_matrix_Aq": "UNBUILT",
        "actual_five_lambda_matrices": "UNBUILT",
        "hexagon_same_base_identity": "paper consequence v93; actual successor matrices UNBUILT",
        "mutation": {"kind": "replace final -q4*lambda4 by -lambda4",
                     "breaks_equality": True},
        "not_616_to_760_transport": True,
    }


def claims(status: str) -> dict[str, Any]:
    return {
        "terminal": status,
        "full_JH_over_JPhi_complete": False,
        "cofinal_lift": False,
        "ihara_witness": False,
        "actual_A18_occurrence": False,
        "registered_108_family_is_full_universe": False,
        # build_full enters its typed heavy try only after build_preflight has
        # reconstructed this finite certificate.  A later runtime-input stop
        # does not erase the already checked current-E4 statement.
        "current_E4_onto": True,
        "cofinal_3_primary_onto_paper_consequence": True,
        "whole_mixed_tower_onto": False,
    }


def build_preflight() -> tuple[dict[str, Any], dict[str, Any]]:
    pins = pin_inputs()
    old = load_pinned(LEGACY_PATH, "_d972_r07_760_preflight_legacy_v9")
    p23 = load_pinned(P23_PATH, "_d972_r07_760_preflight_p23")
    q3 = json.loads((ROOT / Q3_PATH).read_text(encoding="utf-8"))
    require(q3["schema"] == "d972-b345-q-chief/v1", "q3 schema")
    e3, e4, _ = old.reconstruct_quotients(q3)
    f, r, g = construct_base()
    joint = joint_identity(old, p23, q3, e3, e4, f, r, g)
    relation, inverse_words, source_values, source_words = relation_and_onto(
        old, q3, e3, e4, f, g)
    manifest = target_manifest(old, e4, g, inverse_words)
    side = left_right_canary(old, e4, g)
    status = "R07_760_COMMUTATOR_BASE_READY"
    receipt: dict[str, Any] = {
        "schema": SCHEMA, "date": "20260826", "mode": "preflight",
        "status": status, "terminal_token": status,
        "pins": pins,
        "base": {
            "base_kind": "r07_760_commutator",
            "construction": "g=f*y^36*x^-108=f*(x^108*y^-36)^-1",
            "parent_616_word": f, "parent_616_length": len(f),
            "parent_616_sha256": digest_obj(f),
            "settled_kernel_word_r": r, "settled_kernel_word_r_sha256": digest_obj(r),
            "signed_word": g, "length": len(g), "sha256": digest_obj(g),
            "exponent_sums_xy": exponent_sums(g),
            "raw_commutator_subgroup_membership": True,
        },
        "joint_settled_identity": joint,
        "settled_relation_and_current_onto": relation,
        "cofinal_3_frattini_typing": {
            "current_E4_onto": True,
            "P0": "Pi4[3]", "P0_mod_Phi_dimension_F3": 6,
            "Q4_abelianization_order": Q4_AB_ORDER,
            "next_transition_category":
                "finite marked 3-group PB4 quotients mapping onto P0",
            "next_transition_kernel_subset_Phi": True,
            "all_transitions_in_category_kernel_subset_Phi": True,
            "category_cofinal_among_finite_marked_3_group_quotients": True,
            "basis": "paper theorem v94 Theorem 3.1 plus finite pins above",
            "cofinal_3_primary_onto": True,
            "whole_mixed_tower_claimed": False,
        },
        "same_base_left_right_canary": side,
        "literal_target_manifest": manifest,
        "affine_rebuild": {
            "state": "UNBUILT_GHA_ONLY", "base_used": "r07_760_commutator",
            "B0_fresh": False, "B1_fresh": False,
            "all_109_rows_fresh": False, "old_616_RHS_imported": False,
            "old_20_RHS_imported": False,
        },
        "mutations": {
            "PB4_relator": {"ordinal": 1, "checker_must_reject": True},
            "Q4_generator_image": {"ordinal": 1, "checker_must_reject": True},
            "Pi4_mod_Phi_entry": {"row": 1, "column": 1,
                                   "checker_must_reject": True},
            "coface_sign_order": {"target": "ordered_A18",
                                    "checker_must_reject": True},
            "multiplication_side": {"expected": "right via D_L*A_q",
                                     "checker_must_reject": True},
            "base_hash": {"expected": BASE_SHA, "checker_must_reject": True},
            "target6_raw_gradient": {"available_only_full": True,
                                     "checker_must_reject": True},
            "settled_p_value": {"prime": 3, "slot": 0,
                                 "checker_must_reject": True},
        },
        "claims": claims(status),
    }
    receipt["self_digest_sha256"] = digest_obj(receipt)
    private = {"q3": q3, "old": old, "e3": e3, "e4": e4,
               "f": f, "r": r, "g": g, "inverse_words": inverse_words,
               "source_values": source_values, "source_words": source_words}
    return receipt, private


def semantic_gradient_public(em: Any, gradient: dict[Any, int]) -> list[list[Any]]:
    return [[int(component), em.element_blob(value).hex(), int(coefficient) % 3]
            for (component, value), coefficient in sorted(
                gradient.items(), key=lambda item:
                    (item[0][0], em.element_blob(item[0][1])))
            if int(coefficient) % 3]


def remainder_public(row: dict[tuple[int, str], int]) -> list[list[Any]]:
    return [[int(component), str(value_hex), int(coefficient) % 3]
            for (component, value_hex), coefficient in sorted(
                row.items(), key=lambda item:
                    (item[0][0], bytes.fromhex(item[0][1])))
            if int(coefficient) % 3]


def fresh_target_rhs(em: Any, ei: Any, old: Any, e4: Any,
                     seed_words: Sequence[Sequence[int]],
                     prefix: dict[str, Any], anchor_ids: Sequence[int],
                     recovery: Any, monitor: Any) -> dict[str, Any]:
    """Build all 109 g760 rows without calling the old-base target wrapper."""
    words = em.target6_words(old, seed_words)
    adapter = monitor.bind("initial_target")
    gradients: list[dict[Any, int]] = []
    remainders: list[dict[tuple[int, str], int]] = []
    bindings: list[dict[str, Any]] = []
    formulas: list[dict[str, Any]] = []
    word_rows: list[dict[str, Any]] = []
    for ordinal, word in enumerate(words):
        adapter.check("initial_target", force=(ordinal == 0 or ordinal % 4 == 0))
        gradient, value = old.fox_gradient_without_sections(word, e4)
        require(value == e4.identity, f"fresh target value {ordinal}")
        name = "hexagon_1_coface_0" if ordinal == 0 else \
            f"hexagon_1_coface_0_direction_{ordinal:03d}"
        kind = "base" if ordinal == 0 else "registered_seed_direction"
        binding = old.raw_gradient_binding(name, "hexagon", gradient, value)
        if ordinal:
            detail = old.affine_target6_formula(
                seed_words[ordinal - 1], e4, include_gradient=True)
            direct = detail.pop("_direct_gradient")
            direct_value = detail.pop("_direct_value")
            require(direct == gradient and direct_value == e4.identity and
                    detail["formula_equals_direct"] is True,
                    f"fresh target formula {ordinal}")
            formulas.append({"ordinal": ordinal, **detail})
        remainder = old._affine_probe_remainder(
            gradient, prefix, anchor_ids, adapter)
        gradients.append(dict(gradient)); remainders.append(dict(remainder))
        bindings.append(binding)
        word_rows.append({"ordinal": ordinal, "kind": kind,
            "word_length": len(word), "word_sha256": digest_obj(word),
            "gradient_entry_count": len(gradient),
            "gradient_binding": binding,
            "remainder_entry_count": len(remainder),
            "remainder": remainder_public(remainder),
            "remainder_sha256": digest_obj(remainder_public(remainder))})
    require(len(words) == len(gradients) == len(remainders) == 109 and
            len(formulas) == 108, "fresh 109 row dimensions")
    system, solve = em.solve_from_remainders(
        ei, old, e4, remainders, monitor, 1)
    target = em.target_public(system, remainders, 1)
    require(solve["affine_system"]["row_space_sha256"] ==
            target["row_space_sha256"], "fresh target solve equality")
    parent_manifest = em.add_direct_parents(
        old, e4, prefix["pool"], recovery, words, gradients)
    gradients_public = [semantic_gradient_public(em, row) for row in gradients]
    return {
        "target_ordinal": 6, "target_name": "hexagon_1_coface_0",
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
        "raw_parent_manifest": parent_manifest,
        "recovery_map": recovery.public(),
        "all_109_rows_fresh": True,
        "old_616_RHS_imported": False,
        "old_20_RHS_imported": False,
    }


def heavy_affine_rebuild(private: dict[str, Any], seconds: float) -> dict[str, Any]:
    """Enter the authenticated 157em generic core with g760 as FIXED_WORD."""
    runtime_q3 = ROOT / Q3_RUNTIME_PATH
    require(runtime_q3.is_file() and runtime_q3.stat().st_size == 231570 and
            digest_file(runtime_q3) == PIN_SPECS["q3_artifact"][2],
            "full mode requires exact q3 artifact at ci/out runtime path")
    em = load_pinned(EM_PATH, "_d972_r07_760_target6_em_v1")
    monitor = em.Monitor(seconds)
    ei = em.load_ei(); eh = ei.load_eh(); eg = eh.load_v1(); ed = eg.load_ed()
    q3, old = ed.authenticated_input(runtime_q3)
    e3, e4, _ = old.reconstruct_quotients(q3)
    require(e4.degree == 144 and e4.pc.n == 10, "full E4 dimensions")
    g = list(private["g"])
    prior = list(old.FIXED_WORD); old.FIXED_WORD = g
    try:
        source_words = old.source_words_m0(g)
        raw_source_key = tuple(e4.eval(word) for word in source_words)
        require(digest_obj([encode_element(x) for x in raw_source_key]) ==
                SOURCE_KEY_SHA, "full source key bridge")
        row7 = next(row for row in q3["canonical_roof_powers"]["rows"]
                    if row["exponent"] == 7)
        inverse_candidate = old.reduce_word(
            row7["word"] + q3["correction_fibre"]["records"][0]["word"])
        inverse_words = old.source_words_m0(inverse_candidate)
        require(digest_obj(inverse_words) == INVERSE_SHA,
                "full inverse reconstruction")
        seed_info = old.affine_seed_words(q3, e3)
        require(len(seed_info["seed_words"]) == 108 and
                digest_obj(seed_info["seed_words"]) == ei.SEED_MANIFEST_SHA,
                "full seed manifest")
        source_preflight = em.source_preflight(
            old, seed_info["seed_words"], e4, raw_source_key,
            inverse_words, monitor)

        recovery = em.RecoveryMap(monitor)
        prefix, dependent = em.build_prefix_with_recovery(
            old, ed, e4, raw_source_key, monitor, recovery)
        prefix_public = ei._prefix_public(old, prefix, dependent, ed)
        prefix_public["complete_block_registry"] = \
            prefix["_em_complete_block_public"]
        fixed = em.construct_fixed_B1(
            ei, old, ed, eg, e4, prefix, dependent, recovery, monitor)
        fixed_anchor = {key: value for key, value in fixed["anchor"].items()
                        if not key.startswith("_")}
        rhs = fresh_target_rhs(em, ei, old, e4, seed_info["seed_words"],
            prefix, fixed["anchor"]["_ids"], recovery, monitor)

        current_word_sha = rhs["word_rows"][0]["word_sha256"]
        # The saved prior is the old 20-letter base.  Compute its target word
        # only as a comparison diagnostic, never as RHS transport.
        old.FIXED_WORD = prior
        historical_mapping = old.cofaces(3)[0]
        historical_word = old.word_substitute(
            old.embed_f2_pb3(old.hexagon_words(prior)[0]),
            historical_mapping)
        old.FIXED_WORD = g
        comparison = {
            "old_20_base_target_word_sha256": digest_obj(historical_word),
            "g760_base_target_word_sha256": current_word_sha,
            "word_digest_differs": digest_obj(historical_word) != current_word_sha,
            "historical_remainders_sha256": em.B1["fresh_remainders_sha256"],
            "fresh_remainders_sha256": rhs["remainders_sha256"],
            "remainder_digest_differs":
                rhs["remainders_sha256"] != em.B1["fresh_remainders_sha256"],
            "historical_row_space_sha256": em.B1["target_row_space_sha256"],
            "fresh_row_space_sha256": rhs["target_system"]["row_space_sha256"],
            "row_space_digest_differs": rhs["target_system"]["row_space_sha256"] !=
                em.B1["target_row_space_sha256"],
            "at_least_one_base_dependent_digest_differs": False,
            "chain_conjugacy_imported": False,
        }
        comparison["at_least_one_base_dependent_digest_differs"] = any(
            comparison[key] for key in ("word_digest_differs",
                "remainder_digest_differs", "row_space_digest_differs"))
        require(comparison["at_least_one_base_dependent_digest_differs"],
                "fresh base-dependent digest integrity")
        return {
            "state": "R07_760_AFFINE_RHS_READY",
            "base_used": "r07_760_commutator",
            "source_preflight": source_preflight,
            "seed_manifest": seed_info,
            "directed_base_support": prefix["directed_base_support"],
            "directed_surgery": prefix["directed_surgery"],
            "prefix_B0": prefix_public,
            "base_columns": fixed["bundle"]["public"],
            "fixed_B1_block": fixed["block"],
            "fixed_B1_anchor": fixed_anchor,
            "old_qstar_boundary": fixed["old_qstar_provenance"],
            "target6": rhs,
            "comparison_to_historical_old20": comparison,
            "B0_fresh": True, "B1_fresh": True,
            "all_109_rows_fresh": True,
            "old_616_RHS_imported": False, "old_20_RHS_imported": False,
            "registered_target6_solve_executed": False,
            "target_affine_system_assembled_and_ranked": True,
            "complete_D2_column_generation_executed": False,
            "next_target_ordinal": None,
        }
    finally:
        old.FIXED_WORD = prior


def build_full(seconds: float) -> dict[str, Any]:
    receipt, private = build_preflight()
    receipt["mode"] = "full"
    try:
        receipt["affine_rebuild"] = heavy_affine_rebuild(private, seconds)
        receipt["status"] = receipt["terminal_token"] = \
            "R07_760_AFFINE_RHS_READY"
    except Exception as exc:
        resource = ("Resource" in type(exc).__name__ or
                    hasattr(exc, "cap_key") or hasattr(exc, "observed_count"))
        # A typed invariant/input mismatch is a claim-free INPUT_STOP.  Do not
        # turn programming defects (AttributeError, TypeError, KeyError, ...)
        # into a successful terminal envelope.
        if not resource and not isinstance(exc, RuntimeError):
            raise
        token = ("R07_760_AFFINE_UNKNOWN_RESOURCE" if resource else
                 "R07_760_AFFINE_INPUT_STOP")
        receipt["status"] = receipt["terminal_token"] = token
        receipt["affine_rebuild"] = {
            "state": token, "base_used": "r07_760_commutator",
            "exception_type": type(exc).__name__,
            "reason": str(getattr(exc, "key", "")) or type(exc).__name__,
            "requested_seconds": seconds,
            "B0_fresh": False, "B1_fresh": False,
            "all_109_rows_fresh": False, "old_616_RHS_imported": False,
            "old_20_RHS_imported": False,
            "registered_target6_solve_executed": False,
            "target_affine_system_assembled_and_ranked": False,
            "complete_D2_column_generation_executed": False,
            "mathematical_negative_claimed": False,
        }
    receipt["claims"] = claims(receipt["terminal_token"])
    receipt.pop("self_digest_sha256")
    receipt["self_digest_sha256"] = digest_obj(receipt)
    del private
    return receipt


def validate_receipt(receipt: dict[str, Any]) -> None:
    require(receipt["schema"] == SCHEMA and
            receipt["terminal_token"] == receipt["status"] in TERMINALS,
            "receipt envelope")
    claimed = receipt.pop("self_digest_sha256")
    require(claimed == digest_obj(receipt), "receipt self digest")
    receipt["self_digest_sha256"] = claimed
    require(receipt["base"]["base_kind"] == "r07_760_commutator" and
            receipt["base"]["sha256"] == BASE_SHA and
            receipt["base"]["exponent_sums_xy"] == [0, 0], "receipt base")
    require(receipt["claims"]["full_JH_over_JPhi_complete"] is False and
            receipt["claims"]["cofinal_lift"] is False and
            receipt["claims"]["ihara_witness"] is False,
            "receipt negative boundary")


def checked_write(path: Path, receipt: dict[str, Any]) -> bytes:
    validate_receipt(receipt)
    raw = canonical_bytes(receipt) + b"\n"
    full = path if path.is_absolute() else ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    if full.exists():
        require(full.read_bytes() == raw, "immutable output mismatch")
    else:
        full.write_bytes(raw)
    require(full.read_bytes() == raw, "checked readback")
    return raw


def self_test() -> None:
    f, r, g = construct_base()
    require(reduce_word(g + r + inv_word(f)) == [], "g*r=f free identity")
    require(claims("R07_760_COMMUTATOR_BASE_READY")["cofinal_lift"] is False,
            "claim boundary")
    print("R07_760_COMMUTATOR_AFFINE_RHS_V3_PRODUCER_SELFTEST_PASS "
          "base=760 terminals=6 negative=0", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--preflight", action="store_true")
    modes.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seconds", type=float, default=18000.0)
    args = parser.parse_args()
    if args.self_test:
        self_test(); return 0
    receipt = build_full(args.seconds) if args.full else build_preflight()[0]
    output = args.output or (DEFAULT_FULL if args.full else DEFAULT_PREFLIGHT)
    raw = checked_write(output, receipt)
    print(FINAL_MARKER + f" terminal={receipt['terminal_token']} "
          f"sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
