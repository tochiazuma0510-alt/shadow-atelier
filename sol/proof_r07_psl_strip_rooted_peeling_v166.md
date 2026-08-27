# R07 root-seeded propagation for higher PSL-strip cores v166

Author: Sol / 2026-08-27

Status: paper theorem.  This note combines v52 leaf elimination with a
root-seeded propagation on an arbitrary labelled $PSL(2,8)$ strip core.  It
is an exact finite decision acceleration, not a nonemptiness theorem.  No
actual R07 strip roster is evaluated here, and no compatible lift, fake, or
Ihara witness is declared.

## 1. Ordered strip system and the v52 core

Put

$$
 S=PSL(2,8),\qquad |S|=504.
\tag{1.1}
$$

Use the v48/v52 ordered constraints

$$
 E_a(v)=b_{a,0}\alpha_{a,1}(v_{i_1})^{\epsilon_1}b_{a,1}
 \cdots
 \alpha_{a,d_a}(v_{i_{d_a}})^{\epsilon_{d_a}}b_{a,d_a}=1,
\tag{1.2}
$$

where every $\alpha_{a,j}$ is an automorphism of $S$, every sign is
$\pm1$, and repeated occurrences are retained in the incidence multigraph.
The constraints include the complete common-word hexagon and ordered A.18
blocks; their factors are never commuted.

First apply the canonical v52 variable-leaf elimination to the complete
system.  Write $\mathcal G_{\rm core}$ for its obstruction core, $V$ for the
nonisolated variables of that core, and $f$ for the unpivoted variables that
v52 leaves isolated.  The v52 theorem gives

$$
 \operatorname{Sol}(\mathcal G)
 \simeq
 \operatorname{Sol}(\mathcal G_{\rm core})\times S^f.
\tag{1.3}
$$

All v52 pivot values are recovered later in reverse order.  Thus it is enough
to accelerate the exact solve of $\mathcal G_{\rm core}$.

## 2. Root-seeded propagation

Choose a root set $R\subseteq V$ and assign

$$
 r\in S^R.
\tag{2.1}
$$

Mark the roots as known and substitute every root occurrence literally in
every active ordered constraint.  Now repeat the following deterministic
operation.

1. Choose the least active constraint having exactly one occurrence of an
   unknown variable in its ordered word.
2. That occurrence determines a pivot variable.  Solve the constraint
   uniquely for that pivot by v52 Lemma 2.1.
3. Mark the pivot known and substitute all of its occurrences literally in
   every other active constraint.
4. Retire the constraint used to solve the pivot, retaining it for final
   direct replay.

The phrase "exactly one occurrence" is essential: parallel or repeated
occurrences count separately.  At every step all other factors in the pivot
constraint are known, so the unique-solution calculation is legitimate even
when the pivot has further occurrences in other constraints.  The order of
pivots depends only on the typed incidence data and $R$, not on the values of
$r$.

### Definition 2.1 (propagating root set)

A set $R\subseteq V$ is a **propagating root set** if the operation above
eventually marks every variable of $V$ known.  Constraints not used as pivots
then contain only known values; retain them in authenticated order as the
residual replay list $C_R$.

Every finite core has a propagating root set: $R=V$ is the semantic fallback.
The useful invariant is

$$
 \boxed{r_{\rm prop}=\min\{|R|:R\text{ is a propagating root set}\}.}
\tag{2.2}
$$

A total order makes the lexicographically first minimum set canonical.
Computing the minimum may itself be expensive; any authenticated propagating
root set gives a valid upper bound and exact solver.

## 3. Exact root predicate

Fix a propagating root set $R$ and $r\in S^R$.  Perform the deterministic
forward propagation.  Define

$$
 P_R(r)=1
\tag{3.1}
$$

if and only if every constraint in $C_R$ evaluates literally to the identity.
Pivot constraints are replayed as well, although they hold by construction.

After a successful core solve, choose $s\in S^f$ for the v52-isolated free
variables and reconstruct the v52 pivots in reverse order.  If a split onto
detector is present, define

$$
 P_R^{\rm acc}(r,s)=1
\tag{3.2}
$$

if and only if $P_R(r)=1$ and the complete global detector is nontrivial on at
least one member of its registered generating roster after this full
reconstruction.  The detector is not assumed componentwise and is not
assumed independent of $s$.

### Theorem 3.1 (ROOT-PROPAGATION BIJECTION)

For every propagating root set $R$, restriction to the roots, followed by the
deterministic propagation above, gives a bijection

$$
 \boxed{
 \operatorname{Sol}(\mathcal G_{\rm core})
 \simeq
 \{r\in S^R:P_R(r)=1\}.}
\tag{3.3}
$$

Consequently

$$
 \boxed{
 \operatorname{Sol}(\mathcal G)
 \simeq
 \{r\in S^R:P_R(r)=1\}\times S^f.}
\tag{3.4}
$$

With a split onto gate, the complete accepted set is identified with

$$
 \boxed{\{(r,s)\in S^R\times S^f:P_R^{\rm acc}(r,s)=1\}.}
\tag{3.5}
$$

#### Proof

Fix the root values.  At one propagation step the selected ordered constraint
has a single unknown occurrence, so it has the form

$$
 A\,\alpha(v)^{\epsilon}B=1
\tag{3.6}
$$

with $A,B$ already known.  Since automorphisms and inversion are bijections,
there is exactly one pivot value.  Literal substitution preserves order and
all of the pivot's other constraints.  Induction therefore gives one and only
one value for every nonroot core variable.

A complete core solution restricts to roots $r$ and, by uniqueness at every
pivot, its other values equal the propagated ones.  Its unused constraints
are satisfied, hence $P_R(r)=1$.  Conversely, if $P_R(r)=1$, all pivot
constraints hold by construction and all remaining constraints hold by the
definition of $P_R$.  The propagated tuple is therefore a core solution.
The two operations are inverse, proving (3.3).

Equation (3.4) follows from the v52 bijection (1.3).  Evaluating the literal
global detector only after choosing $s$ and completing the v52 reverse
reconstruction gives (3.5). $\square$

### Corollary 3.2 (EXACT HIGHER-CORE COMPLEXITY)

The relation part of a higher strip core is decided by at most

$$
 \boxed{504^{|R|}}
\tag{3.7}
$$

root assignments for any chosen propagating root set $R$, followed by
linear-size ordered propagation and direct replay.  A complete empty
enumeration is an exact obstruction for the full typed relation core, not a
restricted-lane miss.

Using a minimum propagating root set replaces the v52 fallback
$504^{u_{\rm core}}$ by $504^{r_{\rm prop}}$.  This is a relation-solving
bound.  If the global onto detector genuinely depends on the $f$ isolated
variables, an unoptimized exhaustive accepted-set decision can still require
up to $504^{|R|+f}$ pairs $(r,s)$; any sharper detector treatment must be
proved separately.

## 4. Recovery of the earlier lanes

1. If v52 removes every constraint, the core is empty, $R=\varnothing$, and
   Theorem 3.1 reduces exactly to v52.
2. For a connected simple alternating cycle, choose any one core variable as
   root.  Each adjacent constraint then has one unknown occurrence; choosing
   the least propagates successively around the broken cycle.  The last
   unused constraint is precisely the fixed-point equation $F_C(r)=r$.
   Thus Theorem 3.1 specializes to the 504-root solver of v77.
3. For disjoint cycles, one root per component gives the product of the v77
   fixed-point sets, followed by the same global onto detector.
4. For a higher core, a greedy structural procedure may add a root whenever
   propagation stalls, then resume.  It terminates no later than $R=V$ and
   gives a valid exact bound, although it need not attain (2.2).

Thus root-seeded propagation does not introduce a new solution notion.  It
is a single exact acceleration after v52, covering simple cycles and arbitrary
residual cores.

## 5. Authentication and GHA sharding contract

For one actual nonabelian chief edge, a positive or negative receipt must
retain:

1. the complete v48 typed occurrence multigraph, including parallel and
   repeated occurrences, signs, inner conjugators, and field automorphisms;
2. the complete canonical v52 peel record and its direct replay;
3. the chosen root set and a structural replay that it satisfies Definition
   2.1;
4. the canonical root-propagation pivot order;
5. every tested root tuple in authenticated order, or a complete sharded
   coverage manifest with disjoint intervals; for an accepted-set decision,
   the analogous coverage of every required isolated tuple $s$;
6. the literal residual list $C_R$, every propagated value, and direct
   equation replay for every accepted tuple; and
7. for a split edge, the global detector values on the same fully
   reconstructed assignments.

Sharding may partition the $504^{|R|}$ root tuples.  No shard miss is a
negative result until the disjoint coverage manifest is complete and an
independent checker replays it.  This is the natural GHA parallelization of
the perfect-core gate.

## 6. Exact boundary

This theorem makes every finite higher core decidable with a potentially much
smaller exponent.  It does not prove that $P_R$ or $P_R^{\rm acc}$ is
nonempty at every cofinal edge.  The actual R07 isolated strip occurrence
rosters are still required, and their outcomes must be interleaved with the
abelian/cyclic selectors.

```text
ROOT PROPAGATION FOR ARBITRARY PSL CORE:            PAPER_PROOF
V52 AND SIMPLE-CYCLE LANES AS SPECIAL CASES:        PAPER_PROOF
COMPLETE NEGATIVE CERTIFICATE AFTER ROOT COVERAGE:  PAPER_PROOF
GHA SHARDING OVER ROOT TUPLES:                      EXACT CONTRACT
ACTUAL R07 PROPAGATION NUMBERS / ACCEPTED SETS:     NOT COMPUTED
ALL-EDGE PERFECT-CORE NONEMPTINESS:                 OPEN
COMPATIBLE COFINAL R07 LIFT / FAKE / IHARA:         NOT DECLARED
```

`R07_PSL_STRIP_ROOT_PROPAGATION_V166_PAPER_GRADE`
