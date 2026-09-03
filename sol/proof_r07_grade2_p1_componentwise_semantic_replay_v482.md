# R07: componentwise semantic replay for the lazy P1 presentation (v482)

Author: Sol / 2026-09-03

This note factors the mandatory `44+4*8059` global precision-one equalities
into the exact prepare/block equalities already carried by the five Task554
artifacts.  It is a paper theorem and an implementation interface.  It does
not promote the current structural candidate, perform the actual replay, or
assert A0, COMMON, a compatible cofinal lift, fake or Ihara.  `verified=false`.

## 1. Split notation

Work over `k=F3`, with the four characters and four source actors in their
registered orders.  Put

```text
L = (direct sum_chi V0[chi]) + Aux,       dim L = 24192+8,
G = direct sum_lambda V1[lambda],         dim G = 4*18144,
P1src = L + G,                            dim P1src = 96776.
```

Let `r_chi=(505,503,503,503)`, so `R=sum r_chi=2014`, and let
`n_lambda=(1509,1512,1512,1512)`, so `N=sum n_lambda=6045`.  In the v451/v480
global order an old row and a new row have the forms

```text
b[chi,i] = (ell[chi,i], (g[chi,i,lambda])_lambda),
h[lambda,j] = (0, iota_lambda h0[lambda,j]).             (1.1)
```

Here `ell[chi,i]` is supported in `V0[chi]+Aux`; its grade companion may have
all four lambda components.  This distinction is essential.

For every old source defect origin `o=(chi,u)`, let `q[o,i]` be its stored
old reduction.  The 8,232 origins are exactly

```text
4*44 old projected seeds + 4*R old actor defects
  = 176 + 8056 = 8232.                                (1.2)
```

Write `d[o,lambda]` for the authenticated lambda packet obtained from the
degree-one part of the direct defect after subtracting its old reduction.
The lambda block stores coefficients `R[lambda,o,j]` reducing that packet to
the `h[lambda,j]`.  It also stores `p[lambda,j,t,k]` for each new-row actor
transition.

## 2. The local replay table

The following four families are sufficient.

| family | number | exact equality |
|---|---:|---|
| old seed/lower | `4*44=176` | projected seed lower part `= sum_i q[o,i] ell[chi,i]` |
| old actor/lower | `4*R=8056` | acted old lower row `= sum_i q[o,i] ell[chi,i]` |
| packet/block | `4*8232=32928` | direct grade defect component `= d[o,lambda] = sum_j R[lambda,o,j] h0[lambda,j]` |
| new-row actor | `4*N=24180` | `A_t h0[lambda,j] = sum_k p[lambda,j,t,k] h0[lambda,k]` |

Thus there are 65,340 narrow equalities.  This is not a claim that fewer
logical conditions are checked: the factorization deliberately replaces a
global 96,776-coordinate comparison by independently attributable local
comparisons.  Every packet/block check has both halves shown in the table:
the direct defect must reproduce the authenticated packet bytes, and the
stored block expression must reproduce the same packet from the block basis.

The 2,014 old and 6,045 new DAG-node identities are separate prerequisites.
They reconstruct the rows in increasing pivot order, including scale,
reductions and literal origin.  Lead distinctness alone does not establish
any equality in the table.

## 3. Sufficiency theorem

### Theorem 3.1

Assume:

1. the five state bodies, their complete typed expressions and all referenced
   row/packet blobs are authenticated;
2. all 8,059 DAG identities reconstruct the rows in (1.1);
3. every equality in the local replay table holds; and
4. the exact filtered-word resolution `sum_chi P_chi=1` of v451 (1.3) is
   replayed for the 44 seeds.

Then all 44 seed relations and all `4*8059` actor relations in the global lazy
presentation hold coordinatewise in `P1src`.

### Proof

Fix an old origin `o=(chi,u)`.  Its direct precision-one defect splits
uniquely as a lower part in `L` and four grade components in the direct sum
`G`.  The appropriate first or second row of the table identifies the lower
part with the old reduction.  After subtracting the lifted old rows, the
remaining lambda component is, by definition and direct byte replay, the
packet `d[o,lambda]`.  The third row identifies it with

```text
sum_j R[lambda,o,j] h0[lambda,j].                      (3.1)
```

Because the four `V1[lambda]` are a direct sum, adjoining (3.1) for every
lambda gives the full old-origin identity in `L+G`.  This is exactly v451
(2.4) for a projected seed origin and v451 (2.5) for an old-row actor origin;
the plus sign is forced because the subtraction of the old reduction already
occurred when the packet was formed.

For a fixed seed label, sum the four projected-seed identities over `chi`.
The direct sides sum to the unprojected seed by `sum_chi P_chi=1`; equal
coefficient keys on the right combine modulo three.  Hence the corresponding
global seed relation holds.  No idempotence of the filtered `P_chi` is used.

For a new row, both the row and its acted value lie in its single lambda
summand.  The fourth row of the table is therefore already the global actor
identity v451 (2.6).  These cases exhaust the 44 seeds and the actor images of
all `R+N=8059` rows.  Equality on the direct summands is coordinatewise
equality in `P1src`.  QED.

## 4. Streaming implementation consequence

The theorem removes the need to materialize either the dense
`8059 x 96776` basis or the nested global output of `assemble_b1_relations`.
An actual producer/checker may instead perform the following authenticated
passes.

1. Reconstruct each old DAG row and compare its 6,056-trit lower slice and
   72,576-trit grade companion with the two pinned blobs.
2. Replay the 176+8,056 old lower identities.  For the same origin, compute
   the exact grade defect once, split it into four 18,144-trit components and
   compare each component with the corresponding packet row.
3. For one lambda block at a time, reconstruct its DAG rows, replay all 8,232
   packet reductions and its `4*n_lambda` actor transitions, and then release
   that parsed block.  Expressions may be compiled to flat CSR arrays; their
   original complete key/value streams and digests remain authenticated.
4. Accumulate deterministic counters and hashes for every family and compare
   producer/checker receipts.  A shared digest is not a substitute for either
   side reopening the five raw artifacts and replaying the equations.

The arithmetic widths in these passes are 6,056, 72,576 and 18,144, never a
zero-filled family-wide matrix.  The immutable packed row backing remains the
67,011,332 bytes of v480.  This theorem makes no unmeasured peak-RSS or runtime
claim; in particular, nested JSON coefficient forests should not all be kept
resident.

## 5. Boundary toward grade two

After the actual componentwise replay and an independent checker agree, the
lazy rows and their relations supply the complete P1 input required by v474.
The next consumer must still reconstruct every degree-two lift, compare its
precision-one truncation, replay the 44+32,236 degree-two defects, process the
8,059 lower-first connection offers, and decide the fresh rho2.  None of
those obligations is discharged here.

```text
COMPONENTWISE => GLOBAL P1 SEMANTICS: PAPER-CLOSED
ACTUAL FIVE-ARTIFACT SEMANTIC REPLAY: PENDING
INDEPENDENT CHECKER:                  PENDING
GRADE-TWO MEMBER/NONMEMBER:           PENDING
A0 / COMMON / COFINAL / FAKE:         NOT DECLARED
IHARA:                                NOT DECLARED
verified:                             false
```

`R07_GRADE2_P1_COMPONENTWISE_SEMANTIC_REPLAY_V482_CANDIDATE`
