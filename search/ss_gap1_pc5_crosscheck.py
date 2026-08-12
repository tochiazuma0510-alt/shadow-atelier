#!/usr/bin/env python3
"""
search/ss_gap1_pc5_crosscheck.py
SS-GAP-1 Stage 0 / PC-5 crosscheck (independent of GAP; python-only implementation).

Computes, via the Cayley-Hamilton closed form of
docs/notes/ss_gap1_count_spec_v1.md sec 4.1, the counts of
  i2 = #{A in SL(2,Z/p^2): A^2 = I}
  i3 = #{B in SL(2,Z/p^2): B^3 = I}
for p in {3,5,7}, WITHOUT enumerating or multiplying any 2x2 matrices --
only via trace/det histogram counting (elementary number theory).

This is the crosscheck (independent implementation) against
search/certs/ss_gap1_pc5_gap_v1_20260813.json, which was produced by GAP
doing brute-force full enumeration with actual matrix multiplication.
Per CLAUDE.md doctrine this script does NOT import GAP code or GAP's
intermediate results -- it only reads GAP's output cert (numbers) at the
end, for comparison. Everything here is reconstructed from scratch.

Derivation used (see spec Sec 4.1, all within SL(2,Z/p^2), so det(A)=1 always):
  A^2=I, A non-scalar  <=>  tr(A)=0 and det(A)=-1  (CH shortcut)
     -- but det(A)=1 is forced (we are inside SL2), so this needs det=-1=1,
        i.e. n | 2 -- impossible for n=p^2, p odd prime >= 3.
        ==> predicted i2_nonscalar = 0 for all p in {3,5,7}.
  A^2=I, A scalar (A=xI): x^2 = 1 (mod n=p^2). For odd p this has exactly 2
        solutions x = +-1 (both give det(xI)=x^2=1, consistent with SL2).
        ==> predicted i2_scalar = 2.
  B^3=I, B non-scalar <=> tr(B)^2=det(B) and tr(B)*det(B)=-1. With det(B)=1
        forced: tr(B)^2=1 => tr(B)=+-1; tr(B)*1=-1 => tr(B)=-1.
        ==> nonscalar solutions = #{B in SL2: tr(B)=-1} (det=1 already forced)
  B^3=I, B scalar (B=xI): x^3=1 and x^2=1 (SL2 det condition) simultaneously
        => x = x^3/x^2 = 1 forced (ring-theoretic cancellation valid since we
           only need x^2=1,x^3=1 as equations, x=x^3 * (x^2)^{-1} needs x^2
           invertible, true since x^2=1). ==> predicted i3_scalar = 1.

count(t, e, n) := #{(a,b,c,d) in (Z/n)^4 : a+d=t (mod n), a*d-b*c=e (mod n)}
is computed via a b*c-value histogram (O(n^2)) then summed over a (O(n)),
total O(n^2) per (t,e,n) query -- no matrix multiplication anywhere.
"""
import json
import hashlib
from pathlib import Path

def bc_histogram(n):
    """hist[k] = #{(b,c) in (Z/n)^2 : b*c == k mod n}"""
    hist = [0] * n
    for b in range(n):
        for c in range(n):
            hist[(b * c) % n] += 1
    return hist

def count_trace_det(t, e, n, hist):
    """count(t,e,n) = sum_a hist[(a*d - e) mod n], d = (t-a) mod n"""
    total = 0
    for a in range(n):
        d = (t - a) % n
        kappa = (a * d - e) % n
        total += hist[kappa]
    return total

def scalar_sqrt1_count(n):
    """#{x in Z/n : x^2 == 1}"""
    return sum(1 for x in range(n) if (x * x) % n == 1)

def scalar_cube_and_square1_count(n):
    """#{x in Z/n : x^2==1 and x^3==1}"""
    return sum(1 for x in range(n) if (x * x) % n == 1 and (x ** 3) % n == 1)

def kernel_mod_p_congI_count(p, n):
    """#{B in SL(2,Z/n): B == I (mod p)} -- the p-congruence kernel.
    For any such B, B = I + p*M for some integer matrix M (mod p), and
    B^3 = I + 3p*M + 3p^2*M^2 + p^3*M^3. Since n=p^2, p^2*(...) == 0 (mod n)
    for the last two terms, so B^3 == I + 3p*M (mod p^2). If p==3 (the
    characteristic-collision case relevant here), 3p*M = 9*M == 0 (mod 9)
    identically, so EVERY element of this kernel satisfies B^3=I regardless
    of M -- a p=3-specific artifact (order tested (3) collides with the
    prime p being reduced). This does not occur for p=5,7 since 3p*M is
    generally nonzero mod p^2 there (order-3 test does not collide with p).
    Computed here by literal enumeration (independent of GAP), not assumed.
    """
    count = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if (a * d - b * c) % n == 1:
                        if a % p == 1 and d % p == 1 and b % p == 0 and c % p == 0:
                            count += 1
    return count

def main():
    primes = [3, 5, 7]
    results = []
    for p in primes:
        n = p * p
        hist = bc_histogram(n)

        # i2: A^2=I within SL2 (det forced =1)
        # nonscalar predicted impossible (needs det=-1=1 mod n, n=p^2 odd prime sq, false)
        i2_nonscalar_pred = 0
        # sanity: also directly count(t=0, e=-1 mod n) to show it is 0 among ALL
        # matrices with det=-1 (not filtered to SL2) minus scalar overlap, as an
        # extra internal check that the CH formula's own combinatorics are sane.
        neg1 = (-1) % n
        count_tr0_detm1 = count_trace_det(0, neg1, n, hist)  # matrices w/ tr=0,det=-1 (not in SL2 since det=-1)
        i2_scalar_pred = scalar_sqrt1_count(n)

        # i3: B^3=I within SL2
        i3_nonscalar_pred = count_trace_det((-1) % n, 1, n, hist)  # tr=-1, det=1
        i3_scalar_pred = scalar_cube_and_square1_count(n)

        # p-congruence-kernel correction term: only computed by literal
        # enumeration when p == 3 (the collision case order-tested==p);
        # for p=5,7 the closed form already matches GAP exactly (see below),
        # so this expensive term is skipped there (documented, not silently
        # assumed to be absent).
        kernel_congI_count = None
        kernel_extra_beyond_identity = None
        if p == 3:
            kernel_congI_count = kernel_mod_p_congI_count(p, n)
            kernel_extra_beyond_identity = kernel_congI_count - 1  # minus B=I itself

        i3_total_pred_corrected = i3_scalar_pred + i3_nonscalar_pred
        if kernel_extra_beyond_identity is not None:
            i3_total_pred_corrected += kernel_extra_beyond_identity

        results.append({
            "p": p,
            "n": n,
            "i2_scalar_pred": i2_scalar_pred,
            "i2_nonscalar_pred": i2_nonscalar_pred,
            "i2_total_pred": i2_scalar_pred + i2_nonscalar_pred,
            "i3_scalar_pred": i3_scalar_pred,
            "i3_nonscalar_pred": i3_nonscalar_pred,
            "i3_total_pred_raw_CH_formula": i3_scalar_pred + i3_nonscalar_pred,
            "kernel_congI_count_p_eq_3_only": kernel_congI_count,
            "kernel_extra_beyond_identity_p_eq_3_only": kernel_extra_beyond_identity,
            "i3_total_pred_corrected": i3_total_pred_corrected,
            "aux_count_tr0_detm1_all_matrices": count_tr0_detm1,
        })

    # load GAP full-enumeration cert for comparison (read-only, cert values only)
    gap_cert_path = Path("search/certs/ss_gap1_pc5_gap_v1_20260813.json")
    gap_data = json.loads(gap_cert_path.read_text(encoding="utf-8"))
    gap_sha256 = hashlib.sha256(gap_cert_path.read_bytes()).hexdigest()
    gap_by_p = {r["p"]: r for r in gap_data["results"]}

    comparison = []
    all_match_raw_CH_formula = True
    all_match_corrected = True
    for r in results:
        p = r["p"]
        g = gap_by_p[p]
        match_i2_total = (r["i2_total_pred"] == g["i2_total"])
        match_i2_scalar = (r["i2_scalar_pred"] == g["i2_scalar"])
        match_i2_nonscalar = (r["i2_nonscalar_pred"] == g["i2_nonscalar"])
        match_i3_total_raw = (r["i3_total_pred_raw_CH_formula"] == g["i3_total"])
        match_i3_total_corrected = (r["i3_total_pred_corrected"] == g["i3_total"])
        match_i3_scalar = (r["i3_scalar_pred"] == g["i3_scalar"])
        row_match_raw = all([match_i2_total, match_i2_scalar, match_i2_nonscalar,
                              match_i3_total_raw, match_i3_scalar])
        row_match_corrected = all([match_i2_total, match_i2_scalar, match_i2_nonscalar,
                                    match_i3_total_corrected, match_i3_scalar])
        all_match_raw_CH_formula = all_match_raw_CH_formula and row_match_raw
        all_match_corrected = all_match_corrected and row_match_corrected
        comparison.append({
            "p": p,
            "closed_form": r,
            "gap_full_enum": g,
            "match_i2_total": match_i2_total,
            "match_i2_scalar": match_i2_scalar,
            "match_i2_nonscalar": match_i2_nonscalar,
            "match_i3_total_raw_CH_formula": match_i3_total_raw,
            "match_i3_total_corrected": match_i3_total_corrected,
            "match_i3_scalar": match_i3_scalar,
            "row_all_match_raw_CH_formula": row_match_raw,
            "row_all_match_corrected": row_match_corrected,
        })

    out = {
        "schema": "ss_gap1_pc5_crosscheck/v1",
        "generated_by": {
            "tool": "python3 (independent implementation, no GAP import)",
            "script": "search/ss_gap1_pc5_crosscheck.py",
            "order": "SS-GAP-1 Stage0 PC-5",
        },
        "method": "trace_det_histogram_closed_form_CH_shortcut_no_matrix_multiplication",
        "input_gap_cert": {
            "path": str(gap_cert_path).replace("\\", "/"),
            "sha256": gap_sha256,
        },
        "comparison": comparison,
        "PC5_all_match_raw_CH_formula_literal": all_match_raw_CH_formula,
        "PC5_all_match_after_p_eq_3_kernel_correction": all_match_corrected,
        "finding": {
            "summary": "p=3 のみ raw CH 閉形式(spec sec4.1 の字義どおり: tr/det 条件のみ)は "
                       "GAP 全数列挙(実際の行列積)と不一致(73 vs 99, 差26)。p=5,7 は完全一致。"
                       "原因を機械的に特定: 差26 は mod 3 で単位行列に合同な SL(2,Z/9) の部分群"
                       "(3-合同核、位数27)のうち B=I 以外の26元。これらは全て trace=2,det=1 の"
                       "非スカラー行列で、B=I+3M(M は mod3 の行列)の形をとり、"
                       "B^3=I+9M+27M^2+27M^3 が n=9=3^2 で 9M≡0(mod9), 27(...)≡0(mod9) となるため"
                       "M に無関係に自動的に B^3=I が成立する — p=3 特有(検定対象の位数3と標数3が"
                       "衝突する場合にのみ起きるアーティファクト)。tr=-1 条件には乗らないため"
                       "raw CH 式では捕捉できない。",
                "root_cause_verified_by": "3rd independent implementation (scratchpad/pc5_p3_diag.py, "
                    "direct matrix multiplication in python, no GAP import) reproduces GAP's 99 exactly "
                    "and confirms all 26 discrepant elements satisfy B==I (mod 3).",
                "relevance_to_target_p_691": "この衝突は「検定対象の位数(2 or 3)」==「還元先の素数 p」の"
                    "ときにのみ起きる。目標 p=691 は 691 not in {2,3} なので、この特定のアーティファクトは"
                    "起きないと予想されるが、これは予想であり本 PC-5 実行では検証していない"
                    "(p=691 は §7 CP-C/CP-D の判定が出るまで触っていない)。★ 数学者/Sol の裁定要:"
                    "spec sec4.1 の閉形式に一般に「p-合同核の補正項」が必要か、それとも "
                    "p != tested-order の場合は不要と証明できるか。",
            "gap_size_p3": None,
        },
        "u_touched": False,
        "c_touched": False,
        "d_no_interpretation": "machine values only; verdict は司令塔",
    }

    out_path = Path("search/certs/ss_gap1_pc5_crosscheck_v1_20260813.json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=None), encoding="utf-8")
    print("PC-5 all_match (raw CH formula, literal spec sec4.1):", all_match_raw_CH_formula)
    print("PC-5 all_match (after documented p=3 kernel correction):", all_match_corrected)
    for c in comparison:
        print(f"p={c['p']}: closed_form_raw i2={c['closed_form']['i2_total_pred']} "
              f"i3={c['closed_form']['i3_total_pred_raw_CH_formula']} "
              f"i3_corrected={c['closed_form']['i3_total_pred_corrected']}  |  "
              f"gap i2={c['gap_full_enum']['i2_total']} i3={c['gap_full_enum']['i3_total']}  "
              f"match_raw={c['row_all_match_raw_CH_formula']} match_corrected={c['row_all_match_corrected']}")
    print("wrote", out_path)

if __name__ == "__main__":
    main()
