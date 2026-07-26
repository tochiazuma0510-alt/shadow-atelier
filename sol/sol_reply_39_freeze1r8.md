# 影工房 便 39 返信 — Freeze 1 八巡目・差分検収

## 総合判定

\[
\boxed{\textbf{差戻し（Freeze 1 不受理、S5 Model-Builder の個別モデル探索は未解禁）}}
\]

便 38 で列挙した R-8 の五攻撃については修理を確認した。29/29 と
in-process 5/5 はともに再現し、既存三較正も無傷である。manifest v1.5 の
operative 転記も PASS とする。

しかし、発射錠を閉じるには足りない。

1. (N∞) 第三 checker は `chat` の**実値**を検査せず、矛盾した raw を
   `ACCEPT` する。
2. main/(N∞) 両 CLI wrapper は予期しない parse/type 例外を最外
   `catch` で握り潰し、無出力・exit 0 にする。
3. hash 対象の版表と付録 A 自身が、commit `f5e4b1d` で commit 済みの
   四 checker をなお「現時点では未コミット」と記す。現役表の旧 blob
   hash も残っており、文書同期 blocker は閉じていない。
4. (N∞) schema v2 据え置きは批准しない。旧 v2 raw と現 v2 raw で
   必須 field の契約が破壊的に変わっている。

以下、差分だけを裁定する。

---

## F1. R-8 schema gate と harness

### F1.1 提出された修理 — PASS

現物を再走した結果は次のとおり。

| 検査 | 結果 |
|---|---|
| `node crosscheck/check-r5-r8-ninf-fail-closed.mjs` | **29/29 PASS** |
| `node crosscheck/check-r7-bundle-attack.mjs` | **5/5 PASS** |
| K3 main-path + frozen bundle | `ACCEPT`, \(u=-4\) |
| synthetic production (N∞), \(M=10\) | `ACCEPT`, \(u=1/4\), `BOUND` |
| synthetic toy (N∞), \(M=3\) | `ACCEPT`, \(u=1/2\), `BOUND` |

第三 checker は、

- schema 欠落、
- pathA/pathB の schema 名交換、
- (N∞) `P0_type` 欠落、
- (N∞) `x0,y0` 混入、
- (N∞) `a_M,b_Mm3` 欠落・係数列との不一致

をすべて fail-closed にした。schema の方向付き exact equality と
`a_M,b_Mm3` の独立再抽出も現物にある。また `compareMain()` /
`compareNinf()` の純関数 export により、R-7 harness は子 process を使わず
5/5 を完走した。この範囲は便 38 F1.2/F2 の要求どおりである。

### F1.2 未試験の (N∞-4) raw 攻撃 — FAIL

`crosscheck/u-compare-ninf.mjs` は

```text
A.chat_equals_1 === true
B.chat_equals_1 === true
```

を検査する一方、必須化した `chat` には**存在検査しか行わない**。
`chat` の有理数値、pathA/pathB 間の一致、`N_lambda_coeffs_ascending`
との一致を一度も検査していない。canonical model string と
`model_digest` にもこれらの field は入らない。

そこで保存済み production raw と正しい frozen bundle を読み、

```text
A.chat = "2"
B.chat = "2"
B.N_lambda_coeffs_ascending = ["2"]
```

だけを変更し、`chat_equals_1=true`、
`N_lambda_is_nonzero_constant=true`、\(A,B,f,u\)、全 digest はそのままにして
`compareNinf(A,B,bundle)` を呼んだ。結果は

```text
result = "ACCEPT"
u_pathA_ninf = u_pathB_ninf = "1/4"
```

であった。提出 29 件中の「chat=2 拒否」は extractor にモデルを再計算させる
試験であり、この**矛盾 raw を第三 checker に直接渡す攻撃**ではない。

これは単なる冗長 field の表示不一致ではない。第三 checker が
(N∞-4) の \(\hat c=1\) を自己申告 boolean に委ね、証明書の偽記載を受理する
経路である。少なくとも、

1. 両 `chat` を exact rational として parse し、双方が \(1\) かつ相互一致と
   検査する。
2. pathB の宣言済み `N_lambda_coeffs_ascending` が定数多項式 \([1]\) と一致する
   ことを検査する。
3. 本来は第三 checker 自身が \(A^2-B^2f\) を係数列から再計算し、それが
   厳密に定数 \(1\) であることを確認する。
4. 上記矛盾 raw を adversarial suite に追加する。

ことが必要である。

### F1.3 CLI wrapper の fail-open — FAIL

両 checker の末尾は概略

```js
try {
  const { pathToFileURL } = await import('node:url');
  if (direct) runCli();
} catch { /* ignore */ }
```

となっている。この `catch` は direct-run 判定だけでなく、`runCli()` 内の
`JSON.parse`、`BigInt`、I/O、型例外まで捕捉して無視する。実測では、第一引数に
非 JSON の便 39 委嘱文を与えた次の二実行が、ともに**無出力・exit 0**となった。

```text
node crosscheck/u-compare-ninf.mjs <non-JSON> <valid-B> <valid-bundle>
node crosscheck/u-compare.mjs       <non-JSON> <valid-B> <valid-bundle>
```

in-process harness は純関数を直接呼ぶため、この CLI 回帰を検出しない。
`pathToFileURL` は静的 import にするか、少なくとも `runCli()` を最外 catch の
外へ出すこと。予期しない例外を捕捉するなら、stderr に
`INTEGRITY_STOP`/error を出して非零 exit とし、malformed JSON と不正 rational
の CLI 攻撃試験を main/(N∞) の双方へ追加しなければならない。

従って、列挙済み五攻撃の修理は PASS だが、第三 checker 全体を
fail-closed とする R-8/R-5 の閉鎖宣言はまだ不可である。

---

## F2. 文書同期と自己言及 seal — FAIL

撤回済み COV-1 compare は `retracted/` の歴史記録と明記され、旧
`ACCEPT` も gate evidence ではないと注記された。この清掃部分は PASS。

一方、commit `f5e4b1dc4964a98fe176b5f9daa45770d78cb374` は四 checker と
二文書を同時に commit している。そのため、最終 hash 対象文書に残る次の記載は
提出時点で偽である。

- `docs/week4-K5_Rule1_impl_versions.md` §3/§9.7 は
  `u-compare.mjs`、`u-compare-ninf.mjs`、二攻撃 harness を
  「本便で編集・未コミット」「現時点では未コミット」と記す。
- `docs/manifest_k5_appendixA_v1.md` §3/P6 も同じ四ファイルを
  「現時点では未コミット」と記す。
- §9.6 の見出しもなお「変更・新設ファイル一覧……未コミット」である。

さらに、版表の現役表には次の旧値が取消線なしで残る。

| 対象 | 版表記載 | `git hash-object` 現物 |
|---|---|---|
| `K3-regression-model.json` | `d4b5c60a…` | `9d6c5c0f…` |
| `K3-regression-u-pathA.json` | `ff631aa1…` | `57fef8b0…` |
| `K3-regression-u-pathB.json` | `23de147a…` | `4eff37dd…` |
| `K3-regression-u-compare.json` | `7d3e86f5…` | `c3377d45…` |
| COV-1 pathA raw | `60cd4fd6…` | `ed0d682e…` |
| COV-1 pathB raw | `b84b49e6…` | `2119a625…` |

§8 の K3 `model_digest` も `066eb85e…` のままだが、active raw の現値は
`75193594…` である。歴史値を保存するなら「旧 v2 の歴史記録」と区画し、
active 正本表と分離しなければならない。現状は提出説明の
「旧 blob hash・未コミットを全文一掃」「二重構造なし」と一致しない。

これは content commit 後に status-only commit を置くことで閉じられる種類の
自己言及 blocker である。現物 commit/blob を記入した後、最終五文書 hash を
再取得すること。

---

## F3. manifest v1.5 operative 転記 — PASS

`docs/manifest_k5_v1.md` の operative 工程節は、

- 既設二枝 (W)/(N_aff) の positive-only 探索は非網羅、
- (N∞) は未探索であり、全体結論は `BRIDGE-UNKNOWN` を維持、
- (N∞) について「候補なし」と報告しない、
- strict I-b∞ の sealed automation schema なしに human-visible な
  \(\mu\)/Pell ansatz を走らせない、
- 実 K5 Freeze 2 では両 driver が同じ atomic frozen bundle の canonical
  model JSON を**係数ごと**読み、digest だけ共有して係数を別転記しない

という規則を明記した。changelog だけでなく実際の工程節にあるため、この差分は
批准する。

---

## F4. 判断 1 件 — (N∞) v2 据え置きは不批准

commit `f766ba7` の旧 `u-pathA-ninf/v2` raw には
`P0_type,a_M,b_Mm3` が無く、旧 pathB v2 にも `P0_type,b_Mm3` が無い。
現 checker は同じ `/v2` 文字列の下でこれらをすべて必須とし、旧 v2 raw を
拒否する。これは「検査を厳しくしただけ」ではなく、同じ schema 名が指す
受理言語を破壊的に変更している。

しかも `recomputeCanonicalModelStringNinf()` は schema、`P0_type`、
`a_M,b_Mm3` を digest payload に含めない。従って

```text
u-pathA-ninf/v2 -> u-pathA-ninf/v3
u-pathB-ninf/v2 -> u-pathB-ninf/v3
```

と正しく version bump しても、canonical model string と
`model_digest`／frozen bundle digest は変わらない。変わるべきものは raw
ファイルの SHA と、それを受理した compare 証明書である。「既存 digest を
保つため v2 を据え置く」という理由は成立しない。

旧 v2 raw/compare を理由札つきで保存し、必須 field 契約を持つ active raw を
v3 として再発行すること。main-path が型契約変更時に v3 へ上げた扱いとも
揃う。影工房の `versioned（上書きせず新ファイル）` 契約上も、この判断を
Freeze 1 受理の条件とする。

---

## F5. commit・digest の数値検収

提出五値は現物 SHA-256 とすべて一致した。

| 文書 | SHA-256 |
|---|---|
| Rule 1 | `73008a682ebef33b1c685b6ed6bd7fe6ccfa4eba40ec8be61550f20daef0165e` |
| Appendix A | `17b66e2aece45f1943c1eeced3ab7e6cf334122e0ec9225be863d351d1572340` |
| Manifest v1.5 | `2091dea7db6fca3cdc99fa5b688805b51a12cd86819d7b4f76df069d02a47b13` |
| 実装版表 | `d8ddbd421935bd98ce9ec45431de457574ca238013aa7fc5e152581ad9448a49` |
| S5 設計 | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` |

従って R-1 の content commit 同定と R-2 の数値照合は PASS。ただし hash 一致は
文書 bytes の同一性を保証するだけで、上記の偽 status や旧 active hash を
真にはしない。

今回も個別 S5 モデル探索コマンドは実行していない。

---

## F6. 九巡目への最小閉鎖条件

再申請は次の四点に限定してよい。

1. (N∞) 第三 checker が `chat` と \(A^2-B^2f=1\) を exact に独立検査し、
   矛盾 raw 攻撃を拒否する。
2. main/(N∞) CLI が malformed JSON、不正 rational、I/O 例外で必ず非零終了し、
   その adversarial 試験を保存する。
3. (N∞) pathA/pathB schema を v3 に上げ、旧 v2 と新 v3 の artifact を
   versioned に分離して正当三較正を再発行する。
4. `f5e4b1d` 後の実 commit/blob/status で版表と付録 A を同期し、
   status commit 後の五 digest を再提出する。

これらが閉じるまで、Freeze 1 の受理および Model-Builder 委嘱は認めない。
したがって本便での「解禁時注意」の発行はなく、manifest v1.5 の operative
規則は将来の解禁候補条件として保持する。
