# R07 trace-compatible dual covariantization v178

Author: Sol / 2026-08-28

Status: paper theorem and successor-search contract.  It converts scalar
boundary duals into diagonal-equivariant functionals and identifies the exact
compatibility law across relative pro-3 refinements.  It also proves an
explicit Dirac selector when each new actual fibre is a regular kernel orbit.
Neither that regular-fibre hypothesis nor a compatible R07 dual has yet been
established.  No lift, fake certificate, or Ihara witness is declared.

## 1. Finite covariantization

Let (k=\mathbf F_3), let (G) be finite, and let (W) be a left
(k[G])-module.  For a scalar functional
(\varphi\in W^*=\operatorname{Hom}_k(W,k)), define

\[
 \boxed{
 \mathcal C_G(\varphi)(w)
   =\sum_{g\in G}\varphi(g^{-1}w),g\in k[G].}
\tag{1.1}
\]

### Proposition 1.1 (FINITE COVARIANTIZATION)

The map

\[
 \mathcal C_G:W^*\longrightarrow
 \operatorname{Hom}_{k[G]}(W,k[G])
\tag{1.2}
\]

is a (k)-linear isomorphism.  Its inverse takes the coefficient of the
identity group element.

#### Proof

For (h\in G), substitute (g=hr) in (1.1):

\[
 \mathcal C_G(\varphi)(hw)
 =\sum_r\varphi(r^{-1}w),hr
 =h\mathcal C_G(\varphi)(w).
\tag{1.3}
\]

Thus the map is (k[G])-linear.  Its identity coefficient is
(\varphi(w)), so it is injective.  Conversely, if
(L:W\to k[G]) is (k[G])-linear and
(\varphi(w)=[1]L(w)), then

\[
 [g]L(w)=[1]g^{-1}L(w)=[1]L(g^{-1}w)
 =\varphi(g^{-1}w),
\tag{1.4}
\]

which reconstructs (1.1).  Hence it is surjective. \(\square\)

If (W=C_1/\operatorname{im}D_2), a raw scalar row
(\widehat\varphi:C_1\to k) supplies such a functional exactly when

\[
 \widehat\varphi(D_2q)=0\qquad(q\in C_2).
\tag{1.5}
\]

Thus the complete scalar duals already used by the boundary-correlation
calculations are precisely the finite input from which an equivariant
functional can be built.  A raw coordinate which does not satisfy (1.5)
still does not descend.

## 2. The change-of-level law is trace, not pullback

Let

\[
 \pi:G'\twoheadrightarrow G,qquad K=\ker\pi,
\tag{2.1}
\]

and let (r:W'\twoheadrightarrow W) be a compatible module reduction.
Write (\pi_*:k[G']\to k[G]) for the group-algebra map.  Given
(\varphi'\in(W')^*) and (\varphi\in W^*), put
(L'=\mathcal C_{G'}(\varphi')) and
(L=\mathcal C_G(\varphi)).

### Theorem 2.1 (TRACE COMPATIBILITY)

The square

\[
 \pi_*L'(w')=L(rw')\qquad(w'\in W')
\tag{2.2}
\]

commutes if and only if

\[
 \boxed{
 \varphi(rw')=
 \sum_{a\in K}\varphi'(a^{-1}w')
 \qquad(w'\in W').}
\tag{2.3}
\]

#### Proof

The coefficient of (h\in G) on the left of (2.2) is

\[
 \sum_{g\in\pi^{-1}(h)}\varphi'(g^{-1}w').
\tag{2.4}
\]

Choose (g_0\in\pi^{-1}(h)) and write (g=g_0a).  Applying (2.3) to
(g_0^{-1}w') gives

\[
 \sum_{a\in K}\varphi'(a^{-1}g_0^{-1}w')
 =\varphi(h^{-1}rw'),
\tag{2.5}
\]

the (h)-coefficient of the right side.  This proves sufficiency.  Taking
the identity coefficient in (2.2) gives (2.3), proving necessity.
\(\square\)

Equation (2.3) is the load-bearing compatibility condition.  Ordinary
pullback is usually wrong in characteristic three.  Indeed, if
(K\ne1) is a 3-group and
(\varphi'=\varphi\circ r), then its right side is

\[
 |K|\varphi(rw')=0.
\tag{2.6}
\]

Consequently normalized Haar averaging cannot repair this: division by
(|K|) is unavailable in (\mathbf F_3).  Measure language is usable only
for a distribution satisfying the trace law (2.3), not for an invariant
probability average.

## 3. Inverse-limit functional

Return to the diagonal context tower of v173.  Write

\[
 \Delta_{n+1}\twoheadrightarrow\Delta_n,qquad
 K_n=\ker(\Delta_{n+1}\to\Delta_n),qquad
 \Lambda_n=k[\Delta_n],
\tag{3.1}
\]

and let (W_n) be compatible finite actual residual subsystems.  Suppose
there are scalar boundary duals (\varphi_n\in W_n^*) which satisfy
(2.3) at every adjacent pair.

### Theorem 3.1 (TRACE-DUAL INVERSE LIMIT)

The finite maps

\[
 \ell_n=\mathcal C_{\Delta_n}(\varphi_n):
 W_n\longrightarrow\Lambda_n
\tag{3.2}
\]

form one continuous (\Xi)-linear map

\[
 \boxed{
 \ell:\varprojlim W_n\longrightarrow
 \Xi=\mathbf F_3[[\Delta_\infty]].}
\tag{3.3}
\]

Conversely, every continuous (\Xi)-linear map to (\Xi) gives the unique
trace-compatible scalar family obtained by taking identity coefficients.

#### Proof

Proposition 1.1 gives equivariance at each level, and Theorem 2.1 gives
compatibility with every reduction.  The universal property of the inverse
limit gives (3.3), whose continuity follows because all finite coordinates
are continuous.  The converse follows levelwise from the inverse in
Proposition 1.1 and necessity in Theorem 2.1. \(\square\)

This theorem sharpens the functional gate in v177: a good dual at one finite
stage is a discovery candidate, but the missing all-rung datum is its
trace-compatible lift, not a repetition of unrelated dual choices.

## 4. A closed Dirac lift on a regular kernel fibre

The trace equation has an explicit non-averaging solution under a concrete
fibre condition.  Suppose at one adjacent step there is a (k)-linear
section (s:W\to W') and a (K)-stable decomposition

\[
 W'=\left(\bigoplus_{a\in K}a,s(W)\right)\oplus U,
\tag{4.1}
\]

where the displayed copies are linearly independent, (r(a,s(w))=w),
and (r(U)=0).  Thus the first summand is a literal regular (K)-fibre
over (W).

### Proposition 4.1 (REGULAR-FIBRE DIRAC SELECTOR)

For (\varphi\in W^*), define (S\varphi\in(W')^*) by

\[
 \boxed{
 (S\varphi)(a,s(w))=
 \begin{cases}
 \varphi(w),&a=1,\\
 0,&a\ne1,
 \end{cases}
 \qquad (S\varphi)(U)=0.}
\tag{4.2}
\]

Then (S\varphi) satisfies the trace equation (2.3).

#### Proof

For (w'=a_0s(w)), the sum in (2.3) contains exactly one nonzero term,
namely (a=a_0), and that term is (\varphi(w)).  Every translate of a
vector in (U) stays in (U), so its sum is zero, as is its reduction.
Linearity proves the assertion for all (w'\). \(\square\)

If decompositions (4.1) are chosen compatibly at every rung, iterating
(4.2) gives a closed, fully explicit trace-compatible dual family.  This is
the precise field-outer analogue which could accompany the existing
return-odd dihedral selector.  It is a theorem with a checkable hypothesis,
not a claim that R07 fibres are already regular.

## 5. Unit pivot and the pointed correction

Let (d=(d_n)) and (e=(e_n)) lie in a closed actual subsystem (W), and
let (\ell) be supplied by Theorem 3.1.  Put

\[
 \delta=\ell(d).
\tag{5.1}
\]

If the roof value (\delta_0\in k[\Delta_0]) has a literal two-sided
inverse, then v177 Lemma 2.1 makes (\delta) a unit.  If (e) vanishes at
the roof, compatibility gives

\[
 \ell(e)\in\ker(\Xi\to k[\Delta_0])=\mathfrak j.
\tag{5.2}
\]

If (\ell) is injective on a closed subsystem containing both (d) and
(e), v177 gives

\[
 \boxed{
 \mu=\ell(e)\delta^{-1}\in\mathfrak j,
 \qquad e=\mu d.}
\tag{5.3}

V174 then gives the single compatible correction

\[
 \boxed{
 c_\infty=-\sum_{r\ge0}\mu^r a.}
\tag{5.4}

For the weaker cyclic version one may instead prove
(e\in\overline{\Xi d}); unit (\delta) then makes (\ell) injective on
that cyclic subsystem automatically.  The trace selector does not by itself
prove either injectivity or cyclic membership.

## 6. Exact finite search contract after task193

At the genuine first successor, retain the scalar dual as a literal row, not
only its covariantized group-algebra value.  A successor run must test:

1. annihilation of every complete PB3/PB4 boundary translate;
2. the exact trace equation from the roof dual to the successor dual;
3. direct reconstruction of (\ell_1(d_1)) and (\ell_1(e_1)) by (1.1);
4. a literal roof inverse for (\ell_0(d_0));
5. injectivity on the registered finite actual orbit, or direct cyclic
   membership of (e_1); and
6. whether the actual label fibre has the regular decomposition (4.1).

A positive first trace lift is still only a canary for the universal
regular-fibre statement.  A complete failure in the registered finite dual
universe is a finite obstruction; a resource stop is UNKNOWN.  Task194's
sharded full correlation may accelerate item 1, but shard averaging must not
replace the trace sum in item 2.

## 7. Fixed frontier

```text
FINITE DUAL COVARIANTIZATION:                    PAPER_PROOF
ADJACENT TRACE COMPATIBILITY LAW:                PAPER_PROOF
HAAR/PULLBACK SHORTCUT IN CHARACTERISTIC 3:      REFUTED
TRACE-DUAL INVERSE-LIMIT FUNCTIONAL:             PAPER_PROOF
REGULAR-FIBRE DIRAC SELECTOR:                    PAPER_PROOF / HYPOTHESIS OPEN
R07 TRACE-COMPATIBLE SCALAR DUAL FAMILY:          NOT CONSTRUCTED
R07 REGULAR ACTUAL FIBRES AT ALL RUNGS:           NOT PROVED
TASK193 FIRST SUCCESSOR TRACE CANARY:             NOT COMPUTED
UNIT / INJECTIVITY OR CYCLIC-MEMBERSHIP GATES:    OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA:            NOT DECLARED
```

`R07_TRACE_COMPATIBLE_DUAL_COVARIANTIZATION_V178_PAPER_GRADE`
