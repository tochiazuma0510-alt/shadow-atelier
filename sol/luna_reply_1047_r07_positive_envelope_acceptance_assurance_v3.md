Task1047 — positive envelope の acceptance 候補旗を型別に受ける限定修理 v3

**F1. 結果と変更範囲。** Task1047（2806 B / SHA256 `6f1cea15a52be593952a52200200aaf039350a9d7bfd2b8edadf053d40c718dd`）を全文読了し、指定新 helper と本返信だけを作成した。旧受領器が acceptance を含む5票へ一律 `candidate=false` を要求していた箇所を、公開WFと実metadataどおり acceptance は厳密 Boolean `true/false/false`、残り4票は厳密 Boolean `false/false/false` に分けた。新helperの通常変更はこの一箇所で、数学・source/WF・実artifact・旧helper/旧票を変更していない。新helper全実行、Python/import/AST/GAP/数学計算・GHA/network/git/credential・新agent は使用していない。実受領はrootの全差分読了後であり、今回の新版が実PASSしたとは報告しない。

新 helper は `%TEMP%/shadow-atelier-audit163/audit-r07-positive-v5-envelope-metadata-v3.ps1`、**52521 B / SHA256 `c97964c1c3959d3141d695ec8a3f6441041f03199957232a0a034002597dace1` / LF429**。ASCII、CR0、BOMなし、末尾LF。本値で作者freezeする。

**F2. 実停止の独立確認。** 基点 v2 は52185 B / `2b4b974acdf366ee068292bc75bf497d744465efc9874adef3281483313a0cfd` / LF427で、指定pinと実ファイルを照合した。root session75275 が08:29:36.2507854Z→08:39:05.7291721Zに実行した旧結果は `%TEMP%/shadow-atelier-audit163/positive-v5-envelope-reception-v2.json`、267179 B / `0e0c0d80f2cc8b8e0996bd0a6b08857bbb84fc130b0e843a05e07f5f25f47121`。この票の全9 check の名前/状態と唯一のerrorを実metadataとして読み、8 PASS / 1 FAILを確認した。FAIL名は `all16-live-tuples-acquisition-acceptance-and-preservation-inventories`、errorは `System.Management.Automation.RuntimeException:metadata:no-assurance/candidate`、detailはnullである。rootの旧終了値はexit1。新版の実終了値は未観測である。

このFAILは旧helper実201行、同節の全16親 loopとcurrent-run確認の後の最終guardである。そのため、同節のそれ以前の全tuple/全pin/各before-after inventory比較へ到達したことと、節全体のPASS未成立を分けて記録する。同節を過去にPASSしたと読み替えない。他の8節は旧実票で独立のPASSを持つ。具体的には全ZIP/全展開file、source6/raw4/driver/runtime、実旧64の30+10pins、外側実行と未形成D、20/12/8 metadata群とP/D各新3群、入場/元int/repair来歴、全REPORTとpartial、保全INCOMPLETE四義務である。

**F3. 実5票と公開形成契約。** 実展開rootは `%TEMP%/shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1`。次の5票の全bytes/SHAと三旗の実 .NET 型を独立に読んだ。三旗はいずれも `System.Boolean` であり、文字列・整数・小数ではない。

| file | bytes | SHA256 | candidate / cross_checked / verified |
|---|---:|---|---|
| acceptance.json | 1493571 | `16e7fb53a9b557a35e9fe5c20f4a1d93014c946622569d827bf102d5b778a2f9` | true / false / false |
| live-parent-intake.json | 11248 | `899c520129aadfbf79486400b95411be473a68f740bae1bbec8b077042e1cfc4` | false / false / false |
| all-parent-files-before.json | 1483138 | `e3cdbb9cdf6bccbba86c694f5e50717b7628ad287a42e2c8885260597cff04eb` | false / false / false |
| all-parent-files-after.json | 1483138 | `e3cdbb9cdf6bccbba86c694f5e50717b7628ad287a42e2c8885260597cff04eb` | false / false / false |
| acquired-parent-files-after.json | 1491395 | `85aea26d06972a87f108a97821a956b42ebfe18192553e24ecb0372b64b31188` | false / false / false |

公開 `.github/workflows/d972-r07-continuation-positive-word-readout-v5.yml` の実560–561行は `FALSE_ASSURANCE={false,false,false}` と `ASSURANCE={true,false,false}` を区別する。実1287–1333行の `accept()` は全親/旧continuation/元rho2/pinsを受けた後、`WORD_SCHEMA+'.acceptance'` を `ASSURANCE` で形成する。一方、親inventoryや admission-result は `FALSE_ASSURANCE` を使う。この工程は通常P/Dの前であり、acceptance の候補旗は候補入力の受付を意味する。全正語・本D十一slot/grade readout・完成candidateを意味しない。P/D私的本文・私的票を読む必要はなく、公開WF形成と実metadataで原因が閉じる。

**F4. 限定差分と保持。** 新実201–203行は、(1) acceptance.candidate の `-is [bool]` と `-ceq $true`、(2) acceptance の cross_checked/verified の `-is [bool]` と `-ceq $false`、(3) 他4票の三旗の `-is [bool]` と `-ceq $false` を別に確認する。各拒否理由も `acceptance-candidate-admission-only` / `acceptance-no-completion-assurance/<key>` / `other-intake-no-assurance/<key>` と区別する。truthiness、`[bool]` cast、等値整数/floatの受理へ緩めていない。

残る変更は先頭Taskコメント、受領schema `.envelope-metadata-reception.v3`、`previous_helper` の基点v2実pin、今回の `repair_scope` のmetadataだけである。この5領域を逆置換した新helper全文は、旧v2全文と文字列/bytesで完全一致した。全差分を自己読了した。`fc.exe` の表示行番号は長行折返しで実LF行と異なるため、位置は実helperのLF行で示した。

全9 check、全ZIP/406 files/96 directories/3685457381 Bの実取得契約、source6/raw4、全16親metadata/現物旧64、全before/middle/after、型別D未形成、保全四未成立を保持する。Task1044のList[object] `.ToArray()` 五箇所、整数の `Int`、measurement の有限数型、全file SHAとinner sealの区別、既存標準JSON読取も不変。新一般parser/数値serializer/二重全走査/新数学suiteは追加しない。受領票は引き続き `CreateNew` だけで新規作成し、実入力treeに書き込まない。

**F5. 再受領とassuranceの境界。** rootが本helper全差分と本票を読了後に実行する再現コマンドを記す。ここでは未実行である。旧v2受領票は残し、新票を別pathへ作成する。

```powershell
$metadataHelper = Join-Path $env:TEMP 'shadow-atelier-audit163/audit-r07-positive-v5-envelope-metadata-v3.ps1'
if ((Get-FileHash -LiteralPath $metadataHelper -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'c97964c1c3959d3141d695ec8a3f6441041f03199957232a0a034002597dace1') { throw 'helper pin mismatch' }
& $metadataHelper -ArtifactRoot (Join-Path $env:TEMP 'shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1') -AcquisitionReceipt (Join-Path $env:TEMP 'shadow-atelier-audit163/positive-v5-run34009883488-root-acquisition-v1.json') -Old64Root (Join-Path $env:TEMP 'shadow-atelier-cegar-resume64-run33990567016-candidate-a1') -ReceiptPath (Join-Path $env:TEMP 'shadow-atelier-audit163/positive-v5-envelope-reception-v3.json')
```

新受領票自身の candidate/cross_checked/verified/mathematical_replay/full_A0/positive_completion は全false、grade2 MEMBER/NONMEMBER は両 `NOT_DECIDED` のまま。元workflowはfailure、元preservationはINCOMPLETE、本Pは資源停止、本D/正語完成/実D前後境界と最終run票は未形成という実状態を昇格しない。新版のmetadata受領がPASSになった場合も、意味は全取得envelopeと公開metadataの照合完了だけである。実PASS/FAILと実終了値は次のroot受領結果で別に記帳する。

AUDIT_1047_VERDICT: STATIC_METADATA_REPAIR_READY — strict Booleanの候補入場旗を型別に修理し、全差分/実metadata/公開形成契約を照合済み。新helperを上記pinでfreeze、root実再受領は未実行。
