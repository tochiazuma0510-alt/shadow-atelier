# Luna task 157dr — packed relative-Frattini v3

## Role and objective

You are Luna.  Implement a **versioned, semantics-preserving v3** of the
frozen 157dn relative-Frattini sparse-DAG search.  The two v2 production runs
both lost the hosted runner at essentially the same deterministic point
(about 121 minutes); the second run already had `timeout_min=350`, so this is
a memory/resource failure, not an external timeout.  Neither run produced a
checkpoint or artifact.  Do not resume or rerun v2.

The v3 objective is to preserve the registered mathematical universe and
acceptance predicate while replacing the memory representation that exceeded
the roughly 7 GiB hosted-runner budget.

Frozen v2 references:

```text
search/d972_b345_relfrat3_v2.py
  fad364043926dbdc03e56accf089f454d625e0b315c98a7647bc891677313cc8
search/check_d972_b345_relfrat3_v2.py
  3c8967bea6946b42cef08cd097eab4e9071aae203ee27ac38038c4d5adb83f07
search/d972_b345_relfrat3_gha_driver_v2.g
  006e33e97c6f9ac1982887206c904dbcf423c95790ec2fe0c45d9a1b3a2e38aa
```

The q=3 receipt and all older source pins, formulas, candidates, and gates are
the same frozen inputs used by v2.  Recompute and pin their exact current SHAs
rather than copying a value without checking it.

## Authorized files

Create only these four new files:

```text
search/d972_b345_relfrat3_v3.py
search/check_d972_b345_relfrat3_v3.py
search/d972_b345_relfrat3_gha_driver_v3.g
sol/luna_reply_157dr_relfrat3_packed_v3.md
```

Do not edit v1/v2, q3 sources, any workflow, any existing receipt, or any
other file.  Temporary diagnostics must live outside the repository.

## Non-negotiable semantic invariants

The following are byte-for-byte or mathematically identical to v2, except for
the explicitly versioned internal representation and resource/accounting
schema:

1. the 4096 correction dictionary and its order;
2. cheap/full candidate gates and candidate priority;
3. translation BFS order `+1..+6,-1..-6` and the 1,2,4,... geometric
   checkpoints;
4. the exact left-Fox convention, PB4 relator columns, F3 row-space
   membership, normalized inverse fibre, and literal acceptance predicates;
5. PASS / SEARCH_INCOMPLETE / UNKNOWN_RESOURCE meanings, including no
   obstruction claim on a resource stop;
6. a PASS exports a lossless proof DAG whose leaves, sections, translated
   Fox columns, roots, and candidate residuals are independently replayable;
7. changing cache capacity or eviction order must never change a quotient
   value, row space, selected candidate, or terminal.

The sparse pivot may use packed integer storage, but its comparison must be
the v2 canonical `(component, EKey)` order (or an independently proved exact
equivalent).  Do not silently use insertion-order element IDs as the pivot
order.  The row space is invariant, but preserving this order gives a strong
differential canary and avoids an unregistered search-order change.

## Required v3 implementation

### A. Exact element interning

Intern every persistent E4 element exactly once.  Give it a stable integer
ID and store its canonical permutation-144 and PC coordinates in a compact
representation (for example immutable bytes).  Equality is exact; a digest
must not be used as an equality surrogate.

Use integer IDs for all persistent hot structures:

- sparse vector keys (pack component plus element ID into one integer where
  practical);
- pivot rows;
- translation BFS seen/queue state;
- DAG translated-leaf payloads;
- inverse-cache tuple keys;
- candidate gradients and translation maps.

Full tuple/byte values may be created transiently for group operations and
are expanded only at a certificate boundary.  The positive receipt must map
every exported ID through a canonical element registry, and the checker must
reconstruct the actual permutation/PC value rather than trust the ID.

Record pool size, packed bytes, hits/misses, and the exact equality/canonical
ordering contract.  Put explicit caps on the pool and every bounded cache.

### B. Remove the hidden unbounded PC cache

The v2 `PcCollector.cache` keys arbitrary full token words and is unbounded.
It can independently consume multiple GiB.  It must not survive in the hot
path.

Keep only bounded, semantics-neutral caches: fixed generators/inverses and a
bounded pair-product/transition LRU (or an exact equivalent).  Eviction only
affects speed.  Record capacities, peaks, hits, misses, and evictions.  Add a
canary proving that cached and uncached collection return identical canonical
coordinates on a registered finite test corpus.

### C. Lazy section SLP

The BFS must store `parent element ID + signed generator letter`, not a copied
word per queue entry or pivot.  Preserve the exact first-seen shortlex BFS
section.  Support cancellation/reconstruction without quadratic word copying.

Materialize a section only for a proof-DAG leaf reachable from an actual PASS.
Re-evaluate every materialized section to its element before serialization.
Add a differential canary comparing the lazy section with the v2/reference
BFS section on a bounded deterministic prefix.

### D. Drop unused candidate section maps

During the search, cache only candidate names, compact gradients, quotient
values needed by gates, and the correction index.  Do not retain the
`dict[EKey, full-prefix-word]` maps that v2 builds for every target of every
survivor.  Once a PASS is found, regenerate the selected candidate and its
targets, require exact equality with the cached compact gradients/values, and
then build only the sections needed by the exported certificate.

### E. Packed in-memory provenance DAG

Replace per-node Python dict/list objects with compact parallel arrays or an
equivalently bounded packed structure for node kind, relator/translation ID,
edge offsets, parent IDs, and F3 coefficients.  Preserve strict backward
references, rollback semantics, caps, and the v2 algebraic invariant.

Only the union reachable from PASS roots is serialized.  Use a versioned,
lossless compact certificate (parallel integer arrays encoded as bounded
JSON/base64 fields are preferred); **do not** re-inflate millions of Python
dict/list node objects merely to write JSON.  Bind each packed array's type,
length, endianness, cap, and SHA256 in the receipt.  The independent checker
decodes those arrays and reconstructs every leaf column and every linear
node from actual finite quotient values.  It must never accept a receipt by
trusting v3's internal IDs or packed bytes.  If the reachable certificate
cannot be serialized below the RSS guard, return honest UNKNOWN_RESOURCE
rather than losing the runner after finding an uncertified candidate.

### F. Process isolation and live output

The full driver must regenerate and independently check q3 exactly once in a
**separate GAP child process**.  The child must use the same package root and
load requirements as the outer `gap-run.yml` invocation, write a fixed child
script, verify its exact readback, and exit before the Python producer starts.
The outer driver then verifies the frozen q3 artifact SHA, q3 checker sentinel,
and unique PASS marker.  This releases the q3 GAP heap before the Python hot
loop.  Do not change the workflow.

Run producer and checker unbuffered.  On Linux full mode use `bash -o pipefail`
and `tee` so progress is visible while preserving exit status; create the
success sentinel only after the pipe succeeds.  Local selftest mode may use a
portable non-tee path.  Delete all stale artifacts/logs/sentinels first.

Emit and flush progress at powers of two and at least every 30 seconds:

```text
phase elapsed current_rss peak_rss translations columns pivots
live_sparse_entries element_pool dag_nodes dag_edges candidate_cache
pc_cache_hits pc_cache_misses pc_cache_evictions
```

No progress logging requirement may change the search order or keep large
objects alive.

### G. Fail-closed RSS and wall guards

Read current Linux process RSS from a primary OS interface such as
`/proc/self/status` (with a documented portable fallback for selftest).  Use a
4.5 GiB soft RSS limit and the existing 300 minute wall soft limit.  Check both
on the existing elimination cadence and before expensive serialization.

On a guard hit:

- capture bounded accounting;
- release/clear the large basis, DAG, candidate, and transient caches before
  writing the receipt;
- return `UNKNOWN_RESOURCE` with the precise reason and no obstruction claim;
- let the independent checker validate the resource/accounting branch.

The guard must fire before hosted-runner loss and leave a checkable artifact.
Do not add checkpoint/resume in v3.  A sound persistent checkpoint is deferred
to a later version if this packed run still reaches a guard.

## Independent checker

The v3 checker may reuse frozen mathematical constants, but must not import
the producer or share its element pool, collector, cache, section SLP, DAG, or
encoding helpers.  It must:

- rebuild quotient arithmetic independently;
- validate pool uniqueness/canonical encodings and all accounting caps;
- reconstruct reachable leaf elements and lazy sections from receipt data;
- reconstruct each translated Fox column and every F3 DAG node/root;
- replay all positive literal/onto gates;
- reject malformed IDs, collisions, forward references, unreachable inserted
  nodes, bad parent chains, cache-accounting drift, and a resource branch that
  asserts a mathematical obstruction;
- bind exact source SHAs and an exact v3 schema/key layout.

The checker need not duplicate the producer's memory optimization; correctness
and helper independence take priority.  It may stream reachable nodes if that
is necessary to stay within the runner budget.

## Tests and freeze discipline

Run at most one lightweight producer/checker differential selftest after the
first complete implementation.  It must include a bounded toy/reference
comparison for:

- exact EKey interning and canonical pivot order;
- cached versus uncached PC collection;
- v2/reference BFS order and lazy sections;
- translated columns, incremental row-space membership, and checkpoint solves;
- packed DAG rollback/reachability/serialization;
- RSS-guard UNKNOWN and all terminal mutations.

If that single run exposes a fixture-only mistake, report it and request one
explicit corrective rerun rather than silently rerunning.  Do not run the full
producer locally.  Do not run GAP production, Git, or GHA.

Before freezing, perform a static audit of syntax, exact pins, authorized-file
scope, terminal-marker uniqueness, shell quoting, stale artifact removal, and
the absence of unbounded hot caches/full section maps.

## Reply contract

Write `sol/luna_reply_157dr_relfrat3_packed_v3.md` with:

- final SHA256 and byte count of all three code files and the reply;
- exact v2-to-v3 semantic invariants;
- all cache/pool/RSS caps and accounting fields;
- selftest command/result and mutation count;
- source-only runtime/RSS estimate, explicitly labeled as an estimate;
- exact proposed GHA inputs, but do not dispatch;
- known residual risks (Gaussian fill-in may still yield honest UNKNOWN);
- the statement that v3 does not alter the mathematical scope and does not
  establish global B4-B by itself.

Use final token:

```text
B345_RELFRAT3_PACKED_V3_READY_FOR_GHA
```
