#!/usr/bin/env python3
"""
search/wfs1_f0.py -- WFS-1 stage F0 (裁定727(5)), per
docs/notes/weight_family_spectroscopy_design_v1.md (commit 4e6bdcb,
sha256 da3f34c9ffd98c81ce68e691521f21c75c23921b7337e62a87e3b20b53850c50)
SS2.2/SS2.3/SS5.1, verbatim (modulo one corrected typo, documented below).

Constructs L = span_Q{ {s3,{s3,{s3,s7}}}, {s3,Delta2_13}, {s5,{s3,{s3,s5}}} }
using ONLY sigma_3, sigma_5, sigma_7 (no sigma_11/sigma_13 built -- matches
the design's own claim SS2.3 "sigma_11,sigma_13 不要"), and measures dim(L)
(predicted <=2, 命題F-1(a)) and L's depth profile (canary/P-F-0: is
L^(4)=0?).

*** DESIGN TYPO FOUND AND CORRECTED (documented, not silently guessed) ***
The design doc SS2.1 literally defines Delta^(2)_13 := {sigma_3,{sigma_5,
sigma_5}}. This is IDENTICALLY ZERO: for ANY antisymmetric bracket
(Ihara bracket included -- {f,f} = D_f(f)-D_f(f)+[f,f] = 0+0 = 0 by direct
substitution into Definition C-1), {sigma_5,sigma_5}=0, so the literal
formula collapses to {sigma_3,0}=0 regardless of interpretation. This
directly contradicts the design's own claim (SS2.1 table) that
dim(sigma_13's lift space)=2 with basis {Delta^(1)_13, Delta^(2)_13} -- a
genuinely 2-dimensional space needs BOTH generators nonzero.
  The correct generator of the multidegree-(1,2) piece (1 copy of the
"weight-3-type" letter, 2 copies of the "weight-5-type" letter; dimension
of this free-Lie multidegree piece is 1, per the design's OWN Witt-type
formula in SS2.1) is Delta^(2)_13 := {sigma_5,{sigma_3,sigma_5}} -- bracket
the DUPLICATED letter (sigma_5) with the cross pair {sigma_3,sigma_5} --
exactly mirroring the design's own (non-degenerate) Delta_11 :=
{sigma_3,{sigma_3,sigma_5}} (there the duplicated letter is sigma_3, also
bracketed with the cross pair {sigma_3,sigma_5}). This is the structural
pattern used THROUGHOUT the design (matching Brown's own p.3 quoted
ambiguity generator for sigma_11) -- not a new mathematical claim, just the
correct instance of the same pattern applied to the (1,2) case instead of
the (2,1) case.
  Consequently L's 2nd generator is corrected from the design's literal
"{sigma_3,{sigma_3,{sigma_5,sigma_5}}}" (identically zero) to
"{sigma_3,{sigma_5,{sigma_3,sigma_5}}}" (= {sigma_3, Delta^(2)_13-corrected}).
This correction is used below. Flagged prominently in the report; NOT a
silent substitution.

Method: mod-p computation at 2 large primes (2147483647, 998244353) for a
generic-prime cross-check of dim(L) and the depth profile (dim/support
questions do not need exact rationals -- unlike aside3's content/valuation
work, which DOES need exact Q). This matches this task's "秒" cost target
(cf. aside2's established methodology, which computes A12 etc. directly
mod large primes without CRT).

No verdict language (S-WFS-5): raw values only.
"""
import json
import sys
import time

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
import aside1_run_single_prime as a1
import aside2_run_single_prime as a2

WEIGHT16_PRIMES = [2147483647, 998244353]


def run_prime(p):
    h_alg = ed.GradedLie(2, a1.KMAX, p, sparse_degrees=set(range(1, a1.KMAX + 1)))
    sigmas = {}
    for m in (3, 5, 7):
        H_dim, S_dim, ambient, lead_word = a1.sigma_m_ambient(m, h_alg, p)
        if S_dim != 1:
            raise ValueError(f"p={p} m={m}: S_dim={S_dim} != 1 -- SIGMA_NONUNIQUE")
        sigmas[m] = ambient

    ib = a2.ihara_bracket
    s3, s5, s7 = sigmas[3], sigmas[5], sigmas[7]

    delta1_13 = ib(s3, ib(s3, s7, p), p)                 # {s3,{s3,s7}}  (2,1)-type in (s3,s7)
    delta2_13_corrected = ib(s5, ib(s3, s5, p), p)       # {s5,{s3,s5}}  (1,2)-type in (s3,s5) -- CORRECTED
    delta11 = ib(s3, ib(s3, s5, p), p)                   # {s3,{s3,s5}}  (2,1)-type in (s3,s5)

    L_gen1 = ib(s3, delta1_13, p)                      # {s3,{s3,{s3,s7}}}   -- weight 16
    L_gen2 = ib(s3, delta2_13_corrected, p)             # {s3,{s5,{s3,s5}}}   -- weight 16 (corrected)
    L_gen3 = ib(s5, delta11, p)                         # {s5,{s3,{s3,s5}}}   -- weight 16

    L_gens = [L_gen1, L_gen2, L_gen3]

    # rank of 3 ambient vectors (extend the existing 2-vector helper's logic)
    def rank_of_n_ambient_vectors(vecs, p):
        keys = sorted(set().union(*[set(v.keys()) for v in vecs])) if any(vecs) else []
        if not keys:
            return 0
        import numpy as np
        M = np.zeros((len(keys), len(vecs)), dtype=np.int64)
        key_index = {k: i for i, k in enumerate(keys)}
        for col, v in enumerate(vecs):
            for k, c in v.items():
                M[key_index[k], col] = c % p
        return int(ed.rank_modp_np(M, p))

    dim_L = rank_of_n_ambient_vectors(L_gens, p)

    depth_profile = {}
    L_depth_profile = {}
    for d in range(0, 17):
        proj_gens = [a1.project_depth(v, d) for v in L_gens]
        L_depth_profile[d] = {
            "num_terms_per_gen": [len(pg) for pg in proj_gens],
            "rank_at_this_depth": rank_of_n_ambient_vectors(proj_gens, p),
        }

    return {
        "prime": p,
        "sigma_dims": {str(m): {"H_dim": a1.sigma_m_ambient(m, h_alg, p)[0]} for m in (3, 5, 7)},
        "L_gen_num_terms": [len(g) for g in L_gens],
        "dim_L": dim_L,
        "dim_L_le_2": dim_L <= 2,
        "L_depth_profile": L_depth_profile,
        "L4_is_zero": L_depth_profile[4]["rank_at_this_depth"] == 0,
    }


def main():
    t0 = time.time()
    print("=== WFS-1 stage F0 (裁定727(5)) ===", flush=True)
    results = {}
    for p in WEIGHT16_PRIMES:
        t1 = time.time()
        results[p] = run_prime(p)
        print(f"p={p}: dim_L={results[p]['dim_L']} L4_is_zero={results[p]['L4_is_zero']} "
              f"L_gen_num_terms={results[p]['L_gen_num_terms']} elapsed={time.time()-t1:.2f}s", flush=True)

    # cross-prime agreement
    dims = {p: r["dim_L"] for p, r in results.items()}
    agree = len(set(dims.values())) == 1

    out = {
        "schema": "shadow-atelier/wfs1_f0/v1",
        "authority": "裁定727(5) (司令塔), WFS-1 段F0 per "
                      "docs/notes/weight_family_spectroscopy_design_v1.md SS2.2/2.3/5.1 "
                      "(commit 4e6bdcb, verbatim except one corrected typo -- see module docstring)",
        "typo_correction_note": "design doc SS2.1's literal Delta^(2)_13={sigma_3,{sigma_5,sigma_5}} "
                                 "is identically zero (antisymmetry, {f,f}=0) -- corrected to "
                                 "{sigma_5,{sigma_3,sigma_5}} (matching the multidegree-(1,2) "
                                 "generator, mirroring Delta_11's own structure). See module docstring "
                                 "for full derivation. Flagged prominently in the report.",
        "primes": WEIGHT16_PRIMES,
        "results": {str(p): r for p, r in results.items()},
        "dim_L_agrees_across_primes": agree,
        "P_F_0_L4_is_zero_all_primes": all(r["L4_is_zero"] for r in results.values()),
        "no_verdict_note": "S-WFS-5 compliance: raw values only, no interpretive verdict prose.",
        "total_elapsed_sec": round(time.time() - t0, 2),
    }
    out_path = "search/certs/wfs1_f0_v1_20260807.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}", flush=True)
    print("WFS1_F0_DONE", flush=True)


if __name__ == "__main__":
    main()
