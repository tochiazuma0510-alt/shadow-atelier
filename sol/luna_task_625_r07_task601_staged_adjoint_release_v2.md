# Luna Task625: staged-adjoint selected-SLP release v2

Role: Luna implementation.  Repair only the time-terminal leaf expansion of
Task601 according to v473, while preserving every Task622-accepted routing,
authentication, physical replay, compact receipt, and false-claim gate.

Create only these four versioned files:

1. `search/d972_r07_a0_grade1_selected_slp_v2.py`;
2. `search/check_d972_r07_a0_grade1_selected_slp_v2.py`;
3. `.github/workflows/d972-r07-a0-grade1-selected-slp-v2.yml`;
4. `sol/luna_reply_625_r07_task601_staged_adjoint_release_v2.md`.

Do not edit the v1 quartet, v220, proofs, Task623, or any other file.  Do not
run production, GHA, or git.  Run only bounded serial fixtures with bytecode
cache outside the repository.

## 1. Frozen parents and observed terminal

Copy semantics from these exact accepted-static v1 files:

- producer: 47,935 bytes, SHA-256
  `cfd581f8a71176f9252555a94028a8482ede862ee3430098270109e52fa0d3ff`;
- checker: 71,637 bytes, SHA-256
  `09ee815345e9ad2cfd80799a5bf7daf4446cda0eb3d8bc79bd7b3d9c61fa86c8`;
- workflow: 5,497 bytes, SHA-256
  `7f1b59790d2092fd93035742510ce7232834b4f7ea0a470507a408100d2e39cd`;
- Task622 final static audit: 8,106 bytes, SHA-256
  `4eaf1f92f4ef1fdd0a7f3289175d7c8b97c5ac85714b0b368d4aa66a20f151e0`;
- v473 staged theorem:
  `sol/proof_r07_selected_slp_staged_adjoint_v473.md` (compute and report its
  exact bytes/SHA-256 before use).

The real v1 GHA terminal is run/attempt `33723160379/1`, job
`100546373059`, head `6e0f0488e0698713317cb4f9d18a7de5e81a2316`, log artifact
id `9882116568`, artifact digest
`sha256:16aa8deccf54ad5f80330d700822268c78fbfd2b6687bcfc6e1445b5745b463c`.
Its producer log is 449,295 bytes, SHA-256
`b322c94d6e708a942aa03ca29a4bc6bb478c0a349b1e6726a1e7d26a4a0afd65`.
It reached the complete 8,059 route and selected source graph, then stopped
`UNKNOWN_RESOURCE:time` at 2,399.5 seconds with 159,383,552 pathwise states,
4,440 pending, 456 current leaves, maximum path length 21, RSS
1,420,152,832 and peak RSS 2,686,074,880 bytes.  No checker or selected
payload ran.  Do not raise the time limit as the repair.

## 2. Sole semantic repair: topological accumulation

Replace the producer's `pending.popitem()` pathwise reverse expansion by the
exact staged algorithm of v473:

```text
physical grade pivots descending;
physical lower pivots descending;
each character block pivots descending;
all defect origins;
each lifted-old character pivots descending;
leaves.
```

Maintain a sparse `path_id -> coefficient in F3` accumulator per reachable
node.  All incoming coefficients must meet before that node is expanded;
delete zero sums and release a node accumulator immediately afterward.  It is
permitted and preferred to intern freely reduced tuple words as compact
integer IDs, but tuple equality is the authority and the emitted leaf receipt
serializes exact tuples.  Preserve the v1 `word_mul/prepend` order exactly.
Never coalesce by a quotient endpoint, signature, hash alone, or seed alone.

Before expansion, validate every strict triangular edge in v473 (2.2),
including actor parents.  A forward edge, same-pivot edge, missing node,
cycle, or contribution to an already processed stage is a hard semantic
failure.  Report per-stage accumulated-state/expanded-state/path counts,
maximum live entries, maximum path length, final leaf count, wall, RSS, and
peak RSS.  Add explicit caps; cap exhaustion is `UNKNOWN_RESOURCE` and emits
no partial payload.

Keep all prior v1 output components and the compact binary leaf protocol, but
use a new v2 manifest schema and marker so it cannot be confused with the
failed v1 run.  Bind v473 and the exact scheduler statistics in the canonical
manifest.

## 3. Independent checker

The checker must not import the producer or a shared scheduler/interner.  It
must independently:

- authenticate and replay the full lower-first 8,059 route as in v1;
- authenticate the canonical selected source graph and exact roots;
- derive and check the complete triangular partial order;
- recompute the staged exact-path coefficient map;
- compare every byte of the compact leaf receipt; and
- complete the v1 physical replay, Task595 equation, receipts, and false
  claim gates.

The checker may use the same theorem and deterministic stage order, but its
data structures and word interning are locally implemented.  Preserve the
v1 rule that the preliminary lower replay uses only `declared_lower` and the
later authoritative replay consumes all 1,661/8,059 objects.

## 4. Required bounded fixtures

Retain every v1 fixture and add real scheduler-path fixtures for:

1. a diamond in which two identical `(node,path)` contributions cancel
   before expansion;
2. the same diamond plus a later third contribution;
3. actor concatenation with free cancellation at the boundary;
4. coefficient `2=-1`;
5. distinct exact words with an equal toy endpoint remaining distinct;
6. a forward or same-pivot reduction edge;
7. an actor parent which is not earlier;
8. a contribution to a processed stage/cycle attempt; and
9. state/path/time cap exhaustion returning only `UNKNOWN_RESOURCE`.

Fixtures must execute the production scheduler/validator, not a dictionary-
only surrogate.  Producer and checker each need their own fixtures.

## 5. Workflow and resource boundary

The workflow uses the same exact Task554/Task595 parents as v1, authenticates
the v2 executable hashes, runs producer and checker serially, uploads logs
always, and uploads the selected payload only after the independent checker
marker.  Keep the 8-GiB VM / 7-GiB RSS boundaries.  A 60-minute job is
permitted; do not enlarge it in this task.  Use artifact names containing
`task625` and `v2`.  Put the inert marker
`[fire-grade1-selected-slp-staged-v2]` in the workflow; root alone will
commit/push after Sol(max) static audit.

## 6. Reply

Report exact files, bytes, SHA-256, copied versus changed semantics, fixture
commands/results, scheduler statistics on bounded fixtures, resource caps,
and all remaining risks.  State explicitly that no production payload,
cross-check numerator, A0, COMMON, cofinal lift, fake, Ihara, or Lean
verification was produced.

