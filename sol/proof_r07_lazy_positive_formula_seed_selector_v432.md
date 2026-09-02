# R07 lazy positive formula-seed selector (v432)

Author: Sol / 2026-09-02

Status: paper implementation theorem, pending independent audit.  This note
changes only the positive search order in the A0 tau-free single-row ladder.
It proves that the current eager construction of all 6,441 seed formulae is
not needed before accepting one literal rank rise.  It proves no current
COMMON word, A0 terminal, compatible lift, fake, or Ihara witness.
`verified=false`.

## 1. Frozen positive boundary

At a current physical span `V`, the adopted ladder computes a separating
dual `lambda` with

\[
 \lambda(V)=0.
 \tag{1.1}
\]

For printed relator seed `i` and literal conjugator `delta`, let
`r_i(delta)` be the exact physical column obtained by the frozen
`replay_atom` followed by `aggregate`.  The tau-free adjoint and Task179
occurrence compiler give a cheap candidate scalar

\[
 F_i(\delta)=K_i+
   \sum_{(j,t)\in R_i}c^{(i)}_{j,t}
       {\bf1}_{\pi_j(\delta)=t}.
 \tag{1.2}
\]

The existing selected-row route does not promote (1.2) by trust.  It
reconstructs the literal word, reconstructs `r_i(delta)`, checks the exact
exponent pair and forbidden-`E` condition, and requires

\[
 F_i(\delta)=\lambda(r_i(\delta))\ne0
 \tag{1.3}
\]

before insertion.  The independent checker reconstructs the same accepted
literal row rather than trusting a producer row.

### Lemma 1.1 (one checked hit is sufficient)

If one pair `(i,delta)` satisfies the direct checks (1.3), then
`r_i(delta)` is outside `V` and inserting it raises physical rank by one.
No formula belonging to a different seed has to be constructed or checked.

#### Proof

If `r_i(delta)` belonged to `V`, (1.1) would give
`lambda(r_i(delta))=0`, contrary to (1.3).  Hence its reduction modulo the
present echelon is nonzero and has a new pivot.  Formulae for other seeds do
not occur in this implication.  \(\square\)

This is only a positive lemma.  Failure to find such a pair under a finite
resource bound remains `UNKNOWN_RESOURCE` and is never a nonmembership or
exhaustion certificate.

## 2. Lazy seed theorem

The current v3 owner
`search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py` first executes
`compile_formulas`.  For each of all 6,441 presentation relators it performs
both `occurrence_data` and a full `seed_v12`/`aggregate` physical identity
replay.  Only after that complete list has been built does `weighted_hit`
try seed 1, seed 2, and so on.  Consequently a time stop inside
`tau_free_formula_seed` can occur before the first candidate of seed 1 is
tested.

### Theorem 2.1 (positive-only lazy seed compilation)

Replace that order by the following printed-order iterator.

1. Compute the tau-free raw adjoint once for the current `lambda`.
2. For `i=1,...,6441`, compile only (1.2) for seed `i`.
3. If all coordinates used by this seed are in the available selective
   runtime, enumerate its existing support-fibre candidates.  If `K_i != 0`,
   use instead the independently audited v431 global-prefix selector at a
   fresh anchor.
4. For the first proposed nonzero candidate, perform all direct literal and
   physical checks in (1.3).  Return it immediately if they pass.
5. Unsupported seeds and seeds without a positive hit may be skipped.  If
   time/RSS expires or the finite positive schedule ends without a hit,
   return only `UNKNOWN_RESOURCE`.

Every row returned by this lazy iterator is a sound literal rank rise for
the same current span.  It is not necessary to compute the union of
coordinates over later, unvisited seeds, or to execute an identity replay for
those seeds.

#### Proof

The iterator returns only through step 4.  At that point the selected word,
physical row, exact exponents, forbidden-key condition and direct pairing
have been reconstructed for the actual `(i,delta)`.  Lemma 1.1 proves the
rank rise.  A later seed cannot alter that word, row, pairing or present
span.  Therefore neither its coordinate set nor its physical identity is a
premise of the positive conclusion.

Skipping an unsupported seed may omit a possible rise, but cannot create a
false one.  Likewise, a defect in a cheap formula can at worst waste or miss
a candidate: the selected route still requires equality with the direct
physical pairing before promotion.  Since every unsuccessful or truncated
route is typed `UNKNOWN_RESOURCE`, no negative conclusion uses the incomplete
enumeration.  The v431 theorem supplies the corresponding direct checked
route when `K_i != 0`.  \(\square\)

### Corollary 2.2 (defer eager identity replay)

The eager call

```text
fresh = aggregate(seed_v12(..., seedword_i))
require formula_at_identity == pair(lambda, fresh)
```

need not run for every seed before search.  For a selected conjugate the
stronger load-bearing check is already

```text
row = aggregate(replay_atom(i, delta, ...))
fresh = aggregate(seed_v12(..., conjugate(delta, seedword_i)))
require row == fresh
require formula_scalar == pair(lambda, row) != 0
```

and the checker repeats the selected-row reconstruction independently.
Identity checks for unselected seeds provide diagnostics, not a premise of a
positive result.  They may remain in SELFTEST or a bounded audit sample but
must not precede every production hit.

## 3. Exact continuation and checkpoint contract

The lazy successor must preserve:

- action rows before correction rows;
- printed seed order and the current within-seed target/kernel order;
- one physical insertion followed by exactly one dual update;
- the accepted-source literal word, seed index, scalar, exponent pair,
  row/pivot and pre/post dual/remainder digests;
- the rank-111 checkpoint replay and binding until the first new accepted
  row;
- the 4.8-GB cap, bounded time, bounded new rises and positive-only terminal;
  and
- independent replay before any `COMMON_CANDIDATE` is promoted.

It may cache the Task179 model, the current raw adjoint, and the selective
runtime exactly as the present owner does.  It must not cache a producer row
as checker evidence.  A checkpoint written after a rise contains the same
semantic accepted-source record as the eager owner; only the implementation
version/binding and output identity change.

The required adversarial tests are:

1. a seed-1 direct hit returns without touching seed 2;
2. a supported zero seed advances to the next seed;
3. an unsupported seed is skipped and cannot yield a terminal claim;
4. a forged formula nonzero with direct pairing zero is rejected;
5. a direct row or conjugate drift is rejected;
6. time/RSS before a hit yields only `UNKNOWN_RESOURCE`; and
7. replay of the promoted rank-111 checkpoint is byte/semantic identical
   before the first new insertion.

## 4. Why this matters on the actual lane

Authenticated artifact `9826862037` from run `33564845217`, job
`100045550767`, contains 68 accepted correction rows through physical rank
111.  All 68 have `seed_index=1`; the last thirteen rises likewise use seed
1, with `checked_fibres` between 1 and 1,108.  The run then stopped at round
73 inside `UNKNOWN_RESOURCE:tau_free_formula_seed:time_limit`, before testing
the next weighted candidate.

Thus, on every already observed accepted rung, eager compilation performed
up to 6,440 irrelevant later-seed constructions and physical identity
replays before using seed 1.  Theorem 2.1 reduces that formula-construction
part from 6,441 seeds to one whenever the observed seed-1 pattern continues.
It gives no universal wall-clock factor because selective-runtime and
candidate-fibre work remain, and the next dual is not assumed to have a
seed-1 hit.  It does, however, remove the exact round-73 pre-candidate stop:
the successor tests seed 1 before spending resources on seeds 2--6,441.

## 5. v220 consequence

This theorem advances A0 execution design, not its milestone numerator:

```text
A0 actual COMMON:                         still 0/1
stable single-row prefix:                 68 rows / rank 111 / round 73
eager all-6441 formula prepass:            mathematically unnecessary
lazy selected-row direct certification:   paper-closed, audit pending
compatible lift / fake / Ihara:            not claimed
```

`R07_LAZY_POSITIVE_FORMULA_SEED_SELECTOR_V432_PAPER_CANDIDATE`
