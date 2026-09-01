# Sol reply 468 — rank-99 short-batch resume owner v1 adversarial audit

## Verdict

**STOP.  Do not dispatch this producer/driver, and do not treat the current
checker PASS as semantic evidence.**

The submitted producer is a contingent-stop stub, not the successor required
by Task468.  On the default input it writes two wrappers around the unchanged
rank-99 candidate, returns `UNKNOWN_RESOURCE:contingent_Task467_checker_pass`
without constructing the owner or searching, and the submitted checker accepts
that result.  Thus the driver can print `..._COMPLETE` after zero continuation
work.  No mathematical terminal has been obtained.

The four submitted file identities and the four declared frozen identities do
match the Luna reply.  That bookkeeping fact does not repair the semantic
failures below.  Audit was read-only: no production, GAP run, git operation,
GHA dispatch, or checkpoint mutation was performed.

## Load-bearing findings

### F1 — The production owner is absent

Producer `run` (lines 107–122) only calls the shallow resume reader, writes the
same input state first as `BOOTSTRAP` and immediately as `READY`, then returns.
It never loads the Task451 arithmetic, constructs the physical owner, replays
the rank-51 prefix or any batch, computes a dual, constructs the selective
runtime, enumerates an action/correction, closes a new batch, or performs a
positive replay.  `delayed_retained_candidate` (lines 75–90) is dead code with
no caller.  The Task451 producer/checker and paper pins are evaluated only in
FIXTURE mode through `pins()`; production does not authenticate them.

Task467 PASS is an external dispatch prerequisite in the commission, not a
runtime resource condition.  Even after that prerequisite is satisfied, this
program has no flag or branch that can continue past line 122.  Labeling the
prerequisite `UNKNOWN_RESOURCE` is therefore both falsely typed and a permanent
stop.

**Required fix:** replace the stub by an actual continuation of the exact
Task451 owner.  Enforce all frozen code/paper/base pins in production, bind them
into a fresh schema binding, restore the exact rank-99 physical state, and run
the unchanged action/correction selector until COMMON, an allowlisted resource
stop, or the per-invocation rise cap.  Keep Task467 solely in the parent's
dispatch gate; remove the contingent pseudo-resource terminal.

### F2 — The advertised delayed check is not connected and misuses the real ABI

Even considered in isolation, lines 80–89 cannot be connected to the frozen
owner as written.  The exact `PackedEchelon.reduce` reached by Task451 returns
`(remainder, coefficients)`, not a remainder dictionary
(`search/d972_r07_a0_pb34_direct_quotient_owner_v12.py`, lines 89–95).  Line 81
stores that two-tuple in `remainder`; it is always truthy, so the dependent
branch at line 82 is unreachable, and `min(remainder)` at line 87 attempts to
order dictionaries and raises `TypeError`.  Its callback signatures also do
not instantiate the frozen `replay_atom`, full-conjugate `seed_v12`, source, or
literal-receipt ABIs.  Therefore the claimed cost removal is neither executed
nor executable.

**Required fix:** integrate the delayed order in the actual Task451 correction
loop, with the concrete ABI:

1. compute the frozen occurrence-formula scalar and skip zero;
2. compute exactly one actual `aggregate(replay_atom(seed, delta, ...))`;
3. use `remainder, _ = P["phys"].reduce(row)` without mutation;
4. if `remainder` is empty, continue without full conjugate construction,
   `seed_v12`, exponent work, receipt, or `add`;
5. otherwise construct the exact reduced conjugate, require fresh `seed_v12`
   equality, exact exponent pair/divisibility and forbidden-`E` absence,
   formula/direct/anchor scalar equality, selector/delta/adjoint/digest gates,
   and only then form the receipt;
6. call `add` once and require its returned pivot to equal
   `min(remainder)` (with the canonical byte/hex encoding in the receipt).

The action-row path must retain Task451's direct-row and scalar gates.  No
dependent miss may feed an exhaustion or negative terminal.

### F3 — Neither resume dialect nor the 16/64 semantics is implemented

`load_resume` lines 57–62 require every own-schema checkpoint to remain exactly
count 56, rank 99, and three batches.  Consequently the first checkpoint that
actually appended a batch could never be resumed.  Conversely, an own-schema
input is accepted from an unkeyed self-consistent wrapper after only those
counts: there is no new binding, no nested closed-state seal check, no Task451
schema/binding check, no round check, no flattening equality, no anchor/rank
chain, no equality of the first 56 records/first three receipts to the exact
rank-99 prefix, and not even a check that each declared `row_count` equals its
row list.  The exact-candidate branch likewise does not run the commissioned
schema/binding/semantic checks; `frozen()` is unused.

There is no batch loop or counter.  `--max-rises` and `--batch-cap` are merely
required to equal constants (line 130), while the receipt and checker hard-code
zero segment rises.  The new checkpoint wrapper lacks segment start/end
counts/ranks.  It cannot append a 16-row close, close at the 64-rise boundary,
discard an open batch, or distinguish historical 48 batch rows from new
per-invocation rises.

**Required fix:** normalize both allowed inputs into one authenticated closed
state.  For the base dialect verify the exact bytes/SHA, canonical state seal,
old schema/binding, round 12, rank 99/count 56, exact rank-51 eight-record
prefix, exact flattened 48-row suffix, and the exact three 16-row anchor/post
chains.  For the new dialect verify the new canonical seal and binding, frozen
base SHA, physical input identity, all closed receipts, flattening/ranks/counts/
round, and exact equality of its first 56 records and first three batches to
that base; allow only further valid closed batches.  At process start set the
segment counters from the authenticated input, increment only
`accepted_count - segment_start_count`, close/update once per commissioned
batch boundary, and require exactly 64 new rises for a max-rise terminal;
reject 63 for that reason and reject every value above 64.  Both checkpoint and
terminal receipt must bind input path/bytes/SHA, segment start/end counts/ranks,
and the complete closed receipt chain.

### F4 — Typed RESOURCE and closed-fallback behavior is missing

The producer has no `--seconds` or `--rss-bytes` arguments, no budget checks,
and no RESOURCE boundary around construction/replay/search.  The only typed
terminal is the non-resource Task467 stub.  Moreover the outer exception path
at lines 132–134 sets `status=UNKNOWN_RESOURCE` for a prefixed exception but
unconditionally sets `terminal=UNKNOWN`, so a real resource exception would
produce an internally inconsistent envelope.  Immediate overwrite of the
bootstrap with an unearned `READY` state gives no restoration evidence.

The temporary-file, file-`fsync`, and `os.replace` sequence at lines 64–69 is a
reasonable atomic-write primitive, but no open batch exists in this program and
there is no live/closed-state separation for it to protect.

**Required fix:** after cheap exact input authentication, write the sealed
BOOTSTRAP for precisely that closed span and retain its identity as
`last_closed`.  Put pinned arithmetic loading, runtime construction, rank-51
replay, all base/appended batch replay, initial dual/profile, selective-runtime
construction, and search inside one typed boundary with an internal wall gate
strictly inside the 14,400-second supervisor and a 4,800,000,000-byte RSS gate.
Only explicitly allowlisted wall/RSS and
exact max-rise stops may return `status=terminal=UNKNOWN_RESOURCE`, always
pointing to `last_closed`; an interrupted open batch must be absent from every
reported count/rank/list.  Non-resource exceptions must be
`status=terminal=UNKNOWN` and must never be checker-promotable.  Write `READY`
only after the reconstructed closed state has passed replay.

### F5 — The checker is structural theater, not independent semantic replay

The checker imports no frozen arithmetic owner.  `replay_retained` lines 48–65
only increments an integer after checking field types; it does not replay the
eight rank-51 records at all, and for the 48 batch records it recomputes no
literal, selector, exponent, row, scalar, remainder, pivot, anchor, or post-dual
state.  It also replays the separately pinned `base`, not the durable state's
batches.

This separation gives a concrete false-acceptance path.  A self-sealed
checkpoint may have the exact base `accepted_sources`, `accepted_count=56`,
`rank=99`, `batch_count=3`, `open_batch=false`, but `batches=[]` (or arbitrary
batches), and may omit `frozen_sha256`, binding, phase, and input metadata.
`closed_state` accepts it; lines 71–77 accept matching empty top-level batches;
and `replay_retained(base)` independently walks the untouched repository base.
No flattening ties those two objects together.  In addition, line 67 allows
*any* equal `status`/`terminal` string, and there is no resource-reason allowlist
or COMMON positive replay.  Thus even an arbitrary terminal label can reach the
checker PASS marker after recomputing the two unkeyed seals.

The checker is also intrinsically unable to check the requested successor: it
requires the input SHA to be the original candidate (line 70), exactly three
batches and rank 99, and segment rise zero (lines 71–81).  Every legitimate
own-schema resume with appended rows is rejected.

**Required fix:** implement a genuinely independent envelope/parser/seal path
and exact-pin the shared *arithmetic* modules it needs, without calling producer
`run`, `corrections`, its resume parser, or its seal verifier.  Starting from
the accepted rank-51 owner, semantically replay all eight records, the exact
three base batches, and every appended closed batch.  Independently check the
anchor dual/remainder, selector cursor and literal delta, formula and actual
scalar, full retained-only seed/exponent/forbidden-`E` gates, actual row digest,
non-mutating predicted pivot, actual add pivot, post-batch remainder/dual, round
and flattening chain, physical input extension, and segment cap.  Accept only
the commissioned terminal set; require an allowlisted physical closed fallback
for RESOURCE and the unchanged full positive replay for COMMON.

### F6 — The driver can certify zero work and its resource/path gates are incomplete

With fresh output paths, the default producer deterministically emits the
contingent zero-rise receipt, the current checker accepts it, and driver lines
51–58 therefore create the OK file and print COMPLETE.  This is a false
production success path, not merely lost progress.

The shell does have `set -euo pipefail`, one producer process, one checker
process, fresh-path guards, exact submitted producer/checker/base pins, an
external foreground timeout, and a 4.8 GB `ulimit`.  However, because there is
no internal wall/RSS owner gate, an external timeout or memory kill terminates
the pipeline before a typed terminal can be emitted and before the checker can
run.  It cannot satisfy the closed-fallback contract.

The GAP path predicate also does not implement the stated dialect exactly:
`Position(tail,"..")` searches for a list element, not a substring, and the
allowed-character loop permits repeated dots; no `.json` suffix is required.
Thus names containing `..` and non-JSON safe names pass even though the
commission explicitly rejects them.  (Slash, whitespace, control, glob, and
shell characters are rejected by the character allowlist.)

**Required fix:** after F1–F5, pass the internal seconds/RSS bounds and leave an
external foreground timeout/kill grace as the supervisor; ensure the internal
typed stop occurs early enough to seal the preceding closed state.  Require a
canonical one-component `search/certs/<safe-name>.json` using an actual
substring test such as `PositionSublist` plus an exact `.json` suffix test.
Keep the existing fixed fresh paths, pipefail, exact-one command/marker gates,
and make COMPLETE depend on a checker that accepts only the legitimate terminal
set and semantic replay.

### F7 — The bounded gates and Luna report do not exercise the contract

Producer `delayed_fixture` does not call `delayed_retained_candidate` or the
real owner.  Its dependent case records only `reduce`—not the required actual
`replay_atom` plus reduce—and every resume/resource/path/63/64/65 result is a
hard-coded `True`.  Checker `self_test` calls only a four-field toy gate and
hard-codes the remaining claimed capabilities; it never calls `check` and does
not exercise the commissioned mutations.  Therefore the Luna reply's claims
that delayed order, resume, typed fallback, and independent replay are present
are materially unsupported by its reported PASS lines.

**Required fix:** make fixtures invoke the same concrete delayed-candidate and
resume/resource validators used by production, with call counters around the
actual ABI.  Make checker self-tests pass a valid sealed fixture through the
real checker and individually require rejection of altered base prefix, input
prefix, batch anchor, selector/delta, exponent/forbidden-`E`, row/scalar,
predicted/actual pivot, post dual/remainder, segment start, exact-max at 63,
absolute 65, open batch, and RESOURCE without a physical closed output.  Test
both the default base and a safe appended own-schema input, plus traversal,
glob, control, shell, repeated-dot, and non-JSON driver paths.  Boolean labels
without executed gates are not evidence.

## Re-audit gate

A fresh version is eligible for re-audit only after all of the following are
present simultaneously:

```text
actual Task451 arithmetic continuation from exact rank 99
real delayed replay/reduce/literal/add order with the PackedEchelon ABI
appendable authenticated closed checkpoints and per-invocation 64 rises
batch_cap 16 with previous-closed fallback for every open interruption
typed constructor/replay/search RESOURCE boundary
independent rank51 + 8 + base 48 + appended semantic replay
real mutation/63-64-65/resource/path fixtures
one-producer/one-checker driver whose COMPLETE cannot certify zero work
Task467 PASS enforced externally by the parent before dispatch
```

**STOP**
