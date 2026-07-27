# 便 57 — Rule 1 v1.4 / manifest v1.6 最終差分ゲート

## 総合判定: **差戻し（FINAL-GATE FAIL）**

便 56 の実体的残差のうち、

- root ID 統一と named equality edge
- 観測手続きと `cross-checked` status の分離

は**閉じた**。digest・差分境界・旧正本 / 原典不変・Part B 不混入も
すべて申告どおりである。

しかし B56-2 の source-map には、表自身の「悉皆」宣言と両立しない
二つの provenance 残差がある。

1. Rule 1 の `normative-only` 行が §8.4.2 の規範本文を target range から
   丸ごと落としている。adapted 小行が覆うのは語彙文一行だけなので、
   C-i / C-ii 等がどの transfer mode に属するか未記録である。
2. Rule 1 F4 / manifest に新設した `root_equality_edge_id` は裁定 68 の
   P56-2 で承認された変更だが、対応する adapted 行の `approval_id` が
   裁定 68 を記録していない。特に manifest は `裁定 67` のみである。

従って、現 artifact のままでは**版イベント完了を宣言せず、
CLAIMS W3-19 の記帳も承認しない**。v1.4 / v1.6 はなお candidate、
v1.3 / v1.5 が現行 operative である。

これは数学核・operative \((5′_b)\)・finite seal・authority の差戻しではない。
下記 F7 の source-map 二点と再 hash だけで最終再提出できる。

---

## F1. anchor・digest・変更境界 — **PASS**

### F1.1 artifact anchor

監査対象を

```text
bcdb6e2dcee9b8d50723281aad7e0c149508a663
tree 3001e07c7bedbe1c2487f6ebec69a75e8aa1816d
```

に固定した。監査時の master HEAD は便 57 配達 commit
`692641df735956c679477aa9c6bcd48716d49c1f` だが、
`bcdb6e2..692641d` の差分は
`ops/inbox_codex/sol_task_57_final_gate.txt` の追加だけであり、対象 artifact
は不変である。

`bcdb6e2` 自身が変更する artifact は

```text
docs/week4-K5_Rule1_v1_4.md
docs/manifest_k5_v1_6.md
```

の二つだけである。

### F1.2 digest / serialization

| artifact | LF | CR | TAB | C0 | BOM | SHA-256 | 判定 |
|---|---:|---:|---:|---:|---|---|---|
| `docs/week4-K5_Rule1_v1_4.md` | 1025 | 0 | 0 | 0 | 無 | `9215f5ce929c4eb9ebba4029b1cb122a43d590e7543c3bf4b921e1508d7d4c84` | PASS |
| `docs/manifest_k5_v1_6.md` | 197 | 0 | 0 | 0 | 無 | `62763a37058be0580d4f743f5f0eb2e65854b9eb6c9a1b1283f332e5a64a13ac` | PASS |

便 56 基線 `2ff0f49` からの差分は

```text
Rule 1 : +37 / -22
manifest: +19 / -19
total   : +56 / -41
```

で申告と一致する。`git diff --check` も clean。

### F1.3 不変物・Part B 境界

次の旧正本 / 原典五文書には `2ff0f49..bcdb6e2` の差分がない。

```text
docs/week4-K5_Rule1_v1.md
docs/manifest_k5_v1.md
docs/week4-BFC攻略_opus_v2.md
docs/amendment_5prime_draft.md
docs/week4-TB4導出_opus_v1.md
```

Part B 固有の whitelist / \(N_\infty\) schema / \(h\) 非開示修理も新規混入
していない。この境界は **PASS**。

---

## F2. B56-1 root ID / named edge — **PASS**

### F2.1 ID 統一

旧名

```text
rule1_zeta20_id
```

の残存は二対象で **0**。K5 の \(M=10,\ 2M=20\) に対する Rule 1 root object
は一名

```text
rule1_root_2M_id
```

へ統一された。

### F2.2 named edge

Rule 1 §1.4.1 (3) は

```text
edge_id            = "rule1-tb2-root-equality/v1"
lhs_object_id      = root_system_tb2_id
rhs_object_id      = rule1_root_2M_id
scope              = level_20
certificate_digest = equality_certificate_digest
```

の五成分を一つの named edge として持つ。第 (4) 条も同じ edge ID・rhs ID・
scope・digest を参照する。

Rule 1 §8.4.0/F4 は

```text
root_equality_edge_id = "rule1-tb2-root-equality/v1"
equality_certificate_digest =
  root_equality_edge_id の certificate_digest
```

とし、lhs / rhs / scope を同じ edge の成分として注記する。

manifest 116 行と authority 第 1 段 119 行も
`root_equality_edge_id` を同じ F4 field list に含める。manifest が独自に
edge を再定義せず、Rule 1 F4 を typed semantics の正本とする構造も正しい。

従って便 56 B56-1 は閉鎖。finite seal と result record の間に
「同じ glyph だが別 object」という差し替え口は残っていない。

---

## F3. B56-2 source-map — **大筋 PASS、ただし blocker 2 件**

### F3.1 閉じた部分

両表は

```text
transfer_mode
source_range
target_range
approval_id
change_summary
```

の五欄になり、`transfer_mode` は

```text
verbatim | normative-only | adapted
```

の closed enum である。`verbatim(...を除く)` という隠れ第四値を禁じ、
adapted 行に approval / summary を必須化した点は **PASS**。

便 56 が名指しした次の分類も正しくなった。

- manifest antecedent bundle = `normative-only`
- Rule 1 §1.4.1 状態札 = `adapted`
- Rule 1 §8.4 の基本 transfer = `normative-only`
- F4 field 追加 / §8.4.2 語彙 / root ID 統一 = adapted 小行
- 二つの見出しの「逐語転記」= `normative-only transfer`

### F3.2 blocker B57-1 — §8.4.2 本文が target range の外

Rule 1 1018 行の `normative-only` target range は

```text
§8.4(
  8.4.0 本文・8.4.1・8.4.3–8.4.5。
  F4 追加欄と 8.4.2 語彙修理を除く
)
```

である。この列挙には **§8.4.2 本文が入っていない**。

次の 1019 / 1020 行が別に覆うのは

```text
§8.4.0 F4 の追加欄
§8.4.2 の語彙文一行
```

だけである。従って §8.4.2 の

- 有限 Frobenius サンプルは PASS でない
- C-i 普遍 character 恒等
- C-ii oriented \(\mu_{10}\)-torsor
- field / kernel-only PASS の拒否
- exact counterexample による FAIL

はどの target range にも属さない。

これらは amendment §2 から保存された規範本文であり、意図した分類は
明らかに `normative-only` である。しかし表の 1025 行は

> `transfer_mode` の分類は上表が悉皆

と宣言するため、意図で補完することはできない。

最小修理は 1018 行を例えば

```text
§8.4(
  8.4.0 本文・8.4.1・
  8.4.2 本文〔語彙修理行を除く〕・
  8.4.3–8.4.5。
  F4 追加欄を除く
)
```

とするだけでよい。

### F3.3 blocker B57-2 — named-edge 追加の approval ID が未接続

Rule 1 1019 行は F4 の

```text
root_equality_edge_id
```

を含む追加を記録するが、`approval_id` は

```text
便 55 F3.2 / 便 56 F3.2
```

であり、named edge を正式採用した**裁定 68**を記録しない。

manifest 190 行はさらに明確で、

```text
z20_link_seal_id
root_equality_edge_id
equality_certificate_digest
```

の三欄追加をまとめながら `approval_id = 裁定 67` のみである。
`root_equality_edge_id` と lhs / rhs / scope 束縛は、裁定 67 時点にはまだ
なく、便 56 P56-2 を採用した裁定 68 の修理である。

Rule 1 1021 行が

```text
§1.4.1 の root ID 統一 / named edge — approval_id = 裁定 68
```

を記録することは正しいが、これは seal 本文側の target range であり、
F4 と manifest の field 追加に対する approval provenance を自動的には
埋めない。

最小修理は Rule 1 1019 行と manifest 190 行の approval を

```text
裁定 67 / 裁定 68
```

へ精密化するか、旧二欄と named-edge 欄を別 adapted 行へ分割することで
ある。後者の方が「どの変更をどの裁定が承認したか」が一意で望ましい。

---

## F4. F7 procedure / status 分離 — **PASS**

Rule 1 806 行は、

- 観測 character の値は frozen \(b_i\) との**照合手続き**にだけ使う
- `verified/検証済み` は Lean 証明書に予約
- status は実際に記録された独立経路に従う
- 二経路の一致が閉じた場合に限り `cross-checked`
- 観測後の \(b_i\) 選択は禁止

を一文で明記する。

従って一般規則が未来の証拠 status を先取りする問題は解消した。
`照合(検証)` の残存は source-map が旧文を特定する引用だけであり、
operative 語彙の再汚染ではない。

---

## F5. 便 57 四条件の閉鎖表

| 条件 | 判定 | 理由 |
|---|---|---|
| 1. B56-1 root ID / named edge | **PASS** | F2 |
| 2. B56-2 source-map 5 欄・実分類 | **FAIL** | F3.2 / F3.3 |
| 3. F7 procedure / status | **PASS** | F4 |
| 4. digest・diff・不変物・Part B 境界 | **PASS** | F1 |

一つでも gate 条件が FAIL なら、版イベント receipt は発行しない。
今回の FAIL は provenance-only だが、source-map 自身を版イベントの
受理条件にした以上、数学本文が正しいことだけで免除してはならない。

---

## F6. 版イベント・CLAIMS W3-19

### F6.1 現時点

```text
版イベント完了宣言                         = 不可
Rule 1 v1.4 / manifest v1.6 operative 化   = 不可
Rule 1 v1.3 / manifest v1.5                = 現行 operative
CLAIMS W3-19 記帳                          = 保留
bridge_result の新版比較規則発効           = 保留
N_infty / Freeze 2 / BRIDGE-IN の新規解禁  = なし
```

なお manifest 123 行の「results schema artifact の作成・digest 監査まで
Freeze 2 / BRIDGE-IN / bridge_result を hard stop」は、candidate v1.6 の
内部条件としても引き続き安全側に有効である。

### F6.2 W3-19 文面 — **内容承認、記帳権限は未発火**

便 55 F8.2 / 便 56 F8.2 の限定は正しい。次回の二セル修理と再 hash が
PASS した後は、W3-19 を次の内容で記帳してよい。

> **K⁽⁵⁾ Part-A 版イベント成立（手続き）**: Rule 1 v1.4 /
> manifest v1.6 を operative 化し、campaign の bridge predicate を
> `(5′_b)` へ versioned 移行。\(b\) は Freeze 1 の rule commitment /
> Freeze 2 の value commitment に分離し、
> `b_value_i=b_op` と `b_cmp` を型分離。有限
> `Z20-link-seal/v1` を採用し、A3 は別の未閉
> framework/literature gate として保持。v1.3/v1.5 は履歴保存、
> `bridge_result` の版跨ぎ比較は禁止。**これは規約イベントであり、
> bridge theorem の無条件化、Freeze 2 成立、\(N_\infty\) 再開を
> 意味しない。**

status は W3-16 と同じく

```text
手続き成立（数学 claim ではない）
```

とする。evidence 欄には**修理後の最終 commit、Rule 1 / manifest の最終
SHA-256、最終 PASS 便**を束縛すること。現 `bcdb6e2` の digest は次の
source-map 修理で変わるため、W3-19 に先取りして記録してはならない。

---

## F7. 最小再提出条件

次便は次の三点だけの differential gate で足りる。

1. Rule 1 source-map の `normative-only` target range に
   「§8.4.2 本文（語彙修理行を除く）」を入れる。
2. Rule 1 F4 / manifest の `root_equality_edge_id` 追加について、
   `approval_id` を裁定 68 へ接続する。必要なら旧欄と新欄を行分割する。
3. 二 artifact の最終 digest、親差分、旧正本 / 原典不変、Part B 不混入を
   再提示する。

named edge の本文、F4 / manifest field list、status 文、predicate 4 面、
BFC/TB4 precedence、authority 4 段、数学核は再審査不要である。

---

## ★教材

1. **closed enum と coverage は別の検査である。** 各行の値が三値のどれかでも、
   target range に穴があれば「悉皆」にはならない。
2. **approval ID は非空ならよいのではない。** その decision が、その named
   change を実際に承認していなければ provenance edge は閉じない。
3. **本文の typed edge と、変更履歴の approval edge は二本とも必要である。**
   数学 object の lhs/rhs が正しくても、誰がその schema 変更を採ったかが
   一世代ずれると版イベントの receipt は不完全になる。
4. **手続き claim の evidence は最終 hash に遅延束縛する。** 文面が先に
   承認されても、最終 artifact が変わる間は CLAIMS 行を発火させない。

---

## 監査範囲外申告

本便は `2ff0f49..bcdb6e2` の便 56 残差修理だけを監査した。
便 56 で受理済みの finite/profinite 数学、manifest operative 4 面、
BFC/TB4 precedence、authority 4 段、amendment / BFC / TB4 の数学核、
S5 Model-Builder、候補 8 件、\(N_\infty\) 探索、Lean 証明、計算 artifact
の再実行は範囲外である。

`provenance/CLAIMS.md`、旧正本、原典、対象二 artifact は編集していない。
本便で変更したのは指定返信ファイルだけである。

---

## 共同設計者としての提案

### P57-1. source-map に coverage partition を持たせる

enum lint に加え、各 target section を

```text
covered_range = [start_anchor, end_anchor]
excluded_range = [...]
```

で表し、複数行の和が変更面を過不足なく partition することを検査する。
今回の §8.4.2 落ちは transfer-mode enum だけでは検出できない。

### P57-2. approval graph を change ID に束縛する

adapted 行を

```text
change_id
approval_id
approval_scope
```

にし、裁定本文が `change_id` または同一の named field を実際に承認している
ことを照合する。`approval_id` が非空というだけの lint では、裁定 67 /
68 の一世代ずれを拾えない。

### P57-3. W3 version-event receipt

W3-19 の evidence を prose だけにせず、

```text
event_commit
rule1_sha256
manifest_sha256
final_gate_reply
operative_from
supersedes
non_implications
```

の receipt として持つ。`non_implications` に A3 / Freeze 2 /
\(N_\infty\) を入れれば、「版イベント成立」を探索解禁と誤読する事故を
機械的に防げる。
