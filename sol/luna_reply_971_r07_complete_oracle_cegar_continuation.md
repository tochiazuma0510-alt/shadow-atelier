# Task971 — 完全oracle＋Eの動的継続器

実装を完成した。Task971・reply970、裁定2138の正本と二速達、到着した2143正本とgrade/ack速達を全文読んだ。変更は指定新producerと本replyだけ。source959/965とreply965/970は不変。ローカル数値/Python/import/AST/GAP、network/git/credential/追加agent/workflow変更はない。外部Eは実成功candidate33981657987/1の十entryを独立bytes/hash照合して固定した。新Task971のAST/canary/本走/独立checkerはrootのGHAで未実行。Task966/967のrelease条件にはしていない。

## 先行公開ABI・保持import

prefixは `d972.r07.complete-oracle-cegar-continuation.v1`。canonical JSONはASCII/sorted/compact/末尾LF、generic sealは自身のsha256字段を除いたcanonical bytesのSHA。file hashはsealを含む全bytes。arrayは既存packed3/u8-trit/u32leのshape/EOF、P1 exponentはJSON residue54（整数0..53、bool不可）を維持する。

CLIはTask965の13親に `--e-root` を加える。具体的には `--state-root --delta-root --seed34-root --packet-root --refinement-root --oracle-root --e-root --prepare-root --block-root`四回 `--p1-root --task712-root`、`--output`、`--max-appends`、`--max-seconds`、再開時 `--resume`。capは同じoutputでcommitした**新E**数の絶対上限。外部Eをstartへ一回attachしても新completed_stepsは0。`--selftest`はparent不要、`--parent-layout-selftest`はstate/delta/seed34/packet/refinement/oracle/eの7rootsだけ。

明示importは自系 `d972_r07_selected_cycle_materializer_v1.py`（88929 / `4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3`）。その `own_dependencies()` から凍結oracle v1→full-origin v1→fixed packet v2→materializer v3/batch v2/owner v15等を保持する。checkerをimportしない。新 wrapperは元moduleのsource/pin/schema定数を書き換えず、runtime deadline/progress hookだけを接続する。起点の原oracle producer/completion checker/外部E/new loop sourceを別receiptで保持する。

公開関数接続は、bootの `oracle.accepted_snapshot` と `e.read_oracle`、新 `read_external_e/attach_e_delta/build_current_start`、固定 `FixedBundle`、新 `current_section_cached/current_tree_cached` と既存 `oracle.current_roots_and_values/source_cochain/integrate_tree/chord_values/solve_five/classify_complete`、既存 `e.selected_raw_word/source_from_chain/primal_section/corrected_source/four_B/one_physical_row`、新 `PhaseStore/load_prefix/run_loop` とする。関数名がnewのものは本便の実装対象。既存Eのraw/P1/physical typed JSON内側はそのv1 schemaを保持し、動的owner/snapshot/witness refsを引数から生成する。外側のphase/oracle/step/HEADは新prefix。

固定bundleは `fixed/` に、geometryの既存10 payload、`potential-tau.u8` `[54432,5]`、`chord-tau.u8` `[54433,5]`、`selected-chords.u32` `[5]`、`canonical-index.json`、`basis.json`、`p1-exponent-residues.json` と新 `manifest.json` を置く。原oracle geometry stageの全bytesを認証して新固定ownerへ登録し、旧snapshot manifestを改称しない。basisは元owner/local/node/leadsと12blob descriptors/親hash、root pathを除いたsegment情報。同一processでreadersを保持し、各lambdaの8059式やEの全lower再構成を省略しない。

`snapshots/<completed_steps:06d>/start.json` はそのcurrent head/rank/gen/target/lambdaとDERIVED親列。oracleの `section/cochain/tree` は既存全payload rosterを維持する。sectionはq/全4×8059 values/chi/beta/kappa/8059 equations-residuals/元lead配列と解順、cochainはscore/f/b_aux、treeはpotential/chord values/tau/residual/selected/fit/witness。tree後に `oracle-result.json` と `oracle-manifest.json` を保存し、同じsnapshotの全EOF完了だけをE入力にする。

非零時は同じsnapshotの `e/raw, e/source, e/primal, e/p1, e/B, e/physical` にreply965の対応payloadを分ける。rawはword/chain、sourceはd0/d1/d2/aux/receipt、primalはalpha/reductions/mod54、p1はroots/lower-remainder/corrected-top/correction、Bはby-character/raw、physicalはremainder/normalized/target/optional lambda/literal/instruction/result。全six phaseのhashを `steps/<new_step:06d>/manifest.json` が参照し、physical instructionが一つの新state headを与える。

新phase manifestは `phase,owner_sha256,source_sha256,fixed_manifest_sha256,snapshot_sha256,previous_phase_manifest_sha256,files`。filesはfile/bytes/sha256/dtype/shapeのpath昇順、manifest自身を含めない。各phaseのelapsed_seconds/payload_bytes/EOFは別telemetry receipt。実時間は非負finiteとして認証し、checkerとの数値一致を要求しない。payload_bytesは出力量であり入力I/Oではない。

root `owner/source/start` とfixed manifestは不変。HEADはowner/source/start/fixed、completed_steps/last_step_manifest、current state head/rank/gen/kind/target/lambda、current snapshot/checkpointを結ぶ。checkpointは同じsnapshot/physical parent head・last_complete_phase・順序付きphase hashes・current oracle/witness hashを持つ。未計算はnull。cap/timeはinvocation receipt、GHA run/attemptはworkflow側のrun receiptに置き、ownerへ含めない。

phase内の未完だけをやり直し、完成phaseはtyped loaderで戻す。physical全payload→step manifest→HEADのpublish間に協調停止を挟まない。HEAD前のdurable phaseは同じsnapshot/preceding phase連鎖から認証して採用し、到達不能または未完tailを完成stepと数えない。producer resumeは全new bytes/chainを薄くattachし、最後のlambdaを全row/両targetへ直接測る。独立checkerは全new oracle/Eを再計算する。

分岐はCOMPLETE_ZERO_CANDIDATE（v548/Conn前提付きseparator）、LINEAR_MEMBERSHIP_CANDIDATE（Task958 pending、lambdaなし、次oracleなし）、UNKNOWN_CAP、UNKNOWN_RESOURCE、REJECTED。外部Eがlinear零なら初回からpositive pendingへ止め、fixed numerical bundleや次oracleを不要にする。新MEMBER/NONMEMBER/fullA0/verifiedを宣言しない。

2138限定8条を継承する。envelope/word loader/context/transportの共有TCBを明記する。q1..3/aux等の零は**現lambdaでの観測**であり、作用素全入力の恒等零ではない。score/f/tree第三実装の被覆をq/kappa/旧26scanへ広げない。v2専用serialization15 canary PASSと、full selftest未runを分ける。次実v2使用GHAのfull selftest一回はrootが手配する。頻度から確率/独立行数/残iteration/時間を予測しない。

## 公開 ABI 追記1 — 固定bundleと外側metadata

以下はgeneric sealの `schema/sha256` を除く正確な字段。Task554 bodyは `e.basis_segments` の一度の元lead/同一語mod54抽出でreleaseし、8segments/12readersを保持する。lambdaごとのnew→old双対解と全8059最終式を改めて実行する。四Bを一文字へ削減しない。raw Task554 descriptorのrootはstrなのでruntimeでPathへ明示変換し、segment.body_sha256を親body.sha256へjoinする。E primalは保持readerを借り、E corrected_sourceの全P1/全lower再構成と各blob EOF照合は残す。

`fixed/basis.json`（`.basis`）: `segments,rows:8059,lower_blobs:12,p1_manifest_sha256,canonical_index_sha256,lower_blob_pin_sha256,eof:true`。segmentsはold owners0..3→new owners0..3。old字段 `kind:"old",owner,start,rows,body_sha256,leads,lower_descriptor,grade_descriptor`、new字段 `kind:"new",owner,start,rows,body_sha256,leads,basis_descriptor`。root pathは出さずruntimeの同じTask554親へ戻す。descriptorは既存Task554 bodyのfile/rows/width/bytes/sha256等をそのまま保存。`p1-exponent-residues.json` は凍結E `.p1-exponent-residues` 全8059 pairsの同じ公開形式。固定carry3配列は認証済みoracle treeのbytesであり、現在lambdaのtree値ではない。

`fixed/manifest.json`（`.fixed-manifest`）: `owner_sha256,source_sha256,scope,accepted_geometry_stage_sha256,fixed_values_independent_of_lambda:true,files`。filesは先行roster16 payloadの昇順、file/bytes/sha256/dtype/shape。geometry元10 payloadとfixed carry3 payloadは旧oracleの認証済み配列bytesへjoinする。新manifest自身は新owner/sourceに束縛し、旧snapshot stageを流用しない。

root `owner.json`（`.owner`）: `formula_id,scope,external_e_owner_sha256,external_e_layout_sha256,oracle_owner_sha256,p1_parent,task554_parent,task712_parent,task712_manifest_sha256,word_dictionary_sha256,relator_dictionary_sha256`。formula_idは `v548-complete-oracle;v547-ordered-word;canonical-P1;four-B;dynamic-one-row`。scopeは先行宇宙に `source_universe_changed:false,external_e_counted_as_new_step:false,whole_normalized_word_replay:false,eleven_slot_replay:false` を付す。parent fieldsは受理済みoracle ownerと同じ。

root `source.json`（`.source`）: `producer_sha256,modules,data,python,numpy,parent_provenance`。modulesはE v1 + そのretained_sourceの7 modules、dataはその3data。parent_provenanceは `oracle_source_sha256,oracle_original_source_receipt_sha256,oracle_completion_checker_result_sha256,oracle_completion_receipt_sha256,external_e_source_sha256,external_e_source_receipt_sha256,external_e_checker_result_sha256,external_e_checker_sha256`。python/numpyはproducer環境を記録し、独立checker環境の文字列との一致を主張しない。

root `start.json`（`.start`）: `kind,rank,generation,state_head,completed_steps:0,lambda_sha256,target_remainder_sha256,previous_target_remainder_sha256,accepted_external_e_layout,accepted_oracle_layout,accepted_refinement_layout,accepted_target_derivation_parents,lambda_rho2,direct_pairing,external_e_attached:1,external_e_numerically_replayed:false`。

DERIVED current lambda（Separatorのみ）: `mode:"derived",value:1,original_rho2_directly_read:false,original_rho2_packed_sha256,accepted_target_derivation_parents,identity_convention,new_target_steps_executed`。identity_conventionは `base:"rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)",saved_deltas:"parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)",all_one_row_steps:"parent_remainder - child_remainder = target.scalar * accepted_normalized_row"`。new_target_steps_executedは当loopだけのcommitted数。親列は既存accepted列を保持し、external Eをrole `external-e`、loop stepをrole `loop-e-<6桁step>` で順に付す。一行親字段は `role,manifest_sha256,result_sha256,instruction_sha256,state_head,target_sha256`。target_sha256はplain3字段deltaのcanonical全bytes。target零ではlambda_rho2/direct_pairing/lambda_sha256はnull。

snapshot `start.json`（`.snapshot`）: `owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,step,kind,rank,generation,state_head,lambda_sha256,target_remainder_sha256,previous_target_remainder_sha256,accepted_target_derivation_parents,lambda_rho2,direct_pairing`。start_sha256は不変root startのfile hash。stepはこのoracleを使う前のcommitted新E数。

HEAD（`.head`）: `owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,completed_steps,last_step_manifest_sha256,kind,rank,generation,state_head,target_remainder_sha256,lambda_sha256,current_snapshot_sha256,current_checkpoint_sha256`。checkpointはsnapshot下 `checkpoints/<checkpoint全canonical SHA>.json` の不変fileとし、HEADがそのhashを選ぶ。`.checkpoint`字段は `snapshot_sha256,physical_parent_head,last_complete_phase,phase_manifests,current_oracle_manifest_sha256,witness_sha256`、phase_manifestsはPHASES順の `{phase,sha256}` list。新EをcommitしたHEADのcurrent snapshot/checkpointはnullとし、次snapshotの生成は別の停止可能単位。外部Eがlinear零ならfixed hashもnull。

oracle-result（`.oracle-result`）: `status:"PASS",terminal,owner_sha256,source_sha256,fixed_manifest_sha256,snapshot_sha256,step,rank,generation,state_head,lambda_sha256,target_remainder_sha256,lambda_rho2,direct_pairing,stage_manifests,section_equalities:8059,chords_checked:54433,auxiliary_tests:2,witness_sha256,materialization,new_physical_appends:0,old_scans_numerically_replayed:0,old_inserts_numerically_replayed:0,grade2_member:"NOT_DECIDED",grade2_nonmember:"NOT_DECIDED",full_A0:false,candidate:true,cross_checked:false,verified:false`。oracle-manifest（`.oracle-manifest`）: `owner_sha256,source_sha256,fixed_manifest_sha256,snapshot_sha256,stage_manifests,result_sha256,witness_sha256,terminal,stage_eof:["section","cochain","tree"],candidate:true,cross_checked:false,verified:false`。stage_manifestsは新phase hashesのsection/cochain/tree dict。

新phase rosterは先行表のとおりで、各phaseに新 `.phase-telemetry` の `telemetry.json` を追加する。telemetryの正確な字段は `phase,elapsed_seconds,begun_elapsed_seconds,ended_elapsed_seconds,payload_bytes,eof:true`。時刻2値は当invocationのmonotonic開始からの秒、elapsedはその差（丸め誤差3e-6未満）。manifest filesにはtelemetry自身も含め、payload_bytesはtelemetryを除くpayload全bytes合計とする。B phaseのみ型付き復元に必要な `B.json`（新 `.B`）を追加し、字段は `characters:[0,1,2,3],physical_trits:48384,source_correction_sha256,witness_sha256,corrected_scalar,physical_scalar,raw_sha256,by_character_sha256,all_four_summed:true,eof:true` とする。Bの2 scalarは同じcurrent witness scalarと一致する。ほかのE phase JSONは凍結E schema、oracle phase JSONは凍結oracle v1 schemaを保つ。内側raw geometry hashは新fixed manifest hashを受ける。

scopeのexact dictは `vertices:54432,edges:108864,chords:54433,legality_rows:5,normalized_auxiliaries:2,source_tags:6,characters:[0,1,2,3],p1_rows:8059,source_lower_trits:96776,physical_trits:48384,source_universe_changed:false,external_e_counted_as_new_step:false,whole_normalized_word_replay:false,eleven_slot_replay:false`。

## 実E pin接続

成功E candidate run33981657987/1、head `444c71c9e554ae8feb9c8ee54df57d3df19ed66f`、artifact9973974150、name `d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1`、ZIP2816692 bytes / `884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25` を採用した。root資料の十entryについて実展開fileをPowerShellで独立bytes/SHA比較し全一致、実HEADとchecker PASS metadataを読んだ。rank1386/gen8091/Separator、state `5e760f6a7c04a5eaf800289ab5b05ae542dc33c09b502ab7f87958b5e836a6a8`、target `e902cf3b2d9a5a58ac47459877e017fa4d6a44c5868751b8690543665ae269c1`、lambda `a16f4c8289e78efa068cfe923f1ee9a0d7b71f8c71aede582ff0ff93cda0c8ad`。全29output/8731365 bytes照合はrootの実receipt、producer側は十entryの独立metadata照合であり数値再実行ではない。新E起点はこれで観測済みとなった。後着2143の限定格は末節へ反映し、loop未来結果は未観測。

`accepted_external_e_layout`（新 `.external-e-layout`）のexact字段は `artifact,entry_files,manifest_sha256,head_sha256,start_sha256,owner_sha256,source_sha256,result_sha256,instruction_sha256,checker_result_sha256,terminal,kind,rank,generation,state_head,target_remainder_sha256,lambda_sha256,old_arithmetic_replayed:false`。artifactは上のrun/attempt/head/id/name/bytes/sha256（ZIP hashは `sha256:` prefix付き）7字段。entry_filesは `output/HEAD,output/manifest.json,output/start.json,output/owner.json,output/source.json,output/result.json,checker-result.json,source-receipt.json,oracle-intake-receipt.json,run-receipt.json` 十fileの `{file,bytes,sha256}` をpath昇順。実pin表はroot作成 `%TEMP%/shadow-atelier-audit163/selected-cycle-v1-candidate-33981657987-a1-pins.json` と一致し、source E_FILESへ保存した。checker sourceは `a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4`。旧oracle completionと今回Eの実source/run receiptsは別由来としてjoinする。

rootの次run登録は cap1→同outputでresume cap32。cap1内1800秒/外40分、resume内5400秒/外100分、checker全new prefix内10800秒/外190分、job350分であり、予測ではなく停止上限。terminalなら分岐し、completed_stepsをresetしない。

## 公開 ABI 追記2 — step・復元境界

phase外側schemaは新 `.phase-manifest`。pathは `snapshots/<step:06d>/section`・`cochain`・`tree`、Eは同snapshot下 `e/raw`・`e/source`・`e/primal`・`e/p1`・`e/B`・`e/physical`。`oracle/` 中間dirはない。

`steps/<new_step:06d>/manifest.json`（新 `.step-manifest`）のexact字段は `owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,step,snapshot_sha256,oracle_manifest_sha256,witness_sha256,predecessor_step_manifest_sha256,parent_state_head,state_head,rank,generation,kind,instruction_sha256,result_sha256,physical_normalized_sha256,target_remainder_sha256,lambda_sha256,phase_manifests,phase_eof,candidate:true,cross_checked:false,verified:false`。phase_manifestsはsection/cochain/tree/raw/source/primal/p1/B/physicalの**全9**dict、phase_eofはその順list。result_sha256はsnapshot/e/physical/result.jsonの全bytes hash。別 `e_manifest_sha256` は設けない。E全payloadはsix phaseに置き、step manifestが全9phaseの封印を束ねる。step dirはmanifest.jsonだけ（atomic-writeの未完 `.manifest.json.pending-<32hex>` は診断として許容）。

current λ のtreeは新 `current_tree_cached` が既存oracle integrate_tree/chord_values/solve_five/classify_completeへ接続する。固定potential-tau/chord-tau/selected-chord IDsだけを再利用し、current fのpotential/全54433 values/residuals/fitと二auxを省略しない。oracleのgeometry/section/cochain/tree内側schemaはv1のまま。既存 complete_tree_test 一括wrapperを呼ばなくても同じ公開数式/全rosterとなる。

完成rawの復元は既存RawSLPのtyped node/value/Refを再構成するだけで、completed rawのadd/product/Foxを再走しない。次の未完source phaseは同じ復元SLPを六tagで直接emitする。完成primalは全alpha/event orderとsame-word mod54、完成P1は実96776 lower payloadの零とcomponents/refs、完成BはB.jsonのscalar/eofを認証して渡す。固定partsへの破壊的再減算や内部scaleの二重適用は行わない。独立checkerは新全phaseの数値を再計算する。

tree dirの完成とoracle-result/oracle-manifestの間で停止した場合、同snapshotのtyped tree/section/cochain全bytesから決定的top metadataを作って保存する。tree checkpointはoracle top作成後だけpublishするので、phase数3以上のcheckpointはoracle_manifest/witness hashを持ち、phase数0..2は両方null。checkpoint自体は不変hash名fileで、古いHEADが指す旧checkpointを上書きしない。

## 公開 ABI 追記3 — terminal・invocation・診断

root `result.json`（新 `.result`）のexact字段は `status,terminal,owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,head_sha256,completed_steps,last_step_manifest_sha256,kind,rank,generation,state_head,target_remainder_sha256,lambda_sha256,lambda_rho2,direct_pairing,current_snapshot_sha256,current_checkpoint_sha256,complete_zero_oracle_result_sha256,new_physical_appends,external_e_attached:1,old_scans_numerically_replayed:0,old_inserts_numerically_replayed:0,external_e_numerically_replayed:false,positive_readout,separator_premises,grade2_member:"NOT_DECIDED",grade2_nonmember:"NOT_DECIDED",full_A0:false,max_appends_this_invocation,max_seconds_this_invocation,elapsed_seconds,candidate:true,cross_checked:false,verified:false`。statusはterminalがCOMPLETE_ZERO_CANDIDATE/LINEAR_MEMBERSHIP_CANDIDATEならPASS、その他はUNKNOWN_CAP/UNKNOWN_RESOURCEをそのまま使う。new_physical_appendsは累積completed_steps。complete_zero_oracle_result_sha256はCOMPLETE_ZERO時だけ現oracle-result hash、他はnull。positive_readoutはlinear時TASK958_PENDING、他NOT_APPLICABLE。separator_premisesは完全零時 `v548-Conn-same-source-map`、他null。時間/capは宣言値・有限非負として扱い、checkerの実時間と等値比較しない。

`invocations/<32hex>.json`（新 `.invocation`）: `invocation,owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,head_before_sha256,completed_steps_before,resume,max_appends,max_seconds,started_utc`。started_utcはUTC `YYYY-MM-DDTHH:MM:SSZ`、開始時点は入力・fixed認証後のloop呼出直前。cap/timeはここに保存しownerへ入れない。前invocation receiptsは不変。fresh invocationのhead_before_sha256はcompleted0/current snapshotnullの**実初期HEAD hash**でありnullではない。root resultは上のexact字段に `invocation_sha256` を追加し、今回のinvocation file全bytes hashを直接参照する。latest時刻やUUIDの辞書順から推測しない。producerは旧invocationのseal/owner/source/start/有限上限と旧resultの参照を認証する。

rootの許可fileは `owner.json,source.json,start.json,HEAD,result.json,resource-stop.json,rejected.json`、dirは `fixed,snapshots,steps,invocations`。未完writeは対応basenameの `.<name>.pending-<32hex>` file、fixed未完dirは `.pending-fixed-<32hex>`。snapshotの許可fileは `start.json,oracle-result.json,oracle-manifest.json`、dirは `section,cochain,tree,e,checkpoints`、未完oracle phase dirは `.pending-<phase>-<32hex>`。e下は6phase名dirまたは同じ `.pending-<phase>-<32hex>`。完成phase内はexactmanifest rosterだけ。checkpointsには64hex.jsonまたはそのatomic-write未完file、invocationsには32hex.jsonまたはそのatomic-write未完fileを許す。

numbered snapshotは0..HEAD.completed_steps、stepは1..HEAD.completed_steps+1だけを許す。+1 stepは同current snapshotのdurable physical全9phaseを伴う場合だけ薄く回復し、なければREJECTED。より先の到達不能numbered tailは**無視して合格にはせずREJECTEDで保存**する。本v1はorphan改名を行わず、任意 `.orphan-*` を許可しない。明示pending dirを完成扱い・step数へ加算しない。HEADが指す旧checkpointと、その先にdurableな全phaseを同じsnapshot chainへ認証してから最新checkpointまたはstep/HEADへ回復する。

入場/全prefix認証前のUNKNOWN_RESOURCEはroot resultを成功prefixとして書き換えず、新 `.diagnostic` の `resource-stop.json`（可能な場合）とstdoutに保存しexit3。入場後のphase中UNKNOWN_RESOURCEは上の通常root result/HEADでexit0。通常UNKNOWN_CAP/二candidateもexit0。REJECTEDは同 `.diagnostic` をrejected.json（当invocationが正しいoutputへ入場済みの場合）とstdoutへ保存しexit2。diagnostic exact字段は `status,terminal,phase,reason,head_sha256,diagnostic_only:true,elapsed_seconds,candidate:false,cross_checked:false,verified:false`。head_sha256は存在すれば実file bytes hashだが、全prefix合格の主張には使わない。

新 `--parent-layout-selftest` は旧20成功suiteを再実行せず、実oracle/external E metadata読取と新5拒否（external-e-kind / external-e-checker-incomplete / external-e-target-parent / external-e-ordinary-rho2-claim / external-e-current-head）を行う。返値はplain `.parent-layout-selftest` と `status:PASS,metadata_only:true,accepted_oracle_layout,accepted_external_e_layout,rejected_cases,old_success_suites:0,cross_checked:false,verified:false`。

## 2143継承・literal規約

[2143正本](../docs/notes/cycle_mat_v1_cv9_reading_v1.md) とgrade速達を全文読んだ。親EはCV9同一対象・cross-checked限定7条の有限一行事実（rank1385→1386/gen8091、target scalar1、依然Separator）として受理し、candidate payloadのcross_checked/verified falseを書き換えない。新current λや新stepへ格を移さない。

F-cy-1の実観測は未修理w=(epsilon_x,epsilon_y,omega)=(6,0,0)。効いた修理は `(r_x^3)^(-1)` 一因子だけで、repair-yとrepair-centralは空語、ω冪の二次項も本番45nodesでは0だった。三因子すべてを本番非自明に試したとは記さない。語長上界のroot長≤boundはこの構成では恒等式（3338=3338）で、独立な成功試験に数えない。

F-cy-3の**本loopのliteral規約**は既存v547 (4.2)の符号付代表 `s(0)=0,s(1)=1,s(2)=-1` とする。v548 §5の `[r_x,r_y]^omega(w)` はこの `^s(omega(w))` の略記と読む。同じordered factors/SLP hashを要求し、least-residue2へ勝手に置き換えない。2と-1の差はcommutator³であり、同sourceであっても同じliteral word/SLP hashではない。既存凍結Eと新wrapperは既にsを使うためsource変更なし。Task973はこの紙上接続をrootへ渡している。

F-cy-4aを保持する。envelope復号は両系のB物理行生成に効く共有TCBであり、word loader/context/transport、source形状の共有も残る。B表そのもの、旧1385行、P1 cache/Task554 liftは2143第三実装の被覆外で、二系統一致の範囲を超えて主張しない。元rho2は名前付きtarget identitiesを経るDERIVEDのまま。F-cy-4bのq character0だけ非零・κ tag0/aux零は旧current λの観測であり、本loopは全four q/全8059式/全six tagを毎回処理する。

2143のpositive側でE966新3 testsと本番24 source塊/四Bが非自明になったことは受け取る。一方、そこから**oracle checker v2のfull selftest**の既走を推論しない。E run-receiptは `v2_checker_imported_or_executed:false` であり、v2 dedicated15 serialization canary PASSとfull未runの区別は残る。次Task972 GHAでv2 full selftest一回をrootが手配する。旧26scan独立性F-fo-1の遡及閉鎖でもない。

## 最終freezeと残る実走gate

新source `search/d972_r07_complete_oracle_cegar_continuation_v1.py` は **126940 bytes / SHA256 `67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c`**。LF1972/CR0/BOMなし/末尾LF、行末空白なし。sourceを先頭のsource/pin admissionから最後のmainまで静的に読み、root/Task973にも完成blockを順次渡した。最終変更はruntime rootのstr→Path、親body SHA join、result→invocation file hashの明示結合。既存source/返信は変更していない。最終pinをroot/972/973へ通知した。

新canaryは3群で、(1) absolute cap1→resume32のcarryとstale lambda/witness拒否、(2) 完成phase→step manifest→HEAD間の停止をmetadataだけの小fixtureで再現し、typed phase再読でbuilderを呼ばずbytesとcountを維持、source/owner違いと未登録tailを拒否、(3) plain target scalar0・bool/seal拒否・linear zero≠MEMBER・完全oracleなしのCOMPLETE_ZERO拒否を本番関数に接続する。metadata publication fixtureは本番array rosterには拒否され、大規模な合成算術成功証明書ではない。新canary自体はここでは未実行。

GHA command案（各ROOTはTask972 workflowが実tuple/ZIP pinで展開した対応root、PARENTSは同じ配列を両invocationへ渡す）:

```bash
PARENTS=(--state-root "$STATE_ROOT" --delta-root "$DELTA_ROOT"
  --seed34-root "$SEED34_ROOT" --packet-root "$PACKET_ROOT"
  --refinement-root "$REFINEMENT_ROOT" --oracle-root "$ORACLE_ROOT" --e-root "$E_ROOT"
  --prepare-root "$PREPARE_ROOT" --block-root "$BLOCK0_ROOT" --block-root "$BLOCK1_ROOT"
  --block-root "$BLOCK2_ROOT" --block-root "$BLOCK3_ROOT" --p1-root "$P1_ROOT" --task712-root "$TASK712_ROOT")
python -B search/d972_r07_complete_oracle_cegar_continuation_v1.py --selftest
python -B search/d972_r07_complete_oracle_cegar_continuation_v1.py \
  --parent-layout-selftest --state-root "$STATE_ROOT" --delta-root "$DELTA_ROOT" \
  --seed34-root "$SEED34_ROOT" --packet-root "$PACKET_ROOT" --refinement-root "$REFINEMENT_ROOT" \
  --oracle-root "$ORACLE_ROOT" --e-root "$E_ROOT"
python -B search/d972_r07_complete_oracle_cegar_continuation_v1.py \
  "${PARENTS[@]}" --output "$OUTPUT_ROOT" --max-appends 1 --max-seconds 1800
python -B search/d972_r07_complete_oracle_cegar_continuation_v1.py \
  "${PARENTS[@]}" --output "$OUTPUT_ROOT" --resume --max-appends 32 --max-seconds 5400
```

実際の二回目はtyped terminalに従い、同output・既保存全bytes・累積countを維持する。残るgateは新AST、新metadata/canary、実cap1/resume32、Task972の全新completed phases/stepsと最終current prefixの独立照合、追加CV9の限定裁定である。source側は旧数値prefix/Eを数値再走せず、checkerは新phaseを再計算する。旧source/source-envelope/P1/Conn等の保持TCBを継承し、速度・追加rank・target零・反復数の未来値を予測しない。GRADE2_NOT_DECIDED/fullA0 false/verified=false。

AUDIT_971_VERDICT: SOURCE_COMPLETE_RUNTIME_PENDING; OBSERVED_E_PARENT_PINNED; CAP_RESUME_AND_TYPED_PHASES_IMPLEMENTED; verified=false
