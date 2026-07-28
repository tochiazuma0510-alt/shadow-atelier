# `mb/dependency-manifest/v2` — implementation dependency closure の記録様式

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 77)。v1 を supersede。**
**この文書は `mb/ninfty-stage2-predicate/v6` §4.4 の `dependency_manifest_schema_id` が指す実体である。**

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
schema_id     = "mb/dependency-manifest/v2"
schema_digest = <64 hex: 本稿 exact blob の sha256 — 発行時に司令塔が記入>
encoding      = UTF-8, LF, no BOM, no normalization
governing_spec = "mb/ninfty-stage2-predicate/v6"
governing_spec_digest = 00282b4914f4ade9e356ee641a71ba91be6daf27ad82221f6acf8638df4bc39a
supersedes    = "mb/dependency-manifest/v1"
supersedes_digest = 7d513049fa8e79b5c32054135222356e26cf9f32e9e8f8ae6c5ce71aeaf3cdc9   # 監査 FAIL の candidate
```
**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。
**優先関係**: 本稿と governing spec が矛盾した場合、**governing spec が優先**する。

---

## 0.1 v1 → v2 差分

| ID | v1 | v2 | 出所 |
|---|---|---|---|
| **B65-3** | closure が「load する全 artifact」を飲み込み、**A/B が共有する certificate・両 native が必ず $D_A\cap D_B$ に現れる**。これらは TCB ではなく**信用せず独立検査すべき共通入力**なので TCB に入れられず、**正しく独立な二 verifier でも必ず [11] で停止**する(contract と manifest を同時に満たす実装が存在しない) | **`declared_untrusted_inputs[]` を新設して universe を分離**(§5.3)。closure は `implementation_dependency_closure` へ改称し **code / library / runtime / build-time data の推移閉包**に限定。**入力は TCB として差し引くのではなく、そもそも交差検査の対象外。** 入力クラスへの math-helper 混入判定基準を §5.3.2 に。**自認** | 便 65 F6 |
| **F7.1** | 「`depth = 0` の entry しかない manifest は不備」 | **撤回。** $X$ が自己完結 leaf $L$ を一つ load し $L$ が何も load しないなら $D=\{L\}$ は**正しい fixpoint**で全 entry が depth 0。**depth の見た目でなく、各 node の outgoing dependency 証明(load しないことの証明を含む)と受領側の fixpoint 再計算**で検収する(§3 の H-1′/H-1a′)。**自認** | 便 65 F7.1 |
| **F7.2** | E-1/I-1〜I-4 が identity を content digest だけで定める一方、H-2b は「同一 source を別 toolchain で build して digest が変わっても同一 helper とみなす」とした。**mandatory な source digest / lineage identity が record に無く**、`source_ref` は任意・human-readable、`build_root_id` の digest 規約は未定義、I-7 は build root **かつ** toolchain が同じ場合しか止めず **H-2b の主例(同 source・別 toolchain)を拾わない**。「みなしてよい」が受領側の裁量なので**同じ bundle が PASS と FAIL の両方になり得た** | **`source_closure_digest` と `implementation_lineage_digest` を mandatory 化**(§2)。**content 交差と lineage 交差の両方が空**であることを要求(§6 I-3′/I-4′)。**H-2b の裁量を削除し規則化**(H-2b′)。**I-7 を lineage 交差検査へ置換**。**自認** | 便 65 F7.2 |
| **F7.3** | `allowed_shared_tcb[]` の**型**だけで初期 exact entries が無い(省略を暗黙の空集合とも暗黙の許可とも読ませてはならない) | **初期値を実値で宣言: `allowed_shared_tcb = []`(空)**。その帰結として **A と B は異なる runtime で実装する**(§5.4)。同一 runtime を許すなら exact digest・role・justification を**実装着手前の receipt に列挙**する。**自認** | 便 65 F7.3 |

---

## 1. この様式が閉じる未定義項 {#purpose}

| 未定義項(便 63 F8 / 便 65 F6・F7) | 本稿 |
|---|---|
| manifest が直接依存だけか、**推移的閉包**か | §3(R-1〜R-5・H-1′) |
| 同じ helper を**別名・別 path・薄い wrapper**で包んだ場合の同一性 | §2・§4(H-2・H-2a) |
| **rebuild lineage** と exact blob identity の接続 | §2(lineage 欄)・§4(H-2b′)・§6(I-4′) |
| runtime・parser・serialization・CAS/library の**どこまでを helper と数えるか** | §5.1(`role` 分類・H-3a) |
| **共有を許す trusted base** と初期値 | §5.2・§5.4(H-3・H-5・実値 `[]`) |
| **共有 input と共有 implementation の型分離** | §5.3(Y 系) |

---

## 2. entry の型 {#entry-type}

```text
manifest_entry = {
  content_digest,              # 必須・64 hex・exact blob の identity
  role,                        # §5.1 の分類(必須)
  source_closure_digest,       # 必須【F7.2】§2.1
  implementation_lineage_digest, # 必須【F7.2】§2.1
  provenance = {
    build_root_id,             # 必須・§2.1 で digest 規約を定義
    toolchain_id,              # 必須
    source_ref                 # 任意・human-readable(identity には使わない)
  },
  outgoing_dependency_attestation,  # 必須【F7.1】§3.1
  depth,                       # 記録のみ・合否判定に使わない
  reached_via[]                # 到達経路(content_digest の列)
}
```

### 2.1 lineage 識別子の定義【F7.2】{#lineage}

```text
build_root_id = sha256( canonical serialization of {
                  build_definition_blob_digest,     # ビルド定義そのものの digest
                  pinned_input_digests[]            # 固定された入力の digest 列(sorted)
                } )

source_closure_digest = sha256( sorted multiset of content digests of the
                  *source* artifacts (pre-build) that produced this blob )

implementation_lineage_digest = sha256( canonical serialization of {
                  source_closure_digest,
                  generator_lineage_id              # 同一系列を指す安定 ID
                } )
```

| # | 条項 |
|---|---|
| **E-1** | **exact blob の identity は `content_digest` のみで決まる。** `source_ref`・path・パッケージ名・版名は identity に使わない。 |
| **E-1′** | **系列の identity は `implementation_lineage_digest` で決まる。** content が違っても lineage が同じなら**同一系列**である(§4 H-2b′)。**この二つは別の identity であり、交差検査は両方に対して行う**(§6)。 |
| **E-2** | 同じ blob が複数経路で到達しても **entry は 1 つ**。`reached_via[]` に経路を並べる。 |
| **E-2′** | **`depth` は記録欄であって合否判定に使わない**(F7.1)。 |
| **E-3** | `role` の欠落は manifest の不備。**未分類 entry を TCB とみなす既定を置かない。** |
| **E-4** | `provenance` および lineage 欄の欠落は**独立性の主張を無効にする**。 |

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

### 3.1 fixpoint の検収【F7.1】{#fixpoint}

> **v1 の誤り(自認)**: 「`depth = 0` の entry しかない manifest はそれ自体が不備」とした。**しかし $X$ が自己完結な leaf $L$ を一つだけ load し $L$ が何も load しないなら $D=\{L\}$ は正しい fixpoint であり、全 entry の depth は 0 である。** v1 の規則は**完全な manifest を拒否し、架空の depth-1 dependency を要求していた。**

| # | 条項 |
|---|---|
| **H-1′** | **各 entry は `outgoing_dependency_attestation` を持つ。** これは「この node が直接 load する artifact の content_digest の完全な列」であり、**何も load しない場合は空列であることの明示的な証明**を含む(暗黙の欠落と区別する)。 |
| **H-1a′** | **受領側が fixpoint を再計算する。** 全 entry の attestation を辿り、`D` が R-1〜R-5 の閉包になっているかを確認する。**到達可能だが未列挙の artifact があれば `digest-mismatch` [12]**(manifest と実体の不一致)。 |
| **H-1b** | 閉包は **producer の環境で実際に解決された artifact** に対して取る。仕様上の依存関係表ではない。 |
| **H-1c** | **`depth` の分布(0 のみ / 深い)を合否判定に使わない。** 判定は H-1′ の attestation と H-1a′ の fixpoint 再計算のみによる。 |

---

## 4. 同一性の正規化 {#identity}

| # | 条項 |
|---|---|
| **H-2** | **exact blob の同一性は content digest で判定する。** 別名・別 path・薄い wrapper は、**同一 content digest を閉包に含む**ため区別されない。 |
| **H-2a** | **wrapper 貫通**: $W$ が $h$ を呼ぶだけの薄い層なら、$W$ の digest が $h$ と別でも**閉包 $D$ は $h$ の digest を含む**。ゆえに交差検査は wrapper を貫通する。 |
| **H-2b′** | **【F7.2 で規則化】同一 `implementation_lineage_digest` を持つ二 blob は、content digest が異なっても(= 別 toolchain で rebuild されていても)**同一 helper とみなす**。これは受領側の裁量ではなく規則であり、同じ bundle が PASS と FAIL の両方になることはない。**「別実装である」と主張する側に挙証責任**があり、その主張は `source_closure_digest` が異なることの提示によって行う。 |
| **H-2c** | content digest は **exact blob** に対して取る(改行正規化・空白除去・minify を行わない)。 |

---

## 5. `role` 分類・TCB・入力の型分離 {#roles-and-tcb}

### 5.1 `role` の分類

```text
role ∈ {
  math-helper,        # 数学的内容を持つ — 共有禁止
  serialization,      # canonical 直列化・parser
  hash-primitive,     # ハッシュ関数実装
  runtime,            # 言語 runtime / 標準ライブラリ
  cas-io,             # content-addressed storage の読み書き
  build-tool,         # 出力に寄与しないビルド補助
  data-table          # 手続きの挙動を決める定数・規約ファイル
}
```

| # | 条項 |
|---|---|
| **H-3** | **`allowed_shared_tcb[]` は共有を許す trusted base を frozen content digest で列挙し、各項に `role` を付す。** **`role = math-helper` の artifact を TCB に入れることを禁止する。** |
| **H-3a** | **math-helper の判定基準**: 出力が「どの数学的対象が等しいか」に影響しうる処理はすべて math-helper。具体的には **canonicalizer・ideal 演算・Gröbner / normal form / reduction・divisor 正規化・partition 計算・多項式演算・体演算**。**判断に迷う artifact は math-helper に分類する**(既定は禁止側)。 |
| **H-3b** | `serialization` / `hash-primitive` / `runtime` / `cas-io` / `build-tool` は TCB 候補。**ただし自動ではない — 明示列挙して初めて差し引かれる。** |
| **H-3c** | `data-table` は**原則 TCB に入れない**。両 lane が同じ定数表を共有すると、表の誤りが両側に同じ形で入る。 |

### 5.2 `allowed_shared_tcb[]` の宣言様式

```text
allowed_shared_tcb[] = [
  { content_digest, implementation_lineage_digest, role, justification,
    frozen_at_receipt }
]
```
| # | 条項 |
|---|---|
| **H-5** | **追加は追加側に挙証責任がある。** `justification` は「なぜこの artifact の共有が判定の独立性を損なわないか」を述べる。追加は **freeze bundle の変更**であり、**receipt を要する**。 |
| **H-5a** | receipt 前の TCB 追加提案は候補であって効力を持たない。 |
| **H-5b** | TCB は**縮む方向には receipt を要しない**。 |
| **H-5c** | **省略を暗黙の空集合とも暗黙の許可とも読ませない** — §5.4 が実値を宣言する。 |

### 5.3 `declared_untrusted_inputs[]` — 入力と実装の型分離【B65-3】{#input-separation}

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
| **Y-1** | **`declared_untrusted_inputs[]` は `implementation_dependency_closure` の universe から分離される。** TCB として差し引くのではなく、**そもそも §6 の交差検査の対象外**。 |
| **Y-2** | **入力の共有は独立性を毀損しない。毀損するのは実装の共有である。** untrusted input は**両 verifier が独立に内容を再検査する**対象であり、共有されることが前提。 |
| **Y-3** | untrusted input は **A と B で digest 一致を要求する**。不一致は「検査対象が別物」を意味し `digest-mismatch` [12]。 |

#### 5.3.2 入力クラスへの math-helper 混入を防ぐ判定基準 {#input-criteria}

artifact が `declared_untrusted_inputs[]` に属してよいのは、次の **4 条件をすべて**満たすときに限る。

```text
U-1  データとして消費される  — 手続きとして実行 / load されない
U-2  内容が再検査される      — 両 verifier が独立にその内容を検証する対象である
U-3  手続きを実現しない      — canonicalization / 簡約 / 比較の *アルゴリズム* を提供しない
U-4  明示宣言されている      — certificate または contract が入力として列挙している
```

| # | 条項 |
|---|---|
| **Y-4** | **U-1〜U-4 のいずれかを欠く artifact は入力クラスに置けない。implementation closure 側へ回す。** |
| **Y-4a** | **パラメータ値と実装の区別**: `monomial_order_id` や `groebner_reduction_contract_id` のように**規約を選ぶパラメータ値の共有は許される**(U-3 に反しない — 値は「どの規約か」を指すだけで、規約を**実現する**のはコード)。**A と B は同じ規約を各々の実装で実現する。禁止されるのは、その規約を実現するコードの共有である。** |
| **Y-4b** | **判断に迷う artifact は入力クラスに置かず implementation closure へ回す**(既定は厳しい側)。とくに「入力だが読み込むと関数として評価される」形式(実行可能な設定・スクリプト化された規約)は **U-1 違反**として implementation 側。 |
| **Y-4c** | **入力クラスは列挙型であり、拡張には receipt を要する**(H-5 と同じ扱い)。無宣言の artifact を事後に「入力だった」と主張することを禁じる。 |

### 5.4 初期 TCB の実値【F7.3】{#initial-tcb}

```text
allowed_shared_tcb = []          # 空集合(実値・省略ではない)
```

| # | 条項 |
|---|---|
| **T-1** | **初期 TCB は空である。** これは「省略」でも「暗黙の許可」でもなく、**実装着手前の実値宣言**である。 |
| **T-2** | 空 TCB の下で $(\text{closure}_A\cap\text{closure}_B)=\varnothing$ を成り立たせるため、**A と B は異なる runtime で実装する**(例: 一方を GAP 系、他方を node/python 系)。**共通の言語 runtime を持たなければ `role = runtime` の entry は交差しない。** |
| **T-3** | **同一 runtime で A/B を実装したい場合**は、その runtime の **exact content digest・`implementation_lineage_digest`・role・justification** を **実装着手前の receipt** で `allowed_shared_tcb[]` に列挙する(H-5)。**列挙前に同一 runtime で実装を始めてはならない。** |
| **T-4** | `serialization` / `hash-primitive` / `cas-io` を共有したい場合も同じ手続き。**現時点ではいずれも TCB に入っていない。** |

---

## 6. 交差検査 — 受領側の再計算手順 {#intersection}

```text
forbidden_shared_implementation_intersection
    = (implementation_dependency_closure_A ∩ implementation_dependency_closure_B)
      - allowed_shared_tcb

forbidden_shared_lineage_intersection
    = (lineage_set_A ∩ lineage_set_B) - allowed_shared_tcb_lineage
```

| # | 手順 |
|---|---|
| **H-4** | **交差の値は producer の自己申告を信じない。receipt 受領側が canonical digest 集合から導出して再計算する。** |
| **I-1** | 受領側は両 closure を **content_digest の集合**へ落とす(`role`・`provenance`・lineage・`depth` は落とさず別に保持)。 |
| **I-2** | **`declared_untrusted_inputs[]` の digest は universe から除外する**(§5.3 Y-1)。**TCB として差し引くのではなく、集合を作る前に外す。** |
| **I-3′** | **content 交差**を取り、`allowed_shared_tcb` の content_digest 集合を差し引く。 |
| **I-4′** | **lineage 交差**を取り、`allowed_shared_tcb` の lineage 集合を差し引く(**同 source・別 toolchain の rebuild を拾う** — H-2b′)。 |
| **I-5** | **I-3′ と I-4′ のどちらかが非空なら `INTEGRITY_STOP / shared-helper-detected` [11]。** |
| **I-6** | 空であっても、**差し引いた TCB 部分に `role = math-helper` が含まれていれば同じく [11]**(H-3 違反が TCB 宣言で隠されるのを防ぐ)。 |
| **I-7′** | **【F7.2 で置換】** v1 の I-7(build root **かつ** toolchain 一致のときだけ疑いを立てる)は **H-2b の主例(同 source・別 toolchain)を拾わなかった**ので撤回。**代わりに I-4′ の lineage 交差が機械的に拾う。** `implementation_lineage_digest` の欠落は E-4 により独立性主張の無効化 → [11]。 |
| **I-8** | manifest の entry と実体の digest が食い違う、または H-1a′ の fixpoint 再計算で**到達可能だが未列挙**の artifact が見つかれば **`digest-mismatch` [12]**。 |

**段番号 [11] / [12] は spec v6 §5.3.2 の `integrity_priority` を指す。verdict の決定と primary の選択は spec §5.3 の state machine が行う — 本稿は reason code を供給するだけである。**

---

## 7. manifest record の全体形 {#record}

```text
dependency_manifest = {
  schema_id, schema_digest,
  subject_id,                       # verifier_A_id / verifier_B_id / generator_id
  subject_code_digest,
  build_root_id, toolchain_id,
  source_closure_digest, implementation_lineage_digest,
  entries[]                         # §2 の manifest_entry(推移閉包・§3)
  declared_untrusted_inputs[]       # §5.3 — closure とは別欄
  allowed_shared_tcb[]              # §5.2 の様式・初期値は §5.4 で []
  closure_attested = true           # H-1′: 全 entry が attestation を持つ
  produced_at_receipt
}
```
**受領側が保持するのは `entries[]` の content_digest 集合・lineage 集合・`role` 対応表であり、これが §6 の再計算の入力になる。`declared_untrusted_inputs[]` は §6 の universe から外される。**

---

## 8. 適合宣言 {#conformance}

```text
conformance_record = {
  schema_id, schema_digest,
  covered_clauses = [E-1, E-1', E-2, E-2', E-3, E-4,
                     H-1', H-1a', H-1b, H-1c,
                     H-2, H-2a, H-2b', H-2c,
                     H-3, H-3a, H-3b, H-3c,
                     H-5, H-5a, H-5b, H-5c,
                     Y-1, Y-2, Y-3, Y-4, Y-4a, Y-4b, Y-4c, U-1..U-4,
                     T-1..T-4,
                     H-4, I-1, I-2, I-3', I-4', I-5, I-6, I-7', I-8]
  uncovered_clauses = []            # 空でなければ適合しない
}
```
**`uncovered_clauses` が非空の manifest を「様式適合」と呼ばない。** 部分適合は `partial manifest / UNKNOWN` として扱い、**独立性の証跡としては使えない。**
