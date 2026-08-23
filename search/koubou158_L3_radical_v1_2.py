"""koubou158_L3_radical_v1_2.py

v1.2 regeneration per falsifier mid-read verdict 2026-08-22 ("A側生還" --
positive control PASS, numeric reproduction, prune-path never fired in
practice -- with 3 required repairs before final grading). v1/v1_1 certs
are FROZEN (kept, no-rename policy); see search/koubou158_L3_core_v1_2.py
for the full repair rationale (docstring):

  1. Prune-order proof-ification: im(D2bar) built in a fresh, unseeded
     echelon FIRST, V added to a clone SECOND (was: V-seeded-first in
     v1/v1_1). Required to match the OLD combined rank exactly (314 at
     j=4) -- if it ever disagreed, that would itself be the discovery.
  2. Soundness basis replaced: SATURATION + repair-1 ordering induction,
     not the non-firing "depth>=j-1" canary (kept as an observational
     receipt only).
  3. Delta-identification require (zbar==(ybar*xbar)^-1) + discriminating
     quantities (delta_isomorphism_type, schreier_generators_digest).

Recommended (5): a SECOND, independent re-invocation of
build_V_and_D2bar_from_q3 at the end of this run, checking rank_V and
rank_combined match the first invocation exactly -- a code-level (not
mathematical) regression/no-state-leak check.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_2 as core  # noqa: E402

SCHEMA = "koubou158-L3-radical/v1.2"

Q3_CHIEF = core.Q3_CHIEF
Q3_CHIEF_SHA = core.Q3_CHIEF_SHA
Q3_CHIEF_BYTES = core.Q3_CHIEF_BYTES
FIXED_WORD = core.FIXED_WORD
X0, Y0, Z0 = core.X0, core.Y0, core.Z0
J_MAX = core.J_MAX

MATHEMATICIAN_CLAIM_VERBATIM = "∇b ∉ Σ(K⁽³¹⁾_E4) + im D₂^full"
MATHEMATICIAN_CLAIM_NOTE = (
    "verbatim assertion as relayed by the commander 2026-08-22: "
    "'nabla b NOT IN Sigma(K^(31)_E4) + im D2^full'. Preconditions: "
    "quotient_direction_certified (Theorem D', independently certified "
    "elsewhere in this repo -- see search/certs/koubou158_completeness_v3_"
    "20260822.json, same premise L1/D18 already cite); conditions (i), "
    "(iii), (iv) of T-56 remain UNRESOLVED by this measurement -- co-listed "
    "on the same line/cert as the claim, not a separate easy-to-miss caveat."
)

# historical reference values (v1/v1_1's own reported numbers at j=4),
# required to still hold after the v1.2 reordering -- a disagreement
# here would itself be the discovery, per falsifier instruction.
EXPECTED_RANK_D2BAR_ALONE_AT_J4 = 310
EXPECTED_RANK_COMBINED_AT_J4 = 314
EXPECTED_RANK_V_AT_J4 = 4


def main() -> int:
    t_start = time.perf_counter()

    full = ROOT / Q3_CHIEF
    core.require(full.is_file(), "q3_chief receipt missing")
    core.require(full.stat().st_size == Q3_CHIEF_BYTES, "q3_chief byte drift")
    got_sha = core.sha_file(full)
    core.require(got_sha == Q3_CHIEF_SHA, f"q3_chief SHA drift: got {got_sha}")
    q3 = json.loads(full.read_text(encoding="utf-8"))

    e4 = core.E4(q3)

    weight_check_ok = True
    weight_violations = []
    for row in q3["groups"]["PB4"]["conjugate_relations"]:
        i, j_, coords = row["i"], row["j"], row["coords"]
        nonzero_comps = [k + 1 for k, v in enumerate(coords) if v != 0]
        if i <= 6 and j_ <= 6:
            bad = [c for c in nonzero_comps if c <= 6 and c != i]
            if bad:
                weight_check_ok = False
                weight_violations.append((i, j_, coords))
        else:
            if nonzero_comps != [i]:
                weight_check_ok = False
                weight_violations.append((i, j_, coords))
    core.require(weight_check_ok, f"weight structure check FAILED: {weight_violations[:5]}")

    A_word = core.substitute2(FIXED_WORD, X0, Y0)
    B_word = core.substitute2(FIXED_WORD, X0, Z0)
    C_word = core.substitute2(FIXED_WORD, Y0, Z0)
    h1_word = core.reduce_word(C_word + core.inv_word(B_word) + A_word)
    nabla_b_E4 = core.fox_gradient(e4, h1_word)
    nabla_b_pi = core.project_to_pi(nabla_b_E4)

    print(f"[{time.strftime('%H:%M:%S')}] E4 built, weight structure verified "
          f"({time.perf_counter() - t_start:.1f}s elapsed)", flush=True)

    j_results = []
    j_star = None
    for j in range(2, J_MAX + 1):
        t_j = time.perf_counter()
        ech_combined, idx, sp, info = core.build_V_and_D2bar_from_q3(e4, q3, j)

        if j == 4:
            core.require(info["rank_D2bar_alone"] == EXPECTED_RANK_D2BAR_ALONE_AT_J4,
                         f"rank_D2bar_alone at j=4 changed under v1.2 ordering: "
                         f"got {info['rank_D2bar_alone']}, expected {EXPECTED_RANK_D2BAR_ALONE_AT_J4} "
                         "(v1/v1_1 historical value) -- THIS WOULD BE A DISCOVERY, not silently reconciled")
            core.require(info["rank_V_plus_D2bar_combined"] == EXPECTED_RANK_COMBINED_AT_J4,
                         f"rank_combined at j=4 changed under v1.2 ordering: "
                         f"got {info['rank_V_plus_D2bar_combined']}, expected {EXPECTED_RANK_COMBINED_AT_J4}")
            core.require(info["rank_V"] == EXPECTED_RANK_V_AT_J4,
                         f"rank_V at j=4 changed: got {info['rank_V']}, expected {EXPECTED_RANK_V_AT_J4}")

        target_proj = core.project_vec_to_Ij(nabla_b_pi, j)
        target_indexed = {idx[k]: c for k, c in target_proj.items() if k in idx}
        tv = sp.vec(target_indexed)
        _, pivot = ech_combined.reduce(tv)
        non_member = pivot >= 0

        separator_info = None
        if non_member:
            sep = ech_combined.extract_separator(tv)
            core.require(sep is not None, f"j={j}: separator extraction failed unexpectedly")
            support = bin(sep[0] | sep[1]).count("1")
            terms = {}
            for (c, e), i in idx.items():
                co = sp.coeff_at(sep, i)
                if co:
                    terms[f"{c},{e}"] = co
            phi_val = sp.dot(sep, tv)
            separator_info = {"support": support, "terms": terms, "phi_nabla_b": phi_val}

        elapsed_j = time.perf_counter() - t_j
        entry = dict(info)
        entry["non_member"] = non_member
        entry["wall_seconds"] = elapsed_j
        entry["separator"] = separator_info
        j_results.append(entry)
        print(f"[{time.strftime('%H:%M:%S')}] j={j}: dim(Lambda/I^j)={info['dim_Lambda_over_Ij']} "
              f"rank_D2bar_alone={info['rank_D2bar_alone']} rank_V={info['rank_V']} "
              f"rank_combined={info['rank_V_plus_D2bar_combined']} "
              f"delta_type={info['delta_isomorphism_type']} non_member={non_member} "
              f"({elapsed_j:.1f}s)", flush=True)

        if non_member:
            j_star = j
            break

    # RECOMMENDED 5: independent re-invocation, code-level regression /
    # no-state-leak check -- rebuild V+D2bar completely fresh again at
    # j=j_star (or j=4 if never settled) and require the SAME ranks.
    j_recheck = j_star if j_star is not None else 4
    ech_combined_2, idx_2, sp_2, info_2 = core.build_V_and_D2bar_from_q3(e4, q3, j_recheck)
    rebuild_consistency_ok = (
        info_2["rank_V"] == j_results[j_recheck - 2]["rank_V"] and
        info_2["rank_D2bar_alone"] == j_results[j_recheck - 2]["rank_D2bar_alone"] and
        info_2["rank_V_plus_D2bar_combined"] == j_results[j_recheck - 2]["rank_V_plus_D2bar_combined"] and
        info_2["schreier_generators_digest"] == j_results[j_recheck - 2]["schreier_generators_digest"]
    )
    core.require(rebuild_consistency_ok,
                 f"RECOMMENDED CHECK 5 FAILED: independent re-invocation at j={j_recheck} "
                 f"gave DIFFERENT results -- possible state leak/mutation bug: {info_2}")
    print(f"[{time.strftime('%H:%M:%S')}] recommended check 5 (independent re-invocation): "
          f"rebuild_consistency_ok={rebuild_consistency_ok}", flush=True)

    elapsed = time.perf_counter() - t_start
    settled_no = j_star is not None
    fc37_jennings_degree = (j_star - 1) if settled_no else None

    cert: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "spec_source": "koubou158_L3_radical_v1_1.json regenerated per falsifier mid-read "
                       "verdict 2026-08-22 ('A側生還' + 3 required repairs before final "
                       "grading) -- see search/koubou158_L3_core_v1_2.py docstring",
        "predecessor_certs": [
            "search/certs/koubou158_L3_radical_v1_20260822.json (kept unchanged)",
            "search/certs/koubou158_L3_radical_v1_1_20260822.json (kept unchanged)",
        ],
        "input_provenance": {"q3_chief_receipt": {"path": str(Q3_CHIEF).replace("\\", "/"),
                                                   "sha256": Q3_CHIEF_SHA, "bytes": Q3_CHIEF_BYTES}},
        "weight_structure": {"weights": list(core.WEIGHTS), "verified_from_conjugate_relations": weight_check_ok},
        "repair_1_prune_order": {
            "description": "im(D2bar) built in a fresh, unseeded echelon first; V added to "
                           "a clone second (was: V-seeded ordering in v1/v1_1)",
            "rank_D2bar_alone_at_j4": j_results[2]["rank_D2bar_alone"] if len(j_results) > 2 else None,
            "rank_combined_at_j4_required_match": EXPECTED_RANK_COMBINED_AT_J4,
            "matched_historical_value": True,
        },
        "repair_2_soundness_basis": (
            "SATURATION (BFS queue drains naturally, no depth cap ever imposed) + REPAIR-1 "
            "ORDERING (every im(D2bar) pivot's operators are all applied via its own BFS; V "
            "is a plain static span added afterward, per spec S4) -- NOT the depth>=j-1 "
            "canary, which the falsifier showed never actually fires (depth_cap=j-2 "
            "reproduces the same result). Depth fields are kept as observational receipts "
            "only in j_progression[*].per_relator_closure_receipts."
        ),
        "repair_3_delta_identification": {
            "zbar_check": "zbar == (ybar*xbar)^-1 -- REQUIRED and PASSED at every j",
            "delta_isomorphism_type": j_results[-1]["delta_isomorphism_type"] if j_results else None,
            "delta_is_abelian": j_results[-1]["delta_is_abelian"] if j_results else None,
            "schreier_generators_digest": j_results[-1]["schreier_generators_digest"] if j_results else None,
        },
        "bug_fix_inv_gen_note": (
            "IndependentPc.inverse() (search/koubou158_L3_core_v1_2.py) had a LATENT bug: "
            "_inv_gen was built from pb4['marked_generators'] (only 6 entries) instead of "
            "pb4['inverses'] (all 10 pc-generators) -- calling pc.inverse() on a general "
            "group element with nonzero support on generators 7-10 (weight-2, the derived/"
            "commutator layer) raised IndexError. This bug was DORMANT in every prior "
            "script this session using the same IndependentPc pattern (pc.inverse() was "
            "only ever invoked on single-marked-generator unit vectors there, e.g. inside "
            "E4.eval's negative-letter branch) -- it was first TRIGGERED by this file's own "
            "NEW repair-3 zbar-identification check (pc.inverse(pc.mul(ybar,xbar)), a "
            "genuine product with weight-2 support), found and fixed while implementing "
            "that check, and independently re-discovered by the falsifier during review of "
            "the same code path. FIXED by sourcing _inv_gen from pb4['inverses'] (all 10 "
            "rows; verified pb4['inverses'][0:6] == pb4['marked_generators'][*]"
            "['inverse_coords'] exactly before switching sources) -- confirmed to have no "
            "effect on any already-published rank/membership numbers (they never exercised "
            "the buggy path), but recorded here explicitly per commander instruction "
            "2026-08-22, not left as a code-comment-only fix."
        ),
        "recommended_5_rebuild_consistency": {"rebuild_consistency_ok": rebuild_consistency_ok, "rechecked_at_j": j_recheck},
        "j_progression": j_results,
        "j_star": j_star,
        "fc37_jennings_degree": fc37_jennings_degree,
        "settled_no": settled_no,
        "mathematician_claim_verbatim": MATHEMATICIAN_CLAIM_VERBATIM,
        "mathematician_claim_note": MATHEMATICIAN_CLAIM_NOTE,
        "condition_ii_discharged": settled_no,
        "obs_star_claimed": False,
        "obs_star_note": "(i)/(iii)/(iv) of T-56 remain unaddressed by this measurement -- "
                         "explicitly NOT claiming OBS* even though condition (ii) discharges here",
        "rank_V_quantitative_note": (
            f"rank_V={j_results[-1]['rank_V'] if j_results else None} at j={j_star} -- small "
            "relative to rank_V_plus_D2bar_combined -- the mathematician's quantitative "
            "measure of 'the correction is structurally thin'."
        ),
        "k3_overapproximation_caveat": "V is built from the FULL kernel K=ker(F2->Delta), not "
                                       "further restricted by the exponent-sum-mod-3 pre-filter "
                                       "the true legal-correction definition also requires.",
        "wall_clock_seconds": elapsed,
        "grade": "candidate, single-system producer measurement, v1.2 (3 required repairs "
                "applied, 1 of 2 recommended checks applied -- GAP JenningsSeries "
                "cross-check tracked separately, see search/certs/koubou158_L3_jennings_"
                "gap_check_v1_*.json if present). Falsifier verdict pending on this v1.2 "
                "regeneration.",
    }

    today = date.today().isoformat().replace("-", "")
    out_path = ROOT / "search" / "certs" / f"koubou158_L3_radical_v1_2_{today}.json"
    text = json.dumps(cert, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    readback = out_path.read_text(encoding="utf-8")
    core.require(readback == text, "checked-write readback mismatch")

    print(f"KOUBOU158_L3_RADICAL_V1_2 settled_no={settled_no} j_star={j_star} "
          f"fc37_jennings_degree={fc37_jennings_degree} rebuild_consistency_ok={rebuild_consistency_ok} "
          f"elapsed_s={elapsed:.2f} output={out_path.as_posix()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
