# mb-shard-plan.json 書式

Model-Builder 探索を GitHub Actions で並列実行するためのシャード計画ファイル。
`search/mb-shard-plan.json` への push が `.github/workflows/mb-search.yml` の
trigger になる(`workflow_dispatch` でも手動起動可)。

## トップレベルフィールド

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `schema` | string | ○ | `"mb/shard-plan/v1"` 固定。 |
| `frozen_commit` | string | ○ | 凍結正本の commit hash(578b4fe 系)。40 桁 or 短縮 7 桁以上。 |
| `frozen_docs` | array | ○ | 凍結 5 文書の `{path, sha256}`。`git show <frozen_commit>:<path>` の sha256 と一致必須。 |
| `searcher_files` | array | ○ | 探索器ファイル(`search/mb-*.mjs`)の `{path, sha256}`。現在のチェックアウト内容の sha256 と一致必須(判定ロジック不変の保証)。 |
| `shards` | array | ○ | 実行するシャードの配列(下記)。 |

## `shards[]` の各要素

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `shard_id` | string | ○ | 一意な識別子(ファイル名・artifact 名に使う。英数字・ハイフンのみ)。 |
| `script` | string | ○ | 実行する探索器のパス(例 `search/mb-naff-branch-search.mjs`)。 |
| `env` | object | - | 探索器へ渡す環境変数(例 `{"MB_NAFF_BOUND": "4", "MB_NAFF_CN_MIN": "1", "MB_NAFF_CN_MAX": "4"}`)。省略時は探索器の既定値(ローカル実行と同じ後方互換値)。 |
| `timeout_minutes` | number | - | このシャードの GitHub Actions ジョブ timeout。省略時は既定 60。 |

## 検証(job `plan`)

1. **JSON schema 検証**: 上記必須フィールドの存在・型を `search/mb-plan-validate.mjs` が機械的に検査する。
2. **integrity gate**: `frozen_docs` の各 `path` を `git show <frozen_commit>:<path> | sha256sum` で再計算し、`sha256` と全一致すること。不一致は `INTEGRITY_STOP` として即 fail。
3. **探索器ファイルの sha256 照合**: `searcher_files` の各 `path` を現在のチェックアウト内容で sha256sum し、`sha256` と全一致すること(判定ロジックが plan 作成時から変わっていないことの保証。掃引範囲は `shards[].env` の外出しパラメータで変えてよいが、`.mjs` ファイル自体の中身が変わっていないかはここで固定する)。
4. 上記 1-3 のいずれかが 1 件でも不一致なら job `plan` を fail させ、後続 job(`search`・`collect`)を起動しない。

いずれも `search/mb-plan-integrity-check.mjs` (2,3) と `search/mb-plan-validate.mjs` (1) が担う。
両スクリプトは探索器の判定ロジックには一切触れない(ファイル内容の再計算・比較のみ)。
