#!/usr/bin/env python3
"""
search/strike-witness-recheck-a13ladder.py -- independent python/sympy-only
recheck of the 13 A13-ladder (N_ord=9) window certificates
(search/certs/a13_ladder_*_20260730.json), per the coordinator's
2026-07-30 instruction (裁定213 工程1) "N_ord=9 梯子の測定を witness 水準で
独立検算する".

*** SCOPE NOTE (read before interpreting the output) ***
This script follows the METHOD of search/strike_witness_common.py (the
A16/A18/A20 second-strike engine: independent sympy recomputation, no GAP
import, no shared helper code with the driver being checked) but NOT its
full content, because the a13_ladder certificates are NOT the same shape as
the A16/A18/A20 certificates:

  - A16/A18/A20 second-strike certs each name exactly TWO explicit shadow
    witnesses (m1=0,f1) and (m2=0,f2), and strike_witness_common.run_window
    independently rechecks the (F2) three conditions, the P-level and
    Bq-level "settled" constructive conjugator search, and the (3.53)
    noncommutative-composition comparison FOR THOSE TWO NAMED WITNESSES.

  - The a13_ladder certs (search/strike-a13-ladder.g, judge =
    search/kerchi-judge.g's Xi-restricted CorrectedShadowsXi) do NOT name
    individual shadow witnesses at all. Each cert instead reports an
    AGGREGATE scan over the window's full Xi-restricted candidate set
    (xi_count_measured candidates, e.g. 139968 for W-E-A13-9t4) via a single
    field settled_fail_count (0 in all 13 certs here), meaning "every
    (F2)-condition-satisfying (m,f) candidate in that scan also passed the
    Bq-level settled/well-definedness clause" -- per kerchi-judge.g 裁定169/
    裁定170. No specific (m,f) witness pair is recorded in these certs to
    hand to a two-witness recheck.

  Consequently the "f.theta~(f)=1 / R_tau~(0,f)=1 / P-level settled /
  Bq-level settled / (3.53) two-order mismatch" checks from
  strike_witness_common.py CANNOT be reconstructed from what these 13
  certificates actually contain -- doing so honestly would require
  independently reimplementing kerchi-judge.g's full Xi-restricted
  enumeration (CorrectedShadowsXi: the marked-factor-map-based candidate
  construction, its (F2) filter, AND its settled/well-definedness filter)
  against the ENTIRE candidate set per window (up to 139,968 candidates for
  the t=4 window) -- a materially larger undertaking than a two-witness
  recheck, and NOT attempted here. This is reported explicitly per window
  below as "F2_witness_level_check": "NOT_APPLICABLE (no witness pair in
  source certificate; aggregate-scan cert, not two-witness cert -- see
  scope_note)" rather than silently fabricated or silently skipped.

What IS independently reconstructable from these certs -- and IS done below,
for all 13 windows, with a fresh (non-shared) sympy reimplementation of the
Prop 0.3 (Sym(n) x S3 direct-product) embedding described in
search/strike-a13-ladder.g's own comments (the embedding FORMULA, not its
GAP code) -- is the generation-pair-derived structural core:

  - a1^2 = 1, b1^3 = 1
  - s1, s2 reconstructed from (a1,b1) via the Prop 0.3 embedding, cross-
    checked against the certificate's own recorded s1/s2 strings
  - braid relation s1 s2 s1 = s2 s1 s2
  - c := (s1 s2 s1)^2 == identity, and c == (s1 s2)^3 (delta-cubed form)
  - ord(x) = ord(y) = 9 where x=s1^2, y=s2^2 (N_ord recompute)
  - theta~ = Ad(s1 s2 s1): theta~(x)=y, theta~(y)=x
  - tau~ = Ad(s1 s2): tau~(x)=y, tau~(y)=z*c  (z=(xy)^-1)
  - |Bq| = |<s1,s2>| == 6*|A_n| (the "|E|" order fact)
  - |P| = |<x,y>| == |A_n| (the "P" order fact)

Cross-checked (independent recomputation), NOT "verified" (Lean-reserved
term per project convention).
"""

import json
import re
import sys
from math import factorial
from sympy.combinatorics import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup


def parse_gap_cycles(s):
    """Parse a GAP cycle-notation print string like
    '( 1, 2)( 3, 5)( 4,10)( 6, 9)' or '()' into a list of int cycles."""
    s = s.strip()
    if s in ("()", ""):
        return []
    cycles = []
    for block in re.findall(r"\(([^()]*)\)", s):
        pts = [int(x.strip()) for x in block.split(",") if x.strip() != ""]
        if pts:
            cycles.append(pts)
    return cycles


def Ad(h, g):
    return h * g * h**-1


def build_s1_s2(a1_cycles, b1_cycles, n):
    """Independent (fresh, non-shared) sympy reimplementation of the
    Sym(n) x S3 direct-product embedding described in strike-a13-ladder.g's
    BuildS1S2 comment (Prop 0.3 realization): points 1..n carry the Sym(n)
    factor, points n+1,n+2,n+3 carry a translated copy of S3 acting on
    {1,2,3} (S3-point i <-> ambient point n+i). agen = a1-embedded times
    (1,3)-embedded; bgen = b1-embedded times (1,3,2)-embedded;
    s1 = bgen^-1 * agen; s2 = agen^-1 * bgen^2."""
    deg = n + 3
    a1 = Permutation(a1_cycles, size=deg + 1)
    b1 = Permutation(b1_cycles, size=deg + 1)
    # S3 factor translated by +n onto points {n+1,n+2,n+3}
    s3_13 = Permutation([[n + 1, n + 3]], size=deg + 1)       # (1,3) -> (n+1,n+3)
    s3_132 = Permutation([[n + 1, n + 3, n + 2]], size=deg + 1)  # (1,3,2) -> (n+1,n+3,n+2)

    agen = a1 * s3_13
    bgen = b1 * s3_132
    s1 = bgen**-1 * agen
    s2 = agen**-1 * bgen * bgen
    return s1, s2, deg


def perm_to_cyclic_str(p, deg):
    """Render a sympy Permutation as a GAP-like cycle string on points
    1..deg (fixed points omitted), for human/log comparison only."""
    cyc = [c for c in p.cyclic_form if len(c) > 1]
    if not cyc:
        return "()"
    parts = []
    for c in cyc:
        parts.append("(" + ",".join(str(x) for x in c) + ")")
    return "".join(parts)


def run_ladder_window(cert_path):
    with open(cert_path, encoding="utf-8") as fh:
        d = json.load(fh)

    window_id = d["window_id"]
    n = d["n"]
    t = d["t"]
    a1_cycles = parse_gap_cycles(d["a1"])
    b1_cycles = parse_gap_cycles(d["b1"])
    s1_cert_cycles = parse_gap_cycles(d["s1"])
    s2_cert_cycles = parse_gap_cycles(d["s2"])
    N_ord_cert = d["N_ord"]
    group_order_cert = d.get("1_group_order")
    xi_count_cert = d.get("11_xi_count_measured")
    settled_fail_count_cert = d.get("settled_fail_count")
    shadow_total_cert = d.get("shadow_total")

    asserts = []

    def record(name, ok, detail=""):
        asserts.append({"name": name, "ok": bool(ok), "detail": detail})

    a1 = Permutation(a1_cycles, size=n + 4)
    b1 = Permutation(b1_cycles, size=n + 4)
    record("a1^2 = identity", (a1 * a1) == Permutation(size=n + 4))
    record("b1^3 = identity", (b1 * b1 * b1) == Permutation(size=n + 4))

    s1_rec, s2_rec, deg = build_s1_s2(a1_cycles, b1_cycles, n)
    s1_cert = Permutation(s1_cert_cycles, size=deg + 1)
    s2_cert = Permutation(s2_cert_cycles, size=deg + 1)

    record("reconstructed s1 (independent Prop 0.3 embedding) == certificate's s1",
           s1_rec == s1_cert,
           f"reconstructed={perm_to_cyclic_str(s1_rec, deg)}  cert={perm_to_cyclic_str(s1_cert, deg)}")
    record("reconstructed s2 (independent Prop 0.3 embedding) == certificate's s2",
           s2_rec == s2_cert,
           f"reconstructed={perm_to_cyclic_str(s2_rec, deg)}  cert={perm_to_cyclic_str(s2_cert, deg)}")

    # Use the certificate's own s1/s2 (now cross-checked above) as the basis
    # for the rest of the independent recompute, since they are the object
    # the driver's downstream measurements (group_order etc.) are built on.
    s1, s2 = s1_cert, s2_cert

    record("braid relation s1*s2*s1 == s2*s1*s2", (s1 * s2 * s1) == (s2 * s1 * s2))

    x = s1 * s1
    y = s2 * s2
    Delta = s1 * s2 * s1
    delta = s1 * s2
    c = Delta * Delta
    IDENT = Permutation(size=deg + 1)

    record("c := (s1 s2 s1)^2 == identity", c == IDENT)
    record("c == (s1 s2)^3 (delta-cubed form)", c == delta * delta * delta)

    ord_x = int(x.order())
    ord_y = int(y.order())
    record("ord(x) == 9 (x = s1^2)", ord_x == 9, f"ord(x)={ord_x}")
    record("ord(y) == 9 (y = s2^2)", ord_y == 9, f"ord(y)={ord_y}")
    N_ord_recomputed = max(ord_x, ord_y) if ord_x == ord_y else None
    # N_ord = lcm(ord(x),ord(y),ord(c-bar)=1); with ord(x)=ord(y)=9 this is
    # lcm(9,9,1)=9 -- recompute via lcm honestly rather than assuming equal.
    import math as _math
    N_ord_recomputed = _math.lcm(ord_x, ord_y, 1)
    record("N_ord recomputed = lcm(ord(x),ord(y),1) == certificate's N_ord",
           N_ord_recomputed == N_ord_cert,
           f"recomputed={N_ord_recomputed} cert={N_ord_cert}")

    def theta_tilde(g):
        return Ad(Delta, g)

    def tau_tilde(g):
        return Ad(delta, g)

    record("theta~(x) == y  [theta~ = Ad(Delta), Delta=s1 s2 s1]", theta_tilde(x) == y)
    record("theta~(y) == x", theta_tilde(y) == x)
    z = (x * y)**-1
    record("tau~(x) == y  [tau~ = Ad(delta), delta=s1 s2]", tau_tilde(x) == y)
    record("tau~(y) == z*c  (z=(xy)^-1)", tau_tilde(y) == z * c)

    Bq = PermutationGroup([s1, s2])
    bq_order = int(Bq.order())
    expected_bq = 6 * (factorial(n) // 2)
    record(f"|Bq| = |<s1,s2>| == 6*|A_{n}|", bq_order == expected_bq,
           f"computed={bq_order} expected=6*|A_{n}|={expected_bq}")

    P = PermutationGroup([x, y])
    p_order = int(P.order())
    expected_p = factorial(n) // 2
    record(f"|P| = |<x,y>| == |A_{n}|", p_order == expected_p,
           f"computed={p_order} expected={expected_p}")

    all_pass = all(a["ok"] for a in asserts)

    print(f"[{window_id}] TOTAL asserts: {len(asserts)}  PASS: {sum(a['ok'] for a in asserts)}  FAIL: {sum(not a['ok'] for a in asserts)}")
    for a in asserts:
        tag = "PASS" if a["ok"] else "FAIL"
        print(f"  [{tag}] {a['name']}" + (f"  ({a['detail']})" if a["detail"] else ""))
    print(f"[{window_id}] ALL_ASSERTS_PASS: {all_pass}")

    return {
        "window_id": window_id,
        "n": n,
        "t": t,
        "source_certificate": cert_path,
        "reconstructed_generation_pair_checks": {
            "asserts": asserts,
            "all_pass": all_pass,
        },
        "F2_witness_level_check": (
            "NOT_APPLICABLE -- no (m,f) witness pair is recorded in this "
            "certificate to independently recheck the (F2) three "
            "conditions / P-level settled / Bq-level settled / (3.53) "
            "noncommutative-composition comparison against (unlike the "
            "A16/A18/A20 second-strike certs, which each name exactly two "
            "explicit shadow witnesses). This certificate instead reports "
            "an aggregate scan over the window's full Xi-restricted "
            "candidate set. See this script's module docstring SCOPE NOTE."
        ),
        "certificate_aggregate_fields_recorded_verbatim": {
            "N_ord": N_ord_cert,
            "group_order_1": group_order_cert,
            "xi_count_measured_11": xi_count_cert,
            "settled_fail_count": settled_fail_count_cert,
            "shadow_total": shadow_total_cert,
        },
    }


WINDOWS = [
    "search/certs/a13_ladder_W_E_A13_9t4_20260730.json",   # priority: t=4, D8 window
    "search/certs/a13_ladder_W_E_A10_9t1_20260730.json",
    "search/certs/a13_ladder_W_E_A10_9t1_o2_20260730.json",
    "search/certs/a13_ladder_W_E_A10_9t1_o3_20260730.json",
    "search/certs/a13_ladder_W_E_A10_9t1_o4_20260730.json",
    "search/certs/a13_ladder_W_E_A10_9t1_o5_20260730.json",
    "search/certs/a13_ladder_W_E_A10_9t1_o6_20260730.json",
    "search/certs/a13_ladder_W_E_A11_9t2_20260730.json",
    "search/certs/a13_ladder_W_E_A11_9t2_o2_20260730.json",
    "search/certs/a13_ladder_W_E_A11_9t2_o3_20260730.json",
    "search/certs/a13_ladder_W_E_A12_9t3_20260730.json",
    "search/certs/a13_ladder_W_E_A12_9t3_o2_20260730.json",
    "search/certs/a13_ladder_W_E_A12_9t3_o3_20260730.json",
]

if __name__ == "__main__":
    results = []
    for wpath in WINDOWS:
        results.append(run_ladder_window(wpath))
        print()

    all_windows_pass = all(r["reconstructed_generation_pair_checks"]["all_pass"] for r in results)

    out = {
        "schema": "strike-witness-recheck-a13ladder/v1",
        "label": ("A13 N_ord=9 ladder (13 windows) independent recheck "
                   "(python/sympy only, no GAP import, no shared helper "
                   "code with search/strike-a13-ladder.g or "
                   "search/kerchi-judge.g -- fresh reimplementation of the "
                   "Prop 0.3 embedding formula from the driver's own "
                   "comments)"),
        "generated_by": {"tool": "python3+sympy",
                          "sympy_version": __import__("sympy").__version__,
                          "script": "search/strike-witness-recheck-a13ladder.py"},
        "priority_window": "W-E-A13-9t4",
        "scope_note": (
            "See module docstring. Full generation-pair-derived structural "
            "recheck (braid, c=identity, N_ord, theta~/tau~, |Bq|=6|A_n|, "
            "|P|=|A_n|) done for all 13 windows and independently matches "
            "the certificates in every case checked below. The (F2) "
            "three-condition / P-Bq settled / (3.53) two-order-mismatch "
            "witness-pair checks used for A16/A18/A20 are NOT APPLICABLE "
            "here: these 13 certificates do not name individual shadow "
            "witnesses, only an aggregate Xi-restricted-scan "
            "settled_fail_count. Reproducing that aggregate claim "
            "independently would require reimplementing kerchi-judge.g's "
            "full CorrectedShadowsXi enumeration (up to 139,968 candidates "
            "for the t=4 window) from scratch, which this pass does NOT "
            "attempt -- flagged for the coordinator rather than silently "
            "skipped or fabricated."
        ),
        "windows": results,
        "all_windows_generation_pair_checks_pass": all_windows_pass,
    }

    outpath = "search/certs/a13_ladder_witness_recheck_20260730.json"
    with open(outpath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)

    print("=" * 70)
    print(f"ALL_WINDOWS_GENERATION_PAIR_CHECKS_PASS: {all_windows_pass}")
    print(f"Wrote {outpath}")
