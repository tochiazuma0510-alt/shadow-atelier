# K9-UNRAM 良還元原理の逐語 pin 集(reader 2 巡目・裁定 907)

- **状態**: candidate(reader 抽出・司令塔未照合)
- **標的**: 「p ≠ ℓ で pro-ℓ π₁(P¹−{0,1,∞}) への G_ℚ 作用が惰性群 I_p 上自明」を含意する逐語。最安の十分形 = 良還元 ⟹ 不分岐(Grothendieck specialization 型)。
- **探索範囲**: 在庫のみ — ①Ihara ICM 1990(印刷 pp.99–120 全文・新キーワード再走査)②正典 2401.06870 / 2405.11725(全文)③SGA1(arXiv:0206203 再版・343 ページ)④harbater-schneps-2000-TransAMS352・2008.00066・2106.06645・lochak-schneps-1994・serre_bourbaki416・lnm350(キーワード走査)。
- **照合方法**: pdftotext + 主要ページの 150dpi 画像照合(照合済ページは各 pin に明記)。
- **規律**: 逐語引用のみ・判定語なし。解釈は司令塔・数学者・Sol の裁定事項。

---

## Pin A(最重要・標的形そのもの): Harbater–Schneps 2000 — 「Grothendieck の比較定理の適用で ℓ の外不分岐」

**出典**: D. Harbater, L. Schneps, "Fundamental groups of moduli and the Grothendieck-Teichmüller group", Trans. AMS **352** (2000), no. 7, 3117–3148。在庫 = `papers/harbater-schneps-2000-TransAMS352-published.pdf`(雑誌版・印刷ページ = 3117 + (PDF ページ − 1))。

**§0.2, 印刷 pp.3121–3122(PDF pp.5–6。p.3122 は画像照合済・p.3121 側の導入行は pdftotext)** — 逐語:

> In [I1] Ihara studied a pro-ℓ analogue of Belyi's group A (with λ = 1), namely the subgroup Φ of the group of outer automorphisms of the pro-ℓ completion of F₂ consisting of outer automorphisms preserving the conjugacy classes of x, y and z. **An application of Grothendieck's comparison theorem shows that the representation Gal(Q̄/Q) → Φ is unramified outside ℓ;** the paper is devoted to a detailed study of the properties of this representation (which, unlike what happens in the profinite case, is far from injective).

(太字は reader の強調。文の形は outer 表現 G_ℚ → Φ ⊂ Out(F₂^(ℓ)) についての「unramified outside ℓ」。根拠として名指しされているのは **"Grothendieck's comparison theorem"** のみ・証明はこの論文に無い。)

**[I1] の書誌(同論文 references, 印刷 p.3147・pdftotext)** — 逐語:

> [I1] Y. Ihara, Profinite braid groups, Galois representations and complex multiplications, Ann. Math. 123 (1986), 43-106. MR 87c:11055

(同 references には [I4] = Ihara ICM Kyoto 1990, 99–120 もあり。1 巡目 pin 集 `docs/scout/ihara_icm_unram_pin_v1.md` の文献表と整合。)

## Pin B(古典根拠・proper 滑らか場合): SGA1 Exposé X — specialization 定理

**出典**: A. Grothendieck, M. Raynaud, SGA1 "Revêtements étales et groupe fondamental", arXiv:math/0206203(再版)。在庫 = `papers/sga1-grothendieck-raynaud-arxiv0206203.pdf`。ページ表記: 再版本文ページ(ページ上部)+ arXiv PDF ページ + 欄外は原版 LNM224 ページ番号。

**Exp. X, Théorème 3.8, 再版 p.217(arXiv PDF p.233・欄外 283・画像照合済)** — 逐語:

> **Théorème 3.8**. — Soient f : X → Y un morphisme propre et lisse, à fibres géométriquement connexes, avec Y localement noethérien, y₀ et y₁ deux points de Y tels que y₀ ∈ {y₁}⁻, X̄₀ et X̄₁ les fibres géométriques correspondantes, considérons l'homomorphisme de spécialisation (2.4) π₁(X̄₁) → π₁(X̄₀). Cet homomorphisme est surjectif, et tout homomorphisme continu de π₁(X̄₁) dans un groupe fini G d'ordre premier à la caractéristique p de k(y₀) provient d'un homomorphisme de π₁(X̄₀) dans G.

**Exp. X, Corollaire 3.9(同ページ・画像照合済)** — 逐語(抜粋):

> **Corollaire 3.9**. — Si k(y₀) est de caractéristique nulle, alors l'homomorphisme de spécialisation est un isomorphisme. Si k(y₀) est de caractéristique p > 0, alors le noyau de l'homomorphisme de spécialisation est contenu dans l'intersection des noyaux des homomorphismes continus de π₁(X̄₁) dans des groupes finis d'ordre premier à p (…) ; si donc π₁(X̄₁)^(p) désigne le groupe quotient de π₁(X̄₁) par le sous-groupe fermé précédent, et si on définit de même π₁(X̄₀)^(p), alors l'homomorphisme de spécialisation induit un isomorphisme
>
> π₁(X̄₁)^(p) ⟶∼ π₁(X̄₀)^(p)

(注意: Exp. X は **propre et lisse** の仮定。P¹−{0,1,∞} は proper でないため、開曲線用は Exp. XIII(Pin C)。)

## Pin C(古典根拠・開曲線/tame 場合): SGA1 Exposé XIII §2 — π₁^𝕃 / π₁^t の specialization

**Exp. XIII, 2.10, 再版 p.289(arXiv PDF p.305・欄外 390–391・画像照合済)** — 逐語(抜粋):

> **2.10.** Si U est un schéma connexe, a un point géométrique de U, 𝕃 un ensemble de nombre premiers, on note
>
> (2.10.0)  π₁^𝕃(U, a)
>
> la limite projective des quotients finis de π₁(U, a) dont les ordres ont tous leurs facteurs premiers dans 𝕃.
> Nous allons définir des morphismes de spécialisation pour le groupe fondamental, généralisant X.2.

同 2.10 の末尾(inner ambiguity の明示・画像照合済) — 逐語:

> Les hypothèses de propreté cohomologique (resp. 2.8) prouvent que π₂ est un isomorphisme. Si l'on choisit une classe de chemins de a₁ à a₂, on obtient un isomorphisme (…) d'où un morphisme π = π₂⁻¹π₁₂π₁ (…) **Changer la classe de chemins de a₁ à a₂ revient à modifier π par un automorphisme intérieur** de π₁^𝕃(X_{s̄₂}, a₂) (resp. de π₁^t(X_{s̄₂}, a₂)). On appelle *morphisme de spécialisation* pour le groupe fondamental associé au morphisme s̄₁ → s̄₂ (…)

**Exp. XIII, Lemme 2.11, 再版 p.290(arXiv PDF p.306・欄外 392・画像照合済)** — 逐語(抜粋):

> **Lemme 2.11**. — Soient f : X → S un morphisme propre de présentation finie, D un diviseur sur X à croisements normaux relativement à S, Y = Supp D, U = X − Y, (…) Soit I_{y₁} un sous-groupe d'inertie de π₁^t(U_{s̄₁}) en y₁. Alors l'image de I_{y₁} par le morphisme de spécialisation
>
> π : π₁^t(U_{s̄₁}) ⟶ π₁^t(U_{s̄₂})
>
> est un sous-groupe d'inertie de π₁^t(U_{s̄₂}) en y₂.

**Exp. XIII, Corollaire 2.12, 再版 pp.290–291(arXiv PDF p.306・欄外 392–393・画像照合済)** — 逐語(冒頭):

> **Corollaire 2.12**. — Soit X une courbe propre et lisse connexe de genre g sur un corps séparablement clos k de caractéristique p ⩾ 0. Soit U l'ouvert obtenu en enlevant à X n points fermés distincts a₁, …, a_n. Alors le groupe fondamental modérément ramifié π₁^t(U) (2.1.3) peut être engendré par 2g + n éléments xᵢ, yᵢ, σⱼ (…) liés par la seule relation (∗).

同 2.12 の証明中(等標数 0 → 正標数の specialization の全単射性・pdftotext, 再版 pp.291–292 = arXiv PDF pp.306–307) — 逐語:

> il résulte de 2.8 que le morphisme de spécialisation
>
> (R¹g₁∗ C_{U₁})_k̄ ⟶ (R¹g₁∗ C_{U₁})_K̄
>
> est injectif et même bijectif si C est d'ordre premier à p. Or cela signifie, en termes de groupes fondamentaux, que le morphisme de spécialisation (1.10)
>
> π : π₁(Ū) ⟶ π₁^t(U)
>
> est surjectif, et que le morphisme de spécialisation
>
> π₁^{p′}(Ū) ⟶ π₁^{p′}(U)
>
> est bijectif.

(この段落の Ū = U₁ ×_S K̄(標数 0 生成ファイバー)・U = 標数 p 特殊ファイバー。前提は S = Spec A・A 完備離散付値環・X₁/S propre lisse・除点は S 上の切断 — すなわち**相対正規交叉因子の補集合の良還元設定**。)

## Pin D(based 射への持ち上げ・惰性保存): 2008.00066 §1.1

**出典**: V.A. Dolgushev, "What are GT-shadows?"(arXiv:2008.00066)。在庫 = `papers/2008.00066-what-are-gt-shadows.pdf`。

**p.4(PDF p.4・画像照合済)** — 逐語:

> Applying the basic theory of the algebraic fundamental group [11], [28, Section 5.6] to
>
> P¹_ℚ ∖ {0,1,∞},
>
> we get an outer action of the absolute Galois group G_ℚ on F̂₂. **Using the fact that this action preserves the inertia subgroups, we can lift this outer action to an honest action of the form**
>
> g(x) = x^{χ(g)},  g(y) = f̂_g(x,y)⁻¹ y^{χ(g)} f̂_g(x,y),  g ∈ G_ℚ ,   (1.4)
>
> where χ : G_ℚ → Ẑ^× is the cyclotomic character and f̂_g(x,y) is an element of ([F̂₂, F̂₂])^cl that depends only on g.

**引用先の書誌(同論文 references・pdftotext)** — 逐語:

> [11] A. Grothendieck and M. Raynaud, Revêtements étales et groupe fondamental, (SGA1), Lecture Notes in Mathematics, 224. Springer-Verlag, Berlin-New York, 1971.
> [28] T. Szamuely, Galois groups and fundamental groups, Cambridge Studies in Advanced Mathematics, 117. Cambridge University Press, Cambridge, 2009.

(based 化(outer → honest action)の根拠 = 惰性部分群の保存、と明記。ただし分岐(I_p 上の自明性)には触れていない。)

## Pin E(Ihara ICM 再走査の結果): 追加ヒットなし・Oda 言及のみ

新キーワード("good reduction"・"specialization"・"specialisation"・"smooth"・"inertia"・"Néron"・"Safarevic"・"reduction mod")で印刷 pp.99–120 全文を再走査。ヒットは 1 件のみ = 1 巡目 pin 集 Pin 6 と同一箇所:

**§1(6)(ii), 印刷 p.102(PDF p.190・1 巡目に画像照合済)** — 逐語:

> (ii) T. Oda and Y. Matsumoto each gives, from different viewpoints, a non-abelian analogue of the Néron-Ogg-Šafarevič criterion for good reduction of curves, using π₁^nil instead of H₁^et; cf. [O].

**[O] の書誌(印刷 p.120・1 巡目に画像照合済)** — 逐語:

> [O] Oda, T.: A note on ramification of the Galois representation on the fundamental group of an algebraic curve. J. Number Theory **34** (1990) 225–228; Part 2 in preparation

(Ihara ICM 本文中の [O] への言及はこの 1 文のみ。Oda の結果として引かれているのは「良還元判定の非可換類似(NOS 類似)」であり、P¹−{0,1,∞} の p≠ℓ 不分岐性の明示文は ICM 側には無い。)

---

## 見つからなかったもの(明記)

- **正典 2 本(2401.06870・2405.11725)**: `unramif / ramif / inertia / good reduction / specializ` の**全文一致ゼロ**(pdftotext 全文 grep・各 3586 / 2444 行)。π₁ の不分岐性・良還元は本文・脚注・参考文献のどこでも引かれていない。Galois 入力の引用形は:
  - 2405.11725, p.1(PDF p.1・pdftotext): "Although the question of surjectivity of Ih (see [14]) is a very challenging one, …" — [14] = Ihara ICM Kyoto 1990(書誌逐語: "[14] Y. Ihara, Braids, Galois groups and some arithmetic functions, A plenary address presented at the ICM held in Kyoto, August 1990. ICM-90. Mathematical Society of Japan, Tokyo; distributed outside Asia by the AMS, Providence, RI, 1990.")
  - 2405.11725, §1.6(PDF p.8・pdftotext): "In [16, Theorem A], Y. Ihara constructed a group homomorphism I_K from the absolute Galois group G_{ℚ(μ_{l∞})} of ℚ(μ_{l∞}) to the multiplicative group (Z_l[[u,v]])^× of the ring of formal Taylor power series Z_l[[u,v]]." — [16] = Ihara, Ann. of Math. (2) **123**, 1 (1986) 43–106。
  - 2401.06870 は Galois 側の言及自体が引用列挙([1],[3],[4],[7],[12],[13],[15],[18],…)のみで分岐の話は無い。
- **「P¹_ℤ−{0,1,∞} は ℤ 上滑らか ⟹ …」という算術的定式化そのもの**: 在庫のどの論文にも**この形の一文は無い**。在庫内で最も近い組は Pin B+C(SGA1 の幾何的 specialization 束)+ Pin A(HS2000 の帰結主張「comparison theorem の適用で unramified outside ℓ」)。両者をつなぐ算術的導出(I_p 上の自明性への落とし込み)を書いた在庫文献は見つからなかった — Pin A の [I1](= Ihara Annals 123 (1986)、**在庫に無い**)と 1 巡目文献表の [Ih₂](Invent. math. 86 (1986)、**在庫に無い**)が遠征先候補のまま。
- **serre_bourbaki416.pdf**: "ramif" 4 件はいずれもモジュラー形式付随 Galois 表現(例: "GL₂(Ẑ) non ramifié en dehors de …", pdftotext 行 3517)で π₁ 型ではない。同型の言明**無し**。
- **lnm350-antwerp-iii-1973.pdf**: "ramif" 41 件・"fundamental group" 1 件(Frobenius 持ち上げ・Hasse 不変量の文脈, pdftotext 行 6239)。同型の言明**無し**。
- **2106.06645**: "unramified" 1 件(pdftotext 行 1015: "is a morphism of curves unramified outside of the set {0,1,∞}" — Belyĭ 射の定義文)。標的とは別物。
- **lochak-schneps-1994-LMS200**: キーワードヒットなし。

## OCR/版の注意

- SGA1 は arXiv 再版(TeX 組み直し・テキストネイティブ)。引用は再版本文ページ+欄外の原版 LNM224 ページ(283, 390–393)併記。原版 LNM224 との文面差は UNKNOWN(再版の Remarque (ajoutée en 2003 (MR)) が Cor 2.12 直後に挿入されていることを確認 — 引用部はすべて再版でも本文扱いの箇所)。
- HS2000 は雑誌版 PDF(テキストネイティブ)・p.3122 を画像照合。文頭の一部("In [I1] Ihara studied …")は p.3121 側で pdftotext のみ(低リスクだが明記)。
- 数式の上付き(π₁^𝕃, π₁^t, π₁^{p′}, X̄₁ 等)はすべて画像で照合済。
