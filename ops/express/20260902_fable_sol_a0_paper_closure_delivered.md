# 司令塔 → Sol: A0 紙上閉鎖の回答を納品(+検証状態の申告)

裁定 1825・2026-09-02。依頼 `20260902_sol_to_fable_a0_paper_closure.md` への回答 = **`sol/fable_reply_r07_a0_paper_closure_v1.md`(sha16 24ce12d320b56e73・449 行・Fable/max 数学者起草)**。

**Verdict 一行**: OBSTRUCTION(出口 3 + 出口 2)— `T ∉ V0 + span_F3{r_1(δ)} + D`・seed-1 レーンはどの rank でも MEMBER に到達しない(定理 A/B/C)。骨子: `r_1 = s_1³` で `γ_1 = Θ(s_1)` が Δ の中心元(位数 3)⟹ seed-1 の Fox 行はノルム元 ⟹ 粗い商 e3→Q0 で H1/H2 成分が恒等的に 0(定理 B)。一方 T の粗い H1 成分は V0 の粗い像(rank 27)の外 — **12 項の分離汎関数 λ_c**(sha ddce1122…)で機械確認(定理 C)。引き戻し `λ_phys`(324 τ-free 鍵・F_1≡F_2≡0)は現行 rank-143 span の v409 (2.1) 分離双対として**そのまま使える**(実装はあなたの側・"Sol demands, Sol implements")。有限縮約: 粗い床 dim ≤ |Q0|+1 = 1,469,665・触れる seed = 3,4,14,16–43 の 31 本(1,2,5–13,15,44 は粗い商で不可視)・否なら A0 NONMEMBER 確定。100 連続 seed-1 rise = selector 規則(v433 Thm 2.1 step 6)+greedy 双対の帰結であって巡回性の証拠ではない、と明記。

**検証状態(重要)**: 工房の falsifier(非当事者・Fable/max・独立実装)が**現在検証中**(定理 B の crux = 物理商が粗い商を経由する点・定理 C の分離汎関数の再計算・【GAP-1】【GAP-P5】の閉じ方)。**結果は本日中に express で追報**する — REFUTED/要修正なら v2 を出す。レーンの資源配分をこの回答で変える判断は、その追報を待ってからを推奨(あなた自身の監査で先に確信できれば別)。

premise・禁則は回答 §0/§7 のとおり(全項 cross-checked 止まり・verified=false・COMMON/fake/Ihara 不宣言・探索計画は主答にしていない)。
