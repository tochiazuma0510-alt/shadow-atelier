# Luna reply 157da — matched q=3 B3/B4/B5 chief campaign

Date: 2026-08-18

## Verdict

```text
B345_Q3_MANIFEST_READY_FOR_GHA
```

The bounded producer and independent checker are implemented. No local GAP, Git,
GHA, workflow edit, or heavy/parallel Python was used.

The run is no longer predetermined to stop at `MISSING_TYPED_D2`. It first proves
the coarse/q3 pullbacks are direct products, constructs the actual 27-word
coarse-trivial correction fibre, and scans the complete preregistered universe

```text
roof powers {1,2,4,5,7,8} mod 9 × 27 corrections = 162 candidates.
```

The full run can now terminate as follows:

- first settled outside word: `B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION`;
- all 162 fail: `B345_Q3_MISSING_TYPED_D2`;
- ANUPQ resource failure: `B345_Q3_UNKNOWN_RESOURCE`.

`MISSING_TYPED_M5` is not used. A coarse arity-five quotient is never built.

## 1. Direct presentations and the one-ANUPQ construction

The producer independently constructs the standard Fadell–Neuwirth presentations
with lexicographic marked generators:

```text
PB3:  3 generators,  2 relations
PB4:  6 generators, 11 relations
PB5: 10 generators, 35 relations
```

It derives all `A_ij` Artin words, replays every relation in the faithful Artin
action, derives all five `PB3 -> PB4` cofaces, all six `PB4 -> PB5` cofaces, all
deletions, cosimplicial identities, literal A.18 order, and the 14V/21E
six-pentagon/three-square K5 complex. The shared formula digest remains

```text
b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef.
```

Production calls ANUPQ exactly once:

```gap
PqEpimorphism(PB5 : Prime:=3, ClassBound:=4, Exponent:=3)
```

PB4 and PB3 are then recovered as endpoint-insertion subgroups of `Pi5[3]`; no
separate PB4/PB3 ANUPQ call is made. The producer requires ANUPQ 3.3.3, exponent
3, and returned class at most 3. Completeness uses F. Levi and B. L. van der
Waerden, “Über eine besondere Klasse von Gruppen,” *Abh. Math. Sem. Univ.
Hamburg* 9 (1932), 154–158, DOI `10.1007/BF02940639`: exponent-three groups have
nilpotency class at most three.

## 2. Exact no-common-q3 shortcut

The v2 coarse source is reconstructed from the pinned core. The actual groups are

```text
Q4 = im(PB4 -> P^4 × H9),  Q4 = P^4 × H9,
Q0 = P × G9,
P  = PSL(2,8), |P|=504.
```

The producer performs no `AbelianInvariants` call. It performs exactly one new
`DerivedSubgroup`, on actual `H9`, and gates

```text
|H9'| = 3^24,     |H9:H9'| = 32.
```

For G9 it reuses the pinned core series `2916 -> 729 -> 1`, hence
`|G9:G9'|=4`. Since P is perfect,

```text
|Q4^ab|=32,   |Q0^ab|=4.
```

Neither group has a nontrivial finite 3-group quotient: any nontrivial finite
3-group has a C3 quotient. Therefore the common quotients with `Pi4[3]` and
`Pi3[3]` are trivial, and the required pullbacks are exactly

```text
E4 = Q4 × Pi4[3],   V = Pi4[3],
E3 = Q0 × Pi3[3].
```

This is independently checked without trusting GAP's derived-order flag:

1. the checker enumerates P's 504 elements and proves `|P'|=504`;
2. it reconstructs `G9'=C9^3` from the marked permutations;
3. it requires all 24 marked P blocks to lie in P and all 24 marked H9 blocks to
   lie in G9, using those independently enumerated factor groups;
4. it maps all 15 pair commutators of the six H9 generators and the invariant
   linear closure under all six conjugation actions into
   `(G9')^4=(Z/9)^12`;
5. their mod-3 span has rank 12, so Nakayama gives
   `H9'=(G9')^4`; consequently `H9/H9'` embeds in the 2-group
   `(G9/G9')^4`.

Thus the direct-product pullback is cross-checked, not merely asserted by a GAP
abelianization receipt.

## 3. The actual correction fibre and six roof powers

Inside `Pi3[3]`, the marked subgroup `<A12,A23>` is proved to be `B(2,3)` of
order 27. The producer forms the marked diagonal over `Q0`, proves its projection
kernel has order 27, and enumerates only this proved order-27 kernel. The checker
independently enumerates `<A12,A23>` with a fail-closed cap (a 28th element is an
error), proves its order is exactly 27, and requires its element set to equal the
27 exported correction values. The producer obtains
free F2 words by taking preimages only for the at-most-three pc generators of the
kernel, then expands all 27 elements from pc exponents. Thus the expensive
preimage call count is at most three, not 27.

Every correction word is replayed as identity in Q0, its Pi3 pc coordinates are
exported, and all 27 Pi3 values are distinct.

For roof row 18, literal iterated power words are never retained. All 972 frozen
`(P,G9)` keys are evaluated exactly once and cached. At step `n`, the producer
forms only `GTCompose(base, canonical_(n-1))`, identifies its unique frozen
`m=0` row, and immediately canonicalizes again. A hard 100,000-letter bound and
the actual maximum bounded-step/canonical lengths are exported.

The normalized orbit is checked for every `n=0..9`: `n=0` is the unique frozen
coarse identity, the rows at `n=0..8` are pairwise distinct, and `n=9` is the
first repeat and is exactly the identity row. This is a GT-composition orbit
gate, not an inference from the ordinary permutation order. Consequently
`{1,2,4,5,7,8}` is the complete set of nonmultiples of three modulo nine; those
six rows are also checked to have ordinary coarse order nine.

Canonical normalization does **not** require equality of the raw and canonical
q3 images. Instead, for every exponent it proves

```text
{bounded_step_n * k : k in B(2,3)}
  = {canonical_n * k : k in B(2,3)},
```

with 27 distinct elements on both sides. The q3 rebasing shift is bound both to a
correction index and to ambient Pi3 pc coordinates.

## 4. Exact 162-candidate scan

For each canonical outside roof and each correction, the producer applies, in
order:

1. exact coarse roof equality;
2. original/full-B4 charmingness as derived-subgroup membership in the fine
   quotient;
3. both direct hexagons in Q0 and `B(2,3)`;
4. the direct ordered A.18 pentagon in Q4 and `Pi4[3]`;
5. onto gates in Q0 and `B(2,3)`;
6. settlement automorphisms in Q4 and `Pi4[3]`.

`PENT-FORM'`/`Dtilde` is diagnostic only. It is evaluated precisely when the raw
F2 exponent sums are `(0,0)`; otherwise its receipt is
`applicable=false, value=null`. It never rejects an otherwise direct-pentagon
candidate.

All gate-pass indices and per-power progressive counts are losslessly exported.
Fixed coface contexts, onto results, the 972-key table, and settlement image tuples
are cached. A first settled witness stops immediately with
`exhaustive=false, stop_reason=FIRST_TYPED_WITNESS`; only a zero-witness result
runs all 162 and records `ALL_162_EXHAUSTED`.

Candidate words are not concatenated/reduced in the 162-entry hot loop before the
cached gates. Base/correction exponent sums are precomputed; the full word is
materialized only for an applicable Dtilde diagnostic or an actual structural
settlement test. The producer exports structural-test, factor-cache, and global
bijection-call counters. In particular, each global Q4/Pi4 bijectivity call is at
most one.

The literal onto conjugate is pinned in both languages as

```text
PP([f^-1,y,f]) = f*y*f^-1
```

because paper product reverses the displayed list. The P, G9, and B2 checker gates
all call the same `paper_conjugate` helper; the producer's factorized Q0 cache uses
the identical `D972Q3PP` expression. A non-involutory S3 canary distinguishes it
from the opposite `f^-1*y*f` orientation. The checker also precomputes every fixed
hexagon/pentagon context for the base roofs and 27 corrections, matching the
producer cache instead of reevaluating long candidate words in 20 contexts.

For a positive settlement, the producer exports:

- the six source words;
- forward and inverse Pi4 pc-generator images;
- inverse words for every marked generator in both Q4 and Pi4.

The checker validates both Pi4 homomorphisms and both compositions on every pc
generator. For coarse Q4, it independently reconstructs the assignment on each of
the four P and four G9 coordinates. A canonical BFS over P (504) and G9 (2916)
checks every Cayley edge, full bijectivity, and all six marked-row bindings. Since
the H9 image rows are words in the original H9 generators, the ambient G9^4
automorphism restricts to an automorphism of finite H9. Thus a positive terminal
does not trust `Q4_bijective=true` or `Pi4_q3_bijective=true` booleans.

## 5. Independent checker boundary

The Python checker imports neither the GAP producer nor any existing collector
helper. It independently reconstructs the braid/coface/deletion/K5 formulas,
replays all exported pc collectors and maps used by the selected branch, verifies
the correction group and bounded-step/canonical fibre equality, reconstructs the
complete normalized `n=0..9` GT-composition orbit from the frozen 972-key table,
and recomputes every roof/charming/hexagon/pentagon/onto/settled bitset.

For every onto candidate, including the exhaustive-negative branch, settlement
is reconstructed independently. Four P and four G9 marked-factor assignments are
checked by bounded Cayley-edge BFS with all six bindings; the images are words in
H9, so the ambient automorphism restricts to finite H9. The 11 PB4 relators are
replayed in Pi4, and the source-word exponent-sum matrix is required to be `I6`.
Since `Pi4/Phi(Pi4)=PB4_ab mod 3=(C3)^6`, Burnside's basis theorem then gives the
Pi4 automorphism. GAP's global Q4/Pi4 `IsBijective` calls are used only once, on a
first structural witness, as assertions and to export inverse receipts; they are
never the sole reason for an empty settled bitset.

On the all-negative branch, the two endpoint deletion homomorphisms are the exact
last records in the 5-to-4 and 4-to-3 deletion families. The producer constructs
the other seven deletion maps only once; the checker validates each of the nine
distinct maps once and then requires structural equality of the endpoint aliases,
instead of replaying the same two homomorphisms twice.

The final token is bidirectionally bound to this scan: one settled solution means
exactly `...EXACT_WITH_WORD_CORRECTION`; zero solutions means exactly
`...MISSING_TYPED_D2` after all 162 candidates. Other otherwise-allowed campaign
tokens cannot relabel a completed direct-route receipt.

Its only irreducible external construction contract is that pinned ANUPQ's
`PqEpimorphism` returns the maximal exponent-three quotient; the class theorem
closes the finite class bound. In the exact-word branch, the unused full PB5
collector and PB5 map bundle are deliberately absent and the checker requires the
explicit bypass receipt. In the all-162-negative branch, those full objects are
built and checked before returning `MISSING_TYPED_D2`.

## 6. Performance order and failure semantics

Production is sequential in one GAP process:

```text
pins/formulas
 -> pinned row18-v2 core
 -> one H9 derived computation
 -> one PB5 ANUPQ call
 -> light PB4/PB3 collectors
 -> 6×27 direct scan
 -> only if all 162 fail: full PB5 collector + 5+6 cofaces + 9 distinct
    deletions (the two endpoint records are reused, not rebuilt).
```

Expected dominant operations are the one PB5 `PqEpimorphism`, then (only on the
negative branch) the O(n^2) PB5 pc conjugate tables and full map bundle. The exact
witness branch skips that second cost. Other bounded costs are one H9 derived
subgroup, one 972-row key pass, at most three correction preimages, small factor
enumerations in the checker, and at most one positive settlement certificate.
The Q0 onto gate is reduced to cached P(504) and G9(2916) projections; it never
constructs a candidate subgroup inside the 1.47-million-element direct product.
Settlement similarly uses cached small-factor structural tests for every onto
candidate; the giant Q4 and Pi4 global bijectivity assertions run at most once,
only after the first structural success.

There is no PB3/PB4 ANUPQ rerun, class-3/class-4 double production, full Pi5/Q4
enumeration, large Cayley table, or coarse arity-five direct product. The only GAP
`Elements` call is on the already-proved order-27 correction kernel. Checkpoints
and `Runtime()` markers identify presentation, coarse gate, PB5 summary, PB4/PB3
light collectors, direct scan, and—only after a negative scan—the full PB5/map
phases. `PqEpimorphism=fail` is serialized as `B345_Q3_UNKNOWN_RESOURCE`, never a
mathematical obstruction.

Exact dynamic heavy-call budget for `RUN` is:

```text
PqEpimorphism            1  (PB5 only)
DerivedSubgroup          1  (H9 only)
AbelianInvariants        0
Elements                 1  (proved order-27 K only)
PreImagesRepresentative <=3 correction pc-generator preimages
                         +12 only after a first positive settlement
global Q4 IsBijective   <=1 (first structural witness assertion only)
global Pi4 IsBijective  <=1 (same branch)
```

The source contains a second `PqEpimorphism` only in the mutually exclusive tiny
`SELFTEST` branch. The B2 permutation inverse is evaluated through the inverse
isomorphism, so it does not add 27 preimage searches. A positive branch omits the
full PB5 collector/maps; a 162-candidate negative branch builds them exactly once.

## 7. Files, hashes, and static audit

| File | Bytes | SHA256 |
|---|---:|---|
| `search/d972_b345_q3_chief_v1.g` | 74,595 | `459c9b1728316a064644ce2e658c0e09dd06b0722fab3e767aaf6f51ebb91d45` |
| `search/check_d972_b345_q3_chief_v1.py` | 87,732 | `9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb` |

GHA canary run `32129602522` at commit
`b40c7fcae815a4fe6e725001496982e24d6198aa` reached the GAP script and then
failed after about 1m39s with `Error, immutable lists cannot be sorted`.
GAP 4.16 returns an immutable list from `RecNames`; the serializer attempted to
sort it in place. The repaired producer sorts
`ShallowCopy(RecNames(x))`. This changes neither JSON ordering nor any formula,
group, candidate, predicate, schema, terminal, or performance schedule.

The follow-up canary run `32130140976` at commit
`522dc918e51fe14f5c68ea19620b214e7930ec92` passed the immutable-`RecNames`
point, then stopped before ANUPQ with
`157da selftest: cross-language formula digest drift`. Static diagnosis found a
second GAP JSON type-order issue: the empty list also satisfies `IsString`, so
empty word/map arrays were emitted as `""` instead of `[]`. `D972Q3Json` now
returns `[]` for a length-zero list before its string branch. The expected
cross-language formula SHA remains `b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef`.
This is another pre-ANUPQ serializer stop, not a mathematical or ANUPQ result;
the next GHA canary is the runtime test of this repair.

Pinned inputs include both row18-v2 files, not stale v1:

```text
row18 producer  8f8b429b5725b244a214cc6a4cf59daa186e4ee2d4d6eee6df18e580d88ef2a1
row18 checker   bf85cfd142f6c640e96af77aa5f580caa206439329d17ed18ac342ac6acdcd19
row18 core      577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c
phase2b receipt 648335000ff70f37d357c9c27ec5054cd4366b281c616f0391c4c7580cd4bcb9
word artifact   564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9
```

The one permitted Python self-test was run before the final short-route additions:

```powershell
python -B search/check_d972_b345_q3_chief_v1.py --self-test
```

It completed in 4.9 seconds and printed

```text
D972_B345_Q3_CHECKER_SELFTEST_PASS mutations=6 formula_sha256=b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef
```

Per the task's single-test limit, it was not rerun after the final additions. The
final snapshot received a static delimiter-balance audit, stale-pin scan, forbidden
API/performance scan, exact SHA audit, and new unexecuted conjugation-orientation
and terminal-relabel mutation canaries. It also statically binds the normalized
orbit, B2 completeness, endpoint reuse, factor-membership, all-candidate settled
bitset, and global-call counters. No local GAP syntax/runtime claim is made; the
newly repaired registered GHA canary is required next. Both canary failures
above were pre-ANUPQ serializer bugs, not ANUPQ or mathematical failures.

## 8. Generic-workflow dispatch inputs

Canary:

```powershell
gh workflow run gap-run.yml --ref <COMMIT_SHA> `
  -f script=search/d972_b345_q3_chief_v1.g `
  -f 'preamble=D972_B345_Q3_SELFTEST:=true;;' `
  -f out_dir=ci/out `
  -f timeout_min=20 `
  -f with_pquot_packages=true
```

Full run after the canary passes:

```powershell
gh workflow run gap-run.yml --ref <COMMIT_SHA> `
  -f script=search/d972_b345_q3_chief_v1.g `
  -f 'preamble=D972_B345_Q3_RUN:=true;;D972_B345_Q3_OUTPUT:="ci/out/d972_b345_q3_chief_v1.json";;' `
  -f out_dir=ci/out `
  -f timeout_min=330 `
  -f with_pquot_packages=true
```

Artifact and replay:

```text
ci/out/d972_b345_q3_chief_v1.json
```

```powershell
python -B search/check_d972_b345_q3_chief_v1.py ci/out/d972_b345_q3_chief_v1.json
```

The broker must require exactly one registered terminal marker and the independent
`B345_Q3_CHECKER_PASS` marker.

## B4 impact

A checked `...EXACT_WITH_WORD_CORRECTION` artifact would give one actual outside
typed lift at this authenticated q=3 stage, using the complete six-power/27-fibre
universe. It would bypass the missing linear `d2` at this stage. It is still not by
itself the uniform cofinal-stage theorem or final B4-B conclusion.

If all 162 fail, the exact first missing object is the relative six-face
`Q3_TYPED_D2`/chief construction in Pi5[3]; the result is not promoted to a finite
obstruction and does not decide A/B.

## 157df atomic-write supersession

The registered canary `32130817181` passed, while full run `32131160061`
stopped before ANUPQ at its first checkpoint because the GAP process had no
binding for the old rename primitive. The bounded repair uses the official IO
package and `IO_rename` only after the same-directory temporary stream is
closed; it never removes the destination before replacement and fails closed
if the package, operation, or replacement result is unavailable.

The producer self-test now performs two writes to the fixed
`ci/out/d972_b345_q3_atomic_io_smoke.json`, reads the second canonical JSON
plus newline, checks that it is not the first payload, removes the smoke file,
and prints exactly one
`D972_B345_Q3_ATOMIC_IO_SELFTEST_PASS backend=IO_rename replace=true` marker.
The thin driver creates `ci/out` before reading the producer and gates that
marker through the producer's one-count self-test binding. Immediately after
the direct scan, the producer emits one branch marker for either the selected
first typed witness or all 162 candidates exhausted; neither marker is an A/B
conclusion.

Current code pins (checker and all mathematical inputs are unchanged):

```text
search/d972_b345_q3_chief_v1.g        76,704  e3dad87ad066fc9c605e1eecaddbe63efd63ac68500e0fcff0d6d62eb7d83af3
search/d972_b345_q3_gha_driver_v1.g    5,463  6a3cb5339468dd7f1b214c67d9791b0f752d0df625f06781470dc24c92a8a859
search/check_d972_b345_q3_chief_v1.py 87,732  9864e55f6e0ee1ae8100788e5ba127ef95bffd62535c3aa23a192cde6109cfcb
```

The source-only audit is limited to the I/O and logging changes above:
replacement is real and same-directory, the driver gate is exact-one, the
direct scan has no per-candidate logging, and no predicate, candidate order,
terminal mapping, ANUPQ budget, or receipt acceptance rule was altered. The
implementation token is
`B345_Q3_ATOMIC_WRITE_REPAIR_READY_FOR_GHA`.
