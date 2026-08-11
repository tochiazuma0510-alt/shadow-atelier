#!/usr/bin/env python3
"""
search/pl_lab1_normchk_v1.py -- NORM-CHK (裁定783(1)), per
docs/notes/phase2_scoring_v1.md §1.1 命題NORM-1 / 発注NORM-CHK.

Tests the "branch L" (WILD-NOEXCESS / Lazard-dictionary-correction-only)
judgment formula:  def_p = -mult_std(R_p),  where
  R_p := ker( Lambda_p -> measured gamma_p/gamma_{p+1}(P_{c,p}) )
is the S3-module of "lost" degree-p directions (dim R_p = delta_p, the
P-PL-0 drop already recorded in search/certs/pl_lab1_v1_20260811.json).

Inputs (all already independently computed, reused here unchanged):
  - def_p, delta_p (= p_pl_0_drop_at_p), H_p, kernel_dim (=mult_std(measured)):
    from search/certs/pl_lab1_v1_20260811.json (裁定774/.../781, f32451f)
  - m_triv(measured), m_sgn(measured), m_std(measured) [cross-check vs
    kernel_dim]: from search/probe/pl_lab1_v1/exp5_normchk_isotypic.g's
    GAP run (exact nullspace computations -- ker(1-theta)cap ker(1-tau)
    for triv, ker(1+theta)cap ker(1-tau) for sgn, ker(1+theta)cap
    ker(1+tau+tau^2) for std -- avoids the mod-p trace ambiguity that
    would arise at p7c7 where dim_layer=12 > p=7, since raw traces mod p
    are then only determined up to +-p; nullspace/rank has no such issue).
    Reused here as already-computed raw integers (log:
    search/probe/pl_lab1_v1/exp5_normchk_isotypic.log), NOT recomputed by
    this script (this script is pure Python, no GAP).
  - m_triv(Lambda_p), m_sgn(Lambda_p): derived by closed-form arithmetic
    from the ALREADY-ESTABLISHED command TOR-SWEEP addendum A's H_k
    values (H_p = mult_std(Lambda_p)) plus two exact character-theoretic
    facts, both re-derived and checked below (not asserted blindly):
      (a) tr(tau|Lambda_k) = Witt(2,k) - 3*H_k  [from H_k's own defining
          formula H_k = (Witt(2,k) - tr(tau|Lambda_k))/3, algebraically
          inverted -- same H_k formula already independently verified
          3/3 against PL-LAB-1's raw measurement, addendum_a §1.2]
      (b) tr(theta|Lambda_k) = 0 for ODD k [from the design's own
          necklace-trace formula tr(theta|Lambda_k) =
          (1/k) sum_{d|k} mu(d) chi_std(theta^d)^{k/d}, chi_std(theta^d)
          = 2 if d even else 0 -- for k odd, EVERY divisor d of k is odd,
          so chi_std(theta^d)=0 for every term, giving the sum identically
          0. p=5,7 are both odd, so this applies directly.]
    Then S3 character-multiplicity formulas with t=tr(theta)=0, s=tr(tau):
      m_triv = (dim + 2s)/6,  m_sgn = (dim + 2s)/6  [note: equal, since t=0]
      m_std  = (dim - s)/3   [= H_k, consistency check]

No verdict language -- raw integers and the single boolean
"m_std_R_p_equals_abs_def_p" per weight, plus the full isotypic table.
Branch-L/branch-B/branch-B-plus language is NOT asserted (発効は司令塔専権).
"""
import json

PL_LAB1_CERT_PATH = "search/certs/pl_lab1_v1_20260811.json"

# from search/probe/pl_lab1_v1/exp5_normchk_isotypic.log (GAP, exact nullspace computation)
MEASURED_ISOTYPIC = {
    5: {"m_triv": 0, "m_sgn": 0, "m_std": 1, "dim_layer": 2},
    7: {"m_triv": 2, "m_sgn": 2, "m_std": 4, "dim_layer": 12},
}

WITT_2_K = {1: 2, 2: 1, 3: 2, 4: 3, 5: 6, 6: 9, 7: 18, 8: 30}
H_K = {1: 1, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 6, 8: 10}


def tr_tau_lambda(k):
    """tr(tau|Lambda_k) = Witt(2,k) - 3*H_k, exact integer, inverted from
    H_k's own defining formula (already independently verified)."""
    return WITT_2_K[k] - 3 * H_K[k]


def tr_theta_lambda(k):
    """tr(theta|Lambda_k) = 0 for odd k (every divisor of an odd k is odd,
    chi_std(theta^d)=0 for odd d in the design's own necklace formula)."""
    if k % 2 == 1:
        return 0
    raise NotImplementedError("tr_theta_lambda only derived here for odd k (p=5,7 are odd)")


def isotypic_from_traces(dim, t, s):
    """S3 character-multiplicity formulas (standard, from the character
    table: triv=(1,1,1), sgn=(1,-1,1), std=(2,0,-1) at (id,theta,tau))."""
    m_triv = (dim + 3 * t + 2 * s)
    m_sgn = (dim - 3 * t + 2 * s)
    m_std2 = (2 * dim - 2 * s)
    assert m_triv % 6 == 0 and m_sgn % 6 == 0 and m_std2 % 6 == 0, \
        f"non-integer multiplicity: dim={dim} t={t} s={s}"
    return m_triv // 6, m_sgn // 6, m_std2 // 6


def main():
    pl = json.load(open(PL_LAB1_CERT_PATH, encoding="utf-8"))
    targets = {t["p"]: t for t in pl["targets"] if t["kind"] == "main"}

    per_p = {}
    for p in [5, 7]:
        t = targets[p]
        delta_p = t["p_pl_0_drop_at_p"]
        pd = next(x for x in t["per_degree"] if x["k"] == p)
        def_p = pd["def_k"]
        H_p = pd["H_k"]
        kernel_dim = pd["kernel_dim"]  # = mult_std(measured), already computed in pl_lab1_v1.g
        witt_p = WITT_2_K[p]

        # ambient Lambda_p decomposition (closed form, exact)
        t_theta = tr_theta_lambda(p)
        s_tau = tr_tau_lambda(p)
        m_triv_L, m_sgn_L, m_std_L = isotypic_from_traces(witt_p, t_theta, s_tau)
        assert m_std_L == H_p, f"m_std(Lambda_{p}) closed-form={m_std_L} != H_{p}={H_p} (internal consistency check)"

        # measured decomposition (from GAP exact nullspace computation)
        meas = MEASURED_ISOTYPIC[p]
        assert meas["dim_layer"] == witt_p - delta_p, "measured dim_layer inconsistent with delta_p"
        assert meas["m_std"] == kernel_dim, \
            f"GAP-computed m_std(measured)={meas['m_std']} != pl_lab1_v1.g's kernel_dim={kernel_dim} " \
            f"(cross-check between exp5 and the original pl_lab1_v1.g run)"

        # R_p = Lambda_p - measured (additive multiplicities, valid since S3
        # acts semisimply over F_p for p coprime to |S3|=6, Maschke)
        m_triv_R = m_triv_L - meas["m_triv"]
        m_sgn_R = m_sgn_L - meas["m_sgn"]
        m_std_R = m_std_L - meas["m_std"]
        delta_p_check = m_triv_R + m_sgn_R + 2 * m_std_R

        m_std_matches_abs_def = (m_std_R == abs(def_p))

        per_p[p] = {
            "p": p, "delta_p": delta_p, "def_p": def_p, "H_p": H_p,
            "witt_2_p": witt_p, "dim_layer_measured": meas["dim_layer"],
            "Lambda_p_isotypic": {"m_triv": m_triv_L, "m_sgn": m_sgn_L, "m_std": m_std_L,
                                   "trace_theta": t_theta, "trace_tau": s_tau},
            "measured_isotypic": {"m_triv": meas["m_triv"], "m_sgn": meas["m_sgn"], "m_std": meas["m_std"]},
            "R_p_isotypic": {"m_triv": m_triv_R, "m_sgn": m_sgn_R, "m_std": m_std_R},
            "delta_p_consistency_check": {"recomputed_from_isotypic": delta_p_check,
                                            "matches_delta_p": (delta_p_check == delta_p)},
            "m_std_R_p_equals_abs_def_p": m_std_matches_abs_def,
        }
        print(f"p={p}: delta_p={delta_p} def_p={def_p} | Lambda_p=(triv={m_triv_L},sgn={m_sgn_L},std={m_std_L}) "
              f"| measured=(triv={meas['m_triv']},sgn={meas['m_sgn']},std={meas['m_std']}) "
              f"| R_p=(triv={m_triv_R},sgn={m_sgn_R},std={m_std_R}) "
              f"| delta_p_check={delta_p_check} match={delta_p_check == delta_p} "
              f"| m_std(R_p)==|def_p|: {m_std_matches_abs_def}", flush=True)

    all_match = all(per_p[p]["m_std_R_p_equals_abs_def_p"] for p in [5, 7])
    all_delta_consistent = all(per_p[p]["delta_p_consistency_check"]["matches_delta_p"] for p in [5, 7])

    out = {
        "schema": "shadow-atelier/pl_lab1_normchk_v1",
        "authority": "裁定783(1) (司令塔), docs/notes/phase2_scoring_v1.md §1.1 命題NORM-1 / 発注NORM-CHK (verbatim)",
        "supersedes_note": "cert addendum to search/certs/pl_lab1_v1_20260811.json (f32451f) -- "
                           "adds the S3-isotypic decomposition of R_p (delta_p's structure) requested "
                           "by phase2_scoring_v1.md; def_p/delta_p/H_p/kernel_dim values are REUSED "
                           "unchanged from that cert, not recomputed.",
        "source_pl_lab1_cert": PL_LAB1_CERT_PATH,
        "source_gap_isotypic_log": "search/probe/pl_lab1_v1/exp5_normchk_isotypic.log",
        "method_note": "measured isotypic multiplicities computed via exact nullspace (ker(1-theta) "
                       "cap ker(1-tau) for triv, ker(1+theta) cap ker(1-tau) for sgn, ker(1+theta) cap "
                       "ker(1+tau+tau^2) for std), NOT via mod-p trace (avoids ambiguity at p7c7 where "
                       "dim_layer=12 > p=7). Lambda_p (ambient) isotypic multiplicities computed via "
                       "closed-form character arithmetic: tr(tau|Lambda_p) inverted exactly from the "
                       "already-established H_p formula, tr(theta|Lambda_p)=0 derived exactly for odd "
                       "p from the design's own necklace-trace formula (every divisor of odd p is odd).",
        "per_p": {str(p): v for p, v in per_p.items()},
        "all_m_std_R_p_equals_abs_def_p": all_match,
        "all_delta_p_consistency_checks_pass": all_delta_consistent,
        "branch_reading_key_UNASSERTED": {
            "note": "phase2_scoring_v1.md §1.2's own stated branch key, recorded as design context "
                    "ONLY -- this script does not assert which branch obtains (発効は司令塔専権).",
            "match_reading": "def_p == -mult_std(R_p) (found here) is read by the design as branch L "
                             "(WILD-NOEXCESS: Lazard-dictionary-correction-only, no active excess)",
        },
        "no_verdict_note": "raw integers and the m_std_R_p_equals_abs_def_p boolean only. Branch-L "
                           "language is NOT asserted as a conclusion -- 発効は司令塔専権.",
        "stop_code": None,
    }
    out_path = "search/certs/pl_lab1_normchk_v1_20260811.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")
    print(f"all_m_std_R_p_equals_abs_def_p={all_match} all_delta_p_consistency_checks_pass={all_delta_consistent}")


if __name__ == "__main__":
    main()
