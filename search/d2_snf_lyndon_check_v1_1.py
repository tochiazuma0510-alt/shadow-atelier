#!/usr/bin/env python3
"""
search/d2_snf_lyndon_check_v1_1.py -- 裁定756 Q1 決定打 (司令塔), following up
on search/d2_snf_sweep_v1.py (D2-SNF-1, 裁定752/addendum_b §1.4). Produces
cert v1.1 (SUPERSEDES search/certs/d2_snf_sweep_v1_20260807.json, per
裁定756's explicit instruction "cert v1.1(supersede・両基底の対照表)").

d2_snf_sweep_v1.py computed beta_k's Smith Normal Form using AMBIENT
tensor-algebra (word) coordinates, restricted to the observed nonzero
support -- justified by an (unpinned, addendum-external) appeal to the
free Lie ring being a SATURATED Z-submodule of the free associative
Z-algebra (Reutenauer, standard PBW-type fact for free Lie rings). That
appeal was flagged to 司令塔 (ops/express 20260807) as an unverified
implementer judgment call, not present in the addendum's own text.

This script tests that appeal DIRECTLY and computationally for the two
weights 司令塔 designated (k=32: where the p=5 quarantine finding occurred;
k=14: the control/calibration weight, dim S_14=0) by constructing an
EXPLICIT INTRINSIC INTEGER BASIS of the depth-2 free-Lie-algebra piece
(dimension (k-2)/2) via the classical Lyndon-word / standard-bracketing
construction (Chen-Fox-Lyndon factorization: every Lyndon word w of
length>1 has a unique "standard factorization" w=uv with v the longest
proper Lyndon suffix, and bracket(w):=[bracket(u),bracket(v)] recursively;
these Lyndon-word brackets are the classical Z-basis of the free Lie ring
-- Reutenauer, "Free Lie Algebras", Thm 5.1/Cor 4.14), then:

  1. Verifies #{Lyndon words, weight k, depth 2} == (k-2)/2 (matches the
     addendum's target-dimension formula -- an independent confirmation
     that this Lyndon subset really is a full basis candidate).
  2. Expresses each row vector {sigma_bar_a,sigma_bar_b} (already computed,
     verbatim reused, from search/d2_snf_sweep_v1.py's construction) in
     this Lyndon basis by SOLVING the linear system over Q -- if the free
     Lie ring is truly saturated at this weight/multidegree, every
     solution must come out with INTEGER coordinates (no denominators).
     This itself is the primary empirical test: an INTEGER-vs-FRACTIONAL
     outcome, recorded as a raw boolean per row, no interpretation.
  3. Builds the num_pairs x (k-2)/2 INTRINSIC integer matrix (exactly the
     addendum table's stated matrix shape, e.g. 7x15 at k=32) and computes
     its Smith Normal Form (sympy, exact ZZ).
  4. Compares elementary_divisors/gcd_abs/torsion_primes between the
     AMBIENT computation (read from the existing v1 cert, unmodified) and
     this INTRINSIC computation, for k=14 and k=32 only (as instructed).

No verdict language, no reference to (32,5)'s 素性/interpretation
(quarantined per 裁定756's explicit instruction) -- raw booleans and
integer values only, plus the pre-registered STOP code
(NON_INTEGER_COORDINATES) if step 2's integrality fails anywhere.
"""
import json
import sys
import time
from math import comb, gcd

from sympy import Matrix, ZZ, Rational
from sympy.matrices.normalforms import smith_normal_form

TARGET_K = [14, 32]
V1_CERT_PATH = "search/certs/d2_snf_sweep_v1_20260807.json"


# ---------- reused verbatim (same closed forms as d2_snf_sweep_v1.py;
# duplicated here rather than imported, so this script stands as an
# independent re-derivation of the row vectors too, not just the basis
# change) ----------

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


# ---------- Lyndon-word standard basis of the free Lie ring ----------

def is_lyndon(w):
    n = len(w)
    for i in range(1, n):
        if (w[i:] + w[:i]) <= w:
            return False
    return True


def standard_factorization(w):
    """w Lyndon, len(w)>1: return (u,v) with v the LONGEST proper suffix
    of w that is itself Lyndon (smallest split index i>=1 with w[i:]
    Lyndon), u the complementary prefix (also Lyndon, by the standard
    theorem)."""
    n = len(w)
    for i in range(1, n):
        if is_lyndon(w[i:]):
            return w[:i], w[i:]
    raise ValueError(f"no standard factorization found for {w}")


def lyndon_bracket(w, memo):
    """Recursively expand the standard Lyndon bracketing of w into ambient
    word (tensor-algebra) coordinates, memoized."""
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
    """All Lyndon words of length k with exactly two 1-letters (depth 2),
    generated by brute force over the C(k,2) candidate positions (cheap:
    k<=32 => <=496 candidates)."""
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


def write_out(out, path="search/certs/d2_snf_sweep_v1_1_20260807.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path}", flush=True)


def write_stop(stop_code, detail):
    out = {
        "schema": "shadow-atelier/d2_snf_sweep_v1.1",
        "authority": "裁定756 (司令塔) Q1決定打, following search/d2_snf_sweep_v1.py "
                      "(裁定752①, tor_sweep_design_v1_addendum_b.md §1.4)",
        "supersedes": V1_CERT_PATH,
        "stop_code": stop_code,
        "stop_detail": detail,
    }
    write_out(out)
    print("D2_SNF_LYNDON_STOP", flush=True)
    sys.exit(1)


def main():
    t_start = time.time()
    print("=== D2-SNF Lyndon-basis check (裁定756 Q1): JOB START ===", flush=True)

    v1_cert = json.load(open(V1_CERT_PATH, encoding="utf-8"))

    comparison = {}
    non_integer_found = []

    for k in TARGET_K:
        t0 = time.time()
        pairs = [(a, k - a) for a in range(3, k // 2 + 1, 2) if a < k - a]
        num_pairs = len(pairs)
        sigma_cache = {}

        def get_sigma(a):
            if a not in sigma_cache:
                sigma_cache[a] = sigma_bar(a)
            return sigma_cache[a]

        row_vecs = [ihara_bracket(get_sigma(a), get_sigma(b)) for (a, b) in pairs]

        # ---- intrinsic Lyndon basis of the depth-2 piece ----
        lyn_words = depth2_lyndon_words(k)
        target_dim_formula = (k - 2) // 2
        lyndon_count_matches_formula = (len(lyn_words) == target_dim_formula)
        if not lyndon_count_matches_formula:
            write_stop("LYNDON_COUNT_MISMATCH", {"k": k, "lyndon_count": len(lyn_words),
                                                    "target_dim_formula": target_dim_formula})
            return

        memo = {}
        basis_vecs = [lyndon_bracket(w, memo) for w in lyn_words]

        # column space for the linear-solve: union of support of basis
        # vectors AND row vectors (must agree, since rows must lie in the
        # span of the basis if saturation/spanning holds -- checked below)
        support = sorted(set().union(*[set(v.keys()) for v in basis_vecs],
                                      *[set(v.keys()) for v in row_vecs]))
        col_index = {w: i for i, w in enumerate(support)}

        B = Matrix.zeros(len(basis_vecs), len(support))  # basis_dim x support
        for r, v in enumerate(basis_vecs):
            for w, c in v.items():
                B[r, col_index[w]] = c

        basis_rank = B.rank()
        basis_is_full_rank = (basis_rank == len(lyn_words))

        # ---- solve each row vector as an EXACT Q-combination of the
        # Lyndon basis rows: row = c^T * B  (c has length len(lyn_words)) ----
        Bt = B.T  # support x basis_dim
        row_coords = []
        row_is_integer = []
        for v in row_vecs:
            rhs = Matrix([v.get(w, 0) for w in support])  # support x 1
            # solve Bt * c = rhs  (least squares / exact if in row space)
            sol, params = Bt.gauss_jordan_solve(rhs)
            if params:
                # underdetermined (shouldn't happen: basis full rank,
                # support >= basis_dim) -- treat free params as zero and
                # flag via residual check below
                sol = sol.subs({p: 0 for p in params})
            residual = (Bt * sol) - rhs
            if any(x != 0 for x in residual):
                write_stop("ROW_NOT_IN_LYNDON_SPAN", {"k": k, "row_index": len(row_coords),
                                                         "residual_nonzero_count": sum(1 for x in residual if x != 0)})
                return
            coords = [Rational(sol[i]) for i in range(len(lyn_words))]
            is_int = all(c.q == 1 for c in coords)
            row_coords.append([int(c) if c.q == 1 else str(c) for c in coords])
            row_is_integer.append(is_int)
            if not is_int:
                non_integer_found.append({"k": k, "row_index": len(row_coords) - 1,
                                           "coords_with_denominators": [str(c) for c in coords if c.q != 1]})

        all_rows_integer = all(row_is_integer)

        if not all_rows_integer:
            # fail-closed: record raw fact, do not silently proceed to
            # build an integer matrix from fractional coordinates
            write_stop("NON_INTEGER_COORDINATES", {"k": k, "non_integer_rows": non_integer_found})
            return

        # ---- intrinsic matrix (num_pairs x (k-2)/2, exact integers) ----
        M_intrinsic = Matrix(num_pairs, len(lyn_words),
                              lambda i, j: row_coords[i][j])

        rank_Q_intrinsic = M_intrinsic.rank()
        snf = smith_normal_form(M_intrinsic, domain=ZZ)
        diag = [int(snf[i, i]) for i in range(min(snf.rows, snf.cols))]
        elementary_divisors_intrinsic = [d for d in diag if d != 0]
        gcd_abs_intrinsic = abs(elementary_divisors_intrinsic[-1]) if elementary_divisors_intrinsic else 1
        torsion_primes_intrinsic = sorted(factorize(gcd_abs_intrinsic).keys())

        ambient_row = v1_cert["per_k"][str(k)]

        comparison[k] = {
            "num_pairs": num_pairs,
            "target_dim_formula": target_dim_formula,
            "lyndon_word_count": len(lyn_words),
            "lyndon_count_matches_formula": lyndon_count_matches_formula,
            "lyndon_basis_full_rank": basis_is_full_rank,
            "row_coordinates_in_lyndon_basis": row_coords,
            "all_row_coordinates_integer": all_rows_integer,
            "intrinsic": {
                "matrix_shape": [num_pairs, len(lyn_words)],
                "rank_Q": rank_Q_intrinsic,
                "elementary_divisors": elementary_divisors_intrinsic,
                "gcd_abs": gcd_abs_intrinsic,
                "gcd_abs_factorization": {str(p): e for p, e in factorize(gcd_abs_intrinsic).items()},
                "torsion_primes": torsion_primes_intrinsic,
            },
            "ambient": {
                "matrix_shape": [ambient_row["num_pairs"], ambient_row["ambient_support_size"]],
                "rank_Q": ambient_row["rank_Q"],
                "elementary_divisors": ambient_row["elementary_divisors"],
                "gcd_abs": ambient_row["gcd_abs"],
                "gcd_abs_factorization": ambient_row["gcd_abs_factorization"],
                "torsion_primes": ambient_row["torsion_primes"],
            },
            "rank_Q_agrees": (rank_Q_intrinsic == ambient_row["rank_Q"]),
            "elementary_divisors_agree": (elementary_divisors_intrinsic == ambient_row["elementary_divisors"]),
            "gcd_abs_agrees": (gcd_abs_intrinsic == ambient_row["gcd_abs"]),
            "torsion_primes_agree": (torsion_primes_intrinsic == ambient_row["torsion_primes"]),
            "elapsed_sec": round(time.time() - t0, 4),
        }
        print(f"k={k}: lyndon_count={len(lyn_words)} all_rows_integer={all_rows_integer} "
              f"intrinsic_ED={elementary_divisors_intrinsic} intrinsic_gcd_abs={gcd_abs_intrinsic} "
              f"intrinsic_torsion={torsion_primes_intrinsic} | ambient_ED={ambient_row['elementary_divisors']} "
              f"ambient_gcd_abs={ambient_row['gcd_abs']} ambient_torsion={ambient_row['torsion_primes']} | "
              f"AGREE={comparison[k]['elementary_divisors_agree']} elapsed={comparison[k]['elapsed_sec']}s",
              flush=True)

    all_agree = all(comparison[k]["elementary_divisors_agree"] for k in TARGET_K)

    out = {
        "schema": "shadow-atelier/d2_snf_sweep_v1.1",
        "authority": "裁定756 (司令塔) Q1決定打, following search/d2_snf_sweep_v1.py "
                      "(裁定752①, tor_sweep_design_v1_addendum_b.md §1.4)",
        "supersedes": V1_CERT_PATH,
        "supersede_note": "v1 (ambient-tensor-coordinate SNF, all k=12..32) is UNCHANGED and remains "
                           "the primary D2-SNF-1 record; this v1.1 cert adds the k=14/k=32 "
                           "ambient-vs-intrinsic-Lyndon-basis comparison 裁定756 Q1 requested, to test "
                           "the (previously flagged, unpinned) saturation appeal used to justify v1's "
                           "ambient-coordinate SNF as equivalent to an intrinsic-basis SNF.",
        "target_k": TARGET_K,
        "comparison": {str(k): v for k, v in comparison.items()},
        "all_elementary_divisors_agree": all_agree,
        "no_verdict_note": "No interpretation of (32,5)'s 素性/nature is written here (still under "
                            "quarantine per 裁定756). This cert reports only: (a) whether the row "
                            "vectors have INTEGER coordinates in the explicit Lyndon basis (raw bool "
                            "per row), and (b) whether the resulting intrinsic-basis SNF matches the "
                            "already-committed ambient-coordinate SNF (raw bool per k). Pre-registered "
                            "STOP codes: LYNDON_COUNT_MISMATCH / ROW_NOT_IN_LYNDON_SPAN / "
                            "NON_INTEGER_COORDINATES.",
        "stop_code": None,
        "total_elapsed_sec": round(time.time() - t_start, 2),
    }
    write_out(out)
    print(f"=== D2-SNF Lyndon-basis check: JOB END total_elapsed_sec={out['total_elapsed_sec']} "
          f"all_elementary_divisors_agree={all_agree} stop_code=None ===", flush=True)
    print("D2_SNF_LYNDON_DONE", flush=True)


if __name__ == "__main__":
    main()
