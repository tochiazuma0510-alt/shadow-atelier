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
# Sol 便88 P88-o: the receiver-held native-artifact registry -- THIS test
# file is the "receiver" doing out-of-band provisioning (prov.write_entry)
# ahead of building any `raw` evidence artifact; evidence-union.py itself
# never calls write_entry (only resolve), see ninfty-native-registry.py's
# own docstring. Sol 便90 F90-4.1 blocker 2 (docs/notes/
# cert_shape_interpretation_addendum_o_v10.md): resolve/index_exists and
# write_entry now live in TWO SEPARATE modules -- `reg` (resolver-only,
# the same module evidence-union.py itself loads) and `prov`
# (provisioning-only, loaded ONLY by this test file / a future operator
# CLI, never by evidence-union.py).
reg = _load_module("ninfty_native_registry_for_eu_test", "ninfty-native-registry.py")
prov = _load_module("ninfty_native_registry_provisioning_for_eu_test", "ninfty-native-registry-provisioning.py")

# Sol 便89 fix (test/production registry store separation, docs/notes/
# cert_shape_interpretation_addendum_o_v9.md): this test process's own
# registry store is a FRESH tempdir, wholly distinct from
# reg.PRODUCTION_REGISTRY_DIR (search/certs/ep_registry/). Every
# prov.write_entry(...) call in this file passes registry_dir=TEST_REGISTRY_DIR
# explicitly (write_entry has no default registry_dir any more -- a
# caller cannot forget). The NINFTY_EP_REGISTRY_DIR env var is set so that
# reg.resolve(...) -- including the copy of resolve() evidence-union.py's
# own _registry() dynamically loads and calls with NO dir parameter of its
# own -- also reads from this same tempdir, never from production, for the
# whole duration of this test run.
TEST_REGISTRY_DIR = tempfile.mkdtemp(prefix="ninfty_ep_registry_test_")
os.environ["NINFTY_EP_REGISTRY_DIR"] = TEST_REGISTRY_DIR

# Sol 便90 F90-4.1 blocker 5/8 (docs/notes/cert_shape_interpretation_
# addendum_o_v10.md): captured as early as possible (before this run does
# anything else at all) and compared, in section 15, against the SAME
# digest recomputed at the very end of this run -- a stronger replacement
# for v9's negative 14a, which only compared the sorted FILE-NAME list
# under PRODUCTION_REGISTRY_DIR (a same-named file with silently mutated
# bytes would not have been caught by that weaker check).
_PROD_SNAPSHOT_DIGEST_AT_START = reg.production_snapshot_digest(registry_dir=reg.PRODUCTION_REGISTRY_DIR)

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
record("evidence_union_from_raw_w6(genuine raw evidence, cert_pos_01) -> route-level PASS/PASS still reached "
       "(receiver-side dispatch actually invoked BOTH verifiers itself; both R1/R2 refs independently "
       "cross-checked against this raw, R1/R2 confirmed to come from genuinely distinct implementations)",
       result_from_raw_pos["route1_status"] == "PASS" and result_from_raw_pos["route2_status"] == "PASS",
       result_from_raw_pos)
record("Sol 便88 P88-o v8: evidence_union_from_raw_w6(cert_pos_01, NO native_registry_refs) -> overall "
       "INTEGRITY_STOP, not PASS -- cert_pos_01's map_ref uses the legacy object_id/inline path (裁定150 "
       "items 2/3), which never dereferences against a receiver-pinned registry artifact, so it can never "
       "satisfy native_registry_status=PASS (P88-o item 5(f)); this fixture legitimately reached overall "
       "PASS pre-v8 (追補(o) v7) precisely because native_registry_status was non-gating then -- see 10a "
       "below for the registry-backed positive control that now carries this role",
       result_from_raw_pos["overall_status"] == "INTEGRITY_STOP", result_from_raw_pos)
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

# Sol 便88 P88-o positive control: this IS the "properly-registered
# artifact still reaches PASS" demonstration (P88-o completion condition
# "正当な artifact では従来どおり PASS すること"). reg.write_entry is the
# receiver's OUT-OF-BAND provisioning step -- it never runs as part of
# processing a caller-supplied raw evidence artifact.
_REG_DIGEST_NATIVE_A = prov.write_entry("native_a", "native_a", "v1", _native_a_real, registry_dir=TEST_REGISTRY_DIR)["whole_artifact_digest"]
_REG_DIGEST_NATIVE_B = prov.write_entry("native_b", "native_b", "v1", _native_b_real, registry_dir=TEST_REGISTRY_DIR)["whole_artifact_digest"]
_registry_refs_deref_only = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1"},
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1"},
}
_raw_deref_only = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": _native_a_real, "native_b": _native_b_real,
                    "native_registry_refs": _registry_refs_deref_only}
_result_deref_only = eu.evidence_union_from_raw_w6(_raw_deref_only)
record("Sol 便86 P86-2 item 3 / Sol 便88 P88-o positive control (end-to-end): evidence_union_from_raw_w6(no-inline, "
       "json_pointer-only map_ref, PROPERLY REGISTERED native_registry_refs) -> overall PASS -- confirms EP "
       "operative PASS is actually reachable now that the registry is implemented, not just theoretically gated",
       _result_deref_only["overall_status"] == "PASS", _result_deref_only)
record("Sol 便88 P88-o positive control: native_registry_status.status == 'PASS' for a properly-registered artifact",
       _result_deref_only.get("native_registry_status", {}).get("status") == "PASS", _result_deref_only.get("native_registry_status"))

# Sol 便88 P88-o item 1 direct demonstration: raw's OWN top-level
# native_a/native_b are deliberately CORRUPTED here (garbage content that
# would fail dereference outright if it were ever consulted) -- ONLY
# native_registry_refs is left correct. Still overall PASS: this is the
# strongest possible proof that raw["native_a"]/raw["native_b"] are never
# read as authority once native_registry_refs resolves.
_raw_deref_only_raw_native_ignored = {
    "schema_id": RAW_SCHEMA, "certificate": _cert_deref_only,
    "native_a": {"deliberately": "corrupted -- must never be consulted"},
    "native_b": {"also": "corrupted -- must never be consulted"},
    "native_registry_refs": _registry_refs_deref_only,
}
_result_raw_native_ignored = eu.evidence_union_from_raw_w6(_raw_deref_only_raw_native_ignored)
record("Sol 便88 P88-o item 1 direct proof: evidence_union_from_raw_w6 with raw['native_a']/raw['native_b'] "
       "DELIBERATELY CORRUPTED (would fail dereference if ever consulted) but native_registry_refs correct "
       "-> STILL overall PASS -- raw's own native_a/native_b are never read as authority",
       _result_raw_native_ignored["overall_status"] == "PASS", _result_raw_native_ignored)

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
# Sol 便88 P88-o: a DISTINCT artifact_id ("native_b_alt") from 10a's
# already-registered "native_b" -- avoids overwriting 10a's registry
# entry (which 10a's own PASS assertions, and section 11's CLI PASS
# probe, both depend on) with different content under the same id.
_map_ref_b_different = {"artifact_id": "native_b_alt", "digest": DIFFERENT_MAP_DIGEST, "json_pointer": "/pushforward_map"}
_cert_two_real_maps = _synthetic_cert(_map_ref_a_deref_only, _map_ref_b_different)  # legit cert, two genuinely different maps
_REG_DIGEST_NATIVE_B_ALT = prov.write_entry("native_b_alt", "native_b", "v1", _native_b_different, registry_dir=TEST_REGISTRY_DIR)["whole_artifact_digest"]

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

_registry_refs_correct = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1"},
    "native_b": {"artifact_id": "native_b_alt", "whole_artifact_digest": _REG_DIGEST_NATIVE_B_ALT, "version_id": "v1"},
}
# Sol 便88 P88-o item 5(d) A/B swap: the registry REFS (not raw's inert
# top-level native_a/native_b) are what now carries the "which artifact
# backs which slot" claim -- swapping THEM is the v8-era equivalent of
# the old "runner-argument-level swap" this negative originally tested.
_registry_refs_swapped = {
    "native_a": {"artifact_id": "native_b_alt", "whole_artifact_digest": _REG_DIGEST_NATIVE_B_ALT, "version_id": "v1"},
    "native_b": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1"},
}
_raw_swapped = {"schema_id": RAW_SCHEMA, "certificate": _cert_two_real_maps, "native_a": _native_b_different, "native_b": _native_a_real,
                "native_registry_refs": _registry_refs_swapped}
_result_swapped = eu.evidence_union_from_raw_w6(_raw_swapped)
record("Sol 便86 P86-2 item 4 / Sol 便88 P88-o item 5(d) (swapped registry refs, end-to-end): "
       "evidence_union_from_raw_w6(...) -> overall INTEGRITY_STOP",
       _result_swapped["overall_status"] == "INTEGRITY_STOP", _result_swapped)
record("Sol 便88 P88-o item 5(d) A/B swap: native_registry_status.status == 'ROLE_MISMATCH' (the artifact "
       "registered with role 'native_b' was claimed for slot 'native_a', and vice versa)",
       _result_swapped.get("native_registry_status", {}).get("status") == "ROLE_MISMATCH",
       _result_swapped.get("native_registry_status"))

_raw_correct = {"schema_id": RAW_SCHEMA, "certificate": _cert_two_real_maps, "native_a": _native_a_real, "native_b": _native_b_different,
                 "native_registry_refs": _registry_refs_correct}
_result_correct = eu.evidence_union_from_raw_w6(_raw_correct)
record("Sol 便86 P86-2 item 4 control (unswapped, end-to-end, PROPERLY REGISTERED): evidence_union_from_raw_w6(...) "
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


# Sol 便88 P88-o v8: _raw_pos_01 no longer reaches overall PASS (legacy
# object_id path, see the section 7b update above) -- the CLI-exits-0 PASS
# demo now uses 10a's registry-backed _raw_deref_only instead.
_cli_rc_pass, _cli_out_pass, _cli_err_pass = _run_cli(_raw_deref_only)
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

# --- items 2-3, Sol 便88 P88-o v8 update: native_registry_status is now a
#     GATING, registry-backed status (not the old non-gating "UNKNOWN"
#     placeholder) attached to every evidence_union_from_raw_w6 call.
#     Neither cert_pos_01's raw (_raw_pos_01) nor the UPIA attack raw
#     ever declared native_registry_refs at all -- MISSING (a real
#     registry now exists, see 10a, but these two callers never even try
#     to use it), distinct from "artifact_id declared but not found in an
#     existing registry" (UNKNOWN, see new section 13(b) below).
record("Sol 便88 P88-o v8: evidence_union_from_raw_w6(cert_pos_01 raw, no native_registry_refs)."
       "native_registry_status.status == 'MISSING' (was the non-gating 'UNKNOWN' placeholder pre-v8)",
       result_from_raw_pos.get("native_registry_status", {}).get("status") == "MISSING",
       result_from_raw_pos.get("native_registry_status"))
record("Sol 便88 P88-o v8 (present on every overall_status, not just PASS): "
       "evidence_union_from_raw_w6(UPIA attack raw).native_registry_status.status == 'MISSING'",
       _upia_result.get("native_registry_status", {}).get("status") == "MISSING",
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
record("Sol 便87 P87-1 item 3 gap regression guard: ninfty-verifier-b.verify_W6_single (called DIRECTLY, "
       "bypassing the evidence-union facade entirely) with map_ref.artifact_id matching NO pinned identity "
       "still dereferences via json_pointer and reaches PASS -- verifier-b.py itself is UNCHANGED by Sol 便88 "
       "P88-o (the registry-vs-artifact_id cross-check now lives at the FACADE layer, "
       "_resolve_native_registry's ARTIFACT_ID_MISMATCH status, see section 13 below) -- this regression guard "
       "documents that the raw verifier function, in isolation, still does not and need not perform this check",
       _mismatch_status == "PASS", f"got {_mismatch_status!r}: {_mismatch_detail}")


# --------------------------------------------------------------------------
# 13. Sol 便88 P88-o (F88-3.2, sol/sol_reply_88_math15.md; 裁定239 §3):
#     the receiver-held native-artifact registry now GATES overall PASS.
#     (a) literal reproduction of Sol's full-replacement attack; (b)-(f)
#     the five further P88-o item 5 negatives, each isolated.
# --------------------------------------------------------------------------

# --- 13a. Sol 便88 F88-3.2 full-replacement attack, literal + strengthened.
#     Sol's four steps: (1) forge pushforward_map, (2) set both refs'
#     digests to match the forged map, (3) put the same forged map into
#     native_a/native_b, (4) artifact_id matches no pinned identity.
#     Pre-v8 this reached R1=R2=overall=PASS with native_registry_status
#     merely "UNKNOWN" (non-gating). Post-v8: native_a/native_b are never
#     read from raw at all (P88-o item 1), so steps (1)-(3) are moot by
#     construction; native_registry_refs (new, required for PASS) is
#     either absent (literal probe) or, in the strengthened variant,
#     forged too -- and still cannot reach PASS.
_SOL_FORGED_MAP = [{"branch_value": "sol-full-replacement", "multiplicity": 42}]
_sol_forged_digest = eu.sha256_of(_SOL_FORGED_MAP)
_sol_native_a = _synthetic_native(_SOL_FORGED_MAP)
_sol_native_b = _synthetic_native(_SOL_FORGED_MAP)
_sol_map_ref_a = {"artifact_id": "attacker-chosen-id-matching-nothing", "digest": _sol_forged_digest, "json_pointer": "/pushforward_map"}
_sol_map_ref_b = {"artifact_id": "attacker-chosen-id-matching-nothing", "digest": _sol_forged_digest, "json_pointer": "/pushforward_map"}
_sol_cert = _synthetic_cert(_sol_map_ref_a, _sol_map_ref_b)

# literal probe: exactly the old (v7) raw shape -- schema_id, certificate,
# native_a, native_b, all mutually self-consistent and forged. No
# native_registry_refs at all (this IS the shape Sol's probe used;
# native_registry_refs did not exist pre-v8).
_sol_raw_literal = {"schema_id": RAW_SCHEMA, "certificate": _sol_cert, "native_a": _sol_native_a, "native_b": _sol_native_b}
_sol_result_literal = eu.evidence_union_from_raw_w6(_sol_raw_literal)
record("P88-o negative (a) / Sol 便88 F88-3.2 full-replacement attack, LITERAL reproduction (forged cert + "
       "forged native_a + forged native_b, all self-consistent, artifact_id matching no pinned identity, "
       "exact v7-era raw shape with no native_registry_refs at all): evidence_union_from_raw_w6(...) -> "
       "overall != PASS (was PASS/PASS/PASS with native_registry_status=UNKNOWN pre-v8, sol_reply_88_math15.md F88-3.2)",
       _sol_result_literal["overall_status"] != "PASS", _sol_result_literal)
record("P88-o negative (a) literal probe: native_registry_status.status == 'MISSING' (no ref supplied at all)",
       _sol_result_literal.get("native_registry_status", {}).get("status") == "MISSING", _sol_result_literal.get("native_registry_status"))

# strengthened variant: attacker ALSO forges native_registry_refs,
# guessing the conventional artifact_id strings "native_a"/"native_b"
# (visible in this repo's own fixtures) and computing whole_artifact_digest
# from their OWN forged native_a/native_b content (the only content they
# have) -- they cannot know the receiver's actually-pinned content, so the
# claimed digest cannot match.
_sol_map_ref_a2 = {"artifact_id": "native_a", "digest": _sol_forged_digest, "json_pointer": "/pushforward_map"}
_sol_map_ref_b2 = {"artifact_id": "native_b", "digest": _sol_forged_digest, "json_pointer": "/pushforward_map"}
_sol_cert2 = _synthetic_cert(_sol_map_ref_a2, _sol_map_ref_b2)
_sol_raw_strengthened = {
    "schema_id": RAW_SCHEMA, "certificate": _sol_cert2, "native_a": _sol_native_a, "native_b": _sol_native_b,
    "native_registry_refs": {
        "native_a": {"artifact_id": "native_a", "whole_artifact_digest": eu.sha256_of(_sol_native_a), "version_id": "v1"},
        "native_b": {"artifact_id": "native_b", "whole_artifact_digest": eu.sha256_of(_sol_native_b), "version_id": "v1"},
    },
}
_sol_result_strengthened = eu.evidence_union_from_raw_w6(_sol_raw_strengthened)
record("P88-o negative (a) / Sol 便88 F88-3.2, STRENGTHENED (attacker also forges native_registry_refs, "
       "guessing the real artifact_id convention, whole_artifact_digest computed from the ATTACKER's OWN "
       "forged content -- not the receiver's actually-pinned content): evidence_union_from_raw_w6(...) -> "
       "overall != PASS (the receiver's pinned 'native_a'/'native_b' registry entries, from section 10a, "
       "hold DIFFERENT content, so the claimed digest disagrees -> STALE)",
       _sol_result_strengthened["overall_status"] != "PASS", _sol_result_strengthened)
record("P88-o negative (a) strengthened: native_registry_status.status == 'STALE'",
       _sol_result_strengthened.get("native_registry_status", {}).get("status") == "STALE",
       _sol_result_strengthened.get("native_registry_status"))

# --- 13b. unknown artifact_id.
_registry_refs_unknown = {
    "native_a": {"artifact_id": "does-not-exist-in-registry", "whole_artifact_digest": "0" * 64, "version_id": "v1"},
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1"},
}
_raw_unknown_artifact = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": {}, "native_b": {},
                          "native_registry_refs": _registry_refs_unknown}
_result_unknown = eu.evidence_union_from_raw_w6(_raw_unknown_artifact)
record("P88-o negative (b) unknown artifact_id: native_registry_refs['native_a'].artifact_id names an "
       "unregistered artifact (registry itself present and non-empty) -> native_registry_status UNKNOWN, overall != PASS",
       _result_unknown.get("native_registry_status", {}).get("status") == "UNKNOWN" and _result_unknown["overall_status"] != "PASS",
       _result_unknown)

# --- 13c. stale digest.
_registry_refs_stale = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": "1" * 64, "version_id": "v1"},  # WRONG, doesn't match actual registered content
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1"},
}
_raw_stale = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": {}, "native_b": {},
              "native_registry_refs": _registry_refs_stale}
_result_stale = eu.evidence_union_from_raw_w6(_raw_stale)
record("P88-o negative (c) stale digest: native_registry_refs['native_a'].whole_artifact_digest disagrees with "
       "the receiver's currently-pinned artifact digest -> native_registry_status STALE, overall != PASS",
       _result_stale.get("native_registry_status", {}).get("status") == "STALE" and _result_stale["overall_status"] != "PASS",
       _result_stale)

# --- 13d. A/B swap (isolated from 10d's cert-level exercise -- here via a
#     cert that legitimately points both lanes at "native_a"/"native_b"
#     but the registry claim swaps which role each id was pinned under).
_registry_refs_ab_swap = {
    "native_a": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1"},
    "native_b": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1"},
}
_raw_ab_swap = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": {}, "native_b": {},
                 "native_registry_refs": _registry_refs_ab_swap}
_result_ab_swap = eu.evidence_union_from_raw_w6(_raw_ab_swap)
record("P88-o negative (d) A/B swap: native_registry_refs['native_a'] claims the artifact pinned with role "
       "'native_b' (and vice versa) -> native_registry_status ROLE_MISMATCH, overall != PASS",
       _result_ab_swap.get("native_registry_status", {}).get("status") == "ROLE_MISMATCH" and _result_ab_swap["overall_status"] != "PASS",
       _result_ab_swap)

# --- 13e. registry store absent entirely.
import shutil as _shutil
_test_index_path = reg.index_path(TEST_REGISTRY_DIR)
_index_had = os.path.isfile(_test_index_path)
_index_backup_path = _test_index_path + ".p88o_test_backup"
if _index_had:
    _shutil.move(_test_index_path, _index_backup_path)
try:
    _registry_refs_no_store = {
        "native_a": {"artifact_id": "native_a", "whole_artifact_digest": "2" * 64, "version_id": "v1"},
        "native_b": {"artifact_id": "native_b", "whole_artifact_digest": "2" * 64, "version_id": "v1"},
    }
    _raw_no_store = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": {}, "native_b": {},
                      "native_registry_refs": _registry_refs_no_store}
    _result_no_store = eu.evidence_union_from_raw_w6(_raw_no_store)
    record("P88-o negative (e) registry store absent entirely (index.json removed): native_registry_status "
           "MISSING (distinct from (b)'s UNKNOWN -- the store itself, not merely this artifact_id, is absent), "
           "overall != PASS",
           _result_no_store.get("native_registry_status", {}).get("status") == "MISSING" and _result_no_store["overall_status"] != "PASS",
           _result_no_store)
finally:
    if _index_had:
        _shutil.move(_index_backup_path, _test_index_path)

# --- 13f. legacy object_id+inline: a correctly-registered artifact (role,
#     digest, artifact_id all matching) whose CERTIFICATE map_ref still
#     uses the legacy object_id/inline path (no json_pointer at all) --
#     cert_pos_01's own shape. Registering its actual native content does
#     NOT make it operative: the registry is never touched by dereference
#     when there is no json_pointer to resolve.
# Sol 便90 F90-4.1 blocker 3: "native_a"/"native_b" already hold DIFFERENT
# content from 10a/10d above -- overwriting them now requires an explicit
# supersede=True (a default-reject write_entry call would raise
# ValueError here); this is exactly the legitimate, audited re-
# provisioning use case the supersede path exists for (see section 15
# below for the corresponding negative: an overwrite WITHOUT supersede
# raises).
prov.write_entry("native_a", "native_a", "v1", _cert_pos_01["native_a"], registry_dir=TEST_REGISTRY_DIR, supersede=True)
prov.write_entry("native_b", "native_b", "v1", _cert_pos_01["native_b"], registry_dir=TEST_REGISTRY_DIR, supersede=True)
_registry_refs_legacy = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": reg.resolve("native_a")["whole_artifact_digest"], "version_id": "v1"},
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": reg.resolve("native_b")["whole_artifact_digest"], "version_id": "v1"},
}
_raw_legacy_object_id = {
    "schema_id": RAW_SCHEMA, "certificate": _cert_pos_01["certificate"],
    "native_a": _cert_pos_01["native_a"], "native_b": _cert_pos_01["native_b"],
    "native_registry_refs": _registry_refs_legacy,
}
_result_legacy = eu.evidence_union_from_raw_w6(_raw_legacy_object_id)
record("P88-o negative (f) legacy object_id+inline: EVEN WITH a correctly-registered, role/digest/artifact_id "
       "matching registry pin, a map_ref using object_id (no json_pointer) never dereferences against the "
       "pinned registry content -- native_registry_status LEGACY_UNVERIFIED_REF, overall != PASS",
       _result_legacy.get("native_registry_status", {}).get("status") == "LEGACY_UNVERIFIED_REF"
       and _result_legacy["overall_status"] != "PASS",
       _result_legacy)

# NOTE: 13f's reg.write_entry calls above rewrite the "native_a"/"native_b"
# registry entries (to cert_pos_01's own native content) -- this is safe
# only because it is the LAST registry mutation in this file; nothing
# below this point (only the final report) depends on the earlier 10a/10d
# content under those same ids.

# --------------------------------------------------------------------------
# 14. Sol 便89 registry hardening (docs/notes/cert_shape_interpretation_
#     addendum_o_v9.md): 3 new negatives closing the 3 blockers found in
#     v8's registry -- test/production store separation, version_id
#     format validation, version_id omission no longer bypassing the
#     version check.
# --------------------------------------------------------------------------

# --- 14a. test attempts to write into the PRODUCTION registry directory
#     without operator opt-in -> PermissionError, and the production store
#     is provably untouched (file count under it is unchanged before/after
#     the attempt, and NINFTY_EP_ALLOW_PRODUCTION_WRITE is confirmed unset
#     for the whole duration of this test run).
assert os.environ.get(prov.ENV_ALLOW_PRODUCTION_WRITE) != "1", (
    "test process must never set NINFTY_EP_ALLOW_PRODUCTION_WRITE=1 -- this is the precondition 14a checks"
)
os.makedirs(reg.PRODUCTION_REGISTRY_DIR, exist_ok=True)
_prod_files_before = sorted(os.listdir(reg.PRODUCTION_REGISTRY_DIR))
_prod_write_raised = None
try:
    prov.write_entry("attacker_artifact", "native_a", "v1", {"forged": "content"}, registry_dir=reg.PRODUCTION_REGISTRY_DIR)
except PermissionError as e:
    _prod_write_raised = e
_prod_files_after = sorted(os.listdir(reg.PRODUCTION_REGISTRY_DIR))
record("Sol 便89 negative 1: write_entry(registry_dir=PRODUCTION_REGISTRY_DIR) without "
       "NINFTY_EP_ALLOW_PRODUCTION_WRITE=1 raises PermissionError",
       isinstance(_prod_write_raised, PermissionError), repr(_prod_write_raised))
record("Sol 便89 negative 1b: the production registry directory's file listing is BYTE-IDENTICAL before/after "
       "the rejected write attempt (no partial/leaked write occurred)",
       _prod_files_before == _prod_files_after,
       {"before": _prod_files_before, "after": _prod_files_after})
record("Sol 便89 negative 1c: resolve('attacker_artifact') against the production store finds nothing "
       "(the rejected write never reached it)",
       reg.resolve("attacker_artifact", registry_dir=reg.PRODUCTION_REGISTRY_DIR) is None, "n/a")

# --- 14b. version_id omitted from a raw evidence artifact's
#     native_registry_refs claim -> MISSING (not a silent skip-the-check
#     that could still reach PASS pre-fix), overall != PASS. Uses the
#     already-registered 13f-era "native_a"/"native_b" content, TEST store.
_registry_refs_no_version = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": reg.resolve("native_a")["whole_artifact_digest"]},
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": reg.resolve("native_b")["whole_artifact_digest"]},
}
_raw_no_version = {
    "schema_id": RAW_SCHEMA, "certificate": _cert_deref_only,
    "native_a": _native_a_real, "native_b": _native_b_real,
    "native_registry_refs": _registry_refs_no_version,
}
_result_no_version = eu.evidence_union_from_raw_w6(_raw_no_version)
record("Sol 便89 negative 2: native_registry_refs[...] with version_id OMITTED entirely -> "
       "native_registry_status MISSING (was silently skipping the version check and could still reach "
       "PASS pre-fix), overall != PASS",
       _result_no_version.get("native_registry_status", {}).get("status") == "MISSING"
       and _result_no_version["overall_status"] != "PASS",
       _result_no_version.get("native_registry_status"))

# --- 14c. malformed version_id formats at write_entry (registry
#     provisioning level) -> ValueError, none reach the store.
for _bad_version, _bad_label in (
    (None, "None"), ("", "empty string"), ("   ", "whitespace-only"),
    ("has spaces", "contains a space"), ("../../etc/passwd", "path-traversal-shaped"),
    ("a" * 65, "too long (65 chars)"), (42, "non-string (int)"),
):
    _raised = None
    try:
        prov.write_entry("bad_version_probe", "native_a", _bad_version, {"x": 1}, registry_dir=TEST_REGISTRY_DIR)
    except ValueError as e:
        _raised = e
    record(f"Sol 便89 negative 3 ({_bad_label}): write_entry(version_id={_bad_version!r}) raises ValueError",
           isinstance(_raised, ValueError), repr(_raised))
record("Sol 便89 negative 3 (no leakage): none of the malformed-version write_entry attempts left a resolvable "
       "'bad_version_probe' entry in the TEST store",
       reg.resolve("bad_version_probe", registry_dir=TEST_REGISTRY_DIR) is None, "n/a")


# --------------------------------------------------------------------------
# 15. Sol 便90 F90-4.1 (o) 残 4 項 (docs/notes/cert_shape_interpretation_
#     addendum_o_v10.md): resolver/provisioning split, default-reject
#     same-artifact_id overwrite (+ supersede), atomic/locked entry+index
#     updates, malformed-JSON handling inside resolve(), and the stronger
#     whole-tree production_snapshot_digest replacing v9's file-name-list
#     comparison.
# --------------------------------------------------------------------------

import shutil as _shutil15
import time as _time15

_15_DIR = tempfile.mkdtemp(prefix="ninfty_ep_registry_test_15_")

# --- 15a. default-reject: writing a DIFFERENT-content entry under an
#     artifact_id that already exists (same role, different content) with
#     no supersede flag raises ValueError, and the EXISTING entry is left
#     completely unchanged (resolve still returns the OLD content).
prov.write_entry("dup_probe", "native_a", "v1", {"payload": "original"}, registry_dir=_15_DIR)
_dup_before = reg.resolve("dup_probe", registry_dir=_15_DIR)
_dup_raised = None
try:
    prov.write_entry("dup_probe", "native_a", "v1", {"payload": "DIFFERENT"}, registry_dir=_15_DIR)
except ValueError as e:
    _dup_raised = e
_dup_after = reg.resolve("dup_probe", registry_dir=_15_DIR)
record("Sol 便90 F90-4.1 blocker 3 negative (default-reject overwrite): write_entry(same artifact_id, "
       "DIFFERENT content, no supersede) raises ValueError",
       isinstance(_dup_raised, ValueError), repr(_dup_raised))
record("Sol 便90 F90-4.1 blocker 3 negative (no silent overwrite): rejected write left the EXISTING entry's "
       "content byte-identical (whole_artifact_digest unchanged)",
       _dup_before is not None and _dup_after is not None
       and _dup_before["whole_artifact_digest"] == _dup_after["whole_artifact_digest"] == reg._digest({"payload": "original"}),
       {"before": _dup_before, "after": _dup_after})

# --- 15b. supersede=True: succeeds, resolve() now returns the NEW
#     content, and the OLD version is preserved (archived file + index
#     'superseded' history entry), never deleted.
_dup_old_digest = _dup_before["whole_artifact_digest"]
_super_result = prov.write_entry("dup_probe", "native_a", "v2", {"payload": "SUPERSEDED"}, registry_dir=_15_DIR, supersede=True)
_dup_after_super = reg.resolve("dup_probe", registry_dir=_15_DIR)
record("Sol 便90 F90-4.1 blocker 3 (supersede=True succeeds): write_entry(..., supersede=True) does not raise, "
       "reports superseded=True",
       _super_result.get("superseded") is True, _super_result)
record("Sol 便90 F90-4.1 blocker 3 (supersede=True): resolve() now returns the NEW content",
       _dup_after_super is not None and _dup_after_super["content"] == {"payload": "SUPERSEDED"}
       and _dup_after_super["version_id"] == "v2",
       _dup_after_super)
_super_index = reg._load_index(_15_DIR)
_super_hist = (_super_index.get("artifacts", {}).get("dup_probe", {}) or {}).get("superseded", [])
record("Sol 便90 F90-4.1 blocker 3 (old version preserved, not deleted): the index's 'superseded' history for "
       "'dup_probe' contains exactly one entry, recording the OLD whole_artifact_digest",
       len(_super_hist) == 1 and _super_hist[0].get("whole_artifact_digest") == _dup_old_digest,
       _super_hist)
_archive_dir = os.path.join(_15_DIR, "_superseded")
_archive_files = os.listdir(_archive_dir) if os.path.isdir(_archive_dir) else []
_archived_old_content = None
for _af in _archive_files:
    with open(os.path.join(_archive_dir, _af), "r", encoding="utf-8") as _f:
        _archived_entry = json.load(_f)
    if _archived_entry.get("artifact_id") == "dup_probe" and _archived_entry.get("whole_artifact_digest") == _dup_old_digest:
        _archived_old_content = _archived_entry.get("content")
record("Sol 便90 F90-4.1 blocker 3 (archived file, byte-for-byte): an archived copy of the OLD 'dup_probe' "
       "entry ({'payload': 'original'}) exists on disk under _superseded/",
       _archived_old_content == {"payload": "original"}, {"archive_files": _archive_files, "found": _archived_old_content})

# --- 15c. idempotent re-write: SAME content, SAME role, no supersede
#     flag -> succeeds silently (not a content change), superseded=False,
#     no history entry appended.
_idem_result = prov.write_entry("dup_probe", "native_a", "v2", {"payload": "SUPERSEDED"}, registry_dir=_15_DIR)
_idem_index = reg._load_index(_15_DIR)
_idem_hist = (_idem_index.get("artifacts", {}).get("dup_probe", {}) or {}).get("superseded", [])
record("Sol 便90 F90-4.1 blocker 3 (idempotent same-content re-write): write_entry(identical role+content) does "
       "not raise and reports superseded=False",
       _idem_result.get("superseded") is False, _idem_result)
record("Sol 便90 F90-4.1 blocker 3 (idempotent re-write appends no new history): the 'superseded' history is "
       "still exactly the one entry from 15b (unchanged by the idempotent re-write)",
       len(_idem_hist) == 1, _idem_hist)

# --- 15d. locked updates: a held lock file blocks a concurrent write_entry
#     call (RegistryLockTimeout within a short caller-supplied timeout);
#     removing the lock lets a subsequent call through immediately.
_lock_dir = tempfile.mkdtemp(prefix="ninfty_ep_registry_test_15d_")
_held_lock_path = prov._lock_path(_lock_dir)
os.makedirs(_lock_dir, exist_ok=True)
with open(_held_lock_path, "w", encoding="utf-8") as _f:
    _f.write("held-by-test-15d")
_lock_timeout_raised = None
try:
    with prov._acquire_lock(_lock_dir, timeout=0.3, poll=0.05):
        pass
except prov.RegistryLockTimeout as e:
    _lock_timeout_raised = e
record("Sol 便90 F90-4.1 blocker 4 (locked updates): a pre-held lock file blocks a second lock acquisition, "
       "raising RegistryLockTimeout within the caller's own short timeout",
       isinstance(_lock_timeout_raised, prov.RegistryLockTimeout), repr(_lock_timeout_raised))
os.remove(_held_lock_path)
_lock_after_release_ok = False
try:
    with prov._acquire_lock(_lock_dir, timeout=1.0, poll=0.02):
        _lock_after_release_ok = True
except prov.RegistryLockTimeout:
    _lock_after_release_ok = False
record("Sol 便90 F90-4.1 blocker 4 (lock released): once the held lock file is removed, a subsequent "
       "_acquire_lock succeeds immediately",
       _lock_after_release_ok, "n/a")
_shutil15.rmtree(_lock_dir, ignore_errors=True)

# --- 15e. atomic writes: after a normal write_entry call, no stray
#     '.tmp-*' file is left behind under the registry directory (a crash
#     mid-write is the ONLY thing that should ever produce one, and this
#     run performs no crash).
prov.write_entry("atomic_probe", "native_a", "v1", {"x": 1}, registry_dir=_15_DIR)
_tmp_leftovers = [n for n in os.listdir(_15_DIR) if ".tmp-" in n]
record("Sol 便90 F90-4.1 blocker 4 (atomic writes, no partial files): no '.tmp-*' file remains under the "
       "registry directory after a normal write_entry call",
       _tmp_leftovers == [], _tmp_leftovers)

# --- 15f. malformed JSON handling: resolve() must fail closed (return
#     None), never propagate json.JSONDecodeError/OSError, when an entry
#     file or the index itself is corrupted on disk.
prov.write_entry("corrupt_probe", "native_a", "v1", {"y": 2}, registry_dir=_15_DIR)
_corrupt_index = reg._load_index(_15_DIR)
_corrupt_fname = _corrupt_index["artifacts"]["corrupt_probe"]["file"]
_corrupt_entry_path = os.path.join(_15_DIR, _corrupt_fname)
with open(_corrupt_entry_path, "w", encoding="utf-8") as _f:
    _f.write("{not valid json at all")
_corrupt_resolve_raised = None
_corrupt_resolve_result = "SENTINEL_NOT_SET"
try:
    _corrupt_resolve_result = reg.resolve("corrupt_probe", registry_dir=_15_DIR)
except Exception as e:  # noqa: BLE001 -- this IS the "must never raise" probe
    _corrupt_resolve_raised = e
record("Sol 便90 F90-4.1 blocker 6 (malformed entry JSON, resolve() fails closed): resolve() against a "
       "hand-corrupted entry file returns None and raises NOTHING (was an uncaught JSONDecodeError pre-fix)",
       _corrupt_resolve_raised is None and _corrupt_resolve_result is None,
       {"raised": repr(_corrupt_resolve_raised), "result": _corrupt_resolve_result})

_malformed_index_dir = tempfile.mkdtemp(prefix="ninfty_ep_registry_test_15f_")
with open(reg.index_path(_malformed_index_dir), "w", encoding="utf-8") as _f:
    _f.write("{{{ this is not json")
_index_malformed_raised = None
_index_malformed_result = "SENTINEL_NOT_SET"
try:
    _index_malformed_result = reg.resolve("anything", registry_dir=_malformed_index_dir)
except Exception as e:  # noqa: BLE001
    _index_malformed_raised = e
record("Sol 便90 F90-4.1 blocker 6 (malformed index.json, resolve() fails closed): resolve() against a "
       "hand-corrupted index.json returns None and raises NOTHING",
       _index_malformed_raised is None and _index_malformed_result is None,
       {"raised": repr(_index_malformed_raised), "result": _index_malformed_result})
_shutil15.rmtree(_malformed_index_dir, ignore_errors=True)

# --- 15g. production_snapshot_digest is byte-identical at the START and
#     END of this whole test run -- STRONGER than v9's negative 14a (which
#     only compared sorted FILE NAMES; a same-named file with silently
#     mutated bytes would slip past that check but not this one). No test
#     in this file writes into PRODUCTION_REGISTRY_DIR successfully (14a's
#     own attempt is rejected with PermissionError before touching disk;
#     15h below is rejected with ValueError before touching disk, same
#     reasoning).
_PROD_SNAPSHOT_DIGEST_AT_END = reg.production_snapshot_digest(registry_dir=reg.PRODUCTION_REGISTRY_DIR)
record("Sol 便90 F90-4.1 blocker 5/8 (production tree whole-byte digest unchanged across the WHOLE test run): "
       "production_snapshot_digest(PRODUCTION_REGISTRY_DIR) at the very start of this run == at the very end",
       _PROD_SNAPSHOT_DIGEST_AT_START == _PROD_SNAPSHOT_DIGEST_AT_END,
       {"start": _PROD_SNAPSHOT_DIGEST_AT_START, "end": _PROD_SNAPSHOT_DIGEST_AT_END})

# --- 15h. production writes require freeze_id: even WITH the production
#     write opt-in set, omitting freeze_id raises ValueError before any
#     file is touched -- production directory listing/digest unaffected.
_prod_files_before_15h = sorted(os.listdir(reg.PRODUCTION_REGISTRY_DIR))
os.environ[prov.ENV_ALLOW_PRODUCTION_WRITE] = "1"
_freeze_missing_raised = None
try:
    prov.write_entry("freeze_id_probe", "native_a", "v1", {"z": 3}, registry_dir=reg.PRODUCTION_REGISTRY_DIR)
except ValueError as e:
    _freeze_missing_raised = e
finally:
    del os.environ[prov.ENV_ALLOW_PRODUCTION_WRITE]
_prod_files_after_15h = sorted(os.listdir(reg.PRODUCTION_REGISTRY_DIR))
record("Sol 便90 F90-4.1 blocker 7 (production write requires freeze_id): write_entry(registry_dir=PRODUCTION, "
       "ALLOW_PRODUCTION_WRITE=1, freeze_id OMITTED) raises ValueError",
       isinstance(_freeze_missing_raised, ValueError), repr(_freeze_missing_raised))
record("Sol 便90 F90-4.1 blocker 7 (no leakage): the rejected freeze_id-less write left PRODUCTION_REGISTRY_DIR's "
       "file listing byte-identical",
       _prod_files_before_15h == _prod_files_after_15h,
       {"before": _prod_files_before_15h, "after": _prod_files_after_15h})
record("Sol 便90 F90-4.1 blocker 7 (no leakage, resolve confirms): resolve('freeze_id_probe') against "
       "PRODUCTION_REGISTRY_DIR finds nothing",
       reg.resolve("freeze_id_probe", registry_dir=reg.PRODUCTION_REGISTRY_DIR) is None, "n/a")

# --- 15i. structural: no OTHER production file under search/ dynamically
#     loads the provisioning module at all (mirrors section 8's check for
#     ninfty-evidence-union.py's own private names) -- the facade's
#     resolver-only import is not merely a convention, nothing else in
#     the tree can reach write_entry either.
_PROV_LOAD_MARKER = '"ninfty-native-registry-provisioning.py"'
_PROV_EXEMPT_FILES = {"ninfty-native-registry-provisioning.py", "test_ninfty_evidence_union.py"}
_prov_loaders_found = []
for fn in sorted(os.listdir(HERE)):
    full = os.path.join(HERE, fn)
    if not os.path.isfile(full) or fn in _PROV_EXEMPT_FILES or not fn.endswith((".py", ".mjs")):
        continue
    try:
        with open(full, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        continue
    if _PROV_LOAD_MARKER in content:
        _prov_loaders_found.append(fn)
record("Sol 便90 F90-4.1 blocker 2 (resolver/provisioning separation, structural): no file directly under "
       "search/ (excluding this test and the provisioning module itself) dynamically loads "
       "ninfty-native-registry-provisioning.py -- in particular ninfty-evidence-union.py does not",
       _prov_loaders_found == [], _prov_loaders_found)
record("Sol 便90 F90-4.1 blocker 2 (resolver module has no write_entry attribute at all): "
       "hasattr(reg, 'write_entry') is False -- not merely unused, structurally absent from the module the "
       "facade actually loads",
       not hasattr(reg, "write_entry"), hasattr(reg, "write_entry"))

_shutil15.rmtree(_15_DIR, ignore_errors=True)


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
