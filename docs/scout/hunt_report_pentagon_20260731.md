# 遠征報告 hunt_pentagon_20260731 — pentagon(B₄ 系)の正本確保

遠征係(文献ゲート①)/ 発注: 司令塔スペック「pentagon 条件・B₄ 本来系の定義正本」
全候補は実 URL 取得で実在確認済み。PDF は本ディレクトリ(金庫)。

---

## 0. 困難の抽象化と当たり付け(3 通り)

工房の困難 = 「hexagon だけの gentle 系(B₃)で計算基盤ができた。pentagon(B₄)を同じ**有限商・置換群の計算**に落とせるか、落とすといくらかかるか」。

| # | 抽象化(分野非依存の機構) | 導いた探索分野・理由 | 結果 |
|---|---|---|---|
| A1 | 「切り詰めたオペラッドの自己準同型を、生成元 2 個(σ, α)と**関係式の完全系**で表す」= **有限表示の presentation 問題** | オペラッド論・高次圏(PaB = parenthesized braid operad)。pentagon は「truncated operad PaB₄ の関係式の完全系のうち σ に関わらない方」として現れるはず → operad 側の文献に**書き下しの正本**があると当たりを付けた | **的中**。2008.00066 §2.3 が (2.13) pentagon 図式 →(2.20) 群方程式へ完全に落としている |
| A2 | 「非可換群 P の元 f に対し、5 本の**余面写像(coface)** ∂: P₃→P₄ の像の積が消える」= **余単体的群(cosimplicial group)の 1-コサイクル条件** | 単体的手法・群コホモロジー。ここに落ちるなら ∂ は生成元上の値だけで決まり、**有限商での判定は語の評価に還元**する(=置換群で計算可能) | **的中**。2008.00066 Appendix A.4 (A.16)(A.18) が余面 5 本を PB₃ の生成元 x₁₂,x₂₃,x₁₃ 上で明示。まさに余単体的構造として書かれている |
| A3 | 「関係式系の**冗長性**: 3 本のうち 1 本が残り 2 本を含意するか」= 方程式系の従属性・Gröbner 的縮約 | 量子群・結び目不変量(Drinfeld associator の Furusho 定理「pentagon ⇒ hexagon」)。もし profinite でも成り立つなら **hexagon 計算を pentagon で置き換え/併用**する設計判断が変わる | **部分的中**。2008.00066 §4.3 が「Furusho property の profinite 版」を**性質として定義し、35 例で機械判定**(強 11/35・弱 13/35)。=「profinite では一般には成立しない」が実データつきで分かる |

---

## 1. 候補表

| # | 書誌 | 実在確認 | 効く項目 | 金庫内ファイル |
|---|---|---|---|---|
| C1 | V. A. Dolgushev, K. Q. Le, A. A. Lorenz, **"What are GT-shadows?"**, arXiv:2008.00066 [math.AT] (v1 2020-07-31 / v2 2021-10-31). **Algebr. Geom. Topol. 24 (2024) 2721–2777**, DOI 10.2140/agt.2024.24.2721 | arxiv.org/abs/2008.00066 取得 | **1・3・4・5** | `2008.00066v2.pdf` (54p) |
| C2 | V. A. Dolgushev, **"The Action of GT-Shadows on Child's Drawings"**, arXiv:2106.06645 [math.AT, math.NT] (v1 2021-06-12 / v3 2024-07-16). DOI 10.48550/arXiv.2106.06645(**arXiv のみ・掲載誌記載なし**) | arxiv.org/abs/2106.06645 取得 | **2・4** | `2106.06645v3.pdf` (39p) |
| C3 | V. A. Dolgushev, **Package GT**(Python, PaB.py 他 + データファイル群) | sites.temple.edu/vald/files/2024/05/PackageGT.zip / …/PackageGT_README.pdf 取得成功(**旧 URL math.temple.edu/~vald/PackageGT/ は 308 で死んでいる** — 2106.06645 の [7] に生きたリンクあり) | **4**(最重要) | `PackageGT.zip`, `PackageGT_README.pdf`, 展開済 `pkg/PackageGT/` |
| C4 | P. Guillot, **"The GT group of a finite group and G-dessins d'enfants"**, arXiv:1407.3112 [math.GR] (v3 2015-12-03). Springer Proc. Math. Stat. 159, 159–191 | arxiv.org/abs/1407.3112 取得 | **5**(のみ)・4 は×(下記) | `1407.3112.pdf` |
| C5 | P. Guillot, **"The GT group of PSL(2,q)"**, arXiv:1604.04415 [math.GR] (2016-04-15). J. Group Theory 21 (2018) 241–251 | arxiv.org/pdf/1604.04415 取得 | **5** | `1604.04415.pdf` |
| C6 | D. Harbater, L. Schneps, "Fundamental groups of moduli and the GT group", Trans. AMS 352 (2000) 3117–3148 | **書誌のみ**(2008.00066 [15] より)。本文未取得 = **未達** | 5(gentle 版 GT_gen の初出) | — |

補: I. Bortnovskyi, V. A. Dolgushev, B. Holikov, V. Pashkovskyi, arXiv:2405.11725(工房既知)の **Remark 1.2** を原文確認済み(下記 §4)。

---

## 2. 【最重要】pentagon の明示形 — 得られた(はい)

**C1 §2.3 に、有限商で機械判定できる完全な形がある。**

### 2.1 pentagon 関係式(C1 式 (2.20))

N ∈ NFI_{PB₄}(B₄)、f ∈ PB₃(実際は F₂ ⊂ PB₃)に対し

    ∂₂₃₄(f) · ∂₁,₂₃,₄(f) · ∂₁₂₃(f) ≡ ∂₁,₂,₃₄(f) · ∂₁₂,₃,₄(f)   (mod N)   … PB₄/N の中で

hexagon は同 (2.18)(2.19) として **B₃/N_{PB₃}** の中で:

    ∂₁x₁₂^m ∂₂ f⁻¹ x₂₃^m f ≡ f⁻¹ ∂₁₂(x₁₃x₂₃)^m ,   ∂₂ f⁻¹x₂₃^m f ∂₁x₁₂^m ≡ ∂₂₁(x₁₂x₁₃)^m f
(工房の「(fa₁)²=1 ∧ (fb₁⁻¹)³=1」翻訳に対応するのは B₃ 側のこれ。**pentagon だけが PB₄ 側**。)

### 2.2 余面写像の明示式(C1 (A.18)) — これが「置換群に落ちる」ことの本体

5 本の準同型はすべて PB₃ の生成元 x₁₂, x₂₃, x₁₃ 上の値で決まる:

    ∂₁₂₃  : x₁₂↦x₁₂,      x₂₃↦x₂₃,      x₁₃↦x₁₃
    ∂₂₃₄  : x₁₂↦x₂₃,      x₂₃↦x₃₄,      x₁₃↦x₂₄
    ∂₁₂,₃,₄: x₁₂↦x₁₃x₂₃,   x₂₃↦x₃₄,      x₁₃↦x₁₄x₂₄
    ∂₁,₂₃,₄: x₁₂↦x₁₂x₁₃,   x₂₃↦x₂₄x₃₄,   x₁₃↦x₁₄
    ∂₁,₂,₃₄: x₁₂↦x₁₂,      x₂₃↦x₂₃x₂₄,   x₁₃↦x₁₃x₁₄

(B₃ 側の対応物は (A.19): ∂₁₂(x₁₂)=x₁₂, ∂₂₃(x₁₂)=x₂₃, ∂₁₂,₃(x₁₂)=x₁₃x₂₃, ∂₁,₂₃(x₁₂)=x₁₂x₁₃。)

**翻訳可能性(工房設定へ)**: これは *初等的な書き下しに落ちる*。必要なのは (i) PB₄/N を **6 個の置換 (x₁₂,x₂₃,x₁₃,x₁₄,x₂₄,x₃₄) の生成する置換群**として持つこと、(ii) f を F₂ = ⟨x₁₂,x₂₃⟩ の語として持つこと、(iii) 語の各文字を上表で置換に写して 5 本の積を比較すること。GAP でそのまま書ける(Image/PermGroup と語の評価のみ、コホモロジーも表現論も不要)。

### 2.3 実装の実在確認 — C3 `pkg/PackageGT/PaB.py`

`def penta(wm, t)`(508 行〜)がまさに上記そのもの:
- `t` = **6 個の置換のタプル** `x12,x23,x13,x14,x24,x34`(= N ∈ NFI_{PB₄}(B₄) の表現)
- 語 `w` の各文字を `fi234(t)`, `fi123(t)`, `fi12_3_4(t)`, `fi1_23_4(t)`, `fi1_2_34(t)` で写して合成
- 判定は 1 行: `compAll((f234,f1_23_4,f123)) == comp(f1_2_34,f12_3_4)`

→ **pentagon の計算コスト = 「F₂/N_{F₂} の全語(または交換子部分群の全語)を回して置換積を 5 本比較」**。C1 §4 の実データ:
- N⁽¹⁹⁾(“Philadelphia subgroup”, N_ord=6): pentagon を満たす f が **216 個**、うち hexagon も満たす (m,f) を持つのは **36 個**。
- N⁽³⁴⁾(“Mighty Dandy”, N_ord=9): [F₂/N_{F₂},F₂/N_{F₂}] 内で pentagon を満たすのが **4096 個**、うち hexagon も持つのは **243 個**。GT(N⁽³⁴⁾) は位数 486=2·3⁵、≅ (ℤ₂×ℤ₃)⋉(ℤ₉×ℤ₉)。
- Leila Schneps 提供の N_L: PB₄ 内指数 2²⁹·3¹² = 285,315,214,344,192、|F₂:N_{F₂}| = 2¹⁰·3⁵ = 248,832、N_ord=12。

→ **見積の読み**: 支配的なのは PB₄ の指数ではなく **|F₂ : N_{F₂}|**(候補 f の列挙数)。工房の B₃-gentle の探索規模感がそのまま移送できる。深読み時の照合観点 = 「我々の N ∈ NFI_{PB₃}(B₃) に対し Prop 2.5(A) が保証する持ち上げ K ∈ NFI_{PB₄}(B₄) を実際に構成できるか」(C1 Prop 2.5 / Prop 3.9)。

---

## 3. 項目 4(有限商での pentagon 実計算例)の追加所見

C3 の zip に**再現用データが同梱**されている: `subGrPB4_org35`(§4.2 の 35 個の N⁽⁰⁾..N⁽³⁴⁾)、`G_Mighty_Dandy`、`Mighty_Dandy_wm_list`(6.8MB)、`Leila_PB4`、`wm_list_charm35` 他。**C1 §4 の全数値は再実行で追検証可能**(工房の「探索器と照合器の分離」に乗せられる: Python 版を探索器、GAP 独立実装を照合器)。

`NotUsed.py` に `penta_k`, `gener_pr_penta` 等の別実装があり、**同一命題の第二実装として cross-check に使える**。

---

## 4. 項目 5 — 「GT-shadow」同名別物の対応表(原文確認済み)

| 系統 | 群 | 台 | 関係式 | 対象集合 Ob(GTSh) | 正本 |
|---|---|---|---|---|---|
| **本来系** | **ĜT**(Drinfeld/Ihara の profinite GT) | B₄ / PaB(≤4) | hexagon ×2 **+ pentagon** | **NFI_{PB₄}(B₄)** | **C1 = 2008.00066**(+ C2 = 2106.06645 が dessins 作用) |
| **gentle 系**(工房の主線) | **ĜT_gen**(Harbater–Schneps 2000 導入) | B₃ / PaB(≤3) | hexagon のみ | **NFI_{PB₃}(B₃)** | 2401.06870(+ 2405.11725) |
| **coarse 系** | **ĜT₀** | truncated PaB(≤3) の連続自己同型 | pentagon を**落とした**もの、ĜT ⊂ ĜT₀ | — | C1 Remark 1.3 が定義を述べ、**P. Guillot [C4][C5] がこの coarse 版の変種を研究**と明記 |

2405.11725 **Remark 1.2 原文**:
> "GT-shadows for the original version of ĜT were introduced in paper [7]. Note that, in paper [7], the notation GTSh is used for the groupoid of GT-shadows for ĜT and the set of objects of this groupoid is NFI_{PB₄}(B₄). In this paper, GTSh denotes the groupoid of GT-shadows for ĜT_gen and, here, Ob(GTSh) := NFI_{PB₃}(B₃)."

C1 **Remark 1.3 原文**(要点):
> "omitting the pentagon relation from the definition of ĜT, we get the coarse version ĜT₀ … ĜT₀ is the group of continuous automorphisms of the truncated operad PaB^{≤3} and ĜT is a subgroup of ĜT₀. In papers [12] and [13], P. Guillot studies a variant of GT-shadows for this coarse version ĜT₀."

**注意(誤配防止)**: 2401.06870 の "gentle" ĜT_gen と C1 Remark 1.3 の "coarse" ĜT₀ は**別概念**(どちらも pentagon なしだが定義が違う)。C1 は Guillot を ĜT₀ 側に位置づけている。両者の異同を明言した文は今回の探索では**見つからなかった**(= 深読み時の照合観点その 2)。

---

## 5. 候補ごとの機構ベース評(短評)

- **C1**: 本遠征の当たり。定義正本であるだけでなく、**pentagon を有限商の置換計算に落とす完全なレシピ(2.20)+(A.18)** と **35 例の実測** を同時に持つ。工房の B₃ 資産(NFI_{PB₃}(B₃) の列挙器・cert スキーマ)は Prop 2.5(A) の持ち上げを通して**そのまま B₄ 側の入口になる**。移送コストは「x₁₄,x₂₄,x₃₄ を足して 6 生成置換群にする」だけ。
- **C2**: pentagon 自体の新情報は薄いが、**GT-shadow → dessins 作用**という出口(工房の「実現性」側)を与える。Appendix B が C3 の使い方。
- **C3**: 単なる補助でなく**第三者クロスチェック資源**。penta() が我々の設計と同型なので、**同じ N で数を突き合わせれば較正ゲートになる**。
- **C4/C5**: **pentagon を扱っていない**(全文で "pentagon"/"hexagon" の語がゼロヒット)。Guillot の GT(G)/GT₁(G) は dessins・置換群経由の定義で、C1 の位置づけでは coarse 系。→ **項目 4(pentagon の機械計算例)には効かない**。項目 5 の系統整理と、「有限群 G ごとの GT(G) を置換群で明示する」という**別角度の計算手法**としてのみ価値。GT₁(PSL(2,q)) が「初等 abel 2 群 × D₈ の複数コピー」という完全決定は、工房の dihedral 予想線と機構的に近い(**D₈ が出てくるのは偶然か?** — 深読み観点その 3)。
- **C6**: 未取得。gentle 版の初出定義を原典で確認したい場合のみ必要(C1/2401.06870 の引用で足りる可能性大)。

---

## 6. 空振り・未達(負の結果)

- **未達 1**: Leila Schneps の 2 本の PDF(`webusers.imj-prg.fr/~leila.schneps/MIT3A.pdf` = "An introduction to Profinite Grothendieck-Teichmüller"、同 `SchnepsGT.pdf` = "ĜT: a survey")。**サーバが ECONNREFUSED / timeout(exit 28)で 2 回とも到達不能**。検索結果には出るがミラーは未発見。pentagon の**独立第二出典**としてはこれが第一候補だったので、後日再試行の価値あり。
- **未達 2**: Harbater–Schneps, Trans. AMS 352 (2000)(C6)。arXiv 版なし・AMS ペイウォール。
- **空振り 1**: arXiv:1904.06749 "The automorphism groups of the profinite braid groups" — 全文で "pentagon" ゼロヒット。破棄。
- **空振り 2**: Furusho の RIMS preprint 1357 — 取得できたのは 2 ページの表紙のみ。破棄。
- **空振り 3**: Furusho 系「pentagon ⇒ hexagon」(Ann. of Math. 171 (2010) 545–556 / Bar-Natan–Dancso arXiv:1010.0754)は **prounipotent 設定**。profinite/有限商では成り立たないことが C1 §4.3 の実測(35 例中 11 例のみ強 Furusho)で分かるので、**原論文を降ろす必要は薄い**(書誌のみ記録)。
- **空振り 4**: PackageGT の GitHub 版は存在しない。配布は Temple の zip のみ(旧 URL は死亡・生きた URL は 2106.06645 [7])。

### 使ったクエリ
1. `arxiv.org/abs/2008.00066`, `/abs/2106.06645`, `/abs/2401.06870`, `/abs/1407.3112`(直接取得)
2. "Grothendieck-Teichmuller group pentagon equation explicit relation pure braid group P4 definition GT hat"
3. "Drinfeld pentagon relation profinite GT hat f(x12,x23x24)f(x13x23,x34) pure braid generators"
4. `Guillot "GT-shadows" OR "Grothendieck-Teichmuller" coarse version GT0 finite quotients arXiv`
5. `"x12" "x23x24" pentagon relation GT hat Drinfeld profinite "f(x" braid P4 Schneps introduction`
6. `Dolgushev "package GT" GT-shadows software download github Temple PackageGT`
7. `Furusho "profinite Grothendieck-Teichmuller" GT hat pentagon equation explicit "F_2" three relations survey arXiv galois`
8. PDF 内 grep: `pentagon|hexagon`(2008 / 2106 / 1407.3112 / 1604.04415 / 1904.06749 / PackageGT README / PaB.py)

---

## 7. 金庫内ファイルと sha256

```
416c0a91ef7bbb2eb7b8e615d8d209083232965f1151c3e2832256110806784b  1407.3112.pdf
16a2496e4c4929570bbc8d330070dea92f0a08cb0d1dad01a2a9dbcee834cdea  1604.04415.pdf
c44eba890f83c1ac84a44a5b52fd5c6849250b242331d7eaaff9dd983167fb33  2008.00066v2.pdf
be6afb208b09d79716119fcb479bf74175a1c0ade1fa47d6c9727b01aa2d8f52  2106.06645v3.pdf
90545f5ea820b41c8bb16c5719c2540d39207f5247a4649fc4d784f1612468f1  PackageGT_README.pdf
c3124483cb1464b9010c091011370db091a76561a2af923a38efb6900f645f95  PackageGT.zip
```
補助: `2008.txt`, `2106.txt`, `1407.3112.txt`, `1604.04415.txt`(pdftotext -layout 抽出)、`pkg/PackageGT/`(zip 展開)。

採否・降ろし方(機構抽出+一工夫)の判断は司令塔の専権。本報告は判断を含まない。
