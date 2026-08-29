# R07 A0 batched history-free discovery v387

Author: Sol / 2026-08-30

Status: corrected paper theorem replacing rejected v385.  The linear algebra
of batched dual column generation is separated from the authority grade of the
stored basis.  For the current v23 lineage, batching accelerates heuristic
positive discovery only; a proposed common word must still pass v278's full
selected-support replay.  An empty active set gives no negative.  No A0
positive, lift, fake certificate, or Ihara witness is asserted.
\(\mathtt{verified=false}\).

## 1. Finite indexed rosters

Let \(k=\mathbf F_3\), let \(V\) be the finite A0 sparse row space, and let
\(t\in V\) be the fixed target.  The translated-boundary **index family** is
finite.  Blocks 1 and 2 have two relators each over the PB3 quotient of order
81.  Block 3 has eleven relators over the PB4 quotient of order

\[
 583{,}152{,}628{,}325{,}845{,}597{,}028{,}352.
\tag{1.1}
\]

Hence

\[
 \boxed{
 |\Omega_B|=4\cdot81+11\cdot
 583{,}152{,}628{,}325{,}845{,}597{,}028{,}352
 =6{,}414{,}678{,}911{,}584{,}301{,}567{,}312{,}196.}
\tag{1.2}
\]

Different indices may in principle yield the same vector; (1.2) counts the
complete indexed translated family, not a deduplicated set of vectors.  The
naive correction row--\(\Delta\) family has

\[
 6{,}441\cdot357{,}128{,}352
 =2{,}300{,}263{,}715{,}232
\tag{1.3}
\]

indices.  V143's weighted-support theorem can shorten the correction query for
a particular dual; in its fair-fallback case the complete group roster is
retained.

## 2. Exact active-set contract

Let \(S\leq V\) be the span currently used by a discovery or exact owner.  If
\(t\notin S\), Gaussian elimination supplies

\[
 \lambda\in V^*,
 \qquad \lambda(S)=0,
 \qquad \lambda(t)\ne0.
\tag{2.1}
\]

For each boundary index \(\omega\in\Omega_B\), let \(c_\omega\in V\) be its
materialized translated column, and put

\[
 A_\lambda=
 \{\omega\in\Omega_B:\lambda(c_\omega)\ne0\}.
\tag{2.2}
\]

The authority for computing (2.2) is v163 Proposition 2.1 together with v254
Theorem 2.1, not v278.  The following conditions are load-bearing:

1. \(\lambda\) is frozen throughout the epoch;
2. all 104 boundary descriptors are used;
3. every descriptor is paired with every matching entry in the full support
   of \(\lambda\);
4. worker intervals give a disjoint complete cover of those pairs; and
5. all worker accumulators are merged globally in \(\mathbf F_3\), including
   cross-worker cancellation, before zero coefficients are deleted and the
   canonical order is applied.

Only after this global merge may the first \(b\) active indices be selected.
Taking the first \(b\) per shard and merging those prefixes is not equivalent
and is forbidden.

## 3. Batched span growth

Fix \(b\geq1\), and let \(C_\lambda\) be the first
\(\min(b,|A_\lambda|)\) indices in the existing global canonical order.
Materialize them in that order.  Starting from \(S_0=S\), insert each column
by exact sequential reduction and put

\[
 S_j=S_{j-1}+k c_{\omega_j}.
\tag{3.1}
\]

Retain a column precisely when its remainder modulo \(S_{j-1}\) is nonzero.

### Theorem 3.1 (BATCHED DUAL SPAN LEMMA)

For either authority mode described in Section 4:

1. if \(A_\lambda\ne\varnothing\), the first selected column is outside the
   old span \(S\), so the batch raises rank at least once;
2. after processing the batch, the stored space is exactly

   \[
    S'=S+\operatorname {span}_k
       \{c_\omega:\omega\in C_\lambda\};
   \tag{3.2}
   \]

3. discarding a later zero remainder changes no span; and
4. recomputing the separating dual after the batch preserves the finite
   rank-growth argument internal to that authority mode.

#### Proof

For each \(\omega\in A_\lambda\), equations (2.1)--(2.2) imply
\(c_\omega\notin S\).  This proves the first assertion.  The same old
functional need not annihilate \(S_j\) after the first insertion, and no such
claim is used.  Exact sequential Gaussian elimination gives (3.2) by
induction, and a zero remainder is precisely membership in the current span.
Every nonempty batch therefore raises rank. \(\square\)

The theorem does not say that all \(b\) columns are mutually independent.
Actual speedup is the measured retained count per dual, not the requested
batch cap.

## 4. Two authority modes

### 4.1 Exact-resume mode

Suppose every old and restored row, source equality, pivot, current dual, and
formal coefficient has been independently replayed under the v276--v277 exact
basis gates.  In this stronger mode, \(S\) is an authenticated exact span.
Then target membership in \(S'\) and expansion of the authenticated formal
ancestry give an exact expression.

Only in this exact mode, and only after an independently replayed empty global
boundary accumulator and a complete exact correction oracle, may a separating
functional contribute to a nonmembership certificate.  Resource exhaustion
alone remains UNKNOWN.

### 4.2 Current history-free v23 mode

The effective v23 lineage explicitly records

~~~text
heuristic_discovery_only = true
exact_cached_resume = false
~~~

Its sealed checkpoint restores a **heuristic discovery state** \(S_h\), not an
independently authenticated exact A0 span.  Theorem 3.1 applies to the internal
span algebra and therefore permits batched positive search, but it does not
upgrade the checkpoint DAG to a proof transcript.

If the discovery owner reaches target membership, the result is only a
candidate.  Final acceptance must invoke every v278 Section 3
selected-support gate, including:

1. the actual fixed target;
2. every selected old and new row;
3. the complete sparse equality with exact coefficients;
4. reconstruction of the boundary preimage;
5. the literal correction word and its exponent-zero property; and
6. the direct eleven-occurrence/all-seven replay and joint-kernel side gates.

Only that independent replay promotes a finite common word.  Discovery order,
batch size, unused checkpoint rows, and the heuristic DAG are irrelevant once
the selected support has been replayed.

An empty \(A_\lambda\) in history-free mode merely advances the heuristic
schedule to its correction oracle.  It has no nonexistence, exhaustion, or
negative-certificate content.  The worker accumulator remains a scheduling
device for positive discovery; any future negative requires the stronger
exact-mode and independent completeness replay just stated.

## 5. Parent reconstruction and interruption

Batch selection must not trust worker rows.  For each selected global index,
the parent must:

1. reconstruct the exact translated boundary;
2. recompute \(\lambda(c_\omega)\in\{1,2\}\);
3. replay the full contributor sum from the immutable support;
4. attach block, relator, translation, scalar, contributor, and epoch
   provenance; and
5. pass the row separately through current-span reduction.

In history-free mode these checks make a selected row suitable for positive
discovery, while v278 remains the final certificate boundary.

A resource stop after a proper materialized prefix is safe provided each row
commit is atomic.  The checkpoint retains the committed prefix, discards the
unprocessed suffix, rebuilds a fresh dual, and runs a new complete global
convolution.  A stop during convolution must discard the whole incomplete
epoch.  Neither kind of discarded work has absence content.

Receipts should record at least

~~~text
batch_cap
global_active_index_count
selected_batch_sha256
materialized_count
retained_count
dependent_count
dual_rebuild_count
~~~

The current run 33267817818 had 8,727 nonempty epochs and exactly 8,727 winner
reconstructions.  Its two worker accumulators returned 11,473,766 entries in
total, about 1,315 entries per committed epoch before global cancellation.
This demonstrates room for a batch experiment, but not the number of
independent rows it will retain.

## 6. Minimal successor design

Use the low-memory resume baseline to restore the sealed history-free state at
22,912,880 boundary correlations and 8,727 retained discovery columns.  Add a
separate versioned history-free batch successor with conservative cap
\(b=64\).  Required gates are:

1. the exact global active-set contract of Section 2;
2. `b=1` reproduces the one-column fixture apart from version metadata;
3. batched and one-column modes produce the same span on a finite exhaustive
   fixture;
4. worker completion-order permutations give the same global batch;
5. row/scalar/contributor/provenance mutations are rejected; and
6. final positive candidates always pass the unchanged v278 replay checker.

The batch successor must continue to print
`heuristic_discovery_only=true` and `exact_cached_resume=false`.  It must never
emit a negative from an empty active set or a resource cap.

## 7. Exact frontier

~~~text
A0 FINITENESS / INDEXED ROSTER CARDINALITIES:       PAPER ARITHMETIC
GLOBAL ACTIVE-SET CONTRACT:                         v163 + v254 CONDITIONS
BATCHED SPAN LINEAR ALGEBRA:                        PAPER PROOF
CURRENT 1.66 GB CHECKPOINT AUTHORITY:               SEALED HEURISTIC STATE
LOW-MEMORY RESTORE:                                 IMPLEMENTATION REPAIR
HISTORY-FREE BATCH PRODUCER / CHECKER:              NOT IMPLEMENTED
BATCH GHA PRODUCTION:                               NOT RUN
A0 COMMON WORD OR EXACT COMPLETE NEGATIVE:          UNKNOWN
FAKE / IHARA WITNESS:                               NOT DECLARED
~~~

\(\mathtt{R07\_A0\_BATCHED\_HISTORY\_FREE\_DISCOVERY\_V387\_AUDIT\_CANDIDATE}\)
