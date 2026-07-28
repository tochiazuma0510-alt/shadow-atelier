# `typed-edge/v1` — 汎用 typed-edge capsule schema

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 138-1)。状態 = candidate。commit していない。**
**根拠**: 便 77 **P77-1**(typed-edge capsule の発案)・**F77-1.1**($\bar\iota|_{K_q}$ が typed equality でない)・**F77-1.2**(既発効 Z-norm seal と同じ $\bar\iota$ を指していない)・**F77-2.2**(prose string は不受理)。
**規律**: 数学を再証明しない。$u$・封印量に触れていない。外部文献なし。

---

## 0. 何を解く schema か(3 行)

1. **prose equality と object identity を一度に切り分ける。** 「$\bar\iota|_{K_9}=\iota_\infty^{(9)}$」という**文字列**ではなく、**どの object 間の・どの操作による・どの定理を根拠とする等式か**を束縛する。
2. **family specialization / Z-norm migration / (E-iv) naming を同一型で書く。** 三者は「普遍側の定理 or 定義を、具体 object へ適用して得た有向辺」という同じ構造を持つ。
3. **capsule は数学を再証明しない。** 証明は `theorem_or_definition_id` と `proof_artifact_id` の先にあり、capsule はそこへの typed な接続だけを持つ。

---

## 1. schema 本体

```text
[typed-edge-capsule]
schema_id                   = "typed-edge/v1"
schema_digest               = <64 hex — 発行時に receipt が記入>

edge_id                     = <この辺の minted ID>
edge_digest                 = <64 hex: この capsule の exact blob の sha256(receipt が記入)>

source_object_ids[]         = [ <object ID>, ... ]          # 左辺に現れる object(順序有意)
source_object_digests[]     = [ <64 hex>, ... ]             # 同順・要素数一致

target_object_id            = <右辺の object ID>
target_object_digest        = <64 hex>

operation                   = <source から target を得る操作の名>   # §2 の列挙
parameters                  = { <操作の引数> }                     # 例 { level: 36 }

theorem_or_definition_id    = <この辺を正当化する普遍側 artifact の ID>
theorem_or_definition_digest= <64 hex>

specialization_map          = { <普遍側の量化変数> : <具体値>, ... }  # 例 { q: 9, M: 18, 2M: 36 }

proof_artifact_id           = <証明 artifact の ID>          # 定義由来の辺では "definition" 型
proof_artifact_digest       = <64 hex>
```

---

## 2. `operation` の列挙(**閉じた集合**)

| `operation` | 意味 | `parameters` | 典型 |
|---|---|---|---|
| `restrict` | 大きい object の指定 level への制限 | `{ level: N }` | `restrict(root_system_tb2_id, level=36)` |
| `specialize` | 普遍量化された定理/定義の具体値への代入 | `{}`(代入は `specialization_map`) | family clause の $q=9$ 適用 |
| `embed` | 体・群の埋め込み(単射準同型) | `{ generator: <元> }` | $j_q:K_q\hookrightarrow\bar{\mathbb Q}$ |
| `compose` | 二辺の合成 | `{ order: [id1, id2] }` | $\bar\iota\circ j_q$ |
| `name` | 同型による命名規約(量ではなく名前を固定) | `{ correspondence: <対応> }` | (E-iv) の $\zeta_M^{\rm Rule}\mapsto X_q$ |
| `identify` | 二つの ID が同一 object を指すことの宣言 | `{}` | Z-norm の `bar_iota_id` 束縛 |

> **⛔ 列挙外の `operation` を使う capsule は不受理。** 新しい操作が要るときは **schema を版上げする**(`typed-edge/v2`)。**capsule 側で語を作らない。**

---

## 3. 検査規則(受領側・fail-closed)

| # | 条項 |
|---|---|
| **TE-1** | **`source_object_ids[]` と `source_object_digests[]` は同じ長さで同順**。不一致は不受理。 |
| **TE-2** | **すべての ID が実在 object を指し、digest が受領側の再計算と一致**すること。producer の申告値を信じない。 |
| **TE-3** | **`operation` は §2 の列挙のいずれか**。列挙外は不受理。 |
| **TE-4** | **`theorem_or_definition_id` が実在**し、その **量化変数の集合と `specialization_map` の key 集合が一致**すること。**過不足はいずれも不受理**(代入し忘れ・余計な代入の双方を止める)。 |
| **TE-5** | **`proof_artifact_id` が空の capsule は不受理。** 定義由来の辺では `proof_artifact_id = "definition"`・`proof_artifact_digest` は当該定義 artifact の digest を入れる(**空欄で通さない**)。 |
| **TE-6** | **prose string の等式宣言を capsule の代用にしない**(F77-2.2)。左右辺が object ID を指していない記述は**受領側で不受理**。 |
| **TE-7** | **`edge_digest` は capsule 自身の exact blob の sha256** であり、**capsule 本文には書かない**(自己参照禁止・便 61 A61-2 と同じ規律)。**receipt が束縛する。** |
| **TE-8** | **既存 ID があるものは新設・改名しない**(Z-norm seal §2-a の規律)。同じ辺に二つの ID を作らない。 |

---

## 4. 三つの用途への適用(型が同じであることの確認)

### 4.1 family specialization(普遍条項 → 窓)

```text
edge_id                  = "family-rule1/specialize/q9/v1"
source_object_ids[]      = [ "family-Rule1/template/v1" ]
target_object_id         = <q=9 instance の object ID>
operation                = specialize
parameters               = {}
theorem_or_definition_id = "family-Rule1/template/v1"
specialization_map       = { q: 9, M: 18, 2M: 36 }
proof_artifact_id        = "definition"          # 条項の適用であり新しい証明ではない
```

### 4.2 Z-norm migration(profinite 根系 → 指定 level)

```text
edge_id                  = "rule1-tb2-root-equality/level36/v1"
source_object_ids[]      = [ "root-system/tb2/v1" ]
target_object_id         = <level 36 の Rule 1 root object ID>
operation                = restrict
parameters               = { level: 36 }
theorem_or_definition_id = "znorm-seal-final/v1"           # 条 (1)(2) + Rule 1 (1.6)
specialization_map       = { n: 36 }
proof_artifact_id        = "znorm-forall-proof/v1"
```

> **★ level を取り違えない**: `level: 18` の辺は **`level: 36` の辺の代用にならない**。両者は `parameters` が違う**別の capsule** である(F77-2.3)。

### 4.3 (E-iv) naming(命名規約)

```text
edge_id                  = "e-iv-naming/q9/v1"
source_object_ids[]      = [ <zeta_18^Rule の object ID>, <X_9 の object ID>, <tau の object ID> ]
target_object_id         = <marking equality の object ID>
operation                = name
parameters               = { correspondence: "zeta_M^Rule |-> X_q" }
theorem_or_definition_id = "family-Rule1/template/v1"      # (FR-5)
specialization_map       = { q: 9, M: 18 }
proof_artifact_id        = "definition"                    # 命名は群論から出ない(便 73 Q3.3)
```

> **★ 量と名前の分離(★教材 T5)**: `ord(X_9) = 18` は **HF-1(b) が与える量**で、**この capsule の内容ではない**。capsule が固定するのは**どの根を $X_9$ と呼ぶか**である。

---

## 5. 規律の自己申告

- **本 schema は数学を 1 行も証明していない。** 束縛するのは object identity・operation・specialization・証明への参照だけ。
- **`typed-edge/v1` 自体が未凍結**であり、capsule を載せる registry も未作成。**receipt が発行されるまで本稿は「案」である。**
- **UNKNOWN**: §2 の `operation` 列挙が三用途以外を尽くすかは**未検証**。新用途が出たら**列挙を増やすのではなく schema を版上げする**規律だけを先に置いた。
