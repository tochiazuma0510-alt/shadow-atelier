# Luna 371 — A0 v20 RSS/checkpoint 最小修理

## 結論

指定された最小 production path を v20 として実装した。重いローカル本番と
SELFTEST は実行していない。数学、500,000,000 boundary-pair cap、10800 秒 cap、
入力 owner は intended v19 から変更していない。

作成物:

| role | path | bytes | SHA-256 |
|---|---|---:|---|
| producer | `search/d972_r07_history_free_positive_fast_resume_v20.py` | 10739 | `cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7` |
| checker | `crosscheck/check_d972_r07_history_free_positive_fast_resume_v20.py` | 5327 | `7c0a1c8b862f8dd62224e0f4ebc0d50ae7ea2de86c63ffb67e025cba98d7c077` |
| GHA driver | `search/d972_r07_history_free_positive_fast_resume_gha_driver_v20.g` | 6907 | `f9cfffc8e38082a4ff4d24b608ccb0eab5d9a53ba36169264d440827ad6918d4` |

## 修理した4点

1. **empty-new deletion gate**

   producer/checker の双方に専用 `_delete_once` を置いた。`old` の出現数が正確に
   1、削除後 0、かつ byte 長差が `len(old)` と一致することだけを検査する。
   `bytes.count(b"")` は一切呼ばない。descriptor inverse canary は一度だけ残し、
   worker/parent/checker の pair ごとの重複 canary をこの gate で削除する。

2. **2 workers 固定と cache 撤去**

   producer の CLI は `choices=(2,)`, `default=2`、owner constructor も
   `workers == 2` のみ受理する。checker の実 COMMON replay、boundary owner、
   UNKNOWN_RESOURCE checkpoint owner も 2 のみ受理する。driver は CPU 数を見ず
   常に `workers=2` を渡す。v19 の process-lifetime `_FORK_DECODE_CACHE` は導入せず、
   frozen v13 の epoch-local decode に戻したため無制限 cache は存在しない。

3. **checkpoint DAG の再帰的 tuple 正規化**

   producer は JSON の nested list を再帰的 tuple にしてから hash-cons duplicate
   検査および `ancestry.nodes`/`intern` 復元を行う。出力時は逆に再帰的 list 化し、
   復元直後の round-trip equality も検査する。checker は helper 非共有の独自
   recursive freezer を使って nested literal node を hashable にしてから検査する。
   これにより run 33247540982 の `TypeError: unhashable type: 'list'` 経路を除去した。

4. **UNKNOWN_RESOURCE artifact/terminal path と進捗**

   checker は従来の独立な seal/source/checkpoint/monitor/worker-cleanup 検査を通し、
   driver は producer/checker の terminal を各1行抽出して byte 一致を要求する。
   `UNKNOWN_RESOURCE` は sidecar があるか `checkpoint_required:false` の場合だけ
   v20 sentinel `R07_HISTORY_FREE_POSITIVE_FAST_RESUME_V20_DRIVER_PASS` に到達する。
   producer の一分間隔ログは毎回
   `boundary_pairs,candidate_words,retained_columns,dag_nodes,parent_rss,children_rss`
   を表示する。

## 静的確認

以下を実行し、両 wrapper の frozen-owner pin、全 substitution cardinality、生成後
Python compile/definition load が exit 0 になった。

```text
python -B -c "import runpy; runpy.run_path(r'search/d972_r07_history_free_positive_fast_resume_v20.py', run_name='r07_v20_static')"
python -B -c "import runpy; runpy.run_path(r'crosscheck/check_d972_r07_history_free_positive_fast_resume_v20.py', run_name='r07_v20_checker_static')"
```

## GHA 間 sharding の扱い

親の最終優先指示どおり v20 最小版からは切り離した。現 boundary loop の raw pair
ordinal を単純に `mod N` 分割すると、同じ translated-column key への F3 寄与が
複数 shard に跨り相殺し得る。その場合 partial nonzero を単独 MEMBER と扱うのは
不健全である。安全な positive-only shard の最小荷重点は、translation key を一度
だけ所有者決定した後、同一 key の全寄与を必ず同じ shard に送る prepartition
stage である。重複 full scan なしにこれを行う owner/merge ABI は本便では作って
おらず、shard completeness や NONMEMBER を架空出力していない。
