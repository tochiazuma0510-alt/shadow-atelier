# Task959 — v548 single-snapshot complete scalar oracle

Task958 完了後、Task959 / reply957 / v548 / v543 / v546 / v547 を全文読み、A–D と薄い親 intake を実装した。成功 completion candidate の実 bytes と PASS metadata を独立に読み、親定数を接続した。以下が最終公開 ABI と source freeze である。新 oracle の実数値・terminal はまだ未観測。

## 公開 ABI v1（Task960 と共有する契約）

schema prefix は `d972.r07.section-cochain-oracle.v1`。JSON は ASCII、sort_keys、compact separators、末尾 LF。sealed object は `schema=prefix+'.'+kind` を含む全フィールドから `sha256` だけを除いた canonical bytes の SHA256 を同フィールドに持つ。file reference は seal を含む file 全 bytes の hash。全 array は C-order。`u8` は各値0..2、`u32le` は little-endian uint32、`packed3` は base3 の4 trits/byte（重み1,3,9,27）。JSON payload は `dtype:'json',shape:null`。

CLI は既存の `--state-root --delta-root --seed34-root --packet-root --prepare-root --block-root`（4回）`--p1-root --task712-root` に `--refinement-root` を追加する。`--output` は新しい出力 directory、`--max-seconds` は default1800 の運用 deadline。単一 snapshot、append/resume はない。`--selftest` は root 不要。`--parent-layout-selftest` は state/delta/seed34/packet/refinement の5 rootsだけを受け、output と numerical parents を受けない。

qid は `((parity_index*27+9*k0+3*k1+k2)*504+p)`、parity順 `((0,0),(0,1),(1,0),(1,1))`。edge ID は `2*q+slot`、slot0=X、slot1=Y。tree は identity0から正X,Yの順のBFS、root parent/parent_edge は uint32 sentinel4294967295。chord は tree edge 以外を edge ID 昇順。tag順・monomial順・transport は actual v15。全8059の canonical row ID は旧順、dual solve は new各ownerの元lead降順、次にold全体のembedded元lead降順。

output は `owner.json,start.json,source.json,manifest.json,result.json` と四 directory `geometry,section,cochain,tree`。各 directory の `manifest.json` は `seal('stage-manifest',{stage,owner_sha256,snapshot_sha256,inputs,files})`。`inputs` は依存 stage名→その manifest の full byte SHA の dict（geometry/sectionは空、cochainはgeometry/section、treeはgeometry/cochain）。`files` は basename昇順の exact roster、各 item は `{file,bytes,sha256,dtype,shape}`。余分な file を受けない。stage metadata は以下の `.json` もこの roster に含める。

| stage | payload basename | dtype / shape |
|---|---|---|
| geometry | `next-pos.u32`, `prev-pos.u32` | u32le / [54432,2] |
| geometry | `phi.u32` | u32le / [6,54432] |
| geometry | `parent.u32`, `parent-edge.u32`, `bfs-order.u32` | u32le / [54432] |
| geometry | `carry.u8` | u8 / [108864,5] |
| geometry | `chord-edges.u32` | u32le / [54433] |
| geometry | `geometry.json`, `tag-fox.json` | json |
| section | `q.bin` | packed3 / [4,36288] |
| section | `p1-values.u8` | u8 / [4,8059] |
| section | `chi.u8`, `equation-values.u8`, `equation-residuals.u8` | u8 / [8059] |
| section | `beta.u8` | u8 / [2014] |
| section | `kappa.bin` | packed3 / [96776] |
| section | `lead-original.u32`, `lead-embedded.u32` | u32le / [8059] |
| section | `new-solve-order.u32`, `old-solve-order.u32` | u32le / [6045], [2014]；値はcanonical row ID |
| section | `section.json` | json |
| cochain | `score.u8` | u8 / [6,2,54432] |
| cochain | `f.u8`, `b-aux.u8` | u8 / [108864], [2] |
| cochain | `cochain.json` | json |
| tree | `potential-f.u8`, `potential-tau.u8` | u8 / [54432], [54432,5] |
| tree | `chord-values.u8`, `chord-tau.u8`, `chord-residuals.u8` | u8 / [54433], [54433,5], [54433] |
| tree | `selected-chords.u32`, `fit.u8` | u32le / [5], u8 / [5]；selectedはedge ID |
| tree | `witness.json`, `tree.json` | json |

`lead-embedded` は full96776座標：old d0ならa*6048+lead、old auxなら96768+lead−6048、newなら24192+a*18144+lead。old solve の順序比較は E=24200へのembeddingと同じ順になる。normalized blob row の scale は再乗算しない。free kappa coordinatesは0。全8059式の最終値/residualを保存する。

`tag-fox.json` は plain `{tags:[{tag,words:[wordX,wordY],images:[qidX,qidY],fox:[termsX,termsY]}]}`。termは `[component,prefix_qid,coefficient]`、短い literal substituted word の signed Fox encounter順（同一key再訪時は最初の位置、零なら消去）。tag0と4も別record。raw qnormは新linear adapterで、x termを−component0 at sX、−component1 at sXB、aux_tag +1へ、y termをcomponent1 at sへ送る。sXB=sY^-1を全verticesで確認する。

`geometry.json = seal('geometry',{vertices:54432,edges:108864,tree_edges:54431,chords:54433,characters:[[0,0],[0,1],[1,0],[1,1]],actors:[1,2],qid_order:'parity,k-base3,psl-fastest',edge_order:'2*q+slot',tree_order:'positive-bfs-X,Y',chord_order:'edge-id-ascending',group_convention:'section-left/kernel-right;perm=right[left[i]]',fox_convention:'left-prefix;positive-edge-right-product',carry_convention:'rotation-left;integer-carry-before-mod3',sentinel:4294967295,transport:<6x4x2 labels>,q0_marking_sha256:<whole g data pin>,psl_elements_sha256:<canonical list of 504 zero-based permutation lists>,full_vertex_eof:true,full_edge_eof:true,all_phi_edges_checked:true,phi_bijections:6,qnorm_right_identity_checked:true})`。

`section.json = seal('section',{rows:8059,old_rows:2014,new_rows:6045,source_lower_trits:96776,shared_auxiliaries:8,formula:'v548:chi=sum_a<B_a^*lambda,z_i[a]>;kappa(b_i)=chi_i',solve_order:'new-owner-major-descending-original-lead;old-global-descending-embedded-original-lead',free_coordinates:0,p1_cache_sha256:<accepted cache>,lower_blob_pin_sha256:<own batch constant>,p1_passes:1,all_equations_checked:8059,equation_eof:true,old_arithmetic_replayed:false})`。fresh qと全8059 contractionをこのsnapshotで独立に再計算し、過去character sparsityを仮定しない。

`cochain.json = seal('cochain',{formula:'v548:sum_a q_a Psi2[a]-kappa Psi1',tags:6,components:2,vertices:54432,edges:108864,score_eof:true,edge_eof:true,shared_eta:true,normalized_aux_rule:'b_aux=-kappa_aux[6:8];no-mod3-division-by18',raw_edge_adapter:'tagged-Fox-left;right-X-XB-qnorm',physical_mixed_C_used:false})`。

`tree.json = seal('tree',{vertices:54432,tree_edges:54431,chords:54433,independent_tau_columns:5,selection_order:'first-independent-chord;coordinate0-through4',selected_chords:<5edge IDs>,fit:<5trits>,aux_values:<2trits>,first_failed_chord:<edge ID or null>,residual_nonzero:<count>,full_chord_eof:true,terminal:<terminal>,materialization:<status>})`。fitはrow a、selected Tのcolumnsは保存順のtau。witnessは常にseal('witness',body)：零なら `{kind:'none',cycles:[],eta:[0,0],tau:[0,0,0,0,0],scalar:0,materialization:'NOT_NEEDED_FOR_ZERO_TEST'}`。auxなら `{kind:'auxiliary',coordinate:0or1,cycles:[],eta:e_i,tau:[0,0,0,0,0],scalar:b_aux[i],materialization:'MATERIALIZATION_PENDING'}`。chordなら `{kind:'chord',failed_chord:<edgeID>,basis_chords:<5IDs>,basis_coefficients:<d5>,cycles:[{edge:<failed>,coefficient:1},<全5基準の{edge,coefficient:(-d)%3}>],eta:[0,0],tau:[0,0,0,0,0],scalar:<nonzero>,materialization:'MATERIALIZATION_PENDING'}`。0係数も6項receiptには残す。

terminal は `COMPLETE_ZERO_CANDIDATE` または `VIOLATION_CANDIDATE`。零はb_auxと全54433residualの零を要求する。非零の優先順はaux x、aux y、最初のfailed chord。E未実装なのでphysical append/target変更はしない。deadlineは `UNKNOWN_RESOURCE` diagnostic、部分EOFからresult/manifestを発行しない。

## 親と top-level JSON の公開 ABI

`accepted_refinement_layout = seal('refinement-parent-layout',{artifact,entry_files,completed_steps,terminal,rank,generation,state_head,lambda_sha256,target_remainder_sha256,steps,old_arithmetic_replayed:false})`。artifactはrootが渡すexact tuple、entry_filesは `{file,bytes,sha256}` のbasename/path昇順。stepsは保存順に `{step,manifest_sha256,result_sha256,instruction_sha256,target_sha256,state_head,parent_state_head,rank,generation,lead,target_scalar,physical_normalized_sha256,lambda_sha256,target_remainder_sha256}`。target_sha256はplain targetのcanonical+LF hash。Memberは入力型違反、ROOT_ORIGINS_ZEROは要求しない。

actual-parent selftestは旧 `parent_layout` と `accepted_packet_layout` を保持し、`accepted_refinement_layout` を追加する。新5 mutation名は `refinement-instruction-generic-seal,refinement-target-generic-seal,refinement-target-parent,refinement-step-chain,refinement-final-head`。旧10と合計15 rejected_cases、statusPASS、metadata_only true、schema prefix+'.parent-layout-selftest'、cross_checked/verified false。productionも同じrefinement layout validatorを使用する。

`SCOPE={vertices:54432,positive_edges:108864,chords:54433,legality_rows:5,normalized_auxiliaries:2,p1_rows:8059,characters:[0,1,2,3],source_tags:6,snapshot_count:1,complete_finite_test:true,physical_appends:0}`。

`owner=seal('owner',{formula_id:<FORMULA>,scope:SCOPE,accepted_refinement_owner_sha256,accepted_refinement_head_sha256,p1_parent,task554_parent,task712_parent,task712_manifest_sha256,word_dictionary_sha256,relator_dictionary_sha256})`。最後の六parent/dictionary fieldsはaccepted full-origin ownerから同じ値を継承する。FORMULAは `v548:section-corrected-homogeneous-dual;v546:five-carry;v543:complete-tree`。

`start=seal('start',{kind:'Separator',rank,generation,state_head,lambda_sha256,target_remainder_sha256,accepted_refinement_layout,accepted_target_derivation_parents,lambda_rho2,direct_pairing})`。snapshot_sha256はstart全canonicalbytesのSHA。accepted_target_derivation_parentsは旧base/seed30/seed34/packet-step-1..3をそのまま継ぎ、各新段を `role:'refinement-step-'+i,manifest_sha256,result_sha256,target_sha256,state_head` で追加する。

`lambda_rho2={mode:'derived',value:1,original_rho2_directly_read:false,original_rho2_packed_sha256:<retained>,accepted_target_derivation_parents:<same list>,identity_convention:{base:'rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)',saved_deltas:'parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)',packet_and_refinement_steps:'parent_remainder - child_remainder = target.scalar * accepted_normalized_row'},new_target_steps_executed:0}`。direct_pairingは既存形式 `{rows,row_pairings_sha256,lambda_pivots:0,lambda_parent_remainder:1,lambda_new_remainder:1}` で現在lambdaを全保存rows/両targetに実測する。

`source=seal('source',{producer_sha256,modules:<own retained producer filename→hash>,data:<two existing exact data pins>,python:sys.version,numpy:np.__version__})`。modulesは full-origin v1、fixed packet v2 と同版MODULE_PINSの4 filesを含む。checkerはproducer source receiptと別に自己source/runtime pinを出す。

`result=seal('result',{status:'PASS',terminal,materialization,owner_sha256,snapshot_sha256,source_sha256,state_head,rank,generation,lambda_sha256,target_remainder_sha256,stage_manifests:{geometry,section,cochain,tree},witness_sha256:<full canonical witness bytes>,lambda_rho2:<start同値>,direct_pairing:<start同値>,complete_source_and_conn_premises_retained:true,all8059_section_equalities:true,all54433_chords_checked:true,normalized_auxiliary_tests:2,physical_appends:0,grade2_member:'NOT_DECIDED',grade2_nonmember:'CANDIDATE_ONLY' if completezero else 'NOT_DECIDED',full_A0:false,candidate:true,cross_checked:false,verified:false})`。

top `manifest=seal('manifest',{owner_sha256,snapshot_sha256,source_sha256,result_sha256,stage_manifests:<same dict>,files:<owner/start/source/resultだけの{file,bytes,sha256}昇順>,file_roster:['cochain','geometry','manifest.json','owner.json','result.json','section','source.json','start.json','tree'],candidate:true,cross_checked:false,verified:false})`。各stageのmanifest自身を含む全rosterをcheckerが照合する。writerは各stageを一時directoryからrenameし、全A–D完了後にresult→manifestを出す。deadline時は `resource-stop.json` とstdoutのseal('resource-stop',{status:'UNKNOWN_RESOURCE',terminal:'UNKNOWN_RESOURCE',phase,completed_stages:<published stage names in A–D order>,candidate:false,cross_checked:false,verified:false})、exit3。未完走時に top manifest を作らない。

数学算術は共有しない。全 candidate output に `cross_checked=false,verified=false` を維持する。以下の親格は工房裁定の記録であり、この新 source の runtime 結果を格上げしない。

## Source freeze と実 completion 親

producer の A–D、薄い accepted-prefix loader、出力 roster/seal、CLI、変更境界 canary を実装した。凍結 source は `search/d972_r07_section_cochain_oracle_v1.py` **73,290 bytes / SHA256 `4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb`**、LF1257、CR0、BOMなし、最終LF。最終変更は provisional 71,572 bytes / `fdacfbfb…` の空だった三定数への実 artifact・十 entry・26段 snapshot の接続であり、A–D 算術と tail は変えていない。accepted PASS では HEAD/result/checker の三者 generation join を要求する。ResourceStop receipt を成功 checker として取り込まない。

最終親は root broker が回収した **run33971897879/1**、head `64475e1dfab1537a38d1b3131971bfed5fc3071c`、workflow `.github/workflows/d972-r07-full-origin-checker-completion-v1.yml` の成功 candidate。artifact **9971466432**、name `d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1`、ZIP **51,943,596 bytes / SHA256 `0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8`**。artifact tuple の `sha256` 値には `sha256:` prefix を付ける。実展開 root `%TEMP%/shadow-atelier-full-origin-completion-run33971897879-candidate-a1` から、次の十 entry の bytes/SHA を独立に確認した。Task960 と同じ十 entry を `accepted_refinement_layout.entry_files` に封じる。

| entry | bytes | SHA256 |
|---|---:|---|
| output/HEAD | 921 | 6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba |
| output/result.json | 3988 | 04a88c1423f6d99f5e94ded601d20efa5b338ba2b4fae8e9f73023695cd69211 |
| output/start.json | 11011 | 1a709c2853a6d0c239bc31d50ba6e03b0fb4707d93b625d291a487e6d43dc131 |
| output/owner.json | 8432 | c4fd8b27590450d0b73e72efe9d45bf9319e111b5e21d1f3ff0b0ee23910f48c |
| output/source.json | 1139 | 7e99018f58f3f49e371b55e6daab491b71855bb463c8c47cd872dffb57b5774f |
| output/canonical-index.json | 6078393 | 452fe97a9229fa5188493256d1478ead1e684b495bbfed0db03a64f5acf4f00e |
| source-receipt.json | 2355 | 5d65f4313aaed81f30354cba5c90ead201816f72f15fcd799606ed5feab43f3e |
| checker-result.json | 57583 | ccb0b3dd225587dde0e08edca5dfa66b1446b7db01091a3e8118c7aeb4ed2e9c |
| completion-run-receipt.json | 1849 | b1c653283593a2fdef835c938bcc0c8502248b53c92d264842a2133bd4561e57 |
| preserved-input.json | 183567 | 746e097f23c78418a3b43754348099a753639fcceac006e4f1d634ad3fb57298 |

実 HEAD は26段、rank1385、generation8090、Separator、current_scan_manifest=null、producer terminal UNKNOWN_RESOURCE。最終 state は `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`、lambda packed SHA は `1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1`、target は `111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad`。step26 manifest は1,932 bytes / `1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c`。

成功 checker の実 JSON は `status:PASS`、`completed_steps=prefix_steps_replayed=complete_scans_replayed=26`、rank1385/generation8090、terminal UNKNOWN_RESOURCE で、head/result/owner/index の hash は上表に一致した。completion receipt は producer_invocations=0、checker_invocations=1、complete_prefix_replay=true、producer_output_unchanged=true、内部7200秒枠の PASS を記録する。元 run33967668257/1 の producer source commit は `fd04734d20d472e7c09f31de3f92f8a50d6d841a`。その旧 checker の1800秒・22段/22scan UNKNOWN_RESOURCE は履歴として分離し、成功 receipt の代用にはしない。root が output 配下968 files の不変を照合し、裁定2131の非当事者は preserved-input の全975 files を照合した。これらは各担当者の実測であり、こちらが旧数値を再実行したとは記さない。

## 継承する CV-9 格と独立性の境界

`docs/notes/full_origin_v1_cv9_reading_v1.md` と `ops/express/20260905_fable_astra_full_origin_v1_cv9_grade.md` を全文読んだ。裁定2131は rank1385/generation8090 を checker PASS 済み状態として受理し、CV-9を同一対象、工房格を **cross-checked 限定7条**とした。その限定を親前提に保つ。

1. 対象は rank1359→1385 の26周回だけ。rank1385での全 origin scan は存在せず、NONMEMBERではない。
2. 保存26scanの informative は各32,280、character0のみ。残る96,840は構造零である。
3. 選択26本は全て character0 の actor origin、basis506〜823。固定44seedは26scan全て零、24手はbasis815〜823に集中した。
4. target.scalarの零は8個、rank+26に対しtarget剰余の変化は18回である。
5. 固定packet3段は前提、λ·ρ₂はDERIVEDを継続する。元ρ₂の新しい直接読出しはしない。
6. 挿入・正規化・target更新は2117 pairの再利用である。
7. 旧走査表の子covectorを作る `sparse_adjoint` は両系統で本文同一、homogeneous収縮の `vectorized_projection_chunk` は類似0.9908。非クローンfinite27錨は選択26点だけであり、informative actor表に対する被覆は26/(26×32,236)、約0.0031%である。

F-fo-1の独立性不足を、次の新oracleによって旧scanへ遡及的に閉じたとはしない。旧sourceは凍結のまま。本版は actor-child covector を必要とせず、現在λから四つの `B*λ` rootだけを新たに作る。`current_roots_and_values` は全8059 canonical liftを16行ずつ展開し、新しい全四character収縮を行い、旧 `vectorized_projection_chunk` を呼ばない。その新χから同一κを構成し、全source edgeへ d0/d1/d2 と共有auxを通した後、全chordを調べる。これは別の完全scalar問題を現在snapshotで実行する境界であり、旧origin表の再実行や独立性修理ではない。新関数対と今回新たに主役になる継承primitiveの独立性は、Task960の実全配列照合と新CV-9判読の対象として残る。raw seed2 pinも本版で再実行せず、固定packetの名前付き前提として継承する。

## 実装・TCB・残る runtime gate

production intake は大きな materialization payload を stream hash 後に破棄し、各段の小さな instruction/result と normalized row/target/lambda だけを保持する。旧 scan、seed/actor materialization、insert、target 差分の算術は再実行しない。最後の現在 lambda を保存全 rows と両 target に直接当てる。現在 scan がない実 layout にも対応し、q と chi だけを新たに全四 character で計算する。

新しい実算術は `geometry_inputs`、`current_section`、`source_cochain`、`complete_tree_test` に分かれる。P1 cache は16行 chunkで一巡、Task554 body は一つずつ読み、元 row ID/lead と小さな blob descriptor だけを残す。kappa は new d1 の後に old joint d0/共有auxを解き、全8059式を同じ最終値で出力する。full source-edge matrix、全 decoded P1 lift matrix、physical mixed C/mu を作らない。

新 canary は3群である。非単調元leadと誤った reverse insertion、actual非可換右edge/左Fox/非閉edgeのd0・d1・d2・共有eta、全chord後端/偽EOF/六cycleとaux優先を、実 production の changed interfaces へ接続した。全36点 marking、全phi edge、全8059等式、全54433 chord は本体でも省略しない。

TCB は新 producer と自系 full-origin v1、その固定 packet v2、同版の4 retained producer modules、Python/NumPy、二つの pinned raw data。旧 source/P1/Conn/target/physical-prefix の受理済み算術を名前付き前提として保持する。Task960 との共有は本返信の公開契約・正本式・input pinだけで、checker 算術/sourceは読んでいない。ローカルの Python/GAP/import/AST、network/git/credential/dispatch、追加 agent は行っていない。

残りは Task961 の当該最終sourceへの tail/intake 静的監査、GHA上のsource AST/canaries、actual parent metadata双方照合、A–D producer と独立 checker の全配列一致、および新pairのCV-9判読である。新oracleの実算術・zero/violation verdict はまだ実行していない。新実行のrun IDとcommit SHAはroot brokerが実行後に記録する。Eの literal/P1/physical consumer、当該grade MEMBER、full A0 は出力しない。

AUDIT_959_VERDICT: SOURCE_FROZEN_WITH_ACTUAL_COMPLETION_PARENT; STATIC_TAIL_AND_GHA_GATES_PENDING; CV9_2131_PARENT_LIMITS_RETAINED; NO_NEW_ORACLE_RESULT; verified=false
