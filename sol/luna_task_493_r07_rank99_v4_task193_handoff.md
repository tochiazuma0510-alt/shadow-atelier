# Luna task 493 — rank-99 v4 COMMON to Task193 handoff

Role: Luna implementation only.  Do not change the mathematics, search order,
or any existing file.  This task prepares the positive downstream handoff
while the independently audited A0 production run is active.  It must not run
production or claim that COMMON exists.

## 1. Frozen mathematical contract

Use these paper interfaces without strengthening them:

- `sol/proof_r07_a0_batch_positive_to_task193_a2_carrier_v416.md`
  (6918 bytes, SHA-256
  `b3960f4b4900b823fdae614effec29661d24caca1e47b51d4249ac8477082e5a`);
- `sol/proof_r07_task451_carrier_task193_extensional_pin_migration_v417.md`
  (5711 bytes, SHA-256
  `b23b96ebc93dbfa511ee7251cfe91e6c8db35e0c8b8087e4e0b1fb3709939324`).

The only mathematical operation is the already proved extensional map

`checker-accepted COMMON -> terminal_replay.literal_word = a ->`
`(g760, a, freely_reduce(g760+a))`,

followed by the frozen Task193-v5 mathematical core.  Do not introduce a new
selector, boundary closure, replay universe, checkpoint system, worker pool,
or heuristic.

## 2. Exact new upstream

Authenticate the exact adopted v4 trio:

- producer `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py`,
  98576 bytes, SHA-256
  `5b8f3ae76abb64768decb14be50fbd6d75b5e84aeaad2b1a63fcb544933cf36f`;
- checker
  `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py`,
  66212 bytes, SHA-256
  `cd0acf346d4f133dfaa8e047db6593511a5423c6a166060a37fc313504e928e7`;
- driver
  `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v4.g`,
  9424 bytes, SHA-256
  `948f6254298eef51d524e834441c530ecb1a5a3a5cbefbdfe3dac9e7922d0ff8`.

The adopted immutable implementation commit is
`15f8dce96c5bdbeac8a3c3fa3662606bcfe315b0`.  The carrier must additionally
take the actual result, checkpoint, checker log, source head, run id, and
artifact id as explicit production arguments.  No default/fixture path may
stand in for those production inputs.

Positive input means all of the following, not merely `status=COMMON`:

1. canonical result/checkpoint JSON and physical file identities;
2. v4 schema, result seal, exact producer COMMON marker, claims boundary, and
   `status=terminal=COMMON_CANDIDATE`;
3. the result's durable-state identity equals the supplied checkpoint;
4. the exact v4 checker PASS marker occurs in the supplied checker log;
5. the independently pinned v4 checker accepts the complete result and its
   prefix/batch/segment replay;
6. `terminal_replay` is present and the checker-replayed positive object;
7. `literal_word` is freely reduced, exponent zero, and its direct physical
   replay agrees with the target/correction fields exactly as in the existing
   Task451 carrier.

RESOURCE, missing, malformed, stale-head, stale-pin, or checker-negative input
must remain `UNKNOWN_INPUT` with all A2/lift/fake/Ihara claims false.

## 3. Versioned outputs

Create only these new files plus the reply:

1. `search/d972_r07_rank99_v4_task193_carrier_v1.py`
2. `crosscheck/check_d972_r07_rank99_v4_task193_carrier_v1.py`
3. `search/d972_r07_rank99_v4_task193_carrier_gha_driver_v1.g`
4. `search/d972_r07_second_frattini_affine_prefix_compiler_v6.py`
5. `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v6.py`
6. `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v6.g`
7. `sol/luna_reply_493_r07_rank99_v4_task193_handoff.md`

Do not modify or generate cache files in the repository.  Temporary fixtures
belong outside the repository.

## 4. Carrier requirements

The producer must reconstruct the literal carrier from the actual v4 result;
it must not copy a claimed carrier supplied by that result.  Preserve the
existing carrier's exact checks for the 760-letter `g760`, right-product order,
eleven-occurrence/all-seven replay, joint-kernel condition, exponent pair,
physical-row digest, and selected ancestry.  Adapt the input authentication to
the v4 durable result/checkpoint/marker only.

The independent checker must authenticate the same immutable upstream files,
independently validate the v4 positive receipt, independently reconstruct the
carrier, compare every mathematical field, and emit a distinct checker
verdict.  It may call the pinned v4 checker as an accepted independent
component, but must not import the new carrier producer.

The GAP driver must be positive-only and fail closed.  Exactly one carrier
producer and, only after an accepted carrier receipt, exactly one carrier
checker are allowed.  RESOURCE/UNKNOWN is not COMPLETE.  Require explicit
paths and exact one-line owned sentinels.

## 5. Task193-v6 requirements

Use the existing v5 trio as the mathematical owner:

- producer 12207 bytes / SHA-256
  `fab51e296170ac34ebe48b49d79d3460017a51cd797d524e7b0d89481f23960f`;
- checker 7795 bytes / SHA-256
  `941eab0d9c60726436c866427de04b7c25b4ae1934fbf0a1d464f2010a7e2b9e`;
- driver 2269 bytes / SHA-256
  `d2cab901ae608d88bcff6dacdee6072c780b9157e1955cbaa740d227a8f2fe7a`.

V6 changes only the authenticated carrier dialect/pins and output provenance.
It must pass the normalized minimal input to the frozen v5 mathematical core;
do not reimplement the affine-prefix compiler.  The independent v6 checker
must rebuild the new carrier firewall and replay through the pinned v5 checker
mathematics.  Preserve all nonpositive claim boundaries.  No compact-A5 pin
migration belongs in this task.

## 6. Bounded gates

Run only bounded local tests:

- AST/compile for all four Python programs;
- carrier producer fixture and independent checker self-test;
- Task193-v6 producer fixture and independent checker self-test;
- pin checks and generated-shell syntax/GAP parse;
- mutations covering result/checkpoint identity, v4 seal/schema/terminal,
  producer marker, checker marker, source head/run/artifact identity,
  `terminal_replay`, literal word, exponent, physical replay/digest, ancestry,
  right-product order, carrier seal/verdict, and compiler carrier dialect.

Fixtures must say explicitly `actual_common=false` and cannot emit a production
PASS/COMPLETE marker.  Report exact bytes/SHA-256, commands, and final status.
End the reply with exactly one of:

`TASK493_R07_RANK99_V4_TASK193_HANDOFF_PASS`

or

`TASK493_R07_RANK99_V4_TASK193_HANDOFF_STOP`

