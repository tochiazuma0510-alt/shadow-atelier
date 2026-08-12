#!/usr/bin/env python3
"""[P1-D2] step [D2-0] -- premise re-confirmation (arithmetic identity check, "seconds" scale
per spec). docs/notes/t3_gap12_resolution_v1.md §5 [D2-0].

This is NOT a new machine measurement -- it is a bookkeeping/arithmetic verification of the
identity chain that the design doc's own derivation establishes:
  R (total ramification of pi: W9 -> E, degree 3) = 6
    (Riemann-Hurwitz: 2*4-2 = 3*(2*1-2) + R  =>  R = 6)
    (branch decomposition, independently verified in w9k3_tricks_audit_v1.md §3.1:
     Q0 (e=3, contributes e-1=2) + Q_inf (e=3, contributes 2) + B1,B2 (each e=2, contributes 1)
     = 2+2+1+1 = 6, matching R)
  deg(Tschirnhaus bundle E-hat) = R/2 = 3   (t3_gap12_resolution_v1.md §1, boxed)
  deg(D) := deg(disc_t of the depressed cubic) = 2*deg(det E-hat) = 2*3 = 6
    (D is a section of (det E-hat)^{tensor 2}, t3_gap12_resolution_v1.md §2)
  delta (conductor/extra-vanishing degree) = (deg(D) - R) / 2 = (6-6)/2 = 0
    (multiplicity formula: deg(D) = R + 2*delta, per the same doc's §2 argument)

Scope note (honestly flagged): this script verifies the ARITHMETIC CONSISTENCY of the identity
chain using the branch data ALREADY established (paper-derived, independently checked) in
w9k3_tricks_audit_v1.md §3.1 and the RH count in w9_k3_insurance_v1.md §4/w9_E_model_v1.md §2.
It does NOT construct an explicit Tschirnhaus bundle or verify deg(D)=6 against an actual
computed discriminant polynomial (that requires [D2-1]-[D2-3], the Atiyah-classification +
Riemann-Roch + Groebner-basis construction, which is NOT attempted in this script -- flagged
to the coordinator as requiring a fuller design specification before safe implementation).
"""
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# branch decomposition of pi: W9 -> E (degree 3), per w9k3_tricks_audit_v1.md §3.1
# (independently re-verified there by the mathematician; cited here, not re-derived)
branch_points = [
    {"point": "Q0", "e": 3, "contribution": 2},
    {"point": "Q_inf", "e": 3, "contribution": 2},
    {"point": "B1", "e": 2, "contribution": 1},
    {"point": "B2", "e": 2, "contribution": 1},
]
R_from_branch_sum = sum(p["contribution"] for p in branch_points)

# Riemann-Hurwitz for pi: W9 (genus 4) -> E (genus 1), degree 3
g_W9 = 4
g_E = 1
deg_pi = 3
R_from_RH = (2 * g_W9 - 2) - deg_pi * (2 * g_E - 2)

deg_E_hat = R_from_RH // 2  # forced by t3_gap12_resolution_v1.md §1 boxed formula
deg_D = 2 * deg_E_hat        # D is a section of (det E-hat)^{tensor 2}, §2
delta = (deg_D - R_from_RH) // 2

checks = {
    "R_from_branch_sum": R_from_branch_sum,
    "R_from_RH": R_from_RH,
    "branch_sum_matches_RH": R_from_branch_sum == R_from_RH,
    "R_equals_6": R_from_RH == 6,
    "deg_E_hat": deg_E_hat,
    "deg_E_hat_equals_3": deg_E_hat == 3,
    "deg_D": deg_D,
    "deg_D_equals_6_E_a": deg_D == 6,
    "delta": delta,
    "delta_equals_0_E_b": delta == 0,
    "remainder_R_from_RH_is_even": R_from_RH % 2 == 0,
    "remainder_deg_D_minus_R_is_even": (deg_D - R_from_RH) % 2 == 0,
}
all_pass = all([
    checks["branch_sum_matches_RH"],
    checks["R_equals_6"],
    checks["deg_E_hat_equals_3"],
    checks["deg_D_equals_6_E_a"],
    checks["delta_equals_0_E_b"],
])

result = {
    "schema": "r13-p1d2-0/v1",
    "generated_by": {
        "tool": "python (arithmetic bookkeeping, no GAP execution)",
        "script": "search/p1_d2_0_precheck_v1.py",
        "order": "裁定1070 [P1-D2] step [D2-0] / docs/notes/t3_gap12_resolution_v1.md §5",
    },
    "scope_note": "アーカイブ済み分岐データ(w9k3_tricks_audit_v1.md §3.1、独立検算済み・paper-"
                  "derived)を引用し、算術恒等式(R=6・deg(E-hat)=3・deg(D)=6・delta=0)の整合性"
                  "のみを検算。[D2-1]〜[D2-3](Atiyah分類・Riemann-Roch・Groebner解法による実際の"
                  "束構成)は本scriptでは未実施(仕様の具体化が要ると判断・速達確認予定)。",
    "branch_points": branch_points,
    "genus_W9": g_W9,
    "genus_E": g_E,
    "degree_pi": deg_pi,
    "checks": checks,
    "all_checks_pass": all_pass,
    "u_touched": False,
    "c_touched": False,
    "prereg_value_computed": False,
    "d_no_interpretation": "machine values only; verdict は司令塔",
}

script_bytes = Path(__file__).read_bytes()
script_sha256 = hashlib.sha256(script_bytes).hexdigest()
result["provenance"] = {"script_sha256": script_sha256}

out_path = ROOT / "search" / "certs" / "p1_d2_0_precheck_v1_20260813.json"
out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"R_from_branch_sum={R_from_branch_sum} R_from_RH={R_from_RH} deg_E_hat={deg_E_hat} "
      f"deg_D={deg_D} delta={delta}")
print(f"all_checks_pass={all_pass}")
print(f"wrote {out_path}")
print(f"script sha256 = {script_sha256}")
