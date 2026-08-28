# Luna task 260 — task232 projection-coordinate owner repair v1

Role: bounded implementation repair only. Read task232, task244b, task252,
task256, and all current five task232 files in full. Do not run Python, Node,
GAP, git, GHA, or network. Edit only those five task232 files plus the existing
task232 Luna reply.

## Exact parent rejection

Task256 required all seven projection-anchor mutations to own the seven
selected-anchor objects. Six now do, but `projected_coordinate` still mutates
the duplicate top-level `basis_projections` list rather than
`projection_anchor.projected_coordinate`, in both producer and independent
checker. It happens to be rejected by the receipt-list consistency gate, but
that is not a mutation of the commissioned owner and does not test the anchor
equality itself.

## Required repair

1. In producer and checker independently, make the `projected_coordinate`
   mutation change only `projection_anchor.projected_coordinate` to a
   nonidentical value. Retain the other six selected-anchor owners exactly.
2. Ensure validation reconstructs the projected-coordinate vector from every
   basis receipt and compares the selected anchor's serialized coordinate to
   it. The mutation must be non-vacuous and rejected by that owning gate.
3. Do not change H2 arithmetic, basis receipts, source words, K construction,
   production semantics, terminal vocabulary, mutation roster, or downstream
   flags. Inspect the complete five-file set for another direct violation of
   task256 but do not widen scope.
4. Refresh exact driver pins and reply identities. Report UNEXECUTED; parent
   Sol will run GHA.

A4 remains 0/3; SELFTEST itself does not increment the actual v220 gate.
