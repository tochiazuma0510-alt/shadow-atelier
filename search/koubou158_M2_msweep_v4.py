"""koubou158_M2_msweep_v4.py

v4 of the koubou158 target6 m1-direction sweep, per commander instruction
2026-08-22 (mathematician's final dual-form ruling, after the closed-
form theta-hexagon-defect identity was numerically confirmed).

CLOSED-FORM IDENTITY CHECK (mathematician's diagnosis, confirmed here):
  nabla(H_tau) - nabla(R_froz) = translate_by(value(f_yz)) . nabla(f(z,x).f(x,z))
at m=0, verified EXACTLY (dict equality after project_to_pi) against the
48-combination search's closest candidate (search/certs/
koubou158_M2_msweep_v3_20260822.json's predicted-winner row, 14-term
residual). This confirms the residual IS the theta-hexagon acceptance-
condition contribution, not an implementation bug -- see
closed_form_identity_check field below.

DUAL SWEEP (mathematician ruling: both forms are INDEPENDENT necessary
conditions for membership, since (2.18)/(2.19) together imply both
H_theta and H_tau structure; a discrepancy between them is explained by
the theta-row contribution, not a contradiction; they agree on accepted
trajectories):
  - primary   = frozen-template form (search/koubou158_m2_closedform_v2.py,
                h1(m)=pp[y^m++f_xy, x^m++Inv(f_xz), z^m++f_yz]) -- m=0
                SHA/byte-exact canary against target6.base_gradient
  - secondary = tau-orbit form (search/koubou158_m2_closedform_v1.py,
                z_word=(yx)^-1, f positive, order=[tau_g,tau2_g,g] --
                the closest of the 48 combinations tried, NOT required to
                match the frozen gradient exactly at m=0; its m=0
                residual against primary is exactly the theta-hexagon
                identity above)
A given m1 is SETTLED_NO (the slice is empty) if EITHER form gives a
depth-trustworthy NO (non_member=True with depth_requirement_satisfied=
True in the complete-BFS closure). Both verdicts are recorded per m1
regardless.

PREFLIGHT CAVEAT (found running v3, reported honestly, NOT silently
patched): for m1 in {2,3,5,6,8}, hexagon_1_coface_{0..4}(m1) does NOT
evaluate to e4.identity under EITHER form, at any coface slot (verified
computationally). This differs from the m=0 case (where value==identity
is enforced as a hard invariant by the original producer, search/
d972_b345_relfrat3_wordexpr_v8.py's build_wordexpr_candidate,
base_value==e4.identity). Interpreted here as: value==identity is a
CANARY-ONLY requirement (m=0 must reproduce the literal frozen relator);
for m1!=0 the construction is understood to generalize a candidate
"would-be hexagon" whose Fox gradient is tested as a vector-in-module
question regardless of whether the source word is literally a group
relator -- this is NOT re-derived or confirmed from first principles
here, it is the most consistent reading of the instructions received,
and is flagged prominently (not silently assumed) for mathematician
confirmation.

Everything else unchanged: m1 in {2,3,5,6,8}, complete-BFS core
(search/koubou158_L3_core_completebfs_v1.py, selftest-validated),
depth-satisfied acceptance order, J_MAX=12, "mod M1" bookkeeping
(6-point universe independent of the still-unresolved M1 subgroup).
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_1 as core  # noqa: E402
import koubou158_L3_core_completebfs_v1 as cbfs  # noqa: E402
import koubou158_m2_closedform_v1 as cf1  # noqa: E402
import koubou158_m2_closedform_v2 as cf2  # noqa: E402

SCHEMA = "koubou158-M2-msweep/v4"
Q3_CHIEF = core.Q3_CHIEF
Q3_CHIEF_SHA = core.Q3_CHIEF_SHA
Q3_CHIEF_BYTES = core.Q3_CHIEF_BYTES
J_MAX = core.J_MAX

REMAINING_M1 = [2, 3, 5, 6, 8]
SIX_POINT_UNIVERSE = [0, 2, 3, 5, 6, 8]
FROZEN_BASE_GRADIENT_SHA = "788fd8712f76a3ca254bb2179b5498fed3ca00e649ba0321ef297d2d985cc71e"
FROZEN_ENTRY_COUNT = 72

# secondary (tau-orbit) form parameters: the closest of the 48 combinations
TAU_Z_WORD = [-1, -2]  # (yx)^-1
TAU_PERM = ["tau_g", "tau2_g", "g"]


def element_blob(v):
    return v[0] + v[1]


def sha_inner(gradient, value):
    digest = hashlib.sha256()
    rows = sorted(gradient.items(), key=lambda row: (row[0][0], row[0][1]))
    for (component, element), coefficient in rows:
        blob = element_blob(element)
        digest.update(component.to_bytes(1, "little"))
        digest.update(len(blob).to_bytes(2, "little"))
        digest.update(blob)
        digest.update(int(coefficient).to_bytes(1, "little"))
    return digest.hexdigest()


def sha_obj(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def gradient_binding_sha(e4, word):
    val = e4.eval(word)
    grad = core.fox_gradient(e4, word)
    binding = {
        "name": "hexagon_1_coface_0", "kind": "hexagon", "entry_count": len(grad),
        "quotient_value_hex": element_blob(val).hex(),
        "canonical_gradient_sha256": sha_inner(grad, val),
        "canonical_order": "component then exact canonical E4 bytes",
        "digest_is_binding_only_not_element_equality": True,
    }
    return sha_obj(binding), len(grad), val == e4.identity


def build_secondary_h1(m, cofaces_3_4, slot):
    """tau-orbit form: z_word=(yx)^-1, f positive, perm=[tau_g,tau2_g,g]."""
    tau_images = [[2], TAU_Z_WORD]
    g = core.reduce_word([2] * m + core.FIXED_WORD)
    tau_g = cf1.word_substitute(g, tau_images)
    tau2_g = cf1.word_substitute(tau_g, tau_images)
    factors = {"g": g, "tau_g": tau_g, "tau2_g": tau2_g}
    seq = [factors[p] for p in TAU_PERM]
    H = core.reduce_word(seq[0] + seq[1] + seq[2])
    return cf1.push_through_coface(H, cofaces_3_4[slot])


def main() -> int:
    t_start = time.perf_counter()
    full = ROOT / Q3_CHIEF
    core.require(full.is_file(), "q3_chief receipt missing")
    core.require(full.stat().st_size == Q3_CHIEF_BYTES, "q3_chief byte drift")
    got_sha = core.sha_file(full)
    core.require(got_sha == Q3_CHIEF_SHA, f"q3_chief SHA drift: got {got_sha}")
    q3 = json.loads(full.read_text(encoding="utf-8"))
    e4 = core.E4(q3)
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    core.require(len(cofaces_3_4) == 5, "expected 5 cofaces")

    # ---- closed-form theta-hexagon-defect identity check (m=0) ----
    A_word = core.substitute2(core.FIXED_WORD, core.X0, core.Y0)
    B_word = core.substitute2(core.FIXED_WORD, core.X0, core.Z0)
    C_word = core.substitute2(core.FIXED_WORD, core.Y0, core.Z0)
    frozen_h1_slot0 = core.reduce_word(C_word + core.inv_word(B_word) + A_word)

    H0_primary = cf2.build_h1(0)
    h1_primary_slot0 = cf2.push_through_coface(H0_primary, cofaces_3_4[0])
    h1_secondary_slot0_m0 = build_secondary_h1(0, cofaces_3_4, 0)

    diff_word = core.reduce_word(h1_secondary_slot0_m0 + core.inv_word(frozen_h1_slot0))
    diff_pi = core.project_to_pi(core.fox_gradient(e4, diff_word))

    f_zx = core.substitute2(core.FIXED_WORD, core.Z0, core.X0)
    f_xz = core.substitute2(core.FIXED_WORD, core.X0, core.Z0)
    product_word = core.reduce_word(f_zx + f_xz)
    nabla_product = core.fox_gradient(e4, product_word)
    f_yz = core.substitute2(core.FIXED_WORD, core.Y0, core.Z0)
    translator_value = e4.eval(f_yz)
    translated_pi = core.project_to_pi(core.translate_vec(e4, nabla_product, translator_value))

    identity_check_match = diff_pi == translated_pi
    closed_form_identity_check = {
        "identity_verbatim": "nabla(H_tau) - nabla(R_froz) = translate_by(value(f_yz)) . "
                             "nabla(f(z,x).f(x,z)) [m=0; translator=f_yz at m=0]",
        "diff_term_count": len(diff_pi),
        "translated_term_count": len(translated_pi),
        "exact_match": identity_check_match,
        "verdict": "DIAGNOSIS CONFIRMED -- the 14-term residual between the tau-orbit form and "
                  "the frozen relator is EXACTLY the theta-hexagon acceptance-condition "
                  "contribution (translate of nabla(f(z,x).f(x,z)) by value(f_yz)), not an "
                  "implementation residual" if identity_check_match else
                  "MISMATCH -- diagnosis NOT confirmed, residual implementation gap remains",
    }
    print(f"[{time.strftime('%H:%M:%S')}] closed_form_identity_check: {closed_form_identity_check}",
          flush=True)
    core.require(identity_check_match, "157m2v4: theta-hexagon closed-form identity check FAILED "
                 "-- stopping per design (canary discipline)")

    # ---- canary: primary form m=0, all 5 cofaces, byte-exact + SHA ----
    canary_rows = []
    canary_pass = True
    for slot in range(5):
        h1_pb4 = cf2.push_through_coface(H0_primary, cofaces_3_4[slot])
        val = e4.eval(h1_pb4)
        sha, entry_count, is_identity = gradient_binding_sha(e4, h1_pb4)
        row = {"slot": slot, "word_len": len(h1_pb4), "value_is_identity": is_identity,
               "entry_count": entry_count, "sha256": sha}
        if slot == 0:
            row["eq_frozen_word_literal"] = (h1_pb4 == frozen_h1_slot0)
            row["sha_match_frozen_base_gradient"] = (sha == FROZEN_BASE_GRADIENT_SHA)
            canary_pass = canary_pass and row["eq_frozen_word_literal"] and row["sha_match_frozen_base_gradient"]
        canary_pass = canary_pass and is_identity
        canary_rows.append(row)
    print(f"[{time.strftime('%H:%M:%S')}] PRIMARY CANARY (m=0, all 5 cofaces): "
          f"pass={canary_pass}", flush=True)
    core.require(canary_pass, "157m2v4: primary canary FAILED")

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "predecessor_note": "search/certs/koubou158_M2_msweep_v3_20260822.json is the FROZEN "
                           "48-combination judgment table (status=CANARY_ALL_FAIL_STOPPED) -- "
                           "kept unchanged; this cert (v4) is the actual measurement, per "
                           "commander instruction to advance the version number since v3's name "
                           "was already claimed by that table.",
        "primary_construction_source": "search/koubou158_m2_closedform_v2.py",
        "secondary_construction_source": "search/koubou158_m2_closedform_v1.py "
                                        f"(z_word=(yx)^-1, f positive, perm={TAU_PERM})",
        "closed_form_identity_check": closed_form_identity_check,
        "dual_verdict_note_verbatim": (
            "(i) both forms (primary/theta-template and secondary/tau-orbit) are sound "
            "necessary conditions for membership -- (2.18)/(2.19) together imply both H_theta "
            "and H_tau structure; (ii) any discrepancy between the two forms' verdicts is "
            "explained by the theta-row contribution (see closed_form_identity_check above), "
            "not a contradiction; (iii) on the accepted (settled) trajectory the two forms "
            "agree. A given m1 is SETTLED_NO (slice empty) if EITHER form gives a depth-"
            "trustworthy NO."
        ),
        "primary_canary": {"rows": canary_rows, "pass": canary_pass},
        "preflight_caveat_identity_check": {
            "description": "hexagon_1_coface_{0..4}(m1) does NOT evaluate to e4.identity for "
                          "EITHER form at ANY m1 in {2,3,5,6,8}, at any coface slot -- verified "
                          "computationally, reported honestly rather than silently patched. "
                          "Interpreted as a canary-only requirement (m=0 must reproduce the "
                          "literal frozen relator); the m1-sweep tests the Fox gradient as a "
                          "vector-in-module membership question regardless of whether the "
                          "source word is literally a group relator for m1!=0. NOT independently "
                          "re-derived from first principles -- flagged for confirmation.",
            "value_is_identity_by_m1": {},
        },
        "input_provenance": {
            "q3_chief_receipt": {"path": str(Q3_CHIEF).replace("\\", "/"),
                                 "sha256": Q3_CHIEF_SHA, "bytes": Q3_CHIEF_BYTES},
        },
        "six_point_universe": {
            "value": SIX_POINT_UNIVERSE,
            "derivation": "charming condition u1=2*m1+1 in (Z/18)^x (L_ord=18, measured directly) "
                          "is equivalent to m1 in {0,2,3,5,6,8} (mod 9); over-approximation, safe "
                          "in the NO direction, recorded 'mod M1' -- independent of the separately "
                          "unresolved M1 subgroup / M_ord (search/certs/"
                          "koubou158_M1M2_findex_v1_20260822.json, a different open question).",
            "m1_equals_0_status": "already settled -- search/certs/"
                                  "koubou158_L3_radical_v1_1_20260822.json (settled_no=true, j_star=4)",
            "pentagon_row_note": "pentagon row is m-invariant; not re-tested.",
            "remaining_universe": REMAINING_M1,
        },
    }

    # ---- preflight per m1 (both forms, all 5 cofaces) -- non-fatal, recorded ----
    nabla_b_primary_pi: dict[int, dict] = {}
    nabla_b_secondary_pi: dict[int, dict] = {}
    for m1 in REMAINING_M1:
        H_primary = cf2.build_h1(m1)
        primary_rows = []
        for slot in range(5):
            h1_pb4 = cf2.push_through_coface(H_primary, cofaces_3_4[slot])
            val = e4.eval(h1_pb4)
            primary_rows.append({"slot": slot, "value_is_identity": val == e4.identity})
        secondary_rows = []
        for slot in range(5):
            h1_pb4 = build_secondary_h1(m1, cofaces_3_4, slot)
            val = e4.eval(h1_pb4)
            secondary_rows.append({"slot": slot, "value_is_identity": val == e4.identity})
        result["preflight_caveat_identity_check"]["value_is_identity_by_m1"][str(m1)] = {
            "primary": primary_rows, "secondary": secondary_rows,
        }
        primary_word0 = cf2.push_through_coface(H_primary, cofaces_3_4[0])
        secondary_word0 = build_secondary_h1(m1, cofaces_3_4, 0)
        nabla_b_primary_pi[m1] = core.project_to_pi(core.fox_gradient(e4, primary_word0))
        nabla_b_secondary_pi[m1] = core.project_to_pi(core.fox_gradient(e4, secondary_word0))

    print(f"[{time.strftime('%H:%M:%S')}] preflight recorded (non-fatal) for all m1 in "
          f"{REMAINING_M1}; nabla_b constructed both forms "
          f"({time.perf_counter() - t_start:.1f}s elapsed)", flush=True)

    # ---- weight structure sanity ----
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

    # ---- main dual sweep: complete-BFS core, depth-satisfied acceptance ----
    targets = [(m1, form) for m1 in REMAINING_M1 for form in ("primary", "secondary")]
    per_target_progression: dict[tuple, list[dict]] = {t: [] for t in targets}
    per_target_outcome: dict[tuple, dict] = {t: {"status": "PENDING"} for t in targets}
    remaining = set(targets)

    def nabla_for(m1, form):
        return nabla_b_primary_pi[m1] if form == "primary" else nabla_b_secondary_pi[m1]

    for j in range(2, J_MAX + 1):
        if not remaining:
            break
        t_j = time.perf_counter()
        try:
            ech_combined, idx, sp, info = cbfs.build_V_and_D2bar_from_q3_complete(e4, q3, j)
        except RuntimeError as exc:
            print(f"[{time.strftime('%H:%M:%S')}] j={j}: ABORTED -- {exc}", flush=True)
            for t in list(remaining):
                per_target_outcome[t] = {"status": "ABORTED_RESOURCE_CAP", "at_j": j, "error": str(exc)}
            remaining.clear()
            break
        elapsed_build = time.perf_counter() - t_j

        for t in list(remaining):
            m1, form = t
            target_proj = core.project_vec_to_Ij(nabla_for(m1, form), j)
            target_indexed = {idx[k]: c for k, c in target_proj.items() if k in idx}
            tv = sp.vec(target_indexed)
            ech_clone = ech_combined.clone()
            _, pivot = ech_clone.reduce(tv)
            non_member = pivot >= 0
            entry = {
                "j": j, "dim_Lambda_over_Ij": info["dim_Lambda_over_Ij"],
                "rank_V": info["rank_V"], "rank_V_plus_D2bar_combined": info["rank_V_plus_D2bar_combined"],
                "depth_requirement_satisfied": info["depth_requirement_satisfied"],
                "non_member": non_member,
            }
            per_target_progression[t].append(entry)
            if non_member and info["depth_requirement_satisfied"]:
                per_target_outcome[t] = {"status": "SETTLED_NO_DEPTH_TRUSTWORTHY", "j_star": j}
                remaining.discard(t)
            elif non_member and not info["depth_requirement_satisfied"]:
                print(f"[{time.strftime('%H:%M:%S')}] j={j} {t}: non_member=True but depth NOT "
                      f"satisfied -- continuing", flush=True)

        elapsed_j = time.perf_counter() - t_j
        print(f"[{time.strftime('%H:%M:%S')}] j={j}: dim={info['dim_Lambda_over_Ij']} "
              f"build={elapsed_build:.1f}s total={elapsed_j:.1f}s remaining={sorted(remaining)}",
              flush=True)

    for t in targets:
        if per_target_outcome[t]["status"] == "PENDING":
            per_target_outcome[t] = {"status": "J_MAX_EXHAUSTED_INCONCLUSIVE", "j_max": J_MAX}

    elapsed = time.perf_counter() - t_start

    m1_verdicts = {}
    for m1 in REMAINING_M1:
        primary_outcome = per_target_outcome[(m1, "primary")]
        secondary_outcome = per_target_outcome[(m1, "secondary")]
        either_settled = (primary_outcome["status"] == "SETTLED_NO_DEPTH_TRUSTWORTHY" or
                          secondary_outcome["status"] == "SETTLED_NO_DEPTH_TRUSTWORTHY")
        m1_verdicts[str(m1)] = {
            "primary_outcome": primary_outcome,
            "primary_j_progression": per_target_progression[(m1, "primary")],
            "secondary_outcome": secondary_outcome,
            "secondary_j_progression": per_target_progression[(m1, "secondary")],
            "slice_settled_no": either_settled,
        }

    all_settled = all(v["slice_settled_no"] for v in m1_verdicts.values())
    any_aborted = any(v["primary_outcome"]["status"] == "ABORTED_RESOURCE_CAP" or
                      v["secondary_outcome"]["status"] == "ABORTED_RESOURCE_CAP"
                      for v in m1_verdicts.values())

    if all_settled:
        top_verdict = "ALL_FIVE_SLICES_SETTLED_NO_M_DIRECTION_CLOSED"
    elif any_aborted:
        top_verdict = "RESOURCE_CAP_ABORTED_SEE_PER_M1_OUTCOME"
    else:
        top_verdict = "SOME_SLICES_INCONCLUSIVE_SEE_PER_M1_OUTCOME"

    result["verdict"] = top_verdict
    result["m1_verdicts"] = m1_verdicts
    result["all_five_slices_settled_no"] = all_settled
    result["m1_equals_0_reference"] = {
        "cert": "search/certs/koubou158_L3_radical_v1_1_20260822.json",
        "settled_no": True, "j_star": 4,
    }
    result["grade"] = ("candidate, single-system producer measurement (own IndependentPc/E4, own "
                       "Jennings/radical-filtration code); primary canary PASSED byte-exact "
                       "against the frozen target6.base_gradient; theta-hexagon-defect closed-form "
                       "identity CONFIRMED exactly for the secondary form's m=0 residual; "
                       "complete-BFS depth-fix engine independently selftested; no independent "
                       "SECOND-SYSTEM computational cross-check of this m-sweep has been run yet")
    result["wall_clock_seconds"] = elapsed

    today = date.today().isoformat().replace("-", "")
    out_path = ROOT / "search" / "certs" / f"koubou158_M2_msweep_v4_{today}.json"
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    readback = out_path.read_text(encoding="utf-8")
    core.require(readback == text, "checked-write readback mismatch")

    print(f"KOUBOU158_M2_MSWEEP_V4 verdict={top_verdict} elapsed_s={elapsed:.2f} "
          f"output={out_path.as_posix()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
