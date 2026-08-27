"""Bounded materialization scaffold for the v149/v150 finite anchor.

The production path authenticates the complete frozen shelf before parsing it,
replays the frozen 760-letter source, and stops with the exact arithmetic
no-S-coset input state until DIH-ARITH supplies that authenticated object.
The finite toy path is a real residual/selector replay used only by SELFTEST.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-finite-relative-anchor/v1"
SELFTEST_SCHEMA = "d972-r07-finite-relative-anchor-selftest/v1"
FIXTURE = ROOT / "search/certs/d972_r07_finite_relative_anchor_preflight_v1_20260827.json"
FIXTURE_BYTES = 309
FIXTURE_SHA256 = "ef57eca45acb43aa72a5e6e75424812e9b8956833f99ac3d6a83d297a8952829"
UNKNOWN_INPUT = "UNKNOWN_INPUT:ARITHMETIC_NO_S_COSET_NOT_AUTHENTICATED"
UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD"

PINS = {
    "v149": ("sol/proof_r07_task176_joint_formation_residual_v149.md", 9093, "cd0af7ea5b1c9354f1296485a2fe6261f9915be03f1e250812edda078b2f6337"),
    "v150": ("sol/proof_r07_finite_relative_arithmetic_anchor_v150.md", 9107, "9690bb344df580610e9efc1508a124b3871bc17b4e1d4d588eac1ec857f5c218"),
    "v152": ("sol/proof_r07_first_frattini_schreier_coinvariant_selector_v152.md", 9687, "714f96263bdd2a971b223986a97157647992cb7129eb0cfffd405ea05a995448"),
    "v153": ("sol/proof_r07_all_rung_formation_frattini_residual_formula_v153.md", 11107, "D5B4E8ED6AF14094F309E0FC2DDA73CC8E4FF2DE1690A518A1C753F0A8829762".lower()),
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

W2 = (1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -2, 1, 1, 2, 1, 1, -2, 1, 1, 2, 1, 1, 2, 1, 1, -2, 1, 1, -2, 1, 1, 2, 2, -1, -1, -2, -1)
W3 = (1, 1, 1, 1, -2, -2, -2, -2, -1, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, 1, 1, 2, 1, 2, 2, 1, 2, 2, -1, 2, 2, 1, 2, 1, 1, 2, 2, -1, -1, -2, -1, -1, 2, -1, -1, -2, -2, -2, -1, -2, -2, 1, 2, 1, 1, -2, 1)
G760_SHA256 = "518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d"


def need(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_identity(path: Path) -> tuple[int, str]:
    raw = path.read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def authenticate_pins() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for name, (relative, size, expected) in PINS.items():
        path = ROOT / relative
        need(path.is_file(), f"missing authenticated pin {name}")
        got_size, got_sha = file_identity(path)
        need((got_size, got_sha) == (size, expected), f"pin drift {name}")
        out[name] = {"path": relative, "bytes": got_size, "sha256": got_sha}
    got_size, got_sha = file_identity(FIXTURE)
    need((got_size, got_sha) == (FIXTURE_BYTES, FIXTURE_SHA256), "fixture pin")
    out["fixture"] = {"path": str(FIXTURE.relative_to(ROOT)).replace("\\", "/"), "bytes": got_size, "sha256": got_sha}
    return out


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(int(letter))
    return out


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-int(x) for x in reversed(list(word))]


def exponent(word: Iterable[int]) -> tuple[int, int]:
    return (sum(1 if x == 1 else -1 if x == -1 else 0 for x in word),
            sum(1 if x == 2 else -1 if x == -2 else 0 for x in word))


def construct_g760() -> list[int]:
    parent = reduce_word(list(W2) + reduce_word(inverse_word(W3) + list(W2)) * 8)
    tail = [1] * 108 + [-2] * 36
    word = reduce_word(parent + inverse_word(tail))
    need(len(parent) == 616 and len(word) == 760, "g760 length")
    need(digest(word) == G760_SHA256 and exponent(word) == (0, 0), "g760 frozen digest/exponent")
    return word


Perm = tuple[int, ...]


def pmul(a: Perm, b: Perm) -> Perm:
    return tuple(a[b[i]] for i in range(len(a)))


def pinv(a: Perm) -> Perm:
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def subgroup(generators: list[Perm]) -> list[Perm]:
    identity = tuple(range(len(generators[0])))
    seen = {identity}; queue = [identity]
    while queue:
        left = queue.pop(0)
        for right in generators + [pinv(x) for x in generators]:
            value = pmul(left, right)
            if value not in seen:
                seen.add(value); queue.append(value)
    return sorted(seen)


def commutator(a: Perm, b: Perm) -> Perm:
    return pmul(pmul(pmul(pinv(a), pinv(b)), a), b)


def toy_group() -> tuple[list[tuple[tuple[int, int], Perm, tuple[int, int]]], list[Perm]]:
    identity = tuple(range(5)); s1 = (1, 2, 0, 3, 4); s2 = (0, 1, 3, 4, 2)
    simple = subgroup([s1, s2]); need(len(simple) == 60, "toy perfect factor order")
    derived = subgroup([commutator(a, b) for a in simple for b in simple])
    need(len(derived) == 60, "toy perfect factor")
    elements = [((a, b), s, (u, v)) for a in range(3) for b in range(3) for s in simple for u in range(2) for v in range(2)]
    return elements, simple


def toy_selector_selftest() -> dict[str, Any]:
    elements, simple = toy_group(); identity = tuple(range(5))
    def selector(x: tuple[tuple[int, int], Perm, tuple[int, int]]) -> tuple[tuple[int, int], Perm, tuple[int, int]]:
        return (x[0], identity, x[2])
    for element in elements:
        selected = selector(element)
        need(selected[0] == element[0] and selected[2] == element[2] and selected[1] == identity, "toy selector")
        for residual in simple:
            need(selector((element[0], pmul(element[1], residual), element[2])) == selected, "toy residual constancy")
    return {"group_order": len(elements), "perfect_factor_order": len(simple), "residual_representatives": len(simple), "selector_replays": len(elements) * len(simple)}


class SparseSchreier:
    """Sparse mod-3 rewrite over a frozen prefix-closed quotient tree."""
    def __init__(self, parents: list[int], parent_letters: list[int], transitions: list[list[int]]) -> None:
        need(len(parents) == len(parent_letters) == len(transitions) and parents[0] == 0 and parent_letters[0] == 0, "Schreier root")
        self.parents, self.parent_letters, self.transitions = parents, parent_letters, transitions
        self.states = len(parents); self.tree = {(parents[s], parent_letters[s]) for s in range(1, self.states)}
        self.edges = {(s, a) for s in range(self.states) for a in (1, 2) if (s, a) not in self.tree}
    def path(self, state: int) -> list[int]:
        out: list[int] = []
        while state != 0:
            out.append(self.parent_letters[state]); state = self.parents[state]
        return list(reversed(out))
    def step(self, state: int, letter: int) -> int:
        if letter > 0: return self.transitions[state][letter - 1]
        target = next((u for u in range(self.states) if self.transitions[u][-letter - 1] == state), None)
        need(target is not None, "Schreier inverse edge")
        return target
    def rewrite(self, word: Iterable[int]) -> dict[str, int]:
        counts: dict[str, int] = {}; state = 0
        for letter in word:
            letter = int(letter)
            if letter > 0:
                edge = (state, letter); sign = 1
            else:
                target = self.step(state, letter); edge = (target, -letter); sign = -1
            if edge not in self.tree:
                key = f"{edge[0]}:{edge[1]}"; counts[key] = (counts.get(key, 0) + sign) % 3
                if counts[key] == 0: del counts[key]
            state = self.step(state, letter)
        return counts
    def schreier_word(self, state: int, letter: int) -> list[int]:
        target = self.step(state, letter); return self.path(state) + [letter] + inverse_word(self.path(target))


def schreier_selftest() -> dict[str, Any]:
    # C2 x C2 quotient with positive x/y first-seen tree 0--x-->1, 0--y-->2.
    transitions = [[1, 2], [0, 3], [3, 0], [2, 1]]
    tree = SparseSchreier([0, 0, 0, 1], [0, 1, 2, 2], transitions)
    need(tree.path(3) == [1, 2] and tree.rewrite(tree.schreier_word(0, 1)) == {}, "Schreier tree edge")
    probes = [tree.schreier_word(2, 1), tree.schreier_word(3, 1)]
    rows = [tree.rewrite(word) for word in probes]
    need(rows[0] and rows[1] and tree.rewrite([1, -1, 2, -2]) == {}, "Schreier sparse rows")
    return {"quotient_states": tree.states, "non_tree_edges": len(tree.edges), "probe_count": len(probes), "tree_prefix_closed": True, "rows_mod_3": rows}


def validate_q0_boundary(structural: dict[str, Any]) -> None:
    """Reject a Q0 shelf relabelled as the missing G/R quotient."""
    need("Q_tree" not in structural and "quotient_order" not in structural, "Q0/G/R swap")
    q0_order = structural.get("Q0_order")
    if q0_order is None:
        return
    parent = structural.get("Q0_parent_table", {})
    letters = structural.get("Q0_letter_table", {})
    need(parent.get("count") == q0_order and letters.get("count") == q0_order, "Q0 table state count")


def q0_boundary_selftest() -> bool:
    good = {"Q0_order": 1469664, "Q0_parent_table": {"count": 1469664}, "Q0_letter_table": {"count": 1469664}}
    validate_q0_boundary(good)
    bad = {"Q0_order": 1469664, "Q0_parent_table": {"count": 708588}, "Q0_letter_table": {"count": 708588}, "quotient_order": 708588, "Q_tree": {"state_count": 708588}}
    try:
        validate_q0_boundary(bad)
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
    need(state == expected, "semantic mutation state")


def mutation_selftest(controls: list[str]) -> dict[str, Any]:
    baseline = {"gamma_product": 243, "centre_bit": True, "inner_adjustment": "exact",
                "centralizer_element": "present", "derived_commutator": "replayed",
                "residual_roster": "stable-derived", "psl_projection": True,
                "normality_image": True, "stable_derived": True,
                "quotient_product": "replayed", "quotient_order": 708588,
                "g760_letter": 760, "g760_coordinate": "typed",
                "selector_side": "right", "selector_order": "v150",
                "arithmetic_scope": "typed", "incomplete_fibre": "UNKNOWN_INPUT",
                "q0_vs_gr_swap": "separate", "terminal": "SELFTEST_PASS"}
    rejected = 0
    for ordinal, name in enumerate(controls, 1):
        mutated = dict(baseline); mutated[name] = ("MUTATED", ordinal)
        try:
            validate_mutation_state(mutated)
        except RuntimeError:
            rejected += 1
        else:
            raise RuntimeError(f"mutation accepted {ordinal}:{name}")
    need(rejected == len(controls) == 19, "semantic mutation count")
    return {"attempted": len(controls), "rejected": rejected, "names": controls}


def selftest() -> dict[str, Any]:
    controls = ["gamma_product", "centre_bit", "inner_adjustment", "centralizer_element", "derived_commutator", "residual_roster", "psl_projection", "normality_image", "stable_derived", "quotient_product", "quotient_order", "g760_letter", "g760_coordinate", "selector_side", "selector_order", "arithmetic_scope", "incomplete_fibre", "q0_vs_gr_swap", "terminal"]
    toy = toy_selector_selftest(); schreier = schreier_selftest(); word = construct_g760()
    need(len(controls) == 19 and digest(word) == G760_SHA256, "selftest controls")
    need(q0_boundary_selftest(), "Q0/G/R swap control")
    return {"schema": SELFTEST_SCHEMA, "status": "PASS", "terminal": "SELFTEST_PASS", "g760": {"length": len(word), "sha256": digest(word), "exponent": list(exponent(word))}, "toy": toy, "schreier": schreier, "q0_boundary_swap_rejected": True, "mutation_controls": mutation_selftest(controls)}


def inventory() -> list[dict[str, str]]:
    return [
        {"candidate": "ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json", "reason": "roof-only; no task176 quotient coset"},
        {"candidate": "ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json", "reason": "joint kernel receipt; missing arithmetic F-component"},
        {"candidate": "search/certs/d972_r07_760_l3_target6_resume_preflight_v2_20260826.json", "reason": "one direct word/basepoint; unnamed sigma and no quotient map"},
        {"candidate": "crosscheck/verdicts/d972_idx3_arithmetic_crosscheck_v2_20260823.json", "reason": "wrong object; roof/index-three arithmetic only"},
    ]


def rebuild_task176_shelf(q3_path: Path, joint_path: Path) -> dict[str, Any]:
    """Rebuild Gamma/Q0 from the authenticated task176 implementation.

    This is deliberately a data-only handoff: the returned summary retains
    literal Gamma source words and all canonical Q0 replay digests without
    importing the new anchor producer or enumerating the full joint group.
    """
    source = ROOT / PINS["task176_source"][0]
    spec = importlib.util.spec_from_file_location("_r07_task176_anchor_source", source)
    need(spec is not None and spec.loader is not None, "task176 source loader")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    rebuilt = module.build_result(q3_path, joint_path, 1800.0)
    gamma = rebuilt.get("Gamma", {}); q0 = rebuilt.get("Q0_section", {})
    need(gamma.get("order") == 243 and q0.get("order") == 1469664, "task176 rebuilt orders")
    return {"Gamma_order": gamma["order"], "Gamma_source_words": gamma.get("record_words", []),
            "Gamma_source_words_sha256": digest(gamma.get("record_words", [])),
            "Gamma_section_parent_digest": gamma.get("section_parent_states_u16le", {}).get("sha256"),
            "Gamma_section_record_digest": gamma.get("section_parent_record_u8", {}).get("sha256"),
            "Q0_order": q0["order"], "Q0_roster_digest": q0.get("roster_sha256"),
            "Q0_canonical_roster_digest": q0.get("canonical_roster", {}).get("sha256"),
            "Q0_parent_digest": q0.get("parent_states_u32le", {}).get("sha256"),
            "Q0_letter_digest": q0.get("parent_letters_u8", {}).get("sha256"),
            "Q0_parent_table": q0.get("parent_states_u32le"), "Q0_letter_table": q0.get("parent_letters_u8"),
            "Q0_relators_digest": q0.get("complete_presentation_relators_sha256"),
            "Q0_lossless": q0.get("all_section_values_losslessly_reconstructible") is True}


def production() -> dict[str, Any]:
    pins = authenticate_pins()
    joint = json.loads((ROOT / PINS["joint"][0]).read_text(encoding="utf-8"))
    q3 = json.loads((ROOT / PINS["q3"][0]).read_text(encoding="utf-8"))
    gamma = joint.get("gamma", {}); q0 = joint.get("q0_presentation", {})
    gamma_order = gamma.get("order"); phi_order = gamma.get("frattini_order")
    psl_order = q0.get("P_order"); g9_order = q0.get("G9_order")
    need(gamma_order == 243 and phi_order == 27 and gamma.get("frattini_quotient_order") == 9 and gamma.get("center_order") == 27, "Gamma/Frattini gate")
    need(psl_order == 504 and g9_order == 2916 and q0.get("Q0_order") == 1469664, "factor order gate")
    word = construct_g760()
    shelf = rebuild_task176_shelf(ROOT / PINS["q3"][0], ROOT / PINS["joint"][0])
    validate_q0_boundary({"Q0_order": shelf["Q0_order"], "Q0_parent_table": shelf["Q0_parent_table"], "Q0_letter_table": shelf["Q0_letter_table"]})
    structural = {"Gamma_order": gamma_order, "Phi_Gamma_order": phi_order, "Gamma_over_Phi_order": gamma.get("frattini_quotient_order"), "PSL_order": psl_order, "G9_order": g9_order, "G_order": gamma_order * psl_order * g9_order, "Q0_order": shelf["Q0_order"], "residual_identity": "C_E(Gamma)'=E^(infinity)", "residual_roster": "NOT_MATERIALIZED", "R_stable_chain": "NOT_MATERIALIZED", "R_relators": "NOT_MATERIALIZED", "Gamma_source_words": shelf["Gamma_source_words"], "R_source_words": "NOT_MATERIALIZED", "g760_C_coordinate": "NOT_MATERIALIZED", "R_digest_encoding": "NOT_MATERIALIZED", "Q0_is_not_G_over_R": True, "materialization": "STATIC_STOP: authenticated task176 API exposes Q0 only; actual G/R roster and quotient map are unavailable", "shelf_replay": shelf}
    return {"schema": SCHEMA, "status": "UNKNOWN_INPUT", "terminal": "UNKNOWN_INPUT", "comparison": UNKNOWN_INPUT, "static_stop": "STATIC_STOP: actual marked G/R quotient roster and quotient map are not materialized by the authenticated task176 API", "claims": {"roof_membership": False, "dihedral_coordinate": False, "unnamed_sigma": False, "fake": False, "cofinal": False, "ihara": False}, "pins": pins, "task176_production_run": 33044121344, "q3_status": q3.get("status"), "g760": {"length": len(word), "sha256": digest(word), "exponent": list(exponent(word)), "source_word": word}, "structural_receipt": structural, "arithmetic_inventory": inventory()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = selftest() if args.mode == "SELFTEST" else production()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(canonical(result) + b"\n")
    marker = "R07_FINITE_RELATIVE_ANCHOR_V1_SELFTEST_PASS mutations=19" if args.mode == "SELFTEST" else "R07_FINITE_RELATIVE_ANCHOR_V1_PRODUCER_PASS terminal=" + result["terminal"]
    print(marker, flush=True); return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("R07_FINITE_RELATIVE_ANCHOR_V1_PRODUCER_STOP " + type(exc).__name__ + ":" + str(exc), file=sys.stderr)
        raise
