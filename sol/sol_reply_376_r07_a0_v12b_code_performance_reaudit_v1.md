# Sol(max) task 376 — A0/v12b fresh static code/performance reaudit

## 0. Scope, method, and decisive result

I am not the task372 implementer.  I read task354/reply354, task368 and its full
STATIC REJECT, task372/reply372, the six task376 subjects, and the P0-pinned
v275--v290/task176/raw-checkpoint authority roster.  In accordance with the
commission I did **not** run Python, Node, GAP, GHA, a workflow, git, imports,
syntax compilation, candidate code, mutations, RSS tests, subprocess tests, or
network access.  The checks below are fresh static source inspection plus
read-only PowerShell byte counts, SHA-256, ordinary-file tests, character tests,
and independent canonical-body reconstruction.

The decisive result is **STATIC REJECT**.  This is not a near-pass: the frozen
P0 and fixture are not in their declared physical canonical form, and the code
also fails independently on mutation-owner reality, bounded work, deadline
coverage, live-memory proof, and fail-closed publication.  All load-bearing
defects are listed together in §8 so that one bounded repair can address them.

## 1. Exact frozen subjects

Read-only physical inspection reproduced all six commissioned byte/SHA pairs;
each path is an ordinary non-symlink file:

| owner | bytes | SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12b.manifest.v1.json` | 27,295 | `ecd722495b02dc48cfa68e3be9751a82664fd895a4b01d185c647b4053fbfbe7` |
| `search/d972_r07_history_free_positive_fast_resume_v12b.py` | 317,154 | `614bc65bbb36c0a7504923c9ba7b4700ba04ecb66868d5a90994c65e1577dcd7` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v12b.py` | 263,911 | `1b8587de9caabc16f3a51ace1d2ea5a892281d155ea4f4270e830208ec4cd0d0` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v12b.g` | 28,740 | `631ba0d02443d8d4f142248aa098859b2e943cb86073b7021313b22c7cff7896` |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12b_20260829.json` | 23,679 | `64a7dd14e26431387f6ff1dd71aad6d977a5db943c4ca42c01fb19477f3a3ddb` |
| `sol/sol_reply_372_r07_a0_v12b_minimal_complete_repair.md` | 14,913 | `06811754600b16f82e8ca0460c86461ecdd44ebb6588d98596dd724d7f1e7426` |

The GAP driver is ASCII, has no BOM or CR, has 328 LF characters, and ends in
one LF.  Its four top-level pins match the commissioned P0/producer/checker/
fixture identities (driver lines 33--37), and its recursive pins agree with the
P0 roster (lines 38--68).

The P0 contains 33 recursive rows over 32 unique physical paths (the fixture is
named in both `sources` and `frozen_authorities`).  Read-only hashing reproduced
the size/SHA of every presently extant path.  The prospective
`ci/resume/...v12b.raw.json` is correctly absent before the driver runs; a
read-only stream inspection of the pinned 5,001,811-byte archive found exactly
one member with the exact name, uncompressed size 86,368,039, and SHA-256
`c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab`.
Thus there is no retained v12a hash or placeholder among recursive physical
identities; the rejection below concerns ownership/canonicality, not hash drift.

## 2. P0, fixture, canonicality, and authority graph

The semantic body seals themselves reproduce exactly:

- P0 body: 11,351 canonical ASCII bytes, SHA-256
  `3538a629d7e3ce44d965ff796d201bee23cfca1087f3c966b84b9dfe8dcb3419`.
- fixture body: 21,153 canonical ASCII bytes, SHA-256
  `cc787bc588f05a0bf49cebc385a968d10c245d906352d3b6e8e53d101f9c8ad5`.

Those valid semantic seals do not cure the physical contract:

1. P0 lines 17--20 declare sorted compact ASCII JSON plus exactly one LF, but
   the frozen owner is pretty-printed and contains 275 CR and 346 LF bytes.
   Its required full `canonical(value)+LF` representation is 11,440 bytes with
   SHA-256 `5276946c8e63c57117fd9bd59a776c277fd91d80fb56704df13e48a18733dcde`,
   not the frozen 27,295-byte owner.
2. The fixture is likewise pretty-printed (289 LF); its required full canonical
   representation is 21,242 bytes with SHA-256
   `1817b065f0e86399857ac2ff8b4eb747a22975f0d789e956baa4e916e51f9342`,
   not the frozen 23,679-byte owner.
3. Producer `read_bounded_json`/P0 validation (producer lines 2915--2990,
   5680--5744) and checker `open_physical`/P0 validation (checker lines
   960--1034, 3643--3661) parse and seal-check these owners but never require
   `raw == canonical(value)+b"\n"`; their canonical predicate is permissive.
   The driver does impose that equality at lines 213--244, so its artifact gate
   would reject the very P0 accepted upstream.
4. Task376 explicitly requires that P0 not pin final Python physical hashes.
   P0 instead says that it does so (P0 line 13) and embeds the checker and
   producer final byte/SHA rows at lines 323--338.  The driver is not the sole
   downstream final-source pin as required by task376 lines 52--54.  Thus the
   declared one-way authority ownership is nonconforming even though the
   embedded byte values happen to match.
5. The identical fixture physical owner appears twice, as frozen authority
   `fixture` at P0 lines 165--169 and source `fixture_v12b` at 329--333.  That is
   the observed 33 rows/32 paths and violates task376's no-duplicate-owner
   condition; one role must be authoritative and consumers must reuse it.

Accordingly the P0/fixture/acyclic-graph category is REJECT.

## 3. Chronological triangular route and actual selected owner

The underlying ordinary mathematical routes are the strongest part of v12b:

- Producer construction and validation use a growing `seen_pivots` owner
  (producer lines 1320--1431 and 3012--3061); a future pivot is not rejected
  merely because it is a later pivot.  The frozen P5/P6 fixture declares the
  same chronological rule.  This portion passes statically.
- The producer's actual target route derives the current dual at the rank-2896
  epoch, checks annihilation of every chronological row, equates nonzero target
  and remainder pairings, retains the actual formal solution/remainder, searches
  the real Q0/Gamma/K0 roster, and applies ordinary `add_actual` 2896 -> 2897
  (producer lines 3643--3799).  No one-key functional or hard-coded selected
  coordinate is visible.  This portion passes statically.
- The checker begins from one authenticated raw-checkpoint parse and rebuilds
  all 2,896 columns, sparse/provenance/ancestry/P owners, target reduction,
  formal solution, initial/current dual, annihilation, selected owner, and the
  2896 -> 2897 transition before accepting transported heavy identity (checker
  lines 2944--3075 and main ordering at 4805--4869).  It does not initialize
  the dual from the producer statement.  This portion passes statically.

The triangular mutation implementation does not pass the separate physical and
performance requirements.  The producer borrows all 2,896 columns into a frame
(lines 3004--3009), serializes and reparses the complete frame for each of eight
cases (3071, 3082--3097), mutates only a three-column prefix (3120--3154), and
then performs the physical trace (3163--3165).  The checker retains the full
2,896-column snapshot (3070--3074) and reserializes the whole baseline for each
case (3933--4025).  These are full-frame work/DOM/raw owners, contrary to the
claimed small-record mutation policy and task376 lines 103, 126.

## 4. Mutation-owner audit

The declared counts are present in both ledgers: triangular 8, boundary 13,
selected-correction 30, positive 7, physical 11, phase 4, and phase-positive 2.
Both sides normalize the six rejecting groups and compare exact rows/digest
(checker lines 4897--4926).  `MutationAccepted`, wrong-reason failures, and
arbitrary exceptions are outside the narrow expected catch in the ordinary
trace wrappers (producer physical trace around 3082--3118; checker lines
3890--3930).  Nevertheless the required *real owners* are not all exercised:

1. Producer selected mutations construct a full canonical clone through
   serialize/decode for every one of 30 cases (producer lines 4563--4571);
   boundary does the same for 13 (4945--4947), positive for ordinary cases
   (5079 onward), and physical semantic cases clone their baseline (5251
   onward).  Checker `clone = json.loads(canonical(...))` (3816--3817) is used
   for every selected case (3360), boundary case (4070), positive replay
   (4183, 4246), and phase case (4636).  This defeats the claimed no-full-frame/
   no-full-R clone envelope and introduces simultaneous old DOM, serialized
   bytes, and new DOM.
2. The normal process matrix reaches W2 and W4, but producer fault runs are
   hard-coded to W2 and blocked-send uses one child (producer lines 4688--4776).
   Checker repeats that shape (checker lines 2019--2049).  Boundary mutation
   rows therefore borrow W2/one-child fault substitutes rather than the
   mandated real W4 outcome/fault/blocked-send owners.
3. Producer `producer_physical_mutations_v297` starts from a miniature
   `/positive-selftest-frame` (producer lines 5131--5139), not the actual R
   envelope.  For example `terminal_reseal` merely adds/changes a field on that
   substitute (5262--5266), while actual R is not constructed until main lines
   5887--5922.  The checker does borrow actual R for its physical suite
   (checker lines 4351--4527), but that does not repair the producer side's
   missing physical-R owner.
4. The positive validator itself clones the selected-correction seed and then
   invokes the nested selected validator (checker lines 4183--4185); repeated
   positive cases consequently perform hidden selected-owner work in addition
   to the advertised positive transition.
5. The claimed cross-ledger equality omits both phase-positive cases.  Producer
   `observed_groups` contains only the six rejecting groups (producer
   5621--5632); checker `normalized_groups` does the same (checker 4908--4926),
   and even its mutation count at 4962--4965 excludes phase-positive.  Moreover,
   normalization retains only fixture-shaped id/path/validator/stage/reason/
   reseal fields, discarding measured before/after identities and event-trace
   digests.  Equality therefore proves equality to a shared static contract,
   not equality of the two independently measured complete 75-case ledgers.

Hence exact ledger shape is not evidence that every case reaches the required
load-bearing physical owner, and this category is REJECT.

## 5. Linear DAG and avoidable work

`AncestryDAG.expand` passes its narrow algorithmic test on both sides.  Each
implementation uses one descending weights map and one answer map, consumes
children before parents, charges before insertion, and enforces
`len(weights)+len(answer) <= 2,000,000` (producer lines 226--300; checker lines
1141--1240).  There are no per-node memo-dictionary copies in that routine.
Snapshot authentication is cached and later consumers reuse the snapshots
(producer 5747--5772; checker 3675--3739 and 4782--4833), and known Q0
duplicates skip before coordinate work (producer 2463--2470).

The intended last-consumer drops are also visible: producer releases its heavy
source carriers at 5633--5649 and clears the old DOM/source registry at
5885--5886; checker releases raw checkpoint at 4853--4855, selected K0 at
4885--4896, decoded task176/parent caches at 4927--4931, and source snapshots at
4931.  Those local positives do not cover the extra mutation DOMs and repeated
serializations described next.

The broader performance category still rejects:

- `pc_cache` allocates `pc.mul(...)` and `bytes(...)` before charging the
  attempted insertion; only afterward does it call `meter.bump`, check the
  131,072 cardinality, clear, and insert (producer 2479--2487).  Cardinality is
  bounded, but allocation-before-cap violates the explicit preallocation rule.
- The claimed “only two full Gamma” statement (producer 182--193) is false.
  The canary at 2705 and selected construction at 3293 are already two, then
  the ordinary validator reconstructs a 4,814-byte full Gamma again at
  3462--3471.  Baseline and mutation validations repeat that call.  Checker
  ordinary selected validation similarly constructs it at 2760--2764 and is
  called for baseline and many mutation/positive cases.
- Full triangular serialization/reparse is repeated eight times on each side,
  and serialize/decode cloning is repeated across the 30/13/7/4 suites as
  detailed in §§3--4.
- Checker builds a 1,469,664-element Python `parents` integer list and a second
  `letters` list solely to hash them (checker 802--812), instead of streaming
  their already authenticated byte owners.  The Gamma coordinate recurrence
  and selected validation are also repeated for the baseline and mutations.
- Long producer loops lack local meter checks: K0 build loops over 1,469,664
  states without a check inside the loop (producer 2111--2143), and the actual
  selected nested qid/gid/coordinate roster loop (3680--3735) has no check.
  Repeated canonicalization/DOM construction in mutation suites likewise has no
  check inside each heavy serialization/validation.

These are source-visible repeated scans, hashes, allocations, DOMs and
serializations.  Renamed resource counters do not provide a source-derived time
or memory bound for them.

## 6. Live memory, IPC, and publication

The commissioned arithmetic identities reproduce exactly.  Producer payload/
output is

`1,425,574,080 + 52,907,904 + 243,105,472 + 235,710 + 4*86,368,039 + 536,870,912 = 2,604,166,234`,

and `2,604,166,234 + 2,295,833,766 = 4,900,000,000`, nominally leaving
800,000,000 below 5,700,000,000.  Checker payload/output is

`4*86,368,039 + 60,492,663 + 243,105,472 + 536,870,912 = 1,185,941,203`,

and `1,185,941,203 + 3,414,058,797 = 4,600,000,000`, nominally leaving
1,100,000,000.  These are arithmetic identities, not proved live upper bounds.
The two unexplained “CPython/COW/mutation reserve” remainders are constants in
producer lines 182--198/checker 75--89; no source derivation bounds DOM/list/int/
dict/COW costs or the full clone states identified above.

There is also an exact required allocation-accounting deficit.  The fixed
publication cap is 536,870,912 bytes, but at the required point *before* R/V DOM
construction the code has reserved 0 of those bytes: R/V bodies are constructed
in main, and only later does `atomic_json`/`exclusive_json` reserve an estimated
actual serialization length (producer 2854--2860 and 5887--5922; checker
3767--3775 and 4932--4981).  Thus the exact missing preconstruction reservation
is 536,870,912 bytes on each side.  The later estimator is not the required full
cap reservation.  This, plus simultaneous baseline/serialized/new DOM states,
prevents static proof of either 4.9 GB or 4.6 GB peak.

IPC is sequential and normal W2/W4 ownership, additive STOP accounting, maximum
physical gauges, child-PID sampling, peak four, and pre-heavy fork placement are
present.  But the missing W4 fault/blocked owners noted in §4 prevents a full IPC
pass.

Publication is not fail-closed:

- Producer links the temp to final R, unlinks temp, and only then checks parent
  identity and directory fsync (producer 2881--2904).  Its `finally` removes
  only temp (2905--2909); a failure after link leaves R published, and the
  `ProtocolStop` handler does not remove it (5943--5947).
- Checker has the identical post-link gap at 3784--3807 and its local `finally`
  cleans only temp (3808--3812).  Its outer `CheckStop` handler does unlink the
  visible verdict (4991--4997), but it never fsyncs the directory after that
  rollback, so absence is not durably fail-closed as required.
- Driver raw extraction links/unlinks before directory fsync and has temp-only
  rollback (driver 165--173).  Its final sentinel does likewise (313--320): if
  directory fsync fails after link, the visible sentinel survives.  Log
  `publish()` at 193--197 has no directory fsync at all.

The repair must preserve a rollback-capable temp until post-link checks succeed;
on every post-link failure it must remove the final name and fsync the directory
again (or use an equivalently proved no-replace protocol).  Current code has no
such rollback directory fsync.

## 7. Deadlines, driver, platform, and terminal gate

The numeric deadline chain is arithmetically correct:

- producer 9,600 internal / 9,900 external: 300 seconds;
- checker 5,400 internal / 5,700 external: 300 seconds;
- artifact 1,200 internal / 1,500 external: 300 seconds;
- external sum `9,900+5,700+1,500 = 17,100`;
- outer 18,000 gives 900 seconds; workflow 21,600 gives 3,600 seconds.

Driver lines 175--181, 198--207, and 324 encode those boundaries.  It creates
directories natively (87--92), rejects stale v12b prefixes before heavy work
(93--112), pins fixed quoted paths (175--181), checks Linux/x86_64 and required
commands (118--120), streams the last R/V rehash (286--300), and demands exact
one full-line producer/checker terminals (183--192).  It reads R then clears it
before reading V (244--270), so it does not hold R+2V raw or both DOMs.  The
Python preflights require Linux/posix/fork/AF_UNIX/O_NOFOLLOW/proc; mode parsers
have only SELFTEST_BOOTSTRAP.

But a 300-second numerical difference is not a proved strict cleanup margin
when lengthy regions can run past their internal deadline without sampling it.
The producer holes listed in §5 can continue until the external `timeout`; the
checker samples only between whole mutation groups at 4873--4884, not within
each repeated clone/serialization/validator route.  Publication and cleanup
then may receive no internal margin.  In addition, driver sentinel publication
is not fail-closed, and the driver's canonical P0 gate deterministically
disagrees with upstream permissive P0 readers.  Therefore the accepting driver
route and deadline/platform category reject despite correct constants and good
terminal wording.

## 8. One bounded repair: all load-bearing defects

The next version must address all of these together before another execution is
eligible:

1. Re-freeze P0 and fixture as their declared canonical ASCII JSON plus one LF;
   enforce raw canonical equality in both Python readers; remove final
   producer/checker physical hashes from P0 so only the downstream driver pins
   those final owners; collapse the duplicate fixture row to one authoritative
   owner; then update all downstream physical pins without a post-freeze cycle.
2. Replace full triangular/R canonicalize-parse mutation work with bounded
   extant owner views/deltas; remove serialize/decode `clone`/deep-copy routes
   across selected, boundary, positive, and phase suites; keep exact physical
   trace and the same ordinary validator.
3. Supply real W4 normal, timeout, death, partial, and blocked-send owners on
   both sides; make producer physical 11 mutate an actual R owner, not a
   positive miniature; remove the checker positive suite's hidden nested full
   selected replay where it duplicates unrelated work; include both
   phase-positive owners and measured identities/event traces in the
   independently compared complete ledger/digest.
4. Charge `pc_cache` attempts before multiplication/bytes allocation, and make
   the “two full Gamma” invariant true by retaining/reusing exactly the canary
   and selected values.  Stream the checker parent/letter digest and eliminate
   repeated Gamma/K0/full-owner scans.
5. Add wall/deadline checks inside every potentially long K0, selected-roster,
   mutation serialization/validation, hashing, and cleanup route.  A shared
   `check_wall`/meter name is insufficient unless every long loop and allocation
   is actually covered and leaves the advertised strict 300-second cleanup
   margin.
6. Provide source-derived simultaneous lifetime bounds for raw bytearray,
   bytes, ASCII, DOM, lists/ints/dicts, COW, mutation clones and output bytes;
   reserve the exact 536,870,912-byte output cap before constructing R/V, then
   encoded-size recheck.  Recompute the peak after removing duplicate owners.
7. Repair producer, checker, raw extraction, logs, and sentinel publication so
   every failure after no-replace link removes the final name and performs a
   rollback directory fsync.  No positive R, V, log terminal, raw alias, or
   sentinel may survive an UNKNOWN, timeout, mismatch, or fsync failure.

No execution evidence can repair these frozen static defects.  No v12b GHA run,
production, or resume is authorized; actual A0 common/checker remains 0/1.

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
P0 / FIXTURE / ACYCLIC GRAPH:          REJECT
CHRONOLOGICAL PIVOT ROUTE:             PASS
ACTUAL CURRENT DUAL / SELECTED OWNER:  PASS
INDEPENDENT RAW CHECKER:               PASS
ALL REAL MUTATION ROUTES:              REJECT
LINEAR DAG / DUPLICATE WORK:           REJECT
STATIC MEMORY / IPC / PUBLICATION:     REJECT
DEADLINES / DRIVER / PLATFORM:         REJECT
V12B SELFTEST_BOOTSTRAP GHA:           FORBIDDEN
PRODUCTION / RESUME:                   FORBIDDEN
ACTUAL A0 COMMON + CHECKER:             remains 0/1
LIFT / FAKE / IHARA:                   NONE

TASK376_R07_A0_V12B_CODE_PERFORMANCE_REAUDIT_V1
