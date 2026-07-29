#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/sat/encode_tail8_n21.py

Encoder for the n=21 tail-8 SAT calibration target.
Design source: sol/sol_reply_84_math11.md sec 6.2 ("first target n=21 CNF"),
per instructions in 裁定 210 工程 1-B. ES7 pipeline style
(atelier_lean/ES7/abstract_sat/) is followed for the surrounding harness
(search/sat/README.md, .github/workflows/sat-run.yml) but this encoder is a
fresh implementation, not a copy.

Produces TWO DIMACS CNF files from one shared "class" prefix:

  1. <out_prefix>_class.cnf       -- class constraints only.
                                      Expected SAT (a witness is one of the
                                      known 4160 solutions; see
                                      search/probe/wac_v1/tail8_exact.g).
  2. <out_prefix>_transitive.cnf  -- class constraints + bounded-BFS
                                      transitivity goal.
                                      Expected UNSAT (Sol 6.2: A_21
                                      generation implies transitivity, so
                                      UNSAT of this weaker transitivity
                                      requirement already proves "no A_21
                                      generating solution").

Neither CNF encodes A_21-membership, the structure constant 4160, or the
C(u)-orbit census as axioms. Those remain an external oracle used only to
interpret results after the fact (Sol 6.2, 6.5 point 5).

=====================================================================
DESIGN FIDELITY NOTES (do not relax without re-consulting Sol sec 6.2/6.5)
=====================================================================

Fixed data (NOT variables):
  u = (1 2 ... 13)(14 15)(16 17)(18 19)(20 21)  -- the sealed conjugacy
  representative fixed throughout search/probe/wac_v1/tail8*.g.

Product-order convention (VERIFIED against a machine-extracted GAP
witness, see search/sat/fixtures/witness_n21_nontransitive.json):
  GAP's right-action convention gives, for b := a * u^-1,
      i ^ (a * u^-1) = (i ^ a) ^ u^-1
  i.e. "apply a first, then u^-1".  So here:  b(i) = u^-1( a(i) ).
  This was checked pointwise against the GAP fixture before being encoded
  (a(1)=15, u^-1(15)=14, and the fixture's b(1)=14 -- matches).

a is encoded as an INVOLUTION via matching variables, not a full
permutation matrix, because the target cycle type 2^10 1 IS an
involution's cycle type:
  - X[i][j] for 1<=i<j<=21 : "a swaps i and j" (a(i)=j and, by
    involution symmetry, a(j)=i -- same boolean, no separate direction).
  - D[i] for 1<=i<=21      : "a fixes i".
  - Row exactly-one, for every i: exactly one of {X[i][j] or X[j][i] for
    j != i} union {D[i]} holds.  NOTE: row exactly-one alone does NOT
    pin the number of fixed points to 1 (any odd count 1,3,5,...,21 is
    consistent with it) -- a SEPARATE global cardinality-1 constraint
    over all 21 D[i] is required and included below.  This is exactly
    Sol 6.2's "対角 A_ii はちょうど一個".

b is order 3 (not an involution), so it needs a full 21x21 boolean
matrix B[i][k] meaning b(i)=k, DERIVED from a and the fixed u via Tseitin
biconditionals (Sol 6.2: "Tseitin 変数で導出"):
  B[i][k] <-> ( D[i]              if u(k) == i
                X[min(i,u(k)), max(i,u(k))]   otherwise )
b^3=1 is encoded by forcing, for every i,k1,k2 in 1..21:
      B[i][k1] & B[k1][k2]  =>  B[k2][i]
Combined with fixed-point-freeness (b(i) != i for all i, i.e. not
B[i][i]), and the fact that a permutation of order dividing 3 can only
have 1-cycles or 3-cycles, this pins b's cycle type to EXACTLY 3^7
(21 = 3*7, no fixed points allowed).  A_21-membership of <a,b> is never
encoded directly.

Transitivity (CNF #2 only) is bounded-depth (0..20) BFS reachability
from point 1 over the UNDIRECTED Cayley graph with edge set {a, b, b^-1}
(a is self-inverse; b and b^-1 are folded into one symmetric edge
relation E, see below).  21 points => any two points in one orbit are
connected by a simple path of length <= 20, so depth 0..20 is complete
for a group of this degree (Sol 6.2: "21 頂点の連結グラフなら長さ 20
以下の単純路がある").

  E[i][j] for i<j : "i and j are Cayley-graph-adjacent"
      E[i][j] <-> X[i][j]  OR  B[i][j]  OR  B[j][i]
  (B[i][j] covers the b-edge i->j; B[j][i] covers the b^-1-edge, i.e. an
  edge j->i via b folds back to an undirected i~j edge.)

  R[t][v] for t=0..20, v=1..21 : "v is reached from point 1 within t
  BFS steps".
      R[0][1] = true (unit clause); R[0][v] = false for v != 1 (unit
      clauses) -- this NEGATIVE base case matters: without it a solver
      could seed reachability anywhere for free.
      For t=1..20, v=1..21:
          R[t][v] <-> R[t-1][v]  OR  (EXISTS w != v : E[w,v] AND R[t-1][w])
      encoded via Tseitin STEP variables:
          STEP[t][w][v] <-> E[w,v] AND R[t-1][w]   (w != v)
          R[t][v]       <-> R[t-1][v] OR (OR over w of STEP[t][w][v])

  CRITICAL SOUNDNESS POINT (Sol 6.5 mutants: "transitivity dropped",
  "BFS depth 1-off"): both directions of every "<->" above are encoded,
  in particular the NECESSARY direction
      R[t][v]  =>  R[t-1][v]  OR  (OR_w STEP[t][w][v])
  This is what prevents a solver from satisfying the transitivity goal
  clauses (R[20][v] for all v, appended as unit clauses) by simply
  setting all R variables true "for free" with no real justification.
  If this direction were dropped, CNF#2 would silently degrade to
  CNF#1's satisfiability (a real -- but wrong -- bug: an unsound
  "UNSAT" pipeline would then just be reporting CNF#1's SAT-ness under a
  different name, i.e. it would ACTUALLY come out SAT, alerting us; the
  dangerous failure mode is a broken encoding that comes out UNSAT for
  the wrong reason, which drat-trim's DRAT check cannot catch --- see
  README's "encoding fidelity is the linchpin" note and Sol 6.5 point 7:
  the completeness direction, "math witness => CNF assignment", is a
  separate paper audit, not performed by this script).

This encoder does not attempt to minimize clause count (e.g. no
sequential/commander at-most-one encodings, no removal of degenerate
b^3 triples) -- correctness and auditability take priority at n=21 scale
(a few 10^4 clauses, well within kissat's normal operating range).
"""
import argparse
import hashlib
import json
import os
import sys

N = 21

# ---------------------------------------------------------------------
# Fixed data: u and u^-1 (NOT SAT variables).
# ---------------------------------------------------------------------

def build_u():
    u = {}
    for i in range(1, 13):
        u[i] = i + 1
    u[13] = 1
    for a, b in [(14, 15), (16, 17), (18, 19), (20, 21)]:
        u[a] = b
        u[b] = a
    return u


U = build_u()
UINV = {v: k for k, v in U.items()}

# sanity: verify against the machine-extracted GAP fixture at import time.
_FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures",
                              "witness_n21_nontransitive.json")


def _check_convention_against_fixture():
    with open(_FIXTURE_PATH, "r", encoding="utf-8") as f:
        fx = json.load(f)
    u_img = fx["u_images_1indexed"]
    uinv_img = fx["uinv_images_1indexed"]
    for k in range(1, N + 1):
        assert U[k] == u_img[k - 1], f"u mismatch at {k}"
        assert UINV[k] == uinv_img[k - 1], f"u^-1 mismatch at {k}"
    a_img = fx["a_images_1indexed"]
    b_img = fx["b_images_1indexed"]
    for k in range(1, N + 1):
        assert UINV[a_img[k - 1]] == b_img[k - 1], (
            f"product-order convention mismatch at point {k}: "
            f"expected b(k)=u^-1(a(k))={UINV[a_img[k-1]]}, "
            f"fixture has b(k)={b_img[k-1]}"
        )


# ---------------------------------------------------------------------
# Variable allocation (1-indexed DIMACS variable ids).
# ---------------------------------------------------------------------

def pair_index_table():
    """Ordered list of all (i,j), i<j, in 1..N, row-major. 1-indexed rank."""
    pairs = []
    for i in range(1, N + 1):
        for j in range(i + 1, N + 1):
            pairs.append((i, j))
    idx = {p: k + 1 for k, p in enumerate(pairs)}
    return pairs, idx


PAIRS, PAIR_IDX = pair_index_table()
NUM_PAIRS = len(PAIRS)  # 210

# X[i][j] i<j : ids 1 .. NUM_PAIRS
X_BASE = 0
X_COUNT = NUM_PAIRS


def X(i, j):
    if i == j:
        raise ValueError("X(i,i) undefined")
    if i > j:
        i, j = j, i
    return X_BASE + PAIR_IDX[(i, j)]


# D[i] i=1..N : ids after X
D_BASE = X_BASE + X_COUNT
D_COUNT = N


def D(i):
    return D_BASE + i


# B[i][k] i,k=1..N : ids after D
B_BASE = D_BASE + D_COUNT
B_COUNT = N * N


def B(i, k):
    return B_BASE + (i - 1) * N + k


CLASS_VAR_COUNT = B_BASE + B_COUNT  # = 210 + 21 + 441 = 672

# E[i][j] i<j : ids after class vars (transitivity CNF only)
E_BASE = CLASS_VAR_COUNT
E_COUNT = NUM_PAIRS


def E(i, j):
    if i == j:
        raise ValueError("E(i,i) undefined")
    if i > j:
        i, j = j, i
    return E_BASE + PAIR_IDX[(i, j)]


# STEP[t][w][v], t=1..20, w!=v in 1..N : ids after E
STEP_ORDERED_PAIRS = [(w, v) for w in range(1, N + 1) for v in range(1, N + 1) if w != v]
STEP_PAIR_IDX = {p: k + 1 for k, p in enumerate(STEP_ORDERED_PAIRS)}
STEP_PAIRS_PER_T = len(STEP_ORDERED_PAIRS)  # 420
NUM_STEPS_T = N - 1  # t = 1..20

STEP_BASE = E_BASE + E_COUNT
STEP_COUNT = NUM_STEPS_T * STEP_PAIRS_PER_T  # 8400


def STEP(t, w, v):
    if not (1 <= t <= NUM_STEPS_T):
        raise ValueError("t out of range")
    return STEP_BASE + (t - 1) * STEP_PAIRS_PER_T + STEP_PAIR_IDX[(w, v)]


# R[t][v], t=0..20, v=1..N : ids after STEP
R_BASE = STEP_BASE + STEP_COUNT
R_COUNT = (N) * N  # t has N=21 values (0..20), v has N=21 values


def R(t, v):
    if not (0 <= t <= N - 1):
        raise ValueError("t out of range")
    return R_BASE + t * N + v


TRANS_VAR_COUNT = R_BASE + R_COUNT  # = 672 + 210 + 8400 + 441 = 9723

assert CLASS_VAR_COUNT == 672, CLASS_VAR_COUNT
assert TRANS_VAR_COUNT == 9723, TRANS_VAR_COUNT


# ---------------------------------------------------------------------
# Clause construction. Each "group" is recorded as (name, start, end)
# using 1-indexed clause *line numbers* within the final CNF file, so the
# manifest can point auditors at exact ranges.
# ---------------------------------------------------------------------

class ClauseSet:
    def __init__(self):
        self.clauses = []
        self.groups = []  # (name, start_1idx, end_1idx_inclusive)

    def add(self, clause):
        self.clauses.append(list(clause))

    def add_group(self, name, clauses):
        start = len(self.clauses) + 1
        for c in clauses:
            self.add(c)
        end = len(self.clauses)
        self.groups.append({"name": name, "start": start, "end": end, "count": end - start + 1})

    def nclauses(self):
        return len(self.clauses)


def underlying_literal_for_B(i, k):
    """The single literal that B(i,k) is defined equivalent to."""
    j = U[k]  # b(i)=k  <=>  a(i) = u(k)
    if j == i:
        return D(i)
    return X(i, j)


def group_row_exactly_one(cs):
    clauses = []
    for i in range(1, N + 1):
        lits = []
        for j in range(1, N + 1):
            if j == i:
                continue
            lits.append(X(i, j))
        lits.append(D(i))
        # at-least-one
        clauses.append(list(lits))
        # pairwise at-most-one
        for a in range(len(lits)):
            for b in range(a + 1, len(lits)):
                clauses.append([-lits[a], -lits[b]])
    cs.add_group("a_row_exactly_one", clauses)


def group_diagonal_exactly_one(cs):
    clauses = []
    dvars = [D(i) for i in range(1, N + 1)]
    clauses.append(list(dvars))
    for a in range(len(dvars)):
        for b in range(a + 1, len(dvars)):
            clauses.append([-dvars[a], -dvars[b]])
    cs.add_group("a_diagonal_exactly_one_fixed_point", clauses)


def group_b_definition(cs):
    clauses = []
    for i in range(1, N + 1):
        for k in range(1, N + 1):
            lit = underlying_literal_for_B(i, k)
            bvar = B(i, k)
            clauses.append([-bvar, lit])   # B -> lit
            clauses.append([-lit, bvar])   # lit -> B
    cs.add_group("b_definition_tseitin", clauses)


def group_b_cubed_identity(cs):
    clauses = []
    for i in range(1, N + 1):
        for k1 in range(1, N + 1):
            for k2 in range(1, N + 1):
                clauses.append([-B(i, k1), -B(k1, k2), B(k2, i)])
    cs.add_group("b_cubed_equals_identity", clauses)


def group_b_fixed_point_free(cs):
    clauses = []
    for i in range(1, N + 1):
        clauses.append([-B(i, i)])
    cs.add_group("b_fixed_point_free", clauses)


def build_class_clauses():
    cs = ClauseSet()
    group_row_exactly_one(cs)
    group_diagonal_exactly_one(cs)
    group_b_definition(cs)
    group_b_cubed_identity(cs)
    group_b_fixed_point_free(cs)
    return cs


def group_edge_definition(cs):
    clauses = []
    for (i, j) in PAIRS:
        e = E(i, j)
        x = X(i, j)
        bij = B(i, j)
        bji = B(j, i)
        clauses.append([-x, e])
        clauses.append([-bij, e])
        clauses.append([-bji, e])
        clauses.append([-e, x, bij, bji])
    cs.add_group("cayley_edge_definition", clauses)


def group_r_base_case(cs):
    clauses = []
    clauses.append([R(0, 1)])
    for v in range(2, N + 1):
        clauses.append([-R(0, v)])
    cs.add_group("reachability_base_case_t0", clauses)


def group_step_definition(cs):
    clauses = []
    for t in range(1, NUM_STEPS_T + 1):
        for (w, v) in STEP_ORDERED_PAIRS:
            step = STEP(t, w, v)
            rprev = R(t - 1, w)
            e = E(w, v)
            clauses.append([-step, rprev])       # STEP -> R[t-1][w]
            clauses.append([-step, e])           # STEP -> E[w][v]
            clauses.append([-rprev, -e, step])   # R[t-1][w] & E[w][v] -> STEP
    cs.add_group("bfs_step_definition", clauses)


def group_r_step_definition(cs):
    clauses = []
    for t in range(1, NUM_STEPS_T + 1):
        for v in range(1, N + 1):
            rt = R(t, v)
            rprev = R(t - 1, v)
            steps = [STEP(t, w, v) for w in range(1, N + 1) if w != v]
            clauses.append([-rprev, rt])
            for s in steps:
                clauses.append([-s, rt])
            clauses.append([-rt, rprev] + steps)
    cs.add_group("reachability_step_recurrence", clauses)


def group_transitivity_goal(cs):
    clauses = []
    for v in range(1, N + 1):
        clauses.append([R(N - 1, v)])
    cs.add_group("transitivity_goal_all_reached_by_t20", clauses)


def build_transitive_clauses():
    cs = build_class_clauses()
    group_edge_definition(cs)
    group_r_base_case(cs)
    group_step_definition(cs)
    group_r_step_definition(cs)
    group_transitivity_goal(cs)
    return cs


# ---------------------------------------------------------------------
# DIMACS output.
# ---------------------------------------------------------------------

def write_dimacs(path, nvars, clauseset, comment_lines):
    with open(path, "w", encoding="ascii", newline="\n") as f:
        for c in comment_lines:
            f.write("c " + c + "\n")
        f.write(f"p cnf {nvars} {clauseset.nclauses()}\n")
        for cl in clauseset.clauses:
            f.write(" ".join(str(x) for x in cl) + " 0\n")


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_source():
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(__file__), "out"))
    ap.add_argument("--prefix", default="tail8_n21")
    ap.add_argument("--skip-fixture-check", action="store_true",
                     help="Skip cross-check against the GAP witness fixture (debug only).")
    ap.add_argument("--manifest-out", default=None,
                     help="If given, write the encoder manifest JSON here "
                          "(variable/clause ranges, digests). Intended target: "
                          "search/sat/manifest_tail8_n21.json.")
    args = ap.parse_args()

    if not args.skip_fixture_check:
        _check_convention_against_fixture()

    os.makedirs(args.out_dir, exist_ok=True)

    class_cs = build_class_clauses()
    trans_cs = build_transitive_clauses()

    class_path = os.path.join(args.out_dir, f"{args.prefix}_class.cnf")
    trans_path = os.path.join(args.out_dir, f"{args.prefix}_transitive.cnf")

    write_dimacs(
        class_path, CLASS_VAR_COUNT, class_cs,
        [
            "n=21 tail-8 SAT calibration target -- CLASS CONSTRAINTS ONLY.",
            "Expected: SAT. Source: sol/sol_reply_84_math11.md sec 6.2.",
            "Generated by search/sat/encode_tail8_n21.py -- do not hand-edit.",
        ],
    )
    write_dimacs(
        trans_path, TRANS_VAR_COUNT, trans_cs,
        [
            "n=21 tail-8 SAT calibration target -- CLASS + TRANSITIVITY.",
            "Expected: UNSAT. Source: sol/sol_reply_84_math11.md sec 6.2.",
            "Generated by search/sat/encode_tail8_n21.py -- do not hand-edit.",
        ],
    )

    stats = {
        "class_cnf": {
            "path": os.path.relpath(class_path).replace("\\", "/"),
            "num_vars": CLASS_VAR_COUNT,
            "num_clauses": class_cs.nclauses(),
            "sha256": sha256_of_file(class_path),
            "groups": class_cs.groups,
        },
        "transitive_cnf": {
            "path": os.path.relpath(trans_path).replace("\\", "/"),
            "num_vars": TRANS_VAR_COUNT,
            "num_clauses": trans_cs.nclauses(),
            "sha256": sha256_of_file(trans_path),
            "groups": trans_cs.groups,
        },
        "encoder_source_sha256": sha256_of_source(),
    }
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    if args.manifest_out:
        manifest = build_manifest(stats)
        with open(args.manifest_out, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"manifest written to {args.manifest_out}", file=sys.stderr)


def build_manifest(stats):
    """Assemble the encoder manifest purely from values computed by this
    module (variable id functions, ClauseSet groups, stats dict) -- no
    number here is hand-transcribed."""
    return {
        "schema": "shadow-atelier/sat-encoder-manifest/v1",
        "target": "W-D-A21-13t8 n=21 tail-8 SAT calibration (裁定 210 工程 1-B, "
                  "sol/sol_reply_84_math11.md sec 6.2)",
        "encoder_source": "search/sat/encode_tail8_n21.py",
        "encoder_source_sha256": stats["encoder_source_sha256"],
        "universe": {
            "n": N,
            "points": "1..21 (1-indexed, matches GAP convention throughout "
                      "search/probe/wac_v1/tail8*.g)",
        },
        "fixed_u": {
            "cycle_notation": "(1,2,3,4,5,6,7,8,9,10,11,12,13)(14,15)(16,17)(18,19)(20,21)",
            "images_1indexed": [U[k] for k in range(1, N + 1)],
            "inverse_images_1indexed": [UINV[k] for k in range(1, N + 1)],
            "note": "u is a fixed constant, not a CNF variable (sealed symbol, "
                     "same representative as search/probe/wac_v1/tail8_exact.g).",
        },
        "product_order_convention": {
            "statement": "b := a * u^-1 under GAP's right-action convention: "
                          "i^(a*u^-1) = (i^a)^u^-1, i.e. apply a first, then u^-1. "
                          "Equivalently b(i) = u^-1(a(i)).",
            "cross_checked_against": "search/sat/fixtures/witness_n21_nontransitive.json "
                                       "(machine-extracted GAP witness; encoder asserts this "
                                       "at import time unless --skip-fixture-check is passed)",
        },
        "target_classes": {
            "a": "involution, cycle type 2^10 1 (10 disjoint transpositions, 1 fixed point)",
            "b": "cycle type 3^7 (b = a*u^-1, b^3=1, fixed-point-free)",
            "a21_generation_not_encoded": "generation of A_21 by <a,b> is NOT a CNF axiom; "
                "Sol 6.2 notes A_21-generation implies transitivity, so UNSAT of the strictly "
                "weaker transitivity requirement already proves 'no A_21-generating solution'.",
            "oracle_not_encoded": "structure constant 4160 and the C(u)-orbit census "
                "(search/probe/wac_v1/tail8_exact.g, wac_tail8_v1.md) are external oracles, "
                "used only to interpret CNF#1 SAT models after decoding -- never CNF axioms.",
        },
        "variable_families": {
            "class_cnf": {
                "total_vars": CLASS_VAR_COUNT,
                "families": [
                    {"name": "X[i][j]", "meaning": "a swaps i and j (i<j, involution "
                     "transposition variable; A_ij=A_ji per Sol 6.2, encoded as a single "
                     "shared boolean rather than two)",
                     "ids": [X_BASE + 1, X_BASE + X_COUNT], "count": X_COUNT,
                     "index_order": "row-major over 1<=i<j<=21"},
                    {"name": "D[i]", "meaning": "a fixes i",
                     "ids": [D_BASE + 1, D_BASE + D_COUNT], "count": D_COUNT,
                     "index_order": "i=1..21"},
                    {"name": "B[i][k]", "meaning": "b(i)=k (Tseitin-derived from X/D via fixed u)",
                     "ids": [B_BASE + 1, B_BASE + B_COUNT], "count": B_COUNT,
                     "index_order": "i outer 1..21, k inner 1..21, id = B_BASE + (i-1)*21 + k"},
                ],
            },
            "transitive_cnf_additional": {
                "total_additional_vars": TRANS_VAR_COUNT - CLASS_VAR_COUNT,
                "families": [
                    {"name": "E[i][j]", "meaning": "i,j Cayley-graph-adjacent via {a,b,b^-1} "
                     "(i<j, symmetric by construction)",
                     "ids": [E_BASE + 1, E_BASE + E_COUNT], "count": E_COUNT,
                     "index_order": "row-major over 1<=i<j<=21"},
                    {"name": "STEP[t][w][v]", "meaning": "Tseitin AND-gate: "
                     "E[w,v] & R[t-1][w] (w!=v, t=1..20)",
                     "ids": [STEP_BASE + 1, STEP_BASE + STEP_COUNT], "count": STEP_COUNT,
                     "index_order": "t outer (1..20), then ordered pairs (w,v), w!=v, "
                                    "row-major, 420 per t"},
                    {"name": "R[t][v]", "meaning": "v reached from point 1 within t BFS "
                     "steps (t=0..20)",
                     "ids": [R_BASE + 1, R_BASE + R_COUNT], "count": R_COUNT,
                     "index_order": "t outer (0..20), v inner (1..21), "
                                    "id = R_BASE + t*21 + v"},
                ],
            },
        },
        "clause_groups": {
            "class_cnf": stats["class_cnf"]["groups"],
            "transitive_cnf": stats["transitive_cnf"]["groups"],
        },
        "cnf_files": {
            "class": {
                "path": stats["class_cnf"]["path"],
                "num_vars": stats["class_cnf"]["num_vars"],
                "num_clauses": stats["class_cnf"]["num_clauses"],
                "sha256": stats["class_cnf"]["sha256"],
                "expected_verdict": "SAT",
                "expected_model_property": "decodes to one of the 4160 known class-only "
                    "solutions (external oracle: search/probe/wac_v1/tail8_exact.g); "
                    "transitivity is NOT required and the decoded model is expected to be "
                    "non-transitive (all 5 known C(u)-orbit representatives have orbit "
                    "partition [6,15] per sol/sol_reply_84_math11.md F84-3.1).",
            },
            "transitive": {
                "path": stats["transitive_cnf"]["path"],
                "num_vars": stats["transitive_cnf"]["num_vars"],
                "num_clauses": stats["transitive_cnf"]["num_clauses"],
                "sha256": stats["transitive_cnf"]["sha256"],
                "expected_verdict": "UNSAT",
                "theorem_reading": "no (a,b) with a in 2^10 1, b=a*u^-1 in 3^7 generates a "
                    "transitive subgroup of S_21 for this fixed u; since A_21-generation "
                    "implies transitivity, this also rules out A_21-generation "
                    "(W-D-A21-13t8 negative result, Sol F84-3.1 theorem-candidate).",
            },
        },
        "symmetry_reduction": {
            "applied": "u is fixed to a single explicit conjugacy representative "
                       "(same representative as tail8_exact.g); no further row/column "
                       "symmetry breaking (e.g. lexicographic leader clauses on X) is "
                       "applied. C(u)-orbit symmetry (the centralizer action used by "
                       "tail8_exact.g to enumerate 5 orbits instead of 4160 individual "
                       "permutations) is NOT encoded as CNF symmetry-breaking clauses -- "
                       "it remains purely in the external GAP oracle.",
            "rationale": "Sol 6.2 does not request in-CNF symmetry breaking for this "
                        "target; adding it would need a separate soundness argument "
                        "(a symmetry-breaking predicate must not remove genuine models) "
                        "that has not been done here. Left for a follow-up if solver "
                        "runtime demands it.",
        },
        "audit_status": {
            "soundness_direction_of_encoding": "checked informally in this file's "
                "docstring and via search/sat/check_model_n21.mjs (independent, "
                "non-importing re-derivation of a, b, and reachability from a decoded "
                "SAT model).",
            "completeness_direction": "NOT AUDITED HERE. The completeness lemma "
                "('a genuine mathematical witness always induces a satisfying CNF "
                "assignment') is a paper-audit item per Sol 6.5 point 7, assigned to "
                "the mathematician role, not this encoder or its checker. Do not treat "
                "a CNF#2 UNSAT result as a verified non-existence claim until that "
                "lemma is written down and reviewed.",
        },
    }


if __name__ == "__main__":
    main()
