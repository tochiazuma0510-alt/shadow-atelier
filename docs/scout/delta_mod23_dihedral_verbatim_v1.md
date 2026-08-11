# Δ mod 23 dihedral 逐語 pin 記録 v1(裁定 820・CONE-GAP-4)

- **委嘱**: 裁定 820 の一点読(reader)。pin 4 点 = ①exceptional prime の定義(D1)・②Δ の例外素数リスト(D1)・③mod 23 表現の dihedral 性(D1/D2)・④h(ℚ(√−23))=3 の明示言及。
- **性格**: 逐語抽出(verbatim)のみ。解釈・発効判定は書かない(司令塔専権)。導出は「導出値」と明示。精読範囲は pin 限定(全文精読ではない)。
- 作成: 2026-08-12・精密読解係(reader)。

---

## 0. 書誌・出所・読了申告

### D1 = Swinnerton-Dyer(LNM 350・Antwerp III)

| 項目 | 内容 |
|---|---|
| 文献 | H. P. F. Swinnerton-Dyer, *On ℓ-adic representations and congruences for coefficients of modular forms*, in: Modular Functions of One Variable III (Antwerp 1972), Lecture Notes in Math. **350**, Springer, 1973, 巻頭 pp. 1–55 |
| PDF 実体 | `papers/lnm350-antwerp-iii-1973.pdf`(巻全体 352 頁・テキスト抽出可) |
| sha256 | `aa03a07791ebdbc9d3bfab9561d425687b760bdf0b92f82022d913c2447c5fa8` |
| 頁番号の規約 | 論文印字頁 = 各頁欄外の「SwD-n」= 印字頁番号 n。**PDF 物理頁 = n + 5**(印字 p.4 = PDF 9・印字 p.32 = PDF 37 で二点照合済み)。以下「p.n」は印字頁。 |
| 節構成(目次・PDF 7) | §1 Introduction p.3 / §2 The possible images of ρ_ℓ p.10 / §3 Modular forms mod ℓ p.15 / §4 The exceptional primes p.26 / §5 Congruences modulo powers of ℓ p.36 / Appendix p.43 / References p.55 |
| 読了頁申告 | **精読(画像照合)**: pp.4, 5, 9, 12, 32, 33, 34, 35(= PDF 9, 10, 14, 17, 37, 38, 39, 40)。**検索走査のみ**(pdftotext 全文 grep で pin 該当なしを確認): 残り pp.1–55。 |
| 画像照合頁 | pdftocairo 150dpi で PDF 9, 10, 14, 17, 37, 38, 39, 40 をレンダリングし、以下の D1 逐語引用は全て画像で照合済み(pdftotext は当たり付けのみ)。 |

### D2 = Serre(Bourbaki 416)

| 項目 | 内容 |
|---|---|
| 文献 | J.-P. Serre, *Congruences et formes modulaires* [d'après H. P. F. Swinnerton-Dyer], Séminaire N. Bourbaki, 24e année, 1971/72, exposé n° 416(Juin 1972), p. 319–338(numdam 版) |
| PDF 実体 | `papers/serre_bourbaki416.pdf`(21 頁・スキャン。OCR 層はあるが語順が崩れており**引用には使用不可** — 当たり付けのみに使用) |
| sha256 | `0f68c67b057805fe1accfe3c97f74ecc1028fba0a9006e8d590f8ab3492994c6` |
| 頁番号の規約 | 論文印字頁 = 欄外「416-NN」(= numdam 頁 318+NN)。**PDF 物理頁 = NN + 1**(416-01 = PDF 2・416-15 = PDF 16 で二点照合済み)。以下「416-NN」で引く。 |
| 読了頁申告 | **精読(頁画像の目視)**: 416-01, 02, 14, 15, 16, 17, 18, 19, 20(= PDF 2, 3, 15, 16, 17, 18, 19, 20, 21)。**OCR grep 走査のみ**: 416-03〜416-13(= PDF 4–14・§1 後半〜§2 ゼータ値・pin 語(23, cubique, x³, S₃, discriminant 等)のヒットなしを確認。ただし OCR 品質の限界により**見落としの可能性は残る**)。 |
| 画像照合頁 | pdftocairo 150dpi で PDF 2, 3, 13, 14, 15, 16, 17, 18, 19, 20, 21 をレンダリング(うち 13, 14 は未精読)。以下の D2 逐語引用は全て画像で照合済み。仏語原文ママ。 |

---

## pin 1 ★ — exceptional prime の定義(D1)

### 1-a. 定義本文(D1 §1 末尾, p.9・画像照合)

> "In the application of lemma 1 G will be the image of ρ_ℓ and will certainly be closed since Galois groups are compact.  It will be convenient to say that ℓ is an **exceptional prime** for the cusp form f if the image of ρ_ℓ does not contain SL₂(ℤ_ℓ); with this definition lemma 1 can be rewritten as follows."

(原文で "exceptional prime" に下線。ρ_ℓ は §1 Theorem 1(Deligne)で f に付随させた ℓ 進表現 ρ_ℓ : Gal(K_ℓ/ℚ) → GL₂(ℤ_ℓ) — この文脈注記は pin 外のため逐語照合していない。)

### 1-b. 直後の系(同 p.9・画像照合。ρ̃_ℓ = ρ_ℓ の mod ℓ 還元)

> "COROLLARY. Suppose that ℓ > 3; then ℓ is exceptional for f if and only if the image of ρ̃_ℓ does not contain SL₂(𝔽_ℓ).  For ℓ = 2 or 3 this is still a sufficient condition for ℓ to be exceptional for f."

### 1-c. 参考: D2 側の定義(416-14, §3.1・画像照合・pin 指定は D1 だが版差記録のため)

σ_ℓ = (ρ_ℓ, χ_ℓ) を GL₂(ℤ_ℓ) × ℤ_ℓ* の部分群 H_ℓ = {(s,u) : det(s) = u^{k−1}} への連続準同型とした上で:

> "Disons que ℓ est **exceptionnel** (pour f) si l'image de σ_ℓ est distincte de H_ℓ."

続けて "THÉORÈME 10.- L'ensemble des nombres premiers exceptionnels est fini."(同頁)。D1(SL₂(ℤ_ℓ) を含まない)と D2(σ_ℓ の像が H_ℓ に一致しない)は**定式が異なる**(同値性の判定は書かない — 司令塔)。

---

## pin 2 ★ — Δ の例外素数リスト = 2, 3, 5, 7, 23, 691

### 2-a. D1 §1(p.5・画像照合)— 6 個の素数を一括で挙げる文

> "The existence of such congruences raises two obvious questions.  First, are there congruences for τ(n) modulo primes other than 2,3,5,7,23 and 691; and second, are the congruences (2) to (7) best possible or could one with greater labour prove congruences modulo even higher powers of the primes cited ?  These questions are the subject matter of these lectures.  It will be shown that there are no congruences for τ(n) modulo any other primes."

(直前 pp.4–5: 素数 23 は合同式 (6)・素数 691 は合同式 (7) = "τ(n) ≡ σ₁₁(n) mod 691." に対応。691 について p.5 冒頭: "the weight of Δ, and 691 divides the numerator of the Bernoulli number b₁₂." — いずれも画像照合。**リストは 691 を含む形**。)

### 2-b. D1 §4 の確定リスト = Theorem 4 の Corollary(p.32・画像照合)

表(Corollary (i)・type (i) の例外素数と m の値。列 = ℓ):

| Form | k | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 | Other ℓ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Δ | 12 | 0 | 0 | 1 | 1 | No | — | — | — | — | 691 |

(Δ 行の 13〜23 欄は空欄 = 表の対象外。表全体は 6 形式 Δ, QΔ, RΔ, Q²Δ, QRΔ, Q²RΔ を含むが pin 対象の Δ 行のみ転記。)

> "Here the first two columns give the form and its weight, the last column gives the exceptional ℓ > k (for which necessarily m = 0), and the other columns give for each ℓ < k the value of m if ℓ is exceptional, or the word 'No' if ℓ is not exceptional.
> (ii) For these six forms, the only exceptional primes of type (ii) are ℓ = 23 for Δ and ℓ = 31 for QΔ.
> (iii) With the possible exception of ℓ = 59 for QΔ, there are no exceptional primes of type (iii) for any of these six forms."

**導出値**(突合用): Δ の例外素数 = type (i) の {2, 3, 5, 7, 691} ∪ type (ii) の {23}(type (iii) なし)= **{2, 3, 5, 7, 23, 691}**。根拠 = 上表 + Corollary (ii)(iii)。D1 はこの合併を §4 では一文にまとめておらず、一括列挙は 2-a(p.5)の形。

### 2-c. D2 の確定リスト(416-15 §3.1 末尾・416-17 §3.3・画像照合)

416-15:

> "Ce résultat s'applique notamment à la fonction de Ramanujan a_p = τ(p), les nombres premiers exceptionnels étant 2 , 3 , 5 , 7 , 23 et 691 , cf. n° 3.3 ; ainsi, si ℓ ≠ 2 , 3 , 5 , 7 , 23 , 691 , la valeur de τ(p) (mod.ℓ) ne peut pas se déduire d'une congruence sur p ."

416-17(§3.3 Exemple : f = Δ の結び):

> "Finalement, les nombres premiers exceptionnels pour Δ sont 2 , 3 , 5 , 7 , 23 et 691 ."

(同 §3.3 の内訳・画像照合: "Le cas (i) est impossible pour ℓ > 13 , mis à part 691 qui est le numérateur de b₁₂ ; on constate que (i) se produit pour ℓ = 2 , 3 , 5 , 7 (cf. n°1.4), mais pas pour ℓ = 11 , 13 ." / 場合 (ii) は 2-d 参照 / "Enfin, si (iii) se produisait, on aurait τ(2) ≡ 0 , ±2⁶ (mod.ℓ) , et comme τ(2) = −24 , ce n'est possible que si ℓ = 2 , 3 , 5 , 11 , et on constate que ce n'est pas le cas.")

### 2-d. 「exceptional」の三分型(判定基準ごと・D2 416-15 §3.2・画像照合)

ℓ ≥ 5 が exceptionnel なら X_ℓ := Im(ρ̃_ℓ) は次のいずれか:

> "(i) X_ℓ est contenu dans un sous-groupe triangulaire de GL₂(𝔽_ℓ) ; la représentation ρ_ℓ est extension de deux représentations irréductibles de degré 1 , données par des puissances χ̃^m et χ̃^m' de la réduction mod.ℓ de χ_ℓ ; on a m + m' ≡ k − 1 (mod.(ℓ−1)) et a_p ≡ p^m + p^m' (mod. ℓ) si p ≠ ℓ .
> (ii) X_ℓ est contenu dans le normalisateur d'un sous-groupe de Cartan C de GL₂(𝔽_ℓ) , et n'est pas contenu dans C ; on a a_p ≡ 0 (mod.ℓ) si (p/ℓ) = − 1 .
> (iii) L'image de X_ℓ dans PGL₂(𝔽_ℓ) = GL₂(𝔽_ℓ)/𝔽_ℓ* est isomorphe au groupe symétrique 𝔖₄ ; on a a_p²/p^{k−1} ≡ 0 , 1 , 2 ou 4 (mod.ℓ) pour tout p ≠ ℓ ."

(D1 側の対応する分類 = Lemma 2(§2, p.12・画像照合)。pin 3-a に逐語。)

---

## pin 3 ★ — mod 23 表現の dihedral 性(D1/D2 の所在マップ)

### 3-a. D1: 分類補題の dihedral 場合(§2 Lemma 2, p.12・画像照合)

> "LEMMA 2. Let G be a subgroup of GL₂(𝔽_ℓ).  If the order of G is divisible by ℓ, then either G is contained in a Borel subgroup of GL₂(𝔽_ℓ) or G contains SL₂(𝔽_ℓ).  If the order of G is prime to ℓ, let H be the image of G in PGL₂(𝔽_ℓ); then
> (i) H is cyclic and G is contained in a Cartan subgroup, or
> (ii) **H is dihedral and G is contained in the normalizer of a Cartan subgroup but not in the Cartan subgroup itself**, or
> (iii) H is isomorphic to A₄, S₄ or A₅, where S denotes the symmetric and and A the alternating group.
> In case (ii) ℓ must be odd; in case (iii) ℓ must be prime to 6,6 or 30 respectively."

(原文の "and and"・"6,6" は誤植ママ。ℓ = 23 が Δ についてこの case (ii) に当たることは D1 では §4 Corollary (ii)(pin 2-b)で言明。)

### 3-b. D1: ℓ = 23 の像とヒルベルト類体(§4, pp.33–34・画像照合)

p.33(type (ii) の一般論・ℓ = 23, 31 の 2 例に適用):

> "It is however clear that the kernel of the homomorphism
> Gal(K_ℓ/ℚ) → N → N/C ∼ {±1},
> where C is a Cartan subgroup and N its normalizer, consists of those elements of the Galois group which are trivial on ℚ(√−ℓ); and hence for each of our two examples of case (ii) the image of ρ̃_ℓ is canonically isomorphic to Gal(K/ℚ) where K is some unramified abelian extension of ℚ(√−ℓ).  In the case k = 12, ℓ = 23 it is clear from (6) that K is the"

p.34(続き):

> "absolute class field of ℚ(√−ℓ); for the three lines of (6) correspond respectively to (p) remaining prime, splitting as a product of principal ideals, and splitting as a product of non-principal ideals, in ℚ(√−23)."

すなわち **K = ℚ(√−23) の絶対類体(ヒルベルト類体)であり、Im ρ̃₂₃ ≅ Gal(K/ℚ)**。ここで参照される合同式 (6)(§1, p.4・画像照合・Wilton による):

> "τ(p) ≡ 0 mod 23 if p is a quadratic non-residue of 23,
> τ(p) ≡ 2 mod 23 if p = u² + 23v² for integers u ≠ 0, v,      (6)
> τ(p) ≡ −1 mod 23 for other p ≠ 23;"

および (6) の証明手段とされる恒等式 (26)(p.34・画像照合):

> "2Δ ≡ ΣΣ q^{m² + mn + 6n²} − ΣΣ q^{2m² + mn + 3n²}  mod 23.      (26)"

> "Wilton [13] proved (6) by means of (26); but this very simple proof of (26) depends on the product formula (1) and there seems little prospect of a similar proof of (27)."

なお D1 は §4 でこの像の**未確定部分**も明言(p.33・画像照合): "For example, we have now proved the first line of (6) but we have not proved the second or third; nor have we in this case determined either the kernel or the image of ρ̃₂₃."(= (6) の全証明と像の決定は D1 の時点では [15]/Wilton 参照を除き完結していない、の逐語。解釈は書かない。)

### 3-c. D2: X₂₃ ≅ 𝔖₃ の明示(416-17 §3.3・画像照合)

> "Le cas (ii) se produit pour ℓ = 2k − 1 = 23 , cf. [15], n° 3.4, le groupe X_ℓ correspondant étant isomorphe à 𝔖₃ .  Vu ce qui précède, ce cas ne se produit pas pour ℓ > 23 ; on vérifie par calcul direct qu'il ne se produit pas non plus pour ℓ = 11 , 13 , 17 et 19 ."

- **X_ℓ = Im(ρ̃_ℓ) それ自体が 𝔖₃(対称群 S₃)と同型**という言明(射影像でなく)。射影像 𝔖₄ が現れるのは case (iii) の定義(pin 2-d)であり ℓ = 23 とは別。
- 出典指示は **[15] n° 3.4**。書誌(416-20 Bibliographie・画像照合):

> "[15] J.-P. SERRE - Une interprétation des congruences relatives à la fonction τ de Ramanujan, Séminaire Delange-Pisot-Poitou, 1967/1968, exposé 14."

(参考・同頁: "[18] H. P. F. SWINNERTON-DYER - Some implications of Ramanujan's methods of proving congruences for τ(n) (1971, non publié)." = D1 の講義録の前身。)

### 3-d. 「τ(p) ≡ N_p(x³−x−1) − 1 (mod 23)」型の式・x³−x−1 への言及: **両文書に不在(UNKNOWN)**

- **D1**: pdftotext 全文 grep(pp.1–55 相当域)で `x³−x−1` 型の三次式ヒットなし。D1 に現れる唯一の三次式は **ℓ = 59(QΔ・type (iii))の議論**であり x³−x−1 ではない(p.35・画像照合):
  > "Here L must be the absolute class-field of ℚ(√−59), which is the splitting field of x³ + 2x − 1 = 0."
- **D2**: 精読頁(416-01, 02, 14–20)に該当式なし。OCR grep でも `x³` / `cubique` / `N_p` 型のヒットは 416-05 の "réalisation comme cubique plane"(楕円曲線の話・§2 域)のみで無関係。**ℓ = 23 の S₃ 言明の根拠は [15] n° 3.4 への参照で済まされており、明示式は D2 に書かれていない**。
- 従って当該式の一次出典は(この 2 文書からの示唆としては)**[15] = Serre, Sém. Delange-Pisot-Poitou 1967/68 exp. 14 の n° 3.4 と推定されるが、[15] は盤上未収蔵のため UNKNOWN**(取り寄せは司令塔の職掌)。
- 「ℚ(√−23) の類指標からの誘導(induced/induit)」という語法も**両文書に不在**。D1 は 3-b の類体対応(分解型 ↔ (6) の三行)で表現し、D2 は X_ℓ ≅ 𝔖₃ とだけ言う。(D2 の未精読域 416-03〜13 に関しては OCR 走査のみ = 見落とし可能性の留保つき。)

---

## pin 4 — h(ℚ(√−23)) = 3 の明示言及

### 4-a. D1: **あり**(§4, p.34・画像照合)

> "The case k = 16, ℓ = 31 is extremely similar, the analogue of (6) holding with the obvious modifications; **the class number of ℚ(√−31), like that of ℚ(√−23), is 3.**"

### 4-b. D2: **明示言及は見当たらず(UNKNOWN)**

精読頁(416-01, 02, 14–20)に h(ℚ(√−23)) = 3 の明示なし。近い言明は case (iii)(𝔖₄ 型)への括弧書き(416-15・画像照合)のみで、ℓ = 23 とは別の場合:

> "(Si ce cas se produit, on peut montrer que ℓ ≡ ± 5 (mod.8) , et que le nombre de classes du corps quadratique de discriminant ± ℓ est divisible par 3 .)"

(未精読域 416-03〜13 の見落とし可能性の留保つき。)

---

## 台帳用の要約(1 行ずつ・全て candidate・文献裏書き)

| pin | 結果 | 一次根拠 |
|---|---|---|
| 1 | 定義 = 「Im ρ_ℓ ⊅ SL₂(ℤ_ℓ) なる ℓ を f の exceptional prime と呼ぶ」+ 系(ℓ>3 で mod ℓ 判定に落ちる) | D1 §1 p.9(SwD-9)。参考: D2 416-14 は σ_ℓ の像 ≠ H_ℓ という別定式 |
| 2 | Δ の例外素数 = **2,3,5,7,23,691**(691 を含む形で D1 p.5・D2 416-15/416-17 に一括列挙。D1 §4 の確定は表 {2,3,5,7,691}(type i)+ 23(type ii)+ type iii なし、の合併 = 導出値) | D1 p.5・p.32 Cor to Thm 4/D2 416-15, 416-17 |
| 3 | dihedral 性: D1 = Lemma 2(ii)(H dihedral・Cartan 正規化群)+ §4 で Im ρ̃₂₃ ≅ Gal(K/ℚ)・K = ℚ(√−23) のヒルベルト類体・(6) の三行 = 素イデアル分解型対応 + 恒等式 (26)。D2 = X₂₃ ≅ 𝔖₃ の明示(cf. [15] n°3.4)。**τ(p) ≡ N_p(x³−x−1)−1 型の式・x³−x−1・「誘導」の語は両文書に不在(UNKNOWN・推定一次出典 [15] は未収蔵)** | D1 p.12, pp.33–34, p.4, p.35/D2 416-15, 416-17, 416-20 |
| 4 | h(ℚ(√−23)) = 3: **D1 に明示あり**(p.34・ℚ(√−31) と並記)。D2 は見当たらず(UNKNOWN・未精読域の留保つき) | D1 p.34/D2 416-15(別場合の類数言及のみ) |
