# Sol task 526 -- rank99-v7 scalar-gate artifact audit

Role: Sol(max), independent mathematical/code-path auditor.  Do not implement,
edit production/checker/driver files, run production, dispatch GHA, mutate git,
or touch releases.  Write only:

`sol/sol_reply_526_audit_r07_rank99_scalar_gate_artifact_v1.md`

This is a short forensic audit whose result will prevent the failed rank99
formula semantics from contaminating the current rank111 lazy implementation.
It does not seek to revive the rank99 lane.

## 1. Authenticate the returned artifact

Audit run `33570220633`, job `100062348518`, exact head
`4d57c024df74b257e5b4e724b69e6c4d51ff667f`.  The downloaded artifact is in:

`%LOCALAPPDATA%\Temp\shadow-atelier-run33570220633-art9828236283`

GitHub artifact id/name/API size/service digest are respectively
`9828236283`, `gap-run-out`, `26278`, and
`sha256:d87bb87fa3b8749b46a72884adb869e159d52c278c025015406337954499ca49`.

Authenticate all six members and report exact bytes/SHA-256.  In particular,
the result should be `UNKNOWN / correction:scalar_gates`, with every
A0/COMMON/NONMEMBER/fake/Ihara claim false.  Authenticate the checkpoint's
canonical state seal and compare its accepted-source list/count, rank, batch
count and round to its rank99-v7 input.  Decide explicitly whether the run
made **zero durable prefix progress**.

## 2. Locate the exact failed conjunct

Read in full the committed rank99-v7/v6 producer/checker chain, especially
`search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v5.py` and its
`formula_bundle`, `compiled_formula_scalar`,
`retain_correction_candidate`, and caller.  Reconstruct the selected
candidate from the returned log/checkpoint if enough provenance exists.

The coordinate/row/fresh gates precede the terminal scalar gate.  Determine,
without inventing evidence, which of these predicates can be proved to have
failed:

1. `compiled_formula_scalar(formula,direct) in {1,2}`;
2. `pair(dual,row) == compiled_formula_scalar(formula,direct)`;
3. an earlier formula/model identity that makes either value ill-typed.

If the artifact lacks enough detail to distinguish (1) from (2), say so and
give the smallest bounded diagnostic that would distinguish them; do not run
a large replay merely for this audit.

## 3. Compare against the current rank111 authority

Compare rank99's custom formula/model construction with the current task445
state and formula authority:

- `search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py`,
  12215 / `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`;
- `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py`,
  3653 / `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1`;
- corrected theorem v433 and final audit Task524.

Identify precisely which rank99 helpers/data must **not** be copied into the
rank111 lazy K=0 implementation.  State which current-task445 direct pairing,
row reconstruction, normalized N1/N2/K, support-fibre and update APIs remain
the authority.  This is guidance, not a new theorem or implementation.

## 4. Verdict and v220 typing

Return one verdict:

- `AUDITED_ZERO_PROGRESS_WITH_CONTAINED_REGRESSION`, or
- `STOP_INSUFFICIENT_ARTIFACT_AUTHENTICATION`.

State the exact v220 consequence.  No rank99 failure is a nonexistence result,
no prefix is promoted without equality, and this task cannot change any A0,
A4, lift, fake, or Ihara numerator.

Use repository-external temporary files only.  Report exact commands and
bounded evidence.  Do not use git/GHA/network mutation.
