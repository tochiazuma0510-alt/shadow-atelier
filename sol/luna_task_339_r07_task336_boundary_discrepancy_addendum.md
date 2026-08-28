# Luna task 339 - task336 boundary-discrepancy addendum

Role: Luna, binding addendum to the currently active task336.  Read this FULL
mail and `sol/proof_r07_lazy_kernel_boundary_discrepancy_v273.md` first to
last before closing any v4 output.  Do not create a sixth output and do not
execute anything.  The five task336 outputs remain the sole permitted edits.

## 1. Supersession

V273 supersedes task336 Section 7 wherever a retained K representative and
its literal source word are implicitly treated as having identical raw Fox
defects.  They agree only modulo the full translated-boundary space D.

Every K item must retain `(representative, literal_word,
raw_boundary_discrepancy)` and satisfy exact v273 (4.5).  The discrepancy is
a coefficient-bearing immutable ledger in raw symbols `(coordinate,
base_relator,translation)`, not a mutable current-B pivot vector or Boolean.

## 2. Required recurrence

Export all internal reduction coefficients in the fixed convention

```text
r = v - Psi(Q) - sum(c_l*k_l),     k_new = s*r.
```

If the candidate word has raw defect `v+Psi(E_v)` and prior K word l has raw
defect `k_l+Psi(E_l)`, construct the registered literal word and ledger

```text
W_new = (W_v * product_l W_l^(-c_l))^s
E_new = s*(E_v + Q - sum_l c_l*E_l).
```

For an initial presentation word use `E_v=0`.  For the source conjugate
`a W_p a^-1`, use representative `a*k_p` and ledger obtained by actual left
translation of every raw key in `E_p` by the matching context value of a.

Producer and checker must independently flat-evaluate the literal word,
representative, and raw ledger and require exact equality in the ten-tagged
raw affine module.  Equality only modulo discovered B is insufficient.

## 3. Performance and mutations

Use persistent sparse maps/DAGs and charge ledger actions, combinations,
duplicate collection, expansion, and replay.  Add actual-owner mutations for
omitted candidate discrepancy, omitted prior-K discrepancy, flipped Q sign,
missing scale, reversed source action, changed raw tag/translation, and
modulo-B-only replay.  Extend the identical producer/checker mutation roster;
do not replace earlier commissioned mutations.

The task336 reply must state the exact recurrence, raw-ledger grammar, static
initial/conjugate traces, direct replay path, operation bounds, and mutation
owners.  Actual A4 remains at most 1/3 before an independently accepted run.

`TASK339_R07_TASK336_BOUNDARY_DISCREPANCY_ADDENDUM`
