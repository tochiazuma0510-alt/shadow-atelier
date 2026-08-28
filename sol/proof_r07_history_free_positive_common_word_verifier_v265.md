# R07 history-free positive common-word verifier v265

Author: Sol / 2026-08-28

Status: paper proof and corrected A0 trust boundary after v140, task192/v3,
v256, task319, and task321.  It sharpens v140 Section 4: authenticating every
column-generation epoch is sufficient for reproducing the search, but is not
necessary for the soundness of a positive existential witness whose final
word and boundary identity are independently replayed.  The staged v3
checkpoint may therefore be used as discovery state without reconstructing
its missing historical dual epochs.  No COMMON word has yet been obtained;
A0 remains 0/1 and no lift, fake, or Ihara witness is declared.
`verified=false`.

## 1. Discovery and positive verification are different propositions

Retain v140's notation.  The registered joint kernel is

\[
 \Omega\triangleleft F_2,
\]

the raw defect map is

\[
 \mathscr V:\Omega\longrightarrow Z,
\]

the complete translated PB3/PB4 boundary image is \(D\leq Z\), and the fixed
base defect is \(T\in Z\).  The A0 existential statement is

\[
 \boxed{\exists c\in\Omega:\quad T+\mathscr V(c)\in D.}
\tag{1.1}
\]

A column-generation transcript proves how one searched for such a \(c\).
Equation (1.1), however, is certified by one literal \(c\) and one boundary
preimage.  These are logically different certificates.

### Lemma 1.1 (POSITIVE-WITNESS TRUST BOUNDARY)

Let an arbitrary discovery process, possibly using cached or heuristic
internal state, output a finite object \((c,d)\).  Suppose a helper-nonshared
checker, using only immutable registered inputs and the literal output,
independently verifies

\[
 c\in\Omega,\qquad d\in D,\qquad
 T+\mathscr V(c)=d.
\tag{1.2}
\]

Then (1.1) holds.  Soundness of this positive conclusion does not require
the checker to reconstruct any earlier dual, rejected candidate, chosen
column, rank-increase epoch, scan prefix, or scheduler decision.

#### Proof

The first component of (1.2) supplies an admissible correction word and the
second supplies a boundary element.  The last equality is exactly (1.1) for
that word.  The means by which \((c,d)\) was discovered does not occur in the
implication.  \(\square\)

The omitted history can affect whether the search terminates, whether it is
reproducible, and whether a claimed exhaustive negative result is valid.  It
cannot turn a directly replayed true equality (1.2) into a false one.

## 2. A compact proof object for R07

A positive receipt need retain only the following mathematical data.

1. One freely reduced correction word \(c_\star\), or equivalently the final
   exactified word \(c_{\rm exact}\) together with the registered exactifying
   words.
2. The independently selected task179 relator words of ordinals 3, 9, and
   12 and the literal exactification
   \((c_\star,u_0,v_0,h,c_{\rm exact})\).
3. One sparse coefficient vector on the complete, typed PB3/PB4 boundary
   roster whose direct sum is \(d\).
4. Exact source/run/head/member identities for the task198 evaluator and all
   other immutable inputs used to reconstruct \(T\), \(\Omega\), \(D\), and
   the seven defect occurrences.

The independent checker must then perform the following finite replay.

1. Rebuild the joint evaluation of \(c_\star\), \(u_0\), \(v_0\), and
   \(c_{\rm exact}\); require the registered joint-kernel identities.
2. Recompute both integer exponent sums and require the exact zero gate after
   exactification.
3. Reconstruct \(T\) and directly evaluate the full correction word in both
   hexagons and the printed five-factor A.18 pentagon, with all block tags and
   eleven correction occurrences retained.
4. Rebuild every boundary generator referenced by the sparse coefficient
   vector from the authenticated PB3/PB4 presentation, sum it over
   \(\mathbf F_3\), and require literal equality with the direct residual.
5. Reject a boundary word inserted into the source correction, a changed
   right-correction convention, a coface-order change, an exponent alias, or
   a source value from a different joint state.

This is a direct instance of Lemma 1.1.  It is also strictly smaller than a
receipt containing all retained search columns and their successive duals.

### Theorem 2.1 (HISTORY-FREE POSITIVE COMMON-WORD CERTIFICATE)

Acceptance of the compact replay above proves the same finite B4 common-word
statement as v140 Theorem 2.1.  No `boundary_epoch_history` field is a
mathematical prerequisite for this positive terminal.

#### Proof

The joint-kernel and exponent gates type \(c_{\rm exact}\) in the allowed
source domain.  Steps 3--4 give

\[
 T+\mathscr V(c_{\rm exact})=d\in D.
\]

Lemma 1.1 applies.  The registered exactification identities ensure that the
same literal word is used by every gate.  \(\square\)

## 3. What v140 Section 4 was proving

V140 Section 4 required the checker to authenticate the preceding basis,
dual, chosen ACTIVE column, and new pivot at every retained iteration.  That
contract remains valid and useful for an **algorithm-trace certificate**:
it proves that the producer followed the registered positive-only column
generation and makes restart decisions reproducible.

It is stronger than Theorem 2.1.  In particular, the seven final gates in
v140 Section 4 already culminate in direct evaluation of the complete word.
Once that direct evaluation and the boundary equality are independently
recomputed, the preceding search trace is no longer load-bearing for the
existential conclusion.  Thus the following implication must not be
reversed:

\[
 \text{authenticated search trace}
 \Longrightarrow \text{accepted final witness},
\]

whereas an accepted final witness need not expose an authenticated search
trace.

This note supersedes v140 Section 4 only as a statement of **necessity for a
positive terminal**.  It does not weaken v140's theorem or any negative-
claim requirement.

## 4. Application to the task192 checkpoint

The run-33149728601 checkpoint contains 2,896 retained columns and resumes
the same rank/dual state, but it has no complete
`boundary_epoch_history`.  Task321 correctly observed that the approximately
2,896 historical dual epochs cannot be reconstructed from the current
snapshot.  Therefore that checkpoint cannot support a new claim that every
past epoch was independently replayed.

Theorem 2.1 shows that this absence does not block a positive-only search:

- the checkpoint and its columns may be treated as discovery hints;
- a persistent parallel correlation adapter may continue from that state;
- a resource stop remains only `UNKNOWN_RESOURCE` and carries no negative
  mathematical claim; and
- `COMMON` is accepted only after a fresh compact checker ignores the search
  history and reconstructs (1.2) directly.

Even a malformed heuristic column cannot create a false positive under this
boundary.  It may steer the search badly or manufacture a proposed word, but
the independent literal replay rejects that word unless (1.2) is actually
true.  For the same reason the adapter must never emit `SEPARATOR`,
`NONMEMBER`, an exhaustive-zero claim, or a completeness claim from this
history-free route.

The existing task192/v3 checker already contains most of the necessary direct
positive logic: on `COMMON` it reconstructs \(c_\star\) from coefficients,
selects the three exactifying relators independently, recomputes exponent
divisibility, invokes the independent common-word validator, re-evaluates the
exact correction word, and checks the boundary sum.  Its additional replay
of the entire retained-column roster is useful trace authentication but is
not needed by Theorem 2.1.  A new compact checker must duplicate the direct
word/boundary mathematics without importing either producer and without
accepting receipt Booleans as evidence.

## 5. Honest nonpositive and resource semantics

The relaxation is deliberately asymmetric.

### Proposition 5.1 (NO HISTORY-FREE NEGATIVE TERMINAL)

An incomplete or unauthenticated discovery history cannot prove
\(-T\notin D+\mathscr V(\Omega)\), cannot prove that all ACTIVE columns were
absent, and cannot prove search completeness.

#### Proof

A negative assertion quantifies over the full boundary/correction family.
One final rejected candidate supplies no such universal statement.  Missing
epochs or scan suffixes may contain an ACTIVE column.  \(\square\)

Consequently every nonpositive adapter exit is typed only as
`UNKNOWN_INPUT` or `UNKNOWN_RESOURCE`.  Its checkpoint can be authenticated
for transport, counters, caps, and deterministic continuation without being
promoted to a mathematical proof object.  Historical counters are never
reset, but they are telemetry, not evidence for (1.1) or its negation.

## 6. Correct implementation consequence

The next A0 adapter need not add retrospective epoch history to the v3 owner.
It should instead:

1. keep the v3 serial rank/dual/candidate owner and one persistent worker
   pool for complete frozen-dual correlations;
2. consume the existing checkpoint only as authenticated discovery state;
3. preserve exact pair arithmetic, deterministic merge, and truthful live
   resource counters for engineering correctness;
4. output no mathematical claim on a resource/input stop;
5. on a proposed `COMMON`, emit the compact word plus boundary preimage and
   run a helper-nonshared history-free checker; and
6. count A0 only if that checker directly accepts the literal equality.

This removes task321's retrospective-history blocker while retaining the
actual soundness boundary.  It does not guarantee the parallel search will
find a word or fit the wall/RSS envelope.

```text
POSITIVE WITNESS NEEDS FULL SEARCH HISTORY:          FALSE
COMPACT WORD + BOUNDARY DIRECT REPLAY IS SUFFICIENT: PAPER PROOF
TASK321 RETROSPECTIVE EPOCH-HISTORY BLOCKER FOR A0+: REMOVED
NEGATIVE / SEPARATOR WITHOUT COMPLETE HISTORY:      FORBIDDEN
CURRENT SERIAL RUN 33163964747:                      STILL RUNNING
ACTUAL A0 COMMON + INDEPENDENT ACCEPTANCE:           0/1
COMPATIBLE LIFT / FAKE / IHARA:                      NOT ESTABLISHED
```

`R07_HISTORY_FREE_POSITIVE_COMMON_WORD_VERIFIER_V265_PAPER_GRADE`
