# R07 completed-relative-ideal abelian gate v206

Author: Sol / 2026-08-28

Status: paper completion of v205 along the registered relative pro-3 tower.
The mod-2 and mod-3 abelian endpoint maps factor through the roof and extend
continuously to the completed diagonal algebra.  They kill the entire closed
relative augmentation ideal \(\mathfrak j\), not only its finite word-pair
subspace.  Therefore a nonzero fixed residual screen excludes every
completed Neumann-multiplier identity with \(\mu\in\mathfrak j\).  This is
still not a proof that every possible profinite lift must have scalar
multiplier form.  No numerical screen result, lift, fake certificate, or
Ihara witness is declared.

## 1. The finite screens factor through the roof

Retain the matched tower

\[
 \cdots\twoheadrightarrow\Delta_n
 \twoheadrightarrow\Delta_1
 \twoheadrightarrow\Delta_0
\tag{1.1}
\]

and its completed diagonal algebra

\[
 \Xi=\varprojlim_n\mathbf F_3[\Delta_n].
\tag{1.2}
\]

V156 gives

\[
 \Delta_0^{\mathrm{ab}}\cong C_{18}\times C_{18}
\tag{1.3}
\]

with the marked source generators providing the two standard coordinates.
Consequently the source exponent maps modulo \(\ell=2,3\) factor as marked
surjections

\[
 \Delta_0\twoheadrightarrow
 D_\ell\cong(C_\ell)^2.
\tag{1.4}
\]

Composing every transition in (1.1) with (1.4) gives compatible algebra
maps, hence a continuous map

\[
 \widehat\alpha_{\ell,*}:\Xi
 \longrightarrow\mathbf F_3[D_\ell].
\tag{1.5}
\]

This is the completed version of the finite source map in v202.  It is not a
new quotient inferred from a finite word ball.

## 2. The closed relative ideal is annihilated

Let

\[
 P=\ker(\Delta_\infty\to\Delta_0)
\tag{2.1}
\]

and let \(\mathfrak j\subseteq\Xi\) be v173/v174's closed relative
augmentation ideal

\[
 \mathfrak j=
 \overline{\langle p-1:p\in P\rangle}.
\tag{2.2}
\]

### Theorem 2.1 (COMPLETED RELATIVE IDEAL DIES IN BOTH SCREENS)

For \(\ell=2,3\),

\[
 \boxed{
 \widehat\alpha_{\ell,*}(\mathfrak j)=0.}
\tag{2.3}
\]

#### Proof

Every \(p\in P\) has trivial roof value, so its image under the composite
(1.4) is one.  Hence (1.5) sends every generator \(p-1\) of (2.2) to zero,
and it sends the ordinary ideal they generate to zero.  The target
\(\mathbf F_3[D_\ell]\) is finite and discrete, and (1.5) is continuous, so
it also kills the closure of that ideal. \(\square\)

Theorem 2.1 can alternatively be read levelwise: every relative kernel in
(1.1) lies over the identity of \(\Delta_0\), so its augmentation directions
vanish after (1.4).  No uniform choice of finite-support representatives is
needed.

## 3. Completed multiplier obstruction

Let \(A,Z\) be the complete \(\Xi\)-modules of v174, let

\[
 B:A\to Z
\tag{3.1}
\]

be the continuous \(\Xi\)-linear correction map, and retain the actual
vectors \(d,e\in Z\).  The Neumann multiplier identity sought in v174--v175
is

\[
 e=\mu d,
 \qquad \mu\in\mathfrak j.
\tag{3.2}
\]

The occurrencewise mod-\(\ell\) endpoint maps extend continuously to the
completed modules because they factor through the fixed finite roof quotient
(1.4).  Denote the image of \(e\) by \(\bar e_\ell\).

### Corollary 3.1 (NO COMPLETED RELATIVE MULTIPLIER ON A NONZERO SCREEN)

If

\[
 \boxed{
 \bar e_2\ne0
 \quad\text{or}\quad
 \bar e_3\ne0,}
\tag{3.3}
\]

then there is no \(\mu\in\mathfrak j\) satisfying (3.2).

#### Proof

Apply the corresponding completed endpoint projection to (3.2).  By
Theorem 2.1 and module linearity, the right side projects to

\[
 \widehat\alpha_{\ell,*}(\mu)\,\bar d_\ell=0,
\tag{3.4}
\]

contradicting (3.3). \(\square\)

The same argument applies to a completed universal boundary identity

\[
 \widetilde e-\mu\widetilde d
 =\widetilde D_2q
\tag{3.5}
\]

with a possibly completed chain \(q\): applying the endpoint map kills both
\(\mu\widetilde d\) by Theorem 2.1 and
\(\widetilde D_2q\) by \(\widetilde D_1\widetilde D_2=0\).  Thus a nonzero
\(\bar e_\ell\) excludes (3.5) without any finite-support hypothesis.

If both screens vanish, neither (3.2) nor (3.5) follows.  Exact PB or finer
nilpotent endpoint information remains necessary.

## 4. Precise relation to a lift obstruction

Corollary 3.1 is an all-rung theorem inside the scalar relative-multiplier
architecture:

\[
 \boxed{
 \text{one nonzero roof-abelian residual}
 \Longrightarrow
 \text{no finite or completed }\mu\in\mathfrak j
 \text{ solves the Neumann identity}.}
\tag{4.1}
\]

It does not prove the converse implication

\[
 \text{a compatible correction exists}
 \Longrightarrow
 \exists\mu\in\mathfrak j:\ e=\mu d.
\tag{4.2}
\]

Neither v174 nor v175 asserts (4.2): they are positive construction
theorems.  Establishing (4.2) would require a cyclicity or class-specific
generation theorem for the actual completed defect/correction module.  Until
then, (3.3) is a completed multiplier obstruction, not by itself a fake or
Ihara certificate.

This distinction is also why no measure-theoretic or compactness argument
can turn a zero screen into a lift.  Compactness can select compatible
points from nonempty finite fibres; it cannot supply the missing cyclicity or
make a nonzero quotient class vanish.

## 5. Production consequence

The early screen of v205 now has the following stronger interpretation.

1. A nonzero mod-2/mod-3 residual stops both the finite word-pair promotion
   and every completed \(\mathfrak j\)-multiplier attempt.
2. No search radius, Schreier roster, completed-series truncation, or
   all-rung enumeration is involved.
3. A zero result only opens the exact/finer gate; it is not evidence for a
   multiplier.
4. Any future claim that the screen proves a full lift obstruction must cite
   an independent proof of the missing necessity (4.2).

The certificate reuses v205's literal endpoint term ledger and additionally
binds the maps \(\Delta_n\to\Delta_0\to D_\ell\), the definition of
\(\mathfrak j\) as a closed relative ideal, and continuity of the finite
target map.  The checker rejects a purported relative generator with
nontrivial roof value or a completion map not compatible with a registered
transition.

~~~text
D2/D3 SCREENS FACTOR THROUGH Delta0:               PAPER_PROOF
CLOSED RELATIVE IDEAL j MAPS TO ZERO:               PAPER_PROOF
NONZERO SCREEN -> NO COMPLETED NEUMANN MULTIPLIER:  PAPER_PROOF
NONZERO SCREEN -> NO COMPLETED UNIVERSAL PAIR:      PAPER_PROOF
EVERY POSSIBLE LIFT HAS SCALAR MULTIPLIER FORM:     NOT PROVED
ACTUAL RESIDUAL SCREEN VALUES:                      NOT COMPUTED
RELATIVE PRO-3 LIFT / FAKE / IHARA WITNESS:         NOT DECLARED
~~~

R07_COMPLETED_RELATIVE_IDEAL_ABELIAN_GATE_V206_PAPER_GRADE
