#!/usr/bin/env python3
# crosscheck/check_cb_recon_sweep.py
# Independent checker for the CB-RECON e-side sweep cert (裁定763(8),
# search/certs/cb_recon_sweep_v1_20260807.json). Does NOT import
# search/cb_recon_common.py or search/cb_recon_sweep_v1.py (search/
# crosscheck separation). Reads the D2-SNF-1 cert directly (data, not
# code) and independently reimplements: the f_k reindexing, the kernel-
# basis saturation (own from-scratch smith_normal_decomp-based routine),
# the Definition 8.1 (8.5)/(8.6) construction (own polynomial-division and
# substitution code), the SNF/gcd scoring, and the mod-103 rank
# computation -- then compares every reported cert value.
import json
import sys
from math import gcd

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form, smith_normal_decomp

D2_SNF_CERT_PATH = "search/certs/d2_snf_sweep_v1_20260807.json"
CERT_PATH = "search/certs/cb_recon_sweep_v1_20260807.json"


# ---------- independent reimplementation ----------

def saturate(kernel_vectors):
    r = len(kernel_vectors)
    if r <= 1:
        return [list(v) for v in kernel_vectors]
    M = Matrix(kernel_vectors)
    a, s, t = smith_normal_decomp(M, domain=ZZ)
    if s * M * t != a:
        raise ValueError("smith_normal_decomp check failed")
    tinv = t.inv()
    if not all(x.is_Integer for x in tinv):
        raise ValueError("t^-1 not integer")
    sat = tinv[:r, :]
    return [[int(x) for x in sat.row(i)] for i in range(r)]


def f_k_polys(k, per_k):
    row = per_k[str(k)]
    pairs = row["pairs"]
    kernels = saturate(row["kernel_basis_primitive"])
    polys = []
    for kv in kernels:
        poly = {}
        for (a_mine, b_mine), c in zip(pairs, kv):
            if c == 0:
                continue
            ab, bb = k - 1 - a_mine, a_mine - 1
            poly[(ab, bb)] = poly.get((ab, bb), 0) + c
            poly[(bb, ab)] = poly.get((bb, ab), 0) - c
        polys.append({m: c for m, c in poly.items() if c != 0})
    return polys, kernels


def poly_add(*ps):
    out = {}
    for p in ps:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c != 0}


def poly_scale(p, s):
    return {m: c * s for m, c in p.items() if c * s != 0}


def poly_mul(p, q):
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(a + b for a, b in zip(m1, m2))
            c = c1 * c2
            if c:
                out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c != 0}


def poly_pow(p, n, nvars):
    result = {(0,) * nvars: 1}
    base = p
    while n > 0:
        if n & 1:
            result = poly_mul(result, base)
        base = poly_mul(base, base)
        n >>= 1
    return result


def divide_by_xy_xminusy(f_xy):
    if any(i < 1 or j < 1 for (i, j) in f_xy):
        return None, False
    g = {}
    for (i, j), c in f_xy.items():
        key = (i - 1, j - 1)
        g[key] = g.get(key, 0) + c
    if not g:
        return {}, True
    max_i = max(i for i, j in g)
    by_i = {}
    for (i, j), c in g.items():
        by_i.setdefault(i, {})
        by_i[i][j] = by_i[i].get(j, 0) + c
    remainder = {d: dict(by_i.get(d, {})) for d in range(max_i + 1)}
    quotient = {}
    for deg in range(max_i, 0, -1):
        coeff = {j: c for j, c in remainder.get(deg, {}).items() if c != 0}
        if not coeff:
            continue
        for j, c in coeff.items():
            quotient[(deg - 1, j)] = quotient.get((deg - 1, j), 0) + c
        low = remainder.setdefault(deg - 1, {})
        for j, c in coeff.items():
            low[j + 1] = low.get(j + 1, 0) + c
        remainder[deg] = {}
    rem0 = {j: c for j, c in remainder.get(0, {}).items() if c != 0}
    return {m: c for m, c in quotient.items() if c != 0}, (len(rem0) == 0)


def build_e_route_B(f0, f1):
    def lin(idx, c=1):
        m = [0, 0, 0, 0]
        m[idx] = 1
        return {tuple(m): c}

    x1, x2, x3, x4 = lin(0), lin(1), lin(2), lin(3)
    neg = lambda p: poly_scale(p, -1)

    def substitute(F, A, B):
        max_i = max((i for i, j in F), default=0)
        max_j = max((j for i, j in F), default=0)
        A_pows = [{(0, 0, 0, 0): 1}]
        for _ in range(max_i):
            A_pows.append(poly_mul(A_pows[-1], A))
        B_pows = [{(0, 0, 0, 0): 1}]
        for _ in range(max_j):
            B_pows.append(poly_mul(B_pows[-1], B))
        out = {}
        for (i, j), c in F.items():
            term = poly_mul(A_pows[i], B_pows[j])
            for m, tc in term.items():
                out[m] = out.get(m, 0) + c * tc
        return {m: c for m, c in out.items() if c != 0}

    def F1(a, b):
        return substitute(f1, a, b)

    def F0(a, b):
        return substitute(f0, a, b)

    terms = [
        F1(poly_add(x4, neg(x3)), poly_add(x2, neg(x1))),
        F1(neg(x4), poly_add(x3, neg(x2))),
        F1(x1, poly_add(x4, neg(x3))),
        F1(poly_add(x2, neg(x1)), neg(x4)),
        F1(poly_add(x3, neg(x2)), x1),
        poly_mul(neg(x1), F0(poly_add(x2, neg(x3)), poly_add(x4, neg(x3)))),
        poly_mul(poly_add(x1, neg(x2)), F0(poly_add(x3, neg(x4)), neg(x4))),
        poly_mul(poly_add(x2, neg(x3)), F0(x4, x1)),
        poly_mul(poly_add(x3, neg(x4)), F0(neg(x1), poly_add(x2, neg(x1)))),
        poly_mul(x4, F0(poly_add(x1, neg(x2)), poly_add(x3, neg(x2)))),
    ]
    return poly_add(*terms)


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


def snf_of_rows(rows):
    support = sorted(set().union(*[set(r.keys()) for r in rows])) if rows else []
    col_index = {w: i for i, w in enumerate(support)}
    M = Matrix.zeros(len(rows), len(support))
    for r, v in enumerate(rows):
        for w, c in v.items():
            M[r, col_index[w]] = c
    snf = smith_normal_form(M, domain=ZZ)
    diag = [int(snf[i, i]) for i in range(min(snf.rows, snf.cols))]
    ed = [d for d in diag if d != 0]
    gcd_abs = abs(ed[-1]) if ed else (1 if rows else 0)
    return ed, gcd_abs, sorted(factorize(gcd_abs).keys())


def rank_mod_p(rows, p):
    support = sorted(set().union(*[set(r.keys()) for r in rows])) if rows else []
    col_index = {w: i for i, w in enumerate(support)}
    M = [[0] * len(support) for _ in rows]
    for ridx, r in enumerate(rows):
        for w, c in r.items():
            M[ridx][col_index[w]] = c % p
    rank = 0
    row_idx = 0
    ncols = len(support)
    for col in range(ncols):
        pivot = None
        for r in range(row_idx, len(M)):
            if M[r][col] % p != 0:
                pivot = r
                break
        if pivot is None:
            continue
        M[row_idx], M[pivot] = M[pivot], M[row_idx]
        inv = pow(M[row_idx][col], p - 2, p)
        M[row_idx] = [(x * inv) % p for x in M[row_idx]]
        for r in range(len(M)):
            if r != row_idx and M[r][col] % p != 0:
                factor = M[r][col]
                M[r] = [(M[r][c2] - factor * M[row_idx][c2]) % p for c2 in range(ncols)]
        row_idx += 1
        rank += 1
        if row_idx == len(M):
            break
    return rank


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

    if doc.get("schema") != "shadow-atelier/cb_recon_sweep_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/cb_recon_sweep_v1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    d2 = json.load(open(D2_SNF_CERT_PATH, encoding="utf-8"))
    per_k_d2 = d2["per_k"]

    canon_expected = {
        12: {(8, 2): 1, (2, 8): -1, (6, 4): -3, (4, 6): 3},
        16: {(12, 2): 2, (2, 12): -2, (10, 4): -7, (4, 10): 7, (8, 6): 11, (6, 8): -11},
        18: {(14, 2): 8, (2, 14): -8, (12, 4): -25, (4, 12): 25, (10, 6): 26, (6, 10): -26},
        20: {(16, 2): 3, (2, 16): -3, (14, 4): -10, (4, 14): 10, (12, 6): 14, (6, 12): -14,
             (10, 8): -13, (8, 10): 13},
    }
    for k, exp in canon_expected.items():
        polys, _ = f_k_polys(k, per_k_d2)
        match = (polys[0] == exp)
        if not match:
            fail(f"k={k}: recomputed f_k does not match canon")
        else:
            ok(f"k={k}: recomputed f_k matches canon (W-a canary)")

    per_k_cert = doc.get("per_k", {})
    for k in [16, 18, 20, 22, 24, 26, 28, 30, 32]:
        row = per_k_cert.get(str(k))
        if row is None:
            fail(f"k={k}: missing from cert")
            continue

        polys, kernels_sat = f_k_polys(k, per_k_d2)
        dim_P_k = len(polys)
        if dim_P_k != row.get("dim_P_k"):
            fail(f"k={k}: recomputed dim_P_k={dim_P_k} != cert {row.get('dim_P_k')}")

        if dim_P_k > 1:
            sd = row.get("saturation_diagnostic", {})
            if kernels_sat != sd.get("kernel_basis_saturated"):
                fail(f"k={k}: recomputed saturated kernel basis {kernels_sat} != cert {sd.get('kernel_basis_saturated')}")
            else:
                ok(f"k={k}: independently recomputed saturated kernel basis matches cert")

        e_rows = []
        checks_ok = True
        for idx, f in enumerate(polys):
            f0, remzero = divide_by_xy_xminusy(f)
            if not remzero:
                fail(f"k={k} idx={idx}: remainder nonzero in recomputation")
                checks_ok = False
                break
            f1 = poly_mul({(1, 0): 1, (0, 1): -1}, f0)
            e = build_e_route_B(f0, f1)
            e_rows.append(e)
            cert_check = row["internal_checks"][idx]
            if len(e) != cert_check["e_f_num_terms"]:
                fail(f"k={k} idx={idx}: recomputed e_f_num_terms={len(e)} != cert {cert_check['e_f_num_terms']}")
                checks_ok = False
        if not checks_ok:
            continue
        ok(f"k={k}: independently recomputed e_f (route B, own code) for all {dim_P_k} basis vector(s), "
           f"term counts match cert")

        ed, gcd_abs, tp = snf_of_rows(e_rows)
        cert_snf = row["snf_result"]
        if ed != cert_snf["elementary_divisors"]:
            fail(f"k={k}: recomputed elementary_divisors={ed} != cert {cert_snf['elementary_divisors']}")
        elif gcd_abs != cert_snf["gcd_abs"]:
            fail(f"k={k}: recomputed gcd_abs={gcd_abs} != cert {cert_snf['gcd_abs']}")
        elif tp != cert_snf["torsion_primes"]:
            fail(f"k={k}: recomputed torsion_primes={tp} != cert {cert_snf['torsion_primes']}")
        else:
            ok(f"k={k}: independently recomputed SNF elementary_divisors={ed} torsion_primes={tp} "
               f"matches cert exactly")

        if k == 24:
            r103 = rank_mod_p(e_rows, 103)
            if r103 != doc["P_CONE_6"]["rank_F103_E24"]:
                fail(f"k=24: recomputed rank_F103={r103} != cert {doc['P_CONE_6']['rank_F103_E24']}")
            else:
                ok(f"k=24: independently recomputed rank_F103(E_24)={r103} matches cert")

    # ---- re-derive P-CONE-3/4/5 summary bools from per_k data ----
    controls = {22: 11, 26: 13, 28: 7, 30: 5}
    for k, p in controls.items():
        appears = (p in per_k_cert[str(k)]["snf_result"]["torsion_primes"])
        if appears != doc["P_CONE_3"][str(k)]["appears_in_torsion_primes"]:
            fail(f"P_CONE_3 k={k}: recomputed appears={appears} != cert")
    ok("P_CONE_3 control-prime-appearance bools re-derive correctly from per_k torsion_primes")

    guaranteed = [16, 18, 20, 22, 24, 26, 28, 30]
    all_sat = all(per_k_cert[str(k)]["saturated"] for k in guaranteed)
    if all_sat != doc["P_CONE_4"]["all_saturated"]:
        fail(f"P_CONE_4: recomputed all_saturated={all_sat} != cert {doc['P_CONE_4']['all_saturated']}")
    else:
        ok(f"P_CONE_4.all_saturated re-derives correctly: {all_sat}")

    p37 = (37 in per_k_cert["32"]["snf_result"]["torsion_primes"])
    if p37 != doc["P_CONE_5"]["prime_37_appears_in_torsion_primes"]:
        fail("P_CONE_5: prime_37_appears_in_torsion_primes mismatch")
    else:
        ok(f"P_CONE_5.prime_37_appears_in_torsion_primes re-derives correctly: {p37}")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independent from-scratch reimplementation -- own f_k "
              "reindexing+saturation, own Definition 8.1 route-B construction, own SNF/rank code, "
              "none imported from search/ -- reproduces every reported value for all 9 weights "
              "exactly; cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
