# Task1044 返信 — positive envelope受領器の object-list 配列化修理

## F1. 完成・凍結

指定の新 TEMP helper と本返信だけを作成した。新 helper は `%TEMP%/shadow-atelier-audit163/audit-r07-positive-v5-envelope-metadata-v2.ps1`、**52,185 B / SHA256 `2b4b974acdf366ee068292bc75bf497d744465efc9874adef3281483313a0cfd` / LF427**。ASCII、CR0、BOMなし、最終LF、末尾空白0である。rootが全最終差分を読了した同じpinで凍結し、sourceへの追加変更はない。

Task1044（3,447 B / `451c92c469c79a148e0ab818461e5ce73391851f42196f6c29769258031d1ce3`）、Task1034（4,214 B / `2ff716f0ab834da060b502b7dad643cfa1a2fcec3e93231e45c4a7783d91516c`）、公開返信1034（10,170 B / `e4465f682336821d93c740f196c866be837b14984b3fd17b65663308910c535b`）を全文読了した。基点helper全425行と、新版の全保持部分・全差分・末尾receiptを静読した。宣言した変更の文字列逆置換は基点全文と完全一致した。AST等を使った照合ではない。

基点 `%TEMP%/shadow-atelier-audit163/audit-r07-positive-v5-envelope-metadata.ps1` は **51,822 B / `4fcb5fffa4cf9650290cb35b0546f7dc6d989fc3630ba599ee22c9a42df859fb` / LF425** のまま。旧helper/返信・取得tree・全source/WFは変更していない。

## F2. 実停止と局所probeの区別

root session42789は旧helperのSHA guard後、初回実行でexit1 / `Argument types do not match` となり、`positive-v5-envelope-reception-v1.json` は未形成だった。当便のread-only存在確認でも旧v1票は存在しなかった。外側errorに内部の具体行は記録されておらず、実停止行を直接捕捉したとは主張しない。

rootは PS `5.1.19041.6456` の小さいmetadata-shape probeで、`List[object]` に一個のordered metadata辞書を入れた `@($list)` が同じ例外となり、`$list.ToArray()` は同じ要素を含む配列として成功することを局所確認した。List[string]のarray-subexpressionは成功した。この結果はTask1044に明記されたrootの実観測であり、当便で新helperを実行した結果ではない。

基点にはこの直接配列化が実List[object]に対して5箇所ある。最初の `Inventory` は最初のCheck内から呼ばれる。そこで例外が出る場合、CheckはFAILをlistへ記録できても、末尾でそのChecks自身を `@($Checks)` にして同じ種類の例外となる経路があった。OmittedDirectoriesも同じ型である。新v2は集計・返却・末尾receiptの全5箇所を直す。実rootでどのCheckが失敗したか、新票が形成できるか、全九節が合格するかはroot再実行の結果まで未観測とする。

## F3. 限定差分

| 場所 | 基点の式 | 新v2の式 |
| --- | --- | --- |
| Inventory L47 | `File-Map @($files)` | `File-Map ($files.ToArray())` |
| Inventory L48 | `files=@($ordered)` | `files=$ordered.ToArray()` |
| Subtree L54 | `files=@($fs)` | `files=$fs.ToArray()` |
| receipt旧L411→新L413 | `checks=@($Checks)` | `checks=$Checks.ToArray()` |
| receipt旧L412→新L414 | `...=@($OmittedDirectories)` | `...=$OmittedDirectories.ToArray()` |

各変数の生成元・型・使用先を全本文で追った。List内のobject、順序、個数、空配列を変更せず、明示的にObject[]へ出す。File-Mapの全descriptor型と重複拒否、Inventoryのordinal順、Subtreeの相対pathと全file pin、Checksの全節記録、未回収空directoryの各記録を保持する。

ZIP節L111の同名 `$files` はHashSet[string]であり、L132の `@($files)` は変更していない。List[string]のdirs/ds/rows/expected/argv/Unformed、文字列HashSet、既存JSON配列、pipeline結果を受けるarray-subexpressionも無差別置換していない。末尾の `$Checks | Where-Object` によるFAIL集計はそのままである。

残る差分はTask1044注記、receipt schemaを `d972.r07.continuation-positive-word-readout.v5.envelope-metadata-reception.v2` にすること、および二つの来歴字段だけである。`previous_helper` はexact `{file,bytes,sha256}` で上記基点51,822 Bの全pinを指し、`repair_scope` は上表5箇所の文字列配列である。内側のartifact/receipt schemaや旧JSONは変更しない。

## F4. 全九節と型・保全の保持

既存九Checkの本文と条件は不変である。対象は、①取得票/全ZIP stream/全展開file、②公開source6/raw4/WF/driver/runtimeと前中後pin、③16親live tuple/API保存票/取得・受理・保全の全inventory、④現物旧64全inventory/受付30entry/nested completion10entry/retained receipt、⑤形成済command/start/stdout/stderr/exit/資源枠とD未形成、⑥inventory20/path12/公開D型8/P3・D3群、⑦入場・旧start普通整数・repair来歴、⑧全REPORT/word/scratch/fixture/hidden/partialと前後境界、⑨実保全INCOMPLETEの四未完義務である。

OBSERVED resource rowのexact5字段とbool false、NOT_CREATEDのexact4字段・inventory=null・実不在を保持した。宣言された空directoryの輸送差は記録して復元せず、fileを伴う欠損、余剰payload、pin不一致を合格へ変えない。入力treeにmkdir、copy、上書き、削除はない。receiptはinput外の新TEMP fileへCreateNewするだけである。

Intはint/long、有限小数はDecimal/Doubleという既存の型を維持し、boolや等値floatを普通整数にしない。全bytes/SHA/EOF、型別字段、全順序、scope判定、全九節の成否優先順位を変更していない。一般parser/canonicalizerや内側JSON自己sealの再計算は追加しない。全親のうち今回取得treeに再収録されないbodyの独立再取得を主張しない。

## F5. 実来歴と未完成義務

対象はrun `34009883488/1`、head `a590fa9a70322145f1c0688a8f14d2c9640b1bf3`、診断artifact9983263449。全ZIPは1,373,772,131 B / `41c95c7171c9192ec1d589a715c911f7470bb69fe520b80558334ad60636ac61`、全展開は406files/96dirs/3,685,457,381bytes。取得票 `%TEMP%/shadow-atelier-audit163/positive-v5-run34009883488-root-acquisition-v1.json` は736 B / `1d6d0fcd51bf13941cd55eff1559aa92ca5b0c78bc2a54efea73876e718ee32d` を実再hashした。全ZIP/全展開完了はrootの既観測であり、新helperの再受領成否とは別である。

実PはUNKNOWN_RESOURCE、本Dは未形成。元保全INCOMPLETEの四義務は `word-before-D`、`word-unchanged-by-D`、`output-D`、`report-before-D.json` のまま。仮に全診断metadataの受領がPASSでも、完成P語、本D十一slot/current-grade読出し、D前後保全、成功最終run receiptを完成扱いしない。root既知のA0実0/1・階段1/6、grade2両NOT_DECIDED、full_A0=falseを変更しない。

rootから別途通知されたk64 metadata v2のPASSと、positive resource v3のINCOMPLETE_RESOURCE_METADATA（errors0/incomplete6）は、それぞれ別の受領結果である。本envelope v2の実票や数学保証の代用にしない。source内のcandidate/cross_checked/verified/mathematical_replay/full_A0/positive_completionは全てfalse、grade2_member/grade2_nonmemberはNOT_DECIDEDを保持する。

## F6. root実行入口と未実行境界

helper本体は当便で実行していない。四引数は基点どおり。rootから、同pinの全最終差分読了後、SHA guardと新snapshotを経て実受領を開始したとの通知を受けた。開始を成功と混同せず、結果は未観測として記録する。新v2票への再現入口は次のとおり。

```powershell
$ErrorActionPreference = 'Stop'
$taskHelper = Join-Path $env:TEMP 'shadow-atelier-audit163/audit-r07-positive-v5-envelope-metadata-v2.ps1'
if ((Get-FileHash -LiteralPath $taskHelper -Algorithm SHA256).Hash.ToLowerInvariant() -cne '2b4b974acdf366ee068292bc75bf497d744465efc9874adef3281483313a0cfd') { throw 'Task1044 helper pin drift' }
& $taskHelper `
  -ArtifactRoot (Join-Path $env:TEMP 'shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1') `
  -AcquisitionReceipt (Join-Path $env:TEMP 'shadow-atelier-audit163/positive-v5-run34009883488-root-acquisition-v1.json') `
  -Old64Root (Join-Path $env:TEMP 'shadow-atelier-cegar-resume64-run33990567016-candidate-a1') `
  -ReceiptPath (Join-Path $env:TEMP 'shadow-atelier-audit163/positive-v5-envelope-reception-v2.json')
```

局所作業は文書/source文字列の静読、対象型の追跡、全差分と文字列逆置換、bytes/SHA/EOL、取得票pinと旧・新receiptの存在確認だけである。Python/import/AST/GAP/数学/helper全実行、network/GHA/git/credential、新agent、P/D私的sourceの読取は行っていない。新metadata PASS/INCOMPLETE/FAILは未観測である。

AUDIT_1044_VERDICT: ENVELOPE_V2_OBJECT_ARRAY_REPAIR_COMPLETE_STATIC_ONLY_ROOT_RECEPTION_RESULT_PENDING; actual_failure_line_unobserved; root_local_probe_distinguished; candidate=false; cross_checked=false; verified=false; mathematical_replay=false.
