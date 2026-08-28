# R07 bridge-trace factorization and fused DAG replay v286

Author: Sol / 2026-08-29

Status: paper-grade adapter theorem for the in-progress A4-v5 certificate.
It proves that task198's per-relator 10-to-11-to-7 bridge trace can be
recomputed from an independently certified literal word and its already
computed exact ten-coordinate state.  A second flat evaluation of all 6,441
words is unnecessary.  It does not accept A4-v5, compute its boundary or K
basis, or construct a compatible lift, fake certificate, or Ihara witness.
`verified=false`.

## 1. Typed bridge maps

Let

\[
 X_{10}=X_0\times\cdots\times X_9
\]

be the ten typed roof-coordinate sets.  The types may have different encoded
widths; no equality between distinct coordinates is assumed.  Define the
insertion map by

\[
 I(a_0,\ldots,a_9)
 =(a_0,a_1,a_2,a_3,a_0,a_4,a_5,a_6,a_7,a_8,a_9),
\tag{1.1}
\]

and deletion by removing position four (zero based),

\[
 D(b_0,\ldots,b_{10})
 =(b_0,b_1,b_2,b_3,b_5,b_6,b_7,b_8,b_9,b_{10}).
\tag{1.2}
\]

Let \(R\) regroup an eleven-tuple into blocks of sizes
\((3,3,1,1,1,1,1)\), and let \(F\) flatten those seven blocks.

### Lemma 1.1 (BRIDGE BIJECTION ON THE DIAGONAL IMAGE)

For every \(a\in X_{10}\),

\[
 DI(a)=a,\qquad IDI(a)=I(a),\qquad FRI(a)=I(a).
\tag{1.3}
\]

Moreover positions zero and four of \(I(a)\) are equal.

#### Proof

All assertions follow by substituting the index lists in (1.1)--(1.2).
The regrouping map changes only parentheses, so flattening restores the same
ordered eleven entries.  No group law or word evaluation is used. \(\square\)

Thus task198's left-inverse, image-inverse, regroup-inverse, and diagonal
checks are properties of the already evaluated ten-tuple.  They are not a
second mathematical evaluation of the source word.

## 2. Factorization of the task198 trace

Let \(S(w)\in X_{10}\) be the exact ten-coordinate value of a strict signed
source word \(w\).  Let `blob` denote the pinned typed canonical encoding in
each coordinate, and let \(L\) be the authenticated eleven-entry occurrence
ledger.  Define

\[
 \mathcal T(\ell,w,a)
\tag{2.1}
\]

to be the task198 public trace formed from:

1. the label \(\ell\), literal word \(w\), and its canonical digest;
2. the canonical blob lists of \(a\), \(I(a)\), \(D(I(a))\), \(R(I(a))\),
   and \(I(D(I(a)))\);
3. the eleven occurrence values selected from \(I(a)\) by the ordinals in
   \(L\); and
4. the four Boolean equalities in Lemma 1.1.

This is exactly the data used by task198's `replay_bridge_word` after its one
call to the ten-coordinate evaluator.

### Theorem 2.1 (BRIDGE-TRACE FACTORIZATION)

For every strict word \(w\) and label \(\ell\), task198's bridge trace equals

\[
 \boxed{\operatorname{BridgeTrace}(\ell,w)
       =\mathcal T(\ell,w,S(w)).}
\tag{2.2}
\]

Consequently, if an independent evaluator has already proved

\[
 \widehat w=w,\qquad \widehat S=S(w),
\tag{2.3}
\]

then constructing \(\mathcal T(\ell,\widehat w,\widehat S)\) reproduces the
same canonical trace and the same per-row SHA-256 value without evaluating
\(w\) again.

#### Proof

Inspect the task198 definition.  Its only word-dependent operation before
trace construction is the computation of the ten-tuple \(S(w)\).  Every
later field is a deterministic projection, duplication, regrouping, typed
encoding, ledger lookup, or canonical digest of \((\ell,w,S(w))\).  Replacing
these three inputs by equal values therefore preserves every trace field and
its canonical encoding. \(\square\)

The literal-word equality in (2.3) is load-bearing because the trace contains
both the word and its digest.  Equality of the ten states alone is not enough.

## 3. Fusion with the two DAG evaluators

V282 proves two independent ways to obtain (2.3): the producer's forward
prefix DAG and the checker's reversed suffix DAG.  In each row-assembly pass,
the implementation first reconstructs the authenticated ancestry grammar,
compares its literal word once with the stored word, and obtains the exact
ten semidirect states from already evaluated pieces.

Apply Theorem 2.1 immediately at that point.  Append the canonical digest of
the resulting trace to a chronological list

\[
 h_1,h_2,\ldots,h_{6441}.
\tag{3.1}
\]

The final task198 owner is then checked by

\[
 6441=\#(h_i),\qquad
 \operatorname{SHA256}_{\rm canon}([h_1,\ldots,h_{6441}])
 =\texttt{bridge.relator\_replay.digest\_sha256}.
\tag{3.2}
\]

The static occurrence ledger must also be reconstructed from its literal
block, slot, context, orientation, role, factor sign, and ten-index fields.
Together with the occurrence-value selection in (2.1), this binds both the
spelling of the eleven owners and their actual value in every row.

Producer and checker must implement (2.1) separately.  Sharing task198's
composite `replay_bridge_word`, sharing a producer trace, or comparing only a
producer digest would not establish independent replay.

## 4. Checkpoint and complexity consequences

The chronological list (3.1) is bounded: it contains exactly 6,441 fixed
64-hex-character digests.  A replayable checkpoint can therefore retain the
completed prefix of this list, its cursor, and a canonical-prefix canary.
Resume verifies the prefix against the completed row frontier and appends
only new rows.  It need not serialize opaque implementation-specific hash
state and need not revisit old source words.

If \(E_f,E_r\) are the forward and reverse DAG edge counts and \(P\) is the
number of authenticated row pieces, bridge fusion adds constant work per row
and per eleven occurrence.  It does not add a term proportional to the total
expanded word length.  In particular the intended costs remain

\[
 O(10E_f+10P+11\cdot6441)
 \quad\text{and}\quad
 O(10E_r+10P+11\cdot6441),
\tag{4.1}
\]

for producer and checker respectively.  A post-pass calling a flat evaluator
on all 6,441 words is both unnecessary by Theorem 2.1 and outside this bound.

## 5. Fixed frontier

```text
TASK198 BRIDGE TRACE AS FUNCTION OF (WORD,TEN-STATE): PAPER PROOF
FUSION INTO FORWARD/REVERSE ROW-ASSEMBLY PASS:         PAPER PROOF
SECOND 6,441-WORD FLAT BRIDGE EVALUATION NEEDED:       NO
INDEPENDENT PRODUCER/CHECKER IMPLEMENTATION:            IN PROGRESS
ACTUAL A4 CLOSURE / ORDERED K BASIS:                    NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                         NONE
```

`R07_BRIDGE_TRACE_FACTORIZATION_FUSED_DAG_REPLAY_V286_PAPER_GRADE`
