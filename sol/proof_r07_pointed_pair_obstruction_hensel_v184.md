# R07 pointed pair-obstruction Hensel selector v184

Author: Sol / 2026-08-28

Status: paper theorem and a strictly smaller all-rung multiplier gate than
v183 pair saturation.  To lift one already chosen coefficient, it is enough
to kill one named class in the pair-saturation defect; the whole defect
space need not vanish.  The theorem gives an explicit noncommutative
finite-Neumann formula for the lifted coefficient.  The corresponding R07
class has not yet been computed.  No compatible lift, fake certificate, or
Ihara witness is declared.

## 1. One nilpotent relative edge

Let

\[
 \Lambda'\twoheadrightarrow\Lambda,
 \qquad I=\ker(\Lambda'\to\Lambda)
\tag{1.1}
\]

be a surjection of possibly noncommutative rings with \(I^N=0\).  Let
\(Z'\) be a left \(\Lambda'\)-module and put

\[
 Z=Z'/IZ'.
\tag{1.2}
\]

Choose compatible \(d',e'\in Z'\), with reductions \(d,e\in Z\), and set

\[
 M'=\Lambda'd'+\Lambda'e'.
\tag{1.3}
\]

Suppose one downstairs coefficient has already been selected:

\[
 e=\mu d,
 \qquad \mu\in\Lambda.
\tag{1.4}
\]

Choose an arbitrary ring lift \(\widetilde\mu\in\Lambda'\).  Then

\[
 z_{\widetilde\mu}=e'-\widetilde\mu d'
 \in M'\cap IZ'.
\tag{1.5}
\]

Define the pointed obstruction

\[
 \boxed{
 \omega_{d',e'}(\mu)=
 [z_{\widetilde\mu}]
 \in {M'\cap IZ'\over IM'}.}
\tag{1.6}
\]

### Lemma 1.1 (THE POINTED CLASS IS WELL DEFINED)

The class (1.6) is independent of the chosen lift
\(\widetilde\mu\).

#### Proof

Two lifts differ by \(\kappa\in I\), and their residuals differ by
\(-\kappa d'\in IM'\). \(\square\)

The ambient quotient in (1.6) is exactly the pair-saturation obstruction
space of v183, but only one named element of it is relevant to the selected
coefficient \(\mu\).

## 2. Exact pointed lifting theorem

### Theorem 2.1 (POINTED PAIR-OBSTRUCTION HENSEL LIFT)

Under (1.1)--(1.4), the following are equivalent.

1. There is a coefficient \(\mu'\in\Lambda'\) such that

   \[
    e'=\mu'd',
    \qquad \overline{\mu'}=\mu.
   \tag{2.1}
   \]

2. The single pointed class vanishes:

   \[
    \boxed{\omega_{d',e'}(\mu)=0.}
   \tag{2.2}
   \]

3. The downstairs syzygy \((-\mu,1)\) has a syzygy lift: there are
   \(a,b\in\Lambda'\) with

   \[
    ad'+be'=0,
    \qquad (\bar a,\bar b)=(-\mu,1).
   \tag{2.3}
   \]

Moreover, (2.2) gives an explicit coefficient.  If a retained ancestry for
the zero class is written

\[
 e'-\widetilde\mu d'=\alpha d'+\beta e',
 \qquad \alpha,\beta\in I,
\tag{2.4}
\]

then

\[
 \boxed{
 \mu'=(1-\beta)^{-1}(\widetilde\mu+\alpha),
 \qquad
 (1-\beta)^{-1}=\sum_{r=0}^{N-1}\beta^r.}
\tag{2.5}
\]

The order of the factors in (2.5) is load-bearing.

#### Proof

If (2.1) holds, then

\[
 z_{\widetilde\mu}
   =(\mu'-\widetilde\mu)d'\in IM',
\tag{2.6}
\]

so (2.2) holds.

Conversely, (2.2) means exactly that (2.4) can be written.  Rearranging it
without commuting any factors gives

\[
 (1-\beta)e'=(\widetilde\mu+\alpha)d'.
\tag{2.7}
\]

Because \(\beta\in I\) and \(I^N=0\), the displayed finite series in
(2.5) is the two-sided inverse of \(1-\beta\).  Left multiplication of
(2.7) gives (2.1), and reduction of (2.5) gives
\(\overline{\mu'}=\mu\).

Equation (2.4) also gives the syzygy

\[
 (-\widetilde\mu-\alpha)d'+(1-\beta)e'=0,
\tag{2.8}
\]

which reduces to \((-\mu,1)\), proving (2.2) implies (2.3).  Finally, in
(2.3) the element \(b\) reduces to one, so \(b=1+\gamma\) with
\(\gamma\in I\) and is a unit.  Then

\[
 e'=-b^{-1}a\,d',
 \qquad \overline{-b^{-1}a}=\mu,
\tag{2.9}
\]

which proves (2.1). \(\square\)

No annihilator hypothesis on \(d'\) is present.  The coefficient need not
be unique; (2.5) constructs one compatible with the specified downstairs
choice.

## 3. The roof-zero fast gate

At the first relative edge relevant to R07, the intended coefficient at the
roof is \(\mu_0=0\), and the corrected residual reduces to zero.  Take
\(\widetilde\mu_0=0\).  Theorem 2.1 specializes to

\[
 \boxed{
 e_1=\mu_1d_1\text{ for some }\mu_1\in I_0
 \quad\Longleftrightarrow\quad
 e_1\in I_0M_1,}
\tag{3.1}
\]

where

\[
 M_1=\Lambda_1d_1+\Lambda_1e_1.
\tag{3.2}
\]

Thus neither the full pair-saturation equality

\[
 M_1\cap I_0Z_1=I_0M_1
\tag{3.3}
\]

nor direct enumeration of all of \(I_0d_1\) is logically required for the
first pointed decision.  A positive ancestry

\[
 e_1=\alpha d_1+\beta e_1,
 \qquad \alpha,\beta\in I_0
\tag{3.4}
\]

returns the literal coefficient

\[
 \boxed{\mu_1=(1-\beta)^{-1}\alpha\in I_0.}
\tag{3.5}
\]

The inverse is a finite sum.  Direct replay of (3.5), including its
reduction to zero, is part of the certificate.

If the relative edge comes from a finite \(3\)-group kernel \(K\), then
v183 Lemma 2.1 and v180 Lemma 2.1 give

\[
 I_0M_1=J_KM_1
 =\sum_{i=1}^t(s_i-1)M_1
\tag{3.6}
\]

for any registered generating set \(K=\langle s_1,\ldots,s_t\rangle\).
Consequently (3.1) is the single rank comparison

\[
 \boxed{
 \operatorname{rank}(I_0M_1)
 =\operatorname{rank}(I_0M_1+\langle e_1\rangle).}
\tag{3.7}
\]

A negative result with a dual annihilating the complete span in (3.6) but
not \(e_1\) is a complete finite obstruction to a coefficient reducing to
zero.  It is stronger and more targeted than merely observing failure of
the universal pair-saturation equality.

### Lemma 3.1 (EXPLICIT FIRST-FRATTINI INVERSE LENGTH)

If the first relative kernel is

\[
 K=\langle s_1,\ldots,s_t\rangle\cong(C_3)^t,
\tag{3.8}
\]

then

\[
 \boxed{J_K^{,2t+1}=0.}
\tag{3.9}
\]

Consequently every \(\beta\in I_0\) occurring in (3.4) has the certified
inverse

\[
 \boxed{
 (1-\beta)^{-1}=\sum_{r=0}^{2t}\beta^r.}
\tag{3.10}
\]

#### Proof

Put \(T_i=s_i-1\).  Since the generators commute and have order three,
characteristic three gives

\[
 \mathbf F_3[K]
 \cong
 \mathbf F_3[T_1,\ldots,T_t]/(T_1^3,\ldots,T_t^3).
\tag{3.11}
\]

The augmentation ideal is \((T_1,\ldots,T_t)\).  A nonzero monomial has
exponent at most two in each variable, hence total degree at most \(2t\).
This proves (3.9).  Normality of \(K\) gives
\(I_0^r=\Lambda_1J_K^r\), so \(I_0^{2t+1}=0\) as well.  The finite
geometric-series identity proves (3.10). \(\square\)

This bound removes a search parameter from the first-edge certificate: the
producer and checker can replay exactly \(2t+1\) ordered powers.  Later
non-elementary relative kernels require their authenticated nilpotence
bound or a refined chief-step decomposition.

## 4. Compatible tower selector

Let

\[
 \Lambda_{n+1}\twoheadrightarrow\Lambda_n,
 \qquad I_n=\ker(\Lambda_{n+1}\to\Lambda_n),
 \qquad Z_{n+1}/I_nZ_{n+1}\cong Z_n
\tag{4.1}
\]

be the diagonal-context rings and full Fox cokernels on a matched relative
pro-\(3\) tower.  Let \(d=(d_n)\) and \(e=(e_n)\) be compatible and put

\[
 M_n=\Lambda_nd_n+\Lambda_ne_n.
\tag{4.2}
\]

### Theorem 4.1 (POINTED ALL-RUNG HENSEL SELECTOR)

Start with \(e_0=0\) and \(\mu_0=0\).  Suppose that, after
\(\mu_n\) has been chosen, the pointed class

\[
 \omega_{d_{n+1},e_{n+1}}(\mu_n)
 \in {M_{n+1}\cap I_nZ_{n+1}\over I_nM_{n+1}}
\tag{4.3}
\]

vanishes at every successor.  Then the formula (2.5), applied recursively,
constructs a compatible family

\[
 \boxed{
 e_n=\mu_nd_n,
 \qquad \mu_{n+1}\mapsto\mu_n.}
\tag{4.4}
\]

Its inverse-limit value \(\mu\) lies in the relative augmentation ideal
\(\mathfrak j\).  Under the word-bearing and nonlinear hypotheses of v174,
one compatible correction is therefore

\[
 \boxed{
 c_\infty=-\sum_{r\ge0}\mu^ra.}
\tag{4.5}
\]

#### Proof

Every successor ideal is nilpotent by v183 Lemma 2.1.  Given \(\mu_n\),
choose any ring lift and apply Theorem 2.1 to (4.3).  Formula (2.5) returns
\(\mu_{n+1}\) reducing to the specified \(\mu_n\), so induction proves
(4.4).  Since \(\mu_0=0\), the compatible family belongs to the kernel of
the roof reduction, namely \(\mathfrak j\).  Formula (4.5) is v174 Theorem
2.1. \(\square\)

This is strictly weaker than v183 Corollary 5.1: pair saturation makes the
entire quotient in (4.3) zero, whereas Theorem 4.1 asks only for the one
class selected by the preceding coefficient.  It is still an all-rung
obligation.  One positive first-edge computation does not prove that all
later pointed classes vanish.

## 5. Exact R07 certificate and next structural target

For one genuine successor, the smallest certificate is:

1. the full block-tagged Fox cokernels and their registered reduction;
2. the compatible literal rows \(d',e'\) and a specified downstairs
   coefficient \(\mu\);
3. the complete diagonal orbit span of \(M'\) and the generator-only span
   \(IM'\);
4. either an ancestry (2.4), the finite inverse (2.5), and direct replay of
   \(e'=\mu'd'\), or a complete separating dual for the single class; and
5. independent replay with mutations of the residual sign, factor order,
   kernel generator, and one ancestry coefficient.

Task195 may therefore run (3.7) as a pointed fast gate.  Its separate pair-
coinvariant test remains useful evidence for the stronger structural
theorem, but failure of pair saturation does not settle the pointed class.

To stop all later finite tests, it is now enough to construct a natural
class-specific operation which, for every lifted coefficient, writes

\[
 e_{n+1}-\widetilde\mu_nd_{n+1}
   =\alpha_nd_{n+1}+\beta_ne_{n+1},
 \qquad \alpha_n,\beta_n\in I_n,
\tag{5.1}
\]

compatibly with refinement.  Substitution into (2.5) is then the desired
closed relative Hensel selector.  This target is smaller than constructing
a right inverse on the whole return-even module.

## 6. Fixed frontier

```text
POINTED OBSTRUCTION CLASS / LIFT INDEPENDENCE:    PAPER_PROOF
POINTED HENSEL EQUIVALENCE AND FINITE FORMULA:    PAPER_PROOF
ROOF-ZERO I*M FAST GATE:                         PAPER_PROOF
FIRST-FRATTINI INVERSE LENGTH 2t+1:              PAPER_PROOF
POINTED ALL-RUNG COMPATIBLE SELECTOR:             PAPER_PROOF
R07 FIRST SUCCESSOR POINTED CLASS:                NOT COMPUTED
R07 NATURAL ALL-RUNG POINTED ANCESTRY (5.1):      NOT PROVED
TASK192 EXACT FIRST CORRECTION:                   GHA IN PROGRESS
TASK193 ACTUAL SUCCESSOR COMPILER:                SELFTEST CROSS-CHECKED
TASK194 SHARDED BOUNDARY CORRELATION:             STATIC REPAIR IN PROGRESS
TASK195 POINTED / PAIR CANARY:                    IMPLEMENTATION IN PROGRESS
WORD/NONLINEAR/FORMATION GATES:                   OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA:           NOT DECLARED
```

`R07_POINTED_PAIR_OBSTRUCTION_HENSEL_V184_PAPER_GRADE`
