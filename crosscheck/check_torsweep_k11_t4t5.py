#!/usr/bin/env python3
"""
Independent checker for the TOR-SWEEP k=11 T4/T5 cert (docs/notes/
tor_sweep_design_v1.md SS3.2 "TOR-DET" + SS3.4 T4/T5 rows, 裁定734発注①).
Reads ONLY the cert JSON file -- does NOT import
search/torsweep_k11_t4t5_run.py or search/edim_semidirect_v1.py
(search/crosscheck separation). All small helper functions (Bareiss
determinant, mod-p rank, prime sieve) are re-implemented from scratch here,
independently of crosscheck/check_torsweep_k11.py's copies.

What CAN be independently recomputed from the cert alone:
  - every minor determinant, from the recorded N_source + minor_row_sets
    (own Bareiss implementation)
  - gcd_abs, from the recomputed determinants
  - the prime-factorization arithmetic of gcd_abs (product of recorded
    factors, including any UNRESOLVED_COMPOSITE, reconstitutes gcd_abs)
  - the CHEAP tier of each T5 candidate-prime check (rank_p(N_source) via
    an independent mod-p rank), since N_source is recorded in full

What CANNOT be independently recomputed from the cert alone (documented as
an explicit, disclosed limitation rather than silently skipped): the
EXPENSIVE tier (full rank_nu_j_on_subspace_ambient over the whole ambient
target space, for candidates where the cheap N_source check was
inconclusive) requires the full production machinery and is NOT re-derived
here; this checker only confirms those entries are INTERNALLY CONSISTENT
(cheap_N_source_rank matches an independent recomputation, and the
jumps/torsion_primes bookkeeping is arithmetically consistent with the
recorded rank_p).

Usage: python crosscheck/check_torsweep_k11_t4t5.py <cert_path>
"""
import json
import math
import sys


def det_bareiss_independent(mat):
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


def rank_mod_p_independent(rows, p):
    if not rows:
        return 0
    M = [[x % p for x in row] for row in rows]
    nrows = len(M)
    ncols = len(M[0])
    row = 0
    rank = 0
    for col in range(ncols):
        if row >= nrows:
            break
        piv = None
        for r in range(row, nrows):
            if M[r][col] % p != 0:
                piv = r
                break
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        inv = pow(M[row][col], p - 2, p)
        M[row] = [(x * inv) % p for x in M[row]]
        for r in range(nrows):
            if r != row and M[r][col] % p != 0:
                f = M[r][col]
                M[r] = [(M[r][c] - f * M[row][c]) % p for c in range(ncols)]
        rank += 1
        row += 1
    return rank


def small_primes_independent(bound):
    sieve = [True] * (bound + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(bound ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, bound + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]


def fail(msg, failures):
    failures.append(msg)
    print(f"FAIL: {msg}")


def check(cert_path):
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)
    failures = []
    warnings = []

    if cert.get("schema") != "tor_sweep_k11_v1.2":
        fail(f"unexpected schema {cert.get('schema')!r}", failures)
    if cert.get("k") != 11:
        fail(f"unexpected k {cert.get('k')!r}", failures)
    if not cert.get("supersedes"):
        fail("v1.2 cert missing 'supersedes' reference to v1.1", failures)

    t0t3 = cert.get("t0_t3_summary", {})
    if not t0t3.get("canaries_T_a_T_b_T_c_all_pass"):
        warnings.append("t0_t3_summary does not claim T-a/T-b/T-c all pass "
                         "-- T4/T5 results rest on an unverified foundation "
                         "(this checker does not re-verify T0-T3 itself; "
                         "use crosscheck/check_torsweep_k11.py on the v1.1 "
                         "cert for that)")
    H_rank = t0t3.get("H_rank")
    r_prime = t0t3.get("r_prime")

    t4 = cert.get("stages", {}).get("T4")
    if t4 is None:
        fail("missing stages.T4", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    if t4.get("exact_moduli_agree") is not True:
        fail("T4 exact_moduli_agree is not True", failures)

    N_source = t4.get("N_source")
    minor_row_sets = t4.get("minor_row_sets", [])
    minor_dets_str = t4.get("minor_determinants", [])
    minor_dets = [int(d) for d in minor_dets_str]

    if not (isinstance(N_source, list) and N_source):
        warnings.append("N_source not present in this cert -- cannot "
                         "independently recompute minor determinants, "
                         "falling back to trusting recorded values")
        recomputed_dets = minor_dets
    else:
        r_prime_shape = t4.get("N_source_shape", [None, None])[1]
        if len(minor_row_sets) != len(minor_dets):
            fail("minor_row_sets length != minor_determinants length", failures)
        recomputed_dets = []
        for rows, claimed_d in zip(minor_row_sets, minor_dets):
            submat = [N_source[i] for i in rows]
            d = det_bareiss_independent(submat)
            recomputed_dets.append(d)
            if d != claimed_d:
                fail(f"independently recomputed minor determinant for rows "
                     f"{rows[:5]}... = {d} != cert's claimed {claimed_d}", failures)
        # sanity: each minor should be square r'xr'
        for rows in minor_row_sets:
            if len(rows) != r_prime_shape:
                fail(f"minor row set has {len(rows)} rows != N_source_shape "
                     f"r'={r_prime_shape}", failures)

    if len(recomputed_dets) < 3:
        fail(f"only {len(recomputed_dets)} minors recorded, design requires "
             f"s>=3", failures)

    recomputed_gcd = 0
    for d in recomputed_dets:
        recomputed_gcd = math.gcd(recomputed_gcd, abs(d))
    if str(recomputed_gcd) != t4.get("gcd_abs"):
        fail(f"recomputed gcd_abs={recomputed_gcd} != cert's gcd_abs="
             f"{t4.get('gcd_abs')}", failures)

    canary = cert.get("canaries", {}).get("T-P-T-1", {})
    expected_flag = (recomputed_gcd == 1)
    if canary.get("gcd_abs_equals_1") != expected_flag:
        fail(f"canary T-P-T-1 gcd_abs_equals_1={canary.get('gcd_abs_equals_1')} "
             f"!= recomputed {expected_flag}", failures)

    # ---------------- T5 ----------------
    t5 = cert.get("stages", {}).get("T5")
    if t5 is None:
        fail("missing stages.T5", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    if recomputed_gcd == 1:
        if t5.get("triggered") is not False:
            fail("gcd_abs==1 (recomputed) but T5 claims triggered=True", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    if t5.get("triggered") is not True:
        fail("gcd_abs!=1 (recomputed) but T5 claims triggered=False", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    # (a) product of recorded factors reconstitutes gcd_abs
    factors = t5.get("gcd_abs_prime_factors", {})
    product = 1
    unresolved_seen = False
    for key, exp in factors.items():
        if key == "UNRESOLVED_COMPOSITE":
            product *= int(exp)
            unresolved_seen = True
            continue
        try:
            base = int(key)
        except ValueError:
            warnings.append(f"unrecognized factor key {key!r}, skipped in "
                             f"product reconstitution")
            continue
        product *= base ** int(exp)
    if product != recomputed_gcd:
        fail(f"product of recorded gcd_abs_prime_factors = {product} != "
             f"recomputed gcd_abs = {recomputed_gcd}", failures)

    resolved_flag = t5.get("factorization_fully_resolved")
    if resolved_flag != (not unresolved_seen and t5.get("unresolved_cofactor") is None):
        fail(f"factorization_fully_resolved={resolved_flag} inconsistent "
             f"with presence of an unresolved cofactor in the recorded "
             f"factors", failures)
    if not resolved_flag:
        warnings.append("factorization of gcd_abs is NOT fully resolved in "
                         "this cert -- the unresolved cofactor's status as a "
                         "torsion candidate is UNDETERMINED, not confirmed "
                         "innocent; this is a genuine open item, not a "
                         "checker limitation")

    # (b) per-prime jump_at_p bookkeeping
    jump_at_p = t5.get("jump_at_p", {})
    torsion_primes = set(t5.get("torsion_primes", []))
    for p_str, info in jump_at_p.items():
        p = int(p_str)
        rank_p = info.get("rank_p")
        jumps = info.get("jumps")
        expected_jumps = (rank_p < r_prime)
        if jumps != expected_jumps:
            fail(f"prime {p}: jumps={jumps} != (rank_p={rank_p} < "
                 f"r_prime={r_prime}) = {expected_jumps}", failures)
        if jumps and p not in torsion_primes:
            fail(f"prime {p} has jumps=True but is not in torsion_primes", failures)
        if not jumps and p in torsion_primes:
            fail(f"prime {p} has jumps=False but IS in torsion_primes", failures)

        method = info.get("method")
        if method == "cheap_N_source_rank":
            if N_source is not None:
                indep_rank = rank_mod_p_independent(N_source, p)
                if indep_rank != rank_p:
                    fail(f"prime {p} (cheap method): independently "
                         f"recomputed rank_p(N_source)={indep_rank} != "
                         f"cert's rank_p={rank_p}", failures)
        elif method == "full_rank_nu_j_on_subspace_ambient":
            cheap_r = info.get("cheap_N_source_rank")
            if N_source is not None and cheap_r is not None:
                indep_cheap = rank_mod_p_independent(N_source, p)
                if indep_cheap != cheap_r:
                    fail(f"prime {p} (escalated): independently recomputed "
                         f"cheap N_source rank {indep_cheap} != cert's "
                         f"recorded cheap_N_source_rank {cheap_r}", failures)
            warnings.append(f"prime {p}: the ESCALATED (full ambient) rank_p="
                             f"{rank_p} value cannot be independently "
                             f"recomputed by this checker without the full "
                             f"production machinery (search/crosscheck "
                             f"separation) -- only its internal consistency "
                             f"with the cheap tier and the jumps/"
                             f"torsion_primes bookkeeping was checked")
        else:
            fail(f"prime {p}: unrecognized method {method!r}", failures)

    # S-TOR-4 judgement-word scan
    banned_words = ["無条件", "捩れなし", "格上げ", "証明終わり", "verified", "捩れ支持=∅"]
    cert_text = json.dumps(cert, ensure_ascii=False)
    for w in banned_words:
        if w in cert_text:
            fail(f"S-TOR-4 violation: banned judgement word {w!r} found in cert", failures)

    report(cert_path, failures, warnings)
    return len(failures) == 0


def report(cert_path, failures, warnings):
    print(f"\n=== check_torsweep_k11_t4t5.py report for {cert_path} ===")
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
        print("RESULT: cross-check PASSED (subject to the disclosed "
              "escalated-tier limitation above, if any; this is a "
              "cross-check, not a Lean-level verification)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check_torsweep_k11_t4t5.py <cert_path>", file=sys.stderr)
        sys.exit(2)
    ok = check(sys.argv[1])
    sys.exit(0 if ok else 1)
