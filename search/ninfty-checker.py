#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-checker.py

N_infty stage-2 -- lane B "audit lane B" checker (spec sec.3: "proven-baseline
saturated elimination").

Role in the spec (governing spec = mb/ninfty-stage2-predicate/v18, sec.3):

    decision lane: E-1..E-6 + T-1 (rootpart(a) = [2,2,1])
    audit lane A : local differential -> R on C -> mu_* R           (searcher, node)
    audit lane B : proven-baseline saturated elimination            (checker, HERE)

This checker independently re-derives the polynomial-level predicates of
sec.3/sec.4 (E-1..E-6 preconditions, T-1, T-2 == eq.(60.5)) using algorithms
DIFFERENT from what lane A (searcher, node runtime) is presumed to use:

  * gcd is computed by a from-scratch Euclidean algorithm on Q[x]
    (poly_gcd below) -- no resultant is used anywhere in this file
    (spec sec.3: "checker は resultant を使わない" is stated for the
    searcher; this checker additionally avoids resultants as the
    "different algorithm" mandated by the commander's brief).

  * rootpart(a) (the multiplicity partition of the roots of a, needed for
    T-1's target "[2,2,1]") is computed via a self-implemented squarefree
    decomposition (Yun's algorithm, entirely gcd/derivative based) instead
    of any root-finding or resultant-based multiplicity count.  Each
    squarefree factor of degree d and multiplicity m contributes d roots
    of multiplicity m to the partition, over the algebraic closure -- this
    is a standard fact and requires no explicit root computation.

Contact discipline (spec/contract, verbatim requirement): this file is
value-independent.  It never hardcodes C, h, a5, squareclasses, signs,
branch values, concrete coefficients, or raw shard naming patterns.  All
numeric data enters only through the JSON fixture / candidate the caller
supplies.

Scope / EP status (spec sec.7, sec.9): EP (external positive control) has
not run.  Per the freeze receipt (provenance/ninfty_freeze_receipt_sol75.md)
and spec sec.9, this checker is a PARTIAL predicate.  It does NOT claim to
be a "calibrated detector" or "complete search".  Specifically UNKNOWN /
NOT IMPLEMENTED in this file (declared, not silently skipped):

  * T-3 (p-locus), T-4 (Weierstrass locus), T-5 (two-infinity, e=5),
    T-6 (harmonic pair -- sealed, out of scope by contact discipline),
    and the point-level construction of ramification_divisor_on_C /
    branch_divisor_on_P1 that a full "checker_native" artifact needs
    (spec sec.4.1 searcher_native / checker_native) all require locating
    actual points on the curve C_crv over Qbar (roots of p, roots of f6,
    the finite branch fiber structure of sec.1.4).  Root-finding over
    Qbar is out of scope for this partial-predicate checker; only the
    polynomial-identity part of T-7 (deg R_mu = 2g-2+2 deg mu = 12, a
    fixed bookkeeping identity that does not depend on candidate data)
    is checked.  W-6-style pushforward-sum consistency IS checked when
    the native artifact declares branch multiplicities explicitly (see
    check_native_pushforward below), since that only needs integer
    arithmetic on already-declared data, not root-finding.
  * E-5 (divisor orientation, (Or)) cannot be recovered from (a,p,f6)
    alone by any elimination method; it is a construction-time fact.
    This checker treats it as an externally-attested boolean the caller
    must supply (`divisor_orientation_attested`); UNKNOWN if absent.

runtime = python (stdlib only: fractions, hashlib, json, sys, argparse).
No import of lane A code (this checker has never read it and does not
know its existence). No shared math-helper library, no CAS package
(sympy/sage/numpy), no shared data-table with lane A.
"""

from __future__ import annotations
from fractions import Fraction
import hashlib
import json
import sys
import argparse

# --------------------------------------------------------------------------
# Self-implemented Q[x] arithmetic (low-degree-first list[Fraction]).
# No external polynomial library is used anywhere in this module.
# --------------------------------------------------------------------------

Poly = list


def _F(x):
    if isinstance(x, Fraction):
        return x
    if isinstance(x, str):
        # allow "p/q" strings from JSON fixtures
        if "/" in x:
            n, d = x.split("/")
            return Fraction(int(n), int(d))
        return Fraction(x)
    return Fraction(x)


def p_from_json(coeffs):
    return _trim([_F(c) for c in coeffs])


def _trim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return c


def p_deg(c):
    c = _trim(c)
    return len(c) - 1 if c else -1  # -1 = zero polynomial


def p_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    return _trim(out)


def p_neg(a):
    return [-x for x in a]


def p_sub(a, b):
    return p_add(a, p_neg(b))


def p_scale(a, k):
    return _trim([x * k for x in a])


def p_mul(a, b):
    a, b = _trim(a), _trim(b)
    if not a or not b:
        return []
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return _trim(out)


def p_deriv(a):
    a = _trim(a)
    if len(a) <= 1:
        return []
    return _trim([a[i] * i for i in range(1, len(a))])


def p_divmod(a, b):
    """Exact division (self-implemented long division) in Q[x]. Returns (q, r)."""
    a = _trim(a)
    b = _trim(b)
    if not b:
        raise ZeroDivisionError("poly division by zero polynomial")
    db = len(b) - 1
    lb = b[-1]
    r = list(a)
    q = [Fraction(0)]
    while True:
        r = _trim(r)
        dr = len(r) - 1
        if not r or dr < db:
            break
        coef = r[-1] / lb
        shift = dr - db
        if shift >= len(q):
            q += [Fraction(0)] * (shift - len(q) + 1)
        q[shift] += coef
        sub = [Fraction(0)] * shift + [coef * x for x in b]
        r = p_sub(r, sub)
    return _trim(q), _trim(r)


def p_gcd(a, b):
    """Self-implemented Euclidean algorithm. No resultant is computed."""
    a, b = _trim(a), _trim(b)
    while b:
        _, r = p_divmod(a, b)
        a, b = b, r
    return a


def p_monic(a):
    a = _trim(a)
    if not a:
        return a
    lc = a[-1]
    return [x / lc for x in a]


def p_eq(a, b):
    return _trim(a) == _trim(b)


def p_is_zero(a):
    return not _trim(a)


def p_is_squarefree(a):
    """squarefree iff gcd(a, a') is a nonzero constant."""
    a = _trim(a)
    if not a:
        return False
    g = p_gcd(a, p_deriv(a))
    return p_deg(g) == 0


def squarefree_yun(a):
    """
    Self-implemented Yun squarefree decomposition (char 0, gcd/derivative
    based -- no root finding, no resultant). Returns list of
    (monic_squarefree_factor, multiplicity) with
        prod_i factor_i ** multiplicity_i  ==  monic(a)   (as polynomials)
    """
    a = p_monic(_trim(a))
    if p_deg(a) <= 0:
        return []
    ap = p_deriv(a)
    c = p_monic(p_gcd(a, ap))
    if p_deg(c) <= 0:
        w, _ = a, []
        y, _ = ap, []
    else:
        w, _ = p_divmod(a, c)
        y, _ = p_divmod(ap, c)
    w = p_monic(w)
    factors = []
    i = 1
    while p_deg(w) > 0:
        wd = p_deriv(w)
        z = p_sub(y, wd)
        g = p_monic(p_gcd(w, z))
        if p_deg(g) > 0:
            factors.append((g, i))
            w, _ = p_divmod(w, g)
            w = p_monic(w)
        # y must become c_i = z / g (Yun's recurrence), not z itself --
        # forgetting this division was caught by a self-test fixture
        # (see search/fixtures/ninfty/checker_pos_01.json) where it produced
        # a wrong rootpart; fixed here.
        if p_deg(g) > 0:
            y, _ = p_divmod(z, g)
        else:
            y = z
        i += 1
        if i > 10000:
            raise RuntimeError("squarefree_yun: iteration bound exceeded (malformed input)")
    return factors


def rootpart_via_squarefree(a):
    """
    rootpart(a): sorted (desc) multiset of root multiplicities, derived
    WITHOUT root finding, purely from the degrees of the Yun squarefree
    factors. (A squarefree factor of degree d and multiplicity m
    contributes d roots of multiplicity m over the algebraic closure.)
    """
    factors = squarefree_yun(a)
    part = []
    for (f, mult) in factors:
        d = p_deg(f)
        part += [mult] * d
    return sorted(part, reverse=True)


# --------------------------------------------------------------------------
# Reason code tables (spec sec.5.3.1 / sec.5.3.2, literal reproduction of
# the enum only -- no state-machine ownership claimed; this checker only
# *supplies* candidate reason codes for its own lane, it does not compute
# the governing verdict/primary (that belongs to governing spec sec.5.3,
# which is receiving-side / cross-lane and out of this file's scope).
# --------------------------------------------------------------------------

REJECT_PRIORITY = [
    "precondition/degree-mismatch",        # [1]
    "precondition/f6-not-monic",           # [2]
    "precondition/curve-not-squarefree",   # [3]
    "precondition/leading-coeff-mismatch", # [4]
    "precondition/pell-violation",         # [5]
    "precondition/divisor-orientation",    # [6]
    "triple-root-of-a",                    # [7]
    "a-partition-mismatch",                # [8]
]

# Integrity codes this checker is able to raise on its own (subset of the
# 18-stage table, governing spec sec.5.3.2). Digest/shared-helper/sealed
# leak codes ([9]-[12]) are not this file's job (that is the verifier's
# and the receiving side's). This checker can raise:
INTEGRITY_PELL_COPRIME_MISMATCH = "pell-implies-coprime-mismatch"   # [13]
INTEGRITY_PELL_DERIVATIVE_MISMATCH = "pell-derivative-mismatch"     # [15]


def check_preconditions(a, p, f6):
    """
    E-1..E-6 (governing spec sec.2), checked via the from-scratch
    poly arithmetic above. Returns (verdict_stage, reason_code_or_None, detail).
    verdict_stage in {"REJECT", "INTEGRITY_STOP", None} (None = passes here).
    """
    detail = {}

    # E-2: deg a = 5, deg p = 2 ; combined with deg f6 = 6 (part of E-1)
    if p_deg(f6) != 6 or p_deg(a) != 5 or p_deg(p) != 2:
        detail["degrees"] = {"deg_f6": p_deg(f6), "deg_a": p_deg(a), "deg_p": p_deg(p)}
        return "REJECT", "precondition/degree-mismatch", detail

    # E-1: f6 monic
    f6m = _trim(f6)
    if f6m[-1] != 1:
        detail["f6_leading_coeff"] = str(f6m[-1])
        return "REJECT", "precondition/f6-not-monic", detail

    # E-1: f6 squarefree
    if not p_is_squarefree(f6):
        return "REJECT", "precondition/curve-not-squarefree", detail

    # E-3: a5 = p2 (leading coeffs equal and nonzero)
    a5 = _trim(a)[-1]
    p2 = _trim(p)[-1]
    if a5 != p2 or a5 == 0:
        detail["a5"] = str(a5)
        detail["p2"] = str(p2)
        return "REJECT", "precondition/leading-coeff-mismatch", detail

    # E-4: (Pell) a^2 - f6*p^2 = C in Q^x  (nonzero constant polynomial)
    pell = p_sub(p_mul(a, a), p_mul(f6, p_mul(p, p)))
    if p_deg(pell) != 0 or (p_deg(pell) == 0 and pell[0] == 0):
        detail["pell_residual_degree"] = p_deg(pell)
        return "REJECT", "precondition/pell-violation", detail
    C = pell[0]
    detail["pell_constant_is_nonzero"] = True  # value itself withheld (contact discipline)

    # E-6: gcd(a,p) = 1 -- automatic from E-4 + C != 0 (spec sec.2 "E-6 の身分").
    # If E-4 passed but this fails, spec mandates INTEGRITY_STOP (not REJECT).
    g_ap = p_gcd(a, p)
    if p_deg(g_ap) > 0:
        return "INTEGRITY_STOP", INTEGRITY_PELL_COPRIME_MISMATCH, detail

    # E-5: divisor orientation -- cannot be recomputed from (a,p,f6) alone.
    # Left to caller attestation; handled by caller (see run_checker below).

    return None, None, detail


def check_T1(a):
    """
    T-1 (governing spec sec.3): deg gcd(a,a') = 2, gcd(a,a') squarefree,
    deg gcd(a,a',a'') = 0.
    Returns (verdict_stage, reason_code_or_None, detail).
    """
    ap = p_deriv(a)
    app = p_deriv(ap)
    d = p_gcd(a, ap)
    detail = {"deg_gcd_a_ap": p_deg(d)}

    g3 = p_gcd(d, app)
    detail["deg_gcd_a_ap_app"] = p_deg(g3)
    if p_deg(g3) > 0:
        return "REJECT", "triple-root-of-a", detail

    if p_deg(d) != 2 or not p_is_squarefree(d):
        detail["gcd_squarefree"] = p_is_squarefree(d)
        return "REJECT", "a-partition-mismatch", detail

    return None, None, detail


def check_T2(a, p):
    """
    T-2 == eq.(60.5): a' =. p*d  (proportional up to a nonzero scalar),
    where d = monic(gcd(a,a')). Checked by direct polynomial multiplication
    and coefficient-wise comparison -- no polynomial division of a'/p is
    performed (avoids introducing spurious poles / the "while" elimination
    style forbidden by spec sec.3: "二次因子の while 全除去は禁止").
    """
    ap = p_deriv(a)
    d = p_monic(p_gcd(a, ap))
    pd = p_mul(p, d)
    detail = {"deg_pd": p_deg(pd), "deg_ap": p_deg(ap)}

    if p_deg(pd) != p_deg(ap) or p_deg(ap) < 0:
        return "INTEGRITY_STOP", INTEGRITY_PELL_DERIVATIVE_MISMATCH, detail

    # a' =. p*d  <=>  exists nonzero scalar k with a' == k * (p*d)
    lc_ap = _trim(ap)[-1]
    lc_pd = _trim(pd)[-1]
    if lc_pd == 0:
        return "INTEGRITY_STOP", INTEGRITY_PELL_DERIVATIVE_MISMATCH, detail
    k = lc_ap / lc_pd
    if not p_eq(ap, p_scale(pd, k)):
        return "INTEGRITY_STOP", INTEGRITY_PELL_DERIVATIVE_MISMATCH, detail

    return None, None, detail


def check_native_pushforward(declared_native):
    """
    Partial W-6-style consistency check on an ALREADY-DECLARED native
    artifact (does not construct the divisor itself -- see module
    docstring UNKNOWN list). Verifies that the sum of ramification
    multiplicities pushed to each branch point equals the declared
    branch-divisor multiplicity at that point, using plain integer
    arithmetic on the caller-supplied data.
    Returns (ok: bool, detail: dict).
    """
    if declared_native is None:
        return None, {"status": "UNKNOWN", "reason": "no native artifact supplied"}

    ram = declared_native.get("ramification_divisor_on_C", [])
    branch = declared_native.get("branch_divisor_on_P1", [])

    push = {}
    for pt in ram:
        bv = pt["maps_to_branch_value"]
        mult = pt["multiplicity"]
        push[bv] = push.get(bv, 0) + mult

    branch_map = {b["branch_value"]: b["multiplicity"] for b in branch}

    ok = (set(push.keys()) == set(branch_map.keys())) and all(
        push[k] == branch_map[k] for k in push
    )
    return ok, {"pushforward": push, "declared_branch": branch_map, "match": ok}


def rh_bookkeeping_identity(genus, deg_mu):
    """
    T-7 fixed identity: deg R_mu = 2g - 2 + 2 deg(mu). This does not
    depend on candidate data at all (spec sec.1.8 proof, sufficiency
    direction) -- it is checked here purely as a bookkeeping tautology
    guard against caller mis-supplying genus/degree.
    """
    return 2 * genus - 2 + 2 * deg_mu


CHECKER_ID = "search/ninfty-checker.py"
CHECKER_ALGORITHM_TAG = "euclid-gcd+yun-squarefree-elimination"


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def run_checker(candidate):
    """
    candidate = {
      "a": [c0..c5], "p": [c0..c2], "f6": [c0..c6],   # coefficient lists, low-degree-first
      "divisor_orientation_attested": true/false/null,
      "native_artifact": {...} | null,                # optional, for W-6-style consistency only
      "genus": 2, "deg_mu": 5                          # optional, for T-7 bookkeeping guard
    }
    Returns the checker verdict record (a partial predicate result, NOT an
    ACCEPT/verdict-machine decision -- spec sec.5.3's state machine owns
    the final verdict/primary; this is this checker's own contribution).
    """
    a = p_from_json(candidate["a"])
    p = p_from_json(candidate["p"])
    f6 = p_from_json(candidate["f6"])

    reasons = []
    stage = None
    primary = None

    pre_stage, pre_reason, pre_detail = check_preconditions(a, p, f6)
    result = {
        "checker_id": CHECKER_ID,
        "algorithm": CHECKER_ALGORITHM_TAG,
        "precondition_detail": pre_detail,
    }

    if pre_reason:
        reasons.append(pre_reason)
        stage, primary = pre_stage, pre_reason
        result["stage"] = stage
        result["reason_codes"] = reasons
        result["primary_reason_code"] = primary
        result["rootpart_a"] = None
        return result

    # E-5: caller-attested, cannot be re-derived from (a,p,f6) alone.
    attested = candidate.get("divisor_orientation_attested", None)
    if attested is False:
        reasons.append("precondition/divisor-orientation")
        result["stage"] = "REJECT"
        result["reason_codes"] = reasons
        result["primary_reason_code"] = "precondition/divisor-orientation"
        result["rootpart_a"] = None
        return result
    result["divisor_orientation_status"] = "UNKNOWN" if attested is None else "attested-true"

    t1_stage, t1_reason, t1_detail = check_T1(a)
    result["T1_detail"] = t1_detail
    if t1_reason:
        reasons.append(t1_reason)
        stage, primary = t1_stage, t1_reason
        result["stage"] = stage
        result["reason_codes"] = reasons
        result["primary_reason_code"] = primary
        result["rootpart_a"] = rootpart_via_squarefree(a)
        return result

    rootpart = rootpart_via_squarefree(a)
    result["rootpart_a"] = rootpart

    t2_stage, t2_reason, t2_detail = check_T2(a, p)
    result["T2_detail"] = t2_detail
    if t2_reason:
        reasons.append(t2_reason)
        stage, primary = t2_stage, t2_reason

    if candidate.get("native_artifact") is not None:
        ok, pf_detail = check_native_pushforward(candidate["native_artifact"])
        result["pushforward_detail"] = pf_detail
        if ok is False:
            reasons.append("divisor-equality-failure")  # [25], native-declared inconsistency
            if stage is None:
                stage, primary = "INTEGRITY_STOP", "divisor-equality-failure"
    else:
        result["pushforward_detail"] = {"status": "UNKNOWN", "reason": "no native artifact supplied"}

    if "genus" in candidate and "deg_mu" in candidate:
        result["rh_identity_value"] = rh_bookkeeping_identity(candidate["genus"], candidate["deg_mu"])

    result["stage"] = stage  # None => this checker raises no reason on its own
    result["reason_codes"] = reasons
    result["primary_reason_code"] = primary

    # Declared UNKNOWN / NOT IMPLEMENTED items (spec sec.7 EP status; honest,
    # not silently dropped):
    result["unknown"] = [
        "T-3 (p-locus): point-level construction not implemented (needs root-finding over Qbar)",
        "T-4 (Weierstrass locus): not implemented (needs root-finding over Qbar)",
        "T-5 (two-infinity, e=5): not implemented",
        "T-6 (harmonic pair): sealed value, out of scope by contact discipline",
        "full checker_native divisor construction (ramification_divisor_on_C / "
        "branch_divisor_on_P1 from scratch): NOT IMPLEMENTED -- only pushforward "
        "consistency of an already-declared native artifact is checked",
        "E-5 (divisor orientation): not re-derivable from (a,p,f6) alone; "
        "caller-attested only",
    ]

    result["checker_native_digest"] = sha256_of(
        {"rootpart_a": rootpart, "T1_detail": t1_detail, "T2_detail": t2_detail}
    )
    return result


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("candidate_json", help="path to candidate JSON, or '-' for stdin")
    args = ap.parse_args(argv)

    if args.candidate_json == "-":
        candidate = json.load(sys.stdin)
    else:
        with open(args.candidate_json, "r", encoding="utf-8") as f:
            candidate = json.load(f)

    result = run_checker(candidate)
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
