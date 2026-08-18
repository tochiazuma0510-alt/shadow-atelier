# Luna reply 157dl — B345 relative Frattini-3 sparse Fox lane

Date: 2026-08-18

## Verdict

The requested versioned producer, independent checker, and same-job GAP
driver are implemented.  The bundle is a positive semidecision for the
relative elementary-abelian 3-chief step immediately below the frozen,
cross-checked q=3 stage.  It does not claim a finite obstruction from a
bounded miss and does not claim final B4-B.

## Frozen inputs

Both Python programs and the driver bind the following successful 157da
inputs exactly:

```text
q3 producer  b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
q3 checker   ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
q3 driver    c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
formula      b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef
q3 artifact  3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
```

The driver first regenerates the q3 artifact with the pinned q3 driver in
the same GAP job, requires its checker sentinel and exactly one PASS marker,
then checks the exact artifact SHA before invoking the new producer.
Stale artifacts, logs, and sentinels are removed first.  The new producer
and checker use only the fixed `ci/out` paths.

## Exact construction

The producer independently reconstructs the PB3/PB4/PB5 presentations
with 2/11/35 relators and the five PB3-to-PB4 cofaces.  At PB4 it constructs
the sparse left-Fox complex

```text
F3[E4]^11 --D2--> F3[E4]^6 --D1--> F3[E4]
```

using the frozen convention `d(uv)=d(u)+u*d(v)`, and gates `D1*D2=0`
literally.  It never constructs a full regular matrix, a full H1 basis,
a Reidemeister-Schreier presentation, a relative ANUPQ quotient, or
`Elements(H)`.

Every positive `Phi_3(H4)` membership stores a lossless ledger

```text
(PB4 relator index, exact E4 translation element, F3 coefficient)
```

whose translated Fox columns sum exactly to the target gradient.  Quotient
elements used in supports are accompanied by section words.  The checker
imports no producer helper: it reconstructs the presentations, quotient
arithmetic, Fox derivatives, translated columns, element sections, and each
ledger sum independently.

The candidate order begins with the frozen outside word

```text
[-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]
```

and the empty correction.  If needed, it then uses a deterministic bounded
BFS dictionary of at most 4096 explicit coarse-`J_H` commutator words derived from the
authenticated 27-word q3 correction fibre.  The complete registered order
and seed words are written into the receipt.

The load-bearing typed gates are as follows.

- `J_H=ker(PB3 -> E3)` is the authenticated coarse source correction
  kernel.  Every selected correction is additionally replayed through all
  five cofaces and required to land in `H4` (identity in `E4`).
- `J_Phi=intersection_j coface_j^-1(Phi_3(H4))` is the finer source
  kernel.  A correction is deliberately **not** required to lie in
  `J_Phi`: its class in `J_H/J_Phi` is precisely the lift freedom being
  searched.  Thus no Fox boundary ledger is requested for the correction
  alone.
- Both source hexagon residuals are sent through all five cofaces, yielding
  ten independent PB4 boundary certificates.
- The ordered A.18 pentagon is certified directly as a PB4 residual.
- Charming is not inferred from raw exponent sums or the ambient q3 stage.
  The receipt gives an explicit commutator-product representative `g`,
  checks the literal equality, and certifies all five cofaces of `f*g^-1`.
- Onto is certified by a two-sided inverse on all six marked PB4 generators.
  PB4 relations for both maps and all twelve `ST`/`TS` generator residuals
  receive exact sparse boundary ledgers.

The cheap coarse-`J_H` coface gates for each correction, charming, both hexagons,
pentagon, and the source endomorphism relations run before inverse selection.
These gates evaluate directly in `E4`
without first materializing the substituted free words; full literal words
are built only for cheap survivors, with a direct-value/full-word drift
canary.  Failed candidates return immediately.

Raw `S^(ord-1)` word powering is not used.  The producer reconstructs the
pinned normalized exponent-7 roof row and all 27 authenticated q3 fibre
corrections, tests all 27 against the fixed exponent-2 six-image E4 tuple,
and retains the deterministic first two-sided inverse together with the
full passing-index set.  A candidate reuses this short tuple only when its
own ordered six E4 images equal the fixed tuple; a different tuple is a
candidate-local `missing_bounded_inverse_representative` resource skip, not
a mathematical rejection.  Every matching candidate still receives its
own S/T relations, ST/TS residuals, Fox gradients, and ledgers.  One shared incremental translated-relator
basis is reused for every candidate.  The empty correction remains first;
from translation checkpoint 8 onward, all precomputed cheap survivors are
retried in registered order at geometric checkpoints
`8,16,32,...,32768`, rather than waiting behind an empty-only 32768 pass.

## Terminals and claim boundary

The producer emits exactly one registered terminal.  A
`B345_RELFRAT3_LITERAL_PAIR_PASS` plus independent checker PASS proves that
one literal charming/onto outside pair survives every isolated elementary-
F3 next-chief refinement `L` with

```text
Phi_3(H4) <= L <= H4.
```

No isolation of `Phi_3(H4)` is assumed.  Nonabelian factors, other primes,
deeper iteration, a uniform cofinal tower, and final B4-B remain outside
this receipt.

If the registered translated-column and correction caps are exhausted with
no candidate-local resource skip, the
result is `B345_RELFRAT3_SEARCH_INCOMPLETE`; it is not promoted to a finite
obstruction.  Any nonempty candidate that hits a word, inverse, gradient,
or sparse-elimination cap is recorded losslessly by candidate index, phase,
and reason; if no positive remains, those skips force
`B345_RELFRAT3_UNKNOWN_RESOURCE` and are never counted as false candidates.
Every global resource cap has the same non-obstruction terminal.  This
version does not build the PB5
fallback after an incomplete direct sparse search, because that miss does
not prove absence of a PB3/PB4 pair; the receipt records
`PB5_branch_constructed=false` explicitly.
The unsupported `B345_RELFRAT3_MISSING_MATCHED_CHAIN` and
`B345_RELFRAT3_PROJECTED_OBSTRUCTION` mutations are not registered
terminals and are rejected fail-closed.  In particular, a producer boolean
cannot stand in for an independently implemented projected-obstruction
branch in this v1.

## Performance contract

The implemented hard caps are the requested 64-dimensional small
projection, 4096 corrections, 32768 translations per relator, 1,000,000
live sparse entries, and 100,000 letters per word/section.  Runtime phase
markers, basis support sizes, pivot/ledger maxima, candidate membership
tests, cheap-survivor indices, geometric checkpoints, cache size,
candidate-local resource records, and the exact bounded-search policy are
included in the receipt.  The implementation makes zero relative ANUPQ,
RS, full-Elements, or full-regular-matrix calls.

## Independent checks performed

The one permitted lightweight combined self-test was run without building
the production quotient:

```text
python -B search/d972_b345_relfrat3_v1.py --self-test
D972_B345_RELFRAT3_PRODUCER_SELFTEST_PASS relevant_formula_sha256=5b66299d255964ff8afa9e9d75e9a5d61d767fd76539fd3c6ae94acd65039127 normalized_inverse_cache_hit_canaries=1

python -B search/check_d972_b345_relfrat3_v1.py --self-test
D972_B345_RELFRAT3_CHECKER_SELFTEST_PASS mutations=4 fox_orientation_canaries=2
```

After that authorized run, preflight found and corrected the load-bearing
source-kernel typing: corrections range over coarse `J_H/J_Phi` classes and
are no longer incorrectly forced into `J_Phi`.  The corresponding producer
targets, checker reconstruction, receipt vocabulary, geometric shared-basis
schedule, finite normalized inverse fibre, candidate-local tuple/resource
accounting, unsupported-terminal rejection, and final SHA chain were
statically audited.  The one 157dm lightweight combined selftest above was
run after the normalized-inverse edits.  The subsequent removal of the
unsupported projected terminal and addition of its fifth mutation canary
were statically audited without a second execution.  No local GAP, Git, or
GHA command was run.

## Final files and SHA-256

```text
search/d972_b345_relfrat3_v1.py
  77505 bytes
  4b73fbfe19bb33a9decdec5fda437f58f61a3ecb1989090bd08151f60ce6609e

search/check_d972_b345_relfrat3_v1.py
  52315 bytes
  3d86240237229b250943c4795c24c32ac75af9229534c73d16bd838f6d6d0101

search/d972_b345_relfrat3_gha_driver_v1.g
  6811 bytes
  fce9b3ba8c9b686fb6af2bd5a6da1b29f7486616948a6907982af14cd5d8738b
```

B345_RELFRAT3_IMPLEMENTATION_READY
