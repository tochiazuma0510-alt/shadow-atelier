# R07 nested word-section elimination after the relative-dihedral shear v98

Author: Sol / 2026-08-26

Status: paper proof obtained by combining the accumulated-kernel construction
of v64, the pro-relative-dihedral recursion of v82, the pro-$3$ onto theorem
of v94, and the literal A.18 shear of v96.  It removes compatibility of
chosen word sections as a separate hypothesis for constructing one R07
branch.  It does not prove that the actual correction equation is soluble at
every edge, and it does not declare a cofinal lift or an Ihara witness.
`verified=false`.

## 1. Actual nested correction domains

Fix a nested cofinal ladder of finite matched arity-$3/4/5$ diagrams.  At
level $n$, accumulate the exact R07 mark, both hexagons, all five printed
pentagon cofaces, and every side-gate evaluation already frozen.  Let

\[
 \Psi_n:\widehat F_2\twoheadrightarrow H_n,
 \qquad U_n=\ker\Psi_n,
 \qquad U_{n+1}\leq U_n.
\tag{1.1}
\]

For the next level write

\[
 D_{n+1,n}=\Psi_{n+1}(U_n)
 =\ker(H_{n+1}\twoheadrightarrow H_n).
\tag{1.2}
\]

To retain raw charmingness, use the actual commutator correction domain

\[
 D^{\rm com}_{n+1,n}
 =\Psi_{n+1}\bigl(U_n\cap[\widehat F_2,\widehat F_2]\bigr).
\tag{1.3}
\]

The word "actual" is load-bearing: a vector in an over-approximation of
(1.3) need not have one common-word representative.  The L3 target6 screen
tests such an over-approximation only in the safe negative direction and
therefore cannot supply the positive input below.

## 2. A compatible word section is unnecessary

Suppose a partial word $f_n$ already passes through level $n$, and suppose
an actual relation solver returns a value

\[
 d_n\in D^{\rm com}_{n+1,n}
\tag{2.1}
\]

such that replacing $f_n$ by $f_nd_n$ at the joint finite-value level kills
the next two-hexagon/literal-pentagon residual and passes the remaining
finite side gates.

### Theorem 2.1 (NESTED-SECTION-ELIMINATION)

There is a deterministic ordinary signed commutator word

\[
 c_n\in F_2\cap U_n\cap[F_2,F_2]
\tag{2.2}
\]

with $\Psi_{n+1}(c_n)=d_n$.  Choosing the shortlex-first such word at every
stage and putting

\[
 f_{n+1}=f_nc_n
\tag{2.3}
\]

produces compatible partial words.  No family of word sections
$s_n:D^{\rm com}_{n+1,n}\to F_2$ commuting with every refinement map is
required.

#### Proof

By definition of (1.3), $d_n$ has a representative in the closed
commutator subgroup which is trivial under $\Psi_n$.  Its image in the
finite group $H_{n+1}$ lies in the image of the ordinary commutator group:
for the epimorphism $F_2\to H_{n+1}$ one has

\[
 \operatorname{im}[F_2,F_2]=H_{n+1}'.
\tag{2.4}
\]

Choose an ordinary commutator representative of $d_n$.  Since its
$H_{n+1}$ value maps to the identity of $H_n$, the same word lies in
$U_n$.  Enumerating signed words with exponent sums $(0,0)$ in shortlex
order and testing the two finite equalities

\[
 \Psi_n(c)=1,
 \qquad \Psi_{n+1}(c)=d_n
\tag{2.5}
\]

therefore terminates and gives (2.2).

For $m>n$, every later correction satisfies $c_m\in U_m\leq U_n$.
Consequently reduction of every later partial word to $H_n$ equals the
reduction of $f_n$.  Thus (2.3) is compatible independently of how the
shortlex representatives at distinct stages are spelled.  This is exactly
the accumulated-kernel argument of v64, now restricted to the actual
commutator domain. $\square$

### Corollary 2.2 (convergent explicit product)

If a value $d_n$ as in (2.1) exists for every stage along the recursively
chosen branch, then

\[
 \boxed{f_\infty=f_0c_0c_1c_2\cdots}
\tag{2.6}
\]

converges in $\widehat F_2$ and has the already settled value at every
finite level.  This conclusion requires stagewise nonemptiness along the
branch, but not naturality of the spelling selector.

#### Proof

The right tail after stage $n$ lies in $U_n$, so the partial products are
Cauchy.  At each finite level the tail is eventually invisible.  Apply
completeness and continuity exactly as in v64, Theorem 3.1. $\square$

## 3. Interaction with relative dihedral and literal A.18

At one abelian diagram-chief edge, let

\[
 \omega_\rho=(h_1,h_2,r),
 \qquad \omega_{A18}=(h_1,h_2,c)
\tag{3.1}
\]

be the simultaneous theta/rho and literal printed-order residuals.  V96
gives the natural integral shear

\[
 \omega_{A18}=T_A\omega_\rho,
 \qquad
 T_A=
 \begin{pmatrix}
 1&0&0\\
 0&1&0\\
 -1&-A&1
 \end{pmatrix}.
\tag{3.2}
\]

Hence an actual common-word value $d_n$ killing the theta/rho stack kills
the literal A.18 stack after the same correction; no second realization or
pentagon-specific word section is introduced.  If a natural theta/rho
contraction is proved, v96 transports it to a natural literal contraction.
Even if the chosen finite word spellings are not natural, Theorem 2.1 still
assembles their values into one compatible branch.

The distinction is therefore:

\[
\begin{array}{ll}
\text{naturality of residual matrices/closed contraction}
 &\text{useful for proving all-stage nonemptiness at once},\\
\text{naturality of word spellings}
 &\text{not needed for compatibility of one branch}.
\end{array}
\tag{3.3}
\]

## 4. Side gates on the cofinal $3$-primary lane

For corrections chosen in (1.3), exponent sums remain zero, so raw
charmingness is preserved.  The exact R07 mark and every earlier descent or
relation evaluation were included in $\Psi_n$, so $c_n\in U_n$ preserves
them.  On the compatible finite marked $3$-group refinements above
$\Pi_4[3]$, v94 proves that every transition is a Frattini cover and current
E4 onto propagates automatically.  Thus no separate stagewise onto replay
or natural word-section theorem is load-bearing on this lane.

This does not remove formation-residual support or a genuinely new
non-$3$, mixed, or nonabelian side gate.  Such conditions must be included
in the finite accepted-value test defining (2.1).

## 5. Sharpened remaining statement

For one explicit pro-$3$ abelian branch, the following entries are now
removed as independent obstructions:

```text
COMPATIBLE SPELLING OF FINITE CORRECTIONS:  PAPER_PROOF (Theorem 2.1)
CONVERGENCE OF THE INFINITE WORD PRODUCT:   PAPER_PROOF (Corollary 2.2)
CHARMING UNDER COMMUTATOR CORRECTIONS:      PAPER_PROOF
ONTO THROUGH COFINAL 3-FRATTINI TOWER:     PAPER_PROOF (v94)
RHO TO LITERAL A18 CONVERSION:              PAPER_PROOF (v96)
```

The remaining abelian load-bearing assertion is not a choice problem.  It
is the actual-image nonemptiness statement

\[
 \boxed{
 \text{at every active edge, the theta/rho correction equation has a
 solution in }D^{\rm com}_{n+1,n}\text{ passing the finite side gates}.}
\tag{5.1}
\]

A natural class-specific contraction would prove (5.1) uniformly and give
the desired backtracking-free selector.  One successful edge does not prove
(5.1) at later edges.  Conversely, once (5.1) is proved, no further
``compatible $(c_n)$ choice'' remains: Theorem 2.1 and (2.6) construct it.
Nonabelian chief accepted-set nonemptiness is still separate.

For $g_{760}$ the immediate finite question remains the fresh target6 gate.
A cross-checked NONMEMBER kills that prefix.  MEMBER only passes an
over-approximation screen; one must then compute the actual theta/rho or
literal A.18 class and exhibit its value in (1.3).

No new finite computation, external source, or Lean proof is used here.
