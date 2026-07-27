# 便 56 — APPLY-GATE 2 差分監査

## 総合判定: **差戻し**

便 55 の二つの数学的 blocker、

1. finite `Z20-link-seal/v1` と full `(Z-norm)` の型衝突
2. manifest 下流 4 面に残った旧 operative `(5′)` / field-only PASS

は、いずれも**数学的内容としては閉じた**。BFC v2.11 と TB4 v2.4 の
precedence、結果 schema の authority 4 段、実体化までの hard stop も
指定どおり入っている。

しかし、版イベントを完了させるには次の二点がまだ blocker である。

- `Z20-link-seal/v1` 内の `rule1_zeta20_id` と、Rule 1 F4 / manifest の
  `rule1_root_2M_id` が**同一 object であるという typed alias がない**。
  equality certificate の digest は追加されたが、その右辺 object ID が
  結果 record の ID に束縛されていない。
- 出所対応表は三値の定義を追加しただけで、便 55 F5 が具体的に指摘した
  Rule 1 §8.4 と manifest antecedent bundle をなお `verbatim` としている。
  また、TB4 の状態札を finite seal 用に意味適応した行も `verbatim` の
  ままである。

したがって、現時点では**版イベント完了を宣言しない**。
Rule 1 v1.4 / manifest v1.6 を operative にせず、CLAIMS W3-19 の記帳も
承認しない。v1.3 / v1.5 が引き続き現行受理版であり、
\(N_\infty\) 停止と Freeze 2 hard stop はそのまま継続する。

---

## F1. anchor・digest・差分境界 — **PASS**

### F1.1 commit anchor

監査対象を

```text
2ff0f4929d286c28349f965533db5446777c10ae
tree f138e12dd74950fe025011dac615461b22155534
```

に固定した。監査時の作業木 HEAD は便 56 配達 commit
`91927ed382bf943125ea9fe5bcce524d18af692c` まで進んでいるが、
`2ff0f49..91927ed` の対象 artifact 差分はなく、追加は委嘱ファイルだけで
ある。従って artifact anchor は曖昧でない。

`2ff0f49` 自身の親は `59a0ba3...`、便 55 監査基線は `fd04c41` である。
対象 commit が変更する artifact は指定の二ファイルだけである。

### F1.2 digest / serialization

| artifact | LF | CR | TAB | C0 | BOM | SHA-256 | 判定 |
|---|---:|---:|---:|---:|---|---|---|
| `docs/week4-K5_Rule1_v1_4.md` | 1010 | 0 | 0 | 0 | 無 | `f33988c619846c503b43c90dff721fe5557e28853f5ef505894aad0564015d91` | PASS |
| `docs/manifest_k5_v1_6.md` | 197 | 0 | 0 | 0 | 無 | `b2878d0b988167bedba288244eb29170aec9bba3f2e3be45f23be1d85fc305a7` | PASS |

便 55 基線 `fd04c41` からの差分は

```text
Rule 1 : +33 / -24
manifest: +30 / -15
total   : +63 / -39
```

で申告と一致した。`git diff --check` も clean。

### F1.3 不変物

次の旧正本・原典三文書には `fd04c41..2ff0f49` の差分がない。

```text
docs/week4-K5_Rule1_v1.md
docs/manifest_k5_v1.md
docs/week4-BFC攻略_opus_v2.md
docs/amendment_5prime_draft.md
docs/week4-TB4導出_opus_v1.md
```

Part B 固有の whitelist / \(N_\infty\) schema / \(h\) 非開示修理も
operative 条文へ混入していない。冒頭の「Part B を混入しない」という
境界注記だけであり、この点は **PASS**。

---

## F2. 便 55 F9 の閉鎖表

| F9 項目 | 判定 | 要点 |
|---|---|---|
| finite `Z20-link-seal/v1` | **条件付き PASS** | finite/profinite 分離は閉じた。ただし result schema の root ID との typed alias が欠ける |
| manifest operative 4 面 | **PASS** | C-i/C-ii、field-only 拒否、pairwise、covariance、発射条件が `(5′_b)` へ同期 |
| BFC 未同期 / TB4 precedence | **PASS** | Rule 1 198 行に三文すべてある |
| authority 4 段 + hard stop | **PASS** | manifest 118–123 行で一意化されている |
| 出所対応表三値化 | **FAIL** | 定義は追加されたが、実体と違う `verbatim` が複数残る |
| 語彙 | **要一行修理** | 「照合(検証)」は除去。ただし一般条文が `cross-checked` を先取りする |
| digest・旧正本不変・Part B 不混入 | **PASS** | F1 のとおり |

---

## F3. finite `Z20-link-seal/v1`

### F3.1 finite/profinite 分離 — **PASS**

Rule 1 161–174 行は次を明記している。

- `scope = level_20`
- \(\bar\iota|_K=\iota_\infty\)
- \(\zeta_{20}^{\rm TB2}:=\bar\iota^{-1}(e^{2\pi i/20})\)
- Rule 1 側 root との equality certificate
- \(M\mid20\) の比較だけが同じ seal を参照
- \(n\nmid20\) は量化しない
- full `(Z-norm)` はこの版イベントで採らない
- full `(Z-norm)` の将来採用には別認可と status/CLAIMS 全域更新を要する

従って、便 55 F3.1 の「名札 finite・中身 profinite」は解消した。
状態札も TB4-A20 と TB4-B を有限 / profinite に分けている。この数学的
修理を再度開く必要はない。

### F3.2 blocker B56-1 — root object ID が結果 schema まで通っていない

seal は

```text
rule1_zeta20_id
```

を使用する。一方、Rule 1 §8.4.0/F4 と manifest 116/119 行は

```text
rule1_root_2M_id
```

を使用する。K5 では \(M=10\), \(2M=20\) なので意図する数学 object は
同じだが、本文には

```text
rule1_zeta20_id = rule1_root_2M_id  (M = 10)
```

という alias がない。

さらに seal の第 (3) 条

```text
rule1_zeta20_id: zeta_20^TB2 = zeta_20^Rule1 の
                 equality_certificate_digest
```

は object ID と certificate digest を一行の prose に置くだけで、
certificate が

```text
lhs_object_id = root_system_tb2_id
rhs_object_id = rule1_root_2M_id
scope         = level_20
```

へ束縛される型になっていない。従って、結果 record が別の
`rule1_root_2M_id` を記録しても、現 schema の名前照合だけでは拒否できない。

これは便 55 F3.2 の

> Rule 1 / TB4 / BFC / result record が同じ root IDs と equality
> certificate digest を参照する

の未閉部分である。「同じ \(\zeta_{20}^{\rm Rule1}\) という字形」は
typed object identity の代わりにならない。

最小修理は、seal と F4 で一つの field 名に統一することである。例えば

```text
rule1_root_2M_id       = ID(zeta_20^Rule1)  # K5: M=10, 2M=20
equality_certificate:
  lhs_object_id        = root_system_tb2_id
  rhs_object_id        = rule1_root_2M_id
  scope                = level_20
  digest               = equality_certificate_digest
```

とし、第 (4) 条、Rule 1 F4、manifest 116/119 行もこの同じ ID 名を参照する。
`rule1_zeta20_id` を残すなら、型付き alias を明記してもよい。

---

## F4. manifest operative 4 面 — **PASS**

差分後の current / operative 文面を逆検索した。

1. 103 行:
   operative predicate を \((5′_b)\) とし、PASS を C-i / C-ii に限定。
   抽象 field equality、kernel equality、`field_certificate` 単独を
   明示拒否。exact branch は `/exact/v1` として分離。
2. 129 行:
   pairwise の exact 破れを「少なくとも一方の \((5′_b)\) が偽」とした。
3. 161 行:
   covariance を operative \((5′_b)\) の control と型付けし、exact branch
   には `/exact/v1` と route evidence を要求。
4. 168 行:
   算術全射性の禁止条件を operative theorem bundle
   `(4d)(5'_b)` へ同期し、exact を要求する場合だけ追加 route を課した。

残る裸の `(5′)` は FORMAL-IN の `PENDING`、撤回旧文、exact bundle、
exact recovery の説明であり、operative `(5′_b)` の再汚染ではない。

変更面宣言も「科学的 predicate は一つ、下流 normative 4 面を同期」へ
直っている。便 55 blocker 2 は閉鎖と判定する。

---

## F5. precedence・authority・停止条件

### F5.1 BFC / TB4 precedence — **PASS**

Rule 1 196–198 行は、

```text
BFC v2.11 §12.1(ii) は未同期。
本版では TB4 v2.4 §8.3 を現行 normative source とする。
BFC 本文同期は次版の宿題。
```

を明記している。BFC の stale 文面を黙って正本扱いする余地は閉じた。

### F5.2 schema authority — **PASS**

manifest 118–123 行の優先順位は便 55 F6.2 と一致する。

1. \(b\) の二段コミット / typed semantics: Rule 1 F4
2. bundle enum / `exact_recovery_path` presence: manifest
3. route・ordering・orientation の残余詳細: amendment §4
4. results artifact: 1–3 の union の materialization

衝突時の 1/2 優先、results artifact の独自定義禁止、両文書 digest と
schema digest の束縛も明記された。

`provenance/results_k5.md` または専用 schema artifact の作成・digest 監査が
閉じるまで、Freeze 2 / BRIDGE-IN / `bridge_result` を hard stop とする条文も
明示されている。この停止は本便の差戻しとは独立に有効である。

---

## F6. blocker B56-2 — 出所対応表の三値が実体と一致しない

三値の定義自体は正しい。しかし各行を原典と照合すると、少なくとも次の
申告は成り立たない。

### F6.1 Rule 1 §8.4

Rule 1 1006 行は

```text
verbatim (§8.4.0 F4 の追加 2 欄を除く)
```

とする。しかし、

- amendment §2 の A18 / A19 の版履歴・自己訂正説明を省略している
- 794 行は原典の「照合(検証)」を修理し、新しい parenthetical を加えた
- F4 に seal ID / digest を追加した

ので literal verbatim ではない。これは便 55 F5 が名指しした箇所である。
また `verbatim(...を除く)` は、表自身が定義した
`verbatim / normative-only / adapted` の三値にも属さない。

少なくとも

```text
§8.4 normative block          = normative-only
§8.4.0 F4 追加 2 欄           = adapted
§8.4.2 語彙修理               = adapted
```

へ分割すべきである。751 行の見出しにある「§2 の逐語転記」も
`normative-only transfer` 等へ直す必要がある。

### F6.2 manifest antecedent bundle

manifest 188 行は bundle 全体を `verbatim` とする。しかし原典
amendment 182–225 行にある

- v3 / A10 の詳細な自己訂正
- v4 / A12 の prose/code 衝突の履歴
- v5 / A15 の version なし ID を拒否した履歴

を target は省略・要約している。規範 bundle は保存されているので評価は
`normative-only` であり、これは便 55 F5 の具体的指摘そのものである。
manifest 32 行の「antecedent bundle の逐語転記」も同時に修理すること。

### F6.3 Rule 1 の状態札

Rule 1 1003 行は §1.4.1 状態札を `verbatim` とするが、TB4 v2.4 §8.5 は

```text
TB2 + TB2-norm seal = workshop conventions
```

であり、Rule 1 は

```text
TB2 + root seals(Z20-link-seal/v1) = workshop conventions
```

へ変更している。これは finite/profinite 修理として**正しい意味適応**だが、
正しいから verbatim になるわけではない。分類は `adapted`、変更点は
「full seal の状態札を finite level-20 seal に限定」、承認根拠は
便 55 F3.2 / 裁定 67 とすべきである。

従って 1010/197 行の

> 上表以外に判断を要する言い換えはない

という確認も現状では成立しない。出所表は「三値の凡例を置いた」だけでは
閉じず、各 transfer の実際の型が三値のどれかに正しく入る必要がある。

---

## F7. 語彙 — **字面修理 PASS、status 先取りは要修理**

便 55 F9-5 が要求した「照合(検証)」から「照合」への置換、および
`verified/検証済み` を Lean に予約する注記は入った。

ただし Rule 1 794 行の

```text
ここでの一致は cross-checked にとどまる
```

は一般的な受理条文の段階で、将来の一件ごとの証拠状態を先取りする。
`cross-checked` は、独立な二経路とその一致が artifact ID / digest 付きで
実際に記録されたときに付く状態札である。単に frozen \(b_i\) と観測値を
比較する規則を置いただけでは、自動的にその状態へ上がらない。

安全な修文は例えば

```text
「verified/検証済み」は Lean 証明書に予約する。
この照合の状態札は実際に記録された独立経路に従い、
二経路の一致が閉じた場合に限り cross-checked とする。
```

である。これは数学結論の blocker ではないが、版イベントの status 語彙を
正しくするため、同じ最小差分で閉じるべきである。

---

## F8. 版イベント・W3-19・停止札

### F8.1 現時点の裁定

```text
版イベント完了                    = 不可
Rule 1 v1.4 / manifest v1.6 operative 化 = 不可
Rule 1 v1.3 / manifest v1.5       = 引き続き現行受理版
CLAIMS W3-19 記帳                 = 保留
N_infty 再開                      = なし
Freeze 2 / BRIDGE-IN 解禁         = なし
```

便 55 F8.2 の W3-19 推奨文言は**内容としては維持**するが、version event の
成立を前件とする手続き記録なので、今回それだけを先に記帳してはならない。
特に A3 は未閉 framework/literature gate のままであり、今回の finite seal
は A3 を証明しない。

### F8.2 次回 PASS 後

B56-1 / B56-2 と F7 の一行が閉じ、新 digest の差分ゲートが PASS した時点で、
便 55 F8.2 の文言により W3-19 を記帳してよい。その記録は

- amendment 適用手続きの成立
- operative predicate の versioned 移行
- finite `Z20-link-seal/v1` の採用

を記録するものであり、bridge theorem の無条件化、A3 の閉鎖、Freeze 2
成立、\(N_\infty\) 再開を意味しない。

---

## F9. 最小再提出条件

数学核の再審査は不要である。次便は次の差分だけで足りる。

1. seal の `rule1_zeta20_id` と F4 / manifest の
   `rule1_root_2M_id` を一名へ統一するか typed alias を置き、
   equality certificate を lhs/rhs object ID と `scope=level_20` に束縛する。
2. 出所対応表を実体に合わせる。
   - Rule 1 §8.4: `normative-only` と adapted subrows に分割
   - manifest antecedent bundle: `normative-only`
   - Rule 1 状態札: `adapted`
   - 対応する見出しの「逐語転記」と末尾確認も同期
3. 794 行の `cross-checked` 自動付与を、実際の独立経路記録に条件付ける。
4. 新 digest、親差分、旧正本 / 原典不変、Part B 不混入を再提示する。

これは小差分であり、finite seal の数学、manifest operative 4 面、
precedence、authority 4 段を再び開く必要はない。

---

## ★教材

1. **同じ glyph は同じ object ID ではない。** equality certificate を追加しても、
   result record が記録する rhs ID へ束縛しなければ、証明書の差し替え口が残る。
2. **三値分類は凡例でなく各行の型である。** `verbatim（ただし例外あり）` は
   実質的な第四の値であり、adapted change を再び隠す。
3. **正しい修理も provenance 上は adapted である。** full seal の状態札を
   finite seal へ直すことは数学的に正しいが、それを verbatim と呼んでは
   変更の承認根拠が消える。
4. **一般規則は将来の証拠 status を先取りしない。** 「比較せよ」は手続き、
   `cross-checked` は独立二経路が実際に閉じた一件ごとの結果である。

---

## 監査範囲外申告

本便は `fd04c41..2ff0f49` の F9 修理差分だけを監査した。
便 55 で受理済みの BFC / amendment / TB4 の数学核、S5 Model-Builder、
\(N_\infty\) 探索、候補 8 件、Lean 証明、計算 artifact の再実行は
監査範囲外である。`provenance/results_k5.md` は未作成のままであり、
作成・編集・CLAIMS 記帳は行っていない。

---

## 共同設計者としての提案

### P56-1. source-map enum を機械可読にする

各行を

```text
transfer_mode = verbatim | normative-only | adapted
source_range
target_range
approval_id        # adapted のとき REQUIRED
change_summary     # adapted のとき REQUIRED
```

にし、`verbatim(...)` のような未知値を lint で拒否する。これで今回の
「三値化したが例外を括弧に隠した」を機械的に拾える。

### P56-2. equality certificate を named edge にする

root equality を digest 一個で持たず、

```text
edge_id
lhs_object_id
rhs_object_id
scope
certificate_digest
```

の named edge として seal / Rule 1 / manifest / result record の四者で
同じ値を参照する。object の同名・改名・alias の事故を fail-closed にできる。

### P56-3. evidence status と procedure を別 field にする

```text
procedure = compare(frozen_b, observed_character)
status    = candidate | cross-checked | verified
```

を分け、`status=cross-checked` には二つの独立 derivation ID を、
`status=verified` には Lean certificate ID を必須にする。これなら
「照合」という動詞を使っただけで status が昇格することがない。
