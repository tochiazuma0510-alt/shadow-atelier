#!/usr/bin/env python3
"""
torsweep_k13_shard_eval.py -- k=13 GHA row-shard worker (裁定789/792).

Evaluates a CONTIGUOUS RANGE of the 630 Lambda_13 generator (Lyndon-tree)
indices -- NOT a range of H_13 basis rows (裁定789's original "H13基底210
行" framing was a misnomer, corrected in 裁定792: the axis that is actually
embarrassingly parallel and additively recombinable is the 630-wide
GENERATOR axis of edim_semidirect_v1.GradedLie(2,13,p).trees[13], via the
new accumulate_nu_j_restricted_range() helper -- see that function's
docstring for the additivity argument).

Two modes:
  --mode modq   : accumulate mod a single prime q (T2/T3 rank witness).
                  3 primes needed total (no "儀式" reuse exists for k=13,
                  unlike k=12 -- 裁定789(2a): all 3 self-computed).
  --mode crt    : accumulate over a single LARGE NON-PRIME modulus. ★
                  SUPERSEDED per 裁定796(6): the mathematician's SNF-MOD-13
                  spec (docs/notes/tor_sweep_design_v1_addendum_c.md,
                  e3f3c62) determined that this dual-huge-modulus-agreement
                  approach is NOT the right tool at k=13's scale (B_13's
                  entries already exceed 4300 digits) -- HNF/LLL/saturated-
                  basis construction are explicitly prohibited by that
                  spec. The actual T4/T5 method is (i) gcd of a few small
                  r'xr' minor determinants (proof, not heuristic: bounds
                  the torsion support) (ii) mod-q RANK DEFICIENCY per
                  candidate prime (a modq-style pass, reusing this same
                  script's modq machinery, not this crt mode) (iii) mod
                  q^N Smith form only for surviving primes. This --mode
                  crt code path is left in place as harmless raw-data
                  scaffolding (still mathematically valid: it computes a
                  correct partial sum, just not the method that will
                  actually be used) pending the SNF-MOD-13 rewrite
                  (deferred to after k=12 T4/T5, per 裁定796(6) -- not
                  urgent).

Output artifact: a SPARSE serialization of the partial restricted matrix
(nonzero (row,col,value) triples), NOT the dense array -- 裁定792's
artifact-size instruction (dense would be ~2.7GB/shard territory; the FG-H
nnz measurement determines how sparse it actually is, recorded in the
artifact header for the aggregate job to check against).

★裁定867(2): serialization is numpy .npz (savez_compressed, int32 rows/
cols + int32 vals for modq mode -- all three commissioned primes are
< 2**31 so residues fit int32 exactly), NOT the original Python-list-of-
ints + json.dump(gzip) format. run 31515932255's 90-tree shards measured
nnz in the ~10^8 range; a JSON list of 10^8 Python int objects has ~28
bytes/object CPython overhead ALONE (~2.8GB for the rows list, same again
for cols, same again for vals -- ~8.4GB), on top of the ~2.7GB dense
array still live during extraction -- this is the diagnosed OOM cause of
that run's mass job failures (runner "shutdown signal", i.e. killed,
shortly after each shard's tree-evaluation phase finished and entered
this post-processing phase). npz with fixed-width numpy dtypes has ZERO
per-element Python object overhead: rows+cols+vals at 10^8 entries x
4 bytes each = ~1.2GB total, peak (with the still-live 2.7GB dense array)
~3.9GB -- see torsweep_k13_shard_npz_serialize_smoke_test.py (synthetic
10^8-nnz smoke test, run locally per 裁定867(4) before any re-dispatch)
for the measured figure.
crt mode (superseded/deferred, 裁定796(6)) can have values far exceeding
int32/int64 (B_13's entries alone run to ~9720 digits) -- for that mode
only, vals are stored as a numpy object array (Python big ints, pickled by
savez) exactly as before; this mode is not optimized and is not expected
to run at 90-tree-shard scale until/unless SNF-MOD-13 revives it.

This script does not decide shard boundaries or count -- those are
workflow_dispatch inputs (裁定790point2: "シャードサイズと行範囲はdispatch
入力パラメータ化"), computed by the workflow's plan job and passed in via
--tree-start/--tree-end.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
sys.set_int_max_str_digits(0)  # B / CRT-mode entries can be very large; see
                                # torsweep_k13_hnf_construct_v1.py's own note.

import edim_semidirect_v1 as ed  # noqa: E402

K = 13
EXPECTED_H = 210  # 裁定735(6)


def load_h_basis(hnf_cert_path):
    with open(hnf_cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)
    assert cert["stages"]["verification_battery_all_pass"] is True, \
        "refusing to shard against an H_13 cert that did not pass its own battery"
    B = cert["H_basis"]
    H_rank = cert["H_rank"]
    dim_h = cert["dim_h"]
    assert H_rank == EXPECTED_H, (H_rank, EXPECTED_H)
    assert len(B) == H_rank and len(B[0]) == dim_h
    return B, H_rank, dim_h


def load_h_basis_modq(basis_modq_path, expected_prime):
    """裁定842(5): the full HNF cert (~356MB, entries to ~9720 digits) is
    git-ignored (裁定842(2), GitHub's 100MB/file limit) -- a GHA runner's
    checkout will NOT have it. search/torsweep_k13_materialize_modq_basis.
    py pre-reduces B mod each modq-lane prime into small (~1MB), COMMITTED
    files that ARE available on the runner; this loader reads one of
    those directly, already reduced, no huge-integer handling needed here
    at all."""
    with open(basis_modq_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    assert payload["schema"] == "tor_sweep_k13_basis_modq.1"
    assert payload["prime"] == expected_prime, (payload["prime"], expected_prime)
    B_modq = payload["B_modq"]
    H_rank = payload["H_rank"]
    dim_h = payload["dim_h"]
    assert H_rank == EXPECTED_H, (H_rank, EXPECTED_H)
    assert len(B_modq) == H_rank and len(B_modq[0]) == dim_h
    return B_modq, H_rank, dim_h


MODQ_SAFE_INT32_PRIME_BOUND = 2 ** 31  # all 3 commissioned primes qualify


def sparse_arrays_from_dense(restricted, mode, modulus):
    """(rows, cols, vals) numpy arrays for nonzero entries only -- 裁定867(2)
    replacement for the old Python-list sparse_triples_from_dense (OOM'd at
    ~10^8 nnz, see module docstring). rows/cols are int32 (row < H_rank<=
    210, col < ambient_dim_total ~1.6M -- both trivially fit); vals are
    int32 for modq mode (residues < modulus < 2**31 by construction) or a
    numpy object array of Python ints for crt mode (values can be
    arbitrarily large -- not optimized, deferred path)."""
    rows, cols = np.nonzero(restricted)
    vals_raw = restricted[rows, cols]
    rows = rows.astype(np.int32)
    cols = cols.astype(np.int32)
    if mode == "modq":
        if modulus >= MODQ_SAFE_INT32_PRIME_BOUND:
            raise ValueError(
                f"modq modulus {modulus} >= 2**31 -- int32 vals would not "
                f"be safe; this modulus is outside the set this shard "
                f"format was sized for (all 3 commissioned primes)")
        vals = vals_raw.astype(np.int32)
    else:
        vals = np.array([int(v) for v in vals_raw], dtype=object)
    return rows, cols, vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree-start", type=int, required=True)
    ap.add_argument("--tree-end", type=int, required=True)
    ap.add_argument("--mode", choices=["modq", "crt"], required=True)
    ap.add_argument("--modulus", type=int, required=True,
                     help="prime (modq mode) or large non-prime exact "
                          "modulus (crt mode, e.g. 10**40 or 10**40+15)")
    ap.add_argument("--hnf-cert", default=None,
                     help="path to the FULL (LOCAL ONLY, git-ignored per "
                          "裁定842(2)) k=13 HNF construction cert; if "
                          "omitted (and --basis-modq-file is also "
                          "omitted), the most recent matching file in "
                          "search/certs/ is used. NOT available on GHA "
                          "runners -- use --basis-modq-file for --mode "
                          "modq there instead.")
    ap.add_argument("--basis-modq-file", default=None,
                     help="--mode modq only (裁定842(5)): path to a small, "
                          "COMMITTED, pre-reduced-mod-this-prime basis "
                          "file (search/torsweep_k13_materialize_modq_"
                          "basis.py output, schema tor_sweep_k13_basis_"
                          "modq.1). If given, --hnf-cert / the full HNF "
                          "cert is never touched -- this is the path GHA "
                          "runners use.")
    ap.add_argument("--out", required=True,
                     help="output artifact path (.npz -- 裁定867(2); .npz "
                          "extension appended if not already present)")
    args = ap.parse_args()

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    p = args.modulus

    if args.basis_modq_file is not None:
        if args.mode != "modq":
            raise ValueError("--basis-modq-file is only valid with --mode modq")
        record(f"loading pre-reduced H_13 basis (mod {p}) from {args.basis_modq_file}")
        B_modq_list, H_rank, dim_h = load_h_basis_modq(args.basis_modq_file, p)
        hnf_cert_path = None
        subspace_basis_modq = np.array(B_modq_list, dtype=np.int64).T
    else:
        hnf_cert_path = args.hnf_cert
        if hnf_cert_path is None:
            import glob
            candidates = sorted(glob.glob(os.path.join(
                REPO_ROOT, "search", "certs", "torsweep_k13_hnf_construct_v1_*.json")))
            candidates = [c for c in candidates if not c.endswith("_RECEIPT.json")]
            if not candidates:
                raise FileNotFoundError(
                    "no torsweep_k13_hnf_construct_v1_*.json (non-receipt, "
                    "LOCAL) cert found -- on a GHA runner, use "
                    "--basis-modq-file instead (the full cert is not "
                    "checked out there, 裁定842(2))")
            hnf_cert_path = candidates[-1]
        record(f"loading H_13 basis from {hnf_cert_path}")
        B, H_rank, dim_h = load_h_basis(hnf_cert_path)
        record(f"H_rank={H_rank} dim_h={dim_h}")
        subspace_basis_modq = np.array(
            [[v % p for v in row] for row in B], dtype=np.int64).T
    assert subspace_basis_modq.shape == (dim_h, H_rank)

    record(f"building GradedLie(2,{K},{p})")
    h_alg2 = ed.GradedLie(2, K, p)
    n_trees = len(h_alg2.trees[K])
    assert dim_h == n_trees, (dim_h, n_trees)
    ts, te = args.tree_start, args.tree_end
    assert 0 <= ts <= te <= n_trees, (ts, te, n_trees)

    record(f"accumulate_nu_j_restricted_range(tree_start={ts}, tree_end={te}) "
           f"of {n_trees} total generator trees, mode={args.mode}")
    restricted, stats = ed.accumulate_nu_j_restricted_range(
        K, h_alg2, subspace_basis_modq, p, tree_start=ts, tree_end=te)
    elapsed = time.time() - t_start
    record(f"shard done, elapsed={elapsed:.2f}s")

    rows, cols, vals = sparse_arrays_from_dense(restricted, args.mode, p)
    nnz = len(vals)
    record(f"nnz(shard restricted)={nnz} (dense would be "
           f"{restricted.shape[0]}x{restricted.shape[1]}="
           f"{restricted.shape[0]*restricted.shape[1]} entries)")
    del restricted  # 裁定867(2): free the ~2.7GB dense array before the
                     # compression/write step below, not after -- reduces
                     # peak RSS during np.savez_compressed's own internal
                     # buffering.

    meta = {
        "schema": "tor_sweep_k13_shard_eval.2",
        "ruling_refs": ["裁定789", "裁定790", "裁定792", "裁定867"],
        "serialization_note": "npz (int32 rows/cols/vals for modq; object "
                               "array of Python ints for crt) -- replaces "
                               "schema .1's Python-list+json.dump(gzip) "
                               "format, which OOM'd at ~10^8 nnz "
                               "(裁定867(2), see module docstring).",
        "k": K,
        "mode": args.mode,
        "modulus": str(p),
        "tree_start": ts, "tree_end": te, "trees_total": n_trees,
        "H_rank": H_rank, "n_ambient_dim": stats["n_ambient_dim"],
        "h_ambient_dim": stats["h_ambient_dim"],
        "ambient_dim_total": stats["n_ambient_dim"] + stats["h_ambient_dim"],
        "basis_source": (
            {"kind": "basis_modq_file",
             "path": os.path.relpath(args.basis_modq_file, REPO_ROOT).replace(os.sep, "/")}
            if hnf_cert_path is None else
            {"kind": "hnf_cert",
             "path": os.path.relpath(hnf_cert_path, REPO_ROOT).replace(os.sep, "/")}
        ),
        "nnz": nnz,
        "elapsed_seconds": elapsed,
        "additivity_note": "this shard's restricted matrix is a PARTIAL sum "
                            "over generator trees [tree_start,tree_end) "
                            "only; the aggregate job must sum ALL shards "
                            "covering [0,trees_total) entrywise (mod "
                            "modulus for modq; as exact integers, no "
                            "reduction, for crt) to recover the full "
                            "restricted matrix -- see edim_semidirect_v1."
                            "accumulate_nu_j_restricted_range docstring "
                            "for the additivity argument.",
    }
    out_path = args.out if args.out.endswith(".npz") else args.out + ".npz"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    np.savez_compressed(
        out_path, rows=rows, cols=cols, vals=vals,
        meta=np.array(json.dumps(meta, ensure_ascii=False)))
    record(f"artifact written: {out_path} ({os.path.getsize(out_path)} bytes)")
    print(f"TORSWEEP_K13_SHARD_DONE tree_start={ts} tree_end={te} "
          f"mode={args.mode} modulus={p} nnz={nnz}", flush=True)


if __name__ == "__main__":
    main()
