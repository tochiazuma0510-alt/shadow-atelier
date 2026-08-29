# R07 elementary-abelian H1 matrix certificate (v366)

Author: Sol / 2026-08-30

Status: paper theorem making the v365 relative-kernel-freeness gate directly
executable.  For an elementary-abelian relative kernel, the complete first
homology group is the kernel modulo image of two explicit block matrices
built only from the marked action matrices.  It gives both a primal free-
module basis certificate and a dual nonzero-homology certificate.  No actual
A4 action owner is yet substituted, so no compatible lift, fake certificate
or Ihara witness is declared.  `verified=false`.

## 1. The first two matrices of the product resolution

Let

\[
 K=\langle z_1,\ldots,z_t\rangle\cong(C_p)^t,
 \qquad R=\mathbf F_p[K],
 \qquad T_i=z_i-1.
\tag{1.1}
\]

Let \(N\) be a finite left \(R\)-module.  Write the same symbols \(T_i\)
for their commuting nilpotent action matrices on the underlying
\(\mathbf F_p\)-space of \(N\).  Thus

\[
 T_i^p=0,qquad T_iT_j=T_jT_i.
\tag{1.2}
\]

Define

\[
 d_1:N^t\longrightarrow N,
 \qquad
 d_1(n_1,\ldots,n_t)=\sum_{i=1}^tT_in_i.
\tag{1.3}
\]

Let

\[
 C_2=N^t\oplus N^{\binom t2}.
\tag{1.4}
\]

Denote the first \(t\) summands by \(u_i(N)\), and the remaining summands
by \(u_{ij}(N)\) for \(i<j\).  Define

\[
 \begin{aligned}
 d_2(u_i(n))&=e_i(T_i^{p-1}n),\\
 d_2(u_{ij}(n))&=e_i(T_jn)-e_j(T_in).
 \end{aligned}
\tag{1.5}
\]

Commutativity and (1.2) give \(d_1d_2=0\).

### Theorem 1.1 (ELEMENTARY-ABELIAN H1 MATRIX)

The matrices (1.3)--(1.5) compute the complete first group homology:

\[
 \boxed{
 H_1(K,N)=\ker d_1/\operatorname {im}d_2.}
\tag{1.6}
\]

#### Proof

For one cyclic factor \(C_p=\langle z_i\rangle\), use the standard
periodic free resolution of the trivial right module.  Its first two
differentials are right multiplication by

\[
 z_i-1=T_i,
 \qquad
 1+z_i+\cdots+z_i^{p-1}=T_i^{p-1}
\tag{1.7}
\]

in characteristic \(p\).  Tensor the \(t\) periodic resolutions over
\(\mathbf F_p\) and take the total complex.  This is a free right
\(R\)-resolution of the trivial module.  Total degrees zero, one and two
are respectively

\[
 R,qquad R^t,qquad R^t\oplus R^{\binom t2}.
\tag{1.8}
\]

The unary degree-two terms give the first formula in (1.5).  The tensor
differential with its Koszul sign gives the commuting-pair formula, up to
simultaneously reversing the harmless sign of a pair generator.  Tensoring
this free resolution over \(R\) with \(N\) gives exactly (1.3)--(1.5), and
first homology gives (1.6). \(\square\)

If \(n=\dim_{\mathbf F_p}N\), ordinary ranks give the audit identity

\[
 \boxed{
 \dim H_1(K,N)=tn-\operatorname {rank}d_1-operatorname {rank}d_2.}
\tag{1.9}
\]

The inclusion \(\operatorname {im}d_2\subseteq\ker d_1\) must be replayed;
it is not inferred from two reported ranks.

## 2. Complete positive and negative certificates

### Proposition 2.1 (PRIMAL RELATIVE-FREE BASIS)

Suppose \(n=q p^t\).  Vectors \(b_1,\ldots,b_q\in N\) form an
\(R\)-basis if and only if the \(n\) vectors

\[
 \boxed{
 T_1^{a_1}\cdots T_t^{a_t}b_s,
 \quad 1\leq s\leq q,
 \quad 0\leq a_i<p}
\tag{2.1}
\]

form an \(\mathbf F_p\)-basis of \(N\).

#### Proof

The monomials \(T_1^{a_1}\cdots T_t^{a_t}\), with
\(0\leq a_i<p\), are the standard \(\mathbf F_p\)-basis of

\[
 R\cong
 \mathbf F_p[T_1,\ldots,T_t]/(T_1^p,\ldots,T_t^p).
\]

Thus the \(R\)-linear map \(R^q\to N\) sending the standard generators
to the \(b_s\) is an isomorphism exactly when (2.1) is a vector-space
basis. \(\square\)

This is the shortest positive v365 certificate.  A checker reconstructs all
monomial orbit columns in fixed lexicographic exponent order and replays one
full-rank echelon.  The certificate also proves \(H_1(K,N)=0\) by v365.

### Proposition 2.2 (DUAL NONFREE CERTIFICATE)

A pair

\[
 c\in N^t,qquad \lambda\in(N^t)^*
\tag{2.2}
\]

satisfying

\[
 \boxed{
 d_1c=0,qquad
 \lambda d_2=0,qquad
 \lambda(c)\ne0}
\tag{2.3}
\]

proves that \([c]\ne0\) in \(H_1(K,N)\).  Hence \(N\) is not free over
\(R\), and under v365's source-free and leading-onto hypotheses the named
base-change saturation defect \(S_1\) is nonzero.

#### Proof

The first equality puts \(c\) in \(\ker d_1\).  The second says that
\(\lambda\) annihilates \(\operatorname {im}d_2\), while the third says it
does not annihilate \(c\).  Therefore \(c\notin\operatorname {im}d_2\),
which proves the claim by (1.6). \(\square\)

This is a genuine negative result for that base-change route, not a proof
that no R07 witness exists.  Failure of a bounded search to produce either
(2.1) or (2.3) is UNKNOWN.

## 3. The R07 p=3 specialization

At the first R07 relative Frattini edge,

\[
 K\cong(C_3)^t,
 \qquad T_i^3=0.
\tag{3.1}
\]

Thus the physical matrices are

\[
 \boxed{
 \begin{aligned}
 d_1(n_1,\ldots,n_t)&=\sum_iT_in_i,\\
 d_2(u_i(n))&=e_i(T_i^2n),\\
 d_2(u_{ij}(n))&=e_i(T_jn)-e_j(T_in).
 \end{aligned}}
\tag{3.2}
\]

They require only the ordered A4 kernel basis and the marked action of each
\(z_i\) on the actual codomain.  No multiplication table of the full crossed
group algebra is needed.  For each packaged v361 map \(G\) or \(H\), a
complete finite receipt now has the following strict decision order:

1. authenticate that the source restriction to \(K\) is free;
2. compute and independently replay leading surjectivity;
3. if the codomain is visibly a raw full-action free module, record its
   canonical coset/coordinate \(R\)-basis;
4. otherwise return either the orbit-monomial basis (2.1) or the dual class
   (2.3); and
5. on the positive branch, use v365's degree-at-most-\(2t\)
   relative-linear Neumann section to serialize the all-depth base-change
   isomorphisms.

The producer and checker should use different pivot orders for (1.9).  Both
must reconstruct \(T_i\) from the marked action, test all commuting and
cube-zero identities, and bind every vector to the actual source/codomain
owner.  A dimension divisible by \(3^t\) is necessary for freeness but is
not a substitute for (2.1) or zero homology.

## 4. Exact advance and remaining boundary

V365's relative-kernel criterion is no longer an abstract projectivity
question: v366 supplies a complete finite primal/dual certificate using only
marked action matrices.  What remains unavailable is the positive A4 action
owner and the exact physical `G`/`H` source/codomain packaging on which to
run it.  Leading surjectivity and the subsequent actual common-word Jacobian
are still separate computations.

```text
H1(K,N) BLOCK-MATRIX FORMULA:                    PAPER PROOF
PRIMAL R-FREE ORBIT-MONOMIAL BASIS:              PAPER PROOF
DUAL NONZERO-H1 / NONFREE CERTIFICATE:            PAPER PROOF
R07 p=3 MATRIX SPECIALIZATION:                    PAPER PROOF
ACTUAL A4 ACTION MATRICES:                        RUNNING / NOT RETURNED
ACTUAL G/H MODULE OWNER BINDING:                  NOT MATERIALIZED
ACTUAL bar-G / bar-H LEADING ONTO:                NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:           NOT CONSTRUCTED
```

`R07_ELEMENTARY_ABELIAN_H1_MATRIX_CERTIFICATE_V366_PAPER_GRADE`
