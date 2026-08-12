"""
crosscheck/check_s4_fullsweep_3024.py -- ISO-S4 M119-1 解消(裁定944・Sol sol_reply_119 §F2(a) 末尾指定)。

pure Python(GAP 非依存)で S4 窓(PSL(2,8)/N_S4)の**全 3024 候補**((m,f), m in charming_set(6 個)・
f in Gg=[Gg,Gg]=Gg(504 元、PSL(2,8) は単純ゆえ perfect))に対し (3.10)(3.11) hexagon 2 本 + SURJ を
独立に適用し、通過集合を正規化した (m,f) 集合として GAP cert
(search/certs/s4_settled54_v2_20260812.json、その元は search/week3-psl-S4.g の実測)の 54 と集合比較する。
stage counts(h10_fail/h11_fail/generation_fail/shadow_total)も突合する。

群構成(GF(8)・PGL(2,8)・PGammaL(2,8)・Gg=<X,Y>・BFS 正準語・homomorphism well-definedness 判定)は
crosscheck/check_s4_settled54.py の関数を import して流用する(司令塔 裁定944 で明示許可・両者とも
GAP 非依存の独立実装なので流用しても「探索器/照合器」分離は壊れない)。

theta/tau の定義(search/week3-battery-common.g の EnumerateReducedHexagon を GAP コードを読まずに
式だけから独立再実装 -- 式は search/s4_settled54_v1.g の docstring 由来の理解を踏襲):
  theta: x->y, y->x                          (thetaHom)
  tau:   x->y, y->z=(y*x)^{-1}                (tauHom, z := AbstractProd([x,y])^-1 = (y*x)^-1 in GAP form)
  hex310(f)  := theta(f) *_GAP f == I         (AbstractProd([f,thetaf]) の reversal)
  ymf(m,f)   := f *_GAP y^m                   (AbstractProd([y^m,f]) の reversal)
  hex311     := ymf *_GAP tau(ymf) *_GAP tau(tau(ymf)) == I  (AbstractProd([tau2,tau1,ymf]) の reversal)
  genA := x^u, genB := f *_GAP y^u *_GAP f^-1  (AbstractProd([f^-1,y^u,f]) の reversal, 既に
          check_s4_settled54.py で検算済みの式)
  surj := <genA,genB> = Gg

"perm_mul(p,q)" は本ファイル・check_s4_settled54.py 双方で GAP の p*q 規約(「p を適用してから q」)を
模した自前実装であり、AbstractProd の reversal 規約と組み合わせて上式が導かれる。
"""
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, "crosscheck")
from check_s4_settled54 import (  # noqa: E402
    IDENT, X, Y, Gg, word_of_Gg, aut_elts,
    perm_mul, perm_pow, perm_inv, eval_word,
    is_homomorphism_well_defined_and_kernel, generates_full_Gg,
    charming_set_independent, nOrd,
)

CERT_PATH = "search/certs/s4_settled54_v2_20260812.json"
OUT_PATH = "search/certs/s4_fullsweep_python_v1_20260812.json"

FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("[FAIL]", msg)


def ok(msg):
    print("[OK]", msg)


def main():
    # ---- build theta, tau as genuine (well-definedness-tested) homomorphisms on Gg ----
    theta_wd, _theta_ksize, theta_F = is_homomorphism_well_defined_and_kernel(Y, X)  # x->y, y->x
    zElt = perm_inv(perm_mul(Y, X))  # (y*x)^-1 in GAP-style product, matches AbstractProd([x,y])^-1
    tau_wd, _tau_ksize, tau_F = is_homomorphism_well_defined_and_kernel(Y, zElt)  # x->y, y->z
    if not theta_wd:
        fail("theta (x->y,y->x) is not a well-defined homomorphism on Gg -- unexpected, halting")
        print("\n".join(FAILS))
        sys.exit(1)
    if not tau_wd:
        fail("tau (x->y,y->z) is not a well-defined homomorphism on Gg -- unexpected, halting")
        print("\n".join(FAILS))
        sys.exit(1)
    ok(f"theta well-defined on Gg (504 elements): {theta_wd}")
    ok(f"tau well-defined on Gg (504 elements): {tau_wd}")

    Gg_list = list(Gg)
    charming = charming_set_independent
    assert len(charming) == 6, len(charming)
    assert len(Gg_list) == 504, len(Gg_list)

    candidate_total = 0
    h10_fail = 0
    h11_fail = 0
    generation_fail = 0
    shadow_pass = []  # list of (m, f) permutation tuples that pass all 3 checks

    for m in charming:
        u = 2 * m + 1
        y_m = perm_pow(Y, m)
        y_u = perm_pow(Y, u)
        genA = perm_pow(X, u)
        for f in Gg_list:
            candidate_total += 1
            thetaf = theta_F[f]
            hex310 = (perm_mul(thetaf, f) == IDENT)
            if not hex310:
                h10_fail += 1
                continue
            ymf = perm_mul(f, y_m)
            tau1 = tau_F[ymf]
            tau2 = tau_F[tau1]
            hex311 = (perm_mul(perm_mul(ymf, tau1), tau2) == IDENT)
            if not hex311:
                h11_fail += 1
                continue
            genB = perm_mul(perm_mul(f, y_u), perm_inv(f))
            surj = generates_full_Gg(genA, genB)
            if not surj:
                generation_fail += 1
                continue
            shadow_pass.append((m, f))

    shadow_total = len(shadow_pass)
    print(f"[RAW] candidate_total={candidate_total} h10_fail={h10_fail} h11_fail={h11_fail} "
          f"generation_fail={generation_fail} shadow_total={shadow_total}")
    sum_check = (candidate_total - h10_fail - h11_fail - generation_fail == shadow_total)
    print(f"[RAW] stage-count sum check: {sum_check}")
    if not sum_check:
        fail("stage counts do not sum to candidate_total")

    # ---- load GAP cert's 54 and reconstruct f from f_word using the SAME (X,Y) ----
    with open(CERT_PATH, encoding="utf-8") as fh:
        cert = json.load(fh)
    detail = cert["b_kernel_equality"]["detail"]
    cert_shadow_total = cert["b_kernel_equality"]["shadow_total"]

    def reconstruct_f(f_word):
        return eval_word([(l[0], l[1]) for l in f_word], X, Y)

    cert_set = set((entry["m"], reconstruct_f(entry["f_word"])) for entry in detail)
    python_set = set(shadow_pass)

    print(f"[RAW] |cert_set|={len(cert_set)} (cert shadow_total={cert_shadow_total}) "
          f"|python_fullsweep_set|={len(python_set)}")

    only_in_cert = cert_set - python_set
    only_in_python = python_set - cert_set
    sets_equal = (cert_set == python_set)
    print(f"[RAW] sets_equal={sets_equal} only_in_cert={len(only_in_cert)} only_in_python={len(only_in_python)}")
    if not sets_equal:
        fail(f"set mismatch: only_in_cert={len(only_in_cert)} only_in_python={len(only_in_python)}")

    # ---- cross-reference against the GAP run's own printed stage counts (S4 window, this session) ----
    # GAP run (search/s4_settled54_v1.g via RunPSLWindow) printed:
    #   candidate_total=3024 h10_fail=2640 h11_fail=330 generation_fail=0 shadow_total=54
    gap_stage_counts = {"candidate_total": 3024, "h10_fail": 2640, "h11_fail": 330,
                         "generation_fail": 0, "shadow_total": 54}
    python_stage_counts = {"candidate_total": candidate_total, "h10_fail": h10_fail,
                            "h11_fail": h11_fail, "generation_fail": generation_fail,
                            "shadow_total": shadow_total}
    stage_counts_agree = (gap_stage_counts == python_stage_counts)
    print(f"[RAW] gap_stage_counts={gap_stage_counts}")
    print(f"[RAW] python_stage_counts={python_stage_counts}")
    print(f"[RAW] stage_counts_agree={stage_counts_agree}")
    if not stage_counts_agree:
        fail("stage counts (h10_fail/h11_fail/generation_fail/shadow_total) disagree with GAP run log")

    # ---- write cert ----
    out = {
        "schema": "s4-fullsweep-python/v1",
        "generated_by": {"tool": "python (pure, GAP-independent)",
                          "script": "crosscheck/check_s4_fullsweep_3024.py",
                          "task": "ISO-S4 M119-1 (裁定944, Sol sol_reply_119 §F2(a) 末尾)"},
        "reused_from": {
            "group_construction": "crosscheck/check_s4_settled54.py (GF(8)/PGL(2,8)/PGammaL(2,8)/Gg/BFS/"
                                    "homomorphism-well-definedness routines, imported directly per 裁定944)",
            "note": "both this file and check_s4_settled54.py are from-scratch pure-Python "
                    "reimplementations independent of GAP; reuse between them does not import any "
                    "search/*.g code or GAP output beyond the final cert being compared against"},
        "theta_tau_well_defined": {"theta": theta_wd, "tau": tau_wd},
        "sweep": {
            "charming_set_size": len(charming), "gg_size": len(Gg_list),
            "candidate_total": candidate_total, "h10_fail": h10_fail, "h11_fail": h11_fail,
            "generation_fail": generation_fail, "shadow_total": shadow_total,
            "stage_count_sum_check": sum_check,
        },
        "comparison_vs_gap_cert": {
            "gap_cert_path": CERT_PATH,
            "gap_cert_shadow_total": cert_shadow_total,
            "python_shadow_total": shadow_total,
            "sets_equal": sets_equal,
            "only_in_cert_count": len(only_in_cert),
            "only_in_python_count": len(only_in_python),
        },
        "comparison_vs_gap_run_log_stage_counts": {
            "gap_stage_counts": gap_stage_counts,
            "python_stage_counts": python_stage_counts,
            "agree": stage_counts_agree,
        },
        "all_checks_pass": (len(FAILS) == 0),
    }
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"\nwrote {OUT_PATH}")

    if FAILS:
        print(f"\n{len(FAILS)} check(s) FAILED:")
        for m in FAILS:
            print(" -", m)
        sys.exit(1)
    print("\nAll checks: raw agreement (3024 full sweep matches GAP cert's 54, no verdict language).")
    sys.exit(0)


if __name__ == "__main__":
    main()
