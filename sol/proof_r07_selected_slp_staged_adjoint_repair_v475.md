# R07: staged adjoint evaluation of the selected-SLP DAG, repaired (v475)

Author: Sol / 2026-09-03

Status: paper-closed resource repair for the Task601 leaf evaluator after GHA
run `33723160379`, incorporating the finite Task628 repair.  It changes only
the evaluation schedule of the same authenticated noncommutative DAG.  It does
not prune a source edge, identify actor paths by a finite quotient, or assert
an actual selected payload, fresh residual, grade decision, A0, fake, or Ihara
conclusion.  `verified=false`.

## 1. The observed failure and the mathematical issue

The packed Task601 producer completed the exact 8,059-offer route, selected
all 3,317 coefficients, copied the selected source graph, and entered its
reverse literal expansion.  At the time cap it reported

```text
processed                 159,383,552
pending                    4,440
current nonzero leaves       456
maximum actor-path length      21
RSS                    1,420,152,832 bytes
peak RSS               2,686,074,880 bytes
terminal                UNKNOWN_RESOURCE:time
```

The loop stored coefficients modulo three by the exact state key
`(node, freely-reduced actor-path)`, but removed a key and expanded it as soon
as it was encountered.  A later incoming edge could recreate the same key.
Thus algebraically cancelling contributions were repeatedly expanded along
many DAG paths before they met.  The terminal is not a memory obstruction and
is not evidence for an infinite graph.

## 2. The registered triangular stages

Use the exact Task601 node types

\[
 G_i,\quad L_i,\quad B_{a,i},\quad D_o,\quad O_{a,i},               \tag{2.1}
\]

for physical grade pivots, physical lower pivots, source character-block
pivots, source defects, and lifted-old source pivots.  The authenticated
constructors have only the following dependency arrows:

\[
\begin{array}{rcl}
G_i&\longrightarrow&G_j\ (j<i),\ L_j,\ B_{a,j},\ O_{a,j},\\
L_i&\longrightarrow&L_j\ (j<i),\ O_{a,j},\\
B_{a,i}&\longrightarrow&B_{a,j}\ (j<i),\ D_o,\\
D_o&\longrightarrow&O_{a,j}\ \text{or a literal leaf},\\
O_{a,i}&\longrightarrow&O_{a,j}\ (j<i)\ \text{or a literal leaf}.
\end{array}                                                        \tag{2.2}
\]

For an actor-origin edge the declared parent is also strictly earlier than
the child pivot.  Reduction edges have the same strict inequality.  These
inequalities must be checked against the canonical receipts; they are not
inferred from a `DAG` label.

A topological schedule refining (2.2) is therefore

```text
all G pivots in decreasing index;
all L pivots in decreasing index;
each B character in decreasing pivot index;
all D origins;
each O character in decreasing pivot index;
literal leaves.
```

The relative order of the independent L and B stages is immaterial.  The
displayed order is fixed for deterministic receipts.

## 3. Sparse path coefficients

Let \(W=F(x,y)\) in exact freely reduced word representation.  For every
nonterminal node \(v\), keep a finite map

\[
             A_v:W\longrightarrow\mathbf F_3.                     \tag{3.1}
\]

Initialize the maps of the selected physical grade roots with their exact
3,317 coefficients.  When stage \(v\) is reached, expand each nonzero
\((P,c)\in A_v\) through the same ordered Task601 constructor edges.  A
non-actor edge sends \(c\) with its registered scalar to the same path \(P\).
An actor or pure-\(Q_1\) edge sends it to the exact product

\[
                    \operatorname{red}(Pq),                         \tag{3.2}
\]

using the existing left-to-right word convention and the registered edge
word \(q\).  Contributions to a destination map are added modulo three;
zeros are deleted.  After expanding \(v\), release \(A_v\).  Literal outputs
are accumulated by exact `(seed, path)` keys.

An implementation may intern the words in (3.1) as integer path IDs.  The
interning table must be injective on exact freely reduced tuples, and the
leaf receipt must serialize the tuple rather than the transient ID.  No
finite-group endpoint, hash collision, or endpoint signature may identify
two words in this source calculation.

## 4. Schedule-independence theorem

### Theorem 4.1 (one expansion per accumulated state)

The staged algorithm of section 3 returns byte-for-byte the same final
coefficient map

\[
       \mu:(s,P)\longmapsto\mu_{s,P}\in\mathbf F_3                 \tag{4.1}
\]

as the pathwise expansion of every selected root through the authenticated
DAG.  Every nonzero `(node,path)` state is expanded at most once.

#### Proof

For a node \(v\), define its formal incoming coefficient at path \(P\) to be
the sum in \(\mathbf F_3\) of the weights of all root-to-\(v\) DAG paths whose
ordered actor labels freely reduce to \(P\).  This sum is finite because
(2.2) is acyclic.

Proceed through the fixed topological schedule.  Before \(v\) is processed,
every possible predecessor of \(v\) has already been processed and every
possible successor has not.  By induction, each predecessor map contained
its complete formal incoming coefficients when expanded.  The registered
linear edge rules and (3.2) therefore add exactly every root-to-\(v\) path
contribution to \(A_v(P)\).  No later node can send a contribution back to
\(v\).  Hence \(A_v(P)\) is complete when read, and expanding it once is
equal, by distributivity over \(\mathbf F_3\), to expanding all of its
individual path contributions.

At a literal edge the identical argument adds the complete coefficient to
the exact key `(seed,P)`.  Induction over all stages proves (4.1).  Since no
edge points to an already processed node, a state cannot be recreated after
its expansion. \(\square\)

This proof uses cancellation only between identical exact source paths.  It
does not use equality of current quotient endpoints and therefore preserves
the refinement-safe source witness required by v470--v471.

## 5. Result-dependent resource contract

Let \(N_v=|\operatorname{supp}A_v|\), let \(U\) be the number of interned
exact words, and let \(E_{\mathrm{reached}}\) be the number of processed
pairs `(nonzero accumulated state, outgoing constructor edge)`, counted with
multiplicity over states.  Thus it counts state-edge traversals, not merely
distinct constructor edges.  The staged work is charged to

\[
        \sum_v N_v+E_{\mathrm{reached}},                            \tag{5.1}
\]

not to the number of root-to-leaf DAG paths.  This is a result-dependent
bound; the theorem does not assert that (5.1) is uniformly small.  Exact-word
construction and serialization, dictionary storage, and resident memory are
separately controlled by the telemetry and caps below.

The producer and checker must report, per stage, the processed node count,
nonzero accumulated-state count, state-edge traversals, number of exact
interned paths, maximum path length, maximum simultaneously live entries,
final leaf count, wall time, RSS, peak RSS, and durable bytes.  Explicit caps
on accumulated states, interned words, path length, wall time, RSS, and durable
bytes fail as `UNKNOWN_RESOURCE`.  A partial leaf map is never a payload.

For independence, the producer and checker must not import one another's
scheduler or word interner.  The checker independently authenticates the
same graph, rechecks all strict arrows in (2.2), recomputes (4.1), and compares
the complete compact leaf byte stream.  Bounded fixtures must include a
diamond whose two equal `(node,path)` contributions cancel before expansion,
a later third contribution, an actor-boundary free reduction, coefficient
two, an illegal forward edge, and a cycle/processed-stage reinsertion attempt.

## 6. Claim boundary

```text
RUN 33723160379:                       UNKNOWN_RESOURCE:time
CAUSE:                                 PATHWISE RE-EXPANSION BEFORE COALESCENCE
STAGED EXACT-PATH ADJOINT:              PAPER-CLOSED (TASK628 REPAIR APPLIED)
SOURCE EDGE/PATH PRUNING:               NONE
CURRENT-ENDPOINT COALESCENCE:           FORBIDDEN HERE
ACTUAL PACKED SELECTED-SLP PAYLOAD:     NOT YET PRODUCED
FRESH RHO2 / NEXT GRADE:                NOT YET COMPUTED
A0 / COMMON / COFINAL / FAKE / IHARA:   NOT DECLARED
verified:                               false
```

`R07_SELECTED_SLP_STAGED_ADJOINT_V475_PAPER_CLOSED`
