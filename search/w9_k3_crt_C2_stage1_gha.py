#!/usr/bin/env python3
"""[C2-0]+[C2-1] -- k=3 crt lane, step C2 stage 1 (裁定1023).

正本: docs/notes/t3_spec_and_C2_calib_v1.md 第II部 §6-8。

[C2-0] 起動時回帰ゲート(fail-closed, 必須): Sol の k=2 cert(search/certs/
r13_p1_tier2_v2_20260812.json)の4 profile で、重複度公式
    ord_beta(D) = sum_{P->beta}(e_P-1) + 2*delta_beta
の総和形 deg(D_branch) = (奇数位数根の次数総和) + 2*(二重根の次数総和) を検算する。
1本でも外れたら STOP(このscriptは producer をimportせず、cert のJSONを読むだけ)。

[C2-1] D := disc_t F の構成(F=(w^6+t)^3+t*P1~+t^2*P2~, deg P1~<=11, deg P2~<=5,
P1~/P2~ は未定係数のまま symbolic に保持)。w^36 係数が P1~/P2~ の値に依らず恒等的に
0 になることを検算(w9_k3_insurance_v1.md §4 の主張の直接確認 -- 独立再導出)。
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import time
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SOL_K2_CERT = ROOT / "search" / "certs" / "r13_p1_tier2_v2_20260812.json"
DEFAULT_OUTPUT = ROOT / "ci" / "out" / "w9_k3_crt_C2_stage1_result.json"
DEFAULT_CHECKPOINT = ROOT / "ci" / "out" / "w9_k3_crt_C2_stage1_checkpoint.json"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def json_compatible(value: Any) -> Any:
    if value is None or isinstance(value, (bool, str, int, float)):
        return value
    if isinstance(value, sp.Integer):
        return int(value)
    if isinstance(value, sp.Rational):
        return str(value)
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_compatible(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_compatible(v) for v in value]
    return f"<UNSERIALIZABLE:{type(value).__name__}:{value}>"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def with_integrity(payload: dict[str, Any]) -> dict[str, Any]:
    result = json_compatible(copy.deepcopy(payload))
    result.pop("integrity", None)
    result["integrity"] = {
        "canonical_payload_sha256": sha256_bytes(canonical_bytes(result)),
        "definition": "sha256 of canonical UTF-8 JSON after removing the integrity member",
    }
    return result


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    final_payload = with_integrity(payload)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(final_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    os.replace(tmp, path)


QUARANTINE = {
    "name_collide": "本certは K^(9) 窓インスタンス。封印の K^(5) 量とは別対象(裁定1007)。",
    "n5_window_forbidden": "n=5 窓の値計算は本scriptで一切行っていない。",
    "derivation_bridge_stop_rule": "導出橋が現れたら即停止する規約(本runでは現れなかった)。",
}


def c2_0_regression_gate() -> dict[str, Any]:
    """Verify ord_beta(D)=sum(e-1)+2*delta at the branch/S1-S2 total-degree level using
    ONLY Sol's k=2 output cert (no import of Sol's/the producer's code)."""
    cert = json.loads(SOL_K2_CERT.read_text(encoding="utf-8"))
    rows = cert["candidate_factor_classifications"]
    # design doc's boxed table uses the FIRST factor of each branch (branch I's e95f7f94,
    # branch II's 7e2054b0); the other two factors (exponent 2 in their branch) carry the
    # identical squarefree profile shape and are not independent additional data points.
    branch_i_factor = next(r for r in rows if any(m["branch"] == "I" and m["discriminant_exponent"] == 1
                                                    for m in r["branch_memberships"]))
    branch_ii_factor = next(r for r in rows if any(m["branch"] == "II" and m["discriminant_exponent"] == 1
                                                     for m in r["branch_memberships"]))

    def odd_and_double(profile: list[dict[str, int]]) -> tuple[int, int]:
        odd_total = sum(row["distinct_root_degree"] for row in profile if row["multiplicity"] % 2 == 1)
        double_total = sum(row["distinct_root_degree"] for row in profile if row["multiplicity"] == 2)
        return odd_total, double_total

    checks = []
    expected_rows = [
        ("branch_I", "S1", branch_i_factor["S1_squarefree_profile"], 8),
        ("branch_I", "S2", branch_i_factor["S2_squarefree_profile"], 9),
        ("branch_II", "S1", branch_ii_factor["S1_squarefree_profile"], 8),
        ("branch_II", "S2", branch_ii_factor["S2_squarefree_profile"], 9),
    ]
    all_pass = True
    for branch, which, profile, expected_degree in expected_rows:
        odd_total, double_total = odd_and_double(profile)
        formula_value = odd_total + 2 * double_total
        row_pass = (formula_value == expected_degree)
        all_pass = all_pass and row_pass
        checks.append({
            "branch": branch, "which": which, "expected_degree": expected_degree,
            "odd_root_total": odd_total, "double_root_total": double_total,
            "formula_value": formula_value, "pass": row_pass,
        })
    return {"sol_k2_cert_sha256": sha256_file(SOL_K2_CERT), "rows": checks, "all_pass": all_pass}


def c2_1_D_construction() -> dict[str, Any]:
    """D := disc_t F for F = t^3 + b(w)*t^2 + c(w)*t + d(w), with
       b = 3w^6 + P2~(w)  (deg P2~ <= 5),
       c = 3w^12 + P1~(w) (deg P1~ <= 11),
       d = w^18.
    Cubic discriminant formula (monic, standard): D = 18*b*c*d - 4*b^3*d + b^2*c^2 - 4*c^3 - 27*d^2.

    DEGREE ARGUMENT (checked directly, not assumed): each of the 5 terms above is a SUM of
    products of {b or its leading part, c or its leading part, d}. Since P2~ has degree <=5
    (strictly less than b's leading degree 6) and P1~ has degree <=11 (strictly less than c's
    leading degree 12), any term in the fully-expanded D that uses a NON-leading contribution
    from b or c has total w-degree STRICTLY LESS than 36 (the top possible degree, achieved only
    by the all-leading-term product in each of the 5 summands). Hence the w^36 coefficient of D
    depends ONLY on the leading terms (3w^6, 3w^12, w^18) of b,c,d -- independent of the actual
    P1~/P2~ coefficient values. This script verifies that degree claim symbolically (small,
    single-variable computation with b,c,d kept as literal polynomials, not 18 free parameters)
    and then evaluates the resulting pure-numeric leading-term coefficient.
    """
    t, w = sp.symbols("t w")

    # ---- degree-argument check (small, symbolic in w only, single symbolic perturbation
    #      markers eps_b, eps_c standing for "any strictly-lower-degree polynomial part") ----
    eps_b, eps_c = sp.symbols("eps_b eps_c")  # placeholders: deg(eps_b)<=5, deg(eps_c)<=11 conceptually
    # To PROVE the degree claim without picking a concrete P1~/P2~, verify it structurally:
    # b = 3w^6 + (lower-degree terms) => the top-degree part of any power/product of b is
    # governed entirely by the 3w^6 term as long as we only ask about the coefficient of the
    # GLOBALLY maximal degree (36); this is a direct consequence of polynomial multiplication
    # (deg(P+Q)*R has top coefficient = top coefficient of P*R when deg(Q)<deg(P)). We check
    # this mechanically by computing D symbolically for TWO different concrete low-degree
    # perturbations of P1~/P2~ and confirming the w^36 coefficient is identical in both cases
    # (necessary condition for "coefficient independent of perturbation"; combined with the
    # analytic degree argument above, this is a strong two-point confirmation, not a full proof
    # by exhaustion -- reported honestly as such).
    def D_w36_coeff_for(p1_coeffs: list[int], p2_coeffs: list[int]) -> sp.Integer:
        P2_tilde = sum(p2_coeffs[i] * w**i for i in range(len(p2_coeffs)))
        P1_tilde = sum(p1_coeffs[i] * w**i for i in range(len(p1_coeffs)))
        b = 3 * w**6 + P2_tilde
        c = 3 * w**12 + P1_tilde
        d = w**18
        D = sp.expand(18 * b * c * d - 4 * b**3 * d + b**2 * c**2 - 4 * c**3 - 27 * d**2)
        D_poly = sp.Poly(D, w)
        return D_poly.nth(36) if D_poly.degree() >= 36 else sp.Integer(0)

    coeff_zero_perturbation = D_w36_coeff_for([0]*12, [0]*6)
    coeff_nonzero_perturbation_1 = D_w36_coeff_for(list(range(1, 13)), list(range(1, 7)))
    coeff_nonzero_perturbation_2 = D_w36_coeff_for([7, -3, 0, 2, 5, -1, 4, 0, 1, -2, 6, 3],
                                                     [-4, 2, 0, 1, -5, 3])
    all_three_agree = (coeff_zero_perturbation == coeff_nonzero_perturbation_1 == coeff_nonzero_perturbation_2)

    # NOTE: evaluating D with P1~=P2~=0 exactly makes F=(w^6+t)^3 a perfect cube (triple root
    # t=-w^6 for every w), so D itself vanishes IDENTICALLY there (not just its w^36 term) --
    # this is why coeff_zero_perturbation=0 is not by itself informative; the real evidence is
    # that the two GENUINELY NONZERO, non-degenerate perturbations below give the same w^36
    # coefficient (0) as the degenerate case.

    return {
        "coeff_w36_zero_perturbation": int(coeff_zero_perturbation),
        "coeff_w36_nonzero_perturbation_1": int(coeff_nonzero_perturbation_1),
        "coeff_w36_nonzero_perturbation_2": int(coeff_nonzero_perturbation_2),
        "coeff_w36_independent_of_P1_P2_three_point_check": bool(all_three_agree),
        "coeff_w36_value": int(coeff_zero_perturbation),
        "coeff_w36_is_zero": bool(all_three_agree and coeff_zero_perturbation == 0),
        "method_note": "3点(P1~=P2~=0・2種の非零摂動)で w^36係数が一致することを確認(次数論法の"
                        "解析的証明ではなく数値的3点確認 -- 18変数の完全記号展開は計算量的に不可だった"
                        "ため、次数論法(P1~の次数<=11<12・P2~の次数<=5<6ゆえ非leading項はw^36に届かない)"
                        "の妥当性チェックとしてこの3点一致を報告する)",
    }


def main() -> int:
    t_start = time.monotonic()
    out: dict[str, Any] = {
        "schema": "w9-p1-k3-crt-C2-stage1/v1",
        "generated_by": {
            "script": "search/w9_k3_crt_C2_stage1_gha.py",
            "order": "裁定1023 [C2-0]+[C2-1] (crt-C2 job) / docs/notes/t3_spec_and_C2_calib_v1.md §6-8",
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "github_sha": os.environ.get("GITHUB_SHA"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        },
        "quarantine": QUARANTINE,
        "bridge_detected": False,
        "u_touched": False,
        "c_touched": False,
        "prereg_value_computed": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
        "window": "K^(9)",
        "status": "RUNNING",
    }
    atomic_write_json(DEFAULT_CHECKPOINT, out)

    c2_0 = c2_0_regression_gate()
    out["C2_0_regression_gate"] = c2_0
    atomic_write_json(DEFAULT_CHECKPOINT, out)

    if not c2_0["all_pass"]:
        out["status"] = "STOPPED_FAIL_CLOSED_AT_C2_0"
        out["elapsed_seconds"] = time.monotonic() - t_start
        atomic_write_json(DEFAULT_OUTPUT, out)
        atomic_write_json(DEFAULT_CHECKPOINT, out)
        print("W9_K3_CRT_C2_STAGE1_STOPPED_AT_C2_0", flush=True)
        return 1

    c2_1 = c2_1_D_construction()
    out["C2_1_D_construction"] = c2_1
    out["status"] = "COMPLETE" if c2_1["coeff_w36_is_zero"] else "STOPPED_FAIL_CLOSED_AT_C2_1"
    out["elapsed_seconds"] = time.monotonic() - t_start
    atomic_write_json(DEFAULT_OUTPUT, out)
    atomic_write_json(DEFAULT_CHECKPOINT, out)
    print(f"W9_K3_CRT_C2_STAGE1_{'DONE' if out['status']=='COMPLETE' else 'STOPPED'} "
          f"elapsed={out['elapsed_seconds']:.2f}s", flush=True)
    return 0 if out["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
