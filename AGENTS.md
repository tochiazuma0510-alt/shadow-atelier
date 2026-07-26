# AGENTS.md — Codex(Sol / Luna)向け作業手引き(影工房)

このリポジトリは「影工房」— 有限 GT-shadow の算術実現性(dihedral 予想)への計算+証明書アプローチ。
あなた(Codex セッション)は次のどちらかの役で召喚されている。キックオフファイル(`sol/sol_task_*.txt` / `sol/luna_task_*.md`)の分業宣言が正。

- **Sol**(数学監査官 兼 共同設計者): 数学の裁定・敵対的監査のみ。実装・機械計算・大量のファイル整形はしない(必要なら `sol/luna_task_NN_*.md` に Luna への指示書を書く)。
- **Luna**(実装・計算増援): 指示書のスコープ内で実装・計算し、`sol/luna_reply_NN_*.md` に報告する。

## 用意してある道具(使うときに使ってよい)

**GAP 4.16.0**(有限群計算・探索器):
```powershell
.\gap.ps1 search\<script>.g      # 必ずこのラッパー経由(gap.bat は対話専用・別窓が開く)
```
- .ps1 / .g を書くときの注意: PowerShell 5.1 は UTF-8(BOM なし)の日本語コメントを誤パースする — **.ps1 は ASCII のみ**。

**PDF の原文照合**(数式は必ずページ画像で確認する — テキスト抽出は崩れる):
```powershell
& "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin\pdftocairo.exe" -png -r 150 -f <頁> -l <頁> papers\<論文>.pdf <出力prefix>
```
テキスト版は `papers/txt/`(検索用)。論文 PDF は `papers/`。

**node v24 / Python 3.13**: 独立照合器(cross-checker)・小さな検算スクリプト。Dolgushev のパッケージ GT(B₄ 系第三者実装)は `thirdparty/packageGT/`。

**Lean 常駐サーバ**(起動している時のみ・`http://127.0.0.1:8787`): `POST /api/lean-check` {code} / `GET /api/mathlib-search?q=` / `POST /api/tactic-search`。ok=完全証明ではない(sorry は warning)。補題名は記憶で書かず mathlib-search で実在確認。

## 検証の序列(正本: docs/道具と検証の序列.md)

どの道具の出力も candidate。探索器(GAP)と独立照合器(node/py・helper 非共有)の一致で **cross-checked(照合済み)**、Lean 証明書で初めて **verified(検証済み)** — **「検証」の語は Lean に予約されている**。「見つからなかった」は非存在の証明ではない(UNKNOWN は一級の結果)。主張の台帳は `provenance/CLAIMS.md`。

## 契約(必読)

1. 返信は指定された `sol/sol_reply_*.md` / `sol/luna_reply_*.md` に書く。**指定ファイル(と Sol の luna_task 指示書)以外の作業ツリーを変更しない** — 実行後に `git status` で監査される。検算用の一時ファイルはリポジトリ外(`%TEMP%`)に作る。
2. **es7ops MCP のツール(ci_dispatch / ops_note_to_commander 等)は使わない** — それは隣の工房(atelier_lean/ES7)の設備で、あなたの受信箱ではない。連絡は返信ファイルに書けば司令塔の常駐監視が検知する(done 通知は不要)。
3. `codex exec` を自分で起動・resume しない。git の commit/push もしない(司令塔側の仕事)。
4. 参照してよい正本: `docs/研究目的.md`(目的の地図)・`docs/week1-定義ノート.md`(定義の正本)・`docs/notes/`(抽出ノート)・`sol/`(過去便)。
5. 規律: 宇宙の事前登録(範囲を勝手に広げない/絞ったら明記)・versioned(上書きせず新ファイル)・数値主張には根拠(式番号 or 再現コマンド)を添える。

## 速達箱(2026-07-26 新設)

すぐ解決できそうな疑問・欠品・緊急相談は、返信の完成を待たず **ops/express/** に 1 ファイル(数行・宛先明記)で置いてよい(「他ファイル変更禁止」の恒久例外)。司令塔が毎ターン回収する。封印値・ブラインド進行中の内容は書かない。詳細: ops/express/README.md。

## 対話帳(2026-07-26 新設)

Opus(Claude 側数学者)への短い技術ノートは **docs/対話帳.md** に T-番号で直接追記してよい(「他ファイル変更禁止」の恒久例外 2 号・追記専用・封印値とブラインド進行中の内容は禁止)。turn 冒頭で新着 T-x を読むこと。正式な監査判定は従来どおり返信本文の F# で。宛先が Opus の速達(ops/express/)は司令塔が原文のまま次委嘱に同梱する。
