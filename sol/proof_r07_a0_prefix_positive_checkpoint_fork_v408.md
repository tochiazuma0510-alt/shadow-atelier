# R07 A0 prefix-positive checkpoint fork (v408)

Author: Sol / 2026-08-31

Status: paper lemma and a strictly positive-only execution contract.  It
permits an immutable occurrence checkpoint with a nonempty frontier to be
forked into a physical-quotient probe while the exact occurrence owner keeps
running.  A positive fork is an ordinary v403/v406 A0 candidate.  A negative
or resource terminal says nothing about the full correction image.  No common
word, compatible lift, fake, or Ihara witness is asserted here.
`verified=false`.

## 1. The retained prefix is already word-bearing

Use the notation of v405--v407.  Let

\[
 \bar W=\widehat J(\Omega)\subseteq\bar U
\tag{1.1}
\]

be the complete occurrence-quotient correction image, and let an authenticated
occurrence checkpoint contain normalized pivots

\[
 p_1,\ldots,p_r\in\bar W.
\tag{1.2}
\]

The frontier need not be empty.  Put

\[
 W_{\rm pre}=\operatorname{span}_k\{p_1,\ldots,p_r\}.
\tag{1.3}
\]

Every pivot has a v406 expression in literal compact-relator instruction
nodes.  Hence

\[
 W_{\rm pre}\subseteq\bar W,
\tag{1.4}
\]

and every element of \(W_{\rm pre}\) has a literal source word in the
registered correction domain.  No exhaustion claim is needed for (1.4).

## 2. A positive prefix solve is a full positive solve

Let \(\bar L_g:\bar U\to\bar Z\) be the exact physical aggregation after
the two PB3 and five central-PB4 boundary contractions.  Let
\(\widetilde D_0\) be the six-action PB4 space of v404, and let \(\bar T\)
be the normalized target.  The complete A0 equation is

\[
 -\bar T\in\bar L_g(\bar W)+\widetilde D_0.
\tag{2.1}
\]

### Theorem 2.1 (PREFIX-POSITIVE FORK)

If

\[
 \boxed{-\bar T\in\bar L_g(W_{\rm pre})+\widetilde D_0,}
\tag{2.2}
\]

then the original A0 equation (2.1) is positive.  Coefficients for (2.2),
together with the retained pivot expressions and selected six-action rows,
give the same finite literal positive certificate required by v403 and v406.

#### Proof

Inclusion (1.4) and linearity give

\[
 \bar L_g(W_{\rm pre})+\widetilde D_0
 \subseteq
 \bar L_g(\bar W)+\widetilde D_0.
\tag{2.3}
\]

Thus (2.2) implies (2.1).  Expand every selected occurrence pivot through
its literal instruction expression, interpret coefficient two as inverse,
and replay its physical aggregate as in v406.  V404 replays the selected
six-action translates.  V403 then turns quotient zero into membership in the
full typed PB3/PB4 boundary, and v399 exactifies the normalized exponent pair.
These are precisely the ordinary positive gates. \(\square\)

The converse is deliberately not asserted.  If (2.2) fails, a missing
frontier descendant may still solve (2.1).  Therefore the only admissible
nonpositive terminal is `UNKNOWN` or `UNKNOWN_RESOURCE`, never NONMEMBER.

## 3. Streaming a fork does not consume the continuation

Take the occurrence checkpoint as immutable input and create two independent
processes.

1. The continuation process retains the queue and applies the four source
   actors exactly as v407.
2. The prefix probe copies the pivot basis and expression/source arrays,
   intentionally performs no source-actor step, and inserts
   \(\bar L_g(p_i)\) into a fresh physical echelon.

For the probe only, after \(\bar L_g(p_i)\) has been inserted, the coordinate
payload of \(p_i\) may be released.  V407 Lemma 5.1 rebuilds the selected
physical source from its expression/source DAG, and the final direct Fox
replay remains mandatory.  The probe's release is safe because that process
will never evaluate another occurrence child.  It does not alter the input
checkpoint and is not a resumable occurrence state.

After the prefix aggregates are inserted, v404's support-hitting oracle
decides (2.2) exactly: it either reaches zero or produces a dual annihilating
the entire six-action space for this fixed prefix.  The latter proves only
failure of (2.2), not failure of (2.1).

### Corollary 3.1 (PARALLEL MONOTONE PROBES)

For authenticated prefix spaces

\[
 W_1\subseteq W_2\subseteq\cdots\subseteq\bar W,
\tag{3.1}
\]

positive probes are monotone: once (2.2) holds it holds for every later
prefix.  Any finite collection of probes can run independently of the one
exact continuation owner.  Their UNKNOWN terminals carry no negative
information and require no merge into the continuation checkpoint.

## 4. Exact execution boundary for the sequence-40 fork

For the present fork the only admissible input is the byte-pinned v12
sequence-40 checkpoint from run `33328450708`:

```text
bytes       326449173
sha256      0b3169fe6e7051fe46a28bb966ffd3dfeada841dce1a6fe2358959dd99402ff1
rank        1316
frontier    906
parent      410
action      1640
physical    0
```

Its frozen one-time `parent -> occurrence_queue` normalization must pass all
ordinary v12 gates before the fork.  The probe must preserve the input file,
must not emit a continuation checkpoint, and must never serialize the
discarded frontier as an exhausted state.  Its positive artifact must replay:

1. the selected pivot expressions to compact-relator atoms;
2. every reconstructed aggregate digest;
3. every selected six-action row;
4. target plus correction plus actions equal to zero;
5. the literal joint-kernel word and exact exponent pair `(0,0)`; and
6. the fresh all-seven Fox/quotient equality.

An independent candidate-envelope checker is not by itself a promotion to
COMMON; promotion still waits for the registered strict literal replay.

```text
PREFIX PIVOTS ARE LEGAL CORRECTIONS:             PAPER PROOF
PREFIX ZERO + SIX-ACTION -> FULL A0 MEMBER:       PAPER PROOF
NONZERO PREFIX REMAINDER -> FULL NONMEMBER:       FORBIDDEN
IMMUTABLE PARALLEL PREFIX PROBE:                  SOUND
SEQUENCE-40 PREFIX PHYSICAL PROBE:                NOT YET EXECUTED
A0 COMMON WORD / FAKE / IHARA WITNESS:            NOT YET OBTAINED
```

`R07_A0_PREFIX_POSITIVE_CHECKPOINT_FORK_V408_PAPER_GRADE`
