#!/usr/bin/env python
# search/probe/sg_band_sweep/merge_chir2_v1.py
# Merges the 5 per-window JSON files produced by scratchpad/run_chir2_v1.sh
# (+ retry scripts) into the single CHIR-2 cert. Concatenation + prediction
# aggregation only -- no group theory recomputed here.
import json, glob, hashlib

WINDOW_GLOB = "scratchpad/chir2_window_*.json"
OUT = "search/certs/sg_chir2_20260806.json"

LAYER3 = {(1944, 826), (1944, 921)}
LAYER2 = {(1296, 2889), (1296, 3487), (1728, 31096)}

def main():
    windows = []
    for path in sorted(glob.glob(WINDOW_GLOB)):
        d = json.load(open(path, encoding="utf-8"))
        windows.append(d)

    rows = []
    for w in windows:
        key = (w["order"], w["id"])
        layer = "3" if key in LAYER3 else ("2" if key in LAYER2 else "?")
        row = dict(w)
        row["layer"] = layer
        rows.append(row)
    rows.sort(key=lambda r: (r["layer"], r["order"], r["id"]))

    layer3_rows = [r for r in rows if r["layer"] == "3"]
    layer2_rows = [r for r in rows if r["layer"] == "2"]

    # primary prediction: dim_H2 >= 2 for BOTH layer-3 windows
    dim_h2_ge2_all = all(r.get("dim_H2_ge2") is True for r in layer3_rows) if len(layer3_rows) == 2 else None
    # secondary: eigenvector_lift_exists == False for both layer-3 windows (FRAT-CHIR)
    eigvec_false_all = all(r.get("eigenvector_lift_exists") is False for r in layer3_rows) if len(layer3_rows) == 2 else None
    # canaries
    canary_a_all = all(r.get("canary_a_nonsplit") is True for r in layer3_rows) if len(layer3_rows) == 2 else None
    canary_b_all = all(r.get("canary_b_arith") is True for r in rows)
    canary_c_note = "not applicable to this driver (only invoked for the 5 non-isolated windows); the 31 isolated (X=1) windows are handled by CHIR-1, not CHIR-2"

    selfSha = hashlib.sha256(open("search/probe/sg_band_sweep/sg_chir2_single_window_v1.g", "rb").read()).hexdigest()
    noteSha = hashlib.sha256(open("docs/notes/theorem_check_mirrorall_l3vacuous_v1.md", "rb").read()).hexdigest()

    merged = {
        "schema": "shadow-atelier/sg-chir2/v1",
        "driver_self_sha256": selfSha,
        "design_doc": {"path": "docs/notes/theorem_check_mirrorall_l3vacuous_v1.md", "sha256": noteSha},
        "authority": "裁定696 (司令塔), CHIR-2 per SSG.11.3 実測指示書 (verbatim, 数学者起草)",
        "architecture_note": "1 gap.ps1 process per window, external `timeout 120` cap (scratchpad/run_chir2_v1.sh + targeted retries), same architecture as CHIR-1 v2. 4 bugs found and fixed during this run (all disclosed inline in sg_chir2_single_window_v1.g comments): (1) CHR requires a PERMUTATION group; (2) CHR requires the fp-presentation's generators to match GeneratorsOfGroup(G) exactly; (3) AutomorphismGroup(R) (order 648) was the real reflexibility-test bottleneck, replaced by a direct bijective-homomorphism test; (4) the exhaustive [eps]-identification IdGroup loop was lightened with an AbelianInvariants pre-filter + IdGroup(Ghat) caching + a hard 6-call cap (disclosed via eps_identification_capped when hit).",
        "windows_total": 5,
        "windows_ok": len([r for r in rows if r["status"] == "OK"]),
        "rows": rows,
        "predictions": {
            "primary_dim_H2_ge2_both_layer3": {"holds": dim_h2_ge2_all,
                "values": [{"order": r["order"], "id": r["id"], "dim_H2": r.get("dim_H2")} for r in layer3_rows]},
            "secondary_eigenvector_lift_false_both_layer3_FRAT_CHIR": {"holds": eigvec_false_all,
                "values": [{"order": r["order"], "id": r["id"], "eigenvector_lift_exists": r.get("eigenvector_lift_exists")} for r in layer3_rows]},
        },
        "canaries": {
            "a_nonsplit_layer3": {"holds_both": canary_a_all},
            "b_arithmetic_all_windows": {"holds_all": canary_b_all},
            "c_note": canary_c_note,
        },
        "layer2_comparison_note": "SSG.11.3's own disclosed caveat: the (R,chi,H^2) framework may not directly apply to layer-2 the same way (X not <= Phi(P) there). Observed: (1296,2889) X=[27,3] non-abelian -- module framework skipped honestly (not computed). (1296,3487)/(1728,31096) X=C3xC3 abelian, dim=2, dim_H2=0 (SPLIT extension, canary_a_nonsplit=False -- consistent, since NONSPLIT lemma's hypothesis X<=Phi(P) is specific to layer-3 and does NOT hold for these layer-2 windows), eigenvector_lift_exists=False observed but not predicted/scored (comparison data only, per the note's own framing).",
        "claims": {"frat_chir_status": "candidate/single-system (per SSG.11.3/【GAP-G11-1】 -- the eigenvector_lift_exists test as implemented tests lifting MOD X exactly (U->U*x1,W->W^-1*x2), which per 【GAP-G11-1】's own disclosure is NOT strictly identical to full reflexibility of Ghat (a residual Z^1(R,X) torsor adjustment is not resolved here); reported honestly as the note's own acknowledged open gap, not closed by this measurement", "grading_deferred_to": "司令塔/数学者"},
        "non_contact_declaration": {"im_R": False, "d_N": False, "sealed_quantities": False, "n5_series": False},
    }

    blob = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(blob)
    print("Wrote", OUT)
    print("windows_ok=", merged["windows_ok"], "/", merged["windows_total"])
    print("primary dim_H2>=2 (both layer-3):", dim_h2_ge2_all, merged["predictions"]["primary_dim_H2_ge2_both_layer3"]["values"])
    print("secondary eigenvector_lift=False (both layer-3, FRAT-CHIR):", eigvec_false_all)
    print("canary a (nonsplit, layer-3):", canary_a_all)
    print("canary b (arithmetic, all):", canary_b_all)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("sha256=", sha)

if __name__ == "__main__":
    main()
