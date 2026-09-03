# Sol(max) reply Task620: Task601 packed-memory release v2

## Verdict

`PASS_AFTER_REPAIR`

The exact quartet is mathematically faithful to Task618 and its production
paths contain the required compact leaf replay, character-wise block
lifetime separation, and exhaustive online transcript comparison.  I found
no changed route, source graph, coefficient, root, or claim boundary.

It is not yet a release `PASS`, for three small and finite reasons: one
producer canonicality check is an avoidable Python-per-byte hot path; the
checker performs one unneeded all-lower recurrence replay and constructs a
second `RowView` of the complete candidate basis; and the selftest labels
cursor exhaustion/state-boundary coverage without actually exercising both
negative cases.  The production gates themselves are present, so these are
local resource/test repairs, not a mathematical redesign.

## Exact input bindings

All named inputs were read in full.  The four release hashes agree exactly
with Task620.

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_620_audit_r07_task601_packed_memory_release_v2.md` | 5,642 | 88 | `28841a46321fa5e6e0f60735c8b553458c891e1cd44cb84e883734c32c1151ca` |
| `sol/sol_reply_618_audit_r07_task601_memory_terminal_v1.md` | 12,980 | 223 | `e97c2cfc3e7c02ec385245f670335088fe42f128ae3b2ba0c96dd4b46bbdcc88` |
| `sol/luna_task_619_r07_task601_packed_memory_repair_v2.md` | 8,545 | 185 | `3ef92d4e519b82d1137b1331ac841cc6343c2e9c824cc7ca99f0374e98f48026` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | 7,086 | 132 | `e3cfd3b448c11c19bb4973e801bb5eb34dcf9f7744f17da00f694379b802eb79` |
| v468 | 12,016 | 284 | `b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6` |
| v469 | 8,865 | 234 | `bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6` |
| v470 | 8,731 | 225 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |
| v471 | 8,819 | 220 | `38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f` |
| producer | 47,871 | 1,330 | `5f10b486696e992284d64ffcaa2edd69a74c0e6d7ce94c5e5fd703b3c36e4103` |
| checker | 70,507 | 1,970 | `2e4701f7e3d97326411623694e0ae4eb6b52142951e5cce55ba4f78f3cc64fe6` |
| workflow | 5,497 | 111 | `38952d869f8c34f65653282f0db547fdf7d568987e348dfc6c84a2edfcff385c` |

## Adjudications

### 1. Frozen mathematics and universe — pass

The producer still routes the 2,014 registered old offers followed by each
of the four character blocks, with total cursor 8,059, lower/grade offer
counts 2,014/6,398, ranks 1,661/5,044, the exact Task595 coefficient list of
length 3,317, and zero remainder.  No pivot ordering or insertion rule was
changed.  The physical edge order is the reducer's emitted order.

The reverse physical closure begins at every registered MEMBER pivot and
follows all grade and lower intervals without scalar cancellation.  Selected
source descriptors are then exactly the logical origins of that least
closure.  The producer's old/block/defect recursion constructs the full
source closure from those refs, including actor parents, ordered reductions,
seed reductions and transition expressions.  The checker independently
reconstructs that set from the sealed records and requires equality of the
complete key sets.

`C_T` retains the coefficient order, `C_<1` retains the sealed prior terms,
and `C_1` remains `Compose(C_<1,C_T)`.  Manifest and roots retain
`direct_occurrence_replay:false`, `next_degree2_residual:null`, and false
`cross_checked`, `verified`, A0, COMMON, FAKE and IHARA gates.  The checker
performs the full standalone 8,059-offer reroute and final basis/MEMBER
checks; nothing in this snapshot asserts an SLP result before that finishes.

### 2. Producer packed representation and release — pass after one hot-path repair

The production route has one `bytearray` representation for each edge and
row stream.  Edges are appended immediately as `<HB>`; row bytes are appended
directly.  There is no production tuple-edge forest, per-row `bytes` list,
terminal `b''.join`, or whole-stream leaf copy.  The only joins found are in
tiny selftests.  Mutable node tuples last through MEMBER and physical reverse
closure, are packed once as `<IBQIQI>`, and are then deleted.  Dense lower
companions are deleted immediately after the old phase; owners/bodies are
deleted at their character boundaries; both echelon owners, unselected/full
source descriptors, the local route-context binding and row-stream
temporaries are deleted before canonical source/leaf construction.

The defect is producer `append_row` lines 203--207:

```python
any(value > 80 for value in view)
```

It is not an edge-triggered rescan and it retains no data, but it is an
unnecessary Python generator operation for every byte of every appended
physical row.  At the frozen counts it visits 47,964,315 bytes in Python.
Retain the same evidence with one C-level bounded scan, e.g. a length check
followed by `np.frombuffer(view, dtype=np.uint8).max()` when nonempty.  This
is a one-function representation-preserving repair, not permission to remove
canonicality checking or optimize the router generally.

### 3. Producer block lifetime — pass

The route reads, authenticates and validates exactly one block, loads exactly
one owner, consumes every pivot, then explicitly deletes owner and body
before the next character.  It retains only compact logical descriptors and
the four digests.  After the physical selected set is known, it reads each
needed character at most once more, checks the same digest, copies all and
only the selected canonical DAG closure for that character, and deletes the
body.  There is no four-body producer list and no reload per selected origin.

### 4. Compact derived receipt — pass

No expanded `derived.states` or state-child history exists in the production
path.  Adjoint work retains only the live coalescing pending map, final leaf
map and scalar counters.  `source-ancestry.json` contains the canonical graph
and small derived metadata, not leaf contents.  `literal-leaves.bin` is a
separate authenticated receipt.

The `<8sBBBB32sQ>` header fixes magic/version, flags `(1,0,0)`, the raw
source-ancestry digest and record count.  Each `<IIBI>` record carries an
unambiguous remaining-payload length, seed, nonzero coefficient and path
length, followed by signed `int8` letters.  Both parsers reject short or
trailing data, inconsistent lengths, zero/bad coefficients, zero or
out-of-alphabet letters, adjacent inverse pairs, duplicates and non-strict
canonical order.  The ancestry contains only the leaf filename/schema/flags;
the leaf header binds the already computed ancestry digest, so there is no
digest cycle.  Metadata and header agree on
`(quotient_specific_evaluation, common_source_witness, states_exported) =
(true,false,false)`.  The canonical source graph remains the authority.

### 5. Independent exact-leaf derivation — pass

The checker neither imports nor calls the Task601 producer.  It first checks
the canonical graph against the sealed old/block records and its exact least
closure, then starts a new pending map at all 3,317 authenticated roots.  Its
word reducer is independently written and multiplies `prefix` on the left
and the new actor/pure word on the right, matching the registered recurrence.

The coefficient propagation is correct in every branch: grade and lower
origins carry the node scale, their reductions carry `-scale*coefficient`;
block actor/defect origins carry the block scale and block reducers its
negative; transition defects add the acted old parent without an extra scale
and subtract their exact expression; projected seeds carry the old scale and
character sign; seed defects carry the character sign; and every old/block/
defect reduction has the required negative sign.  Arithmetic is reduced
modulo three, so coefficient two is not collapsed to one.  The checker then
uses its own encoder and compares every generated chunk and terminal byte
against the complete authenticated leaf stream.  The exported leaf map is
comparison evidence only.

### 6. Zero-copy views and redundant scans — pass after two local deletions

Ancestry is parsed exactly once.  Node and edge access is fixed-index
`memoryview`/`Struct.unpack_from`; row access is a zero-copy slice.  The old
`gedges`, `ledges`, concatenation, Python expected edge/row lists and final
joins are absent.  `RowView.__getitem__` does not revalidate or rescan a row,
and its canonicality test is one NumPy scan when the view is constructed,
not one scan per edge.

Two avoidable full passes remain:

1. `validate_physical_streams` lines 518--527 replays all 1,661 lower rows,
   while the corresponding grade replay is correctly gated to the selected
   set.  V469 requires this pre-router physical replay only for reached lower
   nodes; the later standalone route already reconstructs and cursor-compares
   every accepted lower row.  Gate this loop by `declared_lower`.  The whole
   lower receipt still gets its one canonicality scan, and every unselected
   row remains covered by the mandatory full independent reroute.
2. The candidate basis is wrapped in a canonicality-checking `RowView` at
   line 516 and again at line 1487.  Pass/reuse `physical["basis"]` in the
   independent comparison instead of constructing the second view.  The
   independent row-by-row equality, final SHA and MEMBER equation remain
   unchanged.

The separate all-zero test for `old-lower-zero` is semantically necessary
and small; it is not to be deleted.  It may use one NumPy `any` over that
receipt instead of Python row iteration, but that optional micro-change is
not a release condition.

### 7. Checker block lifetime — pass

Selected sealed source/origin replay is grouped by character.  Old blobs are
released before that character's block load; one block body and owner are
live, then both are deleted before the next character.  The function returns
and its canonical/source objects and `prepare` are deleted and collected
before `independent_transcript_check` invokes the standalone router.  The
router's already accepted four-block source representation therefore does
not overlap a checker-side body/owner cache, and its entries are released as
each block completes.

### 8. Online independent comparison — pass

`OnlineReceipts` owns exact cursors for lower/grade nodes, lower/grade edges,
all four nonzero row receipts and `old_lower_zero`.  Every accepted node is
compared at the current node cursor; every emitted ordered reduction is
compared at the corresponding edge cursor; every origin, stored row and
companion advances its row cursor.  `finish()` requires equality with the
length of every authenticated view, so omission and trailing records fail.

Crucially, line 1390 advances `old_lower_zero` immediately whenever an old
offer's lower remainder is zero, before testing whether its subsequent grade
insertion is accepted.  Thus dependent as well as accepted grade offers
consume exactly one zero row.  Terminal checks require cursor 8,059, counts
2,014/6,398, ranks 1,661/5,044, full stream exhaustion, independently rebuilt
basis SHA, zero remainder, exact coefficient list and explicit 3,317-term
MEMBER reconstruction.

### 9. Diagnostics — pass

Both programs report elapsed/current/peak RSS and bounded counters without
per-row logging.  Producer boundaries cover old completion, each routed block
release, route/MEMBER/closure, packed temporary release, periodic 65,536-state
adjoint progress, graph/leaf sealing and payload sealing.  Checker boundaries
cover its single ancestry parse, every selected character release, pre-router,
every independent old/block boundary (including the zero-row cursor), final
basis/MEMBER and verdict.  Each has a 64-KiB reserve and a dedicated
`MemoryError` branch that drops the reserve and uses bounded ASCII `os.write`
without JSON construction.  Resource failure remains `UNKNOWN_RESOURCE`.

### 10. Workflow — pass

The workflow pins the exact producer, checker and Task601 reply hashes above,
checks the v3 producer hash before import/download work, and uses marker
`[fire-grade1-selected-slp-v2]`.  Checkout, Python setup, download and upload
actions are commit-pinned.  Source `33677346616/1`, Task595 candidate
`33707397894/1`, and candidate commit
`93f746ad1b649796e1bc28e00ff34993498929ee` are unchanged.  Producer and
checker run serially under a 60-minute job, `ulimit -v 8388608`, 7-GiB RSS
guard, 40-minute internal guard and 45-minute process bounds.  Payload/verdict
upload is success-only and logs are always uploaded.

### 11. Small gates — pass after fixture correction

I ran only the permitted local gates, serially.  Syntax compilation exited
zero.  Producer and checker selftests emitted the exact PASS JSON recorded in
the Luna reply, and static YAML parsing succeeded.  No real route was run.

The production cursor gate is correct, but the checker selftest consumes its
tiny streams and calls `finish()` only in the success case; its sole negative
case is a mismatched node value.  Consequently the reported
`zero_copy_cursor_exhaustion:"PASS"` does not demonstrate rejection of an
unconsumed/trailing authenticated stream.  Add one tiny `OnlineReceipts`
case that deliberately leaves at least one node/edge/row cursor short, calls
`finish()`, and requires `authoritative_cursor_exhaustion`.

Likewise, the production parser correctly requires leaf header
`states_exported=0` and ancestry validation rejects a `states` member, but
the fixture only inspects a clean dictionary.  Add a mutation of the header
states byte to one and, preferably through the same derived-metadata
predicate used in production, inject a `states` member and require rejection.
This is the missing negative state-boundary fixture; it does not authorize a
new selftest framework.

## Mandatory finite repair list

1. Vectorize only producer `append_row`'s canonical-byte scan; preserve its
   length and `<=80` gates.
2. In checker pre-router physical replay, visit only `declared_lower` rows;
   retain the later full online reroute of all 8,059 offers.  Reuse the first
   candidate-basis `RowView` instead of constructing/scanning it twice.
3. Add the two tiny negative fixtures: unfinished cursor exhaustion and the
   forbidden states boundary.  Retain all existing mutation/claim fixtures.
4. Re-run syntax compilation, both small selftests and YAML/static checks,
   then refresh producer/checker/reply workflow pins and submit the stable
   quartet to the same Task620 audit.  No other optimization or framework is
   requested.

These repairs do not alter any serialized mathematical value or accepted
predicate.  After they pass a fresh static audit, one Task618-authorized GHA
rerun is justified.  The remaining empirical risk is only the as-yet unknown
real leaf population, peak RSS and wall time, plus the permitted standalone
router's four-block representation after lifetime separation.  A later
resource terminal remains `UNKNOWN_RESOURCE`.

This `PASS_AFTER_REPAIR` does not authorize committing or running the current
quartet.  `production = NOT_RUN`; `GHA = NOT_RUN`; `git = NOT_RUN`; full
8,059 local route = `NOT_RUN`.  Only this specified reply file was written.

`R07_TASK601_PACKED_MEMORY_RELEASE_V2_PASS_AFTER_REPAIR`
