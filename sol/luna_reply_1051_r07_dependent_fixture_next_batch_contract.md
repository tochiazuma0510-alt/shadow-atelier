# Luna Reply 1051 — DEPENDENT fixture案と次1578 parent契約

F1. 完了範囲と読了資料

Task1051 全4629 B / `24b717759f23ed553601b35a93d82822594b60036b7b5f2872fd6468616c7fd1`、`docs/notes/fixed_lambda_batch_v3_cv9_reading_v1.md`全文、指定P1 canary L3000–3088 / C1 L2212–2283、現在P3/C3の該当通常入口を静読した。以下のP3/C3行番号は基準版の実LF行。TEMPにfixtureだけの候補2本と全差分を作り、新parentは契約調査に限定した。
変更した作業ツリーは本返信だけ。Python/import/AST/source・数学実行、Git/GHA/network/credential、新agent、WF作成は0。公開1048/既存P/C/WF/返信/受領artifactは変更していない。新fixtureのPASSは未観測で、以下の出力値は実行時に要求する期待値である。

F2. 変更前と候補の全pin

基準P3=`search/d972_r07_fixed_lambda_cycle_batch_v3.py`、基準C3=`search/check_d972_r07_fixed_lambda_cycle_batch_v3.py`。候補は `%TEMP%/shadow-atelier-audit163/task1051/search/` の同basename。公開v3/128/旧1450登録を保持する静的案で、次版登録・k256承認・完全な実行用checkoutではない。

| file | bytes | LF行数 | SHA256 |
|---|---:|---:|---|
| 基準P3 | 209926 | 3434 | `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8` |
| 候補P | 220063 | 3570 | `c5a8857ec48aec9d31117ab0762f90f41c3d1bb0f9184ef6dcb54b96e40fc3c0` |
| 基準C3 | 178914 | 2695 | `1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7` |
| 候補C | 189505 | 2836 | `50bd49942a12ddb050a4d59c922fb22f725cbf16a84a4f97468e108654ea23b9` |

候補はいずれもUTF8/LF、CR0、BOM無し、最終LFあり。最終再hashで基準2本も指示pinのまま一致した。

F3. 全変更境界・全差分

Pは基準L3177直前へ `k128_dependent_continuation_canary` 133行を追加（候補L3177–3309）。基準selftest L3299–3324を候補L3432–3460へ移し、第二群への呼出し1行、fixture_scope、production_interfaces_usedだけを変更した。
Cは基準L2448直前へ `k128_dependent_publication_canary` 138行を追加（候補L2448–2585）。基準L2581のcase-ledger保存直前へ呼出し1行（候補L2719）を追加し、基準selftest L2587–2601→候補L2726–2742のscope/interfacesだけを変更した。
この全editを基準raw textへ位置順に挿戻すと候補全文へ完全一致することをPowerShell文字列比較で確かめた。追加helperと列挙したselftest/callを除く全通常本体・import・CLI・元canary本文は同一。既存拒否を消した差分は無い。ASTによる関数比較ではない。

| TEMP task1051内の全差分・記録 | bytes | SHA256 |
|---|---:|---|
| producer-full-diff.txt | 13910 | `5c3233922057524ef798146b027378a4fec5af878e49aa689366ea0677766068` |
| checker-full-diff.txt | 13327 | `c8d0bd38a9f6e48c57f35a75d1842c4236f6cbc727036f1b2e574f650c53bb4b` |
| edit-coverage.json | 1868 | `46a19e73815b9956b2eab315d0207061b5e23ba7cfb439e580296a3329155b2b` |
| proposal-pins.json | 4067 | `0a21b08c70145fb83afa90b75207b1e30774f377b994c5cb59f8d420bf91505b` |

全差分は実LF行番号のzero-context unified形式。追加内容と変更selftestの旧新全文を含む。`proposal-pins.json`には2案・全差分・静的メモ・B観測表の全pinを収録した。

F4. P陽性と別の実陰性1例

旧P1の短い列を自系P3の通常接口へ接続した。full physical幅48384のsynthetic rank1/gen7、既存row=e0、target=2e1+e2+e3、selection functional=2e1*。候補は `[2e1+2e2, 2e1+2e2, 2e1+e2]`、selection scalarは各1。期待branchは `INDEPENDENT, DEPENDENT, INDEPENDENT`。
`make_reduction_state`→`reduce_candidate_numeric`→`reduction_payloads`→実 `BatchPhaseStore.ensure`→別readerで全保存payload再読/`accept`→`restore_reduction`→実 `publish_candidate_decision`（内部 `advance_reduction_numeric`）を通す。documents-onlyの代用ではなくrow/candidate manifestを実fixture directoryへ公開する。旧5 E phaseはsynthetic前方hashだけで、本体算術を通したとは書かない。
二本目は入力非零・実outcome・全零remainder・係数 `[0,2]`、lead/sigma/target_scalar/normalized/new_row_offsetとliteral外側指数のnullを要求する。normalized/instruction/target payload無し、row manifest無し、全物理state/target/祖先/既存row directory全bytes不変、processed/dependentのみ各+1をassertする。候補manifestの履歴更新は正しく残す。三本目は実独立rowを次offsetへ追加し、fixture最終rank3/gen9、processed3/dependent1/accepted2、row2本×4fileを要求する。誤って独立branchを通れば先行branch assertで失敗する。
陰性名 `dependent-nonnull-lead` は実二本目のleadをnull→0に変え、reduction seal、変更後payload bytesのtelemetry seal、全file descriptor、phase manifest sealを再形成する。実再読/accept後の `restore_reduction` の `dependent_preserves_target_and_has_no_normalized_row` でのみ拒否件数へ入る。上流の別例外や受理は成功対照にならない。

F5. C陽性と別の実陰性1例

Cは自系旧C1の入力型と現在 `K128MetadataAnchor` を使い、synthetic rank0/gen0、target=e0+e2、functional=e0*、候補 `[2e0,2e0,e0+e1]`、scalar `[2,2,1]` とする。Pのfixture/helperはimportしない。
実 `BatchReductionState.reduce`→`reduction_payloads`→own `fixture_phase`/`accepted_row_record`/`candidate_decision_record`でfile形成→`compare_phase`→`compare_candidate_publication(required=True)`→その内部の実 `BatchReductionState.advance` まで通す。読んだ全fixture files/dirsの不変も `CandidateFiles.unchanged` で閉じる。
二本目の非零入力が全零remainder・係数 `[2]` へ還元されること、DEPENDENTと全null、row非追加、rank/gen/head/target/rows/pivots/parents不変、processed/dependent各+1を要求する。三本目はremainderのselection pairingが0でも独立で、次offsetへ正常追加し、fixture最終rank2/gen2・processed3/dependent1/accepted2となることをassertする。
陰性名 `dependent-outcome-resealed` は正しいreduction phaseを保持し、実candidate manifestのoutcomeだけDEPENDENT→INDEPENDENTとして再sealする。元の受理済みsynthetic一段をbefore stateとし、`compare_phase`通過後に `compare_candidate_publication`→`CandidateFiles.object/compare` の `candidate_expected_size_hash:candidates/000001/manifest.json` を要求する。seal不正の対照ではない。拒否前後のphysical/カウンタ/decisions一致により `advance` 前で止まったこともassertする。

F6. 公開selftest型・保全・独立性の限界

二群名/順は既存 `k128-version-registration-and-types`, `k128-full-roster-cutoff-and-restoration` のまま。陽性は拒否件数を増やさず、別の実陰性各1件が通った場合だけP `[30,10]` / C `[28,9]` を返す案。実旧artifactのstdout全bytesを読み、基準P `[30,9]`（1703 B/dd24a08d…）、C `[28,8]`（1885 B/010160b8…）を確認した。元群/拒否の本文は全差分照合で保持されている。
Pは `selftest-root/selection/dependent-continuation/`、Cは `selftest-root/roster/dependent-continuation/` にinputs、3段packet、positive-case、別陰性file/receiptを残す。Cは既存case-ledgerにも陽性と追加拒否を収録する。fresh root規則/終了時全保全はそのまま。旧suite全再走0、actual_anchor_arithmetic_replayed=false、candidate/cross_checked/verified=falseを保持する。
両側の通常算術と旧系統は別、相互import/新helper共有無し。ただし今回のfixture案の作者は一名で、fixture作者の独立性は主張しない。P/C自身のserializerでsynthetic期待payloadを形成するが、通常reduceの実branch・full vector/assert・保存file比較・矛盾再sealの実拒否を追加している。全E source/primal/P1、実1450 parent、Ω全演算、独立な本走再現、共有TCB再閉鎖をこの小対照で証明したとはしない。

F7. Bで実読取した入力と限界

実root `%TEMP%/shadow-atelier-fixed-lambda-batch-v3-run34023589045-candidate-a1` の小JSONと行payloadの全bytes/SHAを読んだ。candidate9987222571/run34023589045/1/head794c5e9f883cb5ff21b2ee087c1d4baa84ac6760、ZIP369233546 B/781c9f467bd38305c524a0a2bf5b361f45e75bc4234d9cf6e891e01175db9e2eはroot handback。ZIP全体の再受領は本便では行わない。
`output/HEAD`=1140 B/bf476e1d9e7db9050cec9623d5b94a36a2361331cc1d96b2756085f1bc516b11、`output/final/manifest.json`=1808 B/7cc780041a7cbb605fa6192e9b75f66ae61a30961759006ff8288e808600fbbf、`output/final/separator.json`=118079 B/751a631bc4e6a87c4f5eb0e2a39b25a017e8d663bcf1f57941af71e453e8c636。
final lambda/targetは各12096 B、SHAは `6a0fe9368f2ec7f28c4d8076e7d3184fb57322b9d0905a8e7c3c26b467bcee4e` / `7868b7806a0dc41c2bda8a1c4c6a10d1cfa2c2e6968aadf561e93820f12053e1`。rank1578/gen8283、state `e793896e585bd0e540e25770359e8d36d1a84d69c012d88615e5ecffc02dfba9`、new_lambda_oracle=nullは保存metadataの観測。
128 row directory各4file EOF、全row/candidate/reduction manifest参照、全instruction predecessor、plain target hashとpacked target hashの区別、旧97項全辞書不変＋新128項の実10字段を追い、最終225項/HEAD targetへ結んだ。観測表 `observed-parent-layout.json`=609290 B/9558d9b18babd60e3f0b509355da32a1d0f112ba648dfe88cd956cd6ac4fed78。raw vector演算/seal再計算/元rho2直接再読/全artifact受領とは異なり、root1048のPASSを先取りしない。

F8. Bの最小移行契約（6項目、未実装）

1. **受入形式を分ける。** P3 L1047–1122/L1125–1166、C3 `AcceptedInputs` L484–566は15親/continuation64・1450/8155・旧checker schemaを固定している。旧15親とそのanchorを残し、16番目の `batch-parent` と別のtyped batch-anchor receiptを新versionで追加する案が最小。accepted旧batchのparent-layout/startにある元15親/64 anchorを全pinでjoinする。batchの128候補をcontinuationの128stepsへ改名せず、upstream completed_steps=64、accepted batch rows=128、新packet processed=0を別字段へ保持する。単なる1450→1578 literal置換は不可。
2. **実byte入場を閉じる。** 新親のwhole artifact/run/attempt/head/ZIP、全files/dirs、P3/C3/source/runtime、owner/source/start/parent-layout/fixed/selection start/selection、progress/checkpoint/invocation、public HEAD/result/finalと成功checker全receiptを登録する。実checker-resultは11956 B/5fcb1f9a8a568cf10df660be339763e6e7619bd73bf5932e286796204cf4020b、P resultは206763 B/5c05826c01d7cbca003a66cafde7430fcc7b997876afe2aaf449235d498dc18f。両者にlambda_rho2直接字段は無いので、全final_manifest hash→separator descriptorを介して225項へ結ぶ。rows/<0..127>/の `physical-normalized.bin,instruction.json,target.json,manifest.json` と対応candidate/reduction/literal/packed target payloadは実在する。保持closure/共有TCB資料も来歴として保存し、未観測の次artifactを登録しない。
3. **P/Cで旧1450＋新128を別々にloadする。** P3 `thin_anchor` L1227–1290の旧boot/64段metadata attachを保持し、その後に新saved-batch専用adapterを置く。新instructionはv3 physical-instruction seal/rolling body、row manifestとplain3key targetを持つので旧 `l.attach_step` への無変換流用はできない。P3 `parent_row_sources` L1193–1224へ新親12096 B行を入れ、挿入順/offset/全file hash/row hashを保持する。C3 `restore_physical_anchor` L786–954は自系旧loaderの結果へ別実装で128 `SavedPhysicalRow` とpivotsを付加し、`ThinAnchor` L712–771へ最終target/lambdaを渡す。既存97項を保持し全128 target delta/rolling chain/row manifestを照合する。旧batchのlocal offsetを新batchのoffset0と混同せず、旧行のsourceは `parent-row, role=batch-parent` と受理済みmanifestへ束縛する。
4. **現在separatorと派生鎖を新起点へ閉じる。** 新λの全1578 normalized rowsへの零pairing、旧1450時点targetと現在1578 targetへの各1をP/Cそれぞれ直接測る。次start.previous_targetは直前batchのstart.target（旧1450時点）を名指し、新current targetはfinal payloadとする案。祖先225項/元rho2 hash/符号規約を保持し、P3 `current_derived_rho2` L2238–2250の97固定を受理済み225項＋この次batchで採用した行数へ変更する必要がある。旧225項を再sealで改名せず、新owner/source/parent-layout/startの全hashへ束縛する。これは元rho2の新たな直接source readoutではない。P3 `read_final` L1883–1932 / final L2312–2364、C3 `compare_final` L1698以降の前提とtyped countsも更新対象。
5. **省略する履歴と新λ算術を分ける。** 旧64 snapshotsと旧128候補のA–D/E/reduction solveは、成功checker/full pinを前提にmetadataだけで受ける。full normalized rows/target鎖の読取と前項の直接測定は省かない。λに依存しないgeometry/basis/carry/canonical P1 dataは実fixed descriptor全pin照合後に再利用する。新q四台・全8059 P1 contraction/equalities・section/cochain・全54433 chord＋2auxはfreshにP3 `run_selection` L2675–2696、C3 `replay_selection` L1242–1275の各自通常経路で再計算する。新選択内容/terminalは未計算。非零候補がofferされ、raw pairing=nonzero selection scalarを結べた場合の最初の一本は新親spanを殺すλにより独立だが、二本目以後には保証しない。
6. **同旧1450/同λの先頭256との比較。** こちらは受入旧15親/1450 loaderを維持し、batch上限/版/候補ordinal・phase最大/fixture/登録を256へ広げるため、source移行は前5項より小さい。ただし先頭128の処理を含む重複があり、新λで取り直したoracle情報にはならない。現v3の完成packetは登録/owner/source不変の再受付しか認めないので、上限256への変更をそのままresumeとは呼べない。新1578/λ案は初期parent adapterが増える一方、現在spanを起点に別のrosterで次の一batch128を測れる。a(n)は新λ/新parentの系列として区別し、旧系列の失敗弦cursorや効率外挿は流用しない。新rank増分/従属数/速度/反復回数の予測はしない。

F9. 後続の実装・WF項目と最終判定

Aを採用する後便では、versioned source/closure pin、二群の件数gate P[30,10]/C[28,9]、全fixture archive/保全、実行receiptの接口名を更新する必要がある。歴史suite全再走は0を維持する。Bを採用する後便ではtyped16親/新anchor入場・独立2loader・source/version/policy/現在λ登録・fresh一batch128と資源上限/UNKNOWN・全保存が必要だが、本便ではいずれも実装/発射しない。
2案/全差分の静的読取と全文再構成は完了、通常本体への必須修理は見いだしていない。root途中静読の指摘無しと新fixture未実行は別の事実である。新λ1578 parentに必要な実byte入力は揃うが、現在の実装はその親を受けず、新adapter/新oracleは未実装・未計算。裁定2187のcross-checked限定8条、verified=false、grade2 NOT_DECIDED、A0不変、共有TCB/current-run call coverageの限界を引き継ぐ。

AUDIT_1051_VERDICT: STATIC_PROPOSAL_READY
