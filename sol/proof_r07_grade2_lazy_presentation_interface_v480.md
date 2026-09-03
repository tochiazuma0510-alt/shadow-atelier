# R07: lossless lazy grade-one presentation for the targeted grade-two owner (v480)

Author: Sol / 2026-09-03

Status: paper theorem and corrected implementation interface, independently
audited by Sol(max) Task667 with verdict
`PASS_LAZY_P1 / SAFE_TO_IMPLEMENT=yes`.  This note removes an unnecessary
dense presentation store.  It does not authenticate the five actual artifacts,
run the grade-two decision, or prove a lift/fake/Ihara terminal.
`verified=false`.

## 1. Typed precision-one source row

Work over `k=F3` in character order

```text
A=((0,0),(0,1),(1,0),(1,1)).
```

For each `a` put `V0[a]=k^6048`, `V1[a]=k^18144`, and put
`Aux=k^8`.  The logical precision-one source space is

```text
P1src = (direct sum_a V0[a]) + (direct sum_a V1[a]) + Aux
      = k^(24192+72576+8) = k^96776.                    (1.1)
```

Its flat order is all four degree-zero blocks, then all four degree-one
blocks, then the eight auxiliaries:

```text
D0(a,q)=6048*a+q,
D1(a,q)=24192+18144*a+q,
AUX(r)=96768+r.                                        (1.2)
```

This `96776` is a source precision-one width.  It is not a physical pair.
The later connection map produces the distinct rows

```text
ell_i in F3^32260,       g_i in F3^48384.              (1.3)
```

## 2. Canonical lazy descriptors

Let the cumulative row offsets be

```text
O=(0,505,1008,1511),
H=(2014,3523,5035,6547),
end=8059.                                               (2.1)
```

### 2.1 Old rows

For character `a` and local pivot `p`, the prepare artifact supplies two
authenticated packed slices:

```text
lower[a,p] : 6056 trits = (l[a,p] in V0[a], alpha[a,p] in Aux),
grade[a,p] : 72576 trits = G[a,p] in direct sum_c V1[c].
```

The row with global ID `i=O[a]+p` is defined lazily by

```text
b_i=(iota0_a(l[a,p]), G[a,p], alpha[a,p]).              (2.2)
```

The degree-one companion is the complete four-character row; it is not
character-local.  The auxiliary coordinates belong at the end of (1.2), not
immediately after the owning 6,048 coordinates.

The packed byte offsets are exactly

```text
lower slice:  [1514*p, 1514*(p+1)),
grade slice:  [18144*p,18144*(p+1)).                    (2.3)
```

### 2.2 New character-block rows

For character `a` and local pivot `p`, the block artifact supplies

```text
h[a,p] in V1[a], packed at [4536*p,4536*(p+1)).
```

For `i=H[a]+p`, define

```text
b_i=(0, iota1_a(h[a,p]), 0).                            (2.4)
```

Thus all degree-zero coordinates, the other three degree-one blocks, and all
auxiliaries are structural zeroes.  The ranks are

```text
old: (505,503,503,503),
new: (1509,1512,1512,1512),                             (2.5)
```

which proves (2.1) and the total `8059`.

Every descriptor also retains the authenticated state/body/blob identity,
local row number, semantic kind, DAG origin, reductions and scale.  A digest-
only descriptor is not covered by this construction.

## 3. Coordinatewise assembly theorem

Let `E(i,x)` be the value obtained from (2.2) or (2.4) without constructing a
family-wide matrix.  Let `D_i` be the dense row produced by the old v451/
Task565 `assemble_precision1_basis` routine.

### Theorem 3.1

For every `0<=i<8059` and `0<=x<96776`, one has

```text
E(i,x)=D_i[x].                                          (3.1)
```

Proof.  For an old row the old routine initializes four zero degree-zero
blocks, inserts `l[a,p]` in block `a`, reshapes the stored complete companion
into all four degree-one blocks, and appends `alpha[a,p]`.  These are exactly
the five exhaustive coordinate cases in (1.2), so its output equals (2.2).

For a new row it initializes degree zero and auxiliaries to zero and inserts
the single stored `h[a,p]` in degree-one block `a`.  This is exactly (2.4).

All widths are divisible by four, canonical packed bytes lie in `0..80`, and
the least-significant-trit-first base-three representation is unique.  The
stored matrices are row-major.  Hence the byte intervals (2.3) and their new-
row analogues unpack to precisely the rows used by the old routine.  This
proves (3.1).  QED.

### Lead warning

The old `6056`-coordinate lower lead is not automatically the global lead of
`b_i`: the last eight local positions map to `96768..96775`, and a nonzero
degree-one companion can precede them in the global order.  The implementation
must recompute the actual first nonzero coordinate of the logical row.  For a
new row, the local lead maps to `24192+18144*a+q`.  Every global row must be
nonzero, normalized at its actual global lead, and have a distinct lead in the
ordered presentation.

## 4. Sufficiency for the v474 targeted decision

The lazy presentation supplies every input used by v474 without a resident
`8059 x 96776` matrix.

1. `lift2(i)` reconstructs row `i` in increasing DAG order and stores only its
   degree-two continuation.  Its precision-one truncation is compared with
   the lazy evaluator of Theorem 3.1.
2. Applying the exact occurrence and physical maps to one lift gives the
   pair `(ell_i,g_i)` in (1.3).  The lower-first connection recursion consumes
   this ordered stream one offer at a time.
3. Each of the 44 seed defects and `4*8059=32236` actor defects subtracts the
   canonical global coefficient stream from its direct value.  All `96776`
   precision-one coordinates must vanish before a `36288`-coordinate
   character degree-two slice is returned.
4. Static literal ancestry is retained in the row/DAG descriptors.  Dynamic
   connection, orbit and physical-echelon ancestry remains a separate
   result-dependent obligation.
5. The independent checker reopens the five raw Task554 artifacts and builds
   its own descriptors.  It cannot accept a producer descriptor hash as the
   coordinatewise replay.

The global coefficient streams are not character-local shortcuts.  Seed
relations combine the four offset old expressions and the corresponding
origin reductions in all four new blocks; old actor relations do the same for
their actor-origin, while a new-row actor relation uses its own new block with
the appropriate global offset.  Exact-key coefficients are combined modulo
three and zero sums deleted.

Therefore the lazy representation changes storage and avoids zero-fill work;
it does not reduce the mandatory 32,280 semantic equations, 8,059 lift-DAG
replays, connection offers, separator tests, or terminal ancestry.

## 5. Exact storage gain

The immutable row backing used by (2.2)--(2.4) is

```text
four old lower blobs          3,049,196 bytes
four old degree-one blobs    36,542,016 bytes
four new block basis blobs   27,420,120 bytes
total                        67,011,332 bytes.          (5.1)
```

A duplicate assembled packed family would occupy
`8059*24194=194,979,446` bytes; a dense uint8 family would occupy
`779,917,784` bytes.  Thus (5.1) avoids respectively 127,968,114 and
712,906,452 duplicate bytes.  It does not make mapped pages, the five large
JSON bodies, interpreter objects, metadata, the degree-two lift store, or
dynamic ancestry free.  Bodies and coefficient forests must be streamed into
flat typed records rather than retained as nested Python objects.

## 6. Correction to Task647 and claim boundary

Task647 section 3.4's phrase

```text
all 96,776 source lower/auxiliary coordinates
```

is corrected to

```text
all 96,776 source precision-one coordinates
(24,192 degree-zero + 72,576 degree-one + 8 auxiliary). (6.1)
```

The number was correct; the type label was not.  There is no 96,776-wide
paired physical object.

```text
LAZY/DENSE P1 COORDINATE EQUALITY:  PAPER-CLOSED; ACTUAL REPLAY REQUIRED
RESIDENT 8059 x 96776 FAMILY:       NOT REQUIRED
FIVE TASK554 ARTIFACT INGEST:       IN PROGRESS
ACTUAL FRESH RHO2:                  NOT YET ACCEPTED
GRADE-TWO MEMBER/NONMEMBER:         NOT RUN
A0 / COMMON / COFINAL / FAKE:       NOT DECLARED
IHARA:                              NOT DECLARED
verified:                           false
```

`R07_GRADE2_LAZY_PRESENTATION_INTERFACE_V480_CANDIDATE`
