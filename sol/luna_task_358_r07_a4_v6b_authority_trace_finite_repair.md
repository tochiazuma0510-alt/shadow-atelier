# Luna task 358 - A4/v6b rows 1--7 authority-trace finite repair

Role: Luna, bounded implementation only.  Read this mail and every numbered
section first to last before editing.  Do not run Python, Node, GAP, GHA, a
workflow, git, network, or any candidate command.  Read-only PowerShell
inspection and hashing are allowed.  Use `apply_patch` for repository edits.

Task356/v6a is frozen and task357 rejected it before execution.  This task is
the single finite successor for the same rows 1--7 tranche.  It must repair
all nine task357 findings together; fixing only the first manifest/ordinal
stops is not a completion.

## 1. Binding prerequisites

Read in full, in this order:

1. `sol/luna_task_356_r07_a4_v6a_authority_trace_tranche.md`;
2. all four task356 outputs and the complete task356 reply;
3. `sol/sol_reply_357_r07_task356_a4_v6a_authority_trace_code_performance_audit_v1.md`
   (26,587 bytes, SHA-256
   `c3c376743b96d066bbea9968720e1b00b7c81f14612467787499dc17991737d8`);
4. v291, v292, v293, v297 and v298 in `sol/`;
5. the complete actual task198 receipt, acceptance manifest, attestations,
   verdict and producer/checker/driver sources pinned by v6a.

The v1 files are immutable rejected evidence.  Do not copy a task357 expected
reason into an observed row and do not modify task198.

## 2. Sole permitted outputs and scope

Create only:

- `search/d972_r07_a4_actual_owner_trace_producer_v2.py`;
- `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v2.py`;
- `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v2_20260829.json`;
- `sol/luna_reply_358_r07_a4_v6b_authority_trace_finite_repair.md`.

The fixture remains non-synthetic, candidate-only, `covered_rows=[1..7]`,
`remaining_rows=[8..48]`, and `full_a4_selftest=false`.  No driver, workflow,
GHA execution, rows 8--48 implementation, algebra/DAG merge, A4 completion,
lift, fake or Ihara claim is allowed.

## 3. Correct actual manifest and receipt codecs

Implement two distinct canonical codecs.

- The task198 receipt uses top-level `self_digest_sha256`.  Remove exactly
  that key, hash the sorted compact ASCII body, and insert exactly that key.
- The task198 acceptance manifest uses top-level
  `manifest_self_digest_sha256`.  Remove exactly that key, hash the sorted
  compact ASCII body, and insert exactly that key.  A top-level
  `self_digest_sha256` in a manifest is forbidden.

The ordinary parser checks the exact raw canonical framing used by the actual
owners, not merely semantic JSON equality.  The fixture immutable identities
and every downstream reseal label distinguish the two seal types.  Rows
1/5/6/7 reseal the receipt and manifest receipt binding plus the actual
manifest seal; row 2 reseals only the actual manifest seal; rows 3/4 reseal
nothing.  The actual baseline must pass both codecs before any mutation is
attempted.

## 4. Exact authority semantics and types

Rows are ordered by physical layer blocks but ordinals reset within each
layer:

```text
Gamma_Cayley: positions 1..6318, ordinals 1..6318
action:        positions 6319..6422, ordinals 1..104
Q0_lift:       positions 6423..6441, ordinals 1..19.
```

Require exact Python types (`type(x) is int`, excluding Boolean) and exact
key/list shapes for row count, layer counts, row ordinal/layer records,
normal-generation proof, all occurrence-ledger fields, and evaluator ABI.
Recompute the full canonical occurrence-ledger digest from the typed ledger
and require equality both to its stored digest and the frozen constant.  Do
the analogous underlying-owner binding for the evaluator coordinate ledger;
a hard-coded stored digest alone is not a validator.  Derive the exact schemas
from the opened actual task198 owner and its accepted source/checker contract,
not from the seven mutation names.

Validate the complete acceptance-manifest graph against the already opened
physical pins: receipt, producer/checker attestations, checker verdict,
producer/checker/driver source identities, producer/checker run, head,
artifact/member and terminal bindings.  Also compare the local manifest's
nested receipt self seal with the locally opened receipt's claimed seal.

## 5. One ordinary path route; no row-4 bypass

Delete `receipt_name` or every equivalent case-specific basename override.
There is one ordinary ordering for baseline and all mutations.  Admit both
manifest and receipt paths through the physical containment route before
using manifest semantic receipt binding, so row 4 reaches the registered path
rejection without a mutation-name branch or a forged basename.  Path
admission must preserve lexical ownership and must not call `.resolve()` on a
possibly symlinked fixture or candidate before the no-follow open.

Use supported-POSIX directory/final-component no-follow semantics sufficient
to prevent a parent-component or final-component substitution.  Windows or a
platform lacking the registered one-handle API returns only the typed
unsupported input result and never a PASS.

## 6. Actual V297 witness and deterministic V298 projection

Build the raw identity directly from the opened fd's before/after `fstat` and
pathname-after record while the handle is still live.  Do not close and then
perform a second `lstat` to manufacture the public booleans.  Keep raw
device/inode/mtime/temp-path data internal; project only v298 stable fields.

Producer and checker independently derive owner, identity kind and logical
case from their actual constructor/observation before comparing with the
fixture.  They must not copy those evidence fields from the fixture.  The
checker records `canonical_after_sha256` immediately after successful decode
and canonicality checking, just as the producer does.  Require actual stable
before/after inequality, actual ordinary-entry prefix, exact caught narrow
first rejection, measured `terminal_count=1`, actual owner cleanup and
baseline revalidation for every row.  `MutationAccepted` stays outside the
narrow rejection catch.

Each case has an isolated physical workspace.  A hard link is removed before
the next case and the unchanged baseline link/handle/path identity is checked
again.  `owner_disposed=true` means the case path owner has actually been
removed/restored, not merely that a file descriptor was closed.

## 7. Pin the fixture and keep the graph acyclic

Both v2 sources pin the exact relative v2 fixture path, byte length, SHA-256
and canonical self seal.  Open that lexical path through the same physical
no-follow owner; reject any arbitrary absolute `--fixture`.  The fixture does
not pin either v2 program, so the dependency graph is acyclic.  The reply,
which is not an input owner, records all four final identities.

## 8. One end-to-end meter and finite performance repair

Use one meter per invocation from fixture authentication through baseline,
all seven cases and optional output.  Reserve before every large allocation,
DOM/deepcopy/canonicalization/write/open; do not allocate first and charge
later.  Static caps must cover peak live memory as well as cumulative I/O.

Implement all task357 avoidable-work repairs:

1. read/parse the registered receipt and manifest once; do not perform the
   second 31-MB baseline read;
2. if baseline immutability is rechecked per case, retain a bounded baseline
   handle/identity and compare live fd/path records without rereading bytes;
3. cache the baseline canonical receipt/body/rows digests once;
4. seal a changed receipt or manifest with one body serialization, one hash
   and one final serialization--no triple serialization;
5. perform at most one necessary full parsed-receipt clone per semantic row;
6. evict every exact workspace cache entry at case completion and assert that
   no key under that workspace remains; do not use a platform-specific
   substring such as `"\\Temp\\"`;
7. do not retain the five mutant receipt raw blobs (186,103,472 bytes with
   baseline) after their cases;
8. use streaming/cached hashes where they preserve the exact ordinary
   validator; never replace typed equality by a digest Boolean; and
9. use no sleep, retry, polling, process, pool or subprocess.

Optional output must reject an existing/stale target, bind the parent
directory identity, use an exclusive staged owner, fsync file and directory,
and publish last.  No output is required in this tranche.

## 9. Reply and terminal matrix

The reply gives exact bytes/SHA-256 of all three machine files, complete
source/authority/import graph, line-numbered producer/checker traces for all
seven rows, the exact manifest reseal DAG, static cumulative-I/O and peak-live
memory formulas, cache eviction proof, and all remaining limitations.
Measured runtime/RSS is `UNEXECUTED`.

End exactly with:

```text
TASK357 NINE-ITEM REPAIR:          IMPLEMENTED or BLOCKED
ACTUAL BASELINE ROUTE:             STATICALLY REACHABLE or BLOCKED
ROWS 1--7 PRODUCER TRACE:          IMPLEMENTED or BLOCKED
ROWS 1--7 CHECKER TRACE:           IMPLEMENTED or BLOCKED
V297/V298 PHYSICAL SUBSTRATE:      IMPLEMENTED or BLOCKED
STATIC CAPS / PERFORMANCE:         IMPLEMENTED or BLOCKED
EXECUTION / GHA:                   UNEXECUTED
FULL 48x2 SELFTEST:                INCOMPLETE
SOL(MAX) REAUDIT REQUIRED:         YES
ACTUAL A4:                         remains 1/3
LIFT / FAKE / IHARA:               NONE
```

`TASK358_R07_A4_V6B_AUTHORITY_TRACE_FINITE_REPAIR`
