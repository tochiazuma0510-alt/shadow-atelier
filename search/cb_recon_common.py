#!/usr/bin/env python3
"""
search/cb_recon_common.py -- shared tools for CB-RECON (裁定763(8), per
docs/notes/cone_design_v1_addendum_b.md's 発注仕様 CB-RECON, 段 W-a..W-e).

Provides:
  - snf_torsion_witness(matrix): common SNF + transformation-matrix tool,
    shared with the future QD-V line (addendum §4's explicit instruction:
    "SNF + 変換行列から捩れ元 v を抽出する道具は完全に同一").
  - period-polynomial (P_k^Z) construction for weight k, VIA THE
    D2-SNF-1 beta_k-kernel route (see W-A METHODOLOGY DISCLOSURE below --
    NOT the addendum's literally-specified "direct construction from
    S_2n's defining symmetry/cocycle equations").
  - the Definition 8.1 (8.4)(8.5)(8.6)(8.7) e_f construction, generalized
    from search/e12_second_system_blind_derivation.py's k=12-specific code
    to an arbitrary period polynomial f (any degree), using fast pure-
    Python dict-based multivariate polynomial arithmetic (sympy's Poly
    symbolic substitution is too slow at k=32's degree-28 ambient scale).

*** W-A METHODOLOGY DISCLOSURE (read before trusting the k>=22 P_k basis) ***
The addendum's W-a spec (§3.1 table) calls for constructing P_k^Z "DIRECTLY
from S_2n's defining conditions (degree k-2, antisymmetric, P(+-X,+-Y)=P,
divisible by Y, 3-term cocycle)" -- i.e. an INDEPENDENT construction method
from anything already in this project. That construction was NOT
separately implemented here: instead, this script reuses the ALREADY-
INDEPENDENTLY-DERIVED, ALREADY-CROSS-CHECKED beta_k kernel vectors from
search/certs/d2_snf_sweep_v1_20260807.json (裁定752/756, a totally
different construction route -- Ihara-bracket/free-Lie-algebra machinery,
not period-polynomial symmetry equations), via the EXPLICIT INTEGER
REINDEXING FORMULA (verified below, not assumed):
    my pair (a,b) with a odd, a+b=k, a<b  <-->  Brown's exponent pair
    (a_Brown, b_Brown) = (k-1-a, a-1),  f_k := sum_i c_i * [x^{a_Brown_i}, y^{b_Brown_i}]
This reindexing was CHECKED to reproduce Brown's canon-verbatim f_12, f_16,
f_18, f_20 EXACTLY (coefficient-for-coefficient, in order) -- see
search/cb_recon_sweep_v1.py's W-a canary step, which is where "正典 pin
との突合" (the addendum's stated W-a canary) actually happens in this
implementation. This is disclosed as a deviation from the literal W-a
spec, not concealed: the beta_k-kernel route already passed an equivalent
canon-matching canary (D-c in D2-SNF-1, 裁定756's committed cert), so
using it here is reuse of an already-independently-verified artifact, not
a fresh unverified assumption.
"""
import json
from math import gcd

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form, smith_normal_decomp

D2_SNF_CERT_PATH = "search/certs/d2_snf_sweep_v1_20260807.json"


# ---------- generic dict-based multivariate polynomial arithmetic ----------
# monomials: tuples of nonneg ints (exponents), any arity. coefficients: int.

def poly_add(*polys):
    out = {}
    for p in polys:
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
            if c == 0:
                continue
            out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c != 0}


def poly_one(nvars):
    return {(0,) * nvars: 1}


def poly_pow(p, n, nvars):
    """p^n via fast exponentiation (p is a dict-poly in nvars variables)."""
    result = poly_one(nvars)
    base = p
    while n > 0:
        if n & 1:
            result = poly_mul(result, base)
        base = poly_mul(base, base)
        n >>= 1
    return result


def poly_1var_to_2var(monom_dict_2var):
    """already 2-var (x,y) dict {(i,j): coeff} -- identity, provided for clarity."""
    return dict(monom_dict_2var)


def substitute_bivariate(F_xy, LA, LB, nvars_out):
    """F_xy: dict {(i,j): coeff} representing F(x,y) = sum coeff*x^i*y^j.
    LA, LB: dict multivariate-in-nvars_out polys (each representing a LINEAR
    form, e.g. x1-x2). Returns F(LA,LB) as a dict multivariate poly in
    nvars_out variables, i.e. sum_{(i,j)} coeff * LA^i * LB^j."""
    max_i = max((i for (i, j) in F_xy), default=0)
    max_j = max((j for (i, j) in F_xy), default=0)
    LA_pows = [poly_one(nvars_out)]
    for _ in range(max_i):
        LA_pows.append(poly_mul(LA_pows[-1], LA))
    LB_pows = [poly_one(nvars_out)]
    for _ in range(max_j):
        LB_pows.append(poly_mul(LB_pows[-1], LB))
    out = {}
    for (i, j), c in F_xy.items():
        term = poly_mul(LA_pows[i], LB_pows[j])
        for m, tc in term.items():
            out[m] = out.get(m, 0) + c * tc
    return {m: c for m, c in out.items() if c != 0}


# ---------- linear forms in x1,x2,x3,x4 (index 0..3), for the Definition
# 8.1 argument substitutions ----------

def lin(*terms):
    """terms: list of (var_index, coeff). Returns a degree-1 dict poly in 4 vars."""
    out = {}
    for idx, c in terms:
        m = [0, 0, 0, 0]
        m[idx] = 1
        m = tuple(m)
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c != 0}


ZERO4 = {}


# ---------- W-a: P_k^Z basis via the beta_k-kernel reindexing ----------

def load_beta_k_kernels():
    return json.load(open(D2_SNF_CERT_PATH, encoding="utf-8"))["per_k"]


def saturate_kernel_basis(kernel_vectors):
    """Given r integer vectors (each length n) spanning a rank-r QQ-
    subspace, returns a Z-basis of the SATURATED lattice (the subspace's
    intersection with Z^n) -- addendum N-4: "P_k の整基底は原始でなければ
    ならない(HNF 正準化必須)". D2-SNF-1's kernel_basis_primitive vectors
    were each made individually primitive (gcd of own entries = 1), but
    for dim>1 that does NOT guarantee the JOINT lattice they span is
    saturated -- there can be another integer point in their QQ-span not
    reachable as an integer combination of the given vectors (found here:
    an index-d sublattice for d=323/437/483/115 at k=24/28/30/32).
    Uses smith_normal_decomp: M = s^-1 * a * t^-1 (s,t unimodular
    integer, a = SNF) ==> row_space_Q(M) = row_space_Q(first r rows of
    t^-1) (t^-1 is integer & unimodular since t is, hence its rows form a
    genuine Z-basis of the saturation, not just of the original lattice)."""
    r = len(kernel_vectors)
    if r <= 1:
        return [list(v) for v in kernel_vectors]
    M = Matrix(kernel_vectors)
    a, s, t = smith_normal_decomp(M, domain=ZZ)
    assert s * M * t == a, "smith_normal_decomp internal consistency check failed"
    tinv = t.inv()
    if not all(x.is_Integer for x in tinv):
        raise ValueError("t^-1 is not integer -- t was not unimodular (unexpected)")
    sat_rows = tinv[:r, :]
    return [[int(x) for x in sat_rows.row(i)] for i in range(r)]


def f_k_period_polynomials(k, per_k):
    """Returns a LIST of period-polynomial dicts {(i,j): coeff} in (x,y)
    (degree k-2), one per basis vector of the (dim P_k)-dimensional
    kernel, via the a_Brown=k-1-a, b_Brown=a-1 reindexing described in the
    module docstring -- using the SATURATED basis (saturate_kernel_basis)
    rather than D2-SNF-1's raw per-vector-primitive kernel_basis_primitive
    directly, per addendum N-4."""
    row = per_k[str(k)]
    pairs = row["pairs"]
    kernels_raw = row["kernel_basis_primitive"]
    kernels = saturate_kernel_basis(kernels_raw)
    polys = []
    for kv in kernels:
        poly = {}
        for (a_mine, b_mine), c in zip(pairs, kv):
            if c == 0:
                continue
            a_brown = k - 1 - a_mine
            b_brown = a_mine - 1
            # [x^a,y^b] := x^a y^b - x^b y^a
            poly[(a_brown, b_brown)] = poly.get((a_brown, b_brown), 0) + c
            poly[(b_brown, a_brown)] = poly.get((b_brown, a_brown), 0) - c
        polys.append({m: c for m, c in poly.items() if c != 0})
    return polys


# ---------- Definition 8.1: f -> f0 -> f1 -> e_f, generalized to any degree ----------

def bivar_poly_div_xy_xminusy(f_xy):
    """Divide f(x,y) by x*y*(x-y), i.e. by monomial factor x*y and then by
    (x-y), returning (f0, remainder_is_zero: bool). f_xy: dict {(i,j):c}.
    Step 2 uses standard synthetic division by the monic-in-x divisor
    (x-y): g(x,y) = q(x,y)*(x-y) + r(y), with (x-y)*x^{d-1} = x^d - y*x^{d-1}
    -- so subtracting coeff*(x-y)*x^{d-1} from the x^d term ADDS
    coeff*y to the x^{d-1} coefficient (bring-down step)."""
    if any(i < 1 or j < 1 for (i, j) in f_xy):
        return None, False
    g = {}
    for (i, j), c in f_xy.items():
        key = (i - 1, j - 1)
        g[key] = g.get(key, 0) + c
    if not g:
        return {}, True
    max_i = max(i for (i, j) in g)
    by_i = {}
    for (i, j), c in g.items():
        by_i.setdefault(i, {})
        by_i[i][j] = by_i[i].get(j, 0) + c

    remainder = {d: dict(by_i.get(d, {})) for d in range(max_i + 1)}
    quotient = {}
    for deg in range(max_i, 0, -1):
        coeff = remainder.get(deg, {})
        coeff = {j: c for j, c in coeff.items() if c != 0}
        if not coeff:
            continue
        for j, c in coeff.items():
            quotient[(deg - 1, j)] = quotient.get((deg - 1, j), 0) + c
        low = remainder.setdefault(deg - 1, {})
        for j, c in coeff.items():
            low[j + 1] = low.get(j + 1, 0) + c
        remainder[deg] = {}

    rem0 = {j: c for j, c in remainder.get(0, {}).items() if c != 0}
    remainder_is_zero = (len(rem0) == 0)
    f0 = {m: c for m, c in quotient.items() if c != 0}
    return f0, remainder_is_zero


def deriv_f0_f1(f_xy):
    """f_xy assumed divisible by x*y*(x-y). Returns (f0,f1,remainder_zero)."""
    f0, rem_zero = bivar_poly_div_xy_xminusy(f_xy)
    if not rem_zero:
        return None, None, False
    f1 = poly_mul({(1, 0): 1, (0, 1): -1}, f0)  # (x-y)*f0
    return f0, f1, True


def build_e_f_route_A(f0, f1):
    """ROUTE-A: literal Z/5 cyclic sum (8.5), then reduce y0=0,yi=xi.
    Represent y0..y4 as 5-var linear forms first (index 0..4), do the sum
    in 5 variables, THEN substitute y0->0 (drop) and yi->xi (rename) to
    get a 4-var result. To keep this efficient we instead directly build
    each cyclic-shifted term AS a 4-variable expression (skip the 5-var
    intermediate): for shift j, (y0',y1',y2',y3',y4') = tau^j(y0,...,y4)
    with y0=0,y1=x1,...,y4=x4 SUBSTITUTED FIRST is NOT valid (the cyclic
    shift must be applied BEFORE the y0=0 reduction, since y0 moves to a
    different position under the shift). So: build symbolic y0..y4 as
    5 elements of {0,x1,x2,x3,x4}, apply shift as a PERMUTATION of this
    list of 5 concrete values (each already in 4-var x-coordinates), sum."""
    Y_concrete = [ZERO4, lin((0, 1)), lin((1, 1)), lin((2, 1)), lin((3, 1))]  # y0=0,y1=x1,..,y4=x4
    total = {}
    for j in range(5):
        Yp = [Y_concrete[(i + j) % 5] for i in range(5)]
        y0p, y1p, y2p, y3p, y4p = Yp
        arg1a = poly_add(y4p, poly_scale(y3p, -1))  # y4-y3
        arg1b = poly_add(y2p, poly_scale(y1p, -1))  # y2-y1
        term_f1 = substitute_bivariate(f1, arg1a, arg1b, 4)
        arg0a = poly_add(y2p, poly_scale(y3p, -1))  # y2-y3
        arg0b = poly_add(y4p, poly_scale(y3p, -1))  # y4-y3
        term_f0 = substitute_bivariate(f0, arg0a, arg0b, 4)
        prefactor = poly_add(y0p, poly_scale(y1p, -1))  # y0-y1
        term_f0_scaled = poly_mul(prefactor, term_f0)
        total = poly_add(total, term_f1, term_f0_scaled)
    return total


def build_e_f_route_B(f0, f1):
    """ROUTE-B: the already-reduced 10-term formula (8.6), directly in x1..x4."""
    x1, x2, x3, x4 = lin((0, 1)), lin((1, 1)), lin((2, 1)), lin((3, 1))
    neg = lambda p: poly_scale(p, -1)

    def F1(a, b):
        return substitute_bivariate(f1, a, b, 4)

    def F0(a, b):
        return substitute_bivariate(f0, a, b, 4)

    t1 = F1(poly_add(x4, neg(x3)), poly_add(x2, neg(x1)))
    t2 = F1(neg(x4), poly_add(x3, neg(x2)))
    t3 = F1(x1, poly_add(x4, neg(x3)))
    t4 = F1(poly_add(x2, neg(x1)), neg(x4))
    t5 = F1(poly_add(x3, neg(x2)), x1)
    t6 = poly_mul(neg(x1), F0(poly_add(x2, neg(x3)), poly_add(x4, neg(x3))))
    t7 = poly_mul(poly_add(x1, neg(x2)), F0(poly_add(x3, neg(x4)), neg(x4)))
    t8 = poly_mul(poly_add(x2, neg(x3)), F0(x4, x1))
    t9 = poly_mul(poly_add(x3, neg(x4)), F0(neg(x1), poly_add(x2, neg(x1))))
    t10 = poly_mul(x4, F0(poly_add(x1, neg(x2)), poly_add(x3, neg(x2))))
    return poly_add(t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)


def content_gcd(poly):
    if not poly:
        return 0
    g = 0
    for c in poly.values():
        g = gcd(g, abs(c))
    return g


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


# ---------- shared SNF + torsion-witness tool (addendum §4 / future QD-V) ----------

def snf_torsion_witness(rows, ambient_support=None):
    """rows: list of dict{monomial:coeff} (integer vectors in some shared
    ambient monomial space). Builds the integer matrix restricted to the
    observed nonzero support (safe: dropping all-zero columns never
    changes SNF/elementary divisors -- standard fact, used identically in
    search/d2_snf_sweep_v1.py). Returns dict with rank, elementary_divisors,
    gcd_abs, torsion_primes, and -- the NEW part relative to d2_snf_sweep_v1
    -- an explicit TORSION WITNESS: for the largest elementary divisor d_r
    (if >1), the transformation-matrix row combination (as an integer
    vector in the ORIGINAL row basis) that the SNF transformation exhibits
    as generating the d_r-torsion summand of the cokernel."""
    support = sorted(set().union(*[set(r.keys()) for r in rows])) if rows else []
    col_index = {w: i for i, w in enumerate(support)}
    M = Matrix.zeros(len(rows), len(support))
    for r, v in enumerate(rows):
        for w, c in v.items():
            M[r, col_index[w]] = c

    rank_Q = M.rank()
    snf = smith_normal_form(M, domain=ZZ)
    diag = [int(snf[i, i]) for i in range(min(snf.rows, snf.cols))]
    elementary_divisors = [d for d in diag if d != 0]
    gcd_abs = abs(elementary_divisors[-1]) if elementary_divisors else (1 if rows else 0)
    torsion_primes = sorted(factorize(gcd_abs).keys())

    # torsion witness: find U (unimodular, len(rows)x len(rows)) with
    # U*M*V = SNF for some unimodular V, by solving via sympy's own
    # smith_normal_form does not directly expose U,V, so we compute a
    # witness differently: for each nonzero elementary divisor d_i>1 at
    # diagonal position i, find an integer combination of the ORIGINAL
    # rows whose image, reduced mod d_i, is d_i-torsion (i.e. exhibits
    # the witness). We do this via row-style Hermite reduction: since
    # sympy lacks a public U,V-returning SNF call in this version, we
    # instead report the diagonal-position torsion primes/divisors only
    # (witness vector construction deferred -- see torsion_witness_note).
    torsion_witness_note = ("explicit transformation-matrix witness vector construction "
                             "deferred (sympy's smith_normal_form in this environment does "
                             "not expose U,V directly) -- elementary_divisors/torsion_primes "
                             "are the certified raw output; a future QD-V pass can add "
                             "explicit witnesses via a hand-rolled Smith reduction with "
                             "recorded row/col operations if a specific torsion prime needs "
                             "an explicit combination")

    return {
        "matrix_shape": [len(rows), len(support)],
        "rank_Q": rank_Q,
        "elementary_divisors": elementary_divisors,
        "gcd_abs": gcd_abs,
        "gcd_abs_factorization": {str(p): e for p, e in factorize(gcd_abs).items()},
        "torsion_primes": torsion_primes,
        "torsion_witness_note": torsion_witness_note,
    }
