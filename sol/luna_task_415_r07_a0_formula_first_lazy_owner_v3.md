# Luna task 415: R07 A0 formula-first lazy owner v3

Role: Luna implementation only.  Process all sections in order.  Do not run
heavy production locally, dispatch GHA, commit, push, build PB3/PB4 closures,
or construct the full task179 FibreOracle/Q0 tables.

## 1. Frozen input and purpose

Use the current task413 v2 owner as the frozen mathematical baseline:

- `search/d972_r07_a0_compact_positive_lazy_owner_v2.py`
- `crosscheck/check_d972_r07_a0_compact_positive_lazy_owner_v2.py`
- `search/d972_r07_a0_compact_positive_lazy_owner_gha_driver_v2.g`

V2 already has the exact lazy boundary separation oracle, normalized
`(epsilon/18) mod 3` coordinates, cursor resets, one resource-stop
checkpoint, and honest `COMMON_CANDIDATE` semantics.  Preserve all of these.

The sole production change is to avoid constructing a full all-seven sparse
correction column when its pairing with the current dual is zero.

## 2. Required formula-first correction oracle

For each compact relator and current dual:

1. Make task179 `AllSevenModel.occurrence_data` executable by supplying its
   adapter with both `packed_joint_blob` and the already-loaded task176
   `value_from_blob`.  Do not build qstates, stores, A_maps, parents, or any
   FibreOracle data.
2. Call `occurrence_data(relator, dual_R)` once, where `dual_R` contains only
   the physical `R` coordinates.  Replace its raw exponent constant by

   ```text
   dual[N1] * (epsilon_x(relator)/18 mod 3)
   + dual[N2] * (epsilon_y(relator)/18 mod 3)  mod 3.
   ```

3. For each delta in the unchanged deterministic v2 schedule, obtain its ten
   coordinate blobs directly from `runtime.states_direct(delta)` and the
   frozen packed element encoder.  Evaluate the exact scalar

   ```text
   K + sum coefficient * [delta_blob[coordinate] == target_blob] mod 3.
   ```

4. If the scalar is zero, do not call `direct_column`.
5. If it is nonzero, call `direct_column` once, normalize its exponent rows,
   and fail closed unless its direct pairing with the dual equals the formula
   scalar.  Return that row with literal ancestry.

This is only an accelerator for the same bounded positive schedule.  It is
not an exhaustive negative oracle.  Schedule exhaustion remains
`UNKNOWN_RESOURCE`.

Expose counters for formula candidates examined and full columns
materialized.  Do not retain all coordinate blobs or all candidate rows.

## 3. Outputs

Create only:

- `search/d972_r07_a0_formula_first_lazy_owner_v3.py`
- `crosscheck/check_d972_r07_a0_formula_first_lazy_owner_v3.py`
- `search/d972_r07_a0_formula_first_lazy_owner_gha_driver_v3.g`
- `sol/luna_reply_415_r07_a0_formula_first_lazy_owner_v3.md`

The driver is PRODUCTION-only, needs no GAP preamble, uses unbuffered Python
and `tee`, and gives the producer a 6000-second controlled slice.  Pin every
source byte count and SHA-256.

## 4. Bounded gates only

Run `py_compile`, help/AST parsing, the inherited small fixture, and a small
synthetic formula/direct-pair equality mutation test.  Statistically assert
that the candidate loop calls `direct_column` only inside the nonzero-scalar
branch.  Do not run the actual 31 MB roof production locally.

## 5. Claim boundary

The only possible positive terminal remains `COMMON_CANDIDATE` until strict
typed-boundary/all-seven replay is performed.  Never emit NONMEMBER,
COMMON_WORD, fake, Ihara witness, or exhaustive-completeness claims.
