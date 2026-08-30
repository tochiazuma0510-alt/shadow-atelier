# R07 class-orbit section and relative lift v396

Author: Sol / 2026-08-30

Status: paper theorem refining v395 with a class-specific right inverse.  It
shows that one word-bearing leading preimage can generate the required
relative corrections when the actual defect orbit has no extra source
relations and is saturated under the adjacent reduction.  The construction
retains the occurrence instruction tree and gives literal commutator words.
The actual R07 orbit-relation, saturation, and full-action square gates have
not yet been computed.  No compatible lift, fake, or Ihara witness is
declared.  verified=false.

## 1. The smaller source which is actually needed

Fix one elementary-abelian relative edge and put

\[
  K=\ker(\Gamma_1\to\Gamma_0),\qquad
  R=\mathbf F_3[K],\qquad
  \mathfrak a=\ker(R\to\mathbf F_3).
\tag{1.1}
\]

Let \(D\) be the fine legal correction source, let \(L\) be the fine actual
residual target, and let

\[
 B:D\longrightarrow L
\tag{1.2}
\]

be the occurrence-path operator of v395.  In this note \(B\) is assumed to
be \(R\)-linear.  This is not inferred from endpoint values: it is exactly
the full-action aggregation and same-owner gate of v392.

Choose a finite actual class roster

\[
 \ell_1,\ldots,\ell_q\in L
\tag{1.3}
\]

and literal instruction-tree corrections

\[
 d_1,\ldots,d_q\in D,\qquad B(d_a)=\ell_a.
\tag{1.4}
\]

Define the two orbit maps

\[
 \phi_L:R^q\to L,\quad (r_a)\mapsto\sum_a r_a\ell_a,
 \qquad
 \phi_D:R^q\to D,\quad (r_a)\mapsto\sum_a r_ad_a.
\tag{1.5}
\]

Then \(B\phi_D=\phi_L\).  Write

\[
 L_\chi=\operatorname {im}\phi_L,\qquad
 D_\chi=\operatorname {im}\phi_D.
\tag{1.6}
\]

For the R07 class-specific route, \(L_\chi\) is only the full-actor orbit
needed by the recursively produced defect of

\[
 \chi_{07}=[x,y][y,z]^{-1}.
\tag{1.7}
\]

It need not be the whole ambient relative kernel.

## 2. Exact orbit-section criterion

### Theorem 2.1 (WORD-BEARING ORBIT SECTION)

The rule

\[
 s_\chi\bigl(\phi_L(v)\bigr)=\phi_D(v)
\tag{2.1}
\]

defines an \(R\)-linear map \(s_\chi:L_\chi\to D_\chi\) if and only if

\[
 \boxed{\ker\phi_L\subseteq\ker\phi_D.}
\tag{2.2}
\]

Whenever (2.2) holds,

\[
 \boxed{Bs_\chi=1_{L_\chi}.}
\tag{2.3}
\]

In fact \(B\phi_D=\phi_L\) always gives the reverse inclusion
\(\ker\phi_D\subseteq\ker\phi_L\), so (2.2) is equivalently equality of the
two orbit-relation modules.

#### Proof

The value in (2.1) is independent of the chosen coefficient vector exactly
when \(\phi_L(v)=0\) implies \(\phi_D(v)=0\), which is (2.2).  The formula is
then visibly \(R\)-linear, and

\[
 Bs_\chi(\phi_L(v))=B\phi_D(v)=\phi_L(v).
\]

The final assertion follows by applying \(B\) to an element of
\(\ker\phi_D\). \(\square\)

### Corollary 2.2 (FREE ORBIT SHORTCUT)

If the actual orbit map \(\phi_L:R^q\to L_\chi\) is injective, then (2.2)
is automatic.  In particular, if the orbit of the \(q\) named residuals is
a free \(R\)-module with those residuals as basis, the \(q\) word-bearing
preimages in (1.4) already give the complete right inverse (2.1).  No
classification of the complementary return-even target is needed.

At a finite edge, freeness of this displayed orbit is decided by one exact
rank test: the \(|K|q\) columns \(k\ell_a\) must have rank \(|K|q\).  When
the orbit is not free, (2.2) is the weaker and exact test: every linear
relation among the target orbit columns must replay as the same relation
among the instruction-tree source columns.

## 3. Relative-kernel right inverse on the actual class

Let the fine-to-coarse reductions be \(r_D:D\to D_0\) and
\(r_L:L\to L_0\).  Assume the \(K\)-action disappears after reduction, so

\[
 \mathfrak aD\subseteq\ker r_D,\qquad
 \mathfrak aL\subseteq\ker r_L.
\tag{3.1}
\]

The target-orbit saturation gate is

\[
 \boxed{L_\chi\cap\ker r_L=\mathfrak aL_\chi.}
\tag{3.2}
\]

This equality is automatic for a free \(R\)-orbit reduced by coinvariants.
For a nonfree physical image it is load-bearing and must be checked; it is
the class-orbit version of the relative base-change defect in v365.

### Theorem 3.1 (CLASS-SPECIFIC RELATIVE RIGHT INVERSE)

Assume (2.2) and (3.2).  Then

\[
 h_\chi:=s_\chi\big|_{\mathfrak aL_\chi}:
 L_\chi\cap\ker r_L\longrightarrow\mathfrak aD_\chi
\tag{3.3}
\]

is a well-defined \(R\)-linear right inverse of \(B\).  Consequently

\[
 \boxed{
 B(\mathfrak aD_\chi)=\mathfrak aL_\chi
 =L_\chi\cap\ker r_L.}
\tag{3.4}
\]

In particular, if the v395 fine defect satisfies

\[
 \beta_1\in L_\chi,\qquad r_L(\beta_1)=0,
\tag{3.5}
\]

then the explicit corrected lift is

\[
 \boxed{c_1=\widetilde c_1+h_\chi(\beta_1).}
\tag{3.6}
\]

#### Proof

By (3.2), write \(\beta=\phi_L(v)\) with
\(v\in\mathfrak aR^q\).  Theorem 2.1 makes
\(h_\chi(\beta)=\phi_D(v)\) independent of the choice of \(v\).  Since
\(\phi_D\) is \(R\)-linear, this element belongs to
\(\mathfrak aD_\chi\subseteq\ker r_D\), and

\[
 Bh_\chi(\beta)=B\phi_D(v)=\phi_L(v)=\beta.
\]

This proves (3.3)--(3.4).  Formula (3.6) is v395 Theorem 3.1. \(\square\)

Thus v395's universal equality
\(B(\ker r_D)=\ker r_L\) is stronger than necessary.  For the actual class,
one needs only (2.2), (3.2), and membership (3.5) in its much smaller orbit.

## 4. Literal word returned by the section

Retain a word-bearing basis \(k_1,\ldots,k_t\) of \(K\).  By v388,
\(\mathfrak a\) is generated as a left ideal by \(k_j-1\).  Hence a solved
coefficient vector in (3.3) has the form

\[
 v=\sum_{a,j,g}\epsilon_{a,j,g}\,g(k_j-1)e_a,
 \qquad \epsilon_{a,j,g}\in\{0,1,2\}.
\tag{4.1}
\]

The additive source term \(g(k_j-1)d_a\) is represented by the literal
instruction tree

\[
 \boxed{\operatorname {Conj}
   \bigl(g,\operatorname {Comm}(k_j,d_a)\bigr).}
\tag{4.2}
\]

Indeed, in the active elementary-abelian correction layer,
\([k_j,d_a]\) represents \((k_j-1)[d_a]\), as in v369 Lemma 2.1.
Coefficient \(2\) is represented by inversion, and summation is represented
by the registered ordered product.  Every occurrence evaluates (4.2) with
its own actor path; no common occurrence action and no exchange of
\((p-1)\delta(a)\) with \((a-1)\delta(p)\) is used.

Therefore a finite Gaussian solve for \(v\) returns not merely a vector but
an explicit word-bearing correction ancestry.  This is the promised use of
the relative-dihedral construction: commutators materialize the relative
ideal, while the class-orbit section selects the return-even/full-path
coefficient.

## 5. One inverse-limit section instead of unrelated finite choices

Let the preceding data form compatible inverse systems.  Put

\[
 R_\infty=\varprojlim R_n,\qquad
 \mathfrak a_\infty=\varprojlim\mathfrak a_n.
\tag{5.1}
\]

Assume there are compatible class generators and instruction words giving
continuous maps

\[
 \phi_{L,\infty}:R_\infty^q\to L_{\chi,\infty},\qquad
 \phi_{D,\infty}:R_\infty^q\to D_{\chi,\infty},
\tag{5.2}
\]

with \(B_\infty\phi_{D,\infty}=\phi_{L,\infty}\).  Suppose
\(\phi_{L,\infty}\) is a topological isomorphism onto its image.  Define

\[
 \boxed{s_{\chi,\infty}
 =\phi_{D,\infty}\phi_{L,\infty}^{-1}.}
\tag{5.3}
\]

Then (5.3) is one continuous word-bearing right inverse, its reduction is
the finite section of Theorem 2.1 at every level, and

\[
 h_{\chi,\infty}
 =s_{\chi,\infty}|_{\mathfrak a_\infty L_{\chi,\infty}}
\tag{5.4}
\]

simultaneously supplies all relative corrections.  Substituting (5.4) in
v395 equation (4.1) constructs the coherent sequence without choosing
unrelated \(c_n\)'s.

The topological-isomorphism hypothesis may be certified by compatible
finite free-orbit receipts.  If an orbit is nonfree, the correct replacement
is compatible equality of the relation modules in Theorem 2.1 together
with compatible saturated coefficient lifts; finite nonemptiness without
compatibility is not enough.

## 6. Exact v220 interface

This theorem changes the remaining A9 gate from a full-kernel problem to a
class-orbit problem:

~~~text
A0: literal leading preimage(s) d_a:                    STILL REQUIRED
v392: full-action/same-owner R-linearity:               STILL OPEN PHYSICAL GATE
A4: word-bearing K basis and orbit action:              RUNNING
actual defect beta in the named class orbit:            NOT COMPUTED
target orbit freeness or relation equality (2.2):       NOT COMPUTED
class-orbit saturation (3.2):                           NOT COMPUTED
literal relative right inverse once those pass:         PAPER CONSTRUCTION HERE
one inverse-limit section under compatible orbit data:  PAPER CONSTRUCTION HERE
FAKE / IHARA WITNESS:                                   NOT CONSTRUCTED
~~~

The important reduction is that no full classification of
\(\ker r_L\), and no new correction search at every refinement, is necessary
for \(\chi_{07}\).  A free actual orbit is the best case: one A0 word and the
word-bearing \(K\)-action immediately give the relative selector (4.2).

R07_CLASS_ORBIT_SECTION_RELATIVE_LIFT_V396_PAPER_GRADE
