# Task1052 — DEPENDENT fixtureの独立静的監査

## F0. 対象pinと保存境界

Task1052/1051を全文読了。監査はrootの固定TEMP snapshotに対する静的監査であり、新helper/sourceは一度も実行していない。source差分・状態遷移・陰性の目的ゲート、作者1051最終票全F1–F9/77行を読了し、required findingは0。判定はSTATIC_PASS。以下のfixture期待値は実行PASSではない。

| 対象 | bytes / SHA256 / LF |
| --- | --- |
| 旧P3 `search/d972_r07_fixed_lambda_cycle_batch_v3.py` | 209926 / `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8` / 3434 |
| P案 `task1051-P-c5a8857ec48a-root-snapshot.py` | 220063 / `c5a8857ec48aec9d31117ab0762f90f41c3d1bb0f9184ef6dcb54b96e40fc3c0` / 3570 |
| 旧C3 `search/check_d972_r07_fixed_lambda_cycle_batch_v3.py` | 178914 / `1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7` / 2695 |
| C案 `task1051-C-50bd49942a12-root-snapshot.py` | 189505 / `50bd49942a12ddb050a4d59c922fb22f725cbf16a84a4f97468e108654ea23b9` / 2836 |

snapshotの所在は `%TEMP%/shadow-atelier-audit163/`。全4fileの実bytes/SHA一致、両案CR0/ASCII/最終LFを確認した。旧1048受領器・1048/1050票・候補source/WFは変更していない。

## F1. 全差分と呼出し先

P全差分は新 `k128_dependent_continuation_canary`（L3177以降）とselftestの呼出し・fixture_scope・production_interfaces_used、C全差分は新 `k128_dependent_publication_canary`（L2448以降）、roster群の呼出し、selftestのscope/interfacesのみ。全差分を読了後、追加関数と該当selftest接続をメモリ内の通常文字列で旧形へ戻すと、P全209926 B/a286dca4…、C全178914 B/1aebf6e4…へ完全一致した。通常本体・imports・登録・既存拒否・CLIに変更なし。最初のfc相対POSIX pathはopen失敗だったため絶対pathへ直し、全差分を省略なく読み直した。C本体の一度の出力切詰めも該当範囲を小分け再読して補完した。AST/構文実行ではない。

Pはmake_reduction_state→reduce_candidate_numeric→BatchPhaseStore.ensure/commit/accept→新open_reductionから実accept→restore_reduction→publish_candidate_decision→advance_reduction_numericを定義まで追った（P L430–535、1414–1519、1666–1845）。保持mはseed materializer v3のphysical_reduce/normalize_pivot/update_target L1239–1298へ結ぶ。CはBatchReductionState.reduce/advance（L279–356）、reduction_payloads/accepted_row_record/candidate_decision_record/compare_candidate_publication（L1296–1415）、compare_phase、CandidateFiles.object/compare（L957–995）を追い、保持L.reduce_dense/normalize/next_targetのseed checker v3 L539–579まで読んだ。単に期待outcome文字列を生成するstubではない。

## F2. 非零従属と次候補の紙上遷移

以下はF3上の定義とsourceからの紙上追跡で、実行結果ではない。列の残りは全48384次元の零。

| 系・候補ordinal | raw先頭座標 | 実消去後/正規化 | 処理後rank/gen; processed/dependent/accepted |
| --- | --- | --- | --- |
| P 0 | (0,2,2,0) | 同raw、sigma2で(0,1,1,0) | 2/8; 1/0/1 |
| P 1 | (0,2,2,0) | 旧e0係数0、新row係数2で全零 | 2/8; 2/1/1 |
| P 2 | (0,2,1,0) | (0,0,2,0)、sigma2でe2 | 3/9; 3/1/2 |
| C 0 | (2,0,0) | 同raw、sigma2でe0 | 1/1; 1/0/1 |
| C 1 | (2,0,0) | 新row係数2で全零 | 1/1; 2/1/1 |
| C 2 | (1,1,0) | e1、sigma1 | 2/2; 3/1/2 |

P初期はrank1/gen7、旧row=e0、target=2e1+e2+e3、selection lambda=2e1*。targetはe2の係数2を残す(0,0,2,1)へ更新、DEPENDENTではその全bytes不変、最後はe3になる。C初期はrank0/gen0、target=e0+e2、lambda=e0*。targetは最初にe2となり、従属時と最後のtheta0時もe2。したがって両系とも三候補目まで非零targetを保ち、最後の独立rowは旧lambdaに対するremainder pairingが0でも合法に追加される。

PのDEPENDENTではrow/row_manifest/lead/sigma/target_scalar/normalized_sha/new_row_offset等がNone、全remainder零、係数[0,2]、独立専用三payloadなし。物理rank/gen/head/target・rows/leads/provenance・last_row_manifestをdeepcopyしたbeforeと比較し、rows全inventory不変、processed/dependentだけ増える。last_candidate_manifestは候補決定の更新なので物理headと区別してよい。make_reduction_stateのlambda/lambda_rawはNone、rowsはbytes、残る比較対象はNoneと通常のJSON値・bytesのlist/dictであり、このall equalityはnumpy配列の曖昧な真理値を踏まない。

CもDEPENDENTの全零/None、係数[2]、三payloadなし、全physical identity不変を要求する。identityはtarget/lambdaをpack、rowsをbytes tuple、pivots/parentsをcanonical bytesにしておりnumpy比較事故を避ける。advanceはprocessed/dependentを増やし、decisionsへのdeepcopy追加だけを別履歴に持つ。両系の次独立rowはlocal offset1、global row IDはP2/C1となり、実row serializer/publisherまたはreaderと最終8files（二row×4）が結ぶ。三候補の実branchは個別assertでINDEPENDENT/DEPENDENT/INDEPENDENTを強制する。

## F3. 再seal陰性は別の一拒否

Pはordinal1の正しいDEPENDENT reductionをコピーし、lead=Noneだけを0へ変える。reduction再seal、変化したJSON bytesを含むtelemetry.payload_bytes再計数とseal、全manifest file descriptorのbytes/SHA更新・manifest再sealを行う。outcome/rank/係数/target/実arrayは不変なので、phase_rosterとBatchPhaseStore.acceptの全shape/hash/binding/telemetryを通る形である。restore_reductionは再構成remainder・固定lambda identityまで正例と同じ条件を通し、L1758–1761の `dependent_preserves_target_and_has_no_normalized_row` でlead非Noneを拒否する。k128_rejectはそのliteralを含むValueErrorだけを記録し、上流parse/hash等の別エラーも無拒否も自己試験失敗にする。

Cは正しいreduction phaseを保存したままcandidate outcomeだけDEPENDENT→INDEPENDENTへ変更し、そのcandidateのsealだけを作り直してcheck_documentを先に通す。正しいphaseの全bytesは不変である。別rootのcompare_phase成功を要求後、compare_candidate_publicationが期待DEPENDENT candidateを再構成し、CandidateFiles.object→compare L980の `candidate_expected_size_hash:candidates/000001/manifest.json` で保存候補との差を拒否する。正常advance L1412は比較L1411の後なので到達せず、陰性のbefore state全physical identity・processed/dependent/decisions不変も確認する。想定外ValueErrorを真の拒否として数えない。

P `dependent-nonnull-lead` とC `dependent-outcome-resealed` は各一件の独立したrejected_cases追加で、陽性三遷移は拒否件数へ算入しない。既存群は削除なしなので提案P[30,10]/C[28,9]は静的に整合する。これらの件数を現在GHAの実PASSとしては扱わない。

## F4. 保存と射程

Pはinput三raw/旧row/target/lambda、三候補の実reduction/decision・二row、positive-case、再seal陰性とrejectionをselection/dependent-continuation以下へ保持する。Cはroster/dependent-continuationに同様の実phase/決定/rowと陰性を保持し、rosterのcase-ledgerにも陽性結果と新rejected名を追加する。scopeと実production_interfaces_usedは呼出しに一致する。新cleanupはなく、既存tree/fixtureを削らない。

前五相のhash・source_correction/P1 rootsは明示した未受理synthetic placeholderであり、実E/raw/source/primal/P1/Bや旧1450親を再演したとはしない。Pは新open_reductionから実accept/restoreを使う限定、Cは自系serializerとreaderの同じfixture内比較であり、Pの出力をCが独立照合した証拠ではない。通常P/Cは別保持系統で相互import/新helper共有を増やさないが、新fixture両案は同一作者で、既存shared TCBも残る。静的PASSは機械PASS/cross-checked/verifiedではない。

次parent1578の実装、新lambda/全oracle、本番version登録、WF/資源枠/機械実行は対象外。TEMPのv3自己schemaは移植前の案として意図的に保持され、その名前だけを欠陥にはしない。書込は本返信のみ、ローカルPython/import/AST/数学実行・Git/GHA/network/credential・追加agentなし。

## F5. 作者票の読了と最終判定

作者1051最終票は15586 B / `455e8dfcd2cac35fd428160eb98b8baee1799bf5879370912e39fef4e58347de` / LF77。全F1–F9/全表/6項目の次parent案/末行まで読了し、対象P/C全pinはF0の固定snapshotと同じである。Aのscope・呼出し・別陰性各1件・保全・同一作者の限界は本監査と整合する。Bの実metadata受領と次parent設計は読み取ったが、Task1052のSTATIC_PASSを新parent adapter/新oracleや全artifact受領の独立認証へ広げない。

AUDIT_1052_VERDICT: STATIC_PASS
