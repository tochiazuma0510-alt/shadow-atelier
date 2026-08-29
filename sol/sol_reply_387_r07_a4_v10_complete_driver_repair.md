# Task387 - A4/v10 complete source/driver repair

## 0. Result and audit boundary

The three new machine owners are complete as a **source-static repair
candidate**.  All five task386 rejection groups are repaired together, while
the task386 PASS clauses and the candidate-only rows-1--7 scope are retained.
This is not execution authorization: a fresh independent static audit is still
mandatory, and rows-1--7 GHA remains forbidden.

I used `apply_patch` for the four designated outputs and only read-only
PowerShell inspection, byte comparison, arithmetic and SHA-256 hashing for the
static closure.  I did not run or compile Python, Node, GAP, the candidates,
the driver, mutations, imports, subprocess tests, GHA/workflows, git, network
or RSS measurement.

## 1. Frozen machine-owner identities

| owner | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v8.py` | 103,455 | 976 | `d768605b2ff10abb5da15aa1ba70d73dcae0c6e45b636d46765e0d9529819794` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v7.py` | 101,148 | 768 | `d3c40dfb098a2031f203ef29945577923a9b2d8c214fb96d9c89c3dfaa267cb0` |
| `search/d972_r07_a4_actual_owner_trace_gha_driver_v10.g` | 98,724 | 1,588 | `e5d5a82be2ddd39bc255270b7edb2341f4124561c524b60cdbbb130d732ece39` |

All three are ASCII, BOM-free, NUL-free, LF-only files with a final LF.  The
GAP `Concatenation` wrapper was also checked statically line by line for its
quoted-line envelope.  The reply SHA is intentionally left for the external
freeze step required by the commission.

The v10 driver pins the first two identities exactly at D:71--72.  Its own
identity is obtained from its retained physical `BoundOwner`, avoiding a
self-referential source hash.

## 2. Exact forward and reverse delta

### Producer v7 -> v8

The forward delta is +497 bytes and +7 lines.  It consists only of:

- the truthful Task387/v8 title and result schema at P:2 and P:29;
- the added logical-link field in the opened-file identity at P:348--350;
- the truthful regular/symlink/nonregular/missing path split and link target at
  P:353--360; and
- the explicit `exists`, `type`, `readable`, content-readability,
  symlink/reparse and link-target projection at P:845--852.

An in-memory reverse replaced exactly those three function blocks and the two
version-label lines with their frozen v7 counterparts.  The result was
byte-for-byte equal to producer v7: 102,958 bytes and SHA-256
`4f7f57150892e354f3398c33e0f72c0d968c7101de05b7ce7e5690b47fcd064c`.

### Checker v6 -> v7

The forward delta is +500 bytes and +7 lines.  It consists only of:

- the truthful Task387/v7 title and result schema at C:2 and C:27 (the frozen
  v5 fixture schema remains independently fixed at C:28);
- the opened-file and path-identity changes at C:228--237; and
- the explicit physical projection at C:654--661.

The corresponding in-memory reverse was byte-for-byte equal to checker v6:
100,648 bytes and SHA-256
`7cf5468be847c3a49014986e39af9bb71120af6371aec05e23bb9789bb22c6c1`.

### Driver v9 -> v10

The forward delta is +26,120 bytes and +386 lines.  The complete repair-region
map is:

1. versioned paths, pins, result schemas, output names, task198 source pins and
   hard caps (D:1--124);
2. bounded scalar canonicalization, work/cleanup timers and retained-root
   identity (D:136--228);
3. incrementally owned directory/file descriptors, exact preallocation read,
   fused physical hashing, streaming canonical/root-seal admission and
   close-error recovery (D:239--511);
4. deadline-bearing publication rollback/close plus complete logical/physical
   graph aliasing and revalidation (D:538--729);
5. idempotent process stopping and stdout framing fused into the bounded pipe
   capture, eliminating the duplicate file scan (D:735--853);
6. physical transcript/payload construction, complete task198 manifest graph,
   truthful identity shape and exact snapshot admission (D:932--1153);
7. path-allowlisted streaming projection and the no-triple result reader
   (D:1154--1261); and
8. early parent limit, all-owner lifecycle, serial runs, full sentinel
   accounting, preterminal close/timer order and bounded failure cleanup
   (D:1262--1579), plus the truthful outer task/version labels and
   status-bearing GAP tail (D:1580--1588).

Restoring those enumerated blocks and truthful version labels from v9 recovers
the frozen v9 target (72,604 bytes, SHA-256
`130a6e838f648d58a81854eb74dc8476aa4f1d70dc4d6bfc0a5a81a3e3e68155`).
There is no wider mathematical, mutation, validator, conclusion or scope
delta.  The task386 event-suffix block D:865--931 is text-exact to v9; the
wider driver delta is entirely required by F1--F4, including the fail-closed
constructor/rollback-handle edges and the fused framing pass.

## 3. Task386 PASS clauses retained

- Producer row 4 still requires exactly the ordered pair
  `(transport,manifest.path)`, `(transport,receipt.path)` at P:869--873;
  checker does the independent equivalent at C:672--676.
- The other six rows still require exactly one occurrence of the registered
  rejection validator and its exact final validator/stage at P:874--877 and
  C:677--680.
- Driver reconstruction requires the same complete event lists and digests.
  Row 4 is the exact two-entry predicate at D:1139--1140; the other six use the
  exact singleton/final predicate at D:1141--1142.
- There is exactly one generic `subprocess.Popen`, one producer call at D:1349
  and one checker call at D:1362.  The producer DOM is destroyed before the
  checker call at D:1357--1360.  Both argv vectors remain fixed, serial and
  fixture-only; no producer result is injected into the checker.
- Stdout/stderr remain separate bounded streams.  Exact status zero is required
  at D:840, framing is now recorded during the same pipe capture at D:762--841,
  and no second whole-file framing scan remains.
- The durable same-directory exclusive-temp/no-replace-link/fsync/retained-fd
  publication primitive is retained at D:538--608.  GAP still uses
  status-bearing `Process` and checks its integer status at D:1584--1588.

## 4. F1 - complete physical task198 graph

The v10 physical registry has exactly twelve retained regular-file owners:

- producer v8, checker v7, frozen fixture v5 and driver v10; and
- all eight task198 owners: receipt, manifest, two attestations, checker
  verdict, producer source, checker source and GAP driver source.

The six formerly unbound source identities are declared at D:59--66 and opened
at D:1311--1315.  Receipt and manifest are opened at D:1332--1335; the exact
twelve-owner gate is D:1336.  Their pinned physical identities are:

| task198 owner | bytes | SHA-256 |
|---|---:|---|
| receipt | 31,017,244 | `82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5` |
| acceptance manifest | 2,722 | `cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4` |
| producer attestation | 81 | `b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090` |
| checker attestation | 95 | `260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e` |
| checker verdict | 150 | `ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de` |
| task198 producer source | 137,169 | `6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c` |
| task198 checker source | 157,253 | `001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1` |
| task198 GAP driver | 20,541 | `6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068` |

`validate_task198_manifest_graph` at D:993--1021 ties every manifest edge to
those retained owners, including receipt self-seal, attestations, verdict and
the three program identities.  The transcript at D:964--985 is derived from
the retained physical owners; no transcript literal substitutes for one.

The retained root, both output directories, all twelve file owners, every
visible output and all seven registered future paths participate in the graph
gates at D:685--712.  Thus the directories cannot alias one another, the root,
an authority/candidate/driver, or a visible output.  No-follow component walks
are retained.  The complete graph is rehashed/revalidated before and after
each candidate, immediately before sentinel construction, and after sentinel
publication at D:1348, D:1350, D:1361, D:1363, D:1375 and D:1479.  The
sentinel contains all eight task198 identities and records count eight at
D:1376--1408.

## 5. F2 - truthful row-4 owner and exact admission

Both candidates now distinguish `missing`, `symlink` and other nonregular
owners instead of equating nonregular with symlink/reparse.  For row 4 their
after projection is exactly:

```text
exists=false
type=missing
readable=false
symlink_or_reparse=false
logical_link_target=null
```

Producer constructs/projects this at P:353--360 and P:845--852; checker does
so independently at C:231--237 and C:654--661.  Driver identity admission has
an exact key set at D:932--938 and requires the missing tuple, false
symlink/reparse bit, null link target and unreadable evidence at D:1051--1067.

The resource payload map is no longer admitted by sum.  It is constructed from
exactly the six retained task198 source owners plus fixture, receipt and
manifest at D:986--991: nine exact absolute `cache:` keys, individual physical
byte counts and sum 31,343,744.  Every snapshot must equal that dictionary at
D:1036--1050.

Normalization is now a path allowlist at D:1154--1211.  The only rewritten
classes are the admitted root schema, row `entered_validators`, registered
first-rejection validator/reason, their derived event digest, and the two
role-length-derived canonical counters at the registered row/public-resource
paths.  Dictionary keys and all other nested strings/scalars stream unchanged,
so any other semantic difference survives the projection and rejects.

## 6. F3 - bounded buffers, containers and full passes

`read_bounded_fd` at D:430--453 allocates exactly the already bounded file
size, fills it with `readv`, and fuses the physical SHA-256.  There is no
piece-list/join copy.  `scan_canonical_root` at D:455--497 compares streamed
canonical fragments directly with the raw owner while simultaneously hashing
the root body without its seal.  Result admission at D:1240--1260 parses the
raw including its legal final LF, validates semantics, performs the fused
canonical/body scan, deletes raw/text, and only then builds the restricted
projection.  There is no LF-stripped payload or full canonical-result buffer.

Projection preallocates exactly the 8,000,000-byte cap and checks every
fragment before assignment at D:1213--1224.  It creates no normalized DOM.
Comparison uses two bounded bytearrays and non-copying memoryviews at
D:1226--1238.

The explicit payload/ASCII-character-cap phases are:

```text
authority receipt admission:
  2*31,017,244 + 2*786,434                         = 63,607,356
checker admission with retained producer projection:
  8,000,000 + 2*35,000,001 + 2*786,434            = 79,572,870
second projection construction / comparison bound:
  2*8,000,000 + 2*786,434                         = 17,572,868
sentinel/terminal bounded canonical buffers:
  2*1,000,000                                      =  2,000,000
maximum                                            = 79,572,870
```

Here 786,434 is the exact `12*65,536+2` worst-case ASCII encoding cap for one
JSON string; text and byte encodings may coexist.  Static scans found maximum
raw string-token content lengths 85, 68 and 308 in the pinned fixture,
manifest and receipt respectively.  D:1440--1445 records the same formula and
states its boundary explicitly; it is not RSS.

Container multiplicities are separately recorded at D:1443: three authority
DOMs at receipt admission; later one fixture plus at most one candidate-result
DOM; zero normalized DOM copies; zero retained producer-result DOM during
checker admission; one retained producer metadata dictionary/projection then
two metadata dictionaries/projections during comparison; bounded recursive
generator/path/sorted-key-reference state; nine transcript entries; nine
payload-owner entries; six candidate temp and six candidate published records;
and twelve retained authority/candidate/driver owner objects.  JSON/allocator
overhead and RSS are expressly outside the explicit-unit ledger.

The unavoidable passes, each with a distinct reason, are:

1. stdout pipe capture, now also carrying constant-size framing state;
2. retained-owner physical hash for the pre-interpretation pin and each
   security-boundary revalidation (D:239--262, D:702--712);
3. bounded read fused with physical hash to materialize parser input
   (D:430--453);
4. strict ASCII decode and JSON parse for a typed DOM (D:499--510 and
   D:1240--1250);
5. exact semantic validation before any normalization (D:1036--1152);
6. fused streamed canonical comparison/root body seal (D:455--497);
7. bounded restricted projection for independent-route equality
   (D:1154--1238); and
8. publication copy plus retained-fd hash for a durable independently named
   admitted output (D:560--608).

The former GAP directory scan, Python `os.listdir`, result payload slice, full
canonical result, recursive normalized copy and duplicate stdout file scan are
absent.

## 7. F4 - bounded stale scan, rollback and terminal order

The only stale scan is the bound-fd `os.scandir` route at D:327--345.  It has
an in-loop deadline, 100,000-entry cap, 16,777,216 total encoded-name-byte cap
and 4,096-byte individual-name cap.  The pre-harness GAP `DirectoryContents`
scan is gone.

The work timer is armed to `9000-260=8740` seconds at D:112--124 and
D:1286--1292.  `begin_cleanup` at D:192--201 always reinstalls the private
SIGALRM handler and arms a separate deadline ending no later than both
`now+260` and the 9,000-second global end.  Candidate margins remain CPU
3600/3610, external wall 3900 and two 30-second stop waits; the exact admission
gate is `2*(3900+2*30)+260=8180 < 9000`.  Repeated process-stop waits are
rejected by the idempotence marker at D:735--760.

Rollback has a deadline immediately before every final/temp stat, unlink,
directory fsync and fd close at D:618--671.  Stale iteration, graph loops,
copy/write/read loops, selector loops, owner/directory close loops and
rollback-handle recovery likewise carry deadline checks.  Successful
constructor ownership is registered incrementally, so a later bind failure
does not orphan earlier retained fds.

The success order is exact at D:1479--1508:

1. post-sentinel physical graph revalidation;
2. construct the bounded terminal;
3. arm the cleanup timer;
4. close all seven published/temp descriptors;
5. close all twelve authority file fds and twelve parent fds;
6. close both output-directory fds and the root fd;
7. cancel the timer and restore the previous handler; and
8. perform the sole accepting `os.write`.

After a complete terminal write only a scalar comparison, Boolean assignment
and return remain.  There is no later timer, close, revalidation, publication,
fsync or cleanup operation.

Any failure in steps 3--7 enters the nonaccepting path.  Because those steps
may already have closed directory/root fds, D:351--372 and D:714--728 reopen
only the no-follow paths whose physical identities equal the retained root and
directory identities.  D:1512--1528 rearms bounded cleanup, stops any child,
recovers those rollback handles and invokes rollback before the remaining
close/timer attempts.  Timer restoration failure and terminal short write use
the same route.  All rollback/cleanup errors are recorded, and the outer
harness exits nonzero.

## 8. Publication failure-edge inventory

- **Before visibility:** exclusive temp creation, copy/write, identity or file
  fsync failure leaves only a registered temp; rollback checks its retained
  device/inode, unlinks it and fsyncs its directory.
- **No-replace link failure:** the pre-registered visible record cannot cause
  deletion of a foreign final; a device/inode mismatch is reported and the
  harness is nonaccepting.
- **After link, before temp unlink:** rollback removes only the matching visible
  inode, then the matching temp, fsyncing after each attempt.
- **After temp unlink:** the matching final remains registered and is removed,
  fsynced and closed on any later hash, identity, directory or graph failure.
- **After one or more complete publications:** every visible owner remains in
  `TX.visible`; subsequent candidate, comparison, sentinel, close or timer
  failure rolls all of them back in reverse order.
- **Preterminal close/timer failure:** bound rollback handles are recovered by
  retained identities before unlinking; acceptance is never emitted and
  Python/GAP status is nonzero.
- **Rollback failure:** errors are included in the NONACCEPTING diagnostic and
  cannot convert failure to acceptance.

The publication primitive itself is D:538--608, rollback D:618--671, graph
verification D:609--712, preterminal closure D:1493--1503 and failure routing
D:1509--1569.

## 9. Scope and handoff

No runtime row, GHA artifact, A4 basis, full selftest, lift, fake or Ihara
witness was produced.  Rows 8--48 remain outside the tranche.  The actual A4
numerator remains `1/3`.  The next legal action is a fresh independent
source-static audit of these frozen identities; execution remains forbidden
until that separate audit authorizes it.

A4/V10 VERSIONED OWNERS:                 COMPLETE
TASK386 RETAINED PASS CLAUSES:            RETAINED
COMPLETE TASK198 PHYSICAL GRAPH:          REPAIRED
TRUTHFUL ROW4 MISSING OWNER:              REPAIRED
EXACT PAYLOAD / NORMALIZATION ADMISSION:  REPAIRED
BUFFER / DUPLICATE-PASS ACCOUNTING:       REPAIRED
BOUNDED STALE SCAN / CLEANUP TIMER:       REPAIRED
FAIL-CLOSED CLOSE / TERMINAL ORDER:       REPAIRED
CANDIDATE / DRIVER EXECUTION:             UNEXECUTED
FRESH INDEPENDENT STATIC AUDIT:           REQUIRED
ROWS1-7 A4/V10 GHA:                       FORBIDDEN
FULL 48x2 A4:                             remains INCOMPLETE
ACTUAL A4 NUMERATOR:                      remains 1/3
LIFT / FAKE / IHARA:                      NONE

TASK387_R07_A4_V10_COMPLETE_DRIVER_REPAIR
