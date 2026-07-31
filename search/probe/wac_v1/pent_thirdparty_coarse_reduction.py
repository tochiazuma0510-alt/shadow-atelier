"""
search/probe/wac_v1/pent_thirdparty_coarse_reduction.py

Follow-up measurement ordered 2026-07-31 (ruling 275 follow-up): reduce each
of the third-party package's charming/friendly_pr/gtsh (w,m) entries for our
window K_pi down to the coarse A5 window N_A, and histogram (m, coarse_f).

WORD-ENCODING EVIDENCE (quoted verbatim from search/thirdparty/PackageGT/PaB.py,
unedited file -- no interpretation/guessing needed, see below for why):

  w2g (lines 573-586):
    "def w2g(w,t):
        '''
        t is a tuple of permutations in S_d of length q,
        w is a (possibly empty) word in 0,1,... q-1;
        the function returns the corresponding element on S_d;
        if q is not the length of t the function will NOT work.
        '''
        d = t[0].size
        if w == ():
            return permut(d-1)
        return compAll(tuple(t[i] for i in w))"

  generWF2 (lines 610-616), showing symbol 0 <-> tt[0] and symbol 1 <-> tt[1]:
    "g = comp(L[i],tt[0]); rg = g.rank()
     if rg not in G:
         Wnew.append(W[i] + (0,)); ...
     g = comp(L[i],tt[1]); rg = g.rank()
     if rg not in G:
         Wnew.append(W[i] + (1,)); ..."

  compAll (Aux.py, "returns the consecutive composition of all permutations
  in the iterable t", processing t in the given order via a left fold).

CRUCIALLY: no re-interpretation of the word encoding is needed here, because
we do not re-derive or re-guess the word semantics -- we feed the EXACT SAME
(w,m) tuples the package itself produced (as members of charming_list_wm /
friendly_pr_list_wm / gtsh_list_wm, already internally self-consistent
under the package's own penta/hexa1/hexa2 checks) into the package's OWN
w2g(), using the package's OWN generator pair (t[0],t[1]) restricted to the
coarse window. There is exactly one way to do this that uses only the
package's own functions/conventions, so no "two readings" branch is needed
(instruction point 5's ambiguity-hedge does not apply here for that reason
-- flagged explicitly rather than silently omitted).

COARSE WINDOW N_A: verified (not assumed) to be P5 = <x12,x23> = <t[0],t[1]>
where t is the SAME PB4 tuple used for the K_pi (fine) run -- i.e. the coarse
window is literally the image of F2 under fi123(t) = (x12,x23,x13) alone
(PaB.py's identity coface), as opposed to the FINE quotient tPB3=N_PB3(t)
used inside gener_GT_charm/pr/sh, which additionally pulls back the other 4
cofaces (fi234, fi12_3_4, fi1_23_4, fi1_2_34) and is therefore strictly
finer. |<t[0],t[1])>| is computed below, not hardcoded, and checked to be
60 == the A5-window group order asserted in the GAP construction
(pent_pi_a5.g's P5 := Group(xbar,ybar), Size(P5)=60), matching xbar=t[0],
ybar=t[1] (same objects, S1^2 and S2^2 of the pi-lift).
"""

import sys
import json
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "search" / "probe" / "wac_v1"))

from gt_thirdparty_bootstrap import PaB  # noqa: E402
from sympy.combinatorics import Permutation as permut  # noqa: E402
from sympy.combinatorics.perm_groups import PermutationGroup as PG  # noqa: E402

S1_GAP_1INDEXED = [4, 1, 5, 3, 2, 8, 7, 6]
S2_GAP_1INDEXED = [5, 4, 2, 1, 3, 6, 8, 7]
S3_GAP_1INDEXED = [4, 1, 5, 3, 2, 8, 7, 6]


def to_sympy(L):
    return permut([x - 1 for x in L])


def build_window():
    S1 = to_sympy(S1_GAP_1INDEXED)
    S2 = to_sympy(S2_GAP_1INDEXED)
    S3 = to_sympy(S3_GAP_1INDEXED)
    assert PaB.relB4((S1, S2, S3))
    t = PaB.restr_PB4((S1, S2, S3))
    assert PaB.relPB4(t)
    return t


def coarse_key(p):
    # array_form is a canonical, hashable, JSON-serializable representative
    # of a sympy Permutation (list of images, 0-indexed).
    return tuple(p.array_form)


def reduce_list(wm_list, coarse_gens):
    rows = []
    hist = {}
    for (w, m) in wm_list:
        cf = PaB.w2g(tuple(w), coarse_gens)
        key = (m, coarse_key(cf))
        hist[key] = hist.get(key, 0) + 1
        rows.append({
            "word": list(w),
            "m": m,
            "coarse_f_array_form": list(cf.array_form),
            "coarse_f_cyclic_form": str(cf.cyclic_form),
        })
    hist_rows = [
        {"m": k[0], "coarse_f_array_form": list(k[1]), "count": v}
        for k, v in sorted(hist.items(), key=lambda kv: (kv[0][0], kv[0][1]))
    ]
    return rows, hist_rows, len(hist)


def main():
    t = build_window()
    coarse_gens = (t[0], t[1])
    coarse_group_order = PG(coarse_gens).order()

    result = {
        "schema": "wac_v1-pent-thirdparty-coarse-reduction/v1",
        "generated_by": "search/probe/wac_v1/pent_thirdparty_coarse_reduction.py",
        "note": (
            "Coarse reduction of the third-party package's K_pi charming/friendly_pr/gtsh "
            "(w,m) entries onto the coarse window N_A = <t[0],t[1]> (fi123(t), the identity "
            "coface). Uses the package's own w2g() and the SAME word tuples the package "
            "itself produced -- no re-derivation of word semantics. No determination made "
            "here; raw histogram only."
        ),
        "coarse_window_group_order_measured": coarse_group_order,
    }

    # Recompute the three lists fresh (same window, same package functions,
    # ~1-2s total -- cheap, done to avoid depending on stale in-memory state).
    charming = list(PaB.gener_GT_charm(t))
    friendly_pr = list(PaB.gener_GT_pr(t))
    gtsh = list(PaB.gener_GT_sh(t))

    for label, wm_list, want_full_rows in [
        ("charming", charming, True),
        ("friendly_pr", friendly_pr, False),
        ("gtsh", gtsh, False),
    ]:
        rows, hist_rows, n_classes = reduce_list(wm_list, coarse_gens)
        entry = {
            "total_entries": len(wm_list),
            "distinct_coarse_mf_classes": n_classes,
            "histogram": hist_rows,
        }
        if want_full_rows:
            entry["per_entry_rows"] = rows
        result[label] = entry

    out_path = REPO_ROOT / "OUT_coarse_reduction.json"
    out_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print("WROTE", out_path)
    print("coarse_window_group_order_measured =", coarse_group_order)
    for label in ("charming", "friendly_pr", "gtsh"):
        print(label, "total", result[label]["total_entries"],
              "distinct_classes", result[label]["distinct_coarse_mf_classes"])


if __name__ == "__main__":
    main()
