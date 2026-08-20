# Luna reply 157eb — seed-span affine solver

Status: implementation complete and ready for the parent to commit/push. The
corrective target-6 production-builder selftest is also complete. No local
GAP, full producer, Git, or GHA run was performed.

## Frozen scope

- Task SHA: `d38a8a7647cca720f73650c616803b1d8d499338783e2c4ebe20fed3b91035f2`.
- The producer reconstructs the authenticated 26 cubes and ordered 104 seeds
  (`[k,x],[x,k],[k,y],[y,k]`) with the frozen seed digest, then checks every
  registered occurrence context and all six source anchors.
- Targets 1–5 use the exact identity-root/opcode shortcut. Target 6 uses the
  direct left-Fox formula
  `L_C([c]-[b])+L_h1[a]`, with ordinary product order `C*B^-1*A`, and
  compares the formula against the direct raw gradient. The target-6 helper
  now records and gates the literal reduced-word identity, both word digests,
  and the empty-delta orientation canary.
- Target 6 separates the actual base gradient `D(r0)` from each formula delta
  `D(rs)-D(r0)`, then uses `D(r0)+delta` for the typed seed replay. Later
  targets retain only transposed current remainders. Each row records the
  current 104-column `delta_rank` separately from cumulative
  `constraint_rank_gain`.
- The raw C1 affine certificate is checked before the fixed D2 prefix. The
  prefix basis gate requires least canonical pivots, unit pivot coefficients,
  unique pivots, and no preceding keys; `full_remainder` continues after a
  free key and eliminates later pivots.
- The positive path builds a rank-2 typed seed product and independently
  replays all 33 acceptance targets and 17 diagnostic targets. Diagnostics
  remain excluded from acceptance. The four terminals and no-claim boundary
  are fail-closed.
- The target-6-only typed builder now has a dedicated root selector: it
  requires exactly one acceptance row, index 0, with name
  `hexagon_1_coface_0` and kind `hexagon`. Both producer and checker use this
  selector; name, kind, and cardinality mutations are rejected by selftest.

## Independent checker and shared-core coverage

The checker has a shared production validation core for the envelope/claim and
resource-partial schema, exact authenticated metadata and cap bindings,
echelon/full-remainder replay, F3 affine elimination, raw model/direct
equality, context product orientation, and the lossless selected-proof DAG
replayer. The bounded fixture injects only a tiny quotient/presentation and
leaf provider; it does not replace those gates. The control receipt, including
source hashes, fixed roof, prefix metadata, and registered-universe metadata,
was sent through `checker_affine_validate`; mutations for the F2 image, seed
order/sign/duplicate, occurrence context, target-6 order/translation and
base/delta arithmetic, context product orientation, both remainder cases,
affine consistency, exponent-two semantics, raw/direct mismatch, cap
projection, diagnostic promotion, selected proof, terminal/claim fields, and
resource partials were rejected through that same entry.

The checker now requires the complete authenticated pin projection (formula,
task, q3 producer/checker/driver/artifact, v9 producer, and strong-prefix
source), not only the three affine-local fields. `UNKNOWN_INPUT` has its own
stage-safe closed-schema gate: it verifies the same pin/source projection,
fixed paths, untouched ledgers, and input-error envelope without requiring a
selected q3 roof. q3 schema/formula drift is serialized as `UNKNOWN_INPUT`
rather than escaping as a hard exception. `AFFINE_PREFIX_BINDINGS` now binds
the producer's five prefix counts as well as its five hashes.

The corrective resource ledger removes the former fabricated `cap+1`
default. Every registered ResourceStop carries the actual attempted/current
count, cap key/limit, and `trigger_relation` (`gt` for strict-overflow gates,
`ge` for equality-inclusive RSS/timeout/pool gates); the checker applies the
same reason-specific comparator. Source-preflight callbacks record the actual
seed index, and positive replay callbacks record setup/target/diagnostic stage,
target ordinal, and seed index. Target-6 detail construction is an explicit
deadline-cadenced loop, and transposed absorption calls the producer monitor
every 1024 coordinates. Partial fixtures cover both `gt` and `ge` boundaries,
source-seed progress, positive-replay progress, and prefix count bindings.
Checker deadline calls at those outer cadence points use `force=True`, so the
internal 256-call throttle cannot suppress the target6/source/row/target-seed
checks.

Positive-replay resource stops have a dedicated checker branch: it first
replays and binds all 33 completed target rows, the affine system, and its
canonical-solution digest, then checks setup 0/0, acceptance ordinal 1–33,
or diagnostic ordinal 1–17 with the recorded seed index. The producer resets
target/seed to 0/0 immediately before positive setup, including typed-candidate
construction.

After source preflight succeeds, the producer resets the seed to 0 and enters
`fresh_immutable_prefix` before strong-canary, static, and base evaluation, so
a prefix-stage stop cannot be misclassified as source-preflight seed 0.
Transposed affine absorption is transactional: the producer snapshots the row
maps, equation count, and consistency flag before coordinate absorption and
restores all three on any `ResourceStop`. A bounded producer canary forces a
mid-absorption stop and checks the exact pre-state digest/equation/consistency,
so an interrupted target cannot leak partial rows into the completed-target
receipt.

The final bounded combined lightweight selftest (producer followed by checker)
passed:

```text
D972_B345_SEEDSPAN_AFFINE_PRODUCER_SELFTEST_PASS seed_order=1 seed_digest=1 source_anchor_policy=1 occurrence_gate=1 raw_chain=1 raw_pair=1 raw_inverse=1 raw_square=1 base_delta_split=1 target6_order=1 full_remainder=1 later_pivot=1 affine_consistent=1 affine_inconsistent=1 exponent_two=1 diagnostics_excluded=1 resource_pre_target=1 transposed_rollback=1 phase_boundary=1 terminals=4
D972_B345_SEEDSPAN_AFFINE_CHECKER_SELFTEST_PASS shared_core=1 provider_boundary=1 seed_order=1 seed_digest=1 raw_chain=1 raw_pair=1 raw_inverse=1 raw_square=1 base_delta_split=1 context_registry=1 target6_order=1 full_remainder=1 later_pivot=1 affine_consistent=1 affine_inconsistent=1 selected_proof=1 diagnostics_excluded=1 terminals=4 resource_phases=4 gt_ge=1 source_seed=1 positive_phase=1 positive_ranges=1 prefix_counts=1 deadline=1
```

The corrective combined run additionally exercised the production
`_affine_build_typed_target6`/checker counterpart and its index/name/kind/
cardinality mutation gates, plus full-pin/top-level drift and UNKNOWN_INPUT
fixtures. It passed as:

```text
D972_B345_SEEDSPAN_AFFINE_CORRECTIVE_COMBINED_SELFTEST_PASS
```

Static `py_compile` passed for both Python files, an AST audit found no
ResourceStop constructor lacking the four measurement fields, and a bounded
driver binding check confirmed that its producer/checker pins match the hashes
below. The registered budget is 18,000 seconds and 4,831,838,208 RSS bytes.
Runtime is estimated, not measured: minutes to roughly 30 minutes to reach
target 6 and
roughly 30–120 minutes for a consistent all-33 replay. A resource cap produces
`UNKNOWN_RESOURCE`, not a mathematical conclusion.

For the final freeze, the unmeasured runtime estimate is minutes to roughly
30 minutes to target 6 and roughly 30–120 minutes for a consistent all-33
replay. A cap is `UNKNOWN_RESOURCE`, never a mathematical conclusion.

## Versioned artifacts

```text
search/d972_b345_seedspan_affine_solver_v1.py             487345 bytes  8f911ba8fec127e543f5aad65ed8c3b635ce83855703483d8f1a497bc3825e15
search/check_d972_b345_seedspan_affine_solver_v1.py       523575 bytes  67ad8d8227f1a8a60e481977fd2d07d819d532deb2651cd28667db997ec46081
search/d972_b345_seedspan_affine_solver_gha_driver_v1.g      9028 bytes  fca917211a04c553faf3d85e43fd3dbb184a5c28c6424c04070f5d52c7b4c508
```

The thin GAP driver pins the producer/checker hashes above, runs the q3 child
and its independent checker, uses stale-output cleanup plus pipefail/tee and
exit-zero sentinels, and keeps selftest/full modes exclusive. A future
successful producer plus checker artifact is **cross-checked**, not Lean
verified, and is only a finite registered seed-span result; it does not by
itself claim B4-A, B4-B, full D2, full H3, or cofinality.

B345_SEEDSPAN_AFFINE_V1_READY_FOR_GHA
