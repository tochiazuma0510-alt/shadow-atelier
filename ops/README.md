# ops — 司令塔(Claude)⇔ Sol(Codex CLI)の連絡と自動起動

ES7 の郵便箱一式(`atelier_lean/ES7/ops/`・実証済み)の影工房移植版。2026-07-18 開設。

## 配達体制(誰が何を運ぶか — ES7 §5「TOP 同士が書くのをやめる」の継承)

| 通信 | 書く者 | 配達する者 |
|---|---|---|
| キックオフ・裁定(契約級) | **司令塔** が `sol/` にファイルとして書く | **スクリプト**(`launch_wake.ps1` — 一行指示はファイルへのポインタのみ) |
| Sol の監査・返信(契約級) | **Sol** が `sol/sol_reply_*.md` に書く | ファイル到着を **Monitor が自動検知**(done 通知は不要 — ES7 と違い司令塔側が常駐監視) |
| 運用連絡(定型) | 原則**スクリプト**。郵便処理は **ops 事務員**(`.claude/agents/ops-clerk.md`・haiku)に委譲 | 同左+wake |
| **Sol → Luna の実装指示** | **Sol** が `sol/luna_task_NN_*.md` に指示書を書く(数学成果物扱い・自分では実装しない) | **司令塔が点検**(停止ゲート・規律違反の一瞥)→ **ops 事務員**が `-Role luna` で起動・配達。Luna の返信は `sol/luna_reply_NN_*.md` → 次便で Sol が検収 |
| **Sol は ops の便りを書かない**(ES7 規約)— Sol の出力は数学成果物のみ(reply と luna_task) | — | — |

- Luna(実装増援)を起こす日が来たら: **Luna 専用セッション+専用ピン**(`codex_session_id_luna.txt`)を新設し、
  Codex 側の ops 便り担当は Luna に置く(ES7 と同配置)。Sol のピンと混ぜない。

## 自動起動の仕組み

- **セッション運用(ES7 準拠)**: **便ごとに新規セッション**(2 便目以降は `-Renew` で旧ピンを履歴に退避)。
  文脈はファイルで渡す(キックオフに前便 reply への参照を書く)。
  **wake は同一便内のフォローアップ専用**(ピン ID に `codex exec resume`)。
  ```powershell
  ops\bin\launch_wake.ps1 new  "<一行指示>"                        # Sol 便(sol/max 固定・override 不可)
  ops\bin\launch_wake.ps1 new  "<一行指示>" -Renew                 # 新しい便(旧ピンを履歴へ)
  ops\bin\launch_wake.ps1 new  "<一行指示>" -Role luna             # Luna 便(luna/high・専用ピン)
  ops\bin\launch_wake.ps1 new  "<一行指示>" -Role luna -Effort xhigh   # Lean shard 級(medium=定型)
  ops\bin\launch_wake.ps1 wake "<理由>" [-Role luna] [-Effort ...]     # 便内フォローの起床
  ```
- **推論設定の強制**: 起動・起床の両方でモデルと effort をフラグ明示(config 既定への依存を排除)。
  Sol = max 固定(--effort 指定は拒否)。Luna = medium/high/xhigh(既定 high)。resume にも同フラグを付け、
  config 既定(sol/max)が Luna セッションへ漏れる事故を防ぐ。
- ピン: Sol = `codex_session_id.txt` / Luna = `codex_session_id_luna.txt`(役割別・混線防止)。
  全ターン出力は `ops/codex_activity.log` へ。ゾンビガード: codex.exe が居ても活動ログ 45 分無音なら kill して続行。
- **ES7 との相違(重要)**: `--last` フォールバックは**廃止**。この計算機は複数工房で Codex を使うため、
  ピン ID が無ければ起床を拒否する(誤って他工房のセッションを resume しない)。
  同じ理由で、**この計算機で素の `codex exec`(launch_new 以外)を手で実行しない**こと。
- 資源配分(Sol=数学のみ・Luna=計算と実装・スクリプト=定型)は `docs/体制と道具.md` の資源配分表が正本。

## 既知の混線リスク(要対処・バックログ)

- `~/.codex/config.toml` にグローバル登録の **es7ops MCP**(ES7 の CI dispatch・**ES7 側受信箱への note**)が
  影工房のセッションにも露出している。キックオフで言及しない限り使われない想定だが、
  Sol が「done 通知」に `ops_note_to_commander` を呼ぶと **ES7 の inbox_claude に落ちる**。
  当面: 便の終了時に ES7 側 inbox も点検する。恒久対処(影工房用 MCP の分離 or スコープ)は Luna 発足時に。

## 郵便箱(ES7 と同じ規約)

- `inbox_claude/` — Codex → 司令塔(依頼・チェックポイント)。`YYYYMMDD-HHMMSS_題名.md` 1 件 1 ファイル。
- `inbox_codex/` — 司令塔 → Codex(裁定速報・GO 等)。配達後に wake で起こす。
- 処理済みは `archive/` へ。数学の成果物の正本は従来どおり `sol/`(キックオフ・reply)であり、inbox は運用連絡のみ。

## 契約(キックオフに毎回明記)

- Sol の返信は指定された `sol/sol_reply_*.md` に書く。他ファイル変更禁止(実行後に `git status` で監査)。
