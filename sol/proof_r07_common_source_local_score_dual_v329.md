# R07 common-source local-score dual normal form (v329)

Author: Sol / 2026-08-29

Status: paper theorem dualizing v313 and v324.  Every obstruction to a
common-source quotient-marginal problem is a tuple of admissible local scalar
scores whose sum vanishes on the actual joint image but not on the target.
At a cumulative Goursat step this characterizes the full previous ambiguity
without constructing its primal basis.  The actual R07 joint image and score
space have not yet been computed.  No compatible lift, fake certificate or
Ihara witness is declared.

## 1. Global quotient-marginal map

Let \(k\) be a field, let

\[
 H\leq G_1\times\cdots\times G_m
\tag{1.1}
\]

be a finite joint image, and let

\[
 U_i\leq k[G_i],\qquad
 Q_i=k[G_i]/U_i.
\tag{1.2}
\]

Write

\[
 T:k[H]\longrightarrow\bigoplus_{i=1}^mQ_i
\tag{1.3}
\]

for the tuple of coordinate marginals followed by the quotient maps, and
put

\[
 V=\ker T.
\tag{1.4}
\]

Identify a functional on \(k[G_i]\) with a scalar function on \(G_i\).
A functional descends to \(Q_i\) exactly when it belongs to

\[
 U_i^\perp\leq k[G_i]^*.
\tag{1.5}
\]

### Theorem 1.1 (LOCAL-SCORE NORMAL FORM)

For \(\Phi\in k[H]^*\), the following are equivalent:

1. \(\Phi(V)=0\);
2. there are local functions

   \[
   \phi_i\in U_i^\perp
   \tag{1.6}
   \]

   such that, for every \(h=(g_1,\ldots,g_m)\in H\),

   \[
   \boxed{
   \Phi(h)=\sum_{i=1}^m\phi_i(g_i).}
   \tag{1.7}
   \]

#### Proof

Finite-dimensional duality gives

\[
 V^\perp=(\ker T)^\perp=\operatorname{im}T^*.
\tag{1.8}
\]

An element of the dual of \(\bigoplus_iQ_i\) is a tuple of functionals
\((\phi_i)_i\), each pulled back to \(k[G_i]\) and hence satisfying (1.6).
Pullback by \(T\) evaluates on a basis point \(h\) as the sum in (1.7).
Thus membership in \(\operatorname{im}T^*\) is exactly the displayed local
score form. \(\square\)

The representation by local scores need not be unique: the kernel of
\(T^*\) consists of local identities whose sum already vanishes on \(H\).
Existence, not uniqueness, is the load-bearing statement.

## 2. Complete global target obstruction

Choose representatives \(a_i\in k[G_i]\) of target classes in \(Q_i\), and
write

\[
 a=(a_1+U_1,\ldots,a_m+U_m)
\in\bigoplus_iQ_i.
\tag{2.1}
\]

### Theorem 2.1 (GLOBAL ADDITIVE-SCORE DICHOTOMY)

Exactly one of the following holds:

1. MEMBER: there is \(\eta\in k[H]\) with \(T(\eta)=a\);
2. NONMEMBER: there are \(\phi_i\in U_i^\perp\) such that

   \[
   \sum_i\phi_i(g_i)=0
   \quad\text{for every }(g_i)_i\in H,
   \tag{2.2}
   \]

   but

   \[
   \boxed{
   \sum_i\phi_i(a_i)\ne0.}
   \tag{2.3}
   \]

#### Proof

If \(a\notin\operatorname{im}T\), finite-dimensional separation gives
\(\varphi\in(\bigoplus_iQ_i)^*\) annihilating \(\operatorname{im}T\) and
not \(a\).  Write \(\varphi=(\phi_i)_i\).  Annihilation on every basis point
of \(k[H]\) is (2.2), and nonzero target pairing is (2.3).  Conversely such a
tuple would pair any putative equality \(T(\eta)=a\) both as zero and
nonzero, a contradiction. \(\square\)

The pairing in (2.3) is independent of representatives because every
\(\phi_i\) annihilates \(U_i\).  A row satisfying (2.2)--(2.3) is a complete
global obstruction, not a bounded column-generation miss.

Surjectivity of \(T\) onto the whole direct sum is equivalent to the absence
of every nonzero local-score identity (2.2).  Target-specific membership
requires only that all such identities pair to zero with the one target.

## 3. Cumulative Goursat step without a primal \(V\)-basis

At v324 step \(i\), let

\[
 H_{i-1}\leq G_1\times\cdots\times G_{i-1}
\tag{3.1}
\]

be the cumulative joint image, and let

\[
 \alpha_i:H_{i-1}\twoheadrightarrow D_i,
\qquad
 \beta_i:G_i\twoheadrightarrow D_i.
\tag{3.2}
\]

Let \(V_{i-1}\) be the full direction of all previous quotient-marginal
solutions.  V324 uses

\[
 C_i:V_{i-1}\oplus U_i\longrightarrow k[D_i],
\qquad
 C_i(v,u)=(\alpha_i)_*v-(\beta_i)_*u.
\tag{3.3}
\]

### Theorem 3.1 (GOURSAT LOCAL-SCORE DUAL)

A functional \(\lambda\in k[D_i]^*\) annihilates
\(\operatorname{im}C_i\) if and only if both:

1. there exist \(\phi_j\in U_j^\perp\) for \(1\leq j<i\) such that

   \[
   \boxed{
   \lambda(\alpha_i(g_1,\ldots,g_{i-1}))
   =\sum_{j=1}^{i-1}\phi_j(g_j)}
   \tag{3.4}
   \]

   for every \((g_1,\ldots,g_{i-1})\in H_{i-1}\); and
2. the new-coordinate pullback is locally admissible:

   \[
   \boxed{\lambda\circ\beta_i\in U_i^\perp.}
   \tag{3.5}
   \]

#### Proof

V324 (5.2) says that \(\lambda\) annihilates \(\operatorname{im}C_i\)
exactly when

\[
 \alpha_i^*\lambda\in V_{i-1}^\perp,
\qquad
 \beta_i^*\lambda\in U_i^\perp.
\tag{3.6}
\]

Apply Theorem 1.1 to the first condition.  Its local-score expression is
(3.4), while the second condition is (3.5). \(\square\)

Consequently the v324 prefix mismatch \(d_i\) is MEMBER exactly when

\[
 \lambda(d_i)=0
\tag{3.7}
\]

for every solution of (3.4)--(3.5).  One solution with nonzero pairing is
the complete cumulative NONMEMBER certificate.

This avoids constructing \(V_{i-1}\), \(Z_j\), or every rectangle column on
the dual route.  V325 remains the sparse primal/independent-checker
alternative.

## 4. Prefix-corrected cyclic local scores

For the R07 ambiguity

\[
 U_j=\epsilon_jK_{r_j}p_j^{-1},
\tag{4.1}
\]

v315 gives the exact local admissibility condition on
\(\phi_j:G_j\to k\):

\[
 \boxed{
 \sum_{g\in C}\phi_j(gp_j^{-1})=0}
\tag{4.2}
\]

for every orbit \(C\) of right multiplication by
\(\langle r_j\rangle\).

Therefore every variable in (2.2) or (3.4) is a scalar function subject only
to explicit prefix-twisted orbit equations.  No quotient basis \(Q_j\) need
be materialized.  At the new Goursat coordinate, v323 can further reduce
(3.5) to quotient-orbit equations using the order multiplicity
\(|\langle r_i\rangle\cap\ker\beta_i|\).

The complete finite dual system is thus:

1. prefix-twisted orbit sums in each local context;
2. one additive-score identity on the actual joint image;
3. one nonzero target or Goursat-defect pairing.

All occurrence tags remain separate even if two context maps have the same
underlying group image.

## 5. Column generation with a complete stopping certificate

Equation (2.2) has one row for every \(h\in H\).  A dual solver may begin
with a subset of joint-image rows, solve for candidate local scores, and ask
for a violating \(h\):

\[
 \sum_i\phi_i(g_i)\ne0.
\tag{5.1}
\]

Adding such an \(h\) is exact dual row generation.  A positive target
separation found before all joint rows are certified is only a candidate.
A complete NONMEMBER requires either:

1. exhaustive traversal of \(H\);
2. a group-theoretic proof that the additive score is zero on generators
   and that the property is stable under their multiplication; or
3. another authenticated complete identity classifier.

The sum of arbitrary local functions is not generally a group homomorphism,
so generator checks alone are invalid unless stability is separately
proved.  This guards against promoting a finite prefix separator.

On MEMBER, primal elimination or v324--v325 returns literal coefficient
ancestry.  On NONMEMBER, the local score tuple and complete joint-image
identity are independently replayable.

## 6. Cofinal consequence

At level \(n\), let \(T_n\) and \(a_n\) be the complete finite
common-source marginal problem.  If every local-score identity satisfying
(2.2) has zero pairing with \(a_n\), Theorem 2.1 proves the finite solution
set nonempty.  If this holds at every matched cofinal level and the original
maps and target classes reduce naturally, v313 finite-fibre compactness
gives one compatible completed coefficient.

A uniform symbolic classification of all local-score identities can prove
these levelwise conditions at once.  A single finite level or a bounded
identity prefix cannot.

The theorem addresses only the linear endpoint/common-source problem.
Nonlinear weighted or retract saturation, formation, settlement and
perfect-core accepted sets remain separate.

## 7. Fixed frontier

The local-score normal form, global target dichotomy, cumulative Goursat
dual and cyclic local equations are paper proofs.  The actual R07 joint
image rows, local-score identity space and target pairings are not computed.
A compatible cofinal lift, fake certificate and Ihara witness remain absent.

R07_COMMON_SOURCE_LOCAL_SCORE_DUAL_V329_PAPER_GRADE
