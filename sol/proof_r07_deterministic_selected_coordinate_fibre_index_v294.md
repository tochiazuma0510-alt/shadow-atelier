# R07 deterministic selected-coordinate fibre index (v294)

## 0. Status

This note supplies the missing ordinary checker contract for the A0 selected
`K=0` fibre.  It replaces the v10 per-record Python `dict[bytes,int]` plus
sorted-tuple construction.  It is an algorithm-and-proof contract only: no
candidate has been run, no v12a artifact exists, and A0 remains `0/1`.

The immutable numerical inputs are

```text
N = |Q0| = 1,469,664,
|Gamma| = 243,
w_i = 40  for i=0,...,4,
w_i = 154 for i=5,...,9,
|ker(pi_i)| = [9,9,9,9,9,1,1,1,3,3].
```

## 1. Typed input owners

Fix one selected coordinate `i`.  The ordinary validator receives, from
separately authenticated physical owners:

1. the chronological one-based Q0 parent and letter arrays;
2. the two marked generator blobs of width `w_i`;
3. the chronological one-based Gamma parent/record arrays and their marked
   coordinate transitions;
4. the authenticated literal `A_i` family;
5. the target coordinate blob `t` of width `w_i`;
6. the ordered kernel word-generator roster; and
7. the claimed selected qid, gid, kernel cursor, word, and canonical full
   ten-coordinate kernel-state blob.

The producer and checker may share the frozen finite-group multiplication and
inverse operations.  They must not share this composite index constructor,
Gamma recurrence, kernel BFS, mutation harness, or acceptance routine.

## 2. Q0 state store and exact open-address index

Allocate, after checking the caps,

```text
S : bytearray(N*w_i)
T : array('I', 2^22), initially zero.
```

Slot value zero means empty; a stored value is the one-based qid.  Iterate
`qid=1,...,N` once.  State 1 is the identity.  Every later state is computed
from its strictly earlier parent state and the registered marked generator.
Reject a zero/future parent, an unregistered letter, or a width mismatch
before writing the slot.

For a width-`w_i` blob `s`, let `h_i(s)` be a fixed, versioned, deterministic
64-bit hash over all bytes of `s`.  Its particular collision resistance is
not a soundness assumption.  It only chooses the initial slot.  Insert qid by
linear probing:

```text
j = h_i(s) mod 2^22
while T[j] != 0:
    q = T[j]
    if S[(q-1)w_i : qw_i] == s: reject duplicate full state
    j = (j+1) mod 2^22
T[j] = qid.
```

Lookup of a full blob `u` uses the identical probe sequence.  At every
occupied slot it compares all `w_i` retained bytes, not a prefix, hash,
integer key, or copied qid.  It returns the matching qid, or `NONE` at the
first empty slot.  A hash or coarse-prefix collision therefore changes only
runtime, never the answer.

The implementation may additionally report the old degree-36/144 coarse
prefix for diagnostics.  A coarse match is never acceptance.  A missing full
match is `NONE`, not an exception and not a producer cursor fallback.

### Lemma 2.1 (exact lookup)

After the insertion pass, lookup returns qid exactly when the queried blob is
the qid-th chronological state, and otherwise returns `NONE`.

Proof.  Linear probing preserves a contiguous probe cluster from every
initial slot to the first empty slot.  Every inserted state is in its own
cluster.  Lookup traverses that same cluster and accepts only byte equality.
If it reaches an empty slot, no later insertion with that initial slot can
occur beyond it.  Hash collisions and equal coarse prefixes are harmless
because neither is the equality predicate.  QED.

The validator streams, in qid order, a canonical full-state digest and a
separate slot-table digest.  It does not create a sorted list of 1,469,664
Python tuples.

## 3. Chronological Gamma first-gid table

Compute the selected coordinate Gamma states once in ordinal order using its
actual parent transition.  Keep at most 243 width-`w_i` blobs.  For each
distinct blob `a`, record only its least ordinal `first_gid(a)`.  Recompute:

```text
set of distinct Gamma blobs,
first-gid map,
chronological transition digest,
distinct-state digest.
```

Compare the distinct blob set with the authenticated literal `A_i` family.
This is coordinate-typed equality; a projected 970-byte Gamma owner is not a
full JointGroup object and neither codec may be substituted for the other.

For every distinct Gamma state `a`, form the full coordinate blob

```text
u = a^(-1) * t
```

and call exact Q0 lookup on `u`.  A `NONE` result is skipped.  If lookup
returns qid, directly recompute and require `a*S[qid]=t` in the selected
coordinate, then append `(qid,first_gid(a))`.  Require the candidate set to be
nonempty and select its lexicographic minimum.

### Lemma 3.1 (complete least base)

The selected pair is the lexicographically least `(qid,gid)` satisfying
`Gamma[gid]*Q0[qid]=t`.

Proof.  Every gid has one Gamma blob `a`; equal blobs have identical solution
qids, so only their least gid can improve a lexicographic pair.  The
first-gid table retains exactly that representative.  Lemma 2.1 finds exactly
the Q0 state `a^(-1)t` when it exists, and the direct product check removes no
true solution.  Hence the candidate roster is precisely the set of relevant
least-gid solutions.  Taking its minimum proves the claim.  QED.

This corrects v10's unconditional `qid is not None`: nonmembers are skipped,
while the final nonempty/leastness assertion remains load-bearing.

## 4. Incremental kernel BFS, including the trivial case

Decode the authenticated kernel word generators in their registered order,
including their registered inverses.  Precompute each generator's full ten-
coordinate state once.  Start the BFS roster with

```text
(word=[], full_state=identity_ten_state).
```

For each queue state and generator, compute the next full state by one exact
state multiplication and the next word by the registered free reduction.
Deduplicate by complete ten-coordinate state equality.  Do not replay the
whole accumulated word at every edge.  For every accepted state, require that
coordinate `i` is the identity and retain

```text
cursor, reduced word, canonical full ten-coordinate blob, parent, generator.
```

An empty generator roster is valid exactly when the registered kernel order
is one.  Its completed BFS is the singleton identity roster.  Thus coordinates
S5, S6, and S7 are not falsely rejected.

At completion require the exact registered order, canonical chronological
roster digest, and exact equality of the claimed cursor's word and full state.
No missing selected word may fall back to a candidate cursor or zero.

### Lemma 4.1 (kernel roster exactness)

If the registered generators generate `ker(pi_i)`, the incremental BFS roster
is exactly that kernel and the cursor owner names one unique retained state.

Proof.  Identity is present.  Closure follows from exhausting every retained
state under every registered generator.  Every retained state lies in the
kernel because its selected coordinate is checked to be identity.  Conversely
every generator word is reached inductively.  Full-state deduplication
identifies precisely equal group elements.  The exact-order comparison rules
out an incomplete or enlarged roster.  The cursor equality then binds the
claimed word and state to the unique chronological entry.  QED.

## 5. Memory and work envelope

The largest selected-coordinate persistent allocation is the E4 case:

```text
state store: 1,469,664 * 154 = 226,328,256 bytes
qid slots:   4,194,304 * 4   =  16,777,216 bytes
                                      total = 243,105,472 bytes.
```

This is below the registered 256 MiB payload cap by 25,329,984 bytes.  The
Gamma table, kernel roster, current state, hash state, and fixed framing must
have a separately checked cap within that margin.  No full-state Python bytes
keys, qid Python integers per entry, sorted tuple roster, or second coordinate
store is permitted.  The cache is constructed once per coordinate and reused
by every selected K0 record for that coordinate.

The semantic work is one Q0 transition per nonidentity qid, one bounded probe
sequence per insert/lookup, 243 Gamma transitions, and at most the registered
kernel-order times generator-count BFS edges.  Probe count, full-byte
comparisons, group products, bytes allocated, and peak live phase are metered
before expensive allocation or multiplication.

## 6. Ordinary-validator and mutation boundary

The ordinary validator returns a sealed summary only after all of Sections
2--4 pass.  Actual-owner SELFTEST mutations must enter this same routine and
have exact first reasons for at least:

```text
Q0 parent/letter chronology,
marked generator width/value,
full-state store byte,
slot qid/probe placement,
full-state lookup mismatch and NONE,
Gamma parent/transition and first-gid,
literal A_i equality,
target product and lexicographic leastness,
empty/nonempty kernel-generator roster,
kernel edge/full state/order,
cursor word/full-state binding,
allocation/probe/deadline cap.
```

A detached miniature table, mutation-name rejection branch, copied Boolean,
or shape-only digest is not this validator.

## 7. Consequence for the active program

V294 removes the claimed missing local API.  A0-v12a remains obliged to wire
this independently on producer and checker sides, together with every other
task352 finite repair, before a fresh Sol(max) audit.  Until then:

```text
A0 COMMON + independent checker = 0/1
SELFTEST bootstrap              = UNEXECUTED
compatible lift / fake / Ihara  = NONE
```

`R07_DETERMINISTIC_SELECTED_COORDINATE_FIBRE_INDEX_V294`
