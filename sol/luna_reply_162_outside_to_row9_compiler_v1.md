# Luna reply 162 — outside-to-row9 finite compiler (candidate-conditioned)

## Result and status boundary

The finite compiler exists for each of the two authenticated surviving
index-3 candidates, but the arithmetic receipt has `selected_A_cand=null` and
the independent verdict is `BLOCKED_UNKNOWN_ARITHMETIC_SELECTION`.  Therefore
the results below are **candidate-conditioned** for `IDX3-NN-09` and
`IDX3-NN-12`; neither is called the arithmetic image (A_{ar}).

For each candidate, a deterministic one-outside-letter search over the
alphabet

```text
[A generators, their inverses, x, x^-1]
```

found a word using the `x` letter (epsilon `+1`) for every outside row.  The
unused `x^-1` branch is retained in the declared alphabet; existence in the
full alphabet follows from the found `+x` word.  The search order is
lexicographic by A-prefix BFS distance, prefix token tuple, then row index;
the suffix is the corresponding reverse A-BFS path.  Each returned word was
literally replayed from the identity to zero-based row 9.

This is finite candidate replay only: `cross_checked=false`, `verified=false`.

## Pinned provenance

| input | bytes | SHA-256 |
|---|---:|---|
| `docs/week1-定義ノート.md` | 26498 | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` |
| `search/certs/d972_b4_word_key_artifact_v1_20260816.json` | 176474 | `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9` |
| `search/certs/nf972_sourcemap_a_tuples_v2_20260804.json` | 43751 | `cfa1f3a917e2cd9d21ceaa7f77539633ccb22e8585da8b3248609008d0391801` |
| `search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json` | 249817 | `1fca084f396605a8755534d19412a47f60af76406ca01a2ef99bc0c06f00e7d9` |
| `crosscheck/verdicts/d972_idx3_arithmetic_crosscheck_v2_20260823.json` | 8804 | `6fd63e3453854a02f504695876e246f1f9fa388a0b3018db4a15c84ec35db525` |

The receipt supplies the complete 324-row candidate rosters.  Its two
survivors have canonical-key roster SHA-256 values

```text
IDX3-NN-09  994df2d1bd03d97426e2257322e6c9fb2a101bfe5c4a5db8be10177c17f23364
IDX3-NN-12  e2dbe380afd89bffe5812c20a4d1e8392df566db7dedff3acf988323b9c438a9
```

The independent checker agrees on the two finite survivors, while explicitly
rejecting arithmetic promotion.  No producer/helper source was imported.

## Independent finite reconstruction

The 972 canonical tuples and 972 signed words were replayed independently:

```text
word -> D9^3 x PSL(2,8)                       972/972
distinct canonical keys                       972
identity and row-9 power law                  row9^4 = row36
candidate closure                             324/324 rows, each candidate
candidate + row9 closure                      972
```

The product is reconstructed from definition-note (3.53),

[
[m_1,f_1][m_2,f_2]=[2m_1m_2+m_1+m_2,
f_1E_{m_1,f_1}(f_2)],
\]

with the D9 law ((a,e)(b,d)=(a+(-1)^e b,e+d)) and the note's left-prepend
word convention.  The candidate generator rows are the receipt's
lexicographic generator sets:

```text
NN-09: [4, 10, 83, 164]
NN-12: [4, 11, 83, 164]
```

Both generated exactly the supplied 324-row roster.

## Compiler output

Canonical serialization used for the mapping digest is

```json
[[outside_row_index, [alphabet_token_positions...]], ...]
```

sorted by `outside_row_index`, compact JSON UTF-8, with token positions

```text
0..3 = A generators in listed order
4..7 = their inverses in listed order
8    = x
9    = x^-1 (unused by all returned witnesses)
```

| candidate | outside rows | length histogram | mean | max | mapping SHA-256 |
|---|---:|---|---:|---:|---|
| NN-09 | 648 | `{1:1, 2:9, 3:48, 4:163, 5:253, 6:152, 7:22}` | 4.8549382716 | 7 | `2cb4fea12eadb93d81a87b595b6bed813f41fb33dbfcb7843c3a8218876fc021` |
| NN-12 | 648 | `{1:1, 2:9, 3:48, 4:163, 5:253, 6:152, 7:22}` | 4.8549382716 | 7 | `440afe19f5cfe3db6157cbe812a8cd39607353251c76e400c6d88d89dc28d2a8` |

Representative words (token positions) are:

```text
NN-09:
  row 9:  (8)
  row 36: (8,5,5,5,0)
  max row 133: (2,8,5,6,6,1,0)

NN-12:
  row 9:  (8)
  row 36: (8,5,5,5,4)
  max row 128: (2,8,5,6,6,1,0)
```

Thus row 36 (the pinned R07 roof row) is outside in both candidates and has a
literal replay word.  Row 9 itself is also outside in both candidates and is
the one-letter positive control.

## Core, normality, and double cosets

Direct conjugate-intersection using ambient rows `[1,9,81,162]` gave, for
both candidates,

```text
normal(A)             false
|Core_X(A)|           162
coset action          S3 (candidate receipt and replayed index-3 geometry)
```

For representatives `x=1,9,36,133`, the stabilizer

```text
{a in A : x a x^-1 in A}
```

had size 162 in every case, hence

```text
|A x A| = |A|^2 / |A ∩ x A x^-1| = 324^2/162 = 648.
```

The observed double-coset size is therefore the full outside size; the
compiler's one-letter factorization has the expected form

```text
row9 = a0 * x * a1,     a0,a1 in A,
```

with epsilon `+1` for every returned witness.  Adding row 9 to the fixed A
generators generated all 972 rows, a destructive outside-mutation control.

## Controls and limitations

- `row9^4=row36` is retained under the reconstructed product law.
- Mutating the A roster by adjoining row 9 changes closure order from 324 to
  972; this rejects the “outside is in A” mutation.
- The first-324-rows and wrong-orientation shortcuts are not used as inputs;
  canonical keys, words, and closure are independently replayed.
- The two candidate digests differ, so a compiler digest does not choose the
  arithmetic orientation.  The missing marked Frobenius/local datum remains
  exactly the arithmetic-selection blocker recorded by the receipt.

No Git/GHA operation was performed.  Only this reply file is a persistent
change.

```text
OUTSIDE_TO_ROW9_COMPILER_CANDIDATE_CONDITIONAL_PASS
FINAL_MARKER=LUNA_162_OUTSIDE_TO_ROW9_COMPILER_CANDIDATE_CONDITIONAL_PASS
```
