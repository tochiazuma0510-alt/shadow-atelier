#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_evidence_union.py

Self-made test suite for search/ninfty-evidence-union.py (追補(o) v3.1,
RouteResult two-layer per 裁定192 N83-2.3 -> sol/裁定_192_便83検収.md,
sol/sol_reply_83_math10.md F83-2.1/2.2/2.3). Exercises:
  1. compose_route_statuses: FULL 4x4=16 status-pair domain (table-driven)
     + swap-symmetry + digest-mismatch negatives + the NEW low-level
     digest-format defense (F83-2.2: compose_route_statuses(PASS, None,
     PASS, None) must no longer reach PASS).
  2. route_result_pass/fail/absent/malformed constructors: valid
     construction + the F83-2.1 invariants (expected/checked count
     equality, expected/coverage digest equality) enforced BY THE
     CONSTRUCTOR ITSELF (a caller cannot build an internally-inconsistent
     "PASS").
  3. coerce_to_route_result: None -> ABSENT; any OTHER non-object -> the
     RETURNED STATUS explicitly asserted to be MALFORMED (not ABSENT,
     F83-2.2); unrecognized route_status -> MALFORMED; foreign
     status-shape field co-presence (the LITERAL Sol probe: a PASS-shaped
     result also carrying counterexample_locus) -> MALFORMED, with and
     without a "kind" hint (there is no evidence_kind field in this schema
     at all anymore, so this closes F83-2.2 by construction).
  4. evidence_union_fail_closed_v2: end-to-end, built via constructors.
  5. route_from_verifier_b_w6: armature smoke test against REAL
     verify_W6_single(...) output (search/ninfty-verifier-b.py), now
     producing genuine RouteResult objects (not ad hoc blobs).

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


DIGEST_A = "a" * 64
DIGEST_B = "b" * 64
DIGEST_C = "c" * 64


# --------------------------------------------------------------------------
# 1. compose_route_statuses -- FULL 16-pair table + swap symmetry + digest
#    negatives + F83-2.2 low-level digest-format defense.
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

# F83-2.2 literal probe: low-level digest-missing PASS/PASS must NOT reach
# PASS anymore (defense in depth at compose_route_statuses itself).
_low_level_probe = eu.compose_route_statuses("PASS", None, "PASS", None)
record("裁定192 F83-2.2: compose_route_statuses(PASS, None, PASS, None) -> INTEGRITY_STOP (was PASS)",
       _low_level_probe == "INTEGRITY_STOP", f"got {_low_level_probe!r}")
_low_level_probe2 = eu.compose_route_statuses("FAIL", "not-64-hex", "FAIL", "not-64-hex")
record("裁定192 F83-2.2: compose_route_statuses(FAIL, <non-hex>, FAIL, <non-hex>) -> INTEGRITY_STOP",
       _low_level_probe2 == "INTEGRITY_STOP", f"got {_low_level_probe2!r}")


# --------------------------------------------------------------------------
# 2. RouteResult constructors -- valid construction + F83-2.1 invariants
#    enforced by the constructor itself.
# --------------------------------------------------------------------------

_good_pass = eu.route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
)
record("route_result_pass: valid construction -> route_status=PASS", _good_pass.get("route_status") == "PASS", _good_pass)
record("route_result_pass: route_id preserved", _good_pass.get("route_id") == "R1", _good_pass)
record("route_result_pass: schema_id present", isinstance(_good_pass.get("schema_id"), str) and len(_good_pass["schema_id"]) > 0, _good_pass)

# F83-2.1: count mismatch -> constructor refuses PASS, falls back to MALFORMED.
_bad_pass_count = eu.route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=0,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
)
record("route_result_pass: expected_domain_count != checked_domain_count -> constructor refuses, route_status=MALFORMED (F83-2.1)",
       _bad_pass_count.get("route_status") == "MALFORMED", _bad_pass_count)

# F83-2.1/N82-4.1: expected digest != coverage digest -> constructor refuses.
_bad_pass_digest = eu.route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest="f" * 64,
)
record("route_result_pass: expected_domain_digest != coverage_digest -> constructor refuses, route_status=MALFORMED",
       _bad_pass_digest.get("route_status") == "MALFORMED", _bad_pass_digest)

# ill-typed digest -> MALFORMED.
_bad_pass_digest_type = eu.route_result_pass(
    "R1", "not-hex", DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
)
record("route_result_pass: claim_digest not 64-hex -> constructor refuses, route_status=MALFORMED",
       _bad_pass_digest_type.get("route_status") == "MALFORMED", _bad_pass_digest_type)

_good_fail = eu.route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[{"locus": "x=1"}])
record("route_result_fail: valid construction -> route_status=FAIL", _good_fail.get("route_status") == "FAIL", _good_fail)

_bad_fail_empty_loci = eu.route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[])
record("route_result_fail: empty counterexample_loci -> constructor refuses, route_status=MALFORMED (F83-2.1)",
       _bad_fail_empty_loci.get("route_status") == "MALFORMED", _bad_fail_empty_loci)

_bad_fail_digest = eu.route_result_fail("R2", None, DIGEST_B, counterexample_loci=[{"locus": "x=1"}])
record("route_result_fail: claim_digest missing -> constructor refuses, route_status=MALFORMED",
       _bad_fail_digest.get("route_status") == "MALFORMED", _bad_fail_digest)

_good_absent = eu.route_result_absent("R1", {"reason": "no evidence supplied"})
record("route_result_absent: valid construction -> route_status=ABSENT", _good_absent.get("route_status") == "ABSENT", _good_absent)

_bad_absent = eu.route_result_absent("R1", None)
record("route_result_absent: missing_mask=None -> constructor refuses, route_status=MALFORMED",
       _bad_absent.get("route_status") == "MALFORMED", _bad_absent)

_good_malformed = eu.route_result_malformed("R1", ["some schema error"])
record("route_result_malformed: valid construction -> route_status=MALFORMED", _good_malformed.get("route_status") == "MALFORMED", _good_malformed)

_malformed_empty_errs = eu.route_result_malformed("R1", [])
record("route_result_malformed: empty schema_errors -> generic fallback substituted, still MALFORMED",
       _malformed_empty_errs.get("route_status") == "MALFORMED" and len(_malformed_empty_errs.get("schema_errors", [])) > 0,
       _malformed_empty_errs)


# --------------------------------------------------------------------------
# 3. coerce_to_route_result -- None->ABSENT; any OTHER non-object->MALFORMED
#    (returned status explicitly asserted, 便83 ★4); unrecognized
#    route_status; foreign status-shape co-presence (LITERAL Sol probe).
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

# constructors' own output round-trips cleanly through coerce_to_route_result.
for label, built, expected_status in [
    ("route_result_pass", _good_pass, "PASS"),
    ("route_result_fail", _good_fail, "FAIL"),
    ("route_result_absent", _good_absent, "ABSENT"),
    ("route_result_malformed", _good_malformed, "MALFORMED"),
]:
    status, digest, detail = eu.coerce_to_route_result(built)
    record(f"coerce_to_route_result({label} output) -> {expected_status} (round-trip)",
           status == expected_status, f"got {status!r}: {detail}")


# --------------------------------------------------------------------------
# 4. evidence_union_fail_closed_v2 -- end-to-end, built via constructors.
# --------------------------------------------------------------------------
_pass_r1 = eu.route_result_pass("R1", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C)
_pass_r2_agree = eu.route_result_pass("R2", DIGEST_A, "f" * 64, 3, 3, DIGEST_C, DIGEST_C)  # same claim_digest
result_both_pass = eu.evidence_union_fail_closed_v2(_pass_r1, _pass_r2_agree)
record("evidence_union_fail_closed_v2(PASS R1, PASS R2, same claim_digest) -> overall PASS",
       result_both_pass["overall_status"] == "PASS", result_both_pass)

_fail_r2 = eu.route_result_fail("R2", DIGEST_A, DIGEST_B, [{"locus": "x=1"}])  # same claim_digest as R1
result_pass_fail = eu.evidence_union_fail_closed_v2(_pass_r1, _fail_r2)
record("evidence_union_fail_closed_v2(PASS R1, FAIL R2, same claim) -> overall CONFLICT",
       result_pass_fail["overall_status"] == "CONFLICT", result_pass_fail)

_malformed_r2 = eu.route_result_malformed("R2", ["bad shape"])
result_malformed = eu.evidence_union_fail_closed_v2(_malformed_r2, _pass_r1)
record("evidence_union_fail_closed_v2(MALFORMED R2, PASS R1) -> overall INTEGRITY_STOP",
       result_malformed["overall_status"] == "INTEGRITY_STOP", result_malformed)

result_absent_absent = eu.evidence_union_fail_closed_v2(None, {"route_status": "ABSENT", "missing_mask": {"x": True}})
record("evidence_union_fail_closed_v2(None, ABSENT) -> overall ABSENT",
       result_absent_absent["overall_status"] == "ABSENT", result_absent_absent)

result_absent_pass = eu.evidence_union_fail_closed_v2(None, _pass_r1)
record("evidence_union_fail_closed_v2(None, PASS) -> overall PASS",
       result_absent_pass["overall_status"] == "PASS", result_absent_pass)

# foreign/malicious input directly at the top level -> MALFORMED -> INTEGRITY_STOP.
result_garbage = eu.evidence_union_fail_closed_v2("garbage", _pass_r1)
record("evidence_union_fail_closed_v2('garbage', PASS) -> overall INTEGRITY_STOP (non-object is MALFORMED, not ABSENT)",
       result_garbage["overall_status"] == "INTEGRITY_STOP", result_garbage)


# --------------------------------------------------------------------------
# 5. route_from_verifier_b_w6 -- armature smoke test against REAL
#    verify_W6_single(...) output, now producing genuine RouteResult
#    objects (裁定192, not the old ad hoc blob).
# --------------------------------------------------------------------------
_cert_pos_01 = load_fixture("cert_pos_01.json")
w6_status_real, w6_detail_real = verb.verify_W6_single(
    _cert_pos_01["certificate"], _cert_pos_01["native_a"], _cert_pos_01["native_b"],
)
record("smoke: real cert_pos_01.json verify_W6_single -> PASS (sanity, unaffected by this file)",
       w6_status_real == "PASS", f"got {w6_status_real!r}: {w6_detail_real}")

route_from_real_w6 = eu.route_from_verifier_b_w6(w6_status_real, w6_detail_real, "R1")
record("route_from_verifier_b_w6(real PASS result, 'R1') -> is a well-formed RouteResult (route_status=PASS, route_id=R1)",
       route_from_real_w6.get("route_status") == "PASS" and route_from_real_w6.get("route_id") == "R1",
       route_from_real_w6)
status_via_connector, digest_via_connector, detail_via_connector = eu.coerce_to_route_result(route_from_real_w6)
record("route_from_verifier_b_w6(real PASS result) -> coerce_to_route_result resolves to PASS (armature round-trip)",
       status_via_connector == "PASS", f"got {status_via_connector!r}: {detail_via_connector}")

_cert_neg_03 = load_fixture("cert_neg_03.json")
w6_status_fail, w6_detail_fail = verb.verify_W6_single(
    _cert_neg_03["certificate"], _cert_neg_03["native_a"], _cert_neg_03["native_b"],
)
record("smoke: cert_neg_03.json verify_W6_single -> FAIL (setup check)",
       w6_status_fail == "FAIL", f"got {w6_status_fail!r}: {w6_detail_fail}")
route_fail = eu.route_from_verifier_b_w6(w6_status_fail, w6_detail_fail, "R2")
record("route_from_verifier_b_w6(real FAIL result, 'R2') -> route_status=FAIL, route_id=R2",
       route_fail.get("route_status") == "FAIL" and route_fail.get("route_id") == "R2", route_fail)
status_fail_via_connector, _, _ = eu.coerce_to_route_result(route_fail)
record("route_from_verifier_b_w6(real FAIL result) -> coerce_to_route_result resolves to FAIL (armature round-trip)",
       status_fail_via_connector == "FAIL", f"got {status_fail_via_connector!r}")

route_absent = eu.route_from_verifier_b_w6("ABSENT", {"reason": "not supplied"}, "R1")
status_absent_via_connector, _, _ = eu.coerce_to_route_result(route_absent)
record("route_from_verifier_b_w6('ABSENT', ...) -> coerce_to_route_result resolves to ABSENT (armature round-trip)",
       status_absent_via_connector == "ABSENT", f"got {status_absent_via_connector!r}")

route_malformed = eu.route_from_verifier_b_w6("MALFORMED", {"reason": "schema violation"}, "R2")
status_malformed_via_connector, _, _ = eu.coerce_to_route_result(route_malformed)
record("route_from_verifier_b_w6('MALFORMED', ...) -> coerce_to_route_result resolves to MALFORMED (armature round-trip)",
       status_malformed_via_connector == "MALFORMED", f"got {status_malformed_via_connector!r}")

# end-to-end: compose the REAL PASS route (as "R1") against a synthetic
# agreeing "R2" built the same way -- confirms the connector's output is
# genuinely usable as one side of evidence_union_fail_closed_v2.
r2_agreeing = eu.route_from_verifier_b_w6(w6_status_real, w6_detail_real, "R2")  # same underlying evidence -> same claim_digest
combined = eu.evidence_union_fail_closed_v2(route_from_real_w6, r2_agreeing)
record("evidence_union_fail_closed_v2(real-W6-PASS-via-connector R1, agreeing R2) -> overall PASS",
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
