# R07 A0: exact marked-word repair for the first-rung character projectors (v447)

Author: Sol / 2026-09-03

Status: exact incorporation of the local repair accepted by independent
Task553.  This note supersedes only the source-word justification following
v446 (2.1) and certificate gate 7.4.  All other statements are those of v446
as qualified by Task553.  It proves no grade membership. `verified=false`.

## 1. The gap in the original citation

V442 and Task548 prove that

\[
 s_X=X^9,\qquad s_Y=t_1t_2^{-1}t_3Y
\]

are pure-sign complement elements in the `G9` factor.  That calculation does
not by itself bind the `PSL(2,8)` endpoint of the same free words.  Therefore
it does not by itself produce the full-quotient operators
\(L_{(1_P,a)}\) required in v446 (2.2).

No assertion that the displayed `s_Y` word has a nonidentity PSL endpoint is
made.  The point is only that its cited certificate does not establish the
needed endpoint.

## 2. Exact pure-Q1 source words

Use the pure-\(A\) representatives independently replayed in Task549.  With
letter encoding

```text
1 = x,  -1 = x^-1,  2 = y,  -2 = y^-1,
```

the four words are

```text
a=(0,0): []
a=(0,1): [-2,-2,-2,-2,-2,-2,-2,-2,-2]
a=(1,0): [-2,-2,1,1,2,1,2,1,1]
a=(1,1): [-2,-2,-2,-1,-2,-1,-1,-1,-2,-1]
```

Their exact endpoints in the registered order-2016 quotient are

\[
 (1_P,a)\in Q_1=P\times A.                            \tag{2.1}
\]

They are words in the four legal source actors
\(x,x^{-1},y,y^{-1}\), and Task549's complete enumeration also binds that
these marked actors generate all of \(Q_1\).

## 3. An upstairs kernel coordinate is harmless on the associated grade

Let the value in \(Q_2\) of the word representing \((1_P,a)\) be

\[
 d_a=\sigma(1_P,a)n(v_a),                             \tag{3.1}
\]

where no vanishing assertion about \(v_a\in V\) is required.  For a row
\([p,b]f\) with \(f\) homogeneous of degree \(d\), v443's exact left-action
formula gives

\[
 L_{d_a}([p,b]f)
 =[p,a+b]E(S(b)v_a)f
 \equiv[p,a+b]f\pmod {I^{d+1}},                       \tag{3.2}
\]

because every nonconstant term of \(E(S(b)v_a)-1\) raises augmentation
degree.  Thus the legal actor word induces exactly

\[
 T_a=L_{(1_P,a)}                                      \tag{3.3}
\]

on the associated grade.

This is one correlated action on all six occurrence tags and both Fox
components.  In tag \(j\), its quotient endpoint is
\((1_P,A_ja)\); any crossed kernel term again has constant term one and
vanishes from the associated-grade action.  It is not a tagwise ambient
projection.

## 4. Legal Fourier projectors and exact decomposition

For \(\lambda\in\widehat A\), set

\[
 e_\lambda=\sum_{a\in A}\lambda(a)T_a.               \tag{4.1}
\]

Since \(|A|=4=1\) in \(\mathbf F_3\), this is the normalized character
idempotent.  Character orthogonality gives

\[
 e_\lambda e_\mu=\delta_{\lambda\mu}e_\lambda,
 \qquad \sum_\lambda e_\lambda=1.                    \tag{4.2}
\]

Every \(T_a\), hence every \(e_\lambda\), belongs to the algebra generated
by legal source words.  If \(D_d\) is the complete v444 seed/transition
defect set and

\[
 H_d=\mathbf F_3\langle Q_1\rangle D_d,
\]

then legal actor stability and (4.2) prove

\[
 \boxed{H_d=\bigoplus_{\lambda\in\widehat A}e_\lambda H_d.} \tag{4.3}
\]

This authorizes the four character blocks of v446.  It authorizes no
individual monomial projection; all \(h_d\) monomial coordinates remain
coupled inside each character block.

## 5. Replacement certificate gate

Replace v446 certificate gate 7.4 by:

> Bind each exact pure-\(Q_1\) source word above, its endpoint
> \((1_P,a)\) in the order-2016 quotient, its value (3.1) in the first-rung
> affine coordinates, and its single correlated action on all six tags and
> both Fox components.  Replay (3.2) and the four projector identities
> (4.2).

A producer may instead use a zero-kernel complement word only after binding
both its `PSL` and `G9` endpoints.  A `G9`-only purity check is insufficient.

With this replacement, the exact implementation contract remains:

```text
SOURCE: four character blocks x 18,144 coordinates at degree one
MONOMIALS: three coordinates retained as one coupled tuple
PHYSICAL: one joint width-24,192 fibre, unless every actual-row hyperedge is sealed
FIRST-GRADE MEMBERSHIP: not computed
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: not declared
verified=false
```
