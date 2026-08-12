#!/usr/bin/env python3
"""Checkpointed generator-tree shard for K=13 TOR-DET exact columns."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
sys.set_int_max_str_digits(0)

import edim_semidirect_v1 as ed  # noqa: E402
from torsweep_k12_run import center_lift  # noqa: E402


K = 13
DIM_H = 630
R_PRIME = 207
MODULI = {"A": 10**40, "B": 10**40 + 15}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_resume(path: Path | None, identity: dict) -> list[list]:
    if path is None or not path.is_file():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "tor_sweep_t4_step2_shard_checkpoint.1":
        raise ValueError("resume checkpoint schema mismatch")
    if payload.get("identity") != identity:
        raise ValueError("resume checkpoint identity mismatch")
    rows = payload.get("rows", [])
    expected = list(range(identity["tree_start"], identity["tree_start"] + len(rows)))
    if [row[0] for row in rows] != expected:
        raise ValueError("resume checkpoint rows are not a contiguous prefix")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step1-artifact", type=Path, required=True)
    parser.add_argument("--modulus-label", choices=("A", "B"), required=True)
    parser.add_argument("--tree-start", type=int, required=True)
    parser.add_argument("--tree-end", type=int, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--resume-checkpoint", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    started = time.time()
    step1 = json.loads(args.step1_artifact.read_text(encoding="utf-8"))
    if step1["k"] != K or step1["dim_h"] != DIM_H or step1["r_prime"] != R_PRIME:
        raise ValueError("step1 K/dim_h/r_prime mismatch")
    if len(step1["decoded"]) != R_PRIME:
        raise ValueError("step1 decoded pivot count mismatch")
    if not 0 <= args.tree_start < args.tree_end <= DIM_H:
        raise ValueError("invalid tree range")

    modulus = MODULI[args.modulus_label]
    identity = {
        "k": K,
        "modulus_label": args.modulus_label,
        "exact_modulus": str(modulus),
        "tree_start": args.tree_start,
        "tree_end": args.tree_end,
        "step1_sha256": sha256(args.step1_artifact),
    }
    rows = load_resume(args.resume_checkpoint, identity)
    next_tree = args.tree_start + len(rows)
    print(
        f"K={K} modulus={args.modulus_label} range=[{args.tree_start},{args.tree_end}) "
        f"resume_rows={len(rows)}",
        flush=True,
    )

    h_alg = ed.GradedLie(2, K, modulus, sparse_degrees={K})
    state_leaf_images = ed._rho_power_h_leaf_images_ambient(modulus)
    base_table = ed._delta_base_table(modulus)
    tree_caches = [dict() for _ in range(5)]
    _, cache_allowed = ed._subtree_cache_policy_for_roots(h_alg.trees[K])
    decoded = [(kind, tuple(word)) for kind, word in step1["decoded"]]

    def checkpoint(state: str) -> None:
        atomic_json(
            args.checkpoint,
            {
                "schema": "tor_sweep_t4_step2_shard_checkpoint.1",
                "state": state,
                "identity": identity,
                "rows": rows,
                "next_tree": args.tree_start + len(rows),
                "elapsed_seconds_this_attempt": time.time() - started,
            },
        )

    checkpoint("RUNNING")
    for basis_index in range(next_tree, args.tree_end):
        tree = h_alg.trees[K][basis_index]
        nu_n: dict = {}
        nu_h: dict = {}
        for power in range(5):
            n_part, h_part, _, degree = ed.eval_tree_in_t_ambient(
                tree,
                state_leaf_images[power],
                modulus,
                cache=tree_caches[power],
                base_table=base_table,
                action_cache={},
                cache_result=False,
                cache_allowed=cache_allowed,
            )
            if degree != K:
                raise ValueError("tree degree mismatch")
            nu_n = ed.word_add([nu_n, n_part], modulus)
            nu_h = ed.word_add([nu_h, h_part], modulus)
        row = [
            center_lift((nu_n if kind == "n" else nu_h).get(word, 0), modulus)
            for kind, word in decoded
        ]
        rows.append([basis_index, row])
        checkpoint("RUNNING")
        print(
            f"tree_done={basis_index} completed={len(rows)}/{args.tree_end-args.tree_start}",
            flush=True,
        )

    payload = {
        "schema": "tor_sweep_t4_step2_shard_k13_gha.1",
        "identity": identity,
        "dim_h": DIM_H,
        "r_prime": R_PRIME,
        "rows": rows,
        "elapsed_seconds_this_attempt": time.time() - started,
    }
    checkpoint("COMPLETE")
    atomic_json(args.out, payload)
    print(
        "TORSWEEP_T4_STEP2_SHARD_DONE "
        f"label={args.modulus_label} range={args.tree_start}-{args.tree_end}",
        flush=True,
    )


if __name__ == "__main__":
    main()
