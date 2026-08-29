# R07 class-specific relative retraction kills the saturation tower v384

Author: Sol / 2026-08-30

Status: repaired paper theorem after the independent audit of v383.  The
finite-coordinate modules and their inverse limits are now typed before any
retraction or Newton choice is made.  The abstract retraction theorem is
unconditional.  The actual R07 divisor ABI, retraction, return-even component,
ambient Fox estimate, and initial path-bearing membership remain open.  No fake
certificate or Ihara witness is declared.  \(\mathtt{verified=false}\).

## 1. Retractions and intrinsic powers

Let \(\Lambda\) be a compact Hausdorff topological ring and let
\(J\triangleleft\Lambda\) be a closed two-sided ideal.  Put \(J^0M=M\).  For
\(n>0\), define \(J^nM\) to be the closure of the finite sums

\[
 \sum_k j_{k1}\cdots j_{kn}m_k,
 \qquad j_{k\ell}\in J,quad m_k\in M.
\tag{1.1}
\]

Let \(\iota:L\hookrightarrow E\) be an inclusion of compact Hausdorff left
\(\Lambda\)-modules, with \(L\) closed in \(E\).

### Theorem 1.1 (RETRACTION KILLS ALL SATURATION CLASSES)

Suppose that there is a continuous \(\Lambda\)-linear retraction

\[
 r:E\longrightarrow L,
 \qquad r\iota=1_L.
\tag{1.2}
\]

Then, for every \(n\geq0\),

\[
 \boxed{L\cap J^nE=J^nL.}
\tag{1.3}
\]

Equivalently, the natural map \(L/J^nL\to E/J^nE\) is injective.

#### Proof

The assertion for \(n=0\) is immediate.  The inclusion
\(J^nL\subseteq L\cap J^nE\) is also immediate.  Conversely, take
\(x\in L\cap J^nE\).  By (1.1), there is a net

\[
 x_\alpha=\sum_k
 j_{\alpha k1}\cdots j_{\alpha kn}e_{\alpha k}
 \longrightarrow x.
\tag{1.4}
\]

Continuity and \(\Lambda\)-linearity give

\[
 r(x_\alpha)=\sum_k
 j_{\alpha k1}\cdots j_{\alpha kn}r(e_{\alpha k})
 \in J^nL,
 \qquad r(x_\alpha)\longrightarrow r(x)=x.
\tag{1.5}
\]

The module power \(J^nL\) is closed by definition, so \(x\in J^nL\).
Finally, the kernel of \(L/J^nL\to E/J^nE\) is
\((L\cap J^nE)/J^nL\). \(\square\)

### Corollary 1.2 (ERROR-ENVELOPE FORM)

If \(\epsilon\in L\cap J^nE\), then

\[
 \boxed{\epsilon\in J^nL.}
\tag{1.6}
\]

Thus the divisors in an ambient factorization need only lie in a retracting
error envelope \(E\), not already in \(L\).

## 2. The class-specific Fox envelope is fixed before the recursion

Retain v382's inverse-limit ring and reachable target

\[
 \widehat\Xi=\mathbf F_3[[\widehat\Delta_\infty]],
 \qquad
 \widehat J=\ker\bigl(\widehat\Xi\to
 \mathbf F_3[[\widehat\Delta_\infty/\widehat P]]\bigr),
 \qquad
 L_{\rm reach}\subseteq L_{\rm amb}.
\tag{2.1}
\]

Fix one physical eleven-occurrence ABI: the same marked action, two hexagons,
printed pentagon, PB3/PB4 boundary quotient, localization, and registered
materialization owner at every matched finite coordinate.  This fixation is
made before selecting any Newton correction.

Let \(\mathcal D_{\rm Fox}\subseteq L_{\rm amb}\) be the family of compatible
inverse-limit divisor vectors appearing in the following formulas, quantified
over **all** legal inputs of the fixed ABI:

1. every fixed-versus-moving prefix difference for every leading generator;
2. every ordered-product cross-term divisor; and
3. every corresponding divisor for every depth \(d\geq0\), every registered
   residual input \(w\), and every legal materialized instruction
   \(t\in\widehat J^dP_C\).

Compatibility means that each named divisor is a single element of the
inverse-limit path module, not an unrelated collection of finite vectors.  If
the physical formulas do not produce such compatible elements, the ABI
hypothesis fails.  Define

\[
 \boxed{
 E_{\rm Fox}:=
 \overline{\widehat\Xi\cdot
 (L_{\rm reach}\cup\mathcal D_{\rm Fox})}
 \subseteq L_{\rm amb}.}
\tag{2.2}
\]

This definition is independent of the later Newton choices: it contains the
divisors for every legal triple \((d,w,t)\), not only those selected by one
run.  It is class-specific and need not equal the broad raw-chain module.

Let \(I\) be the directed set of matched finite coordinates.  Write

\[
 \pi_i^E:L_{\rm amb}\to L_{{\rm amb},i},
 \qquad
 E_i:=\pi_i^E(E_{\rm Fox}),
 \qquad
 L_i:=\pi_i^E(L_{\rm reach}),
\tag{2.3}
\]

and let

\[
 q^E_{ji}:E_j\to E_i,
 \qquad
 q^L_{ji}:L_j\to L_i
 \quad(j\geq i)
\tag{2.4}
\]

be the restricted transition maps.  The finite reductions of every divisor
are now automatically elements of \(E_i\); they are not inserted into the
global module as objects of the wrong type.

### Lemma 2.1 (CLOSED SUBMODULE RECONSTRUCTION)

For a closed submodule \(M\) of a compact inverse limit of finite discrete
modules, the canonical map

\[
 M\longrightarrow\varprojlim_i\pi_i(M)
\tag{2.5}
\]

is a homeomorphic module isomorphism.  Consequently,

\[
 E_{\rm Fox}\simeq\varprojlim_iE_i,
 \qquad
 L_{\rm reach}\simeq\varprojlim_iL_i.
\tag{2.6}
\]

#### Proof

Injectivity follows because the ambient inverse-limit coordinates separate
points.  For a compatible family \((m_i)_i\in\varprojlim_i\pi_i(M)\), define

\[
 C_i=\{m\in M:\pi_i(m)=m_i\}.
\tag{2.7}
\]

Every \(C_i\) is nonempty and closed.  Directedness and compatibility imply
that any finite collection of the \(C_i\) contains a common finer-coordinate
member, hence has nonempty intersection.  Compactness of \(M\) gives
\(m\in\bigcap_iC_i\), proving surjectivity.  A continuous bijection from the
compact space \(M\) to the Hausdorff inverse limit is a homeomorphism. \(\square\)

## 3. One retraction closes every saturation gate

The full filtered Fox statement required by v382 is the explicitly quantified
ambient assertion

\[
 \epsilon_d(w,t)\in
 L_{\rm reach}\cap\widehat J^{d+1}E_{\rm Fox}
\tag{3.1}
\]

for every leading generator at \(d=0\), and for every legal recursion triple
\((d,w,t)\) at positive depth.  It includes fixed-prefix associated-graded
agreement with \(B_C(t)\), moving-prefix gain, ordered-product gain, and
filtered boundary/localization.  A retraction does not prove (3.1); it turns
its ambient depth into intrinsic depth.

### Corollary 3.1 (ONE RETRACTION CLOSES EVERY R07 SATURATION GATE)

If there is a continuous \(\widehat\Xi\)-linear map

\[
 \boxed{
 r_{\rm Fox}:E_{\rm Fox}\longrightarrow L_{\rm reach},
 \qquad r_{\rm Fox}|_{L_{\rm reach}}=1,}
\tag{3.2}
\]

then every instance of (3.1) satisfies

\[
 \boxed{
 \epsilon_d(w,t)\in
 \widehat J^{d+1}L_{\rm reach}.}
\tag{3.3}
\]

Hence every leading and positive-depth saturation class appearing in v382
vanishes.  This is Theorem 1.1 with
\((\Lambda,J,L,E)=(\widehat\Xi,\widehat J,L_{\rm reach},E_{\rm Fox})\).

## 4. Conditional completion of the registered pro-3 lift

Let

\[
 q_{\rm loc}^{\rm reach}:W_C\longrightarrow
 L_{\rm reach}/\widehat JL_{\rm reach},
 \qquad
 \overline\beta_{\rm path}=
 [\Phi_{\rm lane}(\widehat w_0)].
\tag{4.1}
\]

### Theorem 4.1 (CLASS-SPECIFIC RETRACTION LIFT)

Assume:

1. the fixed physical ABI authenticates v369, v372, the direct reachable
   task395 square of v382, and every ambient estimate (3.1);
2. \(L_{\rm reach}\) has v377's intrinsic finite-coordinate separation;
3. the retraction (3.2) exists; and
4. the full path-bearing leading membership holds:

   \[
    \boxed{-\overline\beta_{\rm path}
    \in q_{\rm loc}^{\rm reach}(W_C).}
   \tag{4.2}
   \]

Then \(B_C:P_C\to L_{\rm reach}\) is onto and strict at every
\(\widehat J\)-depth, v369 materializes every requested depthwise value, and
the section-free recursion of v382 constructs a compatible zero-residual
correction on the registered relative pro-\(3\) lane.

#### Proof

At depth zero, Corollary 3.1 converts all ambient leading prefix errors into
the intrinsic generator law used by v382.  The direct task395 square and the
full-path condition (4.2) therefore satisfy v382 Theorem 5.1, giving leading
onto.  V377 upgrades it to

\[
 B_C(P_C)=L_{\rm reach},
 \qquad
 B_C(\widehat J^nP_C)=\widehat J^nL_{\rm reach}
 \quad(n\geq0).
\tag{4.3}
\]

For every positive-depth step, Corollary 3.1 supplies the intrinsic error
estimate required by v382 Theorem 6.2.  That theorem's section-free Newton
recursion then gives the stated inverse-limit correction. \(\square\)

This theorem is conditional.  It asserts neither (3.1), (3.2), nor (4.2), and
does not settle mixed-prime, perfect-core, settlement, fake, or Ihara typing.

## 5. Finite retractions and the relative-dihedral target

For every coordinate \(i\), suppose there is an \(\widehat\Xi_i\)-linear map

\[
 r_i:E_i\longrightarrow L_i,
 \qquad r_i\iota_i=1_{L_i},
\tag{5.1}
\]

and, for every \(j\geq i\), suppose the typed naturality square holds:

\[
 \boxed{q^L_{ji}r_j=r_iq^E_{ji}.}
\tag{5.2}
\]

Then \((r_i)_i\) induces

\[
 \varprojlim_iE_i\longrightarrow\varprojlim_iL_i.
\tag{5.3}
\]

Under the canonical identifications (2.6), this is precisely (3.2).  Equally,
one may construct compatible \(\widehat\Xi_i\)-linear idempotents

\[
 e_i:=\iota_ir_i\in\operatorname {End}_{\widehat\Xi_i}(E_i),
 \qquad e_i^2=e_i,
 \qquad\operatorname {im}e_i=\iota_i(L_i),
\tag{5.4}
\]

with the corresponding typed transition identity.

The relative-dihedral decomposition remains a construction specification, not
a theorem already supplied by the shelf.  If the equivariance, image, and
typing hypotheses of v333 hold on the return-odd submodule of this exact
\(E_i\), its conditional odd right inverse may provide that component.  V82
only exhibits an abstract return-even finite candidate; it does not bind an
actual A.18/Fox occurrence.  The required complementary field-outer/full-
\(P_0\) map must therefore still be constructed and bound to the same
\(E_i\), source, and boundaries.

The actual program is:

1. bind the compatible global divisor family \(\mathcal D_{\rm Fox}\) and
   authenticate (3.1);
2. serialize the induced finite modules \(E_i,L_i\) with occurrence ancestry;
3. instantiate the conditional odd component only where v333's hypotheses
   hold;
4. construct the actual legal even component;
5. replay (5.1)--(5.2); and
6. test the one full path-bearing class (4.2).

A success at one finite level does not imply (5.2).  A natural finite formula
does.

## 6. Exact frontier

~~~text
RETRACTION => ALL INTRINSIC SATURATION EQUALITIES:    PAPER PROOF
GLOBAL COMPATIBLE DIVISOR FAMILY / AMBIENT FOX DEPTH: ACTUAL ABI OPEN
CLOSED-SUBMODULE INVERSE-LIMIT IDENTIFICATION:        PAPER PROOF
ODD RELATIVE-DIHEDRAL COMPONENT:                      PRIOR CONDITIONAL INPUT
EVEN FIELD-OUTER COMPONENT:                           NOT CONSTRUCTED
FINITE RETRACTIONS r_i AND TYPED NATURALITY:          NOT COMPUTED
ONE FULL PATH-BEARING MEMBERSHIP:                     NOT COMPUTED
REGISTERED RELATIVE PRO-3 LIFT:                       CONDITIONAL THEOREM
MIXED-PRIME / PERFECT-CORE / SETTLEMENT:              OPEN
FAKE / IHARA WITNESS:                                 NOT DECLARED
~~~

\(\mathtt{R07\_CLASS\_SPECIFIC\_RETRACTION\_KILLS\_SATURATION\_TOWER\_V384\_AUDIT\_CANDIDATE}\)
