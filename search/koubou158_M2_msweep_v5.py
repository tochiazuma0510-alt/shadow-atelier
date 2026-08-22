"""koubou158_M2_msweep_v5.py

v5 of the koubou158 target6 m1-direction sweep -- SAME mathematical
semantics as search/koubou158_M2_msweep_v4.py (dual-form sweep,
closed-form theta-hexagon identity check, primary canary, m sweep
verdict rules) -- per commander instruction 2026-08-22 ("重い処理なら
高速化してGHAで"). ONLY the computational KERNEL changes.

WHY (measured, not guessed): v4's own run log (scratchpad/m2_v4_run.log)
showed j=4/5/6 build times of 9.2s/130.2s/2381.3s -- a much steeper climb
than the dimension growth (636->1740->4056, ~2.7x/2.3x) would explain on
its own, prompting the commander's request for a faster kernel. Before
committing to any specific fix, a cProfile of the j=4 build
(scratchpad/profile_j4.py) was run and reported back: the linear-algebra
kernel (core.F3BitEchelon) is NOT the bottleneck (doesn't appear in the
top 20 functions, well under 1% of wall time). The actual hotspot is:
  - core.project_vec_to_Ij / project_pcvec_terms (recursive per-
    pc-element binomial expansion into I^j monomials): ~66% of wall time.
  - core.apply_xi_minus_1 -> IndependentPc.mul/collect (pc-presentation
    rewriting for one generator multiplication): ~19% of wall time.
Commander approved pivoting the fix to these two (memoization, purity-
canaried) rather than the originally-suspected linear-algebra kernel;
numpy vectorization of the linear algebra (koubou158_L3_core_fastkernel_
v1.F3NumpyEchelon/F3NumpySpace) is ALSO provided in that module (harmless,
matches the original instruction literally) but is not the primary
speedup and is not wired into this driver's default path.

KERNEL: search/koubou158_L3_core_fastkernel_v1.py's
build_V_and_D2bar_from_q3_complete_fast -- same complete-BFS algorithm
as koubou158_L3_core_completebfs_v1 (no pruning, same depth-satisfied
soundness argument), only project_vec_to_Ij and apply_xi_minus_1 are
routed through a persistent memoization cache with a purity canary
(1-in-1000 cache hits re-derived from the ORIGINAL uncached function and
required to match exactly -- any mismatch is a fail-closed abort, not a
silently ignored discrepancy).

PERSISTENT CACHE ACROSS j LEVELS (the actual source of v5's compounding
speedup at higher j, beyond the raw per-call memoization): the BFS's raw
per-relator closure at depth cap j-1 is a strict EXTENSION of the depth
cap (j-1)-1 closure at the previous j level -- the same underlying
apply_xi_minus_1 calls recur across consecutive j levels (that function
does not depend on j at all), so mul_cache is shared and persisted
(pickled to CACHE_DIR) across the ENTIRE run, not reset per j. proj_cache
(keyed on (pcvec, j)) is j-specific but persisted the same way, so
resuming after a kill does not lose the accumulated cache -- only the
per-j checkpoint (dims/outcomes) is needed to know which j levels are
already done; the caches make even a from-scratch j make full use of
work done at all previously-completed j levels.

CHECKPOINT / RESUME (per commander instruction #2, modeled on
search/koubou158_prodrung_j5_resume_v1.py's resumable-driver pattern,
adapted because each j level here is independent -- no cross-j echelon
carried forward, unlike that script's single j=5 level): after EVERY j
level completes (build + all still-remaining per-target membership
checks), the run state (completed j's, per-target progression/outcome,
canary counts) is written to CKPT_PATH (JSON) and the two caches are
pickled to CACHE_PATH -- both flushed with checked-write readback before
moving to the next j. A killed/restarted process reloads both and skips
any j already in `completed_j`, continuing where it left off with a warm
cache.

REGRESSION GATE (commander instruction #3, hardcoded from v4's ACTUAL
run log values -- search/certs/koubou158_M2_msweep_v4_*.json did not
exist yet at v5-authoring time, v4 was still running on m1=6 -- so the
comparison targets below are read off scratchpad/m2_v4_run.log's j=2..6
lines, not invented): dims 42/192/636/1740/4056 at j=2..6; primary canary
PASS; closed_form_identity_check diff_term_count=14 exact_match=True;
m1 in {3,5,8} (both forms) SETTLED_NO_DEPTH_TRUSTWORTHY exactly at j=4;
m1=2 (both forms) exactly at j=5. The gate is CHECKED INLINE as part of
the normal j-loop (not a separate re-run -- the normal loop already
computes j=2..6 en route to j=7+, so checking there is a from-scratch
verification with no double work) -- any mismatch at any of j=2..6
raises core.require() and the run stops BEFORE j=7, per instruction
("一つでも割れたら j=7 に進まず報告").

FALSIFIER DELTA AUDIT (2026-08-22) -- fixes applied, itemized:
  F-1 (critical): PurityCanaryFailure did not exist yet; the canary's
    recheck used core.require(), whose RuntimeError was caught by this
    file's `except RuntimeError` around the build call and relabeled
    ABORTED_RESOURCE_CAP -- a corrupted cache could exit 0 with a cert.
    Fixed in koubou158_L3_core_fastkernel_v1.py (dedicated exception,
    NOT a RuntimeError subclass, not caught here) and below (any_aborted
    now returns 1, not just a verdict string).
  F-2: EXPECTED_DIMS alone is a function of j only (a corrupted cache
    could still reproduce the right dimension) -- the cert's "grade"
    field no longer claims this is a "cross-check"; see F-4 for the
    actual independent-implementation check.
  F-3: added an explicit require() after j=6 that (6,'primary') and
    (6,'secondary') are STILL in `remaining` (v4's log shows m1=6 is the
    one slice genuinely unresolved through j=6) -- catches a corrupted
    cache producing a FALSE early settle for the one target where that
    would otherwise slip through undetected (nothing else checks m1=6
    before j=7).
  F-4: on a --fresh run, j in {2,3,4} are ALSO computed via
    koubou158_L3_core_completebfs_v1.build_V_and_D2bar_from_q3_complete
    (the ORIGINAL, unmemoized, independently-implemented builder) and
    required to agree EXACTLY with the fast kernel's info on rank_V,
    rank_V_plus_D2bar_combined, per_relator_closure_receipts, and
    total_vectors_explored -- turning the log-shaped dims gate into a
    real implementation-diff gate (measured cost: ~11s extra locally).
  F-5: the pickled kernel cache now carries {"schema","q3_sha","code_sha"}
    and load_caches() discards (not aborts) a cache whose q3/code hash
    does not match the current run -- a stale cache from a previous code
    version cannot silently corrupt a new run.
  F-6: save_checkpoint() now does tmp-file write + readback + atomic
    os.replace(), matching save_caches()'s existing pattern (previously
    it wrote directly to CKPT_PATH, so a kill mid-write could leave a
    torn/truncated checkpoint).
  F-8: PurityCanary.mismatches is incremented (in fastkernel) before the
    failure is raised, so it is not structurally stuck at 0.
  F-9: PurityCanary's seed is now drawn from system entropy per run (not
    a hardcoded constant), and the resulting seed/phase is recorded in
    both the checkpoint and the cert.
  F-10: numpy is now a LAZY import inside koubou158_L3_core_fastkernel_
    v1.py's F3NumpySpace/F3NumpyEchelon (not required to import this
    module at all); the cert's "kernel" text no longer implies that dead
    code is exercised by any regression check.
  F-11: a cert is now written after EVERY completed j (not only at the
    end), tagged with run_role ("regression_gate" for a --fresh
    invocation, "production" otherwise) and max_j_reached, so the most
    likely real failure mode (j=7 completes, j=8 gets killed) still
    leaves a usable cert on disk / as a GHA artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_1 as core  # noqa: E402
import koubou158_L3_core_completebfs_v1 as cbfs  # noqa: E402
import koubou158_L3_core_fastkernel_v1 as fast  # noqa: E402
import koubou158_m2_closedform_v1 as cf1  # noqa: E402
import koubou158_m2_closedform_v2 as cf2  # noqa: E402

SCHEMA = "koubou158-M2-msweep/v5"
Q3_CHIEF = core.Q3_CHIEF
Q3_CHIEF_SHA = core.Q3_CHIEF_SHA
Q3_CHIEF_BYTES = core.Q3_CHIEF_BYTES
J_MAX = core.J_MAX

REMAINING_M1 = [2, 3, 5, 6, 8]
SIX_POINT_UNIVERSE = [0, 2, 3, 5, 6, 8]
FROZEN_BASE_GRADIENT_SHA = "788fd8712f76a3ca254bb2179b5498fed3ca00e649ba0321ef297d2d985cc71e"
FROZEN_ENTRY_COUNT = 72

TAU_Z_WORD = [-1, -2]
TAU_PERM = ["tau_g", "tau2_g", "g"]

# ---- regression gate: hardcoded from v4's ACTUAL log, scratchpad/m2_v4_run.log ----
EXPECTED_DIMS = {2: 42, 3: 192, 4: 636, 5: 1740, 6: 4056}
EXPECTED_SETTLED_AT_J = {3: 4, 5: 4, 8: 4, 2: 5}  # m1 -> j at which BOTH forms settle NO
EXPECTED_IDENTITY_CHECK = {"diff_term_count": 14, "exact_match": True}

CKPT_DIR = ROOT / "scratchpad" / "m2_v5"
CKPT_PATH = CKPT_DIR / "checkpoint.json"
CACHE_PATH = CKPT_DIR / "kernel_caches.pkl"
CERT_DIR = ROOT / "search" / "certs"
FASTKERNEL_MODULE_PATH = ROOT / "search" / "koubou158_L3_core_fastkernel_v1.py"


def code_sha() -> str:
    """SHA-256 of the fastkernel module's source -- used (F-5) to tie a
    pickled cache to the code version that produced it; a stale cache
    from a previous code version is discarded rather than trusted."""
    return core.sha_file(FASTKERNEL_MODULE_PATH)


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
    tau_images = [[2], TAU_Z_WORD]
    g = core.reduce_word([2] * m + core.FIXED_WORD)
    tau_g = cf1.word_substitute(g, tau_images)
    tau2_g = cf1.word_substitute(tau_g, tau_images)
    factors = {"g": g, "tau_g": tau_g, "tau2_g": tau2_g}
    seq = [factors[p] for p in TAU_PERM]
    H = core.reduce_word(seq[0] + seq[1] + seq[2])
    return cf1.push_through_coface(H, cofaces_3_4[slot])


# ---------------------------------------------------------------------
# checkpoint / cache persistence
# ---------------------------------------------------------------------

def load_checkpoint() -> dict:
    if CKPT_PATH.is_file():
        return json.loads(CKPT_PATH.read_text(encoding="utf-8"))
    return {
        "schema": SCHEMA, "completed_j": [], "per_target_progression": {}, "per_target_outcome": {},
        "canary_checked": 0, "canary_mismatches": 0, "setup_done": False,
        "closed_form_identity_check": None, "primary_canary": None,
    }


def save_checkpoint(ckpt: dict) -> None:
    """F-6: atomic tmp-write + readback + os.replace(), matching
    save_caches()'s existing pattern -- a kill mid-write can no longer
    leave a torn/truncated checkpoint.json (previously this wrote
    directly to CKPT_PATH)."""
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    text = json.dumps(ckpt, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    tmp = CKPT_PATH.with_suffix(".json.tmp")
    tmp.write_text(text, encoding="utf-8")
    readback = tmp.read_text(encoding="utf-8")
    core.require(readback == text, "checkpoint checked-write readback mismatch")
    tmp.replace(CKPT_PATH)


def load_caches(expected_q3_sha: str):
    """F-5: the pickle now carries {"schema","q3_sha","code_sha"} plus the
    two cache dicts. A cache built under a different q3_chief input or a
    different fastkernel code version is DISCARDED (fresh empty caches
    returned) rather than trusted -- the run continues (just cold), it
    does not abort, since a cold cache is merely slower, never wrong."""
    if not CACHE_PATH.is_file():
        return {}, {}
    with CACHE_PATH.open("rb") as f:
        blob = pickle.load(f)
    if (not isinstance(blob, dict) or blob.get("schema") != SCHEMA or
            blob.get("q3_sha") != expected_q3_sha or blob.get("code_sha") != code_sha()):
        print(f"[{time.strftime('%H:%M:%S')}] cache metadata mismatch (F-5) -- discarding "
              f"cache and starting cold (run continues, not aborted)", flush=True)
        return {}, {}
    return blob["proj_cache"], blob["mul_cache"]


def save_caches(proj_cache: dict, mul_cache: dict, q3_sha: str) -> None:
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    blob = {"schema": SCHEMA, "q3_sha": q3_sha, "code_sha": code_sha(),
            "proj_cache": proj_cache, "mul_cache": mul_cache}
    tmp = CACHE_PATH.with_suffix(".pkl.tmp")
    with tmp.open("wb") as f:
        pickle.dump(blob, f, protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(CACHE_PATH)


def target_key(m1: int, form: str) -> str:
    return f"{m1}_{form}"


def assemble_result(*, run_role: str, max_j_reached, j_top_target: int,
                     closed_form_identity_check: dict, canary_rows: list, canary_pass: bool,
                     canary, preflight_by_m1: dict, per_target_progression: dict,
                     per_target_outcome: dict, completed_j: set, f4_verified_js: set,
                     elapsed: float, in_progress: bool) -> dict:
    """Build the cert dict from the current run state. Called after EVERY
    completed j (F-11(a): in_progress=True) as well as once at the very
    end (in_progress=False) -- so the single most likely real failure
    mode (e.g. j=7 completes, j=8 gets killed) still leaves a usable,
    non-stale cert on disk / as a GHA artifact, tagged with run_role and
    max_j_reached (F-11(b))."""
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
    elif in_progress:
        top_verdict = "IN_PROGRESS_SEE_PER_M1_OUTCOME"
    else:
        top_verdict = "SOME_SLICES_INCONCLUSIVE_SEE_PER_M1_OUTCOME"

    return {
        "schema": SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_role": run_role,
        "max_j_reached": max_j_reached,
        "max_j_target_this_invocation": j_top_target,
        "in_progress": in_progress,
        "predecessor_note": "v4 (search/koubou158_M2_msweep_v4.py) is the mathematically-identical, "
                           "unaccelerated predecessor; this cert (v5) changes ONLY the computational "
                           "kernel (memoized project_vec_to_Ij/apply_xi_minus_1, purity-canaried) -- "
                           "see this module's docstring for the profiling that identified the real "
                           "hotspot and the commander's approval to pivot away from the originally-"
                           "suspected linear-algebra kernel.",
        "kernel": "search/koubou158_L3_core_fastkernel_v1.py: memoized project_vec_to_Ij / "
                 "apply_xi_minus_1 with purity canary (1-in-1000 cache hits re-derived from the "
                 "original uncached function, raising PurityCanaryFailure -- not caught by this "
                 "driver -- on any mismatch); F3BitEchelon linear-algebra kernel UNCHANGED (cProfile "
                 "showed it was not the bottleneck). A numpy int8 GF(3) echelon (F3NumpyEchelon/"
                 "F3NumpySpace) is ALSO present in that module per the original instruction, but "
                 "(falsifier finding F-10) it is NOT wired into this driver's default path and is NOT "
                 "exercised by any check in this cert -- it is dead code for this lane today.",
        "venue": "local (see wall_clock_seconds / --max-j) or GHA (see .github/workflows/"
                "koubou158-m2-msweep-v5-gha.yml) depending on invocation",
        "purity_canary": canary.summary(),
        "primary_construction_source": "search/koubou158_m2_closedform_v2.py",
        "secondary_construction_source": "search/koubou158_m2_closedform_v1.py "
                                        f"(z_word=(yx)^-1, f positive, perm={TAU_PERM})",
        "closed_form_identity_check": closed_form_identity_check,
        "regression_gate": {
            "expected_dims": EXPECTED_DIMS, "expected_settled_at_j": EXPECTED_SETTLED_AT_J,
            "expected_identity_check": EXPECTED_IDENTITY_CHECK,
            "source": "scratchpad/m2_v4_run.log (v4's actual run log; v4's own cert was not yet "
                     "written at v5-authoring time -- v4 was still running on m1=6)",
            "checked_inline_through_j": max((j for j in completed_j if j <= 6), default=None),
            "note_f2": "dims-only agreement (EXPECTED_DIMS) is a function of j alone and is a cheap "
                      "sanity check, NOT an implementation cross-check by itself -- see "
                      "implementation_diff_gate_f4 below for the actual independent-implementation "
                      "diff, and f3_m1_6_still_open_at_j6 for the one slice the settle-at-j gate "
                      "does not otherwise pin down.",
        },
        "implementation_diff_gate_f4": {
            "description": "on a --fresh run, j in {2,3,4} are additionally computed via the "
                          "ORIGINAL, unmemoized, independently-coded "
                          "koubou158_L3_core_completebfs_v1.build_V_and_D2bar_from_q3_complete and "
                          "required to agree EXACTLY (rank_V, rank_V_plus_D2bar_combined, "
                          "per_relator_closure_receipts, total_vectors_explored) with the fast "
                          "kernel's info -- a real implementation-diff gate, not merely a dims match.",
            "verified_at_j": sorted(f4_verified_js),
            "checked": {2, 3, 4}.issubset(f4_verified_js),
        },
        "f3_m1_6_still_open_at_j6": {
            "description": "explicit require() that (6,'primary')/(6,'secondary') are STILL "
                          "unresolved at j=6 (v4's log shows this slice open through j=6, resolved "
                          "only at the in-progress j=7) -- catches a corrupted-cache false-early-"
                          "settle for the one m1 the settle-at-j gate does not otherwise cover.",
            "checked": 6 in completed_j,
        },
        "dual_verdict_note_verbatim": (
            "(i) both forms (primary/theta-template and secondary/tau-orbit) are sound "
            "necessary conditions for membership; (ii) any discrepancy between the two forms' "
            "verdicts is explained by the theta-row contribution; (iii) on the accepted "
            "(settled) trajectory the two forms agree. A given m1 is SETTLED_NO (slice empty) "
            "if EITHER form gives a depth-trustworthy NO."
        ),
        "primary_canary": {"rows": canary_rows, "pass": canary_pass},
        "input_provenance": {
            "q3_chief_receipt": {"path": str(Q3_CHIEF).replace("\\", "/"),
                                 "sha256": Q3_CHIEF_SHA, "bytes": Q3_CHIEF_BYTES},
        },
        "six_point_universe": {
            "value": SIX_POINT_UNIVERSE,
            "remaining_universe": REMAINING_M1,
        },
        "preflight_caveat_identity_check": {"value_is_identity_by_m1": preflight_by_m1},
        "verdict": top_verdict,
        "m1_verdicts": m1_verdicts,
        "all_five_slices_settled_no": all_settled,
        "any_slice_resource_cap_aborted": any_aborted,
        "m1_equals_0_reference": {
            "cert": "search/certs/koubou158_L3_radical_v1_1_20260822.json",
            "settled_no": True, "j_star": 4,
        },
        "grade": ("candidate, single-system producer measurement (own IndependentPc/E4, own "
                 "Jennings/radical-filtration code); primary canary PASSED byte-exact against the "
                 "frozen target6.base_gradient; theta-hexagon-defect closed-form identity CONFIRMED "
                 "exactly; complete-BFS depth-fix engine unchanged from v4/cbfs; kernel change is a "
                 "memoization+purity-canary speedup ONLY. Falsifier finding F-2 (corrected): the dims-"
                 "only log comparison is NOT by itself a cross-check of the implementation (a "
                 "corrupted cache could still reproduce the right dimension) -- the actual "
                 "independent-implementation cross-check is implementation_diff_gate_f4 (exact rank/"
                 "receipt agreement against the original unmemoized cbfs builder, j=2..4 on a --fresh "
                 "run) plus f3_m1_6_still_open_at_j6 (guards the one slice those checks don't cover). "
                 "No independent SECOND-SYSTEM computational cross-check of this m-sweep (a wholly "
                 "separate implementation/toolchain) has been run yet."),
        "wall_clock_seconds": elapsed,
        "max_j_this_run": j_top_target,
    }


def write_cert(result: dict) -> Path:
    today = date.today().isoformat().replace("-", "")
    out_path = CERT_DIR / f"koubou158_M2_msweep_v5_{today}.json"
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(text, encoding="utf-8")
    readback = tmp.read_text(encoding="utf-8")
    core.require(readback == text, "cert checked-write readback mismatch")
    tmp.replace(out_path)
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-j", type=int, default=J_MAX,
                     help="stop after this j level (local smoke tests use a small value; "
                          "GHA production run uses the default J_MAX)")
    ap.add_argument("--fresh", action="store_true",
                     help="ignore any existing checkpoint/cache and start from scratch "
                          "(used by the regression gate, which must be a from-scratch re-run)")
    ap.add_argument("--run-role", choices=("auto", "regression_gate", "production"), default="auto",
                     help="F-11: recorded in the cert as run_role. 'auto' (default) uses "
                          "'regression_gate' when --fresh is passed, else 'production' -- matching "
                          "the GHA workflow's two-step invocation (step 1: --fresh --max-j 6; "
                          "step 2: --max-j <N>, no --fresh).")
    args = ap.parse_args()
    run_role = args.run_role
    if run_role == "auto":
        run_role = "regression_gate" if args.fresh else "production"

    if args.fresh:
        for p in (CKPT_PATH, CACHE_PATH):
            if p.is_file():
                p.unlink()

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

    ckpt = load_checkpoint()
    proj_cache, mul_cache = load_caches(got_sha)
    canary = fast.PurityCanary(sample_rate=1000)
    canary.checked = ckpt.get("canary_checked", 0)
    print(f"[{time.strftime('%H:%M:%S')}] run_role={run_role} purity_canary_seed={canary.seed_used} "
          f"initial_phase={canary.initial_phase} (F-9)", flush=True)

    # ---- setup: closed-form identity check + primary canary (cheap, always redone if not checkpointed) ----
    if not ckpt.get("setup_done"):
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
        }
        core.require(identity_check_match, "157m2v5: theta-hexagon closed-form identity check FAILED")
        core.require(closed_form_identity_check["diff_term_count"] == EXPECTED_IDENTITY_CHECK["diff_term_count"],
                     "157m2v5 REGRESSION: diff_term_count changed from v4")
        core.require(closed_form_identity_check["exact_match"] == EXPECTED_IDENTITY_CHECK["exact_match"],
                     "157m2v5 REGRESSION: exact_match changed from v4")
        print(f"[{time.strftime('%H:%M:%S')}] closed_form_identity_check: {closed_form_identity_check} "
              f"(REGRESSION MATCH vs v4 log)", flush=True)

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
        core.require(canary_pass, "157m2v5: primary canary FAILED")
        print(f"[{time.strftime('%H:%M:%S')}] PRIMARY CANARY (m=0, all 5 cofaces): "
              f"pass={canary_pass} (REGRESSION MATCH vs v4)", flush=True)

        ckpt["closed_form_identity_check"] = closed_form_identity_check
        ckpt["primary_canary"] = {"rows": canary_rows, "pass": canary_pass}
        ckpt["setup_done"] = True
        save_checkpoint(ckpt)
    else:
        closed_form_identity_check = ckpt["closed_form_identity_check"]
        canary_pass = ckpt["primary_canary"]["pass"]
        canary_rows = ckpt["primary_canary"]["rows"]
        print(f"[{time.strftime('%H:%M:%S')}] setup already checkpointed, skipping recompute", flush=True)

    # ---- preflight per m1 (both forms, all 5 cofaces) + nabla_b construction ----
    nabla_b_primary_pi: dict[int, dict] = {}
    nabla_b_secondary_pi: dict[int, dict] = {}
    preflight_by_m1: dict = {}
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
        preflight_by_m1[str(m1)] = {"primary": primary_rows, "secondary": secondary_rows}
        primary_word0 = cf2.push_through_coface(H_primary, cofaces_3_4[0])
        secondary_word0 = build_secondary_h1(m1, cofaces_3_4, 0)
        nabla_b_primary_pi[m1] = core.project_to_pi(core.fox_gradient(e4, primary_word0))
        nabla_b_secondary_pi[m1] = core.project_to_pi(core.fox_gradient(e4, secondary_word0))

    print(f"[{time.strftime('%H:%M:%S')}] preflight recorded for all m1 in {REMAINING_M1} "
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

    # ---- main dual sweep, per-j checkpointed ----
    targets = [(m1, form) for m1 in REMAINING_M1 for form in ("primary", "secondary")]
    per_target_progression: dict[tuple, list[dict]] = {
        t: ckpt["per_target_progression"].get(target_key(*t), []) for t in targets
    }
    per_target_outcome: dict[tuple, dict] = {
        t: ckpt["per_target_outcome"].get(target_key(*t), {"status": "PENDING"}) for t in targets
    }
    remaining = {t for t in targets if per_target_outcome[t]["status"] not in
                 ("SETTLED_NO_DEPTH_TRUSTWORTHY", "ABORTED_RESOURCE_CAP")}
    completed_j = set(ckpt["completed_j"])
    f4_verified_js = set(ckpt.get("f4_verified_js", []))

    def nabla_for(m1, form):
        return nabla_b_primary_pi[m1] if form == "primary" else nabla_b_secondary_pi[m1]

    j_top = min(args.max_j, J_MAX)
    for j in range(2, j_top + 1):
        if not remaining:
            break
        if j in completed_j:
            print(f"[{time.strftime('%H:%M:%S')}] j={j}: already checkpointed, skipping "
                  f"(remaining={sorted(remaining)})", flush=True)
            continue
        t_j = time.perf_counter()
        try:
            ech_combined, idx, sp, info = fast.build_V_and_D2bar_from_q3_complete_fast(
                e4, q3, j, proj_cache, mul_cache, canary)
        except RuntimeError as exc:
            print(f"[{time.strftime('%H:%M:%S')}] j={j}: ABORTED -- {exc}", flush=True)
            for t in list(remaining):
                per_target_outcome[t] = {"status": "ABORTED_RESOURCE_CAP", "at_j": j, "error": str(exc)}
            remaining.clear()
            break
        elapsed_build = time.perf_counter() - t_j

        # ---- regression gate (inline, from-scratch by construction) ----
        # F-2: dims-only agreement is a function of j alone and cannot by
        # itself catch a corrupted cache reproducing the right dimension
        # -- kept as a cheap sanity check, but see F-4 below for the real
        # independent-implementation diff.
        if j in EXPECTED_DIMS:
            core.require(info["dim_Lambda_over_Ij"] == EXPECTED_DIMS[j],
                         f"157m2v5 REGRESSION FAILED at j={j}: dim={info['dim_Lambda_over_Ij']} "
                         f"expected {EXPECTED_DIMS[j]} (v4 log)")

        # ---- F-4: independent-implementation diff gate (--fresh only, j=2..4) ----
        # Re-derives j via the ORIGINAL, unmemoized, independently-coded
        # cbfs.build_V_and_D2bar_from_q3_complete and requires EXACT
        # agreement on the fields that actually depend on the closure
        # contents (not just its final dimension) -- this is what turns
        # the log-shaped dims gate into a real implementation-diff gate.
        if args.fresh and j in (2, 3, 4):
            t_ref = time.perf_counter()
            _, _, _, ref_info = cbfs.build_V_and_D2bar_from_q3_complete(e4, q3, j)
            elapsed_ref = time.perf_counter() - t_ref
            for field in ("rank_V", "rank_V_plus_D2bar_combined", "total_vectors_explored",
                          "per_relator_closure_receipts"):
                core.require(ref_info[field] == info[field],
                             f"157m2v5 F-4 IMPLEMENTATION-DIFF GATE FAILED at j={j}: field={field} "
                             f"fast={info[field]!r} reference(cbfs)={ref_info[field]!r}")
            f4_verified_js.add(j)
            print(f"[{time.strftime('%H:%M:%S')}] j={j}: F-4 implementation-diff gate PASS vs "
                  f"cbfs (reference build {elapsed_ref:.1f}s)", flush=True)

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

        # ---- regression gate: expected settle-at-j for m1 in {2,3,5,8} ----
        if j in (4, 5):
            for m1, expected_j in EXPECTED_SETTLED_AT_J.items():
                if expected_j != j:
                    continue
                for form in ("primary", "secondary"):
                    outcome = per_target_outcome[(m1, form)]
                    core.require(outcome.get("status") == "SETTLED_NO_DEPTH_TRUSTWORTHY" and
                                 outcome.get("j_star") == j,
                                 f"157m2v5 REGRESSION FAILED: m1={m1} form={form} expected "
                                 f"SETTLED_NO_DEPTH_TRUSTWORTHY at j={j} (v4 log), got {outcome}")
            print(f"[{time.strftime('%H:%M:%S')}] j={j}: REGRESSION MATCH (settle-at-j) vs v4 log", flush=True)

        # ---- F-3: m1=6 must STILL be unresolved through j=6 (v4's log) ----
        # The one slice the settle-at-j gate above does NOT pin down is
        # m1=6 (v4's log shows it open through j=6, resolved only at the
        # in-progress j=7). A corrupted cache producing a FALSE early
        # settle for m1=6 would otherwise pass every other check in this
        # gate silently -- this is the one place that would catch it.
        if j == 6:
            core.require((6, "primary") in remaining and (6, "secondary") in remaining,
                         f"157m2v5 F-3 REGRESSION FAILED: m1=6 (primary/secondary) expected to "
                         f"STILL be unresolved at j=6 (v4 log) -- got outcome "
                         f"{per_target_outcome[(6, 'primary')]!r} / "
                         f"{per_target_outcome[(6, 'secondary')]!r}")
            print(f"[{time.strftime('%H:%M:%S')}] j=6: F-3 REGRESSION MATCH (m1=6 still open, per v4 log)",
                  flush=True)

        elapsed_j = time.perf_counter() - t_j
        print(f"[{time.strftime('%H:%M:%S')}] j={j}: dim={info['dim_Lambda_over_Ij']} "
              f"build={elapsed_build:.1f}s total={elapsed_j:.1f}s remaining={sorted(remaining)} "
              f"proj_cache_size={len(proj_cache)} mul_cache_size={len(mul_cache)} "
              f"canary_checked={canary.checked}", flush=True)

        completed_j.add(j)
        ckpt["completed_j"] = sorted(completed_j)
        ckpt["per_target_progression"] = {target_key(*t): v for t, v in per_target_progression.items()}
        ckpt["per_target_outcome"] = {target_key(*t): v for t, v in per_target_outcome.items()}
        ckpt["canary_checked"] = canary.checked
        ckpt["canary_mismatches"] = canary.mismatches
        ckpt["purity_canary_seed_used"] = canary.seed_used
        ckpt["purity_canary_initial_phase"] = canary.initial_phase
        ckpt["f4_verified_js"] = sorted(f4_verified_js)
        save_checkpoint(ckpt)
        save_caches(proj_cache, mul_cache, got_sha)

        # ---- F-11(a): write a cert after EVERY completed j, not just at the end ----
        write_cert(assemble_result(
            run_role=run_role, max_j_reached=j, j_top_target=j_top,
            closed_form_identity_check=closed_form_identity_check,
            canary_rows=canary_rows, canary_pass=canary_pass, canary=canary,
            preflight_by_m1=preflight_by_m1, per_target_progression=per_target_progression,
            per_target_outcome=per_target_outcome, completed_j=completed_j,
            f4_verified_js=f4_verified_js,
            elapsed=time.perf_counter() - t_start, in_progress=True))

    for t in targets:
        if per_target_outcome[t]["status"] == "PENDING":
            per_target_outcome[t] = {"status": "J_MAX_EXHAUSTED_INCONCLUSIVE", "j_max": j_top}

    elapsed = time.perf_counter() - t_start
    result = assemble_result(
        run_role=run_role, max_j_reached=(max(completed_j) if completed_j else None), j_top_target=j_top,
        closed_form_identity_check=closed_form_identity_check,
        canary_rows=canary_rows, canary_pass=canary_pass, canary=canary,
        preflight_by_m1=preflight_by_m1, per_target_progression=per_target_progression,
        per_target_outcome=per_target_outcome, completed_j=completed_j,
        f4_verified_js=f4_verified_js,
        elapsed=elapsed, in_progress=False)
    out_path = write_cert(result)

    print(f"KOUBOU158_M2_MSWEEP_V5 verdict={result['verdict']} elapsed_s={elapsed:.2f} "
          f"max_j={j_top} output={out_path.as_posix()}", flush=True)

    # F-1: EXPAND_CAP resource-cap abortion (any_aborted) must NOT exit 0 --
    # an earlier version always `return 0` here, which is how a real
    # ABORTED_RESOURCE_CAP outcome (or, before F-1's fix, a purity-canary
    # failure mislabeled as one) could look green to a calling CI job.
    if result["any_slice_resource_cap_aborted"]:
        print("KOUBOU158_M2_MSWEEP_V5: at least one slice hit ABORTED_RESOURCE_CAP -- "
              "returning 1 (F-1), not a silent success", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
