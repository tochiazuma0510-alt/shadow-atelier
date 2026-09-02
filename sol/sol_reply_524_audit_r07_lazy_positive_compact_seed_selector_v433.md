# Sol(max) reply 524 — final audit of lazy compact-seed theorem v433

## Verdict

`GO_FOR_LUNA_LAZY_SUCCESSOR_IMPLEMENTATION`.

Version v433 satisfies every required Task523 F6 repair.  Its one-hit
linear-algebra lemma, lazy positive iterator, deferred identity canary,
K=0 fibre argument, restricted v431 K-nonzero transfer, failure typing, and
legacy-prefix boundary are sound against the frozen v3 producer/checker-v7
call graph.  I found no new mathematical overstatement requiring another
paper revision.

This verdict authorizes a bounded Luna successor implementation and its
independent checker.  It does not adopt an implementation, promote A0, or
assert a COMMON word, compatible lift, fake, or Ihara witness.

## Exact audited identities and bounded method

The commissioned identities reproduced exactly:

```text
v433 paper
  10495 3a8b5085e3a0a712dfd32c246cf472ca16616a2e3d7af494e4fcc8b30d02d940
Task523 audit
  18807 629d95528773e741c6531405f0c19d0dc2af45efcaa2cfabd2c91261521d17de
live v3 producer
  12215 0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37
pinned v2 owner
  18191 cd27d69b06538e77dac1963d147f4966d8f63b9bf0d9e54860f2dae69149369b
checker v7
  3653 e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
```

I mechanically mapped the seven F6 corrections to v433, retraced the live
call graph, reran only the bounded v3 fixture and v7 checker self-test, and
reparsed the authenticated rank111 result.  The bounded gates returned:

```text
v3 fixture: PASS; synthetic_rises=3; state_computations=4
v7 self-test: PASS; frozen rank/count/round=68/25/27;
              checkpoint seal, altered prefix, and three monotonicity
              mutations rejected
artifact parse: accepted=68; correction=68; seed1=68; rank/round=111/73;
                terminal tau_free_formula_seed:time_limit; all five claims false
```

No production, GHA, GAP, git/release mutation, implementation edit, or claim
promotion was performed.

## F1. Task523 F6 repair matrix — all PASS

### 1. Exact compact-owner universe — PASS

V433 explicitly fixes the owner universe at 44 compact relators, cites the
live `P["pres"]["relators"]` and `1 <= seed_index <= 44` gates, and states
that the separate 6,441-row Task198 roof interface is not traversed by this
producer.  No live-owner 6,441/6,440 cost claim remains.

This matches the pinned bootstrap, which constructs `pres` through the
compact authority and hard-requires `len(pres["relators"]) == 44`, and the
v1/v2 source validators, which reject correction seeds outside 1..44.

### 2. Exact call counts without a time-factor claim — PASS

V433 states exactly what the eager call graph does before a seed-1 hit:

```text
44 occurrence_data calls
44 coordinate-union updates
44 un-conjugated identity seed_v12/aggregate replays
```

The lazy seed-1 path keeps one formula compilation, so it avoids 43 later
`occurrence_data` calls and 43 later union updates.  With Corollary 2.2 it
also omits all 44 un-conjugated identity canaries while retaining the selected
conjugate `replay_atom`/`fresh` comparison.  Multiplying by the 68 observed
seed-1 rises gives 2,924 and 2,992 respectively.  The paper correctly labels
these as call counts and expressly declines a measured wall-clock factor.

### 3. Round 73 and future-hit boundary — PASS

V433 now states only that the coarse artifact phase proves no next
`weighted_hit` candidate was reached.  It does not infer which of the 44
formula budget checks fired, does not claim that reordering removes the
historical stop, and does not assume the next dual has a seed-1 hit.  The
theorem's benefit is correctly restricted to removing later-seed eager work
from the path to an earlier hit.

### 4. Failure typing — PASS

The corrected split is exact:

```text
finite no-hit / skipped unsupported work / resource truncation
    -> UNKNOWN_RESOURCE, all claims false
literal, replay, seal, or formula-physical invariant failure
    -> fail-closed UNKNOWN or input rejection, all claims false
```

This matches v3 `main`, which maps only `UNKNOWN_RESOURCE:`-prefixed errors to
the resource status and maps other exceptions to plain `UNKNOWN`, always with
A0/COMMON/NONMEMBER/fake/Ihara false.  A forged formula/direct-pair mismatch
is correctly described as an invariant failure, not as harmless wasted work.

The sentence that neither failure class “inserts a row” is sound at the
failed attempt: no unchecked row may be inserted.  It must not be read as
discarding previously certified rises in the same invocation.  V433 Section
2 already requires each successful rise to be durably checkpointed before
restart, and the rank111 artifact itself demonstrates certified rises
followed later by a resource terminal.  Luna and its checker must preserve
those earlier rows.

### 5. Unsupported-seed positive widening — PASS

V433 requires an unsupported seed to be skipped as a whole and forbids use of
a partial formula.  It explicitly calls the behavior a sound positive-search
widening, not equivalence to the eager global coordinate gate.  It also says
that truncation, skip, empty fibre, and no-hit schedules are not nonmembership
or exhaustion evidence.

The distinction is load-bearing and correct: the eager v3 owner unions all
seed coordinates and stops before `weighted_hit` if any later seed is
unsupported, whereas a directly checked earlier row is independent of that
later seed.  Skipping may lose completeness but cannot create a false
positive because the selected row still crosses the direct physical gates.

### 6. Restricted v431 transfer — PASS

V433 supplies every hypothesis needed for the single-row transfer:

- all merged coordinates are in 0..2;
- each live coordinate kernel order is independently authenticated as nine;
- `W` is recomputed once per distinct merged `(coordinate,target)`;
- cursors `0..W` are distinct points of the authenticated
  `1,469,664 * 243` roster;
- the literal word and all ten coordinates are reconstructed directly;
- zero values precede the first nonzero without insertion;
- the nonzero row crosses the Section 1 literal, physical, and rank gates at
  a fresh anchor; and
- exactly one insertion is followed immediately by one dual refresh.

These hypotheses imply `W` is below the roster size, because `0..W` must be a
set of distinct roster points; the implementation should retain the explicit
runtime inequality guard from v431.  At most `W` roster points lie in the
support union, so one of the `W+1` points has all indicators zero and value
`K != 0`.  V433 also correctly requires a new single-row producer/checker
port rather than treating the rank99 batch implementation as a callable
replacement.

### 7. Legacy exactness versus new successor identity — PASS

The paper now separates two notions correctly:

- the legacy input bytes, v3 schema/binding/seal, 68 accepted-source prefix,
  and replayed rank/dual/remainder are authenticated exactly; but
- the versioned lazy successor has a new schema, binding, state seal, and
  output identity.

Thus no impossible whole-checkpoint byte identity is required after
migration.  The successor must preserve the accepted-source prefix and its
semantics exactly while binding every new row to its new versioned state.

## F2. Lemma 1.1 and the lazy iterator — PASS

At a fixed current echelon span `V`, the physical dual returned by the
echelon construction annihilates `V`.  If the directly reconstructed row
has `pair(lambda,row)` in `{1,2}`, membership in `V` is impossible.  Its
remainder is nonzero, so adding one row contributes one pivot and raises rank
by one.  Other seed formulae cannot affect this implication.

The v3 call graph supports the noninterference statement:

- six-action search occurs before tau-free formula work;
- `compile_formulas` creates local formula/coordinate data;
- `AllSevenModel.occurrence_data`, `seed_v12`, and `aggregate` do not mutate
  the physical echelon or dual;
- the selective oracle's canonical/kernel caches do not compile later seed
  formulae; and
- physical state first changes in `insert`, which rechecks the pre-state
  pairing, requires one returned pivot and `old_rank+1`, then performs one
  update.

V433 strengthens the successor boundary by requiring nonmutating reduction
and a predicted pivot before the actual add.  Current v3 obtains and checks
the actual nonzero pivot from `phys.add`, while checker replay binds that
pivot later; requiring a pre-insertion prediction in the successor is a
sound strengthening, not a claim that the old producer already had a
separate pre-reduction helper.

## F3. Deferred identity canary — PASS

For a positive row, the eager identity check for an unselected seed is not a
premise.  The selected path reconstructs the conjugate in two ways,

```text
aggregate(replay_atom(seed,delta))
aggregate(seed_v12(conjugate(delta,seedword)))
```

requires equality, and requires its formula scalar to equal the direct
nonzero dual pairing.  This is stronger at the selected point than the
un-conjugated identity canary.  A faulty cheap formula may miss a row or
trigger a fail-closed direct mismatch, but cannot promote a row whose direct
pairing is zero.  Retaining bounded identity canaries only in SELFTEST is
therefore sound for this positive-only theorem.

Checker v7 already independently reconstructs each accepted `replay_atom`
row, adjoint digest, exponent pair, pairing, pivot/rank, and post-state.  It
does not yet replay lazy formula/K/W/cursor provenance; v433 correctly makes
that new independent checker work mandatory rather than attributing it to
v7.

## F4. K=0 fibre argument — PASS

For `K=0`, a nonzero formula value can occur only in the union of the merged
singleton fibres.  The live selective runtime constructs a canonical
representative and independently exhausts the nine-element kernel for each
coordinate 0..2, so representative times all nine kernel states covers the
entire fibre.  Empty fibres and overlaps only reduce work; duplicates do not
invalidate coverage.  If every visited point evaluates to zero, advancing to
the next seed is safe for positive discovery.  Because deferred canaries and
unsupported seeds remove any negative completeness claim, ending with no
directly checked hit remains only `UNKNOWN_RESOURCE`.

## F5. Mutation contract — sound and sufficient for commissioning

V433 Section 6 retains all load-bearing mutation classes from Task523:

1. exact compact-roster authority and 43/45/6,441 substitutions;
2. seed-1 early return, seed-2 non-touching, one formula, no eager identity,
   one insert/update;
3. K=0 empty/zero/duplicate/unsupported/no-hit behavior;
4. formula/direct, row/fresh, literal/exponent/N/E, dependence, pivot, and
   stale-dual second-insertion failures;
5. K-nonzero zero-before-hit/hit-at-W/invariant/W/cursor/qid/gid/all-ten-
   coordinate/distinctness/freshness failures;
6. action-first short circuit;
7. durable claims-false resource stops; and
8. legacy state plus coordinated producer row/scalar mutations rejected by
   independent reconstruction.

For implementation audit, two compressed phrases must be instantiated as
separate live tests rather than boolean assertions:

- “unsupported” means both an unsupported earlier seed followed by a later
  supported hit, and an earlier supported hit proving a later unsupported
  seed was untouched; and
- “mid-scan” means one interruption in the K=0 fibre schedule and one in the
  K-nonzero global `0..W` schedule.

Likewise, the legacy mutation family must individually cover accepted-source,
count, rank, round, binding, state seal, pivot, and pre/post digest changes.
These are direct unpackings of v433's stated contract and Task523 F7, not
additional mathematical hypotheses or a paper repair.

## Implementation boundary

Luna may now implement a versioned lazy successor, subject to the following
nonnegotiable boundary:

1. independently authenticate and replay the exact rank111 legacy input;
2. pin the 44-word compact roster, v433, and exact v431 dependencies in both
   producer and checker bindings;
3. preserve action-first order and compile seeds 1..44 one at a time;
4. keep K=0 support and K-nonzero global cursors disjoint and independently
   reconstructible;
5. accept only after literal/fresh/direct-pair/nonzero-remainder/pivot checks;
6. insert one row, update once, checkpoint, and restart from seed 1;
7. retain every earlier certified rise across a later claims-false resource
   terminal; and
8. let the checker reconstruct selector provenance and physical rows without
   importing a producer validation helper.

Fixtures, counters, and static marker booleans alone are not sufficient for
the load-bearing mutation cases.  The implementation remains candidate until
the independent checker and transport boundary are separately audited.

## Claim boundary

V433 closes the paper repair milestone only:

```text
A0 actual COMMON:                         0/1
stable single-row prefix:                 68 rows / rank 111 / round 73
lazy 44-seed theorem:                     paper-closed for implementation
implemented/cross-checked successor:      not yet
compatible lift / fake / Ihara witness:   not claimed
```

`TASK524_R07_LAZY_POSITIVE_COMPACT_SEED_SELECTOR_V433_FINAL_AUDIT_GO`
