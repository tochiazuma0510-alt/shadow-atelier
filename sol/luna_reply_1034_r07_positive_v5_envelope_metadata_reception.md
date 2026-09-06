# Task1034 — positive WF5 envelope metadata 受領 helper

F0. Task1034 を全文読了した。変更は本返信と指定 TEMP `audit-r07-positive-v5-envelope-metadata.ps1` だけ。WF5、公開返信1019/1021/1022、公開1024、分担1033、旧v4 metadata helperを読み、実artifactの全取得・全展開完了通知後に公開JSONを読んだ。P/D私的source本文・私的作者票は今回読んでいない。Python/import/AST/GAP/数学、network/git/credential、新agent、helperの実行は行っていない。

F1. 準備した helper は `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/audit-r07-positive-v5-envelope-metadata.ps1`。最終 **51,822 bytes / SHA256 4fcb5fffa4cf9650290cb35b0546f7dc6d989fc3630ba599ee22c9a42df859fb / LF425 / CR0 / ASCII / BOMなし / final LF / 行末空白0**。全本文を静的に読み、末尾まで保存して凍結した。root がこの最終全本文を読んでから実行する準備版であり、本票は新helperの機械PASSではない。前の大きな保存呼出しは中断され、初回実保存の前にはfileが形成されていなかった。その後、native PowerShellによる短い保存単位へ切り替えて全tailを保存した。

F2. 対象の実取得境界は次のとおり。これはrootの全ZIP/全展開認証の受領と公開取得票の読取であり、今回のhelperを既に実行したという意味ではない。

| 項目 | 実受領値 |
|---|---|
| run / attempt | 34009883488 / 1 |
| head | a590fa9a70322145f1c0688a8f14d2c9640b1bf3 |
| workflow ID / job | 351315722 / 101423728128 |
| workflow path | .github/workflows/d972-r07-continuation-positive-word-readout-v5.yml |
| 診断artifact | 9983263449 |
| ZIP | 1,373,772,131 bytes / 41c95c7171c9192ec1d589a715c911f7470bb69fe520b80558334ad60636ac61 |
| 取得票 | positive-v5-run34009883488-root-acquisition-v1.json、736 bytes / 1d6d0fcd51bf13941cd55eff1559aa92ca5b0c78bc2a54efea73876e718ee32d |
| 実展開 | 406 ZIP entries / 406 files / 96 directories / 3,685,457,381 file bytes |
| 展開root | C:/Users/81905/AppData/Local/Temp/shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1 |
| WF5 | 180,687 bytes / a840cebcd0ba3f15ff2c31c13b0a09bacd140cb4c8e756466baafd052df8e436 |
| artifact内driver | 150,975 bytes / 2f7e5b3f495e3c471c0ceb702547d871e4abfa1abe2ef457e9d32579db8bd0df |

取得票の `workflow` は普通整数のID、artifact内 `launch.workflow` は上表のrepo-relative文字列として分離する。ZIPを新たに取得・展開・copy・mkdirする処理はhelperに置かない。既存ZIPを全stream/EOFまで再読し、全展開fileをsize/SHAへ結び、root取得票の実全件数とも結ぶ。

F3. helperは九つのmetadata節を持つ。①取得票/全ZIP/全実file、②凍結WFからのdriver全文とsource6 Python・raw4・WF・runtime・保存前/形成済middle/後の全pin、③16 live tuplesと各run/artifact API保存票、acquired前/後・acceptance・全親前/後inventory、④現物旧64 rootの全inventory、公開30 entryとnested completion10 entry、全retained top-level copies、⑤各形成済command/start/stdout/stderr/exit/outer wall/資源枠とD未形成、⑥inventory20/path12/public D型8とP/D各3群、⑦admission・元startの五字段・repair来歴、⑧REPORT前/middle/後・全word/scratch/fixture/hidden/partial、⑨実保全INCOMPLETEの四理由と未完成義務を結ぶ。

旧64は `C:/Users/81905/AppData/Local/Temp/shadow-atelier-cegar-resume64-run33990567016-candidate-a1`。全30 entryとcompletion10 entryの公開pinは `{bytes,sha256}` 辞書で読み、現物全file hashへ結ぶ。保存Cの全64段PASS、64/1450/8155/Separator/UNKNOWN_CAP、HEAD/result/current lambda/target/owner/source/start/fixedを公開選定票へ結ぶ。旧算術・旧成功suiteの再演は0。16親のうち今回artifactに再収録されない上流全payloadについては、保存された全取得/保全inventoryと凍結tupleを受領する境界を明示し、全親payloadをこのPCで再取得したと主張しない。

F4. 実P stdout全文は514 bytes / 664edc84e7fdaa94d87ed237052dce19694739122f5e189e66b1268ecd43d7e9。`status=UNKNOWN_RESOURCE`、`phase=literal-DFS`、`reason=ResourceStop:literal-DFS:deadline`、`elapsed_seconds=5400.275689`、max_seconds5400 / max_memory_mib7168を読んだ。外側 `executions/P-receipt.json` は815 bytes / 3b27eb40bb30c22ad3711e0d4ea18099849969c1c04406ef0dca010f9a1474de、exit3、wall_seconds5402.03076。stderr `P.log` は19,865 bytes / 56210794be0849a942fc0f0cac1e24564254a81a6619ae218b70d2564f2428ca。`word/resource-stop.json` の全bytesは同stdoutへ結ぶ設計である。

実Dの通常command/receipt/stdout/stderr/exit、D output、resource-D、最終run-receiptは未形成。Dの新resource-selftestの形成済PASSとは別に扱う。helperの分類値は実receiptから作り、UNKNOWN_RESOURCE/FAIL/outer timeout/signal/未形成を相互に書き換えない。PS5.1の実JSON読取では有限非負floatがSystem.Decimalにもなるため、`Finite` はDecimal/Doubleを許す。`Int` はInt32/Int64だけとし、boolや等値Decimal/Doubleを普通整数へ緩和しない。

F5. 公開canaryの実三票と新六群票を全文読んだ。inventory20は形成済stdout/exit/logを全pinへ結ぶ。path12とpublic D型8はdriver内で形成したmetadata票であり、存在しない別stdout/exit/logを要求しない。P三群は `disk-index-cache-and-integrity`、`old-word-bytes-and-new-reread`、`scratch-line-and-resource-boundaries`。D三群は `disk-catalog-pages-canonical-and-refcounts`、`same-D3-eight-op-eleven-slot-and-physical`、`scratch-capacity-and-authentication-negatives`。D第一/第二群の `rejected_cases=[]` は実正対照の合法な形であり、全群に非空逆対照を要求しない。Pの `old_full_suites_run` とDの `old_success_suites` は別の字段として整数0を読む。public resource telemetry/index/cacheの細部は1033が担当し、1034はその保存全fileをinventory/hashと外側executionへ結ぶ。

F6. `preservation-result.json` のstatusは実 `INCOMPLETE`。errorsは順に、`word-before-D` のFileNotFoundError、`word-unchanged-by-D` の不成立、`output-D` のregular-root不成立、`report-before-D.json` のmissing-before-boundary-receiptである。rootからの説明に加え、この四件の元reason全文を実JSONで読んだ。全16親/source/raw/acceptance/driver/acquired source不変の実字段はtrue。これだけでデータ毀損とは判定しない。`driver-always-failure.json` はphase always、reason `ValueError:positive_word_workflow:always-preservation-incomplete` としてそのまま受領する。

REPORT最後の保存inventoryは自身の後書き制御票を含まないため、helperはWFの明示した後書き票だけを登録し、その他の追加payloadを黙って除外しない。前/中の全既存fileは全hashで後へ結ぶ。ZIPが省いた空directoryについては、実ZIPにある明示/暗黙directoryと、保存inventoryが宣言した空directoryを分け、後者の未回収を `DECLARED_EMPTY_DIRECTORY_NOT_PRESENT_IN_ACQUIRED_TREE` / restored=falseとして記録する。fileを持つdirectoryの欠落は許さない。ディレクトリやfixtureを復元・間引き・削除してPASSにする操作はない。

F7. root実行用の四引数は `-ArtifactRoot`、`-AcquisitionReceipt`、`-Old64Root`、`-ReceiptPath`。ReceiptPathはrootが選ぶ未使用TEMP fileとし、parentは実在が必要である。全受領が通ればmetadata PASS/exit0、必要節未完ならINCOMPLETE/exit3、pinやmetadata不一致ならFAIL/exit1を出す。初期の引数/path自体が不正なら処理を拒否する。rootが実行する例は次のとおりで、本票作成時には未実行である。

```powershell
& "$env:TEMP/shadow-atelier-audit163/audit-r07-positive-v5-envelope-metadata.ps1" -ArtifactRoot "$env:TEMP/shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1" -AcquisitionReceipt "$env:TEMP/shadow-atelier-audit163/positive-v5-run34009883488-root-acquisition-v1.json" -Old64Root "$env:TEMP/shadow-atelier-cegar-resume64-run33990567016-candidate-a1" -ReceiptPath "$env:TEMP/shadow-atelier-audit163/positive-v5-envelope-reception-v1.json"
```

新一般JSON parserや数値canonicalizerは導入せず、標準ConvertFrom-Jsonと全file/ZIP hash・型別字段比較だけを使う。内側JSONの自己sealは再計算しておらず、全取得ZIP/full-file pinに基づく受領範囲を明示する。出力受領票はcandidate/cross_checked/verified/mathematical_replay/full_A0=false、grade2_member/grade2_nonmember=NOT_DECIDED、positive_completion=false。完成P、通常Dの全11slot/current-grade読出し、D前後の保全、完成run-receiptは残件のままである。

F8. rootの実行前静的findingを受け、resource observationの型分岐だけを修理した。実 `resource-output-inventories.json` を再読し、OBSERVEDのP_SELFTEST/D_SELFTEST/Pは `completed_arithmetic_inferred,inventory,label,path,status` の5字段、NOT_CREATEDのDは `inventory,label,path,status` の4字段で前者の字段が存在しないことを確認した。旧helperは分岐前に不存在字段を参照してStrictMode2で拒否する欠陥があった。修理後はstatusで分岐して各exact key集合を確認し、OBSERVEDだけでbool falseの `completed_arithmetic_inferred` と全inventory/file hash比較を要求する。NOT_CREATEDはinventory=null、実file/dir/rootの不在を要求し、成功や空算術値へ置き換えない。未知statusは拒否する。差分はこの一blockの +290 bytes / +5 LFだけで、逆置換の全文が旧51,532 bytes本文に一致した。入力tree・他の算術/受領gate・JSON解析方式は不変。更新後helperは上記51,822 bytes / 4fcb5fff…へ再凍結、rootも当方も未実行のままである。
AUDIT_1034_VERDICT: METADATA_HELPER_SOURCE_COMPLETE_FROZEN_UNEXECUTED; OBSERVED_P_UNKNOWN_RESOURCE_D_UNFORMED; NO_MATHEMATICAL_PROMOTION
