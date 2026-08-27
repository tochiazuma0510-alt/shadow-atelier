# R07 boundary-image relative freeness and factored trace v180

Author: Sol / 2026-08-28

Status: paper theorem and computational reduction.  This note turns the
relative-projective gate of v179 into tests on either the complete boundary
image or its syzygy, and factors the first Frattini trace operator without
enumerating an elementary-abelian kernel.  The required R07 ranks and action
matrices have not yet been computed.  No lift, fake certificate, or Ihara
witness is declared.

## 1. Three equivalent relative-freeness tests

Let \(k=\mathbf F_3\), let \(K\) be a finite 3-group, and put
\(A=kK\).  Consider an exact presentation segment of finite left
\(A\)-modules

\[
 0\longrightarrow S\longrightarrow C_2
 \xrightarrow{D_2} C_1\longrightarrow W\longrightarrow0,
\tag{1.1}
\]

where \(C_1,C_2\) are finite free, \(I=\operatorname{im}D_2\), and
\(S=\ker D_2\).  In the R07 application, all context tags are retained and
\(I\) is the span of the complete translated two-PB3/eleven-PB4 boundary
roster.

### Theorem 1.1 (BOUNDARY--QUOTIENT--SYZYGY FREE EQUIVALENCE)

The following are equivalent:

\[
 \boxed{
 W\text{ is }A\text{-free}
 \Longleftrightarrow
 I\text{ is }A\text{-free}
 \Longleftrightarrow
 S\text{ is }A\text{-free}.}
\tag{1.2}
\]

#### Proof

The finite group algebra \(A=kK\) is symmetric, hence self-injective.
Because \(K\) is a 3-group in characteristic three, \(A\) is also local;
finite projective modules are therefore free.

First use

\[
 0\to I\to C_1\to W\to0.
\tag{1.3}
\]

If \(W\) is free, it is projective, so the surjection splits and \(I\) is a
direct summand of the free module \(C_1\).  Thus \(I\) is projective and
free.  Conversely, if \(I\) is free, it is projective and therefore
injective because \(A\) is self-injective.  Its inclusion into \(C_1\)
splits, making \(W\) a direct summand of \(C_1\), hence projective and free.

Apply the same argument to

\[
 0\to S\to C_2\to I\to0
\tag{1.4}
\]

to obtain \(S\) free if and only if \(I\) is free. \(\square\)

This equivalence is finite-level only.  It does not assert that a compatible
splitting has already been chosen through the whole inverse system.

## 2. Generator-only coinvariant calculation

V179 Proposition 3.1 tests an \(A\)-module \(M\) by

\[
 \dim_kM=|K|\dim_k(M/J_KM).
\tag{2.1}
\]

The space \(J_KM\) does not require enumeration of every element of \(K\).

### Lemma 2.1 (AUGMENTATION SPAN FROM GROUP GENERATORS)

If \(K=\langle s_1,\ldots,s_t\rangle\), then

\[
 \boxed{
 J_KM=\sum_{i=1}^t(s_i-1)M.}
\tag{2.2}
\]

#### Proof

The augmentation ideal of \(kK\) is generated as a left ideal by
\(s_i-1\).  Indeed,

\[
 ab-1=(a-1)+a(b-1),
\tag{2.3}
\]

and

\[
 a^{-1}-1=-a^{-1}(a-1).
\tag{2.4}
\]

Induction on a word in the \(s_i^{\pm1}\) expresses every \(g-1\) in the
left ideal they generate.  Acting on \(M\) proves (2.2). \(\square\)

Hence exact matrices for only a registered generating set of \(K\) suffice
to compute the coinvariant dimension.  Combining Theorem 1.1, Lemma 2.1,
and v179 Proposition 3.1 gives three interchangeable complete certificates:

\[
 \dim M=|K|\dim M_K,
 \qquad M\in\{W,I,S\}.
\tag{2.5}
\]

One may choose whichever of the quotient, image, or syzygy has the smallest
exact matrix representation.  The complete boundary roster remains
load-bearing in all three versions.

## 3. Factoring the elementary-abelian trace

At the first relative Frattini successor, the new kernel is elementary
abelian.  Let

\[
 K=\langle s_1,\ldots,s_t\rangle\cong(C_3)^t.
\tag{3.1}
\]

On any \(kK\)-module, including the scalar dual with its contragredient
action, let

\[
 N_K=\sum_{a\in K}a.
\tag{3.2}
\]

### Proposition 3.1 (FACTORED FRATTINI TRACE)

In characteristic three,

\[
 \boxed{
 N_K=\prod_{i=1}^t(1+s_i+s_i^2)
     =\prod_{i=1}^t(s_i-1)^2.}
\tag{3.3}
\]

#### Proof

Every element of \(K\) has a unique expression
\(s_1^{e_1}\cdots s_t^{e_t}\), \(0\leq e_i<3\).  Expanding the first
product therefore gives (3.2).  The generators commute.  In characteristic
three,

\[
 (s_i-1)^2=s_i^2-2s_i+1=s_i^2+s_i+1,
\tag{3.4}
\]

which proves the second equality. \(\square\)

Thus the v178/v179 trace equation

\[
 N_K\varphi'=\varphi\circ r
\tag{3.5}
\]

can be formed by \(2t\) sparse generator actions rather than a sum of
\(3^t\) action matrices.  This factorization does not assume freeness.  It
therefore also provides the exact particular-class test when the freeness
criterion fails: solve (3.5) using the factored operator, and retain either
a preimage or a complete left-nullspace obstruction.

The order in (3.3) is harmless only because the first Frattini kernel is
elementary abelian.  At a nonabelian later 3-kernel, one must use an ordered
subnormal-series factorization with explicit coset representatives; the
commutative product above may not be copied blindly.

## 4. Parallel certificate layout

The expensive portion is the construction of the complete boundary image
and occurrence correlation.  V176 permits exact support/occurrence shards,
followed by coefficientwise merge before zero deletion and canonical pivot
insertion.  After that serial merge, the relative-freeness/trace certificate
can be kept small:

1. exact dimensions of \(C_2,I,C_1,W,S\);
2. the action matrices of \(s_1,\ldots,s_t\) on the chosen smallest module
   among \(W,I,S\);
3. the rank of the horizontally concatenated matrices \(s_i-1\), giving
   \(\dim M_K\) by Lemma 2.1;
4. the equality or inequality in (2.5);
5. the factored trace image of every proposed successor dual; and
6. on failure of particular trace membership, a dual row annihilating the
   full image of (3.3) but not \(\varphi\circ r\).

Producer and independent checker should partition the expensive boundary
correlation differently, but both must replay the same post-merge canonical
module.  Shard-local pivots or averaging cannot replace that merge.

## 5. Consequence for the explicit lift route

If one of the equivalent freeness certificates (1.2) holds at every rung,
v179 constructs trace-compatible scalar duals recursively with no later dual
search.  If a compatible completed free basis is proved, v179 Section 5 gives
the dual in closed form at once.  At the first successor, Proposition 3.1
also makes the weaker particular-dual test practical even if freeness fails.

None of these statements alone proves that the corrected residual lies in
the cyclic module of the original target, or that the resulting word passes
the nonlinear onto/marking/formation gates.  Those are still the multiplier
and admissibility hypotheses of v174--v175.

## 6. Fixed frontier

```text
BOUNDARY/QUOTIENT/SYZYGY FREE EQUIVALENCE:       PAPER_PROOF
GENERATOR-ONLY COINVARIANT TEST:                 PAPER_PROOF
ELEMENTARY-ABELIAN FACTORED TRACE:               PAPER_PROOF
COMPLETE SHARDED BOUNDARY CORRELATION:            IMPLEMENTATION IN PROGRESS
R07 FIRST SUCCESSOR FREENESS OR TRACE PREIMAGE:   NOT COMPUTED
R07 ALL-RUNG RELATIVE PROJECTIVITY:               NOT PROVED
ACTUAL MULTIPLIER / NONLINEAR SIDE GATES:          OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA:            NOT DECLARED
```

`R07_BOUNDARY_IMAGE_RELATIVE_FREENESS_V180_PAPER_GRADE`
