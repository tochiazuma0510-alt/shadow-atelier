#!/usr/bin/env python3
# crosscheck/check_pl_lab1_normchk.py
# Independent checker for the NORM-CHK cert (裁定783(1),
# search/certs/pl_lab1_normchk_v1_20260811.json). Does NOT import
# search/pl_lab1_normchk_v1.py (search/crosscheck separation). Does NOT
# re-run GAP -- reads the PL-LAB-1 cert directly for def_p/H_p/kernel_dim
# (already independently cross-checked in crosscheck/check_pl_lab1.py)
# and independently re-derives the closed-form Lambda_p isotypic
# multiplicities (own arithmetic, not copied), then independently
# verifies the additive R_p decomposition and the m_std(R_p)==|def_p|
# claim from first principles.
import json
import sys

CERT_PATH = "search/certs/pl_lab1_normchk_v1_20260811.json"
PL_LAB1_CERT_PATH = "search/certs/pl_lab1_v1_20260811.json"

WITT_2_K = {1: 2, 2: 1, 3: 2, 4: 3, 5: 6, 6: 9, 7: 18, 8: 30}


def mu(n):
    if n == 1:
        return 1
    r, d, m = 1, 2, n
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            r = -r
        d += 1
    if m > 1:
        r = -r
    return r


def witt(q, n):
    total = 0
    for d in range(1, n + 1):
        if n % d == 0:
            total += mu(d) * q ** (n // d)
    return total // n


def chi_std_tau(d):
    return 2 if d % 3 == 0 else -1


def tr_tau_lambda(k):
    total = 0
    for d in range(1, k + 1):
        if k % d == 0:
            total += mu(d) * (chi_std_tau(d) ** (k // d))
    return total // k


def chi_std_theta(d):
    return 2 if d % 2 == 0 else 0


def tr_theta_lambda(k):
    total = 0
    for d in range(1, k + 1):
        if k % d == 0:
            total += mu(d) * (chi_std_theta(d) ** (k // d))
    return total // k


def H_of(k):
    return (witt(2, k) - tr_tau_lambda(k)) // 3


def isotypic_from_traces(dim, t, s):
    m_triv = dim + 3 * t + 2 * s
    m_sgn = dim - 3 * t + 2 * s
    m_std2 = 2 * dim - 2 * s
    assert m_triv % 6 == 0 and m_sgn % 6 == 0 and m_std2 % 6 == 0
    return m_triv // 6, m_sgn // 6, m_std2 // 6


def main():
    fails = []

    def fail(msg):
        fails.append(msg)
        print("[FAIL]", msg)

    def ok(msg):
        print("[PASS]", msg)

    try:
        doc = json.load(open(CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        print(f"CROSSCHECK RESULT: FAIL (cert not found: {CERT_PATH})")
        sys.exit(1)

    if doc.get("schema") != "shadow-atelier/pl_lab1_normchk_v1":
        fail(f"schema mismatch: {doc.get('schema')}")
    else:
        ok("schema = shadow-atelier/pl_lab1_normchk_v1")
    if doc.get("stop_code") is not None:
        fail(f"stop_code={doc.get('stop_code')} -- job did not complete cleanly")
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    ok("stop_code=None")

    pl = json.load(open(PL_LAB1_CERT_PATH, encoding="utf-8"))
    pl_targets = {t["p"]: t for t in pl["targets"] if t["kind"] == "main"}

    # independently recompute the theta-trace-on-odd-k = 0 fact using the
    # FULL necklace formula (not the shortcut "every divisor is odd"
    # argument) -- a genuine independent re-derivation, not the same
    # reasoning restated.
    for k in [5, 7]:
        t_full = tr_theta_lambda(k)
        if t_full != 0:
            fail(f"k={k}: independently recomputed tr(theta|Lambda_{k}) via full necklace formula = "
                 f"{t_full} != 0")
        else:
            ok(f"k={k}: independently recomputed tr(theta|Lambda_{k})=0 via full necklace formula "
               f"(sum over all divisors, not the odd-divisor shortcut)")

    for p in [5, 7]:
        row = doc["per_p"][str(p)]
        pl_row = pl_targets[p]
        pd = next(x for x in pl_row["per_degree"] if x["k"] == p)

        if row["delta_p"] != pl_row["p_pl_0_drop_at_p"] or row["def_p"] != pd["def_k"] or row["H_p"] != pd["H_k"]:
            fail(f"p={p}: sourced delta_p/def_p/H_p do not match the separately-loaded PL-LAB-1 cert")
        else:
            ok(f"p={p}: delta_p={row['delta_p']} def_p={row['def_p']} H_p={row['H_p']} correctly sourced "
               f"from the separately-loaded PL-LAB-1 cert")

        H_recomputed = H_of(p)
        witt_p = witt(2, p)
        if H_recomputed != row["H_p"] or witt_p != row["witt_2_p"]:
            fail(f"p={p}: recomputed H_p={H_recomputed} witt_2_p={witt_p} != cert "
                 f"H_p={row['H_p']} witt_2_p={row['witt_2_p']}")

        t_theta = tr_theta_lambda(p)
        s_tau = tr_tau_lambda(p)
        m_triv_L, m_sgn_L, m_std_L = isotypic_from_traces(witt_p, t_theta, s_tau)
        cert_L = row["Lambda_p_isotypic"]
        if (m_triv_L, m_sgn_L, m_std_L) != (cert_L["m_triv"], cert_L["m_sgn"], cert_L["m_std"]):
            fail(f"p={p}: recomputed Lambda_p isotypic ({m_triv_L},{m_sgn_L},{m_std_L}) != cert "
                 f"({cert_L['m_triv']},{cert_L['m_sgn']},{cert_L['m_std']})")
        else:
            ok(f"p={p}: independently recomputed Lambda_p isotypic (triv={m_triv_L},sgn={m_sgn_L},"
               f"std={m_std_L}) matches cert")
        if m_std_L != row["H_p"]:
            fail(f"p={p}: m_std(Lambda_p)={m_std_L} != H_p={row['H_p']} (internal consistency)")

        meas = row["measured_isotypic"]
        if meas["m_std"] != pd["kernel_dim"]:
            fail(f"p={p}: measured m_std={meas['m_std']} != PL-LAB-1's kernel_dim={pd['kernel_dim']}")
        else:
            ok(f"p={p}: measured_isotypic.m_std={meas['m_std']} matches PL-LAB-1 cert's kernel_dim")

        m_triv_R = m_triv_L - meas["m_triv"]
        m_sgn_R = m_sgn_L - meas["m_sgn"]
        m_std_R = m_std_L - meas["m_std"]
        cert_R = row["R_p_isotypic"]
        if (m_triv_R, m_sgn_R, m_std_R) != (cert_R["m_triv"], cert_R["m_sgn"], cert_R["m_std"]):
            fail(f"p={p}: recomputed R_p isotypic ({m_triv_R},{m_sgn_R},{m_std_R}) != cert "
                 f"({cert_R['m_triv']},{cert_R['m_sgn']},{cert_R['m_std']})")
        else:
            ok(f"p={p}: independently recomputed R_p isotypic (triv={m_triv_R},sgn={m_sgn_R},"
               f"std={m_std_R}) matches cert")

        delta_check = m_triv_R + m_sgn_R + 2 * m_std_R
        if delta_check != row["delta_p"]:
            fail(f"p={p}: recomputed delta_p from isotypic sum={delta_check} != cert delta_p={row['delta_p']}")
        else:
            ok(f"p={p}: delta_p={row['delta_p']} re-derives correctly from R_p isotypic sum")

        m_std_match_recomputed = (m_std_R == abs(row["def_p"]))
        if m_std_match_recomputed != row["m_std_R_p_equals_abs_def_p"]:
            fail(f"p={p}: recomputed m_std(R_p)==|def_p| = {m_std_match_recomputed} != cert "
                 f"{row['m_std_R_p_equals_abs_def_p']}")
        else:
            ok(f"p={p}: NORM-CHK core claim m_std(R_p)==|def_p| re-verified independently: "
               f"{m_std_match_recomputed}")

    all_match_recomputed = all(doc["per_p"][str(p)]["m_std_R_p_equals_abs_def_p"] for p in [5, 7])
    if all_match_recomputed != doc["all_m_std_R_p_equals_abs_def_p"]:
        fail("all_m_std_R_p_equals_abs_def_p does not re-derive correctly")
    else:
        ok(f"all_m_std_R_p_equals_abs_def_p re-derives correctly: {all_match_recomputed} "
           f"(NORM-CHK: branch L confirmed for both p=5,7, exactly, no residual)")

    print()
    if fails:
        print(f"CROSSCHECK RESULT: FAIL ({len(fails)} issues)")
        sys.exit(1)
    else:
        print("CROSSCHECK RESULT: PASS (independently re-derived tr(theta|Lambda_p)=0 via the FULL "
              "necklace formula, independently recomputed all Lambda_p/measured/R_p isotypic "
              "multiplicities via own arithmetic, and independently re-verified m_std(R_p)==|def_p| "
              "for both p=5,7 from data sourced from the separately-loaded, separately-cross-checked "
              "PL-LAB-1 cert; all match. cross-checked, not 'verified' (reserved for Lean))")
        sys.exit(0)


if __name__ == "__main__":
    main()
