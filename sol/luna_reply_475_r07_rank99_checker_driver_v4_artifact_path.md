# Task475 — rank99 checker-only driver v4 artifact-path repair

Created exactly the two authorized outputs:

1. `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v4.g`
2. this reply file.

The v4 driver preserves the Task471 release, six-member manifest, checker
source pin, timeout/RSS bound, quote-safe shell construction, exact-one log
equality, collision-safe roots, one-checker/no-producer contract, and receipt
bindings. It changes only the artifact transport and versioned owned paths.

After zip/member authentication it copies both exact members to:

```text
<work>/ci/out/d972_r07_a0_dual_anchored_active_batch_v1.json
<work>/ci/out/d972_r07_a0_dual_anchored_active_batch_v1_output.checkpoint
```

Both copies receive byte/SHA checks. The post-`cd <work>` checks prove the
checker-visible paths are `ci/out/<artifact>` and `ci/out/<checkpoint>`, and
the sole checker invocation now receives `ci/out/d972_r07_a0_dual_anchored_active_batch_v1.json`.
Thus the artifact's embedded durable checkpoint path resolves within the same
copied `ci/out` cone; the erroneous `../<archive>/` transport is absent.

Bounded static gates passed: ASCII-only, one checker command, no producer
command, preserved `set -euo pipefail`, external timeout, RSS bound, exact
terminal equality, six-member pins, one outer quote call, and distinct v4
archive/work roots. No semantic replay, producer, download/GHA/workflow
execution, git operation, or bytecode-cache creation was performed.

Driver pin: 8,217 bytes, SHA-256
`cacd34a634a647ca0c7ea4a2a08cb548c49d72a2830d535d270b670012e2aaa7`.

The frozen runtime terminal remains the previously bound rank99 checker PASS;
no new mathematical terminal is claimed by this path-only repair.

TASK475_R07_RANK99_CHECKER_DRIVER_V4_PASS
