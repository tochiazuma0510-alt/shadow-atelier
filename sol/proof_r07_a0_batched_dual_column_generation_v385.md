# R07 A0 batched dual column generation v385

Author: Sol / 2026-08-30

Status: paper justification for replacing the one-column selector in the A0
positive boundary oracle by deterministic batched insertion.  It changes the
search order but not the generated column universe, membership question, or
certificate semantics.  Implementation and production replay remain open.
No finite common word, negative, lift, fake, or Ihara witness is asserted.
\(\mathtt{verified=false}\).

## 1. The finite A0 universe and the actual bottleneck

Let \(k=\mathbf F_3\), let \(V\) be the finite A0 sparse row space, let
\(t\in V\) be the fixed target, and let \(S\subseteq V\) be the span of the
authenticated old rows and every accepted actual row.  The exact echelon
owner supplies, whenever \(t\notin S\), a functional

\[
 \lambda\in V^*,
 \qquad \lambda(S)=0,
 \qquad \lambda(t)\ne0.
\tag{1.1}
\]

The boundary roster is finite.  Blocks 1 and 2 use the PB3 quotient of order
81 and have two relators each.  Block 3 uses the PB4 quotient of order

\[
 583{,}152{,}628{,}325{,}845{,}597{,}028{,}352
\tag{1.2}
\]

and has eleven relators.  Therefore the exact translated-boundary roster has

\[
 \boxed{
 |\Omega_B|=4\cdot81+11\cdot
 583{,}152{,}628{,}325{,}845{,}597{,}028{,}352
 =6{,}414{,}678{,}911{,}584{,}301{,}567{,}312{,}196.}
\tag{1.3}
\]

The correction roster is finite as well.  Its naive row--group product has

\[
 6{,}441\cdot357{,}128{,}352
 =2{,}300{,}263{,}715{,}232
\tag{1.4}
\]

indices before the weighted-support theorem shortens the query made for a
particular dual.

The v23 owner does not enumerate (1.3).  Its complete 104-descriptor
convolution computes the finite active set

\[
 A_\lambda=
 \{\omega\in\Omega_B:\lambda(c_\omega)\ne0\},
\tag{1.5}
\]

where \(c_\omega\) is the exact translated boundary column.  The current hot
path then executes

~~~text
selected = min(accumulated) if accumulated else None
~~~

and reconstructs only that one column.  Run 33267817818 committed 8,727
nonempty epochs and 8,727 winner reconstructions.  Thus it rebuilt a new
separating dual after every single rank increment and never reached the
correction oracle.

## 2. Batch insertion is mathematically sound

Fix an integer \(b\geq1\).  Give \(\Omega_B\) its existing canonical order and
let \(C_\lambda\) be the first \(\min(b,|A_\lambda|)\) indices of
\(A_\lambda\).  Materialize their exact columns in that order.  Starting from
\(S_0=S\), put

\[
 S_j=S_{j-1}+k c_{\omega_j}
 \qquad(\omega_j\in C_\lambda),
\tag{2.1}
\]

and retain \(c_{\omega_j}\) precisely when its exact echelon remainder modulo
\(S_{j-1}\) is nonzero.

### Theorem 2.1 (SAFE BATCHED DUAL COLUMN GENERATION)

The batched update has the following properties.

1. If \(A_\lambda\ne\varnothing\), then the first materialized column is
   independent of \(S\), so the batch raises rank at least once.
2. After the batch, the stored echelon space is exactly

   \[
    S'=S+\operatorname {span}_k
       \{c_\omega:\omega\in C_\lambda\}.
   \tag{2.2}
   \]

3. Discarding a later zero remainder loses no span and no possible target
   representation.
4. If exact reduction gives \(t\in S'\), expanding the formal DAG gives an
   exact A0 expression in authenticated old and materialized boundary columns.
5. If \(A_\lambda=\varnothing\), then every boundary column lies in
   \(\ker\lambda\).  Hence no boundary-only extension can put \(t\), for which
   \(\lambda(t)\ne0\), into the span; advancing to the correction oracle is
   sound.

#### Proof

For every \(\omega\in A_\lambda\), (1.5) gives
\(\lambda(c_\omega)\ne0\), whereas (1.1) gives \(\lambda(S)=0\).  Therefore
\(c_\omega\notin S\), proving item 1.  Exact sequential echelon insertion is
Gaussian elimination, so induction on \(j\) proves (2.2).  A zero remainder is
equivalent to membership in the already stored span, proving item 3.  Formal
ancestry records the same elementary row operations, which proves item 4.
Finally, emptiness of the complete active set means
\(\lambda(c_\omega)=0\) for every \(\omega\in\Omega_B\).  The span of all
boundary columns is therefore contained in \(\ker\lambda\), while the target
is not, proving item 5. \(\square\)

### Corollary 2.2 (FINITE TERMINATION IS PRESERVED)

Recomputing a separating dual only after each batch preserves the finite
termination argument.  Every nonempty boundary batch strictly increases
\(\dim S\); an empty complete boundary batch passes to the unchanged complete
correction oracle.  Since \(V\) and both column rosters are finite, batching
cannot create an infinite branch absent from the one-column algorithm.

This is a correctness statement, not a useful runtime bound: later columns in
one batch may be mutually dependent modulo \(S\).  The speedup is proportional
to the measured number of independent insertions per dual, which production
must report rather than assume.

## 3. Certificate and checkpoint obligations

Batching must not replace exact reconstruction by accumulator trust.  For each
selected index it must:

1. reconstruct `translated_boundary` in the parent;
2. recompute \(\lambda(c_\omega)\in\{1,2\}\);
3. replay the full contributing-pair sum from the same immutable support;
4. attach the existing block, relator, translation, scalar, contributor, and
   boundary-epoch provenance; and
5. pass the exact row and its provenance separately to the formal reducer.

The worker accumulator only selects indices.  It remains outside the trusted
certificate boundary.

A resource stop after a proper prefix of the batch is mathematically safe.
Every accepted row already has complete provenance and enlarges \(S\).  A
resume may discard the unprocessed suffix, derive the separating dual of the
new stored span, and run a fresh complete convolution.  No column is declared
absent by that discard.  For reproducibility the receipt should nevertheless
record

~~~text
batch_cap
active_index_count
selected_batch_sha256
materialized_count
retained_count
dependent_count
dual_rebuild_count
~~~

and the terminal checkpoint must bind every retained row through the existing
formal DAG.  No enormous pending batch or worker-private support needs to be
serialized.

## 4. Minimal production design

The first production successor should use a conservative fixed cap such as
\(b=64\), while retaining \(b=1\) as a small-fixture canary.  Its required
checks are:

1. the complete active-key set and canonical order are unchanged from the v23
   convolution;
2. `b=1` reproduces the frozen one-column fixture byte for byte apart from
   versioned metadata;
3. batched and one-column modes span the same columns on a finite exhaustive
   fixture and give the same target-membership answer;
4. permuting worker completion order does not change the selected batch;
5. mutation of any reconstructed row, scalar, contributor, or DAG binding is
   rejected; and
6. progress prints batch attempts and actual independent rank gain.

The low-memory resume reader is orthogonal: it restores the exact span at
22,912,880 boundary pairings and 8,727 retained columns, after which the
batched owner changes only how many authenticated active columns are inserted
before rebuilding the next dual.

No negative may be emitted merely because a resource cap is reached.  A
negative requires complete exhaustion of the finite boundary and correction
oracles under an exact separating functional.

## 5. Exact frontier

~~~text
A0 FINITENESS / EXACT ROSTER CARDINALITIES:       PROVED FROM FROZEN OWNERS
ONE-COLUMN BOTTLENECK IN RUN 33267817818:         ARTIFACT OBSERVATION
BATCHED INSERTION SOUNDNESS:                      PAPER PROOF
LOW-MEMORY RESTORE OF 1.66 GB CHECKPOINT:         IMPLEMENTATION IN PROGRESS
BATCHED PRODUCER / CHECKER:                       NOT YET IMPLEMENTED
BATCHED GHA PRODUCTION:                           NOT RUN
A0 COMMON WORD OR COMPLETE NEGATIVE:              UNKNOWN
FAKE / IHARA WITNESS:                             NOT DECLARED
~~~

\(\mathtt{R07\_A0\_BATCHED\_DUAL\_COLUMN\_GENERATION\_V385\_AUDIT\_CANDIDATE}\)
