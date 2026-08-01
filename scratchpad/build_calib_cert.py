import importlib.util, json, os, hashlib, subprocess, sys, datetime

ROOT = "C:/Users/81905/Desktop/shadow-atelier"
SEARCH = os.path.join(ROOT, "search")

def load_module(name, relpath):
    path = os.path.join(SEARCH, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

nat = load_module("ninfty_checker_native", "ninfty-checker-native.py")
chk = load_module("ninfty_checker", "ninfty-checker.py")

def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

points = []

# 1. the 3 genuine positive fixtures
for fname in ["checker_pos_01.json", "checker_pos_02.json", "checker_pos_03.json"]:
    path = os.path.join(SEARCH, "fixtures", "ninfty", fname)
    cand = load_json(path)
    res = nat.construct_checker_native(cand["a"], cand["p"], cand["f6"])
    points.append({
        "source": f"search/fixtures/ninfty/{fname}",
        "source_sha256": sha256_file(path),
        "kind": "genuine-positive-2-2-1-fixture",
        "construction_status": res["status"],
        "total_ramification_multiplicity": (
            sum(e["multiplicity"] for e in res["ramification_divisor_on_C"])
            if res["status"] == "ok" else None
        ),
        "matches_Or_hypothesis": (
            res["orientation_derivation"]["matches_Or_hypothesis"] if res["status"] == "ok" else None
        ),
        "native_artifact_digest": res.get("native_artifact_digest"),
        "full_result": res,
    })

# 2. beta candidate (real EP stage1-pass, a-partition-mismatch)
beta_path = os.path.join(SEARCH, "certs", "ep_first_run", "beta_candidate.json")
beta = load_json(beta_path)
res_beta = nat.construct_checker_native(beta["a"], beta["p"], beta["f6"])
points.append({
    "source": "search/certs/ep_first_run/beta_candidate.json",
    "source_sha256": sha256_file(beta_path),
    "kind": "real-stage1-pass-degenerate (a-partition-mismatch, lane A REJECT)",
    "construction_status": res_beta["status"],
    "full_result": res_beta,
})

# 3. two more machine-extracted stage1-pass points (own Pell-division re-derivation)
extract_out = subprocess.run([sys.executable, os.path.join(ROOT, "scratchpad", "extract_more_points.py")],
                              capture_output=True, text=True, cwd=ROOT)
assert extract_out.returncode == 0, extract_out.stderr
extracted = json.loads(extract_out.stdout)
for item in extracted["results"]:
    cand = item["candidate"]
    res = nat.construct_checker_native(cand["a"], cand["p"], cand["f6"])
    points.append({
        "source": "certificates/mb/ninfty-branch-search-bound3.json (own independent Pell-division re-derivation, index %d)" % item["source_index_in_stage1_pass_details"],
        "source_sha256": extracted["source_cert_sha256"],
        "extraction_rule": extracted["extraction_rule"],
        "kind": "machine-extracted-stage1-pass",
        "construction_status": res["status"],
        "full_result": res,
    })

# crosscheck report (separate script, reads lane A's real output artifact)
crosscheck = subprocess.run([sys.executable, os.path.join(SEARCH, "checker_native_crosscheck.py")],
                             capture_output=True, text=True, cwd=ROOT)
assert crosscheck.returncode == 0, crosscheck.stderr
crosscheck_report = json.loads(crosscheck.stdout)

# regression + new-suite results
def run_suite(relpath):
    r = subprocess.run([sys.executable, os.path.join(SEARCH, relpath)], capture_output=True, text=True, cwd=ROOT)
    last_line = [l for l in r.stdout.splitlines() if l.strip()][-1] if r.stdout.strip() else ""
    return {"returncode": r.returncode, "summary_line": last_line}

suite_results = {
    "test_ninfty_checker_native.py (new)": run_suite("test_ninfty_checker_native.py"),
    "test_ninfty_laneB.py (regression)": run_suite("test_ninfty_laneB.py"),
    "test_ninfty_evidence_union.py (regression)": run_suite("test_ninfty_evidence_union.py"),
    "test_ninfty_legacy_normalizer.py (regression)": run_suite("test_ninfty_legacy_normalizer.py"),
}

cert = {
    "schema": "shadow-atelier/checker-native-calib/v1",
    "role": "checker_native (lane B independent native construction) calibration cert -- commander's brief 2026-08-01, 裁定305 EP gap closure",
    "generated_by": "scratchpad/build_calib_cert.py (machine-piped, run this session)",
    "generated_at_utc": datetime.datetime.utcnow().isoformat() + "Z",
    "files": {
        "search/ninfty-checker-native.py": sha256_file(os.path.join(SEARCH, "ninfty-checker-native.py")),
        "search/ninfty-checker.py": sha256_file(os.path.join(SEARCH, "ninfty-checker.py")),
        "search/checker_native_crosscheck.py": sha256_file(os.path.join(SEARCH, "checker_native_crosscheck.py")),
        "search/test_ninfty_checker_native.py": sha256_file(os.path.join(SEARCH, "test_ninfty_checker_native.py")),
    },
    "calibration_points": points,
    "crosscheck_against_lane_a_real_output": crosscheck_report,
    "suite_results": suite_results,
}

out_path = os.path.join(SEARCH, "certs", "checker_native_calib_20260801.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cert, f, indent=2, sort_keys=True, ensure_ascii=True)
print("wrote", out_path)
print(json.dumps(suite_results, indent=2))
