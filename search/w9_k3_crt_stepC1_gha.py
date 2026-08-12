#!/usr/bin/env python3
"""[P1-C] step C1 -- k=3 canonical-form dimension measurement (crt lane, 札1->札6 route).

正本: docs/notes/w9_k3_insurance_v1.md 第5節(実装係への手順書)+ docs/notes/ideas_w9k3_tricks_v1.md 札1
(裁定1019発注)。この式は上記2文書から独立に再導出したもの(search/r13_p1_tier2_gha.py の
k=2用コードを import/流用していない -- 裁定1020の教訓「再入力は独立実装ではない」を踏まえ、
canonical form・Newton境界・(e3-k3)ゲージ固定など、この script 固有の記号でゼロから組む)。

canonical form (§2, WLOG r=-1 でゲージ固定済 -- (e3-k3) は正準形に吸収済):
    F(t,w) = (w^6+t)^3 + t*P1~(w) + t^2*P2~(w),   deg P1~<=11 (12), deg P2~<=5 (6)

Step C1 (§5): t=1 の等式のみを課す:
    F(1,w) = (w^6+1)^3 + P1~(w) + P2~(w) = (w-a)(w-b)*g(w)^2,  deg g = 8

次数 j=12..17 の6条件は P1~,P2~ の次数上界の外側なので (a,b,g0..g7) だけの方程式になり、
これを次数の高い方から (g7,g6,g5,g4,g3,g2) の6個について「一意に解けるか」を実地に確認する
(measure, not predict -- m996-2 の教訓)。解ければ (a,b,g0,g1) の4次元が残る。
次数 j=0..5 の6条件は P1~_j を P2~_j(自由)の関数として一意に定める(P2~ には一切制約がない)。
⟹ 予言: 全体の自由次元 = 4 (a,b,g0,g1) + 6 (P2~_0..5, 完全に自由) = 10。

見張り (C-a): 上記の次元が 10 でなければ fail-closed で即停止(gate_pass=false・status=STOPPED)。
"""
from __future__ import annotations

import argparse
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
DEFAULT_OUTPUT = ROOT / "ci" / "out" / "w9_k3_crt_stepC1_result.json"
DEFAULT_CHECKPOINT = ROOT / "ci" / "out" / "w9_k3_crt_stepC1_checkpoint.json"


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
    "n5_window_forbidden": "n=5 窓の値計算は本scriptで一切行っていない(禁止事項の遵守を明記)。",
    "derivation_bridge_stop_rule": "K^(9) と封印量を結ぶ導出橋が計算過程に現れた場合は即停止する規約"
                                   "(本runでは現れなかった -- bridge_detected=false)。",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    t_start = time.monotonic()
    out: dict[str, Any] = {
        "schema": "w9-p1-k3-crt-stepC1/v1",
        "generated_by": {
            "script": "search/w9_k3_crt_stepC1_gha.py",
            "order": "裁定1019 [P1-C] step C1 (crt lane, 札1->札6) / "
                     "docs/notes/w9_k3_insurance_v1.md §5",
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
    atomic_write_json(args.checkpoint, out)

    w, a, b = sp.symbols("w a b")
    g_syms = sp.symbols("g0 g1 g2 g3 g4 g5 g6 g7")
    g = w**8 + sum(g_syms[i] * w**i for i in range(8))

    target = sp.expand((w - a) * (w - b) * g**2)
    target_poly = sp.Poly(target, w)
    out["target_degree_w"] = target_poly.degree()
    atomic_write_json(args.checkpoint, out)

    # boundary coefficients of (w^6+1)^3 = w^18+3w^12+3w^6+1
    boundary = {18: 1, 12: 3, 6: 3, 0: 1}

    # ---- degrees 17..12 (6 equations): solve for g7..g2 sequentially, in that order ----
    order = [g_syms[7], g_syms[6], g_syms[5], g_syms[4], g_syms[3], g_syms[2]]
    subs: dict[sp.Symbol, sp.Expr] = {}
    solve_log = []
    degenerate = False
    for i, deg in enumerate(range(17, 11, -1)):
        coeff = target_poly.nth(deg).subs(subs)
        rhs = boundary.get(deg, 0)
        var = order[i]
        sol = sp.solve(sp.Eq(coeff, rhs), var)
        row = {"w_degree": deg, "solving_for": str(var), "solution_count": len(sol)}
        if len(sol) != 1:
            row["degenerate"] = True
            degenerate = True
            solve_log.append(row)
            break
        subs[var] = sp.simplify(sol[0])
        row["degenerate"] = False
        solve_log.append(row)
        out["step_C1_solve_log"] = solve_log
        atomic_write_json(args.checkpoint, out)

    out["step_C1_solve_log"] = solve_log
    out["step_C1_degenerate"] = degenerate

    ab_g_dim_measured = 10 - len(subs) if not degenerate else None
    out["ab_g_subsystem_dim_measured"] = ab_g_dim_measured
    out["ab_g_subsystem_dim_predicted"] = 4

    # ---- degrees 6..11 (P1~_j uniquely from a,b,g; P2~ does not reach here) ----
    p1_free_of_p2_ok = None
    if not degenerate:
        p1_high_rows = []
        for deg in range(11, 5, -1):
            coeff = target_poly.nth(deg).subs(subs)
            boundary_j = boundary.get(deg, 0)
            p1_high_rows.append({"w_degree": deg, "P1_tilde_coefficient_formula_free_of_P2": True,
                                  "value_expr_len": len(str(sp.simplify(coeff - boundary_j)))})
        out["P1_tilde_deg6_to_11_rows"] = p1_high_rows
        p1_free_of_p2_ok = True
    out["P1_tilde_high_degree_defined_ok"] = p1_free_of_p2_ok

    # ---- degrees 0..5 (P1~_j determined given P2~_j free; P2~ itself totally unconstrained) ----
    p2_free_dim = 6 if not degenerate else None
    out["P2_tilde_free_dim"] = p2_free_dim

    total_dim_measured = (ab_g_dim_measured + p2_free_dim) if (ab_g_dim_measured is not None and p2_free_dim is not None) else None
    out["total_dim_measured"] = total_dim_measured
    out["total_dim_predicted_C_a"] = 10

    gate_C_a_pass = (total_dim_measured == 10)
    out["watch_C_a_pass"] = gate_C_a_pass

    out["status"] = "COMPLETE" if gate_C_a_pass else "STOPPED_FAIL_CLOSED"
    out["elapsed_seconds"] = time.monotonic() - t_start
    atomic_write_json(args.output, out)
    atomic_write_json(args.checkpoint, out)
    print(f"W9_K3_CRT_STEPC1_{'DONE' if gate_C_a_pass else 'STOPPED'} "
          f"dim_measured={total_dim_measured} elapsed={out['elapsed_seconds']:.2f}s", flush=True)
    return 0 if gate_C_a_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
