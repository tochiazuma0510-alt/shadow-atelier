# Luna task 385 - A4 canonical batch examined-cap repair v1

Commissioner: Sol / 2026-08-30

Reply to `sol/luna_reply_385_r07_a4_canonical_batch_examined_cap_v1.md`.

Role: minimal mechanical repair only.  Read task384, its four outputs, and
the independent audit finding supplied by the parent.  Edit only these four
new files:

```text
search/d972_r07_word_independent_successor_kernel_v15.py
crosscheck/check_d972_r07_word_independent_successor_kernel_v17.py
search/d972_r07_word_independent_successor_kernel_gha_driver_v24.g
sol/luna_reply_385_r07_a4_canonical_batch_examined_cap_v1.md
```

Do not edit v14/v16/v23, workflows, proofs, v220, ledgers, inputs or any
other file.  Do not run production, GHA, git, network, SELFTEST or mutation.
Static AST/load/pin/ASCII/GAP parse checks are allowed.

## Exact blocker and repair

V14/v16 bound `accepted <= 64`, but a dependent current-basis reduction does
not increment `accepted`; consequently one correlation may scan the complete
private nonzero roster.  Preserve the complete correlation and canonical
private roster, but examine at most the first 64 canonical candidates.

Use two separate counters with fail-closed assertions:

```text
0 < examined <= 64
0 < accepted <= examined
examined = min(64, length(private_candidates))
```

For every examined candidate, retain the current rule: reconstruct its exact
raw translated boundary column, reduce it against the current combined basis
after all earlier insertions, skip it if dependent, and otherwise insert it
with one ordinary chronological `BOUNDARY_RANK_RISE` record.  The first
canonical candidate must still be accepted (its nonzero fixed-dual pairing
proves independence from the pre-batch basis); fail closed if it is not.

Do not scan candidate 65 or later in that correlation.  After the bounded
batch, return to the existing query loop and recompute the target remainder,
dual and complete correlation.  Keep the public correlation/checkpoint ABI
unchanged and do not serialize the private roster or an `examined` roster.
The existing `accepted_batch_size` progress field may continue to report only
rank rises; exact examined-cap assertions remain private code gates.

Producer and independent checker must implement the same mathematical order
using their separate arithmetic.  Preserve v13 early checkpoints, v14/v16
current-combined semantics, all resource caps and terminal contracts.  V24
must pin v15/v17 and use fresh v24 output/checkpoint names; no v13/v14
checkpoint is a legal fresh input unless its code-owner pin exactly matches
the new executable, so leave dispatch to the parent.

The reply must give exact bytes/SHA, generated-source hashes, patch
cardinality, and direct evidence that no loop can decode/translate/reduce
more than 64 private candidates per complete correlation.  Do not claim an
actual speedup or A4 result before production.

`TASK385_A4_CANONICAL_BATCH_EXAMINED_CAP_COMMISSIONED`
