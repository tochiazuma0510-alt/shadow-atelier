#!/usr/bin/env python3
"""
torsweep_k11_close_v1_3.py -- closes the unresolved 67-digit residual
cofactor from cert v1.2 (裁定736: "手順1/手順2"), using ONLY the N_source
matrix already recorded in v1.2 (no re-derivation of the expensive exact
ambient construction -- N_source is 62x60, already exact, already verified
against two independent moduli in the v1.2 run).

手順1 (quick): compute ~15 MORE 60x60 minors of N_source via different
ROW subsets (the only kind of "different minor" available without
re-deriving a new set of pivot ambient COLUMNS, which would require redoing
the ~40-minute exact two-modulus construction -- this is recorded honestly
below as column_selection_varied=False, so this step is not overclaimed as
independent sampling in the column direction).

手順2 (main event, if 手順1 doesn't shrink the gcd below the confirmed-
innocent set {2,5,11393}): unit-pivot elimination MODULO M (a possibly
COMPOSITE modulus), a Howell-form-style algorithm that proves "rank == r'
simultaneously for every prime factor of M" WITHOUT factoring M, by
requiring each of the r' pivots found during row reduction (extended-gcd
column combination, exactly as in torsweep_k11_run.py's saturate_spanning_
set, but now reducing mod M throughout to keep numbers bounded, and using
a MODULAR INVERSE step instead of an exact-integer divide once a pivot is
found) to be a UNIT mod M (gcd(pivot, M) == 1). If a pivot instead reveals
gcd(pivot, M) == g with 1 < g < M, that IS a factor of M "for free" (no
trial division / ECM needed) -- recurse on M//g and g separately. This
terminates in finitely many steps since M's factorization is finite.
"""
import json
import os
import sys
import time
from math import gcd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "search"))
from torsweep_k11_run import det_bareiss, sha256_of_file, ext_gcd  # noqa: E402

K = 11
V1_2_CERT_PATH = os.path.join(REPO_ROOT, "search", "certs",
                               "torsweep_k11_v1_2_20260807.json")
EXTRA_MINORS_TARGET = 15
RNG_SEED = 20260807

import random
random.seed(RNG_SEED)


def independent_rows_modp(rows_as_matrix, p, order, target_count):
    pivots = {}
    selected = []
    for r in order:
        row = rows_as_matrix[r]
        vec = {c: row[c] % p for c in range(len(row)) if row[c] % p}
        while vec:
            piv = min(vec)
            old = pivots.get(piv)
            if old is None:
                inv = pow(vec[piv], p - 2, p)
                vec = {c: (v * inv) % p for c, v in vec.items() if v % p}
                pivots[piv] = vec
                selected.append(r)
                break
            factor = vec[piv]
            for c, v in old.items():
                nv = (vec.get(c, 0) - factor * v) % p
                if nv:
                    vec[c] = nv
                else:
                    vec.pop(c, None)
        if len(selected) == target_count:
            break
    return selected


def howell_unit_pivot_mod_M(N_source, M, col_order=None, row_priority=None):
    """Returns a dict: {'status': 'success', 'pivots': [(col,row),...]}
    or {'status': 'split', 'factor': g} or {'status': 'insufficient'}.

    col_order: processing order of the c columns (default 0..c-1).
    row_priority: tie-break order among candidate rows at each column
    (default row index order). Both are exposed so a caller can verify an
    'insufficient' outcome is not a pivot-order artifact (this matters: a
    genuinely order-INDEPENDENT 'insufficient' result is strong evidence
    of an actual rank drop mod M, not a processing artifact -- see
    close_modulus_robust below)."""
    r = len(N_source)
    c = len(N_source[0]) if r else 0
    if col_order is None:
        col_order = list(range(c))
    if row_priority is None:
        row_priority = list(range(r))
    row_rank = {row: i for i, row in enumerate(row_priority)}
    A = [[x % M for x in row] for row in N_source]
    active = list(range(r))
    pivots_found = []

    for col in col_order:
        while True:
            nz = sorted((i for i in active if A[i][col] % M != 0),
                        key=lambda i: row_rank[i])
            if len(nz) <= 1:
                break
            i0, i1 = nz[0], nz[1]
            a, b = A[i0][col], A[i1][col]
            g, x, y = ext_gcd(a, b)
            ag, bg = a // g, b // g
            row_i0, row_i1 = A[i0], A[i1]
            A[i0] = [(x * row_i0[k] + y * row_i1[k]) % M for k in range(c)]
            A[i1] = [(ag * row_i1[k] - bg * row_i0[k]) % M for k in range(c)]
        nz = sorted((i for i in active if A[i][col] % M != 0),
                    key=lambda i: row_rank[i])
        if not nz:
            continue
        piv_row = nz[0]
        pivot_val = A[piv_row][col]
        g = gcd(pivot_val, M)
        if g != 1:
            return {"status": "split", "factor": g, "pivot_col": col,
                    "pivots_before_split": len(pivots_found)}
        inv = pow(pivot_val, -1, M)
        A[piv_row] = [(v * inv) % M for v in A[piv_row]]
        for i in active:
            if i != piv_row and A[i][col] % M != 0:
                f = A[i][col]
                Apiv = A[piv_row]
                A[i] = [(A[i][k] - f * Apiv[k]) % M for k in range(c)]
        pivots_found.append((col, piv_row))
        active.remove(piv_row)
        if len(pivots_found) == c:
            break
    if len(pivots_found) == c:
        return {"status": "success", "pivots": pivots_found}
    return {"status": "insufficient", "pivots_found": len(pivots_found)}


ROBUSTNESS_TRIALS = 8  # number of independent (row,col) orderings tried
                        # before an 'insufficient' result is accepted as
                        # genuine (order-independent) rather than a pivot-
                        # selection artifact.


def robust_howell(N_source, M, log, indent):
    """Tries ROBUSTNESS_TRIALS independent (row,col) processing orders. If
    ANY succeeds or splits, that outcome is used immediately (a single
    success/split is conclusive regardless of what other orders would have
    found). Only if ALL trials return 'insufficient' is the result reported
    as order-independent evidence of a genuine rank drop mod M."""
    r = len(N_source)
    c = len(N_source[0])
    outcomes = []
    for trial in range(ROBUSTNESS_TRIALS):
        col_order = list(range(c))
        row_priority = list(range(r))
        random.shuffle(col_order)
        random.shuffle(row_priority)
        result = howell_unit_pivot_mod_M(N_source, M, col_order, row_priority)
        outcomes.append(result["status"])
        if result["status"] != "insufficient":
            log(f"{indent}robust_howell: trial {trial} gave "
                f"{result['status']} (out of {ROBUSTNESS_TRIALS} planned "
                f"trials) -- using this outcome immediately")
            result["trials_tried"] = trial + 1
            result["all_trial_outcomes"] = outcomes
            return result
    log(f"{indent}robust_howell: ALL {ROBUSTNESS_TRIALS} independent "
        f"(row,col) orderings gave 'insufficient' -- this is ORDER-"
        f"INDEPENDENT evidence of a genuine rank drop mod M, not a pivot-"
        f"selection artifact")
    return {"status": "insufficient_robust", "trials_tried": ROBUSTNESS_TRIALS,
            "all_trial_outcomes": outcomes,
            "pivots_found": [o for o in outcomes]}


def close_modulus(N_source, M, log, depth=0):
    """Recursively apply howell_unit_pivot_mod_M, splitting on any factor
    found, until every irreducible-under-this-method piece is resolved.
    Returns a list of dicts describing the resolution of M's factors."""
    indent = "  " * depth
    log(f"{indent}close_modulus: M has {len(str(M))} digits")
    if M == 1:
        return [{"modulus": "1", "status": "trivial"}]
    result = robust_howell(N_source, M, log, indent)
    if result["status"] == "success":
        log(f"{indent}close_modulus: SUCCESS -- all {len(result['pivots'])} "
            f"pivots are units mod M -- every prime factor of this M is "
            f"confirmed innocent (rank==r' simultaneously), no factoring needed")
        return [{"modulus": str(M), "status": "success",
                 "pivot_count": len(result["pivots"])}]
    if result["status"] == "split":
        g = result["factor"]
        other = M // g
        log(f"{indent}close_modulus: SPLIT at pivot_col={result['pivot_col']} "
            f"-- free factor g={g} ({len(str(g))} digits), "
            f"M//g has {len(str(other))} digits -- recursing on both")
        return (close_modulus(N_source, g, log, depth + 1)
                + close_modulus(N_source, other, log, depth + 1))
    log(f"{indent}close_modulus: INSUFFICIENT (order-independent across "
        f"{result['trials_tried']} trials) -- N_source has a GENUINE rank "
        f"drop mod this M, i.e. mod at least one of its (unfactored) prime "
        f"divisors. This is NOT a processing artifact. It is raw evidence "
        f"only -- no judgement word is written; whether this constitutes a "
        f"real torsion prime for the p>=5, k=11 claim requires identifying "
        f"the actual prime factor (which this method alone could not "
        f"provide here) and is 司令塔's call, per QUAR-TOR SS5.3.")
    return [{"modulus": str(M), "status": "insufficient_order_independent",
             "trials_tried": result["trials_tried"],
             "all_trial_outcomes": result["all_trial_outcomes"]}]


def main():
    log_lines = []
    t_start = time.time()

    def record(msg):
        line = f"[{time.time()-t_start:8.2f}s] {msg}"
        print(line, flush=True)
        log_lines.append(line)

    record("loading v1.2 cert")
    with open(V1_2_CERT_PATH, "r", encoding="utf-8") as f:
        v1_2 = json.load(f)
    t4 = v1_2["stages"]["T4"]
    t5 = v1_2["stages"]["T5"]
    N_source = t4["N_source"]
    r_prime = t4["N_source_shape"][1]
    H_rank = len(N_source)
    existing_minor_row_sets = t4["minor_row_sets"]
    existing_minor_dets = [int(d) for d in t4["minor_determinants"]]
    gcd_abs_v1_2 = int(t4["gcd_abs"])
    unresolved_cofactor = t5.get("unresolved_cofactor")
    unresolved_desc = "None" if unresolved_cofactor is None else f"{len(unresolved_cofactor)} digits"
    record(f"loaded: N_source {H_rank}x{r_prime}, {len(existing_minor_row_sets)} "
           f"existing minors, gcd_abs(v1.2)={len(str(gcd_abs_v1_2))} digits, "
           f"unresolved_cofactor={unresolved_desc}")

    cert = {
        "schema": "tor_sweep_k11_v1.3",
        "supersedes": "search/certs/torsweep_k11_v1_2_20260807.json",
        "supersedes_note": "closes the unresolved 67-digit residual cofactor "
                            "left open in v1.2, per 裁定736, using ONLY the "
                            "N_source matrix already recorded in v1.2 (no "
                            "re-derivation of the exact ambient construction).",
        "design_spec": "docs/notes/tor_sweep_design_v1.md",
        "k": K,
        "generated_by": {
            "tool": "search/torsweep_k11_close_v1_3.py",
            "torsweep_k11_run_sha256": sha256_of_file(
                os.path.join(REPO_ROOT, "search", "torsweep_k11_run.py")),
            "rng_seed": RNG_SEED,
        },
        "stages": {},
    }

    # =========================================================================
    # 手順1: EXTRA_MINORS_TARGET more 60x60 minors via different row subsets
    # of the SAME N_source (honestly recorded: column selection NOT varied).
    # =========================================================================
    record("手順1: computing extra row-subset minors of the existing N_source")
    big_prime = 2147483647
    orders = []
    for _ in range(EXTRA_MINORS_TARGET + 10):
        o = list(range(H_rank))
        random.shuffle(o)
        orders.append(o)
    seen = {tuple(sorted(rs)) for rs in existing_minor_row_sets}
    new_minor_dets = []
    new_minor_row_sets = []
    for order in orders:
        rows_sel = independent_rows_modp(N_source, big_prime, order, r_prime)
        if len(rows_sel) != r_prime:
            continue
        key = tuple(sorted(rows_sel))
        if key in seen:
            continue
        seen.add(key)
        submat = [N_source[i] for i in rows_sel]
        d = det_bareiss(submat)
        if d == 0:
            continue
        new_minor_dets.append(d)
        new_minor_row_sets.append(rows_sel)
        if len(new_minor_dets) >= EXTRA_MINORS_TARGET:
            break
    all_dets = existing_minor_dets + new_minor_dets
    all_row_sets = existing_minor_row_sets + new_minor_row_sets
    gcd_after_step1 = 0
    for d in all_dets:
        gcd_after_step1 = gcd(gcd_after_step1, abs(d))
    record(f"手順1: {len(new_minor_dets)} new minors added (total {len(all_dets)}), "
           f"gcd_after_step1 digits={len(str(gcd_after_step1))}")

    cert["stages"]["step1_extra_minors"] = {
        "column_selection_varied": False,
        "column_selection_note": "all minors (existing + new) share the "
                                  "same 60 ambient columns from v1.2's "
                                  "N_source; only the 60-of-62 row subset "
                                  "varies. A shrinking gcd here would still "
                                  "be informative (fewer accidental shared "
                                  "row-combination factors), but a "
                                  "NON-shrinking gcd is uninformative about "
                                  "column-selection correlation specifically "
                                  "(honest disclosure per 裁定736's request).",
        "new_minor_count": len(new_minor_dets),
        "new_minor_determinant_digit_counts": [len(str(d)) for d in new_minor_dets],
        "total_minor_count": len(all_dets),
        "gcd_abs_before_step1": str(gcd_abs_v1_2),
        "gcd_abs_after_step1": str(gcd_after_step1),
    }

    if gcd_after_step1 == 1:
        record("手順1 alone resolved gcd_abs to 1 -- 手順2 not needed")
        cert["stages"]["step2_howell_mod_M"] = {"triggered": False,
                                                 "reason": "gcd_abs==1 after step1"}
        write_cert(cert, log_lines)
        return

    # =========================================================================
    # 手順2: Howell-style unit-pivot elimination modulo the residual, applied
    # to whatever gcd remains after 手順1 (recursing on any free factors).
    # =========================================================================
    record(f"手順2: Howell unit-pivot elimination modulo the residual "
           f"({len(str(gcd_after_step1))} digits)")
    closures = close_modulus(N_source, gcd_after_step1, record)
    all_success = all(c["status"] == "success" for c in closures)
    cert["stages"]["step2_howell_mod_M"] = {
        "triggered": True,
        "input_modulus_digits": len(str(gcd_after_step1)),
        "closures": closures,
        "all_pieces_resolved_success": all_success,
    }
    record(f"手順2: all_pieces_resolved_success={all_success}")
    record(f"closures={closures}")

    cert["total_elapsed_seconds"] = time.time() - t_start
    write_cert(cert, log_lines)


def write_cert(cert, log_lines):
    cert["run_log"] = log_lines
    out_dir = os.path.join(REPO_ROOT, "search", "certs")
    date_str = time.strftime("%Y%m%d")
    out_path = os.path.join(out_dir, f"torsweep_k11_v1_3_{date_str}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2, ensure_ascii=False, default=str)
    print(f"cert written: {out_path}", flush=True)


if __name__ == "__main__":
    main()
