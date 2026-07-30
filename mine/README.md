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
3. **backend=gap-ci 実行**: `setup-gap@v3.8.0`(GAP 4.16.0)で `resources.v0_driver.script`(+`preamble`)を `-o 12g`・`resources.timeout_min` 分の timeout で実行。
4. **収蔵**: `outputs.out_dir` の cert 群 + `run.log` + `SHA256SUMS.txt` + `result.txt`(`DRIVER_DONE` マーカー検出で `verdict=done`、無ければ `failed`)を artifact として upload。

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

## 第一号ジョブ

`mine/jobs/queue/ladder-recal-20260730.json` -- 梯子走査(T2)の**較正再走**(新窓ではなく既存 13 窓の CI 再発車、裁定237 修正1)。
driver = `search/strike-a13-ladder.g`(無改変)。結果が既知(裁定213/216 で 17/17・13/13 実績)なので、基盤のバグがあれば
collector の再現照合/対付け集計に即座に現れる = v0 の受け入れ試験そのもの。**push はしていない**(司令塔が検分後に実施)。
