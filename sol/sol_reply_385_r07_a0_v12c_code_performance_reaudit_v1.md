# Task 385 — R07 A0/v12c independent code/performance reaudit

## Decisive result

**STATIC REJECT.**  The six frozen physical subjects and the F1 canonical,
acyclic authority graph pass byte-level inspection.  The tranche nevertheless
cannot be authorized: the checker has a visible source-text indentation blocker
and a second independent K0 member-lifetime defect; the producer's boundary
validator uses an unbound name before its baseline can be measured; the internal
deadline does not cover imports or rollback; the resource ledgers are neither
source-derived nor mutually consistent; R and V have unhandled post-publication
failures; and the driver disarms cleanup before its final GAP-side operation.

This was a fresh static audit.  I read task385 from numbered section 1 through
section 7, all six frozen owners in full, and the prerequisite task/reply and
frozen-authority corpus prepared for this audit.  I used only read-only
PowerShell byte inspection, hashing, line inspection, and an in-place read-only
ZIP member hash.  I did **not** run or compile Python, Node, GAP, a candidate,
mutations, GHA/workflows, imports, syntax checks, subprocess tests, RSS probes,
git, or network operations.  In particular, the checker source-text blocker
below was established directly from its spaces and surrounding block structure,
not by invoking a parser.

## Frozen physical subjects and canonical roots

Independent byte counts and SHA-256 hashes are:

| frozen subject | bytes | SHA-256 | result |
|---|---:|---|---|
| `ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.manifest.v1.json` | 11,476 | `24fbc1f9d7a7be3c96e1a56d4eb97d0aa5ccca9233f1e552088e9848bc081d74` | exact |
| `search/d972_r07_history_free_positive_fast_resume_v12c.py` | 342,630 | `fbfcd4f82cccb7a6772270bf755852e94d5d98a5059994797cacc0a8e3feec92` | exact |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v12c.py` | 298,317 | `859cb6e9e1b9c7f74b39014cbdb1accdf54e1a692d5ce962d86f7314e3bb2c44` | exact |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v12c.g` | 43,559 | `56867f847d3242f03bd2763087d58df1985a8634b6260efe2cb91abc23b29c8e` | exact |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12c_20260829.json` | 22,785 | `6fb7fe92c3cf93f54e44f9f26c3e920d131dbc626fc826d8b5bb4745bf67c8ec` | exact |
| `sol/sol_reply_380_r07_a0_v12c_bounded_complete_repair.md` | 16,269 | `633fd4ec9611e3b382695d1f746ae5e51719c1b38d818ee280f12a83945d3159` | exact |

All six are ASCII, have no BOM or CR byte, and end in one LF.  Independent
ordinal-key compact-ASCII reconstruction gives the exact P0 body seal
`39b483cf2df56aa6148bac3026c16c7f4e68950c8ff417543e84b5abaaf5f775`
and fixture body seal
`5569881a6e79c0ad45a794d501f2f0e3a7625aee7f2032f42694ba6d2441256d`.

The P0 physical line 1 has `sources == {}` and exactly 30
`frozen_authorities` rows with 30 distinct physical paths.  It therefore does
not pin either final producer or final checker.  The driver's 32-entry physical
pin list is at driver lines 33–66: lines 34–37 bind P0, producer, checker and
fixture, and lines 38–65 bind the other frozen physical inputs.  All 32 paths
are distinct and all 32 extant files independently match their literal size and
hash.  The remaining frozen raw owner is separately bound at lines 67–68.  It
is not present in the worktree before the authorized extraction; read-only
streaming of the one-member frozen ZIP, without extracting it, independently
gave member length 86,368,039 and SHA-256
`c261aa967867a4870228eae467f46ee4afbfc236445890debd891bcef4a250ab`,
exactly the P0 and driver raw pin.  The driver rehashes that physical owner again
at line 439.

Ordinary JSON admission is canonical-before-semantic: producer lines
3281–3288 and checker lines 1202–1211 decode ASCII and require the original
bytes to equal compact canonical bytes plus one LF.  Their registered
whitespace, top-level key-order, extra-newline and ASCII-escape routes are
ordinary-reader routes at producer lines 3309–3355 and checker lines
4014–4061.  The driver hashes every frozen input before construction at lines
70–85 and pins the final producer/checker only in the driver (lines 35–36).
Thus the immutable-authority -> canonical P0/fixture -> producer/checker ->
driver graph is physically acyclic and contains no v12b alias.  F1 passes.

## Load-bearing defects

### D1. The checker cannot enter its K0 route

At checker lines 2428–2434, `K0CoordinateStore.put` has an eight-space method
body.  Line 2435 abruptly has twelve spaces for `for probe ...`, although line
2434 introduces no block; lines 2436–2437 are nested still farther, and line
2438 returns to twelve spaces.  This is a visible malformed indentation
structure in the frozen source.  No syntax tool was used to reach that finding.
The checker therefore cannot start as frozen.

There is also an independent defect after the minimal indentation repair:

- `K0CoordinateStore.__init__` takes only coordinate/count/width/degree and
  initializes its members at lines 2400–2421; it never creates `self.meter`.
- `put` and `lookup` dereference `self.meter` at lines 2437 and 2458.
- `_build_k0_coordinate_store` retrieves a local meter at lines 2612–2615 but
  constructs `K0CoordinateStore(...)` without it at line 2616.  There is no
  later `store.meter` assignment anywhere in the checker.

Consequently the first K0 probe cannot complete even if line 2435 is reindented.
This independently defeats the promised single K0/index build, selected-owner
reconstruction, checker mutation ledger and checker mathematical route.

### D2. The producer cannot measure the boundary baseline or its 13 mutations

`producer_boundary_validate` is a separate module-level function beginning at
producer line 5210.  It calls `live.parse_sparse` and `live.public_sparse` at
lines 5231 and 5234, but the function has no local assignment, parameter,
closure, import or module-global binding named `live`.  The caller's local
`live = runtime["live"]` at line 5321 does not bind the callee's global lookup.

The ordinary baseline invokes this defective validator at line 5349, before
the mutation loop at lines 5358–5367.  Moreover, the trace wrapper catches only
`ProtocolStop` around the validator at lines 4927–4934; the unbound-name failure
cannot become a measured typed rejection.  Thus the boundary baseline cannot be
revalidated and none of its 13 cases can acquire the required measured owner
identity/event trace/physical digest.  Declarations of the cardinalities
`8+13+30+7+11+4+2=75` (producer lines 6018–6027) do not create the exact real
ledger.  F2 is rejected before considering any candidate execution.

### D3. Heavy reuse is incomplete and avoidable boundary work is duplicated

Several local mechanisms are well aimed: producer pc-cache accounting checks a
duplicate before work and charges before multiplication/bytes/insertion at
lines 2660–2695, with failure/final releases through line 2709; producer and
checker each retain one canary and one selected full Gamma; and checker
parent/letter hashing streams compact byte owners at lines 964–983 rather than
allocating a 1,469,664-integer digest-only list.  Those local positives do not
repair D1.

There is also avoidable repeated processing in the checker.  In one
`_checker_process_case`, line 2115 calls `_checker_boundary_wire_rows` and line
2116 immediately calls `independent_boundary_outcome` on the same immutable
dual/workers.  The first route rebuilds 104 descriptors/inverses, unpacks dual
support and computes every translated pair at lines 1979–1993.  The second
route independently repeats descriptor construction, support unpacking and
every translation at lines 1853–1870, then materializes an additional
`pair_stream` and offsets at lines 1871–1882.  Child-side accumulator
recomputation does not require the parent to reconstruct immutable
descriptor/support/translation owners twice; immutable typed wire rows can be
reused while preserving the child's independent accumulator calculation.
This duplicated full translated-pair work occurs across normal/fault process
cases and is exactly the avoidably delayed processing task385 required the
audit to reject.

F3 therefore rejects both because the one-K0 route is dead and because the
checker repeats a substantial owner pass that is not forced by the retained
mathematics.

### D4. The internal elapsed deadline does not span the required lifetime

The module imports execute at producer lines 9–31 and checker lines 9 onward,
whereas the internal signal is not installed until producer line 6420 and
checker line 5620.  The external driver timeout is not the required internal
elapsed signal and cannot make those imports internally covered.

The signal contexts return from `_bounded_main` only at producer lines
6420–6421 and checker lines 5620–5621.  Their `__exit__` methods explicitly
cancel the signal timer and restore the prior handler at producer lines
510–518 and checker lines 192–199.  Only after that context has unwound do the
top-level handlers call blocking open/unlink/fsync rollback at producer lines
6424–6459 and checker lines 5624–5649.  Hence the required one internal deadline
does not cover rollback or cleanup either.

The numerical margins themselves are consistent (`9600/9900`, `5400/5700`,
`1200/1500`, and `17100 < 18000 < 21600`; producer lines 211–215 and driver
lines 219–225, 284, 450–451).  Correct constants do not cure missing lifetime
coverage.  F4 rejects.

### D5. The live-memory ledgers are opaque and conflict with the frozen fixture

The producer advertises 4,312,038,019 bytes at lines 78 and 193–207.  Its only
formula, line 204, starts from an unexplained 3,564,038,019-byte “fixed byte
owners” aggregate and adds a blanket 300,000,000 “Q0 byte-record/index headers”
aggregate; neither is decomposed into source owners, cardinalities, widths and
simultaneous last-consumer lifetimes.  The checker similarly advertises
3,153,713,824 bytes at lines 43 and 86–100, but line 95 hides
2,616,842,912 bytes inside one “immutable reconstruction/maps/DAG” aggregate.
Producer lines 6295–6296 and checker lines 5374–5376 merely reserve these
aggregate payload tokens; a token whose derivation is unexplained is not a
source-derived charge-before-allocation proof.

The mismatch is physical and semantic, not just a missing comment.  Fixture
line 1 fields
`resource_deadline_platform_contract.producer_explicit_payload_ledger_bytes`
and `checker_explicit_payload_ledger_bytes` are respectively 4,832,908,288 and
4,291,084,288.  P0 line 1 instead binds producer/checker explicit peaks
4,312,038,019 and 3,153,713,824, which match the code constants.  Thus the
frozen fixture's own contract disagrees by 520,870,269 producer bytes and
1,137,370,464 checker bytes.  No single source-derived simultaneous-lifetime
ledger can equal both sets.

The 536,870,912-byte output tokens are correctly reserved before R construction
(producer lines 6358–6360) and V construction (checker lines 5556–5558), and
both sides install/read back the 5.7 GB RLIMIT_AS before `_bounded_main`
(producer lines 521–535, 6419–6421; checker lines 202–215, 5619–5621).  Those
are useful hard-ceiling and output-reservation guards, but they do not explain
payload coexistence or reconcile the frozen ledgers.  F5 rejects; no RSS claim
is made.

### D6. R and V have unhandled failures after final visibility

The producer publication routine does retain a same-directory fd and attempts
final/temp rollback for failures inside `atomic_json` (producer lines
3056–3213).  Once it returns successfully at line 6409, however, final R is
already linked, rehashed and directory-fsynced and its directory fd is closed.
The producer then performs `print(..., flush=True)` at line 6410.  An untyped
output failure such as `OSError`/`BrokenPipeError` is outside both top-level
catch sets at lines 6445 and 6456–6457, so no producer rollback is attempted.

Likewise, checker `exclusive_json` finishes final V publication at line 5607
and closes its retained directory fd at lines 4206–4207.  Afterward the checker
performs an elapsed assertion at lines 5608–5609 and a flushed print at line
5610.  The assertion is typed and reaches rollback, but an output I/O failure
does not: the only top-level catch is `CheckStop` at line 5646.  Both typed
rollback callers also discard rollback exceptions (`except BaseException:
pass` at producer lines 6447–6448/6458–6459 and checker lines 5648–5649), so
they cannot establish the required exact cleanup result.

These are post-visible failure routes in the owner programs themselves.  A
later driver cleanup attempt is not a substitute for the task385 requirement
that every typed and untyped post-visible owner failure attempt exact final and
temp unlink plus directory fsync.  F6 rejects.

### D7. The driver still has a fallible GAP operation after helper success

The driver does use status-bearing GAP `Process` at lines 450–454, Linux/x86_64
gates at generated-shell lines 118–120, exact-one terminal checks at lines
227–236, and a shell EXIT cleanup installed at line 141.  The cleanup remains
armed through raw and sentinel rehashes at lines 439–440, which is good.

But line 442 writes `trap - EXIT` as the final generated-shell command.  At
runtime the shell executes it after the sentinel is visible and rehashed, then
returns success to GAP.  GAP subsequently performs the final
`Print(D380Sentinel,"\n")` at line 455.  If that post-helper output operation
fails, the accepted sentinel/log/R/V owners already exist and the shell EXIT
cleanup has been disarmed; there is no GAP-side rollback.  This violates the
explicit “no fallible acceptance gate after helper success” condition.  The
checker source blocker also prevents the driver from being a usable successful
SELFTEST_BOOTSTRAP route as frozen.  F7 rejects.

## Mathematical status and authority

The source still contains the intended chronological triangular construction,
raw 2,896-column checker reconstruction, dual checks, selected correction and
2,896 -> 2,897 transition bodies (notably producer lines 1468–1579 and checker
lines 3214–3345 and 4404–4488).  They are not enough for retention here: the
checker cannot enter the module as frozen, its selected K0 build has a second
independent dead route, and the producer cannot complete the ordinary boundary
ledger that is incorporated before final R.  Therefore no complete independent
producer/checker path reaches the task376 mathematical passes, so their status
in this tranche is **REGRESSED**, not merely unobserved.

No candidate was executed and no numerator is inferred.  Actual A0 remains
producer/checker `0/1`; there is no common word, lift, fake, Ihara witness, or
production/resume authority.  Because this is a static reject, even the single
bounded v12c SELFTEST_BOOTSTRAP GHA is forbidden.

AUDIT VERDICT:                         STATIC REJECT
FROZEN PHYSICAL OWNERS:                PASS
F1 CANONICAL / ACYCLIC GRAPH:          PASS
F2 REAL 75-CASE MUTATIONS:             REJECT
F3 HEAVY OWNER REUSE:                  REJECT
F4 DEADLINE COVERAGE:                  REJECT
F5 LIVE MEMORY / OUTPUT RESERVE:       REJECT
F6 DURABLE PUBLICATION:                REJECT
F7 STATUS DRIVER / INDEPENDENCE:       REJECT
TASK376 MATHEMATICAL PASSES:           REGRESSED
AVOIDABLE DUPLICATED PROCESSING:       REJECT
V12C SELFTEST_BOOTSTRAP GHA:           FORBIDDEN
PRODUCTION / RESUME:                   FORBIDDEN
ACTUAL A0 COMMON + CHECKER:             remains 0/1
LIFT / FAKE / IHARA:                    NONE

TASK385_R07_A0_V12C_CODE_PERFORMANCE_REAUDIT_V1
