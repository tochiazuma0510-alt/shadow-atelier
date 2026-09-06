# Task1039 — PS5.1 資源metadata受領器の限定修理

## F1. 完成範囲と読了資料

新 `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata-v2.ps1` を完成し、全文1107行と旧版からの全差分を静読した。新helper本体は未実行である。変更はこのTEMP helperと本返信の二fileだけで、旧1033 helper・旧受領票・旧返信・正語P4・Task1036の新P v3を変更していない。

指示書1039を全文読了した実pinは3346 B / `10801812d6f81f2a5c224a9a8d657395c6f83582cffa5ee90303a7188deb01bd`。公開1022（24414 B / `515bf6dd39a91c180169dfceac79825b909e9433d2e43771863b5ef5a54c276f`）と公開1024（3396 B / `6abc0b1900fbc41e3a6f6ad386b5c5fe231249680efefbc341d473e179fd3875`）も全文を読み、小数・ordinary整数・sample・完了sessionの既存契約に接続した。D私的source・返信・実装helperは読んでいない。

## F2. 実失敗と原因の区別

rootの旧受領票 `positive-v5-run34009883488-root-resource-metadata-v1.json` は95109 B / `840fa57a1dda3e2a3622a7c4401ef025941e3524ec884b709e0fcc5ddd8689d5`。保存statusは `FAIL_RESOURCE_METADATA`、errors11 / incomplete2である。10件の `json_scalar_type` は三execution、P fixture三session、P main、D fixture、D selftest top、公開八type票の入口にあり、残る1件はresource inventoryの件数拒否だった。

当地のPowerShellは `5.1.19041.6456`。実 `executions/P-receipt.json` の `wall_seconds=5402.03076` は **System.Decimal**、`exit_code=3` はSystem.Int32、candidateはSystem.Booleanだった。既存 `Finite` がDecimalをJSON scalarとして受けず、`Float` もDoubleだけに限定していた。一般parserの不正や数学の失敗を同定したものではない。

実本Pの `P-stdout.json` は514 B / `664edc84e7fdaa94d87ed237052dce19694739122f5e189e66b1268ecd43d7e9`。保存値は `UNKNOWN_RESOURCE`、phase `literal-DFS`、reason `ResourceStop:literal-DFS:deadline`、内elapsed 5400.275689秒、外wall 5402.03076秒、exit3である。`successful_bundle=false`、grade2 member/nonmemberはともに `NOT_DECIDED`。これは実資源停止として残す。D本番と最終run receiptは未形成であり、受領器のDecimal修理によって正語完成へ格上げしない。

`preservation-result.json` は2669 B / `b98ebfcbfbb2288500176c16f23420eaf87a28942cd9428cbbcae3c89ae90249`、status `INCOMPLETE`。四つの保存問題は `word-before-D` 欠損、`word-unchanged-by-D` 不成立、`output-D` 未形成、`report-before-D.json` 欠損である。実字段 `all_sixteen_parents_unchanged` / `acquired_sources_unchanged` / `source_raw_acceptance_driver_unchanged` はtrue。これは保存票のmetadataとして読んだもので、本helperが16親body全体や最終envelopeを独立に再受理したという意味ではない。

## F3. 小数型だけの修理と保持した拒否

| 入口 | v2の受理型と境界 |
|---|---|
| `Int` | System.Int32 / System.Int64だけ。指定下限を維持し、Decimal・Double・bool・文字列から変換しない。 |
| `Float` | 有限なSystem.Double / System.Decimalだけ。既存の下限を維持する。整数をfloatへ自動的に分類しない。 |
| `NumberOrNull` | null、又は有限非負のDouble / Decimal / Int32 / Int64。これは既公開のnullable number専用である。 |
| `Finite` | object/listを従来どおり辿り、Decimalを有限小数として追加する。string / bool / Int32 / Int64の既存scalar型を維持する。 |
| `Bool` / `Flag` | System.Booleanだけで不変。数値0/1をboolにしない。 |

旧 `Int` 本文にはuint32 / uint64も列挙されていた。指示1039の「int/longだけ」を新helperで明示し、この余分な二型許可を除いた。旧版が既にint/longだけだったとは記録しない。今回読んだPS5.1 JSONのordinary整数はInt32/Int64である。

Doubleへのcastは `IsNaN` / `IsInfinity` の有限性判定の局所引数だけに置き、入力objectの値や型を代入し直さない。`Same`、元ASCII JSONから一つのseal tokenを除くhash照合、JSON EOF / LF / CR / 型別字段gateは変更していない。新JSON parserや一般canonicalizerは作っていない。

全Float呼出しをsource検索で点検した。対象はP/D sample elapsed、P process_max_seconds、D deadline_seconds、execution started_monotonic / wall_seconds、保存済み八type対照の等値floatである。Dmeasurementのnullable数値は `NumberOrNull` に接続する。ordinary budget・cache・sample番号・counter・index幅・exit codeは従来のInt系を通るため、例えば128.0が値だけ128に等しくてもordinary整数には入らない。

小さなJSON型観測のみ当地で行った。`{"integer":128,"wide":34009883488,"floating":128.0,"flag":true}` は順にInt32 / Int64 / Decimal / Booleanだった。これは組込み `ConvertFrom-Json` の受領型を見た操作で、新helper関数の呼出し、新selftest、数学の実行ではない。新helperの実受領成功をこの観測から宣言しない。

## F4. inventory差分の実特定

実Rootは `C:/Users/81905/AppData/Local/Temp/shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1`。`resource-output-inventories.json` 全file pinは19888 B / `24bc7c54842e86061063ddf0650ce0afee3e10e45f80dc8b8896889bedd2a72e`。保存宣言と実filesystemを、file名・directory名の全相対集合で比較した。

| root | 宣言files / 実files | 宣言dirs / 実dirs | 差分 |
|---|---:|---:|---|
| P_SELFTEST scratch | 29 / 29 | 9 / 9 | 全集合一致 |
| D_SELFTEST scratch | 86 / 86 | 6 / 6 | 全集合一致 |
| 本P resource-P | 4 / 4 | 2 / 1 | `index-receipts` 一個だけ不足 |
| 本D resource-D | NOT_CREATED / 未形成 | inventory=null | 空の完成sessionを補わない |

OBSERVED三rootにmissing file、extra file、extra directoryはなかった。本Pの宣言directoriesは `index-receipts` / `indices`。前者の配下には宣言fileも宣言subdirectoryもない。後者の実fileは `indices/000000-build.bin` 一件である。

本Pの保存 `result.json` は948 B / `019be608da5215d4b1d1604f8aa2f2dda9048db168f21b7a0fe6218db320c8ed`、status UNKNOWN_RESOURCE、samples2343、完了 `indices=[]`。`index_states` はnumber0 / purpose build / rows=durable_rows=8777434 / actual_bytes=logical_bytes=368652276 / closed=true / finished=false の一件だった。完了index receiptが一件も形成されていないことと、空だったreceipt directoryの欠落は整合する。未完のindexを完了品と呼ばない。

rootの全entry票（69746 B / `2094e4f4275468694328de30faf91f47a25fb2b8dfb2842bba0a5368a75fe275`）も読んだ。406 entries、`explicit_directory_entries=0`、ZIP SHAは `41c95c7171c9192ec1d589a715c911f7470bb69fe520b80558334ad60636ac61`。resource-P配下の四fileは宣言の全四descriptorと一致し、index-receipts entryはなかった。全entry票は `crc_independently_checked=false` としているので、CRCの独立照合を付加して主張しない。

rootが全ZIP1373772131 Bと全展開406 files / 96 dirs / 3685457381 Bを照合した事実は指示1039と実全entry票を来歴にする。当便で独立に再hashしたのは新旧helper・公開資料・旧受領票・上記小metadata等であり、3.7 GB全bodyを再走したとは記録しない。実全file名集合の比較、四resource-P entryの保存descriptor比較、実小metadata hashと、rootが完了した全body hashを区別した。

この差分は、保存元に宣言された空directoryがdirectory entryを持たないouter ZIPで輸送されなかったケースとしてrootへ送り、rootはINCOMPLETE分類を受理した。取得Rootへのmkdir・file修理・削除は行っていない。

## F5. 新inventory受領規則

新 `InventoryMatch` は先に全descriptor型・相対path・重複・file/directory衝突を確認し、宣言と実集合のmissing / extraを各々保存する。全fileのEOFを保持し、file不足・余分なfile、余分なdirectory、宣言上子を持つdirectoryの不足は構造FAILとする。各宣言fileの全bytes / SHA256照合も従来の `FD` へ戻して行う。

不足directoryについては、宣言fileと宣言subdirectory双方にそのprefixを持つ子がない場合だけ「宣言された空directory」に分ける。全file descriptorが一致した後も、そのdirectoryの不在を `INCOMPLETE_DECLARED_EMPTY_DIRECTORIES_MISSING` として記帳し、`incomplete` へ `DECLARED_EMPTY_DIRECTORIES_MISSING:<相対名>` を加える。一致へ丸めたり、元宣言を変更したりしない。

`archive_cause='NOT_ADJUDICATED_BY_THIS_HELPER'` を各比較に保存する。このhelperは展開Rootだけを受け、外部全ZIP/entry票を自動読込しないため、外側輸送原因の証明をローカルな空dir分類へ混ぜない。F4の原因判断は別の実entry票とrootの受領に基づく。

全比較が閉じれば比較statusは `MATCHED`、宣言空dirのみ欠ければ前述INCOMPLETEとなる。比較row形成後の集合/hash拒否では `FAIL_UNLESS_ALL_CHECKS_COMPLETE` が残り、形成前の型/重複等の拒否はerrorsへ記録される。top-levelは従来どおりerrors優先でFAIL/exit1、その次にincompleteがあればINCOMPLETE/exit3、双方0だけPASS/exit0となる。本PのUNKNOWN_RESOURCEや本D未形成も引き続き独立のincomplete事由になる。新実受領の具体的error/incomplete件数は未観測である。

## F6. 旧版からの全差分と公開receipt

全文字列の行差分は13hunksで、意味上の変更は次の範囲だけだった。新helper全文を1–300、301–590、591–880、881–1107行に分けて読み、切詰めのない出力で静読した。

1. 5行のTask1039/v2注記、13行のinventory比較list追加。
2. 51–85行内のInt / Float / NumberOrNull / Finiteの四つの型判定。
3. 901–952行の `InventoryMatch`。呼出し元のResourceInventoriesとPublicTypeCanaryは同じままで、保存declared bodyも維持する。
4. 1069行の出力schemaを `d972.r07.positive-v5-resource-metadata-reception.v2` にし、1079–1081行に下記三字段を加えた。

新top-level字段は `resource_inventory_comparisons` / `previous_helper` / `numeric_representation_policy`。それ以外のtop-level字段、CLI、session/source/owner/runtime結合、PとDの公開型、未知D keysetの扱い、path gate、全regular file stream hash、外部新receiptへのCreateNew、assurance falseは旧版のままである。

`resource_inventory_comparisons` はlist。各要素のexact15字段は `prefix status declared_file_count actual_file_count declared_directory_count actual_directory_count missing_files extra_files missing_directories extra_directories missing_declared_empty_directories missing_declared_nonempty_directories all_declared_file_descriptors_matched archive_cause input_tree_written`。六つのmissing/extra字段はprefix内相対strの配列、四countは件数、descriptor一致とinput書込はbool。実不足と期待件数の両方を残し、空配列を欠測に置き換えない。

`previous_helper` はexact `{file,bytes,sha256}` で旧78114 B / `654ba851e96060401ebc231145aa112945e452b27b738595d866d8fdae98f85e` を指す。`numeric_representation_policy` はexact `{ordinary_integer,floating,nullable_number,boolean,input_values_rewritten}` で、前四項はsourceに記載した型規則の文字列、最後はfalseである。

Dの未公開追加keysetは引き続き `NOT_ADJUDICATED`。公開WF5/1022/1024が型を規定する字段を照合し、未公開追加は元JSON全file pinとbodyとして残す。Dの負対照catalogを本Dの完成certificateへ取り込まない。`candidate/cross_checked/verified/math_replay` は全てfalse、`whole_envelope_or_final_preservation_adjudicated` もfalseである。

## F7. root実受領へ渡すCLIと未実行境界

引数は `-Root <完成展開Root>` と `-ReceiptPath <Root外の未存在JSON>`。変更していない。rootが新helper全文・全差分を静読した後、旧v1受領票とは別pathで実行する。

```powershell
powershell.exe -NoProfile -File "$env:TEMP/shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata-v2.ps1" -Root "$env:TEMP/shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1" -ReceiptPath "$env:TEMP/shadow-atelier-audit163/positive-v5-run34009883488-root-resource-metadata-v2.json"
```

これは再現用の未実行コマンドである。当便で新helperを起動・dot-sourceしていない。Python、import、AST、GAP、数学、GHA、network、git、credential操作、追加agent、旧数値suiteも実行していない。局所metadata操作は既存JSONの読取・実.NET型観測・相対集合比較・source文字列差分・bytes/hashに限った。

## F8. 最終freeze

新helperは **81620 B / `51fad0e611715799bf9f78dd11b4c302e642da3f2657df43b166e09c6cffbaea` / 1107 LF**、ASCII / CR0 / BOMなし / 最終LF一個である。本文・全差分の静読を閉じ、このpinでfreezeする。新受領器の本体実行と新受領票はrootの後続作業として未観測である。

旧helperは78114 B / `654ba851e96060401ebc231145aa112945e452b27b738595d866d8fdae98f85e`、旧返信1033は14242 B / `9174730159e71e2e6b3f09402eac64dafcd929b3175e5140302053c57f12cab0`、旧失敗受領票はF2のpinで不変を再確認した。Task1036のP v3も209926 B / `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8`、返信1036も18903 B / `2e052e034ac22aa5108f9b02f935f3162a7a92e8c30450ba77a8e9e09d2f9881` のままである。

AUDIT_1039_VERDICT: RECEIVER_V2_COMPLETE_STATIC_ONLY_ROOT_EXECUTION_PENDING
