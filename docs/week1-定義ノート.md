# Week 1 定義ノート v1 — B₃ gentle 系 GT-shadows(主線)

作成 2026-07-18(司令塔)。出典: arXiv 2401.06870(定義の正本)+ 2405.11725(dihedral poset)。
**検証状態**: 抽出は読解 3 隊(`docs/notes/`)→ 司令塔がページ画像で 4 か所を独立照合(2401 p.10 hexagon (3.3)(3.4) / 2405 p.13 ψₙ (3.1) / p.18 Thm 4.3 / p.23 Conj 5.1)→ 数値主張を GAP で独立検算(`search/week1-kn-spotcheck.g` ALL PASSED)。**Sol 定義ゲート未通過 — ゲート通過までは candidate**。

## 1. 基礎対象(2401 §1.1)

- B₃ = ⟨σ₁, σ₂ | σ₁σ₂σ₁ = σ₂σ₁σ₂⟩、PB₃ = ker(ρ: B₃ → S₃)、ρ(σ₁) = (1,2), ρ(σ₂) = (2,3)。
- x := x₁₂ := σ₁²、y := x₂₃ := σ₂²、Δ := σ₁σ₂σ₁、c := Δ²。z := (xy)⁻¹(xyz = 1)。
- Z(B₃) = Z(PB₃) = ⟨c⟩ ≅ ℤ。**PB₃ ≅ F₂ × ⟨c⟩**、F₂ = ⟨x, y⟩(自由)。
- θ, τ ∈ Aut(F₂): θ = (x↔y)、τ: x↦y↦z↦x(位数 3)。
- 共役公式 (1.10)–(1.13)(実装で必須; 2401 p.4–5)。

## 2. groupoid GTSh(2401 §3)

**対象**: NFI_PB₃(B₃) = {N ⊴ B₃ | 指数有限, N ≤ PB₃}。各 N に:
- N_ord := lcm(ord(xN), ord(yN), ord(cN))(PB₃/N 内)(3.1)
- N_F₂ := N ∩ F₂ (3.2)

**hexagon 関係式 mod N**((m,f) ∈ ℤ×F₂; B₃/N 内)【画像照合済】:
- (3.3) σ₁^{2m+1} f⁻¹ σ₂^{2m+1} f N = f⁻¹ σ₁σ₂ x^{−m} c^m N
- (3.4) f⁻¹ σ₂^{2m+1} f σ₁^{2m+1} N = σ₂σ₁ y^{−m} c^m f N

**GT-pair**(Def 3.1): (3.3)(3.4) を満たす [m,f] = (m+N_ord ℤ, fN_F₂) ∈ ℤ/N_ord × F₂/N_F₂。
**charming**: 2m+1 が (ℤ/N_ord)^× の元を代表 かつ fN_F₂ ∈ [F₂/N_F₂, F₂/N_F₂]。
**GT-shadow**(Def 3.7): charming GT-pair + 全射性。全射性は **T^{F₂}: F₂ → F₂/N_F₂ の全射性で十分**(Prop 3.6): ⟨x̄^{2m+1}, f̄⁻¹ȳ^{2m+1}f̄⟩ = F₂/N_F₂。
- T_{m,f}: σ₁ ↦ σ₁^{2m+1}N, σ₂ ↦ f⁻¹σ₂^{2m+1}fN(Prop 3.2)。c ↦ c^{2m+1}N。
- **簡約 hexagon**(Prop 3.4; **f ∈ [F₂,F₂] 前提**、F₂/N_F₂ 内で閉じる): (3.10) fθ(f) ∈ N_F₂、(3.11) τ²(y^m f)τ(y^m f)y^m f ∈ N_F₂。⇒ 探索器は (3.10)(3.11)、検証器は (3.3)(3.4) と役割分担できる(同値の前提条件に注意)。

**射と groupoid 構造**(Thm 3.10)【逆射の式は 2405 p.13 画像でも照合済】:
- GTSh(K,N) := {[m,f] ∈ GT(N) | ker(T_{m,f}) = K}(K = source)。GTSh(K,N) ≠ ∅ ⇒ K_ord = N_ord、各商が同型(Prop 3.8)。
- 合成 (3.53): [m₁,f₁]∘[m₂,f₂] = [2m₁m₂+m₁+m₂, f₁E_{m₁,f₁}(f₂)]、E_{m,f}(x) = x^{2m+1}, E_{m,f}(y) = f⁻¹y^{2m+1}f。2m+1 は乗法的 (3.49)。単位 (0,1)。
- 逆射 (3.54): m̃ = −(2m̄+1)⁻¹m̄(ℤ/N_ord 内)、f̃K_F₂ = (T^{F₂,isom}_{m,f})⁻¹(f⁻¹N_F₂)(**source 側の商の元**)。
- **settled**: ker(T_{m,f}) = N。**isolated**: 全 shadow が settled ⇒ GT(N) = GTSh(N,N) は**有限群**。N^⋄ := 成分の全対象の交わりは isolated(Prop 3.14)、isolated poset は cofinal。

**reduction / survive / genuine**(§3.1, §5)【Cor 5.4 は主線の要】:
- N ≤ H ⇒ R_{N,H}: GT(N) → GT(H)、[m,f] ↦ (m+H_ord ℤ, fH_F₂)(3.60)。isolated 同士なら群準同型。
- [m,f] ∈ GT(H) が **survives into N** ⟺ Im(R_{N,H}) に入る。
- **genuine**(Def 4.2)= ĜT_gen の元の射影。**Cor 5.4: genuine ⟺ 全ての細分 K ≤ N に survive**。⇒ **fake の証明は有限検証 1 個の証明書**で完結、genuine は「深さ d まで survive」までしか言えない(UNKNOWN 一級)。
- Thm 5.2: ĜT_gen ≅ lim(ML)(ML: isolated poset 上の N ↦ GT(N))。
- χ_vir([m,f]) = 2m+1 mod N_ord(virtual cyclotomic character の有限版)。

**gentle の意味**: 本来の ĜT は hexagon×2 + **pentagon(B̂₄ 内)**。gentle 版 ĜT_gen は pentagon をその帰結 f̂ ∈ [F̂₂,F̂₂]^cl に置換(= 有限側では charming 条件)。ĜT ⊆ ĜT_gen、ĜT_gen = Harbater–Schneps の ĜT₀。**ĜT = ĜT_gen かは未解決**。

## 3. dihedral poset(2405 §3–4)

- Dₙ = ⟨r,s | rⁿ, s², srs⁻¹r⟩(位数 2n)。**ψₙ: PB₃ → Dₙ³**: x ↦ (r,s,s), y ↦ (rs,r,rs), c ↦ (1,1,1) (3.1)【画像照合済】。**K⁽ⁿ⁾ := ker(ψₙ)** ∈ NFI_PB₃(B₃)(Prop 3.1; Core_B₃ 構成)。Dih := {K⁽ⁿ⁾ | n ≥ 3}。
- Gₙ := Im(ψₙ) = ⟨(r,s,s),(rs,r,rs)⟩ ≅ PB₃/K⁽ⁿ⁾ ≅ F₂/K⁽ⁿ⁾_F₂。
- **数値事実(GAP 検算済み・n = 3..12)**: |Gₙ| = 4n³(n 奇)/ 4(n/2)³(n 偶)。K_ord = lcm(n,2)。K⁽ⁿ⁾ = K⁽²ⁿ⁾(n 奇)。K⁽q⁾ ⊂ K⁽ⁿ⁾ ⟺ n | lcm(q,2)(Prop 3.5・未検算)。
- **Thm 4.3(較正ゲートの正解)**【画像照合済】: GT(K⁽ⁿ⁾) = {(m, (r^{2k}, r^{−2k}, r^{ϰ(m)})) | m ∈ 𝒳ₙ, k ∈ ℤ}、4|n のときのみ追加条件 k ≡ ϰ(m)/2 mod 2。𝒳ₙ = {m ∈ {0..K_ord−1} | gcd(2m+1, K_ord) = 1}、ϰ(m) = m+1(m 奇)/−m(m 偶)。**K⁽ⁿ⁾ は isolated**。
- 群構造(Thm 4.6): GT(K⁽ⁿ⁾) ≅ Aff(ℤ/n₀ℤ) × 𝒵₂(α ≤ 1)/ Aff(ℤ/n₀ℤ) × H̃_α(α ≥ 2)、n = 2^α n₀。|GT(K⁽ⁿ⁾)| = 2n₀φ(n₀) / n₀φ(n₀)·2^{2α−2}(エージェント導出値・**要独立検算**)。
- **Conjecture 5.1(dihedral 予想)**【画像照合済・原文】: Dih の全対象 K で全 GT-shadow が **arithmetical**(= Ih_K: G_ℚ → GTSh(K,K) 全射)。証明済み: **n = 2^α(α ≥ 2)のみ**(Thm 5.3; |GT(K^(2^α))| = 2^{2α−2} が下限と一致)。α ≥ 3 で非可換(Cor 5.4₍₂₄₀₅₎)。**最小 open: K⁽³⁾**(|GT| = 12 に対し保証 ≥ 4)。混合位数の最小 open: n = 12。
- arithmetical ⇒ genuine ⇒ charming。fake の例はゼロ(両論文とも明言)。

## 4. Week 1-2 再現ターゲット(較正ゲート)

答えを知っている問題(これが全部通るまで新規対象に撃たない):
1. K⁽ⁿ⁾ 構成と数値事実(n = 3..16)— **済**(n = 3..12、`search/week1-kn-spotcheck.g`)
2. GT(K⁽ⁿ⁾) のブルートフォース列挙 = Thm 4.3 の式 (4.12) と一致(探索器: hexagon+charming+全射 / 検証器: 独立実装で再計算)
3. 合成則の乗積表 ≅ Thm 4.6 の群構造(恒等式 (4.19)(4.20) 含む)
4. n = 4, 8, 16: |GT| = 4, 16, 64、H̃_α 同型、α ≥ 3 非可換
5. reduction 全射性(Thm 4.4)を具体対で
6. LS 条件 witness(Thm 5.2)— 論文が読者に委ねた m ≡ 2, 3 mod 6 を含む

## 5. 読書割当(研究者向け・コーチ枠)

**今週の主読**: 2405.11725 §1.7(記法, p.9)→ §2(GTSh 復習, pp.11–13)→ §3(dihedral poset, pp.13–16)→ §4(pp.16–23)。Thm 4.3 の証明(Lemma 4.2 の (h₁,h₂,h₃) 構成)が最重要 — 較正ゲートの数学的心臓。
**並読(定義の根)**: 2401.06870 §3(pp.10–21)。hexagon (3.3)(3.4) がなぜ well-defined か(p.10 末尾の 3 行)を自分の手で確認するのが第一歩。
**確認質問**(次セッションで議論したい):
1. (3.3)(3.4) で c^m が右辺に付く理由を、B₃ の中心拡大 1 → ⟨c⟩ → PB₃ → F₂ → 1 の言葉で説明できるか?
2. charming の f ∈ [F₂/N_F₂, F₂/N_F₂] 条件は、profinite 側の何の影か?(答: pentagon の帰結 f̂ ∈ [F̂₂,F̂₂]^cl — なぜ pentagon からこれが出るかは 2401 は引用で済ませている。出典をたどるか?)
3. Thm 4.3 の 4|n の追加条件 k ≡ ϰ(m)/2 mod 2 は、Gₙ のどの構造の反映か?(Prop 4.5 の ν と H̃_α の定義を見よ)
4. 「fake の証明は有限証明書 1 個」— Cor 5.4(2401)のどの向きの含意を使っているか?

## 6. 副線(B₄ 系)の位置づけ

2106.06645(+定義正本 2008.00066・未入手)は**本来の ĜT 用・B₄ ベース・pentagon あり**の別 groupoid。dessins への作用・軌道計算(moduli 体次数の評価 Cor 3.12)はこちらの言葉。Dolgushev の Python パッケージ GT は B₄ 系の実装 — **第三者クロスチェック資源**(較正: N⁽⁵⁾ で GT♥ ≅ D₆ など)。主線の較正が通ってから着手。
