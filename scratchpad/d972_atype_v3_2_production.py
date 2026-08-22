"""d972_atype_v3_2_production.py

DIR: (iv) の実掃引 = 反例側の判定計器 / FRAME: B4-proper(pentagon 込み・972 系)

A-type instrument v3.2 -- repair pass after falsifier CV-9 second read
(verdict: GO with scope, pending 3 launch-gate repairs + claim corrections).
v3 and v3_1 are left UNTOUCHED (CV-9 evidence artifacts). This is a NEW file.

*** URGENT SIDE-FINDING (discovered while implementing this repair, NOT
part of the ordered repair list -- flagged prominently, reported
separately, NOT silently patched in production) ***
search/koubou158_L3_core_v1_1.py's IndependentPc.inverse() has a latent
bug: it loops idx from self.n(=10) down to 1 and indexes
self._inv_gen[idx-1], but self._inv_gen is built ONLY from
pb4["marked_generators"] (6 entries -- the weight-1 generators), NOT all
10 PC generators. For any element whose pc-coordinate has a NONZERO
exponent at one of the 4 "weight-2" positions (indices 7..10, i.e.
_inv_gen[6..9]), inverse() raises IndexError (self._inv_gen only has 6
elements). This has NOT bitten prior work in this session because every
element actually inverted so far happened to have zero weight-2
coordinates -- but it is a REAL, production bug, not something specific
to this file. WORKAROUND USED HERE (scratchpad only, NOT a production
fix): Pi4[3] has exponent 3, so for ANY pc element p, p^-1 = p^2 exactly
-- safe_e4_inverse() below computes the pc part via self-multiplication
(squaring) instead of calling the buggy core.pc.inverse(). This should be
reported to the commander/mathematician as a standalone finding requiring
a production patch decision -- NOT something this implementer will fix in
search/koubou158_L3_core_v1_1.py without instruction.

REPAIRS IN THIS FILE (commander's ordered list, referencing falsifier's
second CV-9 read):
  1. CAP REMOVED. v3_1's gate3/gate4 evaluation used a `len(f)<1500/2000`
     silent cap that forced UNKNOWN cases to False -- this is exactly why
     v3_1 measured 28/36 gate4 closure instead of the true 36/36 (falsifier
     confirmed cap-free). FIX: predB_fast() below evaluates
     tau0^k(g) DIRECTLY AS AN e4 VALUE without ever materializing the
     (potentially huge, since tau0 substitution roughly triples word
     length per application and (3.53) composition can compound this
     further) substituted word -- push-then-eval is a homomorphism
     F2->e4, so each of x,y's IMAGE under tau0^k (k=0,1,2, tau0 has order
     3: (x,y)->(y,(xy)^-1)->((xy)^-1,x)->(x,y)) can be precomputed ONCE
     per slot, and then ANY word (arbitrarily long) is evaluated in O(len)
     time by folding letter-by-letter through those two fixed images --
     THIS is the "linear evaluator" the commander's algorithm sketch
     describes (cv9_probe4.py's fast_slot referenced for the IDEA only,
     not read/transcribed here -- this implementation was derived
     independently from the homomorphism argument in the ordering
     message). Where a genuine cap would still be needed (there is none
     left in this file), the rule is UNKNOWN (recorded, not coerced to
     False) -- not exercised here since the linear evaluator has no
     length-dependent cost blowup.
  2. m-spectrum routes replaced with REAL witnesses: m=9 <- compose((14,W),
     (11,f'')); m=8 <- compose((14,W),(6,f'')) (both confirmed ALL5=True
     below). m=2, m=15 candidate routes via (3,W) composed with grid
     witnesses at m=5,12 were ATTEMPTED; f5/f12 were NOT found among the
     already-known witnesses (W and f'' alone do NOT realize m=5 or m=12
     directly -- confirmed by direct measurement below) -- reported as
     UNKNOWN (not guessed, not silently dropped) rather than fabricating
     a witness.
  3. w_verification_series EXCLUDED from the campaign entirely (per
     instruction) -- not called anywhere in run_launch_campaign().

CLAIM CORRECTIONS (v3_1's self-reports vs actual code, per falsifier):
  4. regression oracle now uses REAL core.require() (raises on any
     witness-table mismatch) -- not print-only.
  5. slot 0..4 dead-loop removed; system-A/B cross-check is explicitly
     SLOT-0-ONLY (system A has no slot1-4 formulation) -- cert grade
     literally says "candidate, single-system at slots 1-4" per
     falsifier's required wording.
  6. all THREE destructive controls are now core.require-backed asserts:
     (a) theta-false-but-charming word (commutator [x,y] is charming but
         DOES satisfy f.theta0(f)=1 in this specific case -- see below,
         reported honestly; a genuinely theta-breaking charming word was
         constructed instead, see theta_false_charming_word()),
     (b) non-charming word correctly quarantined,
     (c) charming-but-not-GT-pair word correctly rejected.
  7. naive-product control expectation corrected to 25/25 -- the lambda=1
     row/column (11 of the 36 cells: 6+6-1 for the diagonal overlap) is
     algebraically non-discriminating (identity composed with anything
     reduces to no real test) and is EXCLUDED from the control count, not
     silently included as a inflated denominator.
  8. lambda = (2*m+1) % 18 with a centered representative (range
     [-8,9]) used in E()'s exponent to keep word length from blowing up
     -- mathematically identical since ord(x)=18 in e4 (x^lam depends
     only on lam mod 18).
  9. gtpair_all5_raw (the bare predicate) kept SEPARATE from the
     charming-gated verdict at all call sites (no field conflation).
  10. universe_digest computed from actual content (family names, witness
      words, predicate_version) and written into the cert; one-line
      cross-check against core.Q3_CHIEF_SHA recorded.

LAUNCH SCOPE (per falsifier's recommendation, strictly enforced): this
file's run_launch_campaign() does ONLY (a) gate4 (3.53) closure
calibration (target 36/36) (b) m-spectrum sweep with REAL witnesses
(target 12/12, 2 of 4 gaps reported UNKNOWN per finding #2) (c) cert
issuance. W verification series is OUT OF SCOPE this round (item 3).
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_1 as core  # noqa: E402

sys.path.insert(0, str(ROOT / "scratchpad"))
import importlib.util
_spec = importlib.util.spec_from_file_location("p0v4", str(ROOT / "scratchpad" / "audit_P0_naive_judge_v4.py"))
p0v4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p0v4)  # noqa: E402

SCHEMA = "d972-atype-v3_2/production-v1"
PREDICATE_VERSION = "v3_2-launch-gate-repair-post-CV9-second-read"
KAPPA = 18
W_WORD = [-2, -1, -2, -1, 2, 1, 2, 1]


def safe_e4_inverse(e4, v):
    """WORKAROUND for the core.py IndependentPc.inverse() bug (see module
    docstring) -- Pi4[3] has exponent 3, so pc^-1 = pc^2 (self-mul), which
    NEVER touches the buggy self._inv_gen indexing path."""
    perm_inv_part = core.perm_inv(v[0])
    pc_sq = e4.pc.mul(v[1], v[1])
    return (perm_inv_part, pc_sq)


def order_of(e4, val, cap=400):
    cur = val
    for k in range(1, cap + 1):
        if cur == e4.identity:
            return k
        cur = e4.mul(cur, val)
    return None


class Engine:
    def __init__(self):
        self.q3 = p0v4.load_q3()
        self.artin_words = self.q3["formulas"]["presentations"]["PB4"]["artin_words"]
        self.cofaces = self.q3["formulas"]["cofaces_3_4"]
        self.table = p0v4.derive_aij_conjugation_table(self.artin_words)
        self.e4 = core.E4(self.q3)
        p0v4.run_self_tests(self.q3, self.artin_words, self.cofaces[0], self.table, self.e4)

        e4 = self.e4
        self.KAPPA = KAPPA
        self.img_delta = p0v4.aij_automorphism_images([2, 3], self.table)
        self.img_delta2 = p0v4.aij_automorphism_images([2, 3, 2, 3], self.table)
        self.img_half = p0v4.aij_automorphism_images([2, 3, 2], self.table)
        self.c_val = e4.eval([4, 5, 6])
        c_order = order_of(e4, self.c_val)
        core.require(c_order == self.KAPPA, f"ord(c)={c_order} != KAPPA={self.KAPPA}")
        self.CPOW = {}
        cur = e4.identity
        for k in range(self.KAPPA):
            self.CPOW[cur] = k
            cur = e4.mul(cur, self.c_val)
        core.require(len(self.CPOW) == self.KAPPA, f"len(CPOW)={len(self.CPOW)} != {self.KAPPA}")

        # PIN-AB-1 real assert (ord(x)=ord(y)=18 at every coface)
        self.slot_xy_orders = []
        for i, slot in enumerate(self.cofaces):
            ox = order_of(e4, e4.eval(slot[0]))
            oy = order_of(e4, e4.eval(slot[2]))
            self.slot_xy_orders.append((i, ox, oy))
            core.require(ox == 18 and oy == 18, f"PIN-AB-1 FAIL at slot {i}: ord(x)={ox} ord(y)={oy}")
        print(f"[PIN-AB-1] ord(x)=ord(y)=18 at all 5 cofaces: {self.slot_xy_orders}")

        # precompute per-slot tau0-cycle images (x_k,y_k), k=0,1,2 -- this
        # is the linear-evaluator core (fix item 1)
        self.tau0_cycle = []  # per slot: [(x0,y0),(x1,y1),(x2,y2)]
        for slot in self.cofaces:
            x0 = e4.eval(p0v4.push_through_coface_letters([1], slot))
            y0 = e4.eval(p0v4.push_through_coface_letters([2], slot))
            xy = e4.mul(x0, y0)
            xy_inv = safe_e4_inverse(e4, xy)
            x1, y1 = y0, xy_inv          # tau0: x->y, y->(xy)^-1
            x2, y2 = xy_inv, x0          # tau0^2: x->(xy)^-1, y->x
            self.tau0_cycle.append([(x0, y0), (x1, y1), (x2, y2)])

    def push(self, word, slot_idx=0):
        return p0v4.push_through_coface_letters(word, self.cofaces[slot_idx])

    @staticmethod
    def ab(word):
        a = sum(1 if letter == 1 else -1 for letter in word if abs(letter) == 1)
        b = sum(1 if letter == 2 else -1 for letter in word if abs(letter) == 2)
        return (a, b)

    def charming_gate(self, word):
        a, b = self.ab(word)
        return (a % self.KAPPA, b % self.KAPPA) == (0, 0)

    def _eval_via(self, word, x_val, y_val):
        """evaluate an abstract F(x,y) word directly as an e4 element,
        given fixed images x_val,y_val for the two generators -- O(len(word)),
        NEVER materializes a substituted word."""
        e4 = self.e4
        val = e4.identity
        for letter in word:
            if letter == 1:
                val = e4.mul(val, x_val)
            elif letter == -1:
                val = e4.mul(val, safe_e4_inverse(e4, x_val))
            elif letter == 2:
                val = e4.mul(val, y_val)
            elif letter == -2:
                val = e4.mul(val, safe_e4_inverse(e4, y_val))
            else:
                raise RuntimeError(f"bad letter {letter}")
        return val

    # ---- system A (Ad-form) -- slot0-only, kept for cross-check ----
    def hexA_ad(self, word_abstract, slot_idx=0):
        fp = self.push(word_abstract, slot_idx)
        return self.e4.eval(fp + p0v4.apply_automorphism(fp, self.img_half)) == self.e4.identity

    def hexB_ad_klog(self, word_abstract, m, slot_idx=0):
        fp = self.push(word_abstract, slot_idx)
        g = core.reduce_word(self.push([2] * m, slot_idx) + fp)
        t1 = p0v4.apply_automorphism(g, self.img_delta)
        t2 = p0v4.apply_automorphism(g, self.img_delta2)
        return self.CPOW.get(self.e4.eval(t2 + t1 + g))

    def gtpair_A_slot0(self, word_abstract, m):
        if not self.hexA_ad(word_abstract, 0):
            return False
        return self.hexB_ad_klog(word_abstract, m, 0) == m % self.KAPPA

    # ---- system B, LINEAR (fix item 1) ----
    def predB_fast(self, word_abstract, m, slot_idx):
        e4 = self.e4
        x0, y0 = self.tau0_cycle[slot_idx][0]
        x1, y1 = self.tau0_cycle[slot_idx][1]
        x2, y2 = self.tau0_cycle[slot_idx][2]
        theta_x, theta_y = y0, x0  # theta0: x<->y
        # f.theta0(f): evaluate f under (x0,y0), then theta0(f) under (theta_x,theta_y), multiply
        f_val = self._eval_via(word_abstract, x0, y0)
        thf_val = self._eval_via(word_abstract, theta_x, theta_y)
        a_ok = e4.mul(f_val, thf_val) == e4.identity
        # tau0^2(g).tau0(g).g , g = y^m.f : evaluate g three times under (x2,y2),(x1,y1),(x0,y0)
        g = core.reduce_word([2] * m + word_abstract)
        g2 = self._eval_via(g, x2, y2)
        g1 = self._eval_via(g, x1, y1)
        g0 = self._eval_via(g, x0, y0)
        b_ok = e4.mul(e4.mul(g2, g1), g0) == e4.identity
        return a_ok, b_ok

    def gtpair_B_slot(self, word_abstract, m, slot_idx):
        a_ok, b_ok = self.predB_fast(word_abstract, m, slot_idx)
        return a_ok and b_ok

    def is_gtpair_all5(self, word_abstract, m):
        return all(self.gtpair_B_slot(word_abstract, m, i) for i in range(5))

    def verdict(self, word_abstract, m):
        """fix item 9: raw predicate kept separate from charming-gated tag."""
        raw = self.is_gtpair_all5(word_abstract, m)
        charming = self.charming_gate(word_abstract)
        if not charming:
            return {"charming": False, "gtpair_all5_raw": raw, "gtpair_all5_gated": None,
                    "tag": "REDUCED-FORM MEASUREMENT, NOT A GT-PAIR MEASUREMENT "
                           "([f] != (0,0))"}
        return {"charming": True, "gtpair_all5_raw": raw, "gtpair_all5_gated": raw,
                "tag": "GT-PAIR CANDIDATE" if raw else "NOT A GT-PAIR (charming, predicate fails)"}

    # ---- (3.53), fix item 8: centered lambda representative ----
    def E(self, m, f, w):
        lam_raw = (2 * m + 1) % self.KAPPA
        lam = lam_raw if lam_raw <= self.KAPPA // 2 else lam_raw - self.KAPPA
        xw = [1] * lam if lam >= 0 else [-1] * (-lam)
        y_pow = [2] * lam if lam >= 0 else [-2] * (-lam)  # BUG FIX: [2]*lam silently
        # gives [] for negative lam in Python (list*negative_int == []) -- must build
        # the negative-power word explicitly, same as xw does, or the conjugating
        # element yw silently loses its y^lam factor entirely for lam<0.
        yw = core.reduce_word(core.inv_word(f) + y_pow + f)
        return core.reduce_word(core.substitute2(w, xw, yw))

    def compose(self, p1, p2):
        (m1, f1), (m2, f2) = p1, p2
        m = (2 * m1 * m2 + m1 + m2) % self.KAPPA
        f = core.reduce_word(f1 + self.E(m1, f1, f2))
        return m, f


def build_f_double_prime(eng: Engine):
    return eng.compose((3, W_WORD), (3, W_WORD))


def theta_false_charming_word():
    """fix item 6a: a word that IS charming ([f]=(0,0)) but DOES break
    f.theta0(f)=1. The commutator [x,y]=x.y.x^-1.y^-1 turned out (checked
    directly) to SATISFY theta0-symmetry in this specific quotient (honest
    report, not the intended counter-example) -- so a longer, less
    symmetric charming word is used instead: (x.y.x^-1.y^-1).(x.y^-1.x^-1.y)
    (product of two DIFFERENT commutators, still charming, structurally
    asymmetric under x<->y)."""
    c1 = [1, 2, -1, -2]
    c2 = [1, -2, -1, 2]
    return core.reduce_word(c1 + c2)


def self_test_predicate_agreement_slot0_only(eng: Engine):
    """fix item 5: system A vs B cross-check is explicitly SLOT-0-ONLY
    (dead loop removed -- no fake iteration over slots 1-4 for system A,
    which has no such formulation)."""
    cases = [[], [2, -1], [2, 2, -1, -1], W_WORD]
    tested = mism = 0
    for w in cases:
        for m in range(eng.KAPPA):
            a1 = eng.gtpair_A_slot0(w, m)
            b1 = eng.gtpair_B_slot(w, m, 0)
            tested += 1
            if a1 != b1:
                mism += 1
    print(f"[self-test] system A/B conjunction agreement, SLOT 0 ONLY (structural -- "
          f"system A has no slot1-4 formulation): {tested} cells, {mism} mismatches")
    core.require(mism == 0, f"A/B mismatch at slot0: {mism}")
    return tested, mism


def self_test_positive_control(eng: Engine):
    v = eng.verdict([], 0)
    print(f"[self-test] positive control (m=0, f=identity): {v}")
    core.require(v["charming"] and v["gtpair_all5_gated"], "positive control must be charming GT-pair")


def self_test_destructive_controls(eng: Engine):
    """fix item 6: all THREE as real core.require asserts."""
    # (a) theta-false-but-charming
    tf = theta_false_charming_word()
    ab_tf = Engine.ab(tf)
    a_ok0, _ = eng.predB_fast(tf, 0, 0)
    print(f"[destructive-a] theta-probe word {tf} ab={ab_tf} charming={eng.charming_gate(tf)} "
          f"f.theta0(f)==1 at slot0? {a_ok0}")
    core.require(eng.charming_gate(tf), "destructive-a word must be charming (test design)")
    core.require(not a_ok0, "destructive-a FAILED: expected theta0-condition to break for this word, "
                           "but it held -- word choice needs revision, NOT silently accepted")

    # (b) non-charming word must be quarantined
    non_charming = [2, -1]
    v_b = eng.verdict(non_charming, 0)
    print(f"[destructive-b] non-charming y.x^-1: {v_b}")
    core.require(not v_b["charming"], "destructive-b: y.x^-1 must be flagged non-charming")
    core.require("REDUCED-FORM" in v_b["tag"], "destructive-b: must carry reduced-form tag")

    # (c) charming-but-not-GT-pair word must be rejected
    comm = core.reduce_word([1, 2] + core.inv_word([1]) + core.inv_word([2]))
    v_c = eng.verdict(comm, 5)
    print(f"[destructive-c] commutator @ m=5: {v_c}")
    core.require(v_c["charming"], "destructive-c word must be charming")
    core.require(not v_c["gtpair_all5_gated"], "destructive-c: expected NOT a GT-pair at m=5")


def self_test_regression_oracle(eng: Engine):
    """fix item 4: REAL core.require, not print-only."""
    m_fpp, f_pp = build_f_double_prime(eng)
    print(f"[regression] f'' = compose((3,W),(3,W)) -> m={m_fpp}, len(f'')={len(f_pp)}")
    witnesses = [
        ("f=1", [], 0), ("f=1", [], 17),
        ("W", W_WORD, 3), ("W", W_WORD, 14),
        ("f''", f_pp, 6), ("f''", f_pp, 11),
    ]
    results = []
    for name, f, m in witnesses:
        v = eng.verdict(f, m)
        lam = (2 * m + 1) % eng.KAPPA
        ok = bool(v["charming"] and v["gtpair_all5_gated"])
        results.append({"name": name, "m": m, "lambda": lam, "charming": v["charming"],
                       "gtpair_all5": v["gtpair_all5_gated"], "pass": ok})
        print(f"[regression] {name} @ m={m} (lambda={lam}): charming={v['charming']} "
              f"gtpair_all5={v['gtpair_all5_gated']}  pass={ok}")
        core.require(ok, f"REGRESSION ORACLE FAIL: witness {name}@m={m} did not reproduce spec 4.3")
    print(f"[regression] witness table: {len(results)}/{len(results)} PASS (hard-asserted)")
    return results


def self_test_closure_calibration(eng: Engine):
    """fix item 2/7: gate4 across 6 lambda classes, cap-free (linear
    evaluator), naive-product control corrected to 25/25 (lambda=1
    row/col excluded, non-discriminating)."""
    m_fpp, f_pp = build_f_double_prime(eng)
    bases = {1: (0, []), 17: (17, []), 7: (3, W_WORD), 11: (14, W_WORD),
            13: (6, f_pp), 5: (11, f_pp)}
    print(f"[gate4] (3.53) closure across 6 lambda classes: {sorted(bases)}")
    closure_ok = {}
    naive_fail = {}
    naive_excluded = set()
    for lam1, p1 in bases.items():
        for lam2, p2 in bases.items():
            m, f = eng.compose(p1, p2)
            v = eng.verdict(f, m)
            closure_ok[(lam1, lam2)] = bool(v["gtpair_all5_gated"])
            if lam1 == 1 or lam2 == 1:
                naive_excluded.add((lam1, lam2))
                continue
            naive_f = core.reduce_word(p1[1] + p2[1])
            naive_m = (p1[0] + p2[0]) % eng.KAPPA
            vn = eng.verdict(naive_f, naive_m)
            naive_fail[(lam1, lam2)] = not bool(vn["gtpair_all5_gated"])
    n_closed, n_total = sum(closure_ok.values()), len(closure_ok)
    n_naive_fail, n_naive_total = sum(naive_fail.values()), len(naive_fail)
    print(f"[gate4] (3.53)-composed pairs closed (GT-pair again): {n_closed}/{n_total}")
    print(f"[gate4] naive-product control fails (excluding {len(naive_excluded)} "
          f"lambda=1-involving cells, non-discriminating): {n_naive_fail}/{n_naive_total}")
    if n_closed < n_total:
        bad = [k for k, v in closure_ok.items() if not v]
        print(f"[gate4] NOT-closed cells (reported, not masked): {bad}")
    return closure_ok, naive_fail, naive_excluded


def m_spectrum_completion(eng: Engine):
    """fix item 2: real witnesses for m=9,8; m=2,15 reported UNKNOWN
    (f5/f12 not found among known witnesses -- confirmed directly, not
    guessed)."""
    m_fpp, f_pp = build_f_double_prime(eng)
    out = {}

    # confirm W,f'' do NOT directly realize m=5,12 (so no f5/f12 available yet)
    w_at_12 = eng.is_gtpair_all5(W_WORD, 12)
    w_at_5 = eng.is_gtpair_all5(W_WORD, 5)
    fpp_at_12 = eng.is_gtpair_all5(f_pp, 12)
    fpp_at_5 = eng.is_gtpair_all5(f_pp, 5)
    print(f"[m-spectrum] direct check: W@m=12={w_at_12} W@m=5={w_at_5} "
          f"f''@m=12={fpp_at_12} f''@m=5={fpp_at_5}")

    m9, f9 = eng.compose((14, W_WORD), (11, f_pp))
    ok9 = eng.is_gtpair_all5(f9, m9)
    out["m9"] = {"route": "compose((14,W),(11,f''))", "m": m9, "len_f": len(f9), "all5": ok9}
    print(f"[m-spectrum] m9 route -> m={m9} all5={ok9}")

    m8, f8 = eng.compose((14, W_WORD), (6, f_pp))
    ok8 = eng.is_gtpair_all5(f8, m8)
    out["m8"] = {"route": "compose((14,W),(6,f''))", "m": m8, "len_f": len(f8), "all5": ok8}
    print(f"[m-spectrum] m8 route -> m={m8} all5={ok8}")

    out["m15"] = {"route": "compose((3,W),(12,f12))", "status": "UNKNOWN -- f12 not identified "
                 "(W and f'' do not directly realize m=12; not guessed)"}
    out["m2"] = {"route": "compose((3,W),(5,f5))", "status": "UNKNOWN -- f5 not identified "
                "(W and f'' do not directly realize m=5; not guessed)"}
    print(f"[m-spectrum] m15, m2: UNKNOWN (f12/f5 not identified this round, reported honestly)")
    return out


def compute_universe_digest(families, witness_words):
    blob = json.dumps({"families": sorted(families), "witnesses": witness_words,
                      "predicate_version": PREDICATE_VERSION},
                     sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def write_cert(eng, reg_results, closure_ok, naive_fail, naive_excluded, m_spectrum):
    q3_full = ROOT / core.Q3_CHIEF
    q3_sha_measured = core.sha_file(q3_full)
    q3_sha_matches_pin = q3_sha_measured == core.Q3_CHIEF_SHA
    families = ["identity", "W", "f_double_prime"]
    witnesses = {"f=1": [], "W": W_WORD, "f''": build_f_double_prime(eng)[1]}
    udigest = compute_universe_digest(families, witnesses)

    cert = {
        "schema": SCHEMA,
        "predicate_version": PREDICATE_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "provenance": {"q3_sha256_measured": q3_sha_measured, "q3_sha256_matches_pin": q3_sha_matches_pin,
                     "q3_path": str(core.Q3_CHIEF).replace("\\", "/")},
        "universe_digest": udigest,
        "urgent_side_finding": "search/koubou158_L3_core_v1_1.py IndependentPc.inverse() "
                              "raises IndexError for pc elements with nonzero weight-2 "
                              "coordinate (self._inv_gen has only 6 entries, indexed up "
                              "to 10) -- worked around HERE via safe_e4_inverse "
                              "(exponent-3 squaring), NOT patched in production. "
                              "Reported separately for a production-patch decision.",
        "regression_oracle": {"results": reg_results, "all_pass": all(r["pass"] for r in reg_results)},
        "gate4_closure": {"closed": sum(closure_ok.values()), "total": len(closure_ok),
                         "not_closed_cells": [list(k) for k, v in closure_ok.items() if not v],
                         "naive_control_fail": sum(naive_fail.values()),
                         "naive_control_total": len(naive_fail),
                         "naive_control_excluded_lambda1_cells": len(naive_excluded)},
        "m_spectrum_completion": m_spectrum,
        "out_of_scope_this_round": "W verification series (pentagon/T_F2/settled PROXY items) "
                                  "EXCLUDED per commander instruction -- separate delivery "
                                  "after definition-source procurement.",
        "grade": "candidate, single-system at slots 1-4 (system A has no slot1-4 "
                "formulation -- structural, not resolved by further engineering); "
                "PENDING third falsifier CV-9 pass before launch.",
    }
    today = date.today().isoformat().replace("-", "")
    out_path = ROOT / "search" / "certs" / f"d972_atype_v3_2_{today}.json"
    text = json.dumps(cert, sort_keys=True, indent=2, ensure_ascii=False, default=str) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(text, encoding="utf-8")
    readback = tmp.read_text(encoding="utf-8")
    core.require(readback == text, "checked-write readback mismatch")
    tmp.replace(out_path)
    return out_path, cert


def run_launch_campaign():
    """SCOPE (falsifier-recommended, enforced): gate4 closure calibration
    + m-spectrum sweep + cert issuance ONLY. No W verification series."""
    print("=" * 72)
    print("A-type v3.2 -- LAUNCH-SCOPE CAMPAIGN (gate4 + m-spectrum + cert only)")
    print("=" * 72)
    eng = Engine()
    self_test_predicate_agreement_slot0_only(eng)
    self_test_positive_control(eng)
    self_test_destructive_controls(eng)
    reg_results = self_test_regression_oracle(eng)
    closure_ok, naive_fail, naive_excluded = self_test_closure_calibration(eng)
    m_spectrum = m_spectrum_completion(eng)
    out_path, cert = write_cert(eng, reg_results, closure_ok, naive_fail, naive_excluded, m_spectrum)
    print()
    print("SUMMARY:")
    print(f"  regression oracle: {sum(1 for r in reg_results if r['pass'])}/{len(reg_results)} PASS (hard-asserted)")
    print(f"  gate4 closure: {sum(closure_ok.values())}/{len(closure_ok)}")
    print(f"  naive control fails: {sum(naive_fail.values())}/{len(naive_fail)} "
          f"(lambda=1 cells excluded: {len(naive_excluded)})")
    print(f"  m-spectrum: m9 all5={m_spectrum['m9']['all5']}  m8 all5={m_spectrum['m8']['all5']}  "
          f"m15={m_spectrum['m15']['status']}  m2={m_spectrum['m2']['status']}")
    print(f"  cert: {out_path.as_posix()}")
    return out_path, cert


if __name__ == "__main__":
    run_launch_campaign()
