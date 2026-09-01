# Luna task 445 — R07 A0 single-update tau-free rank ladder v3

Role: Luna implementation owner. This is a narrowly versioned performance and
transport repair of Task444 v2. Do not overwrite v1/v2. Do not run production,
GHA, workflow dispatch, git commit, or push. Bounded compile/fixture tests only.

Read the Task444 instruction, reply, producer, checker, and driver in full.
Preserve its mathematical universe exactly: the existing least-transversal ABI,
arbitrary localized tau-free current duals, normalized N1/N2, K=0, and selector
coordinates S0--S2. Do not implement v411, tau phases, S3--S9, a new quotient,
or any new search family.

## Authorized outputs only

1. `search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py`
2. `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v3.py`
3. `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v3.g`
4. `sol/luna_reply_445_r07_a0_single_update_rank_ladder_v3.md`

Temporary files must be outside the repository.

## A. One exact dual/remainder computation per state

V2 currently computes the post-rise dual/remainder in `insert`, repeats it on
the progress/checkpoint line, and repeats it again at the next loop head. This
is forbidden in v3.

- Compute the initial current state exactly once after bootstrap/resume.
- `insert` may call `phys.dual(target)` exactly once after its single
  `PackedEchelon.add`, because the post-state digests and the next state are
  required. Return `(record, post_dual, post_remainder, post_coefficients)`.
- Carry that returned state into the next loop iteration. Progress/profile and
  checkpoint writing must use the stored state; they must not call `update`.
- The next iteration must not recompute that same state. Hence a production
  path with R accepted rises has exactly R+1 state computations (the initial
  state plus one after each rise), apart from explicit resume reconstruction.
- Keep exactly one definition of the state-update helper.

Apply the same carry-forward rule to the independent checker. It computes the
initial replay state once, computes one post-state after each accepted add, and
returns the final state to `check`; `check` must not immediately recompute it.

Add a deterministic synthetic counter fixture that fails if either producer
or checker reintroduces a same-state duplicate. Do not simulate the large
physical space.

## B. Remove only proven hot-path duplication and enforce the existing cap

- In the v410 adjoint, evaluate `pair(dual, q.transform({k:1}))` once per old
  candidate. A nonzero result already is the required direct singleton
  pairing; do not repeat the identical transform as a same-helper assertion.
- Call the inherited `budget_check` at deterministic intervals in the
  localized-dual scan, reverse-neighbourhood/old-candidate scan, and once per
  seed formula compilation. This makes the advertised 2400-second/4.8-GB cap
  effective outside the fibre loop too. A cap hit remains typed
  `UNKNOWN_RESOURCE`, with the current profile and durable checkpoint.
- Do not add `gc.collect`, eager caches, full PB3/PB4 closure, extra matrix
  copies, full-space replay, SAT, or a self-test in production.

## C. Authenticate the durable checkpoint in the checker

For both `UNKNOWN_RESOURCE` and `COMMON_CANDIDATE`, independently read the
repo-relative `ci/out` checkpoint named by `durable_state` and check:

- exact bytes and SHA-256;
- checkpoint schema and independently derived binding;
- its internal canonical `state_sha256` seal;
- exact accepted-source list/count, rank, round, reason, and current profile
  agreement with the artifact.

Then perform the existing independent accepted-source replay and current-state
checks. Rebuild and compare the complete current profile, including normalized
N1/N2, block/label support counts, tau, unrecognized keys, required
coordinates, and any adjoint fields present. Require `terminal == status` and
fix every claim boundary: RESOURCE has A0/COMMON/NONMEMBER/fake/Ihara all
false; a positive may set only its authorized A0 candidate field.

Use a strict allowlist of typed resource prefixes. Bind unrecognized-key, tau,
unsupported-coordinate, and nonzero-K reasons to independently recomputed
values. Max-rise, time/RSS phase, and producer-exhaustion gates remain
non-promoting typed resources and need exact allowed syntax. It is sufficient
to authenticate these measured gates; do not build a second full selector or
full exhaustion engine merely to rederive them.

Tighten correction validation so `adjoint_digest` is a 64-lowercase-hex digest
and `exact_exponent_pair` is a length-two integer list before replay.

## D. Driver and pins

Create a v3 driver pinning the v3 producer/checker and retaining the exact v2
fresh-run command, 2400-second producer cap, 4.8-GB RSS cap, 64-new-rise cap,
visible progress, fixture, independent self-test/checker, and fail-closed
claims. It must require an external v3 preamble. Byte-pin all imported v1
dependencies as v2 did.

Required bounded report: exact bytes/SHA pins, compile/fixture outcomes,
single-update counter outcome, checkpoint seal mutations rejected, diff
confinement from v2, and an explicit no-production/no-GHA/no-git statement.
