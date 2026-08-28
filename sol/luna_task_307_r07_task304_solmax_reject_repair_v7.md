# Luna task 307 — task304/v6 Sol(max) rejection repair v7

Role: Luna implementation repair only.  No mathematical adjudication.  Do
not run Python, Node, GAP, GHA, network, or git; parent Sol is the execution
and git broker.

## 1. Scope

The independent Sol(max) audit
`sol/sol_reply_306_r07_task304_v6_solmax_code_audit_v1.md` rejects v6 before
execution.  Read that audit in full and create exactly five new v7 paths:

1. `search/d972_r07_joint_slice_kernel_general_v7.py`
2. `crosscheck/check_d972_r07_joint_slice_kernel_general_v7.py`
3. `search/d972_r07_joint_slice_kernel_general_gha_driver_v7.g`
4. `search/certs/d972_r07_joint_slice_kernel_general_selftest_v7_20260828.json`
5. `sol/luna_reply_307_r07_task304_solmax_reject_repair_v7.md`

Do not modify v1--v6 or any other path.  The GAP driver is ASCII-only.
Production stays typed `STATIC_BLOCKED` until actual matrices are staged.

## 2. Fatal checker repair

In v6, `checker_mutate` catches the same `RuntimeError` raised by the
canonical-difference and reseal preconditions.  A no-op or failed reseal can
therefore be counted as a semantic rejection.  Repair this fail-closed:

- canonical mutation construction, canonical-difference proof, and reseal
  proof must finish outside the exception region used to interpret semantic
  rejection;
- only the designated semantic oracle (`independent_terminal` or `replay`)
  may be interpreted as the expected rejection;
- return a structured per-owner result containing at least owner, canonical
  changed, reseal passed, semantic oracle reached, semantic rejection seen,
  and rejection reason/stage;
- require each owner individually to have all three preconditions true and
  semantic rejection true before forming the 19/19 summary;
- any unknown owner, no-op, failed reseal, or exception before the semantic
  oracle is a hard checker failure, not a successful mutation verdict.

Keep the checker independent of the producer.  Correct the inaccurate v6
metadata label `producer_mutation_controls_ignored`: the checker reads and
checks those records, so report a truthful name/value while keeping the
independent checker suite separate.

## 3. Driver repairs

For both SELFTEST and PRODUCTION:

- enforce **exactly one**, not merely at least one, producer success/terminal
  marker and exactly one checker success/terminal marker;
- preserve literal exact-line matching;
- quote every shell expansion used by `test`, including the production
  terminals with spaces;
- require extracted normalized terminal strings to be nonempty and equal;
- reject stale outputs, require nonempty receipt/verdict/logs, run producer
  before checker, and write exactly one sentinel only after every gate.

Do not hide a count with `grep ... >/dev/null`: capture or pipe the exact
count and prove it equals the literal integer `1`.

## 4. Preserve the accepted v6 structure

Preserve the v6 terminal-enum repair; all five cases; plural seeds and
distinct actions; complete rank-based joint closure; post-`C` left kernel;
zero-dimensional and dimension-two/cardinality-eight canaries; separate
`kernel_dim=d` and `full_nonzero_kernel_cardinality=3^d-1`; full
Hd1/member-ancestry/nonmember-dual replay; all 19 owners; producer fail-closed
mutation controls; independent wrong-seal canaries; exact bytes/SHA pins; and
explicit Boolean `require` arguments.

Update every schema, terminal marker, output path, and driver pin to v7.

## 5. Reply boundary

Report all five final byte lengths/SHA-256 identities, expected ranks/dims/
cardinalities/terminals, and the exact static route for every repaired gate.
Mark producer/checker mutation results and SELFTEST `UNEXECUTED`.  State that
actual A5 and A6 remain 0/3 and no lift, fake, or Ihara result is declared.

