# Task 157f/157g matrix contract audit

## Verdict: PASS

I found no remaining contract blocker.  The producer and checker agree on the
task-157f receipt schema and on the admissible q5 status semantics.

### Contract and provenance

- The producer computes `producer_source_sha256` from the exact GAP source at
  runtime (`search/d972_b4_burau_matrix_v1.g:41-43`) and emits the full
  task-157f contract, including matrix/block metadata, source/target digests,
  generator/A.18 orders, kernel count/canary, the ten `algorithm_evidence`
  keys, and the row data (`:177-181`).
- The checker requires the same exact evidence-key set and all values true,
  rejects `permutation_degree`, binds `source_target_key_digest`, and compares
  `producer_source_sha256` to the SHA-256 of its exact local producer path
  (`search/check_d972_b4_burau_matrix_v1.py:471-494`).
- There is no producer-side `independence` claim and no `permutation_degree`
  field.  The checker independently reconstructs the expected full 56-action
  generators, including all five finite-field blocks (`:372-385`, `:552-559`),
  so the block layout is substantive rather than decorative.

### Runtime gates

- The producer enumerates the actual kernel, checks completeness/distinctness
  and roof identity, removes an actual enumerated element, and fails closed if
  the deletion-negative cardinality check fails (`:140-146`).  The checker
  independently enumerates its reconstructed kernel and repeats the deletion
  mutation (`:568-593`); it also binds `kernel_generator_count` and generation
  of the complete kernel (`:576-585`).
- Every one of the 972 producer words is evaluated; the common word is checked
  for membership in H' before preimage/fiber construction (`:148-166`), and
  the receipt's evidence key is only set after the scan (`:169-170`).  The
  checker independently replays row keys, H' representatives, complete K
  cosets, and all defect counts (`:594-645`).

### q/status isolation

The only fixed H/H'/K/fiber calibration constants in the producer are inside
the explicit calibration branch (`search/d972_b4_burau_matrix_v1.g:171-175`).
The normal path retains candidate/UNKNOWN status logic (`:170-181`), while the
checker rejects q5 `CALIBRATION_PASS` and validates the allowed candidate or
UNKNOWN outcomes (`search/check_d972_b4_burau_matrix_v1.py:515-520`,
`:532-535`, `:637-645`).  Thus q5 constants are not injected into acceptance.

### Independent lightweight checks

- Producer SHA-256: `50c30806c0a76fa4a4a9f33755d3e6c03b41a5c086ca9542f23214205383bb91`
- Checker SHA-256: `3f19c2a17c51b80ba6ee39ce488dbebee5fe5488fc95cf1c2dd067e231bcc215`
- `python -B -m py_compile search/check_d972_b4_burau_matrix_v1.py`: PASS.
- Checker self-test: `D972_B4_BURAU_MATRIX56_CHECKER_SELFTEST_PASS` and
  `D972_B4_BURAU_MATRIX56_CHECKER_FINAL_MARKER status=PASS`.
- `--help` parses successfully; both audited files have no trailing whitespace.

No local GAP/full receipt run, git operation, or GHA dispatch was performed,
per the kickoff restrictions.
