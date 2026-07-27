# 裁定 62 — 便 51 F6 全束クローズ・F8.3 再実行・便 52 発送(2026-07-28)

## 検収(全 PASS)
- BFC v2.9: I1 バグ修理(b_op,sq = b_op,ns = (t̄_M ε)⁻¹・証明 (a-1)(a-2)(a-3) 分割・t̄_M の両翼非依存を §2 引用)。著者は反例 t₂₀=3 を独立再現し、fixture を全文に当てる走査器で自己検査(違反 0)。proof 側 b_op 同期(scope 射程の明示列挙・565 行 t̄_M 型・付録 B 2 行)。診断先・状態札統一。
- 条文案 v6: 手順 v6 表記・exact_recovery_path ∈ {R-a/current-bfc-proof, R-b/tb4e-alternate}。
- TB4 v2.4: status 同期(「未監査」解消・37/37・path 修正)+checker 自主強化(K³/K⁵ 核の units 完全一致 — 文書だけが主張し検査されていなかった {1,11} を閉鎖)。
- CLAIMS W3-17: 冒頭前件に (Z_{2M}-link) 追加・版参照を v2.9/v2.4/37/37 へ同期(行内 antecedent 一致)。

## 司令塔修正権の行使(開示)
BFC 703 行(F7 型列挙表・B-9′ 行)の「合成 tε も枠組みレベル」を「t_{2M}(ゆえ t̄_M)も…合成 t̄_M ε も枠組みレベル ⇒ b_op,sq = b_op,ns 不変」へ型付け — 確定済み規約(便 51 F2.1 正形)の機械的転記であり数学的判断を含まない。著者・Sol の検分対象として便 52 に明記。

## F8.3 再実行
本文クローズ → digest 凍結(BFC = 9cd1e01c…・条文案 v6 = 3b8d7695…・TB4 v2.4 = 6e6656f9…)→ GAP 再束縛 25/25(input = 9cd1e01c… 一致)→ CLAIMS 同期済 → **lint v2 CLEAN(open 0 / triaged 24 — search/preflight-triage.json に line-hash 束縛の disposition 全記入・reviewer 明記)**。
