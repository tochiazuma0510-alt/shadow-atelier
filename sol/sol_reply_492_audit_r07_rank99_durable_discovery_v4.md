# Sol reply 492 - Task490 v4 immediate GHA-dispatch audit

## Verdict

**GO.  The exact pinned Task490 v4 trio is safe for immediate GHA dispatch.**

The external premise is used exactly as supplied: the 56-source/rank-99 C99
prefix is CROSS-CHECKED by Task487.  This audit found no defect in the narrow
Task489 D1--D6 repair boundary or in the additional base/BOOTSTRAP boundary.
No production run or COMMON computation was performed.

## Audited pins

| object | bytes | SHA-256 |
|---|---:|---|
| producer v4 | 98576 | `5b8f3ae76abb64768decb14be50fbd6d75b5e84aeaad2b1a63fcb544933cf36f` |
| checker v4 | 66212 | `cd0acf346d4f133dfaa8e047db6593511a5423c6a166060a37fc313504e928e7` |
| driver v4 | 9424 | `948f6254298eef51d524e834441c530ecb1a5a3a5cbefbdfe3dac9e7922d0ff8` |

Producer and checker independently agree on binding
`d5777bc12023298808fa7f0637de47e072af0bf8137c7922ce4c0cd17c7327be`.
All embedded C99, rank-51, Task451 producer/checker, and v424/v426/v427
source pins passed.  The producer and checker construct literally equal
normalized C99 predecessor states: phase `BOOTSTRAP`, ledger `digest([])`,
and state seal
`b9761eefb702179ea547d57af3fe5489bff1e5d2a8102bb057f654bcaf0f74ff`.

## D1--D6 findings

### D1 - producer marker

**PASS.**  The checker separates its output `MARKER` from the pinned
`PRODUCER_MARKER` and requires the latter's `_RESOURCE_CANDIDATE` or
`_COMMON_CANDIDATE`.  Its bounded real receipt gate accepts the producer
marker, while a re-sealed receipt carrying the old checker marker rejects at
`resource:marker` before arithmetic replay.

### D2 - immediate predecessor and flat chain

**PASS.**  `load_resume`/`input_identity` reads and authenticates the one
immediate checkpoint once, retains the parsed state, and does not reopen
historical ancestors.  On the first new segment, producer and checker bind:

- the complete accepted-source and batch prefix;
- prefix records/digest, count, rank, batch, and round;
- current profile, rolling ledger, and the complete preceding segment list;
- `prior_state_seal` to the parsed predecessor's actual `state_sha256`.

The chronological segment/batch walk binds every round and row span and is a
flat O(n) traversal.  The same-count/different-prefix predecessor mutant, row
mutant, identity mutant, and prior-seal mutant all reject.  The initial
segment uses the identical producer/checker C99-normalized BOOTSTRAP state,
not an unrelated compact-core hash.

### D3 - zero progress and first-close boundaries

**PASS.**  `run` preserves an own-schema state's historical
`input_checkpoint`; that identity advances only inside a successful closed
batch.  A zero-row soft stop and a hard stop before/inside the first close
therefore return the preceding valid closed state.  The fixture exercises
the production `load_resume`/`flush_rows` boundary and validates all of:

- base hard-pre-replay fallback reloaded as own-schema `BOOTSTRAP`;
- base first close anchored to the normalized C99 state seal;
- own-schema zero progress with the historical identity unchanged;
- own `CLOSED` first close anchored to that parsed state's seal;
- forced pre-close and serialization-close rollback.

### D4 - one retained-correction ABI

**PASS.**  There is one helper, `retain_correction_candidate`.  The real
`run` calls it and the fixture calls the same helper.  It performs one
nonmutating reduction, skips dependent rows before literal reconstruction,
then applies literal equality, exponent, forbidden-coordinate, coordinate,
scalar, and pairing gates, followed by exactly one add with actual pivot equal
to the predicted pivot.  No fixture-only retained-candidate duplicate remains.
The action lane retains its direct candidate/scalar/reduce/add/pivot gates.

### D5 - RESOURCE versus COMMON completion

**PASS.**  The generated shell contains exactly one producer invocation and
one checker invocation below the RESOURCE early-exit branch.  RESOURCE checks
the owned receipt/checkpoint, writes only
`..._V4_RESOURCE_CANDIDATE`, proves its owned OK file contains no `..._COMPLETE`,
and exits before the checker.  COMMON runs the single checker and writes
`..._COMPLETE` only after the exact checker PASS marker.  After shell return,
GAP reads the exact one-line owned OK content and prints either the distinct
`..._RESOURCE_TERMINAL` or `..._COMPLETE`; no unconditional COMPLETE remains.

### D6 - post-batch profile and aggregate rises

**PASS.**  Every committed batch stores the actual profile dictionary from
`profile(P)`, including a post-update `dual is None` profile whose
`dual_digest` is `None`; replay compares that dictionary exactly before a
COMMON candidate can pass.  `segment_rises` is treated as the invocation
aggregate.  A committed soft flush checks only the final local batch's 1--16
rows, while zero-current-row soft fallback and failed-close rollback may keep
earlier committed rises.  The bounded gates pass aggregate rises 17, retained
aggregate 5 on a zero-current-row stop, retained aggregate 5 after failed
close, and an injected post-batch COMMON profile.

## Task480 F1--F6 re-audit

| gate | disposition |
|---|---|
| F1 exact adjoint ABI | **PASS.** Independent AST found producer calls at lines 727, 779, 1185 and checker calls at 599, 647; every target is `v4.tau_free_adjoint(P,m,args)` with three positional arguments. |
| F2 result/durable binding | **PASS.** All duplicated row, batch, count, round, profile, segment, identity, and prefix fields are equated before `arithmetic()`/replay; the real-envelope top-level row mutant rejects first. |
| F3 durable chain | **PASS.** Complete immediate predecessor content and actual state seal are bound; round equations are explicit; the walk is flat and ancestor-read-free. |
| F4 real entry points | **PASS.** Production retain, replay-prefix ABI, `load_resume`, `flush_rows -> commit_batch -> close_batch`, and real checker-envelope gates are exercised.  On this Windows host symlink creation remains privilege-limited (`symlink_platform_limited=true`, `symlink_escape_rejected=false`); the production path guard is unchanged and strict. |
| F5 limits/driver | **PASS.** Wall `14040 < 14220 < 14400`; RSS/VM `4200000000 < 4500000000 < 5120000000`; shell VM is `5000000` KiB.  One producer and at most one conditional checker are pinned. |
| F6 short-batch close | **PASS.** Real close path passes 1/15/16 rows, one post-batch update, zero-row fallback, soft flush, and forced hard rollback; zero and 17 local rows reject. |

## Bounded audit record

- Producer `python -B ... --mode FIXTURE --output %TEMP%/...`: PASS.
- Checker `--self-test`: PASS; checker `--pin-check`: PASS.
- Independent AST/call-target audit and normalized-base equality check: PASS.
- Exact generated driver shell: Git Bash `bash -n` PASS; static branch ownership
  and invocation counts PASS.
- GAP 4.16.0 through `gap.ps1`, `ReadAsFunction` of the exact pinned driver:
  exit 0 with only normal unbound-global warnings.
- No production/GHA/workflow, authority computation, git operation, ancestor
  replay, or persistent repository-extra file was used.

Mathematical status: **UNCHANGED**.  This is an implementation/certificate
envelope dispatch ruling.  It neither upgrades the Task487 CROSS-CHECKED
rank-99 premise to Lean verification nor asserts a COMMON result.

GO_FOR_GHA_DISPATCH
