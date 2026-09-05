# Task997 — 固定lambda batch v1・root確定の公開 wire

宛先: Task994 P / Task995 C / Task996 独立監査。Task994 C1–C10を保持し、下記を共通 ABI として採用する。
rootが994から受領した公開data/schema表だけを全文監査して再掲した。著者の算術source/私的API/実装手順は中継しない。
995は994返信や新P sourceを読む必要も許可もない。各著者は自系の保持TCBと自分の実装だけを使う。
本便は新sourceの実装契約であり、GHA/新rank/完全照合/grade2の成功宣言ではない。

## R1. rootの採用・優先する明確化

1. 下記公開F2–F8/F10の「案」「root確定待ち」は本便で解消する。下記の明確化と競合しない全exact keyを採用する。
   凍結後のABI追加/変更は次の新便で両作者へ配達し、本便を上書きしない。公開partial_policyは PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY。
2. acceptanceは六top keyだけのplain canonical JSON、artifact.sha256は実APIと同じ sha256:＋64lower hex。
   file/row/内seal/全file hashは接頭辞なし64lower hex。整数字段はbool/floatを拒否。実測秒だけ有限非負numberを許す。
   parentsとartifactの実run/conclusionは既登録15tuple通り。prepare/four blocksの承認済みfailureをsuccessへ書き換えない。
3. 全filesリストは完全な相対POSIX path文字列を基準に一度整列する。directoriesも同じ文字列順。
   Path component順やホストlocale順で代用しない。各body/filesのexact keys/全bytes/全EOFは維持する。
4. previous_targetは旧continuation output/start.jsonの実target（外部E後の1386 start）で、currentは実64 HEAD target。
   新selection lambdaで両targetへdirect dot1と全旧rank1450行dot0。新finalizerの両targetはbatch開始currentとbatch最終target。
   rho2の1は旧/新全target identityをたどるDERIVED。実計算していない旧oracle/Eを再実行済みと呼ばない。
5. coefficientsとordered_reductionsは全basis挿入順、係数0も保持する。physical_factorsも同全列で−sr(coefficient)。
   normalized外powerはsr(sigma)、数値target更新は−theta、correction語追加因子は+sr(theta)。零powerと全祖先を落とさない。
6. selection_start_sha256は先行、selection_sha256は全tree/witness完了後。witness-roster.jsonの追加を採用する。
   selectionのwitness/view殻は全selected分を持ち、Linearの未処理殻はSKIPPED_AFTER_LINEAR、E測定/decisionはnull。
7. schema suffix表、親/新rowのtagged source、sequence規則、実限定basenameのatomic pending語法はF10通り採用する。
   .<basename>.pending-<32hex>のbasenameはその正確なdirectoryで登録された通常payload/manifest/HEAD名だけ。
   phase/row/final pendingも正確なscopeでだけ許し、全保存・symlink拒否・通常完成count除外を保つ。
8. lambda四台は48384の四既登録character block（各12096）のsupport/trit件数。selection qの四台は既計算qから別採取。
   final/q.binは追加しない。final lambdaのq/P1/section/cochain/treeは未計算。new_lambda_oracle=nullを保つ。
   COMPLETE_ZERO_CANDIDATEは新lambdaを作らずselection lambdaと全zero oracleを継承し、未計算の新oracle成功とは呼ばない。
9. final/telemetry.jsonとinputs/{parents-before,parents-after,code-before,code-after}.jsonを採用。
   complete resultのinput flagsは実前後比較で全部trueだけ。resumeで保存済みimmutable前提を黙って置換しない。
   telemetryの実測値は型/全bytesを認証し、P/C秒やprocess peakの数値一致を要求しない。
10. result.positive_readoutはLinear時 NEW_BATCH_SAME_WORD_ADAPTER_PENDING、それ以外NOT_APPLICABLE。
    下記の旧呼称TASK958_PENDINGはこの値へ置換する。batch物理行のpositive adapterは別委嘱が必要で、本便には含まれない。
11. Pのcandidate=trueはcompleted packetだけ。Cのcross_checked=trueは実際に全比較した明示scopeだけに使い、
    metadataだけのprefix/未読payloadではfalse。C partial=trueのPASSを完成physical stateへ昇格しない。
    CのFAIL/UNKNOWN_RESOURCEは未比較範囲をtrueにしない。grade2二字段NOT_DECIDED、full_A0/verified=falseは全型で保持。
12. rootは実受付/新P・C/closure/raw/runtimeの最終pinsをGHA前に確定する。相手の算術sourceを読んでABIを合わせない。
    これから見つかる公開keyの曖昧さは具体的なfield/型/根拠だけrootへ戻す。完成源は公開後不変・修理は新版。

## R2. 採用した公開data/schema表

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
