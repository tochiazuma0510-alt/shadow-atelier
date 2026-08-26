# Luna task 167: g760 target6 post-closure recovery v5

Date: 2026-08-27
Role: Luna / implementation and bounded mechanical audit only

## 1. Incident and purpose

GHA run `32975492800`, commit `73efbdb8345d4fa2802d6e948b6e7cd43897369a`,
ran the v4 producer.  It completed all eleven fresh `j=9` D2 relator
closures in about 70 minutes.  The exact terminal ranks were

```text
0 -> 2578 -> 5075 -> 7653 -> 10069 -> 12371 -> 14868 -> 17230
  -> 18739 -> 19498 -> 19563 -> 19621.
```

Every v4 delta was atomically written and logged.  Immediately after relator
11 the producer caught an exception and emitted

```text
terminal=R07_760_L3_TARGET6_INPUT_STOP checkpoints=11
```

without a completed-j marker.  The GAP driver then rejected the otherwise
written receipt with `receipt envelope`, so the generic workflow skipped
artifact upload.  Independently, v3 run `32972580814` completed the same j=9
rank 19621 and emitted `j=9 nonmember=false`, then reached j=10 relator 7 rank
29143 before the six-hour workflow timeout.  Thus this task repairs recovery
plumbing only; it must not reinterpret MEMBER as a lift.

Build a versioned v5 adapter/driver which diagnoses and fixes the v4
post-closure failure, ensures every authenticated claim-free terminal exits
the driver successfully so the existing generic uploader runs, and supplies
a deterministic safe-stop after a requested number of newly completed
relators.  Do not run the full j=9 computation locally.

## 2. Fixed mathematical scope

Pin and preserve v4, v3, and all their mathematical inputs exactly:

- fixed g760 and SHA, inherited `[2,3,4,5,6,7,8]`, fresh `[9,10,11,12]`;
- saturated `(x_i-1)` BFS, D2-first order, all 649,539 translations;
- exact left-multiplication and Jennings caches and insertion order;
- target6 first coface and the complete C-13 legal overapproximation;
- first-NONMEMBER terminal rule and mandatory helper-nonshared direct checker;
- append-only delta rows, authenticated ancestor replay, and all false global
  claims.

No mathematical row generation, projection, closure, target reduction, or
separator logic may change.  MEMBER remains survival of this one L3 screen,
not actual A18, cofinal lift, fake, or Ihara witness.

## 3. Allowed new files

Use versioned v5 paths only:

1. `search/d972_r07_760_l3_target6_delta_resume_v5.py`;
2. `search/d972_r07_760_l3_target6_delta_resume_gha_driver_v5.g`;
3. one v5 preflight certificate under `search/certs/`;
4. `sol/luna_reply_167_r07_target6_postclosure_recovery_v5.md`.

Do not modify v1--v4, workflows, proofs, CLAIMS, `sol_reply_159_iv.md`, or any
unrelated dirty file.  No git, push, GHA dispatch, or workflow operation.

## 4. Required diagnosis and completed-j regression

Trace the exact v4 path from `finish_j_row` through
`validate_terminal_header`, `build_j_checkpoint`, `write_j_checkpoint`, output
validation, and the driver envelope.  State the precise producer-side cause
of the observed INPUT_STOP if mechanically recoverable; do not guess.

Add a bounded exact post-closure regression which reaches the same control
path with:

- 11 completed closure receipts;
- a terminal relator-11 delta record and state commitment;
- a public `nonmember=false` row carrying the v3 accelerator boundary and v5
  append-only boundary;
- terminal-header/public-row binding;
- completed-j checkpoint build, immutable write, reload, full validation,
  and manifest inclusion;
- transition to the exact next j.

This regression must have failed on the v4 defect and pass on v5, or else the
producer-side cause remains explicitly UNKNOWN and v5 must expose a stable
ASCII `stop_stage` plus a sanitized/bounded `stop_reason` in the producer log
and receipt so a GHA rerun cannot hide it.

## 5. Driver receipt repair

Audit every v4 string-count predicate against the canonical JSON structure.
In particular, legitimate fields may occur in both `resume_contract` and
`result`; do not require global textual uniqueness unless the schema makes it
unique.  Bind the entire receipt by its producer log SHA/byte pair, enforce
exactly one terminal token, false global claims, and terminal-specific fields.

A well-formed `NONMEMBER`, `MEMBER_INCONCLUSIVE`, `UNKNOWN_RESOURCE`, or
`INPUT_STOP` receipt must let the GAP driver exit zero after writing timing,
hash ledger, and success sentinel.  This is operational acceptance only.  A
malformed/missing receipt, missing checkpoint, hash mismatch, claim widening,
or terminal mismatch must still fail closed.  Include mutations for the
observed duplicate-field false rejection and for each weakened gate.

## 6. Safe stop and artifact preservation

Add a deterministic option limiting the number of newly completed relator
closures in one invocation.  The stop may occur only immediately after the
corresponding immutable delta checkpoint is written and authenticated.  It
must return `UNKNOWN_RESOURCE` (or a new equally claim-free resource terminal
accepted by the existing four-terminal contract), record the exact next
relator, and never infer an unfinished relator.  It must not count replayed
ancestors as new work.

The v5 GHA driver must expose this as a bounded integer preamble variable and
default the first recovery run to exactly 11 newly completed relators, so the
fresh run stops just after j=9 relator 11 and uploads the complete j=9 chain.
If the completed-j checkpoint can safely be finalized before stopping, require
and upload it; otherwise explain and make the relator-11 delta resumable.

Keep an outer process timeout below the six-hour workflow limit with at least
30 minutes packaging margin.  The safe-stop counter, not a guessed runtime,
is the primary boundary.  All receipt, logs, timing, hash ledger, and the fixed
checkpoint directory must remain under `ci/out/`, already covered by the
generic workflow artifact path.  Do not edit the workflow.  Cross-run artifact
download remains parent Sol's separate authorization problem.

## 7. Bounded audit

Run serial local syntax/selftest/preflight only.  No full j=9, no heavy or
parallel Python/GAP.  At minimum require:

- all v4 delta replay/mutation/cache equality tests retained;
- exact completed-j regression above;
- byte-equal preflight generation twice from the final source;
- driver selftest with one producer and zero checker processes;
- synthetic full-terminal driver fixtures for all four terminals, proving
  well-formed claim-free resource/input stops exit zero and corruptions fail;
- safe-stop fresh and resumed toy cases, proving replayed ancestors do not
  consume the new-work allowance and the exact next relator is recorded;
- ASCII/LF driver and final source/pin drift audit.

## 8. Report boundary

Report exact cause(s), paths, sizes, SHA-256, commands, outputs, mutation
count, completed-j regression receipt, safe-stop receipt, driver terminal
matrix, and remaining UNKNOWNs.  Repeat verbatim:

```text
j=9 nonmember=false is producer survival evidence, not an A18 lift
delta checkpoint = resource recovery, not a mathematical result
fresh NONMEMBER = candidate until helper-nonshared direct checker agrees
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```
