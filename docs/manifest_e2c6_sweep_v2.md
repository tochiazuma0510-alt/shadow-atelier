# 事前登録 manifest — E2 class-6 二方向掃引 v2(2026-07-26・裁定 20 批准反映)

v1 は保存(宇宙・汚染申告は v1 を継承 — 変更なし: A_j⁽⁶⁾・**j = 2 ゲート**・m ∈ {0..63}・期待値 UNKNOWN・実現ギャップ維持)。

## 判定(批准済み・裁定 20)

- 線型段: (1+θ̄)f̄ = 0 ∧ 𝒩̄f̄ = −Ē_m の 2 ブロック(30×15)over Ā_j(v1 の曖昧さを確定 — implementer の読みを追認)。
- 可解なら **ob = [q_θ] ∈ 𝒪 = C^θ/(1+θ)ker𝒩**。**j = 2: ob_a = q_θ の u₄ 係数・ob_b = q_θ の u₂ 係数**。平均化射影禁止。q_θ/q_N の定義は確定表+κ cocycle 項込み(委嘱 16・便 22 の式を正とする)。
- 証明書: {m, linear_solvable, witness/unsolvability_certificate, ob_a, ob_b, **ob_mode: "quotient-ratified-v2"**}。モード錠: 批准文字列なしの ob 値は検算器が REJECT。

## fixture(発射前必須・全 PASS)

(F1) **偽陽性検出**: q_θ = t₅+t₆・q_N = 0 の合成系 → 可解・ob = (0,0) を返すこと(旧式なら (1,1) — 旧式検出器)。
(F2) **真陽性**: u₂ 係数・u₄ 係数が非零の合成 q_θ → ob ≠ 0 が発火すること。
(F3) class-5 統制(実装済み PASS — 再走)。
(F4) **M 系 mass check**(委嘱 16 §5 M1–M8 と便 22 の基準を統合・とくに (1−σ)q_N = 0・(1−θ)q_θ = 0・(1+θ)K = ⟨t₅+t₆, u₁+u₃⟩ ⊕ 2Ru₂ の再計算)。

## 発射条件

① fixture F1–F4 全 PASS ② falsifier 再監査 PASS ③ **発射錠**: search/FIRE_e2c6.auth(中身 = 本 manifest v2 の SHA-256・司令塔のみ発行)。64 系本走査はそれまで物理的に不可。
