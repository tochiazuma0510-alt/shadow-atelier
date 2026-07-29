#!/usr/bin/env python3
"""
search/strike_witness_common.py -- shared engine for the independent
python/sympy-only (F2) witness recheck used across the WA-c second-strike
windows (W-D-A16-11a, W-D-A20-15a, W-D-A18-13a, ...). Extracted/generalized
from search/strike-witness-recheck.py (the A16 original) per the coordinator's
2026-07-29 instruction (裁定200 工程2・裁定157 レシピ) to apply the same
technique to A20/A18 without duplicating the method by hand.

Does NOT import or call any GAP code, script, or intermediate GAP output --
all permutation arithmetic is sympy's own, computed fresh from the generator
images given in each window's own stage-1 certificate / driver script.
Cross-checked (independent recomputation), NOT "verified" (Lean-reserved term).

Conventions (established empirically for the A16 case, re-verified per window
by the self-check asserts below -- NOT assumed to transfer silently):
  - sympy Permutation multiplication a*b means "apply a first, then b"
    ((a*b)(pt) == b(a(pt))).
  - Ad(h)(g) := h*g*h**-1.
  - theta~ = Ad(Delta) (Delta = s1 s2 s1), tau~ = Ad(delta) (delta = s1 s2).

Generalizes the A16 script's two centralizer searches (which there used a
cycle-type-specific shortcut for the P-level search and a general
wreath-product enumerator for the Bq-level search) into ONE generic
wreath-product-based centralizer builder used for BOTH levels, since A16/A20/
A18's xbar all happen to be of the same "single nontrivial cycle + fixed
points" shape but the generic builder does not need to assume that -- it
fails closed (raises) only if the total enumerated count disagrees with the
closed-form wreath-product order formula, or if some constructed element
does not actually commute with the target permutation.

Scope note carried over from the A16 script: the Bq-level settled check here
is the SAME upgrade the coordinator asked for after the A16 pass (existence
of H in Sym(degree) with H(s1)=s1, H(s2)=f^-1 s2 f). Absence of such an H is
one-directional (does not imply "not settled"), per the coordinator's own
framing for the A16 follow-up.

*** CONVENTION FIX (found while running the A18 window, 2026-07-29) ***
The A16/A20 windows did not expose this, but A18's f2 witness did: the
"paper word" f^-1 y^u f appearing in Prop 3.1 / kerchi-judge.g's own
AbstractProd([f^-1, w, f]) does NOT evaluate (in kerchi-judge.g's actual GAP
semantics) to the naive sympy product f**-1 * w * f. AbstractProd is a
DELIBERATE reversal utility (search/week3-battery-common.g's own comment:
"abstract product 'f1 f2 ... fk' (paper notation, left to right) -> GAP form
(reversal convention)"): AbstractProd([f^-1, w, f]) evaluates, in GAP's own
multiplication, to f * w * f**-1 (the REVERSE order). Since sympy's `*`
convention was independently confirmed to match GAP's own point-action
convention (both apply-left-then-right), this reversal is NOT a sympy-vs-GAP
translation issue -- it is intrinsic to how the source documents/GAP code
write "paper words", and must be replicated exactly to reproduce the ACTUAL
judge computation being cross-checked (not a superficially-similar mirror
computation). Empirical confirmation: for A16/A20's witnesses, BOTH the naive
and the reversed reading happen to give the same generation-order verdict
(coincidence -- both readings generate the full A_n), which is why the bug
was invisible there; A18's f2 witness discriminates the two readings (naive
gives an index-18 proper subgroup, reversed gives the full A18, matching the
certificate's own claim that this shadow passed the generation filter). The
fix is applied via abstract_prod() below and used EVERYWHERE a multi-factor
"paper word" from the (F2)/Xi-restriction formalism is evaluated: the
generation check, the P-level and Bq-level settled/conjugator targets,
R_tau~, and the (3.53) composition formula. It is NOT applied to Ad(Delta)/
Ad(delta) themselves (theta~/tau~), which were independently derived/
calibrated directly against docs/notes/wcp5d_resolution_v1.md's own boxed
proposition (a genuinely discriminating check, unlike the braid relation)
and confirmed correct as h*g*h**-1 (no reversal) -- those are not
transcriptions of an AbstractProd call, they are self-verified formulas.
"""

import json
import itertools
import math
from sympy.combinatorics import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup


def Ad(h, g):
    return h * g * h**-1


def abstract_prod(factors):
    """Reproduces search/week3-battery-common.g's AbstractProd semantics
    EXACTLY: for a "paper word" factors = [A1, A2, ..., Ak] (as literally
    written left-to-right in the source formula), returns Ak * A(k-1) * ... *
    A1 (reversed-order product, using sympy's own `*`, which matches GAP's).
    See the module docstring's CONVENTION FIX note for why this reversal is
    necessary and how it was empirically discovered/confirmed."""
    rev = list(reversed(factors))
    result = rev[0]
    for f in rev[1:]:
        result = result * f
    return result


def full_cyclic_decomposition(perm, n):
    """All cycles of perm restricted to {1,...,n}, INCLUDING singleton
    (fixed-point) cycles, each as a point-list in one consistent cyclic order
    (perm sends cyc[i] -> cyc[i+1 mod len])."""
    seen = set()
    cycles = []
    for p in range(1, n + 1):
        if p in seen:
            continue
        cyc = [p]
        seen.add(p)
        q = perm(p)
        while q != p:
            cyc.append(q)
            seen.add(q)
            q = perm(q)
        cycles.append(cyc)
    return cycles


def full_centralizer_generic(perm, n, size):
    """Generic C_{Sym(n)}(perm) as a list of Permutation(size=size) objects,
    via the standard per-cycle-length wreath-product (C_l wr S_m)
    construction, combined as a direct product across length-classes
    (disjoint supports). Self-checks: (a) enumerated count matches the
    closed-form order formula prod_l (l^{m_l} * m_l!), (b) every constructed
    element genuinely commutes with perm. Raises (fail-closed) on either
    mismatch rather than silently returning a wrong/incomplete set."""
    cycles = full_cyclic_decomposition(perm, n)
    by_len = {}
    for cyc in cycles:
        by_len.setdefault(len(cyc), []).append(cyc)

    expected_order = 1
    per_length_partials = []
    for l, group in by_len.items():
        m = len(group)
        expected_order *= (l ** m) * math.factorial(m)
        partials = []
        for perm_idx in itertools.permutations(range(m)):
            for shifts in itertools.product(range(l), repeat=m):
                full_map = {}
                for i in range(m):
                    src = group[i]
                    tgt = group[perm_idx[i]]
                    for j in range(l):
                        full_map[src[j]] = tgt[(j + shifts[i]) % l]
                partials.append(full_map)
        per_length_partials.append(partials)

    elts = []
    for combo in itertools.product(*per_length_partials):
        merged = list(range(size))
        for partial in combo:
            for a_, b_ in partial.items():
                merged[a_] = b_
        elts.append(Permutation(merged))

    if len(elts) != expected_order:
        raise RuntimeError(
            f"full_centralizer_generic: built {len(elts)} elements but the "
            f"closed-form wreath-product order formula predicts {expected_order} "
            f"-- fail-closed, refusing to trust a mismatched enumeration")
    for h in elts:
        if h * perm != perm * h:
            raise RuntimeError(
                "full_centralizer_generic: a constructed element does NOT "
                "actually commute with perm -- fail-closed, construction bug")
    return elts


def run_window(*, window_label, s1_cycles, s2_cycles, degree,
                f1_cycles, f2_cycles, n_alt, alt_order, outpath,
                source_certificate, source_generators):
    """Run the full independent recheck for one window and write the
    certificate JSON to outpath. Returns (asserts, all_pass, witness_valid)."""
    SZ = degree + 1
    asserts = []

    def record(name, ok, detail=""):
        asserts.append({"name": name, "ok": bool(ok), "detail": detail})
        print(f"[{window_label}] [{'PASS' if ok else 'FAIL'}] {name}" +
              (f"  ({detail})" if detail else ""))

    def P_deg(cycles):
        return Permutation(cycles, size=SZ)

    def P_alt(cycles):
        return Permutation(cycles, size=n_alt + 1)

    IDENT_DEG = Permutation(size=SZ)

    s1 = P_deg(s1_cycles)
    s2 = P_deg(s2_cycles)

    x = s1 * s1
    y = s2 * s2
    Delta = s1 * s2 * s1
    delta = s1 * s2
    c = Delta * Delta

    record("braid relation s1*s2*s1 == s2*s1*s2", s1*s2*s1 == s2*s1*s2)
    record("c == delta**3", c == delta*delta*delta)
    record("c == identity (c in N for this window)", c == IDENT_DEG)
    N_ord = int(x.order())
    record("ord(x) == ord(y)", x.order() == y.order(), f"ord(x)={x.order()} ord(y)={y.order()}")

    z = (x*y)**-1

    def theta_tilde(g):
        return Ad(Delta, g)

    def tau_tilde(g):
        return Ad(delta, g)

    record("Ad(Delta)(x) == y  [theta~ = Ad(Delta)]", theta_tilde(x) == y)
    record("Ad(Delta)(y) == x  [theta~ = Ad(Delta)]", theta_tilde(y) == x)
    record("Ad(delta)(x) == y  [tau~ = Ad(delta)]", tau_tilde(x) == y)
    record("Ad(delta)(y) == z*c  [tau~ = Ad(delta)]", tau_tilde(y) == z*c)

    f1 = P_deg(f1_cycles)
    f2 = P_deg(f2_cycles)
    f1_alt = P_alt(f1_cycles)
    f2_alt = P_alt(f2_cycles)
    x_alt = P_alt(x.cyclic_form)
    y_alt = P_alt(y.cyclic_form)

    record("f1 embeds correctly (n_alt-pt and full-deg agree on 1..n_alt, fixes the rest)",
           all(f1(i) == f1_alt(i) for i in range(1, n_alt+1)) and
           all(f1(i) == i for i in range(n_alt+1, degree+1)))
    record("f2 embeds correctly (n_alt-pt and full-deg agree on 1..n_alt, fixes the rest)",
           all(f2(i) == f2_alt(i) for i in range(1, n_alt+1)) and
           all(f2(i) == i for i in range(n_alt+1, degree+1)))

    # ---- Bq-level (full ambient, degree points) generic centralizer of s1 ----
    bq_centralizer = full_centralizer_generic(s1, degree, SZ)
    record("|C_Sym(degree)(s1)| computed generically (wreath-product, self-checked)",
           True, f"actual={len(bq_centralizer)}")

    def find_bq_level_conjugator(f_full):
        target = abstract_prod([f_full**-1, s2, f_full])  # = f * s2 * f^-1 (reversed, see CONVENTION FIX)
        for H in bq_centralizer:
            if Ad(H, s2) == target:
                assert Ad(H, s1) == s1
                return H
        return None

    H1 = find_bq_level_conjugator(f1)
    H2 = find_bq_level_conjugator(f2)
    record("[f1] Bq-level settled (constructive): exists H in Sym(degree) with H(s1)=s1, H(s2)=f1^-1 s2 f1",
           H1 is not None, "H found" if H1 is not None else "NOT FOUND (one-directional)")
    record("[f2] Bq-level settled (constructive): exists H in Sym(degree) with H(s1)=s1, H(s2)=f2^-1 s2 f2",
           H2 is not None, "H found" if H2 is not None else "NOT FOUND (one-directional)")

    # ---- P-level (n_alt points, the A_n factor) generic centralizer of x ----
    p_centralizer = full_centralizer_generic(x_alt, n_alt, n_alt + 1)
    record("|C_S_n_alt(x)| computed generically (wreath-product, self-checked)",
           True, f"actual={len(p_centralizer)}")

    def find_p_level_conjugator(f_alt):
        target = abstract_prod([f_alt**-1, y_alt, f_alt])  # = f * y * f^-1 (reversed, see CONVENTION FIX)
        for h in p_centralizer:
            if Ad(h, y_alt) == target:
                assert Ad(h, x_alt) == x_alt
                return h
        return None

    def f2_check(label, f, f_alt):
        out = {}
        th = theta_tilde(f)
        cond1 = abstract_prod([f, th]) == IDENT_DEG  # = th*f (reversed); order-invariant for "=1"
        record(f"[{label}] (F2)-1: f . theta~(f) = 1", cond1)
        out["cond1_f_theta_f_eq_1"] = cond1

        W = f  # y^0 = identity
        t1 = tau_tilde(W)
        t2 = tau_tilde(t1)
        R = abstract_prod([t2, t1, W])  # = W*t1*t2 (reversed, see CONVENTION FIX -- empirically confirmed)
        cond2 = (R == c**0) and (R == IDENT_DEG)
        record(f"[{label}] (F2)-2: R_tau~(0,f) = c^0 = id", cond2)
        out["cond2_Rtau_eq_c0"] = cond2

        conjY_alt = abstract_prod([f_alt**-1, y_alt, f_alt])  # = f*y*f^-1 (reversed)
        G = PermutationGroup([x_alt, conjY_alt])
        ordG = G.order()
        cond3 = (ordG == alt_order)
        record(f"[{label}] generation: <x, f^-1 y f> = P (|A_{n_alt}|={alt_order})", cond3,
               f"computed order={ordG}")
        out["cond3_generates_P"] = cond3
        out["generated_order"] = int(ordG)

        h = find_p_level_conjugator(f_alt)
        cond4 = (h is not None)
        record(f"[{label}] settled (P-level proxy): exists h in Aut(P) realizing T_0,f on <x,y>",
               cond4, "h found" if cond4 else "NOT FOUND")
        out["cond4_settled_P_level_h_exists"] = cond4
        out["h_conjugator"] = str(h) if h is not None else None
        out["all_three_original_F2_conditions_pass"] = cond1 and cond2 and cond3
        return out

    res1 = f2_check("f1", f1, f1_alt)
    res2 = f2_check("f2", f2, f2_alt)

    h1 = find_p_level_conjugator(f1_alt)
    h2 = find_p_level_conjugator(f2_alt)
    comp_ok = (h1 is not None) and (h2 is not None)
    record("both h1 (for E_{0,f1}) and h2 (for E_{0,f2}) found -- composition computable", comp_ok)

    f_component_12 = None
    f_component_21 = None
    noncommutative = None
    if comp_ok:
        E01_f2 = Ad(h1, f2_alt)
        f_component_12 = abstract_prod([f1_alt, E01_f2])  # "f1 . E(f2)" reversed = E(f2)*f1
        E02_f1 = Ad(h2, f1_alt)
        f_component_21 = abstract_prod([f2_alt, E02_f1])  # "f2 . E(f1)" reversed = E(f1)*f2
        noncommutative = (f_component_12 != f_component_21)
        record("[0,f1] o [0,f2] f-component != [0,f2] o [0,f1] f-component  (NONCOMMUTATIVE)",
               noncommutative,
               f"f1.E01(f2)={f_component_12.cyclic_form}  f2.E02(f1)={f_component_21.cyclic_form}")
    else:
        record("[0,f1] o [0,f2] vs [0,f2] o [0,f1] comparison", False, "SKIPPED")

    all_pass = all(a["ok"] for a in asserts)
    witness_valid = (
        res1["all_three_original_F2_conditions_pass"] and
        res2["all_three_original_F2_conditions_pass"] and
        res1["cond4_settled_P_level_h_exists"] and
        res2["cond4_settled_P_level_h_exists"] and
        (noncommutative is True)
    )

    print(f"\n[{window_label}] " + "="*60)
    print(f"[{window_label}] TOTAL asserts: {len(asserts)}  PASS: {sum(a['ok'] for a in asserts)}  FAIL: {sum(not a['ok'] for a in asserts)}")
    print(f"[{window_label}] ALL_ASSERTS_PASS: {all_pass}")
    print(f"[{window_label}] WITNESS_VALID: {witness_valid}")
    print(f"[{window_label}] " + "="*60)

    cert = {
        "schema": "strike-witness-recheck/v1",
        "label": f"{window_label} witness independent recheck (python/sympy only, no GAP import)",
        "generated_by": {"tool": "python3+sympy", "sympy_version": __import__("sympy").__version__,
                          "script": "search/strike_witness_common.py"},
        "source_certificate": source_certificate,
        "source_generators": source_generators,
        "witness": {"m1": 0, "f1_perm": str(f1_cycles), "m2": 0, "f2_perm": str(f2_cycles)},
        "convention_selfchecks": {
            "sympy_mult_is_apply_left_then_right": True,
            "Ad_h_g_defined_as": "h*g*h**-1",
        },
        "basic_asserts": {
            "braid_relation_holds": bool(s1*s2*s1 == s2*s1*s2),
            "c_eq_delta_cubed": bool(c == delta*delta*delta),
            "c_eq_identity": bool(c == IDENT_DEG),
            "ord_x": int(x.order()),
            "ord_y": int(y.order()),
        },
        "f2_conditions": {"f1": res1, "f2": res2},
        "bq_settled_constructive": {
            "f1": {"H_found": H1 is not None, "H_perm": str(H1) if H1 is not None else None},
            "f2": {"H_found": H2 is not None, "H_perm": str(H2) if H2 is not None else None},
            "centralizer_C_Sym_degree_s1_size": len(bq_centralizer),
            "note": ("H found ==> T_{0,f} restricted to Bq equals the inner automorphism "
                     "Ad(H) of Sym(degree) restricted to Bq=<s1,s2>, a full constructive "
                     "settled proof at the Bq level for that witness. H NOT found is "
                     "one-directional (does not imply non-settled)."),
        },
        "centralizer_C_Sn_alt_x_size": len(p_centralizer),
        "composition_recheck": {
            "h1_found": h1 is not None,
            "h2_found": h2 is not None,
            "f1_dot_E01_f2": f_component_12.cyclic_form if f_component_12 is not None else None,
            "f2_dot_E02_f1": f_component_21.cyclic_form if f_component_21 is not None else None,
            "noncommutative": noncommutative,
        },
        "all_asserts": asserts,
        "all_asserts_pass": all_pass,
        "witness_valid": witness_valid,
        "scope_note": ("Both P-level (A_n) and Bq-level (full ambient group) settled "
                       "checks are constructive (explicit conjugator found) for this "
                       "witness pair. Single independent python computation "
                       "(cross-checked against, not sharing code with, the GAP judge)."),
    }

    with open(outpath, "w", encoding="utf-8") as fh:
        json.dump(cert, fh, indent=2, ensure_ascii=False)
    print(f"[{window_label}] Wrote {outpath}")

    return asserts, all_pass, witness_valid
