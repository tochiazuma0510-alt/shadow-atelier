# Task1127 — C6 公開修理の v6 binding（正式受領前）

F0. 指定1127を全文読了し、root採択 C1125 の opaque pin/公開165区間を current registry→driver→WF へ結んだ。作者静的判断であり、自案の独立監査・通常親入場・数学の再証明ではない。最終は `%TEMP%/shadow-atelier-audit163/task1127/review-snapshot-v2/`、旧1108と途中v1は保持した。

F1. 最終rawは次の3本。全CR0/ASCII/BOMなし/finalLF/末尾空白0。WF 30603 < 500000 を実bytesで照合した。

| file | bytes | SHA256 | LF |
|---|---:|---|---:|
| driver.py | 2277771 | 4904cb5c610ada765e52f6e96c3d1cbef38eaf303c7b485082a495e79c3ffd97 | 10918 |
| workflow.yml | 30603 | 59ddc40a18f1d02b142c229c0f21a69aebdb32b0451a873338dc2f06b2189b9b | 461 |
| audit-region-registry.json | 867287 | 8932a92a640b7389bf507b7294b017e9aec8df2b053c6ffaca4467cb4ab64ae1 | 1 |

F2. 旧C419541/3996972c…から新C427740/a5c449721663940ed2155f90980eb7422999cbaa6af466512e95a0819cd02f58へ、公開165区間の全offset/length/LF/SHAを結んだ。3変更はPREAMBLE・third_batch_parent_admission_canary・selftest、162区間のraw保持はroot採択の公開範囲票に依存する。私的本文/範囲bytesは読まず、C全sourceはopaque全hashのみ再照合した。保持24登録（旧4loader＋20body、21固有raw）のcurrent座標を更新し、元classification/比較順/baseline/文脈は保持。Pと3歴史registryも保持した。

F3. 全差分 `all-public-binding-raw-delta-v2.json` =2336671/d8f92ac36be1b583a60ae83bb55ca1e2895011ddb41365793d6e1d1ca1c8753e。registry23成分（source・165区間配列・保持21固有位置）、driver4成分、WF4行を全順逆raw復元した。元1108の全3rawへ一致。driverはCURRENT_EXECUTABLE_PINS、INHERITANCE_REGISTRY_RAW/PIN、PARENT_TIMING_CONTRACTSのC descriptorだけ。WFはC/driverのbytes・SHAだけで、既名/marker、18親、caps/330分、k128/maxbatch1/no-refill、全起動/保存/停止制御を保持した。

F4. 追加consumerは `parent_timing_contract` L10646–10649の実source等値。途中v1はC計器のpublic_contract.sourceが旧pinのままだったため未採択として保持し、v2で現code_contract().checkerとの実等値を閉じた。元declaration=11356/78f63f389762c12c7ba9ca5d6e9164c4d78cedf3c08705aa18d5d7074bf2638e、root_adoption=581036/fc3150cf742a0fec2c0a79e19e43b5968f4d7052dfdb6c9f22856b4a35bad652は歴史証拠のpinであり変更しない。C source descriptor以外の計器全objectが旧版と型付き等値、C10字段/31完了順・時計/呼出本文は保持。新時間標本や因果推論を追加しない。

F5. `full-EOF-and-metadata-consumers-v2.json` =234638/0bbbf6c7981c77f6ca32c9bad244dbc089785466055fe4dd40d3e4ab22126877。全131区間のEOF再構成と順序を閉じ、129区間raw同一、変更2区間はmodule-prefixと後続top-level計器定数を含むdef final_modeの字句区間。4定数成分を除く実行文は全raw保持。4globalの全16出現行（4宣言/12実reader）をcode_contract/public_audit_registry/audit_material_bindings/audit_mode/parent_timing_contractへ分類し、巨大JSONのliteralを実readerと混同しない。元1108の全consumer意味監査を継承し、今回の依存globalだけを追加追跡した。

F6. selftestのartifact_identityはtopのproduction_interfaces_usedに加わるinterface名であり、新top-level字段ではない。公開top11/群3key/5群順・[28,9,6,7,8]・全43interfaceを既test_gateの非空文字列list契約へ結んだ。exact-listへ変更せず、第五28files/8目的label/empty1も保持。作者metadata集計の途中PowerShellのpath/collection形修正は別版scriptへ保存し、C/helper実行結果と区別した。

F7. `final-binding-location-plan-v2.json` =26749/521e8ce88e4eaa8151f0010706c81b6ca669f2ef53515961c57e78eb73e3e0fd。旧13位置を新rawから再計測し、第14 `PARENT_TIMING_CONTRACTS` L10596/offset2247025/bytes9938を追加。正式inventory5・typed receipt・認証済missing-directory名は未着、3 None/ready falseとregistry末尾nullを保持。正式P→C→current registry→driver（P/C両計器sourceも再結合）→WFの依存順で、元declaration/root_adoptionを現sourceと混同しない。typed receiptの未提供inner exact shapeや未来rankを作らず、静的採択を新gateへ巻き戻さない。

F8. `final-author-static-proof-v1.json` =18180/8f03482adf24e65e9b9258f4796c03966691076567d0727ad416467898469f3e。全3順逆raw・9保護入力不変・P/C計器source等値・format/gateを実metadata照合。最終目録 `final-material-manifest-v1.json` =7801/a0c3764b7fc7fc177756064f5e4fb2f885bea11611b448fb77b5b8efbded08e2、全21材料11610430 B（自己と本返信は除外）、うち最終資料8本、途中稿/scriptは役割別記帳。新TEMPと指定返信以外の変更0、source/Python/GAP/AST/import/compile/数学/新GHA/Git/network/credential/親scan/process操作0。

F9. root報告として1126 run34220805430/1/head4e68cf23fe471623a67bcd7892a713978e7f1bc2のC exit0、Python3.12.3/NumPy2.5.1、5群PASS、outer/inner全ZIP受領採択を受けた。本作者のローカル実測でも通常18親/本走/正式inventoryの代用でもない。v2を凍結し、正式handback到着後の限定bindingを優先できる状態で引き渡す。

TASK1127_VERDICT: LIMITED_AUTHOR_STATIC_PUBLIC_BINDING_PASS_FORMAL_HANDBACK_PENDING
