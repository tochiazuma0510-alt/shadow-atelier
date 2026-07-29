# hunt_20260730_structthm — 「なぜ必ず ε=0 か」遠征報告

論文遠征係(文献ゲート①・裁定 211 スペック)。採否判断は含まない。

## 0. 困難の抽象化(当たり付けの理由)

司令塔スペックの困難を、分野非依存の機構語に 3 通り翻訳した。

**抽象化 A(採った主線): 「D₈ = 位数 8 の extraspecial 2-群」と読み替える。**
Z(D₈) ≅ C₂ で D₈/Z ≅ C₂² は symplectic な F₂-空間。すると
1 → Z(D₈) → C_G(D₈) → G/D₈ → 1 は、**extraspecial 2-群の自己同型拡大(normalizer 拡大)が分裂するか**という古典問題の相対版になる。
この問題は群論では Griess(1973)、量子情報では **Clifford 群 = 有限 Heisenberg 群 ⋊ Sp** の分裂問題として独立に発達している。決定的なのは、そこでの答えが
**「分裂 ⟺ 4 ∤ |A|」**、特に **|A| 奇 ⇒ 障害類が恒等的に消える**、という形をしていること。
当工房の設定は N 奇。**「三例すべてで ε=0」は偶然でなく odd-order 型の一般定理の影である可能性**が最も高い、と当たりを付けた。導いた探索分野: 有限群論(extraspecial p-群)+ **量子情報(Clifford 群 / stabilizer 形式)**。

**抽象化 B: 「Q が abelian のとき ε は二次形式」。**
Q=(ℤ/N)^× の 2 部分は elementary abelian に近く、C₂ 係数の中心拡大は **quadratic map Q(x)=x̃²** と一対一。ε=0 ⟺ **Q の各元が位数 2 の元に持ち上がる**。したがって「なぜ分裂か」は「**なぜ各元が対合に持ち上がるか**」に等しく、複素共役(位数 2)の存在という標的 1 と同じ問いに合流する。導いた探索分野: 二次写像と 2-群コホモロジー(Pakianathan–Yalçın 型)、および Gaschütz の補元定理(素数ごとの Sylow への還元)。

**抽象化 C: 「対合が有限商へ位数 2 のまま降りる」= 実構造 / Artin–Schreier 型の剛性。**
副有限群で「位数 2 の元」が消えずに残り、しかもその中心化群が自分自身になるという現象は、絶対 Galois 群では Artin–Schreier 定理(有限部分群は位数 ≤2・不動体は実閉)として厳密な剛性定理になっている。実 section 予想(Pál)は「対合 ⟺ 実点」という**分裂の幾何的理由**を与える型。導いた探索分野: 実代数幾何 / anabelian(実 section 予想)・quandle 不変量。

## 1. 候補表(当たりの強い順・8 本)

| # | 書誌 | 主張の型 | 当工房との距離 | 入手 |
|---|---|---|---|---|
| 1 | C. Galindo, *Splitting of Clifford groups associated to finite abelian groups*, arXiv:**2603.24743** (2026-03-25) | Thm 1.1「Clifford 拡大が半直積に分裂 ⟺ 4∤\|A\|」。**Prop 3.2「\|A\| 奇 ⇒ 障害類消滅」** | 近(機構) | arXiv 全文(HTML 確認済) |
| 2 | M. Korbelář, J. Tolar, *Clifford group is not a semidirect product in dimensions N divisible by four*, arXiv:**2305.13178**, J. Phys. A **56** (2023) 275304 | 巡回の場合。SL(2,ℤ_N) の表示から分裂準同型の存在/非存在を決定 | 近(手法が明示的・移植しやすい) | arXiv+雑誌 |
| 3 | R. L. Griess Jr., *Automorphisms of extra special groups and nonvanishing degree 2 cohomology*, Pacific J. Math. **48**(2) (1973) 403–422 | extraspecial 群の自己同型拡大の H² 障害の消滅/非消滅の**正典** | 中(D₈ = extraspecial 2-群の n=1) | Project Euclid(euclid.pjm/1102945424 で実ページ確認。DOI 文字列は未確認) |
| 4 | J. Pakianathan, E. Yalçın, *Quadratic maps and Bockstein closed group extensions*, arXiv:**math/0606374** | elementary abelian 2-群の中心拡大 ⟷ 二次写像 Q(w)=w̃² の一対一対応・Bockstein 閉性 | 中(ε の計算装置。抽象化 B の道具) | arXiv |
| 5 | P. Guillot, *The Grothendieck–Teichmüller group of PSL(2,q)*, arXiv:**1604.04415** / 同 *…of a finite group and G-dessins d'enfants*, arXiv:**1407.3112** | GT₁(PSL(2,q)) ≅ (elementary abelian 2-群) × **(位数 8 の二面体群のコピー数個)**。q 偶なら自明 | 近(現象が同型。ただし GT の別定式化) | arXiv |
| 6 | F. R. Beyl, *The Schur multiplicator of metacyclic groups*, Proc. AMS **40** (1973) 413–418 | 有限 metacyclic 群の Schur 乗数は巡回・位数の明示式 | 中(標的 3: Hol(ℤ/N) が metacyclic な場合の中心拡大分類) | 雑誌。**DOI 10.2307/2039383 は検索要約由来で実ページ未確認(UNVERIFIED)** |
| 7 | A. Pál, *The real section conjecture and Smith's fixed point theorem for pro-spaces*, arXiv:**0905.1205** | 素数位数作用の副有限完備化に対する section 予想の位相版 → 実点 section 予想 | 遠(抽象化 C。分裂の「幾何的理由」型) | arXiv |
| 8 | M. Szymik, *Artin–Schreier quandles of involutions in absolute Galois groups*, arXiv:**2403.07545**(Abh. Math. Semin. Univ. Hambg. 掲載予定) | 体の実スペクトル = 絶対 Galois 群の対合の共役類空間。対合の中心化群は自分自身 | 遠(標的 1 の「対合が壊れない」剛性の語彙) | arXiv |

## 2. 各候補の機構ベース評・翻訳可能性・深読み時の照合観点

**#1 Galindo(最有力)**
機構: 有限 abelian 群 A に付随する Heisenberg 群 V_A とその上の Clifford 群 C(A) について、1 → (中心) → C(A) → Sp(V_A) → 1 の障害類を評価。**|A| 奇なら障害は消える(Prop 3.2)**。非分裂は 2-primary 成分にのみ由来し、そこは (a) 巡回 2 冪(SL(2,ℤ_N) の関係式)と (b) elementary abelian(§5・Griess を引用)の 2 ケースに帰着。
翻訳: 我々の D₈ は A=ℤ/2 の Heisenberg 群そのもの(extraspecial 2-群)。C_G(D₈) → G/D₈ は「D₈ を保つ対称性が D₈ 自身に持ち上がるか」= Clifford 拡大の相対版。**N 奇という仮定が Prop 3.2 の仮定と字面で一致する**のが最大の当たり。
照合観点: (i) Prop 3.2 の証明が「2 が可逆 ⇒ 2-コサイクルを 2 で割って cobound する」平均化論法か(ならば Q=(ℤ/N)^× の 2 部分が非自明でも使えるか要検討)、(ii) 障害類の住処が H²(Sp; ℤ/2) か H²(Sp; A) か、(iii) 我々の Q は Sp(V_{D₈}) ≅ S₃ の部分群ではなく (ℤ/N)^× なので、**「Sp の部分群への制限」で定理がどう弱まるか**。

**#2 Korbelář–Tolar**
機構: SL(2,ℤ_N) の生成元と関係式に、仮想的な分裂準同型が満たすべき条件を書き下し、N が 4 で割れるときのみ矛盾が出ることを示す。**完全に初等的・計算可能**。
翻訳: 我々の照合器(GAP + 独立実装)にそのまま移せる型の議論。ε の計算を「関係式に沿った符号の追跡」に落とせる可能性。
照合観点: 使っている SL(2,ℤ_N) の表示(Coxeter–Moser 型か)と、N 奇での分裂準同型の**明示式**。それが (ℤ/N)^× に制限したときどう見えるか。

**#3 Griess**
機構: extraspecial 群 E とその外部自己同型群 O の間の拡大 1→E→N→O→1(および H²(O; Z(E)) の非消滅)を系統的に決定。「いつ消えないか」の正典なので、**逆に「我々の Q では消える」ことの根拠を引ける**。
翻訳: D₈ の場合 Out(D₈) ≅ C₂ と小さいので、Griess の一般論は overkill だが、**「非消滅は n≥2 でのみ起きる」型の境界線**が引ければ ε=0 の構造的理由になる。
照合観点: n=1(= D₈)での H² の値。Griess の非消滅例が n≥2 に限るか。

**#4 Pakianathan–Yalçın**
機構: 中心拡大 0→V→G→W→0(V,W elementary abelian 2)は二次写像 Q:W→V, Q(w)=w̃² で一意に決まる。分裂 ⟺ Q≡0 ⟺ **全元が対合に持ち上がる**。
翻訳: Q の 2-部分に制限した ε を、**「Q の各元 σ の持ち上げ σ̃ の位数」**という完全に計算可能な量に置き換える辞書。三例で ε=0 だったのは「(ℤ/N)^× の各元が対合に持ち上がる」ことの言い換えになり、標的 1(複素共役が位数 2 のまま降りる)と接続する。
照合観点: 定理の仮定が「V,W ともに elementary abelian」であること。(ℤ/N)^× が ℤ/2^k 因子を持つ場合の拡張(Bockstein 閉性の役割)。

**#5 Guillot**
機構: 有限群 G に対する GT(G) の直接計算。**GT₁(PSL(2,q)) が (elementary abelian 2-群) × (D₈ のコピー)** という形。当工房の観測「K = C_N × D₈(直積)」と**現象が同型**。
翻訳: 注意 — Guillot の GT(G) は Dolgushev の GTSh とは別定式化(dessins の monodromy 群 G ごとの定義)。したがって定理の直輸入はできず、**「D₈ 直積因子がどこから来るか」という機構の輸入**が狙い。もし Guillot の D₈ が「三つ組 (x,y,z), xyz=1 上の対称性(位数 2 の 2 つ)から生じる」なら、hexagon のみの B₃-gentle 系での D₈ も同源の可能性。
照合観点: D₈ が直接因子になる補題の出所(PDF が壊れて未読 — 深読み担当は HAL 版 hal-02372970 を推奨)。複素共役 / 対合が生成元として現れるか。

**#6 Beyl**
機構: 有限 metacyclic 群の Schur 乗数は巡回で、位数は表示のパラメータの明示式。
翻訳: 標的 3 に対応。Hol(ℤ/N) = ℤ/N ⋊ (ℤ/N)^× は (ℤ/N)^× が巡回のとき(N = p^k, 2p^k)metacyclic なので、**その場合に限り C₂ 中心拡大の個数を明示計算できる**。一般の N では metacyclic でないので、この線は部分的。
照合観点: M(G) の位数式に「2 の冪が入る条件」。それが N 奇と両立するか。

**#7 Pál**
機構: Smith の不動点定理を pro-空間へ持ち上げ、位数 p の作用に対する section 予想の位相版を証明。実点上では「section ⟺ 実点」。
翻訳: 「対合の共役類 ⟷ 実点」という辞書は、我々の ε=0 を「**その有限商が実点を持つ**」と読み替える道を開く。GT-shadow は dessin/曲線の族に対応するので、**dihedral 族の対象が実定義可能(実 dessin)であることが分裂の理由**という筋書きが立つ。
照合観点: 定理の仮定(有限 CW・正種数など)が我々の genus 0 dessins 設定を含むか。位数 2 に特化した形。

**#8 Szymik**
機構: 絶対 Galois 群の対合の共役類がなす quandle。Artin–Schreier: 対合の中心化群は自分自身で、不動体は実閉。
翻訳: 「複素共役が有限商へ位数 2 のまま降りる」ための**構造的理由の語彙**を与える(位数 4 に持ち上がることが不可能である理由)。定理の直接輸入というより、標的 1 の主張を厳密に述べ直すための枠。
照合観点: 有限商における記述(quandle の有限商への functoriality)があるか。

### 補遺(表外・道具として)
- **Gaschütz の補元定理**: N が abelian 正規部分群のとき、補元の存在 ⟺ 各素数 p の Sylow p-部分群が S∩N 上で分裂。**ε=0 の判定を 2-Sylow に還元する標準道具**。逆向きの精密化: B. Sambale, *On the converse of Gaschütz' complement theorem*, arXiv:**2303.00254**(J. Group Theory 掲載・実在確認は arXiv abs のリンク表示のみ、**要再確認**)。
- N. Combe, Yu. Manin, *Genus zero modular operad and its involution in the Grothendieck–Teichmüller group*(arXiv:**1907.10313** に対応と検索結果は示すが、**当該 abs ページの取得で題名・著者を確定できなかった — UNVERIFIED**。姉妹編 arXiv:1907.10317 *Symmetries of genus zero modular operad* は実在確認済)。標的 1 の「GT 内の基本的対合」に最も近い題名なので、司令塔が必要と判断すれば再確認を要する。

## 3. 空振りの当たりと使ったクエリ(負の結果)

**空振り 1: 「GT̂ の複素共役が有限商へ降りる」十分条件の明示定理。**
複素共役が GT̂ 内で自己中心化的であるという言及(Lochak–Schneps–Scheiderer, *A cohomological interpretation of the GT group*, Invent. Math. 1997 系)は繰り返し現れるが、**「有限商へ位数 2 のまま降りる」型の定理は見つからなかった**。Dolgushev 系(2401.06870 / 2405.11725)の abstract にも複素共役・対合の言及なし(2405.11725 は Lochak–Schneps 条件と dihedral poset Dih、および G_ℚ → GTSh(K,K) 全射予想を含むことを再確認)。
クエリ: `complex conjugation Grothendieck-Teichmuller group involution GT-hat arXiv` / `"Grothendieck-Teichmüller" involution "complex conjugation" element order two GT hat theorem Lochak Schneps` / `arXiv 2401.06870 GT-shadows gentle version complex conjugation element involution GT_gen` / `"GT" hat unique conjugacy class of involutions complex conjugation self-centralizing theorem proof`

**空振り 2: Hol(ℤ/N) の C₂ 中心拡大の明示分類。**
H²(Hol(ℤ/n), −) を直接計算した文献は見つからず。Hol(ℤ/n) は n 奇のとき complete group という事実(および n 奇で Aut(Hol) ≅ Hol)には行き当たったが、C₂ 拡大の分類には届かず。metacyclic 経由(Beyl)の部分解のみ。
クエリ: `Schur multiplier of the holomorph of a cyclic group H^2 central extensions Hol(Z/n)` / `Schur multiplier of metacyclic groups Beyl holomorph cyclic group central extension classification`

**空振り 3: metaplectic 二重被覆が奇 level で分裂するという当たり。**
「奇 N ⇒ 二重被覆が分裂」を SL(2,ℤ/N) / Weil 表現の語彙で直接述べた文献には検索で届かなかった(結果は p-進 metaplectic や Jacobi 形式に流れた)。**ただしこの当たりは #1/#2(Clifford 群)に吸収されており、そちらの方が明示的で移植しやすい** — 空振りは検索語の問題であって当たりの誤りではない、というのが遠征係の見立て。
クエリ: `metaplectic double cover SL(2,Z/N) splits N odd Weil representation genuine representation Gauss sum`

**空振り 4: 「自然な対合を持つ群の C₂ 中心拡大は分裂する」型の一般定理(標的 2 の一般形)。**
Tits 拡大 / Weyl 群の対合の持ち上げ(arXiv:1709.08589 等)、spinor norm、実形の語彙をあたったが、**求める形の一般定理は存在しない模様**。実際 #4(二次写像)が示すとおり、この命題は一般には偽で、「各元が対合に持ち上がる」ことが分裂と同値な**同語反復に近い**。したがって標的 2 は一般定理としてではなく、**#1 の odd-order 論法か #7 の実点論法という「理由の型」として追うべき**、というのが本遠征の結論的な当たり。
クエリ: `central extension by Z/2 splits when group generated by involutions lifting reflections Tits extension Weyl group spinor norm` / `central extension elementary abelian 2-group classified by quadratic form splits iff every element lifts to involution Arf` / `obstruction lifting automorphism action to extraspecial 2-group holomorph theta group normalizer split extension H^2`

**空振り 5: modular tensor category の Galois 対称性の持ち上げ障害。**
Ng–Schauenburg の congruence property / Galois symmetry には届いたが、**(ℤ/N)^× 作用の C₂ 持ち上げ障害の消滅**を主張する形の結果は見つからず。
クエリ: `Galois symmetry modular tensor category lifting obstruction H^2 Frobenius-Schur indicator Ng Schauenburg`

## 4. 実在確認の記録

- 実ページ取得で確認: arXiv 2603.24743(abs+HTML)・2305.13178(abs)・math/0606374(abs)・1604.04415(abs)・1407.3112(abs)・2405.11725(abs)・0905.1205(abs)・2403.07545(abs)・1907.10317(検索結果の abs リンク)・Griess 論文の Project Euclid ページ(euclid.pjm/1102945424)。
- **UNVERIFIED**: Beyl の DOI 10.2307/2039383(検索要約由来)、Sambale arXiv:2303.00254 の掲載誌、Szymik の DOI 10.1007/s12188-026-00297-z(検索結果由来)、Combe–Manin の arXiv ID 1907.10313 との対応。
