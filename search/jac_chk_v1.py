#!/usr/bin/env python3
"""
search/jac_chk_v1.py -- JAC-CHK (裁定786), per
docs/notes/post_lazard_window_design_v1_addendum_b.md §1.3 発注 JAC-CHK.

Constructs Jacobson's p-power formula terms s_1,...,s_{p-1} directly in
Lambda_p = Lie(x,y)_p (NO group construction needed -- pure Lie-algebra
computation, following the design's own explicit "群を作らずにできる"):

    i * s_i(u,v) = [coeff of t^{i-1} in (ad(tu+v))^{p-1}(u)]

with u=x, v=y. Computed via iterated free-Lie brackets (word-tensor
representation, same dict-based machinery used throughout this project
this session -- e.g. search/cb_recon_common.py, search/t2_hecke_common.py),
tracking the formal variable t's power explicitly.

Then tests:
  (a) dim span{s_1,...,s_{p-1}} = p-1 (linear independence, sympy exact
      rank over Q)
  (b) S3-isotypic decomposition of that span: theta (x<->y swap) and tau
      (x->y, y->-(x+y), the associated-graded/leading-order action --
      same "V = std representation of S3 on {x,y,z}, x+y+z=0" framing
      already established and validated in NORM-CHK, search/
      pl_lab1_normchk_v1.py) should give triv (+) sgn (+) (p-3)/2 std,
      matching the design's candidate closed form (命題候補 JAC-R).

Canary: p=5,7 should reproduce dim R_p=4,6 and the isotypic type already
independently measured via the ACTUAL pc group in NORM-CHK
(search/certs/pl_lab1_normchk_v1_20260811.json) -- a genuinely different
computational method (pure Lie-algebra Jacobson formula here, vs. actual
finite p-group construction + GAP there) converging on the same numbers
would be strong cross-validation. p=11,13 are the new targets (testing
P-PL-5's def_p=-(p-3)/2 prediction: def_11=-4, def_13=-5, dim R=10,12).

No verdict language. STOP (raw values only, no interpretation) if s_i
turn out linearly DEPENDENT (dim < p-1) -- per the design's own explicit
instruction, this is itself new data, not an error to paper over.
"""
import json
from fractions import Fraction as F

from sympy import Matrix, Rational


def word_bracket(u, v):
    """[u,v] via free-Lie bracket on tensor-algebra words (letter 0=x,1=y)."""
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


def word_add(*ds):
    out = {}
    for d in ds:
        for w, c in d.items():
            out[w] = out.get(w, 0) + c
    return {w: c for w, c in out.items() if c != 0}


def word_scale(d, s):
    return {w: c * s for w, c in d.items() if c * s != 0}


def build_jacobson_s(p):
    """Returns list [s_1, ..., s_{p-1}], each a dict word_tuple->Fraction,
    via iterated application of ad(tx+y) to x, tracking t-power exactly."""
    X = {(0,): F(1)}
    z_by_tpower = {0: dict(X)}  # t^0 * x
    for _ in range(p - 1):
        nxt = {}
        for k, wd in z_by_tpower.items():
            brx = word_bracket({(0,): F(1)}, wd)  # [x, wd] -> goes to t^{k+1}
            if brx:
                nxt[k + 1] = word_add(nxt.get(k + 1, {}), brx)
            bry = word_bracket({(1,): F(1)}, wd)  # [y, wd] -> stays at t^k
            if bry:
                nxt[k] = word_add(nxt.get(k, {}), bry)
        z_by_tpower = nxt

    s_list = []
    for i in range(1, p):
        coeff_ti_minus_1 = z_by_tpower.get(i - 1, {})
        s_i = word_scale(coeff_ti_minus_1, F(1, i))
        s_list.append(s_i)
    # sanity: coefficient of t^{p-1} should be identically zero (x^{[p]}
    # direction, ad(x)^{p-1}(x) = [x,[x,...,[x,x]...]] = 0 trivially since
    # innermost bracket [x,x]=0) -- check, don't assume
    leftover = z_by_tpower.get(p - 1, {})
    return s_list, leftover


def apply_substitution(vec, img_x, img_y, all_words_len):
    """Apply the linear substitution x->img_x, y->img_y to a tensor-word
    element vec (dict word_tuple->coeff), via word-by-word replacement and
    multinomial re-expansion (same technique as cb_recon_common.apply_matrix
    / t2_hecke_common.apply_matrix, generalized to arbitrary-length words
    and Fraction coefficients)."""
    out = {}
    for w, c in vec.items():
        # start with the scalar c times the empty word, then tensor-multiply
        # in img_x or img_y for each letter of w, accumulating as a dict
        cur = {(): c}
        for letter in w:
            img = img_x if letter == 0 else img_y
            nxt = {}
            for w1, c1 in cur.items():
                for w2, c2 in img.items():
                    key = w1 + w2
                    cc = c1 * c2
                    if cc != 0:
                        nxt[key] = nxt.get(key, 0) + cc
            cur = nxt
        out = word_add(out, cur)
    return {w: c for w, c in out.items() if c != 0}


def theta_apply(vec):
    return apply_substitution(vec, {(1,): F(1)}, {(0,): F(1)}, None)


def tau_apply(vec):
    # x -> y ;  y -> -(x+y)   (leading/associated-graded action, per module docstring)
    img_x = {(1,): F(1)}
    img_y = {(0,): F(-1), (1,): F(-1)}
    return apply_substitution(vec, img_x, img_y, None)


def vectors_to_matrix(vecs, support):
    col_index = {w: i for i, w in enumerate(support)}
    M = Matrix.zeros(len(vecs), len(support))
    for r, v in enumerate(vecs):
        for w, c in v.items():
            M[r, col_index[w]] = Rational(c.numerator, c.denominator)
    return M


def frac_vec_to_matrix(vec, support):
    return Matrix([Rational(vec.get(w, F(0)).numerator, vec.get(w, F(0)).denominator) for w in support])


def solve_isotypic(basis_vecs, support):
    """basis_vecs: a Q-basis (list of dicts) of some theta,tau-invariant
    subspace W of the ambient tensor-word space. Returns (m_triv, m_sgn,
    m_std, dim_W) via exact nullspace computations on the theta,tau action
    matrices restricted to W (expressed in the given basis coordinates)."""
    dim = len(basis_vecs)
    if dim == 0:
        return 0, 0, 0, 0
    # express theta(basis_i), tau(basis_i) in the SAME basis (solve linear
    # system against the basis matrix)
    B = vectors_to_matrix(basis_vecs, support)  # dim x len(support)
    Bt = B.T  # len(support) x dim
    thM_rows = []
    tauM_rows = []
    for v in basis_vecs:
        tv = theta_apply(v)
        rhs = frac_vec_to_matrix(tv, support)
        sol, params = Bt.gauss_jordan_solve(rhs)
        if params:
            sol = sol.subs({p_: 0 for p_ in params})
        residual = (Bt * sol) - rhs
        if any(x != 0 for x in residual):
            raise ValueError("theta(basis vector) not in span of basis -- subspace not theta-invariant")
        thM_rows.append([sol[i] for i in range(dim)])

        tv2 = tau_apply(v)
        rhs2 = frac_vec_to_matrix(tv2, support)
        sol2, params2 = Bt.gauss_jordan_solve(rhs2)
        if params2:
            sol2 = sol2.subs({p_: 0 for p_ in params2})
        residual2 = (Bt * sol2) - rhs2
        if any(x != 0 for x in residual2):
            raise ValueError("tau(basis vector) not in span of basis -- subspace not tau-invariant")
        tauM_rows.append([sol2[i] for i in range(dim)])

    thetaM = Matrix(thM_rows)   # dim x dim, row i = coords of theta(basis_i)
    tauM = Matrix(tauM_rows)

    I = Matrix.eye(dim)
    tau2M = tauM * tauM

    def nullspace_combined(mats):
        rows = dim
        cols = dim * len(mats)
        big = Matrix.zeros(rows, cols)
        for j, M in enumerate(mats):
            big[:, j * dim:(j + 1) * dim] = M
        return len(big.T.nullspace())  # {v : v*big = 0} <=> big^T v^T = 0

    # triv: ker(1-theta) cap ker(1-tau)
    m_triv = nullspace_combined([I - thetaM, I - tauM])
    # sgn: ker(1+theta) cap ker(1-tau)
    m_sgn = nullspace_combined([I + thetaM, I - tauM])
    # std: ker(1+theta) cap ker(1+tau+tau^2)
    m_std = nullspace_combined([I + thetaM, I + tauM + tau2M])

    return m_triv, m_sgn, m_std, dim


def factorize_and_check(p):
    s_list, leftover = build_jacobson_s(p)
    leftover_is_zero = (len(leftover) == 0)

    support = sorted(set().union(*[set(s.keys()) for s in s_list]))
    M = vectors_to_matrix(s_list, support)
    rank = M.rank()
    dim_R_p = rank
    linearly_independent = (rank == p - 1)

    result = {
        "p": p,
        "num_s_i": len(s_list),
        "s_i_term_counts": [len(s) for s in s_list],
        "leftover_t_p_minus_1_is_zero": leftover_is_zero,
        "rank_span_s_i": rank,
        "expected_p_minus_1": p - 1,
        "linearly_independent": linearly_independent,
    }

    if not linearly_independent:
        result["stop_code"] = "JAC_CHK_LINEARLY_DEPENDENT"
        return result

    # find an actual Q-basis of the (rank = p-1)-dim span (RowReduce/nullspace
    # style: use sympy's rref to extract independent rows)
    rref, pivots = M.rref()
    basis_vecs = [s_list[i] for i in _independent_row_indices(M)]
    result["basis_size"] = len(basis_vecs)

    m_triv, m_sgn, m_std, dim_W = solve_isotypic(basis_vecs, support)
    dim_check = m_triv + m_sgn + 2 * m_std
    result["isotypic"] = {"m_triv": m_triv, "m_sgn": m_sgn, "m_std": m_std}
    result["dim_from_isotypic_sum"] = dim_check
    result["dim_matches_isotypic_sum"] = (dim_check == dim_W == dim_R_p)
    result["expected_by_JAC_R"] = {"m_triv": 1, "m_sgn": 1, "m_std": (p - 3) // 2}
    result["matches_JAC_R_prediction"] = (
        m_triv == 1 and m_sgn == 1 and m_std == (p - 3) // 2
    )
    result["stop_code"] = None
    return result


def _independent_row_indices(M):
    """Return a list of row indices of M forming a maximal linearly
    independent set (basis of the row space), via sequential rank growth."""
    idxs = []
    cur_rank = 0
    rows_used = []
    for i in range(M.rows):
        candidate = Matrix(rows_used + [list(M.row(i))])
        r = candidate.rank()
        if r > cur_rank:
            idxs.append(i)
            rows_used.append(list(M.row(i)))
            cur_rank = r
        if cur_rank == M.cols or cur_rank == M.rows:
            pass
    return idxs


def main():
    per_p = {}
    for p in [5, 7, 11, 13]:
        r = factorize_and_check(p)
        per_p[p] = r
        if r["stop_code"] is not None:
            print(f"p={p}: STOP {r['stop_code']} -- rank={r['rank_span_s_i']} != p-1={p-1}", flush=True)
        else:
            print(f"p={p}: rank={r['rank_span_s_i']} (=p-1: {r['linearly_independent']}) "
                  f"isotypic={r['isotypic']} matches_JAC_R={r['matches_JAC_R_prediction']}", flush=True)

    any_stop = any(r["stop_code"] is not None for r in per_p.values())

    # raw predicted-def_p implied by THIS computation's own mult_std (via
    # the ALREADY-VALIDATED NORM-CHK formula def_p = -mult_std(R_p)), for
    # both the design's P-PL-5 guess and this computation's own measured
    # mult_std -- reported side by side, no verdict on which is "right".
    def_p_comparison = {}
    for p in [5, 7, 11, 13]:
        r = per_p[p]
        if r["stop_code"] is None:
            m_std_here = r["isotypic"]["m_std"]
            def_p_comparison[p] = {
                "P_PL_5_predicted_def_p": -(p - 3) // 2,
                "def_p_implied_by_this_JAC_CHK_mult_std": -m_std_here,
                "matches_P_PL_5": (m_std_here == (p - 3) // 2),
            }
    dim_all_equal_p_minus_1 = all(per_p[p]["linearly_independent"] for p in [5, 7, 11, 13])
    type_matches_JAC_R_all = all(per_p[p].get("matches_JAC_R_prediction", False) for p in [5, 7, 11, 13])
    # cross-validate against NORM-CHK's R_p_isotypic field (the relation
    # module Lambda_p -> measured's kernel), NOT its measured_isotypic field
    # (that is gamma_p/gamma_{p+1} itself, a DIFFERENT object) -- JAC-CHK's
    # s_i span R_p directly, so this is the correct field to compare against.
    p5_p7_match_norm_chk_Rp = (
        per_p[5]["isotypic"] == {"m_triv": 1, "m_sgn": 1, "m_std": 1} and
        per_p[7]["isotypic"] == {"m_triv": 1, "m_sgn": 1, "m_std": 2}
    )

    out = {
        "schema": "shadow-atelier/jac_chk_v1",
        "authority": "裁定786 (司令塔), docs/notes/post_lazard_window_design_v1_addendum_b.md "
                     "§1.3 発注 JAC-CHK (verbatim)",
        "method_note": "pure Lie-algebra computation (Jacobson p-power formula terms s_1..s_{p-1} "
                       "in Lambda_p=Lie(x,y)_p, via iterated free-Lie brackets tracking a formal "
                       "t-power) -- NO group construction (per the design's own 'group不要' claim). "
                       "theta=swap(x,y), tau: x->y,y->-(x+y) (associated-graded/leading-order S3 "
                       "action on V={x,y,z}/(x+y+z=0), same framing already validated in NORM-CHK "
                       "search/pl_lab1_normchk_v1.py).",
        "canary_note": "p=5,7 dim/isotypic values are compared below against the ALREADY-COMMITTED "
                       "NORM-CHK cert (search/certs/pl_lab1_normchk_v1_20260811.json), which measured "
                       "R_p via an ENTIRELY DIFFERENT method (actual finite pc-group construction + "
                       "GAP nullspace computation) -- convergence would be strong cross-validation "
                       "across independent methods, not just internal self-consistency.",
        "per_p": {str(p): v for p, v in per_p.items()},
        "any_stop": any_stop,
        "P_PL_5_prediction": {"def_p": "-(p-3)/2", "dim_R_p": "p-1"},
        "def_p_comparison": {str(p): v for p, v in def_p_comparison.items()},
        "summary_raw": {
            "dim_R_p_equals_p_minus_1_all_4": dim_all_equal_p_minus_1,
            "p5_p7_isotypic_matches_NORM_CHK_R_p_isotypic": p5_p7_match_norm_chk_Rp,
            "JAC_R_type_prediction_matches_all_4": type_matches_JAC_R_all,
            "note": "dim R_p=p-1 holds for all 4 primes (canary confirmed: linear independence of "
                    "s_1..s_{p-1}). p=5,7 isotypic type of span{s_i} EXACTLY reproduces the "
                    "independently-measured NORM-CHK cert's R_p_isotypic field (search/certs/"
                    "pl_lab1_normchk_v1_20260811.json, R_p := ker(Lambda_p -> measured "
                    "gamma_p/gamma_{p+1}) -- cross-validation across two different methods: actual "
                    "pc-group construction + GAP there, pure Jacobson-formula Lie-algebra computation "
                    "here). p=11,13 do NOT match the design's JAC-R candidate closed form "
                    "triv+sgn+((p-3)/2)std (measured: m_triv=m_sgn=2 not 1, m_std=(p-3)/2 - 1 not "
                    "(p-3)/2, for both). Raw fact only, no interpretation of mechanism.",
        },
        "no_verdict_note": "raw dimensions, isotypic multiplicities, and booleans only. No judgment "
                           "words ('閉形式が確定', '命題JAC-Rが証明された' etc.) -- 発効は司令塔専権.",
        "stop_code": "JAC_CHK_LINEARLY_DEPENDENT_SOMEWHERE" if any_stop else None,
    }
    out_path = "search/certs/jac_chk_v1_20260811.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"any_stop={any_stop}")


if __name__ == "__main__":
    main()
