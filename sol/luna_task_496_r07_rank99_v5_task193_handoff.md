# Luna task 496 — rank-99 v5 COMMON to Task193 handoff

Role: Luna implementation only.  This supersedes the paused Task493 upstream
pin, not its mathematics.  Read Task493 completely, then apply exactly the
changes below.  Do not run production/GHA/git or alter existing adopted files.

## 1. Correct upstream

Replace every Task493 v4-discovery premise by the independently audited v5
trio:

- producer
  `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py`,
  104031 bytes, SHA-256
  `25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09`;
- checker
  `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py`,
  71589 bytes, SHA-256
  `970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d`;
- driver
  `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v5.g`,
  9425 bytes, SHA-256
  `bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d`;
- binding
  `0e0123e99309a768910e150d5bf4725295a0dc35eab7e15eac66538a3a37d56b`;
- adopted implementation commit
  `dd6d90b64e2bfba73d7f131f4da876235746f314`;
- production run/job currently active:
  `33553895281 / 100009888831` on that exact head.

Task495 independently proved GO and reproduced the old v4 KeyError versus v5
PASS.  V5 has passed the old runtime failure time.  This task still assumes no
actual COMMON result: production paths/run/artifact/head remain mandatory CLI
inputs and fixtures must state `actual_common=false`.

Use v5 schema, producer/checker markers, result/checkpoint fields, and the v5
checker PASS terminal everywhere.  A v4 result or marker must reject.

## 2. Outputs

Create only:

1. `search/d972_r07_rank99_v5_task193_carrier_v1.py`
2. `crosscheck/check_d972_r07_rank99_v5_task193_carrier_v1.py`
3. `search/d972_r07_rank99_v5_task193_carrier_gha_driver_v1.g`
4. `search/d972_r07_second_frattini_affine_prefix_compiler_v6.py`
5. `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v6.py`
6. `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v6.g`
7. `sol/luna_reply_496_r07_rank99_v5_task193_handoff.md`

The paused Task493 created two untracked byte-for-byte copies of the old
carrier-v1 owner:

- `search/d972_r07_rank99_v4_task193_carrier_v1.py`, 8553 bytes,
  SHA-256 `18c4932cbff5fbd5885ea03e80cd7f5c9f9c10bdbf4c7cc043985d3196042644`;
- `crosscheck/check_d972_r07_rank99_v4_task193_carrier_v1.py`, 8516 bytes,
  SHA-256 `82c5e7caa314e530782843bef81e66c431198fdc2d1c479886a14166f0fa1e73`.

They are aborted Task493 scratch outputs, contain no unique result, and must
not survive Task496.  Remove them only if their exact sizes/hashes still match;
otherwise STOP and report drift.  This exact cleanup is the only allowed
change outside the seven outputs above.

## 3. Contract retained from Task493

All Task493 sections 1 and 4--6 remain mandatory, with `v4` replaced by `v5`
only where it names the A0 discovery dialect.  In particular:

- extract only the independently checker-accepted
  `terminal_replay.literal_word`;
- independently reconstruct `(g760, correction_word, corrected_word)`, the
  complete eleven-occurrence/all-seven replay, exponent-zero and physical-row
  digest;
- use explicit result/checkpoint/checker-log/source-head/run/artifact inputs;
- carrier producer and checker may share frozen upstream owners but may not
  import one another;
- Task193-v6 changes only the carrier dialect/pins/provenance and delegates the
  affine-prefix mathematics to the exact Task193-v5 owner/checker trio pinned
  in Task493;
- no selector, search, checkpoint framework, compact-A5 migration, retry,
  worker pool, or production fallback is added;
- RESOURCE/UNKNOWN/stale v4 input keeps every A2/lift/fake/Ihara claim false.

Run the complete bounded Task493 battery plus explicit v4-input rejection and
v5 producer/checker pin checks.  Record exact bytes/hashes and commands.  End
the reply with exactly one of:

`TASK496_R07_RANK99_V5_TASK193_HANDOFF_PASS`

or

`TASK496_R07_RANK99_V5_TASK193_HANDOFF_STOP`

