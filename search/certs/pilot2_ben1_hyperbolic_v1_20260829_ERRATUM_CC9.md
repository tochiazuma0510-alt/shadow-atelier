# ERRATUM CC-9(裁定 1813・2026-08-30)— pilot2_ben1_hyperbolic_v1_20260829.json の 2 欄を supersede

**対象 cert**: `pilot2_ben1_hyperbolic_v1_20260829.json`(sha16 0d6d590d5dda602f・cert 本体は凍結のまま変更しない)

**supersede される欄**(2 つ・ラベル割当の宣言のみ):
- `conventions.reading_used`
- `target.workshop_xyz` — 旧宣言 **(x,y,z) := (λ₃,λ₂,λ₁) すなわち X̄ ↔ σ_∞**

**正**(connect_spec_v1.md v1.2 §3.8.2 T-2・sha16 78da8fa13469955d):
**X̄ = m(γ₀) ↔ σ₀ = λ₁・Ȳ = m(γ₁) ↔ σ₁ = λ₂・z_census = (ȲX̄)⁻¹ = m(γ_∞) ↔ σ_∞ = λ₃**

**根拠**(第 2 前哨 M8・fal_c2_arch.py d929447be8f4940e): 旧割当では鏡映二重 pin の解が 0 個(新割当は一意)。旧 cert の**群論的内容(行列・coset・FD・ρ・全ゲート値)は無傷** — 誤っていたのはラベル割当の宣言 2 欄のみ。

**警告**: CONNECT 便1 以降の全実装は本 erratum 経由で割当を取ること。旧 cert の当該 2 欄を直接読むと **a の符号が静かに反転し SELECT が誤る**(裁定 1812 重大 2)。

関連: CC-8(便1 relator Z̄=(X̄Ȳ)⁻¹ は census z=(ȲX̄)⁻¹ の鏡像 — 別物・両方正しいが混用禁止)。
