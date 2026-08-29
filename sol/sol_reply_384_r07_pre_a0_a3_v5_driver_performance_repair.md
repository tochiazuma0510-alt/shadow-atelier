# task384 bounded static implementation -- pre-A0 A3/v5

## 0. Result and trust boundary

The three new machine owners are complete as a bounded Task384/v5 repair.
They preserve the task381 semantic and mutation PASS clauses, remove the
identified duplicate whole-owner work, replace the status-discarding GAP
invocation, and make every sentinel failure nonaccepting.  This was a static
implementation pass, not the fresh independent audit.  No candidate result,
runtime, RSS value, mutation outcome, or A3 numerator was produced.

The unchanged upstream P0 remains
`ci/in/d972_r07_pre_a0_single_target_a3_v4.prereg.v1.json`, 16,417 bytes,
SHA-256 `14ea6de8efac73e71854f6566a9202eb89164ab6b7b5940954e87b3af21ee8ae`,
with body seal
`f1991fa0c232e1d7ea95a211498b4d1741c2104b22271fb90ec1a7ee3af98be7`.
Its recursive inventory is still exactly 23 unique ordinary non-reparse
owners and 33,121,619 bytes.  Neither P0 nor any authority or frozen v4 owner
was edited.

## 1. Physical output identities

| output | exact bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_pre_a0_single_target_a3_v5.py` | 104,446 | `4fbbd5792a1d1cc7bb1c3d534bdc0966291751cc9d3cea99d1ed20ca7d70fecb` |
| `crosscheck/check_d972_r07_pre_a0_single_target_a3_v5.py` | 116,872 | `90838f12061783c77651c656f7bd1a572ca4a687339b5b70747342d18d32028a` |
| `search/d972_r07_pre_a0_single_target_a3_gha_driver_v5.g` | 18,597 | `0465b46a734048b4ef6c16ed079e7daf825f71407f8cfe1b969a648ffb936d27` |
| `sol/sol_reply_384_r07_pre_a0_a3_v5_driver_performance_repair.md` | 16,209 | external post-write envelope required |

The reply's own physical SHA-256 cannot truthfully be embedded in the same
bytes: that would require solving a SHA-256 fixed-point equation.  Its exact
post-write bytes and SHA-256 are therefore supplied by the parent handoff as
the non-circular external envelope.  The byte count above is fixed after the
last patch; no in-file claim substitutes a preimage or placeholder digest for
the physical reply digest.

All three machine owners are ASCII, LF-only, final-LF files.  Driver lines
19--23 pin the exact P0, producer, and checker identities above.

## 2. Exact forward and reverse deltas

The line delta below is the exact minimal insert/delete distance over physical
lines; byte delta is direct UTF-8 byte length subtraction.

| forward delta from frozen v4 | old -> new bytes | old -> new lines | exact line edit | net bytes |
|---|---:|---:|---:|---:|
| producer | 104,369 -> 104,446 | 2,322 -> 2,323 | +13 / -12 | +77 |
| checker | 115,675 -> 116,872 | 2,469 -> 2,492 | +45 / -22 | +1,197 |
| driver | 20,111 -> 18,597 | 240 -> 245 | +86 / -81 | -1,514 |

The producer reverse map restores the v4 source/schema/path/module/wall
labels, removes the three post-`setrlimit` readback lines, and restores the two
deleted immediate `digest_bytes` checks.  The result was compared in memory
and is byte-for-byte the frozen 104,369-byte producer with SHA-256
`171e73dab2bd27f638021ceea43d8fb96ec4623a13d45873f364114e4290badd`.

The checker reverse map additionally collapses `authenticated_sha` back into
the old inline receipt check, removes its typed transport through normal and
UNKNOWN construction, restores the old verdict-only receipt rehash, removes
the three post-`setrlimit` readback lines, and restores the two import hashes.
It is byte-for-byte the frozen 115,675-byte checker with SHA-256
`eb07e34164f27b6676b97c722fb0fb2ef87b1e971baaab3d18c26770f17b7804`.

The driver reverse map restores v4 paths/pins/schema/error labels, the
38-line pre-checker receipt helper, the two-line `rsha2` pass, the old sentinel
tail and `Exec`, and removes the exact-bash status gate.  It is byte-for-byte
the frozen 20,111-byte driver with SHA-256
`78ee39b6f8926c267cb24d6b15bdc3a961906cdb8ddf9de8f7668222a5113f91`.
All three reverse comparisons used only in-memory read-only PowerShell; no
recovered file was written.

## 3. Producer duplicate-source repair

- The truthful Task384/v5 label and explicit v5 receipt schema are at producer
  lines 2 and 36.  P0 and the projected-interface base schema intentionally
  remain their unchanged v4 upstream identities at lines 31 and 35.
- `read_bytes` at lines 403--434 retains the regular/non-symlink stat, exact
  size, physical read and exact SHA check; line 433 is the sole hash of each
  returned read.
- `load_engine` at lines 1942--1968 retains the pre-import authenticated read,
  fresh Task384/v5 module name, compile/exec boundary, wall deadline, import
  counter and physical post-import authenticated reread.  Lines 1963--1966
  now go directly from counter consumption to `read_bytes(...,
  authority=False)` and release; neither already-authenticated byte object is
  immediately hashed again.
- The source-pin sum remains 894,133 bytes (lines 138--153), so the exact
  removed duplicate hashing is `2*894133 = 1,788,266` bytes.  The necessary
  two physical source reads and two physical SHA passes remain.

## 4. Checker duplicate and digest-transport repair

- Checker lines 2 and 36--37 give truthful Task384/v5 source,
  receipt and verdict schemas; P0/base schema stay v4 at lines 31 and 35.
- The generic authenticated reader's sole SHA is at lines 357--388.
  `load_engine` lines 1881--1906 retains the pre-read, one module build,
  compile/exec deadline/counter and post-import physical authenticated reread,
  with no immediate duplicate digest at lines 1901--1904.  The 1,450,252-byte
  source-pin sum therefore saves exactly `2*1450252 = 2,900,504` duplicate
  hashed bytes.
- `read_receipt` lines 1909--1940 computes `authenticated_sha` exactly once at
  line 1929, proves equality with the driver pin at 1930--1931, then retains
  the same immutable bytes for JSON, canonical, body-seal and result checks.
  The authenticated typed value is returned at line 1940.
- `verdict_document` lines 2095--2114 requires bytes, 64-character lowercase
  hex typing, and exact equality of the transported and pinned digests at the
  function boundary.  Line 2122 writes that value directly.  There is no
  `digest_bytes(receipt_raw)` verdict-population pass.  Normal and UNKNOWN
  call paths transport the value at lines 2164--2175 and 2397--2478 while an
  empty/unread receipt is required to carry `None`.

Let `R` be the exact byte length of the future canonical produced v5 receipt;
statically `0 < R <= 19,000,000`.  The removed checker digest is exactly `R`
hashed bytes.  A numerical `R` does not yet exist in this tranche because
candidate execution is expressly forbidden.

## 5. Driver whole-owner consolidation

- Driver lines 96--100 now require only a regular, non-symlink, nonempty owner,
  the `R <= 19,000,000` bound, and one streaming `sha256sum` for checker
  injection.  The checker command follows immediately at lines 101--102.
  The old 38-line pre-checker JSON/canonical/body-seal helper is absent.
- Exact-one terminals, zero accepting subprocess statuses, UNKNOWN rejection
  and terminal equality remain at lines 86--111.  The receipt SHA is still
  injected into the pinned checker at line 102.
- The intermediate `rsha2` is absent: terminal equality at line 111 proceeds
  directly to verdict owner/size/SHA checks at lines 112--116 and the final
  independent helper at lines 117--165.
- That final helper retains physical/canonical/seal checks, including
  `sha(rraw)==rsha` at line 139; v5 verdict typing at line 141; receipt/verdict,
  P0, 23-owner, projection, evaluator, mutation, rank and resource bindings at
  lines 143--162.  Required post-validation physical receipt and verdict
  rehashes remain at lines 166--169.

The deleted pre-helper's full canonical reconstruction emitted exactly `R`
bytes.  Its body-seal reconstruction emitted exactly `R-88` bytes: the
canonical top-level pair `"self_digest_sha256":"<64 lowercase hex>"` plus its
single comma occupies 88 bytes.  Thus the two removed driver serializations
are exactly `2R-88` serialized bytes.  The removed intermediate driver hash is
exactly another `R` hashed bytes.  The helper removal also eliminates its
separate `R`-byte physical read and its JSON DOM parse; those are stated
separately rather than conflated with serializer-output byte accounting.

For the task384 enumerated hash/serialization items, total exact avoided work
is

`1,788,266 + 2,900,504 + R + (2R-88) + R = 4,688,682 + 4R` bytes,

at most 80,688,682 bytes when `R=19,000,000`.  The additional removed
pre-helper read/parser is not included in that enumerated total.

## 6. Status-bearing GAP shell gate

Installed GAP 4.16 source was read directly.  `lib/process.gd:30` documents
the exact signature
`Process(dir, prg, stream-in, stream-out, options)`; lines 37--39 say it waits
and returns the process return value; lines 148--150 declare argument filters
`[IsDirectory, IsString, IsInputStream, IsOutputStream, IsList]`.
`lib/process.gi:79--105` installs the `InputTextNone`/output-text method and
returns `ExecuteProcess(...)`.  For contrast, `process.gi:257--263` shows
`Exec` calling `Process` and discarding the returned status.

Driver line 2 fixes the executable to exact `/usr/bin/bash`, lines 37--38
require that exact path to exist and be executable, and lines 236--237 call

`Process(DirectoryCurrent(), D363Bash, InputTextNone(), OutputTextUser(),
["--", D363Shell])`.

Lines 238--241 reject a noninteger or any nonzero/signal status.  Only after
that gate does line 242 read the sentinel, lines 243--244 require exact v5
bytes, and line 245 permit `D363_DRIVER_ACCEPTED`.  A surviving sentinel after
any helper or bash failure is therefore never inspected.

## 7. Fail-closed sentinel publication

- Driver lines 170--182 bind the fixed `ci/out` path through no-follow
  root/`ci`/`out` directory fds and use exclusive no-follow creation.  No stale
  output is pre-deleted; stale names are rejected at lines 57--60 and 84--85.
- Lines 184--191 loop until all exact `D363_V5_ACCEPTED` bytes are written,
  fsync the file, require successful file close, and fsync the bound output
  directory.
- Lines 192--205 retain the original publication error and every file/root/ci
  close error.  A first close error becomes an original failure; later close
  errors remain rollback diagnostics.
- On every recorded post-create failure, lines 206--212 attempt exact
  dirfd-relative unlink, treat only exact absent-name as an allowed rollback
  state, and fsync the same bound directory regardless.  Unlink/fsync errors
  are retained, not swallowed.
- Lines 213--227 make output-directory close failure nonzero and, when it is
  the first failure, attempt the same unlink+fsync rollback before retaining a
  reclose failure.  Lines 228--232 print every original and rollback diagnostic
  and exit 70.  The GAP zero-status gate then remains decisive even if an OS
  close/rollback failure leaves exact sentinel bytes behind.

## 8. Remaining necessary passes, live objects and static caps

The task381 PASS topology is unchanged: one producer base build plus three
area builds, one producer closure, one checker base build plus three area
builds, one independent checker verifier, exact 486/729 post-call rosters,
twelve checker-internal directed span comparisons, and twelve owner-local
mutations on each side.  Producer lines 1773--1939 and checker lines
1714--1878 retain baseline plus the exact mutation matrix; producer lines
2198--2217 retain one closure and exact rosters; checker lines 2303--2323
retain one verifier and exact rosters.

Remaining necessary whole-owner passes and maximum simultaneous live objects
are:

1. In each process, each of the 23 authorities has one physical read/SHA.
   The 31,017,244-byte task198 owner has one DOM parse, one streaming canonical
   raw comparison and one streaming body-seal traversal.  The retained raw map
   and that one large DOM coexist only until the compact snapshot is made;
   large raws/DOM are released before task226/closure or verifier work.
2. Each current imported source has exactly two physical read/SHA passes
   (pre-import and post-import drift boundary).  At the post boundary at most
   the two byte buffers `raw` and `post` for that current source coexist, plus
   the one compiled code/module object; modules are built once and retained,
   never rebuilt for hashing.
3. The checker gives the produced receipt one physical read/SHA, one DOM parse,
   one streaming canonical comparison and one streaming body-seal traversal,
   followed by the necessary independent result reconstruction/verifier.  Its
   maximum receipt-side byte objects are the retained `R` bytes, one receipt
   DOM, one shallow seal-body dictionary and one at-most-65,536-byte canonical
   chunk.  There is no duplicate raw/canonical buffer or verdict digest pass.
4. Before the checker, the driver has only the bounded owner checks and one
   streaming injected SHA.  Its final helper holds receipt, at-most-1,000,000-
   byte verdict and 16,417-byte P0 raws/DOMs, creates at most one full canonical
   serialization at a time, and reads one authority owner at a time.  After it,
   exactly one streaming physical receipt rehash and one verdict rehash remain.
5. During checker evaluator reconstruction, private Q0 is 7,348,320 bytes and
   its construction component peak is 14,696,640 bytes; it is no longer live
   when the produced receipt DOM is constructed.  Python object/allocator
   overhead is not asserted equal to payload bytes.

Exact static formulas remain:

| quantity | formula / bound |
|---|---:|
| P0 + 23 authorities | `16,417+33,121,619 = 33,138,036 < 40,000,000` |
| producer six-source input | `16,417+33,121,619+2*894,133 = 34,926,302 < 60,000,000` |
| checker seven-source input before receipt | `16,417+33,121,619+2*1,450,252 = 36,038,540` |
| checker input with max receipt | `36,038,540+19,000,000 = 55,038,540 < 60,000,000` |
| producer normal serializer component | `3*19,000,000+65,536 = 57,065,536` |
| producer failed-normal plus emergency charge | `57,065,536+4*65,536 = 57,327,680` |
| checker verdict serializer component | `3*1,000,000+65,536 = 3,065,536` |
| evaluator build operations | `26+243*26+59,049*6+243*10 = 363,068 < 1,000,000` |
| Linux address-space ceiling | `4,294,967,296` requested bytes |
| walls | `1800<2100`; `2*2100=4200<21600` seconds |

These are component/payload bounds, not an RSS proof.  Producer lines
366--389 and checker lines 321--343 require Linux `RLIMIT_AS`, set the bounded
target, read it back, and require both installed soft and hard values equal the
target (producer 383--386; checker 337--340).  Boundary RSS telemetry remains
in the candidates, but no RSS observation was made here.

## 9. Static-only closure and next gate

Only permitted `apply_patch` writes to the four designated outputs and
read-only PowerShell/.NET inspection, exact byte comparison and SHA-256 hashing
were used.  Python, Node, GAP, candidates, generated shell, mutations,
GHA/workflows, git, network, imports, syntax compilation, child subprocesses
from inspected programs, and RSS measurement were not run.  In particular no
`git status`, commit, push, workflow dispatch or artifact download occurred.

A different auditor must now read all four physical outputs completely,
recheck pins/reverse deltas/Process semantics/failure traces and issue a fresh
independent static PASS.  Until that audit, a serial A3/v5 GHA candidate is
forbidden.  Even after such a run, its output remains a candidate subject to
the repository's independent cross-check and Lean-reserved verification
hierarchy.

A3/V5 VERSIONED OWNERS:                 COMPLETE
TASK381 SEMANTIC / MUTATION PASSES:      RETAINED
PRODUCER DUPLICATE SOURCE HASHES:        REMOVED
CHECKER DIGEST / SOURCE DUPLICATES:      REMOVED
DRIVER RECEIPT PASS CONSOLIDATION:       COMPLETE
STATUS-BEARING SHELL GATE:               COMPLETE
SENTINEL FAIL-CLOSED ROLLBACK:           COMPLETE
STATIC CAPS / PERFORMANCE:               REPAIRED
CANDIDATE EXECUTION:                     UNEXECUTED
FRESH INDEPENDENT STATIC AUDIT:          REQUIRED
PRE-A0 A3/V5 GHA:                        FORBIDDEN
ACTUAL A3 NUMERATOR:                     remains 0/3
A0 / COFINAL LIFT / FAKE / IHARA:        NONE

TASK384_R07_PRE_A0_A3_V5_DRIVER_PERFORMANCE_REPAIR
