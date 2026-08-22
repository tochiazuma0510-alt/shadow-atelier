"""koubou158_L3_core_fastkernel_v1.py

Additive companion (no-edit policy) to koubou158_L3_core_v1_1.py /
koubou158_L3_core_completebfs_v1.py, providing a faster computational
KERNEL for the SAME BFS submodule-closure semantics used by
koubou158_M2_msweep_v4.py -- the mathematical meaning is entirely
unchanged (same fox_gradient / apply_xi_minus_1 / project_vec_to_Ij
definitions; only HOW the results are computed differs, never WHAT is
computed).

PROFILING FINDING (scratchpad/profile_j4.py, cProfile on the j=4 build,
reported to commander before implementing anything further): the true
hotspot is NOT the linear-algebra kernel -- core.F3BitEchelon does not
even appear in the top 20 functions by cumulative time (well under 1%
of wall time). The actual breakdown at j=4 (32.8s total):
  - core.project_vec_to_Ij / project_pcvec_terms (recursive binomial
    expansion of a single pc-group-element into I^j monomials):
    23.75s cumulative (~66% of wall time), called 5088 times (2.1M
    calls into the recursive helper).
  - core.apply_xi_minus_1 -> IndependentPc.mul -> IndependentPc.collect
    (pc-presentation rewriting for one generator multiplication):
    8.63s cumulative (~19% of wall time).
Both are PURE functions of their inputs (project_pcvec_terms depends
only on (pcvec bytes, j); IndependentPc.mul(gen_pcvec(i), pcvec) depends
only on (i, pcvec)) and are called on a bounded, heavily-repeated input
space (the pc-group has exactly 3^10 = 59049 elements), so they are
MEMOIZED here -- this is expected to account for most of the real v5
speedup, not the linear-algebra change.

ALSO PROVIDED, per the commander's instruction (numpy int8 GF(3)
row-reduction, vectorized/blocked): F3NumpySpace / F3NumpyEchelon,
implementing the SAME external contract as core.F3BitSpace /
core.F3BitEchelon (vec/add/neg/sub/scale/leading/coeff_at/dot for the
space; reduce/add/rank/clone/rref/extract_separator for the echelon),
backed by dense int8 numpy rows, PLUS a batch_reduce() method that
tests multiple targets against the same echelon in one vectorized pass
(row subtraction is a numpy op over the full dimension instead of a
per-target Python bit loop) -- this is the "block" membership test the
v4->v5 dual sweep can use (up to 10 targets -- 5 remaining m1 values x
{primary, secondary} -- tested against the SAME per-j echelon).
Reported honestly: per the profiling above, this kernel swap alone is
NOT expected to be the dominant speedup for this specific workload; it
is included because it was explicitly instructed and is harmless
(same results, same interface), while the memoization above targets the
actually-measured bottleneck.

Both kernels are validated against the ORIGINAL core/cbfs functions by
the v5 regression gate (see koubou158_M2_msweep_v5.py) before j=7 is
attempted -- any divergence stops the run rather than silently
proceeding.

PURITY CANARY (commander instruction, 2026-08-22, after approving the
hotspot pivot): memoization is only sound if the cached functions are
truly pure (same input -> same output, always). Rather than trust that
blindly, PurityCanary below re-derives a small RANDOM SAMPLE of cache
hits (default 1-in-1000) from the ORIGINAL uncached core functions and
requires bit-for-bit agreement; any mismatch is a fail-closed
core.require() abort (reported, not silently patched), same discipline
as the rest of this lane.
"""
from __future__ import annotations

import random
from collections import defaultdict
from typing import Any

import numpy as np

import koubou158_L3_core_v1_1 as core


# ---------------------------------------------------------------------
# Purity canary: periodically re-derive a cache hit from the original
# (uncached) function and require exact agreement.
# ---------------------------------------------------------------------

class PurityCanary:
    def __init__(self, sample_rate: int = 1000, seed: int = 20260822) -> None:
        self.sample_rate = sample_rate
        # counter-based sampling (cheap: one int compare per hit, no per-call
        # RNG draw -- an earlier version called random.Random.randrange() on
        # EVERY cache hit and that alone cost ~30% of total wall time at
        # j=4, see scratchpad/profile_j4_fast.py's first run). A single RNG
        # draw at construction picks a random PHASE offset so the sampled
        # calls aren't always the same fixed stride-aligned ones across runs.
        self.counter = random.Random(seed).randrange(sample_rate)
        self.checked = 0
        self.mismatches = 0

    def maybe_check(self, recheck_fn) -> None:
        """recheck_fn: zero-arg callable that recomputes the value from
        the ORIGINAL uncached function and compares to the cached value,
        raising via core.require() on mismatch. Called on 1-in-sample_rate
        cache HITs (misses are already fresh computations, nothing to
        canary)."""
        self.counter += 1
        if self.counter >= self.sample_rate:
            self.counter = 0
            self.checked += 1
            recheck_fn()


# ---------------------------------------------------------------------
# Memoized projection / pc-multiplication (targets the ACTUAL hotspot)
# ---------------------------------------------------------------------

def project_pcvec_terms_cached(pcvec: bytes, j: int, cache: dict, canary: PurityCanary | None = None) -> list:
    key = (pcvec, j)
    hit = cache.get(key)
    if hit is not None:
        if canary is not None:
            def recheck():
                fresh = list(core.project_pcvec_terms(pcvec, j))
                core.require(fresh == hit, f"157m2v5 PURITY CANARY FAILED: project_pcvec_terms_cached "
                             f"drifted for pcvec={pcvec!r} j={j} (cached={hit!r} fresh={fresh!r})")
            canary.maybe_check(recheck)
        return hit
    terms = list(core.project_pcvec_terms(pcvec, j))
    cache[key] = terms
    return terms


def project_vec_to_Ij_cached(v_pi: dict, j: int, cache: dict, canary: PurityCanary | None = None) -> dict:
    out: dict = defaultdict(int)
    for (comp, pcvec), coeff in v_pi.items():
        for e_tuple, c in project_pcvec_terms_cached(pcvec, j, cache, canary):
            out[(comp, e_tuple)] = (out[(comp, e_tuple)] + coeff * c) % 3
    return {k: c for k, c in out.items() if c}


def apply_xi_minus_1_cached(v_pi: dict, i: int, pc: core.IndependentPc, mul_cache: dict,
                             canary: PurityCanary | None = None) -> dict:
    gi = core.gen_pcvec(i)
    translated: dict = defaultdict(int)
    for (comp, pcvec), c in v_pi.items():
        key = (i, pcvec)
        new_pc = mul_cache.get(key)
        if new_pc is not None:
            if canary is not None:
                def recheck(pcvec=pcvec, new_pc=new_pc):
                    fresh = pc.mul(gi, pcvec)
                    core.require(fresh == new_pc, f"157m2v5 PURITY CANARY FAILED: "
                                 f"apply_xi_minus_1_cached mul drifted for i={i} pcvec={pcvec!r} "
                                 f"(cached={new_pc!r} fresh={fresh!r})")
                canary.maybe_check(recheck)
        else:
            new_pc = pc.mul(gi, pcvec)
            mul_cache[key] = new_pc
        translated[(comp, new_pc)] = (translated[(comp, new_pc)] + c) % 3
    out: dict = defaultdict(int)
    for k, c in translated.items():
        out[k] = (out[k] + c) % 3
    for k, c in v_pi.items():
        out[k] = (out[k] - c) % 3
    return {k: c for k, c in out.items() if c}


# ---------------------------------------------------------------------
# numpy int8 GF(3) vectorized/blocked echelon (per commander instruction)
# ---------------------------------------------------------------------

class F3NumpySpace:
    def __init__(self, n: int) -> None:
        self.n = n

    def vec(self, d: dict) -> np.ndarray:
        v = np.zeros(self.n, dtype=np.int8)
        for i, c in d.items():
            v[i] = c % 3
        return v

    def add(self, v: np.ndarray, w: np.ndarray) -> np.ndarray:
        return ((v.astype(np.int16) + w.astype(np.int16)) % 3).astype(np.int8)

    def neg(self, v: np.ndarray) -> np.ndarray:
        return ((-v.astype(np.int16)) % 3).astype(np.int8)

    def sub(self, v: np.ndarray, w: np.ndarray) -> np.ndarray:
        return ((v.astype(np.int16) - w.astype(np.int16)) % 3).astype(np.int8)

    def scale(self, v: np.ndarray, c: int) -> np.ndarray:
        c %= 3
        if c == 0:
            return np.zeros(self.n, dtype=np.int8)
        return v.copy() if c == 1 else self.neg(v)

    def leading(self, v: np.ndarray) -> int:
        nz = np.flatnonzero(v)
        return int(nz[0]) if nz.size else -1

    def coeff_at(self, v: np.ndarray, pos: int) -> int:
        return int(v[pos])

    def dot(self, v: np.ndarray, w: np.ndarray) -> int:
        return int((np.dot(v.astype(np.int32), w.astype(np.int32))) % 3)


class F3NumpyEchelon:
    def __init__(self, sp: F3NumpySpace, pivots=None) -> None:
        self.sp = sp
        self.pivots: dict[int, np.ndarray] = dict(pivots) if pivots else {}

    def clone(self) -> "F3NumpyEchelon":
        return F3NumpyEchelon(self.sp, self.pivots)

    def reduce(self, v: np.ndarray):
        sp = self.sp
        v = v.copy()
        while True:
            p = sp.leading(v)
            if p < 0:
                return v, -1
            basis = self.pivots.get(p)
            if basis is None:
                return v, p
            c = sp.coeff_at(v, p)
            v = sp.sub(v, sp.scale(basis, c))

    def add(self, v: np.ndarray) -> bool:
        sp = self.sp
        v, p = self.reduce(v)
        if p < 0:
            return False
        c = sp.coeff_at(v, p)
        if c == 2:
            v = sp.neg(v)
        self.pivots[p] = v
        return True

    def rank(self) -> int:
        return len(self.pivots)

    def rref(self) -> None:
        sp = self.sp
        ordered = sorted(self.pivots, reverse=True)
        for p in ordered:
            v = self.pivots[p]
            for q in sorted(x for x in self.pivots if x > p):
                c = sp.coeff_at(v, q)
                if c:
                    v = sp.sub(v, sp.scale(self.pivots[q], c))
            self.pivots[p] = v

    def extract_separator(self, target: np.ndarray):
        sp = self.sp
        self.rref()
        v, f0 = self.reduce(target)
        if f0 < 0:
            return None
        cd = {f0: 1}
        for p, rv in self.pivots.items():
            co = sp.coeff_at(rv, f0)
            if co:
                cd[p] = (-co) % 3
        return sp.vec(cd)

    def batch_reduce(self, targets: list) -> list:
        """Blocked membership test: reduce MULTIPLE target vectors against
        this echelon together. Row subtraction (the O(n) inner step) is a
        single vectorized numpy op over the shared big dimension for all
        still-active targets at once, instead of one Python-level bit-loop
        per target (v4's per-target ech_clone.reduce(tv) sequence).
        Returns a list of pivot positions (-1 if fully reduced to zero,
        i.e. member) parallel to `targets`. Mathematically identical to
        calling reduce() once per target independently."""
        sp = self.sp
        if not targets:
            return []
        mat = np.stack([t.astype(np.int16) for t in targets]) % 3  # (k, n)
        k = mat.shape[0]
        result = [None] * k
        active = np.ones(k, dtype=bool)
        while active.any():
            idxs = np.flatnonzero(active)
            nz_mask = mat[idxs] != 0
            any_nz = nz_mask.any(axis=1)
            done_now = idxs[~any_nz]
            for r in done_now:
                result[r] = -1
                active[r] = False
            idxs = idxs[any_nz]
            if idxs.size == 0:
                continue
            leading_cols = np.argmax(mat[idxs] != 0, axis=1)
            progressed_any = False
            for r, p in zip(idxs, leading_cols):
                p = int(p)
                basis = self.pivots.get(p)
                if basis is None:
                    result[r] = p
                    active[r] = False
                    continue
                c = int(mat[r, p])
                mat[r] = (mat[r] - c * basis.astype(np.int16)) % 3
                progressed_any = True
            if not progressed_any:
                # any remaining active rows have no pivot at their leading col
                # (already handled above by setting result/active), so this
                # branch is unreachable in practice but guards against an
                # infinite loop if it ever were.
                break
        return result


# ---------------------------------------------------------------------
# Fast BFS closure: same algorithm as cbfs.submodule_closure_complete,
# same F3BitEchelon (bigint) linear-algebra kernel (NOT the measured
# bottleneck -- left unchanged per commander instruction), but routes
# apply_xi_minus_1 / project_vec_to_Ij through the memoized+canaried
# functions above.
# ---------------------------------------------------------------------

def submodule_closure_complete_fast(v_pi_raw: dict, j: int, idx: dict, sp, pc,
                                     shared_ech, proj_cache: dict, mul_cache: dict,
                                     canary: PurityCanary,
                                     cap: int = 600_000) -> dict:
    from collections import deque

    added = 0
    explored_by_depth: dict = defaultdict(int)
    seen_raw_keys: set = set()
    depth_cap = j - 1

    def fp(v: dict):
        return tuple(sorted(v.items()))

    v0_proj = project_vec_to_Ij_cached(v_pi_raw, j, proj_cache, canary)
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
            nxt = apply_xi_minus_1_cached(cur, i, pc, mul_cache, canary)
            if not nxt:
                continue
            explored_by_depth[depth + 1] += 1
            total_expanded += 1
            core.require(total_expanded <= cap,
                        f"157m2v5: submodule_closure_complete_fast exceeded safety cap {cap} "
                        f"at j={j} depth={depth+1} -- ABORTING, not silently truncating")
            key = fp(nxt)
            if key in seen_raw_keys:
                continue
            seen_raw_keys.add(key)
            nxt_proj = project_vec_to_Ij_cached(nxt, j, proj_cache, canary)
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


def build_V_and_D2bar_from_q3_complete_fast(e4, q3: dict, j: int, proj_cache: dict, mul_cache: dict,
                                             canary: PurityCanary):
    """Same construction as cbfs.build_V_and_D2bar_from_q3_complete (V from
    Schreier generators via the ORIGINAL uncached core functions -- that
    part is cheap, not memoized, no need), but the 11 PB4-relator closure
    uses submodule_closure_complete_fast (memoized+canaried) instead of
    cbfs.submodule_closure_complete. Linear-algebra kernel is
    core.F3BitEchelon, UNCHANGED (not the measured bottleneck)."""
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
        vp = project_vec_to_Ij_cached(v, j, proj_cache, canary)
        ech_v.add(sp.vec({idx[k]: c for k, c in vp.items() if k in idx}))
    rank_v = ech_v.rank()

    ech_combined = core.F3BitEchelon(sp, ech_v.pivots)
    per_relator_receipts = []
    for v_pi in rk_pi:
        receipt = submodule_closure_complete_fast(v_pi, j, idx, sp, pc, ech_combined,
                                                   proj_cache, mul_cache, canary)
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
        "kernel": "koubou158_L3_core_fastkernel_v1 (memoized project_vec_to_Ij / apply_xi_minus_1, "
                 "purity-canaried; F3BitEchelon linear-algebra kernel unchanged)",
        "method_note": "submodule_closure_complete_fast: SAME algorithm as cbfs.submodule_closure_complete "
                       "(expands every distinct nonzero raw vector, deduped by fingerprint, up to depth "
                       "j-1) -- only the project_vec_to_Ij and apply_xi_minus_1 calls are memoized "
                       "(cProfile-identified hotspot, scratchpad/profile_j4.py: 66%+19% of j=4 wall time), "
                       "with a purity canary re-deriving a random sample of cache hits from the original "
                       "uncached functions.",
    }
    return ech_combined, idx, sp, info
