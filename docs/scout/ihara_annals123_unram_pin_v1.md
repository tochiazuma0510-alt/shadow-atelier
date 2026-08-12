# Ihara, Annals 123 (1986) pp.43–55 — 不分岐性 pin(UNRAM-GAP-1 対応)v1

- 出典: Y. Ihara, "Profinite braid groups, Galois representations and complex multiplications", Annals of Mathematics 123 (1986), 43–106(ヘッダ「Annals of Mathematics, 123 (1986), 43–106」p.43 で確認)。
- 素材: `papers/ihara-annals123-pp43-55/iharaannals43.JPG`〜`iharaannals55.JPG`(印刷 pp.43–55 の頁画像 13 枚)。全 13 枚を画像で直読し、標的箇所は 2 倍拡大切り出しで上付き・下付きを再照合済み。
- 記法: 𝔉 = 論文の Fraktur F(free pro-l group)。l は論文どおり(ℓ ではなく l)。引用はすべて逐語(英語原文)。状態: candidate(司令塔照合前)。

---

## Pin A【最優先・主標的】Theorem 1(i) — 不分岐性の言明(p.53 末尾)

> **Theorem 1.**(*) (i) *The Galois representation* φ_**Q**: Gal(**Q̄**/**Q**) → Φ *is unramified outside l.*

- 脚注(同頁): "(*) This was proved also by Deligne."
- 所在: §I.3(*The case r = 2*)内、p.53 最下部。言明は p.53、(ii) と証明は p.54 に続く。

## Pin B【主標的】Theorem 1(ii) — Frobenius と特殊化の両立(p.54 冒頭)

> (ii) *For each prime p ≠ l, the* Φ*-conjugacy class determined by the image under* φ_**Q** *of the Frobenius element of p is the same as that determined by the image under* φ_**F**_p *of the Frobenius automorphism of* **F̄**_p/**F**_p.

## Pin C【主標的】Theorem 1 の証明 — 本文に全文あり(p.54)

証明は pp.53–54 内で**完結**((i)(ii) 一括の証明・p.54)。逐語:

> *Proof.* As before, let K = k̄(t), and now put
>
> K_n = K(t^{1/l^n}, (1 − t)^{1/l^n})  (n = 1, 2, ...).
>
> Then K_n ⊂ M. Since the ramification indices of 0, 1, ∞ in K_n/K are exactly l^n, every finite subextension of M/K is contained in K_n^{ur} for some n, where K_n^{ur} is the maximum *unramified* pro-l extension of K_n. Therefore, M = ∪_n K_n^{ur}. Now let p ≠ l and take k = **Q**_p (the p-adic field). We shall show that the representation φ_{**Q**_p}: Gal(**Q̄**_p/**Q**_p) → Φ factors through Gal(**Q**_p^{ur}/**Q**_p), where **Q**_p^{ur} is the maximum unramified extension of **Q**_p. To show this, let 𝔛_n denote the projective plane curve over **Z** defined by the homogeneous equation X^{l^n} + Y^{l^n} = Z^{l^n}. Then K_n is the function field of 𝔛_n ⊗ **Q̄**_p. By the Grothendieck comparison theorem [10], the finite étale pro-l coverings of 𝔛_n ⊗ **Q̄**_p and of 𝔛_n ⊗ **F̄**_p are categorically equivalent, and so are the finite étale coverings of 𝔛_n ⊗ **F**_{p^d} and of 𝔛_n ⊗ W(**F**_{p^d}) for each d ≥ 1 (W(**F**_{p^d}): the ring of Witt vectors). Therefore, the finite étale pro-l coverings of 𝔛_n ⊗ **Q̄**_p are obtained from those of 𝔛_n ⊗ **Q**_p^{ur}. This implies that there exists a Galois extension M′/**Q**_p^{ur}(t) such that M′·**Q̄**_p = M and M′ ∩ **Q̄**_p = **Q**_p^{ur}. This implies that φ_{**Q**_p} factors through Gal(**Q**_p^{ur}/**Q**_p). The rest is obvious.  q.e.d.

- 外部参照は **[10] = "the Grothendieck comparison theorem"** のみ(文献番号 [10] の書誌は pp.43–55 に無い — References は論文末尾。下記「追加撮影」参照)。

## Pin D — Theorem 1 直後の Remark(p.54)

> *Remark* 1. Let **Q**(μ_{l^∞}) denote the cyclotomic extension of l-power order over **Q**, and Ω̃_l be the maximum pro-l extension of **Q**(μ_{l^∞}) unramified outside l. The above theorem, together with the fact to be shown later that Φ₁ is a pro-l group, shows that the representation φ_**Q** factors through Gal(Ω̃_l/**Q**).

> *Remark* 2. We shall see that there is more than one Φ-conjugacy class c in Φ satisfying N(c) = p. Therefore, the Φ-conjugacy class c defined as the image under φ_{**F**_p} of the Frobenius automorphism of **F̄**_p/**F**_p *cannot* be characterized alone by its property N(c) = p (see Cor. of Prop. 8 (I, §5)).

- 「Φ₁ が pro-l 群であること」は "to be shown later"(I §5 と推定・pp.43–55 の範囲外)。

---

## Pin E — 表現の定義系(§I.1–3・based/outer・基点・惰性群)

### E1. braid 群の定義(§I.1, p.49)

> (2) Brd(𝔊; x₀, x₁, ..., x_r) = { σ ∈ Aut 𝔊 | σ(x_i) ~ x_i^α (0 ≤ i ≤ r)  for some α ∈ **Z**_l^× } / Int 𝔊.

(~ は 𝔊 内共役。α は σ に依存するが i に依らない。)Brd₁(式 (3), p.49)= 上で σ(x_i) ~ x_i(norm-one-part)。𝔊 = 𝔉^(r)(free pro-l of rank r)のとき Brd^(r) と書く(式 (4), p.50)。norm 準同型 N: Brd^(r) → **Z**_l^×(式 (5), p.50)。

### E2. Galois 表現の定義(§I.2, p.51)— **outer 型**(Int 𝔉 で割った Brd への準同型・inner ambiguity つき)

> **2.** *Galois representations in pro-l braid groups.* Let k be any perfect field of characteristic ≠ l, let k̄ be its algebraic closure, and Gal(k̄/k) be the Galois group. Let Σ = (P₀, P₁, ..., P_r) (r ≥ 2) be an ordered (r + 1)-tuple of distinct k-rational points of the projective line **P**¹. Then, to these data, one can associate a (continuous) homomorphism
>
> (1) φ = φ_k^Σ: Gal(k̄/k) → Brd^(r),
>
> *determined up to inner automorphisms of* Brd^(r), in the following way.
>
> Let t be a variable over k, and K = k̄(t) be the rational function field. Regard **P**¹ as the t-line, and the points P_i (0 ≤ i ≤ r) as places of K/k̄. Denote by M the maximum pro-l extension of K unramified outside P_i (0 ≤ i ≤ r).

### E3. 惰性群と基点相当(ι)— Proposition 1(p.51)

> **Proposition 1.** *There exists an isomorphism*
>
> (2) ι: 𝔉^(r) ⥲ Gal(M/K)
>
> *satisfying the following condition: For each i (0 ≤ i ≤ r), ι(x_i) belongs to and generates the inertia group of some extension P_i^M of P_i to a place of M.*

> *Definition.* Such an isomorphism ι will be called an (x₀, x₁, ..., x_r)-*isomorphism*. Later, we restrict ourselves to the case r = 2, taking the points (0, 1, ∞) (in t-coordinates) for (P₀, P₁, P₂), and writing (x, y, z) instead of (x₀, x₁, x₂).

- p.52 Remark 1: "Once ι is fixed, P_i^M is *unique* for each P_i. This is because the normalizer of the group ⟨x_i⟩ generated by x_i in 𝔉^(r) coincides with ⟨x_i⟩ itself."

### E4. φ の構成(p.52・完全列 (4))

> To each k, Σ, and a choice of ι, we shall associate a homomorphism φ: Gal(k̄/k) → Brd^(r), as follows. Since P_i are k-rational, M/k(t) is also a Galois extension, and we have an exact sequence
>
> (4) 1 → Gal(M/K) → Gal(M/k(t)) → Gal(K/k(t)) → 1.
>
> (図: Gal(M/K) の下に ι で 𝔉^(r)・Gal(K/k(t)) の下に canon で Gal(k̄/k)。)

構成(同頁逐語の要部): "For each ρ ∈ Gal(k̄/k), choose ρ* ∈ Gal(M/k(t)) which extends ρ. Consider the automorphism g → ρ*gρ*^{−1} of Gal(M/K), and regard it as an automorphism of 𝔉^(r), via ι. Then its class modulo Int 𝔉^(r) depends only on ρ; call it φ(ρ)." — 続けて φ(ρ) ∈ Brd^(r) の検証(ρ*x_iρ*^{−1} ~ x_i^{α_i}、α_i が i に依らないこと)。ι 変更の効果(p.53): "the dependence of φ on ι is only up to inner automorphisms of Brd^(r)."

### E5. 惰性群への Kummer 指標の制限(p.52・§I.2 内 "The isomorphism T_l(**G**_m) ≅ **Z**_l associated with ι")

- κ_i: Gal(M_i/K_i) → T_l(**G**_m) は π_i(素元)に関する Kummer character、κ_i(x_i) = (ζ_n^{(i)})_{n≥1}、x_i(π_i^{1/l^n}) = ζ_n^{(i)} π_i^{1/l^n}。"κ_i(x_i) is *independent* of i."(p.52 逐語)
- "Let κ_{ij}: Gal(M/K) → T_l(**G**_m) be the 'global' Kummer character with respect to π_{ij}. Then the restriction of κ_{ij} to the inertia group Gal(M_k/K_k) (0 ≤ k ≤ r) is given by κ_i (if k = i), κ_j^{−1} (if k = j), 1 (otherwise)."(p.52 逐語)

### E6. cyclotomic character との両立(p.53)

> **Proposition 2.** *The composite* N∘φ: Gal(k̄/k) → Brd^(r) → **Z**_l^× *is the l-cyclotomic character.*

(証明 p.53 に全文: ρ_i x_i ρ_i^{−1} = x_i^α、κ_{ij} を両辺に適用し κ_i(x_i)^{χ(ρ)} = κ_i(x_i)^α、α = χ(ρ)。)直後:

> **Corollary.** *The norm homomorphism* N: Brd^(r) → **Z**_l^× *is surjective.*(k = **Q** の l-cyclotomic character 全射性より)

### E7. r = 2 の設定(§I.3, p.53)

> **3.** *The case r = 2.* ... 𝔉 = 𝔉^(2) denotes the free pro-l group of rank 2 generated by x, y; put z = (xy)^{−1}, and
>
> (1) Φ = Brd^(2) = Brd(𝔉; x, y, z).
>
> We have an exact sequence
>
> (2) 1 → Φ₁ → Φ →^N **Z**_l^× → 1,
>
> where Φ₁ = Ker(N). Since any 3 distinct k-rational points of **P**¹ can be mapped to 0, 1, ∞ by an element of PGL₂(k), we may choose P₀ = 0, P₁ = 1, P₂ = ∞, and write φ_k = φ_k^{(0,1,∞)}. It is clear that if k′ ⊃ k, then φ_{k′} is obtained from φ_k as the composite:
>
> Gal(k̄′/k′) →_{canon} Gal(k̄/k̄ ∩ k′) ↪ Gal(k̄/k) →^{φ_k} Φ.
>
> So, the only basic cases are those of k = **Q** or k = **F**_p (p: a prime ≠ l).

### E8. 序文側の同内容(0-3 *Connections*, p.46)— 塔としての言い換え+基点

> 0-3. *Connections.* Consider the tower of all pro-l étale coverings of **P**_**Q**¹ \ {0, 1, ∞}. The total Galois group of this tower can be identified with 𝔉, via an isomorphism ι, in such a way that x, y and z generate inertia groups above 0, 1 and ∞ respectively. Fix a "coordinate isomorphism" ι. Then this determines a basis (ζ_n)_{n≥1} of T_l(**G**_m) (I, §2). On the other hand, each element ρ of the absolute Galois group G_**Q** determines an element φ_**Q**(ρ) of Aut 𝔉/Int 𝔉 (conjugation by an extension of ρ). It is easy to see that φ_**Q**(ρ) belongs to the group Φ, and α = χ(ρ). We thus obtain a Galois representation
>
> (6) φ_**Q**: G_**Q** → Φ.

### E9. inner ambiguity の解消 = Belyi lift / Deligne tangential base point(p.47)

> Fortunately, the ambiguity of φ_**Q**(ρ) mod Int 𝔉, which could be quite troublesome in any substantial study of φ_**Q**, can reasonably be eliminated. In fact, fix an ordering of the 3 points 0, 1, ∞. Then for each ι, there is a certain group theoretic way to lift φ_**Q** to a representation φ_**Q***: G_**Q** → Aut 𝔉 (Belyi's normalization I, §4). Deligne, on the other hand, considered a "tangential base point" for π₁(**P**¹ \ {0, 1, ∞}):
>
> (図: ∞ → 0 の点 x から 1 への矢印 "x⟶x, ∞ 1")
>
> (cf. [7]), and has kindly informed the author that this is equivalent to considering the class of Belyi's liftings for all ι.

- Belyi 側の本体は §I.4(p.54 下部〜): "**4.** *Belyi's representative* Φ* ⊂ Aut 𝔉 *and the associated extension* M*/k(t)." — Φ* = { σ ∈ Aut 𝔉 | σx ~ x^α, σy ≈ y^α, σz = z^α, with some α ∈ **Z**_l^× }(≈ は 𝔉′ = [𝔉,𝔉] の元による共役・p.54 逐語)。p.55 **Proposition 3 (Belyi)**: "*The canonical homomorphism* Aut 𝔉 → Aut 𝔉/Int 𝔉 *induces an isomorphism* Φ* ⥲ Φ."(証明 p.55 に全文・centralizer of x (resp. y, z) in 𝔉 is ⟨x⟩ 等)

---

## Pin F【副標的】pro-l 塔・体 Ω̃_l(≒ ICM pin の ℚ^(ℓ) 相当)の定義箇所

1. **p.54 Remark 1**(Pin D に逐語)— Ω̃_l := **Q**(μ_{l^∞}) の maximum pro-l extension unramified outside l。φ_**Q** は Gal(Ω̃_l/**Q**) を factor through(Φ₁ pro-l の事実は "later")。**番号なし(Remark 1 of §I.3 Theorem 1 直後)**。
2. p.47–48(0-5 *Open questions* (i)): "The kernel of the homomorphism F: G_{**Q**(μ_{l^∞})} → 𝒜^× corresponds to the Galois extension of **Q**(μ_{l^∞}) obtained by the adjunction of l-power division points of J_n for all n ≥ 1. It is contained in Ω_l^−, the odd part of the maximal abelian pro-l extension Ω_l/**Q**(μ_l∞) unramified outside l. Do they coincide? Are there connections with Iwasawa theory?"
3. p.48(0-5 (iii)): "What are the kernel and the image of φ_**Q**? The author only knows that the kernel corresponds to *some* pro-l extension of **Q**(μ_{l^∞}) unramified outside l (is it maximal?), and that the image of φ_**Q** is contained in the centralizer of the symmetric group 𝔖₃ in Aut 𝔉/Int 𝔉. In [2], Belyi proved that the *profinite* analogue of φ_**Q** is *injective*."

---

## UNRAM-GAP-1 との対応表(判定は司令塔・ここは所在の報告のみ)

標的の正確な形 = 「specialization 同型が G_{**Q**_p}-同変で、特殊側で I_p-作用自明」に対し、pp.43–55 にあるもの:

| 成分 | 本文の対応物 | 所在 |
|---|---|---|
| I_p-作用自明(l の外不分岐) | Theorem 1(i) 逐語 + 証明中の "φ_{**Q**_p} factors through Gal(**Q**_p^{ur}/**Q**_p)" | p.53(言明)・p.54(証明) |
| specialization 同型 | "By the Grothendieck comparison theorem [10], the finite étale pro-l coverings of 𝔛_n ⊗ **Q̄**_p and of 𝔛_n ⊗ **F̄**_p are categorically equivalent"(圏同値の形。𝔛_n ⊗ **F**_{p^d} と 𝔛_n ⊗ W(**F**_{p^d}) の版も併記) | p.54 |
| G_{**Q**_p}-同変性 | **その語では明文化されていない**。代替: M′/**Q**_p^{ur}(t) with M′·**Q̄**_p = M, M′ ∩ **Q̄**_p = **Q**_p^{ur} の存在(descent の形)+ Theorem 1(ii)(Frobenius 共役類の一致 = 同変性の Frobenius 成分) | p.54 |

- 注意: 「G_{**Q**_p}-同変な specialization 同型」という単一言明は pp.43–55 に**逐語では存在しない**(UNKNOWN: 論文の他ページ・他文献にあるかは本素材からは不明)。本文が与えるのは (a) 圏同値([10] 参照)・(b) M′ の存在による不分岐性・(c) (ii) の Frobenius 一致、の 3 点分解。

## 証明の所在まとめ・外部依存

- **Theorem 1(i)(ii) の証明は pp.53–54 で完結**(上記 Pin C 全文)。撮影範囲内で欠けはない。
- 外部依存:
  1. **[10]**(Grothendieck comparison theorem)— 書誌は論文末尾 References(pp.43–55 に無し)。SGA 1 と推定されるが**素材からは UNKNOWN**。
  2. **Φ₁ が pro-l 群**(Remark 1 が使用)— "to be shown later"、Remark 2 の参照様式 (I, §5) から **I §5** と推定(範囲外)。
  3. Belyi's normalization **I §4** は p.54 下部から始まり p.55 で Prop 3・Prop 4 途中まで入っている(続きは p.56 以降)。
  4. 0-1/0-2 の Theorem A(p.43 式 (1)_A, (2))・Theorem B(p.44 式 (1)_B, (ii)_B, (iii)_B)・Theorem C(p.45 式 (4))・Φ, Ψ の定義(p.46 式 (5))・cocycle 定義(p.47 式 (7))も撮影範囲に含まれる(本 pin の主題外につき番号のみ記録)。

## 追加撮影の要否

**主標的(Theorem 1 の言明+証明)については追加撮影不要**。以下は補助目的で有用(優先順):

1. **References の該当頁**(論文末尾・おそらく pp.104–106 のうち [10] と [2],[7] が載る頁)— [10] の正体確定用。→ **p.106 は入手・下記 Addendum で [10] 確定**(2026-08-12)。残るは [1]〜[7] の載る前頁(p.105)。
2. **I §5**(pp.56 以降・§4 の続きから)— Φ₁ が pro-l 群である証明(Remark 1 の依存)と Cor. of Prop. 8(Remark 2 の参照先)。目安 pp.56–62 程度(正確な頁は UNKNOWN)。
3. p.55 の続き(p.56–)— §I.4 Belyi normalization の残り(Prop 4 証明の続き)。

---

## Addendum(2026-08-12・裁定 933)— References 頁 p.106 の照合

- 素材追加: `papers/ihara-annals123-pp43-55/iharaannals106.JPG`(References 頁・印刷 p.106)。画像直読+2 倍/4 倍拡大切り出しで照合済み。
- **頁の全体像**: p.106 には References の **[8]〜[27]** と末尾の "(Received January 4, 1985)" が載る([1]〜[7] は前頁・本素材に無し)。

### Ad-1. [10] の書誌(逐語・p.106)

> [10] A. Grothendieck, *Eléments de géométrie algébriques IV* (4ᵉ partie) (with Dieudonné), Publ. IHES **32** (1967).

- 正体: **EGA IV 第 4 部**(Publications mathématiques de l'IHÉS, tome 32, 1967)。上記「証明の所在まとめ・外部依存 1」の「SGA 1 と推定されるが UNKNOWN」は本 Addendum で**解消 — SGA 1 ではなく EGA IV(4ᵉ partie)**。
- 表記注(画像 4 倍拡大で照合): 題は印刷どおり "algébriques"(語尾 s あり・イタリック)。"4ᵉ" の e は上付き。巻号 32 は太字。冒頭の E にアクセント記号は視認されない("Eléments")。

### Ad-2. 本 pin 文書に現れる他の参照番号 — [2](Belyi・p.48 引用文中)・[7](Deligne tangential base point・p.47 "cf. [7]")

- いずれも **p.106 には無い**(本頁は [8] から始まる)。書誌は本素材からは **UNKNOWN** のまま(前頁 p.105 に載ると推定)。

### Ad-3. Deligne の文献(p.53 脚注 "This was proved also by Deligne" 対応)

- p.106 の [8]〜[27] に **Deligne 名義の項目は無い**(著者アルファベット順で D は [1]〜[7] 域)。該当書誌の有無・内容は本素材からは **UNKNOWN**。
