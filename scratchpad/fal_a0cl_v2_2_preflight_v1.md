# 反証前哨: a0_cofinal_lift_theorem_v2_2.md 発送前チェック(falsifier / 2026-09-05)

対象: `C:\Users\81905\Desktop\shadow-atelier\scratchpad\a0_cofinal_lift_theorem_v2_2.md`
(sha256 = `5953a6c2e1d8d022d7e1089766bb1b1de83e4d04a5ba06cb47e6096076f5a3e1`, 551 行)
比較対象: `scratchpad/a0_cofinal_lift_theorem_v2_1.md`(sha16 `ef6cc8dcb6594eb1` — note の申告と一致)

## 結論

**修正要(局所文言 2 点)— 修正後は発送可.** 数学的差し戻しではない。
定理 A / 定理 B / 命題 C の本文と証明は **機械照合でバイト同一**(§5)、外部引用は照合した 20 箇所すべて正確、
Sol 162 §2 の 3 つの narrowing 要求は (N1a)/(N1b)/(N1c) に忠実に吸収されている。
要修正は (F1) 注 1.3 が note 内部に新しい NAME-COLLIDE を作っている、(F2) D5 の「内部反証」の前件が引用元では仮定形、の 2 点。

---

## 1. D5 の内部反証(依頼 1)

### 1.1 確認できたこと

- Sol 162 §2 第 1 点(`sol/sol_reply_162_onboarding_astra.md:125-131`)逐語:
  「A nontrivial linear Fox syzygy does not, merely by being a syzygy, imply pentagon implies both hexagons.
  For example, the relation `H1-H2=0` permits `P=0` and `H1=H2!=0`. To derive the claimed implication one would
  need enough independent identities to force the whole H defect to zero. Finite counterexamples to the full
  implication therefore cannot exclude every weaker P--H syzygy. A class-specific identity is also not excluded
  by a counterexample at a different point.」
- これに対する (N1a)/(N1b)/(N1c)(v2_2:290-300)の対応は **1:1 で正確**:
  「H 欠陥全体を零に強制するだけの独立な恒等式族」= "enough independent identities to force the whole H defect to zero";
  (N1b) = "cannot exclude every weaker P--H syzygy"; (N1c) = "not excluded by a counterexample at a different point"。
  **撤回の方向(強い主張 → 限定形)は正しく、3 点とも取りこぼしなし。**
- (N1a) の副論証「`∃m` 版の反例は固定 `m` 版の反例を含意する」は論理的に正しい
  (∀f∃m の反証 ⟹ ∀f(固定 m)の反証。弱い命題の反例は強い命題の反例)。
- v169 (5.1)–(5.3) は実在(`sol/proof_r07_noncommutative_completed_fox_frattini_selector_v169.md:295-320`)、
  引用の式形(`e_± = (1±θ)/2`、(5.2) `B_∞ a_+ = −e_+β`、(5.3))も正確。
  括弧内「θ-odd 部が v75 の相対 dihedral 原像で処理できても θ-even 部の membership v169 (5.2) が残る」も
  v169 原文(「On the correctly typed odd part, v75 supplies the relative-dihedral preimage `h_-e_-β`.
  The remaining equation is exactly one completed actual class: (5.2)」)の正しい読み。
- 在庫 (2) の逐語(DLL 2008.00066 §4.3)は `papers/txt/2008.00066-what-are-gt-shadows.txt:3505-3545` で照合 —
  Property 4.2 の引用文は**一字一句一致**、11/35・残り 24 不成立、Property 4.3 は 13/35・残り 22 不成立、
  N^(19): 216 → 36、N^(34): 4096 → 243 もすべて一致。

### 1.2 【要修正 F1-B(=F2)】内部反証の前件が引用元では仮定形

v2_2:286(および §10 の D5 行 v2_2:527)は

> 内部反証も立つ: R07 には**実際に**欠陥加群上の非自明な線形構造 (S1)(return involution θ の冪等分解 `e_± = (1±θ)/2`、v169 (5.1)–(5.3))が**在り**

と断定するが、引用先 2 本はいずれも条件形である:

- `v169.md:295-296`: 「**Suppose** \(p\) is odd and **the return involution \(\theta\) acts continuously on (3.3)**.」
  — (5.1)–(5.3) はこの仮定の下にある。
- `sol/proof_r07_dihedral_spectral_commutator_split_v399.md:5-13`(Status): 「**If** the typed dihedral involution
  commutes with the same actual eleven-occurrence operator … **The actual R07 equivariance, parity, legality,
  A0 seed, and all-depth occurrence typing are not asserted here.**」
- 支持側として唯一あるのは `sol/proof_r07_return_reynolds_actual_splitter_v112.md:20-26`
  (「Both modules carry the same registered context action and \(B\) is equivariant. … The return involution is
  one such relation.」)だが、これは v111 の **leading-layer datum** についての登録であって、v169 (3.3) の
  completed 水準ではない(v112 §2 も `Bθ=θB` を "assume" と置く)。

リスク: Sol は同じ返書で「finite-shadow failures must not be called profinite counterexamples without compatible
lifts」と、条件つきのものを確定として語ることを名指しで戒めている(162 §2 末)。同じページで別の条件つき命題を
「実際に在り」と書けば、同型の narrowing 要求を再度受ける公算が高い。

### 1.3 【軽微 F2b】内部反証の論理的役割が過大

(S1) は note 自身が「(S1)–(S3) は M₀,₄ 水準(PB3/F₂)で **pentagon を含まず**」(v2_2:322)と書くとおり `E_P` を含まない。
したがって「P–H syzygy」を素直に「`E_P` を実質的に含む syzygy」と読む限り (S1) は v2.1 が否定した類の元ではなく、
reductio は成立しない。成立するのは v2.1 の λ を「`E_P` 係数 0 も含めて量化していた」と読む場合のみで、
それは **Sol の反例(H1−H2=0)がすでに使っている読み**である。つまり内部反証は独立の第二論証ではなく、
Sol の指摘と同型の instance(しかも「(S1) は H 欠陥全体を強制しない」= (N1a) の H-forcing 限定の必要性を示す例)である。

### 1.4 claim boundary `REFUTED WITHIN SCOPE; TRANSLATION PREMISE UNPROVED`(v2_2:491)

**妥当**(翻訳前提を同じ行に併記し、§8 Q8 で在庫照会まで出している = 逃げ道を塞いでいる)。
ただし「WITHIN SCOPE」がどの scope かは行内から読めない(DLL の商族の scope であって R07 の登録商族ではない)。
最小修正案: `REFUTED IN THE DLL FINITE-QUOTIENT SCOPE (stock (2)); TRANSLATION TO THE REGISTERED K_{r,n} UNPROVED`。

### 1.5 最小修正文案(F2 / F2b 同時)

v2_2:286 の一文を下記に差し替え(D5 行 v2_2:527 も同趣旨に):

> **内部にも同型の例がある(独立の反証ではなく Sol の反例と同型の instance)**: **仮に** R07 の欠陥加群上で
> return involution θ の同変性が成り立つなら(v112 §1 は v111 leading-layer datum について登録済み;
> v169 §5 は「Suppose … θ acts continuously on (3.3)」の仮定形; dihedral v399 は「the actual R07 equivariance …
> are not asserted here」と明示的に断りを置く)、(S1) は `E_P` を含まない非自明な線形構造であり、
> v2.1 の推論を認めると在庫 (2) と矛盾する ⟹ 推論が誤り。なお (S1) は H 欠陥全体を零に強制しない
> (θ-odd 部を v75 の相対 dihedral 原像で処理しても θ-even 部の membership v169 (5.2) が残る)ので、
> **(N1a) の「H-forcing」限定がなぜ要るかの例**にもなっている。

---

## 2. D9 の対応表 §5.4(依頼 2)

### 2.1 引用の正確性 — 照合 15 箇所すべて一致

| note の記述 | 引用先の実物 | 判定 |
|---|---|---|
| v526 (0.1)/(4.2) 相対像等式 | `..._v526.md:20-22`(0.1)、`:285-287`(4.2) | 一致 |
| v526 Thm 1.1 = 必要十分 | `:71-96`「If (1.5) … Conversely, if this fibre-surjectivity statement holds for every compatible target pair, then (1.5) holds.」 | 一致 |
| v526 (4.1) = 外から与える compatible target family + 源側全射 | `:259-278`「let … `r^E ρ_{n+1} = ρ_n` (4.1) be a compatible target family. Assume all source reductions are surjective」 | 一致 |
| v526 Thm 4.1 + 閉形式 selector (2.5) | `:280-310`、`:150-157`(2.5) | 一致 |
| v526 Prop 3.1 = 有限 cover ⟹ 像等式 | `:210`「Proposition 3.1 (instruction cover implies relative image equality)」 | 一致 |
| v526 の未証明 = A4/P1 gate | `:371-400` §6 +「A rank count without the columns, an empty search, or a cap does not prove (4.2).」 | 一致 |
| v537 (2.2) 物理核 cover | `..._v537.md:70-80` | 一致 |
| v537 (1.2)(1.3) = 固定語 w0 の関手的残差(target family を仮定しない) | `:41-56` + Status「removes the need to postulate an unrelated all-level target family」 | 一致 |
| v537 (3.1) word-bearing columns / Cor 3.1 | `:111-150` | 一致 |
| v537 §4 = 完全な first-rung coarse member 要 | `:151-186`「supplies (4.1) **only for the grade-two truncation** … must also be completed through grades three to six」 | 一致 |
| 逐語「Grade two alone is not a full initial member」 | `..._v537.md:183` に**そのまま存在** | 一致 |
| v539 (1.1)–(1.3) 生成子水準三恒等式 | `..._v539.md:25-38` +「All three equations must be checked on the registered instruction generators …」 | 一致 |
| v539 (2.5) = v504 Thm 6.1 の初期前件 | `:76-82`「which is exactly the initial completed-source premise of v504 Theorem 6.1」 | 一致 |
| (d3) 残る gate 列(compactness/strictness/separation/physical-jet saturation/side/Cauchy/continuity) | `v539.md:105-108` に**同じ 7 語が同じ順**で存在 | 一致 |
| v504 Thm 6.1 の前件 5 本 | `..._v504.md:404-419` | 一致 |
| §5.4 前文の Sol 逐語 5 本 | `sol_reply_162_onboarding_astra.md:157-171` の 5 文と対応 | 一致 |

### 2.2 「同型の条件を別 owner で・Sol 側が先行」の自己評価 — **正確。過小評価も見当たらない**

- 三条件はいずれも「源側相対核の像 = 標的相対核」の同形: v395 (3.4) `B_{n+1}(K^D_n)=K^L_n`
  (`..._v395.md:150-166`、Cor 3.2 "UNIVERSAL ONE-STEP CRITERION"、「provided `r^D_n` is onto on the legal source」)、
  v526 (4.2)、v537 (2.2)。
- v395 の著者は **Sol**(`v395.md:3` "Author: Sol / 2026-08-30")で、同 note の Status は
  「It does not prove that the actual R07 relative-kernel maps are onto」と自己限定している。
  つまり抽象形すら工房の寄与ではない — note はこれを 5 点目「**一様 lift 定理そのものは本稿の寄与ではない**」で
  正しく認めており、**過小評価(自分を不当に低く置く)にも当たらない**(定理 A / 定理 B (i)(ii) を土台として
  正当に主張している)。
- Sol 162 §3 と矛盾する行は見つからなかった。

### 2.3 【軽微 F3】(d1)/(d2) 行の未証明前件が Sol 162 §3 の列挙より短い

Sol 162 §3(`:149-152`)は「**The source section, kernel columns, common word and all-edge specialization** are
assumptions to be supplied, not consequences of an A0 success.」と 4 本を明示するが、§5.4 の (d1)/(d2) 行は
kernel columns / common word 相当は挙げるものの **source section(σ)** と **all-edge specialization(関手的
schema; v526 §6「one functorial schema which specializes to every edge」/ v537 §4 同文)** を挙げていない。
しかも「edge は無限個」という限定は **定理 B (iii) 行(自分の経路)にだけ**書かれており、(d1)/(d2) 行にはない —
自分の経路にだけ厳しい非対称になっている(D9 の趣旨 = 正しく位置づける、とは逆方向)。

最小修正案: (d1)/(d2) の「未証明の前件」欄の先頭に
`word-bearing source section σ・**all-edge specialization(関手的 schema; edge は無限個で、個別 cover の可算列では足りない)**(Sol 162 §3 逐語)` を追加。

---

## 3. D11 の段名辞書 注 1.3(依頼 3)

### 3.1 Sol 162 §0 との整合 — **一致**

- Sol 162 §0 1.(`:13-15`)「Current precision-two work belongs to the `2016 -> 54432` rung. It is not the
  `54432 -> Q0` rung named in the incoming campaign paragraph.」 ⟺ v2_2:108,112。
- Sol 162 §5(`:230-232`)「first-rung grades `1/6` (workshop ruling1916, limited cross-checked scope)」
  ⟺ v2_2:114 の読み替え(「T2 rung 1 の内部(= 本稿 T1 rung 3)の grade 1/6」)は正しい
  (54,432 段の grade 数 6 は v479 §6「Six accepted MEMBER updates … because `I^7 = 0`」と整合)。
  Sol 162 §5 の `CAMPAIGN_STATUS: … GRADE2_NOT_DECIDED` とも矛盾しない。
- 塔の段番号 504=rung 1 / 2,016=rung 2 / 54,432=rung 3 / Q₀=rung 4 は **内部整合**
  (§5.1「既知の非全射性: rung 1 (504)」、系 A.1 と一致)。
- 地図との整合: `docs/地図.md:27`「grade-two(= **2,016 → 54,432 段の precision-two**・Sol 162 で段名を訂正・
  「54,432 → Q₀」は誤記)」、`:30`「2,016 段 MEMBER・54,432 段 1/6」、`:35`「rung 3 残 5 + Q₀ 6 + …」= 同じ規約。
  `docs/状態.md:173` の「特性商の塔 504→2,016→54,432→Q₀」「rung 2/3」も同規約。
- 「Sol の "first rung" = T2 relative Frattini rung 1 = A0 全体」は v537 の "the complete first-rung physical
  owner required by v504"(= level 0 owner)の用法と整合。

### 3.2 【要修正 F1】注 1.3 の適用範囲文が note 内部に新しい NAME-COLLIDE を作る

v2_2:112 末:

> 本稿の他の箇所の「rung N」はこの表で読む。

これは **偽**である。note は「rung」を T2(相対 Frattini)の意味でも 12 箇所以上で使っている:

- v2_2:214 **命題 C(rung 1 は計算不能)** ← 表で読むと「段[504] は計算不能」
  = 同じ note の 系 A.1(v2_2:175)「rung 1(段[504])… MEMBER(cross-checked)」と**正面衝突**
- v2_2:22(VERDICT (3))「rung 1 の群は |E_{3,1}| = |e3|·3^{39,680,930}」
- v2_2:40(要約)「rung 1 の群の位数が 3 の 4 千万乗」
- v2_2:72(§1.2 見出し)「A0 = relative Frattini 塔の **rung 0 → 1** の一つの有限線形問題」(T1 に rung 0 は無い)
- v2_2:99-100(§1.3 T2 欄)、:199(定理 B (ii))、:222-223、:227(系 B.1)、:234-235(注 B.2)、
  :247/:257(§5.1 rung 0)、:317、:349、:399(§7)、:421(Q5)

D11 が消そうとした NAME-COLLIDE を、かえって note 内部に作り込んでいる(しかも `命題 C` の表題という
最も目立つ位置で矛盾する)。Sol は今回まさに rung 名の前提を訂正してきた相手なので、ここは通せない。

最小修正案(v2_2:112 の当該文を差し替え):

> **この表は T1(§1.3 上段・系 A.1・§5.1・§6 (vii)/(M1)(M2))の「rung N」にのみ適用する。**
> 本稿の **T2 側の「rung n」**(§1.2 見出し・§1.3 下段・定理 B・**命題 C**・系 B.1・注 B.2・§5.1 の rung 0・
> §7・§8 Q5・VERDICT (3))は v145 (1.3) の相対 Frattini 段の番号で、**別系列**である(T2 rung 0 = A0 = T1 の全段)。

併せて(任意・可読性): 命題 C の表題を「命題 C(**T2** rung 1 は計算不能)」、§5.1 を「既知の非全射性:
**T1** rung 1 (504)」に。

---

## 4. D6 / D7 / D8 / D10(依頼 4)

### 4.1 定理 A / B を弱めていないか — **弱めていない(機械確認)**

- D6 は補助命題(S1–S3 由来不変量の分離能力)を UNKNOWN へ格下げするのみ。定理 A/B に依存関係なし。
  格下げの理由(「因数分解定理が要る」「同じ入力に依存することは同じ分離能力を意味しない」)は論理的に正しく、
  在庫 (4)(`provenance/LEDGER.md:1561`「c₂ 有限版は well-defined に定義できた(定義 D1 …)が、分離能力は
  厳密にゼロと否定で確定」)の射程(= 定義 D1 について)を超えて一般化していた v2.1 の誤りを正しく限定している。
- D7 も定理に触れない。**むしろ台帳の誤りを直している**(4.2)。
- D8 は research-status の撤回。Sol 162 §1 Q3 逐語「No necessity theorem is supplied by these notes.」
  (`:64-71`)と一致。
- D10 は定理 B の**帰結の解釈**を lane 限定にするだけで、(i)–(iv) の主張は不変(注 B.3 自身が明記)。
  Sol 162 §2 末「The last equivalence is valid only for the registered pro3 lane and its actual side conditions」
  (`:135-138`)の要求に一致。
  注 B.3 (α) の「v169 §4 条件 4 の side gate(marking, formation, onto, settlement)」は
  `v169.md:296-303` の条件 4「pass the registered marking, formation, onto, and settlement gates」と逐語一致;
  条件 5「reduce to the fixed earlier partial word」= 注 B.0 の根付き版の根拠も一致。

### 4.2 D7 と DLL §4.3 — **矛盾なし。D7 は正しい修理である**

- `provenance/LEDGER.md:668`(在庫 (2) の出所)は「**Furusho property(pentagon ⟹ hexagon)の profinite 版は
  一般には偽**(C1 §4.3・35 例で機械判定・強 11/弱 13)」と書く。C1 = 2008.00066 は同台帳の同じ配達記録
  (`:664-667` に C1 §4 の N^(19) 216/36・N^(34) 4096/243)から確定。
- 原文 §4.3(`papers/txt/2008.00066-what-are-gt-shadows.txt:3505-3545`)は **NFI_PB4(B4) の元 N(= 有限商)に
  ついて** Property 4.2/4.3 の成否を数えているだけで、副有限版については何も主張せず、直後に
  「We conclude this section with selected open questions.」と続く。**副有限版が偽とは書いていない**。
- したがって L668 の「profinite 版」という語は台帳側の過剰な言い換えであり、D7 の読み替え
  (「有限商水準で一般には偽」+ 副有限は在庫 (1) Q14 = open)が正しい。在庫 (1)
  (`LEDGER.md:1414`「Furusho Question 14 … として名前つき未解決問題で実在(副有限版 pentagon⇒hexagon)」)との
  見かけの緊張も解消する。**この修理は note の中で最も価値のある一手**と評価する。
- 在庫 (3)(`LEDGER.md:1422`)・(4)(`:1561`)も逐語一致。

**【司令塔案件 F7】** D7 は台帳 L668 の文言を訂正している。note 側で直しても台帳は直らない —
裁定伝播規律に従い `provenance/LEDGER.md` L668 に errata 行
(「※訂正(2026-09-05): 正しくは『有限商水準で一般には偽』。副有限版 = Furusho Q14 は open」)を入れるのは司令塔案件。

### 4.3 【軽微 F4】研究者向け要約が (N1a) の翻訳前提を落としている

v2_2:42「**全 f 一様な形**については DLL の有限反例(35 窓中 24 で不成立)により**射程内で反証される**」—
「射程内」の中身(= DLL の商族であって R07 の登録 `K_{r,n}` ではない)は要約からは読めない。
最小修正: 「…により**射程内で反証される**(ただし DLL の商族と R07 の登録相対 Frattini 商族の翻訳は未証明 = §8 Q8)」。

---

## 5. 形式 — 差分は本当に D5〜D14 か(依頼 5)

**機械確認: はい。** `## ` 見出し単位の SHA-256 比較(v2.1 vs v2.2):

```text
SAME §0 記号 / §2 逐語表 / §6 有限検査条件 (i)–(xi) / §7 / §9 検算 artifacts
DIFF §1(+12 行 = 注 1.3 のみ)/ §3(1 行 = 系 A.1 冒頭のみ)/ §4(+6 行 = 注 B.3・系 B.1 見出し)
DIFF §5(+65 行 = (i′)/(N1a-c)・表三分割+(d)・(iii) 限定・§5.4 新設)/ §8(+17)/ §10(+34)
```

- **定理 A (i)–(v) と証明・注 A.3・注 A.2 は 1 バイトも変わっていない**(§3 の差分は 系 A.1 の冒頭 1 行のみ)。
- **定理 B (i)–(iv) と証明・注 B.0・注 B.2・命題 C も同様**(§4 の差分は 注 B.3 の挿入と 系 B.1 見出しのみ)。
- §6・§7・§9 は完全同一 ⟹ 「新規計算なし」「§9 の sha16 は v2.1 のまま」の申告と整合。
- **§9 の sha16 4 本を実ファイルで再計算 → 4/4 一致**
  (`a0_cofinal_layers_v1.g` = a63ffbf51b62ca69、出力 = f2c198a8664cad28、
  `a0_cofinal_layers_v2.g` = 5f648fda768fa734、出力 = ee6147ba6e1a9192)。

### 数値の独立再計算(node、整数のみ)— 15/15 一致

`|Δ| = 2⁵·3¹³·7 = 357,128,352` / `|e3| = |Q₀|·81 = 119,042,784` / `|AC| = |Δ|/9 = 39,680,928` /
`[e3:AC] = 3` / `dim M = 357,128,353` / Schreier `rank K_A = 1+39,680,928 = 39,680,929` /
`dim H₁ = 39,680,930` / `2(|G|+2) = 1,012`・`rank K_A^G = 505` / `d₀²/2 = 7.87×10¹⁴`(note「≈8×10¹⁴」) /
`|e4| ≈ |Q4|·3¹⁰ = 3.44×10²⁸` / `Γ/Φ(Γ)` 位数 9 = C₃²・`Φ(Γ)` 位数 27 = C₃³ / `pc3/Φ(pc3)` 位数 27 = C₃³ /
19 = 5+6+6+2 / 座標 9–10 の像 = |Δ|/3 = 119,042,784。

### 軽微(形式)

- **F5**: Status(v2_2:10)は「再実行もしていない」と書くが、§1.2(:74-75)と §9(:435-436)は「本稿で再実行」
  「本稿は再実行のみ」と書いたまま。「本稿」が v2 系列を指すのは文脈から分かるが、外部監査者には字面上の衝突。
  最小修正: §1.2/§9 の「本稿で再実行」→「**v2 で再実行**(v2.2 では再実行なし)」。
- **F6**: v2_2:112「地図 9/3 追記も同じ訂正済」— 段名の訂正文が入っているのは `docs/地図.md:27`(= **9/4 delta**)。
  9/3 delta(:30,:35)は元から同じ target 名規約で書かれている(訂正されたのではなく元から整合)。
  最小修正:「地図 9/4 delta(`docs/地図.md:27`)で訂正済・9/3 delta は元から同規約」。
- **F8**: §9 は自作 GAP 2 本にだけ sha16 を付し、falsifier 作 2 本には付していない。出所管理の一貫性のため
  付すなら値は `fal_a0cl_nu_pent_check_v1.g` = `5b883a1c7e5a528f`、`fal_a0cl_e3check_v1.g` = `08efb9fb8de74df6`。
- **F9**(既存箇所・D5–D14 外): v2_2:265 は DLL Property 4.3 を「weak: charming `f`」と要約するが、
  原文 Property 4.3 の条件は「`f N_{F2} ∈ [F_2/N_{F2}, F_2/N_{F2}]`」= charming(Def 2.19、
  `2008.00066:2013-2022`)の**前半のみ**(charming は加えて `T^{F2}_{m,f}` 全射を要求)。「weak: `f` が交換子部分群」に。
- **F10**(完全性): 系 B.1 の見出しへの併読指示追加(v2_2:225)は D5–D14 のどの項目にも列挙されていない。
  「差分 = D5–D14」を厳密に保つなら D9 か D10 に一行足す。

---

## 6. 反証できなかった観点(正直な範囲報告)

- **定理 A・定理 B・命題 C の数学内容そのもの**は v2.2 で変更されていないため、本前哨では再検査していない
  (v2 の前哨 = 裁定 2002、v2.1 の GAP 検査が既存)。今回新たな穴は探していない。
- **(N1a) の翻訳前提の真偽**(DLL の `N` 族と R07 の `K_{r,n}` 族の比較可能性)は本前哨でも判定できなかった。
  note が UNKNOWN として据え置き、§8 Q8 で在庫照会に回している処理は妥当。
- **注 B.3 (β)「B/C gate は 3 冪商の逆系では原理的に見えない」**は 注 B.2 (T-iii) の玩具例による類比であり、
  R07 についての証明ではない(note も「原理的に見えない」とだけ書き証明を主張していない)。反証も確認もできず。
- **(d) 経路の実現可能性**(A4 物理 basis columns が実際に取れるか)は本前哨の射程外。

## 7. 追加の軽微 — ラベル

**F11**: v2_2:211(注 B.3・新規)、:239(注 B.2)、:401(§7)、claim boundary は
「**B**(mixed-prime)・**C**(perfect-core) gate(v220 §16 規則 8)」と書くが、
`sol/audit_r07_full_proof_reaudit_and_forward_direction_v220.md:499-509` の実物は
**Priority C = mixed-prime actual membership / Priority D = perfect-core gate**(A = universal word-pair、
B = single-seed pre-gate)であり、§16 規則 8(`:526`)は「pro-3 lift を all-prime/perfect-core lift と呼ばない」で
**文字を割り当てていない**。工房の地図・状態・CLAIMS にも「B(mixed-prime)」の登録はない(grep 0 件)。
Sol は v220 の著者なので、文字がずれたまま送ると余計な往復を生む。
最小修正: 「v220 §15 Priority C(mixed-prime)・Priority D(perfect-core)(§16 規則 8: pro-3 lift を
perfect-core lift と呼ばない)」、または文字を落として「mixed-prime gate・perfect-core gate」。

---

## 8. 発送判定

**修正要 → 修正後は発送可。**

- 発送前に直すべき: **F1**(注 1.3 の適用範囲文・内部矛盾)/ **F2**(D5 の内部反証の前件を仮定形に)
- 同時に直すと安い: F3(§5.4 の非対称)/ F4(要約の翻訳前提)/ F11(B/C ラベル)/ F5・F6(字面衝突)
- 司令塔案件: **F7**(LEDGER L668 の errata)
- 数学的差し戻しは無し。Sol 162 §2 の 3 要求(H-forcing 限定・弱い syzygy 未排除・点固有は別点の反例で
  排除されない)は (N1a)/(N1b)/(N1c) で **過不足なく** 吸収されている。

---

sha256 先頭 16 桁(本行を追記する前の本文に対して) = `cffa2024236649fc`
