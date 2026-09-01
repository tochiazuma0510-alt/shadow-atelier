# Luna Task471 — rank99 checker-only driver v3 quote hotfix

## Scope

GHA run `33532584886` stopped before download/checker with exactly
`Error, task470 unsafe path`.  The committed v2 source introduced literal
single quotes in the shell command (`tr -d '[:space:]'` and
`cut -d ' ' -f1`) and then passed the entire command through `D470Quote`,
which correctly rejects any single quote.  Repair only this launch quoting.

Create a versioned full successor; do not overwrite committed v2.  Preserve
all v2 release/checker/checkpoint pins, isolated roots, one checker/no
producer, timeout/RSS, exact log equality, and receipt.  Build the shell
command with no literal single quote (for example use escaped double quotes
for `cut` and the v1 unquoted `tr -d [:space:]` form), so the final
`D471Quote(D471Download)` is defined.  Version owned output names to v3.

## Exact outputs

1. `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v3.g`
2. `sol/luna_reply_471_r07_rank99_checker_driver_v3_quote_hotfix.md`

Run only ASCII/final-newline, GAP external-preamble guard, and static command
construction/cardinality gates.  The static gate must evaluate the assembled
download command and prove it contains no single quote before outer quoting.
No checker replay, producer, GHA, workflow edit, or git.  End with
`TASK471_R07_RANK99_CHECKER_DRIVER_V3_PASS` or a typed STOP.
