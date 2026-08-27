# R07 actual weighted-support hitting selector v143

Date: 2026-08-27
Role: Sol mathematical proof / finite actual-class positive oracle

## 1. Frozen actual data

Let (Delta) be the linked task176 extension used by task179.  The
cross-checked production run `33044121344` gives

\[
 |Delta|=357,128,352,
 qquad |Q_0|=1,469,664,
 qquad |\Gamma|=243.
\]

For the ten coordinate maps
(pi_i:\Delta\to S_i), task176 gives the exact kernel orders

\[
 (k_0,\ldots,k_9)=(9,9,9,9,9,1,1,1,3,3).
\tag{1.1}
\]

It also gives word-bearing generators for every kernel.  Together with the
actual singleton selector of v142, a nonempty fibre
(pi_i^{-1}(t)) can therefore be enumerated completely in at most nine
literal words.  Every word is replayed in all ten coordinates.

The extension roster

\[
 (q,\gamma)\longmapsto u_\Gamma(\gamma)u_{Q_0}(q)
\tag{1.2}
\]

contains (243\cdot1,469,664=357,128,352) distinct elements.  This follows
from the exact extension and section statements in the same task176 receipt.

These are finite cross-checked premises, not Lean-verified assertions.

## 2. Weighted indicator functions

After merging equal targets and deleting zero coefficients, the task179
correlation formula for one relation row has the form

\[
 F(\delta)=K+
 \sum_{(i,t)\in R}c_{i,t}\,1_{\pi_i(\delta)=t},
 \qquad c_{i,t}\in\mathbf F_3^\times.
\tag{2.1}
\]

Put

\[
 U=\bigcup_{(i,t)\in R}\pi_i^{-1}(t),
 \qquad
 W=\sum_{(i,t)\in R} k_i.
\tag{2.2}
\]

Empty target fibres may be omitted from (U); keeping their (k_i) in (W)
only weakens the bound.  The union bound gives

\[
 |U|\leq W.
\tag{2.3}
\]

## 3. The bounded selector

### Theorem 3.1 (actual weighted-support hitting)

For the function (2.1):

1. if (K=0), every nonzero value of (F) lies in (U), so complete
   enumeration of the word-bearing fibres in (2.2) finds a nonzero value
   whenever one exists;
2. if (K\ne0) and (W<|\Delta|), evaluation on any (W+1) distinct
   elements of (Delta) finds a nonzero value; and
3. every returned hit can be checked without trusting the selector by the
   complete merged formula and the direct eleven-occurrence Fox column.

#### Proof

Outside (U), all indicators in (2.1) vanish.  Hence

\[
 F(\delta)=K\qquad(\delta\notin U).
\tag{3.1}
\]

If (K=0), (3.1) proves part 1.  For part 2, (2.3) says that a set of
(W+1) distinct elements cannot be contained in (U); at an element outside
(U), (3.1) equals the nonzero constant (K).  Part 3 is the task175/v140
direct replay and does not use the counting argument.  ∎

The theorem does not say that the first tested point is active.  It supplies
a finite upper bound and therefore replaces an unstructured scan of all
(|\Delta|) elements whenever (W<|\Delta|).

## 4. Complete row schedule

For one merged formula use the following deterministic order.

1. If (K=0), enumerate each distinct nonempty fibre in
   `(coordinate,target)` order, using the v142 least representative followed
   by the complete kernel roster of size (k_i).  Stop at the first direct
   nonzero replay.  If all such fibres are exhausted, this particular (F)
   is identically zero.
2. If (K\ne0) and (W<|\Delta|), evaluate the first (W+1) distinct
   elements of the authenticated global `(q,gamma)` roster.  Theorem 3.1
   guarantees a hit.  The support fibres may still be tried first as a speed
   heuristic, but are not needed for termination.
3. If (K\ne0) and (W\geq|\Delta|), retain the old fair global fallback or
   compute a sharper exact union certificate.  A bounded stop remains
   `UNKNOWN_RESOURCE`, never a zero or separator claim.

Repeated targets for the same coordinate are already merged, and fibres for
different targets of one coordinate are disjoint.  No independence between
different coordinates is assumed.

### Corollary 4.1 (finite correction oracle)

Assume task176's kernel generators and orders are replayed and suppose the
dual functional is nonzero on at least one task179 correction column.  If
every row with (K\ne0) satisfies (W<|\Delta|), scanning the 6,441 relation
rows with the schedule above returns a literal ACTIVE correction after a
finite number of probes.  The maximum probes for a (K=0) row are bounded by

\[
 \sum_{(i,t)\in R}k_i=W,
\]

and for a (K\ne0) row by (W+1).

This is a positive-oracle completeness statement for the frozen finite
family, not a separator for the cofinal problem.

## 5. Checkpoint and claim boundary

A checkpoint records for each processed formula:

- the merged support digest, (K), (W), and (|\Delta|);
- the exact kernel order used for every support fibre;
- completed fibre indices or the completed global prefix;
- every literal candidate word and direct scalar only when retained as an
  ACTIVE column; and
- resource counters and a claim-free terminal on any cap.

The checker of a positive hit only needs the literal word, all ten coordinate
values, the merged formula, and the direct full-eleven Fox column.  It need
not trust the union bound to accept the witness.

This theorem upgrades the actual finite correction selector.  It does not
establish the common-word membership itself, the v141 augmented saturation
membership, all cofinal edges, fake, or the Ihara witness.

`R07_ACTUAL_WEIGHTED_SUPPORT_HITTING_SELECTOR_V143_PAPER_GRADE`
