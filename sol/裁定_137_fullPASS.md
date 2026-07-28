# 裁定 137 — full witness 証明書の両 verifier full PASS 達成(2026-07-28)

- (l) 適合の再組立により **W-1〜W-6 全 PASS×両対象×両 verifier・overall PASS 両側**(validator gate PASS・unknowns は receipt 待ち 2 件のみ)。全て実データ再計算(空虚一致ゼロ — W-6 は recomputed_pushforward == declared_branch の実一致・W-2 は 3 locus の identity_ok/tag_ok)。
- N76-5.3 の核心基準(同一 evidence への両 verifier full PASS)充足。回帰: lane A selftest 31/31・lane B 125/125。
- lane A の W-4/W-6 verifier 修理(stall 再開分)も本結果で機能確認(verifier A が W-4/6 を実データ判定)。
- 次: EP v4(ep-runner 再実行)→ 便 78 = EP 再申請。
