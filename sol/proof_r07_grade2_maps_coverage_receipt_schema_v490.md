# R07 grade-two maps coverage-receipt schema repair v490

Actual run `33812912839/1` authenticated the v3 sources, passed both
selftests, emitted all 40 sparse tables, authenticated the producer roster,
and independently regenerated/compared every table.  It stopped at
`structural_receipt:T_coverage`.

The two independent coverage computations have the same values but different
source-field names.  Producer v3 emits

```text
source_coordinates, tags, components, monomials, psl_indices
```

where checker v3 emits

```text
source_coordinates, source_tags, source_components,
source_monomials, source_psl_indices.
```

Both already emit the same `destination_*` fields.  Consequently the strict
manifest comparison rejects before any mathematical value can differ.  This
is a finite receipt-schema mismatch; it is not a sparse-map, transpose,
inverse, prefix, coverage, or resource failure.

The producer artifact schema is the release source of record.  A checker v4
must rename only those four source keys to `tags`, `components`, `monomials`,
and `psl_indices`, update its own bounded fixture accordingly, and pin the
unchanged producer v3.  Its independent enumeration and all comparisons stay
unchanged.  The actual build/check must then be rerun from fresh output.

```text
CLASSIFICATION=FINITE_CHECKER_RECEIPT_KEY_REPAIR
ACTUAL_MAP_ARTIFACT=NOT_YET_ACCEPTED
GRADE2_DECISION=NOT_RUN
verified=false
```
