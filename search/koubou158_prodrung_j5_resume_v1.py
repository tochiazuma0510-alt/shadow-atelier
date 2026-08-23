"""koubou158_prodrung_j5_resume_v1.py

Resumable, per-relator-checkpointed driver for the prodrung lane's j=5
level (search/koubou158_prodrung_v1.py). Two consecutive attempts at
j<=5 (single uninterrupted process) were KILLED at essentially the same
point (right as j=5's closure computation begins, ~10-12 minutes into
the run) -- this strongly suggests an external time limit on background
tasks in this environment, not a crash (j=2,3,4 always completed cleanly
first; only j=5's own, much larger closure computation (dim=31320,
~7x j=4's cost) triggers the kill).

FIX: process the 11 PB4 relators' im(D2bar) closures at j=5 ONE AT A
TIME, in SEPARATE short-lived process invocations, checkpointing the
shared echelon's pivot state (serialized to hex strings, JSON-safe) to
disk after each relator completes. A bash driver loop invokes this
script repeatedly (--relator-index 0..10) until all are done, then a
final --stage finalize invocation adds V, tests the 18 remaining
branches, and MERGES the j=5 result into the existing
search/certs/koubou158_prodrung_v1_20260822.json cert (whose j=2,3,4
levels are already complete and unaffected -- each j level is an
independent quotient, no cross-j recomputation needed).

Checkpoint file: scratchpad/prodrung_j5_checkpoint.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "search"))
import koubou158_L3_core_v1_2 as core  # noqa: E402
import koubou158_prodrung_v1 as pr  # noqa: E402

Q3_CHIEF = core.Q3_CHIEF
Q3_CHIEF_SHA = core.Q3_CHIEF_SHA
Q3_CHIEF_BYTES = core.Q3_CHIEF_BYTES

J = 5
BLOCK_START = pr.BLOCK_START
BLOCK_SIZE = pr.BLOCK_SIZE
CKPT_PATH = ROOT / "scratchpad" / "prodrung_j5_checkpoint.json"
FINAL_CERT_PATH = ROOT / "search" / "certs" / "koubou158_prodrung_v1_20260822.json"


def serialize_pivots(pivots: dict) -> dict:
    return {str(pos): [hex(v[0]), hex(v[1])] for pos, v in pivots.items()}


def deserialize_pivots(d: dict) -> dict:
    return {int(pos): (int(hv[0], 16), int(hv[1], 16)) for pos, hv in d.items()}


def load_checkpoint() -> dict:
    if CKPT_PATH.is_file():
        return json.loads(CKPT_PATH.read_text(encoding="utf-8"))
    return {"j": J, "completed_relator_indices": [], "echelon_pivots": {}, "per_relator_receipts": {}}


def save_checkpoint(ckpt: dict) -> None:
    CKPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CKPT_PATH.write_text(json.dumps(ckpt, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_context():
    full = ROOT / Q3_CHIEF
    core.require(full.is_file(), "q3_chief receipt missing")
    core.require(full.stat().st_size == Q3_CHIEF_BYTES, "q3_chief byte drift")
    got_sha = core.sha_file(full)
    core.require(got_sha == Q3_CHIEF_SHA, f"q3_chief SHA drift: got {got_sha}")
    q3 = json.loads(full.read_text(encoding="utf-8"))
    e4 = core.E4(q3)
    B = pr.build_B(e4, BLOCK_START, BLOCK_SIZE)
    core.require(len(B) == 18, f"expected |B|=18, got {len(B)}")

    pb4_rels = q3["formulas"]["presentations"]["PB4"]["relations"]
    core.require(len(pb4_rels) == 11, "PB4 relation count")
    rk_E4 = [core.fox_gradient(e4, r) for r in pb4_rels]
    rk_bpi = [pr.project_to_B_and_pi(v, BLOCK_START, BLOCK_SIZE) for v in rk_E4]

    monomials = core.enumerate_monomials(J)
    idx = pr.build_idx(monomials, B)
    dim_j = len(idx)
    sp = core.F3BitSpace(dim_j)
    return q3, e4, B, rk_bpi, idx, sp, dim_j


def do_relator(relator_index: int) -> None:
    t0 = time.perf_counter()
    ckpt = load_checkpoint()
    if relator_index in ckpt["completed_relator_indices"]:
        print(f"relator {relator_index} already completed (checkpoint), skipping", flush=True)
        return

    q3, e4, B, rk_bpi, idx, sp, dim_j = build_context()
    ech = core.F3BitEchelon(sp, deserialize_pivots(ckpt["echelon_pivots"]))
    rank_before = ech.rank()

    rec = pr.submodule_closure_B_pi(rk_bpi[relator_index], J, idx, sp, e4, ech, B)
    rank_after = ech.rank()

    ckpt["echelon_pivots"] = serialize_pivots(ech.pivots)
    ckpt["completed_relator_indices"] = sorted(set(ckpt["completed_relator_indices"]) | {relator_index})
    ckpt["per_relator_receipts"][str(relator_index)] = rec
    save_checkpoint(ckpt)

    elapsed = time.perf_counter() - t0
    print(f"relator {relator_index}: rank {rank_before} -> {rank_after} "
          f"(new_pivots={rec['new_pivots']}, max_depth={rec['max_depth_reached']}) "
          f"in {elapsed:.1f}s. completed={len(ckpt['completed_relator_indices'])}/11", flush=True)


def do_finalize() -> None:
    t0 = time.perf_counter()
    ckpt = load_checkpoint()
    core.require(len(ckpt["completed_relator_indices"]) == 11,
                 f"finalize called with only {len(ckpt['completed_relator_indices'])}/11 relators done")

    q3, e4, B, rk_bpi, idx, sp, dim_j = build_context()
    ech_d2 = core.F3BitEchelon(sp, deserialize_pivots(ckpt["echelon_pivots"]))
    rank_d2_alone = ech_d2.rank()

    x0_val, y0_val, z0_val = e4.eval(pr.X0), e4.eval(pr.Y0), e4.eval(pr.Z0)

    def to_B(val):
        return (bytes(x - BLOCK_START for x in val[0][BLOCK_START:BLOCK_START + BLOCK_SIZE]), val[1])

    xbar, ybar, zbar = to_B(x0_val), to_B(y0_val), to_B(z0_val)
    g1 = (xbar, xbar, ybar)
    g2 = (ybar, zbar, zbar)

    identity3 = ((bytes(range(BLOCK_SIZE)), e4.pc.one()),) * 3
    transversal = {identity3: []}
    tree_edge: dict = {}
    queue = deque([identity3])
    gens = {1: g1, 2: g2}
    while queue:
        cur = queue.popleft()
        cur_word = transversal[cur]
        for s in (1, 2):
            g = gens[s]
            nxt = tuple((core.perm_mul(cur[i][0], g[i][0]), e4.pc.mul(cur[i][1], g[i][1])) for i in range(3))
            if nxt not in transversal:
                core.require(len(transversal) < pr.DELTA_CAP, "Delta enumeration exceeded cap")
                transversal[nxt] = cur_word + [s]
                tree_edge[nxt] = (cur, s)
                queue.append(nxt)
    n_delta = len(transversal)

    sgens: list[list[int]] = []
    for delta, t_delta in transversal.items():
        for s in (1, 2):
            g = gens[s]
            nxt = tuple((core.perm_mul(delta[i][0], g[i][0]), e4.pc.mul(delta[i][1], g[i][1])) for i in range(3))
            edge = tree_edge.get(nxt)
            if edge is not None and edge == (delta, s):
                continue
            t_nxt = transversal[nxt]
            sgens.append(core.reduce_word(t_delta + [s] + core.inv_word(t_nxt)))
    core.require(len(sgens) == n_delta + 1, f"expected {n_delta+1} Schreier generators, got {len(sgens)}")

    C_word = core.substitute2(pr.FIXED_WORD, pr.Y0, pr.Z0)
    Cbar_E4 = e4.eval(C_word)
    sigma_vectors_bpi = []
    for c_word in sgens:
        ga = core.fox_gradient(e4, core.substitute2(c_word, pr.X0, pr.Y0))
        gb = core.fox_gradient(e4, core.substitute2(c_word, pr.X0, pr.Z0))
        gc = core.fox_gradient(e4, core.substitute2(c_word, pr.Y0, pr.Z0))
        diff = core.add_vec(gc, core.neg_vec(gb))
        sigma_c = core.add_vec(core.translate_vec(e4, diff, Cbar_E4), ga)
        sigma_vectors_bpi.append(pr.project_to_B_and_pi(sigma_c, BLOCK_START, BLOCK_SIZE))

    ech_v = core.F3BitEchelon(sp)
    for v in sigma_vectors_bpi:
        ech_v.add(sp.vec(pr.project_vec_to_aj(v, J, idx)))
    rank_v = ech_v.rank()

    ech_combined = ech_d2.clone()
    for v in sigma_vectors_bpi:
        ech_combined.add(sp.vec(pr.project_vec_to_aj(v, J, idx)))
    rank_combined = ech_combined.rank()

    existing_cert = json.loads(FINAL_CERT_PATH.read_text(encoding="utf-8"))
    undetermined = set(existing_cert["branch_results"].keys())
    undetermined = {bid for bid in undetermined if not existing_cert["branch_results"][bid]["non_member"]}
    core.require(undetermined == set(pr.REMAINING_18_BRANCHES), "undetermined branch set drift vs existing cert")

    # branch-level checkpointing (added after the finalize step was ALSO
    # killed mid-way, having tested 15/18 branches with no persistence) --
    # skip already-tested branches, checkpoint after each remaining one.
    branch_ckpt = ckpt.get("branch_results_j5", {})
    newly_resolved = {bid: rec for bid, rec in branch_ckpt.items() if rec.get("non_member")}
    already_tested = set(branch_ckpt.keys())
    for bid in sorted(undetermined):
        if bid in already_tested:
            print(f"branch {bid}: already tested (checkpoint) -> "
                  f"{'NON-MEMBER' if branch_ckpt[bid]['non_member'] else 'still member'}, skipping", flush=True)
            continue
        r_idx = int(bid.split("_c")[0][1:])
        c_idx = int(bid.split("_c")[1])
        rw = pr.roof_word(q3, r_idx)
        cw = pr.correction_word(q3, c_idx)
        candidate_word = core.reduce_word(list(rw) + list(cw))
        c_w = core.substitute2(candidate_word, pr.Y0, pr.Z0)
        b_w = core.substitute2(candidate_word, pr.X0, pr.Z0)
        a_w = core.substitute2(candidate_word, pr.X0, pr.Y0)
        h1_word = core.reduce_word(c_w + core.inv_word(b_w) + a_w)
        nabla_bp = core.fox_gradient(e4, h1_word)
        grad_bpi = pr.project_to_B_and_pi(nabla_bp, BLOCK_START, BLOCK_SIZE)
        tv = sp.vec(pr.project_vec_to_aj(grad_bpi, J, idx))
        ech_branch = ech_combined.clone()
        _, pivot = ech_branch.reduce(tv)
        non_member = pivot >= 0
        if non_member:
            sep = ech_branch.extract_separator(tv)
            core.require(sep is not None, f"branch {bid}: separator extraction failed at j={J}")
            support = bin(sep[0] | sep[1]).count("1")
            phi_val = sp.dot(sep, tv)
            rec = {"branch_id": bid, "j_star": J, "non_member": True,
                  "separator": {"support": support, "phi_val": phi_val}}
            newly_resolved[bid] = rec
            branch_ckpt[bid] = rec
            print(f"branch {bid}: NON-MEMBER at j={J}", flush=True)
        else:
            rec = {"branch_id": bid, "j_star": None, "non_member": False, "separator": None}
            branch_ckpt[bid] = rec
            print(f"branch {bid}: still member at j={J}", flush=True)
        ckpt["branch_results_j5"] = branch_ckpt
        save_checkpoint(ckpt)

    per_relator_receipts = [ckpt["per_relator_receipts"][str(k)] for k in range(11)]
    depth_ok = all(r["max_depth_reached"] >= J - 1 for r in per_relator_receipts)
    j5_entry = {
        "j": J, "dim_Lambda_over_aj": dim_j, "rank_D2bar_alone": rank_d2_alone,
        "rank_V": rank_v, "rank_combined": rank_combined,
        "depth_requirement_observational_ok": depth_ok,
        "per_relator_closure_receipts": per_relator_receipts,
        "n_branches_resolved_this_level": len(newly_resolved),
        "n_branches_still_undetermined_after": len(undetermined) - len(newly_resolved),
        "wall_seconds": time.perf_counter() - t0,
        "note": "computed via the resumable per-relator-checkpointed driver "
                "(koubou158_prodrung_j5_resume_v1.py), not the single-process j-loop "
                "in koubou158_prodrung_v1.py -- two single-process j<=5 attempts were "
                "killed by an external time limit at this exact level",
    }

    for bid, rec in newly_resolved.items():
        existing_cert["branch_results"][bid] = rec
    existing_cert["j_progression"].append(j5_entry)
    n_dead = sum(1 for r in existing_cert["branch_results"].values() if r["non_member"])
    n_undetermined = 18 - n_dead
    existing_cert["n_branches_dead"] = n_dead
    existing_cert["n_branches_undetermined"] = n_undetermined
    existing_cert["all_18_dead"] = (n_dead == 18)
    existing_cert["overall_reading"] = (
        ("all 18 remaining branches DIE at this rung (Ebar_B x Pi4[3] full, reached at j=5): "
         "162/162 branches now have target6 (or their own analog) unliftable to the full "
         "legal-correction span at SOME rung -- combined with the 144 already resolved at "
         "plain L3, this DISCHARGES condition (ii) for the ENTIRE 162-branch census (part of "
         "condition (i)'s census discharges too). NOT reported as OBS*: (iii)/(iv) of T-56 "
         "remain open."
         if existing_cert["all_18_dead"] else
         f"{n_dead}/18 branches resolved (DEAD) through j<=5; {n_undetermined} remain "
         "undetermined at this rung -- next step (PSL(2,8) x Pi, not attempted here) would "
         "be needed for those, per commander's own framing")
    )
    existing_cert["j5_resumable_driver_note"] = (
        "j=5 (dim=31320) was computed via a SEPARATE, resumable, per-relator-checkpointed "
        "driver (search/koubou158_prodrung_j5_resume_v1.py), not the single-process j-loop "
        "in the original producer -- two single-process attempts at j<=5 were independently "
        "KILLED (background task timeout) at essentially the same point (right as j=5's "
        "closure computation began, after j=2/3/4 completed cleanly each time). The "
        "resumable driver processes the 11 relators' closures one at a time across separate "
        "short-lived invocations, checkpointing the shared echelon's pivot state to "
        "scratchpad/prodrung_j5_checkpoint.json between calls."
    )

    text = json.dumps(existing_cert, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    FINAL_CERT_PATH.write_text(text, encoding="utf-8")
    readback = FINAL_CERT_PATH.read_text(encoding="utf-8")
    core.require(readback == text, "checked-write readback mismatch")

    print(f"FINALIZE done: n_dead={n_dead}/18 all_18_dead={existing_cert['all_18_dead']} "
          f"elapsed={time.perf_counter()-t0:.1f}s output={FINAL_CERT_PATH}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="stage", required=True)
    sp1 = sub.add_parser("relator")
    sp1.add_argument("--index", type=int, required=True)
    sub.add_parser("finalize")
    sub.add_parser("status")
    args = ap.parse_args()

    if args.stage == "relator":
        do_relator(args.index)
    elif args.stage == "finalize":
        do_finalize()
    elif args.stage == "status":
        ckpt = load_checkpoint()
        print(f"completed_relator_indices={sorted(ckpt['completed_relator_indices'])} "
              f"({len(ckpt['completed_relator_indices'])}/11)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
