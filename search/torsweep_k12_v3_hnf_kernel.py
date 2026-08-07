#!/usr/bin/env python3
"""
torsweep_k12_v3_hnf_kernel.py -- k=12 T1 (H_basis) RECONSTRUCTED from
scratch via direct integer-kernel (column-HNF/unimodular-transform)
construction, per 裁定754(2): the "根治" (root-cause fix) for the
saturation-defect line of investigation in torsweep_k12_v2_saturate.py
(cert torsweep_k12_v2_saturate_20260807.json).

Diagnosis accepted (裁定754): the OLD construction (rational nullspace via
sympy DomainMatrix/QQ, THEN per-row denominator-LCM clearing, THEN a
bounded-small-prime-list p-saturation refinement) is a "pivot-prime
contamination generator" -- ANY prime that happens to divide one of those
per-row denominator LCMs is a candidate for under-saturation, and the
bounded small-prime sieve (max_prime_bound=2000) can only ever catch a
finite, arbitrarily-incomplete subset of them. This was demonstrated
directly in this run's own development: g=632246415007 (12 digits, first
escaped the sieve), then after fixing g, SIX MORE distinct primes surfaced
in a fresh sat_gcd computation (185189527, 23632759, and four ~9-10 digit
primes from a 37-digit composite), and a 458-digit residual with a
CONFIRMED real deficiency (Howell full-column rank=111/112, decisive, not
an artifact) that a 180s-bounded sympy.factorint could not resolve.

裁定754's ruling: that 458-digit residual is NOT a mathematical finding --
it is a contamination artifact of the OLD construction method, and
factoring it (however long it takes) would answer a question about our own
scaffolding, not about the lattice. The correct move is to abandon
denominator-clearing + prime-hunting entirely and construct H_12^Z the way
that is AUTOMATICALLY saturated by definition:

    Classical fact (used here, not reproven): for an integer matrix
    A: Z^n -> Z^m, if one computes ker_Z(A) via a sequence of ELEMENTARY
    UNIMODULAR COLUMN OPERATIONS on A (i.e. right-multiplication by
    matrices in GL_n(Z), the same operations used to compute a column
    Hermite Normal Form), tracking the accumulated unimodular matrix U
    (so that A@U has some columns identically zero), then the columns of U
    corresponding to A@U's zero columns are, essentially by construction
    (they are literal coordinate directions of a GL_n(Z)-transformed
    basis of Z^n), an INTEGER BASIS OF ker_Z(A) THAT IS AUTOMATICALLY
    SATURATED -- no separate saturation step, no prime search, ever.

Algorithm (implemented here, fraction-free, exact, no primality needed
anywhere): process A's m=670 rows one at a time. For each row, among the
"active" columns (not yet frozen as an earlier row's pivot), use the
extended Euclidean algorithm to combine pairs of columns so that AT MOST
ONE active column is nonzero at this row; if exactly one remains nonzero,
freeze it as this row's pivot column (remove from the active set, apply
the SAME combination to the tracked U). This never divides, only combines
integer columns via unimodular (determinant +-1) 2x2 blocks, so U's
columns stay exact integers throughout, and never touches an already-
frozen column again -- so once a column becomes zero at an earlier row, it
stays zero there for the rest of the run (standard column-echelon
invariant, proved in-line in the module docstring... argument omitted
here for brevity; see LEDGER/report for the induction). After all m rows
are processed, the surviving ACTIVE columns of U are IDENTICALLY ZERO in
every row of A (i.e. A@(active columns)=0 exactly) and span ker_Z(A) as a
saturated Z-submodule.

Verification battery (裁定754③, reusing the primes this run's OWN
gcd-driven-loop already discovered as real defects, per instruction):
  (a) rank(B mod p) == 112 for p in {the 303-prime sieve used by v1/v2} +
      {632246415007 (g), 185189527, 23632759, 192267763, 1129116397,
      6392843131, 1840125437} (all previously-confirmed-real-defect
      primes from this run's own history) -- via the SAME independent
      row/column rank routine used throughout (row_dependency_mod_p /
      independent_columns_modp), NOT trusting the construction method.
  (b) M @ B^T == 0 exact (integer, no modular reduction).
  (c) sat_gcd (gcd of several Bareiss H_rankxH_rank minors) recomputed
      fresh; expected unit-level (per 裁定754, this construction has no
      structural reason to produce a nontrivial sat_gcd). If sat_gcd != 1,
      NO FACTORING is attempted (裁定754's own lesson): the residual is
      closed via ONE direct Howell run (target r_prime=H_rank) -- TOR-DET's
      own asymmetry (innocent needs no factoring; only a genuine defect
      would need it, and per 裁定754 a genuine defect at this stage would
      itself be a new, real finding worth escalating, not scaffolding
      noise).

No judgement words emitted (S-TOR-4): raw values/booleans only.
"""
import hashlib
import json
import os
import random
import sys
import time
from math import gcd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
from torsweep_k12_run import (  # noqa: E402
    det_bareiss, small_primes, row_dependency_mod_p, sha256_of_file,
    ext_gcd,
)
from torsweep_k11_close_v1_4 import close_modulus_full  # noqa: E402

K = 12
EXPECTED_H = 112
V1_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs", "torsweep_k12_v1_20260807.json")

# Primes this run's OWN gcd-driven-loop (torsweep_k12_v2_saturate.py)
# already confirmed as REAL defects of the OLD construction (裁定754(3):
# "発見済み欠陥素数群の転用"). Reused here purely as a verification
# battery against the NEW construction -- not as a candidate-bounding
# list for discovering anything new (that role is filled by (c)'s
# unbounded-Howell / no-factoring step).
KNOWN_HISTORICAL_DEFECT_PRIMES = [
    632246415007,  # g, 裁定745(1)
    185189527, 23632759,  # found in this run's iteration-1 residual closure
    192267763, 1129116397, 6392843131, 1840125437,  # 37-digit leaf factors
]


def integer_kernel_via_unimodular_columns(A, record):
    """A: list of m rows, each length n (exact ints). Returns (B, U_full,
    active_final, stats) where B is the list of kernel basis rows (each
    length n), extracted from U's active columns at the end -- see module
    docstring for the algorithm and correctness argument."""
    m = len(A)
    n = len(A[0]) if m else 0
    # Represent A and U by COLUMNS for cheap column-combination.
    A_cols = [[A[i][j] for i in range(m)] for j in range(n)]
    U_cols = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
    active = list(range(n))
    pivots_found = 0
    combine_ops = 0
    max_abs_seen = 0
    t0 = time.time()
    for row in range(m):
        # active columns with nonzero entry at this row
        nz = [j for j in active if A_cols[j][row] != 0]
        while len(nz) > 1:
            # *** growth-control fix (found during this run's own
            # development): combining via a single extended-gcd Bezout
            # step (x*a+y*b=g) can produce ARBITRARILY LARGE multipliers
            # x,y when a,b are large and gcd(a,b) is small -- this caused
            # the first version of this algorithm to stall (entries
            # blowing up) around row ~100-200 of 670. FIX: reduce each
            # pair via REPEATED EUCLIDEAN SUBTRACTION (a,b) -> (b, a mod
            # b) instead of a single Bezout combination -- every step is
            # still a unimodular (det +-1) column operation (composition
            # of unimodular is unimodular), but coefficient growth is the
            # SAME polynomial growth as the ordinary Euclidean algorithm,
            # not the potentially-exponential Bezout-multiplier blowup.
            # Smallest-magnitude-first pairing (sort nz by |entry|) is a
            # further standard control, applied here too.
            nz.sort(key=lambda j: abs(A_cols[j][row]))
            j0, j1 = nz[0], nz[1]
            Ca_A, Ca_U = A_cols[j0], U_cols[j0]
            Cb_A, Cb_U = A_cols[j1], U_cols[j1]
            while Cb_A[row] != 0:
                # (a,b) -> (b, a - q*b), q = a//b. NOTE: do NOT special-
                # case q==0 as "leave b unchanged" -- that was a bug found
                # during this run's own development (when |a|<|b|, q==0,
                # and the correct new_Cb is a - 0*b = a, i.e. a COPY of
                # Ca, not the old Cb left alone; the shortcut silently
                # corrupted the invariant and produced a wrong kernel
                # dimension, 149 instead of 112, caught by the (3a) rank
                # battery / regression check below -- always compute the
                # general formula, it is correct for every q including 0).
                q = Ca_A[row] // Cb_A[row]
                new_Cb_A = [Ca_A[i] - q * Cb_A[i] for i in range(m)]
                new_Cb_U = [Ca_U[i] - q * Cb_U[i] for i in range(n)]
                Ca_A, Ca_U, Cb_A, Cb_U = Cb_A, Cb_U, new_Cb_A, new_Cb_U
                combine_ops += 1
            A_cols[j0], U_cols[j0] = Ca_A, Ca_U
            A_cols[j1], U_cols[j1] = Cb_A, Cb_U
            assert A_cols[j1][row] == 0, (row, j0, j1, A_cols[j1][row])
            nz = [j for j in nz if j != j1]
            # (j0 keeps its place in nz with the new combined value g,
            # possibly still nonzero -- correct, continue reducing)
        if len(nz) == 1:
            piv = nz[0]
            active.remove(piv)
            pivots_found += 1
        if row % 100 == 0:
            cur_max = max((abs(v) for j in active for v in
                            (A_cols[j][row:row + 1] or [0])), default=0)
            max_abs_seen = max(max_abs_seen, cur_max)
            record(f"  row {row}/{m}: active={len(active)} pivots_found="
                   f"{pivots_found} combine_ops={combine_ops} "
                   f"elapsed={time.time()-t0:.1f}s")
    record(f"integer_kernel: done, {pivots_found} pivots, {combine_ops} "
           f"combine ops, {len(active)} kernel dims, elapsed={time.time()-t0:.1f}s")
    B = [U_cols[j] for j in active]  # each length n; B is len(active) x n
    return B, U_cols, active, {
        "pivots_found": pivots_found, "combine_ops": combine_ops,
        "elapsed_seconds": time.time() - t0,
    }


def independent_columns_modp(rows_as_matrix, p, order):
    pivots = {}
    selected = []
    for col in order:
        vec = {i: rows_as_matrix[i][col] % p for i in range(len(rows_as_matrix))
               if rows_as_matrix[i][col] % p}
        while vec:
            piv = min(vec)
            old = pivots.get(piv)
            if old is None:
                inv = pow(vec[piv], p - 2, p)
                vec = {i: (v * inv) % p for i, v in vec.items() if v % p}
                pivots[piv] = vec
                selected.append(col)
                break
            factor = vec[piv]
            for i, v in old.items():
                nv = (vec.get(i, 0) - factor * v) % p
                if nv:
                    vec[i] = nv
                else:
                    vec.pop(i, None)
        if len(selected) == len(rows_as_matrix):
            break
    return selected


def compute_sat_gcd(B, H_rank, dim_h, big_prime, record, num_minors=4):
    orders = []
    base_order = list(range(dim_h))
    orders.append(base_order)
    r1 = base_order[:]
    random.shuffle(r1)
    orders.append(r1)
    r2 = base_order[:]
    random.shuffle(r2)
    orders.append(r2)
    orders.append(list(reversed(base_order)))
    minor_dets = []
    minor_col_sets = []
    seen = set()
    for order in orders:
        cols = independent_columns_modp(B, big_prime, order)
        if len(cols) != H_rank:
            continue
        key = tuple(sorted(cols))
        if key in seen:
            continue
        seen.add(key)
        submat = [[B[i][c] for c in cols] for i in range(H_rank)]
        d = det_bareiss(submat)
        minor_dets.append(d)
        minor_col_sets.append(cols)
        if len(minor_dets) >= num_minors:
            break
    sat_gcd = 0
    for d in minor_dets:
        sat_gcd = gcd(sat_gcd, abs(d))
    record(f"compute_sat_gcd: {len(minor_dets)} minors, digit_counts="
           f"{[len(str(d)) for d in minor_dets]}, sat_gcd_digits={len(str(sat_gcd))}")
    return sat_gcd, minor_dets, minor_col_sets


def main():
    log = []
    t_start = time.time()

    def record(msg):
        line = f"[{time.time() - t_start:8.2f}s] {msg}"
        print(line, flush=True)
        log.append(line)

    record("loading torsweep_k12_v1 cert (M only -- B is NOT reused, "
           "rebuilt from scratch per 裁定754)")
    with open(V1_CERT_PATH, "r", encoding="utf-8") as f:
        v1 = json.load(f)
    t1 = v1["stages"]["T1"]
    M = t1["M"]
    dim_h = t1["M_shape"][1]
    m_rows = t1["M_shape"][0]
    assert len(M) == m_rows and len(M[0]) == dim_h
    big_prime = 2147483647
    record(f"loaded: M shape=({m_rows},{dim_h})")

    cert = {
        "schema": "tor_sweep_k12_v3_hnf_kernel.1",
        "supersedes_within_pipeline": ["search/certs/torsweep_k12_v2_saturate_20260807.json"],
        "supersedes_note": "根治(裁定754): H_basis を有理核+分母クリアリング"
                            "+p-飽和(prime-hunting)から、整数核の直接構成"
                            "(column-HNF/ユニモジュラ変換Uの追跡)へ全面差替え。"
                            "素数探索を一切経由しない -- 整数解の全格子は"
                            "定義により飽和(saturated by construction)。",
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "ruling_refs": ["裁定745", "裁定754"],
        "lessons": [
            "単素数飽和の干渉(第2実証): 欠陥素数を1個ずつ孤立して"
            "fixed-point 飽和すると、直前まで無罪だった別の素数に新たな"
            "欠陥を作り得る(裁定745(5)実行時、gを単独飽和したところp=3が"
            "壊れた)。joint fixed-point でも原理的には有限回で収束するが、"
            "「壊れては直す」を繰り返すたびに未知の素数が追加で湧く"
            "(この実行では合計6個+458桁未解決の追加欠陥を発見) -- 根治には"
            "ならない。",
            "有理解+分母クリアリングは pivot 素数汚染を量産する ⟹ "
            "飽和保証構成(整数核の直接構成・column-HNF/ユニモジュラ U 追跡)"
            "が正典。素数を探す作業自体が構築法の欠陥の症状であり、"
            "見つけた素数を1個ずつ潰すのは対症療法に過ぎない。",
        ],
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k12_v3_hnf_kernel.py",
            "python": sys.version,
            "torsweep_k12_run_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k12_run.py")),
            "torsweep_k11_close_v1_4_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k11_close_v1_4.py")),
        },
        "stages": {},
    }

    # =========================================================================
    # (2) integer kernel via unimodular column operations (no primes, no
    # denominators, automatically saturated by construction)
    # =========================================================================
    record("(2) integer_kernel_via_unimodular_columns(M) -- exact, no "
           "primes, no fractions")
    B, U_full, active, kstats = integer_kernel_via_unimodular_columns(M, record)
    H_rank = len(B)
    record(f"(2) kernel dimension = {H_rank} (expected {EXPECTED_H})")
    cert["stages"]["kernel_construction"] = {
        "H_rank": H_rank,
        "H_rank_matches_expected": (H_rank == EXPECTED_H),
        "pivots_found": kstats["pivots_found"],
        "combine_ops": kstats["combine_ops"],
        "elapsed_seconds": kstats["elapsed_seconds"],
        "max_abs_entry_in_B": max((abs(v) for row in B for v in row), default=0),
    }
    if H_rank != EXPECTED_H:
        cert.setdefault("stop_rules", {})["S-TOR-2"] = {
            "triggered": True,
            "reason": f"kernel dimension {H_rank} != EXPECTED_H {EXPECTED_H}",
        }
        write_cert(cert, log)
        record("STOP: kernel dimension regression")
        return

    # =========================================================================
    # (3)(b) exact M @ B^T == 0
    # =========================================================================
    record("(3b) exact M@B^T residual check")
    residual_nonzero = 0
    for brow in B:
        for mrow in M:
            s = sum(mrow[j] * brow[j] for j in range(dim_h))
            if s != 0:
                residual_nonzero += 1
    record(f"(3b) M@B^T residual_nonzero_entries={residual_nonzero} (expect 0)")
    cert["stages"]["MBt_check"] = {"residual_nonzero_entries": residual_nonzero}
    if residual_nonzero != 0:
        cert.setdefault("stop_rules", {})["S-TOR-1"] = {
            "triggered": True,
            "reason": "M@B^T != 0 -- STOP, no judgement word (should be "
                      "impossible by construction; indicates a bug)",
        }
        write_cert(cert, log)
        record("STOP: kernel check failed")
        return

    # =========================================================================
    # (3)(a) rank mod {303-prime sieve + all historically-discovered defect
    # primes} == H_rank, via the SAME independent rank routine used
    # throughout this line of work (not trusting the construction).
    # =========================================================================
    record("(3a) rank(B mod p) == H_rank for the 303-prime sieve + all "
           "historically-discovered defect primes")
    test_primes = sorted(set(small_primes(2000)) | set(KNOWN_HISTORICAL_DEFECT_PRIMES))
    rank_results = {}
    all_rank_pass = True
    for p in test_primes:
        dep = row_dependency_mod_p(B, p)
        ok = (dep is None)
        rank_results[str(p)] = ok
        if not ok:
            all_rank_pass = False
            record(f"(3a) FAIL at p={p}: row_dependency_mod_p found a "
                   f"dependency (rank < {H_rank})")
    record(f"(3a) tested {len(test_primes)} primes, all_pass={all_rank_pass}")
    cert["stages"]["rank_battery"] = {
        "primes_tested_count": len(test_primes),
        "historical_defect_primes_included": KNOWN_HISTORICAL_DEFECT_PRIMES,
        "all_pass": all_rank_pass,
        "failures": [p for p, ok in rank_results.items() if not ok],
    }
    if not all_rank_pass:
        cert.setdefault("stop_rules", {})["S-TOR-1"] = {
            "triggered": True,
            "reason": "rank battery failed at one or more primes -- STOP, "
                      "no judgement word",
            "failed_primes": [p for p, ok in rank_results.items() if not ok],
        }
        write_cert(cert, log)
        record("STOP: rank battery failed")
        return

    # =========================================================================
    # (3)(c) sat_gcd recompute; expect unit-level. If not, ONE direct
    # Howell run on the residual -- NO FACTORING (裁定754's own lesson).
    # =========================================================================
    record("(3c) sat_gcd recompute (fresh minors on the NEW B)")
    sat_gcd, minor_dets, minor_col_sets = compute_sat_gcd(
        B, H_rank, dim_h, big_prime, record)
    cert["stages"]["sat_gcd_check"] = {
        "sat_gcd_digits": len(str(sat_gcd)),
        "sat_gcd": str(sat_gcd) if len(str(sat_gcd)) < 300 else
                   f"{str(sat_gcd)[:50]}...({len(str(sat_gcd))} digits)",
    }
    if sat_gcd == 1:
        record("(3c) sat_gcd == 1 -- fully saturated, no closure needed")
        cert["stages"]["sat_gcd_check"]["closure_needed"] = False
        battery_pass = True
    else:
        record(f"(3c) sat_gcd != 1 ({len(str(sat_gcd))} digits) -- closing "
               f"via ONE direct Howell run (no factoring attempted, per "
               f"裁定754)")
        cols = {j: [B[i][j] % sat_gcd for i in range(H_rank)] for j in range(dim_h)}
        closures = close_modulus_full(cols, sat_gcd, H_rank, H_rank, record)
        all_success = all(c["status"] == "success" for c in closures)
        cert["stages"]["sat_gcd_check"]["closure_needed"] = True
        cert["stages"]["sat_gcd_check"]["closures_summary"] = [
            {"modulus_digits": len(c["modulus"]), "status": c["status"]}
            for c in closures
        ]
        cert["stages"]["sat_gcd_check"]["all_pieces_success"] = all_success
        battery_pass = all_success
        if not all_success:
            cert.setdefault("stop_rules", {})["S-TOR-1"] = {
                "triggered": True,
                "reason": "sat_gcd closure did not succeed on all pieces "
                          "-- STOP, no judgement word (this WOULD be a "
                          "genuine finding, not scaffolding noise, since "
                          "the new construction has no denominator-"
                          "clearing step to blame)",
            }

    cert["stages"]["verification_battery_all_pass"] = (
        all_rank_pass and residual_nonzero == 0 and (H_rank == EXPECTED_H) and battery_pass
    )
    record(f"verification_battery_all_pass="
           f"{cert['stages']['verification_battery_all_pass']}")

    if not battery_pass:
        write_cert(cert, log)
        record("STOP: sat_gcd closure failed")
        return

    cert["H_basis"] = B
    cert["H_rank"] = H_rank
    cert["dim_h"] = dim_h
    cert["M_shape"] = [m_rows, dim_h]
    cert["total_elapsed_seconds"] = time.time() - t_start
    write_cert(cert, log)
    record(f"DONE. verification_battery_all_pass=True total_elapsed="
           f"{cert['total_elapsed_seconds']:.2f}s")


def write_cert(cert, log_lines):
    cert["run_log"] = log_lines
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k12_v3_hnf_kernel_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
