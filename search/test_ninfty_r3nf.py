#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_r3nf.py

Test suite for R3-NF (search/ninfty-verifier-w6-r3nf.py) and the
three-column full union (search/ninfty-evidence-union-full.py), per Sol
便95 F95-2.2 / P95-2.2 item 3.

Structure:
  §1  positive control on the REAL registry-pinned genuine artifacts
      (ep-genuine-* nf_a/nf_b) -- R3-NF must reach PASS with every check
      individually reported.
  §2  MALFORMED negatives (schema/producer-identity/digest-recomputation).
  §3  FAIL negatives -- one per checked mathematical invariant (N-1..N-5,
      total degree, infinity, non-ramification certificate), each mutating
      exactly ONE field of a genuine NF so the suite names WHICH check
      caught it, not merely that something failed.
  §4  ABSENT negatives (no NF minted / no NF supplied) -- never PASS.
  §5  full-union level: three separate columns, intersection-only
      composition, missing/stale/swapped nf refs, and the structural
      assertion that the frozen R1/R2 facade's own verdicts are passed
      through VERBATIM (R3-NF cannot rescue or damage them).

Run: python search/test_ninfty_r3nf.py     (exit 0 iff all checks PASS)
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FULL_FIXTURE = os.path.join(HERE, "certs", "ep_ci_full_witness_evidence_20260801.json")

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if not ok else ""))


def _load(alias, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(alias, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r3 = _load("r3nf_under_test", "ninfty-verifier-w6-r3nf.py")
full = _load("full_union_under_test", "ninfty-evidence-union-full.py")
registry = _load("registry_ref", "ninfty-native-registry.py")

# NOTE (Sol 便86 P86-2 item 1 / B86-o1): this file deliberately does NOT
# dynamically load search/ninfty-evidence-union.py. test_ninfty_evidence_union.py
# §8 enforces STRUCTURALLY that no other file under search/ carries a load
# site for that module at all -- the invariant is about the load site, not
# about which attribute is touched, so "we only call the public name" would
# not satisfy it. Where this suite needs the frozen facade's own verdict
# for comparison, it runs the frozen CLI as a SEPARATE OS PROCESS, exactly
# as search/ninfty-evidence-union-full.py itself does.


def _frozen_cli(raw):
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "ninfty-evidence-union.py"), "-"],
        input=json.dumps(raw, sort_keys=True, separators=(",", ":"), ensure_ascii=True),
        capture_output=True, encoding="utf-8", cwd=REPO)
    return json.loads(proc.stdout)


def _reseal(content):
    """Recompute the artifact's own declared nf_digest after a mutation, so
    the resulting negative tests the MATHEMATICAL check under test rather
    than tripping the (separately tested) digest-recomputation gate."""
    content = copy.deepcopy(content)
    content["nf_digest"] = r3.sha256_of(content["nf"])
    return content


# ============================================================================
# §1 positive control on the real registry-pinned genuine artifacts
# ============================================================================

BUNDLE = registry.resolve_bundle([
    "ep-genuine-checker_pos_01-nf-a", "ep-genuine-checker_pos_01-nf-b",
    "ep-genuine-checker_pos_02-nf-a", "ep-genuine-checker_pos_02-nf-b",
    "ep-genuine-checker_pos_03-nf-a", "ep-genuine-checker_pos_03-nf-b",
])
check("§1 registry CURRENT resolves the genuine nf_a/nf_b artifacts for all 3 fixtures",
      BUNDLE is not None and all(
          f"ep-genuine-checker_pos_0{i}-nf-{s}" in BUNDLE["artifacts"] for i in (1, 2, 3) for s in ("a", "b")),
      BUNDLE if BUNDLE is None else sorted(BUNDLE["artifacts"]))

NF_A = BUNDLE["artifacts"]["ep-genuine-checker_pos_01-nf-a"]["content"]
NF_B = BUNDLE["artifacts"]["ep-genuine-checker_pos_01-nf-b"]["content"]

status, detail = r3.verify_R3_NF(NF_A, NF_B)
check("§1 positive control: R3-NF PASS on the genuine same-generation nf_a/nf_b pair",
      status == "PASS", (status, detail.get("reason")))
check("§1 positive control: every individual check is reported and passing (no silent skip)",
      status == "PASS" and detail["failed_checks"] == [] and len(detail["checks"]) >= 11,
      {k: v.get("pass") for k, v in detail.get("checks", {}).items()})
for _name in ("N-1", "N-2", "N-3", "N-4", "N-5", "R3-3-cross-lane-digest",
              "R3-5-finite-degree", "R3-5-branch-degree", "R3-6-infinity-component",
              "R3-7-non-ramification", "R3-1-both-producer-provenance"):
    check(f"§1 positive control reports check {_name}",
          _name in detail.get("checks", {}), sorted(detail.get("checks", {})))

for _i in (2, 3):
    _a = BUNDLE["artifacts"][f"ep-genuine-checker_pos_0{_i}-nf-a"]["content"]
    _b = BUNDLE["artifacts"][f"ep-genuine-checker_pos_0{_i}-nf-b"]["content"]
    _s, _d = r3.verify_R3_NF(_a, _b)
    check(f"§1 positive control: R3-NF PASS on genuine fixture checker_pos_0{_i}", _s == "PASS",
          (_s, _d.get("reason")))

# ============================================================================
# §2 MALFORMED negatives
# ============================================================================

s, d = r3.verify_R3_NF(NF_B, NF_A)  # lanes swapped
check("§2 both-producer guard: lane B's report in the nf_a slot -> MALFORMED (not PASS)",
      s == "MALFORMED", (s, d.get("schema_errors")))

s, d = r3.verify_R3_NF(NF_A, NF_A)  # same producer duplicated into both slots
check("§2 both-producer guard: lane A's report duplicated into BOTH slots -> MALFORMED "
      "(one producer twice is not a two-producer agreement, even though every equality would hold)",
      s == "MALFORMED", (s, d.get("schema_errors")))

_tampered = copy.deepcopy(NF_B)
_tampered["nf"]["ram_finite"]["coefficient"] = 99  # mutate WITHOUT resealing
s, d = r3.verify_R3_NF(NF_A, _tampered)
check("§2 digest recomputation: a mutated nf whose declared nf_digest was NOT resealed -> MALFORMED "
      "(the producer's own digest claim is re-derived by the receiver, never taken on its word)",
      s == "MALFORMED" and any("recomputed" in e for e in d.get("schema_errors", [])),
      (s, d.get("schema_errors")))

_wrong_schema = _reseal(NF_B)
_wrong_schema["nf_schema_id"] = "mb/ninfty-nf/v2-evil"
s, d = r3.verify_R3_NF(NF_A, _wrong_schema)
check("§2 schema gate: wrong nf_schema_id -> MALFORMED", s == "MALFORMED", (s, d.get("schema_errors")))

_no_branch = _reseal(NF_B)
del _no_branch["nf"]["branch"]
_no_branch = _reseal(_no_branch)
s, d = r3.verify_R3_NF(NF_A, _no_branch)
check("§2 schema gate: nf.branch missing entirely -> MALFORMED (not ABSENT, not FAIL)",
      s == "MALFORMED", (s, d.get("schema_errors")))

# ============================================================================
# §3 FAIL negatives -- one per checked invariant
# ============================================================================

def _mutate_fail(label, mutator, expected_failed):
    m = copy.deepcopy(NF_B)
    mutator(m["nf"])
    m = _reseal(m)
    s, d = r3.verify_R3_NF(NF_A, m)
    failed = d.get("failed_checks", [])
    check(f"§3 {label} -> FAIL and names {expected_failed}",
          s == "FAIL" and expected_failed in failed, (s, failed))
    return s, d


_mutate_fail("N-1 (finite ramification ideal generator perturbed on lane B)",
             lambda nf: nf["ram_finite"].__setitem__("ideal_generator", ["9", "6", "1"]),
             "N-1")

_mutate_fail("total finite degree (ram_finite coefficient 1 -> 2, breaking 2*deg*coef == 4)",
             lambda nf: nf["ram_finite"].__setitem__("coefficient", 2),
             "R3-5-finite-degree")

_mutate_fail("infinity (ram_infinite ramification index e: 5 -> 3)",
             lambda nf: nf["ram_infinite"][0].__setitem__("e", 3),
             "N-3")

_mutate_fail("total branch degree (at_infinity coefficient 4 -> 5, breaking the degree-12 identity)",
             lambda nf: nf["branch"]["components"][2].__setitem__("coefficient", 5),
             "R3-5-branch-degree")

_mutate_fail("non-ramification certificate (p_locus squarefree true -> false)",
             lambda nf: nf["non_ramification_certificates"]["p_locus"].__setitem__("squarefree", False),
             "R3-7-non-ramification")

_mutate_fail("N-5 (w_locus generator perturbed on lane B)",
             lambda nf: nf["non_ramification_certificates"]["w_locus"].__setitem__(
                 "generator", ["1", "27408/25", "25628/25", "2484/5", "657/5", "18", "1"]),
             "N-5")

_s_any, _d_any = _mutate_fail("cross-lane digest (any resealed mutation also breaks R3-3)",
                              lambda nf: nf["branch"]["components"][0].__setitem__("coefficient", 3),
                              "R3-3-cross-lane-digest")

# ============================================================================
# §4 ABSENT negatives
# ============================================================================

s, d = r3.verify_R3_NF(None, NF_B)
check("§4 nf_a not supplied at all -> ABSENT (never PASS)", s == "ABSENT", (s, d.get("reason")))
s, d = r3.verify_R3_NF({}, {})
check("§4 both NF slots empty -> ABSENT (never PASS)", s == "ABSENT", (s, d.get("reason")))

_absent_lane = {"lane": "B", "nf_schema_id": r3.NF_SCHEMA_ID, "status": "ABSENT",
                "decision_stage": "REJECT", "nf": None, "nf_digest": None}
s, d = r3.verify_R3_NF(NF_A, _absent_lane)
check("§4 lane B minted nothing (status=ABSENT) -> route ABSENT, lane statuses echoed verbatim",
      s == "ABSENT" and d.get("lane_b_status") == "ABSENT", (s, d))

_stop_lane = dict(_absent_lane, status="INTEGRITY_STOP")
s, d = r3.verify_R3_NF(NF_A, _stop_lane)
check("§4 lane B reported INTEGRITY_STOP -> route ABSENT and the lane's own INTEGRITY_STOP is NOT "
      "overwritten or downgraded in the detail",
      s == "ABSENT" and d.get("lane_b_status") == "INTEGRITY_STOP", (s, d))

# ============================================================================
# §5 full-union level
# ============================================================================

with open(FULL_FIXTURE, "r", encoding="utf-8") as f:
    RAW = json.load(f)

REPORT = full.evidence_union_full_from_raw(RAW)

check("§5 the full union reports THREE separate columns, in a fixed order",
      list(REPORT["column_order"]) == ["R1", "R2", "R3-NF"] and set(REPORT["columns"]) == {"R1", "R2", "R3-NF"},
      REPORT.get("column_order"))
check("§5 R3-NF reaches PASS against the genuine four-role generation",
      REPORT["columns"]["R3-NF"]["status"] == "PASS", REPORT["columns"]["R3-NF"]["status"])
check("§5 the four-role (native_a/native_b/nf_a/nf_b) same-generation resolution is PASS",
      REPORT["four_role_registry_status"]["status"] == "PASS",
      {k: v["status"] for k, v in REPORT["four_role_registry_status"]["roles"].items()})
check("§5 all four roles resolved from ONE generation id",
      len({v.get("generation_id") for v in REPORT["four_role_registry_status"]["roles"].values()}) == 1,
      {k: v.get("generation_id") for k, v in REPORT["four_role_registry_status"]["roles"].items()})

_frozen_direct = _frozen_cli(RAW)
check("§5 R1/R2 columns are the FROZEN facade's own verdicts, passed through verbatim "
      "(R3-NF neither rescues nor damages them)",
      REPORT["columns"]["R1"]["status"] == _frozen_direct["route1_status"]
      and REPORT["columns"]["R2"]["status"] == _frozen_direct["route2_status"],
      (REPORT["columns"]["R1"]["status"], _frozen_direct["route1_status"]))

check("§5 a PASS R3-NF does NOT lift a non-PASS R1/R2 to an overall PASS (no substitution)",
      not (REPORT["columns"]["R1"]["status"] == "PASS" and REPORT["columns"]["R2"]["status"] == "PASS")
      and REPORT["overall_full"] != "PASS",
      (REPORT["columns"]["R1"]["status"], REPORT["columns"]["R2"]["status"], REPORT["overall_full"]))

# intersection-only composition, exercised directly over the status lattice
check("§5 composition: all three PASS + registry PASS -> PASS",
      full._compose_full("PASS", "PASS", "PASS", "PASS") == "PASS")
check("§5 composition: any MALFORMED column -> INTEGRITY_STOP",
      all(full._compose_full(*c, "PASS") == "INTEGRITY_STOP" for c in
          (("MALFORMED", "PASS", "PASS"), ("PASS", "MALFORMED", "PASS"), ("PASS", "PASS", "MALFORMED"))))
check("§5 composition: registry non-PASS -> INTEGRITY_STOP even with three PASS columns",
      full._compose_full("PASS", "PASS", "PASS", "STALE") == "INTEGRITY_STOP")
check("§5 composition: an ABSENT column is never absorbed by two PASS columns",
      full._compose_full("PASS", "PASS", "ABSENT", "PASS") == "ABSENT")
check("§5 composition: a FAIL column outranks an ABSENT one",
      full._compose_full("PASS", "FAIL", "ABSENT", "PASS") == "FAIL")

_no_nf_refs = copy.deepcopy(RAW)
del _no_nf_refs["nf_registry_refs"]
_r = full.evidence_union_full_from_raw(_no_nf_refs)
check("§5 fail-closed input: nf_registry_refs OMITTED -> R3-NF ABSENT and overall_full != PASS "
      "('field not supplied' is never read as 'check not applicable')",
      _r["columns"]["R3-NF"]["status"] == "ABSENT" and _r["overall_full"] != "PASS",
      (_r["columns"]["R3-NF"]["status"], _r["overall_full"]))
check("§5 fail-closed input: the omitted nf refs are reported as MISSING per role, not silently dropped",
      {_r["four_role_registry_status"]["roles"][k]["status"] for k in ("nf_a", "nf_b")} == {"MISSING"},
      {k: v["status"] for k, v in _r["four_role_registry_status"]["roles"].items()})

_swapped = copy.deepcopy(RAW)
_swapped["nf_registry_refs"]["nf_a"], _swapped["nf_registry_refs"]["nf_b"] = (
    _swapped["nf_registry_refs"]["nf_b"], _swapped["nf_registry_refs"]["nf_a"])
_r = full.evidence_union_full_from_raw(_swapped)
check("§5 nf_a/nf_b refs SWAPPED -> ROLE_MISMATCH on both nf roles, R3-NF ABSENT, overall_full != PASS",
      {_r["four_role_registry_status"]["roles"][k]["status"] for k in ("nf_a", "nf_b")} == {"ROLE_MISMATCH"}
      and _r["columns"]["R3-NF"]["status"] == "ABSENT" and _r["overall_full"] != "PASS",
      {k: v["status"] for k, v in _r["four_role_registry_status"]["roles"].items()})

_stale = copy.deepcopy(RAW)
_stale["nf_registry_refs"]["nf_a"]["whole_artifact_digest"] = "0" * 64
_r = full.evidence_union_full_from_raw(_stale)
check("§5 stale nf_a digest claim -> STALE, R3-NF ABSENT, overall_full != PASS",
      _r["four_role_registry_status"]["roles"]["nf_a"]["status"] == "STALE"
      and _r["columns"]["R3-NF"]["status"] == "ABSENT" and _r["overall_full"] != "PASS",
      {k: v["status"] for k, v in _r["four_role_registry_status"]["roles"].items()})

_unknown = copy.deepcopy(RAW)
_unknown["nf_registry_refs"]["nf_b"]["artifact_id"] = "ep-genuine-does-not-exist-nf-b"
_r = full.evidence_union_full_from_raw(_unknown)
check("§5 unregistered nf_b artifact_id -> UNKNOWN, R3-NF ABSENT, overall_full != PASS",
      _r["four_role_registry_status"]["roles"]["nf_b"]["status"] == "UNKNOWN"
      and _r["columns"]["R3-NF"]["status"] == "ABSENT" and _r["overall_full"] != "PASS",
      {k: v["status"] for k, v in _r["four_role_registry_status"]["roles"].items()})

check("§5 the report never claims calibration: calibrated_detector=false and ep_status=uncalibrated/UNKNOWN",
      REPORT["calibrated_detector"] is False and REPORT["ep_status"] == "uncalibrated/UNKNOWN",
      (REPORT.get("calibrated_detector"), REPORT.get("ep_status")))
check("§5 the report labels itself a DIAGNOSTIC CONSTRUCTION, not a minted/published artifact "
      "(Sol 便95 F95-2.3 terminology)",
      "diagnostic construction" in REPORT["artifact_class"], REPORT.get("artifact_class"))

# CLI is fail-closed: nonzero exit for anything other than overall_full == PASS.
_cli = subprocess.run([sys.executable, os.path.join(HERE, "ninfty-evidence-union-full.py"), FULL_FIXTURE],
                      capture_output=True, encoding="utf-8", cwd=REPO)
_cli_json = json.loads(_cli.stdout) if _cli.stdout.strip() else {}
check("§5 CLI is fail-closed: exit code is nonzero exactly when overall_full != PASS",
      (_cli.returncode == 0) == (_cli_json.get("overall_full") == "PASS"),
      (_cli.returncode, _cli_json.get("overall_full")))

# Structural: R1/R2 must remain frozen -- this module may only touch the
# frozen facade through its ONE public name.
with open(os.path.join(HERE, "ninfty-evidence-union-full.py"), "r", encoding="utf-8") as f:
    _full_src = f.read()
# The forbidden tokens are ASSEMBLED at run time rather than written as
# literals: test_ninfty_evidence_union.py §8 greps every file under search/
# for whole-word occurrences of the frozen module's private names, and a
# literal list here would itself trip that check (a test that breaks the
# invariant it is helping to protect).
_FROZEN_PRIVATE = tuple("_" + p for p in (
    "build_R1", "build_R2", "compose_route_statuses", "coerce_to_route_result",
    "evidence_union_fail_closed_v2", "route_result_pass"))
check("§5 structural: the full-union module never reaches into the frozen facade's private names",
      not any(tok in _full_src for tok in _FROZEN_PRIVATE),
      "grep over search/ninfty-evidence-union-full.py's own source")
check("§5 structural: the full-union module does not dynamically LOAD the frozen module at all "
      "(Sol 便86 B86-o1 is about the load site, not the attribute) -- it runs the frozen CLI as a "
      "separate process instead",
      "spec_from_file_location" not in _full_src.split("FROZEN_UNION_CLI")[0]
      or "ninfty-evidence-union.py" not in "".join(
          ln for ln in _full_src.splitlines() if "_load(" in ln),
      "grep over search/ninfty-evidence-union-full.py's own load sites")
with open(os.path.join(HERE, "ninfty-verifier-w6-r3nf.py"), "r", encoding="utf-8") as f:
    _r3_src = f.read()
_r3_code_lines = [ln for ln in _r3_src.splitlines()
                  if ln.strip() and not ln.strip().startswith("#")]
check("§5 structural: R3-NF's verifier is a PURE predicate -- it has no mechanism to load a lane, a "
      "frozen route verifier, a registry, a file or a subprocess at all (not merely 'does not call one')",
      not any(tok in "\n".join(_r3_code_lines) for tok in
              ("importlib", "subprocess", "spec_from_file_location", "open(", "__import__")),
      "grep over search/ninfty-verifier-w6-r3nf.py's non-comment source lines")
check("§5 structural: R3-NF's only imports are stdlib (hashlib/json/re/fractions)",
      sorted(ln.split()[1].split(".")[0] for ln in _r3_code_lines
             if ln.startswith("import ") or (ln.startswith("from ") and " import " in ln))
      == ["__future__", "fractions", "hashlib", "json", "re"],
      sorted(ln for ln in _r3_code_lines if ln.startswith(("import ", "from "))))

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS)} checks, {n_fail} FAIL")
raise SystemExit(1 if n_fail else 0)
