# Sol(max) reply 367 - A4/v6d complete finite repair

## 0. Static implementation verdict and frozen owners

The bounded v4 repair is source-statically complete.  Task366's six concrete
failure modes are repaired in the source: the checker baseline ledger, the two
case-writer target bindings, row-4 identity typing, retained-object lifetime,
avoidable full-size copies/open accounting, and the optional-output
transaction.  This is an implementation/freeze result, not the independent
reaudit requested below.

Only read-only PowerShell inspection and hashing were used.  Python, Node,
GAP, candidate code, syntax compilation, GHA/workflows, git, and network were
not run.  Consequently no statement below is a runtime, RSS, mutation-result,
fault-injection, or workflow result.

| frozen machine owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v4.py` | 102,525 | `4c32f9f9d80664c8f5ce962152f0f4f697d272f8ee77c102dda29b2b6578bde0` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v4.py` | 99,978 | `e0f27444aefffeb55f2d06637d0e1feb0f366239600262aeca9ce4e5c24c25c7` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v4_20260829.json` | 8,457 | `9bf92d19c8ebcabb8cb6a342508af60689e3c689979b065a7733052b499172b3` |

The fixture's canonical body self seal is
`f7d929846f069139bcfe148d07b072849b1f92d2dd9c782aa4a387b4d3467663`
(fixture line 30).  The fixture pins only the immutable task198 receipt and
manifest (line 15), not either v4 program, so its seal dependency graph remains
acyclic.

## 1. F1 - independent checker baseline and exact ABI

The checker-owned eleven-row literal is at checker lines 50--51.  Its row 11
has the exact twelve keys and `context_id=28`; there is no temporary `source`
field or key deletion.  Read-only literal/canonical inspection gives eleven
rows and ledger SHA-256
`040ab853535db8aad06fba295adf8b59bb1cd77435e7c64a1edcc34cdacb4cd7`,
which is the independently fixed constant at line 43.  The ordinary validator
requires the exact twelve-key set, recursive type-sensitive equality, integer
types, and the canonical ledger digest at lines 353--360.  Producer rows
68--78 and validation at lines 499--509 impose the same accepted contract.

The complete checker canary literal is checker line 78 and is checked field by
field and then recursively exactly at lines 363--377.  Producer lines
517--533 do the corresponding independent checks.  Static extraction of each
literal gives 16,464 canonical bytes and SHA-256
`6fb8df36710628faded5438e993a21416809e056b214c5a732aac05688fb66d0`.

The checker baseline ordinary call is outside all mutation catches at line
574; the seven-name loop follows at lines 579--589.  Thus the former literal
mismatch is absent and the untouched baseline control-flow edge leads to the
mutation loop on a clean supported-POSIX run if all physical reads and ordinary
checks return.  This is static reachability only; the baseline and loop were
not executed.

The checker imports only standard-library modules (lines 7--19), explicitly
imports no producer module, and owns its reads, codecs, validators, mutation
constructors, writers, and projections (lines 2--5).  No producer helper or
producer evidence is shared.

## 2. F2/F3 - concrete case targets, row-4 identity, and owners

Both case writers first require a concrete child regular-file target of the
per-case workspace, then call the parent opener on that target itself:
producer lines 661--668 and checker lines 472--479.  The resulting retained fd
therefore names the workspace and the returned leaf names the case file.  The
parent pathname is rewalked and matched to that fd, the leaf must initially be
absent, the stage file is opened exclusively/no-follow, written and hashed
through the same fd, hard-linked exclusively, unlinked from staging, fsynced,
and matched to the final pathname (producer 669--707; checker 480--517).
Failure removes final and staging names through the retained workspace fd,
fsyncs, asserts both absences, preserves cleanup errors, and closes both fds
(producer 708--734; checker 518--544).

Row 4 creates an invocation-unique external temporary parent and verifies its
receipt leaf is absent before use (producer 644--648; checker 456--460).  Its
plan is explicitly `identity_kind="path"`.  The baseline registered receipt
has a separately observed path identity (producer 783; checker 578); the
dynamic `before_key` selects that path identity rather than the receipt-file
identity, and both the before and actual rejection observation are required to
have the plan's same kind (producer 747--755; checker 550--557).  The outside
path observation is made by the containment gate before basename/open
processing (producer 391--400; checker 256--264).  Disposal deletes the unique
outside parent and derives absence of both parent and leaf from the actual
owner (producer 761--771; checker 563--571).  Hence the outside leaf's
before-use/after-disposal absence and v297's same registered identity type are
both explicit; no shared sibling is reused or removed.

Baseline authority handles remain retained and are rewound, length/SHA checked,
`fstat`/no-follow-path identity checked, and counted before and after every
case (producer 355--377, 767--790; checker 224--243, 567--585).  They close in
invocation-level cleanup.  `MutationAccepted` remains after, and therefore
outside, the narrow expected rejection catch (producer 750--769; checker
553--569).

## 3. Preserved semantic seal DAG and exact contracts

Receipt sealing rejects a foreign manifest seal, removes only the receipt seal,
seals the body, and returns the DOM/raw/raw-SHA/length/self-seal tuple; manifest
sealing independently rejects a receipt seal and rebuilds the manifest seal
(producer 574--587; checker 402--411).  The manifest receipt binding is derived
from that typed receipt tuple (producer 586--592; checker 410--414).  Rows
1/5/6/7 carry the five-node receipt-to-manifest DAG, row 2 carries only its
manifest DAG, and rows 3/4 carry no reseal (producer 636--657; checker
448--469).  No stale nested seal or cyclic fixture/program pin was introduced.

Exact presentation keys/types, layer-local ordinals, seven chunk seals, and
the fused 6,441-row order/digest walk remain in producer lines 448--489 and
checker lines 307--349.  Exact normal-generation, 11-entry bridge, coordinate
owner, and complete evaluator ABI checks remain at producer 495--533 and
checker 351--377.

## 4. F4/F5 - exact modeled lifetime, caps, and processing cost

Let

```text
S =    315,289   source pins
F =      8,457   fixture
R = 31,017,244   receipt
M =      2,722   manifest
```

The final formulas are source-identical on both sides (producer 89--99;
checker 56--66):

```text
opened bytes       = 186,443,551 <   250,000,000
temporary bytes    = 155,099,839 <   250,000,000
parsed bytes       = 155,116,462
DOM bytes          = 1,172,627,257 < 1,500,000,000
revalidated bytes  = 438,811,968 <   750,000,000
logical opens      = 19 + 20 + 14 = 53 < 256
writes/events/rows = 10 / 66 / 7
```

The largest receipt is row 6 (`bridge_typed_occurrence_ledger`), whose changed
string adds eight bytes.  The exact implemented peak reservation trace is

```text
B0 = 2S + 8F + 8M + 8R                         = 248,857,962
case physical cache = 2(R+8+M)                  =  62,039,948
case parsed owner   = 6(R+8+M)                  = 186,119,844
receipt seal/canonical allocation reservation   =  35,000,000
                                                   -----------
largest intended peak                            = 532,017,754
                                                   < 750,000,000
```

Canonical allocation is reserved before serialization, checked against its
bound, charged by exact resulting length, converted from the bound reservation
to an exact retained owner, and released after its consumer (producer
220--243; checker 126--147).  Exact parse comparison likewise uses the existing
raw buffer and releases its transient canonical owner (producer 403--420;
checker 266--283).  Receipt/manifest body canonical buffers are deleted and
released before final serialization (producer 574--583; checker 402--409), and
case clone/seal objects and their owner prefix are deleted before ordinary
validation (producer 636--650; checker 448--462).  Narrow rejection tracebacks
are cleared before case parsed owners are released (producer 752--754; checker
554--556); workspace caches are then evicted.  The final clean-route assertion
requires the exact counters, 438,811,968 revalidated bytes, no outstanding
reservation, baseline-only live owners, and the exact 532,017,754 peak
(producer 795--797; checker 590--592).

There is no `bytes(raw)` full-buffer conversion in either frozen source.
Hashing uses `memoryview(raw)` (producer 236--243; checker 140--147), case/output
writes use memoryview chunks, and canonical comparison uses the existing
buffer.  The 6,441 rows are typed, digested, and chunk-checked in one traversal
(producer 459--478; checker 318--337), without concatenating comma-plus-row
temporary buffers.  Each side has one physical cache, evicts every case cache
before the next row, and does not carry the 200-MB mutation clone into ordinary
validation.  The 14 retained-fd scans are the contract-required before/after
checks, not duplicate caches; their 438,811,968 bytes are explicitly counted.
The public counter label says these 53 are logical owner opens plus retained-fd
revalidation passes and excludes traversal-component OS opens (producer
210--213; checker 122--123), so it makes no false physical-open claim.

No superlinear processing was added.  Remaining repeated full scans are the
required canonical/seal checks, typed tuple consistency, and retained-fd
before/after revalidation.  Physical allocator overhead and observed RSS are
not established by this source meter and remain unexecuted.

## 5. F6 - optional publication transaction

For an output such as `ci/out/result.json`, both writers pass the final target,
not `target.parent`, to the no-follow helper (producer 804--816; checker
596--608).  Thus the retained parent fd is `ci/out` and the leaf is
`result.json`; its registered pathname is rewalked before publication and must
match the retained fd.

The transaction creates an exclusive stage directory relative to that parent,
opens and retains its directory fd, creates `staged.json` exclusively, writes,
fsyncs, rewinds, hashes, and validates through that same file fd, then
hard-links exclusively to the final leaf (producer 817--858; checker 609--650).
Success removes and proves absence of the staged file, fsyncs the stage
directory, checks exact final bytes/SHA/regular-file identity, removes and
proves absence of the stage directory, fsyncs the final parent, and rewalks its
identity (producer 854--864; checker 646--656).

Any exception after transaction creation first removes a published final leaf
through `parent_fd`, removes `staged.json` through the actual `stage_fd`, fsyncs
that stage namespace, closes fds, removes the stage directory through
`parent_fd`, fsyncs the final namespace, asserts final/stage absence, and
rewalks the parent before propagating a typed non-PASS.  Cleanup errors are
preserved as rollback failure (producer 865--914; checker 657--706).  A stale
pre-existing final is detected before transaction creation and is not removed.
The optional route adds three logical owner opens and one write after the
seven-row account snapshot; all remain under their caps.  This transaction was
not executed or fault-injected.

## 6. Scope and unresolved execution facts

The fixture records exactly `covered_rows=[1,2,3,4,5,6,7]` and
`remaining_rows=[8,...,48]`, with `candidate_only=true`,
`full_a4_selftest=false`, and `actual_a4_numerator=false` (fixture lines 2--3,
13--15, 25--30).  Both loaders require those exact values (producer 563--570;
checker 394--400), both mutation lists contain the same seven constructors
(producer 100; checker 67), and both result objects preserve the same scope
(producer 797; checker 592).

Static source inspection found no obvious syntax error, but neither file was
compiled.  Python syntax, runtime reachability, actual peak/RSS, resource
counter results, all seven producer results, all seven checker results,
optional-output success and rollback, and GHA are UNEXECUTED.  Windows and a
POSIX platform lacking the required no-follow directory-fd primitives stop
typed rather than weakening the owner model (producer 271--281, 917--926;
checker 157--166, 708--717).  Rows 8--48 remain uncovered; there is no full
48x2 selftest, no new A4 numerator, no lift, no fake result, and no Ihara
claim.  Independent Sol(max) reauditing of these frozen hashes is required.

TASK366 CHECKER BASELINE DEFECT:       REPAIRED
TASK366 CASE WRITER / ROW-4 IDENTITY:  REPAIRED
TASK366 RESOURCE / DUPLICATION DEFECT: REPAIRED
TASK366 OPTIONAL PUBLICATION DEFECT:   REPAIRED
ROWS 1--7 PRODUCER/CHECKER ROUTE:      IMPLEMENTED
EXECUTION / GHA:                       UNEXECUTED
FULL 48x2 SELFTEST:                    INCOMPLETE
INDEPENDENT SOL(MAX) REAUDIT REQUIRED: YES
ACTUAL A4:                             remains 1/3
LIFT / FAKE / IHARA:                   NONE

TASK367_R07_A4_V6D_COMPLETE_FINITE_REPAIR
