# Luna task 356 - A4/v6a authority physical-trace tranche

Role: Luna, bounded implementation only.  Read this mail and every numbered
prerequisite first to last before editing.  Do not run Python, Node, GAP, GHA,
a workflow, git, or network.  Read-only PowerShell inspection and hashing are
allowed.  Use `apply_patch` for repository edits.

Task355 is honestly `BLOCKED / UNEXECUTED`.  Do not attempt all 96 mutation
cells again.  This tranche implements exactly the common v297 trace substrate
and producer/checker rows 1--7 against actual task198 physical owners.  It is
a candidate API for later integration, not A4 SELFTEST and not an A4 result.

## 1. Binding prerequisites

Read in full, in this order:

1. `sol/proof_r07_actual_owner_first_rejection_trace_v297.md`;
2. task355, all five v6 outputs, and complete reply355;
3. task345, all five v5 outputs, and complete reply345;
4. `sol/sol_reply_343_r07_task336_a4_v4_code_performance_audit_v1.md`;
5. v285, v286, v288, v290, v291, v292, and v293; and
6. the complete accepted task198 physical receipt/manifest/attestation/
   verdict/source chain consumed by v6.

The v6 algebraic/DAG core remains frozen and unaccepted.  Do not edit old
files or claim that this tranche repairs rows 8--48.

## 2. Sole permitted outputs

Create only:

- `search/d972_r07_a4_actual_owner_trace_producer_v1.py`;
- `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v1.py`;
- `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v1_20260829.json`;
- `sol/luna_reply_356_r07_a4_v6a_authority_trace_tranche.md`.

These are separately written producer/checker trace modules and a seven-row
fixture.  They may copy the narrow task198 authority parsing needed for the
ordinary route, but must not import v5/v6 producer/checker main, mutation
harness, transcript, DAG, echelon, or one another.  Do not create a driver;
execution is forbidden and integration is a later versioned task.

## 3. Exact seven rows

Preserve task343 names and order 1--7:

```text
per_layer_ordinal
authority_binding
canonical_input_bytes
resolved_path_traversal
normal_generation_proof
bridge_typed_occurrence_ledger
evaluator_abi_canary
```

The fixture has complete, separate producer/checker rows with owner path,
identity kind, ordinary validator, stage, exact first narrow reason, and
allowed downstream reseals.  It explicitly states `covered_rows=[1..7]`,
`remaining_rows=[8..48]`, `candidate_only=true`, and
`full_a4_selftest=false`.  No empty expected map or guessed runtime value is
allowed.

## 4. Actual physical baseline and mutation construction

Both modules independently implement v297:

1. one-handle physical identity and bounded read for the actual pinned
   task198 receipt, manifest, producer/checker attestations/verdict and three
   source files;
2. path/traversal/link/reparse/TOCTOU checks, with explicit Windows typed
   unsupported behavior if one-handle CreateFileW evidence is unavailable;
3. sorted ASCII canonical JSON, exact self seals and bounded atomic temporary
   owners outside the repository;
4. an ordinary event sink whose events are emitted by ordinary open/decode/
   seal/type/authority validators before reading their owner; and
5. `MUTATION_ACCEPTED` outside the narrow ordinary-rejection catch.

The normal unmutated physical route must pass first.  Each semantic mutation
starts from the actual authenticated receipt/manifest bytes in a fresh owned
temporary hierarchy.  If a later semantic validator must be reached, update
only a versioned local transport manifest/self seal downstream of the changed
owner; record every resealed node.  Never alter a frozen repository owner.

The path-traversal row changes the path owner itself and enters the same
ordinary path resolver.  The canonical-byte row changes actual bytes and
must be rejected at the truthful first transport/canonical validator; do not
force it past an earlier digest failure.  Rows 1, 5, 6 and 7 must physically
mutate a canonical task198 receipt clone, pass the locally resealed transport
owner, and reach the ordinary semantic authority validator.  Row 2 mutates
the actual manifest clone and reaches its ordinary manifest validator.

## 5. Evidence and independence

For every row and side emit the static constructor for this evidence shape:

```text
id, owner, identity_kind,
before_identity, after_identity,
resealed_nodes,
event_trace_digest, entered_validators,
first_rejection {validator,stage,narrow_reason},
baseline_revalidated, terminal_count
```

`before_identity` and `after_identity` are derived from actual baseline and
mutant owner/path identities and must differ.  `entered_validators` comes
only from the event sink.  The expected fixture row is consulted only after
the ordinary call has returned its result.  No mutation-name branch may
select a reason or validator, no `reached=True` assignment may replace an
event, no empty/dummy digest is accepted, and no broad exception is an
expected rejection.

Producer and checker separately reconstruct the relevant task198 row count,
layer transition, normal-generation fields, bridge occurrence type and
coordinate ABI.  They do not share constructors, event ledgers, reason
strings, before/after identities, or semantic validation helpers.

## 6. Static resource and portability contract

Register caps for all opened bytes, temporary bytes, canonical bytes, opens,
writes, events and seven mutation cases before allocation.  The normal
task198 receipt may be read once per side and its immutable parsed baseline
reused under v297 Lemma 6.1.  Do not reread or reparse the 31-MB owner once
per row.  Each mutant envelope is bounded separately.

No local process, pool, subprocess, sleep, retry or poll is permitted.  All
runtime/RSS fields remain `UNEXECUTED`.  Explain Linux and Windows behavior
without claiming an unrun platform result.

## 7. Reply and next gate

The reply gives exact bytes/SHA for the three machine/fixture files, complete
import/authority graph, and line-numbered traces for baseline, each of seven
producer rows and seven checker rows, event extraction, identity comparison,
resealing and hard accepted failure.  Give static cap formulas separately
from measured data.

If all 14 constructors and ordinary validators are statically present,
report this tranche `IMPLEMENTED / UNEXECUTED`; this still leaves A4 at 1/3.
Otherwise report the first missing owner/API as `BLOCKED`.  A fresh Sol(max)
audit of this small tranche is required before it may be integrated into a
full v7 SELFTEST.

End exactly with:

```text
ROWS 1--7 PRODUCER TRACE:        IMPLEMENTED or BLOCKED
ROWS 1--7 CHECKER TRACE:         IMPLEMENTED or BLOCKED
V297 EVENT/IDENTITY SUBSTRATE:   IMPLEMENTED or BLOCKED
STATIC TRANCHE:                  IMPLEMENTED or BLOCKED
EXECUTION / GHA:                 UNEXECUTED
FULL 48x2 SELFTEST:              INCOMPLETE
SOL(MAX) AUDIT REQUIRED:         YES
ACTUAL A4:                       remains 1/3
LIFT / FAKE / IHARA:             NONE
```

`TASK356_R07_A4_V6A_AUTHORITY_TRACE_TRANCHE`
