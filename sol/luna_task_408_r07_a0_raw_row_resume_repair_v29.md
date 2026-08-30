# Luna task 408 — A0 raw-row resume repair v29

Role: Luna implementation/fixture only.  Do not dispatch GHA, commit, push,
or run production locally.

## Incident to repair

Generic GHA run `33282364093` (head `ed32ca089f22c7b5db04da67780aa6e6c1406c8d`)
reached the first streamed `new_records` row and stopped with

```text
ProtocolStop: direct P injection gate
```

The cause is now mathematically identified.  `Search.add_actual` stores
`record["sparse_row"]` as the **raw actual column**, while
`record["pivot_hex"]` and `record["pivot_node_id"]` describe that raw column
after reduction by all preceding pivot rows.  Frozen v26 `_stream_record`
incorrectly sends the raw column directly to `FormalReducer.inject`, whose
contract requires the already reduced normalized row.  Hence a nonempty
resume must fail on its first record whenever the raw leading key differs
from its stored pivot.

## Required minimal successor

Read frozen v13/v26 and batch-64 v28, then create only these versioned files:

1. `search/d972_r07_history_free_positive_fast_resume_batch64_v29.py`;
2. `crosscheck/check_d972_r07_history_free_positive_fast_resume_batch64_v29.py`;
3. `search/d972_r07_history_free_positive_fast_resume_batch64_gha_driver_v29.g`;
4. `search/d972_r07_history_free_positive_fast_resume_gha_driver_v30.g`
   (generic `gap-run.yml` prefix adapter reading the v29 batch driver);
5. reply `sol/luna_reply_408_r07_a0_raw_row_resume_repair_v29.md`.

Do not change any pre-existing file.

The producer must be a hash-pinned minimal successor of batch-64 v28.  Replace
only the streamed-record restore semantics:

- parse and authenticate the stored raw sparse row exactly as before;
- replay the same sequential Gaussian reduction/formal-DAG construction used
  by `FormalReducer.add_actual(raw_row, symbol)` (calling that owner is
  preferred if it preserves the frozen accounting);
- require the freshly derived normalized pivot and DAG node id to equal the
  stored `pivot_hex` and `pivot_node_id` before retaining the record;
- require no fresh DAG node allocation against the already restored final
  hash-consed DAG table; a mismatch is a typed STOP, never a fallback;
- preserve sequential rank/order, formal-entry accounting, batch-64 logic,
  checkpoint durability, and all existing terminal semantics.

Do not add a second full active-set scan, SELFTEST production detour, SAT mode,
or unrelated audit machinery.  The aim is to resume the existing 1.66 GB
checkpoint and enter actual batch search as soon as possible.

## Lightweight gates

Add a tiny in-memory regression fixture that demonstrates the incident and
the repair: a raw row reducible by a preceding pivot row has a stored pivot
different from its raw minimum; old direct injection rejects it, repaired
replay reconstructs exactly the stored normalized pivot/row/node.  Also mutate
the stored pivot and stored node independently and require rejection.

Run only compile/help/generated-owner/hash-pin/driver-parse fixtures and the
new tiny replay fixture.  Report exact bytes/SHA-256 and the commands/results.
Do not read or download the 1.66 GB production artifact locally.

