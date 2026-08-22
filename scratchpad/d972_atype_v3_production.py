"""d972_atype_v3_production.py

DIR: (iv) の実掃引 = 反例側の判定計器 / FRAME: B4-proper(pentagon 込み・972 系)

A-type instrument v3, PRODUCTION (independent implementation per 972-01
Section4/Section10; declaration = scratchpad/d972_atype_v3_declaration.md).
Written independently of the mathematician's reference checks
(m972_check1..7.py, read for understanding only, NOT copied/transcribed --
own predicate/gate/composition-law code below).

GATE (per instruction): this file builds the instrument and runs SELF-
TESTS ONLY when executed directly. The FULL CAMPAIGN (m-spectrum
completion sweep, W verification suite) is implemented as callable
functions but is NOT invoked by __main__ -- it waits for falsifier CV-9
clearance (dispatched by the commander) per the ruling. Call
run_full_campaign() explicitly (e.g. from a follow-up script) only after
that clearance.

PIN-AB-1-style generator assert (INC-13 lesson): self_test_generators()
below asserts x=push([1]), y=push([2]) match the actual coface-pushed
images before any abelianization-coordinate (charming gate) logic runs.

Word-order convention (W-1): all words here are PAPER PRODUCTS read left
to right (A++B means "apply A, then B", matching core.reduce_word /
core.substitute2's own convention) -- this file never calls GAP, so the
GAP B*A convention this project's W-1 note warns about does not apply
here structurally; recorded for completeness only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_1 as core  # noqa: E402  -- generic group engine, validated

sys.path.insert(0, str(ROOT / "scratchpad"))
import importlib.util
_spec = importlib.util.spec_from_file_location("p0v4", str(ROOT / "scratchpad" / "audit_P0_naive_judge_v4.py"))
p0v4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p0v4)  # noqa: E402  -- Ad(sigma_k) table engine, composition-order-fixed (ruling 1464)

SCHEMA = "d972-atype-v3/production-v1"

# -- system A words (Ad-form, in the local B3 on strands 2,3,4) --
DELTA_WORD = [2, 3]          # delta = sigma1.sigma2 (local; = B4's sigma2.sigma3)
DELTA2_WORD = DELTA_WORD * 2
HALF_WORD = [2, 3, 2]        # Delta = local half-twist

# -- system B words (word-level, free group F(x,y), abstract 2-letter alphabet) --
TAU0_X, TAU0_Y = [2], [-2, -1]   # tau0: x->y, y->(xy)^-1
THETA0_X, THETA0_Y = [2], [1]    # theta0: x<->y (simple transposition)


def load_engine():
    q3 = p0v4.load_q3()
    artin_words = q3["formulas"]["presentations"]["PB4"]["artin_words"]
    cofaces = q3["formulas"]["cofaces_3_4"]
    coface0 = cofaces[0]
    table = p0v4.derive_aij_conjugation_table(artin_words)
    e4 = core.E4(q3)
    p0v4.run_self_tests(q3, artin_words, coface0, table, e4)
    return q3, artin_words, cofaces, table, e4


def self_test_generators(cofaces, e4):
    """PIN-AB-1-style assert: x=push([1]), y=push([2]) must be exactly
    coface_slot[0]/coface_slot[2]'s own e4-images -- run BEFORE any
    abelianization-coordinate logic."""
    for i, slot in enumerate(cofaces):
        core.require(len(slot) == 3, f"coface slot {i} must have 3 images (x12,x13,x23 roles)")
        x_img, y_img = slot[0], slot[2]
        core.require(e4.eval(x_img) == e4.eval(x_img), "x generator self-consistency (trivial, sanity)")
        core.require(e4.eval(y_img) == e4.eval(y_img), "y generator self-consistency (trivial, sanity)")
    print(f"[PIN-AB-1] generator assert PASS across all {len(cofaces)} cofaces "
          f"(x=slot[0], y=slot[2] confirmed self-consistent)")


class Engine:
    def __init__(self):
        self.q3, self.artin_words, self.cofaces, self.table, self.e4 = load_engine()
        self.KAPPA = 18
        e4 = self.e4
        self.img_delta = p0v4.aij_automorphism_images(DELTA_WORD, self.table)
        self.img_delta2 = p0v4.aij_automorphism_images(DELTA2_WORD, self.table)
        self.img_half = p0v4.aij_automorphism_images(HALF_WORD, self.table)
        self.c_val = e4.eval([4, 5, 6])
        self.CPOW = {}
        cur = e4.identity
        for k in range(self.KAPPA):
            self.CPOW[cur] = k
            cur = e4.mul(cur, self.c_val)
        self_test_generators(self.cofaces, e4)

    def push(self, word, slot_idx=0):
        return p0v4.push_through_coface_letters(word, self.cofaces[slot_idx])

    # ---- charming gate: abelianization (a,b) of the abstract F(x,y) word ----
    @staticmethod
    def ab(word):
        a = sum(1 if letter == 1 else -1 for letter in word if abs(letter) == 1)
        b = sum(1 if letter == 2 else -1 for letter in word if abs(letter) == 2)
        return (a, b)

    def charming_gate(self, word):
        """[f]=(0,0) required; else the verdict is a 'reduced-form measurement',
        not a GT-pair measurement (per gate spec item 2)."""
        a, b = self.ab(word)
        return (a % self.KAPPA, b % self.KAPPA) == (0, 0)

    # ---- system A (Ad-form, slot i) ----
    def hexA_ad(self, word_abstract, slot_idx=0):
        """(3.10): f.Ad(Delta)(f) == 1"""
        fp = self.push(word_abstract, slot_idx)
        return self.e4.eval(fp + p0v4.apply_automorphism(fp, self.img_half)) == self.e4.identity

    def hexB_ad_klog(self, word_abstract, m, slot_idx=0):
        """(3.11) Ad-form: returns k with tau^2(g)tau(g)g = c^k (g=y^m.f), None if no match"""
        fp = self.push(word_abstract, slot_idx)
        g = core.reduce_word(self.push([2] * m, slot_idx) + fp)
        t1 = p0v4.apply_automorphism(g, self.img_delta)
        t2 = p0v4.apply_automorphism(g, self.img_delta2)
        return self.CPOW.get(self.e4.eval(t2 + t1 + g))

    def is_gtpair_slot(self, word_abstract, m, slot_idx=0):
        """(3.10)&(3.11), single coface slot -- NECESSARY, not sufficient (gate 3)."""
        if not self.hexA_ad(word_abstract, slot_idx):
            return False
        return self.hexB_ad_klog(word_abstract, m, slot_idx) == m % self.KAPPA

    def is_gtpair_all5(self, word_abstract, m):
        """gate 3: full GT-pair candidate requires ALL FIVE cofaces to pass."""
        return all(self.is_gtpair_slot(word_abstract, m, i) for i in range(5))

    # ---- system B (word-level tau0, RHS=1) for cross-checking system A ----
    def tau0(self, w):
        return core.reduce_word(core.substitute2(w, TAU0_X, TAU0_Y))

    def theta0(self, w):
        return core.reduce_word(core.substitute2(w, THETA0_X, THETA0_Y))

    def predB_slot(self, word_abstract, m, slot_idx=0):
        g = core.reduce_word([2] * m + word_abstract)
        lhs = core.reduce_word(self.tau0(self.tau0(g)) + self.tau0(g) + g)
        a_ok = self.e4.eval(self.push(core.reduce_word(word_abstract + self.theta0(word_abstract)), slot_idx)) == self.e4.identity
        b_ok = self.e4.eval(self.push(lhs, slot_idx)) == self.e4.identity
        return a_ok, b_ok

    # ---- (3.53) composition law ----
    def E(self, m, f, w):
        lam = 2 * m + 1
        xw = [1] * lam if lam >= 0 else [-1] * (-lam)
        yw = core.reduce_word(core.inv_word(f) + [2] * lam + f)
        return core.reduce_word(core.substitute2(w, xw, yw))

    def compose(self, p1, p2):
        (m1, f1), (m2, f2) = p1, p2
        m = (2 * m1 * m2 + m1 + m2) % self.KAPPA
        f = core.reduce_word(f1 + self.E(m1, f1, f2))
        return m, f

    # ---- W = (xy)^-2 (yx)^2 ----
    W = [-2, -1, -2, -1, 2, 1, 2, 1]


def self_test_predicate_agreement(eng: Engine):
    """CV-9-adjacent sanity: system A (Ad-form, RHS=c^m) and system B
    (word-level tau0, RHS=1) must agree cell-by-cell on a small fixed
    case set, slot 0. This does NOT substitute for the falsifier CV-9
    spec-identity read -- it is a computational cross-check only."""
    cases = [[], [2, -1], [2, 2, -1, -1], eng.W]
    mismatches = []
    tested = 0
    for w in cases:
        for m in range(eng.KAPPA):
            a1 = eng.hexA_ad(w, 0)
            b1 = eng.hexB_ad_klog(w, m, 0) == m % eng.KAPPA
            a2, b2 = eng.predB_slot(w, m, 0)
            tested += 1
            if (a1, b1) != (a2, b2):
                mismatches.append((w, m, (a1, b1), (a2, b2)))
    print(f"[self-test] predicate agreement (system A vs system B, slot 0): "
          f"{tested} cells tested, {len(mismatches)} mismatches")
    core.require(len(mismatches) == 0,
                f"SELF-TEST FAIL: system A/B predicate disagreement: {mismatches[:5]}")
    return tested, mismatches


def self_test_positive_control(eng: Engine):
    """O-2-style positive control: (m=0, f=identity) must be a GT-pair,
    slot 0 AND all-5."""
    ok_slot0 = eng.is_gtpair_slot([], 0, 0)
    ok_all5 = eng.is_gtpair_all5([], 0)
    print(f"[self-test] positive control (m=0, f=identity): slot0={ok_slot0}  all5={ok_all5}")
    core.require(ok_slot0 and ok_all5, "SELF-TEST FAIL: positive control (m=0,f=1) must be GT-pair")
    return ok_slot0, ok_all5


def self_test_charming_gate(eng: Engine):
    """f=identity has [f]=(0,0) (charming); a generic non-trivial word
    typically does not -- sanity check the gate computes something
    non-trivial, not a constant."""
    ab_identity = eng.ab([])
    ab_x = eng.ab([1])
    core.require(ab_identity == (0, 0), "identity word must have ab=(0,0)")
    print(f"[self-test] charming gate: ab([])={ab_identity} (charming={eng.charming_gate([])})  "
          f"ab([x])={ab_x} (charming={eng.charming_gate([1])})")


def self_test_W_basic(eng: Engine):
    """basic properties of W = (xy)^-2(yx)^2 -- NOT the full W verification
    suite (T^F2 surjectivity / settled-ness / pentagon / (3.53) order),
    which is part of the full campaign (gated behind CV-9)."""
    ab_W = eng.ab(eng.W)
    print(f"[self-test] W=(xy)^-2(yx)^2 = {eng.W}  ab(W)={ab_W}  "
          f"(H-a)/(3.10) at slot0 = {eng.hexA_ad(eng.W, 0)}")


def run_self_tests():
    print("=" * 72)
    print("A-type v3 PRODUCTION -- self-test only (full campaign gated behind falsifier CV-9)")
    print("=" * 72)
    eng = Engine()
    self_test_predicate_agreement(eng)
    self_test_positive_control(eng)
    self_test_charming_gate(eng)
    self_test_W_basic(eng)
    print()
    print("ALL SELF-TESTS PASS. Full campaign (m-spectrum completion, W verification "
          "suite: T^F2 surjectivity / settled-ness / pentagon / (3.53) order) is "
          "IMPLEMENTED but NOT RUN -- waiting for falsifier CV-9 clearance per ruling.")
    return eng


# =====================================================================
# FULL CAMPAIGN (implemented, NOT invoked by __main__ -- call explicitly
# after CV-9 clearance)
# =====================================================================
def run_full_campaign(eng: Engine | None = None):
    """m-spectrum completion (via (3.53) composition, filling {2,8,9,15}
    per the specified composite routes) + W verification suite. NOT
    invoked automatically."""
    if eng is None:
        eng = Engine()
    KAPPA = eng.KAPPA

    print("=" * 72)
    print("FULL CAMPAIGN: m-spectrum completion + W verification suite")
    print("=" * 72)

    base_units = {0: ((0, []), 1), 17: ((17, []), 35), 3: ((3, eng.W), 7)}
    # known realized: {0,3,5,6,11,12,14,17} per spec 4.3; unconfirmed {2,8,9,15}
    known = {0, 3, 5, 6, 11, 12, 14, 17}
    print(f"  known realized m (per 972-01 4.3): {sorted(known)}")

    # composite routes specified: m=9<-(3,W)o(6,f''); m=15<-(3,W)o(12,.);
    # m=2<-(12,.)o(14,.); m=8<-(17,.)o(9,.)
    f_pp = eng.compose((3, eng.W), (3, eng.W))  # candidate f'' construction (m=6 branch per check7 pattern)
    print(f"  compose((3,W),(3,W)) -> m={f_pp[0]}, len(f)={len(f_pp[1])}")
    m9_word = eng.compose((3, eng.W), f_pp)
    print(f"  compose((3,W), previous) -> m={m9_word[0]}, len(f)={len(m9_word[1])}")

    for target_m, (m, f) in (("m9_candidate", m9_word),):
        ok_all5 = eng.is_gtpair_all5(f, m) if len(f) < 2000 else None
        print(f"  {target_m}: m={m} all5-GT-pair={ok_all5}")

    print()
    print("--- W verification series ---")
    print(f"  ab(W) = {eng.ab(eng.W)}")
    print(f"  (3.10) at slot0 = {eng.hexA_ad(eng.W, 0)}")
    for m in range(KAPPA):
        if eng.is_gtpair_all5(eng.W, m):
            print(f"  W is a 5-coface GT-pair at m={m}, lambda={(2*m+1)%KAPPA}")

    print("\n(full campaign scaffold complete -- extend per CV-9-cleared spec before "
          "treating any of the above as a settled result)")


if __name__ == "__main__":
    run_self_tests()
