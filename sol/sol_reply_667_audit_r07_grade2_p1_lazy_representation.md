# Sol(max) Task667 audit — minimal lazy representation of `P1`

## Verdict

The lazy representation is mathematically lossless and is sufficient as the
source representation of the complete grade-one transition presentation.  No
downstream operation in Task647 requires the whole `8059 x 96776` family to be
resident.  A downstream operation may form one transient logical row, or one
typed block of that row, but it must not silently replace any of the semantic
replays or the result-dependent ancestry required by v474/v479.

This verdict is conditional on the exact typed contract below.  A descriptor
which retains only digests, omits the actual DAG reductions/scales/origins, or
uses `18144` without a type tag is not lossless and is not covered by the
verdict.

## F667-1 — exact typed reconstruction and offsets

Let `k = F3`, let the character order be

```text
A = ((0,0), (0,1), (1,0), (1,1)),
```

and put

```text
V0[a] = k^6048,
V1[a] = k^18144,
Aux   = k^8,
P1    = (direct sum_a V0[a]) + (direct sum_a V1[a]) + Aux
      = k^(24192 + 72576 + 8) = k^96776.
```

The canonical flat coordinates are therefore

```text
D0(a,q) = 6048*a + q,                 0 <= q < 6048,
D1(a,q) = 24192 + 18144*a + q,        0 <= q < 18144,
AUX(r)  = 96768 + r,                  0 <= r < 8.
```

The base-3 encoding is four trits per byte, least-significant trit first.
Thus the packed row widths are respectively `1514`, `18144`, `4536`, and
`24194` bytes for dense widths `6056`, `72576`, `18144`, and `96776`.

### Old rows

For character `a` and local pivot `p`, read the raw contiguous packed slices

```text
lower_basis_blob[p*1514 : (p+1)*1514]       -> (l, alpha) in k^6048 x k^8,
lifted_grade_blob[p*18144 : (p+1)*18144]    -> G in direct sum_c V1[c].
```

If `i = O[a] + p`, then the reconstructed row is exactly

```text
b_i = (iota0_a(l), G, alpha).
```

Here `iota0_a` puts `l` in the owning degree-zero character block.  The other
three degree-zero blocks are zero by construction.  `G` is a four-character
degree-one companion and must not be treated as character-local.  The eight
auxiliaries occur at the very end of the global row, not directly after the
owning `6048` coordinates.

The real prepare schema and raw file-size equations give:

| `a` / label | rank and global half-open range | lower blob SHA-256; bytes | lifted-grade blob SHA-256; bytes |
|---|---|---:|---:|
| 0 / `(0,0)` | `505`, `[0,505)` | `46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837`; `764570 = 505*1514` | `08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b`; `9162720 = 505*18144` |
| 1 / `(0,1)` | `503`, `[505,1008)` | `8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333`; `761542 = 503*1514` | `14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364`; `9126432 = 503*18144` |
| 2 / `(1,0)` | `503`, `[1008,1511)` | `ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4`; `761542 = 503*1514` | `0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4`; `9126432 = 503*18144` |
| 3 / `(1,1)` | `503`, `[1511,2014)` | `3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48`; `761542 = 503*1514` | `7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5`; `9126432 = 503*18144` |

Thus `O = (0,505,1008,1511)` and the old end is `2014`.

### New `H^[1]` rows

For character `a` and local pivot `p`, read

```text
basis_blob[p*4536 : (p+1)*4536] -> h in V1[a] = k^18144.
```

If `i = H[a] + p`, then

```text
b_i = (0 in direct sum_c V0[c], iota1_a(h), 0 in Aux).
```

Only the owning degree-one character block can be nonzero.  All four
degree-zero blocks, the other three degree-one blocks, and all auxiliaries are
zero by construction.

| `a` / label | rank; attempts; global half-open range | basis blob SHA-256; bytes |
|---|---|---:|
| 0 / `(0,0)` | `1509`; `14268`; `[2014,3523)` | `cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39`; `6844824 = 1509*4536` |
| 1 / `(0,1)` | `1512`; `14280`; `[3523,5035)` | `0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461`; `6858432 = 1512*4536` |
| 2 / `(1,0)` | `1512`; `14280`; `[5035,6547)` | `602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6`; `6858432 = 1512*4536` |
| 3 / `(1,1)` | `1512`; `14280`; `[6547,8059)` | `4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9`; `6858432 = 1512*4536` |

Hence `H = (2014,3523,5035,6547)` and the final end is `8059`.  This proves the
requested cumulative list

```text
0, 505, 1008, 1511, 2014, 3523, 5035, 6547, 8059.
```

The descriptor must record/recompute the first nonzero coordinate in the
*global* `96776` order.  In particular, a local old lower lead in the final
eight positions maps to `96768..96775`, not to a coordinate adjacent to the
owning degree-zero block.  One cannot copy a `6056`-local lead blindly.

## F667-2 — sufficiency for every Task647 operation

The answer is **yes as a representation of `P1`**, with the fixed arithmetic
context and raw Task554 parents also authenticated.  It is not, by itself, an
entire v474 terminal certificate.

1. **Precision-two lift.**  Process row IDs in the authenticated prior order.
   For an old row, replay its projected-seed or actor-parent origin, its prior
   reductions, and its scale.  For a new row, replay its defect or actor-parent
   origin, reductions, and scale.  Earlier degree-two parts may live in the
   separate packed degree-two lift store; the precision-one part is obtained
   lazily.  The reconstructed lift must truncate byte-for-byte to the lazy
   `b_i`.  No family-wide precision-one matrix is needed.
2. **`ell` and `g`.**  Apply the exact physical aggregation to one reconstructed
   full lift.  It yields `ell_i in F3^32260` and `g_i in F3^48384`.  Only that
   offer and the lower-echelon state/companions need be live.
3. **Defects.**  For each of the 44 seeds and each of the four actors on each of
   8,059 rows, construct the direct value and subtract the canonical lazy row
   combination.  The full `96776` precision-one part must compare with zero
   before returning a `36288`-coordinate character degree-two slice.  This is
   `44 + 4*8059 = 32280` defects; the actor part alone is `32236`.
4. **Connection recursion.**  The lower-first recurrence consumes the ordered
   stream `(ell_i,g_i)`.  It requires the lower pivots and companions, not the
   stored precision-one family.
5. **Literal MEMBER ancestry.**  The old/new row descriptors plus actual
   origin/reduction/scale streams preserve the literal source ancestry.  The
   targeted computation must additionally retain the dynamic ancestry of
   connection offers, generated orbit rows, and physical echelon reductions.
   The lazy `P1` object does not replace those result-dependent records, but no
   dense `P1` family is needed to create or expand them.
6. **Independent replay.**  The checker reopens the five pinned Task554
   artifacts, reconstructs its own typed descriptors and global relations, and
   independently evaluates selected or complete equations.  It may not accept
   producer descriptor hashes or import producer reconstruction code as proof.

Consequently no listed operation genuinely requires a resident
`8059 x 96776` dense or packed combined store.  A one-row `96776` buffer is a
permitted implementation convenience, not an authority and not a family
cache.  Component-wise evaluation can avoid even that buffer where the exact
gate does not require a flat comparison.

The global coefficient streams must be derived exactly as in the Task565
presentation assembly, rather than guessed from character locality:

- one seed reduction concatenates the four offset old seed expressions and,
  for each of their four defect-origin IDs, the matching `origin_reductions`
  from *all four* new blocks, followed by exact-key mod-3 normalization;
- an old-row actor reduction concatenates its offset old transition expression
  and the matching origin reduction from all four new blocks;
- a new-row actor reduction is its own block expression offset by `H[a]`.

This dependence across all new blocks is why the DAG/expression metadata is
mandatory even though most stored row coordinates are structural zeroes.

## F667-3 — coordinatewise assembly lemma

Let `U_w` be canonical unpacking of `w` trits from a raw packed row.  Define
the lazy evaluator `E(i,x)` by the two piecewise reconstructions in F667-1.
Let `D_i` be the dense row emitted by Task565's
`assemble_precision1_basis`.

**Lemma.**  For every `0 <= i < 8059` and `0 <= x < 96776`,

```text
E(i,x) = D_i[x] in F3.
```

**Proof.**  For an old row, Task565 creates four zero degree-zero blocks, puts
`l` in block `a`, reshapes the complete `G` into the four degree-one blocks,
and calls

```text
flatten_precision1(degree0, degree1, alpha).
```

That function concatenates the four degree-zero blocks, then the four
degree-one blocks, then the eight auxiliaries.  Therefore equality holds in
the owning degree-zero interval, the three zero degree-zero intervals, the
whole degree-one interval, and the auxiliary interval.  These five exhaustive
cases cover every coordinate.

For a new row, the same function receives zero degree zero, zero auxiliary,
and four zero degree-one blocks except for `h` in block `a`.  Equality follows
on the degree-zero interval, the owning degree-one interval, the three other
degree-one intervals, and the auxiliary interval.

Finally, every relevant width is divisible by four.  A canonical byte in
`0..80` has a unique four-digit base-3 expansion, so `unpack(pack(v)) = v`.
The old `PackedEchelon.matrix_bytes()` and Task565 `PackedRowWriter` serialize
rows in C row-major order; Task565 reopens them with shape
`(rows,width/4)`.  The byte offsets in F667-1 therefore select exactly the
same packed rows.  This completes the coordinatewise proof.

This lemma is only a serialization/assembly equality.  It does **not** prove
the service receipt, HEAD/body/blob hashes and roster, canonical bytes, actual
global lead and normalization, distinct leads, prior-only DAG, origin typing,
44 seed equations, 32,236 actor equations, all 8,059 lift truncations, v451
arithmetic gates, or terminal ancestry.  Producer and independent checker
must still perform those gates.

## F667-4 — honest storage and RSS boundary

The immutable packed files actually needed to reconstruct the `P1` rows are:

| family | exact bytes |
|---|---:|
| four old lower blobs | `3,049,196` |
| four old lifted-grade blobs | `36,542,016` |
| four new block basis blobs | `27,420,120` |
| **lazy row backing total** | **`67,011,332`** |

A synthesized packed `P1` family would be
`8059*24194 = 194,979,446` bytes; a dense uint8 family would be
`8059*96776 = 779,917,784` bytes.  The lazy backing therefore saves
`127,968,114` bytes against the packed duplicate and `712,906,452` bytes
against a dense duplicate.  It does not make the original backing files or
their pages free.

Exact slice and ordinary one-row sizes are:

| item | packed/source bytes or dense scratch |
|---|---:|
| one old row's two packed slices | `1514 + 18144 = 19658` |
| those old nonzero source components decoded | `6056 + 72576 = 78632` |
| one new packed/decoded row | `4536` / `18144` |
| one optional flat precision-one scratch | `96776` |
| one full source row through degree two plus auxiliaries | `241928` |
| one packed degree-two lift row / all 8,059 | `36288` / `292,444,992` |
| one dense `ell` plus `g` / packed pair | `80644` / `20161` |
| one character defect dense / packed | `36288` / `9072` |
| one complete character packet | `9072*32280 = 292,844,160` |

The five raw state bodies are respectively `15,398,340`, `74,883,943`,
`75,400,514`, `75,340,879`, and `75,407,216` bytes, total
`316,430,892`.  Mapping all of those and all lazy row blobs spans exactly
`383,442,224` raw file bytes.  They must be streamed/transcoded one body at a
time and unmapped; `json.loads` of all four approximately 75-MB block bodies
would create a much larger Python list/dict forest and violates Task647's
resource design.

For comparison with Task647's later families, its first four packed families
total `1,076,935,099` bytes.  Adding the lazy backing, the degree-two lift
store, and one character defect packet gives

```text
1,076,935,099 + 67,011,332 + 292,444,992 + 292,844,160
= 1,729,235,583 raw mapped/file bytes.
```

If all five JSON bodies were also mapped, the raw sum would be
`2,045,666,475`.  Neither number is an RSS promise: touched mmap pages, the OS
file cache charged to the process, NumPy casts/copies, map tables, flat
indices, interpreter objects, and dynamic ancestry are additional.

The exact static source counts are 8,059 row/DAG nodes, 8,232 defect origins,
and 73,399 local coefficient-list streams:

```text
176 old seed + 8056 old actor + 32928 new origin
+ 24180 new actor + 8059 DAG reduction = 73399.
```

The receipts examined here do not state the total number `N` of coefficient
pairs.  An honest flat encoding may, for example, use a 16-byte
offset/count record per stream (`1,174,384` bytes) and an unaligned canonical
`u32 row_id + u8 coefficient` payload of exactly `5*N` bytes, plus a versioned
fixed origin/row table.  Luna must emit `N` and every exact flat-file byte
count/hash and charge them to the durable/transcript caps.  Claiming a smaller
exact metadata or ancestry ceiling before those counts exist would be false.

Static source ancestry is file-backed flat data, not a resident object forest.
Selected MEMBER ancestry and CEGAR checkpoint/transcript ancestry are
result-dependent and have no present exact byte total; they remain subject to
Task647's separately preregistered transcript/durable caps.  The existing hard
process RSS ceiling remains `7,516,192,768` bytes.  Reaching an RSS, durable,
transcript, wall, or path cap is `UNKNOWN_RESOURCE`, never MEMBER/NONMEMBER.

Repeatedly decoding the same full row inside nested actor/reduction loops can
also erase the time benefit.  Cache only the current row or bounded chunk,
charge every scratch allocation, and do not describe mmap/page cache as
RSS-free.

## F667-5 — Luna implementation contract

### Identity and immutable source binding

Use canonical IDs

```text
Old(a,p): global = O[a] + p,  0 <= p < (505,503,503,503)[a]
H1(a,p):  global = H[a] + p,  0 <= p < (1509,1512,1512,1512)[a].
```

Every descriptor binds the Task554 run/attempt `33677346616/1`, head
`22c6dddb43d107c05e65f53ad898823ae8ebe276`, the exact successful producing
job/workflow envelope, and the service artifact ID/name/archive bytes/digest,
then the canonical HEAD, body hash, exact roster, and blob receipt.  The five
artifact IDs are `9865061266, 9865238399, 9865242284, 9865193269,
9865239848`; the five state-body hashes are those in Task647 section 1.2 and
F667-1.  A body hash alone is not the artifact binding.

An old descriptor has two independently typed references:

```text
(file_id=old_lower[a], trit_width=6056, byte_offset=1514*p, byte_length=1514)
(file_id=old_grade[a], trit_width=72576, byte_offset=18144*p, byte_length=18144)
```

A new descriptor has

```text
(file_id=h1_basis[a], trit_width=18144, byte_offset=4536*p, byte_length=4536).
```

The explicit `trit_width` and semantic kind are mandatory because `18144` is
both the dense width of a new character row and the packed byte length of an
old 72,576-trit companion.

### Required read-only API

The producer's minimal `Presentation1` surface is:

```text
row_id(i) / descriptor(i)
degree0_block(i,a), degree1_block(i,a), auxiliary(i), coord(i,x)
actual_lead_and_normalization(i)
dag(i)                         # typed origin, prior reductions, scale
seed_reduction(s)              # canonical global row-id/coefficient stream
actor_reduction(i,t)           # t in (1,-1,2,-2)
lift2(i)                       # full exact row through degree two
ell_g(i)                       # F3^32260 x F3^48384
defect_slice(a,o)              # o in 0..32279, after full P1-zero gate
literal_expand(i)              # source occurrence ancestry
```

`dag`, seed, actor, and origin expressions contain actual ordered records, not
only their hashes.  Coefficients are canonical nonzero `1` or `2`; global
expressions are exact-key combined mod 3 and sorted.  DAG parents/reduction
indices are strictly prior in the appropriate local/global order.  Dynamic
connection/orbit/echelon ancestry is stored by the owner separately but points
back to these canonical row IDs.

### Streaming gates and replay gates

The following can be fused with a single sequential pass per raw file:

- service/HEAD/body/roster/blob authentication and EOF;
- exact dimensions, row counts, packed byte range `0..80`, and no alias/path
  substitution;
- actual nonzero first-trit/normalization scan and the typed descriptor table;
- DAG/origin/expression schema, prior-index and coefficient validation while
  transcoding to canonical flat streams.

Those structural passes do not discharge semantic replay.  Producer and
nonimporting checker must still reconstruct the global 44 seed expressions,
all 32,236 actor expressions, and replay all 32,280 equations.  They must also
replay every lift DAG and compare all 8,059 precision-one truncations, and run
the v451 occurrence/aggregation/action/auxiliary gates.  A rolling hash or a
producer-produced flat index is not a substitute.

This design does **not** materially shorten mandatory four-block ingest: all
four bodies and basis blobs still must be authenticated, structurally parsed,
and semantically replayed by both programs.  It eliminates the extra
194,979,446-byte assembled packed `P1` file (and its write/read/zero-fill work)
and substantially reduces peak-memory risk in the grade-two owner.  It does
not change the number of lifts, defects, connection offers, separator steps,
or terminal ancestry checks, and it is not an asymptotic speedup.  A naive
implementation with repeated full-row decoding can be slower.

Current implementation status is unchanged by this paper audit: Task650,
Task653, and Task665 reported `NOT_READY`; Task666 closed only the producer-side
prepare ingest (`2014` DAG rows, `8232` origins, `176` seed and `8056` actor
source expressions, `188,958,668` authenticated prepare-blob bytes).  Its full
first-trit scan, independent checker, all four block ingests, and later Task647
operations remained pending.

## F667-6 — four width types and Task647 correction

| number | exact type | forbidden confusion |
|---:|---|---|
| `6056 = 6048+8` | one old character's degree-zero lower row followed by all eight **source** auxiliaries | not a physical lower row; its last eight coordinates inject at global `96768..96775` |
| `72576 = 4*18144` | one old row's complete four-character source degree-one companion | not character-local; packed row length happens to be `18144` bytes |
| `18144 = 6048*3` | one new `H^[1]` character block's **dense trit width** | its packed length is `4536`, so it must not be confused with the previous row's `18144` packed bytes |
| `96776 = 4*6048 + 4*18144 + 8` | one logical source precision-one row, degrees zero and one plus source auxiliaries | not a physical pair |

There is no `96776`-wide “paired lower/physical object.”  The physical outputs
used by the connection transducer are instead the distinct pair

```text
ell in F3^32260,   g in F3^48384,
```

whose combined dense count would be `80644`, not `96776`.

Task647 line 150 is numerically and mathematically correct.  To remove the
dangerous ambiguity, Task647 line 324 should be read/corrected from

```text
all 96,776 source lower/auxiliary coordinates
```

to

```text
all 96,776 source precision-one coordinates
(24,192 degree-zero + 72,576 degree-one + 8 auxiliary).
```

This wording correction is incorporated into the implementation contract and
does not require a change to the dimension.

## Audited source pins and claim boundary

The principal frozen source bytes used in this audit were:

| source | bytes / LF lines | SHA-256 |
|---|---:|---|
| Task647 reply | `37363 / 740` | `def1be12d5c8337daf82c1f25427c936b2d5d55875cd27109d9487189c4e5cfb` |
| v474 | `12755 / 321` | `a0ae668799de33d79b5e80ca2a6b7b50224770528b1201d8fb999506757c08c9` |
| v479 | `12280 / 292` | `df6850c9e7c86a83ade26c37064a7deb38ec3c8d7907b1eec6ff0d5268b22986` |
| grade1 v4 producer | `144552 / 3326` | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |
| independent full-routing v2 checker | `27778 / 399` | `a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3` |
| Task565 grade2 prebuild v1 | `145917 / 3499` | `acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8` |

This was a static mathematical/code-interface audit plus read-only schema and
file-size inspection.  It did not implement the owner/checker, execute the
heavy computation, accept a grade-two terminal, or turn a targeted MEMBER into
a complete `P2`.  No production/GHA/git action was taken.

```text
verified=false
v220 numerator: unchanged (first-rung 1/6; A0 actual 0/1)
PASS_LAZY_P1 / SAFE_TO_IMPLEMENT=yes
```
