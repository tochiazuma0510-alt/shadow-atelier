# R07 task176 selected-section reconstruction theorem v287

Author: Sol / 2026-08-29

Status: paper-grade authority and complexity theorem for the next A0
checker.  It identifies a lossless route from the already accepted task176
owners to one selected correction section without rerunning the complete
ten-index construction.  It does not accept A0-v8, execute A0-v9, prove a
positive carrier exists, or construct a compatible lift, fake certificate,
or Ihara witness.  `verified=false`.

## 1. Accepted finite owners

Let

\[
 N=1,469,664,\qquad G=243.
\tag{1.1}
\]

The accepted task176 receipt contains the following literal, independently
sealed owners rather than merely their cardinalities or digests.

1. The canonical \(Q_0\) roster: \(N\) records of 36 bytes, hence exactly
   52,907,904 raw bytes, with its zlib/base64 payload, raw length, compressed
   length, and both SHA-256 values.
2. A \(Q_0\) parent state array of \(4N=5,878,656\) raw bytes and a parent
   letter array of \(N=1,469,664\) raw bytes.
3. The ten marked-generator coordinate blobs needed to replay every parent
   edge.
4. The complete \(\Gamma\) ten-coordinate table: \(G\) records of 970 bytes,
   hence 235,710 raw bytes, together with a \(2G=486\)-byte parent array, a
   \(G=243\)-byte parent-record array, and the literal record-word roster.

For every one of the ten coordinates, task176's accepted singleton-bucket
owner records

\[
 \#\{\hbox{coarse keys}\}=N,
 \qquad \min |B_k|=\max |B_k|=1.
\tag{1.2}
\]

The accepted projection-kernel orders are \(9,9,9,9,9,1,1,1,3,3\).
These numbers are used only after the new checker authenticates the exact
task176 receipt, its independent checker verdict, manifest, recovery owner,
and the compressed and raw payload identities.  A producer-supplied copy of
any field is not authority.

## 2. Bounded decoding lemma

### Lemma 2.1 (LOSSLESS OWNER DECODING)

Suppose a checker performs, in this order, an input-size cap, strict base64
decode, bounded zlib expansion to the declared exact raw length, end-of-stream
and no-trailing-data checks, and raw SHA-256 comparison.  Then each decoded
array in Section 1 is the literal array accepted by task176.

#### Proof

Strict base64 and zlib checks make the decoded byte string unique.  Exact
length excludes truncation and extension, the stream checks exclude a hidden
second member or suffix, and equality with the accepted raw SHA-256 binds the
result to task176's literal owner.  The conclusion concerns identity with an
accepted finite owner; it is not a new cryptographic or Lean verification
claim. \(\square\)

The checker must impose the displayed raw lengths before allocation.  Thus
this decoding cannot inherit a producer's unbounded decompression behavior.

## 3. One selected Q0 section

Fix a selected identifier \(q\in\{1,\ldots,N\}\).  Random access to record
\(q\) of the 36-byte roster gives its accepted underlying state.  Starting at
\(q\), follow the accepted parent-state and parent-letter entries using the
pinned task176 root convention.  Require at every step that the indices and
letter are in range, that the parent relation has the accepted chronological
orientation, and that the walk reaches the root within \(N\) steps.  Reverse
the collected letters to obtain the literal section word \(w_q\).

Let \(s_{q,j}\) be the result of replaying \(w_q\) in coordinate \(j\) with
the independently decoded marked-generator blobs.

### Lemma 3.1 (SELECTED Q0 RECONSTRUCTION)

For every selected \(q\), the procedure above uniquely reconstructs its
literal word and ten section values.  Moreover it supplies the independent
checks

\[
 \operatorname{eval}_{Q_0}(w_q)=Q_0[q],
 \qquad
 \operatorname{eval}_{j}(w_q)=s_{q,j}\quad(0\leq j<10).
\tag{3.1}
\]

#### Proof

The bounded chronological parent walk has one prescribed incoming record at
each nonroot identifier, so it determines exactly one word.  Induction from
the root along that word proves both equalities: the first uses the underlying
marked generator and the second uses the independently decoded generator for
coordinate \(j\).  Comparing the first equality with the literal 36-byte
roster record detects a wrong parent, letter, orientation, or multiplication
rule. \(\square\)

This is selected reconstruction.  It neither calls task176's producer helper
nor materializes ten \(N\)-entry indices.

## 4. One selected Gamma section

For \(g\in\{1,\ldots,G\}\), use the accepted \(\Gamma\) parent and
parent-record arrays and literal record-word roster in the same bounded
fashion.  Replay the resulting word independently and compare all ten
coordinates with record \(g\) of the decoded 970-byte table.

### Lemma 4.1 (SELECTED GAMMA RECONSTRUCTION)

The selected identifier \(g\) determines a unique accepted literal word and
ten-state, and the comparison above rejects a substituted state, word,
parent, record, orientation, or multiplication convention.

#### Proof

The proof is the finite parent-walk induction of Lemma 3.1, now on the
243-entry accepted table. \(\square\)

Since \(G=243\), a checker may alternatively reconstruct the complete
\(\Gamma\) table.  This bounded choice does not change the theorem.

## 5. The nonzero-K schedule

For the nonzero-kernel schedule, let the authenticated global cursor be
\(c\), with

\[
 0\leq c<NG,qquad
 q=\left\lfloor c/G\right\rfloor+1,qquad
 g=(c\bmod G)+1.
\tag{5.1}
\]

### Lemma 5.1 (GLOBAL CURSOR BIJECTION)

Equation (5.1) is a bijection from \(\{0,\ldots,NG-1\}\) to the ordered
Cartesian roster \(\{1,\ldots,N\}\times\{1,\ldots,G\}\).

#### Proof

Euclidean division by \(G\) gives unique quotient in
\(\{0,\ldots,N-1\}\) and remainder in \(\{0,\ldots,G-1\}\). \(\square\)

Consequently the checker can reconstruct the two selected states by Lemmas
3.1 and 4.1, multiply them with the pinned task176 section convention, and
compare the resulting section, word, membership condition, correction
factor, and chronological cursor with the receipt.  Bounds and hashes alone
are not substitutes for this replay.

## 6. The zero-K fibre

The zero-kernel schedule claims the canonical least member of a fibre, so a
single selected pair is not by itself a minimality proof.  Let \(j\) be the
coordinate demanded by the correction formula.  Build only the \(j\)-th
coarse inverse as follows.

Stream the accepted \(Q_0\) parent roster once in chronological order.  Carry
only the \(j\)-coordinate state, derive each child from its earlier parent and
the independently decoded \(j\)-generator, compute its pinned coarse key,
and insert \((\text{key},q)\).  Reject a duplicate key.  Equation (1.2),
independently witnessed again by this pass, makes the inverse single-valued.
Reconstruct the 243 \(\Gamma\) values in coordinate \(j\).  For every
one-coordinate Gamma value \(a\) and requested target \(t\), look up the
unique section candidate with coarse key belonging to \(a^{-1}t\), compare
the complete typed blob rather than only its coarse prefix, and retain it
exactly when \(a\,s_j(q)=t\).  Order the retained base pairs \((q,g)\) by the
pinned task176 order.  The accepted task176 `A_families`, `families`, and
`word_generators` owners supply the literal Gamma labels and word-bearing
kernel generators; copied A-map or kernel data from the A0 producer do not.

If the correction formula requires a projection-kernel completion, rebuild
the corresponding bounded kernel BFS using the selected marked generators
and require its order to equal the appropriate accepted value in

\[
 \{1,3,9\}.
\tag{6.1}
\]

### Theorem 6.1 (ONE-COORDINATE FIBRE CERTIFICATION)

The procedure above proves both membership of the claimed zero-K base pair
and that it is the canonical least \((q,g)\) base representative.  The
separate bounded kernel BFS then binds the claimed kernel cursor, word, and
complete ten-coordinate candidate.  It materializes neither the other nine
\(Q_0\) coarse indices nor all ten section-state tables.

#### Proof

Every \(Q_0\) identifier appears exactly once in the streamed accepted
roster.  The chronological recurrence computes its true coordinate value by
the induction in Lemma 3.1.  Duplicate rejection plus (1.2) proves that the
constructed coarse inverse is injective and complete for coordinate \(j\).
The \(\Gamma\) enumeration is complete because it checks all 243 accepted
records, and the full-blob multiplication filters precisely the solutions of
\(a\,s_j(q)=t\).  The bounded kernel BFS supplies exactly the residual
completions allowed by the pinned projection formula.  Hence comparison with
the least base pair proves the canonical-base assertion, while comparison
with the indexed BFS state proves the claimed residual completion.
\(\square\)

The one-coordinate pass is deliberate: it is the minimum complete work for
a canonical-fibre claim.  Merely checking the producer's chosen pair would
not establish leastness.

## 7. Independent selected-correction theorem

### Theorem 7.1 (TASK176 SELECTED-SECTION CHECKER)

Assume the checker:

1. authenticates the physical task176 receipt, checker verdict, manifest,
   recovery data, and their pinned source identities;
2. decodes the Section 1 owners by Lemma 2.1;
3. binds a selected old symbol to its literal chronological raw-record owner;
4. applies Lemmas 3.1 and 4.1 to every selected correction term;
5. applies Lemma 5.1 for nonzero-K terms and Theorem 6.1 for zero-K terms; and
6. independently replays the conjugate word, scalar, eleven occurrences,
   direct H1/H2/P row, and final sparse equality.

Then acceptance of a selected correction is independent of the A0 producer's
copied Q0/Gamma state hex, membership Boolean, schedule label, fibre list,
and digests.  The accepted object is bound instead to the literal task176
owners and the literal old-row source.

#### Proof

Items 1--2 fix the finite authority.  Items 3--5 reconstruct every semantic
input to the selected correction from that authority and prove the relevant
schedule completeness.  Item 6 reconstructs the correction map and compares
it with the final equation.  Therefore changing any producer-supplied
semantic field without changing the independently derived object causes an
equality, schedule, fibre, word, row, or final-equation check to fail.
\(\square\)

The heavy-owner identity in an A0 receipt must name these physically opened
task176/q3/E4/joint owners and their decoded raw identities.  It must not be
defined as a digest of producer-provided selected records.

## 8. Complexity and frontier

For a nonzero-K selected term, the additional work is one bounded parent walk
in \(Q_0\), one in \(\Gamma\), and ten-coordinate replay of those two words.
For a zero-K canonical-fibre term, the complete extra owner is one streaming
coordinate pass through \(N\) parents, all \(G=243\) Gamma entries, and a
kernel BFS of order at most nine.  At no point is a ten-by-\(N\) inverse
required.

```text
TASK176 LOSSLESS SELECTED-Q0/GAMMA AUTHORITY:      PAPER PROOF
NONZERO-K CURSOR RECONSTRUCTION:                   PAPER PROOF
ZERO-K ONE-COORDINATE CANONICAL FIBRE:             PAPER PROOF
A0-v9 INDEPENDENT CHECKER IMPLEMENTATION:          NOT YET AUDITED
A0 POSITIVE CARRIER / COMMON:                      NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                    NONE
```

`R07_TASK176_SELECTED_SECTION_CHECKER_V287_PAPER_GRADE`
