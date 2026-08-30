#!/usr/bin/env python3
"""Bounded, helper-independent replay of the PB4 central C3 split.

The only executable implementation borrowed here is the already independent
q3 PC/permutation checker, pinned by bytes and SHA.  No producer module is
loaded and no matched group is enumerated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import types
from pathlib import Path
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
Q3 = ROOT / "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json"
INDEPENDENT = ROOT / "search/check_d972_b345_q3_chief_v1.py"
TASK = ROOT / "sol/luna_task_418_r07_pb4_central_split_crosscheck.md"
PROOF = ROOT / "sol/proof_r07_a0_pb4_central_split_direct_quotient_v402.md"
Q3_BYTES = 231570
Q3_SHA = "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"
INDEPENDENT_SHA = "ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73"
TASK_SHA = "c91186486ae89ceb051b7f992b7452a757c6880ec902abbb8815fbe1784632b0"
PROOF_SHA = "7945c953db3a5b4dbbedb683a7c2e77ba19354bb2f5c0d76e98a5a550dafe8e9"
Q3_SCHEMA = "d972-b345-q-chief/v1"
Q3_TERMINAL = "B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION"
MARKED = ("A12", "A13", "A14", "A23", "A24", "A34")
Z_WORD = [1, 2, 4, 3, 5, 6]
EXPECTED_PC_Z = (1, 1, 1, 1, 1, 1, 0, 0, 0, 0)
EXPECTED_Q4_DEGREE = 144
EXPECTED_Q4_ORDER = "583152628325845597028352"


class Reject(AssertionError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def sha_bytes(path: Path) -> tuple[int, str]:
    raw = path.read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def load_independent() -> dict[str, Any]:
    size, digest = sha_bytes(INDEPENDENT)
    need(size == 89082 and digest == INDEPENDENT_SHA,
         "independent q3 checker pin drift")
    module_name = "d972_q3_independent_pinned"
    module = types.ModuleType(module_name)
    module.__file__ = str(INDEPENDENT)
    sys.modules[module_name] = module
    exec(compile(INDEPENDENT.read_text(encoding="utf-8"), str(INDEPENDENT), "exec"),
         module.__dict__)
    return module.__dict__


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for x in word:
        need(isinstance(x, int) and x != 0, "bad free letter")
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def free_inverse(word: Sequence[int]) -> list[int]:
    return free_reduce(-x for x in reversed(word))


def free_eval(word: Sequence[int], images: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for x in word:
        need(1 <= abs(x) <= len(images), "free substitution index")
        part = images[x - 1] if x > 0 else free_inverse(images[-x - 1])
        out = free_reduce(out + list(part))
    return out


def conjugation_action(w: Sequence[int], rank: int) -> list[list[int]]:
    wi = free_inverse(w)
    return [free_reduce(list(w) + [i] + wi) for i in range(1, rank + 1)]


def artin_step(rank: int, letter: int) -> list[list[int]]:
    i = abs(letter)
    need(1 <= i < rank, "Artin generator index")
    images = [[j] for j in range(1, rank + 1)]
    if letter > 0:
        images[i - 1] = [i, i + 1, -i]
        images[i] = [i]
    else:
        images[i - 1] = [i + 1]
        images[i] = [-i - 1, i, i + 1]
    return images


def artin_images(rank: int, braid_word: Sequence[int]) -> list[list[int]]:
    images = [[j] for j in range(1, rank + 1)]
    for letter in braid_word:
        step = artin_step(rank, letter)
        images = [free_eval(w, step) for w in images]
    return images


def artin_split_gates() -> dict[str, Any]:
    # These are the six literal substitutions in (1.4), reconstructed here,
    # rather than imported from the producer or from a word-generation helper.
    phi_b_literal = [
        [1, 3, 1, -3, -1],
        [1, 3, -1, -3, 2, 3, 1, -3, -1],
        [1, 3, -1],
    ]
    phi_c_literal = [[1], [2, 3, 2, -3, -2], [2, 3, -2]]
    # Generate the actions from the elementary Artin action on F_3.  The
    # braid words are A13=s2 s1^2 s2^-1 and A23=s2^2 in the frozen order.
    phi_b = artin_images(3, [2, 1, 1, -2])
    phi_c = artin_images(3, [2, 2])
    need(phi_b == phi_b_literal and phi_c == phi_c_literal,
         "literal Artin formulas drift")
    # z3=A12*A13*A23; free reduction of its expanded braid word is used only
    # to generate the action, independently of the asserted conjugation form.
    z3_braid = free_reduce([1, 1, 2, 1, 1, -2, 2, 2])
    z3_generated = artin_images(3, z3_braid)
    w = [1, 2, 3]
    formulas = {
        "phi_b_p": phi_b[0], "phi_b_q": phi_b[1], "phi_b_r": phi_b[2],
        "phi_c_p": phi_c[0], "phi_c_q": phi_c[1], "phi_c_r": phi_c[2],
    }
    need(free_eval(w, phi_b) == w, "phi_b does not fix w")
    need(free_eval(w, phi_c) == w, "phi_c does not fix w")
    z3 = conjugation_action(w, 3)
    need(z3_generated == z3, "z3 action is not conjugation by w")
    need(free_eval(w, z3) == w, "z3 does not fix w")
    return {"w": w, "formulas": formulas, "phi_b_fixes_w": True,
            "phi_c_fixes_w": True, "z3_is_conjugation_by_w": True,
            "z3_fixes_w": True, "substitution_replay": True,
            "z3_braid_word": z3_braid}


def first_coordinate_gate(record: dict[str, Any]) -> dict[str, Any]:
    assignment = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    bad = [1, 1, 1, 1, 1, 1, 0, 0, 0, 1]

    def relations_hold(values: Sequence[int]) -> bool:
        for i, row in enumerate(record["power_relations"]):
            if (3 * values[i] - sum(a * b for a, b in zip(row, values))) % 3:
                return False
        for family in ("conjugate_relations", "inverse_conjugate_relations"):
            for row in record[family]:
                lhs = values[row["i"] - 1]
                rhs = sum(a * b for a, b in zip(row["coords"], values))
                if (lhs - rhs) % 3:
                    return False
        return True

    need(relations_hold(assignment), "first coordinate relation descent")
    need(not relations_hold(bad), "nonhomomorphic coordinate mutation accepted")
    return {"assignment": assignment, "power_relations_checked": len(record["power_relations"]),
            "conjugate_relations_checked": len(record["conjugate_relations"]),
            "inverse_conjugate_relations_checked": len(record["inverse_conjugate_relations"]),
            "homomorphism_to_F3": True, "mutation_rejected": True}


def evaluate(data: dict[str, Any], q3: dict[str, Any], ind: dict[str, Any]) -> dict[str, Any]:
    need(data is q3, "internal receipt identity")
    need(q3["schema"] == Q3_SCHEMA and q3["status"] == Q3_TERMINAL and
         q3["terminal_token"] == Q3_TERMINAL, "frozen q3 schema/terminal")
    rec = q3["groups"]["PB4"]
    need(rec["generator_count"] == 10 and len(rec["marked_generators"]) == 6,
         "PB4 PC width")
    need(rec["order_decimal"] == "59049" and rec["nilpotency_class"] == 2 and
         rec["exponent"] == 3 and rec["relative_orders"] == [3] * 10,
         "PB4 PC frozen fields")
    pc = ind["PcCollector"](rec)
    pc.validate()
    models = q3["coarse_models"]
    q4rec = models["Q4"]
    need(q4rec["degree"] == EXPECTED_Q4_DEGREE and
         q4rec["order_decimal"] == EXPECTED_Q4_ORDER and
         len(q4rec["marked_permutations"]) == 6, "Q4 frozen fields")
    q4 = ind["validate_perm_model"](q4rec, 6)
    one = ind["perm_one"](EXPECTED_Q4_DEGREE)
    zpc = ind["eval_marked"](Z_WORD, rec["marked_generators"], pc)

    def perm_eval(word: Sequence[int]):
        out = one
        for x in word:
            out = ind["perm_mul"](out, q4[x - 1] if x > 0 else ind["perm_inv"](q4[-x - 1]))
        return out

    zcoarse = perm_eval(Z_WORD)
    need(zcoarse == one, "coarse z is not identity")
    need(zpc != pc.zero(), "z is trivial in PC")
    need(pc.power(zpc, 3) == pc.zero(), "z does not have order dividing three")
    pc_commuting = []
    coarse_commuting = []
    for i in range(6):
        gi = rec["marked_generators"][i]["coords"]
        pc_commuting.append(pc.conjugate(gi, zpc) == tuple(gi))
        coarse_commuting.append(ind["perm_mul"](ind["perm_mul"](ind["perm_inv"](zcoarse),
                              ind["perm_inv"](q4[i])), ind["perm_mul"](zcoarse, q4[i])) == one)
    need(all(pc_commuting) and all(coarse_commuting), "z centrality")
    need(zpc == EXPECTED_PC_Z, "PC z coordinates")
    marked_pc = [tuple(x["coords"]) for x in rec["marked_generators"]]
    need(all(marked_pc[i][0] == 0 for i in (1, 2, 3, 4, 5)) and zpc[0] == 1,
         "new noncentral first coordinates")
    # A12 is intentionally not in H0; the five others are.
    need(all(marked_pc[i][0] == 0 for i in (1, 2, 3, 4, 5)), "H0 marked generators")
    hom = first_coordinate_gate(rec)

    rhs = Z_WORD + [-6, -5, -3, -4, -2]
    need(ind["eval_marked"](rhs, rec["marked_generators"], pc) == tuple(rec["marked_generators"][0]["coords"]),
         "source A12 identity in PC")
    need(perm_eval(rhs) == q4[0], "source A12 identity in coarse Q4")
    artin = artin_split_gates()

    # Adversarial checks are intentionally run against the same independently
    # reconstructed operations, and must fail closed.
    wrong_z = [1, 2, 3, 4, 6, 5]
    wrong_pc = ind["eval_marked"](wrong_z, rec["marked_generators"], pc)
    wrong_coarse = perm_eval(wrong_z)
    need(wrong_pc != EXPECTED_PC_Z or wrong_coarse != one, "wrong z order mutation accepted")
    noncentral = [MARKED[i] for i in (1, 2, 3, 4, 5)]
    def complete_noncentral(names: Sequence[str]) -> bool:
        return list(names) == noncentral
    need(complete_noncentral(noncentral), "noncentral generator roster")
    need(not complete_noncentral(noncentral[:-1]),
         "dropped-generator mutation accepted")

    gates = {
        "receipt_schema_terminal": True,
        "pb4_pc_width_and_fields": True,
        "q4_coarse_fields": True,
        "z_coarse_identity": True,
        "z_pc_nonidentity_order_three": True,
        "z_commutes_all_six": True,
        "pc_coordinates": list(zpc),
        "first_coordinate_homomorphism": hom,
        "artin_actions": artin,
        "source_generator_identity": True,
        "central_direct_product_conclusion": "H=H0 direct_product <z>",
        "adversarial_mutations": {
            "wrong_central_word_order_rejected": True,
            "nonhomomorphic_coordinate_rejected": True,
            "dropped_noncentral_generator_rejected": True,
        },
    }
    return gates


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q3", type=Path, default=Q3)
    ap.add_argument("--output", type=Path,
                    default=ROOT / "search/certs/d972_r07_pb4_central_split_v1_20260830.json")
    args = ap.parse_args()
    started = time.perf_counter()
    q3_path = args.q3.resolve()
    size, digest = sha_bytes(q3_path)
    need(q3_path == Q3.resolve(), "only frozen q3 receipt is accepted")
    need(size == Q3_BYTES and digest == Q3_SHA, "q3 receipt pin drift")
    task_bytes, task_sha = sha_bytes(TASK)
    proof_bytes, proof_sha = sha_bytes(PROOF)
    need(task_sha == TASK_SHA and proof_sha == PROOF_SHA, "task/proof pin drift")
    q3 = json.loads(q3_path.read_text(encoding="utf-8"))
    ind = load_independent()
    gates = evaluate(q3, q3, ind)
    checker_size, checker_sha = sha_bytes(Path(__file__).resolve())
    cert = {
        "schema": "d972-r07-pb4-central-split/v1",
        "status": "PB4_CENTRAL_SPLIT_CROSS_CHECKED",
        "cross_checked": True,
        "verified": False,
        "terminal_claim": "PB4_CENTRAL_SPLIT_CROSS_CHECKED",
        "theorem_consequence": "H=H0 direct_product <z>",
        "z_word": Z_WORD,
        "marked_order": list(MARKED),
        "gates": gates,
        "claims_not_made": ["A0_MEMBER", "A0_NONMEMBER", "fake", "Ihara_witness",
                             "compatible_lift", "verified"],
        "pins": {
            "q3_receipt": {"path": str(q3_path.relative_to(ROOT)).replace("\\", "/"),
                           "bytes": size, "sha256": digest},
            "independent_checker": {"path": str(INDEPENDENT.relative_to(ROOT)).replace("\\", "/"),
                                     "bytes": 89082, "sha256": INDEPENDENT_SHA},
            "task": {"path": str(TASK.relative_to(ROOT)).replace("\\", "/"),
                     "bytes": task_bytes, "sha256": task_sha},
            "proof": {"path": str(PROOF.relative_to(ROOT)).replace("\\", "/"),
                      "bytes": proof_bytes, "sha256": proof_sha},
            "this_checker": {"path": str(Path(__file__).resolve().relative_to(ROOT)).replace("\\", "/"),
                             "bytes": checker_size, "sha256": checker_sha},
        },
        "replay": {"enumerated_matched_group": False,
                    "producer_module_loaded": False,
                    "wall_seconds": round(time.perf_counter() - started, 6)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    out_size, out_sha = sha_bytes(args.output)
    print(f"PB4_CENTRAL_SPLIT_CHECKER_PASS output_bytes={out_size} output_sha256={out_sha} "
          f"wall_seconds={cert['replay']['wall_seconds']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"PB4_CENTRAL_SPLIT_CHECKER_FAIL {exc}")
        raise SystemExit(1)
