# Luna task 320 — task307 v10 action-shape, pin, and echelon repair

Role: Luna implementation only.  Do not run Python, Node, GAP, GHA,
network, or git.  Parent Sol is the sole execution and git broker.  Read all
numbered sections and reply only to the path in Section 1.

## 1. Exact new paths

Create exactly these five versioned paths and edit no existing v7--v9 or
other file:

1. `search/d972_r07_joint_slice_kernel_general_v10.py`
2. `crosscheck/check_d972_r07_joint_slice_kernel_general_v10.py`
3. `search/d972_r07_joint_slice_kernel_general_gha_driver_v10.g`
4. `search/certs/d972_r07_joint_slice_kernel_general_selftest_v10_20260828.json`
5. `sol/luna_reply_320_r07_task307_v10_action_shape_pin_echelon_repair.md`

Use v9 as the semantic base and read in full:

- `sol/luna_task_316_r07_task307_all_case_fixture_repair_v9.md`
- `sol/luna_reply_316_r07_task307_all_case_fixture_repair_v9.md`
- `sol/sol_task_318_r07_task316_v9_executed_shape_code_performance_audit.txt`
- `sol/sol_reply_318_r07_task316_v9_shape_code_performance_audit_v1.md`
- all four v9 code/fixture inputs.

The v9 audit is authoritative.  V10 remains synthetic only; production must
remain exactly `STATIC_BLOCKED:actual typed matrices are not staged`.

## 2. Exact fixture repair

Retain the already repaired 30 base/binding pairs and all five expected
tuples.  In the `m` action's `eta_matrix`, append a trailing scalar zero to
exactly these zero-based short rows:

```text
nonzero-member:      rows 6,7
outside-nonmember:   rows 6,7
zero-member:         rows 6,7
zero-nonmember:      rows 4,5,6,7
post-c-cancel:       rows 6,7
```

These are twelve row-array edits.  Afterward every action `theta_matrix`
must be 2x2, every `z_matrix` 2x2, and every `eta_matrix` 11x11.  Do not
change any nontrailing entry, target, expected tuple, case/action order,
mutation owner, or terminal.  Normalize each new text file to exactly one
final LF; do not copy v9's extra EOF LF bytes.

## 3. Complete literal preflight

Both producer and independent checker must preflight, before the first
compile/replay or mutation:

1. the same five-by-six base/binding literal equalities and dimensions as
   v9; and
2. every action matrix in every case, including exact row counts, every row
   length, scalar type, and F3 range.

The preflight must cover all six literal actions in their stored order and
must reject the exact old ragged v9 pattern.  It may not infer action shape
from the base matrices.  The checker must implement this independently and
must not import the producer.

## 4. Remove avoidable echelon rebuilding

Repair the performance findings in task318 without changing the accepted
span or lexicographic semantics.

- In the producer closure, maintain a live incremental F3 echelon/rank
  owner.  A stored closure row is already independent.  Do not recompute
  `rank(seen)` before every pop or recompute the same base rank once per
  action.  Test a candidate by one incremental reduction/insertion.
- In the checker use an independently written incremental basis/change-of-
  basis method.  Do not mirror/import the producer helper.  Do not recompute
  the accepted-basis rank for every action and do not perform the duplicate
  first-row containment check identified at checker lines 142--143.
- Retain full ancestry, independent left-kernel/nullspace replay, exact Hd1,
  MEMBER/dual checks, and all five expected tuples.  No `3^11` enumeration,
  retry, process pool, sleep, lock, or new unbounded loop is allowed.

The reply must give a concrete before/after count of avoidable base-echelon
rebuilds for the five baseline cases; the v10 target is zero.

## 5. Driver pins and execution boundary

The ASCII-only driver must pin the actual final byte length and full 64-hex
SHA-256 of producer, checker, and fixture.  In particular, do not reproduce
v9's 63-digit fixture SHA.  It must reject stale v7--v9 outputs, invoke the
v10 producer once followed by the v10 checker once, require exact-one full
line terminals and terminal equality, and create the sole sentinel only
after all gates.  Retain explicit SELFTEST and statically blocked PRODUCTION
modes.

## 6. Mutation reachability and reply

Keep the complete 19-owner mutation roster.  Ensure all five baseline cases,
the producer wrong-seal canary, all 19 producer mutations, the checker
wrong-seal canary, and all 19 checker semantic mutations become reachable on
the repaired literal fixture.  No no-op or mere reseal may count as a
semantic rejection.

Report exact identities, the twelve fixture edits, the full action-shape
table, the incremental-echolon design and counts, mutation reachability, and
`UNEXECUTED`.  Do not claim SELFTEST PASS, actual A5/A6 progress, lift, fake,
or Ihara.

