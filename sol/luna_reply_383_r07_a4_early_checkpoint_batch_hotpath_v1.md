# Luna reply 383 - A4 early checkpoint / batch hot path v1

## 結論

指定された 3 executable を新規作成した。v12/v14 の数学的 oracle は変更せず、
自然な completed-row 境界での早期 checkpoint、partial canonical chunk の厳密な
resume、進捗表示、v13 producer pin、PRODUCTION/RESUME driver を実装した。

bounded multi-column batch は **exactly blocked** とした。現行 schema は
`selected`、B 挿入順、`query_event_chain`、`epoch_digest`、terminal digest、K recurrence
を履歴として固定し、checker は `initial` と boundary event/terminal/epoch digest、
chronological K roster を producer と完全一致させる。checker 側だけ異なる候補順・
pivot 順にすると、同じ最終 span でもこれらが意図的に相違する。要求された
「異なる順序で計算し、最終空間と ancestry で照合」へ移すには receipt/checkpoint
schema、canonical ancestry、positive comparator をまとめて変更する必要があり、
小さな hot-path patch では数学的意味を維持できない。したがって singleton 選択を
勝手に batch 化していない。

## 成果物 identity

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v13.py` | 9731 | `c8e93ba9b72971428f2a8dba96049e183bfe1d794ac6008cb6495e6d5661f514` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v15.py` | 10487 | `7779d545a679580130a0a191705f96e32834e67eaed37eb934e79aa7875a932d` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v22.g` | 5627 | `30e9929950536f4073b08d01682e6c3ba2db2ace45357799aa6df14e775a6bdd` |

返信票自身は hash の自己参照になるため表から除外した。

## Frozen owners

- producer owner v12: 7209 bytes,
  `816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5`
- transitive producer v6: 219187 bytes,
  `aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a`
- checker owner v14: 8074 bytes,
  `7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47`
- transitive checker v6: 258847 bytes,
  `432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf`
- driver owner v6: 13775 bytes,
  `a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0`

各 wrapper は owner と transitive source を byte/SHA pin し、v12/v14 の全 patch を
cardinality 1 で復元してから、今回の各 patch site も cardinality 1 で適用する。
復元後 source は producer 223193 bytes /
`9513a1d1bddd6f9159c65ae273c50e8af5a9635a61efc02e0c1f566782ad53fe`、
checker 262937 bytes /
`6b2173b7dd2dd873a6fa112a06ef51f1719f3c494fbeb4329a26164c4c2caff9`。

## Early checkpoint と resume

completed-row cadence は両側とも次である。

```text
4, 8, 12, 16, 20, 24, 28, 32,
64, 128, 256, 512, 1024, 2048, 3072, 4096, 5120, 6144, 6441
```

checkpoint 呼出し位置は row の affine/bridge replay、oracle terminal、必要な K 受理と
queue 追記がすべて完了した後であり、half-mutated query は serialize しない。
atomic replace、counter envelope、authority/code identity、row/bridge prefix、B/K basis、
raw ledger、word DAG ancestry、queue state は従来 owner のまま保存される。

早期 checkpoint は canonical 1024-row chunk の途中に位置するため、旧コードの
`last chunk end == next_row-1` はそのままでは resume を拒否する。v13/v15 は、

- `row_digests` 全 prefix と `row_prefix_canary` を従来どおり seal する、
- 完了済み canonical chunk end の列が
  `1024,2048,... <= row_cursor` と厳密一致することを検査する、
- 未完 canonical chunk tail を許し、次の canonical boundary まで同じ
  `chunk_start` から継続する、
- nested `consume_row` に必要な `nonlocal chunk_start` を明記する、

という最小修正を行った。これにより row 4 checkpoint (`next_row=5`, chunks `[]`) も
正当で、row 1024 到達時には canonical chunk 1..1024 が一度だけ閉じる。

最初の v13/v15 run は code SHA が変わるため FRESH である。最初の row-4 atomic seal
以後、resource stop は直前の completed-row checkpoint を参照し、同じ v13/v15 で
RESUME できる。各 snapshot は従来の current 400,000,000 bytes、additive
2,000,000,000 bytes cap を引き続き強制する。

## Observability

追加計算なしで、最大 1 行/60 秒に制限した `A4_PROGRESS` は次を報告する。

```text
phase current_row completed_row combined_rank boundary_rank K_rank
correlation_rounds accepted_batch_size elapsed rss_bytes
durable_checkpoint_row membership_queries correlation_pairs
```

`correlation_rounds` は既存の完全 correlation 呼出しを数える。batch は未実装なので
`accepted_batch_size` は現行 singleton round の正直な 0/1 である。rank は既存 basis
の長さ、RSS は既存 Meter sample、durable row は atomic write 成功後だけ更新する。

## Driver

`D383Mode` は `PRODUCTION` または `RESUME` のみを受け付け、復元した v6 driver の
既存 fresh/resume shell 分岐をそのまま使う。v13/v15 の exact pins、v22diag receipt /
verdict / producer-checkpoint / checker-checkpoint / logs を設定した。内部 limit は
14,400 秒 / 8,000,000,000 bytes、外部 timeout は既存どおり 14,520 秒である。

shell が positive sentinel を作れなくても outer driver は Error にせず、producer と
checker の各末尾 65,535 文字を常に表示し、capture marker を出す。したがって
UNKNOWN receipt/checkpoint/log は artifact upload のために残る。driver marker は
数学的 PASS の代用ではない。

## 静的確認

- Python wrapper ASCII decode / AST parse: PASS
- v12/v14 frozen restoration、全 patch cardinality、復元 source AST parse: PASS
- 復元 module の非-main static load、14,400 秒 / 8 GB cap、checker の v13 pin: PASS
- cadence、`nonlocal chunk_start`、partial-prefix predicate、progress field の一意性: PASS
- v22 の frozen-v6 replacement 全 cardinality、v13/v15 physical pin: PASS
- GAP `ReadAsFunction` parse (`gap.ps1` 経由): PASS

production、GHA、git、network、SELFTEST、mutation campaign は実行していない。

## 残余リスク

- row-4 snapshot の実測 bytes/serialization time は production 未実行のため未知。ただし
  object/additive cap と atomicity は fail-closed のままである。
- restore は保存済み insertion event / word ancestry を再演するため、checkpoint が大きく
  なった後の replay cost 自体は今回短縮していない。
- multi-column batch の速度向上は上記 schema/history blocker により得られていない。

```text
RUN 33250865356 MATHEMATICAL TERMINAL:            UNKNOWN_RESOURCE
EARLY COMPLETED-ROW CHECKPOINT:                   IMPLEMENTED
BOUNDED EXACT COLUMN BATCH:                       EXACTLY BLOCKED
FUTURE RESOURCE STOP RESUMABLE:                   YES AFTER FIRST V13 CHECKPOINT
A4 ACCEPTED WORD-BEARING K:                       NOT YET COMPUTED
```

`TASK383_A4_EARLY_CHECKPOINT_BATCH_HOTPATH_COMMISSIONED`
