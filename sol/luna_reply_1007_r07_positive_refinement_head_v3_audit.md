# Task1007 — 正語P v3 / D v3 / WF v4の限定差分監査

状態: STATIC_PASS_RUNTIME_PENDING。Task996はF19の保存境界で保持して本便を先に完成した。変更は本返信のみ。Task1005/1006/1007/1008を全文読了した。source・実JSON・bytes/SHAの読取だけを行い、ローカルPython/import/AST/数値/GAP/network/git/credential/追加agentは使わない。rootがrelease/GHAを担当する。

## F1. 実失敗と原因

run33999045563/1、head `a324e4b44e3d24def59c901f2dbee758f04369fd` のP-stdout.jsonを実読した。510 B / `c6c1da75f292f8978a79564a0597b7db30547afe0f05b583cbca0d005895ab13`、FAIL、KeyError:'target_remainder_sha256'、elapsed19.929537であり、phase=base-record-closureは最後の進捗表示であって例外のsource行ではない。語/D本走の成功を意味しない。

旧P v2の `read_target_history` 1242–1245行はseed30/seed34を明示的にlegacy=Trueへ渡し、`add_delta` 960–978行は旧入れ子targetを読む。従って工房2163のseed二世代のflat字段仮説を事実として採らない。実在しない参照は1279行の `ref_head["target_remainder_sha256"]` である。旧refinement producerの `head_record` 944–951行はこの字段を保存していない。

保持済みcompletion TEMPと元diagnostic TEMPの実HEADを両方読み、同じ921 B / `6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba` を確認した。schemaはd972.r07.full-origin-refinement.v1.head、body13key＋schema/sha256の全15keyで、26/1385/8090、Separator/current_scan=null、state_head=`8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`、最終step_manifest=`1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c` を持つ。target字段は無い。rootが新たに全ZIPを回収して公表したTask1008とも一致する。この実親に旧1279行の参照は不可能であり、観測KeyErrorと整合する原因をsource/実親から特定した。

旧静的読了ではこのrefinement HEADの世代差を見落としていた。旧票を上書きせず、本便で実schemaと呼出し経路を結ぶ。対象の親世代や全26履歴を除外する修理、HEADへの架空target後付け、最後のtarget比較を削る修理は採らない。

## F2. 実最終stepと診断の照合

実completion root `%TEMP%/shadow-atelier-full-origin-completion-run33971897879-candidate-a1` の最終manifestを全文読み、instruction/resultは必要なschema/identity/target/pivot metadataへ限定して読んだ。全26段についてinstructionのtarget字段が実在すること、result.targetがplain三keyであること、両者と当該target-remainder.bin実SHAが一致すること、manifest/instruction/resultのstateが一致することもmetadataだけで確認した。数値行や消去の再計算ではない。

| 実file | bytes | SHA256 |
|---|---:|---|
| output/steps/000026/manifest.json | 1932 | 1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c |
| output/steps/000026/instruction.json | 147304 | db5327c34a6447220a4309bd4f606a9372849977221bb1c290730c53df52ddc9 |
| output/steps/000026/result.json | 151584 | 45588d8b319fe4c3497bb9ae6d7768119711aa2c8779779945bdf5fcbf78edd7 |
| output/steps/000026/target-remainder.bin | 12096 | 111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad |

最後のtargetはparent=`5cb563ec85586ff7653ded61edb51dfb8748576a8e42d92323625552b5c96427`、child=`111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad`、scalar=1である。instruction/resultのrank1385/gen8090/stateがHEADと合い、最終manifestのfilesがinstruction/result/targetの実全bytes/hashを認証する。新helperはこの経路を閉じる必要がある。

実v3診断のinventory-canary.json（2013 B / `3e4353ca6b000ed04015bfe1fac8d5240ecf8e1ba5349930917f35c2c4bc909b`）は20拒否群PASS、new-canary-result.json（1508 B / `22912f6e826c2ac08be02ef33d67a305916e3e1c8bf62ca753ab599837f85810`）はP4/D3の公開群名とreceiptを持つ。preservation-result.json（893 B / `c107fcf4fdd3547fde3d8ef3b9ecd78b0a8ea58f6b5eba23ea36d3ce04bd1372`）は取得16親/source/raw/受付の不変true、未形成word/Dの二件だけINCOMPLETEである。original-start-header.jsonも実整数1/原start不変を確認した。これらの全文を読み、旧型修理と整列修理の実成功を新readout成功へ昇格しない。

## F3. 独立D v3の全差分

新D `search/check_d972_r07_continuation_same_word_eleven_slots_v3.py` は176579 B / `273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c`。全行比較で変更は1066行のP path v2→v3と1067行の自身path v2→v3だけである。二literalを逆置換した全textが旧D v2と完全一致し、旧176579 B / `865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1`、LF2636を保つ。wireは旧v1のままである。

旧DのPhysicalRecipesとtarget_parent_historyの対象blockを読み、refinement HEADは26countだけを読み、各instruction/result.target/実packed targetと全named履歴を結ぶことを確認した。seed二件の親remainder字段はlegacy-seedでold_remainder_sha256に分岐する。HEADのtarget字段を読む箇所はcontinuationの選択HEADであり、refinement HEADへ誤用していない。同語13file/11slot/full80644/元Ref recipe/一般Act/全16親/全EOF/全資源/三群canaryは二path以外の全bytesが不変である。作者返信1006のF1–F4も全文読了した。

## F4. 新Pの実親readerと最終target結合

新P v3の追加 `validate_refinement_head` / `validate_refinement_terminal` / `read_refinement_parent` と変更後の `read_target_history` を読了した。HEADを実15key・当該schema・全seal・実921 B/hash・26/1385/8090・Separator/current_scan=nullに固定し、owner/source/start/canonical-index/packetの実whole-file SHAへ結ぶ。HEADへtarget字段を追加せず、26段のmanifest/instruction/result/packed target全履歴を読んだ末尾からtargetを取り出す。

実completionのsource/start/owner/resultを必要字段へ射影して再読し、新readerが読むschema、packet owner/manifest、start1359/8064/6 named parents、state/target、packet_parent_layoutを確認した。保存resultはstatus=PASSとterminal=UNKNOWN_RESOURCEを別字段で持ち、26/1385/8090、HEAD全file SHA、scan_manifest=nullが実在する。保存result.lambda_rho2と最終step result.separator.lambda_rho2の全辞書も一致した。このPASSは保存prefixの型であり、探索のcomplete-zeroを表さない。

新terminal helperは最後のmanifest全seal/hashとHEAD.step_manifest、再生したstate/rank/generation、instructionのrolling/predecessor、resultのbefore/after、三者のowner/packet/index/scan/materialization、元targetから子targetへのplain三keyを結ぶ。manifest内の全file descriptorを型・unique・整列で確認し、最後のinstruction/result/target-remainderの実whole-file pinと一致させる。targetは12096 Bの実packed SHAへ接続する。正常呼出しは全instruction/result認証後に必要metadataだけをhelperへ射影するため、projectionを元fileの認証代用にしていない。

seed30/seed34のlegacy=True、packet全3段、refinement全26段、外部E、選択continuation全64段と元33 named parentsからの履歴を維持する。新たな歴史の除外やtarget比較の削除はない。terminalと最終separatorのDERIVED辞書一致も追加された。各親境界の進捗表示と通常例外のstderr tracebackは原因位置を残し、stdoutのFAIL/UNKNOWN_RESOURCEと資源上限を維持する。

## F5. 実metadata canaryとP全差分の保存境界

埋込REFINEMENT_END_METADATA_FIXTUREをPythonとして実行せずJSON literalとして読んだ。実HEAD15字段、実最終manifest13字段、instructionの17字段、resultの14字段の計59字段を個別に照合して差異0、三payloadの実bytes/SHAも全一致である。HEAD/manifestのkey集合も実物と一致する。大きな消去配列を埋込の架空証明書へ置き換えていない。

第5群actual-refinement-head-last-targetは正常な実HEAD全file pinを確認し、本番と同じvalidate_refinement_terminalを呼ぶ。deep copyへの変更31件は、HEADのschema/countのbool・float・誤値/rank/generation/state/最終manifest/kind/current scan/架空target字段、六binding、seal、再生target・親target、instruction/result/payloadのtarget/hash/幅、scalarのbool、rolling、result rankのfloat、stepのboolを拒否する。HEAD変更は必要に応じて正しくresealした上で型・意味のgateへ入る。元fixture不変を確認後、正常helperを再び呼ぶ。これは新GHAで実行予定のsource読了であり、31件の実PASSは未観測である。

200658 B / `bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e` のPについて、旧v2から全text block差分を調べ、変更blockを全文読了した。追加helper/fixture/canary、対象history接続、二source path、docstring/import/traceback以外の既存blockは同一である。既存read_loop_stepと元start-header canary本文もそのまま保持されている。rootが発見したwanted_sources.checkerのv2残留はv3へ修理された実差分を確認した。selftestは既存四群に第五群を加えた全五群を要求し、旧成功suiteの追加再走は0のままである。

## F6. WF v4の全差分と起動境界

旧WF v3の108358 B / `04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604` から、新v4の112685 B / `b675e0fb543db87dd4cf2df13f56d1d2eda49384caba882a8ecf07d6fb19a67e` への全行差分を読んだ。変更はworkflow/schema/出力version、新P/D pathと実pin、第5群の名前・実HEAD/最終manifest/target pin・31拒否順序のgate、三件目の実失敗来歴である。旧20件のinventory canary、historical inventoryのcopy整列、exact16親/全64履歴/全30実entry、受入前の取得済み保全、全before/after EOF、13語file/同根11slot/80644座標、P/D各一回と全資源枠、常時hidden診断保存を維持する。

三件の失敗来歴は原v1の整数count誤読、v2の相対POSIX全文字列順序、v3の今回HEAD欠落字段を別run/source/WF/diagnostic pinで記録する。実v3のP4/D3・20metadata群PASSをP/D本走PASSへ読み替えず、phase表示は例外行の証拠ではないと明示する。診断artifactを第17の数学親にせず、旧失敗の再実行も要求しない。

check_canariesは全P5/D3の順序と各PASS・stdout seal・実exit0を要求し、新第5群のhead_fieldsをstrict int15、target_field_in_HEAD=false、同production helper、旧親数値再生falseと結ぶ。実行は内P5400/D10800秒、外100/190分、各7168MiB、job330分を維持し、cooperative stopとFAIL/UNKNOWNを成功へ変更しない。finishは全保存PASS・一P一Dの成功と現grade限定の全比較後にのみ候補を公開する。新retain helperの独立性、PB4 Fox零、全P零、grade2 MEMBER/NONMEMBER、A0、第三TCBの新主張はしない。

rootが公開前に発見したL22 job.ifのv3-run marker残留を、私も実headerで確認した。作者はv4-runへ修理した。修理後のmarker一literalを旧値へ逆置換した全bytesのSHAがb675e0fb…へ一致することを独立確認し、追加変更がないことを確認した。最終WFのpinはF7に示す。追加算術/gateの必須指摘はない。

## F7. 最終freezeと射程

| 最終file | bytes | SHA256 | LF |
|---|---:|---|---:|
| search/d972_r07_continuation_positive_word_readout_v3.py | 200658 | bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e | 3274 |
| search/check_d972_r07_continuation_same_word_eleven_slots_v3.py | 176579 | 273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c | 2636 |
| .github/workflows/d972-r07-continuation-positive-word-readout-v4.yml | 112685 | a4a436934f545465c97cbaed5cafcd38a73c253581fd6707676c7942af03c0f5 | 1718 |
| sol/luna_reply_1005_r07_positive_readout_refinement_head_v3.md | 11805 | 4a6f35e4fc79b28790d64230a179eb17cefab4249030af54115974b89854e77d | 79 |
| sol/luna_reply_1006_r07_same_word_checker_producer_v3_pin.md | 6491 | b6f0c5745666e99e16f20726d95d881337d0c200d5508b672cf77d8170b57eb5 | 34 |

三実行fileとD作者票の全bytes/hash・LF・CR0/BOM無し/finalLFを実測した。P作者票F1–F8とD作者票F1–F4を全文読了し、P作者票の最後の記述訂正と実hashも確認した。訂正は「HEAD/manifestをreseal」ではなく、該当HEAD逆対照だけをresealし、manifestは元bytes不変で全seal/hashを照合するという事実に合わせたものである。source/WFは変わっていない。

旧schema見落としを認めた上で、実HEADから最終manifest/全target履歴へ結ぶ修理、Dの二pathだけの差分、WFの新pin/canary/来歴/markerを限定静的PASSとする。必要なsource/WF修理は残らない。旧P/D/WF・旧監査票は不変である。

新GHAのAST、P5/D3と第5群31拒否、20metadata群、本P/D一回、全出力・全入力の実照合は未観測である。静的PASSを同語readout成功、grade2 MEMBER/NONMEMBER、A0、第三TCB、verifiedへ昇格しない。本返信を凍結してrootへ通知し、Task996は保存済みF19の境界から再開する。

AUDIT_1007_VERDICT: STATIC_PASS_RUNTIME_PENDING
