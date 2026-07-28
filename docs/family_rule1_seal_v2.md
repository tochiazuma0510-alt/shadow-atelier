# `family-Rule1/template/v1`(普遍 family Rule 1 条項)— **seal v2**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 138-2)。v1 は不変(`docs/family_rule1_seal_v1.md`)。状態 = candidate。commit していない。**
**修理対象**: 便 77 **F77-1.1**($\bar\iota|_{K_q}$ が typed equality でない)・**F77-1.2**(既発効 Z-norm seal と同じ $\bar\iota$ を指していない)・**F77-1.3**(P8-rule が射程外)・**F77-1.4**(apply transaction の最終 blob が一意でない)。
**保持**: **F77-1.5**(FR-1〜FR-5 の数学的骨格と non_implications 八項は妥当 → **不変**)・**F77-1.6**(意味 ID `family-Rule1/template/v1` を維持・**ID は不変のまま digest を external receipt が束縛**)・**F77-1.7**(`w2fam`/`w2arith` を `[downstream-related-artifacts]` へ移す)。
**規律**: $u$・封印量に触れていない。外部文献なし。**条項本体(FR-1〜FR-5)の数学は v1 から 1 行も変えていない。**

### 状態欄

```text
status_now        = drafted / unapproved / non-operative
clause_provenance = docs/notes/i2_family_rule1_memo_v2.md
supersedes_draft  = docs/family_rule1_seal_v1.md          # 便 77 F77-1 で処方つき FAIL

# 発効時(§6 の apply transaction が定める順序でのみ記入)
status_on_apply   = ____________________
applied_at        = ____________________
event_receipt_id  = ____________________
```

> **⚠ digest 自己参照禁止**(便 61 A61-2): 本 seal は**自らの digest を含まない**。authority は **external event receipt**。

---

## 1. 条項本体(**v1 から不変** — 再掲のみ)

```text
family-Rule1/template/v1  (scope = family, quantifier = "for all odd q >= 3"):
  (FR-1) 補題 U による iota_infty の指定
  (FR-2) K_q := Q[T]/(Phi_{4q}),  zeta_{4q}^Rule := T-bar,  iota_infty^{(q)}
  (FR-3) M := 2q, 2M := 4q,  zeta_M^Rule := (zeta_{2M}^Rule)^2,  ord = M
  (FR-4) [制限] —— v2 で typed 化(§2)
  (FR-5) (E-iv) 命名条項:  iota: mu_M --~--> <X_q>,  zeta_M^Rule |--> X_q
```

**FR-1・FR-2・FR-3・FR-5 の文言は v1 のまま**(便 77 F77-1.5 が「指定された射程では妥当」と判定)。**v2 が変えるのは FR-4 の型付けと、§3〜§6 の束縛・手続きである。**

---

## 2. 【F77-1.1 修理】FR-4 を typed edge にする

> **⚠ v1 の欠陥(自認)**: v1 の FR-4 は $\bar\iota|_{K_q}=\iota_\infty^{(q)}$ とだけ書き、**$K_q$ が $\bar\iota$ の定義域の部分体であるという未記載の同一視**を含んでいた。$K_q$ は FR-2 で**抽象商** $\mathbb Q[T]/(\Phi_{4q})$ として定義されるので、この同一視は自明でない。

### 2.1 矢印 $j_q$ の定義(FR-1/FR-2 の選根から)

```text
(FR-2b) [embedding arrow] —— v2 新設
        j_q : K_q  ↪  Qbar
        定義:  j_q(zeta_{4q}^Rule) = j_q(T-bar) := (FR-1) が N = 4q で一意に指定する
                                                   Phi_{4q} の根(Im > 0 かつ Re 最大)
        # Phi_{4q} は T-bar の最小多項式なので、生成元の像を指定すれば j_q は一意に決まる。
        # すなわち j_q は FR-1 の選根から *定義* される矢印であり、新しい仮定ではない。
```

### 2.2 FR-4 の typed 形

```text
(FR-4) [制限 —— typed] —— v2 で書き換え
       bar_iota ∘ j_q = iota_infty^{(q)}          as embeddings K_q -> C
       # v1 の "bar_iota|_{K_q} = iota_infty^{(q)}" は本式の略記である。
       # 左辺の合成は typed-edge capsule (operation = compose) が束縛する。
```

**この等式を束縛する capsule**(`typed-edge/v1`・`docs/notes/typed_edge_capsule_v1.md`):

```text
edge_id                  = "family-rule1/restriction-compat/v1"
source_object_ids[]      = [ bar_iota_id, j_q_id ]
target_object_id         = <iota_infty^{(q)} の object ID>
operation                = compose
parameters               = { order: [ j_q_id, bar_iota_id ] }
theorem_or_definition_id = "family-Rule1/template/v1"      # (FR-1)(FR-2)(FR-2b)
specialization_map       = { q: <奇数> }
proof_artifact_id        = "definition"                    # 選根からの一意性(FR-1)
```

> **★ 生成元上の等式へ縮める場合の条件**(F77-1.1 末尾): **左右の object ID と `generator = T-bar` を同じ certificate が束縛**しなければならない。上の capsule は `source_object_ids[]` にそれを持つ。**prose の「制限が一致する」だけでは不受理**(TE-6)。

---

## 3. 【F77-1.2 修理】既発効 Z-norm seal への束縛(**6 欄**)

> **⚠ v1 の欠陥(自認)**: v1 は記号 $\bar\iota$ を使うだけで、`docs/znorm_seal_final_v1.md` が発効済み object として束縛する ID・receipt・profinite root system を**参照していなかった**。「どちらも $\iota_\infty$ の延長」という**値レベルの説明**だけでは、**別 extension ID を二本作れる**という Z-norm seal §4 の禁止を再び開ける(同 §2 の注記「値の等式では足りない」)。

```text
[znorm-binding]   —— v2 新設・normative
bar_iota_id                = "bar-iota/ext-of-iota-infty/v1"     # 既発効 object(新設・改名しない)
znorm_event_receipt_id     = "znorm-event-receipt/v1"
znorm_event_receipt_digest = ____________________________________  # receipt が記入
j_q_id                     = "family-rule1/embedding/j_q/v1"
j_q_definition             = "j_q(T-bar) := FR-1 の選根 (N = 4q)"   # §2.1 と逐語一致
restriction_edge_id        = "family-rule1/restriction-compat/v1"
restriction_edge_digest    = ____________________________________  # receipt が記入
```

| # | 条項 |
|---|---|
| **ZB-1** | **`bar_iota_id` は既発効の `"bar-iota/ext-of-iota-infty/v1"` を指す。** 本 seal は $\bar\iota$ を**新設しない**(Z-norm seal §2-b の identity binding を継承)。 |
| **ZB-2** | **別 extension ID の二本化を禁止する。** 「$\iota_\infty$ の延長である」という**値の性質**を根拠に新しい ID を作ってはならない(F77-1.2)。 |
| **ZB-3** | **`znorm_event_receipt_digest` が空の間、本 seal は $\bar\iota$ を参照する条項を operative にできない。** Z-norm receipt が先、本 seal が後。 |
| **ZB-4** | **`j_q_definition` は §2.1 と逐語一致**でなければならない。二箇所で文言が割れたら不受理。 |
| **ZB-5** | **profinite root system(`"root-system/tb2/v1"`)への参照は本 seal の射程外**である。**level 付き root object の束縛は窓別 record 側**で行う(混同すると P4 を飛ばす経路になる — 便 77 F77-2.3)。 |

---

## 4. 【F77-1.3 修理】P8-rule 欄

> **⚠ v1 の欠陥(自認)**: v1 の non_implications は **P8-value** を前件から正しく外していたが、それは **P8-rule**(Rule 1 v1.5 §7.1 の `b_rule_commitment`)の digest を供給したことにはならない。**FR-1〜FR-5 は選根・体・$\zeta_M$・embedding compatibility・(E-iv) を扱うだけで、$b$ の決定規則には触れていない。**

```text
[p8-rule-binding]   —— v2 新設・normative
b_rule_commitment_id     = "rule1/7.1/b-rule-commitment/v1"      # Rule 1 v1.5 §7.1 の *規則*
b_rule_commitment_digest = ____________________________________  # receipt が記入
rule1_v1_5_digest        = ____________________________________  # Rule 1 v1.5 の exact blob digest
```

| # | 条項 |
|---|---|
| **PR-1** | **`b_rule_commitment` は「規則」であって「値」ではない**(条文案 A (F1)/(F2) の用語規律)。**規則は窓非依存**なので family theorem registry に束縛してよい。 |
| **PR-2** | **P8-value(actual $b_i$)は本 seal の射程外**であり、**non_implications に残す**(§5)。**規則を供給したことで値を供給したと読まない。** |
| **PR-3** | 上の 3 欄を本 seal に置く代わりに、**別の発効済 family rule artifact を参照してもよい**(F77-1.3 の二択)。**その場合は artifact の ID+digest をここに書き、内容を複製しない。** |

---

## 5. non_implications(**v1 から不変・八項を保持**)

```text
non_implications = [
  "各窓の (E-iii) 供給",
  "P8-value —— actual b_i の測定。予言後の照合側 payload",
  "A3 —— framework gate は未閉(文献要請 13(ii))",
  "Lean verified —— 本 seal は paper-proof candidate",
  "任意の窓の migrated —— FS-1/FS-2/FS-3",
  "family TB4-E の無条件性 —— FS-4",
  "測定側 (B-ii)-(B-iv) の族化",
  "(5') の任意の窓での instance"
]
```

**追加(v2)**:
```text
non_implications += [
  "level 付き root object の束縛 —— ZB-5。窓別 record の (Z_{2M}-link) を飛ばさない",
  "P8-value —— PR-2。規則の供給は値の供給ではない"
]
```

---

## 6. 【F77-1.4 修理】apply transaction の確定

> **⚠ v1 の欠陥(自認)**: v1 は空欄を持つだけで、**どの空欄を apply が変更できるか・receipt ID をいつ mint するか・post-apply digest を誰が計算するか・receipt が何を束縛するか**が固定されていなかった。**承認前 hash と発効後 hash を混同しうる。**

### 6.1 allowed delta(**apply が変更してよい欄の閉じた列挙**)

```text
[allowed-delta]   # これ以外の欄を apply で変更したら transaction は無効
status_on_apply
applied_at
event_receipt_id
znorm_event_receipt_digest        # §3
restriction_edge_digest           # §3
b_rule_commitment_digest          # §4
rule1_v1_5_digest                 # §4
[dependency-digests] の各 *_sha256 欄   # §7
```

| # | 条項 |
|---|---|
| **AT-1** | **上の列挙以外の欄(条項本体 FR-1〜FR-5・§2 の型・§3 の ID・§5 の non_implications)を apply が変更してはならない。** 変更が必要ならそれは apply ではなく**版上げ**である。 |
| **AT-2** | **`event_receipt_id` は事前 mint 値 `"family-rule1-event-receipt/v1"` と一致すること**(Z-norm seal §9 の先例に倣う)。apply 時に新規採番しない。 |

### 6.2 順序(**一本化**)

```text
(1) dependency 確定
      §3 / §4 / §7 の全 *_digest を、各 artifact の exact blob から受領側が算出して確定する。
      -> 1 つでも空なら (2) へ進まない(fail-closed)。
(2) apply
      [allowed-delta] の欄だけを書き込む。他の欄は 1 バイトも変えない。
(3) sha256(post-apply blob)
      apply 後の本 seal の exact blob の sha256 を *受領側が* 計算する。
      -> これが seal の digest である。承認前 blob の digest とは別物であり、混同しない。
(4) receipt
      event receipt が次を束縛して発行される:
        - post_apply_seal_digest   ((3) の値)
        - 全 dependency digest     ((1) の値)
        - event_receipt_id         (AT-2 の事前 mint 値)
        - status_on_apply / applied_at
```

| # | 条項 |
|---|---|
| **AT-3** | **(3) を producer(起草者)が計算して本文へ書くことを禁止**する(自己参照禁止)。**受領側が計算し receipt が持つ。** |
| **AT-4** | **(1) が閉じる前に (2) を始めない。** 便 77 §1 結論「v2 で F77-1.1–1.4 を閉じるまで apply transaction を開始しない」を条文化。 |
| **AT-5** | **承認前 hash を receipt に書かない。** receipt が束縛するのは **post-apply digest のみ**。 |

---

## 7. dependency と downstream の分離(**F77-1.7 修理**)

```text
[dependency-digests]   # 本 seal (FR-1)-(FR-5) の *証明* が依存するもの
lemma_U_proof_id       = "i2-family-rule1-memo/v2"
lemma_U_proof_path     = docs/notes/i2_family_rule1_memo_v2.md
lemma_U_proof_sha256   = ____________________________________

hfun_id                = "hfun-functoriality/v1"          # FR-5 の ord(X_q) = 2q
hfun_path              = docs/notes/hfun_functoriality_v1.md
hfun_sha256            = ____________________________________

[downstream-related-artifacts]   # 併用するが本 seal の受領条件ではない(F77-1.7)
w2_fam_id              = "W2-fam/group-side/v1"     path = docs/notes/w2fam_v1.md
w2_arith_id            = "W2-1/arith-side/v1"       path = docs/notes/w2arith_v1.md
```

> **★ v1 からの移動(自認)**: v1 は `w2fam`/`w2arith` を `[dependency-digests]` に置いていた。**両者は (FR-1)–(FR-5) の証明に使わず、下流の (5′) 組立で併用する資料**なので、**receipt-blocking ではない欄へ移した**(F77-1.7)。

---

## 8. 規律の自己申告

- **v1 の 4 欠陥を自認**: FR-4 の未記載同一視(F77-1.1)・Z-norm object への未束縛(F77-1.2)・P8-rule の欠落(F77-1.3)・apply 手順の未確定(F77-1.4)。
- **条項本体の数学は 1 行も変えていない。** v2 が加えたのは **矢印 $j_q$ の定義(FR-2b)**、**FR-4 の typed 形**、および §3・§4・§6 の束縛と手続きである。
- **意味 ID は `family-Rule1/template/v1` のまま**(F77-1.6)。**ID を版で変えない** — 修理版の exact digest を external receipt が束縛する。
- **UNKNOWN**: `typed-edge/v1` schema 自体が未凍結(`docs/notes/typed_edge_capsule_v1.md` も candidate)。**capsule schema の receipt が先に要る。**
- **本 seal は依然 `drafted / non-operative`。** AT-4 により、dependency が確定するまで apply を開始しない。
