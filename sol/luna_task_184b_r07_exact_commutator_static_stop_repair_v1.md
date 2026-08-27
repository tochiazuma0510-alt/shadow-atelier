# Luna task 184b — exact-commutator static STOP repair v1

Commissioner: Sol / 2026-08-27

Reply by updating:
`sol/luna_reply_184_r07_exact_commutator_common_word_v1.md`.

Role: bounded mechanical repair.  Read task184 and v145--v146 in full.  The
first task184 delivery is **STATIC STOP** and must not be run or promoted.
Repair its four implementation/fixture files in place before parent audit.
Do not run Python, GAP, git, or GHA locally.

## 1. Exact live pin cascade

Replace the stale task175 producer/driver pins in both producer and checker:

```text
search/d972_r07_all_seven_raw_bridge_preflight_v1.py
  60306 / 1e0a65f5182157bb928638c2c9a71d475b3b788a6694ee4ded09f5a0ffd38cfa
crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py
  85848 / c55ec99a9a920cd5d0ef92db7d5f2ad841dda7b0f1dcc59a5dc45e469ed6f7cc
search/d972_r07_all_seven_raw_bridge_preflight_gha_driver_v1.g
  21580 / dbe147f98774fde50dee86de7306f9e18243ac1becef0ec7516765bcb2e08765
```

Retain the current task179 pins exactly:

```text
producer 119396 / 448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512
checker   70020  / 473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d
driver    12872  / fbab67e85de604f157f8bd93f53d64e7265121508aa948c1e01341e78d1b5a11
```

Authenticate every transitive pin before parsing the input artifact.  Bind
the theorem in v146 that the complete 6,441-row roster normally generates
the correction kernel; do not certify `L=exp(Omega)` with an unchecked text
flag.

## 2. Implement the missing augmented positive continuation

The current code's `upgrade_columns` plus immediate
`LATTICE_AUGMENTED_RESUME_REQUIRED` is not the commissioned resumable search.
For both a task179 checkpoint and a COMMON_WORD whose exponent is not in
`3L`, implement the actual v146 augmented continuation:

1. reconstruct the authenticated task179 runtime and target;
2. append the `L/3L` tail to every correction column and zero tail to every
   boundary column;
3. rebuild the complete retained echelon in frozen order;
4. discard/reset the old dual, all old oracle cursors, and pending oracle
   claims;
5. run the task179 boundary/correction column-generation schedule in the
   augmented space under registered time/RSS/column/checkpoint caps;
6. include `lambda_L dot residue(relator)` in every correction weighted
   scalar and never include conjugator exponent;
7. on membership, recover coefficients, materialize the signed ordinary
   word, prove its exponent lies in `3L`, attach the fixed roster-order cube
   tail, and perform all direct replays; and
8. on a cap, write a complete resumable **task184 augmented checkpoint** with
   commitment, rebuilt pivots, current dual, fresh cursors, counters, and
   integrity digest.

An inspection-only handoff may remain available under explicit `INSPECT`
mode.  `PRODUCTION` must either continue the augmented search or return a
typed `UNKNOWN_RESOURCE/UNKNOWN_INPUT`; it may not call an unimplemented
resume a successful task184 outcome.

## 3. Replace asserted replay booleans by computations

The current `exactify_receipt` evaluates only exponent and joint-group
identity, then writes these fields as constants:

```text
cube_tail_all_seven_change_zero = True
hexagons = True
pentagon_printed_order = True
boundary_chains_not_inserted = True
```

This is forbidden.  Recompute from literal words:

- the complete task179 sparse target equality;
- zero all-seven relation-module change of every used cube tail;
- joint finite identity;
- both direct hexagons;
- all five pentagon cofaces with frozen order and signs;
- the corrected word `reduce(g760 + exact_correction_word)`; and
- absence of boundary words in the source-word provenance.

Retain the raw computed values/digests.  A boolean may be emitted only after
the underlying calculation has passed.

## 4. Production checker must be genuinely independent

The current production checker only reads the task184 receipt and accepts
`exact_exponent == [0,0]` plus an asserted `joint_identity` boolean.  Replace
that branch completely.

The driver must pass the exact original task179 artifact, its required SHA,
the task184 receipt/checkpoint, and all relevant source pins to the checker.
The checker must not import either producer.  It may load the independently
pinned task179/task175 checker arithmetic only after recording a helper
firewall.  It must independently:

1. authenticate and parse the original task179 artifact;
2. reconstruct all 6,441 literal roster words and exponent pairs;
3. rebuild its own canonical rank-0/1/2 integer lattice and transformations;
4. compare every lattice row/coordinate/digest, not just rank/basis;
5. reconstruct every retained augmented column and rank transition;
6. check the new dual/cursor reset and, on continuation, every ACTIVE column;
7. recover signed coefficients independently, including coefficient `2` by
   literal inversion;
8. independently solve and replay the sparse cube coefficients;
9. materialize the final literal word; and
10. recompute exponent zero, joint identity, sparse target identity, both
    hexagons, all five pentagon cofaces, and boundary reductions.

For a task184 UNKNOWN checkpoint, independently authenticate all checkpoint
commitments/counters and absence of negative/fake/cofinal/Ihara claims.
Never trust a producer replay flag as evidence.

## 5. Lattice and receipt corrections

- Return `q_j` sparsely as named `(roster_index, coefficient)` entries in
  fixed roster order; a dense 6,441-entry vector may be an internal value.
- Retain every nonempty literal cube word and both unreduced/reduced tail
  digests.  Bind the relation word from which each cube came.
- Prove membership in `3L` before integer division.
- Record integer exponent before tail, tail exponent, and exact round trip.
- Check rank 0, rank 1, and non-primitive rank 2 lattices.  Canonical basis,
  coordinates, basis combinations, determinant/index, and invariant factors
  must all round-trip exactly.

## 6. SELFTEST must exercise real code paths

The current fixed toy and mutation checks mostly alter asserted fields and do
not meet task184 Section 7.  Extend SELFTEST so the actual production lattice,
checkpoint-upgrade, augmented solve, cube materialization, and direct replay
paths run on the proper-sublattice noncommutative toy.  Exhaustively enumerate
a bounded deterministic family of small rank-0/1/2 lattices and compare both
independent implementations with brute-force membership/index data.

Each of the 17 destructive controls must mutate an input, retained column,
word, coefficient, or computed receipt and be rejected by recomputation.
In particular, changing a producer boolean while the underlying word is
unchanged is not a substitute for the required replay mutation.

## 7. Driver and terminal gates

- Pin the repaired producer/checker/fixture identities exactly.
- In PRODUCTION, distinguish task179 receipt from checkpoint and pass the
  correct CLI option.
- Pass the original task179 input to the checker with exact bytes/SHA.
- Require exactly one allowed terminal and its matching checker marker.
- Do not write `.ok` merely because both processes exited zero.
- Preserve/upload a task184 checkpoint for every resource stop.
- A programming exception is a failed job, never `UNKNOWN`.

## 8. Reply and claim boundary

Update the task184 reply with a numbered disposition of all seven repair
sections, exact identities, and `STATIC GO` or remaining `STATIC STOP`.
Do not claim execution before parent GHA SELFTEST.  End with the original four
claim-boundary lines.

