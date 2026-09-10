# Task1159 — C7 final-manifest 独立失敗裁定と repair 再束縛準備

宛先 Sol root。自身の C と公開 actual JSON/member metadata だけで裁定した。結論は、現在の anchor previous384/total512 に対し、final/manifest・HEAD・result の3枚が旧 previous256/total384 を保持した不整合である。C の述語修理・緩和は不要。新 repair identity と opaque P 未束縛の C、有限 raw binder SOURCE、公開伝播契約を納品した。

対象は run34492284273/1、head0373142c8b21a68d351d5160d07681678a0db59c。root受領の artifact10161505854 は403520626 B / a4dd619ac0263e9a1203e0f5115e81cd674c29a1cbad0ec6ef1b017ff219bf4e、全12048 member EOF/CRC/SHA受領済みとの報告を使用した。自分ではZIP受領を再実行していない。実 P native0、C native1 であり、正式成功の採択ではない。

F1. 公開値の独立突合。

| 公開位置 | completed | accepted parent | previous parent | total parent |
|---|---:|---:|---:|---:|
| start.json |64|128|384|512|
| separator.lambda_rho2 |64|128|384|512|
| C checker-result の完了prefix観測 |64|128|384|512|
| final/manifest.json |64|128|256|384|
| HEAD |64|128|256|384|
| result.json |64|128|256|384|

start の rank1962/generation8667、previous target derivations481、accepted target derivations609、実609要素も一致した。current packet は selected/processed/accepted new 各128、dependent0、rank2090/generation8795。separator は final pairing2090、target derivation737、新batch target steps128。これらの anchor count は現batch進行とは別の値であり、total_parent_batch_rows は512のままである。

自身の C は promote_fourth_batch_parent L4459–4461 で previous=128+128+128、total=previous+128 を作り、parent_intake_record L2784以降の普通入場で384/512とrank1962を要求する。root_records L4612–4615、final_rho2 L5207–5211、compare_final L5276–5283 が同じ anchor値を公開出力へ運ぶ。旧nativeの256/384を含む全述語とbodyは変更しない。

F2. 実 gate と到達範囲。

checker-stderr.log の17194行目は ValueError:cycle_batch:candidate_expected_size_hash:final/manifest.json。CandidateFiles.object L4507–4508 は期待した sealed JSON 全体の canonical bytes を compare に渡す。compare L4498 は最初に before の whole bytes/hash と比較し、通過後だけ実ファイルを開いて EOF まで一致させ、expected D3へ登録する。

compare_final L5289–5291 の順序から、この失敗より前に target-remainder.bin、separator.json、lambda.bin、telemetry.json の全4 payload は期待 bytes/hash と実EOF一致を通過している。final telemetry は payload_bytes447684=12096+423492+12096 と元の型/schema/計器条件も通過した。C result は selection3phase、candidate ordinal0..127 の全6phase、candidate decision128、accepted row128の完了prefixを報告している。

未到達は manifest 自体の実EOF比較・期待D3登録、HEAD比較、FinalReplay正常return、public_final_comparedの設定、後続invocation/diagnostics/input_inventories/producer result比較、最終candidate roster閉包、bundle/inputs/filesの終了unchanged、および全体PASSである。実C result は FAIL/REJECTED/partial、public_final_compared=false、final_manifest/public_head/producer_result/input_preservation/lambda は未採択のnull、cross_checked=false。stderr checked_cursor のaccepted/processed0は別cursorであり、result内の128観測を全体成功に昇格させる根拠にはならない。

F3. 診断用再構成とハッシュ伝播。

実公開7枚は strict UTF8・duplicate/nonfinite拒否・canonical raw一致と内部sealをmetadata計算だけで照合した。悪いmanifestは1925 bytesで内部sealも整合しているが、意味上の2countが古い。自身Cの公開literal期待とC progress、source/owner/start/selection-start、全memberの末尾candidate/rowとfinal payload pinsからmanifestを別名で再構成した結果、実値との差は previous、total、内部sealの3fieldsだけになった。サイズは1925のまま、whole hashが異なる。これで当該size/hash gateを説明できる。

仮想manifest whole SHA256 は bc6433b59fa7a6a1d9ec4ebd9e8731549280f8b349f1d19e80d755869957b89c、内部seal は7628e825578c021c09b3aacafa4ad6d8aace30fa3ec6d09c45bf88daebd4c95d。HEAD は2count・whole manifest参照・sealの4fields差で、1257 B / b36647afe7b537904c5fd1d85d70e0a92d1855311e505441848d8b451f125988。result の伝播はさらにwhole HEAD参照を含む5fields差、208916 B / f5cdaf39bde9a031dab639f9e122caedebebbeb23c8da48c1de06d5edacce367。

3枚とも task1159/hypothetical-count-propagated-{manifest,HEAD,result}-v1.json の別名診断材料であり、実artifactは改変していない。resultの他のreadoutは公開実値のコピーで、未到達のC result比較を代行していない。内部sealはunsigned objectのcanonical hash、manifest/HEAD参照はsealed full-file hashであり別物である。ここでsource_sha256はoutput/source.jsonのwhole hashで、P実行source SHAではない。新repairではcode identityからsource/owner/startと下流のhashが再形成されるため、旧run用仮想hashを新runへ流用しない。

F4. C repair の最小準備。

新sourceは task1159/unbound-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v1.py。変更はPRODUCER_FILE、CHECKER_FILE、root明示のCHECKER_WORKFLOWのidentity3 RHSと、旧P D3をNoneへ戻す1 RHSの計4箇所だけ。root指定WFは .github/workflows/d972-r07-fixed-lambda-cycle-batch-v7-repair-v1.yml、name=d972-r07-fixed-lambda-cycle-batch-v7-repair-v1-envelope-v1、marker=[r07-fixed-lambda-cycle-batch-v7-repair-v1-envelope-v1-run]。論理v7 schemaは保持した。

全EOF forward/reverse一致、6979 LF/0 CR、194全域の連続分割、193非prefix raw同一、C4登録24/unique21、旧event/method/selftest rawの保持をmetadataで照合した。正式v6 inventory5は変更していない。最終Pは未束縛であり、P body/hashを推定していない。

root用binder SOURCEは未実行。offset28091/4、line325のNoneだけを root が実発行する公開opaque P exactD3へ置換する。fileはsearch/d972_r07_fixed_lambda_cycle_batch_v7_repair_v1.pyに一致させるがファイルとして絶対に開かない。descriptor transport全pin、厳密型、194域/C4と正逆全EOFを出力前に照合し、全入力前後pin、CreateNew/flush/fsync/readback後の最後にcomplete handbackを発行する。actual native0や数学gradeをbinderが作らない。rootはbinder全文・全194raw・C4・4patchおよび公開cause/仮想hash/member再joinの独立読了を通知した。新P opaque descriptor後のbinder実行はroot工程であり、作者追加承認gateはない。

全材料は %TEMP%/shadow-atelier-audit163/task1159/。主要pinは次のとおり。

| 材料 | bytes | SHA256 |
|---|---:|---|
| unbound-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v7_repair_v1.py |525503|deff42a16b12e86a9d0848ec5568eb07933c1609779f76e580b0ca29dba3d7c0|
| public-final-count-and-propagation-contract-v1.json |18650|c357f6695e6f8fd64a0f5dbb0c7084a1233d4e3ad2a36a0cdb78ddfb69427c06|
| repair-identity-unbinding-forward-reverse-v1.json |4236|ac39cb1a5d87ac9893edf87f5f313f49ecbe8791647dce3c0fa2c863caf6d781|
| repair-unbound-all194-retention-v1.json |79061|3a5042e08d1d719432b541287410442825a5cf2959011ab88439f38f564ec795|
| repair-P-opaque-binding-plan-v1.json |2286|5151922dd60583f7f1fec16dc7dafd7fa0f09e5ee04a06c4d2240ec61ae3dc69|
| bind-repair-C-P-opaque-v1.py |9499|fce81693099800d9b99f568de01b1108c6f21cd5e20477cb9cb1736157406768|
| bind-repair-C-P-opaque-contract-v1.md |4714|b03f2bf37b0f5a1288adcf05b4bf44302cd55c040bc953617d521ea33f909723|
| final-author-material-manifest-v2.json |4012|fc72b96ecb636d3fa9349d06080f039adf46cf08199f18456cbc44fd8329230d|

最終manifest v2は14材料907036 bytes、自身を除く。v1 metadata helperはmember名の誤参照で出力前に停止し、CreateNew v2で正しいoutput/selection/start.jsonへ直した。材料一覧v1のPowerShell集計0も新v2で明示加算へ訂正し、v1を履歴として収録した。数学source/述語/binder/公開診断材料には影響しない。元Cと公開入力11本の終端fresh pinも一致した。

P private source/diff/票/2246原note、数学source import/AST/compile/実行/selftest、binder実行、receiver、Git/GHA/network/credentials、process操作、新agent、既存納品物上書きは行っていない。実runのC native1と全体FAILは保持する。

AUDIT_1159_VERDICT: INDEPENDENT_CURRENT_FINAL_COUNT_MISMATCH_IDENTIFIED; C_PREDICATES_AND_C4_RAW_PRESERVED; REPAIR_IDENTITY_AND_UNBOUND_OPAQUE_P_BINDER_DELIVERED; NO_NEW_RUNTIME_PASS.
