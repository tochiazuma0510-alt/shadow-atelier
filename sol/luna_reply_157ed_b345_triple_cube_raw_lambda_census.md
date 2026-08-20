# Luna reply 157ed - ordered triple-cube raw-lambda census

## Status

`CROSS-CHECKED`.  The producer completed the preregistered ordered `26^3`
census and the independent checker reconstructed the q3 models, fixed prefix,
raw-lambda oracle, typing decisions, and all scalar values.  This is not a Lean
verification and is not a global nonexistence result.

Canonical task:

- `sol/luna_task_157ed_b345_triple_cube_raw_lambda_census.md`
- SHA-256 `15511f73e665a90f1e518383cb7bd218d8dd8e747026c498c3b4acce62837c2f`
- 36,171 bytes / 803 lines

Final source commit:

- `4226e73be45ba464b092bc3d5ff91dad54adc868`
- branch `sol/b345-q3-chief-v1`

## Frozen files

| file | SHA-256 | bytes |
|---|---|---:|
| `search/d972_b345_triple_cube_raw_lambda_census_v1.py` | `d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db` | 126,942 |
| `search/check_d972_b345_triple_cube_raw_lambda_census_v1.py` | `677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce` | 97,363 |
| `search/d972_b345_triple_cube_raw_lambda_census_gha_driver_v1.g` | `29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9` | 10,223 |
| this reply | self-referential final value reported out of band | reported out of band |

The driver pins the producer and checker hashes exactly.

## Cross-checked result

Final terminal:

`B345_TRIPLE_CUBE_RAW_LAMBDA_INERT`

Reason:

`complete_scan_all_typed_scalars_zero`

The complete lexicographic ordered universe, with repetitions retained, has
17,576 tuples.  Exactly 15 tuples passed all registered typing gates.  Their
ordinals and one-based cube triples are:

```text
894    (2,9,10)
1119   (2,18,1)
5452   (9,2,18)
5626   (9,9,10)
5651   (9,10,9)
5671   (9,11,3)
5852   (9,18,2)
6979   (11,9,11)
7021   (11,11,1)
7029   (11,11,9)
11519  (18,2,1)
11694  (18,8,20)
11954  (18,18,20)
12004  (18,20,18)
13296  (20,18,10)
```

All 15 have raw-lambda scalar `0`; scalar counts are exactly
`{0:15, 1:0, 2:0}`.  The other 17,561 tuples failed the first typing gate.
There are 17,414 exact signed-word classes.  The typed-mask SHA-256 is
`ff194ddd9e5b5d8416e683fa237a756209f44a624c52f2a4aa629fbcf8c430f8`;
the decoded tuple-to-class SHA-256 is
`3c00eeda0d299495907b6299f9f9a78c537615d1549ba727c662b25b79dc8089`.

The freshly rebuilt prefix has 32,768 BFS translations, 207 directed
translations, 362,725 columns, 362,709 pivots, 16 dependent columns, and
3,090,367 live sparse entries.  Reverse canonical-pivot propagation visited
2,727,658 row-tail entries and produced 362,710 semantic lambda entries
(362,709 pivots plus the explicit nonpivot qstar).  The lambda semantic digest
is `601681f16d88c85405eb8f460c9014408514e4bf0702aab2c5aa35d5c384e92b`.
All 362,709 pivot rows and all 16 original dependent columns are annihilated.

The predecessor target-6 system was independently reconstructed with
old-104 rank 50, full-108 rank 54, nullity 54, 33,687 coordinates, base
remainder support 184, `lambda(base)=2`, and `lambda(-base)=1`.  The public
dual has support one at target 6 (`hexagon_1_coface_0`), component 4, on the
exact canonical 154-byte E4 key.  Its all-108 annihilation digest is
`400f67f74b1250e538c395aa8bf647f6f7432ec07fe2582aaff06e5a47fe7ed5`.

Therefore none of the 15 typed words in this registered ordered triple
universe moves the fixed-prefix qstar obstruction.  This does **not** claim
full-D2 or full-H3 nonmembership, all-depth-3 exhaustion, all-correction
exhaustion, a global negative result, or nonexistence of a lift.  Every such
claim flag is false in the receipt.

## Final GHA evidence

Bounded final-hash selftest:

- run `32341939583`
- commit `4226e73be45ba464b092bc3d5ff91dad54adc868`
- URL: <https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32341939583>
- producer, checker, and driver PASS markers each occurred exactly once
- `cube_row_index=1` occurred exactly once

Cross-checked full run:

- run `32342044284`
- commit `4226e73be45ba464b092bc3d5ff91dad54adc868`
- URL: <https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32342044284>
- artifact id `9397268505`, name `gap-run-out`, compressed size 748,800 bytes
- artifact URL: <https://github.com/tochiazuma0510-alt/shadow-atelier/actions/runs/32342044284/artifacts/9397268505>
- artifact archive digest `sha256:7bdf9244958c1fe6fb5096ef13e46bdd9d26abaf2cba664e77f355ab30999e7e`
- receipt `d972_b345_triple_cube_raw_lambda_census_v1.json`: 1,571,542 bytes,
  SHA-256 `aa3e61ef1e3f3492bdaf4551f58833f270a5563cc913304c385669304d6efd85`
- producer terminal, producer zero-exit sentinel, checker PASS, and full-driver
  PASS markers each occurred exactly once
- producer elapsed 650.115 seconds; producer plus checker 1,317 seconds;
  run step 1,335 seconds; producer peak RSS 769,536,000 bytes

The q3 child artifact remained SHA-256
`3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`.

## Corrective run ledger

The production predicate was not changed by the transport/API repairs below.
Each failed full run stopped before a cross-checked terminal:

- `32338608942`: initial bounded selftest fixture failure.
- `32338913226`: bounded selftest PASS after fixture repair.
- `32339013984`: full stopped at Python 3.12 dynamic dataclass import.
- `32339417891`: bounded selftest PASS with pinned-import canary.
- `32339510722`: full stopped because the new budget wrapper lacked the
  predecessor monitor `reserve` API.
- `32340105187`: bounded selftest PASS with `monitor_reserve=1`.
- `32340204744`: full stopped after prefix because pool IDs were compared
  directly with raw E4 source-anchor values.
- `32340896270`: bounded selftest PASS with `anchor_decode=1`.
- `32341037385`: producer completed with the same INERT data, but checker
  rejected a receipt-only one-based cube-index offset.
- `32341939583`: final bounded selftest PASS with `cube_row_index=1`.
- `32342044284`: final full cross-check PASS.

Final marker: `B345_TRIPLE_CUBE_RAW_LAMBDA_CENSUS_CROSSCHECKED`.
