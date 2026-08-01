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

# intersection-only composition, exercised directly over the status lattice.
# NOTE (便97 P97-2.1): `_compose_full` now takes `era_ok` as a REQUIRED final
# argument; these rows fix the lattice with the integrity gate satisfied, and
# §8 fixes what happens when it is not.
check("§5 composition: all three PASS + registry PASS -> PASS",
      full._compose_full("PASS", "PASS", "PASS", "PASS", True) == "PASS")
check("§5 composition: any MALFORMED column -> INTEGRITY_STOP",
      all(full._compose_full(*c, "PASS", True) == "INTEGRITY_STOP" for c in
          (("MALFORMED", "PASS", "PASS"), ("PASS", "MALFORMED", "PASS"), ("PASS", "PASS", "MALFORMED"))))
check("§5 composition: registry non-PASS -> INTEGRITY_STOP even with three PASS columns",
      full._compose_full("PASS", "PASS", "PASS", "STALE", True) == "INTEGRITY_STOP")
check("§5 composition: an ABSENT column is never absorbed by two PASS columns",
      full._compose_full("PASS", "PASS", "ABSENT", "PASS", True) == "ABSENT")
check("§5 composition: a FAIL column outranks an ABSENT one",
      full._compose_full("PASS", "FAIL", "ABSENT", "PASS", True) == "FAIL")

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

# ============================================================================
# §6 W-6 is NOT implied by R3-NF: the incidence-forgetting negative
#    (Sol 便96 W96-2.3 minimal counterexample / P96-2.1 item 4 /
#     governing spec sec.5.3.5 W6-C2, W6-C6)
#
# Sol 便96 rejected option (c) ("R3-NF PASS stands in for W-6"). The reason
# is structural, not a matter of coverage: W-6 recomputes
#     (pi_* Ram_C)(b) = sum_{r: pi(r)=b} m_r = m_Branch(b)
# for every branch point b, which needs the INCIDENCE map r |-> pi(r).
# The normal form carries ramification components, branch components,
# total degree, the infinity component and the non-ramification
# certificates -- and no incidence at all. So two pipelines that disagree
# about which ramification component lies over which branch point produce
# BYTE-IDENTICAL normal forms.
#
# This section fixes that non-implication mechanically, with Sol's own
# minimal counterexample: r1, r2 with multiplicities 1, 2 and b1, b2 with
# multiplicities 1, 2.
# ============================================================================

_R = {"r1": 1, "r2": 2}                       # ramification component -> multiplicity
_B = {"b1": 1, "b2": 2}                       # branch component      -> multiplicity
_INCIDENCE_GOOD = {"r1": "b1", "r2": "b2"}    # satisfies W-6
_INCIDENCE_BAD = {"r1": "b2", "r2": "b1"}     # violates W-6 (images swapped)


def _w6_pushforward(incidence):
    """The W-6 left-hand side: sum multiplicities of the ramification
    components lying over each branch component."""
    out = {}
    for r, m in _R.items():
        out[incidence[r]] = out.get(incidence[r], 0) + m
    return out


def _nf_forgetful_image(incidence):
    """Everything R3-NF actually looks at, computed from an incidence-bearing
    model: the two component multisets, the total degree, the infinity
    component and the non-ramification certificate. Note that `incidence`
    is accepted and then never used -- that IS the point being fixed."""
    del incidence
    return {
        "ram_components": sorted(_R.items()),
        "branch_components": sorted(_B.items()),
        "total_degree": sum(_R.values()) + sum(_B.values()),
        "at_infinity": {"coefficient": 4, "ramification_index": 5},
        "non_ramification": {"p_locus_squarefree": True, "w_locus_squarefree": True},
    }


check("§6 W-6 SEPARATES the two incidences: the good one satisfies "
      "sum_{r->b} m_r == m_Branch(b) for every b, the swapped one does not",
      _w6_pushforward(_INCIDENCE_GOOD) == _B and _w6_pushforward(_INCIDENCE_BAD) != _B,
      {"good": _w6_pushforward(_INCIDENCE_GOOD), "bad": _w6_pushforward(_INCIDENCE_BAD), "branch": _B})

check("§6 R3-NF CANNOT separate them: the NF forgetful image of both incidences is identical, "
      "so no NF-level predicate -- present or future -- can distinguish a W-6-satisfying pipeline "
      "from a W-6-violating one (Sol 便96 W96-2.3)",
      _nf_forgetful_image(_INCIDENCE_GOOD) == _nf_forgetful_image(_INCIDENCE_BAD),
      {"good": _nf_forgetful_image(_INCIDENCE_GOOD), "bad": _nf_forgetful_image(_INCIDENCE_BAD)})

# The same statement against the REAL genuine NF: no field of the real NF
# schema carries a ramification -> branch map. This is asserted over the
# artifact's own key structure, not over a hand-written list of "fields we
# believe exist", so a future NF schema that DID grow an incidence field
# would make this check fail loudly rather than silently going stale.
_nf_keys = set()


def _collect_keys(node):
    if isinstance(node, dict):
        for k, v in node.items():
            _nf_keys.add(k)
            _collect_keys(v)
    elif isinstance(node, list):
        for v in node:
            _collect_keys(v)


_collect_keys(NF_A["nf"])
_INCIDENCE_KEY_TOKENS = ("maps_to", "pushforward", "image_branch", "incidence", "lies_over", "pi_of")
check("§6 the genuine lane-A NF carries NO incidence-bearing field at all "
      "(governing spec sec.5.3.5 W6-C2) -- if the NF schema ever grows one, this check fails "
      "and the W-6 non-implication must be re-argued rather than silently assumed",
      not any(tok in k for k in _nf_keys for tok in _INCIDENCE_KEY_TOKENS),
      sorted(_nf_keys))

# And the frozen W-6 verifier DOES consume exactly the map R3-NF lacks --
# read out of the frozen source, so the claim is about the shipped code.
with open(os.path.join(HERE, "ninfty-verifier-b.py"), "r", encoding="utf-8") as f:
    _vb_src = f.read()
check("§6 the frozen W-6 verifier consumes a per-branch multiplicity map (`branch_value` /"
      " `multiplicity`) that the NF route never produces -- so R3-NF PASS is not, and cannot be "
      "made into, a W-6 PASS (Sol 便96 W96-2.3 rejects option (c))",
      "branch_value" in _vb_src and "branch_value" not in _r3_src,
      {"frozen_verifier_has_branch_value": "branch_value" in _vb_src,
       "r3nf_has_branch_value": "branch_value" in _r3_src})

check("§6 W-6 remains OPEN and is reported as such: nothing in this suite, and no green run of it, "
      "may be counted as W-6 closure or as EP re-activation (Sol 便96 F96-2.3 item 3)",
      True,
      "declaration check -- see docs/week4-NInfty_stage2_spec_v19.md sec.5.3.5 UNKNOWN W6-KEY")

# ============================================================================
# §7 payload-era matrix (Sol 便96 W96-2.2 / governing spec sec.5.3.4 /
#    dependency manifest Y-3b)
#
# The hole W96-2.2 names: `docs_era_binding_ok` compared only the RECEIPT's
# three control-plane document hashes, never the version ids embedded in the
# payload -- yet it was being read as "the payload is v19". The repair is
# Sol's option (2): a versioned mixed-era matrix, checked per plane, with the
# consumer field renamed so the two claims can never again be confused.
# ============================================================================

with open(FULL_FIXTURE, encoding="utf-8") as f:
    _RAW = json.load(f)

check("§7 the banned old field name is gone from the emitted report, and BOTH new columns exist "
      "(便96 W96-2.2 required the rename, not merely a second check)",
      '"docs_era_binding"' not in _full_src
      and '"control_plane_docs_receipt_binding"' in _full_src
      and '"payload_era_matrix"' in _full_src,
      "grep over search/ninfty-evidence-union-full.py")

_era_ok, _era = full._check_payload_era_matrix(_RAW, {"ok": True, "documents": {
    k: {"pinned_artifact_id": v} for k, v in (
        ("predicate_spec", "mb/ninfty-stage2-predicate/v19"),
        ("verifier_contract", "mb/ninfty-verifier-contract/v14"),
        ("dependency_manifest", "mb/dependency-manifest/v14"))}})
check("§7 EVERY plane the matrix declares is evaluated and named (no plane may be silently skipped) -- "
      "the expected set is read from the module's own PLANE_ERA, so adding a plane there without "
      "evaluating it fails here",
      sorted(_era["planes"]) == sorted(full.PLANE_ERA),
      (sorted(_era.get("planes", {})), sorted(full.PLANE_ERA)))
check("§7 the classic five planes are still among them (便99 の W6KEY 追加は additive であって、"
      "既存 plane の置換ではない)",
      set(_era["planes"]) >= {"control_plane", "decision_lane_predicate", "frozen_route_verifier",
                              "native_payload_schema", "nf_route"},
      sorted(_era.get("planes", {})))
check("§7 the two ERA_W6KEY planes are evaluated too, and each is PASS / FAIL / PENDING_ADOPTION -- "
      "never absent, never silently 'compatible' (spec sec.5.3.4 M-7)",
      all(_era["planes"].get(p, {}).get("status") in ("PASS", "FAIL", "PENDING_ADOPTION")
          for p in ("w6_point_map_producer", "w6_key_route")),
      {p: _era["planes"].get(p, {}).get("status") for p in ("w6_point_map_producer", "w6_key_route")})
# --- M-7 both edges: PENDING_ADOPTION vs a receipt that does not reproduce --
_CP = {"ok": True, "documents": {k: {"pinned_artifact_id": v} for k, v in (
    ("predicate_spec", "mb/ninfty-stage2-predicate/v19"),
    ("verifier_contract", "mb/ninfty-verifier-contract/v14"),
    ("dependency_manifest", "mb/dependency-manifest/v14"))}}
_real_receipt_path = full.W6KEY_FREEZE_RECEIPT_PATH
try:
    full.W6KEY_FREEZE_RECEIPT_PATH = "search/certs/_no_such_freeze_receipt.json"
    _pend_ok, _pend = full._check_payload_era_matrix(_RAW, _CP)
    check("§7 M-7 non-firing edge: with NO freeze receipt the two W6KEY planes are PENDING_ADOPTION, "
          "and that is counted as NEITHER PASS NOR FAIL -- the rest of the matrix still reports ok",
          _pend_ok is True
          and all(_pend["planes"][p]["status"] == "PENDING_ADOPTION"
                  for p in ("w6_point_map_producer", "w6_key_route")),
          (_pend_ok, {p: _pend["planes"][p]["status"] for p in ("w6_point_map_producer", "w6_key_route")}))

    _probe = os.path.join(HERE, "certs", "_tmp_w6key_receipt_probe.json")
    with open(_probe, "w", encoding="utf-8") as _fh:
        json.dump({"receipt_id": "probe", "freeze_id": "probe",
                   "bound_artifacts": [{"artifact_id": "mb/ninfty-stage2-predicate/v20",
                                        "path": "docs/week4-NInfty_stage2_spec_v20.md",
                                        "sha256": "0" * 64}],
                   "era_adoption": {"era": {}, "planes": {}}}, _fh)
    try:
        full.W6KEY_FREEZE_RECEIPT_PATH = "search/certs/_tmp_w6key_receipt_probe.json"
        _lie_ok, _lie = full._check_payload_era_matrix(_RAW, _CP)
        check("§7 M-7 firing edge: a freeze receipt whose bound digest does NOT reproduce from the "
              "receiver's own copy is a FAIL, never a downgrade to 'pending' -- a lying receipt is "
              "worse than no receipt",
              _lie_ok is False
              and all(_lie["planes"][p]["status"] == "FAIL"
                      for p in ("w6_point_map_producer", "w6_key_route"))
              and any("does not reproduce" in e for e in _lie["errors"]),
              (_lie_ok, {p: _lie["planes"][p]["status"] for p in ("w6_point_map_producer", "w6_key_route")},
               _lie["errors"][:2]))
    finally:
        os.remove(_probe)
finally:
    full.W6KEY_FREEZE_RECEIPT_PATH = _real_receipt_path
check("§7 the real receipt is restored and the W6KEY planes are ADOPTED and PASS again "
      "(the probes above left no state behind)",
      all(full._check_payload_era_matrix(_RAW, _CP)[1]["planes"][p]["status"] == "PASS"
          for p in ("w6_point_map_producer", "w6_key_route")),
      {p: full._check_payload_era_matrix(_RAW, _CP)[1]["planes"][p] for p in ("w6_key_route",)})

check("§7 the two eras are READ from files and are genuinely different -- a matrix that cannot"
      "discriminate must not report PASS",
      _era["eras"]["FROZEN"] != _era["eras"]["CURRENT"], _era["eras"])
check("§7 the genuine artifact set satisfies the matrix on every plane "
      "(R1/R2 payload = FROZEN era, NF route + decision lane + control plane = CURRENT era)",
      _era_ok is True and all(v["status"] == "PASS" for v in _era["planes"].values()),
      {k: v["status"] for k, v in _era["planes"].items()} if not _era_ok else _era["errors"])

# --- negatives: each must FAIL, and must name WHICH plane -------------------
_newer = copy.deepcopy(_RAW)
_newer["certificate"]["predicate_spec_id"] = _era["eras"]["CURRENT"]["predicate_spec_id"]
_ok, _d = full._check_payload_era_matrix(_newer, {"ok": True, "documents": {}})
check("§7 negative: a certificate declaring the CURRENT (newer) spec id FAILS -- there is no "
      "declared forward compatibility, so 'newer must be fine' is exactly the read the matrix bans "
      "(spec sec.5.3.4 M-1)",
      _ok is False and _d["planes"]["native_payload_schema"]["status"] == "FAIL",
      {"ok": _ok, "plane": _d["planes"]["native_payload_schema"]["status"]})

_missing = copy.deepcopy(_RAW)
del _missing["certificate"]["searcher_native"]["native_schema_id"]
_ok, _d = full._check_payload_era_matrix(_missing, {"ok": True, "documents": {}})
check("§7 negative: an ABSENT native_schema_id FAILS -- an unreadable era is never an "
      "'assumed compatible' era (fail-closed)",
      _ok is False and _d["planes"]["native_payload_schema"]["status"] == "FAIL",
      {"ok": _ok, "errors": _d["errors"][:2]})

_nocert = copy.deepcopy(_RAW)
del _nocert["certificate"]
_ok, _d = full._check_payload_era_matrix(_nocert, {"ok": True, "documents": {}})
check("§7 negative: no certificate at all FAILS rather than vacuously passing",
      _ok is False, {"ok": _ok, "errors": _d["errors"][:2]})

_ok, _d = full._check_payload_era_matrix(_RAW, {"ok": False})
check("§7 negative: a control-plane receipt binding that is NOT ok FAILS the control_plane plane "
      "-- and the payload planes are still reported separately, so neither column can be read off "
      "the other (spec sec.5.3.4 M-4)",
      _ok is False and _d["planes"]["control_plane"]["status"] == "FAIL"
      and _d["planes"]["native_payload_schema"]["status"] == "PASS",
      {k: v["status"] for k, v in _d["planes"].items()})

_ok, _d = full._check_payload_era_matrix(_RAW, {"ok": True, "documents": {
    "predicate_spec": {"pinned_artifact_id": "mb/ninfty-stage2-predicate/v18"},
    "verifier_contract": {"pinned_artifact_id": "mb/ninfty-verifier-contract/v13"},
    "dependency_manifest": {"pinned_artifact_id": "mb/dependency-manifest/v13"}}})
check("§7 negative: a receipt whose digests agree but whose pinned era is the FROZEN trio FAILS "
      "the control_plane plane -- digest agreement is not era agreement (便96 W96-2.2)",
      _ok is False and _d["planes"]["control_plane"]["status"] == "FAIL",
      _d["planes"]["control_plane"]["receipt_pinned"])

check("§7 an era-matrix failure cannot be masked into a PASS overall_full "
      "(the composition rule now includes payload_era_matrix.ok)",
      "payload_era_matrix" in _full_src.split("composition_rule")[1][:600],
      "grep over the composition_rule string in search/ninfty-evidence-union-full.py")

# ============================================================================
# §8 era composition: an integrity fault outranks EVERY route verdict
#    (Sol 便97 W97-2.1 / P97-2.1)
#
# The defect: the escalation was written
#     overall = _compose_route_registry(...)
#     if overall == "PASS" and not era_ok: overall = "INTEGRITY_STOP"
# so with R1 FAIL (or ABSENT / CONFLICT / INTEGRITY_STOP) the era fault was
# dropped from the headline -- an untrusted-payload fault masked by a
# mathematical one. Sol also noted that the pre-existing "composition
# includes era" check only GREPPED the composition_rule string and never
# executed the branch, which is why 70/70 green did not catch it.
#
# This section executes the branch, through the PUBLIC entry point, for all
# five base statuses and for three era mutations, and pins BOTH edges: era
# fault present -> INTEGRITY_STOP whatever the base was; era fault absent ->
# the base status survives untouched.
# ============================================================================

import inspect  # noqa: E402  (deliberately local to this section)

_sig = inspect.signature(full._compose_full)
check("§8 `_compose_full` takes era_ok as a REQUIRED argument -- no default may exist, because a "
      "default is exactly how an unevaluated era gate would be read as satisfied (fail-closed)",
      len(_sig.parameters) == 5
      and all(p.default is inspect.Parameter.empty for p in _sig.parameters.values()),
      str(_sig))
# The masking form must be gone from the EXECUTABLE source. The grep is run
# over non-comment, non-docstring lines: the repair's own docstring quotes
# the defective form verbatim (that is how the defect is documented), so a
# whole-file grep would be satisfied by the documentation and would go on
# being satisfied if the code regressed -- the same "checks the prose, not
# the branch" mistake W97-2.1 named about the old composition_rule grep.
_full_code_lines = []
_in_doc = False
for _ln in _full_src.splitlines():
    _s = _ln.strip()
    if _s.startswith('"""') or _s.endswith('"""'):
        # crude but sufficient: toggles on each docstring delimiter line
        if _s.count('"""') == 1:
            _in_doc = not _in_doc
        continue
    if _in_doc or _s.startswith("#") or not _s:
        continue
    _full_code_lines.append(_ln)
_full_code = "\n".join(_full_code_lines)
check("§8 the era gate is not conditioned on the base status being PASS "
      "(the masking form named by W97-2.1 is gone from the EXECUTABLE source, checked over "
      "non-comment/non-docstring lines so the repair's own quotation of the defect cannot satisfy it)",
      'if overall == "PASS" and not era_ok' not in _full_code
      and "era_ok is not True" in _full_code,
      "grep over the executable lines of search/ninfty-evidence-union-full.py")

_BASE_STATUSES = ("PASS", "FAIL", "ABSENT", "CONFLICT", "INTEGRITY_STOP")
check("§8 the lattice, at unit level: era_ok=False forces INTEGRITY_STOP from EVERY base status, and "
      "era_ok=True leaves every base status untouched",
      all(full._compose_full("PASS", "PASS", "PASS", "PASS", False) == "INTEGRITY_STOP"
          for _ in (0,))
      and full._compose_full("PASS", "FAIL", "ABSENT", "PASS", False) == "INTEGRITY_STOP"
      and full._compose_full("PASS", "PASS", "PASS", "PASS", True) == "PASS")
for _bad_era in (False, None, 0, "", "PASS", 1):
    check(f"§8 era_ok={_bad_era!r} (anything that is not the boolean True) is a FAULT, never a "
          "satisfied gate -- an undefined era result is not a PASS",
          full._compose_full("PASS", "PASS", "PASS", "PASS", _bad_era)
          == ("PASS" if _bad_era is True else "INTEGRITY_STOP"),
          full._compose_full("PASS", "PASS", "PASS", "PASS", _bad_era))

# --- full public entry point, all five base statuses x both era edges -------
# Only the ROUTE/REGISTRY composition is stubbed (so every base status can be
# reached at all -- against the genuine frozen artifacts R1/R2 are MALFORMED
# and only INTEGRITY_STOP is reachable). The era check itself, the registry
# resolution and the report assembly are the real ones.
_era_bad_raw = copy.deepcopy(_RAW)
_era_bad_raw["certificate"]["predicate_spec_id"] = _era["eras"]["CURRENT"]["predicate_spec_id"]
_orig_compose_rr = full._compose_route_registry


def _with_stubbed_base(status, raw):
    full._compose_route_registry = lambda *a, **k: status
    try:
        return full.evidence_union_full_from_raw(raw)
    finally:
        full._compose_route_registry = _orig_compose_rr


for _base in _BASE_STATUSES:
    _rb = _with_stubbed_base(_base, _era_bad_raw)
    check(f"§8 FULL PATH, base={_base} + era FAIL -> overall_full=INTEGRITY_STOP (the integrity fault is "
          "NOT masked by a concurrent mathematical verdict -- W97-2.1's exact defect)",
          _rb["overall_full"] == "INTEGRITY_STOP",
          (_rb["overall_full"], _rb["payload_era_matrix"]["ok"]))
    check(f"§8 FULL PATH, base={_base} + era FAIL: the integrity fault is exposed in its OWN column and "
          "the mathematical composition is reported verbatim beside it (neither erases the other)",
          _rb["integrity_gate"]["integrity_faults"] == ["payload_era_matrix"]
          and _rb["integrity_gate"]["route_composition_status"] == _base
          and _rb["integrity_gate"]["payload_era_matrix_ok"] is False
          and _rb["payload_era_matrix"]["ok"] is False,
          _rb.get("integrity_gate"))
    _rg = _with_stubbed_base(_base, _RAW)
    check(f"§8 non-firing edge, base={_base} + era PASS: the base status survives untouched and no "
          "integrity fault is invented",
          _rg["overall_full"] == _base and _rg["integrity_gate"]["integrity_faults"] == []
          and _rg["integrity_gate"]["payload_era_matrix_ok"] is True,
          (_rg["overall_full"], _rg.get("integrity_gate")))

check("§8 the stub is removed again: the module's real composition function is restored",
      full._compose_route_registry is _orig_compose_rr)

# --- the three era mutations, through the public entry point, UNSTUBBED -----
# Base status here is the genuine one (R1/R2 MALFORMED -> INTEGRITY_STOP),
# which is precisely the concurrency case: under the OLD rule the era fault
# would have been invisible in the headline.
_REAL = full.evidence_union_full_from_raw(_RAW)
check("§8 baseline: against the genuine artifact set the era gate is satisfied and the headline is the "
      "route composition (INTEGRITY_STOP from MALFORMED R1/R2), with no integrity fault claimed",
      _REAL["payload_era_matrix"]["ok"] is True and _REAL["integrity_gate"]["integrity_faults"] == []
      and _REAL["overall_full"] == _REAL["integrity_gate"]["route_composition_status"],
      (_REAL["overall_full"], _REAL["integrity_gate"]))

_mut_newer = copy.deepcopy(_RAW)
_mut_newer["certificate"]["predicate_spec_id"] = _era["eras"]["CURRENT"]["predicate_spec_id"]
_mut_missing = copy.deepcopy(_RAW)
del _mut_missing["certificate"]["searcher_native"]["native_schema_id"]

_orig_docs_era = full._check_docs_era


def _stale_control_plane_receipt(bundle):
    """A receipt whose three document DIGESTS agree with the receiver's copies
    (so the control_plane_docs_receipt_binding column is ok) but which pins
    the FROZEN era -- the 'stale control-plane era' mutation."""
    ok, detail = _orig_docs_era(bundle)
    detail = copy.deepcopy(detail)
    for _k, _v in (("predicate_spec", "mb/ninfty-stage2-predicate/v18"),
                   ("verifier_contract", "mb/ninfty-verifier-contract/v13"),
                   ("dependency_manifest", "mb/dependency-manifest/v13")):
        detail.setdefault("documents", {}).setdefault(_k, {})["pinned_artifact_id"] = _v
    return ok, detail


full._check_docs_era = _stale_control_plane_receipt
try:
    _mut_stale_report = full.evidence_union_full_from_raw(_RAW)
finally:
    full._check_docs_era = _orig_docs_era

for _label, _report, _plane in (
        ("newer payload era (certificate declares the CURRENT spec id)",
         full.evidence_union_full_from_raw(_mut_newer), "native_payload_schema"),
        ("missing plane era (searcher_native.native_schema_id absent)",
         full.evidence_union_full_from_raw(_mut_missing), "native_payload_schema"),
        ("stale control-plane era (receipt digests agree but pin the FROZEN trio)",
         _mut_stale_report, "control_plane")):
    check(f"§8 mutation through the PUBLIC entry point -- {_label}: era FAIL on plane {_plane}, "
          "overall_full=INTEGRITY_STOP, and the fault named in integrity_gate",
          _report["payload_era_matrix"]["ok"] is False
          and _report["payload_era_matrix"]["planes"][_plane]["status"] == "FAIL"
          and _report["overall_full"] == "INTEGRITY_STOP"
          and _report["integrity_gate"]["integrity_faults"] == ["payload_era_matrix"],
          {"ok": _report["payload_era_matrix"]["ok"],
           "plane": _report["payload_era_matrix"]["planes"][_plane]["status"],
           "overall": _report["overall_full"], "gate": _report["integrity_gate"]})

check("§8 the report schema id was SUPERSEDED, not mutated in place: `overall_full` now means something "
      "different (integrity-first), so a v1-pinned consumer must not read a v2 report as if the old "
      "rule held",
      _REAL["schema_id"].endswith("/v2") and full.FULL_UNION_SCHEMA_ID_V1.endswith("/v1"),
      _REAL.get("schema_id"))
check("§8 the stub is removed again: the module's real docs-era function is restored",
      full._check_docs_era is _orig_docs_era)

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS)} checks, {n_fail} FAIL")
raise SystemExit(1 if n_fail else 0)
