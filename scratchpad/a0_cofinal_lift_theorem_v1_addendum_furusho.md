# Addendum to `a0_cofinal_lift_theorem_v1.md` — §5.2(b′): 候補型 (b)「pentagon ⟹ hexagons の欠陥恒等式」の水準切り分けと U3 生存経路の再評価

Author: Fable(数学者・Claude 側)/ 2026-09-03.  司令塔の文献ゲート回答(4 点在庫検査 = 在庫内・新規遠征なし)への応答.
本文 v1(sha16 `87e6d2cdef64b6fe`)は falsifier 前哨監査中につき不変; 本稿は別ファイルの追補.  `verified=false`.  GHA/git 不使用.
NAME-COLLIDE 注意: 本稿の「(b)」= v1 §5.2 の候補型 (b)(syzygy 型).  在庫 (3) の「層 (b)」= FAKE-VOID 戦役(裁定 378/380)の層 (b) で**別物**.

## 0. 在庫(司令塔提示・逐語 pin)

- (1) LEDGER L1414(裁定 378): 「型 (i) = **Furusho Question 14(Ann. Math. 2010 末尾)として名前つき未解決問題で実在**(副有限版 pentagon⇒hexagon・被引用 84 件走査で追随ゼロ)」.
  覚書 FV-L1(docs/scout/覚書_fvl1_20260801.md): 「λ²=24c₂(f)+1 の平方根存在を仮定に置いた形 … 射程は Lie/pro-unipotent/pro-ℓ/pro-nilpotent のみ — 副有限は本人が明示的に未解決と宣言」,
  「副有限でも **pentagon ⇒ 2-cycle 関係 (I) は成立**(Furusho 指摘)— 未解決は (II) hexagon のみ」.
- (2) LEDGER L668: 「**Furusho property(pentagon ⟹ hexagon)の profinite 版は一般には偽**(C1 §4.3・35 例で機械判定・強 11/弱 13)⟹ hexagon を pentagon で代替はできない」.
  原文 2008.00066 §4.3(papers/txt, 行 3502–3540; 本稿の読解範囲はこの節のみ): Property 4.2(strong: 「For every f N_{F_2} ∈ F_2/N_{F_2} satisfying pentagon relation (2.20) modulo N, there exists m ∈ Z such that 2m+1 represents a unit in Z/N_ord Z and the pair (m,f) satisfies hexagon relations (2.18), (2.19)」)を満たすのは list (4.2) の 35 元中 11(残り 24 は不成立); Property 4.3(weak: f を交換子部分群に制限)は 13(残り 22 不成立).  例: N^(19)(N_ord = 6)で pentagon 解 216 個中 hexagon を持つのは 36; N^(34)(N_ord = 9)で charming pentagon 解 4096 個中 243.
- (3) LEDGER L1422(裁定 380 訂正①): 「Furusho Q14 = pentagon⇒hexagon であり、層 (b) が要るのは **converse(hexagon+charming⇒pentagon)** — Q14 は層 (b) の家ではない。層 (b) の正しい家 = **HS Main Theorem の M₀,₄/M₀,₅ 水準差・HS Prop 7 の置換持ち上げ特徴づけ**」.
- (4) LEDGER L1561(裁定 408): 「c₂ 有限版は well-defined に定義できた(定義 D1 …)が、**分離能力は厳密にゼロと否定で確定**」; docs/notes/c2q_finite_def_v1.md R3: 「C2-Q の答は『hexagon だけ』= 分離能力ゼロ … gcd(3,d)=1 の窓では c₂ は m の関数にすぎない」.
- (5) LEDGER L2605(裁定 655): dim 𝔤𝔯𝔱₁₂ = 2 の一次資料確定(本稿では使わない; 在庫の完全性のため記載).

## 1. (i) 候補型 (b) が要するのは群水準か Fox 線形化水準か — 切り分け

**設定の同定(同名別物ゲート).**  R07 の証人条件は 2 hexagon(PB3 側, 6 slot)+ 1 pentagon(PB4 側, 5 slot)の**三本同時**(v1 P3 の標的 `T`, v145 Thm 2.2)である.
これは 2008.00066 の本来系(pentagon あり, (2.18)(2.19)(2.20))であり, B₃-gentle 系(2401: hexagon のみ・pentagon なし)ではない.  gentle 系には pentagon が存在しないので
候補型 (b) はそこでは**空**(含意の前件がない).  以下は本来系での議論であり, 在庫 (2) の DLL データ(本来系の有限商)がそのまま適用範囲に入る.

**定義(候補型 (b) の正確な内容).**  T2 の edge `n → n+1`(T1 の fibre 段も同型)で, 水準 `n` の三関係を満たす語 `f` に対し欠陥類
`E_{H_b}(f) := [hex_b(f)] ∈ H_1(K_{3,n};F_3)`, `E_P(f) := [pent(f)] ∈ H_1(K_{4,n};F_3)` を取る.  候補型 (b) が使いたかったのは

```text
(b-lin)   ∃ 線形 Λ (または部分空間の指定):  E_P(f) ∈ (指定部分空間)  ⟹  E_H(f) ∈ im B_H     for all admissible f,
```

特にその最小形 `E_P(f) = 0 ⟹ E_{H_1}(f) = E_{H_2}(f) = 0`.

**補題 (b′.1)(Fox 線形化は群水準と同値).**  v145 Lemma 2.1 (2.4) `∇w ∈ im D_2 ⟺ w ∈ Φ_3(K)` により, `E_{H_b}(f) = 0 ⟺ hex_b(f) ∈ K_{3,n+1}`,
`E_P(f) = 0 ⟺ pent(f) ∈ K_{4,n+1}`.  ゆえに (b-lin) の最小形は edge ごとに次の**群水準**の命題と同値:

```text
(b-grp_n)  f が E_{3,n}, E_{4,n} で三関係を満たし, pent(f) が E_{4,n+1} で成り立つ  ⟹  hex_1(f), hex_2(f) が E_{3,n+1} で成り立つ.
```

これは DLL Property 4.2 の「塔相対・m 固定」版である: 量化子は `f` について弱い(水準 `n` の解に制限)が `m` について強い(roof の `m` に固定・`∃m` ではない).
Fox 行が「線形化」なのは**未知数 c(補正)について**であって, 欠陥類そのものは群水準の障害と一対一である.  したがって候補型 (b) が要するのは
**群水準の(塔相対)Furusho 性**であり, Fox 線形化水準に降りることで要求が弱まることはない. ∎

**補足(より弱い Fox 水準の syzygy について).**  「消滅の含意」でなく単なる線形関係 `λ(E_{H_1},E_{H_2},E_P) = 0`(全 admissible `f` で)も候補になり得るが,
そのような関係が全商で成り立つには語水準の恒等式(hexagon 語を pentagon 語の共役積と「水準 n で消える項」で表す式)が要る.  そうした恒等式があれば任意の
有限商で「pentagon 成立 ⟹ hexagon 成立」が従い, 在庫 (2) の 24/35(強)・22/35(弱)の不成立例と矛盾する.  ゆえに**形式的(語水準の)P–H syzygy は存在しない**.
R07 で実在する Fox 水準の恒等式は (S1) return involution θ による hex_1/hex_2 の対称性(v169 §5, v399 の dihedral split), (S2) Fox 基本公式による cycle 条件,
(S3) 正規化指数 ν(v399/v460)であり, いずれも M₀,₄ 水準(PB3/F₂ 側)で P と H を結合しない.

## 2. (ii) 群水準を要する ⟹ 在庫 (2) により閉塞 — U3 生存経路の再評価

**判定: 候補型 (b) は閉塞.**  根拠 3 点:
- (α) 有限水準: 在庫 (2) — 本来系の有限商で pentagon ⟹ hexagon は一般に偽(35 窓中 24 で強版不成立・22 で弱版不成立; 失敗窓では pentagon 解のうち hexagon を持つ割合が
  36/216, 243/4096 と小さい).  塔相対版 (b-grp_n) は別の量化子だが, 一般機構が無いことは同じ.
- (β) 副有限水準: 在庫 (1) — Q14 は名前つき未解決(追随ゼロ).  仮に真でも, 主張は `∃m`(`λ² = 24c₂(f)+1` の平方根の存在を仮定)であって R07 の固定 `m` を与えない.
- (γ) 翻訳機構の不在: Furusho の証明は char 0・pro-unipotent(lower central 次数付け・Lie 代数 𝔤𝔯𝔱)で, `m` を `c₂` から決める(`λ² = 24c₂+1`).  R07 の線形化は
  char 3・relative Frattini 塔(roof Δ は PSL(2,8) 商を持ち非冪零)であり, 次数付けも係数体も違う.  さらに `c₂` の有限版は在庫 (4) により分離能力が厳密にゼロ
  (証明が hexagon+charming しか使わない)— char 0 の証明で `m` を決める入力が, 有限水準では情報を持たない.  覚書 FV-L1 (a) の「平方根の存在 = 二次剰余条件」も
  有限段の障害として残る.
- 副次: 在庫 (1) の「pentagon ⇒ 2-cycle 関係 (I) は副有限でも成立(Lochak–Schneps 経由)」は, 2-cycle 関係(`f(y,x) f(x,y) = 1` 型)が hexagon 本体 (II) ではないので
  (b) を救わない; ただし (S1) の θ-対称性の群水準の裏づけにはなる(hex_1/hex_2 の連動).

**U3 の生存経路(再評価後).**

| 経路 | 内容 | 現状 | 評価 |
|---|---|---|---|
| (b) syzygy 型 | (b-grp_n) を全 edge で | 群水準 Furusho 性が必要 → (α)(β)(γ) | **閉塞**(R07 特有の構造で成り立つ可能性は否定できないが, 証明機構ゼロ・Q14 級) |
| (a) 層再帰 | `H_1(Ω_{n+1})_{V_n} ≅ H_2(V_n;F_3) ≅ Λ²V_n ⊕ V_n`(五項完全列; `Ω_n` 自由)/標的側 `coker(H_2(K_{r,n}) → H_2(V_{r,n}))` — edge n+1 の障害の `V_n`-共変射影は edge n の線形写像の `Λ²⊕id` で決まる | 推測段階 | **計算縮約としては死亡**: edge 1 の共変部分だけで次元 ~ `d_0²/2 ≈ 8×10¹⁴`(`d_0 ≥ 39,680,929`, v1 命題 C).  理論経路としても「共変障害が構造的に消える」機構は無い.  **保留(候補未満)へ降格** |
| (c) 登録契約型 | v174 (2.1) `β − Ba = μβ`, `μ ∈ 𝔧` ⟹ Neumann 級数; v191 (2.2) 離散共通源 `𝒢` の群環上の**有限台**恒等式 `ẽ − M d̃ = D̃_2 q` ⟹ 全 matched refinement で `e_n = μ_n d_n`; `q` の存在 ⟺ 三 endpoint 零(v194/v198, universal cover 単連結 ⟹ `ker D_1 = im D_2`) | A5–A8 = 0/3(A0 待ち) | **唯一の生存経路**.  理由: 仮説が rung-0 の**決定可能な有限条件**(compiled `M` の三 endpoint)であり, 三ブロックを対角的に同時に扱うので (b) の閉塞に触れない(v191 §2: 「two three-occurrence hexagon blocks and five one-occurrence pentagon blocks」).  十分条件のみ(v220 §14)・必要性は未証明・成否は計算で決まる |

**(c) についての二つの注意(本稿の寄与).**
1. (c) は pointed(distinguished defect `β` に限定)である.  在庫 (2) の失敗窓でも pentagon 解の**一部**は hexagon を持つ(36/216, 243/4096)ので, 「一般には偽」は
   「点 (m, g760) では偽」を意味しない — (c) が点固有の恒等式を要求するのは, 一般機構が無い世界で唯一整合的な形である.
2. (c) の仮説は rung-0 解 `c_0` の取り方に依存する(v191 Thm 3.1 は pointed ancestry から `M` を compile する).  v1 定理 B (ii) の dead-branch 論点はここで効く:
   `c_0` を `S_0 = c_0 + ker` 内で取り替える経路(v1 §8 Q4)が (c) の唯一の自由度であり, v195–v196 の same-μ repair torsor と併せて設計に明記すべき.

## 3. (iii) Fox 水準で生き残る恒等式と在庫 (3)(4) との整合(一段)

候補型 (b) は Fox 水準でも P→H 結合として生存しない(§1)ので, (iii) は (b) には空.  生き残る Fox 水準の恒等式 (S1)(S2)(S3) について一段だけ確認する:
- 対 (3): (S1)–(S3) は M₀,₄ 水準(PB3/F₂)の恒等式で pentagon を含まず, converse(hexagon+charming ⟹ pentagon; 家 = HS Main Theorem の M₀,₄/M₀,₅ 水準差・Prop 7)
  を与えも否定もしない.  = 「型 (ii) 分離不変量は存在せず」(L1414)と整合.  矛盾なし.
- 対 (4): (S1)–(S3) から作れる不変量は hexagon 側の線形化データのみ = `c₂^fin`(定義 D1)と同じ入力に依存するので, R3(分離能力ゼロ)により pentagon の持ち上げを
  判定できない.  矛盾なしどころか, R3 は §2 (γ)(char 0 証明の `c₂` 入力が有限水準で盲目)の直接の裏づけ.
- 帰結(設計面): H ブロックを P ブロックに従属させる (b) も, その逆(P を H に従属; converse・M₀,₅ 水準・open)も使えない.  T1/T2 とも三ブロックは**同時**に
  (定理 A (iii) のブロック逐次 H→P→ν は線形代数の順序であって含意ではない)扱う現行設計が正しい.

## 4. 要約(5 行)

1. 候補型 (b) の欠陥恒等式は, v145 Lemma 2.1 により edge ごとに群水準の塔相対 Furusho 性 (b-grp_n) と同値 — Fox 線形化で要求は弱まらない.
2. 群水準は在庫 (2)(有限商で 24/35・22/35 不成立)で一般閉塞, 在庫 (1)(Q14 未解決・`∃m` 形)で副有限も未解決, 翻訳機構(char 0/lower central → char 3/relative Frattini)も無い.
3. よって (b) は閉塞; (a) 層再帰は計算縮約として死亡(edge 1 の共変部分だけで ~10¹⁵ 次元)・理論機構なし → 保留へ降格.
4. U3 の生存経路は (c) 登録契約型(v174/v191)のみ — rung-0 で決定可能な有限仮説(三 endpoint 零)・十分条件・点固有・成否は A0 後の計算(A5–A8).
5. 生き残る Fox 恒等式 (S1)–(S3) は M₀,₄ 水準で在庫 (3)(4) と矛盾せず; (4) の R3 は (b) の有限水準での失敗機構(`c₂` 入力の盲目)を裏づける.

```text
(b) SYZYGY TYPE (pentagon => hexagon defect identity):   BLOCKED (group-level tower Furusho required; stock (1)(2)(4))
(a) LAYER RECURSION:                                      DEMOTED (no computational or theoretical mechanism)
(c) REGISTERED CONTRACT (v174 / v191 + v194/v198):        SOLE SURVIVING U3 ROUTE; sufficient only; decided after A0
FOX-LEVEL SURVIVORS (S1 theta / S2 cycle / S3 nu):        M_{0,4}-level; consistent with stock (3)(4)
NEW LITERATURE REQUEST:                                   NONE (stock suffices; the 【文献要請】 of v1 §5.2(b) is WITHDRAWN)
verified:                                                 false
```

`R07_A0_COFINAL_LIFT_ADDENDUM_FURUSHO_FABLE_V1`
