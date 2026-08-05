# 精密読解ノート: arXiv 2008.00066v2 — What are GT-shadows?(Dolgushev–Le–Lorenz, 2021-10-31, 54pp)

> 状態: **candidate**(司令塔照合まで)。B₄ ベース**本来系 GT-shadows の定義正本**(裁定 596 指示による抽出)。
> 照合方法: pdftotext 全文 + **ページ画像(150dpi)原文照合済**: p.9, 12, 13, 16, 23, 25, 29, 40, 44, 45, 47, 48, 49。
> 表記: 論文の GT はすべて profinite 版 ĜT(hat 付き)。本ノートでは文脈上明らかな限り hat を省略することがあるが、**GT = ĜT = Aut(P̂aB)** である(p.3)。charming 系の記号は原文どおり ♡(GT♡(N), GTSh♡)。

## 0. 節構成(p.1–2)

| § | 内容 | ページ |
|---|---|---|
| 1 | Introduction(1.1 G_ℚ↔GT・1.2 GTSh 概観・1.4 記法) | p.2–7 |
| 2 | GT-pairs and GT-shadows(2.1 compatible eq. rel.・2.2 N↦~_N・2.3 GT_pr(N)・2.4 Aut(P̂aB) 由来・2.5 groupoid GTSh・2.5.1 virtual cyclotomic character・2.6 charming) | p.7–28 |
| 3 | Main Line functor ML と ĜT(3.1 settled/isolated・3.2 Thm 3.8 証明) | p.29–38 |
| 4 | 計算機実験(4.1 顕著例・4.2 charming∧fake?・4.3 Furusho 性質・open questions) | p.38–43 |
| A | operad PaB と profinite 完備化(A.1 Bₙ/PBₙ・A.2 PaB(n)・A.3 operad 構造・A.4 coface 準同型・A.5 P̂aB) | p.43–49 |
| B | Abelian setting の charming GT-shadows(Thm B.2 = 全 genuine) | p.50–52 |

---

## 1. GT-shadow の定義一式(B₄ 版)

### 1.1 土台: truncated operad PaB^≤4(§1.2 p.4, §1.4 p.6–7)【画像照合済 p.12, 45】

- **PaB^≤4 := PaB(1) ⊔ PaB(2) ⊔ PaB(3) ⊔ PaB(4)**(arity 4 での切り詰め、p.4)。4-truncated operad の公理は (1.9) p.6(Sₙ 作用+挿入 ∘ᵢ: G(n)×G(m)→G(n+m−1) for n+m−1≤4)。
- PaB(n) の対象 = 括弧付き置換列(A.2 節 p.45)。射: **Hom_PaB(τ₁,τ₂) := ρ⁻¹(𝔭(τ₂)⁻¹∘𝔭(τ₁)) ⊂ Bₙ**(A.7, p.45)。合成は Bₙ の積。Aut_PaB(n)(τ) = PBₙ(p.2)。
- **忘却写像 ou: PaB(n) → Bₙ**(A.8)、ou(γ·η)=ou(γ)·ou(η)。**切断 𝔪: Bₙ → PaB(n)**(A.10, source は ((1,2)3)…n))、ou∘𝔪 = id、**𝔪(g₁·g₂) = ρ(g₂)⁻¹(𝔪(g₁))·𝔪(g₂)**(A.11)。
- 生成元(Fig 2.1 p.12 = Fig A.3 p.46): **braiding β ∈ Hom_PaB(2)((1,2),(2,1))**(σ₁ に対応)と **associator α ∈ Hom_PaB(3)((1,2)3, 1(2,3))**(B₃ の単位元に対応、ただし対象が違うので恒等射ではない、p.45)。
- **Theorem A.1**(p.48; = Fresse [9, Theorem 6.2.4]): PaB は α, β で生成され、全関係式は pentagon (A.13) + hexagon 2 本 (A.14)(A.15) の帰結。PaB^≤4 でも同じ(§2.3 p.12: PaB(0) が空なので Theorem A.1 が truncation に降りる)。

### 1.2 窓に相当する対象: poset NFI_{PB₄}(B₄)(§1.2 p.4)【画像照合済 p.9】

- **NFI_{PB₄}(B₄) := { N ⊴ B₄ | 指数有限, N ≤ PB₄ }**(p.4)。これが GTSh の対象(= B₃-gentle 系の「窓」の B₄ 版)。
- N から誘導する下位 arity の正規部分群(**(2.4)(2.5) p.9・画像照合済** — 裁定 252 の読み違い箇所):
  - **(2.4) N_PB₃ := φ₁₂₃⁻¹(N) ∩ φ₁₂,₃,₄⁻¹(N) ∩ φ₁,₂₃,₄⁻¹(N) ∩ φ₁,₂,₃₄⁻¹(N) ∩ φ₂₃₄⁻¹(N)**(5 つの coface 逆像の交わり。N∩PB₃ ではない)
  - **(2.5) N_PB₂ := ϕ₁₂⁻¹(N_PB₃) ∩ ϕ₁₂,₃⁻¹(N_PB₃) ∩ ϕ₁,₂₃⁻¹(N_PB₃) ∩ ϕ₂₃⁻¹(N_PB₃)**
- **Prop 2.2**(p.9): N_PB₃ ∈ NFI_{PB₃}(B₃)、N_PB₂ ∈ NFI_{PB₂}(B₂)(B₃-正規性まで出る)。
- **N_ord := |PB₂ : N_PB₂|**、N_PB₂ = ⟨x₁₂^{N_ord}⟩。**Prop 2.3**(p.10): N_ord = lcm(ord(x₁₂N_PB₃), ord(x₂₃N_PB₃), ord(cN_PB₃))(x₁₂x₁₃ 版・x₁₃x₂₃ 版とも一致; 証明は x₁₂x₁₃ = x₂₃⁻¹c, x₁₃x₂₃ = x₁₂⁻¹c を使用)。※ 2401 の (3.1) N_ord 定義と同型の式。
- **compatible equivalence relation ~_N**(§2.2 p.10): γ ~_N γ̃ :⟺ 同一 source/target かつ **ou(γ⁻¹·γ̃) ∈ N_PBₙ**(N_PB₄ := N)。**Prop 2.4**(p.10–12): ~_N は Def 2.1(p.7 — 合成・Sₙ 作用・∘ᵢ と両立)の意味で compatible、N ↦ ~_N は functor。商 **PaB^≤4/~_N** は有限 groupoid の truncated operad。

### 1.3 GT-pair(§2.3)【画像照合済 p.12–13 — 関係式の逐語】

PaB^≤4 → PaB^≤4/~_N なる truncated operad の射 (2.16) は、対
**(m + N_ord ℤ, f N_PB₃) ∈ ℤ/N_ord ℤ × PB₃/N_PB₃**(2.17)
と全単射対応し、課される関係式は次の 3 本(**Definition 2.6 p.13**: これを満たす対 = **GT-pair**、集合 GT_pr(N)):

- **hexagon 1(2.18)、B₃/N_PB₃ 内**:
  σ₁ x₁₂^m f⁻¹ σ₂ x₂₃^m f N_PB₃ = f⁻¹ σ₁σ₂ (x₁₃x₂₃)^m N_PB₃
- **hexagon 2(2.19)、B₃/N_PB₃ 内**:
  f⁻¹ σ₂ x₂₃^m f σ₁ x₁₂^m N_PB₃ = σ₂σ₁ (x₁₂x₁₃)^m f N_PB₃
- **pentagon(2.20)、PB₄/N 内**:
  **φ₂₃₄(f) φ₁,₂₃,₄(f) φ₁₂₃(f) N = φ₁,₂,₃₄(f) φ₁₂,₃,₄(f) N**

対応する射は **T_{m,f}(α) := [α·𝔪(f)]、T_{m,f}(β) := [β·𝔪(x₁₂^m)]**(p.13)。
well-defined 性: (m,f) が満たせば (m+qN_ord, fh)(q∈ℤ, h∈N_PB₃)も満たす(p.13)。代表対の同値類を [(m,f)] と書く。

pentagon の F₂ 語形(生成元代入後; (2.64) p.27 に明示):
f₁⁻¹(x₁₃x₂₃, x₃₄) f₁⁻¹(x₁₂, x₂₃x₂₄) f₁(x₂₃, x₃₄) f₁(x₁₂x₁₃, x₂₄x₃₄) f₁(x₁₂, x₂₃) ∈ K(f₁∈F₂ のとき)。

### 1.4 誘導準同型(Cor 2.7–2.8)【画像照合済 p.16】

- **T^{Bₙ}_{m,f}(g) := ou(T_{m,f}(𝔪(g)))** は群準同型 Bₙ → Bₙ/N_PBₙ(n=2,3,4)、制限で T^{PBₙ}_{m,f}: PBₙ → PBₙ/N_PBₙ(2.23)(2.24)。
- **(2.25)** T^{B₄}(σ₁) = σ₁x₁₂^m N、T^{B₄}(σ₂) = φ₁₂₃(f)⁻¹(σ₂x₂₃^m)φ₁₂₃(f) N、T^{B₄}(σ₃) = φ₁₂,₃,₄(f)⁻¹(σ₃x₃₄^m)φ₁₂,₃,₄(f) N。
- **(2.26)** T^{B₃}(σ₁) = σ₁x₁₂^m N_PB₃、T^{B₃}(σ₂) = f⁻¹(σ₂x₂₃^m)f N_PB₃。T^{B₂}(σ₁) = σ₁x₁₂^m N_PB₂。
- **(2.28)** T^{PB₃}(x₁₂) = x₁₂^{2m+1} N_PB₃、T^{PB₃}(x₂₃) = f⁻¹x₂₃^{2m+1}f N_PB₃。
- **(2.29)** T^{PB₃}(x₁₃) = x₁₂^{−m}σ₁⁻¹ f⁻¹x₂₃^{2m+1}f σ₁x₁₂^m N_PB₃、**T^{PB₃}(c) = c^{2m+1} N_PB₃**(証明は (2.18)(2.19) と x₁₃x₂₃=x₁₂⁻¹c, x₁₂x₁₃=x₂₃⁻¹c を使用、p.16)。※ 2401 Prop 3.5 (3.20) と同型。

### 1.5 GT-shadow(Definition 2.9, p.17)

- **GT(N) := { [(m,f)] ∈ GT_pr(N) | T^{PB₄}, T^{PB₃}, T^{PB₂} がすべて全射 }**。元を **GT-shadow** と呼ぶ。
- **(2.36)**: T^{PB₂} 全射 ⟺ **2m+1 が ℤ/N_ord ℤ の単元**。これを満たす GT-pair を **friendly** と呼ぶ(p.17)。
- **Prop 2.10**(p.17): [(m,f)] GT-shadow ⟺ T^{PB₃} と T^{PB₂} が全射 ⟺ T_{m,f}: PaB^≤4 → PaB^≤4/~_N が全射(PB₄ 側の全射性は自動で従う)。

### 1.6 groupoid 構造 GTSh(§2.5)【画像照合済 p.23 — 合成則の逐語】

- **Prop 2.11**(p.18–21): **N^s := ker(T^{PB₄}_{m,f}) ∈ NFI_{PB₄}(B₄)** で、T_{m,f} の誘導する同値関係 ~^s は ~_{N^s} に一致。
- **Cor 2.12**(p.21): 指数保存 — |PB₄:N^s| = |PB₄:N|、|PB₃:N^s_PB₃| = |PB₃:N_PB₃|、**N^s_ord = N_ord**(N^s_PB₂ = N_PB₂)。
- **Cor 2.13**(p.21–22): T_{m,f} = T^isom_{m,f} ∘ P_{N^s} と分解し、T^isom_{m,f}: PaB^≤4/~_{N^s} ≅ PaB^≤4/~_N。{[(m,f)] ∈ GT(N) | N^s = ker T^{PB₄}} ≅ Isom(PaB^≤4/~_{N^s}, PaB^≤4/~_N) の全単射 (2.50)。
- **groupoid GTSh**((2.51) p.22): Ob = NFI_{PB₄}(B₄)、**Hom(Ñ, N) := Isom(PaB^≤4/~_Ñ, PaB^≤4/~_N)** = {[(m,f)] ∈ GT(N) | ker(T^{PB₄}_{m,f}) = Ñ}。**source = ker、target = N**(GT-shadow = (1.5) の truncated operad 同型、と intro でも定義)。
- **合成則(Prop 2.14, (2.52) p.23)**: [(m₂,f₂)] ∈ Hom(N⁽²⁾,N⁽³⁾), [(m₁,f₁)] ∈ Hom(N⁽¹⁾,N⁽²⁾) のとき [(m₂,f₂)]∘[(m₁,f₁)] = [(m,f)] で
  **m := 2m₁m₂ + m₁ + m₂、 f N⁽³⁾_PB₃ := f₂N⁽³⁾_PB₃ · T^{PB₃}_{m₂,f₂}(f₁)**。
- **practical**(Remark 2.15, (2.54) p.23): f ∈ F₂ ≤ PB₃ で代表できる shadow。practical に限れば合成は自由群語の代入公式
  **(2.55) m := 2m₁m₂+m₁+m₂、 f(x,y) := f₂(x,y) · f₁(x^{2m₂+1}, f₂(x,y)⁻¹ y^{2m₂+1} f₂(x,y))**
  (practical は部分 groupoid をなす)。※ ℤ×F₂ で代表できない全射 PaB^≤4 → PaB^≤4/~_N の存否は**未解決**(p.23 下)。計算機実装 [4] は practical のみ扱う(脚注 5 p.5, §4 p.38–39)。
- **virtual cyclotomic character**(§2.5.1, Cor 2.16 (2.56) p.24): functor Ch_cyclot: GTSh → (有限巡回群): N ↦ PB₂/N_PB₂ ≅ ℤ/N_ord ℤ、[(m,f)] ↦ (x₁₂N_PB₂ ↦ x₁₂^{2m+1}N_PB₂)。同一連結成分内で N_ord は共通。**Remark 2.17 (2.57)**: g ∈ G_ℚ 由来の shadow では Ch_cyclot(m,f)(x₁₂N_PB₂) = x₁₂^{χ(g)_{N_ord}} N_PB₂(χ = 円分指標)。

### 1.7 charming(§2.6, Definition 2.19, p.25)【画像照合済】

[(m,f)] ∈ GT(N) が **charming** ⟺
1. 剰余類 f N_PB₃ が **f₁ ∈ [F₂, F₂]** で代表できる、かつ
2. **(2.61) T^{F₂}_{m,f} := T^{PB₃}_{m,f}|_{F₂} : F₂ → F₂/(N_PB₃ ∩ F₂) が全射**。

- 記法 **N_F₂ := N_PB₃ ∩ F₂**(2.62)。ker(T^{F₂}) = N^s_F₂、|F₂:N^s_F₂| = |F₂:N_F₂|。
- **Prop 2.18**(p.25): T̂ ∈ Aut(P̂aB^≤4) は PB̂₃ ≅ F̂₂ × ℤ̂ の分解を保つ — (2.58) T̂(x)=x^{2m̂+1}, T̂(y)=f̂⁻¹y^{2m̂+1}f̂、(2.59) T̂(c)=c^{2m̂+1}。
- **Prop 2.20**(p.26–27): **genuine ⇒ charming**(証明は Prop 2.5/3.9 の窓補給と、pentagon (2.64) から x₁₂-指数和 s_x・x₂₃-指数和 s_y が q の倍数になることを使い f₁x₁₂^{−s_x}x₂₃^{−s_y} ∈ [F₂,F₂] に取り替える)。系: **Cor 2.21** ∀(m̂,f̂)∈ĜT で f̂ ∈ ([F̂₂,F̂₂])^cl。
- **GT♡(N) := charming な shadow の集合**。**Prop 2.22**(p.28): charming は合成と逆で閉じ、部分 groupoid **GTSh♡** をなす(逆の証明: f⁻¹ の交換子分解を T^{F₂} 全射で引き戻す)。

---

## 2. B₃-gentle 系(arXiv 2401.06870)との正確な対応

**注意: 本論文(2020–21)は 2401(2024)より先行し、「gentle」の語は登場しない。以下の対応は司令塔指示による突合(導出注記つき)。**

1. **hexagon は完全一致(導出)**: (A.5) x₁₃x₂₃ = x₁₂⁻¹c、x₁₂x₁₃ = x₂₃⁻¹c(p.44 画像照合; c := x₂₃x₁₂x₁₃ = (σ₁σ₂)³)を (2.18)(2.19) に代入し σ₁x₁₂^m = σ₁^{2m+1}, σ₂x₂₃^m = σ₂^{2m+1} と書けば、2401 の (3.3) σ₁^{2m+1}f⁻¹σ₂^{2m+1}f N = f⁻¹σ₁σ₂x₁₂^{−m}c^m N、(3.4) と**逐語一致**する。差は商をとる群のみ: 本論文は B₃/N_PB₃(N_PB₃ は B₄ 窓 N から (2.4) で誘導)、2401 は B₃/N(N ∈ NFI_{PB₃}(B₃) が直接の窓)。
2. **公理の差 = pentagon (2.20) の 1 本のみ**。座標への現れ方: pentagon は f にのみ制約(m を含まない)で、判定の場が PB₄/N(4 本目の紐が要る)。hexagon 2 本は (m,f) 双方に制約で場は B₃/N_PB₃。→ B₃ 窓しか持たない gentle 系では (2.20) が**課せない**(φ の行き先 PB₄ の商が窓に無い)。
3. **窓の射影(導出)**: N ↦ N_PB₃ は NFI_{PB₄}(B₄) → NFI_{PB₃}(B₃) の写像(Prop 2.2)であり、[(m,f)] ∈ GT(N) の (2.18)(2.19)+全射性データは mod N_PB₃ の gentle 型 shadow データに落ちる。ただし**本論文はこの忘却 functor を明示的には構成していない**(それは 2401 §4 と 2405 Remark 1.2 の仕事)。
4. **逆向きの窓補給(重要装置)**: **Prop 2.5 / Prop 3.9(A)**(p.12, p.33): ∀N ∈ NFI(PB₃) に対し K ∈ NFI^isolated_{PB₄}(B₄) で **K_PB₃ ≤ N** となるものが存在。構成は明示的: ψ: PB₃→Sₙ (ker ψ = N) を **ψ̃(x₁₂)=ψ(x₁₂), ψ̃(x₂₃)=ψ(x₂₃), ψ̃(x₁₃)=ψ(x₁₃), ψ̃(x₁₄)=ψ̃(x₂₄)=ψ̃(x₃₄):=id** で PB₄→Sₙ に延長((A.3) で well-defined)し、φ₁₂₃⁻¹(ker ψ̃) = N を得て、指数 |PB₄:ker ψ̃| の正規部分群全交叉(特性部分群)→ Cor 3.5 で isolated 化。(B) は PB₂ 版(ψ̃(x₁₂)=ψ(x₁₂), ψ̃(x₂₃)=ψ(x₁₂)⁻¹, 残り id、(3.12))。
5. **「同名別物」の用語差(要注意)**:
   - 2008 の **GT-shadow** = GT-pair(hexagon×2+pentagon)+ 全射性(Def 2.9)。**charming** は追加条件(f∈[F₂,F₂] 代表+T^{F₂} 全射)で Def 2.19。**friendly** = 2m+1 単元 (2.36)。
   - 2401 の **GT-shadow** = charming GT-pair + 全射性(2401 Def 3.7)で、そこでの charming は「2m+1 単元 ∧ f が商の交換子部分群に入る」(対のレベルの条件)。**つまり 2401 の "GT-shadow" は 2008 の "charming GT-shadow" 側に対応し、2008 の GT(N)(非 charming 込み)に相当する層は 2401 には無い**。集合記号も 2008: GT(N) ⊃ GT♡(N) / 2401: GT_pr(N) ⊃ GT♡_pr(N) → GT(N) とずれる。
6. **coarse 版 GT₀ との区別**(Remark 1.3, p.5): pentagon を外した ĜT₀(Harbater–Schneps [15])は truncated operad **PaB^≤3** の連続自己同型群であり、ĜT ≤ ĜT₀。Guillot [12][13] はこの coarse 版の shadow 変種。※ 2401 の ĜT_gen(B₃ ベース・hexagon のみ)は思想的にこの系列だが定義の場が異なる(B₃ 直接)。

---

## 3. genuine / settled / isolated と算術供給

### 3.1 genuine / fake(Definition 2.19 前半, p.25; intro (1.7) p.5)

- [(m,f)] ∈ GT(N) が **genuine** :⟺ ∃T̂ ∈ ĜT = Aut(P̂aB) が図式 (1.7)(P̂aB^≤4 → T̂ → P̂aB^≤4、両縦射 = 標準射影、下辺 = [(m,f)] の同型)を可換にする(= 「T̂ から来る」§2.4 の意味: T_N := P̂_N ∘ T̂ ∘ I が [(m,f)] を与える (2.31))。そうでなければ **fake**(命名は Harbater、脚注 4 p.5)。
- genuine ⇒ charming(Prop 2.20)。逆は未解決(Question 4.6: **charming ∧ fake の例は見つかっていない** — §4.2: 35 窓リスト内の全 24 包含対 (N⁽ʲ⁾ ≤ N⁽ⁱ⁾) で GT♡(N⁽ʲ⁾)→GT♡(N⁽ⁱ⁾) が全射と実測)。
- **survive**(Definition 3.12, p.38): K ≤ N のとき自然写像 (3.24) GT♡(K) → GT♡(N)(同じ代表対 (m,f) ∈ ℤ×F₂ を K の shadow として読む)。[(m,f)] ∈ GT♡(N) が **K に survive** :⟺ この写像の像に入る。
- **Cor 3.13**(p.38): **[(m,f)] genuine ⟺ ∀K ≤ N (K ∈ NFI_{PB₄}(B₄)) に survive**。(Thm 3.8 + Prop 3.3 の帰結。genuine 判定の有限近似原理。)

### 3.2 settled / isolated / conjugates(§3.1, Definition 3.2, p.29)【画像照合済】

- **GTSh♡_conn(N)** = GTSh♡ における N の連結成分。Ñ ∈ Ob(GTSh♡_conn(N)) ⟺ ∃[(m,f)] ∈ GT♡(N): Ñ = ker(T^{PB₄}_{m,f})。この Ñ を N の **conjugates** と呼ぶ。**Prop 3.1**: GTSh♡_conn(N) は有限 groupoid。連結なら同指数(p.29)。
- **settled**(Def 3.2): charming shadow [(m,f)] ∈ GT♡(N) で source = target、i.e. **ker(T^{B₄}_{m,f}) = N**(= N の自己同型射)。
- **isolated**(Def 3.2): N の**全** shadow ∈ GT♡(N) が settled ⟺ GTSh♡_conn(N) が一対象 ⟺ **GT♡(N) が群**(Aut_GTSh♡(N))。
- **Prop 3.3**((3.1) p.29): **N♯ := ∩_{K ∈ Ob(GTSh♡_conn(N))} K は isolated**。実験上 conjugates は高々 2 個なので実用的な isolated 生成法(Remark 3.4)。
- **Cor 3.5**: isolated 元の subposet **NFI^isolated_{PB₄}(B₄)** は cofinal。**Prop 3.6**: isolated 2 元の交わりも isolated。
- 注意(Remark 4.1 p.39): isolated の定義は charming ベース — GT(N)(非 charming 込み)に non-settled 元を持つ isolated N の存否は原理的に開いている(実験では未遭遇)。

### 3.3 Main Line functor と主定理(§3.1–3.2)

- **ML(N) := GT♡(N)**(isolated N に対し有限群)。**Prop 3.7**(p.31): K ≤ N(共に isolated)に対し ML_{K,N}: ML(K)→ML(N)、T_{m,f} ↦ P_{K,N}∘T_{m,f} が群準同型で functor ML: NFI^isolated_{PB₄}(B₄) → FinGrp をなす(合成の整合 (3.10))。
- **Theorem 3.8**(p.33): **ĜT ≅ lim(ML)**。証明部品: Cor 3.10 P̂aB^≤4 ≅ lim_{K isolated} PaB^≤4/~_K(同相含む)、Prop 3.11 図式 (3.17) 可換、単射性 = 稠密性+Hausdorff、全射性 = 族 {T^isom_K} から連続自己同型を再構成 (3.22)。
- ※ これが「G_ℚ を有限次 Galois 拡大の Gal で近似する functor の ĜT 類似」(p.2–3 の目標宣言)の実現。

### 3.4 G_ℚ からの算術供給(§1.1, p.3–4)

- π₁ 理論による外作用 G_ℚ ↷ F̂₂(P¹_ℚ̄∖{0,1,∞})を inertia 保存で持ち上げ:
  **(1.4) g(x) = x^{χ(g)}, g(y) = f̂_g(x,y)⁻¹ y^{χ(g)} f̂_g(x,y)**(χ = 円分指標、f̂_g ∈ ([F̂₂,F̂₂])^cl)。
- 対 **((χ(g)−1)/2, f̂_g) ∈ ℤ̂ × F̂₂** が ĜT の元を定め、(1.1) G_ℚ → ĜT は群準同型・**Belyi の定理により単射**(p.4; 出典 [7 §4][16 §3][28 Thm 4.7.7])。全射性 = Ihara の ICM 問題(未解決、p.2)。
- shadow への降下: T̂ ∈ ĜT と任意の窓 N に対し T_N := P̂_N∘T̂∘I(2.31)が genuine shadow を与える。円分成分は Remark 2.17 (2.57): Ch_cyclot = χ mod N_ord。
- **Remark B.3**(p.52): Abelian setting では全 charming shadow が **G_ℚ の元から来る**。非 Abelian で「genuine だが G_ℚ 由来でない」shadow が存在すれば (1.1) は非全射(その判定手段は現代数学に無い、と脚注 15)。

---

## 4. 有限窓の計算可能性に効く構造

### 4.1 群論的基礎データ(App A.1)【画像照合済 p.44】

- **Bₙ 表示 (A.1)**: ⟨σ₁,…,σ_{n−1} | σᵢσⱼ=σⱼσᵢ (|i−j|≥2), σᵢσ_{i+1}σᵢ=σ_{i+1}σᵢσ_{i+1}⟩。
- **x_ij := σ_{j−1}⋯σ_{i+1} σᵢ² σ_{i+1}⁻¹⋯σ_{j−1}⁻¹**(A.2)。**PB₄ 表示 (A.3)**(x_rs⁻¹ x_ij x_rs の 4 場合分け — GAP 実装の基準)。
- PB₃: x₁₂=σ₁², x₂₃=σ₂², x₁₃=σ₂σ₁²σ₂⁻¹(A.4)。**c := x₂₃x₁₂x₁₃ = x₁₂x₁₃x₂₃ = (σ₁σ₂)³ = (σ₂σ₁)³**(A.5)、Z(PB₃)=Z(B₃)=⟨c⟩、PB₃ ≅ F₂×ℤ(F₂=⟨x₁₂,x₂₃⟩)。
- **(A.6)** σ₁⁻¹x₂₃σ₁ = x₁₃、σ₂⁻¹x₁₂σ₂ = x₂₃⁻¹x₁₂⁻¹c、σ₂⁻¹x₁₃σ₂ = x₁₂。

### 4.2 coface 準同型の生成元値(A.4)【画像照合済 p.48–49】

φ₁₂₃, φ₁₂,₃,₄, φ₁,₂₃,₄, φ₁,₂,₃₄, φ₂₃₄: PB₃→PB₄(A.16)、ϕ₁₂, ϕ₁₂,₃, ϕ₁,₂₃, ϕ₂₃: PB₂→PB₃(A.17)。**明示値 (A.18)(A.19)**:

| φ | x₁₂ ↦ | x₂₃ ↦ | x₁₃ ↦ |
|---|---|---|---|
| φ₁₂₃ | x₁₂ | x₂₃ | x₁₃ |
| φ₂₃₄ | x₂₃ | x₃₄ | x₂₄ |
| φ₁₂,₃,₄ | x₁₃x₂₃ | x₃₄ | x₁₄x₂₄ |
| φ₁,₂₃,₄ | x₁₂x₁₃ | x₂₄x₃₄ | x₁₄ |
| φ₁,₂,₃₄ | x₁₂ | x₂₃x₂₄ | x₁₃x₁₄ |

(A.19): ϕ₁₂(x₁₂)=x₁₂、ϕ₂₃(x₁₂)=x₂₃、ϕ₁₂,₃(x₁₂)=x₁₃x₂₃、ϕ₁,₂₃(x₁₂)=x₁₂x₁₃。

### 4.3 窓の機械表現と商の作り方(§4 冒頭 p.38–39)

- 窓 N は準同型 ψ: PB₄ → S_d の核として表現。ψ は **6 つ組 (g₁₂,g₂₃,g₁₃,g₁₄,g₂₄,g₃₄) ∈ (S_d)⁶ で (A.3) を満たすもの**(4.1)。
- N_PB₃ の計算 = (2.4) を (A.18) で置換群の言葉に落とす(5 本の合成 ψ∘φ の核の交わり)。N_ord = Prop 2.3 の lcm。
- P̂aB^≤4 の「pedestrian」記述(A.5 p.49): 連結 groupoid の profinite 完備化 Ĝ の射 = λ·h(λ ∈ G(a,b) 固定、h ∈ Ĝ)— 実装は基点自己同型群の有限商のみで足りる。

### 4.4 実験データ(§4, Table 1 p.40)【画像照合済 — pdftotext は列崩れしていたため表は画像から転記】

35 窓 N⁽⁰⁾…N⁽³⁴⁾(全て F₂/N_F₂ 非 Abelian)。列: |PB₄:N| / |F₂:N_F₂| / |[F₂/N_F₂,F₂/N_F₂]| / N_ord / |GT(N)|(practical)/ |GT♡(N)| / isolated:

| i | PB₄指数 | F₂指数 | 交換子部分群位数 | N_ord | GT | GT♡ | isolated |
|---|---|---|---|---|---|---|---|
| 0 | 8 | 16 | 2 | 4 | 4 | 4 | True |
| 1 | 8 | 16 | 2 | 4 | 8 | 4 | True |
| 2 | 12 | 36 | 4 | 3 | 18 | 6 | True |
| 3 | 21 | 63 | 7 | 3 | 36 | 12 | False |
| 4 | 21 | 63 | 7 | 3 | 36 | 12 | False |
| 5 | 24 | 288 | 8 | 6 | 72 | 12 | True |
| 6 | 24 | 144 | 4 | 6 | 72 | 12 | True |
| 7 | 48 | 144 | 4 | 6 | 72 | 12 | True |
| 8 | 60 | 1500 | 60 | 5 | 100 | 20 | True |
| 9 | 60 | 900 | 4 | 15 | 360 | 24 | True |
| 10 | 72 | 144 | 18 | 4 | 16 | 8 | False |
| 11 | 72 | 144 | 18 | 4 | 16 | 8 | False |
| 12 | 108 | 972 | 27 | 6 | 72 | 12 | True |
| 13 | 120 | 6000 | 60 | 10 | 400 | 40 | True |
| 14 | 147 | 441 | 49 | 3 | 216 | 72 | True |
| 15 | 168 | 8232 | 168 | 7 | 294 | 42 | True |
| 16 | 168 | 1344 | 168 | 4 | 64 | 32 | False |
| 17 | 168 | 1344 | 168 | 4 | 64 | 32 | False |
| 18 | 180 | 13500 | 60 | 15 | 600 | 40 | True |
| 19 | 216 | 7776 | 216 | 6 | 72 | 12 | True |
| 20 | 240 | 6000 | 60 | 10 | 400 | 40 | True |
| 21 | 324 | 8748 | 108 | 9 | 486 | 54 | True |
| 22 | 504 | 40824 | 504 | 9 | 486 | 54 | True |
| 23 | 504 | 24696 | 504 | 7 | 294 | 42 | True |
| 24 | 648 | 1296 | 162 | 4 | 32 | 16 | True |
| 25 | 720 | 54000 | 240 | 15 | 1800 | 120 | True |
| 26 | 1512 | 40824 | 504 | 9 | 486 | 54 | False |
| 27 | 1512 | 40824 | 504 | 9 | 486 | 54 | False |
| 28 | 2520 | 63000 | 2520 | 5 | 200 | 40 | True |
| 29 | 2520 | 45360 | 2520 | 6 | 144 | 48 | True |
| 30 | 28224 | 225792 | 28224 | 4 | 512 | 256 | True |
| 31 | 181440 | 8890560 | 181440 | 7 | 588 | 84 | True |
| 32 | 181440 | 9072000 | 181440 | 10 | 800 | 160 | True |
| 33 | 181440 | 40824000 | 181440 | 15 | **≥ 1800** | 120 | True |
| 34 | 762048 | 20575296 | 254016 | 9 | **≥ 4374** | 486 | True |

- 非 isolated 窓の conjugate 対と交わり(p.39): N⁽⁴⁾~N⁽³⁾ で N⁽³⁾∩N⁽⁴⁾=N⁽¹⁴⁾、N⁽¹¹⁾~N⁽¹⁰⁾ で ∩=N⁽²⁴⁾、N⁽¹⁷⁾~N⁽¹⁶⁾ で ∩=N⁽³⁰⁾、N⁽²⁷⁾~N⁽²⁶⁾ で ∩=N⁽³⁴⁾。
- 計算コスト実録(p.39): N⁽³¹⁾ |GT|=588 の確定に F₂/N_F₂ の ~9×10⁶ 元走査で iMac (3.4GHz i5) 9 日超、N⁽³²⁾ で 10 日弱。

### 4.5 顕著例(§4.1)【N⁽¹⁹⁾/N⁽³⁴⁾ の生成元は画像照合済 p.40; N⁽¹⁹⁾ は本文 p.39】

- **Philadelphia subgroup N⁽¹⁹⁾**: |F₂:N_F₂| = 7776 = 2⁵·3⁵。ψ: PB₄→S₉ の核、**(4.3)** g₁₂=(1,3,2)(4,6,5), g₂₃=(1,4,9)(2,7,6), g₁₃=(1,7,5)(3,6,9), g₁₄=(2,6,7)(3,8,5), g₂₄=(1,8,6)(3,4,7), g₃₄=(1,2,3)(7,9,8)。isolated。**GT♡(N⁽¹⁹⁾) ≅ D₆ = ⟨r,s | r⁶, s², rsrs⟩(位数 12)**、ker(Ch_cyclot|) = ⟨r⟩ ≅ C₆。GT(N⁽¹⁹⁾) は 72 個中 charming 12 個(⟹ fake が少なくとも 60 個、§4.2 p.42)。
- **Mighty Dandy N⁽³⁴⁾**: |PB₄:N| = 762048 = 2⁶·3⁵·7²。ψ: PB₄→S₁₈ の核、生成元 **(4.4)**(p.40 画像照合; g₁₂=g₃₄, g₂₃=g₁₄ が同一置換である点に注意)。isolated。**|GT♡| = 486 = 2·3⁵**、ker(Ch_cyclot|) =: Ker₃₄ ≅ ℤ₉×ℤ₉(位数 81)、**GT♡(N⁽³⁴⁾) ≅ (ℤ₂×ℤ₃) ⋉ (ℤ₉×ℤ₉)**、Sylow-3 = ℤ₃⋉(ℤ₉×ℤ₉)(非可換位数 243・正規)。
- **Leila's subgroup N_L**(Schneps 提供、p.41): PB₄→S₁₃₀ の核。|PB₄:N_L| = 2²⁹·3¹² = 285315214344192、|PB₃:N_L,PB₃| = 2¹²·3⁶、|F₂:N_L,F₂| = 2¹⁰·3⁵ = 248832、N_ord = 12、|[F₂/N_F₂,F₂/N_F₂]| = 1728。**charming はわずか 48 個**、isolated。**GT♡(N_L) ≅ ℤ₂ ⋉ (ℤ₂×ℤ₂×ℤ₂×ℤ₃)**((4.5)(4.6): 非自明元の作用 a↔b, c↦c, d↦d⁻¹)、ker(Ch_cyclot|) = ⟨ab, c, d⟩。**|PB₄:N| ≫ |F₂:N_F₂| の例**(リスト 35 窓は全て逆向き)。

### 4.6 Furusho 性質(§4.3, p.42–43)— pentagon ⟹ hexagon の有限版

- **Property 4.2(strong)**: pentagon (2.20) mod N を満たす任意の f N_F₂ ∈ F₂/N_F₂ に対し、∃m: 2m+1 単元 ∧ (m,f) が hexagon (2.18)(2.19) を満たす。
- **Property 4.3(weak)**: 同上だが f N_F₂ ∈ [F₂/N_F₂, F₂/N_F₂] に制限。
- 実測: strong 成立 **(4.7)** = {N⁽¹⁾,N⁽²⁾,N⁽³⁾,N⁽⁴⁾,N⁽⁶⁾,N⁽⁷⁾,N⁽⁹⁾,N⁽¹⁰⁾,N⁽¹¹⁾,N⁽¹⁴⁾,N⁽²⁴⁾}(11 窓)、残り 24 窓は不成立。weak 成立 **(4.8)** = (4.7)+{N⁽⁰⁾,N⁽⁵⁾}(13 窓)、残り 22 窓は不成立。
- 定量例: **N⁽¹⁹⁾**: pentagon 充足 f は 216 個、うち hexagon 持ち上げ可能(∃m∈{0..5})は **36 個のみ**。**N⁽³⁴⁾**: [F₂/N_F₂,·] 内の pentagon 充足 4096 個(計算 52 時間超)、hexagon 持ち上げ可能は **243 個**。※ prounipotent 設定の Furusho の定理(pentagon⇒hexagon [2][10])は profinite 有限窓では**一般に破れる**、が原論文の含意。
- **Open questions**: 4.4(T^{PB₄} 全射 ⟹ T^{PB₂}, T^{PB₃} 全射か)、4.5(conjugates > 2 の窓はあるか)、4.6(charming∧fake の例)、4.7(非 Abelian 窓で genuine 全同定できる例)。

### 4.7 Abelian setting(App B)

- **Prop B.1**(p.50): PB₄/N Abelian ⟺ PB₃/N_PB₃ Abelian ⟺ F₂/N_F₂ Abelian。
- **Theorem B.2**(p.51, 「Kronecker–Weber の類似」): このとき **GT♡(N) = {(m+N_ordℤ, 1̄) | gcd(2m+1, N_ord)=1}** で、**全て genuine**。(証明: 円分指標の全射性 + N_ord 偶数のときは 4k | K₀ なる補助窓 K((B.7): ψ(x_ij) := (1,2,…,4k) 全生成元共通)で 2 解 {m*, m*+k} を分離。)

---

## 5. dessins との関係(要点のみ・深追いせず)

- 本論文自体に dessins への作用の節は**無い**。接続は: (i) Abstract/p.2 で Harbater–Schneps [14](dessins の Galois 軌道近似)を「very similar objects」の先行と明記、(ii) Guillot [12][13](coarse 版 GT₀ の変種・G-dessins)、(iii) Ellenberg [8]。
- 後続 2106.06645(既抽出: docs/notes/2106.06645-抽出ノート_v1.md)が、charming shadow の F₂/N_F₂ への作用として dessins(次数付き・子供の絵)への GTSh♡ 作用を実装し G_ℚ 軌道を近似する — 本論文の Cor 3.13(survive による genuine 判定)と Table 1 の窓群がその土台。

---

## 6. 252 系(PENT-π / pentagon lift)への所見 — 観察のみ・判断せず

1. **§4.3 の per-窓計数(pentagon 充足 f 数 → ∃m での hexagon 持ち上げ数)は (T2) と同型の測定**で、原論文に基準数がある: N⁽¹⁹⁾ 216→36、N⁽³⁴⁾ 4096→243 — (T2) 装置の較正正解データ候補(p.42–43)。
2. **Cor 3.13(genuine ⟺ 全下位窓へ survive)**は「fine で成立・射影で観察」の一方向性を定式化済み — red: GT(K_π)→GT_gen(N_A) の像評価 (T3) の紙側对応物(p.38)。
3. **Prop 3.9(A) の ψ̃ 延長トリック**(x₁₄,x₂₄,x₃₄ ↦ id)は与えられた B₃/PB₃ 窓の上に B₄ 窓を明示構成する装置 — K_π 型持ち上げ窓の標準生成法として使える(p.33)。
4. **Prop 2.10**: T^{PB₃}+T^{PB₂} 全射 ⟹ T^{PB₄} 全射(逆は Question 4.4 で開)— 全射検査は arity 3 以下で足りる(p.17)。
5. (2.20) は **f のみの条件**で m と独立 — pentagon 判定と m-走査(hexagon)の分離実装は原論文の構造どおり(p.13)。

## 7. UNKNOWN・注意点

- Table 1 の i=33, 34 の |GT| は原文で **≥ 1800 / ≥ 4374**(下界表示)。i=31, 32 は太字の確定値 588 / 800。
- N⁽³⁴⁾ の (4.4) で g₂₃ = g₁₄、g₁₂ = g₃₄(同一置換の再掲)— 誤植ではなく原文どおり(画像照合済)。
- ℤ×F₂ で代表できない onto 射 PaB^≤4 → PaB^≤4/~_N の存否は原論文でも UNKNOWN(p.23)。
- 「isolated だが GT(N)(charming 外)に non-settled 元を持つ窓」の存否も UNKNOWN(Remark 4.1)。
- 本論文の実装 [4] = Temple 大 Package GT(https://math.temple.edu/~vald/PackageGT/)— 第三者クロスチェック資源(CLAUDE.md 記載と一致)。
