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
