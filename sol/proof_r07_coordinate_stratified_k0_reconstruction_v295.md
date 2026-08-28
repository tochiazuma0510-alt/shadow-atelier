# R07 coordinate-stratified K0 reconstruction and audit theorem (v295)

## 0. Scope and claim boundary

This note fixes the exact deterministic selector and checker schedule for the
`K=0` correction fibre used by A0.  It consumes only the frozen task176
chronological Q0/Gamma owners and the typed E3/E4 group operations.  It proves
neither A0 COMMON nor a lift, fake, or Ihara witness.  A malformed owner,
duplicate state where injectivity is required, resource exhaustion, or a
failed replay is a typed input/resource stop, never a negative mathematical
result.

The notation is:

```text
N = 1,469,664,       C = 2^22 = 4,194,304,
w_i = 40  (0 <= i < 5),       w_i = 154 (5 <= i < 10),
d_i = 36  (0 <= i < 5),       d_i = 144 (5 <= i < 10).
```

For a fixed coordinate `i`, `Q_i(q)` is the `w_i`-byte state obtained by
chronological replay of task176 Q0 parent/letter record `q`, and `G_i(g)` is
the corresponding replay of the Gamma parent/record owner.  State equality
below always means equality of all `w_i` bytes, not only the first `d_i`
permutation bytes.

## 1. Deterministic full-state table

Store `Q_i(1),...,Q_i(N)` in chronological order in one packed byte array and
use an `array('I')` table of exactly `C` slots.  The initial slot of a state
`s` is

```text
H(s) = uint64_le(SHA256("v12a-k0-full-state\0" || s)[0:8]) mod C.
```

Resolve collisions by increasing the slot modulo `C`.  A nonzero slot stores
`q`, not a pointer or a process-local object.  Every comparison after a hash
collision compares the complete retained `w_i` bytes.  Encountering a second
chronological Q0 id with the same complete state is a typed input stop unless
the implementation is explicitly versioned to retain the least id; it may
not silently overwrite an earlier id.  Python's process-randomized `hash` is
forbidden.

On lookup, an empty slot means `MISS`.  A hash collision or a matching coarse
prefix with unequal full bytes also continues/proves `MISS`; neither may fall
back to a cursor, zero, or arbitrary candidate.  Thus a successful lookup is
exactly a physical Q0 state equality.

### Lemma 1 (table soundness and determinism)

If construction completes, lookup returns `q` exactly when the retained
complete state equals the query.  The returned id, the slot array, and their
streaming digests are functions only of the chronological physical state
roster.  In particular they are independent of process hash seeds and query
order.

**Proof.** Linear probing searches the same finite probe sequence used at
insertion.  Before its first empty slot, every occupied slot is compared by
complete bytes.  Hence an equal state is found and an unequal state is never
returned.  The fixed hash, chronological insertion order, fixed capacity,
and first-empty rule determine every slot.  The duplicate stop makes the
state-to-id relation single valued.  QED.

## 2. Least `(qid,gid)` selector

Replay all 243 Gamma states chronologically and form

```text
first_i(a) = min { g : G_i(g) = a }.
```

The set of keys must equal the literal task176 A-family at coordinate `i`.
For a typed target `z`, define

```text
C_i(z) = { (q,g) : G_i(g) * Q_i(q) = z }.
```

For every distinct Gamma value `a`, compute `s=a^-1*z` using the typed group
law and perform one exact full-state Q0 lookup.  If it hits `q`, register
`(q,first_i(a))`; on a miss, register nothing.  Return the lexicographically
least registered pair, or `NONE` if there is none.

### Lemma 2 (first-Gamma compression preserves the least pair)

The procedure returns `min C_i(z)` in lexicographic `(qid,gid)` order.

**Proof.** For fixed `a`, the equation is equivalent to `Q_i(q)=a^-1*z`, so
Lemma 1 supplies precisely its Q0 solution.  All Gamma ids giving `a` have
the same Q0 solution, and their least pair uses `first_i(a)`.  Taking the
minimum over distinct `a` therefore takes the minimum over all of `C_i(z)`.
QED.

The producer's search order is not changed by this lemma.  It must still scan
roster rows, sorted support targets, and kernel states in the preregistered
order.  Only the implementation of one requested singleton-fibre lookup is
replaced.

## 3. Word-bearing kernel BFS

For coordinate `i`, take the frozen ordered positive generator roster

```text
Gamma_S0_generators, adjusted_L_generators
```

and append each inverse immediately after its positive generator.  Start at
the full ten-coordinate identity.  Breadth-first search in that exact
generator order.  An edge from stored state `(u,S(u))` by generator
`(v,S(v))` stores

```text
red(uv),             S(u)S(v).
```

Before accepting every new state, independently replay `red(uv)` in all ten
typed coordinates and require equality with the incrementally multiplied
970-byte state.  Require its selected coordinate to be the identity.  State
deduplication is by all 970 bytes.  Persist the state bytes, reduced word,
parent index, and generator index.  The empty generator roster is legal
exactly when the expected kernel order is one.

### Lemma 3 (BFS certificate)

If the queue exhausts with the frozen expected order, the persisted roster is
the deterministic ordered subgroup generated by the authenticated words;
each member has an independently replayable word witness.  The selected
cursor is valid only when its word, state, parent and generator agree with
this roster.

**Proof.** Induction on queue order proves every stored state is the replay of
its stored word and lies in the selected-coordinate kernel.  Conversely BFS
applies every ordered generator to every discovered state before exhaustion,
so the result is generator-closed and contains the generated subgroup.  The
reverse containment follows from the edge construction.  First discovery
under a fixed queue and generator order gives deterministic parents.  QED.

## 4. Checker grouping without changing the search

An independent checker may freeze the producer's chronological correction
records and then partition only their *local K0 reconstruction checks* by
coordinate.  Within a coordinate it retains original record order, builds
the coordinate table once, validates all local records, records the table
and result digests, and releases the table before the next coordinate.
Global chronological claims--basis insertion, dual epochs, correction
ordinals, coefficients, and first-success ownership--must still be checked
in the original receipt order.

### Lemma 4 (audit commutation)

This coordinate grouping preserves acceptance exactly when every grouped
predicate reads only the frozen task176 owners and the single correction
record, while all cross-record predicates remain on the original order.

**Proof.** Such local predicates have disjoint mutable scratch state and a
common immutable authority.  Their conjunction is invariant under
permutation.  The excluded chronological predicates are not commuted.  QED.

Consequently a one-entry `last coordinate` cache which rejects an `A,B,A`
record order is not a valid substitute.  The checker must either use Lemma 4
or retain a separately capped table per coordinate.  Every visited coordinate
has build count exactly one.

## 5. Exact memory ledger

The packed state-plus-slot payload is

```text
E3 coordinate: N*40  + C*4 =  75,563,776 bytes,
E4 coordinate: N*154 + C*4 = 243,105,472 bytes.
```

Thus ten simultaneously retained tables occupy

```text
5*75,563,776 + 5*243,105,472 = 1,593,346,240 bytes,
```

before Python/container overhead.  `243,105,472` is the E4 per-coordinate
maximum, not the payload of every coordinate; `10*243,105,472` is only a
conservative upper bound and must not be reported as measured allocation.
Under Lemma 4 the checker table peak is one coordinate, hence at most
`243,105,472` payload bytes, plus frozen authorities and bounded scratch.
The producer may retain all ten tables only if it declares and enforces the
exact simultaneous payload and releases them at the authenticated phase
boundary.

## 6. A0 consequence

Lemmas 1--4 close the selected-K0 subproblem required by v294: exact
full-state lookup, least `(qid,gid)`, word-bearing kernel enumeration, and an
independent bounded checker schedule.  They do not close the remaining A0
gates: the ordinary baseline, all physical mutation owners, acyclic P0/R/V
transport, complete checkpoint/process accounting, and a fresh Sol(max)
code/performance audit are still required.  Therefore A0 remains `0/1`.

