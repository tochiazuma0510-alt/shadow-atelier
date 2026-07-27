# 修正条文案(草案)— bridge evaluation clause の捻れ形化(**(5′) amendment**)

**起草**: 2026-07-27・Claude(数学者レイヤー・Opus 5)。**裁定 48-3 に基づく起草**。
**身分**: **草案である。適用は司令塔** — 凍結正本(`docs/manifest_k5_v1.md` v1.5 / `docs/week4-K5_Rule1_v1.md` v1.3)を**上書きしてはならず**、**manifest v1.6 / Rule 1 v1.4 という新 version を作り差分ゲートを通す**(便 46 F5.3)。
**根拠**: `sol/sol_reply_46_b9prime.md` **F4・F5.2・F5.3**、`docs/week4-BFC攻略_opus_v2.md` **§8.1(U5 注)・§10.1(補題 B-9′)・§15.8**。
**発端**: **研究者の指摘**(2026-07-27・「exact $\varepsilon$ 依存が campaign 判定から消せるのではないか」)→ 司令塔委嘱 → 補題 B-9′ → 残留 1 箇所の同定 → 本条文案。

---

## 0. なぜ直すのか(3 行)

1. 現 manifest / Rule 1 の bridge 述語は **untwisted** の $\rho_i(\mathrm{Ih}_N(\gamma))=\tau_i(\kappa_i(\gamma))$ を採る。
2. しかし定理として成立するのは **twisted** 形 $\rho_i(\mathrm{Ih}_N(\gamma))=\tau_i(\kappa_i(\gamma)^{b})$ である(**定理 B-7$^{\rm tw}$**、前件 (TB4$^{\rm u}$))。exact $\varepsilon=1$(= (TB4))は**文献関所**で未閉鎖。
3. ゆえに $\varepsilon\not\equiv1\ (\mathrm{mod}\ 10)$ の場合、現条文は**数学的に正しい橋を偽 FAIL にできる**。`bridge_result_i` はこの述語の PASS/FAIL/UNKNOWN を記録し、結果規則表はそれを入力にするので、**残留は条文だけでなく `bridge_result_i` の意味の中にある**(便 46 F5.2)。

> **★ 緊急度の判断(便 46 F5.3 の `amendment now` を採用)**: 現行の測定計画に actual shadow を外部経路で計算する工程はない。**しかし「測定計画に現れない」ことは述語の意味を $\varepsilon$-free にしない。** 既知の偽 FAIL 条件を normative text に残す利点がないので、**外部 shadow 経路が入る前に直す**。

---

## 1. 変えるもの / 変えないもの(適用範囲の明示)

| | 内容 |
|---|---|
| **変える(1 述語のみ)** | **bridge evaluation clause** — すなわち「橋の PASS/FAIL をどの等式で判定するか」。該当は **manifest の BRIDGE-FAIL 条項①** と **Rule 1 §8.4「(5′) の量化子」** の 2 箇所 |
| **変えない** | モデル正規形(Rule 1 §2)・selection と全順序(§3・§4)・uniformizer 決定(§5)・$u$ の二経路と受理規則(§6)・**$b_i$ の決定式 (7.1) と受理条件 (7.3)**・exact Kummer 判定器(§8.1–§8.3・§8.5)・停止条件(§9・**I-d を含む**)・whitelist・封印時点・凍結 1 の不変条項・manifest の五/六層札・封印予測 (P1)(P2) の**内容**・結果規則表の**遷移** |

> **記録の精度(便 46 F5.3)**: 「凍結 1 の内容は一行も変わらない」と書いてはならない。**Rule 1 §8.4 の一行は実際に変わる。** 正しい記録は
> $$ \boxed{\text{凍結 1 の}\ \textbf{モデル探索・封印・抽出規律は不変}\ \text{。}\ \textbf{bridge evaluation clause のみ versioned amendment}} $$

---

## 2. 条文案 A — `docs/week4-K5_Rule1_v1.md` §8.4 の差し替え(Rule 1 v1.4)

### 現行(v1.3)

> ### 8.4 (5′) の量化子
> $$ \rho_i(\operatorname{Ih}(\gamma)) = \tau_i(\kappa_i(\gamma))\qquad(\forall\gamma\in G_K). $$
> **有限個の Frobenius サンプル一致は較正であって PASS の証明ではない。** PASS は character 恒等の普遍的導出、または同値な Kummer 拡大の厳密同定を要する。**FAIL は exact な $\gamma$ 一つで足りる。**

### 改定案(v1.4)

> ### 8.4 (5′) の量化子(**bridge evaluation clause**・v1.4 改定)
>
> **8.4.0 事前凍結された捻れ指数.** 各 dessin $i$ について、$b_i\in(\mathbb Z/10)^\times$ を **§7.1 (7.1) により、actual な $G_K$-データを見る前に**決定・記録した値とする。$b_i$ は $\mu_{10}$-torsor **全体**上の実 local monodromy から測るので、$\kappa_i$ の像の大小に影響されない。**$b_i$ は凍結 1 の記録項目であり、本節の判定に用いる時点で既に固定されている。**
>
> **8.4.1 判定式(捻れ形).**
> $$ \boxed{\ \rho_i\bigl(\operatorname{Ih}_N(\gamma)\bigr)\ =\ \tau_i\bigl(\kappa_i(\gamma)^{\,b_i}\bigr)\qquad(\forall\gamma\in G_K).\ } \tag{5$'_b$} $$
> **$b_i=1$ の場合が旧 (5′) である。**
>
> **8.4.2 量化子と証明水準(不変).** **有限個の Frobenius サンプル一致は較正であって PASS の証明ではない。** PASS は character 恒等の普遍的導出、または同値な Kummer 拡大の厳密同定を要する。**FAIL は、8.4.0 で凍結済みの $b_i$ に対する exact な反例 $\gamma$ 一つで足りる。**
>
> **8.4.3 fitting の禁止(新設・falsifiability の保全).**
> > **$G_K$-データを見てから $b_i$ を選び直す(re-fitting する)ことを禁止する。** すなわち「ある $b\in(\mathbb Z/10)^\times$ が存在して (5$'_b$) が成り立つ」という**存在形での PASS 宣言を禁止**する。判定は常に**事前凍結された 1 個の $b_i$** に対して行う。
> > **理由**: $\operatorname{ord}([v_i]_{10})=1$ の分岐では $\kappa_i(G_K)=1$ となり、$b\in\{1,3,7,9\}$ の**四つすべてが同じ自明指標**を与える。$\tau_i$ が単射でも $b$ は $G_K$-character からは同定できない。存在形を許すと**この分岐で判定が空虚になる**。
> > **違反した場合**: `I-i` に準じ、PASS/FAIL を宣言せず記録のみ(→ §9 の新設 **I-n**)。
>
> **8.4.4 pairwise 運用の順序(新設).** 二 dessin を比較する前に、まず **§7.3 の integrity gate $b_{\rm sq}=b_{\rm ns}$** を通す。**数学的には $b_{\rm sq}=b_{\rm ns}$ は定理である**(同じ枠組み単位 $\varepsilon$ の $\bmod 10$ 還元 — BFC v2.3 補題 B-9′(a))。**したがって測定値の不一致は新現象ではなく実装 transport の破損であり、`I-d` の即時 integrity stop が正しい分類である**(この読み替えにより §7.3 は撤回されず、役割が「規約」から「integrity 検査」へ明確化される)。
>
> **8.4.5 $\varepsilon$-free な結論(参考・新設).** 本節の捻れ化にかかわらず、次は $b_i$ の値に依存しない(BFC v2.3 系 B-8・補題 B-9′(c)(d)):
> **(P1)** $\operatorname{ord}([v_i]_{10})$ / **(P2)** $[v_{\rm ns}]_{10}=[v_{\rm sq}]_{10}^{a_{\rm eff}}$ と $a_{\rm eff}=a=1$ / **(R6-full)** 全射判定 / 固定体 $K(v_i^{1/10})$ / §8.3 の exact certificate。
> **⇒ 本 amendment は測定量を 1 つも変えない。変えるのは「橋そのものの PASS/FAIL をどの等式で問うか」だけである。**

### 付随:§9 への 1 行追加(Rule 1 v1.4)

> | **I-n**(v1.4) | **§8.4.3 に反して $b_i$ を $G_K$-データ観測後に再 fitting した / 存在形($\exists b$)で bridge の PASS を宣言した** ⇒ falsifiability の毀損として即時 integrity stop |

---

## 3. 条文案 B — `docs/manifest_k5_v1.md` BRIDGE-FAIL 条項①の差し替え(manifest v1.6)

### 現行(v1.5)

> | **BRIDGE-FAIL**(= B_FC の真の falsifier) | ①個別橋: BRIDGE-IN 独立成立下で **actual $G_K$-置換と $\tau\kappa$ の exact 不一致**、または **(P1) の exact な破れ**(前件札が独立に閉じている場合 — (5′) の候補反例)②pairwise: 封印予測 (P2)/(5.5) の exact な破れ(両 BRIDGE-IN 成立時 —「少なくとも一方の (5′) が偽」までを主張し、どちらかは同定しない) |

### 改定案(v1.6)

> | **BRIDGE-FAIL**(= B_FC の真の falsifier) | ①個別橋: BRIDGE-IN 独立成立下で、**Rule 1 §8.4.0 で事前凍結した $b_i$ に対する捻れ形 (5$'_b$) $\rho_i(\operatorname{Ih}_N(\gamma))=\tau_i(\kappa_i(\gamma)^{b_i})$ の exact な反例 $\gamma$ が一つ得られること**(**存在形 $\exists b$ での判定は禁止** — Rule 1 §8.4.3)、または **(P1) の exact な破れ**(前件札が独立に閉じている場合)②pairwise: 封印予測 (P2)/(5.5) の exact な破れ(両 BRIDGE-IN 成立時 —「少なくとも一方の (5$'_b$) が偽」までを主張し、どちらかは同定しない) |

### 付随:manifest v1.6 の注記 2 行

> - **(5′) の正本形は捻れ形 (5$'_b$) である**(BFC v2.3 定理 B-7$^{\rm tw}$)。$b_i=1$ は **exact (TB4)**(= 枠組み単位 $\varepsilon=1$)が閉じたときの特殊化であり、**(TB4) は現在も文献関所 `FRAMEWORK-UNKNOWN`** である。
> - **`bridge_result_i` の意味は本 amendment で $\varepsilon$-free になる。** それ以前の版で記録された `bridge_result_i` は untwisted 述語に対する値なので、**版を跨いで比較しない**(結果記録 `provenance/results_k5.md` に manifest version を明記する)。

---

## 4. 適用後に BFC 本稿で強められる主張(司令塔への申し送り)

本 amendment が成立したら、`docs/week4-BFC攻略_opus_v2.md` の**補題 B-9′(e) を全称形へ戻せる**:

> **(e′)(amendment 成立後)** $K^{(5)}$ campaign の**全判定** — `bridge_result_i`(PASS/FAIL/UNKNOWN と $\mathrm{ord}_i$)・`pair_gate`・`saturation_result`・結果規則表の**全遷移** — が exact $\varepsilon$ に依存しない。

**それまでは (e) は「(P1)(P2)(R6-full)・固定体・Kummer 証明書型・現行 Belyi-side 測定量」までに限定する**(便 46 F5.2・BFC v2.3 §10.1.2)。

---

## 5. 手続き(司令塔の作業)

1. **凍結正本を上書きしない。** `docs/manifest_k5_v1.md` → **v1.6**、`docs/week4-K5_Rule1_v1.md` → **v1.4** として新 version を作る(既存ファイルは digest 込みで保存)。
2. **差分ゲート**: 本草案 §2・§3 の条文を差分表つきで Sol へ回し、**bridge predicate の typing 以外が動いていないこと**を検収させる。
3. **凍結記録**(Rule 1 §10)に「amendment 適用日時・旧版 digest・変更した clause 名」を追記。
4. 適用後、**BFC 本稿の (e) を (e′) へ更新**し、その版で final digest を取り直す(GAP certificate の `input_doc_path` 束縛も同じ時点で・BFC §15.7)。
5. **`provenance/results_k5.md`** の schema に `manifest_version` / `rule1_version` 欄を追加(版を跨いだ `bridge_result_i` の比較禁止を機械的に担保)。

---

## 6. 起草者の自己申告(監査してほしい点)

1. **§2 の 8.4.3(fitting 禁止)の書き方**が、`ord5` 分岐での正当な PASS 論証まで塞いでいないか。私は「PASS は character 恒等の普遍的導出または Kummer 拡大の厳密同定」という**既存の証明水準**を残したうえで、**$b$ の選び直しだけ**を禁じたつもりである。
2. **§2 の 8.4.4** で「$b_{\rm sq}=b_{\rm ns}$ は定理」と書くことが、**§7.3 の受理条件を空文化しない**か。私は「定理だから測る必要がない」ではなく「**定理だから、測って違えば実装破損である**」という向きで書いた。
3. **§3 の pairwise 条項**で「少なくとも一方の (5$'_b$) が偽」という主張の型を変えていないか(捻れ形にしただけのつもり)。
4. **§5-5** の版欄追加は運用の提案であり、数学的必要ではない — **過剰でないか**。
