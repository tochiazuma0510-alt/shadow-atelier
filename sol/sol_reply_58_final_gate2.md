# 便 58 — Rule 1 v1.4 / manifest v1.6 最終差分ゲート 2

## 総合判定: **PASS**

便 57 で残した二セルは、commit
`507d65931035c74f191a097ceb689f3894a1fac2` で指定どおり閉じた。

- Rule 1 §8.4.2 の規範本文が `normative-only` coverage に入った。
- Rule 1 F4 / manifest の旧二欄（裁定 67）と
  `root_equality_edge_id`（裁定 68）が別 adapted 行へ分離された。

差分は source-map のみで、数学・規範本文への変更はない。digest、差分量、
旧正本 / 原典不変、Part B 不混入もすべて一致した。

従って、ここに

```text
K^(5) Part-A 版イベント = 完了
Rule 1 v1.4              = operative
manifest v1.6            = operative
Rule 1 v1.3              = 凍結履歴
manifest v1.5            = 凍結履歴
CLAIMS W3-19 記帳         = 承認
```

を宣言する。`bridge_result` の版跨ぎ比較禁止も発効する。

この PASS は手続きイベントの成立であり、A3 の閉鎖、bridge theorem の
無条件化、Freeze 2 成立、\(N_\infty\) 再開を意味しない。

---

## F1. anchor・digest・変更境界 — **PASS**

### F1.1 artifact anchor

監査対象を

```text
commit 507d65931035c74f191a097ceb689f3894a1fac2
tree   6df144e5a2f13e97440b56e55687d766db71cbfc
```

に固定した。

監査時の master HEAD は便 58 配達 commit
`4ed2bf8f8d52eda352b99243779e3fdf084d740c` だが、
`507d659..4ed2bf8` の差分は
`ops/inbox_codex/sol_task_58_final_gate2.txt` の追加だけであり、対象
artifact は不変である。

`507d659` の直接親は便 57 配達 commit `692641d...`、artifact の監査基線は
`bcdb6e2` である。対象 commit が変更するのは指定二 artifact だけ。

### F1.2 digest / serialization

| artifact | LF | CR | TAB | C0 | BOM | SHA-256 | 判定 |
|---|---:|---:|---:|---:|---|---|---|
| `docs/week4-K5_Rule1_v1_4.md` | 1026 | 0 | 0 | 0 | 無 | `d99c75940b6132aa46336f489ebebf957d37f2cf198d8e174cff5a2e79eb1f71` | PASS |
| `docs/manifest_k5_v1_6.md` | 198 | 0 | 0 | 0 | 無 | `b392f4a54223310185288301a318493be67ceb64799bd42fde5cbca0d823fbea` | PASS |

`bcdb6e2..507d659` の差分は

```text
Rule 1 : +3 / -2
manifest: +2 / -1
total   : +5 / -3
```

で申告と一致する。`git diff --check` も clean。

### F1.3 不変物

次の旧正本 / 原典五文書には artifact 基線からの差分がない。

```text
docs/week4-K5_Rule1_v1.md
docs/manifest_k5_v1.md
docs/week4-BFC攻略_opus_v2.md
docs/amendment_5prime_draft.md
docs/week4-TB4導出_opus_v1.md
```

Part B 固有の whitelist / \(N_\infty\) schema / \(h\) 非開示修理も混入して
いない。

---

## F2. B57-1 — §8.4.2 coverage — **PASS**

Rule 1 source-map の `normative-only` target range は

```text
§8.4(
  8.4.0 本文・8.4.1・
  8.4.2 本文〔語彙修理行を除く〕・
  8.4.3–8.4.5。
  F4 追加欄を除く
)
```

へ修理された。

これにより §8.4.2 の

- 有限 Frobenius サンプルは PASS の証明でない
- C-i 普遍 character 恒等
- C-ii oriented \(\mu_{10}\)-torsor
- field / kernel-only PASS の拒否
- fixed \(b_i\) に対する exact counterexample による FAIL

が `normative-only` coverage に入る。一方、語彙修理行は直後の adapted 行が
別に覆う。F4 追加欄も二つの adapted 行が覆う。

従って §8.4 の target range は、便 57 が問題にした穴について過不足なく
partition され、末尾の「分類は悉皆」という確認と整合する。

---

## F3. B57-2 — approval provenance の行分割 — **PASS**

### F3.1 Rule 1

F4 追加欄は次の二行へ分離された。

| target | approval |
|---|---|
| `z20_link_seal_id`・`equality_certificate_digest` | 便 55 F3.2（裁定 67） |
| `root_equality_edge_id` | 裁定 68（便 56 F3.2 / P56-2） |

後者の change summary は named edge
`rule1-tb2-root-equality/v1` の lhs / rhs / scope / digest 束縛と、
Rule 1 F4 / manifest の同一 field 名参照を明示する。

### F3.2 manifest

manifest も同じ二行分割を採る。

| target | approval |
|---|---|
| digest 束縛欄の `z20_link_seal_id`・`equality_certificate_digest` | 裁定 67 |
| digest 束縛欄の `root_equality_edge_id` | 裁定 68 |

従って「古い二欄を採った裁定」と「named edge へ型強化した裁定」が
一世代ずれずに記録された。便 57 B57-2 は閉鎖。

---

## F4. 非回帰確認 — **PASS**

本差分は二つの source-map block に限定され、次には触れていない。

- `Z20-link-seal/v1` の finite level-20 型
- `rule1_root_2M_id` と named equality edge の定義
- Rule 1 F4 / manifest field list
- operative \((5′_b)\) と C-i / C-ii
- manifest 下流 4 面
- BFC v2.11 未同期 / TB4 v2.4 precedence
- schema authority 4 段
- results schema 実体化までの hard stop
- procedure / `cross-checked` status 分離

従って便 56 / 57 で受理済みの部分に意味的回帰はない。

source-map に残る `同上` / `同 §...` は人間には一意に読め、本差分による
分類反転もないため今回の blocker としない。ただし P58-1 のとおり、
machine-readable 化の次段では explicit path へ正規化するのが望ましい。

---

## F5. 版イベント完了宣言

本 PASS をもって、K⁽⁵⁾ Part-A の版イベントは完了した。

### F5.1 operative / history

```text
operative:
  docs/week4-K5_Rule1_v1_4.md
  docs/manifest_k5_v1_6.md

frozen history:
  docs/week4-K5_Rule1_v1.md   # Rule 1 v1.3
  docs/manifest_k5_v1.md      # manifest v1.5
```

旧版を削除・上書きしない。新旧の `bridge_result` は、列名が同じでも
predicate version が異なるため比較禁止である。

### F5.2 発効する規約

- campaign の operative bridge predicate は \((5′_b)\)。
- \(b\) は Freeze 1 の rule commitment と Freeze 2 の value commitment に
  分離。
- `b_value_i=b_op`、`b_cmp` は別 typed field。
- finite `Z20-link-seal/v1` を採用。
- result record は Rule 1 / manifest の最終 digest と schema digest を束縛。
- bundle ID / exact route / certificate type は v1.6 の規則に従う。
- version を跨いだ `bridge_result` 比較は禁止。

---

## F6. CLAIMS W3-19 — **記帳承認**

### F6.1 記帳本文

次の本文を W3-19 として記帳してよい。

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

status は

```text
手続き成立（数学 claim ではない）
```

とする。

### F6.2 evidence receipt

W3-19 の evidence 欄には少なくとも次を束縛すること。

```text
event_commit =
  507d65931035c74f191a097ceb689f3894a1fac2

rule1_artifact =
  docs/week4-K5_Rule1_v1_4.md
rule1_sha256 =
  d99c75940b6132aa46336f489ebebf957d37f2cf198d8e174cff5a2e79eb1f71

manifest_artifact =
  docs/manifest_k5_v1_6.md
manifest_sha256 =
  b392f4a54223310185288301a318493be67ceb64799bd42fde5cbca0d823fbea

final_gate_reply =
  sol/sol_reply_58_final_gate2.md

operative_from =
  便 58 PASS

supersedes_for_operation =
  Rule 1 v1.3 / manifest v1.5

non_implications =
  A3 is not closed
  bridge theorem is not unconditional
  Freeze 2 is not complete
  N_infty is not reopened
```

これが P57-3 の version-event receipt である。

---

## F7. 継続する hard stop

版イベント完了と、探索 / 結果受理の解禁は別である。

次は引き続き有効。

1. A3 は未閉 framework/literature gate。
2. `provenance/results_k5.md` または専用 schema artifact の作成・digest
   監査が閉じるまで、Freeze 2 / BRIDGE-IN / `bridge_result` 記録は
   hard stop。
3. \(N_\infty\) schema / run / certificate は別ゲートまで隔離。
4. bound \(\le 5\) の既観測から \(N_\infty\) の不存在を結論しない。
5. W3-19 は数学的飽和、個別 bridge PASS、候補受理を主張しない。

---

## ★教材

1. **coverage と approval を別々に閉じて初めて provenance が完結する。**
   何を転記したかだけでなく、どの世代の裁定がどの field を採ったかを
   partition する必要がある。
2. **最終 receipt は最終 hash に束縛する。** 文面が先に合意されていても、
   source-map 一セルの変更で artifact digest は変わる。
3. **版イベントの PASS は数学定理の PASS ではない。** operative predicate と
   記録規則が確定したこと、未閉 gate がどれかを固定したことが成果である。
4. **差分ゲートの終点を明示する。** 二セルが閉じた後に受理済み数学核を
   再び開かず、残る停止札を receipt の `non_implications` に移す。

---

## 監査範囲外申告

本便は `bcdb6e2..507d659` の source-map 二セルだけを監査した。
便 56 / 57 で受理済みの finite seal、named edge 本文、operative 4 面、
precedence、authority、BFC / amendment / TB4 の数学核、S5 Model-Builder、
候補 8 件、\(N_\infty\) 探索、Lean 証明、計算 artifact の再実行は
範囲外である。

`provenance/CLAIMS.md` や対象 artifact は編集していない。W3-19 は本返信で
**記帳を承認**したのであり、実際の台帳編集は司令塔の仕事である。

作業開始時から未追跡だった過去記録
`sol/sol_reply_57_final_gate.md` には触れていない。本便で新規作成したのは
指定返信 `sol/sol_reply_58_final_gate2.md` だけである。

---

## 共同設計者としての提案

### P58-1. source path の explicit 化

五欄表を真に機械可読にする段では、`同上` / `同 §...` を禁止し、

```text
source_artifact
source_anchor
```

を各行に完全展開する。行挿入で相対参照先がずれる事故を防げる。
今回の PASS 条件ではないが、次回 source-map linter の安い強化である。

### P58-2. coverage receipt の固定

source-map に

```text
coverage_id
covered_target_anchors
excluded_target_anchors
```

を持たせ、行の union が変更面をちょうど一度覆うことを検査する。
P57-1 の実装形であり、§8.4.2 のような中間節落ちを自動検出できる。

### P58-3. W3 event と結果 schema の二段 receipt

今回の W3-19 を

```text
VERSION-EVENT/PART-A
```

とし、将来 results schema artifact が閉じた時は別の

```text
RESULT-SCHEMA-READY
```

receipt を発行する。版イベント成立だけで Freeze 2 が解禁されたように
見える事故を、状態機械として防げる。
