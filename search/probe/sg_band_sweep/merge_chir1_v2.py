#!/usr/bin/env python
# search/probe/sg_band_sweep/merge_chir1_v2.py
# Merges the 36 per-window JSON files produced by
# scratchpad/run_chir1_v2.sh (one gap.ps1 process per window, hard 120s
# external timeout per window via GNU `timeout` -- 司令塔 intervention
# instruction②/③, root cause fixed via
# sg_chir1_single_window_v2.g's Reidemeister-Schreier-via-spanning-tree
# method, instruction④) into the single CHIR-1 cert. Concatenation +
# canary/prediction aggregation only -- no group theory recomputed here.
import json, glob, hashlib, sys, os

WINDOW_GLOB = "scratchpad/chir1_window_*.json"
STATUS_FILE = "scratchpad/chir1_v2_status.txt"
G4G5_CERT = "search/certs/sg_g4_g5_orb_20260806.json"
OUT = "search/certs/sg_chir1_20260806.json"

EXPECTED_36 = [
    (1944, 826), (1944, 921), (1296, 2889), (1296, 3487), (1728, 31096),
    (1458, 573), (1458, 578), (1458, 583), (1458, 584), (1458, 658), (1458, 659),
    (1944, 812), (1944, 815), (1944, 835), (1944, 901), (1944, 904), (1944, 918), (1944, 3878), (1944, 3882),
    (1296, 674), (1296, 681), (1296, 755), (1296, 764), (1296, 3082),
    (1728, 2815), (1728, 2892), (1728, 30092), (1728, 30101), (1728, 30106),
    (1152, 154124), (1152, 154126), (1152, 154158), (1152, 154161), (1152, 155452), (1152, 155454), (1152, 155457),
]

def is_power_of_3(n):
    while n % 3 == 0:
        n //= 3
    return n == 1

def main():
    g4g5 = json.load(open(G4G5_CERT, encoding="utf-8"))
    class_by_key = {(r["order"], r["id"]): r["classification"] for r in g4g5["g5_classification"]}

    windows_by_key = {}
    for path in glob.glob(WINDOW_GLOB):
        d = json.load(open(path, encoding="utf-8"))
        windows_by_key[(d["order"], d["id"])] = d

    # status log (COMPLETED / TIMEOUT_SKIPPED / COMPUTE_FAILED) for windows
    # that never produced a JSON (timeout/failure) -- read the status file
    status_lines = {}
    if os.path.exists(STATUS_FILE):
        for line in open(STATUS_FILE, encoding="utf-8"):
            parts = line.split()
            if len(parts) >= 3:
                status_lines[(int(parts[1]), int(parts[2]))] = parts[0]

    rows = []
    canary_fails = []
    timeout_skipped = []
    compute_failed = []
    missing = []

    for order, wid in EXPECTED_36:
        key = (order, wid)
        classification = class_by_key.get(key, "UNKNOWN")
        is_chiral = (classification == "single_mirror_pair_non_exotic")
        w = windows_by_key.get(key)
        if w is None:
            st = status_lines.get(key, "MISSING")
            if st == "TIMEOUT_SKIPPED":
                timeout_skipped.append({"order": order, "id": wid, "reason": "wall_cap_120s_exceeded"})
                rows.append({"order": order, "id": wid, "classification": classification,
                             "is_chiral": is_chiral, "status": "TIMEOUT_SKIPPED"})
            elif st == "COMPUTE_FAILED":
                compute_failed.append({"order": order, "id": wid})
                rows.append({"order": order, "id": wid, "classification": classification,
                             "is_chiral": is_chiral, "status": "COMPUTE_FAILED"})
            else:
                missing.append({"order": order, "id": wid})
                rows.append({"order": order, "id": wid, "classification": classification,
                             "is_chiral": is_chiral, "status": "MISSING"})
            continue

        if w["status"] != "OK":
            rows.append({"order": order, "id": wid, "classification": classification,
                         "is_chiral": is_chiral, "status": w["status"]})
            continue

        kappa = w["kappa"]
        row = {
            "order": order, "id": wid, "classification": classification, "is_chiral": is_chiral,
            "status": "OK", "method": w["method"], "wall_ms": w["wall_ms"], "num_relators": w["num_relators"],
            "kappa": kappa, "kappa_mirror": w["kappa_mirror"], "id_X": w["id_X"],
            "X_abelian": w["X_abelian"], "X_in_center": w["X_in_center"],
            "X_in_frattini": w["X_in_frattini"], "X_in_derived": w["X_in_derived"],
            "X_excluded_family": w["X_excluded_family"], "X_excluded_family_name": w["X_excluded_family_name"],
            "canary_C3_ok": w["canary_C3_ok"], "canary_C4_ok": w["canary_C4_ok"], "canary_C5_ok": w["canary_C5_ok"],
            "covered_chief_factors": w["covered_chief_factors"],
        }
        rows.append(row)

        # C1/C2
        if not is_chiral and kappa != 1:
            canary_fails.append({"order": order, "id": wid, "canary": "C1", "note": f"reflexible but kappa={kappa}"})
        if is_chiral and kappa == 1:
            canary_fails.append({"order": order, "id": wid, "canary": "C2", "note": "chiral but kappa=1"})
        if not w["canary_C3_ok"]:
            canary_fails.append({"order": order, "id": wid, "canary": "C3", "note": "kappa does not divide |Ghat|"})
        if not w["canary_C4_ok"]:
            canary_fails.append({"order": order, "id": wid, "canary": "C4", "note": f"kappa={kappa} kappa_mirror={w['kappa_mirror']}"})
        if not w["canary_C5_ok"]:
            canary_fails.append({"order": order, "id": wid, "canary": "C5", "note": "P/X not reflexible"})
        if w["X_excluded_family"]:
            canary_fails.append({"order": order, "id": wid, "canary": "C6", "note": f"X matches excluded family {w['X_excluded_family_name']}"})

    ok_rows = [r for r in rows if r["status"] == "OK"]
    chiral_ok = [r for r in ok_rows if r["is_chiral"]]
    refl_ok = [r for r in ok_rows if not r["is_chiral"]]

    # P-CHIR-1: 5 chiral groups all have kappa a power of 3
    pchir1_rows = [{"order": r["order"], "id": r["id"], "kappa": r["kappa"], "is_pow3": is_power_of_3(r["kappa"])} for r in chiral_ok]
    pchir1_holds = all(x["is_pow3"] for x in pchir1_rows) if pchir1_rows else None

    # P-CHIR-2: layer-3 windows (1944,826),(1944,921) -- X<=Z(P) or fallback X<=Phi(P)
    layer3_keys = {(1944, 826), (1944, 921)}
    pchir2_rows = []
    for r in ok_rows:
        if (r["order"], r["id"]) in layer3_keys:
            pchir2_rows.append({"order": r["order"], "id": r["id"], "kappa": r["kappa"],
                                 "X_in_center": r["X_in_center"], "X_in_frattini": r["X_in_frattini"]})

    # P-CHIR-3: layer-2 windows (SECT-broken) -- X covers the broken 3^2 factor
    layer2_keys = {(1296, 2889), (1296, 3487), (1728, 31096)}
    pchir3_rows = []
    for r in ok_rows:
        if (r["order"], r["id"]) in layer2_keys:
            for f in r["covered_chief_factors"]:
                if f["order"] == 9 and not f["sect_holds"]:
                    pchir3_rows.append({"order": r["order"], "id": r["id"], "factor_index": f["index"], "covers": f["covers"]})

    # P-CHIR-4: kappa(layer3) <= 9
    pchir4_rows = [{"order": r["order"], "id": r["id"], "kappa": r["kappa"], "le9": r["kappa"] <= 9} for r in pchir2_rows]

    selfSha = hashlib.sha256(open("search/probe/sg_band_sweep/sg_chir1_single_window_v2.g", "rb").read()).hexdigest()
    noteSha = hashlib.sha256(open("docs/notes/theorem_check_mirrorall_l3vacuous_v1.md", "rb").read()).hexdigest()
    inputCertSha = hashlib.sha256(open(G4G5_CERT, "rb").read()).hexdigest()

    merged = {
        "schema": "shadow-atelier/sg-chir1/v2",
        "note_v2": "v2: 司令塔 intervention (実地確認 (1458,658) stuck 32min on fp-presentation combinatorial blowup). Root-cause fix: IsomorphismFpGroupByGenerators (coset-enumeration-based) REPLACED with a Reidemeister-Schreier-via-spanning-tree construction (O(|Ghat|^2), never calls coset enumeration) for ALL 36 windows, not just a fallback. Architecture: ONE gap.ps1 process PER WINDOW, hard 120s wall-clock cap enforced externally via GNU `timeout` (a single synchronous GAP process cannot preempt its own blocking calls). Execution order: 5 chiral windows FIRST, then 31 reflexible (canary/control) windows.",
        "driver_self_sha256": selfSha,
        "design_doc": {"path": "docs/notes/theorem_check_mirrorall_l3vacuous_v1.md", "sha256": noteSha},
        "input_cert": {"path": G4G5_CERT, "sha256": inputCertSha},
        "authority": "裁定686 (司令塔), CHIR-1 per SSG.10.2 (verbatim, PIN-CHIR-1 corrected: C5 citation = BJNS SS1 p.3 + SS3 preamble p.6); v2 architecture per 司令塔's intervention instruction (実地確認 stall)",
        "windows_total": 36,
        "windows_ok": len(ok_rows),
        "timeout_skipped": timeout_skipped,
        "compute_failed": compute_failed,
        "missing": missing,
        "canary_fails": canary_fails,
        "rows": rows,
        "predictions": {
            "P_CHIR_1": {"rows": pchir1_rows, "holds_for_all_5_chiral": pchir1_holds},
            "P_CHIR_2": {"rows": pchir2_rows},
            "P_CHIR_3": {"rows": pchir3_rows},
            "P_CHIR_4": {"rows": pchir4_rows},
        },
        "claims": {"chirality_group_status": "candidate/single-system (per SSG.10.7)", "grading_deferred_to": "司令塔/数学者"},
        "non_contact_declaration": {"im_R": False, "d_N": False, "sealed_quantities": False, "n5_series": False},
    }

    blob = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(blob)
    print("Wrote", OUT)
    print("windows_ok=", len(ok_rows), "timeout_skipped=", len(timeout_skipped),
          "compute_failed=", len(compute_failed), "missing=", len(missing))
    print("canary_fails=", len(canary_fails))
    for cf in canary_fails:
        print("  ", cf)
    print("P-CHIR-1 holds for all 5 chiral:", pchir1_holds, pchir1_rows)
    print("P-CHIR-2 layer-3 rows:", pchir2_rows)
    print("P-CHIR-3 layer-2 rows:", pchir3_rows)
    print("P-CHIR-4 layer-3 kappa<=9:", pchir4_rows)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("sha256=", sha)

if __name__ == "__main__":
    main()
