#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/sat/calibrate_small_n.py

Small-degree exhaustive calibration requested in
sol/sol_reply_85_math12.md P85-6 point 4 (裁定 214 工程 4): "parameterized
encoder or a separate script, GAP-not-required itertools exhaustive
enumeration", n=5,7.

This is a SEPARATE, self-contained script (not importing
encode_tail8_n21.py's fixed N=21 module, to avoid coupling the frozen
theorem-target encoder to this calibration path) that:

  1. Ground truth (independent oracle, pure Python itertools/BFS, no GAP,
     no SAT solver): for n in {5,7}, fixes u = the n-cycle (1 2 ... n),
     exhaustively enumerates ALL involutions a on {1..n} with EXACTLY ONE
     global fixed point (the only cycle type consistent with the design's
     "row exactly-one + diagonal exactly-one" pair of constraints for odd
     n: (n-1)/2 transpositions + 1 fixed point), computes b(i) = u^-1(a(i))
     for each, keeps those with b^3 = identity (NOTE: b is NOT required to
     be fixed-point-free here, unlike the n=21 target -- 3 does not divide
     5 or 7, so an all-3-cycles b is impossible at these n; this is a
     deliberate, documented relaxation for calibrating the general
     class-constraint + BFS-transitivity MACHINERY, not a reproduction of
     the n=21 target's exact cycle-type axioms), then checks transitivity
     of <a,b> on {1..n} via direct Cayley-graph BFS.

  2. A parameterized CNF encoder, generic in n and the fixed u/u^-1 maps,
     built LOCALLY in this file (small, self-contained duplicate of the
     X/D/B/E/STEP/R Tseitin scheme in encode_tail8_n21.py, minus the
     b_fixed_point_free clause group per point 1's relaxation) that
     produces the class_cnf and transitive_cnf DIMACS files for each n.

  3. An encoding-fidelity spot check: for each ground-truth witness (a,b)
     found in step 1, build the CNF assignment implied by (a,b) per the
     construction in the SAT-COMP completeness lemma
     (docs/notes/sat_completeness_n21_v1.md steps 1-6, generalized to n)
     and evaluate EVERY clause of the generated CNF against that
     assignment (plain clause evaluation, no solver) -- confirming the
     "genuine witness => satisfying assignment" completeness direction
     empirically at small n, and confirming the encoder does not silently
     admit or exclude witnesses.

No kissat/drat-trim run (RAM 8GB; CI dispatch is the commander's job).
This script's own runtime is the calibration deliverable, run locally,
per 裁定 214 工程 4 instructions, and its stdout JSON is what gets
transcribed (machine-generated, not hand-copied) into mutants_n21.json.
"""
import itertools
import json
import time


def build_u_cycle(n):
    u = {i: (i % n) + 1 for i in range(1, n + 1)}
    uinv = {v: k for k, v in u.items()}
    return u, uinv


def compose(f, g):
    """(f then g): (f;g)(i) = g(f(i)) -- matches the module's right-action
    style b(i) = u^-1(a(i)), i.e. 'apply a first, then u^-1'."""
    return {i: g[f[i]] for i in f}


def perm_pow3_is_identity(b, n):
    b2 = compose(b, b)
    b3 = compose(b2, b)
    return all(b3[i] == i for i in range(1, n + 1))


def enumerate_involutions_one_fixed_point(n):
    """All involutions on {1..n} (odd n) with EXACTLY one fixed point,
    i.e. (n-1)/2 disjoint transpositions on the remaining n-1 points."""
    assert n % 2 == 1
    pts = list(range(1, n + 1))
    for fixed in pts:
        rest = [p for p in pts if p != fixed]
        for matching in _all_perfect_matchings(rest):
            a = {fixed: fixed}
            for (x, y) in matching:
                a[x] = y
                a[y] = x
            yield a


def _all_perfect_matchings(points):
    if not points:
        yield []
        return
    first = points[0]
    for i in range(1, len(points)):
        partner = points[i]
        rest = points[1:i] + points[i + 1:]
        for m in _all_perfect_matchings(rest):
            yield [(first, partner)] + m


def cayley_graph_transitive(a, b, n):
    binv = {v: k for k, v in b.items()}
    adj = {i: set() for i in range(1, n + 1)}
    for i in range(1, n + 1):
        adj[i].add(a[i])
        adj[i].add(b[i])
        adj[i].add(binv[i])
        adj[i].discard(i)
    seen = {1}
    frontier = [1]
    while frontier:
        nxt = []
        for w in frontier:
            for v in adj[w]:
                if v not in seen:
                    seen.add(v)
                    nxt.append(v)
        frontier = nxt
    return len(seen) == n


def ground_truth(n):
    u, uinv = build_u_cycle(n)
    class_witnesses = []
    transitive_witnesses = []
    for a in enumerate_involutions_one_fixed_point(n):
        b = {i: uinv[a[i]] for i in range(1, n + 1)}
        # b must be a permutation (it is, by construction) and satisfy b^3=1.
        if not perm_pow3_is_identity(b, n):
            continue
        class_witnesses.append((dict(a), dict(b)))
        if cayley_graph_transitive(a, b, n):
            transitive_witnesses.append((dict(a), dict(b)))
    return {
        "n": n,
        "u": u,
        "uinv": uinv,
        "num_involutions_one_fixed_point_total": sum(
            1 for _ in enumerate_involutions_one_fixed_point(n)
        ),
        "class_witness_count": len(class_witnesses),
        "class_sat": len(class_witnesses) > 0,
        "transitive_witness_count": len(transitive_witnesses),
        "transitive_sat": len(transitive_witnesses) > 0,
        "class_witnesses": class_witnesses,
        "transitive_witnesses": transitive_witnesses,
    }


# ---------------------------------------------------------------------
# Parameterized CNF encoder (generic n, generic u/uinv), no fpf group.
# ---------------------------------------------------------------------

class ClauseSet:
    def __init__(self):
        self.clauses = []
        self.groups = []

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


def make_var_scheme(n):
    pairs = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    pair_idx = {p: k + 1 for k, p in enumerate(pairs)}
    num_pairs = len(pairs)

    X_BASE = 0
    X_COUNT = num_pairs

    def X(i, j):
        if i > j:
            i, j = j, i
        return X_BASE + pair_idx[(i, j)]

    D_BASE = X_BASE + X_COUNT
    D_COUNT = n

    def D(i):
        return D_BASE + i

    B_BASE = D_BASE + D_COUNT
    B_COUNT = n * n

    def B(i, k):
        return B_BASE + (i - 1) * n + k

    class_var_count = B_BASE + B_COUNT

    step_pairs = [(w, v) for w in range(1, n + 1) for v in range(1, n + 1) if w != v]
    step_idx = {p: k + 1 for k, p in enumerate(step_pairs)}
    steps_per_t = len(step_pairs)
    num_steps_t = n - 1

    E_BASE = class_var_count
    E_COUNT = num_pairs

    def E(i, j):
        if i > j:
            i, j = j, i
        return E_BASE + pair_idx[(i, j)]

    STEP_BASE = E_BASE + E_COUNT
    STEP_COUNT = num_steps_t * steps_per_t

    def STEP(t, w, v):
        return STEP_BASE + (t - 1) * steps_per_t + step_idx[(w, v)]

    R_BASE = STEP_BASE + STEP_COUNT
    R_COUNT = n * n

    def R(t, v):
        return R_BASE + t * n + v

    trans_var_count = R_BASE + R_COUNT

    return {
        "pairs": pairs, "X": X, "D": D, "B": B, "E": E, "STEP": STEP, "R": R,
        "class_var_count": class_var_count, "trans_var_count": trans_var_count,
        "num_steps_t": num_steps_t,
    }


def build_class_cnf(n, u):
    vs = make_var_scheme(n)
    X, D, B = vs["X"], vs["D"], vs["B"]
    cs = ClauseSet()

    # row exactly-one
    clauses = []
    for i in range(1, n + 1):
        lits = [X(i, j) for j in range(1, n + 1) if j != i] + [D(i)]
        clauses.append(list(lits))
        for p in range(len(lits)):
            for q in range(p + 1, len(lits)):
                clauses.append([-lits[p], -lits[q]])
    cs.add_group("a_row_exactly_one", clauses)

    # diagonal exactly-one (global)
    clauses = []
    dvars = [D(i) for i in range(1, n + 1)]
    clauses.append(list(dvars))
    for p in range(len(dvars)):
        for q in range(p + 1, len(dvars)):
            clauses.append([-dvars[p], -dvars[q]])
    cs.add_group("a_diagonal_exactly_one_fixed_point", clauses)

    # B definition: B(i,k) <-> (D(i) if u(k)==i else X(i,u(k)))
    clauses = []
    for i in range(1, n + 1):
        for k in range(1, n + 1):
            j = u[k]
            lit = D(i) if j == i else X(i, j)
            bvar = B(i, k)
            clauses.append([-bvar, lit])
            clauses.append([-lit, bvar])
    cs.add_group("b_definition_tseitin", clauses)

    # b^3 = 1
    clauses = []
    for i in range(1, n + 1):
        for k1 in range(1, n + 1):
            for k2 in range(1, n + 1):
                clauses.append([-B(i, k1), -B(k1, k2), B(k2, i)])
    cs.add_group("b_cubed_equals_identity", clauses)
    # NOTE: no b_fixed_point_free group here (see module docstring point 1).

    return cs, vs


def build_transitive_cnf(n, u):
    cs, vs = build_class_cnf(n, u)
    X, B, E, STEP, R = vs["X"], vs["B"], vs["E"], vs["STEP"], vs["R"]

    clauses = []
    for (i, j) in vs["pairs"]:
        e = E(i, j)
        x = X(i, j)
        bij = B(i, j)
        bji = B(j, i)
        clauses.append([-x, e])
        clauses.append([-bij, e])
        clauses.append([-bji, e])
        clauses.append([-e, x, bij, bji])
    cs.add_group("cayley_edge_definition", clauses)

    clauses = [[R(0, 1)]] + [[-R(0, v)] for v in range(2, n + 1)]
    cs.add_group("reachability_base_case_t0", clauses)

    clauses = []
    for t in range(1, vs["num_steps_t"] + 1):
        for w in range(1, n + 1):
            for v in range(1, n + 1):
                if w == v:
                    continue
                step = STEP(t, w, v)
                rprev = R(t - 1, w)
                e = E(w, v)
                clauses.append([-step, rprev])
                clauses.append([-step, e])
                clauses.append([-rprev, -e, step])
    cs.add_group("bfs_step_definition", clauses)

    clauses = []
    for t in range(1, vs["num_steps_t"] + 1):
        for v in range(1, n + 1):
            rt = R(t, v)
            rprev = R(t - 1, v)
            steps = [STEP(t, w, v) for w in range(1, n + 1) if w != v]
            clauses.append([-rprev, rt])
            for s in steps:
                clauses.append([-s, rt])
            clauses.append([-rt, rprev] + steps)
    cs.add_group("reachability_step_recurrence", clauses)

    clauses = [[R(n - 1, v)] for v in range(1, n + 1)]
    cs.add_group("transitivity_goal_all_reached", clauses)

    return cs, vs


def evaluate_clause(clause, true_vars):
    return any((lit > 0 and lit in true_vars) or (lit < 0 and -lit not in true_vars)
               for lit in clause)


def assignment_from_witness(n, u, uinv, a, b, vs, want_transitivity_vars=False):
    """Construct the CNF assignment implied by a genuine witness (a,b),
    per the SAT-COMP completeness lemma's steps 1-4 (generalized to n)."""
    X, D, B, E = vs["X"], vs["D"], vs["B"], vs["E"]
    true_vars = set()
    for i in range(1, n + 1):
        if a[i] == i:
            true_vars.add(D(i))
        elif a[i] > i:
            true_vars.add(X(i, a[i]))
        # if a[i] < i, X(a[i], i) is added when processing i'=a[i]
    for i in range(1, n + 1):
        true_vars.add(B(i, b[i]))
    if want_transitivity_vars:
        binv = {v: k for k, v in b.items()}
        adj = {i: set() for i in range(1, n + 1)}
        for i in range(1, n + 1):
            adj[i].add(a[i]); adj[i].add(b[i]); adj[i].add(binv[i])
            adj[i].discard(i)
        for (i, j) in vs["pairs"]:
            if j in adj[i]:
                true_vars.add(E(i, j))
        # BFS reachability sets, t=0..n-1
        R = vs["R"]
        dist = {1: 0}
        frontier = [1]
        t = 0
        reached_by = {0: {1}}
        while frontier and t < n - 1:
            t += 1
            nxt = []
            cur = set(reached_by[t - 1])
            for w in frontier:
                for v in adj[w]:
                    if v not in cur:
                        cur.add(v)
                        nxt.append(v)
            reached_by[t] = cur
            frontier = nxt
        for tt in range(0, n):
            rs = reached_by.get(tt, reached_by[max(k for k in reached_by if k <= tt)])
            for v in range(1, n + 1):
                if v in rs:
                    true_vars.add(R(tt, v))
        # STEP variables: set true wherever both premises hold (sufficient
        # to satisfy STEP's clauses; the encoder does not require STEP to
        # be minimal).
        STEP = vs["STEP"]
        for tt in range(1, n):
            rs_prev = reached_by.get(tt - 1, reached_by[max(k for k in reached_by if k <= tt - 1)])
            for w in range(1, n + 1):
                for v in range(1, n + 1):
                    if w == v:
                        continue
                    if w in rs_prev and (v in adj[w]):
                        true_vars.add(STEP(tt, w, v))
    return true_vars


def calibrate(n):
    t0 = time.time()
    gt = ground_truth(n)
    u, uinv = gt["u"], gt["uinv"]

    class_cs, class_vs = build_class_cnf(n, u)
    trans_cs, trans_vs = build_transitive_cnf(n, u)

    fidelity = {"class": None, "transitive": None}

    if gt["class_witnesses"]:
        a, b = gt["class_witnesses"][0]
        assign = assignment_from_witness(n, u, uinv, a, b, class_vs, want_transitivity_vars=False)
        violated = [c for c in class_cs.clauses if not evaluate_clause(c, assign)]
        fidelity["class"] = {
            "witness_a": a, "witness_b": b,
            "clauses_checked": class_cs.nclauses(),
            "clauses_violated": len(violated),
            "first_violations": violated[:5],
        }

    if gt["transitive_witnesses"]:
        a, b = gt["transitive_witnesses"][0]
        assign = assignment_from_witness(n, u, uinv, a, b, trans_vs, want_transitivity_vars=True)
        violated = [c for c in trans_cs.clauses if not evaluate_clause(c, assign)]
        fidelity["transitive"] = {
            "witness_a": a, "witness_b": b,
            "clauses_checked": trans_cs.nclauses(),
            "clauses_violated": len(violated),
            "first_violations": violated[:5],
        }

    elapsed = time.time() - t0

    return {
        "n": n,
        "fixed_u_cycle": [u[k] for k in range(1, n + 1)],
        "ground_truth": {
            "num_involutions_one_fixed_point_total": gt["num_involutions_one_fixed_point_total"],
            "class_sat": gt["class_sat"],
            "class_witness_count": gt["class_witness_count"],
            "transitive_sat": gt["transitive_sat"],
            "transitive_witness_count": gt["transitive_witness_count"],
        },
        "cnf_stats": {
            "class_num_vars": class_vs["class_var_count"],
            "class_num_clauses": class_cs.nclauses(),
            "transitive_num_vars": trans_vs["trans_var_count"],
            "transitive_num_clauses": trans_cs.nclauses(),
        },
        "encoding_fidelity_spot_check": fidelity,
        "elapsed_seconds": round(elapsed, 3),
    }


def main():
    out = {"n5": calibrate(5), "n7": calibrate(7)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
