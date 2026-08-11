#!/usr/bin/env python3
"""
torsweep_t4_step2_gha.py -- TOR-DET step 2 (EXACT ambient columns at one
of the two independent large moduli), GHA job-splittable form (裁定876).

Takes step1's artifact (--step1-artifact) and a --modulus-label {A,B}
(fixed values P_EXACT_A=10**40 / P_EXACT_B=10**40+15, matching every
other exact-arithmetic script in this repo -- torsweep_k11/k12_run.py,
torsweep_k13_hnf_construct_v1.py), computes the dim_h x r_prime exact
integer column matrix for JUST that one modulus, and writes it as its own
artifact. Modulus A and modulus B are INDEPENDENT of each other (both
only depend on step1's decoded pivot positions) -- this is exactly why
they can be two PARALLEL GHA jobs rather than the serial "modulus A then
modulus B" the local script did (halving this stage's wall-clock, ~5400s
each at K=12 per the local r1 run's own timing).
"""
import argparse
import json
import os
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
sys.set_int_max_str_digits(0)

import edim_semidirect_v1 as ed  # noqa: E402
from torsweep_k12_run import center_lift  # noqa: E402

P_EXACT_A = 10 ** 40
P_EXACT_B = 10 ** 40 + 15
MODULI = {"A": P_EXACT_A, "B": P_EXACT_B}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step1-artifact", required=True)
    ap.add_argument("--modulus-label", required=True, choices=["A", "B"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    with open(args.step1_artifact, "r", encoding="utf-8") as f:
        step1 = json.load(f)
    if "stop" in step1:
        raise RuntimeError(f"step1 artifact records a STOP: {step1['stop']}")
    K = step1["k"]
    dim_h = step1["dim_h"]
    r_prime = step1["r_prime"]
    decoded = [(kind, tuple(word)) for kind, word in step1["decoded"]]
    p_exact = MODULI[args.modulus_label]
    record(f"K={K} dim_h={dim_h} r_prime={r_prime} modulus_label={args.modulus_label} "
           f"p_exact_digits={len(str(p_exact))}")

    h_alg2_exact = ed.GradedLie(2, K, p_exact, sparse_degrees={K})
    assert h_alg2_exact.dim[K] == dim_h
    state_leaf_images = ed._rho_power_h_leaf_images_ambient(p_exact)
    base_table = ed._delta_base_table(p_exact)
    tree_caches = [dict() for _ in range(5)]
    subtree_counts, cache_allowed = ed._subtree_cache_policy_for_roots(
        h_alg2_exact.trees[K])

    cols = [[0] * r_prime for _ in range(dim_h)]
    for basis_index, tree in enumerate(h_alg2_exact.trees[K]):
        nu_n = {}
        nu_h = {}
        for power in range(5):
            action_cache = {}
            n_part, h_part, h_expr, degree = ed.eval_tree_in_t_ambient(
                tree, state_leaf_images[power], p_exact,
                cache=tree_caches[power], base_table=base_table,
                action_cache=action_cache, cache_result=False,
                cache_allowed=cache_allowed)
            assert degree == K
            nu_n = ed.word_add([nu_n, n_part], p_exact)
            nu_h = ed.word_add([nu_h, h_part], p_exact)
        row = []
        for kind, word in decoded:
            raw = (nu_n if kind == "n" else nu_h).get(word, 0)
            row.append(center_lift(raw, p_exact))
        cols[basis_index] = row
        if basis_index % 50 == 0:
            record(f"  tree {basis_index}/{dim_h}")

    elapsed = time.time() - t_start
    record(f"step2 (modulus {args.modulus_label}) done, elapsed={elapsed:.2f}s")

    payload = {
        "schema": "tor_sweep_t4_step2_gha.1",
        "ruling_refs": ["裁定876"],
        "k": K, "modulus_label": args.modulus_label,
        "exact_modulus": str(p_exact),
        "dim_h": dim_h, "r_prime": r_prime,
        "cols": cols,
        "elapsed_seconds": elapsed,
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    record(f"artifact written: {args.out} ({os.path.getsize(args.out)} bytes)")
    print(f"TORSWEEP_T4_STEP2_DONE k={K} modulus_label={args.modulus_label} "
          f"elapsed={elapsed:.2f}", flush=True)


if __name__ == "__main__":
    main()
