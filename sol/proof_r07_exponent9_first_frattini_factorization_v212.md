# R07 exponent-nine factorization at the first relative Frattini rung v212

Author: Sol / 2026-08-28

Status: paper theorem strengthening v209--v211.  Although the 729-element
class-two exponent-nine endpoint does not factor through the frozen roof, it
does factor through the first matched relative pro-3 Frattini successor.
Consequently the named nonzero central extension class of v211 dies at that
first successor, the v210 invariant functional exists and is surjective, and
the complete exponent-nine image of the same-successor direction ideal is
zero.  Thus no 729-column repair traversal is needed: one actual projected
endpoint evaluation is constant on the whole same-multiplier fibre.  That
endpoint has not yet been produced, so no exact repair, compatible cofinal
lift, fake certificate, or Ihara witness is declared.
verified=false.

## 1. A general one-Frattini-layer factorization lemma

Let \(P\) be a group, let

\[
 \rho_0:P\twoheadrightarrow E_0,
 \qquad K_0=\ker\rho_0,
\tag{1.1}
\]

and put

\[
 \Phi_3(K_0)=K_0^3[K_0,K_0],
 \qquad E_1=P/\Phi_3(K_0).
\tag{1.2}
\]

Suppose that a quotient \(\eta:P\twoheadrightarrow N_9\) has a further
quotient

\[
 N_9\twoheadrightarrow N_3
\tag{1.3}
\]

such that:

1. \(P\to N_3\) factors through \(E_0\); and
2. \(L=\ker(N_9\to N_3)\) is elementary abelian of exponent three.

### Lemma 1.1 (ONE-LAYER CAPTURE)

Under these assumptions,

\[
 \boxed{\Phi_3(K_0)\subseteq\ker\eta.}
\tag{1.4}
\]

Hence \(\eta\) factors uniquely as a surjection

\[
 \boxed{E_1\twoheadrightarrow N_9.}
\tag{1.5}
\]

#### Proof

The factorization through \(E_0\) gives \(\eta(K_0)\subseteq L\).
Since \(L\) is abelian of exponent three,

\[
 \eta(K_0^3)=1,\qquad
 \eta([K_0,K_0])=1.
\tag{1.6}
\]

This proves (1.4).  The quotient property gives the factorization through
\(E_1=P/\Phi_3(K_0)\), and it remains surjective because
\(\eta\) is surjective. \(\square\)

The lemma is functorial: if a homomorphism of two such diagrams commutes with
the maps to \(N_9\) and \(N_3\), then the induced factorizations (1.5)
commute as well.  No section of \(E_1\to E_0\) is chosen.

## 2. The class-two exponent-nine kernels are elementary abelian

For \(r\in\{3,4\}\), retain the canonical verbal quotients of v208

\[
 \mathcal N_r(9)=
 PB_r/\langle\gamma_3PB_r, g^9\ (g\in PB_r)\rangle^{\mathrm{normal}}
\tag{2.1}
\]

and their reductions

\[
 \mathcal N_r(9)\twoheadrightarrow\mathcal N_r(3).
\tag{2.2}
\]

### Lemma 2.1 (THE 9-TO-3 KERNEL)

The kernel

\[
 L_r=\ker\bigl(\mathcal N_r(9)\to\mathcal N_r(3)\bigr)
\tag{2.3}
\]

is an elementary abelian 3-group.

#### Proof

V208 Lemma 2.1 gives class-two Malcev coordinates in
\(\mathbf Z/9\mathbf Z\): degree-one coordinates and central
commutator coordinates.  The kernel of reduction modulo three consists of
the tuples whose coordinates are all divisible by three.  Every such tuple
has order dividing three.  In multiplying two such tuples, the only
non-additive term is a bilinear commutator contribution from two
degree-one coordinates.  Both are divisible by three, so that contribution
is divisible by nine and vanishes.  Hence the kernel is abelian of exponent
three. \(\square\)

## 3. Factorization through every first context successor

Use v145's frozen first relative Frattini quotients

\[
 K_{r,0}=\ker(PB_r\to E_r),\qquad
 E_{r,1}=PB_r/\Phi_3(K_{r,0})
 \qquad(r=3,4).
\tag{3.1}
\]

The roof factor \(E_r\) contains the maximal exponent-three quotient
\(\Pi_r[3]\), and v208 gives a factorization

\[
 PB_r\to E_r\to\Pi_r[3]\twoheadrightarrow\mathcal N_r(3).
\tag{3.2}
\]

### Theorem 3.1 (CONTEXTWISE FIRST-RUNG FACTORIZATION)

For \(r=3,4\), the canonical exponent-nine map factors as

\[
 \boxed{
 PB_r\twoheadrightarrow E_{r,1}\twoheadrightarrow\mathcal N_r(9).}
\tag{3.3}
\]

These factorizations commute with every registered group homomorphism,
including substitution, deletion, and coface maps, and with every repeated
typed occurrence used in the two hexagons and five pentagon contexts.
Inverses of evaluated words are then respected automatically.

#### Proof

Apply Lemma 1.1 to

\[
 P=PB_r,\quad E_0=E_r,\quad
 N_9=\mathcal N_r(9),\quad N_3=\mathcal N_r(3).
\tag{3.4}
\]

Condition 1 is (3.2), and condition 2 is Lemma 2.1.  This proves (3.3).
The quotients in (2.1) are defined by verbal subgroups.  Every group
homomorphism preserves lower-central terms and ninth powers, so all the
displayed braid/source maps descend.  Uniqueness in Lemma 1.1 makes the
resulting squares commute. \(\square\)

## 4. The joint endpoint factors through the actual first successor

Let

\[
 F(x,y)\stackrel{\psi_1}{\twoheadrightarrow}\Delta_1
 \stackrel{p_1}{\twoheadrightarrow}\Delta_0
\tag{4.1}
\]

be the correctly typed joint marked images in, respectively, the first
relative Frattini contexts \(E_{r,1}\) and the roof contexts \(E_r\).  Let

\[
 \phi_9:F(x,y)\twoheadrightarrow D_9
\tag{4.2}
\]

be the eleven-occurrence exponent-nine endpoint map.  V210 gives
\(D_9\cong\mathcal H_2(9)\) and \(|D_9|=729\).

### Theorem 4.1 (JOINT FIRST-RUNG FACTORIZATION)

There is a unique marked surjection

\[
 \boxed{\tilde\phi_1:\Delta_1\twoheadrightarrow D_9}
\tag{4.3}
\]

such that

\[
 \tilde\phi_1\psi_1=\phi_9.
\tag{4.4}
\]

Equivalently, if \(H_1=\ker\psi_1\), then

\[
 \boxed{H_1\subseteq\ker\phi_9.}
\tag{4.5}
\]

#### Proof

Apply Theorem 3.1 at each of the eleven literal occurrences, retaining the
two separately tagged copies of the repeated E3 occurrence.  The commuting
context maps give a homomorphism from their joint source image
\(\Delta_1\) to the joint exponent-nine image \(D_9\).  Its composite
with the source map is (4.2), proving (4.4).  Since (4.2) is onto its image,
so is (4.3).  Equation (4.5) is the equivalent kernel statement.
\(\square\)

This is consistent with, and strictly sharper than, v211: \(D_9\) does not
factor through \(\Delta_0\), but the one missing elementary-abelian layer
is present in \(\Delta_1\).

## 5. The area functional is forced and surjective

Put

\[
 K=\ker(\Delta_1\to\Delta_0),\qquad
 C=\langle[x,y]^3\rangle\leq D_9.
\tag{5.1}
\]

V211 gives

\[
 \phi_9(H_0)=C\cong C_3,\qquad
 D_9/C\cong\Gamma,
\tag{5.2}
\]

where \(H_0=\ker(F\to\Delta_0)\).  The diagram induced by
(4.3) is

\[
\begin{array}{ccccccccc}
1&\to&K&\to&\Delta_1&\to&\Delta_0&\to&1\\
 &&\downarrow\lambda_C&&\downarrow\tilde\phi_1&&\downarrow q_9&&\\
1&\to&C&\to&D_9&\to&\Gamma&\to&1.
\end{array}
\tag{5.3}
\]

### Theorem 5.1 (FORCED AREA QUOTIENT OF THE SUCCESSOR KERNEL)

The restriction in (5.3) is a surjective roof-invariant homomorphism

\[
 \boxed{
 \lambda_C:K\twoheadrightarrow C,\qquad
 \lambda_C(k)=c^{3\lambda(k)},\qquad
 \lambda:K\twoheadrightarrow\mathbf F_3.}
\tag{5.4}
\]

For every v190 roof relator \(r_j\), with successor defect
\(b_j=\psi_1(r_j)\),

\[
 \boxed{\lambda(b_j)=\omega_j.}
\tag{5.5}
\]

After identifying \(C\) with the trivial roof module, this is exactly the
unique invariant functional of v210 Theorem 4.1.  In particular,

\[
 \boxed{\dim_{\mathbf F_3}K\geq1,\qquad
        \ker\lambda\ \text{ has codimension }1\ \text{ in }K.}
\tag{5.6}
\]

#### Proof

If \(k\in K\), its image in \(\Gamma=D_9/C\) is trivial by the
commutative diagram, so \(\tilde\phi_1(k)\in C\).  This defines
\(\lambda_C\), and the fixed coordinate
\(c^{3a}\leftrightarrow a\in\mathbf F_3\) defines \(\lambda\).
Conjugation by \(\Delta_1\) acts trivially on the central subgroup \(C\),
so both maps are invariant under the induced roof action.

The map \(H_0\to K\) is onto.  Given \(z\in C=\phi_9(H_0)\), choose
\(h\in H_0\) with \(\phi_9(h)=z\).  Then
\(\psi_1(h)\in K\) and (4.4) gives
\(\lambda_C(\psi_1(h))=z\).  Thus both maps are onto.  For a roof relator,

\[
 \lambda_C(b_j)=\tilde\phi_1(b_j)=\phi_9(r_j)=c^{3\omega_j},
 \qquad \lambda(b_j)=\omega_j,
\tag{5.7}
\]

which is (5.5) under the fixed additive coordinate on \(C\).  V210 proves
uniqueness because the \(b_j\) generate \(K\) as a roof module.  Finally,
\(K\) is elementary abelian and \(\lambda\) is a nonzero linear
functional, proving (5.6). \(\square\)

## 6. The v211 class dies at exactly this rung

Let

\[
 \alpha_9\in H^2(\Gamma,C_3)
\tag{6.1}
\]

be v211's nonzero class of
\(1\to C_3\to D_9\to\Gamma\to1\).  V211 proves
\(q_9^*\alpha_9\neq0\) on \(\Delta_0\).

### Corollary 6.1 (FIRST-RUNG DEATH)

\[
 \boxed{p_1^*q_9^*\alpha_9=0
 \quad\text{in }H^2(\Delta_1,C_3).}
\tag{6.2}
\]

Thus the pulled-back roof class \(q_9^*\alpha_9\) has exact Frattini depth
one: it is nonzero at the roof and zero after pullback to the first
successor.

#### Proof

The homomorphism \(\tilde\phi_1:\Delta_1\to D_9\) in (4.3)
lifts \(q_9p_1\).  Therefore
\(d\mapsto(d,\tilde\phi_1(d))\) is a section of the pullback of the
central extension along \(q_9p_1\), so the pullback class is zero.
\(\square\)

In the cohomology five-term sequence for
\(1\to K\to\Delta_1\to\Delta_0\to1\), the functional
\(\lambda\in\operatorname{Hom}(K,C_3)^{\Delta_0}\) therefore
transgresses, up to the standard sign convention, to the named nonzero
class \(q_9^*\alpha_9\).  This is the cohomological form of the literal
equality (5.5).

## 7. Zero projected repair directions

Let

\[
 J_1=\ker\bigl(\mathbf F_3[F]\to\mathbf F_3[\Delta_1]\bigr)
\tag{7.1}
\]

and let
\(\Phi_9:\mathbf F_3[F]\to\mathbf F_3[D_9]\) be induced
by \(\phi_9\).

### Theorem 7.1 (SAME-SUCCESSOR CONSTANCY)

\[
 \boxed{\Phi_9(J_1)=0.}
\tag{7.2}
\]

Consequently the complete exponent-nine projected endpoint change of every
same-\(\mu_1\) repair is zero.  If the actual pointed endpoint projects to
a nonzero vector, that vector is an exact obstruction to every
finite-support representative of the same first-successor multiplier.

#### Proof

The factorization (4.3) induces a group-algebra factorization

\[
 \mathbf F_3[F]\longrightarrow
 \mathbf F_3[\Delta_1]\longrightarrow
 \mathbf F_3[D_9].
\tag{7.3}
\]

Its first kernel therefore maps to zero, proving (7.2).  Equivalently, v209
Theorem 3.1 has \(L_1=\phi_9(H_1)=1\), so its ideal
\(I(L_1)\) is zero.  V195/v200 say that differences of
same-multiplier representatives lie in the corresponding direction ideal;
hence their projected endpoint change is zero. \(\square\)

The 729 columns in v210 Corollary 5.1 belong only to the branch
\(L_1=C_3\), which Theorem 4.1 now excludes.  Production must not spend
time traversing them.

## 8. Updated production frontier

The exponent-nine lane now requires only:

1. independently replay the 6,441 area values as a consistency certificate;
2. require their nonzero vector and verify (5.5) against the actual
   successor defect rows when those rows exist;
3. obtain the actual pointed first-successor representative \(M_0\);
4. evaluate its three separately tagged endpoints in the exponent-nine
   quotient; and
5. if the projected endpoint is nonzero, retain it and its coordinate dual
   as the complete same-\(\mu_1\) obstruction; if it is zero, record this
   screen as inconclusive and move to the next non-roof endpoint quotient.

No successor-kernel orbit closure, invariant-functional solve, or 729-state
repair-column traversal is mathematically needed for this screen.  The
actual word replay remains load-bearing.

\[
\begin{array}{ll}
D_9\ \text{ FACTORS THROUGH THE ROOF } \Delta_0
 & \text{NO / v211},\\
D_9\ \text{ FACTORS THROUGH THE FIRST SUCCESSOR } \Delta_1
 & \text{YES / PAPER PROOF},\\
\phi_9(H_1)=1
 & \text{PAPER PROOF},\\
\lambda:K\twoheadrightarrow C_3
 & \text{UNIQUE, INVARIANT, SURJECTIVE / PAPER PROOF},\\
q_9^*\alpha_9\neq0,\quad p_1^*q_9^*\alpha_9=0
 & \text{EXACT FRATTINI DEPTH ONE},\\
\Phi_9(J_1)=0
 & \text{COMPLETE SAME-SUCCESSOR CONSTANCY},\\
\text{729-COLUMN REPAIR TRAVERSAL}
 & \text{ELIMINATED},\\
\text{ACTUAL PROJECTED ENDPOINT}
 & \text{NOT YET COMPUTED},\\
\text{COFINAL LIFT / FAKE / IHARA WITNESS}
 & \text{NOT CONSTRUCTED}.
\end{array}
\tag{8.1}
\]

`R07_EXPONENT9_FIRST_FRATTINI_FACTORIZATION_V212_PAPER_GRADE`
