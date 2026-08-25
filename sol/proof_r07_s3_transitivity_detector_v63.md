# R07 six-state transitivity detector v63

Author: Sol / 2026-08-25

Status: paper-proof candidate; `verified=false`.  The finite index-three
subgroup census used below is `cross_checked`, while the marked arithmetic
selection is `BLOCKED_UNKNOWN` and the present deductions retain their
recorded paper-proof grades.  Every assertion below about the arithmetic
subgroup uses only properties shared by both surviving candidates.  No fake
certificate or Ihara witness is asserted here.

The one-bit theorem v62 asks whether the roof image at a B4 window is the
arithmetic subgroup of order 324 or the whole 972-element group.  The
arithmetic subgroup is nonnormal.  Its three-coset action therefore compresses
this question further, from 972 roof states to the dichotomy

$$
\boxed{C_2\quad\text{or}\quad S_3.}
\tag{0.1}
$$

An exact R07 component exists at a finite isolated window if and only if the
six-state image contains a 3-cycle.  Hence a cofinal Ihara-witness proof needs
only one 3-cycle in this quotient at every sufficiently deep level.

## 1. The canonical six-state quotient

Let $X$ be the fixed 972-element roof group:

$$
|X|=972.
\tag{1.1}
$$

and let

$$
A=\operatorname{Im}(G_{\mathbf Q}\longrightarrow X),
\qquad |A|=324.
\tag{1.2}
$$

The finite index-three census has one normal and twelve nonnormal subgroups.
The two candidates surviving the currently authenticated arithmetic filters,
`IDX3-NN-09` and `IDX3-NN-12`, are both nonnormal and both exclude rows 9
and 36.  The missing marked Frobenius datum has not selected between them.
The actual arithmetic image $A$ is one of this pair, and everything below is
orientation-independent.  Thus

$$
\boxed{[X:A]=3,\qquad A\not\triangleleft X.}
\tag{1.3}
$$

Let $X$ act on the three left cosets of $A$ and write

$$
\sigma:X\longrightarrow \operatorname{Sym}(X/A)\cong S_3.
\tag{1.4}
$$

### Lemma 1.1 (COS3-S3)

The map $\sigma$ is onto.  Its kernel is the core

$$
C=\operatorname{core}_X(A)=\bigcap_{g\in X}gAg^{-1},
\tag{1.5}
$$

and

$$
\boxed{|C|=162,\qquad \sigma(A)\cong C_2.}
\tag{1.6}
$$

#### Proof

The coset action is transitive of degree three.  Its image is therefore
either $C_3$ or $S_3$.  The first possibility would make the point stabilizer
trivial and hence make $A$ the kernel of $\sigma$, contrary to (1.3).
Therefore the image is $S_3$.  The kernel of a coset action is the core, so
$[X:C]=6$ and $|C|=972/6=162$.  The stabilizer of the coset $A$ is $A$;
its image is a point stabilizer in $S_3$, of order two. $\square$

Let $a$ denote zero-based row 9.  The power bridge v61 gives

$$
\operatorname{ord}(a)=9,\qquad a^4=\operatorname{row}36,
\qquad a\notin A.
\tag{1.7}
$$

### Lemma 1.2 (ROW9-IS-A-THREE-CYCLE)

Both $a$ and row 36 have the same nontrivial 3-cycle image:

$$
\boxed{\sigma(a)=\sigma(\operatorname{row}36),\qquad
       \operatorname{ord}(\sigma(a))=3.}
\tag{1.8}
$$

#### Proof

The order of $\sigma(a)$ divides both $9$ and $6$, hence divides three.
It is not the identity because $a\notin A$ and $C\le A$.  Thus it has order
three.  Since row 36 is $a^4$ and $4\equiv1\pmod3$, the two images agree.
$\square$

## 2. The finite B4 detector

For an isolated B4 window $J$ over K2, put

$$
H_J=\mathcal{ML}(J),\qquad
\theta_J:H_J\longrightarrow X,\qquad
P_J=\operatorname{Im}\theta_J.
\tag{2.1}
$$

Every arithmetic component survives at $J$, so $A\le P_J$.  Define the
six-state image

$$
T_J:=\operatorname{Im}(\sigma\theta_J)\le S_3.
\tag{2.2}
$$

### Theorem 2.1 (S3-TRANSITIVITY-DETECTOR)

The following are equivalent.

1. $P_J=X$.
2. $T_J=S_3$.
3. $T_J$ contains a 3-cycle.
4. $3$ divides $|T_J|$.
5. Some $h\in H_J$ has $\sigma\theta_J(h)$ of order three.
6. Row 9 belongs to $P_J$.
7. Some element of $H_J$ has exact K2 coordinate R07.

If these conditions fail, then

$$
\boxed{P_J=A,\qquad T_J=\sigma(A)\cong C_2.}
\tag{2.3}
$$

#### Proof

By v62, $A\le P_J\le X$ and index three imply $P_J=A$ or $X$.  Applying
$\sigma$ and Lemma 1.1 gives respectively $T_J=C_2$ or $S_3$.  This proves
the equivalence of 1 and 2 and the last assertion.  A subgroup of $S_3$
which already contains the point stabilizer $\sigma(A)\cong C_2$ is $S_3$
exactly when it contains a 3-cycle, equivalently when its order is divisible
by three.  This proves 2--5.  Lemma 1.2 gives $6\Rightarrow3$, while
$3\Rightarrow2\Rightarrow1\Rightarrow6$.  Finally v61, Lemma 2.1, gives
the equivalence of 6 and 7. $\square$

This is a complete finite equivalence, not a sampling heuristic.  In
particular, the positive calculation at one stage may stop as soon as a
single six-state 3-cycle is authenticated.  A negative calculation must
still prove that the complete six-state image is only the displayed $C_2$.

## 3. One-letter conversion in either surviving nonnormal case

Because $A$ is nonnormal of index three, its double-coset decomposition is

$$
\boxed{X=A\sqcup AxA}
\tag{3.1}
$$

for every $x\notin A$.  Indeed this is the pullback under $\sigma$ of the
two double cosets of a point stabilizer in $S_3$.  Consequently, for every
outside roof $x$ there are $c_0,c_1\in A$ with

$$
\boxed{a=c_0xc_1.}
\tag{3.2}
$$

Thus the inverse exponent allowed in the general index-three lemma of v62
is unnecessary for the actual 972 group.

The finite compiler replay in
`sol/luna_reply_162_outside_to_row9_compiler_v1.md` confirms (3.2) for all
648 outside rows separately for `IDX3-NN-09` and `IDX3-NN-12`.  Those tables
are candidate-conditioned and do not select the arithmetic orientation;
the theorem itself needs no such selection.

Choose arithmetic lifts $\gamma_0,\gamma_1$ of $c_0,c_1$.  If a typed B4
component $z$ has roof $x$, then

$$
u=\gamma_0z\gamma_1
\tag{3.3}

has roof row 9.  Writing $\operatorname{ord}(u)=3^\alpha q$ with
$3\nmid q$ and choosing $qe\equiv1\pmod9$, v61 gives the explicit exact
conversion

$$
\boxed{u^{4qe}\longmapsto R07.}
\tag{3.4}
$$

Only one occurrence of the nonarithmetic component $z$ is used.  The two
other factors are arithmetic components already available at every B4
window.

## 4. Cofinal form

Let $\mathcal D$ be any downward-cofinal family of finite B4-normal windows
which eventually refines K2; its members need not be isolated.  Suppose
that for every sufficiently deep $D\in\mathcal D$ there is a charming
shadow $z_D$ such that

$$
\operatorname{ord}
\bigl(\sigma(\operatorname{roof}(z_D))\bigr)=3.
\tag{4.1}
$$

Reduction from such a sufficiently fine $D$ to an arbitrary coarser
isolated audit window preserves the roof and its six-state image.  Theorem
2.1 then makes the exact-R07 fibre
nonempty at every isolated window.  Finite-fibre compactness supplies a
compatible inverse-limit point.  Therefore:

### Theorem 4.1 (COFINAL-S3)

R07 is in the image of the original profinite $\widehat{GT}$ if and only
if every isolated B4 audit window has full six-state image $S_3$.  It is
enough that a cofinal family, isolated or not, supply one 3-cycle as in
(4.1) at every sufficiently deep stage.

For the full-verbal family $D_j=N(B_4,60j!)$, the remaining positive target
is therefore exactly

$$
\boxed{
\forall j\gg0\ \exists z_j\in GT^\heartsuit(D_j):
\operatorname{ord}\bigl(\sigma(\operatorname{roof}(z_j))\bigr)=3.}
\tag{4.2}
$$

The $z_j$ may vary with $j$ and need not be chosen compatibly.  Compatibility
is recovered only after finite nonemptiness has been proved at all depths.

## 5. Effect on the remaining proof

The nonnilpotent B4 problem has not disappeared, but its observable has
become minimal:

$$
\text{large finite B4 shadow group}
\longrightarrow P_J\le X
\longrightarrow T_J\le S_3
\in\{C_2,S_3\}.
\tag{5.1}
$$

The first negative transition is exactly the loss of the 3-cycle in this
six-state quotient.  Pronilpotent, relative-formation, and PSL-chief
arguments need no longer preserve a prescribed 972-row while they are being
constructed; they need only prevent that loss.  Once any 3-cycle survives,
(3.2)--(3.4) compile it to exact R07.

This note proves the detector and compiler.  It does not prove (4.2), so
the 972 witness remains open at the coupled nonnilpotent B4 stages.

## 6. Sources

- `sol/proof_r07_one_bit_roof_fullness_v62.md`.
- `sol/proof_r07_row9_power_bridge_v61.md`.
- `sol/proof_relative_dihedral_b3_and_b4_small_window_v3.md`, Section 9.4.
- `crosscheck/d972_idx3_arithmetic_crosscheck_report_v2_20260823.md`.
- `sol/luna_reply_162_outside_to_row9_compiler_v1.md`.
- `sol/sol_reply_159_iv.md`, Sections 20.3 and 23.11.
