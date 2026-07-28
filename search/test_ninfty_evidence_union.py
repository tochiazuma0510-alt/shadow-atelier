#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_evidence_union.py

Self-made test suite for search/ninfty-evidence-union.py (追補(o) v3.1,
Sol F81-3.2/F82-4.1 -> sol/sol_reply_82_math9.md N82-4.1). Exercises:
  1. compose_route_statuses: FULL 4x4=16 status-pair domain (table-driven,
     N82-4.1's explicit "16/16" requirement) + swap-symmetry over the same
     16 pairs + digest-mismatch negative cases beyond the base table.
  2. classify_route: missing/ill-typed claim_digest/evidence_digest
     negative cases (N82-4.1's explicit "missing/ill-typed digest の負例"
     requirement), plus ABSENT/PASS/FAIL positive cases and the
     coverage_digest-vs-expected_domain_digest FAIL (not MALFORMED) path.
  3. evidence_union_fail_closed_v2: end-to-end two-route composition.
  4. route_from_verifier_b_w6: armature smoke test against REAL
     ninfty-verifier-b.py verify_W6_single(...) output (not full EP
     wiring -- see module docstring SCOPE NOTE in ninfty-evidence-union.py).

Run: python search/test_ninfty_evidence_union.py
Exits 0 iff all checks PASS; prints a PASS/FAIL table and returns nonzero
on any failure.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures", "ninfty")


def _load_module(name, relpath):
    path = os.path.join(HERE, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


eu = _load_module("ninfty_evidence_union", "ninfty-evidence-union.py")
verb = _load_module("ninfty_verifier_b_for_eu_test", "ninfty-verifier-b.py")

RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append((name, ok, detail))


def load_fixture(fname):
    with open(os.path.join(FIXDIR, fname), "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# 1. compose_route_statuses -- FULL 16-pair table + swap symmetry
# --------------------------------------------------------------------------
A, M, P, F = "ABSENT", "MALFORMED", "PASS", "FAIL"
DIGEST_MATCH = "d" * 64  # not required to be real hex for this pure-function test

# Base 16-pair table (status1, status2) -> expected overall_status, with
# claim digests set EQUAL wherever both routes are non-ABSENT (the
# "well-behaved agreeing evidence" baseline -- digest-mismatch is a
# SEPARATE axis tested afterward).
BASE_TABLE = {
    (A, A): "ABSENT",
    (A, M): "INTEGRITY_STOP", (M, A): "INTEGRITY_STOP",
    (A, P): "PASS", (P, A): "PASS",
    (A, F): "FAIL", (F, A): "FAIL",
    (M, M): "INTEGRITY_STOP",
    (M, P): "INTEGRITY_STOP", (P, M): "INTEGRITY_STOP",
    (M, F): "INTEGRITY_STOP", (F, M): "INTEGRITY_STOP",
    (P, P): "PASS",
    (P, F): "CONFLICT", (F, P): "CONFLICT",
    (F, F): "FAIL",
}
record("compose_route_statuses table: BASE_TABLE covers all 16 status pairs",
       len(BASE_TABLE) == 16, f"{len(BASE_TABLE)} entries")

for (s1, s2), expected in BASE_TABLE.items():
    d1 = DIGEST_MATCH if s1 in (P, F) else None
    d2 = DIGEST_MATCH if s2 in (P, F) else None
    got = eu.compose_route_statuses(s1, d1, s2, d2)
    record(f"compose_route_statuses({s1!r}, {s2!r}) == {expected!r} (16-pair table)",
           got == expected, f"got {got!r}")

# Swap symmetry over the SAME 16 pairs: compose(s1,d1,s2,d2) ==
# compose(s2,d2,s1,d1).
for (s1, s2) in BASE_TABLE.keys():
    d1 = DIGEST_MATCH if s1 in (P, F) else None
    d2 = DIGEST_MATCH if s2 in (P, F) else None
    forward = eu.compose_route_statuses(s1, d1, s2, d2)
    backward = eu.compose_route_statuses(s2, d2, s1, d1)
    record(f"compose_route_statuses swap symmetry: ({s1!r},{s2!r}) == swap({s2!r},{s1!r})",
           forward == backward, f"forward={forward!r} backward={backward!r}")

# --------------------------------------------------------------------------
# digest-mismatch negative cases beyond the base 16-pair table (item 2 of
# 追補(o) v3.1's ordered rules: mismatch -> CONFLICT for ANY non-ABSENT
# pair, not just PASS/PASS).
# --------------------------------------------------------------------------
DIGEST_OTHER = "e" * 64
for (s1, s2, label) in [(P, P, "PASS/PASS"), (F, F, "FAIL/FAIL"), (P, F, "PASS/FAIL"), (F, P, "FAIL/PASS")]:
    got = eu.compose_route_statuses(s1, DIGEST_MATCH, s2, DIGEST_OTHER)
    record(f"compose_route_statuses digest-mismatch ({label}) -> CONFLICT (rule 2, before status composition)",
           got == "CONFLICT", f"got {got!r}")

# --------------------------------------------------------------------------
# 2. classify_route -- missing/ill-typed digest negative cases + positive
#    cases + coverage-mismatch FAIL path.
# --------------------------------------------------------------------------

# ABSENT: no blob at all, or an empty/no-evidence blob.
for label, blob in [("blob=None", None), ("blob={}", {}), ("blob={'evidence_kind':'ABSENT'}", {"evidence_kind": "ABSENT"})]:
    status, digest, detail = eu.classify_route(blob)
    record(f"classify_route({label}) -> ABSENT", status == "ABSENT" and digest is None, f"got ({status!r}, {digest!r}, {detail})")

# PASS-shaped, well-formed.
GOOD_DIGEST = "a" * 64
good_pass_blob = {
    "evidence_kind": "PASS", "claim_digest": GOOD_DIGEST, "evidence_digest": "b" * 64,
    "checked_domain_count": 3, "coverage_digest": "c" * 64,
}
status, digest, detail = eu.classify_route(good_pass_blob)
record("classify_route(well-formed PASS blob) -> PASS, claim_digest returned",
       status == "PASS" and digest == GOOD_DIGEST, f"got ({status!r}, {digest!r})")

# FAIL-shaped, well-formed.
good_fail_blob = {
    "evidence_kind": "FAIL", "claim_digest": GOOD_DIGEST, "evidence_digest": "b" * 64,
    "counterexample_locus": {"locus": "x=1"},
}
status, digest, detail = eu.classify_route(good_fail_blob)
record("classify_route(well-formed FAIL blob) -> FAIL, claim_digest returned",
       status == "FAIL" and digest == GOOD_DIGEST, f"got ({status!r}, {digest!r})")

# missing/ill-typed claim_digest.
NEGATIVE_DIGEST_CASES = [
    ("PASS missing claim_digest", {k: v for k, v in good_pass_blob.items() if k != "claim_digest"}),
    ("PASS claim_digest not 64-hex", {**good_pass_blob, "claim_digest": "not-a-digest"}),
    ("PASS claim_digest wrong length hex", {**good_pass_blob, "claim_digest": "a" * 63}),
    ("PASS missing evidence_digest", {k: v for k, v in good_pass_blob.items() if k != "evidence_digest"}),
    ("PASS evidence_digest not 64-hex", {**good_pass_blob, "evidence_digest": "zz" * 32}),
    ("FAIL missing claim_digest", {k: v for k, v in good_fail_blob.items() if k != "claim_digest"}),
    ("FAIL missing counterexample_locus", {k: v for k, v in good_fail_blob.items() if k != "counterexample_locus"}),
    ("PASS missing checked_domain_count", {k: v for k, v in good_pass_blob.items() if k != "checked_domain_count"}),
    ("PASS checked_domain_count is a string", {**good_pass_blob, "checked_domain_count": "3"}),
    ("PASS checked_domain_count is negative", {**good_pass_blob, "checked_domain_count": -1}),
    ("PASS missing coverage_digest", {k: v for k, v in good_pass_blob.items() if k != "coverage_digest"}),
    ("PASS coverage_digest not 64-hex", {**good_pass_blob, "coverage_digest": "short"}),
    ("unrecognized evidence_kind", {"evidence_kind": "BOGUS", "claim_digest": GOOD_DIGEST}),
]
for label, blob in NEGATIVE_DIGEST_CASES:
    status, digest, detail = eu.classify_route(blob)
    record(f"classify_route({label}) -> MALFORMED (N82-4.1 missing/ill-typed digest negative)",
           status == "MALFORMED", f"got ({status!r}, {digest!r}, {detail})")

# coverage_digest disagreeing with a caller-supplied expected_domain_digest
# -> FAIL (substantive disagreement), NOT MALFORMED (schema is fine).
mismatched_coverage_blob = dict(good_pass_blob)
status, digest, detail = eu.classify_route(mismatched_coverage_blob, expected_domain_digest="f" * 64)
record("classify_route(PASS with coverage_digest != caller's expected_domain_digest) -> FAIL, not MALFORMED",
       status == "FAIL" and digest == GOOD_DIGEST, f"got ({status!r}, {digest!r}, {detail})")

# coverage_digest AGREEING with expected_domain_digest -> still PASS.
agreeing_blob = dict(good_pass_blob)
status, digest, detail = eu.classify_route(agreeing_blob, expected_domain_digest=good_pass_blob["coverage_digest"])
record("classify_route(PASS with coverage_digest == caller's expected_domain_digest) -> PASS",
       status == "PASS", f"got ({status!r}, {digest!r}, {detail})")

# never raises even on wildly malformed input (fail-closed, no crash).
for label, blob in [("blob is a string", "not-a-dict"), ("blob is a list", [1, 2, 3]),
                    ("blob has non-dict counterexample_locus is fine (any non-None ok)", {"evidence_kind": "FAIL", "claim_digest": GOOD_DIGEST, "evidence_digest": GOOD_DIGEST, "counterexample_locus": 0})]:
    try:
        status, digest, detail = eu.classify_route(blob)
        raised = False
    except Exception:
        raised = True
    record(f"classify_route({label}) does not raise", raised is False, "raised!" if raised else f"status={status!r}")


# --------------------------------------------------------------------------
# 3. evidence_union_fail_closed_v2 -- end-to-end two-route composition.
# --------------------------------------------------------------------------
result_both_pass = eu.evidence_union_fail_closed_v2(good_pass_blob, dict(good_pass_blob))
record("evidence_union_fail_closed_v2(PASS, PASS, same claim) -> overall PASS",
       result_both_pass["overall_status"] == "PASS", result_both_pass)

result_pass_fail = eu.evidence_union_fail_closed_v2(good_pass_blob, good_fail_blob)
record("evidence_union_fail_closed_v2(PASS, FAIL) -> overall CONFLICT",
       result_pass_fail["overall_status"] == "CONFLICT", result_pass_fail)

result_malformed = eu.evidence_union_fail_closed_v2({"evidence_kind": "PASS"}, good_pass_blob)
record("evidence_union_fail_closed_v2(MALFORMED-shaped, PASS) -> overall INTEGRITY_STOP",
       result_malformed["overall_status"] == "INTEGRITY_STOP", result_malformed)

result_absent_absent = eu.evidence_union_fail_closed_v2(None, {})
record("evidence_union_fail_closed_v2(None, {}) -> overall ABSENT",
       result_absent_absent["overall_status"] == "ABSENT", result_absent_absent)

result_absent_pass = eu.evidence_union_fail_closed_v2(None, good_pass_blob)
record("evidence_union_fail_closed_v2(None, PASS) -> overall PASS",
       result_absent_pass["overall_status"] == "PASS", result_absent_pass)


# --------------------------------------------------------------------------
# 4. route_from_verifier_b_w6 -- armature smoke test against REAL
#    verify_W6_single(...) output (search/ninfty-verifier-b.py), NOT full
#    EP wiring (see ninfty-evidence-union.py module docstring SCOPE NOTE).
# --------------------------------------------------------------------------
_cert_pos_01 = load_fixture("cert_pos_01.json")
w6_status_real, w6_detail_real = verb.verify_W6_single(
    _cert_pos_01["certificate"], _cert_pos_01["native_a"], _cert_pos_01["native_b"],
)
record("smoke: real cert_pos_01.json verify_W6_single -> PASS (sanity, unaffected by this file)",
       w6_status_real == "PASS", f"got {w6_status_real!r}: {w6_detail_real}")

route_blob_from_real_w6 = eu.route_from_verifier_b_w6(w6_status_real, w6_detail_real)
status_via_connector, digest_via_connector, detail_via_connector = eu.classify_route(route_blob_from_real_w6)
record("route_from_verifier_b_w6(real PASS result) -> classify_route resolves to PASS (armature round-trip)",
       status_via_connector == "PASS", f"got {status_via_connector!r}: {detail_via_connector}")

# cert_neg_03.json is this repo's own self-made negative fixture, purpose-
# built so the cross-lane pushforward maps genuinely disagree (checker
# lane's multiplicity deliberately mismatched) -- a real FAIL, not a
# digest-integrity MALFORMED (which is what naively re-tampering
# map_ref.inline in place -- without recomputing its digest -- would
# produce instead; using the purpose-built fixture avoids that pitfall).
_cert_neg_03 = load_fixture("cert_neg_03.json")
w6_status_fail, w6_detail_fail = verb.verify_W6_single(
    _cert_neg_03["certificate"], _cert_neg_03["native_a"], _cert_neg_03["native_b"],
)
record("smoke: cert_neg_03.json verify_W6_single -> FAIL (setup check)",
       w6_status_fail == "FAIL", f"got {w6_status_fail!r}: {w6_detail_fail}")
route_blob_fail = eu.route_from_verifier_b_w6(w6_status_fail, w6_detail_fail)
status_fail_via_connector, _, _ = eu.classify_route(route_blob_fail)
record("route_from_verifier_b_w6(real FAIL result) -> classify_route resolves to FAIL (armature round-trip)",
       status_fail_via_connector == "FAIL", f"got {status_fail_via_connector!r}")

# ABSENT connector round-trip.
route_blob_absent = eu.route_from_verifier_b_w6("ABSENT", {"reason": "not supplied"})
status_absent_via_connector, _, _ = eu.classify_route(route_blob_absent)
record("route_from_verifier_b_w6('ABSENT', ...) -> classify_route resolves to ABSENT (armature round-trip)",
       status_absent_via_connector == "ABSENT", f"got {status_absent_via_connector!r}")

# MALFORMED connector round-trip.
route_blob_malformed = eu.route_from_verifier_b_w6("MALFORMED", {"reason": "schema violation"})
status_malformed_via_connector, _, _ = eu.classify_route(route_blob_malformed)
record("route_from_verifier_b_w6('MALFORMED', ...) -> classify_route resolves to MALFORMED (armature round-trip)",
       status_malformed_via_connector == "MALFORMED", f"got {status_malformed_via_connector!r}")

# end-to-end: compose the REAL PASS route (as "R1") against a synthetic
# agreeing "R2" -- confirms the connector's output is genuinely usable as
# one side of evidence_union_fail_closed_v2, not just classify_route alone.
r2_agreeing = dict(route_blob_from_real_w6)  # same claim_digest, same PASS shape
combined = eu.evidence_union_fail_closed_v2(route_blob_from_real_w6, r2_agreeing)
record("evidence_union_fail_closed_v2(real-W6-PASS-via-connector, agreeing R2) -> overall PASS",
       combined["overall_status"] == "PASS", combined)


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
def main():
    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    n_total = len(RESULTS)
    width = max(len(name) for name, _, _ in RESULTS)
    for name, ok, detail in RESULTS:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name.ljust(width)}  {detail}")
    print(f"\n{n_pass}/{n_total} checks passed.")
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
