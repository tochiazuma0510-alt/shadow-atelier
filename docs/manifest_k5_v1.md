# 事前登録 manifest — K⁽⁵⁾ 算術飽和キャンペーン v1(2026-07-27・司令塔)

前提: 裁定 25(D1 検収・封印突合全一致)・裁定 26(便 30 検収・仕様確定)・裁定 27(K5e 負較正)・D1 v1.1(補題 K5-a・a = 1 封印・node 87/87 × GAP 52/52)。定理 R^cyc_formal(W3-13)の前件 (0)(1)(2)(3)(6′) は K⁽⁵⁾ で PASS 済(W3-15)。**本 manifest が統治するのは残る (4d)(5′) — 比較橋 B_FC の K⁽⁵⁾ 実行**。

## 宇宙(事前登録・変更禁止)

- 窓: K⁽⁵⁾ = ker ψ₅(= K⁽¹⁰⁾・Prop 3.4 — 独立二例として二重計上禁止)。P = G₅(位数 500)・M = 10・e = 5・𝔉₀ = C₅・K = ℚ(ζ₂₀)。
- 標的: **target_policy = all_two_classes**。Λ_sq(α ∈ {1,4})と Λ_ns(α ∈ {2,3})の二 fixture(ID: `K5-sq` / `K5-ns`・D1 marking 相対ラベル・canonical H 生成元と正規化置換三つ組の hash は D1 v1.1 §1.3)。標的 dessin: 次数 10・種数 2・ordered (10,2⁴1²,10)・Aut = 1(**固定 U 上の ordered dessin の圏**での主張)。**結果を見て一方を捨てる = NO-GO**。
- 検出器: degree M = 10(μ₁₀-torsor)。degree 5 detector は SCHEMA-OUT(便 29 W3)。

## 五札封印表

| 札 | 内容 |
|---|---|
| **FORMAL-IN** | (0)(1)(2)(3a–d)(6′-i)(6′-ii) の証拠 ID(D1 v1.1・dessin 別行)・命題 K5-1・j_i の定義・**封印値 a = j_ns⁻¹j_sq = 1**(補題 K5-a・二系統確認済)。(5′) は `PENDING`。**結論との不一致 = proof/record consistency failure**(橋の反証ではない — 便 29 ★教材 3) |
| **BRIDGE-IN**(u 開示前に凍結・dessin ごと) | 明示 ℚ-モデル式+hash・branch map(0,1,∞ ↦ X,Y,Z の actual conjugator)・全分岐 cusp・ℚ-有理 uniformizer・FC 比較規約の版・**τ 由来一式**: ①原始根 ζ₁₀ := ζ₂₀² の指定 ②向き τ(ζ₁₀)(H′) = XH′X⁻¹ ③Kummer cocycle を γ(s^{1/10})/s^{1/10} と読む規約 ④ρ₀ 側 𝔉₀ generator と j: μ₁₀[5] ≅ 𝔉₀ の対応。規約捻れ τ ↦ τ∘[b] が必要になった場合は a ↦ ab⁻¹ を**同時**更新(後出しの b 選択は禁止・D1 v1.1 §6.3) |
| **BRIDGE-FAIL**(= B_FC の真の falsifier) | BRIDGE-IN が独立に成立しているのに ①actual G_K-置換と τκ が不一致 ②封印予測 (P2) の破れ |
| **BRIDGE-UNKNOWN** | 明示モデル・actual marking・局所比較のいずれかを閉じられない — 値を推測せず UNKNOWN(scope-out と混同しない) |
| **SCHEMA-OUT** | bad H(degree 5 detector)・非 regular・Λ 不安定・ρ₀ 非忠実。**将来欄: 8\|n の K⁽ⁿ⁾ 一律**(命題 K5-2b・**K5e 負較正で機械裏取り済** 13/13+18/18・K⁽⁸⁾ = 負較正例・裁定 27) |

- B5 の札は二段を維持: 形式 FAIL(M = 10 合成数)+ primary 分離(𝔉₀ = C₅ / 円分商 2-part)で無害化 — **PASS に塗り替えない**(便 30 F6.2)。

## 封印予測(u 開示前・破れうる形で登録)

- **(P1)** ord([u_i⁻¹]₁₀) ∈ {1, 5}(i = sq, ns)。2 や 10 が出たら発見ではなく**警報**(前件札か記録の破れ・便 29 F7.3)。
- **(P2・主整合ゲート)** [u_ns⁻¹]₁₀ = [u_sq⁻¹]₁₀ in K^×/K^{×10}(a = 1・両 dessin 同一 τ 規約の前提)。**生の u_sq = u_ns は要求しない**(便 30 W3)。
- 観測列プロトコル(K3 v2 §6 継承): q_*[u] ∈ ⟨[2]⟩ かの盲検記録(予測登録ではない・2 以外の素点で valuation が 10 の倍数でない例が出たら「根基 2」候補は即棄却)。

## 較正三層(発射前必須)

1. **K5 finite fixture**: 二類・passport・normalizer・regularity・K5-1・ρ₀(𝔉₀) = τ(μ₁₀[5])(D1 v1.1 で済 — 証拠 ID を封印表に転記)。
2. **K3 regression fixture**: K³ の既知データ一体(平面モデル・branch 割当・exact conjugator・cusp と uniformizer・その正規化での u = −4・ord([u⁻¹]₆) = 3・τ/ρ₀/j の向き)で bridge pipeline が既知 class を再現すること。**規約・実装回帰の検査であり、K⁽⁵⁾ の証拠・期待値に数えない**(便 30 P9・W5: 数だけを checker に持ち込まない)。u′ = −256/729 は同一 class の covariance control。
3. **covariance controls**: ①X ↦ X⁻¹ で class が反転し位数と体が不変 ②s ↦ cs で u ↦ u·c⁻¹⁰・class 不変 ③τ ↦ τ∘[a] と Kummer character の逆 power の同時変換で (5′) 不変。

## 工程と発射条件

- **S5(明示 ℚ-モデル探索)= GO**(便 30 F6.5)。二 dessin **同時**に対象。数学者設計 → implementer 実装。機械走行は 1 ジョブ 600 秒 cap。
- **u 抽出 = BRIDGE-IN 凍結後のみ**: 凍結 = 本 manifest と BRIDGE-IN 記録の SHA-256 固定 + FIRE_k5bridge.auth(司令塔のみ発行)。凍結前の抽出 = NO-GO。
- 発射条件: ①較正三層 PASS ②falsifier 計画監査 ③便 31(Sol manifest ゲート — スキップ不可)④発射錠。
- **算術全射性の宣言は (4d)(5′) と Kummer class の閉鎖まで禁止**(便 30 F6.5)。

## 撤退条件(先に書く)

明示 genus-2 モデル(二 dessin とも)が 2 週間相当の予算で得られない場合、BRIDGE-UNKNOWN のまま**保留**し、資源を奇数族の別窓(n = 7 等の D1 横展開)・Lean・論文線へ移す。奇数族横展開の価値(前件チェックの族的成立)はモデル探索の成否と独立に残る。
