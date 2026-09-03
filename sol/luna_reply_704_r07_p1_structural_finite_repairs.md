# Task704 result — finite P1 structural repairs

Status: `READY_FOR_SOL_P1_FINITE_REAUDIT`; `verified=false`.

Only the commissioned producer and this reply were changed.  No workflow,
artifact, v220, Task640/A0, source pin, or git operation was touched.  No
parallel Python and no all-five production replay were run;
`REAL_REPLAY_DEFERRED_TO_GHA`.

## Repairs

In `validate_block_semantics`:

1. `node['lead']` is now required to be a plain integer before comparison
   with the typed `pivot_leads[pivot]`.  Thus `False` versus declared `0` is
   rejected.
2. `downstream_claim_flags` now requires exactly the `FALSE_CLAIMS` key set,
   with every value satisfying `is False`; integer zero is rejected.

The live block fixture now includes both charged mutations.  Its semantic
rejection count is 7 (the previous five plus `node_lead_bool` and
`false_claim_ints`).

The same production `validate_block_envelope` helper now accepts optional
fixture-only digest/parent parameters; production calls omit them and remain
bound to `PARENTS`.  A self-contained temporary three-file block root
(canonical HEAD, canonical body, basis member) is accepted through that
helper, and a wrong-parent HEAD is rejected through the same helper.

## Checks

```text
python -B -m py_compile search/d972_r07_grade2_specific_owner_prejoin_v1.py
PASS: bounded producer selftest
block_fixture: envelope_accept=1, envelope_wrong_parent_rejections=1
block_fixture: semantic_rejections=7
REAL_REPLAY_DEFERRED_TO_GHA
```

The selftest also retained the existing exact roster, canonical-byte,
typed-blob, expression/DAG, and row checks.

## Candidate receipt

| file | bytes | LF count | final LF | SHA-256 |
|---|---:|---:|---|---|
| `search/d972_r07_grade2_specific_owner_prejoin_v1.py` | 47995 | 545 | true | `38fcbe3757d1b14fd19f4f557f763c1f5f6a2e8da47e0e061707cf28c5064d73` |

## Source census

The candidate contains only these bounded changes: one exact false-claim
gate, one plain-integer DAG-lead gate, two fixture mutation cases, one
parameterized envelope helper preserving the pinned production defaults, and
one temporary three-file envelope fixture with its wrong-parent mutation.
No arithmetic, ingestion order, four production roots, basis scanning, or
result-dependent join logic was changed.
