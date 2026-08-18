# Luna task 157cu - implement the literal row-18 C2^24 stage consumer

## RESET BOOTSTRAP -- single current-state authority

After any context compaction or session handoff, read this section before any
older reply.  This section is the current-state authority for the active B4-B
route.  Older conditional/blocker audits must not be promoted back into the
current state when they conflict with the frozen decisions below.

Maintenance rule: whenever a material conclusion, active implementation
stage, commit, workflow run, or terminal result changes, parent Sol must
update this section before proceeding.  Keep it as a current-state snapshot,
not a chronological log; replace stale pointers instead of making a reader
reconstruct the present state from old entries.

Frozen, non-regressible conclusions:

1. The target is zero-based roof row 18, with pure axis `(1,0)`, and its
   arithmetic-outside status is accepted.
2. It is enough to produce one actual typed lift of this fixed target at each
   member of a downward-directed cofinal isolated family.  A preselected
   parent lift does not have to be preserved; stage seeds may differ.
3. Common isolated refinements give the finite-intersection property for the
   exact row-18 fibres.  Finite-fibre compactness then gives a coherent global
   lift and the accepted Main-Line theorem gives B4-B.
4. The stronger 325-distinct-lifts route remains sufficient but is not
   required once the fixed row-18 lift is implemented.
5. The accepted construction engine is surgery + torsor + power.  Do not
   restart a proof-gap, cofinality, parent-preservation, arithmetic-detector,
   Brunnian/horn, or universal-scalar audit.  Remaining work is literal typed
   implementation, independent replay, and GHA execution only.

Current implementation pointer (2026-08-18 JST):

- `157cu` remains the active finite computation.  The cross-checked C2^24
  input is immutable GHA run `32088693149`: GAP producer and independent
  Python checker agree on the lossless 24-word basis and `rank=24` (not Lean
  verified and not by itself terminal B4-B).
- Original literal-row18 run `32090719159` completed with the bounded exact
  result `UNKNOWN_RESOURCE`: its producer reached the 100-minute limit, so no
  mathematical A/B conclusion was emitted and its checker was correctly
  skipped.
- Semantics-preserving first acceleration commit
  `4cf64130b7956fe7d790d4840488c6995943868d` completed as immutable GHA run
  `32094134098`.  Its exact producer ran from `2026-08-18T03:07:28Z` to the
  100-minute bound at `2026-08-18T04:47:28Z`, emitted
  `UNKNOWN_RESOURCE`, and correctly skipped the checker.  This is not an A/B
  conclusion and no longer needs monitoring.
- The exact v2 bundle is the active implementation.  It keeps the complete
  two-powers by 64-corrections universe, literal predicates, selected word,
  and receipt meaning.  It replaces 3840 repeated long-word evaluations by
  240 fixed-context evaluations, replaces the high-variance PB4 fp conversion
  by a faithful Artin action on F4, and uses exact small-factor automorphism
  certificates.  The corrected literal comparison uses explicit products of
  relator conjugates for all 24 marked-kernel basis elements and the exact
  `D=R intersect C=C` kernel diagram; the old generic settlement fallback has
  been removed.  The independent checker reconstructs every certificate and
  no longer accepts either raw-row relabelling or the old projection-order-only
  settlement surrogate.
- Current exact v2 implementation bundle is the audited charm-repair bundle,
  with producer
  `f170a208c3937f2f05d51fd21114a2c8314ee086baae56bb85e82c3b4053fd94`,
  independent checker
  `af54af1ff86bcfd6d5d29a58cca10fc4f0ee83ee1a9177b50b993d35d02141cc`,
  and workflow
  `45aedca4cbad580ed4399dcc96f4af27fcd1dbd0eb45d469a571d2c53a43ddc9`.
  Python AST, checker self-test, YAML and embedded-Python parse, frozen hash and
  action pins, single-semicolon audit, and `git diff --check` pass.  Strict
  subgroup additions are bounded by 105 and conjugation attempts by 1260;
  no joint-group `Size` is computed, membership is batched, and all 24 targets
  stop the search immediately.  The workflow producer bound is 30 minutes and
  the job bound 40 minutes, replacing the obsolete 100/110-minute limits.  No
  local GAP or heavy Python has been run.  Earlier, parent committed and pushed the exact four-file
  v2 bundle as `32881fb2c6f3e6143baf82af55fc03f74664cc4d`, then dispatched registered
  literal-only GHA run `32098738964` at that immutable commit.  The run passed
  setup, all frozen hashes, checker self-test, core reconstruction, and the F4
  Artin replay, then stopped at the producer's P-factor irreducibility gate;
  this is an implementation failure, not an A/B result.  The emitted immutable
  core rows independently give order 504 and invariant-closure rank 6 in all
  four factors.  Diagnostic repair run `32099098286` (commit
  `f263c40bd00f7aad2635e75bbc2d2669445ec140`) made the mismatch exact:
  invariant closure is `[true,true,true,true]`, while GAP reports the four
  generic MatrixObj-generated group sizes as `[infinity,infinity,infinity,
  infinity]`.  This is a representation-recognition issue, not a mathematical
  failure.  Parent now sends the same invertible 6x6 actions faithfully to
  permutations of the 63 nonzero vectors and performs the order-504 and normal
  closure gates in finite permutation groups; raw matrices and the independent
  invariant-rank checks remain unchanged.  The repaired producer hash is
  `59cb71ce21031f309873fbfcef1887a8f0361fb258ffde343bc236443d381174`.
  Parent committed/pushed this repair as
  `5ab0c703b21b947152523a299c58e41bdb8b99e5` and dispatched immutable
  literal-only GHA run `32099345952`.  The finite permutation order and
  irreducibility gates passed immediately; the run then exposed the same
  generic MatrixObj arithmetic mismatch in the six-pure-braid replay.  Parent
  removed the remaining MatrixObj dependence: multiplication, inversion,
  pure-word replay, commutator support, and receipt rows now use exact GF(2)
  bit-row algebra, while order/normal-closure stays in the faithful 63-point
  permutation image.  A matrix/permutation commutator canary binds the two.
  The repaired producer hash is
  `2044f6f2a6a4fabd98b2bde990ccbcf44ca836c56cb49a573f2ad2266a9844d7`.
  Parent committed/pushed this repair as
  `3da719fc7ab596dc225120bd9851226f7f098fd9` and dispatched immutable
  literal-only GHA run `32099636331`.  The complete action block then passed
  in about 2.25 seconds; the run stopped at the first raw A.18 row whose
  P4/G9 projection was not identity.  This is not an A/B result.  Before
  changing that fail-closed gate, parent added a bounded diagnostic giving
  the exact row index, coface, seed, P/G9 orders, and lossless permutation
  arrays.  Diagnostic producer hash:
  `a27da615434463826143e6e79cdc30b8fdbebb89092bc551acb6462dc91150ca`.
  Parent committed/pushed the diagnostic as
  `577f05a0ef589b0c105305cd5d30df89d0ee6234` and dispatched immutable
  literal-only GHA run `32099865818`.  That diagnostic completed and gave the
  first exact counterexample to the implementation shortcut: A.18 coface
  `123`, seed `5` has both P4 and G9^4 image order `9`.  Thus individual raw
  A.18 rows cannot be relabelled as vectors in the marked C2^24 kernel.  This
  is a comparison/implementation error, not an error in the frozen B4-B
  mathematics and not an A/B result.
- The completed exact repair forms the literal normal closure in the joint
  finite image and extracts only base-cancelling kernel combinations.  Its
  release certificate must express each of the 24 standard C2^24 basis words
  as an explicit product of conjugates of the 158 literal relators.  The
  independent checker will reconstruct those conjugate words, replay E/P/G9,
  require P4=G9^4=1, require the 24 standard E masks and rank 24, and will not
  duplicate or trust the producer's normal-closure search.  The producer must
  cache images, grow its subgroup monotonically, test the 24 targets in
  batches, stop as soon as all are present, expand free words only afterward,
  and emit phase timings.  It has no generic fallback.  Parent Sol and a
  separate read-only Sol(max) adversarial audit both found no
  dispatch-stopping blocker: the positive normal-membership certificate,
  105/1260 bounds, F6 expansion, independent checker, `D=C` quotient diagram,
  GAP API surface, and 30-minute workflow bound all pass static review.  Parent
  committed the exact three-file bundle as the SHA above, recorded and pushed
  it through bootstrap commit
  `a55fd48adb722104908b3e6dacd9784e37e3aa2e`, and dispatched registered
  literal-only GHA run `32102023241` at that exact head at
  `2026-08-18T05:13:04Z`.  Attempt 1 failed before any mathematical step:
  the official PackageGT ZIP endpoint reset all six `curl` attempts, so the
  producer and checker were never started and this is not an A/B result.
  Parent immediately requested attempt 2 of the same immutable run/head; it
  failed at the identical pre-mathematics transport step.  Both attempts left
  producer and checker unstarted, so neither is an A/B result.  A timestamped
  Internet Archive capture of the same official URL (`20250208231651`) has
  now been downloaded independently and matches the frozen archive SHA
  `c3124483...f95` byte for byte.  The implemented repair is restricted to an
  official-primary / timestamp-fixed-archive-fallback fetch; the archive SHA,
  unique-member gate, member SHA, and exclusive write remain mandatory.
  Luna and parent independently passed YAML, embedded-Python, immutable-action,
  producer/checker-pin, archive/member, and diff checks; a separate Sol(max)
  transport audit also returned GO.  Parent committed and pushed the repair as
  `da918277594f0a43bd4fa699ea3fa3bb86cf2ac5` and dispatched registered
  literal-only run `32102847972` at that immutable head on
  `2026-08-18T05:25:55Z`.  The transport, every frozen hash, and self-test
  passed.  The new positive normal certificate then succeeded quickly: round
  zero retained 12 literal relators, all 24 marked targets were already in
  their subgroup, and 24 explicit combinations were expanded.  The producer
  subsequently failed at `value outside V4` while trying to form an optional
  norm operator from the still-untyped raw row-18 root; the direct 128-candidate
  replay and checker were therefore not reached.  This is not an A/B result
  and does not invalidate the 24 literal certificates.  The active repair is
  to represent an unavailable raw-root action/norm honestly and continue the
  already independent direct exponent-1/exponent-2 typed replay.  The
  completed Sol audit also requires candidate-specific Dtilde/pentagon
  transport (not a base-only proxy), treats base masks/gauge/norm as
  diagnostics rather than terminal inputs, and settlement-tests every local
  solution in exponent-1-first order instead of stopping at the first local
  candidate.  Only a fully settled candidate is selected; if none settles,
  the bounded universe is an exact finite-stage obstruction.  Luna completed
  this three-file repair; checker self-test, Python/YAML/embedded-Python parse,
  immutable action and source pins, and diff checks pass.  A final independent
  Sol(max) audit returned GO with no dispatch-stopping blocker.  Parent
  committed and pushed the exact three-file repair as the current bundle SHA
  above, recorded it through bootstrap head
  `88de550bb740eae5fcf5c68bb45fa9c5db4cc35c`, and dispatched registered
  literal-only run `32104681787` at that immutable head on
  `2026-08-18T05:54:04Z`.  GAP producer and independent Python checker both
  passed, but the emitted `EXACT_FINITE_STAGE_OBSTRUCTION` is invalid and must
  not be reused: both programs incorrectly tested original-B4 charmingness by
  requiring zero exponent sums of the chosen raw free representative.  The
  fixed row-18 word has exponent sums `(6,-4)` and all six corrections have
  `(0,0)`, so that over-strong test forced all 128 candidates to fail before
  transport.  Definition 2.19 of 2008.00066 instead requires the coset to have
  a representative in `[F2,F2]`, equivalently membership in the derived
  subgroup of the actual finite quotient; its separate `T^F2`-onto condition
  remains the existing `onto_E`/`onto_G9` gate.  The fine quotient is the
  pinned `E direct-product G9`, with orders `32256` and `2916`, `E` perfect,
  and `|G9'|=729`.  The current bundle replaces only the false charm gate by
  `candidate_E in E'` and `candidate_G9 in G9'`; the checker independently
  reconstructs both normal closures.  The 24 literal certificates, A.18,
  candidate universe, hexagon, pentagon, transport, onto, and settlement code
  are unchanged.  Parent and independent Sol(max) static audits both return
  GO.  The active next step is parent commit/push and the same registered GHA
  rerun.  No local GAP or heavy Python is authorized.
- Tasks `157cs` and `157ct` are cancelled/superseded and must not be resumed.

The terminal objective remains B4-B, not a partial finite result.

## Role and frozen mathematics

You are Luna.  This is implementation work only.  Do not reopen, weaken, or
reaudit the following accepted proof chain:

```text
one fixed outside roof target lifted at every cofinal isolated stage
  -> common-refinement finite-intersection property
  -> compactness
  -> B4-B.
```

The fixed target is zero-based roof row 18, the pure axis `(1,0)`, and is
accepted as arithmetic-outside.  A preselected parent lift is not required.
The construction engine is the accepted surgery + torsor + power design.
The current job is to turn the present C2^24 and literal-A.18 artifacts into
one actual typed finite-stage lift/correction receipt.

Read these files in full before editing:

- `sol/luna_reply_157ch_c2_24_chief_consumer.md`
- `sol/luna_reply_157cj_c2_24_fast_witness.md`
- `sol/luna_reply_157cf_literal_a18_obstruction_audit.md`
- `sol/luna_reply_157cn_literal_a18_dependency_closure.md`
- `sol/luna_reply_157ck_b4_surgery_torsor_power.md`
- `sol/luna_reply_157cl_b4_arithmetic_frattini_detector.md`
- `search/d972_d972core_c2six_intersection_v2.g`
- `search/check_d972_d972core_c2six_intersection_v2.py`
- `search/d972_b4_next_obstruction_v2.py`
- `search/check_d972_b4_next_obstruction_v2.py`

Do not run GAP locally and do not start a heavy local Python job.  Do not use
Git, credentials, or GitHub Actions.  Parent Sol is the broker.

## Exact implementation target

Create only these new versioned files:

- `search/d972_b4_literal_row18_stage_v1.g`
- `search/check_d972_b4_literal_row18_stage_v1.py`
- `.github/workflows/d972-b4-literal-row18-stage-v1.yml`
- `sol/luna_reply_157cu_literal_row18_stage_impl.md`

The workflow may rerun the fast v2 C2 producer and the exact literal-A.18
construction in the same pinned job, or consume parent-supplied immutable
artifact IDs and SHA-256 values.  It must never download a floating latest
artifact.

## Required construction

1. Reconstruct the 24 lossless `C_P/C_E ~= F2^24` basis words and all frozen
   tuple/map conventions.  Bind the repaired v2 row-vector PSL convention.
2. Compute, rather than assert, the full marked B4 action on this basis for
   `sigma_1,sigma_2,sigma_3`.  Store exact 24x24 F2 matrices (or an equivalent
   lossless word certificate), verify all Artin relations, and compute the
   exact action image and invariant/chief decomposition.
3. Build the literal A.18 correction map for the fixed row-18 pair.  It must
   include both hexagons, the ordered five-coface pentagon, gauge and relation
   boundaries, marking, representative independence, charming/onto, and
   settlement.  Derive the comparison with the marked C2^24 basis; do not
   relabel the four-deletion ambient module as the A.18 module.
4. Solve the exact finite surgery/torsor equation for row 18.  Emit either:

   - one lossless correction/typed source whose roof reduction is exactly row
     18 and for which every literal gate replays; or
   - an exact finite obstruction witness for this stage; or
   - `UNKNOWN_RESOURCE`/`UNKNOWN_MISSING_INPUT`.

   A necessary-only Burau/Magnus zero is never a typed lift.
5. If the correction uses the accepted power selector, record the exact root,
   exponent, roof result, outside-row proof, action/norm matrix, and the
   unpowered and powered defects.  Do not substitute a naive word power for
   GT-shadow composition.
6. The independent checker must rebuild all finite groups/maps and A.18 words
   without importing producer helpers, replay the 24 basis and B4 action,
   re-solve or independently verify the linear/nonlinear correction equation,
   and replay every typed gate on the final source.
7. Add mutation tests for at least: PSL orientation, one A.18 coface, factor
   order, basis word, action matrix, row-18 key/word binding, correction bit,
   GT composition order, roof reduction, and each terminal status.

## Workflow and resource rules

- Manual dispatch; immutable action SHAs; exact source/input hash gate.
- GAP 4.16.0 only through the repository setup used by the repaired v2
  workflow.
- One GHA job is preferred.  No local parallel computation.
- Timeout/resource exhaustion is UNKNOWN, never a mathematical negative.
- Upload a lossless receipt and logs on success, failure, and timeout.
- Static/Python selftests may be run locally only if lightweight and short;
  do not execute the production calculation.

Do not write another theorem-gap report.  If a code-level datum is absent,
name the exact missing field/function and implement it from the frozen maps
when possible.  Report a blocker only when no exact implementation can be
formed from the repository inputs.

End with exactly one token:

- `LITERAL_ROW18_STAGE_READY_FOR_GHA`
- `LITERAL_ROW18_STAGE_IMPLEMENTATION_BLOCKED`
