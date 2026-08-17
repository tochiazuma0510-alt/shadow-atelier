# Luna task 157f — make matrix receipt independently admissible

Read `sol/luna_reply_157d_burau_matrix_checker.md`.  Repair only the GAP
producer/schema side in:

- `search/d972_b4_burau_matrix_v1.g`
- `sol/luna_reply_157f_matrix_receipt_contract.md`

Do not edit the checker/workflow, run local GAP, commit, push, or dispatch.

Add an honest structured receipt contract and corresponding runtime gates:

- `producer_source_sha256`, computed from the exact producer file at runtime;
- `source_target_key_digest` (retain existing frozen digest fields);
- `generator_order=[x12,x13,x14,x23,x24,x34]`;
- `a18_pair_order=[123,234,12,3,4;1,23,4;1,2,34]` using the exact existing
  string spellings from v2;
- `kernel_generator_count`;
- `exact_kernel_canary` with complete order, distinctness, roof identity,
  and a runtime deletion-negative test using the actual enumerated K;
- `algorithm_evidence` with exactly these honest booleans:
  `faithful_full_roof_module`, `matrix_group_h_exact`,
  `derived_subgroup_exact`, `normal_closure_equals_hprime`,
  `projection_surjective_to_pprime`, `kernel_exact`,
  `kernel_elements_complete`, `signed_word_replay`,
  `all_common_words_in_hprime`, `no_word_bound_or_sampling`.

Do not claim producer-side "independence" and do not add a
`permutation_degree` field: this is a 56-dimensional matrix representation,
already typed by `matrix_dimension` and `block_layout`.

The actual deletion gate must fail if one enumerated kernel element is
removed; do not merely print a boolean.  Keep q5 order/counts unconstrained,
candidate/all-pass semantics unchanged, and q3/q4 calibration-only constants.

Run static source/field/contract checks and `git diff --check`; report new
hashes.  The parent will re-run the GHA campaign because the current run
predates this receipt-contract repair.
