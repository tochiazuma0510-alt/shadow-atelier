#!/usr/bin/env python3
"""
edim_run_c12_single_prime.py -- E-DIM12/691 ceremony, per-PRIME run (裁定656
frozen spec / 裁定692 GHA relocation / 裁定693 dispatch instruction).

Usage: python search/edim_run_c12_single_prime.py <prime>

Log discipline (裁定692 verbatim, "段境界のみ" -- NO hot-loop/progress-spam
prints): this script prints ONLY at phase boundaries -- job start, each
DEGREE's completion (one line per k, not per inner iteration), a memory
snapshot at each degree boundary, and the final summary line at job end.
compute_H_S_at_k_safe (imported unchanged from edim_run_c9_c10_v3_single_
prime.py, Sol's 112e accelerator) is NOT modified and contains no prints of
its own already.

Calibration gate (裁定656/693): H12 must equal 112 (the DERIVED value,
docs/notes/b_type_synthesis_design_v1_addendum_l4b_grt12.md; formula
dim H_k = (Witt(2,k) - ch_k(tau))/3, verified by hand for k=12: Witt(2,12)=
335, ch_12(tau)=-1, H12=(335-(-1))/3=112). If H12 != 112 (at this prime, or
if the k=3..11 known-value sweep mismatches anywhere first), this script
STOPS before reporting S12 -- CALIBRATION_FAIL, per instruction.

This script does NOT write any interpretive verdict text (no "SYN-0",
"k*=12", "段差" language) -- raw H/S values and match flags only, per
instruction ("判定文はコードが書かない"). Interpretation is the aggregate
cert's job to abstain from too; verdict authorship belongs to
司令塔/数学者/Sol.

k=13 is NOT run (out of scope; separate future ceremony if ever authorized).
"""
import json
import sys
import time

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
from edim_run_c9_c10_v3_single_prime import compute_H_S_at_k_safe, peak_rss_mb

KMAX = 12
EXPECTED_H = {3: 1, 4: 1, 5: 2, 6: 3, 7: 6, 8: 10, 9: 19, 10: 33, 11: 62, 12: 112}
EXPECTED_S = {3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 1, 9: 1, 10: 1, 11: 2}  # S12 has no
# "expected" entry -- it is NOT pre-declared as pass/fail criteria (per
# 裁定656's frozen judgment table, S12 is the OBSERVATION itself, not scored
# against a predicted value the way k=3..11 were).

UNITS = {
    "H_dim": "dim_Q H_k (hexagon homogeneous solution space in L_k(x,y)), a "
             "non-negative integer, exact mod p (not an estimate)",
    "S_dim": "dim_Q S_k = dim_Q (H_k cap ker(nu_k . j)), a non-negative "
             "integer, exact mod p (not an estimate)",
    "elapsed_sec": "wall-clock seconds for this degree's compute_H_S_at_k_safe call",
    "peak_rss_mb": "process peak resident set size in MiB at this point (OS-level, "
                    "not Python-heap-only; see edim_run_c9_c10_v3_single_prime.peak_rss_mb)",
}
PREREG_REFS = {
    "656": "provenance/LEDGER.md 裁定656 (k=12 仕様完全凍結: A表12/12一次pin, "
           "D_12構造昇格, k=12判定表凍結, 素数系列2147483647/998244353/691(+条件付677,701))",
    "692": "provenance/LEDGER.md 裁定692 (k=12/691 ceremonyはGHA実行で確定: 素数別matrix+aggregate, "
           "16GB runner, 裁定656の判定表/S-ED-7のまま, ログ段境界のみ)",
    "693": "provenance/LEDGER.md 裁定693 (k=11二素数確定 0ed1ea5 の直後の次ceremony指示: "
           "H12較正値=112, matrix{2147483647,998244353,691}, timeout 180分)",
    "l4b_doc": "docs/notes/b_type_synthesis_design_v1_addendum_l4b_grt12.md",
}


def main():
    if len(sys.argv) != 2:
        print("usage: edim_run_c12_single_prime.py <prime>", file=sys.stderr)
        sys.exit(2)
    p = int(sys.argv[1])

    t_start = time.time()
    print(f"=== E-DIM12/691 ceremony: JOB START prime={p} ===", flush=True)

    t0 = time.time()
    h_alg = ed.GradedLie(2, KMAX, p, sparse_degrees=set(range(1, KMAX + 1)))
    build_elapsed = time.time() - t0
    rss0, rss_metric = peak_rss_mb()
    print(f"p={p}: bases built, elapsed={build_elapsed:.1f}s peak_rss_mb={rss0:.1f}", flush=True)

    results = {}
    mismatch_at_k = None
    calibration_fail = False
    for k in range(3, KMAX + 1):
        tk0 = time.time()
        H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k_safe(k, None, h_alg, None, p)
        elapsed = round(time.time() - tk0, 3)
        rss_mb, _ = peak_rss_mb()

        if k <= 11:
            h_match = (H_dim == EXPECTED_H[k])
            s_match = (S_dim == EXPECTED_S[k])
        else:  # k == 12
            h_match = (H_dim == EXPECTED_H[12])
            s_match = None  # S12 is the observation, not scored pass/fail

        results[k] = {"H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h,
                     "dim_t": dim_t, "elapsed_sec": elapsed, "peak_rss_mb": rss_mb,
                     "H_predicted": EXPECTED_H.get(k), "S_predicted": EXPECTED_S.get(k),
                     "H_match": h_match, "S_match": s_match}
        # DEGREE-BOUNDARY log line only (裁定692) -- one line per k, not per
        # inner loop iteration.
        print(f"p={p} k={k}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} elapsed_sec={elapsed} "
              f"peak_rss_mb={rss_mb:.1f}", flush=True)

        if k <= 11 and not h_match:
            mismatch_at_k = k
            print(f"p={p} k={k}: MISMATCH against known k<=11 value -- STOP (job end early)", flush=True)
            break
        if k == 12 and not h_match:
            calibration_fail = True
            print(f"p={p} k=12: H12={H_dim} != calibration value 112 -- CALIBRATION_FAIL, "
                  f"S12 not to be treated as scored (job end)", flush=True)
            break

    total_elapsed = time.time() - t_start
    rss_final, _ = peak_rss_mb()

    out = {
        "schema": "edim-c12-691-kp-run/v1",
        "prereg_refs": PREREG_REFS,
        "units": UNITS,
        "solver": "Sol H-first ambient sparse rank accelerator (便112e), reused unchanged from "
                  "search/edim_run_c9_c10_v3_single_prime.py's compute_H_S_at_k_safe",
        "prime": p,
        "dim_t_12": 44555,
        "H12_calibration_value": 112,
        "build_elapsed_sec": round(build_elapsed, 2),
        "results": results,
        "mismatch_at_k_le_11": mismatch_at_k,
        "calibration_fail_h12": calibration_fail,
        "total_elapsed_sec": round(total_elapsed, 2),
        "peak_rss_mb_final": rss_final,
        "k13_not_run": True,
    }
    out_path = f"search/certs/edim_c12_691_prime_{p}_v1_20260806.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # JOB END boundary log
    print(f"=== E-DIM12/691 ceremony: JOB END prime={p} total_elapsed_sec={out['total_elapsed_sec']} "
          f"peak_rss_mb_final={rss_final:.1f} ===", flush=True)
    print(f"Wrote {out_path}", flush=True)

    if mismatch_at_k is not None or calibration_fail:
        print("EDIM_C12_691_KP_STOP", flush=True)
        sys.exit(1)
    print("EDIM_C12_691_KP_DONE", flush=True)


if __name__ == "__main__":
    main()
