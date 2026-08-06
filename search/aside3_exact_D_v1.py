#!/usr/bin/env python3
"""
search/aside3_exact_D_v1.py -- RDV-1 (裁定717・最優先), per
docs/notes/ideas_ribet_dig_v2.md 札 RDV-1 (commit b1a3c6e,
sha256 0e917c4794b678ccbaf420387b6c484aa4d5d8b926936520bd14d1ce078d086e),
implemented verbatim.

Computes D := {sigma_3,sigma_9} - 3*{sigma_5,sigma_7} in EXACT RATIONAL
arithmetic (not mod p), using the addendum-C Ihara bracket (search/
aside2_run_single_prime.py's Definition C-1, unchanged/reused).

Method (multi-prime CRT + rational reconstruction, as RDV-1's own text
anticipates as the fallback path -- "有理係数爆発が出たら多素数CRT再構成で
代替", used here as the PRIMARY method since the existing sigma_m_ambient/
theta/tau pipeline is built on numpy int64 modular arithmetic verified only
up to p<=2^31-1 (mat_mul_modp_np_safe's own documented range), so a literal
from-scratch Fraction-based Gaussian elimination reimplementation of the
whole H/S extraction pipeline was judged higher-risk (new code, new bugs)
than reusing the ALREADY-VERIFIED mod-p pipeline at several large primes
and reconstructing the exact rational via CRT + Wang's algorithm):

  1. Run the (already patched, aside1) sigma_m_ambient at RECON_PRIMES
     (4 primes, each <2^31, product ~1.6e37) for m in {3,5,7,9}.
  2. Verify each prime picks the SAME lead_word (S_m is 1-dim over Q, so
     the true leading Lyndon coordinate is prime-independent UNLESS some
     prime coincidentally divides that one true numerator -- checked, not
     assumed).
  3. CRT-combine each ambient-word coefficient across the 4 primes' residues,
     then rational-reconstruct (Wang/extended-Euclid) to get an exact
     Fraction. Fail-closed: every reconstructed Fraction is re-reduced mod
     EVERY reconstruction prime and checked against the original residue.
  4. Ihara-bracket sigma_3,sigma_9 and sigma_5,sigma_7 using an EXACT
     (Fraction, no modulus) reimplementation of Definition C-1 (deriv/
     ihara_bracket), producing v1_Q, v2_Q, D_Q = v1_Q - 3*v2_Q exactly.
  5. Per-depth (d=2..12) report: nonzero term count, "content" (the
     rational c = gcd(numerators)/lcm(denominators), sign fixed positive,
     such that D^(d)/c is a primitive integer vector), v_691(content).
  6. Check content(D^(4)) against 691/144 up to sign.
  7. Report v_691(D^(6)) specifically (RDV-2's "the only excess bit").
  8. Canary: reduce v1_Q,v2_Q,D_Q mod each of the 5 existing aside2-cert
     primes {691,677,701,998244353,2147483647} and compare term-count
     profiles / A12_ihara against the already-committed aside2 certs
     (read-only cross-check, not re-derivation of those certs).
  9. theta mirror check at EXACT rational level: D^(12-d) == -theta(D^(d))
     for every d (Fraction equality, no rounding).

No verdict language (S-AS-5 discipline continued): only raw values and the
pre-registered STOP codes. S12@691 not touched (blind). Pure Python
(fractions + the existing numpy-int64 mod-p pipeline for reconstruction
inputs only -- no GAP).
"""
import json
import sys
import time
from fractions import Fraction
from math import gcd, isqrt

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
import aside1_run_single_prime as a1
import aside2_run_single_prime as a2

RECON_PRIMES = [2147483647, 998244353, 2000000011, 2000000033]
CANARY_PRIMES = [691, 677, 701, 998244353, 2147483647]
CANARY_CERT_PATHS = {p: f"search/certs/aside2_prime_{p}_v2_20260806.json" for p in CANARY_PRIMES}


# ---------- CRT + rational reconstruction ----------

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)


def crt_combine(a1_, m1, a2_, m2):
    g, p_, q_ = egcd(m1, m2)
    assert g == 1, "reconstruction primes must be pairwise coprime"
    lcm = m1 * m2
    x = (a1_ * q_ * m2 + a2_ * p_ * m1) % lcm
    return x % lcm, lcm


def rational_reconstruct(a, m):
    """Wang's algorithm: find (num,den) with num/den == a (mod m),
    |num|,|den| <= sqrt(m/2). Raises ValueError if reconstruction fails
    (bound exceeded / not coprime)."""
    a = a % m
    old_r, r = a, m
    old_s, s = 1, 0
    bound = isqrt(m // 2)
    while r > bound:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if s == 0:
        raise ValueError("rational reconstruction failed: s=0")
    g = gcd(abs(r), abs(s))
    if g != 1:
        raise ValueError(f"rational reconstruction failed: gcd(r,s)={g} != 1")
    if s < 0:
        r, s = -r, -s
    return Fraction(r, s)


def reconstruct_ambient_dict(prime_dicts):
    """prime_dicts: {prime: ambient-word-dict (word tuple -> int residue)}.
    Returns exact Fraction-valued ambient dict, fail-closed verified against
    every input prime's residue."""
    primes = sorted(prime_dicts.keys())
    all_keys = set()
    for d in prime_dicts.values():
        all_keys |= set(d.keys())
    out = {}
    for key in sorted(all_keys):
        a, m = prime_dicts[primes[0]].get(key, 0) % primes[0], primes[0]
        for p in primes[1:]:
            a2_ = prime_dicts[p].get(key, 0) % p
            a, m = crt_combine(a, m, a2_, p)
        frac = rational_reconstruct(a, m)
        for p in primes:
            den_mod = frac.denominator % p
            expected = prime_dicts[p].get(key, 0) % p
            if den_mod == 0:
                raise ValueError(f"reconstructed denominator divisible by reconstruction prime {p} "
                                  f"at key={key} -- reconstruction prime set is singular for this "
                                  f"coefficient, need a different prime set (SCOPE: not expected for "
                                  f"the RECON_PRIMES chosen; if hit, STOP and report)")
            val = (frac.numerator % p) * pow(den_mod, -1, p) % p
            if val != expected:
                raise ValueError(f"reconstruction verify FAILED at key={key} prime={p}: "
                                  f"got {val} expected {expected}")
        if frac != 0:
            out[key] = frac
    return out


# ---------- exact (Fraction) ring operations, mirroring aside2's mod-p ones ----------

def q_word_add(vecs):
    out = {}
    for vec in vecs:
        for w, c in vec.items():
            out[w] = out.get(w, Fraction(0)) + c
    return {w: c for w, c in out.items() if c != 0}


def q_scale(vec, c):
    return {w: (v * c) for w, v in vec.items() if v * c != 0}


def q_word_bracket(u, v):
    out = {}
    for w1, c1 in u.items():
        for w2, c2 in v.items():
            c = c1 * c2
            if c == 0:
                continue
            k1, k2 = w1 + w2, w2 + w1
            out[k1] = out.get(k1, Fraction(0)) + c
            out[k2] = out.get(k2, Fraction(0)) - c
    return {w: c for w, c in out.items() if c != 0}


def q_deriv(f, g):
    img = q_word_bracket({(1,): Fraction(1)}, f)  # [Y,f]
    out = {}
    for w, c in g.items():
        for i, letter in enumerate(w):
            if letter != 1:
                continue
            prefix, suffix = w[:i], w[i + 1:]
            for w2, c2 in img.items():
                key = prefix + w2 + suffix
                out[key] = out.get(key, Fraction(0)) + c * c2
    return {w: c for w, c in out.items() if c != 0}


def q_ihara_bracket(f, g):
    d1 = q_deriv(f, g)
    d2 = q_deriv(g, f)
    plain = q_word_bracket(f, g)
    return q_word_add([d1, q_scale(d2, -1), plain])


def q_theta(v):
    return {tuple(1 - letter for letter in w): c for w, c in v.items()}


def q_depth(word):
    return sum(1 for letter in word if letter == 1)


def q_project_depth(vec, d):
    return {w: c for w, c in vec.items() if q_depth(w) == d}


def content_of(vec):
    """Rational content: the (positive) c such that vec/c is a primitive
    integer vector. Computed correctly as: L := lcm(denominators); w_i :=
    numerator_i * (L // denominator_i) (so L*vec = integer vector w);
    c := gcd(w_i) / L. (NOTE: gcd(numerators) alone is WRONG unless all
    denominators agree -- w_i is numerator_i scaled by L/denominator_i,
    not numerator_i itself, whenever denominators differ across entries.)
    vec must be nonempty (raises otherwise, caller's responsibility)."""
    if not vec:
        return Fraction(0)
    den_lcm = 1
    for c in vec.values():
        den_lcm = den_lcm * c.denominator // gcd(den_lcm, c.denominator)
    num_gcd = 0
    for c in vec.values():
        w = c.numerator * (den_lcm // c.denominator)
        num_gcd = gcd(num_gcd, abs(w))
    return Fraction(num_gcd, den_lcm)


def valuation(frac, p):
    """p-adic valuation of a nonzero Fraction (integer, possibly negative)."""
    if frac == 0:
        return None
    n, d = abs(frac.numerator), frac.denominator
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    while d % p == 0:
        d //= p
        v -= 1
    return v


def factorize_small(n):
    """Trial-division factorization of a positive integer (small/moderate
    size expected here -- weight-12 combinatorial coefficients)."""
    n = abs(n)
    if n == 0:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def main():
    t_start = time.time()
    print("=== ASIDE-3 (RDV-1): JOB START -- exact rational D ===", flush=True)

    # ---- step 1+2: realize sigma_m at each reconstruction prime, verify
    # lead_word agreement ----
    per_prime_sigma = {m: {} for m in a1.SIGMA_DEGREES}
    lead_words = {m: None for m in a1.SIGMA_DEGREES}
    lead_word_mismatch = {}
    dims = {m: None for m in a1.SIGMA_DEGREES}
    for p in RECON_PRIMES:
        t0 = time.time()
        h_alg = ed.GradedLie(2, a1.KMAX, p, sparse_degrees=set(range(1, a1.KMAX + 1)))
        for m in a1.SIGMA_DEGREES:
            H_dim, S_dim, ambient, lead_word = a1.sigma_m_ambient(m, h_alg, p)
            if S_dim != 1:
                print(f"p={p} m={m}: S_dim={S_dim} != 1 -- SIGMA_NONUNIQUE / STOP", flush=True)
                write_stop("SIGMA_NONUNIQUE", {"prime": p, "m": m, "S_dim": S_dim})
                return
            per_prime_sigma[m][p] = ambient
            if dims[m] is None:
                dims[m] = (H_dim, S_dim)
            if lead_words[m] is None:
                lead_words[m] = lead_word
            elif tuple(lead_word) != tuple(lead_words[m]):
                lead_word_mismatch[m] = lead_word_mismatch.get(m, []) + [(p, lead_word)]
        print(f"prime={p}: sigma_m realized for m={a1.SIGMA_DEGREES}, elapsed={time.time()-t0:.1f}s", flush=True)

    if lead_word_mismatch:
        print(f"lead_word MISMATCH across reconstruction primes: {lead_word_mismatch} -- STOP", flush=True)
        write_stop("LEAD_WORD_MISMATCH", {"detail": {str(k): v for k, v in lead_word_mismatch.items()}})
        return

    # ---- step 3: CRT + rational reconstruction ----
    sigma_Q = {}
    for m in a1.SIGMA_DEGREES:
        t0 = time.time()
        try:
            sigma_Q[m] = reconstruct_ambient_dict(per_prime_sigma[m])
        except ValueError as exc:
            print(f"m={m}: reconstruction FAILED: {exc} -- STOP", flush=True)
            write_stop("RECONSTRUCTION_FAIL", {"m": m, "error": str(exc)})
            return
        print(f"sigma_{m}^Q reconstructed: {len(sigma_Q[m])} terms, elapsed={time.time()-t0:.1f}s", flush=True)

    # ---- step 4: exact Ihara brackets ----
    v1_Q = q_ihara_bracket(sigma_Q[3], sigma_Q[9])
    v2_Q = q_ihara_bracket(sigma_Q[5], sigma_Q[7])
    D_Q = q_word_add([v1_Q, q_scale(v2_Q, -3)])
    print(f"v1_Q={len(v1_Q)} terms, v2_Q={len(v2_Q)} terms, D_Q={len(D_Q)} terms", flush=True)

    # ---- step 5: per-depth report ----
    depth_report = {}
    for d in range(2, 13):
        proj = q_project_depth(D_Q, d)
        c = content_of(proj) if proj else None
        v691 = valuation(c, 691) if (c is not None and c != 0) else None
        depth_report[d] = {
            "num_terms": len(proj),
            "content_numerator": c.numerator if c is not None else None,
            "content_denominator": c.denominator if c is not None else None,
            "content_numerator_factorization": {str(k): v for k, v in factorize_small(c.numerator).items()} if c else {},
            "content_denominator_factorization": {str(k): v for k, v in factorize_small(c.denominator).items()} if c else {},
            "v_691_of_content": v691,
        }
        print(f"depth {d}: terms={len(proj)} content={c} v691={v691}", flush=True)

    # ---- step 6: content(D^(4)) vs 691/144 ----
    c4 = depth_report[4]
    expected_num_fact = factorize_small(691)
    expected_den_fact = factorize_small(144)
    content_d4_matches_691_over_144 = (
        c4["content_numerator_factorization"] == {str(k): v for k, v in expected_num_fact.items()} and
        c4["content_denominator_factorization"] == {str(k): v for k, v in expected_den_fact.items()}
    )
    print(f"content(D^(4)) matches 691/144 (up to sign): {content_d4_matches_691_over_144}", flush=True)

    # ---- step 7: v_691(D^(6)) already in depth_report[6] ----

    # ---- 裁定718 追加要請 3項: 明示的な top-level フィールド(depth_report
    # に既に入っている値の抜粋・冗長だが検分の便のため専用フィールド化) ----
    v691_d4 = depth_report[4]["v_691_of_content"]
    v691_d6 = depth_report[6]["v_691_of_content"]
    v691_d4_equals_1 = (v691_d4 == 1)
    content_factorization_by_depth_4_to_8 = {
        str(d): {
            "content_numerator_factorization": depth_report[d]["content_numerator_factorization"],
            "content_denominator_factorization": depth_report[d]["content_denominator_factorization"],
            "primes_other_than_691_in_numerator": sorted(
                k for k in depth_report[d]["content_numerator_factorization"] if k != "691"),
            "primes_other_than_691_in_denominator": sorted(
                k for k in depth_report[d]["content_denominator_factorization"] if k != "691"),
        }
        for d in range(4, 9)
    }
    print(f"[裁定718-1] v_691(D^(6)) = {v691_d6}", flush=True)
    print(f"[裁定718-2] v_691(D^(4)) = {v691_d4} (==1: {v691_d4_equals_1})", flush=True)
    print(f"[裁定718-3] content factorizations d=4..8 recorded (see content_factorization_by_depth_4_to_8)", flush=True)

    # ---- step 8: canary vs existing aside2 certs (read-only) ----
    canary = {}
    for p in CANARY_PRIMES:
        try:
            cert = json.load(open(CANARY_CERT_PATHS[p], encoding="utf-8"))
        except FileNotFoundError:
            canary[p] = {"error": "cert file not found"}
            continue
        # reduce v1_Q, v2_Q, D_Q mod p (skip terms whose denominator is
        # divisible by p -- flagged explicitly, not silently dropped)
        singular_terms = {"v1": [], "v2": [], "D": []}

        def reduce_mod(vec_Q, p, label):
            out = {}
            for w, c in vec_Q.items():
                if c.denominator % p == 0:
                    singular_terms[label].append(list(w))
                    continue
                val = (c.numerator % p) * pow(c.denominator % p, -1, p) % p
                if val:
                    out[w] = val
            return out

        v1_modp = reduce_mod(v1_Q, p, "v1")
        v2_modp = reduce_mod(v2_Q, p, "v2")
        D_modp = reduce_mod(D_Q, p, "D")

        cert_v1_terms = cert.get("stage_B_prime_ihara_weight_graded", {}).get("v1_num_terms")
        cert_v2_terms = cert.get("stage_B_prime_ihara_weight_graded", {}).get("v2_num_terms")
        cert_depth_profile = cert.get("stage_E_D_ihara_takao_difference", {}).get("D_depth_profile", {})
        cert_D_is_zero = cert.get("stage_E_D_ihara_takao_difference", {}).get("D_is_zero")

        recon_D_depth_profile = {}
        for d in range(2, 13):
            recon_D_depth_profile[d] = sum(1 for w in D_modp if q_depth(w) == d)

        canary[p] = {
            "v1_num_terms_exact_reduction": len(v1_modp), "v1_num_terms_cert": cert_v1_terms,
            "v1_terms_match": (len(v1_modp) == cert_v1_terms) if cert_v1_terms is not None else None,
            "v2_num_terms_exact_reduction": len(v2_modp), "v2_num_terms_cert": cert_v2_terms,
            "v2_terms_match": (len(v2_modp) == cert_v2_terms) if cert_v2_terms is not None else None,
            "D_is_zero_exact_reduction": (len(D_modp) == 0),
            "D_is_zero_cert": cert_D_is_zero,
            "D_is_zero_match": ((len(D_modp) == 0) == cert_D_is_zero) if cert_D_is_zero is not None else None,
            "D_depth_profile_exact_reduction": recon_D_depth_profile,
            "D_depth_profile_cert": cert_depth_profile,
            "D_depth_profile_match": (
                {str(k): v for k, v in recon_D_depth_profile.items()} ==
                {str(k): v for k, v in cert_depth_profile.items()}
            ) if cert_depth_profile else None,
            "singular_term_counts": {k: len(v) for k, v in singular_terms.items()},
        }
        print(f"canary p={p}: v1_match={canary[p]['v1_terms_match']} v2_match={canary[p]['v2_terms_match']} "
              f"D_is_zero_match={canary[p]['D_is_zero_match']} profile_match={canary[p]['D_depth_profile_match']} "
              f"singular={canary[p]['singular_term_counts']}", flush=True)

    # ---- step 9: theta mirror at exact rational level ----
    theta_mirror = {}
    for d in range(2, 11):  # check d vs 12-d for d=2..10 (11,12 covered by symmetry)
        dd = 12 - d
        Dd = q_project_depth(D_Q, d)
        Ddd = q_project_depth(D_Q, dd)
        lhs = Ddd
        rhs = q_scale(q_theta(Dd), -1)
        diff = q_word_add([lhs, q_scale(rhs, -1)])
        theta_mirror[d] = {"pair": [d, dd], "exact_match": (len(diff) == 0)}
        print(f"theta mirror depth {d}<->{dd}: exact_match={theta_mirror[d]['exact_match']}", flush=True)

    out = {
        "schema": "shadow-atelier/aside3_exact_D/v1",
        "authority": "裁定717 (司令塔), RDV-1 per docs/notes/ideas_ribet_dig_v2.md 札RDV-1 "
                      "(commit b1a3c6e, verbatim)",
        "reconstruction_primes": RECON_PRIMES,
        "reconstruction_modulus_bits": sum(p.bit_length() for p in RECON_PRIMES),
        "sigma_dims": {str(m): {"H_dim": dims[m][0], "S_dim": dims[m][1]} for m in a1.SIGMA_DEGREES},
        "lead_words": {str(m): list(lead_words[m]) for m in a1.SIGMA_DEGREES},
        "v1_Q_num_terms": len(v1_Q), "v2_Q_num_terms": len(v2_Q), "D_Q_num_terms": len(D_Q),
        "depth_report": {str(d): v for d, v in depth_report.items()},
        "content_D4_matches_691_over_144_up_to_sign": content_d4_matches_691_over_144,
        "v_691_D4": v691_d4,
        "v_691_D4_equals_1": v691_d4_equals_1,
        "v_691_D6": v691_d6,
        "content_factorization_by_depth_4_to_8": content_factorization_by_depth_4_to_8,
        "canary_vs_existing_aside2_certs": {str(p): v for p, v in canary.items()},
        "theta_mirror_exact": {str(d): v for d, v in theta_mirror.items()},
        "no_verdict_note": "S-AS-5 compliance: this script emits ONLY raw numeric values, "
                            "factorizations, valuations, and the pre-registered STOP codes "
                            "(SIGMA_NONUNIQUE / LEAD_WORD_MISMATCH / RECONSTRUCTION_FAIL) -- no "
                            "interpretive verdict prose of the kinds forbidden in the addendum "
                            "S6/S7 is written anywhere in this cert.",
        "stop_code": None,
        "total_elapsed_sec": round(time.time() - t_start, 2),
    }
    write_out(out)
    print(f"=== ASIDE-3: JOB END total_elapsed_sec={out['total_elapsed_sec']} stop_code=None ===", flush=True)
    print("ASIDE3_DONE", flush=True)


def write_out(out):
    path = "search/certs/aside3_exact_D_v1_20260806.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path}", flush=True)


def write_stop(stop_code, detail):
    out = {
        "schema": "shadow-atelier/aside3_exact_D/v1",
        "authority": "裁定717 (司令塔), RDV-1 per docs/notes/ideas_ribet_dig_v2.md 札RDV-1 (commit b1a3c6e, verbatim)",
        "stop_code": stop_code,
        "stop_detail": detail,
    }
    write_out(out)
    print("ASIDE3_STOP", flush=True)
    sys.exit(1)


if __name__ == "__main__":
    main()
