# Sol(max) reply 523 — lazy positive formula-seed selector v432 audit

## Verdict

`GO_WITH_REQUIRED_PAPER_REPAIR`.

The positive linear-algebra lemma is sound, and later unvisited seed formulae
and identity replays are not premises of a directly checked rank rise.  The
paper is not ready under its present quantitative/application wording,
however.  The live owner has **44 compact presentation seeds, not 6,441**.
Consequently the claimed 6,441-to-one reduction, the 6,440 later-seed count,
and the corresponding v220 line are false for this owner.  The exact live
reduction at a seed-1 hit is 44-to-one formula compilation, with the more
precise call counts in F5 below.  The artifact also does not identify which
seed budget check fired in round 73, so reordering alone cannot be said to
remove that exact historical time stop.

This is a required paper repair, not a refutation of the positive theorem.
No claim is promoted by this audit.

## Frozen subject and bounded method

The commissioned identities reproduced exactly:

```text
paper v432
  8204 965ab4f48fbc98cabd4905a7ad0a8fcb10dbe06415bb09771e22c31e74a7d3e5
live owner v3
  12215 0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37
pinned owner v2
  18191 cd27d69b06538e77dac1963d147f4966d8f63b9bf0d9e54860f2dae69149369b
checker v7
  3653 e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
```

I used static owner/checker tracing, independent parsing and hashing of the
authenticated artifact, the bounded v3 fixture, and the bounded v7 checker
self-test.  I did not run production, GHA, GAP, git, or an unbounded search,
and made no implementation change.

The two bounded advertised tests returned PASS:

```text
v3 fixture: synthetic_rises=3, state_computations=4
v7 self-test: frozen rank/count/round=68/25/27; five mutations rejected
```

## F1. Linear-algebra implication and exact positive boundary — PASS

Let the current physical span be (V\subseteq M), and let the current
separating functional satisfy

\[
 \lambda(v)=0\quad(v\in V).
\]

If a reconstructed physical row (r) has

\[
 \lambda(r)\ne0,
\]

then (r\notin V), since (r\in V) would force \(\lambda(r)=0\).  Hence the
echelon remainder of (r) is nonzero.  Adding one row therefore creates one
new pivot and raises rank by exactly one.  No assertion about any other seed
enters this implication.

For the live data structures, a selected correction must cross all of the
following gates before it is a sound literal row:

1. Freeze the present physical echelon and its normalized dual; no insertion
   may occur between dual construction and the selected-row pairing.  The
   dual must annihilate the present echelon span and have the advertised
   nonzero target/remainder pairing.
2. Authenticate the 44-word compact roster, the selected `seed_index`, and a
   legal literal `delta_word`; reconstruct
   `reduce(delta + relator + inverse(delta))` from those inputs.
3. Recompute the selected formula, including the external normalized-exponent
   constant `K`, from the current raw adjoint.  Reconstruct the candidate word
   and its complete coordinate tuple rather than trusting a producer scalar.
4. Reconstruct
   `row = aggregate(replay_atom(seed, delta, ...))` and independently form
   `fresh = aggregate(seed_v12(..., conjugate))`; require `row == fresh`.
   The conjugate must retain the registered joint-identity/literal contract.
5. Recompute the exact exponent pair, require divisibility by 18, reject every
   forbidden raw `E` key, and require the physical `N1,N2` values to agree
   with `(exp_x/18,exp_y/18) mod 3`.  The current `row == fresh` route implies
   the last equality through `seed_v12`, but an explicit successor check is a
   useful load-bearing mutation gate.
6. Require the re-evaluated formula scalar to lie in `{1,2}` and equal the
   direct physical pairing `pair(lambda,row)`.
7. Nonmutatingly reduce `row` against the exact current echelon, require a
   nonzero remainder and the predicted pivot, then require the actual add to
   return one rise, that pivot, and rank `old_rank+1`.
8. Record and later recheck the row digest, scalar, seed/delta, exact exponent
   pair, pivot, and pre/post dual and remainder digests.  Perform exactly one
   dual update after this insertion.

For the rank-rise implication itself, items 1, 4, 6, and the nonzero direct
pairing are the mathematical core.  The other gates establish that the row is
the commissioned literal correction and that its durable ancestry is exact.

## F2. `compile_formulas`, `weighted_hit`, insertion, replay, and checker — PASS with a roster correction

The live control flow is:

```text
action_support_hits
  -> tau_free_adjoint
  -> compile_formulas over P["pres"]["relators"]
  -> global coordinate/K gates
  -> weighted_hit in printed seed order
  -> insert one row
  -> exactly one update
```

`compile_formulas` constructs one `AllSevenModel`, then for each compact seed
calls `occurrence_data`, computes its normalized exponent constant, updates a
local coordinate union, and executes one un-conjugated `seed_v12`/`aggregate`
identity replay.  Only after the complete list returns does `weighted_hit`
start with seed 1.  `weighted_hit` visits merged `(coordinate,target)` keys in
sorted order and the nine kernel states in their existing order; for the
first nonzero formula value it rebuilds `delta`, the conjugate, `row`, and
`fresh`, checks direct equality, exponent divisibility, forbidden `E`, and the
direct dual pairing, then returns.  `insert` repeats the pre-state pairing,
requires the single pivot/rank rise, and records the pre/post state digests.

There is no hidden later-seed premise:

- `AllSevenModel.occurrence_data` allocates a local `merged` dictionary and
  does not mutate the physical echelon, the dual, or another seed formula.
- The `coords` union is local bookkeeping used by the old all-seed support
  gate and profile.  It is not used to construct a selected row.
- `seed_v12` and `aggregate` return rows without inserting them.
- The selective fibre oracle is constructed after the eager formula list in
  v3.  Its caches/kernel states are independent of later formula compilation.
- Physical state first changes in `insert`.

Thus an unvisited seed's formula, coordinate union contribution, and identity
replay are genuinely unnecessary for a positive selected row.  Deferring the
identity replay for the selected seed is also sound when the stronger selected
conjugate `row == fresh` and direct-pairing checks are retained.  Identity
checks for other seeds remain useful diagnostics/SELFTEST canaries, not
premises of this positive conclusion.

Checkpoint replay validates schema/binding, the canonical state seal, count,
and source shapes.  It reconstructs every accepted row, checks the recorded
pre-state, pairing, digest, pivot/rank, and post-state.  The checker-v7 chain
ultimately uses its separately written replay in checker v3: for every
correction it also recomputes the adjoint digest, conjugate exponent pair, and
literal `replay_atom` row before insertion.  It does not trust a serialized
producer row.  Formula/cursor provenance is not currently replayed by v7, so
the lazy successor checker must add its own typed selector checks; direct row
replay remains sufficient for the rank-rise fact.

## F3. Adversarial branch analysis — PASS for positive soundness, not old-search equivalence

### K=0 support fibres

For `K=0`, every nonzero value of

\[
 F_i=\sum_{(j,t)}c_{j,t}{\bf1}_{\pi_j=t}
\]

lies in the union of its listed singleton fibres.  On coordinates 0--2 the
live selective runtime independently exhausts and authenticates kernel order
9.  A canonical fibre representative plus all nine kernel states therefore
covers that fibre.  Empty fibres, duplicate points across targets, and an
identically zero/empty formula are harmless.  Exhausting a seed without a
hit permits advancing to the next seed in a positive search.

That advance is not a negative certificate if formula/identity canaries were
deferred.  The terminal after all skipped/no-hit seeds must remain
`UNKNOWN_RESOURCE`, never `NONMEMBER` or an exhaustion claim.

### Unsupported coordinates

An unsupported seed may be skipped only as a whole; a partial formula must
not be treated as exact.  Skipping it may miss a rise but cannot manufacture
one, because every returned row still crosses F1's direct gates.  This is a
sound **positive-search widening**, not equivalence to v3: v3 first unions all
44 coordinate sets and stops before `weighted_hit` if any seed uses an
unsupported coordinate, whereas the lazy route can accept an earlier fully
supported seed without inspecting that later obstruction.

### K nonzero

The v431 `W+1` theorem is mathematically reusable at a single-row fresh
anchor, but its rank99 batch implementation is not itself a callable proof of
the new owner.  The successor must port its exact hypotheses:

- all merged coordinates are in 0--2 and their independently authenticated
  kernel orders are nine;
- `W` is recomputed as the sum of kernel orders once per distinct merged
  `(coordinate,target)` key;
- cursors `0..W` are distinct elements of the authenticated
  `1,469,664 * 243` roster;
- the literal word and all ten coordinates are reconstructed directly;
- zero values are skipped, the first nonzero value crosses all F1 gates, and
  exactly that one row is inserted before refreshing the dual; and
- `W`, cursor/qid/gid, all coordinates, freshness, and the sole-row boundary
  are independently recomputed by the checker.

Under these hypotheses, at most `W` roster points lie in the formula support,
so one of `W+1` points is outside it and has value `K != 0`.  Action-first
order is unaffected because the lazy branch is reached only after the current
six-action search is empty.

### Failure typing

No inspected path can turn an incomplete search into a negative result.
There is nevertheless a wording error in v432: the live main maps a direct
invariant mismatch whose message lacks the `UNKNOWN_RESOURCE:` prefix to
plain `UNKNOWN`, not `UNKNOWN_RESOURCE`.  A forged formula nonzero with direct
pairing zero currently hard-stops rather than merely “wasting or missing” a
candidate.  The repaired contract should say:

```text
finite no-hit / unsupported skip / time / RSS / bounded truncation
    -> UNKNOWN_RESOURCE, all claims false
direct replay, literal, seal, or invariant mismatch
    -> fail-closed UNKNOWN/INPUT rejection, all claims false
```

Neither class may insert a row or issue `NONMEMBER`.

## F4. Independent artifact parse — PASS

The authenticated files parsed here were:

```text
result v10
  86354 39434b6a4c1a7851805c2deb3be8de4e7e919085a537b8d3913a15d341c19279
output checkpoint
  85934 69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93
```

Independent canonical JSON hashing reproduced the internal checkpoint state
seal

```text
3e0d4bc8e2f9a467a0e50ad8435a7360e1953c2baee369225d8aa6fd71379610
```

and the result/checkpoint accepted-source arrays agree exactly.  The parsed
facts are:

```text
accepted_count / array length: 68 / 68
accepted kinds:                correction=68
seed indices:                  seed 1=68
physical rank / round:         111 / 73
last thirteen rounds:          60..72
last thirteen ranks:           98->99 through 110->111
last thirteen seed indices:    all 1
last thirteen checked_fibres:  28,487,163,1,811,190,1,919,1,55,1108,1,109
observed min/max:               1 / 1108
terminal:                       UNKNOWN_RESOURCE
reason:                         UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit
elapsed_seconds:                7207.618058645
claims A0/COMMON/NONMEMBER/fake/Ihara: all false
```

All 68 rows have sequential one-rank transitions, distinct row digests, and
scalars in `{1,2}`.  The producer log records the thirteen new rises and then
the stated formula-seed gate; the checker log is the exact v7 PASS line.

## F5. Actual seed count and exact eager work avoided

The live bootstrap is unambiguous:

```text
P435.bootstrap:
  pres = base["compact"](...)
  require len(pres["relators"]) == 44
v3 compile_formulas:
  for word in P["pres"]["relators"]
v2/v1 source validation:
  1 <= seed_index <= 44
```

The independent actual-dual profile checker has the same `len == 44` gate.
The 6,441-word Task198 roof roster belongs to a different source universe and
is not the roster traversed by this A0 tau-free owner.

For each of the 68 observed seed-1 accepted rounds, v3 necessarily completed
all 44 eager seed entries before entering `weighted_hit`.  Relative to a
seed-at-a-time implementation:

- compiling only seed 1 avoids exactly **43 `occurrence_data` formula
  compilations** and 43 later-seed coordinate-union updates;
- if an identity canary is retained for the visited seed, it avoids exactly
  **43 unvisited identity `seed_v12`/`aggregate` replays**;
- under v432 Corollary 2.2, where even the selected seed's identity canary is
  replaced by the stronger selected-conjugate replay, it avoids **all 44
  un-conjugated identity replays**; the selected conjugate `replay_atom` and
  `fresh` checks remain and were already present in the eager route.

Across the 68 accepted rungs, those exact avoidable counts are 2,924 later
formula compilations and, under Corollary 2.2, 2,992 un-conjugated identity
replays.  This is a call-count statement, not a wall-clock factor.

The artifact phase label does not expose the formula index at which round 73
timed out.  It proves only that `compile_formulas` did not return and therefore
that no next `weighted_hit` candidate was tested.  Since the time budget was
already 7,207.6 seconds and the budget check is at the top of every seed
iteration, it may even have fired before seed 1.  The lazy successor removes
43 later formula compilations from the critical path **when a seed-1 hit is
reached**; it does not by reordering alone prove that the historical round-73
stop is eliminated or that the next dual has a seed-1 hit.

## F6. Required v432 paper repairs

Before implementation adoption, repair these statements:

1. Replace every live-owner `6,441`/`6,440` count by `44`/`43`, identify the
   roster as the compact Task411-style roster, and keep the 6,441 Task198
   roster explicitly out of this theorem's owner boundary.
2. Replace “reduces formula construction from 6,441 seeds to one” by the
   exact call counts in F5.  Do not claim an unmeasured wall-clock factor.
3. Replace “remove the exact round-73 pre-candidate stop” by: it removes
   later-seed eager work from the path to a seed-1 candidate; the artifact
   does not locate the formula cursor and gives no next-hit guarantee.
4. Replace the blanket “every unsuccessful route is UNKNOWN_RESOURCE” and
   “formula defect can at worst waste/miss” wording by the fail-closed split
   in F3.
5. State explicitly that unsupported-seed skipping is positive widening, not
   equivalence to the old all-seed gate, and that no no-hit/skip result is a
   negative certificate.
6. Restrict the v431 transfer to its coordinates-0--2/kernel-order/global-
   roster hypotheses and require a new single-row producer/checker port.
7. Clarify checkpoint “byte/semantic identity”: the legacy input file and its
   `accepted_sources` prefix are authenticated exactly and replay to the same
   rank/dual/remainder.  A versioned lazy successor necessarily has a new
   schema, binding, state seal, and output identity; its whole checkpoint
   cannot remain byte-identical.

## F7. Bounded Luna successor and mutation contract

A sufficient implementation boundary is:

1. Authenticate the exact rank111 legacy checkpoint/result identities above;
   validate v3 schema/binding/seal and replay all 68 sources to rank 111.
   Require the replayed current dual/remainder digests
   `56ccd1f3cc6b54fe340a69ce6a0ec99f5aeb3358ae80288c6b11c3f1ec664864`
   and
   `9eed8114d9e3172c7a11153d9c5cd6e5fc2e5184a8d6e3681cce5c82a83b4326`
   before a new insertion.
2. Pin the 44-word compact roster and v432's repaired paper plus the exact
   v431 mathematical dependencies.  Use a new schema/binding while preserving
   the accepted-source prefix exactly.
3. Per fresh round, keep six-action search first, compute one tau-free adjoint,
   and compile seeds 1..44 one at a time.  Gate coordinates per seed, not by a
   future all-seed union.  Execute the K=0 fibre or K-nonzero global branch in
   the exact existing within-seed order.
4. Return immediately only after all F1 direct checks; insert one row, perform
   one update, write one durable checkpoint, and restart at seed 1 under the
   new dual.  A complete/no-hit or bounded interruption remains claims-false.
5. Give the checker independent legacy migration, formula/K/W/cursor
   reconstruction, literal row replay, pivot/rank replay, and claim-boundary
   logic; it must not import a producer selector validator or trust a producer
   row/scalar.

The bounded tests must reject or distinguish at least:

1. roster count/digest mutations, including 43, 45, and a substituted 6,441
   roster;
2. a seed-1 hit instrumented to prove seed 2 is untouched, exactly one formula
   was compiled, no un-conjugated identity replay preceded promotion, and one
   add/update occurred;
3. K=0 empty, supported-zero, empty-fibre, duplicate-fibre, and full no-hit
   seeds advancing without a negative terminal;
4. an unsupported earlier seed followed by a supported hit, and an
   unsupported later seed left untouched by an earlier hit;
5. forged formula nonzero/direct-pair zero, `row != fresh`, conjugate drift,
   illegal delta, forbidden `E`, exponent/N drift, dependent row, pivot drift,
   and second insertion before dual refresh;
6. K-nonzero zero-before-hit, hit-at-W, all-zero-through-W invariant failure,
   W/cursor/qid/gid drift, duplicate global point, any of ten coordinate
   drifts, and a multirow/nonfresh global batch;
7. an available action hit causing zero formula compilations;
8. time/RSS before seed 1, mid-fibre, and mid-global scan producing only a
   durable claims-false resource result;
9. rank111 accepted-source, count, rank, round, binding, state-seal, pre/post
   digest, and pivot mutations; and
10. a coordinated producer row/scalar mutation rejected by independent
    checker reconstruction.

## Claim boundary

The repaired theorem is an execution optimization for a positive A0 search.
It does not change the v220 numerator:

```text
A0 actual COMMON:                         0/1
stable single-row prefix:                 68 rows / rank 111 / round 73
lazy positive selector mathematics:       sound after the listed paper repairs
compatible lift / fake / Ihara witness:   not claimed
```

`TASK523_R07_LAZY_POSITIVE_FORMULA_SEED_SELECTOR_V432_AUDIT_GO_WITH_REPAIR`
