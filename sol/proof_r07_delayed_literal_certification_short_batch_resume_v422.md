# R07 delayed literal certification and short-batch resume theorem (v422)

Author: Sol / 2026-09-02

Status: paper theorem for the A0 positive-search owner.  It does not promote
the recovered rank-99 state before independent semantic replay, and it does
not assert COMMON, a compatible lift, fake, or an Ihara witness.
`verified=false`.

## 1. Fixed anchored-batch setting

Let (V) be the current physical span over (mathbf F_3), let (T) be the
target, and let

\[
  \lambda\in V^\perp,\qquad \lambda(T)\ne0                 \tag{1.1}
\]

be the dual returned by the exact echelon solver.  During one anchored batch
(lambda) is fixed.  The registered selector enumerates candidates (t) in
its existing deterministic order and supplies a formula scalar

\[
  s(t)=\lambda(r(t)),                                      \tag{1.2}
\]

where (r(t)) is the actual aggregated physical row of the literal
conjugate.  Equation (1.2) is the already frozen occurrence/adjoint identity;
v422 does not enlarge the selector universe or introduce a new coordinate
model.

After (j) retained rows, write

\[
  V_j=V+\langle r(t_1),\ldots,r(t_j)\rangle .             \tag{1.3}
\]

The physical echelon owner exposes a non-mutating exact `reduce(row)` and a
mutating `add(row,source)`.  This ABI is already used in the accepted
rank-ladder owner before insertion.

## 2. Delayed literal certification

For a correction candidate use the following order.

1. Compute the selector scalar (s(t)).  If it is zero, continue as in the
   existing positive search.
2. Compute `replay_atom` and its aggregate (r(t)) once.
3. Compute the non-mutating remainder of (r(t)) modulo (V_j).  If the
   remainder is zero, discard the dependent candidate without constructing
   the full conjugate row a second time.
4. Only for a nonzero remainder, construct
   (\delta s_i\delta^{-1}), recompute it through full `seed_v12`, check
   equality with (r(t)), check the exact exponent pair and forbidden-(E)
   condition, check (1.2), and form the literal receipt.
5. Insert once and require the actual pivot to equal the pivot predicted by
   the non-mutating remainder.

### Lemma 2.1 (retained sequence is unchanged)

Assume the frozen formula identity (1.2) and literal replay identity.  The
procedure above retains exactly the same ordered rows as the eager Task451
procedure, which performs the full `seed_v12` and exponent work before asking
whether the row raises rank.

#### Proof

Both procedures inspect the same selector order and compute the same row
(r(t)).  At the instant (t) is inspected, `reduce` is zero exactly when
(r(t)\in V_j), which is exactly the `rise=false` branch of `add`.  In that
case insertion changes no span and no row can occur in a positive
certificate.  If the remainder is nonzero, the delayed procedure performs
all checks formerly performed eagerly and then inserts the same row at the
same canonical pivot.  Induction on the selector order gives the same
retained sequence and hence the same (V_j). (square)

The omission for a dependent row is deliberately only a positive-search
optimization.  It is not evidence that all candidate implementations are
globally correct and must not be used for a NONMEMBER or exhaustion claim.
Every row that affects A0 remains literally certified and independently
replayed.

### Corollary 2.2 (safe cost removal)

For each nonzero-scalar dependent correction, one full `seed_v12` evaluation
and one conjugate exponent computation are removed.  `replay_atom` remains,
because exact physical dependence cannot be decided without the row.  No
claim is made about candidates with scalar zero.

## 3. Closed-batch size and loss bound

Let a batch close after (b) retained rises.  A close performs the single
post-batch dual update, writes the literal receipts, and atomically replaces
the durable checkpoint.  If a resource stop interrupts an open batch, its
working mutations are discarded and the preceding closed checkpoint is
returned.

### Lemma 3.1 (open loss bound)

At most (b-1) newly retained rows can be lost at a resource stop.

#### Proof

The (b)-th retained row closes the batch and is made durable.  Hence an open
batch contains at most (b-1) retained rows. (square)

Increasing (b) does not reduce selector, `replay_atom`, or literal-check
work; it only removes some post-batch dual updates and checkpoint writes.
The recovered Task451 run gives a direct calibration: (b=16) closed at
ranks 67, 83, and 99 before its 7,200-second cap.  A one-shot (b=64) owner
may instead spend the same cap without closing any batch.  Therefore the next
production owner uses (b=16) by default.  This is an evidence-backed loss
bound, not a claim that 16 is globally optimal.

## 4. Progress-preserving resume

A closed checkpoint (C) contains the frozen rank-51 prefix, all closed batch
receipts, the round, physical rank, current dual profile, owner binding, and a
canonical seal.  Restoration reconstructs a fresh physical owner and
semantically replays only the retained rows.  Its cost is proportional to the
accepted list (56 rows at recovered rank 99), not to the rejected candidate
universe or a stored boundary closure.

Let (a_0) be the accepted count at invocation start and (a) the live
count.  A per-invocation resource cap is

\[
  \rho=a-a_0.                                               \tag{4.1}
\]

It must not be confused with the historical total (a-8).  Resetting
(ho) after an authenticated resume does not widen the registered universe:
it only bounds one host process.  All historical rows remain in (C), and
the deterministic next round still begins after the last closed batch.

### Theorem 4.1 (resumable anchored ladder)

Suppose each input checkpoint is independently semantically replayed, every
retained new row satisfies Section 2, and each output is committed only at a
closed batch boundary.  Repeated invocations with the per-run cap (4.1)
produce one monotone chain

\[
  V\subseteq V_1\subseteq V_2\subseteq\cdots              \tag{4.2}
\]

of the same registered literal span.  No closed rise is lost or recomputed as
new work.  If some closed state has zero remainder, its selected literal rows
give an A0 COMMON candidate subject to the existing positive replay.

#### Proof

Semantic restoration gives exactly the preceding (V_j), target remainder,
and next round.  Lemma 2.1 gives the deterministic next retained rows.
Atomic close appends them to the checkpoint, so induction gives (4.2).
Resource interruption returns the preceding closed member of the chain by
Lemma 3.1.  If the remainder is zero, the unchanged echelon coefficient and
literal positive replay express the target in the retained registered span.
(square)

This theorem does not turn a finite miss into a negative result.

## 5. Typed bootstrap and driver obligations

Before expensive owner construction, authenticate the resume bytes and write
a sealed bootstrap output describing the same closed state.  Construction,
prefix replay, batch replay, and initial dual computation all lie inside the
RESOURCE boundary.  If any of them hits a wall/RSS gate, return
`UNKNOWN_RESOURCE` with that closed bootstrap seal; never return a terminal
`UNKNOWN` without durable state.

The production driver has explicit INITIAL/RESUME input, distinct immutable
input and fresh output paths, `set -euo pipefail`, an external timeout/RSS
wrapper, and exact-one producer/checker terminal markers.  A resume artifact
is authenticated before use.  The checker replays every retained row and
every closed anchor/post-batch digest; it does not accept a checkpoint merely
because its SHA-256 is self-consistent.

The recovered rank-99 Task451 state may be the first base of Theorem 4.1 only
after Task467's repaired independent checker completes successfully.  Until
then it remains structurally authenticated candidate data.  Its immutable
repository copy is

```text
search/certs/d972_r07_a0_dual_anchored_rank99_candidate_v1.json
173082 bc435660b299f9d72cb2ac10f9765da4ff7f3a16a75242264451c391f20bd358
```

The word `candidate` in that filename is load-bearing and may be removed only
by a new version after Task467 passes.

## 6. Acceptance gate

```text
Task467 rank-99 full semantic replay PASS
registered selector and formula identity unchanged
non-mutating reduce before expensive retained-only literal checks
actual add pivot equals predicted pivot
batch_cap=16 default; closed checkpoint only
per-invocation rise cap separated from historical accepted count
explicit authenticated resume and fresh output
initialization/replay inside typed RESOURCE boundary
producer/checker pipefail, timeout/RSS, exact-one markers
no NONMEMBER/fake/Ihara claim from a finite miss
```

`R07_DELAYED_LITERAL_CERTIFICATION_SHORT_BATCH_RESUME_V422_PAPER_GRADE`
