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

- This task, `157cu`, is the active implementation task.
- Literal-A.18 run `32083392589` has completed all shards and the exact merge;
  its independent v2 checker is running.
- Repaired C2^24 producer run `32086984144` reproduced `rank=24`; its checker
  stopped only because one embedded producer SHA was stale.  Luna repaired
  that binding; parent Sol committed/pushed it as
  `1b91f3067358e3daba793319ce95bdd47eddacfd`.  Automatic rerun `32087818507`
  again reproduced `rank=24` and exposed one remaining finite convention bug:
  producer point order `[infinity,0,...,7]` versus checker order
  `[0,...,7,infinity]`.  Luna is applying the exact nine-point relabelling and
  refreshing the chained hashes before the next rerun.
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
