#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/sat/gen_mutants_reverse_drop.py

Generates the two "reverse-clause drop" mutant CNFs requested in
sol/sol_reply_85_math12.md P85-6 points 1-2 (裁定 214 工程 4):

  M8_reach_reverse_drop : drop the necessary direction
      R[t][v] => R[t-1][v] OR (OR_w STEP[t][w][v])
    from group_r_step_definition, keeping only the sufficient direction.
    Sol's paper argument (P85-6 point 1): the class CNF's model can then
    set all R[t>=1][v]=1 "for free" with no BFS justification, so the
    transitive-mutant CNF is expected SAT on paper (this is the "BFS
    free-true" bug detector).

  M9_edge_reverse_drop : drop the necessary direction
      E[i][j] => X[i][j] OR B[i][j] OR B[j][i]
    from group_edge_definition, keeping only the sufficient direction.
    Sol's paper argument (P85-6 point 2): all E[i][j] can then be set
    true for free (no genuine adjacency required), collapsing BFS to a
    complete graph, so the transitive-mutant CNF is expected SAT on
    paper.

DOES NOT modify encode_tail8_n21.py (the frozen theorem-target encoder).
Instead it imports that module (same "explorer" side of the
searcher/checker split -- CLAUDE.md's separation rule is about not
sharing code between the GAP/SAT *search* side and the independent
*crosscheck* side; reusing the theorem encoder's variable-id functions
and unrelated clause groups from one search-side script in another
search-side script is not a violation of that rule) and re-implements
ONLY the two mutated clause groups locally, byte-for-byte identical to
the originals except for the one dropped clause line, so a diff against
encode_tail8_n21.py's group_edge_definition / group_r_step_definition
shows exactly what changed.

kissat is NOT invoked here (RAM 8GB constraint; CI dispatch is the
commander's job per 裁定 214 工程 4 instructions). This script only
generates the CNF files and registers their SHA-256 + expected verdict.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import encode_tail8_n21 as ENC  # noqa: E402  (search-side reuse, see docstring)


def group_edge_definition_no_reverse(cs):
    """Same as ENC.group_edge_definition but WITHOUT the necessary-direction
    clause  -e, x, bij, bji  (E[i][j] => X[i][j] v B[i][j] v B[j][i])."""
    clauses = []
    for (i, j) in ENC.PAIRS:
        e = ENC.E(i, j)
        x = ENC.X(i, j)
        bij = ENC.B(i, j)
        bji = ENC.B(j, i)
        clauses.append([-x, e])     # X -> E   (kept)
        clauses.append([-bij, e])   # B[i][j] -> E   (kept)
        clauses.append([-bji, e])   # B[j][i] -> E   (kept)
        # DROPPED: clauses.append([-e, x, bij, bji])   # E -> (X v B[i][j] v B[j][i])
    cs.add_group("cayley_edge_definition_NOREVERSE", clauses)


def group_r_step_definition_no_reverse(cs):
    """Same as ENC.group_r_step_definition but WITHOUT the necessary-direction
    clause  -rt, rprev, steps...  (R[t][v] => R[t-1][v] v OR_w STEP[t][w][v])."""
    clauses = []
    for t in range(1, ENC.NUM_STEPS_T + 1):
        for v in range(1, ENC.N + 1):
            rt = ENC.R(t, v)
            rprev = ENC.R(t - 1, v)
            steps = [ENC.STEP(t, w, v) for w in range(1, ENC.N + 1) if w != v]
            clauses.append([-rprev, rt])          # R[t-1][v] -> R[t][v]   (kept)
            for s in steps:
                clauses.append([-s, rt])          # STEP[t][w][v] -> R[t][v]   (kept)
            # DROPPED: clauses.append([-rt, rprev] + steps)
    cs.add_group("reachability_step_recurrence_NOREVERSE", clauses)


def build_transitive_clauses_mutant(kind):
    assert kind in ("reach_reverse_drop", "edge_reverse_drop")
    cs = ENC.build_class_clauses()
    if kind == "edge_reverse_drop":
        group_edge_definition_no_reverse(cs)
    else:
        ENC.group_edge_definition(cs)
    ENC.group_r_base_case(cs)
    ENC.group_step_definition(cs)
    if kind == "reach_reverse_drop":
        group_r_step_definition_no_reverse(cs)
    else:
        ENC.group_r_step_definition(cs)
    ENC.group_transitivity_goal(cs)
    return cs


PAPER_ARGUMENT = {
    "reach_reverse_drop": (
        "Dropping R[t][v] => R[t-1][v] v (OR_w STEP[t][w][v]) removes the only "
        "constraint that could ever force an R variable to FALSE; every R[t][v] "
        "can be set true with zero justification (they still satisfy the kept "
        "sufficient direction vacuously, since it is an implication INTO R). "
        "Setting all R[t>=1][v]=true in particular satisfies the transitivity "
        "goal clauses (R[20][v] for all v) regardless of the actual graph "
        "structure. Expected verdict: SAT (paper-proof, P85-6 point 1)."
    ),
    "edge_reverse_drop": (
        "Dropping E[i][j] => X[i][j] v B[i][j] v B[j][i] removes the only "
        "constraint that could ever force an E variable to FALSE; every E[i][j] "
        "can be set true with zero justification. Setting all E[i][j]=true turns "
        "the Cayley graph into the complete graph K_21, whose diameter is 1, so "
        "the (still-intact) R/STEP Tseitin machinery correctly derives R[t][v]=true "
        "for all v already at t=1 <= 20, again satisfying the transitivity goal "
        "regardless of the actual {a,b,b^-1} adjacency. Expected verdict: SAT "
        "(paper-proof, P85-6 point 2)."
    ),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(__file__), "out", "mutants"))
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    ENC._check_convention_against_fixture()

    results = {}
    for kind, fname in [
        ("reach_reverse_drop", "tail8_n21_mutant_reach_reverse_drop.cnf"),
        ("edge_reverse_drop", "tail8_n21_mutant_edge_reverse_drop.cnf"),
    ]:
        cs = build_transitive_clauses_mutant(kind)
        path = os.path.join(args.out_dir, fname)
        ENC.write_dimacs(
            path, ENC.TRANS_VAR_COUNT, cs,
            [
                f"n=21 tail-8 SAT calibration target -- MUTANT {kind} "
                "(sol/sol_reply_85_math12.md P85-6, Ruling 214 step 4).",
                "Expected: SAT (paper-proof, see PAPER_ARGUMENT in "
                "gen_mutants_reverse_drop.py).",
                "Generated by search/sat/gen_mutants_reverse_drop.py -- do not hand-edit.",
            ],
        )
        results[kind] = {
            "path": os.path.relpath(path).replace("\\", "/"),
            "num_vars": ENC.TRANS_VAR_COUNT,
            "num_clauses": cs.nclauses(),
            "sha256": ENC.sha256_of_file(path),
            "groups": cs.groups,
            "expected_verdict": "SAT",
            "expected_verdict_confidence": "PROVEN",
            "paper_argument": PAPER_ARGUMENT[kind],
        }

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
