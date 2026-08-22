"""koubou158_L3_core_completebfs_v1.py

Additive companion to search/koubou158_L3_core_v1_1.py (NOT a modification
of that file -- no-rename/no-edit policy). Implements a "complete" BFS
submodule-closure variant per commander instruction 2026-08-22 (v2.1
re-run order): the v2 sweep's core.submodule_closure_with_depth PRUNES
expansion -- it only re-enqueues a raw vector for further (x_i-1)
expansion when that vector's projection ADDED A NEW PIVOT to the shared
echelon (see core.py's own docstring: "a depth shortfall is the only
failure mode that could produce a FALSE NO -- if the BFS stopped early,
the combined span could be under-counted"). For m1=3 and m1=5, this
pruned BFS hit depth_requirement_satisfied=False exactly at the j (j=7)
where non_member first went True -- an untrustworthy NO by the core's own
documented criterion, reported honestly rather than accepted at face
value (search/certs/koubou158_M2_msweep_v2_20260822.json).

This module's submodule_closure_complete expands EVERY distinct nonzero
raw vector encountered (deduplicated by raw-vector fingerprint, not by
pivot status) up to depth j-1, so depth_requirement_satisfied becomes
true BY CONSTRUCTION whenever the frontier is fully explored to that
depth (the only way it can still read False is genuine natural
termination -- the frontier empties because all reachable raw vectors
are zero/already-seen, not because of pruning-on-no-new-pivot).

A resource cap (EXPAND_CAP) guards against runaway blowup on this 8GB
machine; hitting it is reported honestly as inconclusive-by-cap, not
silently truncated.
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

import koubou158_L3_core_v1_1 as core

EXPAND_CAP_PER_RELATOR = 600_000


def submodule_closure_complete(v_pi_raw: dict, j: int, idx: dict, sp, pc,
                               shared_ech, cap: int = EXPAND_CAP_PER_RELATOR) -> dict:
    """Full (non-pruned) BFS closure: expands every distinct nonzero raw
    vector reached, up to depth j-1, regardless of whether it changed the
    echelon's rank. Same return-dict shape as core.submodule_closure_with_depth
    so it plugs into the same aggregation code."""
    added = 0
    explored_by_depth: dict = defaultdict(int)
    seen_raw_keys: set = set()
    depth_cap = j - 1

    def fp(v: dict):
        return tuple(sorted(v.items()))

    v0_proj = core.project_vec_to_Ij(v_pi_raw, j)
    v0_indexed = {idx[k]: c for k, c in v0_proj.items() if k in idx}
    explored_by_depth[0] += 1
    if shared_ech.add(sp.vec(v0_indexed)):
        added += 1
    queue = deque()
    fp0 = fp(v_pi_raw)
    seen_raw_keys.add(fp0)
    if depth_cap >= 0:
        queue.append((v_pi_raw, 0))

    total_expanded = 0
    while queue:
        cur, depth = queue.popleft()
        if depth >= depth_cap:
            continue
        for i in range(1, core.N_GEN + 1):
            nxt = core.apply_xi_minus_1(cur, i, pc)
            if not nxt:
                continue
            explored_by_depth[depth + 1] += 1
            total_expanded += 1
            core.require(total_expanded <= cap,
                        f"157m2.1: submodule_closure_complete exceeded safety cap {cap} "
                        f"at j={j} depth={depth+1} -- ABORTING, not silently truncating")
            key = fp(nxt)
            if key in seen_raw_keys:
                continue
            seen_raw_keys.add(key)
            nxt_proj = core.project_vec_to_Ij(nxt, j)
            nxt_indexed = {idx[k]: c for k, c in nxt_proj.items() if k in idx}
            if shared_ech.add(sp.vec(nxt_indexed)):
                added += 1
            queue.append((nxt, depth + 1))

    max_depth_explored = max(explored_by_depth.keys()) if explored_by_depth else 0
    return {
        "new_pivots": added,
        "max_depth_reached": max_depth_explored,
        "explored_count_by_depth": dict(sorted(explored_by_depth.items())),
        "complete_bfs": True,
        "distinct_raw_vectors_seen": len(seen_raw_keys),
    }


def build_V_and_D2bar_from_q3_complete(e4, q3: dict, j: int):
    """Same construction as core.build_V_and_D2bar_from_q3 (V from Schreier
    generators, unchanged -- no depth/pruning concern there), but the 11
    PB4-relator closure uses submodule_closure_complete instead of
    core.submodule_closure_with_depth."""
    pc = e4.pc
    pb4_rels = q3["formulas"]["presentations"]["PB4"]["relations"]
    core.require(len(pb4_rels) == 11, "PB4 relation count")
    rk = [core.fox_gradient(e4, r) for r in pb4_rels]
    rk_pi = [core.project_to_pi(v) for v in rk]

    x0_val = e4.eval(core.X0)
    y0_val = e4.eval(core.Y0)
    z0_val = e4.eval(core.Z0)
    xbar, ybar, zbar = x0_val[1], y0_val[1], z0_val[1]

    C_word = core.substitute2(core.FIXED_WORD, core.Y0, core.Z0)
    Cbar_E4 = e4.eval(C_word)

    g1 = (xbar, xbar, ybar)
    g2 = (ybar, zbar, zbar)
    transversal, tree_edge = core.enum_delta_pc(g1, g2, pc, core.DELTA_CAP)
    n_delta = len(transversal)
    sgens = core.schreier_generators_pc(transversal, tree_edge, g1, g2, pc)
    core.require(len(sgens) == n_delta + 1, f"expected {n_delta+1} Schreier generators, got {len(sgens)}")

    sigma_vectors_pi = []
    for c_word in sgens:
        ga = core.fox_gradient(e4, core.substitute2(c_word, core.X0, core.Y0))
        gb = core.fox_gradient(e4, core.substitute2(c_word, core.X0, core.Z0))
        gc = core.fox_gradient(e4, core.substitute2(c_word, core.Y0, core.Z0))
        diff = core.add_vec(gc, core.neg_vec(gb))
        sigma_c = core.add_vec(core.translate_vec(e4, diff, Cbar_E4), ga)
        sigma_vectors_pi.append(core.project_to_pi(sigma_c))

    monomials = core.enumerate_monomials(j)
    idx = {(c, e): i for i, (c, e) in enumerate((c, e) for c in range(1, 7) for e in monomials)}
    dim_j = len(idx)
    sp = core.F3BitSpace(dim_j)

    ech_v = core.F3BitEchelon(sp)
    for v in sigma_vectors_pi:
        vp = core.project_vec_to_Ij(v, j)
        ech_v.add(sp.vec({idx[k]: c for k, c in vp.items() if k in idx}))
    rank_v = ech_v.rank()

    ech_combined = core.F3BitEchelon(sp, ech_v.pivots)
    per_relator_receipts = []
    for v_pi in rk_pi:
        receipt = submodule_closure_complete(v_pi, j, idx, sp, pc, ech_combined)
        per_relator_receipts.append(receipt)
    rank_combined = ech_combined.rank()

    info = {
        "n_Delta": n_delta, "n_schreier_generators": len(sgens),
        "j": j, "dim_monomials": len(monomials), "dim_Lambda_over_Ij": dim_j,
        "rank_V": rank_v, "rank_V_plus_D2bar_combined": rank_combined,
        "per_relator_closure_receipts": per_relator_receipts,
        "min_depth_reached_across_relators": min(r["max_depth_reached"] for r in per_relator_receipts),
        "depth_requirement_j_minus_1": j - 1,
        "depth_requirement_satisfied": all(r["max_depth_reached"] >= j - 1 for r in per_relator_receipts),
        "total_vectors_explored": sum(sum(r["explored_count_by_depth"].values()) for r in per_relator_receipts),
        "complete_bfs_variant": True,
        "method_note": "submodule_closure_complete: expands EVERY distinct nonzero raw vector "
                       "(deduped by fingerprint, not by pivot status) up to depth j-1 -- fixes "
                       "the pruning risk flagged in core.py's own docstring, per commander "
                       "instruction 2026-08-22 (v2.1 re-run order).",
    }
    return ech_combined, idx, sp, info
