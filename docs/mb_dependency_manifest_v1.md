# `mb/dependency-manifest/v1` — dependency closure の記録様式

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 76)。**
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
schema_id     = "mb/dependency-manifest/v1"
schema_digest = <64 hex: 本稿 exact blob の sha256 — 発行時に司令塔が記入>
encoding      = UTF-8, LF, no BOM, no normalization
governing_spec = "mb/ninfty-stage2-predicate/v6"
governing_spec_digest = <64 hex — 発行時に記入>
```
**接触規律**: 値に依存しない。$C$・$h$・$a_5$・平方類・符号・分岐値・具体係数・raw shard 命名パターンを**一切書かない**。
**優先関係**: 本稿と governing spec が矛盾した場合、**governing spec が優先**する。

---

## 1. この様式が閉じる未定義項 {#purpose}

便 63 F8 が指摘した 4 つの未定義項に、それぞれ本稿の節が対応する。

| 未定義項 | 本稿 |
|---|---|
| manifest が直接依存だけか、**推移的閉包**か | §3(生成規則 R-1〜R-5)・**H-1** |
| 同じ helper を**別名・別 path・薄い wrapper**で包んだ場合の同一性 | §2(entry の型)・§4(正規化)・**H-2** |
| runtime・parser・serialization・CAS/library の**どこまでを helper と数えるか** | §5(`role` 分類)・**H-3** |
| schema parser や hash primitive など、**共有を許す trusted base** | §5(`allowed_shared_tcb[]`)・**H-3・H-5** |

> **「全 helper」の文字どおりなら標準 runtime 等の共有で交差は通常空にならず、それらを暗黙に除けば共通 canonicalizer を除外した証拠にならない。** ゆえに **TCB を明示宣言し、交差から差し引く**形にする。

---

## 2. entry の型 {#entry-type}

```text
manifest_entry = {
  content_digest,          # 必須・64 hex・identity はこれだけで決まる
  role,                    # §5 の分類のいずれか(必須)
  provenance = {
    build_root_id,         # 再現ビルドの根
    toolchain_id,          # コンパイラ / runtime の版
    source_ref             # 任意・人間可読の由来(identity には使わない)
  },
  depth,                   # 0 = 直接依存、1 以上 = 推移的に到達
  reached_via[]            # 到達経路(content_digest の列)
}
```

| # | 条項 |
|---|---|
| **E-1** | **identity は `content_digest` のみで決まる。** `source_ref`・path・パッケージ名・版名は identity に使わない。 |
| **E-2** | 同じ blob が複数経路で到達しても **entry は 1 つ**。`reached_via[]` に経路を並べ、`depth` は**最小**を記録する。 |
| **E-3** | `role` の欠落は manifest の不備であり、`INTEGRITY_STOP / shared-helper-detected` の対象。**未分類 entry を TCB とみなす既定を置かない。** |
| **E-4** | `provenance` の欠落は独立性の主張を無効にする(**path 改名を独立二実装と数える事故の防止**)。 |

---

## 3. 推移的閉包の生成規則 {#closure-rules}

```text
dependency_closure(X) = 最小の集合 D で次を満たすもの:
  R-1  X が直接 import / link / load する全 artifact の content_digest ∈ D
  R-2  d ∈ D ならば、d が直接 import / link / load する全 artifact の
       content_digest ∈ D                          # 推移閉包
  R-3  実行時に動的解決される artifact も、解決され得る候補集合を D に含める
  R-4  データとして読み込まれるだけの artifact のうち、
       出力に影響し得るもの(表・定数・規約ファイル)は D に含める
  R-5  D は fixpoint に達するまで展開する
```

| # | 条項 |
|---|---|
| **H-1** | **直接依存のみの manifest は不可。** `dependency_closure_A[]` / `dependency_closure_B[]` は **R-1〜R-5 の fixpoint** でなければならない。`depth` が 0 の entry しか無い manifest は、それ自体が不備。 |
| **H-1a** | 閉包の**打ち切りを宣言してはならない**。到達可能だが列挙していない artifact があるなら、manifest は不完全であり `shared-helper-detected` ではなく **`digest-mismatch`(manifest と実体の不一致)** として扱う。 |
| **H-1b** | 閉包は **producer の環境で実際に解決された artifact** に対して取る。仕様上の依存関係表ではない。 |

---

## 4. 同一性の正規化 {#identity}

| # | 条項 |
|---|---|
| **H-2** | **同一性は content digest で判定する。** 別名・別 path・薄い wrapper は、**同一 content digest を閉包に含む**ため区別されない。 |
| **H-2a** | **wrapper が独立実装を生まないことの明文化**: $W$ が $h$ を呼ぶだけの薄い層なら、$W$ の digest は $h$ の digest と別でも、**閉包 $D$ は $h$ の digest を含む**。ゆえに交差検査は wrapper を貫通する。 |
| **H-2b** | **再ビルドによる digest 差は独立性の根拠にならない。** 同一 source から異なる toolchain で作った 2 つの blob は digest が異なりうるが、`build_root_id` / `toolchain_id` / `source_ref` が同一系列を指すなら、**受領側は同一 helper とみなして交差に数えてよい**(挙証責任は「別実装だ」と主張する側)。 |
| **H-2c** | content digest は **exact blob** に対して取る(改行正規化・空白除去・minify を行わない)。 |

---

## 5. `role` 分類と `allowed_shared_tcb[]` {#tcb}

### 5.1 `role` の分類

```text
role ∈ {
  math-helper,        # 数学的内容を持つ — 共有禁止
  serialization,      # canonical 直列化・parser
  hash-primitive,     # ハッシュ関数実装
  runtime,            # 言語 runtime / 標準ライブラリ
  cas-io,             # content-addressed storage の読み書き
  build-tool,         # 出力に寄与しないビルド補助
  data-table          # 出力に影響する定数・規約ファイル
}
```

| # | 条項 |
|---|---|
| **H-3** | **`allowed_shared_tcb[]` は共有を許す trusted base を frozen content digest で列挙し、各項に `role` を付す。** **`role = math-helper` の artifact を TCB に入れることを禁止する。** |
| **H-3a** | **math-helper の判定基準**: 出力が「どの数学的対象が等しいか」に影響しうる処理はすべて math-helper。具体的には **canonicalizer・ideal 演算・Gröbner / normal form・divisor 正規化・partition 計算・多項式演算・体演算**。**判断に迷う artifact は math-helper に分類する**(既定は禁止側)。 |
| **H-3b** | `serialization` / `hash-primitive` / `runtime` / `cas-io` / `build-tool` は TCB 候補。**ただし自動ではない — 明示列挙して初めて差し引かれる。** |
| **H-3c** | `data-table` は**原則 TCB に入れない**。両 lane が同じ定数表を共有すると、表の誤りが両側に同じ形で入る。 |

### 5.2 宣言様式

```text
allowed_shared_tcb[] = [
  { content_digest, role, justification, frozen_at_receipt }
]
```
| # | 条項 |
|---|---|
| **H-5** | **`allowed_shared_tcb[]` への追加は追加側に挙証責任がある。** `justification` は「なぜこの artifact の共有が判定の独立性を損なわないか」を述べる。追加は **freeze bundle の変更**であり、**receipt を要する**。 |
| **H-5a** | receipt 前の TCB 追加提案は候補であって効力を持たない(§0 の lifecycle 分離と同じ理由)。 |
| **H-5b** | TCB は**縮む方向には receipt を要しない**(より厳しくなるだけ)。 |

---

## 6. 交差検査 — 受領側の再計算手順 {#intersection}

```text
forbidden_shared_math_helper_intersection
    = (dependency_closure_A ∩ dependency_closure_B) - allowed_shared_tcb
```

| # | 手順 |
|---|---|
| **H-4** | **交差の値は producer の自己申告を信じない。receipt 受領側が canonical content digest 集合から導出して再計算する。** |
| **I-1** | 受領側は `dependency_closure_A[]` / `dependency_closure_B[]` を **content_digest の集合**へ落とす(`role`・`provenance`・`depth` は落とさず別に保持)。 |
| **I-2** | 集合積を取る。**path・名前・順序は一切使わない。** |
| **I-3** | `allowed_shared_tcb[]` の content_digest 集合を差し引く。 |
| **I-4** | 差し引いた結果が**空でなければ `INTEGRITY_STOP / shared-helper-detected` [11]**。 |
| **I-5** | 空であっても、**残った交差(= TCB 部分)に `role = math-helper` が含まれていれば同じく [11]**(H-3 違反が TCB 宣言で隠されるのを防ぐ)。 |
| **I-6** | manifest の entry と実体の digest が食い違う、または閉包が fixpoint でない兆候(到達可能だが未列挙の artifact)があれば **`digest-mismatch` [12]**(H-1a)。 |
| **I-7** | **A と B の `build_root_id` が同一かつ `toolchain_id` が同一の場合、受領側は「同一実装の path 改名」の疑いを立て、`implementation_provenance` の提示を求める。** 説明が無ければ [11]。 |

**段番号 [11] / [12] は spec v6 §5.3.2 の `integrity_priority` を指す。verdict の決定と primary の選択は spec §5.3 の state machine が行う — 本稿は reason code を供給するだけである。**

---

## 7. manifest record の全体形 {#record}

```text
dependency_manifest = {
  schema_id, schema_digest,
  subject_id,                       # 対象(verifier_A_id / verifier_B_id / generator_id)
  subject_code_digest,
  build_root_id, toolchain_id, implementation_provenance,
  entries[]                         # §2 の manifest_entry(推移閉包・§3)
  closure_fixpoint_asserted = true  # H-1 / H-1a
  produced_at_receipt                # どの receipt の下で作られたか
}
```
**受領側が保持するのは `entries[]` の content_digest 集合と `role` 対応表であり、これが §6 の再計算の入力になる。**

---

## 8. 適合宣言 {#conformance}

```text
conformance_record = {
  schema_id, schema_digest,
  covered_clauses = [E-1..E-4, H-1, H-1a, H-1b, H-2, H-2a, H-2b, H-2c,
                     H-3, H-3a, H-3b, H-3c, H-5, H-5a, H-5b,
                     H-4, I-1..I-7]
  uncovered_clauses = []            # 空でなければ適合しない
}
```
**`uncovered_clauses` が非空の manifest を「様式適合」と呼ばない。** 部分適合は `partial manifest / UNKNOWN` として扱い、**独立性の証跡としては使えない。**
