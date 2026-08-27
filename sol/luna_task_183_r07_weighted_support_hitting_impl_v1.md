# Luna task 183 — task179 weighted-support hitting implementation v1

Commissioner: Sol / 2026-08-27

Role: Luna bounded mechanical implementation/static audit after task182.
Do not run Python, Node, GAP, git, or GHA locally.

## 1. Governing theorem and sequencing

Read and implement exactly
`sol/proof_r07_actual_weighted_support_hitting_selector_v143.md`.
This task is a follow-up to task182 and edits the same task179 bundle; do not
start it until the parent confirms task182's changes are complete.

## 2. Runtime kernel-order gate

From the live task176 data reconstruct and require

```text
Delta order = 357128352
kernel orders by coordinate = [9,9,9,9,9,1,1,1,3,3]
```

For each coordinate, prove at runtime that the word-bearing kernel BFS from
`Gamma_S0_generators + adjusted_L_generators` has exactly the registered
order, has no duplicate ten-coordinate state, and every state is identity in
the selected coordinate.  Do not infer completeness from a prefix length.

## 3. Replace the unstructured kernel/global loop

For every merged formula compute

```text
W = sum(kernel_order[coordinate] for each distinct merged support target)
```

using all nonzero merged terms; an empty target fibre may remain in the upper
bound.

- If `K == 0`, enumerate every nonempty support fibre completely in frozen
  `(coordinate,target)` order.  Each fibre uses task182's least representative
  and the complete kernel roster.  A hit is accepted only by the existing
  full formula/direct-column equality.  After complete exhaustion this row
  may be skipped, but no receipt-level separator/negative claim is allowed.
- If `K != 0` and `W < 357128352`, evaluate the first `W+1` distinct elements
  of the authenticated global `(q,gamma)` roster.  The roster order and
  distinctness are already task176 data and must be rebound exactly.  Stop at
  the first full direct hit.
- If `K != 0` and `W >= 357128352`, retain an honest resumable fair global
  fallback.  Exhaustion/caps are typed `UNKNOWN_RESOURCE` only.

The schedule must checkpoint within a row: record roster index, formula
digest, K, W, support-fibre cursor/kernel cursor, global prefix, and whether
the row is completely exhausted.  A resume may repeat the last candidate but
must never skip one.

## 4. Preserve positive soundness

Do not change:

- the negative task175 raw base target;
- the eleven occurrence signs/order or internal positive-factor transport;
- boundary correlation;
- exact dual/rank gates;
- coefficient-2 inverse word materialization;
- PB3/PB4 boundary/source type separation; or
- COMMON/UNKNOWN claim boundaries.

The helper-nonshared checker need not replay an unsuccessful bound.  For an
ACTIVE correction it independently recomputes K, the merged support, W, the
literal global/fibre candidate, full scalar, direct column, and rank increase.

## 5. SELFTEST additions

Extend the finite noncommutative SELFTEST, without removing the existing 15
mutations, to cover:

1. `K=0` with a hit only at the last point of a nontrivial kernel fibre;
2. `K=0` complete support exhaustion and row skip;
3. `K!=0`, a union of size at most W containing the first W global points,
   with the guaranteed hit at point W+1;
4. one overstated/understated kernel order;
5. one omitted merged target from W;
6. a repeated global element falsely counted as distinct; and
7. a completed-row cursor advanced past an untested candidate.

All semantic mutations must enter normal validators.  Whole-dictionary
equality is not a mutation oracle.

## 6. Authorized files and report

Edit only the task179 producer/checker/driver/fixture and
`sol/luna_reply_183_r07_weighted_support_hitting_impl_v1.md`.  Do not edit
task175, task176, proofs, workflows, or any other file.  Parent performs the
final predecessor/source pin cascade, commit, push, SELFTEST, and GHA
production.

Report exact bytes/SHA, the completed-path candidate bounds, checkpoint
schema changes, and any remaining runtime blocker.
