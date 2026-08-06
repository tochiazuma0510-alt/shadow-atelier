#!/usr/bin/env python3
"""
bit252_independent_check.py -- independent (GAP-helper-free) re-check of the
BIT-252 one-way calibration, per docs/notes/bit252_oneway_prereg_iffirst_v1.md
裁定661 (c).

Consumes ONLY the JSON files GAP wrote (search/certs/bit252_oneway_run_v1_raw.json,
search/certs/bit252_oneway_perm_export_v1.json) -- reuses no GAP code, no
GAP data structures beyond the plain permutation-list export.

Two tiers, chosen based on what GAP's export actually contains:
  1. If P's permutation degree was small enough to export (see the GAP
     script's size guard), independently re-derive F-1 (m=0,f=1), F-3
     (h4^t, t=0..6) and F-7 (full 343-point gr_4 sweep) using an entirely
     separate permutation-arithmetic engine (same style as
     search/twin_witness_mc1_check_v1_1.py earlier this session). F-2/F-4/
     F-5/F-6 are NOT independently re-derived this pass (F-1/F-3/F-7 were
     prioritized -- F-7 is the prereg's own flagged-most-important fixture).
  2. ALWAYS (regardless of tier 1): an algebra-only cross-check of F-7's
     claimed solution set against its own definition (the line
     {(t, 4t mod 7, t) : t=0..6}) -- needs no group data, no GAP, just
     re-deriving the claimed line from scratch and comparing set equality.

This script does NOT re-verify the main R3 fiber sweep (117,649 elements
over P', order 7^14) -- P' was not exported (would require a much larger
permutation degree than the size guard allows in general), so that number
is NOT independently re-checked here. Disclosed explicitly, not silently
skipped.
"""
import json
import sys

RAW_CERT_PATH = "search/certs/bit252_oneway_run_v1_raw.json"
PERM_EXPORT_PATH = "search/certs/bit252_oneway_perm_export_v1.json"


# ---------------------------------------------------------------------------
# permutation arithmetic (matches search/twin_witness_mc1_check_v1_1.py
# convention: perm_mul(p,q)[i] = q[p[i]-1], i.e. apply p then q, GAP-style
# i^(p*q) = (i^p)^q).
# ---------------------------------------------------------------------------
def perm_identity(n):
    return list(range(1, n + 1))


def perm_mul(p, q):
    n = len(p)
    return [q[p[i] - 1] for i in range(n)]


def perm_inv(p):
    n = len(p)
    inv = [0] * n
    for i in range(n):
        inv[p[i] - 1] = i + 1
    return inv


def perm_pow(p, k):
    n = len(p)
    if k == 0:
        return perm_identity(n)
    base = p if k > 0 else perm_inv(p)
    result = perm_identity(n)
    for _ in range(abs(k)):
        result = perm_mul(result, base)
    return result


def perm_eq(p, q):
    return list(p) == list(q)


def comm(a, b, n):
    """[a,b] := a^-1 b^-1 a b, matching the prereg's commutator convention
    (= GAP Comm(a,b) natively)."""
    return perm_mul(perm_mul(perm_mul(perm_inv(a), perm_inv(b)), a), b)


def main():
    with open(RAW_CERT_PATH, encoding="utf-8") as f:
        raw_cert = json.load(f)

    print("=== Tier 2 (always): algebra-only F-7 solution-set cross-check ===")
    claimed_solutions = raw_cert["calibration"]["F7_solutions"]
    claimed_set = {tuple(s) for s in claimed_solutions}
    expected_line = {(t, (4 * t) % 7, t % 7) for t in range(7)}
    tier2_ok = (claimed_set == expected_line)
    print(f"claimed F-7 solutions: {sorted(claimed_set)}")
    print(f"expected line F7(1,4,1) = {{(t,4t,t) mod 7}}: {sorted(expected_line)}")
    print(f"F-7 solution set matches the line, independently re-derived: {tier2_ok}")

    all_ok = tier2_ok

    with open(PERM_EXPORT_PATH, encoding="utf-8") as f:
        perm_export = json.load(f)

    tier1_ran = False
    if perm_export.get("exported"):
        tier1_ran = True
        print("\n=== Tier 1: full independent re-derivation of F-1..F-7 via permutations ===")
        deg = perm_export["P_perm_degree"]
        xP = [int(v) for v in perm_export["xP_perm"]]
        yP = [int(v) for v in perm_export["yP_perm"]]
        ident = perm_identity(deg)

        # v1,v2,v3 built directly as PERMUTATIONS via comm() (own engine,
        # not the GAP word engine); h4 = v1 * v2^4 * v3.
        xy = comm(xP, yP, deg)
        v1P = comm(comm(xy, xP, deg), xP, deg)
        v2P = comm(comm(xy, xP, deg), yP, deg)
        v3P = comm(comm(xy, yP, deg), yP, deg)
        h4P = perm_mul(perm_mul(v1P, perm_pow(v2P, 4)), v3P)

        # theta(v_i): theta(x)=y, theta(y)=x, so theta(v_i) = same comm()
        # formula with xP,yP swapped throughout:
        theta_v1 = comm(comm(comm(yP, xP, deg), yP, deg), yP, deg)
        theta_v2 = comm(comm(comm(yP, xP, deg), yP, deg), xP, deg)
        theta_v3 = comm(comm(comm(yP, xP, deg), xP, deg), xP, deg)

        # tau: x->y, y->(xy)^-1 =: z
        zP = perm_inv(perm_mul(xP, yP))
        tau_v1 = comm(comm(comm(yP, zP, deg), yP, deg), yP, deg)
        tau_v2 = comm(comm(comm(yP, zP, deg), yP, deg), zP, deg)
        tau_v3 = comm(comm(comm(yP, zP, deg), zP, deg), zP, deg)
        tau2_v1 = comm(comm(comm(zP, xP, deg), zP, deg), zP, deg)  # tau(tau(v1)): tau(y)=z,tau(z)=x
        tau2_v2 = comm(comm(comm(zP, xP, deg), zP, deg), xP, deg)
        tau2_v3 = comm(comm(comm(zP, xP, deg), xP, deg), xP, deg)

        def w_from_abc(a, b, c, g1, g2, g3):
            return perm_mul(perm_mul(perm_pow(g1, a), perm_pow(g2, b)), perm_pow(g3, c))

        def hex_pass_abc(m, a, b, c):
            f = w_from_abc(a, b, c, v1P, v2P, v3P)
            theta_f = w_from_abc(a, b, c, theta_v1, theta_v2, theta_v3)
            hex1 = perm_eq(perm_mul(f, theta_f), ident)
            ymf = perm_mul(perm_pow(yP, m), f)
            # tau(y^m f): need tau applied to an ARBITRARY element y^m*f,
            # not just the v-combination -- decompose: tau(y^m*f) =
            # tau(y)^m * tau(f) = z^m * tau(f) (tau is a homomorphism)
            tau_f = w_from_abc(a, b, c, tau_v1, tau_v2, tau_v3)
            tau_ymf = perm_mul(perm_pow(zP, m), tau_f)
            tau2_f = w_from_abc(a, b, c, tau2_v1, tau2_v2, tau2_v3)
            tau2_ymf = perm_mul(perm_pow(xP, m), tau2_f)  # tau(z)=x
            hex2 = perm_eq(perm_mul(perm_mul(tau2_ymf, tau_ymf), ymf), ident)
            return hex1 and hex2

        # F-1: m=0, f=1 (a=b=c=0)
        f1 = hex_pass_abc(0, 0, 0, 0)
        print(f"F-1 (m=0,f=1): {f1} (expect True)")
        all_ok = all_ok and f1

        # F-3: m=0, f=h4^t, t=0..6 -- h4 = v1*v2^4*v3, so h4^t is NOT simply
        # v1^t v2^(4t) v3^t in general (non-abelian) UNLESS gr_4 is central/
        # abelian (which it is, per the prereg's own structural claim: gr_4
        # is central elementary abelian). We rely on that fact (independently
        # stated in the prereg, sec3.2/sec4.3) to write h4^t = v1^t v2^(4t) v3^t.
        f3_count = 0
        for t in range(7):
            if hex_pass_abc(0, t % 7, (4 * t) % 7, t % 7):
                f3_count += 1
        print(f"F-3 (m=0,f=h4^t,t=0..6): {f3_count}/7 PASS (expect 7/7)")
        all_ok = all_ok and (f3_count == 7)

        # F-7: full 343-point sweep, independently
        f7_sols = []
        for a in range(7):
            for b in range(7):
                for c in range(7):
                    if hex_pass_abc(0, a, b, c):
                        f7_sols.append((a, b, c))
        print(f"F-7 (independent re-sweep): {len(f7_sols)} solutions (expect 7)")
        print(f"F-7 solutions (independent): {sorted(f7_sols)}")
        f7_indep_ok = (set(f7_sols) == expected_line)
        print(f"F-7 independent re-sweep matches line: {f7_indep_ok}")
        all_ok = all_ok and f7_indep_ok

        # cross-check against GAP's own reported F-7 solutions
        f7_agree_with_gap = (set(f7_sols) == claimed_set)
        print(f"F-7 independent result AGREES with GAP's reported solutions: {f7_agree_with_gap}")
        all_ok = all_ok and f7_agree_with_gap
    else:
        print(f"\n=== Tier 1: SKIPPED (perm export not available: {perm_export.get('reason')}) ===")

    # 裁定663: "独立checkerの緑が未検証数値を含む"問題への対処 -- all_ok とは
    # 別掲で、THIS SCRIPT (bit252_independent_check.py) が実際にカバーして
    # いない項目を明示的に列挙する。falsifier の別ファイル(bit252_lie.py /
    # bit252_indep.py, search/probe/bit252_v1/ に搬入・第二系統として cert
    # second_system 欄に記載済み)は THIS SCRIPT とは別の、より広い独立検証
    # (R3 survival_count・d5・P'-F2 の順序分離テストを含む)を行っており、
    # そちらの結果は GAP 側 cert の "second_system" 欄を参照のこと -- ここで
    # の not_verified は「このスクリプト単体で見て」何が未検証かを指す。
    not_verified_by_this_script = [
        "R3_survival_count (main 117649-element fiber sweep over P') "
        "-- NOT independently re-verified by THIS script (P' perm export "
        "not attempted; but IS independently re-verified by "
        "search/probe/bit252_v1/bit252_indep.py, a SEPARATE falsifier "
        "script using a different construction -- see cert second_system)",
        "F2, F4, F5, F6 (P-side calibration) -- not re-derived in tier1 "
        "(only F1/F3/F7 were prioritized this pass)",
        "positive_control (P'-F2 test) -- NOT re-verified by THIS script "
        "(again covered separately by bit252_indep.py)",
        "d5 -- NOT computed by THIS script (covered by bit252_lie.py)",
    ]

    print(f"\n=== SUMMARY: tier1_ran={tier1_ran}, all_ok={all_ok} ===")
    print("not_verified_by_this_script (see list, distinct from all_ok):")
    for item in not_verified_by_this_script:
        print(f"  - {item}")
    print("NOTE: this script's all_ok=True covers ONLY F1/F3/F7 (tier1, if exported) "
          "and F7's algebra-only re-derivation (tier2). The items above are NOT "
          "covered by all_ok and must not be read as verified by it.")

    with open("search/certs/bit252_independent_check_result_v1.json", "w", encoding="utf-8") as f:
        json.dump({
            "tier2_F7_algebra_only_ok": tier2_ok,
            "tier1_ran": tier1_ran,
            "all_ok": all_ok,
            "all_ok_scope": "F1, F3, F7 (tier1, if perm export available) and F7 algebra-only (tier2) ONLY",
            "not_verified_by_this_script": not_verified_by_this_script,
            "note": "See cert's second_system field for falsifier's separate, broader "
                    "independent verification (bit252_lie.py/bit252_indep.py) covering "
                    "R3 survival_count, d5, and the P'-F2 positive control.",
        }, f, ensure_ascii=False, indent=2)
    print("Wrote search/certs/bit252_independent_check_result_v1.json")

    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
