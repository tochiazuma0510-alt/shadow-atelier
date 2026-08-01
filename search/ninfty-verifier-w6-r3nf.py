#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

# ERA DECLARATION (Sol 便96 W96-2.2 / governing spec sec.5.3.4, dependency
# manifest Y-3b). R3-NF is a CURRENT-era route: it was created by the 便95
# repair wave against spec v19 / contract v14 / manifest v14. It is NOT a
# frozen historical route (those are R1/R2) and it does NOT close W-6
# (便96 W96-2.3 / spec sec.5.3.5 W6-C2). The marker below is machine-read
# by search/ninfty-evidence-union-full.py's payload-era matrix.
#   [ep-era-declaration] plane=nf_route predicate_spec_id=mb/ninfty-stage2-predicate/v19 verifier_contract_id=mb/ninfty-verifier-contract/v14 dependency_manifest_schema_id=mb/dependency-manifest/v14

search/ninfty-verifier-w6-r3nf.py

R3-NF: the THIRD evidence route of the N∞ evidence union (Sol 便95
sol_reply_95_math22.md F95-2.2, 司令塔裁定 2026-08-01 item 5).

Sol's F95-2.2 declined the proposal to teach the frozen R1/R2 routes a
second schema ("旧 native token semantics と NF semantics を一つの verifier
に混ぜると、どちらを通った PASS かが不明になる") and instead approved a NEW
route id with this exact contract:

  - R1/R2 remain historical frozen routes, byte- and semantics-identical
    (this file does not import, modify, or wrap either of them, and
    search/ninfty-evidence-union.py is not touched by R3-NF at all -- the
    three-column full union lives in the separate, additive
    search/ninfty-evidence-union-full.py).
  - R3-NF takes SAME-GENERATION `nf_a`/`nf_b` role artifacts AND their
    digests as REQUIRED inputs (registry resolution is the caller's job,
    see search/ninfty-evidence-union-full.py `_resolve_nf_registry`;
    this module is the PREDICATE over the two resolved contents).
  - R3-NF confirms, FAIL-CLOSED: N-1..N-5, total degree, infinity,
    non-ramification certificate, and BOTH producers' provenance.
  - The full union prints R1, R2 and R3-NF in SEPARATE columns; none of
    the three is ever a substitute for another.

STATUS VOCABULARY (deliberately the same four tokens the union's
RouteResult layer already uses, so the full-union composer needs no new
enum): PASS / FAIL / ABSENT / MALFORMED.

  ABSENT     -- at least one lane minted no NF at all (status != "PRESENT"
                on a well-formed report). Evidence insufficiency, never a
                silent PASS. Note: a lane reporting INTEGRITY_STOP is also
                ABSENT *for this route* (there is no NF to compare); the
                lane's own INTEGRITY_STOP is not swallowed -- it is echoed
                verbatim in the detail's `lane_a_status`/`lane_b_status`.
  MALFORMED   -- shape/schema violation (not a dict, wrong nf_schema_id,
                missing nf, non-64-hex nf_digest, a lane self-declaring the
                wrong producer identity, a declared nf_digest that does not
                match the receiver's own recomputation, ...). A schema
                violation is never folded into FAIL or ABSENT (same
                discipline as ninfty-verifier-b.py 裁定139).
  FAIL        -- both NFs exist and are well-shaped, but at least one of
                the checked equalities/identities does not hold.
  PASS        -- every check below holds.

CHECKS (every one is required for PASS; each is reported individually in
the detail, so a FAIL always names which check broke):

  R3-1 shape/producer identity  -- both contents are dicts with
        nf_schema_id == NF_SCHEMA_ID, status == "PRESENT", nf a dict,
        nf_digest exact 64-hex, and lane == "A" / lane == "B"
        RESPECTIVELY (the both-producer-provenance requirement: an
        nf_a slot carrying lane B's own report, or the same lane's report
        duplicated into both slots, is MALFORMED here, not a PASS).
  R3-2 digest recomputation     -- sha256 over each lane's OWN `nf`
        sub-object, canonically serialized by the receiver, must equal
        that lane's DECLARED nf_digest (self-reported digests are never
        accepted on their own word).
  R3-3 cross-lane digest        -- the two lanes' nf_digest agree.
  R3-4 N-1..N-5                 -- the five §4.1 equalities, implemented
        HERE, independently of search/ninfty-nf-crosscheck.py (which is a
        candidate-driven harness that shells out to the two lane CLIs; here
        is a receiver-side predicate over already-minted artifacts and
        imports neither it nor either lane).
  R3-5 total degree             -- 2*deg(ram_finite)*coefficient == 4 and
        sum(deg*coefficient over branch components, at_infinity counted
        with degree 1) == 12, on BOTH lanes independently.
  R3-6 infinity                 -- ram_infinite == {(inf_+,5,4),(inf_-,5,4)}
        on both lanes, and exactly one at_infinity branch component whose
        coefficient agrees across the lanes.
  R3-7 non-ramification cert    -- p_locus and w_locus are each declared
        squarefree with a coprimality witness on BOTH lanes, and the two
        generators agree across the lanes.

R3-5's identities restate N-2/N-4's numeric halves; they are checked (and
reported) separately ON PURPOSE -- F95-2.2 lists "N-1--N-5" and "total
degree" as two distinct required confirmations, and a future edit that
weakened N-2/N-4 would still have to defeat R3-5 as well.

"cross-checked", not "verified" (project convention: verified is reserved
for Lean).

runtime = python, stdlib only (hashlib, json, fractions).
"""
from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction

NF_SCHEMA_ID = "mb/ninfty-nf/v1"
ROUTE_ID_R3NF = "R3-NF"
IMPLEMENTATION_ID_R3NF = "ninfty-verifier-w6-r3nf.py::verify_R3_NF"

HEX64 = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)

# The theorem-forced constants this route re-checks. They are NOT tunable
# knobs: they are the §4.1 normal-form identities for the N∞ stage-2
# family (degree 12 branch divisor on P^1, reduced finite ramification of
# total degree 4, two order-5 points over infinity each contributing 4).
TOTAL_BRANCH_DEGREE = 12
TOTAL_FINITE_RAM_DEGREE = 4
EXPECTED_INFINITY = {("inf_+", 5, 4), ("inf_-", 5, 4)}


def canonical_serialize(obj):
    """Project-wide canonical form: UTF-8, sorted keys, no whitespace --
    identical convention to ninfty-verifier-b.py / ninfty-nf-laneb.py /
    ninfty-evidence-union.py (this is a data contract, not shared code)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_of(obj):
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def _is_64hex(x):
    return isinstance(x, str) and bool(HEX64.match(x))


def _rat(s):
    s = str(s)
    if "/" in s:
        n, d = s.split("/")
        return Fraction(int(n), int(d))
    return Fraction(int(s))


def _poly_eq(coeffs_a, coeffs_b):
    """Low-degree-first exact rational coefficient lists, both already
    required MONIC by §4.1 -- a non-monic generator from either lane is a
    reportable mismatch, never silently renormalized here."""
    try:
        return [_rat(c) for c in coeffs_a] == [_rat(c) for c in coeffs_b]
    except (ValueError, TypeError, ZeroDivisionError):
        return False


def _is_monic(coeffs):
    try:
        return len(coeffs) >= 2 and _rat(coeffs[-1]) == 1
    except (ValueError, TypeError, ZeroDivisionError, IndexError):
        return False


def _shape_errors(content, expected_lane, slot):
    """R3-1/R3-2. Returns a list of schema errors (empty = well-shaped)."""
    errs = []
    if not isinstance(content, dict):
        return [f"{slot}: NF artifact content is not an object (got {type(content).__name__})"]
    if content.get("nf_schema_id") != NF_SCHEMA_ID:
        errs.append(f"{slot}: nf_schema_id must be exactly {NF_SCHEMA_ID!r}, got {content.get('nf_schema_id')!r}")
    if content.get("lane") != expected_lane:
        errs.append(
            f"{slot}: lane must be {expected_lane!r} (both-producer provenance: the nf_a slot must carry "
            f"lane A's own report and the nf_b slot lane B's -- one lane's report in both slots is not a "
            f"two-producer agreement), got {content.get('lane')!r}"
        )
    status = content.get("status")
    if status == "PRESENT":
        nf = content.get("nf")
        if not isinstance(nf, dict):
            errs.append(f"{slot}: status=PRESENT but 'nf' is not an object (got {type(nf).__name__})")
        declared = content.get("nf_digest")
        if not _is_64hex(declared):
            errs.append(f"{slot}: nf_digest must be exact 64-hex, got {declared!r}")
        elif isinstance(nf, dict):
            recomputed = sha256_of(nf)
            if recomputed != declared:
                errs.append(
                    f"{slot}: declared nf_digest {declared!r} != receiver-recomputed {recomputed!r} -- a "
                    "producer's own digest claim is never accepted on its own word (R3-2)"
                )
    elif status not in ("ABSENT", "INTEGRITY_STOP"):
        errs.append(
            f"{slot}: status must be one of PRESENT/ABSENT/INTEGRITY_STOP, got {status!r}"
        )
    return errs


def _check_n1(nf_a, nf_b, out):
    rf_a, rf_b = nf_a["ram_finite"], nf_b["ram_finite"]
    ga, gb = rf_a.get("ideal_generator"), rf_b.get("ideal_generator")
    monic = _is_monic(ga) and _is_monic(gb)
    match = _poly_eq(ga, gb)
    out["N-1"] = {"pass": bool(monic and match), "monic_both_lanes": monic,
                  "generators_agree": match, "lane_a_generator": ga, "lane_b_generator": gb}


def _check_n2_and_total_finite_degree(nf_a, nf_b, out):
    rf_a, rf_b = nf_a["ram_finite"], nf_b["ram_finite"]
    ca, cb = rf_a.get("coefficient"), rf_b.get("coefficient")
    deg_a = len(rf_a.get("ideal_generator") or []) - 1
    deg_b = len(rf_b.get("ideal_generator") or []) - 1
    coef_eq = (ca == cb) and isinstance(ca, int) and not isinstance(ca, bool)
    id_a = isinstance(ca, int) and not isinstance(ca, bool) and 2 * deg_a * ca == TOTAL_FINITE_RAM_DEGREE
    id_b = isinstance(cb, int) and not isinstance(cb, bool) and 2 * deg_b * cb == TOTAL_FINITE_RAM_DEGREE
    out["N-2"] = {"pass": bool(coef_eq and id_a and id_b), "coefficient_equal": coef_eq,
                  "degree_identity_lane_a": id_a, "degree_identity_lane_b": id_b}
    # R3-5 half 1 (reported separately on purpose, see module docstring).
    out["R3-5-finite-degree"] = {
        "pass": bool(id_a and id_b),
        "lane_a_total": 2 * deg_a * ca if isinstance(ca, int) and not isinstance(ca, bool) else None,
        "lane_b_total": 2 * deg_b * cb if isinstance(cb, int) and not isinstance(cb, bool) else None,
        "expected": TOTAL_FINITE_RAM_DEGREE,
    }


def _check_n3_and_infinity(nf_a, nf_b, out):
    def _inf_set(ram_inf):
        if not isinstance(ram_inf, list):
            return None
        try:
            return {(str(e["point"]).replace("_plus", "_+").replace("_minus", "_-"),
                     e["e"], e["coefficient"]) for e in ram_inf}
        except (KeyError, TypeError):
            return None
    ia, ib = _inf_set(nf_a.get("ram_infinite")), _inf_set(nf_b.get("ram_infinite"))
    n3 = (ia == EXPECTED_INFINITY) and (ib == EXPECTED_INFINITY)
    out["N-3"] = {"pass": bool(n3),
                  "lane_a": sorted(str(x) for x in ia) if ia is not None else None,
                  "lane_b": sorted(str(x) for x in ib) if ib is not None else None,
                  "expected": sorted(str(x) for x in EXPECTED_INFINITY)}


def _branch_classify(components):
    if not isinstance(components, list):
        return None, None, None
    lin, quad, inf = [], [], []
    for c in components:
        if not isinstance(c, dict):
            return None, None, None
        if c.get("at_infinity"):
            inf.append(c)
            continue
        gen = c.get("ideal_generator")
        if not isinstance(gen, list):
            return None, None, None
        if len(gen) == 2:
            lin.append(c)
        elif len(gen) == 3:
            quad.append(c)
        else:
            # any other degree is an unrecognized branch component shape --
            # fail the whole classification rather than silently dropping it
            return None, None, None
    return lin, quad, inf


def _check_n4_and_branch_degree(nf_a, nf_b, out):
    comps_a = (nf_a.get("branch") or {}).get("components")
    comps_b = (nf_b.get("branch") or {}).get("components")
    lin_a, quad_a, inf_a = _branch_classify(comps_a)
    lin_b, quad_b, inf_b = _branch_classify(comps_b)
    shape_ok = all(x is not None for x in (lin_a, quad_a, inf_a, lin_b, quad_b, inf_b)) and \
        len(lin_a) == 1 and len(quad_a) == 1 and len(inf_a) == 1 and \
        len(lin_b) == 1 and len(quad_b) == 1 and len(inf_b) == 1
    if not shape_ok:
        out["N-4"] = {"pass": False, "shape_ok": False,
                      "reason": "branch component shape (exactly 1 linear + 1 quadratic + 1 at_infinity) not "
                                "found on both lanes -- possible -C-square split-vs-undecomposed convention "
                                "mismatch (Sol 便94 F94-4.2)"}
        out["R3-5-branch-degree"] = {"pass": False, "reason": "branch shape gate failed; degree sum not computed"}
        out["R3-6-infinity-component"] = {"pass": False, "reason": "branch shape gate failed"}
        return
    lin_match = _poly_eq(lin_a[0]["ideal_generator"], lin_b[0]["ideal_generator"]) and \
        lin_a[0].get("coefficient") == lin_b[0].get("coefficient")
    quad_match = _poly_eq(quad_a[0]["ideal_generator"], quad_b[0]["ideal_generator"]) and \
        quad_a[0].get("coefficient") == quad_b[0].get("coefficient")
    inf_match = inf_a[0].get("coefficient") == inf_b[0].get("coefficient")
    monic_ok = all(_is_monic(c[0]["ideal_generator"]) for c in (lin_a, quad_a, lin_b, quad_b))

    def _deg_sum(lin, quad, inf):
        try:
            return 1 * lin[0]["coefficient"] + 2 * quad[0]["coefficient"] + inf[0]["coefficient"]
        except (KeyError, TypeError):
            return None
    ds_a, ds_b = _deg_sum(lin_a, quad_a, inf_a), _deg_sum(lin_b, quad_b, inf_b)
    deg_ok = (ds_a == TOTAL_BRANCH_DEGREE) and (ds_b == TOTAL_BRANCH_DEGREE)
    out["N-4"] = {"pass": bool(lin_match and quad_match and inf_match and monic_ok and deg_ok),
                  "shape_ok": True, "lin_match": lin_match, "quad_match": quad_match,
                  "inf_match": inf_match, "monic_both_lanes": monic_ok,
                  "degree_sum_lane_a": ds_a, "degree_sum_lane_b": ds_b}
    # R3-5 half 2.
    out["R3-5-branch-degree"] = {"pass": bool(deg_ok), "lane_a_total": ds_a, "lane_b_total": ds_b,
                                 "expected": TOTAL_BRANCH_DEGREE}
    # R3-6 (branch half; the ram_infinite half is N-3 above).
    out["R3-6-infinity-component"] = {
        "pass": bool(inf_match and inf_a[0].get("coefficient") == 4),
        "lane_a_at_infinity_coefficient": inf_a[0].get("coefficient"),
        "lane_b_at_infinity_coefficient": inf_b[0].get("coefficient"),
        "expected": 4,
    }


def _check_n5_and_nonram(nf_a, nf_b, out):
    nrc_a = nf_a.get("non_ramification_certificates")
    nrc_b = nf_b.get("non_ramification_certificates")
    if not isinstance(nrc_a, dict) or not isinstance(nrc_b, dict):
        out["N-5"] = {"pass": False, "reason": "non_ramification_certificates missing on at least one lane"}
        out["R3-7-non-ramification"] = {"pass": False, "reason": "non_ramification_certificates missing"}
        return
    ok_shape = True
    detail = {}
    for lane, nrc in (("lane_a", nrc_a), ("lane_b", nrc_b)):
        for locus, coprime_key in (("p_locus", "coprime_to_f6"), ("w_locus", "coprime_to_p")):
            blk = nrc.get(locus)
            good = (
                isinstance(blk, dict)
                and blk.get("squarefree") is True
                and isinstance(blk.get(coprime_key), dict)
                and blk[coprime_key].get("coprime") is True
                and isinstance(blk.get("generator"), list)
                and _is_monic(blk.get("generator"))
            )
            detail[f"{lane}.{locus}"] = bool(good)
            ok_shape = ok_shape and good
    p_match = ok_shape and _poly_eq(nrc_a["p_locus"]["generator"], nrc_b["p_locus"]["generator"])
    w_match = ok_shape and _poly_eq(nrc_a["w_locus"]["generator"], nrc_b["w_locus"]["generator"])
    out["N-5"] = {"pass": bool(p_match and w_match), "p_locus_match": p_match, "w_locus_match": w_match}
    out["R3-7-non-ramification"] = {"pass": bool(ok_shape), "per_lane_certificates": detail,
                                    "note": "each locus must declare squarefree=true AND a coprime=true "
                                            "witness on BOTH lanes (Theorem B cancellation certificate)"}


def verify_R3_NF(nf_a_content, nf_b_content):
    """
    The R3-NF predicate. `nf_a_content`/`nf_b_content` are the REGISTRY-
    RESOLVED `content` of the same generation's nf_a / nf_b role artifacts
    (the caller resolves and pins them; this function never reads a
    registry, a file, or a producer's self-declared provenance block).

    Returns (status, detail) with status in
    {"PASS","FAIL","ABSENT","MALFORMED"} -- never raises.
    """
    detail = {"route_id": ROUTE_ID_R3NF, "implementation_id": IMPLEMENTATION_ID_R3NF}

    if not isinstance(nf_a_content, dict) or not nf_a_content or \
       not isinstance(nf_b_content, dict) or not nf_b_content:
        detail["reason"] = (
            "one or both NF artifacts were not supplied at all (empty/non-object content -- e.g. the "
            "caller's registry resolution failed for that role). No NF exists to compare: ABSENT, never a "
            "silent PASS."
        )
        detail["lane_a_supplied"] = isinstance(nf_a_content, dict) and bool(nf_a_content)
        detail["lane_b_supplied"] = isinstance(nf_b_content, dict) and bool(nf_b_content)
        return "ABSENT", detail

    errs = _shape_errors(nf_a_content, "A", "nf_a") + _shape_errors(nf_b_content, "B", "nf_b")
    if errs:
        detail["schema_errors"] = errs
        return "MALFORMED", detail

    detail["lane_a_status"] = nf_a_content.get("status")
    detail["lane_b_status"] = nf_b_content.get("status")
    if nf_a_content.get("status") != "PRESENT" or nf_b_content.get("status") != "PRESENT":
        detail["reason"] = (
            "at least one lane minted no NF (status != PRESENT) -- N-1..N-5 are reported ABSENT, never "
            "silently treated as PASS. The lanes' own statuses are echoed above verbatim; an "
            "INTEGRITY_STOP on either lane is a lane-level finding this route does not overwrite."
        )
        detail["decision_lane_concordance"] = nf_a_content.get("status") == nf_b_content.get("status")
        return "ABSENT", detail

    # R3-3 (cross-lane digest agreement). Both digests were already
    # recomputed-and-matched per lane by _shape_errors (R3-2).
    checks = {}
    digest_match = nf_a_content["nf_digest"] == nf_b_content["nf_digest"]
    checks["R3-3-cross-lane-digest"] = {"pass": bool(digest_match),
                                        "lane_a": nf_a_content["nf_digest"],
                                        "lane_b": nf_b_content["nf_digest"]}

    nf_a, nf_b = nf_a_content["nf"], nf_b_content["nf"]
    for required in ("ram_finite", "ram_infinite", "branch", "non_ramification_certificates"):
        if required not in nf_a or required not in nf_b:
            detail["schema_errors"] = [f"nf.{required} missing on at least one lane"]
            return "MALFORMED", detail
    if not isinstance(nf_a["ram_finite"], dict) or not isinstance(nf_b["ram_finite"], dict):
        detail["schema_errors"] = ["nf.ram_finite is not an object on at least one lane"]
        return "MALFORMED", detail

    _check_n1(nf_a, nf_b, checks)
    _check_n2_and_total_finite_degree(nf_a, nf_b, checks)
    _check_n3_and_infinity(nf_a, nf_b, checks)
    _check_n4_and_branch_degree(nf_a, nf_b, checks)
    _check_n5_and_nonram(nf_a, nf_b, checks)

    # R3-1's producer half, restated as an explicit reported check (the
    # MALFORMED gate above already enforces it).
    checks["R3-1-both-producer-provenance"] = {
        "pass": True,
        "lane_a": nf_a_content.get("lane"),
        "lane_b": nf_b_content.get("lane"),
        "lane_a_decision": nf_a_content.get("decision_verdict", nf_a_content.get("decision_stage")),
        "lane_b_decision": nf_b_content.get("decision_stage", nf_b_content.get("decision_verdict")),
    }

    failed = sorted(k for k, v in checks.items() if not v.get("pass"))
    detail["checks"] = checks
    detail["failed_checks"] = failed
    detail["cross_checked_not_verified"] = True
    if failed:
        detail["reason"] = f"R3-NF: {len(failed)} of {len(checks)} checks failed: {failed}"
        return "FAIL", detail
    detail["reason"] = f"R3-NF: all {len(checks)} checks passed"
    return "PASS", detail
