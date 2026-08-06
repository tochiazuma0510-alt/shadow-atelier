# 【PIN-CHIR-1】BJNS 逐語確認(Prop 2 / Thm 3 / Prop 5 / Cor 6 + 記号規約)

- 発火: 裁定 685(§G.10 発火前条件【PIN-CHIR-1】の履行)
- 対象: `papers/bjns-2009-chirality-groups-maps-hypermaps.pdf`(arXiv math/0609070v1・23 頁)
- **sha256 照合**: `2b533411a76923756f5ba3af9574dcb7e527258baec3256ded321ffc4be2c64a` = トリアージ `docs/scout/bjns_retrieval_triage_v1.md` 記載値と**一致**
- **読了頁申告**: pp.3, 4, 5, 6, 7 を **150 dpi 頁画像で逐語照合**(pdftocairo レンダリング)。p.8 はレンダリングのみで未照合・本報告に不使用。pdftotext は該当箇所の頁特定のみに使用(転記には不使用)。
- 転記の格: **逐語(verbatim)**。原文は英語のまま。解釈・翻案は §D 以降に分離し、導出は「導出」と明記。

---

## A. 記号規約(逐語・出典つき)

### A.1 Mon(H) の定義(§2, p.4)

> By an *oriented hypermap* we mean a triple H = (D, R, L) where D is a set of darts and R and L are two permutations generating a permutation group Mon (H) = ⟨R, L⟩, called the *monodromy group* of H, acting transitively on D. The permutations R and L will be called the *canonical generators* of Mon (H).

(H はカリグラフィー体 ℋ。以下、hypermap は ℋ・hypermap subgroup は斜体 H と書き分ける。)

### A.2 Δ・Δ⁺・ρ・λ(§2, p.5)

> Let Δ denote the free product
>
> Δ = ⟨r₀, r₁, r₂ | r₀² = r₁² = r₂² = 1⟩
>
> and let Δ⁺ = ⟨r₁r₂, r₂r₀⟩ be its even word subgroup. The canonical generators of Δ⁺ will be denoted by ρ = r₁r₂ and λ = r₂r₀.

### A.3 hypermap subgroup H(§2, p.5)

> Thus the monodromy group of any oriented hypermap is a quotient of Δ⁺, and oriented hypermaps correspond to subgroups of Δ⁺. Any subgroup H ≤ Δ⁺ for which (Δ⁺/H, ρ̄, λ̄) ≅ ℋ will be called a *hypermap subgroup* for ℋ.

(直前文脈: μ : Δ⁺ → Mon(ℋ), ρ ↦ R, λ ↦ L なる全射があり、H はダート固定化群の μ 逆像。Lemma 1(iii), p.5: ℋ が orientably regular ⟺ hypermap subgroup が Δ⁺ の正規部分群。)

### A.4 mirror symmetry と reflexible / chiral(§2, pp.5–6)

> More precisely, a permutation ψ of D will be called a *mirror symmetry* of an oriented hypermap ℋ = (D, R, L) if ψR = R⁻¹ψ and ψL = L⁻¹ψ. An orientably regular hypermap admitting mirror symmetries is said to be *reflexible* or *regular*, [...] On the other hand, an orientably regular hypermap with no mirror symmetries will be called a *chiral* hypermap.

### A.5 H^r の定義(§2, p.6)

> Observe that conjugation by r₂ induces an automorphism of Δ⁺ inverting its generators ρ and λ. Since a hypermap subgroup H of an orientably regular hypermap ℋ is normal in Δ⁺, its conjugates in Δ are H and H^{r₀} = H^{r₁} = H^{r₂}. Let H^r denote this common conjugate H^{rᵢ}. It is straightforward to see that H^r is a hypermap subgroup of the *mirror image* ℋ^r = (D, R⁻¹, L⁻¹).

### A.6 H_Δ・H^Δ の定義と極値性(§3 前文, p.6)

> Let ℋ be an orientably regular hypermap with hypermap subgroup H, a normal subgroup of Δ⁺. Then the largest normal subgroup of Δ contained in H is the group H_Δ = H ∩ H^r, and the smallest normal subgroup of Δ containing H is the group H^Δ = HH^r. The corresponding hypermaps ℋ_Δ and ℋ^Δ are respectively the smallest reflexible hypermap that covers ℋ, and the largest reflexible hypermap that is covered by ℋ.

---

## B. 主要 4 命題(逐語)

### B.1 Proposition 2(p.6)— 4 商の同型

> **Proposition 2** The four groups H^Δ/H, H/H_Δ, H^Δ/H^r and H^r/H_Δ are all isomorphic to each other.
>
> *Proof.* The third isomorphism theorem gives
>
> H^Δ/H = HH^r/H ≅ H^r/(H ∩ H^r) = H^r/H_Δ,
>
> and similarly H^Δ/H^r ≅ H/H_Δ. Conjugation by a generator rᵢ of Δ induces isomorphisms H^Δ/H ≅ H^Δ/H^r and H/H_Δ ≅ H^r/H_Δ. □

命名(Prop 2 直後, pp.6–7・逐語):

> We will call this common group the *chirality group* X(ℋ) of ℋ, and its order the *chirality index* κ = κ(ℋ) of ℋ. Thus ℋ is reflexible if and only if κ = 1, and in general X(ℋ) and κ(ℋ) can be regarded as algebraic and numerical measures of how far ℋ deviates from being reflexible.

(改頁位置: 「Thus ℋ is reflexible if and only」まで p.6・「if κ = 1, ...」以降 p.7。)

### B.2 Theorem 3(p.7)— κ 枚被覆と被覆変換群

> **Theorem 3** Let ℋ be an orientably regular hypermap with chirality index κ. Then ℋ_Δ → ℋ and ℋ → ℋ^Δ are both κ-sheeted regular coverings with covering transformation group isomorphic to the chirality group X(ℋ). Moreover, the covering ℋ_Δ → ℋ is smooth.

(証明の要点・p.7: H_Δ ⊴ H・H ⊴ H^Δ より両被覆は regular。Prop 2 により被覆変換群 H/H_Δ と H^Δ/H は同型で X(ℋ) に一致。枚数 = 指数 |H : H_Δ| = |H^Δ : H| = |X(ℋ)| = κ。smooth 部分は r₂⁻¹ρr₂ = ρ⁻¹, r₂⁻¹λr₂ = λ⁻¹, r₂⁻¹(ρλ)r₂ = λ(ρλ)⁻¹λ⁻¹ により ρ, λ, ρλ の同じ冪が H と H^r に属すことから type 保存を導く。)

**注意(reflexible 商の言明の所在)**: 「ℋ^Δ が ℋ の被覆する最大の reflexible hypermap である」(= 商 Mon/X が reflexible)という言明自体は **Theorem 3 の文中にはない**。所在は ①§3 前文(p.6・§A.6 に逐語)②§1(p.3・下記 B.5)の双対定義文。Theorem 3 が与えるのは被覆の枚数・正則性・被覆変換群・smoothness。

### B.3 Proposition 5(p.7)— X ⊴ Mon

番号ずれ**なし**。「X ⊴ Mon(ℋ)」を与える命題は原文どおり Proposition 5(p.7)である。

> **Proposition 5** The chirality group X(ℋ) of each orientably regular hypermap ℋ is isomorphic to a normal subgroup of the monodromy group Mon (ℋ).
>
> *Proof.* X(ℋ) ≅ H^Δ/H ≤ Δ⁺/H ≅ Mon (ℋ). By Theorem 3, X is normal in Mon (ℋ). □

### B.4 Corollary 6(p.7)— κ の割り切り

橋渡し文つき逐語:

> Since the number of darts in an orientably regular hypermap coincides with the order of the monodromy group, Proposition 5 and Lagrange's Theorem now imply:
>
> **Corollary 6** The chirality index of any orientably regular hypermap divides the number of darts.

**正確な形**: 原文の主張は「κ は **ダート数 |D|** を割る」。orientably regular では |D| = |Mon(ℋ)|(橋渡し文で明示)なので κ | |Mon(ℋ)| と同値。

### B.5 参考: §1 の双対定義(p.3・C5 検査の直接根拠)

> The minimal subgroup X(ℋ) ⊴ Mon (ℋ) such that ℋ/X(ℋ) is a reflexible hypermap is called the *chirality group* of ℋ. It is straightforward that ℋ is chiral if and only if X(ℋ) is nontrivial. There is a dual approach to the definition of the chirality group, obtained by considering the smallest reflexible hypermap which covers ℋ. It is proved in Section 3 that these two approaches are equivalent.

(補足・p.3 同段落: In general, |X(ℋ)| ≤ |Mon (ℋ)|. The most extreme type of chirality arises when X(ℋ) = Mon (ℋ); such hypermaps, called totally chiral, ...)

---

## C. Cor 4(付随・p.7 逐語)

> **Corollary 4** If ℋ is an orientably regular hypermap with chirality index κ, then χ(ℋ_Δ) = κχ(ℋ).

---

## D. §G.10「実装可能形」の検証材料(照合結果・解釈は最小限で明記)

対象: `docs/notes/theorem_check_mirrorall_l3vacuous_v1.md` §G.10.1 の枠
X = ⟨⟨π(ι(r₁)), …, π(ι(r_k))⟩⟩^{P̂}(π : Γ ↠ P̂ = Γ/N̄, N̄ = ⟨⟨r₁,…,r_k⟩⟩^Γ)。

**結論: 正当化される(BJNS からの入力は B.1 の 1 点のみ・残りは初等群論の導出)**。鎖は:

1. **BJNS 由来(逐語 B.1 + A.6)**: X = H^Δ/H, H^Δ = HH^r。翻訳 H = N̄, H^r = ι(N̄) の下で X = N̄·ι(N̄)/N̄。Prop 5(B.3)の証明がこの X を Δ⁺/H ≅ Mon の**正規部分群そのもの**として実現しており、§G.10.1 の「X = N̄ι(N̄)/N̄ ⊴ Mon = Γ/N̄ = P̂」と一致。
2. **導出(第二同型定理・標準)**: N̄·ι(N̄)/N̄ = π(ι(N̄))。
3. **導出(標準)**: ι ∈ Aut(Γ) ⟹ ι(⟨⟨r₁,…,r_k⟩⟩^Γ) = ⟨⟨ι(r₁),…,ι(r_k)⟩⟩^Γ。
4. **導出(標準)**: π 全射 ⟹ π(⟨⟨S⟩⟩^Γ) = ⟨⟨π(S)⟩⟩^{P̂}。
5. 1–4 より X = ⟨⟨π(ι(r_j))⟩⟩^{P̂}。∎

**留保 2 点(移送の非逐語部分・§G.10 使用時に明記されたい)**:

- **(D-i) 台群のずれ**: BJNS の Δ⁺ は Δ = C₂∗C₂∗C₂ の偶語部分群(ρ, λ は自由生成)。§G.10.1 の「Γ = C₂∗C₃ = Δ⁺」は**逐語には不成立**(BJNS の Δ⁺ に u² = 1, w³ = 1 の関係はない)。ただし Prop 2 の証明(B.1)が使うのは「H ⊴ G・ι ∈ Aut(G)・ι² が H を保つ・H^r = ι(H)」という抽象データのみなので、Γ = C₂∗C₃ と ι(U) = U, ι(W) = W⁻¹ に対して**同一証明がそのまま通る**(導出・移送)。Prop 5 / Cor 6 の割り切り(κ = |X| が |Γ/N̄| を割る)も同様に Lagrange のみで移送可。Theorem 3 の smooth 部分だけは BJNS 固有の関係式(r₂⁻¹ρr₂ = ρ⁻¹ 等)を使うが、§G.10 はこの部分を使っていない。
- **(D-ii) ι の対応**: BJNS の鏡映は「**両方の**正準生成元を反転」(A.5: inverting its generators ρ and λ)。工房の ι(U↦U, W↦W⁻¹)は W のみ反転に見えるが、Γ = C₂∗C₃ では U⁻¹ = U なので「両生成元反転」と**一致**する。よって MIRROR-PSL 正規化と BJNS の r-共役は整合(導出)。なお工房版では H^r = ι(N̄) を「Γ⋊⟨ι⟩ 内の共役」と読み替えることになる(ι が Γ の内部自己同型でない点は BJNS の r ∈ Δ∖Δ⁺ と同型の状況)。

**§G.10 カナリア C5 の根拠づけの精密化**: 「P̂/X が reflexible(最大 reflexible 商)」の文献上の所在は **Thm 3 ではなく** §3 前文(p.6, A.6)+ §1 双対定義(p.3, B.5)。C5 の実質は正しいが引用は「BJNS §1 p.3 + §3 前文 p.6」と改めるのが正確(下の対照表 T-3)。

**§G.10.1 の「X = 1 ⟺ reflexible」**: 命名文(B.1 直後の逐語)「Thus ℋ is reflexible if and only if κ = 1」で直接支持 ✓。

**§G.10.2 の注記「u², w³ は ι で u², w⁻³ に写り Γ 内で自明」**: 工房側の導出であり BJNS には対応物なし(BJNS の Δ⁺ に u², w³ は存在しない — D-i と同根)。導出自体は Γ = C₂∗C₃ 内で正しい。

---

## E. 既存記録との対照表(食い違い・精度差のみ)

| # | 箇所 | 既存記録 | 原文(本報告) | 判定 |
|---|---|---|---|---|
| T-1 | トリアージ (i)「Corollary 6: κ(H) は \|D\|(= \|Mon(H)\|)を割る」 | κ \| \|D\| = \|Mon\| | 逐語は「divides the number of darts」。\|D\| = \|Mon\| は橋渡し文(p.7)で明示 | **実質一致**(逐語は darts・精度差のみ) |
| T-2 | トリアージ (i) Prop 2 / Thm 3 / Cor 4 / Prop 5 の要約 | §A.6/B.1–B.4 と同内容 | 同 | **一致**(番号ずれなし) |
| T-3 | §G.10.3 カナリア C5 の引用「BJNS Thm 3(最大 reflexible 商)」 | Thm 3 に帰属 | 最大 reflexible 商の言明は §3 前文 p.6 + §1 p.3(B.2 注意) | **引用番号の不正確**(実質は正・引用先を訂正されたい) |
| T-4 | §G.10.1「Γ = C₂∗C₃ = Δ⁺」 | 等号で同一視 | BJNS Δ⁺ は自由(関係なし)・逐語には別物 | **移送(非逐語)**— D-i の留保つきで証明は通る |
| T-5 | §G.10.1 の X の枠(X = N̄ι(N̄)/N̄ ⊴ Mon)・κ \| \|P̂\| | — | Prop 5 証明・Cor 6 と一致(D-i/D-ii の読み替えの下) | **一致** |

トリアージ (ii)(iii)(iv) は本任務(①–④)の範囲外につき照合せず。

---

## F. UNKNOWN 申告

- BJNS 本文に「Γ = C₂∗C₃ 型の台群への一般化」を明示する箇所があるか: pp.3–7 の照合範囲では**なし**(pp.8–23 は本任務で未照合 ⟹ UNKNOWN)。§G.10 での使用は D-i の移送として扱うのが安全。
- 上記以外の①–④該当項目に UNKNOWN なし(全 4 項目とも頁画像で逐語確認済み)。
