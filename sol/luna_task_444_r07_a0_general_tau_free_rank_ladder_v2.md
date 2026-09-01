# Luna task 444 — R07 A0 general tau-free rank ladder v2

Role: Luna implementation owner.  This is a versioned successor to rejected
Task442 v1.  Do not overwrite any v1 file.  Do not run production, Q0, GHA,
workflow dispatch, git commit, or push.  Bounded syntax/fixture checks only.

Read in full before editing:

- `sol/luna_task_442_r07_a0_iterative_rank_ladder_v1.md`
- `sol/luna_reply_442_r07_a0_iterative_rank_ladder_v1.md`
- `search/d972_r07_a0_actual_b72_rank_ladder_v1.py`
- `crosscheck/check_d972_r07_a0_actual_b72_rank_ladder_v1.py`
- `sol/proof_r07_a0_quotient_weighted_actor_column_generation_v409.md`
- `sol/proof_r07_a0_tau_free_sparse_quotient_adjoint_v410.md`
- `sol/proof_r07_a0_actor_adapted_tau_phase_selector_v411.md`
- `sol/proof_r07_a0_actual_b_dual_72_point_reduction_v412.md`
- the exact pinned Task436/v12 sources used by Task442.

The independent dispatch audit rejected v1 for two reasons: it validates a
variable-width physical pivot as a 64-character digest, and it silently
reuses the first-dual-only 72-point adjoint after rank 44.  Both defects are
load-bearing.  V2 must not claim an unrestricted ladder by hiding either one.

## Authorized outputs only

1. `search/d972_r07_a0_actual_tau_free_rank_ladder_v2.py`
2. `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v2.py`
3. `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v2.g`
4. `sol/luna_reply_444_r07_a0_general_tau_free_rank_ladder_v2.md`

Do not change any other file.  Temporary files go outside the repository.

## A. Compact-source and hot-path repair

1. Validate `row_digest`, pre/post remainder digests, and pre/post dual
   digests as exactly 64 lowercase hex characters.  Validate `pivot`
   separately as a nonempty canonical lowercase even-length hex byte string;
   `bytes.fromhex(pivot).hex()==pivot`.  The accepted 43->44 pivot is 46 bytes
   / 92 hex characters and must pass the fixture.
2. Correction `delta_word` letters are exactly in `{1,-1,2,-2}`.  Reject zero
   and every other integer.
3. `--max-rises` counts new rises in the current invocation, not the total
   accepted history restored from a checkpoint.
4. Do not recompute the current `dual/remainder` inside insertion after the
   loop already computed it.  Pass that pre-state into the insertion helper.
   Pairing nonzero with the current annihilating dual proves strict rank rise,
   so call `PackedEchelon.add` once and use its returned pivot; do not first
   call `reduce` and then make `add` repeat the same reduction/copy.  The
   checker must likewise avoid a gratuitous duplicate reduction while still
   checking the returned pivot and rank.
5. Remove unconditional per-rise `gc.collect()`.  Cache deletion is allowed;
   explicit GC is allowed only behind a measured RSS-pressure branch and must
   be reported.
6. The fixture must exercise the actual validator/restart/positive helper
   paths far enough to catch a 92-hex pivot, a noncanonical/odd pivot, an
   illegal delta letter, and a resumed per-invocation rise budget.

## B. General current-dual profile

At every nonzero current remainder, record a compact deterministic profile:

- physical rank and dual/remainder digests;
- normalized exponent coefficients on `N1,N2`;
- for each physical block, localized support counts by label;
- three tau coefficients;
- all rejected/unrecognized key types;
- after formula compilation, the exact set of required Delta coordinates.

This profile must be present in every typed resource terminal after at least
one accepted rise.  It is informational and promotes no A0 claim.

## C. Exact v410 tau-free adjoint for an arbitrary localized dual

Replace the Task436 first-dual-only `actual_adjoint` call by an independently
implemented v410 local reverse-neighbourhood compiler.

For every localized physical key `(block,label,r)` and each `j=0,1,2`, use
the actual group, actual central element, and actual `q.h0`/transversal.  The
candidate new-coordinate singletons are exactly the safe overestimate in
v410 (3.1): the central singleton at `r*z^j`, each noncentral singleton at
`r*z^j`, and each noncentral singleton at `r*z^j*s_c^-1`.  Merge duplicates.

Pull those new-coordinate candidates back through the literal Tietze map
already implemented by the pinned v12 `q.transform`.  A simple exact route is
to generate the following old-singleton candidates and evaluate each
coefficient directly as `<dual,q.transform({old_key:1})>`:

- PB3: new central `h` -> old `a(h)`; new `b(h)` -> old `b(h)` and
  old `a(h*x^-1)`; new `c(h)` -> old `c(h)` and
  old `a(h*y^-1*x^-1)`.
- PB4: new central `h` -> old `a(h)`; for a new noncentral label, include the
  corresponding old singleton at `h`, and the old-a predecessor obtained by
  solving the exact v12 transform formula.  In marked order these are
  `h*r*z^-1`, `h*q*r*z^-1`, `h*p*q*r*z^-1`,
  `h*c*p*q*r*z^-1`, and `h*b*c*p*q*r*z^-1` for labels
  `r,q,p,c,b`, respectively.  Recheck each candidate through direct
  `q.transform`; do not trust the displayed simplification alone.

Delete zero coefficients.  Every retained coefficient must equal the direct
singleton pairing.  The checker must regenerate the reverse neighbourhood
and old predecessors independently, use a different iteration order, and
compare the complete sparse adjoint digest.  It must not import the v2
producer.

The three global tau keys are **not** covered by v410.  If a current dual has
nonzero tau, stop with
`UNKNOWN_RESOURCE:NONZERO_TAU_PHASE_SELECTOR` and the complete profile.  Do
not call the adjoint empty.  V411 is not yet an implementation license to
change the accepted PB3 transversal silently; the reply must identify this
measured gate.  This v2 remains a continuing multi-rise ladder for every
successive tau-free dual, not a one-rise-only specialization.

## D. Normalized exponent constant and exact formula gates

The physical `N1,N2` coordinates are `exp_x/18,exp_y/18 mod 3`; they are not
Task179's raw exponent keys.  Compile the localized terms from the v410 raw
adjoint, then set for seed word `r_i`

`K_i = n1*(exp_x(r_i)/18) + n2*(exp_y(r_i)/18) mod 3`.

Check the identity-state formula against a fresh pinned-v12 physical seed
row, not `q.transform` of Task179 raw exponent keys.

The currently authenticated selective fibre owner supports coordinates
S0--S2.  If a compiled formula needs any other coordinate, return
`UNKNOWN_RESOURCE:SELECTOR_COORDINATES:S...` with the exact sorted coordinate
set and checkpoint.  Do not silently ignore terms.  Likewise, if `K_i != 0`
and the v143 distinct global-prefix branch has not been implemented, return
`UNKNOWN_RESOURCE:NONZERO_CONSTANT_SELECTOR` rather than searching only
support fibres.  These are measured next implementation gates, not EMPTY or
NONMEMBER terminals.

For the supported `K=0`, S0--S2 branch, retain Task442's direct literal
conjugate replay, all-eleven occurrence equality, normalized exponent check,
direct physical scalar, strict rank rise, compact checkpoint, restart replay,
and positive terminal reconstruction.

An exhausted formula may not be promoted to NONMEMBER by the producer alone.
Return a typed separator candidate requiring the independent checker's full
re-enumeration, or fail closed as v1 did.  No fake/Ihara claim.

## E. Driver and independent checker

- Byte-pin every imported source and reconstruct the exact commands.
- The driver runs producer fixture, checker self-test, then one production
  process and the independent checker on its result.  Use visible progress
  markers per rank rise and on every typed resource gate.
- Production defaults: checkpoint under `ci/out`, 4.8 GB RSS cap, bounded
  wall clock, at least 64 new rises per invocation.
- A resource terminal is a successful typed artifact only if its checkpoint,
  current-dual profile, and all accepted sources independently replay.
- Claims remain `A0=false, COMMON=false, NONMEMBER=false, fake=false,
  Ihara=false` unless a strict positive terminal is independently replayed.
  Even then this task may set only its A0/common-word-candidate field; it may
  not declare fake or Ihara.

## Required reply

Report exact byte/SHA pins, bounded commands and outcomes, the implemented
dual types, unsupported measured gates, duplicate-work removals, fixture
mutations, and a clear no-production/no-GHA statement.
