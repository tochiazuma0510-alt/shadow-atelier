# Luna reply 413 — R07 A0 compact positive-first lazy owner v2

## F1 Scope

All numbered sections 1–7 were processed in order. Only the four task413
outputs were created. Task411 and task179 were not modified; no obsolete
checkpoint was read or resumed, and no local heavy production run, GHA
dispatch, commit, or push was performed.

## F2 Implemented owner

The new producer byte-pins task411 (the direct task198 v12/v6 bootstrap),
reuses its authenticated compact roster construction, and enforces the 44-row
digest
`7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8`.
It checks exponent divisibility by 18, uses task179's eleven-occurrence
`AllSevenModel` direct/full-column equality gate, and keeps boundary
translations lazy. The 2+2+11 boundary rows are reconstructed directly from
the accepted `pure_relations(3/4)` Fox gradients; no PB3/PB4 closure table or
frontier is built.

The positive loop inserts only rank-raising base boundary and identity
correction columns, with normalized `(epsilon_x/18,epsilon_y/18) mod 3`
coordinates on every correction column and zero coordinates on boundary and
target rows. It constructs an exact triangular dual, calls the lazy
support-times-occurrence boundary oracle with `t*h=g`, and then runs a
bounded on-demand correction schedule over the compact 44 relators. Every
dual-changing rank increase resets both correction cursors to zero. A
resource/no-hit result is `UNKNOWN_RESOURCE` or `UNKNOWN`, never NONMEMBER.
Checkpoint state is gzip+marshal with chunk hash verification, atomic
replacement, compact echelon/interner/ancestry, cursor, and binding digest.

## F3 Checker and bounded gates

The checker is a narrow positive-receipt checker and never imports the new
producer. For a positive receipt it independently reconstructs the compact
words, selected conjugate factors, v399 exactification, exponent `(0,0)`, and
typed boundary-record shape; UNKNOWN terminals are checked for no overclaim.

Passed:

```text
py_compile producer/checker: PASS
producer --mode FIXTURE: FIXTURE_PASS
checker --fixture: CHECKER_FIXTURE_PASS
producer --help: PASS
```

The actual A0 production path was not run locally, as required. The driver
uses unbuffered output with `tee`, a 6000-second slice, and the exact producer
and checker pins below.

Resource stops during the positive scan write the current rows, ancestry,
dual-bound correction cursors, and binding digest to the atomic checkpoint.
The positive terminal is conservatively `COMMON_CANDIDATE`: strict typed
boundary/all-seven sparse replay is not claimed by this bounded discovery
owner. Thus this output is positive-discovery only and is not an exhaustive
negative oracle.

The focused dispatch audit removed one unused `weighted_support` pass whose
runtime lacked the full task179 section ABI.  Correction selection now uses
only the exact `direct_column` scalar that was already decisive.  It also
removed periodic full-echelon checkpoint copies: one sealed snapshot is
written on the controlled resource stop.  The lazy boundary hot loop updates
sparse rows in place and no longer retains contributor lists for inactive
translations.

## F4 Remaining ABI blocker

The direct task411 adapter exposes the exact occurrence model and lazy
boundary inputs, but not task179's authenticated Q0 section/fibre tables
(`stores`, `A_maps`, `qstates`, `parents`, and kernel generators). Building
those through task179's `build_runtime()` would enumerate the forbidden full
Q0/6,441 roster. Therefore this snapshot contains a deterministic bounded
on-demand shortlex/compact correction schedule plus the exact
`occurrence_data`/support calculation, but it must not be advertised as the
full task179 FibreOracle fairness certificate until the missing lazy section
ABI is supplied. No common word, fake, or Ihara witness is claimed.

## F5 Exact hashes

```text
search/d972_r07_a0_compact_positive_lazy_owner_v2.py
  bytes=26148
  sha256=72cb540056bd812d466e22f90f8ed048b9cfe4821806b0a9e0cab82059c1b403

crosscheck/check_d972_r07_a0_compact_positive_lazy_owner_v2.py
  bytes=5117
  sha256=9998192818fd8ba780e7329df552fd8a5df60c7a3da9e9ec8781abc708bb519c

search/d972_r07_a0_compact_positive_lazy_owner_gha_driver_v2.g
  bytes=2286
  sha256=f6f7c979825e38f9a1e1d1121c89f99f84e6460eb1617130d5f51bfb30a80d1e
```

The driver is intentionally not marked production-ready while the exact
task179 lazy fibre/global candidate ABI remains unavailable.
