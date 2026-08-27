# R07 weighted context-cell selector v132

Author: Sol / 2026-08-27

Status: paper proof and executable design.  This note strengthens the v118
support-fibre correlation: a separating dual can be correlated with a whole
linked context orbit by finite Boolean-cell counts, without enumerating the
support-fibre union element by element.  It requires exact multi-coordinate
projection membership/order queries and a word-bearing finite-group
self-reduction.  Task176 supplies the full and singleton base data; the lazy
multi-coordinate queries and the all-seven solve have not yet run.  No
correction, cofinal lift, fake, or Ihara witness is declared.

## 1. A dual correlation is a weighted union of fibres

Let

\[
 \Delta\leq G_1\times\cdots\times G_s
\tag{1.1}
\]

be the linked context image, with coordinate maps
\(\pi_i:\Delta\to G_i\).  Use the v118 notation for one normal-generator
word \(r\):

\[
 V_r(\delta)=\kappa(r)+
 \sum_{o\in\mathcal O_r}
 a_o e_{b_o,L_o\pi_{i_o}(\delta)h_o}.
\tag{1.2}
\]

Let \(\lambda\) be a finitely supported dual row.  For every occurrence
\(o\) and every support point \((b_o,g)\), the corresponding summand pairs
nontrivially only on the fibre

\[
 \pi_{i_o}(\delta)=L_o^{-1}g h_o^{-1}.
\tag{1.3}
\]

Combine equal constraints in (1.3), add their coefficients in the ground
field \(k\), and delete zero coefficients.  For each coordinate \(i\), this
gives a finite target set \(T_i\subseteq G_i\) and weights

\[
 c_i:T_i\longrightarrow k^\times.
\tag{1.4}
\]

Put \(K_r=\langle\lambda,\kappa(r)\rangle\).  Then the complete correlation
is exactly

\[
 \boxed{
 F_r(\delta)=\langle\lambda,V_r(\delta)\rangle
 =K_r+\sum_{i=1}^s\sum_{t\in T_i}
 c_i(t){\bf1}_{\pi_i(\delta)=t}.}
\tag{1.5}
\]

This is more information than the support union alone: it retains all
same-point coefficient additions and all cancellations between different
occurrences.

## 2. Exact Boolean cells

For each \(i\), choose a symbol \(*\) meaning that the coordinate avoids
every target in \(T_i\).  A cell pattern is

\[
 \eta=(\eta_1,\ldots,\eta_s),
 \qquad \eta_i\in T_i\cup\{*\}.
\tag{2.1}
\]

Define

\[
 C_\eta=
 \{\delta\in\Delta:
 \pi_i(\delta)=\eta_i\text{ if }\eta_i\ne *,
 \quad
 \pi_i(\delta)\notin T_i\text{ if }\eta_i=*\}.
\tag{2.2}
\]

These cells are disjoint and cover \(\Delta\).  Equation (1.5) is constant
on each cell, with value

\[
 \boxed{
 f(\eta)=K_r+\sum_{\eta_i\ne *}c_i(\eta_i).}
\tag{2.3}
\]

It remains to decide exactly which cells are nonempty.

For an ordered subset \(S\subseteq\{1,\ldots,s\}\), write

\[
 \pi_S:\Delta\longrightarrow\prod_{i\in S}G_i,
 \qquad D_S=\pi_S(\Delta).
\tag{2.4}
\]

For a partial assignment \(a=(a_i)_{i\in S}\), define

\[
 N(a)=
 \begin{cases}
  |\ker\pi_S|=|\Delta|/|D_S|,&a\in D_S,\\
  0,&a\notin D_S.
 \end{cases}
\tag{2.5}

For the empty assignment put \(N(\varnothing)=|\Delta|\).

Let

\[
 A_\eta=\{(i,\eta_i):\eta_i\ne *\},
 \qquad I_*(\eta)=\{i:\eta_i=*\}.
\tag{2.6}

A forbidden-choice assignment \(b\) consists of a subset
\(U\subseteq I_*(\eta)\) and one value \(b_i\in T_i\) for each \(i\in U\).

### Theorem 2.1 (WEIGHTED CONTEXT-CELL COUNT)

For every pattern \(\eta\),

\[
 \boxed{
 |C_\eta|
 =\sum_{U\subseteq I_*(\eta)}(-1)^{|U|}
   \sum_{(b_i)\in\prod_{i\in U}T_i}
   N\bigl(A_\eta\cup\{(i,b_i):i\in U\}\bigr).}
\tag{2.7}
\]

Consequently,

\[
 \boxed{
 F_r(\delta)=0\text{ for every }\delta\in\Delta
 \quad\Longleftrightarrow\quad
 f(\eta)=0
 \text{ for every }\eta\text{ with }|C_\eta|>0.}
\tag{2.8}
\]

If the right side fails, any nonempty cell with \(f(\eta)\ne0\) contains an
ACTIVE correction column.

#### Proof

First impose the equalities in \(A_\eta\).  For every star coordinate, remove
the union of its disjoint target fibres.  Inclusion-exclusion over the star
coordinates gives (2.7).  Terms choosing two distinct targets at the same
coordinate are empty, so it is enough to choose at most one value from each
\(T_i\).  Every remaining simultaneous equality locus is either empty or a
coset of \(\ker\pi_S\), and hence has the value (2.5).

The cells partition \(\Delta\), and (2.3) is the value of \(F_r\) on the
whole cell.  This proves (2.8) and the final assertion. \(\square\)

V118 Theorem 2.1 is the special case in which only the all-star complement
is counted.  Formula (2.7) also handles all cancellations inside the support
union, so no elementwise union scan is logically necessary.

## 3. Lazy multi-projection queries from an extension section

Use the authenticated extension of v125,

\[
 1\longrightarrow\Gamma\longrightarrow G
 \longrightarrow Q_0\longrightarrow1,
 \qquad \Delta=\Phi_{\rm all}(G).
\tag{3.1}
\]

For every coordinate subset \(S\) requested by (2.7), define

\[
 A_S=\Phi_S(\Gamma),
 \qquad
 L_S=\{q\in Q_0:\Phi_S(s(q))\in A_S\}.
\tag{3.2}
\]

V125 gives

\[
 |D_S|=|A_S|[Q_0:L_S].
\tag{3.3}
\]

For a particular target tuple \(t\), one has

\[
 \boxed{
 t\in D_S
 \quad\Longleftrightarrow\quad
 \text{for some }q\in Q_0,
 \ t\Phi_S(s(q))^{-1}\in A_S.}
\tag{3.4}
\]

Any witnessing \(q\), together with the stored Gamma adjustment in (3.4),
returns a source word for a section of \(t\).  Thus one shared scan of the
1,469,664 authenticated \(Q_0\) states, with the 243-state \(A_S\) lookup,
answers membership, order, section, and kernel queries for one requested
subset \(S\).  The answer can then be cached for every later dual iteration.

Only subsets appearing in (2.7) need to be built.  Precomputing all
\(2^{10}\) subsets is optional and is not part of the theorem.  A registered
cap which prevents a requested query from finishing gives
`UNKNOWN_RESOURCE`; it cannot be interpreted as zero correlation.

Task176 computes \(S=\mathrm{ALL}\) and all ten singletons and retains the
lossless Gamma/Q0 data needed for (3.2)--(3.4).  Those eleven families are a
base cache, not by themselves a proof of (2.8) for a dual involving several
linked coordinates.

## 4. Word-bearing extraction without blind Delta enumeration

The count (2.7) proves that an ACTIVE cell exists but a positive certificate
must also return an actual source word.  The following finite self-reduction
does so.

Start from the equality part of a positive cell.  Equations (3.3)--(3.4)
return a word-bearing section \(d\) and generators of the kernel \(K\), so
the equality locus is the coset \(dK\).  Choose a finite subgroup chain

\[
 K=K_0>K_1>\cdots>K_h=1
\tag{4.1}
\]

with explicit word-bearing transversals.  At a node \(vK_j\), partition it
into the child cosets of \(K_{j+1}\).  For each child, use the same
inclusion-exclusion formula as (2.7), replacing (2.5) by the exact order of
the intersection of that child coset with the requested coordinate fibres.
Finite-group coset-intersection algorithms decide each term and return a
section when it is nonempty.

Since the parent cell has positive count, at least one child has positive
count.  Choose the first such child in the frozen transversal order and
continue.  At \(K_h=1\), the selected element is in the desired cell.  The
product of the stored section and transversal words is a source word
\(u_\delta\).

### Theorem 4.1 (WORD-BEARING CELL SELF-REDUCTION)

Given exact word-bearing group operations, subgroup generators,
coset-intersection orders, and transversals as above, every pattern with
\(|C_\eta|>0\) has a deterministically recoverable source-word
representative.  No enumeration of all elements of \(\Delta\) is required.

#### Proof

The child cosets partition the parent.  Their cell counts are nonnegative
integers summing to the positive parent count, so a positive child exists.
Induction down (4.1) ends at a singleton of positive count.  Every group
operation was accompanied by its source word, so the singleton has the
claimed word. \(\square\)

This is a terminating exact algorithm, not a promise of a small runtime.
If a finite-group intersection or transversal step exceeds its registered
resource bound, the only sound terminal is `UNKNOWN_RESOURCE`.

For the concrete R07 extension (3.1), there is also a simpler word-bearing
fallback which needs no general coset-intersection package.  Scan the frozen
\(Q_0\) section order.  For the equality coordinates \(S\) of the chosen
cell, compute

\[
 a_q=t_S\Phi_S(s(q))^{-1}.
\tag{4.2}
\]

If \(a_q\notin A_S\), skip \(q\).  Otherwise the stored Gamma table returns
all \(\gamma\) with \(\Phi_S(\gamma)=a_q\); this set is one coset of
\(\Gamma_S^0\) and has at most 243 elements.  Test only those Gamma states
against the star inequalities.  The first passing pair gives the literal
source word

\[
 u_\delta=u_\gamma u_{s(q)}
\tag{4.3}
\]

in the frozen task157ee convention.  Because every element of \(G\) has a
Gamma-section expression, a positive cell must be found by the complete
scan.  The absolute fallback cap is

\[
 |\Gamma||Q_0|=243\cdot1{,}469{,}664=357{,}128{,}352
\tag{4.4}
\]

source pairs, but no \(\Delta\) element set is stored or deduplicated, and
the equality lookup normally removes most pairs.  This fallback is intended
only after (2.7) has already selected one positive ACTIVE cell; it is not a
replacement for exact cell counts on the negative branch.

## 5. Terminating all-seven column generation

Apply Sections 1--4 to the v110 stacked module

\[
 M_{H_1}\oplus M_{H_2}\oplus M_P\oplus k^2,
\tag{5.1}
\]

including the two exponent coordinates in \(\kappa(r)\).  Keep the PB3 and
PB4 presentation-boundary families separately typed.  Their complete dual
correlation is the singleton rule already used in task157eg; the linked
normal-generator family uses Theorem 2.1.

### Theorem 5.1 (CELL-EXACT ONE-WORD SELECTOR)

Assume:

1. the task175 raw formula, 6,441-row normal-generator roster, prefixes,
   signs, target, and boundary families are authenticated;
2. every multi-projection query requested by (2.7) is answered exactly;
3. every positive cell can be materialized by Theorem 4.1; and
4. direct column and word replay uses the same frozen convention as v110.

Then finite column generation decides the v110 membership

\[
 (-T_{\rm all},0,0)
 \in D_{\rm all}+\operatorname{span}
 \{V_{\delta,r}:\delta\in\Delta_{\rm all},r\in\mathcal R_\Omega\}.
\tag{5.2}
\]

On the positive branch it returns one explicit common correction word.  On
the negative branch it returns a dual row which has been proved to annihilate
every boundary and every linked correction column while pairing nontrivially
with the target.

#### Proof

Start with any authenticated independent column set.  If the target does not
reduce to zero, form a separating dual \(\lambda\).  Correlate it with every
boundary family and, for each of the 6,441 rows, use (1.5)--(2.8).  If a
nonzero correlation exists, Theorem 4.1 supplies an actual column outside the
current span; adding it raises rank.  The ambient space in (5.1) is finite
dimensional, so only finitely many rank increases are possible.

If the target eventually reduces to zero, recovery coefficients and the
source words multiply to the common word of v110.  If no family has a
nonzero correlation, the current dual annihilates the complete right side of
(5.2), and its nonzero target pairing is the exact separator. \(\square\)

The negative conclusion is only for the pinned word/roster/module in (5.2).
It is not a nonexistence theorem after enlarging the correction universe or
changing the base word.  A partially answered set of multi-projection
queries cannot support the negative branch.

## 6. Exact successor contract

The first all-seven solver after tasks175--176 should therefore proceed as
follows.

1. Build an initial sparse basis from the authenticated PB3/PB4 boundary
   columns and a deterministic small set of word-bearing correction columns.
2. Reduce the full H1/H2/ordered-pentagon target with both exponent rows.
3. For each nonzero dual, convert all 6,441 correlations to the merged
   weighted-fibre form (1.5).
4. Generate and cache only the multi-coordinate \(D_S\) queries demanded by
   the resulting cell formulas.
5. Add the canonical first ACTIVE boundary block or correction column and
   repeat until Theorem 5.1 terminates.
6. On success, print the single common word, replay all seven occurrences,
   and then solve the intrinsic v129 augmented \((d,\rho)\) equation rather
   than stopping at ambient depth-nine membership.

Independent checking must reconstruct the weighted constraints from the raw
Fox occurrence list.  It must not trust producer-supplied target sets,
cell counts, or an `ACTIVE` bit.  Mutations must cover a merged coefficient
cancellation, one multi-coordinate target, one inclusion-exclusion sign, one
kernel order, one complement cell, and one source-word transversal.

```text
DUAL AS WEIGHTED FIBRE INDICATORS:           PAPER_PROOF
BOOLEAN-CELL COUNT / CANCELLATION TEST:       PAPER_PROOF
LAZY EXTENSION-SECTION MULTI-QUERY:           PAPER_PROOF
WORD-BEARING CELL SELF-REDUCTION:             PAPER_PROOF
TERMINATING ALL-SEVEN COLUMN GENERATION:      PAPER_PROOF
TASK175 RAW BRIDGE:                           GHA RUNNING
TASK176 FULL/SINGLETON BASE CENSUS:           STATIC BUNDLE / NOT EXECUTED
LAZY MULTI-COORDINATE QUERIES:                NOT RUN
ALL-SEVEN COMMON WORD:                        NOT CONSTRUCTED
INTRINSIC (d,rho) SATURATION:                 NOT COMPUTED
COMPATIBLE COFINAL R07 LIFT:                  NOT CONSTRUCTED
FAKE / IHARA WITNESS:                         NOT DECLARED
```
