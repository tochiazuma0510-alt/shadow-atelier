"""audit_P0_naive_judge_v4.py

DIFF FROM v3 (one line, per commander instruction): aij_automorphism_images()
now reverses braid_word internally before composing table entries, fixing
the Ad(u)-composition-order bug diagnosed live (ruling 1464) -- v3 built
Ad(u) for a LEFT-TO-RIGHT group-multiplication word u=[l1,l2,...] as
step_{l_last} o ... o step_{l1} (last letter outermost), but Ad(u1.u2)(x)
= u1.u2.x.u2^-1.u1^-1 = Ad(u1)(Ad(u2)(x)) requires u2's step to be
INNERMOST and u1's OUTERMOST -- i.e. for word=[l1,l2], the correct
automorphism is step_{l1} o step_{l2} (FIRST letter outermost), the
opposite of what v3 computed; v3 called this with the word already
un-reversed at each of its 5 call sites (ad-hoc reversed by hand during
live debugging, never fixed in the function itself or persisted to disk
-- this is exactly the CV-9 gap this file closes).

Self-tests (embedded, run automatically before anything else; abort via
core.require on any failure so a future accidental regression cannot
silently produce results again):
  (1) calibration: pure_relations(4) trivial via this file's own
      aij_to_sigma + artin_images (unchanged from v3, re-affirmed).
  (2) round-trip: Ad(sigma_k) then Ad(sigma_-k) == identity, compared as
      e4 GROUP ELEMENTS (not raw words -- v2's original round-trip bug).
  (3) D-1 canary (braid theorem, mathematician-verified in B3, lifts to
      B4 strand-triple (2,3,4)): Ad(delta)(x) == y EXACTLY, x=local
      sigma1^2=A23=gen4, delta=local sigma1.sigma2=[2,3] (B4's
      sigma2.sigma3), y=A34=gen6 (coface_slot[2]). Must be True with the
      fixed composition order (was False in v3).
  (4) cube-form canary: (H-b) at m=0 lands on c^17 (equivalently c^-1,
      since kappa_full(e4)=18 and delta^3=c^1 exactly / s=1) -- the
      raw value already confirmed under both the buggy and fixed
      composition order this session (m=0 degenerates to g=f, insensitive
      to the bug), kept here as a stable regression anchor.

This file is the ANCHOR for the four-way P0/P1/P2/P3 crosscheck per
falsifier's finding that v3 (broken composition order) makes any
P3-vs-P0 judgment meaningless.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_1 as core  # noqa: E402  (generic group engine only)


def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def inv_word(word):
    return reduce_word([-x for x in reversed(word)])


def artin_step(rank, letter):
    i = abs(letter)
    images = [[j] for j in range(1, rank + 1)]
    if letter > 0:
        images[i - 1] = [i, i + 1, -i]
        images[i] = [i]
    else:
        images[i - 1] = [i + 1]
        images[i] = [-(i + 1), i, i + 1]
    return images


def word_substitute_letters(word, images):
    out = []
    for letter in word:
        i = abs(letter)
        img = images[i - 1]
        out.extend(img if letter > 0 else inv_word(img))
        out = reduce_word(out)
    return out


def artin_images(rank, braid_word):
    images = [[j] for j in range(1, rank + 1)]
    for letter in braid_word:
        step = artin_step(rank, letter)
        images = [word_substitute_letters(w, step) for w in images]
    return images


IDENTITY_IMAGES_4 = [[i] for i in range(1, 5)]


def aij_to_sigma(word_in_aij_letters, artin_words):
    out = []
    for L in word_in_aij_letters:
        i = abs(L)
        aw = artin_words[i - 1]
        out.extend(aw if L > 0 else inv_word(aw))
    return out


def push_through_coface_letters(word, coface_slot):
    images = [coface_slot[0], coface_slot[2]]
    out = []
    for letter in word:
        img = images[abs(letter) - 1]
        out.extend(img if letter > 0 else inv_word(img))
        out = reduce_word(out)
    return out


FIXED_WORD = [-2, -2, -1, -1, 2, 2, 1, -2, -1, -1,
              2, 2, 2, -1, -2, -2, 1, 1, 1, 1]
PAIRS = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


def load_q3():
    Q3_PATH = ROOT / "ci/b345_157en_artifacts_32458556448/d972_b345_q3_chief_v1.json"
    return json.loads(Q3_PATH.read_text(encoding="utf-8"))


def derive_aij_conjugation_table(artin_words):
    def meridian_action(aij_word):
        return artin_images(4, aij_to_sigma(aij_word, artin_words))

    single_actions = {}
    for idx in range(1, 7):
        single_actions[idx] = meridian_action([idx])
        single_actions[-idx] = meridian_action([-idx])
    letters = list(range(1, 7)) + list(range(-1, -7, -1))

    def find_word_for_action(target):
        for g, act in single_actions.items():
            if act == target:
                return [g]
        for g in letters:
            for h in letters:
                if meridian_action([g, h]) == target:
                    return [g, h]
        for g in letters:
            for h in letters:
                if meridian_action([g, h, -g]) == target:
                    return [g, h, -g]
        return None

    table = {}
    for k in (1, 2, 3, -1, -2, -3):
        row = []
        for idx in range(1, 7):
            aw = artin_words[idx - 1]
            conj_sigma_word = [k] + aw + [-k]
            target = artin_images(4, conj_sigma_word)
            w = find_word_for_action(target)
            core.require(w is not None, f"no match found for Ad(sigma{k})(A_{PAIRS[idx-1]})")
            row.append(w)
        table[k] = row
    return table


def aij_automorphism_images(braid_word, table):
    """images of the 6 A_ij generators under Ad(u), where u is the GROUP
    ELEMENT represented by braid_word read LEFT TO RIGHT as an ordinary
    product u = sigma_{l1}.sigma_{l2}. ... .sigma_{ln}.

    FIX (v4, vs v3): Ad(u1.u2)(x) = u1.u2.x.u2^-1.u1^-1 = Ad(u1)(Ad(u2)(x))
    -- the LAST-applied conjugation must be the FIRST letter's Ad (u1
    outermost), so this function processes braid_word in REVERSE (the
    LAST letter's Ad is applied first/innermost, matching u2 above being
    innermost). v3 processed left-to-right directly, which builds
    Ad(u_last)( ... Ad(u_first)(x) ...) instead -- the automorphism for
    the REVERSED word, silently swapped for words of length>=2 whenever
    the generators involved don't commute (diagnosed live via D-1:
    Ad(delta)(A23) gave A24 instead of the braid-theorem-correct A34
    until this reversal was applied)."""
    images = [[i] for i in range(1, 7)]
    for letter in reversed(braid_word):
        step = table[letter]
        images = [word_substitute_letters(w, step) for w in images]
    return images


def apply_automorphism(word, images):
    return word_substitute_letters(word, images)


# =====================================================================
# embedded self-tests -- run BEFORE any substantive computation; abort
# (core.require) on any failure so a future regression cannot silently
# reproduce results again without being caught.
# =====================================================================
def run_self_tests(q3, artin_words, coface_slot, table, e4):
    # (1) calibration
    rels = core.pure_relations(4)
    bad = [idx for idx, r in enumerate(rels)
           if artin_images(4, aij_to_sigma(r, artin_words)) != IDENTITY_IMAGES_4]
    core.require(len(bad) == 0, f"SELF-TEST FAIL (calibration): pure_relations(4) "
                                f"not trivial via this file's own machinery, bad={bad}")

    # (2) round-trip, e4-level (group elements, not raw words)
    def rt_ok(k):
        combo = aij_automorphism_images([k, -k], table)
        return all(e4.eval(combo[i]) == e4.eval([i + 1]) for i in range(6))
    for k in (1, 2, 3):
        core.require(rt_ok(k), f"SELF-TEST FAIL (round-trip): Ad(sigma{k}) then "
                               f"Ad(sigma{-k}) != identity in e4")

    # (3) D-1 canary: Ad(delta)(x) == y EXACTLY (braid theorem, fixed
    # composition order required to pass -- was False under v3's bug)
    DELTA_WORD = [2, 3]  # delta = sigma2.sigma3 (local triple (2,3,4))
    x_word, y_word = [4], [6]  # x=A23=local sigma1^2, y=A34=coface_slot[2]
    delta_images = aij_automorphism_images(DELTA_WORD, table)
    ad_delta_x = apply_automorphism(x_word, delta_images)
    core.require(e4.eval(ad_delta_x) == e4.eval(y_word),
                f"SELF-TEST FAIL (D-1 canary): Ad(delta)(x)={ad_delta_x} != y "
                f"-- composition-order bug has REGRESSED")

    # (4) cube-form canary: (H-b) at m=0 lands on c^17 (== c^-1, kappa_full=18)
    c_val = e4.eval([4, 5, 6])

    def e4_power(base_val, k):
        if k >= 0:
            cur = e4.identity
            for _ in range(k):
                cur = e4.mul(cur, base_val)
            return cur
        inv_base = e4.inverse(base_val)
        cur = e4.identity
        for _ in range(-k):
            cur = e4.mul(cur, inv_base)
        return cur

    delta_cubed_inv = e4.inverse(c_val)  # delta^3 = c^1 (s=1, confirmed exactly)
    delta2_images = aij_automorphism_images(DELTA_WORD * 2, table)
    f_pb4 = push_through_coface_letters(FIXED_WORD, coface_slot)  # g(m=0) = f
    ad_delta_f = apply_automorphism(f_pb4, delta_images)
    ad_delta2_f = apply_automorphism(f_pb4, delta2_images)
    val_b_m0 = e4.mul(delta_cubed_inv,
                     e4.mul(e4.eval(ad_delta2_f), e4.mul(e4.eval(ad_delta_f), e4.eval(f_pb4))))
    core.require(val_b_m0 == e4_power(c_val, 17),
                f"SELF-TEST FAIL (cube-form m=0 canary): expected landing on c^17, got a "
                f"different value -- regression in either the composition fix or the "
                f"rearrangement algebra")

    print("[self-test] ALL PASS: calibration / round-trip(e4) / D-1(Ad(delta)(x)==y) / "
          "cube-form(m=0 lands c^17)")


def main():
    q3 = load_q3()
    artin_words = q3["formulas"]["presentations"]["PB4"]["artin_words"]
    coface_slot = q3["formulas"]["cofaces_3_4"][0]
    table = derive_aij_conjugation_table(artin_words)
    e4 = core.E4(q3)

    run_self_tests(q3, artin_words, coface_slot, table, e4)

    def order_of(val):
        cur = val
        for kk in range(1, 200):
            if cur == e4.identity:
                return kk
            cur = e4.mul(cur, val)
        return None

    def e4_power(base_val, k):
        if k >= 0:
            cur = e4.identity
            for _ in range(k):
                cur = e4.mul(cur, base_val)
            return cur
        inv_base = e4.inverse(base_val)
        cur = e4.identity
        for _ in range(-k):
            cur = e4.mul(cur, inv_base)
        return cur

    def find_power_e4(target_val, base_val, kmax=40):
        for kk in range(0, kmax + 1):
            if e4_power(base_val, kk) == target_val:
                return kk
        for kk in range(1, kmax + 1):
            if e4_power(base_val, -kk) == target_val:
                return -kk
        return None

    print()
    print("=" * 70)
    print("ITEM 0: kappa, s, s_bar, t IN e4 (Pi4[3] and full)")
    print("=" * 70)
    c_aij_word = [4, 5, 6]
    c_val = e4.eval(c_aij_word)
    kappa_full = order_of(c_val)
    kappa_pc = order_of((core.perm_one(e4.degree), c_val[1]))
    print(f"c = A23.A24.A34 :  kappa_full(e4) = {kappa_full}   "
          f"kappa_pc(Pi4[3]) = {kappa_pc}")

    DELTA_WORD = [2, 3]
    DELTA_BAR_WORD = [3, 2]
    HALFTWIST_WORD = [2, 3, 2]

    def identify_pure_braid_as_aij_word(sigma_word, max_len=3):
        target = artin_images(4, sigma_word)
        if target == IDENTITY_IMAGES_4:
            return []
        letters6 = list(range(1, 7)) + list(range(-1, -7, -1))

        def maction(w):
            return artin_images(4, aij_to_sigma(w, artin_words))
        for a in letters6:
            if maction([a]) == target:
                return [a]
        for a in letters6:
            for b in letters6:
                if maction([a, b]) == target:
                    return [a, b]
        for a in letters6:
            for b in letters6:
                for cc in letters6:
                    if maction([a, b, cc]) == target:
                        return [a, b, cc]
        return None

    for label, w in (("delta^3", DELTA_WORD * 3), ("delta_bar^3", DELTA_BAR_WORD * 3),
                    ("Delta_local^2", HALFTWIST_WORD * 2)):
        aij_w = identify_pure_braid_as_aij_word(w)
        val = e4.eval(aij_w) if aij_w is not None else None
        k = find_power_e4(val, c_val) if val is not None else None
        k_mod = (k % kappa_full) if k is not None else None
        print(f"  {label}: A_ij-word={aij_w}  e4-value == c^k for k={k}  "
              f"(k mod kappa_full={kappa_full} -> {k_mod})")

    print()
    print("=" * 70)
    print("P0 JUDGE: (H-a) via e4; (3.3)/(3.4) DIRECT form (ruling: primary "
          "predicate, cube form demoted to secondary instrument per T-0); "
          "(H-b) cube form kept as secondary instrument, m=0..8")
    print("=" * 70)

    f_pb4 = push_through_coface_letters(FIXED_WORD, coface_slot)
    delta_half_images = aij_automorphism_images(HALFTWIST_WORD, table)
    ad_delta_f = apply_automorphism(f_pb4, delta_half_images)
    ha_val = e4.eval(f_pb4 + ad_delta_f)
    print(f"(H-a) f.Ad(Delta)(f) == identity in e4?  {ha_val == e4.identity}")

    delta_images = aij_automorphism_images(DELTA_WORD, table)
    delta2_images = aij_automorphism_images(DELTA_WORD * 2, table)
    delta_bar_inv_images = aij_automorphism_images(inv_word(DELTA_BAR_WORD), table)
    delta_bar_inv2_images = aij_automorphism_images(inv_word(DELTA_BAR_WORD) * 2, table)

    c_val_cubed_delta = e4.eval(identify_pure_braid_as_aij_word(DELTA_WORD * 3))
    c_val_cubed_deltabar = e4.eval(identify_pure_braid_as_aij_word(DELTA_BAR_WORD * 3))
    delta_cubed_inv = e4.inverse(c_val_cubed_delta)
    deltabar_cubed = c_val_cubed_deltabar

    Y = [2]
    results_34, results_hb, results_hbp = [], [], []
    for m in range(0, 9):
        g_abstract = reduce_word(Y * m + FIXED_WORD)
        g_pb4 = push_through_coface_letters(g_abstract, coface_slot)
        g_val = e4.eval(g_pb4)

        # (3.4) DIRECT form: tau^2(g).tau(g).g == 1, with tau realized as
        # Ad(delta) (fixed composition order) -- PRIMARY predicate per ruling
        tau_g = apply_automorphism(g_pb4, delta_images)
        tau2_g = apply_automorphism(g_pb4, delta2_images)
        val_34 = e4.eval(tau2_g + tau_g + g_pb4)
        results_34.append((m, val_34 == e4.identity))

        # (H-b) cube form -- SECONDARY instrument
        ad_delta_g = apply_automorphism(g_pb4, delta_images)
        ad_delta2_g = apply_automorphism(g_pb4, delta2_images)
        val_b = e4.mul(delta_cubed_inv,
                       e4.mul(e4.eval(ad_delta2_g), e4.mul(e4.eval(ad_delta_g), g_val)))
        k_b = find_power_e4(val_b, c_val)
        results_hb.append((m, k_b, val_b == e4.identity))

        # (H-b') cube form -- SECONDARY instrument
        ad_dbi_g = apply_automorphism(g_pb4, delta_bar_inv_images)
        ad_dbi2_g = apply_automorphism(g_pb4, delta_bar_inv2_images)
        val_bp = e4.mul(deltabar_cubed,
                        e4.mul(e4.eval(ad_dbi2_g), e4.mul(e4.eval(ad_dbi_g), g_val)))
        k_bp = find_power_e4(val_bp, c_val)
        results_hbp.append((m, k_bp, val_bp == e4.identity))

        print(f"  m={m}: (3.4)-direct id={val_34 == e4.identity}   "
              f"(H-b) k={k_b} (id={val_b == e4.identity})   "
              f"(H-b') k={k_bp} (id={val_bp == e4.identity})")

    print()
    print("RAW (3.4)-direct (m,is_identity):", results_34)
    print("RAW (H-b)  (m,k,is_identity):", results_hb)
    print("RAW (H-b') (m,k,is_identity):", results_hbp)


if __name__ == "__main__":
    main()
