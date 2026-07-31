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
# file is the "receiver" doing out-of-band provisioning (prov.commit_generation)
# ahead of building any `raw` evidence artifact; evidence-union.py itself
# never calls commit_generation/resolve_bundle-as-provisioner (only
# resolve/resolve_bundle, read-only), see ninfty-native-registry.py's own
# docstring. Sol 便90 F90-4.1 blocker 2 (docs/notes/
# cert_shape_interpretation_addendum_o_v10.md), superseded in shape (not in
# the underlying separation) by Sol 便91 P91-4's generation-commit redesign
# (docs/notes/cert_shape_interpretation_addendum_o_v11.md, `write_entry` ->
# `commit_generation`): resolve/resolve_bundle/index_exists and
# commit_generation now live in TWO SEPARATE modules -- `reg` (resolver-only,
# the same module evidence-union.py itself loads) and `prov`
# (provisioning-only, loaded ONLY by this test file / a future operator
# CLI, never by evidence-union.py). NOTE (Sol 便92 F92-6.2 item 2): this
# comment block previously still said "prov.write_entry" here, describing
# the pre-便91 mutable-entry API that no longer exists in either module --
# corrected to `commit_generation`, the generation-commit call this file
# actually uses throughout (see `_commit15`/section 15/section 16 below).
reg = _load_module("ninfty_native_registry_for_eu_test", "ninfty-native-registry.py")
prov = _load_module("ninfty_native_registry_provisioning_for_eu_test", "ninfty-native-registry-provisioning.py")

# Sol 便89 fix (test/production registry store separation, docs/notes/
# cert_shape_interpretation_addendum_o_v9.md): this test process's own
# registry store is a FRESH tempdir, wholly distinct from
# reg.PRODUCTION_REGISTRY_DIR (search/certs/ep_registry/). Every
# prov.commit_generation(...) call in this file passes
# registry_dir=<some tempdir> explicitly (commit_generation has no default
# registry_dir any more -- a caller cannot forget; keyword-only, required).
# The NINFTY_EP_REGISTRY_DIR env var is set so that reg.resolve(...)/
# reg.resolve_bundle(...) -- including the copy evidence-union.py's own
# _registry() dynamically loads and calls with NO dir parameter of its
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

# Sol 便91 P91-4 (sol/sol_reply_91_math18.md F91-6.2, docs/notes/
# cert_shape_interpretation_addendum_o_v11.md): registry content now
# enters via `prov.commit_generation` -- a whole GENERATION (one or more
# artifacts, all bound to ONE shared freeze_id) is built and self-verified
# off to the side, then published as a single atomic CURRENT-pointer
# swap. `_native_b_different`/`DIFFERENT_MAP` (originally computed later,
# at what was section 10d) is hoisted up here so it can be committed in
# the SAME generation as native_a/native_b -- all three artifacts
# (native_a, native_b, native_b_alt) need to be simultaneously resolvable
# throughout sections 10-13 below, which is only possible if they live in
# ONE generation (resolve() only ever reads the CURRENT generation).
DIFFERENT_MAP = [{"branch_value": "pt-9", "multiplicity": 7}]
DIFFERENT_MAP_DIGEST = eu.sha256_of(DIFFERENT_MAP)
_native_b_different = _synthetic_native(DIFFERENT_MAP)

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
# "正当な artifact では従来どおり PASS すること"). prov.commit_generation is
# the receiver's OUT-OF-BAND provisioning step -- it never runs as part of
# processing a caller-supplied raw evidence artifact. Sol 便91 P91-4: ONE
# generation, bundling native_a/native_b/native_b_alt together under ONE
# shared freeze_id (native_b_alt is needed by section 10d/13d below, and
# must be simultaneously resolvable alongside native_a/native_b -- see the
# hoisting note above REAL_MAP).
GEN10_FREEZE_ID = "freeze-sec10-13"
_gen10 = prov.commit_generation(
    [
        {"artifact_id": "native_a", "role": "native_a", "version_id": "v1", "content": _native_a_real},
        {"artifact_id": "native_b", "role": "native_b", "version_id": "v1", "content": _native_b_real},
        {"artifact_id": "native_b_alt", "role": "native_b", "version_id": "v1", "content": _native_b_different},
    ],
    GEN10_FREEZE_ID, registry_dir=TEST_REGISTRY_DIR,
)
_REG_DIGEST_NATIVE_A = _gen10["artifacts"]["native_a"]
_REG_DIGEST_NATIVE_B = _gen10["artifacts"]["native_b"]
_REG_DIGEST_NATIVE_B_ALT = _gen10["artifacts"]["native_b_alt"]
_registry_refs_deref_only = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
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
# DIFFERENT_MAP/_native_b_different were hoisted above (before the
# combined 10a commit_generation call, Sol 便91 P91-4) so that
# "native_b_alt" could be committed in the SAME generation as native_a/
# native_b -- both must be simultaneously resolvable, and resolve() only
# ever reads the CURRENT generation.
# Sol 便88 P88-o: a DISTINCT artifact_id ("native_b_alt") from 10a's
# already-registered "native_b" -- avoids overwriting 10a's registry
# entry (which 10a's own PASS assertions, and section 11's CLI PASS
# probe, both depend on) with different content under the same id.
_map_ref_b_different = {"artifact_id": "native_b_alt", "digest": DIFFERENT_MAP_DIGEST, "json_pointer": "/pushforward_map"}
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

_registry_refs_correct = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
    "native_b": {"artifact_id": "native_b_alt", "whole_artifact_digest": _REG_DIGEST_NATIVE_B_ALT, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
}
# Sol 便88 P88-o item 5(d) A/B swap: the registry REFS (not raw's inert
# top-level native_a/native_b) are what now carries the "which artifact
# backs which slot" claim -- swapping THEM is the v8-era equivalent of
# the old "runner-argument-level swap" this negative originally tested.
_registry_refs_swapped = {
    "native_a": {"artifact_id": "native_b_alt", "whole_artifact_digest": _REG_DIGEST_NATIVE_B_ALT, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
    "native_b": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
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
        "native_a": {"artifact_id": "native_a", "whole_artifact_digest": eu.sha256_of(_sol_native_a), "version_id": "v1", "freeze_id": "attacker-guessed-freeze"},
        "native_b": {"artifact_id": "native_b", "whole_artifact_digest": eu.sha256_of(_sol_native_b), "version_id": "v1", "freeze_id": "attacker-guessed-freeze"},
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
    "native_a": {"artifact_id": "does-not-exist-in-registry", "whole_artifact_digest": "0" * 64, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
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
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": "1" * 64, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},  # WRONG digest, doesn't match actual registered content
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
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
    "native_a": {"artifact_id": "native_b", "whole_artifact_digest": _REG_DIGEST_NATIVE_B, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
    "native_b": {"artifact_id": "native_a", "whole_artifact_digest": _REG_DIGEST_NATIVE_A, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
}
_raw_ab_swap = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": {}, "native_b": {},
                 "native_registry_refs": _registry_refs_ab_swap}
_result_ab_swap = eu.evidence_union_from_raw_w6(_raw_ab_swap)
record("P88-o negative (d) A/B swap: native_registry_refs['native_a'] claims the artifact pinned with role "
       "'native_b' (and vice versa) -> native_registry_status ROLE_MISMATCH, overall != PASS",
       _result_ab_swap.get("native_registry_status", {}).get("status") == "ROLE_MISMATCH" and _result_ab_swap["overall_status"] != "PASS",
       _result_ab_swap)

# --- 13e. registry store absent entirely. Sol 便91 P91-4: "absent" now
#     means CURRENT.json (the single mutable pointer) is missing --
#     temporarily rename it away and back.
import shutil as _shutil
_test_current_path = reg.current_path(TEST_REGISTRY_DIR)
_current_had = os.path.isfile(_test_current_path)
_current_backup_path = _test_current_path + ".p88o_test_backup"
if _current_had:
    _shutil.move(_test_current_path, _current_backup_path)
try:
    _registry_refs_no_store = {
        "native_a": {"artifact_id": "native_a", "whole_artifact_digest": "2" * 64, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
        "native_b": {"artifact_id": "native_b", "whole_artifact_digest": "2" * 64, "version_id": "v1", "freeze_id": GEN10_FREEZE_ID},
    }
    _raw_no_store = {"schema_id": RAW_SCHEMA, "certificate": _cert_deref_only, "native_a": {}, "native_b": {},
                      "native_registry_refs": _registry_refs_no_store}
    _result_no_store = eu.evidence_union_from_raw_w6(_raw_no_store)
    record("P88-o negative (e) registry store absent entirely (CURRENT.json removed): native_registry_status "
           "MISSING (distinct from (b)'s UNKNOWN -- the store itself, not merely this artifact_id, is absent), "
           "overall != PASS",
           _result_no_store.get("native_registry_status", {}).get("status") == "MISSING" and _result_no_store["overall_status"] != "PASS",
           _result_no_store)
finally:
    if _current_had:
        _shutil.move(_current_backup_path, _test_current_path)

# --- 13f. legacy object_id+inline: a correctly-registered artifact (role,
#     digest, artifact_id all matching) whose CERTIFICATE map_ref still
#     uses the legacy object_id/inline path (no json_pointer at all) --
#     cert_pos_01's own shape. Registering its actual native content does
#     NOT make it operative: the registry is never touched by dereference
#     when there is no json_pointer to resolve.
# Sol 便91 P91-4: "native_a"/"native_b" already hold DIFFERENT content
# from 10a/10d above (the generation committed there, GEN10_FREEZE_ID) --
# there is no "overwrite an existing entry" concept any more (blocker 3):
# re-provisioning new content is always a BRAND NEW generation, committed
# and self-verified off to the side, then published via a single atomic
# CURRENT-pointer swap. This is exactly the legitimate re-provisioning use
# case the old supersede path existed for, now realized without any
# in-place mutation at all -- the 10a/10d generation's own files remain
# byte-identical on disk, simply no longer CURRENT (see section 15b below
# for the corresponding regression guard).
GEN13F_FREEZE_ID = "freeze-sec13f"
_gen13f = prov.commit_generation(
    [
        {"artifact_id": "native_a", "role": "native_a", "version_id": "v2", "content": _cert_pos_01["native_a"]},
        {"artifact_id": "native_b", "role": "native_b", "version_id": "v2", "content": _cert_pos_01["native_b"]},
    ],
    GEN13F_FREEZE_ID, registry_dir=TEST_REGISTRY_DIR,
)
_registry_refs_legacy = {
    "native_a": {"artifact_id": "native_a", "whole_artifact_digest": reg.resolve("native_a")["whole_artifact_digest"], "version_id": "v2", "freeze_id": GEN13F_FREEZE_ID},
    "native_b": {"artifact_id": "native_b", "whole_artifact_digest": reg.resolve("native_b")["whole_artifact_digest"], "version_id": "v2", "freeze_id": GEN13F_FREEZE_ID},
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

# NOTE: 13f's commit_generation call above publishes a NEW generation
# (GEN13F_FREEZE_ID) that becomes CURRENT for artifact_ids "native_a"/
# "native_b" going forward -- this is safe (unlike the old mutable-entry
# design's supersede path) precisely BECAUSE nothing is mutated in place:
# the 10a/10d generation (GEN10_FREEZE_ID, holding "native_a"/"native_b"/
# "native_b_alt" under their ORIGINAL content) is left completely
# untouched on disk, byte for byte, under generations/ -- it is simply no
# longer what CURRENT.json points to. Section 15 below commits further
# generations into TEST_REGISTRY_DIR; each is independently verified not
# to disturb any earlier one's on-disk bytes (see 15b).

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
    prov.commit_generation(
        [{"artifact_id": "attacker_artifact", "role": "native_a", "version_id": "v1", "content": {"forged": "content"}}],
        "attacker-freeze", registry_dir=reg.PRODUCTION_REGISTRY_DIR,
    )
except PermissionError as e:
    _prod_write_raised = e
_prod_files_after = sorted(os.listdir(reg.PRODUCTION_REGISTRY_DIR))
record("Sol 便89 negative 1 (Sol 便91 P91-4 API): commit_generation(registry_dir=PRODUCTION_REGISTRY_DIR) without "
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

# --- 14c. malformed version_id formats at commit_generation (registry
#     provisioning level) -> ValueError, none reach the store (Sol 便91
#     P91-4 API: a rejected commit never creates the generation directory
#     at all -- validated BEFORE any file is written).
for _bad_version, _bad_label in (
    (None, "None"), ("", "empty string"), ("   ", "whitespace-only"),
    ("has spaces", "contains a space"), ("../../etc/passwd", "path-traversal-shaped"),
    ("a" * 65, "too long (65 chars)"), (42, "non-string (int)"),
):
    _raised = None
    try:
        prov.commit_generation(
            [{"artifact_id": "bad_version_probe", "role": "native_a", "version_id": _bad_version, "content": {"x": 1}}],
            "freeze-14c", registry_dir=TEST_REGISTRY_DIR,
        )
    except ValueError as e:
        _raised = e
    record(f"Sol 便89 negative 3 ({_bad_label}): commit_generation(version_id={_bad_version!r}) raises ValueError",
           isinstance(_raised, ValueError), repr(_raised))
record("Sol 便89 negative 3 (no leakage): none of the malformed-version commit_generation attempts left a "
       "resolvable 'bad_version_probe' entry in the TEST store (CURRENT still points at GEN13F_FREEZE_ID)",
       reg.resolve("bad_version_probe", registry_dir=TEST_REGISTRY_DIR) is None, "n/a")


# --------------------------------------------------------------------------
# 15. Sol 便91 P91-4 (sol/sol_reply_91_math18.md F91-6.2, docs/notes/
#     cert_shape_interpretation_addendum_o_v11.md): the generation-commit
#     registry redesign. Each subsection is labeled with the F91-6.2
#     blocker number(s) it targets (11 total, all numbered 1-11 in that
#     finding) plus the consumer-side freeze gate (blocker 10).
# --------------------------------------------------------------------------

import shutil as _shutil15

_15_DIR = tempfile.mkdtemp(prefix="ninfty_ep_registry_test_15_")


def _commit15(artifacts, freeze_id, **kw):
    return prov.commit_generation(artifacts, freeze_id, registry_dir=_15_DIR, **kw)


# --- 15a. blocker 1 (fail-open on a corrupted "existing" entry):
#     commit_generation NEVER reads or depends on any prior state to
#     decide what to write. (i) a fresh, unrelated commit succeeds and
#     publishes even though an EARLIER (no-longer-CURRENT) generation has
#     been hand-corrupted on disk; (ii) an explicit generation_id that
#     COLLIDES with an existing (even corrupted) directory is refused
#     outright (FileExistsError) -- there is no "treat it as absent and
#     overwrite" path to fail open on.
_gen15a_1 = _commit15(
    [{"artifact_id": "a1", "role": "native_a", "version_id": "v1", "content": {"n": 1}},
     {"artifact_id": "b1", "role": "native_b", "version_id": "v1", "content": {"n": 2}}],
    "freeze-15a",
)
_gen15a_1_dir = os.path.join(reg.generations_dir(_15_DIR), _gen15a_1["generation_id"])
_gen15a_1_index = json.load(open(os.path.join(_gen15a_1_dir, "index.json"), encoding="utf-8"))
_gen15a_1_a1_file = _gen15a_1_index["artifacts"]["a1"]["file"]
with open(os.path.join(_gen15a_1_dir, _gen15a_1_a1_file), "w", encoding="utf-8") as _f:
    _f.write("{not valid json at all, corrupted on purpose")

_gen15a_2 = _commit15(
    [{"artifact_id": "a2", "role": "native_a", "version_id": "v1", "content": {"n": 3}},
     {"artifact_id": "b2", "role": "native_b", "version_id": "v1", "content": {"n": 4}}],
    "freeze-15a-2",
)
record("Sol 便91 F91-6.2 blocker 1 (a corrupted PAST generation does not block or corrupt a fresh commit): "
       "commit_generation for a brand-new generation succeeds and publishes despite an unrelated earlier "
       "generation being hand-corrupted on disk",
       _gen15a_2["published"] is True, _gen15a_2)
record("Sol 便91 F91-6.2 blocker 1 (the corrupted past generation resolves to nothing, not silently 'fixed'): "
       "resolve('a1') against CURRENT (now gen 2) finds nothing -- gen 1 is simply no longer live",
       reg.resolve("a1", registry_dir=_15_DIR) is None, "n/a")

_collide_raised = None
try:
    prov.commit_generation(
        [{"artifact_id": "x", "role": "native_a", "version_id": "v1", "content": {}}],
        "freeze-15a-collide", registry_dir=_15_DIR, generation_id=_gen15a_1["generation_id"],
    )
except FileExistsError as e:
    _collide_raised = e
record("Sol 便91 F91-6.2 blocker 1 (no fail-open on generation_id collision): commit_generation with an "
       "EXPLICIT generation_id that already exists on disk (even corrupted) raises FileExistsError, never "
       "silently overwrites",
       isinstance(_collide_raised, FileExistsError), repr(_collide_raised))

# --- 15b. blocker 2 (entry-before-index non-atomicity / cross-generation
#     mutation): committing a SECOND, unrelated generation must not touch
#     ANY byte of an EARLIER generation's own files.
_gen15b_1 = _commit15(
    [{"artifact_id": "keep_a", "role": "native_a", "version_id": "v1", "content": {"stable": True}},
     {"artifact_id": "keep_b", "role": "native_b", "version_id": "v1", "content": {"stable": True}}],
    "freeze-15b-1",
)
_gen15b_1_dir = os.path.join(reg.generations_dir(_15_DIR), _gen15b_1["generation_id"])
_gen15b_1_bytes_before = {
    fn: open(os.path.join(_gen15b_1_dir, fn), "rb").read() for fn in sorted(os.listdir(_gen15b_1_dir))
}
_gen15b_2 = _commit15(
    [{"artifact_id": "other_a", "role": "native_a", "version_id": "v1", "content": {"different": True}},
     {"artifact_id": "other_b", "role": "native_b", "version_id": "v1", "content": {"different": True}}],
    "freeze-15b-2",
)
_gen15b_1_bytes_after = {
    fn: open(os.path.join(_gen15b_1_dir, fn), "rb").read() for fn in sorted(os.listdir(_gen15b_1_dir))
}
record("Sol 便91 F91-6.2 blocker 2 (no cross-generation mutation): every byte of generation 1's own files "
       "(index.json + entries + receipt.json) is IDENTICAL before and after committing an unrelated "
       "generation 2",
       _gen15b_1_bytes_before == _gen15b_1_bytes_after,
       {"before_names": sorted(_gen15b_1_bytes_before), "after_names": sorted(_gen15b_1_bytes_after),
        "equal": _gen15b_1_bytes_before == _gen15b_1_bytes_after})

# --- 15c. blocker 3 (silent metadata drift): the SAME content committed
#     twice with DIFFERENT version_id is always TWO distinct generations
#     (never an in-place metadata update) -- neither mutates the other.
_gen15c_1 = _commit15(
    [{"artifact_id": "drift_a", "role": "native_a", "version_id": "v1", "content": {"same": "content"}},
     {"artifact_id": "drift_b", "role": "native_b", "version_id": "v1", "content": {"same": "content"}}],
    "freeze-15c-1", publish=False,
)
_gen15c_2 = _commit15(
    [{"artifact_id": "drift_a", "role": "native_a", "version_id": "v2-DRIFTED", "content": {"same": "content"}},
     {"artifact_id": "drift_b", "role": "native_b", "version_id": "v2-DRIFTED", "content": {"same": "content"}}],
    "freeze-15c-2", publish=False,
)
record("Sol 便91 F91-6.2 blocker 3 (no silent metadata drift): two generations with IDENTICAL content but "
       "DIFFERENT version_id get DISTINCT generation_ids (same content digest, but never merged/mutated)",
       _gen15c_1["generation_id"] != _gen15c_2["generation_id"]
       and _gen15c_1["artifacts"]["drift_a"] == _gen15c_2["artifacts"]["drift_a"],
       {"gen1": _gen15c_1["generation_id"], "gen2": _gen15c_2["generation_id"]})
_gen15c_1_dir = os.path.join(reg.generations_dir(_15_DIR), _gen15c_1["generation_id"])
_gen15c_1_index = json.load(open(os.path.join(_gen15c_1_dir, "index.json"), encoding="utf-8"))
record("Sol 便91 F91-6.2 blocker 3 (gen 1's own on-disk metadata is untouched by gen 2's commit): "
       "gen 1's index.json still records version_id='v1' for drift_a, not 'v2-DRIFTED'",
       _gen15c_1_index["artifacts"]["drift_a"]["version_id"] == "v1", _gen15c_1_index["artifacts"]["drift_a"])

# --- 15d. blocker 4/5 (non-transactional commit / resolver ignoring
#     index-vs-entry disagreement): hand-tamper ONE cached field in
#     index.json (leaving the entry file itself untouched) -> resolve()
#     must fail closed (None) for the WHOLE generation, not silently
#     trust either copy.
_gen15d = _commit15(
    [{"artifact_id": "meta_a", "role": "native_a", "version_id": "v1", "content": {"m": 1}},
     {"artifact_id": "meta_b", "role": "native_b", "version_id": "v1", "content": {"m": 2}}],
    "freeze-15d",
)
_gen15d_dir = os.path.join(reg.generations_dir(_15_DIR), _gen15d["generation_id"])
_gen15d_index_path = os.path.join(_gen15d_dir, "index.json")
_gen15d_index = json.load(open(_gen15d_index_path, encoding="utf-8"))
_gen15d_index["artifacts"]["meta_a"]["status"] = "REVOKED"  # entry file itself still says ACTIVE
with open(_gen15d_index_path, "w", encoding="utf-8") as _f:
    json.dump(_gen15d_index, _f)
record("Sol 便91 F91-6.2 blocker 4/5 (index-vs-entry metadata disagreement fails closed): hand-tampering "
       "index.json's cached 'status' for one artifact (leaving the entry file itself unchanged) makes "
       "resolve() for THAT artifact return None",
       reg.resolve("meta_a", registry_dir=_15_DIR) is None, "n/a")
record("Sol 便91 F91-6.2 blocker 4/5 (whole generation invalidated, not just the tampered artifact): "
       "the OTHER artifact in the SAME (now-inconsistent) generation also fails to resolve",
       reg.resolve("meta_b", registry_dir=_15_DIR) is None, "n/a")

# --- 15e. blocker 5 (resolver schema not checked): a battery of
#     structurally-malformed generations, each must resolve to None.
def _fresh_gen15e(label):
    r = _commit15(
        [{"artifact_id": f"se_a_{label}", "role": "native_a", "version_id": "v1", "content": {"k": label}},
         {"artifact_id": f"se_b_{label}", "role": "native_b", "version_id": "v1", "content": {"k": label}}],
        f"freeze-15e-{label}",
    )
    return r, os.path.join(reg.generations_dir(_15_DIR), r["generation_id"])


_r15e, _d15e = _fresh_gen15e("wrong_index_schema")
_idx15e = json.load(open(os.path.join(_d15e, "index.json"), encoding="utf-8"))
_idx15e["schema_id"] = "not/the/right/schema"
with open(os.path.join(_d15e, "index.json"), "w", encoding="utf-8") as _f:
    json.dump(_idx15e, _f)
record("Sol 便91 F91-6.2 blocker 5 (wrong index.json schema_id): resolve() returns None",
       reg.resolve("se_a_wrong_index_schema", registry_dir=_15_DIR) is None, "n/a")

_r15e, _d15e = _fresh_gen15e("wrong_entry_schema")
_idx15e = json.load(open(os.path.join(_d15e, "index.json"), encoding="utf-8"))
_fn15e = _idx15e["artifacts"]["se_a_wrong_entry_schema"]["file"]
_ent15e = json.load(open(os.path.join(_d15e, _fn15e), encoding="utf-8"))
_ent15e["schema_id"] = "not/the/right/schema"
with open(os.path.join(_d15e, _fn15e), "w", encoding="utf-8") as _f:
    json.dump(_ent15e, _f)
record("Sol 便91 F91-6.2 blocker 5 (wrong entry schema_id): resolve() returns None",
       reg.resolve("se_a_wrong_entry_schema", registry_dir=_15_DIR) is None, "n/a")

_r15e, _d15e = _fresh_gen15e("bad_role")
_idx15e = json.load(open(os.path.join(_d15e, "index.json"), encoding="utf-8"))
_idx15e["artifacts"]["se_a_bad_role"]["role"] = "native_c"
with open(os.path.join(_d15e, "index.json"), "w", encoding="utf-8") as _f:
    json.dump(_idx15e, _f)
record("Sol 便91 F91-6.2 blocker 5 (invalid role in index metadata): resolve() returns None",
       reg.resolve("se_a_bad_role", registry_dir=_15_DIR) is None, "n/a")

_r15e, _d15e = _fresh_gen15e("bad_version_shape")
_idx15e = json.load(open(os.path.join(_d15e, "index.json"), encoding="utf-8"))
_idx15e["artifacts"]["se_a_bad_version_shape"]["version_id"] = "has spaces"
with open(os.path.join(_d15e, "index.json"), "w", encoding="utf-8") as _f:
    json.dump(_idx15e, _f)
record("Sol 便91 F91-6.2 blocker 5 (malformed version_id in index metadata): resolve() returns None",
       reg.resolve("se_a_bad_version_shape", registry_dir=_15_DIR) is None, "n/a")

_r15e, _d15e = _fresh_gen15e("malformed_entry_json")
_idx15e = json.load(open(os.path.join(_d15e, "index.json"), encoding="utf-8"))
_fn15e = _idx15e["artifacts"]["se_a_malformed_entry_json"]["file"]
with open(os.path.join(_d15e, _fn15e), "w", encoding="utf-8") as _f:
    _f.write("{not valid json at all")
_malformed_entry_raised = None
_malformed_entry_result = "SENTINEL_NOT_SET"
try:
    _malformed_entry_result = reg.resolve("se_a_malformed_entry_json", registry_dir=_15_DIR)
except Exception as e:  # noqa: BLE001 -- this IS the "must never raise" probe
    _malformed_entry_raised = e
record("Sol 便91 F91-6.2 blocker 5 (malformed entry JSON, resolve() fails closed, never raises): "
       "resolve() against a hand-corrupted entry file returns None and raises NOTHING",
       _malformed_entry_raised is None and _malformed_entry_result is None,
       {"raised": repr(_malformed_entry_raised), "result": _malformed_entry_result})

_r15e, _d15e = _fresh_gen15e("malformed_index_json")
with open(os.path.join(_d15e, "index.json"), "w", encoding="utf-8") as _f:
    _f.write("{{{ this is not json")
_malformed_index_raised = None
_malformed_index_result = "SENTINEL_NOT_SET"
try:
    _malformed_index_result = reg.resolve("se_a_malformed_index_json", registry_dir=_15_DIR)
except Exception as e:  # noqa: BLE001
    _malformed_index_raised = e
record("Sol 便91 F91-6.2 blocker 5 (malformed index.json, resolve() fails closed, never raises): "
       "resolve() against a hand-corrupted index.json returns None and raises NOTHING",
       _malformed_index_raised is None and _malformed_index_result is None,
       {"raised": repr(_malformed_index_raised), "result": _malformed_index_result})

# --- 15f. blocker 6 (path confinement): index.json's 'file' field
#     rewritten to point OUTSIDE the generation directory -> resolve()
#     returns None, and the out-of-bounds sentinel file's content is
#     never returned.
_r15f, _d15f = _fresh_gen15e("escape")
_sentinel_path = os.path.join(_15_DIR, "OUTSIDE_SENTINEL.json")
with open(_sentinel_path, "w", encoding="utf-8") as _f:
    json.dump({"schema_id": reg.GEN_ENTRY_SCHEMA_ID, "generation_id": _r15f["generation_id"],
               "artifact_id": "se_a_escape", "role": "native_a", "version_id": "v1",
               "freeze_id": "freeze-15e-escape", "status": "ACTIVE",
               "whole_artifact_digest": reg._digest("SENTINEL"), "content": "SENTINEL"}, _f)
_idx_path15f = os.path.join(_d15f, "index.json")
_idx15f_base = json.load(open(_idx_path15f, encoding="utf-8"))
for _escape_value in ("../OUTSIDE_SENTINEL.json", os.path.join("..", "..", "OUTSIDE_SENTINEL.json"),
                       os.path.abspath(_sentinel_path)):
    _idx15f = json.loads(json.dumps(_idx15f_base))
    _idx15f["artifacts"]["se_a_escape"]["file"] = _escape_value
    with open(_idx_path15f, "w", encoding="utf-8") as _f:
        json.dump(_idx15f, _f)
    _escape_result = reg.resolve("se_a_escape", registry_dir=_15_DIR)
    record(f"Sol 便91 F91-6.2 blocker 6 (path confinement, file={_escape_value!r}): resolve() returns None, "
           "never reads/returns the out-of-bounds sentinel content",
           _escape_result is None, _escape_result)
os.remove(_sentinel_path)

# --- 15g. blocker 7 (production-directory alias bypass): a directory
#     JUNCTION pointing AT PRODUCTION_REGISTRY_DIR (different path
#     STRING, same filesystem object) must still be treated as
#     production and refused without opt-in -- a bare string/abspath
#     comparison would miss this. Junctions need no elevation on NTFS; if
#     junction creation itself is unavailable in this sandbox, the check
#     is skipped honestly rather than faked.
_alias_parent = tempfile.mkdtemp(prefix="ninfty_ep_alias_")
_alias_dir = os.path.join(_alias_parent, "prod_alias")
_junction_ok = False
if sys.platform == "win32":
    _mk = subprocess.run(["cmd", "/c", "mklink", "/J", _alias_dir, reg.PRODUCTION_REGISTRY_DIR],
                          capture_output=True, text=True)
    _junction_ok = _mk.returncode == 0 and os.path.isdir(_alias_dir)
if _junction_ok:
    _alias_write_raised = None
    try:
        prov.commit_generation(
            [{"artifact_id": "alias_attacker", "role": "native_a", "version_id": "v1", "content": {}}],
            "freeze-alias", registry_dir=_alias_dir,
        )
    except PermissionError as e:
        _alias_write_raised = e
    record("Sol 便91 F91-6.2 blocker 7 (production alias bypass via junction): commit_generation through a "
           "directory JUNCTION pointing at PRODUCTION_REGISTRY_DIR still raises PermissionError without "
           "opt-in (samefile-based detection, not a string comparison)",
           isinstance(_alias_write_raised, PermissionError), repr(_alias_write_raised))
else:
    record("Sol 便91 F91-6.2 blocker 7 (production alias bypass via junction) -- SKIPPED: this sandbox could "
           "not create a directory junction (mklink /J failed or non-Windows); _is_production_dir's "
           "samefile/realpath logic is exercised indirectly by every OTHER production-directory check in "
           "this suite (14a, 15o) but the alias-specific case could not be constructed here",
           True, "SKIPPED, not a failure")
_shutil15.rmtree(_alias_parent, ignore_errors=True)

# --- 15h. blocker 8 (receipt self-reference): receipt.json is EXCLUDED
#     from generation_digest's own file set -- tampering a receipt field
#     NOT used by the digest (issued_at) must NOT break resolve(), while
#     tampering the receipt's OWN generation_digest field (which IS
#     checked, just not self-referentially hashed) MUST break it.
_gen15h = _commit15(
    [{"artifact_id": "recv_a", "role": "native_a", "version_id": "v1", "content": {"r": 1}},
     {"artifact_id": "recv_b", "role": "native_b", "version_id": "v1", "content": {"r": 2}}],
    "freeze-15h",
)
_gen15h_dir = os.path.join(reg.generations_dir(_15_DIR), _gen15h["generation_id"])
_receipt_path = os.path.join(_gen15h_dir, "receipt.json")
_receipt = json.load(open(_receipt_path, encoding="utf-8"))
_receipt["issued_at"] = "2099-01-01T00:00:00+00:00"  # not part of generation_digest's domain
with open(_receipt_path, "w", encoding="utf-8") as _f:
    json.dump(_receipt, _f)
record("Sol 便91 F91-6.2 blocker 8 (receipt excluded from its own hash domain): tampering receipt.json's "
       "'issued_at' field (not part of generation_digest's file set) does NOT break resolve()",
       reg.resolve("recv_a", registry_dir=_15_DIR) is not None, "n/a")
_receipt["generation_digest"] = "0" * 64  # now tamper the field that IS checked
with open(_receipt_path, "w", encoding="utf-8") as _f:
    json.dump(_receipt, _f)
record("Sol 便91 F91-6.2 blocker 8 (receipt's OWN generation_digest field IS verified): tampering "
       "receipt.json's 'generation_digest' value makes resolve() return None",
       reg.resolve("recv_a", registry_dir=_15_DIR) is None, "n/a")

# --- 15i. blocker 9 (bundle receipt binds ALL artifacts + shared freeze +
#     generation_digest together, in ONE file): structural check on a
#     fresh generation's own receipt.json, plus a tamper test showing the
#     binding is PER-GENERATION (tampering one artifact's digest inside
#     the receipt invalidates the WHOLE generation, not just that one
#     artifact).
_gen15i = _commit15(
    [{"artifact_id": "bund_a", "role": "native_a", "version_id": "v1", "content": {"i": 1}},
     {"artifact_id": "bund_b", "role": "native_b", "version_id": "v1", "content": {"i": 2}}],
    "freeze-15i",
)
_gen15i_dir = os.path.join(reg.generations_dir(_15_DIR), _gen15i["generation_id"])
_bundle_receipt = json.load(open(os.path.join(_gen15i_dir, "receipt.json"), encoding="utf-8"))
_bundle_ids = {e["artifact_id"] for e in _bundle_receipt.get("artifacts", [])}
record("Sol 便91 F91-6.2 blocker 9 (one bundle receipt lists EVERY artifact in the generation): "
       "receipt.json's 'artifacts' list contains BOTH bund_a and bund_b, plus the shared freeze_id and "
       "generation_digest, all in ONE file",
       _bundle_ids == {"bund_a", "bund_b"} and _bundle_receipt.get("freeze_id") == "freeze-15i"
       and reg.HEX64.match(_bundle_receipt.get("generation_digest", "")) is not None,
       _bundle_receipt)
_receipt_path_i = os.path.join(_gen15i_dir, "receipt.json")
_tampered_receipt = json.loads(json.dumps(_bundle_receipt))
for _e in _tampered_receipt["artifacts"]:
    if _e["artifact_id"] == "bund_a":
        _e["whole_artifact_digest"] = "f" * 64
with open(_receipt_path_i, "w", encoding="utf-8") as _f:
    json.dump(_tampered_receipt, _f)
record("Sol 便91 F91-6.2 blocker 9 (tampering ONE artifact's digest inside the bundle receipt invalidates "
       "the WHOLE generation): resolve('bund_b') -- a DIFFERENT artifact in the SAME generation -- also "
       "returns None, not just resolve('bund_a')",
       reg.resolve("bund_a", registry_dir=_15_DIR) is None and reg.resolve("bund_b", registry_dir=_15_DIR) is None,
       "n/a")

# --- 15j. blocker 10 (consumer freeze gate): native_registry_refs must
#     carry freeze_id, and it must match the registry's pinned value.
_gen15j = _commit15(
    [{"artifact_id": "fz_a", "role": "native_a", "version_id": "v1", "content": {"f": 1}},
     {"artifact_id": "fz_b", "role": "native_b", "version_id": "v1", "content": {"f": 2}}],
    "freeze-15j",
)
_fz_cert = _synthetic_cert(
    {"artifact_id": "fz_a", "digest": eu.sha256_of({"note": "n/a"}), "json_pointer": "/pushforward_map"},
    {"artifact_id": "fz_b", "digest": eu.sha256_of({"note": "n/a"}), "json_pointer": "/pushforward_map"},
)
_fz_a_digest = reg.resolve("fz_a", registry_dir=_15_DIR)["whole_artifact_digest"]
_fz_b_digest = reg.resolve("fz_b", registry_dir=_15_DIR)["whole_artifact_digest"]
_prior_env_registry_dir = os.environ.get("NINFTY_EP_REGISTRY_DIR")
os.environ["NINFTY_EP_REGISTRY_DIR"] = _15_DIR
try:
    _refs_no_freeze = {
        "native_a": {"artifact_id": "fz_a", "whole_artifact_digest": _fz_a_digest, "version_id": "v1"},
        "native_b": {"artifact_id": "fz_b", "whole_artifact_digest": _fz_b_digest, "version_id": "v1"},
    }
    _raw_no_freeze = {"schema_id": RAW_SCHEMA, "certificate": _fz_cert, "native_a": {}, "native_b": {},
                       "native_registry_refs": _refs_no_freeze}
    _result_no_freeze = eu.evidence_union_from_raw_w6(_raw_no_freeze)
    record("Sol 便91 F91-6.2 blocker 10 (freeze_id omitted from native_registry_refs): native_registry_status "
           "MISSING (same bucket as an omitted version_id), overall != PASS",
           _result_no_freeze.get("native_registry_status", {}).get("status") == "MISSING"
           and _result_no_freeze["overall_status"] != "PASS",
           _result_no_freeze.get("native_registry_status"))

    _refs_wrong_freeze = {
        "native_a": {"artifact_id": "fz_a", "whole_artifact_digest": _fz_a_digest, "version_id": "v1", "freeze_id": "not-the-real-freeze"},
        "native_b": {"artifact_id": "fz_b", "whole_artifact_digest": _fz_b_digest, "version_id": "v1", "freeze_id": "freeze-15j"},
    }
    _raw_wrong_freeze = {"schema_id": RAW_SCHEMA, "certificate": _fz_cert, "native_a": {}, "native_b": {},
                          "native_registry_refs": _refs_wrong_freeze}
    _result_wrong_freeze = eu.evidence_union_from_raw_w6(_raw_wrong_freeze)
    record("Sol 便91 F91-6.2 blocker 10 (claimed freeze_id disagrees with the registry's pinned value): "
           "native_registry_status STALE for the disagreeing lane, overall != PASS",
           _result_wrong_freeze.get("native_registry_status", {}).get("status") == "STALE"
           and _result_wrong_freeze["overall_status"] != "PASS",
           _result_wrong_freeze.get("native_registry_status"))
finally:
    if _prior_env_registry_dir is not None:
        os.environ["NINFTY_EP_REGISTRY_DIR"] = _prior_env_registry_dir

# consumer-layer cross-side check (both lanes individually PASS, but their
# RESOLVED freeze_id values disagree with EACH OTHER): unit-tested via a
# stub registry double, since the real generation-commit registry makes a
# genuine cross-generation A/B pairing structurally unreachable through
# ONE resolve() session (a generation binds every artifact it contains to
# ONE shared freeze_id, and resolve() only ever reads the CURRENT
# generation -- see the resolver module's own blocker-10 docstring note).
# This isolates and exercises the CONSUMER's OWN comparison code directly.
class _StubReg:
    @staticmethod
    def resolve(artifact_id, registry_dir=None):
        if artifact_id == "stub_a":
            return {"role": "native_a", "status": "ACTIVE", "version_id": "v1", "freeze_id": "freeze-X",
                    "whole_artifact_digest": "a" * 64, "content": {}}
        if artifact_id == "stub_b":
            return {"role": "native_b", "status": "ACTIVE", "version_id": "v1", "freeze_id": "freeze-Y",
                    "whole_artifact_digest": "b" * 64, "content": {}}
        return None

    @staticmethod
    def index_exists(registry_dir=None):
        return True

    @staticmethod
    def resolve_bundle(artifact_ids, registry_dir=None):
        # Sol 便92 P92-6: the consumer now calls resolve_bundle, not
        # resolve, per side -- this stub double mirrors that (fanning out
        # to the same per-id resolve() above) so the FREEZE_MISMATCH
        # consumer-layer cross-side check (deliberately exercised via a
        # STUB whose two artifacts disagree on freeze_id, something the
        # real generation-commit registry cannot produce in one call) is
        # still reached through the code path the fixed facade actually
        # uses.
        return {
            "generation_id": "stub-gen",
            "freeze_id": "stub-gen-freeze",
            "artifacts": {aid: _StubReg.resolve(aid) for aid in artifact_ids},
        }


_orig_registry_module = eu._NATIVE_REGISTRY_MODULE
eu._NATIVE_REGISTRY_MODULE = _StubReg
try:
    _stub_cert = _synthetic_cert(
        {"artifact_id": "stub_a", "digest": "z" * 64, "json_pointer": "/pushforward_map"},
        {"artifact_id": "stub_b", "digest": "z" * 64, "json_pointer": "/pushforward_map"},
    )
    _stub_refs = {
        "native_a": {"artifact_id": "stub_a", "whole_artifact_digest": "a" * 64, "version_id": "v1", "freeze_id": "freeze-X"},
        "native_b": {"artifact_id": "stub_b", "whole_artifact_digest": "b" * 64, "version_id": "v1", "freeze_id": "freeze-Y"},
    }
    _stub_overall, _, _, _stub_detail = eu._resolve_native_registry(
        {"native_registry_refs": _stub_refs, "certificate": _stub_cert}
    )
    record("Sol 便91 F91-6.2 blocker 10 (consumer cross-side check, stub registry double): native_a resolved "
           "with freeze_id='freeze-X', native_b with freeze_id='freeze-Y' (both individually well-formed "
           "PASS-shaped refs) -> overall FREEZE_MISMATCH, both sides downgraded",
           _stub_overall == "FREEZE_MISMATCH"
           and _stub_detail["native_a"]["status"] == "FREEZE_MISMATCH"
           and _stub_detail["native_b"]["status"] == "FREEZE_MISMATCH",
           _stub_detail)
finally:
    eu._NATIVE_REGISTRY_MODULE = _orig_registry_module

# --- 15k. blocker 11 (production store's old flat-shape entries are no
#     longer resolvable at all): PRODUCTION_REGISTRY_DIR still contains
#     the pre-便91 flat index.json + 3 entry files (inert leftovers of the
#     retired schema -- untouched by this task per the standing "no
#     production-store content changes without commander authorization"
#     instruction) but the NEW resolver never even looks at that shape --
#     it only ever looks for CURRENT.json + generations/, neither of
#     which exists yet under PRODUCTION_REGISTRY_DIR.
record("Sol 便91 F91-6.2 blocker 11 (old flat-shape production entries are inert under the new schema): "
       "reg.index_exists(PRODUCTION_REGISTRY_DIR) is False -- no CURRENT.json exists there yet",
       reg.index_exists(registry_dir=reg.PRODUCTION_REGISTRY_DIR) is False, "n/a")
for _old_id in ("native_a", "native_b", "native_b_alt"):
    record(f"Sol 便91 F91-6.2 blocker 11 (old production entry {_old_id!r} unresolvable under the new schema): "
           "resolve() against PRODUCTION_REGISTRY_DIR returns None",
           reg.resolve(_old_id, registry_dir=reg.PRODUCTION_REGISTRY_DIR) is None, "n/a")

# --- 15l. locked CURRENT-pointer publish: a held lock file blocks a
#     concurrent commit_generation's publish step (RegistryLockTimeout
#     within a short caller-supplied timeout via the same _acquire_lock
#     primitive commit_generation itself uses around the CURRENT.json
#     swap); removing the lock lets a subsequent acquisition through
#     immediately.
_lock_dir = tempfile.mkdtemp(prefix="ninfty_ep_registry_test_15l_")
_held_lock_path = prov._lock_path(_lock_dir)
os.makedirs(_lock_dir, exist_ok=True)
with open(_held_lock_path, "w", encoding="utf-8") as _f:
    _f.write("held-by-test-15l")
_lock_timeout_raised = None
try:
    with prov._acquire_lock(_lock_dir, timeout=0.3, poll=0.05):
        pass
except prov.RegistryLockTimeout as e:
    _lock_timeout_raised = e
record("Sol 便91 F91-6.2 blocker 2/4 (locked CURRENT-pointer publish): a pre-held lock file blocks a second "
       "lock acquisition, raising RegistryLockTimeout within the caller's own short timeout",
       isinstance(_lock_timeout_raised, prov.RegistryLockTimeout), repr(_lock_timeout_raised))
os.remove(_held_lock_path)
_lock_after_release_ok = False
try:
    with prov._acquire_lock(_lock_dir, timeout=1.0, poll=0.02):
        _lock_after_release_ok = True
except prov.RegistryLockTimeout:
    _lock_after_release_ok = False
record("Sol 便91 F91-6.2 blocker 2/4 (lock released): once the held lock file is removed, a subsequent "
       "_acquire_lock succeeds immediately",
       _lock_after_release_ok, "n/a")
_shutil15.rmtree(_lock_dir, ignore_errors=True)

# --- 15m. atomic writes: after a normal commit_generation call, no stray
#     '.tmp-*' file is left behind anywhere under the registry directory
#     (a crash mid-write is the ONLY thing that should ever produce one,
#     and this run performs no crash).
_commit15(
    [{"artifact_id": "atomic_a", "role": "native_a", "version_id": "v1", "content": {"x": 1}},
     {"artifact_id": "atomic_b", "role": "native_b", "version_id": "v1", "content": {"x": 2}}],
    "freeze-atomic",
)
_tmp_leftovers = []
for _dirpath, _dirnames, _filenames in os.walk(_15_DIR):
    _tmp_leftovers.extend(n for n in _filenames if ".tmp-" in n)
record("Sol 便91 F91-6.2 blocker 2/4 (atomic writes, no partial files): no '.tmp-*' file remains anywhere "
       "under the registry directory after a normal commit_generation call",
       _tmp_leftovers == [], _tmp_leftovers)

# --- 15n. production_snapshot_digest is byte-identical at the START and
#     END of this whole test run -- unaffected by the 便91 registry
#     redesign (this function is deliberately schema-agnostic). No test in
#     this file writes into PRODUCTION_REGISTRY_DIR successfully (14a's
#     own attempt, 15g's junction attempt if run, and 15o below are all
#     rejected before touching disk).
_PROD_SNAPSHOT_DIGEST_AT_END = reg.production_snapshot_digest(registry_dir=reg.PRODUCTION_REGISTRY_DIR)
record("Sol 便90 F90-4.1 blocker 5/8 (production tree whole-byte digest unchanged across the WHOLE test run, "
       "carried forward under 便91): production_snapshot_digest(PRODUCTION_REGISTRY_DIR) at the very start "
       "of this run == at the very end",
       _PROD_SNAPSHOT_DIGEST_AT_START == _PROD_SNAPSHOT_DIGEST_AT_END,
       {"start": _PROD_SNAPSHOT_DIGEST_AT_START, "end": _PROD_SNAPSHOT_DIGEST_AT_END})

# --- 15o. production commits require freeze_id UNCONDITIONALLY (carried
#     forward from 便90 blocker 7, now unconditional for every store, not
#     just production -- see 14c's malformed-version loop for the general
#     case; this checks the specific "freeze_id entirely omitted" shape
#     against PRODUCTION_REGISTRY_DIR).
_prod_files_before_15o = sorted(os.listdir(reg.PRODUCTION_REGISTRY_DIR))
os.environ[prov.ENV_ALLOW_PRODUCTION_WRITE] = "1"
_freeze_missing_raised = None
try:
    prov.commit_generation(
        [{"artifact_id": "freeze_id_probe", "role": "native_a", "version_id": "v1", "content": {"z": 3}}],
        None, registry_dir=reg.PRODUCTION_REGISTRY_DIR,
    )
except (ValueError, TypeError) as e:
    _freeze_missing_raised = e
finally:
    del os.environ[prov.ENV_ALLOW_PRODUCTION_WRITE]
_prod_files_after_15o = sorted(os.listdir(reg.PRODUCTION_REGISTRY_DIR))
record("Sol 便90 F90-4.1 blocker 7 (carried forward, now unconditional): commit_generation(registry_dir="
       "PRODUCTION, ALLOW_PRODUCTION_WRITE=1, freeze_id=None) raises",
       isinstance(_freeze_missing_raised, (ValueError, TypeError)), repr(_freeze_missing_raised))
record("Sol 便90 F90-4.1 blocker 7 (no leakage): the rejected freeze_id-less commit left "
       "PRODUCTION_REGISTRY_DIR's file listing byte-identical",
       _prod_files_before_15o == _prod_files_after_15o,
       {"before": _prod_files_before_15o, "after": _prod_files_after_15o})
record("Sol 便90 F90-4.1 blocker 7 (no leakage, resolve confirms): resolve('freeze_id_probe') against "
       "PRODUCTION_REGISTRY_DIR finds nothing",
       reg.resolve("freeze_id_probe", registry_dir=reg.PRODUCTION_REGISTRY_DIR) is None, "n/a")

# --- 15p. structural: no OTHER production file under search/ dynamically
#     loads the provisioning module at all (mirrors section 8's check for
#     ninfty-evidence-union.py's own private names) -- the facade's
#     resolver-only import is not merely a convention, nothing else in
#     the tree can reach commit_generation either.
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
record("Sol 便90 F90-4.1 blocker 2 (resolver/provisioning separation, structural, carried forward): no file "
       "directly under search/ (excluding this test and the provisioning module itself) dynamically loads "
       "ninfty-native-registry-provisioning.py -- in particular ninfty-evidence-union.py does not",
       _prov_loaders_found == [], _prov_loaders_found)
record("Sol 便90 F90-4.1 blocker 2 (resolver module has no commit_generation/write_entry attribute at all): "
       "hasattr(reg, 'commit_generation') is False and hasattr(reg, 'write_entry') is False -- not merely "
       "unused, structurally absent from the module the facade actually loads",
       not hasattr(reg, "commit_generation") and not hasattr(reg, "write_entry"),
       {"commit_generation": hasattr(reg, "commit_generation"), "write_entry": hasattr(reg, "write_entry")})

_shutil15.rmtree(_15_DIR, ignore_errors=True)


# --------------------------------------------------------------------------
# 16. Sol 便92 P92-6 (sol/sol_reply_92_math19.md W92-6/F92-6.1, docs/notes/
#     cert_shape_interpretation_addendum_o_v12.md): same-freeze,
#     different-generation TOCTOU race. Two SEPARATE resolve() calls (one
#     per A/B lane), each independently re-reading CURRENT.json, can
#     straddle a publisher's atomic generation swap and return artifacts
#     from TWO DIFFERENT generations that happen to share one freeze_id --
#     no bundle receipt binds that specific cross-generation pair, and the
#     consumer's own freeze-STRING-equality cross-check (blocker 10, 便91)
#     cannot catch it (both freeze_id strings genuinely agree). The
#     PREVIOUS negative suite (15j) only ever tried a DIFFERENT-freeze
#     mismatch. `resolve_bundle` closes this by reading CURRENT exactly
#     once and resolving every requested artifact from that ONE captured
#     generation.
# --------------------------------------------------------------------------
_16_DIR = tempfile.mkdtemp(prefix="ninfty_ep_registry_test_16_")

_gen16_0 = prov.commit_generation(
    [{"artifact_id": "race_a", "role": "native_a", "version_id": "v0", "content": {"gen": 0, "x": 1}},
     {"artifact_id": "race_b", "role": "native_b", "version_id": "v0", "content": {"gen": 0, "x": 2}}],
    "freeze-race", registry_dir=_16_DIR,
)
_gen16_1 = prov.commit_generation(
    [{"artifact_id": "race_a", "role": "native_a", "version_id": "v1", "content": {"gen": 1, "x": 10}},
     {"artifact_id": "race_b", "role": "native_b", "version_id": "v1", "content": {"gen": 1, "x": 20}}],
    "freeze-race", registry_dir=_16_DIR, publish=False,
)
_gen16_2 = prov.commit_generation(
    [{"artifact_id": "race_a", "role": "native_a", "version_id": "v2", "content": {"gen": 2, "x": 100}},
     {"artifact_id": "race_b", "role": "native_b", "version_id": "v2", "content": {"gen": 2, "x": 200}}],
    "freeze-race", registry_dir=_16_DIR, publish=False,
)
record("Sol 便92 P92-6 fixture: gen16_0/1/2 all share ONE freeze_id ('freeze-race') but are THREE DISTINCT "
       "generations -- nothing in the schema forbids two generations from reusing the same freeze_id, which is "
       "exactly what makes the freeze-STRING-equality cross-check (blocker 10) insufficient on its own",
       len({_gen16_0["generation_id"], _gen16_1["generation_id"], _gen16_2["generation_id"]}) == 3
       and _gen16_0["freeze_id"] == _gen16_1["freeze_id"] == _gen16_2["freeze_id"] == "freeze-race",
       {"gen0": _gen16_0["generation_id"], "gen1": _gen16_1["generation_id"], "gen2": _gen16_2["generation_id"]})

# --- 16a. the OLD/vulnerable pattern (two SEPARATE resolve() calls, a
#     publish landing between them) DOES yield a same-freeze, mixed-
#     generation pair -- CURRENT starts at gen16_0.
_race_entry_a_old = reg.resolve("race_a", registry_dir=_16_DIR)   # reads CURRENT == gen16_0
prov.publish_generation(_gen16_1["generation_id"], registry_dir=_16_DIR)   # atomic swap: CURRENT -> gen16_1
_race_entry_b_old = reg.resolve("race_b", registry_dir=_16_DIR)   # reads CURRENT == gen16_1
record("Sol 便92 W92-6 (bug class reproduced at the resolve() primitive): two separate resolve() calls "
       "straddling a CURRENT swap return artifacts from TWO DIFFERENT generations (gen16_0's race_a, gen16_1's "
       "race_b) that nonetheless share ONE freeze_id -- exactly the reader-atomicity break W92-6 describes; "
       "the previous negative suite (15j) only ever tried DIFFERENT freeze pairs and never caught this",
       _race_entry_a_old is not None and _race_entry_b_old is not None
       and _race_entry_a_old["freeze_id"] == _race_entry_b_old["freeze_id"] == "freeze-race"
       and _race_entry_a_old["content"] == {"gen": 0, "x": 1}
       and _race_entry_b_old["content"] == {"gen": 1, "x": 20},
       {"a": _race_entry_a_old, "b": _race_entry_b_old})

# --- 16b. the FIX: resolve_bundle([...]) reads CURRENT exactly once, so a
#     publish landing AT THE EARLIEST POSSIBLE POINT -- as a side effect of
#     that single CURRENT read itself -- still cannot split the call's
#     result across two generations. CURRENT is currently gen16_1 (16a's
#     publish); this simulates the swap to gen16_2 happening the instant
#     resolve_bundle's one _read_current() call fires.
_orig_read_current_reg = reg._read_current
_swap16b_done = [False]


def _read_current_and_swap_16b(registry_dir=None):
    gen_id = _orig_read_current_reg(registry_dir)
    if not _swap16b_done[0]:
        _swap16b_done[0] = True
        prov.publish_generation(_gen16_2["generation_id"], registry_dir=_16_DIR)
    return gen_id


reg._read_current = _read_current_and_swap_16b
try:
    _bundle16b = reg.resolve_bundle(["race_a", "race_b"], registry_dir=_16_DIR)
finally:
    reg._read_current = _orig_read_current_reg
_current16b_after = reg._read_current(registry_dir=_16_DIR)
record("Sol 便92 P92-6 (resolve_bundle immune to the same swap-during-read interleaving): despite the swap to "
       "gen16_2 firing AS A SIDE EFFECT of resolve_bundle's own (single) CURRENT read, the returned bundle is "
       "bound entirely to gen16_1 (the generation that read actually named) -- generation_id matches, and BOTH "
       "race_a/race_b content come from gen16_1 (x=10/x=20), never mixed with gen16_2's x=100/x=200, even "
       "though CURRENT.json now points at gen16_2 on disk by the time this assertion runs",
       _bundle16b is not None
       and _bundle16b["generation_id"] == _gen16_1["generation_id"]
       and _bundle16b["freeze_id"] == "freeze-race"
       and _bundle16b["artifacts"]["race_a"]["content"] == {"gen": 1, "x": 10}
       and _bundle16b["artifacts"]["race_b"]["content"] == {"gen": 1, "x": 20}
       and _current16b_after == _gen16_2["generation_id"],
       {"bundle": _bundle16b, "current_after": _current16b_after})

# --- 16c. the FIX at the CONSUMER layer: `_resolve_native_registry` (the
#     function P92-6 actually asked to be repaired) uses `eu._registry()`'s
#     OWN loaded module instance, not the test's `reg` -- patch THAT
#     instance's _read_current the same way, and confirm the fixed
#     facade's result is likewise bound entirely to gen16_1 (its own
#     CURRENT read, which happens once, before the swap-to-gen16_2 that
#     read's own side effect performs), reaching overall PASS with
#     gen16_1's content only.
prov.publish_generation(_gen16_1["generation_id"], registry_dir=_16_DIR)  # CURRENT back to gen16_1 for a clean run
_eu_reg = eu._registry()
_orig_read_current_eu = _eu_reg._read_current
_swap16c_done = [False]


def _read_current_and_swap_16c(registry_dir=None):
    gen_id = _orig_read_current_eu(registry_dir)
    if not _swap16c_done[0]:
        _swap16c_done[0] = True
        prov.publish_generation(_gen16_2["generation_id"], registry_dir=_16_DIR)
    return gen_id


_race_cert = _synthetic_cert(
    {"artifact_id": "race_a", "digest": eu.sha256_of({"note": "n/a"}), "json_pointer": "/pushforward_map"},
    {"artifact_id": "race_b", "digest": eu.sha256_of({"note": "n/a"}), "json_pointer": "/pushforward_map"},
)
_race_refs = {
    "native_a": {"artifact_id": "race_a", "whole_artifact_digest": _gen16_1["artifacts"]["race_a"],
                 "version_id": "v1", "freeze_id": "freeze-race"},
    "native_b": {"artifact_id": "race_b", "whole_artifact_digest": _gen16_1["artifacts"]["race_b"],
                 "version_id": "v1", "freeze_id": "freeze-race"},
}
_race_raw = {"schema_id": RAW_SCHEMA, "certificate": _race_cert, "native_a": {}, "native_b": {},
             "native_registry_refs": _race_refs}
_prior_env_registry_dir_16 = os.environ.get("NINFTY_EP_REGISTRY_DIR")
os.environ["NINFTY_EP_REGISTRY_DIR"] = _16_DIR
_eu_reg._read_current = _read_current_and_swap_16c
try:
    _race_overall, _race_native_a, _race_native_b, _race_detail = eu._resolve_native_registry(_race_raw)
finally:
    _eu_reg._read_current = _orig_read_current_eu
    if _prior_env_registry_dir_16 is not None:
        os.environ["NINFTY_EP_REGISTRY_DIR"] = _prior_env_registry_dir_16
    else:
        del os.environ["NINFTY_EP_REGISTRY_DIR"]
record("Sol 便92 P92-6 (fixed consumer, _resolve_native_registry, immune to the same swap-during-read "
       "interleaving): overall PASS, and BOTH native_a/native_b content are gen16_1's (x=10/x=20) -- never a "
       "mix with gen16_2's x=100/x=200 -- even though the publish-to-gen16_2 fires as a side effect of the "
       "facade's own single underlying CURRENT read",
       _race_overall == "PASS"
       and _race_native_a == {"gen": 1, "x": 10}
       and _race_native_b == {"gen": 1, "x": 20},
       {"overall": _race_overall, "native_a": _race_native_a, "native_b": _race_native_b, "detail": _race_detail})

_shutil15.rmtree(_16_DIR, ignore_errors=True)


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
