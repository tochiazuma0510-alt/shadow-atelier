# Luna task 429 — v10 raw-component origin fix

## Exact GHA finding

The bounded Linux traceback run `33318852115` / job `99277131484`, commit
`501b8787903c3ee1ac46bb38b8b6d6b59fa0a630`, produced artifact
`9734292344` and fixed the v9 failure at:

```text
owner_v9.py:230 target=q.transform(...)
owner_v9.py:100 {1:...,2:...,3:...,4:...,5:...}[comp]
KeyError: 6
```

The authenticated task179 typed raw row convention is **one-based**:
`row_key` requires `1 <= component <= 6`.  The quotient formulas in v9 are
written in the internal **zero-based** section convention: E3 uses `0..2`, E4
uses `0..5`.  Therefore the entire raw transform was shifted, not merely
missing an ad-hoc case for six.

Make one versioned v10 patch.  Preserve the v9 namespace repair and every v8
memory/resource/search/claim invariant.  Do not add a special `comp=6` case;
normalize the component origin once before the existing formulas.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v10.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v10.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v10.g`;
4. `sol/luna_reply_429_r07_a0_pb34_direct_quotient_owner_v10_component_origin_fix.md`.

Do not edit v9/trace files, workflows, proofs, v220, checkpoints or artifacts.
Do not commit, push, dispatch or run the production search locally.

## 1. One-based raw input to zero-based internal formula

Add one small helper used by `Quotient.transform`:

```python
def raw_component_zero(block, component):
    limit = 3 if block < 3 else 6
    need(1 <= int(component) <= limit, "raw_component_range")
    return int(component) - 1
```

After decoding an `R` key, preserve the original block/blob but replace the
local formula variable by this normalized value before either E3 or E4 branch.
The existing formula then has the intended exact interpretation:

- E3 raw `1,2,3` -> internal `0,1,2`;
- E4 raw `1,2,3,4,5,6` -> internal `0,1,2,3,4,5`;
- E4 internal zero keeps the six-term eliminated-generator formula;
- internal `1..5` map respectively to `b,p,c,q,r` coordinates
  `0,2,1,3,4` exactly as already written.

Do not alter signs, translations, `contract`, `normal_section`, actor logic or
the physical aggregation.  `normal_section` is already internal-zero-based and
must not receive an additional shift.

Extend the bounded fixture to assert all nine legal endpoint/middle mappings
and to reject E3 `0,4` and E4 `0,7`.  It must also assert specifically that raw
E4 component six normalizes to five rather than throwing.

## 2. Bounded unexpected-error telemetry

The full owner currently reduces unexpected exceptions to `str(e)`, which is
why two extra GHA runs were needed to locate `KeyError(6)`.  Without changing
any status or checker promotion rule, add fail-closed telemetry only in the
top-level unexpected-`UNKNOWN` exception object:

- exception type;
- `str(e)` as the existing reason;
- traceback limited to at most 24 frames and the last 12 KiB.

Do not attach traceback to normal `UNKNOWN`, `UNKNOWN_RESOURCE`,
`MEMORY_STATE_LIMIT` or candidate results.  Do not include state objects,
inputs, environment, secrets or checkpoint contents.  The checker may ignore
these extra diagnostic scalar/string fields; all public claim flags stay false.

## Gates

Run syntax compilation, v10 producer fixture and checker self-test only.  The
Windows real bootstrap remains inapplicable because of the frozen same-handle
gate.  Independently diff v9 to v10 and report that changes are restricted to:
version/schema/markers, the component-origin helper/use/fixture, and bounded
unexpected-error telemetry.

The driver must pin exact v10 producer/checker bytes/SHA, require external
`D972_R07_A0_PB34_V10_RUN:=true`, use fresh distinct v10 input/output paths,
9000 seconds, 4.8 GB, one Python owner and one checker, live logs and generic
GAP-run compatibility.  End with `V10_LOCAL_GO_FOR_PARENT_DISPATCH` or precise
`NO-GO`.
