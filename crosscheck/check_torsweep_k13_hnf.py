#!/usr/bin/env python3
"""
Independent checker for the TOR-SWEEP k=13 T0+T1(HNF construction) cert
(schema tor_sweep_k13_hnf_construct.1, search/torsweep_k13_hnf_construct_
v1.py). Reads ONLY the cert JSON file -- does NOT import search/torsweep_
k13_hnf_construct_v1.py, search/torsweep_k12_run.py, search/torsweep_k12_
v3_hnf_kernel.py, or search/edim_semidirect_v1.py (search/crosscheck
separation, per CLAUDE.md and crosscheck/check_torsweep_k11.py's
precedent).

SCOPE (裁定842(1), "modular レーン限定" -- explicit, not a silent
narrowing): the cert's H_basis (B) entries run to ~9720 decimal digits
(210x630 matrix); a bit-for-bit independent reconstruction of the exact
integer kernel/HNF is NOT attempted here (that would itself be exactly the
"HNF成分爆発" addendum_c warns against, docs/notes/tor_sweep_design_v1_
addendum_c.md, and defeats the purpose of a lightweight cross-check).
Instead this checker verifies, independently and exactly at the modular
level:
  (a) T0: witt2/witt3/t_rank via an independent Mobius-formula
      implementation (own code, matches crosscheck/check_torsweep_k11.py's
      witt_dimension_independent verbatim in method, not import).
  (b) M @ B^T == 0 EXACTLY (integer arithmetic on the recorded M, B --
      cheap: M's entries are small, ~5-6 digits; only B's entries are
      huge, and this is a single dot-product-sum-to-zero check per (row,
      row) pair, not a determinant/elimination -- no blowup).
  (c) rank(B) == H_rank (=210) at THREE FRESH primes NOT in the cert's own
      303-prime battery sieve (small_primes(2000)) and not equal to the
      cert's claimed sat_gcd prime factors -- an independent mod-q
      Gaussian elimination (own implementation).
  (d) sat_gcd claim: independently trial-factor the cert's own reported
      sat_gcd value, confirm the factorization; then for EACH distinct
      prime factor p, confirm full rank(B) mod p (a DIRECT, independent
      re-derivation of "p does not divide any elementary divisor", the
      same theorem TOR-1 argument the run's own Howell closure used, but
      via a completely different code path -- prime-field Gaussian
      elimination, not composite-modulus Howell recursion).
  (e) mod-q^N SPOT SAMPLE (裁定842(1) explicit requirement, "mod-q^N 抜き
      取り"): for each prime factor p of sat_gcd, ALSO verify rank(B) ==
      H_rank at modulus p^N for a modest sample N (independent Z/p^N
      Gaussian elimination -- valid and cheap here specifically BECAUSE
      full rank was already established mod p: a pivot sequence achieving
      full rank mod p consists of UNIT entries mod p, hence units mod
      p^N too (units lift trivially: gcd(x,p)=1 => gcd(x,p^N)=1), so the
      SAME elimination order succeeds mod p^N with ordinary modular
      inverses -- no Howell/zero-divisor-splitting machinery needed for
      this restricted claim). This is a genuine independent computation
      at the p^N level, not a restatement of (d)'s theorem.

NOT independently reconstructed here (documented, not silently skipped):
  - T1a's exact theta/tau construction (would require reimplementing the
    ambient GradedLie/Lyndon-tree machinery -- out of crosscheck's scope
    by the search/crosscheck separation rule itself: that machinery IS
    search/edim_semidirect_v1.py).
  - The full recursive Howell closure structure recorded in the cert
    (closures_summary) -- superseded in spirit by (d)/(e) above, which
    prove the SAME end claim ("every prime factor of sat_gcd is
    innocent") via an independent, simpler route per 裁定842(1)'s
    explicit scope-limitation instruction.

Usage: python crosscheck/check_torsweep_k13_hnf.py <cert_path>
"""
import json
import math
import sys

sys.set_int_max_str_digits(0)  # B's entries run to ~9720 digits


def fail(msg, failures):
    failures.append(msg)
    print(f"FAIL: {msg}")


def warn(msg, warnings):
    warnings.append(msg)
    print(f"WARN: {msg}")


def witt_dimension_independent(alphabet_size, degree):
    """Independent Mobius-based Witt dimension formula (own implementation,
    matches crosscheck/check_torsweep_k11.py's method, not shared code)."""
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


def small_primes_independent(bound):
    sieve = [True] * (bound + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(bound ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, bound + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]


def rank_mod_m_independent(rows, m, require_unit_pivots=False):
    """Independent mod-m rank of a list of integer row-vectors, via a
    fresh row-echelon implementation. If require_unit_pivots is True
    (used for the p^N spot check), every pivot entry chosen must satisfy
    gcd(entry, m) == 1 (an actual unit mod m); if no such pivot exists in
    a column where one is needed, this raises -- the caller is expected
    to have already established (via a prime-field rank at m's unique
    prime factor) that this cannot happen for the specific matrices used
    here."""
    if not rows:
        return 0
    M = [[x % m for x in row] for row in rows]
    nrows = len(M)
    ncols = len(M[0])
    row = 0
    rank = 0
    for col in range(ncols):
        if row >= nrows:
            break
        piv = None
        for r in range(row, nrows):
            v = M[r][col]
            if v % m == 0:
                continue
            if require_unit_pivots and math.gcd(v, m) != 1:
                continue
            piv = r
            break
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        inv = pow(M[row][col], -1, m)
        M[row] = [(x * inv) % m for x in M[row]]
        for r in range(nrows):
            if r != row and M[r][col] % m != 0:
                f = M[r][col]
                M[r] = [(M[r][c] - f * M[row][c]) % m for c in range(ncols)]
        rank += 1
        row += 1
    return rank


def trial_factor_independent(n, bound=10_000_000):
    """Own trial-division factorization (small n expected -- sat_gcd here
    is a handful of digits, per addendum_c's own prediction)."""
    n = abs(n)
    factors = {}
    for p in small_primes_independent(min(bound, int(n ** 0.5) + 2)):
        if p * p > n:
            break
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def check(cert_path):
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    failures = []
    warnings = []

    if cert.get("schema") != "tor_sweep_k13_hnf_construct.1":
        fail(f"unexpected schema {cert.get('schema')!r}", failures)
    if cert.get("k") != 13:
        fail(f"unexpected k {cert.get('k')!r}", failures)

    EXPECTED_WITT2, EXPECTED_WITT3, EXPECTED_T_RANK = 630, 122640, 123270
    EXPECTED_H = 210

    # ---------------- T0 ----------------
    t0 = cert.get("stages", {}).get("T0")
    if t0 is None:
        fail("missing stages.T0", failures)
    else:
        witt2_i = witt_dimension_independent(2, 13)
        witt3_i = witt_dimension_independent(3, 13)
        if witt2_i != t0["witt2"]:
            fail(f"independent witt_dimension(2,13)={witt2_i} != cert witt2={t0['witt2']}", failures)
        if witt3_i != t0["witt3"]:
            fail(f"independent witt_dimension(3,13)={witt3_i} != cert witt3={t0['witt3']}", failures)
        if t0["lyndon2_count"] != t0["witt2"] or t0["lyndon3_count"] != t0["witt3"]:
            fail("cert's own lyndon counts != witt dims (internal inconsistency)", failures)
        if (t0["witt2"], t0["witt3"], t0["t_rank"]) != (EXPECTED_WITT2, EXPECTED_WITT3, EXPECTED_T_RANK):
            fail(f"T0 values != expected table row "
                 f"({EXPECTED_WITT2},{EXPECTED_WITT3},{EXPECTED_T_RANK}), got "
                 f"{(t0['witt2'], t0['witt3'], t0['t_rank'])}", failures)

    canary_Ta = cert.get("canaries", {}).get("T-a", {})
    if canary_Ta.get("pass") is not True:
        fail("canary T-a not pass=True", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0

    # ---------------- T1a (M) ----------------
    t1a = cert.get("stages", {}).get("T1a")
    if t1a is None:
        fail("missing stages.T1a", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0
    if t1a.get("exact_moduli_agree") is not True:
        fail("T1a exact_moduli_agree is not True", failures)
    M = t1a.get("M")
    m_shape = t1a.get("M_shape")
    if m_shape != [1260, 630]:
        fail(f"M_shape={m_shape} != [1260,630] (expected 2*Witt(2,13) x Witt(2,13))", failures)
    warn("T1a's exact theta/tau construction is NOT independently "
         "reconstructed here (out of crosscheck scope -- would require "
         "reimplementing search/edim_semidirect_v1.py's ambient Lyndon-"
         "tree machinery); M is taken as recorded and checked only "
         "structurally + via M@B^T below.", warnings)

    # ---------------- T1b (H_basis) ----------------
    H_rank = cert.get("H_rank")
    B = cert.get("H_basis")
    dim_h = cert.get("dim_h")
    if H_rank != EXPECTED_H:
        fail(f"H_rank={H_rank} != EXPECTED_H={EXPECTED_H}", failures)
    if not (isinstance(B, list) and B and isinstance(M, list) and M):
        fail("H_basis and/or M missing/empty in cert", failures)
        report(cert_path, failures, warnings)
        return len(failures) == 0
    if len(B) != H_rank or len(B[0]) != dim_h:
        fail(f"H_basis shape ({len(B)},{len(B[0]) if B else 0}) != "
             f"(H_rank={H_rank}, dim_h={dim_h})", failures)

    # (b) M @ B^T == 0 exactly -- cheap (M entries small, single dot
    # products, no elimination/determinant blowup)
    bad = 0
    for brow in B:
        for mrow in M:
            if sum(mv * bv for mv, bv in zip(mrow, brow)) != 0:
                bad += 1
    if bad != 0:
        fail(f"independently recomputed M@B^T has {bad} nonzero entries "
             f"(expected 0)", failures)
    cert_mbt = cert.get("stages", {}).get("MBt_check", {}).get("residual_nonzero_entries")
    if cert_mbt != bad:
        fail(f"cert's own MBt_check.residual_nonzero_entries={cert_mbt} != "
             f"independently recomputed {bad}", failures)

    # (c) rank(B) == H_rank at 3 fresh primes, outside the cert's own
    # battery (small_primes(2000)) and outside sat_gcd's own prime factors
    battery_bound = 2000
    sat_gcd_str = cert.get("stages", {}).get("sat_gcd_check", {}).get("sat_gcd")
    try:
        sat_gcd = int(sat_gcd_str)
    except (TypeError, ValueError):
        sat_gcd = None
        fail(f"could not parse sat_gcd={sat_gcd_str!r} as int", failures)

    FRESH_PRIMES = [999999999999999989, 2305843009213693951, 618970019642690137449562111]
    # (Mersenne-adjacent / well-known large primes, chosen independently of
    # anything the run script used -- none <= 2000, none dividing a small
    # sat_gcd like 1944.)
    for p in FRESH_PRIMES:
        if p <= battery_bound:
            fail(f"FRESH_PRIMES entry {p} is <= battery_bound {battery_bound} "
                 f"(not actually fresh)", failures)
            continue
        r = rank_mod_m_independent(B, p)
        if r != H_rank:
            fail(f"independent rank(B) mod fresh prime {p} = {r} != "
                 f"H_rank={H_rank}", failures)
        else:
            print(f"OK: rank(B) mod fresh prime {p} = {r} == H_rank")

    # (d) sat_gcd independent factorization + full-rank-mod-each-factor
    if sat_gcd is not None:
        my_factors = trial_factor_independent(sat_gcd)
        refactored = 1
        for base, exp in my_factors.items():
            refactored *= base ** exp
        if refactored != sat_gcd:
            fail(f"independent trial factorization of sat_gcd={sat_gcd} "
                 f"gave {my_factors} (product {refactored}) -- MISMATCH "
                 f"(possible unfactored residual > trial bound)", failures)
        else:
            print(f"OK: independent factorization of sat_gcd={sat_gcd}: {my_factors}")

        for p in my_factors:
            r = rank_mod_m_independent(B, p)
            if r != H_rank:
                fail(f"independent rank(B) mod sat_gcd prime factor {p} = "
                     f"{r} != H_rank={H_rank} (p would NOT be innocent -- "
                     f"contradicts the cert's Howell-closure claim)", failures)
            else:
                print(f"OK: rank(B) mod {p} (sat_gcd factor) = {r} == H_rank "
                      f"(prime independently confirmed innocent)")

            # (e) mod-q^N spot sample, N chosen so p^N stays a small int
            # (a handful of digits) -- independent Z/p^N elimination,
            # valid here because full rank mod p (just verified above)
            # guarantees an all-unit pivot sequence exists.
            N = 1
            while p ** (N + 1) < 10 ** 12 and N < 20:
                N += 1
            m_pn = p ** N
            r_pn = rank_mod_m_independent(B, m_pn, require_unit_pivots=True)
            if r_pn != H_rank:
                fail(f"independent rank(B) mod {p}^{N}={m_pn} = {r_pn} != "
                     f"H_rank={H_rank} (mod-q^N spot sample FAILED)", failures)
            else:
                print(f"OK: rank(B) mod {p}^{N}={m_pn} = {r_pn} == H_rank "
                      f"(mod-q^N spot sample, 裁定842(1))")

    report(cert_path, failures, warnings)
    return len(failures) == 0


def report(cert_path, failures, warnings):
    print()
    print(f"=== crosscheck report: {cert_path} ===")
    print(f"scope: modular lane only (裁定842(1)) -- see module docstring "
          f"for exactly what is / is not independently reconstructed")
    print(f"warnings: {len(warnings)}")
    for w in warnings:
        print(f"  - {w}")
    print(f"failures: {len(failures)}")
    for f in failures:
        print(f"  - {f}")
    print(f"RESULT: {'PASS' if not failures else 'FAIL'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python crosscheck/check_torsweep_k13_hnf.py <cert_path>")
        sys.exit(2)
    ok = check(sys.argv[1])
    sys.exit(0 if ok else 1)
