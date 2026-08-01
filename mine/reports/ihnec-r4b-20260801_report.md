# mine 検収レポート -- ihnec-r4b-20260801

- job_id: `ihnec-r4b-roof-20260801`(plan ファイル名 `mine/jobs/queue/ihnec-r4b-20260801.json`)
- run_id: `30697198947`(GitHub Actions run)
- plan: `mine/jobs/queue/ihnec-r4b-20260801.json`(裁定385・12 shard)
- driver: `search/probe/wac_v1/ihnec_r4b_run.g`
- 値は全て `result.txt` / cert JSON(`ihnec-r4b/v1` schema)の機械抽出のみ(手写しなし・判定はしていない)。

## GHA 実行結果原文

- `gh run view 30697198947` -- `plan` ジョブ + 全 12 `gate-and-run` shard ジョブとも `conclusion=success`。
- `result.txt` ベースの内部 verdict も **12/12 全て `verdict=done`**、`gap_exit_code=0`(conclusion と verdict が一致 -- 修理版 workflow の fail-closed 昇格ステップは今回発火しなかった=正常系)。

| shard | verdict | gap_exit_code | gap_max_rss_kb | run_log_bytes |
|---|---|---|---|---|
| m0 | done | 0 | 173424 | 1892 |
| m2 | done | 0 | 173660 | 1892 |
| m3 | done | 0 | 174312 | 1892 |
| m5 | done | 0 | 174588 | 1893 |
| m6 | done | 0 | 173960 | 1892 |
| m8 | done | 0 | 173660 | 1893 |
| m9 | done | 0 | 174776 | 1892 |
| m11 | done | 0 | 173840 | 1897 |
| m12 | done | 0 | 174496 | 1896 |
| m14 | done | 0 | 174000 | 1897 |
| m15 | done | 0 | 174604 | 1897 |
| m17 | done | 0 | 175920 | 1896 |

全 shard の `gap_max_rss_kb` は約 170MB(見積り 264MB より低く、cap 12GB に対して大幅余裕 -- 予算どおり)。`run_log_tail_hex` はいずれも末尾 `IHNEC_R4B_DRIVER_DONE`(DRIVER_DONE マーカー相当)で終わっている。

## cert 集約(12/12 生成・機械抽出)

各 shard は単一 m 値を担当(`shard.target_ms`)。`ihnec-r4b/v1` cert の主要欄をそのまま列挙する。

| shard(m) | k9_alone_shadow_total | k9_alone_pass | s4_alone_shadow_total | s4_alone_pass | scan.shadow_total | shadow_accounting_balances | p_ihn_1 (incomparable/prediction_matches) | p_ihn_2 (pb3_over_m=1469664 pass) | p_ihn_3 (m_ord=18 pass) |
|---|---|---|---|---|---|---|---|---|---|
| m=0 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=2 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=3 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=5 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=6 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=8 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=9 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=11 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=12 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=14 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=15 | 108 | true | 54 | true | 81 | true | true/true | true | true |
| m=17 | 108 | true | 54 | true | 81 | true | true/true | true | true |

**K9=108/S4=54 アンカー**: 12 shard全てで `k9_alone_shadow_total=108`(`k9_alone_pass=true`)・`s4_alone_shadow_total=54`(`s4_alone_pass=true`) -- 依頼にあった既知アンカー値と機械照合して一致。

**shadow_total(全体)**: 各 shard の `scan.shadow_total` は 81 で共通(charming_set_m の12元それぞれに対して等しい値)。**Σ = 81 × 12 = 972**(機械集計)-- 依頼にあった `shadow_total=972` の欄と一致。

## 出所整合(fail-closed 検査・診断)

- 12 cert 全ての `provenance.script_sha256` は単一値 `5bf6bc551eb7309c0b83adc363c15985973d9cb04e2cde9e7e34fe45c5277aa2` で一致し、plan の `universe.frozen_docs[0].sha256`(`search/probe/wac_v1/ihnec_r4b_run.g`)と一致(driver 差し替えなし)。
- shard 数: plan 記載 12 / ダウンロード済み 12 -- 一致。
- 各 cert の `shard.target_ms` は plan の `resources.shards[].preamble` の `R4B_TARGET_MS` と 1 対 1(m0, m2, m3, m5, m6, m8, m9, m11, m12, m14, m15, m17 -- 12件、charming_set_m の18元中12元)。
- `cross_checked_status.status = "n/a"`(cert 自身の記載): 単系統 GAP 探索であり cross-checked は主張していない旨が cert 内に明記されている(R4a との入力非共有による独立再現ではあるが、二独立実装照合ではない)。

## 集計まとめ

- verdict: done 12/12
- cert 生成: 12/12
- K9アンカー(108) pass: 12/12
- S4アンカー(54) pass: 12/12
- shadow_total 総和: **972**(機械集計 = 81×12)
- p_ihn_1/2/3: 12/12 shardで pass=true(単一cert内の自己検査欄。予言との突合・裁定は行っていない)

(本レポートは result.txt / cert JSON の機械抽出のみであり、判定・裁定・LEDGER貼付は行っていない。)
