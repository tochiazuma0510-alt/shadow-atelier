# Luna task 157ed — complete triple-cube raw-lambda census at the fixed B345 prefix

## 0. Role, objective, and hard boundary

You are Luna, the implementation/cross-checking engineer.  Implement one new,
versioned, positive-information lane which answers the following finite
question and no larger one.

> For the exact fixed D2 prefix and support-one target-6 functional certified
> by cross-checked run 32326652060, which of the complete ordered
> `26^3 = 17576` literal triple products of the authenticated q3 cube words are
> typed correction directions, and what is the scalar of each direction under
> that functional?

This is a **complete scalar census**, not a full-vector affine solve.  If a
typed tuple has nonzero scalar, emit only the canonical first-active handoff
record after finishing the complete census.  Do not absorb that column into a
109-variable system, do not continue the 33 acceptance targets, and do not
emit a literal GT witness in this task.

If every typed tuple has scalar zero, the only negative conclusion is that the
same support-one dual still obstructs the affine span of the old 108 columns
and all typed words in this exact ordered-triple universe **against the same
fixed prefix**.  Never promote that statement to full D2, full H3, all
depth-three corrections, an actual nonmembership theorem, B4-A, or B4-B.

The implementation must be fail-closed.  Cache limits affect performance only;
semantic limits produce `UNKNOWN_RESOURCE`; authenticated external input drift
produces `UNKNOWN_INPUT`; an internal convention, prefix, rank, dual, ordering,
or formula mismatch is a hard failure.

## A. Frozen evidence and mandatory pins

The predecessor result is cross-checked and immutable:

- GHA run: `32326652060`;
- receipt SHA-256:
  `d556a3e579390ae09ea005d1de94b0d2f88b5ed5f9c5d230034b316afe45fc8d`;
- receipt size: `1043815` bytes;
- terminal/reason:
  `B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE / affine_system_inconsistent`;
- producer runtime: `530.736960599` seconds;
- producer peak RSS: `744943616` bytes;
- complete job/run-step times: `1135` / `1077` seconds;
- checker: PASS.

Pin these exact predecessor files:

| dependency | SHA-256 |
|---|---|
| `search/d972_b345_seedspan_triple4_v1.py` | `fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29` |
| `search/check_d972_b345_seedspan_triple4_v1.py` | `ef5125e3b7e328ce8aa8cfd4c36d0937e28f44a480188fcd4ed01a37eb80b981` |
| `search/d972_b345_seedspan_triple4_gha_driver_v1.g` | `a9c88540c1abdb21dc214d4d4e6461c1431dc407f93542c49e0e65a14788fca4` |
| `sol/luna_task_157ec_b345_seedspan_triple4.md` | `1173f2f8ce6ad899fe5bee6c2a42d7cb6686073306a7e3fd1e17acf0007f89b2` |

Retain and independently gate every q3, formula, v9, 157eb, and strong-prefix
pin already frozen by 157ec.  In particular:

- q3 artifact SHA:
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`;
- strong-prefix source SHA:
  `d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be`;
- old-104 seed digest:
  `e99602b0981251e4bb81ab0d2113791563bc9ec9df2a45828aea2880ec6d2f9e`;
- 26-cube digest:
  `3d26302d01b3c202350fdb8b9ea81badeaf9c62913c9e94be7e049ad7c391463`.

The run id and predecessor receipt SHA are provenance pins, not imported
proof.  Do not read a local copy of the predecessor receipt, import its basis,
or trust its rows.  Reconstruct the q3 quotients, fixed prefix, old 108 words,
target-6 matrix, and support-one functional fresh in the new producer and
independently in the checker.

The fresh reconstruction must reproduce exactly:

```text
prefix columns             362725
prefix pivots              362709
prefix dependent columns       16
prefix live sparse entries 3090367
prefix row-tail visits      2727658
BFS translations             32768
directed translations          207
unique context count             31
named occurrence count           46
31-context rows SHA
  bf07578f91f5ed66e6ddddd4ef83dafa45817a29df066940bbc13bd53cdd00f6
46-name alias mapping SHA
  15cdac950ede8ce4596e5014ae1b6d0caa28523898cb42f3387f435a11b919a8
target-6 coordinate count     33687
old-104 target-6 rank            50
old108+new4 target-6 rank         54
variables                       108
nullity                           54
target-6 row-space SHA
  5dd0bd3411afae0a9adafca4254b6fda739774a8b970b59e661d67e686f549be
base remainder size              184
base remainder SHA
  e62a581658c1a7c6093d9e3e5155acf503731806c075cf1dd3937e336473e179
all-108 annihilation SHA
  400f67f74b1250e538c395aa8bf647f6f7432ec07fe2582aaff06e5a47fe7ed5
dual support count                  1
dual support SHA
  f8b1cb6325b158f0984ca945dac2c0e915e0386e1f13ddb911acf0e4e2d9dcad
```

The unique dual equation label is exactly

```text
[6,"hexagon_1_coface_0",4,
 "0801040503000602070b0e0c110a090d0f10181a161315191412171e1b2322201d1c1f212625242c2b2a2928273534333231302f2e2d3e363738393a3b3c3d403f474645444342414c4d4e4f5048494a4b5251595857565554535a5b5c5d5e5f60616265666768696a6b63646c6d6e6f707172737476757d7c7b7a797877867e7f80818283848588878f8e8d8c8b8a8900000002020100000000"]
```

Its coefficient is `1`; its component is one-based component `4`; its E4 blob
is 144 canonical permutation bytes followed by 10 PC bytes (154 bytes,
308 hex characters).  Require `normalized_rhs=1`, `yTz_mod3=2`, target
boundary `[6]`, and `target6_fixed_prefix_functional=true`.  Mutating the
component, one hex nibble, width, target name, sign, or normalization must be a
hard failure.

## B. Exact ordered universe

Reconstruct the cube words exactly as in 157eb/157ec:

1. Visit the authenticated 27 correction-fibre records in record order.
2. Skip the unique empty word.
3. Form a cube by literal threefold concatenation followed by free reduction.
4. Deduplicate cubes in first-occurrence order and require exactly 26 cubes and
   the frozen cube digest above.

Require the 26 reduced cube lengths to sum to `9162`; consequently the exact
unreduced letter count over all ordered triples is
`3*26^2*9162=18580536`.  These are universe bindings, not estimates.

The census universe is the Cartesian product

```text
(i,j,k) in [1..26] x [1..26] x [1..26]
```

in exact lexicographic nested-loop order: `i` outermost, `j` middle, `k`
innermost.  Its one-based ordinal is

```text
((i-1)*26 + (j-1))*26 + k.
```

Repeated indices are literal and load-bearing.  Do not sort a tuple, quotient
by cyclic/permutation symmetry, or collapse two different tuples because they
reduce to the same word.  The literal correction expression is the ordinary
left-to-right product

```text
s_ijk = reduce(cube_i * cube_j * cube_k).
```

Caching by a unique reduced-word class is permitted, but the public census
must retain all 17,576 tuple ordinals and an exact tuple-to-word-class mapping.
Record the unique-class count and a packed mapping/digest; never replace tuple
completeness by only a set of word hashes.

For each tuple classify, in order, whether it is a typed affine direction.
The exact **typed** gates, and therefore the only values permitted in the
public first-failure code table, are:

1. exponent sums `(0,0)`;
2. E3 identity under `x -> A12`, `y -> A23`;
3. the six source images of `f0*s_ijk` equal the frozen source tuple;
4. the correction evaluates to identity in all 31 exact E4 context pairs and
   all 46 named correction occurrences used by the 33 acceptance roots;
5. the target-6 quotient value is identity.

Use this closed first-failure table: `0=typed`,
`1=exponent_sums`, `2=E3_identity`, `3=marked_source_tuple`,
`4=context_identity`, `5=target6_value`.  No other code is permitted.

Every tuple remains in the census even if a gate fails.  Give it the first
failed typed-reason code and a null lambda code.  The typed universe is exactly
the ordered tuples which pass every gate.  Do not silently discard an empty
reduction, duplicate word, repeated-index tuple, or failed context.

The raw-Fox formula/direct comparison is **not** a sixth typed predicate.  It
is an internal convention theorem.  Prove it on bounded production canaries
(the empty correction, all 26 cube leaves, all 26 literal squares, the four
frozen 157ec triples, and the first and last typed tuple if they exist) by two
independently built routes.  Any value, action, sign, product-order, or
formula/direct drift is a hard failure; it must never be encoded as an untyped
tuple or an `UNKNOWN_*` result.  The complete census uses the theorem-backed
streaming formula below, not a per-tuple flat replay.

Gate 3 is also not shorthand for a product of three correction values.  Build
the single typed word-expression `f=f0*s_ijk`, evaluate it in the six frozen
source contexts

```text
ff      = f(g1,g4)
g       = f(g1,g2)
gs      = f(g4,g5)
f1234   = f(g4*g2,g6)
h       = f(g2*g1,g3)
middle  = f(g2*g1,g6*g5),
```

where every displayed product is the frozen left-to-right quotient product,
and reconstruct the actual six marked PB4 source images, including every
inverse and conjugation, in the frozen order:

```text
S1 = g1
S2 = g^-1 g2 g
S3 = ff^-1 h^-1 g3 h ff
S4 = ff^-1 g4 ff
S5 = ff^-1 middle^-1 gs^-1 g5 gs middle ff
S6 = f1234^-1 g6 f1234.
```

These are the exact six frozen evaluations of the same typed `f0*s_ijk`
construction used by 157ec.  Compare the resulting six-tuple with the
authenticated `raw_source_key`.  A simple
`cube_i*cube_j*cube_k` value check is necessary for the context gates but is
not a replacement for this marked-source DAG replay.

## C. Fresh prefix and the portable support-one raw lambda

Let `B` be the freshly rebuilt fixed prefix basis and `NF_B` its canonical
normal-form reducer.  Let

```text
qstar = (component 4, frozen E4 blob above).
```

The support-one functional is

```text
lambda_B(v) = coefficient of qstar in NF_B(v), in F3.
```

This is the exact specialization of the 157ec dual.  Rebuild the old 108
target-6 columns and prove directly:

```text
lambda_B(delta_k) = 0 for k=1..108
lambda_B(z)       = 2
lambda_B(-z)      = 1
```

Do not infer those values from the predecessor JSON or a digest.  The producer
and checker must each recompute them.

Instrument the fresh prefix construction with a versioned, semantics-neutral
`add_column` wrapper.  It must copy each original translated packed column
*before* elimination and, exactly when that column reduces to zero, retain one
dependent-event record.  Require exactly 16 records, in original column
order.  Each record contains:

- BFS/directed schedule kind and exact translation ordinal;
- translation element as the canonical 154-byte E4 blob, never a pool id;
- relator index;
- the complete original raw packed column, sorted by
  `(component,canonical-E4-blob)`, as triples
  `(component,154-byte-blob,coefficient-in-{1,2})`, together with support,
  byte length, and SHA-256.

The wrapper may observe but must not change column order, pivot selection,
normalization, provenance-DAG operations, section bindings, or the frozen
`362725/362709/16` result.  After the final basis is immutable, replay every
saved original column and require both `NF_B(column)=0` and
`lambda_B(column)=0`.  A changed dependent event, translation/relator
binding, raw column, or count is a hard failure.  A count alone is not an
annihilation certificate.

Implement a portable raw-key oracle without reducing and retaining a complete
candidate remainder.  Freeze the element pool at `prefix_pool_checkpoint`
immediately after the last prefix column.  With the fixed canonical pivot
order, every normalized pivot row
has the form

```text
e_p + sum_{h>p} a_h e_h.
```

Define recursively

```text
lambda_key(h) = 1  if h=qstar is nonpivot
                0  if h is another nonpivot
               -sum_{u>h} a_u lambda_key(u)  if h is a pivot.
```

Construct the pivot table once by reverse canonical dynamic programming.  The
semantic key is always

```text
(one-based component, exact 154-byte canonical E4 blob).
```

Insertion-order pool ids are not equality, order, receipt, or cross-process
keys.  They may be used as a local compact index only for immutable ids
strictly below `prefix_pool_checkpoint`.  For a census query, first compare
the canonical key with `qstar`; otherwise perform a read-only lookup in the
frozen prefix blob-to-id map.  A blob absent from that map, or present but not
a pivot in that component, is a nonpivot and has value zero.  **Do not intern
it.**  Never retain an id-keyed query result across a pool rollback, never
roll back below the prefix checkpoint, and never let candidate values extend
the semantic prefix map.

The implementation must gate:

- `qstar` is a canonical nonpivot;
- every recursive edge strictly increases the exact pivot key;
- all coefficients are reduced mod 3;
- every pivot row has lambda zero;
- all 16 dependent prefix columns have lambda zero after exact reduction;
- the resulting raw oracle agrees with direct `qstar` extraction after
  `NF_B` on the base, all 108 old columns, all 26 cube leaf canaries, all 26
  square canaries, and all four frozen 157ec triple words.

`raw_lambda_oracle_entries` counts the immutable pivot-lambda table plus the
explicit qstar entry; require exactly `362709+1=362710`.  It does not count
transient nonpivot queries.
`raw_lambda_recursion_edges` counts row-tail coefficient visits.  The frozen
source evidence is `3090367-362709=2727658` such visits, below the registered
cap, but both sides must recompute the count.  Optional query-result caches are
bounded, evictable performance caches and may cold-recompute zero or pivot
lookups without changing a terminal.

Serialize a deterministic oracle/proof binding: qstar label, prefix digests
and counts, recursion algorithm/version, pivot-table count, row-tail visit
count, memo accounting, pivot/dependent annihilation counts and zero-vector
digests, old-108 zero digest, and the base/RHS values.  Its semantic digest is
over the complete list of `(component,canonical-blob,lambda)` pivot entries,
sorted by canonical pivot order, followed by qstar; it is never over numeric
pool ids or a cache/access trace.  Query calls/hits/misses are performance
accounting only and need not coincide between different exact checker
organizations.  A hash alone is not the proof; the checker must rebuild the
rows and recompute the values.

This remains a functional on the quotient by the **fixed prefix**.  Do not call
it a full-D2 functional or claim E4-action invariance beyond the exact left
translations actually queried by this census.

## D. Exact noncommutative DP — no long target flattening

The producer must not flatten 17,576 long target expressions or reevaluate
each triple letter by letter in 46 occurrences.  Precompute the 26 cube leaves
and the 26^2 ordered pairs, then stream the third factor.  Tuple completeness
and first-PASS order may not change.

For every required substitution/context, retain exact quotient values and use
the frozen left-Fox product law

```text
value(uv) = value(u) value(v)
D(uv)     = D(u) + value(u) . D(v).

D(abc) = D(a) + value(a).D(b)
                  + value(ab).D(c).
```

The action is the exact existing left translation on `(component,E4-key)`.
Individual cube values are generally nonidentity.  Therefore the shortcut

```text
D(abc) = D(a)+D(b)+D(c)
```

is forbidden even when the total triple value is identity.  The selftest must
contain a nonabelian example where all three prefix actions matter and the
forbidden shortcut gives the wrong scalar.

The 46 named occurrences are an exact alias table onto the 31 unique context
ids; they are not 46 independently evaluated words.  Rebuild and pin both the
31 context rows and the complete 46-name-to-context-id mapping.  For each
context precompute 26 cube values and 676 ordered-pair values, then stream the
third value.  Every named occurrence must read the value of its bound context
id and be checked in named order.

For target 6 retain the exact 157ec notation

```text
A = f0(x,y),  B = f0(x,z),  C = f0(y,z),  h = C B^-1 A = h1(f0),
a = s_ijk(x,y), b = s_ijk(x,z), c = s_ijk(y,z).
```

The raw difference is not an unspecified target replay; it is exactly

```text
Delta_ijk = L_C(D(c)-D(b)) + L_h(D(a)).
```

For each substitution `t in {a,b,c}`, if `v_t(r)` and `D_t(r)` denote the
value and raw gradient of cube `r`, compute

```text
D_t(cube_i cube_j cube_k)
 = D_t(cube_i)
 + L_{v_t(cube_i)} D_t(cube_j)
 + L_{v_t(cube_i)v_t(cube_j)} D_t(cube_k).
```

Thus the scalar scan may retain the 26 leaf gradients, the 26 leaf values and
676 pair **values** for each of the three substitutions.  It must not retain
676 full sparse pair gradients.  Apply the outer `L_C` or `L_h` before each
`lambda_key` lookup.  This is the required 26/676 precomputation plus one
streamed third-factor scalar evaluation per tuple; it is not an additive
shortcut and it never constructs a flattened target word.

For lambda evaluation, stream raw gradient terms through `lambda_key`; do not
materialize a full 33,687-coordinate remainder for each tuple.  A translated
raw key must be formed by the exact quotient multiplication convention before
the oracle lookup.  Cache keys must include every semantic input: occurrence,
component, exact left multiplier, cube/pair identity, and raw E4 key.  LRU
eviction may cause cold exact recomputation only; it may not reject a tuple,
change its scalar, or produce `UNKNOWN_RESOURCE` merely because a cache is
full.

For target 6, compute the exact raw difference

```text
Delta_ijk = rawFox(target6(f0*s_ijk)) - rawFox(target6(f0)).
```

with the 157ec formula/product orientation, and store

```text
lambda_ijk = lambda_B(Delta_ijk) in {0,1,2}
```

for typed tuples.  Coefficient `2` means two literal copies in the F3 affine
span, never an inverse.  For a nonzero scalar the coefficient that solves only
the current qstar equation is `lambda_ijk^-1` (`1 -> 1`, `2 -> 2`).  This is a
handoff hint, not a full solution.

The checker must independently implement the DP/oracle route.  It may use a
different exact streaming organization, but it must not import producer
helpers, packed arrays, pool IDs, booleans, or scalar digests.  Require exact
producer/checker equality for every one of the 17,576 tuple classifications
and lambda codes.

## E. Complete scan, packed receipt, and first-active rule

Scan all tuples even after finding a nonzero scalar.  Freeze the first active
typed tuple by the registered ordinal, but continue through ordinal 17,576.
The first-active record must contain:

- ordinal and `(i,j,k)`;
- correction-fibre record positions and cube indices;
- reduced-word class id, reduced length, and SHA-256;
- all typed gate receipts/digests;
- scalar `1` or `2` and its qstar-equation coefficient inverse;
- exact source tuple/context binding;
- no full remainder, affine solution, or acceptance claim.

Use compact, lossless public arrays.  At minimum include:

- a 17,576-bit typed mask;
- fixed-width lambda codes (`0,1,2`, plus a distinct null/untyped code);
- fixed-width first-failure reason codes;
- tuple-to-word-class ids or a lossless packed equivalent;
- exact byte lengths, bit widths, padding-bit-zero gates, code tables, order,
  SHA-256 for each decoded array, and counts by type/scalar/reason;
- the first-active ordinal or null;
- a complete-scan flag and last ordinal `17576`.

For full or committed-prefix decoded length `n`, encode the typed mask LSB
first in exactly `ceil(n/8)` bytes; all unused high bits of its last byte are
zero.  Encode lambda as exactly `n` bytes with
`0=scalar0,1=scalar1,2=scalar2,255=untyped`, and first failure as exactly `n`
bytes with the closed codes `0..5` above.  Gate typed-mask/code agreement in
both directions.  This simple byte layout is registered; do not silently
change bit packing to save receipt space.

The checker must decode, validate padding and ranges, independently rebuild the
entire arrays, and compare decoded values, not merely hashes or aggregate
counts.

Reduced-word classes are assigned one-based ids in first tuple-occurrence
order.  During construction, equality is exact equality of the complete
freely reduced signed-letter sequence.  A SHA-256 may select a candidate
bucket, but every collision is resolved by signed-word equality; a digest is
never an equality oracle.  Its canonical hash bytes encode letters
`1,2,-1,-2` as the signed two's-complement bytes `01,02,ff,fe`; zero and every
other byte are forbidden.  The known sum of the 26 cube lengths is `9162`, and
the unreduced all-tuple payload bound is `18580536` bytes, so publishing every
class word would itself exceed the registered 16-MiB receipt cap and is
forbidden as a receipt requirement.

Serialize the tuple-to-class map as exactly 17,576 unsigned 16-bit
little-endian ids on a full terminal, or exactly `evaluated_prefix` ids on a
resource terminal, all in `[1,class_count]`, with no padding bytes.  In
class-id order publish three packed metadata arrays: one uint16-le first tuple
ordinal, one uint32-le reduced length, and one exact 32-byte signed-word
SHA-256 per class.  Publish Base64, exact byte lengths, SHA-256 of each raw
array, and a decoded-list digest for the tuple map and all metadata arrays.
Each first ordinal must map back to that class and reproduce its length/hash.
The checker freshly reconstructs every reduced signed word, resolves classes
by exact signed-word equality, and requires exact decoded mapping and metadata
equality.  Endianness, widths, one-based ids, class order, and the absence of
padding are schema gates.  No full class-word payload or offset table belongs
in the receipt.

## F. Terminals and exact claims

Use exactly four mutually exclusive terminals:

```text
B345_TRIPLE_CUBE_RAW_LAMBDA_ACTIVE
B345_TRIPLE_CUBE_RAW_LAMBDA_INERT
B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_RESOURCE
B345_TRIPLE_CUBE_RAW_LAMBDA_UNKNOWN_INPUT
```

`ACTIVE` requires a complete 17,576-tuple census and at least one typed tuple
with scalar `1` or `2`.  It proves only:

```text
one_registered_typed_triple_direction_has_nonzero_qstar_scalar
```

It does not prove target-6 consistency, all-33 acceptance, or a literal pair.
The canonical first-active record is the sole handoff to a future full-vector
lane.

`INERT` requires a complete census and scalar zero for every typed tuple.  It
proves exactly:

```text
the support-one qstar dual annihilates the affine span of the old 108 columns
and every typed correction direction in the complete ordered 26^3 universe,
against the frozen fixed D2 prefix; hence that registered affine system remains
inconsistent at target 6.
```

It does not cover untyped tuples, products not in this exact triple universe,
all depth-three words, full D2, or full H3.

Both mathematical terminals must set, explicitly:

```text
fixed_prefix_only = true
full_D2_claimed = false
full_H3_claimed = false
all_depth3_claimed = false
all_corrections_claimed = false
literal_pair_claimed = false
negative_global_claimed = false
B4_A_claimed = false
B4_B_claimed = false
```

`UNKNOWN_RESOURCE` carries only a committed tuple prefix and no active/inert
claim.  `UNKNOWN_INPUT` is restricted to missing/drifted authenticated files,
paths, JSON, pins, or q3 schema before or during fresh reconstruction.  Internal
qstar/rank/sign/DP/checker drift is a hard failure, not an UNKNOWN terminal.

Terminal derivation is closed and mechanical:

```text
authenticated-input drift                         -> UNKNOWN_INPUT
registered structural/time/RSS cap                -> UNKNOWN_RESOURCE
complete_scan and nonzero typed-scalar count > 0  -> ACTIVE
complete_scan and nonzero typed-scalar count = 0  -> INERT
anything else                                      -> hard failure.
```

The `INERT` implication must be justified in the receipt and checker by the
following exact linear argument.  `lambda_B` annihilates the fixed prefix,
the old 108 columns, and each typed registered triple column, while
`lambda_B(-z)=1`; applying it to a hypothetical solution of
`sum a_r Delta_r = -z (mod span(B))` gives `0=1` in F3.  No group-generation,
normal-closure, full-D2, or literal-product inference is part of this lemma.

Partial state is an exact committed-prefix object.  Append tuple data
atomically only after all five typed gates and, when typed, its scalar are
complete.  On `UNKNOWN_RESOURCE`, serialize arrays of decoded length exactly
`evaluated_prefix` (not padded semantic entries up to 17,576), the last
committed ordinal, prefix tuple-to-class map/class metadata, counts and SHA-256,
and zero padding bits in the final storage byte.  The in-progress tuple is
absent.  If a nonzero scalar was seen, it may appear only as
`provisional_first_active`; set `provisional_only=true` and every mathematical
claim false.  It is not the canonical handoff until the complete scan proves
that no earlier/missing classification changes the registered result.  Full
terminals forbid partial/provisional fields; `UNKNOWN_INPUT` before scanning
uses `evaluated_prefix=0` and no mathematical arrays.

## G. Resource and performance contract

Register and serialize these exact global guards:

```text
cube_count                         26
ordered_pair_count                676
ordered_triple_count              17576
unique_context_count              31
named_occurrence_count            46
cube_total_reduced_letters      9162
ordered_triple_unreduced_letters 18580536
prefix_columns                    362725
prefix_pivots                     362709
raw_lambda_oracle_entries          362710
raw_lambda_recursion_edges        8388608
typed_dp_state_records            1048576
packed_receipt_bytes              16777216
common_math_soft_deadline_seconds 18000
producer_soft_rss_bytes           4831838208
external_job_limit_minutes        330
safety_margin_minutes             30
```

The first nine values are exact universe/binding equalities, not adjustable
caps.  Structural cap hits use a closed reason registry and become
`UNKNOWN_RESOURCE` with cap key, limit, observed value, exact comparator,
phase, tuple ordinal, `(i,j,k)`, typed/active counts, queried oracle count, and
the committed packed-prefix digest.  The driver starts one common
18,000-second producer-plus-checker budget before the producer.  Keep producer
and checker in one fail-closed `bash -o pipefail` command, set Bash `SECONDS=0`
at producer launch, and compute `remaining=18000-SECONDS` after the producer;
do not approximate this by adding two independently allowed timeouts.  The producer
uses its remaining budget with a local monotonic deadline.  After producer
completion the driver subtracts all elapsed math time and passes only the
positive remainder to the checker; the checker starts a local monotonic
deadline for that remainder and cannot reset to 18,000.  Zero/negative
remaining time fails before PASS.  Record the common start, producer
consumption, checker initial remainder, and final margin; wall-clock transport
is never a mathematical receipt claim.  RSS uses the same
`/proc/self/status` primary/fallback discipline as 157ec.  Check at least once
per 64 tuples and force-check at each phase boundary.

Pair/value/translation caches are bounded performance caches.  Their capacity
is not a semantic cap: evict and recompute exactly.  Record hits, misses,
evictions, cold recomputations, current/peak entries, and prove in selftest that
tiny versus roomy caches produce byte-identical decoded census arrays.

Expected source-based runtime on the hosted runner is:

- fresh q3/prefix/support-one reconstruction: approximately 10--20 minutes for
  producer plus checker, based on 157ec;
- complete scalar census with value/pair DP: approximately 15--60 additional
  minutes combined;
- normal same-job band: 35--80 minutes;
- pessimistic band: 90--180 minutes;
- expected peak RSS: roughly 0.9--1.5 GiB with the pivot-only lambda table;
  a design approaching 3 GiB must report which registered structure owns it;
- the 300-minute internal soft stop and 330-minute external limit remain the
  fail-closed hard envelope.

An implementation which flattens all target words or performs 17,576 x 46
letterwise replays is a performance failure and must be redesigned before GHA.

## H. Independent checker and exact schema

Create a standalone checker which does not import the producer or share its
math helpers.  It must independently reconstruct and validate:

1. every frozen file/artifact/task pin and source hash;
2. q3 quotients, 26 cubes, all cube/tuple orders and word classes;
3. the 31 contexts and 46 named occurrences;
4. the fresh 362,725-column prefix, canonical pivot basis, and exact 16
   dependent-event raw-column records;
5. the old-104 rank 50 and full-108 rank 54 predecessor matrix;
6. the exact support-one qstar label, sign, base/RHS values, and all-108 zeros;
7. the canonical-key raw-lambda table and its pivot/dependent annihilation
   certificate without producer pool ids;
8. all 17,576 typed classifications and scalar codes by its own DP;
9. first-active/null or provisional-first-active, counts, packed arrays,
   terminal, committed-prefix boundary, and claim boundary.

Use exact terminal- and phase-aware top-level and nested keysets.  Reject stale,
extra, positive/full-vector, selected-solution, proof-DAG, or imported-receipt
fields.  `ACTIVE` must not contain a full affine solution; `INERT` must not
contain a handoff record; partial/input ledgers appear only on their own
terminals.

Every receipt-producing branch and every synthetic fixture must pass through
the same terminal derivation, exact top-level keyset, nested keyset, packed
decoder, and claim-boundary validator used by the real full path.  A selftest
may inject mathematical callbacks, but may not bypass or replace this sealed
production envelope.  Producer and checker each use its own such validator;
this requirement does not permit importing one executable's implementation
into the other.

The checker must print exactly one PASS marker only after the production path
has been replayed.  A checker crash or mismatch must make the driver fail.

## I. Required selftests and mutations

After static review, one combined bounded producer/checker selftest is
authorized.  It must exercise the real production validators and include:

1. toy `3^3` nested order/ordinal, repeated tuples, duplicate word classes,
   last ordinal, packed padding, and tuple permutation mutations;
2. wrong empty-record handling and wrong 26-cube first-occurrence order;
3. a nonabelian quotient example with nonidentity factor values where
   `D(abc)=D(a)+a.D(b)+ab.D(c)` passes and the additive shortcut fails;
4. left/right action, product order, and negative-letter mutations;
5. a small triangular prefix where recursive `lambda_key` equals direct
   normal-form qstar extraction on every basis key and test vector, plus
   rejected recurrence-cycle, forward-order, numeric-pool-id-order, and
   rollback-id-reuse mutations;
6. qstar pivot, component, E4 byte, width, target name, support count,
   `yb/yz` sign, and normalization mutations;
7. one failed E3/source/context/target-value gate with the exact first reason;
8. synthetic complete `ACTIVE` and `INERT` censuses, including first-active
   freeze while later tuples are still evaluated;
9. a mutation which proves lambda-zero columns are not silently omitted from
   the complete tuple ledger;
10. cache-capacity neutrality with forced eviction/cold recomputation;
11. resource stops before prefix, during oracle construction, mid-census, and
    after first-active but before census completion, with exact committed
    partial arrays and provisional nonclaim;
12. exact terminal/reason/claim/schema/pin mutations and rejection of any
    full-vector/positive field;
13. a toy instrumented `add_column` run with an exact dependent raw column,
    and mutations of its translation ordinal, canonical blob, relator,
    coefficient, NF-zero result, and lambda-zero result;
14. forced SHA-bucket collision with unequal exact signed words, plus
    class-id width/endianness/first-ordinal/length/hash/padding mutations and
    first-occurrence-order rejection;
15. a formula/direct mutation which hard-fails rather than producing a sixth
    typed-reason code, and a source-DAG mutation deleting one inverse or
    conjugating factor;
16. a common-deadline fixture proving that the checker receives only the
    producer-plus-overhead remainder and cannot reset its budget.

The driver must require explicit producer and checker selftest PASS markers.
State every canary in the reply.  Do not call a selftest `verified`.

## J. Driver, files, and allowed worktree changes

Create exactly these four versioned files:

```text
search/d972_b345_triple_cube_raw_lambda_census_v1.py
search/check_d972_b345_triple_cube_raw_lambda_census_v1.py
search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g
sol/luna_reply_157ed_b345_triple_cube_raw_lambda_census.md
```

Do not edit q3, v1--v10, 157ea--157ec, workflows, claims, dialogue, notes, or
other files.  Temporary diagnostics belong outside the repository.  Do not
run a production scan, GAP math, Git, GHA, or workflow.  Syntax compilation and
the single bounded combined selftest above are allowed only after the bundle is
statically complete.

The GAP driver must:

- pin its own frozen producer/checker and every upstream hash;
- select exactly one of selftest/full modes;
- use q3 same-job reconstruction and independent q3 checker exactly as the
  frozen drivers do;
- use fixed paths under `ci/out/`, delete stale artifacts/sentinels/logs first,
  and perform checked writes/readbacks;
- use `bash -o pipefail`, `tee` for live producer/checker progress, exit
  sentinels, exactly-one terminal marker, and exactly-one checker PASS marker;
- start one 18,000-second common math deadline before producer launch, pass
  only its measured positive remainder to the checker, and fail closed if no
  checker budget remains;
- accept all four registered terminals and no other terminal;
- preserve runtime-only q3 normalization and package pins;
- never treat a GAP/Python syntax error, missing artifact, stale sentinel,
  UNKNOWN terminal, or checker failure as a mathematical green result.

Recommended artifact path:

```text
ci/out/d972_b345_triple_cube_raw_lambda_census_v1.json
```

The producer should emit progress at phase boundaries and at least every 256
tuples, including ordinal, typed count, lambda counts, first-active/null,
oracle queries, cache accounting, elapsed time, and RSS.

## K. Reply requirements

The reply must report:

- exact SHA-256 and byte count for all four new files;
- the frozen task SHA supplied by Sol and every upstream/result pin;
- exact terminal/schema names and claim boundaries;
- packed-array layout and decoded counts expected by the checker;
- raw-lambda construction, support-one/base/RHS checks, and DP orientation;
- cache policy, structural cap registry, estimated runtime/RSS, and progress
  cadence;
- the exact bounded selftest command and complete PASS markers;
- confirmation that no production scan, GAP math run, Git operation, GHA
  dispatch, workflow edit, or unrelated file edit occurred.

Stop after implementation, static audit, and the one authorized combined
selftest.  Return the frozen hashes for a separate hostile pre-dispatch audit.
