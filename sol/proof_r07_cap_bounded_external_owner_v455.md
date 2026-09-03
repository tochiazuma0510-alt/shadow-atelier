# R07 A0: cap-bounded external-owner stream reduction (v455)

Author: Sol / 2026-09-03

Status: paper protocol theorem for the six positive grades of the first
`2016 -> 54,432` rung.  It uses the Task575-accepted Cayley--Fox caps of v454
to separate the transient linear-algebra owner from the durable transcript
owner.  It changes no row, pivot order, correction space, or membership
criterion.  No production implementation or mathematical terminal is
claimed.  `verified=false`.

## 1. Bounded setting

For one character and one positive grade let (W) be the packed source width,
(R) the v454 rank cap, and (N) the deterministic v452 offer cap.  Across
all six grades,

[
 Rle3530<4096.                                           \tag{1.1}
]

At grade two the exact registered bounds are

[
 (R,N)=(3027,44388)\quad\hbox{or}\quad(3025,44380),       \tag{1.2}
]

with primary and synchronized companion row widths 36,288 and 48,384 trits.
The live accepted matrices therefore occupy at most

[
 27,460,944+36,614,592=64,075,536\ \text{bytes}.          \tag{1.3}
]

The queue order remains exactly v452: all origins first, followed by the four
actor children of accepted pivots in FIFO/pinned-actor order.  In particular,
the next opaque offer identifier is a deterministic function of the committed
transcript; a second persistent queue is not mathematically necessary.

## 2. Split ownership

Use two deliberately small owners.

1. A persistent C process owns only the live normalized primary basis,
   optional normalized companion pivots, the lead-to-pivot map, one offered
   row pair, and the current reduction ledger.  It performs the frozen v4
   first-lead reduction and returns a length-delimited response.
2. The Python caller owns all durable files and the checkpoint manifest.  On
   an accepted response the C process returns the normalized accepted row
   pair; on a dependent response it returns the unscaled companion remainder.
   The caller appends the accepted rows, lead/ID record, and exactly one
   transcript record and EOF offset.

The C process does not append, hash, fsync, rename, or authenticate durable
files.  Conversely, the Python owner does not recompute echelon decisions.
This removes the cross-language partial-transaction ambiguity which defeated
the v2/v3 candidates.

Since (1.1) holds, one reduction reference may be encoded losslessly as the
little-endian 16-bit integer

[
       2i+(a-1),\qquad 0\le i<R,quad a\in\{1,2\}.         \tag{2.1}
]

Decoding gives (i=\lfloor c/2\rfloor) and (a=1+(c\bmod2)).  This compact
encoding is specific to the audited first-rung positive-grade cap; a caller
with (R\ge4096) must be rejected rather than silently truncated.  At grade
two even the pessimistic `N*R` ledger payload is below 269 MB per character,
instead of about 2.15 GB for pairs of two uint64 values.  Actual records remain
variable-length and subject to a checked byte cap.

## 3. Offer transaction

Let the state before offer (s) have normalized pivots
(b_0,\ldots,b_{r-1}).  The C response contains the echoed opaque ID and the
unique v452 reduction

[
 v_s-\sum_{(i,a)\in q_s}a b_i=\bar v_s.                 \tag{3.1}
]

It is one of:

```text
DEPENDENT: q_s, and the unscaled companion remainder when enabled;
ACCEPTED:  q_s, new pivot r, lead, leading coefficient, scale,
           normalized primary row, normalized companion row;
UNKNOWN_RESOURCE / MALFORMED / FATAL: no accepted state mutation.
```

For `ACCEPTED`, the C process installs the new row and lead before replying.
The caller validates the echoed ID and all response lengths, then appends one
provisional durable record.  It never persists its next FIFO cursor before
that complete response has been appended.  Thus the live process and caller
agree after every acknowledged offer; durability is asserted only at an
explicit checkpoint.

## 4. One atomic manifest is sufficient

At a checkpoint boundary the caller:

1. flushes and fsyncs the basis, companion, lead/ID, transcript and offset
   files;
2. copies its incremental digest contexts and records their digests and exact
   committed lengths;
3. writes a small versioned manifest to a sibling temporary file, fsyncs it,
   atomically replaces the published manifest, and fsyncs the directory where
   supported; and
4. only then reports the new committed generation.

The manifest binds session/parent/input identities, widths, caps, encoding,
offer and accepted counts, file lengths, five digests, transcript byte cap,
and the last opaque ID.  `offsets.bin` is `[0,E_1,...,E_s]`, hence has exactly
(s+1) entries and ends at the committed transcript length.

On restart the caller authenticates the manifest and every committed prefix
once, rejects corruption inside a committed prefix, truncates only bytes past
the committed lengths, parses the complete transcript/offset prefix, and
reconstructs the deterministic next offer/FIFO position.  It then launches a
fresh C process which reads the authenticated accepted matrices and lead/ID
records once, checks normalization and unique leads, and rebuilds the map.
No committed offered row is replayed through elimination.

### Theorem 4.1 (crash-safe equivalence)

Assume the frozen v4 reducer, the v452 offer order, checked append operations,
and atomic publication above.  Every published generation reconstructs
exactly the same basis, reduction transcript, actor queue position and next
offer as uninterrupted execution through its committed offer count.

#### Proof

Induct on offers after the preceding published generation.  Before an offer,
the live basis agrees with the accepted matrix prefix.  Determinism of
first-lead reduction gives the same (q_s,\bar v_s), and normalized pivot as
v452.  The C process mutates its basis only for that complete accepted result;
the caller appends the corresponding normalized row and one lossless record
before advancing its queue.  This proves agreement after every acknowledged
offer.

The manifest is the sole commit point.  A crash before its atomic replacement
leaves the preceding manifest authoritative; later bytes are uncommitted and
are truncated.  A crash after replacement exposes the new lengths and digests,
so every complete append is authenticated.  Sequential transcript parsing
recovers all accepted pivot IDs and therefore the origins-first/FIFO cursor.
Loading the normalized accepted matrix rebuilds precisely the live basis,
without eliminating prior offers again.  This is exactly the uninterrupted
state at that offer count. (square)

## 5. Independent replay boundary

The producer-side theorem does not make its own response a certificate.  An
independent checker must compile and exercise the real C service, then for a
production artifact independently:

- authenticate the manifest and complete committed prefixes;
- recompute all transcript starts and the final EOF;
- regenerate every origin and actor offer in registered order;
- densely or independently packed-reduce it against earlier accepted rows;
- compare every coefficient, dependency/acceptance decision, lead and scale;
- replay the synchronized companion update; and
- check `offers = origins + 4*accepted` and exhausted FIFO.

Saturation under v454 may end discovery of the span, but v454's Task575 repair
still requires reductions for every registered origin and all four actor
images of every retained pivot before the artifact is a complete v444/v451
transition presentation.  The normal unsaturated bound (1.2) already covers
those records.

## 6. Claim boundary

```text
V454 RANK/OFFER ENVELOPE:                 AUDIT-PASSED AFTER LOCAL REPAIR
SPLIT C/PYTHON OWNERSHIP:                 PAPER-EXACT HERE
RESUME WITHOUT COMMITTED OFFER REPLAY:    PAPER-EXACT HERE
GRADE-TWO LIVE SOURCE BASIS:              <= 64,075,536 bytes with companion
PRODUCTION WORKER / COMPILED CALIBRATION: NOT YET IMPLEMENTED
GRADE-ONE TERMINAL / A0:                  UNCHANGED / 0 OF 1
COFINAL LIFT / FAKE / IHARA:              NOT DECLARED
verified:                                 false
```

`R07_CAP_BOUNDED_EXTERNAL_OWNER_V455_PAPER`
