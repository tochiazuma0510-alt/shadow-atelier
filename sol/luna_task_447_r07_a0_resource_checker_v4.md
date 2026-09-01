# Luna task 447 — R07 A0 resource-checker closure v4

Role: Luna implementation owner. This is the final narrow checker repair over
Task445. The v3 producer is frozen and must not be changed or copied. Do not
run production, Q0, GHA, git commit, or push. Bounded checker/driver tests only.

Read Task445 instruction/reply and v3 producer/checker/driver in full, plus the
independent NO-GO audit supplied by the parent.

## Authorized outputs only

1. `crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v4.py`
2. `search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v4.g`
3. `sol/luna_reply_447_r07_a0_resource_checker_v4.md`

Temporary files stay outside the repository.

## Exact repairs

1. Thinly version the v3 checker. In complete adjoint profiles, independently
   count producer-equivalent `localized_dual_support`: every non-N, parsed,
   non-tau localized dual key. Add it before complete profile equality. Do not
   import the producer or trust its profile.
2. A RESOURCE terminal requires the replayed current dual to be non-None.
   A COMMON_CANDIDATE requires dual None, `reason is None`, and
   `current_dual_profile is None`, in addition to the existing positive replay.
3. Bind `durable_state.accepted_count` and `durable_state.rank` to both parsed
   checkpoint and artifact, in addition to existing path/bytes/SHA and internal
   state checks.
4. Replace the arbitrary time/RSS suffix allowance by the exact phases reachable
   inside the authenticated v3 try block:

   - `tau_free_localized_dual`
   - `tau_free_reverse_neighbourhood`
   - `tau_free_old_candidates`
   - `tau_free_formula_seed`
   - `tau_free_candidate`
   - `fine_deletion`
   - `selective_Q0`
   - `selective_membership_S0`
   - `selective_membership_S1`
   - `selective_membership_S2`
   - `L_subgroup_closure`
   - `coarse_inverse_build`

   For each and only each, allow exactly
   `UNKNOWN_RESOURCE:<phase>:time_limit` and
   `UNKNOWN_RESOURCE:<phase>:rss_limit`. Retain the existing exact non-budget
   reasons and exact coordinate-reason parser. Do not broaden the list.
5. Extend bounded mutations to reject a missing localized count, RESOURCE with
   no dual boundary, COMMON with a reason/profile, drifted durable metadata,
   and an invented time/RSS phase.

Create a v4 driver that pins the unchanged v3 producer at 12,215 bytes /
`0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`
and the new v4 checker. Retain fresh paths, 2400 seconds, 4.8 GB, 64 rises,
single production process, exact checkpoint check, visible markers, and an
external v4 preamble. No production SELFTEST or new computation.

Report exact bytes/SHA, checker self-test/mutations, static driver pins and
commands, diff confinement, and explicit no-production/no-GHA/no-git.
