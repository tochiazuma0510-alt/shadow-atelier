# Luna Task757 -- P1 checker body-schema v5 + checker-only GHA v3

```text
RESULT=COMPLETE
REAL_GHA=NOT_RUN
P1_SEMANTICS_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

Created only the three designated files:

```text
crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v5.py
.github/workflows/d972-r07-p1-semantic-checker-only-v3.yml
sol/luna_reply_757_r07_p1_checker_body_schema_v5_and_gha.md
```

## Checker-v5 repair

Checker-v5 is a standalone versioned copy of checker-v4.  Its only production
semantic constant change is:

```python
STATE_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state"
```

The independent HEAD constant remains exactly:

```python
SEALED_HEAD_SCHEMA = "d972.r07.a0.first-rung-grade1.v3.state.head"
```

The bounded literal fixture accepts these two distinct exact strings and
rejects the body without `.state`, the HEAD without `.state.head`, and both
body/HEAD interchanges.  Arithmetic, parser/CLI, result schema and marker,
parent pins, 65,340 obligation set, and downstream claim boundary are
unchanged.

Static comparison against authority
`search/d972_r07_a0_first_rung_grade1_v4.py` passed: checker and authority
`fixed_dimensions()` are equal; the prepare validator and production body
builder have the same 21 top-level keys; the block validator and structural
block builder have the same 22 top-level keys.  No additional schema or
dimension difference was found.

## Workflow-v3

The workflow is push-only on `sol/r07-explicit-lift-20260825`, watches only its
own path, has no `workflow_dispatch`, and requires
`[fire-r07-p1-checker-only-v3]`.  It preserves the v2 honest producer-run
gate: run `33814881435/1`, head
`15778e83c52941040ef9d4289ab76d897ee30ebc`, status `completed`, conclusion
`failure`.  The exact eight producer jobs remain required, with prepare,
block-0--3 and join successful and only the historical `independent-check`
job failed:

```text
100844698807 preflight          completed success
100844805339 prepare            completed success
100846454006 block-0            completed success
100846453918 block-1            completed success
100846453996 block-2            completed success
100846453927 block-3            completed success
100847550237 join               completed success
100847634660 independent-check  completed failure
```

The producer artifact remains `9916479231`, named
`task729-p1-semantic-six-receipts-33814881435-1`, 8,412 bytes, digest
`sha256:91281261a272e6ff48104a579a86e9cb300fc1543eaad1321b609e6d83564245`.
The six receipts and all five Task554 parents are downloaded from their exact
runs/layouts after metadata authentication.  No producer phase is rerun.

Only checker-v5 performs the arithmetic replay.  The 345/360 minute caps,
12,000,000 KiB virtual-memory guard, single BLAS threads, canonical result
checks, timeout `UNKNOWN_RESOURCE` routing, existing checker marker,
success-only outputs and always-uploaded logs are preserved.  Checker output
schema/marker remain v1.  The workflow receipt schema and success/log artifact
names are versioned to v3 and bind producer run conclusion plus all producer
job identities/conclusions.

## Exact receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v5.py` | 133318 | 2740 | yes | `bc60882b3ee22aa449c51cc280491b3d66df384a814a7033e418454f66900f97` |
| `.github/workflows/d972-r07-p1-semantic-checker-only-v3.yml` | 21200 | 340 | yes | `6fccb22c865345ad5cb435bc5e80b140e75159cbfd5a39c466cf18dbaa5978c1` |

Pinned v497 proof is 1,779 bytes / 58 LF / final LF, SHA-256
`dde289b6ea044d3394c69b0e6bb134b56baca5a7c3b046b9b899736dcb3314e1`.
The workflow also authenticates the unchanged producer-v5, checker-v4
runtime dependency, v493 proof, Task749 reply, and Task750 audit pins.

## Bounded checks

```text
safe YAML parse + fire gate/static DAG/pin/run-conclusion checks: PASS
authority static schema/dimensions/body/block comparison: PASS
python -B -m py_compile crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v5.py: exit 0
python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v5.py --selftest: exit 0
fixture_accept=8
rejections=48
actual_five_artifact_check=DEFERRED_TO_GHA
status=PASS
verified=false
```

No real artifact download, producer replay, checker `--check`, GHA, Git,
push, dispatch, or actual build was performed.  The reply's own digest is
supplied post-seal rather than embedded.
