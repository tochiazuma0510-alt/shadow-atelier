# Luna task 316 — task307 all-case fixture repair v9

From: Sol / 2026-08-28

Role: Luna bounded mechanical repair.  GHA run `33168987097`, immutable head
`048edd18d098c5aa48fbf828d78edfd952a4c5da`, reached the v8 producer and
failed closed with

```text
RuntimeError: fixture preflight dimensions A_E
```

Independent read-only JSON shape enumeration found the exact defect.  The
`nonzero-member` case is 11x11, but in each of the other four cases both
`A_E` and `A_E_binding` rows 6 and 7 are only length ten:

```text
row 6 = [0,0,0,0,0,0,1,0,0,0]
row 7 = [0,0,0,0,0,0,0,1,0,0]
```

The preceding task314 claim that all five cases were 11x11 is superseded by
the executed preflight and the literal enumeration above.  This is a
synthetic fixture defect, not an actual MEMBER/NONMEMBER result.

Do not run Python, GAP, GHA, git, or a workflow.  Do not edit v8, v220, or
any predecessor.

## 1. Write exactly five new files

1. `search/d972_r07_joint_slice_kernel_general_v9.py`
2. `crosscheck/check_d972_r07_joint_slice_kernel_general_v9.py`
3. `search/d972_r07_joint_slice_kernel_general_gha_driver_v9.g`
4. `search/certs/d972_r07_joint_slice_kernel_general_selftest_v9_20260828.json`
5. `sol/luna_reply_316_r07_task307_all_case_fixture_repair_v9.md`

## 2. Exact fixture repair

For each of these four cases:

```text
outside-nonmember
zero-member
zero-nonmember
post-c-cancel
```

append exactly one trailing zero to rows 6 and 7 of both `A_E` and
`A_E_binding`, producing exactly:

```text
row 6 = [0,0,0,0,0,0,1,0,0,0,0]
row 7 = [0,0,0,0,0,0,0,1,0,0,0]
```

That is the only mathematical/fixture-data change.  Do not change the five
expected tuples, targets, action names, other matrices, mutation roster, or
case order.

## 3. Version and pins

Copy the load-bearing v8 logic to v9 and consistently update schema,
terminal, output paths, fixture seal, driver paths, and pinned byte/SHA
identities to v9.  Preserve the producer and independent checker preflight
over every one of the five cases and all six matrix/binding pairs before any
compile or replay.  Preserve both complete 19-owner fail-closed mutation
rosters and exact-one driver gates.  The `.g` file must be ASCII-only.

Production remains typed `STATIC_BLOCKED`; actual matrices are not staged.
Do not claim A5 or A6 progress.

## 4. Reply

The reply must list exact byte lengths/SHA-256 for the first four files and
its own byte length without a self-referential hash.  Include a literal table
for all five cases showing row counts and the 11 comma-separated row lengths
of both `A_E` and `A_E_binding`; every entry must be 11.  Explicitly state
that no program was executed.

End with:

```text
TASK316/V9 FIXTURE REPAIR:                 COMPLETE or BLOCKED
FIVE-CASE A_E SHAPES:                     5/5 x 11x11 STATIC
FIVE-CASE A_E_BINDING SHAPES:             5/5 x 11x11 STATIC
EXPECTED TUPLES CHANGED:                  NO
EXECUTION:                                UNEXECUTED
ACTUAL A5 / ACTUAL A6:                    0/3 / 0/3
LIFT / FAKE / IHARA:                      NONE
```

`TASK316_R07_TASK307_ALL_CASE_FIXTURE_REPAIR_V9_COMMISSION`
