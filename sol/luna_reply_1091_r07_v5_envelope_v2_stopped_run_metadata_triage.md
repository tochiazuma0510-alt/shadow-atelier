# Task1091 — v5 envelope-v2 実停止診断

F0. **実停止の一次原因は C の `KeyError:'selection_lambda_sha256'`。最終 gate は actual C exit 1 を拒否し、三 fixture 比較票と最終保全は PASS。P 出力は candidate のままで、正式 parent への昇格はしない。** run 34148667863 / attempt 1、head 3e7e1ccf1996dad15b9019de849cf61548c654d1、workflow 352449001 / job 101826078241、push による envelope-v2 を対象とした。Task1091 の read-only 公開 metadata 診断であり、全 typed envelope receiver の再実行、数学照合、source 修理は本便に含めない。

F1. 取得範囲と実入力。root の全取得・展開完了通知後にだけ実 root `%TEMP%/shadow-atelier-fixed-lambda-batch-v5-run34148667863-diagnostics-a1` を読んだ。診断 artifact は 10029340951 / d972-r07-fixed-lambda-cycle-batch-v5-diagnostics-34148667863-1、全 ZIP 384805623 B / 8947aa9b44be82c9d5f8d8d08f86c3da3fdf5eb8ba0d96c38eedf460e40d71e1。root の download は 18:18:35.6257135–18:32:49.9477967Z / exit 0、全 entry 展開も exit 0。取得票 `v5-run34148667863-root-acquisition-v1.json` = 707 B / 6ca0249065af61354fcaa6cb29e37c1bae9ddb8c585baaed4160bdf57a8442e6 と、同名 `+.all-entry-pins.json` = 2158818 B / 6d53611209db05270e77dfec32a0a1a44c0fe950f20f0658c9b7aca65010097e を実 hash 照合した。root が全 11748 files / 3507 dirs / 1345237252 file bytes の EOF/SHA と展開後全 file 再 hash を完了した handoff に依拠する。私は選定した公開票・raw source pin 49 件を現物から再 hash し、この全 entry 表へ結合した。全 ZIP/全 entry を私自身が再展開したという主張、独立 CRC 再計算の主張はしない。

F2. wrapper 表示と実終了を分離した。最終 run API 13846 B / 99e8d4f52f73052aa30f046b4cc522ff3bbec2a253132b4c16d7bc6a780303dd、artifact API 817 B / 980134a8226eaa987d828dfe30e15c184ad2d82c3f17049765823d0a935316c0、job 最終票 6264 B / 63b38e1b78baafa5f44c0ab445493892997a595da00aba583bfa8ac56e2ea91e を全文読了した。log 318016 B / bd85c25cbee777e8b2d4c0665b91a174eb76c3977306103d9349204e19cacb13 は全 raw pin と工程/error 検索・該当近傍を読んだ。C step16 の API conclusion=success に対して、log L2626 は 18:15:49.7362474Z に shell exit 1、final L3466 は 18:16:41.4394509Z に exit 1。WF L316 の continue-on-error を含む API 表示を child 成功へ読み替えない。五 execution の start pin、stdout/stderr 全 pin、exit-code.txt 全 bytes を照合し、先頭 metadata/P-selftest/C-selftest/P は実 exit 0、C だけ実 exit 1、五件とも outer_terminated=false / outer reason=null だった。

| 実票（root 相対） | bytes / SHA256 | 実状態 |
| --- | --- | --- |
| execution/producer-result.json | 6509 / ec6c407c0b4d5cc1421811c6ebc5a73dee6f8ebb5c1b0480584d302714f05a72 | exit 0、wrapper 1787.754941265 秒 |
| execution/checker-result.json | 6537 / afd9690af20795c5538acb28b6735a0a2fe449a5497c7f2fabbbc79f6436aa6a | exit 1、wrapper 13.521493211000234 秒 |
| producer-stdout.json = output/result.json | 各 208932 / cc3f2192548e064aca5ff202e2ca61f997e5425d9350e73eeae1665ae3daf1d7 | 全 bytes 同一、PASS / BATCH_COMPLETE_CANDIDATE |
| checker-stdout.json = checker-result.json | 各 1631 / 29be91764dc8c6f1de24e17e40d891602750b9038f03f73a675e1141390ca041 | 全 bytes 同一、FAIL / REJECTED / partial=true |
| checker-stderr.log | 26688 / 41f5e28d735b37bda9db32660461df45a121d8055214b7727f30ce7273366994 | 全 279 行読了、最後に実 KeyError |
| run-receipt.json | 359226 / bb6eeedd7d7ea278edd60d3147bf4ff4c269bf0a8add1274df09a70a3c7773c3 | FAIL / ValueError:batch_workflow:execution-actual-success |

F3. 一次停止と公開 key 契約。C stderr L279 の実 JSON は phase=parent_files_authenticated、reason=KeyError:'selection_lambda_sha256'、status=FAIL。checked_cursor は selection_compared=false / processed_candidates=0 / accepted_new_rows=0 / public_head_compared=false / last_complete_phase=null。実 stderr に traceback はなく、C source L1995 という行同定は root の公開所見・後続 Task1094 に依拠する。本便で私的 C 数学本文から独自に line を導いたとはしない。C result の候補比較数・受理行比較数は 0、selection/final/public HEAD の比較実証は成立していない。

実旧 v4 親 root `%TEMP%/shadow-atelier-fixed-lambda-batch-v4-run34120585268-candidate-a1` の次の三 JSON を読み、現 run acceptance.parents の batch-parent-v4 全 file descriptor と next_batch_anchor の各 descriptor の双方へ実 bytes/SHA を結合した。現受付は exact 八 key、親は 17 件である。

| 旧 v4 親 file | bytes / SHA256 | selection_lambda_sha256 |
| --- | --- | --- |
| output/selection/selection.json | 30909 / 181c87b906b2908e8d9d00e29faabf66bff673340e338bf18775e95150c3b4ab | key 自体がない |
| output/selection/start.json | 1038 / 00a6c7e54fa99b1e0d9c390005b02a0972785f2a3b576bb348cc3bb166ce7e2a | 6a0fe9368f2ec7f28c4d8076e7d3184fb57322b9d0905a8e7c3c26b467bcee4e |
| output/start.json | 119074 / 9ee29d5af385f5cb4b884a441237d27d302e17a1d0c15099bc62ea4001008e25 | 同じ λ1578 の hash |

したがって最小修理の所属は、既認証の selection-start record から当該字段を読む C の公開 parent-reader である。旧 selection.json へ架空の key を補う修理や、一般 reader を緩める必要は本観測からは出ていない。具体実装・全 consumer 棚卸しは1092/1093、C pin と envelope 接続は1094の別便に委ねる。これら別便の未完監査を本票で先取りして閉じない。

F4. P 完了票と旧二修理の通過。実 P source は 366659 B / 6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d、C source は 336193 B / 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 で、checkout copy を opaque raw hash で照合した。P は親 intake を作成して実 exit 0 / PASS まで進んだため、前回の formal file_bytes consumer 不一致は今回の通常 P を停止させていない。`output/parent-intake.json` = 5724 B / 194c4d83a1abc606355f430828bbe26edc2656f826d8744c8ccc216720b05852 は rank1706/gen8411 の入口を記録する。

新 P の selection は 30930 B / 1f8584296de7d8bf7306685ad3f3c996835660014107e31295c78e0b5d172812、selection/start は 1115 B / d4604259c9aae1d6fcd99eaf42784ceb91b15476219c0040df59fd7dca8057b7。保存 selection は CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX、selected_count=128（実 roster も128）、chords_checked=54433、eof=true、failed_count=36002、refill=false を宣言し、P result の両 file hash と一致する。新選択の λ1706 は d036e848c46b563a5b0f683fb94afcbc759dc4bc402c6db14c82b172ccc0a653 で、F3 の旧親 λ1578 と別である。P result の processed/accepted_new=128/128、dependent=0、rank1834/gen8539、kind=Separator は **P の未照合 candidate 値**。C がこれらを照合した値でも、正式 parent でもない。

F5. 三票形成・最終保全。before-checker 票は実形成済みで producer_execution_observed=true / checker_execution_observed=false、両 fixture は present=true / COMPLETE / unchanged=true / reason=null。before-producer・after-checker も同じ二 root の PASS で errors/missing は空。各 baseline/inventory の全 file pin を現物へ結び、P の三段階 inventory は同一 SHA、C も同一 SHA だった。固定 driver L8393 の post_producer 入口形成と WF baseline → C 条件に接続しており、前回の before-checker 票欠品は今回は発生していない。C 停止を理由に三票要求を緩めて PASS にしたわけではない。

| 保存票 | bytes / SHA256 | status |
| --- | --- | --- |
| selftest-fixtures-before-producer.json | 1420 / 6e222da6934735c42a03e08b0ee7baf6d596f56819adaa357e0d7ebaf8a828ac | PASS |
| selftest-fixtures-before-checker.json | 1416 / 311cc9e5f55fe268c10698bea0b59c6cfdefd17cba73312ba03d194e8e374e61 | PASS |
| selftest-fixtures-after-checker.json | 1412 / dd2ad4a8d97fc81e675ab7f0939027d33c62a8c5f1cb3f0712977458067cfc4e | PASS |
| selftest-fixtures-archive-receipt.json | 1803 / 753e96006138e6e081bd9a7ba2805de5244fd1056da1756881fce24a8facd4ce | PASS / both_completed_roots_unchanged=true |
| preservation-result.json | 998773 / 559c1b722e268b926ad7bc330deb0fec2079c9149079e67053291ec2721efcf5 | PASS / errors=[] / missing=[] / 全29 flags=true |

保全票は acquired_parent_baselines=17、source/driver/WF/raw copies、旧17親、二 transport、audit資料、二 fixed-reference 票、P/C 前後入力、P出力、fixture、cost 全入力の保存条件を true と記録する。巨大 output 配列を tool に全文表示せず、全 file hash と必要な全 flags/空 errors/空 missing を読んだ。archive 実 file は 4530052 B / 45c76ed69967a503c1490a50c07f2a09a3bfa9236cc0d969dac114a2e6acea83、三つの archive inventory は各 916522 B / 20ee236dc682a896bb81a2dd935f639fe2982e11a68fbc22ef81fd2176567042。inner ZIP の全 entry/CRC 読取は GHA の実 archive 票の観測であり、私のローカル全 stream 再実行ではない。先行 message の「28 flags」は29へ訂正済み。

F6. 費用は停止時の部分観測。cost-receipt.json = 375330 B / 5f9d7dd6733b3f83c72f77dcef74b63420e9d716b4b3c0709c4b9e7e658516ec は **INCOMPLETE**。complete_measurement=false、errors=[] / missing=[]、negative_residual=false、clamp=false。入力欠品ではなく C の FAIL/partial=true によって成功した全測定にならない。全776 input（4 result/wrapper、3 selection、128×6 candidate phases、1 final）の実 pin・保存 elapsed 字段・非負有限数値と、772 manifest pins をローカル metadata 読取だけで照合した。六相それぞれ128、selection3、final1の実登録である。

| 保存された量 | 秒 |
| --- | ---: |
| P total | 1786.546643 |
| P selection | 12.861132000000001 |
| P 六相 total | 1501.164409 |
| P final separator | 1.109362 |
| P residual（符号付き） | 271.41173999999995 |
| C 停止までの result elapsed | 12.569975434999833 |
| P total + C 停止までの elapsed | 1799.1166184349997 |

六相内訳は raw12.472539 / source31.782971 / primal316.4769 / p1 1097.738766 / B9.551466 / reduction33.141767。保存数値の十進集計は P residual=271.411740 で、元 double 字段と1e-9秒以内で一致する。元票を書き換えず、C全比較費用・C残差・P+C固定費・改善倍率・因果的な時間支配は推定しない。

F7. 最終 failure は二次の正しい拒否。実 driver/WF は 1086 凍結 pin（driver1145223/238285767c62b0377d1192bd264233252870e0a5cfb9906a75035c0de2139573、WF26294/3c20910e9fcce7cb8e05e234b7cbf8f1e329146a62613c6031dc8440d11431f7）と一致。driver L9469–9470 は metadata/P-selftest/C-selftest/P/C 順で checked_execution を呼び、L8060–8061 は実 exit0 / outer TERMなし / reason=null / exit file b'0\n' を要求する。前四件は実条件を満たし、Cの実 exit1 / b'1\n' がこの条件を満たさない。run-receipt の reason=ValueError:batch_workflow:execution-actual-success、current=null / batch_observation=null / candidate=false / cross_checked=false / verified=false はこれに対応する。final_mode L9891–9892 が拒否を捕捉して最終票に保存し、candidate upload は skipped、diagnostics upload は success。今回の保全 PASS を source/計算の全成功へ広げない。外側 gate や fixture writer の追加制御修理を必要とする新 finding は本実診断では見つけていない。

F8. 納品・未実行境界。`%TEMP%/shadow-atelier-audit163/task1091/actual-metadata-causal-triage-v1.json` = 75001 B / 7341b0ea069cf6954d8c3a7bba06c447611feeecc11712db4bc85f6132a13b05 に実49 pin、五 execution、全 C result、実 stderr 最終行、三票・archive・保全、全cost入力照合の件数と状態を保存した。`public-selection-and-cost-joins-v1.json` = 11199 B / 9c60d1c3835ae47cc975a3c5e683c72444d8209b1a179ecd421ec0ab800f0dbf に旧三fileの現受付結合、新P selectionのfile hash結合、費用の metadata 集計を保存した。取得前票 8714 B / 3b7496ae0f1c57a3dfe1a684aa4f1be3866f7227a294ef03eef6b2b8c57fae8e と取得前返信 raw も履歴として保持する。source/helper/Python/AST/数学/GHA/Git/network/credential 実行は0、入力・親・fixture・旧 process 変更は0。修理実装は後続便、独立 C の完走・新正式 rank・新 CV9 は未成立。

AUDIT_1091_VERDICT: ACTUAL_METADATA_TRIAGE_COMPLETE_C_PUBLIC_KEY_FAILURE_P_CANDIDATE_ONLY_PRESERVATION_PASS
