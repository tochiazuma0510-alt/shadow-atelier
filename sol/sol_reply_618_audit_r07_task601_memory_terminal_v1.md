# Sol(max) reply Task618: Task601 memory terminal

## Verdict

`PASS_REPAIR_SPEC`

Run `33717064826`, attempt 1, job `100528381356`, at head
`69e95d7fc50f04691a41417c495e27f7064f470d`, is an operational
`UNKNOWN_RESOURCE` result only.  It is not a negative mathematical result and
does not alter the Task595 MEMBER decision.  The producer terminated with
`MemoryError` after 421 seconds; no payload and no checker result exist for
this run.

The failure is sufficiently localized to the Task601 materialization/lifetime
design to specify a bounded repair.  The exact allocation that raised was not
recorded, so it would be too strong to name one unique object as the cause.
That uncertainty does not require `FAIL_UNLOCALIZED`: the current program has
several simultaneous, removable, high-multiplicity representations, and the
failure time is after the known roughly 396.5-second all-8,059 route and at the
entry to the unbounded derived-state construction/serialization region.

## Audited bindings

| input | bytes / lines | SHA-256 |
|---|---:|---|
| Task618 instruction | 2,584 / 51 | `63a421d14d7145c60c360bf43f19fc0de0dc83ddc9708f78f32d6170a7901f46` |
| Task601 producer | 25,722 / 234 | `4cc5d6ccb1bfdcb441b801a4826af04bbbdc9dc7f21d6f7c860d05929e64bfe9` |
| Task601 checker | 54,060 / 589 | `8355fda531b9de41b37df811af932352f07546d6d0ec445764fedaced2595595` |
| Task601 workflow | 5,497 / 111 | `3ddd2f53fb10d698713e2a44a27cd894f4a02120727bb58db65beef9ac4a6fbd` |
| v468 | 12,016 / 284 | `b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6` |
| v469 | 8,865 / 234 | `bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6` |
| v470 | 8,731 / 225 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |
| v471 | 8,819 / 220 | `38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f` |
| Task614 audit reply | 13,159 / 230 | `4ab26ef61db6577d98c9d8ed37c1d7da2e4b6d90b59dc9836f7a26120c981720` |
| Task616 audit reply | 6,749 / 123 | `da9ee1e61ab30a216d7c30e31e9e6cba459d3beefa3cdfec83cb25d448e5da52` |

The immutable `producer.log` is 279 bytes with SHA-256
`912596f139e40502a9e9fdd00717c914158fe552530c51df718aee436dca1897`.
It contains only the outer traceback at producer line 234 and `MemoryError`;
there is no inner phase or allocation trace.  All preflight and parent
downloads passed, and the main step ran from `2026-09-03T05:00:02Z` through
`05:07:03Z`.

## Five adjudications

### 1. Derived states and exact leaves

The full `derived.states` array is optional and shall be removed.  V468
section 5 makes the adjoint state table quotient-specific, permits it to be
discarded and recomputed, and expressly forbids it from replacing the
canonical source graph.  V469 likewise says derived flow and the coalesced
leaf map are not evidence for the physical/canonical obligations.  The
present producer nevertheless retains every expanded state, its copied
children, source references and path, then canonical-JSON serializes all of
it.  Its cap is a count of seven million Python objects, not a byte bound.
That is not required evidence and is the clearest unbounded post-route peak.

There is one important distinction: remove `derived.states`, but do **not**
silently remove the exact-path leaf receipt in this minimal repair.  Although
the leaf map is not authority and could mathematically be recomputed from the
canonical graph, v471 section 4 item 2 currently requires the consumer to
compare its independently recomputed exact-path table with an exported
derived table.  Removing that table would therefore be a proof/consumer
contract change, not the smallest Task601 memory repair.

Retain the semantic `literal_leaves` result as a separate compact, canonical,
sorted receipt of `(seed, freely-reduced signed-letter path, coefficient)`.
Compute it with only the live coalescing `pending` map and final leaf map:
pop a state, expand it, and discard it immediately.  Do not accumulate a
state history or child dictionaries.  A length-prefixed binary record stream
(seed, coefficient, path length, signed `int8` letters) is sufficient.  Its
receipt must bind the canonical ancestry/graph digest and carry
`quotient_specific_evaluation=true` and `common_source_witness=false`.
Task601's checker, and later the v471 consumer, must independently run the
adjoint recurrence from the authenticated canonical graph/physical
recurrences and compare the complete sorted compact stream byte-for-byte.
Thus the export remains only a comparison receipt, never its own authority.

### 2. Physical transcript representations

Yes.  Preserve every physical row and ordered edge, but hold each transcript
in one compact representation.  Edge append should write the existing
`<HB` record directly to a `bytearray`; origin, stored, companion and
old-lower-zero rows should likewise append into their final packed streams.
Do not retain lists of millions of Python `(pivot, coefficient)` tuples or
lists of separate row `bytes` and then make a second copy with `edge_bytes`
or `b''.join`.

The small fixed node records may remain mutable through the MEMBER check and
reverse **physical** least-closure pass.  Then pack them once.  Subsequent
closure/adjoint access must use fixed-width `memoryview`/`struct.unpack_from`
accessors over the packed node and edge streams.  Release the Python node
records, `source_refs` entries not in the selected origin set, route
temporaries and owner objects before constructing the canonical source
closure.  In particular, `lower_comp` is needed while routing the old rows
but not after that phase and must be released there.  None of this changes
the 8,059 offers, ordered reductions, 1,661/5,044 ranks, 3,317 MEMBER
coefficients, origin/companion/lower-zero receipts, or least selected set.

### 3. Block and owner lifetimes

The producer currently parses and retains all four full block JSON bodies at
once.  Their measured raw JSON size is 301,032,552 bytes in total, before the
much larger Python-object expansion.  During routing it has one `owner`
matrix variable at a time, not four simultaneous producer owners; the last
one nevertheless remains live unless explicitly released.

Consume blocks by character.  In the routing pass, authenticate one block,
load its owner, route all of its pivots, retain only compact logical/source
descriptors, then release the owner and body before the next character.  Once
the selected origin set is known, a second authenticated character-wise pass
may collect the selected canonical DAG material for that character.  This is
at most one reload per block/pass, never one reload per selected origin.
Release each body immediately after its selected nodes have been copied into
the canonical least graph.

The checker also retains four parsed block bodies while doing other large
work.  Its selected-source replay can create a per-character owner cache that
eventually holds all four owners, while the independent router separately
loads its own source bodies/matrices.  Run the sealed selected physical/source
replay first, grouped by character with exactly one body and one owner live,
then free those bodies, owners and prepare material not needed later.  Only
after that begin the standalone all-8,059 independent reroute.  The latter's
already established source representation may be used because it no longer
overlaps a second checker-side set; any checker-added block cache must not
survive into it.

### 4. Checker duplication and exact replacement

`loaded['grade_edges']` and `loaded['lower_edges']` are the authenticated raw
streams; the local `ge`/`le` variables merely alias them.  The large extra
copies are `gedges`/`ledges`, which decode every three-byte entry into Python
tuples, the temporary `gedges+ledges`, and the independent reroute's
`expected_ge`/`expected_le` tuple lists.  The expected row lists and their
final `b''.join` add analogous peaks.  The ancestry JSON is also parsed once
inside `validate_source_ancestry` and again for `structure`.

Replace this exactly as follows.

1. Authenticate each receipt once and retain its raw bytes or a
   `memoryview`.  Define edge count as `len(raw)//3` and decode one edge with
   `struct.unpack_from('<HB', raw, 3*i)`.  Validate coefficients, intervals,
   acyclicity and reverse closure through indexed iterators; never construct
   `gedges`, `ledges`, or their concatenation.
2. Expose node records as a zero-copy fixed-width structured view, or unpack
   one fixed record at an index.  This preserves original identifiers and
   all interval/order checks.
3. During the independent reroute, compare each accepted node immediately
   with the candidate node at its node cursor.  Compare every ordered
   reduction directly with the candidate edge at its edge cursor and advance
   it.  Compare each packed origin/stored/companion/lower-zero row directly
   with the corresponding raw slice.  At termination require that every node,
   edge and row cursor exactly consumed its authenticated stream.  A compact
   expected `bytearray` followed by one byte comparison is also sound, but
   online cursor comparison has the smaller peak.  No Python expected tuple
   or row list and no final join is permitted.
4. Preserve the independently materialized final routed basis and compare it
   with the candidate basis and pinned SHA exactly as before.
5. Parse canonical ancestry exactly once, validate it, pass that same object
   to closure/leaf checking, then release its raw JSON when no longer needed.
   It contains roots and the full least canonical structure, but no
   `derived.states`; the compact leaf table is its separately authenticated
   child receipt.

This remains a complete independent reroute and complete transcript
comparison.  It is not sampling or a partial graph.

### 5. Minimum diagnostics

Add one small phase reporter, not a new discovery framework.  Each record
needs monotonic elapsed seconds, current RSS (for Linux, `/proc/self/statm`),
peak RSS (`ru_maxrss`), and only the relevant cursors/counts.

Producer checkpoints are: prepare/old complete; each block routed and
released; route/MEMBER/physical closure complete; packed physical
temporaries released; periodically during streaming adjoint (for example
every 65,536 expansions: processed, pending, leaves, maximum path length);
canonical graph/leaf receipt sealed; payload sealed.  Checker checkpoints
are: receipts and single ancestry parse complete; each character's selected
source replay and release; immediately before the independent router; each
old-character/block boundary in the independent reroute with node/edge/row
cursors; basis/MEMBER complete; verdict sealed.  Per-row logging is neither
needed nor desirable.

Reserve a small emergency buffer at process start.  On `MemoryError`, release
it and issue one fixed-size ASCII diagnostic with `os.write(2, ...)` carrying
the last phase, RSS and cursors, then return nonzero as `UNKNOWN_RESOURCE`.
Do not allocate JSON in the exhausted handler.  This is necessary because the
current outer `except Exception` could itself fail while formatting/printing,
which is consistent with the trace containing only the outer `main()` call.

## Bounded Luna patch and rerun gate

The minimal patch is therefore limited to:

- delete only the bulky `derived.states` export and keep the independently
  checked compact exact leaf receipt required by v471;
- make physical edges/rows and independent expected comparisons packed or
  zero-copy, releasing transient Python collections after their last use;
- separate all checker/producer block and owner lifetimes by character, with
  no per-selected-origin reload;
- parse ancestry once, order selected sealed replay before the independent
  full reroute, and add the phase/RSS/emergency diagnostics above; and
- update the existing tiny schema/stream fixtures for these representations.
  Do not add a broad selftest campaign or another routing implementation.

Before rerun, Luna must pass syntax compilation, the existing small fixtures,
workflow/YAML static inspection, and a fresh static audit of file pins and
receipt bindings.  The workflow must retain its current 60-minute job,
8-GiB virtual/7-GiB RSS envelope and its producer/checker timeouts; do not
raise the resource limit.  It must also retain all 8,059 rows, ranks
1,661/5,044, 3,317 coefficients, physical receipts, independent full reroute,
least canonical graph, three roots, and every false claim flag.

After that bounded patch and static gate, **one production rerun is
justified**.  Success would create a new candidate plus independent checker
receipt; it would still not be `cross_checked` until that checker succeeds,
and never `verified` absent Lean.  A second resource terminal must be reported
with the new phase/RSS/cursors and re-audited rather than weakened, partially
accepted, or relabelled as a mathematical negative.

No implementation, proof, v220, production, GHA, or git action was performed
in this audit.
