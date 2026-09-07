# Task1087 — v5 envelope-v2 の独立静的別読

F0. 判定。Task1086 の最終 review-snapshot-v3 に対し LIMITED_INDEPENDENT_STATIC_ENVELOPE_REPAIR_PASS。全変更driver本文・全WF414行・公開registry結合を読了し、未読変更body=0、未解決required finding=0。before-checker の実fixture比較は post_producer 入口へ一度だけ移り、比較不成立ならCを起動せず、三票保全と実C成功を要求する最終条件は保持されている。作者1086とは別の担当として、独自snapshot・全raw再構成・opaque source範囲照合を行った。新P私的本文の独立数学監査、自作C5の独立算術監査、実GHA成功を本票の判定に含めない。

F1. 基点と読了範囲。1087/1086指示書全文、1084実診断の最終票11336/836210f55118b8bea9823e97aa8fd29ca88362745219fa181e5a43ec68dfd658、旧1079最終・1081独立最終・公開serializer/R1/最終binding追補、1085公開pin/range票、1086作者最終11239/89431880b48ee51f1d2cc91467ef2f830a38a5e4ff03e414d64d3a5cdbb5b0d9を読んだ。旧driver1145254/f7181bc573c3aff041d6fff3520266ca401de6416b410d145c94aceaf3a18913、旧WF26294/f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3、旧registry499053/e30a6bde668f0778932f0c4fbd62752c698bd70b97e9b097dccde4e9348c2858を自系 task1087/baseline-v1 へ全bytes一致で固定した。初期票5290/d9c2eb268919c11d34bb269d0cfdbd854646d6f2199e74fb9eb949971a53021bは新実装未読時の記録として不変保存する。

run34143415388/1、head2751f8942a50377a13078cbf646cfaaa3845b71fの実診断は、P登録readerの fields 拒否・実exit1、C未開始、別の before-checker 票欠名による保全FAILである。Pのstep conclusion successを実exit0へ、C selftest成功を本C成功へ補完しない。この事実の全取得結合は1084/root正本を参照し、本担当が診断全5153fileを再hash・ZIP再展開したとはしない。旧入力・診断・1080受領器には書込も実行も行わなかった。

F2. 最終raw。以下は audit163/task1086/review-snapshot-v3 の作者freezeと、自系 task1087/independent-final-snapshot-v1 の全byte一致コピーを対象とする。新Pだけは公開票が指す task1085 のopaque実bytes、C5は保持repository実bytesである。

| 対象 | bytes | SHA256 |
| --- | ---: | --- |
| driver.py | 1145223 | 238285767c62b0377d1192bd264233252870e0a5cfb9906a75035c0de2139573 |
| workflow.yml | 26294 | 3c20910e9fcce7cb8e05e234b7cbf8f1e329146a62613c6031dc8440d11431f7 |
| inheritance-registry.json | 499053 | 521978064705f784312482883d24b43e931675b8b05a20c62868146c3cec370c |
| P5 active提案 | 366659 | 6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d |
| C5 保持 | 336193 | 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 |
| public-producer-source-and-ranges-v1.json | 226557 | 261c0c6b39d8a600f041c0341181f78268db272efdb887430c7c144c058d34a6 |
| final-material-manifest-v1.json | 3148 | b9772917983efc0b52bd173104180d67f6df47f2af726d0cf924ead8afc7b553 |

driver LF10038、WF LF414、registry LF2628。独自分割は列頭def/classから次の列頭定義またはEOFまでを採り、module-prefix一件を加えた106区間。旧1079正式台帳の全106 offset/bytes/SHA/nameへ一致し、新版も106区間である。105はnamed定義数であり、prefix込み106との数え方の差で欠落ではない。main区間には末尾if/呼出と最終LFも含む。103区間は全byte同一、変更はmodule-prefix・execute・post_producerの3区間だけ。旧同一区間と新変更区間を連結して新全文へ、逆に連結して旧全文へ一致した。

旧executeの2行141 Bを削除し、post_producer入口へ同じrequire一行110 Bを追加した全rawが境界draft1145223/ab9d36ff2e93bfdfab57664d9968b67e0fc2ead3f7112b3cad1dd151c9d42cbbへ一致する。そこから新P whole pin、当該current range pin、registry whole SHAの3行だけを結び、最終driver全文へ一致した。全20行driver差分、全8行registry差分、全23行WF差分を読了し、個々の置換による全文復元も一致した。新driverのbefore-checker呼出は静的文字列でも一箇所だけである。

F3. 実境界と停止条件。新driver7966–8039のexecute全文と8392–8425のpost_producer全文を読了した。post_producer最初の命令が fixture_audit('before-checker') とそのstatus PASS要求であり、P exitやoutput形成、実execution票の存在、eligible判定より前に実行する。helperはP/Cの実全subtreeをscanし、空directory/hiddenを含む全inventory、自己試験baseline、source、実selftest execution、gate、全file pinへ結ぶ。saveはxbであり、同basenameの既存票を上書きしない。旧execute(checker)のwriterを除いたため、正常C実行時にも同名saveは二度呼ばれない。

WF310–318の制御は全raw不変。Pがskippedでなければbootstrap success下のalways工程でpost_producerを呼び、Cはbaseline success・checker=true・metadata/P selftest/C selftestのsuccessを全て要求する。比較FAIL/INCOMPLETEまたは保存例外ではrequireが止め、GITHUB_OUTPUTのeligible=trueへ到達しない。既存helperが保存できた実FAIL/INCOMPLETE票とdriver-failure票を残す経路であり、空のPASS票合成はない。P失敗でもfixture自体が不変なら実比較票は形成できるが、P exit1は所定8fileの形成に関係なくC eligibilityを満たさない。P exit0/3でも全入力不変・所定8fileを満たす場合に限りCへ進む。P skippedまたは境界未到達は未形成のまま保持する。

fixture票のchecker_execution_observedは実checker-result file存在から取り、境界stage名だけで本C実行を主張しない。新runのC開始/成功票はexecute checkerが実際に呼ばれたときだけ形成される。三票reader8643–8680、always after-checker/archive、preservation、final_gate、final_mode/mainは全raw不変である。三stage全PASS・全baseline/実inventory一致・ZIP全entry/explicit directory/EOF等の実読了票と現在全fixture台帳を引き続き要求する。run.executionsは形成済みfileだけを読み、欠けたCはnull。finalは実P/Cの成功を要求するため、fixture境界の欠名を修理してもP失敗やC未開始のcandidateは許されない。これらは静的な制御経路の判定であり、今回新runの実観測ではない。

F4. 公開Pとregistry。P私的本文を文字列decodeせず、新旧全156 current範囲のLF位置/byte範囲/SHA/EOFを実rawへ照合した。155範囲同一、ordinal64 def next_batch_inventory_registration（line2081–2094）だけ1090→1105 B、SHA34b3f78dafc7252fc04bfa627d8931090fd6b019cdfd4fc5718c6204592114fe→270092a3aba2d65e903ed4363e33628b1d9e5a543d9cfcca7684d2b6cc8fef2e。元P366644/664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66と新Pの両方向全文再構成も一致した。三literalの意味監査はroot/1085の公開契約に従い、私的P本文の読了を当方の成果とはしない。正式登録五keyのfile_bytesと、個別file descriptorのbytesは区別され、受付exact8へ新recordを追加していない。公開selftest票が明記する「既存selftestはこの実登録consumerへ到達しない」という限定も保持する。

P4→P5の137→156、C4→C5の117→140全範囲をopaque実rawで閉じ、全分類も再照合した。Pは121同一/16変更/19追加、Cは100同一/17変更/23追加。これはv4→v5の歴史的差分であり、今回P5修理の155同一/1変更と混同しない。P37/C20の保持body57件、旧8loaderの全原/現範囲は全byte一致し、新P公開offset票の37件にも一致。C5全rawも不変である。全10 source versionのwhole pin、保持依存19 Python＋3 rawの22 whole pin、共有4kernelのwhole/指定範囲pinも独自照合した。いずれもsource実行や数学再演ではない。

current registryのraw変更はP5 whole descriptorとその一範囲のbytes/SHAを含む2行だけで、他の全rawは旧版へ逆置換一致した。historical/previous/currentの3埋込rawを独自抽出し、旧2rawの完全不変と新current499053 Bの全file一致を確認した。public_audit_registry→source_mode→audit_mode/全10 source保持→audit_material_bindings→intake/acceptance→execution/post_producer controls→always→final/runの通常本文を追い、同じ新pinが全保存票と原rawへ結ばれる。旧60範囲を今回の変更根拠へ昇格させず、共有TCB/NOT_MEASUREDの型も保持する。既存34blobの列挙契約、三registry、全17親/全inventory、R1の別basename二固定参照票、cost、8key acceptance、128/1/refill=false、全54433宇宙と各資源上限の本文は今回変更されない。

F5. WFと配置計画。最終WF全414行を読み、同active path .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml、name d972-r07-fixed-lambda-cycle-batch-v5-envelope-v2、marker [r07-fixed-lambda-cycle-batch-v5-envelope-v2-run]、新driver_v2 pathを確認した。中間v2の旧marker残留は作者が報告した一literal修理であり、最終3c20910e版には残らない。bootstrap/終了時11 SHA行・exact checkout SHA/workflow ref・driver実whole bytes/SHA/コピー一致・500000 B未満・bootstrap成功時のみの後続実行・終了時pin不一致のfailure伝播・両upload30日/全hidden保存は保持される。

exact-five-path-proposal-v1.json=2702/d0938375031ddf03368091b5e77140b69d63fa240ed82405d7fa770da9359ba6を全文読了した。旧Pを ops/source_versions/d972-r07-fixed-lambda-cycle-batch-v5-before-inventory-key-repair.py、旧WFを ops/workflow_versions/d972-r07-fixed-lambda-cycle-batch-v5-envelope-v1.yml へ原rawで先に保存し、新driverを search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v2.py へ別配置、その後active P/WFを更新するroot用提案である。旧driver_v1とC5の現path/rawを保持し、archiveを実行closure/数学親/TCBへ追加しない。全15材料・総2413098 B・directory0・目録自身を含む16 fileの実全pin一致も確認した。配置・commit/push・通知・次のAPI/run id確定はrootが後続で行い、本票では未実施である。

F6. 独自証拠。以下は task1087 相対で、いずれも新作成後に固定した。author票のPASSだけに依存せず、同じ生bytesから別に照合した記録である。

| file | bytes | SHA256 |
| --- | ---: | --- |
| independent-driver-whole-raw-proof-v1.json | 97856 | b3ee7e190a5d219d2998115e71212a9ab15fded3a8d38b94f7ee30bb96957c25 |
| independent-public-registry-and-opaque-sources-v1.json | 94372 | d299188b66bf9c7e146e99d1a26f5d3eb3799925d5166f28fffdf924b64299d3 |
| independent-workflow-and-control-boundaries-v1.json | 1351 | 43e83b89b304b3f90f87bda5634d59524a16590eb78137c66bc95e20a8998714 |
| independent-final-materials-and-proof-index-v1.json | 10245 | 8486fc834749a33fd6e67ea5335bf9e3bd67b79c2cd8d58272c56988c911389e |
| final-registry-classification-and-material-reception-v1.json | 22554 | da3c37769ac3f96f4d74bfa2daea29193d960fd7d47977de2d7357f17a9bc833 |

F7. 凍結と限界。1086最終作者票全F0–F8/両表/末行まで読了した上で、上記最終3rawに追加required findingなしと確定する。自系旧baselineと独自最終snapshotを保持し、変更scopeは指定返信とtask1087 TEMP材料のみ。metadataのbyte/hash/範囲比較は実施したが、Git/network/credential/Python/GAP/import/AST/compile/source/数学/受領器/GHA実行は0、新agentも0。新Pの全17実親通過・新selection・C成功・新rank・数学assuranceは未観測であり、本票で補完しない。未読変更body=0、未解決required=0として返信をfreezeする。

AUDIT_1087_VERDICT: LIMITED_INDEPENDENT_STATIC_ENVELOPE_REPAIR_PASS; FINAL_V3_PINS_AND_ALL_RAW_RECONSTRUCTION_CLOSED; REAL_PRECHECKER_WRITER_ONCE; ALL_THREE_COMPARISONS_AND_C_SUCCESS_GATES_RETAINED; UNREAD_CHANGED_BODIES_0; REQUIRED_FINDINGS_0; RUNTIME_PENDING; NO_MATHEMATICAL_PROMOTION.
