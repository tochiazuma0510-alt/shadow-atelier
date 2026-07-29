#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/sat/lrat_check.py

Independent LRAT checker requested in sol/sol_reply_85_math12.md P85-6
point 5 (裁定 214 工程 4): "an implementation separate from drat-trim that
reads the LRAT drat-trim produces" -- drat-trim both PRODUCES the LRAT
proof and (via its own DRAT check) VERIFIES the DRAT proof; this script
is a from-scratch, non-importing, deliberately minimal re-implementation
of the LRAT proof-checking algorithm.

Format (per the LRAT paper, Cruz-Filipe/Heule/Hunt/Kaufmann/
Schneider-Kamp, "Efficient Certified RAT Verification", CADE 2017,
https://www.cs.cmu.edu/~mheule/publications/lrat.pdf):

  addition line:
      <id> <lit_1> ... <lit_k> 0 <IDs> [-<D_id> <IDs>]* 0
  where the leading <IDs> block (possibly empty) lists unit-propagation
  hint clause ids attempting to prove the new clause directly via RUP
  (assume the negation of every literal of the new clause, then
  unit-propagate through the hinted clauses in order; a conflict/empty
  clause proves the new clause). If that alone succeeds, the clause is
  accepted -- no RAT check is needed or attempted.

  If the leading RUP attempt does not reach a conflict (including the
  case where the leading block is empty and there is nothing to
  propagate), the new clause must be RAT on its PIVOT literal (the first
  literal of the new clause, i.e. lits[0]): for every clause D currently
  in the database containing the NEGATED pivot, D must be listed as one
  of the `-<D_id> <IDs>` blocks, and the resolvent of the new clause and
  D (on the pivot) must be RUP-provable from the <IDs> hints that follow
  that block. A checker that merely trusts the -<D_id> markers without
  independently confirming they cover EVERY currently-active clause
  containing the negated pivot is unsound (a proof could omit an
  obligation); this implementation maintains a literal -> {active clause
  ids} occurrence index precisely so that completeness can be checked in
  O(occurrences) per step rather than by scanning the whole database.

  A hint list that is COMPLETELY EMPTY (leading run empty, zero RAT
  blocks) is legitimate exactly when the pivot literal is fresh, i.e. no
  currently active clause contains its negation -- this is the "vacuous
  RAT" case used by solvers to introduce definitional/extension
  variables (kissat's inprocessing can add clauses on brand-new
  variables beyond the original CNF's declared var count; a correct LRAT
  checker must NOT reject this as "hints exhausted without a conflict"
  -- it must instead verify the vacuity, i.e. that occ[-pivot] is empty).

  deletion line:  <id> d <id_1> ... <id_j> 0

Checking terminates successfully ("s VERIFIED") the moment the empty
clause is derived by an addition line -- matching kissat/drat-trim's own
convention that an UNSAT proof closes by deriving the empty clause.

This mirrors the reference LRAT-checking algorithm from the paper above,
written from scratch here in Python with no shared code with drat-trim
(the tool that produced the proof.lrat file this script reads) --
searcher/checker separation per CLAUDE.md: drat-trim is the "explorer"
side's own proof producer, this script is the independent crosscheck
that reads only its OUTPUT (proof.lrat + the original problem.cnf),
never drat-trim's source code or intermediate state.

Usage:
  python lrat_check.py --cnf problem.cnf --lrat proof.lrat[.gz]
  python lrat_check.py --self-test

Exit code 0 + "s VERIFIED" on success, exit code 1 otherwise. Fail-closed:
any malformed line, missing RAT obligation, or hint that doesn't resolve
to a conflict causes rejection -- no silent leniency.
"""
import argparse
import gzip
import sys
import time


def _open_maybe_gz(path, mode="rt"):
    if path.endswith(".gz"):
        return gzip.open(path, mode)
    return open(path, mode, encoding="ascii")


def parse_cnf(path):
    clauses = {}
    next_id = 1
    with _open_maybe_gz(path) as f:
        for line in f:
            line = line.strip()
            if not line or line[0] == "c" or line[0] == "p":
                continue
            lits = [int(x) for x in line.split()]
            assert lits[-1] == 0, f"clause not zero-terminated: {line!r}"
            clauses[next_id] = lits[:-1]
            next_id += 1
    return clauses, next_id - 1


def parse_lrat_lines(path):
    with _open_maybe_gz(path) as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            toks = line.split()
            cid = int(toks[0])
            if toks[1] == "d":
                ids = [int(x) for x in toks[2:]]
                assert ids[-1] == 0
                yield ("d", cid, ids[:-1])
            else:
                rest = [int(x) for x in toks[1:]]
                zero_idx = rest.index(0)
                lits = rest[:zero_idx]
                hints = rest[zero_idx + 1:]
                assert hints[-1] == 0, f"hint list not zero-terminated: {line!r}"
                hints = hints[:-1]
                yield ("a", cid, lits, hints)


def split_hints(hints):
    """Splits a hint list into (leading_ids, blocks) where blocks is a
    list of (D_id, ids) pairs, per the LRAT format's
    '<IDs> [-<D_id> <IDs>]*' grammar."""
    leading = []
    blocks = []
    cur_marker = None
    cur_ids = []
    for h in hints:
        if h < 0:
            if cur_marker is None:
                leading = cur_ids
            else:
                blocks.append((-cur_marker, cur_ids))
            cur_marker = h
            cur_ids = []
        else:
            cur_ids.append(h)
    if cur_marker is None:
        leading = cur_ids
    else:
        blocks.append((-cur_marker, cur_ids))
    return leading, blocks


class Trail:
    """Supports mark()/undo_to() so a shared, cumulative assignment can be
    used across the leading RUP run and each RAT block in turn, with each
    block's block-local extra assumptions rolled back before the next
    block starts (matching the reference lrat-check.c epoch-scoped mask
    array: the clause's own negated literals + everything derived from
    the leading hints stay in effect for the WHOLE addition-line check;
    each RAT block's extra "D \\ {-pivot}" assumptions are scoped to that
    block only)."""

    def __init__(self):
        self.assigned = {}
        self.order = []

    def is_true(self, lit):
        return self.assigned.get(lit) is True

    def is_false(self, lit):
        return self.assigned.get(-lit) is True

    def assign(self, lit):
        if lit in self.assigned:
            return
        self.assigned[lit] = True
        self.order.append(lit)

    def mark(self):
        return len(self.order)

    def undo_to(self, mark):
        while len(self.order) > mark:
            lit = self.order.pop()
            del self.assigned[lit]


def clause_status(clause, trail):
    """('sat'|'conflict'|'unit', unit_lit_or_None)."""
    unassigned = None
    for lit in clause:
        if trail.is_true(lit):
            return ("sat", None)
        if not trail.is_false(lit):
            if unassigned is not None:
                return ("unresolved", None)
            unassigned = lit
    if unassigned is None:
        return ("conflict", None)
    return ("unit", unassigned)


def propagate(db, trail, hint_ids):
    """Unit-propagate hint_ids (all positive clause ids present in db)
    against the CURRENT trail (not reset here -- caller controls that).
    Returns ('conflict', None) | ('exhausted', None) | ('error', msg)."""
    for h in hint_ids:
        if h not in db:
            return "error", f"hint clause id {h} not active in database"
        status, lit = clause_status(db[h], trail)
        if status == "conflict":
            return "conflict", None
        if status == "unit":
            trail.assign(lit)
        elif status == "sat":
            return "error", f"hint clause {h} already satisfied under trail (not unit)"
        else:
            return "error", f"hint clause {h} not unit under trail (hint order/soundness violated)"
    return "exhausted", None


class LratChecker:
    def __init__(self, cnf_path):
        self.db, _ = parse_cnf(cnf_path)
        self.occ = {}
        for cid, lits in self.db.items():
            for lit in lits:
                self.occ.setdefault(lit, set()).add(cid)

    def _register(self, cid, lits):
        self.db[cid] = lits
        for lit in lits:
            self.occ.setdefault(lit, set()).add(cid)

    def _delete(self, cid):
        lits = self.db.pop(cid, None)
        if lits is None:
            return
        for lit in lits:
            s = self.occ.get(lit)
            if s is not None:
                s.discard(cid)

    def check_addition(self, cid, lits, hints):
        leading, blocks = split_hints(hints)

        trail = Trail()
        if not lits:
            res, info = propagate(self.db, trail, leading)
            if res != "conflict":
                return False, info or "hints exhausted without reaching a conflict"
            self._register(cid, lits)
            return True, None

        # Assume the negation of every literal of the new clause. This
        # "base layer" of the trail persists for the ENTIRE check below
        # (leading run AND every RAT block), matching the reference
        # lrat-check.c algorithm (the clause's own assumed-false literals
        # and everything unit-propagated from the leading hints stay in
        # scope for all subsequent RAT sub-obligations -- only each
        # block's OWN extra assumptions from resolving against D are
        # rolled back before the next block).
        trivial = False
        for l in lits:
            if trail.is_true(-l):
                trivial = True
                break
            trail.assign(-l)
        if trivial:
            self._register(cid, lits)
            return True, None

        res, info = propagate(self.db, trail, leading)
        if res == "conflict":
            self._register(cid, lits)
            return True, None
        if res == "error":
            return False, info

        pivot = lits[0]
        required_D = set(self.occ.get(-pivot, set()))
        listed_D = set(d for d, _ in blocks)

        if not blocks:
            # No RAT markers at all: only acceptable if there is genuinely
            # nothing to resolve against (vacuous RAT on a fresh/unused
            # pivot polarity) -- verified independently via the occurrence
            # index, not merely trusted from the (empty) hint list.
            if required_D:
                return False, (
                    f"clause not RUP from leading hints, and no RAT blocks given, "
                    f"but {len(required_D)} active clause(s) contain the negated "
                    f"pivot {-pivot} (e.g. {sorted(required_D)[:5]})"
                )
            self._register(cid, lits)
            return True, None

        if required_D != listed_D:
            missing = required_D - listed_D
            extra = listed_D - required_D
            return False, (
                f"RAT obligation mismatch for pivot {pivot}: "
                f"missing={sorted(missing)[:10]} extra={sorted(extra)[:10]}"
            )

        base_mark = trail.mark()
        for D_id, ids in blocks:
            trail.undo_to(base_mark)
            blocked = False
            for clit in self.db[D_id]:
                if clit == -pivot:
                    continue
                if trail.is_false(clit):
                    continue
                if trail.is_true(clit):
                    blocked = True
                    break
                trail.assign(-clit)
            if blocked:
                continue
            res2, info2 = propagate(self.db, trail, ids)
            if res2 != "conflict":
                return False, (
                    f"RAT sub-obligation vs clause {D_id} failed: "
                    f"{info2 or 'hints exhausted without reaching a conflict'}"
                )
        trail.undo_to(base_mark)

        self._register(cid, lits)
        return True, None

    def run(self, lrat_path):
        n_lines = 0
        for entry in parse_lrat_lines(lrat_path):
            n_lines += 1
            if entry[0] == "d":
                _, cid, ids = entry
                for i in ids:
                    self._delete(i)
                continue
            _, cid, lits, hints = entry
            ok, err = self.check_addition(cid, lits, hints)
            if not ok:
                return {
                    "verified": False,
                    "reason": f"line {n_lines} (clause id {cid}): {err}",
                    "lines_processed": n_lines,
                }
            if lits == []:
                return {"verified": True, "reason": None, "lines_processed": n_lines}
        return {
            "verified": False,
            "reason": "no empty clause derived by end of proof",
            "lines_processed": n_lines,
        }


def check_lrat(cnf_path, lrat_path):
    checker = LratChecker(cnf_path)
    return checker.run(lrat_path)


def self_test():
    """Two hand-built smoke instances (this script checking proofs it can
    also be manually inspected against), NOT an external oracle -- the
    real calibration is running this checker against drat-trim's own
    proof.lrat output for the n=21 transitive target
    (search/sat/runs/n21_transitive/proof.lrat.gz) and comparing the
    verdict to drat_verify.txt's 's VERIFIED'."""
    import os
    import tempfile

    results = {}

    # Test 1: pure RUP, no RAT needed.
    cnf1 = "p cnf 2 3\n1 0\n-1 2 0\n-2 0\n"
    lrat1 = "4 2 0 1 2 0\n5 0 4 3 0\n"
    with tempfile.TemporaryDirectory() as d:
        cnf_p = os.path.join(d, "t.cnf")
        lrat_p = os.path.join(d, "t.lrat")
        open(cnf_p, "w").write(cnf1)
        open(lrat_p, "w").write(lrat1)
        results["pure_rup"] = check_lrat(cnf_p, lrat_p)

    # Test 2: a bogus proof (hint clause is not actually unit) -- must be
    # rejected (fail-closed check).
    bad_lrat = "4 2 0 3 0\n5 0 4 3 0\n"
    with tempfile.TemporaryDirectory() as d:
        cnf_p = os.path.join(d, "t.cnf")
        lrat_p = os.path.join(d, "t.lrat")
        open(cnf_p, "w").write(cnf1)
        open(lrat_p, "w").write(bad_lrat)
        results["bogus_proof_rejected"] = check_lrat(cnf_p, lrat_p)

    # Test 3: genuine RAT step with a fresh extension variable, mirroring
    # the pattern observed in the real n=21 transitive proof (definitional
    # clauses on a brand-new variable, vacuous RAT, hints == []).
    # CNF: (x1) & (-x1 v x2) -- SAT alone (x1=T,x2=T), but we add a fresh
    # var x3 via RAT clauses (x3 v -x2) [pivot x3, vacuous: no clause has
    # -x3 yet] and (-x3 v -x2) [pivot -x3, RAT vs the just-added clause,
    # resolvent is (-x2 v -x2)=(-x2), RUP-provable via hint to clause 1&2
    # forcing x2 true then unit -x2 false is the conflict]... to keep this
    # simple and decisively falsifiable, we instead force UNSAT directly:
    # (x1)&(-x1 v x2)&(-x2) as before, but derive the intermediate unit
    # clause (x2) via an explicit fresh-pivot RAT step first, matching the
    # "9724 -18 ... 0 0" vacuous pattern from the real proof.
    cnf3 = "p cnf 2 3\n1 0\n-1 2 0\n-2 0\n"
    # id 4: fresh var 3, clause (3 -2), pivot=3 fresh -> vacuous RAT, hints=[]
    # id 5: clause (2), RAT on pivot 2? simpler: just RUP it from 1,2 directly.
    # id 6: clause (-3) is NOT needed; instead derive empty via id4's clause
    # combined with unit propagation is not enough without x3's polarity
    # fixed, so this test instead just confirms id4 (vacuous RAT, fresh
    # var, empty hints) is ACCEPTED without breaking the rest of a normal
    # proof appended after it.
    lrat3 = "4 3 -2 0 0\n5 2 0 1 2 0\n6 0 5 3 0\n"
    with tempfile.TemporaryDirectory() as d:
        cnf_p = os.path.join(d, "t.cnf")
        lrat_p = os.path.join(d, "t.lrat")
        open(cnf_p, "w").write(cnf3)
        open(lrat_p, "w").write(lrat3)
        results["vacuous_rat_fresh_var"] = check_lrat(cnf_p, lrat_p)

    ok = (
        results["pure_rup"]["verified"] is True
        and results["bogus_proof_rejected"]["verified"] is False
        and results["vacuous_rat_fresh_var"]["verified"] is True
    )
    print({"self_test": results, "pass": ok})
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cnf")
    ap.add_argument("--lrat")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        ok = self_test()
        sys.exit(0 if ok else 1)

    if not args.cnf or not args.lrat:
        ap.error("--cnf and --lrat are required (or use --self-test)")

    t0 = time.time()
    result = check_lrat(args.cnf, args.lrat)
    result["elapsed_seconds"] = round(time.time() - t0, 3)
    if result["verified"]:
        print("s VERIFIED")
    else:
        print("s NOT VERIFIED")
    print(result)
    sys.exit(0 if result["verified"] else 1)


if __name__ == "__main__":
    main()
