# R07 exponent-nine relative-kernel compression v209

Author: Sol / 2026-08-28

Status: paper theorem refining the finite screen of v208 and the projected
selector of v200.  In the class-two exponent-nine screen, the image of the
entire first-successor kernel is recovered from one rank closure on the
6,441 roof-relator defect pairs.  No Schreier roster of the enormous
successor group is needed.  The resulting projected same-multiplier repair
span has at most \(3\cdot729=2{,}187\) translating columns.  The actual
relator defects, first multiplier, endpoint, span, dual, compatible lift,
fake certificate, and Ihara witness remain uncomputed.  `verified=false`.

## 1. The two relative kernels

Put \(k=\mathbf F_3\), \(F=F(x,y)\), and retain the actual roof and first
elementary-abelian successor

\[
 F\xrightarrow{\psi_1}\Delta_1
 \xrightarrow{\pi_{10}}\Delta_0,
 \qquad
 \psi_0=\pi_{10}\psi_1.
\tag{1.1}
\]

Write

\[
 H_0=\ker\psi_0,\qquad H_1=\ker\psi_1,
 \qquad K=\ker(\Delta_1\to\Delta_0)\cong(C_3)^t.
\tag{1.2}
\]

Let

\[
 \phi_9:F\twoheadrightarrow D_9
\tag{1.3}
\]

be the eleven-occurrence joint source image in the class-two exponent-nine
PB3/PB4 quotients of v208.  Coordinate reduction modulo three gives

\[
 D_9\twoheadrightarrow D_3.
\tag{1.4}
\]

By v208 Theorem 1.1, the map \(F\to D_3\) factors through \(\Delta_0\).
Moreover its source quotient is not a proper quotient of the free
two-generator exponent-three class-two group.  In the marked decomposition

\[
 PB_3\cong F(x=A_{12},y=A_{23})\times\langle c\rangle,
 \qquad c=A_{12}A_{13}A_{23},
\tag{1.5}
\]

the class-two exponent-three verbal quotient restricts on the displayed
free factor to

\[
 \mathcal H_2(3)=F/(F^3\gamma_3F).
\tag{1.6}
\]

The typed E3 \((x,y)\) occurrence contains precisely this marked PB3
coordinate.  Thus its two images generate the full order-\(27\) group; the
cross-checked Heisenberg source census independently replays the same marked
order and commutator.  Since every coordinate of \(D_3\) is a quotient of
this same source group, the displayed coordinate projection and the
diagonal source map give

\[
 \boxed{D_3\cong\mathcal H_2(3),\qquad |D_3|=27.}
\tag{1.7}
\]

Consequently

\[
 \phi_9(H_0)\leq L_9:=\ker(D_9\to D_3).
\tag{1.8}
\]

### Lemma 1.1 (THE EXPONENT-NINE RELATIVE LAYER HAS RANK AT MOST THREE)

The group \(L_9\) is elementary abelian and

\[
 \boxed{\dim_kL_9\leq3.}
\tag{1.9}
\]

Conjugation on \(L_9\) factors through \(D_3\), and hence through
\(\Delta_0\).

#### Proof

V208 Theorem 4.1 makes \(D_9\) a quotient of the free two-generator
class-two exponent-nine group

\[
 \mathcal H_2(9)=
 \langle x,y\mid\gamma_3, w^9\ (w\in F)\rangle,
\tag{1.10}
\]

whose normal form has the three coordinates

\[
 x^a y^b[x,y]^c,\qquad a,b,c\in\mathbf Z/9\mathbf Z.
\tag{1.11}
\]

Equation (1.7) says that the composite

\[
 \mathcal H_2(9)\twoheadrightarrow D_9\twoheadrightarrow D_3
\tag{1.12}
\]

has exactly the canonical exponent-three kernel: no additional nonzero
class in \(\mathcal H_2(3)\) is killed by all coordinates.  The kernel of
coordinate reduction modulo three consists of triples
\((3a,3b,3c)\).  It is elementary abelian: products of two degree-one
coordinates divisible by three contribute a central cross term divisible by
nine, and hence zero.  Its rank is three.  Therefore \(L_9\) is a quotient
of this canonical kernel, proving (1.9).

Since \(L_9\) is abelian, conjugation on it by two lifts of one element of
\(D_3\) agrees: the two lifts differ by an element of \(L_9\), whose inner
action on \(L_9\) is trivial.  Thus the action factors through \(D_3\), and
the roof factorization gives the last assertion. \(\square\)

The first-successor kernel \(K\) is already a \(k[\Delta_0]\)-module by
v188.  Lemma 1.1 makes \(L_9\) another such module.  We therefore use the
diagonal roof action on

\[
 V=K\oplus L_9.
\tag{1.13}
\]

## 2. Joint relator defects recover the exact screen image of \(H_1\)

Let

\[
 \mathcal R_{6441}=\{r_1,\ldots,r_{6441}\}
\tag{2.1}
\]

be the complete v190 normal-relator roster for \(H_0\).  For every relator
put

\[
 b_j=\psi_1(r_j)\in K,
 \qquad
 \ell_j=\phi_9(r_j)\in L_9,
 \qquad
 v_j=(b_j,\ell_j)\in V.
\tag{2.2}
\]

Define the finite-dimensional roof submodule

\[
 W=k[\Delta_0]\langle v_1,\ldots,v_{6441}\rangle\leq V.
\tag{2.3}
\]

### Theorem 2.1 (JOINT DEFECT-KERNEL FORMULA)

Let

\[
 L_1:=\phi_9(H_1)\leq L_9.
\tag{2.4}
\]

Then

\[
 \boxed{
 L_1=\{\ell\in L_9:(0,\ell)\in W\}
     =\operatorname{pr}_{L_9}\bigl(W\cap(0\oplus L_9)\bigr).}
\tag{2.5}
\]

In particular \(L_1\cong(C_3)^s\) for some \(0\leq s\leq3\).

#### Proof

Restrict the product homomorphism

\[
 (\psi_1,\phi_9):H_0\longrightarrow K\oplus L_9.
\tag{2.6}
\]

Both target factors are elementary abelian, so (2.6) is an additive map.
The group \(H_0\) is normally generated in \(F\) by the relators (2.1).
For \(u\in F\), conjugating \(r_j\) sends (2.2) to

\[
 \psi_0(u)\cdot(b_j,\ell_j),
\tag{2.7}
\]

under the diagonal action from Section 1.  Products and inverse powers of
conjugated relators become sums and scalar multiples in \(k\).  Therefore

\[
 \operatorname{im}\bigl(H_0\xrightarrow{(\psi_1,\phi_9)}V\bigr)=W.
\tag{2.8}

An element \(h\in H_0\) lies in \(H_1\) exactly when its first coordinate
\(\psi_1(h)\in K\) is zero.  Taking the second coordinates of precisely
those points in (2.8) gives (2.5).  Lemma 1.1 gives \(s\leq3\). \(\square\)

### Corollary 2.2 (RANK-BOUNDED WORD-BEARING COMPILATION)

Start an echelon in the ambient \(t+\dim L_9\) dimensional space \(V\) with
the 6,441 rows (2.2), retaining each source relator as ancestry.  Close every
rank-raising row under the two roof generators and their inverses.  Queue
exhaustion returns exactly \(W\) after at most

\[
 t+\dim L_9\leq t+3
\tag{2.9}
\]

rank increases.  Intersecting the terminal echelon with (0\oplus L_9)
returns a basis

\[
 \lambda_1,\ldots,\lambda_s
\tag{2.10}
\]

of \(L_1\), together with literal source words

\[
 h_i\in H_1,\qquad \phi_9(h_i)=\lambda_i.
\tag{2.11}
\]

The proof is the same exhausted-module-closure argument as v188 Proposition
3.1, applied to the joint rows.  Linear ancestry corresponds to products,
powers, and conjugates of the literal roof relators, so a zero \(K\)
coordinate in (2.10) is replayed as the exact successor identity in (2.11).

## 3. The complete projected direction ideal

Let

\[
 \Phi_9:k[F]\longrightarrow k[D_9]
\tag{3.1}
\]

be induced by \(\phi_9\), and retain the first-successor direction ideal

\[
 J_1=\ker\bigl(k[F]\longrightarrow k[\Delta_1]\bigr).
\tag{3.2}
\]

Normality of \(H_1\) makes \(L_1=\phi_9(H_1)\) normal in \(D_9\).  Put

\[
 I(L_1)=
 \ker\bigl(k[D_9]\longrightarrow k[D_9/L_1]\bigr).
\tag{3.3}
\]

### Theorem 3.1 (PROJECTED SUCCESSOR IDEAL WITHOUT SCHREIER ENUMERATION)

\[
 \boxed{\Phi_9(J_1)=I(L_1).}
\tag{3.4}
\]

If (2.10) is a basis of \(L_1\), then

\[
 \boxed{
 I(L_1)=
 \sum_{i=1}^{s}k[D_9](\lambda_i-1).}
\tag{3.5}
\]

#### Proof

Every element of \(J_1\) is a finite sum of differences \(U-V\) with
\(\psi_1(U)=\psi_1(V)\), by v195 Lemma 2.1.  Then
\(V^{-1}U\in H_1\), so its image under \(\Phi_9\) belongs to the ideal
generated by \(L_1-1\).  This proves

\[
 \Phi_9(J_1)\subseteq I(L_1).
\tag{3.6}
\]

Conversely, choose \(d\in D_9\) and \(\lambda\in L_1\).  There are source
words \(A\in F\) and \(h\in H_1\) with
\(\phi_9(A)=d\) and \(\phi_9(h)=\lambda\).  The element

\[
 A(h-1)\in J_1
\tag{3.7}
\]

maps to \(d(\lambda-1)\).  Such elements span the group-algebra kernel in
(3.3), giving the reverse inclusion.  Finally, because the
\(\lambda_i\) generate the elementary abelian group \(L_1\), the identities

\[
 ab-1=(a-1)+a(b-1),\qquad
 a^{-1}-1=-a^{-1}(a-1)
\tag{3.8}
\]

give the left-ideal formula (3.5). \(\square\)

This theorem is the finite-screen replacement for the rank
(|\Delta_1|+1) Schreier roster in v196.  It computes exactly the part of
that enormous ideal which can be seen by the chosen quotient; no projected
repair direction is discarded.

## 4. At most 2,187 complete repair columns

After projection to the v208 endpoint groups, the v198 endpoint-change map
depends on a source group-algebra element only through its joint value in
\(k[D_9]\).  Thus there is a linear map

\[
 \Lambda_9:k[D_9]\longrightarrow
 k[\mathcal N_3(9)]_{H1}\oplus
 k[\mathcal N_3(9)]_{H2}\oplus
 k[\mathcal N_4(9)]_P
\tag{4.1}
\]

with

\[
 \bar{\mathcal E}_d=\Lambda_9\Phi_9.
\tag{4.2}
\]

Combining Theorem 3.1 with v198 Corollary 4.1 gives the complete projected
repair space

\[
 \boxed{
 \bar{\mathcal E}_d(J_1)=
 \operatorname{span}_k
 \{\Lambda_9(d(\lambda_i-1)):
       d\in D_9,\ 1\leq i\leq s\}.}
\tag{4.3}
\]

V208 gives \(|D_9|\leq729\), while Theorem 2.1 gives \(s\leq3\).
Therefore (4.3) contains at most

\[
 \boxed{729s\leq2{,}187}
\tag{4.4}

authenticated columns.  Sparse echelon insertion may stop storing dependent
columns, but the producer must still traverse every pair in the complete
roster (4.3) before returning a projected NO.

### Corollary 4.1 (ZERO RELATIVE IMAGE IS AN IMMEDIATE GATE)

If \(L_1=0\), then

\[
 \bar{\mathcal E}_d(J_1)=0.
\tag{4.5}
\]

Hence a nonzero projected endpoint of the named \(M_0\) proves that no
finite-support representative of the same first multiplier can pass the
exact endpoint gate.  A zero projected endpoint still requires exact PB
replay; quotient zero is not exact zero.

## 5. Production interface

The exact finite-screen order is now:

1. export the authenticated 6,441 roof relators and the eleven-occurrence
   exponent-nine maps;
2. apply v208 Theorem 3.1 and discard the screen if it factors through the
   roof;
3. after v188 constructs \(K\), evaluate each relator once as the joint pair
   \((b_j,\ell_j)\) and exhaust the rank closure in \(K\oplus L_9\);
4. extract the word-bearing basis (2.10)--(2.11) of \(L_1\);
5. after v191 supplies the actual \(M_0\), project its three endpoints;
6. enumerate all at most 2,187 columns in (4.3), returning either a complete
   quotient dual or a coefficient seed; and
7. interpret a dual by v200 Theorem 5.1, while replaying every YES seed with
   exact Artin/Garside PB normal forms.

The receipt binds every relator pair, roof action, rank ancestry, zero
successor replay for each \(h_i\), the full \(D_9\) BFS, every column, and the
final dual pairing.  An independent checker uses a different pivot order and
reconstructs the class-two coordinate multiplication rather than importing
producer helpers.

```text
EXPONENT-NINE RELATIVE LAYER L9:                  RANK AT MOST 3
IMAGE L1 = phi9(H1) FROM JOINT RELATOR DEFECTS:   PAPER-PROOF
WORD-BEARING L1 BASIS BY RANK CLOSURE:             PAPER-PROOF
PROJECTED J1 IMAGE = KERNEL k[D9] -> k[D9/L1]:    PAPER-PROOF
COMPLETE PROJECTED REPAIR ROSTER:                  AT MOST 2,187 COLUMNS
FULL DELTA1 SCHREIER ENUMERATION FOR THIS SCREEN:   REMOVED
ACTUAL RELATOR PAIRS / L1 / M0 / ENDPOINT / DUAL: NOT COMPUTED
EXACT SAME-mu1 REPAIR / RELATIVE PRO-3 LIFT:       NOT CONSTRUCTED
FAKE / IHARA WITNESS:                              NOT DECLARED
```

`R07_EXPONENT9_RELATIVE_KERNEL_COMPRESSION_V209_PAPER_GRADE`
