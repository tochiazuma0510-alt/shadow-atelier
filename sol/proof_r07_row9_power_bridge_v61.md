# R07 row-9 power bridge v61

Author: Sol / 2026-08-25

Status: paper-proof candidate; `verified=false`.  The finite row-9 power table
and the displayed R07 power square have been replayed independently at
candidate grade in `sol/luna_reply_162_r07_row9_power_bridge_v1.md`.  The K2
row-36 fibre used here is `cross_checked`.  No total K2 roster or asserted
order of $GT_3(K2)$ is used.

This note sharpens v60.  It shows that one does not need a total multiplication
table for $GT_3(K2)$, nor lifts of three Sylow generators, in order to target
R07.  The exact K2 lifting problem is equivalent to lifting one much coarser
point--zero-based row 9--at the 972-element roof.  The conversion from an
arbitrary row-9 lift to an exact R07 lift is one explicit power.

## 1. Pinned finite data

Let

$$
G:=GT_3(K2),\qquad \rho:G\longrightarrow X
\tag{1.1}
$$

be reduction to the fixed 972-element roof.  The complete K2 fibre over
zero-based row 36 is

$$
\rho^{-1}(\operatorname{row}36)=\{R07,R40\}.
\tag{1.2}
$$

Every nonempty fibre of a group homomorphism is a coset of its kernel.
Consequently

$$
\boxed{|\ker\rho|=2.}
\tag{1.3}
$$

Write $k$ for the nonidentity kernel element.  The kernel is normal and
$\operatorname{Aut}(C_2)=1$, so $k$ is central in $G$.

Write $a\in X$ for zero-based row 9.  In the frozen canonical coordinates,

$$
a=\left(0,((1,0),(8,0),(0,0)),1_{PSL(2,8)}\right).
\tag{1.4}
$$

The frozen right-Cayley law gives

$$
\operatorname{ord}(a)=9,\qquad
a^4=\operatorname{row}36.
\tag{1.5}
$$

The second equality is also visible in the coordinates: the two active
rotations become $(4,32)=(4,5)$ modulo $9$, while $m=0$ and the PSL coordinate
remain fixed.  The full GT-law replay is required here; coordinate addition
alone is not used as a substitute for it.

Let $b:=R07\in G$.  Proposition 1.1 of v60 gives

$$
\operatorname{ord}(b)=9,\qquad \rho(b)=a^4.
\tag{1.6}
$$

Define

$$
d:=b^7.
\tag{1.7}
$$

Since $4\cdot7\equiv1\pmod9$, equations (1.5)--(1.7) give

$$
\boxed{
\operatorname{ord}(d)=9,\qquad \rho(d)=a,\qquad d^4=b.}
\tag{1.8}
$$

Using the explicit R07 law from v60, $b^k=(0,f_{07}^k)$, so $d$ itself is
fully explicit.  Its $G_{36}\times PSL(2,8)\times C_3$ word coordinate is

$$
\left(((28,0),(8,0),(0,0)),1,0\right),
\tag{1.9}
$$

and the sevenfold concatenation of the frozen 38-letter R07 word is a literal
representative.  Reduction modulo $9$ gives (1.4).

The fibre above $a$ is $\{d,dk\}$.  The two factors in $dk$ commute and have
orders nine and two, so $dk$ has order eighteen.  Thus

$$
\boxed{d\text{ is the unique }3\text{-element of }G\text{ above }a.}
\tag{1.10}
$$

## 2. Prime-to-three fibre erasure

The following elementary lemma is the main point.

### Lemma 2.1 (COPRIME-FIBRE-ERASER)

Let $H$ be a finite group and let

$$
H\xrightarrow{\psi}G\xrightarrow{\rho}X
\tag{2.1}
$$

be homomorphisms, with $G,X,a,b,d$ as in Section 1.  Then

$$
\boxed{
b\in\operatorname{Im}\psi
\quad\Longleftrightarrow\quad
a\in\operatorname{Im}(\rho\psi).}
\tag{2.2}
$$

More explicitly, suppose $z\in H$ satisfies

$$
\rho\psi(z)=a.
\tag{2.3}
$$

Write

$$
\operatorname{ord}(z)=3^\alpha q,\qquad 3\nmid q.
\tag{2.4}
$$

Then $\alpha\ge2$.  Choose $e$ with

$$
qe\equiv1\pmod9.
\tag{2.5}
$$

The single explicit power

$$
\boxed{L_{07}(z):=z^{4qe}}
\tag{2.6}
$$

satisfies

$$
\psi(L_{07}(z))=R07.
\tag{2.7}
$$

#### Proof

First assume (2.3).  Since the order of $a$ is nine, its order divides
$\operatorname{ord}(z)$, hence $\alpha\ge2$.  Put $z_3=z^{qe}$.  The exponent
$qe$ kills the prime-to-three part of $z$, so $z_3$ is a $3$-element.  At the
same time,

$$
\rho\psi(z_3)=a^{qe}=a
\tag{2.8}
$$

by (2.5).  Therefore $\psi(z_3)$ is a $3$-element of $G$ above $a$.  The
uniqueness in (1.10) forces

$$
\psi(z_3)=d.
\tag{2.9}
$$

Taking fourth powers and using (1.8) proves (2.7), and hence the reverse
implication in (2.2).

Conversely, if $z\in H$ satisfies $\psi(z)=b$, then

$$
\rho\psi(z^7)=\rho(b^7)=\rho(d)=a,
\tag{2.10}
$$

which proves the forward implication. $\square$

The lemma is not a cardinality heuristic.  The load-bearing input is the
complete two-point K2 fibre, which makes the kernel a central $C_2$ and the
$3$-element over $a$ unique.
Without them, prime-primary stripping need not select a prescribed point in a
fibre.

## 3. Cofinal form

Let

$$
J_0\ge J_1\ge J_2\ge\cdots
\tag{3.1}
$$

be a nested cofinal ladder of isolated B4 windows over K2, and set

$$
H_n:=\mathcal{ML}(J_n).
\tag{3.2}
$$

Let

$$
\psi_n:H_n\longrightarrow G
\tag{3.3}
$$

be the B3-component map followed by reduction to K2.  The maps are compatible
with the B4 transition maps.

### Theorem 3.1 (ROW9-COFINAL-EQUIVALENCE)

For every $n$,

$$
\boxed{
\psi_n^{-1}(R07)\ne\varnothing
\quad\Longleftrightarrow\quad
(\rho\psi_n)^{-1}(a)\ne\varnothing.}
\tag{3.4}
$$

Consequently, if the coarse row $a=$ row 9 survives at every level of the
cofinal ladder, then there is a compatible sequence

$$
(b_n)_{n\ge0}\in\varprojlim_n H_n
\tag{3.5}
$$

whose exact K2 coordinate is R07.

#### Proof

Equation (3.4) is Lemma 2.1 applied to $H_n$.

For the inverse-limit assertion, put

$$
F_n:=\psi_n^{-1}(R07).
\tag{3.6}
$$

Every $F_n$ is a nonempty finite set.  Reduction maps carry $F_{n+1}$ into
$F_n$.  Regard the disjoint union of the $F_n$ as a rooted, levelled tree,
joining each point to its reduction.  It has nodes at arbitrarily high levels
and finite branching.  Koenig's lemma gives an infinite compatible path,
which is (3.5). $\square$

No compatibility among the initially chosen coarse row-9 lifts is required.
At a single finite level, (2.6) turns any such lift into an exact R07 lift;
compactness then chooses a compatible subsequence globally.

Under the standard cofinal identification

$$
\varprojlim_n\mathcal{ML}(J_n)\cong\widehat{GT},
\tag{3.7}
$$

the sequence (3.5) is a profinite GT element.  Since its 972-roof coordinate
is the pinned nonarithmetic row 36, it is an Ihara non-surjectivity witness.

## 4. Relation to the relative dihedral programme

The remaining universal statement is now exactly

$$
\boxed{
\text{for every finite isolated B4 refinement over K2, roof row 9 has a
typed B4 component.}}
\tag{4.1}
$$

This is strictly coarser than asking for the prescribed 38-letter R07
representative or even the prescribed K2 point.  It is also the natural input
for a relative dihedral theorem: row 9 has $m=0$, trivial PSL coordinate, and
the primitive dihedral torus coordinate $(1,-1,0)$ modulo nine.  Once any
relative correction produces a typed component over that coarse row, formula
(2.6) removes every prime-to-three ambiguity in the finite source and lands
at exact R07 automatically.

Thus the relative-dihedral strategy has not been replaced.  Its target has
been reduced to the correct one-generator coarse statement (4.1).  The
pentagon/PSL small-window theory is still needed to prove (4.1): a B3
dihedral lift by itself supplies no B4 component, and five separately positive
named windows are not a cofinal ladder.

## 5. Exact current boundary

What is newly proved on paper is

$$
\boxed{
R07\text{ lifts through a finite B4 level}
\iff
\text{roof row 9 lifts through that level},}
\tag{5.1}
$$

with the explicit conversion $z\mapsto z^{4qe}$.  Therefore the full
1944-row K2 roster and a K2 Sylow generator census are not prerequisites for
the witness construction.

What is not proved is (4.1).  In particular:

- full-972 images for finitely many named windows show row-9 survival only in
  those windows;
- the positive dihedral tower is not cofinal among B4 refinements;
- the absent isolated $PSL(2,8)$ strip-occurrence roster still prevents the
  v59 holonomy argument from closing every nonabelian edge.

Hence no fake certificate and no Ihara witness is declared in this note.  The
first mathematical target is no longer an all-generator K2 enumeration; it is
the universal typed row-9 statement (4.1).

## 6. Sources

- `sol/proof_r07_pointed_sylow3_cofinal_lift_v60.md`: the order-nine proof.
- `ci/ordinary_idx3_artifacts_32682548731/`
  `d972_rung_ordinary_idx3_producer_receipt_v2_20260824.json`: complete fixed
  row-36 K2 fibre.
- `sol/luna_reply_159o_ordinary_idx3_crosscheck_v1.md`: independent replay of
  that complete fibre.
- `sol/luna_reply_162_r07_row9_power_bridge_v1.md`: independent finite replay
  of (1.5), (1.8), and the commutative power square.
- `search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json` and its
  independent checker verdict: frozen 972 right-Cayley law and generator rows.
- `docs/week1-定義ノート.md`: canonical finite GT product and reduction law.
