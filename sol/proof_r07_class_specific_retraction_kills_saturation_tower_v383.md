# R07 class-specific relative retraction kills the saturation tower v383

Author: Sol / 2026-08-30

Status: paper theorem after v82, v96, v333 and v382.  It identifies one
precise inverse-limit object which would turn the relative-dihedral
generalization into a uniform nonlinear lift mechanism: a continuous
module retraction from the actual Fox-error envelope onto the reachable
correction module.  Such a retraction kills every ambient/intrinsic
saturation class at once.  The abstract theorem is unconditional.  The
actual R07 retraction, its return-even component, and the initial
path-bearing membership have not been constructed.  No fake certificate or
Ihara witness is declared.  \(\mathtt{verified=false}\).

## 1. Retractions and intrinsic powers

Let \(\Lambda\) be a compact Hausdorff topological ring, let
\(J\triangleleft\Lambda\) be a closed two-sided ideal, and form module
powers by closed spans of finite products.  Let

\[
 \iota:L\hookrightarrow E
\tag{1.1}
\]

be an inclusion of compact Hausdorff left \(\Lambda\)-modules with \(L\)
closed in \(E\).

### Theorem 1.1 (RETRACTION KILLS ALL SATURATION CLASSES)

Suppose there is a continuous \(\Lambda\)-linear retraction

\[
 r:E\longrightarrow L,
 \qquad
 r\iota=1_L.
\tag{1.2}
\]

Then, for every \(n\geq0\),

\[
 \boxed{
 L\cap J^nE=J^nL.}
\tag{1.3}
\]

Equivalently, every natural map

\[
 L/J^nL\longrightarrow E/J^nE
\tag{1.4}
\]

is injective.

#### Proof

The inclusion \(J^nL\subseteq L\cap J^nE\) is immediate.  Conversely, let
\(x\in L\cap J^nE\).  By the definition of the closed module power, there
is a net of finite sums

\[
 x_\alpha=\sum_k a_{\alpha k}e_{\alpha k}
 \longrightarrow x,
 \qquad
 a_{\alpha k}\in J^n,\quad e_{\alpha k}\in E.
\tag{1.5}
\]

Continuity and \(\Lambda\)-linearity of \(r\) give

\[
 r(x_\alpha)
 =
 \sum_k a_{\alpha k}r(e_{\alpha k})
 \in J^nL,
 \qquad
 r(x_\alpha)\longrightarrow r(x)=x.
\tag{1.6}
\]

The submodule \(J^nL\) is closed, so \(x\in J^nL\).  This proves (1.3).
The kernel of (1.4) is
\((L\cap J^nE)/J^nL\), proving the equivalent statement. \(\square\)

### Corollary 1.2 (ERROR-ENVELOPE FORM)

Let \(\epsilon\in L\).  If an ambient calculation supplies

\[
 \epsilon\in J^nE,
\tag{1.7}
\]

then the retraction supplies the intrinsic conclusion

\[
 \boxed{\epsilon\in J^nL.}
\tag{1.8}
\]

It is unnecessary to exhibit a termwise factorization whose divisors
already lie in \(L\): apply \(r\) to any ambient factorization as in
(1.5).

The theorem needs a retraction only on an error envelope \(E\) containing
the divisors used by the calculation.  It does not require the whole broad
path module to retract.

## 2. The actual Fox-error envelope

Retain v382's enriched ring and reachable target

\[
 \widehat\Xi=\mathbf F_3[[\widehat\Delta_\infty]],
 \qquad
 \widehat J=
 \ker\left(
  \widehat\Xi\longrightarrow
  \mathbf F_3[[
   \widehat\Delta_\infty/\widehat P]]
 \right),
 \qquad
 L_{\rm reach}\subseteq L_{\rm amb}.
\tag{2.1}
\]

For one physical eleven-occurrence owner, define \(E_{\rm Fox}\) to be the
smallest closed \(\widehat\Xi\)-submodule of the retained enriched path
module which contains:

1. \(L_{\rm reach}\);
2. every supported divisor vector appearing after complete PB3/PB4
   boundary quotient in a fixed-versus-moving prefix difference;
3. every divisor vector appearing in the ordered-materialization
   cross-term expansion; and
4. the reductions of these vectors in every matched finite coordinate.

Only vectors actually used by the two hexagons and printed pentagon on
\(\widehat w_0\widehat{\mathscr Q}_C\) are included.  Thus

\[
 L_{\rm reach}\subseteq E_{\rm Fox}\subseteq L_{\rm amb}
\tag{2.2}
\]

is class-specific.  It is not the whole raw chain space and does not include
unregistered paths merely because they exist.

The full filtered Fox package required in v382 Section 6 has the ambient
form

\[
 \epsilon_d(w,t)
 \in
 L_{\rm reach}\cap
 \widehat J^{d+1}E_{\rm Fox}.
\tag{2.3}
\]

At \(d=0\), this includes every leading generator prefix error.  At
positive depth, it includes fixed-prefix associated-graded agreement with
\(B_C(t)\), moving-prefix gain, ordered-product gain, and filtered
boundary/localization.

### Corollary 2.1 (ONE RETRACTION CLOSES EVERY R07 SATURATION GATE)

If there is a continuous \(\widehat\Xi\)-linear map

\[
 \boxed{
 r_{\rm Fox}:E_{\rm Fox}\longrightarrow L_{\rm reach},
 \qquad
 r_{\rm Fox}|_{L_{\rm reach}}=1,}
\tag{2.4}
\]

then every ambient congruence (2.3) is intrinsic:

\[
 \boxed{
 \epsilon_d(w,t)\in
 \widehat J^{d+1}L_{\rm reach}.}
\tag{2.5}
\]

In particular, all leading and positive-depth saturation classes of v382
vanish simultaneously.

#### Proof

Apply Corollary 1.2 with
\((\Lambda,J,L,E)=
(\widehat\Xi,\widehat J,L_{\rm reach},E_{\rm Fox})\)
and \(n=d+1\). \(\square\)

This is stronger than checking an unrelated saturation class at every
finite rung.  One inverse-limit identity (2.4) makes all of those checks
formal consequences.

## 3. Conditional completion theorem

Let

\[
 q_{\rm loc}^{\rm reach}:W_C\longrightarrow
 L_{\rm reach}/\widehat JL_{\rm reach}
\tag{3.1}
\]

be v382's directly replayed task395 map, and put

\[
 \overline\beta_{\rm path}
 =
 [\Phi_{\rm lane}(\widehat w_0)]
 \in L_{\rm reach}/\widehat JL_{\rm reach}.
\tag{3.2}
\]

### Theorem 3.1 (CLASS-SPECIFIC RETRACTION LIFT)

Assume:

1. the common physical Magnus/action/boundary ABI authenticates v369,
   v372, v382's reachable task395 square, and the ambient filtered Fox
   congruences (2.3);
2. \(L_{\rm reach}\) has the intrinsic finite-coordinate separation of
   v377;
3. the retraction (2.4) exists; and
4. the one full path-bearing membership holds:

   \[
    \boxed{
    -\overline\beta_{\rm path}
    \in q_{\rm loc}^{\rm reach}(W_C).}
   \tag{3.3}
   \]

Then:

1. \(B_C:P_C\to L_{\rm reach}\) is onto and strict at every
   \(\widehat J\)-depth;
2. v369 materializes every depthwise instruction selected from that
   strict map; and
3. the section-free recursion of v382 Theorem 6.2 constructs a compatible
   zero-residual correction on the registered relative pro-\(3\) lane.

No ambient comparison isomorphism and no ambient full-target span are
required.

#### Proof

At depth zero, Corollary 2.1 turns every ambient prefix congruence into the
intrinsic generator law of v382 Corollary 2.2.  The direct task395 square
and (3.3) therefore satisfy v382 Theorem 5.1, which gives onto and
strictness at every depth.  At all positive depths, Corollary 2.1 supplies
the intrinsic congruence used in v382 Theorem 6.2.  That theorem gives the
stated correction product. \(\square\)

This is a conditional construction theorem, not an assertion that (2.4) or
(3.3) has already been produced.  Mixed-prime, perfect-core, settlement and
the final witness typing remain outside the registered pro-\(3\) conclusion.

## 4. What the relative-dihedral generalization must construct

The pure relative-dihedral antisymmetrizer acts on the return-odd part of
the correction complex.  It does not remove the return-even field-outer
survivor identified in v82 and v333.  The correct all-refinement object is
therefore not a stagewise scalar correction.  It is a natural projection
onto the actual reachable module.

At each matched finite coordinate \(i\), it is enough to construct

\[
 r_i:E_{{\rm Fox},i}\longrightarrow L_{{\rm reach},i},
 \qquad
 r_i\iota_i=1,
\tag{4.1}
\]

with the base-change identities

\[
 \boxed{
 q_{ji}r_j=r_iq_{ji}
 \quad(j\geq i).}
\tag{4.2}
\]

The inverse limit of (4.1)--(4.2) is (2.4).  Equivalently, one may construct
compatible idempotents

\[
 e_i^2=e_i,
 \qquad
 \operatorname {im}e_i=L_{{\rm reach},i}.
\tag{4.3}
\]

The expected decomposition has the form

\[
 \boxed{
 r_i=
 r_i^{\rm dih,-}
 +
 r_i^{\rm class,+},}
\tag{4.4}
\]

where the first term is supplied on the return-odd summand by the
relative-dihedral contraction and the second term is a legal
field-outer/full-\(P_0\), actual-class homotopy on the surviving even
summand.  Equation (4.4) is a specification, not a proved construction:
the two terms must have complementary typed domains, preserve the common
source and literal A.18 boundaries, and satisfy (4.1)--(4.2).

V333 explains the finite algebra behind the second term.  A structural
right inverse needs enough legal even columns to separate the entire even
cokernel.  A witness-first actual-class construction may use fewer columns,
but to obtain the uniform retraction (4.1) those columns must cover the
whole even part of the class-specific error envelope, not merely one
endpoint vector.

Thus the infinite relative-dihedral program is now:

1. serialize \(E_{{\rm Fox},i}\) with path-bearing occurrence ancestry;
2. use the existing antisymmetrizer on its odd part;
3. compute the even cokernel of the inclusion of
   \(L_{{\rm reach},i}\), and supply legal common-word columns for it;
4. replay (4.1) and the refinement square (4.2); and
5. test the single path-bearing class (3.3).

A success at one finite level does not imply (4.2).  A natural finite
formula does.

## 5. Exact frontier

~~~text
RETRACTION => ALL INTRINSIC SATURATION EQUALITIES:    PAPER PROOF
CLASS-SPECIFIC FOX ERROR ENVELOPE:                    PRECISE DEFINITION / ABI BINDING OPEN
ODD RELATIVE-DIHEDRAL COMPONENT:                      PRIOR CONDITIONAL INPUT
EVEN FIELD-OUTER COMPONENT:                           NOT CONSTRUCTED
FINITE RETRACTION IDENTITIES r_i iota_i = 1:          NOT COMPUTED
COFINAL NATURALITY q_ji r_j = r_i q_ji:               OPEN
ONE FULL PATH-BEARING MEMBERSHIP:                     NOT COMPUTED
REGISTERED RELATIVE PRO-3 LIFT:                       CONDITIONAL THEOREM / ACTUAL OPEN
MIXED-PRIME / PERFECT-CORE / SETTLEMENT:              OPEN
FAKE / IHARA WITNESS:                                 NOT DECLARED
~~~

\(\mathtt{R07\_CLASS\_SPECIFIC\_RETRACTION\_KILLS\_SATURATION\_TOWER\_V383\_AUDIT\_CANDIDATE}\)
