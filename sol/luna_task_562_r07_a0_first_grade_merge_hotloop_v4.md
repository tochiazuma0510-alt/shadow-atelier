# Luna Task 562 — minimal first-grade merge hot-loop repair v4

Role: implementation only.  Process every numbered section in order.  This is
a bounded recovery preparation for the already running Task559/v3 production
merge.  Do not change the mathematics, row universe, insertion order, pivot
policy, state data, or claim boundary.  Do not use git, GHA, another agent, or
heavy/parallel local computation.  Change only the designated outputs in
section 7.

## 1. Frozen inputs and purpose

Read in full:

1. `search/d972_r07_a0_first_rung_grade1_v3.py`
2. `search/check_d972_r07_a0_first_rung_grade1_v3.py`
3. `sol/luna_reply_559_r07_a0_first_rung_grade1_release_repair_v3.md`
4. `sol/sol_reply_560_audit_r07_a0_first_rung_grade1_engine_v3.md`
5. `.github/workflows/d972-r07-a0-first-rung-grade1-v3.yml`

Pin their exact byte counts and SHA-256 values in the reply.  V3 production
run `33677346616` has sealed one prepare state and four exhausted character
states.  Its merge hot loop is taking much longer than the four closures.
V4 must be able to consume those exact v3 state bodies and blobs; it must not
rebuild prepare or any block.

## 2. Preserve the complete semantic contract

Create a versioned v4 producer from v3.  Keep the existing v3 `SCHEMA` and
`STATE_SCHEMA` values deliberately, as an explicit input/output compatibility
contract for the frozen v3 prepare and block artifacts.  Change only the
program docstring/version wording and public certificate pathname to
`search/certs/d972_r07_a0_first_rung_grade1_v4.json` where necessary.

The following must remain identical for the same inputs: row traversal order,
lead choice, pivot IDs, normalized packed pivot bytes, reduction expressions,
physical roster, DAG ancestry, MEMBER/NONMEMBER predicate, dual construction,
literal expansion, direct replay, and next-degree residual.  Runtime and state
digests may differ.  No RREF, batch elimination, reordered pivots, new split,
new self-test framework, or mathematical shortcut is permitted.

## 3. Remove repeated suffix scans

Repair only `PackedEchelon.reduce_packed`.  Replace the repeated allocation of
`work[cursor:] != 0` plus `any/argmax` after every elimination by a monotone
packed-byte cursor.  Scan zero bytes once in Python; for a nonzero byte obtain
the first nonzero trit with the existing `_PACKED_FIRST` table.  If its lead is
not registered, stop exactly as v3 does.  If registered, record the identical
`[pivot, coefficient]` and apply the existing `_PACKED_AXPY` lookup.

AXPY may be restricted to the current packed byte and its suffix, but only if
the implementation fail-closes on the invariant that every stored pivot has
no nonzero trit before its declared lead and has coefficient one at that lead.
After eliminating a lead, revisit the same byte so later trits in that byte are
not skipped.  Reduction order must remain increasing by actual lead, including
the existing nonmonotone insertion canary.

## 4. Remove the lower double reduction

Factor the acceptance/normalization half of `PackedEchelon.insert` into one
small private helper which consumes an already reduced packed remainder and
its reduction expression.  Ordinary `insert` must call `reduce_packed` once
and then that helper.  In the lower-first merge path, after the explicit
`lower_owner.reduce_packed(...)`, pass that exact remainder/expression to the
helper rather than calling `insert(physical_lower)` and repeating the same
elimination.  Preserve the returned dictionary byte-for-byte in shape and
meaning, including `leading_coefficient`, `scale`, and insertion-ordered pivot
ID.

## 5. Compatibility and bounded equivalence fixtures

Create a v4 checker by versioning the v3 checker, pinning the final v4 producer
hash, and reading the v4 certificate pathname.  Do not weaken or redesign the
independent checker.  It continues to accept the deliberately v3-compatible
state schema.

Run only serial seconds-scale checks outside the repository bytecode cache:

1. `py_compile` of the two v4 files;
2. producer `--fixture`;
3. checker `--fixture`;
4. one new bounded reducer equivalence fixture inside the producer fixture.

The reducer equivalence fixture must compare v4 against a tiny local reference
implementation of the old v3 reduction algorithm on deterministic packed
rows covering: zero row, missing pivot, several pivots in one packed byte,
nonmonotone insertion leads `[5,3]`, coefficient two, and dependent insertion.
Compare remainder bytes, ordered reductions, acceptance record, leads, and
stored row bytes.  Do not run real prepare/block/merge or a mutation campaign.

## 6. Recovery interface and claims

Retain the exact existing CLI.  `--merge <state-dir>` is the only intended
production use of v4: it consumes the already sealed v3 prepare and four block
artifacts.  A future parent-owned workflow will download those artifacts,
authenticate them, run v4 merge, and then run the independent v4 checker.

No implementation or fixture result promotes grade one, order 54,432, full
Q0, A0, COMMON, a compatible lift, fake, Ihara, or Lean verification.

## 7. Designated outputs

Create only:

1. `search/d972_r07_a0_first_rung_grade1_v4.py`
2. `search/check_d972_r07_a0_first_rung_grade1_v4.py`
3. `search/certs/d972_r07_a0_first_rung_grade1_v4.json` only if a real merge
   is run (it must remain absent in this task)
4. `sol/luna_reply_562_r07_a0_first_grade_merge_hotloop_v4.md`

Report exact commands, timings, byte counts, SHA-256 values, equivalence
coverage, and the absence of a real certificate.  End with:

`FIRST-GRADE MERGE V4: MINIMAL HOT-LOOP REPAIR IMPLEMENTED; INDEPENDENT AUDIT REQUIRED`

`V3 PREPARE/BLOCK COMPATIBILITY: RETAINED`

`FIRST-GRADE MEMBERSHIP: NOT COMPUTED BY THIS TASK`

`ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED`

`verified=false`
