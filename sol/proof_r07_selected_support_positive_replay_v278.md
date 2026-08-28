# R07 selected-support positive replay theorem v278

Author: Sol / 2026-08-29

Status: paper-grade soundness theorem for a speculative, history-free positive
search.  It weakens v277's startup replay requirement without weakening the
final COMMON gate.  It does not establish cached-v3 path parity, accept a
checkpoint, implement v7, or construct a witness.  `verified=false`.

## 1. Exact resume and positive search are different claims

Let the checkpoint contain canonical sparse discovery columns

\[
 C=(c_1,\ldots,c_r)
\tag{1.1}
\]

and literal provenance records \(\pi_i\).  Let the actual direct evaluator
applied to \(\pi_i\), when defined and accepted, be \(\widehat c_i\).

An **exact resume** claims \(c_i=\widehat c_i\) for every i and that the new
basis is the exact historical span.  That claim requires the full v276/v277
replay gates.

A **history-free positive search** makes no such claim.  It may use the
checkpoint rows as deterministic heuristic vectors, provided every accepted
COMMON is rebuilt from actual provenance and directly checked.  Failure or a
cap has no negative content.

## 2. Formal ancestry owner

Construct proposed pivot rows

\[
 p_j=\sum_i a_{ji}c_i
\tag{2.1}
\]

by the sparse triangular calculation of v276, and attach to each live basis
row its formal coefficient map in the symbols

\[
 e_1,\ldots,e_r,f_1,f_2,\ldots,
\tag{2.2}
\]

where \(e_i\) denotes checkpoint provenance \(\pi_i\), while \(f_k\) denotes
a newly generated boundary or correction row.  Every new \(f_k\) is directly
replayed before insertion.  All reduction and row-addition operations update
both the sparse heuristic row and its formal coefficient map over F3.

If the target reduces to zero, the formal map yields finite coefficient sets

\[
 T=\sum_i u_i e_i+\sum_k v_k f_k
\tag{2.3}
\]

in the heuristic module.  Equation (2.3) is only a candidate transcript; it
is not yet an equality of actual Fox rows.

## 3. Final selected-support gate

Let

\[
 S_C=\{i:u_i\ne0\},\qquad S_F=\{k:v_k\ne0\}.
\tag{3.1}
\]

The independent positive checker must:

1. reconstruct the actual target \(\widehat T\) from the frozen H1/H2/P
   source;
2. for every \(i\in S_C\), reconstruct \(\widehat c_i\) from \(\pi_i\) by
   the typed translated-boundary replay or literal eleven-occurrence/direct
   Fox replay, and require \(\widehat c_i=c_i\);
3. independently replay every selected new row \(f_k\), including its ACTIVE
   scalar/translation or literal correction word;
4. check the complete sparse identity

\[
 \widehat T=\sum_{i\in S_C}u_i\widehat c_i+
             \sum_{k\in S_F}v_k\widehat f_k;
\tag{3.2}
\]

5. combine the selected correction words with coefficient 2 interpreted as
   inverse, reconstruct the typed PB3/PB4 boundary preimage, and run every
   final all-seven, exponent, joint-kernel, and side-gate check required by
   the positive COMMON contract.

No unselected checkpoint column is a premise of (3.2).  The checker records
the exact selected ids, coefficients, provenance bytes, and replay digests.

## 4. Soundness theorem

### Theorem 4.1 (SELECTED-SUPPORT POSITIVE SOUNDNESS)

Acceptance of all gates in Section 3 proves the same finite explicit COMMON
word identity as a search that replayed every checkpoint column before its
first dual computation.

#### Proof

The search transcript is used only to propose the finite coefficients in
(3.2).  The checker reconstructs the target and each nonzero summand of that
equation from the immutable mathematical sources and literal provenance.
Therefore (3.2) is an equality of actual sparse Fox rows, independently of
the values, provenance, pivots, or even validity of every unselected
checkpoint row.

The selected correction factors and boundary chains are then replayed in the
group/word owners, so the sparse equality is promoted by the existing
positive theorem to the advertised finite common word.  A false heuristic
row can at worst cause a false candidate; it cannot pass (3.2).  Since no
failure is interpreted negatively, use of speculative discovery state also
cannot prove nonexistence. \(\square\)

This theorem does not say the speculative search has the same trajectory or
completeness as cached-v3.  It proves only the one property needed for the
current goal: every accepted explicit positive certificate is genuine.

## 5. Startup consequence

In speculative-positive mode, the producer may before the first boundary
epoch:

1. authenticate checkpoint bytes, schema, seal, source pins, canonical sparse
   encodings, ids, and ancestry shapes;
2. compute the proposed v276 pivot rows and check their sparse pivot form;
3. omit direct source reconstruction of all r checkpoint provenances; and
4. mark the basis and every derived dual as `heuristic_discovery_only`.

It must not label this state exact resume, cached-v3 parity, or a proof of the
true retained-column span.  On COMMON it pays the complete selected-support
replay cost.  An implementation may optionally expand the replay support to
all r columns; that is stronger but not required by Theorem 4.1.

The formal coefficient map is load-bearing.  It may be sparse and composed
through a persistent ancestry DAG, but it may not be replaced by a digest,
pivot id, copied solution Boolean, or a flattened list with unmetered growth.

## 6. Interaction with v276 and v277

- V276 remains the exact-resume theorem when every raw source row is also
  authenticated.  Here its triangular arithmetic is used only to build a
  deterministic independent heuristic basis and coefficient map.
- V277 remains the Q0-LATE theorem.  In speculative-positive mode its
  requirement to directly reconstruct *all* retained columns at startup is
  replaced by Section 3's selected-support replay at the final positive gate.
  Target reconstruction and all newly inserted rows remain direct.
- The two optimizations are independent: Q0 is delayed until correction
  search, while old provenance replay is delayed until an actual COMMON
  candidate exists.

## 7. Required negative controls

A future implementation must reject:

1. loss or alteration of a formal ancestry coefficient;
2. a candidate whose selected direct row differs from its checkpoint row;
3. omission of one selected checkpoint or new row;
4. coefficient 2 treated as repetition rather than inverse in the word;
5. a sparse target equality accepted from a digest or copied Boolean;
6. use of an unselected invalid row to assert exact-resume parity;
7. any negative/separator claim from a speculative basis; and
8. a COMMON whose final selected set changes after replay or sealing.

## 8. Fixed frontier

```text
SPECULATIVE CHECKPOINT BASIS FOR POSITIVE SEARCH:  SOUND
FINAL SELECTED RAW/WORD/BOUNDARY REPLAY:            MANDATORY
EXACT CACHED-V3 RESUME/PATH PARITY:                 NOT CLAIMED
V7 IMPLEMENTATION / EXECUTION:                     NOT YET COMMISSIONED
ACTUAL A0 COMMON + CHECKER:                         0/1
LIFT / FAKE / IHARA:                               NONE
```

`R07_SELECTED_SUPPORT_POSITIVE_REPLAY_V278_PAPER_GRADE`
