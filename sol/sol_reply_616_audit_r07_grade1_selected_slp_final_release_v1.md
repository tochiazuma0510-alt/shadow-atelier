# Task 616 — final release re-audit of Task601 selected SLP

## Verdict

`PASS`

All four Task614 repair groups are closed in the commissioned quartet, and
the repaired files retain the frozen routing, physical replay, independent
router, resource envelope and candidate-only claim boundary.  I found no
concrete load-bearing defect and require no further repair.

This is a static release verdict only.  I did not run production, GHA, git,
or a full local 8,059-row route.  It is not an execution receipt, cross-check
claim, or Lean verification.

## Exact inputs

I read both numbered inputs and the repaired quartet in full.

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_616_audit_r07_grade1_selected_slp_final_release_v1.md` | 2,437 | 43 | `8a19d2abb6c8a4caebaaa9290cdd68b9964a0fb26acf469fe73a9deca2344ee7` |
| `sol/sol_reply_614_audit_r07_grade1_selected_slp_v1.md` | 13,159 | 230 | `4ab26ef61db6577d98c9d8ed37c1d7da2e4b6d90b59dc9836f7a26120c981720` |
| `sol/luna_task_615_r07_grade1_selected_slp_final_release_repair_v1.md` | 2,985 | 65 | `5e0bf6923bb81e9b1ea722800c02122b60afc30fa27a608da268539774c201f4` |
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | 25,722 | 234 | `4cc5d6ccb1bfdcb441b801a4826af04bbbdc9dc7f21d6f7c860d05929e64bfe9` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | 54,060 | 589 | `8355fda531b9de41b37df811af932352f07546d6d0ec445764fedaced2595595` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | 5,497 | 111 | `3ddd2f53fb10d698713e2a44a27cd894f4a02120727bb58db65beef9ac4a6fbd` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | 3,737 | 63 | `f360beb5a7c70608b48683183d01af3e262e0ce4b687c0cdb5ccb48c9cb31609` |

All four implementation hashes exactly match Task616.  The frozen v3 is
still SHA-256
`bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff`,
and the unchanged standalone router is still SHA-256
`a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3`.

## Task614 repair closure

1. **Least canonical graph: closed.**  The producer enters the canonical
   source closure only through `selected_refs`; the former augmentation from
   quotient-derived `states` is gone.  Old nodes follow only an actor parent
   and their ordered old reductions and create no expression record.  Only a
   reached block defect inserts an expression: exactly its referenced
   `seed_reductions[seed-1]` or single
   `actor_transitions[pivot][ACTORS.index(letter)]`.  Transition children are
   the acted old root first and the expression children afterward.  The
   block-owner `origin_reductions[oi]` insertion receipt is absent from the
   canonical record.  The checker independently reconstructs this same least
   closure from selected refs alone and requires exact key sets, records,
   expressions and deterministic ordering.

2. **Roots receipt and claim boundary: closed.**  Production calls
   `compare_roots_receipt_pointer` to require
   `manifest["roots"] == files["roots"]["file"]`, authenticates that receipt,
   parses exactly `loaded["roots"]`, and requires its canonical bytes.  Those
   same bytes supply all three semantic-root checks, while the verdict records
   that same receipt SHA.  `require_false_claim_flags` is called independently
   on both manifest and roots and requires the presence and exact identity of
   all eight values:

   ```text
   direct_occurrence_replay=false
   next_degree2_residual=null
   cross_checked=verified=A0=COMMON=FAKE=IHARA=false
   ```

   Missing fields, truthy substitutions, integer lookalikes and a non-null
   residual therefore fail closed.

3. **Authenticate before execution: closed.**  The producer hashes frozen v3
   before its module loader executes it.  The checker likewise hashes v3
   before its selected-source `exec_module`, and hashes the standalone router
   before its separate import.  The workflow preflight now actually compares
   v3 against `V3_PRODUCER_SHA256` before invoking either Task601 script, in
   addition to checking the current producer, checker and reply pins.

4. **Fixtures and receipts: closed.**  The checker selftest invokes the same
   production `require_false_claim_flags`, root-pointer/root-binding,
   `compare_source_structure`, and `compare_authoritative_transcript` gates.
   Its 8 claim mutations, 3 root/receipt mutations, 13 source mutations and 11
   transcript mutations cover the commissioned cases.  In particular, the
   source cases include an internally canonical child deletion, acted-old
   omission, same-key duplication, and deletion and mutation of both seed and
   transition expressions; the root cases include receipt-pointer aliasing.
   The Luna reply reports the exact current producer/checker sizes and hashes,
   and the workflow pins the current producer, checker, reply and frozen-v3
   hashes.

## Unchanged release path

The repair did not touch the producer's physical route.  Before any payload
is emitted it still authenticates the decision and sealed parents, routes the
same 8,059 logical offers, requires lower/grade ranks 1,661/5,044 and basis
SHA-256
`b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d`,
and requires the exact 3,317 MEMBER coefficients and zero authenticated
remainder.  The already-packed lower stored row, equally scaled lower grade
companion, ordered old lower link and separate grade scale remain unchanged.

The checker still independently reroutes every offer with the standalone
source and compares every node record, ordered edge stream, origin/stored/
companion/lower-zero row and final basis before accepting MEMBER.  Its sealed
selected-old/block physical-origin replay and four-entry block-owner cache are
unchanged.  There is still one producer basis materialization, one independent
checker basis materialization, no per-origin block reload, no dense
degree-two computation and no flat-word export.

The workflow retains the exact source run `33677346616/1`, candidate run
`33707397894/1`, candidate commit
`93f746ad1b649796e1bc28e00ff34993498929ee`, Python 3.13, NumPy 2.5.1,
40/45/60-minute and 7/8-GiB limits, success marker, success-only payload and
verdict upload, and always-uploaded logs.  `py_compile`, both serial selftests
and a YAML parse passed in this audit; no production data were consumed.

```text
TASK616_FINAL_STATIC_RELEASE_AUDIT:          PASS
TASK614_LEAST_SOURCE_CLOSURE_REPAIR:         CLOSED
TASK614_ROOT_RECEIPT_AND_FLAGS_REPAIR:       CLOSED
TASK614_PREEXECUTION_V3_PIN_REPAIR:          CLOSED
TASK614_FIXTURE_AND_RECEIPT_REPAIR:          CLOSED
FROZEN_ROUTE / PHYSICAL REPLAY / ROUTER:     UNCHANGED
PRODUCTION / GHA / CROSS-CHECK:              NOT RUN BY THIS AUDIT
verified:                                    false
```
