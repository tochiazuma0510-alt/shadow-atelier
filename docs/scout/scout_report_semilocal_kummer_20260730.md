# 遠征報告 — 半局所 Kummer 不変量(非全分岐 cusp での主係数の類)

- 日付: 2026-07-30 / 文献ゲート① / 裁定 217 発スペック
- 出力: 金庫内(リポジトリ外)。採否判断・数学者への配達は行っていない。
- 実在確認: 全 10 件、arXiv abs ページ / numdam / 出版社レコードの実取得で確認済み(UNVERIFIED なし)。

---

## 0. 困難の抽象化(当たり付け)

司令塔スペックの困難を、分野非依存の機構語に 4 通り翻訳した(規定は 3 通り以上)。

### 抽象化 A — 「1 点の Kummer 類」→「有限エタール K-代数上の Kummer 類 + ノルム」
cusp 集合 λ⁻¹(0) は K-有理点ではなく**有限エタール K-代数 E**(点が複数・共役で動く)。
各点の主係数 u は E^×/E^{×M} の元であり、K 上の不変量にするには E^×→K^× のノルム(= Weil 制限トーラス R_{E/K}𝔾_m → 𝔾_m)を通す以外に正準な写像がない。
つまり「どう束ねるか」は選択でなく **corestriction/ノルム関手の一意性定理**の問題。
→ 探索分野: 可換代数のノルム関手・Weil 制限・エタール代数による H¹ の記述。

### 抽象化 B — 「主係数 = 接ベクトル」→ tangential base point の非有理版
局所展開 λ = u·s^M(1+…) の u は、cusp における**接ベクトル(tangential base point)の選択**そのもの。uniformizer 変更 = 接ベクトルの μ_M-捻り。
全分岐なら単点上の μ_M-torsor で閉じるが、非全分岐・複数点では torsor が **E 上に載る(誘導加群 Ind の形)** — 不変量は Shapiro 経由で corestriction に落ちる。
→ 探索分野: 対数幾何(log 構造による接基点の正準化)・Deligne の tangential base point・境界(cuspidal)切断の理論。

### 抽象化 C — 「主係数の曖昧さ」= field of moduli vs field of definition の局所版
u の類が well-defined でないという現象は、被覆の**降下障害**の局所成分。
Dèbes–Douai の枠組みでは障害は H²(K, Z(Aut)) 値、非 Galois 被覆では複数の特性類。
「点を marked する(= cusp を区別する)と降下が改善する」という現象が既知。我々の設定は「cusp を marked した被覆の降下」に相当。
→ 探索分野: 被覆の降下理論・Hurwitz/descent variety・marked curve の explicit descent。

### 抽象化 D — 「Z/N⋊(Z/N)^× 値表現」= 二項式 x^n − a の分裂体
holomorph 値 Galois 表現は、抽象的には**radical(二項式)拡大の Galois 群**そのもの。捻れつき指標「単数 mod N 冪」対応は、二項式の分裂体の構造定理として古典的に完備。局所の分岐(高次分岐群・conductor)も計算されている。
→ 探索分野: 代数的整数論の radical extension 理論(Vélez 学派)・Hopf-Galois/holomorph 文献。

### 抽象化 E(補・近場)— cusp 束の単一軌道化 = DM スタック化
複数 cusp を正規化群/対称群で割ると divisor は**単一の stacky 点**になり、分岐指数 M は自己同型 μ_M として吸収される(root stack)。
これは「多点 → 単点還元」の幾何的処方であり、標的型 3 の直訳。**非彩色ブレイド群 B_n が DM スタックの π₁ になる**という構図がまさにこれ(我々の B₃ 設定と地続き)。
→ 探索分野: root stack・divisorial inertia の cyclotomic 作用・profinite braid group の算術。

---

## 1. 候補表(10 件)

| # | 書誌 | ID/DOI | 主張の型 | 抽象化 | 距離 |
|---|---|---|---|---|---|
| 1 | E. M. O'Dorney, "Étale algebras and the Kummer theory of finite Galois modules" (2025) | arXiv:2506.11310 | H¹(K,M) ↔ Gal ⊂ Hol M = M⋊Aut M のエタール代数辞書 | A,D | **近** |
| 2 | E. T. Jacobson, W. Y. Vélez, "The Galois group of a radical extension of the rationals", manuscripta math. 67 (1990) 271–284 | DOI 10.1007/BF02568433 | x^n−a の分裂体の Galois 群を holomorph の部分群として明示 | D | **近** |
| 3 | F. Viviani, "Ramification groups and Artin conductors of radical extensions of ℚ", JTNB 16 (2004) 779–816 | arXiv:math/0409533 | radical 拡大の高次分岐群・conductor(非整数跳躍) | D | 中 |
| 4 | P. Dèbes, J.-C. Douai, "Algebraic covers: field of moduli versus field of definition", Ann. Sci. ÉNS 30 (1997) 303–338 | DOI 10.1016/s0012-9593(97)89922-3 | 降下障害 = H²(K,Z(G)) 群(非 Galois は複数類)・局所大域原理 | C | **近** |
| 5 | A. Molyakov, "On the fields of definition of genus-one covers of P¹", BLMS (2023) | arXiv:2204.12594 | 定義体/moduli 体の次数は非有界・Belyi pair の局所大域反例 | C | 中(陰性較正) |
| 6 | J. Sijsling, J. Voight, "On explicit descent of marked curves and maps" (2015) | arXiv:1504.02814 | marked(区別点つき)three-point cover は moduli 体上に降下する | C,B | **近** |
| 7 | F. Callegaro, G. Gaiffi, P. Lochak, "Garside elements, inertia and Galois action on braid groups" (2016) | arXiv:1507.07208 | divisorial inertia への cyclotomic 作用・非彩色ブレイド群/DM スタック | E,B | **近** |
| 8 | C. Dupont, E. Panzer, B. Pym, "Logarithmic morphisms, tangential basepoints, and little disks" (2024/2026 rev) | arXiv:2408.13108 | log 幾何の virtual morphism = 接基点の正準化。parenthesized braids が π₁ として出る | B,E | **近** |
| 9 | N. Borne, M. Emsalem, J. Stix, "Lifting Galois sections along torsors", Math. Nachr. | arXiv:1301.4429, DOI 10.1002/mana.201400251 | 境界の **packet**(共役で束ねた cusp 群)と**トーラス torsor**による持ち上げ | A,B | **近** |
| 10 | D. Ferrand, "Un foncteur norme", Bull. SMF 126 (1998) 1–49 | DOI 10.24033/bsmf.2319 | 有限局所自由代数上の対象に対するノルム関手の構成と一意性 | A | 中(基盤) |

(補: Stix, "On cuspidal sections of algebraic fundamental groups", arXiv:0809.0017 — 境界切断を Kummer 理論で作る先行論文。#9 の前身として同時参照推奨。実在確認済み。)

---

## 2. 各候補の機構ベース評・翻訳可能性

### #1 O'Dorney arXiv:2506.11310
機構: H¹(K,M) の元 ⇄ Gal が Hol M = M⋊Aut M に入るエタール代数、という辞書を**組合せ的細部まで書き下す**ことを目的にした論文(著者自身が「広く使われているのに書かれたことがない」と述べる隙間埋め)。
翻訳: 我々の Z/N⋊(Z/N)^× 値表現は M = Z/N の Hol そのもの。[u] ∈ K^×/K^{×M} を「エタール代数の同型類」に翻訳すると、複数 cusp の状況は**分解型のエタール代数**(積分解)として自然に入る — 「点をどう束ねるか」が代数の直積成分の話に還元される可能性。
照合観点: (a) M が非自明 Galois 加群(捻れ)のときの Hol の記述、(b) H¹ の元とエタール代数の分解の対応辞書が我々の cusp 分解と一致するか、(c) Tate pairing の記述が我々の「積/ノルム」処方の正準性を与えるか。

### #2 Jacobson–Vélez (DOI 10.1007/BF02568433)
機構: 二項式 x^n − a の分裂体の Galois 群を、a の「n 冪の割れ方」で完全に決定し holomorph の部分群として明示。
翻訳: 標的型 2 の**古典的完成形**。我々の「捻れつき指標 = 単数 mod N 冪」対応が、この定理の言い換えである可能性が高い(逆に言えば新規性主張の前に必ず突き合わせるべき文献)。
照合観点: a の類 [u] ∈ K^×/K^{×M} と像群の対応表。特に M が合成数・K に ζ_M が入らない場合の場合分け。

### #3 Viviani arXiv:math/0409533
機構: radical 拡大の高次分岐群と Artin conductor を計算。Hasse–Arf に反する非整数跳躍が起きる。
翻訳: 主係数 [u] の**局所情報**(どの素点でどう分岐するか)を conductor という数値不変量で読む処方。半局所束ね方の正準性を「conductor が加法的か」で検定できる可能性。
照合観点: 我々の cusp 分岐指数 M と conductor 公式の対応。discriminant の conductor-discriminant 公式が「積で束ねる」処方を正当化するか。

### #4 Dèbes–Douai (ASENS 1997)
機構: 被覆の moduli 体 vs 定義体の差を H²(K, Z(G)) 値障害で測る。非 Galois 被覆では**単一の類でなく複数の特性類**で制御される。G-被覆については局所大域原理(各 ℚ_p で定義できれば ℚ で定義できる)。
翻訳: 「多点の u をどう束ねるか」の非一意性は、**非 Galois 被覆で障害が複数類になる現象と同型**の可能性が高い。すなわち正準な単一処方は一般には存在せず、cusp ごとの類の族が正しい不変量であり得る(= 束ねる必要がない、という別解)。
照合観点: Z(Aut(cover)) が我々の設定で何になるか。μ_M か、それとも cusp 置換で捻られた誘導加群か。後者なら「ノルムを取る」が corestriction として自動的に出る。

### #5 Molyakov arXiv:2204.12594
機構: 定義体の moduli 体上の次数がいくらでも大きくなる Belyi pair を構成、局所大域原理の反例。
翻訳: **陰性側の較正**。もし我々が「半局所不変量が全情報を捉える」型の主張に向かうなら、この構成が反例になるか要検定。逆に我々の設定(genus 0・B₃ gentle・可換 μ_M)がこの反例の外にいることを示せれば、well-defined 化の見込みが立つ。
照合観点: 反例の genus 1 性・自己同型群の非可換性が本質かどうか。

### #6 Sijsling–Voight arXiv:1504.02814
機構: **marked**(区別された点を持つ)曲線・写像は moduli 体上に降下する、という定理と明示的アルゴリズム。
翻訳: 標的型 3 に最も直結。「cusp を区別する(marked にする)」ことで降下障害が消えるなら、[u] は marked 被覆の不変量として自動的に well-defined になる。多点問題は「どの点を mark するか」の選択に還元され、選択の族は Aut/正規化群の軌道で統制される。
照合観点: marked の定義が「1 点」か「点の集合」か。集合を mark した場合の定理の形。three-point ramified cover に限定されているのは我々の Belyi 設定と一致。

### #7 Callegaro–Gaiffi–Lochak arXiv:1507.07208
機構: 幾何的基本群の**divisorial inertia が cyclotomic に作用する**という事実を、複素鏡映群由来の副有限ブレイド群で明示。非彩色(full)ブレイド群は分類空間が**スキームでなく DM スタック**になる場合として別扱い。
翻訳: 抽象化 E の実装。我々の非全分岐 cusp = 「彩色を落とした(点を区別しない)divisor」であり、cyclotomic 作用は Garside 元(Δ²、B₃ では中心 c!)の共役類で記述される。**c 中心の我々の設定と語彙が一致**するのが最大の魅力。u の類は「Garside 元の inertia 生成元に対する cyclotomic 指標の値」として読み替えられる見込み。
照合観点: Δ²(= 我々の c)に対する inertia の記述と、hexagon のみ・pentagon なしの gentle 設定で対応する式。DM スタック補正項が「多点束ね」の正準処方を与えるか。

### #8 Dupont–Panzer–Pym arXiv:2408.13108
機構: log スキームの **virtual morphism** を定義し、Deligne の tangential base point を「点からの virtual morphism」として正準化。副産物として parenthesized braids がモジュライ空間の基本亜群として現れる。
翻訳: 「主係数 u の well-defined 性」は結局「接基点の正準な選び方」であり、log 構造は**まさに uniformizer の選択を構造として持ち込む**装置。非全分岐・多点では log 構造が divisor 全体(non-reduced 可)に載るので、単点に閉じない状況を最初から扱える。GT/B₃ 語彙(parenthesized braids)で書かれている点で翻訳コストが低い。
照合観点: log 構造つき divisor に対する接基点の torsor が μ_M^{(点数)} か、それとも ind-加群か。後者なら「積で束ねる」= log 構造の大域切断を取る操作として正当化される。

### #9 Borne–Emsalem–Stix arXiv:1301.4429(+ 0809.0017)
機構: 境界の **packet**(1 つの閉点上の共役な cuspidal 切断の束)という概念と、**トーラス torsor** による切断の持ち上げ。ℚ 上ではねじれ部分 packet について持ち上げが常に可能。
翻訳: packet = 我々の「λ⁻¹(0) の共役で束ねられた cusp 群」そのもの。トーラス torsor は Weil 制限トーラス R_{E/K}𝔾_m/𝔾_m 型であり、**「ノルムで束ねる」処方がここで幾何的に正当化されている**可能性が最も高い候補。
照合観点: packet の定義と、packet 上の Kummer 理論(0809.0017 の boundary section 構成)。torsor が 𝔾_m の Weil 制限か、ノルム 1 トーラスか — 後者なら我々の [u] はノルム 1 部分での不変量になる。

### #10 Ferrand, "Un foncteur norme" (DOI 10.24033/bsmf.2319)
機構: 有限局所自由代数拡大に沿ったノルム関手の一般構成と、その普遍性・一意性。
翻訳: 「積で束ねる/ノルムで束ねる」処方が**関手として一意に決まる**ことの基盤文献。標的型 1 の「正準な処方が要る」に対する存在・一意性の土台。単独では我々の問題を解かないが、他候補の処方が「正準」と言えるかの判定基準を与える。
照合観点: 非 Galois・非分離でない有限エタール E/K に対するノルムの一意性主張の正確な形。μ_M 係数(乗法群の M-捻り)への持ち上げが関手的か。

---

## 3. 空振りの当たり・使ったクエリ(負の結果)

### 空振りした当たり
- **Weil 相互律 / tame symbol 方向**: 「主係数の全点にわたる積 = 1」型の相互律を期待したが、ヒットしたのは古典 Weil reciprocity と熱帯化・反復積分版(arXiv:1206.5817, 2408.06372, 1905.11774)で、**分岐被覆の cusp data と結ぶ論文は出ず**。機構としては筋が良い(局所記号の積 = 1 は「束ね方の正準性」の原型)が、既製の理論はない模様。司令塔判断で再遠征の価値あり。
- **root stack 方向**: 「M 乗根を取る = 多点を単一 stacky 点に還元」の当たりで検索したが、ヒットは Gromov–Witten・parabolic bundle・twisted curve 系で、**算術的不変量([u] の類)を扱うものに届かず**。#7 の DM スタック言及の方が近い。
- **modular curve の cusp の Galois 作用**: q 展開の先頭係数と (Z/N)^× 作用を狙ったが、出たのは標準的な X(N) の cusp 作用の教科書的記述(Sage doc, Sharifi ノート等)で、**「先頭係数の類」を不変量として切り出す文献は見当たらず**。
- **Kummer covers with arbitrary ramification**(arXiv:2605.14046, LCP 符号): 非全分岐点を扱うが目的が符号理論の非特殊因子構成で、**機構の移送性はほぼゼロ**と判断し候補から除外。
- **Hurwitz space + 接基点の marked 版**: 「分岐点に接ベクトルを marked した Hurwitz 空間」を狙ったが、該当する定式化は見つからず(#6 の marked curve が最も近い代替)。

### 使ったクエリ(全 12 本)
1. local invariants leading coefficient branched covers of P^1 non totally ramified cusp Kummer class
2. Belyi map field of moduli field of definition local obstruction branch cycle description inertia leading coefficient
3. tame symbol Weil reciprocity leading coefficient uniformizer independence product over points covering curve
4. Kummer theory metacyclic extensions holomorph Z/N semidirect (Z/N)^* Galois representation classification twisted
5. arXiv "Etale algebras and the Kummer theory of finite Galois modules" holomorph
6. Debes Douai field of moduli obstruction cover local-global H^2 center automorphism group
7. tangential base point Galois action torsor of tangent vectors cusp Kummer character comparison ramification cover
8. Galois action on cusps of modular curves q-expansion leading coefficient field of definition (Z/N)^* semidirect
9. corestriction norm map Weil restriction semi-local Kummer classes finite etale algebra points above a place descent invariant
10. root stack ramification divisor M-th root of line bundle section Kummer cover well-defined
11. twists of Belyi maps covers of P^1 quadratic twist Kummer class classification of twists dessins Galois descent
12. Galois group of radical extension x^n - a subgroup holomorph Z/n rtimes (Z/n)^* classification which subgroups arise
（+ Hurwitz space marked tangential base point 系・Nakamura Galois rigidity 系の 2 本）

### 実在確認の方法
arXiv abs ページ実取得: 2506.11310 / 1507.07208 / 2204.12594 / math/0409533 / 1504.02814 / 2408.13108 / 1301.4429 / 0809.0017。
numdam レコード実取得: ASENS_1997_4_30_3_303_0(Dèbes–Douai, DOI 10.1016/s0012-9593(97)89922-3)/ BSMF_1998__126_1_1_0(Ferrand, DOI 10.24033/bsmf.2319)。
Springer は認証壁のため abs 直取得不可 → EUDML/Arizona 業績レコードで著者・巻号頁・DOI を交叉確認(Jacobson–Vélez, manuscripta math. 67 (1990) 271–284, DOI 10.1007/BF02568433)。
**UNVERIFIED は 0 件。**
