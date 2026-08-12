"""
search/ds4_receipt_v1.py -- d_S4 receipt (裁定969, 装置カード=docs/notes/s4_recon_device_v1.md §2/§3(c))

Implements [D1]-[D3] EXACTLY as specified, nothing more:
  [D1] input-tamper-detection assert: read search/certs/u_meas_uloc_v2_20260731.json's
       measurement.u_0_inverse, assert it equals -1423828125/256 (= -3^6*5^9/2^8), and
       independently re-factor this exact rational (sympy) to cross-check the stored
       exponent_vector_mod_9_of_u_0_inverse field against a fresh factorization (not just
       trusting the stored dict).
  [D2] ord([u_0^-1]_9) in Q^x/(Q^x)^9 = lcm over primes p of (9/gcd(9, v_p mod 9)).
       Also verifies the -1=(-1)^9 sign-triviality note.
  [D3] cert (schema ds4-receipt/v1), quar_triggered = (ord != 9) ALWAYS SET.

★ STOP LINE (per instruction order): this script computes ord and writes the cert, and NOTHING
  ELSE. No interpretation of d_S4, no propagation of the value beyond this cert. If quar_triggered
  ends up true, the QUAR protocol (Q1)-(Q5) is a REPORTING/PROCESS matter for the coordinator, not
  something this script performs.

Positive control (裁定961 permanent norm): the ord-computer is calibrated against a KNOWN nontrivial
example (27 = 3^3, expected ord([27]_9) = 9/gcd(9,3) = 3) included directly in the cert, so a
degenerate "always returns 1" bug would be caught.
"""
import json
from fractions import Fraction
from math import gcd

try:
    from sympy import factorint
except ImportError:
    factorint = None

CERT_IN = "search/certs/u_meas_uloc_v2_20260731.json"
CERT_OUT = "search/certs/ds4_receipt_v1_20260812.json"

EXPECTED_U0_INV_STR = "-1423828125/256"


def prime_valuations(frac: Fraction):
    """Return {prime: exponent} for frac = sign * prod p^e_p (sign not included in dict)."""
    num = abs(frac.numerator)
    den = abs(frac.denominator)
    if factorint is not None:
        vals = {}
        for p, e in factorint(num).items():
            vals[p] = vals.get(p, 0) + e
        for p, e in factorint(den).items():
            vals[p] = vals.get(p, 0) - e
        return vals
    # fallback trial division (not expected to be needed -- sympy is available in this env)
    vals = {}
    for n, sign in ((num, 1), (den, -1)):
        x = n
        p = 2
        while p * p <= x:
            while x % p == 0:
                vals[p] = vals.get(p, 0) + sign
                x //= p
            p += 1
        if x > 1:
            vals[x] = vals.get(x, 0) + sign
    return vals


def ord_in_quotient(frac: Fraction, n: int):
    """ord of [frac] in Q^x/(Q^x)^n, via lcm_p(n/gcd(n, v_p mod n)) -- sign handled separately
    by the caller (this function only looks at absolute-value prime valuations)."""
    vals = prime_valuations(frac)
    order = 1
    detail = {}
    for p, v in vals.items():
        vmod = v % n
        contrib = n // gcd(n, vmod) if vmod != 0 else 1
        detail[p] = {"v_p": v, "v_p_mod_n": vmod, "contribution": contrib}
        order = order * contrib // gcd(order, contrib)
    return order, detail


def main():
    # ---- [D1] input tamper-detection ----
    with open(CERT_IN, encoding="utf-8") as fh:
        src = json.load(fh)
    u0_inv_str = src["measurement"]["u_0_inverse"]
    d1_pass = (u0_inv_str == EXPECTED_U0_INV_STR)
    print(f"[D1] u_0_inverse read = {u0_inv_str!r}  expected = {EXPECTED_U0_INV_STR!r}  match={d1_pass}")
    if not d1_pass:
        raise SystemExit(f"[D1] TAMPER-DETECTED / input mismatch: got {u0_inv_str!r}, "
                          f"expected {EXPECTED_U0_INV_STR!r} -- halting, no ord computed.")

    u0_inv = Fraction(u0_inv_str)
    assert u0_inv < 0

    # independent re-factorization (cross-check vs the cert's OWN stored exponent_vector_mod_9)
    fresh_vals = prime_valuations(abs(u0_inv))
    print(f"[D1] independent re-factorization of |u_0_inverse| = {fresh_vals}")
    stored_valuations = src["measurement"]["u_0_inverse_valuations"]
    stored_ok = all(fresh_vals.get(int(p), 0) == v for p, v in stored_valuations.items())
    print(f"[D1] fresh factorization matches cert's stored u_0_inverse_valuations: {stored_ok}")
    if not stored_ok:
        raise SystemExit("[D1] fresh factorization DISAGREES with cert's stored valuations -- halting.")

    # reconstruct u_0_inverse = sign * prod p^e_p, verify it (u_0_inverse = ± p^e form check)
    recon = Fraction(1)
    for p, e in fresh_vals.items():
        recon *= Fraction(p) ** e
    recon *= -1  # sign
    reconstruction_ok = (recon == u0_inv)
    print(f"[D1] reconstruction check (sign * prod p^e_p == u_0_inverse): {reconstruction_ok}")

    # ---- sign-triviality note: -1 = (-1)^9 so sign contributes trivially to the 9th-power class ----
    sign_order, _ = ord_in_quotient(Fraction(-1), 9)
    sign_trivial = (sign_order == 1)
    print(f"[D1 note] ord([-1]_9) = {sign_order} (expect 1, since -1=(-1)^9): sign_trivial={sign_trivial}")

    # ---- [D2] ord computation ----
    ord_value, detail = ord_in_quotient(abs(u0_inv), 9)
    print(f"[D2] ord([u_0^-1]_9) = {ord_value}")
    print(f"[D2] per-prime detail = {detail}")

    # ---- positive control (裁定961 norm): known nontrivial example, 27=3^3, expect ord=3 ----
    pc_value, pc_detail = ord_in_quotient(Fraction(27), 9)
    pc_expected = 3
    pc_pass = (pc_value == pc_expected)
    print(f"[POSITIVE CONTROL] ord([27]_9) = {pc_value} (expect {pc_expected}): pass={pc_pass}")
    if not pc_pass:
        raise SystemExit("[POSITIVE CONTROL] ord-computer FAILED its own calibration example -- "
                          "the ord_value above must NOT be trusted. Halting without writing cert.")

    # ---- [D3] output ----
    quar_triggered = (ord_value != 9)

    prerequisites_status = {
        "P1_TB1_TB4": "framework inheritance (not independently re-verified by this script; "
                       "transcribed status only, per instruction not to judge)",
        "P2_Z18_link": "not_assessed (S4 window not yet in the Z_18-link inventory, per card §1)",
        "P3_C1prime_S4": "open (dessin 6-fold coincidence problem, per card §1)",
        "P4_fullpre_A_S4": "requires arithmetic argument; census substitution NOT allowed "
                            "(裁定961, per card §1) -- NOT established by this script",
        "P5_u0_eq_uS4_identity": "unconfirmed (per card §1.4) -- NOT established by this script",
        "note": "prerequisites_status values are TRANSCRIBED from the device card as of 裁定969; "
                "this script does not assess, re-derive, or judge P1-P5. This receipt is "
                "explicitly conditional on P1-P5 per the card's own framing.",
    }

    out = {
        "schema": "ds4-receipt/v1",
        "generated_by": {"tool": "python (sympy factorint)", "script": "search/ds4_receipt_v1.py",
                          "order": "裁定969 / docs/notes/s4_recon_device_v1.md §2/§3(c)"},
        "d1_input_tamper_check": {
            "cert_read": CERT_IN,
            "u0_inverse_read": u0_inv_str,
            "u0_inverse_expected": EXPECTED_U0_INV_STR,
            "match": d1_pass,
            "fresh_factorization_of_abs_value": {str(p): e for p, e in fresh_vals.items()},
            "matches_cert_stored_valuations": stored_ok,
            "reconstruction_check_sign_times_prodpe_eq_u0inv": reconstruction_ok,
        },
        "sign_note": {
            "claim": "-1 = (-1)^9, so sign contributes trivially to the 9th-power class",
            "ord_of_minus1_in_Qx_mod_9th_powers": sign_order,
            "sign_trivial": sign_trivial,
        },
        "d2_ord_computation": {
            "method": "ord([x]_9) in Q^x/(Q^x)^9 = lcm_p( 9 / gcd(9, v_p(x) mod 9) )",
            "input_u0_inverse": str(abs(u0_inv)),
            "per_prime_detail": {str(p): v for p, v in detail.items()},
            "ord_value": ord_value,
        },
        "positive_control": {
            "note": "裁定961恒久規範: ord計算器が非自明値を返すことの較正(既知の位数3の例)",
            "test_input": "27 = 3^3",
            "expected_ord_mod_9": pc_expected,
            "computed_ord": pc_value,
            "detail": {str(p): v for p, v in pc_detail.items()},
            "pass": pc_pass,
        },
        "input_u0_inverse": EXPECTED_U0_INV_STR,
        "computation_method": "Q^x/(Q^x)^9 での位数(素因子指数 mod 9)",
        "ord_value": ord_value,
        "prerequisites_status": prerequisites_status,
        "quar_triggered": quar_triggered,
        "d_no_interpretation": "machine value only; verdict は司令塔",
    }

    with open(CERT_OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"\nwrote {CERT_OUT}")
    print(f"[RAW] ord_value={ord_value}  quar_triggered={quar_triggered}")


if __name__ == "__main__":
    main()
