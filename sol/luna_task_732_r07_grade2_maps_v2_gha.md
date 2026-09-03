# Luna Task732 -- inert GHA wrapper for accepted grade-two map pair v2

Role declaration: Luna implementation/release support.  Implement only the
bounded workflow wrapper described here.  Do not change either Python program,
do not run the real build locally, do not arm or dispatch the workflow, and do
not perform git operations.  Write only the workflow and requested reply.

## 1. Frozen executable inputs

Use exactly:

```text
search/d972_r07_grade2_forward_adjoint_maps_v2.py
  bytes 44667
  SHA256 fdcb9a8ca9804179f350500c02203cdde550498b5cc5912ff1b0bde1d92e4d84
search/check_d972_r07_grade2_forward_adjoint_maps_v2.py
  bytes 48459
  SHA256 e388300c88de674d6e4550a7f20a40031488e724e40e73cdc89189b472ae61f0
sol/sol_reply_731_audit_r07_grade2_maps_v2.md
  bytes 10488
  SHA256 c63f7e1ee7289452ed4db8f22f3a1e1e0bf888fb7129fc09e51c7abf181bca9d
```

Task731 terminal authorization is
`PASS_GRADE2_MAPS_V2_SAFE_FOR_GHA` and
`SAFE_TO_DISPATCH_GHA=yes`.  Fail before execution if any path, byte count,
hash, or authorization marker differs.

## 2. Output and trigger

Create the versioned workflow only at

```text
.github/workflows/d972-r07-grade2-maps-v2.yml
```

It must have `workflow_dispatch` but remain inert under an explicit job guard
`if: ${{ false }}`.  Root alone will review, arm, commit, push, and dispatch.
Use pinned immutable action SHAs copied from an already accepted recent R07
workflow; do not edit any other workflow.

## 3. Single bounded real build/check job

Use an Ubuntu runner and one job, with an overall timeout no larger than 90
minutes.  Steps, in this order:

1. checkout;
2. strict preflight for the three frozen inputs and Python version;
3. redirect bytecode cache and all outputs to fresh paths under
   `$RUNNER_TEMP`, never the repository;
4. run both `--selftest` modes with short explicit timeouts and retain logs;
5. run the actual producer

   ```text
   python -B search/d972_r07_grade2_forward_adjoint_maps_v2.py \
     --emit "$RUNNER_TEMP/r07-grade2-maps-v2"
   ```

   with a 30-minute process timeout, line-buffered log capture, and exit-code
   preservation;
6. require the producer terminal marker
   `R07_GRADE2_FORWARD_ADJOINT_MAPS_V2_CANDIDATE`, exact 40-table roster,
   manifest and marker file before invoking the checker;
7. run the independent checker with a separate 30-minute timeout:

   ```text
   python -B search/check_d972_r07_grade2_forward_adjoint_maps_v2.py \
     --check "$RUNNER_TEMP/r07-grade2-maps-v2" \
     --output "$RUNNER_TEMP/r07-grade2-maps-v2-checker.json"
   ```

8. require checker exit zero, its unique PASS marker from the program, and a
   strict JSON assertion that all downstream claim flags remain false,
   `verified` is false, and the checker authenticated exactly 40 tables;
9. write a compact workflow receipt binding run id/attempt, commit SHA,
   executable hashes, manifest/checker hashes, table/entry counts, elapsed
   times and peak RSS;
10. upload the map directory, checker JSON, receipt, and bounded logs as one
    artifact named `d972-r07-grade2-maps-v2-${{ github.run_id }}-${{
    github.run_attempt }}` with 30-day retention.

Use `set -euo pipefail`; when piping through `tee`, preserve the real command
status.  Reject `Traceback`, `UNKNOWN_`, `HARD_STOP`, `ERROR`, a missing EOF,
or a missing/extra artifact file.  A failed or timed-out producer/checker is a
workflow failure, never a mathematical NONMEMBER result.

Do not add a checkpoint scheme: this finite map build is deterministic,
sparse and expected to fit one bounded job.  Do not add matrix construction,
replay of P1 artifacts, A0 search, connection transducer, CEGAR, or any
result-dependent input.

## 4. Static checks and reply

Parse the YAML locally without running the job.  Check that the guard is
literally inert, all required source pins/markers occur, all real output paths
are external to the repository, and the artifact step cannot run on a failed
checker.

Reply only to:

```text
sol/luna_reply_732_r07_grade2_maps_v2_gha.md
```

Report file byte/LF/final-LF/SHA receipts, the static checks, exact timeout and
artifact policy, and `WORKFLOW_INERT=true`.  Do not claim an actual map
artifact, grade-two decision, A0, COMMON, compatible cofinal lift, fake,
Ihara, or Lean verification.
