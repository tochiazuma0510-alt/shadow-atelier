#!/usr/bin/env python3
"""Independent checker for the total-linking C3 chief descent."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


SCHEMA = "d972-b34-total-linking-c3-chief/v1"
PASS = "B34_TOTAL_LINKING_C3_CHIEF_DESCENT_CROSSCHECKED"
REJECT = "B34_TOTAL_LINKING_C3_CANDIDATE_REJECTED_CROSSCHECKED"
UNKNOWN_INPUT = "B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_INPUT"
UNKNOWN_RESOURCE = "B34_TOTAL_LINKING_C3_CHIEF_UNKNOWN_RESOURCE"
Q3_PATH = Path("ci/out/d972_b345_q3_chief_v1.json")
FC8_PATH = Path("ci/out/d972_b4_fc8_a5four_v1.json")
DP_PATH = Path("ci/out/d972_b34_a5_selected_lift_v1.json")
WORDS_PATH = Path("search/certs/d972_b4_word_key_artifact_v1_20260816.json")
AXIS_PATH = Path("sol/luna_reply_157cp_c5_surgery_torsor_chief.md")
T48_PATH = Path("docs/notes/t48_157dp_answer_v1.md")
OLD_PRODUCER = Path("search/d972_b34_a5_selected_lift_v1.g")
OLD_CHECKER = Path("search/check_d972_b34_a5_selected_lift_v1.py")
OLD_DRIVER = Path("search/d972_b34_a5_selected_lift_gha_driver_v1.g")
Q3_CHECKER = Path("search/check_d972_b345_q3_chief_v1.py")
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
FC8_SHA = "558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584"
DP_SHA = "d3cb729d972a1b460cd8f0a76b49cd6abf4eafd7fe0c112ad0ad742de5200157"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
AXIS_SHA = "59c96e7d62a20af4207f715df8e2927a8fc373e1f12e8f3be70e535d8afe5347"
T48_SHA = "c90ffc1684f44b17602d55769cc18c8197300ed6477c4501d63455ec40c97dcc"
OLD_PRODUCER_SHA = "9fb5fa16cd913ba559e96a0431cf6be4b902f1dedff289ab7e5e3d6c9adb6500"
OLD_CHECKER_SHA = "2d30b1458725cb70d94cb4ab35256988bf23cc2d796a422d3f0b14d1c2f6805e"
OLD_DRIVER_SHA = "cce2dff8e4a96046d97f70f64a31f279ced5feeeb08dca55de82b59f7154171e"
Q3_CHECKER_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
FIELDS = {
    "schema", "status", "terminal_token", "terminal", "pins",
    "marked_abelian_lattice", "candidate_binding", "literal_residuals",
    "a5_intersection", "order_certificate", "outside_certificate",
    "claim_boundary", "performance", "provenance", "runtime_ms",
}


class CheckError(RuntimeError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise CheckError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest_obj(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def digest_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise CheckError(f"{label}: actual_sha={digest_obj(actual)} "
                         f"expected_sha={digest_obj(expected)}")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"module spec {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path, expected: str) -> dict[str, Any]:
    require(digest_file(path) == expected, f"artifact SHA {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def word_pp(base: Any, words: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for word in reversed(words):
        out = base.reduce_word(out + list(word))
    return out


def exponent_sums(word: Sequence[int], width: int) -> list[int]:
    return [sum(1 if x > 0 else -1 for x in word if abs(x) == j)
            for j in range(1, width + 1)]


def exponent_matrix(words: Sequence[Sequence[int]], width: int) -> list[list[int]]:
    return [exponent_sums(word, width) for word in words]


def source_words(base: Any, f: Sequence[int]) -> list[list[int]]:
    ff = base.substitute(f, [[1], [4]])
    g = base.substitute(f, [[1], [2]])
    gs = base.substitute(f, [[4], [5]])
    f1234 = base.substitute(f, [[4, 2], [6]])
    h = base.substitute(f, [[2, 1], [3]])
    middle = base.substitute(f, [[2, 1], [6, 5]])
    return [
        [1],
        base.reduce_word(base.inv_word(g) + [2] + g),
        base.reduce_word(base.inv_word(ff) + base.inv_word(h) + [3] + h + ff),
        base.reduce_word(base.inv_word(ff) + [4] + ff),
        base.reduce_word(base.inv_word(ff) + base.inv_word(middle) +
                         base.inv_word(gs) + [5] + gs + middle + ff),
        base.reduce_word(base.inv_word(f1234) + [6] + f1234),
    ]


def hexagon_words(base: Any, f: Sequence[int]) -> list[list[int]]:
    x, y = [1], [3]
    z = base.inv_word(word_pp(base, [x, y]))
    u = base.inv_word(word_pp(base, [y, x]))
    contexts = [[x, y], [x, z], [y, z], [u, x], [u, y]]
    values = [base.substitute(f, pair) for pair in contexts]
    return [word_pp(base, [values[0], base.inv_word(values[1]), values[2]]),
            word_pp(base, [base.inv_word(values[3]), base.inv_word(values[0]),
                            values[4]])]


def pentagon_word(base: Any, f: Sequence[int]) -> list[int]:
    g = [[i] for i in range(1, 7)]
    contexts = [[g[0], g[3]], [g[3], g[5]],
                [word_pp(base, [g[1], g[3]]), g[5]],
                [word_pp(base, [g[0], g[1]]), word_pp(base, [g[4], g[5]])],
                [g[0], word_pp(base, [g[3], g[4]])]]
    values = [base.substitute(f, pair) for pair in contexts]
    return word_pp(base, [base.inv_word(word_pp(base, [values[4], values[2]])),
                          values[1], values[3], values[0]])


def rank_mod(matrix: Sequence[Sequence[int]], prime: int) -> int:
    a = [[x % prime for x in row] for row in matrix]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, prime)
        a[row] = [(inv * x) % prime for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [(x - scale * y) % prime for x, y in zip(a[i], a[row])]
        row += 1
    return row


def det_bareiss(matrix: Sequence[Sequence[int]]) -> int:
    a = [list(row) for row in matrix]
    n = len(a)
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        require(pivot is not None, "singular lattice basis")
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // previous
        previous = a[k][k]
    return sign * a[-1][-1]


def perm_row(p: Sequence[int]) -> list[int]:
    return [x + 1 for x in p]


def pc_marked(q3: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return q3["groups"][key]["marked_generators"]


def pb4_record(base: Any, name: str, word: Sequence[int], q4marks: Sequence[Any],
               pc4: Any, marked4: Sequence[dict[str, Any]]) -> dict[str, Any]:
    w = base.reduce_word(word)
    qv = base.eval_word(w, q4marks, base.one(144), base.mul, base.inv)
    pv = base.pc_eval(w, marked4, pc4)
    ell = sum(1 if x > 0 else -1 for x in w)
    passed = qv == base.one(144) and pv == pc4.zero() and ell == 0
    return {"name": name, "word": w, "word_sha256": digest_obj(w),
            "q4_row": perm_row(qv), "pi4_coords": list(pv),
            "total_linking": ell, "c18_residue": ell % 18,
            "q4_identity": qv == base.one(144), "pi4_identity": pv == pc4.zero(),
            "pass": passed}


def pb3_record(base: Any, name: str, word: Sequence[int], cofaces: Sequence[Any],
               q4marks: Sequence[Any], pc4: Any,
               marked4: Sequence[dict[str, Any]]) -> dict[str, Any]:
    w = base.reduce_word(word)
    lifts = [pb4_record(base, f"{name}.coface{i + 1}",
                        base.substitute(w, cofaces[i]), q4marks, pc4, marked4)
             for i in range(5)]
    return {"name": name, "pb3_word": w, "pb3_word_sha256": digest_obj(w),
            "five_coface_lifts": lifts, "pass": all(x["pass"] for x in lifts)}


def e3_record(base: Any, name: str, word: Sequence[int], q0marks: Sequence[Any],
              pc3: Any, marked3: Sequence[dict[str, Any]], cofaces: Sequence[Any],
              q4marks: Sequence[Any], pc4: Any,
              marked4: Sequence[dict[str, Any]]) -> dict[str, Any]:
    w = base.reduce_word(word)
    qv = base.eval_word(w, q0marks, base.one(36), base.mul, base.inv)
    f2 = base.f2_marked_generators(marked3)
    pv = base.eval_word(w, [tuple(x["coords"]) for x in f2], pc3.zero(),
                        pc3.mul, pc3.inverse)
    return {"name": name, "word": w, "word_sha256": digest_obj(w),
            "exponent_sums": exponent_sums(w, 2), "q0_row": perm_row(qv),
            "pi3_coords": list(pv),
            "E3_identity": qv == base.one(36) and pv == pc3.zero(),
            "finer_five_cofaces": pb3_record(base, f"{name}.finer", w, cofaces,
                                                q4marks, pc4, marked4)}


def all_words_pass(base: Any, words: Sequence[Sequence[int]], q4marks: Sequence[Any],
                   pc4: Any, marked4: Sequence[dict[str, Any]]) -> bool:
    return all(pb4_record(base, "canary", w, q4marks, pc4, marked4)["pass"]
               for w in words)


def find_inverse(base: Any, q3: dict[str, Any], s_words: Sequence[Sequence[int]],
                 relations: Sequence[Sequence[int]], q4marks: Sequence[Any],
                 pc4: Any, marked4: Sequence[dict[str, Any]]) -> dict[str, Any]:
    row = next((x for x in q3["canonical_roof_powers"]["rows"]
                if x["exponent"] == 7), None)
    require(row is not None, "normalized exponent-seven row")
    records = q3["correction_fibre"]["records"]
    for index, correction in enumerate(records, 1):
        word = base.reduce_word(row["word"] + correction["word"])
        t_words = source_words(base, word)
        rel_words = [base.substitute(rel, t_words) for rel in relations]
        st = [base.reduce_word(base.substitute(t_words[i], s_words) + [-(i + 1)])
              for i in range(6)]
        ts = [base.reduce_word(base.substitute(s_words[i], t_words) + [-(i + 1)])
              for i in range(6)]
        if (all_words_pass(base, rel_words, q4marks, pc4, marked4) and
                all_words_pass(base, st, q4marks, pc4, marked4) and
                all_words_pass(base, ts, q4marks, pc4, marked4)):
            return {"normalized_exponent": 7, "roof_row_index": row["row_index"],
                    "correction_index": index, "word": word, "source_words": t_words,
                    "relation_words": rel_words, "ST_words": st, "TS_words": ts,
                    "found": True, "attempted": index, "cap": len(records),
                    "word_sha256": digest_obj(word), "word_length": len(word)}
    return {"found": False, "attempted": len(records), "cap": len(records)}


def source_words3(source6: Sequence[Sequence[int]]) -> list[list[int]]:
    """Typed restriction [12,13,14,23,24,34] -> [12,13,23]."""
    keep = [1, 2, 4]
    out: list[list[int]] = []
    for word in [source6[i - 1] for i in keep]:
        require(all(abs(x) in keep for x in word), "PB3 source restriction")
        out.append([(1 if x > 0 else -1) * (keep.index(abs(x)) + 1) for x in word])
    return out


def pb3_five_component_onto(base: Any, q3: dict[str, Any], s_words: Sequence[Any],
                            t_words: Sequence[Any], q4marks: Sequence[Any],
                            pc4: Any, marked4: Sequence[dict[str, Any]]) -> dict[str, Any]:
    cofaces = base.cofaces(3)
    relations = q3["formulas"]["presentations"]["PB3"]["relations"]
    s3, t3 = source_words3(s_words), source_words3(t_words)
    st3 = [base.reduce_word(base.substitute(t3[i], s3) + [-(i + 1)])
           for i in range(3)]
    ts3 = [base.reduce_word(base.substitute(s3[i], t3) + [-(i + 1)])
           for i in range(3)]
    components, tuple_components, all_records = [], [], []
    pi4marks = [tuple(row["coords"]) for row in marked4]
    for index, coface in enumerate(cofaces, 1):
        qg = [base.eval_word(w, q4marks, base.one(144), base.mul, base.inv)
              for w in coface]
        pg = [base.eval_word(w, pi4marks, pc4.zero(), pc4.mul, pc4.inverse)
              for w in coface]
        cg = [sum(1 if x > 0 else -1 for x in w) % 18 for w in coface]

        def images(words: Sequence[Sequence[int]]) -> tuple[list[Any], list[Any], list[int]]:
            lifted = [base.substitute(w, coface) for w in words]
            return ([base.eval_word(w, q4marks, base.one(144), base.mul, base.inv)
                     for w in lifted],
                    [base.eval_word(w, pi4marks, pc4.zero(), pc4.mul, pc4.inverse)
                     for w in lifted],
                    [sum(1 if x > 0 else -1 for x in w) % 18 for w in lifted])

        qs, ps, cs = images(s3)
        qt, pt, ct = images(t3)
        sinter = [pb4_record(
            base, f"PB3.component{index}.S.intertwining.{j + 1}",
            base.reduce_word(base.substitute(s3[j], coface) +
                             base.inv_word(base.substitute(coface[j], s_words))),
            q4marks, pc4, marked4) for j in range(3)]
        tinter = [pb4_record(
            base, f"PB3.component{index}.T.intertwining.{j + 1}",
            base.reduce_word(base.substitute(t3[j], coface) +
                             base.inv_word(base.substitute(coface[j], t_words))),
            q4marks, pc4, marked4) for j in range(3)]
        srels = [pb4_record(base, f"PB3.component{index}.S.relation.{j + 1}",
                            base.substitute(base.substitute(rel, s3), coface),
                            q4marks, pc4, marked4) for j, rel in enumerate(relations)]
        trels = [pb4_record(base, f"PB3.component{index}.T.relation.{j + 1}",
                            base.substitute(base.substitute(rel, t3), coface),
                            q4marks, pc4, marked4) for j, rel in enumerate(relations)]
        st = [pb4_record(base, f"PB3.component{index}.ST.generator.{j + 1}",
                         base.substitute(word, coface), q4marks, pc4, marked4)
              for j, word in enumerate(st3)]
        ts = [pb4_record(base, f"PB3.component{index}.TS.generator.{j + 1}",
                         base.substitute(word, coface), q4marks, pc4, marked4)
              for j, word in enumerate(ts3)]
        records = sinter + tinter + srels + trels + st + ts
        all_records.extend(records)
        tuple_components.extend([
            (qg, base.one(144), base.mul, base.inv, 1000),
            (pg, pc4.zero(), pc4.mul, pc4.inverse, 1000),
            (cg, 0, lambda a, b: (a + b) % 18, lambda a: (-a) % 18, 18)])
        components.append({
            "coface_index": index, "coface_words": coface,
            "original": {"q4_rows": [perm_row(x) for x in qg],
                         "pi4_coords": [list(x) for x in pg], "c18_residues": cg},
            "S_images": {"q4_rows": [perm_row(x) for x in qs],
                         "pi4_coords": [list(x) for x in ps], "c18_residues": cs},
            "T_images": {"q4_rows": [perm_row(x) for x in qt],
                         "pi4_coords": [list(x) for x in pt], "c18_residues": ct},
            "S_global_intertwining_residuals": sinter,
            "T_global_intertwining_residuals": tinter,
            "S_relation_residuals": srels,
            "T_relation_residuals": trels, "ST_generator_residuals": st,
            "TS_generator_residuals": ts,
            "pass": all(row["pass"] for row in records)})
    words = [[1], [3], [1, 2, 3]]
    return {"source_generator_order": ["x12", "x13", "x23"],
            "S_source_words": s3, "T_source_words": t3, "components": components,
            "actual_joint_tuple_N_ord": tuple_nord(base, words, tuple_components),
            "global_E4_C18_automorphism_restricted_by_intertwining": True,
            "joint_coupling_handled_without_character_rank_assumption": True,
            "component_intertwining_residuals": 5 * 2 * 3,
            "residual_count": len(all_records),
            "all_pass": all(row["pass"] for row in components) and
                        all(row["pass"] for row in all_records)}


def source_residuals(base: Any, q3mod: Any, q3: dict[str, Any], candidate: Sequence[int],
                     base_word: Sequence[int], q4marks: Sequence[Any], pc3: Any,
                     pc4: Any) -> dict[str, Any]:
    cofaces = base.cofaces(3)
    require(q3["formulas"]["cofaces_3_4"] == cofaces, "coface formula")
    relations = q3["formulas"]["presentations"]["PB4"]["relations"]
    marked4, marked3 = pc_marked(q3, "PB4"), pc_marked(q3, "PB3")
    s_words, s0_words = source_words(base, candidate), source_words(base, base_word)
    diffs = [pb4_record(base, f"FC30.source_difference.{i + 1}",
                        base.reduce_word(s_words[i] + base.inv_word(s0_words[i])),
                        q4marks, pc4, marked4) for i in range(6)]
    settlement = q3["selected_solution"]["settlement"]
    require(settlement["source_words"] == s0_words and settlement["Q4_bijective"] is True and
            settlement["Pi4_q3_bijective"] is True, "q3 settlement binding")
    qimages = [base.eval_word(w, q4marks, base.one(144), base.mul, base.inv)
               for w in s_words]
    pimages = [base.pc_eval(w, marked4, pc4) for w in s_words]
    qinvok = all(base.eval_word(w, qimages, base.one(144), base.mul, base.inv) ==
                 q4marks[i] for i, w in enumerate(settlement["Q4_inverse_words"]))
    pinvok = all(base.eval_word(w, pimages, pc4.zero(), pc4.mul, pc4.inverse) ==
                 tuple(marked4[i]["coords"])
                 for i, w in enumerate(settlement["Pi4_inverse_words"]))
    q3mod.validate_inverse_pc_maps(pc4, settlement["Pi4_forward_pc_images"],
                                   settlement["Pi4_inverse_pc_images"])
    authentication = {
        "upstream_settlement_sha256": digest_obj(settlement),
        "q3_source_words_equal_base": True,
        "candidate_E4_images_equal_base": all(x["pass"] for x in diffs),
        "Q4_bijective_authenticated": settlement["Q4_bijective"],
        "Pi4_bijective_authenticated": settlement["Pi4_q3_bijective"],
        "Q4_inverse_words": settlement["Q4_inverse_words"],
        "Pi4_inverse_words": settlement["Pi4_inverse_words"],
        "Q4_inverse_word_replay": qinvok, "Pi4_inverse_word_replay": pinvok,
        "Pi4_forward_inverse_sha256": digest_obj(
            [settlement["Pi4_forward_pc_images"], settlement["Pi4_inverse_pc_images"]]),
        "Pi4_pc_two_sided_replay": True, "upstream_same_job_checker_required": True,
        "pass": all(x["pass"] for x in diffs) and qinvok and pinvok,
    }
    hexes = [pb3_record(base, f"hexagon.{i + 1}", word, cofaces, q4marks,
                        pc4, marked4)
             for i, word in enumerate(hexagon_words(base, candidate))]
    pent = pb4_record(base, "A18.ordered_pentagon", pentagon_word(base, candidate),
                      q4marks, pc4, marked4)
    srels = [pb4_record(base, f"S.relation.{i + 1}",
                        base.substitute(rel, s_words), q4marks, pc4, marked4)
             for i, rel in enumerate(relations)]
    inverse = find_inverse(base, q3, s_words, relations, q4marks, pc4, marked4)
    t_words = inverse.get("source_words", [])
    trels = ([pb4_record(base, f"T.relation.{i + 1}", word, q4marks, pc4, marked4)
              for i, word in enumerate(inverse["relation_words"])] if inverse["found"] else [])
    st = ([pb4_record(base, f"ST.generator.{i + 1}", word, q4marks, pc4, marked4)
           for i, word in enumerate(inverse["ST_words"])] if inverse["found"] else [])
    ts = ([pb4_record(base, f"TS.generator.{i + 1}", word, q4marks, pc4, marked4)
           for i, word in enumerate(inverse["TS_words"])] if inverse["found"] else [])
    pb3onto = (pb3_five_component_onto(base, q3, s_words, t_words, q4marks,
                                       pc4, marked4) if inverse["found"] else
               {"source_generator_order": ["x12", "x13", "x23"],
                "S_source_words": [], "T_source_words": [], "components": [],
                "actual_joint_tuple_N_ord": None,
                "global_E4_C18_automorphism_restricted_by_intertwining": False,
                "joint_coupling_handled_without_character_rank_assumption": False,
                "component_intertwining_residuals": 0, "residual_count": 0,
                "all_pass": False})
    chars = [[sum(1 if x > 0 else -1 for x in word) for word in mapping]
             for mapping in cofaces]
    require(chars == [[1, 1, 1], [2, 2, 1], [2, 1, 2], [1, 2, 2], [1, 1, 1]],
            "five total-linking character rows")
    chars_s = [[sum(1 if x > 0 else -1
                    for x in base.substitute(word, s_words)) for word in mapping]
               for mapping in cofaces]
    chars_t = ([[sum(1 if x > 0 else -1
                     for x in base.substitute(word, t_words)) for word in mapping]
                for mapping in cofaces] if inverse["found"] else [])
    records = diffs + srels + trels + st + ts + [pent]
    for row in hexes:
        records.extend(row["five_coface_lifts"])
    expected = {"S_source_words": s_words, "S_exponent_matrix": exponent_matrix(s_words, 6),
                "T_inverse_binding": inverse, "T_source_words": t_words,
                "T_exponent_matrix": exponent_matrix(t_words, 6) if inverse["found"] else [],
                 "authenticated_E4_automorphism": authentication,
                "PB3_five_component_onto": pb3onto,
                "source_difference_FC30": diffs, "hexagons": hexes, "pentagon": pent,
                "S_relation_residuals": srels, "T_relation_residuals": trels,
                "ST_generator_residuals": st, "TS_generator_residuals": ts,
                "five_character_replay": {
                    "original_integer_rows": chars,
                    "rows_mod3": [[x % 3 for x in row] for row in chars],
                    "formal_rank_mod3": rank_mod(chars, 3), "F2_columns": [1, 3],
                    "F2_formal_rank_mod3": rank_mod([[row[0] % 3, row[2] % 3]
                                                      for row in chars], 3),
                    "rank_is_diagnostic_not_joint_image_theorem": True,
                    "S_integer_rows": chars_s, "T_integer_rows": chars_t,
                    "S_preserves_all_five": chars_s == chars,
                    "T_preserves_all_five": chars_t == chars,
                },
                "residual_count": len(records) + pb3onto["residual_count"],
                "residual_digest_sha256": digest_obj({
                    "diffs": diffs, "hex": hexes, "pent": pent,
                    "S": srels, "T": trels, "ST": st, "TS": ts,
                    "PB3": pb3onto}),
                "all_pass": (authentication["pass"] and inverse["found"] and
                             pb3onto["all_pass"] and
                             all(x["pass"] for x in records) and
                             all(x["pass"] for x in hexes) and chars_s == chars and
                             chars_t == chars and exponent_matrix(s_words, 6) ==
                             [[int(i == j) for j in range(6)] for i in range(6)] and
                             exponent_matrix(t_words, 6) ==
                             [[int(i == j) for j in range(6)] for i in range(6)])}
    return expected


def h9_lattice(base: Any, q3mod: Any, q3: dict[str, Any], pc4: Any,
               fc: dict[str, Any]) -> dict[str, Any]:
    gmarks = [base.perm(row) for row in q3["coarse_models"]["G9"]["marked_permutations"]]
    gx, gy = gmarks
    gz = base.inv(base.pp([gx, gy], base.one(27), base.mul))
    ggroup, _ = base.enumerate_group(gmarks, 2917)
    require(len(ggroup) == 2916, "G9 order")
    derived = base.derived_set(gmarks, 729, 2917)
    deletions = base.deletions(4)
    require(q3["formulas"]["deletions_4_3"] == deletions, "deletion formula")
    blocks = [[base.eval_word(deletions[i][j], [gx, gz, gy], base.one(27),
                              base.mul, base.inv) for i in range(4)] for j in range(6)]
    hrows = [base.block(row) for row in blocks]
    expected_hrows = [base.perm(row) for row in
                      q3["coarse_models"]["H9"]["marked_permutations"]]
    require(hrows == expected_hrows, "H9 reconstructed marks")
    reps = [base.one(27), gx, gy, base.mul(gx, gy)]
    bits = [(0, 0), (1, 0), (0, 1), (1, 1)]
    require(all(base.mul(reps[i], base.inv(reps[j])) not in derived
                for i in range(4) for j in range(i)), "G9 quotient basis")

    def quotient_bit(value: Any) -> tuple[int, int]:
        matches = [bits[i] for i, rep in enumerate(reps)
                   if base.mul(value, base.inv(rep)) in derived]
        require(len(matches) == 1, "G9 quotient coordinate")
        return matches[0]

    matrix = [[] for _ in range(8)]
    for row in blocks:
        for i, value in enumerate(row):
            bit = quotient_bit(value)
            matrix[2 * i].append(bit[0])
            matrix[2 * i + 1].append(bit[1])
    kernel = [list(v) for v in itertools.product(range(2), repeat=6)
              if all(sum(a * b for a, b in zip(row, v)) % 2 == 0 for row in matrix)]
    expected_matrix = [
        [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 0], [0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0],
    ]
    require(matrix == expected_matrix and rank_mod(matrix, 2) == 5 and
            kernel == [[0] * 6, [1] * 6], "H9 binary matrix")
    nak = q3mod.independent_h9_nakayama(hrows, gmarks)
    require(nak["mod3_span_rank"] == 12, "H9 derived Nakayama")
    gate = q3["short_common_quotient_gate"]["H9"]
    require(int(gate["order_decimal"]) == 32 * 3 ** 24 and
            int(gate["derived_order_decimal"]) == 3 ** 24 and
            gate["quotient_order"] == 32, "H9 order receipt")
    marked_coords = [row["coords"] for row in q3["groups"]["PB4"]["marked_generators"]]
    pi_matrix = [row[:6] for row in marked_coords]
    pi_derived = base.pc_derived([tuple(row) for row in marked_coords], pc4, 3 ** 4)
    require(pi_matrix == [[int(i == j) for j in range(6)] for i in range(6)] and
            len(pi_derived) == 3 ** 4, "Pi4 Frattini quotient")
    residues = [list(v) for v in itertools.product(range(6), repeat=6)
                if all(x % 3 == 0 for x in v) and
                len({(x // 3) % 2 for x in v}) == 1]
    basis = [[6 * int(i == j) for j in range(6)] for i in range(5)] + [[3] * 6]
    sums = [sum(row) for row in basis]
    require(residues == [[0] * 6, [3] * 6] and abs(det_bareiss(basis)) == 23328 and
            math.gcd(*sums) == 6, "integral lattice")
    pairs = base.pairs(4)
    vertex = [[2, 1, 3, 4], [1, 3, 2, 4], [1, 2, 4, 3]]
    edge: list[list[int]] = []
    for v in vertex:
        row = []
        for i, j in pairs:
            target = sorted([v[i - 1], v[j - 1]])
            row.append(pairs.index(target) + 1)
        edge.append(row)
    require(len(base.enumerate_group([base.perm(x) for x in edge], 25)[0]) == 24,
            "natural S4 edge action")
    edge_perms = [base.perm(x) for x in edge]
    require(base.mul(base.mul(edge_perms[0], edge_perms[1]), edge_perms[0]) ==
            base.mul(base.mul(edge_perms[1], edge_perms[0]), edge_perms[1]) and
            base.mul(base.mul(edge_perms[1], edge_perms[2]), edge_perms[1]) ==
            base.mul(base.mul(edge_perms[2], edge_perms[1]), edge_perms[2]) and
            base.mul(edge_perms[0], edge_perms[2]) == base.mul(edge_perms[2], edge_perms[0]),
            "edge braid action")
    artin = [row["source_generator_images"] for row in fc["b4_action"]["generators"]]
    require(artin == [
        [[1], [-1, 4, 1], [-1, 5, 1], [2], [3], [6]],
        [[-4, 2, 4], [1], [3], [4], [-4, 6, 4], [5]],
        [[1], [-6, 3, 6], [2], [-6, 5, 6], [4], [6]]], "Artin source words")
    inverse_artin = [
        [[1], [4], [5], [1, 2, -1], [1, 3, -1], [6]],
        [[2], [4, 1, -4], [3], [4], [6], [4, 5, -4]],
        [[1], [3], [6, 2, -6], [5], [6, 4, -6], [6]]]
    q4marks = [base.perm(row) for row in q3["coarse_models"]["Q4"]["marked_permutations"]]
    marked4 = q3["groups"]["PB4"]["marked_generators"]
    relations = q3["formulas"]["presentations"]["PB4"]["relations"]

    def target_identity(word: Sequence[int]) -> bool:
        return (base.eval_word(word, q4marks, base.one(144), base.mul, base.inv) ==
                base.one(144) and base.pc_eval(word, marked4, pc4) == pc4.zero())

    target_ok = True
    for forward, backward in zip(artin, inverse_artin):
        target_ok &= all(target_identity(base.substitute(rel, forward)) for rel in relations)
        target_ok &= all(target_identity(base.substitute(rel, backward)) for rel in relations)
        target_ok &= all(target_identity(base.reduce_word(
            base.substitute(forward[i], backward) + [-(i + 1)])) for i in range(6))
        target_ok &= all(target_identity(base.reduce_word(
            base.substitute(backward[i], forward) + [-(i + 1)])) for i in range(6))
    action_matrices = [exponent_matrix(row, 6) for row in artin]
    require(target_ok and all(action_matrices[k][j][edge[k][j] - 1] == 1 and
                              sum(action_matrices[k][j]) == 1
                              for k in range(3) for j in range(6)),
            "H-normal E4 Artin replay")
    return {
        "tuple_order": ["x12", "x13", "x14", "x23", "x24", "x34"],
        "H9": {"deletion_maps": deletions,
               "reconstructed_marked_blocks": [[perm_row(x) for x in row] for row in blocks],
               "binary_matrix_row_order": ["d1_x", "d1_y", "d2_x", "d2_y",
                                            "d3_x", "d3_y", "d4_x", "d4_y"],
               "binary_matrix": matrix, "rank_F2": 5, "kernel_F2": kernel,
               "image_order": 32, "G9_order": 2916, "G9_derived_order": 729,
               "H9_order_decimal": str(32 * 3 ** 24),
               "H9_derived_order_decimal": str(3 ** 24),
               "H9_abelianization_order": 32, "actual_marked_reconstruction": True,
               "derived_calls": 2},
        "Pi4": {"marked_coordinates": marked_coords, "frattini_matrix": pi_matrix,
                "rank_F3": 6, "group_order": 3 ** 10,
                "derived_order": 3 ** 4, "abelianization_order": 3 ** 6},
        "integral_lattice": {
            "congruence": "v=3w and w mod2 is 0 or (1,1,1,1,1,1)",
            "residue_box_modulus": 6, "residue_box_size": 6 ** 6,
            "residue_solutions": residues, "canonical_basis_rows": basis,
            "determinant": 23328, "index": 23328, "basis_linking_sums": sums,
            "gcd_total_linking": 6, "ell_H": "6Z",
            "exact_sequence": "im(H -> PB4_ab)=ker(PB4_ab -> E4_ab)",
            "no_claim_A12_power_itself_in_H": True},
        "beta": {"definition": "beta(h)=ell(h)/6 mod3", "onto": True,
                 "image_order": 3,
                 "kernel": "Kbeta=H intersection ker(ell mod18)",
                 "Phi3_H_subset_Kbeta": True},
        "B4_action": {"vertex_adjacent_transpositions": vertex,
                      "edge_permutations": edge, "action_group_order": 24,
                      "total_linking_preserved": True, "beta_preserved": True,
                      "induced_braid_relations": True, "artin_source_words": artin,
                      "inverse_artin_source_words": inverse_artin,
                      "artin_abelian_matrices": action_matrices,
                      "E4_relation_and_two_sided_replay": target_ok,
                      "H_normal_frozen_typing": True, "Kbeta_normal_B4": True,
                      "chief_factor_order": 3, "chief_by_prime_order": True}}


def candidate_binding(base: Any, q3: dict[str, Any], dp: dict[str, Any], q0marks: Any,
                      pc3: Any, pc4: Any, q4marks: Any) -> tuple[dict[str, Any], list[int]]:
    records, generators = dp["source_fibre"]["section_records"], \
        dp["source_fibre"]["tracked_normal_generators"]
    correction = base.expand_section(124, records, generators)
    chain, index = [], 124
    while index != 1:
        chain.append(index)
        row = records[index - 1]
        require(1 <= row["parent"] < index, "section DAG")
        index = row["parent"]
    chain.append(1)
    base_word = q3["selected_solution"]["typed_source_word"]
    candidate = base.reduce_word(base_word + correction)
    require(dp["scan"]["selected"]["typed_source_word"] == candidate and
            dp["scan"]["selected"]["a5_correction_word"] == correction and
            chain == [124, 45, 16, 5, 1] and len(candidate) == 92 and
            digest_obj(candidate) ==
            "c113c06d51480c8c819a563f6efc2323afecb7a54aabee96e7104d1d2921505b" and
            exponent_sums(candidate, 2) == [0, 0], "candidate 124 binding")
    cofaces = base.cofaces(3)
    marked3, marked4 = pc_marked(q3, "PB3"), pc_marked(q3, "PB4")
    difference = base.reduce_word(candidate + base.inv_word(base_word))
    correction_receipt = {
        "expanded_section_word": correction,
        "expanded_section_word_sha256": digest_obj(correction),
        "section_chain": chain,
        "difference_candidate_times_base_inverse": e3_record(
            base, "candidate_base_difference", difference, q0marks, pc3, marked3,
            cofaces, q4marks, pc4, marked4),
        "correction_word_direct": e3_record(
            base, "registered_A5_correction", correction, q0marks, pc3, marked3,
            cofaces, q4marks, pc4, marked4),
    }
    return ({"outer_index": 1, "m_shift_index": 0, "correction_index": 124,
             "base_word": base_word, "base_word_length": len(base_word),
             "base_word_sha256": digest_obj(base_word), "correction": correction_receipt,
             "candidate_word": candidate, "candidate_word_length": len(candidate),
             "candidate_word_sha256": digest_obj(candidate),
             "free_exponent_sums": [0, 0], "registered_receipt_word_equal": True},
            candidate)


def element_order(value: Any, identity: Any, mul: Callable[[Any, Any], Any], cap: int) -> int:
    current = identity
    for n in range(1, cap + 1):
        current = mul(current, value)
        if current == identity:
            return n
    raise CheckError("element order cap")


def tuple_nord(base: Any, words: Sequence[Sequence[int]], components: Sequence[Any]) -> int:
    values: list[int] = []
    for word in words:
        orders = []
        for marks, identity, operation, inverse, cap in components:
            value = base.eval_word(word, marks, identity, operation, inverse)
            orders.append(element_order(value, identity, operation, cap))
        values.append(math.lcm(*orders))
    return math.lcm(*values)


def order_certificate(base: Any, q3: dict[str, Any], d1: dict[str, Any],
                      q0marks: Sequence[Any], pc3: Any, q4marks: Sequence[Any],
                      pc4: Any) -> dict[str, Any]:
    marked3, marked4 = pc_marked(q3, "PB3"), pc_marked(q3, "PB4")
    pi3marks = [tuple(x["coords"]) for x in marked3]
    pi4marks = [tuple(x["coords"]) for x in marked4]
    h = [(list(q0marks[:1]) + [base.one(36)] + list(q0marks[1:]),
          base.one(36), base.mul, base.inv, 36),
         (pi3marks, pc3.zero(), pc3.mul, pc3.inverse, 27)]
    k: list[Any] = []
    for mapping in base.cofaces(3):
        k.append(([base.eval_word(w, q4marks, base.one(144), base.mul, base.inv)
                   for w in mapping], base.one(144), base.mul, base.inv, 1000))
        k.append(([base.pc_eval(w, marked4, pc4) for w in mapping], pc4.zero(),
                  pc4.mul, pc4.inverse, 100))
        k.append(([sum(1 if x > 0 else -1 for x in w) % 18 for w in mapping],
                  0, lambda a, b: (a + b) % 18, lambda a: (-a) % 18, 18))
    a5_component = (d1["full_marks"], base.one(100), base.mul, base.inv, 100)
    words = [[1], [3], [1, 2, 3]]
    values = [tuple_nord(base, words, h), tuple_nord(base, words, k),
              tuple_nord(base, words, h + [a5_component]),
              tuple_nord(base, words, k + [a5_component])]
    return {"definition_3_1_words": {"x": [1], "y": [3], "c": [1, 2, 3]},
            "H_ord": values[0], "Kbeta_ord": values[1], "L_ord": values[2],
            "Lprime_ord": values[3], "gcd_L_Kbeta": math.gcd(values[2], values[1]),
            "expected": [18, 18, 90, 90],
            "friendly": {"marking_m": 0, "lambda": 1,
                         "gcd_lambda_with_orders": [math.gcd(1, x) for x in values],
                         "all_friendly": True},
            "FC29_pass": values == [18, 18, 90, 90] and
            math.gcd(values[2], values[1]) == 18,
            "component_counts": {"H": len(h), "Kbeta": len(k),
                                 "L": len(h) + 1, "Lprime": len(k) + 1}}


def a5_gate(base: Any, fc: dict[str, Any], d1: dict[str, Any],
            candidate: Sequence[int]) -> dict[str, Any]:
    compact = d1["compact_marks"]
    value = base.eval_word(candidate, [compact[0], compact[2]], base.one(15),
                           base.mul, base.inv)
    hex_values = base.context(candidate, base.hex_pairs(d1["full_marks"][0],
                              d1["full_marks"][2], base.one(100), base.mul, base.inv),
                              base.one(100), base.mul, base.inv)
    hex_res = base.hex_from_values(hex_values, 0, d1["full_marks"][0],
                                   d1["full_marks"][2], base.one(100), base.mul, base.inv)
    pent_values = base.context(candidate, base.elem_pairs(d1["pb4_marks"], base.one(20),
                               base.mul), base.one(20), base.mul, base.inv)
    pent_res = base.pent_from_values(pent_values, base.one(20), base.mul, base.inv)
    conjugate_y = base.pp([base.inv(value), compact[2], value], base.one(15), base.mul)
    onto = len(base.enumerate_group([compact[0], conjugate_y], 1501)[0]) == 1500
    supports, normal_orders = [], []
    for row in fc["rhoA"]["single_support_witnesses"]:
        full = base.eval_word(row["source_word"], d1["pb4_marks"], base.one(20),
                             base.mul, base.inv)
        blocks = [base.restrict(full, 5 * i, 5) for i in range(4)]
        require([perm_row(x) for x in blocks] == row["images"], "FC8 support image")
        target = blocks[row["coordinate"] - 1]
        ngens = base.normal_generators([d1["x"], d1["y"]], [target], 61)
        normal_order = len(base.enumerate_group(ngens, 61)[0])
        normal_orders.append(normal_order)
        supports.append({"coordinate": row["coordinate"], "source_word": row["source_word"],
                         "images": row["images"],
                         "other_coordinates_identity": all(i == row["coordinate"] - 1 or
                                                            blocks[i] == base.one(5)
                                                            for i in range(4)),
                         "target_nontrivial": target != base.one(5),
                         "normal_closure_order": normal_order})
    a5_group, _ = base.enumerate_group([d1["x"], d1["y"]], 61)
    perfect = len(base.derived_set([d1["x"], d1["y"]], 60, 61)) == 60
    factor_rows = [row["factor_permutation"] for row in fc["b4_action"]["generators"]]
    require(factor_rows == [[2, 1, 3, 4], [1, 3, 2, 4], [1, 2, 4, 3]],
            "FC8 factor permutations")
    factor_group, _ = base.enumerate_group([base.perm(row) for row in factor_rows], 25)
    require(len(factor_group) == 24, "FC8 factor action S4")
    result = {"marking_m": 0, "lambda": 1, "candidate_compact_row": perm_row(value),
              "compact_DF_order": len(d1["compact"]),
              "compact_derived_order": len(d1["derived"]),
              "charming_derived_membership": value in d1["derived"],
              "hexagon_rows": [perm_row(x) for x in hex_res],
              "pentagon_row": perm_row(pent_res),
              "hexagon_exact": all(x == base.one(100) for x in hex_res),
              "pentagon_exact": pent_res == base.one(20), "onto_DF": onto,
              "A5": {"order": len(a5_group), "simple": True, "perfect": perfect,
                     "no_C3_quotient": perfect},
              "single_support_witnesses": supports,
              "single_support_normal_orders": normal_orders,
              "A5four_full_product": normal_orders == [60] * 4,
              "factor_permutations": factor_rows, "factor_action_group_order": 24,
              "factor_action_transitive": True,
              "no_common_quotient_A5four_C3": perfect,
              "goursat_L_Kbeta_equals_H": perfect and normal_orders == [60] * 4,
              "index_L_Lprime": 3}
    result["pass"] = (result["charming_derived_membership"] and
                      result["hexagon_exact"] and result["pentagon_exact"] and onto and
                      normal_orders == [60] * 4 and perfect and len(factor_group) == 24)
    return result


def expected_pins(q3: dict[str, Any], fc: dict[str, Any], dp: dict[str, Any]) -> dict[str, Any]:
    def row(path: Path, sha: str) -> dict[str, Any]:
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == sha, f"source pin {path}")
        return {"path": str(path).replace("\\", "/"), "sha256": sha, "bytes": len(raw)}
    return {"q3_artifact": row(Q3_PATH, Q3_SHA), "fc8_artifact": row(FC8_PATH, FC8_SHA),
            "selected_lift_artifact": row(DP_PATH, DP_SHA),
            "selected_lift_producer": row(OLD_PRODUCER, OLD_PRODUCER_SHA),
            "selected_lift_checker": row(OLD_CHECKER, OLD_CHECKER_SHA),
            "selected_lift_driver": row(OLD_DRIVER, OLD_DRIVER_SHA),
            "frozen_words": row(WORDS_PATH, WORDS_SHA),
            "outside_classifier": row(AXIS_PATH, AXIS_SHA),
            "T48_1": row(T48_PATH, T48_SHA),
            "q3_sources": q3["pins"], "fc8_sources": fc["pins"],
            "selected_lift_sources": dp["pins"]}


def validate_receipt(receipt: dict[str, Any]) -> str:
    require(receipt.get("schema") == SCHEMA and set(receipt) == FIELDS, "schema/fields")
    require(isinstance(receipt.get("runtime_ms"), int) and receipt["runtime_ms"] >= 0,
            "runtime")
    require(digest_file(OLD_CHECKER) == OLD_CHECKER_SHA and
            digest_file(Q3_CHECKER) == Q3_CHECKER_SHA, "checker library SHA")
    base = load_module(OLD_CHECKER, "d972_157dq_base_checker")
    q3mod = load_module(Q3_CHECKER, "d972_157dq_q3_checker")
    q3, fc, dp, words = (load_json(Q3_PATH, Q3_SHA), load_json(FC8_PATH, FC8_SHA),
                         load_json(DP_PATH, DP_SHA), load_json(WORDS_PATH, WORDS_SHA))
    # The same-job driver has already run the frozen q3 and 157dp independent
    # checkers.  Exact artifact SHAs bind those cross-checks here; rerunning
    # their 162/202500 candidate universes would violate this lane's no-scan
    # contract.  Only the selected data and the load-bearing small groups are
    # reconstructed below.
    require(q3["schema"] == "d972-b345-q-chief/v1" and
            q3["terminal_token"] == "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION",
            "q3 frozen terminal")
    require(fc["schema"] == "d972-b4-fc8-a5four/v1" and
            fc["terminal_token"] == "FC8_A5_FOUR_CHIEF_CROSSCHECKED",
            "FC8 frozen terminal")
    require(dp["schema"] == "d972-b34-a5-selected-lift/v1" and
            dp["terminal_token"] == base.POSITIVE, "157dp frozen terminal")
    require_equal(receipt["pins"], expected_pins(q3, fc, dp), "pins")
    pc3, pc4 = base.PcCollector(q3["groups"]["PB3"]), base.PcCollector(q3["groups"]["PB4"])
    pc3.validate(); pc4.validate()
    q0marks = [base.perm(row) for row in q3["coarse_models"]["Q0"]["marked_permutations"]]
    q4marks = [base.perm(row) for row in q3["coarse_models"]["Q4"]["marked_permutations"]]
    lattice = h9_lattice(base, q3mod, q3, pc4, fc)
    require_equal(receipt["marked_abelian_lattice"], lattice, "marked lattice")
    binding, candidate = candidate_binding(base, q3, dp, q0marks, pc3, pc4, q4marks)
    require_equal(receipt["candidate_binding"], binding, "candidate binding")
    residuals = source_residuals(base, q3mod, q3, candidate,
                                 q3["selected_solution"]["typed_source_word"],
                                 q4marks, pc3, pc4)
    require_equal(receipt["literal_residuals"], residuals, "literal residuals")
    d1 = base.build_d1(fc)
    a5 = a5_gate(base, fc, d1, candidate)
    require_equal(receipt["a5_intersection"], a5, "A5 intersection")
    orders = order_certificate(base, q3, d1, q0marks, pc3, q4marks, pc4)
    require_equal(receipt["order_certificate"], orders, "FC29 orders")
    outside = base.outside_certificate(q3, words)
    require_equal(receipt["outside_certificate"], outside, "outside classifier")
    correction = binding["correction"]
    all_pass = (correction["difference_candidate_times_base_inverse"]["E3_identity"] and
                correction["difference_candidate_times_base_inverse"]["finer_five_cofaces"]["pass"] and
                correction["correction_word_direct"]["E3_identity"] and
                correction["correction_word_direct"]["finer_five_cofaces"]["pass"] and
                residuals["all_pass"] and
                residuals["PB3_five_component_onto"]["actual_joint_tuple_N_ord"] ==
                orders["Kbeta_ord"] and a5["pass"] and orders["FC29_pass"] and
                outside["outside_A"] and lattice["beta"]["onto"] and
                lattice["B4_action"]["chief_by_prime_order"])
    expected_terminal = PASS if all_pass else REJECT
    require(receipt["terminal_token"] == receipt["status"] == expected_terminal and
            receipt["terminal"] is True, "terminal bidirectional gate")
    claim = receipt["claim_boundary"]
    require(claim == {
        "pass_implication": "one outside GT^heart(L') pair exists; accepted T48-1 moves the known window from L to the strict index-three subgroup L'",
        "H_definition": "ker(PB4 -> E4)",
        "L_definition": "H intersection ker(rhoA)",
        "Kbeta_definition": "H intersection ker(total-linking mod18)",
        "Lprime_definition": "L intersection Kbeta", "strict_index": 3,
        "one_chief_descent_only": True, "L_or_Lprime_isolated_claimed": False,
        "global_B4_B_claimed": False, "cofinal_iteration_claimed": False,
        "compactness_claimed": False, "settlement_diagnostic_only": True,
        "candidate_rejection_not_B4_A": True}, "claim boundary")
    perf = receipt["performance"]
    require(perf == {"candidate_universe_scans": 0, "registered_candidates_replayed": 1,
                     "inverse_certificate_fibre_cap": 27,
                     "inverse_certificate_attempts": residuals["T_inverse_binding"]["attempted"],
                     "H9_binary_kernel_vectors": 2 ** 6,
                     "integral_lattice_residue_vectors": 6 ** 6,
                     "Artin_target_relation_evaluations": 3 * 2 * len(
                         q3["formulas"]["presentations"]["PB4"]["relations"]),
                     "Artin_two_sided_generator_evaluations": 3 * 2 * 6,
                     "FC8_single_support_replays": 4,
                     "PB3_five_component_intertwining_residuals":
                         residuals["PB3_five_component_onto"]
                         ["component_intertwining_residuals"],
                     "compact_DF_enumeration_cap": 1500,
                     "H_or_E4_elements_enumerated": 0, "A5four_elements_enumerated": 0,
                     "PB5_constructions": 0, "ANUPQ_calls": 0, "translation_BFS_calls": 0,
                     "sparse_gaussian_searches": 0, "H9_DerivedSubgroup_calls": 1,
                     "G9_DerivedSubgroup_calls": 1, "Pi4_DerivedSubgroup_calls": 1,
                     "literal_residual_count": residuals["residual_count"]}, "performance")
    require(receipt["provenance"] == {
        "producer": "search/d972_b34_total_linking_c3_chief_v1.g",
        "checker": "search/check_d972_b34_total_linking_c3_chief_v1.py",
        "upstream_crosschecked_run": 32171982444}, "provenance")
    return expected_terminal


def fixture() -> dict[str, Any]:
    basis = [[6 * int(i == j) for j in range(6)] for i in range(5)] + [[3] * 6]
    word = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1, 2, 2, 2, -1, -2, -2,
            1, 1, 1, 1] + [-2] * 18 + [-1] * 18 + [2] * 18 + [1] * 18
    matrix = []
    for _ in range(4):
        matrix.extend([[1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]])
    return {"matrix": matrix, "rank": 1,
            "kernel": 32, "pi": [[int(i == j) for j in range(6)] for i in range(6)],
            "basis": basis, "index": 23328, "gcd": 6,
            "candidate": {"index": 124, "length": 92, "word": word,
                          "sha": digest_obj(word)},
            "residuals": {"hex": True, "pent": True, "S": True,
                          "T": True, "ST": True, "TS": True,
                          "PB3_tuple_onto": True},
            "orders": [18, 18, 90, 90], "fc8": {"perfect": True, "no_c3": True},
            "outside_row": 37, "terminal": PASS,
            "claim": {"global": False, "one_step": True}}


def validate_fixture(row: dict[str, Any]) -> None:
    require(rank_mod(row["matrix"], 2) == row["rank"] and
            2 ** (6 - row["rank"]) == row["kernel"], "binary matrix fixture")
    require(row["pi"] == [[int(i == j) for j in range(6)] for i in range(6)], "Pi fixture")
    require(abs(det_bareiss(row["basis"])) == row["index"] == 23328 and
            math.gcd(*(sum(x) for x in row["basis"])) == row["gcd"] == 6,
            "lattice fixture")
    c = row["candidate"]
    require(c["index"] == 124 and c["length"] == len(c["word"]) == 92 and
            c["sha"] == digest_obj(c["word"]), "candidate fixture")
    require(all(row["residuals"].values()), "residual fixture")
    require(row["orders"] == [18, 18, 90, 90], "FC29 fixture")
    require(row["fc8"] == {"perfect": True, "no_c3": True}, "FC8 fixture")
    require(row["outside_row"] == 37, "outside fixture")
    require(row["terminal"] == PASS and row["claim"] == {"global": False, "one_step": True},
            "terminal/claim fixture")


def self_test() -> None:
    good = fixture()
    validate_fixture(good)
    mutations = [
        lambda x: x["matrix"][0].__setitem__(0, 0),
        lambda x: x.__setitem__("rank", 5),
        lambda x: x.__setitem__("kernel", 2),
        lambda x: x["pi"][0].__setitem__(0, 0),
        lambda x: x.__setitem__("index", 1),
        lambda x: x.__setitem__("gcd", 18),
        lambda x: x["candidate"].__setitem__("index", 123),
        lambda x: x["candidate"].__setitem__("sha", "0" * 64),
        lambda x: x["residuals"].__setitem__("hex", False),
        lambda x: x["residuals"].__setitem__("pent", False),
        lambda x: x["residuals"].__setitem__("S", False),
        lambda x: x["residuals"].__setitem__("T", False),
        lambda x: x["residuals"].__setitem__("ST", False),
        lambda x: x["residuals"].__setitem__("TS", False),
        lambda x: x["residuals"].__setitem__("PB3_tuple_onto", False),
        lambda x: x["orders"].__setitem__(1, 54),
        lambda x: x["fc8"].__setitem__("perfect", False),
        lambda x: x["fc8"].__setitem__("no_c3", False),
        lambda x: x.__setitem__("outside_row", 19),
        lambda x: x.__setitem__("terminal", REJECT),
        lambda x: x["claim"].__setitem__("global", True),
    ]
    for mutate in mutations:
        bad = copy.deepcopy(good)
        mutate(bad)
        try:
            validate_fixture(bad)
        except CheckError:
            continue
        raise CheckError("mutation unexpectedly accepted")
    print(f"D972_B34_TOTAL_LINKING_C3_CHECKER_SELFTEST_PASS mutations={len(mutations)}")


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 2 and argv[1] == "--self-test":
            self_test()
            return 0
        require(len(argv) == 2, "usage: checker RECEIPT | --self-test")
        receipt = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        terminal = validate_receipt(receipt)
        print(f"B34_TOTAL_LINKING_C3_CHECKER_PASS terminal={terminal} "
              f"residuals={receipt['literal_residuals']['residual_count']}")
        return 0
    except (CheckError, RuntimeError, KeyError, IndexError, TypeError, ValueError,
            json.JSONDecodeError, OSError) as exc:
        print(f"B34_TOTAL_LINKING_C3_CHECKER_FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
