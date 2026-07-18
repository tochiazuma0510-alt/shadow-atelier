# ops — 司令塔(Claude)⇔ Sol(Codex CLI)の連絡と自動起動

ES7 の郵便箱一式(`atelier_lean/ES7/ops/`・実証済み)の影工房移植版。2026-07-18 開設。

## 自動起動の仕組み

- **初回**: `powershell -File ops\bin\launch_wake.ps1 new "<一行指示>"` — 新規 Codex セッションを起動し、
  セッション ID を `ops/bin/codex_session_id.txt` に**ピン留め**。全ターン出力は `ops/codex_activity.log` へ。
- **以後の起床**: `powershell -File ops\bin\launch_wake.ps1 wake "<理由>"` — ピン ID に `codex exec resume`。
  文脈は保持される。ゾンビガード: codex.exe が居ても活動ログ 45 分無音なら kill して続行。
- **ES7 との相違(重要)**: `--last` フォールバックは**廃止**。この計算機は複数工房で Codex を使うため、
  ピン ID が無ければ起床を拒否する(誤って他工房のセッションを resume しない)。
  同じ理由で、**この計算機で素の `codex exec`(launch_new 以外)を手で実行しない**こと。
- モデル・エフォートは `~/.codex/config.toml` の既定(gpt-5.6-sol・max)を使う。

## 郵便箱(ES7 と同じ規約)

- `inbox_claude/` — Sol → 司令塔(依頼・チェックポイント・done 通知)。`YYYYMMDD-HHMMSS_題名.md` 1 件 1 ファイル。
- `inbox_codex/` — 司令塔 → Sol(裁定速報・GO 等)。配達後に wake で起こす。
- 処理済みは `archive/` へ。数学の成果物の正本は従来どおり `sol/`(キックオフ・reply)であり、inbox は運用連絡のみ。

## 契約(キックオフに毎回明記)

- Sol の返信は指定された `sol/sol_reply_*.md` に書く。他ファイル変更禁止(実行後に `git status` で監査)。
