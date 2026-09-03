# Sol(max) Task622: final re-audit of Task601 packed-memory release

Role: independent final static auditor.  Do not edit implementation, run the
real route, production, GHA or git.  Write only
`sol/sol_reply_622_reaudit_r07_task601_packed_memory_release_v3.md`.

Read Task618, Task619, Task620 reply and Task621 in full.  Recheck the complete
Task620 adjudication, concentrating on whether Task621 made exactly its four
mandatory finite repairs and no mathematical/protocol weakening.

| exact release file | SHA-256 |
|---|---|
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | `cfd581f8a71176f9252555a94028a8482ede862ee3430098270109e52fa0d3ff` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | `09ee815345e9ad2cfd80799a5bf7daf4446cda0eb3d8bc79bd7b3d9c61fa86c8` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | `7f1b59790d2092fd93035742510ce7232834b4f7ea0a470507a408100d2e39cd` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | `a8511edcebff406af9a3b4fa0a0b2119d46f150741178379800cb1e88b7f16e2` |

Required final gates:

1. producer `append_row` preserves length and canonical-byte checks via a
   zero-copy vectorized scan;
2. pre-router lower recurrence replays exactly `declared_lower`, while the
   later standalone route still reroutes all 8,059 offers and consumes every
   transcript cursor;
3. the first candidate-basis `RowView` is reused in the final independent
   basis comparison, with row equality, SHA, leads, zero remainder and exact
   3,317 coefficients unchanged;
4. selftests actually reject an unfinished cursor at `finish()`, a leaf
   header with `states_exported=1`, and derived metadata containing `states`,
   through the production validation boundaries;
5. all prior Task620 PASS findings remain true: compact unique physical
   representation, no `derived.states`, complete ancestry-bound exact leaf
   receipt and independent leaf derivation, character-wise block release,
   `old-lower-zero` for every zero old offer including dependent grade rows,
   online terminal exhaustion, diagnostics, false claims and unchanged
   60-minute/8-GiB workflow contract;
6. workflow producer/checker/reply pins and
   `[fire-grade1-selected-slp-v2]` match the exact files above.

Only small serial syntax/selftests/YAML inspection are permitted.  Return
`PASS`, `PASS_AFTER_REPAIR` with an exact finite defect, or `FAIL`, with full
input hashes.  `PASS` authorizes root to commit/push this exact release and
perform the one Task618-authorized GHA rerun; it does not itself promote an
SLP, residual, A0, COMMON, fake, Ihara, cross-checked or verified claim.
