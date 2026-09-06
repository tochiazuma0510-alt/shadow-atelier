# Task1043 返信 — positive resource 受領器の実観測型修理 v3

## F1. 完成範囲と実 pin

新 `%TEMP%/shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata-v3.ps1` と本返信だけを作成した。新 helper は **82,046 B / SHA256 `d871d8fb8295b235aaa3dd449c2597ead2063356e2a02430044fb468a4f13765` / LF1115**、ASCII、CR0、BOMなし、最終 LF、末尾空白0で凍結する。helper の実行、dot-source、local canary は行っていない。

指示書1043は root の06:43 UTC追補まで全文読了（4,449 B / `4cdd41e67fb02c826bba5851c79a616d3c13903da864113db7ba8770cea6f140` / LF17）。公開返信1039も全文読了（13,910 B / `994f1837639a26be912b72a7ddc9896c0780888fce63e8285ef7e21cb8f5e97a` / LF101）。基点 v2 の全1,107行を読み、新版の全保持部分・全差分を静読した。宣言した変更を文字列として逆置換した結果は、基点全文と完全一致した。AST、Python、数値処理は使っていない。

基点は81,620 B / `51fad0e611715799bf9f78dd11b4c302e642da3f2657df43b166e09c6cffbaea`。旧 v1/v2 helper、旧返信、旧受領票、P/D source、WFは変更していない。新 helper で読む source は公開 receipt と file pin だけで、P/D私的本文・相手私的返信は読んでいない。

## F2. 実停止3件と原因の区別

root session85355 の旧実受領票 `%TEMP%/shadow-atelier-audit163/positive-v5-run34009883488-root-resource-metadata-v2.json` を必要な keys/scalars に投影して読み、実 bytes/SHAを照合した。1,676,526 B / `222a371e78acbee0f2718874a64279c5dd6ed4901d0419eae3f441083e79563e`、`FAIL_RESOURCE_METADATA`、errors3/incomplete5である。

| 旧 error | 原因と処置 |
| --- | --- |
| `D_fixture_session: resource_metadata:nonempty_string_array` | 正常な先頭2群の `rejected_cases=[]` を全3群共通の非空 guard が拒否。公開型どおり先頭2群は空配列可、第三群は非空のままにする。 |
| `resource_output_inventories: resource_metadata:exact_fields:label path status inventory completed_arithmetic_inferred` | `NOT_CREATED` の実4字段に `OBSERVED` の5字段を要求していた。状態別 exact fields と実不在を照合する。 |
| `outer_success_to_session_completion: resource_metadata:successful_D_fixture_session` | 第一 error の派生。独立した外側 gate の不具合ではなく、当該 gate は変更しない。 |

第三 error の経路は基点 `Dsession` L545–561にある。entry は先に `Sessions` へ登録され、directory存在後に `INCOMPLETE` となる。全 sample の終端確認後、L560の `Dselftest` が上記非空 guard で throwするため、L561の `COMPLETE_RESOURCE_SELFTEST` と `saved_result` 代入に到達しない。続く Job は例外をerrorsへ保存して継続し、外側D_SELFTESTの実exit0に対する gate が、その未完entryを正しく拒否した。

実旧票でも D fixture は一件、state `INCOMPLETE`、54 complete samples、final LF=true、typed_lines_valid=true、last phase=`resource_finish:PASS_RESOURCE_SELFTEST`、saved_result未形成であり、この経路と一致する。D_SELFTESTの外側exitは0、本Dは未開始で別entryの `NOT_CREATED`。新sourceの外側成功gate L1050–1065は基点と同じで、第一errorを隠して外側だけ通す変更はない。新受領の成否や件数をこの静的原因追跡から先取りしない。

## F3. D selftestの公開型と保持境界

実 `D_SELFTEST-stdout.json` と `resource-selftests/D/scratch/selftest-result.json` はともに9,411 B / `161967cb2d6e35030e42e2d5175f73c6f8ea0af670210475d0d4a961001c6816`。三群のexact fields、名前/順序/status、全20拒否名と5resource-stop名を公開metadataとして読んだ。

| 群 | 実 rejected_cases | v3の型 |
| --- | ---: | --- |
| `disk-catalog-pages-canonical-and-refcounts` | 0 | JSON配列。空可、要素があれば非空str。 |
| `same-D3-eight-op-eleven-slot-and-physical` | 0 | 同上。nullやscalarへ置換不可。 |
| `scratch-capacity-and-authentication-negatives` | 20 | 非空のstr配列。既存resource_stop_casesも非空str配列を維持。 |

公開 WF5 の `check_canaries` L1886–1899は各 rejected_cases を空可の string_list とし、`check_D_resource_selftest` L1538–1580は第三群だけ非空を追加要求している。新 `Dselftest` L685–687の変更は `Strings ... ($i -eq 2)` と説明一行だけで、この公開境界に一致する。実20件を新たな私的 negative catalogへ展開したり、未公開のexact D keysetを仮定したりしない。

第一群の157 nodes /42,068 bytes /SHA `798e668c889d8d4b7740733cb1ff72ffba31c3d4642b59f142ff8f91b9f90692` とcache eviction1,297、第二群の11 slots/80,644 coordinatesと三つのtrue flagsは保存metadataの値として読んだ。第二群 all_payloads36件は旧実受領票の全file descriptor表と両D3/D4側で全件一致した。これは保存 descriptor同士のmetadata比較であり、36payloadのFox値や数値配列を当便で再計算したものではない。

新helperは従来の全 fixture file EOF/bytes/SHA、D3/D4 all_payloads の全roster一致、source/raw/settings/path/binding、sample終端、ordinary count、全assurance falseを維持する。先頭2群に存在しない拒否名を補わず、第三群の空配列を合格にしない。

## F4. inventoryの型別修理

実 `resource-output-inventories.json` は19,888 B / `24bc7c54842e86061063ddf0650ce0afee3e10e45f80dc8b8896889bedd2a72e`。全4rowの実keysは次のとおりだった。公開 WF5 L2194–2204の出力分岐も直接読んだ。

| labels | status | exact fields | inventory |
| --- | --- | --- | --- |
| `P_SELFTEST`, `D_SELFTEST`, `P` | `OBSERVED` | `label path status inventory completed_arithmetic_inferred` | 実object。completed_arithmetic_inferredはfalse。 |
| `D` | `NOT_CREATED` | `label path status inventory` | null。完成推論字段は存在しない。 |

新 `ResourceInventories` L954以降は共通4字段の存在と登録label/pathを確認した後、OBSERVEDは従来のexact5字段・strict false・実directory存在・全 `InventoryMatch` へ接続する。NOT_CREATEDはexact4字段・inventory=null・同pathにdirectoryもfileも実在しないことを要求し、`RECORDED_NOT_CREATED` をINCOMPLETEへ記帳する。不在を空の成功inventoryに置換しない。余剰の第五字段もNOT_CREATEDでは拒否する。

既存の5字段FAIL分岐と未知statusの拒否は保持した。公開WFにはinvalid-existing-rootを記帳する4字段FAIL分岐もあるが、これは今回の実rowにはなく、新受領器で成功や通常の未形成へ読み替える対象にしていない。基点どおりその形はexact fieldsの構造FAILとなる。本便は全失敗wrapper形の汎用adapterを追加する作業ではない。

全 `InventoryMatch` は不変である。実file不足/余剰、bytes/SHA不一致、余剰directory、宣言上子を持つdirectoryの不足はFAIL。宣言fileも宣言subdirectoryも持たない空leafだけの欠損は、全file descriptor照合後も `INCOMPLETE_DECLARED_EMPTY_DIRECTORIES_MISSING` として残す。REPORTにmkdir、file修理、削除、無言除外を行わない。

## F5. 保持した未完と計測・保証の境界

旧票のincomplete5は、P outer exit3、D process未開始、P session UNKNOWN_RESOURCE、D session未形成、Pの空 `index-receipts` directory欠落である。今回の修理で従来到達しなかったNOT_CREATEDの記帳が追加され得るため、新error/incomplete件数やtop statusは実再受領まで未観測とする。欠損・資源停止を消してPASSへする修理ではない。

実P stdoutは `UNKNOWN_RESOURCE`、phase=`literal-DFS`、reason=`ResourceStop:literal-DFS:deadline`、elapsed5400.275689、successful_bundle=false、partial_output_only=true。root既知の進捗 A0実0/1・rung1/6、grade2 MEMBER/NONMEMBERともNOT_DECIDED、full_A0=falseを変更しない。本D未形成を十一slot/80,644全比較の実完了と扱わない。

PS5.1の `Float` は有限Double/Decimal、`Int` はint/long限定、boolはBoolean限定というv2修理を保持した。整数を等値Decimalへ緩和していない。全 JSON/JSONLのASCII/LF/EOF、元bytesのseal tokenを除いた既存hash照合、全regular file stream hash、各binding/cache/index receipt、入力path非reparseと外部新receiptのCreateNewも不変である。新一般parser、canonicalizer、inner JSONの数値再serializationを追加していない。

Task1043追補は「末尾 full scan」のroot文言を訂正した。実基点は `ScanAll` 一回であり、その一回全file hashと `input_tree_written=false` / `input_tree_second_full_hash_pass=false` を正確に維持した。二回目のscanを新設したと記録しない。全16親bodyの独立再受理・最終envelope全体の裁定・数値再演は当helperの外である。未公開D追加keysetはNOT_ADJUDICATED、負対照catalogは全bytes保存のままで通常本D証明書へ昇格しない。candidate/cross_checked/verified/math_replayは全てfalse。

## F6. 最終差分・CLI・未実行

機能差分はD rejected_casesの二群許容とinventoryの状態別exact fieldsだけ。ほかはTask1043注記、schema=`d972.r07.positive-v5-resource-metadata-reception.v3`、`previous_helper={file:'audit-r07-positive-v5-resource-metadata-v2.ps1',bytes:81620,sha256:'51fad0e611715799bf9f78dd11b4c302e642da3f2657df43b166e09c6cffbaea'}` の来歴更新である。外側success gate、完成/未完/FAIL優先順位、全保持metadata経路は不変。新public字段を補完していない。

rootは実run `34009883488/1`、head `a590fa9a70322145f1c0688a8f14d2c9640b1bf3` の全 ZIP 1,373,772,131 B / `41c95c7171c9192ec1d589a715c911f7470bb69fe520b80558334ad60636ac61` と全展開406 files/96 dirs/3,685,457,381 bytesを受領済みである。この取得とhelperの再受領を区別する。当便はmetadata小file/旧票/source文字列の読取・hash・型/descriptor比較だけを行い、新helperの全body処理は実行していない。

rootが新helper全文・全差分・本返信を読了後、旧v2票とは別の未存在v3票へ実行する。

```powershell
$ErrorActionPreference = 'Stop'
$taskHelper = Join-Path $env:TEMP 'shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata-v3.ps1'
if ((Get-FileHash -LiteralPath $taskHelper -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'd871d8fb8295b235aaa3dd449c2597ead2063356e2a02430044fb468a4f13765') { throw 'Task1043 helper pin drift' }
powershell.exe -NoProfile -File $taskHelper `
  -Root (Join-Path $env:TEMP 'shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1') `
  -ReceiptPath (Join-Path $env:TEMP 'shadow-atelier-audit163/positive-v5-run34009883488-root-resource-metadata-v3.json')
```

新helperの実受領票は未形成・成否未観測。ローカル数学/Python/import/AST/GAP、GHA/network/git/credential、新agentは実行していない。静的に3errorsの原因と限定修理を閉じ、実行結果はrootへ留保する。

AUDIT_1043_VERDICT: RECEIVER_V3_COMPLETE_STATIC_ONLY_ROOT_EXECUTION_PENDING; observed_errors_two_causes_and_one_derived; outer_success_gate_unchanged; candidate=false; cross_checked=false; verified=false; math_replay=false.
