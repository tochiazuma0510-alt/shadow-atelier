#!/usr/bin/env python3
"""
search/aside2_run_single_prime.py -- ASIDE-2 (裁定708・fire authorized),
per docs/notes/aside_measurement_design_v1_addendum_c.md (commit 85827ca,
sha256 feedb42a1c39a717b3fc62dc53538a1e62e2e4c0f20f5f5c1460c86c21c75d51),
implemented verbatim.  This addendum SUPERSEDES ASIDE-1's stage B/C (the
plain free-Lie commutator used there was BRACKET_IMPL_FAIL, per the
addendum's own diagnosis of the search/aside1_run_single_prime.py S-AS-3
STOP) -- it does NOT modify aside1_run_single_prime.py (frozen), it reuses
stage A/D from it (sigma_m realization, already calibrated) and replaces
stage B/C with the addendum's Definition C-1 Ihara bracket, adding a new
stage E.

Usage: python search/aside2_run_single_prime.py <prime>

Stages (addendum SS4.3, verbatim):
  Stage A (reused unchanged from aside1_run_single_prime.sigma_m_ambient):
    sigma_m for m in {3,5,7,9}, dim S_m asserted ==1 (S-AS-1).
  Stage B' (replaces v1's plain-commutator stage B):
    v1 := ihara_bracket(sigma_3, sigma_9); v2 := ihara_bracket(sigma_5, sigma_7)
    A12_ihara := rank_Fp({v1,v2})   -- expected 2 at general primes (P-C-1),
    691's value is the primary/candidate measurement (P-C-4), NOT gated.
  Stage C' (replaces v1's plain-commutator stage C):
    f_m := ad(X)^(m-1)(Y); d2 := depth-2 component of ihara_bracket(f_a,f_b)
    A12_depth2_ihara := rank_Fp(d2) -- expected EXACTLY 1 at ALL primes
    (Theorem C-A, addendum SS2) -- S-AS-3' STOP if not, at ANY prime.
  Stage D (reused unchanged from aside1): sigma_m's depth-1 leading term
    proportional to ad(X)^(m-1)(Y).
  Stage E (NEW, addendum SS4.3): D := v1 - 3*v2 (the Ihara-Takao difference
    itself, in the model's full weight-12 element -- NOT just its depth-2
    projection). Reports D_is_zero, D's nonzero-term count by depth
    (d=2..12), and theta_ok (Lemma C-2 canary: theta(v1)+v1==0 etc, theta
    = the X<->Y letter-swap automorphism).

Fixture unit tests (addendum SS1.4) run FIRST, standalone (independent of
which prime is being dispatched, using p=2147483647 as an "exact-integer"
substitute since all fixture coefficients have |value|<=70, far below that
prime -- no modular wraparound risk). If the fixture mismatches, this
script STOPS before touching any prime-specific computation (S-AS-7,
per 司令塔 instruction: run the fixture full pass BEFORE anything else).

No verdict language (S-AS-5): only raw values and the pre-registered STOP
codes below.
"""
import json
import sys
import time

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
import aside1_run_single_prime as a1

FIXTURE_PRIME = 2147483647  # exact-integer substitute: all fixture
# coefficients have |value| <= 70, far below this prime, so mod-p results
# equal signed integers directly (after the to_signed conversion below).

AUTHORIZED_GENERAL_PRIMES = {2147483647, 998244353, 677, 701}  # 裁定711:
# 677/701 authorized as the S-ED-7 mid-size control pair (addendum SS4.3),
# expected to behave like the 2 large "general" primes (A12_ihara=2,
# A12_depth2_ihara=1, D nonzero) -- so they get the SAME S-AS-2' gate.
SPECIAL_PRIME = 691


def to_signed(c, p):
    c = c % p
    return c if c * 2 <= p else c - p


def theta_vec(v):
    """theta = the X<->Y letter-swap automorphism (letter 0=X <-> 1=Y),
    applied to an ambient word-vector (dict word-tuple:coeff)."""
    return {tuple(1 - letter for letter in w): c for w, c in v.items()}


def deriv(f, g, p):
    """D_f(g), the addendum's Definition C-1 derivation: D_f(X)=0,
    D_f(Y)=[Y,f], extended by Leibniz. Substitutes [Y,f] at every Y
    (letter==1) position of g's ambient words."""
    img = ed.word_bracket({(1,): 1 % p}, f, p)  # [Y, f]
    out = {}
    for w, c in g.items():
        for i, letter in enumerate(w):
            if letter != 1:
                continue
            prefix = w[:i]
            suffix = w[i + 1:]
            for w2, c2 in img.items():
                key = prefix + w2 + suffix
                val = (c * c2) % p
                new_val = (out.get(key, 0) + val) % p
                if new_val:
                    out[key] = new_val
                else:
                    out.pop(key, None)
    return out


def ihara_bracket(f, g, p):
    """{f,g} := D_f(g) - D_g(f) + [f,g] (addendum Definition C-1, variant
    V1 -- the unique-up-to-overall-sign convention fixed by reproducing
    Brown (1.7) via the addendum's own 5-variant enumeration, SS1.1)."""
    d1 = deriv(f, g, p)
    d2 = deriv(g, f, p)
    plain = ed.word_bracket(f, g, p)
    return ed.word_add([d1, ed.scale_vec(d2, -1, p), plain], p)


def check_fixture(p=FIXTURE_PRIME):
    """Addendum SS1.4 fixture: verify the exact ambient-word coefficient
    tables for {y2,y8}, {y4,y6} (Ihara bracket) and [y2,y8] (plain
    commutator, reference row), PLUS the B_i-basis reconstruction of
    {y2,y8}=6B1+27B2+48B3+42B4 and {y4,y6}=2B1+9B2+16B3+14B4. Returns
    (ok: bool, details: dict of every sub-check's pass/fail)."""
    details = {}
    y = {i: a1.ad_X_pow_Y(i, p) for i in range(0, 11)}
    B = {i: ed.word_bracket(y[i], y[10 - i], p) for i in range(0, 5)}

    ihara_28 = ihara_bracket(y[2], y[8], p)
    ihara_46 = ihara_bracket(y[4], y[6], p)
    plain_28 = ed.word_bracket(y[2], y[8], p)
    plain_46 = ed.word_bracket(y[4], y[6], p)

    # ambient word coefficient table, words X^i Y X^j Y (i+j=10, i=1..9)
    expected_ihara_28 = {1: 6, 2: -27, 3: 48, 4: -42, 5: 0, 6: 42, 7: -48, 8: 27, 9: -6}
    expected_ihara_46 = {1: 2, 2: -9, 3: 16, 4: -14, 5: 0, 6: 14, 7: -16, 8: 9, 9: -2}
    expected_plain_28 = {1: 6, 2: -27, 3: 56, 4: -70, 5: 56, 6: -28, 7: 8, 8: -1, 9: 0}

    word_table_ok = True
    word_table_detail = {}
    for i in range(1, 10):
        j = 10 - i
        word = (0,) * i + (1,) + (0,) * j + (1,)
        got_ihara_28 = to_signed(ihara_28.get(word, 0), p)
        got_ihara_46 = to_signed(ihara_46.get(word, 0), p)
        got_plain_28 = to_signed(plain_28.get(word, 0), p)
        row_ok = (got_ihara_28 == expected_ihara_28[i] and
                  got_ihara_46 == expected_ihara_46[i] and
                  got_plain_28 == expected_plain_28[i])
        word_table_detail[f"(i={i},j={j})"] = {
            "ihara_28": [got_ihara_28, expected_ihara_28[i]],
            "ihara_46": [got_ihara_46, expected_ihara_46[i]],
            "plain_28": [got_plain_28, expected_plain_28[i]],
            "row_ok": row_ok,
        }
        word_table_ok = word_table_ok and row_ok
    details["word_table_ok"] = word_table_ok
    details["word_table"] = word_table_detail

    # nonzero term counts
    term_counts = {
        "ihara_28": [len(ihara_28), 42], "ihara_46": [len(ihara_46), 42],
        "plain_28": [len(plain_28), 42], "plain_46": [len(plain_46), 40],
    }
    term_counts_ok = all(v[0] == v[1] for v in term_counts.values())
    details["term_counts_ok"] = term_counts_ok
    details["term_counts"] = term_counts

    # B_i-basis reconstruction
    recon_28 = ed.word_add([ed.scale_vec(B[1], 6, p), ed.scale_vec(B[2], 27, p),
                             ed.scale_vec(B[3], 48, p), ed.scale_vec(B[4], 42, p)], p)
    recon_46 = ed.word_add([ed.scale_vec(B[1], 2, p), ed.scale_vec(B[2], 9, p),
                             ed.scale_vec(B[3], 16, p), ed.scale_vec(B[4], 14, p)], p)
    diff_28 = ed.word_add([ihara_28, ed.scale_vec(recon_28, -1, p)], p)
    diff_46 = ed.word_add([ihara_46, ed.scale_vec(recon_46, -1, p)], p)
    recon_ok = (not diff_28) and (not diff_46)
    details["recon_ok"] = recon_ok

    # Theorem C-A itself: {y2,y8} - 3*{y4,y6} == 0 (exact, at this prime)
    ca_diff = ed.word_add([ihara_28, ed.scale_vec(ihara_46, -3, p)], p)
    theorem_ca_ok = not ca_diff
    details["theorem_ca_ok"] = theorem_ca_ok

    ok = word_table_ok and term_counts_ok and recon_ok and theorem_ca_ok
    return ok, details


def run_prime(p, fixture_ok):
    out = {
        "schema": "shadow-atelier/aside2/v1",
        "authority": "裁定708 (司令塔), ASIDE-2 per docs/notes/aside_measurement_design_v1_addendum_c.md "
                      "(commit 85827ca, verbatim) -- supersedes ASIDE-1 stage B/C",
        "prime": p,
        "fixture_ok_this_run": fixture_ok,
        "no_verdict_note": "S-AS-5 compliance: this script emits ONLY raw numeric values and the "
                            "pre-registered STOP codes (SIGMA_NONUNIQUE / CALIBRATION_FAIL / "
                            "BRACKET_IMPL_FAIL / FIXTURE_MISMATCH / BRACKET_NOT_GRT / IMPOSSIBLE_CELL) "
                            "-- no interpretive verdict prose of the kinds forbidden in the design addendum "
                            "S6 is written anywhere in this cert.",
    }
    stop_code = None
    if not fixture_ok:
        out["stop_code"] = "FIXTURE_MISMATCH"
        return out

    h_alg = ed.GradedLie(2, a1.KMAX, p, sparse_degrees=set(range(1, a1.KMAX + 1)))

    # Stage A (reused unchanged)
    sigmas = {}
    stage_a = {}
    for m in a1.SIGMA_DEGREES:
        H_dim, S_dim, ambient, lead_word = a1.sigma_m_ambient(m, h_alg, p)
        stage_a[m] = {"H_dim": H_dim, "S_dim": S_dim,
                      "sigma_norm_ok": (S_dim == 1 and ambient is not None),
                      "lead_word": list(lead_word) if lead_word is not None else None}
        print(f"p={p} stage A m={m}: H_dim={H_dim} S_dim={S_dim} sigma_ok={stage_a[m]['sigma_norm_ok']}", flush=True)
        if S_dim != 1:
            stop_code = "SIGMA_NONUNIQUE"
            break
        sigmas[m] = ambient
    out["stage_A_sigma"] = stage_a
    if stop_code:
        out["stop_code"] = stop_code
        return out

    # Stage B' (Ihara bracket, weight-graded, replaces v1's stage B)
    v1 = ihara_bracket(sigmas[3], sigmas[9], p)
    v2 = ihara_bracket(sigmas[5], sigmas[7], p)
    A12_ihara = a1.rank_of_two_ambient_vectors(v1, v2, p)
    print(f"p={p} stage B': A12_ihara={A12_ihara}", flush=True)

    is_general = p in AUTHORIZED_GENERAL_PRIMES
    if is_general and A12_ihara != 2:
        stop_code = "CALIBRATION_FAIL"

    # Stage C' (Ihara bracket, depth-2, replaces v1's stage C)
    f = {m: a1.ad_X_pow_Y(m - 1, p) for m in a1.SIGMA_DEGREES}
    ihara_39 = ihara_bracket(f[3], f[9], p)
    ihara_57 = ihara_bracket(f[5], f[7], p)
    d2_39 = a1.project_depth(ihara_39, 2)
    d2_57 = a1.project_depth(ihara_57, 2)
    A12_depth2_ihara = a1.rank_of_two_ambient_vectors(d2_39, d2_57, p)
    print(f"p={p} stage C': A12_depth2_ihara={A12_depth2_ihara}", flush=True)
    if A12_depth2_ihara != 1:
        stop_code = "BRACKET_IMPL_FAIL"

    out["stage_B_prime_ihara_weight_graded"] = {
        "v1_num_terms": len(v1), "v2_num_terms": len(v2), "A12_ihara": A12_ihara,
    }
    out["stage_C_prime_ihara_depth2"] = {
        "d2_39_num_terms": len(d2_39), "d2_57_num_terms": len(d2_57),
        "A12_depth2_ihara": A12_depth2_ihara,
    }

    # canary C-c / S-AS-8: theta(v1)+v1==0, theta(v2)+v2==0
    t1 = ed.word_add([theta_vec(v1), v1], p)
    t2 = ed.word_add([theta_vec(v2), v2], p)
    theta_ok = (not t1) and (not t2)
    out["theta_ok"] = theta_ok
    print(f"p={p} theta_ok={theta_ok}", flush=True)
    if not theta_ok and stop_code is None:
        stop_code = "BRACKET_NOT_GRT"

    if stop_code:
        out["stop_code"] = stop_code
        return out

    # Stage D (reused unchanged: proportionality of sigma_m's depth-1
    # leading term to ad(X)^(m-1)(Y))
    stage_d = {}
    for m in a1.SIGMA_DEGREES:
        sigma_depth1 = a1.project_depth(sigmas[m], 1)
        prop = a1.proportional(sigma_depth1, f[m], p)
        stage_d[m] = {"proportional_to_adXpow_Y": prop}
    out["stage_D_bh_crosscheck"] = stage_d
    print(f"p={p} stage D: {stage_d}", flush=True)

    # Stage E (NEW): D := v1 - 3*v2, depth profile d=2..12, D_is_zero
    D = ed.word_add([v1, ed.scale_vec(v2, -3, p)], p)
    D_is_zero = (not D)
    depth_profile = {}
    for d in range(2, 13):
        proj = a1.project_depth(D, d)
        depth_profile[d] = len(proj)
    out["stage_E_D_ihara_takao_difference"] = {
        "D_is_zero": D_is_zero,
        "D_num_terms_total": len(D),
        "D_depth_profile": depth_profile,
    }
    print(f"p={p} stage E: D_is_zero={D_is_zero} depth_profile={depth_profile}", flush=True)

    out["stop_code"] = None
    return out


def main():
    if len(sys.argv) != 2:
        print("usage: aside2_run_single_prime.py <prime>", file=sys.stderr)
        sys.exit(2)
    p = int(sys.argv[1])

    t_start = time.time()
    print(f"=== ASIDE-2: JOB START prime={p} ===", flush=True)

    print("running fixture unit tests (addendum SS1.4) FIRST, standalone, before any prime-specific work...", flush=True)
    fixture_ok, fixture_details = check_fixture()
    print(f"fixture_ok={fixture_ok}", flush=True)
    if not fixture_ok:
        print("FIXTURE MISMATCH -- STOP before touching prime-specific computation", flush=True)

    out = run_prime(p, fixture_ok)
    out["fixture_check"] = fixture_details
    out["total_elapsed_sec"] = round(time.time() - t_start, 2)

    out_path = f"search/certs/aside2_prime_{p}_v2_20260806.json"
    with open(out_path, "w", encoding="utf-8") as f_out:
        json.dump(out, f_out, indent=2, ensure_ascii=False)

    stop_code = out.get("stop_code")
    print(f"=== ASIDE-2: JOB END prime={p} total_elapsed_sec={out['total_elapsed_sec']} stop_code={stop_code} ===", flush=True)
    print(f"Wrote {out_path}", flush=True)
    if stop_code:
        print("ASIDE2_STOP", flush=True)
        sys.exit(1)
    print("ASIDE2_DONE", flush=True)


if __name__ == "__main__":
    main()
