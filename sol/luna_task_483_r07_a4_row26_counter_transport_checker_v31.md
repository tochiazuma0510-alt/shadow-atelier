# Luna Task483 — A4 row-26 counter-transport checker v31

## Role

You are Luna.  Make the narrow positive-safe successor required by
`sol/sol_reply_481_audit_r07_a4_row26_checker_v30.md` and
`sol/proof_r07_a4_resumed_resource_counter_transport_erratum_v429.md`.
Do not edit or dispatch v30/v2 and do not regenerate the producer artifact.

Frozen rejected starting point:

```text
checker-v30 19871 660d71f34931d138a7d4fb9a4e3e2e17f7b10d3a73a32d59b90b85c9f2419529
driver-v2   14006 46fae084e45393d59e97f349b8ef839d49325843cabc24160cc49f8f5da7e27c
```

Retain v423, all frozen v28 semantic replay, all six immutable member pins,
release/run/job/head/artifact bindings, path ownership, one-checker/no-producer
execution, and the already-correct `15000 > 14400` and
`8500000*1024 > 8000000000` margins.

Replace only the false whole-domain v428 equality.  With registered semantic
domain `S` and

```text
D={terminal_canonicalization,terminal_serialized_bytes,terminal_final_write}
```

require exactly:

- `B.semantic == B.completed` on all `S`;
- `{k: T.completed[k] != B.semantic[k]} == D`;
- outside `D`, `T.completed` equals both base maps;
- on `D`, `T.completed` equals terminal semantic/canonical and the matching
  terminal transport/serialization fields;
- all maps have exact domains/types/bounds and `T.completed <= T.semantic`.

The exact base fixture values on `D` are `(0,0,0)` and exact terminal values
are `(7,9300,1)`.  Build the positive fixture by parsing/comparing the pinned
asset maps, not by silently normalizing the base.  Add the v429 mutations,
including missing/extra difference-domain members and a simultaneous
canonical+genuine-view second over-cap.  Transport increments must never
advance the row cursor.

Update the checker-only driver to fresh v31 paths and exact v31 pins.  Run only
bounded self-test, exact immutable-map fixture comparison and GAP parse.  No
production replay, GHA, git, producer rerun, or bytecode cache.

## Exact outputs

1. `crosscheck/check_d972_r07_word_independent_successor_kernel_v31.py`
2. `search/d972_r07_word_independent_successor_kernel_row26_checker_only_gha_driver_v3.g`
3. `sol/luna_reply_483_r07_a4_row26_counter_transport_checker_v31.md`

End with `TASK483_R07_A4_ROW26_COUNTER_TRANSPORT_V31_PASS` or a typed STOP.
