# R07 A0: audited relative fibre-echelon lift through an elementary 3-kernel (v441)

Author: Sol / 2026-09-03

This supersedes v440 after independent Task544 verdict
RELATIVE_FIBRE_ECHELON_SOUND_AFTER_REPAIR. It gives a conditional exact
algorithm for each of the two post-2016 finite lifts. It is not a computation,
a uniform surjectivity theorem, a relative homotopy on every class, or a
cofinal compatible lift. No A0, COMMON, fake or Ihara conclusion is declared.
verified=false.

## 1. Extension and filtration

Let \(k=\mathbf F_3\), and consider an extension preserved by every
registered occurrence automorphism,

\[
 1\longrightarrow V\longrightarrow\widetilde Q
   \stackrel{\pi}{\longrightarrow}Q\longrightarrow1,
 \qquad V\cong C_3^3.                                  \tag{1.1}
\]

For \(R=k[\widetilde Q]\), \(\bar R=k[Q]\), and the augmentation ideal
\(J(V)\subset k[V]\), normality gives

\[
 I:=\ker(R\to\bar R)=R J(V)=J(V)R,\qquad
 I^d=R J(V)^d=J(V)^dR.                                \tag{1.2}
\]

Choose \(v_1,v_2,v_3\) in \(V\) and put \(u_i=v_i-1\). Then

\[
 k[V]\cong k[u_1,u_2,u_3]/(u_1^3,u_2^3,u_3^3),
 \qquad I^7=0.                                         \tag{1.3}
\]

The per-transversal grade multiplicities are

\[
 h_d=[t^d](1+t+t^2)^3=(1,3,6,7,6,3,1)_d.
\]

The total group-algebra grade dimensions are

\[
 \boxed{\dim_k I^d/I^{d+1}=|Q|h_d}.                   \tag{1.4}
\]

Let \(\mathcal M\) be the finite space spanned by all legal literal
compact-relator conjugates at \(\widetilde Q\). Let
\(\mathcal O\) be the occurrence-separated module, with its correlated
source action, and let \(W\) be the physical module after the fixed signed
aggregation and boundary quotient. Write

\[
 \mathcal M\stackrel{J_{\rm occ}}{\longrightarrow}
 \mathcal O\stackrel{\Pi_g}{\longrightarrow}W,\qquad
 A=\Pi_gJ_{\rm occ}.                                  \tag{1.5}
\]

The action on \(\mathcal O\) is the six-tag semilinear action. No common
actor action on \(W\) is assumed. Every map in (1.5), every fixed prefix and
the PB3/PB4 boundary quotient must commute with reduction through the
characteristic tower.

Filter every regular coordinate of \(W\) by
\(F^dW=I^dW\). Let
\(\nu:\mathcal M\to k^2\) be normalized exponent and define

\[
 C_d(m)=(\nu(m),A(m)\bmod F^dW),\qquad
 D_d=\ker C_d.                                        \tag{1.6}
\]

Thus

\[
 D_d=\{m:\nu(m)=0,\ A(m)\in F^dW\}.                   \tag{1.7}
\]

## 2. Canonical image fibre

Put \(E_d=\operatorname{im}C_d\). Reduction induces a surjection

\[
 p_d:E_{d+1}\longrightarrow E_d.
\]

Its kernel lies canonically in \(G_d=F^dW/F^{d+1}W\); denote it by
\(K_d\).

### Theorem 2.1

Restriction of \(C_{d+1}\) gives a canonical isomorphism

\[
 \boxed{
 B_d:D_d/D_{d+1}\stackrel{\sim}{\longrightarrow}K_d,
 \quad [m]\longmapsto A(m)\bmod F^{d+1}W.}             \tag{2.1}
\]

#### Proof

For \(m\in\mathcal M\), the class \(C_{d+1}(m)\) maps to zero in \(E_d\)
exactly when \(\nu(m)=0\) and \(A(m)\in F^dW\), namely \(m\in D_d\).
The remaining coordinate is its class in \(G_d\). Its kernel is precisely
the stronger condition \(A(m)\in F^{d+1}W\), namely \(D_{d+1}\).
\(\square\)

### Corollary 2.2

Suppose \(c_{d-1}\) has the required normalized exponent and

\[
 A(c_{d-1})\equiv T\pmod {F^dW}.
\]

Define

\[
 \rho_d=(T-A(c_{d-1}))\bmod F^{d+1}W\in G_d.           \tag{2.2}
\]

There is a correction through the next grade if and only if

\[
 \rho_d\in K_d.                                       \tag{2.3}
\]

Indeed, every lower solution is uniquely of the form
\(c_{d-1}+\delta\) with \(\delta\in D_d\), up to its actual equality in
\(\mathcal M\). Thus (2.3) ranges over differences from all lower solutions,
not merely over visibly degree-\(d\) coefficient changes of the chosen
representative. A functional on the whole \(G_d\) that kills \(K_d\) and is
nonzero on \(\rho_d\) excludes every solution modulo \(F^{d+1}W\).

## 3. Exact occurrence-first fibre echelon

At precision \(d+1\), start again from the original 44 compact seeds. Close
their images under the four correlated source actors
\(x,x^{-1},y,y^{-1}\) in the source or complete occurrence-separated module
\(\mathcal O/F^{d+1}\mathcal O\). Carry a coefficient-bearing source DAG with
every retained occurrence row. Queue exhaustion must be proved.

Only after that closure is complete, apply the fixed aggregation
\(\Pi_g\) to every retained complete row and form \(C_{d+1}\). Choose
coordinates adapted to

\[
 0\longrightarrow G_d\longrightarrow
 k^2\oplus W/F^{d+1}W
 \longrightarrow k^2\oplus W/F^dW\longrightarrow0.    \tag{3.1}
\]

Write each aggregated row as \((L\mid G)\). Reduce \(L\) against a
lower-pivot echelon while carrying \(G\) and ancestry through the identical
operations.

- If a new lower pivot remains, retain the complete row.
- If its lower block becomes zero, insert the remaining grade block in a
  separate fibre echelon and retain its complete ancestry.

### Theorem 3.1

After the occurrence actor queue is exhausted and every retained occurrence
row has been aggregated and processed, the separate grade echelon spans
exactly \(K_d\).

#### Proof

For any fixed complete input span, lower-first elimination is ordinary block
Gaussian elimination. Every zero-lower remainder lies in the kernel of the
projection to \(E_d\). Conversely, reducing any combination with zero lower
part expresses its grade part as a combination of the zero-lower remainders.
The occurrence-first exhausted closure supplies the complete legal orbit
image, so Theorem 2.1 identifies this kernel with \(K_d\). \(\square\)

It is unsound to close only retained aggregated physical rows. Aggregation
need not carry a well-defined common actor action: two source rows with the
same physical image can have actor images with different physical images.
Therefore an aggregated dependent row may never be discarded before its
source or occurrence actor descendants have been accounted for.

## 4. Avoiding the lost-kernel error

Directions with nonzero lower-degree source coefficients can cancel
physically through degree \(d-1\) and then correct degree \(d\). Hence
\(D_d\) must not be replaced by \(I^d\mathcal M\), by the chosen preceding
corrections, or by a lower-precision physical image basis.

Two sufficient implementation choices are:

1. retain source ancestry for the complete kernel of every earlier \(C_j\)
   and propagate it at higher precision;
2. regenerate the occurrence-first closure from the original 44 seeds at
   every new precision and recompute the two-block fibre.

The second is the simplest fail-closed route. It may cache group arithmetic,
transversals and seed evaluations, but it recomputes the high-precision
legal image rather than promoting a lower-precision image basis.

## 5. Deterministic literal representative

The map \(B_d\) in (2.1) is already a canonical isomorphism. Fixed seed,
actor, coordinate and pivot orders let echelon reduction choose a
representative

\[
 \widehat h_d:K_d\longrightarrow D_d,\qquad
 A(\widehat h_d(\rho))\equiv\rho\pmod {F^{d+1}W}.      \tag{5.1}
\]

Its class modulo \(D_{d+1}\) is the canonical inverse of \(B_d\). This is a
choice of representative, not a proof that \(K_d=G_d\).

Every DAG leaf is a literal conjugate \(d r_i d^{-1}\). Combining equal
leaves modulo three and pinning the interpretation of coefficient two gives
an ordered correction word. All its factors are identities in the finite
quotient, so the Fox product rule reduces to addition and directly replays
the selected row.

If and only if each actual residual is MEMBER, six successive representative
updates and residual recomputations give one class-specific filtered
correction for this extension. The six maps are not asserted to compose as a
global homotopy, and no uniform surjectivity is claimed. The dihedral
antisymmetrizer may give a closed section on its odd summand; (5.1) is the
finite class-specific treatment of the complementary actual residual.

## 6. The two R07 extensions

Use

\[
 Q_1=Q_0/(1\times G9'),\qquad
 Q_2=Q_0/(1\times(G9')^3).
\]

The pinned equality \(G9'=C_9^3\) gives

\[
\begin{aligned}
 1&\to G9'/(G9')^3\cong C_3^3
      \to Q_2\to Q_1\to1,\\
 1&\to (G9')^3\cong C_3^3
      \to Q_0\to Q_2\to1,
\end{aligned}                                         \tag{6.1}
\]

with

\[
 |Q_1|=2016,\qquad |Q_2|=54,432,\qquad
 |Q_0|=1,469,664.                                     \tag{6.2}
\]

The solvable radical \(1\times G9\), its derived subgroup
\(1\times G9'\), and its power subgroup \(1\times(G9')^3\) are
characteristic. Hence all registered occurrences preserve both extensions.
This characteristicity is also an executable certificate gate, not merely
a paper observation.

Each extension has the six positive grade multiplicities

\[
 (3,6,7,6,3,1).                                       \tag{6.3}
\]

For the first extension, the largest new-grade occurrence and physical
coordinate blocks before a further exact decomposition have dimensions

\[
 6\cdot2\cdot2016\cdot7=169,344,\qquad
 2\cdot2\cdot2016\cdot7=56,448.                        \tag{6.4}
\]

These are coordinate counts, not time or memory estimates. If all first six
tests are MEMBER, their literal updates solve the order-54,432 floor. If all
second six tests are MEMBER, their updates solve the full-Q0 coarse floor.

## 7. Exact data and certificate gates

Every extension/grade certificate must bind and independently replay:

1. the marked exact extension, orders, kernel equality and characteristic
   tower;
2. a transversal, its kernel-valued multiplication cocycle, and the quotient
   conjugation action on \(V\);
3. preservation of \(I^d\) by every occurrence, its quotient action,
   restriction to \(V\), crossed cochain and full truncated substitutions
   \(u_i\mapsto\prod_j(1+u_j)^{m_{ji}}-1\);
4. the 44 literal identities and normal-generation authority at the current
   quotient;
5. occurrence-separated semilinear chain-rule identities, correlated source
   actor action, left-prefix convention, six signs and full-extension g760
   prefix values;
6. the PB3 normal map, every translated PB3 boundary row, the PB4
   boundary/block, and commutation of boundary reduction with filtration,
   occurrence transport and aggregation;
7. normalized exponent divisibility before mod-three reduction, its fixed
   actor action and its presence in every lower block;
8. coordinate/filtration bases, target, exhausted occurrence closure,
   lower/fibre ranks and canonical residual digest.

MEMBER additionally requires all coefficient operations producing the fibre
preimage, a literal accumulated correction, zero normalized exponent, zero
lower change, direct grade replay and the next residual. NONMEMBER requires a
dual on the full grade coordinates, annihilation of every final fibre row
and nonzero residual pairing.

## 8. Claim boundary

A negative grade dual becomes an A0 obstruction only after the complete
quotient and PB3/PB4 boundary-killing chain has been independently rebound.
Twelve positive tests give a finite full-Q0 coarse correction, not by
themselves a cofinal compatible lift, fake, or Ihara witness.

ORDER-2016 RESULT:                 NOT YET COMPUTED
Q1->Q2 RELATIVE ALGORITHM:         PAPER-CLOSED CONDITIONALLY; SIX FIBRE TESTS
Q2->Q0 RELATIVE ALGORITHM:         PAPER-CLOSED CONDITIONALLY; SIX FIBRE TESTS
ACTUAL TWISTING DATA / RUNS:       NOT YET MATERIALIZED
UNIFORM GRADE SURJECTIVITY:        NOT CLAIMED
FULL-Q0 CORRECTION:                NOT COMPUTED
A0 / COMMON / COFINAL LIFT:        NOT DECIDED
FAKE / IHARA:                      NOT DECLARED
verified:                          false

R07_A0_RELATIVE_FIBRE_ECHELON_LIFT_V441_PAPER
