# Sol(max) task 337 reply — task325 A0/v6 code/performance audit

Date: 2026-08-29  
Role: Sol(max), independent mathematical/code/performance auditor

## 0. Ruling

**REJECT / UNEXECUTED.**  No Python, Node, GAP, GHA/workflow, network, or git
operation was run.  I read the commissioned files and source text, recomputed
bytes/SHA-256 read-only, and made one read-only sparse extraction from the
exact pinned ZIP member.  That extraction is not an execution of either
producer or checker, is not a second-implementation cross-check, and is not a
Lean certificate.

The first production failure is already deterministic:

1. the v6 driver supplies `--seconds 19800` (driver line 131);
2. the authenticated checkpoint has
   `monitor.limits.wall_seconds == 10800.0`; and
3. after one complete 2,896-column rank-zero insertion, cached-v3 compares the
   two complete limit dictionaries and returns
   `UNKNOWN_INPUT:resume:monitor_limits` (cached-v3 lines 1770--1784,
   2398--2417).

Consequently the live v1 runtime, the second provenance/rank replay, the v6
persistent pool, and the first parallel boundary epoch are unreachable in the
literal v6 production command.  The driver can nevertheless accept that
nonpositive terminal and write its PASS sentinel.  Three further independent
rejection classes survive the minimal hypothetical `19800 -> 10800` repair:

- the pool is installed only after a second 2,896-column insertion and the
  eager 1,469,664-state Q0 construction;
- positive sidecar binding is symlink/TOCTOU-open and the advertised compact
  view copies mathematical fields instead of deriving them; and
- the 22+22 mutations are post-hoc synthetic-document tests, not mutations of
  their physical production owners and actual validators.

The A0 numerator remains unchanged.  There is no COMMON result in this audit.

## 1. Complete-input and identity audit

I read AGENTS.md, the whole task337 commission, task325 commission/reply, all
four v6 outputs, the full cached-v3 quartet, task303 and its quartet, task298,
task319/reply319, task321/reply321, v140, v253--v256, v265, the checkpoint ZIP
manifest/member, and the transitive live-v1/task175/task176 sources and
receipts reached by the pinned manifests.  I also read the requested fallback
papers v275 and v276, the Q0-LATE paper v277, the selected-support paper v278,
and the supplied run-boundary audit v279, from first line to last.

### 1.1 v6 quartet

| file | bytes | read-only SHA-256 | result |
|---|---:|---|---|
| `search/d972_r07_normalized_exact_common_word_positive_parallel_v6.py` | 127,376 | `6f06465bc4599f91dee32ecab9624971c33461b12c7d38139684f578ee9d9218` | exact |
| `crosscheck/check_d972_r07_normalized_exact_common_word_positive_parallel_v6.py` | 58,516 | `fe3b83309eaff0531f0154a31a1a7a051171fb6a1ae8a3f706eb672f6659e47c` | exact |
| `search/d972_r07_normalized_exact_common_word_positive_parallel_gha_driver_v6.g` | 10,927 | `862ef3ea41b7683847f29a0cd1ddf7c95da8601c9dfdbabe3cf0cabc9d7898c5` | exact |
| `search/certs/d972_r07_normalized_exact_common_word_positive_parallel_selftest_v6_20260828.json` | 4,102 | `a6ade562478f86fcd986f119f4d349949c7a866332999acb1d9605a039fcb8ad` | exact |

The producer's 23 `SOURCE_PINS`, the checker's 23 `DEPENDENCY_PINS` plus two
`CURRENT_PINS`, and the driver's 25-entry `D325Pins` roster all agree in bytes
and digest with the present files.  Thus no first failure is a stale direct
pin.  In particular, the 22 dependency identities outside the current v6
fixture agree for:

- task325, v140, v253--v256, v265, task319, and task321/reply321;
- all four task303 files and all four cached-v3 files;
- the task298 driver/reply; and
- the staged ZIP and manifest.

I also followed the nested cached-v3/live-v1 manifests.  The live-v1 quartet,
task186 quartet, task190 commission/reply, v156/v157, task179 commission,
v108/v110/v121/v122/v125/v135/v138/v139/v142/v143, task175 and task176
producer/checker/drivers, q3 and joint receipts, and the seedspan/old
arithmetic/joint/v172/g760/PB4/full-d2 sources all have zero byte/digest
mismatches against their literal pins.  This establishes current immutable
identity only; it is not evidence that v6 reached or executed them.

The fallback paper identities I read are:

| paper | bytes | SHA-256 |
|---|---:|---|
| `proof_r07_two_way_basis_checkpoint_resume_v275.md` | 7,662 | `51febdaadcdf9130af4dd0586969f28f533ff3e9d06d883841aa115410dd40ea` |
| `proof_r07_triangular_checkpoint_basis_resume_v276.md` | 5,571 | `5765aec25e08e687841451d3707ba16e0f3e2c6c4d9de6c120e92bdafe071abb` |
| `proof_r07_boundary_first_lazy_runtime_resume_v277.md` | 9,070 | `2539fa530195b7c5fe7035d2261301ed85c471af2df313fd33fb01e96df9a56d` |
| `proof_r07_selected_support_positive_replay_v278.md` | 7,055 | `f9dcb97c86e401bd96a92805b6c31428483d624874388bcc0439d1f7dc2f390b` |
| `audit_r07_task298_six_hour_cancel_no_artifact_v279.md` | 3,844 | `f669705e93a5ad3c84fb94a5b7f8ec4cf3cedd103df1e0b1d78460e9c8b1f5c9` |

The commission supplied commit labels `3d0bc6a0` (v275), `a0b10131`
(v276), `76ca3ce7` (v277), `11298582` (v278), and `930e4508`
(v279/delta87).  I did not inspect git; the table records the file bytes
actually read in this audit.

### 1.2 Exact staged member

The ZIP is 5,001,811 bytes and contains exactly one member,
`d972_r07_normalized_exact_common_word_cached_v3.json.checkpoint.json`, with
compressed size 5,001,577 and exact raw identity

```text
bytes   86,368,039
sha256  c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab
schema  d972-r07-normalized-exact-cached-colgen/v3
```

The raw structural counts are:

```text
rank = columns = retained columns       2,896
boundary columns / correction columns   2,896 / 0
nonnull per-column active_dual           2,881 (columns 16..2896)
stored sparse-row entries                20,354, maximum 12 per row
pivot_ancestry entries                   137,926, maximum 258 per row
monitor boundary_pairs                   3,145,728
progress boundary pair_attempts          3,145,088
discarded attempted suffix of counter    640
current dual support                     1,188
```

All 1,188 current-dual keys are typed `(block,component)=(1,1)`, with
coefficient one.  Across the 2,881 historical active duals there are exactly
786,272 such support entries and no other type; four `(1,1)` descriptors give
`4 * 786,272 = 3,145,088`, the stored completed pair count.  The current clean
restart epoch therefore has exactly `N = 4 * 1,188 = 4,752` pairs, not merely
the generic bound `104 * 1,188 = 123,552`.

## 2. Literal call graph, first failures, and reachability

### 2.1 GAP driver and SELFTEST

The GAP file does execute its emitted shell: it writes/ closes the script at
lines 116--171 and calls `Exec(Concatenation("bash ",D325Shell))` at line 173.
It pins inputs first, rejects the v4--v6 stale-output roster, chooses W=4 when
`nproc >= 4` and W=2 otherwise, runs producer then checker serially, demands
one producer and one checker terminal line, compares their payloads, and
enforces terminal-specific sidecars.

There is nevertheless a literal driver-contract failure: line 169 writes the
sentinel and line 170 subsequently runs `test -s` on it.  The sentinel is not
the final successful shell operation as task337 requires.  GAP then reads it
at lines 174--175.  The minimal repair is to make the already-guarded `printf`
itself the last shell operation; redirection failure already propagates under
`set -e`.

The SELFTEST producer route is statically connected to receipt, checker,
verdict, and sentinel, but its first substantive audit failure is coverage:
all eight advertised case rows are run with W=2 (producer lines 2939--2985),
only the three persistent-epoch jobs are repeated at W=2 and W=4 (lines
2953--3013), and timeout/death/partial faults are W=2 only (lines 2885--2919).
Thus every advertised case is not constructed at both worker counts.  The
tests also use the one-byte additive C17 model, not the live 40-byte E3 and
154-byte E4 codecs or inherited production group objects.

### 2.2 Literal production route: deterministic first stop

The exact route is:

```text
driver line 173 -> emitted bash
  -> v6 main 3100--3121
  -> authenticate_sources
  -> production 1991--2105
  -> _read_resume 1740--1806 (ZIP read/hash/extract/JSON parse)
  -> _seed_counters
  -> load cached-v3 and install the class hook
  -> cached-v3 main
  -> cached-v3 rank_zero_resume_checkpoint 1414--1626
       fresh Echelon.add for all 2,896 columns
  -> resume_over_cap_preflight 1770--1806
       10800.0 != 19800.0
  -> inner UNKNOWN_INPUT:resume:monitor_limits
  -> outer UNKNOWN_INPUT:cached_v3:resume:monitor_limits
  -> v6 checker nonpositive route (zero cached-v3 checker calls)
  -> driver sentinel
```

The hook is registered before cached-v3 starts, but no
`BoundaryDescriptorCache` instance is constructed on this route.  The outer
adapter state reports the `not_started` cleanup branch.  It is therefore
incorrect to treat a green driver sentinel from this command as evidence that
parallel correlation ran.

Even this deterministic early stop is needlessly expensive.  Before noticing
the limit mismatch, cached-v3 parses all columns, inserts them into a fresh
`Echelon`, reduces the target, and constructs a fresh dual.  Since
`Echelon.add` scans every earlier pivot (live v1 lines 407--423), the insertion
alone makes

```text
2,896 * 2,895 / 2 = 4,191,960
```

pivot probes.  The final target reduction plus exact-dual construction adds
four full 2,896-pivot passes, so the literal mismatch route performs
4,203,544 pivot-loop visits before its typed stop, apart from sparse
combinations and JSON work.

### 2.3 Minimal hypothetical `--seconds 10800` repair

Changing only the seconds value removes the first stop, as task298 already
documented.  It does not make the pool an early owner.  The next literal
prefix is:

1. cached-v3 first rank-zero replay: 2,896 stored rows into a fresh echelon;
2. `v1.main`: authenticate all nested inputs and call `build_runtime`;
3. `build_runtime` reconstructs task175/task176, enumerates all 1,469,664 Q0
   states, builds ten stores, scans memberships, and constructs emitted data
   (live v1 lines 454--580, especially 544--569);
4. patched `PositiveSearch.__init__` calls the original constructor first
   (cached-v3 lines 2107--2109); the original v1 loader reconstructs every
   boundary row from literal `(block,relator,translation)` provenance and
   inserts all 2,896 rows into a second fresh echelon (v1 lines 1389--1451);
5. only after that original constructor returns does cached-v3 construct
   `BoundaryDescriptorCache` (lines 2161--2163); the v6 subclass then starts
   `PersistentProcessRoster` (v6 lines 1637--1645).

Thus the producer performs two complete 2,896-column echelon insertions before
the pool.  Their insertion loops alone are 8,383,920 pivot probes.  Including
the two final target/dual derivations gives 8,407,088 pivot-loop visits.  The
first pass trusts authenticated stored sparse rows; the second pass additionally
recomputes all 2,896 translated-boundary rows from provenance.  Both target
remainder and exact dual are also derived twice.

V278 shows that this second all-column direct provenance replay is not a
mathematical prerequisite for a strictly positive-only speculative search:
formal ancestry may propose a basis, provided a COMMON candidate is accepted
only after direct replay of every selected support row and the complete target
identity.  V6 makes the stronger exact-resume/path-style startup claim and
pays the full 2,896-row replay even though its final authority is positive
only.

The 86,368,039-byte JSON is parsed by v6 `_read_resume`, parsed again by
cached-v3, converted and serialized, parsed by v1 `load_checkpoint`, and then
parsed once more by the cached-v3 post-original-init wrapper (cached-v3 line
2115).  This is two full parses of the raw checkpoint plus two full parses of
the comparably sized converted checkpoint, before considering later receipt
or checker reads.

There is also a checkpoint reachability defect in this prefix.  In v1 main,
`search` remains `None` until the entire `PositiveSearch(...)` constructor
returns (v1 lines 2310--2316).  A `ResourceStop` in eager Q0 construction or
inside the second resume replay therefore produces an inner resource receipt
without a checkpoint (lines 2320--2329).  Cached-v3 then requires a resource
checkpoint unconditionally and hard-stops at lines 2431--2434.  No v6 outer
receipt/checkpoint follows.  The expensive pre-pool prefix is consequently
not only serial but non-resumable through the advertised outer transport.

If the constructor completes, the first restarted frozen-dual epoch is the
exact 4,752-pair epoch stated above.  A successful epoch may then add a rank
column and continue serially; a resource stop after a completed constructor
can flow through v1 checkpoint -> cached-v3 checkpoint -> v6 bound checkpoint.

### 2.4 Hypothetical COMMON and physical checker

For a hypothetical inner cached-v3 COMMON, v6 writes one physical sibling
`*.inner_v3.json`, records its path/bytes/SHA/self digest/schema/terminal/pins,
and omits a checkpoint.  The v6 checker invokes the exact pinned cached-v3
checker once via `subprocess.run` (checker lines 494--513), requires return
code zero, empty stderr, and exactly the sole full PASS line, then constructs
its compact view.  Nonpositive and SELFTEST routes make zero such calls.

However, “one physical cached-v3 checker call” does not mean “one column
replay.”  Inside that one call, cached-v3 `full_independent_production` first
calls the live independent helper's `replay_columns` at lines 2537--2578 to
manufacture a temporary COMMON checkpoint.  It then calls
`checker.validate_common` at line 2636, whose line 974 calls
`replay_columns` again.  Therefore:

```text
producer before pool                    two 2,896-column replays
one physical cached-v3 checker call     two further 2,896-column replays
successful end-to-end COMMON path       four complete replays
```

Each independent checker replay calls `basis.dual(target)` at every one of
the 2,881 active-dual gates.  The exact sum of then-existing ranks is
4,191,855.  A successful `RowSpace.dual` makes one forward reduction, one
reverse pivot pass, and one annihilation pass, so each checker replay has
12,575,565 active-dual pivot-row visits plus 4,191,960 insertion probes and a
final 2,896-pivot target reduction: 16,770,421 pivot-loop visits.  The two
checker replays total 33,540,842; producer plus checker total at least
41,947,930 such loop iterations, before provenance/group arithmetic and sparse
row-entry scans.  This duplication is a material performance owner, not
boundary-correlation work.

### 2.5 Malformed/fault routes

| route | literal first handling | audit result |
|---|---|---|
| malformed/traversing output | `_fresh_relative` runs before v6 main's `try` (3100--3104) | uncaught `InputStop`, no typed receipt |
| malformed resume path/ZIP/UTF-8/JSON | generally caught by main's narrow input tuple (3112--3116) | sealed UNKNOWN_INPUT when the exception is in that tuple |
| semantic `require` failure | raises `ProtocolError`, which main does not catch | hard nonzero stop; fail-closed but no typed receipt |
| live timeout | parent `connection.wait` deadline -> cancel -> force close -> `ResourceStop` | no partial commit, but blocking request sends have no deadline |
| worker death/EOF | `is_alive`, EOF, or send failure -> force close | last published shared attempt count charged; no partial commit |
| partial result | `complete is True` gate fails during merge | converted to `ParallelResource(merge_protocol)`, cleanup, no commit |
| startup failure after some forks | constructor wraps start/ready in `except BaseException: _fail_cleanup()` (872--890) | partial starts are cleaned; no registry-leak finding |

The timeout fault worker ignores the transmitted `deadline_ns` and waits up to
60 seconds; only the parent owns the deadline.  Normal waiting is event-driven
and has no polling sleep, but `Connection.send_bytes` and full-frame
`recv_bytes` themselves are blocking and have no per-operation deadline.  A
live child that stops draining a pipe can prevent the parent from reaching its
deadline/cleanup logic.

## 3. Conditional mathematical equivalence of the v6 correlation owner

Subject to actually reaching the hook, the parallel correlation arithmetic is
equivalent to cached-v3's `BoundaryDescriptorCache.correlation` on the present
immutable runtime.  I found no row/hash substitution in this kernel.

- Cached-v3 builds and sorts descriptors by
  `(block, relator_index, component, h_blob, base_coefficient)` (lines
  955--972).  v6 preserves that tuple order in `_production_roster` (1606--1629).
- Cached-v3 iterates the sparse dual dictionary in insertion order, filters
  `R` keys, and appends support by typed `(block,component)` (1023--1031).
  v6 `_production_support` does the same; the actual dual is canonical F3 and
  dictionary keys are unique.  `_encode_support` rejects any duplicate typed
  `(block,component,blob)` and accepts only coefficients 1 or 2.
- The flattened prefix is exactly the sum of matching typed support lengths.
  With `A=min(N,W)`, intervals
  `[iN/A,(i+1)N/A)` are disjoint, contiguous, and complete, including N=0 and
  N<W.  The parent rechecks the observed ordered cover.
- Each worker computes the actual quotient product `t=g*h_inverse`, checks
  `t*h=g`, and accumulates the full key `(block,relator,t_blob)` over F3.
  Zero deletion is equivalent to cached-v3's later nonzero filter.
- Shard merge is ordered by worker id but F3 addition is commutative.  The
  winner order `(block,t_blob,relator)` exactly matches cached-v3 lines
  1058--1059.
- After selection, the parent independently rescans the selected relator's
  descriptors/support to reconstruct all contributing pairs, calls the
  inherited exact `translated` row builder, and directly checks
  `pair(dual,row)` against the merged scalar (v6 lines 1671--1698).  It returns
  that sparse row, not a digest, endpoint, or hash tuple.
- `run_epoch` is synchronous and the cached-v3 owner calls one correlation per
  live dual.  A rank/dual epoch cannot overlap the next one; no failed partial
  accumulator is returned or serialized.

The worker's `local_provenance` contents are not validated—only its nullness is
checked at lines 1387--1389—but that field is not used for the final receipt:
the parent reconstructs the selected contributors afresh.  It is therefore
not a mathematical gap in the returned row, although SELFTEST claims about
mutating worker provenance do not exercise the live owner.

The hook timing is semantically correct only after the repaired resume prefix:
v6 replaces the cached-v3 global class before cached-v3 installs its runtime,
and the live constructor eventually resolves that replacement.  In the
literal 19800 command it is unreachable, and under 10800 it is too late to
accelerate either resume insertion or Q0.

## 4. Processes, atomic resume, resources, and present-shape cost

### 4.1 Fork/process lifecycle

The code requires `sys.platform == "linux"`, obtains
`multiprocessing.get_context("fork")`, and checks its start method.  One daemon
roster is reused across serial epochs.  Workers read the fork-inherited
runtime/groups and mutate only their private accumulator, their own shared
counter slot, and pipe/event state.  The inspected graph has no deliberately
shared mutable group object and the ZIP/file reads are closed before pool
construction; the redirected `StringIO` is inherited but unused by workers.
This is a plausible read-only fork use, not a general fork-safety proof for
all imported third-party Python objects.

Startup exceptions are cleanup-guarded.  Normal production also calls
`registry.close_all` in a `finally` (v6 lines 2021--2025).  Close sends
shutdown/awaits `bye`, joins, terminates survivors, joins again, closes all
parent connections, records exit codes and rejects any nonempty final PID
roster (999--1056).  Thus I retract the potential constructor-leak hypothesis:
the literal constructor has an exception guard.  Remaining lifecycle defects
are:

- force close can spend up to roughly `2*W*SHUTDOWN_SECONDS` across two serial
  join rounds before rejecting a survivor;
- it never calls `multiprocessing.Process.close()` after reaping; and
- an unbounded blocking pipe send can prevent entry into this bounded cleanup.

### 4.2 Counters and atomic state

The seeded exact counters are:

```text
attempted_pairs  = 3,145,728
committed_pairs  = 3,145,088
discarded_pairs  =       640
retried_pairs    =         0
attempted_epochs =     2,882
committed_epochs =     2,881
discarded_epochs =         1
retry_pending    =       640
```

Both conservation equations hold.  The 640 are the attempted tail of the
cumulative monitor after the current dual's clean starting counter; because
the cached-v3/v6 pair order agrees, restarting the 4,752-pair epoch at zero
repeats those first 640 positions and then completes the epoch.  On success
the literal update is:

```text
attempted_pairs  3,150,480
committed_pairs  3,149,840
discarded_pairs        640
retried_pairs           640
retry_pending             0
```

On a failure after x published pair attempts, attempted and discarded both
increase by x and the full N-pair atomic epoch becomes pending.  No partial
accumulator commits.  One limitation is semantic: after such a partial v6
failure, `retry_pending_pairs=max(N,old)` causes the next full epoch to count
all N as “retried,” including pair positions the failed try may not have
reached.  Conservation remains true, but `retried_pairs` is an epoch-restart
charge, not an exact count of duplicated physical pair evaluations.  The
schema must not claim the latter.

Progress/result frames are charged by deltas, and after a failure the parent
joins/terminates before charging `shared_attempted - already_charged`; I found
no literal normal-path double charge.  A hard death can occur after arithmetic
and accumulator mutation but before the worker publishes its next shared
counter value, so “exact attempted” is exact only to the last published
logical pair, not to every CPU/group operation that may already have happened.

The epoch chain hashes the prior chain plus the full latest epoch record and
retains only that last record.  A v6 resource checkpoint carries counters,
chain, last record, source binding, and a clean cursor with no partial
accumulator; the immutable roster is reconstructed from pinned runtime data.
This is sufficient for atomic full-epoch restart, not historical replay.
COMMON correctly forbids the checkpoint reference and both producer/checker
reject an orphan checkpoint sidecar.

Checkpoint byte accounting is unnecessarily expensive: `_bind_checkpoint_bytes`
deep-copies the whole roughly 86 MB object, reseals and canonicalizes it until
a fixed point, with up to 12 full passes, and checks the 4 GB cap only after
materialization (lines 1821--1853).  Failure to converge raises uncaught
`ProtocolError`, so this route hard-stops rather than yielding a typed
resource receipt.

### 4.3 RSS and frame truth

The claimed aggregate peak RSS is not exact:

- `_sample_rss` reads a child from `/proc` only while that child's cached
  sample is zero; later values arrive only in progress/result frames, so
  samples are stale and nonsimultaneous;
- fork-shared pages are counted once in every process RSS, so their sum is not
  unique physical memory;
- with the present 1,188/2,376-pair shards and progress granularity 4,096,
  there are no mid-epoch progress frames at W=4 or W=2, hence no mid-epoch
  child peak sample; and
- `pickle.dumps` allocates the complete frame before the 32 MiB cap is checked.

Thus `aggregate_parent_children_rss` is a sampled upper-style sum of per-process
RSS, not an exact peak.  A v7 claim must use a declared sampled metric or a
cgroup/PSS owner and must measure serialization allocation itself.

Every request/result/progress frame is pickled.  The per-frame 32 MiB and
per-epoch 256 MiB checks are fail-closed, but the epoch cap is checked after
traffic and allocations occur.  A worst-case shard accumulator has O(n_i)
distinct full keys and its list form plus pickle is another O(n_i) copy.

### 4.4 Exact current overhead and symbolic bounds

For the current first epoch, support encoding is exactly

```text
4 + 1,188 * (9 + 40) = 58,216 bytes.
```

The parent encodes and decodes it once; each active worker receives and
decodes the whole buffer.  Therefore W=2 sends at least 116,432 support bytes
and performs `(2+1)*1,188 = 3,564` element unpacks; W=4 sends at least 232,864
and performs `(4+1)*1,188 = 5,940`, before pickle/frame overhead.  Parent plus
workers make 312 descriptor visits at W=2 or 520 at W=4 for prefix
construction, and every worker also republishes/rehashes the 104-descriptor
roster each epoch.  A shared `lock=False` 64-bit slot is written once per pair,
which adds per-pair shared-memory/cache-line traffic.

Source authentication is also repeated by layers rather than sharing one
immutable byte snapshot: v6 reads its full pin roster, cached-v3 authenticates
its live bundle, v1 authenticates its own transitive inputs, and the independent
checker repeats its manifests.  The producer loads cached-v3/v1 in-process
and then forks W workers; the outer checker launches exactly one cached-v3
checker subprocess, which rebuilds the independent runtime.  There is no
normal polling sleep, but there are repeated source reads/hashes and the
explicit 60-second timeout-fault wait.

In general, with D descriptors, S dual support records, and
`N=sum_d |S_(block(d),component(d))| <= D*S`, v6 spends

```text
support traffic     A copies, A=min(N,W)
decode/index work   O((A+1)S + (A+1)D)
group arithmetic    exactly N pair products/checks
worker+merge memory O(N) worst case
winner replay       another descriptor/support scan plus exact row build
```

per epoch.  The support cap is only a byte cap
`4 + sum(9+blob_length) <= 1,048,576`; it is not an efficiency bound.  The
present 4,752 arithmetic pairs are small enough that repeated support codecs,
descriptor scans, hashes, fork-RSS sampling, accumulator list conversion, and
pickling can be material.  These costs are not removed work.

### 4.5 Relation to run 33163964747

Task298 run 33163964747 uses the same cached-v3 resume firewall with the
correct `--seconds 10800` and a fresh wall clock.  Static call-graph identity
shows that it owns the same first rank-zero insertion, eager Q0/runtime build,
and second provenance insertion before boundary correlation.  v6 would repeat
that entire unaccelerated prefix before starting its pool.  No conclusion
about that run was inferred from source or from an execution by this auditor;
the strict static point is that parallel correlation cannot shorten work that
precedes its constructor, and a resource stop there is currently
non-resumable.

After the static audit, the parent supplied v279's separate public-run record:
run 33163964747 was cancelled at the six-hour job limit with zero artifacts.
Its producer printed the candidate
`UNKNOWN_RESOURCE:phase=positive_boundary_correlation:cap=wall_seconds:value=10803.370851337:limit=10800.0`;
the mandatory cached-v3 checker then emitted no terminal for nearly the
remaining three hours, and cancellation killed an orphan `python3`.  There is
no checker PASS, driver sentinel, recoverable checkpoint, accepted UNKNOWN, or
COMMON.  This supplied observation is consistent with, but not a substitute
for, the static diagnosis and does not change `EXECUTION: UNEXECUTED` for this
task337 audit.

It also isolates a second unnecessary full-runtime path in the old task298
driver: checking a nonpositive resource transport rebuilt the heavy runtime.
V6's outer checker correctly makes zero cached-v3 checker calls on nonpositive
terminals; v7 must preserve and strengthen that split.  UNKNOWN_INPUT and
UNKNOWN_RESOURCE checking should be bounded to seal/path/bytes/source/counter/
checkpoint/claim integrity and must not enumerate Q0, replay all columns, or
run the positive mathematical checker.

## 5. Positive authority and checker independence

The checker is a separate stdlib implementation and does not import v6
producer code.  It authenticates its pinned cached-v3 checker, invokes it
exactly once only for COMMON, and requires rc=0, empty stderr and the sole
exact PASS line.  These are good controls.  The following independent positive
authority requirements nevertheless fail.

1. **Symlink/alias not excluded.**  `Path.is_file()` at checker line 477
   follows symlinks.  There is no `lstat`, `is_symlink`, inode/device, or
   hard-link policy for the physical inner sibling.  Exact path text and
   digest do not exclude a symlink at that pathname.
2. **TOCTOU.**  `read_bound_json` hashes/parses bytes A, then the cached-v3
   subprocess reopens the pathname and can see bytes B; after it returns the
   outer checker derives its compact view from the already-parsed A and never
   reopens/re-hashes the physical sidecar.  The path can then contain C.  The
   accepted checker result is not bound to one immutable open object.
3. **Compact view is copying, not derivation.**  Checker lines 426--461 copy
   `correction_word`, solution coefficients, exact words, registered relators,
   exponents, A/B, `joint_kernel_replay`, `exact_direct_replay`, ancestry
   fields, and `boundary_words_not_inserted`.  `typed_boundary_ancestry`
   decorates copied receipt fields; it does not recompute their word/Fox/group
   equalities.  Equality with the producer's equally copied view is not an
   independent mathematical replay.
4. **Impossible COMMON adapter state accepted.**  `validate_cleanup` permits
   `['not_started']` by default, including positive validation.  An actual
   reachable COMMON through the v6 hook necessarily constructed and closed a
   pool.  Because the outer self seal is unkeyed, a valid inner COMMON can be
   wrapped with resealed `not_started` telemetry and still pass this gate.

The physical cached-v3 checker does perform substantial independent
mathematics, but task337 specifically requires the outer physical binding and
compact claimed fields themselves to be independent and immutable.  The
above gaps therefore remain fatal.  The internal duplicate `replay_columns`
calls described in section 2.4 are also unnecessary checker delay.

## 6. SELFTEST and all 22 mutation owners

The real-process C17 kernel cases do demonstrate fork construction, empty and
short rosters, cancellation, lexicographic selection, reuse, timeout, death,
partial return, and cleanup in a toy group.  They do not meet the commissioned
owner/coverage standard for the reasons in section 2.1.

All producer mutations are applied after real runs have been summarized into
the synthetic `document` at lines 3022--3033.  The checker independently
recreates and mutates a similar synthetic document; it does not merely trust
the producer's effect list.  That is better than a copied `mutation_ok=true`,
but neither side routes the mutation through the physical production owner
named by the test.  The per-control ruling is:

| # | mutation | production-shaped physical owner / actual validator? | ruling |
|---:|---|---|---|
| 1 | `wrong_dual_digest` | mutated C17 run dict, not live request/result frame | FAIL |
| 2 | `noncanonical_c17_alias` | synthetic one-byte codec dict, not E3/E4 ABI | FAIL |
| 3 | `missing_interval` | summarized interval list, not a physical shard omission | FAIL |
| 4 | `overlapping_interval` | summarized interval list, not a physical shard overlap | FAIL |
| 5 | `changed_accumulator` | post-hoc accumulator with refreshed local digest | FAIL |
| 6 | `changed_winner_provenance` | post-hoc local provenance; live parent ignores its contents | FAIL |
| 7 | `changed_direct_scalar` | synthetic C17 scalar, not live translated row/pair owner | FAIL |
| 8 | `cross_epoch_result` | synthetic epoch field, not a stale pipe frame | FAIL |
| 9 | `partial_return_accepted` | synthetic completion flag, not actual partial worker return | FAIL |
| 10 | `child_left_alive` | cleanup dictionary only; no child is deliberately left alive | FAIL |
| 11 | `counter_reset` | counter dictionary only; no physical resume checkpoint | FAIL |
| 12 | `unbound_checkpoint` | embedded synthetic reference; no sidecar bytes/path/fixed point | FAIL |
| 13 | `changed_inner_receipt_digest` | synthetic embedded bytes/reference, no physical sibling | FAIL |
| 14 | `fake_v3_checker_terminal` | stored string; it never launches the cached-v3 checker | FAIL |
| 15 | `compact_view_mismatch` | synthetic copied compact dict, no mathematical replay | FAIL |
| 16 | `positive_claim_on_resource_exit` | resealed synthetic resource envelope | FAIL |
| 17 | `separator_flip` | resealed synthetic claim vector | FAIL |
| 18 | `cofinal_flip` | resealed synthetic claim vector | FAIL |
| 19 | `fake_flip` | resealed synthetic claim vector | FAIL |
| 20 | `ihara_flip` | resealed synthetic claim vector | FAIL |
| 21 | `terminal_reseal` | resealed synthetic envelope, not driver/physical sidecars | FAIL |
| 22 | `stale_output` | toggles a synthetic `output_fresh` field, not an `xb` filesystem race | FAIL |

The narrow synthetic validators may reject each mutation at the registered
stage/reason, but task337 explicitly says same-shaped dictionaries, explicit
raises, digest changes, and broad catches are insufficient.  Fault control is
also broad at producer lines 2904--2909: any `ParallelResource` is recorded as
rejection before the document validator later examines its reason.  Hence the
advertised 22/22 producer and 22/22 checker mutation counts do not establish
the physical controls claimed.

## 7. v275/v276/v277/v278 and the smallest versioned repair

### 7.1 v275 is sound but not the minimal present artifact

V275's two-way P/A/B certificate is a sound history-free way to avoid serial
insertion: direct checks of `P=A*C` and `C=B*P` establish span equality, after
which target and dual are rebuilt and only final positive membership is
authoritative.  V275 itself correctly says that the current P/A/B package was
not constructed and that no wall-time gain follows without measuring its
sparsity.  It also permits a different basis/path, so it does not alone prove
exact cached-v3 byte-path parity.  As a drop-in repair to v6 it is incomplete:
it does not split eager Q0, reconstruct current typed provenance, or bind the
physical positive checker.

### 7.2 Actual applicability of v276 triangular ancestry

V276 removes the reverse B matrix when the retained-column ancestry matrix A
is lower triangular with nonzero diagonal and the computed rows pass exact
pivot gates.  I assessed those premises directly from the fixed raw checkpoint
bytes without invoking repository code.  For every j I formed the F3 sparse
sum `p_j = sum_i a_ji c_i` from stored canonical sparse rows and ancestry,
then compared it with the stored pivot key and all earlier pivot keys.

| read-only extraction over all 2,896 rows | exact value |
|---|---:|
| ancestry indices outside `1..j` | 0 |
| missing/zero diagonal coefficients | 0 |
| noncanonical ancestry order/F3 coefficient failures | 0 |
| duplicate pivot keys | 0 |
| empty computed pivot rows | 0 |
| computed coefficient at stored pivot not one | 0 |
| computed nonzero at an earlier stored pivot | 0 |
| computed minimum key different from stored pivot | 0 |
| raw sparse support total / max | 20,354 / 12 |
| ancestry coefficient count / max per row | 137,926 / 258 |
| **ancestry-weighted raw-support contributions** | **1,011,460** |
| maximum weighted contributions for one pivot | 1,892 |
| computed pivot support total / max | 289,774 / 522 |

Therefore the immutable current `sparse_row + pivot_ancestry + pivot_hex`
bytes are a concrete sparse candidate satisfying v276's triangular and pivot
shape, and the reverse B of v275 is unnecessary for span equality.  The
1,011,460 contribution count is the relevant static arithmetic size, not the
mere 137,926 ancestry-entry count.  It is materially below one old
4,191,960-probe insertion loop and its rows are independently parallelizable,
although this is not a wall-time claim.

This finding has strict limits:

- the checkpoint does not store full trusted p rows; producer and independent
  checker must each recompute A*C and all gates rather than accept this audit;
- the read-only extraction is a single candidate calculation, not a
  helper-nonshared cross-check;
- all 2,896 raw columns are boundary columns.  An **exact-resume** v276 claim
  must reconstruct all of them from typed translated-relation provenance;
  v278's weaker speculative-positive mode may defer this to the finally
  selected support, but then must not claim the true historical span;
- target remainder and fresh exact dual must still be recomputed;
- triangular span equality does not by itself assert cached-v3 scheduler/path
  parity.  A parity schema must additionally establish the registered
  deterministic Echelon transition/order and same target/dual, or the v7
  terminal must explicitly claim only history-free positive authority.

Thus v276 is applicable to a redesigned v7 loader, but is not an automatic
acceptance of the present checkpoint and is not a one-line v6 patch.

### 7.3 Q0-LATE v277, selected-support v278, and concrete v7 repair

V277 proves the missing phase split for a history-free positive search.  The
target, retained-row provenance, triangular basis, fresh dual, and complete
PB3/PB4 boundary correlation use only the light runtime.  The 1,469,664 Q0
states, ten stores, memberships, adjusted-L data, and singleton-fibre tables
may be postponed until a complete boundary correlation is zero and the
correction oracle is about to be called.  Current v6 does not implement this:
`build_runtime` eagerly pays all heavy work before `PositiveSearch` and before
the pool.

V278 permits a still smaller positive-only authority boundary.  Startup need
not directly reconstruct all 2,896 historical provenances at all.  The pinned
stored sparse rows and v276 triangular arithmetic may drive a basis marked
`heuristic_discovery_only`, while every newly generated row is directly
replayed.  A zero target reduction is only a candidate.  Before COMMON, the
formal ancestry map must be expanded to its nonzero selected checkpoint/new
row support; an independent checker reconstructs exactly those actual rows,
checks their equality with the selected stored rows, checks the complete
sparse target identity, and replays the selected correction words and typed
boundary preimage.  No exact historical span, cached-v3 trajectory, separator,
or negative conclusion may be claimed.  An invalid unselected row can then
only perturb discovery, not pass the final positive gate.

The smallest performance-credible **versioned v7** is therefore:

1. repair the driver to use the checkpoint-bound `--seconds 10800`, make the
   sentinel the final shell operation, and keep A0 claims false on every
   unknown/hard stop;
2. authenticate the existing raw member once, build only v277's light layer,
   check canonical stored rows/ids/ancestry shapes, compute the v276 triangular
   A*C/pivot candidate, and retain a load-bearing sparse formal ancestry DAG;
   in the minimal v278 mode, do **not** direct-replay all 2,896 historical
   boundary provenances at startup and label the state
   `heuristic_discovery_only`;
3. inject the resulting candidate P/order/formal ancestry into a new
   history-free positive owner, recompute the heuristic target remainder and
   dual, and remove both serial producer rank-zero insertions—do not call the
   old converter and old v1 loader in succession;
4. start the persistent boundary pool before any heavy Q0 census and run the
   complete exact correlation; construct Q0 exactly once, metered and
   checkpointable, only immediately before the first correction-oracle call;
5. make pre-pool/light and heavy-construction resource stops produce a real
   bound checkpoint rather than depend on a `PositiveSearch` object whose
   constructor has not returned;
6. remove both checker-wide 2,896-column replays in speculative mode; at a
   COMMON candidate, freeze the selected formal support and have the
   helper-nonshared checker directly reconstruct exactly that support, the
   target, the full sparse equality, correction words, boundary preimage and
   all-seven side gates.  An optional exact-resume mode may instead perform
   the stronger all-column v276/v277 replay, but it is not the minimal A0
   positive path;
7. keep nonpositive checking bounded to physical transport, seal, source,
   counters, sidecar and false-claim gates.  It must make zero positive
   mathematical-checker calls and must not construct Q0 or replay all columns;
   preserve this good v6 split rather than the old task298 full-runtime
   UNKNOWN checker;
8. bind the COMMON sidecar through one immutable physical object (reject
   symlink/hard-link aliases, hold/recheck identity across the subprocess, and
   bind its verdict to the exact digest), and derive every compact field rather
   than copy booleans/scalars;
9. replace all 22 mutation models with physical owner injections, run every
   advertised real-process case/fault at W=2 and W=4 using production E3/E4
   codecs, make pipe deadlines/RSS metrics truthful, and close reaped process
   objects.

A smaller correctness-only patch that merely changes 19800 to 10800 would
still leave the hours-scale serial/non-resumable prelude and cannot authorize a
synthetic SELFTEST.  V275 remains the general fallback if triangular gates
fail; for this exact checkpoint v276 supplies the sparse formal candidate,
v277 removes eager Q0, and v278 removes startup replay of all unselected
provenances while preserving a complete final positive gate.  None changes
the A0 numerator on failure or cap.

## 8. Final decision

The parallel kernel is conditionally mathematically faithful, and all present
file identities agree, but it is unreachable in the literal production
command and arrives after duplicated rank/provenance work and the unnecessary
eager Q0 prelude under the first repair.  Positive transport and SELFTEST
authority also fail independently.  No execution is authorized from this
audit.

AUDIT: REJECT
EXECUTION: UNEXECUTED
SYNTHETIC SELFTEST AUTHORIZED: NO
ACTUAL A0 COMMON + CHECKER: 0/1
LIFT / FAKE / IHARA: NONE

TASK337_R07_TASK325_V6_CODE_PERFORMANCE_AUDIT
