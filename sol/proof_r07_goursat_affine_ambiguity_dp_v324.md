# R07 Goursat affine-ambiguity dynamic selector (v324)

Author: Sol / 2026-08-29

Status: paper theorem strengthening v322--v323.  Instead of correcting a
new Goursat overlap only with the new coordinate ambiguity, it retains the
entire affine direction of all earlier joint couplings.  The resulting
recursion is an exact finite linear decision, never a greedy relaxation.
Right inverses give a closed selector; actual-class ancestry is enough for
one target.  The actual R07 joint images and targets have not yet been
authenticated.  No compatible lift, fake certificate or Ihara witness is
declared.

## 1. Quotient-marginal solution spaces

Let \(k\) be a field and let

\[
 H\leq G_1\times\cdots\times G_m
\tag{1.1}
\]

be a finite subdirect product.  Fix an order of the factors and use the
cumulative Goursat data of v322:

\[
 H_i=\operatorname{pr}_{1,\ldots,i}(H)
     =H_{i-1}\times_{D_i}G_i,
\qquad
 \alpha_i:H_{i-1}\twoheadrightarrow D_i,
\quad
 \beta_i:G_i\twoheadrightarrow D_i.
\tag{1.2}
\]

For every coordinate choose a linear ambiguity space

\[
 U_i\leq k[G_i],\qquad Q_i=k[G_i]/U_i,
\tag{1.3}
\]

and a representative \(a_i\in k[G_i]\) of the prescribed class in \(Q_i\).
Let

\[
 P_i:k[H_i]\longrightarrow\bigoplus_{j=1}^ik[G_j]
\tag{1.4}
\]

be the coordinate-marginal map and define the complete prefix solution set

\[
 \mathcal A_i=
 \{\eta\in k[H_i]:
       (\operatorname{pr}_j)_*\eta\in a_j+U_j
       \text{ for }1\leq j\leq i\}.
\tag{1.5}
\]

It is either empty or an affine subspace.  Whenever it is nonempty, write

\[
 \mathcal A_i=\eta_i^0+V_i,
\qquad
 V_i=\ker\left(
 k[H_i]\longrightarrow\bigoplus_{j=1}^iQ_j\right).
\tag{1.6}
\]

The direction \(V_i\) is canonical; only its displayed basepoint depends on
choices.  It contains changes of earlier local representatives and changes
of their joint correlation which preserve every prescribed quotient class.

At \(i=1\),

\[
 \eta_1^0=a_1,\qquad V_1=U_1.
\tag{1.7}
\]

For the R07 zero first-shadow marginal, take \(a_1=0\) and \(U_1=0\) when
that marginal is imposed exactly.

## 2. One exact affine Goursat step

Assume

\[
 \mathcal A_{i-1}=\eta_{i-1}^0+V_{i-1}\ne\varnothing.
\tag{2.1}
\]

Define the base mismatch

\[
 d_i=(\alpha_i)_*\eta_{i-1}^0-(\beta_i)_*a_i
 \in k[D_i]
\tag{2.2}
\]

and the cumulative ambiguity map

\[
 C_i:V_{i-1}\oplus U_i\longrightarrow k[D_i],
\qquad
 C_i(v,u)=(\alpha_i)_*v-(\beta_i)_*u.
\tag{2.3}
\]

### Theorem 2.1 (EXACT CUMULATIVE GOURSAT OBSTRUCTION)

\[
 \boxed{
 \mathcal A_i\ne\varnothing
 \quad\Longleftrightarrow\quad
 -d_i\in\operatorname{im}C_i.}
\tag{2.4}
\]

If \(C_i(v_i,u_i)=-d_i\), then

\[
 x_i=\eta_{i-1}^0+v_i,\qquad
 y_i=a_i+u_i
\tag{2.5}
\]

have equal \(D_i\)-pushforwards.  Applying the v317 two-factor gluing
section gives a basepoint

\[
 \boxed{
 \eta_i^0=G_i^{\rm fib}(x_i,y_i)\in\mathcal A_i.}
\tag{2.6}
\]

#### Proof

If \(\eta\in\mathcal A_i\), let \(x,y\) be its two factor marginals in
\(k[H_{i-1}]\) and \(k[G_i]\).  Then

\[
 x=\eta_{i-1}^0+v,\qquad y=a_i+u
\tag{2.7}
\]

for some \(v\in V_{i-1}\), \(u\in U_i\).  Because
\(H_i=H_{i-1}\times_{D_i}G_i\), their overlap marginals agree.  Substitution
in that equality gives

\[
 d_i+C_i(v,u)=0,
\tag{2.8}
\]

proving necessity.  Conversely a solution of (2.8) makes the pair (2.5)
compatible.  V317 Lemma 1.1 glues it without changing either factor
marginal, so all first \(i\) quotient classes have the prescribed values.
\(\square\)

Unlike v322's new-coordinate-only sufficient test, (2.4) allows the entire
earlier affine solution to move.  Therefore a NONMEMBER result in (2.4) is
not a bounded greedy miss: no choice of any previous coupling can pass this
prefix.

## 3. Retaining the full direction for the next step

Let

\[
 M_i:k[H_i]\longrightarrow k[H_{i-1}]\oplus k[G_i]
\tag{3.1}
\]

be the pair of factor marginals and put

\[
 Z_i=\ker M_i.
\tag{3.2}
\]

The space \(Z_i\) consists of pure correlation changes invisible in both
factor marginals.  Fix the linear v317 gluing section

\[
 S_i:
 \{(x,y):(\alpha_i)_*x=(\beta_i)_*y\}
 \longrightarrow k[H_i],
\qquad
 M_iS_i(x,y)=(x,y).
\tag{3.3}
\]

Let

\[
 E_i=\ker C_i
 =\{(v,u)\in V_{i-1}\oplus U_i:
       (\alpha_i)_*v=(\beta_i)_*u\}.
\tag{3.4}
\]

### Theorem 3.1 (AFFINE-DIRECTION RECURRENCE)

For the basepoint (2.6),

\[
 \boxed{
 V_i=Z_i\oplus S_i(E_i).}
\tag{3.5}
\]

In particular, (1.6), (2.2)--(2.6), and (3.2)--(3.5) recursively compute
the complete affine solution space at every prefix.

#### Proof

Every \(z+S_i(v,u)\) with \(z\in Z_i\) and \((v,u)\in E_i\) has earlier
factor marginal \(v\), new factor marginal \(u\), and hence zero value in
all first \(i\) quotient coordinates.  Thus the right side of (3.5) is
contained in \(V_i\).

Conversely let \(w\in V_i\).  Its factor marginals \(v,u=M_i(w)\) lie in
\(V_{i-1}\) and \(U_i\).  Since \(w\) is supported on the fibre product,
their \(D_i\)-pushforwards agree, so \((v,u)\in E_i\).  Then

\[
 w-S_i(v,u)\in\ker M_i=Z_i,
\tag{3.6}
\]

giving the reverse inclusion.  The sum is direct because \(M_i\) vanishes
on \(Z_i\) and is the identity on the image of \(S_i\). \(\square\)

The \(Z_i\) term is load-bearing for later stages.  It does nothing at the
current coordinate marginals but can have a nonzero image in a later
cumulative Goursat quotient.  Discarding it can create a false later
NONMEMBER.

## 4. Closed selector and actual-class selector

Suppose \(C_i\) has a linear right inverse

\[
 h_i:k[D_i]\longrightarrow V_{i-1}\oplus U_i,
\qquad C_ih_i=1.
\tag{4.1}
\]

Then choose

\[
 (v_i,u_i)=h_i(-d_i)
\tag{4.2}
\]

in (2.5)--(2.6), and update \(V_i\) by (3.5).

### Corollary 4.1 (FULL AFFINE GOURSAT SELECTOR)

If (4.1) is available at every step, the recursion constructs a linear
common-source selector for every tuple of local quotient classes.

Full onto is stronger than necessary.  For one actual R07 tuple it is enough
to retain one ancestry

\[
 C_i(v_i,u_i)=-d_i
\tag{4.3}
\]

at each step.  The resulting sequence of basepoints is a deterministic
actual-class selector once the sections and ancestry tie-breaks are fixed.

V322 Theorem 3.1 is the special case in which every \(v_i\) is forced to
zero and \(-(\beta_i)_*:U_i\to k[D_i]\) alone is onto.  V323 computes that
new-coordinate summand explicitly.  The present theorem can still pass when
\(\beta_i(r_i)\ne1\), because \((\alpha_i)_*V_{i-1}\) may supply the missing
directions.

## 5. Complete dual alternative

For \(\lambda\in k[D_i]^*\), the transpose of (2.3) is

\[
 C_i^*\lambda=
 \left(
   (\alpha_i)^*\lambda|_{V_{i-1}},
   -(\beta_i)^*\lambda|_{U_i}
 \right).
\tag{5.1}
\]

Therefore

\[
 \boxed{
 \lambda(\operatorname{im}C_i)=0
 \Longleftrightarrow
 \begin{cases}
  (\alpha_i)^*\lambda\in V_{i-1}^{\perp},\\
  (\beta_i)^*\lambda\in U_i^{\perp}.
 \end{cases}}
\tag{5.2}
\]

### Theorem 5.1 (CUMULATIVE DUAL DICHOTOMY)

Exactly one of the following holds:

1. MEMBER: there is ancestry (4.3);
2. NONMEMBER: there is \(\lambda\in k[D_i]^*\) satisfying (5.2) and

   \[
   \lambda(d_i)\ne0.
   \tag{5.3}
   \]

In the second case \(\mathcal A_i=\varnothing\); the row obstructs every
earlier coupling, not just the displayed basepoint.

#### Proof

This is finite-dimensional separation of \(-d_i\) from
\(\operatorname{im}C_i\), followed by Theorem 2.1.  The sign does not affect
the nonzero pairing. \(\square\)

For the R07 prefix-corrected cyclic ambiguity
\(U_i=\epsilon_iK_{r_i}p_i^{-1}\), the second line of (5.2) is exactly the
v323 quotient-orbit condition.  The first line records which overlap
functionals are already forced by all previous quotient marginals and
correlations.  Hence the only genuinely new dual survivor is a quotient row
which satisfies both conditions and pairs nontrivially with \(d_i\).

## 6. Finite computation and certificate

At a finite authenticated joint image, the exact algorithm is:

1. initialize \(\eta_1^0,V_1\) by (1.7);
2. construct the next genuine cumulative image \(H_i\), not only pairwise
   coordinate projections;
3. compute its Goursat maps \(\alpha_i,\beta_i\);
4. form \(d_i,C_i\) and return ancestry (4.3) or a complete row (5.2)--(5.3);
5. on MEMBER, glue (2.6) and retain the full direction (3.5), including
   \(Z_i\);
6. continue to all occurrence-tagged contexts; and
7. lift the final coefficient from \(k[H]\) to the finite common-source
   group algebra and replay every marginal.

The certificate records bases, maps, one primal ancestry or one dual row,
the gluing sections, and direct final marginals.  An independent checker can
rebuild the dual from (5.2) when the producer uses primal elimination, or
rebuild primal rank when the producer emits a dual.

The state size is the dimension of the cumulative direction \(V_i\), not
the number of all candidate coefficient tuples.  Sparse bases of \(Z_i\)
and \(E_i\) avoid enumerating all \(|k|^{|H_i|}\) coefficient vectors,
although construction may still require enumeration or a compact
presentation of the group basis \(H_i\).  This is a linear dynamic program,
not an exponential search over representatives.

## 7. Cofinal consequence

Apply the recurrence at every finite level of a matched cofinal tower.
There are two valid promotions.

First, if the Goursat data, gluing sections and right inverses (or selected
actual ancestries) commute with reduction, the recursion directly constructs
one compatible completed coefficient.

Second, naturality of the arbitrary sections is unnecessary for existence.
If the joint-image reductions, marginal maps, ambiguity spaces and target
classes reduce naturally, and the exact recurrence proves
\(\mathcal A_{m,n}\ne\varnothing\) at every level \(n\), then these finite
full-solution sets form the system \(X_n\) of v313.
Finite-fibre compactness gives

\[
 \varprojlim_n\mathcal A_{m,n}\ne\varnothing.
\tag{7.1}
\]

Thus stagewise exact affine feasibility is enough for a compatible measure;
one finite success is still insufficient.  The compactness route gives a
mathematical witness but not necessarily an effective next-edge formula.

The output remains a linear endpoint correction.  V319--v321's nonlinear
localized recurrence and saturation, as well as formation, settlement and
perfect-core gates, must still be discharged.

## 8. Fixed frontier

The exact cumulative affine obstruction is a paper proof.  The full
direction recurrence including invisible coupling kernels is a paper proof.
The cumulative primal/dual dichotomy and closed-selector criterion are paper
proofs.  The actual R07 cumulative groups, matrices, defects and ancestries
are not computed.  The compatible cofinal lift, fake certificate and Ihara
witness remain absent.

R07_GOURSAT_AFFINE_AMBIGUITY_DP_V324_PAPER_GRADE
