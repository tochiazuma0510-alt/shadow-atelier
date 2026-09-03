# Sol(max) Task646: finite release re-audit of repaired Task640 v3

## Verdict

`FAIL`

`SAFE_TO_DISPATCH_GHA=no`

The frozen quartet is byte-exact, and repairs R1, R3, R4, R5, and R7 are
present.  R2/R6 still contain an honest-producer/checker type contradiction,
R6 does not require the exact receipt filenames, and R8 remains a collection
of mostly synthetic comparisons rather than the mandated live-predicate
mutation suite.  These are finite release blockers.  No production run, GHA
dispatch, implementation edit, or git operation was performed.

`verified=false`

## Frozen-input authentication

No `INPUT_MISMATCH` occurred.

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,227 | 299 | `d8957511167f3ace568f59fd2d50dfcdbd7a16fc50bd4475077fcd73dbc3a5b9` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 85,627 | 1,490 | `3b8b335da4a2233977464fc553e040a3a0f0c79d5bf58451255d8370e63e88af` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `0f8df3e4bfd22024ffd0f3c5841717441dc03dedb8834cec9fe46a460634826f` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,833 | 53 | `508c28e322dae868f2dd7043a3ed4a01c4110fffb8fbe4154b4d25c29577896f` |

The complete Task646 mail is 4,277 bytes / 75 lines / SHA-256
`0850a7fe497c217546346be7b724f3fc64b67e52d36c63499c93fb6d91f40337`.
I also read the complete Task644 reply (10,395 bytes, SHA-256
`50f8365835282ab0f79c33c4a392e930b4ea4e0cc0a49923a5bad5c3eb3c467e`)
and Task645 instruction (6,827 bytes, SHA-256
`2f8de1df35ba4ecb70338e09761770010020eac2018dd7a8d3ea56f93df94f2d`),
as well as the required Task640/643 and pinned paper/audit context.

## R1--R8

### R1 — PASS

Workflow lines 112--118 download the real immutable Task595 artifact
`task595-grade1-decision-v2-candidate-33707397894-1` from run
`33707397894`.  The former nonexistent `decision-v3-candidate` name is gone.

### R2 — FAIL

The live envelope portion is repaired: workflow lines 84--89 require the
Task625 attempt, head, success, workflow name, exact job id/name/success, and
lines 90--96 require artifact id, name, size, digest, non-expiry, workflow-run
id and head.  Lines 97--103 retain the exact run/name download.

The sealed parent object is nevertheless inconsistent across the two
executables.  Producer constants at lines 19 and 22--23 are strings, and
producer line 272 therefore emits these four JSON strings:

- `task601_run: "33734643746"`;
- `task601_attempt: "1"`;
- `source_run: "33677346616"`;
- `candidate_run: "33707397894"`.

Checker line 387 independently writes all four as JSON integers and line 388
requires exact dictionary equality.  Hence every honest payload emitted by
the frozen producer fails `consumer_parent_binding`; the workflow cannot
reach its checker PASS marker.  The smallest repair is to use one canonical
type for these four fields on both sides (quoting the four checker literals is
consistent with the producer constants and workflow identifiers).

### R3 — PASS

Producer lines 217--218 and checker lines 402--404 construct ordered raw
`prior + leaves`, derive the reached-seed set before cancellation, and only
then form the canonical nonzero exact-key map.  Producer lines 230--234 and
checker lines 409--414 gate every raw reached seed.  Producer lines 235--237
and checker lines 434--436 run the independent all-seven direct canary for
every surviving exact key before bucket construction at lines 238 and 437,
respectively.  Exact zero cancellation therefore cannot hide a source seed,
while cancelled keys are correctly absent from evaluation.

### R4 — PASS

Checker lines 437--442 independently rebuild and byte-compare its nonzero
signature buckets.  Lines 444--445 form replay terms from those checker-owned
buckets, including the coefficient and retained representative path, and
pass only that set to dense replay.  The separate exact-key canary remains at
lines 434--436.  Producer dense replay is likewise bucket-only at lines
246--249.

### R5 — PASS

The checker contains local word/substitution, Artin/PB presentation,
permutation, PC-collection, E3/E4 quotient, Fox/translation and word
operations at lines 36--178.  `SevenSources.authenticate` at lines 179--190
only byte/hash-authenticates pinned inputs; of those six inputs, only the
pinned q3 JSON is parsed (the pinned words JSON is read separately).
`build_checker_light` at lines 1198--1218 and
`IndependentAllSeven` at lines 1250--1430 locally construct the typed eleven
contexts, prefixes, coordinates, hexagon/pentagon paths, occurrence column,
and direct-versus-occurrence equality.  The checker has no dynamic `exec`,
`.load`, `exec_module`, `ModuleType`, or live import of the producer-shared
semantic modules.  Producer-side pinned v12f loading at producer lines 87--96
is within the stated allowance.

As an additional bounded serial smoke, local endpoint construction produced
11 contexts with E3/E4 degrees 36/144, all real 44-by-11 seed endpoint gates
passed, and one local direct-versus-occurrence canary passed with equal sparse
support 1,383.  This was not a dense or production run.

### R6 — FAIL

Most manifest equalities are now live: canonical schema/claims at checker
lines 384--385, roots and recomputed artifact bytes at lines 398 and
433--451, exact rho2 metadata at lines 452--453, the exact allowed top-level
key set at lines 454--455, roots/digests and occurrence at lines 456--458,
`L/U/G/cache` at lines 459--460, dimensions at line 461, and the positive
degree-one/coefficient/lower gates at line 462.  The parent type contradiction
described under R2, however, makes the advertised full parent equality reject
the producer itself.

There is also one independent exact-receipt hole.  Lines 390--397 require the
seven receipt keys and check each producer-supplied `file/bytes/sha256` object
against the file it names.  Subsequent lines compare every resulting blob to
the independently recomputed bytes, so byte counts, digests, and semantics
are covered.  But line 395 follows the manifest-provided filename, and no
line compares any `file` value with the producer's seven canonical filenames.
For example, renaming `rho2.bin` to `renamed.bin` while changing only
`files.rho2_packed.file` leaves exact bytes and hashes unchanged and is
accepted.  That is receipt self-consistency, not the required complete
receipt equality.  The smallest repair is an exact key-to-filename map and
equality of each complete receipt with
`{file: fixed_name, bytes: len(recomputed), sha256: sha(recomputed)}`.

### R7 — PASS

Producer lines 157--166 and checker lines 305--314 stream-hash every parent
receipt in 1 MiB chunks and retain bytes only for the 255,846-byte roots and
565,981-byte leaf stream.  The 149,359,882-byte ancestry receipt is not
DOM-loaded on either live path.  Its frozen digest is required by the leaf
header at producer lines 101--105 and checker lines 248--252, then sealed and
checked in the child manifest.

Both live leaf parsers enforce record and path-length caps (producer
105/110; checker 252/257).  Unique complete paths, trie prefixes, and combined
evaluation/signature state are tied to live counters at producer lines
219/226/243 and checker lines 416/420/443.  Exhaustion has the
`UNKNOWN_RESOURCE:*` prefix.  Task639's exact parent values (19,393 leaf
records, 2,622 prior terms, 2,565 interned paths, maximum path length 24) are
far below those bounds.

Static memory has no remaining concrete production-sized blocker: ancestry
uses one streaming buffer; roots and leaves total under 1 MiB; the candidate
basis is a transient 30.5 MB read; the checker source-pin byte snapshots total
about 1.34 MB; the declared 44-seed cache is 10,644,832 bytes; and dense
target/replay/difference arrays are serial at widths 8,064/24,192/48,384.
Path/signature/bucket objects are bounded by the live caps.  This is well
inside the workflow's 7 GiB internal and 8 GiB address-space limits.  The
unused graph-replay functions do not execute or load ancestry on the live
route.

### R8 — FAIL

Task645's required live-predicate fixture repair was not made.  Checker
`fixture_rejects` at lines 362--380 does not call production
`validate_payload` (lines 381--463), `build_checker_light`,
`IndependentAllSeven.direct_column`, the production trie recurrence, or the
dense/packing comparisons.  Its endpoint and occurrence helpers are also not
the inline production gates.  Several cases merely compare unequal toy
values and invoke `fail(...)` themselves.  The 20 cases consist of one toy
endpoint, one row rotation, two canonical-term comparisons, 13 standalone
claim-dictionary changes, two unequal byte strings, and one unequal hash.
Checker selftest lines 470--475 add only three live leaf-parser failures, for
the reported `mutation_count=23`.  Producer selftest lines 277--288 similarly
has four leaf-parser mutations plus tuple arithmetic.

Thus mutations of slot 1 versus 5, E3/E4 typing, sign/inverse/PP/block/prefix
and right-multiplication order, nonidentity block product, premature merge,
failed raw seed gate, missing/swapped roots, ancestry binding, the live parent
envelope, manifest receipt fields, and target/lower/top/packing values are not
routed through the validators that production executes.  Even the false/null
claim cases use standalone `claim_gate`, not `validate_payload`'s live claim
gate.  A production right-to-left trie multiplication regression, for
example, leaves both frozen selftests green.

The smallest repair remains Task645 R8 as written: factor only the bounded
validators already required by production and send tiny mutations through
those same call sites.  No real graph, ancestry, dense row, or other large
fixture is needed.

## Bounded serial checks

- External-cache `py_compile` of both executables: `PASS`.
- Producer `--selftest`: exit 0, `leaf_live_mutations=4`.
- Checker `--selftest`: exit 0, `mutation_count=23`.
- PyYAML safe parse: `PASS`.
- Immutable action scan: `PASS`, seven `uses:` entries, each pinned to a full
  40-hex commit SHA.
- Forbidden shared execution/import scan: `PASS`.
- Frozen-quartet whitespace/final-LF scan: `PASS`.
- Workflow lines 39--42 still contain the inert `false &&` guard: `PASS`.

The green selftests are not evidence that R8 is closed; their own code shows
that the required mutations never reach the live validators.

## Claim boundary

This audit establishes no rho2 value, grade2 MEMBER/NONMEMBER result, A0,
order 54,432/full-Q0, COMMON word, cofinal lift, FAKE, IHARA, cross-check, or
Lean verification.  A future PASS would authorize only the single fresh-rho2
GHA consumer feeding v474.  The present quartet is not authorized for
dispatch.
