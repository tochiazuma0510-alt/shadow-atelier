# R07 multicyclic completed actual-class selector v167

Author: Sol / 2026-08-27

Status: paper theorem.  This note extends the cyclic one-variable route of
v133/v164 to a finite-rank abelian $p$-primary deck tower.  It shows that one
completed actual-class membership, rather than unrelated choices at every
finite level, constructs all compatible corrections.  It does not
authenticate that the current R07 tower is such a base change, does not
compute the actual completed membership, and does not cover nonabelian simple
chief factors.  No compatible R07 lift, fake, or Ihara witness is declared.

## 1. Multicyclic deck tower

Let $k$ be a field of characteristic $p$ and fix $d<\infty$.  For a
multi-index $\mathbf a=(a_1,\ldots,a_d)$ put

$$
 \Gamma_{\mathbf a}=\prod_{i=1}^d C_{p^{a_i}},
 \qquad R_{\mathbf a}=k[\Gamma_{\mathbf a}].
\tag{1.1}
$$

Choose compatible generators $\tau_{i,\mathbf a}$ under coordinatewise
quotient maps and put $T_i=\tau_i-1$.  Then

$$
 R_{\mathbf a}\cong
 k[T_1,\ldots,T_d]/
 (T_1^{p^{a_1}},\ldots,T_d^{p^{a_d}}),
\tag{1.2}
$$

and, over the directed set of cofinal multi-indices,

$$
 \Lambda:=\varprojlim_{\mathbf a}R_{\mathbf a}
 \cong k[[T_1,\ldots,T_d]].
\tag{1.3}
$$

Write

$$
 I_{\mathbf a}=
 (T_1^{p^{a_1}},\ldots,T_d^{p^{a_d}})\triangleleft\Lambda.
\tag{1.4}
$$

The ideals $I_{\mathbf a}$ are cofinal for the $(T_1,\ldots,T_d)$-adic
topology when every $a_i\to\infty$.  Lanes in which some direction is held
fixed are treated by deleting that direction from the completed variables,
not by silently calling the resulting family cofinal.

## 2. Finite equivariant templates still base-change

Let $X$ be a finite connected presentation complex.  Suppose one compatible
map

$$
 \chi:\pi_1(X)\longrightarrow\mathbf Z_p^d
\tag{2.1}
$$

has surjective reduction onto every registered $\Gamma_{\mathbf a}$.  Choose
one orientation and one lift of every cell.  The regular cover then has

$$
 C_j(X_{\mathbf a};k)\cong R_{\mathbf a}^{c_j}.
\tag{2.2}
$$

Evaluate the Fox derivatives of one fixed finite ordered all-seven template
through

$$
 k[\pi_1(X)]\longrightarrow R_{\mathbf a},
 \qquad
 g\longmapsto\prod_{i=1}^d
 \tau_{i,\mathbf a}^{\chi_i(g)}.
\tag{2.3}
$$

As in v164, distinct typed cells and distinct printed A.18 occurrences remain
distinct coordinates even if their evaluated group values coincide.

### Proposition 2.1 (MULTICYCLIC FOX BASE CHANGE)

Assume that H1, H2, every printed A.18 occurrence, every PB3/PB4 boundary
block, and the literal target are the complete deck translates of the same
fixed finite ordered template at every level.  Then there are finite free
completed modules

$$
 A=\Lambda^m,\qquad Z=\Lambda^n,
\tag{2.4}
$$

a matrix $B:A\to Z$, and $z\in Z$ such that the literal finite system is

$$
 \boxed{
 A_{\mathbf a}=A/I_{\mathbf a}A,\quad
 Z_{\mathbf a}=Z/I_{\mathbf a}Z,\quad
 B_{\mathbf a}=B\bmod I_{\mathbf a},\quad
 z_{\mathbf a}=z\bmod I_{\mathbf a}.}
\tag{2.5}
$$

All coordinatewise transition squares commute in the frozen typed order.

#### Proof

Fox differentiation takes place before evaluation and commutes with every
ring homomorphism (2.3), by the product and inverse identities used in v164
Lemma 2.1.  A complete family of translates of each base column is precisely
its $R_{\mathbf a}$-span, now with the unique group-ring expansion indexed by
$\Gamma_{\mathbf a}$.  Therefore one finite base-column roster defines the
same matrix over every $R_{\mathbf a}$ and over their inverse limit
$\Lambda$.  The literal target has the same naturality.  Typed direct sums
preserve the statement block by block. $\square$

This proposition is a conditional authentication theorem.  A collection of
finite quotient orbit columns with no common deck character, or a producer
which adds level-dependent cell orbits, does not satisfy its hypothesis.

## 3. Completion removes independent finite choices

Let

$$
 M=\operatorname{im}B\subseteq Z,
 \qquad Q=Z/M,
\tag{3.1}
$$

and denote the class of $z$ in $Q$ by $\bar z$.  Since $\Lambda$ is a
Noetherian complete local ring and $Q$ is finitely generated, $Q$ is separated
for its maximal-ideal topology.  In particular,

$$
 \bigcap_{N\geq0}(T_1,\ldots,T_d)^NQ=0.
\tag{3.2}
$$

### Theorem 3.1 (ALL-FINITE-LEVELS IMPLY ONE COMPLETED SOLUTION)

Under Proposition 2.1, the following are equivalent.

1. There exists $a_\infty\in A$ with $Ba_\infty=z$.
2. There is a compatible family
   $a_{\mathbf a}\in A_{\mathbf a}$ satisfying
   $B_{\mathbf a}a_{\mathbf a}=z_{\mathbf a}$.
3. The finite equation
   $B_{\mathbf a}a=z_{\mathbf a}$ is soluble for every cofinal
   multi-index $\mathbf a$; the separately found solutions need not have
   been chosen compatibly.
4. The actual completed class vanishes: $\bar z=0$ in $Q$.

When these conditions hold, any one completed coefficient $a_\infty$ reduces
to mutually compatible finite coefficients at every level.

#### Proof

Conditions 1 and 4 are equivalent by (3.1), and condition 1 immediately gives
condition 2, which gives condition 3.

Assume condition 3.  Finite-level solubility says

$$
 z\in M+I_{\mathbf a}Z,
 \qquad\text{hence}\qquad
 \bar z\in I_{\mathbf a}Q
\tag{3.3}
$$

for every $\mathbf a$.  If
$q_{\mathbf a}=\min_i p^{a_i}$, then
$I_{\mathbf a}\subseteq(T_1,\ldots,T_d)^{q_{\mathbf a}}$.
Cofinality makes $q_{\mathbf a}$ arbitrarily large, so (3.2) and (3.3) imply
$\bar z=0$.  This proves condition 4 and closes the cycle. $\square$

When $k$ is finite, equivalently one may apply compactness to the finite
solution sets: a finitely branching tree having a nonempty level at every
depth has a compatible infinite branch.  The module proof above works over
arbitrary $k$ and additionally identifies the only obstruction as the
completed cokernel class.

### Corollary 3.2 (NO MEASURE-ZERO OBSTRUCTION)

No measure-theoretic positive-density hypothesis is required.  Under exact
base change, mere nonemptiness at every finite cofinal level already forces a
compatible branch.  Conversely, positive density at many levels says nothing
if even one cofinal level is empty.  Thus compactness/completion is the sound
replacement for a probabilistic selector on this lane.

## 4. One actual-class computation

For $d=1$, v133 diagonalizes $B$ over the DVR $k[[T]]$ and obtains the exact
Smith divisibility test.  For $d>1$, the ring
$k[[T_1,\ldots,T_d]]$ is generally not a PID, so an invariant-factor Smith
form must not be asserted.

Instead use a completed module-membership certificate.  Fix a local monomial
order and let $G=(g_1,\ldots,g_t)$ be a finite standard basis of
$M\subseteq\Lambda^n$, with recorded representations

$$
 g_j=Bq_j,\qquad q_j\in\Lambda^m.
\tag{4.1}
$$

### Theorem 4.1 (COMPLETED STANDARD-BASIS SELECTOR)

Suppose an authenticated complete division of the actual target gives

$$
 z=\sum_{j=1}^t h_jg_j+r,
\tag{4.2}
$$

where $r$ is the standard remainder.  Then

$$
 \boxed{z\in\operatorname{im}B\iff r=0.}
\tag{4.3}
$$

If $r=0$, the explicit completed coefficient

$$
 \boxed{a_\infty=\sum_{j=1}^t h_jq_j}
\tag{4.4}
$$

satisfies $Ba_\infty=z$, and reduction modulo every $I_{\mathbf a}$ gives
the compatible finite correction.  If $r\ne0$, the nonzero completed
remainder is an exact module-membership obstruction for this named lane.

#### Proof

The defining property of a standard basis is that complete division has zero
remainder exactly on the generated submodule.  Substituting (4.1) into (4.2)
when $r=0$ proves (4.4).  Proposition 2.1 then carries the equality to every
finite level. $\square$

The certificate must contain complete power-series data or an independently
replayable finite recurrence which determines it to arbitrary precision.
A long but finite truncation with zero remainder is not by itself a completed
membership proof.  The theorem supplies a class-specific coefficient, not a
linear splitting of all of $M$; such a splitting need not exist in several
variables.

## 5. Literal words and relative dihedral splitting

Every coefficient in
$R_{\mathbf a}=k[\Gamma_{\mathbf a}]$ is a finite combination of deck
translates.  If the authenticated realization sends addition to the frozen
ordered product, additive inverse to word inverse, and deck monomials to the
registered translate/conjugate operation, then
$a_\infty\bmod I_{\mathbf a}$ materializes a finite ordinary correction word.
Direct replay of both hexagons and the printed-order pentagon remains the
positive certificate.

Assume $p$ is odd and a continuous involution $\theta$ preserves $A,Z,B$.
Put $e_\pm=(1\pm\theta)/2$.  If the established relative-dihedral homotopy
supplies a preimage of the actual return-odd class and Theorem 4.1 supplies a
preimage of the actual return-even class, their sum is one completed preimage
of the full class.  This is the multivariable analogue of v133 Corollary 5.1.
It does not claim that $1-\theta$ kills a return-even survivor.

The normalized exponent coordinates factor through augmentation and are
torsion targets, not free summands of $Z$.  They remain governed separately
by v157/v158 and literal exactification, exactly as in v164 Section 5.

## 6. Exact application boundary

For R07, this theorem replaces infinitely many abelian $p$-primary checks by
one completed actual-class check only after the following finite gates pass:

1. one finite-rank compatible character to $\mathbf Z_p^d$ is registered;
2. every H1/H2/A.18/boundary column is the full deck orbit of one fixed typed
   Fox template;
3. the literal R07 defect is one compatible completed target;
4. no level-dependent cell orbit or section convention lies outside that
   template; and
5. an exact Smith certificate ($d=1$) or completed standard-basis certificate
   ($d>1$) accepts the actual class.

Different primes must be handled in their own coefficient characteristics
and interleaved along the chosen ladder.  An arbitrary nonabelian or
unbounded-rank Frattini tower is not turned into (1.3) by this theorem.
Nonabelian simple chief factors still require the v52/v77/v166 accepted-set
solve.

```text
MULTICYCLIC FOX TEMPLATE => COMPLETED BASE CHANGE: PAPER_PROOF
ALL FINITE LEVELS SOLUBLE => COMPATIBLE BRANCH:    PAPER_PROOF
COMPLETED STANDARD-BASIS ACTUAL-CLASS SELECTOR:    PAPER_PROOF
RELATIVE DIHEDRAL-ODD + COMPLETED EVEN GLUING:     PAPER_PROOF
R07 MULTICYCLIC TEMPLATE AUTHENTICATION:           NOT PERFORMED
R07 COMPLETED ACTUAL-CLASS MEMBERSHIP:             NOT COMPUTED
FIRST EXACT ALL-SEVEN WORD:                        NOT YET CONSTRUCTED
NONABELIAN ACCEPTED SETS:                          OPEN
COMPATIBLE COFINAL R07 LIFT / FAKE / IHARA:        NOT DECLARED
```

`R07_MULTICYCLIC_COMPLETED_CLASS_SELECTOR_V167_PAPER_GRADE`
