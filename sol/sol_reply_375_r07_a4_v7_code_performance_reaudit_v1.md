# Sol(max) reply 375 — independent A4/v7 code/performance reaudit v1

## 0. Boundary and decisive result

This was a source-static, read-only audit.  I used PowerShell inspection and
SHA-256 hashing only.  I did not run Python, Node, GAP, either candidate,
syntax/import compilation, mutations, RSS, GHA/workflows, git, or the network.

The frozen v5 tranche is **STATIC REJECT**.  The immutable authority graph,
checker route, token arithmetic, streaming design, Linux address-space guard,
and removal of the result publisher pass static inspection.  The producer,
however, calls the global name `admit_path` at line 651, while the complete
944-line v5 producer contains no definition or import of that name.  Its
definition inventory jumps from `PhysicalStore.close` (446--451) directly to
`parse_object` (453).  Thus the untouched producer baseline called at 867
cannot enter its ordinary manifest path validator.  All seven producer cases
are consequently unreachable.  This is a direct source-name/control-flow
finding, not a syntax-compiler or runtime experiment.

The failure is narrow but load-bearing.  It forbids even the first bounded
rows-1--7 candidate execution; it does not alter A4=1/3.

## 1. Frozen physical identities and seals

All four task375 subjects match exactly:

| frozen owner | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v5.py` | 101,139 | `2d0be0e2875404cf25fbaa020d501a7e250c977e9fa9c946362363544540dde9` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v5.py` | 99,782 | `33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json` | 8,489 | `474d8e19ca49cad06b560cf0ac1d5eeeac1927fe2666224cb9501e77b5cc8481` |
| `sol/sol_reply_373_r07_a4_v7_minimal_allocation_repair.md` | 12,791 | `3ab963655608df1ec5c962caef89f8e8d6474aa1d4ca87e732f7f68db46c10fb` |

The physical fixture has one trailing LF.  Removing the *root* 88-byte
`,"self_digest_sha256":"..."` member from its 8,488-byte canonical line
(not the nested task198 receipt member with the same final key name) gives
exactly 8,400 ASCII bytes and SHA-256
`c674491a2f50b200a70349780f0e7a80c21cc0fc3cecd44432dc6e70c51f63fb`.
That equals the root seal and the constants at producer 32--34 and checker
29--31.

The four frozen v6d outputs were also read and independently rehashed; they
match the task367 pins: producer 102,525 bytes / `4c32f9f9d80664c8f5ce962152f0f4f697d272f8ee77c102dda29b2b6578bde0`,
checker 99,978 / `e0f27444aefffeb55f2d06637d0e1feb0f366239600262aeca9ce4e5c24c25c7`,
fixture 8,457 / `9bf92d19c8ebcabb8cb6a342508af60689e3c689979b065a7733052b499172b3`,
and reply 13,295 / `bcc85c3612c4ddc60d943b33ddd2eedb98e0d17987d757696755ae414ee49f66`.

## 2. Acyclic fixture and task198 authority

The fixture's single physical line pins only the immutable task198 receipt and
manifest.  It contains no v5-program or task373-reply identity.  The programs
require those two identities at producer 668 and checker 510, and independently
pin the six owners below at producer 94--101 and checker 65--67.  The accepted
manifest's one-line body supplies the receipt binding, attestations/verdict,
and three task198 source identities; the exact fixed graph is also reconstructed
at producer 130--138 and checker 93.

| task198 owner | bytes | SHA-256 |
|---|---:|---|
| receipt `ci/in/d972_r07_seven_context_roof_presentation_v1.json` | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| acceptance manifest | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| task198 producer | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| task198 checker | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| historical task198 GHA driver | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |

The receipt seal-minus-field body is 31,017,156 bytes with SHA-256
`c8f7e65f6ec7553ab31928c911575de45fc0e3d70cd6e1d678bbebfee7502b9f`;
the manifest body is 2,625 bytes with SHA-256
`0f630669a906c93a3b7d40bd36633213316ff8da1b46ca254a552b3636963684`.
No edge points back to the v5 fixture or either v5 program, so the dependency
graph is acyclic.  The task198 driver in this table is an immutable authority
input, not a v7 execution driver.

The literals themselves retain row 11 with exactly twelve keys and
`context_id=28` (producer 80--91; checker 62--64).  Exact ledger/type checks
are at producer 597--607 and checker 462--470.  The complete coordinate widths,
encoding, six entry points, semantics, eight canary keys, typed ten-coordinate
values, source/action/cocycle shapes, and recursive equality are checked at
producer 121, 125--128, 615--632 and checker 83, 87--90, 472--488.  These
contracts are intact as literals; the producer cannot reach them because of
the earlier missing admission function.

## 3. Ordinary routes and the load-bearing producer defect

### F1 — producer route: REJECT

The producer call chain is `main` 927--940 -> `execute` 866--890 -> baseline
`ordinary_route` at 867.  `ordinary_route` begins at 650, and its first
load-bearing expression at 651 calls `admit_path`.  An exhaustive exact-token
scan finds only that call and no definition/assignment/import.  In contrast,
the frozen v4 producer owned the required function at v4 lines 391--400.  The
v5 refactor removed it between `PhysicalStore.close` and `parse_object` while
leaving the call in place.

Accordingly, after fixture loading and the six source-pin reads, direct v5
execution would fail closed on unresolved global lookup before the ordinary
manifest/receipt baseline.  It cannot retain the complete nine-fd baseline,
reach the mutation loop, or prove any producer first-rejection result.  The
fixture table cannot substitute for an executed ordinary validator.

### F2 — checker route: PASS source-statically

The checker owns its admission routine at 318--326 and calls it through its
ordinary validator at 497--501.  It imports only standard-library modules
(7--19) and no producer helper or evidence.  Its baseline is called at 680;
the nine retained authority identities are assembled at 682--686; and the
seven cases run at 687--697.  `NarrowRejection` alone is caught and checked at
660--674, while `CheckerMutationAccepted` is raised outside that catch at 675.
Wrong validator/stage/reason/owner/reseal data becomes `CheckerInputStop` at
664 rather than an accepted row.

The independently reconstructed intended/checker-first table is:

| row | physical owner mutation | exact ordinary first rejection |
|---:|---|---|
| 1 | `rows[0].ordinal: 1 -> 2`, receipt+manifest resealed | authority / `checker.authority.row_order` / `checker:authority:layer_ordinal` (437) |
| 2 | manifest `accepted: true -> false`, manifest resealed | authority / `checker.authority.manifest_acceptance` / `checker:authority:manifest_acceptance` (427) |
| 3 | final receipt byte flipped, no reseal | transport / `checker.transport.receipt_identity` / `checker:transport:receipt_sha256` (499--500) |
| 4 | invocation-unique absent receipt path outside both roots | transport / `checker.transport.path_containment` / `checker:path:registered_containment` (318--326) |
| 5 | normal-generation Cayley edge count incremented, full reseal | authority / `checker.authority.normal_generation` / `checker:authority:normal_generation_proof` (460--461) |
| 6 | occurrence row 1 block `H1 -> H1_mutated`, full reseal | authority / `checker.authority.bridge_occurrence` / `checker:authority:bridge_occurrence_ledger` (463--466) |
| 7 | evaluator coordinate width `40 -> 41`, full reseal | authority / `checker.authority.evaluator_abi` / `checker:authority:evaluator_abi_canary` (472--486) |

The producer contains corresponding constructors at 713--742 and validators
at 553--632, but their registered reasons are not producer results because
the common route at 651 is broken.

Both case writers otherwise bind the concrete case target, retain its actual
workspace parent fd, and perform fd-relative exclusive stage/link/readback/
cleanup operations (producer 745--823; checker 573--650).  Row 4 is explicitly
path-kind and invocation-unique (producer 728--732; checker 557--561); its
before owner is the registered baseline path identity (producer 874; checker
686), and same-kind/different-owner checks are at producer 836--845 and checker
656--664.  Expected cleanup and fourteen before/after revalidations are wired
at producer 850--883 and checker 669--697.  This case-owner design passes, but
does not cure the producer entry failure.

## 4. Independently recomputed token and cumulative ledgers

Let

```text
S = 81+95+150+137,169+157,253+20,541 =    315,289
F =                                              8,489
R =                                         31,017,244
M =                                              2,722
A = S+F+R+M                                = 31,343,744
```

From the actual source formulas (producer 102--112; checker 68--78):

```text
owner-read bytes
  = A + 3(R+M) + (R+8+M) + (M+1) + R
  = 186,443,583

case-stage readback / temporary bytes
  = 3(R+M) + (R+8+M) + (M+1) + R
  = 155,099,839

ordinary parsed input
  = F + 5R + 8M + 9
  = 155,116,494
four fresh sequential constructor parses
  = 4R = 124,068,976
total parsed input
  = 279,185,470

fourteen retained-fd revalidations
  = 14A = 438,812,416

largest modeled token state (row 6 stage readback)
  = A + (R+8) + 1,048,576
  = 63,409,572

end-of-seven-row authority payload
  = A = 31,343,744
```

The logical-open decomposition is 19 authenticated owner reads + 20
case-writer fd acquisitions + 14 retained-fd passes = 53; it expressly does
not claim to count component-directory OS opens (producer 238--239; checker
141).  Ten physical case writes and 66 events also reconstruct exactly.

The token lifetime is coherent conditional on restoring producer reachability:

1. Each authority/case read reserves a bounded I/O slot before `os.read`,
   charges exact cache bytes before `bytearray.extend`, releases the I/O slot,
   and retains authority caches through their last validator/stdout consumer
   (producer 372--451; checker 245--316).
2. Canonical fragments are cut to at most 65,536 ASCII characters; the source
   charges both bounded string/byte representations before slicing/encoding
   and releases them when the generator resumes (producer 246--263; checker
   147--164).  Constructed bytearrays acquire exact fragment-length tokens
   before extension (producer 285--295; checker 186--196).
3. Four semantic cases parse the baseline receipt sequentially, retain only
   one final receipt bytearray, pass its sealed `(length, SHA-256, self-seal)`
   directly into the manifest, and release all `case:*` payloads before the
   ordinary reopen (producer 675--742; checker 513--571).
4. Row 3 alone retains a second `R`-byte wire owner (producer 706--711;
   checker 537--542).  Each case readback adds at most 1,048,576 tokens and
   releases them immediately (producer 765--785; checker 592--612).
5. Narrow tracebacks are cleared before case cache/DOM disposal (producer
   841--850; checker 660--669).  The pre-result assertion requires the exact
   peak/end values and zero reservations at producer 886--888 and checker
   698--700.  Authority cache tokens finally fall to zero in `close` after
   stdout (producer 941--942; checker 749--750).

The public field is `modeled_payload_tokens`, never peak live bytes or RSS.
It explicitly excludes parsed DOMs, decoder/interpreter/container/allocator
overhead, bytearray capacity slack, and RSS (producer 223--239; checker
139--143).  Thus 63,409,572 is a truthful payload-token maximum, not an
allocation/RSS claim.

## 5. Streaming semantics and full-pass inventory

The standard encoder is configured for ASCII escaping, sorted keys, and exact
comma/colon separators (producer 244; checker 145).  The manual sealed-object
walk preserves that encoding recursively, omits only the selected root seal
member (including the correct comma), streams every other member in sorted
order, compares every emitted fragment with the same physical raw owner, and
requires exact exhaustion (producer 472--551; checker 347--421).  Standard
encoder handling supplies strings/escapes, lists, booleans, null, and numbers;
the frozen schemas introduce no non-JSON numeric value.

The special `Delta0.presentation.rows` path feeds the exact whole-array digest
and seven 1,024-row canonical chunk digests while the same fragments feed the
physical comparison/body seal (producer 484--540; checker 359--410).  The
following schema/type loop serializes nothing and preserves transport-before-
authority first-rejection order (producer 565--590; checker 435--458).  There
is no full-document canonical `str`+`bytes` pair, second 31-MB canonical
buffer, `deepcopy`, unbounded row-chunk roster on the pinned 6,441-row input,
or quadratic string concatenation.

The complete intended seven-row work inventory per program is:

- nine initial physical owner reads and ten mutation-owner reads;
- eight small manifest acceptance canonical/seal scans and five receipt
  acceptance scans, the latter simultaneously doing body seal and row feeds;
- four complete schema/type row walks (baseline and rows 5--7), plus row 1's
  immediate first-row rejection;
- four fresh receipt parses, four streamed receipt-body seal passes, and four
  final receipt construction passes;
- five small manifest-body and five final-manifest construction passes;
- ten case-stage readback hashes, one row-3 wire-source hash, and fourteen
  passes over all nine retained authority fds;
- seven small event-trace digests, one result-body seal pass, and one canonical
  stdout pass.

The two constructor receipt passes are necessary: the first derives the
self-seal and the second emits the object containing it.  `copy_manifest`
uses the local receipt identity directly (producer 693--698; checker 527--529),
while only the ordinary physical validator reopens and hashes the case owner.
Full constructed DOM/raw owners are released before the next ordinary case;
only small result records accumulate.  Result self-sealing and stdout occur
after the explicitly labelled public snapshot (producer 239, 910--925;
checker 141, 722--733), but both still use the same cumulative canonical cap,
fragment-token ledger, and installed address-space limit.  No avoidable
31-MB materialization/hash/schema pass or slow nested scan remains.

## 6. RLIMIT_AS, failure order, and stdout-only result route

On each supported application route, a supplied `--output` is rejected at
producer 930 or checker 738.  Its value is never converted to a path or passed
to a helper.  The rejection precedes cap installation, deferred ABI parsing,
fixture validation, authority reads, and every mutation workspace operation.

Otherwise `install_address_space_limit` (producer 892--908; checker 704--720)
requires Linux/POSIX `RLIMIT_AS`, selects the minimum of 700,000,000 and every
pre-existing finite soft/hard limit, rejects a nonpositive or >=750,000,000
target, preserves the hard limit, installs the soft limit, and demands exact
readback.  It is called at producer 931/checker 739 before the ABI JSON parse
at 933/741 and before fixture/source reads at 938/746.  Unsupported or
ineffective platforms stop before any authority-sized allocation.  Module and
CLI bootstrap allocations are small; no unavoidable source-visible allocation
is structurally incompatible with the 700,000,000-byte ceiling.  Actual Python
object cost and RSS remain unobserved.

`MemoryError`, an input/resource refusal, the unresolved producer name, an
external deadline, or cleanup failure cannot enter `seal_result` and stdout
on the seven-row route.  A failure during result streaming can at most leave
an incomplete canonical stdout prefix and a nonzero process termination; no
PASS terminal is emitted.

There is no v5 result-stage directory, final result leaf, link/rename result
operation, or output publication helper.  The only result functions are the
in-memory seal and bounded canonical stdout at producer 910--925 and checker
722--733.  The `os.link` operations at producer 786 and checker 613 belong
solely to the invocation-unique physical mutation case writer, whose target
must be an immediate child of that temporary workspace (producer 745--748;
checker 573--576).  They cannot receive `--output` and are not publishers.

## 7. Scope and one bounded repair

The fixture's only line, producer 667/888, and checker 508/700 all require
exactly:

```text
covered_rows=[1,2,3,4,5,6,7]
remaining_rows=[8,9,...,48]
candidate_only=true
full_a4_selftest=false
actual_a4_numerator=false
```

The `Q0_lift`, `fake`, and `Ihara_witness` strings occur only as keys of the
immutable task198 receipt contract; the v5 result constructor makes no lift,
fake, Ihara, basis, production-acceptance, full-A4, or rows-8--48 claim.  There
is no v7 driver in this tranche.

There is one load-bearing repair: create a new versioned producer tranche
which restores a **producer-owned** `admit_path` definition before its use,
including the ordinary containment event, registered-or-workspace test,
no-symlink component walk, path-kind rejection observation, and exact
`producer:path:registered_containment` reason.  Do not import or alias the
checker helper and do not alter the seven mutation meanings.  Freeze the new
physical identity and independently reaudit it.  No execution is authorized
before that repair.

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
ACYCLIC FIXTURE / TASK198 AUTHORITY:   PASS
ROWS 1--7 ORDINARY PRODUCER ROUTE:     REJECT
ROWS 1--7 INDEPENDENT CHECKER ROUTE:   PASS
MODELED TOKEN LEDGER:                  PASS
RLIMIT_AS / FAIL-CLOSED ORDER:         PASS
STREAMING CANONICAL / DUPLICATE WORK:  PASS
NO RESULT PUBLISHER / OUTPUT PATH:     PASS
V7 ROWS-1--7 CANDIDATE EXECUTION:      FORBIDDEN
PINNED GHA DRIVER:                     NOT PRESENT
FULL 48x2 SELFTEST:                    INCOMPLETE
ACTUAL A4:                             remains 1/3
LIFT / FAKE / IHARA:                   NONE

TASK375_R07_A4_V7_CODE_PERFORMANCE_REAUDIT_V1
