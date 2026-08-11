#!/usr/bin/env python3
"""
torsweep_k13_shard_aggregate.py -- k=13 GHA row-shard aggregator (裁定789/
790/792). Runs LOCALLY (裁定789(2c)) after the workflow's shard artifacts
have been downloaded (retrieval is 司令塔's own step per 裁定680; assembly
is this script).

MODQ path (T2/T3, fully implemented): sums the sparse partial-restricted
artifacts for each of the 3 self-computed primes (裁定789(2a): no "儀式"
reuse exists for k=13, unlike k=12 -- 裁定785's trick does not apply here),
reconstructs the dense restricted matrix per prime, computes its rank via
the SAME rank_dense_restricted_ambient_modp certificate routine used
throughout this project, and produces a T2/T3-shaped cert (ranks_agree /
r_prime / dim_S_Q_byproduct), checked against the frozen calibration
values (裁定735(6): rank nu_13=207, dim S_13(Q)=3) as regression stops
(both ">207/<3" AND "<207/>3" are STOP -- raw values only, no judgement
words, S-TOR-4).

CRT path (T4/T5): the OPEN ITEM this module originally flagged (whether a
fixed "large enough" dual-modulus-agreement reconstruction, T1a's own
style, is safe at k=13's scale) has been RESOLVED by the mathematician,
裁定796(6) relay, spec: docs/notes/tor_sweep_design_v1_addendum_c.md
(e3f3c62), "SNF-MOD-13". Short version: exact reconstruction of N_13's
entries (or of a saturated basis at all) is NOT NEEDED -- elementary
divisors are determined entirely by (i) gcd of a few r'xr' minor
determinants (a genuine UPPER BOUND proof on the torsion support, not a
heuristic -- d_r | g always), (ii) mod-q rank deficiency per candidate
prime q|g (#{i: q|s_i} = r - rank_F_q(A), one modq pass per candidate, no
large numbers), (iii) mod q^N Smith form (q^N > g) ONLY for primes that
survive (ii), whose entries are provably < q^N <= q*g -- 4300-digit
entries never appear because HNF/saturated-basis construction was never
the right tool for elementary divisors, only a means to a saturated BASIS
(which the design/785/792's own theorem TOR-S3 and rank arguments never
actually needed to be saturated at this scale). HNF and LLL are explicitly
PROHIBITED by that spec ("禁止: HNF・LLL・飽和基底の明示構成"). Its own
canary requires reproducing k=12's ALREADY-KNOWN elementary divisors
(including the (32,5) precedent from D2-SNF-1, a different but
structurally analogous computation) before trusting the k=13 run.
THIS SCRIPT'S CRT-MODE PATH IS THEREFORE SUPERSEDED, NOT YET REWRITTEN:
the shard artifact format (sparse tree-range partials) and the modq
machinery below are directly reusable for SNF-MOD-13 steps (ii)/(iii)
(both are themselves modq-style computations, no new shard --mode is
obviously required -- to be confirmed when this is actually implemented);
step (i)'s minor-determinant machinery is new and not yet written here.
Per 裁定796(6): not urgent (mod-q lane / T2-T3 / P-a takes priority),
implementation deferred to after k=12 T4/T5 completes. The crt-mode
data-collection code below is LEFT AS-IS (harmless, produces raw sums of
whatever crt-mode shards exist) but should be read as provisional
scaffolding pending the SNF-MOD-13 rewrite, not as this module's intended
final T4/T5 path.
"""
import argparse
import glob
import json
import os
import sys
import time

import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
sys.set_int_max_str_digits(0)

import edim_semidirect_v1 as ed  # noqa: E402

K = 13
EXPECTED_H = 210
EXPECTED_S = 3          # 裁定735(6): dim S_13(Q)
EXPECTED_RANK_NU = 207  # 裁定735(6): rank nu_13 (= EXPECTED_H - EXPECTED_S)


def load_shards(shard_dir, mode):
    """裁定867(2): shard artifacts are now .npz (rows/cols/vals numpy
    arrays + a 'meta' entry holding the JSON metadata that used to be the
    whole payload in schema .1's Python-list+json.dump(gzip) format).
    Returns (path, payload) pairs where payload is the parsed meta dict
    with 'rows'/'cols'/'vals' (numpy arrays) merged in, so downstream code
    (check_coverage, sum_shards_modp, the crt-mode raw summary) reads the
    same field names as before."""
    paths = sorted(glob.glob(os.path.join(shard_dir, "*.npz")))
    shards = []
    for path in paths:
        with np.load(path, allow_pickle=True) as npz:
            meta = json.loads(str(npz["meta"]))
            if meta["mode"] != mode:
                continue
            payload = dict(meta)
            payload["rows"] = npz["rows"]
            payload["cols"] = npz["cols"]
            payload["vals"] = npz["vals"]
        shards.append((path, payload))
    return shards


def check_coverage(shards, trees_total):
    """Every shard must belong to the SAME modulus group; the union of
    [tree_start,tree_end) ranges must be EXACTLY [0,trees_total) with no
    gaps and no overlaps (each generator tree contributes exactly once)."""
    ranges = sorted((p["tree_start"], p["tree_end"]) for _, p in shards)
    cursor = 0
    for a, b in ranges:
        if a != cursor:
            raise ValueError(f"coverage gap/overlap: expected next tree_start="
                              f"{cursor}, got {a} (ranges={ranges})")
        cursor = b
    if cursor != trees_total:
        raise ValueError(f"coverage incomplete: covered up to {cursor}, "
                          f"need {trees_total} (ranges={ranges})")
    return ranges


def sum_shards_modp(shards, H_rank, ambient_dim_total, p):
    """裁定867(2): vectorized (np.add.at, index-repeat-safe -- distinct
    shards/generator-trees can and do contribute to the same (row,col)
    ambient position, so a plain fancy-index assignment would silently
    drop all but the last write) instead of the old per-element Python
    loop. Also fixes a latent correctness gap in the old version: it took
    '% p' after EACH single-triple addition rather than after summing all
    contributions, which is equivalent here since modular addition
    commutes/associates fine either way -- but doing it once at the end
    over the whole array is what makes the vectorized form possible."""
    dense = np.zeros((H_rank, ambient_dim_total), dtype=np.int64)
    for _, payload in shards:
        rows = payload["rows"].astype(np.int64)
        cols = payload["cols"].astype(np.int64)
        vals = payload["vals"].astype(np.int64)
        np.add.at(dense, (rows, cols), vals)
    dense %= p
    return dense


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard-dir", required=True,
                     help="directory containing downloaded *.npz shard artifacts (裁定867(2))")
    ap.add_argument("--hnf-cert", default=None)
    ap.add_argument("--primes", default="", help="comma-separated modq primes "
                     "expected (for coverage/T-c bookkeeping; if omitted, "
                     "inferred from the shard artifacts present)")
    args = ap.parse_args()

    t_start = time.time()

    def record(msg):
        print(f"[{time.time()-t_start:8.2f}s] {msg}", flush=True)

    hnf_cert_path = args.hnf_cert
    if hnf_cert_path is None:
        candidates = sorted(glob.glob(os.path.join(
            REPO_ROOT, "search", "certs", "torsweep_k13_hnf_construct_v1_*.json")))
        if not candidates:
            raise FileNotFoundError("no torsweep_k13_hnf_construct_v1_*.json cert found")
        hnf_cert_path = candidates[-1]
    with open(hnf_cert_path, "r", encoding="utf-8") as f:
        hnf = json.load(f)
    H_rank = hnf["H_rank"]
    dim_h = hnf["dim_h"]
    assert H_rank == EXPECTED_H, (H_rank, EXPECTED_H)
    record(f"H_rank={H_rank} dim_h={dim_h} (from {hnf_cert_path})")

    cert = {
        "schema": "tor_sweep_k13_shard_aggregate.2",
        "ruling_refs": ["裁定735(6)", "裁定789", "裁定790", "裁定792", "裁定867"],
        "k": K,
        "hnf_cert_path": os.path.relpath(hnf_cert_path, REPO_ROOT).replace(os.sep, "/"),
        "H_rank": H_rank, "dim_h": dim_h,
        "stages": {}, "canaries": {}, "stop_rules": {},
    }

    # =========================================================================
    # MODQ path -- T2/T3 (fully implemented)
    # =========================================================================
    modq_shards_all = load_shards(args.shard_dir, "modq")
    by_prime = {}
    for path, payload in modq_shards_all:
        by_prime.setdefault(payload["modulus"], []).append((path, payload))

    if args.primes:
        expected_primes = [s.strip() for s in args.primes.split(",") if s.strip()]
    else:
        expected_primes = sorted(by_prime.keys(), key=int)
    record(f"modq primes present: {sorted(by_prime.keys(), key=int)}, "
           f"expected: {expected_primes}")

    per_prime = {}
    n_ambient_dim = None
    ambient_dim_total = None
    for q_str in expected_primes:
        q = int(q_str)
        shards = by_prime.get(q_str, [])
        if not shards:
            record(f"WARNING: no shards found for prime {q}")
            continue
        _, sample = shards[0]
        trees_total = sample["trees_total"]
        n_ambient_dim = sample["n_ambient_dim"]
        ambient_dim_total = sample["ambient_dim_total"]
        ranges = check_coverage(shards, trees_total)
        record(f"prime={q}: {len(shards)} shards, coverage OK "
               f"({len(ranges)} ranges over [0,{trees_total}))")
        dense = sum_shards_modp(shards, H_rank, ambient_dim_total, q)
        nnz_total = int(np.count_nonzero(dense))
        rank, rank_cert = ed.rank_dense_restricted_ambient_modp(
            dense, q, tag_boundary=n_ambient_dim)
        per_prime[q_str] = {
            "rank": int(rank), "nnz_reconstructed": nnz_total,
            "shard_count": len(shards),
        }
        record(f"prime={q}: rank={rank} nnz_reconstructed={nnz_total}")

    ranks = [per_prime[q]["rank"] for q in expected_primes if q in per_prime]
    canary_Tc_pass = (len(ranks) == len(expected_primes) and len(set(ranks)) == 1)
    r_prime = ranks[0] if canary_Tc_pass and ranks else None
    dim_S_Q = (H_rank - r_prime) if r_prime is not None else None
    rank_nu_matches_expected = (r_prime == EXPECTED_RANK_NU) if r_prime is not None else False
    dim_S_matches_expected = (dim_S_Q == EXPECTED_S) if dim_S_Q is not None else False

    cert["stages"]["T2_T3"] = {
        "per_prime": per_prime,
        "ranks_agree": canary_Tc_pass,
        "r_prime": r_prime,
        "dim_S_Q_byproduct": dim_S_Q,
        "rank_nu13_matches_expected_207": rank_nu_matches_expected,
        "dim_S13_Q_matches_expected_3": dim_S_matches_expected,
    }
    cert["canaries"]["T-c"] = {
        "ranks_by_prime": {q: per_prime[q]["rank"] for q in per_prime},
        "pass": canary_Tc_pass,
    }
    record(f"T2/T3: r_prime={r_prime} dim_S_Q={dim_S_Q} "
           f"(expected rank_nu13={EXPECTED_RANK_NU}, dim_S13={EXPECTED_S}) "
           f"canary_Tc_pass={canary_Tc_pass}")

    # 裁定735(6): "分岐表: >3 も <3 も STOP 生値報告" -- BOTH directions of
    # mismatch are a STOP, not just an upward surprise. Raw values only, no
    # judgement words.
    if not canary_Tc_pass:
        cert["stop_rules"]["S-TOR-1"] = {
            "triggered": True,
            "reason": "LATTICE_CANARY_FAIL (T-c, prime rank disagreement or "
                      "missing shard coverage for one or more primes)",
        }
    elif not (rank_nu_matches_expected and dim_S_matches_expected):
        cert["stop_rules"]["S-TOR-2"] = {
            "triggered": True,
            "reason": f"branch table (裁定735(6)): r_prime={r_prime} "
                      f"(expected {EXPECTED_RANK_NU}), dim_S_Q={dim_S_Q} "
                      f"(expected {EXPECTED_S}) -- BOTH directions of "
                      f"mismatch are STOP per 裁定735(6), raw values only",
        }

    # =========================================================================
    # CRT path -- T4/T5 raw data collection ONLY.
    #
    # OPEN ITEM (flagged, not silently resolved): the T1a HNF construction
    # cert's own H_basis entries already exceed 4300 decimal digits (this
    # script's own sys.set_int_max_str_digits(0) call exists because of
    # that, see torsweep_k13_hnf_construct_v1.py). The N_13 restricted
    # matrix's TRUE (unreduced) entries are linear combinations of those
    # already-huge B coefficients against tree-evaluation coefficients, so
    # they are very likely FAR larger than any fixed "large enough" modulus
    # like 10**40 -- meaning the repo's existing "two large non-prime
    # moduli, require exact agreement" convention (used successfully for
    # T1a's theta/tau, where entries stayed small, max_abs ~80000) is NOT
    # obviously safe to reuse here without an actual magnitude bound.
    # A real Chinese-Remainder-Theorem reconstruction over enough DISTINCT
    # PRIME moduli (not a fixed huge non-prime one) is the standard fix,
    # but needs either (a) a magnitude bound on the true entries/minors to
    # know how many primes are enough, or (b) restricting T4/T5 to ONLY the
    # r' pivot ambient columns identified by the T2/T3 mod-q stage (design
    # note's own §3.2 intent: a handful of small r'xr' minors, not the full
    # matrix) and CRT-reconstructing just those r'^2 entries or even just
    # the handful of Bareiss DETERMINANTS directly (computing det mod many
    # primes, then CRT-combining the determinant residues, needs a
    # Hadamard-type bound on |det| instead of on individual entries -- the
    # design's own TOR-DET write-up assumes ordinary bounded-size integer
    # arithmetic once the r'xr' submatrix is in hand, which was true at
    # k<=12's H_rank<=112 scale but is UNVERIFIED at k=13's H_rank=210 /
    # much larger B-entry-magnitude scale).
    # This script therefore only RE-SUMS whatever crt-mode shards are
    # present (their raw per-shard "modulus" value is honored as reported,
    # no assumption that summing two of them and checking equality is a
    # valid exactness proof at this scale) and reports the raw sums's
    # digest for the coordinator/mathematician to decide the reconstruction
    # method BEFORE this aggregate's crt output is trusted for TOR-DET.
    # =========================================================================
    crt_shards_all = load_shards(args.shard_dir, "crt")
    if crt_shards_all:
        by_modulus = {}
        for path, payload in crt_shards_all:
            by_modulus.setdefault(payload["modulus"], []).append((path, payload))
        crt_summary = {}
        for mod_str, shards in by_modulus.items():
            _, sample = shards[0]
            trees_total = sample["trees_total"]
            ranges = check_coverage(shards, trees_total)
            total_nnz = sum(p["nnz"] for _, p in shards)
            crt_summary[mod_str] = {
                "shard_count": len(shards), "coverage_ranges": ranges,
                "total_nnz_across_shards_unmerged": total_nnz,
            }
        cert["stages"]["T4_T5_crt_raw"] = {
            "moduli_present": list(by_modulus.keys()),
            "summary": crt_summary,
            "reconstruction_method": "NOT YET DECIDED -- see module "
                                      "docstring 'OPEN ITEM'. This stage "
                                      "does not compute a TOR-DET gcd or "
                                      "any torsion-prime claim.",
        }
        record(f"CRT/T4-T5: {len(crt_shards_all)} shards present across "
               f"{len(by_modulus)} moduli -- raw summary only, "
               f"reconstruction method open (see module docstring)")
    else:
        record("CRT/T4-T5: no crt-mode shards present in this shard-dir "
               "(expected if only the T2/T3 modq dispatch has run so far)")

    cert["stop_rules"]["S-TOR-4"] = {
        "note": "no judgement words emitted anywhere in this cert; raw "
                "values and booleans only",
    }
    cert["total_elapsed_seconds"] = time.time() - t_start
    write_cert(cert)
    record(f"DONE. total_elapsed={cert['total_elapsed_seconds']:.2f}s")


def write_cert(cert):
    import time as _time
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    os.makedirs(out_dir, exist_ok=True)
    date_str = _time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k13_shard_aggregate_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
