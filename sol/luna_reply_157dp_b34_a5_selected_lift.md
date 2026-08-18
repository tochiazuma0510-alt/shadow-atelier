# Luna reply 157dp — B4 q3 × A5 selected-roof lift bundle

## Verdict

Implemented the complete versioned `157dp` bundle in the four authorized new
files.  I did not run GAP, Git, GHA, or the full producer.  The one authorized
lightweight Python checker self-test passed.

This bundle registers the complete composite fibre over the fixed outside roof
`exponent=2`, frozen row `37`:

```text
27 q3 representatives × 5 marking shifts × 1500 D_F corrections = 202500.
```

The implementation has two exact, asymmetric terminal meanings:

- `B34_A5_LAYER_FIXED_OUTSIDE_ROOF_LIFT_CROSSCHECKED`: a literal charming,
  friendly, hexagon, ordered-pentagon, and F2-onto lift exists at the concrete
  `A5^4` layer.  This is one chief-layer advance only.  It does not claim that
  the non-isolated computational `L` has `I_L=X`, and it does not by itself
  finish B4-B.
- `B4_A_FIXED_OUTSIDE_ROOF_FIBRE_OBSTRUCTION_CROSSCHECKED`: allowed only after
  a cap-free, independently reconstructed scan of all 202500 coordinates with
  no skipped candidate.  Corollary 3.13 then excludes the fixed `x∈X\A` from
  the genuine roof image `P`; with `A≤P≤X` and `[X:A]=3`, this gives `P=A`,
  hence B4-A.

Settlement at the non-isolated `L` is explicitly diagnostic-only and is never
an acceptance or rejection gate.

## Files and frozen hashes

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_b34_a5_selected_lift_v1.g` | 54196 | `ed350659ea6f77c0151e84e92395b050e7c0d65455c2e8e8a7d9851af9393440` |
| `search/check_d972_b34_a5_selected_lift_v1.py` | 78293 | `e062b4e16f323bee1c8af1f23cfdce5820a9b782066c8bf6bbf1327506f8f0f4` |
| `search/d972_b34_a5_selected_lift_gha_driver_v1.g` | 12310 | `598b2edc3b3847207f993f493859179d91b1465b6c1e679bd3f0a89315ec30cc` |

The driver hard-pins the first two hashes.  It also pins the q3 and FC8
producer/checker/driver sources and the frozen word/pure-axis inputs.

## Exact construction and independent gates

### Fixed roof and complete old fibre

- Rebound the complete normalized GT-compose orbit to all frozen 972 keys:
  exponents `0..9` have row indices
  `[1,19,37,55,73,10,28,46,64,1]`.
- Reconstructed row 37 as the normalized `e1^2` row, not from the q3 receipt's
  outside boolean.  In `X/W≅S3×C6`, the square is the nontrivial C3 element and
  belongs to none of the three possible C2 arithmetic complements.  The
  accepted pure-axis source is pinned at
  `59c96e7d62a20af4207f715df8e2927a8fc373e1f12e8f3be70e535d8afe5347`.
- Independently reconstructed the exported PB3 exponent-three collector,
  proved `<x12,x23>` has exactly 27 elements, and checked that the 27 source
  words are q3-coarse-trivial and take all 27 distinct B(2,3) values.  Thus
  they are the full fine fibre, not samples.

### D1 and actual source sections

- Rebuilt the five literal A.18 cofaces and four deletions, then all twenty
  PB3→PB4→A5 composites independently in producer and checker.
- Obtained exactly eight common onto A5 components and twelve C5 components,
  with cyclic source multiplicities `[4,4,4]`.
- Replayed the exact image orders
  `|D|=7500`, `|D_F|=1500`, and `|D_F'|=60`.
- Used the actual F2 words `x^18` and `y^18`.  They are identity in the old
  target, while their conjugates normally generate all of the small compact
  `D_F`.  A tracked normal-generator list and deterministic 1500-state BFS
  DAG give a lossless old-trivial source word for every correction class.
  Neither side constructs or enumerates a large `F_H×D_F` joint group.
- Closed the PB2 fibre explicitly: the old image has order 18, the new factor
  has order 5, their joint image has order 90, and the five shifts
  `m=0,18,36,54,72` are old-trivial and pairwise distinct in the new C5
  factor.  Only `s=4` fails `gcd(36s+1,90)=1`.

### Complete scan and performance invariants

- The registered loop order is exactly outer q3 receipt order, `s=0..4`, then
  section-BFS order.  A negative requires `evaluated=202500`, selected null,
  and `resource_skips=0` on both producer and checker.
- `derived_all` counts the affine `D_F'` slice across all five shifts before
  friendliness; `friendly_derived` separately counts the four friendly
  shifts.  Their hard bounds are respectively 8100 and 6480.
- All fixed quotient/context values and the 27×1500 derived flags are
  precomputed.  No section word is expanded in the 202500-coordinate hot
  loop.  At most the first accepted candidate materializes one long source
  word, followed by a direct replay in every old/new hexagon and pentagon
  context.
- New F2-onto closures are cached by `(A5-derived value, friendly shift)`.
  The implementation and checker enforce the structural upper bound
  `60×4=240` cache entries.
- The old marking-period implementation was corrected during static audit:
  it now raises each individual hexagon context element to the 18th power,
  rather than attempting to power a pair-list.

## Same-job driver and FC8 normalization

The thin driver removes every stale upstream/new artifact and sentinel before
production, regenerates each pinned upstream exactly once in a separate GAP
process, and requires its exit-zero sentinel and exactly one checker marker.

The historical FC8 receipt differs on regeneration only in the nonsemantic
`performance.runtime_ms` field.  The approved driver contract is fail-closed:

1. require the fresh FC8 checker PASS;
2. require canonical JSON and exactly one integer `performance.runtime_ms`;
3. replace only that integer by the frozen value `598`;
4. compare the parsed receipts with that field removed and require all other
   fields equal;
5. require raw SHA256
   `558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584`;
6. rerun the independent FC8 checker and require PASS.

The observed fresh runtime and the before/after checker facts are recorded in
the 157dp receipt.

## Static and self-test audit

- Python AST parse: PASS.
- GAP source delimiter/function static balance: PASS (`35/35` producer,
  `7/7` driver).
- All three executable files are ASCII-only.
- Placeholder scan after driver pinning: clean.
- Checker self-test:

```text
D972_B34_A5_SELECTED_LIFT_CHECKER_SELFTEST_PASS mutations=21
```

The mutations cover a q3 word, duplicate and missing q3 records, coface,
deletion, A5 marking, cyclic coordinate, marking shift, direct-product kernel,
charming rule, literal residual, outside roof key, both upstream artifact
hashes, coverage digest, derived count, settlement gate, nested rhoA/block
conversion, the PB3-to-F2 alphabet projection, and terminal relabel.

## Run 32164627934 checker repair

The first full run at commit `82bf4bb1` reached a producer positive at
candidate 124 (`new_charming=9`, producer runtime 410 ms), then the checker
stopped at `rhoA replay`.  This did not refute the candidate.  The exact cause
was a checker-only representation mismatch:

- the frozen FC8 field `rhoA.marked_images` is shaped `6 x 4 x 5` (six PB4
  generators, four A5 coordinates, five permutation images);
- the checker constructed six degree-20 block permutations and compared those
  flat rows directly with the nested receipt;
- the GAP producer had already converted the four receipt components to one
  degree-20 block before comparison, which is why its replay passed.

The checker now independently validates the exact `6 x 4 x 5` shape, compares
all twenty component rows first, converts each receipt row with
`block([perm(component) for component in row])`, and then compares the six
degree-20 permutations.  A focused mutation changes one nested A5 component
and is rejected.  No candidate predicate, group operation, registered universe,
terminal implication, producer source, or frozen input pin changed.

## Run 32165338456 checker repair

The rerun at commit `ae1607a3` again produced the same positive candidate 124
(`new_charming=9`, producer runtime 529 ms).  The repaired checker passed the
rhoA gate and then stopped at `q3 ambient coords`.  This was a second
checker-only typing error.

The q3 `correction_fibre.records[*].word`, the selected row-37 word, every
outer word, and every materialized correction candidate are words in
`F2=<x12,x23>`.  The GAP producer evaluates them with
`[b2x,b2y]=[PB3 marked generator 1, PB3 marked generator 3]`.  The checker had
used the complete canonical PB3 list `[x12,x13,x23]`; its letter `2` therefore
meant `x13`, contradicting both the frozen q3 checker and the producer.

All four F2-word sites now use the explicit projected alphabet
`[marked3[0],marked3[2]]`:

1. q3 correction word versus `ambient_Pi3_coords`;
2. each outer word's B(2,3) main value;
3. the selected materialized candidate's B(2,3) value;
4. its comparison with the cached outer value.

The PB2 coface words remain correctly evaluated on the full three-generator
PB3 marking.  A focused canary fixes canonical PB3 order
`(x12,x13,x23)` and requires the F2 projection `(x12,x23)`.  Again, the
producer, registered 202500 universe, candidate predicate, and mathematical
terminal implications are unchanged; candidate 124 was not refuted.

## Run 32166647535 checker schema repair

At commit `d50ecb01`, the producer again returned the same positive candidate
124 (`new_charming=9`, runtime 573 ms).  The checker passed both previous
repairs and then raised `KeyError: 'derived_slice'`.

The producer's internal `D972A5LScan` record has a `derived_slice` diagnostic,
but the pinned top-level JSON constructor deliberately serializes only its two
load-bearing totals inside `scan.counts` as `derived_all` and
`friendly_derived`; it does not serialize a top-level `derived_slice` field.
The checker was therefore reading an unregistered internal field rather than
the actual receipt schema.

The checker now reads the two totals from `scan.counts`, compares them with its
independently reconstructed values, and explicitly rejects a stale top-level
`derived_slice`.  To avoid serial schema KeyErrors after this point, it also
checks the exact top-level, `scan`, and `performance` key sets before the heavy
audit, verifies provenance and runtime types, and checks the exact positive/
negative proof-record layouts before dereferencing them.  The selected record
continues to be compared as a complete dictionary against the independently
reconstructed first positive, so missing or extra selected fields fail closed.

A focused mutation inserts the stale top-level location and is rejected.  No
producer code, candidate predicate, registered universe, or terminal semantics
changed.

## Run 32169507334 scan-diagnostic repair

At commit `1bb5705f`, the producer again returned the same positive candidate
124 (`new_charming=9`, runtime 369 ms).  The checker passed the rhoA, F2-word,
receipt-layout, outer-fibre, and derived-total gates, then stopped at the old
composite message `scan replay`.

A field-by-field static comparison found no discrepancy in the registered
loop order, short-circuit order, counter update points, section-state
multiplication, hexagon/pentagon formulas, or onto predicate.  Consequently I
did not guess at, remove, or weaken a mathematical predicate.  The remaining
failure domain is exactly the serialized lossless scan transcript.

The checker now has separate fail-closed gates for:

1. `evaluated_candidates`;
2. `exhaustive`;
3. `counts`;
4. `rejection_rle`;
5. `rejection_stream_sha256`;
6. every ordinary field of `selected` and every field of its nested
   `direct_materialization_replay` record;
7. `settlement_is_acceptance_gate`;
8. `resource_skips`.

For a compound mismatch it prints only bounded canonical SHA256 stamps, never
the long selected word or full RLE.  This change is diagnostic and
fail-closed: equality predicates and expected values are unchanged.  The
focused self-test checks that a counts mismatch is reported specifically as
`scan.counts`; the complete lightweight self-test remains PASS with 21
mutation cases.  The producer SHA is unchanged.

## Source-only operation and runtime estimate

New producer heavy-operation contract:

- ANUPQ/PB5 calls: `0`;
- `Elements(A5^4)`: `0`;
- large joint-kernel/full-joint enumeration: `0`;
- `NormalClosure(D_F,…)`: exactly `1`;
- production `DerivedSubgroup`: exactly `4` (`D_F`, compact `D_F`, `Q0`, B2);
- `IsomorphismPermGroup(B2)`: exactly `1`;
- `Elements(B2)`: exactly `1` (27 elements);
- full 1500-state small-factor BFS passes: exactly `2`;
- Q4 permutation-group size gate: exactly `1`;
- old onto cache entries: at most `27+27+27`; new onto entries: at most `240`.

The checker executes no GAP/ANUPQ.  Its largest explicitly enumerated small
groups have orders 7500, 2916, and 1500; it never enumerates Q0, E4, or A5^4.

Based on the frozen q3 bootstrap (~13 s), FC8's frozen producer runtime
(598 ms), the bounded small-group tables, and two compact 202500-coordinate
passes, the source-only estimate is:

- driver/self-test canary: roughly 2–15 s;
- first-positive full job: roughly 1–4 min;
- cap-free negative full job: roughly 3–10 min;
- expected peak memory: below about 1.5 GB; conservative dispatch envelope:
  15 min and 2 GB.

These are pre-dispatch estimates, not measured 157dp timings.

## Remaining positive boundary

A positive closes this concrete q3→A5^4 chief layer and supplies an actual
outside stage witness.  The remaining B4-B obligation is still the uniform,
cofinal absorption of every later required chief layer, followed by the
finite-fibre compactness passage.  This bundle does not silently promote one
successful non-isolated stage to that global conclusion.
