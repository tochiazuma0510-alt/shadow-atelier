#!/usr/bin/env python3
"""
search/t2_hecke_common.py -- shared Hecke-operator machinery for T2-HECKE
(裁定769(3), per docs/notes/cone_design_v1_addendum_d.md §3.2 発注仕様
T2-HECKE, 段 H-a..H-g).

*** Formula provenance (important, read before trusting) ***
The exact, fully-normalized classical formula for how T_n acts on period
polynomials is genuinely subtle (path/coboundary corrections between
cusps -- this implementer tried and failed several plausible-looking
formulas against the tau(2)=-24 calibration before consulting the
mathematician role for a from-scratch derivation, NOT external web
literature -- 文献ゲート compliance: this is internal mathematical
reasoning/established classical theory, not a paper lookup). The
mathematician's derivation (Manin's continued-fraction telescoping
construction of the period-polynomial coboundary correction) was
INDEPENDENTLY numerically re-verified by this implementer before use (see
search/t2_hecke_v1.py's H-b step) -- both the matrix-set claim and, more
importantly, the KEY STRUCTURAL FINDING that Brown's period-polynomial
representative f_k is NOT itself a Hecke eigenvector: applying T_n
produces (Hecke-eigenvector combination) + lambda*(X^(k-2) - Y^(k-2)),
where X^w - Y^w is a genuine coboundary (Q=Y^w, Q|S - Q = X^w-Y^w) that
must be projected out to recover the honest action on P_k^Z (isomorphic,
as a Hecke module, to S_k(SL_2(Z))). This coboundary-projection step is
NOT mentioned in the addendum's H-a/H-b text -- it was discovered during
this implementation and is disclosed here, not hidden; it is essential
for H-b's calibration to pass at all (verified: without projecting out
the coboundary, T_2 f_12 != -24 f_12 exactly -- it equals
-24 f_12 + 108(X^10-Y^10), confirmed by direct computation).

Hecke action formula (mathematician-derived, independently verified for
k=12 by direct hand+machine computation):
    matrix set  T_n := {(a,b;c,d) in M_2(Z) : ad-bc=n, a>c>=0, d>b>=0}
    (T_n P)(X,Y) := sum_{M in T_n} P(aX+bY, cX+dY)      (no prefactor)
"""
import json
import sys
from math import gcd

sys.path.insert(0, "search")
import cb_recon_common as cb  # reuse the ALREADY-VALIDATED P_k^Z basis construction (W-a route)

from sympy import Matrix, Rational, sqrt as sympy_sqrt, nsimplify


# ---------- 2-variable dict-poly arithmetic (X,Y) -> {(i,j): coeff} ----------

def p_add(*ps):
    out = {}
    for p in ps:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c != 0}


def p_scale(p, s):
    return {m: c * s for m, c in p.items() if c * s != 0}


def hecke_matrix_set(n):
    """T_n = {(a,b;c,d) in M_2(Z): ad-bc=n, a>c>=0, d>b>=0}. Brute-force
    enumeration (small n here: 2,3,4,6 at most) -- a,d bounded by n since
    ad-bc=n with b,c>=0 forces ad>=n, and a>c>=0,d>b>=0 with bc=ad-n>=0
    bounds the search trivially for these small n."""
    mats = []
    for a in range(1, n + 1):
        for d in range(1, n + 1):
            for b in range(0, d):
                for c in range(0, a):
                    if a * d - b * c == n:
                        mats.append((a, b, c, d))
    return mats


def apply_matrix(poly, a, b, c, d):
    """poly(X,Y) -> poly(aX+bY, cX+dY), via binomial expansion."""
    from math import comb
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


def hecke_apply(poly, n):
    mats = hecke_matrix_set(n)
    result = {}
    for (a, b, c, d) in mats:
        result = p_add(result, apply_matrix(poly, a, b, c, d))
    return result, mats


def coboundary(k):
    """X^(k-2) - Y^(k-2)."""
    w = k - 2
    return {(w, 0): 1, (0, w): -1}


def decompose(vec, basis_polys, coboundary_poly):
    """Solve vec = sum_i c_i * basis_polys[i] + lam * coboundary_poly
    EXACTLY (over Q), returns (coeffs list, lam, residual_is_zero: bool).
    Uses a plain linear solve over the union support."""
    all_basis = list(basis_polys) + [coboundary_poly]
    support = sorted(set().union(*[set(p.keys()) for p in all_basis], set(vec.keys())))
    A = Matrix([[p.get(m, 0) for p in all_basis] for m in support])
    b = Matrix([vec.get(m, 0) for m in support])
    sol, params = A.gauss_jordan_solve(b)
    if params:
        # underdetermined -- shouldn't happen if basis+coboundary independent
        # and support spans correctly; substitute free params = 0 and flag via residual
        sol = sol.subs({p: 0 for p in params})
    residual = (A * sol) - b
    residual_is_zero = all(x == 0 for x in residual)
    coeffs = [sol[i] for i in range(len(basis_polys))]
    lam = sol[len(basis_polys)]
    return coeffs, lam, residual_is_zero


def load_per_k():
    return cb.load_beta_k_kernels()


def p_k_basis(k, per_k):
    """The already-validated P_k^Z basis (W-a route, addendum B / 裁定763),
    reused unchanged."""
    return cb.f_k_period_polynomials(k, per_k)


def hecke_matrix_on_Pk(k, n, per_k, basis=None):
    """Computes the dim(P_k) x dim(P_k) integer matrix of T_n acting on
    P_k^Z (columns = images of each basis vector, expressed in the SAME
    basis, after projecting out the coboundary direction). Returns
    (matrix as list-of-lists of Fractions/ints, lambdas list, all_integer:
    bool, all_residual_zero: bool, mats_used)."""
    if basis is None:
        basis = p_k_basis(k, per_k)
    cob = coboundary(k)
    cols = []
    lambdas = []
    all_residual_zero = True
    mats_used = None
    for P in basis:
        Tn_P, mats = hecke_apply(P, n)
        mats_used = mats
        coeffs, lam, resid_zero = decompose(Tn_P, basis, cob)
        cols.append(coeffs)
        lambdas.append(lam)
        all_residual_zero = all_residual_zero and resid_zero
    dim = len(basis)
    # cols[j] = coordinates of T_n(basis[j]) -- matrix acts on column vectors,
    # M[i][j] = coeff of basis[i] in T_n(basis[j])
    M = [[cols[j][i] for j in range(dim)] for i in range(dim)]
    all_integer = all(all(c.q == 1 for c in row) if hasattr(row[0], 'q') else True
                       for row in M) if dim else True
    # normalize: convert Rational->int where possible, else keep Rational
    M_out = [[int(c) if getattr(c, 'q', 1) == 1 else c for c in row] for row in M]
    all_integer = all(isinstance(c, int) for row in M_out for c in row)
    return M_out, lambdas, all_integer, all_residual_zero, mats_used


def charpoly_2x2(M):
    """M: 2x2 list-of-lists (int). Returns (trace, det, charpoly coeffs
    [1,-trace,det] for x^2 - trace x + det)."""
    a, b = M[0]
    c, d = M[1]
    trace = a + d
    det = a * d - b * c
    return trace, det


def discriminant_2x2(M):
    """disc of char poly x^2 - trace x + det = trace^2 - 4*det."""
    trace, det = charpoly_2x2(M)
    return trace * trace - 4 * det


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
    fact = factorize(n)
    sf = 1
    for p, e in fact.items():
        if e % 2 == 1:
            sf *= p
    return sf
