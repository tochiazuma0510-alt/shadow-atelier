# R07 relative-projective trace selector v179

Author: Sol / 2026-08-28

Status: paper theorem and finite certificate contract.  This note weakens
v178's literal regular-orbit decomposition to relative projectivity, gives a
dimension/coinvariant certificate for that condition over each finite
3-kernel, and isolates a completed-free special case in which one dual is
available on all rungs without any averaging.  Relative projectivity of the
actual R07 residual quotient has not been established.  No compatible lift,
fake certificate, or Ihara witness is declared.

## 1. The trace equation as a norm equation

Let \(k=\mathbf F_3\), let

\[
 \pi:G'\twoheadrightarrow G,
 \qquad K=\ker\pi
\tag{1.1}
\]

with \(K\) a finite 3-group, and let

\[
 r:W'\twoheadrightarrow W
\tag{1.2}
\]

be a compatible module reduction.  Thus \(W\) is inflated from \(G\) and
\(r(aw')=r(w')\) for \(a\in K\).  On the scalar dual put

\[
 (N_K\lambda)(w')=
 \sum_{a\in K}\lambda(a^{-1}w').
\tag{1.3}
\]

The image is contained in \(((W')^*)^K\).  For
\(\varphi\in W^*\), the change-of-level law of v178 is precisely

\[
 \boxed{N_K\varphi'=\varphi\circ r.}
\tag{1.4}
\]

For an arbitrary \(kK\)-module, (1.4) need not have a solution.  Its exact
obstruction is the Tate class

\[
 [\varphi\circ r]\in
 \widehat H^0(K,(W')^*)
 =((W')^*)^K/N_K((W')^*).
\tag{1.5}
\]

This explains both phenomena in v178: pullback followed by trace is zero
when \(K\ne1\), while a non-invariant Dirac functional can still have the
required nonzero trace.

## 2. Relative projectivity removes the trace obstruction

### Theorem 2.1 (PROJECTIVE TRACE SURJECTIVITY)

If \(W'\), restricted to \(kK\), is projective, then

\[
 N_K:(W')^*\longrightarrow ((W')^*)^K
\tag{2.1}
\]

is surjective.  Consequently every scalar boundary dual
\(\varphi\in W^*\) has a successor dual \(\varphi'\in(W')^*\) satisfying
the exact v178 trace equation (1.4).

#### Proof

The group algebra \(kK\) of a finite 3-group in characteristic three is a
finite-dimensional local algebra, with augmentation ideal as its Jacobson
radical.  Every finite projective \(kK\)-module is therefore free.  Choose a
left \(kK\)-basis \(b_1,\ldots,b_s\) of \(W'\).

For \(\psi\in((W')^*)^K\), define the based Dirac functional
\(S_b\psi\in(W')^*\) on the \(k\)-basis
\(\{ab_i:a\in K,1\leq i\leq s\}\) by

\[
 (S_b\psi)(ab_i)=
 \begin{cases}
   \psi(b_i),&a=1,\\
   0,&a\ne1.
 \end{cases}
\tag{2.2}
\]

For \(a_0\in K\), exactly one term in

\[
 (N_KS_b\psi)(a_0b_i)
 =\sum_{a\in K}(S_b\psi)(a^{-1}a_0b_i)
\tag{2.3}
\]

is nonzero, namely \(a=a_0\).  Its value is \(\psi(b_i)\), which equals
\(\psi(a_0b_i)\) by \(K\)-invariance.  Hence

\[
 N_KS_b\psi=\psi.
\tag{2.4}
\]

Taking \(\psi=\varphi\circ r\), which is \(K\)-invariant by (1.2), proves
the final assertion. \(\square\)

The selector (2.2) is not Haar averaging and contains no division by
\(|K|\).  V178 Proposition 4.1 is the special case in which the chosen free
summand has already been displayed as literal regular fibres.

## 3. A complete finite freeness certificate

The projectivity hypothesis of Theorem 2.1 is decidable by exact finite
linear algebra.

### Proposition 3.1 (DIMENSION--COINVARIANT FREE CRITERION)

Let \(M\) be a finite-dimensional \(kK\)-module and let

\[
 J_KM=\langle (a-1)m:a\in K,\ m\in M\rangle_k.
\tag{3.1}
\]

Put \(d=\dim_k(M/J_KM)\).  Then

\[
 \boxed{
 M\text{ is free over }kK
 \quad\Longleftrightarrow\quad
 \dim_kM=|K|d.}
\tag{3.2}
\]

#### Proof

If \(M\cong(kK)^d\), both sides of (3.2) are immediate.  Conversely,
lift a \(k\)-basis of \(M/J_KM\) to \(m_1,\ldots,m_d\in M\).  Nakayama's
lemma gives a surjection

\[
 (kK)^d\twoheadrightarrow M,
 \qquad e_i\longmapsto m_i.
\tag{3.3}
\]

Under the dimension equality in (3.2), source and target both have
dimension \(|K|d\), so (3.3) is an isomorphism. \(\square\)

Thus a certificate consists of the exact \(K\)-action matrices, a basis of
the span (3.1), the quotient dimension \(d\), and the full-rank orbit matrix

\[
 \{a m_i:a\in K,1\leq i\leq d\}.
\tag{3.4}
\]

With an ordered input basis, choose the lexicographically first lifts whose
orbit matrix has full rank.  Formula (2.2) then becomes a deterministic
selector rather than an unspecified choice.

For a boundary quotient

\[
 W'=C_1/\operatorname{im}D_2,
\tag{3.5}
\]

the test must use the complete \(K\)-stable presentation-boundary image.
Testing a truncated column roster can certify neither the quotient dimension
nor freeness.  Task194's complete shard/merge theorem is therefore directly
relevant: it can construct the full boundary correlation in parallel, after
which (3.1)--(3.4) are a comparatively small serial calculation.

## 4. An all-rung recursive selector

Retain the tower of v178,

\[
 \Delta_{n+1}\twoheadrightarrow\Delta_n,
 \qquad K_n=\ker(\Delta_{n+1}\to\Delta_n),
 \qquad W_{n+1}\twoheadrightarrow W_n.
\tag{4.1}
\]

### Theorem 4.1 (RELATIVE-PROJECTIVE TRACE TOWER)

Assume that \(W_{n+1}|_{kK_n}\) is free at every rung and fix one based
Dirac selector \(S_n\) from (2.2) at every rung.  Starting with any scalar
boundary dual \(\varphi_0\in W_0^*\), define

\[
 \boxed{
 \varphi_{n+1}=S_n(\varphi_n\circ r_n).}
\tag{4.2}
\]

Then \((\varphi_n)\) is trace-compatible at every adjacent pair.  Its
covariantizations form one continuous

\[
 \ell:\varprojlim W_n\longrightarrow
 \mathbf F_3[[\Delta_\infty]]
\tag{4.3}
\]

as in v178 Theorem 3.1.

#### Proof

Theorem 2.1 gives

\[
 N_{K_n}\varphi_{n+1}=\varphi_n\circ r_n
\tag{4.4}
\]

for every \(n\).  This is exactly the necessary and sufficient trace law
of v178 Theorem 2.1.  V178 Theorem 3.1 then covariantizes and takes the
inverse limit. \(\square\)

This closes the choice problem once a compatible free-basis rule is proved:
there is no later dual search.  A positive freeness test at one successor is
only a canary; the all-rung conclusion requires either (3.2) at every rung or
one structural completed-free theorem.

## 5. The completed-free special case

There is a stronger form in which the entire family is written without
recursion.  Suppose the completed actual residual subsystem has a compatible
topological basis

\[
 W\cong\Xi^s,
 \qquad
 \Xi=\mathbf F_3[[\Delta_\infty]],
\tag{5.1}
\]

whose reductions give \(W_n\cong k[\Delta_n]^s\).  Coordinate projection

\[
 \ell\!\left(\sum_i\lambda_i b_i\right)=\lambda_1
\tag{5.2}
\]

is already one continuous \(\Xi\)-linear functional.  Its finite scalar
duals are the identity coefficients of (5.2), and their trace compatibility
follows directly because the identity coefficient after
\(k[\Delta_{n+1}]\to k[\Delta_n]\) is the sum of the coefficients over the
kernel fibre.

In particular, if the closed actual subsystem is rank-one free with basis
the original target \(d\), then

\[
 \ell(d)=1.
\tag{5.3}
\]

Every corrected residual \(e\) in that subsystem has the unique form

\[
 e=\mu d,
 \qquad \mu=\ell(e).
\tag{5.4}
\]

If \(e\) vanishes at the roof, then \(\mu\in\mathfrak j\), and v174 gives
the compatible correction

\[
 -\sum_{r\ge0}\mu^r a.
\tag{5.5}
\]

Thus completed rank-one freeness simultaneously supplies cyclic membership,
injectivity, the unit pivot, and the all-rung trace dual.  It is a strong
structural target, not something implied by a one-rung dimension match.

## 6. Exact R07 successor contract

After a positive task186 word and task193 successor residual are available,
the smallest additional experiment is:

1. form the genuine diagonal kernel \(K_0\) and its action on the complete
   successor boundary quotient;
2. compute \(J_{K_0}W_1\), \(d=\dim W_1/J_{K_0}W_1\), and test
   \(\dim W_1=|K_0|d\);
3. on success, retain the lexicographic free orbit basis (3.4) and construct
   the Dirac successor of a roof dual;
4. replay boundary annihilation, the full trace equation, and the
   covariantized values on the actual \(d_1,e_1\);
5. test injectivity on the registered actual subsystem or direct membership
   of \(e_1\) in the cyclic module of \(d_1\).

A failed equality in item 2 is a finite nonfreeness theorem for that exact
module, not a failure of all trace selectors: (1.5) must then be tested for
the particular roof dual.  A resource stop is `UNKNOWN`.

## 7. Fixed frontier

```text
TRACE OBSTRUCTION AS TATE H^0 CLASS:              PAPER_PROOF
PROJECTIVE/FREE SUCCESSOR TRACE SURJECTIVITY:      PAPER_PROOF
DIMENSION--COINVARIANT FREE CERTIFICATE:           PAPER_PROOF
ALL-RUNG RELATIVE-PROJECTIVE TRACE RECURSION:       PAPER_PROOF
COMPLETED-FREE CLOSED TRACE FUNCTIONAL:             PAPER_PROOF
R07 FIRST SUCCESSOR RELATIVE FREENESS:              NOT COMPUTED
R07 ALL-RUNG COMPLETED FREE PRESENTATION:            NOT PROVED
TASK186 EXACT FIRST CORRECTION:                      GHA IN PROGRESS
TASK193 ACTUAL SUCCESSOR / TRACE CANARY:             GHA SELFTEST
COMPATIBLE COFINAL LIFT / FAKE / IHARA:              NOT DECLARED
```

`R07_RELATIVE_PROJECTIVE_TRACE_SELECTOR_V179_PAPER_GRADE`
