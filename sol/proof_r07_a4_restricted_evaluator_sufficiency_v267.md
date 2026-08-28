# R07 A4 restricted evaluator sufficiency v267

Author: Sol / 2026-08-28

Status: paper/interface theorem after v188, task198, v247, and the task323
audit.  It proves that the word-independent first-successor kernel and anchor
do not require reconstruction of all 1,469,664 Q0 states.  The accepted
task198 receipt already contains every source word used by A4; a local
ten-context evaluator, the two generator actions, and a complete lazy PB
boundary oracle are sufficient.  The actual A4/v2 implementation does not
provide this runtime and remains rejected.  No A4 numerator, lift, fake, or
Ihara witness is declared.  `verified=false`.

## 1. Finite A4 input

Let

\[
 \mathcal R=(r_1,\ldots,r_{6441})
\tag{1.1}
\]

be the accepted task198 word-bearing roof-presentation roster, with the three
local-ordinal blocks

\[
 6318+104+19=6441.
\tag{1.2}
\]

Every \(r_i\) is an explicit freely reduced source word with retained
ancestry.  The bridge isomorphism identifies its ten roof-coordinate values
with the seven tagged relation blocks and eleven printed defect occurrences.

Let \(V\) be the typed first-successor defect module and

\[
 \delta:F_2\longrightarrow V
\tag{1.3}
\]

the literal ten-context/seven-block defect evaluation.  Let \(x,y\) act on
\(V\) through simultaneous conjugation in the same ten coordinate groups.
The word-independent successor module is the invariant span

\[
 \boxed{
 K=\left\langle g\delta(r_i):
      1\le i\le6441,\ g\in\langle x,y\rangle
    \right\rangle \pmod D,}
\tag{1.4}
\]

where \(D\) is the complete typed translated PB3/PB4 boundary image.

## 2. The global Q0 section table is a discovery device

Task198's full runtime supplies an operation

\[
 \operatorname{source\_section}(\gamma,q)
\tag{2.1}
\]

by storing parent/letter data for every Q0 state.  This is necessary when a
consumer is given only state ids and must recover a source word.  A4 is not in
that situation: every generator in (1.1) already carries its source word, and
every later word is formed from those words by multiplication, inversion,
and conjugation by \(x^{\pm1},y^{\pm1}\).

### Lemma 2.1 (NO NEW SECTION QUERY)

The construction of (1.4), its coefficient ancestry, and the v247 anchor use
no arbitrary Q0 state-section query.

#### Proof

The initial queue consists of the literal words \(r_i\).  If a retained basis
word is \(w\), closure under a generator uses the explicit word

\[
 xwx^{-1},\quad x^{-1}wx,\quad ywy^{-1},\quad y^{-1}wy.
\tag{2.2}
\]

Linear coefficient two is materialized by the inverse word, and a linear
combination is materialized in retained factor order.  Thus induction on the
closure queue constructs every later source word from an earlier literal
word without referring to a state id.  V247's powered/commutator/anchor words
use the same multiplication and inversion operations on these retained
words.  \(\square\)

The Q0 enumeration was used upstream to prove that the task198 roster is
complete.  Once that result and its independent checker are authenticated,
rerunning the discovery enumeration in every downstream consumer is not a
new mathematical gate.

## 3. Minimal actual evaluator interface

Define a restricted runtime \(\mathcal E_{\rm loc}\) with the following live
operations.

1. `eval(w)`: evaluate one explicit signed F2 word in the ten actual E3/E4
   contexts and convert it, through the task198 bridge, to the seven/eleven
   typed defect row \(\delta(w)\).
2. `multiply`, `inverse`: exact componentwise operations on the ten packed
   coordinate values.
3. `action(letter,v)`: simultaneous conjugation of a typed sparse defect row
   by the ten values of \(x^{\pm1},y^{\pm1}\).
4. `boundary_source(lambda)`: for a separating dual \(\lambda\), return one
   actual translated PB3/PB4 boundary row with nonzero pairing, or certify a
   complete zero correlation for the registered finite boundary family.
5. `group_product`, `group_identity`: direct first-successor replay of the
   retained v247 word equations.

The first three operations can be constructed without Q0 enumeration by
reconstructing the pinned E3/E4 quotients and 31-row context registry, then
building task176's finite deletion map from its fine kernel and the two marked
Q0 permutations.  This uses approximately \(6\cdot59049\) fine-deletion
edges, not \(2\cdot1469664\) Q0 edges.  Actor values for the four signed
letters in ten coordinates give forty cache entries.

### Theorem 3.1 (RESTRICTED EVALUATOR SUFFICIENCY)

Given the authenticated roster (1.1), bridge, and a complete implementation
of the five operations above, A4 can compute and independently certify:

1. the complete invariant kernel \(K\) modulo \(D\);
2. coefficient-bearing raw B/K ancestry for every retained row;
3. word-bearing ancestry for every K basis vector;
4. the two-way basis/change-of-basis identities modulo \(D\); and
5. the v247 word-bearing anchor.

No full Q0 state roster, edge roster, parent/letter store, Gamma Cayley
enumeration, or arbitrary `source_section` operation is required.

#### Proof

Evaluate all initial words using operation 1.  Maintain the span modulo the
complete boundary oracle 4.  Whenever a new K pivot is retained, apply the
four generator actions using operation 3 and enqueue any new pivot.  The
ambient typed first-successor module is finite, so this queue terminates; by
standard invariant-span induction its output is exactly (1.4).

Every row operation is recorded in the immutable raw B/K label space.  Lemma
2.1 materializes the same operations by literal words, while operations 1--3
replay their defects.  This proves items 2--3.  Rebuilding the closure with an
independent pivot order and reducing both bases against each other proves item
4 without cross-basis coordinate equality.  Finally, v247 uses only retained
basis words, scalar inversion/powering, explicit commutators, coarse/context
evaluation, and direct equality; operations 1--5 supply exactly those data.
No step asks for (2.1).  \(\square\)

## 4. Completeness belongs to the boundary oracle

Eliminating the global Q0 roster does not permit a bounded scan to be called
a boundary NONMEMBER result.  At any query the oracle must either:

- exhibit one typed PB3/PB4 boundary preimage;
- produce a dual whose correlation with the **complete registered boundary
  family** is zero; or
- return `UNKNOWN_RESOURCE`.

The complete family is generated from the finite PB3/PB4 presentations and
their registered translation actions.  A lazy dual correlation is allowed;
its zero branch must cover the full family.  This is the same positive/zero
discipline as v140 and does not require Q0 source sections.

## 5. Exact audit consequence

Task323 found that A4/v2 has no actual codec/runtime and stops before positive
work.  Theorem 3.1 identifies the smallest sound repair.  It is insufficient
to replace the unconditional stop by a shaped object or by the synthetic
coordinate-wise codec.  A corrected consumer must bind:

- the accepted authority-v2 manifest and checker verdict;
- the actual E3/E4/context/deletion objects;
- direct re-evaluation of all 6,441 roster words;
- forty actual actor values;
- the complete boundary oracle; and
- a helper-nonshared reconstruction of the same kernel and anchor.

If some future code reaches an operation requiring an arbitrary Q0 state id
not accompanied by an authenticated word, it is outside Theorem 3.1 and must
stop `UNKNOWN_INPUT` rather than silently instantiate the full task179
runtime.

```text
TASK198 6441 SOURCE WORDS ALREADY EXPLICIT:          CROSS-CHECKED INPUT
ARBITRARY Q0 SOURCE-SECTION REQUIRED BY A4:          NO (PAPER PROOF)
LOCAL E3/E4 + DELETION EVALUATOR SUFFICIENT:         PAPER PROOF
COMPLETE PB BOUNDARY ORACLE STILL REQUIRED:          YES
ACTUAL LOCAL EVALUATOR IMPLEMENTATION:               PENDING TASK328
ACTUAL A4 KERNEL / ANCHOR:                           NOT COMPUTED
LIFT / FAKE / IHARA:                                 NOT ESTABLISHED
```

`R07_A4_RESTRICTED_EVALUATOR_SUFFICIENCY_V267_PAPER_GRADE`
