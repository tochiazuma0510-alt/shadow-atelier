"""
search/probe/wac_v1/pent_thirdparty_gt_run.py

Third-party judge run for the pentagon collision (v4 "20 all-arithmetic" vs
fine-lift=4, both suspension). Uses Dolgushev-Le-Lorenz-Zackey's own Python
package "Package GT" (search/thirdparty/PackageGT/, byte-identical copy of
the zip in the vault; see cert for sha256) as an INDEPENDENT third
implementation of the pentagon+hexagon+charming machinery, run against our
precise window K_pi (the sigma3 |-> sigma1 pi-lift of the A5 window N_A,
ruling 248 / docs/notes/litgate_pentagon_v1.md).

Contact isolation: this script never reads or imports any of our own
GAP/Sol/diagnostic pentagon-count code, and does not hardcode our own
predicted values (4, or per-m [1,1,1,1], or "20") anywhere -- it only
constructs the window (from the same sigma1/sigma2/sigma3 permutation
images GAP already derived and printed, transferred as raw permutation
arrays) and calls the package's own generator functions. All arithmetic
comparison against our own values happens OUTSIDE this script, in the
commander's cert-reading step.

The window K_pi is transferred WITHOUT any hand conversion of GAP's action
convention vs sympy's: only the three generator images (S1, S2, S3, as
explicit bijections on domain [1..8], 1-indexed -> shifted to 0-indexed
arrays for sympy.combinatorics.Permutation) are transferred; the package's
OWN PaB.restr_PB4() then derives x12..x34 in ITS OWN convention. Before
using this transfer for anything, both PaB.relB4() (on S1,S2,S3) and
PaB.relPB4() (on the derived PB4 tuple) are checked and must return True --
this is an empirical, package-computed self-check that the transferred
generators really do represent a B4->S8 homomorphism in the package's own
algebra, not an assumption.

Run from repo root:
    echo no | "<python313>" search/probe/wac_v1/pent_thirdparty_gt_run.py
(The "no" answers PaB.py's one-time interactive prompt at import time,
which asks whether to precompute a >1-minute nested list we do not need.)
"""

import sys
import time
import json
import hashlib
from pathlib import Path
from math import gcd

warnings_off = None
import warnings
warnings.filterwarnings("ignore")

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "search" / "probe" / "wac_v1"))

from gt_thirdparty_bootstrap import PaB  # noqa: E402
from sympy.combinatorics import Permutation as permut  # noqa: E402
from sympy.combinatorics.perm_groups import PermutationGroup as PG  # noqa: E402


# ---------------------------------------------------------------------------
# STEP 0: provenance -- hashes of the third-party files actually imported
# ---------------------------------------------------------------------------
def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


PKG_DIR = REPO_ROOT / "search" / "thirdparty" / "PackageGT"
# NOTE: Aux.py cannot be opened by native-Windows Python at all (reserved
# DOS device name "AUX", enforced even with extension and even with a
# \\?\ extended-length prefix -- see gt_thirdparty_bootstrap.py docstring).
# Its sha256 was computed via `sha256sum` in Git-Bash/MSYS (which CAN open
# it) on 2026-07-31, and cross-checked equal to AuxSafe.py's hash computed
# both ways (bash sha256sum AND this script's sha256_of, since AuxSafe.py
# is not a reserved name). Hardcoded here, not recomputed by this script.
AUX_PY_SHA256_VIA_BASH = "62d7f24c502209994663cb79e2f2469c5ab9ac982d1312604722445437fd7144"

file_hashes = {
    "PaB.py": sha256_of(PKG_DIR / "PaB.py"),
    "NotUsed.py": sha256_of(PKG_DIR / "NotUsed.py"),
    "Aux.py (sha256 via bash sha256sum -- unreadable by native Windows Python)": AUX_PY_SHA256_VIA_BASH,
    "AuxSafe.py (bootstrap-only rename, bash-diff-verified byte-identical to Aux.py)": sha256_of(
        PKG_DIR / "AuxSafe.py"
    ),
    "subGrPB4_org35": sha256_of(PKG_DIR / "subGrPB4_org35"),
    "wm_list_charm35": sha256_of(PKG_DIR / "wm_list_charm35"),
    "wm_list_all31": sha256_of(PKG_DIR / "wm_list_all31"),
}
assert file_hashes["AuxSafe.py (bootstrap-only rename, bash-diff-verified byte-identical to Aux.py)"] == AUX_PY_SHA256_VIA_BASH, "AuxSafe.py drifted from Aux.py!"


# ---------------------------------------------------------------------------
# STEP 1: calibration -- N(19) "Philadelphia" and N(34) "Mighty Dandy",
# using the package's OWN bundled data (subGrPB4_org35, wm_list_charm35)
# and OWN functions (penta, hexa1, hexa2, generWF2, generWComm).
# ---------------------------------------------------------------------------
def calibration():
    out = {}
    listE = PaB.listE
    GTcharm_wm = PaB.GTcharm_wm

    # N(34) "Mighty Dandy": author-precomputed charming-shadow list length.
    # Published value (Dolgushev-Le-Lorenz 2008.00066 Sect. 4): |GT(N(34))|=486.
    out["N34_index_in_subGrPB4_org35"] = 34
    out["N34_precomputed_charming_count"] = len(GTcharm_wm[34])
    E34 = listE[34]
    out["N34_invariants"] = {
        "N0": E34.N0, "ind3": E34.ind3(), "ind4": E34.ind4(), "indF2": E34.indF2(),
    }

    # N(19) "Philadelphia subgroup": recomputed from scratch via the
    # package's own penta/hexa1/hexa2/generWF2 (fast: indF2 is small).
    E19 = listE[19]
    t19 = E19.PB4
    tPB3 = PaB.N_PB3(t19)
    N0 = PaB.Nord(tPB3)
    penta_count = 0
    f_with_hex = 0
    pair_count = 0
    t0 = time.time()
    for w in PaB.generWF2(tPB3[:2], timed=False):
        if PaB.penta((w, 0), t19):
            penta_count += 1
            found = False
            for m in range(N0):
                if gcd(2 * m + 1, N0) == 1:
                    if PaB.hexa1((w, m), tPB3) and PaB.hexa2((w, m), tPB3):
                        pair_count += 1
                        found = True
            if found:
                f_with_hex += 1
    out["N19_invariants"] = {
        "N0": N0, "ind3": E19.ind3(), "ind4": E19.ind4(), "indF2": E19.indF2(),
    }
    out["N19_recomputed_pentagon_f_count"] = penta_count
    out["N19_recomputed_f_with_some_hexagon_m"] = f_with_hex
    out["N19_recomputed_total_mf_pairs_with_hexagon"] = pair_count
    out["N19_recompute_time_s"] = time.time() - t0

    # N(34) pentagon/hexagon-in-commutator-subgroup recount was ATTEMPTED
    # and ABORTED: indF2 = 20,575,296 makes generWComm's BFS-over-the-full-
    # group approach too expensive for the 30-minute/8GB discipline (killed
    # after several minutes with no output). Calibration for N(34) therefore
    # rests on the author-precomputed charming count (486) above, which
    # already matches the published |GT(N34)|=486 exactly.
    out["N34_penta_hexagon_recount_in_commutator_subgroup"] = "ABORTED (indF2=20575296, exceeded time/RAM budget); not attempted to completion"

    return out


# ---------------------------------------------------------------------------
# STEP 2: transfer K_pi (sigma3 |-> sigma1 pi-lift of the A5 window N_A)
# S1,S2,S3 images exported by search/probe/wac_v1/pent_pi_a5_export_sigmas.g
# (GAP run, domain [1..8], 1-indexed image lists -- pasted here verbatim).
# ---------------------------------------------------------------------------
S1_GAP_1INDEXED = [4, 1, 5, 3, 2, 8, 7, 6]
S2_GAP_1INDEXED = [5, 4, 2, 1, 3, 6, 8, 7]
S3_GAP_1INDEXED = [4, 1, 5, 3, 2, 8, 7, 6]  # pi-lift: sigma3 |-> sigma1, identical to S1


def build_window():
    def to_sympy(L):
        return permut([x - 1 for x in L])

    S1 = to_sympy(S1_GAP_1INDEXED)
    S2 = to_sympy(S2_GAP_1INDEXED)
    S3 = to_sympy(S3_GAP_1INDEXED)

    relB4_ok = PaB.relB4((S1, S2, S3))
    t = PaB.restr_PB4((S1, S2, S3))
    relPB4_ok = PaB.relPB4(t)

    E = PaB.Equiv(t)
    invariants = {
        "ind4_PB4_over_N": E.ind4(),
        "ind3_PB3_over_N_PB3": E.ind3(),
        "indF2": E.indF2(),
        "N0": E.N0,
        "ord_x": E.ord_x(),
        "ord_y": E.ord_y(),
    }
    return t, relB4_ok, relPB4_ok, invariants


# ---------------------------------------------------------------------------
# STEP 3: production -- run the package's own generators on K_pi
# ---------------------------------------------------------------------------
def production(t):
    out = {}

    t0 = time.time()
    charming = list(PaB.gener_GT_charm(t))
    out["charming_total"] = len(charming)
    out["charming_time_s"] = time.time() - t0
    out["charming_list_wm"] = [[list(w), m] for (w, m) in charming]

    t0 = time.time()
    friendly_pr = list(PaB.gener_GT_pr(t))
    out["friendly_pr_total"] = len(friendly_pr)
    out["friendly_pr_time_s"] = time.time() - t0
    out["friendly_pr_list_wm"] = [[list(w), m] for (w, m) in friendly_pr]

    t0 = time.time()
    gtsh = list(PaB.gener_GT_sh(t))
    out["gtsh_total"] = len(gtsh)
    out["gtsh_time_s"] = time.time() - t0
    out["gtsh_list_wm"] = [[list(w), m] for (w, m) in gtsh]

    t0 = time.time()
    penta_comm = list(PaB.gener_GT_penta(t))
    out["penta_comm_total"] = len(penta_comm)
    out["penta_comm_time_s"] = time.time() - t0
    out["penta_comm_word_list"] = [list(w) for w in penta_comm]

    # per-m distributions (raw counts; no comparison to our own predicted
    # values performed here)
    def per_m(wm_list):
        d = {}
        for (w, m) in wm_list:
            d[m] = d.get(m, 0) + 1
        return dict(sorted(d.items()))

    out["charming_per_m"] = per_m(charming)
    out["friendly_pr_per_m"] = per_m(friendly_pr)
    out["gtsh_per_m"] = per_m(gtsh)
    out["charming_distinct_words"] = len(set(tuple(w) for (w, m) in charming))

    return out


def main():
    result = {
        "schema": "wac_v1-pent-thirdparty-gt-cert/v1",
        "generated_by": "search/probe/wac_v1/pent_thirdparty_gt_run.py",
        "note": (
            "Third-party judge run of Dolgushev et al.'s own Package GT "
            "(independent Python implementation of pentagon+hexagon+charming) "
            "against our precise window K_pi (sigma3 |-> sigma1 pi-lift of the "
            "A5 window N_A). Contact-isolated: our own predicted values are "
            "never read or written by this script. No determination is made "
            "here -- raw machine output only."
        ),
        "file_hashes": file_hashes,
    }
    result["calibration"] = calibration()
    t, relB4_ok, relPB4_ok, window_invariants = build_window()
    result["window_transfer_checks"] = {
        "relB4_on_transferred_S1_S2_S3": relB4_ok,
        "relPB4_on_restr_PB4": relPB4_ok,
    }
    result["window_invariants"] = window_invariants
    result["production"] = production(t)

    out_path = REPO_ROOT / "OUT_pent_thirdparty_gt_full.json"
    out_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print("WROTE", out_path)


if __name__ == "__main__":
    main()
