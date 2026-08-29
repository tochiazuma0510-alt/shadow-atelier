# Task383 reply — A4/v9 exact trace repair and pinned rows-1--7 driver

## Decision

COMPLETE as a bounded static implementation.  The sole row-4 contradiction is
repaired independently in the producer and checker, the other six routes and
all non-trace Task379 clauses are byte-for-byte retained, and the v9 driver is
complete for a later fresh independent static audit.  Nothing was executed.

The scope remains candidate-only rows 1--7.  Rows 8--48, a full A4 selftest,
an A4 basis, lift, fake, and Ihara conclusions remain outside this tranche.

## Final physical identities

| output | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v7.py` | 102,958 | 969 | `4f7f57150892e354f3398c33e0f72c0d968c7101de05b7ce7e5690b47fcd064c` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v6.py` | 100,648 | 761 | `7cf5468be847c3a49014986e39af9bb71120af6371aec05e23bb9789bb22c6c1` |
| `search/d972_r07_a4_actual_owner_trace_gha_driver_v9.g` | 72,604 | 1,202 | `130a6e838f648d58a81854eb74dc8476aa4f1d70dc4d6bfc0a5a81a3e3e68155` |

All three code owners are ASCII, BOM-free, CR-free, and end in exactly one LF.
The closed physical bytes/SHA-256 of this reply are supplied in the enclosing
handoff: embedding a file's own physical SHA-256 in that same file is
self-referential.  That handoff is the exact fourth output identity.

The driver pins the repaired owners at D:79--80 and the unchanged fixture at
D:81--82.  Here and below P means the v7 producer, C the v6 checker, and D the
v9 driver.

## Exact forward and reverse deltas

Producer forward delta from the frozen v6 owner:

- P:2 changes only the truthful header `Task378/v6` to `Task383/v7`.
- P:29 changes only the result schema `/v6` to `/v7`; P:30 keeps the frozen
  fixture schema `/v5/authority-fixture/v5`.
- Frozen P-v6:862 is replaced by P:862--870.  The new lines construct the
  rejection-validator subsequence and final event, apply the row-4 predicate,
  apply the other-six predicate, and feed those Booleans into the otherwise
  unchanged fixture/terminal check.
- Physical forward delta is +807 bytes and +8 lines: 102,151/961 becomes
  102,958/969.

The in-memory reverse delta restored P:2 and P:29, replaced P:862--870 by the
exact frozen P-v6:862, and recovered exactly 102,151 bytes with SHA-256
`6bbae63e284e055bba2097696f0202645bc38ec9856815af9c1857ecd2131a58`.
Byte equality with the frozen v6 file was true.

Checker forward delta from the frozen v5 owner:

- C:2 changes only the truthful header `Task373/v5` to `Task383/v6`.
- C:27 changes only the result schema `/v5` to `/v6`.
- C:28 names the still-frozen v5 fixture schema explicitly; C:508 uses that
  constant so changing the result schema cannot relabel the fixture.
- Frozen C-v5:664 is replaced by C:665--673 with a separately written checker
  predicate and checker-owned journal events.
- Physical forward delta is +866 bytes and +9 lines: 99,782/752 becomes
  100,648/761.

The in-memory reverse delta restored C:2 and C:27, removed C:28, restored the
frozen C-v5:507 fixture expression, and replaced C:665--673 by exact frozen
C-v5:664.  It recovered exactly 99,782 bytes with SHA-256
`33b7905fb1f00b23b8e30c8b90b57a793cabf62ed272fb258790d3c88ba34165`.
Byte equality with the frozen v5 file was true.

Thus every byte outside the truthful labels, the necessary frozen-fixture
schema decoupling, and the one trace predicate is inherited from the frozen
Task379 owners.  No Task379 non-trace PASS clause was reimplemented or
weakened.

## Row-4 and other-six trace proof

Producer P:862 filters only entries equal to the actual rejection validator.
P:864 selects `resolved_path_traversal`; P:865 requires exactly
`[("transport","manifest.path"),("transport","receipt.path")]` in order.
P:866 requires the final event to have the same rejection validator and stage
and owner `receipt.path`.  P:867--869 separately require exactly one rejection
validator and the final validator/stage for every other mutation.  P:870 keeps
the exact owner, identity kind, logical path, ordinary validator, stage, first
rejection, allowed reseals, and terminal-count checks.  Existing owner-change,
cleanup, disposal and post-revalidation code remains outside and unchanged.

Checker C:665 independently filters its own journal.  C:667--669 require the
same exact ordered two-admission row-4 subsequence and receipt-path terminal
event using checker validator strings.  C:670--672 retain the exact-once and
final-validator/stage rule for the other six.  C:673 retains the frozen fixture
and terminal checks; the independent checker route, cleanup and revalidation
remain unchanged.

The driver independently reconstructs all seven ordered event lists at
D:628--693.  D:853--857 requires the exact row-4 two-entry subsequence and
terminal receipt-path event; D:858--859 requires exact-once plus final
validator/stage for each other row.  It also requires the exact entered list
and event digest at D:848--852.  The missing outside path has its truthful
after-identity projection at D:770--795: before is a regular path, after is the
registered-stage unreadable/missing path, and neither state is silently
treated as a readable file.

## Frozen authority and route gates

- D:69--86 fixes all source/fixture/receipt/manifest paths, repaired source
  pins, fixture bytes/hash/body seal, and truthful v7/v6 result schemas.
- D:186--208 rejects absolute/escaping/backslash paths and opens every
  component and leaf no-follow.  D:210--250 binds output directories by
  stable device/inode/type/link identity while correctly permitting their own
  file-content metadata to change.
- D:252--309 binds regular single-link owners, retains file and parent fds,
  re-walks the current no-follow path, streams the hash, and detects identity,
  path, or byte mutation on every revalidation.
- D:312--334 bounds, canonically decodes, and recomputes fixture/task198 body
  seals.  D:973--1003 admits the repaired sources, fixture, driver, exact
  task198 receipt/manifest paths and fixture-derived identities; D:998 rejects
  duplicate logical or physical owners.  D:1006--1027 revalidates all retained
  owners before and after each candidate route.
- Producer and checker are separate fixed subprocesses.  The checker receives
  only its fixed fixture argument; producer output is never passed to it.
  Producer DOM release is D:1017--1020, before checker construction.

The future fixed commands are exactly:

```text
python3 -B 'search/d972_r07_a4_actual_owner_trace_producer_v7.py' --fixture 'search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json'
python3 -B 'crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v6.py' --fixture 'search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v5_20260829.json'
```

They occur as auditable quoted GAP strings at D:49--50 and exact Python argv
plus quoted-text identities at D:75--78.  D:550--609 rejects `--output`, checks
the fixed command, starts one child, keeps stdout/stderr separate, applies
bounds while streaming, requires status exactly zero, and accepts exactly one
complete logical stdout JSON document.  The current sources omit a terminator;
D:518--548 adds the sole framing LF, while rejecting partial, CR/BOM, extra-line
or over-bound output.  Main has exactly one producer call at D:1010 and one
checker call at D:1025, in that order.

## Independent canonical result admission

D:916--939 independently bounds and reads each physical stdout owner, requires
compact ASCII canonical JSON plus one LF, recomputes the root body seal after
removing only `self_digest_sha256`, and only then validates the result.
D:822--869 requires the exact root schema/scope, immutable baseline pins,
seven mutation IDs in order, exact fixture owner/reason/reseal data, event
lists/digests, terminal/disposal evidence, before/after identities,
revalidation transcripts and resource snapshots.  D:756--821 gives the exact
snapshot, identity and public-resource formula checks.

D:871--915 normalizes only a leading producer/checker validator or reason
prefix and the already-admitted truthful v7/v6 root schema.  It compensates
only the measured canonical-byte effect of each mutation event prefix and
recomputes normalized event digests.  The complete remaining result projection
is compared at D:1028--1030; no producer value enters the checker route.
Producer and checker self seals and physical result hashes remain independently
recorded at D:1092--1097.

Required scope is enforced at D:829 and repeated in the durable sentinel at
D:1045--1055:

```text
candidate_only=true
synthetic=false
covered_rows=[1,2,3,4,5,6,7]
remaining_rows=[8,9,...,48]
full_a4_selftest=false
actual_a4_numerator=false
```

## Resource and deadline boundary

- D:102--114 fixes 1 MiB streaming chunks, 35,000,000-byte candidate JSON
  payloads (35,000,001 with LF), 1,000,000-byte stderr logs, 8,000,000-byte
  projections, requested parent RLIMIT_AS 1,200,000,000, child CPU 3600/3610
  seconds, external wall 3900 seconds, two 30-second stop waits, 260 seconds
  cleanup margin, and 9000 seconds global wall.
- D:944--955 installs and reads back the hard parent RLIMIT_AS before authority
  material, rejecting an existing effective ceiling below 800,000,000.
  D:497--500 installs the child CPU limit; each candidate independently installs
  and reports its 700,000,000-byte soft RLIMIT_AS, admitted at D:814.
- External 3900 is 290 seconds above the hard child CPU limit.  D:550--559
  requires before each start enough time for all remaining candidates, two stop
  waits apiece, and cleanup.  The full formula recorded at D:1071--1080 is
  `2*(3900+2*30)+260 = 8180 < 9000`.
- All authority/result hashes are streamed; stdout/stderr caps are enforced
  before writes.  Global SIGALRM plus explicit `deadline` checks cover hashing,
  subprocess polling, bounded reads, canonical projection, copy, publication,
  revalidation and terminal emission.
- D:1081--1090 records the maximum simultaneous explicit-byte formula
  `max(2*31017244+1048576+8489+2722,
  2*35000001+2*8000000+1048576) = 87,048,578`.
  Only one result DOM is live: producer DOM is cleared before checker DOM;
  candidates are serial.  Parsed-container/interpreter overhead is governed by
  RLIMIT_AS, not mislabeled as observed RSS; `rss_observed=false` is explicit.

## Stale gate and durable fail-closed publication

- GAP performs native directory creation and an initial reject-only stale scan
  at D:22--48.  Invocation-specific final and dotted-temp prefixes and every
  future name are fixed at D:87--101.  Python repeats the scan through bound
  directory fds at D:242--246 and D:971--972 before authority work.
- D:361--399 pre-registers every exclusive same-directory temp before creation
  and signal-masks the create/register critical section.  D:400--430 uses an
  atomic no-replace hard link, explicitly checks the transient two-link state,
  removes/fsyncs the temp name, restores the one-link identity, streams the
  final hash through a retained fd, and rechecks the bound directory.
- D:431--439 rehashes all visible results/logs/sentinel through retained fds.
  D:440--495 rolls back only names whose retained device/inode is the exact
  transaction owner, fsyncs after final/temp unlink attempts, closes retained
  fds, records rollback errors, and never converts rollback failure to
  acceptance.
- The two raw results, two logs and two admitted copies are published at
  D:1013--1016 and D:1030--1033.  All are rehashed before sentinel construction
  at D:1038--1042.  D:1043--1113 pins driver, repaired sources, frozen fixture,
  task198 authorities, exact commands, result identities, seals, event digests,
  resource boundary and every false conclusion flag.
- D:1114--1128 self-seals, fsyncs and no-replace publishes the accepted
  sentinel, then revalidates every source and every visible output.  Only after
  that durable state does D:1129--1144 construct one canonical terminal JSON,
  close transaction fds, and write it to stdout.
- On any core failure, D:1146--1183 disables acceptance, stops a live process,
  runs rollback before owner/directory fds are closed, and writes diagnostics
  only to stderr.  GAP uses `Process` and checks the actual harness exit status
  at D:1197--1202; unlike `Exec`, a nonzero child cannot be mistaken for a
  leftover sentinel after rollback failure.  There is no fallible GAP
  acceptance gate after a successful Python terminal write.

## Future artifacts

Under `ci/out`:

- `d972_r07_a4_actual_owner_trace_rows1_7_v9.producer.stdout.raw.json`
- `d972_r07_a4_actual_owner_trace_rows1_7_v9.checker.stdout.raw.json`
- `d972_r07_a4_actual_owner_trace_rows1_7_v9.producer.stderr.log`
- `d972_r07_a4_actual_owner_trace_rows1_7_v9.checker.stderr.log`
- `d972_r07_a4_actual_owner_trace_rows1_7_v9.accepted.json`

Under `search/certs`:

- `d972_r07_a4_actual_owner_trace_rows1_7_v9.producer.admitted.json`
- `d972_r07_a4_actual_owner_trace_rows1_7_v9.checker.admitted.json`

No future artifact was created in this task.

## Static-only closure

Only read-only PowerShell text/byte inspection, SHA-256 hashing, and in-memory
reverse-delta comparison were used around the four permitted file writes.
I did not run or compile Python, Node, GAP, either candidate, any mutation,
the driver, GHA/workflows, git, network access, imports, syntax checks,
subprocess tests, or RSS measurement.  No candidate claim was upgraded by
execution.  Commit label `49178d94` was treated only as the frozen commission
label because git use was expressly forbidden.

A4/V9 VERSIONED REPAIRED OWNERS:          COMPLETE
ROW4 TWO-ADMISSION TRACE:                 REPAIRED
OTHER SIX FIRST-REJECTION TRACES:         RETAINED
TASK379 NON-TRACE PASS CLAUSES:            RETAINED
PINNED ROWS1-7 DRIVER:                     COMPLETE
INDEPENDENT PRODUCER/CHECKER ROUTES:       COMPLETE
CANONICAL RESULT/SELF-SEAL ADMISSION:      COMPLETE
RESOURCE / DEADLINE BOUNDS:                COMPLETE
DURABLE FAIL-CLOSED PUBLICATION:           COMPLETE
CANDIDATE / DRIVER EXECUTION:              UNEXECUTED
FRESH INDEPENDENT STATIC AUDIT:            REQUIRED
ROWS1-7 GHA:                               FORBIDDEN
FULL 48x2 SELFTEST:                        INCOMPLETE
ACTUAL A4:                                 remains 1/3
LIFT / FAKE / IHARA:                       NONE

TASK383_R07_A4_V9_TRACE_REPAIR_AND_PINNED_DRIVER
