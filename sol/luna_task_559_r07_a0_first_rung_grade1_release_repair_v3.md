# Luna Task 559 — bounded release repair for the A0 first-grade engine v3

Role: Luna implementation only. Process every numbered section in order.
Implement exactly the four localized repairs accepted by Task558; do not
change the finite question, affine/Fourier mathematics, row universe, pivot
policy, ancestry semantics, or GHA workflow. Do not run a real prepare,
block, merge, the 56-second calibration, parallel Python, git, GHA, es7ops,
or another agent. Change only the designated outputs in section 7.

## 1. Frozen source and audit

Read in full:

1. `sol/luna_task_554_r07_a0_first_rung_grade1_character_blocks_v2.md`
2. `sol/luna_reply_554_r07_a0_first_rung_grade1_character_blocks_v2.md`
3. `sol/sol_task_558_audit_r07_a0_first_rung_grade1_engine_v2.md`
4. `sol/sol_reply_558_audit_r07_a0_first_rung_grade1_engine_v2.md`
5. `search/d972_r07_a0_first_rung_grade1_v2.py`
6. `search/check_d972_r07_a0_first_rung_grade1_v2.py`

Freeze the v2 producer at 114,922 bytes /
`df3aea9f49f5f76cd52f10923a38f75072eb2fc9cd4808578259ee48c4129ee4`
and checker at 55,010 bytes /
`a11824ff42602698219ccd130e1a03d1fd4dcdc76a3cbece4a9ed816e0ac050d`.
Task558 must end in `FIRST_GRADE_ENGINE_V2_PASS_AFTER_REPAIR`. Create a
versioned v3 snapshot; do not overwrite v2.

## 2. R1 — complete NONMEMBER roster gates

Before any NONMEMBER packet/transition algebra, fail closed unless every new
block satisfies all of:

```python
body["origin_count"] == len(prepare["defect_origins"])
len(body["origin_reductions"]) == body["origin_count"]
len(body["actor_transitions"]) == body["rank"]
all(len(row) == 4 for row in body["actor_transitions"])
len(body["dag_nodes"]) == body["rank"]
```

Also range/type-check every referenced pivot and F3 coefficient before it is
used. Add one seconds-scale reached helper/canary showing that truncating the
origin-reduction list is rejected. Do not reproduce the producer's pivot
order merely for telemetry.

## 3. R2 — strict, streaming state validation on consumption and resume

Add bounded validators for prepare, block, and merge states. A blob validator
must check filename shape, receipt keys, exact expected rows/width/encoding
and byte count, file size, and SHA-256 by streaming fixed-size chunks; it must
not read a large blob into a second full byte string merely to authenticate
it.

At the appropriate phase boundaries require:

- current `load_pinned_inputs()` receipt equals the complete stored receipt
  and its digest, and fixed dimensions match exactly;
- prepare phase/fixture semantics and exact residual, old-lower, old-lift,
  and packet receipt shapes;
- block parent, character, packet binding, origin/rank/attempt/cardinality,
  queue exhaustion, DAG digest, pivot roster and exact basis receipt;
- merge parent, exact ordered four `block_sha256` values, dimensions, roster
  digest/cardinality, lower/grade DAG ranks, terminal type, and exact physical
  basis receipt.

Invoke validation for completed phase resumes and before a downstream phase
consumes a state. Validate each large blob when it is actually relevant, and
do not introduce needless repeated full-file scans inside a row loop. In
particular, before finalizing a provisional merge require

```python
merge["block_sha256"] == [digest for _, digest in blocks]
```

The same immutable checkout is not a substitute for these state gates. This
is a localized validator, not a row-level database or a new checkpoint
framework.

## 4. R3 — idempotent certificate recovery

Close the crash window between installing the final merge HEAD and writing
the public certificate. Factor deterministic certificate construction and
an atomic idempotent writer/validator from the existing finalizer. On a fully
authenticated final `FIRST_RUNG_GRADE1_MEMBER` or
`FIRST_RUNG_GRADE1_NONMEMBER` resume:

- recreate the certificate if it is absent;
- if present, require its complete canonical content (including every
  duplicated state field) to equal the deterministic object from the sealed
  final state;
- never accept a fixture/provisional terminal as final;
- retain the exact producer hash, input/state chain, source ancestry,
  degree-two receipt when MEMBER, and false downstream flags.

Use a deterministic runtime value already sealed in the final merge body so
recovery does not change certificate bytes. Do not weaken the direct MEMBER
replay or NONMEMBER dual terminal.

## 5. R4 — existing caps and progress cover ingestion/replay

Inside the initial packet-origin ingestion loop, run the same
256-attempt-or-30-second progress report and `enforce_resource` gate used by
the actor queue, plus one check after the loop. Initialize prepare caps before
the raw/canonical lower replays, pass them into that replay, and enforce them
at its existing 256-term/30-second progress points and once at completion.
It is acceptable to cover seed evaluation similarly while touching the same
small area. Do not add a heavy SELFTEST, profiling framework, or speculative
optimization. The sorted-pivot metadata noted by Task558 is not a release
blocker and must not be redesigned here.

## 6. Version and bounded tests

The new files must use schema/certificate names ending in `v3`; the v3
checker pins the final v3 producer and must not import it or share a new
helper. Preserve the v443 accumulation canary, nonmonotone-lead canary,
projector ancestry canary, and existing three semantic mutations. Add only
the smallest fixture-state canaries needed to reach R1--R3.

Run serially with bytecode outside the repository:

```powershell
$task559Cache = Join-Path $env:TEMP 'task559_pycache'
$env:PYTHONPYCACHEPREFIX = $task559Cache
python -B -m py_compile search/d972_r07_a0_first_rung_grade1_v3.py search/check_d972_r07_a0_first_rung_grade1_v3.py
python -B -u search/d972_r07_a0_first_rung_grade1_v3.py --fixture
python -B -u search/check_d972_r07_a0_first_rung_grade1_v3.py --fixture
```

Do not run any real phase. Record exact commands, output, time, files,
byte counts, SHA-256 values, and why each of R1--R4 is reached or statically
load-bearing. No production certificate may be created.

## 7. Designated outputs and claim boundary

Create only:

1. `search/d972_r07_a0_first_rung_grade1_v3.py`
2. `search/check_d972_r07_a0_first_rung_grade1_v3.py`
3. `sol/luna_reply_559_r07_a0_first_rung_grade1_release_repair_v3.md`

Temporary files stay outside the repository. End with:

`FIRST-GRADE ENGINE v3: FOUR LOCAL RELEASE REPAIRS IMPLEMENTED; REAUDIT REQUIRED`

`FIRST-GRADE MEMBERSHIP: NOT COMPUTED`

`ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED`

`verified=false`
