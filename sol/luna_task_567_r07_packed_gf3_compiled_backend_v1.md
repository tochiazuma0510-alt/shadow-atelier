# Luna Task 567: compiled packed-GF(3) elimination backend candidate (v1)

Author: Sol / 2026-09-03

## 1. Objective and boundary

Implement a small compiled backend for the exact packed base-three echelon
operation used by the audited grade-one v4 merge and needed at larger scale
by grade two.  The current GHA runs are immutable: do not alter, cancel or
dispatch them.  This task produces a candidate backend and seconds-scale
equivalence fixtures only.  It is not authorized for production until an
independent audit and a separate GHA calibration.

The performance defect to remove is millions of Python-to-NumPy calls, one
for each pivot elimination.  Do not change row order, pivot policy, field,
membership, dual, or ancestry semantics.

## 2. Allowed output files

Write only:

1. `search/d972_packed_gf3_echelon_backend_v1.c`;
2. `search/d972_packed_gf3_echelon_backend_v1.py`;
3. `search/check_d972_packed_gf3_echelon_backend_v1.py`;
4. `sol/luna_reply_567_r07_packed_gf3_compiled_backend_v1.md`.

Do not edit v3/v4, Task565 files, workflows, certificates, v220 or
provenance.  Do not commit, push, dispatch GHA, install into the repository,
or run a real merge.  Temporary build products, if any, belong outside the
repository.  This machine has no guaranteed local C compiler; absence of one
is not a blocker to writing the source and running the pure reference fixture.

## 3. Exact algebra and ABI

Rows use the frozen four-trits-per-byte encoding: each byte is in `0..80`
and stores four coefficients of `F3` with weights `(1,3,9,27)`.  The backend
must support a row-major packed input file and deterministic insertion in
file order.  It must return versioned binary/JSON receipts sufficient to
recover:

- accepted basis rows in insertion order;
- unique pivot lead for each basis row;
- for every offered input row, the ordered `(pivot,coefficient)` reduction
  list, accepted/dependent flag, normalization scale and new pivot when
  accepted; and
- reduction of one separately supplied target row, including its complete
  coefficient list and remainder.

The accepted-row identity must match the v4 `PackedEchelon` exactly.  A row
is repeatedly reduced at its first nonzero coordinate by the already stored
row with that lead.  A new row is normalized to leading coefficient one;
coefficient two uses multiplication by two.  Pivot IDs are insertion order,
not sorted-lead order.

It is legal to update only from the packed byte containing the current lead
to the end, but the source and checker must prove and test the invariant that
every stored pivot row is zero in all earlier bytes.  Do not silently replace
full-row v4 AXPY without that gate.  All integer bounds, file lengths,
allocation products and ledger offsets need overflow checks.  Malformed
bytes, duplicate leads, truncated files or a resource cap fail closed.

The C program should be a portable C11 command-line worker using only the
standard library, with explicit version/schema arguments.  The Python file
is a fail-closed wrapper/reference/receipt parser; production callers must
never fall back silently to the slow reference path.  The worker may use
memory mapping or bounded buffered I/O, but must not retain duplicate full
input and basis matrices.

## 4. Certificate semantics

The backend is only a linear-algebra primitive.  It must not claim that its
input roster is complete.  The caller remains responsible for source actor
closure, physical aggregation, PB3/PB4/exponent gates and literal ancestry.
The backend's ledger is allowed to carry caller-supplied opaque row IDs so a
caller can reconstruct the existing physical DAG without changing its
meaning.

For MEMBER, direct replay of the returned coefficients against the original
rows and equality with the target is load-bearing.  For NONMEMBER, this task
does not need to construct the final dual; expose the complete echelon and
remainder so the existing audited dual construction can run, and state that a
production NONMEMBER still needs independent annihilation of every original
row plus nonzero target pairing.

## 5. Mandatory bounded tests

The independent checker must not import the wrapper or C source.  It should
implement a small dense F3 reference and compare complete receipts on at
least:

1. the six frozen v3/v4 equivalence cases from Task562;
2. randomized deterministic matrices with zero, dependent, scale-two and
   out-of-lead-order pivots;
3. a row with multiple nonzero trits in the same pivot byte;
4. suffix-update versus full-row-update equality;
5. MEMBER target coefficients and NONMEMBER remainder;
6. opaque row-ID round trip and deterministic resume boundary;
7. rejection of one mutated byte, lead, coefficient, ledger offset, schema
   and truncated file; and
8. one bounded benchmark large enough to report reference/compiled timings
   when a compiler is available, but capped to seconds and never using the
   production artifacts.

If no local compiler exists, run `py_compile` and all pure reference/parser
fixtures, state `COMPILED_FIXTURE_NOT_RUN_NO_COMPILER`, and leave actual C
execution for the separately audited GHA calibration.  Do not manufacture a
speedup number.

## 6. Reply

Record exact files, bytes, SHA-256, commands, runtimes, compiler availability,
tests run and limitations.  End with exactly one verdict:

```text
PACKED_GF3_BACKEND_V1_CANDIDATE_AUDIT_REQUIRED
PACKED_GF3_BACKEND_V1_BLOCKED
```

State explicitly:

```text
CURRENT GRADE-ONE RUNS: unchanged
GRADE-TWO PRODUCTION: not launched
MATHEMATICAL TERMINAL: none
verified=false
```
