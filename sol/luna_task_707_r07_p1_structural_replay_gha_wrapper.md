# Luna Task707: inert GHA wrapper for the Task704 P1 structural replay

Role: Luna implementation.  Modify only a new workflow `.github/workflows/d972-r07-p1-structural-replay-v1.yml` and new reply `sol/luna_reply_707_r07_p1_structural_replay_gha_wrapper.md`.  Do not edit the producer, v220, any other workflow/file, git, or dispatch a run.

## Frozen computation

- Producer: `search/d972_r07_grade2_specific_owner_prejoin_v1.py`, exact candidate SHA-256 `38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73`.
- Source artifact run/attempt/head: `33677346616/1`, `22c6dddb43d107c05e65f53ad898823ae8ebe276`.
- Exact service tuples are frozen in the producer `SERVICE`: prepare artifact `9865061266` and block artifacts `9865238399,9865242284,9865193269,9865239848`, with their full names, sizes and artifact digests.  Copy the complete literal values; no ellipses or broad patterns.

## Wrapper requirements

1. Versioned workflow name `d972-r07-p1-structural-replay-v1`; push trigger only on the work branch and relevant producer/workflow paths, plus `workflow_dispatch`.  Keep the job inert with `false && (...)` until root release.  The live condition after root removes only `false &&` must accept manual dispatch or commit marker `[fire-p1-structural-replay-v1]`.
2. Pin the existing action SHAs used by accepted workflows, checkout exact `${{ github.sha }}`, Python 3.13, serial/thread-count-one environment, `contents: read` and `actions: read`, and a reasonable 30--45 minute job timeout.  No matrix or parallel Python.
3. Authenticate the producer SHA and every artifact's exact ID/name/size/digest/non-expiry/source-run identity through the GitHub API before download.  Download the prepare and four blocks by exact name into five distinct roots; assert their expected HEAD files and exact top-level file counts before running.
4. Run `py_compile`, bounded `--selftest`, then exactly one serial all-five command with ordered roots:
   `--prepare-dir PREP --block-dirs B0 B1 B2 B3`.
   Capture stdout JSON and `/usr/bin/time -v` stderr separately.  Assert the exact terminal `TASK554_ALL_FIVE_P1_STRUCTURALLY_INGESTED`, 8,059 rows/distinct/coefficient-one, ranks/offsets and the frozen four/global lead digests from Task699/Task702.  Assert `resident_matrix=false`, `semantic_equations_replayed=false`, `precision2=false`, `verified=false`.
5. Produce a small receipt binding event head, producer SHA/bytes/LF/final-LF, exact five artifact identities, result SHA/bytes and terminal/counters.  Upload result+receipt only after all assertions pass; upload logs always.  Use 90-day retention and compression level zero.  No independent checker, semantic replay, Task640 join or grade-two claim.

## Report

Run only mechanical YAML/static inspection locally.  Report workflow/reply bytes, LF, final LF and SHA-256, plus a normalized delta/census.  End `READY_FOR_SOL_P1_GHA_WRAPPER_AUDIT`; `verified=false`.
