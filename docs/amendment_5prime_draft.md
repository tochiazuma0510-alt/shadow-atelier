# 修正条文案 **v2**(草案)— bridge evaluation clause の捻れ形化(**(5′_b) amendment**)

**起草**: 2026-07-27・Claude(数学者レイヤー・Opus 5)。**裁定 48-3 に基づく起草・v2 は便 47(`sol/sol_reply_47_amendment.md`)の blocker 2 件 + F7–F10 を反映(裁定 50)。**
**身分**: **草案である。適用は司令塔** — 凍結正本(`docs/manifest_k5_v1.md` v1.5 / `docs/week4-K5_Rule1_v1.md` v1.3)を**上書きしてはならず**、**manifest v1.6 / Rule 1 v1.4 という新 version を作り差分ゲートを通す**。**本草案が PASS してから新 version を作る**(便 47 F12-5)。
**根拠**: 便 46 F4・F5.2・F5.3 / **便 47 F4–F10** / `docs/week4-BFC攻略_opus_v2.md` §8.1(U5 注)・§10.1(補題 B-9′ = **two-mathematician PASS**)・§15.8。
**発端**: **研究者の指摘**(2026-07-27)→ 司令塔委嘱 → 補題 B-9′ → 残留 1 述語の同定 → 本条文案。

## v1 → v2 差分(便 47 の blocker と条文修理)

| # | 箇所 | v1 | v2 | 出所 |
|---|---|---|---|---|
| **A1** | §2 の 8.4.0 | actual $b_i$ を「**凍結 1** の記録項目」とした | **FAIL(blocker 1)**。$c_i,\ell_i$ と個別モデルが未確定の凍結 1 で actual 値は書けない(Rule 1 §9.3・§10-6・manifest と矛盾)。**二段コミットへ分離**: 凍結 1 = **規則・向き・入力 schema・記録欄** / 凍結 2(BRIDGE-IN)= **値**。**自認** | 便 47 F5 |
| **A2** | §2 の 8.4.2 | 「character 恒等の普遍的導出、**または同値な Kummer 拡大の厳密同定**」 | **FAIL(blocker 2)**。後半は**単なる体の同定**と読める。$\kappa_i$ と $\kappa_i^{\,d}$ は同核・同体だが**別 character**。**oriented $\mu_{10}$-torsor 証明書**を要求し、抽象的な体・核の一致を**明示的に除外**。**自認** | 便 47 F6 |
| **A3** | §2 の 8.4.3 | ord1 で「存在形を許すと**判定が空虚**になる」 | **強すぎ**。空虚になるのは **$b$ の同定・選択**だけで、**左辺 $\rho_i(\mathrm{Ih}_N\vert_{G_K})$ が自明か否かの試験は残る**。**自認** | 便 47 F6 末尾 |
| **A4** | §3 | 「**(5′) の正本形**は捻れ形 (5$'_b$)」 | **名前を上書きしない**。BFC/K3/$R^{\rm cyc}$ では `(5′)` は exact $b=1$ の等式、捻れ形は B-7$^{\rm tw}$。正しくは「**K5 campaign の operative bridge evaluation clause は (5$'_b$)。exact (5′) は $b_i=1$ の特殊化で (TB4) の下で回収される**」 | 便 47 F7.1 |
| **A5** | §1 | 「**1 述語・2 箇所**」「停止条件は不変」としつつ I-n を新設(**字義矛盾**) | **開示を精密化**: 「**変更する科学的 predicate は 1 つ。既存 I-d と既存結果遷移の意味は不変。付随する enforcement/provenance として I-n・凍結記録・結果 schema を追加**」 | 便 47 F7.2 |
| **A6** | §3 pairwise | 「両 BRIDGE-IN 成立時」だけを前件に見せていた | **antecedent bundle を明記**: FORMAL-IN・B-9′ の共通枠組み前件・両 BRIDGE-IN・§7.3 gate。**閉じていなければ `FRAMEWORK-UNKNOWN` 等であって bridge falsifier ではない** | 便 47 F7.3 |
| **A7** | §5-5 | `manifest_version` / `rule1_version`(可読名のみ) | **digest 束縛へ強化**: `manifest_sha256` / `rule1_sha256` / `bridge_predicate_id` / `results_schema_version` | 便 47 F7.4 |
| **A8** | §2・§4 | — | **F10.1 二段コミット schema**(`b_rule_commitment` / `b_value_i` / `b_value_source` / `b_observed_before_gk`)と **F10.2 証明書三分離**(`field_certificate` / `orientation_certificate` / `character_identity_certificate`)を組み込み | 便 47 F10・裁定 50 |
| **A9** | §2 I-n | 「fitting 違反 = 即時 integrity stop」 | **「汚染 run は隔離し、同 run の PASS/FAIL を救済しない」**を追加 | 便 47 F9 |

> **便 47 F4 の判定**: amendment の**中心設計は PASS**(捻れ形への変更・$\exists b$ 禁止・FAIL は固定 $b_i$ に対する反例 1 個・$b_{\rm sq}=b_{\rm ns}$ を pairwise の前に検査し不一致を I-d・fitting 違反を I-n・版跨ぎ比較の禁止)。**v2 が直すのは blocker 2 件と条文の精度のみ。**

---

## 0. なぜ直すのか(3 行)

1. 現 manifest / Rule 1 の bridge 述語は **untwisted** の $\rho_i(\mathrm{Ih}_N(\gamma))=\tau_i(\kappa_i(\gamma))$ を採る。
2. しかし定理として成立するのは **twisted** 形(**定理 B-7$^{\rm tw}$**、前件 (TB4$^{\rm u}$))である。exact $\varepsilon=1$(= (TB4))は**文献関所**で未閉鎖。
3. ゆえに $\varepsilon\not\equiv1\ (\mathrm{mod}\ 10)$ なら、現条文は**数学的に正しい橋を偽 FAIL にできる**。`bridge_result_i` はこの述語の PASS/FAIL/UNKNOWN を記録し、結果規則表はそれを入力にするので、**残留は条文だけでなく `bridge_result_i` の意味の中にある**。

> **`amendment now`**(便 46 F5.3): 現行の測定計画に actual shadow を外部経路で計算する工程はないが、**「測定計画に現れない」ことは述語の意味を $\varepsilon$-free にしない**。既知の偽 FAIL 条件を normative text に残す利点がない。

---

## 1. 変更面の開示(**A5 で精密化**)

> **変更する科学的 predicate は 1 つ**(bridge evaluation clause)。**既存 I-d と既存結果遷移の意味は不変。** 付随する **enforcement / provenance** として **I-n・凍結記録欄・結果 schema** を追加する。

| | 内容 |
|---|---|
| **科学的 predicate(1 つ)** | 「橋の PASS/FAIL をどの等式で判定するか」 — **Rule 1 §8.4** と **manifest BRIDGE-FAIL 条項①** |
| **enforcement / provenance(追加)** | **I-n**(fitting 禁止の強制)/ 凍結記録の $b$ 二段コミット欄 / 結果 schema の digest 束縛と証明書三分離 |
| **不変** | モデル正規形(§2)・selection と全順序(§3・§4)・uniformizer 決定(§5)・$u$ の二経路と受理規則(§6)・**$b_i$ の決定式 (7.1) と受理条件 (7.3)**・exact Kummer 判定器(§8.1–§8.3・§8.5)・**既存の停止条件 U-a〜U-f / I-a〜I-m(I-d を含む)の意味**・whitelist・**封印時点**・凍結 1 の不変条項・(P1)(P2) の**内容**・結果規則表の**遷移** |

> **記録の精度**: 「凍結 1 の内容は一行も変わらない」と書いてはならない。
> $$ \boxed{\text{凍結 1 の}\ \textbf{モデル探索・封印・抽出規律は不変}\ \text{。}\ \textbf{bridge evaluation clause のみ versioned amendment}\ (+\ \text{enforcement/provenance の追加})} $$

---

## 2. 条文案 A — `docs/week4-K5_Rule1_v1.md` §8.4 の差し替え(Rule 1 v1.4)

### 現行(v1.3)

> ### 8.4 (5′) の量化子
> $$ \rho_i(\operatorname{Ih}(\gamma)) = \tau_i(\kappa_i(\gamma))\qquad(\forall\gamma\in G_K). $$
> **有限個の Frobenius サンプル一致は較正であって PASS の証明ではない。** PASS は character 恒等の普遍的導出、または同値な Kummer 拡大の厳密同定を要する。**FAIL は exact な $\gamma$ 一つで足りる。**

### 改定案(v1.4)

> ### 8.4 bridge evaluation clause(v1.4 改定)
>
> #### 8.4.0 捻れ指数 $b_i$ の**二段コミット**
>
> **(F1) 凍結 1 で固定するもの(規則)**: §7.1 (7.1) の**決定アルゴリズム**、**向きの規約**(§1.2–§1.3・(1.6) の埋め込み・$\ell_i$ を正の向きの実 local monodromy とすること)、**入力 schema**($c_i$ と $\ell_i$ の型)、および**記録欄の存在**。**この段階で actual 値は存在しない**($c_i,\ell_i$ が個別モデルに依存するため)。
> **(F2) 凍結 2 / BRIDGE-IN で固定するもの(値)**: actual $b_i\in(\mathbb Z/10)^\times$ は、**Model-Builder が凍結対象モデルの $c_i,\ell_i$ から (7.1) により計算**し、**両翼 atomic 凍結 2 / BRIDGE-IN bundle に値として記録**する(既存 §9.3・§10-6・manifest の BRIDGE-IN 規定のとおり — **封印時点を変えない**)。
> **(F3) 順序の要件**: 記録された $b_i$ は、**$u$ の開示**・**bridge の $G_K$/shadow 観測**・**本節 8.4 の判定**の**いずれよりも前**に固定済みでなければならない。以後**再 fitting しない**。
> **(F4) 機械的検出のための schema**(凍結記録・結果 record 共通):
> ```text
> b_rule_commitment    = Rule1-(7.1) の digest             # 凍結 1
> b_value_i            = actual exponent (i = sq, ns)      # 凍結 2 / BRIDGE-IN
> b_value_source       = c_i, ell_i の artifact ID
> b_observed_before_gk = true                              # (F3) の宣言
> ```
> **★ 用語規律**: 「凍結」という同じ語で**式**と**値**を呼ばない。(F1) は *rule commitment*、(F2) は *value commitment* と呼ぶ。
>
> #### 8.4.1 判定式(捻れ形)
> $$ \boxed{\ \rho_i\bigl(\operatorname{Ih}_N(\gamma)\bigr)\ =\ \tau_i\bigl(\kappa_i(\gamma)^{\,b_i}\bigr)\qquad(\forall\gamma\in G_K).\ } \tag{5$'_b$} $$
> **$b_i$ は 8.4.0 (F2) の値。これが K5 campaign の operative bridge evaluation clause である。** 従来の exact **(5′)** は $b_i=1$ の特殊化であり、**(TB4)(= 枠組み単位 $\varepsilon=1$)の下で回収される**。**(5′) という既存の名前は上書きしない**(BFC/K3/$R^{\rm cyc}$ の数学文書では `(5′)` は exact $b=1$ の等式、捻れ形は B-7$^{\rm tw}$ を指す)。
>
> #### 8.4.2 PASS の証明書型(**限定列挙**)
> **有限個の Frobenius サンプル一致は較正であって PASS の証明ではない。** PASS は次の**いずれか**に限る。
> **(C-i) 普遍的 character 恒等**: **全 $\gamma\in G_K$** に対する (5$'_b$) の恒等式の導出。
> **(C-ii) oriented $\mu_{10}$-torsor 同型**: **凍結済みの $(\zeta_{10},\ \tau_i,\ j_i,\ b_i)$ と、選択した Kummer root** に対して、**左右作用と $G_K$-作用をともに保つ** $\mu_{10}$-torsor の同型を明示すること。
> **⛔ 除外(明示)**: **抽象的な体の一致・核の一致だけでは PASS にならない。** $d\in(\mathbb Z/5)^\times$ が非自明なら $\kappa_i$ と $\kappa_i^{\,d}$ は**同じ核・同じ巡回 Kummer 拡大** $K(\sqrt[10]{v_i})$ を与えるが、**固定された (5$'_b$) の character としては異なる**。したがって $\mathrm{Fix}(\ker)$ の等号は指数 $b_i$ を含む bridge を証明しない。
> **⛔ 除外(明示)**: `field_certificate` **単独**での PASS 宣言(§4)。
> **★ ord5 での観測 character の扱い**: $\mathrm{ord}([v_i]_{10})=5$ なら観測 character から指数を読み取れるが、その値は**凍結済み $b_i$ との照合(検証)にのみ**使用でき、**$b_i$ の選択には使えない**(8.4.3)。
> **FAIL**: **8.4.0 (F2) で固定済みの $b_i$** に対する **exact な反例 $\gamma$ 一つ**で足りる。
>
> #### 8.4.3 fitting の禁止(falsifiability の保全)
> > **$G_K$-データを見てから $b_i$ を選び直す(re-fitting する)ことを禁止する。** すなわち「**ある $b\in(\mathbb Z/10)^\times$ が存在して (5$'_b$) が成り立つ**」という**存在形での PASS 宣言を禁止**する。判定は常に **8.4.0 (F2) の 1 個の $b_i$** に対して行う。
> > **理由(A3 で修文)**: $\mathrm{ord}([v_i]_{10})=1$ の分岐では $\kappa_i(G_K)=1$ となり、右辺は $b\in\{1,3,7,9\}$ の**四つすべてで自明**になる。したがって**この分岐で空虚になるのは $b$ の同定・選択**である。
> > **⚠ bridge equality 全体が空虚になるのではない**: 左辺 $\rho_i(\mathrm{Ih}_N\vert_{G_K})$ が自明か否かは**依然として試験される** — 自明でなければ (5$'_b$) は **$b$ の値によらず FAIL** である。存在形を禁じる理由は、**$b$ を後から合わせて PASS を作れてしまう**ことにある。
> > **違反した場合**: §9 の新設 **I-n**。
>
> #### 8.4.4 pairwise 運用の順序
> 二 dessin を比較する前に、まず **§7.3 の integrity gate $b_{\rm sq}=b_{\rm ns}$** を通す。
> **数学的には $b_{\rm sq}=b_{\rm ns}$ は定理である**(同じ枠組み単位 $\varepsilon$ の $\bmod 10$ 還元 — BFC 補題 B-9′(a)。**前件は (TB4$^{\rm u}$) 等の共通枠組み前件であり framework-conditional である**)。**したがって §7.3 は「二つの独立 transport が共通値を実現したかを見る negative control」**であり、**不一致は新現象ではなく実装 transport の破損** ⇒ **既存 `I-d` の即時 integrity stop がそのまま正しい分類**である(§7.3 は撤回されず、役割が「規約」から「integrity 検査」へ明確化される)。
>
> #### 8.4.5 $\varepsilon$-free な結論(参考)
> 本節の捻れ化にかかわらず、次は $b_i$ の値に依存しない(BFC 系 B-8・補題 B-9′(c)(d)):
> **(P1)** $\mathrm{ord}([v_i]_{10})$ / **(P2)** $[v_{\rm ns}]_{10}=[v_{\rm sq}]_{10}^{a_{\rm eff}}$ と $a_{\rm eff}=a=1$ / **(R6-full)** 全射判定 / 固定体 $K(v_i^{1/10})$ / §8.3 の exact certificate。
> **⇒ 本 amendment は測定量を 1 つも変えない。**
> **★ 版の区別**: **amendment 成立後**は `bridge_result_i` を含む campaign 全判定が $\varepsilon$-free になる。**成立前は Belyi-side の限定結論だけ**が無条件である(BFC v2.4 §10.1.2 (e))。

### 付随:§9 への 1 行追加(Rule 1 v1.4)

> | **I-n**(v1.4) | **§8.4.3 に反して $b_i$ を $G_K$/shadow 観測後に再 fitting した / 存在形($\exists b$)で bridge の PASS を宣言した / `b_observed_before_gk` が偽または欠落** ⇒ **falsifiability の毀損として即時 integrity stop**。**当該 run は汚染として隔離し、同一 run 内の他の PASS/FAIL を救済しない**(部分的な結果採用を禁じる)。再実施は**新 run** として行う |

---

## 3. 条文案 B — `docs/manifest_k5_v1.md` BRIDGE-FAIL 条項①の差し替え(manifest v1.6)

### 現行(v1.5)

> | **BRIDGE-FAIL**(= B_FC の真の falsifier) | ①個別橋: BRIDGE-IN 独立成立下で **actual $G_K$-置換と $\tau\kappa$ の exact 不一致**、または **(P1) の exact な破れ**(前件札が独立に閉じている場合 — (5′) の候補反例)②pairwise: 封印予測 (P2)/(5.5) の exact な破れ(両 BRIDGE-IN 成立時 —「少なくとも一方の (5′) が偽」までを主張し、どちらかは同定しない) |

### 改定案(v1.6)

> | **BRIDGE-FAIL**(= B_FC の真の falsifier) | **①個別橋**: 下記 **antecedent bundle** が成立する下で、**Rule 1 §8.4.0 (F2) で値としてコミットされた $b_i$** に対する **(5$'_b$) $\rho_i(\operatorname{Ih}_N(\gamma))=\tau_i(\kappa_i(\gamma)^{b_i})$ の exact な反例 $\gamma$ が一つ得られること**(**存在形 $\exists b$ による判定は禁止** — Rule 1 §8.4.3)、または **(P1) の exact な破れ**。**②pairwise**: 同じ antecedent bundle の下で封印予測 (P2)/(5.5) が exact に破れること ⇒「**少なくとも一方の (5$'_b$) が偽**」までを主張し、どちらかは同定しない |

> **antecedent bundle(新設・A6)**: ①② いずれも次が**すべて**成立していることを前件とする。
> **(AB-1)** FORMAL-IN((0)(1)(2)(3)(5′)(6′))
> **(AB-2)** BFC 補題 B-9′ の**共通枠組み前件**((TB1)(TB2)(TB3)(TB4$^{\rm u}$)+(CAL)+ 両 detector の (W1)–(W5) と **(6′-ii)** + 補題 K5-a)
> **(AB-3)** 両 dessin の BRIDGE-IN(**独立**成立)
> **(AB-4)** Rule 1 §7.3 の gate $b_{\rm sq}=b_{\rm ns}$
> **いずれかが閉じていなければ、分類は `FRAMEWORK-UNKNOWN` / `SCHEMA-OUT` / `MODEL-UNKNOWN` 等であって bridge falsifier ではない。**

### 付随:manifest v1.6 の注記

> - **K5 campaign の operative bridge evaluation clause は (5$'_b$) である**(BFC 定理 B-7$^{\rm tw}$)。**従来の exact (5′) は $b_i=1$ の特殊化**であり、**(TB4)(exact $\varepsilon=1$)の下で回収される**。**(5′) の名前は上書きしない。**
> - **(TB4) は現在も文献関所 `FRAMEWORK-UNKNOWN`。**
> - **`bridge_result_i` の意味は本 amendment で変わる。** 旧版(untwisted 述語)の値と新版(twisted 述語)の値は**同じ列名でも比較不能**。結果記録は §4 の digest 束縛で版を機械的に区別する。

---

## 4. 結果 record schema(`provenance/results_k5.md`)— **A7 + A8**

```text
# 版の束縛(可読名だけでは不十分 — 同名 artifact の差替えを機械的に排除する)
manifest_sha256          # 適用した manifest の digest
rule1_sha256             # 適用した Rule 1 の digest
bridge_predicate_id      # 例: "5prime_b/v1"(untwisted 版は "5prime/v0")
results_schema_version

# b の二段コミット(F10.1)
b_rule_commitment        # Rule1-(7.1) digest         [凍結 1]
b_value_sq, b_value_ns   # actual exponents           [凍結 2 / BRIDGE-IN]
b_value_source           # c_i, ell_i の artifact ID
b_observed_before_gk     # true/false(false or 欠落 ⇒ I-n)

# 証明書の三分離(F10.2)
field_certificate                 # 核・固定体を証明する(exponent は証明しない)
orientation_certificate           # 凍結済み (zeta10, tau_i, j_i, b_i) と Kummer root の向き
character_identity_certificate    # (5'_b) の character 恒等(全 gamma)

# 既存
bridge_result_sq / bridge_result_ns  in {PASS, FAIL, UNKNOWN}(PASS には ord_i)
pair_gate            in {PASS, FAIL, OPEN}
saturation_result    in {PROVED, REFUTED, NOT_PROVED}
```

> **★ 三分離が防ぐもの**: `field_certificate` は核と固定体を証明するが **(5$'_b$) の exponent までは証明しない**。三つを別欄にすることで、**ord5 における「体が合ったから PASS」という誤 PASS を機械的に排除**できる(便 47 F10.2)。**PASS 宣言には `character_identity_certificate`(= C-i)または `orientation_certificate`(= C-ii)が必須**であり、**`field_certificate` 単独では不可**。

---

## 5. 適用後に BFC 本稿で強められる主張(司令塔への申し送り)

> **(e′)(amendment 成立後)** $K^{(5)}$ campaign の**全判定** — `bridge_result_i`(PASS/FAIL/UNKNOWN と $\mathrm{ord}_i$)・`pair_gate`・`saturation_result`・結果規則表の**全遷移** — が exact $\varepsilon$ に依存しない。

**それまでは (e) は「(P1)(P2)(R6-full)・固定体・Kummer 証明書型・現行 Belyi-side 測定量」までに限定する**(BFC v2.4 §10.1.2・便 47 F2.3)。

---

## 6. 手続き(司令塔の作業)

1. **本草案 v2 を差分ゲートに掛ける**(便 47 F12-5: 差分が PASS してから新 version を作る)。
2. **凍結正本を上書きしない。** `docs/manifest_k5_v1.md` → **v1.6**、`docs/week4-K5_Rule1_v1.md` → **v1.4** として新 version を作る(旧版は digest 込みで保存)。
3. **凍結記録**(Rule 1 §10)に「amendment 適用日時・旧版 digest・変更した clause 名・`bridge_predicate_id`」を追記。
4. 適用後、**BFC 本稿の (e) を (e′) へ更新**し、その版で final digest を取り直す(GAP certificate の `input_doc_path` 束縛も同時点)。
5. `provenance/results_k5.md` に §4 の schema を実装。

> **★ TB4 の成否を待つ必要はない**(便 47 F10.3): 将来 $\varepsilon=1$ が証明されても、**「事前コミットした $b_i$ を測る / 観測後 fitting を禁ずる / actual 値と定理値の不一致を integrity failure とする」という規範は regression control として残すべき**である。$\varepsilon\ne1$ なら本 amendment がそのまま必要になる。**したがって条文設計は TB4 の成否と独立に確定できる。**

---

## 7. 起草者の自己申告(v2 で監査してほしい点)

1. **8.4.2 (C-ii) の「oriented $\mu_{10}$-torsor 同型」の定義**が十分に operational か。私は「凍結済み $(\zeta_{10},\tau_i,j_i,b_i)$ と選択した Kummer root に対し、**左右作用と $G_K$-作用をともに保つ**同型」と書いたが、**実装者が何を出せば足りるか**が一意に読めるか。
2. **8.4.3 の修文**(空虚なのは $b$ の同定だけ)が、**ord1 分岐での FAIL 判定**を正しく残しているか — 私は「左辺が自明でなければ $b$ によらず FAIL」と書いた。
3. **8.4.0 (F3) の順序要件**が、既存の凍結 2 = 両翼 atomic joint freeze(manifest v1.2 P3)と**時点の衝突を起こしていない**か。
4. **§3 の antecedent bundle (AB-1)–(AB-4)** に過不足はないか(とくに (AB-2) に **(6′-ii)** を入れた判断)。
5. **I-n の「汚染 run 隔離」**が既存 **I-h**(hash・発射錠)や **I-i** と**重複・矛盾していない**か。
