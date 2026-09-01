# Luna task 468 -- rank-99 delayed-check short-batch resume owner v1

Role: Luna mechanical implementation only.  Do not run production, dispatch
GHA, edit workflows, commit, push, or touch files outside the four outputs
below.

Implement the paper theorem
`sol/proof_r07_delayed_literal_certification_short_batch_resume_v422.md`.
This task prepares the successor; parent will not dispatch it unless the
Task467 checker-only replay accepts the frozen rank-99 base.

## 1. Required outputs

Create only:

1. `search/d972_r07_a0_dual_anchored_rank99_short_batch_resume_v1.py`;
2. `crosscheck/check_d972_r07_a0_dual_anchored_rank99_short_batch_resume_v1.py`;
3. `search/d972_r07_a0_dual_anchored_rank99_short_batch_resume_gha_driver_v1.g`;
4. `sol/luna_reply_468_r07_rank99_short_batch_resume_owner_v1.md`.

## 2. Frozen owners

Exact-pin:

```text
Task451 producer
search/d972_r07_a0_dual_anchored_active_batch_v1.py
13834 ca7fb15e06dd04881146c38d63d93015a9e630fbc334cf15098cbd8a32f22f9b

Task451 checker
crosscheck/check_d972_r07_a0_dual_anchored_active_batch_v1.py
13725 5c2f76b825bd920245d0200f29ff860ba93a32663ef5db9567bc499a86f7ff8a

rank-99 candidate checkpoint (exact original bytes)
search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json
173082 bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358

v422 paper
sol/proof_r07_delayed_literal_certification_short_batch_resume_v422.md
8777 52392cd30afa73872834417f8aa3d5fce7ce6ffcf3fba1ce62407257dbf89bdc
```

Retain Task451's registered selector order, rank-51/eight-record frozen base,
three recovered batch semantics, occurrence/adjoint formula, actual action
rows, literal correction rows, and positive replay.  Do not add a candidate,
actor, closure, worker, or coordinate model.

## 3. Resume dialect and per-run cap

Version the producer/checkpoint schema.  `--resume` is required in production
and accepts only:

1. the exact frozen Task451 rank-99 candidate above; or
2. a closed checkpoint of this new schema whose frozen-base SHA equals the
   exact rank-99 candidate SHA.

For either dialect authenticate the canonical seal, schema/binding, closed
batch shape, flattened accepted list, ranks, counts, round, and exact
rank-99 prefix.  The initial accepted state is rank 99 / count 56 / three
closed 16-row batches.  An own-schema resume may append further closed
batches but may not alter that prefix.

At invocation start set

```text
segment_start_count = accepted_count
segment_start_rank  = physical_rank
segment_rises       = accepted_count - segment_start_count
```

The `--max-rises 64` cap is per invocation, not the historical count after
rank 51.  Every output carries the physical input checkpoint bytes/SHA,
segment start/end counts/ranks, and all closed batch receipts.  The checker
requires the output accepted/batch lists to extend the input lists exactly.
Do not use a self-consistent SHA as a substitute for semantic replay.

## 4. Delayed retained-only checks

Implement v422 Section 2 exactly for correction candidates:

1. formula scalar; skip zero as before;
2. one actual `replay_atom` aggregate;
3. non-mutating `P["phys"].reduce(row)` against the current within-batch
   span;
4. if dependent, continue without full `seed_v12`, conjugate exponent, or
   literal receipt;
5. if independent, perform the unchanged full conjugate `seed_v12` equality,
   exact exponent/forbidden-E, anchor scalar, selector, and digest checks;
6. insert once and require the actual pivot to equal the precomputed pivot.

Do not mutate before the retained-only literal checks pass.  Action rows keep
their existing exact direct/scalar checks.  A dependent miss is never a
negative or exhaustion certificate.

Use `--batch-cap 16`.  Close after each 16 retained rises or at the 64-rise
segment cap; a shorter final batch may close at the cap.  Perform one dual
update per closed batch.  A resource stop during an open batch reports the
preceding closed state, so no more than 15 tentative rises are lost.

## 5. Bootstrap and resource boundary

Authenticate and parse the input before expensive construction.  Write a
sealed output `BOOTSTRAP` state that represents exactly the same closed span.
Then place runtime construction, rank-51 prefix replay, all batch replay,
initial dual, selective-runtime construction, and search inside the typed
RESOURCE boundary.

On any allowlisted wall/RSS stop in those phases, emit
`status=terminal=UNKNOWN_RESOURCE` and bind the last physical closed output
checkpoint.  Constructor/replay stops must not become `terminal=UNKNOWN`, and
an output checkpoint must never name an open batch.  Non-resource exceptions
remain fail-closed `UNKNOWN` and the checker must not promote them.

## 6. Independent checker

Do not call producer `run`, `corrections`, resume parser, or seal verifier.
The checker may exact-pin shared frozen arithmetic modules but must implement
its own input/output envelope and checkpoint checks.  Starting from the
accepted rank-51 owner, semantically replay:

- all eight frozen records;
- the three exact rank-99 base batches;
- every appended closed batch and retained row;
- anchor dual/remainder, selector cursor, literal delta, exact exponent,
  actual row and scalar, predicted/actual pivot, and post-batch state;
- segment prefix, per-run 64 cap, typed RESOURCE reason, and positive replay
  if COMMON is reached.

Avoid the Task451 name-shadowing defect: no local assignment may shadow the
global formula builder.  Mutations must reject altered base prefix, input
prefix, batch anchor, selector, exponent, pivot, post dual, segment start,
63-vs-64 exact max-rise reason, 65 rises, open batch, and a RESOURCE terminal
without physical closed output.

## 7. Reusable driver

Require external preamble

```text
D972_R07_A0_DUAL_ANCHORED_RANK99_SHORT_BATCH_RESUME_V1_RUN:=true;;
```

Also accept a preamble string

```text
D972_R07_A0_DUAL_ANCHORED_RANK99_SHORT_BATCH_RESUME_V1_INPUT:=
  "search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json";;
```

Default to that exact base if the variable is unbound.  Any nondefault input
must be a canonical `search/certs/<safe-name>.json` path with no `..`, slash
ambiguity, whitespace/control, glob, or shell metacharacter.  Future closed
checkpoints can therefore be committed as versioned certificates and resumed
without rewriting this driver.  Producer and checker still authenticate and
semantically replay them.

Use fixed fresh output paths.  Exact-pin producer/checker/base, record the
selected input bytes/SHA, and run one producer followed by one independent
checker.  Production bounds are 14,400 seconds, 4,800,000,000 RSS bytes,
64 segment rises, batch cap 16.  Use `set -euo pipefail`, an external
foreground timeout with kill grace, pipeline-status propagation, output
freshness checks, and exact-one producer terminal plus checker PASS.  No
fixture/self-test precedes production and no second producer process exists.

## 8. Bounded local gates

Run only repo-external-cache compile/load/help, fixture, checker self-test,
pin/cardinality gates, and static driver scans.  Fixtures must show:

- dependent nonzero-scalar row calls `replay_atom`/reduce but not full
  `seed_v12` or exponent;
- retained row performs all checks before one mutation and binds predicted
  pivot;
- input rank99 plus 64 segment rises is accepted while 63 is rejected for an
  exact max-rise terminal and 65 is rejected absolutely;
- an open interruption preserves the previous closed seal;
- resource failure during construction/replay returns typed closed fallback;
- default and safe versioned resume paths pass, traversal/glob/control/shell
  paths fail;
- producer/checker command counts and exact marker counts are one.

Do not run actual A0 production locally.  State that no mathematical terminal
has been obtained and that dispatch remains contingent on Task467 PASS.

