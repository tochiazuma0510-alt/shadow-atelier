# R07 Q4-to-Q0 noncontiguous deletion layout v135

Author: Sol / 2026-08-27

Status: paper proof and implementation erratum.  This note fixes the exact
permutation-block realization of the fourth-strand coarse deletion used by
task176.  It does not alter v122's abstract deletion theorem.  No census
order, common correction, cofinal lift, fake, or Ihara witness is declared.

## 1. Frozen permutation layouts

The authenticated coarse models use

\[
 Q_4\le P^4\times H_9,
 \qquad H_9\le G_9^4,
 \qquad Q_0=P\times G_9,
\tag{1.1}
\]

with permutation degrees

\[
 \deg P=9,\qquad \deg G_9=27,\qquad
 \deg Q_4=4\cdot9+4\cdot27=144,\qquad
 \deg Q_0=9+27=36.
\tag{1.2}
\]

The zero-based point intervals in the frozen Q4 row are therefore

\[
\begin{array}{c|cccc}
\text{factor}&P_1&P_2&P_3&P_4\\ \hline
\text{interval}&[0,9)&[9,18)&[18,27)&[27,36)
\end{array}
\tag{1.3}
\]

followed by

\[
\begin{array}{c|cccc}
\text{factor}&G_{9,1}&G_{9,2}&G_{9,3}&G_{9,4}\\ \hline
\text{interval}&[36,63)&[63,90)&[90,117)&[117,144).
\end{array}
\tag{1.4}
\]

This layout is independently replayed in
`search/check_d972_b34_q3_positive_first_v1.py`: the first four 9-point
restrictions are required to lie in the frozen P group, and the four
27-point restrictions of the final H9 block are required to lie in the
frozen G9 group.  V122 Section 2 likewise specifies projection to the
fourth P block and the fourth G9 block.

## 2. Exact fourth-strand restriction

Let \(\sigma\) be a frozen Q4 permutation, written as a zero-based image
array of length 144.  Define \(R_4(\sigma)\) on 36 points by

\[
 \boxed{
 \begin{aligned}
 R_4(\sigma)(i)&=\sigma(27+i)-27,
     &&0\le i<9,\\
 R_4(\sigma)(9+j)&=\sigma(117+j)-108,
     &&0\le j<27.
 \end{aligned}}
\tag{2.1}
\]

The second subtraction is \(108=117-9\): it sends the input interval
\([117,144)\) to the Q0 output interval \([9,36)\), not to \([0,27)\).

### Theorem 2.1 (NONCONTIGUOUS COARSE DELETION)

On the frozen block-preserving Q4 model, \(R_4\) is a homomorphism to the
frozen degree-36 model \(P\times G_9\).  On the six marked PB4 generators
\((A_{12},A_{13},A_{14},A_{23},A_{24},A_{34})\), its values are

\[
 \boxed{(X,Z,1,Y,1,1),\qquad Z=(YX)^{-1}.}
\tag{2.2}
\]

#### Proof

Every Q4 element preserves each factor interval in (1.3)--(1.4).  Restriction
to one invariant interval commutes with multiplication and inverse.
Relabelling the fourth P interval by subtracting 27 and the fourth G9
interval by subtracting 108 gives the disjoint degree-36 action in (2.1), so
\(R_4\) is a homomorphism.

The Q4 marked row is built from the four strand-deletion targets.  Selecting
the fourth P and fourth G9 coordinates is precisely deletion of strand four.
The frozen marked table of v122 (2.2) is then (2.2) above.  In the matched E3
model the three nontrivial values are respectively the coarse parts of
\(A_{12},A_{13},A_{23}\), namely \(X,Z,Y\). \(\square\)

## 3. Why the contiguous suffix is wrong

The interval \([108,144)\) is not a Q0 factor.  By (1.4) it consists of the
last nine points of \(G_{9,3}\) together with all 27 points of \(G_{9,4}\).
Consequently

\[
 \sigma[108:144]
\tag{3.1}
\]

mixes two different invariant G9 blocks and omits the required P4 block.
Even when its entries happen to form 36 distinct numbers after a shift, it
cannot realize the marked homomorphism (2.2).  The task176 production stop

```text
CENSUS_REJECT:coarse marked fourth-strand deletion
```

at run `33039406462` is exactly the expected fail-closed consequence of this
layout error; it is not an order or nonexistence result.

## 4. Executable contract

The repaired producer and independent checker must each:

1. require a canonical packed 144-byte permutation;
2. require invariance of both intervals \([27,36)\) and \([117,144)\);
3. construct the packed 36-byte permutation by (2.1);
4. replay all six marked values in (2.2);
5. reject a contiguous-suffix selector, a wrong P block, a wrong G9 block,
   and an output-offset mutation; and
6. compose this coarse map with the separately reconstructed fine
   \(d_\Pi\), retaining the canonical `tuple[bytes,bytes]` E3 element type.

The immutable mathematical endpoint remains

\[
 d_E=d_Q\times d_\Pi,
 \qquad d_E i_E=1.
\tag{4.1}
\]

```text
ABSTRACT FOURTH-STRAND DELETION (v122):       PAPER_PROOF
EXACT Q4/Q0 PERMUTATION BLOCK FORMULA:        PAPER_PROOF / v135
TASK176 REPAIRED EXECUTABLE REPLAY:            PENDING
ALL-SEVEN CENSUS:                              UNKNOWN
COMMON CORRECTION / COFINAL LIFT / FAKE:       NOT DECLARED
```
