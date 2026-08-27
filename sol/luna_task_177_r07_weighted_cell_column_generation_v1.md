# Luna task 177 — R07 weighted-cell all-seven column generation v1

Author: Sol / 2026-08-27

Role: Luna implementation and GHA computation.  The mathematics is fixed by
v110, v125, v129, and v132.  Do not replace the linked context group by a
direct product, do not solve H1/H2/P separately, and do not interpret a cap
as a separator.

## 1. Objective

Build a fail-closed producer, helper-nonshared checker, ASCII GAP/GHA driver,
immutable SELFTEST fixture, and Luna reply for the exact membership

\[
 (-T_{H1},-T_{H2},-T_P,0,0)
 \in D_{\rm all}+\operatorname{span}
 \{V_{\delta,r}:\delta\in\Delta_{\rm all},
 r\in\mathcal R_\Omega\}.
\]

On the positive branch, return one word-bearing common correction and replay
both hexagons plus the printed-order pentagon.  On the negative branch, return
an exact dual only after every correction and boundary correlation has been
proved zero by v132.  Any missing prerequisite, lazy query, word section,
or resource is typed UNKNOWN.

This task stops after the first common all-seven word.  The intrinsic
v129 \((d,\rho)\) solve, cyclic inverse-limit v133 test, nonabelian chief
choices, cofinal lift, fake, and Ihara claim are outside this implementation.

## 2. Frozen prerequisites and promotion gate

Production may start only after all of the following have authenticated
positive terminals at one exact commit:

1. task175 receipt status `READY`, checker agreement, complete 6,441 roster,
   actual Fox/presentation canaries, and its source/checker hashes;
2. task176 receipt status `COMPLETE`, checker PASS, exact ALL/singleton
   extension census, and its source/checker hashes;
3. v108 PB4 and v121 PB3 exact presentation boundaries; and
4. v122/v125 typed ten-coordinate map.

The large task176 JSON need not be committed or loaded as Python object data.
The task177 reply must pin the prerequisite run ids, head SHAs, receipt SHA-256
values, and checker verdict hashes before PRODUCTION.  Until those values are
known, production must terminate `UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED`.

Past SELFTEST logs and checked-in UNKNOWN fixtures are not positive inputs.

## 3. Correct target and typed ambient module

The task175 field `stacked_target` is a canary correction-change row.  It is
not the v110 target.  Reconstruct the target independently from task175
`raw_base_targets.H1/H2/P`, negate it over \(\mathbf F_3\), append the two
zero exponent coordinates, and retain the three block tags.  Cross-block
cancellation is forbidden.

The sparse ambient is

\[
 M_{H1}\oplus M_{H2}\oplus M_P\oplus\mathbf F_3^2.
\]

PB3 rows may enter only H1 or H2 with their correct translate/prefix type.
PB4 rows may enter only P.  A raw list of two or eleven base relators is not
the complete translated boundary family.

## 4. Full weighted occurrence formula

For every one of the 6,441 signed normal-generator words, reconstruct every
literal occurrence from the raw H1/H2/five-coface Fox formula.  Merge equal
`(coordinate,target)` constraints over \(\mathbf F_3\), add coefficients,
and delete exact zero cancellations.  Store

\[
 K_r,\qquad T_i(r),\qquad c_{r,i}:T_i(r)\to\mathbf F_3
\]

as in v132 (1.5).  Do not trust producer-supplied target sets or ACTIVE bits.
The checker must rebuild them from the roster, literal words, prefixes,
signs, and marked group operations.

The 110-row task175 transcript is a canary, not the full weighted table.

## 5. Lazy multi-coordinate oracle

For every ordered coordinate subset \(S\) requested by a dual, compute and
cache only:

- \(A_S=\Phi_S(\Gamma)\);
- \(L_S\), \(|D_S|\), and \(|\ker\pi_S|\);
- literal tuple membership in \(D_S\);
- a witnessing Q0 section and Gamma adjustment when membership is positive;
- the exact \(N(a)\) values used by v132 inclusion-exclusion.

The one 1,469,664-state Q0 scan must be shared inside an iteration.  Never
enumerate or deduplicate all of \(\Delta_{\rm all}\).

Memory rule: do not inflate the roughly 1.4 GiB fixed-width ten-coordinate
table into nested Python objects.  Use a temporary fixed-width binary file
outside the repository plus streaming or `mmap`; keep the 243 Gamma table,
Q0 parent/letter data, membership bitsets, hashes, and requested query cache
in bounded structures.  The production receipt stores digests and the
queries actually used, not an unbounded duplicate of the raw table.

If a requested subset, membership query, or exact kernel order does not
finish under its registered cap, return `UNKNOWN_RESOURCE`; it is not zero.

## 6. Boolean cells and word-bearing extraction

For every dual/row correlation, use v132 (2.7) with exact integer counts.
A field value and a cell count are different types.  Inclusion-exclusion
must include the all-star complement and every cancellation-relevant cell.

For a positive ACTIVE cell, recover one source word by the concrete v132
fallback:

1. scan Q0 in the frozen section order;
2. impose the equality coordinates through the cached \(A_S\) lookup;
3. scan only the matching Gamma coset, at most 243 states; and
4. test every star inequality before emitting
   \(u_\delta=u_\gamma u_{s(q)}\).

The emitted correction column is the direct replay of
\(u_\delta r u_\delta^{-1}\).  A context tuple without its source word is not
a positive certificate.

## 7. Column-generation loop

Use deterministic sparse Gaussian elimination over \(\mathbf F_3\).

1. Start from authenticated, block-typed PB3/PB4 boundary columns and a
   deterministic small set of word-bearing correction columns.
2. Reduce the correct target from Section 3.
3. If nonzero, construct a dual and correlate it with every full translated
   boundary family and all 6,441 correction families.
4. Add only the canonical first rank-increasing ACTIVE column, retaining its
   source word, and repeat.
5. On membership, print coefficients and multiply the associated words in
   the same order to obtain one common correction.
6. On apparent separation, require every lazy query and every family to be
   complete before printing the dual.

Register caps for iterations, sparse nonzeros, distinct subset queries,
cell terms, Q0 scans, source-pair tests, disk bytes, wall time, and RSS.
Every cap has a typed `UNKNOWN_RESOURCE:<phase>` terminal.

## 8. Final positive replay

The producer and checker must independently verify:

1. the correction word lies in the registered joint kernel;
2. its two exponent sums are zero modulo three;
3. H1 and H2 vanish modulo their exact PB3 boundary images;
4. the five A.18 coface values occur in the frozen order and their
   noncommutative pentagon product vanishes modulo exact PB4 boundaries;
5. the sparse column sum equals the target with block tags intact;
6. every emitted context section and conjugate word replays literally; and
7. the corrected word is `reduce(g760 + correction)` in the registered right
   convention.

Do not promote a module equality without this direct word replay.

## 9. Independent checker and mutations

The checker must not import the producer or share its weighted-formula,
projection, cell-count, Gaussian, or word-replay helpers.  It may load only
the frozen third-party arithmetic primitives already permitted by tasks175
and 176.

SELFTEST uses a small nonabelian extension and must reject, through the real
validator path, at least these resealed semantic changes:

1. merged same-target coefficient cancellation;
2. one multi-coordinate target;
3. one inclusion-exclusion sign;
4. one kernel order;
5. the complement/all-star cell;
6. one Q0 section or Gamma adjustment;
7. one source-word transversal/conjugator;
8. one PB3/PB4 block tag;
9. one target base-defect coordinate;
10. one exponent coordinate;
11. one final correction coefficient; and
12. one pentagon factor order/sign.

Whole-dictionary equality is not a semantic mutation oracle.  Every mutation
must enter the same validator used for production receipts.

## 10. Files and execution discipline

Luna may create only the following new files plus its versioned fixture:

- `search/d972_r07_weighted_cell_colgen_v1.py`
- `crosscheck/check_d972_r07_weighted_cell_colgen_v1.py`
- `search/d972_r07_weighted_cell_colgen_gha_driver_v1.g`
- `search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json`
- `sol/luna_reply_177_r07_weighted_cell_colgen_v1.md`

Do not edit workflows.  Do not run Python/Node/GAP locally.  Parent alone
commits, pushes, and dispatches GHA.  SELFTEST must finish before PRODUCTION.

The GHA driver must be ASCII-only, serial inside one job, pin every input,
reject log continuation/backslash-newline, and emit exactly one unwrapped
terminal line.  A normal GitHub-hosted job has a six-hour outer ceiling;
register a production soft cap below that ceiling and return a receipt before
the workflow hard timeout.

## 11. Allowed conclusions

Positive terminal:

```text
R07_WEIGHTED_CELL_COLGEN_COMMON_WORD
```

Exact negative terminal, only after complete correlation:

```text
R07_WEIGHTED_CELL_COLGEN_SEPARATOR
```

Otherwise use typed UNKNOWN.  Neither positive terminal is by itself a
cofinal lift, fake, or Ihara witness.
