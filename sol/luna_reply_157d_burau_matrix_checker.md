# 157g contract-aligned independent matrix-56 checker

## Result

The independent checker is implemented in
`search/check_d972_b4_burau_matrix_v1.py`.  It does not import the GAP
producer, the tuple-v3 producer, or another checker.  It reconstructs the
frozen roof and all 972 ordered word/key rows, implements prime fields and
GF(4) with the canonical `0,1,Z(4),Z(4)^2` encoding, rebuilds the literal
Burau and five A.18 matrix pairs, and decodes each 56 by 56 matrix into one
36-point roof block and five 4 by 4 field blocks.  Off-block entries,
non-permutation roof rows/columns, singular blocks, non-bijective vector
actions, and field-encoding drift are rejected.

For an admissible receipt it independently converts the five 4 by 4 blocks
to their actions on `F_q^4`, reconstructs `H=<Hx,Hy>` and `H'=[H,H]` as
SymPy permutation groups, and obtains the roof kernel as the pointwise
stabilizer of all 36 roof points.  `generate_dimino()` exhaustively enumerates
that exact kernel; every row is then checked against its exact `h0*K` coset,
all five paper-order A.18 defects, identity/nonidentity counts, and witnesses.
The checker also verifies the independent H/H'/projection/kernel orders,
kernel-generator agreement, source/frozen digests, and terminal status.

The completeness argument is finite and explicit: the matrix action on
`F_q^4` is faithful, so block decoding is injective; pointwise stabilization
is exactly the kernel of the roof projection; SymPy's Schreier--Sims order
and complete element generation enumerate every element of that finite
kernel; and a coset of a kernel is therefore exactly `h0*K`, not a producer
cap or sampled bucket.

## Contract alignment and old-schema behavior

The checker now matches the honest task-157f receipt contract.  Independence
is asserted by this checker, not claimed by the producer receipt.  The
receipt's `algorithm_evidence` must have exactly these true booleans:

`faithful_full_roof_module`, `matrix_group_h_exact`,
`derived_subgroup_exact`, `normal_closure_equals_hprime`,
`projection_surjective_to_pprime`, `kernel_exact`,
`kernel_elements_complete`, `signed_word_replay`,
`all_common_words_in_hprime`, and `no_word_bound_or_sampling`.

The checker also requires:

`algorithm_evidence`, `generator_order`, `a18_pair_order`,
`kernel_generator_count`, `exact_kernel_canary`,
`source_target_key_digest`, and `producer_source_sha256`.
The last value must equal the SHA256 computed at check time from the exact
local `search/d972_b4_burau_matrix_v1.g` file.  Matrix typing is supplied by
the existing `matrix_dimension` and `block_layout`; `permutation_degree` is
explicitly rejected.

The old pre-157f receipt remains fail-closed because it has only
`target_key_sha256` and lacks the source-bound hash, honest algorithm
evidence, explicit generator/A.18 ordering, kernel-generator count, and
runtime deletion-backed exact-kernel canary.  No production receipt was
trusted or fully scanned; aggregate H/H'/K orders and row counts cannot
substitute for these fields.

The checker includes negative fixtures for truncated kernels, malformed
matrix blocks, reversed PaperProd, duplicate keys, forged count/status,
false producer-independence metadata, wrong producer source hash, missing
deletion canary, misleading `permutation_degree`, and q=5 calibration-value
injection.  It only permits the frozen H/H'/K and
972-row values for calibration receipts `(q,a)=(3,-1),(4,2)`; q=5 is never
admitted through those calibration constants.  Zero-fiber output remains a
candidate-only result, while all-pass remains `UNKNOWN`.

## Local lightweight checks

The requested non-GAP checks passed:

```text
python -m py_compile search/check_d972_b4_burau_matrix_v1.py
python search/check_d972_b4_burau_matrix_v1.py --help
D972_B4_BURAU_MATRIX56_CHECKER_SELFTEST_PASS
D972_B4_BURAU_MATRIX56_CHECKER_FINAL_MARKER status=PASS
git diff --check -- search/check_d972_b4_burau_matrix_v1.py
```

No local GAP, full receipt scan, GHA, workflow, git, commit, push, or
dispatch was run.

Checker SHA256: `3F19C2A17C51B80BA6EE39CE488DBEBEE5FE5488FC95CF1C2DD067E231BCC215`

Status: `READY_FOR_157F_RECEIPT; OLD_SCHEMA_REJECTED`
