# R07 boundary-first lazy-runtime resume theorem v277

Author: Sol / 2026-08-29

Status: paper-grade phase-separation theorem for the history-free positive A0
resume.  It proves that the complete Q0 section census may be postponed until
the first correction-oracle call.  It does not repair an implementation,
accept the current checkpoint, or declare a COMMON word.  `verified=false`.

## 1. The two runtime layers

Write the authenticated runtime data as two layers.

The **light layer** \(L\) contains exactly the data used by the target,
retained-column, echelon, and full-boundary owners:

1. the task175 raw target and PB3/PB4 boundary rows;
2. the marked quotients \(E_3,E_4\), their exact multiplication, inversion,
   evaluation, and packed-element codecs;
3. the old Fox evaluator, the ten marked contexts, the complete 6,441-row
   relation roster, and the joint-kernel evaluator;
4. the immutable source pins and the authenticated checkpoint bytes; and
5. the retained columns with their literal boundary or correction
   provenance.

The **heavy layer** \(H\) is the Q0 candidate-section machinery:

\[
 (qstates,qids,parents,letters,stores,memberships,emitted),
\tag{1.1}
\]

together with the singleton-fibre coarse inverse tables.  In the present
implementation this starts with all \(1,469,664\) Q0 section states, all ten
coordinate stores, and the ensuing membership scans.

The distinction is literal in the accepted v1 owner.  `exact_target`,
`translated_boundary`, `boundary_oracle`, `AllSevenModel.direct_column`, and
the sparse echelon use \(L\).  `FibreOracle.canonical`,
`FibreOracle.global_candidate`, and construction of the adjusted L generators
use \(H\).

## 2. What a retained column needs

Every retained boundary column has typed provenance

\[
 (b,r,t),\qquad
 c=t\cdot d_{b,r},
\tag{2.1}
\]

and is reconstructed from the marked quotient operations and the pinned
base boundary row.  This uses only \(L\).

Every retained correction column carries its literal `delta_word` and
`relator_word`.  Its sparse row is reconstructed by the eleven-occurrence
Fox calculation and independently by the direct H1/H2/P calculation.  Its
joint-kernel word is evaluated directly.  These checks also use only \(L\):
the old Q0 state or selector that originally discovered the word is not a
premise of the resulting word identity.

Thus an old Q0 state id is discovery provenance, not mathematical authority
for a retained raw column.  A history-free positive verifier may discard it
after authenticating the checkpoint bytes, provided it directly reconstructs
every retained row from (2.1) or from the literal correction words.

## 3. Boundary-first resume algorithm

Assume the v276 triangular checkpoint gates have passed and give an exact
normalized basis \(P\) spanning the retained raw columns.  The following
algorithm is sound.

1. Authenticate the immutable sources and checkpoint, build \(L\), directly
   reconstruct the target and all retained raw columns, and check the v276
   triangular basis certificate.
2. Reduce the target against \(P\).  If the remainder is zero, emit only a
   candidate positive receipt and subject its complete word/boundary replay
   to the independent positive checker.  Do not build \(H\).
3. Otherwise construct a fresh exact dual \(\lambda\) annihilating \(P\) and
   pairing nontrivially with the target.
4. Run the complete support-inversion correlation of \(\lambda\) against all
   PB3/PB4 translated boundary families using \(L\).  If an ACTIVE translate
   is returned, directly build its complete sparse row, check the nonzero
   pairing, add it to the live basis, and return to step 2.
5. Only when the complete correlation is zero for the current \(\lambda\)
   instantiate \(H\) and call the correction oracle.  A correction hit is
   directly replayed, added, and returns the algorithm to step 2.

Every cap or failed heavy construction is `UNKNOWN_RESOURCE` or
`UNKNOWN_INPUT`.  In particular, a zero boundary correlation is not a
negative terminal; it only transfers control to the positive correction
dovetail.

## 4. Phase-separation theorem

### Theorem 4.1 (Q0-LATE)

For a history-free positive search, moving construction of \(H\) from process
startup to the first execution of step 5 preserves every possible accepted
COMMON certificate.

#### Proof

Before step 5, the mutable mathematical state consists of the retained raw
column span, its normalized sparse basis, the target, the fresh remainder and
dual, and any newly accepted translated boundary columns.  By Sections 1--2,
each of these is a function of \(L\) and the authenticated literal
provenance; none reads \(H\).

The full-boundary answer is likewise independent of \(H\).  For each dual
support term \((b,i,g)\) and each base occurrence \((b,i,h)\), it computes
the unique left translation \(t=gh^{-1}\), accumulates the exact F3
coefficient at \((b,r,t)\), and directly constructs the selected translated
row.  Therefore building \(H\) earlier cannot change a target reduction, a
dual, an ACTIVE key, or an inserted boundary row.

If the target enters the span before step 5, the positive certificate uses
only the retained literal correction words and typed boundary preimage, so
its complete direct replay also does not use the discovery section.  If step
5 is reached, constructing \(H\) at that point produces exactly the data the
correction oracle would have read after eager startup, under the same
immutable sources.  Subsequent positive candidates are still accepted only
by direct word/Fox replay.  Hence delayed construction removes no accepted
COMMON certificate and adds no unsound one. \(\square\)

The theorem asserts positive-certificate equivalence, not byte-for-byte
cached-v3 scheduler parity.  Old Q0 progress, cached fibre ids, and dual-bound
correction cursors must be discarded unless independently rebuilt for the
fresh basis.

## 5. Authentication split

The adapter must publish two non-confusable digests.

- `light_input_sha256` binds every source and derived object used before
  step 5, including target, quotient codecs, boundary rows, roster, joint
  evaluator, raw retained rows, and triangular ancestries.
- `heavy_input_sha256`, absent before step 5, binds the rebuilt Q0 section,
  parents/letters, ten stores, memberships, adjusted L generators, and any
  coarse inverse table actually used.

The checkpoint's old monolithic `input_sha256` is checked for internal sealed
consistency, but it is not evidence that a live heavy runtime has been
rebuilt.  Conversely, absence of the heavy digest is legal only while no
heavy owner has been called.  A terminal schema must record the phase and
reject any correction-oracle event preceding the heavy digest.

For final positive authority, either the pinned existing direct checker is
invoked once on the physical inner receipt, or a new helper-nonshared checker
reconstructs the same target, selected literal correction words, typed
boundary preimage, and all-seven identity from \(L\).  A copied Boolean or a
Q0 state id is never a substitute.

## 6. Resource consequence

On every boundary-only resume, Q0-LATE removes from the pre-boundary critical
path:

1. enumeration of 1,469,664 Q0 sections and their parent/letter arrays;
2. construction and hashing of all ten fixed-width coordinate stores;
3. the complete membership scan and adjusted-L word construction; and
4. all singleton-fibre coarse inverse tables.

This is an exact absence claim about the boundary phase, not a wall-time
claim.  The light task175/quotient/roster reconstruction and the exact
checkpoint/basis work remain.  If boundary correlation is exhausted, the
heavy work is paid once and metered honestly before correction search.

No boundary-only run may serialize placeholder Q0 hashes, silently borrow a
stale in-memory heavy runtime, or claim full v1 input parity.  Process RSS,
serialized bytes, and construction counts must distinguish the two phases.

## 7. Required negative controls

A future producer/checker pair must reject at least:

1. a boundary function that reads a heavy-only object;
2. a retained correction row accepted from its old Q0 id without direct
   word/Fox replay;
3. a correction-oracle call before `heavy_input_sha256` exists;
4. a fabricated heavy digest without complete Q0 reconstruction;
5. stale correction progress retained across the fresh v276 basis;
6. a zero boundary correlation promoted to NONMEMBER;
7. a COMMON compact view containing an un-replayed boundary chain; and
8. a phase/counter/RSS transcript that hides heavy construction.

## 8. Fixed frontier

```text
BOUNDARY PHASE DEPENDS ONLY ON LIGHT RUNTIME:       PAPER PROOF
Q0/MEMBERSHIP/COARSE TABLES MAY BE BUILT LATE:     PAPER PROOF
CURRENT CHECKPOINT TRIANGULAR EXTRACTION:           STATIC CANDIDATE ONLY
A0 V6 REPAIR OR V7 IMPLEMENTATION:                  NOT YET COMMISSIONED
ACTUAL A0 COMMON + CHECKER:                          0/1
LIFT / FAKE / IHARA:                                NONE
```

`R07_BOUNDARY_FIRST_LAZY_RUNTIME_RESUME_V277_PAPER_GRADE`
