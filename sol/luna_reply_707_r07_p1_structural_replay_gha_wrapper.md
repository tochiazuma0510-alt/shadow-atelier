# Task707 result — inert P1 structural replay wrapper

Status: `READY_FOR_SOL_P1_GHA_WRAPPER_AUDIT`; `verified=false`.

Only the new workflow and this reply were created.  No producer, existing
workflow, v220, git operation, dispatch, or replay was changed/run.

## Workflow

Created `.github/workflows/d972-r07-p1-structural-replay-v1.yml` with:

- exact producer SHA `38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73`;
- exact source run `33677346616`, attempt `1`, head
  `22c6dddb43d107c05e65f53ad898823ae8ebe276`;
- complete literal prepare/block artifact IDs, names, sizes, digests,
  expiry and source-run/head API checks;
- five distinct download roots with prepare roster count 15 and each block
  roster count 3 checked before execution;
- serial Python 3.13 compile/selftest and exactly one ordered all-five replay;
- separate result JSON, producer stderr, and `/usr/bin/time -v` output;
- assertions for the frozen terminal, ranks, offsets, 8,059 row/echelon
  counts, four local lead digests, global lead digests, and all false replay
  status flags;
- post-assertion result receipt binding event head, producer code receipt,
  five artifact identities, result receipt, terminal and counters;
- inert `false && (...)` guard, 45-minute job timeout, pinned actions, and
  compression level zero with 90-day retention.

The guard's live condition is manual dispatch or marker
`[fire-p1-structural-replay-v1]` after root removes only `false &&`.

## Mechanical static inspection

```text
YAML parse: PASS
job timeout: 45 minutes
matrix/parallel Python: absent
producer/checker edits: none
```

No runtime selftest or all-five replay was run locally, as required;
`REAL_REPLAY_DEFERRED_TO_GHA`.

## Exact receipt

| file | bytes | LF count | final LF | SHA-256 |
|---|---:|---:|---|---|
| `.github/workflows/d972-r07-p1-structural-replay-v1.yml` | 11950 | 206 | true | `f25893d8ebc8bdd2c3d972e044c5b42fd8fa3e2ba7a279a84c1c774edc90e775` |

## Delta/census

The workflow is a new versioned file.  Its bounded census is one inert job,
five exact API artifact authentications, five exact downloads, one serial
replay, one result assertion/receipt step, and two conditional uploads.  No
other file or computation path was altered.
