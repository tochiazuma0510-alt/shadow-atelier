# Luna Reply Task808 — A0 v17 checker coordinate repair

## Result

The commissioned defect is repaired in the new checker v9 and workflow v17.
The old first failure, reproduced from the frozen checker log, was exactly:

```text
{"error": "'coordinate'", "status": "NOT_READY"}
```

`IndependentAllSeven.__init__` constructed all eleven actual records without a
`coordinate` field, while `occurrence_prefix_contract` correctly required that
field.  The new shared `build_actual_specs` helper binds the positional order
`(0,1,2,3,0,4,5,6,7,8,9)` during actual construction and requires the complete
coordinate tuple to equal `TEN` at the `checker actual coordinate order` gate.
`occurrence_prefix_contract` remains fail-closed and unchanged in its required
field/layout checks; `coordinates` and `occurrence_data` consume the bound
field rather than a separate inferred order.

The bounded regression constructs the synthetic eleven records through the same
`build_actual_specs` helper, then traverses `occurrence_prefix_contract`.
The honest tuple accepts.  Mutating record 10's coordinate to `1` is rejected
at the layout gate with `checker_prefix_layout`.

## Bounded checks

Checker compile and selftest passed without running the producer or a
production-size checker replay.  Selftest output included:

```text
fixture=PASS
mutation_count=56
actual_coordinate_mutation_rejections=1
positive_direct_canary=1
base_canary_direct_calls=2
base_canary_completion=2
```

The 56 mutations preserve all 55 prior mutations and add the one actual
coordinate mutation.  Direct bounded invocation of `fixture_rejects()` also
returned `actual_coordinate_mutation_rejections=1`.

## Versioned receipts

| file | bytes | LF | CR | BOM | SHA-256 |
|---|---:|---:|---:|---|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` (unchanged producer) | 70945 | 1272 | 0 | none | `1422bec44e1367c0ea22043cb7b5e844ba8e7df69e3da763bd08e372d5dc8046` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` | 113012 | 1969 | 0 | none | `7b2beb39dbdc65494f85fa4451ed69d99a22685d11f1d4fef6e671322d24098d` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v17.yml` | 13818 | 213 | 0 | none | `94ff396ed41ff5a6231d5b2fbe79648da921c02f809199542a7195080c7d5c75` |

The checker marker/schema are v9.  Workflow v17 keeps the single serial job,
exact parent pins, 8-GiB virtual-memory cap, bounded fixtures, 90-day
retention, and all claim flags false.  It runs producer v9, authenticates the
producer marker, uploads the complete payload as the explicitly
`unchecked-candidate` artifact, runs checker v9 separately against that exact
payload, and uploads payload plus verdict only after the checker marker.  The
producer and checker logs upload under `always()`.

No GHA dispatch or production computation was run.  Fresh rho2, A0, COMMON,
compatible lift, FAKE, and IHARA are not claimed; `verified=false`.

```text
TERMINAL=READY_FOR_HOSTILE_REAUDIT
```
