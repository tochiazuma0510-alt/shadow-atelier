# Task1098 — envelope-v3 の独立 WF／driver 静的別読

F0. **LIMITED_INDEPENDENT_STATIC_ENVELOPE_V3_PASS。** 1094作者とは別の担当として、最終 WF414行、driver登録3行、registry2行とその通常結合を読了した。未読変更body0、未解決required finding0。自作Cの数学的独立監査、P私的本文の監査、新GHA成功はこの判定に含めない。先行1092は最終返信13757 B / 940489bdde6e8a34dfd4c95d89caea06ca49fb8d988b5bdefd3f124b5b5e2283で凍結し、その実装作者としての立場を維持する。

F1. 読了と独自受領。Task1098／1094、作者reply1094全F0–F8／表／末行、前回の独立reply1087を全文読了した。作者最終目録5730 B / ccc7d163c9137999da0364cd7322671ba25d59a4cb4ba6c24ce4743d6ff36dccの全19材料／2532477 Bを実再hashし、目録自身を含む全20 fileを `task1098/independent-proposal-snapshot-v1/` へ全bytes一致で固定した。現repositoryのdriver_v2／active WFと、前回独自snapshotのregistryを `baseline-v1/` へ別に固定した。rootの7527 B静的票を根拠の代わりに用いず、自系rawから照合した。

| 最終対象 | bytes | SHA256 |
| --- | ---: | --- |
| 新driver_v3 | 1145223 | f1b50bc529f08ad8654d775e2fce652334dfa8b325d3d2bcc27286aa09cb3f98 |
| active v5.yml の envelope-v3 | 26294 | 3102f115c0d59d69d7ecc0b3941588b7fab5181e961b6399126a4e2516c4e969 |
| current registry | 499053 | 8792321d9cdcf25244726050928ae7fbd0cce5812e4f6867fa303ffcb49caa73 |
| C5 active提案（opaque pin結合） | 336211 | 111e23bfe6a7b49b4b3a03a00f3b48345c3f75ab098f06efc18279e881555b19 |
| P5保持（opaque bytesのみ） | 366659 | 6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d |

F2. 全raw差分。旧driver1145223/238285767c62b0377d1192bd264233252870e0a5cfb9906a75035c0de2139573から、変更行はL2852のC5 whole pin、L3509のcurrent reader範囲pin、L5463のcurrent registry全SHAだけ。列頭def/classとmodule-prefixで独自に全EOF106区間へ分け、105 named bodyは全bytes同一、module-prefixのみ変更と確認した。main末尾／最終LFも分割に含む。各変更行を代入した全文、同一区間と変更区間を連結した全文の両方式で、forward／reverseの全bytesが新旧それぞれに一致した。

WF変更はL2／11／145／146／150／152／170の7行、registryはL19／676の2行だけで、こちらも独自の双方向全文再構成が一致する。旧WFは26294/3c20910e9fcce7cb8e05e234b7cbf8f1e329146a62613c6031dc8440d11431f7、旧registryは499053/521978064705f784312482883d24b43e931675b8b05a20c62868146c3cec370c。新driver LF10038／WF414／registry2628、全てASCII・CR0・BOMなし・最終LF・行末空白0である。

F3. 三registryと公開source接続。driverから三つのbytes literalを実抽出した。HISTORICALは76867/9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38、PREVIOUSは236390/84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114で全raw不変。CURRENTだけ上表の8792321d…となり、独立したregistry file全文と同一だった。現C5全pinとordinal66の13653 B / d27a780a90627b8e7e641927706ed7a7bc0fd2082643f4ca023706491d4004f5を別々の対象として結び、後者を全source SHAやregistry SHAと混同していない。

全10 sourceのwhole pin、P4→P5の137／156区間とC4→C5の117／140区間、合計550の公開LF範囲／bytes／SHA／連続EOFを実rawへ独自照合した。保持P37＋C20 bodyと旧8 loaderの65結合も両端の実bytesが一致する。P sourceはbyte配列としてのみ読み、数学本文のdecode／読了やP consumer意味の全域閉鎖は主張しない。C sourceの同照合はWF登録のopaque結合であって、自案の独立算術監査ではない。

通常 `code_contract` → `public_audit_registry` → source／audit材料 → acceptance／execution → P後／C後／always／finalの接続は前回読了本文と全raw一致し、必要近傍を再読した。WFのC環境pinとcurrent registryのCURRENT_RUN_EXECUTABLEを同値で要求し、三registry原raw・非実行history全コピー・全receiptを再照合する。旧60範囲、共有TCB、CURRENT_RUN call coverage=NOT_MEASURED、full_typed_parent_metadata_complete=falseの留保は保持される。

F4. 起動・停止・保存の制御。全WF414行を別読し、同active path、name `d972-r07-fixed-lambda-cycle-batch-v5-envelope-v3`、marker `[r07-fixed-lambda-cycle-batch-v5-envelope-v3-run]`、作業branch限定、driver_v3 pathを確認した。checkoutのgithub.sha／credential非永続、起動前と終了時のdriver実bytes／SHA／raw copy、同順11 SHA行、WFの500000 B未満条件を維持する。全17親と8-key受付、旧64／previous128／immediate128／total256／353祖先、native1450／1578／1706は不変。次便は正式1706親run34120585268からfresh一回であり、失敗run34148667863のP1834出力を親やcacheへ流用しない。

上限はbatch128／max_batches1／refill=false、P5400秒／外6000秒、C10800秒／外11400秒、双方RSS7168 MiB、自己試験300秒／外360秒、job330分。metadata16、P[30,10,6,7]／C[28,9,6,7]の四群を保持し、数学二群と親metadata二群を区別する。旧数学群の再実行0、新群追加0。fresh selftest-root、空directory／hiddenを含む全fixtureの三時点比較とZIP全entry再読は変更されない。

`post_producer` L8393の最初の命令は実before-checker比較とPASS要求であり、その呼出は全driverに一箇所だけ。失敗するとeligible=trueへ進まず、WFはbaseline success＋eligible＋metadata/P/C selftest successを満たす場合だけCを起動する。形成済み八fileとP実exit0または3はC診断への入口となるが、最終candidateは `checked_execution` の普通整数exit0、終了理由なし、外側停止なし、実終了file `0\n`をP/C双方に要求する。step表示を実exit0へ補完しない。

finalは実stdout／外部C結果の全bytes一致、完成HEAD／result／finalの全hash、全相／全候補／全row比較、partial=false／durable_tail=null、全入力／source／出力不変、三fixture比較／全archive、別名の二fixed-reference票、親二層の復元票を要求する。bootstrap成功後のcost／fixture／保全／終了時再照合はalways、diagnostics uploadは無条件always。candidate uploadはfinalのcandidate=trueに加え実P/C／fixture／保全工程のsuccessを要求する。資源停止・C未形成・保全FAILをcandidateへ昇格させる変更はない。

F5. exact五pathと保全。提案はactive C、`search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v3.py`、active WF、`ops/source_versions/check-d972-r07-fixed-lambda-cycle-batch-v5-before-selection-key-repair.py`、`ops/workflow_versions/d972-r07-fixed-lambda-cycle-batch-v5-envelope-v2.yml`の五pathだけ。全提案source pinを独自照合し、active C／WFは旧pin、新三pathは未形成の状態も再確認した。旧Carchiveは336193/47cf2596…、旧WFarchiveは26294/3c20910e…の全rawである。P5／旧driver_v1／v2の現path全bytesは保持、新archive二pathはdriver／WFの登録本文に出現せず、親／実行closure／shared TCBへの追加0。repo配置はroot専任で、当方は行わない。

F6. 独自証拠は `%TEMP%/shadow-atelier-audit163/task1098/` の次表。本文sourceを実行せず、raw／JSON metadata／hashだけで作成した。

| 独自材料 | bytes | SHA256 |
| --- | ---: | --- |
| independent-material-intake-v1.json | 8188 | 2152f4cd01205260fe13d5d49991744c317b3498416b06e7ea3cd86b79ea3855 |
| independent-entire-raw-delta-v1.json | 120726 | 04e3ddae1bd6f5819df12a37f3d0dafe7e8d3ba4f217ea28da3c8309785e8b7b |
| independent-registry-and-opaque-bindings-v1.json | 644350 | c9ecc1648abae3efe22748c10a3c8e867b5b249c3b969b54fadcf0ba7557de97 |
| independent-static-control-review-v1.json | 36907 | f128dfa9a029862e83202513b54c84128da7c8712488a95ef4937abc2fd19bcf |

F7. 凍結と残る射程。限定WF／driver独立別読に追加required findingなし。1092の自系公開key監査、1093のP公開consumer gate、root最終全pin／配置前express、新full fresh P/C runtimeは別の要件として保持し、本票だけで先取りしない。2199／2217／2218のnotify-and-goとroot brokerの既存授権を変更せず、追加ユーザー承認待ちを作らない。新run／artifact／数学assuranceは未観測。変更は指定返信とtask1098 TEMP新材料だけ。source／数学／AST／import／compile／dot-source／受領器／試験／Git／GHA／network／credential／既存process操作／新agentは全て0。

AUDIT_1098_VERDICT: LIMITED_INDEPENDENT_STATIC_ENVELOPE_V3_PASS; ALL414_WF_LINES_AND_ALL_RAW_DELTAS_READ; 105_NAMED_DRIVER_BODIES_UNCHANGED; THREE_REGISTRY_BINDINGS_CLOSED; REQUIRED_FINDINGS_0; RUNTIME_PENDING; OWN_C_INDEPENDENT_MATH_AUDIT_NOT_CLAIMED.
