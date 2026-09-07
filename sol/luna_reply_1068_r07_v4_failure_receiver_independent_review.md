# Task1068 返信 — 早期 failure 受領器1066の独立静的別読

F0. 結論と実施範囲

最終受領器 57,665 B / `890a0e61f45cb636e62ddd80094d474d1ee31122290cb0fe8139d3b91c223d68` 全218行と、保存された4修理の全差分を独立に静読した。指定の実JSON型・全file pin・opaque raw区間を読み合わせ、残る必須findingは0件。本票は固定入力に対する限定metadata監査であり、1066作者の自己監査ではない。
Task1068全文、Task1066全文、返信1066全文を読了した。1066最終票は全JSONとして読み、6群の保存値・入力19 pin・全21出力・実診断treeと照合した。原受領器の再実行、P/C数学本文の読解、Python/import/AST/compile/GAP、Git/GHA/network/credential操作は行っていない。変更は本返信と新TEMP `shadow-atelier-audit163/task1068/` だけで、1064案・1065源・旧票・入力treeを変更していない。

F1. 固定した正本

以下のSHA256を実fileで再照合した。helperの安定snapshotも同じ全bytesで、実行していない。

| 対象 | bytes | SHA256 |
| --- | ---: | --- |
| Task1068 | 3178 | `8000263c7d49f69d4698439f1a30bd779413ebf34410462b2e3e2ecf030ee281` |
| 返信1066 | 9886 | `ec168225178be6aa0f1ccbcac9c163ba28fa5c00d0621d9912b4d7b4fb956dd3` |
| `audit-r07-v4-early-failure-v1.ps1` | 57665 | `890a0e61f45cb636e62ddd80094d474d1ee31122290cb0fe8139d3b91c223d68` |
| 最終票 `v4-early-failure-metadata-20260906T2236187823581Z.json` | 1064001 | `1daf1c00990125b74bde74933bbedeba0b33696d598d4ab838bebbefaea06c9b` |
| `task1066-output-pins-v1.json` | 5732 | `2c3d24d4e5b806a1912feaed184745ff17a7e52536ffeb61fbc70669ca1d4c09` |
| 最終process観測 | 1810 | `f09c718e8d4abe82f8a9a4baed9c50404c24f981a75269f141cf3b5d43531634` |
| 最終log | 1416 | `36afa45d0b1dfdf481e5a296d6bbf48710dfc51eaa1730eaeb5a3e3c152a62b0` |

全21出力は途中4版のhelper・4失敗票・全5 log/exitを含め欠品0、bytes/SHA差0。最終票の外部入力19件も全実pinが一致した。旧失敗票を最終PASSへ上書きしていない。

F2. 比較述語の実効性 — STATIC PASS

helper L14–57の `Same` はnull、arrayの型と要素数、stringの型と大文字小文字、ValueTypeの実型と値、PSCustomObjectの全key集合と各値を分岐する。したがってbool/整数/decimal、array/scalar、null/空objectを同値扱いしない。`Fields` のkey列挙修理後もexact key集合を保持する。実 `producer_resource_or_failure_diagnostics` はPSCustomObjectで0字段であり、正常な空objectとして照合される。
`PlainInt` はint/long、`Finite` は非負の有限double/decimalと普通整数を許す。実archive.elapsed_secondsはPS5.1でSystem.Decimal、region countsはSystem.Int32、run/artifactの大きいIDはSystem.Int64だった。型の受理範囲と実票は整合する。
`Pin` のexact三字段、普通整数bytes、SHA字面、safe相対名、包含、非reparse、regular file、全file SHAとtyped pin比較を追った。`FileMap` はOrdinal名辞書と重複拒否を用い、配列を名だけに縮めず各descriptor全体へ戻る。`RangePin` は普通整数のLF範囲・全bytes・全SHAを実byte境界へ結ぶ。固定全file pinで認証済みのJSONを読む射程を保持し、inner sealを再生成したとは主張しない。

F3. 実failureと全診断envelope — STATIC / SAVED METADATA PASS

run `34040070261/1`、head `4290ed7c947a9dacdb132209f247f18ef8dae6d9`、workflow ID `351613185`、job `101505092062`、artifact `9991438160` を保存API・取得票・実launchへ結ぶL71–97を読了した。初期runs APIのin_progressと、後着jobs APIのcompleted/failureを区別している。実ZIPは7,379,999 B / `22f8f60157e96f31d159f558abe55b9aa922d3b81000f2d16f9c2454189194ea`。
ZIP readerは全entry名/重複/既知名集合と実展開pinを結び、各streamを末尾まで読み、Length・全SHA・最後のEOFを比較する。抽出先へ書かず、CRCの独自再計算を主張しない。当便ではこの経路と1066保存結果を静読し、ZIP全file SHAと実展開252 files / 14 dirs / 33,742,914 Bの全file SHAを別に再照合した。原受領器・ZIP entry readerを再走していない。
保存before/afterの全inventoryは一致し、今回の実treeも両方の全pinと一致した。runの250 files / 14 dirs / 33,691,608 Bは、自己除外されたinventory 35,918 Bとrun receipt 15,388 Bを足すと実252件に一致する。空dir/hiddenを名集合から黙って除外していない。L209–211は前段失敗時にも最終tree再読を試み、6件未完またはerrorありをPASSにしない。

F4. 実source・継承・全EOF — STATIC / OPAQUE RAW PASS

source24（Python21/raw3）、history6、driver 529,340 B、active WF 20,296 B、旧WF archive 599,085 B、両registry、source/audit before-afterを全実pinと保存receiptへ結ぶL117–157を追った。history6は非実行証拠、現P4/C4は当該失敗runのcheckout copyであり、未公開の1064/1065修理を混入していない。
当便のopaque再照合では8 sourceの全pin/LFと全547 spanが一致した。内訳は現遷移471 span、歴史60 span、旧8 loaderの両側16 span。P37も両側の全byte区間が一致し、共有kernel4は全file pinと登録raw区間SHAが一致した。本文をdecodeした数学監査ではない。

| 遷移 | baseline / current区間 | 全分類 | raw不変 / 変更 / 追加 / 削除 |
| --- | ---: | ---: | --- |
| P3→P4 | 122 / 136 | 136 | 104 / 18 / 14 / 0 |
| C3→C4 | 96 / 117 | 117 | 79 / 17 / 21 / 0 |

全253分類の5字段を実型付きでregistry・GHA継承票・1066最終票の間で比較した。全ordinalは範囲内で一度ずつ現れ、4区間列は先頭からEOFまでgap/overlapなし。exact-raw分類はSHA/bytes一致、changedは別SHA、added/removedは対応側nullを要求する。
旧root partition票は `DRAFT_PENDING_SOURCE_PINS` の235,897 B / `e0cbaf0a4aae7f0812c29b2bfcf423852de061cb2e0225cb3f48792e4d1df34e` を指す。実最終registryは235,914 B / `36ae3dc38419bcb711499b4f0216f1d9997d10fb6d23ff96cc8e79a48efc1867`。この2 pinを同一扱いせず、全8 source pin、全raw、全分類count・変更scopeを別に照合する接続である。旧8 loaderの文脈記録も保存値として全joinし、CURRENT_RUN call coverageのNOT_MEASUREDと第三独立性falseを維持する。

F5. shell9・元path・16親・36記録 — STATIC / SAVED METADATA PASS

L158–178は実5 SHA行からcheckoutとREPORTを読み、実WF/ref/head・driver/archiveの固定pathと全literalへ結ぶ。before/afterのSHA5行、placementの全原文、exitの実0 LF、stdout順序、空stderrを照合し、架空のexecution argvに依存しない。9原票と全24 source capture/6 history captureへの接続を確認した。
L179–208はlive16の実artifact/run API、全role集合、expiry、実root/archive、取得直後の全保存inventory、after inventory、全16保全flagを結ぶ。保存親総bytesは3,824,247,024であり、別hostの親payloadを当便で全再hashしたとの主張ではない。旧64の保存22 receiptも対応するcontinuation全inventoryのpinへ戻る。
当便でも旧batch全11,437 fileの実保存entry票と新transport before/afterをOrdinal名辞書で比較し、名・普通整数bytes・全SHAが全件一致した。3439→3475のdir集合は元集合を包含し、追加は計画36名に正確に一致する。全36 journalのexact6字段、ordinal、相対/絶対path、mkdir_return=null、即時存在/regular=trueを実保存JSONとtyped比較した。
旧ローカルrootの同36名は今回も存在0件。これは別hostの観測であり、今回GHAの3475保存inventory・作成journalと混ぜない。受領rootへmkdirせず、local restoration/physical-directory validation/completed acceptanceをいずれもfalseのまま保持した。

F6. 4停止修理の全差分 — 必須追加修理なし

| 保存停止 | 原因と限定修理 | 維持する比較 |
| --- | --- | --- |
| 01、checks=2 | 空objectのProperties.Name列挙を明示列挙へ変更 | exact空key集合と全typed再帰 |
| 02、checks=3 | GHAのbaseline/current_regions整数をregistry配列のCountへ接続 | 全471実区間と全253分類を別途照合 |
| 03、checks=5 | ZIP entry順とPOSIX inventory順の相違をOrdinal名辞書へ接続 | unique全11,437名と全descriptor bytes/SHA |
| 04、checks=5 | 別hostの旧ローカル空dir存在必須を実Exists観測へ変更 | GHAの全3475dir・36 journal・前後不変を保持 |

4旧失敗票のstatusはNEEDS_ROOT_REVIEWのまま。各log/実reason/該当helper差分を全読し、最後のPASSへ旧エラーを隠していないと裁定する。これは数学gateの修理・陰性結果の格上げではない。

F7. 実停止と最終6件の意味

実driverはintakeでbatch-parent/output/fixed/basis.jsonのFileNotFoundErrorを記録した。run-receipt/preservationはFAIL、5 executionは全部null、13指定結果字段も明示null、producer診断は空object。fixture2件はUNFORMED、比較とarchiveはINCOMPLETE、preservationのmissing4とfixture由来error1を保持する。保存stepのexit0から全保全PASSや本P/C実行を推論していない。
最終6件は `actual-api-and-entire-diagnostic-zip`、`typed-early-failure-and-incomplete-preservation`、`all-source-and-opaque-inheritance-bindings`、`nine-shell-receipts-and-original-paths`、`sixteen-live-parents-and-36-restoration-records`、`second-full-diagnostic-tree-readback`。全部PASS_METADATA_ONLY、最終error=null、status=PASS_METADATA_EARLY_FAILURE_ENVELOPEを確認した。
最終process票はsession60448/chunk2ec0f1の保存観測としてexit0を記録し、helper/最終票/logの全pinを結ぶ。1 Bのexit captureは実0Aだけであり、明示文字「0」ではない。成功時はPSスクリプトがfall-throughしLASTEXITCODEがnullだったという区別を保持する。当便はこの保存観測と実fileを照合したのであり、process成功を再実行で再現したのではない。
数学実行、DEPENDENT実枝、new oracle、completed candidate、CV9、grade2、full A0、cross_checked、verifiedを本票から昇格させない。1064/1065の具体修理案は本監査と別である。

F8. 新保存物と凍結

新TEMPは `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1068/`。全8資料の出力indexは2574 B / `3d9ab24475e12ebd6f8caf33e61bdcf4617e2bc0c56200b2ca61c5543ab8d0ee`。index自身と本返信は循環pinから除外した。
主要新票は `receipt-and-input-pin-review-v1.json` 103940 B / `fe836df2a72eb38ac3e5eb669bd33f117c7bedc47dc465d4049b7bc5c8805a2f`、`opaque-region-review-v1.json` 9620 B / `afcf9993f2753a381e811b2ec9218051ccad8fae8a5c8ac2dfdc81a0ebf5ea77`、`typed-receipt-review-v1.json` 12912 B / `84b1961bd288e36c1767aa1c0532189394b069c7c1c593f014cfd3a1b4f52479`。helper snapshotと全4差分も同indexに固定した。
当便の直接metadata集計では保存前に2度停止した（OrderedDictionaryへのMeasure-Object適用、同値JSON objectの字段順の比較）。それぞれ整数集計と全字段の型付き比較へ直し、原因を新票に明記した。原受領器を実行・改変したエラーではなく、入力変更もなかった。最終3新票は実metadata全一致の結果で、未完の集計をPASS扱いしていない。

AUDIT_1068_VERDICT: LIMITED_STATIC_METADATA_PASS
