#!/usr/bin/env python3
# crosscheck/check_t2_hecke.py
# Independent checker for the T2-HECKE cert (裁定769(3),
# search/certs/t2_hecke_v1_20260807.json). Does NOT import
# search/t2_hecke_common.py or search/t2_hecke_v1.py (search/crosscheck
# separation). Reads the D2-SNF-1 cert directly (data, not code) and
# independently reimplements: the f_k reindexing+saturation (own code,
# same as check_cb_recon_sweep.py's independent reimplementation), the
# Heilbronn-style Hecke matrix set, the substitution action, the
# coboundary-projection linear solve, charpoly/disc, commutativity, and
# the order-index computation -- then compares every reported cert value.
import json
import sys
from math import comb, gcd

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_decomp

D2_SNF_CERT_PATH = "search/certs/d2_snf_sweep_v1_20260807.json"
CERT_PATH = "search/certs/t2_hecke_v1_20260807.json"


# ---------- independent P_k^Z basis (same reindexing+saturation as check_cb_recon_sweep.py) ----------

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
    return polys


# ---------- independent Hecke machinery ----------

def matrix_set(n):
    mats = []
    for a in range(1, n + 1):
        for d in range(1, n + 1):
            for b in range(0, d):
                for c in range(0, a):
                    if a * d - b * c == n:
                        mats.append((a, b, c, d))
    return mats


def apply_matrix(poly, a, b, c, d):
    out = {}
    for (i, j), coeff in poly.items():
        polyX = {}
        for p in range(i + 1):
            cc = comb(i, p) * (a ** (i - p)) * (b ** p)
            polyX[(i - p, p)] = polyX.get((i - p, p), 0) + cc
        polyY = {}
        for p in range(j + 1):
            cc = comb(j, p) * (c ** (j - p)) * (d ** p)
            polyY[(j - p, p)] = polyY.get((j - p, p), 0) + cc
        for (u1, v1), c1 in polyX.items():
            for (u2, v2), c2 in polyY.items():
                key = (u1 + u2, v1 + v2)
                out[key] = out.get(key, 0) + coeff * c1 * c2
    return {m: c for m, c in out.items() if c != 0}


def p_add(*ps):
    out = {}
    for p in ps:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c != 0}


def hecke_apply(poly, n):
    result = {}
    for (a, b, c, d) in matrix_set(n):
        result = p_add(result, apply_matrix(poly, a, b, c, d))
    return result


def decompose(vec, basis_polys, coboundary_poly):
    all_basis = list(basis_polys) + [coboundary_poly]
    support = sorted(set().union(*[set(p.keys()) for p in all_basis], set(vec.keys())))
    A = Matrix([[p.get(m, 0) for p in all_basis] for m in support])
    b = Matrix([vec.get(m, 0) for m in support])
    sol, params = A.gauss_jordan_solve(b)
    if params:
        sol = sol.subs({p: 0 for p in params})
    residual = (A * sol) - b
    residual_is_zero = all(x == 0 for x in residual)
    coeffs = [sol[i] for i in range(len(basis_polys))]
    lam = sol[len(basis_polys)]
    return coeffs, lam, residual_is_zero


def hecke_matrix(k, n, basis):
    w = k - 2
    cob = {(w, 0): 1, (0, w): -1}
    cols = []
    all_ok = True
    for P in basis:
        TnP = hecke_apply(P, n)
        coeffs, lam, resid_zero = decompose(TnP, basis, cob)
        all_ok = all_ok and resid_zero and all(c.q == 1 for c in coeffs)
        cols.append([int(c) for c in coeffs])
    dim = len(basis)
    M = [[cols[j][i] for j in range(dim)] for i in range(dim)]
    return M, all_ok


def charpoly_2x2(M):
    a, b = M[0]
    c, d = M[1]
    return a + d, a * d - b * c


def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(len(B[0]))] for i in range(n)]


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


def squarefree_part(n):
    sf = 1
    for p, e in factorize(n).items():
        if e % 2 == 1:
            sf *= p
    return sf


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

    if doc.get("schema") != "shadow-atelier/t2_hecke_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/t2_hecke_v1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    d2 = json.load(open(D2_SNF_CERT_PATH, encoding="utf-8"))
    per_k_d2 = d2["per_k"]

    ms2 = matrix_set(2)
    if sorted(ms2) != sorted(tuple(m) for m in doc["H_a_matrix_set_T2"]):
        fail(f"H-a matrix set mismatch: recomputed {ms2} vs cert {doc['H_a_matrix_set_T2']}")
    else:
        ok(f"H-a matrix set T_2 independently recomputed: {ms2} (matches cert)")

    # ---- H-b calibration ----
    basis12 = f_k_polys(12, per_k_d2)
    M12, ok12 = hecke_matrix(12, 2, basis12)
    t2_12 = M12[0][0]
    if t2_12 != -24 or t2_12 != doc["H_b_calibration"]["T2_weight12"]:
        fail(f"H-b: recomputed T2_weight12={t2_12} != -24 or != cert {doc['H_b_calibration']['T2_weight12']}")
    else:
        ok(f"H-b: independently recomputed T2_weight12={t2_12} matches -24 and cert")

    M12_T3, ok12_T3 = hecke_matrix(12, 3, basis12)
    t3_12 = M12_T3[0][0]
    if t3_12 != doc["due_diligence_T3_weight12"]["T3_weight12"]:
        fail(f"T3_weight12 recomputed={t3_12} != cert {doc['due_diligence_T3_weight12']['T3_weight12']}")
    else:
        ok(f"T3_weight12 independently recomputed: {t3_12} (matches cert; classical tau(3)=252 crosscheck: {t3_12==252})")

    # ---- H-c ----
    for k in [12, 16, 18, 20, 22, 26]:
        basis = f_k_polys(k, per_k_d2)
        M, allok = hecke_matrix(k, 2, basis)
        val = M[0][0]
        cert_val = doc["H_c_a2_by_weight"][str(k)]["T2_scalar"]
        if val != cert_val:
            fail(f"H-c k={k}: recomputed T2={val} != cert {cert_val}")
        else:
            ok(f"H-c k={k}: independently recomputed T2={val} matches cert")

    # ---- H-d/H-e ----
    T2_matrices = {}
    for k in [24, 28, 30, 32]:
        basis = f_k_polys(k, per_k_d2)
        M, allok = hecke_matrix(k, 2, basis)
        T2_matrices[k] = M
        trace, det = charpoly_2x2(M)
        disc = trace * trace - 4 * det
        cert_row = doc["H_d_H_e_disc_by_weight"][str(k)]
        if trace != cert_row["trace"] or det != cert_row["det"] or disc != cert_row["disc"]:
            fail(f"H-d/e k={k}: recomputed trace={trace} det={det} disc={disc} != cert "
                 f"trace={cert_row['trace']} det={cert_row['det']} disc={cert_row['disc']}")
        else:
            ok(f"H-d/e k={k}: independently recomputed trace={trace} det={det} disc={disc} matches cert")

    # ---- P-T2-1 ----
    disc24 = T2_matrices[24]
    trace24, det24 = charpoly_2x2(disc24)
    disc24_val = trace24 * trace24 - 4 * det24
    p_t2_1_recomputed = {
        "144169_divides_disc": (disc24_val % 144169 == 0),
        "disc_equals_576_times_144169": (disc24_val == 576 * 144169),
    }
    for key, val in p_t2_1_recomputed.items():
        if val != doc["P_T2_1"][key]:
            fail(f"P-T2-1.{key} recomputed={val} != cert {doc['P_T2_1'][key]}")
    else:
        ok(f"P-T2-1 independently recomputed: {p_t2_1_recomputed} (matches cert)")

    # ---- H-f commutativity ----
    basis24 = f_k_polys(24, per_k_d2)
    M24_T3, ok24_T3 = hecke_matrix(24, 3, basis24)
    prod_23 = matmul(T2_matrices[24], M24_T3)
    prod_32 = matmul(M24_T3, T2_matrices[24])
    commute = (prod_23 == prod_32)
    if commute != doc["H_f_commutativity"]["commute"] or prod_23 != doc["H_f_commutativity"]["T2_T3"]:
        fail(f"H-f: recomputed commute={commute} T2T3={prod_23} != cert")
    else:
        ok(f"H-f: independently recomputed T2*T3=T3*T2 commute={commute} matches cert")

    # ---- H-g order index ----
    for k in [24, 28, 30, 32]:
        trace, det = charpoly_2x2(T2_matrices[k])
        disc = trace * trace - 4 * det
        sf = squarefree_part(disc)
        field_disc = sf if (sf % 4 == 1) else 4 * sf
        idx_sq = disc // field_disc if disc % field_disc == 0 else None
        idx = None
        if idx_sq is not None:
            r = int(round(idx_sq ** 0.5))
            if r * r == idx_sq:
                idx = r
        cert_row = doc["H_g_order_index"][str(k)]
        if sf != cert_row["squarefree_part"] or field_disc != cert_row["field_disc_Q_sqrt_sf"] or idx != cert_row["index_Z_T2_in_maximal_order"]:
            fail(f"H-g k={k}: recomputed sf={sf} field_disc={field_disc} idx={idx} != cert "
                 f"sf={cert_row['squarefree_part']} field_disc={cert_row['field_disc_Q_sqrt_sf']} idx={cert_row['index_Z_T2_in_maximal_order']}")
        else:
            ok(f"H-g k={k}: independently recomputed squarefree_part={sf} field_disc={field_disc} "
               f"index={idx} matches cert")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independent from-scratch reimplementation -- own P_k basis "
              "reconstruction, own Hecke matrix-set/substitution/coboundary-projection code, own "
              "charpoly/disc/commutativity/order-index code, none imported from search/ -- reproduces "
              "every reported value exactly; cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
