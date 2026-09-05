# Task920 -- actual seed-2 materializer intake and semantic stop

## Disposition

The concrete production adapters and all locally available parent bytes were
identified.  No parent was rebuilt or downloaded, no Git/GitHub/GHA operation
was used, and no physical row was inserted.

The requested seed-2 materialization must **not** proceed.  A bounded check of
the actual Task919 root covector found that Task919's direct seed scalar used
the filtered projector on only the direct side.  The raw direct side changes
the scalar from the advertised `1` to `0` in F3.  Root has recorded the repair
in `sol/proof_r07_scalar_filtered_direct_side_repair_v541.md`; Task921 has
independently approved that formula and the lower-dot plan.  Task919 remains a
same-object receipt for the numeric computation it actually performed, but it
is not a physical violation authority.

```text
SEED2_PHYSICAL_VIOLATION_FROM_RUN33903333330=WITHDRAWN
ACTUAL_SEED2_MATERIALIZED=false
ACTUAL_PHYSICAL_PIVOT_INSERTED=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```

## 1. Exact Task554 global SeedRed adapter

The smallest existing authenticated relation reader is the actual root batch
reader in `search/d972_r07_actual_grade2_root_scalar_batch_v1.py`:

- fixed ranks, offsets and origin ranges: lines 49--62;
- relation identity: `relation_source_sha256`, lines 286--301;
- unsorted-unique expression validation: `_expression`, lines 304--312;
- exact prepare/block validation: `_validate_task554_body`, lines 315--377;
- exact body/HEAD join: `_state_descriptor`, lines 380--408;
- prepare-plus-one-block evaluation: `accumulate_scalars`, lines 449--522.

The input expression order must be retained.  Task554 expressions are unique
and in range, but not sorted.  Globalization adds the fixed offsets

```text
old = [0, 505, 1008, 1511]
new = [2014, 3523, 5035, 6547]
```

and combines repeated global indices modulo 3.  A materializing adapter must
retain, for every raw term, at least parent role/body digest, old source
character or new target block, Task554 origin id, term ordinal, local index,
global index and coefficient.  Only the final coefficient map may delete
zero cancellations.  The old fixture helper
`normalize_terms` in `search/d972_r07_grade2_violation_materializer_v2.py`
lines 221--228 sorts away this ancestry and is not the production adapter.

The five exact body digests are:

```text
prepare  1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865
block-0  9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74
block-1  d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6
block-2  a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac
block-3  642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01
```

For zero-based registered seed 2, the four Task554 origins are ids
`[2,2066,4122,6178]`; their one-based literal descriptors say `seed=3` and
`lower_character=0,1,2,3`.  The exact retained source expressions are one
term each in the prepare body,

```text
old character 0: local 2, coefficient 2 -> global 2
old character 1: local 0, coefficient 2 -> global 505
old character 2: local 0, coefficient 2 -> global 1008
old character 3: local 0, coefficient 2 -> global 1511
```

All sixteen corresponding new-block origin expressions are empty.  Thus

```text
SeedRed(2) = [[2,2],[505,2],[1008,2],[1511,2]]
nonzero support = 4
raw ancestry events = 4
cancellations = 0
```

The actual nonzero support counts for `SeedRed(s)`, `s=0,...,43`, are:

```text
[1,2,4,5,0,0,0,0,0,0,0,0,0,5,1,8,12,8,12,14,14,15,18,18,
 20,23,23,28,33,8,902,23,0,2,1052,1563,1634,2,30,25,32,22,52,0]
```

This extraction opened one authenticated prepare body and one block body at a
time.  The four block SHA-256 values recomputed equal the fixed digests above.

## 2. Exact 96,776-coordinate precision-one adapter

No fixture lower provider is needed.  Task554 itself stores the complete lower
part of every global P1 row.  The authoritative implementation is:

- coordinate widths and Fourier order:
  `search/d972_r07_a0_first_rung_grade1_v3.py` lines 32--46;
- base-3 packing: `pack_trits`/`unpack_trits`, lines 641--654;
- blob receipt authentication: `validate_blob_receipt`, lines 870--951;
- prepare/blob semantic validation: `validate_prepare_state`, lines 1419--1538;
- block/basis semantic validation: `validate_block_state`, lines 1541--1612;
- authenticated memmap: `search/d972_r07_a0_first_rung_grade2_prebuild_v1.py`
  `load_grade1_packed_matrix`, lines 1569--1583;
- exact global-row assembly: the same file's
  `assemble_precision1_basis`, lines 1593--1621, and canonical v9
  `LazyP1.row`, `search/d972_r07_canonical_p1_dag_degree2_lift_v9.py`
  lines 1707--1753.

The flat row layout is fixed by `flatten_precision1`/`split_precision1` at
prebuild-v1 lines 818--839:

```text
degree0: 4 * 6048  = 24192 trits
degree1: 4 * 18144 = 72576 trits
auxiliary:                 8 trits
total:                 96776 trits
```

For an old row in character block `a`, read its local row from both:

- `old-a-lower-basis`: 6,056 trits, 1,514 packed bytes per row; it contains
  degree0 character slice `a` followed by the eight auxiliary trits;
- `old-a-lifted-grade`: 72,576 trits, 18,144 packed bytes per row; it contains
  all four degree-one character slices.

Put the 6,048 lower trits in degree0 block `a`, put the companion in the whole
degree1 block, and put the final eight lower-blob trits in the auxiliary tail.
For a new row in block `b`, read 18,144 trits / 4,536 packed bytes from
`block-b-basis`, put it in degree1 block `b`, and leave degree0, the other
three degree1 blocks and auxiliary entries zero.

The exact local payloads are:

| role | local path | rows | bytes | SHA-256 |
|---|---|---:|---:|---|
| old-0 lower | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-0-lower-basis.46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837.bin` | 505 | 764570 | `46beeda1dfca7a228eafc9fbf030eb3ccd87c5009c380bae39efa4d17dda7837` |
| old-0 grade | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-0-lifted-grade.08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b.bin` | 505 | 9162720 | `08632b4f3c0a8b0163926d48b406a58417038e427c902da56391c57963b4ab2b` |
| old-1 lower | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-1-lower-basis.8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333.bin` | 503 | 761542 | `8a37de95859793ef3c8321d18de09590c28ec5adbc9025e70f819426a8d89333` |
| old-1 grade | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-1-lifted-grade.14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364.bin` | 503 | 9126432 | `14ea8ee3833f11250d18beac102b3e8b8d759ca13e0f8230069ece5f395cf364` |
| old-2 lower | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-2-lower-basis.ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4.bin` | 503 | 761542 | `ee6ee8c731be47024b9f6656a31100139ddc4ca685c568427d8fe90b172a60b4` |
| old-2 grade | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-2-lifted-grade.0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4.bin` | 503 | 9126432 | `0609799f1bf4ba0fd534592c71ed22bee9c69b558930a4eddd745adf386076c4` |
| old-3 lower | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-3-lower-basis.3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48.bin` | 503 | 761542 | `3b9be2ac16be5a4394c164f759a6e4414b65c597ee77d42830e33aeaa5fb0b48` |
| old-3 grade | `%TEMP%/task554-prepare-33677346616-1-pinextract/old-3-lifted-grade.7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5.bin` | 503 | 9126432 | `7a3f436f4f2e324f0784f40efb975c31a24d845c350b0819f61b727aead3bec5` |
| new-0 grade | `%TEMP%/r07_grade1_blocks_33677346616/b0/block-0-basis.cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39.bin` | 1509 | 6844824 | `cc7e38114afc58e3aba10fa340a6ebd4f9a7a4752d5bb5fb9408ea8d84021e39` |
| new-1 grade | `%TEMP%/r07_grade1_blocks_33677346616/b1/block-1-basis.0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461.bin` | 1512 | 6858432 | `0223f72b7d2cb8a72f2ff99b8812fea977ed761c8505dab52ad3fba284b93461` |
| new-2 grade | `%TEMP%/r07_grade1_blocks_33677346616/b2/block-2-basis.602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6.bin` | 1512 | 6858432 | `602f23081aa609973860eac24d2f65104a9530c8ddf356d60a9d0378921b99f6` |
| new-3 grade | `%TEMP%/r07_grade1_blocks_33677346616/b3/block-3-basis.4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9.bin` | 1512 | 6858432 | `4ed4de15c00290f60e5fd2d57dd94db3103be92c602d92481f2835d9d96db0b9` |

These twelve immutable row payloads total exactly `67,011,332` bytes.  The
directory `d972-r07-p1-semantic-v2-33814881435-six` contains only the six
accepted semantic receipt JSON files; it is not itself a lower-row provider.

For one fixed 96,776-trit covector `kappa`, contractions with all P1 rows need
no dense basis and no DAG replay.  Pack the corresponding covector slices and
use a fixed `81 x 81` four-trit dot lookup while streaming/memmapping the above
matrices:

```text
old a: dot(kappa.d0[a] || kappa.aux, old-a-lower[p])
       + dot(kappa.d1[all four], old-a-lifted-grade[p])
new b: dot(kappa.d1[b], block-b-basis[p])
```

All values are reduced modulo 3 and emitted in the fixed global order.  This
is exactly v541 section 5: four lower covectors occupy 387,104 unpacked bytes,
the four result arrays occupy 32,236 bytes, and only prepare plus the current
block need be resident.

### Actual seed-2 lower-zero extraction

The selected complete P1 rows are global/local
`2=(old0,2)`, `505=(old1,0)`, `1008=(old2,0)`, and
`1511=(old3,0)`.  Their dense 96,776-trit receipts are:

| global row | support | dense SHA-256 |
|---:|---:|---|
| 2 | 2559 | `b5bf7356f162a7f8bd4477f5569e941d8aa386da472540090f9da1cefd741520` |
| 505 | 2558 | `8239e3bf0765c0dbd5d721e8951c063bbcea49ade9e7db92efb203bc8fe82dca` |
| 1008 | 2558 | `0f0e43f86f92ae3587e6cf3d58e1ae8f4b45c2e188d16b459a38de66158802a1` |
| 1511 | 2558 | `675264c220ce31c26e29dd3c87488569a8fb7a5af73d655f92ad7a1f0962344a` |

The raw third relator's complete precision-one row has support 2,801 and
dense SHA-256
`e2f907f900092e6c2ce3dc137982bba4779dd24e6e7b4cd089876563c768ecdb`.
Twice the sum of the four selected P1 rows has exactly the same support and
digest.  Their difference has support zero and the 96,776-zero-byte digest
`4cb171cdde559267e0f19b9eea4eb141e35b75c061685f87c4440706c573bd07`.
This is a real Task554 lower-zero join, not fixture evidence.

## 3. Selected P1 degree-two rows and projector convention

The accepted P1 parent is run `33851744070/1`, head
`6673eb2ea15ca6022acc2ddc5a8a204a0380172f`, artifact `9931437113`, manifest
SHA-256 `86e8b14cb0a60c86468ffb54a7bf14980366406a1e5bea17018fc6961f331feb`.
Its local root contains the complete `degree2.cache.bin` (292,444,992 bytes,
SHA-256 `b88edb9b12753cdb7a3629403f8ac14206595e03525fa2a201b6b00b985c1abf`)
and `instructions.jsonl` (349,055,442 bytes, SHA-256
`8b549337786b1f3b970a7250f1c326724ef957369c213c55af5a3d52a96f38ae`).

Each degree-two row is 145,152 trits / 36,288 packed bytes, as four
36,288-trit character slices.  Character `a` is read at packed offset
`node*36288 + a*9072`.  `PackedCache.row` is the exact positioned reader at
canonical-v9 lines 833--840; `full_from` joins it to `LazyP1.row` at lines
767--771.

The four seed-2 rows were extracted at their authenticated offsets:

| node | row offset | full packed SHA / support | a0 packed SHA / support | ancestry SHA |
|---:|---:|---|---|---|
| 2 | 72576 | `e5a6625e06ad97337edad5382d485d360a85bed2d05f0422e3e81408851a09f8` / 3666 | `a65a5bbf2467c28635d159752d41de9c503a85f8c2597bdead3e27f13b767e5f` / 849 | `b5e2ebad25f1ce5c3dcac8e24fe4d32ff089a6e94a8c37c169e196bf4d24effa` |
| 505 | 18325440 | `d30ed503bc707d0f57851bade215f39b6b57643ec98ffac9dd7016dad8c64584` / 3666 | `e9932ae482477843988c591fb44cad9640d85240a132eb8ee0b6032873eca8fb` / 933 | `74fc75ebe9d69fc898dab862f11c7ef0a5b51a467d50be7cf6a350fa6125d47a` |
| 1008 | 36578304 | `c84cc9f72f1e08085fdfab2c1491c62e455e5960d4031ffa26364965d3607347` / 3666 | `0c8e4fe89b60fa9d48a07297ddcbc7e4b71a907e12d1d8386cc870d3d89911b2` / 908 | `d39cc62d06eb87a81a11326e11858cd6e08713567c73ba12775acab2cb622c96` |
| 1511 | 54831168 | `ad25f92ba54fa937f18c24cab5724b89d7f18962a76db7a2a94d7121af5819f2` / 3666 | `09b391d1f2098bf581748225a418c200aa2cd2d8cfbe7b6ea40cac5cbfea9d42` / 976 | `aa39920bfa8a1b46f894ca5ad84bc861813662b4c64e7ca28ffd5548f9deeebe` |

All four instruction records have origin
`{"kind":"projected_seed","seed":3}`, no reductions, and scale 2.  The
full filtered projector is the unnormalized four-character sum in
grade1-v3 `projected_seed_pair`, lines 468--494, and in precision two
`project_full_by_words`, prebuild-v1 lines 762--773.  There is no extra
factor because `4=1` in F3.  That projector remains part of the P1 lift
construction, but v541 forbids using its top slice as the corrected direct
seed side.

## 4. Decisive direct-side counterexample

Using the exact Task919 `q-a0-root.bin` (support 2,742), the zero-based seed-2
top rows are:

| row | support | packed SHA-256 |
|---|---:|---|
| raw `_seed_evaluate_seed(...)[2][0]` | 568 | `e67d0a0b21aaf41fd1617811b45cd51191a0087c7d04fcc33dda5a58f4fcfca6` |
| old `_seed_full_project(...)[2][0]` | 849 | `7f151eec27ff74d68b13759ad3719913dcf26c3434274aa0e95868d5a4e45983` |
| raw minus projected | 1050 | `f57b13d028ca786c3bab7c88dbef463a63f8558093c18c9c4b626d9f87c5ed60` |

The actual q pairing with the difference is `2`.  Since every reconstructed
term is unchanged, the corrected scalar is `1+2=0 mod 3`.  The 44-seed
bounded comparison found raw and projected rows byte-equal for only 16 seeds;
the q-pairing counts for their differences were `0:25, 1:8, 2:11`.

The faulty production pointer is
`search/d972_r07_targeted_grade2_owner_generated_join_v15.py` lines 807--824:
`direct_seed_rows` calls `_seed_full_project` before pairing.  The correct raw
evaluator is `_seed_evaluate_seed`, lines 763--792.  The actor side also needs
the missing lower-to-top contraction from v541 (4.1); Task712 contains only
the homogeneous degree-two map.

## 5. Task712 B0 and current-S adapters (held, not applied)

The accepted Task712 parent is run `33814194630/1`, artifact `9915928157`,
archive SHA-256
`abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858`,
manifest SHA-256
`48c5d1f455e775cbcb3d887248de72d6bbda9df25deb5bafb8f02c8d121bdd47`.
The exact reader is `read_task712` in
`search/d972_r07_grade2_violation_materializer_v2.py` lines 307--422 and its
independent table parser is lines 264--304.

`B_fwd_a0.jsonl` has 36,288 entries, source width 36,288, destination width
48,384, 536,296 bytes, file SHA-256
`763affaa7be5dea7a1d432fa5cf43e65177abb1b9fb4935dc4b2e5c37cb5fd67`.
Its identity is exactly
`B_fwd_a0.jsonl:763affaa7be5dea7a1d432fa5cf43e65177abb1b9fb4935dc4b2e5c37cb5fd67`.
The retained sparse forward application is materializer-v2 lines 231--242;
the eventual single B call is lines 2330--2335.  It was not called here
because there is no valid nonzero seed-2 defect.

The Task904 current state is generation 8059, rank 1,354, HEAD
`69fdcc8cd740f8ea11bd198aaf44bcf50d1c4980331f51aa7f792544b00f9d88`,
manifest SHA-256
`d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b`.
The production state loader is
`search/d972_r07_grade2_physical_state_separator_v2.py` lines 979--1021;
the correct insertion-order reducer is lines 752--774.  Normalization and
record publication are lines 875--905.  The independent exact replay is
`search/check_d972_r07_grade2_physical_state_separator_v2.py` lines 397--478.

A bounded parse of the actual files found:

```text
records: 8059 = 1354 physical_pivot + 0 dependent + 6705 skipped
lead range: 0..1416; unique leads: 1354
adjacent lead descents/ascents: 348/1005 (not numerically monotone)
lead-list canonical compact-JSON SHA-256:
  47964722836d64aa3cfd9e71915fc9dd208322736bb9e6c15e291df333d422f0
first 20 leads:
  [0,3,1,4,2,5,6,7,8,9,11,10,12,13,14,15,19,16,17,18]
last 20 leads:
  [1393,1395,1396,1398,1400,1397,1399,1401,1402,1403,
   1404,1406,1412,1405,1408,1407,1411,1413,1414,1416]
prior reductions recorded: 610996
```

Every stored normalized row has lead trit 1 and zero at every earlier
insertion-pivot coordinate.  Physical offsets are `pivot_id*12096`, companion
offsets are `pivot_id*2015`, and rank after each pivot is `pivot_id+1`.
Consequently an eventual reducer must sweep all 1,354 leads in insertion
order; numeric lead sorting or an early free-coordinate stop is invalid.

## 6. Concrete minimum successor implementation

The seed-2 materializer is stopped.  The minimum valid successor is the
specialized corrected root scalar batch of v541, retaining the current actual
batch and parent machinery:

1. Replace the seed direct values by the raw
   `_seed_evaluate_seed(...)[2][a]` slices.  Do not reuse the registered
   projected-seed row hashes as a correctness oracle for this side.
2. For each active q and each of four actors, construct the 96,776-entry lower
   adjoint `kappa_(a,t)(q)` by v541 (4.1).  Its degree-two restriction must
   independently reproduce the accepted Task712 adjoint table.
3. Stream the twelve authenticated Task554 blobs above once, using the exact
   row adapter and packed dot products, to obtain the four 8,059-entry missing
   lower contractions.  Add them to the existing homogeneous child value
   arrays.
4. Keep the exact five-body global SeedRed/ActRed family, v540
   prepare-plus-one-block fold, 32,280 origin order, one P1-cache pass and all
   existing parent joins.
5. Use an independent checker implementation of the raw seed evaluator,
   lower adjoint and blob contractions.  A corrected nonzero scalar is only a
   candidate for the separate v534 materialization/pivot step.

All bytes needed for that corrected root scan are present locally.  For a
future GHA launch, the only staging delta relative to Task908 is that the
Task554 prepare artifact must retain the eight old lower/grade blobs and each
block artifact must retain its one `basis_blob`; the exact descriptors are in
the table above.  No old parent replay and no 349 MB instruction-DAG rebuild
is required.

The missing input for physical materialization is semantic, not a file: a
nonzero violation from the corrected scalar interface, joined to its exact
launch/result.  Until that exists, raw-source/B0/current-S insertion is
intentionally not run.

`R07_TASK920_INTAKE_COMPLETE_SEED2_MATERIALIZATION_STOPPED`
