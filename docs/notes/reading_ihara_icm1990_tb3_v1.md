# 精密読解ノート: Ihara「Braids, Galois Groups, and Some Arithmetic Functions」(ICM Kyoto 1990) — TB3 pin 用抽出

- **状態: candidate**(司令塔照合前)
- 作成: 2026-08-05(精密読解係)/ 委嘱: 文献要請 14(TB3 の 3 条項)・正本 `docs/notes/framework_promotion_campaign_v1.md` §6.7
- 出典 PDF: `papers/ihara-ICM1990-vol1-braids-galois-arithmetic.ocr.pdf`(ICM 1990 Proceedings 第 1 巻・856 頁)
- **頁対応(本ノートで確定): PDF 頁 = 印字頁 + 88**(印字 99 = PDF 187 で照合。以下すべて「印字頁 (PDF 頁)」併記)
- 照合方法: 全引用は pdftocairo 150–400 dpi の頁画像で原文照合済み(OCR テキストは補助のみ)。逐語引用の言語は原文(英語)のまま。

---

## 0. 前提文脈(§2.1–2.2 — 3 条項の土台)

### 0.1 π̂₁ の定義と étale 比較(印字 103 = PDF 191)

π̂₁(X(ℂ); a, b) は位相的 π₁ の完備化として定義され、有限被覆のファイバー全単射の整合系と同一視される(頁中央の表示式):

> π̂₁(X(ℂ); a, b) ≈ { compatible systems of fiber bijections p̂_f : f⁻¹(a) ≅ f⁻¹(b) }_f

その直後に代数化(一般化 Riemann 存在定理)と G_ℚ 作用の定義:

> "Since all finite coverings of X(ℂ) are algebraic and defined over ℚ̄ (the generalized Riemann existence theorem), we may assume that f runs over all finite etale coverings of X ⊗ ℚ̄. If a, b ∈ X(ℚ), each σ ∈ G_ℚ induces the fiber bijections f⁻¹(a) ≅ (σf)⁻¹(a), f⁻¹(b) ≅ (σf)⁻¹(b); hence σ acts on π̂₁(X(ℂ); a, b) by {p̂_f} ⟶ {σ ∘ p̂_{σ⁻¹f} ∘ σ⁻¹}." — 印字 103 (PDF 191)

注: Ihara の記法 π̂₁(X(ℂ); a, b) が(この整合系記述を介して)π₁^ét(X_ℚ̄; a, b) に当たる。「étale fundamental group」という語自体は §2.3 周辺には現れない(比較はこの p.103 の全単射+GRET が担う)。

### 0.2 φ_X と X₄ の設定(印字 104 = PDF 192)

- χ の定義: "Call χ(σ) = lim← χ(σ)_N ∈ Ẑ×. Then χ is a (continuous) homomorphism χ : G_ℚ → Ẑ× (2.1.3), called the cyclotomic character." — 印字 104 (PDF 192)
- §2.2: φ_{X,b} : G_ℚ → Aut π̂₁(X(ℂ), b)、φ_X : G_ℚ → Out π̂₁(X(ℂ))。
- X_n の定義と P₄ ≃ F₂ (free, rank 2)、P₅ ≃ F₂ ⋉ F₃。
- > "Now let X = X₄ = ℙ¹ − {0, 1, ∞}, so that π₁(X(ℂ)) ≃ F₂. As reviewed in §1, Belyi proved that φ_X is then injective." — 印字 104 (PDF 192)

---

## 1. 条項 (a): π₁^ét(ℙ¹−{0,1,∞}) ≅ F̂₂ に当たる言明

### 1.1 「This group is free on x, y」の正確な文と位置

§2.3 の続き、**印字 106 (PDF 194) 第 1 段落末尾**:

> "interval (0,1). Call it p. The second group contains a small positive loop around 0, called x, and y = p⁻¹ ∘ x′ ∘ p, where x′ is the transform of x by t → 1 − t (t = t₀₁). **This group is free on x, y.**" — 印字 106 (PDF 194)

「This group」= 前頁末(印字 105 = PDF 193 最終文)で導入された π₁(X(ℂ), 0⃗1)(「The second group」)を指す。原文の基点記号は 01 の上に右向き矢印(以下 0⃗1 と転記)。

### 1.2 profinite 版の同一視 F̂₂

(2.3.2) の直前、**印字 106 (PDF 194)**:

> "Then σ acts on the generators of π̂₁(X(ℂ), 0⃗1) = F̂₂ as" — 印字 106 (PDF 194)

また §2.3 冒頭(印字 105 = PDF 193)で F₂ と F̂₂′ を宣言:

> "**2.3** Let X = ℙ¹ − {0, 1, ∞}, and F₂ be the free group of rank 2 on two letters x, y. Our first goal is to show that for each σ ∈ G_ℚ, φ_X(σ) is determined by two "coordinates", χ(σ) and f_σ, where χ : G_ℚ → Ẑ× is the cyclotomic character and f_σ is an element of F̂₂′ = (F̂₂, F̂₂), the commutator subgroup of F̂₂." — 印字 105 (PDF 193)

(補助: §6.1 でも再掲 — "Let X = ℙ¹ − {0,1,∞} and, as in §2.3, identify the fundamental group π₁(X(ℂ), 0⃗1) with the free group F₂ on x, y." — 印字 114 (PDF 202)。)

---

## 2. 条項 (b): x, y の慣性生成元としての構成

**印字 105 (PDF 193) 最終段落 → 印字 106 (PDF 194) 第 1 段落**(逐語・通し):

> "Now we consider π₁(X(ℂ); 0⃗1, 1⃗0), π₁(X(ℂ), 0⃗1) and the Galois action on their completions. The first set contains an obvious element defined from the interval (0,1). Call it p. The second group contains a small positive loop around 0, called x, and y = p⁻¹ ∘ x′ ∘ p, where x′ is the transform of x by t → 1 − t (t = t₀₁). This group is free on x, y." — 印字 105–106 (PDF 193–194)

要素の定義まとめ:
- **p** = 開区間 (0,1) が定める道類 ∈ π₁(X(ℂ); 0⃗1, 1⃗0)(接基点 0⃗1 から 1⃗0 への「自明な」道)。
- **x** = 0 の周りの小さい正の向きのループ("a small positive loop around 0")∈ π₁(X(ℂ), 0⃗1)。
- **x′** = x の t → 1−t(t = t₀₁)による移送(= 1 の周りの小正ループ、基点 1⃗0)。
- **y** = p⁻¹ ∘ x′ ∘ p ∈ π₁(X(ℂ), 0⃗1)。
- 印字 106 (PDF 194) には x(0 の周りの円)と y(0 から 1 へ行き 1 を回って戻る)の**挿絵**あり。

注意(翻訳事項): Ihara は「inertia(慣性)」の語をこの箇所で使わない。x, y が尖点 0, 1 の慣性部分群の生成元であることは、この幾何的構成(小正ループ+接基点)からの標準的読み替えであり、本論文には明文がない。TB3 の条項が文字通り「inertia generator」を要求するなら、この一語分の翻訳は工房側で補う(内容は同一)。

---

## 3. 条項 (c・本命): 接基点の固定 — B・Puiseux branch・positive real root・[De]

### 3.1 方針宣言と Deligne への言及(逐語)

**印字 105 (PDF 193)**、§2.3 第 1 段落末:

> "This can also be done relying more on group-theoretic normalization as in [B₁], [Ih₁], but we proceed more "conceptually" using **Deligne's tangential base points [De]**." — 印字 105 (PDF 193)

### 3.2 B(6 本の矢印)の定義(逐語)

**印字 105 (PDF 193)** 第 2 段落:

> "Let 𝔹 be the set of "arrows" i⃗j with i, j ∈ {0, 1, ∞}, i ≠ j. Thus, 𝔹 has six elements and the symmetric group S₃ acts simply transitively on 𝔹. **For a, b ∈ 𝔹, Deligne defines π₁ = π₁(X(ℂ); a, b) and the G_ℚ-action on its profinite completion.** Topologically, it is clear what π₁ should mean when, in general, a, b are *simply connected subspaces* of X(ℂ). The base point i⃗j plays the same role as the open interval I_ij on ℝ bounded by i, j *and* not containing the third point k from {0, 1, ∞}." — 印字 105 (PDF 193)

### 3.3 branch の代数的定義(Puiseux 級数環への局所埋め込み・逐語)

**印字 105 (PDF 193)** 同段落続き:

> "For a finite etale covering Y → X over ℚ̄, the fiber above i⃗j consists of points P ∈ Ȳ(ℚ̄) above i given together with a "topological branch" (i.e., a lifting of I_ij) at each P. Here f̄ : Ȳ → ℙ¹ is the compactification of f. In order to define the G_ℚ-action on π̂₁(X(ℂ); a, b) for a, b ∈ 𝔹, it suffices to give an *algebraic* interpretation of the branches at P. One way to put it is as follows. (This device proved to be useful [A–I₁].) Let t_ij be the linear fractional function ℙ¹ → ℙ¹ which maps i, j, k to 0, 1, ∞, respectively. Then a branch at P is a local embedding of the local ring of Ȳ at P into the ring of *Puiseux series* in t_ij which extends: (i) the obvious embedding of the local ring of ℙ¹ at i into the ring of power series in t_ij, and (ii) the residue field embedding determined by the geometric point P." — 印字 105 (PDF 193)

### 3.4 「positive real root」原理と G_ℚ 作用(逐語)

同段落続き、**印字 105 (PDF 193)**:

> "The corresponding topological branch is obtained by the principle to choose **"the positive real root for t_ij^{1/e}, on I_ij"**. The group G_ℚ acts on the fibers above i⃗j via its action on the Puiseux coefficients ∈ ℚ̄. One may prefer to reinterpret this in terms of the normalization of the fiber product of f̄ with Spec ℂ[t_ij^{1/e}] (e: the ramification index)." — 印字 105 (PDF 193)

(注: 最後の文の f̄ は画像上 f とも読み得る字形。UNKNOWN(f か f̄ か)— 内容には影響しない。)

### 3.5 (2.3.1)(2.3.2) — 逐語転記(400 dpi 画像照合済み)

**印字 106 (PDF 194)**:

> "Now for each σ ∈ G_ℚ, put
>
> f_σ = p⁻¹ ∘ σ(p) ∈ π̂₁(X(ℂ), 0⃗1) .   (2.3.1)
>
> Then σ acts on the generators of π̂₁(X(ℂ), 0⃗1) = F̂₂ as
>
> x ⟶ x^{χ(σ)},  y ⟶ f_σ⁻¹ · y^{χ(σ)} · f_σ .   (2.3.2)
>
> It follows easily that f_σ ∈ F̂₂′, and that (2.3.2) with this requirement characterizes f_σ. When σ is the complex conjugation, χ(σ) = −1, f_σ = 1." — 印字 106 (PDF 194)

### 3.6 z = (xy)⁻¹ の Remark(g_σ の式込み・逐語)

**印字 106 (PDF 194)**:

> "*Remark.* By (3.1.1)(I),(II) below, it follows also that z = (xy)⁻¹ (a loop around ∞) is mapped to g_σ⁻¹ z^{χ(σ)} g_σ, where **g_σ = f_σ(x, z) x^{½(1−χ(σ))}**." — 印字 106 (PDF 194)

直後に f(x,y) 記法の規約:

> "Although F̂₂ contains much more than the free words on x, y, we shall express an element of this group conveniently as f(x, y), because it will then make sense to speak of f(ξ, η) for any elements ξ, η ∈ G of any profinite group G; the image of f under the unique homomorphism F̂₂ → G mapping x, y to ξ, η respectively." — 印字 106 (PDF 194)

---

## 4. 付随事項

### 4.1 §3.1 (3.1.1) の (I)(II)(III)(hexagon 祖形)

**印字 106 (PDF 194)** 下段、§3「The Galois Action (Profinite)」:

> "**3.1** So what is the image of the mapping G_ℚ → Ẑ× × F̂₂′ defined by σ ↦ (χ(σ), f_σ)? The known equations satisfied by λ = χ(σ), f = f_σ are as follows.
>
> (I)  f(x, y) f(y, x) = 1;
>
> (II)  f(z, x) z^m f(y, z) y^m f(x, y) x^m = 1,  if xyz = 1, m = ½(λ−1);   (3.1.1)
>
> (III) (Drinfeld) Let P₅ = π₁(X₅(ℂ), 𝓑₅) and x_ij ∈ P₅ (1 ≤ i, j ≤ 5) be as defined below. Then in P̂₅,
>
> f(x₁₂, x₂₃) f(x₃₄, x₄₅) f(x₅₁, x₁₂) f(x₂₃, x₃₄) f(x₄₅, x₅₁) = 1 ." — 印字 106 (PDF 194)

- **裁定 478 のスクショ(`papers/ihara-ICM1990-p_galois_action_3_1_1.jpg`)との同一性: 確認済み** — 同 jpg は印字 106 (PDF 194) の §3 見出し〜(III)〜Remark 冒頭の切り抜きで、本頁と字句同一。
- 直後の Remark(印字 106→107): "Drinfeld's formula given in [Dr₂] is in terms of *plane* braid group on 4 strings and is non-cyclic. The above formula is equivalent to his. The author previously wrote down more complicated formulas as 4 transposition relations (w.r.t. (1 2),(2 3),(3 4),(4 5) in S₅ instead of (12345)) in [Ih₆]." — 印字 106–107 (PDF 194–195)

### 4.2 §3.2 証明スケッチ(参考・印字 107 = PDF 195)

> "**3.2** *Sketch of proof of (3.1.1).* (I) Apply the automorphism θ : t → 1 − t to both sides of (2.3.1).
> (II) Let r be the element of π₁(X(ℂ); 1⃗0, 1⃗∞) corresponding to the rotation of argument π at the point 1: […] Then it is easy to see that r⁻¹ · σ(r) = θ(x)^{½(χ(σ)−1)} ∈ π̂₁(X(ℂ), 1⃗0). Therefore, if q = r ∘ p, we have σ(q) = q y^{½(χ(σ)−1)} f_σ(x, y). Let ω be the automorphism t → (1 − t)⁻¹ of X. Then ω²(q) ω(q) q = 1. Apply σ on this to obtain (II)." — 印字 107 (PDF 195)

𝓑_n と x_ij の定義(hexagon/pentagon の舞台)も同頁: "The definitions of 𝓑_n and x_ij. Let 𝓑̃_n be the space of all n-tuples (b₁,…,b_n) of distinct points of ℝ∪(∞) satisfying the condition: b_{i+1} is next to b_i in the positive direction for all i (1 ≤ i ≤ n−1) including the case of passing through ∞. Then PGL₂⁺(ℝ) […] acts on 𝓑̃_n diagonally, and the quotient space 𝓑_n = 𝓑̃_n / PGL₂⁺(ℝ) is naturally embedded into X_n(ℂ). The space 𝓑_n is simply connected and hence it makes sense to speak of the fundamental group P_n = π₁(X_n(ℂ), 𝓑_n)." — 印字 107 (PDF 195)

### 4.3 基点規約差の脚注 — **所在訂正: 印字 107 ではなく印字 114 (PDF 202)**

委嘱文は「印字 p.107 付近の脚注」としたが、当該脚注は **§6.1 内・印字 114 (PDF 202) の脚注 1**([Ih₂]; cf. also [A-I₂ §2] に付く)。400 dpi 画像照合済みの逐語:

> "¹ In these papers, the base point is **∞⃗1** and x, y are loops around 0, 1, respectively. So, the definitions are slightly different. See *Remark* at the end of §6.5." — 印字 114 (PDF 202) 脚注 1

- 基点記号は **∞⃗1**(∞1 の上に右向き矢印)であって 0⃗1 ではない(OCR テキストは「ööl」と劣化していたが 400 dpi で確定)。
- 意味: Ihara 自身の旧論文 [Ih₂][A-I₂] では基点が ∞⃗1 で x, y は 0, 1 の周りのループ — 本 ICM 講演(基点 0⃗1)と規約が微妙に異なる、という文献間規約差の注意。TB3 で他文献(とくに Ihara 系旧論文)の式を接続する際はこの脚注が規約差の一次典拠になる。

---

## 5. 判定

### 5.1 TB3 の 3 条項の供給可否: **供給する(3/3)** — ただし翻訳注 2 点

| 条項 | 供給 | pin |
|---|---|---|
| (a) π₁^ét(ℙ¹−{0,1,∞}) ≅ F̂₂ | ○ | 「This group is free on x, y.」印字 106 (PDF 194) + 「π̂₁(X(ℂ), 0⃗1) = F̂₂」同頁 (2.3.2) 直前 + π̂₁ の étale 記述(整合系+GRET)印字 103 (PDF 191) |
| (b) x, y の慣性生成元構成 | ○ | p・x・x′・y = p⁻¹∘x′∘p の定義文、印字 105–106 (PDF 193–194) |
| (c) 接基点の固定 | ○ | 𝔹(6 矢印)・Puiseux branch の代数的定義・positive real root 原理・[De] 言及、すべて印字 105 (PDF 193)。(2.3.1)(2.3.2) と z の Remark は印字 106 (PDF 194) |

翻訳注(不足ではなく読み替え):
1. **π̂₁ ↔ π₁^ét の辞書**: Ihara は「étale fundamental group」の名を使わず、π̂₁(X(ℂ); a, b) を有限 étale 被覆のファイバー全単射整合系として与える(印字 103)。これは π₁^ét の fiber-functor 記述そのものであり同一視は無害だが、TB3 の条文を π₁^ét の記法で書くなら一行の辞書を添える。
2. **「inertia」の語**: 本論文は x を「0 の周りの小正ループ」としか呼ばない(§2 に「inertia」の語なし)。尖点 0, 1 における慣性部分群の生成元という表現は標準的読み替えで補う。

### 5.2 Deligne 接基点(0⃗1 = 接ベクトル)と Ihara の Puiseux branch 構成の関係

同一視してよい — ただし「同じ対象の二つの提示」であることを一行で明示するのが安全。Ihara 自身が本構成を Deligne の tangential base point の実装として提示しており(「we proceed more "conceptually" using Deligne's tangential base points [De]」「For a, b ∈ 𝔹, Deligne defines π₁ = π₁(X(ℂ); a, b) and the G_ℚ-action…」、いずれも印字 105)、帰属は論文内で完結している。内容上も、Deligne 流の 0⃗1(0 における 1 方向の単位接ベクトルが定める fiber functor)と Ihara 流の 0⃗1(区間 I₀₁ と「t₀₁^{1/e} の正の実根を I₀₁ 上で選ぶ」Puiseux branch)は、同じデータ — 局所径数 t の e 乗根の整合的な選択 = 接方向 +∂/∂t に沿う「近傍点」— を指定しており、fiber functor として自然同型。したがって TB3 の条文で「Deligne [De] の接基点(Ihara [Ih ICM] §2.3 の Puiseux branch による明示化)」と併記すれば翻訳は不要。唯一の注意は規約面: (i) t_ij は i,j,k ↦ 0,1,∞ を送る一次分数変換で、0⃗1 では t₀₁ = t(恒等)なので齟齬なし; (ii) Ihara 系の**旧**論文([Ih₂][A-I₂])は基点 ∞⃗1 で定義が微妙に異なる(§4.3 の脚注・印字 114)ため、ICM 版以外から式を輸入する際はこの脚注経由で規約を合わせること。

---

## 6. 照合記録

- 頁対応確定: pdftotext 頁走査(PDF 187 頭 = タイトル頁 = 印字 99)。
- 画像照合: PDF 191–197, 202 を 150 dpi で全読、(2.3.1)(2.3.2)・Remark(g_σ)・§2.3 branch 段落・脚注 1 は 300–400 dpi で拡大再照合。
- OCR 劣化の訂正例: 脚注の「ööl」→ 正しくは ∞⃗1(400 dpi で確定)。
- UNKNOWN: §3.4(3.4 節)の "the fiber product of f" の f が f̄(コンパクト化)か f かは字形上判別不能(内容に影響なし)。それ以外の転記に UNKNOWN なし。
