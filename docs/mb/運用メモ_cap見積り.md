# Model-Builder 運用メモ — 1ジョブ600秒cap の見積りとシャーディング規則

2026-07-28 起草(委嘱3・司令塔指示「cap 見積もり規則を docs/mb/ の運用メモに明文化」)。

## 背景

委嘱2で `naff-branch-search-bound4-a5p1`(全域・シャーディングなし)が603.3秒で完走し、600秒capをわずかに超過した。バックグラウンド実行中に完走してしまい途中で打ち切れなかったため、以後は事前見積りでcap内に収める。

## 規則

1. **本走前に必ず小規模ラン(bound=1 または 2)を実測し、per-candidate cost(ms/候補)を得る。**
   - 例(委嘱2・N_aff): bound=2 で 25000点・21.7秒 → 約0.87ms/候補。
   - 例(委嘱3・N_infty): bound=2 で 625000点・17.15秒 → 約0.027ms/候補(N_aff より軽い — GCDでなく単一の多項式除算のため)。
2. **本走の候補点数(格子の全点数)を事前に計算し、per-candidate cost を掛けて見積り時間を出す。**
3. **見積り時間が 600秒 の8割(480秒)を超える場合は、実行前に分割する。** 分割の軸は探索変数のうち最も大きい離散レンジ(例: `c_N` の範囲・`p2` の範囲・`a5`の符号)を選び、各シャードの見積りが480秒以下になるよう区間を割る。
4. **シャーディングは独立ジョブとして実行し、各シャードの証明書を別ファイルに残す。** 全シャードの `tested` 合計が意図した全域候補数と一致することを確認する(委嘱2・3ではこれを明示的に突合した)。
5. **実測が見積りを超えた場合(委嘱2の a5=1 系列で最終シャードが577.9秒に達した例)は、次回はより小さいシャードへ切り直す。** 実測値は証明書の `elapsed_ms` に記録済みなので、次回見積りの実績値として使う(このメモの「例」欄を随時更新する)。
6. **fail-closed の記帳**: `skip_count`・`error_count`・`internal_error_count` のいずれかが1件でもあれば非零 exit(`process.exitCode=2`)にする実装を全 mb-* 探索器の標準とする(委嘱3で mb-naff/mb-w-branch/mb-w-branch-gaugefix/mb-w-branch-rational に導入済み)。cap超過そのものは fail-closed の対象ではない(完走していれば結果は有効)が、証明書に超過を明記する。

## 実測値ログ(随時追記)

| 探索器 | bound/範囲 | 候補数 | 実測時間 | ms/候補 |
|---|---|---|---|---|
| mb-naff-branch-search (stage1のみ支配的) | bound=2(全域) | 25000 | 21.7秒 | 0.868 |
| mb-naff-branch-search | bound=3(全域) | 201684 | 229.4秒 | 1.137 |
| mb-naff-branch-search | bound=4, a5=1, cN∈[-4,-1] | 236196 | 299.9秒 | 1.270 |
| mb-naff-branch-search | bound=4, a5=1, cN∈[1,4] | 236196 | 577.96秒(**cap8割超過**) | 2.447 |
| mb-naff-branch-search | bound=4, a5=-1, cN∈[-4,-1] | 236196 | 296.9秒 | 1.257 |
| mb-naff-branch-search | bound=4, a5=-1, cN∈[1,4] | 236196 | 297.5秒 | 1.260 |
| mb-ninfty-branch-search | bound=2(全域) | 625000 | 17.15秒 | 0.0274 |
| mb-ninfty-branch-search | bound=3(全域) | 9882516 | 309.6秒 | 0.0313 |

> **注**: mb-naff の cN∈[1,4] シャードだけ ms/候補が突出して大きい(2.447)。原因は未特定(同一形状の他シャードと比較して stage1 通過数は同数だが実行環境のばらつきの可能性がある)。次回はこの系列でさらに保守的な見積り(実測の最大値を基準にする)を使うこと。

## GitHub Actions 並列実行(委嘱4のインフラ・2026-07-28)

`search/mb-shard-plan.json` を push すると `.github/workflows/mb-search.yml` が起動し、シャードを並列実行する(書式は `search/mb-shard-plan.schema.md`)。ローカル実行(このメモの上記シャーディング規則)と Actions 実行は同じ探索器・同じ判定ロジックを使う——Actions はローカルの手動シャード分割を自動並列化する経路であり、判定ロジックには一切触れない。

- **ランナー仕様**: 公開(無料枠)ランナーは 4vCPU/16GB(`ubuntu-latest`)。同時実行数は既定で約 20 並列(組織/リポジトリのデフォルト上限。必要なら GitHub 側の設定で調整可能だが本タスクでは既定のまま)。
- **shard 粒度の目安**: 1 shard = 30 分目安(ローカルの 480 秒 cap より緩いが、再試行の粒度を細かくするため 30 分を上限の目安とする)。1 job あたりの絶対上限は GitHub Actions の 6 時間(360 分)。`shards[].timeout_minutes` で shard ごとに明示し、省略時は既定 60 分。
- **integrity gate**: job `plan` が (a) plan の JSON 構造検証(`search/mb-plan-validate.mjs`)、(b) `frozen_commit`(578b4fe 系)から凍結 5 文書を `git show <commit>:<path> | sha256sum` して plan 記載値と照合、(c) `search/mb-*.mjs` の sha256 を plan 記載値と照合、のいずれかに失敗すれば `search`/`collect` を起動せず即 fail する(`INTEGRITY_STOP`)。掃引範囲(bound・c_N/p2 範囲など)は `shards[].env` の環境変数で外出しし、探索器ファイル自体の中身は不変に保つ設計(sha256 一致で保証)。
- **証明書の集約**: job `collect` が各 shard の artifact(証明書 `.json`/`.err`・sidecar provenance)を `certificates/mb/actions/<run_id>/` へ集め、per-shard 成否の `summary.json` を添えて 1 コミットで master へ push する(ステージするパスは `certificates/mb/actions/**` に限定するガード付き)。

以後の本走(委嘱4以降)は、事前にローカルで見積り→本メモに実測値を追記→ plan ファイルへシャード分割を書き起こす、という手順を踏む(この点はローカル実行の規律と変わらない)。
