# Luna task 353 - A0/v11 finite audit repair and deterministic SELFTEST bootstrap

Role: Luna, bounded implementation only.  Read this mail and every numbered
prerequisite first to last before editing.  Do not run Python, Node, GAP, GHA,
a workflow, git, or network.  Read-only PowerShell source/byte/hash inspection
is allowed.  Use `apply_patch` for every repository edit.  Preserve every
v1--v10 file and every physical owner.  This task authorizes exactly the six
new outputs in Section 2 and no SELFTEST or production execution.

Task352's frozen verdict is `REJECT / UNEXECUTED`.  This is one versioned v11
repair, not another partial audit loop.  Every defect and unnecessary-work
finding in the full task352 reply is normative even when this mail summarizes
it.  Return `BLOCKED / UNEXECUTED` rather than claiming implementation if any
one item cannot be closed literally and fail-closed.

## 1. Binding prerequisites

Read in full, in order:

1. `sol/luna_task_351_r07_task350_recovery_v2_a0_v10.md` and all six outputs,
   including the complete reply;
2. `sol/sol_reply_352_r07_task351_a0_v10_code_performance_audit_v1.md`;
3. v287, v289 and v290, then v275--v279 and v284;
4. task348/reply348, the accepted task176 receipt/verdict/manifest, recovery-v1
   and recovery-v2;
5. every q3/E3/E4/joint/old/task176 owner pinned by v10.

Recompute the frozen v10 and recovery-v2 identities read-only.  Raw checkpoint
canonical self seal `29bb74f3...fd123` is PASS; do not repeat the withdrawn
LF-based rejection and do not rewrite, reseal or adapt that owner.  All v10
positive, negative and resume routes remain forbidden.

## 2. Sole permitted outputs

Create only:

- `ci/in/d972_r07_history_free_positive_fast_resume_selftest_v11.preregistration.v1.json`;
- `search/d972_r07_history_free_positive_fast_resume_v11.py`;
- `crosscheck/check_d972_r07_history_free_positive_fast_resume_v11.py`;
- `search/d972_r07_history_free_positive_fast_resume_gha_driver_v11.g`;
- `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v11_20260829.json`;
- `sol/luna_reply_353_r07_task352_a0_v11_finite_repair.md`.

The recovery-v2 owner is reused byte-for-byte and is not an output.  V11 may
copy audited sound arithmetic from v10, but must not edit v10 in place.  A
fresh Sol(max) code/soundness/performance PASS is required before any command
or GHA workflow can be commissioned.

## 3. First-stop and deterministic SELFTEST closure

Repair all three literal SELFTEST stops together:

1. `_validate_triangular_subset` must process columns chronologically and
   forbid only `seen_pivots`; a valid P row may contain a future pivot.  Retain
   distinct uniqueness, diagonal, `min(P)=pivot`, coefficient-one and exact P
   equation checks.
2. Every bounded reader receives an explicit meter or explicit no-meter
   policy.  No preflight or mutation path may refer to an unbound `meter`.
3. Pin the new fixture everywhere; no stale v10 fixture identity survives.

Every fixture mutation must reach the same ordinary validator used by the
baseline.  A temporary six-column substitute is insufficient where the
mutation claims a full-owner property.  Baseline and each mutation record one
narrow first rejection.  The SELFTEST main actually calls all suites; no
defined-but-dead checker function and no copied mutation-name list is allowed.

## 4. Noncircular preregistration of receipt and verdict

One source version is possible only with a deterministic bootstrap.  The new
preregistration manifest `P` records the expected paths, exact bytes, physical
SHA-256, self seals and semantic digests of the prospective SELFTEST producer
receipt `R` and independent checker verdict `V`.  `P` itself says
`execution=UNEXECUTED` and does not claim that R or V already exists.

Make R and V completely deterministic.  Time, PID, inode, mtime, RSS, wall
samples and other host telemetry are excluded from R/V and, if retained at
all, go only to a non-load-bearing log already permitted by the driver.  R
binds the complete ordinary-validator ledger, fixture, recovery-v2, frozen
owners and final producer/checker source identities.  V binds R's content
identity and semantic digest, reruns the validators independently, and binds
the same identities.  Construct P without a cryptographic cycle: producer and
checker sources do not hard-code P's physical hash; the final driver pins P,
producer, checker and fixture after those files are fixed.  R/V need not bind
the driver's own SHA.

SELFTEST requires generated R and V to equal P byte-for-byte after their own
self-seal checks.  PRODUCTION requires both exact owners, independently reruns
the same semantic validation, and passes the resulting validated summary into
`Search` and the final COMMON receipt.  Never discard it or construct
`Search(..., None)`.  A self-resealed arbitrary JSON, an R without V, or a
manifest updated after execution is rejected.

If deterministic exact R/V bytes cannot be preregistered before execution,
stop as `BLOCKED / UNEXECUTED`; do not weaken this into a self-declared PASS.

## 5. Q3, Q0, Gamma and codec typing

Implement three separate q3 gates: each literal marked-permutation row is
exactly the set 1..36; convert every entry by `x-1`; then replay Q0 using the
physical convention

```text
mul(left,right)[i] = right[left[i]]
```

and compare the selected 36-byte roster state.  Do not retain the v10
`left[right[i]]` recurrence.

Keep the 970-byte projected ten-coordinate Gamma state distinct from a full
JointGroup diagnostic.  A single quotient `(permutation,pc_bytes)` codec may
never receive `(E3, tuple(31 E4))`.  Either omit the full diagnostic from
acceptance or add a separately typed, bounded, checker-reconstructed codec;
shape or self-hash alone is never load-bearing.  Preserve exact one-based Q0
and Gamma parent grammars, root-to-leaf word order, `record-1` indexing, and
`red(gword+qword)`.

## 6. Exact bounded K0 reconstruction

Replace the checker's per-record Python `dict[bytes,int]` inverse by one
deterministic selected-coordinate cache.  Use a stable, specified hash and an
open-address `array('I')` qid table; a 2^22-slot table is the audited reference
bound.  Pre-cap the retained 40/154-byte state slab plus slots and allocation
overhead before allocation.  Build each selected coordinate at most once and
reuse it for all selected K0 records.

For every Gamma value compute `source=a^-1*t`; lookup absence means skip, not
failure.  After a coarse hit, require retained full 40/154-byte state equality
with `source`, then require `a*source=t`.  A mismatch is skipped.  Compare the
complete authenticated A first-gid table, each gid, sorted order and literal
digest, not only the key set.  Reconstruct Gamma by one-coordinate
chronological recurrence rather than replaying all ten coordinates 243 times.

Accept the authenticated trivial kernels for S5/S6/S7.  For every coordinate
bind canonical kernel state blobs, exact generator words, order, cursor and
selected kernel word.  A missing selected word or cursor is a hard failure;
delete the producer's candidate-zero fallback.  Reconstruct a kernel edge
incrementally rather than replaying the whole word in ten coordinates.
Finally replay the selected word, target, formula scalar, direct H1/H2/P row
and active-dual pairing exactly as v287 requires.

## 7. Heavy identity and final COMMON

Derive `heavy_input_sha256` independently from the physically opened
task176 receipt/verdict/manifests/recovery-v2, q3/E3/E4/joint/raw owners,
selected Q0/Gamma full-state proof, selected-coordinate inverse digest,
kernel BFS, cursor, current dual and code identities.  A copied 64-hex string,
producer Boolean or producer `heavy_public` digest is rejected.

Retain v10's sound selected-support proof: every selected old row is identical
to the opened raw record; every selected new boundary/correction row replays
its direct provenance; formal symbols are one-to-one; coefficient-two inverse,
correction product, eleven/direct all-seven row and final finite sparse zero
are independently recomputed.  Unknown, resource exhaustion and absence of a
COMMON result never imply a separator.

## 8. Checkpoint, DAG and v290 accounting

Repair checkpoint/resume as one authenticated carrier:

- normalize every DAG node recursively by opcode before duplicate detection;
  a literal's inner list must never remain unhashable;
- use the literal `OBJECT_CAPS` checkpoint cap before bytearray/string/JSON
  allocation, read/open/parse once, and never accept a self-consistent but
  externally unpinned portable manifest;
- authenticate and replay each new row's ordinary boundary/correction
  provenance, active dual, scalar, pivot and fixed rebuild canary before
  injecting its node id;
- distinguish heavy logical completion from materialization and checkpoint
  only truthful fields;
- implement v290 exactly: historical completed semantic counters add to the
  present run; restore-validation counters are separate; fresh input/wall
  counters are not overwritten; peaks/gauges compose by maximum; every
  declared semantic counter, including sparse operations, is actually bumped;
- use iterative bounded DAG expansion with reference counts or an equivalent
  no-recursion implementation and no quadratic memo-copy path;
- write and fsync the final receipt and directory before retiring the
  checkpoint; then unlink and fsync the directory.

UNKNOWN_INPUT has no sidecar and a narrow safe reason grammar.  UNKNOWN_RESOURCE
may use only the one pinned, bounded checkpoint; validate Boolean values by
type/value correctly.  Producer and checker have the same compatible receipt
cap, and neither may materialize a 4 GB JSON DOM.

## 9. Required performance repairs

No runtime measurement is requested, but the literal algorithm must remove
task352's unnecessary work:

- add defended outer producer 10,800 s, checker 7,200 s, artifact 3,600 s and
  total 21,600 s deadlines; reject unknown driver modes rather than coercing
  them to production;
- keep light boundary workers alive across heavy construction or fork a
  minimal light-only image before heavy pages exist; stream bounded pair
  slices and retain winner contributors without a second full scan;
- accumulate IPC/STOP bytes, committed epochs and restarts across owner
  transitions, with no busy-loop fault path;
- after a Q0 coarse successor is already known duplicate, do not calculate
  the ten unused coordinate products; share identical L-bitset proofs;
- parse the 86 MB old owner once per process, do not keep two checker DOMs,
  and release compressed/base64/task176 representations phase by phase;
- use symbol-index maps instead of deep-list membership and avoid duplicate
  target/dual reductions, whole-document hashes and repeated selected walks;
- make hot meter bumps O(1), sampling/synchronizing only at bounded public
  boundaries, and enforce checker wall/RSS/allocation limits too.

The reply gives formula counts and static upper bounds, never labels them
measurements.  If a repair would merely move the same repeated work behind a
cache with an unbounded owner, it is not closed.

## 10. Complete physical mutation connection

Every mutation named in task352 Section 8 is mandatory: triangular/raw,
process/fault, heavy/checkpoint, 13 boundary/process, 30 selected-correction,
7 positive and 11 physical/terminal mutations.  Each changes a real opened
owner or real transport object, invokes the same ordinary production
validator, and records the narrow first rejection.  Recovery-v1/v2, q3,
Q0/Gamma, projected/full state, K0 full-state membership, trivial kernel,
cursor, product order, heavy identity and final row mutations are all
included.  Symlink, hardlink, TOCTOU, stale output, terminal reseal and
checkpoint binding tests use safe SELFTEST temporaries only.  PRODUCTION runs
no fault injection or mutation.

The fixture roster, producer execution ledger and checker independent ledger
must agree exactly; no mutation is accepted because its name appears in a
list.  If a physical platform primitive is unavailable, return a typed
SELFTEST rejection for that platform and keep the Linux/GHA contract explicit.

## 11. Driver, static audit trail and reply

The ASCII GAP driver pins the exact final producer/checker/fixture/P and all
frozen authorities, uses exact enumerated modes, same-handle/no-follow checks
where available, bounded atomic outputs, file/directory fsync, byte-exact
producer/checker terminal comparison, and last-write sentinel.  It exposes
separate SELFTEST, fresh and authenticated-resume routes without sleep,
retry, polling or nested pools.

In the reply report exact bytes/SHA for all five machine outputs, P's self
digest and expected R/V identities, the complete import/process/physical
owner graph, line-numbered static traces for Sections 3--10, the explicit
removal of every task352 blocker and slow-work item, and any remaining first
exact blocker.  State clearly that all execution is still absent.  End
exactly with:

```text
PREREGISTRATION:                 COMPLETE or BLOCKED
IMPLEMENTATION:                  IMPLEMENTED or BLOCKED
SELFTEST / PRODUCTION:           UNEXECUTED
FROZEN INPUTS:                   PASS or BLOCKED
FRESH SEARCH ROUTE:              STATICALLY REACHABLE or BLOCKED
AUTHENTICATED RESUME ROUTE:      STATICALLY REACHABLE or BLOCKED
SOL(MAX) REAUDIT REQUIRED:       YES
ACTUAL A0 COMMON + CHECKER:      0/1
SEPARATOR / NEGATIVE CLAIM:      FORBIDDEN
LIFT / FAKE / IHARA:             NONE
```

`TASK353_R07_TASK352_A0_V11_FINITE_REPAIR`
