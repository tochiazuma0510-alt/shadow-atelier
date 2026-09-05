# Task974 — 継続prefixから同一語readoutへのABI差分

新consumerだけでA/B/Cを実装できる。必要な順序・係数・原点参照は凍結資料に残っている。ただし、Eのraw SLPからP1補正・physical補正を経た一つのnormalized wordと、その最終target積はまだ出力されていない。`source_lower_zero`、四Bの一致、target零をその完成の代わりにしない。

Task974、reply958/970/971、v518/v547/v548、[2144の訂正・signed代表採用](../ops/express/20260906_fable_astra_cycle_cv9_correction_ack.md)を読んだ。下記の自系sourceを静的に調べ、外部Eの実instruction/resultから字段だけを照合した。変更は本返信のみ。ローカル数値/Python/import/AST/GAP、network/git/credential、checker算術読取、追加agentはない。

本便の実状態はrootから通知されたrun33984832010/1、launch `b8c9e95ddd0183d9e43b7fcc961cb251fdaea13e`、cap1/resume32 success・全prefix checker中まで。新rank、scalar列、target零、terminalは未観測である。受理済み起点は外部E後のrank1386/gen8091/Separator。実E親はreply971の十entryおよびsource971の`E_FILES`をそのまま使う。artifact9973974150、ZIP2816692 bytes / `884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25`、run33981657987/1、launch `444c71c9e554ae8feb9c8ee54df57d3df19ed66f`である。新runをこの親の格で先取りしない。

## F1. 一つのtarget readerへ追加する確定規則

以下のpathは各artifact rootからの相対path。pivot IDは物理行の挿入順0-based、offerはinstruction stream上のIDであり、lead順でもP1 node IDでもない。旧分の数値を再掲・再除去せず、reply958 F1のreaderに最後の二行を足す。

| 系統 | coefficient / normalized row / ancestryを読む実体 | 物理pivot ID |
|---|---|---|
| base | `output/result.json.target_reduction.reductions`の`pivot_id,scalar`。`state/instructions.jsonl`の`kind=physical_pivot`と`state/physical.bin` | 0..1353。target reductionsにない位置は0 |
| seed30 / seed34 | 各`output/result.json.target.new_reductions`、`output/instruction.json`、`output/physical-normalized.bin`。旧sealed target-updateのparent target/result/state joinを保つ | 1354 / 1355 |
| fixed44 | `output/steps/000001..000003/{manifest,instruction,result}.json`と`physical-normalized.bin`。係数は`result.target.scalar` | 1356..1358 |
| 旧full-origin26段 | `output/steps/<j:06d>/{manifest,instruction,result,materialization}.json`とnormalized行。旧accepted HEADの26段を読む | j=1..26に対し1358+j |
| 外部E | `output/{manifest,instruction,result,physical-literal,source-correction,p1-roots,p1-reductions,raw-word}.json`とnormalized行 | 1385。実target scalarは1 |
| 新loop | `output/steps/<j:06d>/manifest.json`から`output/snapshots/<j-1:06d>/e/physical/{instruction,result,physical-literal}.json`とnormalized行へ到達 | `root.start.rank+j-1`。現起点なら1385+jというID規則のみ |

新loopのsnapshot `start.step=j-1`は**追加前**、step manifestの`step=j`は**追加後**。instructionの`offer`はsnapshot.generation、`rank`はsnapshot.rank+1、`generation`はsnapshot.generation+1、`physical_offset`はsnapshot.rank×12096にjoinする。これらは[source971:501](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L501)の型規則であり、新runの完成段数や結果rankを予想した式ではない。外部Eはroot startへ一回だけ含まれ、loopの`completed_steps`に数えない。

新readerはpin済み`output/HEAD`の`completed_steps=m,last_step_manifest_sha256`から、j=1..mの連続chainだけを読む。各stepはowner/source/start/fixed、snapshot、oracle-manifest/witness、全9`phase_manifests`、instruction/result、parent/new stateを結ぶ（[971:1395](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L1395)）。`snapshot/e/physical/result.json`が内側E resultで、root`result.json`は継続terminalである。別の`e_manifest_sha256`や`steps/j/e/`を探さない。

fixed44以後の一行targetは、厳密に`{parent_remainder_sha256,remainder_sha256,scalar}`のplain dictである。Eでは[965:727](../search/d972_r07_selected_cycle_materializer_v1.py#L727)がbool・余分なseal・範囲外scalarを拒否する。`result.target.scalar == instruction.target_scalar`を読む。instruction自身は`rolling_sha256 = SHA(parent_state_head_bytes || canonical(unsigned_instruction))`であり、generic JSON sealではない。manifest/result等のfile hashはsealを含む全canonical bytes、plain targetのhashにも末尾LFを含む。`selected_scalar`、`pivot.scale`/`instruction.sigma`をtarget係数へ代入しない。

新target列は、baseのrho2-minus-remainder、seed30/34のsaved delta、一行ごとの`parent_remainder-child_remainder=target.scalar*normalized_row`を接続する。元rho2 hashと全named parentsを保持し、外部Eは`external-e`、新段は`loop-e-<j:06d>`（[971:555](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L555)）。旧26段までの係数をa_i、新段の実読取係数をt_jと書けば、条件付きのreadoutは

\[
\rho_2=r_m+\sum_{i=0}^{1385}a_iS_i
                 +\sum_{j=1}^{m}t_jS_{1385+j}.
\]

係数0も全pivot表に残す。後のphysical reductionがそのpivotを参照し得るためである。相殺したraw祖先も落とさない。

HEADのcurrent snapshot/checkpoint、その先に完成していてもHEADに未採用のphysical、`steps/m+1`、登録されたhidden pendingは、readerの対象係数へ加算しない。未登録tailは拒否する。特に既存[971:`load_prefix`:1572](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L1572)はdurable physicalを`commit_step`してHEADを進めるので、read-only Aからそのまま呼べない。新Aは同じ認証規則の**非変更reader**とし、採用HEAD外のtailを診断として区別する。runのsuccessだけでなく、rootが回収するexact candidate/HEAD/result/全prefix checker receiptを入場条件とする。未知の新pinは閉じたままである。

## F2. 新Eを同じwordへ接続する式

以下`sr(0,1,2)=(0,1,-1)`、`W^[c]=W^sr(c)`。普通整数の冪は別型である。新Eのraw constructorsは[965:`selected_raw_word`:390](../search/d972_r07_selected_cycle_materializer_v1.py#L390)、signed emitterは[`RawSLP.letters`:309](../search/d972_r07_selected_cycle_materializer_v1.py#L309)、新layout復元は[971:`restore_raw`:1048](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L1048)にある。

chord枝では`witness.cycles`の全6項を記録順に、係数0の項も参照を保持して

\[
w=\prod_{h=0}^{5}\bigl(T_{tail_h}\,x_{slot_h}\,T_{head_h}^{-1}\bigr)^{[c_h]},\qquad
R_{raw}=w(r_x^3)^{-\epsilon_x(w)/6}(r_y^3)^{-\epsilon_y(w)/6}
          [r_x,r_y]^{sr(\omega(w))}
\]

とする。`T_v`は同じgeometryの`parent/parent-edge/next-pos`から根へ遡り、逆順にしたpositive tree word。`[r_x,r_y]=r_x^-1 r_y^-1 r_x r_y`。二つの`epsilon/6`は普通整数で、mod3冪へ縮めない。2144に従いomega=2の中央冪は-1である。+2に変えるとcomm³差で同じsourceとなり得ても、同じliteral word/SLP hashではない。raw-rootの因子順を固定する。

auxiliary枝は`coordinate=0/1`に対する`r_x^9/r_y^9`。`cycles=[]`、二成分etaを保持する。chord枝のeta=[0,0]をaux枝へ上書きしない。raw-wordの`nodes/root/node_values/normalizers/geometry_manifest_sha256/witness_sha256/word_stream`がこの同じ語を指す。外部Eのtree Refはaccepted oracle geometry stage、新loopでは`fixed/manifest.json`を指すというhash境界の差を処理する。

canonical P1の正規化済み語をW_iとすれば、primalの記録順に

\[
V=R_{raw}\prod_{e\in p1\text{-}reductions.events}^{\rm recorded}
                 W_{e.node}^{-sr(e.coefficient)},\qquad
S_{new}^{word}=\left(V\prod_{f\in physical\_reductions}^{\rm recorded}
                 (S_{f.pivot\_id}^{word})^{-sr(f.scalar)}\right)^{sr(\sigma)}.
\]

P1因子の正本は`p1-reductions.json.events`と`source-correction.json.p1_factors`のjoinである。順序はold-global-ascending-embedded-original-lead、次にnew-owner-major-ascending-original-lead（[965:646](../search/d972_r07_selected_cycle_materializer_v1.py#L646)）。`p1-roots.roots`のnode昇順やalpha配列順に置き換えない。W_i内のP1 scaleはそのcanonical recurrenceで一回、外の`-sr(alpha_i)`は別、さらにphysical sigmaは上式の全productに一回だけ掛ける。負の全productをemitする場合は因子順も反転する。

`source-correction.json`は上式Vについてraw-word/P1根/alpha hash、因子順・符号、mod54 pair、全96776 lower-zeroを保存する（[965:733](../search/d972_r07_selected_cycle_materializer_v1.py#L733)）。`physical-literal.json`はVのhash、`accepted_physical_head`、全physical factors、`literal_outer_exponent`、normalized行hashを保存する（[965:821](../search/d972_r07_selected_cycle_materializer_v1.py#L821)）。physical factorの実字段は`pivot_id,offer,lead,scalar,physical_offset,row_sha256`で、literal receiptに`literal_exponent`が追加される（[materializer v3:1239](../search/d972_r07_actual_root_seed_materializer_v3.py#L1239)）。global物理offsetは旧連結ストアでの位置であり、新E個別ファイルのseek位置ではない。

六tagは六つの別wordではない。同じraw-rootを各`SEED_OO`へ代入したFox chainと、同じ(z,eta)のsource liftを`source_from_chain`がjoinし、etaを共有auxの末尾2成分へ入れる（[965:486](../search/d972_r07_selected_cycle_materializer_v1.py#L486)）。同じP1 liftを全lower/topから引いたVのsourceを四character全部のBへ通したものが新raw physical行である（[965:784](../search/d972_r07_selected_cycle_materializer_v1.py#L784)）。四Bはwordを作る四つの操作ではなく、Vのevaluation receiptである。Eへ旧character projectorを余分に掛けない。

このVのsource-lower零と、S_newのphysical-lower零は異なる型である。過去S_pのphysical reduction後はsource lowerが再び非零でもよい。実`physical-literal.source_lower_zero`は`NOT_ASSERTED`、`whole_word_direct_replay/eleven_slot_replay/target_word_direct_replay`はいずれもfalse。そこへVの零やraw stream EOFを移植しない。

## F3. 混在するreachable DAGと、未保存字段の扱い

最終wordはv518(4.4)のまま

\[
\Delta C_2=\prod_{i=0}^{\text{committed rank}-1}^{\rm insertion}
                      (S_i^{word})^{[a_i]}.
\]

旧full-originのraw wordは[954:`actor_literal`:805](../search/d972_r07_full_origin_refinement_v1.py#L805)と`materialization.relation.raw_events`から、`t W_i t^-1`、全ActRed、whole-character projectorの順に作る。direct inputと`cancelled_nodes`を含む参照集合が保存されている（[954:830](../search/d972_r07_full_origin_refinement_v1.py#L830)）。`final_coefficients`だけへ潰すとliteral ancestryを失う。old seed・P1 projector・actor nesting・Connの式はreply958 F2/v518をそのまま用い、E部分だけF2を追加する。

| typed namespace / 根 | 必須joinと復元単位 |
|---|---|
| `p1:<global node>` | `fixed/canonical-index.json`（または同一旧refinement index）の`instruction_offset,length,sha256,ancestry_sha256,predecessor,p1_sha256,row_sha256,origin/reductions hashes,scale,literal_input_sha256`からP1`instructions.jsonl`をpositioned read。度二cacheはglobal node×36288 bytes、全145152 trit。origin/reductionsのowner-local IDをold/new offsetsへ変換する |
| P1 old-defect / Rel / actor | Task554 prepareの`old_blocks[].record.dag_nodes/seed_reductions/actor_transitions/defect_origins`、各new blockの`dag_nodes`へjoin。new defectの`origin.origin`はprepareのdefect IDでありP1 nodeではない。word/relator dictionary、PURE_Q1_WORDS、owner/character/actor orderを束縛 |
| `conn-lower:<lower pivot ID>` / `conn-raw:<offer>` | base`state/instructions.jsonl`のnested`source`。`kind=skipped`でも元Conn record全体が保存される（[state v2:833](../search/d972_r07_grade2_physical_state_separator_v2.py#L833)）。Conn `source.source.node`はP1 offer、`source.reductions`のIDはlower-pivot挿入順。dependent raw Connにはouter sigmaがない |
| `physical:<global pivot ID>` | baseでは`kind=physical_pivot`を順に採番し、outer`reductions/sigma`、nested Conn sourceを使う（[state v2:874](../search/d972_r07_grade2_physical_state_separator_v2.py#L874)）。後続は各保存delta/stepのinstruction、raw recipe、normalized行receipt。P1 ID/lower pivot IDと同じ整数でも別namespace |
| `raw-e:<artifact/snapshot>:<raw node id>` | 実raw-wordのordered nodesをそのまま参照。tree/normalizer Refは固定geometryとv459辞書へ解決し、全cycleの係数0のedgeもreceiptから落とさない。snapshot・witness・raw-wordのfile hashを必ず含める |
| `target:<accepted HEAD hash>` | Aの全係数列を挿入順にした一つのOrderedProduct。外側0係数のfactorもPower(0)として根へのedgeと元receiptを保持する |

indexは原点全文ではない。[954:`canonical_index`:348](../search/d972_r07_full_origin_refinement_v1.py#L348)が位置とhashを保存し、元P1 instructionには`origin/reductions/scale/old_defect_literal_input_sha256/parent_row_sha256/reduction_parent_sha256`が残る（[P1 v9:`make_instruction`:1770](../search/d972_r07_canonical_p1_dag_degree2_lift_v9.py#L1770)）。旧defectは同[v9:1351](../search/d972_r07_canonical_p1_dag_degree2_lift_v9.py#L1351)のprepare参照で復元できる。新consumerは**最終非零alphaのP1根だけで終わらず、そのprior-only DAGの推移的閉包**を読む。old/new offsetsは `(0,505,1008,1511)` / `(2014,3523,5035,6547)`、local reductionsは所属blockへ束縛する。

未保存なのは(a)混在全pivotのword-root index、(b)P1/Conn/旧origin/Eを接続した共通ordered SLP、(c)その最終rootのnormalized pair、(d)直接11slot replayである。rawのflat stream本体は保存されていないが、typed nodesと固定Refから再emitできる。P1-rootsは選択根のreceiptであって完全なliteral DAGではないが、上の位置参照から展開できる。baseのlower-pivot recordsも消えていないので、語構文のためだけにConn消去をやり直す理由はない。

親物理行が一ファイルに連結されているという前提は追加しない。新readerが`global_pivot_id → artifact-relative payload / offset / length / sha256`を作る。個別deltaのnormalizedファイルはoffset0、baseだけはstate物理storeのoffset。JSONL祖先については一巡のbytes/rolling/EOF認証から行offset/length/hash indexを新consumer出力へ作れる。Task554 bodyは本体hashとJSON pointer、blobはfile hashと行offsetを記録する。OS絶対pathをowner identityへ入れない。

したがって**既存sourceの追改変は不要**。不足は新consumerの実装・その独立照合、および未知の新完成candidate pinである。元rho2のDERIVED identitiesはAのtarget bookkeepingには使えるが、Dが比較するfresh-rho2の実bytes/manifest・同じtyped owner/endpointを代用しない。fresh-rho2 inputは既存の別artifactとして明示的に渡す。

## F4. 次の最小実装単位と公開ABI案

次の一つのversioned producerにA/B/Cの三entry pointを置けばよい。仮称`d972_r07_continuation_positive_word_readout_v1.py`であり、本便では新設していない。入力は971と同じ親集合、`--continuation-root`、`--rho2-root`、rootが確定する`--acceptance` receipt、別`--output`。既存CLIを変更しない。

1. `read_target_history(parents, continuation, acceptance) -> TargetHistory`。F1の全typed pivot表と全target係数、residual payload、selected HEAD・完成数・全named parentsを出す。将来のlinear-zero rootでは`terminal=LINEAR_MEMBERSHIP_CANDIDATE`/kind/lambda不存在/target実零と成功全prefix receiptをjoinする。零以外でもhistoryは読めるがpositive適用は`NOT_APPLICABLE`。HEAD外tailを取り込まず、出力や親をresumeしない。
2. `compile_target_word(history, literal_parents) -> OrderedWordBundle`。F2/F3のprior-only typed referencesをmemoizeし、rootを一つだけ出す。input receiptのclosureとliteral dependencyのclosureを両方保持する。leaf coefficient collectionは補助線形receiptに限り、word rootの置換に使わない。
3. `read_normalized_pair(word_bundle) -> NormalizedPair`。**同じroot**のsigned grammar上でepsilon mod54を再帰計算する。residueは整数0..53（bool不可）でF3 trit/packed3ではない。rが各座標で0,18,36に入ることが18整除、r/18がnormalized F3値である。負のepsilonも標準剰余で扱う。raw repairの二整数は小さなraw SLPで普通整数として再生し、`-epsilon/6`と照合する。P1/physical全語の巨大整数を十進出力したとは記さない。

公開prefix案は`d972.r07.continuation-positive-word.v1`、canonical JSONはASCII/sorted/compact/末尾LF。出力は`target-history.json`、`ancestor-index.json`、`ordered-word.jsonl`、`word-manifest.json`、`normalized-pair.json`、top manifest/result。Aは各factorに`pivot_id,target_scalar,literal_exponent,physical_recipe_ref,row_ref,target_delta_ref`を保存し、順序と係数0を保つ。ancestry ref共通形は`namespace,parent_manifest_sha256,file,file_sha256,offset,length,record_sha256,json_pointer`（非該当位置はnull）とし、owner/source/dictionary/P1/Task554/Task712/fresh-rho2 identityをtopのparent rosterへ結ぶ。

word nodeは`id,type,op,args,receipt_refs,node_sha256`。`id`は0-based連続、node sealは自身のhash字段を除いたcanonical bytes、child argsは`{node,sha256}`で必ずprior-only。opは`Identity/Letter/Rel/Act/OrderedProduct/Inverse/IntegerPower/Ref`に限定する。Relは辞書hashと正確なrelator ID、Actはliteral conjugatorと`P*W*P^-1`、Productは配列順、Powerは普通整数exponentを保存する。F3係数は元receiptに残し、コンパイル時にsrへ一度変換する。tree/normalizerを隠れたruntime evaluatorへ残さず、同じRefから構成した先行ノードへ解決する。共有nodeは最初のDFS後順で一度出し、重複する使用edgeは消さない。

word-manifestは`grammar,owner_sha256,source_sha256,context_manifest_sha256,fresh_rho2_manifest_sha256,parent_roster_sha256,accepted_head_sha256,target_history_sha256,ancestor_index_sha256,nodes_file,root_id,root_sha256,character_order,actor_convention,central_representative,coefficient_rule,eof`を束ねる。`central_representative="sr(0,1,2)=(0,1,-1)"`を明示する。ordered-word fileの全bytes hash、root node hash、元raw word_stream hashを別字段とする。CとTask975 Dは同じword-manifest/root hashを入力にし、Cのpair receiptは`modulus:54,exponent_residues,divisible18,normalized_pair,same_root_sha256,eof`を持つ。source-lower96776、physical-lower32260、top48384、直接11slotのreceiptは別型のままにする。

E差分の必須canaryは以下で足りる。ここでは設計だけであり、実行済みとはしていない。

- omega=2でcentral -1を+2へ変える。source/chainが同じでも同一word/hash gateは拒否する。両epsilon修理が非零のfixtureで三因子順・普通整数冪も固定する。
- P1内部scale2、外alpha2、physical sigma2、target係数を異なる値にした小DAG。scale二重適用、全product inverseの順序反転忘れ、selected_scalarの誤用をそれぞれ拒否する。
- 非可換因子を挟んだ相殺raw eventsをmod3 leaf mapへ潰す変異、node順にP1 eventsを並べ替える変異、旧actorの向き反転を拒否する。数値相殺祖先のreceiptは残る。
- target scalar0のpivotを次のphysical reductionが参照するfixture。0行省略、lead順への再採番、P1/lower/physical IDのnamespace混同、global offsetを個別ファイルへseekする誤りを拒否する。
- step jとsnapshot jの取り違え、前snapshotのwitness、HEAD外の完成physical/pendingを採用する変異を拒否する。読取の前後で親HEADと全入力bytesが不変であることを確認する。
- aux枝のeta単位ベクトルを零にする変異、Eに旧projectorを追加する変異、四Bの一characterを落とす変異を拒否する。六tagと一つのraw rootの結合も切れないことを調べる。
- residue54の18/36を「零pair」と扱う、2を18整除と扱う、-18を負のtritへ格納する、boolを整数に通す変異を拒否する。CがVだけのpairを最終physical/target rootへ移植しても拒否する。

当該gradeのMEMBERには、実target零とAの連鎖、Bの同一ordered root、Cのnormalized零、Task975 Dによるその同じwordの11 typed occurrence再生と印刷済みaggregation、fresh-rho2/完全physical lower零の照合、選択laneの残るside/localization条件が必要である。linear target零だけではその語の受理は完成しない。完全oracle零はSeparator側の別結論でありpositive readoutを起動しない。これらを終えてもfull A0、他floor、cofinal lift、fake/Iharaの結論にはしない。既存P1/Conn/source-map/共有TCBと限定格を保持し、新runのgradeを本便から宣言しない。

判定は `INTAKE_COMPLETE; NEW_CONSUMER_ONLY_FEASIBLE; SAME_WORD_COMPILER_AND_C_D_RUNTIME_PENDING; NEW_CONTINUATION_TERMINAL_UNOBSERVED; GRADE2_NOT_DECIDED; verified=false`。

AUDIT_974_VERDICT:
