#!/usr/bin/env python3
"""
search/d2_snf_sweep_v1.py -- D2-SNF-1 (裁定752①, per
docs/notes/tor_sweep_design_v1_addendum_b.md §1.4 発注仕様D2-SNF-1,
implemented verbatim). Task order: implementer 単任務2連, task 2/2.

Computes the depth-2 Ihara-bracket map
  beta_k : wedge^2(ls_1)_k -> (depth-2 part)_k ,   sigma_bar_a ^ sigma_bar_b
    |-> {sigma_bar_a, sigma_bar_b}          (a+b=k, a,b odd >=3, a<b)
for every even weight k in [12,32] (the addendum's frozen prereg range),
as an EXACT INTEGER matrix, then its rank over Q, an integer kernel basis,
and its Smith Normal Form (elementary divisors) -- testing the frozen
prediction P-D2-1: d_r(beta_k) = +-1 (zero torsion primes) for all k in
this range.

sigma_bar_a := (-1)^((a-1)/2) * (ad X)^(a-1)(Y), constructed via the
CLOSED FORM (ad X)^n(Y) = sum_{i=0}^n (-1)^i C(n,i) X^(n-i) Y X^i (an
elementary, independently-verifiable identity for the free-Lie left-adjoint
action, cross-checked against the recursive word-bracket construction used
in search/ra7_probe_v1.py for a=3, where both give the identical 3-term
vector -- see that script's R-b). No sigma_m reconstruction pipeline
(aside1/aside2/aside3/GAP) is used anywhere in this script: sigma_bar_a is
pure closed-form, and the Ihara bracket {sigma_bar_a,sigma_bar_b} of two
depth-1 elements stays entirely INTEGER (deriv/word_bracket involve only
integer word-concatenation and binomial-integer coefficients, no
denominators arise) -- this is what makes the whole sweep millisecond-scale
(addendum's own cost estimate).

Ambient-vs-intrinsic justification (record for the reader, not re-derived
here): beta_k's image lies in the depth-2 piece of the free LIE algebra
(dimension (k-2)/2, a genuine sub-lattice of the depth-2 part of the free
ASSOCIATIVE (tensor) algebra, dimension C(k,2)). The free Lie ring is a
SATURATED (direct-summand) Z-submodule of the free associative Z-algebra
(standard fact, e.g. via a Lyndon/PBW-type basis extension -- Reutenauer,
"Free Lie Algebras"). For a saturated sublattice L <= Z^N, any map
phi: Z^s -> L has THE SAME Smith Normal Form/elementary divisors whether
computed w.r.t. an intrinsic Z-basis of L or w.r.t. the ambient
Z^N-coordinates (pad the intrinsic basis to a Z-basis of Z^N; the matrix
in the extended basis is phi padded with zero rows, same nonzero
invariant factors). Hence this script computes beta_k directly in ambient
WORD (tensor-algebra) coordinates -- restricted to the observed nonzero
word-support (dropping unused zero columns does not change any k x k
minor's gcd, hence does not change the SNF) -- rather than constructing an
explicit intrinsic Lyndon basis of the depth-2 Lie piece, which is not
needed for this argument to hold.

SNF computed via sympy.matrices.normalforms.smith_normal_form over ZZ
(polynomial-time row/column reduction, NOT brute-force gcd-of-all-minors
-- feasible even though the ambient column count for k=32 (C(32,2)=496)
is far larger than the r<=7 nonzero elementary divisors sought).

Prereg table (addendum §1.2, frozen BEFORE this run) is hard-coded below
and checked as a canary at D-b (rank) and, for the 4 weights the addendum
gives explicit integer kernel vectors for (k=12,16,18,20), at D-c
(kernel basis, up to sign/scalar proportionality). Canary failure ==> STOP
per addendum's own stop rule S-D2-1 (D-b/D-c canaries). S-D2-2: no verdict
language -- cert emits raw values, factorizations, and booleans only.

Pure Python (sympy for exact-integer rank/nullspace/SNF only) -- no GAP.
"""
import json
import sys
import time
from math import comb, gcd

from sympy import Matrix, ZZ, Rational
from sympy.matrices.normalforms import smith_normal_form

# ---- frozen prereg table (addendum §1.2, verbatim) ----
# k -> (num_pairs, dim_S_k, rank_Q_beta_k, target_dim=(k-2)/2)
PREREG_TABLE = {
    12: (2, 1, 1, 5),
    14: (2, 0, 2, 6),
    16: (3, 1, 2, 7),
    18: (3, 1, 2, 8),
    20: (4, 1, 3, 9),
    22: (4, 1, 3, 10),
    24: (5, 2, 3, 11),
    26: (5, 1, 4, 12),
    28: (6, 2, 4, 13),
    30: (6, 2, 4, 14),
    32: (7, 2, 5, 15),
}
# k -> expected kernel vector, in pair-order (ascending a), up to overall
# sign/scalar multiple (addendum §1.4 D-c canary, quoting 裁定727's
# independently-derived period-polynomial vectors)
EXPECTED_KERNEL_VECTORS = {
    12: [1, -3],
    16: [2, -7, 11],
    18: [8, -25, 26],
    20: [3, -10, 14, -13],
}
K_RANGE = list(range(12, 33, 2))


def sigma_bar(a):
    """sigma_bar_a = (-1)^((a-1)/2) * (ad X)^(a-1)(Y), closed form:
    (ad X)^n(Y) = sum_{i=0}^n (-1)^i C(n,i) X^(n-i) Y X^i, n=a-1.
    letter 0 = X, letter 1 = Y (convention shared with search/ra7_probe_v1.py
    and search/aside3_exact_D_v1.py)."""
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
    img = word_bracket({(1,): 1}, f)  # [Y,f]
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
    d1 = deriv(f, g)
    d2 = deriv(g, f)
    plain = word_bracket(f, g)
    out = {}
    for w, c in d1.items():
        out[w] = out.get(w, 0) + c
    for w, c in d2.items():
        out[w] = out.get(w, 0) - c
    for w, c in plain.items():
        out[w] = out.get(w, 0) + c
    return {w: c for w, c in out.items() if c != 0}


def depth_of(word):
    return sum(1 for letter in word if letter == 1)


def primitive_int_vector(rational_list):
    """Given a list of sympy Rationals (a Q-basis vector of a 1-dim
    nullspace slice, or a single nullspace column), clear denominators and
    divide by gcd to get a primitive integer vector. Sign convention: make
    the first nonzero entry positive."""
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
    """True iff v1 == +-v2 exactly (both already primitive-integer, same
    length)."""
    if len(v1) != len(v2):
        return False
    if v1 == v2:
        return True
    if [-x for x in v1] == v2:
        return True
    return False


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


def write_out(out, path="search/certs/d2_snf_sweep_v1_20260807.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path}", flush=True)


def write_stop(stop_code, detail):
    out = {
        "schema": "shadow-atelier/d2_snf_sweep_v1",
        "authority": "裁定752① (司令塔), docs/notes/tor_sweep_design_v1_addendum_b.md "
                      "§1.4 発注仕様D2-SNF-1 (verbatim)",
        "stop_code": stop_code,
        "stop_detail": detail,
    }
    write_out(out)
    print("D2_SNF_SWEEP_STOP", flush=True)
    sys.exit(1)


def main():
    t_start = time.time()
    print("=== D2-SNF-1: JOB START ===", flush=True)

    per_k = {}
    canary_failures = []

    for k in K_RANGE:
        t0 = time.time()
        pairs = [(a, k - a) for a in range(3, k // 2 + 1, 2) if a < k - a]
        num_pairs = len(pairs)
        target_dim_formula = (k - 2) // 2

        sigma_cache = {}

        def get_sigma(a):
            if a not in sigma_cache:
                sigma_cache[a] = sigma_bar(a)
            return sigma_cache[a]

        row_vecs = []
        for (a, b) in pairs:
            v = ihara_bracket(get_sigma(a), get_sigma(b))
            depths = set(depth_of(w) for w in v)
            weights = set(len(w) for w in v)
            if depths - {2}:
                write_stop("DEPTH_CANARY_FAIL", {"k": k, "pair": [a, b], "depths_seen": sorted(depths)})
                return
            if weights - {k}:
                write_stop("WEIGHT_CANARY_FAIL", {"k": k, "pair": [a, b], "weights_seen": sorted(weights)})
                return
            row_vecs.append(v)

        support = sorted(set().union(*[set(v.keys()) for v in row_vecs])) if row_vecs else []
        col_index = {w: i for i, w in enumerate(support)}

        M = Matrix.zeros(num_pairs, len(support))
        for r, v in enumerate(row_vecs):
            for w, c in v.items():
                M[r, col_index[w]] = c

        rank_Q = M.rank()
        dim_S_k = num_pairs - rank_Q

        # ---- D-b canary: rank vs prereg table ----
        expected = PREREG_TABLE.get(k)
        rank_matches_prereg = (expected is not None and expected[2] == rank_Q)
        pairs_match_prereg = (expected is not None and expected[0] == num_pairs)
        dimS_matches_prereg = (expected is not None and expected[1] == dim_S_k)
        target_matches_prereg = (expected is not None and expected[3] == target_dim_formula)
        if not (rank_matches_prereg and pairs_match_prereg and dimS_matches_prereg and target_matches_prereg):
            canary_failures.append({
                "k": k, "stage": "D-b",
                "computed": {"num_pairs": num_pairs, "dim_S_k": dim_S_k, "rank_Q": rank_Q,
                             "target_dim_formula": target_dim_formula},
                "prereg_expected": {"num_pairs": expected[0], "dim_S_k": expected[1],
                                     "rank_Q": expected[2], "target_dim": expected[3]} if expected else None,
            })

        # ---- D-c: integer kernel basis ----
        kernel_basis_primitive = []
        if dim_S_k > 0:
            # kernel of beta_k as a map FROM the source (pairs) means: which
            # linear combinations of ROWS of M vanish -- i.e. the LEFT
            # nullspace of M, equivalently the (right) nullspace of M^T.
            # Each resulting vector has length num_pairs (NOT len(support)).
            nullspace = M.T.nullspace()  # list of column vectors, length num_pairs, len(list)==dim_S_k
            for vec in nullspace:
                comps = [Rational(vec[i]) for i in range(num_pairs)]
                kernel_basis_primitive.append(primitive_int_vector(comps))

        # ---- D-c canary: kernel vector proportional to 裁定727 values (k=12,16,18,20) ----
        expected_kv = EXPECTED_KERNEL_VECTORS.get(k)
        kernel_canary_result = None
        if expected_kv is not None:
            match = any(proportional_up_to_sign(kv, expected_kv) for kv in kernel_basis_primitive)
            kernel_canary_result = match
            if not match:
                canary_failures.append({
                    "k": k, "stage": "D-c",
                    "computed_kernel_basis": kernel_basis_primitive,
                    "expected_kernel_vector_up_to_sign": expected_kv,
                })

        # ---- D-d: SNF (sympy, exact ZZ) ----
        snf = smith_normal_form(M, domain=ZZ)
        diag = [int(snf[i, i]) for i in range(min(snf.rows, snf.cols))]
        elementary_divisors = [d for d in diag if d != 0]
        if len(elementary_divisors) != rank_Q:
            write_stop("SNF_RANK_MISMATCH", {"k": k, "elementary_divisors": elementary_divisors, "rank_Q": rank_Q})
            return
        gcd_abs = abs(elementary_divisors[-1]) if elementary_divisors else 1
        torsion_primes = sorted(factorize(gcd_abs).keys())
        p_d2_1_pass_this_k = (gcd_abs == 1)

        # ---- 裁定756 Q2: bookkeeping classification (NOT a verdict) ----
        # p in {2,3} = scope boundary (P-T-1-style quantifier restricts to
        # p>=5 throughout this project, TOR-S3/Maschke); p>=5 = quarantine
        # candidate per addendum's own "反証されたら...一級" clause.
        torsion_primes_classification = {
            str(p): ("scope_boundary_no_alarm" if p in (2, 3) else "quarantine_surprise")
            for p in torsion_primes
        }

        per_k[k] = {
            "num_pairs": num_pairs,
            "pairs": [list(p) for p in pairs],
            "target_dim_formula": target_dim_formula,
            "rank_Q": rank_Q,
            "dim_S_k": dim_S_k,
            "rank_matches_prereg": rank_matches_prereg,
            "pairs_matches_prereg": pairs_match_prereg,
            "dimS_matches_prereg": dimS_matches_prereg,
            "target_matches_prereg": target_matches_prereg,
            "kernel_basis_primitive": kernel_basis_primitive,
            "kernel_canary_expected_vector": expected_kv,
            "kernel_canary_match": kernel_canary_result,
            "ambient_support_size": len(support),
            "elementary_divisors": elementary_divisors,
            "gcd_abs": gcd_abs,
            "gcd_abs_factorization": {str(p): e for p, e in factorize(gcd_abs).items()},
            "torsion_primes": torsion_primes,
            "torsion_primes_classification": torsion_primes_classification,
            "P_D2_1_pass_this_k": p_d2_1_pass_this_k,
            "elapsed_sec": round(time.time() - t0, 4),
        }
        print(f"k={k}: pairs={num_pairs} rank_Q={rank_Q} dim_S_k={dim_S_k} "
              f"kernel={kernel_basis_primitive} elementary_divisors={elementary_divisors} "
              f"gcd_abs={gcd_abs} torsion_primes={torsion_primes} "
              f"elapsed={per_k[k]['elapsed_sec']}s", flush=True)

    # ---- S-D2-1 stop rule: any D-b/D-c canary failure ⟹ STOP ----
    if canary_failures:
        write_stop("D2_SNF_CANARY_FAIL", {"failures": canary_failures})
        return

    all_gcd_abs_1 = all(per_k[k]["gcd_abs"] == 1 for k in K_RANGE)
    torsion_found = {k: per_k[k]["torsion_primes"] for k in K_RANGE if per_k[k]["torsion_primes"]}

    # ---- 裁定756 Q2 bookkeeping split (raw lists only, no verdict) ----
    scope_boundary_findings = []
    quarantine_surprise_findings = []
    for k in K_RANGE:
        for p in per_k[k]["torsion_primes"]:
            entry = {"k": k, "prime": p}
            if p in (2, 3):
                scope_boundary_findings.append(entry)
            else:
                quarantine_surprise_findings.append(entry)

    out = {
        "schema": "shadow-atelier/d2_snf_sweep_v1",
        "authority": "裁定752① (司令塔), docs/notes/tor_sweep_design_v1_addendum_b.md "
                      "§1.4 発注仕様D2-SNF-1 (verbatim)",
        "prereg": {
            "k_range": K_RANGE,
            "prereg_table": {str(k): {"num_pairs": v[0], "dim_S_k": v[1], "rank_Q": v[2], "target_dim": v[3]}
                              for k, v in PREREG_TABLE.items()},
            "expected_kernel_vectors": {str(k): v for k, v in EXPECTED_KERNEL_VECTORS.items()},
            "P_D2_1_statement": "d_r(beta_k) = +-1 (zero torsion primes) for k=12..32",
        },
        "per_k": {str(k): v for k, v in per_k.items()},
        "P_D2_1_all_gcd_abs_1": all_gcd_abs_1,
        "torsion_primes_found_by_k": {str(k): v for k, v in torsion_found.items()},
        "prime_finding_classification_note": "裁定756 Q2 (司令塔): p in {2,3} = scope boundary "
                                              "(想定類・警報なし, per this project's standing p>=5 "
                                              "quantifier convention, e.g. TOR-S3/Maschke); p>=5 "
                                              "(here: only p=5 at k=32) = quarantine_surprise. This "
                                              "is a bookkeeping split, not a verdict on (32,5)'s "
                                              "素性/interpretation (still under quarantine).",
        "scope_boundary_findings": scope_boundary_findings,
        "quarantine_surprise_findings": quarantine_surprise_findings,
        "canary_failures": canary_failures,
        "no_verdict_note": "S-D2-2 compliance: this script emits ONLY raw numeric values, integer "
                            "vectors, factorizations, and the pre-registered STOP codes "
                            "(DEPTH_CANARY_FAIL / WEIGHT_CANARY_FAIL / SNF_RANK_MISMATCH / "
                            "D2_SNF_CANARY_FAIL) -- no interpretive verdict prose. P_D2_1_all_gcd_abs_1 "
                            "is a raw boolean re-derivable from per_k[*].gcd_abs; its格付け (candidate/"
                            "cross-checked/etc.) is reserved for 司令塔/Sol per addendum §1.4.",
        "stop_code": None,
        "total_elapsed_sec": round(time.time() - t_start, 2),
    }
    write_out(out)
    print(f"=== D2-SNF-1: JOB END total_elapsed_sec={out['total_elapsed_sec']} "
          f"P_D2_1_all_gcd_abs_1={all_gcd_abs_1} stop_code=None ===", flush=True)
    print("D2_SNF_SWEEP_DONE", flush=True)


if __name__ == "__main__":
    main()
