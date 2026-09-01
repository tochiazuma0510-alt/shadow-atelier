# Luna task 503 - A4 actual production shard wiring v1

Role: Luna implementation only.  Task502 rejected Task499 because both shard
helpers were unreachable and v42 did not execute its transport.  Repair those
exact defects; do not alter A4 mathematics, the legal-source order, resource
caps, terminal meanings, A0, Task193, workflows, git, GHA or production.

Read in full:

- `sol/proof_r07_a4_actual_production_shard_wiring_v430.md`, 7137 /
  `acea72aea1a8f62a3de1c84a7bf4cab95fc4da85162bbe226b1a5f158755a904`;
- v425, v423 and v429;
- Task499 and Task502 replies;
- the exact v22 producer, v31 checker, v41 driver, and Task483 checker-only v3
  transport driver.

Task502's rejected v23/v32/v42 files are exact transformation references only:

- v23 14472 /
  `d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a`;
- v32 10036 /
  `8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0`;
- v42 4362 /
  `650b1d052dbae8df65b2b8a4e8b7a33ab6f9c66d7b74117600e361b1dfa74629`.

Do not edit them.

## 1. Outputs only

Create only:

1. `search/d972_r07_word_independent_successor_kernel_v24.py`;
2. `crosscheck/check_d972_r07_word_independent_successor_kernel_v33.py`;
3. `search/d972_r07_word_independent_successor_kernel_gha_driver_v43.g`;
4. `sol/luna_reply_503_r07_a4_actual_production_shard_wiring_v1.md`.

Use exact-pin/cardinality-checked successors.  Do not create a second helper-
only path and do not run the real 6,441-row computation.

## 2. Producer: wire the real call graph

Implement v430 in the generated production body.  The real, non-SELFTEST call
graph must construct/restore one physical controller in `build_kernel`, call
`prepare` from `consume_row`, call `close_batch` from the actual
`Oracle.query` correlation loop, direct-restore before that loop continues,
and call `commit` after its unique row terminal.

In particular:

- move the current pre-query appends to bridge/row/chunk/sample completed
  prefixes into commit;
- one batch owns the `m=min(64,len(private_candidates))` fully examined
  prefix, its ordered identity/coefficient digest and accepted mask; do not
  confuse `m` with the number of accepted rises;
- capture every accepted rise's real boundary/combined insertion details,
  formal/ledger/coefficient state, insertion/query events, epochs, ranks and
  semantic-counter transition from the live `LiveBasis.add_boundary` path;
- durably write the sealed shard then HEAD with existing `write_atomic`;
- on restore, load authenticated physical maps/formals/events/counters
  directly, with no `insert`, `reduce`, `correlate` or raw-boundary replay for
  admitted shard entries;
- expose typed CLI paths for the physical root/HEAD.  A first row-27 run has
  no physical HEAD; a later run may restore one while using the same sealed
  completed-row base;
- on ResourceStop publish a typed `physical_shard_chain` checkpoint reference
  whenever at least one closed batch exists, binding the ordinary completed-
  row delta HEAD, open query, physical HEAD and exact ordered shard identities.
  Before the first closed batch, the ordinary row-26 delta reference remains
  valid;
- after MEMBER/ZERO, append the completed row data once, write the ordinary
  row delta once, and mark the physical HEAD obsolete.

No complete physical matrix snapshot, cumulative shard-prefix rewrite,
historical-checkpoint retention, dense conversion, or repeated earlier-
boundary closure is permitted.

## 3. Independent checker: wire the real acceptance path

V33 must not import v24 or call its helper.  Extend the actual
`validate_terminal_checkpoint`/producer-acceptance route for a
`physical_shard_chain` reference.  Starting from the authenticated ordinary
base, independently recompute each batch's dual, correlation roster and exact
`m`-candidate prefix; sequentially recompute its accepted mask and every
accepted boundary/combined reduction, formal transition, event, epoch, rank
and semantic-counter delta.  Compare full values, not only producer digests.

Reject an omitted accepted rise, an extra physical entry, reordered/missing
or mixed-row shards, stale/open-query drift, HEAD ahead, an open row in a
completed prefix, and a duplicate terminal.  Retain v423's unique resource
excess and v429's exact completed-counter transport relation.  The ordinary
positive replay path remains extensionally v31.

## 4. Executable v43 transport

V43 must make every pin executable.  Reuse the exact immutable row-26 release
transport from
`search/d972_r07_word_independent_successor_kernel_row26_checker_only_gha_driver_v3.g`
rather than v42's assignment-only registry:

- release 56410 /
  `5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3`;
- authenticate and install all six Task483 member pins, including row-26 HEAD
  700 /
  `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114`
  and delta2 3625 /
  `acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523`.

Then run exactly one v24 producer from that row-26 HEAD with a distinct v24
physical root.  Preserve v41's 14,400-second/8-GB internal caps and external
margin.  A RESOURCE result is uploaded without a second full checker; only a
positive/nonresource result invokes exactly one v33 checker.  Require exact
owned one-line terminal markers, nonempty owned outputs, and reject
UNKNOWN_INPUT/HARD_STOP/ERROR/Traceback.  Do not add SELFTEST, retry search,
worker pool, fallback traversal or workflow changes.  Generated producer and
checker hashes, release hash, and every member hash must be checked by commands
actually reached before the producer.

## 5. Bounded gates

Run only bounded tests:

1. exact owner/generated pins, patch cardinalities, AST and diff confinement;
2. a tiny fixture entering the real production `main -> consume_row ->
   Oracle.query` route, with at least three closed batches, interruption and
   CLI restore, exactly equal to uninterrupted completion;
3. positive non-SELFTEST call counts for producer `prepare`, `close_batch`,
   direct restore and `commit`, and checker physical validation;
4. independently re-sealed mutations for every v430 field, especially
   accepted-mask omission/extra-entry and physical-row/raw-identity drift;
5. instrumentation which raises if restore calls insertion/reduction/
   correlation for admitted entries;
6. bounded copy/memory audit excluding full matrix JSON and cumulative-prefix
   copying;
7. v43 exact source/generated/release/six-member command reachability, GAP
   `ReadAsFunction`, and generated-shell syntax.

A helper-only fixture or parse PASS is a STOP.  No production/GHA/git.  Report
exact wrapper and generated pins plus a concise call-graph/diff account.
Mathematical status remains A4 `1/3 UNKNOWN_RESOURCE`, cross-checked through
row 26.  End with exactly one of:

`TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_PASS`

or

`TASK503_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_STOP`
