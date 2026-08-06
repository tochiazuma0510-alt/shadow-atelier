#!/usr/bin/env python3
"""
edim_semidirect_v1.py -- 【EDIM-GAP-1】semidirect model implementation.

Spec (verbatim authority): docs/notes/edim_semidirect_model_design_v1.md.
Commissioned: 裁定646 (via 司令塔, this session), implementer scope = data
structures + bracket formula + delta_X/delta_Y recursion + rho bracket-tree
re-evaluation + calibration C-1..C-3, THEN STOP AND REPORT at C-4 (C-4 must
match search/certs/edim56_20260806.json exactly -- lifeline check, per
instruction). k=7+ was not run by that original pass.

Acceleration wave 112e (2026-08-06) adds an exact production backend for
k=3..12 feasibility.  It computes H first, evaluates only nu_k o j on H by
degree-one rho substitution in the tagged ambient tensor algebras, and takes
rank there using the injective free-Lie/PBW embedding.  The legacy delta-table
and full-rho functions remain below as an independent small-degree comparison
path; production no longer constructs either object.

Model (design doc SS1): t = n rtimes h, n = Lie(A,B,C) free, h = Lie(X,Y)
free. Bracket: [(n1,h1),(n2,h2)] = ([n1,n2] + delta_h1(n2) - delta_h2(n1),
[h1,h2]). delta_X: A->[A,B], B->-[A,B], C->0; delta_Y: A->0, B->[B,C],
C->-[B,C] (design doc SS2).

rho (design doc SS3, degree 1): rho(A)=A+B+X, rho(B)=C, rho(C)=-A-B-C-X-Y,
rho(X)=-(A+B+C), rho(Y)=A. rho on higher degree is: substitute these degree-1
images into a basis element's OWN bracket tree and re-evaluate the bracket
IN t (i.e. via the full semidirect bracket above, since rho does not
preserve n -- design doc SS3 note).

j: x->T_1=X, y->T_2=Y -- i.e. j is literally the identity map from L_k's own
Lyndon-word structure (alphabet {x,y}) onto h_k's Lyndon-word structure
(alphabet {X,Y}), h-component only (n=0).

H_k := ker(1+theta) cap ker(1+tau+tau^2) subseteq L_k=Lie(x,y) (hexagon
homogeneous solution space; docs/notes/b_type_synthesis_design_v1_addendum_
edim56_prediction.md SS1). theta: x<->y. tau: x->y, y->-x-y.

S_k := H_k cap ker(nu_k . j), nu_k = sum_{i=0}^4 rho^i.

Implementation strategy (free Lie algebra via Lyndon words + standard
bracketing, NOT the ideal-quotient method): the compatibility path keeps
Lyndon trees, ambient associative-word expansions, and basis coordinates.
Its sparse coordinate conversion uses the unit-triangular leading-word
property of the standard Lyndon basis, with a residual-zero check.  The 112e
production S-map bypasses n-side coordinates completely and evaluates the
semidirect bracket directly on sparse ABC/XY associative-word dictionaries.

Two-prime cross-check (S-ED-3 discipline, matches search/certs/
edim56_20260806.json's own convention): all linear algebra done mod two
independent primes; results must agree, single-prime results are not
reported as exact.
"""
import itertools
import json
import hashlib
import sys

import numpy as np

PRIMES = [2147483647, 998244353]

# ===========================================================================
# Lyndon word combinatorics (brute force; the production path constructs only
# the two-letter h side, so degree 12 still scans just 2^12 words).
# ===========================================================================

def rotations(w):
    n = len(w)
    return [w[i:] + w[:i] for i in range(n)]


def is_lyndon(w):
    """w is Lyndon iff it is strictly smaller than every one of its proper
    rotations (equivalently: strictly smaller than every proper suffix, and
    aperiodic)."""
    for r in rotations(w)[1:]:
        if not (w < r):
            return False
    return True


def all_lyndon_words(alphabet_size, k):
    words = []
    for tpl in itertools.product(range(alphabet_size), repeat=k):
        if is_lyndon(tpl):
            words.append(tpl)
    return sorted(words)


def is_lyndon_and(w):
    return len(w) > 0 and is_lyndon(w)


def standard_factorization(w):
    """For a Lyndon word w of length>1: find the (unique) standard
    factorization w=uv with u,v both Lyndon and v the longest proper Lyndon
    suffix. Brute force over suffix lengths (degree<=6 here, cheap)."""
    n = len(w)
    best = None
    for split in range(1, n):
        u, v = w[:split], w[split:]
        if is_lyndon_and(u) and is_lyndon_and(v):
            # the standard factorization is the one with v as LONG as
            # possible (equivalently u as short as possible)
            if best is None or len(v) > len(best[1]):
                best = (u, v)
    if best is None:
        raise ValueError(f"no standard factorization found for {w!r}")
    return best


_tree_cache = {}


def bracket_tree_of_lyndon_word(w):
    """Returns a nested tuple: ('leaf', letter) or ('node', left_tree,
    right_tree, deg_left, deg_right). Memoized."""
    if w in _tree_cache:
        return _tree_cache[w]
    if len(w) == 1:
        t = ('leaf', w[0])
    else:
        u, v = standard_factorization(w)
        lt = bracket_tree_of_lyndon_word(u)
        rt = bracket_tree_of_lyndon_word(v)
        t = ('node', lt, rt, len(u), len(v), u, v)
    _tree_cache[w] = t
    return t


# ===========================================================================
# modular linear algebra (pure python, small matrices)
# ===========================================================================

def modinv(a, p):
    return pow(a % p, p - 2, p)


def rref_modp(mat, p):
    """mat: list of rows (lists of ints). Returns (rref_rows, pivot_cols)."""
    mat = [row[:] for row in mat]
    nrows = len(mat)
    ncols = len(mat[0]) if nrows else 0
    pivot_cols = []
    r = 0
    for c in range(ncols):
        piv = None
        for rr in range(r, nrows):
            if mat[rr][c] % p != 0:
                piv = rr
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = modinv(mat[r][c], p)
        mat[r] = [(x * inv) % p for x in mat[r]]
        for rr in range(nrows):
            if rr != r and mat[rr][c] % p != 0:
                factor = mat[rr][c]
                mat[rr] = [(mat[rr][cc] - factor * mat[r][cc]) % p for cc in range(ncols)]
        pivot_cols.append(c)
        r += 1
        if r == nrows:
            break
    return mat, pivot_cols


def rank_modp(mat, p):
    if not mat or not mat[0]:
        return 0
    _, pivots = rref_modp(mat, p)
    return len(pivots)


def solve_modp(M_cols, v, p):
    """M_cols: list of column vectors (each a list of length nrows) forming
    the basis matrix (nrows x ncols). v: target vector (length nrows).
    Returns coordinate vector c (length ncols) with M_cols @ c = v, assuming
    v truly lies in the column span (verified by caller)."""
    ncols = len(M_cols)
    nrows = len(v)
    # augmented matrix as ROWS: nrows x (ncols+1)
    aug = [[M_cols[c][r] for c in range(ncols)] + [v[r]] for r in range(nrows)]
    rref, pivots = rref_modp(aug, p)
    coord = [0] * ncols
    for i, pc in enumerate(pivots):
        if pc < ncols:
            coord[pc] = rref[i][ncols] % p
    return coord


def _mat_inv_modp_numpy(mat, p):
    """mat: numpy int64 array, n x n, invertible mod p. Returns inverse mod
    p via Gauss-Jordan with vectorized (outer-product) row elimination --
    needed for k=7,8 (n up to 840); the pure-python rref_modp above is too
    slow at that scale (used only for k<=6 elsewhere in this module)."""
    n = mat.shape[0]
    aug = np.concatenate([mat.astype(np.int64) % p, np.eye(n, dtype=np.int64)], axis=1)
    for col in range(n):
        nz = np.nonzero(aug[col:, col] % p != 0)[0]
        if len(nz) == 0:
            raise ValueError(f"_mat_inv_modp_numpy: singular matrix at column {col}")
        r = col + int(nz[0])
        if r != col:
            aug[[col, r]] = aug[[r, col]]
        inv = modinv(int(aug[col, col]) % p, p)
        aug[col, :] = (aug[col, :] * inv) % p
        colvals = aug[:, col].copy()
        colvals[col] = 0
        aug = (aug - np.outer(colvals, aug[col, :])) % p
    return aug[:, n:] % p


def mat_mul_modp_np(A, B, p):
    """Numpy int64 matmul mod p. SAFE ONLY when p*p*K < int64max (K = shared
    contraction dimension, i.e. A.shape[1]==B.shape[0]) -- caller's
    responsibility (see PRIMES_SMALL/ARBITRATION_PRIME choices in the k=7,8
    driver, all chosen with this margin in mind: p^2*840 well under 2^63).
    DO NOT use this for the large primes (2147483647/998244353) required by
    the k=9,10,11 task -- p^2 alone (~4.6e18) leaves almost no room for
    summing more than ~1 term before overflowing int64's ~9.22e18 ceiling.
    Use mat_mul_modp_np_safe below for those."""
    A = np.asarray(A, dtype=np.int64) % p
    B = np.asarray(B, dtype=np.int64) % p
    return (A @ B) % p


def _mat_mul_modp_np_safe_rank1(A, B, p):
    """Low-memory fallback used only if the limb-split int64 bound fails."""
    A = np.asarray(A, dtype=np.int64) % p
    B = np.asarray(B, dtype=np.int64) % p
    M, K = A.shape
    K2, N = B.shape
    assert K == K2
    acc = np.zeros((M, N), dtype=np.int64)
    for k in range(K):
        acc = (acc + np.outer(A[:, k], B[k, :])) % p
    return acc


def mat_mul_modp_np_safe(A, B, p):
    """Exact overflow-safe modular matmul, accelerated with two int64 limbs.

    A raw int64 ``A @ B`` is invalid for the large EDIM primes: two terms of
    size roughly ``p^2`` can already overflow.  Split every residue exactly
    as ``x = x0 + 2^15*x1`` and perform the four limb products with integer
    BLAS instead.  Each raw dot product is then bounded by

        K * max(2^15-1, floor((p-1)/2^15))^2.

    The EDIM range (p <= 2^31-1 and K <= 44,555 through degree 12) is below
    2^48, far inside int64.  Recombination is also below 2.4e18.  The bound
    is checked at runtime; an unexpectedly larger input uses the slower
    rank-1 implementation above rather than risking silent overflow.  No
    floating-point arithmetic is used anywhere in this routine.
    """
    A = np.asarray(A, dtype=np.int64) % p
    B = np.asarray(B, dtype=np.int64) % p
    M, K = A.shape
    K2, N = B.shape
    assert K == K2
    if K == 0:
        return np.zeros((M, N), dtype=np.int64)

    limb_bits = 15
    limb_base = 1 << limb_bits
    limb_mask = limb_base - 1
    high_max = (p - 1) >> limb_bits
    raw_bound = K * max(limb_mask, high_max) ** 2
    recombine_bound = ((p - 1) + limb_base * (p - 1)
                       + limb_base * limb_base * (p - 1))
    int64_max = np.iinfo(np.int64).max
    if raw_bound > int64_max or recombine_bound > int64_max:
        return _mat_mul_modp_np_safe_rank1(A, B, p)

    A0 = A & limb_mask
    A1 = A >> limb_bits
    B0 = B & limb_mask
    B1 = B >> limb_bits
    C00 = (A0 @ B0) % p
    C01 = ((A0 @ B1) % p + (A1 @ B0) % p) % p
    C11 = (A1 @ B1) % p
    return (C00 + limb_base * C01 + (limb_base * limb_base) * C11) % p


def mat_vec_modp_np_safe(A, v, p):
    """Exact large-prime-safe matrix-vector specialization."""
    v = np.asarray(v, dtype=np.int64).reshape((-1, 1))
    return mat_mul_modp_np_safe(A, v, p)[:, 0]


def mat_pow_modp_np(A, e, p):
    n = A.shape[0]
    R = np.eye(n, dtype=np.int64)
    base = A.copy()
    while e > 0:
        if e & 1:
            R = mat_mul_modp_np_safe(R, base, p)
        base = mat_mul_modp_np_safe(base, base, p)
        e >>= 1
    return R


def rank_modp_np(mat, p):
    """Exact rank over GF(p), using forward row elimination only."""
    M = np.array(mat, dtype=np.int64) % p
    nrows, ncols = M.shape
    if nrows == 0 or ncols == 0:
        return 0
    row = 0
    rank = 0
    for col in range(ncols):
        if row >= nrows:
            break
        nz = np.nonzero(M[row:, col] % p != 0)[0]
        if len(nz) == 0:
            continue
        r = row + int(nz[0])
        if r != row:
            M[[row, r]] = M[[r, row]]
        inv = modinv(int(M[row, col]) % p, p)
        M[row, col:] = (M[row, col:] * inv) % p
        if row + 1 < nrows:
            factors = M[row + 1:, col].copy()
            M[row + 1:, col:] = (M[row + 1:, col:]
                                  - np.outer(factors, M[row, col:])) % p
        rank += 1
        row += 1
    return rank


def nullspace_modp_np(mat, p):
    """Return a column basis for the right nullspace of ``mat`` over GF(p).

    The matrices here are the small theta/tau constraint blocks (at most a
    few hundred columns through k=12).  Full RREF is therefore inexpensive,
    and every row update is one scalar product followed immediately by mod
    p, so it has the same large-prime int64 safety as rank_modp_np.
    """
    M = np.array(mat, dtype=np.int64) % p
    nrows, ncols = M.shape
    row = 0
    pivot_cols = []
    for col in range(ncols):
        if row >= nrows:
            break
        nz = np.nonzero(M[row:, col] != 0)[0]
        if len(nz) == 0:
            continue
        r = row + int(nz[0])
        if r != row:
            M[[row, r]] = M[[r, row]]
        inv = modinv(int(M[row, col]), p)
        M[row, :] = (M[row, :] * inv) % p
        factors = M[:, col].copy()
        factors[row] = 0
        M = (M - np.outer(factors, M[row, :])) % p
        pivot_cols.append(col)
        row += 1

    pivot_set = set(pivot_cols)
    free_cols = [c for c in range(ncols) if c not in pivot_set]
    basis = np.zeros((ncols, len(free_cols)), dtype=np.int64)
    for j, free_col in enumerate(free_cols):
        basis[free_col, j] = 1
        for r, pivot_col in enumerate(pivot_cols):
            basis[pivot_col, j] = (-M[r, free_col]) % p

    # Fail closed: this is cheap at EDIM's h-dimensions and catches any
    # regression in the RREF/nullspace construction immediately.
    if basis.shape[1] and np.any(mat_mul_modp_np_safe(np.asarray(mat), basis, p)):
        raise ValueError("nullspace_modp_np verification FAILED")
    return basis


def sparse_column_space_basis_modp_np(mat, p):
    """Choose a light exact basis from the *original* columns of ``mat``.

    Columns are considered by increasing nnz count, then reduced against a
    sparse echelon dictionary over GF(p).  Returning original rather than
    RREF-generated columns materially reduces the fan-out when an H-basis is
    later distributed over ambient rho images.
    """
    original = np.asarray(mat, dtype=np.int64) % p
    nrows, ncols = original.shape
    order = sorted(range(ncols), key=lambda c: (int(np.count_nonzero(original[:, c])), c))
    pivots = {}
    selected = []
    for column in order:
        dense = original[:, column]
        vec = {int(row): int(dense[row]) for row in np.nonzero(dense)[0]}
        while vec:
            pivot = min(vec)
            old = pivots.get(pivot)
            if old is None:
                inv = modinv(vec[pivot], p)
                vec = {row: (value * inv) % p for row, value in vec.items() if value % p}
                pivots[pivot] = vec
                selected.append(column)
                break
            factor = vec[pivot]
            for row, value in old.items():
                new_value = (vec.get(row, 0) - factor * value) % p
                if new_value:
                    vec[row] = new_value
                else:
                    vec.pop(row, None)
    return original[:, selected]


# ===========================================================================
# free Lie algebra machinery for one alphabet (used for both n={A,B,C} and
# h={X,Y}); "plain" bracket = associative-word commutator, no semidirect
# mixing.
# ===========================================================================

def word_add(vecs, p):
    out = {}
    for vec in vecs:
        for w, c in vec.items():
            out[w] = (out.get(w, 0) + c) % p
    return {w: c for w, c in out.items() if c % p != 0}


def word_bracket(u, v, p):
    """Plain commutator on associative-word vectors (dict word-tuple:coeff)."""
    out = {}
    for w1, c1 in u.items():
        for w2, c2 in v.items():
            c = (c1 * c2) % p
            if c == 0:
                continue
            k1 = w1 + w2
            k2 = w2 + w1
            out[k1] = (out.get(k1, 0) + c) % p
            out[k2] = (out.get(k2, 0) - c) % p
    return {w: c for w, c in out.items() if c % p != 0}


def eval_plain_tree(tree, leaf_vecs, p, cache=None):
    """Evaluate a Lyndon bracket tree using PLAIN word_bracket, substituting
    leaf letter -> ambient vector (dict) via leaf_vecs."""
    cache_key = id(tree)
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    if tree[0] == 'leaf':
        result = dict(leaf_vecs[tree[1]])
    else:
        _, lt, rt, dl, dr, u, v = tree
        lv = eval_plain_tree(lt, leaf_vecs, p, cache)
        rv = eval_plain_tree(rt, leaf_vecs, p, cache)
        result = word_bracket(lv, rv, p)
    if cache is not None:
        cache[cache_key] = result
    return result


class SparseFillinExceeded(Exception):
    """Raised when sparse elimination's fill-in ratio exceeds the configured
    threshold -- per docs/notes/edim_sparse_solver_design_v1.md SS2.2:
    'SPARSE_FILLIN_EXCEEDED / STOP', NOT a silent fallback to the dense
    solver."""
    pass


def build_sparse_solver(basis, p, fillin_threshold=0.30, degree_label=""):
    """Build the exact unit-triangular solver for a standard Lyndon basis.

    For the standard bracketing ``[w]`` of a Lyndon word ``w``, its
    associative expansion is ``w`` with coefficient one plus words strictly
    larger than ``w`` in lexicographic order.  Since ``GradedLie`` stores the
    Lyndon words in that same order, the ambient-word/basis matrix already
    has a canonical unit-triangular pivot block.  Generic Markowitz
    Gauss-Jordan was therefore doing substantial work to rediscover a
    theorem-built pivot order and creating an inverse that is not needed.

    We check the triangular hypotheses for every column at runtime and fail
    closed if a caller ever supplies a different basis.  Coordinate solving
    then subtracts basis columns in pivot order; an empty final residual is
    an exact recombination check.  There is no fill-in and no dense ambient
    allocation.  ``fillin_threshold`` remains in the signature for backward
    API compatibility but is immaterial for this Lyndon-specific solver.
    """
    basis_dim = len(basis)
    if basis_dim == 0:
        return {"piv_rows": [], "pivot_coeff_inv": [], "basis": basis,
                "solver_kind": "lyndon_unit_triangular", "basis_dim": 0,
                "fillin_ratio": 0.0, "nnz_final": 0, "nnz_initial": 0, "max_nnz_seen": 0}
    piv_rows = []
    pivot_coeff_inv = []
    previous = None
    nnz_initial = 0
    for c, bvec in enumerate(basis):
        cleaned = [(w, coef % p) for w, coef in bvec.items() if coef % p]
        if not cleaned:
            raise ValueError(f"build_sparse_solver({degree_label}): zero basis column {c}")
        pivot = min(w for w, _ in cleaned)
        if previous is not None and pivot <= previous:
            raise ValueError(f"build_sparse_solver({degree_label}): Lyndon pivots are not "
                             f"strictly increasing at column {c}")
        coeff = bvec[pivot] % p
        if coeff == 0:
            raise ValueError(f"build_sparse_solver({degree_label}): zero pivot at column {c}")
        piv_rows.append(pivot)
        pivot_coeff_inv.append(modinv(coeff, p))
        previous = pivot
        nnz_initial += len(cleaned)

    return {"piv_rows": piv_rows, "pivot_coeff_inv": pivot_coeff_inv, "basis": basis,
            "solver_kind": "lyndon_unit_triangular", "basis_dim": basis_dim,
            "fillin_ratio": nnz_initial / max(1, basis_dim * basis_dim),
            "nnz_final": basis_dim, "nnz_initial": nnz_initial,
            "max_nnz_seen": nnz_initial}


def sparse_solve_coords(solver, vec, p):
    """Exact Lyndon triangular solve, with residual-zero span verification."""
    basis_dim = solver["basis_dim"]
    piv_rows = solver["piv_rows"]
    pivot_coeff_inv = solver["pivot_coeff_inv"]
    basis = solver["basis"]
    residual = {w: c % p for w, c in vec.items() if c % p}
    coord = [0] * basis_dim
    for j in range(basis_dim):
        c = (residual.get(piv_rows[j], 0) * pivot_coeff_inv[j]) % p
        if c == 0:
            continue
        coord[j] = c
        for w, value in basis[j].items():
            new_value = (residual.get(w, 0) - c * value) % p
            if new_value:
                residual[w] = new_value
            else:
                residual.pop(w, None)
    if residual:
        smallest = min(residual)
        raise ValueError("sparse_solve_coords verification FAILED: target is not in the "
                         f"Lyndon span (smallest residual word={smallest!r})")
    return coord


class GradedLie:
    """One free Lie algebra Lie(alphabet), Lyndon basis per degree, with
    ambient<->coordinate conversion mod p. p is fixed at construction."""

    def __init__(self, alphabet_size, kmax, p, sparse_degrees=None, fillin_threshold=0.30):
        """sparse_degrees: set/list of degrees at which coords_of_ambient
        should use the sparse solver (build_sparse_solver/sparse_solve_
        coords, docs/notes/edim_sparse_solver_design_v1.md) instead of the
        dense numpy solver (_get_solver). Degrees not listed use the dense
        path unchanged (so k<=10 callers that never pass this argument are
        byte-for-byte unaffected -- this is an ADDITIVE change, not a
        replacement, per the design spec's own regression-gate plan: k=9,10
        must agree between dense and sparse before k=11 is trusted)."""
        self.alphabet_size = alphabet_size
        self.kmax = kmax
        self.p = p
        self.sparse_degrees = set(sparse_degrees or [])
        self.fillin_threshold = fillin_threshold
        self._sparse_solver_cache = {}
        self.words = {}       # degree -> list of Lyndon words
        self.trees = {}       # degree -> list of bracket trees
        self.ambient = {}     # degree -> list of ambient vectors (dict)
        self.dim = {}         # degree -> int
        self.word_index = {}  # degree -> {word: index}
        for k in range(1, kmax + 1):
            ws = all_lyndon_words(alphabet_size, k)
            self.words[k] = ws
            self.word_index[k] = {w: i for i, w in enumerate(ws)}
            trees = [bracket_tree_of_lyndon_word(w) for w in ws]
            self.trees[k] = trees
            identity_leaf = {i: {(i,): 1 % p} for i in range(alphabet_size)}
            if k == 1:
                plain_cache = {}
            self.ambient[k] = [eval_plain_tree(t, identity_leaf, p, plain_cache) for t in trees]
            self.dim[k] = len(ws)

    def _get_solver(self, degree):
        """Build (once, cached) a fast numpy-based solver for degree `degree`:
        picks basis_dim independent AMBIENT-WORD pivot rows out of the full
        alphabet_size^degree word space (dense, since degree<=8 here keeps
        this at most 3^8=6561 rows), inverts the basis_dim x basis_dim pivot
        submatrix mod p. Subsequent coords_of_ambient calls at this degree
        then cost O(basis_dim^2) instead of a fresh O(ambient_dim*basis_dim^2)
        elimination every time -- this is the perf fix needed for k=7,8
        (k<=6 was fine without it, k=7/8 is not: thousands of conversion
        calls per run)."""
        if not hasattr(self, '_solver_cache'):
            self._solver_cache = {}
        if degree in self._solver_cache:
            return self._solver_cache[degree]
        basis = self.ambient[degree]
        basis_dim = len(basis)
        p = self.p
        if basis_dim == 0:
            self._solver_cache[degree] = None
            return None
        all_words = [tuple(w) for w in itertools.product(range(self.alphabet_size), repeat=degree)]
        word_pos = {w: i for i, w in enumerate(all_words)}
        ambient_dim = len(all_words)
        M = np.zeros((ambient_dim, basis_dim), dtype=np.int64)
        for c, bvec in enumerate(basis):
            for w, coef in bvec.items():
                M[word_pos[w], c] = coef % p
        # Gaussian elimination (numpy-vectorized row ops) to find basis_dim
        # independent pivot ROWS (ambient word positions) and reduce M to
        # identity on those rows (RREF), giving the pivot submatrix inverse
        # directly as the corresponding rows of the reduced matrix restricted
        # to... simplest robust route: track an explicit identity-augmented
        # elimination is unnecessary here -- instead solve for the inverse of
        # the basis_dim x basis_dim pivot submatrix via standard augmented
        # elimination on JUST those rows once found.
        Mwork = M.copy()
        piv_rows = []
        row_available = np.ones(ambient_dim, dtype=bool)
        for col in range(basis_dim):
            nz = np.nonzero((Mwork[:, col] % p != 0) & row_available)[0]
            if len(nz) == 0:
                raise ValueError(f"degree {degree}: basis matrix column {col} has no available "
                                  f"pivot row -- basis is not full column rank (should not happen)")
            r = int(nz[0])
            piv_rows.append(r)
            row_available[r] = False
            inv = modinv(int(Mwork[r, col]) % p, p)
            Mwork[r, :] = (Mwork[r, :] * inv) % p
            colvals = Mwork[:, col].copy()
            colvals[r] = 0
            # eliminate this column from ALL other rows (vectorized outer-product update)
            Mwork = (Mwork - np.outer(colvals, Mwork[r, :])) % p
        pivot_sub = M[piv_rows, :] % p  # basis_dim x basis_dim, from ORIGINAL M
        pivot_sub_inv = _mat_inv_modp_numpy(pivot_sub, p)
        solver = {"piv_rows": piv_rows, "pivot_sub_inv": pivot_sub_inv, "word_pos": word_pos,
                  "all_words": all_words, "basis_dim": basis_dim, "M": M}
        self._solver_cache[degree] = solver
        return solver

    def coords_of_ambient(self, degree, vec):
        """Express ambient vector (dict, degree `degree`) in this degree's
        Lyndon basis coordinates. Returns list length self.dim[degree]."""
        basis = self.ambient[degree]
        ncols = len(basis)
        if ncols == 0:
            assert not vec, f"expected zero vector, got {vec} at degree {degree} with empty basis"
            return []
        p = self.p
        if degree in self.sparse_degrees:
            return self._coords_of_ambient_sparse(degree, vec)
        solver = self._get_solver(degree)
        v_piv = np.array([vec.get(solver["all_words"][r], 0) % p for r in solver["piv_rows"]], dtype=np.int64)
        # p up to ~2^31 (large-prime task, 裁定658) means a raw numpy `@`
        # here silently overflows int64 (sum of >1 terms each ~(p-1)^2) --
        # use the overflow-safe mat-vec (see mat_vec_modp_np_safe docstring).
        coord = mat_vec_modp_np_safe(solver["pivot_sub_inv"], v_piv, p)
        coord = [int(x) for x in coord]
        # verify (correctness-critical -- keep it; same overflow concern for
        # large p, use the safe mat-vec here too)
        recomb = mat_vec_modp_np_safe(solver["M"], np.array(coord, dtype=np.int64), p)
        target = np.array([vec.get(w, 0) % p for w in solver["all_words"]], dtype=np.int64)
        if not np.array_equal(recomb, target):
            raise ValueError(f"coords_of_ambient verification FAILED at degree {degree}: "
                              f"recombination mismatch (basis may not span the target vector)")
        return coord

    def _coords_of_ambient_sparse(self, degree, vec):
        """Sparse-solver path (docs/notes/edim_sparse_solver_design_v1.md):
        no ambient_dim-sized dense array is ever built. Verification is kept
        (same fail-closed discipline as the dense path), done sparsely
        (only touches the nonzero entries of vec and of the recombination,
        not the full ambient_dim^alphabet_size^degree space)."""
        p = self.p
        if degree not in self._sparse_solver_cache:
            self._sparse_solver_cache[degree] = build_sparse_solver(
                self.ambient[degree], p, fillin_threshold=self.fillin_threshold,
                degree_label=f"alphabet{self.alphabet_size}_k{degree}")
        solver = self._sparse_solver_cache[degree]
        coord = sparse_solve_coords(solver, vec, p)
        # sparse_solve_coords maintains target - sum(coord[j]*basis[j]) as
        # an exact sparse residual and refuses to return unless it is empty;
        # that is the same full recombination check without a second pass.
        return coord

    def coords_to_ambient(self, degree, coords):
        basis = self.ambient[degree]
        p = self.p
        out = {}
        for i, c in enumerate(coords):
            c %= p
            if c == 0:
                continue
            for w, value in basis[i].items():
                new_value = (out.get(w, 0) + c * value) % p
                if new_value:
                    out[w] = new_value
                else:
                    out.pop(w, None)
        return out


def scale_vec(vec, c, p):
    c = c % p
    if c == 0:
        return {}
    return {w: (cc * c) % p for w, cc in vec.items()}


# ===========================================================================
# delta table: D[d_h][d_n] = dim_h[d_h] x dim_n[d_n] matrix of coordinate
# vectors (each length dim_n[d_h+d_n]) -- delta_{h_basis_i}(n_basis_j).
# ===========================================================================

def _delta_base_table(p):
    """delta_X on n_1 basis (A=0,B=1,C=2): A->[A,B], B->-[A,B], C->0.
    delta_Y on n_1 basis: A->0, B->[B,C], C->-[B,C]. [A,B]/[B,C] computed
    via the REAL bracket commutator (AB-BA), not a hand-typed single word --
    a single word like {(0,1):1} would be WRONG (that is just the tensor
    monomial AB, not the Lie bracket [A,B]=AB-BA)."""
    eA, eB, eC = {(0,): 1 % p}, {(1,): 1 % p}, {(2,): 1 % p}
    AB = word_bracket(eA, eB, p)
    BC = word_bracket(eB, eC, p)
    neg_AB = scale_vec(AB, -1, p)
    neg_BC = scale_vec(BC, -1, p)
    return {
        ('X', 'A'): AB, ('X', 'B'): neg_AB, ('X', 'C'): {},
        ('Y', 'A'): {}, ('Y', 'B'): BC, ('Y', 'C'): neg_BC,
    }


def witt_dimension(alphabet_size, degree):
    """Witt dimension of the degree-``degree`` free Lie piece (integer)."""
    def mobius(n):
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


def delta_letter_on_nambient(letter, n_vec, p, base_table=None):
    """Apply delta_X/delta_Y directly to an associative ABC polynomial.

    This is the exact Leibniz extension of the three generator images in
    _delta_base_table.  Keeping the production rho-orbit evaluation in the
    ambient tensor algebra removes all intermediate Lyndon coordinate solves
    and the precomputed delta table; conversion is unnecessary for rank by
    injectivity of the standard free-Lie embedding.
    """
    if not n_vec:
        return {}
    letter_index = letter if isinstance(letter, int) else 'XY'.index(letter)
    if letter_index == 0:
        first, second = 0, 1
    else:
        first, second = 1, 2
    out = {}
    for word, coeff in n_vec.items():
        coeff %= p
        if coeff == 0:
            continue
        for pos, generator in enumerate(word):
            if generator == first:
                signed_coeff = coeff
            elif generator == second:
                signed_coeff = -coeff
            else:
                continue
            prefix = word[:pos]
            suffix = word[pos + 1:]
            word_pos = prefix + (first, second) + suffix
            word_neg = prefix + (second, first) + suffix
            value = (out.get(word_pos, 0) + signed_coeff) % p
            if value:
                out[word_pos] = value
            else:
                out.pop(word_pos, None)
            value = (out.get(word_neg, 0) - signed_coeff) % p
            if value:
                out[word_neg] = value
            else:
                out.pop(word_neg, None)
    return out


def delta_h_on_nambient(h_vec, n_vec, p, base_table=None):
    """Apply an ambient XY Lie polynomial as a derivation to ``n_vec``.

    The universal-enveloping word X_1...X_r acts as the composition
    delta_X1 o ... o delta_Xr, hence letters are applied right-to-left.
    A per-call suffix cache shares the repeated compositions among the
    associative words in a bracket expansion.
    """
    if not h_vec or not n_vec:
        return {}
    if base_table is None:
        base_table = _delta_base_table(p)
    action_cache = {(): n_vec}

    def apply_word(word):
        if word in action_cache:
            return action_cache[word]
        inner = apply_word(word[1:])
        value = delta_letter_on_nambient(word[0], inner, p, base_table)
        action_cache[word] = value
        return value

    out = {}
    for h_word, h_coeff in h_vec.items():
        h_coeff %= p
        if h_coeff == 0:
            continue
        acted = apply_word(h_word)
        for n_word, value in acted.items():
            new_value = (out.get(n_word, 0) + h_coeff * value) % p
            if new_value:
                out[n_word] = new_value
            else:
                out.pop(n_word, None)
    return out


def delta_hexpr_on_nambient(h_expr, n_vec, p, base_table=None, cache=None):
    """Apply a bracket-DAG h expression without expanding it into XY words."""
    if h_expr is None or not n_vec:
        return {}
    cache_key = (id(h_expr), id(n_vec))
    if cache is not None and cache_key in cache:
        saved_expr, saved_vec, result = cache[cache_key]
        if saved_expr is h_expr and saved_vec is n_vec:
            return result
    if h_expr[0] == 'lin':
        dx = delta_letter_on_nambient(0, n_vec, p, base_table) if h_expr[1] else {}
        dy = delta_letter_on_nambient(1, n_vec, p, base_table) if h_expr[2] else {}
        result = word_add([scale_vec(dx, h_expr[1], p),
                           scale_vec(dy, h_expr[2], p)], p)
    else:
        _, left, right = h_expr
        step_right = delta_hexpr_on_nambient(right, n_vec, p, base_table, cache)
        left_then = delta_hexpr_on_nambient(left, step_right, p, base_table, cache)
        step_left = delta_hexpr_on_nambient(left, n_vec, p, base_table, cache)
        right_then = delta_hexpr_on_nambient(right, step_left, p, base_table, cache)
        result = word_add([left_then, scale_vec(right_then, -1, p)], p)
    if cache is not None:
        # Retaining both input objects makes the id-based key collision-safe.
        cache[cache_key] = (h_expr, n_vec, result)
    return result


def t_bracket_ambient(e1, e2, p, base_table=None, action_cache=None):
    """Semidirect bracket entirely in the two ambient tensor algebras."""
    n1, h1, h_expr1, d1 = e1
    n2, h2, h_expr2, d2 = e2
    if base_table is None:
        base_table = _delta_base_table(p)
    nn = word_bracket(n1, n2, p) if n1 and n2 else {}
    dh1n2 = delta_hexpr_on_nambient(h_expr1, n2, p, base_table, action_cache)
    dh2n1 = delta_hexpr_on_nambient(h_expr2, n1, p, base_table, action_cache)
    n_out = word_add([nn, dh1n2, scale_vec(dh2n1, -1, p)], p)
    h_out = word_bracket(h1, h2, p) if h1 and h2 else {}
    h_expr_out = ('bracket', h_expr1, h_expr2) if h_out else None
    return n_out, h_out, h_expr_out, d1 + d2


def eval_tree_in_t_ambient(tree, leaf_images, p, cache=None, base_table=None,
                           action_cache=None, cache_result=True):
    """Evaluate a Lyndon tree in ambient semidirect form, with subtree memo.

    ``cache_result=False`` is used for a degree-k root: its proper subtrees
    are still memoized, but the nearly dense root dictionary is released
    after it has been accumulated into the restricted nu columns.  This
    prevents a cross-degree resident-memory staircase at k=11/12.
    """
    cache_key = id(tree)
    if cache_result and cache is not None and cache_key in cache:
        return cache[cache_key]
    if tree[0] == 'leaf':
        result = leaf_images[tree[1]]
    else:
        _, lt, rt, dl, dr, u, v = tree
        left = eval_tree_in_t_ambient(
            lt, leaf_images, p, cache, base_table, action_cache, cache_result=True)
        right = eval_tree_in_t_ambient(
            rt, leaf_images, p, cache, base_table, action_cache, cache_result=True)
        result = t_bracket_ambient(left, right, p, base_table, action_cache)
    if cache_result and cache is not None:
        cache[cache_key] = result
    return result


def _rho_power_h_leaf_images_ambient(p):
    """Ambient images of X,Y under rho^i, i=0,...,4 (degree one)."""
    letters = ['A', 'B', 'C', 'X', 'Y']
    rho = [[0] * 5 for _ in range(5)]
    for col, letter in enumerate(letters):
        n_coord, h_coord = RHO_DEG1[letter]
        column = n_coord + h_coord
        for row, value in enumerate(column):
            rho[row][col] = value % p

    current = ([0, 0, 0, 1, 0], [0, 0, 0, 0, 1])
    powers = []
    for _ in range(5):
        images = {}
        for leaf, vector in enumerate(current):
            n_vec = {(i,): vector[i] % p for i in range(3) if vector[i] % p}
            h_vec = {(i,): vector[3 + i] % p for i in range(2) if vector[3 + i] % p}
            h_expr = ('lin', vector[3] % p, vector[4] % p) if h_vec else None
            images[leaf] = (n_vec, h_vec, h_expr, 1)
        powers.append(images)
        next_vectors = []
        for vector in current:
            next_vectors.append([
                sum(rho[row][col] * vector[col] for col in range(5)) % p
                for row in range(5)
            ])
        current = tuple(next_vectors)

    # The design's degree-one rho^5=id check is repeated here because these
    # powers drive the optimized production path.
    expected = ([0, 0, 0, 1, 0], [0, 0, 0, 0, 1])
    for got, want in zip(current, expected):
        if [x % p for x in got] != want:
            raise ValueError("rho^5 degree-one verification FAILED")
    return powers


def rank_sparse_vectors_modp(vectors, p):
    """Exact rank of sparse column vectors (dict row-key -> coefficient)."""
    pivots = {}
    for original in vectors:
        vec = {key: value % p for key, value in original.items() if value % p}
        while vec:
            pivot = min(vec)
            old = pivots.get(pivot)
            if old is None:
                inv = modinv(vec[pivot], p)
                vec = {key: (value * inv) % p for key, value in vec.items() if value % p}
                pivots[pivot] = vec
                break
            factor = vec[pivot]
            for key, value in old.items():
                new_value = (vec.get(key, 0) - factor * value) % p
                if new_value:
                    vec[key] = new_value
                else:
                    vec.pop(key, None)
    return len(pivots)


def rank_nu_j_on_subspace_ambient(k, h_alg, subspace_basis, p):
    """Rank of nu_k o j restricted to a supplied h_k column subspace.

    Only the required columns are constructed.  Each rho^i is evaluated by
    substituting its degree-one X,Y images into the h Lyndon trees, directly
    in the ambient semidirect algebra.  The resulting n/h associative words
    are tagged into a disjoint sparse row space.  The standard embeddings
    Lie(A,B,C)->T(ABC) and Lie(X,Y)->T(XY) are injective, so sparse ambient
    rank is exactly the desired coordinate rank (PBW/free-Lie embedding).
    """
    subspace_basis = np.asarray(subspace_basis, dtype=np.int64) % p
    dim_h = h_alg.dim[k]
    if subspace_basis.shape[0] != dim_h:
        raise ValueError("rank_nu_j_on_subspace_ambient: wrong subspace row dimension")
    subspace_dim = subspace_basis.shape[1]
    if subspace_dim == 0:
        return 0

    state = getattr(h_alg, "_nu_ambient_state", None)
    if state is None or state["p"] != p:
        state = {
            "p": p,
            "leaf_images": _rho_power_h_leaf_images_ambient(p),
            "tree_caches": [dict() for _ in range(5)],
            "base_table": _delta_base_table(p),
        }
        h_alg._nu_ambient_state = state

    restricted = [dict() for _ in range(subspace_dim)]
    for basis_index, tree in enumerate(h_alg.trees[k]):
        coefficients = subspace_basis[basis_index, :]
        nonzero_columns = np.nonzero(coefficients)[0]
        if len(nonzero_columns) == 0:
            continue
        nu_n = {}
        nu_h = {}
        for power in range(5):
            # Derivation intermediates are useful only while evaluating this
            # one new tree.  Keeping them in the cross-degree state caused a
            # large resident-memory staircase at k=10/11 with no meaningful
            # cross-root hit rate; retain only the much smaller tree results.
            action_cache = {}
            n_part, h_part, h_expr, degree = eval_tree_in_t_ambient(
                tree, state["leaf_images"][power], p,
                cache=state["tree_caches"][power], base_table=state["base_table"],
                action_cache=action_cache, cache_result=False)
            if degree != k:
                raise ValueError("ambient rho evaluation returned wrong degree")
            nu_n = word_add([nu_n, n_part], p)
            nu_h = word_add([nu_h, h_part], p)

        for column in nonzero_columns:
            scalar = int(coefficients[column])
            target = restricted[int(column)]
            for word, value in nu_n.items():
                key = (0,) + word
                new_value = (target.get(key, 0) + scalar * value) % p
                if new_value:
                    target[key] = new_value
                else:
                    target.pop(key, None)
            for word, value in nu_h.items():
                key = (1,) + word
                new_value = (target.get(key, 0) + scalar * value) % p
                if new_value:
                    target[key] = new_value
                else:
                    target.pop(key, None)

    return rank_sparse_vectors_modp(restricted, p)


def build_delta_table(n_alg: GradedLie, h_alg: GradedLie, kmax, p):
    """D[d_h][d_n] -> list-of-lists: D[d_h][d_n][i][j] = coord vector
    (length n_alg.dim[d_h+d_n]) for delta_{h_basis_i}(n_basis_j)."""
    D = {}
    letters_h1 = ['X', 'Y']  # h_1 basis order must match all_lyndon_words(2,1) = [(0,),(1,)]
    assert h_alg.words[1] == [(0,), (1,)]

    # ---- D[1][d_n] for d_n = 1..kmax-1 ----
    D[1] = {}
    for d_n in range(1, kmax):
        d_out = 1 + d_n
        rows = []
        for hi_letter in letters_h1:  # X then Y, matches h basis order
            row = []
            for j, n_tree in enumerate(n_alg.trees[d_n]):
                amb = delta_leaf_on_ntree(hi_letter, n_tree, n_alg, D, p)
                coord = n_alg.coords_of_ambient(d_out, amb)
                row.append(coord)
            rows.append(row)
        D[1][d_n] = rows

    # ---- D[d_h][d_n] for d_h = 2..kmax-1, via commutator of derivations ----
    for d_h in range(2, kmax):
        D[d_h] = {}
        h_trees = h_alg.trees[d_h]
        for d_n in range(1, kmax - d_h + 1):
            d_out = d_h + d_n
            if d_out > kmax:
                continue
            rows = []
            for hi_tree in h_trees:
                row = []
                for j in range(n_alg.dim[d_n]):
                    e_j = [1 if jj == j else 0 for jj in range(n_alg.dim[d_n])]
                    val_coord = delta_of_htree_on_ncoord(hi_tree, d_n, e_j, n_alg, h_alg, D, p)
                    row.append(val_coord)
                rows.append(row)
            D[d_h][d_n] = rows
    return D


def delta_leaf_on_ntree(hi_letter, n_tree, n_alg: GradedLie, D, p, base_table=None):
    """delta_{hi_letter} (hi_letter in {'X','Y'}) applied to a SPECIFIC
    n-Lyndon-tree, via Leibniz recursion, base case = _delta_base_table(p).
    Returns an AMBIENT vector (degree = tree's degree + 1)."""
    if base_table is None:
        base_table = _delta_base_table(p)
    if n_tree[0] == 'leaf':
        letter = 'ABC'[n_tree[1]]
        return dict(base_table[(hi_letter, letter)])
    _, lt, rt, dl, dr, u, v = n_tree
    lv_amb = eval_plain_tree(lt, {i: {(i,): 1 % p} for i in range(3)}, p)
    rv_amb = eval_plain_tree(rt, {i: {(i,): 1 % p} for i in range(3)}, p)
    dl_amb = delta_leaf_on_ntree(hi_letter, lt, n_alg, D, p, base_table)
    dr_amb = delta_leaf_on_ntree(hi_letter, rt, n_alg, D, p, base_table)
    term1 = word_bracket(dl_amb, rv_amb, p)
    term2 = word_bracket(lv_amb, dr_amb, p)
    return word_add([term1, term2], p)


def delta_of_htree_on_ncoord(hi_tree, d_n, n_coord, n_alg: GradedLie, h_alg: GradedLie, D, p):
    """delta_{hi_tree} applied to an n-element given in COORDINATES (degree
    d_n), where hi_tree is a bracket tree over {X,Y} of degree d_h. Returns
    coordinate vector at degree d_h + d_n. Uses D[smaller][*] (already
    built) recursively for internal h-nodes."""
    if hi_tree[0] == 'leaf':
        letter = 'XY'[hi_tree[1]]
        row_idx = 0 if letter == 'X' else 1
        rows = D[1][d_n]
        out = [0] * n_alg.dim[d_n + 1]
        for j, c in enumerate(n_coord):
            if c % p == 0:
                continue
            vec = rows[row_idx][j]
            for k in range(len(out)):
                out[k] = (out[k] + c * vec[k]) % p
        return out
    _, lt, rt, dl, dr, u, v = hi_tree
    # delta_{[h1,h2]}(n) = delta_h1(delta_h2(n)) - delta_h2(delta_h1(n))
    step_r = delta_of_htree_on_ncoord(rt, d_n, n_coord, n_alg, h_alg, D, p)
    step_l_then = delta_of_htree_on_ncoord(lt, d_n + dr, step_r, n_alg, h_alg, D, p)
    step_l = delta_of_htree_on_ncoord(lt, d_n, n_coord, n_alg, h_alg, D, p)
    step_r_then = delta_of_htree_on_ncoord(rt, d_n + dl, step_l, n_alg, h_alg, D, p)
    out = [(step_l_then[k] - step_r_then[k]) % p for k in range(len(step_l_then))]
    return out


def delta_apply(h_coord, d_h, n_coord, d_n, D, n_alg, p):
    """General delta_h(n) for h given in H_{d_h} coords, n given in
    N_{d_n} coords. Returns coord vector at degree d_h+d_n."""
    d_out = d_h + d_n
    out = [0] * n_alg.dim[d_out]
    rows = D[d_h][d_n]
    for i, hc in enumerate(h_coord):
        if hc % p == 0:
            continue
        for j, nc in enumerate(n_coord):
            if nc % p == 0:
                continue
            vec = rows[i][j]
            coeff = (hc * nc) % p
            for k in range(len(out)):
                out[k] = (out[k] + coeff * vec[k]) % p
    return out


# ===========================================================================
# t-element (n_coord,h_coord,degree) + semidirect bracket
# ===========================================================================

def t_bracket(e1, e2, n_alg: GradedLie, h_alg: GradedLie, D, p):
    (n1, h1, d1) = e1
    (n2, h2, d2) = e2
    d_out = d1 + d2
    # [n1,n2]: plain bracket in n, via ambient round-trip
    n1_amb = n_alg.coords_to_ambient(d1, n1) if any(c % p for c in n1) else {}
    n2_amb = n_alg.coords_to_ambient(d2, n2) if any(c % p for c in n2) else {}
    nn_amb = word_bracket(n1_amb, n2_amb, p)
    nn_coord = n_alg.coords_of_ambient(d_out, nn_amb) if nn_amb else [0] * n_alg.dim[d_out]
    # delta_h1(n2), delta_h2(n1)
    dh1n2 = delta_apply(h1, d1, n2, d2, D, n_alg, p) if any(c % p for c in h1) and any(c % p for c in n2) \
        else [0] * n_alg.dim[d_out]
    dh2n1 = delta_apply(h2, d2, n1, d1, D, n_alg, p) if any(c % p for c in h2) and any(c % p for c in n1) \
        else [0] * n_alg.dim[d_out]
    n_out = [(nn_coord[k] + dh1n2[k] - dh2n1[k]) % p for k in range(n_alg.dim[d_out])]
    # [h1,h2]: plain bracket in h
    h1_amb = h_alg.coords_to_ambient(d1, h1) if any(c % p for c in h1) else {}
    h2_amb = h_alg.coords_to_ambient(d2, h2) if any(c % p for c in h2) else {}
    hh_amb = word_bracket(h1_amb, h2_amb, p)
    hh_coord = h_alg.coords_of_ambient(d_out, hh_amb) if hh_amb else [0] * h_alg.dim[d_out]
    return (n_out, hh_coord, d_out)


def zero_t(n_alg, h_alg, d):
    return ([0] * n_alg.dim.get(d, 0), [0] * h_alg.dim.get(d, 0), d)


def add_t(e1, e2, p):
    (n1, h1, d1) = e1
    (n2, h2, d2) = e2
    assert d1 == d2
    return ([(a + b) % p for a, b in zip(n1, n2)], [(a + b) % p for a, b in zip(h1, h2)], d1)


def scale_t(e, c, p):
    n, h, d = e
    c = c % p
    return ([(x * c) % p for x in n], [(x * c) % p for x in h], d)


RHO_DEG1 = {
    # rho(A) = A+B+X ; rho(B) = C ; rho(C) = -A-B-C-X-Y
    # rho(X) = -(A+B+C) ; rho(Y) = A
    # represented as (n_coord in n_1 basis [A,B,C], h_coord in h_1 basis [X,Y])
    'A': ([1, 1, 0], [1, 0]),
    'B': ([0, 0, 1], [0, 0]),
    'C': ([-1, -1, -1], [-1, -1]),
    'X': ([-1, -1, -1], [0, 0]),
    'Y': ([1, 0, 0], [0, 0]),
}


def eval_tree_in_t(tree, leaf_images, n_alg, h_alg, D, p):
    """Evaluate a bracket tree (over EITHER alphabet -- leaves are letter
    indices into whatever alphabet the tree was built over) via rho-style
    substitution into t, using the FULL semidirect bracket."""
    if tree[0] == 'leaf':
        return leaf_images[tree[1]]
    _, lt, rt, dl, dr, u, v = tree
    lv = eval_tree_in_t(lt, leaf_images, n_alg, h_alg, D, p)
    rv = eval_tree_in_t(rt, leaf_images, n_alg, h_alg, D, p)
    return t_bracket(lv, rv, n_alg, h_alg, D, p)


def rho_deg1_images(alphabet, p):
    """alphabet: 'n' (letters A,B,C -> leaf 0,1,2) or 'h' (letters X,Y ->
    leaf 0,1). Returns leaf_images dict for eval_tree_in_t, mod p."""
    letters = ['A', 'B', 'C'] if alphabet == 'n' else ['X', 'Y']
    out = {}
    for i, L in enumerate(letters):
        nco, hco = RHO_DEG1[L]
        out[i] = ([x % p for x in nco], [x % p for x in hco], 1)
    return out


def build_rho_matrix(k, n_alg: GradedLie, h_alg: GradedLie, D, p):
    """Returns rho as a (dim_t_k x dim_t_k) matrix over GF(p), in the basis
    [n_alg basis of degree k (dim n_k)] ++ [h_alg basis of degree k (dim
    h_k)]. Column j = image of basis element j, as a t_k coordinate vector
    (n-part ++ h-part)."""
    dim_n = n_alg.dim[k]
    dim_h = h_alg.dim[k]
    dim_t = dim_n + dim_h
    cols = []
    leaf_images_n = rho_deg1_images('n', p)
    for tree in n_alg.trees[k]:
        n_out, h_out, d_out = eval_tree_in_t(tree, leaf_images_n, n_alg, h_alg, D, p)
        assert d_out == k
        cols.append(n_out + h_out)
    leaf_images_h = rho_deg1_images('h', p)
    for tree in h_alg.trees[k]:
        n_out, h_out, d_out = eval_tree_in_t(tree, leaf_images_h, n_alg, h_alg, D, p)
        assert d_out == k
        cols.append(n_out + h_out)
    # matrix rows x cols, rows=dim_t (component index), cols=dim_t (basis index)
    M = [[cols[c][r] % p for c in range(dim_t)] for r in range(dim_t)]
    return M, dim_n, dim_h


def mat_mul_modp(A, B, p):
    n = len(A)
    m = len(B[0])
    kk = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        for l in range(kk):
            a = Ai[l]
            if a % p == 0:
                continue
            Bl = B[l]
            Ci = C[i]
            for j in range(m):
                Ci[j] = (Ci[j] + a * Bl[j]) % p
    return C


def identity_modp(n, p):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def mat_add_modp(A, B, p):
    return [[(A[i][j] + B[i][j]) % p for j in range(len(A[0]))] for i in range(len(A))]


def mat_pow_modp(A, e, p):
    n = len(A)
    R = identity_modp(n, p)
    base = A
    while e > 0:
        if e & 1:
            R = mat_mul_modp(R, base, p)
        base = mat_mul_modp(base, base, p)
        e >>= 1
    return R


# ===========================================================================
# theta, tau, H_k on L_k = h_alg (alphabet {x,y}, reusing h_alg's plain
# 2-letter Lie machinery -- theta/tau stay purely within this Lie algebra).
# ===========================================================================

def build_theta_tau_matrix(k, h_alg: GradedLie, kind, p):
    """kind: 'theta' (x<->y) or 'tau' (x->y, y->-x-y)."""
    dim_h = h_alg.dim[k]
    if kind == 'theta':
        leaf_images = {0: {(1,): 1 % p}, 1: {(0,): 1 % p}}
    else:
        leaf_images = {0: {(1,): 1 % p}, 1: {(0,): (p - 1) % p, (1,): (p - 1) % p}}
    cols = []
    for tree in h_alg.trees[k]:
        amb = eval_plain_tree(tree, leaf_images, p)
        coord = h_alg.coords_of_ambient(k, amb) if amb else [0] * dim_h
        cols.append(coord)
    M = [[cols[c][r] % p for c in range(dim_h)] for r in range(dim_h)]
    return M
