# Task994 — 固定 lambda cycle batch v1・P 公開契約と実装

新P sourceは213861 B / 229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591で完成・凍結した。最終状態はF13–F17、F9–F12の未完成記載は過去の保存境界である。新数値/AST/三群/本走は未実行。

## F1. 開始と拘束

Task994 の C1–C11 を全文読了した。Task991 の source / WF / 返信は完成凍結済みで、以後変更しない。変更可は新 search/d972_r07_fixed_lambda_cycle_batch_v1.py と本返信だけ。以下は root の Task997 共通 wire へ渡す公開 ABI 案であり、Task989 の衝突する名称・partial publication 案を置換する。新 C source / reply995 は読んでいない。ローカル Python / import / AST / 数値 / GAP、network / git / credentials、新 agent は行わない。

本走は実64親 run33990567016/1、headc57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70、artifact9977040548、304642285 B / a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792 の一 batch、k=32 / max_batches=1 / refill=false に固定する。初期1450 / 8155 / 64 は実 HEAD から認証し、未来96を親にしない。selection lambda、private growing reduction state、最後の lambda を別の型にする。非零数、採用数、target零、時間や速度を予測しない。

## F2. wire の基礎と portable identity（root 確定待ち案）

prefix は d972.r07.fixed-lambda-cycle-batch.v1。以下の「body keys」は schema / sha256 を除く exact keys。seal は sha256 を除く sorted compact ASCII JSON + LF の SHA、file hash は seal を含む全 bytes の SHA。受付だけは C2 の指定通り六 top keys の plain canonical JSON で、自己 seal 字段を持たない。file descriptor は JSON等で exact file/bytes/sha256、binary だけさらに dtype/shape。配列 shape の成分、counts、signed ordinary exponent は type is int（bool / float を拒否）。u8=trit0..2、packed3=base3の4trit/byte0..80、u32le=unsigned little endian、residue54は明示0..53の普通整数 list。

owner / start / source / selection_start の portable identity に host path / 新 run / nonce / 時刻を含めない。受付 parents.path と CLI の実 root は完全一致させるが、保存 parent-layout は path を除いた role/artifact/全file・directory pinへ結ぶ。実受付 file 全 SHA は invocation に保存し、portable acceptance hash は parents.path を除いた受付本文から得る。別ホストの同一親を re-root しても owner が変わらず、resume 時は portable hash と実全bytesを再認証する。launch / host path / nonce / 実資源・計測は invocation だけの明示 metadata とする。

## F3. exact acceptance 案

top keys は schema, parents, anchor, code, runtime, registration。schema は prefix+.acceptance。parents は順序付き list、role は state,delta,seed34,packet,refinement,oracle,e,prepare,block-0,block-1,block-2,block-3,p1,task712,continuation の15件。各 item exact role,path,artifact,files,directories。artifact は run,attempt,head,workflow,id,name,bytes,sha256,repository_id,conclusion の既存10 key tuple。files は root 相対の file/bytes/sha256 を辞書順、directories は全相対dirを辞書順。元14親の既存 envelope root、accepted failure の prepare / four blocks もそのまま。外部の未収載 receiptへ出ない。

anchor exact keys は head,result,checker,owner,source,start,fixed,invocations,checker_prefix,completed_steps,rank,generation,kind,state_head,target_remainder_sha256,lambda_sha256,terminal。前七件は実 file descriptor（output/HEAD,output/result.json,checker-result.json,output/owner.json,output/source.json,output/start.json,output/fixed/manifest.json）。invocations は output/invocations の全実 file descriptor を file辞書順。checker_prefix exact steps,snapshots,steps_sha256,snapshots_sha256,invocations_sha256：前二件は64/64、後三件は実 C の該当 list 全体を canonical JSON+LFした hash。七 file、C全step/snapshot/invocation、実 n/rank/gen/head/target/lambda/terminal と source/runtime/旧parent全部を producer が実内容へ結ぶ。callerの status PASS 字段は受付に置かない。

code exact keys は producer,checker,producer_dependencies,checker_dependencies,data。前二件は新 P / 新 C の file descriptor、後三件は依存 file descriptor の file辞書順 list。P自系の登録closureを exact pinsと照合し、C側はroot配達の公開closure/pin rosterと実file hashだけを確認する（C算術sourceを読まない）。dataは両系の登録raw union。runtime exact python,numpy。

registration exact batch_size,max_batches,selection_policy,partial_policy,refill,producer_limits,checker_limits。値は32,1,CHORD_FIRST_ROSTER_32_THEN_FIRST_AUX,PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY,false。limitsは exact max_seconds,max_memory_mib、P5400/7168、C10800/7168。本走CLIの各宣言へ結ぶ。--resumeは登録値の変更を許さない。新三群selftestは別の metadata/線形fixture型、300/7168であり実親の成果を称さない。

## F4. 外側 root と保持 fixed の案

root payload は owner.json/source.json/start.json/parent-layout.json/fixed/manifest.json/selection/、candidates/、rows/、final/、progress/、invocations/ と、完成後だけ HEAD/result.json。協調停止は resource-stop.json と private progress のみで、公開 physical HEAD を途中作成しない。

parent-layout body：portable_acceptance_sha256,parents,anchor,code,runtime,registration。parents は受付から path だけ除いた全15件。source body：producer,retained_producer_dependencies,checker,retained_checker_dependencies,data,runtime,formula_id,retained_TCB_independence_reproved。最後の bool は false。owner body：formula_id,scope,parent_layout_sha256,source_sha256,portable_acceptance_sha256,registration。scope は vertices54432/edges108864/chords54433/legality_rows5/source_lower96776/physical_lower32260/physical48384/p1_rows8059/characters[0,1,2,3]/auxiliary_tests2/batch_size32/max_batches1。formula_id は v548-fixed-section;v547-signed-word;canonical-P1;four-B;batch-physical-reduction;single-final-separator。

start body：owner_sha256,source_sha256,parent_layout_sha256,anchor_head_sha256,anchor_result_sha256,anchor_checker_sha256,anchor_completed_steps,rank,generation,kind,state_head,target_remainder_sha256,previous_target_remainder_sha256,selection_lambda_sha256,original_rho2_packed_sha256,accepted_target_derivation_parents,anchor_pairing,anchor_pairing_rows,old_snapshot_numeric_replays,old_insert_numeric_replays,external_e_attached,registration。kind は Separator、最後の三countは0,0,1。旧親 list は深いcopy、旧/現targetと全旧行の直接dotを anchor_pairing へ保存し、rho2値1はDERIVEDのまま。

fixed/manifest body：owner_sha256,source_sha256,start_sha256,accepted_fixed_manifest,accepted_geometry_stage_sha256,files,fixed_values_independent_of_lambda。accepted_fixed_manifest は continuation役の output/fixed/manifest.json descriptor、files は同固定 root の全旧 payload descriptor（新 outputへ複写せず外部参照）。同8059 basis / mod54 /12 readers / geometry/carry/tau/Jを旧自系 L.FixedBundle で既存親の型として読んだ後、新outer固定manifestを結ぶ。旧 manifestを書き換えない。root相対fileは accepted_fixed_manifestの親directoryを基準にする。

selection/start.json body：owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,anchor_completed_steps,rank,generation,state_head,target_remainder_sha256,previous_target_remainder_sha256,selection_lambda_sha256,selection_policy,batch_size,max_batches。この先行 file の全hashを selection_start_sha256 とする。後で作る全oracle/roster完了 selection.json の hash は selection_sha256 と別。前の file は後のhashを含めない。

## F5. 共通 selection と phase manifest 案

selection/section と cochain の inner payload名/shape/旧数式JSONは凍結 L.registered_phase_roster/E.ORACLE_ROSTERS を保つ。tree は potential-f.u8[N],potential-tau.u8[N,5],chord-values.u8[54433],chord-tau.u8[54433,5],chord-residuals.u8[54433],selected-chords.u32[5],fit.u8[5] に、basis-tau.u8[5,5]（J順を行）、failed-indices.u32[failed_count],failed-edges.u32[failed_count],tree.json を置く。旧 single witness.json は tree へ置かず、候補ごとに別 witness を作る。

tree.json body：vertices,tree_edges,chords,independent_tau_columns,basis_chords,fit,aux_values,first_failed_index,first_failed_edge,residual_nonzero,full_chord_eof,selection_policy。数値は全54433を完了してから決まる。全tail検査前に32で打ち切らない。最初のmin32 failed indicesとedgeを選び、弦が全零の場合だけ最初の非零auxを一件、それも全零なら候補0件。

全 phase manifest body は共通：owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,selection_start_sha256,selection_sha256,candidate_ordinal,witness_sha256,phase,previous_phase_manifest_sha256,files,eof。selection側三phaseでは selection_sha256/candidate_ordinal/witness_sha256 は null。sectionのpreviousはnull、cochain/treeは直前phase全filehash。候補Eのphaseは raw/source/primal/p1/B/reduction の順で、rawのpreviousは oracle-view.json全hash、以後直前phase hash。候補側のselection_sha256は完成selection hash、ordinal/witnessは候補固有。JSONdescriptorは3key、binaryは5key。telemetry.jsonもfilesに含め、payload_bytesはtelemetry自身を除いたpayload bytes合計。

phase telemetry body：phase,elapsed_seconds,process_ru_maxrss_kib,proc_io_before,proc_io_after,payload_bytes,measurement_scope,eof。proc_ioはLinux /proc/self/io の rchar,wchar,read_bytes,write_bytes の普通整数、取得不能時のみnull。ru_maxrssはprocess累積peakでありphase増分RAMとは呼ばない。measurement_scopeは process-cumulative-rusage-and-proc-io;payload-bytes-are-output-only。P/Cの実時間一致は要求せず、Cが保存P測定の全bytesと型を認証して別のC実測を出す。

## F6. witness と selection の循環を避ける案

候補の ordinal は0始まり選定順。candidates/000000/witness.json body：owner_sha256,source_sha256,start_sha256,selection_start_sha256,ordinal,selection_policy,kind,roster_index,edge,coordinate,failed_chord,basis_chords,basis_coefficients,cycles,eta,tau,scalar,materialization。ここでは後の selection_sha256 を持たない。chordはcoordinate=null、roster_index/edge/failed_chordを実値、basis_chordsはJの5edge、basis_coefficientsは同J順d、cyclesは選定edge係数1の後にJの各係数-d mod3を5件、零係数も残す。eta=[0,0],tau=[0]*5,scalar=保存residualの1又は2。auxはroster_index/edge/failed_chord=null、coordinate=0又は1、basis_chords/basis_coefficients/cycles=[]、etaは標準基底、tau=[0]*5、scalar=同b_auxの非零。materialization=MATERIALIZATION_PENDING。

各witnessを先行 selection_start に結んで保存し、その後 selection/selection.json body：owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,selection_start_sha256,phase_manifests,selection_policy,batch_size,max_batches,refill,chords_checked,auxiliary_tests,failed_count,first_failed_index,first_failed_edge,failed_indices,failed_edges,selected_count,selected,aux_values,basis_chords,basis_tau,fit,terminal,eof。failed_indices/failed_edgesはtree相対のbinary descriptor、selectedは exact ordinal,kind,roster_index,edge,coordinate,scalar,witness のlistで witnessはroot相対descriptor。basis_tauは五rowのtrit list。terminalは VIOLATION_CANDIDATE または COMPLETE_ZERO_CANDIDATE。この file 全hashが selection_sha256 である。

候補 oracle-view.json body：owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,selection_start_sha256,selection_sha256,ordinal,witness_sha256,geometry_manifest_sha256,phase_manifests,anchor_state_head,selection_lambda_sha256,terminal。geometry_manifest_sha256は新fixed manifest hash、phase_manifestsは同section/cochain/tree三hash、terminal=VIOLATION_CANDIDATE。旧Eに渡す内部 view はこの新型を明示的に展開し、witness/q/kappa/f/b_auxを同selectionから与える。旧「先頭一件のoracle成功artifact」を他候補へ流用しない。

## F7. 候補別 E と実消去の案

raw/source/primal/p1/Bの各 inner payload と dtype/shape は凍結Lの同 phase rosterを保持し、新 outer manifestだけ前記型へする。同selection stateを E.four_B に渡す。one_physical_row / restore_physical / 行ごとのfresh separatorは呼ばない。raw源/P1の mutable parts は候補ごとにfresh。大配列は一候補完了後に解放する。

reduction phase は coefficients.u8[rank_before],physical-remainder.bin[48384],target-before.bin[48384],target-remainder.bin[48384],physical-literal.json,reduction.json,telemetry.json。独立時だけ physical-normalized.bin[48384],instruction.json,target.json を追加する。全係数を挿入順に保存し、physical-literalの消去factorも旧全row→新採用順で零powerを含める案とする（rootがC6のevent定義として確定する）。元source correction後の語を先頭、各row語の指数は -sr(coefficient)、最後の外powerは sr(sigma)。依存時はnormalized/lead/sigma/target_scalar/new_row/instructionをnullとし、物理零語を自由群identityと呼ばない。

reduction.json body：candidate_ordinal,selection_sha256,witness_sha256,selection_scalar,raw_pairing,remainder_pairing,subtracted_new_pairing,rank_before,generation_before,parent_state_head,target_before_sha256,coefficients_sha256,ordered_reductions,remainder_sha256,remainder_zero,outcome,lead,sigma,normalized_sha256,target_scalar,target_after_sha256,rank_after,generation_after,state_head,new_row_offset。ordered_reductionsは全basis順の exact row_id,source,lead,coefficient のlist、sourceは旧role/physicalfile/offsetまたは新rows local file、row_idはglobal0始まり。subtracted_new_pairing=sum(coeff*lambda_selection(new_normalized))、全旧row pairing0を前提とし raw_pairing - subtracted_new_pairing = remainder_pairing mod3を直接照合する。remainder_pairing=0でも独立なら採用する。

physical-literal body：candidate_ordinal,selection_sha256,witness_sha256,source_correction_sha256,p1_roots_sha256,physical_factors,outer_exponent,physical_lower_zero,source_lower_zero,normalized_word_available。physical_factorsは同ordered_reductionsを exact row_id/source/coefficient/exponent で表す。source_lower_zero=NOT_ASSERTED、physical_lower_zero=true。依存時 outer_exponent=null,normalized_word_available=false とし、外scale前の物理零recipeを保持する。target update receiptは旧 plain exact parent_remainder_sha256,remainder_sha256,scalar を保つ。

instructionは新 prefix+.physical-instruction の seal bodyに predecessor,offer,global_row_id,rank,generation,lead,sigma,physical_offset,local_row_offset,candidate_ordinal,selection_sha256,witness_sha256,physical_sha256,literal_sha256,target_sha256,target_scalar,coefficients_sha256,rolling_sha256 を持つ。rollingは sha256(bytes.fromhex(predecessor)+canonical(bodyからrolling_sha256を除く))、schema/外sealとは別。target correction は元rho2-current remainderで、追加 normalized語を +sr(theta) で右に積む情報を target_literal_factor={row_id,local_row_offset,coefficient,exponent,normalized_literal_sha256} として採用row manifestへ保持し、theta0も残す。

## F8. row/candidate/進捗/final の案

rowsは新local offset0から。rows/000000にはphysical-normalized.bin/instruction.json/target.json/manifest.jsonを置き、reduction phaseの同bytesと一致させる。row-manifest body：owner_sha256,source_sha256,start_sha256,selection_start_sha256,selection_sha256,local_row_offset,global_row_id,candidate_ordinal,predecessor_row_manifest_sha256,reduction_manifest_sha256,files,state_head,rank,generation,target_literal_factor,eof。row側から後で公開するcandidate manifestを参照せず循環を避ける。

candidate manifestをcandidate decisionの公開receiptとする。body：owner_sha256,source_sha256,start_sha256,selection_start_sha256,selection_sha256,ordinal,witness_sha256,oracle_view_sha256,phase_manifests,predecessor_candidate_manifest_sha256,outcome,row_manifest_sha256,accepted_new_rows_before,accepted_new_rows_after,rank_before,rank_after,generation_before,generation_after,parent_state_head,state_head,target_before_sha256,target_after_sha256,eof。DEPENDENTではrow_manifest=null、採用数/row chain/head/targetは不変。

progress/checkpoints/<全fileSHA>.jsonは新checkpoint seal。body：owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,selection_start_sha256,selection_sha256,predecessor_checkpoint_sha256,sequence,kind,processed_candidates,dependent_candidates,accepted_new_rows,rank,generation,reduction_state_head,target_remainder_sha256,current_lambda_sha256,current_candidate_ordinal,current_phase_manifests,last_candidate_manifest_sha256,last_row_manifest_sha256,selection_phase_manifests。kind=BatchReductionState/current_lambda=null。selection未完ならselection_sha=null、candidate未開始ならcurrent ordinal=null。完了prefixのpayload/hashからcountsを導き、callerからcountsを受け入れない。

progress/HEAD bodyは owner_sha256,source_sha256,start_sha256,checkpoint_sha256,sequence,kind,processed_candidates,dependent_candidates,accepted_new_rows,rank,generation,reduction_state_head,target_remainder_sha256,current_lambda_sha256。phase完成→manifest→candidate decision/row（消去段のみ）→checkpoint→progressHEADの列に協調停止を挟まない。HEADより一つ先の登録phaseだけ完全認証して回復し、builderを再呼出ししない。hole/飛び番号/別snapshot/未登録extraを拒否、.pending-<登録phase>-<32hex>と.orphan-<登録phase>-<32hex>だけ未完診断として保存する。phase未完の再作成は新pendingで行い、old pendingを数えない。

finalでは target-remainder.bin、Separatorの場合だけlambda.bin、separator.json、manifest.json。separator body：kind,selection_lambda_sha256,lambda_sha256,lambda_rho2,direct_pairing,anchor_pairing_rows,final_pairing_rows,new_lambda_oracle,source_lower_zero,physical_lower_zero。非零targetのfinalizerは最後に一回だけ全旧/新行dot0・batch初期/最終targetdot1を直接確認、rho2は旧target親列＋採用row差分のDERIVED。new_lambda_oracle=null、source_lower_zero=NOT_ASSERTED、physical_lower_zero=true。Linearではlambda/lambda_rho2/direct_pairingをnull、typed kind=LinearMembershipCandidate。初期COMPLETE_ZEROはselection lambdaを維持し新行なし。

final manifest body：owner_sha256,source_sha256,start_sha256,selection_start_sha256,selection_sha256,terminal,kind,anchor_completed_steps,selected_count,processed_candidates,dependent_candidates,accepted_new_rows,skipped_after_linear,rank,generation,state_head,target_remainder_sha256,lambda_sha256,last_candidate_manifest_sha256,last_row_manifest_sha256,files,eof。skipped_after_linearは未処理selected ordinal list、当該測定値はresultでnull。非空正常完走はaccepted_new_rows>=1、rank/generationはanchorから採用数のみ増す。

公開HEAD body：owner_sha256,source_sha256,start_sha256,selection_start_sha256,selection_sha256,final_manifest_sha256,terminal,kind,anchor_completed_steps,selected_count,processed_candidates,dependent_candidates,accepted_new_rows,rank,generation,state_head,target_remainder_sha256,lambda_sha256,new_lambda_oracle。完成final payload/manifestの後でのみHEADを書き、current kindはSeparator又はLinearMembershipCandidate。resultは同HEAD全文hash、前記counts/terminal/typed assurance、全候補測定/decision list、selection計測、final計測、入力不変、invocation全hashを記録する。result/ invocationの残る実測小keyはroot確定表に続けて公表する。

## F9. 実在 P API と現在の保存境界

L=d972_r07_complete_oracle_cegar_continuation_v1.py、E=d972_r07_selected_cycle_materializer_v1.py、O=d972_r07_section_cochain_oracle_v1.py、F=d972_r07_full_origin_refinement_v1.py、M=d972_r07_actual_root_seed_materializer_v3.py の自系凍結APIを静的に読んだ。L.own_dependencies/boot/attach_step は旧親のthin受領だけ、L.FixedBundle/CachedOracleは既受理固定資料と12 reader、L.current_section_cached / O.source_cochainはselection一回、treeは独自batch分類を新設する。候補Eの raw/source/primal/corrected/four_B と L.restore_raw/source/primal/corrected/B を利用する。物理消去はM.physical_reduce/normalize_pivot/update_targetの数値式を新batch型で呼び、one-rowの非零lambda残差gateは使わない。

いま保存したのは root監査用の公開ABI案だけである。sourceを次に段階保存し、Task997の共通確定と必要な型差分を反映する。新GHA、三群canary、本batch、全C照合は未実行。旧TCB共有は残り、新しい第三の独立算術を得たとは言わない。

## F10. root 追加指示への exact wire 補足案（Task997 確定待ち）

previous_target_remainder_sha256 と anchor の旧targetは、旧 continuation output/start.json が指す元 target（external E後の target）へ固定する。直近63段目のtargetではない。selection current は実64 HEAD target。親のlambdaで両者へ直接dot1を確認する。C10の「lambda四台」は物理lambdaの既登録四character blockの直接support / trit件数であり、final q を計算しない。final/q.binを作らず、new_lambda_oracle=null、finalのq/P1/section/cochain/treeは未計算のままとする。

schema suffix 完全表案は acceptance（六key plain）,parent-layout,source,owner,start,fixed-manifest,selection-start,phase-manifest,phase-telemetry,tree,witness-roster,witness,selection,oracle-view,physical-literal,reduction,physical-instruction,row-manifest,candidate-manifest,checkpoint,progress-head,separator,final-manifest,head,result,invocation,resource-stop,rejected,selftest,checker-result。前記plain acceptanceと三key target以外はprefixを付けた seal。旧inner section/cochain/raw/source/primal/p1/B JSON の各 schema は凍結旧型のままである。original target の plain 三keyには schema/sha256 を足さない。

ordered_reductions.source の exact tagged union は次の二型。古い各rowは実元normalized bytesの所在で、convenience copyへ付け替えない。単一fileを親全rosterで認証した上で offset/length/hash を bound し、packed EOFはlength12096。

- parent-row：kind="parent-row",role,file,file_bytes,file_sha256,offset,length,row_sha256。roleは実15親のいずれか、fileはそのroot相対。base physical.binは元fileの行offset、旧one-row physical-normalized.binはoffset0。他のschema/fileを推測しない。row_sha256はその正確な範囲。
- batch-row：kind="batch-row",local_row_offset,file,bytes,sha256,row_manifest_sha256。file="rows/"+6桁local+"/physical-normalized.bin"、bytes=12096、localは先採用rowだけ。root相対pathであり新candidate ordinalとは別。

両者を ordered_reductions の row_id,source,lead,coefficient へ入れる。global row_id は挿入順0始まり、全rank個を係数0も含める。physical_factors の各item exact row_id,source,coefficient,exponent で exponent=-sr(coefficient)。full old/new row vector と同順であり、pivot event非零だけを ancestryに縮めない。row_manifest_shaの参照は先行rowだけなので循環しない。

selection tree の完成数値を再走せず witness 外fileを回復するため、F5の tree rosterに witness-roster.json を追加する案。suffix .witness-roster のbody exact owner_sha256,source_sha256,start_sha256,selection_start_sha256,witnesses,eof。witnessesは選定順の完成 .witness sealed object全体。全d/tau/scalar/六cycle算術はtree builder内で完了し、このreceiptをtree payload/manifestへ保存する。tree manifest後の candidates/*/witness.jsonはこの保存objectの同canonical bytesを複写するだけである。selection.jsonはそのdescriptorを持ち、各oracle-viewもmetadataだけで作る。tree完成後のcrash回復でdを再計算しない。

checkpoint sequenceの exact規則案：

1. sequence=0 は immutable root/fixed/selection-start完成、selection_phase_manifests={}、selection_sha256=null、processed/accepted/dependent=0。
2. selection section後=1、cochain後=2。各selection_phase_manifestsは同順の完成prefix、current候補ordinal=null/current_phase_manifests={}。
3. tree payload/manifest→witnessコピー→selection.json→全選定oracle-viewを閉じた後=3。selection_sha256が初めて非nullになる。数値tree完成後に上記metadata列を回復できる。候補dirsは全selected個がwitness/viewだけの未処理殻として存在してよい。
4. 候補ordinal iのraw/source/primal/p1/B/reductionはp=1..6としsequence=3+6*i+p。p<=5はprocessed=i、current_candidate_ordinal=i、current_phase_manifestsがその候補の完成p-prefix。p=6はrow（独立時）とcandidate decisionを先に公開してprocessed=i+1、current ordinal=null/current phase={}、last candidate/row hashを更新する。
5. DEPENDENTも同じp=6のsequenceを進めるがaccepted/rank/generation/physical head/target/last_rowは不変。非空完走採用>=1を要求。
6. finalizerは新progress checkpointを数えず、private末尾sequence=3+6*processedを保ったまま final payload/manifest→公開HEAD→resultを協調停止なしで結ぶ。初期完全零はsequence3からfinalへ。Linearの未処理selected殻はwitness/viewだけで、phase/decisionを捏造しない。

progress HEADより前方に認めるのは直後の登録phase一つと、そのphaseに付随する未完metadata publication列だけ。例えばreduction p=6の全manifestが完成していれば、row/candidate/checkpoint/HEADを保存payloadから回復する。二phase先、穴、別selection/owner、未登録の通常名は拒否する。中断後も完了builderを再呼出し・二重採用しない。原子的file書込尾は登録basenameだけの .<basename>.pending-<32hex>。phaseの未完dirはその正確な親に .pending-<phase>-<32hex> または .orphan-<phase>-<32hex>、finalはroot直下 .pending-final-<32hex>、rowはrows直下 .pending-row-<6桁local>-<32hex>。いずれも診断として保存し通常countに数えず、その中のsymlinkは拒否する。

invocation body exact：id,portable_acceptance_sha256,acceptance_sha256,owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,selection_start_sha256,registration,resume,batch_size,max_batches,max_seconds,max_memory_mib,progress_head_before_sha256,physical_head_before_sha256,processed_candidates_before,accepted_new_rows_before,started_utc,launch,host_paths。idは32hex、invocations/<id>.json、開始時に一度書く。launchはexact run/attempt/head/workflow（GHAの実envから）で、host_pathsはexact parents/acceptance/output、parentsは15role→実絶対path辞書。実受付file SHAはhost pathを含むもの、portable hashはF2のpath除外版。resumeのbeforeは実HEADを読み、freshは両head hash=null/count0。新run/nonce/pathはこのreceiptに閉じ、owner/startへ混ぜない。

result は完成HEAD後だけ公開する。body exact：status,terminal,kind,owner_sha256,source_sha256,start_sha256,parent_layout_sha256,selection_start_sha256,selection_sha256,head_sha256,final_manifest_sha256,anchor_completed_steps,selected_count,processed_candidates,dependent_candidates,accepted_new_rows,skipped_after_linear,rank,generation,state_head,target_remainder_sha256,lambda_sha256,new_lambda_oracle,selection_readout,final_lambda_characters,candidates,selection_telemetry,final_telemetry,invocation_sha256,invocations,input_preservation,elapsed_seconds,old_snapshot_numeric_replays,old_insert_numeric_replays,old_success_suites,positive_readout,grade2_member,grade2_nonmember,full_A0,candidate,cross_checked,verified。status=PASS、old三count0、new_lambda_oracle=null、grade2二件NOT_DECIDED、full_A0/cross_checked/verified=false。positive_readoutはLinearでTASK958_PENDING、それ以外NOT_APPLICABLE。candidate=trueは新completed packetの意味だけ。

selection_readout exact：failed_count,first_failed_index,first_failed_edge,failed_indices,failed_edges,q_characters,lambda_characters,aux_values,score_support,kappa_support,p1_equation_residual_support。failed二列は全tree binary descriptor、q_charactersは既計算qの四row、lambda_charactersは同selection physical lambdaの四block。character receipt exact character,offset,trits,support,trit_counts、counts=[n0,n1,n2]。qは各36288、lambdaは物理48384の四登録block各12096。final_lambda_charactersは同型四件、Linearだけnull。final qは無い。

candidatesはselected_count長のlist、各item exact ordinal,kind,witness_sha256,selection_scalar,outcome,candidate_manifest_sha256,row_manifest_sha256,lead,sigma,target_scalar,rank_before,rank_after,generation_before,generation_after,phase_telemetry,raw_readout。processedのoutcomeはINDEPENDENT又はDEPENDENT、未処理tailはSKIPPED_AFTER_LINEARでwitness/selection scalar以外のdecision値とraw_readoutをnull、phase_telemetryは全6phaseキーで全部null。processedのphase_telemetryはraw/source/primal/p1/B/reductionをkeyとする各telemetry.json root相対descriptor。DEPENDENTのlead/sigma/target_scalar/row_manifestはnull。raw_readout exact epsilon_unrepaired,omega_unrepaired,repair_exponents,raw_slp_letters,source_homogeneous_scalar,section_scalar,selection_scalar,alpha_support。epsilonはordinary integer二件、omegaは0..2、repair_exponentsはchordで三ordinary integer（中央はsigned0/1/-1）、auxでnull。各実値は同raw/S/P1 receiptから読む。

selection_telemetryはsection/cochain/treeをkeyとする各telemetry descriptor、final_telemetryはfinal/telemetry.json descriptor。final rosterへこのtelemetry.jsonだけ追加し、phase=finalの .phase-telemetry とする。payload_bytesは同telemetryを除いたfinal payload bytes。final計測と入力I/O/output bytes/RSSを混同しない。invocationsは開始receipt全file descriptorのfile辞書順、invocation_sha256は今回の一件を指す。

input_preservation exact parents_before_sha256,parents_after_sha256,code_before_sha256,code_after_sha256,portable_acceptance_sha256,acceptance_sha256,all_parent_files_and_directories_unchanged,all_code_and_raw_unchanged,acceptance_unchanged。この4 inventoryは新outputの inputs/{parents-before,parents-after,code-before,code-after}.json に plain canonical JSONとして置く案。parents entriesはhost pathを除く15role/全files/dirs、codeは登録file descriptor全union。比較flags三件が全trueでないと完成resultは作らない。新output配置F4へ inputs/ を追加する（旧入力を変更する意味ではない）。

resource-stop body exact status,terminal,phase,reason,partial,owner_sha256,source_sha256,start_sha256,selection_start_sha256,selection_sha256,invocation_sha256,progress_head_sha256,checkpoint_sha256,public_head_sha256,final_manifest_sha256,processed_candidates,dependent_candidates,accepted_new_rows,rank,generation,max_seconds,max_memory_mib,elapsed_seconds,candidate,cross_checked,verified。status/terminal=UNKNOWN_RESOURCE、partial=true/candidate=false。起動前欠品はbinding/counts=nullで、実保存されていないrankを示さない。private progressがあればその全hash/型/countへ結ぶ。final HEADが既に完成しているI/O等の中断は実public_head/final pinを保持し、完成physicalをprivateと偽装しない。通常協調停止はfinal publication列の前まで。rejectedは同bodyでstatus=FAIL/terminal=REJECTED、exit1。resourceはexit3。完成resultが無いことと、完成physical HEADの有無は別字段である。

selftest body exact status,tests,fixture_scope,production_interfaces_used,old_success_suites,actual_anchor_arithmetic_replayed,candidate,cross_checked,verified。testsはname/status/rejected_casesの三要素で、nameは fixed-selection-full-roster-and-aux,dependent-independent-target-signs-and-packed,private-prefix-publication-resume-and-isolation。old_success_suites=0/actual_anchor_arithmetic_replayed=false/candidate=false。本番helperとの接続と各逆対照は実装中に具体化し、実行はGHAだけ。

checker-result公開案（995 sourceを読まない）：body exact status,partial,terminal,owner_sha256,source_sha256,start_sha256,selection_start_sha256,selection_sha256,progress_head_sha256,public_head_sha256,producer_result_sha256,final_manifest_sha256,anchor_completed_steps,selected_count,processed_candidates,dependent_candidates,accepted_new_rows,rank,generation,state_head,target_remainder_sha256,lambda_sha256,selection_phases_compared,candidate_phases_compared,candidate_decisions_compared,accepted_rows_compared,all_completed_payloads_and_json_compared,public_final_compared,old_snapshot_numeric_replays,old_insert_numeric_replays,old_success_suites,checker_source,runtime,elapsed_seconds,input_preservation,grade2_member,grade2_nonmember,full_A0,candidate,cross_checked,verified。candidate_phases_compared各item exact ordinal,phases、phasesは完成phase名prefix。selection_phases_comparedも完成prefix。privateだけのPASSはpartial=true/candidate=false/public_final_compared=false、公開final全比較PASSだけpartial=false/candidate=true。未形成binding/count値はnull。資源UNKNOWN_RESOURCE/不一致FAILは未比較範囲を全比較済みとしない。checker_sourceは自身file descriptor、runtimeは自身python/numpy。root/995がこの公開案を共通表へ確定し、必要差分は表だけ戻す。

## F11. Task997 全文読了と現在の実装境界

root確定 Task997（36485 B / bfd181b7f31c5baa789abf6596325d5b4597e92a8f44c0c1eee2cb58a4b2db78）を全文読了した。R1の12項を優先し、前記「案」「確定待ち」は解消する。Linearのpositive_readoutは NEW_BATCH_SAME_WORD_ADAPTER_PENDING に置換する。全files/directoriesは相対POSIX pathの完全な文字列順で整列する。selection/final lambda四台の区別、previous_target=元1386 start target、全係数/零literal factor、私的prefix/公開finalの区別は997通りである。

新P sourceは現在563行、定数/codec/計測・public基礎に加え、全roster分類 classify_batch/current_batch_tree、可変historyのdeepcopy make_reduction_state、旧selectionと消去残差を分離する reduce_candidate_numeric、依存/採用の二cursor advance_reduction_numeric、最後の一回separator final_separator_numeric、四character support/trit countsまで保存した。これらはsource記述だけでローカル数値/AST/import未実行。初期inventoryも997 R1.3通り最終relative文字列で再整列する。まだ薄い実親loader / phase store / publication / recovery / CLI / canary / source freezeは未完成である。

rootの優先指示により、この保存境界からTask998のWF-only v3整列修理を先に行い、その完成後に994へ戻る。994はキャンセルしない。991の凍結済みP/WF/返信は変更しない。

## F12. 1000–1002 公開追補と再開後の保存境界

Task1000（5929 B / f262bc3cfd5f40809ddf5b71e3f6ebd91a4a2e0534dfc309a33ff90932ecbc6c）、Task1001（3515 B / 2f8dc3941c8dc1df5e0cb62b7a8075159c83e0a7cf66bdc7a015341fec3145c9）、Task1002（5490 B / 68f7e854f90fa9e4692bad03f09fceaabbc096fb1cd4a9e94a03c703b58b61e0）を全文読了した。相手sourceや返信は読まない。direct pairingのfive-key/rows整数、全97旧target親、全kappa tag/八aux、採用rowの列挙10key、旧fixed JSON五key認証後の新三key射影を採用する。rootが以前述べた十一keyは数え違いとの訂正を受領し、新keyは足さない。

入力inventoryは15role順のplain list、code/dataは全unionを相対file文字列順のplain listとする。Task1001のchecker durable-tail scopeは公開prefix countを進めない別記録であり、P側phase sequenceを変えない。failed-indices/edges descriptorの基準はselection/tree/で、file値はbasename。witnessはroot相対、phase内部descriptorは当該phase directory相対。

Task998は108358 B / 04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604で凍結し、994へ戻った。新sourceには strict actual acceptance（15tuple/30実entry/旧全C prefix/原start int1/full runtime）、Task1002のP9/C10/raw3 exact pins、旧64 thin loader、全1450元rowへの実所在receipt、新owner/source/start/fixed/selection-start、typed BatchPhaseStore、全tree/witness保存とmetadata回復、全係数のliteral/target符号/依存分岐、row/candidate publicationまで保存した。旧snapshot/Eのbuilder、旧full oracle、旧one-row separator wrapperは呼ばない。保存treeからdを再solveせず、保存係数のtau/scalar identityだけを確認してwitness/viewを回復する。

ここは未凍結の進行票であり、本sourceの私的checkpoint/HEAD orchestration・最終packet/計測・CLI・三群canaryはまだ未完成。全数値/import/ASTは未実行、未観測のbatch terminal/rank/速度/採用数を予想しない。公開後の旧source/WF/返信は不変。

## F13. 最終実装と 1003 / 1004 / 1011 の確定

F9・F11・F12 は各保存時点の進行記録である。現在は新 P の入場、旧64のthin受領、全selection、候補別E、依存/採用、私的checkpoint、復旧、final/HEAD/result、資源診断、CLI、新三群canaryまで実装を完了した。先行案の解釈は997および1000–1004/1011を優先する。

追加の全文読了資料は次の通りである。

| 公開契約 | bytes | SHA256 |
|---|---:|---|
| sol/luna_task_1003_r07_batch_final_public_field_types_v1.md | 1367 | 5d494eded07e22b34fde010d1bfdc7823be36f3f19f21b8dbf3770b2f2e60a91 |
| sol/luna_task_1004_r07_batch_completed_resume_contract_v1.md | 1381 | 39abfd307935082426ceeaf36c53eec6d6d9c0594e7733bba02d9075a76fc978 |
| sol/luna_task_1011_r07_batch_bootstrap_and_diagnostic_names_v1.md | 4774 | a26e11e6c937aebddd33829982144750ec7029ef9039b13ed8054d2908d7687f |

1003のlaunch run/attemptはboolを除く正の普通整数、headは40桁lower hex、workflowは .github/workflows/d972-r07-fixed-lambda-cycle-batch-v1.yml。host_pathsはexact parents/acceptance/output、parentsは15role→実絶対path。これらと実受付全hashはinvocationにだけ入り、portable identityへ混ぜない。新physical instructionのtarget_sha256はplain三key target.jsonの全file hashで、packed targetのremainder_sha256と区別する。

1004の完成済再受付は、全入力・全保存prefix・final・実HEAD/result・全invocation・入力不変を認証して既存result bytesを返す。新invocation/resultを作らず、旧elapsedを新計測としない。全照合済のread-only再受付フラグを置き、その後のdeadlineやstdout例外でも元packetへ診断を書かない。完了ログは停止判定を持たない。HEADだけ/resultだけの保存tailはこの完成分岐に入れず、未完成再開として保存finalからmetadataを補う。

1011に従い、通常resume=false receiptは高々1件。通常receiptがある場合、fresh1件か、resume=true・両before HEAD null・strict count0のbootstrapが1件以上ある履歴だけを受ける。複数bootstrapを許し、nonceや時刻順から履歴を推測しない。通常receipt0件は実progress HEAD/checkpoint/phase未形成時だけ。旧host_pathsから受付全体を再構成して各acceptance_sha256も照合する。before progressはHEAD以内の認証済みcheckpoint歴史、before physicalは実在するoutput/HEADの全file hashであり、durable finalだけから仮HEADを合成しない。

診断名はresource-stop.jsonとrejected.jsonの二本で、各schema/status/terminalを1011の表へ固定する。両方あれば両方を全文照合し、早期nullを後から埋めない。非nullのowner/source/start/selection-start/selection/invocation/checkpoint/count/final/public HEADは実保存fileと結ぶ。資源・停止診断はcandidate/cross_checked/verified=false。どちらかの診断名だけで完成terminalを決めず、完成packetのterminalは全finalから得る。

## F14. 最終 source の経路・保存境界

入口のoutput_path_gateは、mkdirとOUTPUT_CREATED設定より先に全15親との両方向の包含を拒否し、受付file・登録code/rawを含む出力先も拒否する。不正な--outputへの早期失敗を親やcodeへのrejected.json書込みに変えない。正しい別outputの早期診断保存は維持する。その後のauthenticate_acceptanceは実全files/directories、30固定entry、旧全C64 metadata、原startのint1、全runtime/closure/事前登録を照合する。

thin_anchorは旧P971の原1386 startを再命名せず、保存64のnormalized rows・全phase/step metadataを挿入順に受ける。旧oracle/E/挿入のbuilderは呼ばない。今回のselection lambdaについて全1450行へdot0、原1386 start targetと現64 targetへdot1を直接確認する。元rho2は97本の保存target identityを明示するDERIVEDである。

selectionはL.current_section_cached、O.source_cochain、新current_batch_tree/classify_batchへ接続する。全8059/54433/2auxを閉じてから、先頭min32失敗弦、弦全零時の先頭非零aux、両者全零を分類する。全失敗列と全六cycleの零係数を保持する。各候補のraw/source/primal/P1/four-Bは自系凍結Eの同算術と新候補viewを用い、selection lambdaを更新しない。新reduce_candidate_numericが全旧/先採用行の挿入順消去を行い、依存と独立を全48384で分ける。lambda_selection(remainder)=0でも独立行を採用する。

load_private_prefixは全通常file・typed phase roster・checkpoint系列を読み、HEADより直後の一phaseだけを許す。publish_selectionとpublish_candidate_decisionには純粋なdocuments収集モードを設け、全prefix/通常rosterの認証前に欠品metadataを書かない。保存section/cochain/treeやEのbuilderを再呼出しせず、保存payloadと係数identityから復元する。未完metadataは認証後のrecover_private_metadataだけで補い、row/candidate/checkpoint/HEADを二重採用しない。数値・payloadの大配列は一候補単位で保持し、32候補分を常駐させない。

途中はBatchReductionState/current lambda=nullとprogress/HEADだけで、公開physical HEADを作らない。最後に全選定候補を処理してから新separatorを一回構成し、全旧/新rowとbatch開始/最終targetを直接照合する。途中で実targetが零ならLinear、残りのselected殻はSKIPPED_AFTER_LINEARで各E測定はnull。初期COMPLETE_ZEROだけは元selection lambdaを継承する。final/qや新lambdaのoracleは作らずnew_lambda_oracle=null。Linearのpositive_readoutはNEW_BATCH_SAME_WORD_ADAPTER_PENDINGである。

全入力のafter inventoryを実照合した後、final payload/telemetry/manifestをdurableにしてから公開HEAD→resultを結ぶ。この列に協調停止を挟まない。保存finalの復元ではseparatorを再solveせず、全payloadと直接pairingを認証する。二種のphase pending、rowsのlocal pending、final pending、登録basenameのatomic pendingは限定した親directoryでだけ保持し、symlinkと未知通常名を拒否する。特に未形成nonceのinvocation atomic fileをglobal rosterでも診断として受け、通常receipt件数には加えない。

独立監査996の指摘により、公開前にnested witnessのbool、未形成invocation atomic名、認証済read-only再受付後の診断書込み、出力先分離の実行順、未commit checkpointのbefore履歴、未形成public HEADの仮hashを修理した。いずれも新source内の型/保存/受付境界で、旧凍結sourceや新batchの数学scopeを変更していない。

## F15. 公開 CLI と新三群

本走引数はstate/delta/seed34/packet/refinement/oracle/e/prepare/p1/task712各--*-root、--block-root四件、--continuation-root、--acceptance、--output、--batch-size 32、--max-seconds 5400、--max-memory-mib 7168。--resumeは同portable入力・同登録policyの保存prefixだけに使える。max_batches=1/refill=falseは固定で、新しい可変cap引数を足さない。初回1009はfresh一回であり、自動resumeや96親への差替えはしない。

新canaryの公開呼出しは次である。ここでは実行していない。

```text
python -B search/d972_r07_fixed_lambda_cycle_batch_v1.py --selftest --max-seconds 300 --max-memory-mib 7168
```

selftest bodyは997のexact型を保つ。fixture_scopeは非空str、production_interfaces_usedは非空str list、tests各項はname/status/rejected_cases、最後は非空str list。三nameと実接続は次の通りである。

| name | 本番 helper へ接続した対照 |
|---|---|
| fixed-selection-full-roster-and-aux | 全長54433の合成roster、32を越えた失敗列保持、末尾だけの違反、弦優先、aux-only、完全零、全六factorと零係数。saved_selection_valuesへ完全reseal後の別selection-start/bool ordinal/cycle/aux coordinate/etaとEOF欠損を渡す。 |
| dependent-independent-target-signs-and-packed | reduce_candidate_numeric/reduction_payloads/restore_reductionで実合成消去。DEPENDENT、selection残差pairing零のINDEPENDENT、sigma2/theta2の両符号、SeparatorとLinear、全因子、base3 byte80、u32 sentinel、packed短長EOF/byte81/非零padding/bool拒否。 |
| private-prefix-publication-resume-and-isolation | 実load_private_prefix/recover_private_metadataの合成bootstrap、保存reductionのbuilder未呼出し、同decision再受付のbytes不変、深い親list隔離、row/final→HEADの順、HEADだけの完成再受付拒否、完全reseal/hole/二phase先/cap reset拒否。1011の0fresh bootstrap・複数bootstrap・2fresh/bool/host hash拒否、二診断全結合、未形成nonceを含む実roster、未知名/symlink拒否、read-only例外時不変、出力先包含5拒否も同helperへ接続する。 |

これらは合成cochain/小さいphysical span/metadata fixtureであり、実Omega、実rank1450、実原14親の算術成果を称さない。old_success_suites=0、actual_anchor_arithmetic_replayed=false、candidate/cross_checked/verified=false。三群の実PASS、AST、初回batch、独立Cの全比較はGHAでのみ判定する。

Pの正常完成はsealed resultの全bytesをstdoutへ出しexit0。資源上限や協調停止はUNKNOWN_RESOURCE/exit3、型・算術不一致はREJECTED/exit1で、保存されたprivate prefixだけを記録する。登録P5400秒/C10800秒/7168MiBとselftest300秒は上限であって速度予測ではない。実測秒、process累積ru_maxrss、proc_io前後、出力payload bytesを区別して保持する。

## F16. 最終 source と保持 closure の凍結

新P sourceは次の実bytesで凍結する。PowerShellによるmetadata/hashとsource全文静的読取だけを行い、ローカルPython/import/AST/GAP/数値、network/git/credentials、新agentは実行していない。

| file | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_fixed_lambda_cycle_batch_v1.py | 213861 | 229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591 |

ASCII互換UTF-8、LF3463、CR0、BOMなし、final LFあり、行末空白0。996はこのsource hashの全既読core・新tail・通知修理に追加必須source指摘なしと通知しており、最終返信末節の読了票を別途残す。rootへ同pinとCLI/三nameを通知済みである。

Task1002の保持P9/C10/raw3の全22実fileを再hashし、下表の全bytes/SHAと一致した。C欄はroot配達公開pinとfile hashだけであり、新C source/返信もC算術helperも読んでいない。新C自身の最終pinはroot/995が別に確定し、1009のacceptanceへ入れる。このPのcode入場はその新C全descriptorも実hashへ結ぶが、その本文を算術依存としてimportしない。

| 区分 | file | bytes | SHA256 |
|---|---|---:|---|
| P保持 | search/d972_r07_actual_grade2_root_scalar_batch_v2.py | 118315 | 3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856 |
| P保持 | search/d972_r07_actual_root_seed_materializer_v3.py | 86643 | 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332 |
| P保持 | search/d972_r07_complete_oracle_cegar_continuation_v1.py | 126940 | 67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c |
| P保持 | search/d972_r07_fixed_root_packet_loop_v2.py | 84173 | e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6 |
| P保持 | search/d972_r07_full_origin_refinement_v1.py | 97806 | d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa |
| P保持 | search/d972_r07_rank1355_root_seed_scalars_v1.py | 31578 | 973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb |
| P保持 | search/d972_r07_section_cochain_oracle_v1.py | 73290 | 4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb |
| P保持 | search/d972_r07_selected_cycle_materializer_v1.py | 88929 | 4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3 |
| P保持 | search/d972_r07_targeted_grade2_owner_generated_join_v15.py | 126565 | 76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632 |
| C公開pin | search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py | 119619 | e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6 |
| C公開pin | search/check_d972_r07_actual_root_seed_materializer_v3.py | 64626 | eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701 |
| C公開pin | search/check_d972_r07_complete_oracle_cegar_continuation_v2.py | 129557 | e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3 |
| C公開pin | search/check_d972_r07_fixed_root_packet_loop_v2.py | 66251 | 5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5 |
| C公開pin | search/check_d972_r07_full_origin_refinement_v1.py | 75083 | 1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2 |
| C公開pin | search/check_d972_r07_rank1355_root_seed_scalars_v1.py | 36236 | f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62 |
| C公開pin | search/check_d972_r07_section_cochain_oracle_v1.py | 80740 | 2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967 |
| C公開pin | search/check_d972_r07_section_cochain_oracle_v2.py | 84402 | a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d |
| C公開pin | search/check_d972_r07_selected_cycle_materializer_v1.py | 103757 | a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4 |
| C公開pin | search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py | 141770 | 8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662 |
| raw | scratchpad/a0_paper_words_v1.json | 115928 | 90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893 |
| raw | scratchpad/a0_v2_words.json | 106133 | fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612 |
| raw | scratchpad/fuda1_a0_rmax_data.g | 4709 | 625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba |

## F17. 完成の射程と残る実走

Task994の指定二file内の実装・公開ABI・静的自己読取を完了した。途中の994保留中に別便で行った正語修理source/WF/返信を、この凍結作業で再変更していない。Task1005の公刊候補や後続正語runの失敗は本batchの結果として扱わない。

今回の登録親は実64/rank1450/gen8155/Separator/UNKNOWN_CAPのままで、正式96の観測を入力へ流用しない。新batchのselected/dependent/accepted/target/terminal/rank/gen/elapsedは全て未観測。非空batchの採用数32、rank増分32、失敗弦改善、速度比を予告しない。保持TCBの共有と旧独立性の限定は残り、新runで旧scopeを遡及して閉じたとはしない。

残るのはrootによる新C/1009/監査票の最終受付と、GHA上の新三群・全本走・全C比較、その実候補のscopeに対する裁定である。Pのcandidateは機械出力候補に限り、grade2_member/grade2_nonmemberはNOT_DECIDED、full_A0/cross_checked/verified=falseを維持する。公開後の本source/返信は不変とし、根拠ある修理が必要ならrootへ先に連絡する。

AUDIT_994_VERDICT: P_SOURCE_COMPLETE_STATIC_ONLY_RUNTIME_PENDING
