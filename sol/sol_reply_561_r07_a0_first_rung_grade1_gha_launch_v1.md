# Sol Reply 561 — A0 first-grade v3 GHA launch receipt

## Outcome

The independently release-audited v3 first-grade engine is now running on
GitHub Actions.  The active production run is
[`33677346616`](https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/33677346616)
at exact source commit
`22c6dddb43d107c05e65f53ad898823ae8ebe276`.  Its real prepare phase completed
successfully and all four character closures are running simultaneously.

## Release identity

The release commit for the audited programs was
`09d47c0bf3ecb5e14cbebf561cd25825122c1ddd`.  It contains:

- producer v3: 138,202 bytes /
  `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff`;
- checker v3: 69,193 bytes /
  `67f56ee92aea7e17ce88303657ca519ee9539269eef44e6e5550da63d6a4a012`;
- Sol(max) Task560 audit: 10,225 bytes /
  `5ba42f2aadcf216a75df298d05657ce3fff27bbfd5c40226e6fcf2e7cee4ed64`,
  verdict `FIRST_GRADE_ENGINE_V3_PASS` and `GHA_RELEASE: ALLOWED`.

The first guarded-push preflight, run `33677024094`, stopped before any real
phase.  Its producer fixture reported
`ModuleNotFoundError: d972_r07_a0_c2fourier_joint_floor_v1`.  The programs were
present in the feature-branch commit, but all 18 already-hash-pinned runtime
inputs were still local-only.  No mathematical computation or memory-heavy
work was lost.

Commit `22c6dddb43d107c05e65f53ad898823ae8ebe276` adds exactly that frozen
18-file dependency closure and extends the guarded workflow path roster.  It
does not change either v3 program, any frozen hash, the finite row universe,
or the Task560 verdict.  A repository-tree check found all 18 paths at that
commit before push.

## Reached production state

Run `33677346616` passed checkout, Python installation, all three release hash
gates, producer fixture, and checker fixture on GHA.  Prepare job
`100405252316` then completed in 5m49s including setup and artifact upload.
The actual producer receipt is:

```json
{"defect_origins":8232,"elapsed_seconds":326.194140029,"old_ranks":[505,503,503,503],"phase":"prepare","residual_support":16254,"resumed":false,"state_sha256":"1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"}
```

The largest RSS printed by prepare was 453,427,200 bytes.  Thus neither the
7 GiB engine gate nor the 8 GiB virtual-memory guard was approached.  The
immutable prepare artifact is service artifact `9865061266` (204,360,988
bytes); its log artifact is `9865062076` (25,626 bytes), both retained for 90
days.

The four live closure jobs are:

```text
block 0  job 100407172564
block 1  job 100407172576
block 2  job 100407172504
block 3  job 100407172523
```

Each consumes the same authenticated prepare state and runs in its own hosted
runner.  Merge and independent terminal checking remain downstream and have
not run yet.

## Claim boundary

This receipt records a launch and one completed prepare phase.  It is not a
first-grade membership terminal.  A0 remains 0/1 actual and the first rung
remains 0/6 grades decided until the independent checker completes.

FIRST-GRADE PRODUCTION: ACTIVE (RUN 33677346616)

FIRST-GRADE MEMBERSHIP: NOT COMPUTED

ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED

verified=false
