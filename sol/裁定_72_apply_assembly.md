# 裁定 72 — Z-norm apply assembly 完了・snapshot 事故の訂正(2026-07-28)

## snapshot 事故(自認・プロセス修理)
着弾監視がファイル生成の瞬間に発火し、Sol のターン完了前の返信 snapshot を commit していた(便 59/60)。Sol はターン内で推敲を継続する — 最終版には P60-B9(whitelist の基礎体 K 型付け)等が追加されており、B_FC 著者は最終版を読んで spec v3 の B9 対応を済ませていた(裁定 71 の「B1〜B8」記載は snapshot 由来 — 本裁定で B9 込みに訂正)。**記録は Sol 最終版を正とする**。以後の監視は「ファイル存在」でなく**ファイル安定(サイズ・mtime が 60 秒不変)or turn end 確認後**に発火させる。

## apply assembly の状態
- component 1(∀n proof・a8eee738…)/2(K5 migration・ae1e9ef0…)hash 確定 → final seal に記入・ID 群 mint(bar-iota/ext-of-iota-infty/v1 等 4 本)→ final seal 承認候補 hash = 022e6e2e…(status_on_apply 欄は空 — 便 61 PASS 後に記入し operative hash を確定する二段方式)。
- TB4 v2.5(P-1 札更新・P-2 (R1)(R2)(R3))適用済・TB4-A20/数学本文不変。Rule 1 v1.5・manifest v1.7(typed reference のみ・旧版無変更)。BFC v2.12(関所 8 箇所+文献要請 13(ii) 解消)。
- CLAIMS の二区分記帳(採用手続き+相対定理化)は便 61 PASS 後に遅延束縛(★教材 便 57-4)。

## D-2 裁定(spec v3 の司令塔決定事項)
divisor 同値は **(D-2) 第三の equality certificate 案を採用** — (D-1) canonical schema 案は canonicalizer 自体が第三実装となり共通バグ経路を作る(起草者の指摘を採用)。便 61 Part B に明記して Sol の確認を求める。
