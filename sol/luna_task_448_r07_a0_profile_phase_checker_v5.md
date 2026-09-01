# Luna task 448 — R07 A0 profile-phase checker v5

Role: Luna implementation owner. Final one-condition repair over Task447 v4.
Do not change/copy the v3 producer. No production, GHA, git, Q0, or new tests
beyond bounded checker/static driver gates.

## Authorized outputs only

1. `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v5.py`
2. `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v5.g`
3. `sol/luna_reply_448_r07_a0_profile_phase_checker_v5.md`

Read Task447 and its three outputs in full.

## Sole semantic repair

The frozen v3 producer adds `localized_dual_support` only after the complete
adjoint returns (`current.update(adj)`). Pre-adjoint resource profiles —
unrecognized key, nonzero tau, max-rises, and a budget stop before adjoint
completion — correctly do not contain it.

Thinly version the v4 checker so:

- if and only if the claimed profile contains `adjoint_digest`, require and
  independently reconstruct `localized_dual_support`, remove that one field
  for the inherited v3 complete-profile comparison, and compare the count;
- if no `adjoint_digest` is present, require no
  `localized_dual_support` field and delegate the unchanged complete basic
  profile to the v3 checker.

Keep every other v4 gate byte-semantically unchanged: dual/status boundary,
durable metadata, exact 12-phase allowlist, coordinate parsing, checkpoint
authentication, claims, and positive replay.

Add bounded fixtures for both valid profile shapes and mutations adding or
deleting the localized field in the wrong phase. Create a v5 driver that pins
the frozen 12,215-byte v3 producer and the v5 checker, with the exact v4
production command/caps/fresh paths and no production fixture/self-test.

Report bytes/SHA, bounded outcomes and exact no-production/no-GHA/no-git.
