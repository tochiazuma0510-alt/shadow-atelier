# mine/ -- 採掘場(大規模探索基盤)v0

出所: 発案係 ideas_013(`ideas/ideas_013_solver_platform.md`)・裁定237(`sol/裁定_237_mine採用v0発注.md`)で v0 採用。
実装: implementer(worktree 隔離)。

**設計原理(§4.0 のとおり)**: 探索の数学(述語の中身)と、探索の工程(配車・分割・収蔵・照合)を物理で分離する。
`mine/` は工程だけを持つ。実装(`.g`/`.py`)と証明書は `search/` に置いたまま動かさない(パス不変・移動ゼロ — §7-1 の過渡期リスク対策)。

## v0 の範囲

- `mine-job/v1` schema(`mine/schema/mine-job-v1.schema.json`)+ preflight(`mine/preflight.py`)+ 統一配車 CI(`.github/workflows/mine-dispatch.yml`)+ collector 最小(`mine/collector/collect.py`)+ 梯子テンプレ(`mine/jobs/templates/ladder.json`)。
- backend は `gap-ci` のみ(sat-ci/py-ci は §4.5 の設計に予約済みだが v0 の実装対象外)。
- shard は driver に窓選択 knob がある場合のみ(v0 の第一号 `strike-a13-ladder.g` には無い → 非分割 1 job。裁定237 修正2)。
- 述語台帳(`mine/registry/`)は v0 では未整備。§7-1 の官僚化防止条項どおり「カード化は走った後でよい」— plan の `pipeline` は driver への名前付きポインタで代用する。
- LEDGER 行・地図 delta 案の自動生成は v1 以降(§6)。

## v1 配管で追加した物(裁定237 v1 範囲)

- **梯子 driver の窓選択 knob**: `search/strike-a13-ladder.g` に `LADDER_ONLY_WINDOWS`(窓 ID 文字列のリスト)を追加。bound なら窓をフィルタするだけ(判定ロジック・走査・cert 内容は無改変。未 bound なら従来と完全同一動作)。
- **shard matrix**: `resources.shards` が配列 `[{"name", "preamble"}, ...]` のとき、`mine-dispatch.yml` が matrix でシャード並列実行する(各シャードの preamble は `v0_driver.preamble` の後に連結)。driver.g 生成は python heredoc 直接生成方式(shell 展開を経由しない -- master 側の修理を踏襲)。
- **ジョブ専用 out_dir**: driver は引き続き `search/certs` 固定で書くが、実行前後の mtime 比較で「今回の実行で新規・更新された cert だけ」を `mine/out/<job_id>[/<shard>]/` へ回収し、artifact はそちらを収蔵する(分類不能 cert 混入の解消)。
- **certs メモ化索引**: `mine/collector/build_index.py` -- `search/certs/` を走査し `(window_id/canonical_id_sha256, generated_by, script_sha256)` の索引を `mine/index/certs_index.json` へ構築。完全な (UID×述語×版×impl_sha) 鍵は v1 後半に伸ばす(§4.7)。
- **LEDGER 行・地図 delta 案の下書き**: `collect.py --emit-ledger-draft` -- 検収レポートに加えて `mine/reports/<job_id>_ledger_draft.md`(LEDGER.md 様式の下書き+地図 delta 案 1 行)を機械生成する。**貼るのは人**。
- **述語台帳(最小)**: `mine/registry/` に XI-SCAN・PRUNE-ODD の 2 カード。preflight の (d) registry ゲートが、plan の `pipeline[*].predicate` がカード id を指す場合のみ `impl_sha256` の現物一致を検査する(カード無し述語は従来どおり無検査)。
- **[小修理] collector の checker cert 出所**: 対付け(§4.6)の checker(python)側 cert は `--artifact-dir` からでなく、常に `plan.crosscheck.checker_certs_glob` を repo ルート相対で glob して取る(v1 の staged out_dir には explorer 側 cert しか入らず対付けが 0/0 に落ちる事故の修理)。同じ window_id が artifact-dir 側にもあれば artifact 版を優先(v0 互換)。

## backend=py-ci(§4.5 予約設計の実装。2026-08-01 miner の事前検出対応で汎用化)

`resources.backend: "py-ci"` で python 照合器スクリプトを CI 上で走らせる。`v0_driver`(gap-ci)と対の橋渡し欄
`resources.py_driver`(`{script, sha256[, args, done_marker, result_count_check]}`)がスクリプトを指す。CLI 契約は
2 種類(後方互換):

1. **旧 u_meas 契約(無改変)** -- `pipeline[0].params.primes`(plan の params から渡す非空整数配列)がある場合。
   primes を CLI 引数にして起動する。最初の消費者は `search/probe/wac_v1/u_meas_caseb_locus2.py`
   (CLI: `<logpath> <primes...>`)。完走判定は run.log 中 `=== p = N ===` 見出しの出現数が `primes` 数と一致すること。
2. **汎用契約** -- `primes` が無い場合。`py_driver.args`(省略可・文字列配列)を CLI 引数にして起動する。完走判定は
   `py_driver.done_marker`(省略時 `"PY_DRIVER_DONE"`)が run.log に出現すること。`py_driver.result_count_check`
   (`{marker, expect}`・省略可)があれば `marker` の出現数が `expect` と一致することも必須にする(省略時はこの突合を
   スキップし done_marker 出現+exit 0 のみで done)。第一の消費者は `search/certs/ep_sweep744/run_laneb_sweep744.py`
   (CLI 引数なし・末尾で `PY_DRIVER_DONE` を print する)。

- **fail-closed**: どちらの契約でも exit code が非 0 なら即 `verdict=failed`(gap-ci の `DRIVER_DONE` マーカー検出と
  同水準の構造チェック。数学的な当否の判定はしない)。
- **provenance**: python バージョン・スクリプト sha256(preflight の integrity gate とは別に実行時点で再計算)・
  引数を run.log 先頭と result.txt に機械記録する。
- **収蔵**: スクリプトが書く log ファイル(out_dir 直下)を gap-ci と同じ mtime-diff ステージングで回収する。

## v0_driver 欄について

`resources.v0_driver`(`{script, sha256, preamble}`)は **v1 の述語カード化までの橋**。述語台帳が無いあいだ、plan は GAP driver を直接指す(名前付きポインタ)。**driver 自体の改変は禁止** — plan.universe.frozen_docs / resources.v0_driver.sha256 で「plan 凍結時から driver が 1 バイトも変わっていない」ことを preflight/CI integrity gate が強制する。v1 で述語台帳が棚入れされたら、`pipeline` は driver 直参照ではなくカード参照へ移行し、この欄は縮退させる。

## 職務境界(§5.1 の要旨。詳細は `.claude/agents/miner.md`)

| 行為 | 実行係(miner) | 司令塔/数学者 |
|---|---|---|
| plan 起票(テンプレ params 穴埋め) | ○ | 承認(negative-claim は必須) |
| preflight・発車(push)・監視 | ○ | -- |
| collector 実行・検収レポート提出 | ○ | レポートを受けて裁定 |
| 述語カード・universe generator の追加 | × | ○(三段レビュー) |
| 予言の作成・封印 | × | ○ |
| LEDGER・地図への貼り付け | ×(行の生成まで) | ○(貼付と裁定) |

## 起動手順(3 コマンド以内)

```
1. python mine/preflight.py mine/jobs/queue/<job>.json
2. git push                                                 # 発車(push が起動トリガー)
3. python mine/collector/collect.py --artifact-dir <回収ディレクトリ> --plan mine/jobs/queue/<job>.json
```

CI(`.github/workflows/mine-dispatch.yml`)は `mine/jobs/queue/*.json` の push(または `workflow_dispatch` の `job_path` 入力)で発火し、以下を行う:

1. **plan 発見**: push 差分(または `job_path` 入力)から対象 plan を特定。
2. **preflight**: `mine/preflight.py` をそのまま実行((a) schema (b) integrity (c) 予言ゲート)。1 つでも FAIL なら発車しない。
3. **backend 分岐**(§4.5): `gap-ci`(`setup-gap@v3.8.0` で `resources.v0_driver.script`(+`preamble`)を `-o 12g`・`resources.timeout_min` 分の timeout で実行)/ `py-ci`(`resources.py_driver.script` を `-o 12g` 相当の timeout 付きで実行 -- 引数は `pipeline[0].params.primes` があれば旧 u_meas 契約、無ければ `py_driver.args` の汎用契約。最初の消費者は `search/probe/wac_v1/u_meas_caseb_locus2.py`・`search/certs/ep_sweep744/run_laneb_sweep744.py`)。`sat-ci` は §4.5 の設計に予約済みだが未実装。
4. **収蔵**: `outputs.out_dir` の cert 群(py-ci はスクリプトが書く log ファイルを含む)+ `run.log` + `SHA256SUMS.txt` + `result.txt`(gap-ci: `DRIVER_DONE` マーカー検出、py-ci: 旧契約=exit code+結果数/対象数突合、汎用契約=exit code+done_marker 出現(+result_count_check)で `verdict=done`/`failed`)を artifact として upload。

collector は **CI の外**(実行係のローカル)で、DL した artifact に対して手動実行する(§5.2)。

## 禁止事項票

- `search/`(*.g・*.py・certs/)・`crosscheck/`・既存 workflow(`gap-run.yml`・`mb-search.yml` 等)・`docs/`・`sol/`・`ops/`・`provenance/` は本基盤からは**変更しない**(読み取りのみ)。
- 封印・金庫関連(`ep_handoff` を含む)には触れない。EP(`ninfty-*`)は接続点予約のみ(欄を `null` で置く。統合しない — §1.8)。
- plan の `universe`/`pipeline`/`predictions` 欄は実行係による書き換え禁止(テンプレ params の指定範囲のみ可)。
- 判定は cert JSON の値のみから行う(**ログ grep 禁止**)。collector はログファイルを一切読まない実装になっている。

## 検収チェックリスト(§5.3)

- `agreement` が全項目一致 → cross-checked 候補として裁定へ。片系統 → candidate(自動ラベル済み)。
- `prediction` 欄: 的中/外れ/NULL。外れは負の結果として地図 delta 案に自動反映(裁定で確定 — v0 は手動確定)。
- negative-claim: 三段 checker(drat-trim・lrat_check・cake_lpr)全通過 + mutant matrix 全緑 + 宇宙 sha 一致が昇格の必要条件(v0 は未実装 — v2 以降)。

## 判定 receipt(P88-R4-2・sol_reply_88_math15.md §2)

裁定235型「`PREDICTION_TO_MEASUREMENT_CONTAMINATION`」(予言値を実測欄へ手書き転記する事故)の恒久処方。
`mine/collector/receipt.py` が凍結 prediction 文書と cert JSON を**別入力**として読み、`mine/reports/<job_id>_receipt.md` を機械生成する。

- **実測欄は cert JSON からのみ機械抽出**(prediction 文書の値は予言欄にのみ引用として現れる。実測欄への手書き転記は経路自体が無い)。
- **恒等式 assert**: `|G|=|K||Q|`・`|K|=|K|_odd|K|_2`・`|Ξ(G)|=|G|`・`layer sum = total` を、cert に該当欄がある場合のみ評価して記帳する。
- **fail-closed な出所検査**: (1) `--prediction-doc` の実 SHA-256 が `--prediction-sha256` と一致しない、(2) `--prediction-map` の `source_sha256` が prediction-doc の実 SHA-256 と一致しない、(3) `--manifest` が `--cert` の実 SHA-256 を `windows[].cert_sha256` で束縛していない、のいずれかなら **`RECEIPT_GENERATION_STOPPED` で終了し md を書かない**。
- **予言欄・実測欄・派生判定欄は md 上でも節が分離**(§「予言欄」§「実測欄」§「恒等式 assert」§「派生判定欄」)。派生判定は予言欄の予言値と実測欄の cert 値を比較した結果(PASS/FAIL/NULL)のみを表示する。

予言側は prediction 文書を直接パースせず、`mine/collector/r4_prediction_map_v1.json`(`P-R4-0`..`P-R4-11` を cert フィールドへ対付ける表・予言値の引用のみで実測値は持たない・`source_doc`/`source_sha256` で凍結文書に束縛)を介す。単一 cert から判定できない予言(座標リスト本体が必要な `P-R4-4`・両枝比較が必要な `P-R4-8`)は `NULL` として誠実に記帳する(fabricate しない)。

使用例(検収実行時の実コマンド):

```
python mine/collector/receipt.py `
  --prediction-doc docs/notes/r4_prediction_v1.md `
  --prediction-sha256 a991f65a8c84a553b4d730a39cb3591c42e3fd6f3bfa05c2292fd56b2d66b78f `
  --prediction-map mine/collector/r4_prediction_map_v1.json `
  --cert search/certs/r4_W_E_A20_5x4t0_C_20260730.json `
  --manifest search/certs/r4_manifest_C_20260730.json `
  --job-id r4-C
```

`r=4` の C 枝・B 枝両方で実走し、`mine/reports/r4-C_receipt.md` / `mine/reports/r4-B_receipt.md` を検収済み(派生判定は Sol 便88 F88-2.2 の独立判定表と完全一致 -- C: PASS5/FAIL5/NULL2、B: PASS3/FAIL7/NULL2)。

## 第一号ジョブ

`mine/jobs/queue/ladder-recal-20260730.json` -- 梯子走査(T2)の**較正再走**(新窓ではなく既存 13 窓の CI 再発車、裁定237 修正1)。
driver = `search/strike-a13-ladder.g`(無改変)。結果が既知(裁定213/216 で 17/17・13/13 実績)なので、基盤のバグがあれば
collector の再現照合/対付け集計に即座に現れる = v0 の受け入れ試験そのもの。**push はしていない**(司令塔が検分後に実施)。
