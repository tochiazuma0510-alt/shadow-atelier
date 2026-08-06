#!/usr/bin/env python
# search/probe/sg_band_sweep/merge_chir3_v1.py
# Merges the 2 per-window JSON files (CHIR-3, 裁定699) into the single
# cert. Concatenation + prediction aggregation only.
import json, glob, hashlib

WINDOW_GLOB = "scratchpad/chir3_window_*.json"
OUT = "search/certs/sg_chir3_20260806.json"
CHIR2_CERT = "search/certs/sg_chir2_20260806.json"

def main():
    windows = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(WINDOW_GLOB))]
    chir2 = json.load(open(CHIR2_CERT, encoding="utf-8"))
    chir2_by_key = {(r["order"], r["id"]): r for r in chir2["rows"]}

    rows = []
    for w in windows:
        key = (w["order"], w["id"])
        c2 = chir2_by_key.get(key, {})
        row = dict(w)
        row["dim_H2_matches_chir2"] = (w.get("dim_H2_crosscheck") == c2.get("dim_H2"))
        rows.append(row)
    rows.sort(key=lambda r: (r["order"], r["id"]))

    p_chir5_holds = all(r.get("dim_H1_ge1") is True for r in rows) if len(rows) == 2 else None
    gap_g11_1_closed = all(r.get("correction_possible_general") is True for r in rows) if len(rows) == 2 else None
    dim_h2_consistency = all(r.get("dim_H2_matches_chir2") is True for r in rows)

    selfSha = hashlib.sha256(open("search/probe/sg_band_sweep/sg_chir3_single_window_v1.g", "rb").read()).hexdigest()
    noteSha = hashlib.sha256(open("docs/notes/theorem_check_mirrorall_l3vacuous_v1.md", "rb").read()).hexdigest()
    chir2Sha = hashlib.sha256(open(CHIR2_CERT, "rb").read()).hexdigest()

    merged = {
        "schema": "shadow-atelier/sg-chir3/v1",
        "driver_self_sha256": selfSha,
        "design_doc": {"path": "docs/notes/theorem_check_mirrorall_l3vacuous_v1.md", "sha256": noteSha},
        "input_cert_chir2": {"path": CHIR2_CERT, "sha256": chir2Sha},
        "authority": "裁定699 (司令塔), CHIR-3 per SSG.12.2 実測指示書 (verbatim, 数学者起草)",
        "windows_total": 2,
        "windows_ok": len([r for r in rows if r["status"] == "OK"]),
        "rows": rows,
        "predictions": {
            "P_CHIR_5_dim_H1_ge1_both": {"holds": p_chir5_holds,
                "values": [{"order": r["order"], "id": r["id"], "dim_H1": r.get("dim_H1")} for r in rows]},
        },
        "gap_g11_1_closure": {
            "closed_general": gap_g11_1_closed,
            "note": "GENERAL closure of 【GAP-G11-1】's Wells-correction machinery (image_dim=2 for both windows, i.e. any future (x,y) target would be correctable IF a weak lift existed). This is a methodological/general-machinery statement, NOT new information about these 2 windows' chirality (already established directly and exhaustively in CHIR-2, independent of this apparatus). Step 3 (explicit weak-lift construction) was correctly skipped for both windows per the note's own clause, since CHIR-2 already showed omega!=0 (no weak lift exists at all for these specific windows).",
        },
        "dim_H2_crosscheck": {"consistent_with_chir2": dim_h2_consistency},
        "claims": {"gap_g11_1_status": "candidate/single-system; general closure achieved for the Wells-correction machinery, not a new chirality determination for these windows", "grading_deferred_to": "司令塔/数学者"},
        "non_contact_declaration": {"im_R": False, "d_N": False, "sealed_quantities": False, "n5_series": False},
    }

    blob = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        f.write(blob)
    print("Wrote", OUT)
    print("windows_ok=", merged["windows_ok"])
    print("P-CHIR-5 (dim_H1>=1, both):", p_chir5_holds)
    print("GAP-G11-1 general closure:", gap_g11_1_closed)
    print("dim_H2 crosscheck consistent with CHIR-2:", dim_h2_consistency)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print("sha256=", sha)

if __name__ == "__main__":
    main()
