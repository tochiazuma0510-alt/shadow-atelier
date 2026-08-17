# Luna task 157d — independent checker for matrix-56 receipts

Implement a helper-nonsharing Python checker for receipts emitted by:

- `search/d972_b4_burau_matrix_v1.g`

Authorized files:

- `search/check_d972_b4_burau_matrix_v1.py`
- `sol/luna_reply_157d_burau_matrix_checker.md`

Do not modify/import the GAP producer or the tuple v3 producer, create a
workflow, run a full local receipt check/GAP, commit, push, or dispatch.
Lightweight selftests/negative fixtures are allowed.

The checker must independently reconstruct the frozen 36-point roof, finite
field arithmetic (including GF(4)), literal Burau/A.18 tuple generators, word
artifact and all frozen hashes.  It must decode the 56 by 56 matrices into the
full roof block plus five distinct 4 by 4 blocks and reject any off-block or
field-encoding drift.

For a production receipt, independently and exactly reconstruct H', its roof
image, and the complete kernel with a finite normal-closure plus exhaustive
signed Schreier traversal (or another proved complete exact algorithm).  Do
not trust the producer's H/H'/K orders, kernel generators, finite caps, or
representatives.  Recompute H/H' orders and compare all recorded values.

For each of 972 ordered unique rows, bind the target key and common word,
decode h0, require h0 in the independently reconstructed H' with the correct
roof, enumerate the full h0*K fiber, recompute every paper-convention A.18
defect/count and witness, and compare the receipt.  Recompute terminal status:
zero identity fiber is candidate-only; all-pass is UNKNOWN.  Apply frozen
q3/q4 values only to calibration receipts, never to q5.

Require exact schema/final marker/source/frozen hashes, algorithm evidence,
block layout, generator/A.18 ordering, and reconstructability fields.  Add
negative selftests for truncated kernel, bad matrix block, reversed product,
duplicate key, forged count/status, and q5 calibration-value injection.

Document the completeness proof and runtime risk.  Run `py_compile`,
`--self-test`, `--help`, and `git diff --check`; report hashes.  If the current
receipt schema lacks data required for a sound check, return a precise BLOCKER
instead of weakening the checker.
