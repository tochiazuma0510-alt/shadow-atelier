# R07 A0: decision-first factorization of the first grade-one terminal (v463)

## 0. Scope and status

This note factors the running Task554 grade-one merge into an exact finite
membership decision followed by result-dependent certificate construction.
It changes neither the registered 8,059-row logical roster nor the physical
map.  It is a restart/runtime theorem, not a MEMBER/NONMEMBER result.

The evidence fixed here is the failed production run
`33677346616` at head
`22c6dddb43d107c05e65f53ad898823ae8ebe276`.  Its four sealed character
blocks and prepare state completed.  The merge log artifact
`9875030711` records

```text
attempts=7168  rank=5044  elapsed=269.09 s
attempts=7424  rank=5044  elapsed=294.17 s
attempts=7680  rank=5044  elapsed=319.43 s
attempts=7936  rank=5044  elapsed=344.60 s
```

and then the outer 335-minute bound returned exit 124.  Since progress is
printed only at multiples of 256, this log proves neither that the last 123
logical rows completed nor which post-row operation was entered.  In
particular it does **not** establish that the separating-dual routine was the
stall.

## 1. The finite predicate precedes every expensive terminal object

Let the deterministic lower-first routing of the 2,014 old rows and the 6,045
block rows produce the physical grade echelon

\[
 E=(e_0,\ldots,e_{r-1})\subseteq\mathbf F_3^{24192}
\]

and let \(\rho\) be the already sealed grade-one residual.  The actual first
grade decision is exactly

\[
 \operatorname{MEMBER}_1\quad\Longleftrightarrow\quad
 \operatorname{rem}_{E}(\rho)=0.                 \tag{1.1}
\]

The v3/v4 control flow computes this remainder before all of the following:

1. construction and full-basis validation of a separating dual;
2. serialization of `physical_roster`, the lower/grade ancestry DAGs and the
   transition presentation;
3. expansion of selected ancestry into literal words;
4. lower, precision-one and degree-two literal replays.

Consequently none of those four operations is logically needed to decide
(1.1).  Stopping immediately after the remainder cannot change the predicate.

## 2. A compact exact decision checkpoint

After all 8,059 logical roster positions have been routed, a decision-first
producer may atomically seal the tuple

\[
 \mathcal D=(H_P,H_{B_0},\ldots,H_{B_3},8059,r,
 H_E,L_E,H_\rho,H_{\rm rem},C).                  \tag{2.1}
\]

Here the first five hashes bind the sealed prepare/four-block chain; \(H_E\)
binds the packed normalized physical-grade basis, \(L_E\) is its ordered
pivot-lead list, and \(C\) is the ordered reduction coefficient list when
the remainder is zero.  For a nonzero remainder the checkpoint stores its
packed value (or a hash plus authenticated blob).  At the last logged prefix
the basis has rank 5,044.  Since the remaining 123 logical positions can each
add at most one pivot, the final basis costs at most

\[
 (5,044+123)\cdot(24,192/4)
 =31,250,016\ {\rm bytes}.                          \tag{2.2}
\]

The remaining fields are small.  No ancestry list or transition presentation
belongs in this checkpoint.

An independent replay regenerating the same 8,059 logical inputs, checking
the lower-first routing and reproducing (2.1) establishes the decision.  If
the result is NONMEMBER, a separating dual can then be constructed and
checked against the sealed basis in a separate bounded phase.  If it is
MEMBER, \(C\) selects the exact ancestry roots for a separate literal
expansion.  Thus decision-first factorization loses no information required
by either branch.

## 3. Why the current v4 run is not the recovery contract

V4 replaces v3's vectorized next-nonzero packed-byte search by a Python loop
which advances one packed byte at a time.  A physical-grade row has 6,048
packed bytes, so the grade-owner roster scans admit the conservative ceiling

\[
 8,059\cdot6,048=48,740,832                     \tag{3.1}
\]

of 48,740,832 Python-level cursor iterations, apart from pivot eliminations.
The lower-owner scans and one target reduction are additional bounded work;
(3.1) is not a whole-run operation count.  Therefore the live v4 step need
not have reached the post-row terminal at all.  The v3 log is the measured
fast row path and must be retained for the decision probe; v4's scan is not a
justified speedup merely because it removes a NumPy allocation.

The next producer must emit flushed markers immediately before and after:

```text
LAST_LOGICAL_ROW
TARGET_REDUCTION
DECISION_SEAL
```

and terminate after `DECISION_SEAL`.  A failure before a marker is then
localized without inference, and the sealed decision can be resumed by the
appropriate result-dependent branch without rerunning source blocks.

## 4. Claim boundary

```text
REGISTERED LOGICAL ROSTER:       UNCHANGED, EXACTLY 8,059
V3 MEASURED PREFIX:              7,936 / 8,059, RANK 5,044
V3 POST-ROW SUBPHASE:            NOT IDENTIFIED BY ITS LOG
V4 BYTE-SCAN SPEEDUP CLAIM:      REJECTED WITHOUT MEASUREMENT
DECISION-FIRST FACTORIZATION:    EXACT
GRADE-ONE MEMBER/NONMEMBER:      NOT DECIDED HERE
A0 / COMMON / COFINAL / IHARA:  NOT DECLARED
```
