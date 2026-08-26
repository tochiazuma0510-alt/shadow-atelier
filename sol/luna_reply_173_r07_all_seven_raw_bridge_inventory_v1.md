# Luna reply 173: R07 all-seven raw bridge inventory v1

Date: 2026-08-27
Scope: static callable inventory only

## 1. Outcome and scope

Verdict:

```text
GO    write a bounded, fail-closed all-seven raw-bridge preflight
STOP  call the present shelf an exact instantiation of v110
STOP  run an all-seven solve from the present shelf
```

The low-level word, quotient, Fox, coface, context-registry, and PB4 boundary
operations already exist.  The first load-bearing missing binding is not a
Fox routine: it is a typed proof that the task-157ee kernel is contained in
the four non-base source-E3 substitution kernels used by H1/H2.  The next
missing theorem is exactness of the marked two-relator PB3 presentation.  A
bounded successor can expose and test these gates without running an orbit or
linear solve, but it must return `UNKNOWN_INPUT` until they are closed.
V99 supplies the structural HT1/HT2/HT5 paper statements, but it does not
serialize either of these finite typing gates.

This audit used static reads/searches only.  No Python, GAP, Node, GHA, git,
generated scratch, or mathematical production run was used.

## 2. Literal executable relations

### 2.1 Shared word convention

The active executable definition is in
`search/d972_b345_seedspan_triple4_v1.py`:

- `inv_word`, `word_substitute`, and `pp_words`: lines 453--468;
- pure-braid relators and cofaces: lines 549--607;
- `f2_substitute`, `hexagon_words`, `embed_f2_pb3`, and `pentagon_word`:
  lines 897--930.

`pp_words([w1,...,wk])` reverses the displayed factor list before native word
concatenation.  This is the frozen convention
`paper_product = displayed_factors_multiplied_right_to_left`, also rebuilt
independently in
`search/check_d972_b345_seedspan_triple4_v1.py:270-299,357-442`.
`docs/week1-定義ノート.md:77,129` independently warns that relation products
use the paper convention.  No factor may be commuted.

Put, exactly as the code does,

```text
x = [1]
y = [2]
z = inv_word(pp_words([x,y]))
u = inv_word(pp_words([y,x]))
```

The executable relation occurrences are:

| block | printed occurrence order | signs | fixed factors between occurrences |
|---|---|---|---|
| H1 | `f(x,y)`, `f(x,z)^-1`, `f(y,z)` | `+,-,+` | all identity in this m=0 executable residual |
| H2 | `f(u,x)^-1`, `f(x,y)^-1`, `f(u,y)` | `-,-,+` | all identity in this m=0 executable residual |
| A.18 | `phi234(f)`, `phi1_23_4(f)`, `phi123(f)`, `phi12_3_4(f)^-1`, `phi1_2_34(f)^-1` | `+,+,+,-,-` | all identity |

The last row is the literal v71/v93 word

```text
b1 b2 b3 b5^-1 b4^-1,
b1=phi234, b2=phi1_23_4, b3=phi123,
b4=phi1_2_34, b5=phi12_3_4.
```

In the source's internal `parts` order,

```text
parts[0]=phi123
parts[1]=phi234
parts[2]=phi12_3_4
parts[3]=phi1_23_4
parts[4]=phi1_2_34
```

and lines 928--930 implement the same printed word as
`pp_words([inv_word(pp_words([parts[4],parts[2]])), parts[1], parts[3],
parts[0]])`.  This compressed inverse is not permission to swap the two
negative factors.

The five literal coface maps, in printed factor order, are:

| printed slot | source name | coface slot | images of `(a12,a13,a23)` |
|---:|---|---:|---|
| 1 | `phi234` | 0 | `[[4],[5],[6]]` |
| 2 | `phi1_23_4` | 2 | `[[1,2],[3],[5,6]]` |
| 3 | `phi123` | 4 | `[[1],[2],[4]]` |
| 4 | `phi12_3_4` | 1 | `[[2,4],[3,5],[6]]` |
| 5 | `phi1_2_34` | 3 | `[[1],[2,3],[4,5]]` |

The declaration order in `relevant_formula` is instead
`phi123,phi234,phi12_3_4,phi1_23_4,phi1_2_34` with slots
`4,0,1,2,3`; both orders must be serialized, not identified by ordinal.

### 2.2 Correction side, difference sign, and inverse rule

For a source word, list concatenation `reduce_word(g760 + c)` is the right
correction `f0 -> f0 c`.  The only fresh-g760 named raw formula is task 172's
H1/coface-0 constructor
`search/d972_r07_full_e4_joint_orbit_preflight_v2.py:62-76`.  It explicitly
records `corrected_minus_base` and the three substitutions
`(X0,Y0),(X0,Z0),(Y0,Z0)`.

The older `affine_target6_formula` at
`search/d972_b345_seedspan_triple4_v1.py:8949-8994` also forms
`R(f0 c) R(f0)^-1`, but its `f0` is the historical 20-letter `FIXED_WORD`, not
g760.  The historical typed-DAG lane at lines 9343--9402 builds H1, H2, and
the ordered pentagon with a right correction, and lines 9570--9618 form
`one_gradient - base_gradient`; it is reusable as an algorithmic pattern but
not as a g760 result.

There is no named fresh-g760 H2 or pentagon difference constructor.  The
smallest correct constructor for every block is

```text
delta_R(c) = reduce_word(R(reduce_word(g760+c)) + inv_word(R(g760)))
Sigma_R(c) = Fox(delta_R(c))
```

so the v110 convention is corrected-minus-base and the corrected defect is
`T_R + Sigma_R(c)`.  The opposite sign must be a destructive test.

Negative letters are differentiated literally.  The flat left-Fox engine at
`search/d972_b345_seedspan_triple4_v1.py:1105-1150` advances the prefix by the
inverse generator and then adds coefficient 2.  The expression evaluator at
lines 3891--3926 applies the product rule and, for an inverse node, left
translates by the inverse value and multiplies by 2.  Thus no inverse
occurrence is moved to a different position.

The fixed right-correction prefix transports are:

- H1: write the native relation as `C B^-1 A`, where
  `A=f(x,y)`, `B=f(x,z)`, `C=f(y,z)`.  Task 172 lines 67--76 give
  `L_C(grad c-grad b)+L_H1 grad a`, retaining the literal base value
  `H1=C B^-1 A` even when it is identity in E4.
- H2: write the native relation as `C B^-1 A^-1`, where
  `A=f(u,x)`, `B=f(x,y)`, `C=f(u,y)`.  Literal product/inverse expansion gives
  `L_C(grad c-grad b)-L_(C B^-1) grad a`.  No named fresh-g760 export of these
  prefixes exists; it must be generated by the generic expression evaluator
  and independently checked against the direct difference word.
- A.18: v93, Theorem 2.1, gives the right derivative
  `q1*lambda1 + q1*q2*lambda2 + q1*q2*q3*lambda3
  - q1*q2*q3*lambda5 - q4*lambda4`, with the `b_i` order above.  The generic
  evaluator can produce the raw full-E4 prefixes, but no fresh-g760 routine
  currently exports all five prefix blobs.  They must be rebuilt and compared
  with v93 plus a final-prefix mutation.

No rho shortcut is callable as a replacement for these five factors.  V96
has only the simultaneous shear
`D_A18 = D_rho - D_H1 - A*D_H2`; omitting either hexagon component changes the
system.

## 3. Typed context registry

### 3.1 Authenticated registry

The authenticated task-157ee receipt is
`ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json`
(receipt SHA-256
`1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df`).
Its registry has:

```text
context_count                    31
named_use_count                  46
deduplication                    exact E4 pair equality
context_rows_sha256              bf07578f91f5ed66e6ddddd4ef83dafa45817a29df066940bbc13bd53cdd00f6
named_use_mapping_sha256         15cdac950ede8ce4596e5014ae1b6d0caa28523898cb42f3387f435a11b919a8
```

The producer registers a new row only after exact equality of the two typed
E4 `EKey` values (`search/d972_b345_seedspan_triple4_v1.py:2800-2817`) and
serializes their complete left/right blobs at lines 2857--2869.  The
helper-independent reconstruction is
`search/check_d972_b345_seedspan_triple4_v1.py:903-962`.  No name-based dedup
was used.

### 3.2 Eleven f-occurrence bindings

The two relation blocks plus five A.18 evaluations contain eleven literal
occurrences of `f`.  Source H1/H2 live in E3; the current 31-row registry is
E4-only.  Therefore their `registry id` is genuinely absent, not zero.
The final column records the task172 coface-0 E4 diagnostic binding; it must
not be silently substituted for the source-E3 row.

| block/slot | sign and source pair | source evaluator | 31-id / all 46-table names | coface-0 E4 diagnostic |
|---|---|---|---|---|
| H1/1 | `+ (x,y)` | `f2_substitute -> embed_f2_pb3 -> e3.eval` | none | id 1: `correction_coface_0`, `hexagon_1_fxy_0`, `hexagon_2_fxy_0`, `pentagon_part_1` |
| H1/2 | `- (x,z)` | same | none | id 2: `hexagon_1_fxz_0` |
| H1/3 | `+ (y,z)` | same | none | id 3: `hexagon_1_fyz_0` |
| H2/1 | `- (u,x)` | same | none | id 4: `hexagon_2_fux_0` |
| H2/2 | `- (x,y)` | same | none | id 1: `correction_coface_0`, `hexagon_1_fxy_0`, `hexagon_2_fxy_0`, `pentagon_part_1` |
| H2/3 | `+ (u,y)` | same | none | id 5: `hexagon_2_fuy_0` |
| P/1 (`b1`) | `+ phi234`, map `[[4],[5],[6]]` | `e4.eval(f,[g4,g6])` | id 1: `correction_coface_0`, `hexagon_1_fxy_0`, `hexagon_2_fxy_0`, `pentagon_part_1` | same row |
| P/2 (`b2`) | `+ phi1_23_4`, map `[[1,2],[3],[5,6]]` | `e4.eval(f,[pp(g1,g2),pp(g5,g6)])` | id 27: `pentagon_part_3`, `source_middle` | same row |
| P/3 (`b3`) | `+ phi123`, map `[[1],[2],[4]]` | `e4.eval(f,[g1,g4])` | id 21: `correction_coface_4`, `hexagon_1_fxy_4`, `hexagon_2_fxy_4`, `pentagon_part_0`, `source_ff` | same row |
| P/4 (`b5`) | `- phi12_3_4`, map `[[2,4],[3,5],[6]]` | `e4.eval(f,[pp(g2,g4),g6])` | id 26: `pentagon_part_2`, `source_f1234` | same row |
| P/5 (`b4`) | `- phi1_2_34`, map `[[1],[2,3],[4,5]]` | `e4.eval(f,[g1,pp(g4,g5)])` | id 28: `pentagon_part_4` | same row |

Here `g1,...,g6` are the lexicographically ordered PB4 marks
`a12,a13,a14,a23,a24,a34`.  The exact E4 context construction is at
`search/d972_b345_seedspan_triple4_v1.py:2819-2842`; the direct E4 relation
evaluation is at lines 2729--2772.

Within a new source-E3 namespace, H1/1 and H2/2 may share one row only after
the rank tag and both 40-byte E3 blobs are compared.  The five other named
hexagon occurrences reduce to four more unique E3 pairs, so the all-seven
context state has five unique E3 rows plus five unique E4 pentagon rows.  No
E3 row may deduplicate with E4 id 1 merely because a coface name matches.

### 3.3 Does the task-157ee kernel kill every required context?

No, not visibly from the current serialized bindings.

`JointGroup.eval` in
`search/d972_b345_joint_kernel_qstar_closure_v1.py:204-247` is exactly

```text
( e3.eval(embed_f2_pb3(w)),
  tuple(e4.eval(w,[left,right]) for all 31 registered E4 pairs) ).
```

Consequently its kernel visibly kills:

- the source-E3 `(x,y)` row, hence both occurrences using that exact pair;
- every pentagon row id `1,21,26,27,28`; and
- the E4 coface-0 diagnostic rows `1,2,3,4,5`.

It does **not** directly include the source-E3 pairs `(x,z)`, `(y,z)`,
`(u,x)`, or `(u,y)`.  Killing their coface-0 E4 images would imply the E3
identities if a typed finite deletion were serialized as a left inverse, but
the selected q3 artifact has empty `maps.cofaces_3_4` and
`maps.deletions_4_3` arrays and
`endpoint_retractions.status = BYPASSED_BY_EXACT_WORD_CORRECTION`.  The prose
construction record is not a callable map.  No executable pinned symmetry
was found that supplies the four identities, and H2 is therefore not inferred
from H1.

The exact first missing edge is:

```text
E3_CONTEXT_KERNEL_BRIDGE:
  a serialized matched-quotient homomorphism d:E4->E3 for the chosen coface,
  direct generator/blob proof d o coface0 = id_E3,
  and direct replay for (x,z),(y,z),(u,x),(u,y).
```

Alternatively the joint map and its complete normal-presentation roster must
be rebuilt with those four E3 factors included.  That creates a different,
smaller kernel and cannot be advertised as the existing task-157ee `N`.

## 4. Raw targets, Fox boundaries, and direct replay

### 4.1 Common base and raw constructors

The independent g760 constructor is
`search/check_d972_r07_616_to_760_commutator_affine_rhs_v3.py:127-134`.
It gives one word of length 760, exponent sums `[0,0]`, and signed-word digest

```text
518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d.
```

The v3 report records that the settled-kernel word relating g760 to its
616-letter parent is identity in the complete E3 source and all five complete
E4 cofaces, hence that the two bases have equal settled values.  It does not
export the new all-seven raw rows.  A successor must reconstruct g760 and
replay the relations itself.

The callable raw constructors are:

| output block | base raw target | correction/change row | direct replay |
|---|---|---|---|
| H1/E3 | `Fox(embed_f2_pb3(hexagon_words(g760)[0]),e3)` | direct `delta_H1(c)` above; compare with the three literal prefix transports | `e3.eval(embed_f2_pb3(hexagon_words(g760+c)[0])) == 1` |
| H2/E3 | same with index 1 | direct `delta_H2(c)`; compare with the fresh H2 prefix formula | same with index 1 |
| P/E4 | `Fox(pentagon_word(g760),e4)` | direct `delta_P(c)`; compare with all five v93 right prefixes | evaluate all five factor blobs and prefix products, then the exact noncommutative `b1*b2*b3*b5^-1*b4^-1`; also compare with `e4.eval(pentagon_word(g760+c))` |

`fox_gradient_without_sections` supplies each raw row and quotient value
(`search/d972_b345_seedspan_triple4_v1.py:1126-1150`).  `d1` and left
translation are lines 1153--1166.  The direct relation evaluator at lines
2729--2772 and the typed expression builder at lines 9373--9402 are useful
patterns, but both are E4/historical-base lanes rather than a source-E3
all-seven certificate.

### 4.2 Sparse typing and canonical serialization

An element is `EKey=(permutation_bytes,pc_coordinate_bytes)`, and
`_element_blob(value)=value[0]+value[1]`
(`search/d972_b345_seedspan_triple4_v1.py:2796-2797`).  From the pinned q3
artifact:

```text
E3: coarse degree 36 + PC rank 4  = 40-byte element blob
E4: coarse degree 144 + PC rank 10 = 154-byte element blob
```

Thus H1 and H2 have three C1 components each, while P has six.  Coefficients
are in `{1,2}` modulo 3 and zero entries are omitted.  The existing E4 binding
sorts by component and exact element bytes and hashes
`component-u8 | blob-length-u16le | blob | coefficient-u8` at
`search/d972_b345_seedspan_triple4_v1.py:4103-4118`.  The 157em/en public
semantic key is `(component,canonical 154-byte E4 blob)`.

The integrated successor must use an ordered direct sum, for example

```text
(block_tag, component, element_blob) -> coefficient,
block_tag = 1:H1/E3, 2:H2/E3, 3:P/E4,
```

serialized in block/component/blob order.  The block tag is load-bearing:
an H1 coefficient may not cancel an H2 coefficient merely because the source
context and component agree.  Each pentagon factor also retains a separate
occurrence ledger even though its final row is in the single P block.

### 4.3 D1 and D2

For H1/H2, the raw presentation constructor is

```text
[ Fox(r,e3) for r in pure_relations(3) ]
```

followed by all E3 left translations.  The frozen rows are the two signed
PB3 relators

```text
[-1,2,1,2,3,-2,-3,-2]
[-1,3,1,2,-3,-2]
```

and the C1 component count is three.  Existing sources replay their quotient
values and `D1=0`; that proves only that their translated span is contained in
the true presentation boundary.

No required-chain proof note was found which identifies the normal closure of
these two frozen rows with `ker(F3 -> P3)` at the same exact boundary grade as
v108.  Reports describing a recursive Fadell--Neuwirth presentation and
faithful Artin replay are strong inputs, but relator replay alone is the
`M subset M_true` direction, not presentation equality.  Therefore the PB3
span is not labelled exact here.

The smallest gate can reuse v108 rather than duplicate its whole proof:

1. give signed-word certificates that the chosen PB3-to-PB4 coface and a
   PB4-to-PB3 deletion descend between the frozen two- and eleven-relator
   presentations;
2. prove their composite is the identity on all three marked generators;
3. combine the resulting split presentation map with v108's
   `F6/<11 rows> = P4` and the ordinary pure-braid insertion/deletion
   retraction.

Equivalently, a short rank-3 Fadell--Neuwirth/Tietze paper proof plus the
already available independent Artin-action replay is sufficient.  Either
route should end in an explicit `PB3-PRES-EQ` theorem before the H1/H2 D2
image is called true.

For P, the callable base constructor is
`search/d972_b345_target6_dual_colgen_v2.py:1921-1929`; it creates all eleven
raw PB4 columns and checks quotient identity and `D1=0`.  Lines 1932--1974
independently compare direct occurrence translation with typed left
translation.  V108, Theorem 4.1 and Section 5, proves that the eleven-relator
normal closure is exactly the marked PB4 kernel, so this translated D2 image
is exact.

PB4 exactness does not repair the source-PB3 block without the split
presentation gate above.  Replacing H1/H2 by their coface-0 E4 versions would
produce a different all-E4 specialization, not the PB3/PB4 stack specified in
v110.

## 5. What task 157ee--157en actually supplies

| shelf lane | reusable authenticated object | boundary for this task |
|---|---|---|
| 157ee/157ef | 26 signed correction records; exact 243-state joint image; compact complete normal-presentation data with 6,318 Cayley-edge, 104 x/y-action, and 19 Q0-factor relations; 31/46 E4 registry; cross-checked run 32359956713 | joint map has only one E3 evaluation; it does not visibly kill the four extra source-E3 contexts |
| 157eg/157eh | raw full-E4 D2/correlation machinery and a cross-checked ACTIVE translated-column diagnostic | not a target solution and not an H2/pentagon bridge |
| 157ei--157el | target6 lex-block construction and checker/accounting repairs | target ordinal 6 only; historical base and prefix |
| 157em | canonical 154-byte E4 keys, eleven-row complete blocks, recovery/serialization, and independent full-D2 checker design | target6 only; no source-E3 block |
| 157en | version-2 target6 producer/checker sources and the producer artifact from run 32458556448 | producer terminal is `...UNKNOWN_RESOURCE` (`common_math_soft_deadline_seconds`), receipt SHA `54e795e0411af5cc5194ebad10235363e16623f06a4e11db475e638fcb783135`, 14,603,356 bytes; it remains target6-only and supplies no all-seven result |
| task 172 v2 (historical failure) | fresh g760 target6 formula, 26-word/6,441-row reconstruction, and all eleven PB4 raw rows | historical fail-closed terminal `UNKNOWN_INPUT:FOX_CANARY`; it stopped after 36 pairs at Q0 relator 17 and is superseded by v7, not the current shelf |
| task 172 v7, Sol audit v119 (commit `d22a3a63`) | current cross-checked bounded target6 raw bridge: 26 records, 6,441 reconstructed relation words, eleven PB4 rows, g760, 101 actual conjugation transcripts, and five same-context pairs | terminal `R07_FULL_E4_ORBIT_PREFLIGHT_READY`; accepted only for a target6 context census and independently replayed full-orbit successor; no orbit calculation, correction, all-seven solve, literal A.18, cofinal lift, fake, or Ihara witness |

The current task-172 v7 shelf is exactly:

```text
92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed  search/d972_r07_full_e4_joint_orbit_preflight_v7.py
e3917ec05b95b8996e3a5cec1cc2bfde51c3ed8c6972175fd9be9e1178205c23  crosscheck/check_d972_r07_full_e4_orbit_preflight_v7.py
86c6f3a72a3f852a1be7c5323bf72c7ad987377fd5483b6e32528fe263e290ff  search/certs/d972_r07_full_e4_orbit_preflight_v7_20260827.json
62ab78ecf0f832452d2a8e4e929cbc142188f0ba08c9751cc06e9eec026204e2  sol/luna_reply_172_r07_full_e4_orbit_preflight_repair_v7.md
```

Its target formula, expanded-roster constructor, and canary are respectively
at producer lines 67--81, 82--108, and 109--173.  V119 accepts all 101/101
actual Fox rows in the layer split `35+33+33` and five distinct-conjugate,
same-three-context pairs.  This is a limited target6 promotion, not an
all-seven Fox certificate.  V119 also leaves two successor debts: semantic
mutations must traverse the full independent replay, and a separately
labelled actual-product additivity canary is still absent.  The all-seven
checker specified below must close both rather than inheriting them as PASS.

## 6. Minimal integrated successor

The smallest bounded successor should create only a versioned producer,
helper-independent checker, immutable receipt, and reply, for example:

```text
search/d972_r07_all_seven_raw_bridge_preflight_v1.py
crosscheck/check_d972_r07_all_seven_raw_bridge_preflight_v1.py
search/certs/d972_r07_all_seven_raw_bridge_preflight_v1_20260827.json
sol/luna_reply_174_r07_all_seven_raw_bridge_preflight_v1.md
```

It should perform the following bounded work, in this order.

1. Pin and independently reconstruct the one g760 word.  Select one
   deterministic, fully typed signed correction word `c` from the expanded
   normal roster, record its layer/ordinal/free-word SHA, and use exactly
   `f1=reduce_word(g760+c)` in H1, H2, and all five pentagon occurrences.
2. Build a typed registry with five unique source-E3 pairs and the five E4
   pentagon rows.  Preserve all eleven occurrence aliases.  Either construct
   and directly certify the finite coface/deletion retraction or stop at
   `UNKNOWN_INPUT:E3_CONTEXT_KERNEL_BRIDGE`.
3. Construct the three raw base targets and the three
   `R(f1) R(g760)^-1` change words.  Compare every direct Fox gradient with
   its literal prefix formula.  Serialize one stacked sparse row with the
   block tags above.
4. Run at least 110 actual conjugation canaries (at least ten for each of the
   eleven named f-slots), stratified across all three roster layers and using
   nonempty conjugators.  Each canary compares direct Fox evaluation of
   `u r u^-1` with slotwise left translation by the full typed context state.
   The H2 and both inverse pentagon slots must be represented independently.
5. Include nontrivial same-context/different-conjugate tests: find at least
   two pairs `u != v` with equal complete five-E3-plus-five-E4 state, require
   the freely reduced conjugates to differ, and require equality of the full
   tagged H1/H2/P row.  Reusing `v=u` or comparing only registry IDs is a
   failed test.
6. Replay `H1(f1)` and `H2(f1)` literally in E3.  For the pentagon, serialize
   all five E4 factor values and the four intermediate prefix products, then
   replay `b1*b2*b3*b5^-1*b4^-1` without commuting.  Compare this with the
   direct `pentagon_word(f1)` evaluation.  Mutate the two negative factors,
   one coface slot, and correction side.
7. Build two PB3 and eleven PB4 raw D2 columns and check every value and D1.
   Mark PB4 exact by the pinned v108 theorem.  Mark PB3 `UNKNOWN_PRESENTATION`
   until the separate exact split-presentation/paper gate is pinned.  Do not
   run a D2 orbit, column-generation, or all-seven solve.

The checker must import neither the producer nor its word/Fox/context helpers.
It should independently rebuild free reduction, paper product, the two
hexagons, all five cofaces, the pentagon, E3/E4 arithmetic, the 31/46 table,
the expanded roster, left Fox, D1, both raw D2 rosters, block serialization,
all canaries, and direct relation products.  Required destructive controls
include correction-left/right, corrected/base sign, H2 `u/z`, inverse Fox
prefix, pentagon negative-factor order, coface 1/3 swap, E3/E4 rank/blob swap,
context-name-only dedup, and dropped block tag.

Objects which may be reused by authentication are the q3 artifact and
collectors, g760 signed word, 26 correction records, 157ee compact
presentation, 31/46 E4 rows, generic producer-side quotient/Fox primitives,
the eleven PB4 rows, and v108.  Objects which must be fresh are the five-row
source-E3 context registry, finite retraction binding, H2 and pentagon g760
right-difference constructors, all five pentagon prefix blobs, tagged stack,
all-slot canaries, direct seven-evaluation replay, PB3 exactness gate, and the
helper-independent checker.

No full-orbit runtime estimate is made from this bounded inventory.

## 7. Final boundary

The finite missing edges are narrow enough that writing the bounded preflight
is a GO.  Promotion past its input gate is a STOP until both
`E3_CONTEXT_KERNEL_BRIDGE` and `PB3-PRES-EQ` are exact.  Even after those
pass, the preflight would authenticate inputs only; v110's orbit image,
stacked selector, materialized common correction, and direct final replay
would still require a separate production computation and independent
checker.

```text
static callable inventory only
target6 alone is not the all-seven common-word system
PB4 exactness is not silently transferred to PB3
no all-seven solve / cofinal lift / fake / Ihara witness declared
```
