# $K^{(9)}$ window-instance record(案 α)v2 — capsule 参照版

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 138-3)。v1 は不変(`docs/notes/k9_window_instance_v1.md`)。状態 = candidate。commit していない。**
**修理対象**: 便 77 **F77-2.1**(受領可能状態でない・`embedding_digest` 欄が無い・`family_clause_available=true` は現時点で偽)・**F77-2.2**(`restriction_equality` / `E-iv_marking_equality` が prose string → **不受理**)・**F77-2.3**(P4 は閉じない・$M=18$ root では $(Z_{36}$-link$)$ にならない)・**F77-2.4**(P5/P6/P7/P8-rule も未閉)・**F77-2.5**(schema と receipt が未凍結)。
**保持**(便 77 NOTE): WS-1〜3・WR-5・WI-1〜6 の fail-closed 思想、二段分離、`migrated_by_family_clause` の禁止、thin record が数学を再証明しない設計。
**規律**: $u$・封印量に触れていない。lane 実装・freeze 線文書に触れていない。

---

## 0. v1 → v2 の変更(4 行)

1. **`restriction_equality` / `E-iv_marking_equality` を prose から `typed-edge/v1` capsule 参照へ**(F77-2.2)。
2. **`embedding_digest` 欄を新設**し、**埋められる ID/digest はすべて埋めた**(F77-2.1)。**埋められない欄は「何の receipt 待ちか」を明記**した。
3. **`family_clause_available` を主張値から receipt 導出へ**(F77-2.1 後段 — family seal が `drafted / non-operative` の現時点で `true` は偽)。
4. **§4 に「P4 は level-36 restriction edge が別途必要($M=18$ root では不可)」を明記**(F77-2.3)。

---

## 1. 二段 status(**導出値・主張しない**)

```text
[window-status]
# v2: いずれも *導出* 値である。record が真理値を先取りして書かない。
family_clause_available      = derive( family_clause_receipt_id != null )
                               # 現在: family seal は drafted / non-operative
                               #       -> 導出結果 false(v1 は true と書いていた・自認)
migrated_via_family_instance = derive( this_record_receipt_id != null AND WI-1..WI-6 all pass )
                               # 現在: false
inventory_row_status         = not_assessed

family_clause_receipt_id     = ____________________   # 待ち: family-Rule1 seal v2 の event receipt
this_record_receipt_id       = ____________________   # 待ち: 本 record の receipt
```

| # | 条項 |
|---|---|
| **WS-1** | **`family_clause_available` から `migrated_via_family_instance` への自動遷移を置かない**(N76-4.2)。 |
| **WS-2** | **`migrated_by_family_clause` の語を使わない**(F76-4.1)。 |
| **WS-3** | **family TB4-E が各窓で compatibility を成立させたとは主張しない**(F76-4.2)。 |
| **WS-4** | **【v2 新設】status を record 本文に真理値として書かない。** 上の `derive(...)` は**受領側が receipt の有無から計算する**。**candidate に先取りした真理値を埋めない**(F77-2.1)。 |

---

## 2. record 本体(capsule 参照版)

```text
[window-instance-record]
schema_id            = "mb/window-instance/v2"
schema_digest        = ____________________   # 待ち: schema 凍結の receipt(F77-2.5)

window_id            = "K9"
n                    = 9
M                    = 18                     # = 2n
2M                   = 36                     # = 4n ・ (W2) の完全列と link の水準

# --- 普遍側(参照のみ・内容を複製しない: WR-1)---
family_clause_id     = "family-Rule1/template/v1"      # 便 76 N76-4.1 / seal v2 §1 と一致
family_clause_digest = ____________________   # 待ち: family-Rule1 seal v2 の post-apply digest
                                              #       (seal v2 §6.2 (3) を受領側が計算 -> receipt)

# --- Z-norm 側(既発効 object・新設しない)---
bar_iota_id                = "bar-iota/ext-of-iota-infty/v1"
znorm_event_receipt_id     = "znorm-event-receipt/v1"
znorm_event_receipt_digest = ____________________   # 待ち: Z-norm receipt の digest 転記
root_system_tb2_id         = "root-system/tb2/v1"    # profinite 根系(level 付き object ではない)

# --- 窓固有 object(本 record の実質)---
rule_root_id         = ____________________   # 待ち: level 36 の Rule 1 field-generator object の凍結(P7)
rule_root_digest     = ____________________
tb2_root_18_id       = ____________________   # 待ち: restrict(root-system/tb2/v1, level=18) の凍結(P6)
tb2_root_18_digest   = ____________________
tb2_root_36_id       = ____________________   # 待ち: restrict(root-system/tb2/v1, level=36) の凍結(P4 用・§4)
tb2_root_36_digest   = ____________________
embedding_id         = "family-rule1/embedding/j_9/v1"   # j_9 : K_9 = Q[T]/(Phi_36) -> Qbar
embedding_digest     = ____________________   # 待ち: j_9 object の凍結【v2 新設欄・F77-2.1】

# --- typed equality は capsule 参照で持つ(prose 禁止・F77-2.2)---
restriction_edge_id      = "family-rule1/restriction-compat/q9/v1"     # §3.1
restriction_edge_digest  = ____________________   # 待ち: capsule の receipt
e_iv_naming_edge_id      = "e-iv-naming/q9/v1"                          # §3.2
e_iv_naming_edge_digest  = ____________________   # 待ち: capsule の receipt

# --- 規則側(P8-rule)---
b_rule_commitment_id     = "rule1/7.1/b-rule-commitment/v1"
b_rule_commitment_digest = ____________________   # 待ち: family seal v2 §4 の receipt

# --- inventory ---
inventory_row_digest = ____________________   # 待ち: W3-19/20 の named-window inventory の K9 行
```

> **⛔ 削除した欄(v1 → v2)**: `restriction_equality` / `E-iv_marking_equality` の **prose string 2 欄**。**WI-4 に照らして不受理**であり(F77-2.2)、**§3 の capsule 参照が代わる**。

---

## 3. typed-edge capsule($q=9$ instance)

schema は `docs/notes/typed_edge_capsule_v1.md`(`typed-edge/v1`)。**本 record は capsule の ID/digest を参照するだけ**で、capsule 本体は別 artifact として凍結される。

### 3.1 `restriction_edge` — $\bar\iota\circ j_9=\iota_\infty^{(9)}$

```text
edge_id                  = "family-rule1/restriction-compat/q9/v1"
source_object_ids[]      = [ "bar-iota/ext-of-iota-infty/v1",
                             "family-rule1/embedding/j_9/v1" ]
target_object_id         = <iota_infty^{(9)} の object ID>       # 待ち: 凍結
operation                = compose
parameters               = { order: [ "family-rule1/embedding/j_9/v1",
                                      "bar-iota/ext-of-iota-infty/v1" ] }
theorem_or_definition_id = "family-Rule1/template/v1"            # (FR-1)(FR-2)(FR-2b)(FR-4)
specialization_map       = { q: 9, M: 18, 2M: 36 }
proof_artifact_id        = "definition"                          # FR-1 の選根からの一意性
proof_artifact_digest    = <family seal v2 の post-apply digest>  # 待ち
```

### 3.2 `e_iv_naming_edge` — $\tau(\zeta_{18}^{\rm Rule})=\tau(X_9)$

```text
edge_id                  = "e-iv-naming/q9/v1"
source_object_ids[]      = [ <zeta_18^Rule の object ID>,          # 待ち(rule_root_id からの導出物)
                             <X_9 の object ID>,                   # 待ち
                             <tau の object ID> ]                  # 待ち
target_object_id         = <marking equality object の ID>         # 待ち
operation                = name
parameters               = { correspondence: "zeta_M^Rule |-> X_q" }
theorem_or_definition_id = "family-Rule1/template/v1"             # (FR-5)
specialization_map       = { q: 9, M: 18 }
proof_artifact_id        = "definition"                           # 命名は群論から出ない(便 73 Q3.3)
proof_artifact_digest    = <family seal v2 の post-apply digest>   # 待ち
```

> **★ 量と名前の分離**: `ord(X_9) = 18` は **HF-1(b) の量**であって本 capsule の内容ではない。capsule が固定するのは**どの根を $X_9$ と呼ぶか**。

---

## 4. P4 は本 record では閉じない — **level 36 の restriction edge が別途要る**

> **★【v2 新設・F77-2.3】** $(Z_{36}$-link$)$ が要求するのは、**同一の profinite root system `"root-system/tb2/v1"` の level 36 への restriction** と、**Rule 1 の level 36 root** を結ぶ typed edge である。

```text
# P4 用に *別途* 要る capsule(本 record は参照するだけ・本 record では閉じない)
edge_id                  = "rule1-tb2-root-equality/level36/v1"
source_object_ids[]      = [ "root-system/tb2/v1" ]
target_object_id         = <level 36 の Rule 1 root object ID>     # = rule_root_id
operation                = restrict
parameters               = { level: 36 }
theorem_or_definition_id = "znorm-seal-final/v1"                   # 条 (1)(2) + Rule 1 (1.6)
specialization_map       = { n: 36 }
proof_artifact_id        = "znorm-forall-proof/v1"
```

| # | 条項 |
|---|---|
| **P4-1** | **$M=18$ の root artifact だけでは P4 にならない**(F77-2.3)。**`tb2_root_18_*` と `tb2_root_36_*` は別 object**であり、**前者で後者を代用しない**。 |
| **P4-2** | **family seal の存在だけで個別 migration を飛ばせない**(Z-norm seal の atomic clause (4))。**既存窓は migration/compatibility certificate まで従来 normalization に留まる。** |
| **P4-3** | **本 record は P4 を束縛しない。** 上の capsule と、`Z-norm-seal/v1` の $n=9$ migration certificate(案 α)は**別 receipt**である。 |

---

## 5. 残件の現況(**F77-2.4 の否認を受け入れる**)

> **⚠ v1 の誤り(自認)**: v1 §4 は「thin record は P6・P7 の 2 件を束縛する」と書き、司令塔経由で「seal 発効 + 本 record 受領後、T63-P1 の残件は P8-value だけ」という帰結が流れた。**便 77 F77-2.4 はこれを否認**した。**現時点で P4/P5/P6/P7/P8-rule/P8-value がそれぞれ open である。**

| 項目 | 現況 | 何の receipt 待ちか |
|---|---|---|
| **P4** $(Z_{36}$-link$)$ | **open** | §4 の level-36 capsule + $n=9$ migration certificate |
| **P5** (E-iv) instance | **open** | §3.2 capsule($X_9,\tau,\zeta_{18}^{\rm Rule}$ の object 凍結が先) |
| **P6** level-18 TB2 root | **open** | `tb2_root_18_*`(既発効 profinite root system からの restriction として) |
| **P7** level-36 Rule root | **open** | `rule_root_*` |
| **P8-rule** | **open** | family seal v2 §4 の `b_rule_commitment_*` |
| **P8-value** | **open**(将来測定・非前件) | 凍結 2 / BRIDGE-IN bundle。**この区分自体は正しい**(F77-2.4) |

---

## 6. 受領側の検査手順(v1 の WI-1〜6 を capsule 対応へ)

```text
WI-1  schema_id / schema_digest が window_instance_registry の型と一致
WI-2  family_clause_id が family_theorem_registry に実在し digest 一致
WI-3  bar_iota_id / znorm_event_receipt_id が既発効 object を指し digest 一致
        -> 別 extension ID の二本化を検出したら INTEGRITY_STOP(seal v2 ZB-2)
WI-4' restriction_edge_id / e_iv_naming_edge_id が typed-edge capsule を指し、
        capsule 側で TE-1..TE-8 が通ること
        -> prose string の等式宣言は不受理(TE-6)【v2: WI-4 を capsule 検査へ】
WI-5  inventory_row_digest を受領側が再計算して照合
WI-6  空欄が 1 つでもあれば migrated_via_family_instance を true にしない
WI-7' level 混同の検出【v2 新設】: tb2_root_18_* を P4 の根拠に使っていないこと
```

---

## 7. 規律の自己申告

- **v1 の 3 誤りを自認**: (a) `family_clause_available = true` を先取りで書いた(現時点で偽)、(b) typed equality を prose string で書いた(WI-4 に照らして自分の record が不受理だった)、(c) 残件を「P6・P7 の 2 件」と数え、下流に「残りは P8-value だけ」という誤った帰結を流した。
- **数学は 1 行も再証明していない**(N76-4.3 の趣旨)。束縛するのは object identity と capsule 参照だけ。
- **埋まっていない欄は 13**(§8)。**空欄を family clause で補わない**(WR-5)。
- **UNKNOWN**: `mb/window-instance/v2` schema・`window_instance_registry` の実体・record receipt の minted ID・受領時の canonical serialization は**未凍結**(F77-2.5)。**値を埋めるだけでは lifecycle が閉じない。**

---

## 8. 受領待ち一覧(**13 欄**)

| # | 欄 | 待っている receipt |
|---|---|---|
| 1 | `schema_digest` | `mb/window-instance/v2` の schema 凍結 |
| 2 | `family_clause_digest` | family-Rule1 seal v2 の event receipt(post-apply digest) |
| 3 | `znorm_event_receipt_digest` | Z-norm receipt からの転記 |
| 4 | `rule_root_id` | level 36 Rule 1 field-generator object の凍結(P7) |
| 5 | `rule_root_digest` | 同上 |
| 6 | `tb2_root_18_id` | `restrict(root-system/tb2/v1, level=18)` の凍結(P6) |
| 7 | `tb2_root_18_digest` | 同上 |
| 8 | `tb2_root_36_id` | `restrict(root-system/tb2/v1, level=36)` の凍結(P4 用) |
| 9 | `tb2_root_36_digest` | 同上 |
| 10 | `embedding_digest` | $j_9$ object の凍結 |
| 11 | `restriction_edge_digest` | §3.1 capsule の receipt |
| 12 | `e_iv_naming_edge_digest` | §3.2 capsule の receipt |
| 13 | `b_rule_commitment_digest` | family seal v2 §4 の receipt |
| (+) | `inventory_row_digest` | W3-19/20 の K9 行(受領側が再計算) |
