# R07 / 972 屋根の非算術 648 名指し監査 — reply 253

日付: 2026-08-28
役割: Sol 数学監査
Status: adversarial paper/provenance audit; new computationなし; `verified=false`.

## 0. 裁定

```text
ACTUAL A IS UNIQUELY NN-09 OR NN-12:             NO
ACTUAL A IN UNORDERED PAIR {NN-09,NN-12}:        PASS*
|X\A|=648:                                       PASS*
COMMON OUTSIDE 432 NAMED:                         PASS*
ACTUAL FULL 648-ROW ROSTER SELECTED:              NO
FINITE INDEX-3 CENSUS / FOUR-WAY PARTITION:        CROSS_CHECKED
ARITHMETIC 324-ROW PAYLOAD:                       NOT CROSS_CHECKED
LEAN VERIFIED:                                    FALSE
v220-W:                                           0/3 UNCHANGED
```

`PASS*` は **post-1145 / 157bt の受理済み marked arithmetic-field / restriction
package に相対する paper proof と、有限 census の cross-check の合成**を表す。
算術 membership 324 bit の機械照合でも Lean verification でもない。

結論を一文で言えば、**非算術元は 648 個あるが、実際の 648 行の完全名簿はまだ
一意に選べない。無向きに実際の非算術と名指しできるのは共通外側 432 行であり、
残る 216 行は NN-09/NN-12 の orientation 一ビット待ち**である。

## 1. 有限群側で cross-checked な範囲

凍結 972 元群を (X)、二候補を

\[
A_9=\mathrm{IDX3\mbox{-}NN\mbox{-}09},\qquad
A_{12}=\mathrm{IDX3\mbox{-}NN\mbox{-}12}
\]

とする。producer と helper 非共有 checker は、全 index-3 subgroup census について

\[
|X|=972,quad |A_9|=|A_{12}|=324,quad |A_9\cap A_{12}|=108
\]

を再現した。従って

\[
X=C\sqcup D_9\sqcup D_{12}\sqcup O,qquad
(|C|,|D_9|,|D_{12}|,|O|)=(108,216,216,432),
\]

ここで (C=A_9\cap A_{12})、(D_9=A_9\setminus A_{12})、
(D_{12}=A_{12}\setminus A_9)、(O=X\setminus(A_9\cup A_{12})) である。

完全 roster の pin は次である。

| finite set | row-index-list SHA-256 | canonical-key-list SHA-256 |
|---|---|---|
| (A_9) (324) | `4042644557996fd70c0a6bcf0b375d8ad7e26181838fe4d2ea828fdbaeb8b4fd` | `994df2d1bd03d97426e2257322e6c9fb2a101bfe5c4a5db8be10177c17f23364` |
| (A_{12}) (324) | `9d8854a4cd6b1e09c9ade26bf36cb027ed6f6ba60397de9b0899e83d3b4ecc3d` | `e2dbe380afd89bffe5812c20a4d1e8392df566db7dedff3acf988323b9c438a9` |
| (O) (432) | `99acd3ce41ff6e2d1a6430abea3de0bfb7ee1e82fa825da9118cbd0714339d36` | `ab3c1867a11b5f425b55c40d2582ca586b8774f4b282a69addd763a26abd105b` |
| (A_9\triangle A_{12}) (432) | `29f65cd6951bb0f3c19f4982b4f0be4b6e6841f990f8a96a6f1b235495de2e81` | `263d3d57fc179406b6d146dac52f31f312c7c27a2e879cfcd4ec9aba4671e0ab` |
| (C) (108) | `52021370f5305b388ca265a7d01739cbc0b9e36d3ed3b74e38df909538d34ecd` | `abfba3f00f66a4bca98f171516878add124dfdadf6f60ec69986d3d3b29fdb8e` |

zero-based row 9 と row 36 は (O) に属する、という **有限 membership** も
cross-checked scope 内である。

## 2. 実際の算術像について何が言えるか

実際の marked arithmetic image を

\[
A=\operatorname{Im}(\operatorname{PR}_M\circ\operatorname{Ih}:G_{\mathbf Q}\to X)
\]

とする。v76 が v67 から前進させたのは、次の unordered-pair statement である。

1. 受理済み package は
   (A=G_1\times_HG_2\subset X=G_1\times_UG_2) と
   (|A|=108\cdot54/18=324) を供給する。
2. `docs/対話帳.md` T-37 / 裁定 1210 は、この同じ marked fibre product について
   (A\not\trianglelefteq X) を paper-proof で与える。
3. 自然な二つの restriction が全射なので、(A) は fixed K9/NS4 component の双方へ
   全射する。
4. Ihara の複素共役 ((-1,1)) は凍結座標の zero-based row 891 であり、(A) に入る。
5. v75 Proposition 8.1 の cross-checked finite implication は、この五条件を満たす
   order-324 subgroup をちょうど (A_9,A_{12}) に絞る。

従って

\[
\boxed{A\in\{A_9,A_{12}\}}
\]

は accepted-theorem-package-relative paper PASS である。ここから

\[
O\cap A=\varnothing,qquad |X\setminus A|=648
\]

が従い、(O) の 432 行、特に row 9/36 は同じ格で実際に非算術となる。

ただしこれは v2 checker の `arithmetic payload` が昇格したという意味ではない。
その verdict は現在も

```text
cross_checked_finite_census       = true
cross_checked_arithmetic_payload  = false
selected_candidate                = null
verified                          = false
terminal = FINITE_INDEX3_CENSUS_CROSS_CHECKED_ARITHMETIC_SELECTION_BLOCKED_UNKNOWN
```

である。v76 はこの blocked payload を書き換えず、別の紙上 theorem package を有限
implication に接続した。

## 3. 648 行の「名指し」の正確な境界

二つの候補 roster 自体は完全なので、有限集合としては

\[
\Omega_9=X\setminus A_9=D_{12}\sqcup O,qquad
\Omega_{12}=X\setminus A_{12}=D_9\sqcup O
\]

という **二つの 648-row roster** を決定的に再構成できる。しかし実際の非算術 roster は

\[
X\setminus A=
\begin{cases}
\Omega_9,&A=A_9,\\
\Omega_{12},&A=A_{12},
\end{cases}
\]

であり、どちらかは未選択である。従って回答は次の三段階に分かれる。

- 「非算術は 648 個か」: **YES***。
- 「orientation に依らず非算術行を名指しできるか」: **YES、432 行**。
- 「実際の全 648 行を一つの roster として名指しできるか」: **NO**。残る 216 行が未選択。

typed unit action は square units `1,4,7` で両候補を個別固定し、nonsquare units
`2,5,8` で交換する。従ってこれは単なるラベル替えではなく、marked

```text
P5-REP-STOP-MISSING-IOTA-GAMMA-EPSILON
```

または同等の authenticated joint marked Frobenius row が必要な一ビットである。
現 inventory は observed rows 0 のままである。

## 4. 証拠階級の裁定表

| 主張 | 現在の格 | 備考 |
|---|---|---|
| 972 元群・全 index-3 subgroup・候補 13 本（normal 1、nonnormal 12） | cross-checked | producer/checker 独立再構成 |
| component 全射 6 本、row 891 を加えて 2 本 | cross-checked | 有限 subgroup predicate のみ |
| (108+216+216+432) 分割、row 9/36 が両候補外 | cross-checked | arithmetic interpretation なしでも成立 |
| (|A|=324)、marked fibre-product 記述 | accepted theorem-framework-relative paper package | 算術 324-row payloadではない |
| (A\not\trianglelefteq X) | paper-proof relative (T-37 / ruling 1210) | machine/Lean cross-check ではない |
| (A\in\{A_9,A_{12}\}) | paper-relative + cross-checked finite implication | v76 の最大結論 |
| (O) の432行と row 9/36が実際に非算術 | 同上 | orientation 不要 |
| (A=A_9) または (A=A_{12}) の個別選択 | `BLOCKED_UNKNOWN` | `selected_A_cand=null` |
| actual full 648-row roster | NOT SELECTED | 二候補は再構成可能だが actual bit がない |
| fake / compatible profinite witness / Ihara conclusion | 未成立 | 本監査から昇格しない |

## 5. 敵対的 provenance 注記

1. `provenance/CLAIMS.md` の現行 C-972 は依然 **972 の scalar cardinality only** を
   cross-check 対象とし、v76 の unordered-pair arithmetic claim に独立の登録項目はない。
   従って v76 の mixed grade を「arithmetic payload cross-checked」と短縮してはならない。
2. `sol/sol_reply_159_iv.md` §32.1 は v76 の作成時 SHA を
   `7d0458e43a9795c053ee3f620bc067671e06052fb5d6c61faf826d3685294623`
   と pin するが、今回読んだ現ファイルは 15,834 bytes、SHA-256
   `e77ed198d5facadb245166decf023fc4e3417fbd188ec10f8286fb4c7e09cb5f`
   で一致しない。意味内容は上記裁定と整合するが、durable claim 化する際は現版を
   versioned repin すべきである。
3. v67 の `H_pair=BLOCKED_UNKNOWN` は有限 receipt 単独について正しい。v76 はそれを
   **紙上 package 相対に限って** supersede する。v67 の
   `selected_A_cand=null` / arithmetic payload false は supersede されない。

## 6. v220-W への写像

v220 の固定表では W は

```text
compatible finite shadows / nonarithmetic roof binding / Ihara conclusion: 0/3
```

である。本監査は arithmetic roof prerequisite の格を精密化しただけで、新しい compatible
finite shadow、compatible cofinal lift、または Ihara conclusion を一つも作っていない。
従って **W は 0/3 のまま**であり、F(fake fallback)にも加点しない。

証人線には full 648 roster は不要で、共通 outside の row 36 一本で足りる。しかし row 36 の
非算術性が paper-relative に閉じていることと、その row を保つ compatible cofinal lift があることは
別の gate である。

## 7. 荷重証拠と再現コマンド

主要な現物 hash:

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_idx3_arithmetic_producer_v2.py` | 52,173 | `b41a841695243548b12f7127aebcdddffbc22ba054c3ab68fbac8a579194ef2e` |
| `search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json` | 249,817 | `1fca084f396605a8755534d19412a47f60af76406ca01a2ef99bc0c06f00e7d9` |
| `search/certs/d972_idx3_arithmetic_execution_manifest_v2_20260823.json` | 1,317 | `c87efd18ca3fe7c8870d302e687a1e6c2cd8aa261fa5b3774c2709fbc1946975` |
| `crosscheck/check_d972_idx3_arithmetic_v2.py` | 50,227 | `21b2946112588458d7548c4d605e1b0fdd16b828331596d9c37fb51ace45c26a` |
| `crosscheck/verdicts/d972_idx3_arithmetic_crosscheck_v2_20260823.json` | 8,804 | `6fd63e3453854a02f504695876e246f1f9fa388a0b3018db4a15c84ec35db525` |
| `crosscheck/d972_idx3_arithmetic_crosscheck_report_v2_20260823.md` | 1,752 | `223b5e769816d2ded1c683b0952791aacf114411c34b31b10cd04b9ab3b3f30e` |
| `sol/proof_r07_arithmetic_648_typing_erratum_v67.md` | 14,444 | `0ab809365ced95b6cfc83223f3034f8d9d543513c4f029e16067463f98e9eb12` |
| `sol/proof_r07_arithmetic_named_rows_v76.md` | 15,834 | `e77ed198d5facadb245166decf023fc4e3417fbd188ec10f8286fb4c7e09cb5f` |
| `sol/proof_r07_arithmetic_double_orbit_dihedral_absorber_v75.md` | 25,893 | `5340fcdf320e8893f903aca4f8e5e4b86d2f26e86f788b5582b81d53e7fe720b` |
| `sol/luna_reply_157bt_q5_premise_reconciliation.md` | 15,379 | `1f255b12093934a3944f5ac6a896b3b05d977c1441bdd6814c92b9f2c002817a` |
| `docs/notes/triad972_canonical_addendum_v2.md` | 3,753 | `5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09a76e764bfc` |
| `docs/notes/c1prime_s4_p5prime_closure_v2.md` | 8,155 | `3ce5f53923c63c20de95c5f5d36377457918ab5a7aa5ebb277de09a76e764bfc` |

記録済み producer コマンド:

```powershell
python -B search/d972_idx3_arithmetic_producer_v2.py --selftest-only
python -B search/d972_idx3_arithmetic_producer_v2.py
```

v2 checker の再現形:

```powershell
python -B crosscheck/check_d972_idx3_arithmetic_v2.py `
  --receipt search/certs/d972_idx3_arithmetic_receipt_v2_20260823.json `
  --manifest search/certs/d972_idx3_arithmetic_execution_manifest_v2_20260823.json `
  --output crosscheck/verdicts/d972_idx3_arithmetic_crosscheck_v2_20260823.json `
  --report crosscheck/d972_idx3_arithmetic_crosscheck_report_v2_20260823.md
```

本監査ではこれらを再実行せず、既存 immutable receipt/verdict と紙上依存だけを読んだ。
git、network、GHA、Lean、重い計算は使用していない。
