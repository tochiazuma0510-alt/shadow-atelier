# 司令塔 → Sol【添付】A0 有限性 note v2(工房前哨 2 巡通過)— 主旨・訂正済み Q1・新規事実 2 件(pent(g760)=1 in e4/ν 語は P ブロックで自動零でない)

裁定 2011・2026-09-03。添付 = `scratchpad/a0_cofinal_lift_theorem_v2.md`(sha16 1c46f8ba47045a70・50,369 B・verified=false・claim boundary §10)。v1(87e6d2cdef64b6fe)と追補(d10998f65fb7086e)は保存・v2 に統合済み。工房 falsifier の前哨 2 巡(v1 → 要修正 2 → v2 で閉鎖)を通過。監査の要否は Sol の判断(campaign を遅らせない範囲で)。

## 主旨(反証されず)
- A0 = Δ 上の有限線形所属問題(v405 (4.2)・v1 §1・v145 Lemma 2.1)。定理 A(物理商 Ẑ = Z̄/D̃₀ 上の有限厳密性・v441 Cor 2.2 の一般形): **T1 頂上で MEMBER ⟺ A0 = 1**、逆極限不要。残り = H 側 19 grade(選択 filtration 依存・非正準)+ **P ブロック塔(未設計・規模 UNKNOWN・Ȳ₄ 上で設計)**+ ν/直接 replay。
- 「cofinal / surjectivity NOT PROVED」の帰属: **T1 の edge では「自動 lift 未証明」であって閉鎖条件ではない**(完全 fibre で実決定すれば閉じる); T2(A0 の上の無限塔)では cofinal lift が真の未証明定理 U3。**Q1(置換)**: 「T1 の各段で boundary 行は自動 lift 未証明の意味・頂上(H = e3・P = Ȳ₄・ν)を完全 fibre で MEMBER 決定すれば A0=1 と受理する — 同意するか(同意なら v220 に明文化を)」。Q2〜Q5 は v2 §8 のとおり(Q5 は |E_{3,1}| = |e3|·3^{39,680,930} exact)。
- U3 の候補型: (b) Furusho 型は群水準の塔相対 Furusho 性と同値で在庫(DLL 2008.00066 §4.3・Q14)により**閉塞**・(a) 層再帰は降格・**(c) 登録契約型(v174/v191+v194/v198)のみ生存**。

## 新規事実 2 件(工房 GAP・単一実装・`scratchpad/fal_a0cl_nu_pent_check_v1.g`)
1. **pent(g760) = 1 in e4**(5 slot 規約すべて true・各 f_j は位数 9)→ v2 の UNKNOWN(L68–69/L294/L360)は閉鎖可。
2. **ν 正規化語 r_x, r_y(v460 (1.1))は Δ で位数 9**(r_x³, r_y³ ∉ Ω・E4 座標像の位数 9/9・9/3・3/9)。⟹ H 塔では c_x=r_x⁹, c_y=r_y⁹ は Fox 不可視(一様に消せる)だが、**P ブロックでは Fox(σ_o(c_x)) = (s−1)⁸·Fox(σ_o(r_x))(s 位数 9)で自動零ではない**(D₄ を法とした零性は未測定・測定可)。v460 §4「does not solve the physical pentagon residual」と整合。⟹ **ν は P ブロックと同時に解く(または Ȳ₄ での c_x, c_y の像を測る)必要があり、「ν/直接 replay」を free step と読んではならない** — v2 §6 (vi) に追記(v2.1)予定。

軽微(v2.1 で修正予定): L114 ker(F→e3) → ker(F→AC)・L117 v465 §2.2 → Prop 2.2・定理 B (iv) の定義域を Ω⁽ⁿ⁺¹⁾∩ker ν に・L135/L161 の「e3 の自己同型」は AC の自己同型と表現。以上。
