#!/usr/bin/env python3
"""Independent checker for w9-p1-k3-crt-stepC1/v1 certs.

Does NOT import search/w9_k3_crt_stepC1_gha.py. Rebuilds the same target
polynomial (w-a)(w-b)*g(w)^2 from the design document's canonical form
(docs/notes/w9_k3_insurance_v1.md §5) independently -- symbol names and
solving order are re-typed here on purpose (裁定1020 lesson: re-input of the
same expression is not independent implementation, so this checker re-derives
from the same source document text rather than copying the producer file),
then verifies:
  (1) the producer's claimed watch_C_a_pass / total_dim_measured against a
      freshly-solved sequence for g7..g2,
  (2) the producer JSON's own internal integrity hash.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def integrity_ok(payload: dict[str, Any]) -> bool:
    stored = payload.get("integrity", {}).get("canonical_payload_sha256")
    candidate = copy.deepcopy(payload)
    candidate.pop("integrity", None)
    return stored == sha256_bytes(canonical_bytes(candidate))


def independent_dimension_measurement() -> tuple[int | None, list[dict[str, Any]]]:
    """Re-derive dim(a,b,g0..g7 subject to w^17..w^12 matching (w-a)(w-b)g(w)^2 against
    boundary of (w^6+1)^3) from scratch, using a different variable-elimination ORDER
    than the producer (solve for g2..g7 in ASCENDING w-degree order this time, i.e.
    degree 12 first instead of degree 17 first) as an extra independent cross-check
    that the answer does not depend on solve order."""
    w, a, b = sp.symbols("w a b")
    gs = sp.symbols("g0 g1 g2 g3 g4 g5 g6 g7")
    g = w**8 + sum(gs[i] * w**i for i in range(8))
    target_poly = sp.Poly(sp.expand((w - a) * (w - b) * g**2), w)
    boundary = {18: 1, 12: 3, 6: 3, 0: 1}

    # ascending order this time: solve degree 12 for g2, degree 13 for g3, ..., degree 17 for g7
    order = [gs[2], gs[3], gs[4], gs[5], gs[6], gs[7]]
    subs: dict[sp.Symbol, sp.Expr] = {}
    log = []
    for i, deg in enumerate(range(12, 18)):
        coeff = target_poly.nth(deg).subs(subs)
        rhs = boundary.get(deg, 0)
        var = order[i]
        sol = sp.solve(sp.Eq(coeff, rhs), var)
        row = {"w_degree": deg, "solving_for": str(var), "solution_count": len(sol)}
        log.append(row)
        if len(sol) != 1:
            return None, log
        subs[var] = sp.simplify(sol[0])
    dim = 10 - len(subs)
    return dim, log


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cert = json.loads(args.cert.read_text(encoding="utf-8"))

    dim_check, log = independent_dimension_measurement()
    ab_g_dim_independent = dim_check
    total_dim_independent = (ab_g_dim_independent + 6) if ab_g_dim_independent is not None else None

    checks = {
        "producer_integrity_valid": integrity_ok(cert),
        "producer_total_dim_measured": cert.get("total_dim_measured"),
        "independent_total_dim_measured": total_dim_independent,
        "dims_agree": cert.get("total_dim_measured") == total_dim_independent,
        "producer_watch_C_a_pass": cert.get("watch_C_a_pass"),
        "independent_watch_C_a_pass": (total_dim_independent == 10),
        "watch_agree": cert.get("watch_C_a_pass") == (total_dim_independent == 10),
        "ascending_order_solve_log": log,
    }
    result = {
        "schema": "w9-p1-k3-crt-stepC1-check/v1",
        "d_no_interpretation": "machine values only; verdict は司令塔",
        "cert_path": str(args.cert),
        "checks": checks,
        "all_checks_true": bool(
            checks["producer_integrity_valid"]
            and checks["dims_agree"]
            and checks["watch_agree"]
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    print(f"CHECK_{'PASS' if result['all_checks_true'] else 'FAIL'}", flush=True)
    return 0 if result["all_checks_true"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
