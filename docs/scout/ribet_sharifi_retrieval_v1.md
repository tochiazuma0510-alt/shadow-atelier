# 取り寄せ+トリアージ: Ribet–Sharifi 系(裁定 699 後の設計素材) v1

発注: 司令塔スペック(2026-08-06)。5 系統の正本を実在確認のうえ PDF を `papers/` へ配置し、書誌+一次トリアージのみ行う。**深読み・数学的評価はしていない**(禁止事項どおり)。トリアージ観点は発注文言のとおり2つ:
- (A) ρ̄_{Δ,691} の像(Borel 型・C₆₉₁ ⋊ ねじれ)の明示記述がどこにあるか
- (B) 窓構成に使える有限商の情報がどこにあるか

## 候補一覧

| # | 候補 | 識別子 | 年 | 実在確認 | 取得 | 該当箇所(暫定) |
|---|------|--------|----|----------|------|------------------|
| 1 | Ribet, A modular construction of unramified p-extensions of Q(μ_p) | Invent. Math. 34, 151–162 | 1976 | 確認済(著者サイトPDF直取得・Springer誌面と一致) | PDF取得済 | Thm 1.3 (p.152) = ρ̄ の明示的 Borel 型記述 |
| 2 | Mazur, Modular curves and the Eisenstein ideal | Publ. IHES 47, 33–186 | 1977 | 確認済(numdam実ページ・DOI一致) | PDF取得済(全186頁) | Eisenstein ideal 定義 = chap. II §9、Hecke環との辞書 = chap. II §6・(14.2) |
| 3 | Sharifi, A reciprocity map and the two-variable p-adic L-function | Ann. of Math. 173 (2011), 251–300 (= arXiv:0709.3591v3) | 2011 | 確認済(arXiv abstractページ・journal-ref一致) | PDF取得済(arXiv版) | §1.2「A special case」(p.3-4) = 明示的 φ_f: A_F^- ⊗μ_p → T_f^- ⊗μ_p、cup product↔p進L値の対応 |
| 4 | Wake–Wang-Erickson, The rank of Mazur's Eisenstein ideal | Duke Math. J. 169 (2020), 31–115 (= arXiv:1707.01894v3) | 2017/2020 | 確認済(arXiv abstractページ) | PDF取得済 | §1.2 Thm 1.2.1(cup product消滅⇔rank条件)、§1.3-1.4 Massey積・Newton多角形 |
| 5 | Brown, Depth-graded motivic multiple zeta values | arXiv:1301.3053v2 | 2013/2020 | 確認済(arXiv abstractページ) | PDF取得済 | §1.1 式(1.4) Ramanujan Δ の depth-4関係式(既知)、§1.3 depth-graded Lie環 𝔤^m の定義 |
| 6 | Pollack, Relations between derivations arising from modular forms(Duke卒論) | 未刊行(Duke, 2009) | 2009 | 確認済(DukeSpace実ページ・PDF直取得) | PDF取得済 | §2「Period polynomials of modular forms」(p.8) = ε_2m 関係式と周期多項式の対応の言明箇所 |

依頼 5 系統目は「Brown 1301.3053 + Pollack の関係式」の2本立てだったため、表では #5/#6 に分割した。

## 配置

`papers/` (リポジトリ外扱い・.gitignore対象、コミットはノートのみ):

- `ribet-1976-invent34-modular-construction-unramified-p-ext.pdf`
- `mazur-1977-ihes47-modular-curves-eisenstein-ideal.pdf`
- `sharifi-2011-annmath-reciprocity-map-two-variable-padic-L.pdf`
- `wake-wangerickson-2020-rank-mazur-eisenstein-ideal.pdf`
- `brown-2013-1301.3053-depth-graded-motivic-mzv.pdf`
- `pollack-2009-duke-thesis-relations-derivations-modular-forms.pdf`

sha256(取得直後に計算、再ダウンロード時の整合性チェック用):

```
ribet-1976-invent34-modular-construction-unramified-p-ext.pdf
  6985813b4026bb0fd7098aed3f816262e0922f62a5d2dab22e29bcc2eb323471
mazur-1977-ihes47-modular-curves-eisenstein-ideal.pdf
  ecaaf13790adf0ab037f4f36896eb1f3953f16aacd72985f35df111ccfa6f2a1
sharifi-2011-annmath-reciprocity-map-two-variable-padic-L.pdf
  e2528cca31f6440d09af390b28ac318fdb078be8d3373ae29d2de298377e0369
wake-wangerickson-2020-rank-mazur-eisenstein-ideal.pdf
  9d04e8f757f3527f11ac3f46400648747cc52ba30846c5478ac72e9a4602426e
brown-2013-1301.3053-depth-graded-motivic-mzv.pdf
  9c1998789966d4950b8a52ab0a26861bfc872e7e6908927d038715b27ace3d68
pollack-2009-duke-thesis-relations-derivations-modular-forms.pdf
  6508b6673a5ac01437c7433655508b7d95d320a989eb7d0d5509fd60ac9a207e
```

取得元URL:
- Ribet: https://math.berkeley.edu/~ribet/Articles/invent_34.pdf (著者本人サイト・Springer誌面画像1頁目と突合済)
- Mazur: https://www.numdam.org/item/10.1007/BF02684339.pdf (Numdam公式アーカイブ)
- Sharifi: https://arxiv.org/pdf/0709.3591 (v3, 2011-01-06)
- Wake–Wang-Erickson: https://arxiv.org/pdf/1707.01894 (v3, 2019-07-10)
- Brown: https://arxiv.org/pdf/1301.3053 (v2, 2020-01-10)
- Pollack: https://dukespace.lib.duke.edu/server/api/core/bitstreams/7ea21e50-913b-4816-b76c-b94293535a19/content

---

## 各候補の一次トリアージ

### 1. Ribet 1976, Invent. Math. 34, 151–162

**書誌**: Kenneth A. Ribet, "A Modular Construction of Unramified p-Extensions of Q(μ_p)", Inventiones mathematicae 34, 151–162 (1976).

**要旨(3-4行)**: p が不正則素数(p | B_k, 2≤k≤p-3偶数)のとき、Herbrand の逆(converse)を証明。すなわち p|B_k ⟹ イデアル類群の指標 χ^(1-k) 固有空間 C(χ^{1-k}) ≠ 0(補助仮定なしで)。証明はモジュラー形式の mod p 表現の構成による。

**なぜ効き得るか(機構ベース)**: **Thm 1.3 (p.152)** が観点(A)に直撃する — 「体 F ⊇ F_p と連続表現 ρ̄: Gal(Q̄/Q) → GL(2,F) が存在し、(i) p 以外で不分岐、(ii) ρ̄ は簡約可能で上三角 (1 * / 0 χ^{k-1}) 型(=Borel型)に同型、(iii) 像の位数は p で割れる(非対角化)、(iv) p での分解群への制限は対角化可能(位数はpと互いに素)」という4条件つきの**明示的 Borel 型表現構成**。窓構成(観点B)には Thm 1.2 の Galois 拡大 E/Q(μ_p) の (p,...,p) 型構造(有限 p-群による塔)が使える可能性。

**深読み時の照合観点**: Thm 1.3 の ρ̄ の「非対角化」条件と当工房の NFI_PB₃(B₃) 有限商の非可換性要求との対応。p=691 特化時に χ^{k-1} が Δ の691合同とどう結びつくか(§1 冒頭のBernoulli数条件 p|B_k との関係)。

**懸念**: 691 は p=691 として不正則素数(B_12 の分子)であり k=12 の場合に相当 — この論文の一般論(任意の不分岐p, k)を p=691, k=12 に特化する読み替えが必要。原論文自体は691を名指ししない一般論。

---

### 2. Mazur 1977, Publ. IHES 47, 33–186

**書誌**: Barry Mazur, "Modular curves and the Eisenstein ideal", Publications Mathématiques de l'I.H.É.S., tome 47 (1977), p. 33-186.(全186頁・大部のため章立てのみ)

**章立て(要点)**:
- Introduction(p.33-40): 主定理1-10の概観。Thm(1)=X_0(N)のtorsion部分のcyclic性(Ogg予想2)。
- Chap. I §1, §3: レベル構造・Shimura部分群。
- Chap. II §6: Hecke環T(Thm述べる箇所)。§8.10, §9: **Eisenstein ideal 𝕴 の定義**(central object、p.37 の spec図に予告あり)。§11: Shimura部分群との対応。§14.2: T の極大イデアルと簡約 Galois 表現の辞書(Thm 4 直後で言及)。§17.10: Eisenstein商 J̃ が J^- の商であることの証明。
- Chap. III §1, §3-6: Mordell-Weil群の決定・torsion分類(Thm 8=15群のリスト)。

**なぜ効き得るか(機構ベース)**: 観点(B)「窓構成に使える有限商」に直結——Eisenstein商 J̃ の Mordell-Weil 群が **Z/n**(n = numerator((N-1)/12))という**明示的巡回有限商**(Thm 4, chap.III (3.1))。当工房の「有限商での関係式チェック」設計と機構的に同型な操作(モジュラー曲線の有限商への射影→torsion群の完全決定)。観点(A)は間接的(Eisenstein ideal 自体はBorel表現の"reducible"側を特徴づけるが、明示的な691型の記述は本論文になく、Ribet 1976 やその後続(Wake–Wang-Erickson)で補完される構図)。

**深読み時の照合観点**: chap.II §9 の Eisenstein ideal 𝕴 の定義(Hecke作用素 T_ℓ - (1+ℓ) が生成)と、当工房の hexagon-only 生成系との類似性の有無。n = numerator((N-1)/12) の N=691 特化。

**懸念**: 全186頁と重量級。今回は書誌+章立てのみで PDF自体は取得済(15.9MB, numdam公式)だが該当節の精読は未実施。

---

### 3. Sharifi 2011, Ann. of Math. 173, 251–300 (= arXiv:0709.3591)

**書誌**: Romyar T. Sharifi, "A reciprocity map and the two-variable p-adic L-function", Annals of Mathematics 173 (2011), no.1, 251–300. arXiv版: 0709.3591v3(2011-01-06)。

**要旨(3-4行)**: p≥5 に対し、Q(μ_p) の p 以外で不分岐な最大拡大の Galois コホモロジーにおける cup 積の値と、Eisenstein級数と mod p 合同するモジュラー固有形式の p進L関数の値との関係を予想。cyclotomic塔とHida塔を渡る空間の同型を構成し、reciprocity写像の値と Mazur–Kitagawa の two-variable p進L関数の比較を与える。

**なぜ効き得るか(機構ベース)**: 観点(A)に**最も直接的**——**§1.2「A special case」(p.3-4)** が明示式そのもの。F=Q(μ_p)、cup積ペアリング (·,·): E_F × E_F → A_F ⊗ μ_p を定義し、weight2・level p・character ω^{k-2} の newform f に対し、その mod p 表現の格子(X_1(p) の第一エタールコホモロジー)から生じる **T_f への Galois 作用**が写像 A_F^- → Hom(T_f^+, T_f^-) を誘導、さらに φ_f: A_F^- ⊗μ_p → T_f^- ⊗μ_p を構成(式の直前)。これは Ribet の Borel型表現 ρ̄ の "±固有空間分解" 版にあたり、691 の場合の T_Δ^± の明示的取り扱いに転用できる可能性が高い。観点(B): §1.3「Summary of the conjectures」以降(未読部分)に一般の窓(Hida塔・cyclotomic塔)構成の記述があると推測される。

**深読み時の照合観点**: (1.1)式 φ_f((α_t, α_{k-t})) = c_{p,k}·L_p(f,ω^{t-1},1) の c_{p,k} の型と、当工房の窓構成での正規化定数との対応。T_f^± の複素共役固有空間分解が B₃-gentle 系のc中心元とどう対応しうるか(構造的類似のみ、直接対応の保証なし)。

**懸念**: 主定理群は「予想(conjecture)」であり証明された定理ではない(§1.1 で明記: "we propose a conjecture")。ただし §1.2 末尾に [Sh, Theorem 5.2] からの特殊化としての部分的証明の言及あり(t=1の場合)。

---

### 4. Wake–Wang-Erickson 2020, Duke Math. J. 169, 31–115 (= arXiv:1707.01894)

**書誌**: Preston Wake, Carl Wang-Erickson, "The rank of Mazur's Eisenstein ideal", Duke Mathematical Journal 169 (2020), no.1, 31-115. arXiv: 1707.01894v3(2019-07-10)。

**要旨(3-4行)**: pseudodeformation理論を用いて Mazur の Eisenstein ideal を研究。N,p を素数(p>3)とし、Γ_0(N) のweight2 Eisenstein極大イデアルでの Hecke環完備化 𝕋 の cuspidal商 𝕋^0 について、そのrank(および Newton多角形)を Galois コホモロジーの Massey積で完全に計算(Mazurの問題に解答、Calegari-Emerton結果の一般化)。

**なぜ効き得るか(機構ベース)**: 観点(A)(B)双方に効く——**Thm 1.2.1 (p.2)**: rank_{Z_p}(𝕋^0) ≥ 2 ⟺ cup積 b∪c が消滅 ⟺ cup積 a∪c が消滅、という**cup積による有限商rankの明示的判定条件**。§1.3「Higher rank and Massey products」(p.3)では2×2行列型のcocycle M と「matrix cup product」M∪M を導入し、これが当工房の C₆₉₁⋊ねじれ(半直積)構造の cocycle 記述と機構的に類似(観点A: Borel型2次元表現の非対角成分がcup積で統制される点)。§1.4 Thm 1.4.1 は 𝕋^0 の Newton多角形を Massey積の消滅パターンで完全決定——窓構成(観点B)に転用可能な「有限商の階層構造」の明示的記述。

**深読み時の照合観点**: p|N-1の場合の a,b,c ∈ H^1(Z[1/Np], Z/p^tZ(·)) の定義(Appendix B参照要)。Corollary 1.2.2 の類数条件 Cl(Q(N^{1/p}))[p] cyclic との対応。N=691型ケースへの特化可能性(N,pの役割が当工房のC_691の"691"とどちらに対応するか要確認 — 本論文は N=level, p=residual characteristicの一般論で、691がどちらの役割かは未確定)。

**懸念**: N,p は独立の素数パラメータ(N=level, p=Eisenstein素数)。当工房の p=691 特化がどちらの役割かは読み替えが必要(数学者委嘱事項、司令塔翻訳の一工夫が要る)。

---

### 5. Brown 2013/2020, arXiv:1301.3053(v2)

**書誌**: Francis Brown, "Depth-graded motivic multiple zeta values", arXiv:1301.3053v2(初版2013-01-14、改訂2020-01-10)。math.NT, MSC 11M32, 16T05, 13B05。

**要旨(3-4行)**: MZVのdepthフィルトレーション、Z上のmixed Tate motivesのmotivic Galois群、Grothendieck-Teichmüller群との関係を研究。SL_2(Z)のcusp formの周期多項式を用いてlinearized double shuffle方程式の解の明示的Lie環を構成、これがMZV間の(ζ(2)を法・より低いdepthを法とする)全恒等式の予想的記述を与える。このLie環のhomologyに関する単一の予想がBroadhurst-Kreimer, Racinet, Zagier, Drinfeldの予想を導く。

**なぜ効き得るか(機構ベース)**: 既に候補表にあり(発注文言のとおり)、司令塔メモにある通り GT Lie環との関係が主題。**§1.1式(1.4)(p.2)**: 28ζ(3,9)+150ζ(5,7)+168ζ(7,5) = (5197/691)ζ(12) — **691 が分母に明示的に現れる depth-4 関係式**(Ramanujan cusp form Δ (weight12) に対応)。**§1.3(p.3)**: motivic Lie環 𝔤^m の depth filtration 𝔇^r、その次数化 ∂𝔤^m = gr_𝔇 𝔤^m の定義。Thm 1.1: 𝔤^m は生成元σ_{2n+1}(各奇数次数)上の自由Lie環。

**なぜ効き得るか(観点A/B)**: 691という数値そのものが Δ の Eisenstein合同素数として (1.4)式に現れる点が、当工房の C_691 ⋊ ねじれ構造の**motivic側からの再現**の可能性を示唆(観点A)。§1.3の depth-graded Lie環の階層構造は窓構成(観点B)の候補になりうる。ただし GT Lie環側(pentagon等)は B₄系(pentagon あり)の枠組みであり、当工房のB₃-gentle系(hexagonのみ)への機構移送には**注意が必要**(混入札: B₄系)。

**懸念**: この論文の主眼はmotivic Galois群/GT Lie環(pentagon込みの本来系)であり、B₃-gentle系への直接適用ではない。「691」の出現は depth-4の"exceptional generator"としての一事例(p.2の議論)であり、当工房の p=691特化文脈とは独立起源(単なる数値の一致=Bernoulli数分子としての691がここでも表れているだけで、機構的接続は未確認)。

---

### 6. Pollack 2009, Duke卒論(未刊行)

**書誌**: Aaron Pollack, "Relations between Derivations Arising from Modular Forms", Thesis submitted to Department of Mathematics, Duke University, Durham, NC, 2009. 指導教員 R. Hain。DukeSpace所蔵(未刊行卒論・査読論文ではない)。

**要旨(3-4行)**: 自由Lie環 L(a,b)(H=Ca⊕Cb)上の導分 ε_{2m}(m≥0, ε_{2m}([a,b])=0, ε_{2m}(a)=ad(a)^{2m}(b))が生成するLie部分環 u の関係式を研究。(depth,weight)の二次数付けを導入し、depthはコミュテータ長と一致することを示す。主結果は §4「Proofs of Main Theorems」。

**なぜ効き得るか(機構ベース)**: **§2「Period polynomials of modular forms」(p.8、目次より)**が観点(A)(B)双方に関わる該当箇所——ε_{2m}間の関係式の係数が cusp form の周期多項式と結びつくという言明の所在(Brown 1301.3053 §1.1 の "Pollack's relations" 参照元)。この構造がFresse/Horel系のGT Lie環の生成子間関係(hexagon/pentagon)とどう対応するかは未読(深読み対象外)。

**懸念**: 未刊行の学部卒論であり査読を経ていない。数学的主張の信頼性は Brown 1301.3053 での引用("Pollack studied in his honours' thesis")によって間接的に裏付けられる程度。直接引用時は要注意(査読論文ではない旨を明記すべき)。

---

## 空振りだった角度・使ったクエリ

今回は司令塔スペックが「探すべき5系統」を明示指定していたため、標準の4角度検索(概念/機構/著者系譜/逆引き)は行わず、**直接の書誌検索**(WebSearch)+**実ページ実在確認**(WebFetch)+**PDF直接取得**(curl)の3段のみを実施。空振りなし——6件すべて初回検索で実在確認・取得に成功した。

使用クエリ(全6件・各1クエリで的中):
1. `Ribet "A modular construction of unramified p-extensions" Inventiones Mathematicae 1976 pdf`
2. `Mazur "Modular curves and the Eisenstein ideal" Publications IHES 47 1977 pdf`
3. `Sharifi "A reciprocity map and the two-variable p-adic L-function" Annals of Mathematics pdf arxiv`
4. `Wake Wang-Erickson "rank of Mazur's Eisenstein ideal" arxiv`
5. `arxiv 1301.3053 Brown depth-graded motivic multiple zeta values`
6. `Pollack thesis 2009 relations period polynomials cusp forms depth` → 補助クエリ `Aaron Pollack "Relations between derivations arising from modular forms" thesis pdf Duke`

**UNKNOWN規律に基づく明記**: 上記トリアージは表紙・目次・冒頭数頁(2-6頁分)の読解のみに基づく一次仕分けであり、各論文の該当節の精読(定理の正確な適用条件・691特化の妥当性)は未実施。特に Wake–Wang-Erickson の N,p 役割対応、Sharifi の予想部分と証明済み部分の切り分け、Brown/Pollack の GT Lie環(B₄系)と当工房B₃-gentle系との機構移送可能性は、数学者への降ろし判断時に司令塔が改めて精読・翻訳(一工夫)を要する。
