# Luna Task754 -- P1 checker-only run-conclusion v2

```text
RESULT=COMPLETE
REAL_CHECKER_ONLY_GHA=NOT_RUN
P1_PRODUCER_SIX_PHASES=ACTUAL_SUCCESS
P1_SEMANTICS_CROSS_CHECKED=NO
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```

Created only the designated files:

```text
.github/workflows/d972-r07-p1-semantic-checker-only-v2.yml
sol/luna_reply_754_r07_p1_checker_only_run_conclusion_v2.md
```

## Narrow v1 repair

The checker-only workflow is a v2 successor of v1.  It remains push-only on
`sol/r07-explicit-lift-20260825`, watches only its own path, has no
`workflow_dispatch`, and requires
`[fire-r07-p1-checker-only-v2]` on the job.  Action SHAs and NumPy `2.5.1`
are unchanged from v2 of the producer workflow.

The producer run is intentionally authenticated as the known historical
`completed/failure` run, rather than requiring whole-run success:

```text
producer run/attempt 33814881435/1
producer head        15778e83c52941040ef9d4289ab76d897ee30ebc
run status/conclusion completed/failure
artifact id          9916479231
artifact name        task729-p1-semantic-six-receipts-33814881435-1
archive bytes        8412
artifact digest      sha256:91281261a272e6ff48104a579a86e9cb300fc1543eaad1321b609e6d83564245
producer-v5 SHA      dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf
```

The jobs API is fetched for that exact run and must contain exactly these
eight completed jobs, with the listed conclusions:

| job id | name | conclusion |
|---:|---|---|
| 100844698807 | preflight | success |
| 100844805339 | prepare | success |
| 100846454006 | block-0 | success |
| 100846453918 | block-1 | success |
| 100846453996 | block-2 | success |
| 100846453927 | block-3 | success |
| 100847550237 | join | success |
| 100847634660 | independent-check | failure |

Thus prepare, all four blocks, and join are required successful producer
phases; only the known old checker job may be failed.  The workflow receipt
schema is versioned as
`d972.r07.p1.componentwise.checker-only.v2.workflow-receipt` and binds the
producer run status/conclusion plus every producer job id/name/status/conclusion.

## Preserved checker-only contract

The exact producer six-receipt artifact is metadata-authenticated and fetched
from its exact run.  Exactly the canonical prepare, block-0--3, and join files
are required.  The five Task554 parent artifacts retain source run
`33677346616/1`, head
`22c6dddb43d107c05e65f53ad898823ae8ebe276`, their v2 names/layouts, and exact
ids/sizes/digests.  Checker-v4 is compiled and self-tested before large input
downloads, then is the only arithmetic command run with the v2 five roots and
six receipt arguments.

The 345-minute process timeout, 360-minute job timeout,
`ulimit -v 12000000`, one-thread BLAS settings, time/RSS log,
`UNKNOWN_RESOURCE` timeout routing, audited marker
`R07_GRADE2_P1_COMPONENTWISE_INDEPENDENT_CHECKER_V1_PASS`, canonical result
checks, all-false claims, success-only result upload, and always-uploaded logs
are unchanged.  A nonzero checker cannot upload a mathematical success
artifact.

## Exact workflow receipt

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `.github/workflows/d972-r07-p1-semantic-checker-only-v2.yml` | 22464 | 421 | yes | `db3f528135a4dfdfbdd6bfd98f028d3f39406ed0b36bd0f4deac350f6041ad98` |

Fixed source pins authenticated by the workflow:

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py` | 132129 | 2719 | `cc9a27e8ab447ecd6e4fbebbd1240195e442d6c5eb14241a5f9d7c669154ee19` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` | 41619 | 382 | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |
| `sol/proof_r07_p1_checker_state_head_schema_repair_v493.md` | 2414 | 80 | `2feb9f83135cc4af234dfc7110128b2636fb12bd82e920ce3bdab19b02fddf5b` |
| `sol/luna_reply_749_r07_p1_checker_state_head_v4.md` | 3340 | 71 | `2d93e8e576633d5b8d5bfc9434c266266054c89ff0a808dec782493bb8b0a316` |
| `sol/sol_reply_750_audit_r07_p1_checker_state_head_v4.md` | 10046 | 216 | `a4a738ac814a5470ee471416380c00a51f1cfef555e32d63c273404fb34ef517` |

## Bounded checks

```text
safe YAML parse + fire gate/static DAG/pin/run-conclusion checks: PASS
python -B -m py_compile crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py: exit 0
python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v4.py --selftest: exit 0
fixture_accept=7
rejections=42
actual_five_artifact_check=DEFERRED_TO_GHA
status=PASS
verified=false
```

No real artifact download, producer replay, checker `--check`, GHA, Git,
push, dispatch, or actual build was performed.  The reply's own digest is
supplied post-seal rather than embedded.
