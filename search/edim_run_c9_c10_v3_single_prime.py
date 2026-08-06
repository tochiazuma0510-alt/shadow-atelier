#!/usr/bin/env python3
"""
edim_run_c9_c10_v3_single_prime.py -- per-PRIME exact run for k=3,...,10,
runnable standalone with one CLI arg (the prime). Split out of
edim_run_c9_c10_v2.py so GHA can run the two commissioned primes as
PARALLEL matrix jobs.  The speedup path constructs only nu_k o j restricted
to H_k: rho^i(X),rho^i(Y) are substituted directly into h Lyndon trees and
evaluated in the ambient semidirect tensor algebra.  It constructs neither
the full dim(t_k)^2 rho matrix nor the all-degree delta table.

Usage: python search/edim_run_c9_c10_v3_single_prime.py <prime>
       EDIM_OUTPUT_DIR=<temporary-directory> may redirect the certificate.

Writes edim_c9_c10_prime_<prime>_v3_20260806.json with a fail-closed k=3..10
per-prime regression verdict.  The commissioned battery is complete only
after the two outputs for 65521 and 2147483647 both say regression_ok and
their H/S rows agree.  The older v3 aggregate script uses a different prime
pair and is intentionally not part of this run.
"""
import json
import os
import sys
import time
import tracemalloc

import numpy as np

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed

KMAX = 10
EXPECTED_H = {3: 1, 4: 1, 5: 2, 6: 3, 7: 6, 8: 10, 9: 19, 10: 33}
EXPECTED_S = {3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 1, 9: 1, 10: 1}
REQUIRED_REGRESSION_PRIMES = {65521, 2147483647}


def peak_rss_mb():
    """Process peak resident memory in MiB, using only the stdlib/OS API."""
    if sys.platform == "win32":
        import ctypes

        class ProcessMemoryCounters(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.c_ulong),
                ("PageFaultCount", ctypes.c_ulong),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        counters = ProcessMemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        get_current_process = ctypes.windll.kernel32.GetCurrentProcess
        get_current_process.restype = ctypes.c_void_p
        get_process_memory_info = ctypes.windll.psapi.GetProcessMemoryInfo
        get_process_memory_info.argtypes = [
            ctypes.c_void_p, ctypes.POINTER(ProcessMemoryCounters), ctypes.c_ulong]
        get_process_memory_info.restype = ctypes.c_int
        process = get_current_process()
        ok = get_process_memory_info(
            process, ctypes.byref(counters), counters.cb)
        if not ok:
            raise OSError("GetProcessMemoryInfo failed")
        return counters.PeakWorkingSetSize / (1024 * 1024), "windows.PEAK_WORKING_SET"

    import resource
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Linux reports KiB; macOS/BSD reports bytes.
    divisor = 1024 * 1024 if sys.platform == "darwin" else 1024
    return peak / divisor, "resource.ru_maxrss"


def compute_H_S_at_k_safe(k, n_alg, h_alg, D, p):
    """Exact H/S dimensions via the H-first ambient sparse-rank path.

    ``n_alg`` and ``D`` are retained as optional compatibility parameters;
    the optimized path deliberately does not use either one.
    """
    dim_n = ed.witt_dimension(3, k)
    dim_h = h_alg.dim[k]
    dim_t = dim_n + dim_h

    theta = np.array(ed.build_theta_tau_matrix(k, h_alg, 'theta', p), dtype=np.int64) % p
    tau = np.array(ed.build_theta_tau_matrix(k, h_alg, 'tau', p), dtype=np.int64) % p
    I_h = np.eye(dim_h, dtype=np.int64)
    one_plus_theta = (I_h + theta) % p
    tau2 = ed.mat_mul_modp_np_safe(tau, tau, p)
    one_plus_tau_tau2 = (I_h + tau + tau2) % p

    H_stack = np.concatenate([one_plus_theta, one_plus_tau_tau2], axis=0)
    H_dim = dim_h - ed.rank_modp_np(H_stack, p)
    if p % 2 and p % 3:
        # Q=(1-theta)(1-tau) has image exactly H when 6 is invertible.
        # Indeed im Q is killed by 1+theta and by N=1+tau+tau^2. Conversely,
        # for v in H, theta*v=-v and theta*tau=tau^2*theta give
        # (1-theta)tau*v=tau*v+tau^2*v=-v, hence Qv=3v.
        Q = ed.mat_mul_modp_np_safe((I_h - theta) % p, (I_h - tau) % p, p)
        H_basis = ed.sparse_column_space_basis_modp_np(Q, p)
        if H_basis.shape[1] != H_dim:
            raise ValueError(f"Q image dimension {H_basis.shape[1]} != H dimension {H_dim}")
        if ed.rank_modp_np(H_basis, p) != H_dim:
            raise ValueError("selected Q columns are not an independent H basis")
        if H_dim and np.any(ed.mat_mul_modp_np_safe(H_stack, H_basis, p)):
            raise ValueError("Q image is not annihilated by the H constraints")
    else:
        # Conservative fallback outside the commissioned prime range.
        H_basis = ed.nullspace_modp_np(H_stack, p)
        if H_basis.shape[1] != H_dim:
            raise ValueError("nullspace dimension/rank mismatch")
    nu_rank_on_H = ed.rank_nu_j_on_subspace_ambient(k, h_alg, H_basis, p)
    S_dim = H_dim - nu_rank_on_H

    return H_dim, S_dim, dim_n, dim_h, dim_t


def main():
    if len(sys.argv) != 2:
        print("usage: edim_run_c9_c10_v3_single_prime.py <prime>", file=sys.stderr)
        sys.exit(2)
    p = int(sys.argv[1])

    trace_python_allocations = os.environ.get("EDIM_TRACEMALLOC") == "1"
    if trace_python_allocations:
        tracemalloc.start()
    t_start = time.time()

    t0 = time.time()
    n_alg = None  # optimized ambient path needs only Witt dimensions
    h_alg = ed.GradedLie(2, KMAX, p, sparse_degrees=set(range(1, KMAX + 1)))
    print(f"p={p}: bases built in {time.time()-t0:.1f}s", flush=True)
    build_elapsed = time.time() - t0
    D = None  # compatibility slot; no delta table is constructed
    print(f"p={p}: direct ambient action ready in {build_elapsed:.1f}s", flush=True)

    results = {}
    mismatch_at_k = None
    warm_repeat_max_k = int(os.environ.get("EDIM_WARM_REPEAT_MAX_K", "8"))
    for k in range(3, KMAX + 1):
        tk0 = time.time()
        H_dim, S_dim, dim_n, dim_h, dim_t = compute_H_S_at_k_safe(k, n_alg, h_alg, D, p)
        fillin_h = h_alg._sparse_solver_cache.get(k, {}).get("fillin_ratio")
        cold_elapsed = round(time.time() - tk0, 3)
        # A second call exercises the memoized subtree path and guards cache
        # determinism.  Keep this timing distinct from the first/cold value;
        # only cold_elapsed_sec is used for production scaling estimates.
        warm_elapsed = None
        if k <= warm_repeat_max_k:
            tw0 = time.time()
            warm_result = compute_H_S_at_k_safe(k, n_alg, h_alg, D, p)
            warm_elapsed = round(time.time() - tw0, 3)
            if warm_result != (H_dim, S_dim, dim_n, dim_h, dim_t):
                raise RuntimeError(f"p={p} k={k}: cold/warm cache result mismatch")
        h_match = (H_dim == EXPECTED_H[k])
        s_match = (S_dim == EXPECTED_S[k])
        results[k] = {"H_dim": H_dim, "S_dim": S_dim, "dim_n": dim_n, "dim_h": dim_h,
                     "dim_t": dim_t, "elapsed_sec": cold_elapsed,
                     "cold_elapsed_sec": cold_elapsed,
                     "warm_repeat_elapsed_sec": warm_elapsed,
                     "fillin_ratio_n": None, "fillin_ratio_h": fillin_h,
                     "H_predicted": EXPECTED_H[k], "S_predicted": EXPECTED_S[k],
                     "H_match": h_match, "S_match": s_match}
        print(f"p={p} k={k}: H_dim={H_dim} S_dim={S_dim} dim_t={dim_t} "
              f"cold={cold_elapsed}s warm={warm_elapsed}s fillin_h={fillin_h}", flush=True)
        if not (h_match and s_match):
            mismatch_at_k = k
            print(f"*** p={p} k={k} REGRESSION_MISMATCH -- STOP ***", flush=True)
            break

    rss_peak_mb, rss_metric = peak_rss_mb()
    traced_peak_mb = None
    if trace_python_allocations:
        current, traced_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        traced_peak_mb = traced_peak / (1024 * 1024)
    total_elapsed = time.time() - t_start
    regression_complete = set(results) == set(EXPECTED_H)
    regression_ok = regression_complete and mismatch_at_k is None and all(
        row["H_match"] and row["S_match"] for row in results.values())

    out = {
        "schema": "edim-c9-c10-prime-run/v3",
        "solver": "H-first direct ambient sparse rank (exact mod-p; no full rho/delta table)",
        "prime": p,
        "required_regression_primes": sorted(REQUIRED_REGRESSION_PRIMES),
        "is_required_regression_prime": p in REQUIRED_REGRESSION_PRIMES,
        "kmax": KMAX,
        "bases_and_delta_table_elapsed_sec": round(build_elapsed, 2),
        "delta_table_constructed": False,
        "production_algorithm": "rho^i degree-1 substitution + ambient Leibniz action + sparse rank on H",
        "results": results,
        "full_k3_k10_regression_complete": regression_complete,
        "regression_ok": regression_ok,
        "regression_mismatch_at_k": mismatch_at_k,
        "timing_note": "cold_elapsed_sec is the first incremental degree call (lower-degree subtree "
                       "cache retained); warm_repeat_elapsed_sec is an immediate deterministic cache repeat "
                       f"only through k={warm_repeat_max_k} (override EDIM_WARM_REPEAT_MAX_K)",
        "aggregation_note": "The commissioned two-prime battery is 65521 and 2147483647; require "
                            "regression_ok in both per-prime outputs and compare all H/S rows. The existing "
                            "v3 aggregate script targets the older 998244353 pairing and is not used here.",
        "total_elapsed_sec": round(total_elapsed, 2),
        # Compatibility alias retained for the existing v3 aggregate reader;
        # by default it now contains OS peak RSS, not tracemalloc's heavily
        # distorting Python-allocation trace.  memory_metric is authoritative.
        "peak_memory_traced_mb": round(rss_peak_mb if traced_peak_mb is None else traced_peak_mb, 2),
        "peak_memory_mb": round(rss_peak_mb, 2),
        "memory_metric": rss_metric,
        "tracemalloc_opt_in": trace_python_allocations,
        "tracemalloc_peak_mb": round(traced_peak_mb, 2) if traced_peak_mb is not None else None,
        "note": "Per-prime fail-closed k=3..10 regression verdict. Complete the commissioned "
                "battery by AND/comparison of the 65521 and 2147483647 outputs; the older "
                "v3 aggregate script is not used for this prime pair.",
    }
    output_dir = os.environ.get("EDIM_OUTPUT_DIR", "search/certs")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"edim_c9_c10_prime_{p}_v3_20260806.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print("total_elapsed_sec:", out["total_elapsed_sec"],
          "peak_memory_mb:", out["peak_memory_mb"], "metric:", out["memory_metric"])
    if not regression_ok:
        print("EDIM_C9_C10_SINGLE_PRIME_REGRESSION_FAILED", file=sys.stderr)
        sys.exit(1)
    print("EDIM_C9_C10_SINGLE_PRIME_DONE")


if __name__ == "__main__":
    main()
