# R07 class-two nonlinear remainder vanishes (v356)

Author: Sol / 2026-08-29

Status: R07-specific paper theorem after v33, v252, v263, v266 and v355.
For every literal first correction with zero exponent sums, the two registered
hexagon class-two contributions cancel in characteristic three, while the
pentagon contribution vanishes because the mod-three degree-two Brunnian
subspace of PB4 is zero.  Hence the first nonlinear canary is structurally
`q2=0`, so its pointed cyclic-return coefficient may be chosen `nu2=0`.
This does not prove the transported-linear return at later depths or the
all-depth nonlinear recurrence.  No actual A0 word, compatible lift, fake or
Ihara witness is declared.  `verified=false`.

## 1. Registered hexagon contexts in class two

In the task198/task193 PB3 owner put

\[
 x=A_{12},\qquad y=A_{23},\qquad
 z=(xy)^{-1},\qquad u=(yx)^{-1}.
\tag{1.1}
\]

The exact occurrence/sign rosters are

\[
\begin{array}{c|ccc}
H1&(x,y),+&(x,z),-&(y,z),+\\
H2&(u,x),-&(x,y),-&(u,y),+ .
\end{array}
\tag{1.2}
\]

The physical product is stored in reverse occurrence order, but degree two
is central, so only the retained signs matter after the literal order has
first been authenticated.

Let `c` be the word actually applied by task193 and assume its two integer
exponent sums vanish.  Then `c in [F2,F2]`.  In the maximal exponent-three
class-two quotient of `F2`, there is one scalar `kappa in F3` with

\[
 [c]_2=\kappa[X,Y].
\tag{1.3}
\]

For any context `rho`, the class-two value of `rho(c)` depends only on the
degree-one images of `X,Y`.

### Lemma 1.1 (H1 THREE-CYCLE CANCELLATION)

The three signed H1 occurrence values of `c` sum to zero in the degree-two
PB3 quotient.

#### Proof

Write `h=[x,y]`.  In abelian degree one, `z=-x-y`, so

\[
 [x,z]=-h,\qquad [y,z]=h.
\tag{1.4}
\]

Applying the signs in (1.2), the three values are

\[
 \kappa h,\qquad -\kappa(-h),\qquad \kappa h.
\tag{1.5}
\]

Their sum is `3*kappa*h=0` over `F3`.  Every task193 prefix conjugation is
invisible because these occurrence values are already central in the
class-two quotient.  \(\square\)

### Lemma 1.2 (H2 THREE-CYCLE CANCELLATION)

The three signed H2 occurrence values of `c` sum to zero in the degree-two
PB3 quotient.

#### Proof

In degree one `u=-y-x`, whence

\[
 [u,x]=h,\qquad [u,y]=-h.
\tag{1.6}
\]

The signs in (1.2) give

\[
 -\kappa h,\qquad -\kappa h,\qquad -\kappa h,
\tag{1.7}
\]

whose sum is `-3*kappa*h=0`.  Prefix conjugations again act trivially in
degree two.  \(\square\)

In v355 notation every occurrence has `ell_o=0`, since `rho_o(c)` has zero
PB abelianization.  Thus there is no pairwise `ell wedge ell'` term, and
Lemmas 1.1--1.2 prove

\[
 q_{2,H1}=q_{2,H2}=0.
\tag{1.8}
\]

## 2. The degree-two PB4 Brunnian subspace is zero

Let `t_ij` be the degree-one class of `A_ij` in PB4.  The degree-two
infinitesimal pure-braid relations are

\[
 [t_{ij},t_{kl}]=0
 \quad(\{i,j\}\cap\{k,l\}=\varnothing),
\tag{2.1}
\]

and, for distinct `i,j,k`,

\[
 [t_{ij},t_{ik}+t_{jk}]=0.
\tag{2.2}
\]

They are exactly the degree-two initial forms of task292's complete PB4
relator roster.  Row reduction gives the four-element basis

\[
 h_{123},\ h_{124},\ h_{134},\ h_{234},
\qquad h_{ijk}=[t_{ij},t_{ik}],
\tag{2.3}
\]

for the mod-three degree-two quotient.  Equivalently its dimension is
`1+3=4` from the recursive splitting `PB4=PB3 semidirect F3`.

Let `d_l:PB4->PB3` delete strand `l`.

### Lemma 2.1 (FOUR-DELETION SEPARATION IN DEGREE TWO)

\[
 \boxed{
 \bigcap_{l=1}^4\ker(\operatorname{gr}_2d_l)=0.}
\tag{2.4}
\]

#### Proof

Deleting the unique strand outside the triple `{i,j,k}` maps `h_ijk` to the
nonzero degree-two generator of PB3.  Deleting any strand inside that triple
kills it.  Thus, in the ordered basis (2.3), deletion of strands `4,3,2,1`
reads respectively the four coordinates `123,124,134,234`.  A vector killed
by all four maps has every coordinate zero.  \(\square\)

### Corollary 2.2 (BRUNNIAN PB4 STARTS IN DEGREE THREE)

For the mod-three Zassenhaus filtration,

\[
 \operatorname{Brun}_4\subseteq D_3(PB4).
\tag{2.5}
\]

#### Proof

The degree-one assertion follows similarly: every generator `t_ij` survives
deletion of either strand outside its pair.  A Brunnian braid is killed by
all four deletions, so its degree-one and degree-two classes lie in the two
common kernels.  They are both zero, the latter by Lemma 2.1.  \(\square\)

## 3. Vanishing of the complete first nonlinear remainder

Assume, as in the accepted R07 lane, that both `f0=g760` and
`f1=g760*c` are commutator words.  BRUN-DEF gives

\[
 P(f_0),P(f_1)\in\operatorname{Brun}_4.
\tag{3.1}
\]

Since the Brunnian subgroup is a subgroup,

\[
 P(f_1)P(f_0)^{-1}\in\operatorname{Brun}_4.
\tag{3.2}
\]

V355 identifies the degree-two coordinate of (3.2) with `q_(2,P)`.
Corollary 2.2 therefore gives

\[
 q_{2,P}=0.
\tag{3.3}
\]

### Theorem 3.1 (R07 FIRST NONLINEAR CANARY VANISHES)

For every authenticated task193 first correction with zero exponent sums,

\[
 \boxed{q_2=(q_{2,H1},q_{2,H2},q_{2,P})=0.}
\tag{3.4}
\]

Consequently the pointed return condition of v263 holds with

\[
 \boxed{\nu_2=0,\qquad\lambda_2=\mu.}
\tag{3.5}

#### Proof

Combine (1.8) and (3.3).  The zero vector belongs to every actual cyclic and
localized return module with the empty common-source ancestry, proving the
first equality in (3.5); the second is v263's
`lambda_2=mu+nu_2`.  \(\square\)

No numerical A0-dependent class-two elimination is required for membership.
The v355/task379 compiler remains useful as a direct destructive check of
the eleven physical contexts, signs and factor order.

## 4. Remaining all-depth boundary

V266 Lemma 5.1 already shows that from depth `r>=2`, terms containing two
new occurrences of the depth-`r` correction skip the immediately following
layer.  Theorem 3.1 removes the exceptional depth-one self-quadratic term.
What remains is the transported-linear interaction of each new correction
with the accumulated shallower word and residual tail.  This theorem does
not prove that those later terms return to the same actual common-word
module.

Thus the next structural target is narrower than NLSAT as previously stated:
construct a natural return operator for the transported-linear one-layer
term.  No fresh self-quadratic solver is needed at any depth.

```text
H1 CLASS-TWO NONLINEAR TERM:                 ZERO IN CHARACTERISTIC THREE
H2 CLASS-TWO NONLINEAR TERM:                 ZERO IN CHARACTERISTIC THREE
PB4 DEGREE-TWO BRUNNIAN SUBSPACE:            ZERO
FIRST R07 NONLINEAR REMAINDER q2:             ZERO, nu2=0 (PAPER PROOF)
TASK379 NUMERICAL REPLAY:                     IMPLEMENTATION ACTIVE
LATER NEW-NEW QUADRATIC TERMS AT NEXT LAYER:  ABSENT FOR r>=2 (v266)
LATER TRANSPORTED-LINEAR RETURN:              OPEN
ALL-DEPTH NONLINEAR RECURRENCE:               OPEN
COMPATIBLE LIFT / FAKE / IHARA:               NONE
```

`R07_CLASS_TWO_NONLINEAR_REMAINDER_VANISHES_V356_PAPER_GRADE`
