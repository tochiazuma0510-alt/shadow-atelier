# R07 one-bit roof-fullness criterion v62

Author: Sol / 2026-08-25

Status: paper-proof candidate; `verified=false`.  The finite row-9 power
bridge is independently replayed but is not promoted here beyond its recorded
evidence grade.  No total roster for `GT_3(K2)` is used.

This note combines the row-9 power bridge v61 with the pinned arithmetic
index-three theorem at the 972-element roof.  The result replaces a
prescribed-fibre search at each B4 level by one binary question:

$$
\boxed{\text{is the roof image the arithmetic subgroup of order }324,
\text{ or all }972\text{ elements?}}
\tag{0.1}
$$

A positive answer needs only one roof element outside the arithmetic image;
it need not be row 9 and it may vary from level to level.  A negative answer
still requires a complete image/fibre argument.

The cofinal one-outside argument itself is the mechanism already isolated as
FV-5 in `docs/notes/fullverbal_tower_screening_v1.md`.  The new specialization
here is its equivalence with the **exact K2 point R07**, via the explicit
row-9 power section of v61.

## 1. Pinned objects

Let

$$
G=GT_3(K2)\xrightarrow{\rho}X
\tag{1.1}
$$

be the fixed reduction to the roof group, with

$$
|X|=972.
\tag{1.2}
$$

Let

$$
A=\operatorname{Im}(G_{\mathbf Q}\longrightarrow X).
\tag{1.3}
$$

The authenticated arithmetic classification gives

$$
|A|=324,\qquad [X:A]=3,
\tag{1.4}
$$

and the explicit complement

$$
\Omega=X\setminus A,qquad |\Omega|=648.
\tag{1.5}
$$

Zero-based row 36 belongs to $\Omega$.  If $a$ is zero-based row 9, the
finite power bridge v61 gives

$$
\operatorname{ord}(a)=9,qquad a^4=\operatorname{row}36.
\tag{1.6}
$$

In particular

$$
a\notin A,
\tag{1.7}
$$

because $A$ is a subgroup and otherwise $a^4$ would belong to $A$.

For an isolated B4 window $J$ over K2, let

$$
\theta_J:\mathcal{ML}(J)\longrightarrow X
\tag{1.8}
$$

be arity-three restriction followed by roof reduction, and put

$$
P_J:=\operatorname{Im}\theta_J\le X.
\tag{1.9}
$$

Every Galois element has a component at every original finite B4 window.
Consequently every arithmetic roof row occurs in $P_J$ and

$$
\boxed{A\le P_J\le X.}
\tag{1.10}
$$

## 2. The local one-bit theorem

### Theorem 2.1 (ONE-BIT-ROOF)

For every isolated B4 window $J$ over K2, the following conditions are
equivalent.

1. $P_J=X$.
2. $P_J\cap\Omega\ne\varnothing$.
3. $a=\operatorname{row}9$ belongs to $P_J$.
4. Some element of $\mathcal{ML}(J)$ has exact K2 coordinate R07.
5. $|P_J|=972$.
6. $243$ divides $|P_J|$.

If none holds, then

$$
\boxed{P_J=A,\qquad |P_J|=324.}
\tag{2.1}
$$

#### Proof

By (1.10) and $[X:A]=3$, Lagrange's theorem leaves only

$$
P_J=A\quad\text{or}\quad P_J=X.
\tag{2.2}
$$

This proves the equivalence of (1), (2), and (5).  It also proves the
equivalence with (6), since

$$
324=4\cdot3^4,qquad 972=4\cdot3^5.
\tag{2.3}
$$

Condition (1) implies (3), while (3) implies (2) by (1.7).  Finally apply
v61, Lemma 2.1, to

$$
\mathcal{ML}(J)\longrightarrow G\longrightarrow X.
\tag{2.4}
$$

It says exactly that row 9 occurs in the roof image if and only if R07
occurs in the exact K2 image.  Thus (3) and (4) are equivalent.  The final
assertion follows from (2.2). $\square$

The theorem is asymmetric in the way useful for computation:

- to prove positivity at $J$, it suffices to exhibit **any one** typed B4
  component whose roof is one of the 648 rows in $\Omega$;
- to prove negativity, a failed chosen word or restricted correction lane is
  insufficient--one must prove $P_J=A$, or equivalently exhaust the complete
  row-9 fibre.

No multiplication table for the 1944 possible K2 pairs enters the proof.

### Lemma 2.2 (INDEX-THREE-ONE-LETTER)

Let $A$ be any index-three subgroup of a finite group $X$.  For every two
elements $x,y\in X\setminus A$ there are

$$
\varepsilon\in\{1,-1\},\qquad c_0,c_1\in A
\tag{2.5}
$$

such that

$$
\boxed{y=c_0x^\varepsilon c_1.}
\tag{2.6}
$$

#### Proof

If $A\triangleleft X$, then $X/A\cong C_3$.  The two outside cosets are
inverse, so one of $x,x^{-1}$ has the same coset as $y$; (2.6) follows even
with one of $c_0,c_1$ equal to $1$.

Suppose $A$ is not normal.  The action on the three left cosets has image
$S_3$, and the image of $A$ is a point stabilizer.  A point stabilizer in
$S_3$ has exactly two double cosets: itself and its four-element complement.
Pulling back through the coset action gives

$$
X=A\sqcup AxA.
\tag{2.7}
$$

Thus every outside $y$ lies in $AxA$, and (2.6) holds with
$\varepsilon=1$. $\square$

### Corollary 2.3 (OUTSIDE-TO-R07-COMPILER)

For each $x\in\Omega$, fix one factorization

$$
a=\operatorname{row}9=c_0(x)x^{\varepsilon(x)}c_1(x)
\tag{2.8}
$$

from Lemma 2.2, and choose Galois elements with roof images $c_0(x)$ and
$c_1(x)$.  Let $J$ be isolated and let $z\in\mathcal{ML}(J)$ have roof $x$.
If $\gamma_{0,J},\gamma_{1,J}$ are the corresponding arithmetic components,
put

$$
u=\gamma_{0,J}z^{\varepsilon(x)}\gamma_{1,J}.
\tag{2.9}
$$

Then $u$ has roof row 9.  If

$$
\operatorname{ord}(u)=3^\alpha q,\qquad 3\nmid q,\qquad qe\equiv1\pmod9,
\tag{2.10}
$$

the completely explicit finite-level conversion

$$
\boxed{u\longmapsto u^{4qe}}
\tag{2.11}
$$

has exact K2 coordinate R07.

#### Proof

Equation (2.9) may be evaluated because $\mathcal{ML}(J)$ is a group, and
its roof is (2.8).  Formula (2.11) is v61, Lemma 2.1. $\square$

One need not factor the individual order of $u$.  If $Q_J$ is the largest
divisor of $|\mathcal{ML}(J)|$ coprime to three and
$s_J=v_3(|\mathcal{ML}(J)|)$, choose $E_J$ so that

$$
Q_JE_J\equiv1\pmod{3^{s_J}}.
$$

Then the uniform levelwise formula

$$
\boxed{u\longmapsto u^{4Q_JE_J}}
\tag{2.12}
$$

has the same conclusion: $Q_J$ kills every prime-to-three primary component,
while the congruence preserves the full three-primary component.

There is also one genuinely compatible exponent.  Let

$$
\mathbf e_3=(1\in\mathbf Z_3,\ 0\in\mathbf Z_\ell\text{ for }\ell\ne3)
\in\widehat{\mathbf Z}.
\tag{2.13}
$$

Exponentiation by $\mathbf e_3$ is defined in the procyclic closure of any
element of a profinite group.  Hence a compatible outside thread with fixed
roof $x$, after the arithmetic sandwich (2.9), is sent compatibly at every
level by

$$
\boxed{u\longmapsto u^{4\mathbf e_3}}
\tag{2.14}
$$

to an exact-R07 thread.  Formula (2.12) is its ordinary finite-level
realization.

Thus the finite compiler needs only **one occurrence of the supplied outside
component**, two arithmetic components, and one power extraction.  Since
$\Omega$ is finite, the 648 triples
$(c_0(x),\varepsilon(x),c_1(x))$ can be precomputed once.  This compiler is
only a post-processing device: the hard input remains one actual outside B4
component.

## 3. Cofinal form and monotonicity

Order B4 windows by refinement: $K\preceq J$ means that $K$ is finer than
$J$.  Reduction gives

$$
K\preceq J\quad\Longrightarrow\quad P_K\le P_J.
\tag{3.1}
$$

### Theorem 3.1 (COFINAL-ONE-BIT)

The following are equivalent.

1. R07 lies in the image of the original profinite $\widehat{GT}$ at K2.
2. $P_J=X$ for every isolated B4 window $J$ over K2.
3. There is a cofinal family $\mathcal C$ of such windows for which
   $P_K\cap\Omega\ne\varnothing$ for every $K\in\mathcal C$.

In condition 3 the displayed outside element may be different for every
$K$.

#### Proof

If a profinite element has exact K2 coordinate R07, its component at every
$J$ proves condition 4 of Theorem 2.1, hence $P_J=X$.  This gives
$1\Rightarrow2$, and $2\Rightarrow3$ follows by taking all windows.

Assume condition 3.  Given an arbitrary $J$, choose $K\in\mathcal C$ with
$K\preceq J$.  Theorem 2.1 gives $P_K=X$, and (3.1) then forces

$$
X=P_K\le P_J\le X.
\tag{3.2}
$$

Thus condition 2 holds.  Theorem 2.1 makes the exact R07 fibre nonempty at
every finite B4 level.  The finite-fibre tree and Koenig compactness argument
of v61, Theorem 3.1, supplies a compatible inverse-limit point.  Hence
$2\Rightarrow1$. $\square$

For a nested cofinal ladder $J_0\succeq J_1\succeq\cdots$, the sequence

$$
P_{J_n}\in\{X,A\}
\tag{3.3}
$$

can change at most once: after it becomes $A$, every finer image remains
$A$.  Therefore it is enough to certify one outside roof row at levels
$n_i\to\infty$.  Those certificates need neither use the same outside row
nor form compatible chosen components; compactness is applied only after
all finite fibres are known to be nonempty.

### Theorem 3.2 (NONISOLATED-COFINAL-ONE-OUTSIDE)

Let $\mathcal D$ be a downward-cofinal family of finite B4-normal windows
whose sufficiently deep members refine the fixed K2 roof condition.  The
members of $\mathcal D$ are **not** assumed isolated.  Suppose that for every
sufficiently deep $C\in\mathcal D$ there is a charming B4 shadow

$$
z_C\in GT^\heartsuit(C)
\tag{3.4}
$$

whose roof belongs to $\Omega$.  Then R07 lies in the K2 image of
$\widehat{GT}$.

#### Proof

Take an arbitrary isolated B4 window $J$ over K2.  Cofinality gives a
sufficiently deep $C\in\mathcal D$ with $C\preceq J$.  The survive/reduction
map sends $z_C$ to a charming shadow at $J$ with the same outside roof row.
Isolation is required at $J$, not at $C$: it makes $P_J$ a subgroup.  Hence
Theorem 2.1 gives $P_J=X$ and a nonempty exact-R07 fibre at $J$.  This holds
for every isolated $J$, so Theorem 3.1 and compactness give the claimed
profinite point. $\square$

This is the exact FV-5 isolation-removal mechanism.  In particular, FV-3
provides the canonical full-verbal cofinal family

$$
C_j=N(B_4,q_j),\qquad q_j=60\,j!.
\tag{3.5}
$$

Therefore a fully explicit endgame may target just

$$
\boxed{
\forall j\gg0\ \exists z_j\in GT^\heartsuit(N(B_4,60j!))
\text{ with roof}(z_j)\in\Omega.}
\tag{3.6}
$$

The $z_j$ need not initially be compatible and need not have roof row 9.
An explicit compatible formula would contain more information, but it is
strictly stronger than what the witness proof requires.

## 4. Where a first negative transition can occur

Theorem 2.1 turns the obstruction tree into a binary roof-image tree.  Take
a chief refinement chain and suppose a first transition

$$
P_{J_i}=X,\qquad P_{J_{i+1}}=A
\tag{4.1}
$$

occurs.  At that edge the complete exact-R07 fibre, equivalently the complete
row-9 fibre, becomes empty.  The earlier relative-dihedral theorems route
such a transition as follows.

1. V18 supplies the lift in the finite formation having no
   $S=PSL(2,8)$ composition factor.  Hence a transition cannot be explained
   by a purely formation-free target.
2. V20 and v22 supply the marked lift under their prime-to-three,
   three-kernel, $3'$-by-$3$, and stated nilpotent/product hypotheses.  A
   first transition must violate those decoupling hypotheses.
3. V33 puts the surviving relation defect simultaneously in the Brunnian
   subgroup and the $S$-formation residual.
4. V35 says that an active nonabelian chief factor of multiplicity at most
   six has simple type $S$; a different simple type can occur only with
   multiplicity at least seven.  V36 leaves active abelian modules as a
   genuine linear relation problem.
5. For an $S$-power step, v48/v52/v57/v59 reduce the exact common-word
   equations to the labelled PSL-strip system, leaf elimination, and the
   28-state Sylow-torus holonomy/linear solve when the torus lane applies.

Thus the still-open positive theorem is not an all-generator K2 theorem.
It is the exclusion of the binary transition (4.1) in genuinely coupled
PB4 chief refinements.  Globally one must retain both the active abelian
case and the multiplicity-at-least-seven different-simple escape; the
currently missing actual isolated PSL-strip roster addresses only the
small $S$-power branch.  On the full-verbal cofinal family (3.5), other simple
types can occur already at the first computationally relevant stages, so a
PSL-only roster is not by itself the global closure theorem.

## 5. Computational consequence

At a registered actual isolated B4 window, any of the following is a
finite positive certificate for that level:

$$
\begin{array}{c}
\text{one typed component with roof in }\Omega,\\
|P_J|=972,\\
243\mid |P_J|,\\
\operatorname{row}9\in P_J.
\end{array}
\tag{5.1}
$$

The first is usually the cheapest.  Once a preimage $z$ of row 9 is found,
v61 gives an exact R07 preimage by the explicit power

$$
z\longmapsto z^{4qe},\qquad
\operatorname{ord}(z)=3^\alpha q,\qquad 3\nmid q,\qquad
qe\equiv1\pmod9.
\tag{5.2}
$$

The independent finite replay additionally reports that the squares in
$X$ form a 243-element subgroup generated by zero-based rows
$1,9,81^2=656$.  This is a useful machine checksum for the last two tests
in (5.1), but it is not load-bearing in Theorems 2.1 or 3.1.

## 6. Fake/witness boundary

- If a complete actual level proves $P_J=A$, then R07 does not come from
  $\widehat{GT}$.  This is a complete negative certificate for that K2
  coordinate, but it should not by itself be renamed a paper `fake
  GT-shadow` without the required typed B4 object and refinement statement.
- If a cofinal family satisfies the positive condition of Theorem 3.1, the
  resulting compatible exact-R07 thread has roof row 36 in $\Omega$ and is
  an Ihara non-surjectivity witness.
- The present note proves the equivalences and the one-bit reduction, not
  either terminal.  No fake certificate and no Ihara witness is declared.

## 7. Sources

- `sol/proof_r07_row9_power_bridge_v61.md`.
- `sol/luna_reply_162_r07_row9_power_bridge_v1.md`.
- `sol/proof_relative_dihedral_formation_lift_v18.md`.
- `sol/proof_r07_uniform_prime_to3_extension_lift_v20.md`.
- `sol/proof_r07_three_kernel_decoupling_v22.md`.
- `sol/proof_relative_dihedral_brunnian_double_localization_v33.md`.
- `sol/proof_r07_active_nonabelian_chief_classification_v35.md`.
- `sol/proof_r07_active_abelian_layer_over_psl_core_v36.md`.
- `sol/proof_r07_psl_strip_normal_form_v48.md` through
  `sol/proof_r07_sylow3_torus_holonomy_v59.md`.
- `docs/notes/fullverbal_tower_screening_v1.md`, FV-5.
- `sol/proof_relative_dihedral_b3_and_b4_small_window_v3.md`, Section 9.4,
  for the 324/648 arithmetic classifier and row 36.
