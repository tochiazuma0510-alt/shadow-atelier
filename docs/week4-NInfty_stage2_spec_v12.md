# $N_\infty$ searcher — **stage 2 述語の仕様(spec v12・自己完結版)**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 85)。**

> **【版履歴】本版 = 前版の同期。** 起点は **内部前哨ゲート(falsifier)の第 2 巡**(cross-document 同期類型)。変更は **2 点** — **(L) contract / manifest の新版 pin と §9 exact_freeze_bundle の更新**・**(M) §10 `live_authority_refs[]` の label—digest 対応の点検**(script v3 の check #13 が機械照合)。**数学核・入口契約・lane・certificate・二軸 routing は前版と逐語同一。**

> **【版履歴】v11 = v10 の修理。** **起点は Sol の監査便ではなく、便 69 発送前の内部前哨ゲート(falsifier)** — **self-audit 9/9 ALL PASS の外側**で見つかった。変更は **2 点** — **(J) FINDING-2 の修理**: §4.1 certificate schema の**未定義欄 `verifier_evidence` を削除**し、独立性証跡が SEALED_INTERNAL 並列であることを注記・**(K) contract v6 / manifest v6 pin・§9 exact_freeze_bundle を v11 束へ**。**数学核(§1)・入口契約(§2)・lane(§3)・二軸 routing(§5)は v10 と逐語同一。****再監査範囲は (J)(K) に限る。**

> **【版履歴】v10 = v9 の同期版。** 変更は **3 点のみ** — **(G) live な `contract v3` 参照の版中立化**(:441 の二軸 routing 定義と :478 の normative X-6 は **operative 本文**であり、spec 自身が contract v4 を pin する一方で **nominal owner として v3 を指していた**)・**(H) §6 pin を contract v5 / manifest v5 へ・§9 exact_freeze_bundle を v10 束へ**・**(I) §10 に `live_authority_refs[]` の機械可読 block を新設**。**数学核(§1)・入口契約(§2)・lane(§3)・certificate(§4)・二軸 routing の内容(§5)は v9 と逐語同一。****再監査範囲は (G)(H)(I) に限る。**

> **【版履歴】v9 = v8 の erratum。** 変更は **3 点のみ** — **(D) §5.3 invariant 2 を P-S3 と同期**(v8 は public schema と §5.4.1 を足しながら **invariant 2「public は primary_reason_code のみ」を直し忘れ、同一 blob 内で直接矛盾していた**)・**(E) §9 の live gate を「v6 の Sol 監査 PASS」から「本 exact bundle の freeze PASS receipt」へ**・**(F) §6 の pin を contract v4 / manifest v4 へ更新**。**それ以外の節は v8 と逐語同一。****invariant 1・3・4 は不変 — 更新したのは invariant 2 のみ。****再監査範囲は (D)(E)(F) に限る。**

> **【版履歴】v8 = v7 の erratum。** 変更は **3 点のみ** — **(A) §6 の `#input-separation` 束縛の修正**(v7 は external anchor を **v7 自身の digest** に束ねており **freeze binding が偽**だった)・**(B) §5.1 / §5.3.3 の二軸 routing(semantic / concordance)と public `secondary_reason_codes[]` の新設**・**(C) §6 の pin を contract v3 / manifest v3 へ更新**。**それ以外の節は v7 と逐語同一である。****再監査範囲は (A)(B)(C) の erratum 項に限る。**
> **v7 の E1(§4.2 の witness 型分け)は便 66 F3 で PASS を得ており、本 erratum は触れない。**

> **【版履歴】v7 = v6 の erratum。** 変更は **2 点のみ** — **(E1) §4.2 の数学的型誤りの修正**(Bézout を点同一性の witness としていた誤り → `ideal-equality` 限定 + `disjointness` 別型)・**(E2) `[26]` を `checker-mismatch` から `verifier-result-mismatch` へ改名**(state machine の該当行・enum・説明文を同期)。**それ以外の節は v6 と同一である**(§0.0 lifecycle・§0 差分表・§1 数学核・§2・§3・§4.1・§4.3・§4.4・§5.1・§5.2・§5.3 の構造・§6・§7・§8・§9)。**v6 は Sol 便 64 で本体 PASS を得ており、本 erratum は §4.2 の誤りのみを外科的に除く。**

## 0.0 lifecycle state【B63-4・便 63 F11】

> **⚠ 無時制の状態欄を frozen artifact に埋め込むと、freeze ID / 実装認可を外から発行した瞬間に artifact 自身が反対の live 状態を主張し続ける。欄を直接更新すれば full digest が変わり、提示済み hash は freeze digest でなくなる。自認**(A62-2 と同型の欠陥)。

```text
embedded_state_at_candidate_creation = {
  freeze_id:      NOT ISSUED,
  implementation: NOT AUTHORIZED,
  model_builder:  LOCKED
}
live_status_authority = Sol freeze reply + commander receipt
live_freeze_and_authorization_authority = approved freeze receipt
```
**本稿の上記 blob は「candidate 作成時点で埋め込まれた状態」であって live status ではない。live status の正本は approved freeze receipt 側にあり、receipt 発行によって本稿を書き換える必要はない(digest 不変)。**

```text
supersedes_draft             = sha256:77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
audited_predecessor_rejected = sha256:813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
supersedes_v3 = sha256:83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b
supersedes_v4 = sha256:9b2f26ab436d44a059ad5e33c388f8486e24a47c343e4b1894542fd0dc263fb2
supersedes_v5 = sha256:290c7d5768f95e9a1b9412fea123cfa36527f7e3917a1b656fe4479065d9428b
supersedes_v6 = sha256:00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a   # audited (Sol 便 64: 本体 PASS)
supersedes_v7 = sha256:4589df9f6b4eef97b96d3c6ec02b370941c83f653926ff51ac7646ce83973e6e   # audited (Sol 便 66: E1 PASS / E2 未閉鎖・binding FAIL)
supersedes_v8 = sha256:9a7df744341e41f30d82f1b36c26638925abee89e367cd5f3d26675302539963   # audited (Sol 便 67: anchor/pin/topology/routing/P-S3 PASS / invariant 2 矛盾・§9 gate FAIL)
supersedes_v9  = sha256:645cb6ae04a413d3cdde0d292c7f2ce51acc7524c1a5ac4ef2d7f294b08890ea   # audited (Sol 便 68: invariant 2・build face・family 降格+N-1・gate・anchor/topology すべて PASS / live contract v3 参照のみ FAIL)
supersedes_v10 = sha256:f1fb9f277ff65cc34e9b5d90bd6504119e087333bf4a98a46bf327c2b561cf45   # 内部前哨ゲート(falsifier)差戻し — Sol 便による判定ではない (FINDING-2)
supersedes_v11 = sha256:43e65e067ca75e826aff499193b00eeff0b797dcd470f633a809ab060714ebff   # 内部前哨ゲート第 2 巡差戻し — cross-document 同期類型 (Sol 便ではない)
erratum_scope_v7 = { §4.2 witness kind (math type error), [26] rename }
erratum_scope_v8 = { external anchor binding (A), two-axis routing + public secondary (B), pins (C) }
erratum_scope_v9  = { invariant 2 sync (D), implementation gate origin (E), pins to v4 artifacts (F) }
erratum_scope_v10 = { live contract ref version-neutralization (G), pins to v5 artifacts (H), live_authority_refs block (I) }
erratum_scope_v11 = { undefined certificate field removal (J), pins to v6 artifacts (K) }
erratum_scope_v12 = { pins to new contract/manifest (L), authblock label-digest audit (M) }
v12_trigger = internal falsifier gate, round 2 (not a Sol audit reply)
v11_trigger = internal falsifier gate (not a Sol audit reply)
hash_order = manifest -> contract -> spec -> receipt        # 便 66 F11(非循環)
self_containment = FULL RESTATEMENT (no external proof import)
```
**正典**: `sol/sol_reply_65_freeze.md` **F4–F8**・`sol/sol_reply_63_final2.md` **F4 / F8–F11**・便 62 F4–F13・便 61・便 60・便 59・便 54・S5 設計(命題 S5-1 / 命題 S5-2 / 系 S5-2a / §3.3.5 S5-3∞)・便 36 F2.1。
**接触規律**: 値に依存しない。$C:=\hat c_\mu$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。

> **【自己完結の方針(v5 から継続)】** 便 62 F12 問 6 の裁定どおり **§1 に数学核を全文再掲し、v3/v4/v5 から proof body を import しない**。**normative body は本稿のみ。**

---

## 0.0.-4 前版差分【裁定 85・内部前哨ゲート第 2 巡起点】

> **教材(採録)**: 「**修理の自己完結 ≠ 体系の整合**」 — **同期は文書単位でなく clause-ID 単位で機械検査する。**

| ID | 前版 | 本版 | 出所 |
|---|---|---|---|
| **L** | §6 pin・§9 exact_freeze_bundle が前版の contract / manifest | **新版へ**。**三 digest のいずれかが変われば gate 再取得**の規律は不変 | 裁定 85 |
| **M** | §10 `live_authority_refs[]` の label—digest 対応を**機械検査していなかった**(下位文書で label 遅れが実際に起きた) | **check #13 で artifact_id の版と digest を §0 / §6 の pin 表と機械照合**。**LA-3 を `[sweep-def]` 型へ再型付け** | 第 2 巡 重大 2・軽微 1 |

---

## 0.0.-3 前版差分【裁定 84・内部前哨ゲート起点】(【chg v11 から継承・変更なし】)

> **起点の明示**: 本版の差戻しは **Sol の監査便ではなく、便 69 発送前の内部前哨ゲート(falsifier)**による。**self-audit 9/9 ALL PASS の外側**の指摘である。

| ID | v10 | v11 | 出所 |
|---|---|---|---|
| **J** | §4.1 の certificate schema 末尾に **`verifier_evidence`** があるが、**この名前はどこにも定義されていない**。**§4.4 が定義するのは `independence_evidence`** であり、**§5.2 `SEALED_INTERNAL` でも certificate と並列の別オブジェクト**である。**verifier contract 側にも `verifier_evidence` は一度も現れず、検査契約がこの欄を検査しない**状態だった。**自認** | **§4.1 から当該欄を削除**し、**「独立性証跡は certificate の欄ではなく `SEALED_INTERNAL` の並列オブジェクト(§4.4 で定義・§5.2 で格納)」**と注記。**certificate 内の重複を作らない最小修理**を採る | 内部ゲート FINDING-2 |
| **K** | §6 pin = contract v5 / manifest v5・§9 exact_freeze_bundle = v10 束 | **contract v6 / manifest v6 へ**・**§9 の三 ID を v11 束へ** | 裁定 84 |

> **これ以外の節は v10 と逐語同一。** **再監査は (J)(K) に限る。**

---

## 0.0.-2 前版差分【裁定 83】(【chg v10 から継承・変更なし】)

| ID | v9 | v10 | 出所 |
|---|---|---|---|
| **G** | :441 の「二軸 routing(… **contract v3** §5.1 X-1〜X-6 と同期)」と :478 の「[26] …(**contract v3** §3.4 R-1)」は**版履歴でも historical quotation でもなく、現行 routing の定義と normative X-6 の本文**である。**spec 自身は contract v4 の exact digest を pin するので、同じ operative block が nominal owner として v3 と v4 の二つを指す。****内容が現時点で逐語同一でも、exact artifact gate では owner version を同一視できない。**「旧版起点の live 残存 sweep = 0」という前便の申告は**反証された**・**自認** | **live 参照を版中立化**(「**verifier contract §5.1**」「**verifier contract §3.4**」— **版 token を持たない節参照**)。**版束縛は §6 の pin 1 箇所と §10 の `live_authority_refs[]` に集約** | 便 68 F6.1 |
| **H** | §6 pin = contract v4 / manifest v4・§9 exact_freeze_bundle = v9 束 | **contract v5(`e66ab58f…`)/ manifest v5(`8623c83f…`)へ**・**§9 の三 ID を v10 束へ** | 裁定 83・便 68 F11 |
| **I** | live 参照の版 token が本文に散在し機械 lint できない | **§10 に `live_authority_refs[]` / `historical_quotation_refs[]` を新設**・**LA-3 に sweep の対象定義**(自版 + 他 2 文書の全版 token)を明記 | 便 68 F13.1・裁定 83 |

> **これ以外の節は v9 と逐語同一。** 便 68 F3・F4・F5 は invariant 2・build face・family 降格 + N-1・gate・anchor / topology を **PASS**。**再監査は (G)(H)(I) に限る。**

---

## 0.0.-1 前版差分【裁定 81】(【chg v9 から継承・変更なし】)

| ID | v8 | v9 | 出所 |
|---|---|---|---|
| **D** | §5.1 が public envelope に `secondary_reason_codes[]` を置き §5.4.1 P-S3〜P-S6 が **[26] の secondary 出力を normative に要求**する一方、**同じ blob の §5.3 invariant 2 が逐語で「public は primary_reason_code のみを出す(単数・全域)」**としていた。**[24]+[26] の例で P-S5(secondary=[[26]])と invariant 2(secondary を出すな)が同時に operative になり、public envelope が一意に決まらない。**契約側の案 B 自身が「§5.3 の invariant に secondary 条文を足す」と要求していたのに、**public schema と §5.4.1 だけを追加して既存 invariant を直し忘れた**。**prose typo ではなく public output schema と漏洩境界の双方を決める条文の衝突。自認** | **invariant 2 を置換**(§5.3)。**§5.3.3 末尾の「invariant 1–4 はそのまま成立する」も「invariant 1・3・4 は不変・invariant 2 は v9 で更新」へ訂正。** §5.1・§5.3・§5.4.1 の**三箇所を同期** | 便 67 F6 |
| **E** | §9 の boxed chain が **「v6 の Sol 監査 PASS → …」**。**これは版履歴中の historical quotation ではなく current implementation condition。** v6 は E1・E2・A・B・C の erratum 前であり、**v6 の audit PASS は現 exact bundle の freeze PASS の代用にならない**(便 66 F7 で contract/manifest の live v6 参照を blocker としたのと同じ基準)。**自認** | **起点を「本 exact bundle(spec + contract + manifest の三 digest)の Sol freeze PASS + その digest 群を束縛した commander receipt」へ**。**旧版起点の live 残存を全 sweep** | 便 67 F8 |
| **F** | §6 の pin が contract v3 / manifest v3 | **contract v4(`703fb47f…`)/ manifest v4(`378f30c8…`)へ**。hash 順序 manifest → contract → spec → receipt は不変 | 裁定 81・便 67 F11 |

> **これ以外の節は v8 と逐語同一。** 便 67 F3・F4・F5 は anchor / pin / topology / routing / P-S3 を **PASS**。**再監査は (D)(E)(F) に限る。**

---

## 0.0.0 前版差分【裁定 80】(【chg v8 から継承・変更なし】)

| ID | v7 | v8 | 出所 |
|---|---|---|---|
| **A** | §6 は `schema_id(input-separation) = dependency_manifest_schema_id + "#input-separation"` としながら、**`bound_blob_digest(all of the above) = predicate_spec_digest` で一括して束ねていた**。`input-separation` の実体は **manifest §5.3** なので、**bound blob は manifest digest でなければならず spec 自身の digest ではない**。**full-blob anchor が正しい source blob を指さない以上、literal hash が揃っていても freeze binding は偽。自認** | **内部 anchor と external anchor を分離**し、`bound_blob_digest(input-separation) = dependency_manifest_schema_digest` へ。**`dependency_manifest_schema_id/digest` の定義を先に置き forward reference を消す** | 便 66 F8・contract v3 §8 案 C |
| **B** | §5.3.3 は「前段が reason を発したら停止」で後段を抑圧した。**同じ原因の二重分類を防ぐ意図が、別原因として同時に起きた verifier disagreement まで消していた** — ① [24] と A/B の vector 不一致が同時でも [26] が public から落ちる ② A: W-2 FAIL/W-3 PASS・B: W-2 PASS/W-3 FAIL は**両者 overall FAIL でも vector は不一致**なのに [25] を発して step 4 へ行かない(**enum 名と一致しない**)。**自認** | **§5.3.3 を二軸 routing へ**(semantic 軸は排他 / concordance 軸は常時評価・共存)。**[26] の述語を canonical per-witness result vector の不一致に確定**。**§5.1 に public `secondary_reason_codes[]` を新設**([26] 限定・§5.4.1 の理由づけつき) | 便 66 F4・F13・contract v3 §8 案 A/B |
| **C** | §6 の pin が **contract v2 / manifest v2**(いずれも監査 FAIL の candidate) | **contract v3 / manifest v3 の実 digest へ更新**。**hash 順序 manifest → contract → spec → receipt** を明記 | 便 66 F11・contract v3 §8 |

> **これ以外の節は v7 と逐語同一。** v7 の E1 は便 66 F3 で PASS。**再監査は (A)(B)(C) に限る。**

---

## 0.0.1 前版差分【裁定 78】(【chg v7 から継承・変更なし】)

| ID | v6 | v7 | 出所 |
|---|---|---|---|
| **E1** | §4.2 が **`Bézout / reduction certificate`($1=\sum u_ig_i$)を witness メニューに未型付けで併記**。**これは非交差($V(I_1)\cap V(I_2)=\varnothing$)の certificate であって点同一性の certificate ではない** — 反例 $\mathbb Q[x]$, $I_0=(x)$, $I_1=(x-1)$ で $1=x-(x-1)$ ゆえ**異なる二点が PASS する**(witness 群全体の false positive)。**自認** | **§4.2 を 2 kind に型分け** — **`kind = ideal-equality`** が点同一性の唯一の形式(表現係数 または `reduction-to-zero` 列)/ **`kind = disjointness`** は別型で**単射性と余剰排除にのみ**使用。**全 reduction certificate に `reduction-to-zero` / `reduction-to-one` の tag を必須化**。§4.1 に `distinctness_witnesses` 欄を新設 | 便 65 F4・contract v2 §8 |
| **E2** | `[26] checker-mismatch` — **名称が新しい述語(A/B verifier result の不一致)と齟齬**し、述語自体も spec 側に無かった | **`[26] verifier-result-mismatch` へ改名**し、**§5.3.3 に [25]/[26] の相互排他な述語と評価順序を明記**(contract v2 §5.1 X-1〜X-4 と同期) | 便 65 F5・contract v2 §8 |

> **これ以外の節は v6 と逐語同一。** v6 は Sol 便 64 で本体 PASS を得ているので、**再監査の範囲は E1・E2 の 2 点に限る。**

---

## 0. 前版差分(旧)(【chg v6 から継承・変更なし】)

| ID | v5 | v6 | 出所 |
|---|---|---|---|
| **B63-1** | `shared_helper_intersection = ∅` のみ。**直接依存か推移的閉包か未定義**で、別名・wrapper・runtime/parser/CAS をどこまで helper と数えるかも未定義。文字どおり「全 helper」なら標準 runtime の共有で交差は通常空にならず、暗黙に除けば**共通 canonicalizer を除外した証拠にならない** | **§4.4 を推移的依存閉包へ**。`dependency_manifest_schema_id + digest` / `dependency_closure_A[]/B[] = transitive content digests` / `allowed_shared_tcb[] = frozen content digests + role` / `forbidden_shared_math_helper_intersection = (closure_A ∩ closure_B) − allowed_shared_tcb = ∅`。**「直接依存のみの manifest は不可」を条文化**。**intersection は producer の自己申告を信じず receipt 受領側が canonical content digest 集合から導出**。build root / toolchain / implementation provenance も記録。**自認** | 便 63 F8 |
| **B63-2** | 「16 段」と表記(実列挙は $[9]$–$[26]$ の **18 段**)。**public primary = 全順序の最小**としたため、`precondition/degree-mismatch`[1] と `sealed-field-leak`[9] の同時検出で **REJECT[1] が選ばれ証拠汚染[9] を隠す**(設計理由と逆転)。`accepted` が failure と同居しない不変条件も無い。G-2 が入力 digest 不一致を `divisor-equality-failure` へ送り `digest-mismatch`[12] と**二重割当** | **18 段に数え直し**。**§5.3 を verdict state machine へ**(verdict 決定と reason priority を**分離**・`primary = minimum(I, integrity_priority)`・`accepted` は $I=R=\varnothing$ のときのみ)。**envelope-level leak / digest / dependency check を early REJECT より先に実行**。**G-2 の routing を分割**(digest 不一致 → `digest-mismatch` / witness 欠落・不成立 → `divisor-equality-failure`)。**自認** | 便 63 F9 |
| **B63-3** | §6 の digest が `sha256(§x.y 本文)` という**計算式**で 64 桁 hex ではなく、heading 行・区切り・改行正規化の**境界規約も未定義**(同じ blob から複数の正当な section digest が出る)。ID も statement の説明(`"K^x / (K^x)^2"` 等)で versioned artifact ID でない。外部 dependency の digest を**自分の段落**へ向けていた | **section digest を全廃**し、**全 fragment を full-blob digest へ anchor**(便 63 F10.3 の最小形・裁定 75 の推奨)。`predicate_spec_id = "mb/ninfty-stage2-predicate/v6"` / `predicate_spec_digest = <発行時記入>` / `lemma_id = predicate_spec_id + "#anchor"` / `bound_blob_digest = predicate_spec_digest`。**byte-range 抽出規約の凍結を丸ごと回避**。外部 dependency は**外部 source artifact の versioned ID + digest 欄**として分離。**自認** | 便 63 F10 |
| **B63-4** | `NOT ISSUED / NOT AUTHORIZED / LOCKED` が**無時制**で、§9 も現行命令として再掲 | **§0.0 の `embedded_state_at_candidate_creation` + `live_status_authority` 分離形へ**。**§9 も時制付き**(receipt 前は禁止 / approved receipt 後は **receipt の scope に限って**認可)。**自認** | 便 63 F11 |

> **便 63 F9.2 の局所判断は保持**: `[15] pell-derivative-mismatch` と `[25] divisor-equality-failure` の同時例で **primary = [15]**。**18 段内部の順序方針そのものには Sol も反対していない。**

---

## 1. 数学核(**全文再掲**)

### 1.1 設定と**体の型**【F7.1】

$$ C_{\rm crv}:\ y^2=f_6(x),\quad \deg f_6=6,\ f_6\ \text{monic squarefree};\qquad \mu=a(x)+p(x)\,y,\quad \deg a=5,\ \deg p=2,\ a_5=p_2\ne0 $$
$$ \textbf{(Pell)}\ \ a^2-f_6p^2=C\in\mathbb Q^\times,\qquad \textbf{(Or)}\ \ (\mu)=5P_0-5P_\infty $$

> **【chg v5・F7.1】体と量化の型(4 つは別物)**
> ```text
> curve coefficient field   = Q          # a, p, f6 の係数体
> geometric working field   = k = Qbar   # 幾何点・fiber・divisor を取る体
> v                         in k^times   # 特に v != 0(j(v)=C/v を使う箇所)
> prediction field          = K = Q(zeta_20)   # whitelist の squareclass 用(§7)
> ```
> **valuation の正規化**: 各 closed point $P$ の $\operatorname{ord}_P$ は**整数値に正規化**($\operatorname{ord}_P$ の像が $\mathbb Z$)。
> $\pi:C_{\rm crv}\to\mathbb P^1_x$、$\iota$ = 超楕円対合、$j(v):=C/v$($v\in k^\times$)。
> **$\gcd(a,p)=1$ は (Pell) と $C\ne0$ から自動。**
> **⚠ v4 の欠落(自認)**: v4 は $k$ を定義せず $v$ の所属も量化していなかった。**係数体 $\mathbb Q$・幾何点を取る体・prediction field は別の型**である(便 62 F7.1)。

### 1.2 補題 `N∞-N`(norm / divisor pushforward) {#N-inf-N}

$$ H_v:=(v-\mu)(v-\mu^\iota)=(v-a)^2-p^2f_6=v^2-2va+C \tag{N-1} $$
> **補題 `N∞-N`.** $v\in k^\times$、$v\ne\infty$ に対し
> $$ \operatorname{div}_{\mathbb P^1_x}(H_v)=\pi_*\operatorname{div}_{C_{\rm crv}}(v-\mu)=\pi_*[\mu^{-1}(v)]-5[\infty_x] \tag{60.1} $$
> $$ \boxed{\ (H_v)_0=\pi_*[\mu^{-1}(v)]\ } \tag{60.2} $$

**証明.**
1. $\mu\mu^\iota=C$、$\mu+\mu^\iota=2a$ より $(v-\mu)(v-\mu^\iota)=v^2-2va+C$。左辺は $\iota$-不変ゆえ $k(x)$ に属し、それが $H_v$。
2. $k(C_{\rm crv})/k(x)$ は**次数 2 の有限分離拡大**(標数 0)。体のノルム
$$ N:=N_{k(C_{\rm crv})/k(x)}:\ k(C_{\rm crv})^\times\to k(x)^\times,\qquad N(g)=g\,g^\iota $$
に対し $H_v=N(v-\mu)$。**整数値に正規化した closed-point valuation について**
$$ \boxed{\ \operatorname{ord}_P N(g)=\sum_{Q\mid P}[\kappa(Q):\kappa(P)]\ \operatorname{ord}_Q(g)\ } \tag{61.1} $$
(61.1) の右辺は定義により $\pi_*\operatorname{div}(g)$ の $P$-係数だから $\operatorname{div}(N(g))=\pi_*\operatorname{div}(g)$。
3. $\operatorname{div}(v-\mu)=[\mu^{-1}(v)]-5P_\infty$((Or))、$\pi_*(5P_\infty)=5[\infty_x]$。以上で (60.1)、零部分で (60.2)。∎

### 1.3 系 `N∞-1:1`(局所 multiplicity 一致) {#N-inf-1to1}

> $Q\in\mu^{-1}(v)$ なら $\mu^\iota(Q)=C/v$。ゆえに
> $$ \boxed{\ \iota Q\in\mu^{-1}(v)\iff v^2=C\ } \tag{60.3} $$
> ($Q=\iota Q$ すなわち $y(Q)=0$ の場合も同じ: $\mu(Q)^2=\mu(Q)\mu^\iota(Q)=C$。**したがって $v^2\ne C$ の fiber に Weierstrass 点は存在しない**。)
> $v^2\ne C$ なら $\pi|_{\mu^{-1}(v)}$ は単射・unramified で、$(v-\mu^\iota)(Q)=(v^2-C)/v\ne0$ ゆえ他因子は単元。よって
> $$ \boxed{\ \operatorname{ord}_{x(Q)}H_v=\operatorname{ord}_Q(v-\mu)\ } \tag{60.4} $$
> したがって multiplicity partition が一致。さらに $v\ne0$ なら $H_v=-2v(a-w)$、$w=(v^2+C)/(2v)$。

### 1.4 命題 `N∞-fix`(fixed fiber の局所構造) {#N-inf-fix}

$v^2=C$ なら fiber 全体で $py=0$、$a(x_0)=v$。$\{py=0\}$ の三場合は exhaustive:

| 場合 | uniformizer | 導出 | 結果 |
|---|---|---|---|
| (i) $y_0=0,\ p(x_0)\ne0$ | $y$ | $\operatorname{ord}_Q(x-x_0)=2$ ゆえ $\operatorname{ord}_Q(a-v)\ge2$、$\operatorname{ord}_Q(py)=1$ | **$e=1$** |
| (ii) $p(x_0)=0,\ y_0\ne0$ | $x-x_0$ | $(a-v)(a+v)=f_6p^2$、$a(x_0)+v=2v\ne0$ ⟹ $\operatorname{ord}(a-v)=2m$;$\operatorname{ord}(py)=m$ | **$e=m:=\operatorname{ord}_{x_0}p$** |
| (iii) $p(x_0)=y_0=0$ | $y$ | $\operatorname{ord}_Q(p)=2m$、$\operatorname{ord}_Q(py)=2m+1$、$\operatorname{ord}_{x_0}(f_6p^2)=2m+1$ ⟹ $\operatorname{ord}_Q(a-v)=4m+2$ | **$e=2m+1$(奇数)** |

**⇒ (iii) から $e=2$ は出ない。**

### 1.5 補題 `N∞-pair`(十分側・**target 非依存**) {#N-inf-pair}

> $k=\bar{\mathbb Q}$ 上で $s^2=-C$ を選ぶ。$C\ne0$・標数 0 ゆえ $s\ne0$ かつ $s^2\ne C$。よって $\pm s$ の二 fiber は **non-fixed** で
> $$ H_{s}=-2s\,a,\qquad H_{-s}=+2s\,a \tag{N-pair-1} $$
> $$ \boxed{\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=\operatorname{rootpart}(a)\ } \tag{N-pair-2} $$

**証明.** (N-1) に $s^2=-C$ を代入して (N-pair-1)。$a(x_0)=0$ なら (Pell) より $p(x_0)^2f_6(x_0)=-C=s^2\ne0$、すなわち **$p(x_0)\ne0$ かつ $f_6(x_0)\ne0$** — 両 fiber は**自動的に非退化 locus**にある。$s^2\ne C$ ゆえ (60.4) が使え multiplicity が一致。∎
**この証明は S5 の target branch condition・`N∞-swap`・branch polynomial の計算を一切使わない。**

### 1.6 補題 `N∞-swap`(必要側) {#N-inf-swap}

> $\deg p=2$・$f_6$ squarefree の下で、**有限 branch fiber が二つとも $[2,2,1]$** かつ **有限 branch pair が $\{s,-s\}$**(系 S5-2a)ならば $\boxed{j(s)=-s,\ s^2=-C}$。

**証明.**
**(0) $j$-stability**: $\mu\circ\iota=C/\mu=j\circ\mu$。$\iota$ は $C_{\rm crv}$ の自己同型ゆえ **ramification locus を保ち**、$j$ は target の Möbius 自己同型ゆえ **branch-value set を保つ**。$j$ は $0,\infty$ を交換するから**有限二値 $\{s,-s\}$ は $j$-stable**。
**(1)** $j$-stable な二値集合は **fixed**($s^2=C$)か **swapped**($s\cdot(-s)=C$ ⟹ $s^2=-C$)。
**(2) fixed の排除**: `N∞-fix` より fixed fiber で $e=2$ が出るのは **(ii) の $m=2$** のみ。$\deg p=2$ ゆえ double root は唯一で、その $x_0$ が与える fixed value $a(x_0)$ も唯一。fixed case は $s$ と $-s$ の**双方**に $e=2$ 点を要求するが、$a(x_0)$ は一方にしかなれない($s\ne0$)。矛盾。∎

### 1.7 補題 `N∞-div` {#N-inf-div}

(Pell) を微分して $2aa'=p(f_6'p+2f_6p')$、$\gcd(a,p)=1$ より **$p\mid a'$**。
$\operatorname{rootpart}(a)=[2,2,1]$ のとき $d:=\operatorname{monic}\gcd(a,a')$ は $\deg d=2$・squarefree、$\gcd(p,d)=1$、$\deg a'=4=\deg p+\deg d$。ゆえに
$$ \boxed{\ a'\doteq p\,d,\qquad a'/p\doteq d\ } \tag{60.5} $$

### 1.8 定理 `N∞-criterion`(iff) {#N-inf-criterion}

> E-1〜E-6 の下で
> $$ \boxed{\ \operatorname{rootpart}(a)=[2,2,1]\iff \begin{array}{c}\operatorname{Br}(\mu)=\{0,s,-s,\infty\}\ \text{for some}\ s\in k\ \text{with}\ s^2=-C,\\ \operatorname{part}\mu^{-1}(s)=\operatorname{part}\mu^{-1}(-s)=[2,2,1]\end{array}\ } \tag{60.6} $$
> **右辺は stage 2 が必要とする branch signature を述べる。monodromy 群そのものの再証明は主張しない。**

**証明.**
**(⇐ 必要方向)** RHS ⟹ 有限 pair は $\{s,-s\}$ で二 fiber とも $[2,2,1]$ ⟹ **`N∞-swap`** ⟹ $s^2=-C$ ⟹ **`N∞-pair`** (N-pair-2) ⟹ $\operatorname{rootpart}(a)=[2,2,1]$。
**(⇒ 十分方向)** $\operatorname{rootpart}(a)=[2,2,1]$ とし $k=\bar{\mathbb Q}$ へ base change。標数 0 ゆえ $\mu$ は separable、$\deg\mu=5$、$g(C_{\rm crv})=2$ で
$$ \deg R_\mu=2g-2+2\deg\mu=12. $$
**(Or)** より $0,\infty$ 上の二点で contribution は $4+4$。**`N∞-pair`** より $s\ne-s$ の各 fiber の contribution は $2+2$。よって既知の四 fiber で $4+4+2+2=12$ を**使い切る**。**different coefficient $e_Q-1$ は非負**なので、$\bar{\mathbb Q}$ にのみ定義される点を含め**他の ramification point は存在できない**。ゆえに $\operatorname{Br}(\mu)=\{0,s,-s,\infty\}$、有限 branch polynomial は degree 2 かつ even。∎
**十分方向は `N∞-swap` の結論を一切仮定していない(循環なし)。**

### 1.9 dependency の型

```text
N∞-pair + RH                                   -> rootpart(a)=[2,2,1] から (60.6) RHS
S5 target(E-7 + two [2,2,1] fibers) + N∞-swap  -> (60.6) RHS
```
**`N∞-swap` の役 = 「S5 target を (60.6) の RHS へ入れる bridge」。** RHS は既に `for some $s^2=-C$` を含むので、**RHS ⟹ LHS の依存閉包では `N∞-swap` は冗長**である(循環はない)。**RHS から $s^2=-C$ を外す案は採らない**(RHS が stage 2 の必要 signature を直接述べる形を保つため)。

---

## 2. 入口契約 / target condition

**raw precondition**: E-1($f_6$ monic squarefree・$\deg f_6=6$)/ E-2($\deg a=5$・$\deg p=2$)/ E-3($a_5=p_2\ne0$)/ E-4((Pell))/ E-5(divisor orientation)/ E-6($\gcd(a,p)=1$)。
**target condition**: E-7(有限 branch 値が調和対 $\{s,-s\}$)。**入口ではない** — **T-1 と定理 `N∞-criterion` が導出**し、T-6 は別経路の cross-check。

**出所 map**: E-1〜E-4 = **S5-3∞**(+便 36 F2.1)/ E-5 = **命題 S5-1**(+S5-3∞ との同値)/ E-7・分岐型 $(5,2^21,2^21,5)$ = **系 S5-2a** / $\lambda=c\mu^2$ = **命題 S5-2**。
**E-6 の身分**: **E-4 + $C\ne0$ から自動**。ゆえに **E-4 exact PASS 後の $\gcd(a,p)\ne1$ は REJECT ではなく `INTEGRITY_STOP`**(§5.3)。

---

## 3. 述語(decision lane / audit lane)

```text
decision lane: E-1..E-6 + T-1 (rootpart(a) = [2,2,1])
audit lane A : local differential -> R on C -> mu_* R           (searcher)
audit lane B : proven-baseline saturated elimination            (checker)
```
**T-1**: $\deg\gcd(a,a')=2$・$\gcd(a,a')$ squarefree・$\deg\gcd(a,a',a'')=0$。
**T-2**((60.5) 逐語)/ **T-3** $p$-locus / **T-4** Weierstrass locus / **T-5** 二 infinity($e=5$)/ **T-6** harmonic(sealed)/ **T-7** RH 12・有限 branch count 2・extra 0 / **T-8** 両 lane の finite aggregate partitions 比較。
**T-1 通過後の不一致はすべて `INTEGRITY_STOP`**(`N∞-criterion` が target signature を強制するため)。
**二次因子の `while` 全除去は禁止。** searcher は resultant を使わない。checker は baseline multiplicity と saturation の proof ID を束縛する。

---

## 4. divisor equality certificate(D-2)

> **★ 独立性は名前ではなく運用条項が担保する**(便 61 F9): **D-1 でも二 lane が仕様だけを共有して canonicalizer を独立実装すれば単一 shared implementation にはならない**し、**D-2 でも単一 generator/verifier を両 lane が oracle として信じればそれが共通 bug 経路になる**。

### 4.1 schema {#cert-schema}

```text
divisor_equality_certificate = {
  schema_id, schema_digest, predicate_spec_id, predicate_spec_digest, candidate_ref,

  # --- 曲線とチャート ---
  curve_model_digest, chart_ids,

  # --- ambient algebra(B62-1)---
  ambient_coordinate_ring_schema_id  + digest    # ring と quotient relations
  ambient_quotient_relations                     # 明示(例: y^2 - f6(x))
  coefficient_field_presentation_id  + digest
  field_embedding_witness_schema_id  + digest
  monomial_order_id                  + digest
  groebner_reduction_contract_id     + digest    # normal form / reduction の規約

  # --- 各 lane の native(二対象)---
  searcher_native = { ramification_divisor_on_C_ref, branch_divisor_on_P1_ref,
                      native_schema_id + digest, native_artifact_digest }
  checker_native  = { ramification_divisor_on_C_ref, branch_divisor_on_P1_ref,
                      native_schema_id + digest, native_artifact_digest }

  # --- witness 群 ---
  component_bijection,
  exact_point_equality_witnesses,               # §4.2 kind = ideal-equality のみ
  distinctness_witnesses,                       # §4.2 kind = disjointness【chg v7 新設】
  multiplicity_equalities,
  chart_overlap_witnesses,
  total_coverage_and_no_extra_component_witness,
  pushforward_compatibility_witness,

  # --- 独立性証跡はここに置かない(§4.4 で定義・§5.2 に並列格納)---
}
```

> **【chg v11・erratum J】certificate は独立性証跡を内包しない。** §4.4 の `independence_evidence` は **`SEALED_INTERNAL` において certificate と並列に置かれる別オブジェクト**である(§5.2)。**v10 までの schema 末尾にあった `verifier_evidence` はどこにも定義されておらず、verifier contract もそれを検査していなかった**(内部前哨ゲート FINDING-2・**自認**)。**欄を削除し、重複を作らずに §4.4 / §5.2 の並列構成へ一本化する。**

### 4.2 `exact_point_equality_witnesses` の型【B62-1】 {#witness-type}

> **⚠ v6 の数学的型誤り(erratum E1・自認)**: v6 は `Bézout / reduction certificate`($1=\sum u_ig_i$)を **witness のメニューに未型付けで並べていた**。**$1\in I_1+I_2$ は $V(I_1)\cap V(I_2)=\varnothing$、すなわち二つの点が「交わらない」ことの certificate であって、「等しい」ことの certificate ではない。**
> **最小反例(独立に検算)**: $R=\mathbb Q[x]$, $I_0=(x)$, $I_1=(x-1)$。$1=1\cdot x+(-1)\cdot(x-1)$ ゆえ v6 の Bézout 分岐は PASS を出す。一方 ideal membership の正しい判定は $x \bmod (x-1)=1\ne0$、$(x-1)\bmod (x)=-1\ne0$ で**両方向とも不成立** — 二点は等しくない。**v6 の記述は「異なる点」を「同じ点」として component bijection へ流し、witness 群全体の false positive を許していた。**
>
> **reduced Gröbner basis は ring と term order を固定して初めて一意になる。** ゆえに §4.1 の **`ambient_coordinate_ring_schema_id` + `ambient_quotient_relations` + `monomial_order_id` + `groebner_reduction_contract_id`** を**証明書から再検査できる形で束縛**したうえで、**witness を次の 2 種に型分けする**。
>
> - **`kind = ideal-equality`(点同一性 witness の唯一の形式)**: $I_1\subseteq I_2$ と $I_2\subseteq I_1$ を、**固定 monomial order の reduced Gröbner basis に対する明示の表現係数**、または**各生成元の `reduction-to-zero` 列**で。
> - **`kind = disjointness`(別 witness 型)**: $1\in I_1+I_2$ の Bézout certificate。**component bijection の単射性と余剰排除にのみ使い、点同一性の PASS には使わない。**
>
> **すべての reduction certificate は `reduction-to-zero` / `reduction-to-one` の tag を持たねばならない。** tag 無しは FAIL(「各生成元が相手 ideal で $0$ に reduce する」のか「$1$ を得る」のかを区別しない certificate は、どちらの主張の証明にもならない)。
> **異なる presentation の係数体を跨ぐ場合は `field_embedding_witness` を添える。**
> **⛔ 拒否**: **Bézout $1=\sum u_ig_i$ を点同一性の根拠とすること**・tag の無い reduction certificate・単なる digest 一致・最終 partition 一致・degree 一致。
>
> **数学的注記(型の限定)**: 一般には **disjointness $\Rightarrow$ distinctness** であって逆は成り立たない。**本設定では両 native の component は $C_{\rm crv}$ 上および $\mathbb P^1$ 上の閉点であり、support は 0 次元 reduced** なので、**相異なる閉点は交わらず、この設定に限り両者は同値**である。**多重度は disjointness witness ではなく `multiplicity_equalities` が扱う** — `disjointness` に用いる ideal は**点の ideal(radical)**であり、非被約構造を持ち込まない。
>
> **手続き的具体化**: **verifier contract §3.1・§3.1.2**(W-2 / W-2′)。**本節と verifier contract は同じ型分けを述べる**【chg v10 で版中立化】。

### 4.3 運用条項 {#operational-clauses}

| # | 条項 |
|---|---|
| **G-1** | generator は**第三の判定 lane に数えない。単独で ACCEPT を出せない。** 両 native output から witness を作るだけ。 |
| **G-2** | **【chg v6・便 63 F9.3 で routing 分割】** 同一 event に二 code が割り当たらないよう次で分ける。**入力 / native / certificate の digest 不一致 → `digest-mismatch`[12]** / **equality witness の欠落・不成立 → `divisor-equality-failure`[25]**。いずれも `INTEGRITY_STOP`。 |
| **G-3** | **A/B が独立 verifier で同じ certificate を検査する。単一 verifier を両 lane が oracle として信じることを禁止。** |
| **G-4** | **shared canonicalizer / math helper の再導入禁止** — 判定は §4.4 の**推移的依存閉包**で行う。generator が canonicalizer を内包しても、**両 verifier は witness を独立に再検査**する。 |
| **G-5** | §4.4 の independence evidence を freeze bundle に束縛。 |
> **[historical] G-2**: 自認**(v5 の G-2 は digest 不一致を後者へ送っていた)。


### 4.4 independence evidence schema【B63-1・便 63 F8】 {#independence-evidence}

```text
independence_evidence = {
  generator_id  + code_digest + build_root_id + toolchain_id,
  verifier_A_id + code_digest + result_digest + build_root_id + toolchain_id
                + implementation_provenance,
  verifier_B_id + code_digest + result_digest + build_root_id + toolchain_id
                + implementation_provenance,

  dependency_manifest_schema_id + digest,     # manifest の型そのものを束縛
  dependency_closure_A[] = transitive content digests,   # 推移的閉包(直接依存のみは不可)
  dependency_closure_B[] = transitive content digests,

  allowed_shared_tcb[] = frozen content digests + role,  # 共有を許す trusted base
  forbidden_shared_math_helper_intersection
      = (dependency_closure_A ∩ dependency_closure_B) - allowed_shared_tcb
      = empty,

  verifier_contract_id + digest
}
```

| # | 条文 |
|---|---|
| **H-1** | **manifest は直接依存では不可。`dependency_closure_*` は推移的閉包の content digest 集合である。** |
| **H-2** | **同一性は content digest で判定する** — 別名・別 path・薄い wrapper は**同一 content digest を含む閉包**として現れるため区別されない。**path 改名を独立二実装と数える事故を防ぐため `build_root_id` / `toolchain_id` / `implementation_provenance` を receipt に残す。** |
| **H-3** | **`allowed_shared_tcb[]` は共有を許す trusted base を列挙する**(標準 runtime・schema parser・hash primitive 等)。**各項に `role` を付し、frozen content digest で固定する。** **数学的内容を持つ helper(canonicalizer・ideal 演算・divisor 正規化・partition 計算)を TCB に入れることを禁止。** |
| **H-4** | **交差の値は producer の自己申告を信じない。receipt 受領側が canonical content digest 集合から導出して再計算する。** 非空なら `INTEGRITY_STOP / shared-helper-detected`[11]。 |
| **H-5** | **`allowed_shared_tcb[]` への追加は挙証責任を追加側に置く**(freeze bundle の変更として receipt が要る)。 |

> **⚠ v5 の欠陥(自認)**: `shared_helper_intersection = ∅` だけでは、**閉包の深さ・同一性判定・helper の範囲・許される TCB** が未定義。文字どおり「全 helper」なら標準 runtime の共有で交差は通常空にならず、暗黙にそれらを除けば**共通 canonicalizer を除外した証拠にならない**(便 63 F8)。**空集合検査は必要な一部でしかなかった。**

---

## 5. certificate と verdict / reason

### 5.1 public envelope {#public-envelope}
```text
public_envelope = {
  candidate_ref,                    # random opaque
  predicate_spec_id, predicate_spec_digest,
  searcher_id + digest, checker_id + digest,
  verdict,
  primary_reason_code,              # 単数・全域(従来どおり)
  secondary_reason_codes[],         # canonical 昇順・primary を含まない【chg v8 新設・§5.4.1】
  finite_branch_count, finite_branch_pair_harmonic, a_root_partition,
  exceptional_locus_clear, ramification_sum       # 数学的射影 5 欄
}
```

### 5.2 `SEALED_INTERNAL` {#sealed-envelope}
```text
tuple_coefficients
searcher_native = { ramification_divisor_on_C, branch_divisor_on_P1,
                    finite_aggregate_partitions, native_artifact_digest }
checker_native  = { ramification_divisor_on_C, branch_divisor_on_P1,
                    finite_aggregate_partitions, native_artifact_digest }
divisor_equality_certificate, independence_evidence, partition_equality_result
all_reason_codes[]                      # canonical 整列(§5.3)・semantic ∪ concordance の全 code(§5.4.1 P-S7)
fibers[], fiber_refs[], branch_values, finite_branch_polynomial
artifact_digests
commitment = { hmac_of_tuple, key_holder="clean HMAC steward",
               reveal_after="Freeze 2" }
```
**⛔ 片側を他側の parser / canonicalizer で変換してから保存することを禁止。**

### 5.3 verdict state machine【B63-2・便 63 F9】 {#verdict-state-machine}

> **verdict の決定と reason の priority を分離する。** v5 は「全順序の最小」を public primary としたため、**`precondition/degree-mismatch`[1] と `sealed-field-leak`[9] の同時検出で REJECT[1] が選ばれ証拠汚染を隠す**(設計理由と逆転)。**自認。**

```text
# --- 検出順序: envelope-level check を early REJECT より先に実行 ---
step 1: envelope-level leak / digest / dependency checks   -> I に加算
step 2: mathematical precondition + T-1                    -> R に加算
step 3: cross-lane checks                                  -> I に加算

I = detected integrity reasons          # 18 段(§5.3.2)
R = detected mathematical reject reasons #  8 段(§5.3.1)

if I != empty:
    verdict          = INTEGRITY_STOP
    primary          = minimum(I, integrity_priority)
    all_reason_codes = canonical_sort(I ∪ R)
elif R != empty:
    verdict          = REJECT
    primary          = minimum(R, reject_priority)
    all_reason_codes = canonical_sort(R)
else:
    verdict          = ACCEPT
    primary          = accepted
    all_reason_codes = [accepted]

invariant 1: accepted appears iff I = R = empty      # accepted は他 code と排他
invariant 2: 【chg v9 erratum D で更新】
             primary_reason_code は単数・全域。
             public reason は primary と
                 canonical_sort( ({[26]} ∩ I) - {primary} )
             のみ。すなわち public secondary は concordance 軸の code に限る(§5.4.1 P-S3)。
             semantic 軸の非 primary code は sealed にのみ置く。
invariant 3: sealed は canonical 整列した all_reason_codes[] を保つ
invariant 4: 同一入力に対し (verdict, primary_reason_code) は一意
invariant 5: 同一入力に対し secondary_reason_codes[] も一意(invariant 2 の式が決定的)
```

#### 5.3.1 `reject_priority`(**8 段**・decision lane のみ)
```text
[1] precondition/degree-mismatch
[2] precondition/f6-not-monic
[3] precondition/curve-not-squarefree
[4] precondition/leading-coeff-mismatch
[5] precondition/pell-violation
[6] precondition/divisor-orientation
[7] triple-root-of-a          # deg gcd(a,a',a'')>0 または gcd(a,a') 非 squarefree
[8] a-partition-mismatch      # それ以外の T-1 失敗
```

#### 5.3.2 `integrity_priority`(**18 段** — $26-9+1=18$)
```text
[ 9] sealed-field-leak                 # 証拠そのものが信用できない類(最優先)
[10] deterministic-digest-exposed
[11] shared-helper-detected            # §4.4 H-4
[12] digest-mismatch                   # 入力/native/certificate の digest 不一致(G-2)
[13] pell-implies-coprime-mismatch     # 定理が強制する恒等式の破れ
[14] divisor-identity                  # (Or) の破れ
[15] pell-derivative-mismatch          # (60.5)
[16] chart-degree-mismatch             # chart / locus の未処理
[17] p-locus-unhandled
[18] weierstrass-unhandled
[19] infinity-unhandled
[20] rh-mismatch                       # 大域整合
[21] extra-branch-value
[22] finite-branch-count-mismatch
[23] branch-pair-not-harmonic
[24] finite-partition-cross-mismatch
[25] divisor-equality-failure          # 二経路照合(witness 欠落・不成立: G-2)
[26] verifier-result-mismatch  # 同一入力に対する A/B verifier result の不一致【chg v7 改名】
```
> **段数**: `[9]`–`[26]` で $26-9+1=18$。**v5 の「16 段」は表題 typo。自認。**
> **設計理由**: 証拠不信 [9]–[12] → 定理強制恒等式の破れ [13]–[15] → chart/locus 未処理 [16]–[19] → 大域整合 [20]–[24] → 二経路照合 [25]–[26](**[25]/[26] の述語と二軸 routing は §5.3.3**)。
> **検証例**: `degree-mismatch`[1] + `sealed-field-leak`[9] 同時 ⟹ $I\ne\varnothing$ ゆえ **verdict = INTEGRITY_STOP, primary = [9]**(v5 の規則は誤って [1] を選んでいた)。`pell-derivative-mismatch`[15] + `divisor-equality-failure`[25] 同時 ⟹ **primary = [15]**(便 63 F9.2 の期待どおり)。

#### 5.3.3 二軸 routing — semantic 軸と concordance 軸【chg v8・erratum B】{#two-axis}

> **v7 の欠陥(自認)**: v7 §5.3.3 は step 1〜4 を「前段が reason を発したら停止」とした。**同じ原因の二重分類を防ぐには正しかったが、別原因として同時に起きた verifier disagreement まで消していた。**
> - **F4.1**: native partition mismatch `[24]` があり、同時に `verifier A: vector = PASS` / `verifier B: vector = FAIL` の場合、step 2 停止で **`[26]` が発せられない**。**`[24]` は native data の不一致、`[26]` は verifier 実装の不一致であり、同じ event の別名ではない。** 後者を隠すと**二実装監査が検出すべき common/individual bug の証跡**を public reason から落とす。
> - **F4.2**: `A: W-2 FAIL, W-3 PASS` / `B: W-2 PASS, W-3 FAIL` は**両者の overall verdict が FAIL でも per-witness result vector は不一致**。v7 の step 3 は「A と B がともに欠落・不成立を確認」と読めて **`[25]` を発し step 4 へ行かない** — **enum 名 `verifier-result-mismatch` と一致しない。**

**二軸 routing(便 66 F13 の発案を採用・**verifier contract §5.1** X-1〜X-6 と同期・版束縛は §6 pin)**:

```text
# --- semantic axis(軸内は排他・上から評価し reason を発した段で停止)---
S1  envelope-level: leak / digest / dependency checks       -> [9]..[12]
S2  native cross-check: 両 native への specific な数学的検査  -> [13]..[24]
      (divisor identity, pell-derivative, chart/locus, RH,
       branch count, harmonicity, finite partition の突合)
S3  witness validity                                        -> [25]

# --- concordance axis(独立・入力 digest が一致する限り常に評価)---
C1  R_A vs R_B    # canonical per-witness result vector      -> [26]

# --- 合成 ---
if R_A != R_B:
    concordance_reasons = { [26] }
elif S2 の native reason が空 かつ (R_A = R_B) が witness failure を含む:
    semantic_reasons |= { [25] }

I       = semantic_reasons | concordance_reasons
verdict = INTEGRITY_STOP   (I != empty のとき)
primary = minimum(I, integrity_priority)          # 単数性は維持
```

| 段 | 述語 | 軸 |
|---|---|---|
| **[24]** | 両 native の finite aggregate partition が異なる | semantic S2 |
| **[25]** | **native の一致が S2 で確認された下で**、$R_A=R_B$ が witness の欠落・不成立を含む | semantic S3 |
| **[26]** | **同一 certificate・同一 native inputs に対する canonical per-witness result vector の不一致** $R_A\ne R_B$ | **concordance C1** |

| # | 条項 |
|---|---|
| **X-1** | **semantic axis は軸内で排他。** [9]–[12] / [13]–[24] / [25] は同時に立たない。 |
| **X-2** | **[25] は「native の一致が S2 で確認された下で $R_A=R_B$ が witness failure を含む」に限定される。** |
| **X-3** | **[26] は concordance axis に属し、semantic reason と共存する。** [13]–[24] と同時に検出してよい。「native 不一致を [26] に予約する」案は**不採用**(便 65 F5)。 |
| **X-4** | **[25] と [26] は相互排他**($R_A=R_B$ が [25] の前提、$R_A\ne R_B$ が [26] の前提)。 |
| **X-5** | **S2 で停止した場合も witness 検証と concordance 比較は実行する。 |
| **X-6** | **[26] の述語は「overall verdict の不一致」ではなく「canonical per-witness result vector $R_A\ne R_B$」**(**verifier contract §3.4** R-1)。**vector は `ABSENT` と `FAIL` を区別する**(verifier contract §3.4 R-2)。overall verdict の不一致に限定するなら enum 名を `verifier-verdict-mismatch` とすべきだが、**本仕様は vector 比較を採る**(便 66 F4.2)。 |
> **[historical] X-5**: semantic の後段 reason は発しないが、**concordance の [26] は発する** — これが v7 との違い。


> **state machine は変わらない。** 二軸化は $I$ の**作り方**を「排他的な単一 code」から「semantic $\cup$ concordance」へ広げるだけで、**§5.3 の `primary = minimum(I, integrity_priority)`・`accepted iff I = R = ∅` はそのまま成立する。**
> **【chg v9 erratum D で訂正】invariant 1・3・4 は不変。invariant 2 は v9 で更新した**(v8 は「invariant 1–4 はそのまま成立する」と書きながら **invariant 2 が public secondary を禁止したままだった** — **自認**)。**invariant 5 を新設**して secondary の一意性も明示する。

### 5.4.1 `secondary_reason_codes[]`(public)【chg v8・erratum B】{#secondary}

| # | 条項 |
|---|---|
| **P-S1** | **`primary_reason_code` の単数性は維持する。** `secondary_reason_codes[]` は primary を**含まない**。 |
| **P-S2** | **canonical 昇順に整列**する(producer の順序に依存しない)。 |
| **P-S3** | **【漏洩最小化】public の secondary は concordance axis の code に限る**(現行 enum では **[26] のみ**)。**semantic axis の非 primary code は sealed の `all_reason_codes[]` にのみ置く。** |
| **P-S4** | **P-S3 の理由**: public envelope の情報量が増えるほど、**小さい探索宇宙では reason の組合せが指紋になり得る**(便 59 F11.3 の deterministic digest と同型のリスク)。**便 66 F4.1 が要求するのは「verifier disagreement が public から消えないこと」**であり、それは **1 ビット**([26] の有無)で満たせる。**semantic の全 code を public へ出す必要はない。** |
| **P-S5** | ゆえに **[24] と [26] の同時成立**では `primary = [24]`(priority 最小)・`secondary = [[26]]` となり、**両方が public に可視**である(F4.1 の要求を満たす)。 |
| **P-S6** | 空のときは**空配列を明示**する(欄の欠落と区別する)。 |
| **P-S7** | **sealed の `all_reason_codes[]` は従来どおり $I\cup R$ の全 code を canonical 整列で保持する**(invariant 3 不変)。**public secondary はその真部分集合であって、sealed の代替ではない。** |

---

## 6. freeze bundle(**full-blob anchor 方式**)【B63-3・便 63 F10.3・裁定 75】 {#freeze-bundle}

> **section digest を全廃する。** 便 63 F10.1 のとおり `sha256(§x.y 本文)` は計算式であって literal hex でなく、**heading 行を含むか・次 heading 直前の空行や `---` を含むか・改行正規化をするか**が未定義なら**同じ blob から複数の正当な値**が出る(Sol が v3 §1.1 を自然な規約で再計算して `27252221b02abfcd` を得、記録値 `d7ee78c460bfec6e` と一致しなかったのがその実例)。**byte-range 抽出規約を凍結するより、全 fragment を full-blob digest へ anchor する方が小さく fail-closed。**

```text
predicate_spec_id     = "mb/ninfty-stage2-predicate/v12"
predicate_spec_digest = <64 hex: 本稿 exact blob の sha256 — 発行時に司令塔が記入>
encoding              = UTF-8, LF, no BOM, no normalization

# --- 定理群: ID は anchor 名のみ・digest は full blob 一本 ---
lemma_id( N-inf-N )           = predicate_spec_id + "#N-inf-N"
lemma_id( N-inf-1to1 )        = predicate_spec_id + "#N-inf-1to1"
lemma_id( N-inf-fix )         = predicate_spec_id + "#N-inf-fix"
lemma_id( N-inf-pair )        = predicate_spec_id + "#N-inf-pair"
lemma_id( N-inf-swap )        = predicate_spec_id + "#N-inf-swap"     # role: S5 target -> (60.6) RHS bridge
lemma_id( N-inf-div )         = predicate_spec_id + "#N-inf-div"
theorem_id( N-inf-criterion ) = predicate_spec_id + "#N-inf-criterion"
  dependency_closure = { #N-inf-N, #N-inf-1to1, #N-inf-fix,
                         #N-inf-pair, #N-inf-swap, #N-inf-div }
bound_blob_digest(all of the above) = predicate_spec_digest

# --- 実装契約(§4.4 が要求する欄の実体)【chg v8 erratum C・forward reference を消すため先に置く】---
verifier_contract_id     = "mb/ninfty-verifier-contract/v7"
verifier_contract_digest = d863bd7a018c2c5c3bfc1d74fde5b9c538d4954dcfa06abf6094188f3056465a
dependency_manifest_schema_id     = "mb/dependency-manifest/v7"
dependency_manifest_schema_digest = 9bdd91604559cebae270efbb420324a320190f875fd2948e4e69df4b9c966673

# --- schema 群 (i) spec 内部 anchor: bound blob = spec 自身 ---
schema_id( cert )              = predicate_spec_id + "#cert-schema"
schema_id( witness-type )      = predicate_spec_id + "#witness-type"
schema_id( operational )       = predicate_spec_id + "#operational-clauses"
schema_id( independence )      = predicate_spec_id + "#independence-evidence"
schema_id( public-envelope )   = predicate_spec_id + "#public-envelope"
schema_id( sealed-envelope )   = predicate_spec_id + "#sealed-envelope"
schema_id( verdict-machine )   = predicate_spec_id + "#verdict-state-machine"
schema_id( two-axis )          = predicate_spec_id + "#two-axis"            # v8 erratum B
schema_id( secondary )         = predicate_spec_id + "#secondary"           # v8 erratum B
schema_id( witness-kinds )     = predicate_spec_id + "#witness-type"        # v7 erratum E1
bound_blob_digest(cert .. witness-kinds) = predicate_spec_digest

# --- schema 群 (ii) external anchor: bound blob = 実体側の artifact 【chg v8 erratum A】---
schema_id( input-separation )       = dependency_manifest_schema_id + "#input-separation"
bound_blob_digest( input-separation ) = dependency_manifest_schema_digest
schema_id( result-vector )          = verifier_contract_id + "#result-vector"
bound_blob_digest( result-vector )    = verifier_contract_digest
schema_id( derivation-rules )       = dependency_manifest_schema_id + "#derivation"
bound_blob_digest( derivation-rules ) = dependency_manifest_schema_digest

# --- hash 順序(便 66 F11・非循環)---
hash_order = manifest -> contract -> spec -> receipt
#   manifest/contract は spec digest を pin しない(governing spec は ID 束縛・digest は receipt)
#   spec は contract/manifest の exact digest を pin する
#   spec 自己 digest と contract の governing_spec_digest は receipt 側

# --- 外部 dependency: 自分の段落ではなく source artifact を束縛(F10.2)---
external_dependency[] = [
  { id = "S5/S5-4-infinity", digest = <64 hex of S5 source artifact> },
  { id = "S5/S5-3-infinity", digest = <64 hex of S5 source artifact> },
  { id = "S5/prop-S5-1",     digest = <64 hex of S5 source artifact> },
  { id = "S5/prop-S5-2",     digest = <64 hex of S5 source artifact> },
  { id = "S5/cor-S5-2a",     digest = <64 hex of S5 source artifact> }
]

# --- campaign / field 型(statement ではなく型宣言として保持)---
campaign_window_id              = K5
curve_coefficient_base_field_id = Q
geometric_working_field_id      = Qbar
prediction_base_field_id        = Q(zeta_20)
```
> **⚠ v5 の欠陥(自認)**: (i) digest が**計算式**で literal hex でなく、**境界規約が文書にも再現 script にも無かった**(後から値を選べる) — 便 63 F10.1。(ii) `squareclass_quotient_schema_id = "K^x / (K^x)^2"` 等は **versioned artifact ID ではなく statement の説明**で、`s5_4_infinity_dependency_id` の digest を **v5 §7 本文へ向けていた**(外部 dependency の identity を束縛せず、「依存すると書いた自分の段落」を束縛するだけ) — 便 63 F10.2。(iii) §4.4 が要求する `verifier_contract_id/digest` が §6 に無かった。**v6 は (i) を full-blob anchor で、(ii) を `external_dependency[]` で、(iii) を実装契約欄で閉じる。**
> **⚠ v7 の欠陥(自認・erratum A)**: v7 §6 は `schema_id(input-separation)` を **manifest の anchor** としながら、`bound_blob_digest(all of the above) = predicate_spec_digest` で**一括して spec 自身の digest に束ねていた**。**`input-separation` の実体は manifest §5.3 なので bound blob は manifest digest でなければならない。****full-blob anchor が正しい source blob を指さない以上、literal hash が揃っていても freeze binding は偽である**(便 66 F8)。**v8 は内部 anchor と external anchor を分離し、後者を実体側の artifact digest に束ねる。** 併せて **`dependency_manifest_schema_id/digest` の定義を先に置いて forward reference を消した。**
> **空欄の身分**: `<...— 発行時に記入>` は **freeze receipt 側で埋める欄**であり、本稿の blob には入らない(§0.0 の lifecycle 分離と同じ理由)。

---

## 7. whitelist / fixtures / EP / 役割分離

- **whitelist**: `branch_value_square -> squareclass(C) -> P1`。**型は §6 の field 欄が固定**($K=\mathbb Q(\zeta_{20})$・$i=\zeta_{20}^5$ ゆえ $-1=i^2\in K^{\times2}$ で $[s^2]=[C]$)。`aliases_blocked` は**非網羅列挙**で、新出力量を足す側に**挙証責任**。**deterministic commitment も同じ規則の対象。**
- **negative fixtures**: `ninfty-neg-01..08`、期待 `REJECT / triple-root-of-a`・`a_root_partition=[3,1,1]`・`triple_gcd_degree>0`・`gcd_squarefree=false` の **4 欄回帰**。**raw shard 名・命名パターン・digest は本稿に書かない**(sealed mapping)。**証拠の射程は `source-audited candidate`。**
- **EP**: same degree/schema・non-campaign coefficients。**EP 不在中は `partial predicate / UNKNOWN`。freeze 後も `calibrated detector` / `complete search` と呼ばない。**
- **役割分離**: **negative-lane runner $\ne$ clean HMAC steward。旧 mapping を知る tainted actor は steward 不可**(taint ledger の別欄 + 機械検査)。

---

## 8. Sol への監査依頼(v11 — **修理の 2 点に限る**)

1. **【必須】§4.4 の推移的閉包形**が便 63 F8 の 4 未定義項(閉包の深さ / 別名・wrapper の同一性 / helper の範囲 / 許される TCB)を閉じているか。とくに **H-3(数学的内容を持つ helper を TCB に入れない)** の線引きで足りるか。
2. **【必須】§5.3 の verdict state machine**が便 63 F9 の要求(verdict と priority の分離・`primary = minimum(I, integrity_priority)`・`accepted` 排他・envelope check を early REJECT より先)を満たすか。**二つの検証例の primary が期待どおりか。**
3. **【必須】§6 の full-blob anchor 方式**が便 63 F10.3 の最小形か。**`external_dependency[]` の digest 欄を「発行時に記入」で空にしたまま候補を提示する**運用でよいか(埋めれば blob digest が変わるため)。
4. **【必須】§0.0 の lifecycle 分離**が A62-2 と同型の修理として十分か。**§9 の時制付けで足りるか。**
5. **【推奨】§4.3 G-2 の routing 分割**(digest 不一致 → [12] / witness 欠落・不成立 → [25])が同一 event の二重割当を解消しているか。他に二重割当が残っていないか。
6. **【推奨】§1 の数学核**は 【chg v5】 以来不変(便 62 F7.1 の型修理を含む)。**再監査不要と扱ってよいか。**

**【chg v7 の追加依頼 — erratum の 2 点】**
7. **【必須】§4.2 の 2 kind 型分け**が便 65 F4 の要求を満たすか。とくに **`disjointness` の使い所を単射性と余剰排除に限定**し、**0 次元 reduced ゆえ本設定では distinctness と同値**とした注記の射程。**radical ideal を使い多重度を分離**した扱いでよいか。
8. **【必須】§5.3.3 の [25]/[26] 述語と評価順序**が便 65 F5 の最小排他案と一致するか。**[24]/[25]/[26] が相互排他になっているか。**
9. **【推奨】改名 `verifier-result-mismatch`** で spec と contract の語彙が同期したか。

**【chg v8 の追加依頼 — erratum の 3 点】**
10. **【必須・A】§6 の内部 anchor / external anchor の分離**が便 66 F8 の正形か。**`result-vector` を contract digest に、`input-separation`・`derivation-rules` を manifest digest に束ねた**割当でよいか。**forward reference は消えたか。**
11. **【必須・B】§5.3.3 の二軸 routing**が便 66 F4・F13 の要求を満たすか。**X-5(S2 停止時も concordance は発する)**と **X-6(vector 比較・`ABSENT` と `FAIL` の区別)**が F4.1・F4.2 の二例を正しく捌くか。
12. **【必須・B】§5.4.1 P-S3 の限定**(public secondary を concordance axis に限る)。**F4.1 の要求は 1 ビットで満たせる**という判断と、**F13 の「public は primary 一個」という設計**の折り合いとして妥当か。**semantic の全 code を public に出す方が良いなら P-S3 を差し替える。**
13. **【必須・C】§6 の pin と hash 順序 manifest → contract → spec → receipt** が非循環か。**manifest/contract 側が spec digest を pin せず ID 束縛にとどめた**片方向 topology でよいか。

**【chg v9 の追加依頼 — erratum の 3 点】**
14. **【必須・D】invariant 2 の置換**が便 67 F6 の最小修理形か。**`canonical_sort( ({[26]} ∩ I) - {primary} )`** という式で **[24]+[26] の例が一意に決まる**か。**invariant 5(secondary の一意性)**の新設は妥当か。
15. **【必須・E】§9 の実装ゲート**が「exact freeze bundle の三 digest に対する Sol PASS + receipt」になったか。**旧版起点の live 残存が無いか**(私の sweep では 0)。
16. **【必須・F】contract / manifest の pin**。**manifest で family を audit flag へ降格し build face を normative に昇格した判断**(manifest §6 注記 N-1 に「三面が旧 I-3c を包含する」証明を付した)を、**spec 側から見て承認できるか。**

**【chg v10 の追加依頼 — 同期の 3 点】**
17. **【必須・G】live 参照の版中立化**が便 68 F6.1 を閉じたか。**operative 本文から版 token を除き、版束縛を §6 pin と §10 block の 2 箇所に集約**した設計でよいか。
18. **【必須・H】contract / manifest の pin と §9 の三 ID/digest**。**hash 順序 manifest → contract → spec → receipt** は不変。
19. **【必須・I】§10 の `live_authority_refs[]` / `historical_quotation_refs[]`**(F13.1)。**LA-3 の sweep 対象定義(自版 + 他 2 文書の全版 token)**が、前便の失敗型(自版だけ見る sweep)を閉じているか。

**【chg v11 の追加依頼 — 内部前哨ゲート起点の 2 点】**
21. **【必須・J】§4.1 からの `verifier_evidence` 削除**。**独立性証跡を certificate の欄にせず §4.4 定義 + §5.2 並列格納に一本化**した最小修理でよいか。**certificate 内に独立性証跡への参照(digest 等)を置くべきか、置かない方が良いか。**
22. **【必須・K】dependency manifest の FINDING-1 修理**(D-4′ を record ごとの自己束縛へ・「相互照合」撤回・SB-5 の `build_record_present` 明示宣言・SB-6 の I-3d との棲み分け)。**この設計で entry 粒度の substitution 反例が閉じているか。** **build record を持たない entry の宣言義務が抜け穴を塞いでいるか。**
20. **【推奨】dependency manifest §2.4 の `subject_build_binding_digest`(SB-1〜SB-4)と §2.5 の `build_attestation`(BA-1〜BA-5)の二層分離**を、spec 側の依存として承認できるか。**identity binding は取り違え防止まで・実生成関係は attestation 提出時のみ主張可・未実施なら `UNKNOWN`** という効力宣言でよいか。



---

## 9. 実装着手の条件(**時制付き**)【B63-4】

> **receipt 前**: 実装着手は**禁止**。searcher / checker / D-2 generator / 二 verifier のいずれについても、コードを書き始めてはならない。**model builder は LOCKED。**
> **approved receipt 後**: **その receipt が明示した scope に限って**認可される。scope 外(model builder の解錠・新しい lane の追加・`allowed_shared_tcb[]` の拡張)は**別の receipt を要する**。

> **⚠ v8 の欠陥(自認・erratum E)**: v8 §9 は **current implementation condition** でありながら起点を **「v6 の Sol 監査 PASS」**としていた。**これは historical quotation ではない。** v6 は E1・E2・A・B・C の erratum 前であり、**その audit PASS は現 exact bundle の freeze PASS の代用にならない**(便 67 F8)。
> **§0.0 の `live_status_authority` により receipt 自体を省略できないので即時実装を許す穴ではないが、起点の版が古いまま live だったこと自体が、便 66 F7 で contract / manifest の live v6 参照を blocker とした基準に反する。**

**現行の実装ゲート(v9)**:

```text
exact_freeze_bundle = {
  predicate_spec_id     = "mb/ninfty-stage2-predicate/v12",    predicate_spec_digest,
  verifier_contract_id  = "mb/ninfty-verifier-contract/v7",    verifier_contract_digest,
  dependency_manifest_schema_id = "mb/dependency-manifest/v7",  dependency_manifest_schema_digest
}

gate = Sol freeze PASS on exact_freeze_bundle(三 digest すべて)
     + commander receipt がその digest 群を束縛
     -> receipt の scope 内でのみ実装
```

$$ \boxed{\ \text{本 exact bundle(三 digest)の Sol freeze PASS}\ +\ \text{digest 群を束縛した commander receipt}\ \to\ \text{receipt の scope 内で searcher / checker / generator / 二 verifier を}\ \textbf{別々に}\ \text{実装}\ } $$

- **三 digest のいずれか一つでも変われば、gate は再取得を要する**(部分的な差し替えを認めない)。
- **本 bundle の三 digest と一致しない版に対する audit 結果は、この gate を満たさない。**

- **D-2 generator は判定 lane に数えない。二 verifier は独立実装で、§4.4 の禁止交差が空。**
- **EP が揃うまで札は `partial predicate / UNKNOWN`。**
- **旧 8 hit は neutral lane でのみ使う。runner ≠ clean HMAC steward。**

---

## 10. live authority refs(機械可読)【F13.1・裁定 83】{#live-authority}

```text
live_authority_refs[] = [
  { artifact_id: "mb/ninfty-verifier-contract/v7",
    digest_or_receipt_slot: "d863bd7a018c2c5c3bfc1d74fde5b9c538d4954dcfa06abf6094188f3056465a",
    anchor: "§3.1 / §3.1.2 witness kinds, §3.4 result-vector, §5.1 two-axis" },
  { artifact_id: "mb/dependency-manifest/v7",
    digest_or_receipt_slot: "9bdd91604559cebae270efbb420324a320190f875fd2948e4e69df4b9c966673",
    anchor: "#input-separation, #derivation, §2.4 subject binding, §6 intersections" },
  { artifact_id: "mb/ninfty-stage2-predicate/v12",
    digest_or_receipt_slot: "receipt:predicate_spec_digest",
    anchor: "self" }
]

historical_quotation_refs[] = [
  { artifact_id: "mb/ninfty-stage2-predicate/v5..v10", note: "版履歴・差分表・自認文のみ" },
  { artifact_id: "mb/ninfty-verifier-contract/v1..v5", note: "差分表・自認文のみ" },
  { artifact_id: "mb/dependency-manifest/v1..v5", note: "差分表・自認文のみ" }
]
```

| # | 条項 |
|---|---|
| **LA-1** | **本稿の live な版束縛は §6 の pin 3 欄と上の block のみ。** 本文の他の contract / manifest 参照は**版中立**(「verifier contract §…」「dependency manifest §…」)である。 |
| **LA-2** | **release lint は本文の version token を走査し、`live_authority_refs[]` に無い旧版 ID が live 文に現れたら fail させる。** `historical_quotation_refs[]` の ID は版履歴・差分表・自認文にのみ現れてよい。 |
| **LA-3** | **【[sweep-def]・現行有効な lint 契約】** 本行は `[historical]` ではなく、**現在の release lint が従う sweep 対象定義**である。定義は直下の `sweep_definition` block を正本とする。 |

```text
sweep_definition = {                      # [sweep-def] 現行有効
  self_artifact   = "mb/ninfty-stage2-predicate/*",
  self_alias      = "spec v<N>",
  other_artifacts = [ "mb/ninfty-verifier-contract/*", "mb/dependency-manifest/*" ],
  other_aliases   = [ "contract v<N>", "manifest v<N>" ],
  bare_token      = "v<N> + 助詞",       # 【chg v<N> …】 のみ allowlist
  current_version = "v12",
  historical_upper_bound = "v11",   # = current - 1(script v3 が自動照合)
  rationale = "自版だけを見る sweep は不十分 — 便 68 F6 が反証した失敗型"
}
```

