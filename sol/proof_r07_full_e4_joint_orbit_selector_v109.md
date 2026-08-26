# R07 full-E4 joint-orbit correction selector v109

Author: Sol / 2026-08-27

Status: exact paper reduction from the registered common-value correction
domain to a finite, provenance-bearing full-\(E_4\) linear system.  It removes
the positive-direction \(E_4\twoheadrightarrow\Pi_4[3]\) loss from the next
target6 computation.  The required full orbit calculation has not yet been
run.  The theorem concerns one target6 component and does not by itself prove
literal A.18, cofinal compatibility, a fake, or an Ihara witness.

## 1. Full context kernel and the correction cocycle

Let \(F=F(x,y)\).  Denote the three substitutions used by target6 by

\[
 \phi_A(w)=w(X_0,Y_0),\qquad
 \phi_B(w)=w(X_0,Z_0),\qquad
 \phi_C(w)=w(Y_0,Z_0).
\tag{1.1}
\]

Evaluation in the pinned full group \(E_4\) gives

\[
 \omega_E:F\longrightarrow E_4^3,
 \qquad
 \omega_E(w)=
 (\overline{\phi_A(w)},\overline{\phi_B(w)},
  \overline{\phi_C(w)}),
\tag{1.2}
\]

and put \(\Delta_E=\operatorname{im}\omega_E\).  Let

\[
 \Omega^+:F\longrightarrow
 G_{\rm joint}\times(\mathbf F_3)^2
\tag{1.3}
\]

be the task-157ee marked joint value map, augmented by the two exponent sums
modulo three.  Its kernel

\[
 N^+=\ker\Omega^+
\tag{1.4}
\]

consists exactly of words invisible in the registered
\(Q_0/E_3/31\)-context value gate and in the historical exponent-mod-three
gate.  Since the three contexts in (1.2) occur among the registered contexts,

\[
 N^+\subseteq\ker\omega_E.
\tag{1.5}
\]

Let \(R_E=\mathbf F_3[E_4]\), and let \(p\in E_4\) be the fixed g760 prefix
action.  With the pinned Fox convention define

\[
 \Sigma_E(w)=
 p\bigl(\nabla\phi_C(w)-\nabla\phi_B(w)\bigr)
 +\nabla\phi_A(w)
 \in R_E^6.
\tag{1.6}
\]

This is the unprojected version of the row called `projected_sigma` in the
Jennings calculation.

### Lemma 1.1 (FULL-KERNEL ADDITIVITY)

The restriction

\[
 \boxed{\Sigma_E:N^+\longrightarrow R_E^6}
\tag{1.7}
\]

is a group homomorphism to the additive group.  In particular it kills
cubes and commutators internal to \(N^+\).

#### Proof

For each substitution \(\phi\), the Fox cocycle identity is

\[
 \nabla\phi(uv)=\nabla\phi(u)
 +\overline{\phi(u)}\nabla\phi(v).
\tag{1.8}
\]

If \(u,v\in N^+\), all three evaluated values in (1.2) are one by (1.5).
Thus each of the three gradients in (1.6) is additive on \(N^+\), and the
fixed left translation by \(p\) preserves addition.  This proves (1.7).
The target is an \(\mathbf F_3\)-space, so cubes and commutators vanish.
\(\square\)

The qualification "internal to \(N^+\)" is load-bearing.  The raw map need
not kill an element of \([K_3,K_3]\cap N^+\), because the larger projected
kernel \(K_3\) need not lie in the full kernel (1.5).  Consequently the
28-coordinate image from v107 is sufficient after projection but is not, by
itself, the complete raw-\(E_4\) correction image.

## 2. Conjugation depends on one finite context state

Let \(r\in\ker\omega_E\) and \(u\in F\).  Applying (1.8) to
\(uru^{-1}\), using \(\overline{\phi(r)}=1\), gives

\[
 \nabla\phi(uru^{-1})
 =\overline{\phi(u)}\nabla\phi(r).
\tag{2.1}
\]

Indeed, the gradient terms belonging to \(u\) and \(u^{-1}\) cancel.
Therefore

\[
 \boxed{
 \Sigma_E(uru^{-1})
 \text{ depends only on }r\text{ and }\omega_E(u)\in\Delta_E.}
\tag{2.2}
\]

This is the exact finite-state compression needed for a full-\(E_4\) orbit
calculation.  There is no need to distinguish two conjugators having the same
ordered triple of full context values.

## 3. Normal generators and the complete orbit image

Let \(N=\ker\Omega\) omit the exponent factor for a moment.  Let
\(\mathcal R\subset F\) be the finite relation-word roster reconstructed from
the complete task-157ee presentation:

1. the 6,318 Gamma Cayley-edge relations;
2. the 104 x/y action relations; and
3. the 19 complete \(Q_0\)-factor relations with Gamma defects.

Thus

\[
 N=\langle\!\langle\mathcal R\rangle\!\rangle_F.
\tag{3.1}
\]

For \(r\in\mathcal R\) and \(\delta\in\Delta_E\), choose any word
\(u_\delta\) with \(\omega_E(u_\delta)=\delta\), and define the augmented
column

\[
 v_{\delta,r}=
 \bigl(
 \Sigma_E(u_\delta r u_\delta^{-1}),
 \epsilon_3(r)
 \bigr)
 \in R_E^6\oplus(\mathbf F_3)^2.
\tag{3.2}
\]

Here \(\epsilon_3\) is the pair of source exponent sums modulo three.
Conjugation does not change this pair.

### Theorem 3.1 (FULL-E4 JOINT-ORBIT IMAGE)

\[
 \boxed{
 \operatorname{im}
 \bigl((\Sigma_E,\epsilon_3):N\to
 R_E^6\oplus(\mathbf F_3)^2\bigr)
 =operatorname{span}_{\mathbf F_3}
 \{v_{\delta,r}:\delta\in\Delta_E, r\in\mathcal R\}.}
\tag{3.3}
\]

#### Proof

By (3.1), every \(n\in N\) is a finite product

\[
 n=\prod_\nu
 (u_\nu r_\nu u_\nu^{-1})^{e_\nu},
 \qquad r_\nu\in\mathcal R,quad e_\nu\in\mathbf Z.
\tag{3.4}
\]

Every factor lies in the normal subgroup \(N\), which is contained in the
three-context kernel.  Lemma 1.1 is therefore additive on the product, and
the characteristic-three target replaces \(e_\nu\) by its residue modulo
three.  Equation (2.2) replaces each \(u_\nu\) by the fixed representative of
its state in \(\Delta_E\).  The same argument applies to \(\epsilon_3\), so
the image in (3.3) is contained in the displayed span.  Conversely every
displayed column is the image of the actual conjugate word
\(u_\delta r u_\delta^{-1}\in N\), proving the reverse containment.
\(\square\)

The last two exponent coordinates solve the legal gate without demanding
that every individual orbit generator already have exponent zero.  A linear
combination with total exponent coordinate zero materializes a product in
\(N^+=N\cap\ker\epsilon_3\).

## 4. Exact full-E4 target6 criterion

Let \(T_E\in R_E^6\) be the unprojected g760 target6 Fox row, and let

\[
 D_E=\operatorname{im}D_{2,E}\subseteq R_E^6
\tag{4.1}
\]

be the span of the eleven PB4 Fox columns and all full-\(E_4\) left
translations.  V108 proves that these eleven relators present the true marked
\(P_4\), so (4.1) is now the true presentation-boundary image rather than a
one-sided approximation.

### Theorem 4.1 (FULL-E4 TARGET6 SELECTOR)

There exists an actual registered-joint-value and exponent-three correction
word \(c\in N^+\) satisfying

\[
 T_E-\Sigma_E(c)\in D_E
\tag{4.2}
\]

if and only if

\[
 \boxed{
 (T_E,0,0)in
 (D_E\oplus0\oplus0)
 +\operatorname{span}_{\mathbf F_3}
 \{v_{\delta,r}\}.}
\tag{4.3}
\]

Moreover, any displayed coefficient solution of (4.3) prints an explicit
word:

\[
 \boxed{
 c=\prod_{(\delta,r)}
 (u_\delta r u_\delta^{-1})^{a_{\delta,r}},
 \qquad a_{\delta,r}\in\{0,1,2\}.}
\tag{4.4}
\]

#### Proof

If (4.2) holds, apply Theorem 3.1 to
\((\Sigma_E(c),\epsilon_3(c))=(\Sigma_E(c),0,0)\); this yields (4.3).
Conversely, use the orbit coefficients in (4.3) to form (4.4).  Normality
puts \(c\) in \(N\), the last two coordinates put it in
\(\ker\epsilon_3\), and Lemma 1.1 identifies its first coordinate with the
orbit-column sum.  The remaining first-coordinate term is in \(D_E\), which
is (4.2).  \(\square\)

This is an equality criterion for the pinned target6 abelian
relation-module layer, not an overapproximation.  It simultaneously closes,
for that layer, the two positive gaps still present after a task-168
coefficient receipt:

1. it works in full \(E_4\), not in \(\Pi_4[3]\); and
2. every correction column carries an actual common-value-kernel word.

## 5. Relation to the j=9--12 calculation

The Jennings calculation uses the quotient

\[
 R_E\longrightarrow
 \mathbf F_3[\Pi_4[3]]/I^j.
\tag{5.1}
\]

For the pinned PC group the ten Jennings weights are

\[
 (1,1,1,1,1,1,2,2,2,2),
\tag{5.2}
\]

and every PC exponent ranges through \(0,1,2\).  Hence the largest Jennings
monomial degree is

\[
 2(6\cdot1+4\cdot2)=28.
\tag{5.3}
\]

Thus

\[
 I^{29}=0,
\tag{5.4}
\]

and \(j=29\) is the exact terminal projected calculation.  The nested
families satisfy

\[
 \mathcal A_{29}^{\rm joint}subseteq\cdots
 \subseteq\mathcal A_{10}^{\rm joint}subseteq
 \mathcal A_9^{\rm joint}.
\tag{5.5}
\]

Consequently:

- an empty family at any depth kills the pinned branch at that projected
  gate;
- a nonempty family at \(j=9\) is useful positive input but not exact; and
- a full-\(E_4\) solution of (4.3) automatically survives every projected
  depth through \(j=29\).

Once the full-orbit solver in (4.3) is available, completing every
intermediate \(j=10,\ldots,28\) is no longer a logical prerequisite for a
positive result.  Those depths remain useful cheaper fatal screens and
diagnostics.  In particular, the lex-first point selected at \(j=9\) must not
be frozen as the only full-\(E_4\) candidate; a different point of the same
affine family, or a conjugation direction invisible in the 28 projected
coordinates, may be required by (4.3).

## 6. Executable finite column generation

Although \(\Delta_E\) can be large, Theorem 4.1 does not require materializing
its whole orbit before finding a positive certificate.  Use a
provenance-bearing dual column-generation loop:

1. start with the authenticated PB4 D2 prefix and a bounded set of
   joint-relation orbit columns;
2. reduce \((T_E,0,0)\);
3. if a remainder survives, lift a dual functional and correlate it with the
   complete PB4-D2 and joint-correction orbit families;
4. add the canonical first ACTIVE block, retaining its relation word and
   conjugator section;
5. repeat until the target reduces to zero or a complete zero correlation is
   obtained.

A positive terminal needs only the finitely many selected columns and direct
replay of (4.4).  A negative terminal requires a complete correlation against
both full column families.  A resource cap is `UNKNOWN`, never a proof.

The task-157eg--157en full-\(E_4\) infrastructure already implements the
PB4-D2 half of this pattern.  Task 169 reconstructs the relation words and
their exact value pins.  The smallest useful successor is therefore an
integrated target6 run adding the columns (3.2), not another unconstrained
4096-word search.

## 7. Exact remaining boundary

A positive, independently replayed solution of (4.3) would prove one explicit
full-\(E_4\) target6 correction at the pinned abelian relation-module layer,
in the registered joint value plus exponent-mod-three domain.  It would still
leave:

1. the second hexagon for the same word;
2. the ordered five-coface A.18 defect for that same word;
3. the exact integral commutator/exponent condition and any registered
   syzygy, charmingness, onto, descent, and settlement side gates not implied
   by those direct evaluations;
4. HT1--HT5 across later abelian chief refinements; and
5. accepted-set nonemptiness across nonabelian chief refinements.

```text
FULL-KERNEL ADDITIVITY:                         PAPER_PROOF
FINITE CONTEXT-ORBIT COMPRESSION:               PAPER_PROOF
FULL-E4 JOINT-ORBIT IMAGE THEOREM:               PAPER_PROOF
TRUE PB4 D2 INPUT (v108):                       COMPLETE
j=9 COEFFICIENT FAMILY:                         WAITING FOR TASK 168 FULL RUN
PROJECTED JOINT INTERSECTION:                   WAITING FOR TASK 169
FULL-E4 ORBIT SYSTEM:                           NOT YET EXECUTED
EXPLICIT FULL-E4 TARGET6 CORRECTION:            NOT YET CONSTRUCTED
ALL-SEVEN RELATION REPLAY / COFINAL LIFT:       OPEN
FAKE / IHARA WITNESS:                           NOT DECLARED
```
