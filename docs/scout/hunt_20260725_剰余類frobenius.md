# hunt_20260725 — 剰余類 Frobenius(要請 4+5 合同出撃)

司令塔スペック: 有限群 Q(Δ(2,3,2k) の有限商)内で、A = [P,P] を走る f に対し
#{f ∈ A : (uf)³=1}, #{f ∈ A : (vf)²=1}, および両者の同時成立数。
欲しい型: (a) 剰余類指標公式 (b) 方程式解数の指標法 (c) 単純群での漸近正値性。

---

## 0. 困難の抽象化(3 通り)+ 当たり付けの理由

**抽象化 I — 「固定剰余類内の n 乗根の数え上げ」= 部分集合への射影付き Frobenius**
Frobenius の #{g : gⁿ=1} = Σ_χ ν_n(χ)χ(1)(ν_n = n 次 Frobenius–Schur 指標)は
台が G 全体であることに依存する。台を uA に絞る操作は、A ◁ Q かつ Q/A アーベル
(A = [P,P] なら P/A はアーベル。Q/A については要確認)ならば **剰余類の指示関数を
Irr(Q/A) の線型指標で展開する射影** で書ける:
  1_{uA}(g) = (|A|/|Q|) Σ_{λ ∈ Irr(Q/A)} λ(u)⁻¹ λ(g).
すると #{g ∈ uA : gⁿ=1} = (|A|/|Q|) Σ_λ λ(u)⁻¹ Σ_χ ν_n(λ⊗χ 的な捻り) …
つまり **「線型指標で捻った高次 Frobenius–Schur 指標」の和**。
→ 探索分野: **高次/捻れ Frobenius–Schur 指標**(Kawanaka–Matsuyama, Bump–Ginzburg,
Vinroot)・**剰余類上の指標論**(Dokchitser²)。n=2 のときこれは文字通り
「twisted FS 指標」そのもの — 分野一致でなく機構一致。

**抽象化 II — 「2 条件同時」= 固定元の (2,3)-分解数(構造定数)**
x := uf, y := vf と置くと f を消去でき、y x⁻¹ = v u⁻¹ =: w(固定)。よって
  #{f ∈ A : (uf)³=1 ∧ (vf)²=1} = #{(x,y) ∈ uA × vA : x³=1, y²=1, y x⁻¹ = w}.
これは **「固定元 w を 位数 3 元 × 位数 2 元 の積に書く方法の数」を剰余類で成層したもの**
= 三角群 Δ(2,3,m) → Q の準同型数え上げの局所版。古典の武器は Frobenius の
類乗積公式 |C₁||C₂|/|G| · Σ_χ χ(x)χ(y)χ(w⁻¹)/χ(1)。
→ 探索分野: **Fuchsian 群の表現多様体**(Liebeck–Shalev)・**三角群の有限単純商**
(Marion)・**word map / Waring**(Larsen–Shalev–Tiep)。困難が求める「正値性」は
まさにこれらの主定理の型(主項 |G|^{μ(Γ)+1} + 誤差)。

**抽象化 III — 「解数の合同・可除性」= 定数つき一階論理式の解数**
閉じた公式が取れなくても「≠ 0」を出すには可除性で十分な場合がある。
Frobenius 可除性(n | #{gⁿ=1})の現代的一般化は **定数を許す一階論理式の解数の
可除性**(Klyachko–Mkrtchyan → Brusyanskaya)。u, v は定数、f は変数 — 型が合う。
→ 探索分野: **組合せ論的群論の可除性定理**(Frobenius/Solomon/Iwasaki の統一)。
※ ただし「変数を部分群 A に制限」できるかは本文確認が要る(下表に照合観点)。

近場も禁じられていないので、上記 I は指標論の近場を意図的に含めた。

---

## 1. 候補表(8 件・全件 実在確認済み)

| # | 文献 | 実在確認 | 機構 |
|---|---|---|---|
| 1 | T. Dokchitser, V. Dokchitser, *Character formula for conjugacy classes in a coset*, **arXiv:2105.07247**, DOI **10.4171/ECR/20**(Arithmetic of L-Functions, ICMAT 2023 会議録) | abs ページ取得済 | G/N アーベルのとき、剰余類 qN 内の共役類と「qN 上恒等的に 0 でない Irr(G)」の対応 |
| 2 | N. Kawanaka, H. Matsuyama, *A twisted version of the Frobenius–Schur indicator and multiplicity-free permutation representations*, Hokkaido Math. J. **19** (1990) no.3, DOI **10.14492/hokmj/1381517495** | Project Euclid ページ取得済 | ε_ι(χ) = (1/|G|)Σ χ(g ι(g)) — 「捻れた対合」の数え上げの指標公式 |
| 3 | C. R. Vinroot, *Twisted Frobenius–Schur indicators of finite symplectic groups*(+ *On involutions and indicators of finite orthogonal groups*, J. Austral. Math. Soc.) | math.wm.edu の PDF 実在・Cambridge Core ページ実在 | 捻れ指標の**実計算例**。指標和が「指数 2 の 2 つの剰余類に分割される」形で使われる |
| 4 | M. W. Liebeck, A. Shalev, *Fuchsian groups, finite simple groups and representation varieties*, Invent. Math. **159** (2005) 317–367, DOI **10.1007/s00222-004-0390-3** | 著者サイト PDF (ma.imperial.ac.uk/~mwl/fuchslie.pdf) を実取得(314KB)。Springer 抄録は認証壁 | |Hom(Γ,G)| = |G|^{μ(Γ)+1+o(1)}。指標比評価で **解数 > 0** を出す標準機構 |
| 5 | M. W. Liebeck, *Applications of character theory of finite simple groups*(サーベイ, ma.imperial.ac.uk/~mwl/cib-survey.pdf) | PDF 実在確認 | 類乗積公式 → 生成・被覆数・word map の正値性へ至る道具立ての目録 |
| 6 | C. Marion, *Deformation theory and finite simple quotients of triangle groups* **I / II**, **arXiv:1301.2949 / 1301.2955** | 両 abs ページ実在 | T(a,b,c) = ⟨x,y,z | xᵃ=yᵇ=z^c=xyz=1⟩ の有限商。**(2,3,k) がまさに主戦場** |
| 7 | M. Larsen, A. Shalev, P. H. Tiep, *The Waring problem for finite quasisimple groups*, **arXiv:1107.3341**(+ *A Refined Waring Problem*, **arXiv:1312.4998**) | abs 取得済 | word map の像の積で全元を覆う — 「解数 > 0」の最強型の定理群 |
| 8 | (可除性系) Brusyanskaya, *On the number of tuples of group elements satisfying a first-order formula*, **arXiv:2306.16498**, J. Group Theory (DOI 10.1515/jgth-2023-0111) / Klyachko et al., *What do Frobenius's, Solomon's, and Iwasaki's theorems ... have in common?*, **arXiv:1806.08870**, Pacific J. Math. **302** (2019) no.2 | 両 abs 取得済・PJM 目次ページ実在 | **定数を含む一階論理式**の解数の可除性。u, v を定数、f を変数とする型に文法上合致 |

補助(古典・二次資料): P. X. Gallagher, *Group characters and normal Hall subgroups*,
Nagoya Math. J. **21** (1962) 223–230(Project Euclid PDF 実在)。Amit–Vishne,
*Characters and solutions to equations in finite groups*, J. Algebra Appl. **10** (2011)
675–686, DOI 10.1142/S0219498811004690(word の解数が指標/仮想指標になる条件)。

---

## 2. 機構評・当工房への翻訳可能性・深読み時の照合観点

**#1 Dokchitser²** — 最も型が近い。Q/A がアーベルなら uA 内の共役類構造が
Irr(Q) の「uA 上の非消滅」で制御される。翻訳: 抽象化 I の射影公式の**共役類側の相方**。
照合観点: (i) 定理は G/N アーベルを仮定するか巡回のみか。(ii) 「qN 上 0 でない χ」の
判定が計算可能か(GAP の CharacterTable で直接引けるか)。(iii) 剰余類内**元数**の
公式まで書いてあるか、それとも**類の個数**止まりか(後者なら射影公式は自作要)。

**#2 Kawanaka–Matsuyama + #3 Vinroot** — n = 2 の場合の剰余類版はこれで実質解決の
可能性。ι(g) = w g w⁻¹ 型ではなく、指数 2 の拡大 G ⊃ N で「外側剰余類の対合数
= Σ 捻れ指標 × 次数」という形が標準。翻訳: v A が Q の指数 2(あるいは Q/A の
位数 2 の元)に対応するときそのまま適用。一般の |Q/A| ではアーベル群 Q/A の
線型指標和に一般化する必要 — その一般化は初等的で、当工房で自作できる。
照合観点: 捻れ指標の定義が「反自己同型 ι」ベースか「自己同型 σ」ベースか、
剰余類版に翻訳する際どちらの ι を取るか。

**#4/#5 Liebeck–Shalev** — 「同時成立数 > 0」の要請 (c) に直撃。機構は
Σ_χ (|C₂||C₃|/χ(1)) χ 比の評価で自明指標項が主項として残ることを示す型。
翻訳: 当工房の Q は単純群でないので**漸近定理はそのままでは効かない**が、
「主項 + 誤差の指標比評価」という**証明の骨格**は有限商 Q でも回る(誤差項が
Σ_{χ≠1} で押さえられるか否かが勝負)。照合観点: 位数 2・位数 3 の**類**を固定した
版の主項の形、および Q が可解/冪零のとき誤差評価が壊れる箇所。

**#6 Marion** — 対象そのものが (2,3,k) 三角群の商。当工房の Δ(2,3,2k) 有限商と
同じ族。翻訳: 彼の「rigid / 剛性」条件が当工房の hexagon のみ・pentagon なしの
制約とどう対応するかが核心の翻訳作業。照合観点: 剛性判定が Lie 型に限るか、
一般有限群でも使える形の補題があるか。

**#7 LST Waring** — 「解が存在する」の最強形。翻訳可能性は低め(準単純が前提)だが、
**「2 値の積で全元」型の言明が (2,3) 分解の存在保証に読み替わる**点が有用。
照合観点: 語 w を x² と x³ に取ったときの明示的な大きさの閾値。

**#8 可除性系** — 閉じた公式が出ないとき「解数 ≠ 0」を mod で出す退路。
翻訳: 変数 f を A に制限したい。定数は許されるので (uf)³=1 は書けるが、
「f ∈ A」という制約が一階論理式(定数つき)で表現できるかが分岐点。
照合観点: 定理の可除量が gcd(何, |G|) か、制約部分群があるとき何が残るか。

---

## 3. 総括(公式の有無)

- **完全に閉じた「剰余類版 Frobenius 公式」を主定理として掲げた文献は見つからなかった。**
- ただし n = 2 の剰余類版は **捻れ Frobenius–Schur 指標(#2/#3)として実質存在**。
- 一般 n の剰余類版は、抽象化 I の線型指標射影で **初等的に自作可能**(Q/A アーベル前提)。
  文献はその部品(#1 の共役類側、#2 の n=2 側)を供給する。
- 同時成立数は **類乗積公式の剰余類成層版**として書ける(#4/#5 の骨格)。正値性は
  単純群では #4/#7 が保証、当工房の Q では誤差評価の再検討が必要。

## 4. 空振りの当たりと使ったクエリ(負の結果)

**空振り 1: Gallagher の「剰余類指標和」を主定理とする論文** — スペックが示唆した
Gallagher は Nagoya 1962(Hall 部分群への指標の拡張)が実体で、剰余類内の**元数**を
数える公式ではなかった。二次文献が引く「Gallagher の補題」は Σ_{Hg} |χ(x)|² = |H|
(χ|_H が既約なとき)で、位数条件つき数え上げではない。要請 (a) の直接の解にはならない。
クエリ: `Gallagher character sums cosets number of elements of order n in a coset` /
`Gallagher 1965 "group characters and normal Hall subgroups" coset character sum lemma`

**空振り 2: 「x^n = 1 in a coset」の直接検索** — Frobenius の一般化として出てくるのは
M. Hall の x^n = c(c が類を走る)版と Frobenius 予想であって、剰余類制限版ではない。
クエリ: `Frobenius theorem number of solutions g^n=1 in a coset of a normal subgroup
character formula` / `generalization Frobenius theorem "in a coset" number of solutions
x^n=1 divisibility normal subgroup arXiv`

**空振り 3: arXiv:2605.22127**(Twisted FS indicators and character degree sums in
dihedral groups)— 題名は魅力的だが、内容は T(G) ≥ m_σ の不等式であり剰余類の
位数 n 元の数え上げ公式ではない。dihedral という語の一致に釣られた例(機構不一致)。
クエリ: `twisted Frobenius-Schur indicator Kawanaka Matsuyama counting involutions in a coset`

**空振り 4: MathOverflow の直接質問** — 該当スレッドを検索で拾えず(検索エンジン経由)。
クエリ: `mathoverflow number of elements of order n in a coset xN character formula
linear characters twisted indicator`

**その他使用クエリ**: `Solomon "solution of equations in groups" 1969 ... nu_n(chi)` /
`Liebeck Shalev "Fuchsian groups" ... character sum` / `Liebeck Shalev "(2,3)-generation"
... character ratio positivity` / `Larsen Shalev Tiep "Waring problem" word maps` /
`Frobenius formula number of homomorphisms triangle group prescribed conjugacy classes` /
`Claude Marion triangle groups (2,3,k) generation ... arXiv`

**UNVERIFIED 申告**: なし(全候補で abs ページまたは PDF を実取得)。ただし
Liebeck–Shalev の Springer 抄録ページは認証壁で直接取得不可 — 巻号頁は検索結果と
著者サイト PDF の存在で裏取りした二次確認である旨を明記する。
