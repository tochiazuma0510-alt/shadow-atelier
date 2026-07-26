# 照合ノート: Ih / Ih_N の定義の正確な形(速達 P1)

- 状態: **画像照合済み**(pdftocairo 150dpi・全引用をページ画像で原文照合)
- 照合日: 2026-07-26 / 照合者: reader(精密読解係)
- 対象: papers/2405.11725-nonabelian-quotients-gt-elementary.pdf(p.4–6)、papers/2401.06870-gt-shadows-gentle-version.pdf(p.15–16)
- 画像: スクラッチパッド p2405-03/04/05/06.png・p2401-15/16/17.png

## 結論(先頭)

1. **(a) 作用の形は速達記載と一致**: γ(x)=x^χ(γ)、γ(y)=f_γ⁻¹ y^χ(γ) f_γ(f⁻¹ が左・f が右、χ の指数は y の肩)。
2. **(b) 基点の指定は両論文とも一切なし**(0⃗1 も 01⃗ も tangential basepoint という語も不出現。grep で "tangential" "basepoint" 0 件)。基点は Ihara [15] への参照に暗黙委任。**どの接基点かは本 2 論文からは UNKNOWN**。
3. **(c) 向きは共変(covariant)**: Ih は「group homomorphism」と明記。anti-homomorphism / cofunctor の語は両論文で 0 件。合成則も E_{m₁,f₁}∘E_{m₂,f₂}=E_{m,f}((m,f)=(m₁,f₁)•(m₂,f₂))で共変。

---

## 1. arXiv 2405.11725 §1.3(p.4)— Ihara の作用と Ih の定義

### 1.1 Ihara の作用(§1.3、(1.4) と (1.5) の間の**無番号表示式**、p.4)

逐語(画像照合済み):

> In [15, Section 1], Y. Ihara constructed a splitting of (1.4) that gives us an action of G_ℚ on F̂₂ of the form
>
> g(x) = x^{χ(g)},  g(y) = f_g^{−1} y^{χ(g)} f_g,  g ∈ G_ℚ,
>
> where χ : G_ℚ → Ẑ^× is the cyclotomic character and the construction of the element f_g ∈ F̂₂ is described in great detail in [15, Section 1.4]. (See also [25, Corollary 4.7.3] and [25, Example 4.7.4].)

- **共役の位置**: f_g⁻¹ が左、f_g が右(f_g⁻¹ y^{χ(g)} f_g)。
- **χ の指数**: x は x^{χ(g)}、y は共役の内側の y^{χ(g)}。
- **基点**: この文に基点の指定なし。(1.4) は完全系列 1 → π₁(P¹_ℚ̄ − {0,1,∞}) → π₁(P¹_ℚ − {0,1,∞}) → G_ℚ → 1(p.4、(1.4))で、π₁ の基点は書かれていない。

### 1.2 Ih の定義((1.5)–(1.6)、p.4)

逐語:

> the formula
>
> Ih(g) := ( (χ(g) − 1)/2, f_g ) ∈ Ẑ × F̂₂   (1.5)
>
> defines a group homomorphism
>
> G_ℚ → ĜT   (1.6)
>
> and
> • Belyi's theorem [2] implies that homomorphism (1.6) is injective.

続けて(p.4):

> In this paper, we call the homomorphism in (1.6) the **Ihara embedding**. Since ĜT is a subgroup of ĜT_gen, formula (1.5) also defines an injective homomorphism G_ℚ ↪ ĜT_gen. We use the same notation Ih for the injective homomorphism G_ℚ ↪ ĜT_gen.

- 第 1 成分は **m̂ = (χ(g) − 1)/2 ∈ Ẑ**(χ そのものではない)。2m̂+1 = χ(g) が χ_vir との整合((1.7): χ_vir(m̂, f̂) := 2m̂ + 1、p.4)。
- **「group homomorphism」と明記 = 共変**。anti- の語なし。

### 1.3 Ih_N の定義(§1.3.1、(1.11)、p.5)

逐語:

> Composing 𝒫𝓡_N with the Ihara embedding Ih : G_ℚ ↪ ĜT_gen we get the following version of the Ihara homomorphism
>
> Ih_N := 𝒫𝓡_N ∘ Ih : G_ℚ → GT(N)   (1.11)
>
> for GT-shadows.

- 𝒫𝓡_N(m̂, f̂) := (𝒫̂_{N_ord}(m̂), 𝒫̂_{N_F₂}(f̂))((1.3)、p.3)。
- GT_arith(N) := Ih_N(G_ℚ)((1.12)、p.5)。
- **注意(Remark 1.4、p.6)**: N が isolated でない場合、GT(N) に自然な群構造がなく「Ih_N is not a group homomorphism」(逐語)。isolated なら群準同型。
- 可換図式: (1.8) p.4(χ = χ_vir ∘ Ih)、(1.13) p.5(χ 経由 (ℤ/N_ord ℤ)^× へ)、Remark 1.5 (1.14) p.6(𝓡_{H,N}(GT_arith(H)) = GT_arith(N))。

## 2. arXiv 2401.06870 §3((3.41)–(3.44)、p.15–16)— shadow 側の E_{m,f}

### 2.1 (3.41)(p.15)逐語:

> For every pair (m, f) ∈ ℤ × F₂, the formulas
>
> E_{m,f}(x) := x^{2m+1},  E_{m,f}(y) := f^{−1} y^{2m+1} f   (3.41)
>
> define an endomorphism E_{m,f} of F₂.

- Ihara 作用と同形: 指数 2m+1(= χ_vir)、f⁻¹ が左・f が右。**一致**。

### 2.2 (3.42)–(3.43)(p.15–16)逐語:

> A direct computation shows that
>
> E_{m₁,f₁} ∘ E_{m₂,f₂} = E_{m,f},   (3.42)
>
> where
>
> m := 2m₁m₂ + m₁ + m₂,  f := f₁ E_{m₁,f₁}(f₂).

> (m₁, f₁) • (m₂, f₂) := (2m₁m₂ + m₁ + m₂, f₁E_{m₁,f₁}(f₂))   (3.43)
>
> and the identity element (0, 1_{F₂}). Moreover, the assignment (m, f) ↦ E_{m,f} defines a homomorphism of monoids (ℤ × F₂, •) → End(F₂).

- **共変**: (m₁,f₁)•(m₂,f₂) ↦ E_{m₁,f₁}∘E_{m₂,f₂}(順序保存の monoid homomorphism)。cofunctor/anti- の語なし。
- 群oid 側も同順序: Prop 3.9(p.16)で [m₁,f₁] ∈ GTSh(N⁽²⁾,N⁽¹⁾)、[m₂,f₂] ∈ GT(N⁽³⁾,N⁽²⁾)、(3.45) の (m,f)(=(m₁,f₁)•(m₂,f₂))が GTSh(N⁽³⁾,N⁽¹⁾) の元で、(3.48): T^isom_{m₁,f₁} ∘ T^isom_{m₂,f₂} = T^isom_{m,f}。

### 2.3 (3.44)(p.16)逐語:

> Note that, if (m, f) ∈ ℤ × F₂ represents a GT-pair with the target N ∈ NFI_{PB₃}(B₃), then
>
> T^{F₂}_{m,f}(w) = E_{m,f}(w) N_{F₂},  ∀ w ∈ F₂,   (3.44)
>
> where T^{F₂}_{m,f} is defined in (3.21).

### 2.4 2401.06870 における Ih への言及

- 本文 p.10 のみ: 「Using the Ihara embedding Ih : G_ℚ ↪ ĜT (see [16, Section 1])」。**2401.06870 は Ih を自前定義せず** Ihara [16] に委任。Ih_N の定義は 2405.11725 (1.11) が正本。

## 3. 差分・注意点((d))

1. **基点 0⃗1 は両論文に不出現**。「接基点 0⃗1 における」という限定は本 2 論文の記述には存在しない(Ihara [15]/Neukirch 等の外部文献由来の慣習)。速達がこれを「定義の一部」として引くなら出典は [15, Section 1] 側であり、本 2 論文からは UNKNOWN。
2. 速達の f_γ の位置(左に f⁻¹・右に f)・χ 指数の位置は**両論文と完全一致**。「逆元の位置が逆」等の食い違いは**なし**。
3. Ih の第 1 成分は χ(g) でなく **(χ(g)−1)/2**((1.5))。作用の指数と shadow 指数の対応は χ(g) = 2m̂+1((1.7))。
4. 向きはすべて共変(homomorphism)。anti-homomorphism/cofunctor 規約は両論文とも不採用(語自体が 0 件)。
5. N が isolated でないときの Ih_N は群準同型でない(2405.11725 Remark 1.4、p.6)— 「準同型」と呼べるのは isolated N のときのみ。

---

## 追加照合: f の所属(f̂ ∈ [F̂₂,F̂₂]^top.cl. が定義の要求か)

- 状態: **画像照合済み**(q2401-01/02/06/07/11/26.png・q2405-02/11.png)
- 照合日: 2026-07-26

### 結論: **Yes — 両論文とも ĜT_gen の定義の明示的要求**(2401.06870 p.2・(2.8) p.7 / 2405.11725 p.2)

### A. arXiv 2401.06870

1. **Introduction(p.2)逐語**:

   > Just as ĜT, the group ĜT_gen consists of pairs (m̂, f̂) ∈ Ẑ × F̂₂ satisfying hexagon relations (1.1), (1.2), the invertibility condition and the following consequence of pentagon relation (1.3):
   >
   > f̂ ∈ [F̂₂, F̂₂]^{top. cl.}.

   - gentle 版は pentagon を落とし、その**帰結**である f̂ ∈ [F̂₂,F̂₂]^{top.cl.}(交換子部分群の位相的閉包)を定義条件として残す、と明記。

2. **正式定義((2.8)、§2.2、p.7)逐語**:

   > Let us denote by ĜT_gen,mon the subset of Ẑ × F̂₂ that consists of pairs
   >
   > (m̂, f̂) ∈ Ẑ × [F̂₂, F̂₂]^{top. cl.}   (2.8)
   >
   > satisfying the hexagon relations (2.9), (2.10).

   - **(2.8) の第 2 成分の属域そのものが [F̂₂,F̂₂]^{top.cl.}**。定義の一部であることは確定。

3. **Drinfeld の元の ĜT(p.1、§1)**: 「It consists of pairs (m̂, f̂) ∈ Ẑ × F̂₂ satisfying the hexagon relations: (1.1), (1.2), the pentagon relation: (1.3) ... and the invertibility condition.」— **ĜT 自体の定義には f̂ ∈ F̂₂′ の明示要求なし**(pentagon から従う帰結という扱い。p.2 の「consequence of pentagon relation (1.3)」)。

4. **shadow 側(有限側)の対応条件 = charming(p.11、§3)逐語**:

   > A GT-pair (3.5) is called charming if
   > • 2m + 1 represents a unit in the ring ℤ/N_ord ℤ and
   > • f N_F₂ ∈ [F₂/N_F₂, F₂/N_F₂], or equivalently the coset f N_F₂ can be represented by an element in the commutator subgroup [F₂, F₂] of F₂.

5. **profinite 版が shadow 側条件から復元されること(p.26、§5、Thm 5.2 の証明中)逐語**:

   > The element f̂ belongs to the topological closure of the commutator subgroup [F̂₂, F̂₂] in F̂₂ due to these properties:
   > • for every N ∈ NFI^isolated_PB₃(B₃), f̂(N_F₂) ∈ [F₂/N_F₂, F₂/N_F₂],
   > • the open subsets 𝒫̂⁻¹_{N_F₂}(1_{F₂/N_F₂}) ⊂ F̂₂, N ∈ NFI^isolated_PB₃(B₃) form a basis of neighborhoods of 1_{F̂₂} in F̂₂.

   - すなわち**有限側の f N_F₂ ∈ [F₂/N_F₂, F₂/N_F₂](全 isolated N)⇒ profinite 側の f̂ ∈ [F̂₂,F̂₂]^{top.cl.}** が明示的に述べられている(方向は「有限側条件の逆極限が profinite 条件を出す」)。

### B. arXiv 2405.11725

1. **p.2(§1 導入)逐語**:

   > The group ĜT_gen consists of pairs (m̂, f̂) ∈ Ẑ × F̂₂ satisfying the hexagon relations (see equations (1.1) and (1.2) in [6, Introduction]) and the technical condition f̂ ∈ [F̂₂, F̂₂]^{top.cl.}.

   - 「**the technical condition**」として定義に明示。

2. **(1.5) 周辺(p.4)**: f_g 自体には交換子条件の言明なし(「the construction of the element f_g ∈ F̂₂ is described in great detail in [15, Section 1.4]」のみ)。f_g ∈ [F̂₂,F̂₂]^{top.cl.} は Ih の像が ĜT ⊂ ĜT_gen に入るという主張(1.5)–(1.6) 経由の**含意**であり、p.4 に明示の式はない。

3. **shadow 側 = charming(Definition 2.1、p.11)逐語**:

   > If, in addition, the GT-pair satisfies
   >
   > gcd(2m + 1, N_ord) = 1  and  f N_F₂ ∈ [F₂/N_F₂, F₂/N_F₂],
   >
   > then we call it **charming**.

   - 有限側の条件は**剰余群の交換子部分群への所属**(coset レベル)。判定の釘付けは profinite 側((2.8)/p.2)で行うこと — 有限側は F₂/N_F₂ が完全群(例: A₅ 系)のとき [F₂/N_F₂, F₂/N_F₂] = F₂/N_F₂ となり条件が空虚化する。

### C. 文献ゲート用データ(判定には不使用)

2405.11725 参考文献 [15](p.33、逐語・行結合):

> [15] Y. Ihara, On the embedding of Gal(Q̄/Q) into ĜT. With an appendix by Michel Emsalem and Pierre Lochak. London Math. Soc. Lecture Note Ser., 200, The Grothendieck theory of dessins d'enfants (Luminy, 1993), 289–321, Cambridge Univ. Press, Cambridge, 1994.

---

## 二次資料照合: Schneps/Furusho(定理 A₅ 絶対較正 (I3*) の証拠固め)

- 状態: **画像照合済み**(pdftocairo 150dpi・スクラッチパッド schn-02/04/12/13/21.png・furu-13/23/24.png)
- 照合日: 2026-07-26 / 照合者: reader(精密読解係)
- 対象: papers/delivered/schneps_2005_AWS_GT_notes.pdf(全 42 頁)、papers/delivered/furusho_RIMS1357_mzv_gt.pdf(全 43 頁)
- 注意: 両ノートとも当該箇所に**式番号なし**(Schneps §I は式番号を一切振らない)。頁番号は PDF 印字頁(= PDF 頁番号と一致)。

### S1. Schneps: Ihara の path 解釈(p.13・式番号なし)

p.12 末尾に「**Theorem.** (Ihara) *There is an injection G_ℚ ↪ ĜT.*」があり、その 3 通りの証明スケッチの第 2 ビュレット(p.13)に逐語(画像照合済み):

> We can approach this more arithmetically by using the fact that not only does G_ℚ act on (homotopy classes of) *loops* on a variety X based at a ℚ-point, but also on (homotopy classes of) *paths* on X from one ℚ-point to another. Ihara explained that the geometric meaning of the element f_σ(x, y) is that if p denotes the path from 0 to 1 (taking tangential base points), then σ(p) = pf(x, y).

- 続き: 「the path r from 0 to 1/2」で σ(r) = rg(x, y)、Θ(z) = 1 − z、p = Θ(r)⁻¹r から無番号の連鎖式で f(x, y) = g(y, x)⁻¹g(x, y) を導き relation (I) を出す。
- **接基点の較正は皆無(本丸の回答)**: この近傍にあるのは括弧書き「(taking tangential base points)」の**語だけ**。単位接ベクトル・±∂/∂t・速度/座標の正規化は一切なし。全 42 頁 grep で「unit tangent」「tangent vector」「∂/∂t」「direction」**0 件**。ノート内で tangential base point が実質定義されるのは p.21(§II「Tangential base points」)のみで、それは M₀,n(ℝ) の maximal degeneration 点近傍の **simply connected regions を基点に使う**という定義(「these regions can be used as base points for a topological fundamental groupoid; they are called *tangential base points of maximal degeneration*」逐語)— ベクトル較正はここにもない。**どの向き・どの正規化の接基点かは本ノートからは UNKNOWN**。

### S2. Schneps: f ∈ F̂₂′(derived subgroup)の言明 — Galois 側と GT 定義側の両方

1. **Galois 側(p.2、§I.1)逐語**:

   > 1) to identify each element σ ∈ G_ℚ with a pair (χ(σ), f_σ) ∈ Ẑ* × F̂₂′.
   >
   > As for f_σ ∈ F̂₂′, which is the derived subgroup of the profinite completion of the free group F̂₂ on two generators, ...
   >
   > 2) Find necessary and sufficient conditions on f ∈ F̂₂′ for it to come from a σ ∈ G_ℚ.

2. **Galois 側の正規化の仕組み(p.4、§I.3)逐語** — f_σ ∈ F̂₂′ は**外作用の持ち上げの一意化条件**として導入される:

   > Suppose g ≡ x^δ y^ε in F̂₂^ab, and set f = y^{−ε} g x^δ. Then
   >
   > σ(x) = x^α, σ(y) = f^{−1} y^β f
   >
   > is the unique lifting of the outer action of σ such that f ∈ F̂₂′.
   >
   > We have obtained a map G_ℚ → Ẑ* × F̂₂′.

   - すなわち Schneps の提示では **f_σ の釘付けは abelianization による純群論的正規化**(接基点によるのではない)。p.13 の path 解釈は「Ihara が説明した幾何的意味」として後置され、両者の整合の較正(どの接基点でこの正規化が実現されるか)はノート内では**述べられない**。

3. **GT 定義側(p.12)逐語**:

   > **Definition.** The *Grothendieck-Teichmüller group* ĜT is the group of pairs (λ, f) ∈ Ẑ* × F̂₂′ such that x ↦ x^λ and y ↦ f^{−1}y^λ f induces an automorphism of F̂₂, and such that (I) f(x,y)f(y,x) = 1, (II) f(x,y)x^m f(z,x)z^m f(y,z)y^m = 1 where xyz = 1 and m = (λ−1)/2, (III) (5-cycle relation) ...

   - **結論: f ∈ F̂₂′ は「GT の定義条件」かつ「Galois の f_σ の正規化条件」の両方**。ĜT 定義では属域そのもの(Ẑ* × F̂₂′ の第 2 成分)、Galois 側では lift 一意化の条件(p.4)として機能。

### S3. Furusho RIMS-1357: 条件 (0) の 2 箇所と Galois 像との関係

1. **pro-代数版(Definition 2.2.1、p.12–13、[Dr]§4 引用)逐語**:

   > GT(k) = {(λ, f) ∈ k^× × F₂(k) | (λ, f) satisfies (0)∼(iii) below.}
   >
   > (0) f ∈ [F₂, F₂](k)

   - ここで F₂(下線付き)は F₂ の **Malcev completion**、k は任意の ℚ-algebra(p.12)。**GT の定義条件**であり Galois 表現の言明ではない。脚注 3(p.13): 「For our convenience, we reverse the original definition of the multiplication of GT in [Dr]」(乗法の向きが [Dr] と逆)。

2. **pro-ℓ 版(p.24 冒頭、ĜT₁^(ℓ) の定義)逐語** — 司令塔指定の「(0) f ∈ [F₂^(ℓ), F₂^(ℓ)]」はこちら:

   > Here ĜT₁^(ℓ) := { σ ∈ Aut F̂₂^(ℓ) | σ(x) = x, σ(y) = f⁻¹yf for ∃f ∈ F̂₂^(ℓ) which satisfies (0) ∼ (iii) below. }
   >
   > (0) f ∈ [F̂₂^(ℓ), F̂₂^(ℓ)]
   > (i) f(X,Y)f(Y,X) = 1
   > (ii) f(Z,X)f(Y,Z)f(X,Y) = 1 for XYZ = 1
   > (iii) (5-cycle、P̂₅^(ℓ) 内)

   - **Note 4.1.2(p.24)逐語**: 「Here [F̂₂^(ℓ), F̂₂^(ℓ)] means the topological commutator subgroup of F̂₂^(ℓ) ... Note that σ ∈ ĜT₁^(ℓ) determines f ∈ F̂₂^(ℓ) uniquely because of the condition (0).」— **(0) は f の一意化(正規化)条件**と明記。
   - これは λ = 1 の unipotent 部分(ĜT₁)なので (ii) に X^m 因子なし(m = 0)。

3. **Galois 像との関係(p.23、§4.1)**: 定義自体は GT 側だが、**Galois 像が (0)〜(iii) を満たして中に入る**ことが Lemma 4.1.1 で言明される。逐語:

   > The absolute Galois group Gal(Q̄/Q) acts on the algebraic fundamental group π₁(P¹_Q̄ − {0,1,∞}, 0⃗1) of the projective line minus 3 points, where 0⃗1 means the tangential base point (see [De]§15). ... p₁^(ℓ) : Gal(Q̄/Q(μ_{ℓ∞})) → Aut F̂₂^(ℓ) ...
   >
   > By imitating the construction of the embedding Gal(Q̄/Q) ↪ ĜT in [Ih94], we can show that its image is contained in the following pro-ℓ group version of the Grothendieck-Teichmüller group ĜT₁^(ℓ).
   >
   > **Lemma 4.1.1.** Im p₁^(ℓ) ⊆ ĜT₁^(ℓ).

   - **f が Galois 表現の像かどうかへの回答**: 条件 (0) は **ĜT₁^(ℓ) の定義条件**として書かれ、Galois 側は「Im p₁^(ℓ) ⊆ ĜT₁^(ℓ)」(Lemma 4.1.1、証明は [Ih94] の模倣と述べるのみ)経由で **f_σ ∈ [F̂₂^(ℓ), F̂₂^(ℓ)] が帰結**する構成。Galois の作用の基点は **0⃗1 = tangential base point(矢印つき記法)で明示**されるが、その較正は **[De]§15(Deligne, Le groupe fondamental de la droite projective moins trois points, §15)へ委任**— 単位接ベクトル等の正規化は本稿に書かれていない。
   - なお σ の範囲は Gal(Q̄/Q(μ_{ℓ∞}))(円分指標を消した部分群)であり、full Gal(Q̄/Q) の f_σ ではない点に注意。

### S4. (I3*) への含意(判定材料の整理)

1. σ(p) = p·f(x,y)(p = 0 から 1 への道)という**規約の向き(f が右)**は Schneps p.13 で確定(画像照合)。
2. ただし Schneps は接基点の較正(単位接ベクトル・向き)を**どこにも書かない**。較正の一次出典は Ihara [I]/Deligne [De]§15 側 — 本 2 資料は「二次資料として規約の向きを支持する」ことまで。**接基点較正の一次証拠としては使えない**。
3. f ∈ (derived subgroup) は Schneps では Galois 側の一意化(p.4)+GT 定義の属域(p.12)、Furusho では GT(k) の条件 (0)(p.13)+ĜT₁^(ℓ) の条件 (0)(p.24、一意化と明記)+Lemma 4.1.1 で Galois 像に伝播。**両資料とも「(0) = f の一意正規化条件」という役割で一貫**。
