# ツール総点検 — 事例・潜在需要・対応表と backlog(2026-07-26)

> 発注: 司令塔(研究者指示・仕様書優先の原則 = docs/体制と道具.md「質問の免許」3)。
> 担当: 運用改善担当(本セッション)。方針: **誤用対策は錠でなく仕様書と拡張** — 各事例の
> 「弾いた/詰まった」箇所に潜在的な正当需要を認め、安全なものはその場で実装した。
> 裏取りソース: ops/codex_activity*.log・provenance/LEDGER.md・docs/notes/・git 追跡状態。

## 総点検表(事例 → 潜在需要 → 対応)

| # | 事例(裏取り) | 潜在的な正当需要 | 対応 |
|---|---|---|---|
| 1 | wake_codex.mjs: 主レーン起床が sol2 稼働中に taskkill 巻き添えの危険 → ガードで拒否(restriction)。拒否されたメッセージは inbox に滞留し、誰も再発火しない | **レーンのキュー運用**: 起床要求を弾かず enqueue し、codex 終了時に自動発火 | **済(実装)**: `ops/bin/wake_queue.jsonl`(キュー)+ wake_codex.mjs v2(SKIP→ENQUEUED・dup 検出・retry 上限 10)+ `ops/bin/wake_queue_drain.mjs`(終了フック/monitor/手動の 3 経路・lock で多重発火防止・1 回 1 件・空キュー仕様はヘッダ明記)。常駐なし(8GB 制約) |
| 2 | sol2 の OOM 死が約 40 分〜65 分未検知(死亡 ~04:15 UTC → 起床 05:20 UTC・sol2 ログ L1578 に turn end 欠落・検知は研究者の目視)。同時刻帯に main ログ L330374 の turn も turn end 欠落(巻き添え死の痕跡) | **打ち上げ後の死活監視の標準装備**: launch/wake が軽量 monitor を自動起動し、「プロセス消滅かつ返信ファイル未作成」で ops/express/ に自動速達 | **済(実装)**: `ops/bin/turn_monitor.ps1`(新設)+ launch_wake.ps1 統合(全 launch/wake で自動起動・-ReplyFile/-NoMonitor 追加)。判定 4 種(NOTURN/OK/ALERT(turndeath)/ALERT(noreply))・ALERT は express 自動速達(常駐 express 監視が拾う)・OK 時は drain も駆動 |
| 3 | watch_log.ps1 ビューアが「動いているのか止まっているのか分からない」(研究者が二度質問) | **死活表示**: 最終更新経過秒と codex プロセス生存をビューア自身が示す | **済(実装)**: v3 — タイトルバーに「upd Ns ago・codex.exe ALIVE xN [pids]/GONE・時刻」を 5 秒毎更新(-StatusSec)。Get-Content -Wait を自前ポーリング(FileShare+stateful UTF8 decoder)に置換し、無更新時もタイトルが動き続ける |
| 4 | GAP 既知罠を各実装者が個別に踏み直し: Concatenation 単一引数クラッシュ(LEDGER L319)・JoinC O(n²)(LEDGER L100-115・437 秒事故)・600 秒 cap・PrintTo 整形改行。JoinC は 15 ファイルに逐語コピー(うち線形版は 2 ファイルのみ) | **共通ヘッダライブラリ** | **済(実装)**: `search/gaplib_common.g`(gaplib/v1・最小版) — 線形 JoinC+JSON ヘルパー(既存とバイト互換)+壁時計 cap タイマー+罠コメント集 7 件(`^` 右作用規約・prepend 語規約含む)。**新規スクリプト専用・既存は書き換えない**(発注条件) |
| 5 | 証明書スキーマの版文字列が家系ごとにばらばら | スキーマ台帳と統一規約 | **backlog(実装せず・下記 §2 に現状一覧と統一案)** |
| 6 | 定義漏れによる implementer ブロック 2 回(U-F7 restricted 定義式欠落 → 司令塔追給・(q_θ)₊ 射影定義未確定 → 保留のち裁定 20)— いずれも「止まって訊く」が機能 | ブロック時の標準復旧手順の明文化 | **済(1 行追記)**: docs/体制と道具.md「質問の免許」3 末尾に「定義漏れブロック時は ops-clerk の定義限定抽出が標準(期待値は渡さない)」 |
| 7 | (追加発見)ガード判定・起床結果の console 出力(SKIP-WAKE/ZOMBIE-DETECTED/WAKE-DONE 等)が launch_wake.ps1 の Hidden 起動で全て消失 — 両活動ログに SKIP/ZOMBIE の記録 0 件・turn end 欠落の事後説明が不可能だった | **配車記録**: ガード判定と発火結果の永続ログ | **済(実装 1 に統合)**: `ops/wake_dispatch.log` — wake/drain/monitor の全判定を [wake]/[drain]/[monitor] タグで追記(gitignore 済) |
| 8 | (追加発見・**要司令塔処置**)`ops/bin/codex_session_id_sol2.txt` と `ops/codex_activity_sol2.log` が **git 追跡済み = public リポジトリで公開中**。.gitignore が 3 ピンの個別列挙で、後から出来た sol2 系が漏れた(LEDGER 2026-07-26「公開除外 … codex_session_id*.txt」決定に反する) | 公開除外決定の機械的な貫徹(glob 化) | **一部済**: .gitignore を glob 化(`codex_activity*.log`・`codex_session_id*.txt`)+注記。**残り(司令塔・コミット時)**: `git rm --cached ops/codex_activity_sol2.log ops/bin/codex_session_id_sol2.txt` で untrack(履歴には残るため、sol2 ピンは次の -Renew で新 id に回転すれば漏洩 id は失効) |
| 9 | (追加確認)Sol 便 05 の 503/401 障害(LEDGER 2026-07-25)は手動の再試行判断・間隔拡大・研究者への再ログイン依頼で対処 | 起床失敗(exit≠0・API 障害)の再試行政策の標準化 | **backlog(§3-b)**: monitor(実装 2)が turn 死は検知するようになったが、503/401 の区別と自動 backoff は未実装 |

## §2 証明書スキーマ家系の現状一覧と統一案(事例 5・実装せず)

### 現状(2026-07-26 実地 grep・全 search/ crosscheck/ certificates/)

| 家系(版文字列) | 使用ファイル | 特徴 |
|---|---|---|
| `gtsh-cert/v1` | suite-wp2-explorer.g・-q1836.g・shard-{a,b,b1,b2}.g・smallgroup32-scan.g・sg32-admissibility.g | 正本定義 docs/wp2-transversal-model.md。`schema` 欄あり |
| `gtsh-cert/v2` | week3-battery-{1a,1b,2a,2b,3}.g(battery-3 は f_word を「v2.1 互換拡張」として追加・schema 欄は v2 のまま — 内容拡張が版文字列に現れない前例) | 正本定義 search/manifest_spec_v1.md §1.4 |
| `gtsh-cert/v2-psl` | week3-psl-S*.g | 正本定義 search/manifest_spec_v2_psl.md §1.5(v2 全欄継承+追加) |
| `a5-dessin-crosscheck/v1` | a5-dessin-crosscheck.g | 単発家系・`schema` 欄あり |
| (無印・e2sweep 家系) | e2-sweep-r2.g → certificates/e2sweep/ | **`schema` 欄なし**。版情報は `method`(例 `left_kernel_mod_prime_power/v1`)とコメント「v3 sec.3.3(A) schema」に分散 |
| (無印・e2c6 家系) | e2c6-sweep.g → certificates/e2c6/(凍結ビルド・読み取りのみで確認) | **`schema` 欄なし**。`claim`+`method`+`ob_mode`(`PENDING`/`quotient-ratified-v2`)+`fixture` 欄。ob_mode は「仕様の刻印」として機能中(体制と道具.md の裁定どおり) |

### 統一案(採否は司令塔)

1. **最上位 `schema` 欄を全証明書の必須欄にする**(家系名/版: `<family>/v<N>`)。e2 系のような
   claim/method 分散型も、既存欄はそのまま + `schema` を追加するだけで適合できる。
2. **家系レジストリを 1 箇所に**: `provenance/cert-schemas.md`(新設・追記専用)に
   家系名・現行版・正本定義文書・書き手スクリプト・照合器を 1 行ずつ。新家系はここに登録してから書く。
3. **版繰り上げ規則**: 欄の追加=マイナー(v2→v2.1 で **schema 文字列も上げる** — battery-3 の
   「内容は v2.1・文字列は v2」の前例を再発させない)。欄の意味変更・削除=メジャー。
4. **`ob_mode` 型の刻印は家系内欄として存続**(錠でなく仕様の刻印 — 研究者裁定)。照合器の
   REJECT 条件は刻印と値の整合のみ(e2c6 のモード錠が現行の手本)。
5. **移行は新規のみ**: 凍結済み証明書・ハッシュ台帳記録済み家系は書き換えない(byte 同一性の保護)。
   照合器の「schema 欄必須」検査は新家系からの適用。

## §3 その他 backlog(小粒・優先度順)

- **(a) 司令塔処置(至急・コミット時)**: 表 #8 の untrack 2 件+sol2 ピンの回転(-Renew)。
- **(b) 起床失敗の再試行政策**(表 #9): wake exit≠0 を monitor が区別(503=間隔拡大の自動再キュー・
  401=再試行停止+express)。現行 v1 は「turn 死・返信欠落」のみ検知。
- **(c) ops-clerk.md の 1 行更新(次セッション反映)**: 「SKIP-WAKE ならそのまま」→「ENQUEUED なら
  そのまま(自動発火する・状況は ops/wake_dispatch.log)」。agent 定義はセッション起動時読み込みのため
  本セッションでは書き換えず記帳のみ。
- **(d) launch_new.mjs の dispatch ログ対応**: 現在 [wake]/[drain]/[monitor] のみ。launch_new の
  console 出力(PINNED/CODEX-ALREADY-RUNNING 等)も Hidden 起動では消失する — 同じ dlog 方式を
  次の改修で(今回は発射系の変更を最小化するため見送り)。
- **(e) 既存 GAP スクリプトの JoinC 統一**: 発注条件により見送り(LEDGER 2026-07-19 の
  「JoinC の統一は将来の別便で」を再確認)。移行するなら証明書ハッシュ再照合とセット。
- **(f) es7ops MCP の分離**: 既存 backlog(ops/README.md「既知の混線リスク」)— 変化なし・継続。

## §4 実装 4 件の所在(仕様ヘッダは各ファイル先頭)

| 実装 | ファイル |
|---|---|
| キュー運用 | `ops/bin/wake_queue_drain.mjs`(新)・`ops/bin/wake_codex.mjs`(v2 改修)・キュー実体 `ops/bin/wake_queue.jsonl`(自動生成・gitignore) |
| 死活監視 | `ops/bin/turn_monitor.ps1`(新)・`ops/bin/launch_wake.ps1`(統合改修・-ReplyFile/-NoMonitor) |
| ビューア死活表示 | `ops/bin/watch_log.ps1`(v3) |
| GAP 共通ヘッダ | `search/gaplib_common.g`(gaplib/v1・新規スクリプト専用) |
| 配車記録(追加) | `ops/wake_dispatch.log`(自動生成・gitignore) |
