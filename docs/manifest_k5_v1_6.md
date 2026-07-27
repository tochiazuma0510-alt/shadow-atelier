# 事前登録 manifest — K⁽⁵⁾ 算術飽和キャンペーン v1.6(2026-07-28・司令塔)

> **v1.6(裁定 66・裁定 67 で修理)= v1.5 + amendment v8(`docs/amendment_5prime_draft.md` 条文案 B)。旧正本 v1.5 は不変・digest 固定**(`docs/manifest_k5_v1.md` はこの版イベントで一切編集していない)。**版イベント発火許可 = 裁定 66 Part A**(`sol/裁定_66_ben54.md`)。本版が変更するのは **五札封印表の BRIDGE-FAIL 行(①差し替え)・antecedent bundle 節の新設・結果 record schema への digest 束縛欄の追加**、および**それに伴う predicate 型の下流同期**である。**Part B 由来の whitelist/schema 修理(N_infty 隔離・h 非開示等)はここに混入しない**(裁定 66 F4 — 別ゲート)。他の全節(宇宙・五札封印表の他行・規約捻れの型・封印予測・BRIDGE-IN 構築の独立性・S5 の紙上 ansatz・較正三層の記述本体・工程と発射条件の発射条件本文・即時 integrity stop・撤退条件)は**逐語不変**。**科学的 predicate は 1 つ(operative $(5'_b)$)のままだが、旧 $(5′)$ をそのまま複製していた下流 normative 面 4 箇所(exact 判定の証明書型・結果規則表 pairwise 行・較正三層 covariance controls の型注記・工程と発射条件の算術全射性禁止条件)は、便 55 F4.2 の指摘に基づき本版で predicate 型へ同期する。**「exact 判定の証明書型・結果規則表等は逐語不変」という当初の変更面宣言は撤回する**(便 55 F4.2 末尾)。

> v1.4 → v1.5(便 38・裁定 39): F8-6 の sealed automation・positive-only 非網羅規則を changelog から **operative な工程節へ転記**+実 K5 Freeze 2 の「同一 bundle から係数ごと読む」不変条件(F1.3)を追加。

> v1.3 → v1.4(便 36 条件 4・裁定 37): **I-b∞ の逐語反映** — whitelist 禁止と即時 integrity stop の双方に「(N_∞) 枝の ĉ_μ(μ の norm 定数)の値・平方類・平方因子・符号」を追加(I-b∞: (N_∞) では (P1) ⟺ ĉ_μ ∈ K^{×2} — ĉ_μ 単独が封印予測を決める)。**μ/Pell ansatz の human-visible な探索は strict I-b∞ を守る sealed automation schema の事前登録なしに禁止**。(N_∞) 探索器が未設計の間は当該枝について「候補なし」と報告してはならず、既設二枝のみの探索は非網羅・全体結論 BRIDGE-UNKNOWN 維持を委嘱文に明記する。
> v1.2 → v1.3(便 32 P1/P3・裁定 31): 結果規則を total transition table 化(UNKNOWN+UNKNOWN 追加・REFUTED 新設 = 便 35 で批准済)・whitelist に Rule 1 I-b と同語の禁止を反映。

> v1.1 → v1.2(便 31 差戻しの全採用・裁定 29): ①fixture 実データ表(付録 A)の実体化を必須化(P1 — **実体化済: docs/manifest_k5_appendixA_v1.md**・K5-sq `a49252af…6716`・K5-ns `0ce28a6d…cd81`・K3-regression `70f2a604…9ed9`(sha256・機械計算)。付録 A 内の新設 tie-break 2 規則(代表 H の辞書式最小・σ₀ ラベル付け)は Sol 検収対象)②凍結 1 の時点を一意化・「または初期」削除(P2)③凍結 2 = 両翼 atomic joint freeze(P3)④formal a = 1 は永久不変・橋側捻れは b_sq/b_ns・比較指数 a_eff(P4 — v1.1 の「a ↦ ab⁻¹ 更新」は誤りとして撤回・裁定 29-2)⑤exact Kummer 証明書型(P5)⑥結果規則表と結果記録の分離(P6)⑦Model-Builder whitelist・u 二経路の独立性要件(P7)⑧即時 integrity stop 条件(P8)⑨S5 紙上 ansatz と Rule 1 要件(P9)。
> v1 → v1.1: falsifier 監査(F1・W1–W3・P1–P2)全採用。

## 宇宙(事前登録・変更禁止)

- 窓: K⁽⁵⁾ = ker ψ₅(= K⁽¹⁰⁾・Prop 3.4 — 独立二例として二重計上禁止)。P = G₅(位数 500)・M = 10・e = 5・𝔉₀ = C₅・K = ℚ(ζ₂₀)。
- 標的: **target_policy = all_two_classes**。Λ_sq(α ∈ {1,4})と Λ_ns(α ∈ {2,3})の二 fixture。標的 dessin: 次数 10・種数 2・ordered (10,2⁴1²,10)・Aut = 1(固定 U 上の ordered dessin の圏)。**結果を見て一方を捨てる = NO-GO**。
- 検出器: degree M = 10(μ₁₀-torsor)。degree 5 detector は SCHEMA-OUT(便 29 W3)。
- **fixture の実体(付録 A・必須)**: dessin ごとに fixture_id / marking_version((X,Y,Z) 正本と作用規約)/ H_generators(G₅ 固定座標での生成元列)/ perm_triple((σ₀,σ₁,σ_∞) ∈ S₁₀³)/ normalization_algorithm(同時共役の正規化と tie-break)/ **sha256(canonical serialization の digest — serialization 規約(UTF-8・改行 LF・配列順序)も付録 A に固定)**/ evidence_ids(node/GAP の検査項目と出力 artifact)を**値として**記載する。K5 finite fixture・K3 regression fixture も同形式で実体化。**付録 A が埋まるまで本 manifest は「凍結済み発射物」ではない**(便 31 F1.2・★教材 19: hash は書かれて初めて seal)。

## 五札封印表

| 札 | 内容 |
|---|---|
| **FORMAL-IN** | (0)(1)(2)(3a–d)(6′-i)(6′-ii) の証拠 ID(付録 A・dessin 別行)・命題 K5-1・j_i の定義・**封印値 a = j_ns⁻¹j_sq = 1(formal invariant・永久不変)**。(5′) は `PENDING`(結果は本ファイルでなく結果記録に書く — 下記)。結論との不一致 = proof/record consistency failure |
| **BRIDGE-IN**(凍結 2 で確定・dessin ごと) | 明示 ℚ-モデル式+hash・branch map(0,1,∞ ↦ X,Y,Z の actual conjugator の**完全な置換データ**)・全分岐 cusp・ℚ-有理 uniformizer(式)・局所助変数の式・FC 比較規約の版・**τ 由来一式**(原始根 ζ₁₀ := ζ₂₀² と K 内での表現・向き τ(ζ₁₀)(H′) = XH′X⁻¹・loop の向きと左右作用・Kummer cocycle を γ(s^{1/10})/s^{1/10} と読む規約・ρ₀ 側 generator と j: μ₁₀[5] ≅ 𝔉₀ の対応)・**b_sq, b_ns の機械記録**(下記)。**受理条件: b_sq = b_ns**(不一致は規約不整合として停止・u を開けない) |
| **BRIDGE-FAIL**(= B_FC の真の falsifier・**v1.6 改定 — 条文案 v8 §3「条文案 B」の逐語転記**) | **①個別橋**: 下記 **antecedent bundle** が成立する下で、**Rule 1 §8.4.0 (F2) で値としてコミットされた $b_i$** に対する **(5$'_b$) $\rho_i(\operatorname{Ih}_N(\gamma))=\tau_i(\kappa_i(\gamma)^{b_i})$ の exact な反例 $\gamma$ が一つ得られること**(**存在形 $\exists b$ による判定は禁止** — Rule 1 §8.4.3)、または **(P1) の exact な破れ**。**②pairwise**: 同じ antecedent bundle の下で封印予測 (P2)/(5.5) が exact に破れること ⇒「**少なくとも一方の (5$'_b$) が偽**」までを主張し、どちらかは同定しない |
| **BRIDGE-UNKNOWN** | 明示モデル・actual marking・局所比較・**exact Kummer 証明書**のいずれかを閉じられない — 値を推測せず UNKNOWN(探索失敗は判定でない) |
| **SCHEMA-OUT** | bad H(degree 5 detector)・非 regular・Λ 不安定・ρ₀ 非忠実。将来欄: 8\|n の K⁽ⁿ⁾ 一律(命題 K5-2b・K5e 機械裏取り済・裁定 27) |

> **旧文(v1.5・撤回)**: 「①個別橋: BRIDGE-IN 独立成立下で actual $G_K$-置換と τκ の exact 不一致、または (P1) の exact な破れ(前件札が独立に閉じている場合 — (5′) の候補反例)②pairwise: 封印予測 (P2)/(5.5) の exact な破れ(両 BRIDGE-IN 成立時 —「少なくとも一方の (5′) が偽」までを主張し、どちらかは同定しない)」。**差し替え理由と派生注記は下記「付随:manifest v1.6 の注記」を見よ。**

### antecedent bundle(**v1.6 新設 — 条文案 v8 §3「antecedent bundle」の normative-only transfer**)

**⚠ 循環の除去(便 48 F3.2・裁定 53)**: (5′)/(5$'_b$) を前件に置くと、falsifier を論理的に殺す循環になる — (i) 個別反例が「(5′) を真と仮定して (5$'_b$) の破れを探す」ことになり、(ii) (P1) の破れは (5′)+(6′) から $\mathrm{ord}([u^{-1}]_M)\mid e$ を出す $R^{\rm cyc}_{\rm formal}$ と正面衝突して反証分岐が空になり、(iii) pairwise の「少なくとも一方の橋が偽」を言いたいのに前件で exact bridge を真と置いてしまう。**⇒ bundle を目的別に二つに分ける。同じ名前で兼用しない。**

#### (B-I) `THEOREM-ANTECEDENT-Rcyc/*` — **定理を適用する側**

```text
base = FORMAL-IN(下記 B-II の (AB-1) と同内容)
     + B-9' の共通枠組み前件((AB-2) と同内容)

THEOREM-ANTECEDENT-Rcyc/twisted/v1 = base + (5'_b)
THEOREM-ANTECEDENT-Rcyc/exact/v1   = base + (5')  + (b_i = 1)
```

- **`/twisted/v1`** — K5 campaign が実際に使う側。**operative predicate = (5$'_b$)**。
- **`/exact/v1`** — exact (5′) を使う側。**追加前件 $b_i=1$ が要る**。**その回収経路は 2 通りあり、どちらを指すかを名指しする**:
  - **(R-a) 現行 BFC proof を採る場合**: **(TB4)+$(Z_{2M}$-link$)$**(BFC v2.11 §8・§8.1 の**現行 proof ID**・**current source**)。**本 campaign が採るのはこちら。**
  - **(R-b) TB4-E alternate を採る場合**: **(E-i)–(E-iv)+別 proof ID**(TB4 導出側の別証)。**現行 BFC proof と前件を混ぜない。**
  `bridge_predicate_id` と併せて **`exact_recovery_path` ∈ {`R-a/current-bfc-proof`, `R-b/tb4e-alternate`} を結果 record に記録**する。
**この bundle の下で結論が破れたら、それは `THEOREM/RECORD-CONSISTENCY-FAIL`(証明か記録の誤り)であって橋の反証ではない。**
**★ 結果 record の `antecedent_bundle_id` は predicate version まで区別する**(`.../twisted/v1` と `.../exact/v1` を同一視しない)。

#### (B-II) `FALSIFIER-ANTECEDENT-BFC/twisted/v1` — **橋を試す側**

BRIDGE-FAIL ①② が参照するのは**こちら**。**(5′) 系を一切含まない。**

```text
FALSIFIER-ANTECEDENT-BFC/twisted/v1
  = (AB-1) + (AB-2) + (AB-3) + (AB-4)
```

**(AB-1)** **現行 manifest v1.5 の FORMAL-IN(逐語転記)**:
> 「(0)(1)(2)(3a–d)(6′-i)(6′-ii) の証拠 ID(付録 A・dessin 別行)・命題 K5-1・$j_i$ の定義・**封印値 $a=j_{\rm ns}^{-1}j_{\rm sq}=1$(formal invariant・永久不変)**。**(5′) は `PENDING`**」
> **⇒ (5′) および (5$'_b$) は (AB-1) に含めない。**
**(AB-2)** BFC 補題 B-9′ の**共通枠組み前件**((TB1)(TB2)(TB3)(TB4$^{\rm u}$)+(CAL)+ 両 detector の (W1)–(W5) と **(6′-ii)** + 補題 K5-a)。**(AB-1) と (6′-ii) が重複しても害はない** — theorem provenance と campaign evidence は役割が違うので両方に残す。
**(AB-3)** 両 dessin の BRIDGE-IN(**独立**成立)
**(AB-4)** Rule 1 §7.3 の gate $b_{\rm sq}=b_{\rm ns}$
**いずれかが閉じていなければ、分類は `FRAMEWORK-UNKNOWN` / `SCHEMA-OUT` / `MODEL-UNKNOWN` 等であって bridge falsifier ではない。**

**★ 結果 record には `antecedent_bundle_id` を記録する。許される値は次の 3 つだけ**(closed enumeration — 未知の値・version なしの値は fail-closed で記録を拒否し integrity stop):
```text
THEOREM-ANTECEDENT-Rcyc/twisted/v1
THEOREM-ANTECEDENT-Rcyc/exact/v1
FALSIFIER-ANTECEDENT-BFC/twisted/v1
```
**どちらの帽子で判定したかを後から選べないようにする**(便 29 ★教材 3 の系)。

### 付随:manifest v1.6 の注記(条文案 v8 §3 の逐語転記)

- **K5 campaign の operative bridge evaluation clause は (5$'_b$) である**(BFC 定理 B-7$^{\rm tw}$)。**従来の exact (5′) は $b_i=1$ の特殊化**であり、**(R-a) (TB4)+$(Z_{2M}$-link$)$ または (R-b) TB4-E alternate の (E-i)–(E-iv) の下で回収される**(上記 `(B-I)` の `/exact/v1` を参照・**どちらの経路かを名指しする**)。**(5′) の名前は上書きしない。**
- **(TB4) は現在も文献関所 `FRAMEWORK-UNKNOWN`。**
- **`bridge_result_i` の意味は本 amendment で変わる。** 旧版(untwisted 述語)の値と新版(twisted 述語)の値は**同じ列名でも比較不能**。結果記録は §「結果規則表と結果記録の分離」の digest 束縛で版を機械的に区別する。

- B5 の札は二段を維持: 形式 FAIL(M = 10 合成数)+ primary 分離で迂回 — PASS に塗り替えない。

## 規約捻れの型(v1.2 で全面差替え・裁定 29-2)

- 凍結 1 で決定式を封印: 各 dessin の凍結済み sheet identification c_i と正向き実 local monodromy ℓ_i に対し **c_i ℓ_i c_i⁻¹ = τ_i(ζ₁₀^{b_i})** — τ_i 単射より b_i ∈ (ℤ/10)^×(候補は 1,3,7,9 の 4 つ)は一意。右辺の巡回群に属さなければ actual marking 未閉 = BRIDGE-UNKNOWN。
- **formal invariant a = 1 は永久不変**(有限群側の封印・K5-1 の帰結)。橋側の記録は b_sq, b_ns と **a_eff = b_ns⁻¹ · a · b_sq**(別欄)。(P2) の一般形は [u_ns⁻¹]₁₀ = [u_sq⁻¹]₁₀^{a_eff} — ただし受理条件 b_sq = b_ns の下では a_eff = 1 で完全一致形に戻る。
- (ℤ/20)^× からの lift 2 対 1 は別封印項目として付録 A に記載。

## 封印予測(u 開示前・破れうる形で登録)

- **(P1)** ord([u_i⁻¹]₁₀) ∈ {1, 5}(i = sq, ns)。**exact な破れ(位数 2/10)は、前件札が独立に閉じていれば BRIDGE-FAIL 候補・どの前件が壊れたか未確定なら integrity quarantine**(新現象とも記録事故とも断定しない)。
- **(P2・主整合ゲート)** [u_ns⁻¹]₁₀ = [u_sq⁻¹]₁₀ in K^×/K^{×10}(b_sq = b_ns 受理下・生の u 一致は要求しない)。
- 観測列プロトコル(K3 v2 §6 継承): q_*[u] ∈ ⟨[2]⟩ の盲検記録(予測ではない・即時棄却規準あり)。

## exact 判定の証明書型(v1.2・便 31 F2.2/F2.3)

- v_i := u_i⁻¹。**位数 1 の陽性**: 明示 witness c ∈ K^× with c¹⁰ = v_i。**位数 5 の陽性**: c¹⁰ = v_i⁵ **かつ** v_i ∉ K^{×10} の exact obstruction(素イデアル valuation が 10 の倍数でない/単数・1 の冪根成分の exact obstruction/T¹⁰ − v_i の非可解の厳密数体証明書、のいずれか)。**探索失敗のみ = UNKNOWN**(浮動小数点 root search は証明書でない)。
- **(P2) 判定**: r := v_ns / v_sq^{a_eff} について r ∈ K^{×10} の witness(PASS)/ exact obstruction(FAIL)。二経路が同じ代表を返したことだけでは閉じない(W5)。
- **(5$'_b$) の量化子(v1.6・便 55 F4.2 — Rule 1 §8.4.2 と同文に同期)**: operative predicate は ∀γ ∈ G_K の (5$'_b$) 恒等。有限個の Frobenius サンプル一致は較正であって PASS の証明でない。**PASS は次のいずれかに限る**: **(C-i) 普遍的 character 恒等**(全 γ ∈ G_K に対する (5$'_b$) の恒等式の導出)、または **(C-ii) oriented μ₁₀-torsor 同型**(凍結済みの (ζ₁₀, τ_i, j_i, b_i) と選択した Kummer root に対し、左右作用と G_K-作用をともに保つ μ₁₀-torsor の同型の明示)。**⛔ 抽象的な体の一致・核の一致だけ、および `field_certificate` 単独での PASS 宣言は明示的に拒否する**(field/kernel-only PASS の排除)。**exact (5′) を扱う場合はこの限定列挙の対象に含めず、`/exact/v1`(上記 antecedent bundle (B-I) 参照・`exact_recovery_path` の名指しを要する)として別記する。** FAIL は exact な γ 一つで足りる。
  > **旧文(v1.5・撤回)**: 「(5′) の量化子: ∀γ ∈ G_K の恒等 … PASS は character 恒等の普遍的導出 or Kummer 拡大の厳密同定」— untwisted (5′) を operative predicate であるかのように書いており、撤回済みの predicate と現行 operative (5$'_b$) が混在していた(便 55 F4.1 の blocker)。

## 結果規則表と結果記録の分離(v1.2・便 31 F1.3/F6.1)

- **manifest は開示後も不変**。結果は別 versioned record `provenance/results_k5.md` に bridge_result_sq / bridge_result_ns ∈ {PASS, FAIL, UNKNOWN}(PASS には ord_i ∈ {5, 1} を付記)・pair_gate ∈ {PASS, FAIL, OPEN}・saturation_result ∈ {PROVED, **REFUTED**, NOT_PROVED} を保存し、凍結 manifest の digest を参照する。**REFUTED は v1.3 で司令塔が追加**(橋が閉じて ord = 1 なら fake shadow の存在 = 飽和の反証であり NOT_PROVED と区別すべき決着 — 便 34 で Sol 確認対象)。
- **(v1.6 新設 — 条文案 v8 §5-5/A7・§4 の逐語転記)結果 record の版の束縛**: 可読名(`manifest_version`/`rule1_version`)だけでは同名 artifact の差替えを排除できないため、`provenance/results_k5.md` の各 record は次を digest として記録する:
  ```text
  manifest_sha256          # 適用した本 manifest(v1.6)の digest
  rule1_sha256             # 適用した Rule 1(v1.4)の digest
  bridge_predicate_id      # 例: "5prime_b/v1"(untwisted 版は "5prime/v0")
  results_schema_version
  ```
  上記に加え、`antecedent_bundle_id`(上記 closed enumeration の 3 値のみ)・`exact_recovery_path`(discriminator = `antecedent_bundle_id`。`.../exact/v1` のときのみ REQUIRED で `{R-a/current-bfc-proof, R-b/tb4e-alternate}` のいずれか一つ、それ以外は PROHIBITED — 記入は integrity stop)・Rule 1 §8.4.0 (F4) の二段コミット欄(`b_rule_commitment`・`b_value_sq`/`b_value_ns` = `b_op`・`b_semantics = "op"`・`b_cmp_value`・`root_system_tb2_id`・`rule1_root_2M_id`・`root_twist_2M_value`・`root_twist_mod_M_value`・`b_value_source`・`b_observed_before_gk`・`z20_link_seal_id`・`root_equality_edge_id`・`equality_certificate_digest`)・証明書三分離(`field_certificate`/`orientation_certificate`/`character_identity_certificate`)を記録する。**詳細 schema は `docs/amendment_5prime_draft.md` §4 を正本とし、本節はそこへの digest 束縛欄のみを manifest 側に固定する。**

- **(v1.6 新設・裁定 67 — 便 55 F6.2)結果 schema の authority 優先順位**: Rule 1 §10 (F4 記録欄 8.)・manifest(本節)・amendment §4 の三つが並んで「結果 schema の正本」を名乗る事故を防ぐため、次の 4 段を明文化する。
  1. **$b$ の二段コミットと typed semantics** は **Rule 1 §8.4.0/F4 が正本**(`b_rule_commitment`/`b_value_i`/`b_semantics`/`b_cmp_value`/`root_system_tb2_id`/`rule1_root_2M_id`/`root_twist_2M_value`/`root_twist_mod_M_value`/`b_value_source`/`b_observed_before_gk`/`z20_link_seal_id`/`root_equality_edge_id`/`equality_certificate_digest` の定義・型)。
  2. **bundle ID の closed enum と `exact_recovery_path` の conditional presence rule** は **manifest v1.6(本節・「antecedent bundle」節)が正本**。
  3. **amendment §4** は、上記 1/2 の適用元であり、**残余詳細**(route evidence・ordering evidence・orientation certificate 構造)の source である。**専門正本 1/2 の定義と衝突した場合は 1/2 を優先**する。
  4. **`provenance/results_k5.md`(または専用 schema artifact)** は 1–3 の union を **materialize** する record であり、**独自定義を追加しない**。両文書(Rule 1・manifest)の digest と schema digest を束縛する。
  **hard stop 条件**: `results_k5.md`(または専用 schema artifact)の作成・digest 監査が閉じるまで、**Freeze 2 / BRIDGE-IN / bridge_result 記録は hard stop**とする。この条件を満たす限り、`results_k5.md` を Freeze 2 より前に実体化することは受理できる。
- **結果規則(total transition table・v1.3・便 32 P1)** — 非順序対 {sq, ns} の全状態を尽くす:

| 状態(非順序) | pair_gate | saturation_result | 記録 |
|---|---|---|---|
| PASS(ord5) + PASS(ord5)・(P2)/(6.2) 一致 | PASS | PROVED | 完全決着 |
| PASS(ord5) + PASS(ord5)・(P2) exact 破れ | FAIL | NOT_PROVED | pairwise BRIDGE-FAIL(「少なくとも一方の **(5$'_b$)** が偽」— どちらかは同定しない・便 55 F4.2)・integrity quarantine |
| PASS(ord5) + PASS(ord1) | FAIL | NOT_PROVED | 両橋閉鎖下では矛盾(両者とも Ih 像を計算しているため)⟹ integrity quarantine |
| PASS(ord1) + PASS(ord1)・(P2) 一致 | PASS | **REFUTED** | fake shadow の存在(反証側の決着 — 台帳は W3 三値の fake) |
| PASS(ord5) + FAIL | FAIL | PROVED | 存在型は成立・橋の dessin 非依存性は反証・FAIL 側を捨てない |
| PASS(ord1) + FAIL | FAIL | REFUTED | 同上(反証側) |
| PASS(ord5) + UNKNOWN | OPEN | PROVED | 存在型 witness・(P2) は「未検証」・両翼閉鎖まで campaign OPEN |
| PASS(ord1) + UNKNOWN | OPEN | REFUTED | 反証は片翼で数学的に成立・(P2) 未検証 |
| FAIL + UNKNOWN | FAIL | NOT_PROVED | 個別 bridge falsifier 記録 |
| FAIL + FAIL | FAIL | NOT_PROVED | pairwise falsifier 記録 |
| UNKNOWN + UNKNOWN | OPEN | NOT_PROVED | falsifier なし(便 32 F1.5) |

- 付則: (P1) exact 破れ(ord 2/10)は当該 dessin の bridge_result を確定させる前に integrity quarantine(前件札が独立に閉じていれば BRIDGE-FAIL 候補)。u 二経路不一致は結果を記録せず integrity stop。**「存在型の定理」「橋の普遍性」「全二類整合 campaign」は別出力**(W6)。

## BRIDGE-IN 構築の独立性(v1.1 設置・v1.2 強化)

1. **凍結 1(Rule 1)**: **両 dessin のいかなる個別モデル候補・係数・数値近似にも接する前・探索コマンドを一度も実行する前**に完了する(「初期」条項は削除 — W2)。内容: モデルの同値関係と正規形アルゴリズム・複数候補の全順序と tie-break・y の符号/基底三点/sheet numbering・cusp と uniformizer の決定アルゴリズム(**λ/t¹⁰ の定数項正規化は u を使うため禁止**・P₀ が Weierstrass 点か否かの分岐も先に書く)・「一意に決まらなければ UNKNOWN」規則・**u 二経路の数式・実装版・受理規則**・**b_i の決定式 (5.1)**・exact 数体/Kummer 判定器の版。
2. **凍結 2 = atomic joint freeze**: 両モデル・両 actual marking・両 uniformizer を**一つの bundle として同時に**凍結(★教材 20: 一翼を開く前に両翼を殺す)。片翼しか得られない場合は保存のみ・Extractor 起動は保留(片翼先行は別 manifest の別キャンペーン)。
3. **役割分離**: Model-Builder(A)の出力 **whitelist** — 許可: 明示モデル・Belyi map・分岐 divisor・cusp・uniformizer の式・target triple への exact conjugator(分岐指数 10 や uniformizer 性の証明は許可)。**禁止: λ/t¹⁰ の非零定数項とその同値物(leading coefficient・その valuation/class)、Rule 1 I-b と同語で「c の平方類・平方因子・符号の計算、λ の (c, μ) 対への分離報告」、および **I-b∞ と同語で「ĉ_μ の値・平方類・平方因子・符号の計算」(v1.4)**・それらを候補選択に使うこと**。A は「u 未計算」を申告し全 transcript 保存。**主根拠 = 凍結済み入出力 schema+役割別 access log・grep は補助検査**(W4)。Extractor(B)は凍結 2+発射錠後にのみ起動・規約変更権なし。
4. **u の二経路**(cusp 展開 × Vieta/単数): 非共有 helper・別中間表現・raw 出力の別保存・**一致判定のみを行う第三 checker**。不一致時は平均・符号調整・座標再選択を禁止し即 integrity stop / BRIDGE-UNKNOWN。
5. **hash commitment**: canonical serialization の digest・UTC/JST timestamp・commit ID・凍結対象の全ファイル一覧・**発射錠 FIRE_k5bridge.auth はこの digest 組に束縛(一回性・別 artifact へ再利用不可)**。

## S5 の紙上 ansatz(v1.2・便 31 F9 採録)

- Riemann–Hurwitz: 2g−2 = −20+(9+4+9) = 2・g = 2。divisor 恒等式を係数 ansatz より先に使う: (λ) = 10P₀ − 10P_∞・(λ−1) = 2Q₁+…+2Q₄+R₁+R₂−10P_∞・(dλ) = 9P₀+Q₁+…+Q₄−11P_∞。
- **紙上フィルタ**: [P₀−P_∞] ∈ J(C)(ℚ)[10] で **ord ∈ {5, 10}**(位数 1 は不可能・位数 2 は超楕円対合が λ を固定して Aut = 1 に反する)。
- **λ ∈ ℚ(x) と仮定してはならない**: 超楕円対合が deck 変換になり Aut = 1 に反する。**λ = A(x) + B(x)y, B ≠ 0** を許す(★教材 21)。二 dessin は同一曲線とは限らない — 「同時」は共同凍結の意味であり同一 ansatz の強制ではない。
- 凍結 2 に入れる受理物は exact のみ: 曲線方程式と Belyi map・divisor 恒等式・種数/分岐型・monodromy 群と exact conjugator・Aut(C/P¹) = 1・P₀/P_∞ と uniformizer。**数値近似や database label は discovery 用であり証拠でない**。

## 較正三層(発射前必須)

1. **K5 finite fixture**: 二類・passport・normalizer・regularity・K5-1・ρ₀(𝔉₀) = τ(μ₁₀[5])— 代表・置換三つ組・ρ_i・j_i・a = 1・証拠 ID・digest を付録 A に一表固定。
2. **K3 regression fixture**: 既知データ一体(モデル・branch・exact conjugator・cusp/uniformizer・その正規化での u = −4・ord = 3・τ/ρ₀/j の向き)を付録 A に実体化し、pipeline が**モデルから raw 再計算**で既知 class を再現。u = −4 は二者一致(厳密 blind independence は主張しない)— **回帰専用・「独立二経路の新証拠」へ札を上げない**。u′ = −256/729 は covariance control。
3. **covariance controls**: X ↦ X⁻¹(class 反転・位数/体不変)・s ↦ cs(u ↦ uc⁻¹⁰・class 不変)・τ ↦ τ∘[d]+Kummer character 逆冪(同時変換で **operative (5$'_b$) の control**として不変であることを検査する — 便 55 F4.2。**exact branch を扱う場合は `/exact/v1` と route evidence [`exact_recovery_path`] を名指しする**。b_i と同じ型で実装し **formal a を書き換えない**)。

## 工程と発射条件

- **現在許可されている工程(便 31)**: S5 の紙上設計と凍結 1(Rule 1)文書の起草まで。**個別モデル探索は修正版凍結 1 の受理後・u 抽出は両翼共同凍結 2+発射錠後に限る**。
- 発射条件: ①付録 A 実体化+較正三層 PASS ②falsifier 計画監査(v1.1 で PASS・v1.2 差分は Sol 差分検収に含める)③Sol ゲート(差分検収)④FIRE_k5bridge.auth(digest 束縛・一回性)。
- **(v1.5・operative)** S5 探索の許容範囲: **既設二枝((W)/(N_aff))のみの positive-only 探索は非網羅**であり、委嘱文に「(N_∞) 枝は未探索・全体結論は BRIDGE-UNKNOWN 維持」を明記する。(N_∞) 探索器が S5 設計 §3.3.6 で「未設計」の間、当該枝について「候補なし」と報告してはならない。**μ/Pell ansatz を用いる探索は、strict I-b∞ を守る sealed automation schema の事前登録なしに人間可視で走らせてはならない**。実 K5 の Freeze 2 では両 driver が**同一 atomic frozen bundle の canonical model JSON を係数ごと読む**(digest のみ読取り+係数別転記の運用は禁止 — 便 38 F1.3)。
- 算術全射性の宣言は、campaign の operative theorem bundle **(4d)(5$'_b$)**+exact Kummer 証明書の閉鎖まで禁止する(便 55 F4.2)。**exact を要求する場合に限り**、`/exact/v1` の閉鎖と `exact_recovery_path`(route evidence)の名指しを追加要件とする。

## 即時 integrity stop(期限を待たない・v1.2)

凍結 1 前の個別候補接触/凍結 2 前の u または同値 leading class の漏洩(**同値物は I-b・I-b∞ と逐語同一: c および ĉ_μ の値・平方類・平方因子・符号・(c,μ) 分離報告** — v1.4)/hash・serialization・発射錠対象の不一致/両翼共同凍結前の片翼 u 開示/モデル検査二系統の不一致/u 二経路の不一致/b_i が一意に決まらない・受理規約 b_sq = b_ns の破れ/K3 regression・covariance control の失敗/exact Kummer 証明書なしの PASS/FAIL 宣言。**漏洩 run は後から同じ規則を hash して救済しない** — 汚染 artifact を隔離し、規則を変えるなら新 version の campaign とする。

## 撤退条件(先に書く)

明示 genus-2 モデル(二 dessin とも)が **暦日 2026-08-10 まで、または S5 実装委嘱 8 回のいずれか早い方**(委嘱 = 委嘱 ID を付した 1 発注・失敗/timeout/再走も 1 回に数える・片翼のみ取得も「両翼未閉鎖」として期限発火)で得られない場合、BRIDGE-UNKNOWN のまま**保留**し、資源を奇数族の別窓・Lean・論文線へ移す。

---

## 出所対応表(v1.6・便 56 差分ゲート用・裁定 68 で機械可読 5 欄へ修理)

**欄の定義(便 55 F5・便 56 P56-1)**: `transfer_mode` ∈ {`verbatim`(転記元の逐語・版ラベルと節番号の付替えのみ), `normative-only`(規範内容は保存するが版履歴注記・自己訂正説明を省略), `adapted`(転記元から意味的に変更した)}。`verbatim(…を除く)` のような複合値は**禁止** — 例外を持つ転記は行を分割する。`source_range`(転記元の文書・節)/ `target_range`(本文書の節)/ `approval_id`(`adapted` のとき REQUIRED)/ `change_summary`(`adapted` のとき REQUIRED)。

| transfer_mode | source_range | target_range | approval_id | change_summary |
|---|---|---|---|---|
| normative-only | 裁定 66 Part A(`sol/裁定_66_ben54.md`) | 冒頭版履歴(v1.6 ボックス) | — | — |
| verbatim | `docs/amendment_5prime_draft.md`(条文案 v8)§3「改定案(v1.6)」 | 五札封印表 BRIDGE-FAIL 行(①②の差し替え) | — | — |
| normative-only | 同 §3「antecedent bundle」全体(v3・A10 の二分割 / v4・A12 の 2 ID 分割 / v5・A15 の closed enumeration / v6・A16 の R-a/R-b 名指し) | antecedent bundle 節((B-I)(B-II)・(AB-1)–(AB-4)・closed enumeration) | — | v3/A10・v4/A12・v5/A15 の自己訂正の版履歴詳細は要約・省略(便 56 F6.2) |
| verbatim | 同 §3「付随:manifest v1.6 の注記」 | 付随:manifest v1.6 の注記 | — | — |
| adapted | 同 §4「結果 record schema」(A7・A8・A13・A15・A20 の該当欄) | 結果規則表と結果記録の分離への digest 束縛欄追加(Rule 1 F4 の欄追記を含む) | 裁定 67 | 二段コミット欄の列挙に `z20_link_seal_id`・`root_equality_edge_id`・`equality_certificate_digest` の 3 欄を追加(便 55 F3.2 末尾・便 56 F3.2 の named edge 束縛に基づく) |
| adapted | 便 55 F4.2(Rule 1 §8.4.2 と同文)+ 旧 manifest v1.5 本節 | exact 判定の証明書型(旧 (5′) 量化子行) | 裁定 67 | operative `(5'_b)` の C-i/C-ii 限定列挙へ置換・field/kernel-only PASS を明示拒否・exact branch を `/exact/v1` として分離(便 55 F4.2 blocker 2 の修理) |
| adapted | 便 55 F4.2 | 結果規則表 pairwise 行(旧 121 行相当) | 裁定 67 | 「少なくとも一方の (5′) が偽」→「少なくとも一方の `(5'_b)` が偽」 |
| adapted | 便 55 F4.2 | 較正三層 covariance controls の型注記(旧 153 行相当) | 裁定 67 | 「(5′) 不変」→「operative `(5'_b)` の control」+ exact branch 名指しの追記 |
| adapted | 便 55 F4.2 | 工程と発射条件の算術全射性禁止条件(旧 160 行相当) | 裁定 67 | campaign の operative theorem bundle `(4d)(5'_b)` へ同期・exact 要求時のみ `/exact/v1` + route evidence を追加要件化 |
| adapted | 便 55 F6.2 | 結果 schema の authority 優先順位(4 段・新設) | 裁定 67 | Sol の推奨文言をほぼ逐語で新設(便 55 に既存条文がないため adapted 扱い・出典は F6.2 全文) |

**確認**: `transfer_mode` の分類は上表が悉皆である(便 56 F6)。上表以外に本文書が独自の判断を要する言い換えを追加することはない。digest 束縛欄は条文案 v8 §4 の該当 6 欄(`manifest_sha256`/`rule1_sha256`/`bridge_predicate_id`/`results_schema_version`/`antecedent_bundle_id`/`exact_recovery_path`)を manifest 側の固定点として転記し、二段コミット欄・証明書三分離欄は同 §4 を参照するのみ(定義の重複記載はしない)。
