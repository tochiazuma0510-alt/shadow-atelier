# R07 uniform nested correction product v64

Author: Sol / 2026-08-25

Status: paper-proof candidate; `verified=false`, `cross_checked=false`.
This is a constructive
inverse-limit theorem.  It proves how compatible finite correction formulas
assemble into one explicit profinite word.  It does not prove that every
remaining nonabelian chief equation is soluble.

The purpose of this note is to distinguish two demands which had been mixed:

1. a functorial lift section for **every** element at **every** refinement;
2. one explicit compatible R07 branch.

The first is much stronger and is unnecessary.  For the second it is enough
to choose, at the $n$-th step, one correction which is invisible at all
earlier steps.  The resulting infinite product is automatically compatible;
no separate composition law for arbitrary lift sections is required.

## 1. One cofinal evaluation filtration

Fix a nested cofinal ladder of finite B4 audit windows

$$
J_0\succeq J_1\succeq J_2\succeq\cdots
\tag{1.1}
$$

which eventually refines the fixed K2 mark.  Include at level $n$ every
word evaluation used by the two hexagons, the ordered five-coface pentagon,
descent, and the marked B3 coordinate through $J_n$.  Their joint image is a
finite group

$$
\Psi_n:\widehat F_2\twoheadrightarrow H_n,
\qquad U_n:=\ker\Psi_n.
\tag{1.2}
$$

Replace $\Psi_n$ by the product of all evaluations through levels
$0,\ldots,n$ if necessary.  Then, without changing the finite equations at
level $n$,

$$
U_0\ge U_1\ge U_2\ge\cdots,
\qquad \bigcap_nU_n=1.
\tag{1.3}
$$

The last equality is the cofinal separation statement: two profinite words
which agree in every evaluation in the ladder agree in $\widehat F_2$.  For
convergence below it is enough that the $U_n$ form a neighbourhood basis of
the identity on the closed correction subgroup being used.

Put

$$
S=PSL(2,8),\qquad
\Pi_S=\ker(\widehat F_2\longrightarrow F_2^{\mathcal C_S}),
\tag{1.4}
$$

as in v37.  The full correction group after level $n$ is $U_n$ itself.
It is a closed normal subgroup, $U_{n+1}\le U_n$, and every element of
$U_n$ fixes all relation values, side data, and the exact K2 mark already
frozen through level $n$.  The smaller group $\Pi_S\cap U_n$ is the
preferred relative-formation lane.  It is useful, but it is not assumed to
contain every possible next correction.

## 2. The exact finite one-step domain

The finer joint image $H_{n+1}$ maps onto the accumulated coarse image
$H_n$; write this quotient map as

$$
\pi_{n+1,n}:H_{n+1}\twoheadrightarrow H_n.
\tag{2.1}
$$

The complete finite value domain for an arbitrary correction which fixes
the prefix is

$$
\boxed{
D_{n+1,n}:=\Psi_{n+1}(U_n)
=\ker\pi_{n+1,n}.}
\tag{2.2}
$$

Indeed, the forward inclusion follows from
$\Psi_n=\pi_{n+1,n}\Psi_{n+1}$.  Conversely, if
$d\in\ker\pi_{n+1,n}$, choose $c\in\widehat F_2$ with
$\Psi_{n+1}(c)=d$.  Then $\Psi_n(c)=1$, so $c\in U_n$.

V37, Theorem 2.1, applied to the accumulated maps also identifies the
preferred relative subdomain:

$$
\boxed{
 C^{\mathrm{rel}}_{n+1,n}
 :=\Psi_{n+1}(\Pi_S\cap U_n)
=R_S(H_{n+1})\cap\ker\pi_{n+1,n}.}
\tag{2.3}
$$

Every point of (2.3) is the joint value of one common profinite word
$c\in\Pi_S\cap U_n$.  Hence this lane does not select five independent
coface corrections and has no encode/decode gap.  But (2.3) may be a proper
subgroup of (2.2); failure in the relative lane alone is not failure of the
full one-step problem.

Let $f_n\in\widehat F_2$ be a word which already gives an admissible exact
R07 component through level $n$.  Substitute $f_nc$ into the printed two
hexagons and ordered pentagon and impose descent and onto.  This gives a
finite subset

$$
Z_{n+1}(f_n)\subseteq D_{n+1,n}
\tag{2.4}
$$

of correction values which extend that particular prefix through level
$n+1$.  This is the exact ONE-STEP fibre, restricted only by the necessary
condition that every earlier evaluation be fixed.  Its relative part is

$$
Z^{\mathrm{rel}}_{n+1}(f_n)
:=Z_{n+1}(f_n)\cap C^{\mathrm{rel}}_{n+1,n}.
\tag{2.5}
$$

Fix once and for all a signed-word shortlex order in the two free generators.
The discrete free group $F_2$ is dense in $\widehat F_2$, so its image in
the finite group $H_{n+1}$ is all of $H_{n+1}$.  Consequently every
$d\in D_{n+1,n}$ has a finite signed-word representative $c\in F_2$.
Because $d$ projects trivially to $H_n$, that same representative belongs
to $F_2\cap U_n$.  Thus breadth-first shortlex enumeration, with the two
finite tests

$$
\Psi_{n+1}(c)=d,\qquad \Psi_n(c)=1,
\tag{2.6}
$$

terminates for every $d\in D_{n+1,n}$.  Order the finite set
$D_{n+1,n}$ by the shortlex-minimal representative supplied this way.  If
(2.4) is nonempty, let

$$
\operatorname{corr}_{n+1}(f_n)
\tag{2.7}
$$

be the first representative of the first passing value.  This makes the
finite step deterministic.  It is not an assertion that (2.4) is always
nonempty.  When a passing value lies in (2.3), v37 authenticates its
relative origin; the finite signed-word representative selected by (2.6)
need only lie in $U_n$, not literally in $\Pi_S$.

## 3. The uniform product theorem

### Theorem 3.1 (NESTED-CORRECTION-PRODUCT)

Assume that:

1. an explicit word $f_0$ is an admissible B4 component through $J_0$ and
   has exact K2 coordinate R07;
2. recursively, for every $n\ge0$, the finite set
   $Z_{n+1}(f_n)$ is nonempty; and
3. with

   $$
   c_n=\operatorname{corr}_{n+1}(f_n)\in U_n,
   \qquad f_{n+1}=f_nc_n,
   \tag{3.1}
   $$

   the literal representative selected in (2.7) is used, including all
   side gates.

Then the product

$$
\boxed{
f_\infty=f_0c_0c_1c_2\cdots}
\tag{3.2}
$$

converges in $\widehat F_2$.  The pair $(0,f_\infty)$ belongs to the
original profinite $\widehat{GT}$ and has exact K2 coordinate R07.
Consequently its 972-roof is nonarithmetic row 36 and it is an Ihara
non-surjectivity witness.

#### Proof

For $m>n$, equation (3.1) gives the exact right-tail identity

$$
f_n^{-1}f_m=c_nc_{n+1}\cdots c_{m-1}\in U_n.
\tag{3.3}
$$

Every factor $c_r$ for $r\ge n$ lies in $U_r\le U_n$, and $U_n$ is a
subgroup.  Therefore the partial products are Cauchy in the profinite
topology.  Completeness of $\widehat F_2$ supplies the limit (3.2).

Fix a level $j$.  Every correction $c_n$ with $n\ge j$ lies in
$U_n\le U_j$, so all evaluations at level $j$ are constant from $f_j$
onward.  By construction $f_j$ satisfies the two hexagons, ordered
pentagon, descent, charming, and onto gates there.  Continuity therefore
makes $f_\infty$ satisfy the same gates at level $j$.  Since this holds for
every level of a cofinal ladder, the inverse-limit/Main-Line theorem gives
$(0,f_\infty)\in\widehat{GT}$.

The K2 marked map is included in every accumulated $\Psi_n$.  Thus every
$c_n$ has trivial K2 value and the limit retains the exact R07 value of
$f_0$.  Row 36 is outside the arithmetic subgroup, proving the last
assertion. $\square$

The theorem produces one word, not unrelated finite choices.  It also shows
that the stronger identity

$$
\mathscr L_{J''/J'}\mathscr L_{J'/J}=\mathscr L_{J''/J}
\tag{3.4}
$$

for lift maps on every possible input is unnecessary.  Adjacent corrections
in the nested kernels already imply compatibility of the selected branch.

### Corollary 3.2 (FINITE ROOF NORMALIZATION POLICY)

At any fixed B4 audit level, suppose an admissible shadow with an outside
roof has been found.  Because the admissible shadows form a group and their
roof image contains the arithmetic subgroup, v63 allows one to compose in
the *finite GT-shadow group law* with arithmetic shadows so that the roof
becomes row 9.  V61 then takes a suitable finite group power and produces an
admissible shadow with exact K2 coordinate R07.

This is a normalization of finite shadow elements, not the false word
identity obtained by multiplying their $f$-coordinates in $F_2$.  In an
explicit implementation the arithmetic shadows and all compositions must
be evaluated with the actual GT group law.  Thus the finite search may start
from whichever of the 648 outside rows makes the active equations cheapest,
then normalize the passing shadow to R07 before starting Theorem 3.1.

### Proposition 3.3 (FRONTIER SEARCH VERSUS A UNIFORM SELECTOR)

There is already a uniform complete procedure at every **finite** depth.
Let $V_n$ be the finite set of exact-R07 admissible states through level
$n$.  For every $v\in V_n$, choose its stored word representative, enumerate
the finite domain $D_{n+1,n}$, and retain exactly the values passing the
level-$n+1$ equations.  This computes the complete edge set

$$
V_{n+1}\longrightarrow V_n.
\tag{3.5}
$$

It never confuses death of one prefix with death of the whole fibre.  If the
resulting finite tree has vertices at every depth, Koenig compactness gives
an infinite branch.  This is a uniform exhaustive finder, although its
frontier may be very large and compactness alone does not certify that the
first locally passing edge will survive forever.

A genuinely greedy explicit finder follows from the stronger local datum:
subsets $E_n\subseteq V_n$, a seed $f_0\in E_0$, and formulas

$$
\kappa_{n+1}:E_n\longrightarrow U_n
\tag{3.6}
$$

such that

$$
f\,\kappa_{n+1}(f)\in E_{n+1}
\qquad(f\in E_n).
\tag{3.7}
$$

Then $c_n=\kappa_{n+1}(f_n)$ satisfies Theorem 3.1 by induction and gives
one explicit compatible word without backtracking.  Thus the remaining aim
of the relative-dihedral programme is not merely finite nonemptiness: it is
to identify an extension-stable invariant $E_n$ and prove (3.7).  The closed
formulas in Section 4 provide $\kappa$ on the chief-step types already
settled.

## 4. Closed formulas already available for `corr`

The definition (2.7) is a finite fallback.  On the branches already treated
in the preceding notes it has a closed form.

1. **Formation-free stage.**  The relative-dihedral word of v18 already
   solves the stage; the new correction is the identity after the relative
   base has been installed.
2. **Prime-to-three four-forget extension.**  V20 uses the one profinite
   primary exponent $e_3$; no stagewise CRT choice is needed.
3. **Lower-central marked stage.**  V31 supplies the affine hexagon solve
   followed by the Brunnian lattice solve, and v43 repairs the finite mark by
   one-degree-deeper tail surgery.
4. **Typed abelian chief stage satisfying FC-13'--FC-15.**  V3, Theorem
   5.2, gives

   $$
   c_n=\operatorname{word}(-\Sigma\beta_n),\qquad
   \Sigma=(\sigma\mathbf D_3)^{-1}\sigma.
   \tag{4.1}
   $$

5. **Peelable $PSL(2,8)^t$ stage.**  V52 recovers every pivot variable by
   the unique nonabelian leaf formula.  Under torus alignment, v57--v59
   replace the remaining core by at most 28 holonomy trials followed by one
   Smith solve modulo nine; v37 then authenticates the passing tuple as the
   value of one common relative word.

Each displayed finite tuple lies in $D_{n+1,n}$, and (2.6) supplies a
literal signed-word representative in the accumulated kernel $U_n$.
Relative formulas land in $C^{\mathrm{rel}}_{n+1,n}$ and therefore retain
their one-common-word meaning, but no claim that the chosen discrete
representative lies globally in $\Pi_S$ is needed.  Hence the different
local formulas can be interleaved in (3.2) without damaging an earlier
component.

## 5. Exact unsolved local statement

The uniform assembly mechanism and the complete finite-frontier algorithm
are therefore available.  What is not yet complete is a backtracking-free
selector.  For one chosen branch, the unproved input to Theorem 3.1 is
precisely

$$
\boxed{Z_{n+1}(f_n)\ne\varnothing\quad\text{at every remaining active
coupled B4 chief step}.}
\tag{5.1}
$$

After v33--v36 and v48--v59, a first unresolved step can occur only in the
doubly supported Brunnian/formation residual and has one of the following
forms:

- an active abelian module for which the actual FC-13'--FC-15 complex has
  not yet been proved;
- a $PSL(2,8)^t$ strip whose obstruction core is not removed by leaf
  elimination and whose actual torus holonomy/linear system has not passed;
- a different nonabelian simple type occurring with multiplicity at least
  seven.

The six-state theorem v63 changes the search policy but not this logical
boundary.  If a fixed exact-R07 prefix dies, one should not declare failure:
one may restart (3.2) from any other outside seed.  A positive proof needs
one seed for which (5.1) holds forever, while a negative certificate must
show that the complete outside fibre is empty at one actual finite level.

Thus v64 answers **how** a uniform explicit lift is assembled once the local
relative corrections are supplied.  Proposition 3.3 also states exactly
what would turn it into a uniform discovery theorem: the extension-stable
rule (3.6)--(3.7).  The note does not conceal the remaining chief-step
nonemptiness behind compactness and does not yet declare the 972 witness.

## 6. Sources

- `sol/proof_relative_dihedral_b3_and_b4_small_window_v3.md`.
- `sol/proof_relative_dihedral_formation_lift_v18.md`.
- `sol/proof_r07_uniform_prime_to3_extension_lift_v20.md`.
- `sol/proof_r07_brunnian_compressed_lift_recursion_v31.md`.
- `sol/proof_relative_dihedral_brunnian_double_localization_v33.md`.
- `sol/proof_relative_formation_residual_exact_correction_domain_v37.md`.
- `sol/proof_marked_tail_exactification_recursion_v43.md`.
- `sol/proof_r07_psl_strip_leaf_elimination_v52.md`.
- `sol/proof_r07_sylow3_torus_linearization_v57.md`.
- `sol/proof_r07_sylow3_torus_holonomy_v59.md`.
- `sol/proof_r07_s3_transitivity_detector_v63.md`.
