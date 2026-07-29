#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_evidence_union.py

Self-made test suite for search/ninfty-evidence-union.py (追補(o) v5,
RouteResult two-layer per 裁定192 N83-2.3 -> sol/裁定_192_便83検収.md,
sol/sol_reply_83_math10.md F83-2.1/2.2/2.3; nominal gate hardened per Sol
便84 F84-5.4/P84-5 -> sol/sol_reply_84_math11.md; trust-boundary hardened
per Sol 便85 F85-6.3 B85-o1..o4/P85-5 -> sol/sol_reply_85_math12.md).
Exercises:
  1. compose_route_statuses: FULL 4x4=16 status-pair domain (table-driven)
     + swap-symmetry + digest-mismatch negatives + the F83-2.2 low-level
     digest-format defense.
  2. _route_result_pass/fail/absent/malformed constructors (module-private
     per Sol 便85 P85-5 item 7): valid construction + the F83-2.1
     invariants + the NEW 便85 B85-o2 required-refs invariant.
  3. coerce_to_route_result: None -> ABSENT; any OTHER non-object ->
     MALFORMED; unrecognized route_status -> MALFORMED; foreign
     status-shape field co-presence; the NEW 便85 B85-o2 refs=None probe.
  4. evidence_union_fail_closed_v2: end-to-end, built via constructors
     (white-box composition plumbing test -- NOT the public trust
     boundary, see 7b).
  5. route_from_verifier_b_w6: armature smoke test against REAL
     verify_W6_single(...) output (now takes a `raw` parameter, 便85).
  6. Sol 便84 P84-5.4 hardening -- nominal-gate literal probes.
  7. Sol 便85 F85-6.3 B85-o1..o4 -- trust-boundary hardening: the literal
     probes from sol/sol_reply_85_math12.md F85-6.3 (valid-shape forged
     PASS, refs=None, unknown w6_status), negativized and asserted to the
     RETURNED status, PLUS end-to-end tests of the new public entry point
     `evidence_union_from_raw_w6` (the only trust boundary this module now
     exposes for untrusted/raw input).

Run: python search/test_ninfty_evidence_union.py
Exits 0 iff all checks PASS; prints a PASS/FAIL table and returns nonzero
on any failure.
"""
import importlib.util
import inspect
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


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64
DIGEST_C = "c" * 64
REF_SRC = {"source": "test-fixture", "digest": DIGEST_A}
REF_LIST = [REF_SRC]


# --------------------------------------------------------------------------
# 1. compose_route_statuses -- FULL 16-pair table + swap symmetry + digest
#    negatives + F83-2.2 low-level digest-format defense. (Unaffected by
#    the 便85 trust-boundary repair -- compose_route_statuses' 4-rule
#    structure is unchanged.)
# --------------------------------------------------------------------------
A, M, P, F = "ABSENT", "MALFORMED", "PASS", "FAIL"
DIGEST_MATCH = "d" * 64

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

for (s1, s2) in BASE_TABLE.keys():
    d1 = DIGEST_MATCH if s1 in (P, F) else None
    d2 = DIGEST_MATCH if s2 in (P, F) else None
    forward = eu.compose_route_statuses(s1, d1, s2, d2)
    backward = eu.compose_route_statuses(s2, d2, s1, d1)
    record(f"compose_route_statuses swap symmetry: ({s1!r},{s2!r}) == swap({s2!r},{s1!r})",
           forward == backward, f"forward={forward!r} backward={backward!r}")

DIGEST_OTHER = "e" * 64
for (s1, s2, label) in [(P, P, "PASS/PASS"), (F, F, "FAIL/FAIL"), (P, F, "PASS/FAIL"), (F, P, "FAIL/PASS")]:
    got = eu.compose_route_statuses(s1, DIGEST_MATCH, s2, DIGEST_OTHER)
    record(f"compose_route_statuses digest-mismatch ({label}) -> CONFLICT (rule 2, before status composition)",
           got == "CONFLICT", f"got {got!r}")

_low_level_probe = eu.compose_route_statuses("PASS", None, "PASS", None)
record("裁定192 F83-2.2: compose_route_statuses(PASS, None, PASS, None) -> INTEGRITY_STOP (was PASS)",
       _low_level_probe == "INTEGRITY_STOP", f"got {_low_level_probe!r}")
_low_level_probe2 = eu.compose_route_statuses("FAIL", "not-64-hex", "FAIL", "not-64-hex")
record("裁定192 F83-2.2: compose_route_statuses(FAIL, <non-hex>, FAIL, <non-hex>) -> INTEGRITY_STOP",
       _low_level_probe2 == "INTEGRITY_STOP", f"got {_low_level_probe2!r}")


# --------------------------------------------------------------------------
# 2. RouteResult constructors (module-private, Sol 便85 P85-5 item 7) --
#    valid construction + F83-2.1 invariants + NEW B85-o2 required-refs
#    invariant, all enforced by the constructor itself.
# --------------------------------------------------------------------------

_good_pass = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
)
record("_route_result_pass: valid construction -> route_status=PASS", _good_pass.get("route_status") == "PASS", _good_pass)
record("_route_result_pass: route_id preserved", _good_pass.get("route_id") == "R1", _good_pass)
record("_route_result_pass: schema_id present", isinstance(_good_pass.get("schema_id"), str) and len(_good_pass["schema_id"]) > 0, _good_pass)

# F83-2.1: count mismatch -> constructor refuses PASS, falls back to MALFORMED.
_bad_pass_count = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=0,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
)
record("_route_result_pass: expected_domain_count != checked_domain_count -> constructor refuses, route_status=MALFORMED (F83-2.1)",
       _bad_pass_count.get("route_status") == "MALFORMED", _bad_pass_count)

# F83-2.1/N82-4.1: expected digest != coverage digest -> constructor refuses.
_bad_pass_digest = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest="f" * 64,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
)
record("_route_result_pass: expected_domain_digest != coverage_digest -> constructor refuses, route_status=MALFORMED",
       _bad_pass_digest.get("route_status") == "MALFORMED", _bad_pass_digest)

# ill-typed digest -> MALFORMED.
_bad_pass_digest_type = eu._route_result_pass(
    "R1", "not-hex", DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
)
record("_route_result_pass: claim_digest not 64-hex -> constructor refuses, route_status=MALFORMED",
       _bad_pass_digest_type.get("route_status") == "MALFORMED", _bad_pass_digest_type)

# Sol 便85 B85-o2: claim_source_ref/evidence_refs are now REQUIRED (no
# default None) -- omitting/nulling them must refuse construction.
_bad_pass_no_refs = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=None, evidence_refs=None,
)
record("Sol 便85 B85-o2: _route_result_pass with claim_source_ref=None/evidence_refs=None -> constructor refuses, route_status=MALFORMED",
       _bad_pass_no_refs.get("route_status") == "MALFORMED", _bad_pass_no_refs)
_bad_pass_illshaped_refs = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref={"source": "x"}, evidence_refs=[],
)
record("Sol 便85 B85-o2: _route_result_pass with ill-shaped claim_source_ref (missing digest) / empty evidence_refs -> MALFORMED",
       _bad_pass_illshaped_refs.get("route_status") == "MALFORMED", _bad_pass_illshaped_refs)

_good_fail = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[{"locus": "x=1"}],
                                    claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
record("_route_result_fail: valid construction -> route_status=FAIL", _good_fail.get("route_status") == "FAIL", _good_fail)

_bad_fail_empty_loci = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[],
                                              claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
record("_route_result_fail: empty counterexample_loci -> constructor refuses, route_status=MALFORMED (F83-2.1)",
       _bad_fail_empty_loci.get("route_status") == "MALFORMED", _bad_fail_empty_loci)

_bad_fail_digest = eu._route_result_fail("R2", None, DIGEST_B, counterexample_loci=[{"locus": "x=1"}],
                                          claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
record("_route_result_fail: claim_digest missing -> constructor refuses, route_status=MALFORMED",
       _bad_fail_digest.get("route_status") == "MALFORMED", _bad_fail_digest)

_bad_fail_no_refs = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[{"locus": "x=1"}],
                                           claim_source_ref=None, evidence_refs=None)
record("Sol 便85 B85-o2: _route_result_fail with claim_source_ref=None/evidence_refs=None -> constructor refuses, route_status=MALFORMED",
       _bad_fail_no_refs.get("route_status") == "MALFORMED", _bad_fail_no_refs)

_good_absent = eu._route_result_absent("R1", {"reason": "no evidence supplied"})
record("_route_result_absent: valid construction -> route_status=ABSENT", _good_absent.get("route_status") == "ABSENT", _good_absent)

_bad_absent = eu._route_result_absent("R1", None)
record("_route_result_absent: missing_mask=None -> constructor refuses, route_status=MALFORMED",
       _bad_absent.get("route_status") == "MALFORMED", _bad_absent)

_good_malformed = eu._route_result_malformed("R1", ["some schema error"])
record("_route_result_malformed: valid construction -> route_status=MALFORMED", _good_malformed.get("route_status") == "MALFORMED", _good_malformed)

_malformed_empty_errs = eu._route_result_malformed("R1", [])
record("_route_result_malformed: empty schema_errors -> generic fallback substituted, still MALFORMED",
       _malformed_empty_errs.get("route_status") == "MALFORMED" and len(_malformed_empty_errs.get("schema_errors", [])) > 0,
       _malformed_empty_errs)


# --------------------------------------------------------------------------
# 3. coerce_to_route_result -- None->ABSENT; any OTHER non-object->MALFORMED
#    (returned status explicitly asserted, 便83 ★4); unrecognized
#    route_status; foreign status-shape co-presence (LITERAL Sol probe);
#    NEW 便85 B85-o2 refs=None probe.
# --------------------------------------------------------------------------

status, digest, detail = eu.coerce_to_route_result(None)
record("coerce_to_route_result(None) -> ABSENT", status == "ABSENT", f"got ({status!r}, {digest!r}, {detail})")

for label, val in [("string 'garbage'", "garbage"), ("empty list []", []), ("empty dict {} (no route_status at all)", {}),
                   ("integer 0", 0), ("boolean True", True)]:
    status, digest, detail = eu.coerce_to_route_result(val)
    record(f"裁定192 F83-2.2: coerce_to_route_result({label}) -> MALFORMED exactly (returned status asserted, not just 'no crash')",
           status == "MALFORMED", f"got status={status!r}: {detail}")

status, digest, detail = eu.coerce_to_route_result({"route_status": "BOGUS"})
record("coerce_to_route_result(unrecognized route_status) -> MALFORMED", status == "MALFORMED", f"got {status!r}: {detail}")

# LITERAL Sol probe (F83-2.2): a PASS-shaped result ALSO carrying
# counterexample_loci (a FAIL-only field) -- must be MALFORMED regardless
# of which field set "looks more complete"; and removing counterexample_loci
# entirely still leaves a well-formed PASS (confirms the field itself, not
# some other defect, is what triggers MALFORMED).
_superset_route = dict(_good_pass)
_superset_route["counterexample_loci"] = [{"locus": "smuggled-in"}]
status, digest, detail = eu.coerce_to_route_result(_superset_route)
record("裁定192 F83-2.2 literal probe: PASS-shaped result ALSO carrying counterexample_loci -> MALFORMED "
       "(status-shape co-presence, never silently resolved to PASS)",
       status == "MALFORMED", f"got {status!r}: {detail}")

status, digest, detail = eu.coerce_to_route_result(_good_pass)
record("coerce_to_route_result(well-formed PASS, no foreign fields) -> PASS (control for the probe above)",
       status == "PASS" and digest == DIGEST_A, f"got {status!r}: {detail}")

# same probe the other direction: FAIL-shaped result ALSO carrying a PASS-only field.
_fail_with_pass_field = dict(_good_fail)
_fail_with_pass_field["coverage_digest"] = DIGEST_C
status, digest, detail = eu.coerce_to_route_result(_fail_with_pass_field)
record("裁定192 F83-2.2: FAIL-shaped result ALSO carrying coverage_digest (PASS-only field) -> MALFORMED",
       status == "MALFORMED", f"got {status!r}: {detail}")

# ABSENT result also carrying a PASS-only field -> MALFORMED.
_absent_with_pass_field = dict(_good_absent)
_absent_with_pass_field["checked_domain_count"] = 5
status, digest, detail = eu.coerce_to_route_result(_absent_with_pass_field)
record("裁定192 F83-2.2: ABSENT-shaped result ALSO carrying checked_domain_count (PASS-only field) -> MALFORMED",
       status == "MALFORMED", f"got {status!r}: {detail}")

# Sol 便85 B85-o2 literal probe: a well-formed-looking PASS route with
# claim_source_ref/evidence_refs blanked to None -- must be MALFORMED, not
# silently accepted (this was PASS before the fix).
_probe_refs_none_pass = dict(_good_pass)
_probe_refs_none_pass["claim_source_ref"] = None
_probe_refs_none_pass["evidence_refs"] = None
status, digest, detail = eu.coerce_to_route_result(_probe_refs_none_pass, expected_route_id="R1")
record("Sol 便85 B85-o2 literal probe: coerce_to_route_result(PASS route with claim_source_ref=None, "
       "evidence_refs=None) -> MALFORMED (was PASS pre-fix)",
       status == "MALFORMED", f"got {status!r}: {detail}")

# constructors' own output round-trips cleanly through coerce_to_route_result.
for label, built, expected_status in [
    ("_route_result_pass", _good_pass, "PASS"),
    ("_route_result_fail", _good_fail, "FAIL"),
    ("_route_result_absent", _good_absent, "ABSENT"),
    ("_route_result_malformed", _good_malformed, "MALFORMED"),
]:
    status, digest, detail = eu.coerce_to_route_result(built)
    record(f"coerce_to_route_result({label} output) -> {expected_status} (round-trip)",
           status == expected_status, f"got {status!r}: {detail}")


# --------------------------------------------------------------------------
# 4. evidence_union_fail_closed_v2 -- end-to-end, built via constructors
#    (white-box composition-plumbing test; NOT the public trust boundary,
#    see section 7b for that).
# --------------------------------------------------------------------------
_pass_r1 = eu._route_result_pass("R1", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                  claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
_pass_r2_agree = eu._route_result_pass("R2", DIGEST_A, "f" * 64, 3, 3, DIGEST_C, DIGEST_C,
                                        claim_source_ref=REF_SRC, evidence_refs=REF_LIST)  # same claim_digest
result_both_pass = eu.evidence_union_fail_closed_v2(_pass_r1, _pass_r2_agree)
record("evidence_union_fail_closed_v2(PASS R1, PASS R2, same claim_digest) -> overall PASS",
       result_both_pass["overall_status"] == "PASS", result_both_pass)

_fail_r2 = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, [{"locus": "x=1"}],
                                  claim_source_ref=REF_SRC, evidence_refs=REF_LIST)  # same claim_digest as R1
result_pass_fail = eu.evidence_union_fail_closed_v2(_pass_r1, _fail_r2)
record("evidence_union_fail_closed_v2(PASS R1, FAIL R2, same claim) -> overall CONFLICT",
       result_pass_fail["overall_status"] == "CONFLICT", result_pass_fail)

_malformed_r2 = eu._route_result_malformed("R2", ["bad shape"])
result_malformed = eu.evidence_union_fail_closed_v2(_malformed_r2, _pass_r1)
record("evidence_union_fail_closed_v2(MALFORMED R2, PASS R1) -> overall INTEGRITY_STOP",
       result_malformed["overall_status"] == "INTEGRITY_STOP", result_malformed)

_absent_r2 = eu._route_result_absent("R2", {"x": True})
result_absent_absent = eu.evidence_union_fail_closed_v2(None, _absent_r2)
record("evidence_union_fail_closed_v2(None, ABSENT[R2]) -> overall ABSENT",
       result_absent_absent["overall_status"] == "ABSENT", result_absent_absent)

_pass_r2_solo = eu._route_result_pass("R2", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                       claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
result_absent_pass = eu.evidence_union_fail_closed_v2(None, _pass_r2_solo)
record("evidence_union_fail_closed_v2(None, PASS[R2]) -> overall PASS",
       result_absent_pass["overall_status"] == "PASS", result_absent_pass)

# foreign/malicious input directly at the top level -> MALFORMED -> INTEGRITY_STOP.
result_garbage = eu.evidence_union_fail_closed_v2("garbage", _pass_r1)
record("evidence_union_fail_closed_v2('garbage', PASS) -> overall INTEGRITY_STOP (non-object is MALFORMED, not ABSENT)",
       result_garbage["overall_status"] == "INTEGRITY_STOP", result_garbage)


# --------------------------------------------------------------------------
# 5. route_from_verifier_b_w6 -- armature smoke test against REAL
#    verify_W6_single(...) output. Sol 便85 change: now takes a `raw`
#    parameter (the raw evidence artifact refs are computed against).
# --------------------------------------------------------------------------
_cert_pos_01 = load_fixture("cert_pos_01.json")
w6_status_real, w6_detail_real = verb.verify_W6_single(
    _cert_pos_01["certificate"], _cert_pos_01["native_a"], _cert_pos_01["native_b"],
)
record("smoke: real cert_pos_01.json verify_W6_single -> PASS (sanity, unaffected by this file)",
       w6_status_real == "PASS", f"got {w6_status_real!r}: {w6_detail_real}")

route_from_real_w6 = eu.route_from_verifier_b_w6(w6_status_real, w6_detail_real, "R1", _cert_pos_01)
record("route_from_verifier_b_w6(real PASS result, 'R1', raw) -> is a well-formed RouteResult (route_status=PASS, route_id=R1)",
       route_from_real_w6.get("route_status") == "PASS" and route_from_real_w6.get("route_id") == "R1",
       route_from_real_w6)
status_via_connector, digest_via_connector, detail_via_connector = eu.coerce_to_route_result(route_from_real_w6)
record("route_from_verifier_b_w6(real PASS result) -> coerce_to_route_result resolves to PASS (armature round-trip)",
       status_via_connector == "PASS", f"got {status_via_connector!r}: {detail_via_connector}")

# Sol 便85 B85-o4: PASS domain claim is now grounded in the real two-lane
# W-6 contract, not a hardcoded placeholder "1".
record("Sol 便85 B85-o4: route_from_verifier_b_w6 PASS branch reports expected_domain_count==checked_domain_count==2 "
       "(the real W6_DOMAIN_LANES count, not the old hardcoded placeholder 1)",
       route_from_real_w6.get("expected_domain_count") == 2 and route_from_real_w6.get("checked_domain_count") == 2,
       route_from_real_w6)

_cert_neg_03 = load_fixture("cert_neg_03.json")
w6_status_fail, w6_detail_fail = verb.verify_W6_single(
    _cert_neg_03["certificate"], _cert_neg_03["native_a"], _cert_neg_03["native_b"],
)
record("smoke: cert_neg_03.json verify_W6_single -> FAIL (setup check)",
       w6_status_fail == "FAIL", f"got {w6_status_fail!r}: {w6_detail_fail}")
route_fail = eu.route_from_verifier_b_w6(w6_status_fail, w6_detail_fail, "R2", _cert_neg_03)
record("route_from_verifier_b_w6(real FAIL result, 'R2', raw) -> route_status=FAIL, route_id=R2",
       route_fail.get("route_status") == "FAIL" and route_fail.get("route_id") == "R2", route_fail)
status_fail_via_connector, _, _ = eu.coerce_to_route_result(route_fail)
record("route_from_verifier_b_w6(real FAIL result) -> coerce_to_route_result resolves to FAIL (armature round-trip)",
       status_fail_via_connector == "FAIL", f"got {status_fail_via_connector!r}")

route_absent = eu.route_from_verifier_b_w6("ABSENT", {"reason": "not supplied"}, "R1", {"note": "synthetic-absent-raw"})
status_absent_via_connector, _, _ = eu.coerce_to_route_result(route_absent)
record("route_from_verifier_b_w6('ABSENT', ..., raw) -> coerce_to_route_result resolves to ABSENT (armature round-trip)",
       status_absent_via_connector == "ABSENT", f"got {status_absent_via_connector!r}")

route_malformed = eu.route_from_verifier_b_w6("MALFORMED", {"reason": "schema violation"}, "R2", {"note": "synthetic-malformed-raw"})
status_malformed_via_connector, _, _ = eu.coerce_to_route_result(route_malformed)
record("route_from_verifier_b_w6('MALFORMED', ..., raw) -> coerce_to_route_result resolves to MALFORMED (armature round-trip)",
       status_malformed_via_connector == "MALFORMED", f"got {status_malformed_via_connector!r}")

# end-to-end: compose the REAL PASS route (as "R1") against a synthetic
# agreeing "R2" built the same way, from the SAME raw -- confirms the
# connector's output is genuinely usable as one side of
# evidence_union_fail_closed_v2.
r2_agreeing = eu.route_from_verifier_b_w6(w6_status_real, w6_detail_real, "R2", _cert_pos_01)  # same underlying evidence -> same claim_digest
combined = eu.evidence_union_fail_closed_v2(route_from_real_w6, r2_agreeing)
record("evidence_union_fail_closed_v2(real-W6-PASS-via-connector R1, agreeing R2) -> overall PASS",
       combined["overall_status"] == "PASS", combined)


# --------------------------------------------------------------------------
# 6. Sol 便84 P84-5.4 hardening -- the LITERAL adversarial probes from
#    sol/sol_reply_84_math11.md F84-5.4 (schema_id missing/foreign,
#    route_id missing/producer-chosen/wrong-slot, unknown header fields),
#    each asserted to the RETURNED status (not just "no crash"), including
#    the end-to-end combinator overall_status.
# --------------------------------------------------------------------------

# F84-5.4 literal probe 1: schema_id missing, route_id missing,
# route_status="PASS" -- used to reach PASS; must now be MALFORMED.
_probe_no_schema_id = {"route_status": "PASS", "claim_digest": DIGEST_A, "evidence_digest": DIGEST_B,
                        "expected_domain_count": 3, "checked_domain_count": 3,
                        "expected_domain_digest": DIGEST_C, "coverage_digest": DIGEST_C}
status, digest, detail = eu.coerce_to_route_result(_probe_no_schema_id, expected_route_id="R1")
record("P84-5.4 probe: {schema_id missing, route_id missing, route_status=PASS} -> MALFORMED (was PASS)",
       status == "MALFORMED", f"got {status!r}: {detail}")

# F84-5.4 literal probe 2: schema_id="evil/v9", route_id="producer-choice".
_probe_evil_schema = dict(_probe_no_schema_id, schema_id="evil/v9", route_id="producer-choice")
status, digest, detail = eu.coerce_to_route_result(_probe_evil_schema, expected_route_id="R1")
record('P84-5.4 probe: {schema_id="evil/v9", route_id="producer-choice"} -> MALFORMED (was PASS)',
       status == "MALFORMED", f"got {status!r}: {detail}")

# F84-5.4 literal probe 3: the union of the two forged routes above -- was
# overall PASS, must now be overall INTEGRITY_STOP (both sides MALFORMED).
result_forged_union = eu.evidence_union_fail_closed_v2(_probe_no_schema_id, _probe_evil_schema)
record("P84-5.4 probe: evidence_union_fail_closed_v2(forged-no-schema_id, forged-evil-schema_id) -> "
       "overall INTEGRITY_STOP (was overall PASS)",
       result_forged_union["overall_status"] == "INTEGRITY_STOP", result_forged_union)

# F84-5.4 item 3: _route_result_pass("producer-choice", ...) itself must
# refuse (constructor-level enum), falling back to MALFORMED.
_producer_choice_pass = eu._route_result_pass("producer-choice", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                               claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
record('P84-5.4 item 3: _route_result_pass("producer-choice", ...) -> route_status=MALFORMED (constructor refuses)',
       _producer_choice_pass.get("route_status") == "MALFORMED", _producer_choice_pass)
_producer_choice_fail = eu._route_result_fail("also-not-r1-or-r2", DIGEST_A, DIGEST_B, [{"locus": "x=1"}],
                                               claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
record('P84-5.4 item 3: _route_result_fail("also-not-r1-or-r2", ...) -> route_status=MALFORMED (constructor refuses)',
       _producer_choice_fail.get("route_status") == "MALFORMED", _producer_choice_fail)
_producer_choice_absent = eu._route_result_absent("bogus-id", {"reason": "x"})
record('P84-5.4 item 3: _route_result_absent("bogus-id", ...) -> route_status=MALFORMED (constructor refuses)',
       _producer_choice_absent.get("route_status") == "MALFORMED", _producer_choice_absent)

# F84-5.4 item 2: top-level slot binding -- first argument must be
# route_id="R1", second must be "R2", even when BOTH routes are otherwise
# perfectly well-formed. Swapping them must not silently succeed.
_r1_route = eu._route_result_pass("R1", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                   claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
_r2_route = eu._route_result_pass("R2", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                   claim_source_ref=REF_SRC, evidence_refs=REF_LIST)
status_wrong_slot, _, detail_wrong_slot = eu.coerce_to_route_result(_r2_route, expected_route_id="R1")
record("P84-5.4 item 2: a well-formed route_id='R2' route placed in the FIRST (R1) slot -> MALFORMED",
       status_wrong_slot == "MALFORMED", f"got {status_wrong_slot!r}: {detail_wrong_slot}")
result_swapped_slots = eu.evidence_union_fail_closed_v2(_r2_route, _r1_route)  # R2 first, R1 second -- swapped
record("P84-5.4 item 2: evidence_union_fail_closed_v2(R2-route, R1-route) [swapped slots] -> overall INTEGRITY_STOP",
       result_swapped_slots["overall_status"] == "INTEGRITY_STOP", result_swapped_slots)
result_correct_slots = eu.evidence_union_fail_closed_v2(_r1_route, _r2_route)  # control: correct order
record("P84-5.4 item 2 control: evidence_union_fail_closed_v2(R1-route, R2-route) [correct slots] -> overall PASS",
       result_correct_slots["overall_status"] == "PASS", result_correct_slots)

# F84-5.4 item 4: an unknown/foreign header field on an otherwise
# well-formed PASS route -- must be MALFORMED, not silently ignored.
_probe_unknown_field = dict(_r1_route)
_probe_unknown_field["evil_extra_field"] = "smuggled-in"
status, digest, detail = eu.coerce_to_route_result(_probe_unknown_field, expected_route_id="R1")
record('P84-5.4 item 4: well-formed PASS route ALSO carrying "evil_extra_field" -> MALFORMED',
       status == "MALFORMED", f"got {status!r}: {detail}")

# F84-5.4 item 5: route_from_verifier_b_w6 now populates claim_source_ref/
# evidence_refs from the raw evidence (never left as None).
_w6_route_for_refs = eu.route_from_verifier_b_w6(w6_status_real, w6_detail_real, "R1", _cert_pos_01)
record("P84-5.4 item 5: route_from_verifier_b_w6(...) populates claim_source_ref (not None)",
       _w6_route_for_refs.get("claim_source_ref") is not None, _w6_route_for_refs.get("claim_source_ref"))
record("P84-5.4 item 5: route_from_verifier_b_w6(...) populates evidence_refs (not None)",
       _w6_route_for_refs.get("evidence_refs") is not None, _w6_route_for_refs.get("evidence_refs"))


# --------------------------------------------------------------------------
# 7. Sol 便85 F85-6.3 B85-o1..o4 -- trust-boundary hardening. The THREE
#    literal probes from sol/sol_reply_85_math12.md F85-6.3 (valid-shape
#    forged PASS, refs=None, unknown w6_status), negativized and asserted
#    to the RETURNED status, PLUS the union path -- and end-to-end tests
#    of the new public entry point evidence_union_from_raw_w6.
# --------------------------------------------------------------------------

h = DIGEST_A
_forged_ref = {"source": "forged-by-producer", "digest": h}
_probe_r1_valid_shape = eu._route_result_pass(
    "R1", h, h, 1, 1, h, h, claim_source_ref=_forged_ref, evidence_refs=[_forged_ref],
)
_probe_r2_valid_shape = eu._route_result_pass(
    "R2", h, h, 1, 1, h, h, claim_source_ref=_forged_ref, evidence_refs=[_forged_ref],
)
record("Sol 便85 F85-6.3 probe (control): a valid-shape, self-asserted PASS RouteResult coerces to PASS at "
       "the LOW-LEVEL nominal gate in isolation -- documents that shape alone is NOT provenance; this is why "
       "the fix has to be architectural (no code path from a bare RouteResult dict to PASS at the PUBLIC "
       "trust boundary any more -- see the evidence_union_from_raw_w6 probes below)",
       eu.coerce_to_route_result(_probe_r1_valid_shape)[0] == "PASS", "n/a")
_probe_union_low_level = eu.evidence_union_fail_closed_v2(_probe_r1_valid_shape, _probe_r2_valid_shape)
record("Sol 便85 F85-6.3 probe (control): evidence_union_fail_closed_v2(forged-but-valid-shape R1, R2) -> "
       "still overall PASS at the white-box combinator layer (EXPECTED -- this function only ever re-checks "
       "SHAPE; B85-o1's fix is that this layer is no longer reachable from untrusted input at all, see 7b)",
       _probe_union_low_level["overall_status"] == "PASS", _probe_union_low_level)

# B85-o2 literal probe: refs=None.
_probe_refs_none_direct = dict(_probe_r1_valid_shape)
_probe_refs_none_direct["claim_source_ref"] = None
_probe_refs_none_direct["evidence_refs"] = None
status_refs_none, _, detail_refs_none = eu.coerce_to_route_result(_probe_refs_none_direct, expected_route_id="R1")
record("Sol 便85 B85-o2 literal probe: r1.claim_source_ref=None, r1.evidence_refs=None -> coerce -> MALFORMED "
       "(was PASS pre-fix per F85-6.3's literal probe transcript)",
       status_refs_none == "MALFORMED", f"got {status_refs_none!r}: {detail_refs_none}")
_probe_union_refs_none = eu.evidence_union_fail_closed_v2(_probe_refs_none_direct, _probe_r2_valid_shape)
record("Sol 便85 B85-o2: evidence_union_fail_closed_v2(refs=None R1, valid-shape R2) -> overall INTEGRITY_STOP "
       "(was overall PASS per F85-6.3's transcript: 'union(r1,r2) = PASS')",
       _probe_union_refs_none["overall_status"] == "INTEGRITY_STOP", _probe_union_refs_none)

# B85-o3 literal probe: unknown w6_status ("BOGUS") against the REAL adapter.
_forged_detail = {"reason": "forged BOGUS status probe (Sol 便85 F85-6.3 literal transcript)"}
route_bogus = eu.route_from_verifier_b_w6("BOGUS", _forged_detail, "R2", {"note": "synthetic-bogus-probe-raw"})
record('Sol 便85 B85-o3 literal probe: route_from_verifier_b_w6("BOGUS", forged_detail, "R2", raw).route_status '
       '-> MALFORMED (was PASS pre-fix per F85-6.3\'s transcript: '
       '\'route_from_verifier_b_w6("BOGUS", forged_detail, "R2").route_status = PASS\')',
       route_bogus.get("route_status") == "MALFORMED", route_bogus)
status_bogus_via_coerce, _, _ = eu.coerce_to_route_result(route_bogus, expected_route_id="R2")
record("Sol 便85 B85-o3: coerce_to_route_result(route_from_verifier_b_w6('BOGUS', ...)) -> MALFORMED",
       status_bogus_via_coerce == "MALFORMED", f"got {status_bogus_via_coerce!r}")


# --------------------------------------------------------------------------
# 7b. evidence_union_from_raw_w6 -- the ACTUAL public trust-boundary entry
#     point (Sol 便85 P85-5 items 1/6/7). Confirms genuine raw evidence is
#     independently re-verified end to end, AND that neither a forged
#     valid-shape RouteResult pair nor the retired {route1, route2}
#     top-level shape can reach PASS through this function at all.
# --------------------------------------------------------------------------

RAW_SCHEMA = eu.RAW_W6_EVIDENCE_SCHEMA_ID

_raw_pos_01 = {"schema_id": RAW_SCHEMA, "certificate": _cert_pos_01["certificate"],
               "native_a": _cert_pos_01["native_a"], "native_b": _cert_pos_01["native_b"]}
result_from_raw_pos = eu.evidence_union_from_raw_w6(_raw_pos_01)
record("evidence_union_from_raw_w6(genuine raw evidence, cert_pos_01) -> overall PASS (receiver-side dispatch "
       "actually invoked verify_W6_single itself; both R1/R2 refs independently cross-checked against this raw)",
       result_from_raw_pos["overall_status"] == "PASS", result_from_raw_pos)

_raw_neg_03 = {"schema_id": RAW_SCHEMA, "certificate": _cert_neg_03["certificate"],
               "native_a": _cert_neg_03["native_a"], "native_b": _cert_neg_03["native_b"]}
result_from_raw_neg = eu.evidence_union_from_raw_w6(_raw_neg_03)
record("evidence_union_from_raw_w6(genuine raw evidence, cert_neg_03) -> overall FAIL (real recomputed FAIL, both routes agree)",
       result_from_raw_neg["overall_status"] == "FAIL", result_from_raw_neg)

# B85-o1 architectural probe: feeding the OLD top-level {route1, route2}
# shape (a forged-but-valid-shape RouteResult pair) to the NEW public
# entry point must not be interpretable as raw evidence at all --
# schema_id mismatch -> both _run_w6_verifier calls see a non-raw-evidence
# shape -> MALFORMED -> the union resolves to INTEGRITY_STOP, never PASS.
_forged_route_pair_as_raw = {"route1": _probe_r1_valid_shape, "route2": _probe_r2_valid_shape}
result_forged_top_level = eu.evidence_union_from_raw_w6(_forged_route_pair_as_raw)
record("Sol 便85 B85-o1 architectural probe: evidence_union_from_raw_w6({route1, route2} forged-but-valid-shape "
       "pair) -> overall INTEGRITY_STOP (the old top-level shape is not raw evidence; the public entry point "
       "never accepts a pre-built RouteResult -- this reached overall PASS through the retired main() before the fix)",
       result_forged_top_level["overall_status"] == "INTEGRITY_STOP", result_forged_top_level)

# a raw evidence artifact missing the required schema_id entirely.
result_bad_raw_schema = eu.evidence_union_from_raw_w6({"certificate": {}, "native_a": {}, "native_b": {}})
record("evidence_union_from_raw_w6(raw evidence missing schema_id) -> overall INTEGRITY_STOP",
       result_bad_raw_schema["overall_status"] == "INTEGRITY_STOP", result_bad_raw_schema)

# a raw evidence artifact with the right schema_id but missing native_b.
result_bad_raw_missing_key = eu.evidence_union_from_raw_w6(
    {"schema_id": RAW_SCHEMA, "certificate": _cert_pos_01["certificate"], "native_a": _cert_pos_01["native_a"]}
)
record("evidence_union_from_raw_w6(raw evidence missing native_b) -> overall INTEGRITY_STOP",
       result_bad_raw_missing_key["overall_status"] == "INTEGRITY_STOP", result_bad_raw_missing_key)

# non-dict raw entirely.
result_garbage_raw = eu.evidence_union_from_raw_w6("garbage")
record("evidence_union_from_raw_w6('garbage') -> overall INTEGRITY_STOP", result_garbage_raw["overall_status"] == "INTEGRITY_STOP", result_garbage_raw)
result_none_raw = eu.evidence_union_from_raw_w6(None)
record("evidence_union_from_raw_w6(None) -> overall INTEGRITY_STOP (raw evidence absence is a schema problem here, "
       "not a route-level ABSENT -- this function's contract is 'a raw artifact was supplied', not 'a route was supplied')",
       result_none_raw["overall_status"] == "INTEGRITY_STOP", result_none_raw)

# structural check (items 1/2): no route_id / route1 / route2 parameter
# exists anywhere a caller could smuggle a pre-verified route through.
_sig = inspect.signature(eu.evidence_union_from_raw_w6)
record("Sol 便85 P85-5 item 1: evidence_union_from_raw_w6 takes exactly one parameter (the raw evidence "
       "artifact) -- no route_id/route1/route2 parameter for a caller to bypass verification with",
       list(_sig.parameters.keys()) == ["raw"], str(_sig))
_sig_r1 = inspect.signature(eu._build_R1)
_sig_r2 = inspect.signature(eu._build_R2)
record("Sol 便85 P85-5 item 2: _build_R1/_build_R2 take exactly one parameter each (raw) -- no route_id "
       "parameter a caller could pass to choose the slot",
       list(_sig_r1.parameters.keys()) == ["raw"] and list(_sig_r2.parameters.keys()) == ["raw"],
       f"{_sig_r1} / {_sig_r2}")

# item 4: a raw evidence artifact whose certificate is doctored AFTER
# _build_R1 ran (simulated by cross-checking the SAME already-built route
# against a DIFFERENT raw artifact) must be caught -- refs must resolve to
# the raw the receiver actually holds, not merely to some digest the
# route self-reports.
_route1_from_pos = eu._build_R1(_raw_pos_01)
_other_raw = {"schema_id": RAW_SCHEMA, "certificate": {"different": True}, "native_a": {}, "native_b": {}}
_cross_checked_against_wrong_raw = eu._cross_check_refs_against_raw(_route1_from_pos, _other_raw)
record("Sol 便85 B85-o2/item 4: _cross_check_refs_against_raw(route built from raw_pos_01, but checked "
       "against a DIFFERENT raw artifact) -> MALFORMED (refs digest does not match the receiver's own "
       "recomputed digest of the raw it actually holds)",
       _cross_checked_against_wrong_raw.get("route_status") == "MALFORMED", _cross_checked_against_wrong_raw)
_cross_checked_against_same_raw = eu._cross_check_refs_against_raw(_route1_from_pos, _raw_pos_01)
record("Sol 便85 B85-o2/item 4 control: _cross_check_refs_against_raw(route built from raw_pos_01, checked "
       "against the SAME raw_pos_01) -> unchanged route_status (PASS)",
       _cross_checked_against_same_raw.get("route_status") == "PASS", _cross_checked_against_same_raw)


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
