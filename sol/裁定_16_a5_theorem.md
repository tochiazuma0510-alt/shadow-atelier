# 裁定 16 — 定理 A₅(A₅ 窓の算術飽和)の確定(2026-07-26・司令塔)

## 裁定

**定理 A₅ を `paper-proof / two-mathematician audit PASS` として確定する。**

> **定理 A₅.** (I1) N_A は isolated(⇒ N̄_A は G_ℚ-安定)、(I2) Φ: GT(N_A) → Aut(A₅) = S₅ は単射で |GT(N_A)| = 20・像は N_{S₅}(⟨X⟩) = F₂₀、のもとで
> **Ih_{N_A}: G_ℚ ↠ GT(N_A) ≅ F₂₀ は全射**。ker(Φ∘Ih_{N_A}) の固定体は **L = ℚ(ζ₅, ⁵√2)**(Gal(L/ℚ) ≅ F₂₀)。ゆえに **GT(N_A) の 20 元すべてが arithmetical、したがって genuine**。
> 旧 (I3) 系の規約仮定は**消滅**: 補題 C(絶対較正・標準実経路の Galois path cocycle ∈ [F̂₂,F̂₂]^top.cl.)+補題 D(F̂₂′-正規化持ち上げの一意性)+補題 I3‡(outer class 一致は 2405 p.4 の splitting 文から従う source-closed fact)により α^Ih = α^norm = α^std は**証明**された。

**意義**: 2405.11725 Conj 5.1 の風景で証明済みは dihedral 2 冪族のみだった。本定理は**非可解・非 dihedral・単純群窓での算術飽和の初例**であり、切り出す体まで明示。(I1)(I2) はともに二系統確定済み(A1.v2.2・W3-3b)。

## 正本と固定ハッシュ

- 主文書: `docs/week4-A5算術飽和_v4.md`(663 行)SHA-256 `7017DF1911F7CEE92C16C1D250CE3A2A43AD4FD35463F10D1CCA3144F509CF20`
- 監査: `sol/sol_reply_17_a5_audit.md`(対象 v2 `9AD44906…733A0` を条件付き PASS)・`sol/sol_reply_18_lemmaCD.md`(対象 v3 `6462BEA3…95DC8` を条件付き PASS)SHA-256 `DBC87E7C3BA078BD8729B5DBF99F8DFAC15F15625C26DC822C0B755119C5FF3E`。v4 は便 18 の条件 2 件(F5 本文化・F10 清掃 6 箇所)を反映済み(検算 37/37 PASS)。

## 確定までの鎖(要約)

委嘱 12(定理 R・u 四経路抽出)→ 便 16(Sol 独立 u 抽出)→ **収束 6 号: u ≡ [2]⁴ mod (ℚ^×)⁵ で両者一致**(u_Sol/(−1/2) = (−9/16)⁵)→ P1/P1′(reader ページ画像照合: 式・向き・共変性一致+f̂ ∈ [F̂₂,F̂₂]^top.cl. は ĜT_gen 定義の明示要求)→ 便 17 条件付き PASS(**Sol がスケール自由度の循環を検出** — 系 B′ 反転危険)→ v3 = 路線 (iii)(補題 C・D・系 E)→ **meta-procyclic 地雷**(scout 発見 → Opus 裁定+D0 自前証明/Sol F5 独立閉鎖 = **収束 7 号: 同じ穴を独立に発見し別経路で閉鎖**)→ 便 18 条件付き PASS → v4 清掃 → 確定。

## 付随する閉鎖・残存

- **【GAP-C4】閉鎖**(本日): dessin 数値の GAP 二系統化 `certificates/a5/gap_dessin_crosscheck.json`((a) 10 項目+(c′) 4 項目全 PASS)。**これは組合せ入力((5,5,5) 一意性・Aut = 1・𝒟(v)↔Λ)の cross-checked 化であって、定理 A₅ の札の昇格ではない**(主鎖は補題 C・D0・D・I3‡・FC-3〜FC-5 の紙上証明)。FC-6 の MAIN/NAIVE 両規約 PASS は**補強であって load-bearing ではない**(便 18 F7: FC-6 は主証明に不要)。
- 【GAP-D0】経路 (B) の引用: R–Z (2000) **Thm 9.1.12** を 2 独立の二次情報(0712.4244 Thm 2.9 逐語引用・1711.01500 p.13)で特定 — **札は「二次情報 2 系統で特定・原本未達」**(閉鎖ではない)。9.1.12 は多部構成の可能性があり**項番号の特定は次版課題**・2010 第 2 版の番号異同未確認。経路 (A) = ZZ Prop 4.7+Lemma 4.2+初等補足(配達済み現物のページ画像照合)で本文は自立。
- 残存: 【GAP-C2】【GAP-C3】【GAP-C6】【**GAP-C7 = dihedral 較正ゲート(v2 §8 P3)— 未実施・推奨後続**】。
- 状態語の規律: 本定理は cross-checked(全体)でも verified(Lean)でもない。Lean 化候補: 補題 D の ψ 計算・命題 M の骨格・(2.5) の付値計算。

## ★ 収束記録の追記

収束 6 号(u の類・二抽出一致)・収束 7 号(中心化群の地雷・二重独立閉鎖)を登録。ブラインド収束は通算 7 件。
