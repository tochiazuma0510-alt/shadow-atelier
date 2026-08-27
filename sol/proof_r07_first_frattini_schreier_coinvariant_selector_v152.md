# R07 first-Frattini Schreier coinvariant selector v152

Author: Sol / 2026-08-27

Status: paper theorem and finite compiler contract.  For the universal first
relative-Frattini source module, the formation-visible quotient from v151 is
the first homology of one explicit finite-index free subgroup.  Its quotient
map is computed by sparse Schreier rewriting on the 708,588-state solvable
quotient graph.  No such production graph or task179 correction coordinate
has yet been emitted.  No cofinal lift, fake certificate, or Ihara witness is
declared.

## 1. The universal source relation module

Let

\[
 F=F(x,y)\twoheadrightarrow G
\tag{1.1}
\]

be the fixed task157ee/task176 joint evaluation, and put

\[
 \Omega=\ker(F\twoheadrightarrow G).
\tag{1.2}
\]

The universal first relative pro-3 Frattini kernel is

\[
 V=\Omega/\Phi_3(\Omega)
 =\Omega/\Omega^3[\Omega,\Omega]
 =H_1(\Omega;\mathbf F_3).
\tag{1.3}
\]

Conjugation through \(F\) gives its \(\mathbf F_3[G]\)-module structure.
V149 gives

\[
 R=R_S(G)=\widetilde S\cong PSL(2,8).
\tag{1.4}
\]

Let

\[
 P=q^{-1}(R)\leq F,
\tag{1.5}
\]

where \(q:F\twoheadrightarrow G\).  Then

\[
 1\longrightarrow\Omega\longrightarrow P
 \longrightarrow R\longrightarrow1.
\tag{1.6}
\]

The quotient of \(V\) relevant to v151 is the coinvariant module

\[
 V_R=V/[R,V].
\tag{1.7}
\]

## 2. Coinvariants are the homology of P

### Theorem 2.1 (SCHREIER COINVARIANT IDENTIFICATION)

The inclusion \(\Omega\hookrightarrow P\) induces a canonical isomorphism

\[
 \boxed{
 H_1(\Omega;\mathbf F_3)_R
 \xrightarrow{\sim}H_1(P;\mathbf F_3).}
\tag{2.1}
\]

Equivalently,

\[
 \boxed{
 V_R\cong P/P^3[P,P].}
\tag{2.2}
\]

#### Proof

The homology five-term exact sequence for (1.6) contains

\[
 H_2(P;\mathbf F_3)\longrightarrow H_2(R;\mathbf F_3)
 \longrightarrow H_1(\Omega;\mathbf F_3)_R
 \longrightarrow H_1(P;\mathbf F_3)
 \longrightarrow H_1(R;\mathbf F_3)\longrightarrow0.
\tag{2.3}
\]

The subgroup \(P\) of the free group \(F\) is free, so
\(H_2(P;\mathbf F_3)=0\).  The group \(R\cong PSL(2,8)\) is perfect and has
trivial integral Schur multiplier.  The universal-coefficient sequences for
homology therefore give

\[
 H_1(R;\mathbf F_3)=0,
 \qquad H_2(R;\mathbf F_3)=0.
\tag{2.4}
\]

The middle arrow in (2.3) is consequently an isomorphism, proving (2.1).
Equation (2.2) is the mod-3 abelianization description of the right side.
\(\square\)

### Corollary 2.2 (EXACT KERNEL)

The word map

\[
 \Omega\longrightarrow P/P^3[P,P]
\tag{2.5}
\]

factors through \(V\), and its kernel on \(V\) is exactly

\[
 \boxed{[R,V]=V\cap R_S(F/\Phi_3(\Omega)).}
\tag{2.6}

#### Proof

The map kills \(\Omega^3[\Omega,\Omega]\), so it factors through (1.3).
Theorem 2.1 identifies the resulting map with the canonical quotient to
coinvariants, whose kernel is \([R,V]\).  V151 Theorem 3.1 gives the second
equality. \(\square\)

Thus a formation-fibre coordinate for a literal correction word is not an
abstract cohomology label.  It is its ordinary mod-3 abelianization after the
word is regarded as an element of the explicit subgroup \(P\).

## 3. Exact dimension in the task176 group

Since \(R\triangleleft G\),

\[
 [F:P]=[G:R].
\tag{3.1}
\]

V149 and task176 give

\[
 |G|=357,128,352,
 \qquad |R|=504,
\tag{3.2}
\]

and hence

\[
 \boxed{[F:P]=|G/R|=708,588.}
\tag{3.3}

Nielsen--Schreier applied to the rank-two free group \(F\) gives

\[
 \operatorname{rank}(P)
 =1+[F:P](2-1)
 =\boxed{708,589}.
\tag{3.4}

Therefore

\[
 \boxed{
 V_R\cong\mathbf F_3^{708,589}.}
\tag{3.5}

This large dimension is not a contradiction with the small return-even or
full-pair spaces computed in v81--v83.  Those are particular finite module or
cohomology quotients of the universal source relation module.  A comparison
map is required before a vector in one is identified with a vector in the
other.

## 4. Closed sparse Schreier formula

Put

\[
 Q=G/R.
\tag{4.1}

Choose a deterministic rooted spanning tree in the marked \(x,y\) Cayley
graph of \(Q\), and let

\[
 t:Q\longrightarrow F
\tag{4.2}

be the corresponding prefix-closed transversal, with \(t(1)=1\).  For
\(q\in Q\) and \(a\in\{x,y\}\), the standard Schreier word is

\[
 s(q,a)=t(q)a\,t(qa)^{-1}\in P.
\tag{4.3}

Tree-edge Schreier words are trivial.  The nontrivial oriented edge words
form a free basis of \(P\); their number is

\[
 2|Q|-(|Q|-1)=|Q|+1=708,589.
\tag{4.4}

For a word \(w\in P\), trace its signed letters in the Cayley graph of \(Q\).
Every traversed edge contributes \(+1\) or \(-1\) to the corresponding
non-tree Schreier generator after the usual inverse-edge rewrite.  Reducing
the accumulated counts modulo three gives

\[
 \operatorname{Sch}_Q(w)
 \in\mathbf F_3^{708,589}.
\tag{4.5}

### Theorem 4.1 (LITERAL COINVARIANT SELECTOR)

Restricted to \(\Omega\), the map (4.5) is a homomorphism and induces the
isomorphism

\[
 \boxed{
 V_R\xrightarrow{\sim}\mathbf F_3^{708,589}}
\tag{4.6}

of (3.5).  In particular,

\[
 \boxed{
 [w]\in[R,V]
 \quad\Longleftrightarrow\quad
 \operatorname{Sch}_Q(w)=0}
\tag{4.7}

for every \(w\in\Omega\).

#### Proof

Schreier rewriting is an equality in the free group \(P\).  Abelianizing its
free basis and reducing modulo three gives (4.5), hence a homomorphism
\(P\to H_1(P;\mathbf F_3)\).  Theorem 2.1 identifies its restriction to
\(\Omega\), modulo \(\Phi_3(\Omega)\), with the coinvariant quotient.
The basis count (4.4) makes the target map an isomorphism, and its kernel is
(4.7). \(\square\)

The output is naturally sparse for a finite word: at most its literal length
many edge coordinates are touched before cancellations.  No
\(708,589\)-column dense matrix is required.

## 5. Direct use in task179

Every task179 correction factor and every accepted product correction lies in
\(\Omega\), because its complete task176 joint value is identity.  Therefore
the formation coordinate of a literal correction \(c\) is exactly

\[
 \rho_{\rm form}(c)=\operatorname{Sch}_Q(c).
\tag{5.1}

This gives a lossless augmented positive system:

\[
 \boxed{
 \begin{aligned}
 B_{\rm all}(c)&=-\beta_{\rm all},\\
 \operatorname{Sch}_Q(c)&=\eta_{\rm form},
 \end{aligned}}
\tag{5.2}

where the second target \(\eta_{\rm form}\) must come from an authenticated
relative-arithmetic or other prescribed formation reference.  If following
the direct explicit-word route without such a reference, task179 may solve
the first line alone and replay a first-rung successor; it must not silently
set \(\eta_{\rm form}=0\).

For column generation:

1. retain the source word of every correction column;
2. append its sparse \(\operatorname{Sch}_Q\) row computed from the same
   literal word;
3. coefficient \(2\) negates both the relation row and Schreier row and uses
   the literal inverse word;
4. append zero Schreier rows to PB3/PB4 boundary columns, because they are
   cellular chains and are not source correction words; and
5. replay the final source word directly in both blocks.

The fourth item is a typing rule, not the assertion that a boundary word has
zero formation coordinate: no source boundary word exists in the task179
correction product.

## 6. Relation to task185 and the arithmetic anchor

Task185 is commissioned to construct the same quotient

\[
 Q=G/\widetilde S
\tag{6.1}

with exact order 708,588, marked generators, and a deterministic source-word
section.  Its quotient Cayley roster and parent/letter table are precisely the
finite data needed for (4.2)--(4.5).  The residual and quotient should be
reconstructed independently in a Schreier checker rather than accepted from
order alone.

V150 shows that the **coarse** finite v18 anchor depends only on one arithmetic
coset in \(Q\).  That does not automatically determine the first-Frattini
target \(\eta_{\rm form}\) in (5.2): two profinite arithmetic lifts with the
same coarse \(Q\)-coordinate can differ by an element of \(\Omega\), whose
Schreier coordinate need not vanish.  Thus:

\[
 \boxed{
 \text{coarse arithmetic coset}\ne
 \text{first-Frattini arithmetic displacement}.}
\tag{6.2}

An authenticated first-rung arithmetic word/component, or a theorem proving
independence modulo \([R,V]\), is still required for the formation-purified
second line of (5.2).

## 7. Naturality and the next rung

The construction is canonical after freezing the marked quotient graph and
spanning-tree rule.  A quotient map of marked graphs which sends the chosen
tree and source section compatibly induces the expected linear map on
Schreier homology.  Without that tree-compatibility, the coordinates differ by
an explicit change of free basis; the underlying homology map remains
canonical but coordinate equality is not literal.

At the second Frattini rung the residual is generally an extension of
\(\widetilde S\) by the active submodule \([R,V]\), rather than the bare
superperfect group \(R\).  V151's superperfect collapse therefore cannot be
iterated without checking the new residual's low-degree homology.  Theorem
4.1 is an exact first-rung selector, not yet the all-rung homotopy.

```text
FIRST UNIVERSAL FORMATION QUOTIENT = H1(P;F3):      PAPER_PROOF
TASK176 QUOTIENT STATE COUNT:                       708588
SCHREIER COINVARIANT DIMENSION:                     708589 / PAPER_PROOF
SPARSE LITERAL WORD SELECTOR Sch_Q:                 PAPER_PROOF
Q CAYLEY ROSTER / TREE / INDEPENDENT REPLAY:         NOT MATERIALIZED
TASK179 CORRECTION Schreier COORDINATE:              NOT COMPUTED
FIRST-RUNG ARITHMETIC TARGET eta_form:               UNKNOWN_INPUT
SECOND-RUNG RESIDUAL LOW-DEGREE HOMOLOGY:            OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:     NOT DECLARED
```

`R07_FIRST_FRATTINI_SCHREIER_COINVARIANT_SELECTOR_V152_PAPER_GRADE`
