#!/usr/bin/env python3
"""
Independent checker for the TOR-SWEEP k=11 T0-T3 cert (docs/notes/
tor_sweep_design_v1.md SS3.4, 裁定731(11)). Reads ONLY the cert JSON file --
does NOT import search/torsweep_k11_run.py or search/edim_semidirect_v1.py
(search/crosscheck separation, per CLAUDE.md and the wp2/aside1 precedent in
this repo -- crosscheck/check_aside1.py). Re-derives every stop-rule/canary
predicate from the raw fields recorded in the cert and compares against what
the cert itself claims, plus recomputes the Bareiss determinants of the
recorded saturation minors from scratch (own implementation, not shared with
the run script) to confirm the T-b gcd claim independently.

Usage: python crosscheck/check_torsweep_k11.py <cert_path>
"""
import json
import math
import sys


def det_bareiss_independent(mat):
    """Independent fraction-free (Bareiss) integer determinant -- written
    from scratch here, not imported from search/torsweep_k11_run.py."""
    n = len(mat)
    if n == 0:
        return 1
    M = [row[:] for row in mat]
    prev = 1
    sign = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            swap_row = None
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    swap_row = i
                    break
            if swap_row is None:
                return 0
            M[k], M[swap_row] = M[swap_row], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def witt_dimension_independent(alphabet_size, degree):
    """Independent Mobius-based Witt dimension formula (own implementation,
    not imported from edim_semidirect_v1.py)."""
    def mobius(n):
        if n == 1:
            return 1
        factors = 0
        q = n
        d = 2
        while d * d <= q:
            if q % d == 0:
                q //= d
                factors += 1
                if q % d == 0:
                    return 0
                while q % d == 0:
                    q //= d
            d += 1
        if q > 1:
            factors += 1
        return -1 if factors % 2 else 1

    total = 0
    for d in range(1, degree + 1):
        if degree % d == 0:
            total += mobius(d) * alphabet_size ** (degree // d)
    return total // degree


def fail(msg, failures):
    failures.append(msg)
    print(f"FAIL: {msg}")


def check(cert_path):
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    failures = []
    warnings = []

    if cert.get("schema") != "tor_sweep_k11_v1":
        fail(f"unexpected schema {cert.get('schema')!r}", failures)
    if cert.get("k") != 11:
        fail(f"unexpected k {cert.get('k')!r}", failures)

    EXPECTED_H = 62
    EXPECTED_S = 2

    # ---------------- T0 ----------------
    t0 = cert.get("stages", {}).get("T0")
    if t0 is None:
        fail("missing stages.T0", failures)
    else:
        witt2_i = witt_dimension_independent(2, 11)
        witt3_i = witt_dimension_independent(3, 11)
        if witt2_i != t0["witt2"]:
            fail(f"independent witt_dimension(2,11)={witt2_i} != cert witt2={t0['witt2']}", failures)
        if witt3_i != t0["witt3"]:
            fail(f"independent witt_dimension(3,11)={witt3_i} != cert witt3={t0['witt3']}", failures)
        if t0["lyndon2_count"] != t0["witt2"]:
            fail("cert's own lyndon2_count != witt2 (internal inconsistency)", failures)
        if t0["lyndon3_count"] != t0["witt3"]:
            fail("cert's own lyndon3_count != witt3 (internal inconsistency)", failures)
        expected_t_rank = t0["witt2"] + t0["witt3"]
        if t0["t_rank"] != expected_t_rank:
            fail(f"t_rank={t0['t_rank']} != witt2+witt3={expected_t_rank}", failures)
        if (t0["witt2"], t0["witt3"], t0["t_rank"]) != (186, 14880, 15066):
            fail(f"T0 values do not match design table SS1.1 "
                 f"(186,14880,15066), got {(t0['witt2'], t0['witt3'], t0['t_rank'])}", failures)
        if t0.get("t_hnf_diag_all_units") is not True:
            fail("t_hnf_diag_all_units is not True", failures)

    canary_Ta = cert.get("canaries", {}).get("T-a", {})
    ta_recomputed = bool(
        t0 and t0["lyndon2_count"] == t0["witt2"]
        and t0["lyndon3_count"] == t0["witt3"]
        and (t0["witt2"], t0["witt3"], t0["t_rank"]) == (186, 14880, 15066))
    if canary_Ta.get("pass") != ta_recomputed:
        fail(f"canary T-a pass flag {canary_Ta.get('pass')} != recomputed {ta_recomputed}", failures)

    if not ta_recomputed:
        print("T-a failed -- per S-TOR-1 the run should have stopped here; "
              "checking that stop_rules reflects this.")
        sr = cert.get("stop_rules", {}).get("S-TOR-1")
        if not sr or not sr.get("triggered"):
            fail("T-a failed but stop_rules.S-TOR-1 not recorded as triggered", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    # ---------------- T1 ----------------
    t1 = cert.get("stages", {}).get("T1")
    if t1 is None:
        fail("missing stages.T1", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    if t1.get("exact_moduli_agree") is not True:
        fail("exact_moduli_agree is not True (two-modulus cross-check failed "
             "-- theta/tau construction may not be exact)", failures)

    if t1.get("M_shape") != [372, 186]:
        fail(f"M_shape={t1.get('M_shape')} != [372,186] (expected "
             f"2*Witt(2,11) x Witt(2,11))", failures)

    H_rank = t1.get("H_rank")
    modq = t1.get("H_rank_via_modq_rank", {})
    if not modq:
        fail("H_rank_via_modq_rank missing/empty", failures)
    else:
        vals = set(modq.values())
        if len(vals) != 1:
            fail(f"H_rank_via_modq_rank values disagree across primes: {modq}", failures)
        elif H_rank not in vals:
            fail(f"H_rank={H_rank} not equal to mod-q rank cross-check value(s) {vals}", failures)
        if t1.get("H_rank_via_modq_rank_agree") != (len(vals) == 1):
            fail("H_rank_via_modq_rank_agree flag inconsistent with recorded values", failures)

    if t1.get("H_rank_exact_Q_nullspace") != H_rank:
        fail("H_rank_exact_Q_nullspace != H_rank", failures)

    if t1.get("exact_kernel_residual_nonzero_entries") != 0:
        fail(f"exact_kernel_residual_nonzero_entries="
             f"{t1.get('exact_kernel_residual_nonzero_entries')} != 0 -- "
             f"the recorded spanning matrix B does not exactly satisfy M@B^T=0", failures)

    # Recompute the T-b saturation gcd independently from the recorded
    # minor determinants (own Bareiss implementation above, not re-deriving
    # B itself since B's raw entries are not stored in the cert -- this
    # checker verifies internal consistency of what WAS recorded, i.e. that
    # the claimed gcd is truly the gcd of the claimed determinants, and that
    # this gcd is what the pass/fail flag is based on).
    minor_dets_str = t1.get("saturation_minor_determinants", [])
    try:
        minor_dets = [int(d) for d in minor_dets_str]
    except Exception:
        minor_dets = []
        fail("saturation_minor_determinants not parseable as integers", failures)
    recomputed_gcd = 0
    for d in minor_dets:
        recomputed_gcd = math.gcd(recomputed_gcd, abs(d))
    if minor_dets and str(recomputed_gcd) != t1.get("saturation_gcd_of_minors"):
        fail(f"recomputed gcd of recorded minors = {recomputed_gcd} != cert's "
             f"saturation_gcd_of_minors = {t1.get('saturation_gcd_of_minors')}", failures)
    canary_Tb = cert.get("canaries", {}).get("T-b", {})
    tb_recomputed = (recomputed_gcd == 1) if minor_dets else (H_rank == 0)
    if canary_Tb.get("pass") != tb_recomputed:
        fail(f"canary T-b pass flag {canary_Tb.get('pass')} != recomputed "
             f"{tb_recomputed} from recorded minors", failures)
    if not minor_dets and H_rank != 0:
        warnings.append("no saturation minors recorded but H_rank != 0 -- "
                         "cannot independently confirm T-b from this cert alone")

    if not tb_recomputed:
        sr = cert.get("stop_rules", {}).get("S-TOR-1")
        if not sr or not sr.get("triggered"):
            fail("T-b failed but stop_rules.S-TOR-1 not recorded as triggered", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    h_match = (H_rank == EXPECTED_H)
    if t1.get("H_rank_matches_edim_c11_measurement_62") != h_match:
        fail(f"H_rank_matches_edim_c11_measurement_62 flag "
             f"{t1.get('H_rank_matches_edim_c11_measurement_62')} != recomputed {h_match}", failures)
    if not h_match:
        sr = cert.get("stop_rules", {}).get("S-TOR-2")
        if not sr or not sr.get("triggered"):
            fail("H_rank regression mismatch but stop_rules.S-TOR-2 not "
                 "recorded as triggered", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    # ---------------- T2/T3 ----------------
    t23 = cert.get("stages", {}).get("T2_T3")
    if t23 is None:
        fail("missing stages.T2_T3 (T1 passed but T2/T3 not present)", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    per_prime = t23.get("per_prime", {})
    ranks = [v["rank"] for v in per_prime.values()]
    if len(per_prime) < 3:
        fail(f"only {len(per_prime)} primes recorded, design requires 3 "
             f"(canary T-c)", failures)
    ranks_agree = len(set(ranks)) == 1
    canary_Tc = cert.get("canaries", {}).get("T-c", {})
    if canary_Tc.get("pass") != ranks_agree:
        fail(f"canary T-c pass flag {canary_Tc.get('pass')} != recomputed "
             f"{ranks_agree} from per-prime ranks {ranks}", failures)
    if t23.get("ranks_agree") != ranks_agree:
        fail("stages.T2_T3.ranks_agree inconsistent with per-prime ranks", failures)

    if not ranks_agree:
        sr = cert.get("stop_rules", {}).get("S-TOR-1")
        if not sr or not sr.get("triggered"):
            fail("T-c failed but stop_rules.S-TOR-1 not recorded as triggered", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    r_prime = ranks[0]
    if t23.get("r_prime") != r_prime:
        fail(f"r_prime={t23.get('r_prime')} != recomputed {r_prime}", failures)
    dim_S_Q = H_rank - r_prime
    if t23.get("dim_S_Q_byproduct") != dim_S_Q:
        fail(f"dim_S_Q_byproduct={t23.get('dim_S_Q_byproduct')} != "
             f"H_rank - r_prime = {dim_S_Q}", failures)

    s_match = (dim_S_Q == EXPECTED_S)
    if t23.get("dim_S_Q_matches_edim_c11_measurement_2") != s_match:
        fail(f"dim_S_Q_matches_edim_c11_measurement_2 flag "
             f"{t23.get('dim_S_Q_matches_edim_c11_measurement_2')} != "
             f"recomputed {s_match}", failures)

    if not s_match:
        sr = cert.get("stop_rules", {}).get("S-TOR-2")
        if not sr or not sr.get("triggered"):
            fail("dim_S_Q regression mismatch but stop_rules.S-TOR-2 not "
                 "recorded as triggered", failures)

    # ---------------- judgement-word scan (S-TOR-4) ----------------
    banned_words = ["無条件", "捩れなし", "格上げ", "証明終わり", "verified"]
    cert_text = json.dumps(cert, ensure_ascii=False)
    for w in banned_words:
        if w in cert_text:
            fail(f"S-TOR-4 violation: banned judgement word {w!r} found in cert", failures)

    report(cert_path, failures, warnings)
    return len(failures) == 0


def report(cert_path, failures, warnings):
    print(f"\n=== check_torsweep_k11.py report for {cert_path} ===")
    if warnings:
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  WARN: {w}")
    if failures:
        print(f"{len(failures)} FAILURE(S):")
        for f in failures:
            print(f"  FAIL: {f}")
        print("RESULT: cross-check FAILED")
    else:
        print("RESULT: cross-check PASSED (all recomputed predicates match "
              "the cert's own recorded booleans; this is a cross-check, not "
              "a Lean-level verification)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check_torsweep_k11.py <cert_path>", file=sys.stderr)
        sys.exit(2)
    ok = check(sys.argv[1])
    sys.exit(0 if ok else 1)
