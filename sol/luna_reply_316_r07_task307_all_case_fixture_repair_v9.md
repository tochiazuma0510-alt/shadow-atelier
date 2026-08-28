# Luna reply 316 - task307 all-case fixture repair v9

Created exactly the five authorized v9 paths. No existing v8, v220, predecessor,
workflow, or git path was modified. No Python, Node, GAP, GHA, workflow, or
other project program was executed; SELFTEST and production are UNEXECUTED.

## Final identities

```text
producer  13001  1e38453980eac5dc4b3b8edcb63235a7de60684393491a5bc01cdd356f4d103a
checker   24995  5cadaeb180e2058466a9a97bb54c5b98393e2e4096035f4e64b69a65d0da8121
driver     4860  be0f1d75e7ea3d4814cf234dd00b59e4e1def0745e1d1094170e0b3c18ba9859
fixture   10356  6a866e980422afc405c4d6b574c06cee8ca8ee6792b536a006e4d104724c7cd
reply      3137  [self-referential SHA intentionally omitted]
```

The v9 GAP driver pins the producer, checker, and fixture to the exact
identities above. Schema, fixture seal, terminal markers, output paths, and
driver paths are v9; the .g file is ASCII-only. The reply byte length is
reported below after its final serialization.

## Exact fixture repair

Exactly 16 trailing zeros were appended: rows 6 and 7 of both `A_E` and
`A_E_binding` in each of `outside-nonmember`, `zero-member`,
`zero-nonmember`, and `post-c-cancel`. Each repaired row is:

```text
row 6 = [0,0,0,0,0,0,1,0,0,0,0]
row 7 = [0,0,0,0,0,0,0,1,0,0,0]
```

No expected tuple, target, action name, other matrix, mutation roster, or case
order was changed.

## Five-case literal shape table

| case | A_E row count | A_E row lengths (11 comma-separated) | A_E_binding row count | A_E_binding row lengths (11 comma-separated) |
|---|---:|---|---:|---|
| nonzero-member | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 |
| outside-nonmember | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 |
| zero-member | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 |
| zero-nonmember | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 |
| post-c-cancel | 11 | 11,11,11,11,11,11,11,11,11,11,11 | 11 | 11,11,11,11,11,11,11,11,11,11,11 |

Both producer and independent checker retain fail-closed preflight over all five
cases and all six matrix/binding pairs before compile or replay. Both retain
the complete 19-owner mutation roster and exact-one driver gates. Production
remains typed `STATIC_BLOCKED`; actual matrices are not staged. No A5 or A6
progress is claimed.

Expected tuples remain:
```text
nonzero-member       2 2 8 2 MEMBER
outside-nonmember    1 1 2 1 NONMEMBER
zero-member          1 1 2 0 MEMBER
zero-nonmember       1 0 0 0 NONMEMBER
post-c-cancel        2 1 2 1 MEMBER
```

Reply byte length is given without a self-referential hash. No program was
executed.

TASK316/V9 FIXTURE REPAIR:                 COMPLETE
FIVE-CASE A_E SHAPES:                     5/5 x 11x11 STATIC
FIVE-CASE A_E_BINDING SHAPES:             5/5 x 11x11 STATIC
EXPECTED TUPLES CHANGED:                  NO
EXECUTION:                                UNEXECUTED
ACTUAL A5 / ACTUAL A6:                    0/3 / 0/3
LIFT / FAKE / IHARA:                      NONE

`TASK316_R07_TASK307_ALL_CASE_FIXTURE_REPAIR_V9_COMMISSION`
