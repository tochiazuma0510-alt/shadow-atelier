#!/usr/bin/env python3
"""
c8_packagegt_crosscheck.py -- CAL-B4 C-8 (Package GT `penta` cross-check),
Linux-only job. On Windows/Git-Bash this repo's local environment cannot
import search/thirdparty/PackageGT/PaB.py: its sibling module Aux.py collides
with the Windows-reserved device name "AUX" (CON/PRN/AUX/NUL/COM1-9/LPT1-9),
causing `import Aux` to raise ModuleNotFoundError despite the file being
present (confirmed via os.listdir() showing the file while import fails).
GHA's ubuntu-latest runner has no such reserved-name restriction, so this
script is dispatched as a separate Linux job in .github/workflows/b4-cal.yml
rather than attempted locally.

Cross-checks the N19 (Philadelphia) row of PackageGT's own pre-loaded
35-window inventory (listE[19]) against the paper's Table 1 values AND
against this repo's independently-derived GAP values (search/probe/
b4_cal_v1/cal_b4_n19_pentagon.g), using PackageGT's OWN pentagon-evaluator
(`penta`) and word generator (`generWComm`) -- not a reimplementation, a
genuine independent third-party check.
"""
import sys
import builtins

# PaB.py's top-level code prompts interactively at import time ("Please type
# yes if you want to form the nested list GTcharm..."); patch input() to
# decline (that branch takes >1 minute per PaB.py's own warning and is not
# needed for this check).
builtins.input = lambda *a, **k: 'no'

try:
    import PaB  # noqa: E402  (import after builtins patch, deliberate)
except ModuleNotFoundError as e:
    print(f"C8_FAIL: PaB import failed even on Linux: {e}")
    sys.exit(1)


def main():
    all_ok = True

    n_entries = len(PaB.listE)
    print(f"len(listE) = {n_entries} (expect 35)")
    if n_entries != 35:
        all_ok = False

    E19 = PaB.listE[19]
    ind4 = E19.ind4()
    indF2 = E19.indF2()
    N0 = E19.N0
    commF2 = E19.commF2()

    print(f"E19.ind4()   = {ind4}   (expect 216, = |PB4:N19|)")
    print(f"E19.indF2()  = {indF2}  (expect 7776, = |F2:N_F2|)")
    print(f"E19.N0       = {N0}     (expect 6, N_ord)")
    print(f"E19.commF2() = {commF2} (expect 216, |[F2/N,F2/N]|)")

    checks = {
        "ind4=216": ind4 == 216,
        "indF2=7776": indF2 == 7776,
        "N0=6": N0 == 6,
        "commF2=216": commF2 == 216,
    }
    for name, ok in checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
        all_ok = all_ok and ok

    # Independent pentagon count via PackageGT's OWN penta()+generWComm()
    # (not our GAP reimplementation, not our reordered/inverted psi -- this
    # is PackageGT's own N19 realization end to end).
    print("\nCounting pentagon-satisfying words via PackageGT's own "
          "generWComm(E19.xy, True) + penta((w,0), E19.PB4)...")
    count = 0
    total = 0
    for w in PaB.generWComm(E19.xy, True):
        total += 1
        if PaB.penta((w, 0), E19.PB4):
            count += 1
    print(f"PackageGT pentagon-pass count = {count} / {total} words enumerated "
          f"(commutator-subgroup domain, |[F2,F2]|=commF2={commF2})")

    c8_pass = (count == 216)
    print(f"\nC-8 cross-check (PackageGT count == 216): "
          f"{'PASS' if c8_pass else 'MISMATCH -- report, do not silently accept'}")
    all_ok = all_ok and c8_pass

    if all_ok:
        print("\nC8_PASS")
    else:
        print("\nC8_FAIL (see individual checks above)")
        sys.exit(1)


if __name__ == "__main__":
    main()
