# 読解ノート: 2401.06870 の Prop 3.14/3.15/Cor 5.4(ML-ODD 依存条文の逐語 pin・reader 2026-08-01)

状態: candidate(抽出のみ)。発注 = 裁定 374 ②(ihnec_v1.md 定理 ML-ODD の依存条文照合)。ページ画像照合済(150dpi)。

## Prop 3.14(§3.2 p.21)— N^⋄ 構成と isolated 性
- 逐語: "For every N ∈ NFI_{PB₃}(B₃), the subgroup N^⋄ := ⋂_{K ∈ Ob(GTSh_conn(N))} K (3.61) is an isolated object of the groupoid GTSh."
- 証明使用補題: Prop 3.12(target 移送)・Prop 3.8(指数一致)。
- **共終性は Prop 3.14 の系として本文注記**(p.21 逐語): "Proposition 3.14 implies that the subposet NFI^{isolated}_{PB₃}(B₃) … is cofinal, i.e. for every N ∈ NFI_{PB₃}(B₃), there exists Ñ ∈ NFI^{isolated} such that Ñ ≤ N."

## Def 3.13(p.20)— settled/isolated の定義正本
- 逐語: "[m,f] ∈ GT(N) is called settled if ker(T_{m,f}) = N … N is called isolated if every GT-shadow in GT(N) is settled." 直後: isolated ⟺ 連結成分の対象が 1 つ・このとき GT(N)=GTSh(N,N) は群。

## Prop 3.15(p.21)— 交叉閉性
- 逐語: "For all N, K ∈ NFI^{isolated}_{PB₃}(B₃), N ∩ K ∈ NFI^{isolated}_{PB₃}(B₃)."
- **証明は本文に無し**(逐語: "The proof of the following proposition is straightforward and we leave it to the reader")— ML-ODD が使う場合は 2 行証明の自前補完を推奨。
- 分業: 共終性 = 3.14 の系/有向性の実体(交叉閉)= 3.15。"directed" の語は Appendix の一般論のみ。

## Remark 3.16(p.21)— reduction homomorphism
- N ≤ H(共に isolated)で R_{N,H}: GT(N)→GT(H) は群準同型(代表元 (m,f) 共通+(3.53) 合成)。式 (3.60): R([m,f]) := (m+H_ord ℤ, f H_{F₂})。

## Cor 5.4(§5 p.28)— genuine ⟺ 全制限像
- 逐語: "Let N ∈ NFI_{PB₃}(B₃). A GT-shadow [m,f] ∈ GT(N) is genuine if and only if [m,f] belongs to the image of the map R_{K,N}: GT(K) → GT(N) for every K ∈ NFI_N(B₃)."
- **奇数条件なし・isolated 制限なし**(N 任意)。依存: Thm 5.2(Ψ: ĜT_gen ≅ lim(ML)・同相)+Prop 5.1+3.14/3.15+有限非空逆極限の非空性([27] Prop 1.1.4)。証明は F(K):=R⁻¹([m,f]) の関手化 → lim 非空 → isolated 元での評価。

## Prop 5.1(p.25)— K|N_ord 型共終性
- 逐語(第 3 文): "for every pair (K,H) ∈ ℤ_{≥1} × NFI(F₂), there exists N ∈ NFI^{isolated} such that K|N_ord and N_{F₂} ≤ H."(証明中で N⁽¹⁾∩N⁽²⁾ に Prop 3.15 適用・normal core 交叉に 3.14 適用)

## 気づき(reader)
- 「K^(a)∩K^(b)」記法は本論文に無い(2405 側の記法)— 本論文の対応物は 3.15 の N∩K と 5.1 の N⁽¹⁾∩N⁽²⁾。

収載元 = 2026-08-01 reader 報告。ihnec_v1.md との対応づけは数学者の pin 差替作業(裁定 376)。
