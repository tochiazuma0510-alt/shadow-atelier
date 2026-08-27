# R07 exponent-nine non-roof theorem from the roof extension v211

Author: Sol / 2026-08-28

Status: paper theorem strengthening v210.  The exponent-nine joint endpoint
group \(D_9\) has order 729, whereas every 3-group quotient of the frozen
roof has order at most 243.  Hence \(D_9\) cannot factor through the roof.
Moreover its quotient by the unique roof-defect subgroup
\(\langle[x,y]^3\rangle\) is canonically the 243-element task157ee
kernel \(\Gamma\).  Thus this screen's exact roof defect is the nonzero class
of one explicit non-split central \(C_3\)-extension; it is not an unspecified member
of a large abstract module.  This theorem does not decide whether that class
dies at the first successor, and it does not construct an endpoint repair,
compatible cofinal lift, fake certificate, or Ihara witness.
verified=false.

## 1. The coarse roof has no nontrivial 3-group quotient

Let the frozen marked roof be denoted by \(\Delta_0\).  V149, v154, and
v190 identify the task157ee extension with this roof and give an exact
sequence

\[
 1\longrightarrow \Gamma\longrightarrow \Delta_0
 \stackrel{\pi}{\longrightarrow}Q_0\longrightarrow1,
 \qquad |\Gamma|=3^5=243,
\tag{1.1}
\]

where

\[
 Q_0\cong G_9\times PSL(2,8),
 \qquad |Q_0|=1{,}469{,}664.
\tag{1.2}
\]

The frozen \(G_9\) structure has

\[
 [G_9,G_9]\cong C_9^3,
 \qquad G_9^{\mathrm{ab}}\cong C_2^2,
\tag{1.3}
\]

and \(PSL(2,8)\) is perfect.  Consequently

\[
 \boxed{Q_0^{\mathrm{ab}}\cong C_2^2.}
\tag{1.4}
\]

### Lemma 1.1 (NO COARSE 3-QUOTIENT)

Every homomorphism from \(Q_0\) to a finite 3-group is trivial.

#### Proof

Let \(I\) be a homomorphic image of \(Q_0\) which is a finite 3-group.  Its
abelianization \(I^{\mathrm{ab}}\) is a quotient of (1.4), hence is both a
2-group and a 3-group.  Thus \(I^{\mathrm{ab}}=1\).  Every nontrivial finite
\(p\)-group has a quotient of order \(p\), for example by quotienting by a
maximal subgroup.  A nontrivial \(I\) would therefore have nontrivial
abelianization, a contradiction.  Hence \(I=1\). \(\square\)

### Theorem 1.2 (ROOF 3-QUOTIENT BOUND)

If \(P\) is a finite 3-group quotient of \(\Delta_0\), then

\[
 \boxed{P\ \text{ is an image of }\Gamma,\qquad |P|\leq243.}
\tag{1.5}
\]

#### Proof

Let \(\theta:\Delta_0\twoheadrightarrow P\) and put
\(\Gamma_P=\theta(\Gamma)\).  Since \(\Gamma\triangleleft\Delta_0\),
the quotient \(P/\Gamma_P\) is a 3-group quotient of
\(\Delta_0/\Gamma=Q_0\).  Lemma 1.1 gives \(P/\Gamma_P=1\).
Therefore \(P=\Gamma_P\), and (1.5) follows from
\(|\Gamma|=243\). \(\square\)

The bound uses the full 243-element extension kernel.  It does not make the
false inference that the roof has no 3-primary quotient: v156 shows that the
extension kernel contributes the roof's \(C_9^2\) marked abelian quotient.

## 2. The order-729 endpoint is forced non-roof

Let

\[
 \phi_9:F(x,y)\twoheadrightarrow D_9
\tag{2.1}
\]

be the eleven-occurrence class-two exponent-nine endpoint map of v208--v210.
V210 Lemma 1.1 gives

\[
 D_9\cong\mathcal H_2(9)
 =\langle x,y,c\mid c=[x,y], c\ {\rm central},
 x^9=y^9=c^9=1\rangle,
 \qquad |D_9|=9^3=729.
\tag{2.2}
\]

Write

\[
 \psi_0:F(x,y)\twoheadrightarrow\Delta_0,
 \qquad H_0=\ker\psi_0.
\tag{2.3}
\]

### Theorem 2.1 (FORCED NON-ROOF)

The endpoint map (2.1) does not factor through the roof:

\[
 \boxed{H_0\nsubseteq\ker\phi_9.}
\tag{2.4}
\]

Equivalently, there is no marked surjection
\(\Delta_0\twoheadrightarrow D_9\) induced by (2.1).

#### Proof

If \(H_0\subseteq\ker\phi_9\), the universal property of
\(F/H_0=\Delta_0\) would induce a surjection
\(\Delta_0\twoheadrightarrow D_9\).  It is surjective because
\(\phi_9\) is.  But \(D_9\) is a 3-group of order \(729>243\),
contradicting Theorem 1.2. \(\square\)

This replaces v210's undecided all-zero/nonzero roof test.  Non-roofness is
now a paper consequence of the frozen roof order structure; the 6,441-scalar
replay is still required as a literal certificate and implementation check,
but not to discover whether the screen is non-roof.

## 3. Exact identification of the roof-visible quotient

Put

\[
 C=\langle c^3\rangle\leq D_9,
 \qquad |C|=3,
 \qquad \bar D_9=D_9/C.
\tag{3.1}
\]

V210 Theorem 2.1 proves

\[
 \phi_9(H_0)\leq C.
\tag{3.2}
\]

Therefore the composite \(F\to D_9\to\bar D_9\) kills \(H_0\) and
induces a marked surjection

\[
 q_9:\Delta_0\twoheadrightarrow\bar D_9,
 \qquad |\bar D_9|=243.
\tag{3.3}
\]

### Theorem 3.1 (THE TASK157EE KERNEL IS THE ROOF-VISIBLE ENDPOINT)

Restriction of (3.3) to the extension kernel is an isomorphism:

\[
 \boxed{q_9|_{\Gamma}:\Gamma\xrightarrow{\sim}\bar D_9.}
\tag{3.4}
\]

In particular,

\[
 \boxed{
 \Gamma\cong
 \mathcal H_2(9)/\langle[x,y]^3\rangle,
 \qquad |\Gamma|=243.}
\tag{3.5}
\]

#### Proof

The quotient
\(\bar D_9/q_9(\Gamma)\) is a 3-group quotient of \(Q_0\), so
Lemma 1.1 makes it trivial.  Thus \(q_9(\Gamma)=\bar D_9\).  Both groups
have order 243, hence the restriction is an isomorphism. \(\square\)

Thus the endpoint does not introduce an unrelated 729-state screen.  Its
243-state quotient is exactly the already frozen roof kernel; the one new
direction is the central subgroup \(C\).

### Corollary 3.2 (EXACT ROOF DEFECT)

One has

\[
 \boxed{\phi_9(H_0)=C=\langle[x,y]^3\rangle\cong C_3.}
\tag{3.6}
\]

Consequently at least one of the 6,441 v190 roof relators has nonzero area
scalar \(\omega_j\) from v210.

#### Proof

Containment in \(C\) is (3.2).  If the image were trivial, (2.1) would
factor through \(\Delta_0\), contrary to Theorem 2.1.  Since \(C\) has
prime order, the image is all of \(C\).  V190 says the 6,441 relators
normally generate \(H_0\), and v210 says the area character is invariant
under conjugation.  If every \(\omega_j\) vanished, their normal closure
would have trivial image, contradicting (3.6). \(\square\)

An all-zero scalar replay is therefore an implementation or pinning stop,
not a mathematically viable roof branch.

## 4. The actual class is a non-split central extension

Using (3.4), rewrite the natural quotient of \(D_9\) as

\[
 1\longrightarrow C_3
 \longrightarrow D_9
 \longrightarrow\Gamma
 \longrightarrow1.
\tag{4.1}
\]

Let

\[
 \alpha_9\in H^2(\Gamma,C_3)
\tag{4.2}
\]

be its central extension class, with trivial \(\Gamma\)-action on
\(C_3\).

### Theorem 4.1 (NON-SPLIT ENDPOINT CLASS)

The extension (4.1) is non-split, so

\[
 \boxed{\alpha_9\neq0.}
\tag{4.3}
\]

Moreover the roof relator-area vector

\[
 (\omega_1,\ldots,\omega_{6441})
\tag{4.4}
\]

is a literal presentation representative of the pullback class
\(q_9^*\alpha_9\) on \(\Delta_0\), and this pullback class is
nonzero.

#### Proof

The derived subgroup of \(D_9=\mathcal H_2(9)\) is
\(\langle c\rangle\cong C_9\).  The derived subgroup of
\(\Gamma=D_9/C\) is \(\langle cC\rangle\cong C_3\).  If (4.1) split,
its central kernel would make
\(D_9\cong C_3\times\Gamma\), whose derived subgroup has order
three.  This contradicts \(|D_9'|=9\), proving (4.3).

Evaluate the chosen marked lifts \(x,y\in D_9\) on a complete roof
presentation.  Every roof relator lands in the central kernel by (3.2), and
its kernel coordinate is exactly the v210 area value
\(\omega_j\).  This is the standard presentation cocycle for the
pullback of (4.1), giving (4.4).

It remains to rule out that a different lift of the two marked roof
generators trivializes this cocycle.  Any other lifts have the form

\[
 x\mapsto xc^{3a},\qquad y\mapsto yc^{3b}
 \qquad(a,b\in\mathbf F_3).
\tag{4.5}
\]

For \(h\in H_0\), v156 gives both exponent sums in \(18\mathbf Z\).
The central factors in (4.5), which have order three, therefore contribute
trivially to \(h\).  Hence every choice of lifts has the same relator-area
vector.  Corollary 3.2 says that vector is nonzero, so the pullback
extension over \(\Delta_0\) cannot split.  Thus
\(q_9^*\alpha_9\neq0\). \(\square\)

This is the screen-class identification needed for the next gate: on this
endpoint the abstract field-outer/full-\(P_0\) search is replaced by one
named nonzero class \(\alpha_9\) and its literal 6,441-coordinate
representative.  It is not yet the pointed \(\mu_1\) of the R07 word.

## 5. Exact meaning of the first-successor dichotomy

Let

\[
 p_1:\Delta_1\twoheadrightarrow\Delta_0,
 \qquad K=\ker p_1,
\tag{5.1}
\]

be the first elementary-abelian successor.  Pull (4.1) back along
\(q_9p_1\).  The resulting class is

\[
 p_1^*q_9^*\alpha_9\in H^2(\Delta_1,C_3).
\tag{5.2}
\]

### Theorem 5.1 (SUCCESSOR CLASS TEST)

With \(L_1=\phi_9(\ker(F\to\Delta_1))\) as in v210, one has

\[
 \boxed{
 L_1=1
 \iff p_1^*q_9^*\alpha_9=0,
 \qquad
 L_1=C_3
 \iff p_1^*q_9^*\alpha_9\neq0.}
\tag{5.3}
\]

Under v210's relator-module notation, the first condition is equivalent to
the existence of the unique invariant functional

\[
 \lambda:K\longrightarrow\mathbf F_3,
 \qquad \lambda(b_j)=\omega_j
 \quad(1\leq j\leq6441).
\tag{5.4}
\]

#### Proof

The class in (5.2) vanishes exactly when the central extension pulled back
to \(\Delta_1\) splits, equivalently when \(q_9p_1\) lifts to \(D_9\).
Any two lifts of the marked generators again differ by elements of the
central kernel \(C_3\).  Since
\(\ker(F\to\Delta_1)\subseteq H_0\), the exponent-lattice
argument in Theorem 4.1 shows that existence of any lift is equivalent to
the prescribed map \(\phi_9\) killing that kernel.  This is exactly
\(L_1=1\).  If it does not, v210 Theorem 4.1 gives
\(L_1=C_3\).  The equivalence with (5.4) is v210 equations
(4.8)--(4.12). \(\square\)

Thus the next machine question is no longer an abstract search for an
unknown class.  It is the single transgression question: does the named
nonzero class \(q_9^*\alpha_9\) die on the actual first successor?  The
6,441 values and the invariant dual of \(K\) answer precisely that question.

## 6. Updated executable boundary

The production order is now:

1. export the exact 6,441 roof relators and replay their area values;
2. require at least one nonzero value, with all-zero as a hard stop;
3. identify the induced 243-state quotient with the task157ee
   \(\Gamma\) table as an independent marked consistency check;
4. compute the actual successor defects \(b_j\in K\);
5. test the single invariant-functional system (5.4);
6. if it has no solution, retain an explicit kernel ancestry with area one
   and traverse v210's complete 729 projected columns; and
7. compare the actual pointed endpoint only after its exact word and
   multiplier have been produced.

\[
\begin{array}{ll}
Q_0\ \text{ HAS A NONTRIVIAL 3-GROUP QUOTIENT} & \text{NO / PAPER PROOF},\\
\text{EVERY ROOF 3-QUOTIENT HAS ORDER AT MOST }243 & \text{PAPER PROOF},\\
D_9\ \text{ FACTORS THROUGH THE ROOF} & \text{NO / PAPER PROOF},\\
D_9/C_3\cong\Gamma & \text{PAPER PROOF},\\
\phi_9(H_0)=C_3 & \text{PAPER PROOF},\\
\alpha_9\in H^2(\Gamma,C_3) & \text{NAMED NONZERO NON-SPLIT CLASS},\\
\text{ACTUAL 6,441 AREA VECTOR} & \text{EXPORT/REPLAY PENDING},\\
p_1^*q_9^*\alpha_9\stackrel{?}=0 & \text{ACTUAL SUCCESSOR TEST PENDING},\\
\text{POINTED ENDPOINT / EXACT REPAIR} & \text{NOT COMPUTED},\\
\text{COFINAL LIFT / FAKE / IHARA WITNESS} & \text{NOT CONSTRUCTED}.
\end{array}
\tag{6.1}
\]

`R07_EXPONENT9_NONROOF_FORCED_BY_ROOF_EXTENSION_V211_PAPER_GRADE`
