# Week 1 定義ノート v2 — B₃ gentle 系 GT-shadows(主線)

v1: 2026-07-18(司令塔)。v2: 同日、Sol 定義ゲート(便 01)の指摘を反映。出典: arXiv 2401.06870(定義の正本)+ 2405.11725(dihedral poset)。
**検証状態**: 読解 3 隊の抽出 → 司令塔のページ画像照合 4 か所+GAP 検算(ALL PASSED)→ **Sol 定義ゲート: 条件付き PASS(2026-07-18・`sol/sol_reply_01_definition_gate.md`)**。骨格((3.3)(3.4)・charming・(3.53)(3.54)・K⁽ⁿ⁾・Thm 4.3/4.6・位数公式・rs=s*r 慣習)は原文一致と裁定。**§4 の較正スイート v2 全通過をもって「定義+既知例の再現」達成を宣言する**(それまで宣言しない)。裁定記録: `sol/裁定_01_definition_gate.md`。

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
**GT-shadow**(Def 3.7): charming GT-pair + 全射性。charming GT-pair では **T_{m,f}, T^{PB₃}, T^{F₂} の全射性は同値**(Prop 3.6 — どれで判定してもよい)。有限商では ⟨x̄^{2m+1}, f̄⁻¹ȳ^{2m+1}f̄⟩ = F₂/N_F₂ を用いる。
- T_{m,f}: σ₁ ↦ σ₁^{2m+1}N, σ₂ ↦ f⁻¹σ₂^{2m+1}fN(Prop 3.2)。c ↦ c^{2m+1}N。
- **簡約 hexagon**(Prop 3.4; **f ∈ [F₂,F₂] 前提**、F₂/N_F₂ 内で閉じる): (3.10) fθ(f) ∈ N_F₂、(3.11) τ²(y^m f)τ(y^m f)y^m f ∈ N_F₂。⇒ 探索器は (3.10)(3.11)、照合器は full B₃/N 上の (3.3)(3.4) と役割分担できる(同値の前提条件に注意)。

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
- 群構造(Thm 4.6): GT(K⁽ⁿ⁾) ≅ Aff(ℤ/n₀ℤ) × 𝒵₂(α ≤ 1)/ Aff(ℤ/n₀ℤ) × H̃_α(α ≥ 2)、n = 2^α n₀。|GT(K⁽ⁿ⁾)| = 2n₀φ(n₀) / n₀φ(n₀)·2^{2α−2}(**Sol が独立再導出済み・一致** 2026-07-18)。
- **Conjecture 5.1(dihedral 予想)**【画像照合済・原文】: Dih の全対象 K で全 GT-shadow が **arithmetical**(= Ih_K: G_ℚ → GTSh(K,K) 全射)。※GTSh(K,K) = GT(K) と書けるのは Thm 4.3 が K ∈ Dih の isolated 性を証明しているから — 一般の N に安易に一般化しない(Sol 注記)。証明済み: **n = 2^α(α ≥ 2)のみ**(Thm 5.3; |GT(K^(2^α))| = 2^{2α−2} が下限と一致)。α ≥ 3 で非可換(Cor 5.4₍₂₄₀₅₎)。**最小 open target: K⁽³⁾ = K⁽⁶⁾**(|GT| = 12 に対し保証 ≥ 4; 文字どおりの「混合」最小は n = 6 = 2·3 でこれと同一物)。重複 K⁽ⁿ⁰⁾ = K⁽²ⁿ⁰⁾ を除いた正規化代表のうち **α ≥ 2 かつ n₀ > 1 が同時に現れる最小 open 代表は n = 12**。
- arithmetical ⇒ genuine ⇒ charming。fake の例はゼロ(両論文とも明言)。

## 4. 較正スイート v2(Sol 定義ゲートの条件を反映・2026-07-18)

答えを知っている問題(**全 8 項目が通るまで新規対象に撃たない**。実装規約: Sol 警告 6 件+罠 12 件 = `sol/sol_reply_01_definition_gate.md` §6):
1. K⁽ⁿ⁾ 構成と数値事実 — **部分済**(n = 3..12 spotcheck 済み)。残: **n = 13..16**、奇数 13, 15 の K⁽ⁿ⁾=K⁽²ⁿ⁾、**Prop 3.5 の包含判定を marked factor map で**検査
2. GT(K⁽ⁿ⁾) の完全列挙 = Thm 4.3 (4.12) と一致。**探索(簡約 hexagon・F₂/N_F₂ 内)と検証(full B₃/K⁽ⁿ⁾ 上の (3.3)(3.4))を helper 非共有で分離**。全候補数も記録
3. **source kernel 証明書**: 全 shadow について ker(T_{m,f}) = K⁽ⁿ⁾ を Lemma 4.2 (4.11) の共役 triple(または marked factorization)で証明書化 — 個数一致・指数一致では不足
4. 群構造: 乗積表 ≅ Thm 4.6(恒等式 (4.19)(4.20)・単位・結合・**(3.54) の逆元との一致**まで)。m の法 N_ord と u = 2m+1 の法 2n を混同しない
5. 2 冪 n = 4, 8, 16: |GT| = 4, 16, 64、H̃_α への明示同型、α ≥ 3 の**非可換 witness の積の保存**
6. reduction: **branch suite (q,n) = (8,4), (36,12), (12,4), (18,3), (9,3)**(Thm 4.4 の証明分岐を被覆)+ 関手性 R∘R = R (5.3) + 代表元不変性((m,f) ∼ (m+N_ord, fh))
7. **N₅ control(c ≠ 1)**: β₅: B₃ → S₃×C₅(σ₁ ↦ ((12),t), σ₂ ↦ ((23),t))、N₅ = ker β₅(位数 30 の商)。PB₃/N₅ ≅ C₅(x,y ↦ t², c ↦ t)、N_ord = 5、期待 |GT(N₅)| = 4(m ∈ {0,1,3,4}, f = 1)。**full B₃/N₅ 上で (3.3)(3.4) の c^m 項と T(c) = c^{2m+1} を検査** — Dih では c = 1 のため中心項が一度も試されない盲点への control
8. LS 条件 witness(Thm 5.2): n = 3 と n = 12 で全許容 (m,k)、特に論文が読者に委ねた m ≡ 2, 3 mod 6

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
