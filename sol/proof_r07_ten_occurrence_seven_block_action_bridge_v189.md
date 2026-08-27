# R07 ten-occurrence / seven-block action bridge v189

Author: Sol / 2026-08-28

Status: paper theorem and exact frozen R07 specialization.  This note fixes
the ambiguity in v173 Section 1: there are seven **relation blocks**, but ten
distinct typed evaluation coordinates.  The resulting marked common-source
groups are canonically isomorphic.  No quotient is taken and no
357,128,352-state roster is required.  This closes only the roof type bridge;
it does not construct the first successor multiplier, a compatible cofinal
lift, a fake certificate, or an Ihara witness.

## 1. Eleven literal occurrences and ten typed coordinates

At one matched finite roof, let (F=F(x,y)).  Write the five source-E3
evaluation maps as

\[
 a=\rho_{xy},\quad b=\rho_{xz},\quad c=\rho_{yz},\quad
 d=\rho_{ux},\quad e=\rho_{uy}:F\longrightarrow E_3,
\tag{1.1}
\]

and write the five ordered pentagon maps as

\[
 p_1,p_2,p_3,p_5,p_4:F\longrightarrow E_4.
\tag{1.2}
\]

The order in (1.2) is the printed A.18 occurrence order

\[
 b_1,b_2,b_3,b_5^{-1},b_4^{-1}.
\tag{1.3}
\]

The two hexagons and the pentagon contain eleven literal occurrences:

\[
 \Omega_{11}(w)=
 \bigl(a(w),b(w),c(w);d(w),a(w),e(w);
       p_1(w),p_2(w),p_3(w),p_5(w),p_4(w)\bigr).
\tag{1.4}
\]

The two copies of (a(w)) are the occurrences H1/1 and H2/2 of the same
source-E3 substitution ((x,y)).  Hence the distinct typed-coordinate map is

\[
 \Omega_{10}(w)=
 \bigl(a(w),b(w),c(w),d(w),e(w);
       p_1(w),p_2(w),p_3(w),p_5(w),p_4(w)\bigr).
\tag{1.5}
\]

This is exactly the task176 order

\[
 (d_EC_{21},d_EC_{22},d_EC_{23},d_EC_{24},d_EC_{25};
   C_1,C_{27},C_{21},C_{26},C_{28}).
\tag{1.6}
\]

There are two different kinds of repetition, and they must not be confused.

1. H1/1 and H2/2 are the same **E3** map (a=\rho_{xy}).  They may be stored
   once, because the missing occurrence is recovered by diagonal insertion.
2. The labels (d_EC_{21}) and (C_{21}) occur in (1.6), but the first lies
   in E3 and the second in E4.  They are different typed coordinates and may
   never be deduplicated.

The signs in (1.3), and the negative H2 occurrence, belong to the relation
formula.  They do not change the underlying conjugating-value homomorphisms
in (1.1)--(1.2).  Signs, occurrence order, block tags, and Fox prefix
transports remain part of the residual-module interface.

## 2. The seven objects are relation blocks

Define the two hexagon block images

\[
 Q_{H1}=\operatorname{im}(a,b,c),
 \qquad
 Q_{H2}=\operatorname{im}(d,a,e),
\tag{2.1}
\]

and the five one-occurrence pentagon images

\[
 Q_{Pj}=\operatorname{im}(p_j)
 \qquad (j=1,2,3,5,4).
\tag{2.2}
\]

Thus the phrase “seven contexts” in v173 means the seven relation blocks

\[
 H1,H2,P1,P2,P3,P5,P4,
\tag{2.3}
\]

where the first two blocks internally retain three occurrence coordinates
each.  Put

\[
 \Omega_7(w)=
 \bigl((a(w),b(w),c(w)),(d(w),a(w),e(w)),
       p_1(w),p_2(w),p_3(w),p_5(w),p_4(w)\bigr)
\tag{2.4}
\]

and

\[
 D_{10}=\operatorname{im}\Omega_{10},
 \qquad
 \Delta_7=\operatorname{im}\Omega_7.
\tag{2.5}
\]

### Theorem 2.1 (TEN-OCCURRENCE / SEVEN-BLOCK MARKED ISOMORPHISM)

There is a canonical marked isomorphism

\[
 \boxed{\theta:D_{10}\xrightarrow{\ \sim\ }\Delta_7}
\tag{2.6}
\]

given by

\[
 \theta(A,B,C,D,E;P_1,P_2,P_3,P_5,P_4)
 =((A,B,C),(D,A,E),P_1,P_2,P_3,P_5,P_4).
\tag{2.7}
\]

Its inverse forgets the repeated second-block (A)-slot:

\[
 \theta^{-1}((A,B,C),(D,A,E),P_1,P_2,P_3,P_5,P_4)
 =(A,B,C,D,E;P_1,P_2,P_3,P_5,P_4).
\tag{2.8}
\]

In particular,

\[
 \ker\theta=1.
\tag{2.9}
\]

#### Proof

Let

\[
 \iota:E_3^5\times E_4^5\longrightarrow E_3^6\times E_4^5
\tag{2.10}
\]

insert the first E3 coordinate in the H2/2 position, and let

\[
 \pi:E_3^6\times E_4^5\longrightarrow E_3^5\times E_4^5
\tag{2.11}
\]

delete that position.  Then

\[
 \Omega_{11}=\iota\Omega_{10},
 \qquad \pi\iota=1.
\tag{2.12}
\]

Every point of \(\operatorname{im}\Omega_{11}\) has equal H1/1 and H2/2
coordinates by (1.4), so

\[
 \iota\pi=1
 \quad\hbox{on }\operatorname{im}\Omega_{11}.
\tag{2.13}
\]

Consequently deletion and diagonal insertion restrict to inverse marked
group isomorphisms between the ten- and eleven-occurrence images.  Regrouping
the eleven coordinates into the two triples and five singletons in (2.4) is
an ambient direct-product reassociation, hence another isomorphism.  Their
composite is (2.7), and (2.8)--(2.9) follow.  Both maps commute with the
images of the marked source generators (x,y), so the isomorphism is marked.
\(\square\)

This is not an order-count argument.  The inverse is the explicit typed
coordinate operation (2.8), and it works for every source word.

## 3. Equality of the relation-module actions

Retain the block-tagged residual module

\[
 Z=Z_{H1}\oplus Z_{H2}\oplus Z_P.
\tag{3.1}
\]

Conjugation of one common source correction by (w\in F) translates the
three H1 occurrences by (a(w),b(w),c(w)), the three H2 occurrences by
(d(w),a(w),e(w)), and the five pentagon occurrences by the (p_j(w)).
Therefore the action defined from the ten-coordinate value
\(\Omega_{10}(w)\) is exactly the action defined from the seven-block value
\(\Omega_7(w)\) after transport by \(\theta\).

### Corollary 3.1 (ACTION-ALGEBRA IDENTIFICATION)

The marked isomorphism induces

\[
 \mathbf F_3[D_{10}]\cong\mathbf F_3[\Delta_7],
\tag{3.2}
\]

under which the complete H1/H2/P correction map, its actual cyclic defect
submodule, its annihilator, and every pointed/direct/pair span are unchanged.

#### Proof

The literal conjugation formula depends on the eleven occurrence values in
(1.4).  Equations (2.7)--(2.8) recover those values without loss from either
representation.  Relation signs and Fox prefixes are fixed block data and
are not altered by the coordinate reassociation.  Hence the actions and all
functorially constructed spans agree. \(\square\)

Thus v173 Proposition 1.1 and Theorem 3.1 remain valid after replacing its
ambiguous phrase “seven separately tagged evaluation contexts” by the seven
block maps (2.1)--(2.4).  One must not instead choose only one scalar
coordinate for either hexagon block.

## 4. Frozen R07 specialization

The executable inventory and receipts bind the abstract maps as follows.

1. Task175 records 11 occurrences, with counts H1=3, H2=3, P=5, and retains
   the five distinct source pairs
   ((x,y),(x,z),(y,z),(u,x),(u,y)).
2. V122 identifies those source-E3 maps with
   (d_EC_{21},\ldots,d_EC_{25}).
3. Task176 serializes the ten coordinates in (1.6), explicitly records the
   selected IDs
   `21,22,23,24,25,1,27,21,26,28`, and requires that the E3/E4 reuse of
   `C21` is not deduplicated.
4. Its direct evaluator applies the same source word to all ten maps.

The cross-checked task176 production run `33044121344` returned

\[
 |D_{10}|=357{,}128{,}352,
 \tag{4.1}
\]

using the exact extension-section reduction with

\[
 |\Gamma|=243,
 \qquad |Q_0|=1{,}469{,}664,
 \qquad 243\cdot1{,}469{,}664=357{,}128{,}352.
\tag{4.2}
\]

The receipt SHA-256 is
`715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41`.
The computation deliberately did not enumerate (D_{10}).

Combining this frozen replay with Theorem 2.1 fixes the task198 bridge
terminal mathematically as

```text
ROOF_BRIDGE_ISOMORPHISM
bridge kernel = 1
Delta0^(7) order = 357128352
```

provided the implementation independently reconstructs the exact maps and
sign/block ledger above.  `ROOF_BRIDGE_PROPER_QUOTIENT` is not a live branch
for this correctly defined seven-block target.

## 5. Consumer interface

A complete marked presentation

\[
 D_{10}\cong\langle x,y\mid R\rangle
\tag{5.1}
\]

transfers verbatim through \(\theta\) to

\[
 \Delta_7\cong\langle x,y\mid R\rangle.
\tag{5.2}
\]

The successor relator defects in v188 may therefore be evaluated directly
from the same source-word relator DAG.  No bridge-kernel relations and no
357-million-state traversal are added.  An implementation certificate need
only replay:

1. the five E3 and five E4 marked generator pairs;
2. diagonal reinsertion of the H2/2 E3 ((x,y)) value;
3. the immutable occurrence signs, block tags, and order; and
4. both composites (2.7)--(2.8) on the marked generators and on every
   streamed presentation relator.

```text
SEVEN RELATION BLOCKS / TEN UNIQUE COORDINATES:  PAPER_PROOF
TEN -> ELEVEN DIAGONAL INSERTION:                EXPLICIT INVERSE
TEN-COORDINATE -> SEVEN-BLOCK BRIDGE:            MARKED ISOMORPHISM
BRIDGE KERNEL:                                   TRIVIAL
TASK176 D_all ORDER:                             CROSS-CHECKED
COMPLETE MARKED ROOF PRESENTATION:               SEPARATE INPUT
ACTUAL SUCCESSOR K / POINTED MU1:                NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:          NOT DECLARED
```

`R07_TEN_OCCURRENCE_SEVEN_BLOCK_ACTION_BRIDGE_V189_PAPER_GRADE`
