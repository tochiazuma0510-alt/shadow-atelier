# 裁定 52 — v2.4+条文案 v2 検収・GAP 再束縛・便 48 発送(2026-07-27)

## v2.4 検収(PASS)
- 司令塔独立検証: code point 走査 CTRL 0 / CR 0(両ファイル)・digest 一致(v2.4 = 52b77ff…・条文案 v2 = a921cb7…)・spot-check(amendment-pending ×5・8.4.0 (F1)–(F4) 二段コミット・★教材 19-21 転記)。
- 根因の更新: 制御文字は裁定 50 の推定(シェル heredoc)ではなく **\v(Python 非 raw)+\b(JSON)のエスケープ解釈**と著者が確定。対策 = \bmod 全廃。裁定 50 の推定を訂正。
- 著者申告の手順逸脱(バイト単位フィルタ・CRLF→LF・U+FF65 統一)は受理 — エスケープを含むペイロードを書かない除去のみで再混入経路なし。

## §15.7 残件クローズ
GAP certificate を v2.4 へ再束縛(束縛パス 2 行のみ変更)・再走 25/25 PASS・input_doc_sha256 一致。B_FC 線の artifact 残件はこれで 0。

## 発送
便 48 = ops/inbox_codex/sol_task_48_tb4_and_v24.txt(二部構成: A = 差分再検収+版上げ許可・B = TB4 定理ゲート+一括承認 4 点)。PASS 後の版上げは v1.4/v1.6 の**単一版イベント**(amendment+Z-norm+§7.4+札更新を一括・裁定 49-3/51 の順序維持)。
