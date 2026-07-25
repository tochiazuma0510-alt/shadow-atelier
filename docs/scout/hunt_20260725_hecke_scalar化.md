# hunt_20260725 — 非中心 group-algebra 元 z_{2,C} の Fourier 反転を scalar 指標式に落とす理論(要請 4/5 絞り直し・第二次出撃)

対象基準式:
  n_m = (1/|Q|) Σ_χ S₃(χ) · Tr(ρ_χ(z_{2,C}) ρ_χ(v_m⁻¹)),  z_{2,C} = Σ_{x∈C, x²=1} x, C = ΔA(非中心)

---

## 0. 困難の抽象化(3 通り)と当たり付けの理由

**抽象化 I — 「非中心元のスペクトル分解 = 部分群不変元の可換化」**
Tr(ρ(z)ρ(v⁻¹)) が指標値の積に落ちない唯一の理由は ρ(z) がスカラーでないこと。スカラー化の一般機構は二つしかない:(α) z を中心元の和に分解する、(β) z が或る部分群 A の共役作用で不変なら ρ(z) ∈ End_A(Res_A ρ) = **(Q,A) の Hecke/centralizer 環**に属し、Res が multiplicity-free(= Gelfand pair)なら Schur により各等質成分上でスカラー → **球関数**。
→ 探索分野: 有限群の centralizer ring 理論・Gelfand pair/triple・球関数の調和解析。

**抽象化 II — 「coset 上の類関数 = 指数 2 拡大の twisted 世界」**
C = ΔA は A の coset。coset 上に台を持つ類関数の理論は Clifford 理論(拡張・非拡張)、twisted Frobenius–Schur 指標(σ-捻り involution 数)、Shintani descent(twisted class algebra)が担う。z_{2,C} は本質的に「σ-twisted involution 和」であり、Bump–Ginzburg 型の Σ_χ ε_σ(χ)χ(1) = #{g : σ(g)=g⁻¹} が **まさに coset 版 involution 計数の scalar 公式**。
→ 探索分野: Kawanaka–Matsuyama 系・Clifford 理論・Shintani descent。

**抽象化 III — 「指定した層での方程式解数の正値性」**
n_m > 0 は「v_m⁻¹ ∈ (位数 3 の類)·(C 内の involution 集合)」という**積被覆問題**。scalar 公式は Frobenius の類乗法係数、正値性は Arad–Herzog 系の被覆定理・involution width。
→ 探索分野: products of conjugacy classes・covering numbers・involution width。

**★ 検索の結論(先に書く)**: (a) の scalar 化理論は**存在する。しかも二段構え**である。第一段は初等的で当工房に即適用可能:**C を Q-共役類の合併に分解すれば各類和は中心的**になり、Tr(ρ(z)ρ(v⁻¹)) は完全に scalar 指標式 Σ_K (|K|/χ(1))χ(K)χ(v⁻¹) に落ちる(C が Q-共役閉でない場合は C∩(位数2元) を Q-類と交わる部分に切る)。第二段(C が A-共役でしか閉じない真に非中心な場合)が **Curtis–Fossum の centralizer ring 指標公式**と **Gelfand triple の operator-valued 球関数**であり、これが (a) の直球文献。

---

## 1. 候補表(A群 = (a) scalar 化理論 / B-i 群 = coverage / B-ii 群 = prescribed coset)

| # | 群 | 文献 | ID/DOI | 実在確認 |
|---|---|---|---|---|
| A1 | (a) | Curtis & Fossum, *On centralizer rings and characters of representations of finite groups*, Math. Z. **107** (1968) 402–406 | DOI 10.1007/BF01110070 | ✅ Springer ページ確認 |
| A2 | (a) | Ceccherini-Silberstein, Scarabotti, Tolli, *Harmonic analysis and spherical functions for multiplicity-free induced representations of finite groups* = 書籍 *Gelfand Triples and Their Hecke Algebras*, LNM **2267**, Springer 2020 | arXiv:**1811.09526**(journal-ref に LNM 2267 明記) | ✅ arXiv abs 取得 |
| A3 | (a)/(b-ii) | T. Dokchitser & V. Dokchitser, *Character formula for conjugacy classes in a coset* | arXiv:**2105.07247** | ✅ arXiv abs 取得 |
| A4 | (a)/(c) | Kawanaka & Matsuyama, *A twisted version of the Frobenius–Schur indicator and multiplicity-free permutation representations*, Hokkaido Math. J. **19** (1990) no.3 | DOI 10.14492/hokmj/1381517495 | ✅ Project Euclid 取得(open access) |
| A5 | (c) | Yerrapati, Dixit, Shukla, *Twisted Frobenius–Schur Indicators and Character Degree Sums in Dihedral Groups*(2026-05-21) | arXiv:**2605.22127** | ✅ arXiv abs 取得 |
| A6 | (c) | 同著者, *Complex Representations of Groups and Involutions of its Automorphisms*(2026-05-22) | arXiv:**2605.23195** | ✅ arXiv abs 取得 |
| B-i 1 | (b)(i) | Arad & Herzog (eds.), *Products of Conjugacy Classes in Groups*, LNM **1112**, Springer 1985 | ISBN 978-3-540-13916-4 | ✅ Springer 書誌ページ確認(章 "Powers and Products of Conjugacy Classes in Groups" 実在) |
| B-i 2 | (b)(i) | Malcolm, *The involution width of finite simple groups* | arXiv:**1611.06900** | ✅ arXiv abs 取得 |

(≤8 遵守。B-ii 群は A3 が唯一の直球ヒットで、B-i とは**独立に**扱うこと — 下記 §3 参照。)

---

## 2. 機構ベース評・当工房(B₃-gentle: Q = 有限商・A ≤ Q・Δ = 位数 2 類・v_m)への翻訳可能性

### A1 Curtis–Fossum(1968)★最重要
- 機構: H ≤ G の線形表現から誘導した表現の **centralizer ring**(= Hecke 環)における直交関係(Thm 2.4)と、群環内のべき等元の明示公式。すなわち「G の中心には居ないが H-不変な群環元」のスペクトルを指標値で書く装置そのもの。
- 翻訳: z_{2,C} は A-共役不変(Δ が A-安定なら)なので Hecke 環 H(Q,A) の元。A1 の直交関係で ρ_χ(z_{2,C}) を H(Q,A) の標準基底(二重剰余類和)に展開 → 各係数が指標値の線形式。Tr(·ρ(v⁻¹)) はその展開を v_m の属する二重剰余類の指標値で拾う操作になる。**基準式の右辺が「Q-指標 × Hecke 環構造定数」に分離できるか**が照合観点。
- 深読み観点: Thm 2.4 の直交関係が multiplicity-free を仮定するか否か(仮定するなら Gelfand pair 条件が当工房の (Q,A) で成立するかを別途検査)。

### A2 Gelfand Triples(LNM 2267 / arXiv:1811.09526)★(a) の現代的正本
- 機構: 誘導表現 Ind_K^G V(V は K の非自明表現も可)の commutant を **operator-valued 球関数**の畳み込み代数として実現。multiplicity-free の場合、Hecke 環が可換になり Tr(ρ(z)ρ(v⁻¹)) 型が球関数値の積に落ちる。
- 翻訳: 当工房で必要なのは「trivial 表現の誘導」ではなく **Δ の符号付き線形指標を A から誘導**した状況に近い(Δ が位数 2 → 符号指標が自然)。A2 は trivial 以外の誘導を扱う点でまさに適合。**(Q,A,線形指標 θ) が multiplicity-free triple か**が go/no-go の判定条件。
- 深読み観点: 「multiplicity-free triple の判定条件」の章と、normal subgroup からの誘導を扱う節(A が正規なら Clifford 理論で完全に降りる)。

### A3 Dokchitser–Dokchitser(arXiv:2105.07247)★(b)(ii) の唯一の直球
- 機構: 剰余類 qN 内の G-共役類と、qN 上で恒等的に 0 でない Irr(G) との対応。G/N 巡回なら「G に拡張する Irr(N) の個数 = qN 内の共役類の個数」。**coset に台を持つ指標だけが coset 上の計数に寄与する**という選択則。
- 翻訳: 基準式の Σ_χ が **C 上で消えない χ に自動的に制限される**ことを保証する。これは非中心性を殺すのではなく、和を大幅に切る枝刈りとして効く。さらに C 内の Q-共役類を数える公式は、抽象化 I の第一段(z_{2,C} を中心類和に分解)を実行するための土台。
- 深読み観点: A ⊴ Q かつ Q/A 巡回(位数 2)という当工房の典型形にそのまま乗るか。C = ΔA は q=Δ の coset なので設定が一致する。

### A4 Kawanaka–Matsuyama(1990)+ A5/A6(2026 の後継)
- 機構: ε_σ(χ) = (1/|G|)Σ_g χ(g·σ(g)) と Σ_χ ε_σ(χ)χ(1) = #{g : σ(g) = g⁻¹}。**σ-twisted involution の個数を指標次数の重み付き和で書く scalar 公式**。σ = Δ による共役をとれば「Δg が involution」という当工房の条件そのもの。
- 翻訳: n_m の第二条件「Δf が位数 2」は twisted involution 条件。K–M は χ(1) 重みの和しか与えないが、**v_m による重み付け(第一条件「v_m f が位数 3」)を入れた relative 版**が必要 — そこが工房側の一工夫。A5 は dihedral 群での m_σ の完全分類を与えており、**当工房の dihedral 対象に対する fixture / sanity check の即用データ**になり得る(2026-05 の新着で未消化)。
- 深読み観点: A5 Table(D_n の m_σ の数論的分類)を GAP 計数と突合 → 基準式の Δ-部分だけの較正ゲートに使える。

### B-i 1 Arad–Herzog LNM 1112 / B-i 2 Malcolm(arXiv:1611.06900)
- 機構(i 型 = coverage): 「torsion 類の積が群を覆う」型。Malcolm は非可換有限単純群の involution width ≤ 4(最適)。Arad–Herzog は covering number(C^n = G)の系統理論。
- 翻訳: 当工房の Q は単純とは限らない有限商なので **直接は使えない**。使えるのは「被覆が成り立つための必要条件・障害の形」(例: 商が位数 2 の abel 商を持つと involution 積が偶数長に制限される、等のパリティ障害)。n_m > 0 の**反例側**(空になる条件)を作る道具として価値がある。
- 深読み観点: パリティ/abel 化障害の一般命題を Arad–Herzog から抜き、Q の abel 化に翻訳。

---

## 3. (b) の分離申告(混ぜないこと)

- **(i) coverage 型**(全 torsion 集合の積が群を覆う): B-i 1(Arad–Herzog LNM 1112)、B-i 2(Malcolm involution width, arXiv:1611.06900)。いずれも**単純群前提**が骨格で、当工房の一般有限商 Q へは移送不可。ヒットは「非存在寄り」— この方向は当工房の主線ではない。
- **(ii) 指定 coset/layer での解数が正**: **A3(Dokchitser–Dokchitser, arXiv:2105.07247)のみ**が直球。他に「指定 coset での解数正値」を主定理に据えた一般論は今回の遠征では発見できず(§4 参照)。この空白自体が結果: **「coset 指定つき解数の正値性」は一般理論として整備されていない可能性が高く、当工房が自前で組む正当性がある。**

---

## 4. 空振りの当たり・使ったクエリ(負の結果)

**空振りだった当たり**
1. **relative/spherical character(Aizenbud–Gourevitch 系, arXiv:1501.01479 等)** — 実在するが reductive 群上の超関数論で、有限群の scalar 計数には移送不能。「spherical character」の語は当工房が期待する意味では**無人**。
2. **Shintani descent の twisted class algebra**(arXiv:1504.06198, 2401.09309 等) — twisted class function ↔ class function の同型は概念的に近いが、有限簡約群の Frobenius 特有の構造(norm 写像)に依存。当工房の一般 Q には norm 写像がなく移送不可。
3. **「全ての元が involution × 位数 3 元の積」型の定理** — 明示的に探したが**存在せず**。ヒットするのは (2,3)-生成(King, arXiv:1603.04717)と involution width のみで、**生成**であって**単一元の表示**ではない。(b)(i) の想定した形の定理は少なくとも標準文献には無い。
4. **Diaconis 系 involution walk / 確率論的 Gelfand pair** — 当たりを付けたが、有限群上の解数の**厳密 scalar 公式**を与える文献に到達できず(random walk の混合時間評価が主で、正値性の証明道具にならない)。
5. **Hopf 代数版 twisted FS 指標**(arXiv:1107.0742) — 一般化としては存在するが、群環に戻すと K–M に退化。追加情報なし。

**使ったクエリ**
- "Hecke algebra of a Gelfand pair spherical functions counting solutions of equations in finite groups coset"
- "twisted Frobenius-Schur indicator Kawanaka Matsuyama generalization involutions coset counting"
- "Arad Herzog products of conjugacy classes covering finite groups involution times element of order 3"
- "relative character spherical character subgroup pair finite group trace rho(z) rho(v) scalar reduction"
- "\"every element\" finite simple group \"product of an involution and an element of order 3\""
- "Frobenius formula number of solutions equation prescribed coset of normal subgroup character sum extended character coset"
- "centralizer algebra End_H(Res V) commutant Hecke algebra subgroup invariant sum acts by scalar multiplicity-free spherical function finite group"
- "Arad Herzog Products of Conjugacy Classes in Groups LNM 1112 covering number C1C2=G"
- "Ceccherini-Silberstein Scarabotti Tolli Gelfand pairs finite groups book spherical functions Hecke algebra multiplicity-free triple"
- "class multiplication coefficients character formula number of ways element product of involution and element of order 3 finite group"
- "Shintani descent twisted class algebra coset G.sigma class sums center twisted characters finite group Digne Michel"

**UNVERIFIED 申告**
- Bump–Ginzburg の一般化(K–M を任意位数の自己同型へ拡張; J. Algebra 2004 と複数の二次資料が引用)は**実ページ未取得のため UNVERIFIED**。使う場合は要再確認。
- LNM 2267 の Springer 書籍 DOI(10.1007/978-3-030-51607-9 と推定)は認証リダイレクトで**直接未確認**。ただし arXiv:1811.09526 の journal-ref に「Lecture Notes in Mathematics, 2267. Springer, Cham, [2020]」と明記されており、書籍の実在自体は確認済み。
- Arad–Herzog LNM 1112 は書誌ページ・章タイトルまでは確認したが、covering number の具体的定理番号は未確認。

---

*作成: 論文遠征係 / 2026-07-25 / 採否判断は司令塔の専権*
