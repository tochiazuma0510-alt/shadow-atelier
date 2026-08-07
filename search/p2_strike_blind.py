import json
from fractions import Fraction as F
from math import gcd

def bernoulli(n):
    A = [F(0)] * (n + 1)
    for m in range(n + 1):
        A[m] = F(1, m + 1)
        for j in range(m, 0, -1):
            A[j - 1] = j * (A[j - 1] - A[j])
    return A[0]

def p_adic_val(num, p):
    if num == 0:
        return None  # undefined / infinite, flag
    v = 0
    n = abs(num)
    while n % p == 0:
        n //= p
        v += 1
    return v

def legendre_vp_factorial(n, p):
    v = 0
    pk = p
    while pk <= n:
        v += n // pk
        pk *= p
    return v

def val_mod_p2(k, p):
    Bk = bernoulli(k)
    frac = Bk / k
    num = frac.numerator
    den = frac.denominator
    modulus = p * p
    g = gcd(den, modulus)
    if g != 1:
        return None, True  # anomaly
    inv_den = pow(den % modulus, -1, modulus)
    return (num * inv_den) % modulus, False

targets = [
    (37,32), (59,44), (67,58), (101,68), (103,24),
    (131,22), (149,130), (157,62), (157,110)
]

results = []
canary_all_pass = True
stop_code = None

# Algorithm P2-A for all 9
for (p, k0) in targets:
    k_star = k0 + p - 1
    Bkstar = bernoulli(k_star)
    num = abs(Bkstar.numerator)
    v_p_num_B = p_adic_val(num, p)
    if v_p_num_B is None:
        v_p_num_B = -1  # numerator was zero, flag distinctly
    v_p_kfact = legendre_vp_factorial(k_star, p)
    v_p_zeta = v_p_num_B - v_p_kfact
    canary_pass = (v_p_num_B >= 1)
    if not canary_pass:
        canary_all_pass = False
    results.append({
        "p": p, "k0": k0, "k_star": k_star,
        "v_p_num_B": v_p_num_B, "v_p_kfact": v_p_kfact, "v_p_zeta": v_p_zeta,
        "alpha_raw": None, "beta": None, "j_star": None,
        "degenerate_case": None,
        "canary_v_ge_1_pass": canary_pass,
        "denominator_anomaly_at_k0": False,
        "denominator_anomaly_at_kstar": False,
    })

if not canary_all_pass:
    stop_code = "CANARY_FAIL"
    out = {
        "targets": results,
        "canary_all_pass": canary_all_pass,
        "stop_code": stop_code,
    }
    with open(r"C:\Users\81905\Desktop\shadow-atelier\scratchpad\p2_strike_blind_raw.json", "w") as f:
        json.dump(out, f, indent=2)
    print("CANARY FAILED. Stopping. Details:")
    for r in results:
        if not r["canary_v_ge_1_pass"]:
            print(r)
    raise SystemExit(0)

# Algorithm B' for all 9 (only runs if canary passed for all)
for r in results:
    p = r["p"]; k0 = r["k0"]; k_star = r["k_star"]

    val0, anomaly0 = val_mod_p2(k0, p)
    val1, anomaly1 = val_mod_p2(k_star, p)
    r["denominator_anomaly_at_k0"] = anomaly0
    r["denominator_anomaly_at_kstar"] = anomaly1

    if anomaly0 or anomaly1:
        r["degenerate_case"] = "DENOMINATOR_HAS_P_FACTOR"
        continue

    # alpha_raw = val0 // p, flag if not exactly divisible
    alpha_exact = (val0 % p == 0)
    alpha_raw = val0 // p  # floor div regardless; flag if not exact
    val1_div_exact = (val1 % p == 0)
    sum_raw = val1 // p

    r["alpha_raw"] = alpha_raw
    r["_alpha_exact_divisibility"] = alpha_exact
    r["_val1_exact_divisibility"] = val1_div_exact
    r["_val0_mod_p2"] = val0
    r["_val1_mod_p2"] = val1

    beta = (sum_raw - alpha_raw) % p
    r["beta"] = beta

    if beta != 0:
        j_star = (-alpha_raw * pow(beta, p - 2, p)) % p
        r["j_star"] = j_star
        r["degenerate_case"] = "unique"
    else:
        if alpha_raw % p != 0:
            r["j_star"] = None
            r["degenerate_case"] = "no_j_star"
        else:
            r["j_star"] = None
            r["degenerate_case"] = "all_j_degenerate"

out = {
    "targets": results,
    "canary_all_pass": canary_all_pass,
    "stop_code": stop_code,
}
with open(r"C:\Users\81905\Desktop\shadow-atelier\scratchpad\p2_strike_blind_raw.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"{'p':>4} {'k0':>4} {'k*':>4} {'vB':>3} {'vk!':>4} {'vzeta':>6} {'alpha':>6} {'beta':>5} {'j*/class':>16}")
for r in results:
    cls = r["j_star"] if r["j_star"] is not None else r["degenerate_case"]
    print(f"{r['p']:>4} {r['k0']:>4} {r['k_star']:>4} {r['v_p_num_B']:>3} {r['v_p_kfact']:>4} {r['v_p_zeta']:>6} {str(r['alpha_raw']):>6} {str(r['beta']):>5} {str(cls):>16}")

exceptions = [r for r in results if r["v_p_num_B"] >= 2]
print("\nCanary all pass:", canary_all_pass)
print("Exceptions (v_p_num_B >= 2):", [(r["p"], r["k0"], r["v_p_num_B"]) for r in exceptions])
print("Denominator anomalies:", [(r["p"], r["k0"]) for r in results if r["denominator_anomaly_at_k0"] or r["denominator_anomaly_at_kstar"]])
print("Non-exact alpha/val1 divisibility flags:", [(r["p"], r["k0"], r.get("_alpha_exact_divisibility"), r.get("_val1_exact_divisibility")) for r in results if r.get("_alpha_exact_divisibility") is False or r.get("_val1_exact_divisibility") is False])
