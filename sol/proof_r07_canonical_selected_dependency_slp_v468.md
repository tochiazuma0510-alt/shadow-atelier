# R07: canonical noncommutative selected-dependency SLP (v468)

Author: Sol / 2026-09-03

Status: candidate constructive theorem. This note separates the exact
common-source SLP required after the grade-one MEMBER result from the
quotient-specific adjoint coefficient pass of v467. It repairs a concrete
implementation ambiguity: coefficients may coalesce while evaluating one
associated-grade row, but dependency edges may not be deleted or combined in
the source witness. No actual SLP payload, grade-two residual, A0, COMMON,
cofinal lift, fake or Ihara conclusion is asserted. `verified=false`.

## 1. Two objects which must not be identified

Let \(F\) be the registered free source, with the normal filtration and actor
stability of v465. Let

\[
 b_j=\sigma_j\left(z_{o(j)}-
        \sum_{(p,q)\in E_j}^{\longrightarrow}q b_p\right),
 \qquad \sigma_j\in\{1,2\},                         \tag{1.1}
\]

be one authenticated accepted-node record. The arrow is the reducer's
recorded edge order. There are two different constructions attached to
(1.1).

1. The **source syntax** recursively replaces \(z_{o(j)}\), every earlier
   \(b_p\), every sign and every actor by literal group operations in \(F\).
   It is one noncommutative word SLP.
2. At one fixed quotient and one fixed associated grade, the **adjoint
   evaluation** propagates scalar weights backwards through (1.1), as in
   v467. Equal quotient-specific states may then be added in
   \(\mathbf F_3\), including cancellation to zero.

Only the first object is the common-source witness. The second is a derived
evaluation receipt. In particular,

\[
 \boxed{\text{zero total coefficient at one grade does not delete an SLP
 edge.}}                                                   \tag{1.2}
\]

Indeed, two ordered factors whose grade-\(d\) classes cancel can have a
nonzero commutator or different grade-\((d+1)\) contribution. Replacing
their ordered product by the empty word therefore changes the lift which the
next residual must measure.

## 2. Canonical typed constructors

For \(a\in\mathbf F_3\), retain v465's fixed integral representative

\[
 [0]=0,\qquad[1]=1,\qquad[2]=-1.                    \tag{2.1}
\]

Write `Pow(T,a)` for the empty word, \(T\), or \(T^{-1}\) according to
(2.1); write `Prod` for an ordered product, `Act(P,T)` for the registered
literal actor/conjugation operation with exact actor word \(P\), and
`Compose` for the registered correction composition. None of these nodes is
commutative.

For every accepted owner node \(j\), define

\[
 \mathcal W_j=
 \operatorname{Pow}\!\left(
   \operatorname{Prod}\!\left(
      \mathcal Z_{o(j)},
      \bigl(\operatorname{Pow}(\mathcal W_p,-q)\bigr)_{
        (p,q)\in E_j}^{\longrightarrow}
   \right),\sigma_j
 \right).                                             \tag{2.2}
\]

Formula (2.2), including origin first, the complete ordered edge list, and
the outer normalizing power, is the canonical syntax. Sharing
\(\mathcal W_p\) as a DAG reference is allowed; deleting a reference because
another reference has the opposite grade coefficient is not.

The R07 owners are expanded with the following typed order.

### 2.1 Physical grade and lower owners

For a physical-grade node whose origin is a block pivot, \(\mathcal Z\) is
that block-pivot SLP. If its origin is an old connection, first form the
exact old-origin SLP and then append, in the recorded lower-reduction order,
the signed physical-lower pivot SLPs used to kill its complete lower image.
This complete ordered product is \(\mathcal Z\) in (2.2). The node's own
physical-grade reductions are appended only afterward by (2.2).

A physical-lower node has its exact old origin followed by all recorded
earlier lower reductions, and then its normalizing power. Thus its SLP
represents both the normalized lower row and its stored grade companion. A
regular lower block alone is not substituted for the normalized exponent,
PB3 boundary or auxiliary coordinates.

### 2.2 Character block owner

A character-block node has either a defect origin or an actor-parent origin.
For an actor parent, its origin is `Act(P,W_parent)` with the exact registered
one-letter actor word \(P\). For a defect origin, apply the four exact
pure-\(Q_1\) actor words in their registered character order, with their
registered character signs, to the referenced defect SLP. Then append every
earlier block reduction in its stored order and apply the node scale as in
(2.2).

### 2.3 Defect and old owners

A seed defect is the exact compact seed followed by the inverses/powers of
all old pivots in its referenced `seed_reductions` expression, in stored
order. A transition defect is the exact acted old pivot followed by the
inverses/powers of all old pivots in its referenced `actor_transitions`
expression, again in stored order.

An old accepted node starts with either its exact projected-seed origin or
its exact actor-parent origin. It then appends every earlier old reduction
and finally applies its scale as in (2.2). Projected seeds retain all four
literal pure-\(Q_1\) actor factors in registered order. Actor parents retain
the exact actor word.

The `seed_reductions` and `actor_transitions` references may contain arbitrary
old-pivot identifiers from the completed old owner. This causes no cycle:
the type edge has already descended from block defect to the completed old
owner, whose own accepted-node ancestry is acyclic. Inside any one accepted
owner, reduction and actor-parent edges point to earlier accepted nodes.

## 3. Selected closure and three roots

Let the authenticated target reduction return the ordered list

\[
 ((j_1,a_1),\ldots,(j_m,a_m)),\qquad m=3317.          \tag{3.1}
\]

The selected physical closure is the least **graph-reachable** set containing
all \(j_i\) and every child reference in (2.2), including all reached lower
references. Source attachment then takes the graph-reachable closure through
the block, defect and old rules of Section 2. Reachability ignores scalar
cancellation. A child with a nonzero recorded local edge is retained even if
the sum of all incoming associated-grade weights on that child is zero.

Define, in the exact order of (3.1),

\[
 C_T=\operatorname{Prod}
   \bigl(\operatorname{Pow}(\mathcal W_{j_1},a_1),\ldots,
    \operatorname{Pow}(\mathcal W_{j_m},a_m)\bigr).   \tag{3.2}
\]

Let \(C_{<1}\) be the exact ordered SLP encoded by the sealed
`canonical_solution["terms"]`; it is not sorted or recanonicalized. The
complete correction is

\[
 C_1=\operatorname{Compose}(C_{<1},C_T)              \tag{3.3}
\]

in the registered composition order. The tuple consisting of the selected
node/edge tables, the reached non-DAG expressions, exact seed and actor words,
and roots (3.2)--(3.3) is the canonical selected-dependency payload.

## 4. Exact-word theorem

### Theorem 4.1 (well-defined selected source word)

Assume the authenticated records obey the type and earlier-node conditions
above. Then the payload of Section 3 is a finite acyclic SLP and determines
one element \(c_1\in F\). It is independent of the quotient in which it is
later evaluated.

#### Proof

Order the types

\[
 \text{physical grade} > \text{physical lower/block} >
 \text{defect} > \text{old} > \text{literal leaves}.          \tag{4.1}
\]

Every cross-type edge strictly descends (4.1). Within an owner, every
reduction or actor-parent edge has a smaller accepted-node number.
Lexicographic induction on type and node number therefore terminates and
assigns a free-group element to every reached node. Ordered product, inverse,
actor and composition are literal group operations, so (3.2)--(3.3) define
one \(c_1\in F\). No quotient has entered the construction. \(\square\)

### Theorem 4.2 (associated-grade correctness)

Under v465's filtration and induced-action hypotheses, evaluation of this
exact SLP in the registered grade-one module has class

\[
 [C_T]_1=\sum_{i=1}^{3317}a_i b_{j_i}.               \tag{4.2}
\]

If the complete lower/auxiliary direct replay vanishes and the authenticated
MEMBER equation equals the registered residual, \(C_1\) hits the complete
precision-one target.

#### Proof

Apply the quotient homomorphism \(F^1\to F^1/F^2\) to (2.2). Ordered product,
inverse and literal actor action become exactly the addition, negation and
registered linear action in (1.1). Induction gives
\([\mathcal W_j]_1=b_j\), and (3.2) gives (4.2). Old/lower nodes not known
individually to be pure are licensed only by their stipulated complete
physical direct replay, exactly as in v465 Proposition 2.2. Composing with
the separately replayed prior root proves the final assertion. \(\square\)

### Corollary 4.3 (naturality, not uniform solvability)

For a registered refinement \(Q'\to Q\), evaluation of the same syntax
satisfies

\[
 r_{Q',Q}(\operatorname{ev}_{Q'}C_1)
     =\operatorname{ev}_{Q}C_1.                    \tag{4.3}
\]

This follows by structural induction. It makes \(C_1\) one compatible
source instruction, but it does not assert that (4.2) remains the required
target equation in every refinement. The fresh defect must be recomputed at
each next grade, and all-edge relative-kernel surjectivity remains separate.

## 5. Legal adjoint compression

At a fixed current quotient, after every reached literal endpoint has been
checked to be one, v467 permits a reverse scalar pass through the same
authenticated syntax. Its state table may combine equal
\((\text{node},\text{actor path})\) keys and discard a key whose total scalar
is zero. The resulting weighted literal-origin map evaluates the current
Fox row and may be used to compute the fresh grade-two residual efficiently.

This derived map must carry a digest of the canonical SLP parent and be typed

```text
quotient_specific_evaluation = true
common_source_witness = false
```

It may not replace the selected graph, roots (3.2)--(3.3), or the separate
source-kernel replay. The canonical SLP remains unchanged when this map is
discarded and recomputed at another quotient.

## 6. Minimal independent checker obligations

An independent consumer accepts a selected-dependency payload only after it:

1. authenticates the decision, prepare, four blocks, compact tables and exact
   3317-entry root list;
2. checks record widths, original node identifiers, scales, ordered edge
   intervals and all earlier-node/type acyclicity conditions;
3. marks reachability from (3.1) without scalar aggregation and proves that
   the exported node set contains exactly every reached child, including
   lower links and non-DAG seed/transition expressions;
4. checks exact seed words, actor words, all local child orders, \(C_T\),
   \(C_{<1}\), and \(C_1\);
5. reproduces the grade-one packed basis and MEMBER equality; and
6. directly replays all reached endpoints and the complete physical
   lower/auxiliary and precision-one target equations before constructing
   \(\rho_2\).

A mod-three flow-conservation check is useful for a derived adjoint receipt,
but it cannot replace item 3: a pair of locally present edges may have zero
net flow while remaining load-bearing in the noncommutative SLP.

The payload size is \(O(V+E)\) for the selected dependency graph. Memoized
evaluation does not materialize the flat free word. Resource exhaustion is
UNKNOWN_RESOURCE and never authorizes pruning a dependency.

```text
CANONICAL SELECTED GRAPH -> ONE FREE-SOURCE SLP:  PAPER-CLOSED
COEFFICIENT CANCELLATION INSIDE WITNESS GRAPH:    FORBIDDEN
COEFFICIENT CANCELLATION IN CURRENT ADJOINT ROW:  ALLOWED AFTER ENDPOINT GATES
CURRENT GRADE-ONE CLASS OF THE SLP:               PAPER-CLOSED UNDER REPLAY HYPOTHESES
NATURAL EVALUATION AT REGISTERED REFINEMENTS:     PAPER-CLOSED
ACTUAL SELECTED SLP PAYLOAD / DIRECT REPLAY:       NOT YET PRODUCED
FRESH GRADE-TWO RESIDUAL / REMAINING FIVE GRADES: NOT YET COMPUTED
A0 / COMMON / COFINAL LIFT / FAKE / IHARA:        NOT DECLARED
verified:                                          false
```

`R07_CANONICAL_SELECTED_DEPENDENCY_SLP_V468_CANDIDATE`
