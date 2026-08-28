# R07 bidirectional word/Fox DAG evaluator v282

Author: Sol / 2026-08-29

Status: paper correctness and performance theorem for the next A4
implementation.  A literal word value together with its left-Fox row is a
state in a semidirect product.  Therefore all 6,441 presentation words may
be evaluated exactly once along a shared forward-prefix DAG.  A genuinely
independent checker can build a reverse suffix DAG from the same immutable
literal words and obtain the same leaf values without importing the producer
trie or repeating quadratic whole-prefix free reductions.  No actual A4
closure, word-bearing kernel, anchor, lift, fake certificate, or Ihara
witness is declared. `verified=false`.

## 1. One context as a semidirect product

Fix one of the ten typed E3/E4 contexts.  Let

\[
 \rho:F(X)\longrightarrow G
\tag{1.1}
\]

be its literal group evaluation and let \(M\) be the registered left
\(\mathbf F_3[G]\)-module containing the corresponding Fox row.  Write

\[
 \delta(uv)=\delta(u)+\rho(u)\delta(v)
\tag{1.2}
\]

for the retained left-Fox convention.

Define

\[
 \mathcal S=G\ltimes M,\qquad
 (g,a)\cdot(h,b)=(gh,a+gb).
\tag{1.3}
\]

### Lemma 1.1 (WORD/FOX STATE HOMOMORPHISM)

The map

\[
 \boxed{S(w)=(\rho(w),\delta(w))}
\tag{1.4}
\]

is a monoid homomorphism from freely written source words to \(\mathcal S\).
For a generator \(x\),

\[
 S(x^{-1})=
 \bigl(\rho(x)^{-1},-\rho(x)^{-1}\delta(x)\bigr).
\tag{1.5}
\]

#### Proof

Equation (1.2) and ordinary group multiplication give

\[
 S(uv)
 =(\rho(u)\rho(v),\delta(u)+\rho(u)\delta(v))
 =S(u)S(v).
\tag{1.6}
\]

Putting \(v=u^{-1}\) in (1.2) gives (1.5). \(\square\)

The same statement applies to the left-affine actor used by A4: enlarge
\(M\) by the affine translation coordinate, or take the direct product of
the affine and Fox semidirect states.  All coefficients and block tags remain
typed; no E3/E4 coordinate is identified by a shared label.

## 2. Forward prefix-DAG producer

Let \(W=(w_1,\ldots,w_R)\) be the immutable ordered roster of literal source
words, with \(R=6,441\) for the accepted task198 presentation.  Build the
ordinary prefix trie from the literal signed letters.  Its root represents
the empty word.  If node \(v\) has parent \(p\) and final letter \(\ell\),
define

\[
 S^+(v)=S^+(p)S(\ell),\qquad S^+(\varnothing)=(1,0).
\tag{2.1}
\]

Every roster word points to its terminal node.  Duplicate words point to the
same node but retain distinct row tags and chronological positions.

### Theorem 2.1 (PREFIX-DAG EXACTNESS)

If node \(v\) spells the literal prefix \(a_v\), then

\[
 \boxed{S^+(v)=S(a_v).}
\tag{2.2}
\]

In particular every leaf contains the exact group, affine, and Fox values of
its literal roster word.

#### Proof

Induct on node depth and apply Lemma 1.1 at the last edge. \(\square\)

The producer may derive every A4 row, primitive, discrepancy, and word
ancestry from these leaf states.  It must not subsequently re-evaluate all
literal words through a flat `word_substitute` loop merely to reproduce the
same values.  Direct raw replay remains appropriate for the finite selected
support of a positive word-bearing basis or anchor.

## 3. Reverse suffix-DAG checker

The independent checker reads the same immutable literal word roster, but
does not read the producer trie, node ids, states, leaf digests, pivots, or
transcript.  It builds a trie of reversed signed-letter sequences.  A node
now represents a literal suffix.  If suffix node \(v\) begins with letter
\(\ell\) and has shorter suffix child \(s\), define

\[
 S^-(v)=S(\ell)S^-(s),\qquad S^-(\varnothing)=(1,0).
\tag{3.1}
\]

### Theorem 3.1 (SUFFIX-DAG EXACTNESS AND LEAF AGREEMENT)

For every literal word \(w_i\),

\[
 \boxed{S^-({w_i})=S(w_i)=S^+({w_i}).}
\tag{3.2}
\]

#### Proof

Induction from the empty suffix and Lemma 1.1 prove the first equality.
Theorem 2.1 proves the second. \(\square\)

The two traversals use opposite decompositions:

\[
 (a\ell)\quad\text{versus}\quad(\ell b).
\tag{3.3}
\]

Their implementations can therefore use distinct node layouts, iteration
orders, multiplication wrappers, sparse-row collectors, and canonicalizers.
They share only literal input bytes and the public group/module operations.
This is a semantic cross-check, not equality of two producer-generated
digests.

For an even stronger checker separation, evaluate group values by the
suffix DAG and Fox rows by a dense or bottom-pivot accumulator assembled
from (1.5); no producer echelon or ancestry helper is needed.

## 4. Exact work bound

Let \(E_+\) and \(E_-\) be the nonroot edge counts of the independently
built prefix and suffix tries, and let \(C=10\) be the number of distinct
typed context maps.  After authenticating and parsing the literal words,
the mathematical evaluation counts are exactly

\[
 \boxed{C E_+\quad\text{and}\quad C E_-}
\tag{4.1}
\]

semidirect-state multiplications for producer and checker, respectively,
plus linear leaf lookup and row assembly.  Repeated E3 positions reuse the
same typed group evaluation but retain their separate occurrence prefix,
sign, and row tag.

Thus the combined evaluator cost is

\[
 O(C(E_++E_-)+CR),
\tag{4.2}
\]

before the separate quotient/echelon work.  It is bounded by the total
literal input size and never by the sum of all prefix lengths produced by
successive whole-word reductions.

In particular, an implementation which first builds a trie and then flatly
substitutes and freely reduces all 6,441 long words twice has not used the
theorem's result.  Such a second pass is mathematically redundant.  A cap
during DAG evaluation is `UNKNOWN_RESOURCE` and may serialize the immutable
word roster plus completed node frontier; it is not a mathematical negative.

## 5. From exact leaf states to A4 rows

The A4 construction has three distinct layers.

1. **Literal evaluation.**  Sections 2--3 compute the exact multi-context
   group/affine/Fox state of every primitive and presentation word.
2. **Finite row assembly.**  The registered signs, block tags, source
   actors, translations, and discrepancy recurrence assemble each sparse
   boundary or kernel row from those exact states.
3. **Quotient decisions.**  A lazy finite-coordinate echelon tests only the
   rows needed by the current dual/K/anchor query and retains literal word
   ancestry.

The DAG theorem removes repetition only from Layer 1.  It does not permit:

- omitting any of the 6,441 authority rows;
- replacing a word value by a hash or Boolean;
- accepting transcript fields such as `all_row_dots`;
- identifying contexts with the same display label;
- discarding chronology or coefficient ancestry;
- declaring a quotient NONMEMBER without complete correlation; or
- accepting an A4 anchor without v280's downstream recomputation.

On a positive A4 output, the producer expands and directly replays every
selected basis/anchor word from the raw literal source.  The checker also
replays those selected words independently.  This selected-support replay is
small and is not the rejected flat reevaluation of every long authority row.

## 6. Authority schema and destructive controls

The evaluator's accepted canary roster must be derived from and compared
with the authenticated task198 schema.  A hard-coded required key which the
authority does not contain is a deterministic `UNKNOWN_INPUT`, not a reason
to fabricate the missing field.

Physical mutations must alter the immutable literal roster or one normal
semantic input and rebuild the corresponding DAG.  Required controls include
at least:

- one signed source letter and one word length;
- one parent/letter edge after reconstruction;
- a duplicate word's distinct chronological row tag;
- one typed context map and one inverse-letter state;
- affine multiplication order and Fox left-prefix action;
- one block/sign/translation/discrepancy owner;
- one selected basis word and its raw replay; and
- one v280 rho0/rho1/q anchor recomputation.

Mutating a copied trie digest, transcript Boolean, same-shaped dictionary,
or explicit mutation-name branch is not an owner test.

## 7. Minimal A4-v5 consequence

A bounded successor to the rejected v4 route should:

1. bind only canary keys literally present in the accepted task198 authority;
2. parse each authority source word once;
3. evaluate producer states on the forward prefix DAG;
4. evaluate checker states on a separately built reverse suffix DAG;
5. assemble all mathematical rows directly from the leaf states;
6. remove all post-trie flat whole-word reevaluation;
7. keep the v272 finite active-dual/lazy quotient and discrepancy-ledger
   semantics;
8. checkpoint after each completed evaluation frontier and quotient epoch;
9. replay the finite selected positive support from raw words; and
10. export the complete ordered basis needed for v280, without asking A4 to
    provide a trusted downstream anchor Boolean.

This theorem addresses the literal evaluation bottleneck.  The independent
task343 audit remains authoritative for every additional v4 blocker and for
the complete v5 commission.

## 8. Fixed frontier

```text
WORD + LEFT-FOX ROW AS SEMIDIRECT STATE:           PAPER PROOF
FORWARD PREFIX-DAG EXACTNESS:                      PAPER PROOF
INDEPENDENT REVERSE SUFFIX-DAG EXACTNESS:          PAPER PROOF
POST-TRIE FLAT REEVALUATION OF ALL LONG ROWS:      REMOVED
ALL 6,441 AUTHORITY ROWS:                          STILL MANDATORY
SELECTED POSITIVE RAW-WORD REPLAY:                 STILL MANDATORY
ACTUAL A4 INVARIANT CLOSURE / K BASIS / ANCHOR:    NOT COMPUTED
ACTUAL A5 / A6 / EXACT ENDPOINTS:                  NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                    NOT CONSTRUCTED
```

`R07_BIDIRECTIONAL_WORD_FOX_DAG_EVALUATOR_V282_PAPER_GRADE`
