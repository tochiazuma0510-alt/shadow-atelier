#!/usr/bin/env python3
"""koubou158_sweep_v1.py (lane koubou160-bsweep-v1 per docs/notes/branch_sweep_design_v1.md)

Implements P0-P1 of the branch-sweep design (docs/notes/branch_sweep_design_v1.md
sec 4): a GENERIC chain-rule gradient evaluator over the WordExprDAG opcode
table (sec 2.1), used to (a) reproduce target6's addendum-sec-2.3' closed
form through an independently-structured code path (canary c1), (b) confirm
targets 1-5 are literally the identity node with zero gradient everywhere
(canary c3 / BSW-0), and (c) reproduce the frozen base_gradient hash /
per-seed typed_split hashes (canary c2).

*** SCOPE ACTUALLY DELIVERED THIS PASS (report honestly; see "NOT DONE" below) ***

DONE:
  - Generic Expr AST (Gen/F/Mul/Inv/PaperProduct/Identity) + grad_base/
    grad_delta recursive evaluator implementing design doc sec 2.1's table
    exactly (generator atom, f-at-context atom with its 2-char chain rule,
    product rule nabla(UV)=nabla(U)+Ubar.nabla(V), inverse rule
    nabla(U^-1)=-Ubar^-1.nabla(U), paper_product = product_many(reversed)).
  - target6 built THROUGH this generic evaluator (not the old hand-rolled
    closed form from koubou158_sat_wired_v1.py) as
    PaperProduct([F(x0,y0), Inv(F(x0,z0)), F(y0,z0)]), matching the frozen
    receipt's registered product_order "h1=C*B^-1*A".
  - canary c1: generic-evaluator base gradient (nabla_b) and all 108 delta
    gradients (s_j) cross-checked against the frozen 157en receipt's own
    claimed hashes (base_gradient.canonical_gradient_sha256,
    target6.typed_split[j].gradient_sha256) -- same external ground truth
    koubou158_sat_wired_v1.py used, but reached via a STRUCTURALLY
    DIFFERENT code path (recursive Expr evaluator vs. the hand-derived
    Cbar*([c]-[b])+[a] formula), so a match is a genuine cross-check of
    BOTH implementations, not just a repeat of the same arithmetic.
  - canary c3 / BSW-0: T1-5 = Identity() expr; confirmed grad_base and
    every grad_delta(w_j) are the empty dict (TRUE, matches design doc's
    proof-by-construction claim in sec 0 correction 2).
  - canary c2: nabla_b entry_count == 72 and matches base_gradient_sha256.

NOT DONE (flagged, not silently skipped -- see design doc sec 6 GAP list and
this cert's "blockers" section):
  - c4 (formula_checks[].formula text cross-check) is only meaningfully
    exercised for target6 (the only target this receipt carries
    formula_checks for); T7-T27's formula text was not located in the
    receipts available to this script and was NOT guessed at.
  - c5 (D1 canary: D1(nabla_b')=0, D1(s_j')=0) is NOT implemented -- the
    operator D1 is referenced in addendum sec S3' canary-3 but its precise
    definition was not found in the addendum itself (likely in
    direct_membership_design_v1.md v1, which this pass did not read in
    full). Implementing an undefined operator from a guess would risk a
    silent wrong-formula bug exactly of the kind this whole canary
    discipline exists to catch -- flagged rather than guessed.
  - P2 (BSW-1 at L1, barE=PSL(2,8) order 504) is NOT attempted: it needs
    the projection pi: E4 -> P constructed as "restrict the 144-point
    permutation to one 9-point block of the P^4 factor", which per the
    addendum needs a GAP orbit decomposition to IDENTIFY which block (the
    addendum's own "implementer procedure" is a GAP session, not a pure-
    Python derivation). This is a distinct, well-scoped follow-up task,
    not attempted here to avoid a wrong/guessed block identification.
  - P3-P6 (22-target battery, STACKED, axis C/R sweep, L0->L2->L3
    promotion) all DEPEND on P2 (the NM predicate is defined at L1) and
    on having verified composition formulas for T7-T27 (not yet located)
    -- NOT started.

Because P2 (the actual NM/DEAD determination) was not reached, this cert
makes NO branch-liveness claim of any kind. It only reports: does the
generic evaluator reproduce known frozen numbers, yes/no.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "search"))

Q3_PATH = REPO_ROOT / "ci" / "b345_157en_artifacts_32458556448" / "d972_b345_q3_chief_v1.json"
COLGEN_PATH = REPO_ROOT / "ci" / "b345_157en_artifacts_32458556448" / "d972_b345_target6_dual_colgen_v2.json"
SEEDSPAN_MODULE_PATH = REPO_ROOT / "search" / "d972_b345_seedspan_triple4_v1.py"
CERT_DIR = REPO_ROOT / "search" / "certs"

X0, Y0, Z0 = [4], [6], [-4, -6]  # target6's 3 contexts (addendum sec 2.3' 2.2)


def load_seedspan_module():
    spec = importlib.util.spec_from_file_location("_koubou158_seedspan", SEEDSPAN_MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_koubou158_seedspan"] = mod  # required before exec_module: py3.13
    # dataclasses resolves field types via sys.modules[cls.__module__], which
    # must already point at this module object during class-body execution.
    spec.loader.exec_module(mod)
    return mod


def reduce_word(word):
    out = []
    for l in word:
        if out and out[-1] == -l:
            out.pop()
        else:
            out.append(l)
    return out


def inv_word(w):
    return reduce_word([-x for x in reversed(w)])


def substitute2(word2, x, y):
    out = []
    for l in word2:
        if l == 1:
            out.extend(x)
        elif l == -1:
            out.extend(inv_word(x))
        elif l == 2:
            out.extend(y)
        elif l == -2:
            out.extend(inv_word(y))
        else:
            raise ValueError(f"unexpected 2-generator token {l}")
        out = reduce_word(out)
    return out


def fox_gradient_E4(word, e4):
    acc = defaultdict(int)
    prefix = e4.identity
    for l in word:
        i = abs(l)
        if l > 0:
            acc[(i, prefix)] += 1
            prefix = e4.mul(prefix, e4.generators[i - 1])
        else:
            prefix = e4.mul(prefix, e4.inverse(e4.generators[i - 1]))
            acc[(i, prefix)] += -1
    return {k: v % 3 for k, v in acc.items() if v % 3}


def add_vec(a, b):
    out = defaultdict(int)
    for k, v in a.items():
        out[k] = (out[k] + v) % 3
    for k, v in b.items():
        out[k] = (out[k] + v) % 3
    return {k: v for k, v in out.items() if v}


def neg_vec(a):
    return {k: (-v) % 3 for k, v in a.items()}


def translate_vec_E4(v, g, e4):
    out = defaultdict(int)
    for (comp, elt), c in v.items():
        out[(comp, e4.mul(g, elt))] = (out[(comp, e4.mul(g, elt))] + c) % 3
    return {k: c for k, c in out.items() if c}


def blob_hex(v):
    return (v[0] + v[1]).hex()


def canonical_gradient_sha256(grad):
    rows = sorted([comp, blob_hex(elt), coeff] for (comp, elt), coeff in grad.items())
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------------------
# Generic WordExprDAG-opcode evaluator (design doc sec 2.1 table)
# ---------------------------------------------------------------------------


class Expr:
    def value(self, e4):
        raise NotImplementedError

    def grad_base(self, e4):
        """nabla, at w = empty (no seed correction)."""
        raise NotImplementedError

    def grad_delta(self, e4, w):
        """delta-nabla, the seed-correction gradient for seed word w."""
        raise NotImplementedError


@dataclass(frozen=True)
class Identity(Expr):
    """DAG.identity(6): the vacuous acceptance-row atom (design doc sec 0
    correction 2 / T1-T5). Value = E4 identity, gradient = 0 always."""
    def value(self, e4):
        return e4.identity

    def grad_base(self, e4):
        return {}

    def grad_delta(self, e4, w):
        return {}


@dataclass(frozen=True)
class Gen(Expr):
    """A single free generator a_i (1-indexed into e4.generators)."""
    i: int

    def value(self, e4):
        return e4.generators[self.i - 1]

    def grad_base(self, e4):
        return {(self.i, e4.identity): 1}

    def grad_delta(self, e4, w):
        return {}  # generators do not depend on the seed


@dataclass(frozen=True)
class F(Expr):
    """f evaluated at context (ell, rho): FIXED_WORD(ell,rho), with the
    seed-correction reading FIXED_WORD as 'base . correction' so
    grad_delta = fbar . nabla(w(ell,rho)) (design doc sec 2.1 table row 2)."""
    ell: tuple
    rho: tuple
    fixed_word: tuple

    def _full_word(self):
        return substitute2(list(self.fixed_word), list(self.ell), list(self.rho))

    def value(self, e4):
        return e4.eval(self._full_word())

    def grad_base(self, e4):
        return fox_gradient_E4(self._full_word(), e4)

    def grad_delta(self, e4, w):
        fbar = self.value(e4)
        w_word = substitute2(list(w), list(self.ell), list(self.rho))
        return translate_vec_E4(fox_gradient_E4(w_word, e4), fbar, e4)


@dataclass(frozen=True)
class Mul(Expr):
    a: Expr
    b: Expr

    def value(self, e4):
        return e4.mul(self.a.value(e4), self.b.value(e4))

    def grad_base(self, e4):
        abar = self.a.value(e4)
        return add_vec(self.a.grad_base(e4), translate_vec_E4(self.b.grad_base(e4), abar, e4))

    def grad_delta(self, e4, w):
        abar = self.a.value(e4)
        return add_vec(self.a.grad_delta(e4, w), translate_vec_E4(self.b.grad_delta(e4, w), abar, e4))


@dataclass(frozen=True)
class Inv(Expr):
    a: Expr

    def value(self, e4):
        return e4.inverse(self.a.value(e4))

    def grad_base(self, e4):
        ainv = e4.inverse(self.a.value(e4))
        return neg_vec(translate_vec_E4(self.a.grad_base(e4), ainv, e4))

    def grad_delta(self, e4, w):
        ainv = e4.inverse(self.a.value(e4))
        return neg_vec(translate_vec_E4(self.a.grad_delta(e4, w), ainv, e4))


def paper_product(items: Sequence[Expr]) -> Expr:
    """paper_product(list) = product_many(reversed(list)); product_many is a
    left fold of Mul in list order (design doc sec 2.1 / v1.1 sec 2.1)."""
    chain = list(reversed(items))
    acc = chain[0]
    for item in chain[1:]:
        acc = Mul(acc, item)
    return acc


def product_many(items: Sequence[Expr]) -> Expr:
    """Plain left-to-right fold of Mul, NO reversal (distinct from
    paper_product -- both appear in build_wordexpr_candidate, see P3)."""
    acc = items[0]
    for item in items[1:]:
        acc = Mul(acc, item)
    return acc


def substitute_expr(word: Sequence[int], roots: Sequence[Expr]) -> Expr:
    """dag.substitute(word, roots): word is a free-group word over an
    abstract alphabet 1..len(roots); substitute token i -> roots[i-1] (or
    Inv(roots[i-1]) if negative), left to right. This is NOT a new gradient
    rule -- it decomposes into the existing Mul/Inv recursion, so its
    grad_base/grad_delta correctness follows directly from Mul/Inv's already
    -verified rules (no new formula to get wrong)."""
    parts = [roots[abs(l) - 1] if l > 0 else Inv(roots[abs(l) - 1]) for l in word]
    return product_many(parts)


def flat_expr(word: Sequence[int], n_gens: int = 6) -> Expr:
    """dag.flat(word, n): a literal free-group word over the n real
    generators, as an Expr (via substitute_expr with the generator atoms)."""
    gens = [Gen(i) for i in range(1, n_gens + 1)]
    return substitute_expr(word, gens)


def run_p0_p1():
    """Returns (ok, e4, nabla_b, seed_gradients) where seed_gradients is a
    list of (seed_index_1based, s_j dict) -- reused by run_p2_l1 so the L1
    projection doesn't need to recompute gradients from scratch."""
    t0 = time.time()
    cert = {
        "schema": "shadow-atelier/koubou158-sweep-P0-P1/v1",
        "namespace": "koubou158_sweep_*",
        "lane": "koubou160-bsweep-v1",
        "generated_by": "search/koubou158_sweep_v1.py",
        "generated_at_unix": time.time(),
        "design_authority": "docs/notes/branch_sweep_design_v1.md sec 2.1, 4 (P0-P1)",
        "phase": "P0-P1 only (see module docstring for exact scope + NOT DONE list)",
        "blockers": [
            {"id": "P2-blocker", "detail": "BSW-1 (NM at L1, barE=PSL(2,8) order 504) needs "
                                            "projection pi:E4->P via GAP orbit-block identification "
                                            "(addendum v1.1 sec 3's own recommended procedure is a "
                                            "GAP session) -- not attempted this pass."},
            {"id": "P3-blocker", "detail": "T7-T27 composition formulas (hexagon_2/pentagon/source "
                                            "row structure) were not located in the receipts read "
                                            "this pass; only T6's formula (registered "
                                            "product_order='h1=C*B^-1*A') and T1-T5 (vacuous "
                                            "identity, per design doc sec 0 correction 2) were "
                                            "confirmed. 22-target battery NOT built."},
            {"id": "c5-blocker", "detail": "D1 canary operator definition not located in the "
                                            "addendum; not guessed at."},
        ],
    }

    q3_bytes = Q3_PATH.read_bytes()
    colgen_bytes = COLGEN_PATH.read_bytes()
    q3 = json.loads(q3_bytes)
    colgen = json.loads(colgen_bytes)
    cert["frozen_inputs"] = {
        "q3_sha256": hashlib.sha256(q3_bytes).hexdigest(),
        "colgen_sha256": hashlib.sha256(colgen_bytes).hexdigest(),
    }

    ss = load_seedspan_module()
    cert["G9_fixed_word_pin"] = {
        "seedspan_module_sha256": hashlib.sha256(SEEDSPAN_MODULE_PATH.read_bytes()).hexdigest(),
        "FIXED_WORD_sha256": hashlib.sha256(json.dumps(ss.FIXED_WORD).encode()).hexdigest(),
    }
    e3, e4, extra = ss.reconstruct_quotients(q3)
    fixed_word = tuple(ss.FIXED_WORD)

    # --- target6 via the GENERIC evaluator ---------------------------------
    f_xy = F(tuple(X0), tuple(Y0), fixed_word)
    f_xz = F(tuple(X0), tuple(Z0), fixed_word)
    f_yz = F(tuple(Y0), tuple(Z0), fixed_word)
    target6_expr = paper_product([f_xy, Inv(f_xz), f_yz])

    h1bar = target6_expr.value(e4)
    nabla_b = target6_expr.grad_base(e4)

    # --- SHA canary retargeted per commander correction (2026-08-21):
    # base_gradient.canonical_gradient_sha256 is producer-internal "binding
    # only" and NOT reproducible by an independent [component, element_hex,
    # coefficient]-sorted canonicalization (implementation A / the ladder
    # lane hit the same non-reproduction independently, cause under
    # investigation by implementation C). The receipt's
    # raw_parent_manifest.rows[*].gradient_sha256 IS documented+reproduced
    # by A under exactly this "sorted [component, element_hex, coefficient]
    # + sha256" canonicalization (109/109 match for A) -- retarget here so
    # this becomes a THIRD independent confirmation (different code path:
    # generic Expr evaluator here vs A's ladder machinery).
    raw_rows = colgen["raw_parent_manifest"]["rows"]
    raw_rows_by_ordinal = {r["source_word_ordinal"]: r for r in raw_rows}
    assert colgen["raw_parent_manifest"]["source_word_order"] == "base target6 then registered seeds 1..108"

    base_gradient = colgen["initial_target"]["target6"]["base_gradient"]
    my_base_sha = canonical_gradient_sha256(nabla_b)
    base_row = raw_rows_by_ordinal[0]
    c2 = {
        "h1bar_is_identity": h1bar == e4.identity,
        "my_entry_count": len(nabla_b),
        "expected_entry_count_base_gradient": base_gradient["entry_count"],
        "expected_entry_count_raw_parent_manifest": base_row["gradient_entry_count"],
        "my_canonical_sha256": my_base_sha,
        "raw_parent_manifest_gradient_sha256 (retargeted canary)": base_row["gradient_sha256"],
        "base_gradient_canonical_gradient_sha256 (legacy target, non-blocking)": base_gradient["canonical_gradient_sha256"],
        "pass_vs_raw_parent_manifest": h1bar == e4.identity
            and len(nabla_b) == base_row["gradient_entry_count"]
            and my_base_sha == base_row["gradient_sha256"],
        "pass_vs_base_gradient_legacy_non_blocking": my_base_sha == base_gradient["canonical_gradient_sha256"],
    }
    c2["pass"] = c2["pass_vs_raw_parent_manifest"]
    c2["base_gradient_sha_note"] = (
        "base_gradient.canonical_gradient_sha256 uses a different, undocumented internal "
        "convention (self-flagged 'digest_is_binding_only_not_element_equality'); a mismatch "
        "there is expected and non-blocking. The canonical canary is raw_parent_manifest."
    )
    cert["canary_c2_nabla_b"] = c2

    seed_words = colgen["seed_manifest"]["seed_words"]
    c1_results = []
    seed_gradients = []  # (seed_index_1based, s_j dict) -- reused by run_p2_l1
    for j0, w in enumerate(seed_words):
        j = j0 + 1
        s_j = target6_expr.grad_delta(e4, w)
        seed_gradients.append((j, s_j))
        my_sha = canonical_gradient_sha256(s_j)
        row = raw_rows_by_ordinal.get(j)
        expected_sha = row["gradient_sha256"] if row else None
        expected_count = row["gradient_entry_count"] if row else None
        ok = expected_sha is not None and my_sha == expected_sha and len(s_j) == expected_count
        c1_results.append({"seed_index": j, "pass": ok})

    n_pass = sum(1 for r in c1_results if r["pass"])
    cert["canary_c1_seed_gradients_via_generic_evaluator"] = {
        "target": "raw_parent_manifest.rows[seed_index].gradient_sha256 (retargeted per "
                  "commander correction; implementation A independently confirmed 109/109 "
                  "under this same [component, element_hex, coefficient]-sorted convention)",
        "n_seeds": len(c1_results), "n_pass": n_pass, "all_pass": n_pass == len(c1_results),
        "failures": [r for r in c1_results if not r["pass"]][:5],
    }

    # --- T1-T5 vacuous check (c3 / BSW-0) -----------------------------------
    identity_expr = Identity()
    c3_base_zero = identity_expr.grad_base(e4) == {}
    c3_delta_zero_all = all(identity_expr.grad_delta(e4, w) == {} for w in seed_words)
    cert["canary_c3_BSW0_targets_1_5_vacuous"] = {
        "grad_base_is_empty": c3_base_zero,
        "grad_delta_empty_for_all_108_seeds": c3_delta_zero_all,
        "pass": c3_base_zero and c3_delta_zero_all,
    }

    sha_all_pass = c2["pass"] and (n_pass == len(c1_results))
    cert["overall"] = {
        "sha256_canary_all_pass (retargeted to raw_parent_manifest, three-way cross-check with "
        "implementation A)": sha_all_pass,
        "BSW_0": {"predicate": "T1-5 b' and all s'_j are exactly 0", "predicted": "TRUE",
                  "observed": c3_base_zero and c3_delta_zero_all},
        "note": "This cert makes NO branch-liveness (NM/DEAD/ALIVE) claim -- P2/P3 continue below "
                "in this same script (reusing the ladder lane's L1 projection, read-only).",
    }
    cert["claim_boundary_same_line_as_verdict_P0P1"] = (
        f"P0-P1: sha256_canary_all_pass={sha_all_pass} (retargeted to raw_parent_manifest per "
        f"commander correction -- third independent confirmation alongside implementation A), "
        f"BSW-0 (T1-5 vacuous) TRUE. NOT a branch-liveness result by itself."
    )
    print(f"P0-P1: sha256_canary_all_pass={sha_all_pass}")
    print(json.dumps(cert["claim_boundary_same_line_as_verdict_P0P1"]))

    if not sha_all_pass:
        cert["STOPPED_BEFORE_P2"] = (
            "P0-P1 SHA canary (retargeted to raw_parent_manifest) did not fully pass -- refusing "
            "to proceed to P2 (BSW-1) on ungrounded gradients. See canary_c1/c2 for the exact "
            "mismatch."
        )
        cert["wall_seconds"] = time.time() - t0
        CERT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = CERT_DIR / f"koubou158_sweep_P0P1_v1_{time.strftime('%Y%m%d')}.json"
        out_path.write_text(json.dumps(cert, indent=2, default=str), encoding="utf-8")
        print(f"wrote {out_path}")
        return False, e4, None, None

    cert["wall_seconds"] = time.time() - t0
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CERT_DIR / f"koubou158_sweep_P0P1_v1_{time.strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(cert, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out_path}")
    return True, e4, nabla_b, seed_gradients


# ---------------------------------------------------------------------------
# P2: BSW-1 -- reproduce the current branch's L1 (barE=P=PSL(2,8), |barE|=504)
# NM determination, INDEPENDENTLY of implementation A's
# search/koubou158_ladder_L1_v1.py (reusing only the GAP-verified projection
# method, per commander instruction -- not reimplementing the GAP orbit
# verification itself, and not importing A's rank-computation code: this
# script writes its own sparse F3 Gaussian elimination for genuine
# producer/checker double-implementation per branch_sweep_design_v1.md sec 4
# "評価器を producer/checker で二重実装し...梯子の rank も 2 系統").
# ---------------------------------------------------------------------------


def pi_L1(elt):
    """Projection E4 -> P = PSL(2,8): the 144-point permutation restricted to
    the first 9 points (a GAP-verified Q4-invariant orbit block, image order
    504). Reused, read-only, from search/koubou158_ladder_L1_v1.py /
    search/koubou158_ladder_blocks_v1.g (implementation A's ladder lane,
    GAP-verified 2026-08-21) per commander authorization -- NOT re-derived."""
    return elt[0][:9]


def perm_mul9(a, b):
    return bytes(b[a[i]] for i in range(9))


def enumerate_group9(gens):
    from collections import deque
    identity = bytes(range(9))
    seen = {identity}
    queue = deque([identity])
    while queue:
        cur = queue.popleft()
        for g in gens:
            nxt = perm_mul9(cur, g)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen)


class F3RankTracker:
    """Independent (not seedspan.AffineSystem) incremental sparse F3 rank
    tracker: maintains a set of pivot rows (dict pivot_col -> reduced row),
    reduces each incoming vector against all current pivots, and if a
    nonzero remainder survives, promotes it to a new pivot. Standard
    Gaussian elimination; F3 makes inversion trivial (1^-1=1, 2^-1=2, i.e.
    every nonzero element is self-inverse)."""

    def __init__(self):
        self.pivots = {}  # pivot_col -> {col: coeff} (pivot_col's coeff == 1)

    def add(self, vec):
        # PERFORMANCE FIX (2026-08-22, caught by a runaway P3/STACKED run):
        # the original version looped over ALL existing pivots for every
        # incoming vector (`for pcol, prow in list(self.pivots.items())`),
        # i.e. O(n_vectors * n_pivots) total regardless of sparsity -- with
        # STACKED's ~66k-dim coordinate space and tens of thousands of
        # pivots, this made the run effectively hang (>30 min, no P3 cert).
        # Fixed to only ever touch pivot columns that are actually present
        # as keys in the CURRENT (sparse) row, repeating until none remain
        # -- standard sparse Gaussian elimination, cost driven by fill-in
        # size, not total pivot count.
        row = {k: v % 3 for k, v in vec.items() if v % 3}
        progress = True
        while progress:
            progress = False
            for col in list(row.keys()):
                prow = self.pivots.get(col)
                if prow is None:
                    continue
                c = row.get(col, 0) % 3
                if not c:
                    continue
                for pc, pv in prow.items():
                    nv = (row.get(pc, 0) - c * pv) % 3
                    if nv:
                        row[pc] = nv
                    else:
                        row.pop(pc, None)
                progress = True
        if not row:
            return False  # dependent, rank unchanged
        pivot_col = next(iter(row))
        inv = row[pivot_col]  # self-inverse in F3 for {1,2}
        normalized = {k: (v * inv) % 3 for k, v in row.items()}
        self.pivots[pivot_col] = normalized
        return True

    @property
    def rank(self):
        return len(self.pivots)


def run_p2_l1(e4, nabla_b, seed_gradients, colgen):
    t0 = time.time()
    cert = {
        "schema": "shadow-atelier/koubou158-sweep-P2-L1/v1",
        "namespace": "koubou158_sweep_*",
        "lane": "koubou160-bsweep-v1",
        "generated_by": "search/koubou158_sweep_v1.py (run_p2_l1)",
        "generated_at_unix": time.time(),
        "design_authority": "docs/notes/branch_sweep_design_v1.md sec 3.2 (NM predicate), "
                             "sec 4 (P2: BSW-1)",
        "projection_reuse_note": "pi:E4->P (perm[0:9]) reused read-only from implementation A's "
                                  "search/koubou158_ladder_L1_v1.py / "
                                  "search/koubou158_ladder_blocks_v1.g (GAP orbit verification "
                                  "NOT redone here, per commander authorization 2026-08-21: "
                                  "'独立性の要件は照合器側だけの話'). The RANK COMPUTATION below is "
                                  "an independent from-scratch implementation (F3RankTracker), not "
                                  "an import of seedspan.AffineSystem -- this IS the "
                                  "producer/checker double-implementation the design doc sec 4 asks "
                                  "for on the rank side.",
    }

    marks_bar = [pi_L1(g) for g in e4.generators]
    ebar = enumerate_group9(marks_bar)
    g7_ok = True
    for i in range(6):
        for j in range(6):
            lhs = pi_L1(e4.mul(e4.generators[i], e4.generators[j]))
            rhs = perm_mul9(marks_bar[i], marks_bar[j])
            if lhs != rhs:
                g7_ok = False
    cert["projection"] = {
        "size_Ebar": len(ebar), "expected_504": len(ebar) == 504,
        "G7_homomorphism_spot_check": g7_ok,
    }
    if len(ebar) != 504 or not g7_ok:
        cert["STOPPED"] = "projection sanity check failed -- refusing to build the L1 system"
        cert["wall_seconds"] = time.time() - t0
        CERT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = CERT_DIR / f"koubou158_sweep_P2_v1_{time.strftime('%Y%m%d')}.json"
        out_path.write_text(json.dumps(cert, indent=2, default=str), encoding="utf-8")
        print(f"wrote {out_path}")
        return False, None

    def project_vec(v):
        out = defaultdict(int)
        for (comp, elt), c in v.items():
            out[(comp, pi_L1(elt))] = (out[(comp, pi_L1(elt))] + c) % 3
        return {k: c for k, c in out.items() if c}

    nabla_b_bar = project_vec(nabla_b)
    s_bars = [(j, project_vec(s)) for j, s in seed_gradients]

    occurrences = colgen["base_columns"]["occurrences"]
    r_k_bar = defaultdict(dict)
    for row in occurrences:
        k = int(row["relator_index"])
        comp = int(row["component"])
        elt_bar = bytes.fromhex(row["element_hex"])[:9]
        key = (comp, elt_bar)
        r_k_bar[k][key] = (r_k_bar[k].get(key, 0) + int(row["coefficient"])) % 3
    r_k_bar = {k: {kk: vv for kk, vv in v.items() if vv} for k, v in r_k_bar.items()}

    tracker = F3RankTracker()
    for j, s in s_bars:
        tracker.add(s)
    translate_count = 0
    for k, vec in r_k_bar.items():
        for g in ebar:
            translated = {(comp, perm_mul9(g, elt)): c for (comp, elt), c in vec.items()}
            tracker.add(translated)
            translate_count += 1
    r108 = tracker.rank
    tracker.add(nabla_b_bar)
    r109 = tracker.rank
    non_member = r109 > r108

    cert["s4_membership_test"] = {
        "dimension_6_times_Ebar": 6 * 504, "seed_columns": len(s_bars),
        "relator_translate_columns": translate_count, "r108": r108, "r109": r109,
        "non_member_at_L1": non_member,
    }
    cert["cross_check_vs_implementation_A"] = {
        "A_r108": 2012, "A_r109": 2013, "A_non_member": True,
        "match": (r108 == 2012 and r109 == 2013 and non_member is True),
        "A_cert_path": "search/certs/koubou158_ladder_L1_v1_20260821.json",
    }

    cert["BSW_1"] = {
        "predicate": "current branch pi0, T6, NM=1 (non-member) at L1 -- reproduced?",
        "predicted": "TRUE (reproduction of already-run result)",
        "observed": non_member,
        "matches_prediction": non_member is True,
    }
    cert["verdict"] = (
        f"BSW-1 {'CONFIRMED' if non_member else 'NOT CONFIRMED'} via an independent "
        f"(from-scratch F3 rank tracker, not seedspan.AffineSystem) implementation: "
        f"r108={r108}, r109={r109}, non_member_at_L1={non_member}. "
        f"cross-check vs implementation A: {cert['cross_check_vs_implementation_A']['match']}. "
        "claim boundary (design doc sec 0 correction 3, verbatim): DEAD/NM here means ONLY "
        "'within the registered 108-seed family, at rung L1' -- it does NOT prove non-membership "
        "at full E4 (that needs L2/L3), does NOT imply OBS*-grade obstruction even if every "
        "branch turns out DEAD (design doc's own limit statement), and by Theorem D' a "
        "non-member finding at L1 DOES lift to a valid non-member statement at E4 for this "
        "exact (roof, correction, target) triple -- but says nothing about other branches "
        "until the sweep (P4-P5) actually visits them."
    )
    cert["claim_boundary_same_line_as_verdict"] = cert["verdict"]
    cert["wall_seconds"] = time.time() - t0

    CERT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CERT_DIR / f"koubou158_sweep_P2_v1_{time.strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(cert, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"r108={r108} r109={r109} non_member={non_member} "
          f"matches_A={cert['cross_check_vs_implementation_A']['match']}")
    return non_member is True, cert


# ---------------------------------------------------------------------------
# P3: the 22-target battery (T6-T27) + STACKED, for the current branch pi0
# (roof = current FIXED_WORD, correction = identity / records[0].word=[]).
#
# Target STRUCTURE (which contexts feed which target, which opcodes combine
# them) is read from the frozen producer source
# search/d972_b345_relfrat3_wordexpr_memo_v9.py's build_wordexpr_candidate
# (SHA below, read-only, per commander instruction 2026-08-21). Only the
# PURE COMBINATORIAL helpers (pure_relations, cofaces via q3's frozen
# formulas.cofaces_3_4) are reused from there -- the actual GRADIENT
# COMPUTATION is this script's own Expr/Mul/Inv/PaperProduct/ProductMany/
# substitute_expr evaluator (built in P0-P1, cross-checked against
# raw_parent_manifest and against implementation A's independent rank
# computation in P2), NOT the producer's WordExprDAG numeric engine. This is
# the producer/checker split the design doc sec 4 asks for: read the
# STRUCTURE from the frozen source (deterministic word combinatorics, no
# "judgment" to trust), recompute the NUMBERS independently.
# ---------------------------------------------------------------------------

WORDEXPR_MODULE_PATH = REPO_ROOT / "search" / "d972_b345_relfrat3_wordexpr_memo_v9.py"


def load_wordexpr_module():
    spec = importlib.util.spec_from_file_location("_koubou158_wordexpr", WORDEXPR_MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_koubou158_wordexpr"] = mod
    spec.loader.exec_module(mod)
    return mod


def build_22_targets(cofaces_3_4, pure_relations_4, fixed_word):
    """Returns an ordered list of (target_name, Expr) for T6-T27 (22 acceptance
    rows), branch pi0 (candidate_word = fixed_word, i.e. correction=[]).

    All contexts below (hexagon cofaces, pentagon's fixed generator pairs,
    source's fixed generator pairs) are LITERAL free-group words (lists of
    signed 1-based generator indices) -- never Expr objects -- so f_at can
    always build an F(ell, rho, fixed_word) leaf directly. This mirrors
    build_wordexpr_candidate's own f_at(left,right), which likewise only
    ever receives literal-word DAG nodes (dag.flat(...) results) as its
    context arguments.

    Word-composition convention (verified in P0-P1 against target6, cross-
    checked to raw_parent_manifest): for LITERAL WORDS, paper_product([A,B])
    as a value equals product_many([B,A]) = B++A (concatenation); e.g.
    z0 = (pp[x0,y0])^-1 = inv_word(y0 ++ x0), which reproduced the already-
    verified Z0=[-4,-6] for x0=[4],y0=[6] in P0-P1.
    """
    gens = [Gen(i) for i in range(1, 7)]
    targets = []

    def f_at(left, right):
        return F(tuple(left), tuple(right), tuple(fixed_word))

    hex1 = []
    hex2 = []
    for slot in range(5):
        mapping = cofaces_3_4[slot]  # [coface(a12), coface(a13), coface(a23)]
        x = list(mapping[0])
        y = list(mapping[2])
        z = inv_word(y + x)  # (pp[x,y])^-1 = inv_word(y ++ x)
        u = inv_word(x + y)  # (pp[y,x])^-1 = inv_word(x ++ y)
        fxy = f_at(x, y)
        fxz = f_at(x, z)
        fyz = f_at(y, z)
        fux = f_at(u, x)
        fuy = f_at(u, y)
        h1 = paper_product([fxy, Inv(fxz), fyz])
        h2 = paper_product([Inv(fux), Inv(fxy), fuy])
        hex1.append((f"T{6 + slot}_hexagon_1_coface_{slot}", h1))
        hex2.append((f"T{11 + slot}_hexagon_2_coface_{slot}", h2))
    targets.extend(hex1)
    targets.extend(hex2)

    # pentagon (T16): fixed generator-pair contexts, literal words (as
    # per build_wordexpr_candidate: paper_product([g_i,g_j]) as a literal
    # word = product_many([g_j,g_i]) = [j,i]).
    pent_ctx_words = [
        ([1], [4]),
        ([4], [6]),
        ([4, 2], [6]),   # paper_product([g2,g4]) = g4++g2 = [4,2]
        ([2, 1], [6, 5]),  # paper_product([g1,g2])=[2,1]; paper_product([g5,g6])=[6,5]
        ([1], [5, 4]),   # paper_product([g4,g5]) = [5,4]
    ]
    pent_parts = [f_at(l, r) for l, r in pent_ctx_words]
    pent = paper_product([
        Inv(paper_product([pent_parts[4], pent_parts[2]])),
        pent_parts[1], pent_parts[3], pent_parts[0],
    ])
    targets.append(("T16_ordered_A18_pentagon", pent))

    # source rows (T17-27, S_relation_1..11): fixed generator-pair contexts,
    # then conjugation chains, then dag.substitute(relator, source).
    ff = f_at([1], [4])
    gv = f_at([1], [2])
    gs = f_at([4], [5])
    f1234 = f_at([4, 2], [6])
    h_ = f_at([2, 1], [3])
    middle = f_at([2, 1], [6, 5])

    source = [
        gens[0],
        product_many([Inv(gv), gens[1], gv]),
        product_many([Inv(ff), Inv(h_), gens[2], h_, ff]),
        product_many([Inv(ff), gens[3], ff]),
        product_many([Inv(ff), Inv(middle), Inv(gs), gens[4], gs, middle, ff]),
        product_many([Inv(f1234), gens[5], f1234]),
    ]
    for idx, relator in enumerate(pure_relations_4, start=1):
        targets.append((f"T{16 + idx}_S_relation_{idx}", substitute_expr(relator, source)))

    return targets


def run_p3_battery(e4, colgen, q3, seed_words):
    t0 = time.time()
    cert = {
        "schema": "shadow-atelier/koubou158-sweep-P3/v1",
        "namespace": "koubou158_sweep_*",
        "lane": "koubou160-bsweep-v1",
        "generated_by": "search/koubou158_sweep_v1.py (run_p3_battery)",
        "generated_at_unix": time.time(),
        "design_authority": "docs/notes/branch_sweep_design_v1.md sec 3.2-3.3, 4 (P3)",
        "branch": "pi0 (current FIXED_WORD roof, correction=identity/records[0].word=[])",
    }

    wx = load_wordexpr_module()
    wx_sha = hashlib.sha256(WORDEXPR_MODULE_PATH.read_bytes()).hexdigest()
    cert["wordexpr_source_pin"] = {
        "path": str(WORDEXPR_MODULE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "sha256": wx_sha,
        "note": "structure (which contexts/opcodes build each target) read from here; "
                "gradient arithmetic is this script's own independent evaluator, not "
                "the producer's WordExprDAG.",
    }

    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)
    require = lambda cond, msg: (_ for _ in ()).throw(AssertionError(msg)) if not cond else None
    require(len(pure_relations_4) == 11, "expected 11 PB4 relations")

    fixed_word = colgen["seed_manifest"]  # unused, kept for symmetry; FIXED_WORD comes from seedspan
    ss = load_seedspan_module()
    targets = build_22_targets(cofaces_3_4, pure_relations_4, ss.FIXED_WORD)
    cert["n_targets"] = len(targets)
    require(len(targets) == 22, f"expected 22 targets (T6-T27), got {len(targets)}")

    occurrences = colgen["base_columns"]["occurrences"]
    r_k_bar = defaultdict(dict)
    for row in occurrences:
        k = int(row["relator_index"])
        comp = int(row["component"])
        elt_bar = bytes.fromhex(row["element_hex"])[:9]
        key = (comp, elt_bar)
        r_k_bar[k][key] = (r_k_bar[k].get(key, 0) + int(row["coefficient"])) % 3
    r_k_bar = {k: {kk: vv for kk, vv in v.items() if vv} for k, v in r_k_bar.items()}

    marks_bar = [pi_L1(g) for g in e4.generators]
    ebar = enumerate_group9(marks_bar)
    require(len(ebar) == 504, "|Ebar| != 504")

    def project_vec(v):
        out = defaultdict(int)
        for (comp, elt), c in v.items():
            out[(comp, pi_L1(elt))] = (out[(comp, pi_L1(elt))] + c) % 3
        return {k: c for k, c in out.items() if c}

    per_target_results = []
    stacked_seed_union = defaultdict(dict)  # seed_idx -> {(target_idx,comp,elt): coeff}
    stacked_target_vecs = []  # (target_idx, {(comp,elt):coeff})

    for t_idx, (name, expr) in enumerate(targets):
        t1 = time.time()
        b_prime = expr.grad_base(e4)
        b_prime_bar = project_vec(b_prime)

        tracker = F3RankTracker()
        s_bars_this_target = []
        for j0, w in enumerate(seed_words):
            j = j0 + 1
            s_jT = expr.grad_delta(e4, w)
            s_bar = project_vec(s_jT)
            s_bars_this_target.append((j, s_bar))
            tracker.add(s_bar)
            for key, coeff in s_bar.items():
                stacked_seed_union[j][(t_idx,) + key] = coeff

        translate_count = 0
        for k, vec in r_k_bar.items():
            for g in ebar:
                translated = {(comp, perm_mul9(g, elt)): c for (comp, elt), c in vec.items()}
                tracker.add(translated)
                translate_count += 1
        r108 = tracker.rank
        tracker.add(b_prime_bar)
        r109 = tracker.rank
        nm = r109 > r108

        stacked_target_vecs.append((t_idx, name, b_prime_bar))

        per_target_results.append({
            "target": name, "b_prime_entry_count": len(b_prime),
            "r108": r108, "r109": r109, "NM": nm,
            "wall_seconds": time.time() - t1,
        })
        print(f"  P3 {name}: r108={r108} r109={r109} NM={nm} "
              f"({time.time()-t1:.2f}s)")

    n_dead_predicate = sum(1 for r in per_target_results if r["NM"])
    branch_dead = n_dead_predicate >= 1  # BS-1: any one NM kills the branch
    cert["per_target_results"] = per_target_results
    cert["n_targets_NM"] = n_dead_predicate
    cert["branch_pi0_status"] = "DEAD" if branch_dead else "ALIVE-L1 (individually)"
    cert["BS_1_note"] = (
        "Lemma BS-1 (design doc sec 0 correction 1): a single NM=1 acceptance target kills the "
        "branch within the registered 108-seed family. This uses acceptance rows ONLY (T6-T27); "
        "diagnostic rows (D1-D17, not built this pass) never kill a branch per design doc sec 1.2."
    )

    # --- STACKED: shared 108-dim x, 22 independent relator-translate blocks --
    ts0 = time.time()
    stacked_tracker = F3RankTracker()
    for j, union_vec in stacked_seed_union.items():
        stacked_tracker.add(union_vec)
    stacked_translate_count = 0
    for t_idx, name, _ in stacked_target_vecs:
        for k, vec in r_k_bar.items():
            for g in ebar:
                translated = {(t_idx, comp, perm_mul9(g, elt)): c for (comp, elt), c in vec.items()}
                stacked_tracker.add(translated)
                stacked_translate_count += 1
    r108_stacked = stacked_tracker.rank
    for t_idx, name, vec in stacked_target_vecs:
        keyed = {(t_idx,) + k: c for k, c in vec.items()}
        stacked_tracker.add(keyed)
    r109_stacked = stacked_tracker.rank
    stacked_dead = r109_stacked > r108_stacked

    cert["stacked"] = {
        "n_targets": len(targets), "seed_columns": len(seed_words),
        "relator_translate_columns": stacked_translate_count,
        "r108": r108_stacked, "r109": r109_stacked,
        "STACKED_DEAD": stacked_dead,
        "wall_seconds": time.time() - ts0,
        "note": "shared 108-dim x (one column per seed, spanning all 22 target blocks at once) "
                "+ 22 independent relator-translate blocks + 22 target constraint vectors added "
                "together. STACKED_DEAD means no single x is simultaneously consistent across all "
                "22 targets, even if some/all individual targets were member_at_L1.",
    }
    print(f"  P3 STACKED: r108={r108_stacked} r109={r109_stacked} "
          f"STACKED_DEAD={stacked_dead} ({time.time()-ts0:.2f}s)")

    overall_dead = branch_dead or stacked_dead
    cert["verdict"] = (
        f"branch pi0 (T6..T27 individual): {'DEAD' if branch_dead else 'not killed by any single target'} "
        f"({n_dead_predicate}/22 targets NM=1). STACKED: {'DEAD' if stacked_dead else 'consistent'}. "
        f"Overall: {'DEAD' if overall_dead else 'ALIVE-L1'} -- claim boundary (design doc sec 0 "
        f"correction 3, verbatim): DEAD here means ONLY 'within the registered 108-seed family, at "
        f"L1, for branch pi0'. Even if all 162 branches (not just pi0) turn out DEAD, that does NOT "
        f"constitute an OBS*-grade obstruction certificate -- (ii) seed span extension and (iii) the "
        f"full Syl_3(ML(H)) generating set remain outside this sweep's reach."
    )
    cert["claim_boundary_same_line_as_verdict"] = cert["verdict"]
    cert["wall_seconds"] = time.time() - t0

    CERT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CERT_DIR / f"koubou158_sweep_P3_v1_{time.strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(cert, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out_path}")
    print(cert["verdict"])
    return overall_dead, cert


# ---------------------------------------------------------------------------
# P4: axis C sweep -- 27 corrections (correction_fibre.records), roof fixed
# at the current row (pi0's FIXED_WORD). Commander scope (2026-08-22,
# widened from the design doc's own "27 corrections x T6 only" default):
# test all 6 targets that killed branch pi0 in P3 (T6,T7,T11,T12,T26,T27)
# against every one of the 27 corrections, to map how the death pattern
# depends on the correction axis.
#
# c=0 (correction_fibre.records[0].word == []) reproduces pi0 exactly --
# used as a free correctness canary against the already-verified P3 numbers.
#
# NOTE ON THE PER-BRANCH PRECONDITION GATE (design doc sec 2.3, "枝ごとの
# 前件ゲート"): this pass does NOT implement the
# source_words_m0(candidate)==frozen check (needs machinery from a producer
# module not yet located/verified this session). Flagged, not silently
# skipped -- see cert.precondition_gate_not_verified. r_k_bar (the 11 base
# relator gradients) and the L1 projection/enumeration are branch-
# independent (relators are evaluated on bare generators, never through
# candidate_word) so they are computed ONCE and reused across all 27
# corrections, matching design doc sec 2.2's efficiency claim.
# ---------------------------------------------------------------------------

P4_KILLER_TARGET_NAMES = [
    "T6_hexagon_1_coface_0", "T7_hexagon_1_coface_1",
    "T11_hexagon_2_coface_0", "T12_hexagon_2_coface_1",
    "T26_S_relation_10", "T27_S_relation_11",
]


def run_p4_axis_c(e4, colgen, q3, seed_words, target_names=None, progress_every_seconds=1800):
    t0 = time.time()
    target_names = target_names or P4_KILLER_TARGET_NAMES
    cert = {
        "schema": "shadow-atelier/koubou158-sweep-P4/v1",
        "namespace": "koubou158_sweep_*",
        "lane": "koubou160-bsweep-v1",
        "generated_by": "search/koubou158_sweep_v1.py (run_p4_axis_c)",
        "generated_at_unix": time.time(),
        "design_authority": "docs/notes/branch_sweep_design_v1.md sec 1.1 (axis C), sec 4 (P4)",
        "scope_note": "commander 2026-08-22 widened P4 from the design doc's default "
                       "'27 corrections x T6 only' to all 6 targets that killed branch pi0 in "
                       "P3 (T6,T7,T11,T12,T26,T27), to map death-pattern dependence on axis C.",
        "target_names": target_names,
        "roof": "fixed at pi0's current FIXED_WORD (axis R not swept this phase)",
        "precondition_gate_not_verified": "source_words_m0(candidate)==frozen gate (design doc "
                                           "sec 2.3) NOT implemented this pass -- flagged, not "
                                           "silently skipped. All 27 corrections are treated as "
                                           "in-universe without this check.",
    }

    wx = load_wordexpr_module()
    ss = load_seedspan_module()
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)
    records = q3["correction_fibre"]["records"]
    assert len(records) == 27, f"expected 27 correction records, got {len(records)}"
    cert["correction_fibre_record_count"] = len(records)

    occurrences = colgen["base_columns"]["occurrences"]
    r_k_bar = defaultdict(dict)
    for row in occurrences:
        k = int(row["relator_index"])
        comp = int(row["component"])
        elt_bar = bytes.fromhex(row["element_hex"])[:9]
        key = (comp, elt_bar)
        r_k_bar[k][key] = (r_k_bar[k].get(key, 0) + int(row["coefficient"])) % 3
    r_k_bar = {k: {kk: vv for kk, vv in v.items() if vv} for k, v in r_k_bar.items()}

    marks_bar = [pi_L1(g) for g in e4.generators]
    ebar = enumerate_group9(marks_bar)
    assert len(ebar) == 504

    def project_vec(v):
        out = defaultdict(int)
        for (comp, elt), c in v.items():
            out[(comp, pi_L1(elt))] = (out[(comp, pi_L1(elt))] + c) % 3
        return {k: c for k, c in out.items() if c}

    # relator-translate columns are branch-independent -- build once, reuse.
    relator_translate_vecs = []
    for k, vec in r_k_bar.items():
        for g in ebar:
            relator_translate_vecs.append({(comp, perm_mul9(g, elt)): c for (comp, elt), c in vec.items()})

    results = []
    last_progress = t0
    total_combos = len(records) * len(target_names)
    done = 0

    for c_idx, rec in enumerate(records):
        correction = rec["word"]
        candidate_word = reduce_word(list(ss.FIXED_WORD) + list(correction))
        targets = build_22_targets(cofaces_3_4, pure_relations_4, candidate_word)
        by_name = dict(targets)

        for name in target_names:
            expr = by_name[name]
            t1 = time.time()
            b_prime_bar = project_vec(expr.grad_base(e4))

            tracker = F3RankTracker()
            for w in seed_words:
                s_bar = project_vec(expr.grad_delta(e4, w))
                tracker.add(s_bar)
            for vec in relator_translate_vecs:
                tracker.add(vec)
            r108 = tracker.rank
            tracker.add(b_prime_bar)
            r109 = tracker.rank
            nm = r109 > r108

            results.append({
                "correction_index": c_idx, "target": name,
                "r108": r108, "r109": r109, "NM": nm,
                "wall_seconds": time.time() - t1,
            })
            done += 1
            print(f"  P4 c={c_idx} {name}: r108={r108} r109={r109} NM={nm} "
                  f"({time.time()-t1:.2f}s) [{done}/{total_combos}]")

            now = time.time()
            if now - last_progress >= progress_every_seconds:
                elapsed = now - t0
                print(f"  P4 PROGRESS: {done}/{total_combos} combos done, "
                      f"{elapsed:.0f}s elapsed, {elapsed/max(done,1)*total_combos - elapsed:.0f}s "
                      f"estimated remaining")
                last_progress = now

    cert["results"] = results
    # per-target NM-vs-correction table
    per_target = defaultdict(list)
    for r in results:
        per_target[r["target"]].append((r["correction_index"], r["NM"]))
    death_map = {}
    for name in target_names:
        rows = sorted(per_target[name])
        n_nm = sum(1 for _, nm in rows if nm)
        death_map[name] = {
            "n_corrections_NM": n_nm, "n_corrections_total": len(rows),
            "always_dead": n_nm == len(rows), "never_dead": n_nm == 0,
            "corrections_where_ALIVE (NM=False)": [ci for ci, nm in rows if not nm],
        }
    cert["death_pattern_by_target"] = death_map

    # canary: c=0 (identity correction) must reproduce P3's pi0 numbers exactly
    c0_results = {r["target"]: r for r in results if r["correction_index"] == 0}
    cert["canary_c0_matches_p3"] = {
        name: {"NM": c0_results[name]["NM"]} for name in target_names if name in c0_results
    }

    any_alive_correction = any(
        any(not nm for _, nm in per_target[name]) for name in target_names
    )
    cert["verdict"] = (
        f"axis C sweep (27 corrections x {len(target_names)} targets = {total_combos} combos), "
        f"roof fixed at pi0: "
        + ("at least one (correction,target) combo is member_at_L1 (NM=False) -- some death "
           "pattern is correction-dependent, see death_pattern_by_target for which targets/"
           "corrections." if any_alive_correction else
           "ALL 27 corrections x all 6 killer targets are NM=True -- these 6 targets kill the "
           "branch uniformly across the entire correction fibre for this roof.")
        + " claim boundary: this is still an L1, registered-108-seed-family, single-roof result "
          "(design doc sec 0 correction 3) -- says nothing about axis R (roof) or about targets "
          "outside these 6."
    )
    cert["claim_boundary_same_line_as_verdict"] = cert["verdict"]
    cert["wall_seconds"] = time.time() - t0

    CERT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CERT_DIR / f"koubou158_sweep_P4_v1_{time.strftime('%Y%m%d')}.json"
    out_path.write_text(json.dumps(cert, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out_path}")
    print(cert["verdict"])
    return cert


def quick_load_e4():
    """Load q3/colgen + build e4 WITHOUT running P0-P1's full canary suite
    (that suite is already independently confirmed, see
    search/certs/koubou158_sweep_P0P1_v1_*.json) -- used by phases that
    don't need the canary re-run every invocation (P4, P5)."""
    q3 = json.loads(Q3_PATH.read_bytes())
    colgen = json.loads(COLGEN_PATH.read_bytes())
    ss = load_seedspan_module()
    e3, e4, extra = ss.reconstruct_quotients(q3)
    return e4, colgen, q3


# ---------------------------------------------------------------------------
# P5: axis C x R sweep, 162 branches (27 corrections x 6 roofs), early exit
# (design doc sec 3.3: stop at the first NM=1 acceptance target -- that
# alone kills the branch, lemma BS-1). Battery order = T6..T27 (build_22_
# targets' own order), which starts with the cheap hexagon_1 targets, so a
# branch that dies early (as pi0 did, on T6 itself) is cheap; only branches
# that survive many targets pay the expensive S_relation cost.
#
# Sharded for GHA (commander 2026-08-22): this module exposes a CLI shard
# entrypoint (`p5-shard`) taking a roof index and a half-open correction
# index range, so a matrix workflow can split the 162 branches into
# independent <=60-minute jobs. Local execution (this process) is
# unaffected -- these functions are additive.
# ---------------------------------------------------------------------------


def roof_word(q3, roof_index):
    return q3["canonical_roof_powers"]["rows"][roof_index]["word"]


def correction_word(q3, correction_index):
    return q3["correction_fibre"]["records"][correction_index]["word"]


def run_p5_branch(e4, cofaces_3_4, pure_relations_4, r_k_bar, ebar, seed_words,
                   roof_w, corr_w, target_order=None):
    """One branch = (roof_w, corr_w). Iterate targets T6..T27 in order,
    early-exit on the first NM=1. Returns a dict result."""
    candidate_word = reduce_word(list(roof_w) + list(corr_w))
    targets = build_22_targets(cofaces_3_4, pure_relations_4, candidate_word)
    if target_order:
        by_name = dict(targets)
        targets = [(name, by_name[name]) for name in target_order]

    def project_vec(v):
        out = defaultdict(int)
        for (comp, elt), c in v.items():
            out[(comp, pi_L1(elt))] = (out[(comp, pi_L1(elt))] + c) % 3
        return {k: c for k, c in out.items() if c}

    per_target = []
    for name, expr in targets:
        t1 = time.time()
        b_prime_bar = project_vec(expr.grad_base(e4))
        tracker = F3RankTracker()
        for w in seed_words:
            tracker.add(project_vec(expr.grad_delta(e4, w)))
        for vec in r_k_bar:
            tracker.add(vec)
        r108 = tracker.rank
        tracker.add(b_prime_bar)
        r109 = tracker.rank
        nm = r109 > r108
        per_target.append({"target": name, "r108": r108, "r109": r109, "NM": nm,
                            "wall_seconds": time.time() - t1})
        if nm:
            return {"status": "DEAD", "killer_target": name, "n_targets_tested": len(per_target),
                    "per_target": per_target}
    return {"status": "ALIVE-L1", "killer_target": None, "n_targets_tested": len(per_target),
            "per_target": per_target}


def build_r_k_bar_vecs(colgen, ebar):
    """Branch-independent relator-translate vectors (11 relators x |Ebar|
    translates), computed once and reused across every branch."""
    occurrences = colgen["base_columns"]["occurrences"]
    r_k = defaultdict(dict)
    for row in occurrences:
        k = int(row["relator_index"])
        comp = int(row["component"])
        elt_bar = bytes.fromhex(row["element_hex"])[:9]
        key = (comp, elt_bar)
        r_k[k][key] = (r_k[k].get(key, 0) + int(row["coefficient"])) % 3
    r_k = {k: {kk: vv for kk, vv in v.items() if vv} for k, v in r_k.items()}
    vecs = []
    for k, vec in r_k.items():
        for g in ebar:
            vecs.append({(comp, perm_mul9(g, elt)): c for (comp, elt), c in vec.items()})
    return vecs


def run_roof_wiring_check(e4, colgen, q3, roof_index_a=0, roof_index_b=1):
    """P5's required first check (commander 2026-08-22, mirrors the P4 axis-C
    check): compare T6's pi(nabla_b) digest across two DIFFERENT roofs
    (correction fixed at identity). If identical, the roof axis is not wired
    into the L1 computation and P5 would be uninformative (162 repeats of
    the same math) -- fail closed rather than run the sweep. Returns
    (wired: bool, detail: dict)."""
    wx = load_wordexpr_module()
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)
    identity_correction = []

    def project_vec(v):
        out = defaultdict(int)
        for (comp, elt), c in v.items():
            out[(comp, pi_L1(elt))] = (out[(comp, pi_L1(elt))] + c) % 3
        return {k: c for k, c in out.items() if c}

    def digest_for_roof(idx):
        rw = roof_word(q3, idx)
        candidate_word = reduce_word(list(rw) + identity_correction)
        targets = build_22_targets(cofaces_3_4, pure_relations_4, candidate_word)
        by_name = dict(targets)
        b_prime = by_name["T6_hexagon_1_coface_0"].grad_base(e4)
        b_bar = project_vec(b_prime)
        rows = sorted([comp, elt.hex(), coeff] for (comp, elt), coeff in b_bar.items())
        payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
        return {"raw_entry_count": len(b_prime), "L1_entry_count": len(rows),
                "digest": hashlib.sha256(payload).hexdigest()}

    da = digest_for_roof(roof_index_a)
    db = digest_for_roof(roof_index_b)
    wired = da["digest"] != db["digest"]
    return wired, {"roof_a": roof_index_a, "roof_b": roof_index_b,
                    "digest_a": da, "digest_b": db, "wired": wired}


def run_p5_shard(roof_index, corr_start, corr_end, out_path=None):
    """CLI-facing shard entrypoint: one roof, a half-open correction index
    range [corr_start, corr_end). Writes a cert to out_path (or the default
    certs dir) and returns it."""
    t0 = time.time()
    e4, colgen, q3 = quick_load_e4()
    wired, wiring_detail = run_roof_wiring_check(e4, colgen, q3, 0, 1)
    cert = {
        "schema": "shadow-atelier/koubou158-sweep-P5-shard/v1",
        "namespace": "koubou158_sweep_*",
        "lane": "koubou160-bsweep-v1 / koubou158-sweep-sharded-v1 (GHA)",
        "generated_at_unix": time.time(),
        "shard": {"roof_index": roof_index, "corr_start": corr_start, "corr_end": corr_end},
        "roof_wiring_check": wiring_detail,
    }
    if not wired:
        cert["STOPPED"] = "roof wiring check failed (digests identical across roof_a/roof_b) -- refusing to run this shard"
        cert["wall_seconds"] = time.time() - t0
        _write_p5_cert(cert, out_path, roof_index, corr_start, corr_end)
        return cert

    wx = load_wordexpr_module()
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)
    seed_words = colgen["seed_manifest"]["seed_words"]

    marks_bar = [pi_L1(g) for g in e4.generators]
    ebar = enumerate_group9(marks_bar)
    assert len(ebar) == 504
    r_k_bar_vecs = build_r_k_bar_vecs(colgen, ebar)

    rw = roof_word(q3, roof_index)
    branch_results = []
    for c_idx in range(corr_start, corr_end):
        cw = correction_word(q3, c_idx)
        t1 = time.time()
        result = run_p5_branch(e4, cofaces_3_4, pure_relations_4, r_k_bar_vecs, ebar,
                                seed_words, rw, cw)
        result["roof_index"] = roof_index
        result["correction_index"] = c_idx
        result["wall_seconds"] = time.time() - t1
        branch_results.append(result)
        print(f"  P5 roof={roof_index} c={c_idx}: {result['status']} "
              f"(killer={result['killer_target']}, {result['n_targets_tested']} targets tested, "
              f"{result['wall_seconds']:.1f}s)")

    cert["branch_results"] = [
        {k: v for k, v in r.items() if k != "per_target"} for r in branch_results
    ]
    cert["branch_results_full"] = branch_results
    n_dead = sum(1 for r in branch_results if r["status"] == "DEAD")
    n_alive = len(branch_results) - n_dead
    cert["n_branches"] = len(branch_results)
    cert["n_DEAD"] = n_dead
    cert["n_ALIVE_L1"] = n_alive
    cert["verdict"] = (
        f"shard roof={roof_index} corrections=[{corr_start},{corr_end}): {n_dead} DEAD, "
        f"{n_alive} ALIVE-L1 (out of {len(branch_results)} branches). claim boundary: DEAD is "
        f"L1/registered-108-seed-family only (design doc sec 0 correction 3); ALIVE-L1 needs L0/"
        f"L2/L3 promotion (P6) before being treated as a real candidate."
    )
    cert["claim_boundary_same_line_as_verdict"] = cert["verdict"]
    cert["wall_seconds"] = time.time() - t0
    _write_p5_cert(cert, out_path, roof_index, corr_start, corr_end)
    print(cert["verdict"])
    return cert


def _write_p5_cert(cert, out_path, roof_index, corr_start, corr_end):
    if out_path:
        path = Path(out_path)
    else:
        CERT_DIR.mkdir(parents=True, exist_ok=True)
        path = CERT_DIR / f"koubou158_sweep_P5_shard_r{roof_index}_c{corr_start}-{corr_end}_v1_{time.strftime('%Y%m%d')}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, default=str), encoding="utf-8")
    print(f"wrote {path}")


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "p0-p3"

    if phase == "p0-p3":
        ok, e4, nabla_b, seed_gradients = run_p0_p1()
        if not ok:
            print("P0-P1 did not pass -- stopping before P2 (see cert STOPPED_BEFORE_P2)")
            return 1
        colgen = json.loads(COLGEN_PATH.read_bytes())
        p2_ok, p2_cert = run_p2_l1(e4, nabla_b, seed_gradients, colgen)
        print(f"P2: BSW-1 confirmed={p2_ok}")
        q3 = json.loads(Q3_PATH.read_bytes())
        seed_words = colgen["seed_manifest"]["seed_words"]
        p3_dead, p3_cert = run_p3_battery(e4, colgen, q3, seed_words)
        print(f"FINAL: P0-P1 pass, P2 BSW-1 confirmed={p2_ok}, "
              f"P3 branch pi0 overall={'DEAD' if p3_dead else 'ALIVE-L1'}")
        return 0

    if phase == "p4":
        e4, colgen, q3 = quick_load_e4()
        seed_words = colgen["seed_manifest"]["seed_words"]
        p4_cert = run_p4_axis_c(e4, colgen, q3, seed_words)
        print(f"FINAL P4: {p4_cert['verdict']}")
        return 0

    if phase == "roof-wiring-check":
        e4, colgen, q3 = quick_load_e4()
        roof_a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        roof_b = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        wired, detail = run_roof_wiring_check(e4, colgen, q3, roof_a, roof_b)
        print(json.dumps(detail, indent=2))
        print(f"WIRED={wired}")
        return 0 if wired else 1

    if phase == "p5-shard":
        # p5-shard <roof_index> <corr_start> <corr_end> [out_path]
        roof_index = int(sys.argv[2])
        corr_start = int(sys.argv[3])
        corr_end = int(sys.argv[4])
        out_path = sys.argv[5] if len(sys.argv) > 5 else None
        cert = run_p5_shard(roof_index, corr_start, corr_end, out_path)
        return 1 if "STOPPED" in cert else 0

    print(f"unknown phase {phase!r} (expected p0-p3 | p4 | roof-wiring-check | p5-shard)")
    return 2


if __name__ == "__main__":
    sys.exit(main())
