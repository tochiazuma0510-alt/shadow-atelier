# `mb/dependency-manifest/v5` — implementation dependency closure の記録様式

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 83)。v4 を supersede。**
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
schema_id     = "mb/dependency-manifest/v5"
schema_digest = <64 hex: 本稿 exact blob の sha256 — receipt が記入>
encoding      = UTF-8, LF, no BOM, no normalization
governing_spec = "mb/ninfty-stage2-predicate/v10"
governing_spec_digest = <64 hex: governing spec の digest — receipt が記入>
supersedes    = "mb/dependency-manifest/v4"
supersedes_digest = 378f30c84f79bf5d18055ccb824f21e65b3efd11a1d947178e94233f74412d11   # 監査 FAIL の candidate
supersedes_v3     = 1a8d1f2147178b49d5fe81da625256762a9e9dafd1a963b57d554bcf97c7b7dd
```

> **【hash 順序・便 66 F11 / 便 67 F11】** 非循環な順序は **manifest → contract → spec → receipt**。**本稿は下流(contract / spec)の digest を pin しない。** governing spec は **ID で束縛し digest は receipt 側**。
> **【fail-closed】header の governing spec は本稿起草時点で未発行の後継である。receipt がその実在と digest を束縛するまで、本稿を operative として扱ってはならない。**

**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。
**優先関係**: 本稿と governing spec が矛盾した場合、**governing spec が優先**する。

---

## 0.1 v4 → v5 差分【裁定 83】

| ID | v4 | v5 | 出所 |
|---|---|---|---|
| **Q1(F8)** | D-3 の preimage は `build_definition_blob_digest` と `pinned_input_digests[]` のみで、**`subject_code_digest` が一度も計算に現れない**。top-level record は両者を並べるだけで**結ぶ等式が無く**、R-1 は subject $X$ 自身を `content_digest` とする entry を要求しないので **I-0c の「該当 entry」も subject output を一意に指定しない**。**紙上反例(Sol F8 を条文内に採録)**: 任意の $c$・$b$・$P$ に対し $r:=H(\{b,P\})$ とすると、受領側は $r$ の自己整合を確認できるが **$c$ を別の $c'$ に差し替えても I-0c は同じ結果を返す**。**自認** | **§2.4 に `subject_build_binding_digest` を frozen preimage の mandatory 欄として新設**(D-4)。**top-level subject と対応 build record の双方で受領側再計算・照合**(I-0c′ を「$c$ が計算に現れる」形へ書き直し)。**上位層 `build_attestation` は optional schema として定義**し、**実生成関係を主張する場合に限り必須**と効力を明記(§2.5) | 便 68 F8・F13.2 |
| **Q2(F9)** | 冒頭の要約と §5.2 heading が **「五欄」**と書く一方、実際の宣言・§5.4 の初期値・T-1′・契約 C-3′/C-5′/C-8′ はすべて**四欄**。H-5c が omitted field を暗黙の空集合にも暗黙の許可にも読ませないので、**算数 typo として放置できない**。**自認** | **2 箇所とも「四欄」へ**。**`allowed_shared_family[]` は欄を保持**し、意味を **「`family_overlap_flag` への acknowledged justification list(audit 専用・非 blocking・I-3c′ は差し引かない)」**に一意化(§5.2・§6) | 便 68 F9・裁定 83 |
| **Q3(F13.1)** | live 参照の版 token が本文に散在し、機械 lint できなかった | **§9 に `live_authority_refs[]` / `historical_quotation_refs[]` の機械可読 block を新設**。**本文の版束縛は header 1 箇所に集約**し、他は版中立の節参照へ | 便 68 F13.1・裁定 83 |

---

## 0.1.1 v3 → v4 差分【B67-2】(v4 から継承・変更なし)

| ID | v3 | v4 | 出所 |
|---|---|---|---|
| **P1(F7.1)** | D-3 を「凍結された導出規則」として書いたが、**`build_definition_blob_digest` と `pinned_input_digests[]` が `manifest_entry` にも top-level にも無く**、**D-R2 / I-0 の再計算義務も D-1 / D-2 にしか及んでいなかった**。ゆえに **`build_root_id` は依然 producer の申告値**で、「D-1〜D-3 を凍結し受領側が再計算」という要旨を D-3 について満たしていない。**自認** | **D-3 の preimage を record 欄に mandatory 化**(§2.1 E-9)。**D-R2 / I-0 の再計算義務に D-3 を含める**(D-R2′・I-0′)。**`build_root_id` の subject code への binding も受領側が検査**(I-0c) | 便 67 F7.1 |
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
| **build 経路(toolchain / build step / build definition)の閉鎖** | **§2.1 E-9・§3 R-6・§6 I-3d** |
| helper の範囲 | §5.1(`role` 分類・H-3a) |
| 共有を許す trusted base と初期値 | §5.2・§5.4(**四欄すべて実値 `[]`**・**v4 の「五欄」は算数 typo・自認**) |
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

  # --- build_root preimage(すべて必須・§2.1 E-9)【v4 新設】---
  build_definition_blob_digest,  # build 定義そのものの exact blob digest
  pinned_input_digests[],        # sorted・deduplicated
  subject_build_binding_digest,  # = D-4 の再計算値と一致すること【v5 新設・§2.4】

  # --- 受領側が再計算する導出値(producer の申告値は参照値にすぎない)---
  source_closure_digest,         # = D-1 の再計算値と一致すること
  implementation_lineage_digest, # = D-2 の再計算値と一致すること
  build_root_id,                 # = D-3 の再計算値と一致すること【v4 で再計算対象へ】
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
| **E-9** | **【v4 新設】`build_definition_blob_digest` と `pinned_input_digests[]`(sorted・deduplicated)も mandatory。** これが **D-3 の preimage の全体**である。 |
| **E-10** | **【v5 新設】`subject_build_binding_digest` は mandatory**。preimage は §2.4 D-4 の 3 要素(`subject_code_digest`・`build_definition_blob_digest`・`pinned_input_digests[]`)。**build record を持つ各 entry と top-level record の双方に置く。** |
| **E-7″** | **E-5・E-6・E-9・E-10 が D-1 / D-2 / D-3 / D-4 すべての preimage を尽くす。** 受領側はこれだけから §2.2 の三 hash を再計算できなければならない。**再計算不能な entry は独立性の証跡として使えない。** |
| **E-8″** | **producer が申告した `source_closure_digest` / `implementation_lineage_digest` / `build_root_id` / `subject_build_binding_digest` は参照値でしかない。** 受領側の再計算値と食い違えば `digest-mismatch` [12]。 |

### 2.2 導出規則(**凍結**・受領側が再計算)【D-3 を含む】{#derivation}

```text
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

D-4  subject_build_binding_digest =                          # 【v5 新設】
       sha256( canonical_serialize( {
           "subject":          subject_code_digest,
           "build_definition": build_definition_blob_digest,
           "pinned_inputs":    sort(dedup(pinned_input_digests[]))
       } ) )

canonical_serialize = UTF-8 / LF / key 昇順 / 配列は明示順 / 空白なし
```

| # | 条項 |
|---|---|
| **D-R1** | **D-1〜D-3 は本稿で凍結された規則であり、producer 側の裁量を含まない。** |
| **D-R2″** | **【v5 で D-4 を追加】受領側は preimage から D-1・D-2・D-3・D-4 の四つすべてを再計算して照合する。** v3 は D-1・D-2 のみ、v4 は D-3 までしか要求していなかった(**自認**)。 |
| **D-R3** | **preimage が一致すれば同一 lineage と判定する。** ID・名前・版文字列の相違は判定に影響しない — **ID の付け替えでは逃げられない。** |
| **D-R4** | **【v4】hash の再計算は「申告 preimage と申告 aggregate の整合」を示すだけで、preimage の完全性や build への実接続を自動では証明しない**(便 67 F7 末尾)。ゆえに **R-6 の closure 昇格**と **I-0c の binding 検査**を併置する。 |

### 2.4 `subject_build_binding_digest` — **identity binding 層**【Q1】{#subject-binding}

> **⚠ v4 の欠陥(自認)**: D-3 の preimage に **`subject_code_digest` が無く**、top-level の `subject_code_digest` と `build_root_id` を**結ぶ等式が存在しなかった**。R-1 は subject $X$ 自身を entry にする規則ではないので、**I-0c の「該当 entry」も subject output を一意に指定しない**。
> **反例(便 68 F8 を逐語採録)**: 任意の `subject_code_digest` $c$、任意の build definition $b$、pinned inputs $P$ を選び $r:=H(\{b,P\})$ とする。top-level と該当 entry に同じ $b,P,r$ を置けば、**受領側は D-3 を再計算して $r$ の自己整合を確認できるが、$c$ は計算に一度も現れない**。**ゆえに別の $c'$ に差し替えても I-0c は同じ結果を返す。** R-6 は $b,P$ を closure へ昇格するが、$\mathrm{Build}(b,P)=c$ の binding を追加しない。

| # | 条項 |
|---|---|
| **SB-1** | **`subject_build_binding_digest` は §2.2 D-4 で定義される frozen preimage の mandatory 欄である。** preimage は $\{$`subject_code_digest`, `build_definition_blob_digest`, `pinned_input_digests[]`$\}$。 |
| **SB-2** | **top-level record と、対応する build record を持つ各 entry の双方に置く。** 受領側は**両方**を D-4 で再計算し、申告値および相互に照合する(I-0c′)。 |
| **SB-3** | **これにより `subject_code_digest` が binding の計算に現れる。** $c$ を差し替えれば `subject_build_binding_digest` が変わるので、Q1 の反例は閉じる。 |
| **SB-4** | **【効力の正直な宣言】本層が保証するのは identity binding(取り違え防止)までである。** 「この build が実際に $c$ を生成した」という**実生成関係は主張しない** (**hash tuple だけでは実生成関係を証明しない** — 便 68 F8・D-R4)。実生成を主張するには §2.5 の上位層が要る。 |

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
| **M-4** | **v2 の `generator_lineage_id` は廃止**。**producer 可変の識別子を lineage 判定に用いない。** |
| **M-5** | **merge のみ可能・split 不可**という単調性により、**family の追加操作は判定を緩めない**(緩める方向の操作が存在しない)。 |

| # | 条項(v3 から継続) |
|---|---|
| **E-1** | **exact blob の identity は `content_digest` のみで決まる。** `source_ref`・path・パッケージ名・版名は identity に使わない。 |
| **E-1′** | 系列の identity は preimage から §2.2 で導かれる。**交差検査は §6 の各面に対して行う。** |
| **E-2** | 同じ blob が複数経路で到達しても entry は 1 つ。 |
| **E-2′** | **`depth` は記録欄であって合否判定に使わない。** |
| **E-3** | `role` の欠落は不備。**未分類 entry を TCB とみなす既定を置かない。** |
| **E-4** | preimage 欄(E-5・E-6・E-9)の欠落は**独立性の主張を無効にする**。 |

---

## 3. 推移的閉包の生成規則 {#closure-rules}

```text
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

  R-6  【v4 新設】output-affecting な build-time artifact —
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
**【v4】`code-generator` を追加** — R-6 で closure へ昇格する build-time artifact のうち、**出力コードを生成するもの**。

| # | 条項 |
|---|---|
| **H-3** | `allowed_shared_tcb[]` は frozen content digest で列挙し `role` を付す。**`role = math-helper` を TCB に入れることを禁止する。** |
| **H-3a** | **math-helper の判定基準**: 出力が「どの数学的対象が等しいか」に影響しうる処理はすべて math-helper — **canonicalizer・ideal 演算・Gröbner / normal form / reduction・divisor 正規化・partition 計算・多項式演算・体演算**。**迷えば math-helper**(既定は禁止側)。 |
| **H-3a′** | **【v4】`code-generator` が math-helper を生成する場合、その generator も math-helper と同じ扱い**(TCB 禁止)。**生成物が数学処理なら、生成器の共有は共通 bug 経路である。** |
| **H-3b** | `serialization` / `hash-primitive` / `runtime` / `cas-io` / `build-tool` は TCB 候補。**自動ではなく明示列挙して初めて差し引かれる。** |
| **H-3c** | `data-table` は**原則 TCB に入れない**。 |

### 5.2 TCB の宣言様式(**四欄**)【Q2 で訂正】

```text
allowed_shared_tcb[]        = [ { content_digest, role, justification, frozen_at_receipt } ]
allowed_shared_source_tcb[] = [ { source_artifact_digest, role, justification, frozen_at_receipt } ]
allowed_shared_build_tcb[]  = [ { build_artifact_digest, role, justification, frozen_at_receipt } ]  # v4 新設
allowed_shared_family[]     = [ { implementation_family_id, role, justification, frozen_at_receipt } ] # audit 専用(§5.2.1)
```
| # | 条項 |
|---|---|
| **H-5** | **追加は追加側に挙証責任。** 追加は freeze bundle の変更であり **receipt を要する**。 |
| **H-5a** | receipt 前の追加提案は候補であって効力を持たない。 |
| **H-5b** | 縮む方向には receipt を要しない。 |
| **H-5c** | **省略を暗黙の空集合とも暗黙の許可とも読ませない** — §5.4 が実値を宣言する。 |
| **H-5d′** | **各欄は独立**。content 側を許しても source / build / family 側は自動的には許されない。 |
| **H-5e** | **【v5・Q2】欄数は四である**(`allowed_shared_tcb` / `_source_tcb` / `_build_tcb` / `_family`)。**v4 の冒頭要約と §5.2 heading が「五欄」と書いていたのは誤り・自認。** |

#### 5.2.1 `allowed_shared_family[]` の意味の一意化【Q2・裁定 83】{#family-allowlist}

| # | 条項 |
|---|---|
| **FA-1** | **`allowed_shared_family[]` は `family_overlap_flag` への acknowledged justification list である。** |
| **FA-2** | **audit 専用・非 blocking。** I-3c′ は**この集合を差し引かない** — family 交差が非空なら、allowlist に載っていても `family_overlap_flag` は記録される。**載っているのは「authority が承知している」ことの記録**であって免除ではない。 |
| **FA-3** | **欄は保持する**(削除しない)。理由: 契約 C-3′/C-5′/C-8′ と receipt が **四欄の arity** を前提にしており、欄を削ると下流の schema arity が崩れる(裁定 83)。 |
| **FA-4** | **初期値 `[]`。** 空である限り観測される挙動は v4 と同一(I-3c′ は常に flag を記録する)。 |

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
| **Y-4d** | **【v4】build-time artifact は入力クラスに置けない**(U-1 違反 — 手続きとして実行される)。**R-6 により必ず closure 側。** |

### 5.4 初期 TCB の実値 {#initial-tcb}

```text
allowed_shared_tcb        = []      # 空集合(実値・省略ではない)
allowed_shared_source_tcb = []      # 空集合
allowed_shared_build_tcb  = []      # 空集合【v4 新設・実値】
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
build_artifact_set(X)  = ⋃ { entry.toolchain_digest }
                       ∪ ⋃ { entry.build_step_digests[] }
                       ∪ ⋃ { entry.build_definition_blob_digest }
                       ∪ ⋃ { entry.pinned_input_digests[] }          # v4 新設
authority_family_set(X) = { entry.implementation_family_id }          # audit flag
```

| # | 手順 |
|---|---|
| **H-4** | **交差の値は producer の自己申告を信じない。receipt 受領側が canonical digest 集合から導出して再計算する。** |
| **I-0′** | **受領側はまず §2.2 の D-1・D-2・D-3 を preimage から再計算し、entry の申告値と照合する**(不一致 → [12]・E-8′)。**再計算不能(preimage 欠落)なら E-4 により独立性主張は無効 → [11]。** |
| **I-0c′** | **【v5 で書き直し・Q1】`subject_code_digest` が計算に現れる形で binding を検査する。** 手順: (1) D-3 を再計算し `build_root_id` の自己整合を確認 — **これだけでは $c$ を束縛しない**(便 68 F8 の反例)。 (2) **D-4 を top-level record について再計算**し `subject_build_binding_digest` と照合。 (3) **D-4 を対応 build record を持つ各 entry についても再計算**し、**top-level の値と相互照合**。 (4) いずれかが不一致、または `subject_build_binding_digest` が欠落していれば `digest-mismatch` [12]。 **producer 申告のみの `build_root_id` / `subject_build_binding_digest` を受理しない。** |
| **I-0d** | **§2.5 の `build_attestation` が提出されている場合**、`output_digest == subject_code_digest` を検査する(BA-3)。**提出が無い場合、実生成関係は `UNKNOWN`** であって PASS ではない(BA-4)。 |
| **I-1** | 両 closure を四面へ落とす(`role` は別に保持)。 |
| **I-2** | **`declared_untrusted_inputs[]` の digest は universe から除外する**(集合を作る前に外す)。 |
| **I-3a** | **binary content 交差** $-$ `allowed_shared_tcb` → **非空なら [11]** |
| **I-3b** | **source artifact 交差** $-$ `allowed_shared_source_tcb` → **非空なら [11]** |
| **I-3d** | **【v4 新設・normative】build artifact 交差** $-$ `allowed_shared_build_tcb` → **非空なら [11]**(**共有 toolchain / build step / generator / build definition / pinned input を直接拾う**) |
| **I-3c′** | **family 交差**は **audit flag**。非空なら `family_overlap_flag` を receipt に記録するが、**単独では [11] を発しない**(M-3′)。**`allowed_shared_family[]` を差し引かない**(§5.2.1 FA-2) — allowlist は flag に添える acknowledged justification であって免除ではない。 |
| **I-5′** | **I-3a / I-3b / I-3d のいずれかが非空なら `INTEGRITY_STOP / shared-helper-detected` [11]。** |
| **I-6** | 空であっても、**差し引いた TCB 部分に `role = math-helper`(または H-3a′ の `code-generator`)が含まれていれば同じく [11]**。 |
| **I-8** | manifest の entry と実体の digest が食い違う、または H-1a″ の fixpoint 再計算で **未列挙 artifact / R-6 の未解決 digest** が見つかれば **`digest-mismatch` [12]**。 |

### 6.1 注記 N-1 — **三面は v3 の I-3c を包含する**(降格は弱化ではない){#subsumption}

> **主張.** `toolchain_digest` が mandatory かつ null 不可(E-6)であるとき、**v3 の family 交差(= lineage digest 交差)が非空ならば、v4 の build face 交差も非空である。**
> **証明.** v3 の family は $D_2$ の単射像だったから、family 交差が非空 $\iff$ ある entry 対 $(e_A,e_B)$ で $D_2(e_A)=D_2(e_B)$。sha256 の衝突を仮定しなければ preimage が一致し、とくに $\mathrm{toolchain\_digest}(e_A)=\mathrm{toolchain\_digest}(e_B)=:t$。E-6 より $t$ は null でなく、定義より $t\in \mathrm{build\_artifact\_set}(A)\cap \mathrm{build\_artifact\_set}(B)$。ゆえに build face 交差は非空。∎
> **系.** **v3 の I-3c を normative から外しても検出力は落ちない**(むしろ build face は $D_2$ 一致を要さないので、便 67 F7.2 の反例 — source が異なり toolchain だけ共有 — を新たに拾う)。**降格は弱化ではなく、主観判定を blocking path から除いたうえでの強化である。**

**段番号 [11] / [12] は governing spec §5.3.2 の `integrity_priority` を指す。verdict の決定と primary の選択は governing spec §5.3 の state machine が行う — 本稿は reason code を供給するだけである。**

---

## 7. manifest record の全体形 {#record}

```text
dependency_manifest = {
  schema_id, schema_digest,
  subject_id, subject_code_digest,

  # --- D-3 preimage(top-level にも必須)【v4】---
  build_definition_blob_digest,
  pinned_input_digests[],
  build_root_id,                    # 受領側が D-3 で再計算・照合
  subject_build_binding_digest,     # 受領側が D-4 で再計算・照合(I-0c′)【v5】
  build_attestation,                # optional(§2.5)

  entries[]                         # §2 の manifest_entry(推移閉包・§3)
  declared_untrusted_inputs[]       # §5.3 — closure とは別欄
  allowed_shared_tcb[]              # §5.2・初期値 §5.4
  allowed_shared_source_tcb[]
  allowed_shared_build_tcb[]
  allowed_shared_family[]
  closure_attested = true           # H-1′
  build_promotion_attested = true   # R-6 の昇格が完了している【v4】
  produced_at_receipt
}
```

---

## 8. 適合宣言 {#conformance}

```text
conformance_record = {
  schema_id, schema_digest,
  covered_clauses = [BA-1, BA-2, BA-3, BA-4, BA-5, CR-1, CR-2, CR-3, D-R1, D-R2″, D-R3, D-R4, 
                     E-1, E-10, E-1′, E-2, E-2′, E-3, E-4, E-5, E-6, E-7″, E-8″, E-9, FA-1, FA-2, 
                     FA-3, FA-4, H-1a″, H-1b, H-1c, H-1′, H-2, H-2a, H-2b″, H-2c, H-2d, H-3, 
                     H-3a, H-3a′, H-3b, H-3c, H-4, H-5, H-5a, H-5b, H-5c, H-5d′, H-5e, I-0c′, 
                     I-0d, I-0′, I-1, I-2, I-3a, I-3b, I-3c′, I-3d, I-5′, I-6, I-8, LA-1, LA-2, 
                     LA-3, M-1′, M-2′, M-3′, M-4, M-5, P4, SB-1, SB-2, SB-3, SB-4, T-1″, T-2′, 
                     T-3, T-4, Y-1, Y-2, Y-3, Y-4, Y-4a, Y-4b, Y-4c, Y-4d]
  covered_procedure_checks = [D-1, D-2, D-3, D-4, U-1, U-2, U-3, U-4]
  uncovered_clauses = []
}
```
| # | 条項 |
|---|---|
| **CR-1** | **`normative_clause_registry` の抽出規則(機械的)**: 本稿の **normative table 行 `| **ID** | … |` に現れる clause ID の全体**。この規則は正規表現 `^\| \*\*([A-Z][A-Za-z0-9\-\.]*[′″‴]?)\*\* \|` で再現でき、**受領側が本文から再生成できる**。**`covered_clauses` はその全列挙。** 手続き段階のラベル(`P-0.*`・`P-1.*`・`W-*`・`S1`–`S3`・`D-*`・`U-*`)は clause ではなく **check** なので **`covered_procedure_checks` に分けて全列挙**する。 |
| **CR-2** | **range 表記(`C-1..C-5` 型)は禁止**する — prime / double-prime を落とすため(便 68 F13.3)。**v4 の `M-1'..M-5`・`R-1..R-6`・`Y-1..Y-3`・`U-1..U-4` は range だった・自認。** |
| **CR-3** | registry に無い ID を `covered` に書く、または registry の ID が両集合のどちらにも無い場合は**様式不適合**。 |

**`uncovered_clauses` が非空の manifest を「様式適合」と呼ばない。** 部分適合は `partial manifest / UNKNOWN` として扱い、**独立性の証跡としては使えない。**

---

## 9. live authority refs(機械可読)【F13.1・裁定 83】{#live-authority}

```text
live_authority_refs[] = [
  { artifact_id: "mb/ninfty-stage2-predicate/v10",
    digest_or_receipt_slot: "receipt:governing_spec_digest",
    anchor: "§4.4 dependency_manifest_schema_id / §5.3.2 integrity_priority" }
]

historical_quotation_refs[] = [
  { artifact_id: "mb/dependency-manifest/v4", digest: "378f30c8...(supersedes)" },
  { artifact_id: "mb/dependency-manifest/v3", digest: "1a8d1f21...(supersedes)" },
  { artifact_id: "mb/dependency-manifest/v2", note: "§0.1 差分表の引用のみ" }
]
```

| # | 条項 |
|---|---|
| **LA-1** | **本稿の live な版束縛は §0 header の `governing_spec` 1 箇所と上の block のみ。** 本文の他の spec 参照は**版中立**(「governing spec §…」)である。 |
| **LA-2** | **release lint は本文の version token を走査し、`live_authority_refs[]` に無い旧版 ID が live 文に現れたら fail させる。** `historical_quotation_refs[]` の ID は差分表・supersedes・自認文にのみ現れてよい。 |
| **LA-3** | **sweep の対象定義**: 自 artifact の全版 token("manifest v1..v5"/`mb/dependency-manifest/v*`)と、**他 2 文書の全版 token**("spec v5..v10"/`mb/ninfty-stage2-predicate/v*`・"contract v1..v5"/`mb/ninfty-verifier-contract/v*`)。**自版だけを見る sweep は不十分**(便 68 F6 が反証した失敗型)。 |
