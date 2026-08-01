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
    T-6 (harmonic pair -- sealed, out of scope by contact discipline)
    remain NOT IMPLEMENTED in this file.  Only the polynomial-identity
    part of T-7 (deg R_mu = 2g-2+2 deg mu = 12, a fixed bookkeeping
    identity that does not depend on candidate data) is checked here.
    W-6-style pushforward-sum consistency IS checked when a native
    artifact declares branch multiplicities explicitly (see
    check_native_pushforward below), since that only needs integer
    arithmetic on already-declared data, not root-finding.
  * [実装済み(20260801)] the point-level construction of
    ramification_divisor_on_C / branch_divisor_on_P1 (spec sec.4.1
    searcher_native / checker_native) -- the finite branch fiber points
    (spec sec.1.4/1.5, roots of gcd(a,a')) and the two infinity points
    (spec (Or), via a local Puiseux-order computation) -- WAS the one
    remaining "requires locating actual points over Qbar, out of scope"
    item in this list.  It is now implemented, from the spec text only,
    in the SEPARATE module search/ninfty-checker-native.py (sympy exact
    algebra: CRootOf/all_roots/series, no floating point), and wired in
    below via construct_native_from_scratch().  That module's own
    docstring carries the full derivation.  This file still performs its
    own from-scratch T-1/T-2/rootpart work using the self-implemented
    Euclid/Yun code above; ninfty-checker-native.py is a distinct,
    additional capability, not a replacement of it.
  * [SUPERSEDED 2026-08-01, C-1..C-5] E-5 (divisor orientation, (Or)) was
    formerly treated as unrecoverable from (a,p,f6) alone and caller-
    attested-only (REJECT[6] on attested=False, permanent UNKNOWN entry).
    This was stale relative to 裁定113/Prop E5-D
    (docs/notes/e5_interpretation_v1.md §2.2): under E-1..E-4 (already
    checked by check_preconditions before this point), the orientation
    IS derived, matching lane A's independent derivation (search/
    ninfty-searcher-v2.mjs L390-406). run_checker now: derives E-5 as
    True whenever E-1..E-4 passed (C-1); no longer lists E-5 as UNKNOWN
    (C-2); routes an attested=False that CONTRADICTS the derivation to
    INTEGRITY_STOP[27] instead of REJECT[6] (C-3, same class as the
    E-6 gcd(a,p)!=1-after-Pell precedent); still never REJECTs on a
    merely-absent attestation (C-4). ninfty-checker-native.py's
    `native_construction.orientation_derivation` remains available as
    an independent instance-level cross-check of this derivation.

runtime = python (stdlib only: fractions, hashlib, json, sys, argparse) for
the T-1/T-2/rootpart core above.  [20260801] The optional
construct_native_from_scratch() wrapper additionally imports
search/ninfty-checker-native.py (python + sympy exact algebra) -- a
SEPARATE module, independently derived from the governing spec text only,
never from lane A's implementation or output; see that module's own
docstring for its independence discipline.  No import of lane A code
anywhere in this file or in ninfty-checker-native.py (neither has ever
read it and neither knows its existence).  No shared math-helper library
between this file's own T-1/T-2 core and lane A; sympy itself (a public
CAS, not a project-internal helper) is used only inside
ninfty-checker-native.py, not in this file's own from-scratch algorithms.
"""

from __future__ import annotations
from fractions import Fraction
import hashlib
import json
import os
import sys
import argparse
import importlib.util

# TERMINOLOGY (Sol 便95 F95-2.3 -- 用語分離). `construct_native_from_scratch`
# produces a DIAGNOSTIC CONSTRUCTION: a native object built for inspection,
# freely constructible at any time, including BEFORE any gate, and NOT
# publishable. A MINTED/PUBLISHED ARTIFACT is something else entirely -- a
# native or NF object that passed the NF mint gate (both lanes PRESENT with
# agreeing digests) and was committed to the EP registry by
# search/ninfty-ep-genuine-provisioning.py. The broad claim "no native object
# is ever constructed before the gate" is FALSE and must not be made; the
# gate governs PUBLICATION, not construction.

# --------------------------------------------------------------------------
# Lazy loader for search/ninfty-checker-native.py [20260801].  Loaded by
# file path (not `import`, since the filename has hyphens) and only when
# construct_native_from_scratch() is actually called -- callers that never
# touch native construction pay no sympy import cost.
# --------------------------------------------------------------------------

_NATIVE_MODULE = None


def _load_native_module():
    global _NATIVE_MODULE
    if _NATIVE_MODULE is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "ninfty-checker-native.py")
        spec = importlib.util.spec_from_file_location("ninfty_checker_native", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _NATIVE_MODULE = mod
    return _NATIVE_MODULE


def construct_native_from_scratch(a_json, p_json, f6_json, series_cap=40):
    """
    Thin wrapper around ninfty-checker-native.py's construct_checker_native.
    Returns that module's result dict verbatim (status="ok" plus the
    ramification_divisor_on_C / branch_divisor_on_P1 / etc. fields, or a
    degeneracy status -- see that module's docstring). Never raises for
    ordinary malformed/degenerate candidate data.
    """
    mod = _load_native_module()
    return mod.construct_checker_native(a_json, p_json, f6_json, series_cap=series_cap)


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

# ERA DECLARATION (Sol 便96 W96-2.2 / governing spec sec.5.3.4 M-5,
# dependency manifest Y-3b). This file's DECISION-LANE part implements the
# CURRENT era's enum and routing ([27]; S2 accumulation). It emits no
# native/certificate payload, so it belongs to exactly one plane. The
# marker below is machine-read by search/ninfty-evidence-union-full.py's
# payload-era matrix; a missing or disagreeing marker is FAIL, never
# "assumed compatible".
#   [ep-era-declaration] plane=decision_lane_predicate predicate_spec_id=mb/ninfty-stage2-predicate/v19 verifier_contract_id=mb/ninfty-verifier-contract/v14 dependency_manifest_schema_id=mb/dependency-manifest/v14
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
# 19-stage table, governing spec sec.5.3.2 -- the table is [9]..[27], i.e.
# 27-9+1 = 19 stages since the v19 addition of [27]). Digest/shared-helper/
# sealed leak codes ([9]-[12]) are not this file's job (that is the
# verifier's and the receiving side's). This checker can raise:
INTEGRITY_PELL_COPRIME_MISMATCH = "pell-implies-coprime-mismatch"   # [13]
INTEGRITY_PELL_DERIVATIVE_MISMATCH = "pell-derivative-mismatch"     # [15]
# [27] 2026-08-01 (C-3, see run_checker's E-5 handling): attested orientation
# contradicts the E-1..E-4-derived value (Prop E5-D), mirrored from lane A's
# same-numbered code (search/ninfty-searcher-v2.mjs REASON_CODE_NUMBER).
INTEGRITY_DIVISOR_ORIENTATION_MISMATCH = "divisor-orientation-attestation-mismatch"  # [27]

# Sol 便96 W96-2.1 / governing spec sec.5.3.3 X-1, X-1a (v19 DRAFT repair
# R96-1): the semantic axis is exclusive BETWEEN bands (S1 -> S2 -> S3) but
# CUMULATIVE WITHIN the S2 band -- [24] (finite partition mismatch) and [27]
# (attestation contradiction) are DIFFERENT causes and both must survive into
# all_reason_codes[].  Consequences for this file (X-1a):
#   * the [27] site below no longer early-returns; it accumulates and the
#     checker keeps evaluating T-1 / T-2 / pushforward;
#   * `primary_reason_code` is no longer "whichever fired first" -- it is
#     MACHINE-COMPUTED as the minimum of the accumulated set under the
#     governing priority tables (governing spec invariant 4: (verdict,
#     primary_reason_code) must be a function of the INPUT, not of the
#     evaluation order).
# INTEGRITY_PRIORITY reproduces governing spec sec.5.3.2's 19-stage total
# order literally (enum reproduction only, no state-machine ownership).
INTEGRITY_PRIORITY = [
    "sealed-field-leak",                            # [ 9]
    "deterministic-digest-exposed",                 # [10]
    "shared-helper-detected",                       # [11]
    "digest-mismatch",                              # [12]
    "pell-implies-coprime-mismatch",                # [13]
    "divisor-identity",                             # [14]
    "pell-derivative-mismatch",                     # [15]
    "chart-degree-mismatch",                        # [16]
    "p-locus-unhandled",                            # [17]
    "weierstrass-unhandled",                        # [18]
    "infinity-unhandled",                           # [19]
    "rh-mismatch",                                  # [20]
    "extra-branch-value",                           # [21]
    "finite-branch-count-mismatch",                 # [22]
    "branch-pair-not-harmonic",                     # [23]
    "finite-partition-cross-mismatch",              # [24]
    "divisor-equality-failure",                     # [25]
    "verifier-result-mismatch",                     # [26]
    "divisor-orientation-attestation-mismatch",     # [27]
]


# governing spec sec.5.3.3: the S2 band, as an explicit (non-contiguous) set.
S2_CODES = frozenset({
    "pell-implies-coprime-mismatch",             # [13]
    "divisor-identity",                          # [14]
    "pell-derivative-mismatch",                  # [15]
    "chart-degree-mismatch",                     # [16]
    "p-locus-unhandled",                         # [17]
    "weierstrass-unhandled",                     # [18]
    "infinity-unhandled",                        # [19]
    "rh-mismatch",                               # [20]
    "extra-branch-value",                        # [21]
    "finite-branch-count-mismatch",              # [22]
    "branch-pair-not-harmonic",                  # [23]
    "finite-partition-cross-mismatch",           # [24]
    "divisor-orientation-attestation-mismatch",  # [27]
})


def _resolve_stage_and_primary(reasons):
    """
    governing spec sec.5.3 state machine, applied to THIS lane's own
    accumulated reason set (X-1a).  Returns (stage, primary).

    Fail-closed by construction: a reason string that appears in NEITHER
    priority table is not silently dropped and is not silently treated as
    a REJECT -- it sorts LAST inside whichever class it lands in, and an
    unknown code is classified as an integrity reason (the strictly more
    severe class), because an unrecognised code must never be able to
    downgrade a verdict.
    """
    rejects = [r for r in reasons if r in REJECT_PRIORITY]
    integrities = [r for r in reasons if r not in REJECT_PRIORITY]
    if integrities:
        return "INTEGRITY_STOP", min(
            integrities,
            key=lambda c: (INTEGRITY_PRIORITY.index(c) if c in INTEGRITY_PRIORITY else len(INTEGRITY_PRIORITY), c),
        )
    if rejects:
        return "REJECT", min(rejects, key=REJECT_PRIORITY.index)
    return None, None


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
        # X-1a (Sol 便96 W96-2.1): an S2-band precondition reason -- currently
        # only E-6's [13], which check_preconditions evaluates LAST, i.e. with
        # E-1..E-4 already PASSED -- must NOT terminate the lane, because the
        # S2 band is cumulative.  Lane A already accumulates [13] and [27]
        # together (search/ninfty-searcher-v2.mjs evaluateDecisionLane keeps
        # both in its I set); before this repair lane B stopped at [13] and
        # reported a strictly smaller set for the same input, which is a
        # cross-lane [26] concordance divergence waiting to happen.
        # Reasons OUTSIDE the S2 band here are the REJECT-axis preconditions
        # [1]..[5]; those genuinely invalidate the downstream algebra
        # (degrees/monicity/Pell), so they still terminate.
        if pre_reason not in S2_CODES:
            stage, primary = _resolve_stage_and_primary(reasons)
            result["stage"] = stage
            result["reason_codes"] = reasons
            result["primary_reason_code"] = primary
            result["rootpart_a"] = None
            return result

    # E-5: DERIVED, not caller-attested-only. 2026-08-01 correction (C-1..C-5,
    # docs/notes/lanea_native_semantics_v1.md §5.2 / sol_reply_94_math21.md
    # P94-4.1 item 2): E-1..E-4 (V-E5.1..V-E5.4) already passed by this point
    # (check_preconditions returned no reason above), so Prop E5-D (裁定113,
    # docs/notes/e5_interpretation_v1.md §2.2) already forces
    # div(mu) = 5(inf_-) - 5(inf_+), i.e. the STANDARD orientation, exactly as
    # lane A derives it (search/ninfty-searcher-v2.mjs L390-406). This checker
    # no longer treats divisor_orientation_attested as unrecoverable-caller-
    # only data; C-1: E-5 is derived (True) whenever this line is reached.
    derived_orientation_ok = True
    attested = candidate.get("divisor_orientation_attested", None)
    if attested is False:
        # C-3: attestation CONTRADICTS the theorem-derived value -- same class
        # as E-6's gcd(a,p)!=1-after-Pell-PASS precedent -- is an input-
        # consistency defect (INTEGRITY_STOP), not an ordinary REJECT. This
        # replaces the pre-2026-08-01 REJECT[6] routing.
        # Sol 便96 W96-2.1 / spec sec.5.3.3 X-1a (v19 DRAFT repair R96-1):
        # ACCUMULATE, do not early-return.  Before this repair the checker
        # returned here, which meant a candidate that broke BOTH the
        # attestation ([27]) and, say, (60.5) ([15]) reported only [27] --
        # exactly the evidence loss W96-2.1 objects to.  The band-level
        # semantics are unchanged: [27] is an S2 reason, and S3's [25] is
        # still suppressed whenever S2 is non-empty (see the pushforward
        # site below).
        reasons.append(INTEGRITY_DIVISOR_ORIENTATION_MISMATCH)
        result["divisor_orientation_status"] = "attested-false-contradicts-derivation"
    else:
        # C-4: attestation absent is NOT rejected -- the derived value is authoritative.
        result["divisor_orientation_status"] = (
            "derived-true-attestation-absent" if attested is None else "derived-true-attestation-agrees"
        )
    result["divisor_orientation_derived"] = derived_orientation_ok

    t1_stage, t1_reason, t1_detail = check_T1(a)
    result["T1_detail"] = t1_detail
    if t1_reason:
        # T-1 failure ([7]/[8]) is a REJECT-axis reason; it still terminates
        # this lane's evaluation because T-2's (60.5) identity is only
        # defined once T-1 produced a genuine degree-2 squarefree d (lane A
        # gates it identically).  Any S2 reason accumulated ABOVE survives
        # into reason_codes[] and, per the spec state machine, dominates:
        # I != empty => INTEGRITY_STOP (X-1a / invariant 4).
        reasons.append(t1_reason)
        stage, primary = _resolve_stage_and_primary(reasons)
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
        # S2 band, cumulative (X-1a): [15] joins whatever S2 reason is
        # already present rather than replacing or being replaced by it.
        reasons.append(t2_reason)

    if candidate.get("native_artifact") is not None:
        ok, pf_detail = check_native_pushforward(candidate["native_artifact"])
        result["pushforward_detail"] = pf_detail
        if ok is False:
            # [25] is the S3 band.  The band-level exclusion is UNCHANGED by
            # the R96-1 repair: S3 is evaluated only when the S2 band raised
            # nothing (spec sec.5.3.3 X-2 / the composition rule "elif S2 の
            # native reason が空 ...").  Written as an explicit S2-emptiness
            # test rather than the old `if stage is None`, which conflated
            # "no S2 reason" with "no reason of any kind".
            if not any(r in S2_CODES for r in reasons):
                reasons.append("divisor-equality-failure")  # [25]
            else:
                result["s3_suppressed_by_s2"] = {
                    "reason": ("[25] not raised: the S3 band is only evaluated when the S2 band is "
                               "empty (governing spec sec.5.3.3 X-2). The pushforward inconsistency "
                               "is still recorded in pushforward_detail."),
                    "s2_reasons_present": sorted(r for r in reasons if r in S2_CODES),
                }
    else:
        result["pushforward_detail"] = {"status": "UNKNOWN", "reason": "no native artifact supplied"}

    if "genus" in candidate and "deg_mu" in candidate:
        result["rh_identity_value"] = rh_bookkeeping_identity(candidate["genus"], candidate["deg_mu"])

    # [20260801] From-scratch native construction (search/ninfty-checker-native.py),
    # opt-out via candidate["skip_native_construction"]=true (e.g. for tests
    # that want to isolate the T-1/T-2 core from the sympy-dependent path).
    if not candidate.get("skip_native_construction", False):
        try:
            native = construct_native_from_scratch(candidate["a"], candidate["p"], candidate["f6"])
        except Exception as e:  # noqa: BLE001 -- never let native construction crash the checker
            native = {"status": "internal-error", "diagnostics": {"exception": f"{type(e).__name__}: {e}"}}
        result["native_construction"] = native
        # self-consistency: our own from-scratch construction must be
        # internally pushforward-consistent (independent of whether the
        # caller supplied its own native_artifact above).
        if native.get("status") == "ok":
            self_ok, self_detail = check_native_pushforward(native)
            result["native_construction_self_pushforward_check"] = {"ok": self_ok, "detail": self_detail}

    # X-1a: verdict/primary are MACHINE-COMPUTED from the accumulated set
    # under the governing priority tables, never "whichever fired first".
    stage, primary = _resolve_stage_and_primary(reasons)
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
        # E-5 removed from this list 2026-08-01 (C-2): it is no longer UNKNOWN
        # -- it is DERIVED (see run_checker's divisor_orientation_status /
        # divisor_orientation_derived fields, and Prop E5-D). Leaving it here
        # would be UNKNOWN inflation for a solved item (P94-4.1 item 2).
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
