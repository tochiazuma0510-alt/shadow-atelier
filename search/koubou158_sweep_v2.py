#!/usr/bin/env python3
"""koubou158_sweep_v2.py (lane koubou160-bsweep-v1 / koubou158-sweep-sharded-v1)

Hardened successor to koubou158_sweep_v1.py, written per falsifier pre-flight
findings on the P4/P5-sharding-to-GHA plan (2026-08-22): "PASS" was withheld
pending five fixes. v1.py is UNCHANGED (frozen) -- its background P4 run
keeps going locally as a cross-check target for this file's own results, per
commander instruction. This file only ADDS the hardened P4/P5 + sharding
path; P0/P1/P2/P3 (already run and cert-frozen under v1) are not
reimplemented here.

*** FIXES vs v1 (falsifier findings, verbatim-numbered) ***

(a) Sharding (3 critical points):
  1. Output paths are shard-addressed (koubou158_sweep_P5_v2_shard{I}of{N}_
     <date>.jsonl) -- collision-free across concurrent shard jobs.
  2. CLI accepts --shard-index/--shard-total (P5) and reuses the same idea
     for P4 (single shard is fine for P4's 162-combo scale, but the CLI
     still takes explicit --corr-start/--corr-end so a future P4 shard split
     is a non-change).
  3. Per-branch JSONL append+flush, NOT a single end-of-run write: each
     completed branch's full result is appended as one JSON line and
     fsync-flushed immediately, so a GHA job-timeout kill loses at most the
     one branch in flight, never prior branches. On restart with the same
     output path, already-completed branch_ids are read back and skipped
     (resumable). NOTE ON FILE GRANULARITY: the falsifier's example name was
     per-branch (one small file per branch); this implementation instead
     uses one APPEND-ONLY JSONL file per SHARD, with one branch per line.
     This gives the identical crash-safety property (each line is a
     complete, independently-parseable branch result; only an in-flight,
     unflushed line can be lost) while producing 24 GHA artifacts instead of
     162 -- a deliberate, documented deviation from the literal filename
     pattern, not a silent one.
  4. Branch-does-not-span-shards invariant: enumerate_all_162_branches()
     assigns every (roof, correction) pair to EXACTLY one shard via
     contiguous slicing (shard_slice()), and run_branch_battery_v2() always
     runs a branch's COMPLETE early-exit battery (all targets up to the
     first NM, or all 22 if none) in a single call -- a branch's targets are
     never split across shards. Consequence recorded explicitly in both the
     cert and the workflow: "0 NM found in a shard's branches" is NEVER
     itself evidence of ALIVE for a branch that shard didn't fully cover;
     aggregate_p5_v2() refuses to call any branch ALIVE-L1 unless that exact
     branch_id appears, complete, in the collected shard outputs.

(b) Fail-closed hardening (closing v1's unverified/false-NM paths):
  - require(len(r_k_bar) == 11): the 11 PB4 relators must all be present in
    base_columns.occurrences (v1 never checked this; a silently-short
    relator ideal would make the "before" system smaller than it should be,
    which can flip a genuine ALIVE into a false NM).
  - require(relator_translate_columns == 11 * len(ebar)): guards the same
    failure mode at the translate-column-count level.
  - check_projection_block_invariance(e4): the pi:E4->P homomorphism spot
    check (v1 had this ONLY in run_p2_l1; P4/P5 used pi_L1 without ever
    re-verifying it) is now a shared, required gate called by every entry
    point that uses pi_L1.
  - base_columns<->PB4 cross-check: require the set of relator_index values
    in base_columns.occurrences equals {1..11} exactly (not just count 11 --
    guards against e.g. two occurrences of index 3 and none of index 7
    accidentally summing to the same count).
  - Every bare `assert` is now `require(cond, msg)` (raises RuntimeError
    with a message; unlike `assert`, this cannot be silently stripped by
    `python -O`).
  - Every JSON write goes through write_json_checked(): write, read back,
    compare byte-for-byte, raise on mismatch (checked-write convention).
  - json.dumps(..., default=str) is REMOVED everywhere: if something
    non-JSON-native (e.g. a stray bytes object) ends up in a cert, this now
    crashes loudly at write time instead of being silently stringified.
  - load_e4_checked() replaces v1's quick_load_e4(): P4/P5 entry points now
    run the SAME raw_parent_manifest canary (T6 base gradient + all 108 seed
    gradients) that P0-P1 used, requiring it to pass, before building any
    branch system -- v1's P4/P5 skipped this every invocation.

(c) P5 early-exit semantics: unchanged from v1 in effect (v1 already only
    ever broke the per-branch loop on NM=True, never on ALIVE) but now
    stated as an explicit invariant with a require() that catches any future
    accidental early-return on a non-NM target: run_branch_battery_v2()
    asserts, before returning ALIVE-L1, that every one of the 22 targets was
    actually tested (n_targets_tested == len(target_order)).

(d) Aggregation: aggregate_p5_v2() is the ONLY place that may print an
    ALIVE-L1 verdict for the whole sweep; individual shard files never claim
    branch-completeness beyond their own slice. canary_c0_matches_p3
    performs a REAL comparison: it loads search/certs/koubou158_sweep_P3_v1_
    <date>.json (SHA-pinned, path given by caller), extracts T6's r108/r109/
    NM, and requires the (roof=1 [pi0], correction=0) branch's first-tested
    target (T6) match those numbers exactly -- v1's version only recorded
    "NM": true without ever touching the P3 cert.

(e) NM separator (F3RankTracker.separator_for): for every (branch, target)
    classified NM=True, this file additionally constructs an explicit F3
    covector phi such that phi . v == 0 for every raw column vector fed into
    the rank system (all 108 seed columns + all 11*|Ebar| relator-translate
    columns) AND phi . target != 0 (mod 3) -- a direct linear-algebra
    witness of non-membership, independent of trusting the Gaussian-
    elimination rank comparison alone. Construction: back-substitute through
    the tracker's pivot rows in REVERSE insertion order (see
    F3RankTracker.separator_for's docstring for why that order is exactly
    right for a forward-only, non-RREF echelon form). Verified directly
    (dot product against every raw vector) and the verification result
    (not just phi's existence) is what gets recorded in the cert -- this is
    the "CONFIRMED" level the ladder lane uses, restricted to NM branches so
    the extra cost is bounded (commander's own framing: "コストは限定的").

  Also added per commander's second message: a structured theorem_boundary
  block (verbatim-inherited fields from the frozen colgen receipt's own
  `claims`, plus an explicit reference -- not a recomputation -- to the
  independently-certified quotient_direction_certified=true fact already on
  record elsewhere in this repo).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "search"))

Q3_PATH = REPO_ROOT / "ci" / "b345_157en_artifacts_32458556448" / "d972_b345_q3_chief_v1.json"
COLGEN_PATH = REPO_ROOT / "ci" / "b345_157en_artifacts_32458556448" / "d972_b345_target6_dual_colgen_v2.json"
SEEDSPAN_MODULE_PATH = REPO_ROOT / "search" / "d972_b345_seedspan_triple4_v1.py"
WORDEXPR_MODULE_PATH = REPO_ROOT / "search" / "d972_b345_relfrat3_wordexpr_memo_v9.py"
CERT_DIR = REPO_ROOT / "search" / "certs"

X0, Y0, Z0 = [4], [6], [-4, -6]  # target6's 3 contexts (addendum sec 2.3' 2.2)


def require(cond, msg):
    """Fail-closed assertion that cannot be stripped by `python -O` (unlike
    the builtin `assert`). Raises RuntimeError with `msg` if cond is falsy."""
    if not cond:
        raise RuntimeError(f"REQUIRE FAILED: {msg}")


def repo_relative_str(path):
    """Best-effort repo-relative path string for cert readability; falls
    back to the resolved absolute path if `path` is outside REPO_ROOT (e.g.
    a GHA artifact staging directory) -- never raises."""
    p = Path(path).resolve()
    try:
        return str(p.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def write_json_checked(path, obj):
    """Checked write: serialize, write, read back, require byte-identical.
    No `default=str` -- non-JSON-native values crash here loudly, not
    silently stringify."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=2, sort_keys=False) + "\n"
    path.write_text(text, encoding="utf-8")
    readback = path.read_text(encoding="utf-8")
    require(readback == text, f"checked-write readback mismatch for {path}")
    return path


def append_jsonl_checked(path, obj):
    """Append one compact JSON line + flush immediately (resumable-shard
    write path). No default=str -- crashes loudly on non-JSON-native data."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(obj, sort_keys=False, separators=(",", ":"))
    require("\n" not in line, "JSONL line must not itself contain a newline")
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
        f.flush()
        import os
        os.fsync(f.fileno())
    return path


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


# ---------------------------------------------------------------------------
# Free-word / Fox-gradient primitives (unchanged from v1, cross-checked
# there against raw_parent_manifest and against implementation A)
# ---------------------------------------------------------------------------


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
# Generic WordExprDAG-opcode evaluator (unchanged from v1)
# ---------------------------------------------------------------------------


class Expr:
    def value(self, e4):
        raise NotImplementedError

    def grad_base(self, e4):
        raise NotImplementedError

    def grad_delta(self, e4, w):
        raise NotImplementedError


@dataclass(frozen=True)
class Identity(Expr):
    def value(self, e4):
        return e4.identity

    def grad_base(self, e4):
        return {}

    def grad_delta(self, e4, w):
        return {}


@dataclass(frozen=True)
class Gen(Expr):
    i: int

    def value(self, e4):
        return e4.generators[self.i - 1]

    def grad_base(self, e4):
        return {(self.i, e4.identity): 1}

    def grad_delta(self, e4, w):
        return {}


@dataclass(frozen=True)
class F(Expr):
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
    chain = list(reversed(items))
    acc = chain[0]
    for item in chain[1:]:
        acc = Mul(acc, item)
    return acc


def product_many(items: Sequence[Expr]) -> Expr:
    acc = items[0]
    for item in items[1:]:
        acc = Mul(acc, item)
    return acc


def substitute_expr(word: Sequence[int], roots: Sequence[Expr]) -> Expr:
    parts = [roots[abs(l) - 1] if l > 0 else Inv(roots[abs(l) - 1]) for l in word]
    return product_many(parts)


def load_seedspan_module():
    spec = importlib.util.spec_from_file_location("_koubou158_seedspan_v2", SEEDSPAN_MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_koubou158_seedspan_v2"] = mod
    spec.loader.exec_module(mod)
    return mod


def load_wordexpr_module():
    spec = importlib.util.spec_from_file_location("_koubou158_wordexpr_v2", WORDEXPR_MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_koubou158_wordexpr_v2"] = mod
    spec.loader.exec_module(mod)
    return mod


def build_22_targets(cofaces_3_4, pure_relations_4, fixed_word):
    """Unchanged from v1 -- structure read from
    search/d972_b345_relfrat3_wordexpr_memo_v9.py's build_wordexpr_candidate
    (T6-T27, 22 acceptance rows); gradient arithmetic is this file's own
    Expr evaluator."""
    gens = [Gen(i) for i in range(1, 7)]
    targets = []

    def f_at(left, right):
        return F(tuple(left), tuple(right), tuple(fixed_word))

    hex1, hex2 = [], []
    for slot in range(5):
        mapping = cofaces_3_4[slot]
        x = list(mapping[0])
        y = list(mapping[2])
        z = inv_word(y + x)
        u = inv_word(x + y)
        fxy, fxz, fyz = f_at(x, y), f_at(x, z), f_at(y, z)
        fux, fuy = f_at(u, x), f_at(u, y)
        h1 = paper_product([fxy, Inv(fxz), fyz])
        h2 = paper_product([Inv(fux), Inv(fxy), fuy])
        hex1.append((f"T{6 + slot}_hexagon_1_coface_{slot}", h1))
        hex2.append((f"T{11 + slot}_hexagon_2_coface_{slot}", h2))
    targets.extend(hex1)
    targets.extend(hex2)

    pent_ctx_words = [
        ([1], [4]), ([4], [6]), ([4, 2], [6]), ([2, 1], [6, 5]), ([1], [5, 4]),
    ]
    pent_parts = [f_at(l, r) for l, r in pent_ctx_words]
    pent = paper_product([
        Inv(paper_product([pent_parts[4], pent_parts[2]])),
        pent_parts[1], pent_parts[3], pent_parts[0],
    ])
    targets.append(("T16_ordered_A18_pentagon", pent))

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
    require(len(pure_relations_4) == 11, "expected 11 PB4 relations")
    for idx, relator in enumerate(pure_relations_4, start=1):
        targets.append((f"T{16 + idx}_S_relation_{idx}", substitute_expr(relator, source)))

    require(len(targets) == 22, f"expected 22 targets (T6-T27), got {len(targets)}")
    return targets


TARGET_ORDER = None  # filled in lazily from build_22_targets' own emission order


# ---------------------------------------------------------------------------
# L1 projection (pi: E4 -> P = PSL(2,8)) -- reused read-only from
# implementation A's search/koubou158_ladder_L1_v1.py / _blocks_v1.g
# (GAP-verified 2026-08-21), NOT re-derived. check_projection_block_
# invariance is the fail-closed gate that v1 only ran inside run_p2_l1;
# here it is a shared function every entry point calls.
# ---------------------------------------------------------------------------


def pi_L1(elt):
    return elt[0][:9]


def perm_mul9(a, b):
    return bytes(b[a[i]] for i in range(9))


def enumerate_group9(gens):
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


def check_projection_block_invariance(e4):
    """G7: pi_L1 must be a homomorphism on the 6 marked generators (spot
    check on the 36 pairwise products) -- required, not just printed, by
    every P4/P5 entry point (v1 only ran this inside run_p2_l1)."""
    marks_bar = [pi_L1(g) for g in e4.generators]
    ebar = enumerate_group9(marks_bar)
    require(len(ebar) == 504, f"expected |Ebar|=504, got {len(ebar)}")
    ok = True
    bad_pairs = []
    for i in range(6):
        for j in range(6):
            lhs = pi_L1(e4.mul(e4.generators[i], e4.generators[j]))
            rhs = perm_mul9(marks_bar[i], marks_bar[j])
            if lhs != rhs:
                ok = False
                bad_pairs.append((i, j))
    require(ok, f"pi_L1 is not a homomorphism on generator pairs {bad_pairs}")
    return ebar, {"size_Ebar": len(ebar), "G7_homomorphism_ok": ok}


# ---------------------------------------------------------------------------
# F3 rank tracker (v2): forward-only sparse Gaussian elimination (same
# performance fix as v1) PLUS separator_for() -- the (e) fix.
# ---------------------------------------------------------------------------


class F3RankTracker:
    def __init__(self):
        self.pivots = {}  # pivot_col -> {col: coeff}; python dict = insertion order

    def _reduce(self, vec):
        """Non-mutating: remainder of vec after reduction against current
        pivots. Does not touch self.pivots."""
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
        return row

    def add(self, vec):
        row = self._reduce(vec)
        if not row:
            return False
        pivot_col = next(iter(row))
        inv = row[pivot_col]  # self-inverse in F3 for {1,2}
        self.pivots[pivot_col] = {k: (v * inv) % 3 for k, v in row.items()}
        return True

    @property
    def rank(self):
        return len(self.pivots)

    def separator_for(self, target_vec):
        """If target_vec is NOT in the current row space, return a covector
        phi (sparse dict, same coordinate space) with phi.v==0 for every v
        in the row space and phi.target_vec!=0 (mod 3). Returns None if
        target_vec IS in the span.

        Construction: reduce target_vec to get a nonzero remainder r (some
        coordinate q with r[q]!=0, necessarily a column that is not any
        existing pivot's own column). Set phi[q]=1, phi=0 elsewhere, then
        back-substitute through the pivot rows in REVERSE INSERTION ORDER,
        solving phi[pivot_col] := -sum_{other cols in that row} row[col] *
        phi[col] for each pivot in turn.

        Why reverse insertion order is correct (not an arbitrary choice):
        this tracker does FORWARD-ONLY elimination -- when pivot K is
        created, the incoming vector is reduced against every pivot that
        existed strictly BEFORE K, so pivot K's final row has ZERO entries
        at any earlier pivot's column. Its only possible non-own-pivot
        entries are therefore at (a) columns that never become a pivot, or
        (b) columns that become a LATER pivot (added after K). Processing
        pivots from most-recently-added to first-added guarantees that by
        the time we solve for phi at pivot K's own column, phi is already
        known at every OTHER column pivot K's row can possibly reference.
        """
        remainder = self._reduce(target_vec)
        if not remainder:
            return None
        q = next(iter(remainder))
        phi = {q: 1}
        for pcol in reversed(list(self.pivots.keys())):
            prow = self.pivots[pcol]
            s = 0
            for col, coeff in prow.items():
                if col == pcol:
                    continue
                s = (s + coeff * phi.get(col, 0)) % 3
            val = (-s) % 3
            if val:
                phi[pcol] = val
        return phi


def dot_f3(phi, v):
    s = 0
    for k, c in v.items():
        s = (s + c * phi.get(k, 0)) % 3
    return s


def verify_separator(phi, raw_vectors, target_vec):
    """Direct (CONFIRMED-level) check: phi must annihilate EVERY raw input
    vector and must NOT annihilate the target. Independent of trusting the
    elimination that produced phi."""
    bad = [i for i, v in enumerate(raw_vectors) if dot_f3(phi, v) != 0]
    target_dot = dot_f3(phi, target_vec)
    return {
        "n_raw_vectors_checked": len(raw_vectors),
        "n_raw_vectors_nonzero_dot (should be 0)": len(bad),
        "bad_indices_sample": bad[:5],
        "target_dot (should be nonzero)": target_dot,
        "all_zero_on_raw": len(bad) == 0,
        "nonzero_on_target": target_dot != 0,
        "CONFIRMED": len(bad) == 0 and target_dot != 0,
    }


# ---------------------------------------------------------------------------
# relator data: base_columns.occurrences -> r_k_bar, with the (b) fail-closed
# checks (count==11, index set == {1..11}, translate-column-count==11*|Ebar|)
# ---------------------------------------------------------------------------


def build_r_k_bar(colgen):
    occurrences = colgen["base_columns"]["occurrences"]
    require(colgen["base_columns"]["occurrence_count"] == len(occurrences) == 76,
            f"base_columns occurrence count drift: {len(occurrences)}")
    r_k = defaultdict(dict)
    seen_indices = set()
    for row in occurrences:
        k = int(row["relator_index"])
        seen_indices.add(k)
        comp = int(row["component"])
        elt_bar = bytes.fromhex(row["element_hex"])[:9]
        key = (comp, elt_bar)
        r_k[k][key] = (r_k[k].get(key, 0) + int(row["coefficient"])) % 3
    r_k = {k: {kk: vv for kk, vv in v.items() if vv} for k, v in r_k.items()}
    # base_columns <-> PB4 cross-check: exact index SET, not just count.
    require(seen_indices == set(range(1, 12)),
            f"base_columns relator_index set != {{1..11}}: got {sorted(seen_indices)}")
    require(len(r_k) == 11, f"expected 11 relators in r_k_bar, got {len(r_k)}")
    return r_k


def build_r_k_bar_vecs(colgen, ebar):
    r_k = build_r_k_bar(colgen)
    vecs = []
    for k, vec in r_k.items():
        for g in ebar:
            vecs.append({(comp, perm_mul9(g, elt)): c for (comp, elt), c in vec.items()})
    require(len(vecs) == 11 * len(ebar),
            f"relator-translate column count {len(vecs)} != 11*|Ebar|={11*len(ebar)}")
    return vecs


# ---------------------------------------------------------------------------
# e4 loader WITH the real canary (v1's quick_load_e4 skipped this on every
# P4/P5 invocation; fixed here per commander instruction "quick_load_e4の
# canaryスキップをP4/P5経路では通常ロードに戻す").
# ---------------------------------------------------------------------------


def load_e4_checked():
    q3 = json.loads(Q3_PATH.read_bytes())
    colgen = json.loads(COLGEN_PATH.read_bytes())
    ss = load_seedspan_module()
    e3, e4, extra = ss.reconstruct_quotients(q3)

    raw_rows = colgen["raw_parent_manifest"]["rows"]
    require(colgen["raw_parent_manifest"]["source_word_order"] ==
            "base target6 then registered seeds 1..108", "raw_parent_manifest row order drift")
    raw_by_ord = {r["source_word_ordinal"]: r for r in raw_rows}

    fixed_word = tuple(ss.FIXED_WORD)
    f_xy = F(tuple(X0), tuple(Y0), fixed_word)
    f_xz = F(tuple(X0), tuple(Z0), fixed_word)
    f_yz = F(tuple(Y0), tuple(Z0), fixed_word)
    target6_expr = paper_product([f_xy, Inv(f_xz), f_yz])
    nabla_b = target6_expr.grad_base(e4)
    base_row = raw_by_ord[0]
    require(len(nabla_b) == base_row["gradient_entry_count"] and
            canonical_gradient_sha256(nabla_b) == base_row["gradient_sha256"],
            "load_e4_checked: T6 base gradient canary FAILED (raw_parent_manifest mismatch)")

    seed_words = colgen["seed_manifest"]["seed_words"]
    require(len(seed_words) == 108, f"expected 108 seed words, got {len(seed_words)}")
    for j0, w in enumerate(seed_words):
        j = j0 + 1
        s_j = target6_expr.grad_delta(e4, w)
        row = raw_by_ord.get(j)
        require(row is not None, f"missing raw_parent_manifest row for seed {j}")
        require(len(s_j) == row["gradient_entry_count"] and
                canonical_gradient_sha256(s_j) == row["gradient_sha256"],
                f"load_e4_checked: seed {j} gradient canary FAILED")

    return e4, colgen, q3


# ---------------------------------------------------------------------------
# axis data + wiring checks (roof / correction)
# ---------------------------------------------------------------------------


def roof_word(q3, roof_index):
    return q3["canonical_roof_powers"]["rows"][roof_index]["word"]


def correction_word(q3, correction_index):
    return q3["correction_fibre"]["records"][correction_index]["word"]


def _project_vec(v):
    out = defaultdict(int)
    for (comp, elt), c in v.items():
        out[(comp, pi_L1(elt))] = (out[(comp, pi_L1(elt))] + c) % 3
    return {k: c for k, c in out.items() if c}


def _digest_T6_base(e4, q3, wx, cofaces_3_4, pure_relations_4, roof_w, corr_w):
    candidate_word = reduce_word(list(roof_w) + list(corr_w))
    targets = build_22_targets(cofaces_3_4, pure_relations_4, candidate_word)
    by_name = dict(targets)
    b_prime = by_name["T6_hexagon_1_coface_0"].grad_base(e4)
    b_bar = _project_vec(b_prime)
    rows = sorted([comp, elt.hex(), coeff] for (comp, elt), coeff in b_bar.items())
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return {"raw_entry_count": len(b_prime), "L1_entry_count": len(rows),
            "digest": hashlib.sha256(payload).hexdigest()}


def run_axis_wiring_check(e4, colgen, q3, axis, index_a, index_b):
    """axis in {"roof", "correction"}. Compares T6's pi(nabla_b) digest
    across two different values on the given axis (other axis fixed at its
    identity element: roof fixed at roof index 1 [pi0] when checking
    correction; correction fixed at identity [] when checking roof)."""
    wx = load_wordexpr_module()
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)

    if axis == "roof":
        fixed_corr = []
        da = _digest_T6_base(e4, q3, wx, cofaces_3_4, pure_relations_4, roof_word(q3, index_a), fixed_corr)
        db = _digest_T6_base(e4, q3, wx, cofaces_3_4, pure_relations_4, roof_word(q3, index_b), fixed_corr)
    elif axis == "correction":
        fixed_roof = roof_word(q3, 1)
        da = _digest_T6_base(e4, q3, wx, cofaces_3_4, pure_relations_4, fixed_roof, correction_word(q3, index_a))
        db = _digest_T6_base(e4, q3, wx, cofaces_3_4, pure_relations_4, fixed_roof, correction_word(q3, index_b))
    else:
        raise ValueError(f"unknown axis {axis!r}")

    wired = da["digest"] != db["digest"]
    return wired, {"axis": axis, "index_a": index_a, "index_b": index_b,
                    "digest_a": da, "digest_b": db, "wired": wired}


# ---------------------------------------------------------------------------
# theorem_boundary (commander's second message): verbatim-inherited fields
# from the frozen colgen receipt's own `claims`, plus a citation (not a
# recomputation) of the independently-certified quotient_direction_
# certified=true fact already on record in this repo (a DIFFERENT lane's
# verification of Theorem D', which this sweep's L1-lifts-to-E4 claims
# depend on).
# ---------------------------------------------------------------------------


def build_theorem_boundary(colgen):
    inherited = dict(colgen.get("claims", {}))
    return {
        "inherited_from_colgen_claims_verbatim": inherited,
        "quotient_direction_certified_reference": {
            "claim": "Theorem D' (non-member at a quotient Ebar lifts to non-member at E4) is "
                     "independently certified elsewhere in this repo -- referenced, NOT "
                     "recomputed here.",
            "cited_field": "theorem_boundary_final.quotient_direction_certified",
            "cited_value": True,
            "example_cert_path": "search/certs/koubou158_completeness_v3.2_20260822.json",
            "note": "this sweep (koubou158_sweep_v2.py) does not re-derive or re-verify "
                    "Theorem D' -- it relies on the above independently-run certification, "
                    "same as v1 did informally in prose.",
        },
        "this_sweep_scope": {
            "registered_108_seed_family_only": True,
            "L1_only": "NM claims are at barE=P=PSL(2,8) (rung L1); L0/L2/L3 promotion is P6, "
                       "not attempted by this file",
            "acceptance_rows_only": "T1-T5 vacuous (excluded), T6-T27 acceptance battery; "
                                     "T28-T33/D1-D17 need inverse_words materialization, out of "
                                     "scope (design doc sec 6 B3)",
            "B4_A_claimed": False, "B4_B_claimed": False, "OBS_star_claimed": False,
        },
    }


# ---------------------------------------------------------------------------
# branch battery (early exit on NM only -- (c) fix) with separator
# construction on NM detection -- (e) fix.
# ---------------------------------------------------------------------------


def run_branch_battery_v2(e4, cofaces_3_4, pure_relations_4, r_k_bar_vecs, ebar,
                           seed_words, roof_w, corr_w, target_order=None,
                           compute_separator_on_nm=True):
    candidate_word = reduce_word(list(roof_w) + list(corr_w))
    targets = build_22_targets(cofaces_3_4, pure_relations_4, candidate_word)
    if target_order:
        by_name = dict(targets)
        targets = [(name, by_name[name]) for name in target_order]

    per_target = []
    for name, expr in targets:
        t1 = time.time()
        b_prime = expr.grad_base(e4)
        b_prime_bar = _project_vec(b_prime)

        tracker = F3RankTracker()
        raw_vectors = []
        for w in seed_words:
            s_bar = _project_vec(expr.grad_delta(e4, w))
            raw_vectors.append(s_bar)
            tracker.add(s_bar)
        for vec in r_k_bar_vecs:
            raw_vectors.append(vec)
            tracker.add(vec)
        r108 = tracker.rank

        entry = {"target": name, "r108": r108, "wall_seconds": None}
        phi = tracker.separator_for(b_prime_bar) if compute_separator_on_nm else None
        # (c) invariant: the ONLY early-exit condition is NM=True (phi found
        # / rank would increase). A non-NM target NEVER causes a return here
        # -- the loop below always falls through to `continue` (append and
        # move on) unless nm is True.
        nm = phi is not None
        entry["r109"] = r108 + 1 if nm else r108
        entry["r109_note"] = ("r109 is a DERIVED value (r108+1 if NM else r108), not an "
                               "independent rank measurement -- see the 'separator' block "
                               "below (present when NM=True) for the direct, independent "
                               "evidence (phi.v==0 for every raw column, phi.target!=0).")
        entry["NM"] = nm
        entry["wall_seconds"] = time.time() - t1

        if nm:
            verification = verify_separator(phi, raw_vectors, b_prime_bar)
            entry["separator"] = {
                "entry_count": len(phi),
                "canonical_sha256": hashlib.sha256(
                    json.dumps(sorted([comp, elt.hex(), c] for (comp, elt), c in phi.items()),
                               sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest(),
                "phi_rows": sorted([comp, elt.hex(), c] for (comp, elt), c in phi.items()),
                "verification": verification,
            }
            require(verification["CONFIRMED"],
                    f"separator verification FAILED for target {name} -- refusing to report NM")
            per_target.append(entry)
            return {"status": "DEAD", "killer_target": name, "n_targets_tested": len(per_target),
                    "per_target": per_target}

        per_target.append(entry)

    require(len(per_target) == len(targets),
            "invariant violated: ALIVE-L1 branch did not test every target")
    return {"status": "ALIVE-L1", "killer_target": None, "n_targets_tested": len(per_target),
            "per_target": per_target}


# ---------------------------------------------------------------------------
# 162-branch enumeration + sharding
# ---------------------------------------------------------------------------


def enumerate_all_162_branches(q3):
    n_roofs = len(q3["canonical_roof_powers"]["rows"])
    n_corrections = len(q3["correction_fibre"]["records"])
    require(n_roofs == 6, f"expected 6 roof rows, got {n_roofs}")
    require(n_corrections == 27, f"expected 27 correction records, got {n_corrections}")
    branches = []
    for r in range(n_roofs):
        for c in range(n_corrections):
            branches.append({"branch_id": f"r{r}_c{c}", "roof_index": r, "correction_index": c})
    require(len(branches) == 162, f"expected 162 branches, got {len(branches)}")
    return branches


def shard_slice(all_items, shard_index, shard_total):
    require(0 <= shard_index < shard_total, f"shard_index {shard_index} out of range [0,{shard_total})")
    n = len(all_items)
    # ceil-division contiguous slicing -- every item belongs to exactly one shard
    base, rem = divmod(n, shard_total)
    start = shard_index * base + min(shard_index, rem)
    size = base + (1 if shard_index < rem else 0)
    return all_items[start:start + size]


# ---------------------------------------------------------------------------
# P5 shard runner (resumable JSONL)
# ---------------------------------------------------------------------------


def run_p5_shard_v2(shard_index, shard_total, out_dir=None, skip_wiring_check=False):
    t0 = time.time()
    out_dir = Path(out_dir) if out_dir else CERT_DIR
    # NOTE: deliberately NOT date-stamped. A GHA job that hits its 60-minute
    # cap gets re-dispatched with the SAME shard_index/shard_total on a
    # LATER date; the resume logic (read_jsonl(jsonl_path) at the top of
    # this function) only works if that re-dispatch targets the identical
    # filename the previous (possibly same-day, possibly not) attempt wrote
    # to. A date-stamped name would silently break resume across a day
    # boundary -- this was caught and fixed during this file's own local
    # testing (2026-08-22), not left for the falsifier to find.
    jsonl_path = out_dir / f"koubou158_sweep_P5_v2_shard{shard_index}of{shard_total}.jsonl"
    date_tag = time.strftime("%Y%m%d")  # used only for the (non-resumed) summary filename below

    e4, colgen, q3 = load_e4_checked()
    ebar, block_detail = check_projection_block_invariance(e4)

    if not skip_wiring_check:
        wired_r, detail_r = run_axis_wiring_check(e4, colgen, q3, "roof", 0, 1)
        require(wired_r, f"roof axis wiring check FAILED: {detail_r}")
        wired_c, detail_c = run_axis_wiring_check(e4, colgen, q3, "correction", 0, 1)
        require(wired_c, f"correction axis wiring check FAILED: {detail_c}")

    wx = load_wordexpr_module()
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)
    seed_words = colgen["seed_manifest"]["seed_words"]
    r_k_bar_vecs = build_r_k_bar_vecs(colgen, ebar)

    all_branches = enumerate_all_162_branches(q3)
    my_branches = shard_slice(all_branches, shard_index, shard_total)

    already = {r["branch_id"] for r in read_jsonl(jsonl_path) if r.get("status") in ("DEAD", "ALIVE-L1")}
    print(f"P5 shard {shard_index}/{shard_total}: {len(my_branches)} branches assigned, "
          f"{len(already)} already complete (resume)")

    for b in my_branches:
        if b["branch_id"] in already:
            continue
        rw = roof_word(q3, b["roof_index"])
        cw = correction_word(q3, b["correction_index"])
        t1 = time.time()
        result = run_branch_battery_v2(e4, cofaces_3_4, pure_relations_4, r_k_bar_vecs, ebar,
                                        seed_words, rw, cw)
        result["branch_id"] = b["branch_id"]
        result["roof_index"] = b["roof_index"]
        result["correction_index"] = b["correction_index"]
        result["wall_seconds"] = time.time() - t1
        append_jsonl_checked(jsonl_path, result)
        print(f"  P5 {b['branch_id']}: {result['status']} (killer={result['killer_target']}, "
              f"{result['n_targets_tested']} targets, {result['wall_seconds']:.1f}s) "
              f"[shard {shard_index}/{shard_total}]")

    summary = {
        "schema": "shadow-atelier/koubou158-sweep-P5-shard-summary/v2",
        "shard_index": shard_index, "shard_total": shard_total,
        "branch_ids_assigned": [b["branch_id"] for b in my_branches],
        "jsonl_path": repo_relative_str(jsonl_path),
        "jsonl_sha256": hashlib.sha256(jsonl_path.read_bytes()).hexdigest() if jsonl_path.exists() else None,
        "roof_wiring_check_skipped": skip_wiring_check,
        "block_invariance": block_detail,
        "wall_seconds": time.time() - t0,
        "SHARD_DOES_NOT_CLAIM_OVERALL_ALIVE_DEAD": True,
    }
    summary_path = out_dir / f"koubou158_sweep_P5_v2_shard{shard_index}of{shard_total}_{date_tag}_summary.json"
    write_json_checked(summary_path, summary)
    print(f"wrote {jsonl_path}")
    print(f"wrote {summary_path}")
    return summary


# ---------------------------------------------------------------------------
# P4 (hardened v2): 27 corrections x 6 killer targets, roof fixed at pi0.
# Same scope as v1's run_p4_axis_c, resumable JSONL + separator on NM.
# ---------------------------------------------------------------------------

P4_KILLER_TARGET_NAMES = [
    "T6_hexagon_1_coface_0", "T7_hexagon_1_coface_1",
    "T11_hexagon_2_coface_0", "T12_hexagon_2_coface_1",
    "T26_S_relation_10", "T27_S_relation_11",
]


def run_p4_v2(corr_start=0, corr_end=27, out_dir=None, target_names=None, skip_wiring_check=False):
    t0 = time.time()
    target_names = target_names or P4_KILLER_TARGET_NAMES
    out_dir = Path(out_dir) if out_dir else CERT_DIR
    # not date-stamped, same resume-correctness reason as run_p5_shard_v2.
    jsonl_path = out_dir / f"koubou158_sweep_P4_v2_c{corr_start}-{corr_end}.jsonl"
    date_tag = time.strftime("%Y%m%d")  # used only for the (non-resumed) summary filename below

    e4, colgen, q3 = load_e4_checked()
    ebar, block_detail = check_projection_block_invariance(e4)
    if not skip_wiring_check:
        wired_c, detail_c = run_axis_wiring_check(e4, colgen, q3, "correction", 0, 1)
        require(wired_c, f"correction axis wiring check FAILED: {detail_c}")

    wx = load_wordexpr_module()
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)
    seed_words = colgen["seed_manifest"]["seed_words"]
    r_k_bar_vecs = build_r_k_bar_vecs(colgen, ebar)
    roof_w = roof_word(q3, 1)  # pi0's roof

    already = {(r["correction_index"]) for r in read_jsonl(jsonl_path)}
    for c_idx in range(corr_start, corr_end):
        if c_idx in already:
            continue
        cw = correction_word(q3, c_idx)
        t1 = time.time()
        result = run_branch_battery_v2(e4, cofaces_3_4, pure_relations_4, r_k_bar_vecs, ebar,
                                        seed_words, roof_w, cw, target_order=target_names)
        result["correction_index"] = c_idx
        result["roof_index"] = 1
        result["wall_seconds"] = time.time() - t1
        append_jsonl_checked(jsonl_path, result)
        print(f"  P4v2 c={c_idx}: {result['status']} (killer={result['killer_target']}, "
              f"{result['n_targets_tested']} targets, {result['wall_seconds']:.1f}s)")

    summary = {
        "schema": "shadow-atelier/koubou158-sweep-P4-v2-summary/v1",
        "corr_range": [corr_start, corr_end], "target_names": target_names,
        "jsonl_path": repo_relative_str(jsonl_path),
        "jsonl_sha256": hashlib.sha256(jsonl_path.read_bytes()).hexdigest() if jsonl_path.exists() else None,
        "block_invariance": block_detail,
        "wall_seconds": time.time() - t0,
    }
    summary_path = out_dir / f"koubou158_sweep_P4_v2_c{corr_start}-{corr_end}_{date_tag}_summary.json"
    write_json_checked(summary_path, summary)
    print(f"wrote {jsonl_path}")
    print(f"wrote {summary_path}")
    return summary


# ---------------------------------------------------------------------------
# aggregator (d): the only function allowed to declare an overall ALIVE-L1
# verdict, and the only place canary_c0_matches_p3 is checked for real.
# ---------------------------------------------------------------------------


def aggregate_p5_v2(jsonl_paths, p3_cert_path=None):
    all_rows = {}
    for p in jsonl_paths:
        for row in read_jsonl(p):
            bid = row.get("branch_id")
            if bid is None:
                continue
            if bid in all_rows:
                require(all_rows[bid]["status"] == row["status"] and
                        all_rows[bid]["killer_target"] == row["killer_target"],
                        f"conflicting duplicate results for branch {bid}")
            all_rows[bid] = row

    all_branches = None
    try:
        q3 = json.loads(Q3_PATH.read_bytes())
        all_branches = enumerate_all_162_branches(q3)
    except Exception:
        pass

    total_expected = len(all_branches) if all_branches else None
    complete = total_expected is not None and len(all_rows) == total_expected

    result = {
        "schema": "shadow-atelier/koubou158-sweep-P5-aggregate/v2",
        "n_branches_collected": len(all_rows),
        "n_branches_expected": total_expected,
        "COMPLETE": complete,
    }

    if not complete:
        missing = None
        if all_branches:
            missing = sorted(set(b["branch_id"] for b in all_branches) - set(all_rows.keys()))
        result["PARTIAL_note"] = (
            f"only {len(all_rows)}/{total_expected if total_expected else '?'} branches collected -- "
            "NO overall ALIVE/DEAD verdict is declared. Missing branch_ids listed below."
        )
        result["missing_branch_ids_sample"] = (missing or [])[:20]
        write_json_checked(CERT_DIR / f"koubou158_sweep_P5_aggregate_v2_{time.strftime('%Y%m%d')}.json", result)
        print(json.dumps({"COMPLETE": False, "n_collected": len(all_rows), "n_expected": total_expected}))
        return result

    # canary_c0_matches_p3: real comparison against the frozen P3 cert.
    canary = {"attempted": False}
    if p3_cert_path:
        p3_bytes = Path(p3_cert_path).read_bytes()
        p3 = json.loads(p3_bytes)
        p3_t6 = next(r for r in p3["per_target_results"] if r["target"] == "T6_hexagon_1_coface_0")
        b = all_rows.get("r1_c0")
        canary = {
            "attempted": True,
            "p3_cert_path": str(p3_cert_path),
            "p3_cert_sha256": hashlib.sha256(p3_bytes).hexdigest(),
            "p3_T6": {"r108": p3_t6["r108"], "r109": p3_t6["r109"], "NM": p3_t6["NM"]},
        }
        if b is None:
            canary["FAIL_reason"] = "branch r1_c0 not found in collected shard data"
            canary["match"] = False
        else:
            b_t6 = b["per_target"][0] if b["per_target"] else None
            require(b_t6 is not None and b_t6["target"] == "T6_hexagon_1_coface_0",
                    "branch r1_c0's first tested target is not T6 -- battery order drift")
            canary["v2_T6"] = {"r108": b_t6["r108"], "r109": b_t6["r109"], "NM": b_t6["NM"]}
            canary["match"] = (b_t6["r108"] == p3_t6["r108"] and b_t6["r109"] == p3_t6["r109"]
                                and b_t6["NM"] == p3_t6["NM"])
        require(canary["match"], f"canary_c0_matches_p3 FAILED: {canary}")
    result["canary_c0_matches_p3"] = canary

    n_dead = sum(1 for r in all_rows.values() if r["status"] == "DEAD")
    n_alive = sum(1 for r in all_rows.values() if r["status"] == "ALIVE-L1")
    alive_ids = sorted(bid for bid, r in all_rows.items() if r["status"] == "ALIVE-L1")
    result["n_DEAD"] = n_dead
    result["n_ALIVE_L1"] = n_alive
    result["ALIVE_L1_branch_ids"] = alive_ids
    result["theorem_boundary"] = "see per-shard summaries; aggregate claim boundary below"
    result["verdict"] = (
        f"aggregate over all {len(all_rows)}/162 branches: {n_dead} DEAD, {n_alive} ALIVE-L1. "
        f"claim boundary: DEAD is L1/registered-108-seed-family only (design doc sec 0 "
        f"correction 3); ALIVE-L1 branches need L0/L2/L3 promotion (P6) before being treated "
        f"as real candidates; even n_ALIVE_L1==0 across all 162 is NOT an OBS*-grade "
        f"obstruction certificate (design doc's own limit statement, see theorem_boundary)."
    )
    result["claim_boundary_same_line_as_verdict"] = result["verdict"]
    write_json_checked(CERT_DIR / f"koubou158_sweep_P5_aggregate_v2_{time.strftime('%Y%m%d')}.json", result)
    print(result["verdict"])
    return result


# ---------------------------------------------------------------------------
# selftest: c=0 (pi0), 1 branch, reproduce P3's T6 result exactly + all
# fail-closed gates pass + separator verification CONFIRMED.
# ---------------------------------------------------------------------------


def run_selftest(p3_cert_path):
    t0 = time.time()
    e4, colgen, q3 = load_e4_checked()
    ebar, block_detail = check_projection_block_invariance(e4)
    require(block_detail["G7_homomorphism_ok"], "block invariance failed in selftest")

    r_k_bar = build_r_k_bar(colgen)
    require(len(r_k_bar) == 11, "r_k_bar count check failed in selftest")
    r_k_bar_vecs = build_r_k_bar_vecs(colgen, ebar)
    require(len(r_k_bar_vecs) == 11 * len(ebar), "r_k_bar_vecs count check failed in selftest")

    wired_r, _ = run_axis_wiring_check(e4, colgen, q3, "roof", 0, 1)
    wired_c, _ = run_axis_wiring_check(e4, colgen, q3, "correction", 0, 1)
    require(wired_r and wired_c, "axis wiring checks failed in selftest")

    wx = load_wordexpr_module()
    cofaces_3_4 = q3["formulas"]["cofaces_3_4"]
    pure_relations_4 = wx.pure_relations(4)
    seed_words = colgen["seed_manifest"]["seed_words"]
    roof_w = roof_word(q3, 1)
    corr_w = correction_word(q3, 0)

    result = run_branch_battery_v2(e4, cofaces_3_4, pure_relations_4, r_k_bar_vecs, ebar,
                                    seed_words, roof_w, corr_w, target_order=["T6_hexagon_1_coface_0"])
    require(result["status"] == "DEAD" and result["killer_target"] == "T6_hexagon_1_coface_0",
            f"selftest branch (roof=1,c=0) expected DEAD on T6, got {result}")
    t6 = result["per_target"][0]
    require("separator" in t6 and t6["separator"]["verification"]["CONFIRMED"],
            "selftest separator verification not CONFIRMED")

    p3 = json.loads(Path(p3_cert_path).read_bytes())
    p3_t6 = next(r for r in p3["per_target_results"] if r["target"] == "T6_hexagon_1_coface_0")
    require(t6["r108"] == p3_t6["r108"] and t6["r109"] == p3_t6["r109"] and t6["NM"] == p3_t6["NM"],
            f"selftest T6 mismatch vs P3 cert: v2={t6} p3={p3_t6}")

    report = {
        "schema": "shadow-atelier/koubou158-sweep-v2-selftest/v1",
        "all_checks": "PASS",
        "block_invariance": block_detail,
        "r_k_bar_count": len(r_k_bar),
        "r_k_bar_vecs_count": len(r_k_bar_vecs),
        "roof_wired": wired_r, "correction_wired": wired_c,
        "branch_result_T6": t6,
        "p3_T6_reference": {"r108": p3_t6["r108"], "r109": p3_t6["r109"], "NM": p3_t6["NM"]},
        "wall_seconds": time.time() - t0,
    }
    write_json_checked(CERT_DIR / f"koubou158_sweep_v2_selftest_{time.strftime('%Y%m%d')}.json", report)
    print("SELFTEST PASS")
    print(json.dumps({"r108": t6["r108"], "r109": t6["r109"], "NM": t6["NM"],
                       "separator_CONFIRMED": t6["separator"]["verification"]["CONFIRMED"]}))
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description="koubou158_sweep_v2 -- hardened P4/P5")
    sub = ap.add_subparsers(dest="phase", required=True)

    sp = sub.add_parser("selftest")
    sp.add_argument("--p3-cert", required=True)

    sp = sub.add_parser("roof-wiring-check")
    sp.add_argument("--a", type=int, default=0)
    sp.add_argument("--b", type=int, default=1)

    sp = sub.add_parser("correction-wiring-check")
    sp.add_argument("--a", type=int, default=0)
    sp.add_argument("--b", type=int, default=1)

    sp = sub.add_parser("p4")
    sp.add_argument("--corr-start", type=int, default=0)
    sp.add_argument("--corr-end", type=int, default=27)
    sp.add_argument("--out-dir", default=None)
    sp.add_argument("--skip-wiring-check", action="store_true")

    sp = sub.add_parser("p5-shard")
    sp.add_argument("--shard-index", type=int, required=True)
    sp.add_argument("--shard-total", type=int, required=True)
    sp.add_argument("--out-dir", default=None)
    sp.add_argument("--skip-wiring-check", action="store_true")

    sp = sub.add_parser("p5-aggregate")
    sp.add_argument("--jsonl", nargs="+", required=True)
    sp.add_argument("--p3-cert", default=None)

    args = ap.parse_args()

    if args.phase == "selftest":
        run_selftest(args.p3_cert)
        return 0

    if args.phase == "roof-wiring-check":
        e4, colgen, q3 = load_e4_checked()
        wired, detail = run_axis_wiring_check(e4, colgen, q3, "roof", args.a, args.b)
        print(json.dumps(detail, indent=2))
        return 0 if wired else 1

    if args.phase == "correction-wiring-check":
        e4, colgen, q3 = load_e4_checked()
        wired, detail = run_axis_wiring_check(e4, colgen, q3, "correction", args.a, args.b)
        print(json.dumps(detail, indent=2))
        return 0 if wired else 1

    if args.phase == "p4":
        run_p4_v2(args.corr_start, args.corr_end, args.out_dir,
                   skip_wiring_check=args.skip_wiring_check)
        return 0

    if args.phase == "p5-shard":
        run_p5_shard_v2(args.shard_index, args.shard_total, args.out_dir,
                         skip_wiring_check=args.skip_wiring_check)
        return 0

    if args.phase == "p5-aggregate":
        aggregate_p5_v2(args.jsonl, args.p3_cert)
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
