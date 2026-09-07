# Task1085 — P5 正式 inventory consumer の三 literal 修理

F1. Task1085 全文を読了し、指定 P5 の三 literal だけを修理した。新 immutable source は TEMP/shadow-atelier-audit163/task1085/d972_r07_fixed_lambda_cycle_batch_v5.py = 366659 B / 6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d。LF 5536 / CR 0 / ASCII のみ / BOM なし / final LF あり / 行末空白 0。旧版から +15 B、行の増減 0、変更行は 2084 / 2086 / 2089 のみである。source を凍結し、実行はしていない。repo の同名 P5、旧 source、C、WF、registry、既存親、公開済み返信は変更していない。

F2. 実停止の三根拠を metadata として全 bytes / SHA に結び直した。実 run34143415388/1、head2751f8942a50377a13078cbf646cfaaa3845b71f は P exit1、phase=batch_checkpoint_metadata、reason=ValueError:fixed_lambda_batch:next_batch_registered_inventory_exact_fields。stderr は通常 run_actual → authenticate_acceptance → authenticate_next_batch_parent → L2084 exact_keys の経路を記録している。新 lambda1706 の selection / 処理は未観測、本 C は未開始という task の境界を保持する。

| 実診断 root 内 file | bytes | SHA256 |
| --- | ---: | --- |
| producer-stdout.json | 2757 | abb788bdb1b3dab7adef7e21978697f9b5ee67a3a8b7ffe9cde2dc6c924ed6ad |
| producer-stderr.log | 10051 | 8b4cbeae6a3b21ee38194368989472a5f39bb95b93026410587ddf245b4d028d |
| execution/producer-result.json | 6489 | aa84078afbd8a097013223e4f921239d348885a74af70ff132d79ac0b9d1aca1 |

実診断 root は TEMP/shadow-atelier-fixed-lambda-batch-v5-run34143415388-diagnostics-a1。これは保存結果の metadata 読取であり、P/C 数学を再演した記録ではない。

F3. 正式 source constant は files / file_bytes / directories / files_sha256 / directories_sha256 の exact5key であり、root 正式登録票 7022 B / 64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753 と全字段・実値が一致した。実値は files=11648、file_bytes=1308094050、directories=3525、files_sha256=ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5、directories_sha256=f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64。consumer の registered はこの source constant、inv は全実 parent scan の観測目録である。

| 変更行 | 変更した登録側の用途 | 変更 |
| --- | --- | --- |
| 2084 | exact5key の集合 | bytes → file_bytes |
| 2086 | 正の ordinary integer を要求する三字段 | bytes → file_bytes |
| 2089 | 各 file の bytes 合計と比較する登録値 | registered["bytes"] → registered["file_bytes"] |

2089 の各 file descriptor に対する x["bytes"] はそのまま残した。whole file count / 合計 bytes / directory count / canonical files SHA / canonical directories SHA の全比較を保持し、旧誤 bytes 形との両用を認めない。dict 型、exact key 集合、ordinary integer、SHA 型の gate は緩めていない。constant、正式目録、accepted8key、parents 各要素の共通5keyを変更せず、別の registration record を acceptance に足していない。root 通知の2214では、工房も source 確認後に2213補記の別 record 不足という帰属を撤回した。本便は root の正式五keyを読む consumer の修理である。三 literal 以外の旧コメントを含む source raw は保持した。

F4. consumer 全本文と、L2486–2493 の authenticate_next_batch_parent、L2761–2792 の通常 admission を静読した。17 親ごとに typed expected inventory を読み、実 root を全走査し、名前・bytes・SHA・directory EOF が一致してから by_role に保持する。original64 と v3 の受付後、batch-parent-v4 の実 inv が当 consumer に渡る。consumer は登録定数から exact5key と型を取り、全実目録の count / 全量 bytes / 全 hash を接続する。この経路を飛ばす枝や補完値は足していない。

現四群 selftest は当実 bound consumer を通していなかった。registration 群の authenticate_acceptance 対照は旧 schema を目的 label で拒否する入口対照で、全実17親の正例ではない。第四群も old16 projection / 世代付き source / 225+128 ancestry / theta0 / previous target / plain対packed SHA / fixed参照の各 helper を試すが、next_batch_inventory_registration を呼ばない。production_interfaces_used に広い authenticate_acceptance の名があることを、当 consumer の実正例到達と解釈しない。この見落としを記帳し、以前の自己試験 PASS を実入場成功へ昇格させない。

新 test 群 / CLI / 数値実装 / 合成 fixture は追加していない。四群の source 全 raw と P[30,10,6,7] を保持した。群名は k128-version-registration-and-types、k128-full-roster-cutoff-and-restoration、batch-parent1578-admission-and-projection、batch-parent1706-two-layer-admission の同じ順である。修理後の意味ある実確認は、root が別に承認・起動する通常 GHA 一回で全実17親の通常入場を通すことである。本便ではその実結果を先取りしない。

F5. 旧全 raw を task1085/producer-v5-before-inventory-key-repair.py = 366644 B / 664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66 として新 immutable file に保存した。Git 履歴だけを旧 run の現物保持の代用にしない。repo 同名へ配置する前の ops/source_versions 新 archive の具体名と配置は root が担当する。この task の archive 候補は旧 repo と全 bytes が一致し、作者自己点検時にも repo 側は旧 pin のままだった。

三 token の最小 raw offset は旧121737 / 121928 / 122283、新121737 / 121933 / 122293。各 token は 7 B の "bytes" から 12 B の "file_bytes" へ変わる。前後4つの不変 span と三 token から全新 366659 B を再構成し、逆方向でも全旧 366644 B を再構成して完全一致を閉じた。全行比較でも三行以外の相違は 0 だった。

全 EOF 区間は 156 → 156、raw不変155 / 変更1 / 追加0 / 削除0。全旧区間を実旧 bytes へ、全新区間を実新 bytes へ SHA で照合し、欠落・重複なし、前後再構成一致を閉じた。変更区間 next_batch_inventory_registration の開始は121495のまま、旧1090 B / 34b3f78dafc7252fc04bfa627d8931090fd6b019cdfd4fc5718c6204592114fe、新1105 B / 270092a3aba2d65e903ed4363e33628b1d9e5a543d9cfcca7684d2b6cc8fef2e。それより後の区間は +15 B の offset 移動で本文は同一、行番号は動かない。

F6. P37 保持本文は、基準 P4 290457 B / a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a、修理前 P5、修理後 P5 の三者で全37範囲の bytes / SHA が一致した。旧8 loader の P 側4範囲も保持した。新 current 範囲は下表である。

| P 側旧 loader | 新 offset | bytes | SHA256 |
| --- | ---: | ---: | --- |
| authenticate_anchor_metadata | 69476 | 6289 | 2d45494a3dbc6064b2ea08f39fba6e5288ba539e36eeeef893b427d0efca0b55 |
| accepted_oracle_top_metadata | 178122 | 1920 | 47077c84812c4caf7cb782e12a43c4ee0e61126111e84fdf4b57e7339b96f610 |
| parent_row_sources | 180042 | 2180 | 683367b46c3ffd5b586204e95562190fe42146a0542f8bacb3406125a616e4fa |
| thin_anchor | 182222 | 5144 | 2b2e5b425efdb999c47339888caad3c76313dcb83baaeefb9ff332b1f2aaf571 |

run_candidates の継承範囲は元登録の2487 B本文、新 offset295624 / SHA256 9dc6a9d161c631dbebdaebc48399a1960e87dca45b0fd020b10973e9c9f33438 であり、これをより広い def-to-next-def 範囲と同じ scope と呼ばない。数学 body 変更0、親17役、old64 + v3/128 + v4/128、最大128 / no-refill / 単一 batch、既存 caps、lambda1706、TCB、全保存契約、selftest / CLI の変更0。C 私的本文は読んでいない。

F7. 全納品は T=TEMP/shadow-atelier-audit163/task1085 に固定した。公開 handoff は source pin / metadata ABI / 全 current range / 37bodyと旧4loaderの offset・SHA のみで、私的算術本文や全 diff 本文を埋め込んでいない。WF1086作者と root へ公開版を配達した。

| 納品 file | bytes | SHA256 |
| --- | ---: | --- |
| d972_r07_fixed_lambda_cycle_batch_v5.py | 366659 | 6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d |
| producer-v5-before-inventory-key-repair.py | 366644 | 664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66 |
| producer-all-three-literal-changes-v1.diff | 899 | 57c67c9023fe809a358d2364fc36e83507d7afd550ce70e65d3df45e96b878cb |
| producer-all-raw-byte-delta-v1.json | 8127 | b5139e5a5dcd77afa3604eb0845cefb65393713131fd181f6abd2501fa097b98 |
| all-current-raw-regions-v1.json | 242861 | 03fc6152d0298b22a0a25c690d17279637054cdb14a633fa70c362b6172a4485 |
| producer-body-inheritance-v1.json | 67019 | 9a3ac71c0b99602b62d94610365bc30d216428f5d71a74c671d10c158981484f |
| public-producer-source-and-ranges-v1.json | 226557 | 261c0c6b39d8a600f041c0341181f78268db272efdb887430c7c144c058d34a6 |
| author-static-review-v1.json | 6701 | 52b3b3fee01c3b8a1e71e633829587d2cca2566dbda86b1076408dadd99d72db |
| final-material-manifest-v1.json | 3050 | 47da96a723b357e85f31db549b62fa33c8b6c9e565a55ac52039937a5729f00e |

最終目録の8 fileは目録自身と本返信を除く定義で、旧全 raw archive 候補を含む。全 diff / 区間の作者自己点検は root の独立全差分監査の代用ではない。root から三行だけ・descriptor bytes保持・consumer全本文/通常caller読了との独立速報を受領したが、root全区間再hash/配置/notify-and-go/次実GHAは root の仕事として分ける。

F8. 本便の実行は raw text / bytes / SHA / typed JSON の metadata 操作だけ。Python / GAP / import / AST / compile / source / 自己試験 / 数学実行は 0、network / Git / GHA / credentials / 新 agent も 0。source と全材料をこの pin で凍結する。修理の新 runtime 結果は未観測、candidate=false / cross_checked=false / verified=false。静的には正式五keyと consumer の全使用点が閉じ、旧誤 bytes 形を許す例外はない。

AUDIT_1085_VERDICT: THREE_LITERAL_STATIC_REPAIR_COMPLETE; ALL_OTHER_SOURCE_RAW_UNCHANGED; FULL_FORWARD_REVERSE_EOF_EQUAL; P37_AND_OLD4_P_LOADERS_RAW_IDENTICAL; EXISTING_SELFTEST_BOUND_CONSUMER_NOT_COVERED; NEW_TEST_OR_CLI_0; NORMAL_GHA_ACTUAL_17_PARENT_ADMISSION_PENDING; NO_SOURCE_EXECUTION; CANDIDATE_FALSE; CROSS_CHECKED_FALSE; VERIFIED_FALSE.
