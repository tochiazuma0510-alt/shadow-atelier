# R07 A0 dual-anchored ACTIVE batch (v415)

Author: Sol / 2026-09-01

Status: paper acceleration theorem for the finite A0 rank ladder.  It proves
that all directly replayed columns detected by one separating dual may be
inserted before that dual is recomputed.  It also records the exact eight
S0 target values from Task448.  No new A0 terminal, common word, compatible
lift, fake, or Ihara witness is asserted.  `verified=false`.

## 1. Actual rank-43--51 target pattern

Task448 run `33504248130` accepted eight correction records.  Every record has

```text
seed_index=1, coordinate=0, fibre_cursor=0,
required_coordinates=[0,1,2].
```

The S0 target blob has width 40: the first 36 bytes are the coarse
permutation and the last four are the PB3 PC coordinates.  In chronological
order the eight target blobs have identity permutation and PC tails

\[
\begin{split}
 &(0,0,1,0),(0,0,2,0),(1,0,0,0),(1,0,2,0),\\
 &(2,0,1,0),(1,0,1,0),(2,0,0,0),(2,0,2,0).
\end{split}
\tag{1.1}
\]

As a set, (1.1) is exactly

\[
 \{(a,0,c,0):(a,c)\in\mathbf F_3^2\setminus\{(0,0)\}\}.
\tag{1.2}
\]

Thus the first eight selected targets sweep the eight nonidentity points of
one actual two-dimensional PC plane.  This is evidence of a small structured
slice, not a claim that rank 51 already spans every state in each target
fibre or every other seed/context.

## 2. Linear batching lemma

Let \(V\) be the finite physical quotient space, \(S\leq V\) the span of the
currently accepted legal columns, and \(t\notin S\) the target.  Let
\(\lambda\in V^*\) be the canonical dual returned by echelon reduction, so

\[
 \lambda(S)=0,\qquad \lambda(t)\ne0.
\tag{2.1}
\]

For the complete action-plus-compact column universe \(\mathcal C\), put

\[
 \mathcal A_\lambda=\{c\in\mathcal C:\lambda(c)\ne0\}.
\tag{2.2}
\]

The v410--v414 selector enumerates (2.2) finitely in the tau-free branches;
the actor-adapted selector does the same in the nonzero-tau branch.

### Lemma 2.1 (DUAL-ANCHORED BATCH INSERTION)

Fix one \(\lambda\) satisfying (2.1).  Traverse any finite authenticated
sublist of \(\mathcal A_\lambda\), directly replay every listed column, and
insert every row that raises the current echelon rank.  It is sound to
recompute the target remainder and its canonical dual only after the whole
sublist has been processed.

If the sublist is nonempty, at least its first element raises rank.  Every
accepted element remains a legal A0 column even though it need not pair
nontrivially with a *later* canonical dual.

#### Proof

For \(c\in\mathcal A_\lambda\), (2.1) gives \(c\notin S\), since every element
of \(S\) is annihilated by \(\lambda\).  Hence the first listed column raises
rank.  After an insertion, ordinary echelon reduction decides whether each
later directly replayed column lies outside the enlarged span.  Accepting
exactly the rank-raising rows constructs a larger subspace generated only by
legal columns.  Neither legality nor linear independence requires the
canonical target dual to be recomputed between insertions. \(\square\)

The discovery scalar remains tied to the frozen batch anchor \(\lambda\).
It must not be mislabeled as the post-insertion canonical dual scalar.

## 3. Complete ACTIVE batches

For one frozen dual, run the complete action oracle and the complete formula
selector.  Instead of returning the first ACTIVE row, enumerate every
candidate with nonzero direct anchor pairing, in the already authenticated
seed/coordinate/target/kernel order.  Directly replay it and feed it to the
echelon.  Stop the batch at a declared finite cap if desired, then recompute
the target remainder once.

### Theorem 3.1 (BATCHED FINITE LADDER)

Replacing single ACTIVE insertion by Lemma 2.1 preserves all three possible
mathematical outcomes:

1. if the recomputed remainder is zero, the ordinary expression replay gives
   the same kind of positive A0 certificate;
2. if it is nonzero, its new canonical dual starts the next finite batch; and
3. if a complete action/formula enumeration is empty, that dual is the same
   exact separator as in v413--v414.

Every nonterminal complete batch raises rank, so finite-dimensional
termination is unchanged.  The number of expensive canonical-dual
computations is the number of batches, not the number of accepted rows.

#### Proof

Lemma 2.1 shows that the enlarged span contains only legal columns and that a
nonempty batch raises its dimension.  Target membership is a property of the
span and is therefore decided by the ordinary post-batch reduction.  If the
complete ACTIVE set is empty, the selector theorem says the anchor dual
annihilates the entire legal column universe while (2.1) says it does not
annihilate the target.  This is the separator case.  Strict finite dimension
growth proves termination. \(\square\)

## 4. Certificate boundary

A batch record must contain:

```text
batch anchor dual/remainder digest and rank
authenticated selector cursor and direct anchor scalar
literal correction/action ancestry
direct physical row digest
pre/post insertion rank and pivot
post-batch remainder/dual digest, written once after batch close
```

An independent checker reconstructs the frozen batch anchor, replays every
literal row, checks its anchor scalar, replays every echelon rise, and then
recomputes the post-batch remainder/dual.  It must not require each row to
pair with the canonical dual after previous rows in the same batch.  A
resource stop before a batch closes is `UNKNOWN_RESOURCE`; it is neither a
separator nor a positive result.  A versioned continuation may conservatively
close a partial nonempty batch and recompute before returning, without losing
soundness.

```text
TASK448 ACTUAL TARGET SLICE:          F3^2 MINUS ZERO / EIGHT S0 VALUES
SINGLE-ROW DUAL RECOMPUTATIONS:       NOT MATHEMATICALLY REQUIRED
BATCH DISCOVERY FUNCTIONAL:           FROZEN PRE-BATCH DUAL
ROW TRUST BOUNDARY:                   FRESH LITERAL PHYSICAL REPLAY
POST-BATCH DECISION:                  ONE TARGET REDUCTION / DUAL
ACTUAL A0 TERMINAL:                   STILL PENDING
```

`R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V415_PAPER_GRADE`
