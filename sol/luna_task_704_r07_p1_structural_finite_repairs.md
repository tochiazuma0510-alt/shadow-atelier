# Luna Task704: close the three finite Task702 P1 structural blockers

Role: Luna implementation.  Read `sol/sol_reply_702_audit_r07_task699_p1_structural_ingest.md` in full before editing.

## Scope

Modify only:

1. `search/d972_r07_grade2_specific_owner_prejoin_v1.py`;
2. new reply `sol/luna_reply_704_r07_p1_structural_finite_repairs.md`.

Do not touch workflows, artifacts, v220, git, Task640/A0, arithmetic algorithms, source pins, the four production roots, or any other file.  Do not start parallel Python.  This is a narrow finite repair, not generic hardening.

## Required code repairs

1. In the production `validate_block_semantics` DAG predicate, require `node['lead']` itself to be a plain integer before comparing it to the already typed `pivot_leads[pivot]`.  The mutation `node['lead']=False` with declared lead `0` must be rejected.
2. Replace ordinary equality for `downstream_claim_flags` by an exact-key and exact-value check: the key set must equal the keys of `FALSE_CLAIMS`, and every required value must be the boolean singleton `False` (`is False`).  Integer zero in any flag must be rejected.
3. Extend the live block-semantic fixture with exactly those two charged mutations and require rejection.
4. Add one bounded self-contained three-file block-root fixture that calls the same `validate_block_envelope` helper used by `ingest_all_five`.  It must accept its canonical fixture once and reject at least a wrong-parent HEAD mutation through that helper.  If fixture-specific expected body/basis hashes are needed, factor parameters/defaults so the production call remains pinned to the existing `PARENTS` and `BLOCK_BASIS_SHA`; do not weaken or bypass production pins.  Keep exact roster and canonical byte checks live.

## Checks and report

- Run `py_compile` and the bounded selftest.
- Run the all-five serial replay only if it is safe and single-process; never start parallel Python.  If memory/runtime makes it nontrivial, stop after selftest and report `REAL_REPLAY_DEFERRED_TO_GHA` rather than changing the design.
- Report exact candidate bytes, LF count, final-LF status and SHA-256.  If the real replay was run, bind its terminal/counters/runtime/RSS explicitly to that candidate receipt; otherwise make no production-success claim.
- Show a concise source diff/census proving only the commissioned semantic/envelope/fixture changes occurred.
- End with either `READY_FOR_SOL_P1_FINITE_REAUDIT` or a typed blocker.  `verified=false`.
