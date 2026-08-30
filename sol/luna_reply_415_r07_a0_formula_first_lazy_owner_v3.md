# Luna reply 415 — R07 A0 formula-first lazy owner v3

Processed all numbered sections 1–5 in order. Only the four task415 outputs
were created; task411/task413/task179 were not modified. No heavy production
run, GHA dispatch, commit, or push was performed.

The producer byte-pins task413 v2 and replaces only its correction oracle.
For each compact relator it calls `occurrence_data(relator, dual_R)` once,
replaces the raw exponent constant with the normalized epsilon/18 N1/N2
constant, and obtains candidate coordinate blobs from the direct runtime
state tuple plus the frozen packed encoder. A zero formula scalar skips
`direct_column`; a nonzero scalar materializes exactly one full column and
checks its direct pairing against the formula scalar. Counters
`formula_candidates_examined` and `full_columns_materialized` are attached
to the result. Existing v2 lazy-boundary separation, normalized correction
rows, cursor reset, checkpoint, and `COMMON_CANDIDATE` semantics are kept.

The checker is narrow and accepts only UNKNOWN/UNKNOWN_RESOURCE or the honest
COMMON_CANDIDATE terminal; it never claims COMMON_WORD, NONMEMBER, fake, Ihara,
or exhaustive completeness. The driver is PRODUCTION-only, unbuffered, uses
`tee`, and supplies a 6000-second slice.

Bounded gates passed:

```text
py_compile producer/checker: PASS
producer --mode FIXTURE: FIXTURE_PASS
checker --fixture: CHECKER_FIXTURE_PASS
producer --help: PASS
```

The fixture includes the inherited v2 fixture, AST/branch assertion that the
zero-scalar path does not call `direct_column`, a synthetic direct-pair branch
test, and checkpoint mutation coverage inherited from v2. Actual roof
production was not run locally.

Exact hashes:

```text
search/d972_r07_a0_formula_first_lazy_owner_v3.py
  bytes=6254
  sha256=657f12e4c7f52dd8012e55a7e775a518c532f1d2b0e4735f88a9adfd7fb9e01c

crosscheck/check_d972_r07_a0_formula_first_lazy_owner_v3.py
  bytes=2227
  sha256=efbbfafad0aa156b9b2d7d9cfafaba775597d24269760fe93aee4f8cace4c91a

search/d972_r07_a0_formula_first_lazy_owner_gha_driver_v3.g
  bytes=2281
  sha256=0c9303a4fc701786bcf2350fe686ae77eeff2f231b869cbf7a9ee368dbd0e6ec
```
