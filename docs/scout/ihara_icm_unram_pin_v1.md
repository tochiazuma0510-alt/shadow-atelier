# Ihara ICM Kyoto 1990 — 「unramified outside l」逐語 pin 集

- **状態**: candidate(reader 抽出・司令塔未照合)
- **任務**: 裁定 902・K9-LIT-1 内製先行(K9-UNRAM の文献根拠 — 「L_{9,Aff} が 3 の外で不分岐」の古典的根拠候補)
- **出典**: Y. Ihara, "Braids, Galois Groups, and Some Arithmetic Functions", Proceedings of the ICM, Kyoto, Japan, 1990, 印刷 pp. 99–120。
- **在庫 PDF**: `papers/ihara-ICM1990-vol1-braids-galois-arithmetic.ocr.pdf`(全集 Vol.1・856 ページ)。**ページ対応: 印刷ページ = PDF ページ − 88**(例: 印刷 p.112 = PDF p.200)。
- **照合方法**: pdftotext 全文(印刷 pp.99–120)+ 主要 8 ページを 150dpi 画像で原文照合(PDF 190, 199, 200, 202, 203, 205, 206, 207, 208 = 印刷 102, 111, 112, 114, 115, 117, 118, 119, 120)。
- **規律**: 以下はすべて逐語引用(引用格)。解釈・「よって不分岐が言える」等の判定は書かない(司令塔・数学者・Sol の裁定事項)。記法は原文どおり(素数は l 表記・ℓ ではない)。

---

## Pin 1(主目標・最重要): §5.2 — Q^(l)(∞) は Q(μ_{l∞}) 上 pro-l かつ l の外で不分岐

**§5.2, 印刷 p.111(PDF 199)** — 塔の定義(画像照合済):

> **5.2** For each prime number l, there is a canonical sequence
>
> Q ⊆ Q^(l)(1) ⊆ ··· ⊆ Q^(l)(m) ⊆ ··· ⊆ Q^(l)(∞) = ∪ Q^(l)(m)   (5.2.1)
>
> of (infinite) Galois extensions over Q, starting with Q^(l)(1) = Q(μ_{l∞}) (μ_{l∞} : the group of roots of unity of l-power order), and an associated graded Lie algebra g^(l), defined as follows. For each m ≥ 1, Q^(l)(m) is the field corresponding to the kernel of the representation
>
> G_Q ⟶ Out(F_2^(l)/F_2^(l)(m+1))

(注意: OCR テキスト層ではこの表現の行が「Out(if/jf(m+l))」に崩れている。画像照合で **Out(F_2^(l)/F_2^(l)(m+1))** — F_2^(l) は F₂ の pro-l 完備化・F_2^(l)(m+1) は lower central series — と確認。)

**§5.2 続き, 印刷 p.112(PDF 200)** — 主 pin(画像照合済・逐語):

> induced from φ_X^(l) for X = X₄ = P¹ − {0,1,∞}. This kernel will not change if X₄ is replaced by X_n (n ≥ 5) [Ih₅]. The union field Q^(l)(∞) corresponds to the kernel of φ_X^(l) for X = X_n, for any n ≥ 4. **It is a pro-l (non-abelian) extension over Q(μ_{l∞}) unramified outside l.** For each m ≥ 1, the Galois group Gal(Q^(l)(m+1)/Q^(l)(m)) is a free Z_l-module of finite rank (call it r^(l)(m)). It is centralized by Gal(Q^(l)(m+1)/Q^(l)(1)), and as Gal(Q^(l)(1)/Q)-module, has the Tate twist m. The graded Lie algebra g^(l) is the direct sum of its m-th graded pieces
>
> Gal(Q^(l)(m+1)/Q^(l)(m)) ⊗_{Z_l} Q_l   (m = 1,2,3,...),
>
> each of which is a Q_l-module (Q_l : the l-adic number field); cf. [Ih₄].

(太字は reader による強調。出典表示の事実関係: 「This kernel will not change …」の文には [Ih₅] が付くが、**「unramified outside l」の文自体には引用が付いていない**(講演録内では無証明の主張)。graded piece の記述には cf. [Ih₄] が付く。)

## Pin 2(主目標・対): Question 6.5.2 — 最大 pro-l 不分岐拡大かという開問題

**§6.5, 印刷 p.118(PDF 206)**(画像照合済・逐語):

> We shall conclude this lecture with two additional open questions.
>
> *Question 6.5.2.* i) *Is* Q^(l)(∞) *the maximal pro-l extension over* Q(μ_{l∞}) *unramified outside l ?*
>
> ii) *How big is* E^(l) *and* E^(l) ∩ Q(μ_{l∞}) ?

(文脈: 直前に **Corollary [A-I₁]  Q^(l)(∞) = Q(E^(l))** — E^(l) = higher circular l-units の群(Definition 6.5.1, 同 p.118)。i) が開問題として立っていること自体が、「Q^(l)(∞) ⊆ (l の外不分岐な最大 pro-l 拡大)」の包含は前提事実・逆包含が未知、という向きの傍証になる — ただしこの一文は reader の読み取りであり判定は司令塔へ。)

## Pin 3(副目標): §6.1 — f_σ から ψ_σ へ・anti 1-cocycle 性

**§6.1, 印刷 p.114(PDF 202)**(画像照合済・逐語):

> Take any σ ∈ G_Q. Then the action of σ on F̂₂ can be expressed by two coordinates χ(σ) and f_σ (χ(σ) ∈ Ẑ^×, f_σ ∈ F̂₂′) (see §2.3). Therefore, its action on F₂^nil can be expressed by χ(σ) and the projection f_σ^nil of f_σ on F₂^nil.

> (f_σ^nil)^{−1} = 1 + A₁ξ + A₂η   (A₁, A₂ ∈ 𝒜) .
>
> Put ψ_σ(ξ,η) = 1 + A₁ξ. Then it follows easily from (3.1.1)(I) that
>
> f_σ^nil = ψ_σ(η,ξ) · ψ_σ(ξ,η)^{−1} .
>
> Thus, *knowing ψ_σ is equivalent to knowing f_σ^nil*. Moreover, ψ_σ is an anti 1-cocycle
>
> ψ_{στ} = σ(ψ_τ) · ψ_σ   (σ, τ ∈ G_Q)
>
> with respect to the action of G_Q on 𝒜 extending that on F₂^nil, and is more convenient for describing the σ-action on abelian subquotients of π̂₁ ([Ih₂]; cf. also [A-I₂ §2]).

(𝒜 = Ẑ≪ξ,η≫ 非可換冪級数環・F₂^nil を x → 1+ξ, y → 1+η で埋め込む。同 p.114。)

## Pin 4(副目標・核心): §6.2 — Soulé cyclotomic elements = μ_{l^n} 値の Kummer 的コサイクル

**§6.2, 印刷 p.115(PDF 203)**(画像照合済・逐語):

> **6.2 The Old Invariants.** Fix a prime number l.
> (i) *The l-adic cyclotomic character* χ^(l) is the l-component of χ, i.e., χ(σ) = (χ^(l)(σ)), χ^(l)(σ) ∈ Z_l^×.
> (ii) *The cyclotomic elements* (Soulé, Deligne). These are certain continuous mappings
>
> κ_m^(l) : G_Q ⟶ Z_l   (m ≥ 1, odd) ,
>
> satisfying the 1-cocycle relation
>
> κ_m^(l)(στ) = κ_m^(l)(σ) + χ^(l)(σ)^m κ_m^(l)(τ)   (σ, τ ∈ G_Q) .   (6.2.1)

> **[Construction]** Let n ≥ 1 (but n ≥ 2 if l = 2). Put ζ_n = exp(2πi/l^n) and
>
> ε_{m,n} = ∏_a (ζ_n^a − 1)^{⟨a^{m−1}⟩} ,
>
> where the product is over all integers a such that 0 < a < l^n and (a,l) = 1; ⟨a^{m−1}⟩ is the smallest positive integer congruent to a^{m−1} mod l^n. Note that ε_{m,n} is totally real and totally positive (because m is *odd*). It is easy to see that each of ε_{m,n+1}/ε_{m,n} and σ(ε_{m,n})/ε_{m,n}^b is an l^n-th power of a totally positive element of Q(μ_{l∞}), where σ ∈ G_Q, b ∈ Z, b ≡ χ^(l)(σ)^{1−m} (mod l^n). Hence there is a unique κ_m^(l)(σ) ∈ Z_l such that
>
> σ((ε_{m,n})^{1/l^n}) = (σ(ε_{m,n}))^{1/l^n} · ζ_n^{χ^(l)(σ)^{1−m}·κ_m^(l)(σ)}
>
> holds for all n ≥ 2. Moreover, κ_m^(l) satisfies (6.2.1). Here, for any positive real number c, c^{1/l^n} denotes its *positive real* root. By (6.2.1), κ_m^(l) factors through Gal(Q(μ_{l∞})^ab/Q), Q(μ_{l∞})^ab being the maximal *abelian* extension of Q(μ_{l∞}). Moreover, by Soulé [So₁,₂], these 1-cocycles κ_m^(l) do not vanish at least if l > 2.

(これが「μ_l 値コサイクル(Kummer 的量)」の本論文における現形: 円単数系 ε_{m,n} の l^n 乗根への σ-作用のずれ ζ_n^{…} として κ_m^(l) を定義。**不分岐性そのものの明示証明はこの節に無い** — 構成と cocycle 関係・非消滅([So₁,₂] 引用)のみ。)

**つなぎ(§6.1 末尾→§6.2 冒頭, 印刷 pp.114–115・画像照合済)**:

> Then G_Q → (𝒜^ab)^× (σ ↦ ψ_σ^ab) is a 1-cocycle, and it turns out that each coefficient of ψ_σ^ab can be expressed in terms of "old invariants" of σ which we now recall.

(さらに §6.3, 印刷 p.115: **Theorem [A₃, C₃, IKY]** が ψ_σ^ab(ξ,η) を κ_m^*(σ)(= κ_m^(l) の正規化)と Bernoulli 項で明示表示する公式。式は長いので画像 pin のみ: ψ_σ^ab(ξ,η) = exp{Σ_{m≥3,odd} (κ_m^*(σ)/m!)((X+Y)^m − X^m − Y^m)} × exp{−(1/2)Σ_{m≥2,even} (b_m(1−χ(σ)^m)/m!)((X+Y)^m − X^m − Y^m)} — X, Y の定義行は本ページ外(§6.3 内)・未逐語確認 = UNKNOWN。)

## Pin 5(副目標・outer 表現の単射性): §1 — Belyĭ の定理

**§1(1), 印刷 p.100(PDF 188・pdftotext、画像照合は p.100 未実施 = OCR 不確かの可能性低いが明記)**:

> Belyï proved, among other things in [B₁] that the canonical representation
>
> φ_X : G_Q → Out π̂₁(X(ℂ))
>
> for X = P¹ − {0,1,∞} is injective.

## Pin 6(補・分岐関連の他言及): §1(6)(ii) — Oda–Matsumoto(Néron–Ogg–Šafarevič 類似)

**§1(6)(ii), 印刷 p.102(PDF 190)**(画像照合済・逐語):

> (ii) T. Oda and Y. Matsumoto each gives, from different viewpoints, a non-abelian analogue of the Néron-Ogg-Šafarevič criterion for good reduction of curves, using π₁^nil instead of H₁^et; cf. [O].

**§1(4), 印刷 p.102(PDF 190)**(画像照合済・逐語 — 三塔と定義体):

> As for the common field of definition, (i) is related to abelian extensions over the cyclotomic field Q(μ_∞), (ii) to a very natural sequence of Galois extensions over Q that are nilpotent over Q(μ_∞), and (iii) to (the field generated by) higher circular l-units.

((i) = meta-abelian tower, (ii) = nilpotent tower, (iii) = genus 0 tower。列挙の定義文は印刷 p.101 末尾〜p.102。)

## Pin 7(補・Frobenius と Jacobi 和): §6.4 Theorem [Ih₁]

**§6.4, 印刷 p.117(PDF 205)**(画像照合済・逐語):

> **Theorem [Ih₁].** *Let l be a prime number, n ≥ 1,* 𝔭 *be a prime ideal of* Q(μ_{l^n}) *not lying above l, and* σ = σ_𝔭 *be a Frobenius element of* 𝔭. *Then for any l^n-torsion points s,t of* Q/Z *with s,t, s+t ≠ 0, the special value of the l-component of* ψ_σ^ab (∈ Z_l[[ξ,η]]) *at* ξ = exp(2πis) − 1, η = exp(2πit) − 1, *is essentially the Jacobi sum (w.r.t.* 𝔭, l^n, s, t*)*.

(l の外の素点 𝔭 で Frobenius が well-defined に作用し特殊値が Jacobi 和になる、という主張の逐語。「l 上に無い素イデアル」という制限の付き方が分岐集合の傍証。判定は司令塔へ。)

---

## 見つからなかったもの(明記)

- **探索範囲**: 講演録全文 印刷 pp.99–120(PDF 186–208)を pdftotext で全文検索(ramif/unramif/outside/Kummer/cocycle/kernel/fixed field/faithful/Jacobi/Frobenius/good reduction)+ 上記 9 ページを画像照合。
- **「unramified outside l」の証明**: この講演録内には**無い**。Pin 1 の文は無証明の事実主張(survey 文体)で、文単位の引用も付いていない。周辺引用は [Ih₅](kernel の n-非依存性)と [Ih₄](graded piece)。**完全証明の所在はこの論文からは特定できず** — 下記文献表の [Ih₂](塔 Q^(l)(m) の由来論文として §6.1 で引用)と [Ih₁] が第一候補だが、それはこの論文の記述からの推定ではなく一般常識側の当たりであり、判定は司令塔・数学者へ。
- **inner ambiguity を明示的に処理して不分岐性へ落とす論法の記述**: 明示的には**無い**。最も近いのは Pin 3(f_σ は Aut レベルの座標・基点は tangential base point で固定、§2.3 印刷 pp.105–106)と Pin 4(Kummer 構成)。「outer → cocycle」の橋の証明はこの講演録に無い。
- **「ramified only over l」等の別表現**: 無し(「unramified outside l」が 2 回 — Pin 1 と Pin 2 — が全て)。他の ramification 言及は §2.3 の tangential base point の「ramification index」(印刷 p.105、技術的・分岐塔とは無関係)と §1(6)(ii)(Pin 6)のみ。

## 文献表(遠征先リスト・references 印刷 pp.119–120 = PDF 207–208 から逐語・画像照合済)

- **[Ih₁]** Ihara, Y.: Profinite braid groups, Galois representations and complex multiplications. Ann. Math. **123** (1986) 43–106
- **[Ih₂]** Ihara, Y.: On Galois representations arising from towers of coverings of P¹∖{0,1,∞}. Invent. math. **86** (1986) 427–459
- **[Ih₃]** Ihara, Y.: Some problems on three point ramifications and associated large Galois representations. Adv. Stud. Pure Math. **12** (1987) 173–188
- **[Ih₄]** Ihara, Y.: The Galois representation arising from P¹ − {0,1,∞} and Tate twists of even degree. In: Galois groups over Q. Publ. MSRI, no. 16 (1989) 299–313. Springer, Berlin Heidelberg New York
- **[Ih₅]** Ihara, Y.: Automorphisms of pure sphere braid groups and Galois representations. In: The Grothendieck Festschrift, vol. 2. Progress in Mathematics, vol. 87. Birkhäuser, Basel 1991, pp. 353–373
- **[A-I₁]** Anderson, G., Ihara, Y.: Pro-l branched covering of P¹ and higher circular l-units. Ann. Math. **128** (1988) 271–293
- **[A-I₂]** Anderson, G., Ihara, Y.: ibid Part 2. Int'l J. Math. **1** (1990) 119–148
- **[A₁]** Anderson, G.: Cyclotomy and an extension of the Taniyama group. Compositio Math. **57** (1986) 153–217
- **[A₃]** Anderson, G.: (a) The hyperadelic gamma function. Invent. math. **95** (1989) 63–131. (b) ibid (a précis). Adv. Stud. Pure Math. **12** (1987) 1–19
- **[B₁]** Belyi, G. V.: On Galois extensions of a maximal cyclotomic field. Izv. Akad. Nauk USSR **43** (1979) 267–276; transl. Math. USSR Izv. **14** (1980) 247–256
- **[De]** Deligne, P.: Le groupe fondamental de la droite projective moins trois points. In: Galois groups over Q. Publ. MSRI, no. 16 (1989) 79–298. Springer, Berlin Heidelberg New York
- **[So₁]** Soulé, C.: On higher p-adic regulators. Lecture Notes in Mathematics, vol. 854. Springer, Berlin Heidelberg New York 1981, pp. 372–401
- **[So₂]** Soulé, C.: Éléments cyclotomiques en K-théorie. Astérisque **147–148** (1987) 225–257
- **[O]** Oda, T.: A note on ramification of the Galois representation on the fundamental group of an algebraic curve. J. Number Theory **34** (1990) 225–228; Part 2 in preparation
- **[IKY]** Ihara, Y., Kaneko, M., Yukinari, A.: On some properties of the universal power series for Jacobi sums. Adv. Stud. Pure Math. **12** (1987) 65–86

(在庫状況の注記: 本 pin の対象 PDF は ICM 全集 Vol.1。上記文献のうち工房在庫に有るものは司令塔が把握 — reader からは未確認 = UNKNOWN。)
