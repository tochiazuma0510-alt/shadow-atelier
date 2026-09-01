# R07 A4: terminal resource witness envelope (v423)

## Scope

This note repairs only the logical gate which rejected the producer-sealed
row-26 continuation in run `33506331399`.  It does not certify row 26 by
itself, does not retain any of the open row-27 work, and does not alter the A4
search mathematics.

The v28 checker currently asks simultaneously that every terminal counter be
at most its cap and that the counter named in an `UNKNOWN_RESOURCE` witness be
strictly above that same cap.  For the observed reason

```text
dual_pullback:wall_seconds:14402.408729186>14400:state=dual_pullback
```

these predicates are disjoint.

## Typed envelope

Let `C` be the canonical full counter map, `L` the cap map, and let the typed
views `S,H,P,V` be respectively the semantic, host, peak, and restore
validation maps.  Their domains and their equality with the corresponding
coordinates of `C` remain exactly as in v28.  Parse the resource reason as a
unique tuple

\[
(k,v,\ell,s),\qquad k\in\operatorname{dom} C,
\quad v>\ell=L(k),
\]

where `s` is the last replayable state.  A terminal resource envelope is
valid precisely when:

1. every counter in every typed view is numeric and nonnegative;
2. the domain, type, duplication, and equality gates of v28 all hold;
3. `C(k) >= v > L(k)` and the resource's last replayable state is `s`;
4. for every `j != k`, `C(j) <= L(j)`;
5. each occurrence of coordinate `k` in its typed view is equal to `C(k)`
   and is allowed the same unique excess; and
6. no other coordinate in any typed view exceeds its cap.

Equivalently, after all typed-view equality gates have been imposed, the cap
predicate is

\[
 \forall j\in\operatorname{dom}C,
 \qquad j=k\ ?\ C(j)\ge v>L(j) : C(j)\le L(j).
\]

The checkpoint embedded in the terminal is a different object: it is the
last *closed* replayable state and continues to satisfy its ordinary sealed
checkpoint bounds.  The over-cap terminal counter must not be copied into
that earlier checkpoint merely to satisfy the resource witness.

## Soundness

The repaired predicate cannot turn an arbitrary failure into a resource
terminal.  The reason fixes one named, typed coordinate `k`; its advertised
limit must equal the authenticated cap; the canonical counter and the
appropriate typed view must agree and dominate the advertised measured value;
all other coordinates remain bounded; and the checkpoint is independently
authenticated as the last closed state.  Hence exactly one permitted cap
crossing explains the stop.

Conversely, any honest resource stop necessarily has one first observed
triggering coordinate.  Taking that coordinate as `k` satisfies the repaired
predicate, whereas the old universal `<=` predicate rejected it by
construction.  Thus the repair is both necessary and sufficient for the
narrow typed resource envelope.

## Required checker regression gates

A successor checker must reject independently:

- a witness with `v <= limit`;
- a limit different from the authenticated cap;
- a canonical counter below `v`;
- a typed-view value different from the canonical counter;
- a second over-cap coordinate;
- a changed last replayable state;
- a changed closed-checkpoint seal; and
- the original contradictory implementation in which the trigger is still
  passed through the universal `<=` loop.

It must accept a fixture having exactly one wall-time excess and all other
counters in range.  The production artifact must then be replayed by a
checker-only job; fixture success is not evidence for row 26.

## Consequence for v220

After an independent checker-only replay passes, row 26 may advance from
`PRODUCER-SEALED CANDIDATE` to `CROSS-CHECKED CLOSED CURSOR`.  Row 27 remains
unstarted for durable-accounting purposes because its transient rank 138,592
was not checkpointed.  No A4 numerator, compatible lift, fake, or Ihara
witness follows from this envelope repair alone.
