# retracted/ — 撤回済み証明書(certificates/bfc/)

## bfc-antecedents_v1_retracted.json (旧 `certificates/bfc/bfc-antecedents.json`, schema `bfc-antecedents-check/v1`, 17/17 PASS)

**撤回日**: 便 44 検収対応(実装担当・2026-07-27)。

**撤回理由**(`sol/sol_reply_44_bfc_v2.md` F6.1): `search/bfc-antecedents-check.g` は
D1 (3.6) の `z-bar = (x-bar y-bar)^{-1} = (r^2 s, r^-1 s, r)` を、`x-bar,y-bar` に
既に適用済みの marked transport(論文の `rs` を GAP の `s*r` と読む規約 — Sol 便01 F3、
`Phi=(phi_1,id,phi_3)`, `phi_1(r)=r,phi_1(s)=r^-2 s,phi_3(r)=r^-1,phi_3(s)=s`)を
適用せず、生の座標のまま `tr(r^2*s,1)*tr(r^-1*s,2)*tr(r,3)` として埋め込んでいた。
`y-bar` は移送側(`tr(s*r,...)`)なのに `z-bar` だけ未移送という混在の結果、
`n=3` で

```
x_g y_g z_g = (r, 1, r^2) <> 1
```

となる(Sol が紙上計算・本便で GAP 実測でも再現)。すなわち「x,y,z が同じ marked
object(D1 (3.1)(3.6) の x-bar,y-bar,z-bar)を指す」という照合器の前提が崩れており、
Node 側(`search/week4-bfc-antecedents.mjs`、独立の整数エンコーディング実装で
`z-bar` を直接埋め込み・xyz=1 を自明に満たす)との一致は「同じ marked object を
helper 非共有で照合した」という cross-check の型を満たしていなかった。
17/17 という表示自体は本ファイルの数値どおりだが、上記の理由で
`cross-checked` 昇格の根拠にはならない(便44 F6 が同旨)。

**帰結**: `search/bfc-antecedents-check.g` を修理し、

1. `zg := (xg*yg)^-1` として直接計算(`x-bar,y-bar` が既に一貫して移送済みなので
   積の逆元を取るだけで自動的に整合する)。
2. `Phi` を `D_n` 上の準同型として明示構成し(`phi1,phi3`)、D1 (3.6) の生座標に
   `Phi` を後合成した結果が `zg` と一致することを独立に検査(`z_phi_transport_check`)。
3. `x_g*y_g*z_g = 1` を fail-closed fixture として追加(`xyz_identity_check`)。
4. `kappa(m)` 第 3 スロットの符号 `-kap` を「全単射になる符号を試した」較正では
   なく、同じ `phi_3(r)=r^-1` の明示移送から導出し、`kap in {0,1,2}` 全部で
   `Image(phi_3, r^kap) = r^{(-kap) mod 3}` を検査(`kappa_phi_sign_check`)。
5. Sol 便43 F2.1 の反例で `<X>` が `P/H` 上推移的であることを明示に検査
   (`X_transitive_on_P_over_H`、旧版は位数・指数・normalizer だけだった)。
6. `V3` の該当 `H` の個数 `v3_matching_H_count` を JSON に記録(旧版は
   `pass_count` の中に埋もれ、値自体を保存していなかった)。
7. script/入力 doc/node 対応物の SHA-256 を `provenance` block に記録。

再走結果は **21/21 PASS**(旧 17 件 + 上記 4 件の新規 fail-closed 検査)。
target H(order 18, |Lambda|=6)・`|Aut(G3)|=1296`・`Lambda`-stabilizer `432`・
`GT(K^(3))` 12 元はいずれも数値不変(旧証明書と一致)。数値そのものは
z の修理前後で変わらなかったが、これは「z が旧版の target 同定・passport
検査に(たまたま)影響しなかった」ことの確認であって、marked-fidelity の
欠陥が無害だったことの証明ではない — 欠陥自体は実在し、今回の修理で閉じた。

**裁定根拠**: `sol/sol_reply_44_bfc_v2.md` F6(F6.1/F6.2/F6.3)。
後継は `bfc-antecedents_v2_retracted.json` を経て、現行版
`certificates/bfc/bfc-antecedents.json`(schema `bfc-antecedents-check/v3`)。

## bfc-antecedents_v2_retracted.json (旧 `certificates/bfc/bfc-antecedents.json`, schema `bfc-antecedents-check/v2`, 21/21 PASS)

**撤回日**: 便45 検収対応(実装担当・2026-07-27)。

**撤回理由**(`sol/sol_reply_45_bfc_final.md` F4・F5、裁定47 点3・4): 差戻し理由3
「GAP 側の fail-closed・V3=12 の assert・Phi による全 marking の同時移送は、
報告どおりには実装されていない」、および理由4「証明書の input digest が現在
どの正本にも一致せず」。具体的には

1. `ck()` は failCount を数えるだけで、失敗時に `Error` せず常に証明書を書き出していた
   (fail-closed 未実装)。
2. `V3` の判定が `v3bad = 0 and v3n > 0` のままで、便44 F6.3 が要求した
   `v3n = 12` の明示 assert になっていなかった。
3. `z_phi_transport_check`・`kappa_phi_sign_check` しか証明書化されておらず、
   `x_g,y_g` の生座標移送、および `f_{m,k}`(GT(K^(3)) 全12元)の移送は
   fixture 化されていなかった。
4. `provenance.input_doc_sha256` (`8082effe...`) が、その時点で
   `docs/week4-BFC攻略_opus_v1.md` に実在するファイル(`659a9570...`)と
   不一致だった(バージョニング移動後に証明書を再発行していなかったため)。

**帰結**: `search/bfc-antecedents-check.g` を修理し、

1. `x_g,y_g` についても `z_g` と同じ様式で D1 (3.6) 生座標の
   `Phi=(phi1,id,phi3)` 移送との一致を fixture 化(`x_phi_transport_check`,
   `y_phi_transport_check`)。
2. `BuildPhi` 内で `f_{m,k}` の D1 (4.9)(4.12) 生座標の Phi 移送を、実際に
   使う 12 個の `(m,k)` すべてについて個別検査し(`fk_phi_transport_check_all12`)、
   `x,y,z,f_{m,k}` の同時移送を単一 fixture `all_markings_phi_transport_check`
   として集約。
3. `V3` の assert を `v3n = 12` の明示値一致へ強化。
4. 証明書書出し直前に `failCount <> 0` なら `Error` して停止する fail-closed
   gate を実装(意図的に `v3n = 99999` へ壊して `Error` 発生・証明書
   未更新・`exit code 1` を実測確認済み)。

再走結果は **25/25 PASS**(旧 21 件 + 新規 4 件: `0b`,`0c`,`2b`,`2c`)。
数値(`target_H` order 18・`|Aut(G3)|=1296`・`Lambda`-stabilizer `432`・
`V3` 該当 `H=12`・`GT(K^(3))` 12 元)はいずれも不変。
`provenance.input_doc_sha256` は現在の
`docs/week4-BFC攻略_opus_v1.md`(`659a9570...`)と一致するよう再計算済み。

**裁定根拠**: `sol/sol_reply_45_bfc_final.md` F4/F5、`sol/裁定_47_ben45.md` 点3・4。
後継は `certificates/bfc/bfc-antecedents.json`(現行版、schema
`bfc-antecedents-check/v3`)。
