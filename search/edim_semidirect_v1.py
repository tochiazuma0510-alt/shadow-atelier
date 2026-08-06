#!/usr/bin/env python3
"""
edim_semidirect_v1.py -- 【EDIM-GAP-1】semidirect model implementation.

Spec (verbatim authority): docs/notes/edim_semidirect_model_design_v1.md.
Commissioned: 裁定646 (via 司令塔, this session), implementer scope = data
structures + bracket formula + delta_X/delta_Y recursion + rho bracket-tree
re-evaluation + calibration C-1..C-3, THEN STOP AND REPORT at C-4 (C-4 must
match search/certs/edim56_20260806.json exactly -- lifeline check, per
instruction). k=7+ is NOT run by this pass.

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
bracketing, NOT the ideal-quotient method): every graded piece is
represented BOTH as (a) a basis of Lyndon bracket-trees (explicit nested
tuples, needed for the delta/rho recursions per design doc SS5.1) and (b) a
basis-coordinate vector space, with conversion via a one-time linear solve
per Lyndon basis (Gaussian elimination mod p) expressing each basis
element's "plain embedding as an associative word" in terms of that same
basis (trivially the identity by construction) and, more importantly,
expressing arbitrary computed ambient vectors (e.g. delta_X(A)=[A,B]) in
basis coordinates.

Two-prime cross-check (S-ED-3 discipline, matches search/certs/
edim56_20260806.json's own convention): all linear algebra done mod two
independent primes; results must agree, single-prime results are not
reported as exact.
"""
import itertools
import json
import hashlib
import sys

PRIMES = [2147483647, 998244353]

# ===========================================================================
# Lyndon word combinatorics (brute force -- alphabet size <=3, degree <=6 in
# this pass, totally tractable: 3^6=729 candidate words at the largest case).
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


def eval_plain_tree(tree, leaf_vecs, p):
    """Evaluate a Lyndon bracket tree using PLAIN word_bracket, substituting
    leaf letter -> ambient vector (dict) via leaf_vecs."""
    if tree[0] == 'leaf':
        return dict(leaf_vecs[tree[1]])
    _, lt, rt, dl, dr, u, v = tree
    lv = eval_plain_tree(lt, leaf_vecs, p)
    rv = eval_plain_tree(rt, leaf_vecs, p)
    return word_bracket(lv, rv, p)


class GradedLie:
    """One free Lie algebra Lie(alphabet), Lyndon basis per degree, with
    ambient<->coordinate conversion mod p. p is fixed at construction."""

    def __init__(self, alphabet_size, kmax, p):
        self.alphabet_size = alphabet_size
        self.kmax = kmax
        self.p = p
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
            self.ambient[k] = [eval_plain_tree(t, identity_leaf, p) for t in trees]
            self.dim[k] = len(ws)

    def coords_of_ambient(self, degree, vec):
        """Express ambient vector (dict, degree `degree`) in this degree's
        Lyndon basis coordinates. Returns list length self.dim[degree]."""
        basis = self.ambient[degree]
        ncols = len(basis)
        if ncols == 0:
            assert not vec, f"expected zero vector, got {vec} at degree {degree} with empty basis"
            return []
        all_words = sorted(set().union(*[set(b.keys()) for b in basis], set(vec.keys())))
        M_cols = [[b.get(w, 0) for w in all_words] for b in basis]
        v = [vec.get(w, 0) % self.p for w in all_words]
        coord = solve_modp(M_cols, v, self.p)
        # verify
        check = word_add([{w: (M_cols[c][i] * coord[c]) % self.p} for c in range(ncols)
                           for i, w in enumerate(all_words)] if False else
                          [scale_vec(basis[c], coord[c], self.p) for c in range(ncols)], self.p)
        if check != vec:
            raise ValueError(f"coords_of_ambient verification FAILED at degree {degree}: "
                              f"recombination mismatch (basis may not span the target vector)")
        return coord

    def coords_to_ambient(self, degree, coords):
        basis = self.ambient[degree]
        return word_add([scale_vec(basis[i], c, self.p) for i, c in enumerate(coords) if c % self.p != 0], self.p)


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
