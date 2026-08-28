# R07 Neumann--Fox group-like integrability v249

Author: Sol / 2026-08-28

Status: paper theorem characterizing exact integrability of one raw additive
Fox chain.  V251 reclassifies this as a strict sufficient canary, not a
necessary A9 word-lift gate: ordered word materialization has deeper Fox
prefix terms.  A finite failure rejects only literal equality with this raw
chain.  It does not reject the module correction, roof branch, lift, fake, or
Ihara witness.  The current A6 multiplier is uncomputed.  `verified=false`.

## 1. Completed Fox calculus in the relative source group

Let \(P\) be the normal common-source roof kernel.  It is a finite-index
subgroup of the free group \(F(x,y)\), hence is free of finite rank.  Let

\[
 \mathcal P=\widehat P^{(3)}
\tag{1.1}
\]

be its pro-3 completion and put

\[
 \mathcal R=\mathbf F_3[[\mathcal P]],
 \qquad I=\ker(\varepsilon:\mathcal R\to\mathbf F_3).
\tag{1.2}
\]

Choose once a Schreier free basis \(S\) of \(P\).  The completed left Fox
chain module and endpoint map are

\[
 \mathcal C_1=\mathcal R^{(S)},
 \qquad
 \partial((v_s)_{s\in S})=
       \sum_{s\in S}v_s(s-1).
\tag{1.3}
\]

Only finitely many coordinates occur in every finite word calculation; the
completion is taken in the pro-3 topology.

### Lemma 1.1 (COMPLETED FREE FOX RESOLUTION)

The map in (1.3) is a topological \(\mathcal R\)-module isomorphism

\[
 \boxed{\partial:\mathcal C_1\xrightarrow{\sim}I.}
\tag{1.4}
\]

For \(g\in\mathcal P\), its continuous Fox chain \(\delta(g)\) is the
unique vector satisfying

\[
 \boxed{\partial\delta(g)=g-1.}
\tag{1.5}
\]

#### Proof

The pro-3 completion of a finite-rank free group is the free pro-3 group on
the same basis.  Its Magnus map identifies the completed group algebra with
the noncommutative power-series algebra

\[
 \mathcal R\cong\mathbf F_3\langle\!\langle X_s:s\in S\rangle\!\rangle,
 \qquad s\longmapsto1+X_s.
\tag{1.6}
\]

Every nonconstant monomial has a unique last letter.  Consequently every
element of the power-series augmentation ideal has a unique expansion

\[
 \sum_{s\in S}v_sX_s.
\tag{1.7}
\]

Since \(S\) is finite, (1.7) is a topological direct-sum decomposition and,
under (1.6), is exactly (1.3)--(1.4).  The ordinary Fox fundamental formula
extends continuously from the dense discrete free group and gives (1.5);
uniqueness follows from (1.4). \(\square\)

The Magnus argument is load-bearing.  It would be incorrect to assert that
the augmentation ideal of each finite quotient group algebra is itself a
free module on the images of \(s-1\); finite quotients introduce relations.
Only the completed free pro-3 group algebra has the isomorphism (1.4).

Changing the Schreier basis changes the coordinates of \(\delta(g)\) but
not the element \(1+\partial\delta(g)=g\).  The integrability test below is
therefore intrinsic.

## 2. Group-like elements are exactly profinite words

Equip \(\mathcal R\) with its completed Hopf algebra structure

\[
 \Delta(g)=g\widehat\otimes g,
 \qquad \varepsilon(g)=1
 \quad(g\in\mathcal P).
\tag{2.1}
\]

Call \(u\in\mathcal R\) group-like when

\[
 \Delta(u)=u\widehat\otimes u,
 \qquad \varepsilon(u)=1.
\tag{2.2}
\]

### Lemma 2.1 (GROUP-LIKES OF A COMPLETED GROUP ALGEBRA)

One has

\[
 \boxed{G(\mathcal R)=\mathcal P.}
\tag{2.3}
\]

#### Proof

In the group algebra of a finite quotient \(Q\), write
\(u=\sum_{g\in Q}a_gg\).  The left side of the group-like identity contains
only diagonal basis terms \(g\otimes g\), whereas \(u\otimes u\) has
coefficient \(a_ga_h\) at \(g\otimes h\).  All off-diagonal products must
vanish, so at most one coefficient is nonzero.  The counit condition makes
that coefficient one.  Thus the group-like elements of
\(\mathbf F_3[Q]\) are exactly the elements of \(Q\).

A group-like element of \(\mathcal R\) projects to one group element in
every finite quotient.  These elements are compatible and hence define an
element of \(\mathcal P\).  The converse follows from (2.1). \(\square\)

This proof also supplies a finite negative certificate: one finite quotient
in which the support has more than the single coefficient-one group basis
element disproves group-likeness.

## 3. Exact Fox integrability criterion

### Theorem 3.1 (FOX CHAIN IS A WORD IFF ITS ENDPOINT IS GROUP-LIKE)

For \(Q\in\mathcal C_1\), put

\[
 u_Q=1+\partial Q\in\mathcal R.
\tag{3.1}
\]

Then the following are equivalent.

1. There is a unique \(c\in\mathcal P\) with \(Q=\delta(c)\).
2. The element \(u_Q\) is group-like.
3. In every finite pro-3 quotient, the reduction of \(u_Q\) is exactly one
   group-basis element with coefficient one.

When they hold,

\[
 \boxed{c=u_Q.}
\tag{3.2}
\]

#### Proof

If \(Q=\delta(c)\), (1.5) gives \(u_Q=c\), which is group-like.  Lemma
2.1 proves the equivalence of items 2 and 3 and gives a unique
\(c=u_Q\in\mathcal P\).  Equations (1.5) and (3.1) then give

\[
 \partial\delta(c)=c-1=\partial Q.
\tag{3.3}
\]

Injectivity of \(\partial\) in Lemma 1.1 yields \(\delta(c)=Q\).
\(\square\)

Thus word integrability is not a dimension, rank, or arbitrary section
question.  It is the intrinsic quadratic coalgebra identity (2.2).

## 4. Applying the criterion to the A6 Neumann chain

Let \(a_{\rm w}\in P\) be the accepted exact task192 correction word and
put

\[
 \alpha=\delta(a_{\rm w})\in\mathcal C_1.
\tag{4.1}
\]

An accepted A6 receipt retains the literal roof-fibre pairs

\[
 M=\sum_i b_i(U_i-V_i),
 \qquad \pi(U_i)=\pi(V_i).
\tag{4.2}
\]

Normality of \(P\) makes every retained source word \(W\) act by
conjugation on \(\mathcal P\) and on \(\mathcal R\); denote this action by
\(\sigma_W\).  Transport it through (1.4):

\[
 T_W=\partial^{-1}\sigma_W\partial:
       \mathcal C_1\longrightarrow\mathcal C_1.
\tag{4.3}
\]

Thus \(T_W\delta(g)=\delta(WgW^{-1})\).  Retaining the literal source words
defines the continuous additive operator

\[
 \boxed{\mathcal M=\sum_i b_i(T_{U_i}-T_{V_i}).}
\tag{4.4}
\]

Its reduction is the A6 multiplier action, provided the production receipt
replays the same literal conjugation convention rather than retaining only
the first-shadow coefficient.

### Lemma 4.1 (ROOF-FIBRE DIFFERENCES RAISE FOX FILTRATION)

Put

\[
 \mathcal F^m\mathcal C_1=\partial^{-1}(I^{m+1})
 \quad(m\geq0).
\tag{4.5}
\]

Then

\[
 \boxed{\mathcal M(\mathcal F^m\mathcal C_1)
                 \subseteq\mathcal F^{m+1}\mathcal C_1.}
\tag{4.6}
\]

#### Proof

For one pair put \(p=U_iV_i^{-1}\in P\).  On \(\mathcal R\),

\[
 \sigma_{U_i}=\operatorname{Inn}(p)\sigma_{V_i}.
\tag{4.7}
\]

If \(z\in I^{m+1}\), then

\[
 \bigl(\operatorname{Inn}(p)-1\bigr)z
 =(p-1)zp^{-1}+z(p^{-1}-1)\in I^{m+2}.
\tag{4.8}
\]

Both automorphisms preserve every augmentation power.  Equations
(4.3), (4.7), and (4.8) show that each \(T_{U_i}-T_{V_i}\) raises the
filtration once; their finite linear combination does too. \(\square\)

Since \(\alpha\in\mathcal F^0\mathcal C_1\), Lemma 4.1 proves that the series

\[
 \boxed{
 Q_\infty=-\sum_{r\ge0}\mathcal M^r\alpha}
\tag{4.9}
\]

converges.  Every finite quotient stable under the retained conjugation
actions sees a finite sum, because the augmentation ideal of its finite
3-group image is nilpotent.  Formula (4.9) is the source-Fox-chain version of
v174's pointed Neumann correction.

### Corollary 4.1 (ONE EXACT WORD-INTEGRABILITY GATE)

The additive Neumann candidate (4.9) is the Fox chain of one compatible
pro-3 correction word if and only if

\[
 \boxed{
 \Delta\bigl(1+\partial Q_\infty\bigr)
 =\bigl(1+\partial Q_\infty\bigr)
  \widehat\otimes
  \bigl(1+\partial Q_\infty\bigr).}
\tag{4.10}
\]

On a pass the word is explicit as the group-like element

\[
 \boxed{c_\infty=1+\partial Q_\infty.}
\tag{4.11}
\]

On a failure at one finite quotient, the named \((a_{\rm w},M)\) additive
Neumann chain is not the Fox chain of a word.  This does not exclude another
A5 multiplier, another word representative with a different finer action,
or an adaptive nonlinear Hensel correction.

#### Proof

Apply Theorem 3.1 to (4.9).  Lemma 4.1 makes all registered finite
reductions effective. \(\square\)

The literal-word ancestry in A6 is essential: a first-shadow coefficient
with source representatives discarded does not determine the operator
\(\mathcal M\), hence does not determine (4.9)--(4.11).

## 5. Certificate contract and claim boundary

For a proof-carrying A9 word-integrability result, retain:

1. the exact task192 source word and its Schreier/Fox chain \(\alpha\);
2. every A6 pair, coefficient, source conjugation, and action order;
3. at finite rung \(n\), the nilpotence cutoff and every term of the finite
   reduction of (4.9);
4. the complete coefficient support of \(u_{Q,n}=1+\partial Q_n\);
5. on a pass, its unique basis element and compatible reductions; or
6. on a failure, the first preregistered quotient and at least two nonzero
   support coefficients (or another exact violation of (2.2)).

The independent checker reconstructs the Fox chain with a different
Schreier tree and checks the basis-independent group-algebra element
\(u_{Q,n}\).  A matching hash without support replay is insufficient.

Passing (4.10) constructs one especially rigid word whose Fox chain is the
raw additive series.  V174 does not require this literal Fox-chain equality:
v98 materializes the same graded module values by ordered word products whose
Fox chains contain deeper prefix terms.  Therefore failure of (4.10) rejects
only this strict Fox-linear materialization.  It does not reject an explicit
word lift obtained by nonlinear Hensel correction.  Exact two-hexagon and
printed-pentagon evaluations remain separate.

## 6. Fixed frontier

```text
COMPLETED FREE FOX ENDPOINT ISOMORPHISM:             PAPER PROOF
GROUP-LIKE ELEMENTS = PRO-3 WORDS:                   PAPER PROOF
FOX CHAIN INTEGRABLE <=> ENDPOINT GROUP-LIKE:        PAPER PROOF
A6 WORD PAIRS -> EXPLICIT NEUMANN SOURCE CHAIN:      PAPER CONSTRUCTION
ONE HOPF IDENTITY DECIDES RAW FOX-CHAIN INTEGRABILITY: PAPER PROOF
ACTUAL A6 M / Q_INFINITY / GROUP-LIKE TEST:           NOT COMPUTED
GROUP-LIKE TEST AS NECESSARY A9 GATE:                 RETRACTED BY v251
EXACT NONLINEAR H1/H2/P FOR THE RESULTING WORD:       OPEN
MIXED-PRIME / PERFECT-CORE / FAKE / IHARA:           OPEN
```

`R07_NEUMANN_FOX_GROUP_LIKE_INTEGRABILITY_V249_PAPER_GRADE`
