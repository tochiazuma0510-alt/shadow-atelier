# `mb/ninfty-verifier-contract/v14` — divisor equality certificate の検査契約

2026-08-01 起草: Claude(実装係・司令塔指示 便95 修理バンドル item 1)。**W95-2.3 の要求(versioned freeze)を履行。前版を supersede。**

> **[historical]** **【版履歴】本版 = 前版への追加(erratum ではなく新規 integrity code の versioned freeze)。** 起点は **Sol 便95 W95-2.3** — governing spec v19 §0.0.-6 (P) と同一の変更を本稿へ反映する。**変更は 1 点のみ** — **(Q) `[27] divisor-orientation-attestation-mismatch` を §5.1 の semantic axis S2 集合・§5.2 の routing 表・§0 header の governing spec pin へ反映**。**検査手続き・二軸 routing の構造(合成規則)・registry 規則・[9]–[26] の既存段は前版と逐語同一。**

> **[historical]** **【版履歴】v13 = v12 の修理。** 起点は **内部前哨ゲート(falsifier)の第 2 巡** — **cross-document 同期類型の重大 2 件**。変更は **3 点** — **(Z1) §7 の clause-ID 全同期**(前版は `I-0c′`・`D-4`・`D-R2″`・`SB-1〜SB-3` という**修理前の ID** を参照していた = **実装者が本稿だけを読むと壊れた binding 概念で実装する経路**が残っていた)・**(Z2) §10 の label—digest 不整合の修理**(dependency manifest を旧版とラベルしながら新版の digest を貼っていた)・**(Z3) manifest pin・governing spec ID の更新**。**検査手続き・二軸 routing・registry 規則は前版と逐語同一。**

> **[historical]** **【版履歴】v6 = v5 の修理。** 起点は **Sol 便ではなく内部前哨ゲート(falsifier)**。変更は **3 点** — **(T1) FINDING-3 の修理**: `covered_procedure_checks` にも registry と集合等式を与える(CR-5)・**(T2) FINDING-2 の pin**: governing spec の certificate schema から未定義欄 `verifier_evidence` が除かれ、独立性証跡が SEALED_INTERNAL 並列であることを検査手続きに反映・**(T3) manifest v6 pin・FINDING-4 の配置修理**。**数学的内容・検査手続き・二軸 routing は v5 と逐語同一。**
**この文書は governing spec §4.4 の `verifier_contract_id` が指す実体である**(版束縛は §0 header の 1 箇所・§10 の `live_authority_refs[]`)。

> **[historical]** **【版履歴】v4 = v3 の同期版。** 変更は **3 点** — **(S1) manifest pin を v4 へ**(hash 順序 manifest → contract → spec により、manifest が変われば contract も新版が要る)・**(S2) governing spec を v9 へ**(ID 束縛・digest は receipt)・**(S3) §5.3 の cross-reference 誤り(案 A → 案 B)の修正**。**数学的内容・検査手続き・二軸 routing は v3 と逐語同一。**

### 0.1.-1 v14 DRAFT 内修理【Sol 便 96・freeze 差戻し】{#v14-draft-repair}

> **本版は Sol 便96 §2 で freeze 差戻しとなり一度も凍結されていない DRAFT。** よって以下は versioned supersede ではなく**同版内修正**である(**前版までの凍結版は byte 不変のまま**)。

| ID | 差戻し理由(便96) | v14 修理後 | 出所 |
|---|---|---|---|
| **R96-1(W96-2.1)** | **S2 排他性の自己矛盾** — §5.1 X-1(S2 軸内排他)が governing spec §5.3.2 の検証例([24]+[27] 同時)と両立しない。**自認** | **X-1 を「帯間排他・S2 帯内累積」へ**。**X-1a 新設**(両 lane の early-return 禁止・primary は priority 最小の機械計算)。**X-5 の文言を帯間停止の意味へ明確化。** pseudocode 同期 | 便96 W96-2.1 |
| **R96-2(W96-2.2)** | **payload-era 混在** — P-3.1/P-3.2 が「governing v19 と一致」と読める一方 payload は v18 を宣言 | **§3.3.1 新設**: P-3.1/P-3.2 を governing spec §5.3.4 の `PAYLOAD_ERA_MATRIX` 経由で読む。**certificate/native の era は `ERA_FROZEN`** が正解であることを normative 化 | 便96 W96-2.2 |
| **R96-3(W96-2.3)** | **W-6 未閉鎖** | **§3.2.1 新設**: W-6 は option (a)・R3-NF は代替不能・`UNKNOWN W6-KEY` 登録(governing spec §5.3.5 と同期) | 便96 W96-2.3・P96-2.1 |

---

## 0. lifecycle state {#lifecycle}

```text
embedded_state_at_candidate_creation = {
  contract_freeze_id: NOT ISSUED,
  verifier_implementation: NOT AUTHORIZED
}
live_status_authority = Sol freeze reply + commander receipt
live_freeze_and_authorization_authority = approved freeze receipt
```
**上記 blob は candidate 作成時点で埋め込まれた状態であって live status ではない。live status の正本は approved freeze receipt 側にあり、receipt 発行によって本稿を書き換える必要はない(digest 不変)。**

```text
contract_id     = "mb/ninfty-verifier-contract/v14"
contract_digest = <64 hex: 本稿 exact blob の sha256 — receipt が記入>
encoding        = UTF-8, LF, no BOM, no normalization
governing_spec  = "mb/ninfty-stage2-predicate/v19"
governing_spec_digest = <64 hex: governing spec の digest — receipt が記入>
dependency_manifest_schema_id     = "mb/dependency-manifest/v14"
dependency_manifest_schema_digest = e892be68e79244c8493e37ec77eb3a1cbdb29ee45a911f73040aadaebbb889af
supersedes        = "mb/ninfty-verifier-contract/v13"
supersedes_digest = e41d51dbdbdcf66efaff2ccd073bbfba9bff12bbfff435ca290a4248abcf5022   # 便95 W95-2.3 起点(pin 同期)
supersedes_prev2  = 1eda4fb28e367d03b0655888df301e0064d033dbd274cc9651ab7dfe49692d89
supersedes_v4     = 703fb47f60e721b2f0f6a79197f4047f723f030367fca9641a841aca6728bd75
supersedes_v3     = bd4d5064e04ef292d7f21fa3cf5b8089c20ef34c322461920dc95c9775e4d484
supersedes_v2     = 1fd36b3eda0da33b2aba5d3d371a24749850b9b05a3f4c4f17ef1725ffe555bd
```

> **【hash 順序・便 66 F11】** 非循環な順序は **manifest → contract → spec → receipt**。**本稿は §0 header の `dependency_manifest_schema_id` / `dependency_manifest_schema_digest` を exact pin し、governing spec の digest は receipt 側で束縛する。**(governing spec は **ID で束縛し digest は receipt 側**)。**governing spec が本稿の exact digest を pin する。**
> **【fail-closed】header の governing spec は本稿起草時点で未発行の後継である。receipt がその実在と digest を束縛するまで、本稿を operative として扱ってはならない。**

**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

### 0.1 優先関係 {#precedence}

**本稿と governing spec が矛盾した場合、governing spec が優先する。** 本稿は spec §4.1–§4.4 の**手続き的具体化**であって、新しい数学的前件を導入しない。
**§8 は erratum 案の記録を持つが、これは要請であって本稿の優先を主張するものではない** — **§0 header の governing spec が発行され receipt がその digest を束縛するまで、本稿を operative にしない**(上の fail-closed 条項)。

> **[historical]** **【自認・v6 で移設】** v5 はこの位置(operative 本文)に「v2 が置いていた 1 点優先の例外は spec v7 erratum E1 で解消済み」という歴史記述を置いていた。**operative 行に歴史 token を置くことは LA-2 の配置規約違反**であり、**「記録」の語を含むだけで sweep の除外域と見なされる**穴でもあった(内部ゲート FINDING-4)。**本 blockquote へ移設した。**

---

## 0.17 前版差分【Sol 便 95・W95-2.3】

> **起点の明示**: governing spec v19 §0.0.-6 (P) と同一の起点(Sol 便95 W95-2.3)。**凍結 enum に無い `[27]` を live 実装(`search/ninfty-searcher-v2.mjs`・`search/ninfty-checker.py`)へ足したまま事後追認していなかった**ことへの応答。

| ID | v13 | v14 | 出所 |
|---|---|---|---|
| **Q** | §5.1 の semantic axis S2 が `[13]..[24]` の連続区間表記のみで `[27]` を含まず、§5.2 の routing 表にも `[27]` の行が無かった。**governing spec の integrity enum は `[9]`–`[26]` の 18 段で閉じており、本稿もそれに同期していた** | **§5.1 の S2 を明示集合 `{13,14,...,24,27}` へ拡張**(governing spec v19 §5.3.3 と逐語同期)。**§5.2 の routing 表へ `[27]` の行を追加**(事象・reason code・軸)。**§0 header を governing spec v19 / 本稿 v14 の pin へ更新**。**public routing(§5.4 P-S3)は無改定** — `[27]` は semantic 軸なので public secondary の対象外(concordance 軸 `[26]` のみが対象という既存規約のまま) | 便95 W95-2.3・governing spec v19 §0.0.-6 (P) |
| **(付随)** | §0 header の `dependency_manifest_schema_id/digest` が manifest v13 を pin | **manifest v14 へ**(**check #1 の版トークン sweep が検出**: manifest v13 自身の §0 header も `governing_spec = v18` を ID 束縛しており、spec の v19 化に伴い manifest も純同期版 v14 を要した — 内容無改定・§0 header の 1 欄のみの変更。hash 順序 manifest → contract → spec の連鎖により本稿もその新 digest を再 pin) | bundle-selfaudit-v9 check #1(機械検出) |

> **検査手続き(§3)・二軸合成規則そのもの(§5.1 の if/elif ロジック)・registry 規則・§7 独立要件・§9 conformance schema・[9]–[26] の既存段は v13 と逐語同一。** **再監査範囲は (Q) と pin に限る。**

---

## 0.16 前版差分【裁定 85・内部前哨ゲート第 2 巡起点】

> **教材(採録)**: 「**修理の自己完結 ≠ 体系の整合**」 — 単一文書内で完結した修理でも、**参照する側の文書に旧概念が残れば体系としては矛盾仕様**。**同期は文書単位でなく clause-ID 単位で機械検査する。**

| ID | 前版 | 本版 | 出所 |
|---|---|---|---|
| **Z1(重大)** | §7 の C-1′ が **`I-0c′`(旧)**、C-6‴ が **`D-4`・`D-R2″`・`I-0c′`・`SB-1〜SB-3`** を参照。**dependency manifest 側の現行は `D-4′`・`D-R2⁗`・`I-0c″` であり、`SB-5`・`SB-6` への言及はゼロ**だった。**実装者が本稿だけを読むと、修理前の壊れた binding 概念(「top-level と相互照合」)で実装する経路が残る。自認** | **§7 全行を dependency manifest の現行 clause-ID 表と突合して書き直し**。**C-1′ → I-0c″**・**C-6‴ → D-4′・D-R2⁗・I-0c″・SB-1′〜SB-7**(SB-5・SB-6・SB-7 を含む)。**移設で [historical] 側へ落ちていた normative 文(preimage 6 欄・TCB 四欄・family allowlist)も版中立形で本文へ復帰** | 第 2 巡 重大 1 |
| **Z2(重大)** | §10 `live_authority_refs[]` が dependency manifest を**旧版とラベル**しながら**新版の digest** を貼付。**LA-1 が「live 版束縛はここのみ」と定めた block 自身の label—digest 不整合。自認** | **artifact_id を現行版へ**。**script v3 の check #13 が label—digest 対応を機械照合**する | 第 2 巡 重大 2 |
| **Z3** | manifest pin・governing spec ID が前版 | **現行版へ** | 裁定 85 |

---

## 0.15 前版差分【裁定 84・内部前哨ゲート起点】(【chg v6 から継承・変更なし】)

> **起点の明示**: 本版の差戻しは **Sol の監査便ではなく、便 69 発送前の内部前哨ゲート(falsifier)**による。**self-audit 9/9 ALL PASS の外側**で見つかった。

| ID | v5 | v6 | 出所 |
|---|---|---|---|
| **T1(FINDING-3)** | CR-1/2 の registry 再生成と集合等式は **clause 側のみ**。check 側(`D-*`・`U-*`・`P-*`・`W-*`・`S*`)には**母集合を機械確定する規則が無く**、**check を黙って落としても CR-2/3/4 のどれも検出しない** — 「procedure check への分離」が**義務の格下げ**になっていた。**自認** | **CR-5 新設**: check ラベルを正規表現で本文から再生成した `procedure_check_registry` を定義し、**`covered_procedure_checks ∪ uncovered_checks = check_registry` かつ `∩ = ∅`** を受領側が exact set equality で照合。**clause と同格の完全性保証へ引き上げる** | 内部ゲート FINDING-3 |
| **T2(FINDING-2)** | governing spec §4.1 の certificate schema 末尾に **どこにも定義されない欄 `verifier_evidence`** があった(§4.4 が定義するのは `independence_evidence`・§5.2 では certificate と**並列の別オブジェクト**)。**contract v5 に `verifier_evidence` は一度も現れず、検査契約がこの欄を検査しない**状態だった | **spec 側で当該欄を削除**し「独立性証跡は SEALED_INTERNAL 並列」と注記(spec v11)。**本稿 §2 に、certificate は独立性証跡を内包せず §7 の独立要件が別オブジェクトを検査する旨を明記** | 内部ゲート FINDING-2 |
| **T3** | manifest pin = v5・:42 の歴史文が operative 本文位置にあった | **manifest v6 pin**・**歴史文を自認 blockquote へ移設**(LA-2 の配置規約適合) | 内部ゲート FINDING-4・裁定 84 |

---

## 0.2 前版差分【裁定 83】(【chg v5 から継承・変更なし】)

| ID | v4 | v5 | 出所 |
|---|---|---|---|
| **V1(F6.2)** | header と P-3.1 は governing spec を **v9** に束縛する一方、**live 本文が「governing spec(v8)」を指していた**(:79 入力型・:240 reason code owner・:249 state-machine owner)。**nominal typing では、v9 の certificate は P-3.1 を満たすが §2 の文言に合わず、v8 の certificate はその逆になる。** §0.1 の lifecycle 文も v9 receipt を要求する header と非同期だった。**「旧版起点の live 残存 sweep = 0」という前便の申告は反証された・自認** | **live 参照をすべて版中立化**(「governing spec §4.1」「governing spec §5.3.2」等 — **版 token を持たない節参照**)。**版束縛は header の 1 箇所に集約**(ID + receipt digest)。§0.1 lifecycle も header 参照へ同期 | 便 68 F6.2 |
| **V2(F7)** | §7 の実際の義務 ID は `C-1', C-2, C-3', C-4', C-5', C-6", C-7, C-8'` なのに、§9 の machine-facing `conformance_record` は **v3 のまま** (— `build_definition_blob_digest` と `pinned_input_digests[]` が欠落・comment は manifest v3・clause list は `C-1..C-5, C-6', C-7, C-8` で prime を落とす)。**旧 record を提出した実装が `uncovered_clauses=[]` と自己申告しつつ C-6" の build 義務を machine record 上まったく提出しない反例がある。****§9 は「契約適合」を宣言する schema そのものであり、compliance boundary を v3 へ巻き戻していた。自認** | **§9 を v5 へ同期**: preimage **6 欄**(source_artifact_digests[]・toolchain_digest・build_step_digests[]・**build_definition_blob_digest**・**pinned_input_digests[]**・**subject_build_binding_digest**)+ **TCB 四欄**。**§9.1 に `normative_clause_registry` を新設**し(F13.3)、受領側が **exact set equality** で照合。**range 表記を禁止** | 便 68 F7・F13.3 |
| **V3** | manifest pin = v4 | **manifest v5**(`8623c83f…`)へ。§7 の条項も manifest v5 の新条項(SB / BA / FA)へ同期 | 裁定 83 |
| **V4(F13.1)** | live 参照の版 token が本文に散在 | **§10 に `live_authority_refs[]` / `historical_quotation_refs[]` の機械可読 block を新設** | 便 68 F13.1 |

> **[historical]** **v5 でも不変**: **§1 役割・§2 検査対象・§3 検査手続き(W-2 / W-2′ の型分け・§3.4 result vector)・§4 合否・§5.1 二軸 routing(X-1〜X-6)・§5.4 secondary(P-S1〜P-S6)・§6 入力型分離。**

---

## 0.2.1 前版差分【裁定 81】(【chg v4 から継承・変更なし】)

| ID | v3 | v4 | 出所 |
|---|---|---|---|
| **S1** | `dependency_manifest_schema_id/digest` が **v3**(`1a8d1f21…`)を pin | **manifest v4**(`378f30c8…`)へ。**hash 順序 manifest → contract → spec により、manifest が新版になれば contract も新版が必要**(v3 のまま spec v9 が manifest v4 を pin すると、contract と spec が別の manifest を指す — 便 66 F7 と同型の型不一致) | 便 67 F11-2 |
| **S2** | governing spec = v8 | **v9 へ**(ID 束縛・digest は receipt) | 裁定 81 |
| **S3** | §5.3 の表が public secondary の spec 側条文を **「§8 の erratum 案 A」** と参照していた。**正しくは案 B**(案 A は二軸 routing、案 B が public secondary)。**自認** | **案 B へ修正** | 便 67 F11-2 |

> **[historical]** **v4 でも不変**: **§1 役割・§2 検査対象・§3 検査手続き(W-2 / W-2′ の型分け・§3.4 result vector)・§4 合否・§5.1 二軸 routing(X-1〜X-6)・§5.4 secondary(P-S1〜P-S6)・§6 入力型分離・§7 独立要件。**

---

## 0.2.1 前版差分(【chg v3 から継承・変更なし】)

| ID | v2 | v3 | 出所 |
|---|---|---|---|
| **B66-1(F4)** | §5.1 の評価順序が「前段が reason を発したら停止」で**後段を抑圧**した。**同じ原因の二重分類を防ぐ意図が、別原因として同時に起きた verifier disagreement まで消していた。** ① native partition mismatch [24] と **A/B の witness vector 不一致**が同時でも step 2 停止で [26] が public から落ちる(**二実装監査が検出すべき common/individual bug の証跡**が消える) ② A: W-2 FAIL/W-3 PASS・B: W-2 PASS/W-3 FAIL は**両者 overall FAIL だが result vector は不一致**なのに、現 step 3 が [25] を発して step 4 へ行かない(**enum 名 `verifier-result-mismatch` と一致しない**)。**自認** | **§5.1 を二軸へ**(便 66 F13 の発案を採用): **semantic axis**(envelope / native mathematics / witness validity — **軸内は排他**)と **concordance axis**($R_A$ vs $R_B$ — **入力 digest が一致する限り常に評価**)。**[26] は semantic reason と共存する。** 判定は **`if R_A ≠ R_B: add [26] / elif native reasons 空 かつ $R_A=R_B$ が failure を含む: add [25]`**。**primary の単数性は維持**し、**public に `secondary_reason_codes[]` を新設**(§5.4) | 便 66 F4・F13 |
| **B66-2(F7)** | machine field は v7 へ直ったが、**live 文が v6 のまま**: 冒頭「v6 §4.4 の実体」・§2「spec v6 §4.1 の certificate」・§5.2「spec v6 §5.3 が決める」。**P-3.1 の governing-spec equality と衝突する exact bundle の型不一致。**(§8 の v6 記述は historical quotation なので可) | **live 三箇所を後継 spec(v8)へ同期。** §8 の歴史記述は `[historical quotation]` として保持。**自認** | 便 66 F7 |

---

## 1. 役割と非役割 {#role}

[normative-check-table]
| # | 条項 |
|---|---|
| **V-0** | verifier は **`divisor_equality_certificate` を検査する装置**であり、**判定 lane ではない**。candidate に対する `ACCEPT` を**単独で出せない**。出力は §3.4 の **canonical per-witness result vector** と overall `PASS`/`FAIL`、およびその digest。 |
| **V-1** | verifier は **searcher / checker の native 出力を再生産しない**。両 native は入力として受け取り、**certificate の witness が両者を実際に同一視しているか**だけを検査する。 |
| **V-2** | **generator は verifier ではない**(spec §4.3 G-1)。generator が作った witness を、**A と B が独立に再検査**する(G-3)。 |
| **V-3** | verifier は **`SEALED_INTERNAL` の値を public envelope へ写さない**。検査に用いた量は digest でのみ参照する。 |

---

## 2. 検査対象 {#scope}

入力は **governing spec §4.1**(版束縛は §0 header)の `divisor_equality_certificate` 全体と、それが参照する両 native artifact。**これらはすべて `declared_untrusted_inputs[]`(§6)に属する** — **共有されるが信用されない**。

```text
W-1   component_bijection
W-2   exact_point_equality_witnesses            # kind = ideal-equality のみ(§3.1)
W-2′  distinctness_witnesses                    # kind = disjointness(§3.1.2)
W-3   multiplicity_equalities
W-4   chart_overlap_witnesses
W-5   total_coverage_and_no_extra_component_witness
W-6   pushforward_compatibility_witness
```
両 native は各々 **2 対象**(`ramification_divisor_on_C_ref`・`branch_divisor_on_P1_ref`)を持つ。**W-1〜W-6 は 2 対象それぞれについて検査する**(片方だけの PASS を全体の PASS としない)。

> **[historical]** **【chg v6・FINDING-2】certificate は独立性証跡を内包しない。** governing spec §4.4 が定義する `independence_evidence` は、**`SEALED_INTERNAL` において certificate と並列に置かれる別オブジェクト**である(governing spec §5.2)。**本稿 §7 の独立要件はその別オブジェクトを検査対象とする** — certificate schema の欄としては検査しない。**v5 が pin していた governing spec は certificate schema 末尾に未定義欄 `verifier_evidence` を持ち、本稿はそれを一度も検査していなかった**(内部ゲート FINDING-2・**自認**)。

---

## 3. 検査手続き {#procedure}

### 3.0 前段: ambient の固定を再検査

```text
[normative-check-block]
P-0.1  ambient_coordinate_ring_schema_id + digest が存在し、digest が実体と一致
P-0.2  ambient_quotient_relations が明示されている
P-0.3  coefficient_field_presentation_id + digest が存在し一致
P-0.4  monomial_order_id + digest が存在し一致
P-0.5  groebner_reduction_contract_id + digest が存在し一致
P-0.6  異 presentation を跨ぐ witness には field_embedding_witness が添付されている
P-0.7  curve_model_digest と chart_ids が存在し、両 native が同じ curve model / chart を
       参照していること(certificate が宣言する曲線モデルを、どの verifier も検査しない状態を作らない)
P-0.8  field_embedding_witness_schema_id + digest が存在し一致(P-0.6 の witness の型を固定する)
```
**理由**: reduced Gröbner basis は ring と term order を固定して初めて一意になる。固定が再検査できない状態で W-2 を「再計算した」と称してはならない。

### 3.1 W-2 の再検査 — **`kind = ideal-equality` に限定**

> **[historical]** **⚠ v1 の数学的誤り(自認・記録)**: v1 は $1=\sum u_ig_i$ の展開で W-2 を PASS にしていた。**$1\in I_0+I_1$ は $V(I_0)\cap V(I_1)=\varnothing$ の certificate であって「等しい」ことの certificate ではない。**
> **最小反例(独立に検算)**: $R=\mathbb Q[x]$, $I_0=(x)$, $I_1=(x-1)$。$1=1\cdot x+(-1)\cdot(x-1)$ ゆえ v1 の Bézout 分岐は PASS を出す。正しい membership 判定は $x \bmod (x-1)=1\ne0$、$(x-1)\bmod (x)=-1\ne0$ で**両方向とも不成立**。

```text
[normative-check-block]
kind = ideal-equality
  I_0 ⊆ I_1  かつ  I_1 ⊆ I_0  を、各生成元の membership certificate で示す
```

| 形式 | 再計算内容 | PASS 条件 |
|---|---|---|
| **membership by representation** | 各生成元 $g\in G_0$ について表現係数 $\{u_i\}$ から $\sum u_i h_i$($h_i\in G_1$)を `groebner_reduction_contract_id` の規約で計算し、$g$ と**係数まで**一致するかを見る。逆向きも同様。 | **両方向の全生成元**について一致 |
| **membership by `reduction-to-zero`** | 各生成元を、固定 monomial order における相手 ideal の reduced Gröbner basis で**正規形へ簡約**する(reduction 列を一段ずつ再実行)。 | **両方向の全生成元**について**正規形が $0$** |

```text
[normative-check-block]
P-1.1  表現係数 / reduction 列がすべての生成元について存在する
P-1.2  再計算が固定 monomial order・固定 reduction 規約の下で行われた
P-1.3  再計算結果が certificate の主張と一致する
P-1.4  異体 presentation を跨ぐ場合、field_embedding_witness の像が一致する
P-1.5  witness の kind tag が明示されている。tag 無しの reduction certificate は FAIL
```

> **⛔ W-2 の PASS 根拠にならないもの**: **Bézout $1=\sum u_ig_i$**・tag の無い `reduction certificate`・単なる digest 一致・最終 partition の一致・degree の一致・generator の内部 canonicalizer の宣言。

### 3.1.2 W-2′ `distinctness_witnesses` — `kind = disjointness` {#distinctness}

```text
kind = disjointness
  1 ∈ I_P + I_Q  の Bézout certificate(表現係数 {u_i} を明示)
```

| 用途(この 2 つに限る) | 内容 |
|---|---|
| **W-1 の単射性** | component bijection が**相異なる component を相異なる component へ送る**ことの証明。 |
| **W-5 の余剰排除** | ある component が既にマッチした全 component と別物であることの証明。 |

> **数学的注記(型の限定)**: 一般には **disjointness $\Rightarrow$ distinctness** で逆は偽。**本設定では component は $C_{\rm crv}$ 上・$\mathbb P^1$ 上の閉点で support は 0 次元 reduced** なので、**相異なる閉点は交わらず、この設定に限り同値**。**多重度は W-3 が扱う** — W-2′ の ideal は**点の radical**であり非被約構造を持ち込まない。
> **⛔ W-2′ を W-2 の代用にしてはならない。**

### 3.2 W-1・W-3〜W-6

| # | 再計算内容 | PASS 条件 |
|---|---|---|
| **W-1** | 全単射を **W-2 の点同一性から独立に構成し直す**。単射性は **W-2′** で裏づける | certificate の `component_bijection` と一致し、両側とも全域・単射 |
| **W-3** | 対応する component 対の multiplicity を**整数として比較** | 全対で一致 |
| **W-4** | chart 重なり上で両 chart が同じ component を与えるか再計算 | 全重なりで一致 |
| **W-5** | component 総数と W-1 の像の大きさを比較。余剰候補には **W-2′** を要求 | 被覆に漏れがなく、**両側**に余剰 component が無い |
| **W-6** | `ramification_divisor_on_C` の pushforward と `branch_divisor_on_P1` の整合を multiplicity の和として再計算 | 全 branch point で一致 |

#### 3.2.1 W-6 の閉じ方【chg v14 修理 R96-3・便96 W96-2.3 / P96-2.1】{#w6-closure}

```text
[normative-check-block]
W6-C1  W-6 は incidence(どの ramification component がどの branch component
       へ写るか)を本質的に使う。
W6-C2  R3-NF PASS は W-6 を含意しない。NF は incidence/pushforward map を
       持たない(便96 W96-2.3 の★最小反例)。R3-NF を W-6 closure と
       数えてはならない。
W6-C3  採用は option (a): lane A producer が自身の ideal/locus data から
       導いた registry-pinned canonical pushforward map を現 W-6 shape で
       出す。option (b)/(c) は不採用。
W6-C4  aggregate は producer の自己申告を信じず、受領側が per-component
       record(canonical ID / image branch key / multiplicity /
       導出元 ideal・locus pointer)から再集計する。
W6-C5  inline-only ref は LEGACY_UNVERIFIED_REF のまま。
W6-C6  異なる incidence で同じ NF を作る負例を必須とする。
W6-C7  修理後も R1/R2 と R3-NF は別列・別 route。
```

> **`UNKNOWN W6-KEY`**: 実装の閉塞点は **両 lane 共通の canonical branch key 符号化が存在しないこと**(lane A = $x$ 上の ideal generator / lane B = sympy `srepr` 文字列)。frozen `verify_W6_single` は両 map を**文字列辞書として `==` 比較**するため、素朴な option (a) 実装は lane A に sympy `srepr` の模倣を強い、**二 lane 独立性を破壊する**。共通符号化の新設は normative schema の新設であり**司令塔検問 + Sol ゲート事項**。詳細は governing spec §5.3.5。

### 3.3 入出力の束縛

```text
[normative-check-block]
P-3.1  certificate の predicate_spec_id / predicate_spec_digest が governing spec と一致
P-3.2  certificate の schema_id / schema_digest が governing spec §4.1 の anchor と一致
P-3.3  両 native の native_artifact_digest が、verifier が実際に読んだ blob の digest と一致
```
**P-3.3 の不一致は「検査対象が入れ替わっている」ことを意味するので即停止。**

#### 3.3.1 P-3.1/P-3.2 の era 解釈【chg v14 修理 R96-2・便96 W96-2.2】{#era-reading}

```text
[typed-registry]
M-1  P-3.1/P-3.2 の「governing spec と一致」は、governing spec §5.3.4 の
     PAYLOAD_ERA_MATRIX が当該 plane に割り当てた era と exact に一致、と読む。
M-2  certificate の predicate_spec_id / schema_id は plane
     "native_payload_schema" に属す。よって ERA_FROZEN
     (mb/ninfty-stage2-predicate/v18) と一致すべきであり、
     ERA_CURRENT(v19)と一致してはならない。
M-3  両 native の native_schema_id も同 plane。同じく ERA_FROZEN。
M-4  本稿(contract)と search/ninfty-verifier-b.py は plane
     "frozen_route_verifier" の実装として ERA_FROZEN を宣言する
     — この宣言は stale ではなく matrix 上の正解である。
M-5  「新しい方を許す」「どちらでもよい」は禁止。era は plane ごとに単一値。
```

> **なぜこの読みが要るか**(便96 W96-2.2): 初稿 v14 の P-3.1/P-3.2 は素朴に「governing v19 と一致」と読め、一方で現 payload は v18 を宣言していた。**両立しない条文を抱えたまま `docs_era_binding_ok` が PASS していたので、control-plane の文書 pin が payload-era binding と誤読されていた。** matrix を明示し、consumer 側の欄名も `control_plane_docs_receipt_binding` / `payload_era_matrix` の二欄へ分離する(governing spec §5.3.4 M-3/M-4)。

### 3.4 canonical per-witness result vector【B66-1】{#result-vector}

```text
[normative-check-block]
R_X = canonical_serialize( [
        ("W-1",  result), ("W-2",  result), ("W-2′", result),
        ("W-3",  result), ("W-4",  result), ("W-5",  result), ("W-6", result)
      ] )                       # X ∈ {A, B}・各 result ∈ {PASS, FAIL, ABSENT}
      × 2 対象(ramification_divisor_on_C / branch_divisor_on_P1)

result_digest_X = sha256( canonical_serialize( {
        contract_id, contract_digest, certificate_digest,
        searcher_native_artifact_digest, checker_native_artifact_digest,
        native_cross_check_results[],        # §5.1 semantic step 2
        R_X, overall_verdict_X
      } ) )
```

[normative-check-table]
| # | 条項 |
|---|---|
| **R-1** | **$R_A$ と $R_B$ は同一の canonical 形式で作られ、要素ごとに比較可能でなければならない。** overall verdict だけの比較を「result 比較」と称してはならない(**両者 FAIL でも vector は違い得る** — 便 66 F4.2)。 |
| **R-2** | **$R_X$ は `ABSENT`(witness が存在しない)と `FAIL`(存在するが不成立)を区別する。** |
| **R-3** | **$R_A\ne R_B$ の比較は、入力 digest(certificate・両 native)が A/B で一致する場合にのみ意味を持つ。** 不一致なら先に [12]。 |

---

## 4. 合否規準 {#verdict}

```text
verifier_verdict_X = PASS  iff  P-0.* ∧ P-1.* ∧ (R_X の全成分が PASS) ∧ P-3.*
                   = FAIL  otherwise
```
- **PASS は「certificate が両 native の同一性を実際に証明している」ことのみを主張する。** candidate の数学的判定は述べない。
- **A と B の verdict または vector が食い違った場合、両者を FAIL として扱う**(§5.1 concordance axis の [26])。**多数決・片側採用を禁止。**

---

## 5. `INTEGRITY_STOP` 条件と routing {#integrity}

### 5.1 二軸 routing【B66-1・便 66 F13】{#two-axis}

> **[historical]** **v2 の欠陥(自認)**: 「前段が reason を発したら停止」は**同じ原因の二重分類**を防ぐには正しかったが、**別原因として同時に起きた verifier disagreement まで消していた**。**[24] は native data の不一致、[26] は verifier 実装の不一致であり、同じ event の別名ではない。**

```text
[normative-check-block]
# --- semantic axis(【chg v14 修理 R96-1】帯間は排他・S1→S2→S3 の順に
#     評価し reason を発した「帯」で停止 / S2 帯内は累積)---
S1  envelope-level: leak / digest / dependency checks      -> [9]..[12]
S2  native cross-check: 両 native への specific な数学的検査 -> S2_CODES = {13,14,15,16,17,18,19,20,21,22,23,24,27}
      【chg v14・便95 W95-2.3】非連続集合を明示集合で書く(governing spec v19
      §5.3.3 束縛条項(a)と同期)。[27] は S2_CODES に属す。
      【chg v14 修理 R96-1・便96 W96-2.1】S2 帯内は累積: 発火した S2 述語は
      すべて semantic_reasons へ加える(最初の 1 個で停止しない)。
      S2_EQUIVALENT_CAUSE_PAIRS = {}   # 同一事象を二重分類する code 対のみ
                                       # 「同時に立ってはならない」。現行 enum
                                       # では空。S2 帯全体の排他ではない。
S3  witness validity(S2 が空のときのみ評価・X-2)            -> [25]

# --- concordance axis(独立・入力 digest が一致する限り常に評価)---
C1  R_A vs R_B                                              -> [26]

# --- 合成 ---
if R_A != R_B:
    concordance_reasons = { [26] }
elif S2 の native reason が空 かつ (R_A = R_B) が failure を含む:
    semantic_reasons ∪= { [25] }

I       = semantic_reasons ∪ concordance_reasons
verdict = INTEGRITY_STOP (I ≠ ∅ のとき)
primary = minimum(I, integrity_priority)          # 単数性は維持
```

[normative-check-table]
| # | 条項 |
|---|---|
| **X-1** | **【chg v14 修理 R96-1・便96 W96-2.1】semantic axis は帯間で排他・S2 帯内は累積。** **帯間**: S1(`[9]`–`[12]`)・S2(`S2_CODES`)・S3(`[25]`)は上から評価し、reason を発した**帯**で停止する。**帯内(S2 のみ)**: 発火した S2 述語は**すべて**蓄積する。ゆえに **`[24]` と `[27]` は同時に立ちうる**(governing spec §5.3.2 検証例と同期 — primary=[24]・[27] は sealed の `all_reason_codes[]` に残る)。**同時に立ってはならないのは `S2_EQUIVALENT_CAUSE_PAIRS` に明示列挙した同値原因対のみ**で、現行 enum ではその集合は**空**。**初稿 v14 の「S2 軸内排他」は governing spec §5.3.2 の検証例と自己矛盾していた — 自認・本修理で廃止。** |
| **X-1a** | **【chg v14 修理 R96-1】X-1 の帰結として、両 lane の実装は S2 帯で early-return してはならない。** lane A(`search/ninfty-searcher-v2.mjs`)は元より集合蓄積で整合。lane B(`search/ninfty-checker.py`)の `[27]` early-return は蓄積へ同期した。**`primary_reason_code` は蓄積後に `integrity_priority` の最小として機械計算する。** |
| **X-2** | **[25] は「native の一致が S2 で確認された下で、$R_A=R_B$ が witness failure を含む」に限定される。** |
| **X-3** | **[26] は concordance axis に属し、semantic reason と共存する。** [13]–[24] と同時に検出してよい。**「native 不一致を [26] に予約する」案は不採用**(便 65 F5)。**【chg v14】[27] とも共存する。** |
| **X-4** | **[25] と [26] は相互排他**($R_A=R_B$ が [25] の前提、$R_A\ne R_B$ が [26] の前提)。 |
| **X-5** | **S2 が reason を発した場合も witness 検証と concordance 比較は実行する。**(**【chg v14 修理 R96-1】**「S2 で停止」は帯間の停止 = S3 の `[25]` を発しないことを指す。S2 帯**内**は停止せず累積する。) |
| **X-6** | **`[26]` の述語は「overall verdict の不一致」ではなく「canonical result vector $R_A\ne R_B$」である**(R-1)。もし overall verdict の不一致に限定するなら enum 名を `verifier-verdict-mismatch` とすべきだが、**本稿は vector 比較を採る**(便 66 F4.2)。 |
> **[historical] X-5**: semantic の後段 reason は発しないが、**concordance の [26] は発する** — これが v2 との違い。


### 5.2 routing 表

| 事象 | reason code(**governing spec §5.3.2** の段・版束縛は §0 header) | 軸 |
|---|---|---|
| 入力 / native / certificate の **digest 不一致** | **`digest-mismatch` [12]** | semantic S1 |
| implementation closure の三交差が非空(§7) | **`shared-helper-detected` [11]** | semantic S1 |
| verifier が sealed 値を public 面に露出 | **`sealed-field-leak` [9]** | semantic S1 |
| **native cross-check の specific な失敗** | **[13]–[24] の該当 code** | semantic S2 |
| **E-1..E-4 前提 PASS 後、attested E-5 divisor-orientation 値が定理導出値(Prop E5-D)と矛盾**【chg v14 新設】 | **`divisor-orientation-attestation-mismatch` [27]** | semantic S2 |
| **$R_A=R_B$ が witness の欠落・不成立を含む**(native 一致確認後) | **`divisor-equality-failure` [25]** | semantic S3 |
| **$R_A\ne R_B$**(同一入力に対する canonical result vector の不一致) | **`verifier-result-mismatch` [26]** | **concordance C1** |

**上記はすべて `INTEGRITY_STOP` であり、REJECT ではない。** verdict の決定と primary の選択は **governing spec §5.3** の state machine が行う — **本稿は reason code を供給するだけで、自ら verdict を宣言しない。**

### 5.3 state machine との整合 {#state-machine-fit}

| 層 | 内容 | spec 側の根拠 |
|---|---|---|
| **primary** | `minimum(I, integrity_priority)` — **単数・全域** | spec §5.3 invariant 2・4 |
| **sealed** | `all_reason_codes[]` = canonical 整列した $I\cup R$ — **全 code を保持** | spec §5.3 invariant 3 |
| **public secondary** | **§5.4 で新設** | 
> **[historical] primary**: v6 以来の不変条件をそのまま保つ。
> **[historical] public secondary**: spec 側条文が要る → §8 の erratum 案 B**【chg v4 で修正・v3 は「案 A」と誤記(**自認**)】 |。


**二軸化そのものは spec §5.3 の state machine を変えない** — `I` の作り方が「排他的な単一 code」から「semantic ∪ concordance」へ広がるだけで、`primary = minimum(I, ...)` と `accepted iff I=R=∅` はそのまま成立する。

### 5.4 `secondary_reason_codes[]`(public)【裁定 79】{#secondary}

```text
public envelope = {
  candidate_ref, predicate_spec_id, predicate_spec_digest,
  searcher_id+digest, checker_id+digest,
  verdict,
  primary_reason_code,              # 単数・従来どおり
  secondary_reason_codes[],         # canonical 整列【chg v3 新設】
  <数学的射影 5 欄>
}
```

[normative-check-table]
| # | 条項 |
|---|---|
| **P-S1** | **`primary_reason_code` の単数性は維持する。** `secondary_reason_codes[]` は primary を**含まない**。 |
| **P-S2** | **`secondary_reason_codes[]` は canonical 昇順に整列**する(producer の順序に依存しない)。 |
| **P-S3** | **【漏洩最小化】public の secondary は concordance axis の code に限る**(現行 enum では **[26] のみ**)。**semantic axis の非 primary code は sealed の `all_reason_codes[]` にのみ置く。** |
| **P-S4** | **P-S3 の理由**: public envelope の情報量が増えるほど、**小さい探索宇宙では reason の組合せが指紋になり得る**(便 59 F11.3 の deterministic digest と同型のリスク)。**F4.1 が要求するのは「verifier disagreement が public から消えないこと」**であり、それは **1 ビット**([26] の有無)で満たせる。**semantic の全 code を public へ出す必要はない。** |
| **P-S5** | ゆえに **[24] と [26] の同時成立**では `primary = [24]`(priority 最小)・`secondary = [[26]]` となり、**両方が public に可視**である(F4.1 の要求を満たす)。 |
| **P-S6** | `secondary_reason_codes[]` が空のときは**空配列を明示**する(欄の欠落と区別する)。 |

---

## 6. 入力の型分離 {#input-separation}

```text
declared_untrusted_inputs[] = {
  divisor_equality_certificate, searcher_native_artifact, checker_native_artifact,
  governing_spec_blob, contract_blob
}
```

[normative-check-table]
| # | 条項 |
|---|---|
| **Y-1** | **TCB として差し引くのではなく交差検査の対象外。** |
| **Y-2** | **入力の共有は独立性を毀損しない。毀損するのは実装の共有である。** |
| **Y-3** | untrusted input については **A と B で digest 一致を要求する**(P-3.1〜P-3.3)。不一致は [12]。**これは R-3 の前提でもある。** |
| **Y-4** | **入力クラスへの math-helper 混入を禁止**。**規約を選ぶパラメータ値の共有は許され、禁止されるのはその規約を実現するコードの共有。** |
> **[historical] Y-1**: `declared_untrusted_inputs[]` は implementation closure の universe から分離される**(dependency manifest §5.3・版は §0 header の dependency_manifest_schema_id により束縛)。
> **[historical] Y-4**: 判定基準は dependency manifest §5.3.2(U-1〜U-4・**Y-4d: build-time artifact は入力クラスに置けない**・版は §0 header の dependency_manifest_schema_id により束縛)。


---

## 7. 二 verifier の独立要件 {#independence}

**dependency manifest(§0 header が pin する版)を参照する。** 以下の括弧内 ID は **すべて dependency manifest の現行 clause-ID**であり、**本版で全行を突合済み**(前版は修理前の ID を参照していた・**自認**)。

[normative-check-table]
| # | 義務 |
|---|---|
| **C-1″** | A と B は **別実装**であり、`implementation_dependency_closure` を**推移的閉包**として提出する(H-1′)。検収は **attestation と受領側 fixpoint 再計算**による(depth の見た目で判定しない)。**R-6 の昇格対象が `content_digest` に解決されない場合も [12]**(H-1a″)。**subject binding の欠落・不一致も [12]**(**I-0c″**)。 |
| **C-2** | 同一性は **content digest** で判定される(H-2)。別名・別 path・薄い wrapper では独立性を主張できない(H-2a・H-2d)。 |
| **C-3‴** | 共有してよいのは **TCB 四欄**に列挙された値のみ(H-5e)。**`role = math-helper` を TCB に入れてはならない**(H-3・H-3a)。**`code-generator` が math-helper を生成する場合も同じ扱い**(H-3a′)。**`allowed_shared_family[]` は audit 専用の acknowledged justification list であり、family 交差の判定から差し引かない**(FA-1・FA-2)。 |
| **C-4‴** | **禁止交差は receipt 受領側が四面から再計算する**(H-4・I-0″・I-1・I-2・**I-3a** binary / **I-3b** source / **I-3d** build・I-5′・I-6・I-8)。**family(I-3c′)は audit flag であり単独では [11] を発しない**(M-3′)。 |
| **C-5‴** | TCB の拡張は**追加側に挙証責任**があり receipt を要する(H-5・H-5a・H-5b・H-5c)。**四欄は独立**(H-5d′)。**欄数は四**(H-5e)。 |
| **C-6⁗** | **分岐 owner = dependency manifest §2.34 `[branch-contract]`(BC-1)。** **preimage 欄は `[branch-contract]` の `required_keys` に従って提出する**(**`true` は 8 欄・`false` は 4 欄 + `forbidden_keys` は ABSENT**) — `source_artifact_digests[]`・`toolchain_digest`・`build_step_digests[]`(E-5・E-6)・`build_definition_blob_digest`・`pinned_input_digests[]`(E-9′)・`subject_build_binding_digest`(**E-10′**)。**preimage の完全性は E-7‴**、**申告値が参照値にすぎないことは E-8″**。**受領側は `[branch-contract]` の `recompute` に従って再計算する** — **`true` / top-level は D-1・D-2・D-3・D-4′ の四つ**、**`false` leaf は D-1・D-2 の二つのみ**(D-R2⁗・I-0c″ と同一分岐)(D-R1・**D-R2⁗**・D-R3・**I-0″**・**I-0c″**)。**binding は record ごとに自己完結する** — **preimage 第一成分は top-level では `subject_code_digest`、entry では当該 entry 自身の `content_digest`**(**SB-1′**・**SB-2′**・**SB-3′**)。**異 record 間の照合は行わない**(**SB-6** — build 共有の検出は I-3d の領分)。**build record の不在は `build_record_present` で明示宣言する**(**SB-5**)。**identity binding が保証するのは取り違え防止まで**であり(SB-4・**SB-7**・D-R4)、**実生成関係を主張する場合は `build_attestation` が必須**(BA-1・**BA-2**・BA-3・BA-4・BA-5・I-0d)。**output-affecting な toolchain / build step / code generator は closure entry へ必須昇格**(R-1〜**R-6**)。**`implementation_family_id` は receipt authority が mint する audit flag**(M-1′・M-2′・**M-3′**・M-4・M-5)。 |
| **C-7** | **A と B は互いの中間結果を読まない。** 相手の `result_digest` を自分の再計算の**前に**参照することを禁止する。**§5.1 C1 の比較は、両者が独立に確定した $R_A$・$R_B$ に対して受領側が行う。** |
| **C-8‴** | **初期 TCB は四欄とも空**(T-1″)。ゆえに **A と B は異なる runtime で実装し、かつ異なる toolchain / build step で build する**(T-2′ — **共有 toolchain は build face で [11]**)。共有するなら**実装着手前の receipt** で該当欄に追加する(T-3・T-4)。 |
| **C-9** | **【本版新設】入力クラスの規律**: `declared_untrusted_inputs[]` は implementation closure の universe 外(Y-1・Y-2・Y-3)。**入力クラスへの math-helper 混入禁止**(Y-4・Y-4a・Y-4b・Y-4c・**Y-4d**: build-time artifact は入力クラスに置けない・U-1〜U-4)。 |

> **【[sync-note]】本節の括弧内 ID は dependency manifest の clause+check registry に実在するものだけを用いる。** **script v3 の check #12 が両方向の集合照合で機械検査する**(プライム `′″‴` は U+2032 系の exact match)。

---

## 8. governing spec への erratum 案【記録】{#erratum}

> **[historical]** **【状態・v4 更新】以下 A/B/C は `mb/ninfty-stage2-predicate/v8` として発行済み**(裁定 80)。**便 67 F3・F4・F5 で anchor / pin / topology / routing / P-S3 は PASS。**
> **[historical]** **v9 に残る 2 件**(便 67 F6・F8・裁定 81 で発行決定): **(D) §5.3 invariant 2 を P-S3 と同期**(v8 は public schema と §5.4.1 だけを足し、**既存 invariant 2「public は primary のみ」を直し忘れて同一 blob 内で直接矛盾**していた — **契約側の案 B 自身が「invariant に条文を足す」と要求していたのに漏れた。自認**)・**(E) §9 の live gate を「v6 の Sol 監査 PASS」から「本 exact bundle(spec+contract+manifest の三 digest)の freeze PASS receipt」へ**(v6 は erratum 前であり、その audit PASS は現 bundle の freeze PASS の代用にならない)。

> **[historical]** **以下は要請時の原文(記録)。**

### 案 A — §5.3.3 を二軸 routing へ(便 66 F4)

> **v7 §5.3.3 の step 1〜4「前段が reason を発したら停止」を、本稿 §5.1 の二軸へ差し替える。**
> - **semantic axis**(S1 envelope / S2 native mathematics / S3 witness validity)— **軸内は排他**。
> - **concordance axis**(C1: canonical result vector $R_A$ vs $R_B$)— **入力 digest が一致する限り常に評価**し、**semantic reason と共存**する。
> - 合成規則: `if R_A ≠ R_B: add [26] / elif S2 の native reason が空 かつ R_A=R_B が failure を含む: add [25]`。
> - **[24] と [25] は semantic 軸内で排他。[26] は別軸なので [13]–[24] と同時に立つ。**
> - **[26] の述語は「canonical per-witness result vector の不一致」**であり、overall verdict の不一致に限定しない(限定するなら `verifier-verdict-mismatch` へ改名すべき)。

### 案 B — public envelope に `secondary_reason_codes[]` を新設(裁定 79)

> **§5.1 public envelope に `secondary_reason_codes[]`(canonical 昇順・primary を含まない)を追加**し、**§5.3 の invariant に次を足す**。
> - `primary_reason_code` は従来どおり**単数・全域**。
> - **public の secondary は concordance axis の code に限る**(現行 enum では [26] のみ)。**semantic の非 primary code は sealed の `all_reason_codes[]` にのみ置く** — public の情報量増加を 1 ビットに抑えるため(本稿 P-S3・P-S4)。
> - 空のときは**空配列を明示**する。

### 案 C — external anchor の digest 型付け(便 66 F8)

> **v7 §6 は `schema_id(input-separation) = dependency_manifest_schema_id + "#input-separation"` としながら、`bound_blob_digest(all of the above) = predicate_spec_digest` で束ねている。** `input-separation` の実体は **manifest の §5.3** なので、**bound blob は manifest digest でなければならず、spec 自身の digest ではない。**
> ```text
> # spec 内部 anchors
> bound_blob_digest(cert .. witness-kinds) = predicate_spec_digest
> # external manifest anchor
> schema_id(input-separation)       = dependency_manifest_schema_id + "#input-separation"
> bound_blob_digest(input-separation) = dependency_manifest_schema_digest
> ```
> **併せて `dependency_manifest_schema_id/digest` の定義を先に置き forward reference を消す。**

### 併せて governing spec §6 で pin すべき値(当時の記録・値は本稿 §0 header が正本)

> **[historical]** **本節は当時(spec §8 erratum 提案時点)の pin 案の記録であり、実際の pin 値は本稿 §0 header(現行版)を正本とする。** verifier_contract_id は「本稿自身の ID」・verifier_contract_digest は「本稿の sha256」・dependency_manifest_schema_id/digest は「§0 header が pin する manifest の ID/digest」を指す、という**役割の記録**であって、リテラルな旧版 ID を再掲するものではない(旧版 ID の再掲は §0 header・supersedes・差分表にのみ許される、という LA-2 の規約に従う)。
**hash 順序は manifest → contract → spec → receipt**(便 66 F11)。**spec 自己 digest と contract の governing-spec digest は receipt 側**に置く。

---

## 9. 適合宣言【chg v5 で同期・F7・F13.3】{#conformance}

> **[historical]** **⚠ v4 の欠陥(自認)**: §7 の実際の義務 ID は `C-1′, C-2, C-3′, C-4′, C-5′, C-6″, C-7, C-8′` だったのに、**§9 の machine-facing `conformance_record` は v3 のまま**だった — `build_definition_blob_digest` と `pinned_input_digests[]` が欠落し、comment は manifest v3、`covered_clauses` は `C-1..C-5, C-6′, C-7, C-8` で **prime を落とす range 表記**。**旧 record を提出した実装が `uncovered_clauses=[]` と自己申告しつつ、C-6″ の build 義務を machine record 上まったく提出しない反例があった。****§9 は「契約適合」を宣言する schema そのものであり、compliance boundary を v3 へ巻き戻していた**(便 68 F7)。

```text
conformance_record = {
  contract_id, contract_digest,
  verifier_id, code_digest,

  # --- provenance preimage 6 欄(dependency manifest §2.1 E-5・E-6・E-9′・E-10′・版は §0 header の dependency_manifest_schema_id により束縛)---
  source_artifact_digests[],
  toolchain_digest,
  build_step_digests[],
  build_definition_blob_digest,
  pinned_input_digests[],
  subject_build_binding_digest,

  # --- 受領側が再計算する導出値 ---
  source_closure_digest, implementation_lineage_digest, build_root_id,
  build_root_id_recomputed_ok, subject_build_binding_recomputed_ok,
  implementation_family_id,          # audit flag
  build_attestation,                 # optional(dependency manifest §2.5・版は §0 header の dependency_manifest_schema_id により束縛)

  # --- closure と入力 ---
  implementation_dependency_closure[],
  declared_untrusted_inputs[],

  # --- TCB 四欄(dependency manifest §5.2・初期値はすべて []・版は §0 header の dependency_manifest_schema_id により束縛)---
  allowed_shared_tcb[], allowed_shared_source_tcb[],
  allowed_shared_build_tcb[], allowed_shared_family[],

  covered_clauses = [C-1″, C-2, C-3‴, C-4‴, C-5‴, C-6⁗, C-7, C-8‴, C-9, CR-1, CR-10, CR-11, CR-2, 
                     CR-3, CR-4, CR-5, CR-6, CR-7, CR-8, CR-8b, CR-9, LA-1, LA-2, LA-3, P-S1, 
                     P-S2, P-S3, P-S4, P-S5, P-S6, R-1, R-2, R-3, V-0, V-1, V-2, V-3, W-1, W-3, 
                     W-4, W-5, W-6, X-1, X-1a, X-2, X-3, X-4, X-5, X-6, Y-1, Y-2, Y-3, Y-4]
  covered_procedure_checks = [C1, P-0.1, P-0.2, P-0.3, P-0.4, P-0.5, P-0.6, P-0.7, P-0.8, P-1.1, 
                              P-1.2, P-1.3, P-1.4, P-1.5, P-3.1, P-3.2, P-3.3, S1, S2, S3, W-1, 
                              W-2, W-2′, W-3, W-4, W-5, W-6]
  uncovered_checks = []
  uncovered_clauses = []
}
```

### 9.1 `normative_clause_registry`【F13.3】{#clause-registry}

[normative-check-table]
| # | 条項 |
|---|---|

```text
[registry-definition]                 # 正本: 文書表示と checker が同一の literal を読む
clause_id_regex = ^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴⁗]?)\*\* \|
check_id_regex  = (?<![A-Za-z0-9])(W-2′|D-[0-9]′?|R-[0-9]|U-[0-9]|P-[0-9]\.[0-9]|W-[0-9]|S[123]|C1)(?![A-Za-z0-9])
clause_scope    = [normative-clause-table]   # 差分表/fence/blockquote を除く table 行のみ
check_scope     = tagged [normative-check-block] fence + operative [normative-check-table] row のみ
#                 (通常 prose / blockquote / conformance / registry-definition / branch-contract は母体外)
#                 (covered/uncovered/registry-definition/branch-contract/conformance の meta block は除外)
prime_class     = U+2032 U+2033 U+2034 U+2057   # exact match(ASCII 代用不可)
alternation_rule = long-token-first (W-2′ before W-[0-9])
fixture_1 = extract_clause of a C-6⁗ row yields exactly C-6⁗
fixture_2 = extract_check of W-2′ yields exactly W-2′
```

| **CR-1** | **`normative_clause_registry` の抽出規則**: 直上の `[registry-definition]` block の **`clause_id_regex` が唯一の正本**であり、**文書表示と checker は同一の literal を読む**(**checker は起動時にこの block の自己 digest を表示する**)。適用範囲は `clause_scope`。**`covered_clauses` はその全列挙。** 手続き段階のラベルは clause ではなく **check** なので **`covered_procedure_checks` に分けて全列挙**する(CR-5)。**【本版・B69-2】前版は prime class を `[′″‴]?` と凍結し quadruple prime `C-6⁗` を registry から落としていた**(checker 側が無断で `[′″‴⁗]?` へ拡張していた) — **文書側を昇格して両者を一本化。自認。** |
| **CR-2** | **受領側は exact set equality で照合する**: `covered ∩ uncovered = ∅` かつ `covered ∪ uncovered = normative_clause_registry`。 |
| **CR-3** | **range 表記(`C-1..C-5` 型)は禁止**する — **prime / double-prime を落とすため**(便 68 F13.3)。**** |
| **CR-4** | registry に無い ID を `covered` に書く、または registry の ID が両集合のどちらにも無い場合は**契約不適合**。 |
| **CR-5** | **【chg v6 新設・内部ゲート FINDING-3】`procedure_check_registry` の抽出規則(機械的)**: 本稿の本文に現れる **check ラベル** (`D-<digit>`・`R-<digit>`・`U-<digit>`・`P-<digit>.<digit>`・`W-<digit>`・`W-2′`・`S1`・`S2`・`S3`・`C1`)の全体。**受領側は `covered_procedure_checks ∪ uncovered_checks = procedure_check_registry` かつ `∩ = ∅` を exact set equality で照合する。** |
| **CR-6** | **check は clause と同格の完全性保証を受ける。** **`covered_procedure_checks` から check を黙って落とすことは様式不適合**であり、CR-2 と同じ扱いで検出される。 |
| **CR-7** | **check 側にも range 表記を禁止**する(CR-3 と同じ理由)。 |
| **CR-8** | **【本版新設・B70-2・F9.2 逐語】registry の抽出母体と coverage を分離する。** **`defined_procedure_checks` は明示タグ `[normative-check-block]` を持つ normative procedure block と normative table 行だけから抽出**する。**`covered_procedure_checks` は conformance record から抽出**する。**禁止**: `covered_procedure_checks` / `uncovered_checks` / `[registry-definition]` / `[branch-contract]` の各 meta block を `defined_procedure_checks` の抽出母体へ入れること。 |
| **CR-8b** | **【本版新設・裁定 91】per-document scope**: 各文書の `covered_procedure_checks` は、**その文書に normative 定義がある check だけ**を列挙する(dependency manifest = `D-*` / `R-*` / `U-*`、verifier contract = `P-*` / `W-*` / `S1`–`S3` / `C1`)。**相互の義務は clause 散文(C-6⁗ 等)で表現済み**であり、**他文書側の概念を covered に混入させない**(Sol 便 69 F6 末尾「registry scope 案で併せて除く」の履行)。 |
| **CR-9** | **【本版新設】前版の欠陥(自認)**: 抽出母体が conformance fence を含んでいたため、**covered に未知 ID を書いた瞬間それ自身が registry の一員になり**、CR-4 の「registry に無い ID を covered に書けば不適合」が成立しなかった。**独立 probe で未知 ID を covered に足しても equality が true のまま**になり、さらに **coverage list だけが生成した幽霊 ID が 1 件**存在した。 |
| **CR-10** | **【本版新設・F11.2 逐語】registry は三層とし、層ごとに owner を分ける。** **`defined_checks` = 契約本文** / **`claimed_covered` = conformance record** / **`implemented_checks` = 受領側 executable inventory**。**freeze 時は前二者の exact equality**、**実装 receipt 時は三者の exact equality** を要求する。 |
| **CR-11** | **CR-5〜CR-7 は `implemented_checks` 層が未成立**である(受領側 executable inventory が存在しない)。**現状の主張は「defined = claimed_covered」まで**であり、**三者 equality は `[current-unknown]`** として receipt / EP へ送る。 |
> **[historical] CR-3**: v4 の `covered_clauses` は range を使い、実際に `C-3′`・`C-4′`・`C-5′`・`C-6″`・`C-8′` を覆っていなかった・自認。
> **[historical] CR-6**: v5 は clause 側にしか母集合規則を持たず、「procedure check への分離」が事実上の義務の格下げになっていた**(内部ゲート FINDING-3・**自認**)。


**`uncovered_clauses` が非空の実装を「契約適合」と呼ばない。** 部分適合は `partial verifier / UNKNOWN` として扱う。

---

## 10. live authority refs(機械可読)【F13.1・裁定 83】{#live-authority}

```text
live_authority_refs[] = [
  { artifact_id: "mb/ninfty-stage2-predicate/v19",
    digest_or_receipt_slot: "receipt:governing_spec_digest",
    anchor: "§4.1 certificate schema / §5.3 state machine / §5.3.2 integrity_priority" },
  { artifact_id: "mb/dependency-manifest/v14",
    digest_or_receipt_slot: "e892be68e79244c8493e37ec77eb3a1cbdb29ee45a911f73040aadaebbb889af",
    anchor: "§2.1 preimage / §2.4 subject binding / §5.2 TCB / §6 intersections" }
]

historical_quotation_refs[] = [
  { artifact_id: "mb/ninfty-verifier-contract/v1..v13", note: "版履歴・差分表・自認文のみ" },
  { artifact_id: "mb/dependency-manifest/v1..v12",      note: "差分表・自認文のみ" },
  { artifact_id: "mb/ninfty-stage2-predicate/v5..v18", note: "§0.2 差分表・§8 erratum 記録のみ" }
]
```

[normative-check-table]
| # | 条項 |
|---|---|
| **LA-1** | **本稿の live な版束縛は §0 header の 3 欄(`contract_id` / `governing_spec` / `dependency_manifest_schema_id`)と上の block のみ。** 本文の他の spec 参照は**版中立**(「governing spec §…」)である。 |
| **LA-2** | **release lint は本文の version token を走査し、`live_authority_refs[]` に無い旧版 ID が live 文に現れたら fail させる。** `historical_quotation_refs[]` の ID は差分表・supersedes・自認文・§8 記録にのみ現れてよい。 |
| **LA-3** | **【[sweep-def]・現行有効な lint 契約】** 本行は `[historical]` ではなく、**現在の release lint が従う sweep 対象定義**である。定義は直下の `sweep_definition` block を正本とする。 |

```text
sweep_definition = {                      # [sweep-def] 現行有効
  self_artifact   = "mb/ninfty-verifier-contract/*",
  self_alias      = "contract v<N>",
  other_artifacts = [ "mb/ninfty-stage2-predicate/*", "mb/dependency-manifest/*" ],
  other_aliases   = [ "spec v<N>", "manifest v<N>" ],
  bare_token      = "v<N> + 助詞",       # 【chg v<N> …】 のみ allowlist
  current_version = "v14",
  historical_upper_bound = "v13",   # = current - 1(script v3 が自動照合)
  rationale = "自版だけを見る sweep は不十分 — 便 68 F6 が反証した失敗型"
}
```
> **[historical] LA-3**: sweep の対象定義**: 自 artifact の全版 token("contract v1..v5" / `mb/ninfty-verifier-contract/v*`)と、**他 2 文書の全版 token**("spec v5..v10" / `mb/ninfty-stage2-predicate/v*`・"manifest v1..v5" / `mb/dependency-manifest/v*`)。