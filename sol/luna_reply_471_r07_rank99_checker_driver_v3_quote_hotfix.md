# Task471 — rank99 checker-only driver v3 quote hotfix

Created the two authorized outputs only:

1. `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v3.g`
2. `sol/luna_reply_471_r07_rank99_checker_driver_v3_quote_hotfix.md`

The v2 driver baseline was preserved (size 6963, SHA-256
`aec1a65754e96757ffec6dc37e12f81e92a6fc5856ea4012f27a54f596646936`). The
v3 driver keeps the same release URL/run and artifact bindings, six-file
manifest, release/checkpoint/checker pins, isolated `ci/out` roots, one
checker invocation and no producer invocation, 6600-second timeout, and
4687500 KiB (`4800000000` byte) virtual-memory cap. Owned zip/archive/work,
checker-log, receipt, schema, pass marker, and final marker names are v3.

The launch command now uses escaped double quotes for `cut -d " " -f1` and
the unquoted `tr -d [:space:]` form. Thus the assembled `D471Download`
contains no literal single quote before the single outer
`D471Quote(D471Download)` call.

Final v3 driver pin:

```text
6920 bytes
05c438d045431948f4a487e0e264ed15e628cc7f22bc0cccf89fd9661b84431d
```

Bounded gates:

- PASS — ASCII-only and final-newline check.
- PASS — GAP external-preamble guard; a no-execution GAP harness assembled
  the complete download command and confirmed the quote-safe construction.
- PASS — static command/cardinality gate: exactly one outer quote call,
  exactly one checker command, no producer command, preserved timeout/RSS,
  six-file manifest, v3 owned paths, and no single quote in the assembled
  command.

Checker replay, producer execution, download/GHA/workflow execution, and git
operations were not run. No blockers for the bounded hotfix.

TASK471_R07_RANK99_CHECKER_DRIVER_V3_PASS
