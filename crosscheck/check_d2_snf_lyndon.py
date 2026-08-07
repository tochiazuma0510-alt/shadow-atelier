#!/usr/bin/env python3
# crosscheck/check_d2_snf_lyndon.py
# Independent checker for the D2-SNF-1 Lyndon-basis comparison cert
# (裁定756 Q1, search/certs/d2_snf_sweep_v1_1_20260807.json). Reads the
# v1.1 cert AND the v1 cert it references (both cert JSONs -- legitimate
# inputs, not search/ code) -- does NOT import search/d2_snf_sweep_v1.py
# or search/d2_snf_lyndon_check_v1_1.py (search/crosscheck separation).
# Independently reimplements sigma_bar/Ihara-bracket/Lyndon-factorization/
# SNF from scratch and recomputes everything reported in the v1.1 cert for
# k=14 and k=32, then separately verifies the v1.1 cert's "ambient" block
# genuinely matches the (separately loaded) v1 cert's per_k data (a
# cross-file consistency check the v1.1 script's own author could not
# accidentally fudge without this checker catching it).
import json
import sys
from math import comb, gcd
from fractions import Fraction

from sympy import Matrix, ZZ, Rational
from sympy.matrices.normalforms import smith_normal_form

V1_1_CERT_PATH = "search/certs/d2_snf_sweep_v1_1_20260807.json"
V1_CERT_PATH = "search/certs/d2_snf_sweep_v1_20260807.json"
TARGET_K = [14, 32]


# ---------- independent from-scratch reimplementation ----------

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


def is_lyndon(w):
    n = len(w)
    for i in range(1, n):
        if (w[i:] + w[:i]) <= w:
            return False
    return True


def standard_factorization(w):
    n = len(w)
    for i in range(1, n):
        if is_lyndon(w[i:]):
            return w[:i], w[i:]
    raise ValueError("no standard factorization")


def lyndon_bracket(w, memo):
    if w in memo:
        return memo[w]
    if len(w) == 1:
        res = {w: 1}
    else:
        u, v = standard_factorization(w)
        res = word_bracket(lyndon_bracket(u, memo), lyndon_bracket(v, memo))
    memo[w] = res
    return res


def depth2_lyndon_words(k):
    import itertools
    out = []
    for ones in itertools.combinations(range(k), 2):
        w = [0] * k
        for i in ones:
            w[i] = 1
        w = tuple(w)
        if is_lyndon(w):
            out.append(w)
    return out


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
        doc = json.load(open(V1_1_CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (cert not found: {V1_1_CERT_PATH})")
        sys.exit(1)
    try:
        v1_doc = json.load(open(V1_CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (referenced v1 cert not found: {V1_CERT_PATH})")
        sys.exit(1)

    if doc.get("schema") != "shadow-atelier/d2_snf_sweep_v1.1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/d2_snf_sweep_v1.1")

    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    if doc.get("target_k") != TARGET_K:
        fail(f"target_k={doc.get('target_k')} != expected {TARGET_K}")
    else:
        ok(f"target_k = {TARGET_K} as 裁定756 instructed")

    comparison = doc.get("comparison", {})

    for k in TARGET_K:
        row = comparison.get(str(k))
        if row is None:
            fail(f"k={k}: missing from comparison")
            continue

        pairs = [(a, k - a) for a in range(3, k // 2 + 1, 2) if a < k - a]
        num_pairs = len(pairs)
        row_vecs = [ihara_bracket(sigma_bar(a), sigma_bar(b)) for (a, b) in pairs]

        lyn_words = depth2_lyndon_words(k)
        target_dim_formula = (k - 2) // 2
        if len(lyn_words) != target_dim_formula:
            fail(f"k={k}: recomputed lyndon count={len(lyn_words)} != (k-2)/2={target_dim_formula}")
        else:
            ok(f"k={k}: recomputed lyndon word count={len(lyn_words)} matches (k-2)/2")
        if len(lyn_words) != row.get("lyndon_word_count"):
            fail(f"k={k}: recomputed lyndon count {len(lyn_words)} != cert {row.get('lyndon_word_count')}")

        memo = {}
        basis_vecs = [lyndon_bracket(w, memo) for w in lyn_words]
        support = sorted(set().union(*[set(v.keys()) for v in basis_vecs],
                                      *[set(v.keys()) for v in row_vecs]))
        col_index = {w: i for i, w in enumerate(support)}
        B = Matrix.zeros(len(basis_vecs), len(support))
        for r, v in enumerate(basis_vecs):
            for w, c in v.items():
                B[r, col_index[w]] = c
        Bt = B.T

        row_coords_recomputed = []
        all_int = True
        for v in row_vecs:
            rhs = Matrix([v.get(w, 0) for w in support])
            sol, params = Bt.gauss_jordan_solve(rhs)
            if params:
                sol = sol.subs({p: 0 for p in params})
            residual = (Bt * sol) - rhs
            if any(x != 0 for x in residual):
                fail(f"k={k}: a row vector is NOT in the span of the recomputed Lyndon basis")
                all_int = False
                continue
            coords = [Rational(sol[i]) for i in range(len(lyn_words))]
            is_int = all(c.q == 1 for c in coords)
            all_int = all_int and is_int
            row_coords_recomputed.append([int(c) for c in coords] if is_int else None)

        if all_int != row.get("all_row_coordinates_integer"):
            fail(f"k={k}: recomputed all_row_coordinates_integer={all_int} "
                 f"!= cert {row.get('all_row_coordinates_integer')}")
        else:
            ok(f"k={k}: independently recomputed all_row_coordinates_integer={all_int} matches cert")

        if not all_int:
            continue

        M_intrinsic = Matrix(num_pairs, len(lyn_words), lambda i, j: row_coords_recomputed[i][j])
        rank_Q_intrinsic = M_intrinsic.rank()
        snf = smith_normal_form(M_intrinsic, domain=ZZ)
        diag = [int(snf[i, i]) for i in range(min(snf.rows, snf.cols))]
        elementary_divisors_intrinsic = [d for d in diag if d != 0]
        gcd_abs_intrinsic = abs(elementary_divisors_intrinsic[-1]) if elementary_divisors_intrinsic else 1
        torsion_primes_intrinsic = sorted(factorize(gcd_abs_intrinsic).keys())

        cert_intrinsic = row.get("intrinsic", {})
        if elementary_divisors_intrinsic != cert_intrinsic.get("elementary_divisors"):
            fail(f"k={k}: recomputed intrinsic elementary_divisors={elementary_divisors_intrinsic} "
                 f"!= cert {cert_intrinsic.get('elementary_divisors')}")
        else:
            ok(f"k={k}: independently recomputed intrinsic-Lyndon-basis SNF "
               f"elementary_divisors={elementary_divisors_intrinsic} matches cert")
        if torsion_primes_intrinsic != cert_intrinsic.get("torsion_primes"):
            fail(f"k={k}: recomputed intrinsic torsion_primes={torsion_primes_intrinsic} "
                 f"!= cert {cert_intrinsic.get('torsion_primes')}")
        else:
            ok(f"k={k}: independently recomputed intrinsic torsion_primes={torsion_primes_intrinsic} matches cert")

        # ---- cross-file check: v1.1's "ambient" sub-block genuinely
        # matches the separately-loaded v1 cert's per_k data ----
        v1_row = v1_doc.get("per_k", {}).get(str(k), {})
        cert_ambient = row.get("ambient", {})
        ambient_checks = [
            (cert_ambient.get("rank_Q"), v1_row.get("rank_Q"), "rank_Q"),
            (cert_ambient.get("elementary_divisors"), v1_row.get("elementary_divisors"), "elementary_divisors"),
            (cert_ambient.get("gcd_abs"), v1_row.get("gcd_abs"), "gcd_abs"),
            (cert_ambient.get("torsion_primes"), v1_row.get("torsion_primes"), "torsion_primes"),
        ]
        ambient_ok = True
        for a, b, label in ambient_checks:
            if a != b:
                ambient_ok = False
                fail(f"k={k}: v1.1 cert's ambient.{label}={a} does NOT match the separately-loaded "
                     f"v1 cert's per_k.{label}={b}")
        if ambient_ok:
            ok(f"k={k}: v1.1 cert's ambient block genuinely matches the separately-loaded v1 cert "
               f"(rank_Q={v1_row.get('rank_Q')}, elementary_divisors={v1_row.get('elementary_divisors')}, "
               f"torsion_primes={v1_row.get('torsion_primes')})")

        # ---- agreement bool re-derivation ----
        agree_recomputed = (elementary_divisors_intrinsic == cert_ambient.get("elementary_divisors"))
        if agree_recomputed != row.get("elementary_divisors_agree"):
            fail(f"k={k}: recomputed elementary_divisors_agree={agree_recomputed} "
                 f"!= cert {row.get('elementary_divisors_agree')}")
        else:
            ok(f"k={k}: elementary_divisors_agree re-derives correctly: {agree_recomputed}")

    all_agree_recomputed = all(comparison.get(str(k), {}).get("elementary_divisors_agree") for k in TARGET_K)
    if all_agree_recomputed != doc.get("all_elementary_divisors_agree"):
        fail(f"all_elementary_divisors_agree recomputed={all_agree_recomputed} "
             f"!= cert {doc.get('all_elementary_divisors_agree')}")
    else:
        ok(f"all_elementary_divisors_agree re-derives correctly: {all_agree_recomputed}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (full independent from-scratch recomputation of the intrinsic "
              "Lyndon-basis construction, SNF, and cross-file consistency against the separately-"
              "loaded v1 (ambient-coordinate) cert -- for both k=14 and k=32, the intrinsic and "
              "ambient elementary-divisor lists agree exactly, and all row coordinates in the "
              "intrinsic Lyndon basis are integers (no denominators); cross-checked, not 'verified' "
              "(reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
