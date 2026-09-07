# Task1084 — v5 run34143415388 停止の公開metadata診断

F0. 対象と判定。run34143415388/1、head2751f8942a50377a13078cbf646cfaaa3845b71f、workflow352449001、job101810168873。最初の停止は P の登録inventory字段の拒否、C は未開始。保全全体の FAIL は別の before-checker 比較票未形成による。final は本 P の実 exit=1 を最初に拒否し、候補は形成されていない。本票は停止帰属の限定監査であり、新source修理・新算術成功・新rankを主張しない。旧1079/1081/rawは不変。

F1. 取得範囲。診断artifact10026881343、name d972-r07-fixed-lambda-cycle-batch-v5-diagnostics-34143415388-1、全ZIP22185849 B / a9ff8b6ae480ad8530dc563f0a8c025479687fe0563e76277865550f9a4c40b0。rootから全展開完了後に通知された実rootは %TEMP%/shadow-atelier-fixed-lambda-batch-v5-run34143415388-diagnostics-a1、5153 files / 2342 directories / 106318347 B。初期5reportの限定取得と、その後の全entry取得を区別した。指定32入力の実全file bytes/SHAを取得entry票へ独自照合し全一致、初期5reportも完成rootと全一致した。rootは全entry EOF/展開後全SHAを照合済みと報告。本担当はwhole ZIP再展開・全5153file再hash・独立CRC・inner JSON seal再計算を行っていない。取得票の explicit_directory_entries=0、crc_independently_checked=false を維持し、ZIPが省いた空directoryの復元完了を主張しない。

材料の固定pinは以下。ファイルは audit163 または上記実root相対。

| file | bytes | SHA256 |
| --- | ---: | --- |
| v5-run34143415388-root-acquisition-v1.json | 703 | f3b660ecb024cb7700848781153f0357e0fbf8df17edb3cd7466075bd92c61fd |
| v5-run34143415388-root-acquisition-v1.json.all-entry-pins.json | 1024099 | 42d5c04323fed143801427b78fad0afde1709cd7cb63e967f7afd368223f9b88 |
| v5-run34143415388-selected-reports-v1.json | 1602 | 5581b51e2d545a57b32606f13c6909af5acd5c49ca8c35350e29959feb0ff017 |
| execution/producer-result.json | 6489 | aa84078afbd8a097013223e4f921239d348885a74af70ff132d79ac0b9d1aca1 |
| producer-stdout.json | 2757 | abb788bdb1b3dab7adef7e21978697f9b5ee67a3a8b7ffe9cde2dc6c924ed6ad |
| producer-stderr.log | 10051 | 8b4cbeae6a3b21ee38194368989472a5f39bb95b93026410587ddf245b4d028d |
| preservation-result.json | 1976 | 18a6048d767d4854fe4a7fddc359f12adef315b99cce792fcf2d3e1779e0ed99 |
| run-receipt.json | 352170 | 0eada85b7b583f06dafc431a95ba538ab1928446699580957ecf730962079789 |
| selftest-fixtures-before-producer.json | 1420 | a2805dd30eeeb94e0afd28eecc21c1ee2f9e8e73617e299dfeac4fb0d38ec3b4 |
| selftest-fixtures-after-checker.json | 1413 | b733b55fac5e84466bc7f9fe6ed21bddf9a02be0bd4f444f967698556d3f8e86 |
| selftest-fixtures-archive-receipt.json | 1804 | f8e6dae8b9cb8b8e186b0e11b1fdd110e2f4fab130dca16e090bda4c82b04ec7 |
| selftest-fixtures-inventory.json | 916522 | 73ddd8815c9793b9a85344194601c7bfb4b12a99edd935eb34f4f6f250b1b326 |
| selftest-fixtures.zip | 4529804 | 5311f16c1a356949a694faba3862c20036417429781f3e88656818acaf6830ca |
| cost-receipt.json | 18922 | 608a70842c469af15f2e920e56d90a42682c28e9f798d373c7be8d2b075c373b |

F2. P の実停止。producer-stdout は schema d972.r07.fixed-lambda-cycle-batch.v5.rejected、status FAIL、terminal REJECTED、phase batch_checkpoint_metadata、reason ValueError:fixed_lambda_batch:next_batch_registered_inventory_exact_fields、elapsed_seconds=31.769016。execution/producer-result は開始2026-09-07T16:32:03.625953+00:00、終了16:32:35.652340+00:00、outer elapsed=32.02643309899997、整数 exit_code=1、outer_terminated=false、reason=null。producer-exit-code.txt は実2 bytesの1とLFであり、stdout/stderrの全pinとrun内execution全valueも一致した。時間5400秒/7168 MiBでの資源打切りではなく通常の型・keyset拒否である。両 elapsed は別の観測。rank/generation/processed/accepted_new_rows、selection/public HEAD等はnullで、旧128 rowのmetadata進捗を今回の128採択へ読み替えない。

公開stderrのtracebackは main→run_actual→authenticate_acceptance→authenticate_next_batch_parent→next_batch_inventory_registration と到達し、最後に要求した五字段が files, bytes, directories, files_sha256, directories_sha256 と記録されている。正式1082登録は file_bytes であり、rootもPのconsumer不一致を確認した。本担当はこの公開traceと登録契約までを根拠とし、P私的本文を読んでいない。Pの専用登録reader修理が必要であり、数学・Cの修理や資源上限緩和へ置換しない。

F3. workflow success表示と実制御。既読WF workflow.yml=26294/f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3、driver.py=1145254/f7181bc573c3aff041d6fff3520266ca401de6416b410d145c94aceaf3a18913 は実artifactと同pin。WF303–307のproducerはcontinue-on-errorで、jobsのsuccess表示を子Pのexit0へ補完できない。ログ301586/131236bd3aa407b5335ff6077769f5dd857ef6f30e94c245cc9fc0ab98865855 のL2299に16:32:35.6708182Z exit1、preserveのL2932に16:33:19.6725981Z exit1、finalのL3298に16:33:21.3362545Z exit1を読了した。全raw pinと関連範囲を読んだが全3494行の全文読了とはしない。redirectされたP reasonは実stderr/stdoutから読む。

post_producer（driver8394–8426）は実P後outputと全入力baselineを採取し、C eligibilityには exit∈{0,3} と所定8fileの存在を要求する。今回outputは rejected.json 一件2757/abb788bdb1b3dab7adef7e21978697f9b5ee67a3a8b7ffe9cde2dc6c924ed6adだけ、directories=[]、exit1であり、両条件が不成立。WF313–318のC gateが閉じたことは正しい。execution/checker-start.json、execution/checker-result.json、checker-exit-code.txt、checker-result.json、output/result.json は実rootと全entry名簿の双方に存在せず、run.executions.checker=null。本C未開始とC selftest成功は別。

F4. 旧R1と異なる保全finding。最初の欠名は selftest-fixtures-before-checker.json。writerはdriver7977–7978の execute(checker) 内にしかなく、C未開始では呼ばれない。check_fixture_preservation（8645–8646）は before-producer→before-checker→after-checker の三票を無条件に sealed/read へ渡すため、二票目が JSON-regular-file で止まる。run比較descriptor before-checker=nullと、実root/取得entryの欠名を独自確認した。対応fixture-inventories/before-checker/P.json・C.jsonも双方に存在しない。これは旧R1の二固定参照票の保存名衝突とは別で、R1の二basenameを戻す理由にならない。

実before-producerはPASS、両P/C fixture COMPLETE・unchanged=true、producer_execution_observed=false/checker_execution_observed=false。always fixture_archive_mode（8356）が実形成したafter-checkerもPASS、両root COMPLETE・unchanged=true、producer_execution_observed=true/checker_execution_observed=false。この stage 名はCが実行された証拠ではない。Pのbaseline/before/afterは全inventory一致（1449 files/719 directories）、Cも全inventory一致（3341 files/1630 directories）。それぞれ実baselineが示すexecution/selftest票の全pinも照合した。

archive receiptは実status PASS、both_completed_roots_unchanged=true、reason=null、raw_fixtures_retained=true、all_entries_and_explicit_directories_read=true、all_file_bytes_SHA_EOF_and_CRC_read=true、partial_or_missing_roots_claimed_complete=false。3 inventory rawは全て916522/73ddd8815c9793b9a85344194601c7bfb4b12a99edd935eb34f4f6f250b1b326、保存台帳は4790 files/2351 directoriesである。ここでCRC/full inner-entry読了はGHA側receiptの観測であり、本担当の独立再計算ではない。欠名による保全FAILからfixture改変やarchive破損を推論しない。

F5. 保全とfinalの射程。preservation-result のstatusはFAIL、errorsは一件だけ scope both_complete_fixture_subtrees_and_entire_archive_unchanged / ValueError:batch_workflow:JSON-regular-file、missing=[]、false flagもこの一件だけ。17 acquired-parent flags、source/code/driver/copies、両fixed-reference receipts、全入力・親・audit・二層transport・保存cost等の残る旗はtrue。これは読了した実票の主張であり、本担当による全親payload再計算とはしない。producer_output_unchanged_by_checker=true も未開始Cの成功証拠ではない。

final_gateはmetadata/P selftest/C selftest/P/Cの順にchecked_executionを呼び、Pに対するdriver8062–8063の実exit0条件が先に落ちた。run-receipt はstatus FAIL / ValueError:batch_workflow:execution-actual-success。current、producer_result、checker_result、parent_intake、batch_observation はnull、candidate/cross_checked/verified=false。候補uploadはskipped、diagnostics uploadは成功。cost-receiptはINCOMPLETE、missing output/result.json とchecker-result.json、errors=[]、seconds全nullである。P停止に伴う費用欠品を0秒、正常P/C固定費、新進捗へ埋めない。

F6. 最小修理境界。Pは正式 file_bytes を読む専用readerのliteral/keysetだけを修理する。driverは実before-checker採取を常時P後のpost_producerへ一度だけ移設し、execute(checker)の重複排他saveを除く案を採る。採取はP exit/OUTPUT8file形成/eligibilityの判定に依存させず、比較不成立ならeligible=trueを出さずCを止める。両実selftestが形成したbaselineと全fixture subtreeをその時点で再採取・照合するため、Cを実行したという架空票は不要であり、checker_execution_observed=falseを保つ。

三票必須reader、baseline/source/execution bindings、always全archive/全entry EOF/空directory・hidden保存、実C成功を要求するcandidate/final gateは維持する。未開始Cに対するreader免除や空のPASS票合成はしない。post_producer自身が未到達/比較失敗/部分保存なら保全は引き続きFAILまたはINCOMPLETE、candidate拒否のままにする。修理の別便ではP失敗→常時P後採取→C未開始→always終了採取の実保存を確認し、正常P→P後採取→C開始でも同basenameを二重saveしないことを全caller/WF条件で閉じる。C/math/親/caps/no-refill/宇宙の変更は必要ない。本便ではソース変更も試験実行も行わない。

F7. 記帳。task1084/public-metadata-causal-triage-v1.json =18458 B / fd62767865ab6e7b6e0381f717e2015b6deb986b32e10354a8a11162089c6108 に実32全pin・選別5一致・未形成8名・actual全execution/両比較/archive/preservation/cost・因果区別を保存した。pre-artifact-control-path-v1.json =5595/7aa7bd18468cd6cb9deb3ee8ea9d1557cc9fb3286a51704af7768fc5fb16b282 は取得前の歴史票として不変保持。Git/network/credential/数学/Python/GAP/import/AST/compile/source/受領器実行は0、入力root/旧1079/既存WF/driver/P/C/registryは変更0。修理は別Task1085/1086と独立別読へ渡す。

AUDIT_1084_VERDICT: PUBLIC_METADATA_CAUSAL_TRIAGE_COMPLETE; P_REGISTERED_INVENTORY_FILE_BYTES_CONSUMER_REPAIR_REQUIRED; BEFORE_CHECKER_REAL_CAPTURE_RELOCATION_REQUIRED; C_NOT_STARTED; NO_NEW_CANDIDATE_OR_RANK; NO_SOURCE_EXECUTION.
