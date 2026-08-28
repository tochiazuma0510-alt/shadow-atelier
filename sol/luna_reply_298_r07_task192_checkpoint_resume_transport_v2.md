# Luna reply 298 - task192 checkpoint resume transport v2

Only the commissioned v2 driver and this reply were created. Task295's v1
driver/reply, the sealed ZIP and manifest, the producer, checker, serial
driver, workflow, and mathematical engine were not changed. No Python, GAP,
GHA, network, or git command was executed.

## Repaired defect

Task295 v1 supplied `--seconds 19800`, but the authenticated source
checkpoint has `monitor.limits.wall_seconds == 10800.0`. The pinned v3
producer first converts the authenticated checkpoint through its rank-zero
resume firewall and records the old monitor as
`resume_monitor_history.snapshot`. Its preflight then requires literal
equality between that snapshot's limits and a new `Monitor(args).limits`.
Consequently v1 was deterministically headed to
`UNKNOWN_INPUT:resume:monitor_limits` before search.

The v2 command supplies `--seconds 10800` and preserves every other
commissioned cap. The pinned producer has no `--global-roster` option; its
fixed producer-owned value is `357128352`, and the extraction guard binds
that value in the authenticated monitor limits.

The fresh process receives a **new 10800-second wall-clock budget**. The
source `elapsed_seconds == 10802.377323564` is retained as history only and
is not charged against the new process clock. In contrast, the authenticated
work counters carry forward (with `checkpoint_bytes` treated by the pinned
producer as a serialized-size gauge). Thus matching the old
`wall_seconds=10800.0` does not immediately spend the new wall budget.

## Static identity

```text
driver  19682  169da7aa149d68907abb435f380b9ec2994c2bc285c6a17f13431614a388f5ad
reply   self-referential bytes/SHA intentionally omitted
```

The driver's path/schema/version identity is:

```text
search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g
d972-r07-normalized-exact-cached-colgen/resume-transport/v2
task298-v2
```

It is ASCII-only and intentionally has no embedded raw self-SHA.

Task295 v1 remains byte-for-byte unchanged:

```text
driver  14718  cd7b881c1e89a412eff7a4dbbb08642960f7e9faa72313fdeb6366295a377217
reply    6616  22a83c6fdfdab447d3a230529e2a8e8a2ebfe943b68ef7db1fc4f3a2601d0d2f
```

## Immutable input pins

All five v1 pins were rechecked read-only and remain:

```text
checkpoint ZIP
  5001811  f3ac82a04907983d987cc2a42d06fe3b612ec2040555f40be81200969358f566
manifest
  1328     6911dfe822662a17ae95c896f97573e553d15325631f1606bd0bf7f550e88302
producer
  193704   f27b4971351832b8730fb8cce4e782e893a958dfb850203cc735c7bc3aa31f37
checker
  154009   dfc8cbbd96a1da45f15e01607ed343b66a78a7201f4a80952fba33aaeb361e10
task192 serial driver v3
  11548    2f7ff7b459e46d014268907ff5ba5f03c035836e8f8df79a2c5f4cdc3b75351d
```

The ZIP guard still requires exactly one non-directory, one-part member:

```text
d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json
raw bytes  86368039
raw sha256 c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab
```

## Authenticated JSON monitor/progress gate

Only after ZIP, manifest, member metadata, decompressed byte count, and raw
SHA-256 authentication does the extraction helper parse the raw checkpoint
JSON. It requires `monitor.limits` literally equal to:

```text
boundary_pairs   8000000
candidate_words  2000000
checkpoint_bytes 4000000000
fibre_scans      80000000
global_roster    357128352
oracle_rounds    1
retained_columns 250000
rss_bytes        5700000000
wall_seconds     10800.0
```

It also binds the complete monitor key set, integer/float types, phase,
single-process flag, historical elapsed time and RSS, and the exact carried
counters:

```text
boundary_pairs   3145728
candidate_words  0
checkpoint_bytes 86367576
fibre_scans      0
global_roster    0
oracle_rounds    0
retained_columns 2896
```

The raw progress object is required exactly: boundary correlation is
incomplete with `pair_attempts=3145088`, `restart_pair_cursor=0`, and dual
digest
`0960259714fa94ddd89e2ac4f582f040942ab7bd258185c0448c133e50b00f0c`;
the correction cursor, live fibres, kernel prefix, global cursors, and
weighted rows are all at their authenticated zero/empty values with the same
dual.

The helper additionally requires:

- manifest phase/counter values equal the monitor values;
- `rank == len(columns) == retained_columns == 2896`;
- the exact v3 safe chunk, including complete empty chunk, canonical ordering,
  and replayable empty repeated suffix;
- chunk/correction cursor equality and the exact authenticated
  `3145728 - 3145088 = 640` counter/progress relation;
- current, boundary, correction, and v3 epoch dual digests all equal;
- historical elapsed time exceeds the authenticated old wall limit;
- no pre-existing `resume_monitor_history` or `resume_rebuild` field.

Only after those gates does it exclusively create the fixed v2 resume input
and replay its bytes/SHA after writing. Any existing destination is a stale
STOP.

## Exact resume command and fresh paths

The exact producer command assembled by the driver is:

```text
python3 -u -B search/d972_r07_normalized_exact_common_word_cached_v3.py --mode PRODUCTION --output ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.json --resume ci/resume/task192_run33149728601_checkpoint_v2.json --seconds 10800 --boundary-pairs 8000000 --fibre-scans 80000000 --candidate-words 2000000 --retained-columns 250000 --checkpoint-bytes 4000000000 --rss-bytes 5700000000 --oracle-rounds 1
```

It is followed unconditionally and serially by:

```text
python3 -u -B crosscheck/check_d972_r07_normalized_exact_common_word_cached_v3.py ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.json
```

Every transport/output path is fresh and stale-rejected:

```text
ci/resume/task192_run33149728601_checkpoint_v2.json
ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.json
ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.json.checkpoint.json
ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.producer.log
ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.checker.log
ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.sh
ci/out/d972_r07_normalized_exact_common_word_cached_resume_v2.ok
```

## Terminal, sidecar, and sentinel gates

The extraction marker, producer terminal prefix, checker pass prefix, and
typed sidecar marker each must occur exactly once. The accepted terminal
grammar remains the pinned task192 v3 grammar. The producer and independent
checker terminals must be byte-for-byte equal.

The shell-level sidecar replay remains fail-closed:

- COMMON must have neither a checkpoint reference nor a sidecar;
- UNKNOWN_RESOURCE must reference the fresh sidecar by exact basename, bytes,
  and SHA-256;
- UNKNOWN_INPUT may omit a sidecar, but any reference must authenticate and
  an unreferenced sidecar is rejected.

Only after nonempty receipt/log gates does the driver write the one exact
sentinel:

```text
R07_TASK192_CHECKPOINT_RESUME_TRANSPORT_V2_SENTINEL
```

## Boundary and status

This is transport repair only. It neither promotes the old checkpoint nor
asserts a positive or negative mathematical conclusion. COMMON can become an
A0 positive-terminal candidate only after the existing independent checker
accepts the exact same terminal.

```text
TRANSPORT DRIVER V2:    IMPLEMENTED STATICALLY
TASK295 V1 MUTATION:    NONE
ZIP/MANIFEST MUTATION:  NONE
WORKFLOW CHANGE:        NONE
EXECUTION:              UNEXECUTED
FAKE / IHARA:           FALSE / NOT DECLARED
```

`TASK298_R07_TASK192_CHECKPOINT_RESUME_TRANSPORT_V2_UNEXECUTED`

## Parent Sol dispatch

After an independent static comparison with the authenticated checkpoint and
the pinned v3 resume firewall, parent Sol committed and pushed the unchanged
generic-workflow input, then dispatched it through the JSON API:

```text
run id       33163964747
commit sha   f723f58fee9c587fded73114151abec193bc9d5e
script       search/d972_r07_normalized_exact_common_word_cached_resume_gha_driver_v2.g
preamble     empty
out_dir      ci/out
timeout      360 minutes
status       IN_PROGRESS (2026-08-28 19:36 JST)
```

This records transport execution only.  A0 remains zero unless the run emits
COMMON and the pinned helper-nonshared checker accepts the identical terminal.
