#!/usr/bin/env python3
# crosscheck/check_d2_snf_sweep.py
# Independent checker for the D2-SNF-1 cert (裁定752①,
# docs/notes/tor_sweep_design_v1_addendum_b.md §1.4, verbatim).
# Reads the cert JSON for its reported numbers, but does NOT import
# search/d2_snf_sweep_v1.py (search/crosscheck separation). Instead of
# merely re-deriving internal consistency, this checker independently
# REIMPLEMENTS the entire mathematical construction from scratch (its own
# sigma_bar/word_bracket/deriv/ihara_bracket code, its own sympy rank/
# nullspace/SNF calls) directly from k and the addendum's stated formulas
# -- since sigma_bar_a's closed form and the depth-2 Ihara bracket are both
# small, cheap, and fully specified by k alone, a genuine from-scratch
# recomputation is both possible and stronger than a cert-internal-only
# check.
import json
import sys
from math import comb, gcd

from sympy import Matrix, ZZ, Rational
from sympy.matrices.normalforms import smith_normal_form

CERT_PATH = "search/certs/d2_snf_sweep_v1_20260807.json"
K_RANGE = list(range(12, 33, 2))


# ---------- independent (from-scratch) reimplementation ----------

def sigma_bar(a):
    n = a - 1
    vec = {}
    for i in range(n + 1):
        word = (0,) * (n - i) + (1,) + (0,) * i
        coeff = ((-1) ** i) * comb(n, i)
        vec[word] = vec.get(word, 0) + coeff
    sign = (-1) ** ((a - 1) // 2)
    return {w: sign * c for w, c in vec.items() if sign * c != 0}


def word_bracket(u, v):
    out = {}
    for w1, c1 in u.items():
        for w2, c2 in v.items():
            c = c1 * c2
            if c == 0:
                continue
            k1, k2 = w1 + w2, w2 + w1
            out[k1] = out.get(k1, 0) + c
            out[k2] = out.get(k2, 0) - c
    return {w: c for w, c in out.items() if c != 0}


def deriv(f, g):
    img = word_bracket({(1,): 1}, f)
    out = {}
    for w, c in g.items():
        for i, letter in enumerate(w):
            if letter != 1:
                continue
            prefix, suffix = w[:i], w[i + 1:]
            for w2, c2 in img.items():
                key = prefix + w2 + suffix
                out[key] = out.get(key, 0) + c * c2
    return {w: c for w, c in out.items() if c != 0}


def ihara_bracket(f, g):
    out = {}
    for w, c in deriv(f, g).items():
        out[w] = out.get(w, 0) + c
    for w, c in deriv(g, f).items():
        out[w] = out.get(w, 0) - c
    for w, c in word_bracket(f, g).items():
        out[w] = out.get(w, 0) + c
    return {w: c for w, c in out.items() if c != 0}


def primitive_int_vector(rational_list):
    dens = [r.q for r in rational_list]
    L = 1
    for d in dens:
        L = L * d // gcd(L, d)
    ints = [int(r * L) for r in rational_list]
    g = 0
    for v in ints:
        g = gcd(g, abs(v))
    if g == 0:
        return ints
    ints = [v // g for v in ints]
    for v in ints:
        if v != 0:
            if v < 0:
                ints = [-x for x in ints]
            break
    return ints


def proportional_up_to_sign(v1, v2):
    if len(v1) != len(v2):
        return False
    return v1 == v2 or [-x for x in v1] == v2


def factorize(n):
    n = abs(n)
    if n <= 1:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    try:
        doc = json.load(open(CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (cert not found: {CERT_PATH})")
        sys.exit(1)

    if doc.get("schema") != "shadow-atelier/d2_snf_sweep_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/d2_snf_sweep_v1")

    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    per_k_cert = doc.get("per_k", {})

    for k in K_RANGE:
        row = per_k_cert.get(str(k))
        if row is None:
            fail(f"k={k}: missing from cert per_k")
            continue

        pairs = [(a, k - a) for a in range(3, k // 2 + 1, 2) if a < k - a]
        num_pairs = len(pairs)
        row_vecs = [ihara_bracket(sigma_bar(a), sigma_bar(b)) for (a, b) in pairs]
        support = sorted(set().union(*[set(v.keys()) for v in row_vecs])) if row_vecs else []
        col_index = {w: i for i, w in enumerate(support)}
        M = Matrix.zeros(num_pairs, len(support))
        for r, v in enumerate(row_vecs):
            for w, c in v.items():
                M[r, col_index[w]] = c

        rank_Q = M.rank()
        dim_S_k = num_pairs - rank_Q

        if num_pairs != row.get("num_pairs"):
            fail(f"k={k}: recomputed num_pairs={num_pairs} != cert {row.get('num_pairs')}")
        elif rank_Q != row.get("rank_Q"):
            fail(f"k={k}: recomputed rank_Q={rank_Q} != cert {row.get('rank_Q')}")
        elif dim_S_k != row.get("dim_S_k"):
            fail(f"k={k}: recomputed dim_S_k={dim_S_k} != cert {row.get('dim_S_k')}")
        else:
            ok(f"k={k}: independently recomputed num_pairs={num_pairs} rank_Q={rank_Q} "
               f"dim_S_k={dim_S_k} -- matches cert")

        kernel_basis = []
        if dim_S_k > 0:
            nullspace = M.T.nullspace()
            for vec in nullspace:
                comps = [Rational(vec[i]) for i in range(num_pairs)]
                kernel_basis.append(primitive_int_vector(comps))
        cert_kernel = row.get("kernel_basis_primitive", [])
        if len(kernel_basis) != len(cert_kernel):
            fail(f"k={k}: recomputed kernel basis has {len(kernel_basis)} vectors, "
                 f"cert has {len(cert_kernel)}")
        else:
            all_span_match = True
            for kv in kernel_basis:
                if not any(proportional_up_to_sign(kv, cv) for cv in cert_kernel):
                    all_span_match = False
            if all_span_match:
                ok(f"k={k}: independently recomputed kernel basis {kernel_basis} matches cert "
                   f"(each vector proportional up to sign to a cert-reported vector)")
            else:
                fail(f"k={k}: recomputed kernel basis {kernel_basis} does not match cert {cert_kernel}")

        snf = smith_normal_form(M, domain=ZZ)
        diag = [int(snf[i, i]) for i in range(min(snf.rows, snf.cols))]
        elementary_divisors = [d for d in diag if d != 0]
        cert_ed = row.get("elementary_divisors", [])
        if elementary_divisors != cert_ed:
            fail(f"k={k}: recomputed elementary_divisors={elementary_divisors} != cert {cert_ed}")
        else:
            ok(f"k={k}: independently recomputed SNF elementary_divisors={elementary_divisors} "
               f"matches cert exactly")

        gcd_abs = abs(elementary_divisors[-1]) if elementary_divisors else 1
        if gcd_abs != row.get("gcd_abs"):
            fail(f"k={k}: recomputed gcd_abs={gcd_abs} != cert {row.get('gcd_abs')}")
        torsion_primes = sorted(factorize(gcd_abs).keys())
        if torsion_primes != row.get("torsion_primes"):
            fail(f"k={k}: recomputed torsion_primes={torsion_primes} != cert {row.get('torsion_primes')}")
        else:
            ok(f"k={k}: independently recomputed torsion_primes={torsion_primes} matches cert")

        p_pass = (gcd_abs == 1)
        if p_pass != row.get("P_D2_1_pass_this_k"):
            fail(f"k={k}: recomputed P_D2_1_pass_this_k={p_pass} != cert {row.get('P_D2_1_pass_this_k')}")

    all_gcd_abs_1_recomputed = all(
        (per_k_cert.get(str(k), {}).get("gcd_abs") == 1) for k in K_RANGE
    )
    if all_gcd_abs_1_recomputed != doc.get("P_D2_1_all_gcd_abs_1"):
        fail(f"P_D2_1_all_gcd_abs_1 re-derived={all_gcd_abs_1_recomputed} "
             f"!= cert {doc.get('P_D2_1_all_gcd_abs_1')}")
    else:
        ok(f"P_D2_1_all_gcd_abs_1 re-derives correctly from per_k gcd_abs values: {all_gcd_abs_1_recomputed}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (full independent from-scratch recomputation -- own "
              "sigma_bar/Ihara-bracket/SNF code, not imported from search/ -- reproduces every "
              "reported rank, kernel vector, elementary-divisor list, and torsion-prime list "
              "exactly for all k in 12..32; this is cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
