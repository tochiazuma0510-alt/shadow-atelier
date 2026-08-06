# Brown「Depth-graded motivic multiple zeta values」式 (1.4) 逐語転記と 691 の全出現 v1

- **依頼**: 【RW-GAP-4】k=12/691 実験の解釈に直結する 1 点精読(①式 (1.4) 逐語 ②理論的文脈 ③F₆₉₁ 判断材料)。**解釈はしない — 判断材料の完全提供まで**。
- **対象 PDF**: `papers/brown-2013-1301.3053-depth-graded-motivic-mzv.pdf`(arXiv:1301.3053**v2** [math.NT] 10 Jan 2020, Francis Brown, "Depth-graded motivic multiple zeta values")
- **読了頁申告**: ページ画像照合(150dpi レンダリング)= **pp. 1, 2, 4, 21, 25**。全文テキスト走査(pdftotext)= 全 34 頁(691 / Ihara / Takao / Gangl / 5197 の全出現を grep で確認済み)。
- **表記**: 論文の σ̄(上線)= `σ̄`、σ̃(チルダ・§8.5 の canonical lift)= `σ̃`、depth-graded motivic Lie algebra = `dg^m`(論文では 𝔡𝔤^𝔪)、太字 sans の S = `S_{2n}`(even period polynomial の空間)、e₁₂ 等 = exceptional element。

---

## ① 式 (1.4) の完全な逐語転記(前後の定義込み)

### 1.1 前提定義(§1.1, p.1 — 画像照合済み)

> "Multiple zeta values are defined for integers n₁, …, n_{r−1} ≥ 1 and n_r ≥ 2 by
>
> ζ(n₁, …, n_r) = Σ_{1≤k₁<…<k_r} 1 / (k₁^{n₁} … k_r^{n_r}) .
>
> Their **weight** is the quantity n₁ + … + n_r, and their **depth** is the number of indices r."

> "Let Z_N denote the ℚ-vector space spanned by multiple zeta values in weight N."

Zagier 予想 (1.1)(p.1):

> "(1.1)  Σ_{N≥0} dim_ℚ(Z_N) s^N = 1 / (1 − s² − s³) ."

Broadhurst–Kreimer 予想 (1.2)(p.1、Z_{N,d} = weight N, depth d の MZV が張る ℚ-ベクトル空間):

> "(1.2)  Σ_{N,d≥0} dim_ℚ(Z_{N,d}) s^N t^d = (1 + 𝔼(s)t) / (1 − 𝕆(s)t + 𝕊(s)t² − 𝕊(s)t⁴) ,"

(1.3)(p.2):

> "(1.3)  𝔼(s) = s²/(1−s²) , 𝕆(s) = s³/(1−s²) , 𝕊(s) = s¹² / ((1−s⁴)(1−s⁶)) ."

### 1.2 (1.4) 直前の段落(§1.1, p.2 — 画像照合済み・逐語)

> "The series 𝔼(s) and 𝕆(s) are the generating series for the dimensions of the spaces of even and odd single zeta values respectively, and 𝕊(s) is the generating series for the dimensions of the space of cusp forms for the full modular group SL₂(ℤ). The first prediction of (1.2), due to the presence of a non-trivial coefficient of t² in the denominator of the right-hand side, is the existence of an **extra relation between double zeta values of even weight for every cusp form, modulo multiple zeta values of lower depth (single zeta values)**. These relations have indeed been shown to exist and are well-understood by the work of Gangl, Kaneko and Zagier [17], who exhibited an infinite family of such relations. The smallest one corresponds to the Ramanujan cusp form of weight 12:"

### 1.3 式 (1.4) 本体(p.2 — 画像照合済み・逐語)

> **(1.4)  28 ζ(3, 9) + 150 ζ(5, 7) + 168 ζ(7, 5) = (5197 / 691) ζ(12) .**

### 1.4 (1.4) 直後の段落(p.2 — 画像照合済み・逐語)

> "The coefficients in this and all such equations can be related to **period polynomials for cusp forms, or equivalently, to group cocycles for SL₂(ℤ)**. Furthermore, a geometric mechanism for these relations is by now fairly well understood [6]."

### 1.5 (1.4) の所属・構造(論文記載の事実のみ)

| 項目 | 内容 | 出典 |
|---|---|---|
| どの空間の関係式か | 実数の MZV(ℚ 上の線形関係)。weight 12 の空間 Z₁₂ 内の厳密な等式(近似・合同ではない) | §1.1, p.2 |
| 重み (weight) | 12(全項: 3+9 = 5+7 = 7+5 = 12) | §1.1, p.2 |
| 深さ (depth) | 左辺 = depth 2(double zeta values)、右辺 = depth 1(single zeta ζ(12))。「modulo multiple zeta values of lower depth(= single zeta values)で消える extra relation」として提示 | §1.1, p.2 |
| **691 の位置** | **右辺係数 5197/691 の分母**。左辺係数 28, 150, 168 は整数。691 は他のどの項にも現れない | §1.1, p.2(画像照合) |
| 対応 cusp form | weight 12 の Ramanujan cusp form Δ | §1.1, p.2 |
| 由来 | Gangl–Kaneko–Zagier [17] の無限族の最小例([17] = "Double zeta values and modular forms", Automorphic forms and zeta functions, 71–106, World Sci. 2006 — 論文 References p.33) | §1.1, p.2 + Refs |

---

## ② 理論的文脈(depth-graded motivic Lie algebra・Ihara–Takao・period polynomial)

### 2.1 背景: motivic Lie algebra g^m と freeness(§1.2, p.3 — テキスト照合)

- g = 𝕃(e₀, e₁)(2 生成の自由次数付き Lie 代数)、g^m := Lie G^{dR}_{MT(ℤ)} は Ihara bracket { , } 付きの (g, { , }) に埋め込まれる(p.3)。
- **Theorem 1.1** [4](p.3 逐語): "The graded Lie algebra g^m is a free Lie algebra on (some choice of) generators σ_{2n+1} in each degree −(2n+1) for n ≥ 1."
- 生成元は canonical でない(p.3 逐語): "σ₁₁ is only well-defined up to addition of rational multiples of {σ₃, {σ₅, σ₃}}"。

### 2.2 depth-graded 化と Ihara の関係式(§1.3, p.4 — 画像照合済み・逐語)

depth filtration D(e₁ の出現回数 ≥ r で減少フィルトレーション・Ihara bracket で保たれる)により dg^m = gr_D g^m。depth 1 に canonical な生成元:

> "(1.6)  σ̄_{2n+1} = (−1)ⁿ (ad e₀)^{2n} e₁ ∈ dg₁^m ."

> "**Ihara discovered, astonishingly, that in the depth-graded Lie algebra the generators σ̄_{2n+1} are not free. The first relation occurs in weight 12**
>
> **(1.7)  {σ̄₃, σ̄₉} − 3{σ̄₅, σ̄₇} = 0 .**
>
> In order to reconcile this relation with the freeness theorem 1.1, there must exist an **extra generator in dg^m in weight 12** to compensate for it. These exceptional generators are one of the main objects of study of this paper."

- (1.7) は **dg^m(weight 12, depth 2 成分)内の厳密な等式**。係数は 1, −3 で、**(1.7) 自体に 691 は現れない**。
- Ihara–Takao の出典は [22] = "Y. Ihara, N. Takao, seminar talk (May 1993)"(References p.34)。§1.3 では一般の二次関係式の既知性として "[22, 32, 19, 17]" が引かれる(p.4)。

### 2.3 period polynomial との対応(§1.3, p.4 — 画像照合済み・逐語)

> "Evaluating cocycles on the matrix (0 −1; 1 0) induces an isomorphism H¹_cusp(SL₂(ℤ), V_{2n−2})⁺ ≅ S_{2n} where + denotes invariants under real Frobenius, and S_{2n} ⊂ ℚ[X,Y] is the space of **even period polynomials**: it is the space of antisymmetric homogeneous polynomials P(X,Y) of degree 2n−2, divisible by Y, satisfying P(±X, ±Y) = P(X,Y) and
>
> P(X,Y) + P(X−Y, X) + P(−Y, X−Y) = 0 ."

> "One shows that the quadratic relations are completely described by period polynomials:
>
> (1.8)  Σ_{i<j} λ_{i,j} {σ̄_{2i+1}, σ̄_{2j+1}} = 0  ⟺  Σ_{i,j} (λ_{ij} − λ_{ji}) X^{2i} Y^{2j} ∈ S_{2n} ."

### 2.4 (1.7) の period polynomial 由来の再導出(§7.3 Example 7.2, p.21 — 画像照合済み・逐語)

完全列 (7.8): 0 → S → D₁ ∧ D₁ → D₂ → 0(D_r は多項式表現の depth r 空間・[17] による)。

> "**Example 7.2.** The smallest non-trivial period polynomial occurs in degree 10 and is given by **s₁₂ = X²Y²(X−Y)³(X+Y)³ = X⁸Y² − 3X⁶Y⁴ + 3X⁴Y⁶ − X²Y⁸**. By the exact sequence (7.8) it immediately gives rise to the equation
>
> (7.9)  3{x₁⁴, x₁⁶} = {x₁², x₁⁸} ,
>
> which, by the faithfulness of the map ρ̄ is equivalent to Ihara's formula (1.7)."

### 2.5 exceptional generator e₁₂ と Conjecture 1(§1.4, p.4 — 画像照合済み)

- 明示写像 e : H¹_cusp(SL₂(ℤ); V_{2n−2})⁺ → D⁴g(even period polynomial ごとに e₁ 次数 4 の Lie word)。**Conjecture 1** (1.9): H₁(dg^m; ℚ) ≅ ⊕_{n≥1} σ̄_{2n+1}ℚ ⊕ ⊕_n e(S_{2n})、H₂ ≅ ⊕_n S_{2n}、H_i = 0 (i ≥ 3)。
- **Theorem 1.2** (1.10)(p.4–5 テキスト照合): e : S_{2n} → ls₄ は明示的単射線形写像(ls = linearized double shuffle の解空間)。「ef が motivic(dg^m に入る)か」は open(→ Conjecture 3, §8.4)。
- weight 12, depth 4 では dim D₄ = 1 だが Lie₄(D₁) = 0(quadruple Ihara bracket 非全射の最小例、§7.4, p.21 画像照合)。

---

## ③ F₆₉₁ 係数での挙動を判断するのに必要な全情報(691 の全出現と各々の位置)

### 3.1 論文中の「691」全 3 出現(grep 全文走査で確認・すべて画像照合済み)

| # | 位置 | 式 | 691 の役割 |
|---|---|---|---|
| 1 | p.2, 式 (1.4) | 28ζ(3,9) + 150ζ(5,7) + 168ζ(7,5) = (5197/691) ζ(12) | **分母**(実 MZV の関係式の右辺係数) |
| 2 | p.25, 式 (8.8) | {σ̃₃, σ̃₉} − 3{σ̃₅, σ̃₇} = (691/144) e₁₂ mod depth ≥ 5 | **分子**(g^m 内・e₁₂ の係数) |
| 3 | p.25, Examples 8.5 中の合同式 | {σ̃₃, σ̃₉} − 3{σ̃₅, σ̃₇} ≡ 0 mod 691 | **法**(合同式の modulus) |

### 3.2 式 (8.8) とその前後(§8.4 Examples 8.5, p.25 — 画像照合済み・逐語)

> "**Examples 8.5.** The elements σ̃₃, σ̃₅, σ̃₇, σ̃₉ defined by the coefficients of ζ(3), ζ(5), ζ(7), and ζ(9) in weights 3,5,7,9 in Drinfeld's associator are canonical, and we have
>
> **(8.8)  {σ̃₃, σ̃₉} − 3{σ̃₅, σ̃₇} = (691/144) e₁₂  mod depth ≥ 5 ,**
>
> which proves that the element e₁₂ is motivic. Using the depth-parity proposition 6.4, one can show that the corresponding congruence
>
> **{σ̃₃, σ̃₉} − 3{σ̃₅, σ̃₇} ≡ 0  mod 691 ,**
>
> propagates to depth five also. Compare with the 'key example' of [20], page 258, and the ensuing discussion."

注(論文記載の事実のみ):
- (8.8) は **depth-graded でない g^m 内**の式(canonical lift σ̃ を用いる)。左辺は (1.7) の depth 2 部分では 0 になるので、(8.8) は**その depth 4 成分**が (691/144)·e₁₂ に等しい(mod depth ≥ 5)という主張。e₁₂ は depth 4・weight 12 の exceptional element。
- 「mod 691 の合同式が depth 5 にも propagate する」の根拠として depth-parity proposition 6.4 が引かれている。**合同 "≡ 0 mod 691" の正確な意味(どの ℤ 構造・どの格子上の合同か)は論文のこの箇所には明示されていない — UNKNOWN**(比較先として Ihara [20] p.258 の 'key example' が指定されているのみ)。

### 3.3 続く例(p.25 — 画像照合済み・逐語、higher weight の類似)

> "Thereafter, one checks that
>
> d(2σ₃∧σ₁₃ − 7σ₅∧σ₁₁ + 11σ₇∧σ₉) ≡ (3617/720) e₁₆ (mod 𝔞)
> d(8σ₃∧σ₁₅ − 25σ₅∧σ₁₃ + 26σ₇∧σ₁₁) ≡ (43867/9000) e₁₈ (mod 𝔞)
> d(3σ₃∧σ₁₇ − 10σ₅∧σ₁₃ + 14σ₇∧σ₁₃ − 13 f₉∧f₁₁) ≡ (174611/35280) e₂₀ (mod 𝔞)
>
> where 𝔞 = {g^m, g^m} + D⁵g^m, i.e., the previous identities hold modulo commutators and modulo terms of depth 5 or more. In this manner, I have checked that the elements ef are motivic for all f up to weight 30. … **The numerators on the right-hand side are the numerators of ζ(16)π^{−16}, ζ(18)π^{−18}, and ζ(20)π^{−20}.**"

(注意: 3 本目の "14σ₇∧σ₁₃" は画像でもそのまま(σ₁₃ が 2 回出る)。weight の勘定上は σ₇∧σ₁₁ が期待されるが、**原文は σ₁₃ — 逐語のまま記録**(v2 の原文どおり)。)

(後注・裁定 727 相互参照: 偶周期多項式の独立導出(docs/notes/weight_family_spectroscopy_design_v1.md・4e6bdcb)により正しい式は **3σ₃∧σ₁₇ − 10σ₅∧σ₁₅ + 14σ₇∧σ₁₃ − 13σ₉∧σ₁₁** と確定 — 原文の誤植は第 2 項(σ₅∧σ₁₃ → σ₅∧σ₁₅)と第 4 項(f₉∧f₁₁ → σ₉∧σ₁₁)の 2 件で、疑われた "14σ₇∧σ₁₃" 自体は正しい(7+13=20)。逐語本文は原文どおり不改変。)

### 3.4 Bernoulli 数分子・Ihara の問いとの接続(p.25 — 画像照合済み・逐語)

> "If the elements ef can be shown to be motivic, then they provide in particular an answer to the question raised by Ihara in ([20], end of §4 page 259). **The appearance of the numerators of Bernoulli numbers is related to conjecture 2 in [20]** and has been studied from the Galois-theoretic side by Sharifi [31] and McCallum and Sharifi [27]."

- [20] = Y. Ihara, "Some arithmetic aspects of Galois actions on the pro-p fundamental group of P¹∖{0,1,∞}", Proc. Symp. Pure Math. 70 (2002), 247–273。[31] = Sharifi、[27] = McCallum–Sharifi(References p.34)。

### 3.5 「分母か分子か」の整理(論文記載事実の並置 — 解釈なし)

1. **(1.4)(実 MZV, weight 12, depth 2)では 691 は分母**: 左辺(整数係数の double zeta 結合)= (5197/691)·ζ(12)。
2. **(1.7)(dg^m, depth 2)では 691 は現れない**: {σ̄₃,σ̄₉} − 3{σ̄₅,σ̄₇} = 0 は係数 1, −3 の ℚ 上の厳密な関係式。
3. **(8.8)(g^m, depth 4 成分)では 691 は分子**: 同じ結合(canonical lift 版)の depth 4 成分 = (691/144)·e₁₂ mod depth ≥ 5。これが「e₁₂ が motivic であること」の証明に使われている。
4. **合同式では 691 は法**: {σ̃₃,σ̃₉} − 3{σ̃₅,σ̃₇} ≡ 0 mod 691 が depth 5 まで propagate(prop 6.4 経由)。
5. 論文は (1.4) の 5197/691 と (8.8) の 691/144 の**直接の橋渡しを明示的には書いていない**(UNKNOWN)。書かれているのは: (1.4) 型の係数は period polynomial / SL₂(ℤ) cocycle に帰着する(p.2)、higher weight の類似式の**分子**は ζ(2k)π^{−2k} の分子 = Bernoulli 数の分子(p.25)、これが Ihara [20] conjecture 2 と関連(p.25)、という 3 点。

### 3.6 導出値(論文外・判断材料としての算術事実 — すべて「導出」と明示)

- 導出値: (1.4) の両辺に 691 を掛けると 691·(28ζ(3,9) + 150ζ(5,7) + 168ζ(7,5)) = 5197·ζ(12)(根拠 = (1.4) の逐語形)。
- 導出値: 5197 = 7·691 + 360、よって 5197 ≢ 0 (mod 691)、gcd(5197, 691) = 1(691 は素数)。
- 導出値(外部標準事実・論文は weight 12 について明示せず): ζ(12) = 691·π¹²/638512875、B₁₂ = −691/2730 — すなわち **691 は B₁₂(および ζ(12)π^{−12})の分子**。論文 p.25 が weight 16, 18, 20 で明示している規則("numerators of ζ(2k)π^{−2k}")の k=6 版に当たるが、**論文自身は (8.8) の 691 についてこの言い換えを書いていない**(直後の一般論 "The appearance of the numerators of Bernoulli numbers…" p.25 が最も近い記述)。

---

## 出典一覧(頁は PDF 印刷頁 = 論文頁、v2)

- §1.1 定義・(1.1)(1.2): p.1(画像照合)/ (1.3)(1.4) と前後段落: p.2(画像照合)
- §1.2 Theorem 1.1・(1.5): p.3(テキスト照合)
- §1.3 (1.6)(1.7)(1.8)・S_{2n} 定義・§1.4 Conjecture 1 (1.9): p.4(画像照合)
- Theorem 1.2 (1.10): pp.4–5(テキスト照合)
- §7.3 (7.7)(7.8)・Example 7.2 (7.9)・§7.4 (7.10)・dim D₄ = 1: p.21(画像照合)
- §8.4 Examples 8.5・(8.8)・mod 691 合同・weight 16/18/20 の d 計算・Bernoulli 分子と Ihara [20]: p.25(画像照合)
- References([6][17][20][22][27][31]): pp.33–34(テキスト照合)
