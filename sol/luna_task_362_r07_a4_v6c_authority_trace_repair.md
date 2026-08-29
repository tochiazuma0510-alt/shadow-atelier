# Luna task 362 — R07 A4/v6c authority-trace complete finite repair

Role: Luna, bounded mechanical repair only.  Read every numbered section
first to last before editing.  Do not run Python, Node, GAP, GHA, a workflow,
git, network, or any candidate command.  Read-only PowerShell inspection and
hashing are allowed.  Use `apply_patch` for repository edits.

This task repairs the statically rejected v6b rows-1--7 authority trace.  It
does not execute A4, extend coverage to rows 8--48, or change an A4
mathematical numerator.

## 1. Binding inputs and verdict

Read in full:

1. `sol/luna_task_358_r07_a4_v6b_authority_trace_finite_repair.md`;
2. `sol/luna_reply_358_r07_a4_v6b_authority_trace_finite_repair.md`;
3. `sol/sol_reply_360_r07_task358_a4_v6b_code_performance_audit_v1.md`;
4. the frozen v2 producer, checker, and authority fixture audited there;
5. the actual task198 receipt, acceptance manifest, producer/checker/driver,
   attestations and verdict directly referenced by the audit; and
6. the prior task356/task357 contracts only where task360 cites a retained
   physical-owner or row semantic.

The binding v2 identities are:

```text
producer  66,200 bytes  ca8755b6ad4bf9de001783d76d4de0e4d5d8680795540264ee843680a8deb3e9
checker   62,039 bytes  8ec2fb33d17ac19cab2f13a141e91f05423b87e9edb82fbd8f5543512c0d3252
fixture    8,457 bytes  8fd4de7b89eb07e3adb272782f3052c9b9b3bb90bf7a27212933ae40f892a91d
audit     19,738 bytes  f8f172d753493ea08463f635fc05ac04ac6326b11a5835dea167b6b0277c6d32
```

Task360's verdict is `REJECT / UNEXECUTED`.  Treat every defect in Sections
2--7 as load-bearing; do not repair only the first peak stop.

## 2. Sole permitted outputs and versioning

Create only:

```text
search/d972_r07_a4_actual_owner_trace_producer_v3.py
crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v3.py
search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v3_20260829.json
sol/luna_reply_362_r07_a4_v6c_authority_trace_repair.md
```

Do not edit or delete any v1/v2 owner, task360 audit, v220, workflow, or
actual task198 input.  Do not create a driver or runtime output.  The v3
fixture remains acyclic: it pins immutable external authorities and the exact
row/cap contract, but not either new program or the reply.

## 3. Semantic receipt/manifest reseal DAG

Implement the actual task198 codecs exactly.

1. A receipt decoder/sealer removes exactly top-level
   `self_digest_sha256`; a foreign `manifest_self_digest_sha256` is rejected,
   never silently popped.
2. A manifest decoder/sealer removes exactly
   `manifest_self_digest_sha256`; a foreign top-level receipt seal is
   rejected.
3. Receipt resealing returns or mutates one explicit tuple containing the
   newly sealed DOM, canonical raw bytes, raw SHA-256, byte length, and new
   receipt self seal.  No caller may continue with a pre-seal shallow DOM.
4. `copy_manifest` binds all three nested receipt values — bytes, raw SHA,
   and the **new** receipt self seal — from that tuple.
5. Rows 1/5/6/7 replay the complete five-node DAG:

```text
changed receipt body -> new receipt self seal -> new receipt raw/SHA
new receipt identity -> changed manifest nested receipt binding
changed manifest body -> new manifest self seal/raw/SHA
```

6. Row 2 reseals only the changed manifest; rows 3/4 intentionally do not
   reseal a physically mutated owner.  Every final comparison uses the new
   semantic owner, not baseline data.

The producer and checker implement this independently.  A common new helper
or cross-import is forbidden.

## 4. Exact task198 type and ABI validation

Close every validator gap listed by task360 Section 4.

- `layer_counts` uses exact recursive type/value equality: bool, float, and
  integer subclasses do not substitute for exact integers.
- Every presentation row enforces the exact key set, exact string fields,
  positive exact integer `target_state/state/generator/record/letter`, and
  exact integer `orientation` in `{-1,1}`.
- Layer-local ordinal, contiguous global coverage, all chunk seals, chunk
  coverage, `sealed=true`, `prefix_complete=true`, resume cursor, source
  encoding, legacy digest and every stored presentation digest are checked
  against the actual baseline contract.
- Validate the evaluator's full exact ABI, including `module`,
  `relator_rows_sha256`, entry points, encoding, semantics, all nested canary
  word/value shapes and their exact values.  Prefer an independently
  reconstructed expected object or a field-by-field strict validator plus
  exact equality; key-set-only acceptance is forbidden.
- Retain the complete 11-field occurrence ledger, coordinate-owner and
  normal-generation checks already repaired by v2.

Avoid a second full 6,441-row structural traversal.  Fuse exact comparison
to the authenticated baseline with the typed row walk, or use another
explicit single-pass design.  Do not replace semantic validation by a stored
digest alone.

## 5. Physical owners, baseline lifetime, and row 4

Keep no-follow physical handles to every baseline authority owner for the
whole invocation, rather than closing them after initial read.  Before and
after each case:

1. compare device, inode, file type/mode, size, link count and `mtime_ns`
   with the frozen baseline identity;
2. read/hash through the retained fd (with exact rewind/length checks) and
   require the frozen bytes/SHA;
3. compare the registered pathname through a no-follow parent walk to the
   retained fd identity; and
4. fail before recording `baseline_revalidated=true` on any mismatch.

Close every retained fd in an exception-safe invocation-level `finally`.

Row 4 uses an invocation-unique outside owner inside its own temporary parent
created outside the workspace, asserts the exact path absent before creation
and after disposal, and derives `owner_disposed` from that actual outside
owner.  It must never reuse or remove a pre-existing shared sibling path.
The path mutation still reaches the registered containment gate before any
basename or resolution shortcut.

Evidence owner/kind/logical-path values must flow from the actual mutation
constructor/observation object.  A separate name-indexed label table may be
comparison data but cannot author the accepted evidence.

## 6. Meter ownership and exact resource account

Release every per-case owner in the same case `finally`, including
`case:<name>:receipt`, manifest, clone, changed-manifest clone, canonical
transients, raw receipt/manifest and physical/cache tokens.  No token from
row 1 may remain live on entry to row 2.

Reserve before every allocation or copy.  The repair must statically support
the clean supported-POSIX seven-row route under the frozen caps.  Use
task360's corrected size deltas:

```text
opened_bytes intended = 186,443,551
temporary_bytes       = 155,099,839
largest intended peak = 728,045,006 < 750,000,000
```

Recompute all formulas from the final source rather than copying these
numbers blindly.  Include the row-2 `+1`, row-6 `+8`, every 10,000-byte
changed-manifest clone, all canonical transients, retained baseline handles,
and optional-output costs.  Distinguish logical metered opens from actual OS
directory/file opens; do not call the former a full physical-operation
count.  Remove the duplicated 31-MB-class row traversal identified in the
audit.

## 7. Bound-parent, failure-atomic optional publication

All optional output operations use one retained no-follow parent-directory
fd and dir-fd-relative calls.  No pathname-reopened or symlink-substitutable
parent is authoritative.

Prepare, serialize, write, flush/fsync, validate, and clean every object that
can be completed before publication.  Publish the final name with an
exclusive no-replace operation.  If any link cleanup, parent fsync, final
identity, or post-publication check fails, synchronously roll back the final
name through the same retained parent fd, fsync the rollback, assert the
target absent, and only then propagate failure.  A failed call may not leave
a published target.

On success require:

```text
final target present with exact bytes/SHA and regular-file identity
temporary link/name absent
same retained parent fd and pathname identity
parent fsynced after final namespace state
all staging owners disposed
```

Every fd closes under `finally`, including fsync exceptions.  Stale target,
unsupported no-follow/dir-fd primitives, or inability to prove rollback is
typed non-PASS.  Document the precise POSIX support boundary; do not claim
Windows support from a lexical path check.

## 8. Rows 1--7 and independent checker

Preserve the exact seven row order and expected first-rejection terminals.
One meter spans the full invocation.  The producer and checker each execute
all seven mutation constructors against actual task198-shaped owners; the
checker does not trust producer evidence, expected-reason control flow, or a
shared helper.

Each evidence record retains the physical owner identity, actual mutation
observation, complete semantic reseal DAG where applicable, first gate,
resource before/after state, baseline revalidation transcript and disposal
proof.  `MutationAccepted` remains outside narrow expected catches.

Rows 8--48 remain explicitly uncovered.  The fixture and reply must retain:

```text
covered_rows = [1,2,3,4,5,6,7]
remaining_rows = [8,...,48]
candidate_only = true
full_a4_selftest = false
actual_a4_numerator = false
```

## 9. Reply and freeze

The reply processes Sections 1--9 in order and gives exact bytes/SHA-256 of
all three machine owners, fixture self seal, line-numbered repair traces,
the semantic DAG, exact final resource formulas, supported-platform boundary,
and every remaining limitation.  Explicitly state that no candidate code or
GHA was run.

End exactly with:

```text
TASK360 SEMANTIC RESEAL DEFECTS:       REPAIRED or BLOCKED
TASK360 DOM OWNER / PEAK DEFECT:       REPAIRED or BLOCKED
TASK360 BASELINE REVALIDATION:         REPAIRED or BLOCKED
TASK360 EXACT TYPE / ABI VALIDATOR:    REPAIRED or BLOCKED
TASK360 OUTPUT ATOMICITY / DURABILITY: REPAIRED or BLOCKED
ROWS 1--7 PRODUCER/CHECKER ROUTE:      IMPLEMENTED or BLOCKED
EXECUTION / GHA:                       UNEXECUTED
FULL 48x2 SELFTEST:                    INCOMPLETE
ACTUAL A4:                             remains 1/3
LIFT / FAKE / IHARA:                   NONE
```

`TASK362_R07_A4_V6C_AUTHORITY_TRACE_REPAIR`
