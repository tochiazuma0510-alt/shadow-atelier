# Luna task 499 - A4 intra-query physical-shard resume v1

Role: Luna implementation only.  This is parallel v220/A4 work and must not
touch A0, Task193, Task496, workflows, git, GHA or production.  Read in full:

- `sol/proof_r07_a4_intraquery_physical_shard_resume_v425.md`;
- `sol/proof_r07_a4_terminal_resource_witness_v423.md`;
- `sol/proof_r07_a4_resumed_resource_counter_transport_erratum_v429.md`;
- Task443/446/449 replies and Task483/485 replies;
- exact v22 producer, v28 checker, v31 checker and v41 driver owners.

Implement v425 without changing A4 arithmetic, row order, legal source
universe, membership/correlation order, rank rules, K/queue rules, evaluator,
resource caps or terminal meanings.  This task solves only the loss of all
open-row work at a wall stop.

## 1. Exact frozen premises

- producer wrapper v22: 4055 /
  `0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2`;
  generated v22: 256509 /
  `20fdeb66f70f428152e06f5e7a92b455dd211bd0e72d665c10d24d2ad0491e94`;
- checker wrapper v31: 19483 /
  `7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e`;
  generated v31: 288650 /
  `89d8626f8c14972ccad21efa441de07e5e9cf1baf18f98a68751f8bc16e46744`;
- production-envelope owner v41: 2674 /
  `002dcea0d78bb14252e975ff69311f596aac742392658a9b7fb7022cf5c17bbd`.

The immutable row-26 source is release
`artifact_9809473723_gap-run-out.a4-row26.zip`, 56410 /
`5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`.
Use all six exact member pins from Task485.  In particular the authenticated
HEAD is 700 / `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114`,
with deltas 1 and 2 pinned there; it closes row 26 and resumes at row 27.  Do
not claim or attempt to recover the lost transient row-27 rank 138592.

## 2. Outputs only

Create only:

1. `search/d972_r07_word_independent_successor_kernel_v23.py`;
2. `crosscheck/check_d972_r07_word_independent_successor_kernel_v32.py`;
3. `search/d972_r07_word_independent_successor_kernel_gha_driver_v42.g`;
4. `sol/luna_reply_499_r07_a4_intraquery_physical_shard_resume_v1.md`.

Use exact-pin, cardinality-checked in-memory successors.  Do not overwrite any
owner and do not create a second implementation path.

## 3. Producer durability contract

Implement v425 literally:

- split one row into `prepare`, `query`, `commit`; completed row/bridge
  prefixes exclude the open row;
- `open_query` seals row id, source word, target, bridge trace, row/sample
  digests and owns `R:27` until a unique terminal;
- inside the existing correlation traversal, close one canonical batch after
  every 64 fully examined candidates (`q=1` for this first implementation);
- a physical shard contains every accepted rise from that batch: raw identity,
  normalized boundary and combined packed rows, chronological pivots/labels,
  boundary and combined formal reductions, `b_coefficients`, `b_formals`,
  event/epoch/counter transitions and batch offsets/digest chain;
- write a temporary shard, flush+fsync, atomically install it, then atomically
  replace a small HEAD.  An open batch is absent after interruption;
- resume authenticates base + ordered shard chain, direct-loads the two
  echelons/formals/events without rerunning insertion/reduction, binds the
  pending-query equation and continues at the next unexamined candidate;
- after a row terminal, ordinary row delta commit happens once, clears
  `open_query`, advances `next_row`, and makes the shard head obsolete;
- RESOURCE publishes only the last closed shard HEAD.  Never serialize a
  whole duplicate matrix snapshot, keep every historical checkpoint in RAM,
  or rebuild all earlier boundaries merely to resume.

The producer may direct-load authenticated physical rows only as candidate
computation.  It must not mark them independently replayed or cross-checked.

## 4. Independent checker

V32 must not import v23.  Starting from the exact generated v31 mathematics,
authenticate the v23 source pin and independently validate every v425 gate:
ordered/unique sealed shards; HEAD not ahead; chronological pivot normal form;
physical row recreated from raw identity; both reductions/formal ledgers;
event, epoch and counter transition; pending-query target/word/bridge/sample
digests; no open-row occurrence in completed prefixes; no duplicate terminal;
and exact final state/terminal equality with uninterrupted execution.

Keep v423's unique resource excess and v429's transport difference relation.
Do not embed acceptance of the observed row-26 result as a substitute for
generic shard validation.

## 5. Driver and bounded gates

V42 must exact-pin v41 and change only the producer/checker/output/shard
dialect needed above.  Reuse the authenticated row-26 base/delta1/delta2/HEAD
seed and resume at row 27.  Preserve v41 resource limits and its behavior that
a RESOURCE producer uploads its durable candidate without paying a second
full semantic checker; only a positive/nonresource result may invoke the full
checker.  No SELFTEST path, retry, worker pool, extra traversal or workflow
change in production.

Run only bounded local gates:

- AST and generated-source pins/diff confinement;
- tiny synthetic uninterrupted versus interruptions after at least three
  closed 64-candidate batches, requiring exact final equality;
- mutations for every v425 independent gate, including HEAD-ahead and
  physical-row/raw-identity drift;
- proof that restore calls no insertion/reduction routine for admitted shard
  entries;
- bounded memory/copy audit: no complete matrix JSON snapshot and no
  quadratic cumulative-prefix copy;
- exact row26 seed reconstruction, GAP `ReadAsFunction`, and generated shell
  syntax.

Do not run the real 6441-row computation, GAP production, GHA or git.  Report
exact bytes/SHA and a concise semantic diff.  Mathematical status stays A4
1/3 UNKNOWN_RESOURCE, cross-checked through row 26; SELFTEST is not progress.
End with exactly one of:

`TASK499_R07_A4_INTRAQUERY_PHYSICAL_SHARD_RESUME_PASS`

or

`TASK499_R07_A4_INTRAQUERY_PHYSICAL_SHARD_RESUME_STOP`
