# Sol(max) reply 508 — rank99 nonzero-constant global prefix v6 audit

## Verdict

`STOP_DO_NOT_ADOPT`.

The v431 mathematics remains sound, and the implemented v5-to-v6 state
migration itself is lossless.  The frozen v6 implementation is nevertheless
unsafe to dispatch: the production scan does not skip zero values, the
checker trusts the producer's duplicated `W`, the checker rejects an intended
support-prefix close while accepting a non-fresh multirow global batch, and
the driver only syntax-checks its generated shell instead of executing it.
No mathematics change is required; all repairs are implementation, checker,
transport, and live-test repairs.

## Exact audited pins

```text
v431 paper
  9592 7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4
Task507 audit
  7164 741c5be74245e1944ce497a2fdd101b099b57d580f12ab96577f07074546ccdb
v6 producer
  14329 3173c9d99fc5a94713d3dbed1b2c90d4ed3a5723b428838ec0bd50d8aee3d90c
v6 checker
  12191 2f579f818b7fff01a3af4764393ac2f2a3190767f0671e6d407c7fe2517e91da
v6 driver
  5291 bd51bb88295d2b1238233ab37de8a2bd69cf5ea598138772197dc2f2bf5f5395
Task506 implementation reply
  1584 a53320e4b3623b1e8b56d3567920d601a434375eb67b6f30e5207e4ff52e0aa9
v5 producer
  104031 25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09
v5 checker
  71589 970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d
v5 driver
  9425 bed9105b36fef5e59120d954029ec507b16f393ab2859a7599867a19156b1b5d
```

The exact inherited pin check also passed for:

```text
C99             173082 bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358
rank51           10934 a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4
Task451 producer 13834 ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b
Task451 checker  14442 1d1080cd3e130d987316feefd820215f495cd6320aa5eca764fd2f8997f0c424
v424 paper         7009 f2e2103f214e6d7c15f5d1c2bc84cd100cd37a69634c381793a42a20e8bad2d9
v426 paper         9165 5c3176011ea64235196587ed19720ad5d5a5c542c2896e46fe33ef3df3a3977a
v427 paper         6602 b958a164dfc78c77596876227b31a39467e077c9666d4a7be9033a58ee4c0ec5
```

Notably, both v6 `PROOF` constants are dead: `pins()`/`BINDING` remain the
old seven-entry v5 set, and the driver's proof-size/hash constants are never
used to hash the file.

## Bounded commands and reproductions

Only pin/static inspection, fixtures, and in-memory synthetic replay were
used.  No production, GHA, authority construction, GAP search, persistent
checkpoint, or implementation edit was run.

```powershell
python -B search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py `
  --mode FIXTURE --output "$env:TEMP\task508_producer_fixture.json"
python -B crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py --self-test
python -B crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py --pin-check
```

All three advertised bounded gates returned PASS.  They do not cover the
load-bearing new branch.  Four small `python -B -c` harnesses then called the
actual imported helpers/batch loop and exact durable functions.  Their
essential outputs were:

```json
{"global_invariant_in_executable":true,"main_run_identity":true,"old_nonzero_stop_in_executable":false,"patched_source_flag":true,"production_run_has_global_helper":true}
{"checker_semantic_W_values_accepted":[0,17],"producer_zero_scalar":"RuntimeError:global:zero_scalar","resealed_mutated_W":17,"resealed_structural_validation":"PASS","true_W":0}
{"support_preclose_with_later_nonzero_K":"RuntimeError:batch:branch","two_global_post_rank":2,"two_global_rows_same_batch":"ACCEPTED"}
{"checker_legacy_validation":"PASS","historical_segments_equal":true,"ledger_equal":true,"migration_diff":["binding","schema","state_sha256"],"prefix_equal":true,"producer_legacy_validation":"PASS"}
```

The W mutation changed both copies of `W`, recomputed the row-containing
rolling prefix, segment ledger/end core, and top state seal, passed exact v6
structural validation, and then passed the live checker semantic helper.

### Post-audit actual-run evidence

This audit did not launch production.  Root subsequently supplied the frozen
facts from GHA run `33553895281`, and the reported failure agrees exactly with
the frozen executable source:

```text
terminal: plain UNKNOWN
reason:   'dict' object has no attribute 'relators'
durable checkpoint: rank 99 / accepted_count 56 / new rises 0
```

The transformed live loop evaluates `P["pres"].relators`, but the actual
production `P["pres"]` is a dictionary; the established ABI everywhere else
is `P["pres"]["relators"]`.  Thus the new branch is reached, but fails before
performing any commissioned global rise.

The same run log completed selective Q0 and S0/S1/S2 twice.  Static control
flow explains the duplicate exactly: `replay_all` constructs and returns
`sf` while replaying the frozen correction prefix, then `run` discards that
returned object at v5-owner line 1155 by unconditionally calling
`m.selective_runtime(P,p179,args)` again.  This is a reachable multi-hour/RSS
regression, not fixture noise.  The repair must reuse returned `sf` and its
runtime, building only if `sf is None`.

## Findings

### F1. Production transformation reachability — STOP

The transformation anchor occurs exactly once.  Exported `main` resolves to
the transformed `run`; its executable code contains `_v6_retain_global` and
`GLOBAL_SELECTOR_INVARIANT`, and no longer contains the old
`NONZERO_CONSTANT_SELECTOR` stop.  Action-first and the old zero-K loop remain
on the executable path.

However, the loop at producer lines 156--164 calls `_v6_retain_global` for
every cursor.  That helper immediately requires `scalar in (1,2)` at line 77.
Thus the first zero value raises `RuntimeError:global:zero_scalar` instead of
being skipped.  The W+1 theorem guarantees a later nonzero point, not that
cursor zero or every earlier cursor is nonzero.  This makes the intended
production branch incomplete.

Before that defect is reached, actual run `33553895281` demonstrates an even
earlier live ABI failure: the transformed loop uses the invalid attribute
access `P["pres"].relators`.  It terminated plain UNKNOWN at rank99/56 with
zero new rises.  Replace it with `P["pres"]["relators"]`.

Finally, retain the `sf` returned by `replay_all`.  Unconditionally rebuilding
the selective runtime caused the actual run to complete Q0 and S0/S1/S2
twice.  This does not change the theorem, but it consumes the audited resource
margin before useful search.

### F2. Fresh-anchor producer close — PASS conditional on F1 repair

When `rows` is nonempty, the transformed loop breaks before any global word
evaluation and reaches the unchanged v427 `flush_rows`; the outer loop then
recomputes its dual.  At an empty anchor, a retained global row breaks both
loops and reaches the same close with one row.  There is no continued scan
under that stale dual.  These control edges are correct, but the fresh scan
cannot reach its guaranteed point until F1 repairs the relator ABI, reuses the
replay runtime, and skips zero values.

### F3. Producer W, roster, and ten-coordinate path — PASS

The producer sums `sf.kernel_orders[coordinate]` once for every distinct
merged `(coordinate,target)` key, so target multiplicity is retained.  It
checks coordinates 0--2 and `W < 357128352`, scans `range(W+1)`, uses
`divmod(cursor,243)`, forms Gamma word followed by Q0 section word, and calls
direct `p179.coordinate_blobs`.  It checks a ten-byte-tuple ABI and never
calls inherited `sf.global_candidate` or constructs omitted stores.

### F4. Independent checker W — STOP

Checker lines 79--85 merely read `W` from the cursor, check the range, and
require `record["W"] == W`.  There is no use of `sf.kernel_orders` anywhere
in the global replay.  With formula `K=1, merged={}`, the mathematical value
is `W=0`; changing both producer-supplied copies to 17 and consistently
resealing prefix/ledger/state was accepted.  This is exactly the coordinated
mutation the independent recomputation is meant to reject.

The checker must compute, from its independently compiled selected formula
and its independently built selective runtime,

```text
expected_W = sum(sf.kernel_orders[j] for (j,t) in formula["merged"])
```

and require `cursor_W == record_W == expected_W`.  It should also bind the
redundant `record["global_cursor"]` to the cursor point; the current checker
does not inspect that field.

### F5. Checker literal/fresh/order contract — STOP

The checker does independently reconstruct qid/gid, word, all ten blobs,
compiled scalar, conjugate, occurrence row, exponent, forbidden-E condition,
row digest, nonmutating pivot, direct pairing, and actual physical add.  Typed
dispatch rejects cross-kind cursor substitutions fail-closed.

Two batching defects remain:

1. There is no requirement that a batch containing a global cursor have
   exactly one row.  The live `_replay_batch_v6` accepted two ordered global
   records in one batch.  Require `len(batch["rows"]) == 1` for the global
   branch, which also enforces its fresh-anchor receipt semantics.
2. For an old support cursor, checker lines 148--149 still require that
   **every** compiled formula have `K=0`.  The new producer is specifically
   allowed to retain support rises from earlier zero-K seeds, encounter a
   later nonzero-K seed, close that nonempty prefix, and restart.  The live
   checker rejected this intended receipt with `batch:branch`.  Validate the
   selected support record against its own zero-K formula and old cursor
   contract; do not restore the removed global all-formulas-zero gate.

### F6. v5-to-v6 migration and identities — PASS, with one pin repair

Producer and checker separately authenticate the full exact v5 state before
migration.  The bounded one-segment reconstruction passed both legacy
validators.  Migration changed exactly `schema`, `binding`, and
`state_sha256`; historical rows, segments, identities, prefix, ready core,
and ledger remained equal.  Own-v6 validation and producer/checker binding
equality also passed.  Immediate input identity handling remains inherited
from the audited v5 boundary and does not reopen historical ancestors.

The new v431 proof must nevertheless be included in the v6 binding/pin map
and checked independently on both sides.  Merely declaring an unused `PROOF`
tuple does not bind a durable v6 state to its new theorem.

### F7. Driver transport — STOP

The generated shell contains one v6 producer and a checker only on the COMMON
branch, and its producer numeric envelope is correctly
`14040 < 14220 < 14400`, `4200000000 < 4500000000 < 5120000000`, with
`ulimit -v 5000000`.

But the GAP driver ends with `bash -n` and the message “production is
intentionally not started”; it never executes the shell.  It therefore runs
zero producers and zero checkers under dispatch and produces no uploadable
closed checkpoint.  Compared with the audited v5 transport it also removed:

- actual byte/hash checks for producer, checker, proof, and frozen inputs;
- canonical realpath and unique terminal-status checks;
- RESOURCE artifact/checkpoint nonempty, discovery-mode, and state-seal
  checks, plus the claims-false resource OK marker;
- the checker PASS-terminal marker check and owned OK validation; and
- the final execution/result dispatch marker.

It also expanded the checker timeout from the audited 5400 seconds to another
14400-second window.  Restore the v5 execution/transport envelope verbatim,
changing only versioned paths, exact pins, schema/markers, and preamble; keep
RESOURCE checker-free and never print global COMPLETE there.

### F8. Mutation coverage — STOP

The producer's v6 fixture only calls `_global_literal_word` twice and sets
four booleans.  It never exercises formula evaluation, zero skipping,
`_retain_global`, either fresh-close edge, or migration.  The checker extension
likewise tests only one direct word and sets `v6_legacy_migration_gate=True`
without testing the new W/batch rules.  This explains why all advertised
tests passed despite the four live counterexamples above.

Add the Task506-required live tests: the real dictionary `pres` ABI, reuse of
the `sf` returned by replay, zero-before-hit and hit-at-W schedules,
independent re-sealed W mutation, one-row global enforcement, support-prefix
preclose with a later nonzero-K formula, exact migration mutations, and
driver generated-shell execution/transport assertions.

## Minimal repair list

1. Use `P["pres"]["relators"]`, reuse the selective `sf/runtime` returned by
   `replay_all`, and skip zero compiled scalars before invoking the retaining
   wrapper; retain the first nonzero actual rise and keep the invariant error
   only after exhausting `0..W`.
2. Independently recompute W in the checker, bind `global_cursor`, enforce a
   one-row global batch, and admit old support rows by their selected zero-K
   formula rather than by an all-formulas-zero condition.
3. Bind/check v431 in both v6 pin maps/bindings and restore the exact audited
   v5 driver execution, pin, RESOURCE, COMMON-checker, marker, and wall gates
   with only versioned substitutions.
4. Replace the boolean-only v6 fixture additions with bounded live-path and
   mutation tests covering items 1--3.

## Claim boundary

No inspected defect supplies a negative certificate, compatible lift, fake,
Ihara witness, or current COMMON word.  Resource/partial states remain
claims-false, and A0 remains 0/1 pending a successfully transported,
independently checked COMMON result.  The current files must not be dispatched
or adopted.

TASK508_R07_RANK99_NONZERO_CONSTANT_GLOBAL_PREFIX_V6_AUDIT_STOP
