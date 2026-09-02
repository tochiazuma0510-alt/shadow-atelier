# R07 lazy positive compact-seed selector (v433)

Author: Sol / 2026-09-02

Status: corrected paper implementation theorem.  This version supersedes
v432's quantitative/application wording after independent Task523 audit.  The
live A0 tau-free owner has 44 compact seeds, not the 6,441 Task198 roof rows.
The positive linear-algebra theorem is unchanged.  This note proves no current
COMMON word, A0 terminal, compatible lift, fake, or Ihara witness.
`verified=false`.

## 1. Exact owner boundary

The live producer
`search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py` receives
`P["pres"]["relators"]` from the compact bootstrap, which requires exactly
44 relators.  Seed validation likewise requires

```text
1 <= seed_index <= 44.
```

The separate Task198 complete roof interface has 6,441 rows.  It is not the
formula roster traversed by this producer and no 6,441 count is used below.

At a current physical span `V`, the producer computes a separating dual
`lambda` with

\[
 \lambda(V)=0.
 \tag{1.1}
\]

For compact seed `i` and literal conjugator `delta`, let `r_i(delta)` be the
exact physical column returned by the frozen `replay_atom` and `aggregate`.
The tau-free adjoint and Task179 occurrence compiler provide the candidate
formula

\[
 F_i(\delta)=K_i+
   \sum_{(j,t)\in R_i}c^{(i)}_{j,t}
       {\bf1}_{\pi_j(\delta)=t}.
 \tag{1.2}
\]

Equal `(j,t)` entries are merged and zero coefficients deleted.  A selected
row is not accepted from (1.2) alone.  Its literal word and all coordinates
are reconstructed, and the producer requires

\[
 r_i(\delta)=r_i^{\rm fresh}(\delta),\qquad
 F_i(\delta)=\lambda(r_i(\delta))\ne0.
 \tag{1.3}
\]

It also checks the exact exponent pair, divisibility by 18, forbidden-`E`
condition, row digest, nonzero echelon remainder and predicted pivot.  The
checker independently replays every accepted literal row.

### Lemma 1.1 (one directly checked hit is sufficient)

If one `(i,delta)` satisfies (1.3) against the unchanged current span, then
`r_i(delta)` is outside `V` and its insertion raises physical rank by one.
No other compact seed formula is a premise.

#### Proof

Membership `r_i(delta) in V` would imply
`lambda(r_i(delta))=0` by (1.1), contradicting (1.3).  Hence its reduction
against the current echelon is nonzero and supplies a new pivot.  Formulae
for all other seeds are irrelevant to this implication.  \(\square\)

This is positive-only.  A truncated/no-hit schedule is not a nonmembership or
exhaustion certificate.

## 2. Lazy compact-seed theorem

The current eager order constructs formulae for all 44 compact seeds.  For
each seed it calls `occurrence_data`, updates a coordinate union, and performs
one un-conjugated `seed_v12`/`aggregate` identity replay.  Only after all 44
entries return does `weighted_hit` try seed 1.

### Theorem 2.1 (positive-only lazy compilation)

The eager prepass may be replaced by this printed-order iterator.

1. Keep the six-action search first.  If it has no hit, compute one tau-free
   raw adjoint for the current `lambda`.
2. For `i=1,...,44`, compile only formula (1.2) for seed `i`.
3. Gate this seed's complete coordinate set.  A seed using an unavailable
   coordinate is skipped as a whole; no partial formula is used.
4. If `K_i=0`, enumerate its complete authenticated support fibres in the
   existing `(coordinate,target,kernel)` order.  If `K_i!=0`, use the global
   selector of Section 3.
5. For a proposed nonzero value, execute every direct gate in (1.3), the
   literal/exponent/forbidden-key gates, and nonmutating echelon reduction.
   Return immediately only after these pass.
6. Insert exactly that one row, update the dual exactly once, durably
   checkpoint, and restart at seed 1 under the new dual.

Every returned row is a sound literal rank rise.  Later unvisited seed
formulae, their coordinate-union contributions, and their identity replays
are unnecessary for that positive conclusion.

#### Proof

Only step 6 mutates the physical span.  All formula dictionaries and the
all-seed coordinate union in the eager owner are local search bookkeeping;
`seed_v12`/`aggregate` do not insert rows.  At step 5 the selected conjugate
is directly reconstructed and its actual physical pairing is checked.
Lemma 1.1 therefore applies before any later seed can matter.  Skipping a
seed may omit a possible row but cannot create a false row, and no incomplete
route is promoted as negative.  \(\square\)

This is a sound positive-search widening, not equivalence to the old global
coordinate gate.  The eager owner stops before any hit if any of the 44 seeds
uses an unsupported coordinate.  The lazy iterator may soundly accept an
earlier fully supported seed without examining that later obstruction.

### Corollary 2.2 (deferred identity canary)

The un-conjugated identity replay for every formula is diagnostic rather than
a premise of a selected rank rise.  It can be omitted from the production
critical path provided the selected route retains the stronger gates

```text
row = aggregate(replay_atom(i, delta, ...))
fresh = aggregate(seed_v12(..., conjugate(delta, seedword_i)))
require row == fresh
require formula_scalar == pair(lambda, row) in {1,2}
```

and the independent checker repeats the selected-row reconstruction.
Bounded identity canaries may remain in SELFTEST.

## 3. Exact K branches

For `K_i=0`, every nonzero value of (1.2) lies in the union of its listed
fibres.  On live coordinates 0--2, canonical representatives and the
independently authenticated kernel order nine exhaust each fibre.  A seed
with empty fibres or no nonzero value may be passed without a negative claim.

For `K_i!=0`, the v431 `W+1` argument transfers only under all of these
hypotheses:

- every merged coordinate is in 0--2 and has authenticated kernel order 9;
- `W` is recomputed as the sum of those kernel orders once per distinct
  merged `(coordinate,target)`;
- cursors `0,...,W` are distinct points of the authenticated
  `1,469,664 * 243` global roster;
- the literal word and all ten coordinates are reconstructed directly; and
- the first nonzero result crosses all Section 1 direct gates at a fresh
  single-row anchor and is followed immediately by the one dual refresh.

At most `W` roster points lie in the support union, so one of the `W+1`
points is outside it and has value `K_i!=0`.  A new single-row producer and
checker must port these hypotheses; the rank99 batch implementation is not
silently reused as code.

## 4. Failure and checkpoint typing

The successor has two distinct fail-closed classes:

```text
finite no-hit / unsupported skip / time / RSS / bounded truncation
    -> UNKNOWN_RESOURCE, all claims false

direct replay / literal / seal / formula-physical invariant mismatch
    -> UNKNOWN or input rejection, all claims false
```

A forged formula nonzero whose direct pairing is zero is an invariant
failure, not merely wasted work.  Neither class inserts a row or issues
`NONMEMBER`.

The legacy rank111 input checkpoint is authenticated byte-for-byte and its 68
accepted sources replay to the same rank, dual and remainder.  A versioned
lazy successor necessarily has a new schema, binding, state seal and output
identity; only the legacy accepted-source prefix and its replayed semantics
remain exact.  Each new accepted record retains seed/delta, scalar, exact
exponents, row/pivot and pre/post dual/remainder digests.

The independent checker must add typed lazy-selector provenance checks for
formula/K/W/cursor decisions and must not import a producer selector
validator.  Its existing direct literal-row replay remains the rank-rise
authority.

## 5. Exact evidence and honest cost statement

Authenticated artifact `9826862037` from run `33564845217`, job
`100045550767`, contains:

```text
accepted correction rows:                 68
seed indices:                              seed 1 = 68
physical rank / round:                     111 / 73
last thirteen checked_fibres min/max:      1 / 1108
terminal:                                  UNKNOWN_RESOURCE
reason: UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit
A0/COMMON/NONMEMBER/fake/Ihara claims:     all false
```

For each observed seed-1 accepted round, the eager owner completed all 44
formula entries before the hit.  Relative to lazy seed-1 selection this
avoids exactly 43 later `occurrence_data` calls and 43 later coordinate-union
updates.  If Corollary 2.2 is used, it also avoids all 44 un-conjugated
identity replays while retaining the selected conjugate replay.  Across the
68 recorded rungs, the exact avoidable totals are 2,924 later formula
compilations and 2,992 un-conjugated identity replays.

These are call counts, not a measured wall-clock factor.  The artifact does
not record which formula-index budget check fired at round 73, and it does not
prove that the next dual has a seed-1 hit.  The theorem therefore claims only
that later-seed eager work is removed from the path to any earlier hit; it
does not claim that reordering alone eliminates the historical round-73 stop.

## 6. Bounded successor contract

A Luna implementation must at least test/reject:

1. compact-roster count/digest mutations, including 43, 45 and substituted
   6,441-row input;
2. seed-1 hit with seed 2 untouched, one formula compiled, no eager identity
   replay, exactly one insertion and one update;
3. supported-zero, empty, duplicate-fibre, unsupported and full no-hit seeds
   without a negative terminal;
4. forged formula/direct-pair mismatch, `row != fresh`, conjugate/exponent/N
   drift, forbidden `E`, dependent row, pivot drift and a second insertion
   before dual refresh;
5. K-nonzero zero-before-hit, hit-at-W, all-zero invariant failure,
   W/cursor/qid/gid/ten-coordinate drift, duplicate global point and
   nonfresh/multirow use;
6. an action hit causing zero formula compilation;
7. time/RSS before seed 1 and mid-scan producing only a durable claims-false
   resource terminal; and
8. every legacy rank111 prefix/seal/digest mutation plus a coordinated
   producer row/scalar mutation rejected by independent reconstruction.

## 7. v220 consequence

```text
A0 actual COMMON:                         still 0/1
stable single-row prefix:                 68 rows / rank 111 / round 73
lazy 44-seed positive selector:            paper-corrected, audit required
measured wall-clock speedup:               not claimed
compatible lift / fake / Ihara:            not claimed
```

`R07_LAZY_POSITIVE_COMPACT_SEED_SELECTOR_V433_PAPER_CANDIDATE`
