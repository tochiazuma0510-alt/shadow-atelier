#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_evidence_union.py

Self-made test suite for search/ninfty-evidence-union.py (追補(o) v5/v6,
RouteResult two-layer per 裁定192 N83-2.3 -> sol/裁定_192_便83検収.md,
sol/sol_reply_83_math10.md F83-2.1/2.2/2.3; nominal gate hardened per Sol
便84 F84-5.4/P84-5 -> sol/sol_reply_84_math11.md; trust-boundary hardened
per Sol 便85 F85-6.3 B85-o1..o4/P85-5 -> sol/sol_reply_85_math12.md; public
facade / R2 independence / native dereference hardened per Sol 便86
F86-1.4 B86-o1..o3/P86-2 -> sol/sol_reply_86_math13.md).

Sections 1-7 exercise the pre-existing (便85) surface, with names updated
to match 便86's public-facade renames (compose_route_statuses ->
_compose_route_statuses, coerce_to_route_result -> _coerce_to_route_result,
evidence_union_fail_closed_v2 -> _evidence_union_fail_closed_v2,
route_from_verifier_b_w6 -> _route_from_verifier_result) and to the new
required implementation_id/source_digest fields on every PASS/FAIL
RouteResult. New sections:

  8. Sol 便86 P86-2 item 1 (B86-o1) -- public-facade one-ification:
     __all__ == ("evidence_union_from_raw_w6",) and a structural grep that
     no OTHER production file under search/ references this module's
     low-level (underscore) names. Calling this module's own private API
     directly from THIS test file (as sections 1-7 do throughout) is the
     normal Python convention for testing internals and is explicitly NOT
     what B86-o1 closes -- what it closes is a PRODUCTION caller doing so.
  9. Sol 便86 P86-2 item 2/5 (B86-o2) -- R2 independence: R2 is now built
     from search/ninfty-verifier-w6-r2.py's verify_W6_single_r2, a
     separately-written implementation sharing no helper code with R1's
     ninfty-verifier-b.py; both routes record distinct implementation_id/
     source_digest; _require_distinct_implementations is exercised
     directly (regression guard: if R1/R2 are ever re-wired onto the same
     implementation, the union fails closed instead of silently PASSing).
  10. Sol 便86 P86-2 item 3/4 (B86-o3) -- native dereference: a positive
      control (map_ref resolved via json_pointer into the real native
      artifact, no inline at all) plus THREE new negatives: valid-shape
      forged RouteResult fed directly to the public facade,
      matching-but-forged inline maps that disagree with the real native
      artifact, and native_a/native_b swapped at the runner-argument
      level.
  11. Sol 便86 P86-2 NOTE -- CLI exit code: `python
      search/ninfty-evidence-union.py <raw.json>` exits 0 iff
      overall_status == PASS, nonzero otherwise (previously always 0).

Run: python search/test_ninfty_evidence_union.py
Exits 0 iff all checks PASS; prints a PASS/FAIL table and returns nonzero
on any failure.
"""
import importlib.util
import inspect
import json
import os
import subprocess
import sys
import tempfile

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
r2mod = _load_module("ninfty_verifier_w6_r2_for_eu_test", "ninfty-verifier-w6-r2.py")

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

# Sol 便86 P86-2 item 2: every PASS/FAIL RouteResult now REQUIRES
# implementation_id (non-empty str) / source_digest (exact 64-hex). These
# test-only constants stand in for a real verifier's self-report in the
# white-box constructor/coercion tests (sections 1-7); sections 9-11 use
# the REAL IMPLEMENTATION_ID_R1/R2 and file digests instead.
IMPL_ID = "test-fixture-impl"
SRC_DIGEST = "9" * 64
IMPL_ID_2 = "test-fixture-impl-2"
SRC_DIGEST_2 = "8" * 64


# --------------------------------------------------------------------------
# 1. compose_route_statuses (now _compose_route_statuses) -- FULL 16-pair
#    table + swap symmetry + digest negatives + F83-2.2 low-level
#    digest-format defense. (Unaffected by the 便85/便86 trust-boundary
#    repairs -- the 4-rule structure is unchanged, only the name is now
#    private.)
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
record("_compose_route_statuses table: BASE_TABLE covers all 16 status pairs",
       len(BASE_TABLE) == 16, f"{len(BASE_TABLE)} entries")

for (s1, s2), expected in BASE_TABLE.items():
    d1 = DIGEST_MATCH if s1 in (P, F) else None
    d2 = DIGEST_MATCH if s2 in (P, F) else None
    got = eu._compose_route_statuses(s1, d1, s2, d2)
    record(f"_compose_route_statuses({s1!r}, {s2!r}) == {expected!r} (16-pair table)",
           got == expected, f"got {got!r}")

for (s1, s2) in BASE_TABLE.keys():
    d1 = DIGEST_MATCH if s1 in (P, F) else None
    d2 = DIGEST_MATCH if s2 in (P, F) else None
    forward = eu._compose_route_statuses(s1, d1, s2, d2)
    backward = eu._compose_route_statuses(s2, d2, s1, d1)
    record(f"_compose_route_statuses swap symmetry: ({s1!r},{s2!r}) == swap({s2!r},{s1!r})",
           forward == backward, f"forward={forward!r} backward={backward!r}")

DIGEST_OTHER = "e" * 64
for (s1, s2, label) in [(P, P, "PASS/PASS"), (F, F, "FAIL/FAIL"), (P, F, "PASS/FAIL"), (F, P, "FAIL/PASS")]:
    got = eu._compose_route_statuses(s1, DIGEST_MATCH, s2, DIGEST_OTHER)
    record(f"_compose_route_statuses digest-mismatch ({label}) -> CONFLICT (rule 2, before status composition)",
           got == "CONFLICT", f"got {got!r}")

_low_level_probe = eu._compose_route_statuses("PASS", None, "PASS", None)
record("裁定192 F83-2.2: _compose_route_statuses(PASS, None, PASS, None) -> INTEGRITY_STOP (was PASS)",
       _low_level_probe == "INTEGRITY_STOP", f"got {_low_level_probe!r}")
_low_level_probe2 = eu._compose_route_statuses("FAIL", "not-64-hex", "FAIL", "not-64-hex")
record("裁定192 F83-2.2: _compose_route_statuses(FAIL, <non-hex>, FAIL, <non-hex>) -> INTEGRITY_STOP",
       _low_level_probe2 == "INTEGRITY_STOP", f"got {_low_level_probe2!r}")


# --------------------------------------------------------------------------
# 2. RouteResult constructors (module-private, Sol 便85 P85-5 item 7) --
#    valid construction + F83-2.1 invariants + B85-o2 required-refs
#    invariant + NEW Sol 便86 P86-2 item 2 required implementation_id/
#    source_digest invariant, all enforced by the constructor itself.
# --------------------------------------------------------------------------

_good_pass = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
record("_route_result_pass: valid construction -> route_status=PASS", _good_pass.get("route_status") == "PASS", _good_pass)
record("_route_result_pass: route_id preserved", _good_pass.get("route_id") == "R1", _good_pass)
record("_route_result_pass: schema_id present", isinstance(_good_pass.get("schema_id"), str) and len(_good_pass["schema_id"]) > 0, _good_pass)
record("Sol 便86 P86-2 item 2: _route_result_pass valid construction carries implementation_id/source_digest",
       _good_pass.get("implementation_id") == IMPL_ID and _good_pass.get("source_digest") == SRC_DIGEST, _good_pass)

# F83-2.1: count mismatch -> constructor refuses PASS, falls back to MALFORMED.
_bad_pass_count = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=0,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
record("_route_result_pass: expected_domain_count != checked_domain_count -> constructor refuses, route_status=MALFORMED (F83-2.1)",
       _bad_pass_count.get("route_status") == "MALFORMED", _bad_pass_count)

# F83-2.1/N82-4.1: expected digest != coverage digest -> constructor refuses.
_bad_pass_digest = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest="f" * 64,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
record("_route_result_pass: expected_domain_digest != coverage_digest -> constructor refuses, route_status=MALFORMED",
       _bad_pass_digest.get("route_status") == "MALFORMED", _bad_pass_digest)

# ill-typed digest -> MALFORMED.
_bad_pass_digest_type = eu._route_result_pass(
    "R1", "not-hex", DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
record("_route_result_pass: claim_digest not 64-hex -> constructor refuses, route_status=MALFORMED",
       _bad_pass_digest_type.get("route_status") == "MALFORMED", _bad_pass_digest_type)

# Sol 便85 B85-o2: claim_source_ref/evidence_refs are now REQUIRED (no
# default None) -- omitting/nulling them must refuse construction.
_bad_pass_no_refs = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=None, evidence_refs=None,
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
record("Sol 便85 B85-o2: _route_result_pass with claim_source_ref=None/evidence_refs=None -> constructor refuses, route_status=MALFORMED",
       _bad_pass_no_refs.get("route_status") == "MALFORMED", _bad_pass_no_refs)
_bad_pass_illshaped_refs = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref={"source": "x"}, evidence_refs=[],
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
record("Sol 便85 B85-o2: _route_result_pass with ill-shaped claim_source_ref (missing digest) / empty evidence_refs -> MALFORMED",
       _bad_pass_illshaped_refs.get("route_status") == "MALFORMED", _bad_pass_illshaped_refs)

# Sol 便86 P86-2 item 2: implementation_id/source_digest are now REQUIRED
# too -- empty/ill-typed values must refuse construction.
_bad_pass_no_impl = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
    implementation_id="", source_digest=SRC_DIGEST,
)
record("Sol 便86 P86-2 item 2: _route_result_pass with implementation_id='' -> constructor refuses, route_status=MALFORMED",
       _bad_pass_no_impl.get("route_status") == "MALFORMED", _bad_pass_no_impl)
_bad_pass_bad_src_digest = eu._route_result_pass(
    "R1", DIGEST_A, DIGEST_B, expected_domain_count=3, checked_domain_count=3,
    expected_domain_digest=DIGEST_C, coverage_digest=DIGEST_C,
    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
    implementation_id=IMPL_ID, source_digest="not-hex",
)
record("Sol 便86 P86-2 item 2: _route_result_pass with source_digest='not-hex' -> constructor refuses, route_status=MALFORMED",
       _bad_pass_bad_src_digest.get("route_status") == "MALFORMED", _bad_pass_bad_src_digest)

_good_fail = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[{"locus": "x=1"}],
                                    claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                    implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
record("_route_result_fail: valid construction -> route_status=FAIL", _good_fail.get("route_status") == "FAIL", _good_fail)
record("Sol 便86 P86-2 item 2: _route_result_fail valid construction carries implementation_id/source_digest",
       _good_fail.get("implementation_id") == IMPL_ID and _good_fail.get("source_digest") == SRC_DIGEST, _good_fail)

_bad_fail_empty_loci = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[],
                                              claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                              implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
record("_route_result_fail: empty counterexample_loci -> constructor refuses, route_status=MALFORMED (F83-2.1)",
       _bad_fail_empty_loci.get("route_status") == "MALFORMED", _bad_fail_empty_loci)

_bad_fail_digest = eu._route_result_fail("R2", None, DIGEST_B, counterexample_loci=[{"locus": "x=1"}],
                                          claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                          implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
record("_route_result_fail: claim_digest missing -> constructor refuses, route_status=MALFORMED",
       _bad_fail_digest.get("route_status") == "MALFORMED", _bad_fail_digest)

_bad_fail_no_refs = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[{"locus": "x=1"}],
                                           claim_source_ref=None, evidence_refs=None,
                                           implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
record("Sol 便85 B85-o2: _route_result_fail with claim_source_ref=None/evidence_refs=None -> constructor refuses, route_status=MALFORMED",
       _bad_fail_no_refs.get("route_status") == "MALFORMED", _bad_fail_no_refs)

_bad_fail_no_impl = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, counterexample_loci=[{"locus": "x=1"}],
                                           claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                           implementation_id=None, source_digest=SRC_DIGEST)
record("Sol 便86 P86-2 item 2: _route_result_fail with implementation_id=None -> constructor refuses, route_status=MALFORMED",
       _bad_fail_no_impl.get("route_status") == "MALFORMED", _bad_fail_no_impl)

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
# 3. _coerce_to_route_result -- None->ABSENT; any OTHER non-object->MALFORMED
#    (returned status explicitly asserted, 便83 ★4); unrecognized
#    route_status; foreign status-shape co-presence (LITERAL Sol probe);
#    B85-o2 refs=None probe; NEW Sol 便86 P86-2 item 2 implementation_id/
#    source_digest-missing probe.
# --------------------------------------------------------------------------

status, digest, detail = eu._coerce_to_route_result(None)
record("_coerce_to_route_result(None) -> ABSENT", status == "ABSENT", f"got ({status!r}, {digest!r}, {detail})")

for label, val in [("string 'garbage'", "garbage"), ("empty list []", []), ("empty dict {} (no route_status at all)", {}),
                   ("integer 0", 0), ("boolean True", True)]:
    status, digest, detail = eu._coerce_to_route_result(val)
    record(f"裁定192 F83-2.2: _coerce_to_route_result({label}) -> MALFORMED exactly (returned status asserted, not just 'no crash')",
           status == "MALFORMED", f"got status={status!r}: {detail}")

status, digest, detail = eu._coerce_to_route_result({"route_status": "BOGUS"})
record("_coerce_to_route_result(unrecognized route_status) -> MALFORMED", status == "MALFORMED", f"got {status!r}: {detail}")

# LITERAL Sol probe (F83-2.2): a PASS-shaped result ALSO carrying
# counterexample_loci (a FAIL-only field) -- must be MALFORMED regardless
# of which field set "looks more complete"; and removing counterexample_loci
# entirely still leaves a well-formed PASS (confirms the field itself, not
# some other defect, is what triggers MALFORMED).
_superset_route = dict(_good_pass)
_superset_route["counterexample_loci"] = [{"locus": "smuggled-in"}]
status, digest, detail = eu._coerce_to_route_result(_superset_route)
record("裁定192 F83-2.2 literal probe: PASS-shaped result ALSO carrying counterexample_loci -> MALFORMED "
       "(status-shape co-presence, never silently resolved to PASS)",
       status == "MALFORMED", f"got {status!r}: {detail}")

status, digest, detail = eu._coerce_to_route_result(_good_pass)
record("_coerce_to_route_result(well-formed PASS, no foreign fields) -> PASS (control for the probe above)",
       status == "PASS" and digest == DIGEST_A, f"got {status!r}: {detail}")

# same probe the other direction: FAIL-shaped result ALSO carrying a PASS-only field.
_fail_with_pass_field = dict(_good_fail)
_fail_with_pass_field["coverage_digest"] = DIGEST_C
status, digest, detail = eu._coerce_to_route_result(_fail_with_pass_field)
record("裁定192 F83-2.2: FAIL-shaped result ALSO carrying coverage_digest (PASS-only field) -> MALFORMED",
       status == "MALFORMED", f"got {status!r}: {detail}")

# ABSENT result also carrying a PASS-only field -> MALFORMED.
_absent_with_pass_field = dict(_good_absent)
_absent_with_pass_field["checked_domain_count"] = 5
status, digest, detail = eu._coerce_to_route_result(_absent_with_pass_field)
record("裁定192 F83-2.2: ABSENT-shaped result ALSO carrying checked_domain_count (PASS-only field) -> MALFORMED",
       status == "MALFORMED", f"got {status!r}: {detail}")

# Sol 便85 B85-o2 literal probe: a well-formed-looking PASS route with
# claim_source_ref/evidence_refs blanked to None -- must be MALFORMED, not
# silently accepted (this was PASS before the fix).
_probe_refs_none_pass = dict(_good_pass)
_probe_refs_none_pass["claim_source_ref"] = None
_probe_refs_none_pass["evidence_refs"] = None
status, digest, detail = eu._coerce_to_route_result(_probe_refs_none_pass, expected_route_id="R1")
record("Sol 便85 B85-o2 literal probe: _coerce_to_route_result(PASS route with claim_source_ref=None, "
       "evidence_refs=None) -> MALFORMED (was PASS pre-fix)",
       status == "MALFORMED", f"got {status!r}: {detail}")

# Sol 便86 P86-2 item 2 literal probe: a well-formed-looking PASS route
# with implementation_id/source_digest blanked to None -- must be
# MALFORMED (this field did not exist pre-便86, so there is no "was PASS"
# regression baseline -- this documents the NEW invariant).
_probe_impl_none_pass = dict(_good_pass)
_probe_impl_none_pass["implementation_id"] = None
_probe_impl_none_pass["source_digest"] = None
status, digest, detail = eu._coerce_to_route_result(_probe_impl_none_pass, expected_route_id="R1")
record("Sol 便86 P86-2 item 2 literal probe: _coerce_to_route_result(PASS route with implementation_id=None, "
       "source_digest=None) -> MALFORMED",
       status == "MALFORMED", f"got {status!r}: {detail}")

# constructors' own output round-trips cleanly through _coerce_to_route_result.
for label, built, expected_status in [
    ("_route_result_pass", _good_pass, "PASS"),
    ("_route_result_fail", _good_fail, "FAIL"),
    ("_route_result_absent", _good_absent, "ABSENT"),
    ("_route_result_malformed", _good_malformed, "MALFORMED"),
]:
    status, digest, detail = eu._coerce_to_route_result(built)
    record(f"_coerce_to_route_result({label} output) -> {expected_status} (round-trip)",
           status == expected_status, f"got {status!r}: {detail}")


# --------------------------------------------------------------------------
# 4. _evidence_union_fail_closed_v2 -- end-to-end, built via constructors
#    (white-box composition-plumbing test; NOT the public trust boundary,
#    see section 7b for that).
# --------------------------------------------------------------------------
_pass_r1 = eu._route_result_pass("R1", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                  claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                  implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
_pass_r2_agree = eu._route_result_pass("R2", DIGEST_A, "f" * 64, 3, 3, DIGEST_C, DIGEST_C,
                                        claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                        implementation_id=IMPL_ID_2, source_digest=SRC_DIGEST_2)  # same claim_digest, DIFFERENT implementation
result_both_pass = eu._evidence_union_fail_closed_v2(_pass_r1, _pass_r2_agree)
record("_evidence_union_fail_closed_v2(PASS R1, PASS R2, same claim_digest) -> overall PASS",
       result_both_pass["overall_status"] == "PASS", result_both_pass)

_fail_r2 = eu._route_result_fail("R2", DIGEST_A, DIGEST_B, [{"locus": "x=1"}],
                                  claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                  implementation_id=IMPL_ID_2, source_digest=SRC_DIGEST_2)  # same claim_digest as R1
result_pass_fail = eu._evidence_union_fail_closed_v2(_pass_r1, _fail_r2)
record("_evidence_union_fail_closed_v2(PASS R1, FAIL R2, same claim) -> overall CONFLICT",
       result_pass_fail["overall_status"] == "CONFLICT", result_pass_fail)

_malformed_r2 = eu._route_result_malformed("R2", ["bad shape"])
result_malformed = eu._evidence_union_fail_closed_v2(_malformed_r2, _pass_r1)
record("_evidence_union_fail_closed_v2(MALFORMED R2, PASS R1) -> overall INTEGRITY_STOP",
       result_malformed["overall_status"] == "INTEGRITY_STOP", result_malformed)

_absent_r2 = eu._route_result_absent("R2", {"x": True})
result_absent_absent = eu._evidence_union_fail_closed_v2(None, _absent_r2)
record("_evidence_union_fail_closed_v2(None, ABSENT[R2]) -> overall ABSENT",
       result_absent_absent["overall_status"] == "ABSENT", result_absent_absent)

_pass_r2_solo = eu._route_result_pass("R2", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                       claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                       implementation_id=IMPL_ID_2, source_digest=SRC_DIGEST_2)
result_absent_pass = eu._evidence_union_fail_closed_v2(None, _pass_r2_solo)
record("_evidence_union_fail_closed_v2(None, PASS[R2]) -> overall PASS",
       result_absent_pass["overall_status"] == "PASS", result_absent_pass)

# foreign/malicious input directly at the top level -> MALFORMED -> INTEGRITY_STOP.
result_garbage = eu._evidence_union_fail_closed_v2("garbage", _pass_r1)
record("_evidence_union_fail_closed_v2('garbage', PASS) -> overall INTEGRITY_STOP (non-object is MALFORMED, not ABSENT)",
       result_garbage["overall_status"] == "INTEGRITY_STOP", result_garbage)


# --------------------------------------------------------------------------
# 5. _route_from_verifier_result -- armature smoke test against REAL
#    verify_W6_single(...) output. Sol 便86 change: renamed from
#    route_from_verifier_b_w6 and generalized (implementation_id/
#    source_digest are now explicit parameters, since this adapter is
#    shared by both R1 and R2).
# --------------------------------------------------------------------------
_cert_pos_01 = load_fixture("cert_pos_01.json")
w6_status_real, w6_detail_real = verb.verify_W6_single(
    _cert_pos_01["certificate"], _cert_pos_01["native_a"], _cert_pos_01["native_b"],
)
record("smoke: real cert_pos_01.json verify_W6_single -> PASS (sanity, unaffected by this file)",
       w6_status_real == "PASS", f"got {w6_status_real!r}: {w6_detail_real}")

route_from_real_w6 = eu._route_from_verifier_result(w6_status_real, w6_detail_real, "R1", _cert_pos_01, IMPL_ID, SRC_DIGEST)
record("_route_from_verifier_result(real PASS result, 'R1', raw, impl, src) -> is a well-formed RouteResult (route_status=PASS, route_id=R1)",
       route_from_real_w6.get("route_status") == "PASS" and route_from_real_w6.get("route_id") == "R1",
       route_from_real_w6)
status_via_connector, digest_via_connector, detail_via_connector = eu._coerce_to_route_result(route_from_real_w6)
record("_route_from_verifier_result(real PASS result) -> _coerce_to_route_result resolves to PASS (armature round-trip)",
       status_via_connector == "PASS", f"got {status_via_connector!r}: {detail_via_connector}")

# Sol 便85 B85-o4: PASS domain claim is now grounded in the real two-lane
# W-6 contract, not a hardcoded placeholder "1".
record("Sol 便85 B85-o4: _route_from_verifier_result PASS branch reports expected_domain_count==checked_domain_count==2 "
       "(the real W6_DOMAIN_LANES count, not the old hardcoded placeholder 1)",
       route_from_real_w6.get("expected_domain_count") == 2 and route_from_real_w6.get("checked_domain_count") == 2,
       route_from_real_w6)
record("Sol 便86 P86-2 item 2: _route_from_verifier_result threads implementation_id/source_digest onto the RouteResult",
       route_from_real_w6.get("implementation_id") == IMPL_ID and route_from_real_w6.get("source_digest") == SRC_DIGEST,
       route_from_real_w6)

_cert_neg_03 = load_fixture("cert_neg_03.json")
w6_status_fail, w6_detail_fail = verb.verify_W6_single(
    _cert_neg_03["certificate"], _cert_neg_03["native_a"], _cert_neg_03["native_b"],
)
record("smoke: cert_neg_03.json verify_W6_single -> FAIL (setup check)",
       w6_status_fail == "FAIL", f"got {w6_status_fail!r}: {w6_detail_fail}")
route_fail = eu._route_from_verifier_result(w6_status_fail, w6_detail_fail, "R2", _cert_neg_03, IMPL_ID_2, SRC_DIGEST_2)
record("_route_from_verifier_result(real FAIL result, 'R2', raw, impl, src) -> route_status=FAIL, route_id=R2",
       route_fail.get("route_status") == "FAIL" and route_fail.get("route_id") == "R2", route_fail)
status_fail_via_connector, _, _ = eu._coerce_to_route_result(route_fail)
record("_route_from_verifier_result(real FAIL result) -> _coerce_to_route_result resolves to FAIL (armature round-trip)",
       status_fail_via_connector == "FAIL", f"got {status_fail_via_connector!r}")

route_absent = eu._route_from_verifier_result("ABSENT", {"reason": "not supplied"}, "R1", {"note": "synthetic-absent-raw"}, IMPL_ID, SRC_DIGEST)
status_absent_via_connector, _, _ = eu._coerce_to_route_result(route_absent)
record("_route_from_verifier_result('ABSENT', ..., raw, impl, src) -> _coerce_to_route_result resolves to ABSENT (armature round-trip)",
       status_absent_via_connector == "ABSENT", f"got {status_absent_via_connector!r}")

route_malformed = eu._route_from_verifier_result("MALFORMED", {"reason": "schema violation"}, "R2", {"note": "synthetic-malformed-raw"}, IMPL_ID_2, SRC_DIGEST_2)
status_malformed_via_connector, _, _ = eu._coerce_to_route_result(route_malformed)
record("_route_from_verifier_result('MALFORMED', ..., raw, impl, src) -> _coerce_to_route_result resolves to MALFORMED (armature round-trip)",
       status_malformed_via_connector == "MALFORMED", f"got {status_malformed_via_connector!r}")

# end-to-end: compose the REAL PASS route (as "R1") against a synthetic
# agreeing "R2" built the same way, from the SAME raw -- confirms the
# connector's output is genuinely usable as one side of
# _evidence_union_fail_closed_v2.
r2_agreeing = eu._route_from_verifier_result(w6_status_real, w6_detail_real, "R2", _cert_pos_01, IMPL_ID_2, SRC_DIGEST_2)  # same underlying evidence -> same claim_digest, DIFFERENT implementation
combined = eu._evidence_union_fail_closed_v2(route_from_real_w6, r2_agreeing)
record("_evidence_union_fail_closed_v2(real-W6-PASS-via-connector R1, agreeing R2) -> overall PASS",
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
status, digest, detail = eu._coerce_to_route_result(_probe_no_schema_id, expected_route_id="R1")
record("P84-5.4 probe: {schema_id missing, route_id missing, route_status=PASS} -> MALFORMED (was PASS)",
       status == "MALFORMED", f"got {status!r}: {detail}")

# F84-5.4 literal probe 2: schema_id="evil/v9", route_id="producer-choice".
_probe_evil_schema = dict(_probe_no_schema_id, schema_id="evil/v9", route_id="producer-choice")
status, digest, detail = eu._coerce_to_route_result(_probe_evil_schema, expected_route_id="R1")
record('P84-5.4 probe: {schema_id="evil/v9", route_id="producer-choice"} -> MALFORMED (was PASS)',
       status == "MALFORMED", f"got {status!r}: {detail}")

# F84-5.4 literal probe 3: the union of the two forged routes above -- was
# overall PASS, must now be overall INTEGRITY_STOP (both sides MALFORMED).
result_forged_union = eu._evidence_union_fail_closed_v2(_probe_no_schema_id, _probe_evil_schema)
record("P84-5.4 probe: _evidence_union_fail_closed_v2(forged-no-schema_id, forged-evil-schema_id) -> "
       "overall INTEGRITY_STOP (was overall PASS)",
       result_forged_union["overall_status"] == "INTEGRITY_STOP", result_forged_union)

# F84-5.4 item 3: _route_result_pass("producer-choice", ...) itself must
# refuse (constructor-level enum), falling back to MALFORMED.
_producer_choice_pass = eu._route_result_pass("producer-choice", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                               claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                               implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
record('P84-5.4 item 3: _route_result_pass("producer-choice", ...) -> route_status=MALFORMED (constructor refuses)',
       _producer_choice_pass.get("route_status") == "MALFORMED", _producer_choice_pass)
_producer_choice_fail = eu._route_result_fail("also-not-r1-or-r2", DIGEST_A, DIGEST_B, [{"locus": "x=1"}],
                                               claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                               implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
record('P84-5.4 item 3: _route_result_fail("also-not-r1-or-r2", ...) -> route_status=MALFORMED (constructor refuses)',
       _producer_choice_fail.get("route_status") == "MALFORMED", _producer_choice_fail)
_producer_choice_absent = eu._route_result_absent("bogus-id", {"reason": "x"})
record('P84-5.4 item 3: _route_result_absent("bogus-id", ...) -> route_status=MALFORMED (constructor refuses)',
       _producer_choice_absent.get("route_status") == "MALFORMED", _producer_choice_absent)

# F84-5.4 item 2: top-level slot binding -- first argument must be
# route_id="R1", second must be "R2", even when BOTH routes are otherwise
# perfectly well-formed. Swapping them must not silently succeed.
_r1_route = eu._route_result_pass("R1", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                   claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                   implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
_r2_route = eu._route_result_pass("R2", DIGEST_A, DIGEST_B, 3, 3, DIGEST_C, DIGEST_C,
                                   claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                   implementation_id=IMPL_ID_2, source_digest=SRC_DIGEST_2)
status_wrong_slot, _, detail_wrong_slot = eu._coerce_to_route_result(_r2_route, expected_route_id="R1")
record("P84-5.4 item 2: a well-formed route_id='R2' route placed in the FIRST (R1) slot -> MALFORMED",
       status_wrong_slot == "MALFORMED", f"got {status_wrong_slot!r}: {detail_wrong_slot}")
result_swapped_slots = eu._evidence_union_fail_closed_v2(_r2_route, _r1_route)  # R2 first, R1 second -- swapped
record("P84-5.4 item 2: _evidence_union_fail_closed_v2(R2-route, R1-route) [swapped slots] -> overall INTEGRITY_STOP",
       result_swapped_slots["overall_status"] == "INTEGRITY_STOP", result_swapped_slots)
result_correct_slots = eu._evidence_union_fail_closed_v2(_r1_route, _r2_route)  # control: correct order
record("P84-5.4 item 2 control: _evidence_union_fail_closed_v2(R1-route, R2-route) [correct slots] -> overall PASS",
       result_correct_slots["overall_status"] == "PASS", result_correct_slots)

# F84-5.4 item 4: an unknown/foreign header field on an otherwise
# well-formed PASS route -- must be MALFORMED, not silently ignored.
_probe_unknown_field = dict(_r1_route)
_probe_unknown_field["evil_extra_field"] = "smuggled-in"
status, digest, detail = eu._coerce_to_route_result(_probe_unknown_field, expected_route_id="R1")
record('P84-5.4 item 4: well-formed PASS route ALSO carrying "evil_extra_field" -> MALFORMED',
       status == "MALFORMED", f"got {status!r}: {detail}")

# F84-5.4 item 5: _route_from_verifier_result now populates claim_source_ref/
# evidence_refs from the raw evidence (never left as None).
_w6_route_for_refs = eu._route_from_verifier_result(w6_status_real, w6_detail_real, "R1", _cert_pos_01, IMPL_ID, SRC_DIGEST)
record("P84-5.4 item 5: _route_from_verifier_result(...) populates claim_source_ref (not None)",
       _w6_route_for_refs.get("claim_source_ref") is not None, _w6_route_for_refs.get("claim_source_ref"))
record("P84-5.4 item 5: _route_from_verifier_result(...) populates evidence_refs (not None)",
       _w6_route_for_refs.get("evidence_refs") is not None, _w6_route_for_refs.get("evidence_refs"))


# --------------------------------------------------------------------------
# 7. Sol 便85 F85-6.3 B85-o1..o4 -- trust-boundary hardening. The THREE
#    literal probes from sol/sol_reply_85_math12.md F85-6.3 (valid-shape
#    forged PASS, refs=None, unknown w6_status), negativized and asserted
#    to the RETURNED status, PLUS the union path -- and end-to-end tests
#    of the public entry point evidence_union_from_raw_w6.
# --------------------------------------------------------------------------

h = DIGEST_A
_forged_ref = {"source": "forged-by-producer", "digest": h}
_probe_r1_valid_shape = eu._route_result_pass(
    "R1", h, h, 1, 1, h, h, claim_source_ref=_forged_ref, evidence_refs=[_forged_ref],
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
_probe_r2_valid_shape = eu._route_result_pass(
    "R2", h, h, 1, 1, h, h, claim_source_ref=_forged_ref, evidence_refs=[_forged_ref],
    implementation_id=IMPL_ID_2, source_digest=SRC_DIGEST_2,
)
record("Sol 便85 F85-6.3 probe (control): a valid-shape, self-asserted PASS RouteResult coerces to PASS at "
       "the LOW-LEVEL nominal gate in isolation -- documents that shape alone is NOT provenance; this is why "
       "the fix has to be architectural (no code path from a bare RouteResult dict to PASS at the PUBLIC "
       "trust boundary any more -- see the evidence_union_from_raw_w6 probes below)",
       eu._coerce_to_route_result(_probe_r1_valid_shape)[0] == "PASS", "n/a")
_probe_union_low_level = eu._evidence_union_fail_closed_v2(_probe_r1_valid_shape, _probe_r2_valid_shape)
record("Sol 便85 F85-6.3 probe (control): _evidence_union_fail_closed_v2(forged-but-valid-shape R1, R2) -> "
       "still overall PASS at the white-box combinator layer (EXPECTED -- this function only ever re-checks "
       "SHAPE; B85-o1's fix is that this layer is no longer reachable from untrusted input at all, see 7b; "
       "B86-o1 additionally moved this function itself behind a leading underscore, private-API-only)",
       _probe_union_low_level["overall_status"] == "PASS", _probe_union_low_level)

# B85-o2 literal probe: refs=None.
_probe_refs_none_direct = dict(_probe_r1_valid_shape)
_probe_refs_none_direct["claim_source_ref"] = None
_probe_refs_none_direct["evidence_refs"] = None
status_refs_none, _, detail_refs_none = eu._coerce_to_route_result(_probe_refs_none_direct, expected_route_id="R1")
record("Sol 便85 B85-o2 literal probe: r1.claim_source_ref=None, r1.evidence_refs=None -> coerce -> MALFORMED "
       "(was PASS pre-fix per F85-6.3's literal probe transcript)",
       status_refs_none == "MALFORMED", f"got {status_refs_none!r}: {detail_refs_none}")
_probe_union_refs_none = eu._evidence_union_fail_closed_v2(_probe_refs_none_direct, _probe_r2_valid_shape)
record("Sol 便85 B85-o2: _evidence_union_fail_closed_v2(refs=None R1, valid-shape R2) -> overall INTEGRITY_STOP "
       "(was overall PASS per F85-6.3's transcript: 'union(r1,r2) = PASS')",
       _probe_union_refs_none["overall_status"] == "INTEGRITY_STOP", _probe_union_refs_none)

# B85-o3 literal probe: unknown w6_status ("BOGUS") against the REAL adapter.
_forged_detail = {"reason": "forged BOGUS status probe (Sol 便85 F85-6.3 literal transcript)"}
route_bogus = eu._route_from_verifier_result("BOGUS", _forged_detail, "R2", {"note": "synthetic-bogus-probe-raw"}, IMPL_ID_2, SRC_DIGEST_2)
record('Sol 便85 B85-o3 literal probe: _route_from_verifier_result("BOGUS", forged_detail, "R2", raw, ...).route_status '
       '-> MALFORMED (was PASS pre-fix per F85-6.3\'s transcript: '
       '\'route_from_verifier_b_w6("BOGUS", forged_detail, "R2").route_status = PASS\')',
       route_bogus.get("route_status") == "MALFORMED", route_bogus)
status_bogus_via_coerce, _, _ = eu._coerce_to_route_result(route_bogus, expected_route_id="R2")
record("Sol 便85 B85-o3: _coerce_to_route_result(_route_from_verifier_result('BOGUS', ...)) -> MALFORMED",
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
       "actually invoked BOTH verifiers itself; both R1/R2 refs independently cross-checked against this raw, "
       "R1/R2 confirmed to come from genuinely distinct implementations)",
       result_from_raw_pos["overall_status"] == "PASS", result_from_raw_pos)
record("evidence_union_from_raw_w6(genuine raw evidence, cert_pos_01) -> route1/route2 implementation_id differ (R1=verifier-b, R2=verifier-w6-r2)",
       result_from_raw_pos["route1_detail"].get("implementation_id") == eu.IMPLEMENTATION_ID_R1
       and result_from_raw_pos["route2_detail"].get("implementation_id") == eu.IMPLEMENTATION_ID_R2
       and result_from_raw_pos["route1_detail"].get("implementation_id") != result_from_raw_pos["route2_detail"].get("implementation_id"),
       result_from_raw_pos)

_raw_neg_03 = {"schema_id": RAW_SCHEMA, "certificate": _cert_neg_03["certificate"],
               "native_a": _cert_neg_03["native_a"], "native_b": _cert_neg_03["native_b"]}
result_from_raw_neg = eu.evidence_union_from_raw_w6(_raw_neg_03)
record("evidence_union_from_raw_w6(genuine raw evidence, cert_neg_03) -> overall FAIL (real recomputed FAIL, both routes agree)",
       result_from_raw_neg["overall_status"] == "FAIL", result_from_raw_neg)

# B85-o1 architectural probe: feeding the OLD top-level {route1, route2}
# shape (a forged-but-valid-shape RouteResult pair) to the NEW public
# entry point must not be interpretable as raw evidence at all --
# schema_id mismatch -> both dispatch calls see a non-raw-evidence
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
# 8. Sol 便86 P86-2 item 1 (B86-o1) -- public-facade one-ification.
#    Structural checks: __all__ pins the ONLY public export to
#    evidence_union_from_raw_w6, and no OTHER production (non-test) file
#    in the repo references any of this module's low-level (underscore)
#    names. Sections 1-7 above call this module's private API directly --
#    that is THIS FILE testing its own project's internals, the normal
#    Python convention, NOT what B86-o1 closes (a production caller
#    reaching the low-level combinator from OUTSIDE this module/its test).
# --------------------------------------------------------------------------

record("Sol 便86 P86-2 item 1: eu.__all__ == ['evidence_union_from_raw_w6'] -- the ONLY public export",
       list(getattr(eu, "__all__", [])) == ["evidence_union_from_raw_w6"], getattr(eu, "__all__", None))

# Structural check: does ANY other file under search/ actually LOAD this
# module at all (the only way a caller could reach an attribute of it in
# the first place)? This codebase's own convention for loading a
# hyphenated-filename module (importlib.util.spec_from_file_location) is
# to quote the exact relative path string "ninfty-evidence-union.py" as
# the file argument -- exactly as THIS test file does at the top. A mere
# prose/docstring MENTION of the module's name (e.g. a sibling verifier's
# docstring explaining how it relates to ninfty-evidence-union.py) is not
# a load and is not what B86-o1 closes -- only a genuine dynamic-load call
# site is. (A naive substring/name grep for the private helper names
# themselves is unreliable here: names like "_verifier_b" collide with
# unrelated identifiers elsewhere in the codebase, e.g. ninfty-verifier-b.py's
# OWN unrelated "run_verifier_b" function -- so this check targets the
# LOAD SITE, the actual mechanism by which a caller could reach any
# attribute of this module, public or private.)
_LOAD_MARKER = '"ninfty-evidence-union.py"'
_EXEMPT_FILES = {"ninfty-evidence-union.py", "test_ninfty_evidence_union.py"}
_loaders_found = []
for fn in sorted(os.listdir(HERE)):
    full = os.path.join(HERE, fn)
    if not os.path.isfile(full) or fn in _EXEMPT_FILES or not fn.endswith((".py", ".mjs")):
        continue
    try:
        with open(full, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        continue
    if _LOAD_MARKER in content:
        _loaders_found.append(fn)
record("Sol 便86 P86-2 item 1: no OTHER file directly under search/ (excluding this test and the module "
       "itself) dynamically loads ninfty-evidence-union.py at all -- so no production caller can reach "
       "ANY attribute of it (public or private); evidence_union_from_raw_w6 (via THIS test's own load) is "
       "the only demonstrated reachable API",
       len(_loaders_found) == 0, _loaders_found)

# defense in depth: among files that WOULD load this module (there are
# none today, per the check above), a bare word-boundary reference to a
# low-level private name is still worth flagging as a future regression
# signal -- restricted to files that actually contain the load marker, so
# unrelated same-named identifiers elsewhere in the codebase (e.g.
# "run_verifier_b") can never trigger a false positive.
import re as _re_for_structural_check
_PRIVATE_LOW_LEVEL_NAMES = [
    "_route_result_pass", "_route_result_fail", "_route_result_absent", "_route_result_malformed",
    "_coerce_to_route_result", "_compose_route_statuses", "_evidence_union_fail_closed_v2",
    "_route_from_verifier_result", "_build_R1", "_build_R2", "_run_w6_verifier_r1", "_run_w6_verifier_r2",
    "_cross_check_refs_against_raw", "_require_distinct_implementations", "_verifier_b", "_verifier_r2",
    "_validate_raw_w6_evidence",
]
_offending = []
for fn in _loaders_found:
    with open(os.path.join(HERE, fn), "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    for name in _PRIVATE_LOW_LEVEL_NAMES:
        if _re_for_structural_check.search(r"(?<!\w)" + _re_for_structural_check.escape(name) + r"(?!\w)", content):
            _offending.append((fn, name))
record("Sol 便86 P86-2 item 1 defense in depth: among any (currently zero) OTHER files that DO load "
       "ninfty-evidence-union.py, none reference a low-level private name by whole-word match",
       len(_offending) == 0, _offending)

# a production-style caller that only imports the public name must still
# be able to do everything the public contract promises (positive control
# for the structural claim above -- __all__ is not merely decorative).
record("Sol 便86 P86-2 item 1 control: evidence_union_from_raw_w6 is reachable as eu.evidence_union_from_raw_w6 "
       "and usable with no other module attribute (the __all__ member itself works end to end)",
       callable(getattr(eu, eu.__all__[0], None)), eu.__all__)


# --------------------------------------------------------------------------
# 9. Sol 便86 P86-2 item 2/5 (B86-o2) -- R2 independence. R2 is now built
#    from a SEPARATELY WRITTEN implementation (search/ninfty-verifier-w6-r2.py)
#    sharing no helper code with R1's ninfty-verifier-b.py; both routes
#    record distinct implementation_id/source_digest;
#    _require_distinct_implementations is exercised directly as a
#    regression guard.
# --------------------------------------------------------------------------

# r2mod (ninfty-verifier-w6-r2.py) and verb (ninfty-verifier-b.py) agree on
# the underlying predicate for the same real fixtures (both are correct
# implementations of the SAME mathematical predicate) while being
# DIFFERENT code -- structural check below confirms no import coupling.
r2_status_pos, r2_detail_pos = r2mod.verify_W6_single_r2(
    _cert_pos_01["certificate"], _cert_pos_01["native_a"], _cert_pos_01["native_b"],
)
record("ninfty-verifier-w6-r2.verify_W6_single_r2(cert_pos_01) -> PASS, agrees with verifier-b's verify_W6_single",
       r2_status_pos == "PASS" == w6_status_real, f"got {r2_status_pos!r}: {r2_detail_pos}")
r2_status_neg, r2_detail_neg = r2mod.verify_W6_single_r2(
    _cert_neg_03["certificate"], _cert_neg_03["native_a"], _cert_neg_03["native_b"],
)
record("ninfty-verifier-w6-r2.verify_W6_single_r2(cert_neg_03) -> FAIL, agrees with verifier-b's verify_W6_single",
       r2_status_neg == "FAIL" == w6_status_fail, f"got {r2_status_neg!r}: {r2_detail_neg}")

# structural: ninfty-verifier-w6-r2.py contains NO actual import/dynamic-
# load coupling to ninfty-verifier-b.py -- only stdlib imports (hashlib,
# json, re, sys) and, separately, PROSE docstring mentions of
# "ninfty-verifier-b.py" explaining the design rationale (those are
# documentation, not code coupling, and are expected/desired). The
# structural fact that matters is: no `import` statement or
# importlib.util.spec_from_file_location call names ninfty-verifier-b at
# all -- checked by requiring every `import ...` line in the file to be a
# stdlib import, and that the literal load-marker pattern
# "ninfty-verifier-b.py" (quoted, as this codebase's own convention for a
# dynamic-load path argument -- see _verifier_b() in ninfty-evidence-union.py)
# never appears.
import ast as _ast_for_structural_check
_r2_source_path = os.path.join(HERE, "ninfty-verifier-w6-r2.py")
with open(_r2_source_path, "r", encoding="utf-8") as f:
    _r2_source_text = f.read()
_r2_ast = _ast_for_structural_check.parse(_r2_source_text)
_r2_imported_names = []
for node in _ast_for_structural_check.walk(_r2_ast):
    if isinstance(node, _ast_for_structural_check.Import):
        _r2_imported_names.extend(alias.name for alias in node.names)
    elif isinstance(node, _ast_for_structural_check.ImportFrom):
        _r2_imported_names.append(node.module)
_STDLIB_ONLY = {"__future__", "hashlib", "json", "re", "sys"}
record("Sol 便86 P86-2 item 2 structural check: ninfty-verifier-w6-r2.py's ONLY `import` statements are "
       "stdlib (hashlib/json/re/sys) -- no import of ninfty-verifier-b or anything else",
       set(_r2_imported_names) <= _STDLIB_ONLY, sorted(set(_r2_imported_names)))
record('Sol 便86 P86-2 item 2 structural check: ninfty-verifier-w6-r2.py never contains the quoted '
       'dynamic-load marker "ninfty-verifier-b.py" (this codebase\'s own convention for a load-path '
       'argument -- absence means no importlib.util dynamic load of verifier-b either)',
       '"ninfty-verifier-b.py"' not in _r2_source_text, '"ninfty-verifier-b.py"' in _r2_source_text)

# end-to-end via _build_R1/_build_R2: distinct implementation_id/source_digest.
_route1_built = eu._build_R1(_raw_pos_01)
_route2_built = eu._build_R2(_raw_pos_01)
record("Sol 便86 P86-2 item 2: _build_R1(raw).implementation_id == IMPLEMENTATION_ID_R1 (ninfty-verifier-b.py)",
       _route1_built.get("implementation_id") == eu.IMPLEMENTATION_ID_R1, _route1_built)
record("Sol 便86 P86-2 item 2: _build_R2(raw).implementation_id == IMPLEMENTATION_ID_R2 (ninfty-verifier-w6-r2.py)",
       _route2_built.get("implementation_id") == eu.IMPLEMENTATION_ID_R2, _route2_built)
record("Sol 便86 P86-2 item 2: _build_R1(raw).source_digest != _build_R2(raw).source_digest (different file bytes)",
       _route1_built.get("source_digest") != _route2_built.get("source_digest")
       and eu._is_64hex(_route1_built.get("source_digest")) and eu._is_64hex(_route2_built.get("source_digest")),
       (_route1_built.get("source_digest"), _route2_built.get("source_digest")))
record("Sol 便86 P86-2 item 2: _build_R1(raw).source_digest matches a fresh recomputation of ninfty-verifier-b.py's own bytes",
       _route1_built.get("source_digest") == eu._file_sha256(os.path.join(HERE, "ninfty-verifier-b.py")),
       _route1_built.get("source_digest"))
record("Sol 便86 P86-2 item 2: _build_R2(raw).source_digest matches a fresh recomputation of ninfty-verifier-w6-r2.py's own bytes",
       _route2_built.get("source_digest") == eu._file_sha256(os.path.join(HERE, "ninfty-verifier-w6-r2.py")),
       _route2_built.get("source_digest"))

# _require_distinct_implementations: control (genuinely distinct) passes through unchanged.
_ctrl1, _ctrl2 = eu._require_distinct_implementations(_route1_built, _route2_built)
record("Sol 便86 P86-2 item 5 control: _require_distinct_implementations(genuinely-distinct R1, R2) -> both unchanged (still PASS)",
       _ctrl1.get("route_status") == "PASS" and _ctrl2.get("route_status") == "PASS", (_ctrl1, _ctrl2))

# REGRESSION GUARD (the actual point of item 5): if R1 and R2 were ever
# re-wired onto the SAME implementation (B86-o2's original defect), this
# must be caught -- construct two otherwise-valid PASS routes sharing one
# implementation_id/source_digest and confirm the union fails closed.
_same_impl_r1 = eu._route_result_pass("R1", DIGEST_A, DIGEST_B, 1, 1, DIGEST_C, DIGEST_C,
                                       claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                       implementation_id=IMPL_ID, source_digest=SRC_DIGEST)
_same_impl_r2 = eu._route_result_pass("R2", DIGEST_A, DIGEST_B, 1, 1, DIGEST_C, DIGEST_C,
                                       claim_source_ref=REF_SRC, evidence_refs=REF_LIST,
                                       implementation_id=IMPL_ID, source_digest=SRC_DIGEST)  # SAME impl/src as R1
_downgraded1, _downgraded2 = eu._require_distinct_implementations(_same_impl_r1, _same_impl_r2)
record("Sol 便86 P86-2 item 5 REGRESSION GUARD: _require_distinct_implementations(R1, R2 sharing the SAME "
       "implementation_id/source_digest) -> BOTH downgraded to MALFORMED (this is exactly B86-o2's original "
       "defect reappearing -- must be caught structurally, not merely documented)",
       _downgraded1.get("route_status") == "MALFORMED" and _downgraded2.get("route_status") == "MALFORMED",
       (_downgraded1, _downgraded2))
_same_impl_union = eu._evidence_union_fail_closed_v2(_downgraded1, _downgraded2)
record("Sol 便86 P86-2 item 5: union of implementation-independence-violating routes -> overall INTEGRITY_STOP",
       _same_impl_union["overall_status"] == "INTEGRITY_STOP", _same_impl_union)


# --------------------------------------------------------------------------
# 10. Sol 便86 P86-2 item 3/4 (B86-o3) -- native dereference. A positive
#     control (map_ref resolved via json_pointer into the real native
#     artifact, NO inline at all) plus THREE new negatives.
# --------------------------------------------------------------------------


def _synthetic_native(map_list):
    return {
        "ramification_divisor_on_C_ref": {"note": "n/a for W-6-focused synthetic fixture"},
        "branch_divisor_on_P1_ref": {"note": "n/a for W-6-focused synthetic fixture"},
        "pushforward_map": map_list,
        "witness": {"note": "n/a for W-6-focused synthetic fixture"},
    }


_DUMMY_DIGEST = eu.sha256_of({"note": "n/a for W-6-focused synthetic fixture"})


def _dummy_side_refs(artifact_id):
    d = {"artifact_id": artifact_id, "digest": _DUMMY_DIGEST, "inline": {"note": "n/a for W-6-focused synthetic fixture"}}
    return {
        "ramification_ref": dict(d, json_pointer="/ramification_divisor_on_C_ref"),
        "branch_ref": dict(d, json_pointer="/branch_divisor_on_P1_ref"),
        "witness_ref": dict(d, json_pointer="/witness"),
    }


def _w6_entry(side, artifact_id, map_ref):
    d = _dummy_side_refs(artifact_id)
    return {"native_side": side, "ramification_ref": d["ramification_ref"], "branch_ref": d["branch_ref"],
            "map_ref": map_ref, "witness_ref": d["witness_ref"]}


def _synthetic_cert(searcher_map_ref, checker_map_ref):
    return {"pushforward_compatibility_witness": [
        _w6_entry("searcher", "native_a", searcher_map_ref),
        _w6_entry("checker", "native_b", checker_map_ref),
    ]}


REAL_MAP = [{"branch_value": "pt-1", "multiplicity": 1}, {"branch_value": "pt-2", "multiplicity": 3}]
REAL_MAP_DIGEST = eu.sha256_of(REAL_MAP)
_native_a_real = _synthetic_native(REAL_MAP)
_native_b_real = _synthetic_native(REAL_MAP)  # same map both sides -> legitimate PASS

# --- 10a. positive control: json_pointer resolves into the real native
#     artifact, NO inline at all on map_ref -- proves dereference itself
#     (not merely inline) drives the result.
_map_ref_a_deref_only = {"artifact_id": "native_a", "digest": REAL_MAP_DIGEST, "json_pointer": "/pushforward_map"}
_map_ref_b_deref_only = {"artifact_id": "native_b", "digest": REAL_MAP_DIGEST, "json_pointer": "/pushforward_map"}
_cert_deref_only = _synthetic_cert(_map_ref_a_deref_only, _map_ref_b_deref_only)
_deref_status, _deref_detail = verb.verify_W6_single(_cert_deref_only, _native_a_real, _native_b_real)
record("Sol 便86 P86-2 item 3 positive control: verify_W6_single with map_ref carrying json_pointer and NO "
       "inline at all -> PASS (real dereference into native_a/native_b, not merely an inline cache)",
       _deref_status == "PASS", f"got {_deref_status!r}: {_deref_detail}")

_raw_deref_only = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": _native_a_real, "native_b": _native_b_real}
_result_deref_only = eu.evidence_union_from_raw_w6(_raw_deref_only)
record("Sol 便86 P86-2 item 3 positive control (end-to-end): evidence_union_from_raw_w6(no-inline, "
       "json_pointer-only map_ref) -> overall PASS",
       _result_deref_only["overall_status"] == "PASS", _result_deref_only)

# --- 10b. NEW negative 1: valid-shape forged RouteResult fed DIRECTLY to
#     the public facade (not wrapped in the retired {route1,route2}
#     shape -- a single bare RouteResult object passed AS `raw` itself).
_bare_forged_route_as_raw = eu._route_result_pass(
    "R1", h, h, 1, 1, h, h, claim_source_ref=_forged_ref, evidence_refs=[_forged_ref],
    implementation_id=IMPL_ID, source_digest=SRC_DIGEST,
)
_result_bare_forged = eu.evidence_union_from_raw_w6(_bare_forged_route_as_raw)
record("Sol 便86 P86-2 item 4 NEW negative (valid-shape forged RouteResult via the public facade, passed "
       "DIRECTLY as `raw` with no wrapping at all): evidence_union_from_raw_w6(bare forged PASS RouteResult) "
       "-> overall INTEGRITY_STOP",
       _result_bare_forged["overall_status"] == "INTEGRITY_STOP", _result_bare_forged)

# --- 10c. NEW negative 2: matching forged inline maps that DISAGREE with
#     the real native artifact's content at the resolvable json_pointer.
#     Pre-B86-o3, inline was authoritative whenever present -- this would
#     have PASSed (both lanes self-consistently claim the same forged
#     map). Post-fix, the pointer resolves into the REAL native artifact
#     first, and the forged digest disagrees with the REAL content's
#     digest -> RefDigestMismatch -> MALFORMED.
FORGED_MAP = [{"branch_value": "pt-1", "multiplicity": 99}]
FORGED_DIGEST = eu.sha256_of(FORGED_MAP)
_map_ref_a_forged = {"artifact_id": "native_a", "digest": FORGED_DIGEST, "json_pointer": "/pushforward_map", "inline": FORGED_MAP}
_map_ref_b_forged = {"artifact_id": "native_b", "digest": FORGED_DIGEST, "json_pointer": "/pushforward_map", "inline": FORGED_MAP}
_cert_forged_inline = _synthetic_cert(_map_ref_a_forged, _map_ref_b_forged)
_forged_status, _forged_detail = verb.verify_W6_single(_cert_forged_inline, _native_a_real, _native_b_real)
record("Sol 便86 P86-2 item 4 NEW negative (matching forged inline maps): verify_W6_single with BOTH lanes "
       "carrying the SAME self-consistent forged inline map (would have PASSed pre-B86-o3) -> MALFORMED "
       "(the real native artifact's content at the resolvable json_pointer disagrees with the forged digest)",
       _forged_status == "MALFORMED", f"got {_forged_status!r}: {_forged_detail}")
_raw_forged_inline = {"schema_id": RAW_SCHEMA, "certificate": _cert_forged_inline, "native_a": _native_a_real, "native_b": _native_b_real}
_result_forged_inline = eu.evidence_union_from_raw_w6(_raw_forged_inline)
record("Sol 便86 P86-2 item 4 NEW negative (matching forged inline maps, end-to-end): "
       "evidence_union_from_raw_w6(...) -> overall INTEGRITY_STOP",
       _result_forged_inline["overall_status"] == "INTEGRITY_STOP", _result_forged_inline)

# --- 10d. NEW negative 3: native_a/native_b SWAPPED at the runner-argument
#     level. A legitimate certificate pins searcher's map to native_a's
#     TRUE content and checker's map to native_b's TRUE (genuinely
#     different) content; swapping which native artifact is passed as
#     native_a/native_b makes each side's json_pointer resolve to the
#     WRONG map, disagreeing with the digest the certificate pinned.
DIFFERENT_MAP = [{"branch_value": "pt-9", "multiplicity": 7}]
DIFFERENT_MAP_DIGEST = eu.sha256_of(DIFFERENT_MAP)
_native_b_different = _synthetic_native(DIFFERENT_MAP)
_map_ref_b_different = {"artifact_id": "native_b", "digest": DIFFERENT_MAP_DIGEST, "json_pointer": "/pushforward_map"}
_cert_two_real_maps = _synthetic_cert(_map_ref_a_deref_only, _map_ref_b_different)  # legit cert, two genuinely different maps

# control: correct (unswapped) assignment -> legitimate FAIL (real
# disagreement, not a schema violation) -- confirms dereference works
# correctly on a genuine mismatch before we test the swap.
_correct_status, _correct_detail = verb.verify_W6_single(_cert_two_real_maps, _native_a_real, _native_b_different)
record("Sol 便86 P86-2 item 4 NEW negative 3 control (unswapped): verify_W6_single(cert pinning two "
       "genuinely different real maps, native_a/native_b in the CORRECT slots) -> FAIL (legitimate "
       "disagreement, not a schema violation)",
       _correct_status == "FAIL", f"got {_correct_status!r}: {_correct_detail}")

# swapped: native_a/native_b arguments exchanged -- each side's
# json_pointer now resolves to the WRONG artifact's content.
_swapped_status, _swapped_detail = verb.verify_W6_single(_cert_two_real_maps, _native_b_different, _native_a_real)
record("Sol 便86 P86-2 item 4 NEW negative 3 (swapped native refs): verify_W6_single(SAME cert, native_a/"
       "native_b SWAPPED at the argument level) -> MALFORMED (each lane's json_pointer dereferences to "
       "content whose digest disagrees with what the certificate pinned)",
       _swapped_status == "MALFORMED", f"got {_swapped_status!r}: {_swapped_detail}")

_raw_swapped = {"schema_id": RAW_SCHEMA, "certificate": _cert_two_real_maps, "native_a": _native_b_different, "native_b": _native_a_real}
_result_swapped = eu.evidence_union_from_raw_w6(_raw_swapped)
record("Sol 便86 P86-2 item 4 NEW negative 3 (swapped native refs, end-to-end): evidence_union_from_raw_w6(...) "
       "-> overall INTEGRITY_STOP",
       _result_swapped["overall_status"] == "INTEGRITY_STOP", _result_swapped)

_raw_correct = {"schema_id": RAW_SCHEMA, "certificate": _cert_two_real_maps, "native_a": _native_a_real, "native_b": _native_b_different}
_result_correct = eu.evidence_union_from_raw_w6(_raw_correct)
record("Sol 便86 P86-2 item 4 NEW negative 3 control (unswapped, end-to-end): evidence_union_from_raw_w6(...) "
       "-> overall FAIL (both R1/R2 independently recompute the same legitimate mismatch)",
       _result_correct["overall_status"] == "FAIL", _result_correct)


# --------------------------------------------------------------------------
# 11. Sol 便86 P86-2 NOTE -- CLI exit code: nonzero for anything other than
#     overall_status="PASS" (previously always 0 regardless of status).
# --------------------------------------------------------------------------


def _run_cli(raw_obj):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(raw_obj, f)
        path = f.name
    try:
        proc = subprocess.run(
            [sys.executable, os.path.join(HERE, "ninfty-evidence-union.py"), path],
            capture_output=True, text=True, timeout=60,
        )
        return proc.returncode, proc.stdout, proc.stderr
    finally:
        os.unlink(path)


_cli_rc_pass, _cli_out_pass, _cli_err_pass = _run_cli(_raw_pos_01)
record("Sol 便86 P86-2 NOTE (CLI): `python ninfty-evidence-union.py <PASS raw>` -> exit code 0",
       _cli_rc_pass == 0, f"rc={_cli_rc_pass} stdout={_cli_out_pass!r} stderr={_cli_err_pass!r}")
record("Sol 便86 P86-2 NOTE (CLI) control: PASS run's stdout JSON has overall_status=PASS",
       json.loads(_cli_out_pass or "{}").get("overall_status") == "PASS", _cli_out_pass)

_cli_rc_fail, _cli_out_fail, _cli_err_fail = _run_cli(_raw_neg_03)
record("Sol 便86 P86-2 NOTE (CLI): `python ninfty-evidence-union.py <FAIL raw>` -> exit code NONZERO (was 0 pre-fix)",
       _cli_rc_fail != 0, f"rc={_cli_rc_fail} stdout={_cli_out_fail!r} stderr={_cli_err_fail!r}")

_cli_rc_forged, _cli_out_forged, _cli_err_forged = _run_cli(_raw_forged_inline)
record("Sol 便86 P86-2 NOTE (CLI): `python ninfty-evidence-union.py <matching-forged-inline-maps raw>` -> "
       "exit code NONZERO (INTEGRITY_STOP)",
       _cli_rc_forged != 0, f"rc={_cli_rc_forged} stdout={_cli_out_forged!r} stderr={_cli_err_forged!r}")


# --------------------------------------------------------------------------
# 12. Sol 便87 P87-1 item 1 (F87-1.2, sol/sol_reply_87_math14.md):
#     UNRESOLVED_POINTER_INLINE_ATTACK -- json_pointer PRESENT but
#     UNRESOLVABLE against the pinned native artifact, paired with a
#     self-digest-consistent FORGED inline that has NO counterpart in
#     native_a/native_b at all. Sol's exact probe (json_pointer=
#     "/definitely_missing", native_a=native_b={}) reached R1=R2=
#     overall=PASS pre-fix; the 481-negative suite only ever exercised
#     pointers that DO resolve, never this branch. Reproduced here through
#     R1 alone, R2 alone, and the end-to-end public facade.
# --------------------------------------------------------------------------

UPIA_FORGED_MAP = [{"branch_value": "sol-forged", "multiplicity": 87}]
UPIA_FORGED_DIGEST = eu.sha256_of(UPIA_FORGED_MAP)
_upia_map_ref_a = {"artifact_id": "native_a", "digest": UPIA_FORGED_DIGEST,
                    "json_pointer": "/definitely_missing", "inline": UPIA_FORGED_MAP}
_upia_map_ref_b = {"artifact_id": "native_b", "digest": UPIA_FORGED_DIGEST,
                    "json_pointer": "/definitely_missing", "inline": UPIA_FORGED_MAP}
_upia_cert = _synthetic_cert(_upia_map_ref_a, _upia_map_ref_b)
_upia_native_a = {}
_upia_native_b = {}

_upia_r1_status, _upia_r1_detail = verb.verify_W6_single(_upia_cert, _upia_native_a, _upia_native_b)
record("Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, R1 alone): "
       "verify_W6_single(json_pointer='/definitely_missing', native_a=native_b={}, self-consistent forged "
       "inline) -> MALFORMED (was PASS pre-fix -- Sol's exact probe)",
       _upia_r1_status == "MALFORMED", f"got {_upia_r1_status!r}: {_upia_r1_detail}")

_upia_r2_status, _upia_r2_detail = r2mod.verify_W6_single_r2(_upia_cert, _upia_native_a, _upia_native_b)
record("Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, R2 alone): "
       "verify_W6_single_r2(SAME probe) -> MALFORMED (was PASS pre-fix -- Sol's exact probe)",
       _upia_r2_status == "MALFORMED", f"got {_upia_r2_status!r}: {_upia_r2_detail}")

_upia_raw = {"schema_id": RAW_SCHEMA, "certificate": _upia_cert, "native_a": _upia_native_a, "native_b": _upia_native_b}
_upia_result = eu.evidence_union_from_raw_w6(_upia_raw)
record("Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, end-to-end public facade): "
       "evidence_union_from_raw_w6(SAME probe) -> overall INTEGRITY_STOP (was PASS/PASS/PASS pre-fix, "
       "sol/sol_reply_87_math14.md F87-1.2 literal reproduction)",
       _upia_result["overall_status"] == "INTEGRITY_STOP", _upia_result)

_upia_cli_rc, _upia_cli_out, _upia_cli_err = _run_cli(_upia_raw)
record("Sol 便87 P87-1 item 1 (F87-1.2 UNRESOLVED_POINTER_INLINE_ATTACK, CLI): "
       "`python ninfty-evidence-union.py <UPIA raw>` -> exit code NONZERO (was 0/PASS pre-fix)",
       _upia_cli_rc != 0, f"rc={_upia_cli_rc} stdout={_upia_cli_out!r} stderr={_upia_cli_err!r}")

# --- items 2-3: native_registry_status is an honest, non-gating UNKNOWN
#     declaration attached to every evidence_union_from_raw_w6 call -- no
#     receiver-held native-artifact registry exists in this codebase, so
#     this reports the gap instead of fabricating one (裁定232 P87-1).
record("Sol 便87 P87-1 items 2-3: evidence_union_from_raw_w6(genuine PASS raw).native_registry_status.status "
       "== 'UNKNOWN' (honest declaration, no registry implemented anywhere in this codebase, not fabricated)",
       result_from_raw_pos.get("native_registry_status", {}).get("status") == "UNKNOWN",
       result_from_raw_pos.get("native_registry_status"))
record("Sol 便87 P87-1 items 2-3 (present on every overall_status, not just PASS): "
       "evidence_union_from_raw_w6(UPIA attack raw).native_registry_status.status == 'UNKNOWN'",
       _upia_result.get("native_registry_status", {}).get("status") == "UNKNOWN",
       _upia_result.get("native_registry_status"))

# --- item 3 gap regression guard: artifact_id is NOT checked against any
#     pinned identity today (there is nothing implemented to check it
#     against) -- a map_ref whose artifact_id string matches neither
#     "native_a" nor "native_b" still dereferences successfully via
#     json_pointer against whichever native payload the caller positionally
#     supplied. This is exactly the gap native_registry_status declares
#     UNKNOWN above; the assertion below is a regression guard that this
#     gap stays honestly declared rather than silently assumed fixed by a
#     string comparison that was never added.
_mismatched_artifact_id_ref_a = dict(_map_ref_a_deref_only, artifact_id="totally-unrelated-label")
_mismatched_artifact_id_ref_b = dict(_map_ref_b_deref_only, artifact_id="also-unrelated-label")
_cert_mismatched_artifact_id = _synthetic_cert(_mismatched_artifact_id_ref_a, _mismatched_artifact_id_ref_b)
_mismatch_status, _mismatch_detail = verb.verify_W6_single(_cert_mismatched_artifact_id, _native_a_real, _native_b_real)
record("Sol 便87 P87-1 item 3 gap regression guard: verify_W6_single with map_ref.artifact_id matching NO "
       "pinned identity (none is implemented) still dereferences via json_pointer and reaches PASS -- this IS "
       "the exact gap native_registry_status declares UNKNOWN, not a silent claim that artifact_id is checked",
       _mismatch_status == "PASS", f"got {_mismatch_status!r}: {_mismatch_detail}")


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
