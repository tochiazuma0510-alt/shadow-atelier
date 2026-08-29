# Task373 — A4/v7 minimal allocation and publication repair

## 0. Static closure and verdict

The bounded v5 repair is **source-statically complete**.  It repairs only the
three task371 rejection groups and preserves the frozen rows-1--7 route.  This
is not an execution verdict: I did not run syntax, imports, either candidate,
Python, Node, GAP, mutations, RSS, GHA, workflows, git, or network.  The first
permitted execution remains blocked on another independent Sol(max) reaudit.

The four task373 outputs are the only files created for this repair.  The v5
fixture pins task198 authority only; it contains no v5-program or task373-reply
identity, so the fixture/seal DAG remains acyclic.

## 1. Exact v5 identities

| machine owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v5.py` | 101,139 | `2d0be0e2875404cf25fbaa020d501a7e250c977e9fa9c946362363544540dde9` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v5.py` | 99,782 | `33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json` | 8,489 | `474d8e19ca49cad06b560cf0ac1d5eeeac1927fe2666224cb9501e77b5cc8481` |

Removing the root fixture seal field from the canonical object gives 8,400
bytes and SHA-256
`c674491a2f50b200a70349780f0e7a80c21cc0fc3cecd44432dc6e70c51f63fb`.
That is the fixture's `self_digest_sha256` and is pinned by both owners
(producer 32--34; checker 29--31).  The fixture contract and immutable task198
receipt/manifest identities are checked at producer 663--671 and checker
504--511.

## 2. Preserved finite route

The fixture still says exactly `covered_rows=[1,2,3,4,5,6,7]`,
`remaining_rows=[8,...,48]`, `candidate_only=true`,
`full_a4_selftest=false`, and `actual_a4_numerator=false` (fixture line 1;
producer 667, 888; checker 508, 700).  The producer/checker coordinate-owner,
eleven-occurrence, canary, task198 manifest, and generation literal blocks are
unchanged from v4.  In particular, the independent checker literal retains row
11 with `context_id=28` (producer 68--91; checker 40--63), and both complete
16,464-character ABI canary literals are deferred until after the process cap.

Static control flow preserves the ordinary baseline and a fresh ordinary route
for every mutation (producer 650--655, 720--742, 835--858; checker 497--503,
549--571, 655--675).  The seven registered first rejections remain:

| row | mutation | producer / checker first validator | stage and narrow reason |
|---:|---|---|---|
| 1 | per-layer ordinal | `*.authority.row_order` | authority / `*:authority:layer_ordinal` |
| 2 | authority binding | `*.authority.manifest_acceptance` | authority / `*:authority:manifest_acceptance` |
| 3 | canonical input bytes | `*.transport.receipt_identity` | transport / `*:transport:receipt_sha256` |
| 4 | resolved path traversal | `*.transport.path_containment` | transport / `*:path:registered_containment` |
| 5 | normal-generation proof | `*.authority.normal_generation` | authority / `*:authority:normal_generation_proof` |
| 6 | bridge occurrence ledger | `*.authority.bridge_occurrence` | authority / `*:authority:bridge_occurrence_ledger` |
| 7 | evaluator ABI canary | `*.authority.evaluator_abi` | authority / `*:authority:evaluator_abi_canary` |

Here `*` is independently `producer` or `checker`, exactly as recorded in the
fixture.  Only the narrow `TraceReject`/`NarrowRejection` is caught;
`MutationAccepted`/`CheckerMutationAccepted` stays outside it (producer
841--858; checker 660--675).  Retained descriptors, fourteen before/after
revalidations, concrete case-file parents, row-4 path identity, traceback
clearing, cache eviction, and cleanup remain at producer 369--451, 745--823,
835--883 and checker 242--316, 573--650, 655--695.

The checker imports only standard-library modules and imports no producer
helper or evidence (checker 7--19).  Its owner, scanner, validators,
constructors, and case route are separately implemented at checker 242--700.

## 3. F1 — exact modeled tokens versus the process cap

Let

```
S =    315,289  six task198 source pins
F =      8,489  v5 fixture
R = 31,017,244  task198 receipt
M =      2,722  task198 manifest
```

The frozen cumulative resource arithmetic recomputes to:

```
authority raw payload S+F+R+M                         =  31,343,744
opened and physically owner-hashed bytes              = 186,443,583
temporary case bytes / case-stage readback bytes      = 155,099,839
ordinary parsed input F+5R+8M+9                       = 155,116,494
four fresh sequential receipt parses 4R               = 124,068,976
total parsed input                                    = 279,185,470
retained-fd revalidation 14(S+F+R+M)                  = 438,812,416
logical opens / writes / events / mutations           = 53 / 10 / 66 / 7
```

These formulas are shared only as literal contract values, not helper code
(producer 102--112, 663--670, 886--888; checker 68--78, 509--510,
698--700).  Opens are explicitly logical owner opens plus retained-fd passes;
they do not purport to count component-directory OS opens (producer 238--240;
checker 141).

The exact modeled-token lifetime is:

1. Each authenticated file read reserves an I/O request token before
   `os.read`, acquires the exact retained cache-byte token before extending
   the bytearray, then releases the I/O token.  The `cache:*` tokens for the
   nine authority owners remain through the seven revalidations and total
   `S+F+R+M=31,343,744`; workspace cache tokens are released at case eviction,
   and the authority tokens are released by final owner close (producer
   372--451; checker 245--316).
2. Every canonical piece is emitted incrementally.  Before slice/ASCII
   encoding, a `fragment:*` token reserves both bounded live representations,
   at most `2*65,536=131,072` tokens, and is released when its sink returns.
   A constructor acquires its output owner's exact bytes fragment by fragment
   before `bytearray.extend`; no complete canonical `str` plus complete
   canonical `bytes` pair exists (producer 246--295; checker 147--196).
3. A semantic mutation uses one fresh sequential parse of the retained
   baseline receipt.  The parsed DOM is deliberately unmeasured object state.
   Its sealed receipt bytearray retains `R` tokens, or `R+8` for row 6, until
   the physical case has been written and its manifest binding copied.  The
   small manifest owner is handled identically.  All `case:*` constructor
   tokens are released before the ordinary validator reopens the case
   (producer 675--742; checker 513--571).
4. The row-3 wire bytearray reserves `R` before allocation and releases it
   after the case write.  Every case-stage or retained-fd read reserves at most
   `1,048,576` I/O tokens before allocation and releases them after the hash
   consumer (producer 706--711, 745--823; checker 537--542, 573--650).
5. The baseline full receipt DOM is released before the first mutation; only
   the small expected bridge/ABI subowners and the load-bearing raw receipt
   remain.  The raw receipt is needed by rows 1, 3, 5, 6, and 7 and is released
   at final owner close (producer 866--890; checker 679--702).
6. Result sealing has no full canonical buffer, and canonical stdout retains
   only one bounded fragment at a time.  Those tokens are released after each
   write and cannot exceed the earlier peak (producer 910--941; checker
   722--749).

The deterministically largest token state is the row-6 constructed receipt
while its first case-stage readback slot is reserved:

```
(S+F+R+M) + (R+8) + 1,048,576 = 63,409,572 modeled_payload_tokens.
```

Both implementations assert that exact peak, an end-of-seven-row live value
of `31,343,744`, no reserved ledger residue, and every exact cumulative count
(producer 887; checker 699).  The old `532,017,754` value and the names
`peak_live_bytes`/`live_peak_bytes` are absent.  Public wording calls these
ledger tokens and explicitly omits parsed DOMs, decoder/interpreter/container/
allocator overhead, bytearray capacity slack, and RSS (producer 185--242;
checker 107--143).

Separately, each owner supports only Linux `RLIMIT_AS`, chooses the minimum of
700,000,000 and any pre-existing finite soft/hard limits, rejects a nonpositive
or `>=750,000,000` target, installs it, and requires exact readback before use
(producer 892--908; checker 704--720).  `--output` is rejected first; otherwise
the cap is installed at producer 931 and checker 739, before the deferred ABI
parse and before the first fixture/authority read at producer 933--938 and
checker 741--746.  A finite address-space limit is not an RSS observation:
both public ledgers say `rss_observed=false`.  Runtime RSS remains unobserved.

## 4. F2 — remaining traversals and why they remain

The receipt acceptance pass is fused: one streamed canonical traversal both
compares every physical byte, hashes the seal-minus-field body, and feeds the
rows whole/chunk digests (producer 466--551; checker 347--421).  The following
row schema/type loop performs no canonical serialization and remains separate
so the transport seal finishes before the authority row validator is entered,
preserving the registered first-rejection order (producer 565--590; checker
429--458).  Thus the former second 30.5-MB row canonical materialization is
gone.

The complete traversal ledger distinguishes:

- authenticated/case-owner physical hashing plus retained-fd hashing;
- case-stage readback hashing and the one row-3 wire-source hash;
- full canonical comparison, seal-body hashing, and whole/chunk row digest
  feeds in the fused acceptance scan;
- constructor body-digest streams and constructor final canonical streams;
- small fixture/bridge/coordinate/event/result digest streams; and
- canonical stdout.

The dedicated counters are declared at producer 185--198 and checker
107--120, and are charged at producer 274--295, 397, 424--436, 520--540,
767--785, 916--925 and checker 175--196, 268, 294--304, 393--410,
593--612, 725--733.  Source-static exact physical totals are
`186,443,583` owner-read bytes, `438,812,416` retained-fd bytes,
`155,099,839` case-stage readback bytes, and `31,017,244` row-3 wire-source
bytes.  Canonical-purpose counters are runtime-exact but remain unexecuted.

Each local sealed receipt constructor necessarily has two streamed passes:
the body must first produce the self seal, then the final object containing
that seal produces the immutable `(byte_length, raw_sha256, self_seal)` tuple.
There is only one final bytearray.  `copy_manifest` copies that tuple directly
and never rehashes the local 31-MB receipt (producer 675--698; checker
513--533).  The independent ordinary route later reopens and hashes the
physical owner, which is the required independent comparison.  Four fresh
sequential parses replace full-receipt `deepcopy`; no `copy` module,
`deepcopy`, or full `json.dumps(...).encode(...)` route remains.

## 5. F3 — result publisher removed

There is no result-output stage, result link, final result pathname, output
seal helper, or filesystem publication helper in either v5 owner.  Both parsers
retain `--output` only to reject any supplied value immediately, before the
address cap, fixture validation, authority access, or any path creation/open
(producer 927--938; checker 735--746).  The only machine-result emission is an
in-memory self-sealed object streamed canonically to stdout (producer
910--925; checker 722--733).

The fd-relative `write_case` staging/link logic at producer 745--823 and
checker 573--650 is not a result publisher: it is confined to invocation-unique
temporary workspaces and remains load-bearing for the seven concrete physical
mutation owners.  No caller can route `--output` into it.

## 6. Remaining limitations

This is candidate-only source code.  No syntax/import check, runtime mutation,
address-cap observation, RSS measurement, producer/checker comparison, GHA,
or workflow ran.  The process cap does not measure Python object size or RSS.
Rows 8--48, the full 48x2 selftest, lift, fake, Ihara, and a full actual-A4
numerator are untouched.  Another independent Sol(max) source reaudit is
mandatory before execution.

TASK371 MODELED/ACTUAL MEMORY CONFUSION: REPAIRED
TASK371 DUPLICATE MATERIAL WORK:         REPAIRED
TASK371 OPTIONAL PUBLISHER:              REMOVED
ROWS 1--7 PRODUCER/CHECKER ROUTE:        IMPLEMENTED
PROCESS ADDRESS-SPACE CAP:               IMPLEMENTED
RUNTIME RSS / MUTATIONS / GHA:           UNEXECUTED
FULL 48x2 SELFTEST:                      INCOMPLETE
INDEPENDENT SOL(MAX) REAUDIT REQUIRED:   YES
ACTUAL A4:                               remains 1/3
LIFT / FAKE / IHARA:                     NONE

TASK373_R07_A4_V7_MINIMAL_ALLOCATION_REPAIR
