"""koubou158_M2_msweep_v3.py

v3 of the koubou158 target6 m1-direction sweep (condition (iv) universe
completeness), per commander instruction 2026-08-22 (mathematician's
final closed-form construction, theta-hexagon defect diagnosed and
fixed -- see search/koubou158_m2_closedform_v2.py and search/certs/
koubou158_M2_msweep_v3_20260822.json [the CANARY_ALL_FAIL_STOPPED cert
from the previous round, superseded by this v3 measurement cert]).

Construction: h1(m) = pp[y^m++f_xy, x^m++Inv(f_xz), z^m++f_yz], z=(yx)^-1
-- sigma-free, no GAP, no Reidemeister-Schreier. At m=0 this is BYTE-
IDENTICAL (not just SHA-equal) to the frozen target6.base_gradient's
source word, confirmed in search/koubou158_m2_closedform_v2.py's own
module docstring derivation and re-verified here as the mandatory
canary gate before any m1 in {2,3,5,6,8} sweep is trusted.

m-universe (unchanged from v2/v1): mathematician's charming-condition
derivation u1=2*m1+1 in (Z/18)^x (L_ord=18, measured directly, see
search/certs/koubou158_M2_msweep_v1_20260822.json) is EQUIVALENT to
m1 in {0,2,3,5,6,8} (mod 9) -- an OVER-approximation, safe in the NO
direction, recorded here as "mod M1" bookkeeping: this measurement does
NOT resolve, depend on, or require knowledge of the (separately
unresolved, see search/certs/koubou158_M1M2_findex_v1_20260822.json) M1
subgroup or its order M_ord -- the 6-point universe is derived solely
from the charming-condition-necessary modulus 9, independent of M_ord.
m1=0 is already settled (C-12/C-13, search/certs/
koubou158_L3_radical_v1_1_20260822.json, settled_no=true, j_star=4).
Pentagon row is m-invariant, not re-tested.

Depth-fix (v2.1's order-of-evaluation correction, unchanged): uses the
complete (non-pruned) BFS submodule closure (search/
koubou158_L3_core_completebfs_v1.py, already selftest-validated against
the trusted m1=0 result) so that a NO is only accepted when
depth_requirement_satisfied=True AT THE SAME j -- an untrustworthy NO
(non_member=True but depth not yet satisfied) does not stop the j-loop;
it continues to the next j.

Preflight (per m1, mathematician-requested re-evaluation): before
running the expensive L3 membership test for a given m1, verify
hexagon_1_coface_0(m1) actually evaluates to e4.identity in ALL 5
cofaces (a necessary well-formedness condition for it to be a genuine
hexagon-relator family member -- analogous to build_wordexpr_candidate's
own base_value==e4.identity gate). A failure here would mean the
construction breaks down for that m1 and the nabla_b(m1) test would be
built on a non-relator, hence meaningless.
"""
from __future__ import annotations

import hashlib
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
import koubou158_m2_closedform_v2 as cf2  # noqa: E402

SCHEMA = "koubou158-M2-msweep/v3"
Q3_CHIEF = core.Q3_CHIEF
Q3_CHIEF_SHA = core.Q3_CHIEF_SHA
Q3_CHIEF_BYTES = core.Q3_CHIEF_BYTES
J_MAX = core.J_MAX

REMAINING_M1 = [2, 3, 5, 6, 8]
SIX_POINT_UNIVERSE = [0, 2, 3, 5, 6, 8]

FROZEN_BASE_GRADIENT_SHA = "788fd8712f76a3ca254bb2179b5498fed3ca00e649ba0321ef297d2d985cc71e"
FROZEN_ENTRY_COUNT = 72


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

    # ---- mandatory canary: m=0, all 5 cofaces, byte-exact + SHA check ----
    A_word = core.substitute2(core.FIXED_WORD, core.X0, core.Y0)
    B_word = core.substitute2(core.FIXED_WORD, core.X0, core.Z0)
    C_word = core.substitute2(core.FIXED_WORD, core.Y0, core.Z0)
    frozen_h1_slot0 = core.reduce_word(C_word + core.inv_word(B_word) + A_word)

    H0 = cf2.build_h1(0)
    canary_rows = []
    canary_pass = True
    for slot in range(5):
        h1_pb4 = cf2.push_through_coface(H0, cofaces_3_4[slot])
        val = e4.eval(h1_pb4)
        sha, entry_count, is_identity = gradient_binding_sha(e4, h1_pb4)
        row = {
            "slot": slot, "word_len": len(h1_pb4), "value_is_identity": is_identity,
            "entry_count": entry_count, "sha256": sha,
        }
        if slot == 0:
            row["eq_frozen_word_literal"] = (h1_pb4 == frozen_h1_slot0)
            row["sha_match_frozen_base_gradient"] = (sha == FROZEN_BASE_GRADIENT_SHA)
            canary_pass = canary_pass and row["eq_frozen_word_literal"] and row["sha_match_frozen_base_gradient"]
        canary_pass = canary_pass and is_identity
        canary_rows.append(row)

    print(f"[{time.strftime('%H:%M:%S')}] CANARY (m=0, all 5 cofaces, closedform_v2): "
          f"pass={canary_pass} rows={canary_rows}", flush=True)

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "construction_source": "search/koubou158_m2_closedform_v2.py -- "
                              "h1(m)=pp[y^m++f_xy, x^m++Inv(f_xz), z^m++f_yz], z=(yx)^-1, "
                              "sigma-free, no GAP/Reidemeister-Schreier",
        "theta_hexagon_defect_diagnosis_note": (
            "v3's predecessor cert (search/certs/koubou158_M2_msweep_v3_20260822.json, "
            "status=CANARY_ALL_FAIL_STOPPED) found a 14-nonzero-term residual in its closest "
            "candidate, caused by treating the frozen row's 'Inv(f_xz)' leaf as f(z,x) "
            "(argument-swapped substitution) instead of literally inv_word(f(x,z)) (word-"
            "inverse). Those two differ by exactly the theta-hexagon acceptance-condition "
            "gradient (f(v,u)=f(u,v)^-1), which lies outside im(D2bar) by construction -- using "
            "it to build the target would have been circular (testing the acceptance condition "
            "against itself). This v2 closed-form module fixes that: Inv(f_xz):=inv_word(f_xz) "
            "literally, never f(z,x)."
        ),
        "canary": {
            "required": True,
            "description": "m=0 must reproduce the frozen target6.base_gradient EXACTLY -- both "
                          "byte-identical source word (slot 0) AND SHA match -- by construction, "
                          "not merely by value-equality (the v2/theta-hexagon lesson).",
            "frozen_reference": {"entry_count": FROZEN_ENTRY_COUNT, "sha256": FROZEN_BASE_GRADIENT_SHA},
            "rows": canary_rows,
            "pass": canary_pass,
        },
        "input_provenance": {
            "q3_chief_receipt": {"path": str(Q3_CHIEF).replace("\\", "/"),
                                 "sha256": Q3_CHIEF_SHA, "bytes": Q3_CHIEF_BYTES},
        },
        "six_point_universe": {
            "value": SIX_POINT_UNIVERSE,
            "derivation": "charming condition u1=2*m1+1 in (Z/18)^x (L_ord=18, measured directly, "
                          "koubou158_M2_msweep_v1 cert) is equivalent to m1 in {0,2,3,5,6,8} (mod 9); "
                          "this 6-point set is an OVER-approximation, safe in the NO direction, "
                          "recorded here 'mod M1' -- i.e. explicitly INDEPENDENT of and not "
                          "requiring resolution of the separately-unresolved M1 subgroup / M_ord "
                          "(see search/certs/koubou158_M1M2_findex_v1_20260822.json, a DIFFERENT, "
                          "still-open question not addressed by this measurement).",
            "m1_equals_0_status": "already settled -- search/certs/"
                                  "koubou158_L3_radical_v1_1_20260822.json (settled_no=true, "
                                  "j_star=4), referenced as C-12/C-13.",
            "pentagon_row_note": "pentagon row is m-invariant; not re-tested.",
            "remaining_universe": REMAINING_M1,
        },
    }

    if not canary_pass:
        result["verdict"] = "CANARY_FAILED"
        today = date.today().isoformat().replace("-", "")
        out_path = ROOT / "search" / "certs" / f"koubou158_M2_msweep_v3_measurement_{today}.json"
        text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        core.require(out_path.read_text(encoding="utf-8") == text, "checked-write readback mismatch")
        print(f"CANARY FAILED -- wrote {out_path}", flush=True)
        return 1

    # ---- preflight per m1: value_is_identity across all 5 cofaces ----
    preflight: dict[int, dict] = {}
    hex1_coface_0_word_by_m1: dict[int, list[int]] = {}
    nabla_b_pi_by_m1: dict[int, dict] = {}
    for m1 in REMAINING_M1:
        Hm = cf2.build_h1(m1)
        rows = []
        all_identity = True
        for slot in range(5):
            h1_pb4 = cf2.push_through_coface(Hm, cofaces_3_4[slot])
            val = e4.eval(h1_pb4)
            is_identity = val == e4.identity
            rows.append({"slot": slot, "word_len": len(h1_pb4), "value_is_identity": is_identity})
            all_identity = all_identity and is_identity
            if slot == 0:
                hex1_coface_0_word_by_m1[m1] = h1_pb4
        preflight[m1] = {"all_5_cofaces_value_is_identity": all_identity, "rows": rows}
        core.require(all_identity, f"157m2v3: preflight FAILED for m1={m1} -- not a valid hexagon relator family member")
        nabla_b_E4 = core.fox_gradient(e4, hex1_coface_0_word_by_m1[m1])
        nabla_b_pi_by_m1[m1] = core.project_to_pi(nabla_b_E4)

    print(f"[{time.strftime('%H:%M:%S')}] preflight PASSED for all m1 in {REMAINING_M1}; "
          f"nabla_b(m1) constructed ({time.perf_counter() - t_start:.1f}s elapsed)", flush=True)

    result["preflight"] = {str(m1): preflight[m1] for m1 in REMAINING_M1}

    # ---- weight structure sanity (unchanged from v1/v2) ----
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

    # ---- main m1-sweep: complete-BFS core, depth-satisfied acceptance ----
    per_m1_progression: dict[int, list[dict]] = {m1: [] for m1 in REMAINING_M1}
    per_m1_outcome: dict[int, dict] = {m1: {"status": "PENDING"} for m1 in REMAINING_M1}
    remaining = set(REMAINING_M1)

    for j in range(2, J_MAX + 1):
        if not remaining:
            break
        t_j = time.perf_counter()
        try:
            ech_combined, idx, sp, info = cbfs.build_V_and_D2bar_from_q3_complete(e4, q3, j)
        except RuntimeError as exc:
            print(f"[{time.strftime('%H:%M:%S')}] j={j}: ABORTED -- {exc}", flush=True)
            for m1 in list(remaining):
                per_m1_outcome[m1] = {"status": "ABORTED_RESOURCE_CAP", "at_j": j, "error": str(exc)}
            remaining.clear()
            break
        elapsed_build = time.perf_counter() - t_j

        for m1 in list(remaining):
            target_proj = core.project_vec_to_Ij(nabla_b_pi_by_m1[m1], j)
            target_indexed = {idx[k]: c for k, c in target_proj.items() if k in idx}
            tv = sp.vec(target_indexed)
            ech_clone = ech_combined.clone()
            _, pivot = ech_clone.reduce(tv)
            non_member = pivot >= 0
            entry = {
                "j": j, "dim_Lambda_over_Ij": info["dim_Lambda_over_Ij"],
                "rank_V": info["rank_V"], "rank_V_plus_D2bar_combined": info["rank_V_plus_D2bar_combined"],
                "depth_requirement_satisfied": info["depth_requirement_satisfied"],
                "min_depth_reached_across_relators": info["min_depth_reached_across_relators"],
                "total_vectors_explored": info["total_vectors_explored"],
                "non_member": non_member,
            }
            per_m1_progression[m1].append(entry)
            if non_member and info["depth_requirement_satisfied"]:
                per_m1_outcome[m1] = {"status": "SETTLED_NO_DEPTH_TRUSTWORTHY", "j_star": j}
                remaining.discard(m1)
            elif non_member and not info["depth_requirement_satisfied"]:
                print(f"[{time.strftime('%H:%M:%S')}] j={j} m1={m1}: non_member=True but depth "
                      f"NOT satisfied -- continuing to next j (not accepting this NO)", flush=True)

        elapsed_j = time.perf_counter() - t_j
        print(f"[{time.strftime('%H:%M:%S')}] j={j}: dim(Lambda/I^j)={info['dim_Lambda_over_Ij']} "
              f"build={elapsed_build:.1f}s total={elapsed_j:.1f}s remaining_m1={sorted(remaining)} "
              f"outcomes_so_far={ {k: v['status'] for k, v in per_m1_outcome.items()} }", flush=True)

    for m1 in REMAINING_M1:
        if per_m1_outcome[m1]["status"] == "PENDING":
            per_m1_outcome[m1] = {"status": "J_MAX_EXHAUSTED_INCONCLUSIVE", "j_max": J_MAX}

    elapsed = time.perf_counter() - t_start

    verdicts = {}
    for m1 in REMAINING_M1:
        verdicts[str(m1)] = {
            "outcome": per_m1_outcome[m1],
            "hexagon_1_coface_0_word_length": len(hex1_coface_0_word_by_m1[m1]),
            "j_progression": per_m1_progression[m1],
        }

    all_settled_trustworthy = all(v["outcome"]["status"] == "SETTLED_NO_DEPTH_TRUSTWORTHY"
                                  for v in verdicts.values())
    any_aborted = any(v["outcome"]["status"] == "ABORTED_RESOURCE_CAP" for v in verdicts.values())
    any_inconclusive = any(v["outcome"]["status"] == "J_MAX_EXHAUSTED_INCONCLUSIVE"
                           for v in verdicts.values())

    if all_settled_trustworthy:
        top_verdict = "ALL_FIVE_SETTLED_NO_DEPTH_TRUSTWORTHY_M_DIRECTION_CLOSED"
    elif any_aborted:
        top_verdict = "RESOURCE_CAP_ABORTED_SEE_PER_M1_OUTCOME"
    elif any_inconclusive:
        top_verdict = "J_MAX_EXHAUSTED_INCONCLUSIVE_SEE_PER_M1_OUTCOME"
    else:
        top_verdict = "MIXED_SEE_PER_M1_OUTCOME"

    result["verdict"] = top_verdict
    result["m1_verdicts"] = verdicts
    result["all_five_settled_no_depth_trustworthy"] = all_settled_trustworthy
    result["m1_equals_0_reference"] = {
        "cert": "search/certs/koubou158_L3_radical_v1_1_20260822.json",
        "settled_no": True, "j_star": 4,
    }
    result["grade"] = ("candidate, single-system producer measurement (own IndependentPc/E4, own "
                       "Jennings/radical-filtration code); m=0 canary PASSED byte-exact (not "
                       "merely value-equal) against the frozen target6.base_gradient; complete-BFS "
                       "depth-fix engine independently selftested; no independent SECOND-SYSTEM "
                       "computational cross-check of this m-sweep has been run yet")
    result["wall_clock_seconds"] = elapsed

    today = date.today().isoformat().replace("-", "")
    out_path = ROOT / "search" / "certs" / f"koubou158_M2_msweep_v3_measurement_{today}.json"
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    readback = out_path.read_text(encoding="utf-8")
    core.require(readback == text, "checked-write readback mismatch")

    print(f"KOUBOU158_M2_MSWEEP_V3 verdict={top_verdict} "
          f"outcomes={ {k: v['status'] for k, v in per_m1_outcome.items()} } "
          f"elapsed_s={elapsed:.2f} output={out_path.as_posix()}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
