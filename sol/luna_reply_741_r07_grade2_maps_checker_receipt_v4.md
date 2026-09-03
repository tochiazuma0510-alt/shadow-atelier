# Luna Reply 741 — grade-two maps checker coverage-receipt v4

## Result

v490 の有限 checker receipt-key repair のみを versioned checker v4 に適用した。producer、workflow、数学、独立 arithmetic は変更していない。実 40-table check、git、GHA は行っていない。

`verify_coverage` の source-side receipt keys だけを producer manifest schema に合わせた。

```text
source_tags        -> tags
source_components  -> components
source_monomials   -> monomials
source_psl_indices -> psl_indices
```

`source_coordinates` と全 `destination_*` keys、値の列挙、coverage check は不変。selftest の対応 expected dictionary と checker pass marker だけを追随させた。

## Producer binding

Checker v4 は変更なしの producer v3 を厳密に pin する。

```text
path   search/d972_r07_grade2_forward_adjoint_maps_v3.py
SHA256 7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84
```

Producer artifact schema/marker は v3 のまま維持した。versioned checker terminal marker は `R07_GRADE2_FORWARD_ADJOINT_MAPS_V4_CHECKER_PASS`。

## Mechanical AST comparison

v3→v4 の top-level AST 差は次の三ノードだけだった。

```text
assignment: PASS_MARKER
function:   verify_coverage
function:   selftest
added top-level nodes:   none
removed top-level nodes: none
```

`verify_coverage` 差は四つの result key と同じ四つの lookup key の rename のみ。`selftest` 差は対応 expected dictionary の rename のみ。dense allocation、retry、parallelism、scan、refactor は追加していない。

## Bounded checks

bytecode cache を `%TEMP%/task741-pycache` に置き、次だけを実行した。

```powershell
python -m py_compile search/check_d972_r07_grade2_forward_adjoint_maps_v4.py
python -B search/check_d972_r07_grade2_forward_adjoint_maps_v4.py --selftest
```

結果:

```text
py_compile: PASS
selftest:   PASS
fixture_rejection_count: 13
producer_sha256: 7d6243901ef34b5c00e56e7be517beb8775fe83aedd277b23c4ed4fb29a72b84
```

既存 parser、transpose、inverse、prefix、bool/type、roster、canonicality、truncation/trailing-byte、malformed-coverage mutation fixtures はすべて維持されている。

## Output receipts

| file | bytes | LF lines | final LF | SHA-256 |
|---|---:|---:|---:|---|
| `search/check_d972_r07_grade2_forward_adjoint_maps_v4.py` | 49,643 | 1,013 | yes | `7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29` |
| `sol/luna_reply_741_r07_grade2_maps_checker_receipt_v4.md` | self-referential reply | LF-only | yes | supplied externally after sealing |

```text
CLASSIFICATION=FINITE_CHECKER_RECEIPT_KEY_REPAIR
ACTUAL_MAP_CHECK=DEFERRED_TO_GHA
ACTUAL_MAP_ARTIFACT=NOT_YET_ACCEPTED
GRADE2_DECISION=NOT_RUN
verified=false
```
