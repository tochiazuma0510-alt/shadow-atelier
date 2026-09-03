# R07: reverse-selected physical ancestry extraction (v466)

Author: Sol / 2026-09-03

Status: candidate constructive theorem written after Task595 returned the
grade-one MEMBER candidate.  It specifies how to recover the exact selected
physical SLP of v465 with one bounded reroute and one reverse marking pass,
without serializing the full merge JSON or flattening a group word.
It does not promote the candidate result or prove later-grade success.
verified=false.

## 1. Frozen deterministic echelon

Let \(z_1,\ldots,z_N\) be the registered physical rows in their frozen order.
For Task595, \(N=8059\).  A deterministic echelon accepts some rows as
\(b_0,\ldots,b_{r-1}\).  When \(b_j\) is accepted, retain

\[
 b_j=\sigma_j\left(
       z_{o(j)}-\sum_{p<j}q_{jp}b_p
      \right),\qquad \sigma_j\in\{1,2\}.                       \tag{1.1}
\]

Here \(o(j)\) is the logical origin, and the list of pairs
\((p,q_{jp})\) is retained in the exact order in which the reducer used the
pivots.  The row bytes themselves are already in the Task595 basis artifact.
The ancestry transcript therefore needs only:

\[
 (o(j),\sigma_j;\,(p,q_{jp})_{\rm ordered}).                   \tag{1.2}
\]

The same convention is used for the lower-first owner.  A grade origin coming
from an old row additionally points to the ordered lower reductions used to
make its complete lower image zero.

Because every reduction edge has \(p<j\), (1.2) is an acyclic presentation.
No actor orbit or source block is recomputed by this statement.

## 2. Transcript construction is a replay, not a new search

Rerun the exact frozen stream with the exact Task595 reducer and input-state
digests.  At each accepted pivot, append (1.2) to a compact transcript before
discarding the temporary Python reduction list.  A suitable lossless layout
is:

1. one fixed record per accepted node containing origin, scale and the offset
   of its edge interval;
2. one contiguous edge array containing a uint16 earlier-pivot index and one
   trit coefficient per edge; and
3. separate fixed records and an edge array for the lower-first owner.

The accepted ranks \(1661\) and \(5044\) are below \(2^{16}\), so uint16
pivot indices are exact.  The run must reproduce the Task595 basis SHA-256,
pivot leads, ranks and target coefficients.  Any mismatch is
UNKNOWN_INPUT, never a second mathematical answer.

The transcript can be append-only and digest-chained.  It never contains the
48,384-trit degree-two rows, a separating dual, expanded source words, or the
unselected transition presentation.  Thus this replay performs exactly the
measured finite grade-one route plus compact edge writes.

## 3. Reverse marking theorem

Let the MEMBER reduction be

\[
 \rho_1=\sum_{j=0}^{r-1}a_jb_j.                               \tag{3.1}
\]

Initialize a bit vector \(S\) by \(S_j=1\) precisely when \(a_j\ne0\).
Visit \(j=r-1,r-2,\ldots,0\).  Whenever \(S_j=1\), retain node \(j\) and all
of its ordered edge records, and set \(S_p=1\) for every edge
\((p,q_{jp})\) with \(q_{jp}\ne0\).  Apply the identical rule to every
lower-owner node reached from a selected old-connection origin.

### Theorem 3.1 (exact selected closure)

At termination, \(S\) is the least ancestry-closed set containing every
nonzero root in (3.1).  The retained records define exactly the SLP obtained
from (1.1) and (3.1), in the original product, inverse and normalization
order.

#### Proof

Every edge decreases the node number, so the reverse pass encounters a node
only after all possible later parents have had an opportunity to mark it.
Induction downward shows that every descendant of a selected root is marked.
Conversely, the procedure marks a node only as a root or through an edge from
an already marked node, proving minimality.  Replacing each retained equation
(1.1) by the ordered SLP rule of v465 gives the same rooted acyclic syntax;
no factor is commuted or collected. \(\square\)

The theorem deliberately marks an edge even if later associated-grade
coefficients might cancel.  Removing such an edge by linear cancellation
would generally change the exact higher-grade word.  The safe compression is
dependency pruning, not commutative flattening.

## 4. Attaching source ancestry

Each retained physical origin has one of two forms:

1. a selected old-connection row, together with its reached lower-owner
   reductions; or
2. a selected basis row from one of the four exhausted source-character
   blocks.

Follow only these origins into the already sealed prepare/block ancestry.
For every reached block node, retain its ordered reduction edges, scale and
origin.  For every reached old node, retain its reached defect_origin and the
specific seed_reductions or actor_transitions expression referenced there.
Continue until exact compact-seed, prior-correction and literal-actor leaves
are reached.

This second reverse closure is again acyclic by the registered pivot and
actor-transition orders.  Its output, joined to the selected physical
closure, is precisely the canonical payload required by v465 Section 4.

## 5. Replay obligations

Before the SLP is used at grade two, an independent interpreter must:

1. authenticate the Task595 decision and every prepare/block parent digest;
2. reproduce the packed grade-one basis and MEMBER equality;
3. check each reached lower-first SLP against the complete lower and
   auxiliary zero target and its stored grade row;
4. evaluate the selected update \(C_T\) in all eleven occurrences;
5. compose it in the fixed order with the authenticated prior correction
   \(C_{<1}\), producing the complete root \(C_1\); and
6. after the complete precision-one equality, evaluate this same \(C_1\)
   through degree two and compute the fresh residual \(\rho_2\).

The source-kernel assertion required by a later v395 edge remains a distinct
direct source-reduction replay.  Physical lower zero is not substituted for
that assertion.

## 6. Complexity and v220 boundary

The reroute has the same \(N=8059\) row arithmetic as Task595.  Transcript
space is linear in the number of accepted nodes plus recorded reduction
edges.  Reverse marking is linear in that transcript and uses two bit vectors
of ranks \(1661\) and \(5044\).  Selected source attachment is linear in the
reached sealed subgraphs.  There is no flat-word length term.

    TASK595 GRADE-ONE MEMBER:               CANDIDATE RESULT
    COMPACT PHYSICAL TRANSCRIPT:            CONSTRUCTIVELY SPECIFIED
    LEAST SELECTED PHYSICAL SLP CLOSURE:    PAPER-CLOSED
    COMPLETE SOURCE SLP AND DIRECT REPLAY:  NOT YET PRODUCED
    FIRST RUNG 1/6:                         NOT YET PROMOTED
    LATER GRADES / ALL-EDGE SURJECTIVITY:   NOT PROVED
    A0 / COMMON / COFINAL LIFT:              NOT DECLARED
    FAKE / IHARA:                           NOT DECLARED

