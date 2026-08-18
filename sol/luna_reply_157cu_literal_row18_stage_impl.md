# Luna reply 157cu — literal row-18 finite-stage implementation

## Result

The requested versioned bundle is implemented and statically ready for the
parent-brokered GHA run.  I did not run GAP, Git, or GitHub Actions locally.
The only local execution was the short checker syntax/mutation selftest; it
printed

```text
AST_PASS
D972_B4_LITERAL_ROW18_STAGE_V1_CHECKER_SELFTEST_PASS
```

No mathematical terminal result is claimed before the producer and the
independent full replay finish on GHA.  The producer can emit exactly one of

```text
ROW18_TYPED_STAGE_LIFT
EXACT_FINITE_STAGE_OBSTRUCTION
UNKNOWN_MISSING_INPUT
```

and the workflow converts a wall-clock stop only to `UNKNOWN_RESOURCE`.

## 1. Producer

Created `search/d972_b4_literal_row18_stage_v1.g`.

It performs the following finite construction in one pinned GAP 4.16.0
process.

1. It reruns the fast v2 C2 producer, retains all 24 lossless source words,
   and replays their `E^4`, `P^4`, and `G9^4` images in the ordering
   `(coord1 u..z),...,(coord4 u..z)`.  The first-deletion words give a
   separately replayed six-word `F2` correction basis.
2. It derives the natural action
   `p^sigma = sigma^-1 p sigma` inside the Artin presentation of `B4`.  The
   tested PackageGT `conjBySig*` words are kept as the opposite
   kernel-conjugation orientation and are independently compared with
   `p^(sigma^-1)`.  Thus natural `EvalWord` is not mixed with reverse
   `PaperProd`.  The three 24-by-24 matrices are obtained from the 24 actual
   transformed source words, not declared from coordinate permutations.
3. It checks both Artin braid relations, distant commutation, all three
   coordinate transpositions, and replays all six canonical pure generators
   as actual words in the three `B4` matrices.  Projection order 504 is not
   used by itself to infer a direct product.  The commutators
   `(x23,x24)`, `(x13,x14)`, `(x12,x14)`, `(x12,x13)` are computed as exact
   matrices; they have support only in coordinates 1, 2, 3, 4 respectively,
   and their normal closures in the corresponding factor projections each
   have order 504.  This certifies `P^4` inside the pure image and hence
   pure-image order `504^4`.  Separately, every nonzero vector in each
   six-space has invariant closure rank 6 (module irreducibility, not group
   simplicity), while the computed coordinate image is transitive `S4` of
   order 24.  These certificates give the single 24-dimensional chief
   factor and exact full image order `504^4*24`.  The receipt retains every
   witness word, its four block matrices, support, normal-closure order, and
   the exact matrix-word kernel membership certificate.
4. It reconstructs the literal presentation as the 18 prefix rows plus all
   five ordered coface images of the 28 seeds.  It recomputes the prefix,
   seed, `5*28`, presentation, and all-972 ordered-Dtilde digests.  Every raw
   coface row must vanish in `P^4` and `G9^4` and land in the marked `V^4`;
   otherwise the producer fails closed.
5. It converts all 140 raw relation values to the marked 24-bit basis and
   closes their span under the computed Artin action.  Every independent
   boundary retains its original row, actual transformed F6 word, raw-row
   index, and Artin path.  This is the literal relation boundary, rather than
   a relabeling of a Magnus residue or the old rho orbit.
6. It binds zero-based row 18 to the exact key and 24-letter source word.  It
   evaluates both hexagons and the ordered five-coface pentagon for all 64
   correction elements.  The receipt records the two hexagon residuals, the
   pentagon residual, the six gauge columns, the complete relation
   combination, and the corrected lossless pentagon word.  Marking,
   charmingness, PB3 onto, exact roof reduction, and representative
   independence are all gates, not annotations.
7. It also constructs the exact GT-shadow square with the composition
   substitution formula, never by concatenating a naive word square.  It
   finds the unique powered roof among the frozen 972 rows, computes the root
   action `T`, the characteristic-two norm `I+T`, and records unpowered and
   powered hexagon/pentagon defects.  Exponent 1 is preferred when it works;
   exponent 2 is selected only as the accepted pure-axis power route.
8. For a selected witness it forms the literal boundary subgroup
   `R <= V^4`, proves its order and normality, constructs the actual finite
   quotient `E^4/R`, and checks the source homomorphism is bijective there.
   It separately checks the `P^4` and actual `G9` fourfold-image source
   homomorphisms.  Settlement is therefore tested after relation surgery in
   the correct quotient, not incorrectly demanded in raw `E^4`.

At static time there is no omitted code field.  The only fail-closed runtime
missing names are:

```text
a18_comparison.dtilde_to_pab_pentagon_transport
stage.row_power_base_hexagon_membership
stage.row_power_base_pentagon_membership
settlement.source_endomorphism_bijective
```

They are emitted only if the corresponding exact finite reconstruction
fails; they are not theorem-gap placeholders.

## 2. Independent checker

Created `search/check_d972_b4_literal_row18_stage_v1.py`.

It imports no producer helper.  It independently reconstructs the marked
72-point `E`, its 64-element module, the row-vector `PSL(2,8)` action and
marked `E/V` table, exact `MakeGn(9)`, the four strand-deletion tuples, and
all 24 basis-word values.  It then independently rebuilds the natural Artin
words, all three matrices, all-six pure-generator matrix replays, the four
single-support commutators and normal closures, factor orders and the chief
test, literal 18+140 rows, Dtilde words, the B4-closed relation span,
the six correction words, both 64-element fibres, the exact GT square,
norm, selected relation correction, roof reduction, and quotient settlement
data.

The mutation selftest covers every requested class:

- PSL row/column orientation;
- one literal A.18 coface;
- factor order;
- a basis/source word;
- one action-matrix bit;
- one single-support commutator pair and the matrix inverse/commutator path;
- row-18 key and word;
- one correction bit;
- GT composition order and naive word powering;
- roof reduction/key binding; and
- each of the three producer terminal statuses.

## 3. Workflow

Created `.github/workflows/d972-b4-literal-row18-stage-v1.yml`.

It supports both direct manual dispatch and same-ref reusable `workflow_call`,
uses immutable 40-hex action revisions, and checks
the exact SHA-256 of the producer, checker, fast-v2 producer/checker, all
phase2b/map/core inputs, both frozen roof artifacts, literal input, and the
PackageGT source.  It installs the same pinned JSON 2.4.0 package as the
repaired v2 workflow, requires GAP 4.16.0, uses one job, and runs the existing
independent core checker before the new independent stage checker.  The
100-minute command bound is below the 110-minute job bound.  Receipt and all
logs are uploaded under `always()`, including timeout and failure paths.

The stale fast-v2 pins were replaced and independently rehashed as follows:

```text
search/d972_d972core_c2six_intersection_v2.g
  577de029a49e2db3a33cf3b4437c78548214f9635b1750185d48a5385c161f4c
search/check_d972_d972core_c2six_intersection_v2.py
  ab6b26d40c268de5e309ebcd9b56eddd52e91de2cc147ef8a1af9198a6523761
.github/workflows/d972-d972core-c2six-intersection-v2.yml
  0b13b52af7e9f277ffd41f1bd0ac198e684facbf223ff62aefd1c1d8bf0a9be8
```

The first two are runtime dependencies and are pinned by this workflow.  The
third is not executed as a nested workflow; its hash was nevertheless checked
to bind the audited upstream bundle version.

## 4. Final immutable hashes

```text
search/d972_b4_literal_row18_stage_v1.g
  e3a8df2d61d7e4f2527bd3a46ef631c2349f2b1f31d1afa84266f545d040c6d9

search/check_d972_b4_literal_row18_stage_v1.py
  1c9b9fb4f2c1e331323ec0cd8cf6e46bcac9fd2957780493f02ea3991c4d7649

.github/workflows/d972-b4-literal-row18-stage-v1.yml
  f508b7b82bdba4077a233ccca7df569cfbedf092aeb149ef58f717f64a897a4b
```

The workflow contains the first two hashes verbatim, has no placeholder,
and its three action references passed the immutable-revision static check.

LITERAL_ROW18_STAGE_READY_FOR_GHA
