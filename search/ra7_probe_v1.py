#!/usr/bin/env python3
"""
search/ra7_probe_v1.py -- RA7-PROBE-1 (裁定752③, per
docs/notes/tor_sweep_design_v1_addendum_b.md §3.3 発注仕様RA7-PROBE-1,
implemented verbatim). Task order: implementer 単任務2連, task 1/2.

Measures the single vanishing bit {e_12, sigma3_bar} =? 0 (Brown's
"presently rule out できない" minimal case, weight 15 depth 5 -- see
命題B-1, addendum §3.1), using D^(4) (weight 12, depth 4, 350 terms) of
docs/notes/ideas_ribet_dig_v2.md 札RDV-1's exact-rational D (committed as
search/certs/aside3_exact_D_v1_20260806.json) as the proxy for e_12.

*** ABSOLUTE CONSTRAINT (裁定752③ trap, addendum §3.2) ***
D^(4) = (691/144) * (primitive integer vector). The proxy identically
VANISHES mod 691 (already observed/committed in aside3's own cert:
v_691_D4 == 1). Firing this probe at p=691 would certainly misread "proxy
coefficient vanished" as "e_12 information vanished". p=2,3 are likewise
forbidden (144 = 2^4*3^2 divides the content denominator -- singular mod
reduction). Prime panel is HARD-CODED to the addendum's fixed set:
  {677, 701, 998244353, 2147483647}
and this script will refuse (STOP) if that set is ever edited to include
691, 2, or 3.

Method:
  R-a: reconstruct D_Q exactly (same CRT+rational-reconstruction pipeline
       as search/aside3_exact_D_v1.py, reusing its module-level functions
       UNCHANGED -- reconstruct_ambient_dict, q_ihara_bracket, etc. --
       "既存Ihara括弧実装を再利用" per the order), project to depth 4, and
       verify the result's shape (350 terms, content factorization
       691^1 / (2^4*3^2)) against the ALREADY-COMMITTED aside3 cert's own
       summary fields -- a data-integrity canary, not a re-derivation of
       aside3's result (that cert is read-only input here).
  R-b: construct sigma3_bar = -(ad X)^2 (Y) exactly (weight 3, depth 1,
       3 terms), per addendum §1.1's general formula
       sigma_bar_a = (-1)^((a-1)/2) (ad X)^(a-1)(Y), a=3.
  R-c: exact Ihara bracket {D^(4), sigma3_bar} (ambient weight 15 = 2^15
       word space, matching the existing stage-E scale). Canary: only the
       depth-5 component should be nonzero (depth additive: 4+1).
  R-d: reduce the exact bracket mod each panel prime; report is_zero[p]
       as a raw bool (P-RA7-1: at least one prime nonzero is the
       "expected win" case per addendum, but no verdict language is
       written here -- raw per-prime bools only).
  R-e: prime panel as fixed above; 【B-PIN-1】 verbatim pin recorded in
       cert prereg (from docs/scout/brown_prop64_lattice_verbatim_v1.md
       §3, quoting the p.6 text on the unruled-out {e_f,sigma_2n+1} in
       Lie_5 ls_1).

No verdict language (S-AS-5-style discipline, continued from aside1-3):
only raw values, factorizations, booleans, and pre-registered STOP codes.
Pure Python (fractions + the existing numpy-int64 mod-p pipeline for the
reconstruction inputs only, exactly as aside3 uses it) -- no GAP.
"""
import json
import sys
import time
from fractions import Fraction
from math import gcd

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
import aside1_run_single_prime as a1
import aside3_exact_D_v1 as a3

# ---- hard-coded prime panel (裁定752③ / addendum §3.2 -- DO NOT EDIT
# without a new design ruling: 691, 2, 3 are permanently excluded here) ----
PRIME_PANEL = [677, 701, 998244353, 2147483647]
FORBIDDEN_PRIMES = {691, 2, 3}

ASIDE3_CERT_PATH = "search/certs/aside3_exact_D_v1_20260806.json"
BROWN_PIN_SOURCE = "docs/scout/brown_prop64_lattice_verbatim_v1.md"
B_PIN_1_QUOTE = (
    "nor can we presently rule out the existence of relations of the form "
    "{e_f, σ_{2n+1}} ∈ Lie₅ ls₁ which can only occur in "
    "depth ≥ 5 and weight ≥ 15. Relations which are quadratic in "
    "the e_f could first occur in weight 28 and depth 8."
)
B_PIN_1_SUBJECT = (
    "the existence of relations of the form {e_f, sigma_{2n+1}} in Lie_5(ls_1) "
    "which can only occur in depth >= 5 and weight >= 15 "
    "(this is the object Brown states cannot presently be ruled out; "
    "命題B-1 shows weight 15 forces Lie_5(ls_1)=0, so the minimal such "
    "relation {e_12, sigma_3} degenerates to a single vanishing bit)"
)


def write_out(out, path="search/certs/ra7_probe_v1_20260807.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Wrote {path}", flush=True)


def write_stop(stop_code, detail):
    out = {
        "schema": "shadow-atelier/ra7_probe_v1",
        "authority": "裁定752③ (司令塔), docs/notes/tor_sweep_design_v1_addendum_b.md "
                      "§3.3 発注仕様RA7-PROBE-1 (verbatim)",
        "stop_code": stop_code,
        "stop_detail": detail,
    }
    write_out(out)
    print("RA7_PROBE_STOP", flush=True)
    sys.exit(1)


def reduce_mod_Q(vec_Q, p):
    """Reduce an exact-Fraction word-vector mod p. Returns (reduced dict of
    int coeffs, list of words whose denominator is divisible by p -- flagged
    explicitly, never silently dropped, mirroring aside3's canary reduction)."""
    out = {}
    singular = []
    for w, c in vec_Q.items():
        if c.denominator % p == 0:
            singular.append(list(w))
            continue
        val = (c.numerator % p) * pow(c.denominator % p, -1, p) % p
        if val:
            out[w] = val
    return out, singular


def main():
    t_start = time.time()
    print("=== RA7-PROBE-1: JOB START ===", flush=True)

    # ---- hard guard: panel must never include the forbidden primes ----
    panel_set = set(PRIME_PANEL)
    violation = panel_set & FORBIDDEN_PRIMES
    if violation:
        write_stop("FORBIDDEN_PRIME_IN_PANEL", {"violating_primes": sorted(violation)})
        return
    if len(panel_set) != len(PRIME_PANEL):
        write_stop("PANEL_DUPLICATE_PRIME", {"panel": PRIME_PANEL})
        return

    # ---- R-a: reconstruct D_Q exactly (same pipeline as aside3, module
    # functions reused unmodified) ----
    per_prime_sigma = {m: {} for m in a1.SIGMA_DEGREES}
    lead_words = {m: None for m in a1.SIGMA_DEGREES}
    lead_word_mismatch = {}
    for p in a3.RECON_PRIMES:
        t0 = time.time()
        h_alg = ed.GradedLie(2, a1.KMAX, p, sparse_degrees=set(range(1, a1.KMAX + 1)))
        for m in a1.SIGMA_DEGREES:
            H_dim, S_dim, ambient, lead_word = a1.sigma_m_ambient(m, h_alg, p)
            if S_dim != 1:
                write_stop("SIGMA_NONUNIQUE", {"prime": p, "m": m, "S_dim": S_dim})
                return
            per_prime_sigma[m][p] = ambient
            if lead_words[m] is None:
                lead_words[m] = lead_word
            elif tuple(lead_word) != tuple(lead_words[m]):
                lead_word_mismatch[m] = lead_word_mismatch.get(m, []) + [(p, lead_word)]
        print(f"prime={p}: sigma_m realized for m={a1.SIGMA_DEGREES}, elapsed={time.time()-t0:.1f}s", flush=True)

    if lead_word_mismatch:
        write_stop("LEAD_WORD_MISMATCH", {"detail": {str(k): v for k, v in lead_word_mismatch.items()}})
        return

    sigma_Q = {}
    for m in a1.SIGMA_DEGREES:
        try:
            sigma_Q[m] = a3.reconstruct_ambient_dict(per_prime_sigma[m])
        except ValueError as exc:
            write_stop("RECONSTRUCTION_FAIL", {"m": m, "error": str(exc)})
            return
        print(f"sigma_{m}^Q reconstructed: {len(sigma_Q[m])} terms", flush=True)

    v1_Q = a3.q_ihara_bracket(sigma_Q[3], sigma_Q[9])
    v2_Q = a3.q_ihara_bracket(sigma_Q[5], sigma_Q[7])
    D_Q = a3.q_word_add([v1_Q, a3.q_scale(v2_Q, -3)])
    D4_Q = a3.q_project_depth(D_Q, 4)
    print(f"D_Q={len(D_Q)} terms total, D4_Q (depth 4)={len(D4_Q)} terms", flush=True)

    # ---- integrity check vs the already-committed aside3 cert's own
    # summary fields (data-integrity canary, not a re-derivation) ----
    try:
        aside3_cert = json.load(open(ASIDE3_CERT_PATH, encoding="utf-8"))
    except FileNotFoundError:
        write_stop("ASIDE3_CERT_NOT_FOUND", {"path": ASIDE3_CERT_PATH})
        return
    committed_d4 = aside3_cert.get("depth_report", {}).get("4", {})
    d4_content = a3.content_of(D4_Q)
    d4_content_num_fact = {str(k): v for k, v in a3.factorize_small(d4_content.numerator).items()}
    d4_content_den_fact = {str(k): v for k, v in a3.factorize_small(d4_content.denominator).items()}
    d4_integrity = {
        "num_terms_match": (len(D4_Q) == committed_d4.get("num_terms")),
        "content_numerator_factorization_match": (d4_content_num_fact == committed_d4.get("content_numerator_factorization")),
        "content_denominator_factorization_match": (d4_content_den_fact == committed_d4.get("content_denominator_factorization")),
        "recomputed_num_terms": len(D4_Q),
        "committed_num_terms": committed_d4.get("num_terms"),
        "recomputed_content_numerator_factorization": d4_content_num_fact,
        "committed_content_numerator_factorization": committed_d4.get("content_numerator_factorization"),
        "recomputed_content_denominator_factorization": d4_content_den_fact,
        "committed_content_denominator_factorization": committed_d4.get("content_denominator_factorization"),
    }
    d4_integrity_all_match = all([
        d4_integrity["num_terms_match"],
        d4_integrity["content_numerator_factorization_match"],
        d4_integrity["content_denominator_factorization_match"],
    ])
    print(f"D4 integrity vs committed aside3 cert: all_match={d4_integrity_all_match} detail={d4_integrity}", flush=True)
    if not d4_integrity_all_match:
        write_stop("D4_INTEGRITY_MISMATCH", d4_integrity)
        return

    # ---- R-b: sigma3_bar = -(ad X)^2 (Y), exact ----
    y_vec = {(1,): Fraction(1)}
    ad1 = a3.q_word_bracket({(0,): Fraction(1)}, y_vec)          # [X,Y]
    ad2 = a3.q_word_bracket({(0,): Fraction(1)}, ad1)            # [X,[X,Y]]
    sigma3_bar_Q = a3.q_scale(ad2, Fraction(-1))                 # -(ad X)^2(Y)
    sigma3_bar_shape_ok = (
        len(sigma3_bar_Q) == 3 and
        all(len(w) == 3 for w in sigma3_bar_Q) and
        all(a3.q_depth(w) == 1 for w in sigma3_bar_Q)
    )
    print(f"sigma3_bar_Q = {sigma3_bar_Q} shape_ok(3 terms,weight3,depth1)={sigma3_bar_shape_ok}", flush=True)
    if not sigma3_bar_shape_ok:
        write_stop("SIGMA3BAR_SHAPE_FAIL", {"sigma3_bar_Q": {str(k): str(v) for k, v in sigma3_bar_Q.items()}})
        return

    # ---- R-c: exact Ihara bracket {D^(4), sigma3_bar}, ambient weight 15 ----
    B_Q = a3.q_ihara_bracket(D4_Q, sigma3_bar_Q)
    depth_profile_Q = {}
    for w in B_Q:
        d = a3.q_depth(w)
        depth_profile_Q[d] = depth_profile_Q.get(d, 0) + 1
    weights_seen = sorted(set(len(w) for w in B_Q))
    only_depth5_nonzero = (set(depth_profile_Q.keys()) <= {5})
    print(f"B_Q = {len(B_Q)} terms, depth_profile={depth_profile_Q}, weights_seen={weights_seen}, "
          f"only_depth5_nonzero={only_depth5_nonzero}", flush=True)

    # ---- R-d/R-e: reduce mod each panel prime ----
    per_prime = {}
    for p in PRIME_PANEL:
        reduced, singular = reduce_mod_Q(B_Q, p)
        dp = {}
        for w in reduced:
            d = a3.q_depth(w)
            dp[d] = dp.get(d, 0) + 1
        per_prime[p] = {
            "nonzero_term_count": len(reduced),
            "is_zero": (len(reduced) == 0),
            "singular_term_count": len(singular),
            "singular_terms": singular,
            "depth_profile": {str(k): v for k, v in dp.items()},
        }
        print(f"prime={p}: nonzero_term_count={per_prime[p]['nonzero_term_count']} "
              f"is_zero={per_prime[p]['is_zero']} singular_term_count={per_prime[p]['singular_term_count']}", flush=True)

    is_zero_summary = {str(p): per_prime[p]["is_zero"] for p in PRIME_PANEL}
    at_least_one_prime_nonzero = any(not per_prime[p]["is_zero"] for p in PRIME_PANEL)
    all_primes_zero = all(per_prime[p]["is_zero"] for p in PRIME_PANEL)

    # ---- B-PIN-1 verbatim source check (file must actually contain the
    # quoted string -- fail-closed if the pin drifted from the source) ----
    try:
        pin_source_text = open(BROWN_PIN_SOURCE, encoding="utf-8").read()
    except FileNotFoundError:
        write_stop("B_PIN_1_SOURCE_NOT_FOUND", {"path": BROWN_PIN_SOURCE})
        return
    b_pin_1_verbatim_confirmed = (B_PIN_1_QUOTE in pin_source_text)
    print(f"B-PIN-1 verbatim quote found in {BROWN_PIN_SOURCE}: {b_pin_1_verbatim_confirmed}", flush=True)
    if not b_pin_1_verbatim_confirmed:
        write_stop("B_PIN_1_VERBATIM_MISMATCH", {"quote": B_PIN_1_QUOTE, "source": BROWN_PIN_SOURCE})
        return

    out = {
        "schema": "shadow-atelier/ra7_probe_v1",
        "authority": "裁定752③ (司令塔), docs/notes/tor_sweep_design_v1_addendum_b.md "
                      "§3.3 発注仕様RA7-PROBE-1 (verbatim)",
        "prereg": {
            "prime_panel": PRIME_PANEL,
            "prime_panel_exclusions": {
                "691": "D^(4) content = 691/144 (committed in aside3 cert, "
                       "v_691_D4=1) -- D^(4) IDENTICALLY VANISHES mod 691 as a "
                       "proxy artifact (the '691 echo', already measured "
                       "elsewhere); firing at p=691 would certainly misread "
                       "'proxy coefficient vanished' as 'e_12 information "
                       "vanished'. Addendum §3.2 boxed statement: "
                       "'p=691 でこのプローブを撃ってはならない'.",
                "2": "144 = 2^4 * 3^2 divides the content denominator of D^(4) "
                     "-- mod-2 reduction of the proxy is singular (addendum "
                     "§3.2: 'p|144(=2^4 3^2)(p=2,3)も禁止').",
                "3": "144 = 2^4 * 3^2 divides the content denominator of D^(4) "
                     "-- mod-3 reduction of the proxy is singular (same clause "
                     "as p=2).",
            },
            "b_pin_1": {
                "source": BROWN_PIN_SOURCE + " §3",
                "verbatim_quote": B_PIN_1_QUOTE,
                "subject_of_unruled_out_proposition": B_PIN_1_SUBJECT,
                "verbatim_confirmed_in_source_file": b_pin_1_verbatim_confirmed,
            },
        },
        "source_cert": ASIDE3_CERT_PATH,
        "reconstruction_primes": a3.RECON_PRIMES,
        "D4_integrity_vs_committed_aside3_cert": d4_integrity,
        "D4_integrity_all_match": d4_integrity_all_match,
        "D4_Q_num_terms": len(D4_Q),
        "D4_Q_terms": [[list(w), c.numerator, c.denominator] for w, c in sorted(D4_Q.items())],
        "sigma3_bar_construction": {
            "formula": "sigma3_bar = -(ad X)^2 (Y), per addendum §1.1 general "
                       "formula sigma_bar_a = (-1)^((a-1)/2) (ad X)^(a-1)(Y), a=3",
            "shape_ok_3terms_weight3_depth1": sigma3_bar_shape_ok,
        },
        "sigma3_bar_Q_terms": [[list(w), c.numerator, c.denominator] for w, c in sorted(sigma3_bar_Q.items())],
        "ambient_weight": 15,
        "B_Q_num_terms": len(B_Q),
        "B_Q_depth_profile": {str(k): v for k, v in sorted(depth_profile_Q.items())},
        "B_Q_only_depth5_nonzero": only_depth5_nonzero,
        "per_prime": {str(p): v for p, v in per_prime.items()},
        "is_zero_summary": is_zero_summary,
        "at_least_one_prime_nonzero": at_least_one_prime_nonzero,
        "all_primes_zero": all_primes_zero,
        "no_verdict_note": "S-AS-5-style compliance: this script emits ONLY raw "
                            "numeric values, term vectors, factorizations, "
                            "booleans, and the pre-registered STOP codes "
                            "(SIGMA_NONUNIQUE / LEAD_WORD_MISMATCH / "
                            "RECONSTRUCTION_FAIL / D4_INTEGRITY_MISMATCH / "
                            "SIGMA3BAR_SHAPE_FAIL / B_PIN_1_VERBATIM_MISMATCH / "
                            "FORBIDDEN_PRIME_IN_PANEL / PANEL_DUPLICATE_PRIME / "
                            "ASIDE3_CERT_NOT_FOUND / B_PIN_1_SOURCE_NOT_FOUND) -- "
                            "no interpretive verdict prose. The判定 of "
                            "P-RA7-1 (at_least_one_prime_nonzero as 'the win') "
                            "is reserved for 司令塔/Sol per addendum §3.3.",
        "stop_code": None,
        "total_elapsed_sec": round(time.time() - t_start, 2),
    }
    write_out(out)
    print(f"=== RA7-PROBE-1: JOB END total_elapsed_sec={out['total_elapsed_sec']} stop_code=None ===", flush=True)
    print("RA7_PROBE_DONE", flush=True)


if __name__ == "__main__":
    main()
