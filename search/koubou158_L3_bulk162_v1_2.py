"""koubou158_L3_bulk162_v1_2.py

v1.2 regeneration of the 162-branch L3 bulk re-verdict, per falsifier
mid-read verdict 2026-08-22 (3 required repairs -- see
search/koubou158_L3_core_v1_2.py docstring and
search/koubou158_L3_radical_v1_2.py's header for the full rationale).
v1's cert (koubou158_L3_bulk162_v1_20260822.json) is kept unchanged
(no-rename policy).

Same branch-independent V+im(D2bar) reuse pattern as v1, now built via
core_v1_2's repaired ordering (im(D2bar) fresh-echelon first, V added to
a clone second) and Delta-identification checks. Adds:
  - required-match asserts against the v1/v1.1 historical numbers
    (rank_D2bar_alone=310, rank_V=4, rank_combined=314 at j=4)
  - RECOMMENDED 5: an independent re-invocation of
    build_V_and_D2bar_from_q3 AFTER all 162 branch clones have been
    tested, confirming no state leaked/mutated across 162 ech_shared.
    clone() calls (a code-level, not mathematical, regression check)
  - a note on the separator-support distribution across the 144 NON-
    MEMBER branches (falsifier flag: "大半 support-1(零列駆動)である
    事実は修理1・2と併せてcertに注視事項として1行" -- most separators
    are support-1, i.e. driven by a single zero column in the row
    matrix; recorded as an observation to watch, not over-interpreted)
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_2 as core  # noqa: E402

SCHEMA = "koubou158-L3-bulk162/v1.2"

Q3_CHIEF = core.Q3_CHIEF
Q3_CHIEF_SHA = core.Q3_CHIEF_SHA
Q3_CHIEF_BYTES = core.Q3_CHIEF_BYTES

COLGEN_RECEIPT = Path("ci/b345_157en_artifacts_32458556448/d972_b345_target6_dual_colgen_v2.json")

X0, Y0, Z0 = core.X0, core.Y0, core.Z0
J_FIXED = 4
N_ROOFS = 6
N_CORRECTIONS = 27
N_BRANCHES = 162

EXPECTED_RANK_D2BAR_ALONE = 310
EXPECTED_RANK_V = 4
EXPECTED_RANK_COMBINED = 314


def roof_word(q3: dict, roof_index: int) -> list[int]:
    return q3["canonical_roof_powers"]["rows"][roof_index]["word"]


def correction_word(q3: dict, correction_index: int) -> list[int]:
    return q3["correction_fibre"]["records"][correction_index]["word"]


def main() -> int:
    t_start = time.perf_counter()

    full = ROOT / Q3_CHIEF
    core.require(full.is_file(), "q3_chief receipt missing")
    core.require(full.stat().st_size == Q3_CHIEF_BYTES, "q3_chief byte drift")
    got_sha = core.sha_file(full)
    core.require(got_sha == Q3_CHIEF_SHA, f"q3_chief SHA drift: got {got_sha}")
    q3 = json.loads(full.read_text(encoding="utf-8"))
    core.require(len(q3["canonical_roof_powers"]["rows"]) == N_ROOFS, "roof row count")
    core.require(len(q3["correction_fibre"]["records"]) == N_CORRECTIONS, "correction record count")

    e4 = core.E4(q3)

    print(f"[{time.strftime('%H:%M:%S')}] E4 built. Building branch-independent "
          f"V + im(D2bar) at j={J_FIXED} (v1.2 ordering: D2bar fresh-echelon first, "
          f"V added to a clone second)...", flush=True)

    ech_shared, idx, sp, info = core.build_V_and_D2bar_from_q3(e4, q3, J_FIXED)
    core.require(info["rank_D2bar_alone"] == EXPECTED_RANK_D2BAR_ALONE,
                 f"rank_D2bar_alone changed: got {info['rank_D2bar_alone']}, expected {EXPECTED_RANK_D2BAR_ALONE}")
    core.require(info["rank_V"] == EXPECTED_RANK_V,
                 f"rank_V changed: got {info['rank_V']}, expected {EXPECTED_RANK_V}")
    core.require(info["rank_V_plus_D2bar_combined"] == EXPECTED_RANK_COMBINED,
                 f"rank_combined changed: got {info['rank_V_plus_D2bar_combined']}, expected {EXPECTED_RANK_COMBINED}")

    print(f"[{time.strftime('%H:%M:%S')}] shared base built: |Delta|={info['n_Delta']} "
          f"n_schreier={info['n_schreier_generators']} delta_type={info['delta_isomorphism_type']} "
          f"dim(Lambda/I^{J_FIXED})={info['dim_Lambda_over_Ij']} "
          f"rank_D2bar_alone={info['rank_D2bar_alone']} rank_V={info['rank_V']} "
          f"rank_combined={info['rank_V_plus_D2bar_combined']} "
          f"({time.perf_counter() - t_start:.1f}s elapsed)", flush=True)

    per_branch = []
    n_non_member = 0
    n_member = 0
    support_counter: Counter = Counter()
    for r in range(N_ROOFS):
        for c in range(N_CORRECTIONS):
            bid = f"r{r}_c{c}"
            rw = roof_word(q3, r)
            cw = correction_word(q3, c)
            candidate_word = core.reduce_word(list(rw) + list(cw))
            c_word = core.substitute2(candidate_word, Y0, Z0)
            b_word = core.substitute2(candidate_word, X0, Z0)
            a_word = core.substitute2(candidate_word, X0, Y0)
            h1_word = core.reduce_word(c_word + core.inv_word(b_word) + a_word)
            nabla_bp_E4 = core.fox_gradient(e4, h1_word)
            nabla_bp_pi = core.project_to_pi(nabla_bp_E4)

            target_proj = core.project_vec_to_Ij(nabla_bp_pi, J_FIXED)
            target_indexed = {idx[k]: co for k, co in target_proj.items() if k in idx}
            tv = sp.vec(target_indexed)

            ech_branch = ech_shared.clone()
            _, pivot = ech_branch.reduce(tv)
            non_member = pivot >= 0

            separator_info = None
            if non_member:
                sep = ech_branch.extract_separator(tv)
                core.require(sep is not None, f"branch {bid}: separator extraction failed unexpectedly")
                support = bin(sep[0] | sep[1]).count("1")
                phi_val = sp.dot(sep, tv)
                separator_info = {"support": support, "phi_nabla_bprime": phi_val}
                support_counter[support] += 1

            if non_member:
                n_non_member += 1
            else:
                n_member += 1
            per_branch.append({
                "branch_id": bid, "roof_index": r, "correction_index": c,
                "non_member_at_L3": non_member,
                "separator": separator_info,
            })

    # RECOMMENDED 5: independent re-invocation AFTER all 162 clone() calls
    # -- confirms no state mutation leaked across branches.
    ech_recheck, idx_recheck, sp_recheck, info_recheck = core.build_V_and_D2bar_from_q3(e4, q3, J_FIXED)
    rebuild_consistency_ok = (
        info_recheck["rank_D2bar_alone"] == info["rank_D2bar_alone"] and
        info_recheck["rank_V"] == info["rank_V"] and
        info_recheck["rank_V_plus_D2bar_combined"] == info["rank_V_plus_D2bar_combined"] and
        info_recheck["schreier_generators_digest"] == info["schreier_generators_digest"]
    )
    core.require(rebuild_consistency_ok,
                 f"RECOMMENDED CHECK 5 FAILED (post-162-branch re-invocation): {info_recheck} vs {info}")
    print(f"[{time.strftime('%H:%M:%S')}] recommended check 5 (post-162-branch re-invocation): "
          f"rebuild_consistency_ok={rebuild_consistency_ok}", flush=True)

    elapsed = time.perf_counter() - t_start
    non_member_ids = sorted(b["branch_id"] for b in per_branch if b["non_member_at_L3"])
    member_ids = sorted(b["branch_id"] for b in per_branch if not b["non_member_at_L3"])
    support_distribution = dict(sorted(support_counter.items()))
    n_support1 = support_counter.get(1, 0)

    cert: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "spec_source": "v1.2 regeneration of koubou158_L3_bulk162_v1.json per falsifier "
                       "mid-read verdict 2026-08-22 (3 required repairs) -- see "
                       "search/koubou158_L3_core_v1_2.py and "
                       "search/koubou158_L3_radical_v1_2.py for full rationale",
        "predecessor_cert": "search/certs/koubou158_L3_bulk162_v1_20260822.json (kept unchanged, "
                            "no-rename policy)",
        "input_provenance": {
            "q3_chief_receipt": {"path": str(Q3_CHIEF).replace("\\", "/"), "sha256": Q3_CHIEF_SHA, "bytes": Q3_CHIEF_BYTES},
            "colgen_receipt_path": str(COLGEN_RECEIPT).replace("\\", "/"),
        },
        "j_fixed": J_FIXED,
        "shared_base_info": info,
        "required_match_asserts": {
            "rank_D2bar_alone_expected": EXPECTED_RANK_D2BAR_ALONE,
            "rank_V_expected": EXPECTED_RANK_V,
            "rank_combined_expected": EXPECTED_RANK_COMBINED,
            "all_matched": True,
        },
        "recommended_5_post_branch_rebuild_consistency": {"rebuild_consistency_ok": rebuild_consistency_ok},
        "bug_fix_inv_gen_note": (
            "IndependentPc.inverse() (search/koubou158_L3_core_v1_2.py) had a LATENT bug: "
            "_inv_gen was built from pb4['marked_generators'] (only 6 entries) instead of "
            "pb4['inverses'] (all 10 pc-generators) -- calling pc.inverse() on a general "
            "group element with nonzero support on generators 7-10 (weight-2 layer) raised "
            "IndexError. Dormant in every prior script this session (pc.inverse() was only "
            "ever called on single-marked-generator unit vectors there); first triggered by "
            "this lane's own repair-3 zbar-identification check, found and fixed while "
            "implementing it, independently re-discovered by the falsifier. Fixed by "
            "sourcing _inv_gen from pb4['inverses'] (all 10 rows). No effect on any "
            "already-published rank/membership numbers."
        ),
        "n_branches_total": len(per_branch),
        "n_non_member_at_L3": n_non_member,
        "n_member_at_L3": n_member,
        "non_member_at_L3_branch_ids": non_member_ids,
        "member_at_L3_branch_ids": member_ids,
        "separator_support_distribution_note": (
            f"among the {n_non_member} NON-MEMBER branches, {n_support1} ({100*n_support1/n_non_member:.0f}%) "
            f"have separator support=1 (i.e. driven by a single ZERO COLUMN in the row matrix -- the "
            "cheapest possible witness). Full distribution: " + str(support_distribution) + ". "
            "Flagged (falsifier instruction) as an item to WATCH alongside repairs 1/2 -- a "
            "support-1-dominant pattern is consistent with the branch-independent V+im(D2bar) "
            "base already containing most of the relevant structure (rank 314/636), with only a "
            "thin, easily-isolated coordinate distinguishing most branches' targets -- not "
            "independently verified as a DEEPER structural fact here, just recorded as observed."
        ),
        "separator_support_distribution": support_distribution,
        "per_branch": per_branch,
        "meaning_note": (
            "a branch's non_member_at_L3=true UPGRADES that branch's death claim from "
            "L1-only (block[0:9], registered-108-seed-family) to L3-full-legal-correction-"
            "family -- part of condition (i)'s 162-branch census discharges beyond the "
            "L1-limited claim boundary for such branches. non_member_at_L3=false is recorded "
            "honestly and is NOT a contradiction of that branch's existing L1 death."
        ),
        "k3_overapproximation_caveat": "V is built from the FULL kernel K, not the true "
                                       "exponent-sum-mod-3-filtered legal-correction span -- "
                                       "non_member_at_L3=true is sound/stronger; "
                                       "non_member_at_L3=false does not by itself prove "
                                       "membership in the TRUE, smaller span",
        "wall_clock_seconds": elapsed,
        "grade": "candidate, single-system producer measurement, v1.2 (3 required repairs "
                "applied, recommended check 5 applied). Falsifier verdict pending on this "
                "v1.2 regeneration.",
    }

    today = date.today().isoformat().replace("-", "")
    out_path = ROOT / "search" / "certs" / f"koubou158_L3_bulk162_v1_2_{today}.json"
    text = json.dumps(cert, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    readback = out_path.read_text(encoding="utf-8")
    core.require(readback == text, "checked-write readback mismatch")

    print(f"KOUBOU158_L3_BULK162_V1_2 n_non_member={n_non_member}/{len(per_branch)} "
          f"support1_fraction={n_support1}/{n_non_member} rebuild_consistency_ok={rebuild_consistency_ok} "
          f"elapsed_s={elapsed:.2f} output={out_path.as_posix()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
