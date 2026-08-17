# Luna task 157g — align the independent checker with the honest matrix schema

Repair only:

- `search/check_d972_b4_burau_matrix_v1.py`
- `sol/luna_reply_157d_burau_matrix_checker.md`

Do not edit/import either producer, create a workflow, run a full check/local
GAP, commit, push, or dispatch.

Replace the current schema expectations that incorrectly ask the producer to
claim `h_reconstructed_independently` / `hprime_reconstructed_independently`.
Independence belongs to this checker, not the receipt.  Require instead the
exact honest `algorithm_evidence` keys specified by task 157f:

- `faithful_full_roof_module`
- `matrix_group_h_exact`
- `derived_subgroup_exact`
- `normal_closure_equals_hprime`
- `projection_surjective_to_pprime`
- `kernel_exact`
- `kernel_elements_complete`
- `signed_word_replay`
- `all_common_words_in_hprime`
- `no_word_bound_or_sampling`

Require `producer_source_sha256` to equal the SHA256 of the exact local GAP
producer file, plus `source_target_key_digest`, generator/A.18 orders,
`kernel_generator_count`, and the actual deletion-backed kernel canary.  Do
not require or accept `permutation_degree`; require the existing matrix
dimension/block layout instead.

Keep all independent H/H'/K/fiber reconstruction and negative tests.  Add
negative fixtures for false producer-independence metadata, wrong source hash,
missing deletion canary, and a misleading permutation-degree substitution.
The result should be schema-admissible once a task-157f receipt is supplied,
while still fail-closing on the old receipt.

Run `py_compile`, `--self-test`, `--help`, and `git diff --check`; update the
reply verdict and hashes.
