#!/usr/bin/env python3
"""
d972_local3_producer_v1.py -- LOCAL-3 protocol (S1-S10), PRODUCER system.
Math source: scratchpad/d972_idx3_arith_datum_independent_v1.md sec.7.3 (frozen spec).
Independent authorship: this file shares NO code/helpers with the checker
(scratchpad/d972_local3_checker_v1.g, written in GAP, a different language/system).

Inputs (inventory only, per sec.7.3.2):
  u0inv  = -1423828125/256   (search/certs/ds4_receipt_v1_20260812.json field input_u0_inverse)
  beta   = 2                  (pin, per instruction; sec.3.1's beta=2 prediction)

Declared convention D (this run): sgn = +1, i.e. u_S4 := u0inv literally (no extra inversion).
This is a PRE-DECLARED, reproducible choice -- NOT validated against u_dih (pending, per
instruction point 4). DC-1 tests that flipping this declaration flips c' as expected.
"""
import json
from fractions import Fraction

U0INV = Fraction(-1423828125, 256)
BETA = 2

def mod_frac(fr: Fraction, p: int) -> int:
    """Reduce a Fraction mod prime p, returning an int in [0,p)."""
    num = fr.numerator % p
    den = fr.denominator % p
    den_inv = pow(den, p - 2, p)
    return (num * den_inv) % p

def cube_residue(z_mod_p: int, p: int) -> int:
    """S3 = z^((p-1)/3) mod p, in mu_3(F_p)."""
    return pow(z_mod_p, (p - 1) // 3, p)

def find_mu3_generator(p: int) -> int:
    """Canonical generator omega of mu_3(F_p): smallest g in [2,p) with g^((p-1)/3) != 1,
    then omega := g^((p-1)/3). Deterministic/reproducible convention."""
    for g in range(2, p):
        cand = pow(g, (p - 1) // 3, p)
        if cand != 1:
            return cand
    raise RuntimeError("no generator found (should not happen for p == 1 mod 3)")

def discrete_log_mu3(val: int, omega: int, p: int) -> int:
    """val = omega^e, e in {0,1,2}. val must be in mu_3(F_p)."""
    cur = 1
    for e in range(3):
        if cur == val:
            return e
        cur = (cur * omega) % p
    raise RuntimeError(f"discrete_log_mu3: {val} not a power of omega={omega} mod {p}")

def run_chain(p: int, sgn: int, mu3_gen_power: int = 1, u_extra_factor: Fraction = Fraction(1),
              beta_val: int = BETA, u0inv_val: Fraction = U0INV, label: str = ""):
    """
    Run S1-S9 for a single prime p.
    sgn: +1 or -1, selects u_S4 = u0inv^sgn (declared convention D).
    mu3_gen_power: 1 (normal) or 2 (DC-2: use omega^2 as the generator base instead of omega).
    u_extra_factor: multiplicative factor injected into u_S4 before cubing (DC-3 uses a^-9).
    beta_val: override for DC-4 style negative controls (kept =2 normally).
    Returns a dict of all intermediate + final values (fail-closed: raises/flags on any S5 violation).
    """
    out = {"p": p, "sgn": sgn, "label": label}

    # S1
    s1 = (p % 9 == 1)
    out["S1_p_mod9_eq_1"] = s1
    if not s1:
        out["status"] = "STOP_S1_FAIL"
        return out

    # S2: p does not divide num/den of u0inv, beta, disc(model) -- disc(model) not in our inventory
    # (spec's INPUT line only lists u0inv, beta, census -- "disc(model)" is not a supplied datum;
    # we check what we DO have: numerator/denominator of u0inv, and beta itself).
    num_ok = (u0inv_val.numerator % p != 0)
    den_ok = (u0inv_val.denominator % p != 0)
    beta_ok = (beta_val % p != 0)
    s2 = num_ok and den_ok and beta_ok
    out["S2_p_does_not_divide_u0inv_or_beta"] = s2
    if not s2:
        out["status"] = "STOP_S2_FAIL"
        return out

    # base u_S4 (before extra factor), per declared convention D
    if sgn == 1:
        u_S4 = u0inv_val
    elif sgn == -1:
        u_S4 = 1 / u0inv_val
    else:
        raise ValueError("sgn must be +1 or -1")
    u_S4 = u_S4 * u_extra_factor
    out["u_S4_fraction"] = str(u_S4)

    u_S4_mod_p = mod_frac(u_S4, p)
    beta_mod_p = beta_val % p

    # S3/S4
    Su = cube_residue(u_S4_mod_p, p)
    Sbeta = cube_residue(beta_mod_p, p)
    out["Su"] = Su
    out["Sbeta"] = Sbeta

    # S5: both nontrivial (discriminating-power condition)
    s5 = (Su != 1) and (Sbeta != 1)
    out["S5_both_nontrivial"] = s5
    if not s5:
        out["status"] = "STOP_S5_FAIL_NONDISCRIMINATING"
        return out

    # S6
    cprime = 1 if Su == Sbeta else 2  # 2 encodes "-1"
    out["cprime_code"] = cprime  # 1 means c'=+1, 2 means c'=-1
    out["cprime"] = 1 if cprime == 1 else -1

    # S7/S8: discrete logs in mu_3(F_p), base = omega^mu3_gen_power (DC-2 uses power=2)
    omega_base = find_mu3_generator(p)
    omega = pow(omega_base, mu3_gen_power, p)
    k3 = discrete_log_mu3(Sbeta, omega, p)
    psi = discrete_log_mu3(Su, omega, p)
    out["omega_base_generator"] = omega_base
    out["omega_used"] = omega
    out["k3"] = k3
    out["psi"] = psi

    # S9: SELECT -- PENDING per instruction (census sign-convention not yet delivered).
    out["S9_SELECT"] = "PENDING_CENSUS_CONVENTION_NOT_PINNED"
    out["S9_psi_eq_k3"] = (psi == k3)

    out["status"] = "OK"
    return out


def run_stability(primes, sgn=1, label=""):
    """S10: repeat S1-S9 for each prime, check c' agrees across all."""
    results = [run_chain(p, sgn=sgn, label=label) for p in primes]
    statuses = [r["status"] for r in results]
    if not all(s == "OK" for s in statuses):
        return {"primes": primes, "results": results, "agree": None,
                "note": "not all primes reached OK status -- see individual results"}
    cprimes = [r["cprime"] for r in results]
    agree = len(set(cprimes)) == 1
    return {"primes": primes, "results": results, "cprimes": cprimes, "agree": agree}


def main():
    report = {}
    report["pins"] = {
        "u0inv": str(U0INV),
        "u0inv_source": "search/certs/ds4_receipt_v1_20260812.json field input_u0_inverse",
        "beta": BETA,
        "beta_source": "pin per instruction (sec.3.1 prediction)",
        "declared_convention_D_this_run": "sgn=+1 (u_S4 := u0inv literally, no extra inversion)",
    }

    # candidate primes p == 1 mod 9, p not dividing 2*3*5
    candidate_primes = [19, 37, 73, 109, 127, 163, 181, 199, 271, 307, 379, 397]

    # find primes satisfying condition (iii): Sbeta != 1 and Su != 1 (under sgn=+1)
    valid_primes = []
    invalid_prime_for_DC4 = None
    diag = []
    for p in candidate_primes:
        r = run_chain(p, sgn=1, label="scan")
        diag.append({"p": p, "status": r["status"], "Su": r.get("Su"), "Sbeta": r.get("Sbeta")})
        if r["status"] == "OK":
            valid_primes.append(p)
        elif r["status"] == "STOP_S5_FAIL_NONDISCRIMINATING" and invalid_prime_for_DC4 is None:
            invalid_prime_for_DC4 = p

    report["prime_scan"] = diag
    chosen_primes = valid_primes[:3]
    report["chosen_primes"] = chosen_primes

    if len(chosen_primes) < 3:
        report["STATUS"] = "STOP_INSUFFICIENT_VALID_PRIMES"
        print(json.dumps(report, indent=2))
        return

    # ================= main computation (S1-S10), declared convention D (sgn=+1) =================
    main_stability = run_stability(chosen_primes, sgn=1, label="main")
    report["main_computation"] = main_stability

    # ================= 432-key canary (sec.7.1) -- MUST pass before main computation is trusted ===
    # (computed separately in this same producer file; census + artifact read directly, no shared
    #  helper with the checker)
    census = json.load(open("search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json", encoding="utf-8"))
    cands = census["finite_index3_census"]["nonnormal_candidates"]
    nn09 = None
    nn12 = None
    for c in cands:
        if c["candidate_id"] == "IDX3-NN-09":
            nn09 = set(c["row_indices"])
        if c["candidate_id"] == "IDX3-NN-12":
            nn12 = set(c["row_indices"])
    if nn09 is None or nn12 is None:
        report["STATUS"] = "STOP_CENSUS_ROWS_NOT_FOUND"
        print(json.dumps(report, indent=2))
        return
    symdiff = nn09.symmetric_difference(nn12)
    art = json.load(open("search/certs/d972_b4_word_key_artifact_v1_20260816.json", encoding="utf-8"))
    rows = art["rows"]
    inv2_mod9 = 5  # 2*5=10=1 mod9
    bad_rows = []
    for idx in symdiff:
        _, key, word = rows[idx]
        m, delta, pi = key
        a1 = delta[0][0]
        k = (a1 * inv2_mod9) % 9
        k3 = k % 3
        if k3 == 0:
            bad_rows.append(idx)
    canary_432 = {
        "NN09_size": len(nn09), "NN12_size": len(nn12), "symdiff_size": len(symdiff),
        "expected_symdiff_size": 432,
        "bad_rows_with_K3_zero": bad_rows,
        "pass": (len(symdiff) == 432) and (len(bad_rows) == 0),
    }
    report["canary_432key"] = canary_432
    if not canary_432["pass"]:
        report["STATUS"] = "STOP_432_CANARY_FAILED"
        print(json.dumps(report, indent=2))
        return

    # ================= DC-1: orientation flip (sgn -> -1); c' must flip =================
    dc1_stability = run_stability(chosen_primes, sgn=-1, label="DC1_flipped")
    dc1_pass = None
    if main_stability["agree"] and dc1_stability["agree"]:
        dc1_pass = (main_stability["cprimes"][0] != dc1_stability["cprimes"][0])
    report["DC1_orientation_flip"] = {
        "flipped_results": dc1_stability,
        "original_cprime": main_stability["cprimes"][0] if main_stability["agree"] else None,
        "flipped_cprime": dc1_stability["cprimes"][0] if dc1_stability["agree"] else None,
        "pass_cprime_flipped": dc1_pass,
    }

    # ================= DC-2: embedding flip (use omega^2 as base); c' and psi==k3 relation invariant
    p0 = chosen_primes[0]
    orig = run_chain(p0, sgn=1, mu3_gen_power=1, label="DC2_orig")
    flipped = run_chain(p0, sgn=1, mu3_gen_power=2, label="DC2_flipped_gen")
    dc2_pass = (orig["cprime"] == flipped["cprime"]) and (orig["S9_psi_eq_k3"] == flipped["S9_psi_eq_k3"])
    report["DC2_embedding_flip"] = {
        "prime": p0, "orig_cprime": orig["cprime"], "flipped_gen_cprime": flipped["cprime"],
        "orig_k3_psi": [orig["k3"], orig["psi"]], "flipped_k3_psi": [flipped["k3"], flipped["psi"]],
        "pass_cprime_and_relation_invariant": dc2_pass,
    }

    # ================= DC-3: cube-number injection (a^-9 factor); Su must be unchanged =================
    a = Fraction(2)  # arbitrary rational
    a_pow_neg9 = a ** (-9)
    orig2 = run_chain(p0, sgn=1, u_extra_factor=Fraction(1), label="DC3_orig")
    injected = run_chain(p0, sgn=1, u_extra_factor=a_pow_neg9, label="DC3_injected")
    dc3_pass = (orig2["Su"] == injected["Su"])
    report["DC3_cube_injection"] = {
        "prime": p0, "a": str(a), "a_pow_neg9": str(a_pow_neg9),
        "orig_Su": orig2["Su"], "injected_Su": injected["Su"], "pass_Su_unchanged": dc3_pass,
    }

    # ================= DC-4: negative control (prime failing condition iii) =================
    if invalid_prime_for_DC4 is not None:
        dc4result = run_chain(invalid_prime_for_DC4, sgn=1, label="DC4_negative")
        dc4_pass = (dc4result["status"] == "STOP_S5_FAIL_NONDISCRIMINATING")
        report["DC4_negative_control"] = {
            "prime": invalid_prime_for_DC4, "result_status": dc4result["status"],
            "pass_correctly_stopped": dc4_pass,
        }
    else:
        report["DC4_negative_control"] = {"status": "NO_INVALID_PRIME_FOUND_IN_SCAN_RANGE"}

    # ================= DC-5: 3-prime agreement (== S10, already computed in main_computation) ======
    report["DC5_three_prime_agreement"] = {
        "agree": main_stability["agree"],
        "cprimes": main_stability.get("cprimes"),
        "caveat": "Agreement across 3 primes does NOT guarantee convention D's correctness (all primes "
                  "could be consistently reflecting a WRONG declared convention). This is a stability "
                  "check only, not a validity proof -- per sec.7.3.4 DC-5's own explicit caveat.",
    }

    report["conclusion_pending_u_dih"] = True
    report["conclusion_note"] = (
        "c' has been computed under the DECLARED convention D (sgn=+1) with 3-prime agreement "
        "(if DC5 agree=true). The final NN-09/NN-12 SELECT is NOT resolved (S9 census-sign-convention "
        "not yet pinned) and u_dih (the geometric anchor for convention D itself) has not been "
        "delivered. This report records raw values and two-system agreement only, per instruction."
    )

    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
