# `mb/dependency-manifest/v3` — implementation dependency closure の記録様式

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 79)。v2 を supersede。**
**この文書は `mb/ninfty-stage2-predicate/v8` §4.4 の `dependency_manifest_schema_id` が指す実体である。**

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
schema_id     = "mb/dependency-manifest/v3"
schema_digest = <64 hex: 本稿 exact blob の sha256 — receipt が記入>
encoding      = UTF-8, LF, no BOM, no normalization
governing_spec = "mb/ninfty-stage2-predicate/v8"
governing_spec_digest = <64 hex: v8 の digest — receipt が記入>
supersedes    = "mb/dependency-manifest/v2"
supersedes_digest = c485e0166da1aa4b9c34474dbb49d1ed18d4c3f1c29ccba14614dbd4dcbb56d2   # 監査 FAIL の candidate
```

> **【hash 順序・便 66 F11】** 非循環な順序は **manifest → contract → spec → receipt**。**本稿は spec の digest を pin しない**(governing spec は **ID で束縛し digest は receipt 側**)。**spec v8 が本稿の exact digest を pin する。**
> **【fail-closed】`mb/ninfty-stage2-predicate/v8` は本稿起草時点で未発行の後継である。receipt が v8 の実在と digest を束縛するまで、本稿を operative として扱ってはならない。**

**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。
**優先関係**: 本稿と governing spec が矛盾した場合、**governing spec が優先**する。

---

## 0.1 v2 → v3 差分

| ID | v2 | v3 | 出所 |
|---|---|---|---|
| **B66-1** | $\mathrm{lineage}=H(\mathrm{source\_closure\_digest},\ \mathrm{generator\_lineage\_id})$ としたが、**`generator_lineage_id` の mint authority・一意性・受領側 recomputation が無い**。**producer が両側に別の ID を書くだけで、同一 source を二 toolchain で build した rebuild が content 交差も lineage 交差も空にできる**(H-2b′ が捕捉したい事故がそのまま PASS)。さらに entry は aggregate `source_closure_digest` しか持たず、**受領側は preimage を再構成できないので producer の aggregate を再計算できない**。**自認** | **preimage を mandatory 化**: `source_artifact_digests[]`(sorted exact source blob digests)と `build_step_digests[]`・`toolchain_digest` を entry に列挙し、**§2.2 に導出規則を凍結**して**受領側が hash を再計算**する。**`generator_lineage_id` を廃止**し、**`implementation_family_id` は receipt authority が mint**(producer 不可)。**判定は preimage 一致で行うので ID の付け替えでは逃げられない。** **三集合の交差を別々に検査**(§6 I-3a/I-3b/I-3c — 便 66 F13 の発案を採用) | 便 66 F6・F13 |
| **B66-2(F7)** | `governing_spec = "mb/ninfty-stage2-predicate/v6"` を **hard-pin** し、冒頭と §6 末尾も v6 を authority としていた。**v7 contract が `declared_untrusted_inputs[]` に要求する governing spec blob と、manifest の governing spec blob が別物**になる(**exact bundle の型不一致**) | **後継 spec(v8)へ同期**。**digest は receipt 側**(F11 の非循環順序)。**冒頭・§6 末尾も v8 authority へ。** **自認** | 便 66 F7 |

---

## 1. この様式が閉じる未定義項 {#purpose}

| 未定義項 | 本稿 |
|---|---|
| manifest が直接依存だけか、**推移的閉包**か | §3(R-1〜R-5・H-1′) |
| 別名・別 path・薄い wrapper の同一性 | §2・§4(H-2・H-2a) |
| **rebuild lineage** と exact blob identity の接続 | §2.1・§2.2・§4(H-2b″)・§6(I-3b/I-3c) |
| **lineage の producer 自己申告回避** | §2.2(mint authority と再計算規則)・§4(H-2d) |
| helper の範囲 | §5.1(`role` 分類・H-3a) |
| 共有を許す trusted base と初期値 | §5.2・§5.4 |
| 共有 input と共有 implementation の型分離 | §5.3(Y 系・U 系) |

---

## 2. entry の型 {#entry-type}

```text
manifest_entry = {
  content_digest,                # 必須・64 hex・exact blob の identity
  role,                          # §5.1 の分類(必須)

  # --- lineage preimage(すべて必須・§2.1)【B66-1】---
  source_artifact_digests[],     # sorted・deduplicated・exact source blob digests
  toolchain_digest,              # toolchain 実体の exact blob digest
  build_step_digests[],          # ordered digest 列(build 手順そのもの)

  # --- 受領側が再計算する導出値(producer の申告値は参照しない)---
  source_closure_digest,         # = §2.2 D-1 の再計算値と一致すること
  implementation_lineage_digest, # = §2.2 D-2 の再計算値と一致すること
  implementation_family_id,      # receipt authority が mint(producer 不可・§2.3)

  provenance = { build_root_id, source_ref },   # source_ref は identity に使わない
  outgoing_dependency_attestation,              # §3.1
  depth,                                        # 記録のみ
  reached_via[]
}
```

### 2.1 preimage の列挙義務【B66-1】{#preimage}

| # | 条項 |
|---|---|
| **E-5** | **`source_artifact_digests[]` は mandatory** であり、**aggregate ではなく構成要素の列**である。sorted・deduplicated・exact source blob(pre-build)の digest。 |
| **E-6** | **`toolchain_digest` と `build_step_digests[]` も mandatory。** 前者は toolchain 実体の exact blob digest(名前・版文字列ではない)、後者は build 手順の digest の**順序つき列**。 |
| **E-7** | **これら 3 欄が lineage hash の preimage の全体である。** 受領側はこれだけから §2.2 の hash を再計算できなければならない。**再計算不能な entry は独立性の証跡として使えない。** |
| **E-8** | **producer が申告した `source_closure_digest` / `implementation_lineage_digest` は参照値でしかない。** 受領側の再計算値と食い違えば `digest-mismatch` [12]。 |

### 2.2 導出規則(**凍結**・受領側が再計算)【B66-1】{#derivation}

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
           "pinned_inputs":    sort(pinned_input_digests[])
       } ) )

canonical_serialize = UTF-8 / LF / key 昇順 / 配列は明示順 / 空白なし
```

| # | 条項 |
|---|---|
| **D-R1** | **D-1〜D-3 は本稿で凍結された規則であり、producer 側の裁量を含まない。** |
| **D-R2** | **受領側は preimage から D-1・D-2 を再計算して照合する。** |
| **D-R3** | **preimage が一致すれば同一 lineage と判定する。** ID・名前・版文字列の相違は判定に影響しない — **ID の付け替えでは逃げられない。** |

### 2.3 `implementation_family_id` の mint authority【B66-1】{#mint}

| # | 条項 |
|---|---|
| **M-1** | **`implementation_family_id` は receipt authority が mint する。producer は自分で選べない。** |
| **M-2** | **mint 規則**: receipt authority は §2.2 D-2 の `implementation_lineage_digest` を**受領側で再計算**し、**同じ値には同じ family ID を割り当てる**(決定的・単射)。 |
| **M-3** | **producer が提出した `implementation_family_id` は照合対象**であり、authority の割当と食い違えば `digest-mismatch` [12]。 |
| **M-4** | **v2 の `generator_lineage_id` は廃止**する。**producer 可変の識別子を lineage 判定に用いない。** |

| # | 条項(v2 から継続) |
|---|---|
| **E-1** | **exact blob の identity は `content_digest` のみで決まる。** `source_ref`・path・パッケージ名・版名は identity に使わない。 |
| **E-1′** | **系列の identity は preimage(§2.1)から §2.2 D-2 で導かれる。** exact blob identity と系列 identity は別物であり、**交差検査は §6 の三集合すべてに対して行う**。 |
| **E-2** | 同じ blob が複数経路で到達しても entry は 1 つ。`reached_via[]` に経路を並べる。 |
| **E-2′** | **`depth` は記録欄であって合否判定に使わない。** |
| **E-3** | `role` の欠落は不備。**未分類 entry を TCB とみなす既定を置かない。** |
| **E-4** | `provenance` および §2.1 の preimage 欄の欠落は**独立性の主張を無効にする**。 |

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
```

### 3.1 fixpoint の検収 {#fixpoint}

| # | 条項 |
|---|---|
| **H-1′** | **各 entry は `outgoing_dependency_attestation` を持つ。** 直接 load する artifact の content_digest の完全な列であり、**何も load しない場合は空列であることの明示的証明**を含む。 |
| **H-1a′** | **受領側が fixpoint を再計算する。** 到達可能だが未列挙の artifact があれば `digest-mismatch` [12]。 |
| **H-1b** | 閉包は **producer の環境で実際に解決された artifact** に対して取る。仕様上の依存関係表ではない。 |
| **H-1c** | **`depth` の分布を合否判定に使わない**($D=\{L\}$ で全 depth 0 は正しい fixpoint たり得る)。 |

---

## 4. 同一性の正規化 {#identity}

| # | 条項 |
|---|---|
| **H-2** | **exact blob の同一性は content digest で判定する。** 別名・別 path・薄い wrapper は同一 content digest を閉包に含むため区別されない。 |
| **H-2a** | **wrapper 貫通**: $W$ が $h$ を呼ぶだけの薄い層なら、閉包 $D$ は $h$ の digest を含む。 |
| **H-2b″** | **【B66-1 で再構成】同一 `implementation_lineage_digest`(§2.2 D-2 の受領側再計算値)を持つ二 blob は、content digest が異なっても同一 helper とみなす。** これは規則であって裁量ではない。**「別実装である」と主張する側に挙証責任**があり、その主張は **preimage(`source_artifact_digests[]` / `toolchain_digest` / `build_step_digests[]`)が異なることの提示**によって行う。 |
| **H-2c** | content digest は **exact blob** に対して取る(改行正規化・空白除去・minify を行わない)。 |
| **H-2d** | **【B66-1】producer 可変の識別子(名前・版文字列・自己申告 ID)を同一性判定に用いない。** 判定は §2.2 の再計算値と §6 の三集合交差のみによる。 |

---

## 5. `role` 分類・TCB・入力の型分離 {#roles-and-tcb}

### 5.1 `role` の分類

```text
role ∈ { math-helper, serialization, hash-primitive, runtime,
         cas-io, build-tool, data-table }
```

| # | 条項 |
|---|---|
| **H-3** | **`allowed_shared_tcb[]` は共有を許す trusted base を frozen content digest で列挙し、各項に `role` を付す。** **`role = math-helper` を TCB に入れることを禁止する。** |
| **H-3a** | **math-helper の判定基準**: 出力が「どの数学的対象が等しいか」に影響しうる処理はすべて math-helper — **canonicalizer・ideal 演算・Gröbner / normal form / reduction・divisor 正規化・partition 計算・多項式演算・体演算**。**迷う artifact は math-helper に分類**(既定は禁止側)。 |
| **H-3b** | `serialization` / `hash-primitive` / `runtime` / `cas-io` / `build-tool` は TCB 候補。**自動ではなく明示列挙して初めて差し引かれる。** |
| **H-3c** | `data-table` は**原則 TCB に入れない**。 |

### 5.2 TCB の宣言様式

```text
allowed_shared_tcb[]        = [ { content_digest, role, justification, frozen_at_receipt } ]
allowed_shared_source_tcb[] = [ { source_artifact_digest, role, justification, frozen_at_receipt } ]
allowed_shared_family[]     = [ { implementation_family_id, role, justification, frozen_at_receipt } ]
```
| # | 条項 |
|---|---|
| **H-5** | **追加は追加側に挙証責任。** `justification` は「なぜこの共有が判定の独立性を損なわないか」を述べる。追加は freeze bundle の変更であり **receipt を要する**。 |
| **H-5a** | receipt 前の追加提案は候補であって効力を持たない。 |
| **H-5b** | 縮む方向には receipt を要しない。 |
| **H-5c** | **省略を暗黙の空集合とも暗黙の許可とも読ませない** — §5.4 が実値を宣言する。 |
| **H-5d** | **【v3】三つの TCB は別欄である。** content 側を許しても source 側・family 側は自動的には許されない(逆も同じ)。 |

### 5.3 `declared_untrusted_inputs[]` — 入力と実装の型分離 {#input-separation}

```text
declared_untrusted_inputs[] = {
  divisor_equality_certificate,
  searcher_native_artifact,
  checker_native_artifact,
  governing_spec_blob,
  contract_blob
}
```

| # | 条項 |
|---|---|
| **Y-1** | **`declared_untrusted_inputs[]` は implementation closure の universe から分離される。** TCB として差し引くのではなく、**§6 の交差検査の対象外**。 |
| **Y-2** | **入力の共有は独立性を毀損しない。毀損するのは実装の共有である。** |
| **Y-3** | untrusted input は **A と B で digest 一致を要求する**。不一致は `digest-mismatch` [12]。 |

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
| **Y-4a** | **パラメータ値と実装の区別**: `monomial_order_id` 等**規約を選ぶパラメータ値の共有は許される**。**禁止されるのは、その規約を実現するコードの共有。** |
| **Y-4b** | **迷う artifact は implementation closure へ回す**(既定は厳しい側)。「読み込むと関数として評価される」形式は **U-1 違反**。 |
| **Y-4c** | **入力クラスは列挙型であり、拡張には receipt を要する。** |

### 5.4 初期 TCB の実値 {#initial-tcb}

```text
allowed_shared_tcb        = []      # 空集合(実値・省略ではない)
allowed_shared_source_tcb = []      # 空集合【v3 新設・実値】
allowed_shared_family     = []      # 空集合【v3 新設・実値】
```

| # | 条項 |
|---|---|
| **T-1** | **初期 TCB は三欄とも空である。** 「省略」でも「暗黙の許可」でもなく、**実装着手前の実値宣言**。 |
| **T-2** | 空 TCB の下で三交差を空にするため、**A と B は異なる runtime で実装する**(一方を GAP 系、他方を node/python 系)。 |
| **T-3** | **同一 runtime・同一 source・同一 family を使いたい場合**は、該当欄に **exact digest / ID・role・justification** を**実装着手前の receipt** で列挙する。**列挙前に着手してはならない。** |
| **T-4** | `serialization` / `hash-primitive` / `cas-io` を共有したい場合も同じ手続き。**現時点ではいずれも三欄に入っていない。** |

---

## 6. 交差検査 — 受領側の再計算手順 {#intersection}

> **【便 66 F13 の発案を採用】** 一つの自己申告 aggregate に押し込まず、**三集合を直接持って別々に検査**する。これにより **exact blob 共有・source helper 共有・同一 generator family の三事故**が分離して見える。

```text
binary_content_set(X)        = { entry.content_digest : entry ∈ closure(X) }
source_artifact_digest_set(X)= ⋃ { entry.source_artifact_digests[] : entry ∈ closure(X) }
implementation_family_set(X) = { entry.implementation_family_id : entry ∈ closure(X) }
                               # receipt authority が mint した値のみ
```

| # | 手順 |
|---|---|
| **H-4** | **交差の値は producer の自己申告を信じない。receipt 受領側が canonical digest 集合から導出して再計算する。** |
| **I-0** | **受領側はまず §2.2 D-1・D-2 を preimage から再計算し、entry の申告値と照合する**(不一致 → [12]・E-8)。**再計算不能(preimage 欠落)なら E-4 により独立性主張は無効 → [11]。** |
| **I-1** | 両 closure を三集合へ落とす(`role`・`provenance`・`depth` は別に保持)。 |
| **I-2** | **`declared_untrusted_inputs[]` の digest は universe から除外する**(集合を作る前に外す)。 |
| **I-3a** | **binary content 交差** $-$ `allowed_shared_tcb` |
| **I-3b** | **source artifact 交差** $-$ `allowed_shared_source_tcb`(**部分的な source helper 共有を拾う** — aggregate だけでは見えない) |
| **I-3c** | **implementation family 交差** $-$ `allowed_shared_family`(**同一 source の別 toolchain rebuild を拾う** — H-2b″) |
| **I-5** | **I-3a / I-3b / I-3c のいずれかが非空なら `INTEGRITY_STOP / shared-helper-detected` [11]。** |
| **I-6** | 空であっても、**差し引いた TCB 部分に `role = math-helper` が含まれていれば同じく [11]**。 |
| **I-7″** | **【B66-1 で置換】** v2 の I-7′(aggregate lineage 交差のみ)は**producer が ID を替えるだけで回避できた**ので撤回。**I-3b と I-3c が preimage 由来の値で機械的に拾う。** |
| **I-8** | manifest の entry と実体の digest が食い違う、または H-1a′ の fixpoint 再計算で**到達可能だが未列挙**の artifact が見つかれば **`digest-mismatch` [12]**。 |

**段番号 [11] / [12] は governing spec §5.3.2 の `integrity_priority` を指す。verdict の決定と primary の選択は governing spec §5.3 の state machine が行う — 本稿は reason code を供給するだけである。**

---

## 7. manifest record の全体形 {#record}

```text
dependency_manifest = {
  schema_id, schema_digest,
  subject_id,                       # verifier_A_id / verifier_B_id / generator_id
  subject_code_digest,
  build_root_id,
  entries[]                         # §2 の manifest_entry(推移閉包・§3)
  declared_untrusted_inputs[]       # §5.3 — closure とは別欄
  allowed_shared_tcb[]              # §5.2・初期値 §5.4
  allowed_shared_source_tcb[]
  allowed_shared_family[]
  closure_attested = true           # H-1′
  produced_at_receipt
}
```
**受領側が保持するのは §6 の三集合と `role` 対応表であり、これが交差検査の入力になる。`declared_untrusted_inputs[]` は universe から外される。**

---

## 8. 適合宣言 {#conformance}

```text
conformance_record = {
  schema_id, schema_digest,
  covered_clauses = [E-1, E-1', E-2, E-2', E-3, E-4, E-5..E-8,
                     D-R1..D-R3, M-1..M-4,
                     H-1', H-1a', H-1b, H-1c,
                     H-2, H-2a, H-2b", H-2c, H-2d,
                     H-3, H-3a, H-3b, H-3c,
                     H-5, H-5a, H-5b, H-5c, H-5d,
                     Y-1..Y-3, Y-4, Y-4a, Y-4b, Y-4c, U-1..U-4,
                     T-1..T-4,
                     H-4, I-0, I-1, I-2, I-3a, I-3b, I-3c, I-5, I-6, I-7", I-8]
  uncovered_clauses = []            # 空でなければ適合しない
}
```
**`uncovered_clauses` が非空の manifest を「様式適合」と呼ばない。** 部分適合は `partial manifest / UNKNOWN` として扱い、**独立性の証跡としては使えない。**
