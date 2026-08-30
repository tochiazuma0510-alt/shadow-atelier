# Luna task 431 — A0 v12 phase-separated packed owner

Read `sol/proof_r07_a0_phase_separated_packed_echelon_v407.md` completely.
Implement its exact owner.  This is the direct successor of task430/v11; do
not reopen quotient formulas, actors, the 44-seed universe, the six-action
oracle, or positive claim rules.

## Actual input and reason for the version

GHA run `33320103188`, job `99280454030`, head
`eb840541ece21f394a6ac46b1b7a6e0a6cd5a301`, reached:

```text
status                    UNKNOWN_RESOURCE:rss_limit
seed_cursor               44
parent_cursor             86
action_cursor             344
occurrence_rank           344
physical_rank             344
frontier_length           258
occurrence_pivot_nnz      31,847,811
physical_pivot_nnz        38,056,986
checkpoint_seq            10
checkpoint bytes          275,905,469
checkpoint sha256         3ac222801a1a91b8e0f163554835e569a26c2cac0f3f8bea481e1825e5f911b8
```

The independent v11 checker accepted this only as `UNKNOWN_RESOURCE` with a
sealed continuation.  All claim flags are false.  V405 §3--§4 explicitly
requires occurrence closure first and physical insertion afterward; v11
unnecessarily held both echelons during the first phase.

The exact artifact is mirrored permanently as a public release asset:

```text
url     https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9735328330_gap-run-out.valid.zip
bytes   211,296,971
sha256  b044eb9d730cb99c39253aedc573f8bba764ade0f732920e2ad7c306a5a3db92
```

The zip has exactly six expected files, including
`d972_r07_a0_pb34_direct_quotient_owner_v11_output.checkpoint`; extraction of
that entry was independently replayed and gives the checkpoint bytes/SHA
above.  Do not use the deleted, corrupt non-`.valid` asset name.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v12.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v12.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v12.g`;
4. `sol/luna_reply_431_r07_a0_phase_separated_packed_owner_v12.md`.

Do not edit v11 or earlier files, workflows, proofs, v220, release assets,
checkpoints, or artifacts.  Do not commit, push, dispatch, or run production
locally.

## 1. Frozen mathematics and v11 behavior

Clone v11 and preserve exactly:

- the pinned v3 dependency and all quotient/component/transversal formulas;
- `central_power3`, per-occurrence actor and seed construction;
- the 44 accepted seeds and four-letter occurrence frontier;
- the six PB4 action roster `[5:11]` and v404 support oracle;
- exponent coordinates, signs and `target + correction + actions = 0`;
- literal exactification and all positive replay gates;
- 9000-second owner limit and 4,800,000,000-byte production RSS cap;
- fail-closed `UNKNOWN`/`UNKNOWN_RESOURCE` and all false claim flags unless a
  strict `COMMON_CANDIDATE` envelope is produced.

Never emit `COMMON_WORD`, `MEMBER`, `NONMEMBER`, fake, compatible lift, Ihara
witness, or verified.  An empty six-action accumulator remains the existing
exact-separator `UNKNOWN` envelope, not a promoted theorem in this task.

## 2. Packed coordinate registry and pivot rows

Use one owner-local registry with:

```text
keys: list[bytes]                 # id -> exact coordinate bytes
ids:  dict[bytes,int]             # rebuilt on resume, not serialized twice
```

Require `sys.byteorder == "little"`, `array('I').itemsize == 4`, unique
registry keys and fewer than `2**32` coordinates.  A stored pivot row must be
the primitive marshal-safe pair:

```text
(little-endian uint32 id blob, aligned coefficient byte blob)
```

with equal entry counts, strictly increasing ids, coefficients only 1 or 2,
and every id in the registry.  Candidate/work rows remain ordinary byte-keyed
sparse dictionaries.  Select `p=min(work_row)` before packing, so the frozen
byte-lexicographic pivot is unchanged.  Stored-row axpy and dual operations
decode through `keys` and must be coefficient-for-coefficient identical to
v11.

Do not store a Python dict per pivot row and do not keep a second decoded
copy.  Maintain each echelon's payload-nnz counter incrementally.  Progress,
checkpoint and resource logging must use that counter; do not rescan all
pivots merely to print nnz.  Expression dictionaries and typed source lists
remain unchanged.

## 3. Exact v11 migration before heavy runtime bootstrap

Add one production-only `--resume-v11-url` argument.  Accept exactly the URL,
zip bytes/SHA, entry name and checkpoint bytes/SHA preregistered above.

Before constructing `core.Runtime`, the matched groups or target:

1. stream-download the public zip to a relative `ci/in` temporary file while
   hashing and counting bytes; atomically seal it;
2. use Python stdlib `zipfile`, reject duplicate/absolute/traversal entries,
   require the exact expected six-name roster, and stream-extract only the
   v11 checkpoint while checking CRC, bytes and SHA;
3. check the checkpoint outer header/seal, exact v11 schema and binding;
4. load the v11 state once;
5. immediately discard all four partial physical fields.  They are redundant
   by v407 Lemma 2.1 and must never be repacked;
6. validate and pack the occurrence rows one at a time, removing each raw
   row as its packed replacement is created;
7. retain exact occurrence order, expressions, sources, queue and the three
   cursors `44/86/344`;
8. set the v12 phase to `occurrence_queue`, physical state empty and
   `physical_cursor=0`;
9. collect garbage and call Linux `malloc_trim(0)` best-effort if available;
10. require post-migration RSS below the unchanged 4.8 GB production cap and
    write a sealed v12 checkpoint before runtime bootstrap or another actor.

The v11 release mirror is immutable input.  On any mismatch or migration
resource failure, emit fail-closed diagnostics and do not silently restart.
Do not hold the zip bytes in RAM, do not import third-party download/archive
packages, and do not make two whole-file seal scans.

## 4. Three exact production phases

### A. `occurrence_queue`

Continue the migrated queue from parent 86.  Physical echelon must remain
empty.  A rank rise stores/enqueues only the packed occurrence pivot and its
source expression.  Periodic checkpoints retain every packed occurrence row,
queue item, expression/source and cursor.

### B. `physical_build`

After the queue exhausts, iterate the fixed occurrence order from
`physical_cursor`.  For each pivot:

1. decode and aggregate its normalized packed occurrence row;
2. compute a deterministic sparse-row SHA-256 using sorted raw coordinate
   bytes plus coefficient framing;
3. insert the aggregate into the packed physical echelon with source
   `{family:"PHYSICAL", occurrence_pivot, source_digest}`;
4. advance `physical_cursor`;
5. delete that occurrence coordinate payload and decrement only the
   occurrence payload-nnz counter.

Do not delete occurrence order, expression maps or sources.  Save periodically
and after the final pivot.  A checkpoint in this phase has payload rows exactly
for the unprocessed suffix and a physical echelon for the processed prefix.

### C. `six_action`

Require all occurrence coordinate payloads absent and
`physical_cursor == occurrence_rank`.  Run the unchanged v404 dual/support
loop, storing new physical action pivots in packed form.  Save after rank
rises and at every terminal.

Resume must dispatch from the recorded phase without rebuilding completed
physical prefixes or replaying processed parents.

## 5. DAG-only positive reconstruction

Modify positive replay only as required by the deliberately deleted
occurrence payloads.  `atoms_pivot` continues to use occurrence expression
maps and sources.  For each selected PHYSICAL source:

1. expand its atoms;
2. rebuild each leaf using the authenticated seed;
3. apply stored prefix actors in reverse tuple iteration;
4. combine with the exact F3 coefficients and physically aggregate;
5. require the rebuilt sparse-row digest to equal `source_digest`;
6. use that freshly rebuilt row in the selected correction sum.

Then run every existing v11 literal word, exponent-zero, joint-state, fresh
Fox, quotient-normal, selected-action and target-zero gate.  Digest equality
is an additional canary, never a replacement for fresh replay.

## 6. Checkpoint and checker contract

Use a fresh v12 schema/header/binding and fresh paths.  Serialize the registry
key list once, packed rows, incremental nnz counters, phase,
`physical_cursor`, full cursors/frontier, expressions and typed sources.

The checker must independently reject:

- bad outer seal/schema/binding or non-little-endian packed contract;
- duplicate registry keys, out-of-range/duplicate/non-increasing ids;
- misaligned id/coefficient blobs or coefficients outside 1/2;
- pivot normalization failure after decoding;
- expression/source index failures;
- queue references absent during `occurrence_queue`;
- nonempty physical state during `occurrence_queue`;
- a `physical_build` prefix/suffix mismatch;
- surviving occurrence payloads in `six_action`;
- source-digest shape failures;
- raw pivot dictionaries or old eliminated-boundary rows;
- checkpoint/result identity mismatch or any claim promotion.

For `UNKNOWN_RESOURCE`, a valid output checkpoint is mandatory.  A
`COMMON_CANDIDATE` remains only a candidate envelope with strict replay data.

## 7. Bounded fixtures and performance gates

Run locally only bounded fixtures.  They must cover:

1. legacy v11 Echelon versus packed Echelon on the same nontrivial insertion,
   dependence, reduction, expression and dual sequence;
2. all packed corruption gates listed above;
3. toy v11 migration proving physical rows are discarded while occurrence
   rows, queue, sources, expressions and cursors are preserved;
4. simultaneous versus deferred physical insertion giving the same span;
5. streaming deletion and phase-resume prefix/suffix invariants;
6. DAG atom reconstruction, reverse-prefix order and digest equality;
7. resource-stop durable fallback and fresh-object mutation rejection.

Static/performance audit must establish:

- no stored pivot row is a Python dict;
- no full-pivot nnz rescan occurs in progress or checkpoint hot paths;
- no physical insertion occurs before occurrence exhaustion;
- no zip/checkpoint whole-file duplicate read;
- no self-test/fixture is executed in production;
- no full closure or production bootstrap is run locally.

## 8. Driver

The v12 GAP driver must pin exact producer/checker bytes and SHA, require
external `D972_R07_A0_PB34_V12_RUN:=true`, pass the exact release URL through
`--resume-v11-url`, use fresh v12 artifact/output checkpoint/log paths, 9000
seconds, 4.8 GB, one producer and one checker, live `tee`, and generic
`gap-run.yml` compatibility.  It must not request p-quotient packages or
modify/download through workflow-specific steps.

Run syntax compilation, producer fixture and checker self-test only.  End the
reply with `V12_LOCAL_GO_FOR_PARENT_AUDIT_AND_DISPATCH` or precise `NO-GO`.
