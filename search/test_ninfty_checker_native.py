#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/test_ninfty_checker_native.py

Self-made test suite for search/ninfty-checker-native.py (the from-scratch
checker_native point-level construction, commander's brief 2026-08-01,
裁定305 gap closure) and its wiring into search/ninfty-checker.py.

Normal-system cases: the three genuine positive fixtures
(search/fixtures/ninfty/checker_pos_0{1,2,3}.json), each satisfying T-1
(rootpart(a)=[2,2,1]) by construction.

Degenerate-system cases:
  * a with a genuine TRIPLE root (Pell necessarily fails first -- this IS
    the real behavior, checked explicitly, not assumed).
  * gcd(a,a') of degree != 2 (the real beta candidate,
    search/certs/ep_first_run/beta_candidate.json -- stage1-pass-only,
    a-partition-mismatch).
  * degree mismatch (deg a/p/f6 wrong).
  * a Pell-violating (a,p,f6) triple.
  * a genuine positive candidate with f6's constant term perturbed (breaks
    the Pell identity -- exercises pell-not-nonzero-constant on
    near-genuine data, not just obviously-wrong toy data).

Run: python search/test_ninfty_checker_native.py
Exits 0 iff all checks PASS.
"""
import importlib.util
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
FIXDIR = os.path.join(HERE, "fixtures", "ninfty")

RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append((name, ok, detail))


def _load_module(name, relpath):
    path = os.path.join(HERE, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


nat = _load_module("ninfty_checker_native", "ninfty-checker-native.py")
chk = _load_module("ninfty_checker", "ninfty-checker.py")


def load_fixture(fname):
    with open(os.path.join(FIXDIR, fname), "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# 1. Normal system: the three genuine [2,2,1] positive fixtures.
# --------------------------------------------------------------------------
for fname in ["checker_pos_01.json", "checker_pos_02.json", "checker_pos_03.json"]:
    cand = load_fixture(fname)
    res = nat.construct_checker_native(cand["a"], cand["p"], cand["f6"])
    record(f"{fname}: status == ok", res["status"] == "ok", res.get("status"))
    if res["status"] != "ok":
        continue

    total_mult = sum(e["multiplicity"] for e in res["ramification_divisor_on_C"])
    record(f"{fname}: total ramification multiplicity == 12 (RH bookkeeping, T-7)",
           total_mult == 12, str(total_mult))

    n_finite = sum(1 for e in res["ramification_divisor_on_C"] if e["kind"] == "finite")
    n_infinity = sum(1 for e in res["ramification_divisor_on_C"] if e["kind"] == "infinity")
    record(f"{fname}: exactly 4 finite ramification points (2 roots x 2 branches)",
           n_finite == 4, str(n_finite))
    record(f"{fname}: exactly 2 infinity ramification points",
           n_infinity == 2, str(n_infinity))

    record(f"{fname}: orientation_derivation matches (Or) hypothesis "
           "(order -5 pole / +5 zero at the two infinity points)",
           res["orientation_derivation"]["matches_Or_hypothesis"] is True,
           json.dumps(res["orientation_derivation"]))

    record(f"{fname}: finite_aggregate_partitions == [2,2,1] for both finite branch values",
           all(v == [2, 2, 1] for v in res["finite_aggregate_partitions"].values()),
           json.dumps(res["finite_aggregate_partitions"]))

    record(f"{fname}: branch_divisor_on_P1 has exactly 4 entries "
           "({0, infinity, s, -s})",
           len(res["branch_divisor_on_P1"]) == 4, json.dumps(res["branch_divisor_on_P1"]))

    bmap = {b["branch_value"]: b["multiplicity"] for b in res["branch_divisor_on_P1"]}
    record(f"{fname}: branch multiplicities are exactly {{4,4,2,2}} as a multiset",
           sorted(bmap.values()) == [2, 2, 4, 4], json.dumps(bmap))

    # every constructed finite point must actually satisfy y^2=f6(x) and
    # mu(x,y)=branch_value -- re-derived independently here (this test does
    # not trust construct_checker_native's own internal guard blindly).
    a_expr = nat.poly_from_coeffs(cand["a"])
    p_expr = nat.poly_from_coeffs(cand["p"])
    f6_expr = nat.poly_from_coeffs(cand["f6"])
    all_on_curve = True
    all_mu_correct = True
    for e in res["ramification_divisor_on_C"]:
        if e["kind"] != "finite":
            continue
        xv = sp.sympify(e["x_srepr"])
        yv = sp.sympify(e["y_srepr"])
        bv = sp.sympify(e["maps_to_branch_value"])
        if sp.simplify(yv ** 2 - f6_expr.subs(nat.X, xv)) != 0:
            all_on_curve = False
        if sp.simplify(a_expr.subs(nat.X, xv) + p_expr.subs(nat.X, xv) * yv - bv) != 0:
            all_mu_correct = False
    record(f"{fname}: independently re-verified finite points lie on y^2=f6(x)",
           all_on_curve, "")
    record(f"{fname}: independently re-verified mu(point) == declared branch value",
           all_mu_correct, "")

    # self-consistency: pushforward sums (via ninfty-checker.py's own
    # check_native_pushforward) must match.
    ok, detail = chk.check_native_pushforward(res)
    record(f"{fname}: check_native_pushforward(self-constructed native) == True",
           ok is True, json.dumps(detail))

# native_artifact_digest must be a stable function of the artifact content
# (recomputing twice on the same candidate gives the same digest).
cand1 = load_fixture("checker_pos_01.json")
r1 = nat.construct_checker_native(cand1["a"], cand1["p"], cand1["f6"])
r2 = nat.construct_checker_native(cand1["a"], cand1["p"], cand1["f6"])
record("checker_pos_01.json: native_artifact_digest is deterministic across repeated runs",
       r1["native_artifact_digest"] == r2["native_artifact_digest"],
       f"{r1['native_artifact_digest']} vs {r2['native_artifact_digest']}")


# --------------------------------------------------------------------------
# 2. Wiring into search/ninfty-checker.py's run_checker().
# --------------------------------------------------------------------------
for fname in ["checker_pos_01.json", "checker_pos_02.json", "checker_pos_03.json"]:
    cand = load_fixture(fname)
    result = chk.run_checker(cand)
    record(f"{fname} via run_checker(): native_construction.status == ok",
           result.get("native_construction", {}).get("status") == "ok",
           str(result.get("native_construction", {}).get("status")))
    record(f"{fname} via run_checker(): native_construction_self_pushforward_check.ok == True",
           result.get("native_construction_self_pushforward_check", {}).get("ok") is True,
           json.dumps(result.get("native_construction_self_pushforward_check")))
    record(f"{fname} via run_checker(): T-1/T-2/rootpart core stage unaffected (still None)",
           result["stage"] is None, str(result["stage"]))

# opt-out flag must actually skip native construction (no sympy path touched).
cand_skip = dict(load_fixture("checker_pos_01.json"))
cand_skip["skip_native_construction"] = True
result_skip = chk.run_checker(cand_skip)
record("checker_pos_01.json + skip_native_construction=true: no native_construction key present",
       "native_construction" not in result_skip, str(list(result_skip.keys())))


# --------------------------------------------------------------------------
# 3. Degenerate system cases.
# --------------------------------------------------------------------------

# 3a. Real degenerate data: the beta candidate (stage1-pass-only,
# a-partition-mismatch -- gcd(a,a') has degree 1, not 2).
beta = load_fixture(os.path.join("..", "certs", "ep_first_run", "beta_candidate.json")) \
    if os.path.exists(os.path.join(FIXDIR, "..", "certs", "ep_first_run", "beta_candidate.json")) \
    else None
beta_path = os.path.join(HERE, "certs", "ep_first_run", "beta_candidate.json")
with open(beta_path, "r", encoding="utf-8") as f:
    beta = json.load(f)
res_beta = nat.construct_checker_native(beta["a"], beta["p"], beta["f6"])
record("beta_candidate.json (real stage1-pass-only degenerate data): "
       "status == gcd-degree-not-2 (no crash, honest degeneracy report)",
       res_beta["status"] == "gcd-degree-not-2", str(res_beta["status"]))

# 3b. Degree mismatch.
res_deg = nat.construct_checker_native(["1", "1"], ["1", "1"], ["1", "1", "1"])
record("degree-mismatch candidate: status == degree-mismatch (no crash)",
       res_deg["status"] == "degree-mismatch", str(res_deg["status"]))

# 3c. Genuine triple root of a (Pell necessarily fails first on
# arbitrary p/f6 -- checked explicitly as the actual observed behavior).
x = sp.symbols("x")
a_triple = sp.expand((x + 1) ** 3 * (x + 2) * (x + 3))
a_triple_coeffs = [str(sp.Rational(c)) for c in sp.Poly(a_triple, x).all_coeffs()[::-1]]
res_triple = nat.construct_checker_native(a_triple_coeffs, ["1", "0", "1"],
                                           ["1", "0", "0", "0", "0", "0", "1"])
record("triple-root-of-a candidate (arbitrary unrelated p,f6): "
       "status == pell-not-nonzero-constant (Pell guard fires first, no crash)",
       res_triple["status"] == "pell-not-nonzero-constant", str(res_triple["status"]))

# 3d. A genuine positive candidate with f6 perturbed just enough to break
# the Pell identity (near-genuine data, not obviously-wrong toy data).
cand_perturbed = load_fixture("checker_pos_01.json")
wrong_f6 = list(cand_perturbed["f6"])
wrong_f6[0] = str(sp.Rational(wrong_f6[0]) + 1)
res_pert = nat.construct_checker_native(cand_perturbed["a"], cand_perturbed["p"], wrong_f6)
record("checker_pos_01.json with f6 constant-term perturbed by +1: "
       "status == pell-not-nonzero-constant (no crash, no silent wrong construction)",
       res_pert["status"] == "pell-not-nonzero-constant", str(res_pert["status"]))

# 3e. run_checker() must not crash when native construction hits a
# degeneracy internally raised as an exception path (defensive: feed a
# candidate whose a/p/f6 keys are present but degenerate at the native
# layer while still passing T-1/T-2 upstream is not constructible by
# design -- T-1 passing implies gcd degree 2, so this exercises the
# internal-error catch-all defensively via a monkeypatched failure).
class _BoomModule:
    @staticmethod
    def construct_checker_native(*a, **kw):
        raise RuntimeError("synthetic failure (test-only)")


_orig_loader = chk._load_native_module
chk._NATIVE_MODULE = _BoomModule
result_boom = chk.run_checker(load_fixture("checker_pos_01.json"))
record("run_checker(): a synthetic native-construction exception is caught, "
       "not propagated (native_construction.status == internal-error)",
       result_boom.get("native_construction", {}).get("status") == "internal-error",
       json.dumps(result_boom.get("native_construction")))
record("run_checker(): T-1/T-2 core stage is UNAFFECTED by a native-construction crash",
       result_boom["stage"] is None, str(result_boom["stage"]))
chk._NATIVE_MODULE = None  # restore for any later use in this process


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
n_pass = sum(1 for _, ok, _ in RESULTS if ok)
n_total = len(RESULTS)
for name, ok, detail in RESULTS:
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  {detail}" if (not ok and detail) else ""))
print(f"\n{n_pass}/{n_total} checks passed.")
sys.exit(0 if n_pass == n_total else 1)
