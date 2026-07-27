# 便 55 返信 — Rule 1 v1.4 / manifest v1.6 適用差分ゲート

## 総合判定: **差戻し（APPLY-GATE FAIL）**

commit・receipt・digest の provenance は **PASS**、旧正本不変と Part B
不混入も **PASS** である。しかし適用本文には、版イベント完了を止める
blocker が 2 件ある。

1. `Z20-link-seal/v1` の名の下へ、有限 level 20 の seal ではなく
   **全 \(n\)** を量化する full `(Z-norm)` の 4 条を入れている。
2. manifest v1.6 の旧 operative 箇所に、撤回済みの
   **field/kernel-only PASS** と exact `(5′)` の結論が残り、新しい
   operative predicate `(5′_b)` と衝突している。

従って現時点では **版イベント完了を宣言しない**。Rule 1 v1.4 /
manifest v1.6 を operative とせず、CLAIMS W3-19 もまだ記帳しない。

---

## F1. 監査 anchor と provenance — **PASS**

### F1.1 git anchor

委嘱指定の artifact anchor は

```text
fd04c41a53dcecfcaa0512d10c0607bc44134880
tree 2e3a3bfb6979a7d1cb5a10d32ed8c047c198be0d
parent 47e55dd2e671c0611049de7ae4b0f61b49e42f31
```

である。現在の HEAD は `fdcb8e1...` まで進んでいるが、
`fd04c41..HEAD` が対象数学 artifact に加えた変更はなく、便 55 の委嘱
ファイルが追加されただけである。従って数学判定は指定どおり
`fd04c41` に固定した。

`47e55dd..fd04c41` の差分は次の新規 2 ファイルだけである。

```text
A  docs/manifest_k5_v1_6.md
A  docs/week4-K5_Rule1_v1_4.md
```

### F1.2 C/R 二段 provenance

承認元の二段は現物で閉じている。

```text
C = 38e4652543db051c580a4e37489c977ae2cc577c
C.tree = edf1200e702b5fb402355b192d1e99ca95113a81

R = 686ceeafe1c100a2a5743f57ddd63d38e5a20b0a
R.parent = C
receipt.source_commit = C
receipt.source_tree = C.tree
```

receipt が束縛する三原典と、`fd04c41` での現物は一致する。

| 原典 | LF | SHA-256 | C → `fd04c41` |
|---|---:|---|---|
| `docs/week4-BFC攻略_opus_v2.md` (v2.11) | 1214 | `2aa84e6762a643c10727cdca99556e660cd97ccab5088ce38262dd2679473acc` | 不変 |
| `docs/amendment_5prime_draft.md` (v8) | 358 | `ccba23a317fe6fb016d95d81143760fdd77d5edba2c2144cf6280ae23a776655` | 不変 |
| `docs/week4-TB4導出_opus_v1.md` (v2.4) | 852 | `ff71e9fbc162ee613713d9ad317e8fbea635c7e4fadeae189cff1656b52634f4` | 不変 |

途中に Part B の委嘱・裁定 commit があるが、上記三原典と CLAIMS は
C から適用 commit まで不変である。従って別 lineage の文言を source
へ後付けした形跡はない。

### F1.3 新旧 artifact

| artifact | LF | CR | BOM | SHA-256 | 判定 |
|---|---:|---:|---|---|---|
| Rule 1 v1.4 | 1001 | 0 | 無 | `02c60a768ec27f86ff347eeca99d2b07800ece582e314d22df02422dc3692199` | 委嘱値一致 |
| manifest v1.6 | 182 | 0 | 無 | `c3b90068ff0448be4016b40e0e76cd14431de6d787888777bad8878eb3875feb` | 委嘱値一致 |
| 旧 Rule 1 v1.3 | 883 | 0 | 無 | `8367ba7ac57876b490bbe775c56768747a519f3f5e4c1fe69dfab0c022cdf8db` | 親 → 適用 commit 不変 |
| 旧 manifest v1.5 | 103 | 0 | 無 | `2091dea7db6fca3cdc99fa5b688805b51a12cd86819d7b4f76df069d02a47b13` | 親 → 適用 commit 不変 |

旧正本を上書きせず新版を作る手続きは正しい。

---

## F2. 原典との転記突合

### F2.1 Rule 1 v1.4 — **中心条文は PASS**

次の規範内容は amendment v8 / TB4 v2.4 と一致する。

- §8.4.0 の Freeze 1 = rule commitment / Freeze 2 = value commitment。
- actual \(b_i=b_{\rm op}\) を \(u\)・\(G_K\)/shadow 観測より前に固定し、
  以後 fitting しないこと。
- operative predicate `(5′_b)`、exact `(5′)` の二経路 R-a/R-b、
  C-i/C-ii の限定列挙、field/kernel-only PASS の排除。
- ord1 で空虚になるのは \(b\) の同定だけで、左辺の自明性試験は残ること。
- pairwise gate を先行し、不一致を I-d とすること。
- §9.2 I-n の run 全体隔離と新 run での再実施。
- §7.4 の四段 quarantine。
- \(U_\lambda=U_\beta\)、接基点、向き、\(\gamma_0\)、\(\ell_i\) の typed equality。

amendment の A18/A19 等の版履歴注記や自己訂正履歴は省略されているが、
上の規範的数学内容に欠落はない。

### F2.2 manifest v1.6 — **新規ブロックの中心は PASS**

次は amendment v8 と一致する。

- BRIDGE-FAIL を、事前コミット済み \(b_i\) に対する `(5′_b)` の exact
  反例へ変更。
- theorem bundle と falsifier bundle の分離。
- falsifier bundle から `(5′)` 系を除去。
- `antecedent_bundle_id` の version 付き 3 値 closed enumeration。
- `/exact/v1` の R-a/R-b 分離と `exact_recovery_path` の conditional
  presence。
- digest 4 欄、typed \(b_{\rm op}/b_{\rm cmp}\) 欄、証明書三分離への参照。
- `bridge_result_i` の版跨ぎ比較禁止。

しかし「新規ブロックが正しく転記された」だけでは、文書全体の意味が
整合したことにならない。F4 の stale operative 文言が残っている。

---

## F3. blocker 1 — `Z20-link-seal/v1` が full `(Z-norm)` を誤収容

### F3.1 型の衝突

Rule 1 v1.4 §1.4.1 は `Z20-link-seal/v1` と名乗りながら、

```text
(ii) zeta_n^TB2 := bar_iota^{-1}(exp(2*pi*i/n))
     （すべての n について）
```

を含む。

原典 TB4 v2.4 §8.1 のこの 4 条は
`TB2-norm / comparison-root seal`、すなわち **full `(Z-norm)`** の条文
である。同稿の定理 TB4-B も明示的に

```text
(Z-norm) = §8.1 の 4 条 atomic seal
```

を前件とし、全 \(n\) の (ii) から profinite \(\varepsilon=1\) を導く。
一方、有限 TB4-A20 に必要なのは level 20 の `(Z20-link)` だけであり、
便 49 F6.5 はこれを full `(Z-norm)` と別の独立 ID
`Z20-link-seal/v1` にせよ、と裁定した。

従って現 §1.4.1 は

- 名札では finite L3、
- 内容では profinite L4、
- 直後の状態表では L3 と L4 を別札

としており、以前の監査で守った
\[
(Z\text{-norm})\Rightarrow(Z_{20}\text{-link}),\qquad
(Z_{20}\text{-link})\not\Rightarrow(Z\text{-norm})
\]
を正文内で潰している。「`(Z-norm)` の一部凍結とは呼ばない」という
注記を加えても、全 \(n\) を量化した事実は変わらない。

### F3.2 必須修理

本イベントの認可範囲は有限 `Z20-link-seal/v1` なので、例えば次の型に
限定すること。

1. `bar_iota_id` と \(\bar\iota|_K=\iota_\infty\)。
2. `root_system_tb2_id` と
   \(\zeta_{20}^{\rm TB2}:=\bar\iota^{-1}(e^{2\pi i/20})\)。
3. `rule1_zeta20_id` および
   \(\zeta_{20}^{\rm TB2}=\zeta_{20}^{\rm Rule1}\) の
   `equality_certificate_digest`。
4. \(K^{(5)}\)/\(M\mid20\) の全比較が同じ ID・certificate を参照すること。

ここでは **\(n\nmid20\) を量化しない**。full `(Z-norm)` を本当に採るなら、
それはこの適用差分ではなく、別の明示的認可と status/CLAIMS 全域更新を
要する。

また便 49 F6.5 が要求した「Rule 1 / TB4 / BFC / result record が同じ
root IDs と equality certificate digest を参照」は、現 Rule 1 の F4
欄では equality certificate digest が明示されていない。上の修理と
結果 schema の双方へ同じ seal ID/digest を入れること。

---

## F4. blocker 2 — manifest に撤回済み predicate/certificate が残存

### F4.1 field-only PASS の再侵入

manifest v1.6 §「exact 判定の証明書型」の現行文は、

> PASS は character 恒等の普遍的導出 or Kummer 拡大の厳密同定

とする。しかしこれは amendment v8 A2 が blocker として撤回した文
そのものである。Rule 1 v1.4 §8.4.2 と amendment §4 は、

- 同じ Kummer 体・同じ kernel でも unit-power character は異なりうる。
- `field_certificate` 単独では PASS 不可。
- C-i character identity または C-ii oriented torsor が必須。

と定めている。manifest 115 行の「証明書三分離」参照は、103 行の明示的
許可を自動的には撤回しない。同じ operative 文書の中に正反対の受理規則
があるため blocker である。

### F4.2 downstream の `(5′)` 残存

少なくとも次の current/operative 箇所は型付けし直す必要がある。

| manifest 箇所 | 現文 | 必要な処置 |
|---|---|---|
| 103 行 | `(5′)` の PASS に field identification を許す | operative `(5′_b)` の C-i/C-ii に置換し field-only を明示拒否。exact branch は `/exact/v1` として別記 |
| 121 行 | pairwise 破れ ⇒「少なくとも一方の `(5′)` が偽」 | 「少なくとも一方の **`(5′_b)`** が偽」 |
| 153 行 | covariance control で `(5′)` 不変 | operative `(5′_b)` の control か exact branch の control かを明示 |
| 160 行 | 算術全射性は `(4d)(5′)` 閉鎖まで禁止 | campaign の operative theorem bundle `(5′_b)` に同期。exact を要求する場合だけ `/exact/v1` と route evidence を名指し |

121 行の修理は結果 transition の値を変えない。**同じ遷移が何を反証するか**
を、新 predicate の型へ同期するだけである。

従って冒頭の「exact 判定の証明書型・結果規則表等は逐語不変」という
変更面宣言も、そのままでは維持できない。科学的 predicate は一つのまま
だが、その predicate を複製している下流 normative surface は悉皆同期が
必要である。

---

## F5. 出所対応表・「逐語」申告 — **要修理**

出所対応表は地図として有用だが、現物の

> 逐語（版ラベルと節番号の付替えのみ）

は事実より強い。

- Rule 1 §1.4.1 は、TB4 §8.1 の英語 4 条を翻訳しただけでなく、
  `TB2-norm` を `Z20-link-seal/v1` へ**型替え**している。F3 のとおり
  この型替えは意味も変えている。
- Rule 1 §8.4 と manifest の bundle は、A18/A19/A12/A15 等の履歴注記・
  自己訂正説明を省略している。規範内容は保たれているが、literal
  verbatim ではない。
- 組立申告では BFC v2.11 §12.1 を「対応節・未同期」と注記したとあるが、
  Rule 1 193/995 行には **`未同期` の語も、TB4 が現行優先 source だという
  precedence もない**。

修理後の対応表は、各行を少なくとも

```text
verbatim / normative-only（履歴注記省略）/ adapted
```

に分類すること。`adapted` なら変更点と承認根拠を一行で書くこと。

---

## F6. 組立時の低リスク判断 2 点

### F6.1 文献要請 13(ii) — **判断自体は条件付き PASS、現適用は注記不足**

TB4 v2.4 §8.3 の縮小文言を採る判断は正しい。root normalization は工房
規約、文献要請として残す load-bearing 部分は A3
（forward transport \(\leftrightarrow\) postcomposition-left、
inverse でないこと）である。

ただし BFC v2.11 §12.1 は実際に旧 (ii) のままなので、新 Rule 1 に

```text
BFC v2.11 §12.1(ii) は未同期。
本版では TB4 v2.4 §8.3 を現行 normative source とする。
BFC 本文同期は次版の宿題。
```

と明記すること。BFC v2.11 自体をこのイベントで編集しない判断には賛成する。

### F6.2 結果 schema の分担 — **設計は条件付き PASS**

`provenance/results_k5.md` がまだ存在しないこと自体は、**Freeze 2 /
BRIDGE-IN / 結果 record を一件も受理しない限り**、Part A の文書版上げを
単独では止めない。

しかし現文には、

- Rule 1 §10: Rule 1 が二段コミット欄の生成元、
- manifest: enum/conditional presence の正本、
- manifest 115 行: amendment §4 が「詳細 schema の正本」

という三つの authority が並ぶ。次の優先順位を明文化すること。

1. \(b\) の二段コミットと typed semantics は Rule 1 §8.4.0/F4 が正本。
2. bundle ID の closed enum と `exact_recovery_path` presence rule は
   manifest v1.6 が正本。
3. amendment §4 は適用元・残余詳細
   （route evidence、ordering evidence、orientation certificate 構造）の
   source。専門正本 1/2 と衝突した場合は 1/2 が優先。
4. `provenance/results_k5.md` は上記の union を materialize する record で、
   独自定義を追加しない。両文書 digest と schema digest を束縛する。

`results_k5.md` または専用 schema artifact の作成・digest 監査が閉じるまで、
**Freeze 2 / BRIDGE-IN / bridge_result 記録は hard stop** とする。この条件
なら「Freeze 2 前に実体化」は受理できる。

---

## F7. Part B 境界 — **PASS、ただし停止は継続**

旧版との意味差分を検索すると、Part B 固有の `-108`、taint/recusal、
N-infinity searcher v2、h 非開示等を operative 条文へ混入した箇所はない。
新規差分に現れるのは「Part B を混入しない」という版履歴注記だけである。
裁定 66 F4 は守られた。

ただし旧 v1.3/v1.5 由来の N-infinity 条文がそのまま複製されていることは、
裁定 66 Part B の integrity stop を解除しない。将来 Part A が PASS して
v1.4/v1.6 が operative になっても、

```text
N_infty の schema/run/certificate は別ゲートまで隔離、
bound <= 5 は UNKNOWN、Freeze 2 候補受理は不可
```

が継続する。ここを CLAIMS の「版イベント成立」から誤って解除してはならない。

---

## F8. 版イベント・CLAIMS W3-19

### F8.1 現時点

- **版イベント完了宣言: 不可**
- Rule 1 v1.4 / manifest v1.6 の operative 化: **不可**
- v1.3 / v1.5: 引き続き凍結履歴かつ、現行受理版
- W3-19 記帳: **保留**
- S5/Freeze 2/N-infinity の新規解禁: **なし**

### F8.2 再提出 PASS 後の推奨文言

委嘱案の短文は方向としてよいが、単に「seals」と書くと A3 まで閉じたと
誤読される。次を推奨する。

> **K⁽⁵⁾ Part-A 版イベント成立（手続き）**: Rule 1 v1.4 /
> manifest v1.6 を operative 化し、campaign の bridge predicate を
> `(5′_b)` へ versioned 移行。\(b\) は Freeze 1 の rule commitment /
> Freeze 2 の value commitment に分離し、
> `b_value_i=b_op` と `b_cmp` を型分離。有限
> `Z20-link-seal/v1` を採用し、A3 は別の未閉
> framework/literature gate として保持。v1.3/v1.5 は履歴保存、
> `bridge_result` の版跨ぎ比較は禁止。**これは規約イベントであり、
> bridge theorem の無条件化、Freeze 2 成立、N-infinity 再開を意味しない。**

状態は W3-16 と同様に **「手続き成立（数学 claim ではない）」** が適切である。

---

## F9. 最小再提出条件

1. F3 の finite/profinite seal 型を修理し、root IDs と equality certificate
   digest を結果 schema まで通す。
2. manifest 103/121/153/160 行を `(5′_b)` / exact branch の型へ同期し、
   field-only PASS を排除する。
3. 文献要請 13(ii) の BFC 未同期・TB4 precedence と、schema authority の
   優先順位を明記する。
4. 出所対応表の `verbatim` 申告を実態に合わせる。
5. Rule 1 787 行の「照合(検証)」は **「照合」** に直す。
   本工房では `verified/検証済み` は Lean 証明書に予約されている。
6. 新 digest、親からの全差分、旧正本不変、Part B 不混入を再提示する。

この差分だけなら数学核を再審査する必要はなく、次便では上記箇所の
differential gate で足りる。

---

## ★教材

1. **seal の名前は型である。** `Z20` と名付けた箱へ「全 \(n\)」を入れると、
   注記が何を言っても finite/profinite の分離は壊れる。
2. **predicate を版上げしたら、定義箇所だけでなく、証明書型・遷移表・
   covariance・発射条件まで逆向きに検索する。** 遷移の値が不変でも、
   「何が偽になったか」のラベルは不変とは限らない。
3. **「逐語」と「規範部分を転記」は別の provenance 型である。**
   履歴注記を省くこと自体は安全でも、逐語と申告すると本当の adapted
   change が埋もれる。
4. **未来に schema を作る約束は現在の authority conflict を解消しない。**
   未作成は許せても、誰がどの field の正本かは先に一意でなければならない。

---

## 共同設計者発案

### P55-1. predicate surface lint

新 manifest にある `(5′)` / `(5′_b)` の全 occurrence を

```text
historical-quote / exact-branch / operative-twisted
```

の三値で注釈し、無注釈の current normative occurrence を fail-closed に
拒否する。今回の 103/121/153/160 行を機械的に捕まえられる。

### P55-2. seal-scope lint

seal ID に scope を持たせる。

```text
Z20-link-seal/v1.scope = level_20
Z-norm-seal/v1.scope   = profinite
```

`level_20` の本文に `for every n` / `すべての n` が現れたら停止する。
逆に profinite theorem が level-20 seal だけを前件にした場合も停止する。

### P55-3. machine-readable authority table

結果 schema の各 field group に

```text
canonical_source
canonical_section
source_sha256
presence_rule_source
```

を一つずつ持たせる。`amendment`、Rule 1、manifest、結果 record の四者で
同じ field を「正本」と名乗る事故を防げる。

---

## 監査範囲外申告

本便で監査したのは、commit/parent/tree/receipt/digest、旧正本との差分、
三原典との条文突合、Part A/Part B 境界、schema authority、CLAIMS 候補文言
である。外部文献の原文、Lean 証明、GAP/Node 数学計算、個別
\(K^{(5)}\) モデル、\(u\)、候補 8 件の再監査、N-infinity 修理設計そのものは
範囲外である。本返信以外のファイルは変更していない。
