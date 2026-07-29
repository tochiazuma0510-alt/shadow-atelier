# 読解: Guillot「有限群の Grothendieck-Teichmüller 群と G-dessins d'enfants」

- 状態: **candidate(開示済み — 2026-07-30 裁定 212 で検疫解除)**。原文 2 本が文献ゲート配達(LEDGER 2026-07-30)で papers/delivered/ に降りたため、本 digest の数学者閲覧可。ただし**同名別物ゲートは未架橋**(Guillot 系は λ 座標を持たず ε 対応物なし — 機構輸入不可の判断は epsilon_mechanism_v1.md §8)・輸入時は司令塔の定義橋設計が前提。
- 読解日: 2026-07-25 / 読解者: reader(精密読解係)
- 主対象: arXiv **1407.3112v3**(P. Guillot, "The Grothendieck-Teichmüller group of a finite group and G-dessins d'enfants", 2015-12-03, 25 頁, SIGMAP proceedings 版)
- 補助対象: arXiv **1604.04415v1**(P. Guillot, "The Grothendieck-Teichmüller group of PSL(2,q)", 2016-04-15, 7 頁)
- 入手物: `docs/scout/papers/guillot_1407.3112.pdf`(sha256 `416c0a91…0806784b`)、`docs/scout/papers/guillot_1604.04415.pdf`(sha256 `16a2496e…be834cdea`)。テキスト層抽出 `guillot_1407_full.txt` / `guillot_1604_full.txt`(同ディレクトリ)。
- 照合方法: pdftotext のテキスト層+**ページ画像照合済み**(1407: p.1, 2, 3, 5, 13, 18 / 1604: p.1 を 150dpi レンダリングで原文確認)。以下の引用・数値はすべて画像照合済みか、テキスト層が画像と一致することを確認したページからの転記。

**表記**: 論文の GT(G) はカリグラフ体 𝒢𝒯(G)。Ḡ = 論文の \overline{G}。工房の「主線」= B₃ ベース gentle 系(arXiv 2401.06870 の GTSh・hexagon のみ)、「副線」= B₄ ベース本来系(pentagon あり)。

---

## 0. 結論先出し(系統判定)

**Guillot の GT(G) は hexagon 階層(pentagon なし)= Drinfeld の \widehat{GT}₀ の有限切片であり、当工房の主線(gentle 系)と同じ関係式階層に属する。ただし B₃ ではなく F̂₂ の outer 自己同型として定式化された「粗い(outer)変種」であり、主線 GTSh と同一物ではない。** 判定根拠は §2 に詳述。

- 「pentagon」の語は両論文に **0 回**出現(全文 grep で機械確認)。
- 逆極限の同定主張(1407, p.2, §1 Introduction): 「𝒢𝒯 coincides with the group denoted **\widehat{GT}₀** by Drinfeld in [Dri90] (we shall have nothing to say about the subgroup **\widehat{GT} ⊂ \widehat{GT}₀**, also considered by Drinfeld). All this, and more, is proved in [Gui14].」— \widehat{GT}(pentagon つき)は \widehat{GT}₀ の部分群として明示的に**除外**されている。

---

## 1. GT(G) の正確な定義(1407)

### 1.1 台となる群 Ḡ(§2.1, p.5)

- F₂ = ⟨x, y⟩(自由群)。部分群 N ⊂ Γ が「index G を持つ」とは (i) N ⊴ Γ かつ (ii) Γ/N ≅ G のこと(§2.1 冒頭の用語定義)。
- **N_G := F₂ の index G を持つ部分群すべての交わり**(有限個)。**Ḡ := F₂/N_G**(有限群)。x, y の像も x, y と書く。
- Lemma 2.1: (1) Ḡ の index G 部分群すべての交わりは自明。(2) 普遍性(index G 部分群の交わりが自明な任意の群 Γ と生成対 (x′,y′) に対し Ḡ → Γ, x↦x′, y↦y′ が存在)。(3) **Ḡ の任意の生成対 (x′,y′) に対し x↦x′, y↦y′ なる自己同型が存在**。
- 具体モデル(§2.1): index G 部分群 ↔ Aut(G)\P の軌道(P = G の生成対の集合)。軌道代表 (x₁,y₁),…,(x_r,y_r) を選ぶと **Ḡ ≅ ⟨x,y⟩ ⊂ G^r**、x = (x₁,…,x_r), y = (y₁,…,y_r)。射影 p_i の核 K_i が r 個の index G 部分群で、**特性的な族**(∀φ ∈ Aut(Ḡ), φ(K_i) = K_{σ(i)})。
- **Ḡ̿ = Ḡ**(冪等性; r(Ḡ) = 1 による。§2.1 末尾)。

### 1.2 GT(G) の定義(§1 p.1 および §2.2 p.5)

Ḡ は Lemma 2.1(3) により自己同型 **θ: θ(x) = y, θ(y) = x** と **δ: δ(x) = y⁻¹x⁻¹, δ(y) = y** を持つ(§2.2。§1 では z を xyz = 1 なる元として δ(x) = z, δ(y) = y と書く — 同じもの)。

φ ∈ Aut(Ḡ) に課される条件(§2.2 の番号 (1)(2)。**式番号つきの関係式はこれが全部** — 本論文に hexagon/pentagon の明示方程式は書かれない):

1. **(1) φ(x) は x^k(k は Ḡ の位数と素)の共役**。(帰結として φ(y) ∼ y^k, xy ∼ (xy)^k。§1 版では「some integer k」だが §2.2 で「k prime to the order of Ḡ」と精密化)
2. **(2) φ は Out(Ḡ) の中で θ および δ と可換**(= inner を法として可換)。

これらの φ のなす部分群の **Out(Ḡ) における像が GT(G)**(§1 の記法では A(Γ) ⊂ Aut(Γ), その像 𝒜(Γ), GT(G) := 𝒜(Ḡ))。**GT₁(G)** = 条件 (1) を k = 1 に制限したものの像(正規部分群)。

注意(§2.2 末尾, p.5): **k は well-defined でない**(x^k どうしが共役になり得るため、φ ↦ k なる写像は存在しない。λ 座標を持つ GTSh との重要な差)。

Lemma 2.2 (§2.2, p.6): GT(G)/GT₁(G) はアーベルで、指数は (Z/NZ)^× の指数を割る(N = Ḡ における x の位数)。

### 1.3 課される関係式の正体(工房語への翻訳)

- 本論文の枠組では「hexagon 型関係式」は**明示方程式としては現れず**、「θ, δ との Out 内可換性」に**エンコード**されている。Drinfeld の (λ,f) 言語との対応(θ 可換 ↔ 反転関係 f(x,y)f(y,x)=1 型、δ 可換 ↔ 3-サイクル hexagon 型)の証明は本論文でなく **[Gui14]**(Enseign. Math. 60 (2014) 293–375, "An elementary approach to dessins d'enfants and the Grothendieck-Teichmüller group";arXiv 番号はおそらく 1309.1968 — **UNKNOWN**、未照合)に委ねられている。
- **unitality / pentagon / λ の 2m+1 パラメータ化はいずれも本論文に存在しない**。

### 1.4 逆極限と Drinfeld との同定(§1 p.2, §2.3 p.6)

- lim_G Out(Ḡ) ≅ Out(F̂₂)(p.2)。N_G たちは F₂ の有限指数正規部分群の族の中で共終(§2.3: 任意の有限指数 N ⊴ F₂ に対し G = F₂/N とすれば N_G ⊂ N)、lim F₂/N_G ≅ F̂₂。
- N_G ⊂ N_H のとき誘導写像 GT(G) → GT(H) があり(核が特性的部分群、§2.3)、**GT := lim_G GT(G)**、GT₁ := lim_G GT₁(G)。
- **GT = \widehat{GT}₀(Drinfeld [Dri90])、\widehat{GT} ⊂ \widehat{GT}₀ には言及しない**(p.2、画像照合済み。証明は [Gui14])。GT は Out(F̂₂) の部分群と見なせ、Aut(F̂₂) へ持ち上げ可能(p.2)。

---

## 2. 系統判定(判定根拠の詳細)

**判定: 主線(hexagon-only)と同階層。ただし「第三の変種」と呼ぶべき差異が 2 点ある。**

| 観点 | Guillot GT(G) | 主線 gentle GTSh (2401.06870) | 副線本来系 (2008.00066) |
|---|---|---|---|
| 関係式階層 | hexagon 相当のみ(θ,δ 可換にエンコード)。pentagon 出現 0 回 | hexagon のみ | hexagon + pentagon |
| 逆極限 | \widehat{GT}₀ (Drinfeld) | \widehat{GT} 系(gentle 版の受け皿)| \widehat{GT} |
| 台 | F₂ の有限商 Ḡ の **Out**(outer・(λ,f) データなし) | B₃/N 上の (m, f_N) 対(pointed・明示方程式) | PB₄ 系 |
| 中心 c(B₃ の Z)| **存在しない**(F₂ のみ、braid 群不使用) | あり(c 座標。M5 知見の焦点) | あり |

判定根拠(式レベル):
- (a) 逆極限が \widehat{GT}₀ と同定される主張は 1407 p.2(§1)に明文(上記引用)。\widehat{GT}₀ は Drinfeld [Dri90] の hexagon(関係式 (I),(II))のみの群であり、pentagon (III) を課した \widehat{GT} はその部分群 — Guillot 自身が「\widehat{GT} ⊂ \widehat{GT}₀ には触れない」と宣言。
- (b) 全文に braid 群・operad・pentagon が一切現れない(grep 0 件)。台は常に F₂/N_G とその Out。
- (c) 条件 (1)(2) は Drinfeld の x ↦ x^λ, y ↦ f⁻¹y^λf(hexagon 付き)の **outer 化+有限化**に相当([Gui14] に委任)。したがって「B₄ 系ではない」ことは確定。「B₃ 系そのもの」でもない(braid の σ_i も中心 c も持たないから)。**結論: 主線と同じ hexagon 階層の、F̂₂-outer 定式化による粗い変種**。

---

## 3. 明示計算の機構(1407 §4–§5)

### 3.1 S(G) の構成(§4.1–4.3)

- P = G の生成対 (g,h) の集合。**P_c = P の Inn(G) 軌道の集合**(c は conjugation)。r = |P/Aut(G)|。Out(G) は P_c に自由に作用し |P_c| = r·|Out(G)|(§4.1)。Lemma 4.1: P_c ≅ Out(G) × P/Aut(G)(Out(G) 同変な集合の全単射)。
- Remark 4.2: P は xyz = 1 なる生成三つ組 (x,y,z) の集合と同一視可能(dessin 文献との接続)。
- §4.2: Out(Ḡ) の P_c への作用を構成。φ·[x_i,y_i]_c = [φ_i⁻¹(x_{σ(i)}), φ_i⁻¹(y_{σ(i)})]_c(φ_i は p_{σ(i)}∘φ が p_i を経由して誘導する G の自己同型、σ = σ(φ))。Proposition 4.3: 準同型 Out(Ḡ) → C_S(Out(G))(S = S(P_c)、Out(G) の中心化群へ)。
- 特定元の誘導する置換(明示計算の要):
  - **Lemma 4.5**: θ·[g,h]_c = [h,g]_c。
  - **Lemma 4.6**: δ·[g,h]_c = [h⁻¹g⁻¹, h]_c。
  - **Lemma 4.7**: φ(x) ∼ x かつ φ(y) ∼ y なら φ の P_c 作用は G×G-「軌道」(座標ごとの共役類。Remark 4.8 の注意つき)を保つ。
- **§4.3 定義**: ⟨θ,δ⟩ ⊂ S(P_c) は θ² = 1, δ² = 1, δθδ = θδθ を満たし S₃ の準同型像。**S(G) := { P_c の置換で、Out(G)×⟨θ,δ⟩ の作用と可換、かつ G×G-「軌道」を保つもの } = C_S(H) ∩ Y**(H = Out(G)×⟨θ,δ⟩、Y = G×G-「軌道」分割に対応する Young 部分群。§4.4 冒頭の記法)。

### 3.2 同定定理と証明骨格(§4.3–4.4)

- **Theorem 4.9**: **G が単純非可換なら GT₁(G) → S(G) は同型**(一般の G では写像があるだけ。§5.4 の 2-群表で実際に |GT₁| ≠ |S| の例あり)。
- 証明骨格: Lemma 4.10([Jon14] 由来): G 単純非可換なら **Ḡ = G^r 全体**、G^r の正規部分群は ∏_{i∈I} G_i 型、極大正規部分群 = K_j。Lemma 4.11: Aut(G^r) ≅ Aut(G) ≀ S_r、Out(G^r) ≅ Out(G) ≀ S_r、**Out(Ḡ) の P_c 作用は忠実**。Out(G) の P_c 作用は自由で r 軌道なので C_S(Out(G)) ≅ Out(G) ≀ S_r となり位数比較で **Out(Ḡ) ≅ C_S(Out(G))**(p.13)。この同一視の下で GT₁ の条件「θ,δ と可換」は文字通り中心化条件、「φ(x) ∼ x(k=1)」は Lemma 4.7 とその逆(p.13 末尾: [φ_i⁻¹(x_{σ(i)}),φ_i⁻¹(y_{σ(i)})]_c が [x_i,y_i]_c と同じ G×G-軌道 ⇒ x と φ(x) が G^r で共役)により Young 条件と等価。∎
- **Proposition 4.12**: S(G) は輪積 E_k ≀ S_{r_k} の直積(Σr_k = r、E_k は H の部分商)、**r_k ≤ |Z|m²/|G|**(m = G の最大共役類サイズ、Z = 中心)。証明は H-軌道をブロック(H-同変全単射+分割整合で同値類化)にまとめ、各ブロック上で C_{S(B)}(H) ∩ Y_B = E ≀ S_s とする。
- **Corollary 4.13 / 4.14・Theorem 1.2**(p.3、画像照合済み): G 単純非可換のとき GT₁(G) の単純因子は **C₂ / C₃ / Out(G) の部分商 / A_s (s ≤ m²/|G|)** のいずれか(GT(G) では cyclic 因子が追加。Out(Ḡ) でなく Out(G) である点を著者が強調)。

### 3.3 アルゴリズム(§5、GAP)

- **総当たり法(§5.1)**: Ḡ を G^r ⊂ 直積として構成(AutomorphismGroup / OrbitsDomain で生成対軌道 r 個を列挙)。**Lemma 5.1**: GT₁(G) の各元 φ に一意の両側剰余類 D ∈ C_x\Ḡ/C_y を対応(φ̃: x ↦ x^f, y ↦ y と正規化したときの f の類。C_x, C_y は x, y の中心化群)。さらに **θ 可換性 ⇔ 1 ∈ C_x f θ(f) C_y^{θ(f)}**。手順: DoubleCosets(GB,Cx,Cy) → θ-条件と生成性で篩 → 残った f で GroupHomomorphismByImages により φ̃ 構成(ここが律速)→ δ との可換を IsInnerAutomorphism で判定。位数 32 超の G では実際上破綻(p.3 の記述)。
- **S(G) 法(§5.2、数桁高速)**: P_c を OrbitsDomain(diagG, G×G)+生成性フィルタで構成(長さ ℓ = r|Out(G)|)。G×G-「軌道」分割は ConjugacyClass(GG, pair) への所属で構成(OrbitsDomain 不可 — Remark 4.8 の擬軌道のため)。θ, δ の置換を Lemma 4.5/4.6 の式で、Out(G) 生成元の置換も直接構成 → H ⊂ S_ℓ。丸ごと Centralizer∩Y は不可能なので、H-軌道を「**packet**」(stabilizer の共役類 + 各 P_i との交わりの濃度で同値化した粗いブロック)に分け、packet ごとに C(H′) ∩ Y′ を計算して直積(Prop 4.12 の実装)。
- **完全例(§4.5)**: G = PSL₃(F₂)(位数 168, Out = C₂)。|P_c| = 114。G×G-分割(サイズ 2×4, 3×8, 6×9, 8×1, 10×2 個)と α, θ, δ の置換を明示列挙(p.15)。GT₁ の位数 512、**GT₁(PSL₃(F₂)) ≅ C₂³ × D₈²**。

### 3.4 計算結果(§5.3–5.4、p.18 画像照合済み)

- **Theorem 5.2**: GT₁(PSL₂(F_q)) — q=4: 自明 / q=7: C₂³×D₈² / q=9: C₂¹²×D₈ / q=8: 自明 / q=11: C₂²⁷×D₈⁷ / q=13: C₂⁵⁴×D₈¹⁷ / q=17: C₂¹⁰⁴×D₈⁵⁰ / q=19: C₂¹³³×D₈⁷⁴ / q=16: 自明。
- **Theorem 5.3**: GT₁(PSL₃(F₃)) ≅ C₂²⁶ × D₈⁶ × S₃⁴ × S₄²¹ × S₆¹² × S₇⁶ × S₈³ × S₉¹¹ × A³ × B⁸ × C⁵(A = (((C₂⁵)⋊A₆)⋊C₂)⋊C₂、B = ((((C₂×D₈)⋊C₂)⋊C₃)⋊C₂)⋊C₂、C = ((C₂⁴⋊A₅)⋊C₂))。
- **Theorem 5.4**: GT₁(A₇) の単純因子の直積 = C₂¹⁵² × C₃¹⁵ × A₅³ × A₆³ × A₇ × A₈² × A₁₀ × A₁₈。
- **Theorem 5.5**(= Thm 1.3): GT₁(M₁₁) の単純因子の直積 = C₂⁴⁶⁵ × C₃⁴⁶ × A₅¹⁰ × A₆⁹ × A₇¹⁰ × A₈⁴ × A₉⁴ × A₁₀⁵ × A₁₁⁵ × A₁₂ × A₁₄² × A₁₅⁴ × A₁₆ × A₁₇³ × A₁₈¹² × A₁₉ × A₂₀² × A₂₃ × A₂₈ × A₃₁ × A₃₃²。位数 = 2¹¹⁴¹·3⁴⁰⁷·5¹⁶⁵·7⁹⁸·11⁴³·13³⁴·17²³·19⁸·23⁵·29³·31³(p.3-4)。
- §5.4: 2-群(位数 2³–2⁷ の 2 生成非可換群)の表。max|GT₁| と max|S| が乖離(n=7 で 4 対 16)— **一般の G では GT₁ ≇ S(G)**。
- **Proposition 3.1**(§3, p.9): **GT₁(D_n) は n 奇数で位数 2**、n = 2k(k 奇数)でも位数 2、k 偶数(4 | n)で自明。手計算例として全証明つき(δ 条件から m ∈ {0,2} の 2 択に落とし、(t,1,1) ∈ G³∖Ḡ による共役で存在を示す)。

---

## 4. PSL(2,q) の構造定理(1604.04415、証明は骨子のみ)

- **§2 の定義(単純非可換 G 専用の言い換え)**: T = { (x,y,z) ∈ G³ : xyz = 1, ⟨x,y,z⟩ = G }、T/G = 同時共役の軌道。**θ·[x,y,z] = [y,x,z^x]、δ·[x,y,z] = [z,y,x^y]**(いずれも冪等、S₃ → S(T/G) で (12)↦θ, (13)↦δ)。H := Out(G) × S₃ が T/G に作用(Out(G) は自由)。**≡** : [x,y,z] ≡ [x′,y′,z′] ⇔ 座標ごとに共役。**GT₁(G) := { φ ∈ S(T/G) : H-作用と可換、≡ と両立 }**(1407 の定義とこの形の同値性は [Gui] = 1407 に委任)。
- **Theorem 1.1**(p.1 画像照合済み): **GT₁(PSL(2,2^s)) は自明(∀s ≥ 1)。q 奇数のとき GT₁(PSL(2,q)) ≅ C₂^{n₁} × D₈^{n₂}**。
- 証明骨子: 標数 2(§3)は MacBeath [Mac69] Thm 2・Thm 3(ii) — trace 三つ組 E(a,b,c) が生成三つ組を含めば単一共役類 ⇒ Corollary 3.3 自明。奇標数(§4)は E(a,b,c)(SL₂ 内 trace 指定)→ PE(a,b,c)(PSL への像)、符号解析(Lemma 4.1)、**Proposition 4.5**: PE(a,b,c) ≠ ∅ ならちょうど 2 共役類で、対角行列 diag(1,−1) 共役の外部自己同型 α が入れ替える。T(a,b,c) = PE(a,b,c) ∪ PE(a,b,−c)(2 or 4 元)。**Lemma 4.6**: H₀(T(a,b,c)/G の安定化部分群)の誘導置換群は C₂, C₂², D₈ のいずれか(C₄ 排除は Out(G) = ⟨α⟩×Gal(F_q/F_p) の自由作用から矛盾を引く)。**Lemma 4.7**: GT₁(G) = Π_{(a,b,c)} GT₁(G)_{abc}(X(a,b,c) = H-軌道で貼った分割上の直積分解)。**Lemma 4.8**: 各因子は {1, C₂, C₂², D₈}(C₄ が生じかけたら ≡ が退化して逆に D₈ 全体が入る、という論法)⇒ **Theorem 4.9** = Thm 1.1。
- n₁, n₂ の表(p.7): q=5: (0,0) / 7: (3,2) / 9: (12,1) / 11: (27,7) / 13: (54,17) / 17: (104,50) / 19: (133,74)。
- **Theorem 1.2**(dessins 応用): 任意の有限群 G に対し、Galois 拡大 K/Q が存在して Gal(K/Q) ⊂ GT(G) かつ monodromy 群 G の任意の dessin の moduli 体を含む(K = ker(λ_G: Gal(Q̄/Q) → GT(G)) の固定体、§5)。PSL(2,q): q 偶 ⇒ moduli 体はアーベル拡大;q 奇 ⇒ moduli 体の Galois 閉包 F̃ は **derived length ≤ 3**(GT₁ の derived length ≤ 2 + アーベル商)。
- 微細な注意: §5 冒頭に「proof of Theorem 1.1」とあるが内容は Thm 1.2 の証明(原文の誤植と思われる — 推測)。

---

## 5. G_Q との関係・genuine/fake 相当概念

- **単射 Φ: Gal(Q̄/Q) → GT**([Gui14] で証明、1407 §1 p.1・§2.4 p.6)。構成は dessins 経由で、Belyi–Grothendieck の忠実性から単射(§6.1 p.19-20)。さらに **GT 自体も regular dessins に忠実に作用**([Gui14] Thm 5.7 引用、p.20)。
- **λ の算術的計算(§2.4)**: φ = Φ(λ) のとき、k は円分指標で与えられる: N = x の位数、ζ = e^{2iπ/N} として λ(ζ) = ζ^k なる k で φ(x) ∼ x^k。Gal(Q̄/Q)′ → GT₁(Kronecker–Weber)。
- **Lemma 2.3(§2.4)**: 任意の k(N と素)に対し φ ∈ GT(G) で φ(x) ∼ x^k なるものが存在 — **証明は Galois 元 Φ(λ) を取るのみ**(「Gal(Q̄/Q) に訴えずに証明するのは難しそうで意外」と明記)。= λ-成分の算術的全実現が全有限レベルで成立。
- **genuine/fake の用語はない**が、実質的な同型の議論が 2 箇所:
  1. **§3 末尾(p.9)**: GT₁ → GT₁(D_n) の像は**すべての n で自明**。理由: 射影が GT₁(D_{4n}) = 1 を経由するから。特に n 奇数の位数 2 元(Prop 3.1)は**逆極限から来ない = 工房用語で fake**。lim_n GT₁(D_n) = 1。**fake の検出が「より細かいレベル(D₄ₙ)への持ち上げ不能性」で行われている** — 当工房の genuine 判定と方法論的に同型。
  2. **1604 Theorem 1.2**: 各有限レベルでの genuine 像は Gal(K/Q) ⊂ GT(G)(K = ker λ_G の固定体)という**有限 Galois 群としての実現**。どの元が算術的かの個別判定基準は与えていない(UNKNOWN: 論文中に個別 shadow の genuine 判定アルゴリズムはない)。

---

## 6. 当工房との接点メモ(★以下はすべて読解者の見立て・推測)

1. **翻訳の向き**: Guillot は既に hexagon-only なので「hexagon-only 版に翻訳したら何が変わるか」という問いは逆向きになる — 変わるのは関係式でなく**座標系**。(a) 主線 GTSh は (m, f_N) という pointed データ+商群内の明示方程式、Guillot は Out 内の可換条件(inner を法とする)で λ 座標すら well-defined でない。(b) 主線の台 B₃/N は中心 c を持つ(M5 知見「c ∈ N 暗黙前提」の焦点)が、Guillot の Ḡ = F₂/N_G に c は存在しない。**PB₃ ≅ F₂ × Z(c) なので、c を先に殺す商に限定すれば Guillot の塔は主線の塔の「c-自由な断面」に見える**(推測。証明は当然未見)。
2. **比較写像の予想(推測)**: N_G に対応する N ⊴ B₃(F₂ ↠ Ḡ の核 × ⟨c⟩ で生成される類の N)を取れば、gentle shadow (m, f) ∈ GTSh(N) から x ↦ x^{2m+1}, y ↦ f⁻¹y^{2m+1}f が Ḡ の自己同型を誘導し、hexagon 2 本がそれぞれ θ・δ との Out-可換性を与える ⇒ **自然な写像 GTSh(N) → GT(G) が存在するはず**。この写像の核(inner 化で潰れる分)と余核(outer 類のうち (m,f) に持ち上がらないもの)が「Guillot 版の粗さ」の定量になる。逆向きの持ち上げ障害の解析は新規性のある小課題になり得る。
3. **fake 検出の教材**: §3 の「GT₁(D_n) の位数 2 元は D₄ₙ で消える」は、**shadow atlas の genuine 判定を『より細かい宇宙への持ち上げテスト』として設計する**当工房方針の、独立な文献上の先例。dihedral 予想(2405.11725 Conj 5.1)とは塔が違う(あちらは K⁽ⁿ⁾ = ker ψₙ ⊴ PB₃、こちらは F₂ の N_G)ので矛盾はしないが、「同じ dihedral でも塔の取り方で fake だらけにもなる」という警告例として atlas の解釈節で引用価値が高い。
4. **計算技法の輸入候補**: (i) Lemma 5.1 の**両側剰余類 C_x\Ḡ/C_y による f-候補のパラメータ化+θ-条件 1 ∈ C_x f θ(f) C_y^{θ(f)} による前段フィルタ**は、WP2 transversal-cocycle モデルの f 列挙の枝刈りに直訳できる可能性(推測)。(ii) S(G) 法の「centralizer ∩ Young を packet 分割してから計算」は、GAP での中心化群計算が爆発する場面の標準回避策として有用。(iii) Theorem 1.2 型の単純因子制約(C₂/C₃/Out 部分商/A_s, s ≤ m²/|G|)は、当工房の対象群での GTSh(N) のサイズ見積りの sanity check に流用できるかもしれない(ただし枠組が違うので直接適用は不可 — 要検討)。
5. **D₈ の遍在**: PSL(2,q)(q 奇)で GT₁ ≅ C₂^{n₁}×D₈^{n₂} となる機構は「α(位数 2 中心的外部自己同型)の自由作用 + 4 点集合上の中心化群 = D₈」という純組合せ(1604 Lemma 4.6/4.8)。λ = 1 成分の hexagon-only 世界では D₈ ブロックが構造の基本単位になる、という経験則の裏付け(見立て)。
6. **注意(版差)**: Guillot の「GT(G)」は当工房主線の「GTSh(K,K)」とも副線の「GT(G)-パッケージ(Dolgushev)」とも別物。Dolgushev 系文献と併読する際は、**同名 GT₁ でも (a) pentagon の有無 (b) outer か pointed か (c) 塔(F₂ 商か PB₃/PB₄ 商か)の 3 軸で必ず区別**すること。

## 未確認事項(UNKNOWN)

- [Gui14] の arXiv 番号(1309.1968 と推定、未照合)と、そこでの GT = \widehat{GT}₀ 同定・単射性の証明の詳細。
- Drinfeld [Dri90] における \widehat{GT}₀ の関係式 (I)(II) の原文表記(本読解では標準的理解に依拠。式レベルの突合は Dri90 未入手のため未実施)。
- 1604 §5 の「Theorem 1.1 の証明」表記の誤植疑い(上記 §4)。
- Guillot 塔と主線 NFI 塔の圏論的関係(接点メモ 1–2 は全面的に推測)。
