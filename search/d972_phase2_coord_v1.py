#!/usr/bin/env python3
"""TRIAD-972 Phase 2 coordinate producer.

This producer evaluates the canonical formula of 2405 Thm. 4.3 and the
ROOF fibre product.  It uses exact (3.60) reduction of m modulo H_ord.
It neither reads nor computes any local Kummer quantity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def kappa(m: int) -> int:
    return m + 1 if m % 2 else -m


def gt_dih(n: int) -> set[tuple[int, int, int, int]]:
    """The literal (m,r-exponent triple) set in Thm. 4.3 (4.12)."""
    n_ord = math.lcm(n, 2)
    k_period = n // math.gcd(n, 2)
    ans: set[tuple[int, int, int, int]] = set()
    for m in range(n_ord):
        if math.gcd(2 * m + 1, n_ord) != 1:
            continue
        kap = kappa(m)
        for k in range(k_period):
            if n % 4 == 0 and (k - kap // 2) % 2:
                continue
            ans.add((m, 2 * k % n, -2 * k % n, kap % n))
    return ans


def reduce_dih(e: tuple[int, int, int, int], target_n: int) -> tuple[int, int, int, int]:
    target_ord = math.lcm(target_n, 2)
    m, a, b, c = e
    return (m % target_ord, a % target_n, b % target_n, c % target_n)


def u18(e: tuple[int, int, int, int]) -> int:
    return (2 * (e[0] % 18) + 1) % 18


def roof_measure(source_n: int, target: set[tuple[int, int, int, int]]) -> dict[str, int | bool]:
    source = gt_dih(source_n)
    units18 = (1, 5, 7, 11, 13, 17)
    s4_coordinates = tuple((u, translation) for u in units18 for translation in range(9))
    domain = []
    image = set()
    for e in source:
        ue = u18(e)
        for s4 in s4_coordinates:
            if s4[0] == ue:
                domain.append((e, s4))
                image.add((reduce_dih(e, 9), s4))
    return {
        "source_dih_size": len(source),
        "source_roof_size": len(domain),
        "raw_image_size": len(image),
        "image_subset_of_target_roof": all(pair[0] in target for pair in image),
    }


def shift_perm(p: Permutation, offset: int, total: int) -> Permutation:
    arr = list(range(total))
    for j in range(p.size):
        arr[offset + j] = offset + p(j)
    return Permutation(arr, size=total)


def direct_sum(p: Permutation, q: Permutation) -> Permutation:
    total = p.size + q.size
    return shift_perm(p, 0, total) * shift_perm(q, p.size, total)


def make_gn(n: int) -> tuple[Permutation, Permutation]:
    r = Permutation(list(range(1, n)) + [0])
    s = Permutation([(-j) % n for j in range(n)])
    total = 3 * n

    def tr(p: Permutation, i: int) -> Permutation:
        return shift_perm(p, i * n, total)

    x = tr(r, 0) * tr(s, 1) * tr(s, 2)
    y = tr(s * r, 0) * tr(r, 1) * tr(s * r, 2)
    return x, y


GF8_MOD = 0b1011


def gf8_mul(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= GF8_MOD
    return result & 7


def gf8_inv(a: int) -> int:
    if not a:
        raise ZeroDivisionError
    return next(b for b in range(1, 8) if gf8_mul(a, b) == 1)


P1_GF8 = tuple([(1, t) for t in range(8)] + [(0, 1)])


def matrix_line_perm(matrix: tuple[tuple[int, int], tuple[int, int]]) -> Permutation:
    arr = []
    for a, b in P1_GF8:
        c = gf8_mul(a, matrix[0][0]) ^ gf8_mul(b, matrix[1][0])
        d = gf8_mul(a, matrix[0][1]) ^ gf8_mul(b, matrix[1][1])
        line = (1, gf8_mul(d, gf8_inv(c))) if c else (0, 1)
        arr.append(P1_GF8.index(line))
    return Permutation(arr)


def s4_marking() -> tuple[Permutation, Permutation, dict[str, int]]:
    s = matrix_line_perm(((1, 0), (1, 1)))
    t = matrix_line_perm(((4, 3), (1, 5)))
    w = s * (~t)
    x = w**2
    y = (~s) * x * s
    return x, y, {
        "ord_s": int(s.order()),
        "ord_t": int(t.order()),
        "ord_w": int(w.order()),
        "marked_group_order": int(PermutationGroup([x, y]).order()),
    }


def group_order_receipts() -> dict[str, object]:
    gens = {n: make_gn(n) for n in (9, 27, 36, 108)}
    orders = {str(n): int(PermutationGroup(gens[n]).order()) for n in gens}
    x27, y27 = gens[27]
    x36, y36 = gens[36]
    meet_order = int(PermutationGroup([direct_sum(x27, x36), direct_sum(y27, y36)]).order())
    sx, sy, s4 = s4_marking()
    roof_orders = {}
    for n, (x, y) in gens.items():
        roof_orders[str(n)] = int(PermutationGroup([direct_sum(x, sx), direct_sum(y, sy)]).order())
    return {
        "canonical_gn_orders": orders,
        "marked_product_g27_g36_order": meet_order,
        "marked_g108_order": orders["108"],
        "meet_order_equality": meet_order == orders["108"],
        "s4_marking": s4,
        "roof_orders": roof_orders,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="search/certs/d972_phase2_coord_v1_20260813.json")
    parser.add_argument("--checkpoint", default="search/certs/d972_phase2_coord_v1_checkpoint.json")
    parser.add_argument("--hard-timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    output = ROOT / args.output
    checkpoint = ROOT / args.checkpoint
    started = time.monotonic()
    state = {
        "schema": "d972_phase2_coord_checkpoint/v1",
        "stage": "start",
        "complete": False,
        "u_touched": False,
        "c_touched": False,
    }
    atomic_json(checkpoint, state)

    def timeout() -> None:
        state.update(stage="hard_timeout", complete=False, elapsed_ms=int((time.monotonic() - started) * 1000))
        atomic_json(checkpoint, state)
        os._exit(124)

    timer = threading.Timer(args.hard_timeout_seconds, timeout)
    timer.daemon = True
    timer.start()
    try:
        groups = group_order_receipts()
        state.update(stage="group_orders", elapsed_ms=int((time.monotonic() - started) * 1000))
        atomic_json(checkpoint, state)

        gt9 = gt_dih(9)
        gt27 = gt_dih(27)
        gt36 = gt_dih(36)
        gt108 = gt_dih(108)
        im27_9 = {reduce_dih(e, 9) for e in gt27}
        im36_9 = {reduce_dih(e, 9) for e in gt36}
        im108_27 = {reduce_dih(e, 27) for e in gt108}
        im108_9 = {reduce_dih(e, 9) for e in gt108}
        factorization = all(reduce_dih(reduce_dih(e, 27), 9) == reduce_dih(e, 9) for e in gt108)

        depth1 = roof_measure(27, gt9)
        depth2 = roof_measure(108, gt9)
        independent36 = roof_measure(36, gt9)
        state.update(
            stage="measurements",
            depth1_raw=depth1["raw_image_size"],
            depth2_raw=depth2["raw_image_size"],
            elapsed_ms=int((time.monotonic() - started) * 1000),
        )
        atomic_json(checkpoint, state)

        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        cert = {
            "schema": "d972_phase2_coord/v1",
            "run_id": f"d972-phase2-coord-{now}",
            "generated_by": {
                "tool": "Python 3.13 + SymPy 1.14",
                "script": "search/d972_phase2_coord_v1.py",
            },
            "mathematical_inputs": {
                "dihedral_coordinates": "2405 Thm. 4.3 (4.9),(4.12)",
                "reduction": "2401 (3.60): m mod H_ord and exponent reduction",
                "roof": "GT(K^n cap N_S4) as fibre product over U=(Z/18)^x",
                "s4_coordinate_fibres": "Hol(Z/9)=Z/9 semidirect (Z/9)^x",
            },
            "coordinate_rule": {
                "m_reduction": "m mod H_ord",
                "legacy_half_modulus_used": False,
            },
            "chain_prefix": {
                "enumerand_1": "K^(27) cap N_S4",
                "enumerand_2": "K^(36) cap N_S4",
                "L_1": "K^(27) cap N_S4",
                "L_2": "K^(27) cap K^(36) cap N_S4 = K^(108) cap N_S4",
            },
            "group_order_receipts": groups,
            "dihedral_coordinate_counts": {
                "9": len(gt9),
                "27": len(gt27),
                "36": len(gt36),
                "108": len(gt108),
            },
            "dihedral_reductions": {
                "image_27_to_9": len(im27_9),
                "image_36_to_9": len(im36_9),
                "image_108_to_27": len(im108_27),
                "image_108_to_9": len(im108_9),
                "image_27_to_9_equals_target": im27_9 == gt9,
                "image_36_to_9_equals_target": im36_9 == gt9,
                "image_108_to_27_equals_target": im108_27 == gt27,
                "image_108_to_9_equals_target": im108_9 == gt9,
                "factorization_108_27_9_all_coordinates": factorization,
            },
            "depths": [
                {"depth": 1, "window": "L_1", **depth1},
                {"depth": 2, "window": "L_2", **depth2},
            ],
            "nonchain_probe": {"window": "K^(36) cap N_S4", **independent36},
            "base_roof_size": 972,
            "elapsed_ms": int((time.monotonic() - started) * 1000),
            "u_touched": False,
            "c_touched": False,
            "sealed_k5_touched": False,
            "prereg_quantities_untouched": True,
            "interpretation": "raw finite-depth values only",
            "input_sha256": {
                str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p)
                for p in (
                    ROOT / "docs/week1-定義ノート.md",
                    ROOT / "docs/notes/2405.11725-抽出ノート_v1.md",
                    ROOT / "docs/notes/ihnec_v1.md",
                    ROOT / "search/certs/d972_phase1_v1_20260813.json",
                )
            },
        }
        atomic_json(output, cert)
        state.update(
            stage="complete",
            complete=True,
            output=str(output.relative_to(ROOT)).replace("\\", "/"),
            elapsed_ms=cert["elapsed_ms"],
        )
        atomic_json(checkpoint, state)
        print(json.dumps({"run_id": cert["run_id"], "raw": [d["raw_image_size"] for d in cert["depths"]]}))
        return 0
    finally:
        timer.cancel()


if __name__ == "__main__":
    raise SystemExit(main())
