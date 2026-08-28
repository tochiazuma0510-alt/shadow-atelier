# R07 tagged boundary seed-count erratum v270

Author: Sol / 2026-08-29

Status: paper/type erratum to v269 and its task332 implementation addendum.
The invariant-closure theorem itself is correct, but the initial seed roster
was counted in the wrong module.  A4's ten independently tagged successor
coordinates require 65 seed rows, not 13.  The older H1/H2/P occurrence
module of v163 requires 15 seed rows, not 13.  No actual boundary rank, A4
kernel, anchor, lift, fake, or Ihara witness is declared.  `verified=false`.

## 1. The two boundary modules must not be identified

V231 defines the first-successor ambient kernel as

\[
 V=\prod_{i=0}^{9}\ker(E_{i,1}\to E_{i,0}),
 \tag{1.1}
\]

with five PB3-type coordinates and five PB4-type coordinates.  Task232 then
requires each coordinate's affine/Fox chain to be quotiented by its complete
translated presentation-boundary image and says explicitly that all ten
copies are tagged before taking their direct sum.

Let \(M_i\) be the affine/Fox row module for coordinate \(i\).  Put

\[
 M=\bigoplus_{i=0}^{9}M_i,
 \qquad
 D_i=\operatorname{span}_{\mathbf F_3}
       \{q\,d_{i,j}:q\in Q_i\},
 \qquad
 D=\bigoplus_{i=0}^{9}D_i.
 \tag{1.2}
\]

Here PB3 has two base presentation rows and PB4 has eleven.  If
\(\iota_i:M_i\to M\) denotes the tagged summand injection, the correct A4
seed roster is

\[
 \mathcal B_{A4}=
 \{\iota_i(d_{i,j}):0\le i<5,\ 1\le j\le2\}
 \cup
 \{\iota_i(d_{i,j}):5\le i<10,\ 1\le j\le11\}.
 \tag{1.3}
\]

Consequently

\[
 \boxed{|\mathcal B_{A4}|=5\cdot2+5\cdot11=65.}
 \tag{1.4}
\]

Equal group-element bytes, equal context IDs, or isomorphic quotient factors
do not identify two rows in (1.3), because the coordinate tag is part of the
row key.  In particular E3-C21 and E4-C21 remain distinct, and two different
E3 coordinates also remain different direct-summand coordinates.

V163 uses a different occurrence-lifted module with three independently
tagged blocks \(H1,H2,P\).  There are two PB3 relations in each of H1 and H2
and eleven PB4 relations in P.  Its correct seed count is therefore

\[
 \boxed{|\mathcal B_{H1,H2,P}|=2+2+11=15.}
 \tag{1.5}
\]

Neither (1.4) nor (1.5) equals 13.  V269 conflated the untagged list of two
PB3 relation *forms* plus eleven PB4 relation forms with their required
tagged instances.

## 2. Correct invariant-closure theorem for A4

Insert the 65 rows (1.3) into one coefficient-bearing echelon.  Enqueue each
rank raise.  For every dequeued row apply the common source actions
\(x,x^{-1},y,y^{-1}\), insert the resulting row with its immutable
seed/parent/action coefficient ancestry, and stop only when the queue is
empty.  Call the resulting space \(D_q\).

### Theorem 2.1 (SIXTY-FIVE-SEED A4 BOUNDARY CLOSURE)

\[
 \boxed{D_q=D.}
 \tag{2.1}
\]

If the terminal rank is \(b\), the computation has exactly \(b\)
rank-raising rows, at most \(4b\) post-seed action candidates, and at most
\(65+4b\) insertion attempts.

#### Proof

Every seed belongs to its corresponding \(D_i\), and every source action
preserves each tagged summand and its translated-boundary space.  Hence
\(D_q\subseteq D\).

Conversely fix \(i\), a base row \(d_{i,j}\), and \(q\in Q_i\).  The two
marked context images of \(x,y\) generate \(Q_i\), so there is a source word
\(w\in F(x,y)\) whose image in coordinate \(i\) is \(q\).  Queue exhaustion
makes \(D_q\) invariant under both marked generators and their inverses.
Therefore

\[
 w\cdot\iota_i(d_{i,j})=\iota_i(qd_{i,j})\in D_q.
 \tag{2.2}
\]

Although the source action is componentwise on all ten coordinates, the seed
in (2.2) is zero outside coordinate \(i\); actions in the other coordinates
therefore introduce no diagonal restriction.  Thus every generator of every
\(D_i\) belongs to \(D_q\), proving \(D\subseteq D_q\).  Each accepted row
strictly raises finite-dimensional rank, giving termination and the count.
\(\square\)

## 3. Correct independent support-inversion checker

For a dual \(\lambda\) on the ten-tagged module, the checker must process
every tuple

\[
 (i,j,c,h,\alpha),
 \quad 0\le i<10,
 \tag{3.1}
\]

from the 65 tagged base rows and every matching support value
\(g\in\operatorname{supp}(\lambda_{i,c})\).  It reconstructs

\[
 t=gh^{-1},\qquad th=g,
 \tag{3.2}
\]

and accumulates under the full key \((i,j,t)\).  The coordinate \(i\) may
not be dropped from that key.  The v163 proof then applies verbatim in each
summand: a nonzero accumulator gives a strict rank-raising translated column,
while a complete zero accumulator proves annihilation of all of (1.2).

For the H1/H2/P occurrence module the same statement uses the three block
tags and its 15 seeds.  A checker that processes only one PB3 relation-form
copy cannot certify either module.

## 4. Executable source audit

This correction agrees with the older actual boundary-oracle architecture:

- `search/d972_r07_word_independent_successor_kernel_v1.py` projects a dual
  separately for every coordinate `0..9`, calls the PB3/PB4 boundary oracle
  in that coordinate, and reinserts the coordinate tag;
- `search/d972_r07_positive_common_word_colgen_v1.py` keeps H1, H2, and P as
  blocks `1,2,3`, and its base loop uses counts `2,2,11`; and
- `search/d972_r07_second_frattini_affine_prefix_compiler_v1.py` reconstructs
  the two PB3 and eleven PB4 relation *forms* only because that compiler uses
  one PB3 block and one PB4 block, not A4's ten-coordinate direct sum.

Thus task193's 13-row reconstruction is a valid local two-block interface but
cannot be copied as A4's total boundary seed roster.

## 5. Supersession and fixed frontier

V269 Theorem 2.1 is retained only after replacing its A4 seed roster and all
counts by Theorem 2.1 above.  V269 Sections 1 and 4 and task332 are superseded
wherever they say 13 seeds.  Any task328/v3 implementation hard-coding 13 is
not authorized for SELFTEST or production and must be independently rejected
or repaired to the 65-tagged construction.

```text
A4 TAGGED BASE BOUNDARY SEEDS:                 65
H1/H2/P OCCURRENCE-MODULE BASE SEEDS:          15
UNTAGGED PB3/PB4 RELATION FORMS:               13
65-SEED INVARIANT CLOSURE = COMPLETE A4 D:     PAPER PROOF
POST-SEED ACTION CANDIDATES:                   <= 4b
ACTUAL A4 BOUNDARY RANK / K / ANCHOR:          NOT COMPUTED
LIFT / FAKE / IHARA:                           NONE
```

`R07_TAGGED_BOUNDARY_SEED_COUNT_ERRATUM_V270_PAPER_GRADE`
