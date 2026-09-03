# R07: disjoint-lead completion of the grade-one presentation (v481)

Author: Sol / 2026-09-03

Status: exact paper reduction plus actual old-row census.  The old-row census
was independently reproduced in Task693, but the Task692 production scan has
two finite binding/fixture defects and is therefore not promoted by this note.
The four new block blobs still require the prescribed exact ingest and
independent replay.  `verified=false`.

## 1. Coordinate intervals

Use the v480 source precision-one order

```text
D0(a,q) = 6048*a+q,                    0 <= q < 6048,
D1(a,q) = 24192+18144*a+q,             0 <= q < 18144,
AUX(r)  = 96768+r,                     0 <= r < 8.
```

Put

```text
I0   = [0,24192),
I1,a = [24192+18144*a,24192+18144*(a+1)),
IAux = [96768,96776).
```

These six intervals are pairwise disjoint and exhaust the 96,776 source
coordinates.

## 2. Exact old-row fact

The independent Task693 scan of the canonical prepare body and its eight old
row blobs reproduced Task692 coordinate for coordinate:

```text
old rows                         2014
degree-zero global leads         2012
degree-one global leads             0
auxiliary global leads              2
distinct, coefficient-one leads 2014
```

The two auxiliary rows are character-zero pivots 0 and 1 with local leads
6,054 and 6,055, hence global leads 96,774 and 96,775.  Thus every old global
lead lies in `I0 union IAux`, and no old global lead lies in any `I1,a`.

The canonical lead/coefficient digest is

```text
1be9a7a806fbb70f5d9825d865004b049d8c0d092a840a0c31ce951b4d5976ee.
```

This paragraph is an actual-data fact, not yet an accepted producer terminal:
Task693 correctly requires the reopened scan bytes to be receipt-bound and its
edge fixture to use the production summarizer.  Task696 is the exact repair.

## 3. New-block local-to-global lemma

For character `a`, let a stored block basis row have local first nonzero
coordinate `q` and coefficient one.  Its v480 lazy row has structural zero in
all degree-zero coordinates, in the other three degree-one blocks, and in all
auxiliaries.  Therefore its actual global lead is exactly

```text
24192+18144*a+q in I1,a.                         (3.1)
```

Consequently:

1. distinct local leads inside block `a` give distinct global leads;
2. rows in two different character blocks cannot have the same global lead;
3. by Section 2, no new-row global lead can equal an old-row global lead; and
4. normalization at the local lead is normalization at the global lead.

No 96,776-trit assembled row and no reduction of a new row against the old
family is required to establish these statements.  It suffices to authenticate
each 4,536-byte packed block row once, reject bytes above 80, recompute its
local first nonzero trit, and compare it with the body's declared lead and
coefficient one.

## 4. Presentation completion theorem

Assume the exact four Task554 block ingests establish normalized, pairwise
distinct actual local leads for their ranks

```text
(1509,1512,1512,1512).
```

Then the v480 ordered family of 2,014 old plus 6,045 new rows has 8,059
pairwise distinct normalized global leads.  In particular it is linearly
independent in `F3^96776`, so its rank is 8,059.

Proof.  Distinctness and normalization within the old family are Section 2.
For each new family they follow from (3.1) and the local hypotheses.  All
cross-family collisions are excluded by the pairwise-disjoint intervals in
Section 1.  In a nontrivial linear combination, choose the least leading
coordinate among rows with nonzero coefficient.  Exactly one row contributes
there, contradiction.  Hence the family is independent.  QED.

This theorem turns the remaining structural basis check into four serial
6,045-row local scans.  The large block JSON bodies are still needed for exact
origin, DAG, seed/actor-transition and parent replay; the theorem removes only
global zero-fill and cross-reduction work.

## 5. Claim boundary and v220 map

```text
P1 global-rank theorem:       PAPER-CLOSED CONDITIONAL ON FOUR LOCAL SCANS
old actual lead census:       INDEPENDENTLY MATCHED; producer repair pending
four block ingests/scans:     PENDING
44 + 4*8059 semantic replay: PENDING
fresh rho2:                   GHA v8 running separately
grade-two MEMBER/NONMEMBER:   NOT RUN
A0 actual / first rung:       0/1 and 1/6 cross-checked
COMMON / COFINAL / FAKE:      NOT DECLARED
IHARA:                        NOT DECLARED
verified:                     false
```

`R07_GRADE2_P1_DISJOINT_LEAD_COMPLETION_V481_CANDIDATE`
