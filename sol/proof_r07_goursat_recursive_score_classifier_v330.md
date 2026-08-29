# R07 recursive Goursat local-score identity classifier (v330)

Author: Sol / 2026-08-29

Status: paper theorem completing the finite stopping rule left open in v329.
An additive local-score identity on a cumulative joint image can be certified
recursively from Goursat kernel invariance and quotient-section values.  The
classifier never has to enumerate the new fibre-product group.  Combined with
the prefix-corrected orbit equations, it gives a complete finite dual
MEMBER/NONMEMBER decision for an authenticated R07 marginal target.  The
actual R07 joint image, Goursat kernels, local scores and target pairing have
not been computed.  No compatible lift, fake certificate or Ihara witness is
declared.  `verified=false`.

## 1. A two-factor fibre identity needs only fibre invariance and quotient values

Let \(k\) be a field and let

\[
 A\mathrel{\mathop{\twoheadrightarrow}^{\alpha}}D,
 \qquad
 B\mathrel{\mathop{\twoheadrightarrow}^{\beta}}D
\tag{1.1}
\]

be surjective maps of finite groups.  Put

\[
 H=A\times_D B
   =\{(a,b):\alpha(a)=\beta(b)\}.
\tag{1.2}
\]

Choose set sections \(s_A:D\to A\) and \(s_B:D\to B\).  For arbitrary
functions \(F:A\to k\) and \(f:B\to k\), write

\[
 Z_{F,f}(a,b)=F(a)+f(b).
\tag{1.3}
\]

### Theorem 1.1 (FIBRE-STAR IDENTITY CRITERION)

The following are equivalent.

1. \(Z_{F,f}=0\) on all of \(H\).
2. The three finite conditions hold:

   \[
   \begin{aligned}
   F(an)&=F(a)
       &&(a\in A, n\in\ker\alpha),\\
   f(br)&=f(b)
       &&(b\in B, r\in\ker\beta),\\
   F(s_A(d))+f(s_B(d))&=0
       &&(d\in D).
   \end{aligned}
   \tag{1.4}
   \]

Equivalently, it is enough to test one base pair in every quotient fibre and
the two stars through that pair; no other pair of the cartesian fibre is
needed.

#### Proof

Assume (1).  If \(n\in\ker\alpha\), then both
\((a,s_B(\alpha(a)))\) and
\((an,s_B(\alpha(a)))\) lie in \(H\).  Subtracting their two zero equations
gives \(F(an)=F(a)\).  The same argument gives the second line of (1.4), and
the section pair gives the third.

Conversely let \((a,b)\in H\) and put
\(d=\alpha(a)=\beta(b)\).  The first two lines of (1.4) imply

\[
 F(a)=F(s_A(d)),\qquad f(b)=f(s_B(d)).
\tag{1.5}
\]

The last line of (1.4) then gives \(F(a)+f(b)=0\).  \(\square\)

If \(S_A,S_B\) are group-generating sets of the two kernels, the first two
lines need only be tested for \(n\in S_A\) and \(r\in S_B\).  Repeated right
multiplication proves invariance under every kernel word.  This is a valid
generator test because the tested property is fibre invariance and is stable
under multiplication; it is not the invalid assertion that an arbitrary
score sum is a homomorphism.

## 2. Recursive classifier on a cumulative Goursat chain

Let

\[
 H_i=H_{i-1}\times_{D_i}G_i
\tag{2.1}
\]

be the cumulative Goursat chain of v322, with quotient maps

\[
 \alpha_i:H_{i-1}\twoheadrightarrow D_i,
 \qquad
 \beta_i:G_i\twoheadrightarrow D_i.
\tag{2.2}
\]

Choose finite group-generating rosters

\[
 S_i^L\subseteq N_i^L:=\ker\alpha_i,
 \qquad
 S_i^R\subseteq N_i^R:=\ker\beta_i,
\tag{2.3}
\]

and quotient sections \(s_i^L,s_i^R\).  For local functions
\(\phi_j:G_j\to k\), put

\[
 F_i(g_1,\ldots,g_i)=\sum_{j=1}^i\phi_j(g_j)
 \quad\text{on }H_i.
\tag{2.4}
\]

Define a recursive certificate \({\sf Zero}_i(\phi_1,\ldots,\phi_i)\).

- At \(i=1\), it consists of the equations
  \(\phi_1(g)=0\) for every \(g\in G_1\).
- At \(i\ge2\), it consists of:

  1. for every \(n=(n_1,\ldots,n_{i-1})\in S_i^L\), the recursive
     certificate

     \[
     {\sf Zero}_{i-1}
       (\Delta_{n_1}\phi_1,\ldots,
        \Delta_{n_{i-1}}\phi_{i-1}),
     \qquad
     \Delta_u\phi(g)=\phi(gu)-\phi(g);
     \tag{2.5}
     \]

  2. the equations

     \[
     \phi_i(gr)=\phi_i(g)
     \quad(g\in G_i, r\in S_i^R);
     \tag{2.6}
     \]

  3. for every \(d\in D_i\), the section equation

     \[
     \sum_{j<i}\phi_j((s_i^L(d))_j)
       +\phi_i(s_i^R(d))=0.
     \tag{2.7}
     \]

All entries of \(n\) and \(s_i^L(d)\) are retained in their original tagged
coordinates.  No isomorphic occurrences are identified.

### Theorem 2.1 (RECURSIVE GOURSAT SCORE CLASSIFIER)

\[
 \boxed{
 {\sf Zero}_i(\phi_1,\ldots,\phi_i)
 \quad\Longleftrightarrow\quad
 F_i=0\text{ on }H_i.}
\tag{2.8}
\]

#### Proof

Induct on \(i\).  The base case is the definition.  For \(i\ge2\), apply
Theorem 1.1 with

\[
 A=H_{i-1},\quad B=G_i,\quad F=F_{i-1},\quad f=\phi_i.
\tag{2.9}
\]

For \(n\in N_i^L\), right multiplication in \(H_{i-1}\) gives

\[
 F_{i-1}(hn)-F_{i-1}(h)
   =\sum_{j<i}(\Delta_{n_j}\phi_j)(h_j).
\tag{2.10}
\]

By induction, (2.5) says exactly that (2.10) vanishes for all
\(h\in H_{i-1}\).  Testing the generating roster therefore gives invariance
under all of \(N_i^L\).  Equation (2.6) gives the corresponding invariance
under \(N_i^R\), and (2.7) is the quotient-section equation.  These are
precisely the three conditions of Theorem 1.1.  \(\square\)

The recursive equations are linear in all values of the \(\phi_j\).  They
may be canonicalized and duplicate rows removed.  Their completeness does
not depend on a score being a homomorphism and does not require traversal of
the newly formed set \(H_i\), whose fibres may be much larger than the input
groups and kernels.

## 3. Complete dual decision for the quotient-marginal target

Retain v329's local ambiguity spaces

\[
 U_j\le k[G_j],\qquad Q_j=k[G_j]/U_j,
\tag{3.1}
\]

and target representatives \(a_j\in k[G_j]\).  Introduce the values of local
scores \(\phi_j:G_j\to k\) as finite scalar variables and impose:

1. local admissibility \(\phi_j\in U_j^\perp\);
2. the complete recursive equations
   \({\sf Zero}_m(\phi_1,\ldots,\phi_m)\); and
3. the normalized target equation

   \[
   \sum_j\phi_j(a_j)=1.
   \tag{3.2}
   \]

### Theorem 3.1 (FINITE SCORE-DUAL DICHOTOMY)

The system (1)--(3) has a solution if and only if the prescribed target is
NONMEMBER in the common-source marginal image.  If it is inconsistent, the
target is MEMBER.

#### Proof

Theorem 2.1 identifies the second group of equations exactly with v329
equation (2.2), while the first group makes every score descend to \(Q_j\).
Over a field, every nonzero target pairing can be scaled to one.  V329
Theorem 2.1 now gives both directions and the dichotomy.  \(\square\)

For the R07 spaces

\[
 U_j=\epsilon_jK_{r_j}p_j^{-1},
\tag{3.3}
\]

the first group is exactly the prefix-twisted orbit-sum equations of v315
and v329.  Thus all rows of the complete dual system are explicit from:

- local right-orbit rosters and mandatory prefixes;
- cumulative Goursat kernel generators and quotient sections; and
- the one actual target tuple.

A producer may solve this dual system directly.  An independent checker can
instead use v324--v325's sparse primal affine DP.  If the dual system is
inconsistent, primal finite-dimensional elimination returns the literal
MEMBER ancestry; inconsistency alone is not used as a word certificate.

## 4. Cumulative overlap equations are covered by the same classifier

V329 Theorem 3.1 asks whether, for
\(\lambda\in k[D_i]^*\),

\[
 \lambda\circ\alpha_i
   =\sum_{j<i}\phi_j
 \quad\text{on }H_{i-1}.
\tag{4.1}
\]

This is again a zero-score identity: adjoin the graph coordinate

\[
 \operatorname{Graph}(\alpha_i)
 \le H_{i-1}\times D_i
\tag{4.2}
\]

with local score \(-\lambda\) on \(D_i\), and apply Theorem 2.1 to the
resulting cumulative chain.  The last right kernel is trivial and the left
kernel is \(\ker\alpha_i\).  Together with
\(\lambda\circ\beta_i\in U_i^\perp\), this gives a complete finite
constraint system for every annihilator of v324's map \(C_i\), without
constructing \(V_{i-1}\) or enumerating \(H_i\).

Therefore a Goursat prefix defect \(d_i\) is NONMEMBER exactly when this
finite graph-score system has a normalized solution
\(\lambda(d_i)=1\).  Otherwise finite duality proves MEMBER and the sparse
primal route recovers its correction ancestry.

## 5. Certificate and cost boundary

An acceptable negative certificate contains:

1. the authenticated ordered joint-image generators and cumulative Goursat
   quotient data;
2. independently checked generating rosters for every \(N_i^L,N_i^R\);
3. the chosen quotient sections with direct map replay;
4. every local orbit-sum row, recursive difference row and section row;
5. the local score values and all zero equations; and
6. the normalized target pairing.

The checker need not reproduce the producer's elimination order.  It
rebuilds the equation roster from the group data, verifies the kernel
generators generate the complete kernels, and evaluates the supplied score.
A mere list of joint generators, without kernel generation and recursive
invariance, is insufficient.

This theorem removes the potentially multiplicative enumeration of each new
fibre product.  It does not promise that the canonicalized recursive system
is small: repeated difference constraints may still be large, and a resource
stop is `UNKNOWN_RESOURCE`.  What is now finite and complete is the stopping
criterion itself.

## 6. Cofinal boundary

At every finite matched level, Theorem 3.1 decides the actual linear
common-source marginal target once the authenticated Goursat data are
available.  If the target is MEMBER at every level, v313's finite-fibre
compactness gives a compatible completed coefficient.  Alternatively,
natural kernel rosters, sections and primal inverses make the v322/v324
selector commute with reduction and construct it directly.

The recursive classifier does not prove that the actual target pairs to zero
with every score at all levels; those are the finite calculations or a future
symbolic identity theorem.  It also does not discharge nonlinear weighted or
retract saturation, formation, settlement, or perfect-core gates.

```text
ADDITIVE SCORE ZERO ON A FIBRE PRODUCT:             FIBRE-STAR CRITERION
GENERATOR CHECK FOR KERNEL INVARIANCE:              COMPLETE
CUMULATIVE JOINT-IMAGE ZERO IDENTITY:               RECURSIVE CLASSIFIER
PREFIX-CORRECTED R07 LOCAL ADMISSIBILITY:           EXPLICIT ORBIT EQUATIONS
ACTUAL FINITE TARGET MEMBER/NONMEMBER STOPPING:     COMPLETE GIVEN AUTHORITY
FULL H_i POINT ENUMERATION:                         NOT REQUIRED
ACTUAL R07 GOURSAT DATA / SCORE SOLVE:              NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:    NOT CONSTRUCTED
```

`R07_GOURSAT_RECURSIVE_SCORE_CLASSIFIER_V330_PAPER_GRADE`
