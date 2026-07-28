# `mb/dependency-manifest/v10` — implementation dependency closure の記録様式

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 91)。前版を supersede。**

> **[historical]** **【版履歴】本版 = 前版の修理。** 起点は **Sol 便ではなく内部前哨ゲート(falsifier)の第 2 巡**。変更は **3 点** — **(W1) SB-7 新設**: SB-3′ の主張に **D-R4 と同水準の限界宣言**を付す・**(W2) N-2 新設**: `build_record_present` の虚偽宣言に対する **R-6 + I-3a の補償論法**を番号つきで明文化し、**実装依存部を UNKNOWN として EP へ送る**・**(W3) LA-3 の再型付け**: `[historical]` ではなく **`[sweep-def]`(現行有効な sweep 対象定義)**へ。**数学的内容・交差検査の四面・TCB 四欄・D-1〜D-4′ は前版と逐語同一。**

> **[historical]** **【版履歴】v6 = v5 の修理。** 起点は **Sol 便ではなく内部前哨ゲート(falsifier)**。変更は **2 点** — **(R1) FINDING-1 の修理**: entry 粒度の subject binding を **record ごとの自己束縛**に一意化(「相互照合」を撤回)・**(R2) FINDING-4 の配置点検**: LA-2 の配置規約に反する historical token を持つ live 行が無いことを構造 lint で確認。**数学的内容・交差検査の四面・TCB 四欄は v5 と逐語同一。**
**この文書は governing spec §4.4 の `dependency_manifest_schema_id` が指す実体である**(版束縛は §0 の header 1 箇所・§9 の `live_authority_refs[]`)。

## 0. lifecycle state {#lifecycle}

```text
embedded_state_at_candidate_creation = {
  schema_freeze_id: NOT ISSUED,
  manifest_production: NOT AUTHORIZED
}
live_status_authority = Sol freeze reply + commander receipt
live_freeze_and_authorization_authority = approved freeze receipt
```
**上記 blob は candidate 作成時点で埋め込まれた状態であって live status ではない。live status の正本は approved freeze receipt 側にあり、receipt 発行によって本稿を書き換える必要はない(digest 不変)。**

```text
schema_id     = "mb/dependency-manifest/v10"
schema_digest = <64 hex: 本稿 exact blob の sha256 — receipt が記入>
encoding      = UTF-8, LF, no BOM, no normalization
governing_spec = "mb/ninfty-stage2-predicate/v15"
governing_spec_digest = <64 hex: governing spec の digest — receipt が記入>
supersedes    = "mb/dependency-manifest/v9"
supersedes_digest = 5a7da84c3ff076e10a164827158ecfc6d5832ba72dfaf8fb43f670d4db70ff12   # 内部前哨ゲート第 3 巡 (FINDING 2/3/4)
supersedes_prev2  = 46150ba03ae02c340431fe3a162d2925b7b7a5b8fcf55dca76fd2c6c5e351df8
supersedes_v4     = 378f30c84f79bf5d18055ccb824f21e65b3efd11a1d947178e94233f74412d11
supersedes_v3     = 1a8d1f2147178b49d5fe81da625256762a9e9dafd1a963b57d554bcf97c7b7dd
```

> **【hash 順序・便 66 F11 / 便 67 F11】** 非循環な順序は **manifest → contract → spec → receipt**。**本稿は下流(contract / spec)の digest を pin しない。** governing spec は **ID で束縛し digest は receipt 側**。
> **【fail-closed】header の governing spec は本稿起草時点で未発行の後継である。receipt がその実在と digest を束縛するまで、本稿を operative として扱ってはならない。**

**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。
**優先関係**: 本稿と governing spec が矛盾した場合、**governing spec が優先**する。

---

## 0.-1 前版差分【裁定 85・内部前哨ゲート第 2 巡起点】

> **起点の明示**: 本版の差戻しも **Sol の監査便ではなく内部前哨ゲート(falsifier)**による。第 2 巡は **cross-document 同期類型**を突いた。
> **教材(採録)**: 「**修理の自己完結 ≠ 体系の整合**」 — 単一文書内で完結した修理でも、**参照する側の文書に旧概念が残れば体系としては矛盾仕様**。**同期は文書単位でなく clause-ID 単位で機械検査する必要がある。**

| ID | 前版 | 本版 | 出所 |
|---|---|---|---|
| **W1** | SB-3′ は「差し替えれば binding が変わる」とだけ述べ、**D-R4 と同水準の限界宣言が無かった** | **SB-7 新設**: 本層の主張は**申告 preimage との整合の範囲**に限られ、**$c$・$b$・$P$・$r$ を一括で自己整合に捏造する経路は本層では防がない**ことを明示。**防御は `content_digest` の実バイト照合・§2.5 の `build_attestation`・EP の領分**と出所を書き分ける | 第 2 巡 要修正 1 |
| **W2** | `build_record_present = false` の虚偽宣言をどう拾うかが**未明文**(N-1 型の証明が無い) | **N-2 新設**(番号つき補償論法): R-6 昇格と H-1a″ の fixpoint 再計算により、**build 欄を隠しても build artifact 自体は closure entry として現れ I-3a が拾う**。**ただし R-6 昇格の完全性は受領側の独立再導出能力に依存する**ので、**その部分は UNKNOWN と明記し EP の検収項目へ送る**(過大主張しない) | 第 2 巡 要修正 2 |
| **W3** | LA-3 を `[historical]` blockquote に置いていたが、**実体は現行有効な sweep 対象定義**でありラベルが意味的に不正確 | **`[sweep-def]` 型の明示 block へ**。**3 文書で同型**。script v3 の除外域も同型で対応し、**「上限 = 現行版 − 1」の自動照合**を追加 | 第 2 巡 軽微 1 |

---

## 0.0 前版差分【裁定 84・内部前哨ゲート起点】(【chg v6 から継承・変更なし】)

> **起点の明示**: 本版の差戻しは **Sol の監査便ではなく、便 69 発送前の内部前哨ゲート(falsifier)**による。**self-audit 9/9 ALL PASS の外側**で見つかった。

| ID | v5 | v6 | 出所 |
|---|---|---|---|
| **R1(FINDING-1・重大)** | I-0c′ 手順 (3)「D-4 を対応 build record を持つ各 entry についても再計算し **top-level と相互照合**」は**実行不能**だった。**`subject_code_digest` は top-level record にのみ存在し、`manifest_entry` スキーマに無い。** E-10 は **entry 側 D-4 の第一成分の出所を定義していない**。読み (a) top-level 値の流用 → entry の build_definition/pinned_inputs は top-level と異なるので**相互照合が恒常不一致**(一致するのは build 共有 = 本来 I-3d が [11] で弾く場合のみ)。読み (b) entry の `content_digest` 代入 → **「top-level と相互照合」が無意味**。**どちらの読みでも破綻。**さらに R-1〜R-6 は subject $X$ 自身を entry 化しないので**「対応 build record を持つ entry」の参照先が未定義**だった。**帰結: SB-3 の「Q1 反例は閉じる」は top-level についてのみ真で、entry 粒度では同型反例を再構成できた。自認** | **D-4 を record ごとの自己束縛へ一意化**(§2.2 D-4′): **preimage 第一成分は **top-level record では `subject_code_digest`・build record を持つ entry では当該 entry 自身の `content_digest`**。**「相互照合」の語を廃止**し、義務を **「record ごとに受領側が preimage から再計算し、その record の記載値と一致すること」**へ(I-0c″)。**異 record 間の等式は主張しない** — 二 record の binding が一致するのは build 共有であり、**それは I-3d の領分**(§2.4 SB-6 で棲み分けを条文化)。**E-10′ で第一成分の出所を明記**・**SB-3′ の射程を全 record 粒度へ**・**SB-5 で build record 不在 entry の明示宣言を義務化** | 内部ゲート FINDING-1・裁定 84** |
| **R2(FINDING-4)** | live 行の版 token 判定が語の部分一致に依存し、**LA-2 の配置規約に反する live 行を見逃す**恐れがあった | **構造 lint(`search/bundle-selfaudit.py` v2)で点検**し、本稿に配置違反 0 を確認。**LA-2 に「歴史 token を含む live 行を置かない」を明文化** | 内部ゲート FINDING-4 |

---

## 0.1 前版差分【裁定 83】(【chg v5 から継承・変更なし】)

| ID | v4 | v5 | 出所 |
|---|---|---|---|
| **Q1(F8)** | D-3 の preimage は `build_definition_blob_digest` と `pinned_input_digests[]` のみで、**`subject_code_digest` が一度も計算に現れない**。top-level record は両者を並べるだけで**結ぶ等式が無く**、R-1 は subject $X$ 自身を `content_digest` とする entry を要求しないので **I-0c″ の「該当 entry」も subject output を一意に指定しない**。**紙上反例(Sol F8 を条文内に採録)**: 任意の $c$・$b$・$P$ に対し $r:=H(\{b,P\})$ とすると、受領側は $r$ の自己整合を確認できるが **$c$ を別の $c'$ に差し替えても I-0c″ は同じ結果を返す**。**自認** | **§2.4 に `subject_build_binding_digest` を frozen preimage の mandatory 欄として新設**(D-4)。**top-level subject と対応 build record の双方で受領側再計算・照合**(I-0c′ を「$c$ が計算に現れる」形へ書き直し)。**上位層 `build_attestation` は optional schema として定義**し、**実生成関係を主張する場合に限り必須**と効力を明記(§2.5) | 便 68 F8・F13.2 |
| **Q2(F9)** | 冒頭の要約と §5.2 heading が **「五欄」**と書く一方、実際の宣言・§5.4 の初期値・T-1′・契約 C-3′/C-5′/C-8′ はすべて**四欄**。H-5c が omitted field を暗黙の空集合にも暗黙の許可にも読ませないので、**算数 typo として放置できない**。**自認** | **2 箇所とも「四欄」へ**。**`allowed_shared_family[]` は欄を保持**し、意味を **「`family_overlap_flag` への acknowledged justification list(audit 専用・非 blocking・I-3c′ は差し引かない)」**に一意化(§5.2・§6) | 便 68 F9・裁定 83 |
| **Q3(F13.1)** | live 参照の版 token が本文に散在し、機械 lint できなかった | **§9 に `live_authority_refs[]` / `historical_quotation_refs[]` の機械可読 block を新設**。**本文の版束縛は header 1 箇所に集約**し、他は版中立の節参照へ | 便 68 F13.1・裁定 83 |

---

## 0.1.1 前版差分【B67-2】(【chg v4 から継承・変更なし】)

| ID | v3 | v4 | 出所 |
|---|---|---|---|
| **P1(F7.1)** | D-3 を「凍結された導出規則」として書いたが、**`build_definition_blob_digest` と `pinned_input_digests[]` が `manifest_entry` にも top-level にも無く**、**D-R2 / I-0 の再計算義務も D-1 / D-2 にしか及んでいなかった**。ゆえに **`build_root_id` は依然 producer の申告値**で、「D-1〜D-3 を凍結し受領側が再計算」という要旨を D-3 について満たしていない。**自認** | **D-3 の preimage を record 欄に mandatory 化**(§2.1 E-9′)。**D-R2 / I-0 の再計算義務に D-3 を含める**(D-R2′・I-0′)。**`build_root_id` の subject code への binding も受領側が検査**(I-0c″) | 便 67 F7.1 |
| **P2(F7.2)** | 三交差(binary / source / family)は **共有 build helper を見逃す**。反例: `toolchain_digest = t`・`build_step_digests = [g]` を共有しつつ `content_digest` と `source_artifact_digests[]` が異なる A/B は、$D_2$ が異なるので family も異なり、**I-3a / I-3b / I-3c をすべて通る**。$t,g$ が両実装へ同じ数学処理を生成する共有 build helper なら、空 TCB の下で [11] で止まるべき common bug path である。**さらに R-1〜R-5 に「出力へ影響する build-time artifact を closure entry にする」条文が無かった。自認** | **(a)+(b) の両方を実施**: **R-6 で output-affecting な toolchain / build step / code generator を closure entry へ必須昇格**(fixpoint 検収の対象)し、**§6 に build face の交差 I-3d を normative 新設**。**四面(binary / source / build / family)へ分離**(便 67 F13.2 の発案) | 便 67 F7.2・F13.2 |
| **P3(F7.2c)** | `implementation_family_id` は **M-2 が $D_2\to$ family を単射にする**ので **lineage digest の別名**にすぎず、「異なる lineage を同じ generator family にまとめる」検出器になっていなかった(**過大主張**)。**自認** | **family を normative な blocking path から外し `audit flag` へ降格**(便 67 F13.2 の推奨 —「family の主観判定を避けたいなら最初の三面だけを normative にし、family は audit flag に留める方が fail-closed」)。**M-2′ で family を lineage の粗化と定義**し、**authority は根拠つきで merge のみ可能・split 不可**。**§6 注記 N-1 に「三面が旧 I-3c を包含する」証明**を置き、降格が**弱化でないこと**を示す | 便 67 F7.2・F13.2 |
| **P4** | governing spec = v8 | **v9 へ**(ID・digest は receipt) | 裁定 81 |

---

## 1. この様式が閉じる未定義項 {#purpose}

| 未定義項 | 本稿 |
|---|---|
| 直接依存か**推移的閉包**か | §3(R-1〜R-6・H-1′) |
| 別名・別 path・薄い wrapper の同一性 | §2・§4(H-2・H-2a) |
| rebuild lineage と exact blob identity の接続 | §2.1・§2.2・§4(H-2b″) |
| lineage の producer 自己申告回避 | §2.2(再計算規則)・§2.3・§4(H-2d) |
| **build 経路(toolchain / build step / build definition)の閉鎖** | **§2.1 E-9′・§3 R-6・§6 I-3d** |
| helper の範囲 | §5.1(`role` 分類・H-3a) |
| 共有を許す trusted base と初期値 | §5.2・§5.4(**四欄すべて実値 `[]`**) |
| 共有 input と共有 implementation の型分離 | §5.3(Y 系・U 系) |

---

## 2. entry の型 {#entry-type}

```text
manifest_entry = {
  content_digest,                # 必須・64 hex・exact blob の identity
  role,                          # §5.1 の分類(必須)

  # --- lineage preimage(すべて必須・§2.1)---
  source_artifact_digests[],     # sorted・deduplicated・exact source blob digests
  toolchain_digest,              # toolchain 実体の exact blob digest(null 不可)
  build_step_digests[],          # ordered digest 列(build 手順そのもの)

  # --- build_root preimage(すべて必須・§2.1 E-9′)【chg v4 新設】---
  build_definition_blob_digest,  # build 定義そのものの exact blob digest
  pinned_input_digests[],        # sorted・deduplicated
  subject_build_binding_digest,  # = D-4′ の再計算値と一致すること(第一成分 = 当該 entry の content_digest)
  build_record_present,          # true / false・分岐は [branch-contract] が正本
                                 # false なら forbidden_keys は ABSENT(key 不在)であること

  # --- 受領側が再計算する導出値(producer の申告値は参照値にすぎない)---
  source_closure_digest,         # = D-1 の再計算値と一致すること
  implementation_lineage_digest, # = D-2 の再計算値と一致すること
  build_root_id,                 # = D-3 の再計算値と一致すること【chg v4 で再計算対象へ】
  implementation_family_id,      # audit flag(§2.3)・normative な判定には使わない

  provenance = { source_ref },   # human-readable・identity には使わない
  outgoing_dependency_attestation,
  depth,                         # 記録のみ
  reached_via[]
}
```

### 2.1 preimage の列挙義務 {#preimage}

| # | 条項 |
|---|---|
| **E-5** | **`source_artifact_digests[]` は mandatory** であり、**aggregate ではなく構成要素の列**(sorted・deduplicated・exact source blob)。 |
| **E-6** | **`toolchain_digest` と `build_step_digests[]` も mandatory。** 前者は toolchain 実体の exact blob digest(名前・版文字列ではない)で **null 不可**、後者は build 手順 digest の**順序つき列**。 |
| **E-9′** | **【本版で条件化・B69-4】`build_definition_blob_digest` と `pinned_input_digests[]`(sorted・deduplicated)は **top-level record と `build_record_present = true` の entry で mandatory**。これが **D-3 の preimage の全体**である。**`present = false` の entry では `[branch-contract]` の `forbidden_keys` が ABSENT(key の不在)でなければならない** — 判定は四象限表(QD-1〜QD-4)が正本。** |
| **E-10′** | **【chg v6 で書き直し】`subject_build_binding_digest` は、build record を持つ全 record(top-level および `build_record_present = true` の各 entry)で mandatory**。preimage は §2.2 D-4′ の 3 要素で、**第一成分の出所は record 種別で決まる** — **top-level では `subject_code_digest`・entry では当該 entry 自身の `content_digest`**。**** |
| **E-7‴** | **E-5・E-6・E-9′・E-10′ が D-1 / D-2 / D-3 / D-4′ の**四** hash すべての preimage を尽くす。** 受領側はこれだけから §2.2 の四 hash を再計算できなければならない。**再計算不能な entry は独立性の証跡として使えない。** |
| **E-8″** | **producer が申告した `source_closure_digest` / `implementation_lineage_digest` / `build_root_id` / `subject_build_binding_digest` は参照値でしかない。** 受領側の再計算値と食い違えば `digest-mismatch` [12]。 |
> **[historical] E-10′**: v5 は entry 側第一成分の出所を定義せず、「top-level と相互照合」を要求していた・自認。


### 2.2 導出規則(**凍結**・受領側が再計算)【D-3 を含む】{#derivation}

```text
[normative-check-block]
D-1  source_closure_digest =
       sha256( canonical_serialize( sort(dedup(source_artifact_digests[])) ) )

D-2  implementation_lineage_digest =
       sha256( canonical_serialize( {
           "source":    sort(dedup(source_artifact_digests[])),
           "toolchain": toolchain_digest,
           "steps":     build_step_digests[]          # 順序を保つ
       } ) )

D-3  build_root_id =
       sha256( canonical_serialize( {
           "build_definition": build_definition_blob_digest,
           "pinned_inputs":    sort(dedup(pinned_input_digests[]))
       } ) )

D-4′ subject_build_binding_digest =                       # 【chg v6 で第一成分の出所を確定】
       sha256( canonical_serialize( {
           "subject":          <当該 record の subject>,
           "build_definition": build_definition_blob_digest,
           "pinned_inputs":    sort(dedup(pinned_input_digests[]))
       } ) )
       #  <当該 record の subject> =
       #      top-level record   -> subject_code_digest
       #      manifest_entry     -> その entry 自身の content_digest
       #  各 record は「その record が指す artifact」を「その artifact の build」に束縛する。
       #  異 record 間の等式は主張しない(build 共有の検出は I-3d の領分)。

canonical_serialize = UTF-8 / LF / key 昇順 / 配列は明示順 / 空白なし
```

| # | 条項 |
|---|---|
| **D-R1** | **D-1・D-2・D-3・D-4′ の四つはいずれも本稿で凍結された規則であり、producer 側の裁量を含まない。** |
| **D-R2⁗** | **【本版で分岐同期・B70-1】 `[branch-contract]` の `recompute` に従う** — **D-1 と D-2 は全 record**・**D-3 と D-4′ は top-level と `present = true` の entry のみ**。**`present = false` の entry は QD-3 / QD-4 の canonical-empty check だけへ送る。** |
| **D-R3** | **preimage が一致すれば同一 lineage と判定する。** ID・名前・版文字列の相違は判定に影響しない — **ID の付け替えでは逃げられない。** |
| **D-R4** | **【chg v4】hash の再計算は「申告 preimage と申告 aggregate の整合」を示すだけで、preimage の完全性や build への実接続を自動では証明しない**(便 67 F7 末尾)。ゆえに **R-6 の closure 昇格**と **I-0c″ の binding 検査**を併置する。 |
> **[historical] D-R2‴**: v3 は D-1・D-2 のみ、v4 は D-3 まで、v5 は D-4 を要求したが **entry 側第一成分が未定義**だった(**自認**)。


### 2.34 `branch_contract` — **分岐の唯一正本**【B70-1・F11.1 逐語】 {#branch-contract}

> **⚠ 前版の欠陥(自認)**: 「QD 表が正本」と宣言しただけでは足りず、**同じ blob の operative 条項が false leaf に別の判定を命じていた** — D-R2‴(四つ全て再計算)・contract C-6⁗(六欄提出)・I-0c″(4)(binding 欠落は [12])・R-6 / H-1a″ / N-2(値に関わらず昇格)。**同じ record が reader ごとに PASS / [12] に分かれた。**
> **以後、分岐の正本は下の `[branch-contract]` block だけである。QD 表(§2.35)はこの block の描画にすぎない。**

```text
[branch-contract]                      # 【唯一の分岐正本・全 consumer はここを参照する】
branch_contract = {
  true: {
    required_keys  = [build_record_present, build_definition_blob_digest,
                      pinned_input_digests[], build_root_id, subject_build_binding_digest,
                      source_artifact_digests[], toolchain_digest, build_step_digests[]],
    recompute      = [D-1, D-2, D-3, D-4′],
    closure_policy = recursive,
    assurance      = identity-binding (SB-7 の限界内)
  },
  false: {
    required_keys  = [build_record_present,
                      source_artifact_digests[], toolchain_digest, build_step_digests[]],
    forbidden_keys = [build_definition_blob_digest, pinned_input_digests[],
                      build_root_id, subject_build_binding_digest],
    recompute      = [D-1, D-2],
    closure_policy = bootstrap_leaf,
    assurance      = UNKNOWN
  }
}
# valid_scalar_digest(x) := x が 64 hex の非空文字列
# forbidden_keys は ABSENT(key 不在)でなければならない。null/空文字/0 は違反。
# consumer = { D-R2‴, I-0″, I-0c″, build_artifact_set, R-6, H-1a″, N-2, contract C-6⁗ }
```

| # | 条項 |
|---|---|
| **BC-1** | **`[branch-contract]` block が分岐の唯一正本。** 本稿・contract・receipt の全 consumer はこの block を参照し、**独自の分岐記述を持たない**。 |
| **BC-2** | **consumer 一覧は block の `consumer` 行に literal で置く。** consumer を増やすときは block を先に更新する。 |
| **BC-3** | **consumer matrix equality**: QD-1〜QD-4 の concrete record に対し、**全 consumer が同一 verdict を返さなければならない**(self-audit の check で機械照合)。 |

### 2.35 `build_record_present` の四象限 fixture 表—**`[branch-contract]` の描画**—**本節が分岐の正本**【B69-4・F13.2】 {#quadrants}

> **[historical]** **⚠ 前版の欠陥(自認)**: `build_record_present = false` の entry について、**SB-5 は 4 欄が空でよいとし I-0c″(3) は空を確認せよと命じる**一方、**E-9′ は build definition / pinned inputs を全 entry で mandatory とし、I-0′ は全 entry で D-3 を再計算せよと命じ、`build_artifact_set` は全 entry の `build_definition_blob_digest` を無条件に union していた**。ゆえに同じ false entry に対し **reader A は [11] または [12]、reader B は PASS** という**二結果**が出た。さらに empty を共通 sentinel として集合へ入れると **A/B 双方の closure が同じ empty を共有し I-3d が偽の [11]** を出す。**正直な `false` record の受け方が未定義だった。**

**以後、`build_record_present` の分岐はこの表だけを正本とする。E-9′・I-0″・I-0c″・build-face 射影は本表を参照し、prose で別々に説明しない。**

| # | `present` | fields | expected |
|---|---|---|---|
| **QD-1** | `true` | **complete** = `true.required_keys` がすべて present・**scalar digest 欄は valid nonempty 64-hex**・**`pinned_input_digests[]` は present かつ schema-valid で `[]` を許す** | **D-1・D-2・D-3・D-4′ を再計算**して申告値と照合 |
| **QD-2** | `true` | **missing** = `true.required_keys` のいずれかが不在、または scalar digest が invalid | **`digest-mismatch` [12]** |
| **QD-3** | `false` | **canonical empty** = `false.forbidden_keys` がすべて ABSENT かつ `false.required_keys` が present | **bootstrap leaf として受理**・**D-1・D-2 のみ再計算**・**D-3 / D-4′ は免除**・**失う保証は `UNKNOWN`** |
| **QD-4** | `false` | **nonempty** = `false.forbidden_keys` のいずれかが present(null / 空文字 / 0 を含む) | **`digest-mismatch` [12]** |

```text
[canonical-empty]                       # QD-3 の唯一の表現(他形は QD-4)
build_definition_blob_digest : ABSENT      # key ごと存在しない(null でも空文字でもない)
pinned_input_digests[]       : ABSENT
build_root_id                : ABSENT
subject_build_binding_digest : ABSENT
# ABSENT は値ではなく key の不在である。ゆえに集合演算の要素にならない。
```

| # | 条項 |
|---|---|
| **QD-5′** | **【本版で R-6 との衝突を解消・F9.1 最小形】 `present = false` は provenance の bootstrap leaf である。****R-6 / H-1a″ の例外は「その leaf 自身の toolchain を再帰的に entry 化すること」だけ**である。**申告済みの `toolchain_digest` / `build_step_digests[]` は build face(I-3d)に残る** — 例外は昇格の再帰であって射影ではない。**この例外で失う完全性は QD-6 の `UNKNOWN`。** E-6 が要求する non-null `toolchain_digest` の**再帰的な entry 化はこの leaf で停止**する(toolchain の toolchain を無限に要求しない)。**有限 manifest の base case はこれ。** |
| **QD-6** | **leaf で失う保証は `UNKNOWN` として receipt / EP へ送る。** leaf の artifact には **build への binding が存在しない**ので SB-7 の限界がそのまま適用される。**「leaf だから安全」と読んではならない。** |
| **QD-7** | **`ABSENT` は sentinel ではない。** null や空文字や 0 で埋めた record は **QD-4 = [12]**。**ゆえに empty が集合の要素になる経路は存在せず、I-3d の偽 [11] は起きない。** |

### 2.4 `subject_build_binding_digest` — **identity binding 層**【Q1】{#subject-binding}

> **[historical]** **⚠ v4 の欠陥(自認)**: D-3 の preimage に **`subject_code_digest` が無く**、top-level の `subject_code_digest` と `build_root_id` を**結ぶ等式が存在しなかった**。R-1 は subject $X$ 自身を entry にする規則ではないので、**I-0c″ の「該当 entry」も subject output を一意に指定しない**。
> **反例(便 68 F8 を逐語採録)**: 任意の `subject_code_digest` $c$、任意の build definition $b$、pinned inputs $P$ を選び $r:=H(\{b,P\})$ とする。top-level と該当 entry に同じ $b,P,r$ を置けば、**受領側は D-3 を再計算して $r$ の自己整合を確認できるが、$c$ は計算に一度も現れない**。**ゆえに別の $c'$ に差し替えても I-0c″ は同じ結果を返す。** R-6 は $b,P$ を closure へ昇格するが、$\mathrm{Build}(b,P)=c$ の binding を追加しない。

| # | 条項 |
|---|---|
| **SB-1′** | **`subject_build_binding_digest` は §2.2 D-4′ で定義される frozen preimage の mandatory 欄である。** preimage は $\{$ **当該 record の subject**, `build_definition_blob_digest`, `pinned_input_digests[]` $\}$。 |
| **SB-2′** | **【chg v6 で撤回・書き直し】各 record の D-4′ は「その record 自身の subject」で計算する** — **top-level では `subject_code_digest`、entry では当該 entry 自身の `content_digest`**。**受領側の義務は「record ごとに preimage から再計算し、その record の記載値と一致すること」**(I-0c″)。 |
| **SB-3′** | **これにより、各 record の subject がその record の binding 計算に現れる。** top-level では $c$ を差し替えれば binding が変わり、**entry では当該 artifact の `content_digest` を差し替えれば binding が変わる**。 |
| **SB-5** | **【chg v6 新設・本版で ABSENT 語へ統一】build record の不在は明示する。** entry は `build_record_present` を持ち、`false` のとき build preimage 4 欄(`build_definition_blob_digest`・`pinned_input_digests[]`・`build_root_id`・`subject_build_binding_digest`)は **ABSENT(key 不在)でなければならない**(§2.34 `[branch-contract]` の `forbidden_keys`)。**`null` / 空文字 / `0` で埋めた record は QD-4 = `digest-mismatch` [12]**(QD-7 と同語)。**ただし `false` の宣言自体が必須**であり、**欄を黙って落とすことは不備**(H-1′ の「空列であることの明示的証明」と同じ規律 — **さもなくば producer は build 欄を省略するだけで per-record binding を回避できる**)。**`build_record_present = true` なら 4 欄すべてが必須。** |
| **SB-6** | **【chg v6 新設】異 record 間の binding 等式は主張しない。** 二つの record の `subject_build_binding_digest` が一致するのは、**subject と build definition と pinned inputs のすべてが一致する場合**に限る。**build の共有それ自体の検出は §6 の build face(I-3d)の領分**であり、binding 層はこれを担わない。**二層を混同しない**(BA-5 と同じ規律)。 |
| **SB-7** | **【本版新設・限界宣言(D-R4 と同水準)】** SB-3′ の「subject を差し替えれば binding が変わる」という主張は、**申告された preimage と申告された aggregate の整合の範囲**でのみ成り立つ。**producer が $c$(subject)・$b$(build definition)・$P$(pinned inputs)・$r$(build_root_id)・binding を*一括して自己整合に捏造*する経路は、本層では防がない。** hash の再計算は**内部整合の証明であって、実在する artifact や実在する build への接続の証明ではない**(D-R4 と同じ限界)。**防御の所在は本層の外にある**: (i) **`content_digest` の実バイト照合**(受領側が artifact そのものを取得して digest を計算する)(ii) **§2.5 の `build_attestation`**(`output_digest == subject_code_digest` と deterministic rebuild)(iii) **EP(external positive control)**。**本層をこれらの代替として用いてはならない。** |
| **SB-4** | **【効力の正直な宣言】本層が保証するのは identity binding(取り違え防止)までである。** 「この build が実際に $c$ を生成した」という**実生成関係は主張しない** (**hash tuple だけでは実生成関係を証明しない** — 便 68 F8・D-R4)。実生成を主張するには §2.5 の上位層が要る。 |
> **[historical] SB-2′**: v5 の「top-level と相互照合」は撤回する** — 異なる record は異なる build definition を持つのが通常であり、**相互照合は恒常不一致になるか、無意味になるかのどちらかだった**(内部ゲート FINDING-1・**自認**)。
> **[historical] SB-3′**: ゆえに Q1 の反例は top-level だけでなく全 record 粒度で閉じる**(v5 は top-level についてのみ真だった・**自認**)。


### 2.5 `build_attestation` — **実生成証跡層(optional)**【F13.2】{#build-attestation}

```text
build_attestation = {            # optional schema
  inputs_digest,                 # build に入った全入力の canonical digest
  output_digest,                 # == subject_code_digest でなければならない
  builder_digest,                # builder 実体の exact blob digest
  reproducibility_result         # deterministic rebuild の結果(一致 / 不一致 / 未実施)
}
```

| # | 条項 |
|---|---|
| **BA-1** | **`build_attestation` は optional。** 省略しても本稿の identity binding(§2.4)は成立する。 |
| **BA-2** | **ただし「この build が subject を生成した」という実生成関係を主張する場合に限り必須**となる。**attestation 無しでその主張をしてはならない。** |
| **BA-3** | **`output_digest == subject_code_digest` は受領側が検査する。** 不一致は `digest-mismatch` [12]。 |
| **BA-4** | **`reproducibility_result` が「未実施」のとき、実生成関係は `UNKNOWN`** であって PASS ではない。 |
| **BA-5** | **§2.4 と §2.5 を同じ「binding」という語で混ぜない**(便 68 F13.2)。前者は取り違え防止、後者は実生成の証跡である。 |

### 2.3 `implementation_family_id` — **audit flag へ降格**【P3】{#family}

| # | 条項 |
|---|---|
| **M-1′** | **`implementation_family_id` は receipt authority が mint する。producer は自分で選べない。** |
| **M-2′** | **family は lineage の粗化(coarsening)である。** 既定は $D_2$ 誘導クラス(同じ `implementation_lineage_digest` は同じ family)。**authority は記録された根拠つきで複数 lineage を merge できるが、split はできない。** |
| **M-3′** | **family は `audit flag` であって normative な blocking path には置かない**(便 67 F13.2)。**[11] の判定は §6 の三面(binary / source / build)だけで行う。** family 交差が非空なら **receipt に `family_overlap_flag` を記録**し、authority の判断材料とする。 |
| **M-4** | **producer 可変の識別子を lineage 判定に用いない。** |
| **M-5** | **merge のみ可能・split 不可**という単調性により、**family の追加操作は判定を緩めない**(緩める方向の操作が存在しない)。 |
> **[historical] M-4**: v2 の `generator_lineage_id` は廃止**。


| # | 条項(前版から継続) |
|---|---|
| **E-1** | **exact blob の identity は `content_digest` のみで決まる。** `source_ref`・path・パッケージ名・版名は identity に使わない。 |
| **E-1′** | 系列の identity は preimage から §2.2 で導かれる。**交差検査は §6 の各面に対して行う。** |
| **E-2** | 同じ blob が複数経路で到達しても entry は 1 つ。 |
| **E-2′** | **`depth` は記録欄であって合否判定に使わない。** |
| **E-3** | `role` の欠落は不備。**未分類 entry を TCB とみなす既定を置かない。** |
| **E-4** | preimage 欄(E-5・E-6・E-9′)の欠落は**独立性の主張を無効にする**。 |

---

## 3. 推移的閉包の生成規則 {#closure-rules}

```text
[normative-check-block]
implementation_dependency_closure(X) = 最小の集合 D で次を満たすもの:
  R-1  X が直接 import / link / load する全 *implementation* artifact
       の content_digest ∈ D        # declared_untrusted_inputs[] は含めない(§5.3)
  R-2  d ∈ D ならば、d が直接 import / link / load する全 artifact の
       content_digest ∈ D                          # 推移閉包
  R-3  実行時に動的解決される artifact も、解決され得る候補集合を D に含める
  R-4  データとして読み込まれるだけの artifact のうち、
       *手続きの挙動を決める* もの(規約ファイル・定数表)は D に含める
       ※ *内容が再検査される入力データ* は §5.3 により universe 外
  R-5  D は fixpoint に達するまで展開する

  R-6  【chg v4 新設】output-affecting な build-time artifact —
       toolchain、build step、code generator、build definition、pinned input —
       は必ず closure entry へ昇格し、その digest が
       いずれかの entry の content_digest に解決されること。
       # これにより共有 build helper は I-3a(binary face)でも捕捉される
```

### 3.1 fixpoint の検収 {#fixpoint}

| # | 条項 |
|---|---|
| **H-1′** | 各 entry は `outgoing_dependency_attestation` を持つ。**何も load しない場合は空列であることの明示的証明**を含む。 |
| **H-1a″** | **受領側が fixpoint を再計算する。** 到達可能だが未列挙の artifact、**または R-6 の昇格対象で `content_digest` に解決されない digest** があれば `digest-mismatch` [12]。 |
| **H-1b** | 閉包は **producer の環境で実際に解決された artifact** に対して取る。 |
| **H-1c** | **`depth` の分布を合否判定に使わない。** |

---

## 4. 同一性の正規化 {#identity}

| # | 条項 |
|---|---|
| **H-2** | **exact blob の同一性は content digest で判定する。** |
| **H-2a** | **wrapper 貫通**: $W$ が $h$ を呼ぶだけの薄い層なら、閉包 $D$ は $h$ の digest を含む。 |
| **H-2b″** | **同一 `implementation_lineage_digest`(受領側再計算値)を持つ二 blob は、content digest が異なっても同一 helper とみなす。** 規則であって裁量ではない。**「別実装である」と主張する側に挙証責任**があり、**preimage が異なることの提示**によって行う。 |
| **H-2c** | content digest は **exact blob** に対して取る。 |
| **H-2d** | **producer 可変の識別子(名前・版文字列・自己申告 ID)を同一性判定に用いない。** |

---

## 5. `role` 分類・TCB・入力の型分離 {#roles-and-tcb}

### 5.1 `role` の分類

```text
role ∈ { math-helper, serialization, hash-primitive, runtime,
         cas-io, build-tool, data-table, code-generator }
```
**【chg v4】`code-generator` を追加** — R-6 で closure へ昇格する build-time artifact のうち、**出力コードを生成するもの**。

| # | 条項 |
|---|---|
| **H-3** | `allowed_shared_tcb[]` は frozen content digest で列挙し `role` を付す。**`role = math-helper` を TCB に入れることを禁止する。** |
| **H-3a** | **math-helper の判定基準**: 出力が「どの数学的対象が等しいか」に影響しうる処理はすべて math-helper — **canonicalizer・ideal 演算・Gröbner / normal form / reduction・divisor 正規化・partition 計算・多項式演算・体演算**。**迷えば math-helper**(既定は禁止側)。 |
| **H-3a′** | **【chg v4】`code-generator` が math-helper を生成する場合、その generator も math-helper と同じ扱い**(TCB 禁止)。**生成物が数学処理なら、生成器の共有は共通 bug 経路である。** |
| **H-3b** | `serialization` / `hash-primitive` / `runtime` / `cas-io` / `build-tool` は TCB 候補。**自動ではなく明示列挙して初めて差し引かれる。** |
| **H-3c** | `data-table` は**原則 TCB に入れない**。 |

### 5.2 TCB の宣言様式(**四欄**)【Q2 で訂正】

```text
allowed_shared_tcb[]        = [ { content_digest, role, justification, frozen_at_receipt } ]
allowed_shared_source_tcb[] = [ { source_artifact_digest, role, justification, frozen_at_receipt } ]
allowed_shared_build_tcb[]  = [ { build_artifact_digest, role, justification, frozen_at_receipt } ]  # build face 用(本版で条件化)
allowed_shared_family[]     = [ { implementation_family_id, role, justification, frozen_at_receipt } ] # audit 専用(§5.2.1)
```
| # | 条項 |
|---|---|
| **H-5** | **追加は追加側に挙証責任。** 追加は freeze bundle の変更であり **receipt を要する**。 |
| **H-5a** | receipt 前の追加提案は候補であって効力を持たない。 |
| **H-5b** | 縮む方向には receipt を要しない。 |
| **H-5c** | **省略を暗黙の空集合とも暗黙の許可とも読ませない** — §5.4 が実値を宣言する。 |
| **H-5d′** | **各欄は独立**。content 側を許しても source / build / family 側は自動的には許されない。 |
| **H-5e** | **【chg v5・Q2】欄数は四である**(`allowed_shared_tcb` / `_source_tcb` / `_build_tcb` / `_family`)。**** |
> **[historical] H-5e**: v4 の冒頭要約と §5.2 heading が「五欄」と書いていたのは誤り・自認。


#### 5.2.1 `allowed_shared_family[]` の意味の一意化【Q2・裁定 83】{#family-allowlist}

| # | 条項 |
|---|---|
| **FA-1** | **`allowed_shared_family[]` は `family_overlap_flag` への acknowledged justification list である。** |
| **FA-2** | **audit 専用・非 blocking。** I-3c′ は**この集合を差し引かない** — family 交差が非空なら、allowlist に載っていても `family_overlap_flag` は記録される。**載っているのは「authority が承知している」ことの記録**であって免除ではない。 |
| **FA-3** | **欄は保持する**(削除しない)。理由: 契約 C-3′/C-5′/C-8′ と receipt が **四欄の arity** を前提にしており、欄を削ると下流の schema arity が崩れる(裁定 83)。 |
| **FA-4** | **初期値 `[]`**。 |
> **[historical] FA-4**: 空である限り観測される挙動は v4 と同一(I-3c′ は常に flag を記録する)。


### 5.3 `declared_untrusted_inputs[]` — 入力と実装の型分離 {#input-separation}

```text
declared_untrusted_inputs[] = {
  divisor_equality_certificate, searcher_native_artifact, checker_native_artifact,
  governing_spec_blob, contract_blob
}
```

| # | 条項 |
|---|---|
| **Y-1** | **implementation closure の universe から分離される。** TCB として差し引くのではなく**交差検査の対象外**。 |
| **Y-2** | **入力の共有は独立性を毀損しない。毀損するのは実装の共有である。** |
| **Y-3** | **A と B で digest 一致を要求する。** 不一致は `digest-mismatch` [12]。 |

#### 5.3.2 入力クラスへの math-helper 混入を防ぐ判定基準 {#input-criteria}

```text
[normative-check-block]
U-1  データとして消費される  — 手続きとして実行 / load されない
U-2  内容が再検査される      — 両 verifier が独立にその内容を検証する対象である
U-3  手続きを実現しない      — canonicalization / 簡約 / 比較の *アルゴリズム* を提供しない
U-4  明示宣言されている      — certificate または contract が入力として列挙している
```

| # | 条項 |
|---|---|
| **Y-4** | **U-1〜U-4 のいずれかを欠く artifact は入力クラスに置けない。** |
| **Y-4a** | **パラメータ値と実装の区別**: 規約を選ぶパラメータ値の共有は許される。**禁止されるのはその規約を実現するコードの共有。** |
| **Y-4b** | **迷えば implementation closure へ**(既定は厳しい側)。 |
| **Y-4c** | **入力クラスは列挙型であり、拡張には receipt を要する。** |
| **Y-4d** | **【chg v4】build-time artifact は入力クラスに置けない**(U-1 違反 — 手続きとして実行される)。**R-6 により必ず closure 側。** |

### 5.4 初期 TCB の実値 {#initial-tcb}

```text
allowed_shared_tcb        = []      # 空集合(実値・省略ではない)
allowed_shared_source_tcb = []      # 空集合
allowed_shared_build_tcb  = []      # 空集合【chg v4 新設・実値】
allowed_shared_family     = []      # 空集合(audit flag 用)
```

| # | 条項 |
|---|---|
| **T-1″** | **初期 TCB は四欄とも空である**(`allowed_shared_tcb` / `_source_tcb` / `_build_tcb` / `_family`)。 「省略」でも「暗黙の許可」でもなく、**実装着手前の実値宣言**。 |
| **T-2′** | 空 TCB の下で三面の交差を空にするため、**A と B は異なる runtime で実装し、かつ異なる toolchain / build step で build する**。**共有 toolchain は build face で [11] になる。** |
| **T-3** | 共有したい場合は該当欄に **exact digest・role・justification** を**実装着手前の receipt** で列挙する。**列挙前に着手してはならない。** |
| **T-4** | `serialization` / `hash-primitive` / `cas-io` を共有したい場合も同じ手続き。**現時点ではいずれも四欄に入っていない。** |

---

## 6. 交差検査 — 受領側の再計算手順(**四面**){#intersection}

> **【便 67 F13.2 の発案を採用】** provenance を **runtime(binary)/ source / build / family** の四面に分ける。**normative(blocking)は前三面**、**family は audit flag**(主観判定を blocking path に置かない — fail-closed)。

```text
binary_content_set(X) = { entry.content_digest : entry ∈ closure(X) }
source_artifact_set(X) = ⋃ { entry.source_artifact_digests[] : entry ∈ closure(X) }
build_artifact_set(X)  = union { entry.toolchain_digest        : 全 entry }
                       union { entry.build_step_digests[]     : 全 entry }
                       union { entry.build_definition_blob_digest : build_record_present = true の entry のみ }
                       union { entry.pinned_input_digests[]   : build_record_present = true の entry のみ }
                       # ABSENT(§2.35 [canonical-empty])は key 不在ゆえ要素にならない(QD-7)
authority_family_set(X) = { entry.implementation_family_id }          # audit flag
```

| # | 手順 |
|---|---|
| **H-4** | **交差の値は producer の自己申告を信じない。receipt 受領側が canonical digest 集合から導出して再計算する。** |
| **I-0″** | **【本版で条件化・B69-4】** **D-1 と D-2 は全 entry で再計算**する。**D-3 と D-4′ は top-level と `build_record_present = true` の entry だけで再計算**する(QD-1)。**`build_record_present = false` の entry は I-0c″(3) の canonical-empty check だけへ送る**(QD-3)。不一致は [12](E-8″)。**D-1 / D-2 の preimage 欠落は E-4 により独立性主張を無効化 → [11]。** |
| **I-0c″** | **【chg v6 で書き直し・R1】binding は record ごとに自己完結して検査する。** 手順: (1) **各 record**(top-level および `build_record_present = true` の各 entry)について D-3 を再計算し `build_root_id` の自己整合を確認 — **これだけでは subject を束縛しない**(便 68 F8 の反例)。 (2) **同じ record について D-4′ を再計算**する。**第一成分は top-level なら `subject_code_digest`、entry なら当該 entry の `content_digest`**。得た値を **その record の `subject_build_binding_digest`** と照合する。 (3) `build_record_present = false` の entry は **§2.35 の `[canonical-empty]` 表現に厳密一致すること**を確認する(QD-3)。**canonical empty でなければ [12]**(QD-4)。**宣言欄そのものの欠落は不備。** (4) **`present = true` と top-level に限り**、不一致または `subject_build_binding_digest` の欠落は `digest-mismatch` [12]。**`present = false` では ABSENT が唯一の PASS 形**であり、値が入っていれば QD-4 = [12]。**`build_record_present` 欄そのものの欠落は常に [12]。** **producer 申告のみの `build_root_id` / `subject_build_binding_digest` を受理しない。** **異 record 間の照合は行わない**(SB-2′・SB-6)。 |
| **I-0d** | **§2.5 の `build_attestation` が提出されている場合**、`output_digest == subject_code_digest` を検査する(BA-3)。**提出が無い場合、実生成関係は `UNKNOWN`** であって PASS ではない(BA-4)。 |
| **I-1** | 両 closure を四面へ落とす(`role` は別に保持)。 |
| **I-2** | **`declared_untrusted_inputs[]` の digest は universe から除外する**(集合を作る前に外す)。 |
| **I-3a** | **binary content 交差** $-$ `allowed_shared_tcb` → **非空なら [11]** |
| **I-3b** | **source artifact 交差** $-$ `allowed_shared_source_tcb` → **非空なら [11]** |
| **I-3d** | **【chg v4 新設・normative】build artifact 交差** $-$ `allowed_shared_build_tcb` → **非空なら [11]**(**共有 toolchain / build step / generator / build definition / pinned input を直接拾う**) |
| **I-3c′** | **family 交差**は **audit flag**。非空なら `family_overlap_flag` を receipt に記録するが、**単独では [11] を発しない**(M-3′)。**`allowed_shared_family[]` を差し引かない**(§5.2.1 FA-2) — allowlist は flag に添える acknowledged justification であって免除ではない。 |
| **I-5′** | **I-3a / I-3b / I-3d のいずれかが非空なら `INTEGRITY_STOP / shared-helper-detected` [11]。** |
| **I-6** | 空であっても、**差し引いた TCB 部分に `role = math-helper`(または H-3a′ の `code-generator`)が含まれていれば同じく [11]**。 |
| **I-8** | manifest の entry と実体の digest が食い違う、または H-1a″ の fixpoint 再計算で **未列挙 artifact / R-6 の未解決 digest** が見つかれば **`digest-mismatch` [12]**。 |

### 6.1 注記 N-1 — **三面は v3 の I-3c を包含する**(降格は弱化ではない){#subsumption}

> **主張.** `toolchain_digest` が mandatory かつ null 不可(E-6)であるとき、**v3 の family 交差(= lineage digest 交差)が非空ならば、v4 の build face 交差も非空である。**
> **証明.** v3 の family は $D_2$ の単射像だったから、family 交差が非空 $\iff$ ある entry 対 $(e_A,e_B)$ で $D_2(e_A)=D_2(e_B)$。sha256 の衝突を仮定しなければ preimage が一致し、とくに $\mathrm{toolchain\_digest}(e_A)=\mathrm{toolchain\_digest}(e_B)=:t$。E-6 より $t$ は null でなく、定義より $t\in \mathrm{build\_artifact\_set}(A)\cap \mathrm{build\_artifact\_set}(B)$。ゆえに build face 交差は非空。∎
> **系.** **v3 の I-3c を normative から外しても検出力は落ちない**(むしろ build face は $D_2$ 一致を要さないので、便 67 F7.2 の反例 — source が異なり toolchain だけ共有 — を新たに拾う)。**降格は弱化ではなく、主観判定を blocking path から除いたうえでの強化である。**

### 6.2 注記 N-2 — `build_record_present = false` の虚偽宣言に対する補償論法【本版新設】 {#false-absence}

> **問題**: SB-5 は build record の不在を明示宣言させるが、**producer が実際には build した artifact について `false` と宣言すれば、その entry は per-record binding(I-0c″ (2))の対象外になる。** この経路を何が拾うか。

**補償論法(番号つき)**:

1. **R-6 は独立の義務である(【本版で例外つきに弱める・QD-5′】)。** **`present = false` の leaf 自身の toolchain の再帰 entry 化を除き**、`build_record_present` の値に関わらず、**output-affecting な build-time artifact (toolchain・build step・code generator・build definition・pinned input)は closure entry へ昇格**しなければならない。**SB-5 の宣言は R-6 の免除ではない。**
2. **H-1a″ は昇格の完全性を検査する。** 受領側は fixpoint を再計算し、**R-6 の昇格対象で `content_digest` に解決されない digest があれば `digest-mismatch` [12]** を発する。
3. **昇格された build artifact は `binary_content_set` に入る。** ゆえに A と B が同じ build helper を共有していれば、**`build_record_present = false` と宣言していても I-3a(binary face)が交差を検出して [11]** を発する。**さらに §6 の build face(I-3d)は `toolchain_digest`・`build_step_digests[]`・`build_definition_blob_digest`・`pinned_input_digests[]` を直接集合にするので、これらを申告した entry については二重に拾う。**
4. **したがって虚偽の `false` 宣言が隠せるのは「その entry と自身の build との binding」だけであり、「共有 build helper の存在」は隠せない。** 前者は取り違え防止の層(SB-7 の限界内)、後者は独立性判定の層であり、**独立性判定は毀損されない。**

> **[historical]** **⚠ UNKNOWN(一級の結果として記録)**: 上の (2) は **受領側が closure を独立に再導出できること**を前提にする。**受領側が producer の attestation の内部整合しか検査できない場合、build record と R-6 昇格の両方を同時に省いた manifest は、紙上の機構では捕捉されない。****この部分は UNKNOWN であり、EP(external positive control)の検収項目へ送る** — **「H-1a″ の独立再導出が実際に可能か」を EP で確認するまで、本注記は「補償経路が存在する」までしか主張しない。**
> **過大主張の禁止**: 本注記を根拠に「虚偽宣言は検出される」と述べてはならない。**述べてよいのは「共有 build helper の検出は虚偽宣言に依存しない」まで。**

**段番号 [11] / [12] は governing spec §5.3.2 の `integrity_priority` を指す。verdict の決定と primary の選択は governing spec §5.3 の state machine が行う — 本稿は reason code を供給するだけである。**

---

## 7. manifest record の全体形 {#record}

```text
dependency_manifest = {
  schema_id, schema_digest,
  subject_id, subject_code_digest,

  # --- D-3 preimage(top-level にも必須)【chg v4】---
  build_definition_blob_digest,
  pinned_input_digests[],
  build_root_id,                    # 受領側が D-3 で再計算・照合
  subject_build_binding_digest,     # 受領側が D-4′ で再計算・照合(I-0c″)・第一成分 = subject_code_digest
  build_attestation,                # optional(§2.5)

  entries[]                         # §2 の manifest_entry(推移閉包・§3)
  declared_untrusted_inputs[]       # §5.3 — closure とは別欄
  allowed_shared_tcb[]              # §5.2・初期値 §5.4
  allowed_shared_source_tcb[]
  allowed_shared_build_tcb[]
  allowed_shared_family[]
  closure_attested = true           # H-1′
  build_promotion_attested = true   # R-6 の昇格が完了している【chg v4】
  produced_at_receipt
}
```

---

## 8. 適合宣言 {#conformance}

```text
conformance_record = {
  schema_id, schema_digest,
  covered_clauses = [BA-1, BA-2, BA-3, BA-4, BA-5, BC-1, BC-2, BC-3, CR-1, CR-10, CR-11, CR-2, 
                     CR-2′, CR-3, CR-5, CR-6, CR-7, CR-8, CR-8b, CR-9, D-R1, D-R2⁗, D-R3, D-R4, 
                     E-1, E-10′, E-1′, E-2, E-2′, E-3, E-4, E-5, E-6, E-7‴, E-8″, E-9′, FA-1, 
                     FA-2, FA-3, FA-4, H-1a″, H-1b, H-1c, H-1′, H-2, H-2a, H-2b″, H-2c, H-2d, 
                     H-3, H-3a, H-3a′, H-3b, H-3c, H-4, H-5, H-5a, H-5b, H-5c, H-5d′, H-5e, 
                     I-0c″, I-0d, I-0″, I-1, I-2, I-3a, I-3b, I-3c′, I-3d, I-5′, I-6, I-8, LA-1, 
                     LA-2, LA-3, M-1′, M-2′, M-3′, M-4, M-5, QD-1, QD-2, QD-3, QD-4, QD-5′, QD-6, 
                     QD-7, SB-1′, SB-2′, SB-3′, SB-4, SB-5, SB-6, SB-7, T-1″, T-2′, T-3, T-4, 
                     Y-1, Y-2, Y-3, Y-4, Y-4a, Y-4b, Y-4c, Y-4d]
  covered_procedure_checks = [D-1, D-2, D-3, D-4′, R-1, R-2, R-3, R-4, R-5, R-6, U-1, U-2, U-3, 
                              U-4]
  uncovered_checks = []
  uncovered_clauses = []
}
```
| # | 条項 |
|---|---|

```text
[registry-definition]                 # 正本: 文書表示と checker が同一の literal を読む
clause_id_regex = ^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴⁗]?)\*\* \|
check_id_regex  = (?<![A-Za-z0-9])(W-2′|D-[0-9]′?|R-[0-9]|U-[0-9]|P-[0-9]\.[0-9]|W-[0-9]|S[123]|C1)(?![A-Za-z0-9])
clause_scope    = [normative-clause-table]   # 差分表/fence/blockquote を除く table 行のみ
check_scope     = [normative-check-block] タグ付き fence + normative table 行 + 手続き fence
#                 (covered/uncovered/registry-definition/branch-contract/conformance の meta block は除外)
prime_class     = U+2032 U+2033 U+2034 U+2057   # exact match(ASCII 代用不可)
alternation_rule = long-token-first (W-2′ before W-[0-9])
fixture_1 = extract_clause of a C-6⁗ row yields exactly C-6⁗
fixture_2 = extract_check of W-2′ yields exactly W-2′
```

| **CR-1** | **`normative_clause_registry` の抽出規則**: 直上の `[registry-definition]` block の **`clause_id_regex` が唯一の正本**であり、**文書表示と checker は同一の literal を読む**(**checker は起動時にこの block の自己 digest を表示する**)。適用範囲は `clause_scope`。**`covered_clauses` はその全列挙。** 手続き段階のラベルは clause ではなく **check** なので **`covered_procedure_checks` に分けて全列挙**する(CR-5)。**【本版・B69-2】前版は prime class を `[′″‴]?` と凍結し quadruple prime `C-6⁗` を registry から落としていた**(checker 側が無断で `[′″‴⁗]?` へ拡張していた) — **文書側を昇格して両者を一本化。自認。** |
| **CR-2** | **range 表記(`C-1..C-5` 型)は禁止**する — prime / double-prime を落とすため(便 68 F13.3)。**** |
| **CR-3** | registry に無い ID を `covered` に書く、または registry の ID が両集合のどちらにも無い場合は**様式不適合**。 |
| **CR-2′** | **受領側は exact set equality で照合する**: `covered_clauses ∩ uncovered_clauses = ∅` かつ `covered_clauses ∪ uncovered_clauses = normative_clause_registry`。 |
| **CR-5** | **【chg v6 新設・内部ゲート FINDING-3】`procedure_check_registry` の抽出規則(機械的)**: 本稿の本文に現れる **check ラベル** (`D-<digit>`・`R-<digit>`・`U-<digit>`・`P-<digit>.<digit>`・`W-<digit>`・`W-2′`・`S1`・`S2`・`S3`・`C1`)の全体。**受領側は `covered_procedure_checks ∪ uncovered_checks = procedure_check_registry` かつ `∩ = ∅` を exact set equality で照合する。** |
| **CR-6** | **check は clause と同格の完全性保証を受ける。** **`covered_procedure_checks` から check を黙って落とすことは様式不適合**であり、CR-2′ と同じ扱いで検出される。 |
| **CR-7** | **check 側にも range 表記を禁止**する(CR-2 と同じ理由)。 |
| **CR-8** | **【本版新設・B70-2・F9.2 逐語】registry の抽出母体と coverage を分離する。** **`defined_procedure_checks` は明示タグ `[normative-check-block]` を持つ normative procedure block と normative table 行だけから抽出**する。**`covered_procedure_checks` は conformance record から抽出**する。**禁止**: `covered_procedure_checks` / `uncovered_checks` / `[registry-definition]` / `[branch-contract]` の各 meta block を `defined_procedure_checks` の抽出母体へ入れること。 |
| **CR-8b** | **【本版新設・裁定 91】per-document scope**: 各文書の `covered_procedure_checks` は、**その文書に normative 定義がある check だけ**を列挙する(dependency manifest = `D-*` / `R-*` / `U-*`、verifier contract = `P-*` / `W-*` / `S1`–`S3` / `C1`)。**相互の義務は clause 散文(C-6⁗ 等)で表現済み**であり、**他文書側の概念を covered に混入させない**(Sol 便 69 F6 末尾「registry scope 案で併せて除く」の履行)。 |
| **CR-9** | **【本版新設】前版の欠陥(自認)**: 抽出母体が conformance fence を含んでいたため、**covered に未知 ID を書いた瞬間それ自身が registry の一員になり**、CR-4 の「registry に無い ID を covered に書けば不適合」が成立しなかった。**独立 probe で未知 ID を covered に足しても equality が true のまま**になり、さらに **coverage list だけが生成した幽霊 ID が 1 件**存在した。 |
| **CR-10** | **【本版新設・F11.2 逐語】registry は三層とし、層ごとに owner を分ける。** **`defined_checks` = 契約本文** / **`claimed_covered` = conformance record** / **`implemented_checks` = 受領側 executable inventory**。**freeze 時は前二者の exact equality**、**実装 receipt 時は三者の exact equality** を要求する。 |
| **CR-11** | **CR-5〜CR-7 は `implemented_checks` 層が未成立**である(受領側 executable inventory が存在しない)。**現状の主張は「defined = claimed_covered」まで**であり、**三者 equality は `[current-unknown]`** として receipt / EP へ送る。 |
> **[historical] CR-2**: v4 の `M-1'..M-5`・`R-1..R-6`・`Y-1..Y-3`・`U-1..U-4` は range だった・自認。
> **[historical] CR-6**: v5 は clause 側にしか母集合規則を持たず、「procedure check への分離」が事実上の義務の格下げになっていた**(内部ゲート FINDING-3・**自認**)。


**`uncovered_clauses` が非空の manifest を「様式適合」と呼ばない。** 部分適合は `partial manifest / UNKNOWN` として扱い、**独立性の証跡としては使えない。**

---

## 9. live authority refs(機械可読)【F13.1・裁定 83】{#live-authority}

```text
live_authority_refs[] = [
  { artifact_id: "mb/ninfty-stage2-predicate/v15",
    digest_or_receipt_slot: "receipt:governing_spec_digest",
    anchor: "§4.4 dependency_manifest_schema_id / §5.3.2 integrity_priority" }
]

historical_quotation_refs[] = [
  { artifact_id: "mb/dependency-manifest/v1..v9",     note: "版履歴・差分表・自認文のみ" },
  { artifact_id: "mb/ninfty-verifier-contract/v1..v9", note: "差分表・自認文のみ" },
  { artifact_id: "mb/ninfty-stage2-predicate/v5..v14", note: "差分表・自認文のみ" }
]
```

| # | 条項 |
|---|---|
| **LA-1** | **本稿の live な版束縛は §0 header の `governing_spec` 1 箇所と上の block のみ。** 本文の他の spec 参照は**版中立**(「governing spec §…」)である。 |
| **LA-2** | **release lint は本文の version token を走査し、`live_authority_refs[]` に無い旧版 ID が live 文に現れたら fail させる。** `historical_quotation_refs[]` の ID は**差分表の行・`supersedes` 行・版履歴 blockquote・明示の自認 blockquote のみ**に現れてよい。**【chg v6 で明文化】operative 本文の行に歴史 token を置いてはならない** — 「記録」「自認」等の語を含むだけの operative 行を除外域と見なすことを禁じる(内部ゲート FINDING-4)。**除外域は構造(差分表・blockquote・コードフェンス境界)で定義し、語の部分一致で定義しない。** |
| **LA-3** | **【[sweep-def]・現行有効な lint 契約】** 本行は `[historical]` ではなく、**現在の release lint が従う sweep 対象定義**である。定義は直下の `sweep_definition` block を正本とする。 |

```text
sweep_definition = {                      # [sweep-def] 現行有効
  self_artifact   = "mb/dependency-manifest/*",
  self_alias      = "manifest v<N>",
  other_artifacts = [ "mb/ninfty-stage2-predicate/*", "mb/ninfty-verifier-contract/*" ],
  other_aliases   = [ "spec v<N>", "contract v<N>" ],
  bare_token      = "v<N> + 助詞",       # 【chg v<N> …】 のみ allowlist
  current_version = "v10",
  historical_upper_bound = "v9",   # = current - 1(script v3 が自動照合)
  rationale = "自版だけを見る sweep は不十分 — 便 68 F6 が反証した失敗型"
}
```

