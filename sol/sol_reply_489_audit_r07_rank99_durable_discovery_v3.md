# Sol reply 489 - Task482 v3 GHA-dispatch audit

## Verdict

**STOP.  Task482 v3 cannot be dispatched immediately.**

The externally supplied Task487 premise is accepted: the rank-99 input prefix
is already CROSS-CHECKED.  That mathematical premise is not affected by this
audit.  The defects below are in the execution/certificate envelope.  They do
not refute the rank-99 prefix, the v424/v426/v427 paper arguments, or any other
mathematical result.  No COMMON result was computed here.

## Immutable audited pins

The owner finalized the files after the original kickoff pin was superseded.
The final bytes audited here agree with the synchronized Luna reply and driver:

| object | bytes | SHA-256 |
|---|---:|---|
| producer v3 | 100066 | `90bd58dce838eb518da7b32d8eaec210223efdee6a35d5f98d404e57517615a1` |
| checker v3 | 66854 | `70540c60f0685539d21ca5a23c10cdacb840c4317b93b88fa57fb89fc7398c35` |
| driver v3 | 8488 | `8ee2253e244f45e27307d72f7cbacf613211c10381858340e29c7b52fc7ee616` |

Producer and checker independently compute the reported binding
`71d8f66576cccf2f91e8641e1a0f0f3d00d104502a6f3d428356db9df2de8aa6`.
All pinned C99, rank-51, Task451 producer/checker, v3/v2 rank-ladder, and
v424/v426/v427 source bytes also match their embedded sizes and hashes.

## Dispatch-blocking defects

### D1 - COMMON is guaranteed to fail at the candidate-marker gate

The producer marker is
`R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V3` (producer line 20), and
`terminal_result` emits that marker followed by `_COMMON_CANDIDATE` or
`_RESOURCE_CANDIDATE` (lines 1015--1016).  The checker instead defines its
own log marker with an added `_CHECKER` suffix (checker line 17) and uses that
log marker when checking the producer artifact (lines 769 and 792).

Consequently it demands
`..._V3_CHECKER_COMMON_CANDIDATE`, while the pinned producer emits
`..._V3_COMMON_CANDIDATE`.  A bounded producer-receipt injection reached the
real checker and rejected at `resource:marker`; the COMMON equation has the
same deterministic mismatch.  The driver runs this checker on every COMMON
candidate, so it cannot reach its advertised checker PASS or COMMON COMPLETE.
The checker self-test hides the defect by synthesizing its candidate marker
from the checker marker itself (line 1141), rather than using a producer
receipt.

### D2 - The immediate predecessor file is not bound to the segment start

The flat chronological row/round/prefix walk itself is O(n), does not reopen
cumulative ancestors, and detects the commissioned same-count row mutation.
However, it does not establish the load-bearing predecessor equation required
by F3.

For an own-schema input, `input_identity` parses and validates the immediate
checkpoint but returns only its path/bytes/SHA identity (checker lines
686--706).  No later equation compares that parsed checkpoint's complete
prefix, count, rank, round, profile, or ledger to the new segment's start.
Moreover, producer lines 882--885 set `prior_state_seal` equal to a newly
computed compact `ready_core`, not to the authenticated predecessor READY
state seal.  The checker merely recomputes that same compact core from the
new output (lines 418--423).

This is concrete, not only nomenclature.  A bounded two-state fixture made a
canonical immediate predecessor with prefix digest
`9fc6d5d8e2cac1e02ea2bba953202994aed32269b1ad6127a6edb3865d9f9dba`
and a durable segment whose start-prefix digest was
`9433fac13cbc695b95ff97969ac7374116b0a127fa2d71d437c4abc2ccb4b7d8`.
The real `input_identity` accepted the former and the real `validate_state`
accepted the latter under the former's exact byte/SHA identity.  Thus the
claimed predecessor can have a different complete row prefix with identical
counts.  Also, for the canonical initial state, the actual READY state seal
was `5977770c317749f644d2a80707c37a11889dbabffdb5bfc2fdb901808ad37950`,
whereas the stored compact core was
`bd921d0124ee899b868d4c3cd4a034d7a30174abd035212b61d9d6bbcb07758c`.

The smallest repair is to retain the flat rolling validator but carry the
parsed immediate state forward and literally equate its complete prefix and
start tuple/profile/ledger to the new segment start, with an actual READY
predecessor-seal equation.  No historical ancestor walk is needed.

### D3 - A resumed zero-progress resource fallback is structurally invalid

After loading an own-schema checkpoint, producer lines 1032 and 1044 replace
the state's `input_checkpoint` with the current resume-file identity before a
new segment exists.  The last historical segment still contains the previous
invocation's input identity, while `segment_chain_gate` requires the state
identity to equal the last segment identity (producer lines 474--475; checker
lines 435--436).

Therefore a soft stop with zero retained rows, or a hard stop during replay or
before the first new close, publishes a checkpoint which its own validator
rejects.  A bounded real-helper replay of exactly that rebind failed with
`segment:final_prefix`.  This breaks the v426 repeated-candidate lane precisely
at the v427 zero-row fallback boundary.  The own-schema fixture only checks
`load_resume`; it does not perform and validate this production rebind.

### D4 - The commissioned production retained-candidate ABI is still not used

`delayed_retain` is defined at producer lines 803--821, but AST inspection
found zero calls to it from `run`.  Its only calls are in the legacy/current
fixtures (lines 1236, 1242, 1251, 1435, 1442, and 1450).  The real correction
loop separately reimplements the sequence at lines 1117--1152.

The inline production order appears to retain the intended reduce/literal/add
gates, but Task482 explicitly required the fixture to call the same factored
ABI as production.  The passing fixture therefore cannot detect drift in the
actual candidate path and does not discharge F4.

### D5 - Resource and COMPLETE branch markers are not exclusive

The shell resource branch correctly skips the expensive checker and writes a
resource-candidate value to `D482OK` (driver lines 86--93).  After the shell
returns, however, GAP checks only that `D482OK` exists and unconditionally
prints `R07_A0_DUAL_ANCHORED_RANK99_DURABLE_DISCOVERY_V3_COMPLETE` (driver
lines 101--102).  Thus an UNKNOWN_RESOURCE run issues the same COMPLETE log
marker as a checker-approved COMMON run.  This violates the v426 requirement
that COMPLETE be issued only after the one full independent checker passes.
The driver must inspect the exact OK content and emit a distinct resource
terminal without the COMMON COMPLETE marker.

### D6 - A post-batch COMMON profile cannot pass the checker

If the ordinary post-batch update reaches `dual is None`, producer line 931
sets `post_profile = None`, and lines 934--935 store that `None` as the current
profile.  The next loop iteration emits COMMON.  The checker then replays the
same terminal state but unconditionally compares `v3.b.profile(P)` with the
stored profile (checker line 655).  The pinned v2 `profile(P)` function always
returns a dictionary, including when `P["dual"]` is `None`.

A bounded injected close reproduced `post[0] is None`, stored profile `None`,
and a non-None profile-function result.  Hence, even after fixing D1, an actual
COMMON reached by closing a batch deterministically rejects at
`replay:profile`.

The resource checker has a related aggregate-count error: `segment_rises` is
the total number of rises in the invocation, but checker lines 779--786 demand
at most 16 for a committed soft flush and exactly zero for a zero-row soft
fallback or hard rollback.  After one earlier closed batch, valid totals such
as 17 are therefore rejected.  Bounded receipts reproduced
`resource:soft_flush_rows`, `resource:soft_zero_rows`, and
`resource:hard_close_rollback`.  The v426 driver presently skips that resource
checker, but the checker contract and its claimed v427 fixtures remain false.

## F1--F6 disposition

| gate | disposition |
|---|---|
| F1 exact adjoint ABI | **PASS.** AST found producer calls at 703, 755, 1100 and checker calls at 567, 615; every call is `v3.tau_free_adjoint(P,m,args)`.  No three-argument call targets `v3.b`/the one-argument v2 helper.  The injected real `replay_prefix` entry passed. |
| F2 result-to-durable equality | **PASS.** Lines 711--719 bind all commissioned duplicated fields before arithmetic at line 797; the re-sealed top-level row mutant stopped before the replay sentinel. |
| F3 flat durable chain | **FAIL** by D2 and D3.  The rolling walk is linear and ancestor-read-free, but the immediate predecessor content/READY seal is not bound and zero-progress own-schema resume is invalid. |
| F4 real fixtures | **FAIL** by D4.  Real own-file resume passed.  On this Windows host symlink creation was privilege-limited (`symlink_platform_limited=true`, `symlink_escape_rejected=false`); that limitation is reported honestly and the path guard remains static. |
| F5 limits/driver | Strict margins **PASS**: wall `14040 < 14220 < 14400`; RSS/VM `4200000000 < 4500000000 < 5120000000`, with `ulimit -v 5000000` KiB.  Exactly one producer and one conditional checker are present, and RESOURCE skips it.  Exact branch/COMMON completion **FAIL** by D1 and D5. |
| F6 v427 close | The actual `flush_rows -> commit_batch -> close_batch` fixtures pass 1/15 rows, one update, zero fallback, and forced hard rollback; checker has a meaningful 17-row rejection.  The complete envelope nevertheless **FAILS** by D3 and D6. |

## Bounded audit record

- Producer `--mode FIXTURE`: PASS, with 1/15 flush, rollback, own-schema
  resume, and three-argument replay-entry flags true.
- Checker `--self-test` and `--pin-check`: PASS, but the synthetic blind spots
  described above remain.
- Independent Python AST parse and call-target audit: PASS.
- GAP bounded parse reached the required
  `task482 external run preamble required` guard before external action.
- No production run, authority construction, GHA/workflow action, git action,
  or persistent repository-extra file was performed.

Dispatch now: **NO**.  Mathematical status: **UNCHANGED**.  Required changes
are confined to the implementation/certificate envelope and require a new
pinned successor followed by bounded re-audit.

STOP_WITH_EXACT_DEFECTS
