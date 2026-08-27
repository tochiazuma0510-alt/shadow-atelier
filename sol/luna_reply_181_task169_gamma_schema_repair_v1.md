# Luna reply 181: task169 Gamma schema repair v1

Date: 2026-08-27  
Role: Luna / implementation and static audit only  
Outcome: checker schema repair applied; local execution and GHA dispatch were not performed.

## Exact repair

The producer's `Gamma_invariants` field remains the explicitly named 19-key
projection. The helper-nonshared checker now:

1. freezes and requires the exact 19-key set;
2. requires the authenticated predecessor `gamma` to have the exact 25-key
   public schema;
3. compares the producer field with the projection of the pinned public
   object onto the 19 invariant keys; and
4. independently replays the 243-state state-row and transition digests.

The prior whole-dictionary comparison at checker line 1010 was therefore
replaced by the typed projection plus the unchanged independent digest gates.
The producer was not changed and no public packed fields were copied under
`Gamma_invariants`.

## Expected key sets

The exact producer invariant key list, in frozen source order, is:

```text
order
edge_count
generator_count
greedy_generator_state_ids
greedy_generator_count
max_section_factors
order_distribution
exponent
center_order
derived_order
cube_subgroup_order
frattini_order
frattini_quotient_order
frattini_dimension_F3
derived_in_center
conjugacy_class_size_distribution
normal_under_x_y
state_rows_sha256
transition_rows_sha256
```

The six public-only keys intentionally excluded from `Gamma_invariants` are:

```text
canonical_state_key
canonical_states
first_seen_BFS
section_parent_generators
section_parent_states
transitions
```

The authenticated predecessor `gamma` is required to contain exactly the
union of those two lists (25 keys).

## Normal-path mutation probes

`gamma_schema_probe()` constructs a valid 243-state/transition fixture and
sends the valid row through the same `validate_gamma_replay()` path used by
`independent_domain_check()`. It rejects all five load-bearing mutations:

```text
missing_invariant_key
extra_public_section_key
changed_invariant_value
changed_state_row_digest
changed_transition_row_digest
```

The probe is run by normal `check_receipt()` and directly at checker
`--self-test` entry. Its result is retained under `gamma_schema_probe`; the
checker pass marker carries `gamma_schema_mutations=5`. The task169b
preflight driver now requires that exact marker from the checker process.
All failures remain `RuntimeError` hard stops.

## Changed files and static identities

```text
94904  46623966a71d1c9f2aa0f86f6f1e5fdf74098b4ecd5a76b4c2713eb8a33bbc95  crosscheck/check_d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py
27068  a303205139b4f00aa0bb9426a515b26dd9bfdff796d923350ec56fd0d5027966  search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_gha_preflight_driver_v1.g
```

The producer is unchanged:

```text
111249  f7d80db6197224b2096d8034e2bccc7f3f62956cc0454727156652131cfaf0c7  search/d972_r07_760_l3_target6_joint_kernel_coeff_intersection_v1.py
```

No task169 immutable selftest certificate exists in the checked-in
`search/certs` directory, so no certificate was edited. No task175/task176/
task179 file, proof, workflow, or predecessor file was changed.

## Static audit boundary and rerun requirement

Only PowerShell read/size/hash scans and source edits were used. Python, Node,
GAP, git, and GHA were not run. The previous run's CANDIDATE receipt was not
promoted. Parent-controlled serial GHA production must rerun the two producer
generations and checker after the checker pin update; the repair does not
assert any mathematical terminal.

```text
TASK169_GAMMA_INVARIANTS_SCHEMA_REPAIR_APPLIED
```
