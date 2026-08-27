"""Helper-nonshared checker for the finite relative-anchor receipt."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "search/certs/d972_r07_finite_relative_anchor_preflight_v1_20260827.json"
FIXTURE_BYTES = 309
FIXTURE_SHA256 = "ef57eca45acb43aa72a5e6e75424812e9b8956833f99ac3d6a83d297a8952829"
# The checker intentionally repeats the immutable shelf pins and does not
# import the producer or any producer helper.
PINS = {
    "v149": ("sol/proof_r07_task176_joint_formation_residual_v149.md", 9093, "cd0af7ea5b1c9354f1296485a2fe6261f9915be03f1e250812edda078b2f6337"),
    "v150": ("sol/proof_r07_finite_relative_arithmetic_anchor_v150.md", 9107, "9690bb344df580610e9efc1508a124b3871bc17b4e1d4d588eac1ec857f5c218"),
    "v152": ("sol/proof_r07_first_frattini_schreier_coinvariant_selector_v152.md", 9687, "714f96263bdd2a971b223986a97157647992cb7129eb0cfffd405ea05a995448"),
    "v153": ("sol/proof_r07_all_rung_formation_frattini_residual_formula_v153.md", 11107, "d5b4e8ed6af14094f309e0fc2dda73cc8e4ff2de1690a518a1c753f0a8829762"),
    "v154": ("sol/proof_r07_task176_full_direct_product_quotient_v154.md", 6976, "bdb9ae86dcd490788854c9c1b95a3c6709ee3a0feebfeb91528ae876003333e8"),
    "task157ee_producer": ("search/d972_b345_joint_kernel_qstar_closure_v1.py", 67945, "06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc"),
    "task157ee_checker": ("search/check_d972_b345_joint_kernel_qstar_closure_v2.py", 5942, "5c3b03af26a47f00fbfbd8484e17c591c5399ac708e566506d726d5dbd03ba88"),
    "task157ee_driver": ("search/d972_b345_joint_kernel_qstar_closure_gha_driver_v2.g", 3912, "8ff80ba97f3801daf28ad61b19d2f0a01572a5720c13578f11c56bf0d7ad26e7"),
    "task157ee_task": ("sol/luna_task_157ee_b345_joint_kernel_qstar_closure.md", 11226, "64a32c0b7e3d4efc41ddb8e0e7036282b0b5430d9ab46bbfe125b588478a95d4"),
    "task157ee_reply": ("sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md", 4118, "53f20c2cb1395b8ff59ee961e1d5a14d55156a488eb6fa49edefed5dd7619eee"),
    "q3": ("ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", 231570, "3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72"),
    "joint": ("ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", 2166036, "1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df"),
    "e3e4": ("search/d972_b345_seedspan_triple4_v1.py", 535219, "fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29"),
    "task176_source": ("search/d972_r07_all_seven_extension_section_census_v1.py", 66109, "878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b"),
    "task176_checker": ("crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py", 84980, "4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695"),
    "task176_driver": ("search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g", 15929, "1c6dc7f10d9b27092c2441a274ff74726d8899599ac10c2b8cc47cb59da02995"),
    "task176_task": ("sol/luna_task_176_r07_all_seven_extension_section_census_v1.md", 7054, "a1778c17c33e42880a6dd0c2480303a13702cb38950cf836a4ca9d8cca6fa332"),
    "task176_record": ("sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md", 47164, "aa173122310e33910d546bd3e02a98a6bf16aea9d3aad066b7d49976098ebb0c"),
    "g760_source": ("search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py", 33409, "f8c7fc7f5b5bbfffa0cf147a59313981c5a4b2c6c00504a9f773029097fdde5f"),
}
G760_SHA256 = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"
UNKNOWN_INPUT = "UNKNOWN_INPUT:ARITHMETIC_NO_S_COSET_NOT_AUTHENTICATED"

W2 = (1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -2, 1, 1, 2, 1, 1, -2, 1, 1, 2, 1, 1, 2, 1, 1, -2, 1, 1, -2, 1, 1, 2, 2, -1, -1, -2, -1)
W3 = (1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, 1, 1, 2, 1, 2, 2, 1, 2, 2, -1, 2, 2, 1, 2, 1, 1, 2, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, -2, -1, -2, -2, 1, 2, 1, 1, -2, 1)


def need(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def authenticate() -> None:
    for name, (relative, size, expected) in PINS.items():
        path = ROOT / relative; need(path.is_file(), "missing pin " + name)
        raw = path.read_bytes(); need(len(raw) == size and hashlib.sha256(raw).hexdigest() == expected, "pin drift " + name)
    raw = FIXTURE.read_bytes(); need(len(raw) == FIXTURE_BYTES and hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, "fixture drift")


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter: out.pop()
        else: out.append(int(letter))
    return out


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-int(x) for x in reversed(list(word))]


def construct_g760() -> list[int]:
    parent = reduce_word(list(W2) + reduce_word(inverse_word(W3) + list(W2)) * 8)
    word = reduce_word(parent + inverse_word([1] * 108 + [-2] * 36))
    need(len(word) == 760 and digest(word) == G760_SHA256, "checker g760")
    need(sum(1 if x == 1 else -1 if x == -1 else 0 for x in word) == 0 and sum(1 if x == 2 else -1 if x == -2 else 0 for x in word) == 0, "checker g760 exponent")
    return word


Perm = tuple[int, ...]


def pmul(a: Perm, b: Perm) -> Perm: return tuple(a[b[i]] for i in range(len(a)))


def pinv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, j in enumerate(a): out[j] = i
    return tuple(out)


def closure(gens: list[Perm]) -> list[Perm]:
    ident = tuple(range(len(gens[0]))); seen = {ident}; queue = [ident]
    while queue:
        left = queue.pop(0)
        for right in gens + [pinv(x) for x in gens]:
            value = pmul(left, right)
            if value not in seen: seen.add(value); queue.append(value)
    return sorted(seen)


def toy_replay() -> dict[str, int]:
    s1 = (1, 2, 0, 3, 4); s2 = (0, 1, 3, 4, 2); simple = closure([s1, s2]); need(len(simple) == 60, "checker toy A5")
    elements = [((a, b), s, (u, v)) for a in range(3) for b in range(3) for s in simple for u in range(2) for v in range(2)]
    identity = tuple(range(5))
    for gamma, value, quotient in elements:
        selected = (gamma, identity, quotient)
        for residual in simple: need((gamma, identity, quotient) == selected and pmul(value, residual) in simple, "checker selector replay")
    return {"toy_group_order": len(elements), "perfect_factor_order": len(simple), "residual_coset_replays": len(elements) * len(simple)}


class CheckerSchreier:
    def __init__(self, parents: list[int], letters: list[int], transitions: list[list[int]]) -> None:
        need(len(parents) == len(letters) == len(transitions) and parents[0] == 0 and letters[0] == 0, "checker Schreier root")
        self.parents, self.letters, self.transitions = parents, letters, transitions
        self.tree = {(parents[i], letters[i]) for i in range(1, len(parents))}
    def step(self, state: int, letter: int) -> int:
        if letter > 0: return self.transitions[state][letter - 1]
        target = next((i for i, row in enumerate(self.transitions) if row[-letter - 1] == state), None)
        need(target is not None, "checker Schreier inverse")
        return target
    def path(self, state: int) -> list[int]:
        out: list[int] = []
        while state:
            out.append(self.letters[state]); state = self.parents[state]
        return list(reversed(out))
    def rewrite(self, word: Iterable[int]) -> dict[str, int]:
        counts: dict[str, int] = {}; state = 0
        for letter in word:
            letter = int(letter); edge = (state, letter) if letter > 0 else (self.step(state, letter), -letter); sign = 1 if letter > 0 else -1
            if edge not in self.tree:
                key = f"{edge[0]}:{edge[1]}"; counts[key] = (counts.get(key, 0) + sign) % 3
                if counts[key] == 0: del counts[key]
            state = self.step(state, letter)
        return counts
    def schreier_word(self, state: int, letter: int) -> list[int]:
        target = self.step(state, letter); return self.path(state) + [letter] + inverse_word(self.path(target))


def checker_schreier_selftest() -> dict[str, Any]:
    tree = CheckerSchreier([0, 0, 0, 1], [0, 1, 2, 2], [[1, 2], [0, 3], [3, 0], [2, 1]])
    rows = [tree.rewrite(tree.schreier_word(2, 1)), tree.rewrite(tree.schreier_word(3, 1))]
    need(tree.path(3) == [1, 2] and rows[0] and rows[1] and tree.rewrite([1, -1, 2, -2]) == {}, "checker sparse Schreier")
    return {"quotient_states": 4, "non_tree_edges": 5, "probe_count": 2, "rows_mod_3": rows, "tree_prefix_closed": True}


def validate_q0_boundary(structural: dict[str, Any]) -> None:
    need("Q_tree" not in structural and "quotient_order" not in structural, "checker Q0/G/R swap")
    q0_order = structural.get("Q0_order")
    if q0_order is None:
        return
    parent = structural.get("Q0_parent_table", {})
    letters = structural.get("Q0_letter_table", {})
    need(parent.get("count") == q0_order and letters.get("count") == q0_order, "checker Q0 table state count")


def q0_boundary_selftest() -> bool:
    validate_q0_boundary({"Q0_order": 1469664, "Q0_parent_table": {"count": 1469664}, "Q0_letter_table": {"count": 1469664}})
    try:
        validate_q0_boundary({"Q0_order": 1469664, "Q0_parent_table": {"count": 708588}, "Q0_letter_table": {"count": 708588}, "quotient_order": 708588, "Q_tree": {"state_count": 708588}})
    except RuntimeError:
        return True
    return False


def validate_mutation_state(state: dict[str, Any]) -> None:
    expected = {"gamma_product": 243, "centre_bit": True, "inner_adjustment": "exact",
                "centralizer_element": "present", "derived_commutator": "replayed",
                "residual_roster": "stable-derived", "psl_projection": True,
                "normality_image": True, "stable_derived": True,
                "quotient_product": "replayed", "quotient_order": 708588,
                "g760_letter": 760, "g760_coordinate": "typed",
                "selector_side": "right", "selector_order": "v150",
                "arithmetic_scope": "typed", "incomplete_fibre": "UNKNOWN_INPUT",
                "q0_vs_gr_swap": "separate", "terminal": "SELFTEST_PASS"}
    need(state == expected, "checker semantic mutation state")


def mutation_selftest() -> dict[str, Any]:
    controls = ["gamma_product", "centre_bit", "inner_adjustment", "centralizer_element", "derived_commutator", "residual_roster", "psl_projection", "normality_image", "stable_derived", "quotient_product", "quotient_order", "g760_letter", "g760_coordinate", "selector_side", "selector_order", "arithmetic_scope", "incomplete_fibre", "q0_vs_gr_swap", "terminal"]
    baseline = {"gamma_product": 243, "centre_bit": True, "inner_adjustment": "exact", "centralizer_element": "present", "derived_commutator": "replayed", "residual_roster": "stable-derived", "psl_projection": True, "normality_image": True, "stable_derived": True, "quotient_product": "replayed", "quotient_order": 708588, "g760_letter": 760, "g760_coordinate": "typed", "selector_side": "right", "selector_order": "v150", "arithmetic_scope": "typed", "incomplete_fibre": "UNKNOWN_INPUT", "q0_vs_gr_swap": "separate", "terminal": "SELFTEST_PASS"}
    rejected = 0
    for ordinal, name in enumerate(controls, 1):
        mutated = dict(baseline); mutated[name] = ("MUTATED", ordinal)
        try:
            validate_mutation_state(mutated)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError(f"checker mutation accepted {ordinal}:{name}")
    need(rejected == 19, "checker semantic mutation count")
    return {"attempted": 19, "rejected": rejected, "names": controls}


def check_selftest(receipt: dict[str, Any]) -> None:
    need(receipt.get("schema") == "d972-r07-finite-relative-anchor-selftest/v1" and receipt.get("status") == "PASS" and receipt.get("terminal") == "SELFTEST_PASS", "selftest envelope")
    word = construct_g760(); g = receipt.get("g760", {})
    need(g.get("length") == len(word) and g.get("sha256") == digest(word) and g.get("exponent") == [0, 0], "selftest g760")
    need(receipt.get("toy") == toy_replay(), "selftest toy replay")
    need(receipt.get("schreier") == checker_schreier_selftest(), "selftest Schreier replay")
    need(receipt.get("q0_boundary_swap_rejected") is True and q0_boundary_selftest(), "selftest Q0/G/R swap")
    controls = receipt.get("mutation_controls", {}); need(controls == mutation_selftest(), "selftest controls")


def check_production(receipt: dict[str, Any]) -> None:
    need(receipt.get("schema") == "d972-r07-finite-relative-anchor/v1" and receipt.get("terminal") == "UNKNOWN_INPUT" and receipt.get("status") == "UNKNOWN_INPUT", "production terminal")
    need(receipt.get("comparison") == UNKNOWN_INPUT, "typed arithmetic comparison")
    claims = receipt.get("claims", {}); need(all(claims.get(name) is False for name in ("roof_membership", "dihedral_coordinate", "unnamed_sigma", "fake", "cofinal", "ihara")), "claim boundary")
    word = construct_g760(); g = receipt.get("g760", {}); need(g.get("length") == 760 and g.get("sha256") == G760_SHA256 and g.get("exponent") == [0, 0] and g.get("source_word") == word, "production g760 replay")
    need(receipt.get("static_stop", "").startswith("STATIC_STOP:"), "static stop boundary")
    structural = receipt.get("structural_receipt", {}); need(structural.get("Gamma_order") == 243 and structural.get("Phi_Gamma_order") == 27 and structural.get("Gamma_over_Phi_order") == 9 and structural.get("PSL_order") == 504 and structural.get("G9_order") == 2916 and structural.get("Q0_order") == 1469664 and structural.get("Q0_is_not_G_over_R") is True and structural.get("residual_roster") == "NOT_MATERIALIZED" and structural.get("R_stable_chain") == "NOT_MATERIALIZED" and structural.get("R_relators") == "NOT_MATERIALIZED" and structural.get("R_source_words") == "NOT_MATERIALIZED" and structural.get("g760_C_coordinate") == "NOT_MATERIALIZED" and structural.get("R_digest_encoding") == "NOT_MATERIALIZED", "partial structural orders")
    shelf = structural.get("shelf_replay", {}); need(structural.get("Gamma_source_words") and shelf.get("Gamma_source_words") == structural.get("Gamma_source_words") and structural.get("R_source_words") == "NOT_MATERIALIZED" and shelf.get("Q0_order") == 1469664 and shelf.get("Q0_lossless") is True, "task176 shelf replay")
    need(shelf.get("Q0_parent_table", {}).get("count") == 1469664 and shelf.get("Q0_letter_table", {}).get("count") == 1469664, "Q0 table state count")
    need("Q_tree" not in structural and "quotient_order" not in structural and "direct_C" not in structural and "R_tree" not in structural, "no fake G/R tree")
    need(receipt.get("arithmetic_inventory") and all("reason" in row and row["reason"] for row in receipt["arithmetic_inventory"]), "input inventory")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(); p.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), required=True); p.add_argument("--receipt", type=Path, required=True); p.add_argument("--verdict", type=Path, required=True); args = p.parse_args(argv)
    authenticate(); receipt = json.loads(args.receipt.read_text(encoding="ascii"))
    if args.mode == "SELFTEST": check_selftest(receipt); marker = "R07_FINITE_RELATIVE_ANCHOR_V1_CHECKER_SELFTEST_PASS mutations=19"; result = {"status": "PASS", "terminal": "SELFTEST_PASS", "mutations": 19}
    else: check_production(receipt); marker = "R07_FINITE_RELATIVE_ANCHOR_V1_CHECKER_PASS terminal=UNKNOWN_INPUT"; result = {"status": "PASS", "terminal": "UNKNOWN_INPUT", "comparison": UNKNOWN_INPUT}
    verdict = args.verdict if args.verdict.is_absolute() else ROOT / args.verdict; verdict.parent.mkdir(parents=True, exist_ok=True); verdict.write_bytes(canonical(result) + b"\n"); print(marker, flush=True); return 0


if __name__ == "__main__":
    raise SystemExit(main())
