#!/usr/bin/env python3
"""Assemble the final B-HUNT J0-J2 certificate from:
  - scratchpad/bhunt_j0_output.json (J0 join, python, streamed from existing
    lane S/V/P artifacts -- zero new window computation)
  - scratchpad/bhunt_j1j2_gap_output.json (J1' Phi measurement + J2 C
    identification, GAP, group computation in the SAME P as the main-run
    lanes -- built via predicate_lib_laneS.g / candidate_key_lib.g)

Determines the BH-5 branch per docs/notes/bhunt_prereg_iffirst_v1.md Sec 6.
Writes search/certs/bhunt_j0j2_20260806.json.

Per the prereg's own rule (Sec 6.2/6.3), if branch BH-gamma fires, the cert
still records the full result, but summary text must not headline it as a
"discovery" -- that governs the *report*, not this cert (the cert always
records the true machine result).
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main():
    j0 = json.load(open(ROOT / "scratchpad/bhunt_j0_output.json", encoding="utf-8"))
    gap = json.load(open(ROOT / "scratchpad/bhunt_j1j2_gap_output.json", encoding="utf-8"))

    # ---- registration ledger check (Sec 9): prereg note must be a standalone commit ----
    prereg_path = "docs/notes/bhunt_prereg_iffirst_v1.md"
    prereg_commit = git("log", "--follow", "--format=%H", "--", prereg_path).splitlines()[-1]
    files_in_commit = git("show", "--name-only", "--format=", prereg_commit).splitlines()
    files_in_commit = [f for f in files_in_commit if f.strip()]
    prereg_standalone = (files_in_commit == [prereg_path])
    prereg_sha256 = sha256_of(ROOT / prereg_path)

    head_commit = git("rev-parse", "HEAD")

    # ---- BH-5 branch determination ----
    # BH-delta: registration falsified (BH-3 uniqueness violated, or layer
    # counts != 7, or |H_W| != 42). Already gated inside bhunt_j1j2.g
    # (branch_delta_bh3_uniqueness_violated) and inside the J0 join (all 6
    # layers checked to equal 7 by construction of pent_per_layer_counts).
    layer_counts = j0["pent_per_layer_counts"]
    layers_all_seven = all(v == 7 for v in layer_counts.values())
    h_w_total = j0["pent_total"]
    h_w_is_42 = (h_w_total == 42)
    bh3_unique = (gap["c_hits_count"] == 1)

    branch_delta = (not layers_all_seven) or (not h_w_is_42) or (not bh3_unique)
    phi_invariant = gap["phi_invariant"]
    branch_gamma = (not branch_delta) and (not phi_invariant)
    branch_open_alpha_beta = (not branch_delta) and phi_invariant

    if branch_delta:
        branch_resolved = "BH-delta"
        branch_note = ("PREREGISTRATION_FALSIFIED: layers_all_seven=%s h_w_is_42=%s "
                        "bh3_unique=%s" % (layers_all_seven, h_w_is_42, bh3_unique))
    elif branch_gamma:
        branch_resolved = "BH-gamma"
        branch_note = ("Phi(L) != L. |G_ar|=6 forced (BH-5). B-type candidates=36. "
                        "EXTERNAL_CONSISTENCY_ALARM/HOLD per prereg Sec 6.2 -- "
                        "not to be reported as a discovery until the 4-point "
                        "consistency check (Sec 6.2) is independently run.")
    else:
        branch_resolved = "BH-alpha/BH-beta-open"
        branch_note = ("Phi(L) = L (L = L_3, PL-GAP-1 closed via addendum A's "
                        "equivalence). |G_ar| in {6,42} remains undetermined -- "
                        "the residual 1 bit is Thm BH-4's "
                        "Ih_N(G_{Q(mu_7)}) != 1 question, which lies outside the "
                        "window (J3, literature-gated, BH-GAP-1 OPEN). C (the "
                        "explicit order-6 subgroup through anchor c) is "
                        "identified regardless of this bit (J2, BH-3).")

    cert = {
        "schema": "bhunt-j0j2-cert/v1",
        "date": "2026-08-06",
        "class_id": "B-HUNT",
        "commit_sha": head_commit,
        "iffirst_registry": {
            "prereg_path": prereg_path,
            "prereg_sha256": prereg_sha256,
            "prereg_standalone_commit_sha": prereg_commit,
            "prereg_standalone_commit_files": files_in_commit,
            "prereg_standalone_commit_verified": prereg_standalone,
        },
        "constraints_honored": {
            "no_705894_rerun": True,
            "note_705894": ("J0 reads lane S/V join_manifest.json (705,894 records "
                             "each) and lane P join_manifest.json (117,649 records) "
                             "as PRE-EXISTING artifacts only (streamed, not "
                             "recomputed). No hexagon/PENT predicate was "
                             "re-evaluated on any of the 705,894 or 117,649 "
                             "candidates in this run."),
            "sealed_three_quantities_noncontact": True,
            "sealed_quantities_excluded": ["u_9/a_9 (K^(5) campaign)", "Im R_{N,K^(5)}",
                                           "d_N", "genuine-layer u value (K^(5) campaign)"],
            "no_subdivision_used": True,
            "artifacts_unmodified": True,
        },
        "J0_join": {
            "description": ("Post-hoc join of pre-collected lane S (hexagon, "
                             "layered) / V (independent hexagon lane) / P (PENT, "
                             "layer-independent) PASS sets, realizing all 42 "
                             "candidate keys. Zero new window computation. This "
                             "upgrades the main-run cert's layer-uniform "
                             "extrapolation (42 = 6*7, previously stated as "
                             "extrapolated for m!=0) to a direct measurement."),
            "provenance": j0["provenance"],
            "xn_ordered": j0["xn_ordered"],
            "s_pass_per_layer_counts": j0["s_pass_per_layer_counts"],
            "v_pass_per_layer_counts": j0["v_pass_per_layer_counts"],
            "s_v_mismatch_count": j0["s_v_mismatch_count"],
            "p_pass_global_count": j0["p_pass_global_count"],
            "pent_per_layer_counts": j0["pent_per_layer_counts"],
            "pent_total": j0["pent_total"],
            "pent_all_keys": j0["pent_all"],
        },
        "J1_L": {
            "description": "L = ker(D|_A) = pent(0), realized via J0 join.",
            "L_evecs": j0["L_m0"],
            "L_count": j0["L_m0_count"],
        },
        "J1prime_Phi": {
            "description": ("Phi = E_{m0,f0}|_{gamma3(P)} measured in P (same "
                             "group object as main-run lanes, built via "
                             "predicate_lib_laneS.g + candidate_key_lib.g "
                             "BasisFromP). m0=1 (generating layer, u0=2*1+1=3, "
                             "a generator of (Z/7)^x). f0 = first element of "
                             "pent(m0=1) (any hexagon representative of that "
                             "layer suffices for conjugation; f0 need not "
                             "itself satisfy PENT)."),
            "m0": gap["m0"],
            "L_closed_subgroup_check": gap["L_closed_subgroup"],
            "phi_well_defined": gap["phi_well_defined"],
            "phi_bijective": gap["phi_bijective"],
            "phi_images": gap["phi_images"],
            "phi_invariant_Phi_L_equals_L": gap["phi_invariant"],
        },
        "J2_C": {
            "description": ("Search among the 7 elements of pent(m0=1) for the "
                             "unique g=[m0,f0c] with g^3 = c = [6,1] (BH-3). "
                             "Composition law (2405 (2.6)/2401 (3.43)): "
                             "[m1,f1] o [m2,f2] = [2 m1 m2+m1+m2, f1 E_{m1,f1}(f2)]."),
            "m1_of_square": gap["m1"],
            "m3_raw": gap["m3_raw"],
            "m3_mod7": gap["m3_mod7"],
            "anchor_c": {"m": gap["anchor_c_m"], "e": gap["anchor_c_e"]},
            "c_candidates": gap["c_candidates"],
            "c_hits_count": gap["c_hits_count"],
            "C_generator": {
                "m0": gap["m0"],
                "f0_e": next(c["f0_e"] for c in gap["c_candidates"] if c["cube_f_equals_c"]),
            } if gap["c_hits_count"] == 1 else None,
            "BH3_uniqueness_confirmed": bh3_unique,
        },
        "BH5_branch": {
            "layers_all_seven": layers_all_seven,
            "h_w_total": h_w_total,
            "h_w_is_42": h_w_is_42,
            "bh3_unique": bh3_unique,
            "phi_invariant": phi_invariant,
            "branch_delta_falsified": branch_delta,
            "branch_gamma_fired": branch_gamma,
            "branch_resolved": branch_resolved,
            "note": branch_note,
        },
        "grading": {
            "measured_vs_framework_relative": ("J0/J1/J1prime/J2 are MEASURED "
                                                "(machine, this run). They sit "
                                                "on top of the framework-relative "
                                                "paper-proof-candidate lemmas "
                                                "SUP-1..4/BH-1..5 (Sol unaudited)."),
            "cross_checked": False,
            "verified": False,
            "novelty_claimed": False,
        },
        "tooling": {
            "j0_join_script": {"path": "scratchpad/bhunt_j0_join.py",
                                "sha256": sha256_of(ROOT / "scratchpad/bhunt_j0_join.py")},
            "gap_input_generator": {"path": "scratchpad/bhunt_gen_gap_input.py",
                                     "sha256": sha256_of(ROOT / "scratchpad/bhunt_gen_gap_input.py")},
            "gap_input_file": {"path": "scratchpad/bhunt_j0_input.g",
                                "sha256": sha256_of(ROOT / "scratchpad/bhunt_j0_input.g")},
            "gap_script": {"path": "scratchpad/bhunt_j1j2.g",
                            "sha256": sha256_of(ROOT / "scratchpad/bhunt_j1j2.g")},
            "gap_driver": {"path": "scratchpad/bhunt_j1j2_driver.g",
                            "sha256": sha256_of(ROOT / "scratchpad/bhunt_j1j2_driver.g")},
            "gap_output": {"path": "scratchpad/bhunt_j1j2_gap_output.json",
                            "sha256": sha256_of(ROOT / "scratchpad/bhunt_j1j2_gap_output.json")},
            "gap_group_construction": ("search/probe/hsp7_mainrun/predicate_lib_laneS.g "
                                        "+ search/probe/hsp7_mainrun/candidate_key_lib.g "
                                        "(byte-identical to the main-run lane wrappers' "
                                        "group construction; P built via ANUPQ from "
                                        "search/probe/hsp7_cond4_laneS/PQ_OUTPUT_P.g)"),
        },
    }

    out_path = ROOT / "search/certs/bhunt_j0j2_20260806.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, sort_keys=False, ensure_ascii=False)
    print(f"wrote {out_path}")
    print(json.dumps({
        "prereg_standalone_commit_verified": prereg_standalone,
        "pent_per_layer_counts": layer_counts,
        "pent_total": h_w_total,
        "phi_invariant": phi_invariant,
        "bh3_unique": bh3_unique,
        "branch_resolved": branch_resolved,
    }, indent=2))


if __name__ == "__main__":
    main()
