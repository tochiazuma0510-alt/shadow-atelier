# Task965 — selected cycle / auxiliary の一行 consumer

指定 producer を完成し、成功した oracle checker completion の実 entry pins を接続して source を凍結した。Task959 source/reply を凍結して root の開始連絡を受け、Task965、正式 reply963、reply957 E、v547/v548、reply958、Task959 の公開 ABI を全文読んだ。以下は Task966 と先に共有した公開契約と最終実装記録であり、新算術 helper は共有していない。Task965 自身のローカル AST・import・数値実行はゼロ。本走と独立照合は root broker の GHA 待ちであり、新 target の変化や終端を予測しない。

## 公開 ABI v1 — CLI・封・出力配列

schema prefix は `d972.r07.selected-cycle-materializer.v1`。JSON は ASCII / sorted keys / compact separators / 末尾 LF。`seal(kind,body)` は schema を加え、sha256 フィールド自身だけを除いた canonical bytes の SHA256 を sha256 に持つ。file reference は seal を含む全 bytes の SHA。trit は0..2、packed3 は4 trits/byte、重み1,3,9,27、全配列 C-order。

CLI は Task959 の十二 parent roots `--state-root --delta-root --seed34-root --packet-root --refinement-root --prepare-root --block-root`（四回）`--p1-root --task712-root` に `--oracle-root` を追加し、fresh `--output` と `--max-seconds`（default1800）を取る。`--selftest` は parent 不要。`--parent-layout-selftest` は state/delta/seed34/packet/refinement/oracle の六 rootsだけ。単一 snapshot・一行だけであり resume loop はない。deadline は exit3 / `UNKNOWN_RESOURCE` diagnostic とし、未完出力を完成 manifest/HEAD にしない。

oracle が実受理済み `COMPLETE_ZERO_CANDIDATE` なら E の source/P1/B/physical算術を開始せず、`status:NOT_APPLICABLE,terminal:NOT_APPLICABLE,oracle_terminal:COMPLETE_ZERO_CANDIDATE,physical_appends:0` を出す。`VIOLATION_CANDIDATE` だけを E の入力とする。成功した一行は `status:PASS`、target非零なら terminal `PIVOT_CANDIDATE`、target零なら `LINEAR_MEMBERSHIP_CANDIDATE`。後者の Task958 positive gate は pending。どちらも `candidate:true,cross_checked:false,verified:false`。

本走は以下の flat payload roster を使う。runtime `telemetry.json` は同じ file manifest に認証するが、双方の実時間そのものを一致条件にはしない。全算術 array と typed receipt は独立再計算して比較する。

| basename | dtype / shape / 契約 |
|---|---|
| `owner.json`, `start.json`, `source.json` | json、exact current prefix/oracle/runtimeの親 |
| `raw-word.json` | json、下記 typed raw SLP と各 node の整数/endpoint receipt |
| `raw-chain.bin` | packed3 / [108864]、edge ID=2*q+slot |
| `raw-source-d0.bin` | packed3 / [4,6048] |
| `raw-source-d1.bin` | packed3 / [4,18144] |
| `raw-source-d2.bin` | packed3 / [4,36288] |
| `raw-source-aux.bin` | packed3 / [8]、最後二成分は同じ legal raw root の eta |
| `raw-source.json` | json、全六tagの同一raw SLP直接Foxとchain routeの一致、raw scalar、EOF |
| `p1-coefficients.u8` | u8 / [8059]、canonical ID順 |
| `p1-reductions.json` | json、old embedded元lead昇順→new owner-major元lead昇順の nonzero events |
| `p1-roots.json` | json、accepted index の selected roots / exact positioned instructions / component pins |
| `p1-exponent-residues.json` | json、全8059 canonical wordの同じliteral exponent pair mod54、各0..53 |
| `source-lower-remainder.bin` | packed3 / [96776]、全零 |
| `source-top-corrected.bin` | packed3 / [4,36288]、同じalphaを四topから引く |
| `source-correction.json` | json、V_wordのordered P1 refsとsource-lower零、exponent mod54から18整除とnormalized pair |
| `physical-by-character.bin` | packed3 / [4,48384]、各Bのprimal値 |
| `physical-raw.bin`, `physical-remainder.bin`, `physical-normalized.bin` | packed3 / [48384] |
| `physical-literal.json` | json、V_wordと全ordered old physical refsを結ぶtyped normalized ancestry |
| `instruction.json` | rolling hash付き一行instruction、generic sha256 sealは付けない |
| `target-remainder.bin` | packed3 / [48384] |
| `lambda.bin` | packed3 / [48384]、target非零時のみ |
| `telemetry.json`, `result.json`, `manifest.json`, `HEAD` | json、下記stage/終端/耐久契約 |

## 公開 ABI v1 — raw SLP と literal 順序

SLP node は `id`（文字列）と `op` を持つ plain object。grammar は `Identity`、`Letter{letter}`、`Ref{namespace,key}`、`OrderedProduct{factors:[id...]}`、`Inverse{node:id}`、`IntegerPower{node:id,exponent:integer}`。trit2のword代表はinverse、整数冪はmod3へ落とさない。

raw-word の nodes は次の順番を固定する。先頭は `identity`、`x`、`y`。次に保存 witness cycles の順（failed、その後基準5）で、各 i=0..5 に `tail-i` / `head-i`（Ref namespace=`oracle-tree`, key=vertex）、`head-inverse-i`、`cycle-i`（tail / xまたはy / head-inverse のOrderedProduct）、`cycle-power-i`（IntegerPower、signed代表0/1/-1）を作る。0係数の六項も削除しない。次に `w` は全 cycle-power のOrderedProduct（aux時は空）とする。tree Ref は geometry の同じ parent/parent-edge/BFS の有限 path を表す。最初に shared Refへ畳み込んだり edge ID順へsortしない。

次に `r-x` / `r-y`（Ref namespace=`normalizer-v459`, key=`r_x` / `r_y`）、`r-x-cube` / `r-y-cube`（IntegerPower3）、`r-x-inverse` / `r-y-inverse`、`commutator`（二inverse、r-x、r-yの順）を置く。chord branchでは `repair-x` / `repair-y`（cubeの整数冪 -A(w)/6、-B(w)/6）、`repair-central`（commutatorのsigned omega(w)冪）、最後に `raw-root`（w、repair-x、repair-y、repair-centralのOrderedProduct）。aux branchでは `raw-root` は選択r-xまたはr-yのIntegerPower9である。

`raw-word.json=seal('raw-word',{grammar:'ordered-slp-v1',nodes,root:'raw-root',cycles:<保存六項または空>,eta:<2trits>,node_values,normalizers,geometry_manifest_sha256,witness_sha256,word_bound,word_stream,legality})`。node_valuesはnodesと同順で `{id,exponent:[A,B],omega,length,q0:[36個の0-based permutation],q2:<qid>}`。raw chain/P1/current巨大wordを全node分dense保存しない。integer A/B とlengthはraw SLPのordinary integers。

normalizersはactual `scratchpad/a0_v2_words.json` の whole-file106133 / `fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612` と、19-word listのcompact ASCII **LFなし** SHA `dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a` を区別する。`r_x=q1*q6^-2*q7^4*q9`、`r_y=q8^-1*q4^-1` のfree reductionをv459のlength/hashへjoinする。r_x/r_yはN0、raw-rootのOmega型はv547またはv459の名前付き有限群前提と実Q0/Q2 endpoint、整数epsilon、omega、chain/tauから出す。Q0の実36点とGamma0を混同しない。

`word_stream` は同じraw-rootのsigned lettersを順に消費する実emitted count / EOF / SHA256を記録する。hash encodingは各letterを単一byte `{1:1,-1:255,2:2,-2:254}` にする。free reduction後のv459 JSON hashとは別。SLPで展開長を先に計算し、emitted countがそのlengthと一致することを確認する。P1/current wordはflattenしない。

nested exact fields: `normalizers={dictionary:<file/bytes/wholeSHA>,raw_relators_sha256,words:[{name,length,word_sha256}]}`、words順r_x,r_y,c_x,c_y。`word_bound={tree_height,unrepaired:<w length>,normalized:<F2の整数上界>,actual_slp_length:<raw-root length>}`。`word_stream={encoding:'signed-byte:1=01,-1=ff,2=02,-2=fe',bytes,letters,sha256,full_eof:true}`。`legality={method:'v547-three-factor'|'v459-ninth-power',q0_identity:true,q2_identity:true,tau:[0,0,0,0,0],epsilon_divisible18:true,normalized_pair:<eta>,omega:0,epsilon_exact_zero:<bool>,omega_zero:true,delta_endpoint_mode:'v547-retained-Gamma0-readout'|'v459-retained-expGamma9',actual_delta_enumerated:false,normalizer_Q2_Fox_zero:true,raw_chain_matches_witness:true}`。

`raw-source.json=seal('raw-source',{method:'raw-Q2-Fox-and-six-tag-direct-SLP',components:<既存d0,d1,d2,aux component receipts>,raw_word_sha256,chain_sha256,eta,tag_chain_receipts:[{tag,raw_fox_sha256,direct_fox_same:true,q2_endpoint:0}],source_lower_sha256,source_full_top_sha256,homogeneous_scalar,section_scalar,witness_scalar,direct_raw_word_replay:true,full_tag_eof:true,eleven_slot_replay:false})`。raw_fox_sha256は各tagの未qnorm Fox chainをedge ID=2*q+slotに並べpacked3した全bytes。homogeneous_scalarは全四qとraw d2の和、section_scalarはκとraw full96776 lowerのdot。

P1補正語は `V_word=raw-root * product_(recorded nonzero P1 events) W_i^signrep(-alpha_i)`。物理normalized語は `(V_word * product_(recorded physical reductions) S_p^signrep(-q_p))^signrep(sigma)`。P1 Refはaccepted canonical index/instruction/cache、physical Refはaccepted complete prefixの挿入順pivot ID / offer / row hashへ結ぶ。source-lower零はV_wordだけに付ける。Connも引くnormalized語にはphysical-lower零の型を付け、V_wordの96776座標零receiptをコピーしない。raw-rootのwhole-word直接Foxは新実施範囲、V_wordはcanonical P1 ancestryと線形source replay、normalized/target全wordのeleven-slot直接再生は未実施と分ける。

## 公開 ABI v1 — metadata と一行 chain

exact oracle acceptance tuple/entryはroot受領後に固定する。layoutは `seal('oracle-parent-layout',{artifact,entry_files,manifest_sha256,start_sha256,owner_sha256,source_sha256,result_sha256,witness_sha256,terminal,state_head,rank,generation,lambda_sha256,target_remainder_sha256,old_arithmetic_replayed:false})`。entry_filesは `{file,bytes,sha256}` のpath昇順。元completion親tupleと旧producer source/state由来を別に保持する。全oracle stageのexactroster/hash/EOFを認証し、source/root lambda/target/currentstateの一致を要求する。

`result.target` は plain `{parent_remainder_sha256,remainder_sha256,scalar}`。scalar0合法。instructionは `schema=prefix+'.instruction'` と predecessor=current state headを持ち、`rolling_sha256=SHA(bytes.fromhex(predecessor)+canonical(instruction excluding rolling_sha256))`。rank/generationは親+1、offerは親generation、physical_offsetは親rank×12096。origin.kindは `v548-cycle` または `v548-aux`。witness scalar、normalizing sigma、target scalarを別々のfieldへ保存する。HEAD.kindは `Separator` または `LinearMembershipCandidate`、completed_steps=1。payload/result/instruction/manifestをdurable化してからHEADを公開する。HEADはmanifest自身のfile rosterに含めず、HEADからmanifestを参照する。

stageは `raw,source,primal,p1,B,physical` の順。各stageでelapsed_seconds/bytes/EOF、rawは実長、primal/P1はalpha supportを `telemetry.json` に保存する。UNKNOWN_RESOURCEは完成したstage名だけのdiagnosticとし、数値のprefixを全零へ読み替えない。

`telemetry.json=seal('telemetry',{stages:[{stage,elapsed_seconds,bytes,eof:true,alpha_support:<int|null>,letters:<int|null>}],old_scans_numerically_replayed:0,old_inserts_numerically_replayed:0,physical_appends:1})`。bytesは当該stageで新規に書いたpayload全bytesの和（telemetry自身/owner/start/source/manifest/HEADは含めない）。rawはraw-word/chain、sourceはraw-source四配列とreceipt、primalはcoefficients/reductions/exponent-residues、p1はroots/lower-remainder/corrected-top/source-correction、Bはby-character/raw物理行、physicalはremainder/normalized/literal/instruction/target/optional lambda/result。elapsed_secondsだけを非負finite floatとして認証し双方一致を要求しない。bytes/letters/alpha support/stage順/EOFは実payloadに結ぶ。

`SCOPE={snapshot_count:1,physical_appends:1,characters:[0,1,2,3],source_tags:6,p1_rows:8059,source_lower_trits:96776,physical_trits:48384,max_cycles:6,full_raw_word_source_replay:true,full_normalized_word_replay:false,eleven_slot_replay:false}`。`FORMULA='v547-literal-repair;v548-primal-section;four-B;one-physical-row'`。

`owner=seal('owner',{formula_id:FORMULA,scope:SCOPE,oracle_owner_sha256,refinement_head_sha256,p1_parent,task554_parent,task712_parent,task712_manifest_sha256,word_dictionary_sha256,relator_dictionary_sha256})`。最後六 fields は oracle owner と同じ値。`start=seal('start',{kind:'Separator',rank,generation,state_head,lambda_sha256,target_remainder_sha256,accepted_oracle_layout,accepted_refinement_layout,accepted_target_derivation_parents,lambda_rho2,direct_pairing})`。後ろのrefinement layout/target parents/lambda certificate/direct_pairing は薄い現 snapshot loader と実 oracle start の一致を要求する。

`source=seal('source',{producer_sha256,modules:<own retained producer filename→SHA>,data:<old2 raw pins+normalizer dictionary pin>,python:sys.version,numpy:np.__version__})`。modulesには凍結 oracle producer v1と、その六 retained producer filesを含む。data は path を key、`{bytes,sha256}` を value とする既存形式。`scratchpad/a0_v2_words.json` の value は `{bytes:106133,sha256:<上記whole-file>}` であり、この value 内に重複した file field は置かない。raw-word.normalizers.dictionary の descriptor は引き続き file/bytes/sha256 の三字段である。

`p1-reductions.json=seal('p1-reductions',{order:'old-global-ascending-embedded-original-lead;new-owner-major-ascending-original-lead',rows:8059,events,coefficients_sha256,lower_zero:{trits:96776,packed_sha256},eof:true})`。各eventは `{event:<0based>,kind:'old'|'new',owner,local,node,original_lead,embedded_lead,coefficient,literal_exponent,row_offset,row_sha256,companion_offset,companion_sha256}`。embedded_leadは full96776座標。rowはold lower(6056)またはnew d1(18144)のpacked原行、offsetはoriginal local ID×row bytes。old companionは全四d1の72576-trit行、newではcompanion両字段null。literal_exponentは `-signrep(coefficient)`。

`p1-roots.json=seal('p1-roots',{p1_manifest_sha256,instruction_sha256,cache_sha256,canonical_index_sha256,roots,all_references_authenticated:true})`。rootsはselected node昇順。各itemはaccepted canonical-index.references[node] の全fieldsに `lift_components:<旧v1 subtract_liftsが出す{role,bytes,sha256}のlist>` を加える。positioned instructionも同じoffset/length/hash/ancestryで読み、origin/reductions/scaleの型をjoinする。転記したopaque wordを作らず、accepted DAG自身をexternal Refとする。

`p1-exponent-residues.json=seal('p1-exponent-residues',{rows:8059,order:'canonical-row-id',modulus:54,pairs:<8059個の[0..53,0..53]>,p1_manifest_sha256,instruction_sha256,method:'ordered-signed-DAG-exponent-mod54',eof:true})`。old projected seed、actor、whole old defectへのnew projector、ordered negative reductions、inverse scaleを同じliteral grammarでmod54へ送る。canonical source数値を再計算する操作ではなく、source auxのmod3値から逆算しない。rootが本便作業中に認可した軽量化である。整数epsilonの剰余rについて18整除はr∈{0,18,36}と同値、normalized pairはr/18 mod3で完全に決まるため、Task958の必要gateを失わない。raw v547修復の-A/6,-B/6には引き続き普通整数を使う。巨大なP1普通整数をexportしたとは記さない。

このJSON pairの型は **residue54**、通常int（bool不可）の0..53であり、F3 tritやpacked3へencodeしない。加算・符号・projector倍算はPython整数で行い、その後に標準非負剰余へ戻す。全8059 pairsのexact EOFを要求する。負の普通指数も同じ標準剰余で18整除とr/18のF3値を正しく読む。

`source-correction.json=seal('source-correction',{operation:'ordered-product',raw_word_sha256,p1_factor_order:'event-ascending',p1_factors,p1_roots_sha256,coefficients_sha256,exponent_residue_mod54:<0..53 pair>,normalized_pair:<2trits>,components:<d0,d1,d2,auxの既存component receipts>,source_lower_zero:{trits:96776,packed_sha256},source_lower_equality:true,top_characters:[0,1,2,3],whole_word_direct_replay:false,canonical_p1_source_replay:true,eleven_slot_replay:false})`。p1_factorsはevent順の `{event,node,coefficient,literal_exponent,p1_sha256}`。primalの計算済みlowerへsubtract_liftsを再適用せず、raw tupleの別copyから一度だけ引いて全lower一致を要求する。

`physical-literal.json=seal('physical-literal',{operation:'scaled-ordered-product',source_correction_sha256,accepted_physical_head,physical_factors,sigma,literal_outer_exponent,source_lower_zero:'NOT_ASSERTED',physical_lower_zero:true,physical_normalized_sha256,whole_word_direct_replay:false,eleven_slot_replay:false,target_word_direct_replay:false})`。physical_factorsは物理挿入順reductionの `{pivot_id,offer,lead,physical_offset,row_sha256,scalar,literal_exponent}`。accepted_physical_headから既存whole-prefixのtyped instructionsへ繋がる。literal_outer_exponentはsignrep(sigma)。

instruction の exact body fields は `{schema:prefix+'.instruction',predecessor,offer,rank,generation,physical_offset,origin:{kind,oracle_manifest_sha256,witness_sha256,raw_word_sha256},source_correction_sha256,physical_literal_sha256,p1_roots_sha256,p1_reductions_sha256,physical_reductions,lead,sigma,physical_sha256,selected_scalar,target_scalar,target_remainder_sha256}`。上記 rolling_sha256 を最後に加える。physical_reductionsはretained materializerのplain六field `{pivot_id,offer,lead,scalar,physical_offset,row_sha256}` のordered list。

`target_derivation={mode:'derived',original_rho2_directly_read:false,original_rho2_packed_sha256,accepted_target_derivation_parents:<startの同じlist>,new_delta:{instruction_sha256,state_head,normalized_sha256,target_sha256},identity:'parent_remainder - new_remainder = target.scalar * new_normalized_row'}`。target_sha256はplain target dictのcanonical+LF hash。自己result/manifest hashを同objectへ循環参照しない。target非零の `separator={free_coordinate,free_value,lambda_sha256,direct_pairing,lambda_rho2}`。lambda_rho2は `{mode:'derived',value:1,original_rho2_directly_read:false,target_derivation:<上記>,new_target_steps_executed:1}`。target零ではseparator=nullであり新lambda.binも存在しない。

`result=seal('result',{status:'PASS',terminal,kind,owner_sha256,start_sha256,source_sha256,parent_state_head,state_head,rank_before,rank_after,generation_before,generation_after,selected_scalar,homogeneous_scalar,section_scalar,corrected_scalar,physical_scalar,remainder_scalar,pivot:{lead,scale,normalized_sha256,reductions},target,separator,target_derivation,raw_word_sha256,source_correction_sha256,physical_literal_sha256,p1_roots_sha256,instruction_sha256,physical_appends:1,positive_readout:'TASK958_PENDING' if targetzero else 'NOT_APPLICABLE',grade2_member:'NOT_DECIDED',grade2_nonmember:'NOT_DECIDED',full_A0:false,candidate:true,cross_checked:false,verified:false})`。五scalar等式は `selected=homogeneous-section=corrected=physical=remainder !=0`、normalization後のold lambda値とは区別する。

`manifest=seal('manifest',{owner_sha256,start_sha256,source_sha256,result_sha256,instruction_sha256,parent_state_head,state_head,files:<manifest/HEADを除く全payloadのpath昇順{file,bytes,sha256,dtype,shape}>,stage_eof:['raw','source','primal','p1','B','physical'],candidate:true,cross_checked:false,verified:false})`。JSON dtype='json',shape=null、上表のarray型を固定する。`HEAD=seal('head',{owner_sha256,source_sha256,start_sha256,manifest_sha256,instruction_sha256,parent_state_head,state_head,rank,generation,kind,completed_steps:1,physical_sha256,target_remainder_sha256,lambda_sha256:<hashまたはnull>})`。HEAD公開を完成点とする。

零oracleのNOT_APPLICABLEは `{schema:prefix+'.not-applicable',status:'NOT_APPLICABLE',terminal:'NOT_APPLICABLE',oracle_terminal:'COMPLETE_ZERO_CANDIDATE',accepted_oracle_layout,physical_appends:0,candidate:false,cross_checked:false,verified:false}` のsealed objectをstdoutと `not-applicable.json` のみに出す。親薄いmetadata join以外のE算術は呼ばない。resource診断はsealed `{status:'UNKNOWN_RESOURCE',terminal:'UNKNOWN_RESOURCE',phase,completed_stages,candidate:false,cross_checked:false,verified:false}`。actual parent canaryはold15件を保持し、`oracle-roster,oracle-witness-scalar,oracle-snapshot,oracle-eof,oracle-current-root` の5変異を追加する。

親rank1385は裁定2131のcross-checked限定7条を継承する。旧origin表の独立性不足、旧seed2のhash継承、lambda rho2 DERIVEDを消さない。新consumerは旧scanを再実行せず、この一つのraw witness/source/primal/four-B/physical rowを独立照合の対象にする。Task965自身のGHA上のAST/canaries/actual metadata/新算術とCV-9は未実行。

## 実 oracle completion の intake と親の格付け

root が回収した `%TEMP%/shadow-atelier-section-oracle-completion-run33977701313-candidate-a1` の JSON と実 bytes/hash を独立に読んだ。candidate tuple は run **33977701313 / attempt1**、head `bbce98d8f95a845f36fe89c0f507b9360792666f`、workflow `.github/workflows/d972-r07-section-cochain-checker-completion-v1.yml`、artifact **9972829869**、name `d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1`、ZIP **2299772 bytes / 1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d**。tuple の sha256 は既存 ABI と同じ `sha256:` prefix付き、entry hash は hexのみ。

実採用する十 entry は以下。file hash は末尾LFを含む全bytesのSHA256であり、JSON内部sealとは別である。

| entry | bytes | SHA256 |
|---|---:|---|
| output/manifest.json | 1430 | 7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639 |
| output/start.json | 48377 | 7ff970e54dec57512593f5445fed387075d6602bff31f41b7db9f34bab045a2a |
| output/owner.json | 8419 | 6c71fbc405105bd0722924a308594ba41aea6745725ae85d046ff7409998b322 |
| output/source.json | 1246 | af1e178d19e4ee427439d102de74a559ed6202ca0a2839212a60748ccfe482ac |
| output/result.json | 13727 | c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312 |
| checker-result.json | 15387 | 92739f2db1007ec9ee040716c9dcb26859c10e5a5917a377514bb8e4eb4cd41a |
| source-receipt.json | 2673 | cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934 |
| completion-run-receipt.json | 2089 | 3c2eb678db147c7538adf7520f19d91610b255488464704d32a224f9cda4102b |
| repair-source-receipt.json | 3204 | 2b2efda3b1922e30246621a8b8cf87a277587767ca77662a03b7a35ef821bd37 |
| preserved-input.json | 10504 | 332f6b62aca1042868e65117d4cc9de952ef8d4817d5169ae8a1ee1a9298e625 |

元 producer は run **33975617653 / 1**、head `c57a722224320f9a573cfe84dea6979df5cb5320`、`d972_r07_section_cochain_oracle_v1.py` **73290 bytes / 4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb**。元 diagnostic artifact は9972256636、ZIP2271586 / `c66e7477740c8c5e0c0e9e00e613836bf5baacf00f10acf63fad5b23d6cc113a`。元checker v1はgeometry出力時のint32/sentinel型エラーで全array比較前に停止しており、その旧結果をPASSへ読み替えていない。

新 completion は producer呼出0、checker呼出1、旧成功suite0、旧parent canary0で保存出力を再照合した。checker v2 **84402 bytes / a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d** の成功結果を使う。schemaは引き続き `d972.r07.section-cochain-oracle.v1.checker-result`、内部generic sealも実在する。元14 executable file receipts が repair receipt の先頭14件として不変で、その末尾一件が v2 checkerである。producer/sourceの元由来と、新checker/completionの由来をこの三receiptで分けている。

metadataの実観測は `status:PASS,terminal:VIOLATION_CANDIDATE,materialization:MATERIALIZATION_PENDING`、rank1385 / generation8090、全stage arrays比較済、section equalities8059 / chords54433 / auxiliaries2 / physical appends0。親state headは `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`、lambdaは `1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1`、target remainderは `111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad`。witnessの全file hashは `1c282b82cbf430b3ef492a325c26ac3c7d2bf9146f15aa76c94744f8477620fd`。これは格付け前の成功candidateの実metadataであって、このworkerが数値を再導出したという主張ではない。

保存 witness は failed chord12、基準chords `[2,3,4,6,11]`、basis coefficients `[2,0,2,2,2]`、ordered cycles `[(12,1),(2,1),(3,0),(4,1),(6,1),(11,1)]`、eta `[0,0]`、scalar1。ゼロ係数のchord3もraw SLP receiptに残す。Eの実行結果はまだ無く、この観測からtarget scalarや新終端を推測しない。

PowerShellのmetadata/hash読取だけで preserved-input に記載された **output全44 files / 5361492 bytes** も照合し、不一致0を確認した。rootとTask967も十entry pinsと型の一致を独立に確認した。production `validate_oracle_completion` はcompletion/repairのlaunchとworkflow、preserved origin、五receipt hash連鎖、producer0/checker1/fullA–D PASS、44files/4dirs/5361492bytes、元producerと修理checker、data pins、元六entryとwitness hashをjoinする。`read_oracle` はこれに加えて全A–D payload roster/shape/dtype/hash/EOF、固定snapshot、checkerの全数比較、currentlambda/targetを認証する。既存A–Dの数値再走は行わない。

`ops/express/20260906_fable_astra_section_completion_cv9_ack.md`（裁定2137）を全文読んだ。工房CV9は進行中であり、候補pin消費とTask965〜967継続を妨げないと明示されている。独自にcross-checkedへ格上げせず、裁定2131の七限定およびF-fo-1を維持する。今回の出力型修理は旧origin表の独立性不足を遡及して閉じない。

## 最終 source と実装の完了範囲

`search/d972_r07_selected_cycle_materializer_v1.py` を **88929 bytes / SHA256 4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3**、**LF1450 / CR0 / BOMなし / finalLFあり** で凍結する。変更した作業ツリーはこのsourceと本replyだけ。Task959を含む公刊済みsource/reply、workflowは変更していない。ローカルPython/GAP/import/AST・network・git・credential・dispatch・追加agentは実施していない。末尾空白のtext検索も不一致0である。

実装したのは、同じordered raw SLPの整数epsilon/omega/Q0/Q2/stream hash/EOF、全6tag直接Foxとraw chain routeの一致、全四characterのd0/d1/d2/sharedaux、old元embedded lead昇順からnew各owner元lead昇順のprimal、全8059 literal exponent residue mod54、全四top補正、一回の四B加算、一行physical消去/normalize/target更新、新separatorと全row/両targetの直接pairing、typed ancestry、およびmanifest→HEADの耐久公開である。Task967とrootは新算術/tailの静的読了でrequired correctionなしを報告し、Task967は最後のcompletion metadata差分も実JSONと照合してrequired correctionなしとした。これはruntimeのPASSではない。

P1の数値行とliteral DAGは分離する。normalized canonical rowへscaleを二度掛けず、同じraw tupleのfresh copyへ `subtract_lifts` を一回だけ適用し、別計算したprimal全96776 lowerと一致させる。P1 ordinary exponentそのものはexportせず、同じsigned DAGのmod54を使う。原raw語のordinary整数と/6は保持する。source-lower零はV_wordの型であり、Connを引いたnormalized physical literalにはphysical-lower零だけを付す。

新interface canaryは三群をproduction helpersへ接続した。第一群はomega積/負冪/commutator、負chord、同じnegative raw seed SLPの全filtered degrees/四character直接source、非可換endpoint。第二群は元lead順と逆挿入順が異なるsmall fixture、old四d1 companion/sharedaux、新owner rows、scale非再乗算、residue54とtrit型の区別。第三群はone-row本体、target scalar0、dynamic generation、新separator、linear target零をMEMBERへ上げない型、plain targetへgeneric sealを付けた変異拒否、実payload/rolling instruction serializerである。これは旧成功suiteや旧26scan/insertの全数再走ではない。いずれの新canaryもまだローカル実行していない。

resource deadline/SIGINT/SIGTERMは既存の読取・source・P1・physical progress boundaryまで伝播し、exit3 / UNKNOWN_RESOURCEを保存する。新鮮なoutputだけを作成し、完成stage一覧をdiagnosticに残す。完成payload・result・manifestをdurable化してからHEADを出す。途中stageだけを完成candidateへ数えない。raw/source/primal/P1/B/physicalの六時間・payloadbytes・EOFと必要support/実長は本走時に記録する。

残る実行gateは、Task966の独立checkerと承認済みworkflowのsource freeze、GHA上のAST/actual親layout・20 metadata変異/双方の新interface canary、実一行producer、独立全payload照合、runtime telemetry、工房CV9である。rootが単一brokerとして実施する。Task965で新runは未dispatchであり、実run id/commitはrootの実行記録へ委ねる。raw whole-word source直接評価はこのconsumerの対象、normalized physical word/target whole wordの11slot直接再生とTask958 positive readoutは未実装の別consumerである。target零でもLINEAR_MEMBERSHIP_CANDIDATEに止め、grade2 MEMBER/NONMEMBER/fullA0/verifiedを宣言しない。

AUDIT_965_VERDICT: SOURCE_FROZEN_WITH_OBSERVED_ORACLE_COMPLETION_PARENT; STATIC_REVIEW_NO_REQUIRED_FIX; NEW_RUNTIME_AND_INDEPENDENT_CHECKER_GATES_PENDING; CV9_2137_PARENT_GRADE_PENDING_AND_2131_LIMITS_RETAINED; verified=false
