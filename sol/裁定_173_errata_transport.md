# 裁定 173 — equality errata v2・I-24 transport 設計の検収(2026-07-29)

## kerchi_equality_v2 — 受理(10 errata 全採用)
- E1 型ゲート(K⁽ⁿ⁾ は正典 Thm 4.3 で isolated ⟹ **dihedral 主線は無傷**)・E3/E4(素数核は除外先でなく**最安の反例候補**へ反転)・E5(N₃ = 等号成立・M₃ が唯一の UNKNOWN)・E6 Maschke・E8 KERNEL-DL3 正式名・E9 二段 assert・E10 **予想 KE-P**(G_N 可換 ⟹ χ̃ 単射)— どちらに転んでも収穫の win-win 形。
- 追加検分を委嘱: v5 の χ-退化窓(idx126 兄弟・G_N 可換位数 6・χ̃ 像自明)は KE-P の反例か射程外か。あわせて χ-退化窓は「自明型の等号破れ」(L 型 = 全射でも破れ、とは別種)に当たるかの判定。

## i24_transport_design_v1 — 受理(F79-4.1 修理・要求超え)
- **補題 TR/SQ-INV**: 輸送因子 −1 = ζ₄ₙ^{2n} は 2n 乗 ⟹ **[u]_{2n} 水準で消滅** — a_n・ord・P_{n,p}・FULL_p_DEPTH・[u]₂ が全て j 盲目(平方類より強い)。
- **定理 W-REL(族化)**: ν = Ad(Δδ) で ν(H_{3,α,β}) = H_{2,−α,β−1}(全奇数 n・Python 悉皆 PASS・S₆ witness はその一標本)。covariance control (2/3)⁶ の既存公開値が設計の予言どおりであることも確認。
- **C1′ の誠実な残余**: 消えるのは j 曖昧性のみ・[α] 曖昧性(j=2 行の φ(n)/2 類)は残る。**n=3 は C1 完全閉鎖**(φ(3)/2 = 1)・q=7 は 3 類残存。
- capsule schema relabel-transport/v1(RT-1〜8)採用。typed-edge v2 仕様に operation = **relabel** を追加(便 80 の v2 設計に編入)。
- 証明書 erratum(裁定方式・artifact 不変): i24_u3_recheck_20260729.json の u3_reproduction_status は誤読 — 正 = RELABEL_1INF_TRANSPORT_FACTOR_MINUS_ONE(本裁定が正本)。

## 凍結予言 I24-P1(本 commit で凍結)
**λ₃ = t/(t+1)・同一 cusp・同一 uniformizer で u_{H₃} = +4**(−4 でない — 機構は複素共役でなく Möbius (1 ∞))。検定 = week4-u-k3.mjs の λ 一行差し替え・公開値のみ。凍結後ただちに測定を委嘱(prediction-first)。
