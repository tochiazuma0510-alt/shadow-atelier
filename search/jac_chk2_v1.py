#!/usr/bin/env python3
"""
*** DEPRECATED / TOOL-CHOICE ERROR (裁定806) -- DO NOT RUN AS-IS FOR p>=17 ***
This script's exact-sympy-rational rank/nullspace approach was ruled a tool-choice error by
the commander for p in {17,19} (Witt(2,19)=27,594-dim Lambda_19 does not scale under exact
rational Gaussian elimination). A local attempt at p=17 alone ran for >1.5 hours without
completing before the process was killed (plausibly OOM on the 8GB local machine). Superseded
by search/jac_chk2_modq_v1.py (mod-q two-prime rank + RREF-pivot-shortcut character trace,
dispatched via .github/workflows/jac-chk2-modq.yml on GHA per 裁定806/807/808). Retained here
UNMODIFIED as an honest record of the attempted method and its real cost (per this project's
自誤申告 discipline) -- not as a script anyone should re-run for p>=17 without first reading
search/jac_chk2_modq_v1.py's module docstring.

search/jac_chk2_v1.py -- JAC-CHK-2 (docs/notes/post_lazard_window_design_v1_addendum_c.md
§2.1, 発注 by the addendum's author, queued via 裁定795-4/796/798 as "PL-LAB-2" then
corrected by the commander to be exactly this order -- addendum C supersedes addendum B's
closed-form candidate, and search/jac_chk_v1.py's own p=5,7,11,13 measurements are already
the addendum C §1.3 table's 4/4 match; this script extends the SAME method to p=17,19).

Reuses the p=5..13 script's machinery UNCHANGED (word_bracket/build_jacobson_s/
apply_substitution/theta_apply/tau_apply/solve_isotypic/factorize_and_check) -- imported
directly from search/jac_chk_v1.py rather than copy-pasted, since this is the SEARCH side
reusing its own prior search-side code (not a search/crosscheck boundary; the crosscheck/
checker below is the independent side and does NOT import either file).

New in this script: the addendum C §1.3/§2.1 prediction comparison, which SUPERSEDES the
old JAC-R candidate (triv+sgn+(p-3)/2 std) used by jac_chk_v1.py -- for p=17,19 the frozen
prediction (P-PL-5'a) is:
    m_triv = m_sgn = round(p/6),  m_std = floor((p-1)/3)
  p=17 -> (3,3,5) ;  p=19 -> (3,3,6)
STOP condition per addendum C §2.1: "dim < p-1 が出たら即停止・報告" (dim_R_p < p-1, i.e.
s_1..s_{p-1} linearly DEPENDENT) -- same STOP discipline as jac_chk_v1.py, re-applied here.
p=23 (Witt(2,23)=364,722) is explicitly OUT OF SCOPE per addendum C's own RAM-8GB caution;
NOT attempted here.

No verdict language. Raw dims/isotypic multiplicities/booleans only.
"""
import json
import sys
import time

sys.path.insert(0, "search")
from jac_chk_v1 import factorize_and_check  # search-side reuse of search-side code (not crosscheck)


def round_half_up(x):
    # round(p/6) per addendum C ("round" convention, p never lands on .5 for
    # integer p not divisible by 3, so this is unambiguous for our inputs)
    import math
    return math.floor(x + 0.5)


def main():
    per_p = {}
    timings = {}
    for p in [17, 19]:
        t0 = time.time()
        r = factorize_and_check(p)
        t1 = time.time()
        timings[p] = t1 - t0
        per_p[p] = r
        if r["stop_code"] is not None:
            print(f"p={p}: STOP {r['stop_code']} -- rank={r['rank_span_s_i']} != p-1={p-1} "
                  f"(elapsed={t1-t0:.1f}s)", flush=True)
        else:
            print(f"p={p}: rank={r['rank_span_s_i']} (=p-1: {r['linearly_independent']}) "
                  f"isotypic={r['isotypic']} (elapsed={t1-t0:.1f}s)", flush=True)

    any_stop = any(r["stop_code"] is not None for r in per_p.values())

    # addendum C §1.3 P-PL-5'a prediction (supersedes jac_chk_v1.py's old JAC-R
    # (p-3)/2 comparison, which addendum C itself flagged as reverted for p>=11)
    ppl5a_comparison = {}
    for p in [17, 19]:
        r = per_p[p]
        pred_triv_sgn = round_half_up(p / 6)
        pred_std = (p - 1) // 3
        if r["stop_code"] is None:
            m = r["isotypic"]
            ppl5a_comparison[p] = {
                "predicted": {"m_triv": pred_triv_sgn, "m_sgn": pred_triv_sgn, "m_std": pred_std},
                "measured": m,
                "matches_P_PL_5a": (m["m_triv"] == pred_triv_sgn and m["m_sgn"] == pred_triv_sgn
                                     and m["m_std"] == pred_std),
            }
        else:
            ppl5a_comparison[p] = {
                "predicted": {"m_triv": pred_triv_sgn, "m_sgn": pred_triv_sgn, "m_std": pred_std},
                "measured": None,
                "matches_P_PL_5a": None,
            }

    dim_all_equal_p_minus_1 = all(per_p[p]["linearly_independent"] for p in [17, 19])
    ppl5a_matches_all = all(
        ppl5a_comparison[p]["matches_P_PL_5a"] is True for p in [17, 19]
    )

    out = {
        "schema": "shadow-atelier/jac_chk2_v1",
        "authority": "裁定795-4/796/798 (queued as \"PL-LAB-2\", corrected by 司令塔 to this "
                     "exact order per implementer's spec cross-check) -- "
                     "docs/notes/post_lazard_window_design_v1_addendum_c.md §2.1 発注 JAC-CHK-2",
        "method_note": "IDENTICAL method to search/jac_chk_v1.py (p=5,7,11,13; reused via direct "
                       "import, not copy-paste) -- pure Lie-algebra Jacobson p-power formula "
                       "s_1..s_{p-1} in Lambda_p, NO group construction, NO ANUPQ/pc-group "
                       "machinery (addendum C explicitly notes ANUPQ/群構成 is NOT used for "
                       "this order; the group-side NORM-CHK-2 (11^412 generators) remains an "
                       "explicit UNKNOWN the addendum's own author declines to attempt).",
        "scope_note": "p=17,19 only. p=23 (dim Lambda_23 = Witt(2,23) = 364,722) explicitly "
                      "OUT OF SCOPE per addendum C's RAM-8GB caution -- not attempted.",
        "per_p": {str(p): v for p, v in per_p.items()},
        "timings_sec": {str(p): timings[p] for p in [17, 19]},
        "any_stop": any_stop,
        "P_PL_5a_prediction_formula": {"m_triv": "round(p/6)", "m_sgn": "round(p/6)",
                                        "m_std": "floor((p-1)/3)"},
        "P_PL_5a_comparison": {str(p): v for p, v in ppl5a_comparison.items()},
        "summary_raw": {
            "dim_R_p_equals_p_minus_1_both": dim_all_equal_p_minus_1,
            "P_PL_5a_matches_both": ppl5a_matches_all,
            "note": "dim R_p=p-1 (linear independence of s_1..s_{p-1}, the [PLB-GAP-1] "
                    "residual open item per addendum C §5) and the isotypic type "
                    "(m_triv,m_sgn,m_std) vs addendum C §1.3's predicted "
                    "(round(p/6),round(p/6),floor((p-1)/3)) are reported raw above.",
        },
        "no_verdict_note": "raw dimensions, isotypic multiplicities, and booleans only. No "
                           "judgment words -- 発効は司令塔専権.",
        "stop_code": "JAC_CHK2_LINEARLY_DEPENDENT_SOMEWHERE" if any_stop else None,
    }
    out_path = "search/certs/jac_chk2_v1_20260811.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"any_stop={any_stop}")


if __name__ == "__main__":
    main()
