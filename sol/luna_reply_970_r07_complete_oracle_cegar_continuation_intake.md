# Task970 — 完全 oracle＋E 継続器の最小 intake

Task970を全文読み、指定replyだけを作成した。結論は、**既存の動的算術入口を使い、親load・固定資料の寿命・snapshotの封・phase checkpointを新しいversioned wrapperで接続できる**。設計上の数学blockerは見つからない。Task965 source/replyは凍結したまま、Task966/967 releaseの追加条件にはしない。新実装・workflow・ローカル数値/Python/import/AST/GAP・network/git/credential・追加agentはない。

以下、`O`=`search/d972_r07_section_cochain_oracle_v1.py`、`E`=`search/d972_r07_selected_cycle_materializer_v1.py`、`F`=`search/d972_r07_full_origin_refinement_v1.py`、`M`=`search/d972_r07_actual_root_seed_materializer_v3.py`、`B`=`search/d972_r07_actual_grade2_root_scalar_batch_v2.py`、`C`=`search/check_d972_r07_section_cochain_oracle_v2.py`。行は本便読取時の凍結sourceに対するもの。checkerは公開signature・serializer境界と正式reply960/968を読み、新算術helper本文をproducerへ取り込んでいない。957/958/963/964の数学は再説明しない。

起点は成功oracle completion **33977701313/1**、artifact9972829869、rank1385/gen8090、lambda `1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1`、state head `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`。Eの実run結果・artifact・新stateは未観測。本便には未来のrank・SHA・実時間を置かない。登録宇宙は同じfive-carry kernel＋二eta、54432 vertices/108864 edges、六tag・四character、8059 P1・96776 lower、四B・48384 physical、retained Connで固定する。

## 1. 一行deltaをcurrent stateへ接続する入口

| 実在API | 現在の返値／制約 | 最小adapter |
|---|---|---|
| O:925 `accepted_snapshot(refinement,p2,m,base,descriptors,args)` | `(state,start,owner,p1,task554,tables)`。保存26段のtyped bytesをattachし、最後に全current row/両targetへ直接dot。旧scan/insertを再実行しない | 初回bootだけに使い、受理済みrank1385のanchorを得る |
| E:972 `read_oracle(oracle,root)` | 固定completionの全roster/hash/EOFと成功checker、snapshotを認証し、`objects/layout/stages/arrays/witness/q/kappa/f/b_aux/geometry` を返す | 起点の一回だけ。次lambdaの内部oracleをこの固定pin loaderへ通さない |
| E:821 `one_physical_row(oracle,m,state,start,owner,source_pin,accepted,raw,source,primal,corrected,physical)` | 動的stateから一行を計算し、`remainder/normalized/literal/instruction/target/lambda/result` を返す。state自身はadvanceしない | 新wrapperが返値を封印してから一度だけstateをadvanceする |
| E:1132 `run_actual(args)`／E:1092 `PayloadWriter` | 固定親一致・fresh output専用。manifest→HEADはE:1227以降。manifestのrank字段はなく、rank/genはHEADまたはresultのafter fields | 数学入口は保持し、固定親／一行output wrapperだけを置換。既存CLIを反復呼出してpinを書き換える方式にはしない |
| F:954 `advance_state(m,state,manifest,instruction,normalized,target,lambda_raw)` | records/rows/leadsを追加、previous targetを保存しcurrent scanをnullにする。F固有のmanifest.step/rank/generation/kindを要求 | 動作の型を参照した専用E-delta attachを新設。E manifestをそのまま渡さない |
| M:1239 `physical_reduce(raw,pivots,rows)`、:1270 `normalize_pivot(remainder,old_leads)`、:1284 `update_target(old,normalized,lead,old_leads)` | 動的rowsを挿入順で扱う。physical offsetは論理IDであり、各row bytesの所在とは別 | 新行を別fileで持つrow-providerとrecords索引を保つ。巨大な連結basis fileの再作成は不要 |

外部の実Eをbootへ加える条件は、実candidate/成功checkerのtupleと全entryを一回固定できた場合だけである。`HEAD/result/manifest/start/source/owner/instruction`、全payload roster、current parent head/target/lambda、原oracle manifest/witness、source closureをjoinする。rolling instructionは `SHA(parent_state_head bytes + canonical(unsigned instruction))`、`offer=parent generation`、`rank_after=rank_before+1`、`generation_after=generation_before+1`、`physical_offset=parent rank*12096`、plain target三字段とscalar0合法を要求する。これは旧Eのsource/P1/insert算術の再走ではない。

attachは `records += {offer,lead,physical_offset,rank,rolling_sha256}`、`rows += normalized bytes`、`leads += lead`、`previous_target_raw = old target`、current target/head/rank/gen更新で足りる。新行の正規化・旧lead零、全manifest hash/EOFを認証する。target非零なら保存lambdaをloadし全current rowsと両targetへ直接dotを行う。target零なら`kind=LinearMembershipCandidate,lambda=None`を保持してTask958へ分岐する。Eが未完・UNKNOWN_RESOURCE・checker未完ならbootの新accepted rowには加えない。

名前空間は、canonical P1の `node0..8058 + accepted index/instruction/cache hash` と、physicalの `base/refinement/E-import/loop-step + global pivot_id/offer/row hash` を分ける。既存P1 RefのIDを新physical row IDに再利用しない。原oracle producerはc57a7222…/v1、成功checkerはbbce98d8…/v2 completion、実Eは将来受領する第三の由来である。新loopのowner/sourceでこれらの原receiptを上書きしない。

**DERIVEDの形を揃える小adapterは必須。** E:851の`target_derivation`は原rho2 hash・全既存親・new_deltaを保持するが、E:815の新`separator.lambda_rho2`はこれを内側の`target_derivation`に置く。次のE:852は`start.lambda_rho2.original_rho2_packed_sha256`を直接読むため、前のseparatorをそのままstartへ代入できない。動的start builderがanchorの原hashとbase/seed30/seed34/packet/26段の親を保持し、各新Eのmanifest/result/plain-target/instruction/state hashを明示した親参照を加える。原identityと各 `r_parent-r_child = target.scalar*S_new` を保ち、実current-target dot1とDERIVED rho2を分ける。

## 2. 固定資料とlambda依存資料

| run内で固定して保持するもの | 各current lambdaで作り直すもの |
|---|---|
| marked Q0/Q2、qid順、六tag/transport、RightMaps、正BFS、next/prev/phi、carry、chord roster | 四root `q=B*lambda`、全4×8059 P1 values、chi |
| carryのtree potential、全chord tau、最初の五独立chordとその行列。選択順は固定 | 同じ元normalized rowsに対するnew→oldのdual、beta/kappa、最後の全8059等式 |
| canonical P1 index/positioned instruction/cache pins、Task554の元leads・owner/local IDs・12blob descriptors/readers、literal exponent residue mod54 | score/f/b_aux、fのtree potential、全54433 chord values/residuals、fit、同じlambdaのwitness |
| 四BとConnの受理前提、normalizer dictionary/words、source/runtime closure | 選択witnessのraw SLP/chain/full source、alpha/events/補正top、四B合計、新一行/target/freshlambda |

実在する可変算術入口は O:443 `current_roots_and_values(base,tables,state,p1)` → O:470 `current_section(base,tables,state,p1,task554)` → O:642 `source_cochain(arith,context,geometry,section)` → O:771 `complete_tree_test(geometry,cochain)`。stateのrankを固定値として数値solverへ埋めたものではない。E側も :390 `selected_raw_word(oracle,arith,context,accepted)` → :486 `source_from_chain(oracle,refinement,m,arith,context,accepted,raw)` → :646 `primal_section(oracle,m,segments,parts)` → :733 `corrected_source(oracle,refinement,m,p1,index,segments,pairs,raw,source,primal)` → :784 `four_B(oracle,m,tables,state,accepted,corrected)` → :821一行に分かれている。

固定化には次の現物差分を明示する必要がある。

- O:43/50/62のREFINEMENT定数、E:31/38/50のORACLE定数はbootの一つの受理親。O:1142とE:1132のrun wrapperは毎回そこへ戻り、fresh directoryを要求する。動的start/accepted-like objectは新wrapperで作り、凍結moduleの定数やschemaをmonkeypatchしない。
- `B:360 source_context()`はwordsを再読して`_SeedContext`を新構築する。O:232/E:128の依存loadはmodule import・`sys.modules`・deadline hookに副作用がある。これらはprocess初期化で一回。raw sourceに必要なcontext/mapsをloop外に保持する。
- O:470は毎lambdaでTask554五bodyを再parseし、O:409 `PackedRows(root,descriptor)`は生成ごとに全blob hashを読む。old gradeとnew basisは最終8059等式で再openされる。`B:722 _state_descriptor(...,need_blobs=True)`自身もbody全読込/validationである。新しいfixed-basis builderで一bodyずつ認証し、必要なleads/descriptors/小metadataだけ残す。readersの寿命をloopへ上げる。hashを一度読んだことと、各RHSの算術用row読取を省いたことは区別する。
- E:571 `basis_segments(...)`の五body/全8059 mod54はlambda非依存。E:646は毎回12 readersを開き、E:733→F:753 `subtract_lifts`は選択topと全12lower blobを読み、さらにP1 instructions全file hashを取り直す。positioned row/instruction receiptsを保つhandle/index adapterを作れば再認証をまとめられるが、全top補正とlower再構成の等式は残す。原blobを変更しない契約の下で同じ開いたfileを使い、resumeでは固定資料を再認証する。
- O:443のP1 contractionは各lambdaで全cacheの実一巡が必要。前lambdaのchiを使わない。O:771は固定carry potential/tau/五独立chordまで毎回計算するので、そこだけを固定receiptへ分離できる。f potential/fit/residual/witnessは毎回更新する。O:619は`geometry['maps']`を必要とし、E:972が返す保存geometryにはmapsが無い。保存array loaderが同じcontextの`RightMaps`を一回付加する。
- O:211のgeometry stage manifestは`owner_sha256`と`snapshot_sha256`を持つ。固定arrayが同じでも、前snapshotのmanifestを新snapshotのものと称して再利用しない。固定geometry owner/manifestを別に作り、各current oracle stageからそのhashを参照する。

dualは **new owner順・元lead降順→old embedded元lead降順**（O:426/470）、E primalは **old embedded元lead昇順→new owner順・元lead昇順**（E:646）。physicalは挿入順消去／逆挿入順separator（M:1239、E:799）。file row順や一つの共通「逆順」に置き換えない。Gammaは本便の最小adapterに含めない。

## 3. 一stepの状態遷移

現在snapshotを `S=(owner/source/fixed geometry/index hashes, physical head, rank, generation, target hash, lambda hash)` とする。`Separator`のときだけ、Sへ結ぶsection→cochain→treeを全EOFまで作る。途中値や前snapshotのwitnessをEへ渡さない。

| 実際に得られた状態 | 次の動作・保存物 |
|---|---|
| 全8059/54433/2完了、COMPLETE_ZERO_CANDIDATE | 同じcurrent lambdaと全oracle arrays/EOFを封印。v548のcomplete-source/Conn前提付きseparator候補で停止。Eなし |
| 全EOF、VIOLATION_CANDIDATE | oracle manifest/witness/current Sが一致する一つのraw/P1/四B/Eだけを実体化。原six-cycleの零係数やevent順を残す |
| E完了、target非零 | `selected=homogeneous-section=corrected=physical=remainder !=0`を要求。normalize一回、rank/genを実親から+1、target scalar0も保存。freshlambdaで全current rows/両targetを確認し、次Sへadvance。次oracle cursorはnull |
| E完了、target零 | 一行と全target差分を保存しLINEAR_MEMBERSHIP_CANDIDATE。lambdaなし。Task958へ渡し、余分なoracleを走らせない |
| cap到達 | UNKNOWN_CAP。完成current oracleが既にあれば保持する。cap確認のためだけに新oracleを強制しない |
| missing／未完phase／期限 | missingは未計算cursor、期限はUNKNOWN_RESOURCE。完成phaseだけ保持し、零・非零・PASSへ読み替えない。hash/type不一致はREJECTEDで停止 |

Eの全出力rosterはreply965のまま保持する。source-lower零は補正V_word、physical-lower零はConnも引いたnormalized literalに属する。次stateへ移るたび、前lambdaのoracleをcurrentとして使えない。仮に一部raw witness bytesを再参照できても、新snapshotの全oracle EOFとそのwitness scalarの再結合が必要である。

## 4. cap/resumeの最小ABI案

以下は**次の別委嘱へ渡す新schema案**であり、既存export・未来source SHAではない。初期の外部Eを採る場合はその実receiptを`start.imported_e`へ置き、loopの`completed_steps`は0から始める。外部Eの一行を新loopの成果として二重に数えない。capはこの同じoutputでcommitした新E数の絶対上限とし、resumeのたびにcountを0へ戻さない。cap/time/launchはinvocation receiptへ置き、ownerを変えずにcapを引き上げられるようにする。具体的cap値は本便では指定しない。

最小保存構成は、immutable `owner/source/start`、`fixed/manifest`とgeometry/P1 metadata、`snapshots/<step>/start.json`とそのoracle stages、`steps/<step>/e/`、各step manifest、root `HEAD`、停止result/diagnosticである。fixed ownerは全source/data/geometry/tag/P1/index/12blobs/四B/Conn/formulaのhashを固定し、lambda/rank/capを含めない。current snapshot startは毎回physical head/rank/gen/target/lambdaと完全なDERIVED親列を持つ。

HEADの最小字段は `owner_sha256,source_sha256,start_sha256,fixed_manifest_sha256,completed_steps,last_step_manifest_sha256,state_head,rank,generation,kind,target_sha256,lambda_sha256,current_snapshot_sha256,checkpoint_sha256`。checkpointは `snapshot_sha256,physical_parent_head,last_complete_phase,phase_manifest_hashes,current_oracle_manifest_sha256,witness_sha256`。未計算の参照はnull、零arrayのhashで表さない。各step manifestは `step,parent_state_head,state_head,predecessor_step_manifest_sha256,snapshot_sha256,oracle_manifest_sha256,e_manifest_sha256,rank/gen before/after,kind` と全payloadのexact roster/bytes/hash/dtype/shape/EOFを持つ。rolling instructionのpredecessorはphysical head、step manifestのpredecessorは前step manifestであり、二つを混同しない。

phaseの切れ目は、固定初期化後の **oracle section / cochain / tree・top** と、非零時の **E raw / source / primal / P1 / B / physical**。最小版ではphase内の未完row/word-streamを再開せず、そのphaseだけやり直す。完成phaseは再計算しないため、次の薄いphase loaderを新設する。

- oracleはq/kappa、score/f/b_aux、tree全arraysとwitnessを各manifestから読む。tree/top完了前にEへ進めない。
- E rawは保存SLP grammar/Ref/node値・raw-chainをtyped emitterへ戻し、次source phaseの直接tag Foxに使う。rawの完了endpoint検算を再走せず、同じRefとstreamを未完sourceで消費する。
- sourceは四component、primalはalpha/events/mod54、P1は全lower remainder/corrected top/roots/typed correction、Bは全四physical/rawをloadして次phaseへ渡す。primalの未保存live accumulatorを捏造して使わない。primal完了後のlowerは保存したzero receiptとP1段の全reconstruction equalityに結ぶ。
- physical完了bundleは全E payload/result/instructionを含む。ここをdurableにしてからstep manifest、最後にHEADをatomicに進め、RAM stateも一度だけadvanceする。publishとHEADの間に協調停止判定を挟まない。

再開時はF:1090 `load_prefix`の「same owner/start/source、全chain/hash/typeをauthenticateしてrowをattachする」構造を使う。ただしF固有scan/packet/Member schemaを流用しない。boot anchorとimported Eから全新committed stepsを薄くattachし、最後のcurrentlambdaを全row/両targetへ測る。完成oracleがHEADと同じsnapshotへ結ばれていれば再利用し、異なるsnapshotのものは拒否する。F:1179の限定`.pending-*`/`.orphan-*`処理にならい、HEADから到達しない数値tailは計上しない。durable phase manifestだけが先行した場合は、同じsnapshotと直前phase連鎖を認証してcheckpointへ採用できる。認証できないtailを完成phaseと推定しない。

cap/資源停止の後も同じownerとoutputを使い、親stateを再copyして作り直さない。未完初期化、section、cochain、tree、raw、source、primal、P1、B、physicalのどこで止まったかと最後の完全cursorを区別する。旧26scan/insertや旧成功suiteは再計算対象にしない。独立checkerは各新snapshotの全完了oracleと、各新E一行を起点から順に数値照合できる。

## 5. 独立checkerの保持部分と新たな照合

checker側の実在公開入口は C:351 `current_roots_and_contractions(args,state,tables,functional)`、:397 `current_section(args,state,roots,p1_values)`、:502 `complete_tree_test(geometry,f,b_aux)`、:628〜690のstage serializers、:708 `compare_complete_stage(root,payloads,manifest)`。C:892/934/997のcurrent snapshot/start/check wrapperは旧固定親用なので、producerとは別の動的attach/snapshot/loop checkerを作る。Task968のv2修理はu32 root sentinel serializer境界であり、旧array型とsame-byte EOFを維持する。

保持TCBは受理済みConn/source-map/P1 canonical lifts/Task554 normalized rows/Task712 maps、old prefix・target identities、marked group/transport、双方それぞれの旧import lineageとpacking/JSON/runtimeである。既存26scanのF-fo-1や裁定2131限定を次runで遡及して解消したとはしない。起点oracleは候補pinとして消費でき、裁定2137時点のCV9格付け待ちを新stepのcross-checked宣言で置換しない。

新scopeではchecker自身のgeometry/普通27係数sourceと別dual/primal/四B/physicalを使う。各lambdaで全4root・P1 values・同じ最後のkappaの8059式・全score/f/b_aux・54433 chordと2aux・ordered witnessを照合する。各Eでは同じraw wordのQ0/Q2/Fox/epsilon/omega/tau/eta、全六tag/四character/d0/d1/d2、alpha/events、same-word mod54/全Ref、全96776lower、四B合計、physical ordered reductions/一回normalize/plain target/freshlambda/全row・両targetを再計算する。元lambda scalarだけの一致に縮めない。固定geometry/basis metadataはcheckerが独立に一度認証／構築し、全新stageはそのhashとcurrent snapshotへ結ぶ。

新producerの算術helperをcheckerがimportする案は採らない。prefix checkerのresource停止は照合済みcursorと未完を報告し、全new stagesのPASSがそろうまで最終全prefixを受理したとしない。phase再開のinterface canaryはstale witness、capの持越し、stage完了→HEAD前の停止、plain target scalar0、target零分岐、署名source/owner変更を対象にする。旧成功suiteを追加しない。**Task958の同じ最終wordに対する全11 typed slots直接readoutは未実装**であり、linear候補からMEMBERへ進める別consumerが必要である。

## 6. 固定complete packetとの比較に使う次の実測

次の一個のEから使えるのは、raw SLP実長/上界・実chain/source support、alpha supportとordered events、四B/physical support・reduction数、raw/source/primal/P1/B/physical各実時間、実際のtarget scalarと完了／資源停止位置だけである。E:1113のtelemetry `bytes` は**当該stageの出力payload bytes**であり、入力読込bytes・hash traffic・peak memoryではない。これをTask964のI/O費用へそのまま代入しない。一つの非零scalarやalpha supportから残iteration数・他のsourceの疎性・全体速度を予測しない。

比較用に追加profileを別途委嘱するなら、(a)固定資料の認証/parse/reader構築を算術row読取から分けたbytes/回数、(b)P1 contractionと元lead dual/primal・selected top・全lower reconstructionのread/AXPY量、(c)四Bの実entry数とselected source座標support、(d)Task964のh/Gamma候補についてcache構築/保持量と全8059 **physical vector** 等式の費用、を測る。測定しても `kappa(b_i)=chi_i`、`lower(raw-sum alpha_i*lift_i)=0`、`sum四B=selected physical` を保持する。hを`G(tilde_b_i)`と呼ばず、Gammaをcurrent scalar一致だけで受理しない。

最小継続器の実装範囲は **動的E attach/DERIVED start、固定geometry・P1 reader bundle、current oracle→E wrapper、phase commit/load/resume、独立全新prefix checker** の五点で固まった。固定complete packetやGammaは任意の別方式であり、今回のE実走または次継続器の開始条件に加えない。未来E結果・source/run/artifact hashは未観測のまま、以後は別委嘱で実装する。

AUDIT_970_VERDICT: DESIGN_COMPLETE_DYNAMIC_ORACLE_E_ADAPTER_AND_PHASE_RESUME; NO_NEW_IMPLEMENTATION_OR_RUNTIME; E_RESULT_PINS_UNOBSERVED; NO_TERMINAL_OR_PERFORMANCE_PREDICTION; verified=false
