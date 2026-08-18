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
  `4cf64130b7956fe7d790d4840488c6995943868d` is executing as immutable GHA
  run `32094134098`.  It remains live and must not be cancelled; its exact
  producer began at `2026-08-18T03:07:28Z`, with checker pending.
- A stronger exact v2 contingency is locally ready for dispatch.  It keeps
  the complete two-powers by 64-corrections universe, literal predicates,
  selected word, receipt meaning, and fail-closed generic settlement fallback.
  It replaces 3840 repeated long-word evaluations by 240 fixed-context
  evaluations, replaces the high-variance PB4 fp conversion by a faithful
  Artin action on F4, evaluates action words compositionally, materializes
  only independent relation rows, and uses exact small-factor automorphism
  certificates plus invariant-module descent before the unchanged generic
  fallback.  The independent checker reconstructs all of these gates and no
  longer accepts the old projection-order-only settlement surrogate.
- Current v2 hashes are producer
  `ed60d787997fa912f72afadabe3d48be7dda9f128d0fe62a51ca9e179bdeef52`,
  independent checker
  `5c1eac3907d0b050e76de4fbf4712ca605cd69a77c0fe00a7bba7cca7c4eb719`,
  and workflow
  `d6acd056c2d58ae06e851fa0b6b0323499116d10729561d5940ed850067964ee`.
  Python AST, checker self-test, YAML parse, frozen hash pins, and
  `git diff --check` pass.  A read-only Sol(max) adversarial audit found no
  dispatch-stopping error in the intended fast path; if its sufficient factor
  certificate failed but the old generic fallback succeeded, the checker
  would reject fail-closed rather than risk a false PASS.  No local GAP or
  heavy Python has been run.  Parent committed and pushed the exact four-file
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
  Dispatch it while continuing to monitor `32094134098`; no run may support a
  terminal claim until its independent checker passes.
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
