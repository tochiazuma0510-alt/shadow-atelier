# Task989 — 固定 lambda batch の producer 移行契約

F1. Task989、共通 Task988、裁定2154の express/CV9正本、裁定2155 snapshot を全文読了した。変更は本返信だけで、実装 source/WF は作っていない。既存 P source・公開共通数学・実保存 metadata の静的読取だけを行う。990返信と新 C source、ローカル Python/import/AST/数値/GAP、network/git/credential、新 agent は用いない。

実親は run33990567016/1、head c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70、artifact9977040548、ZIP304642285 bytes / a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792、64段・rank1450/gen8155・Separator・UNKNOWN_CAP。裁定2154で工房 cross-checked 限定8条として受理された状態である。最後の snapshot/checkpoint は null なので、この最終 lambda の全弦値はまだ保存されていない。旧64段の前進率や character0-only の実測を、次固定 lambda の値へ代入しない。新985/対照986の未来結果・parent pin は使わない。

F2. 第一案は、旧64 prefix を入力親として不変に保つ新しい fixed-lambda batch packet。新 source 名の候補は search/d972_r07_fixed_lambda_cycle_batch_v1.py、schema 候補は d972.r07.fixed-lambda-cycle-batch.v1。どちらも本票の提案であり未作成・未承認。固定 selection snapshot S0=(旧 owner/source/start/fixed、head/rank/gen/target/lambda) と、追加行で進む reduction state Rj を別の型・別の object にする。新 packet の owner/source は新 scope/source と旧親の全 pin を持ち、旧 P971 の same-owner output へ新仕様を継ぎ足さない。

共通 q/kappa/section/cochain/tree は S0 で一回全 EOF、全54433 chord residual と2 auxを保存する。固定 carry basis/fit の下で、既定 chord roster の先頭非零を最大32件選び、各々を六 cycle の別 witness へ写す。P971 current_section_cached:803 と current_tree_cached:1229、O current_roots_and_values:443 / source_cochain:642 / classify_complete:722 が実在の境界である。以下 O=search/d972_r07_section_cochain_oracle_v1.py、E=search/d972_r07_selected_cycle_materializer_v1.py、L=search/d972_r07_complete_oracle_cegar_continuation_v1.py、M=search/d972_r07_actual_root_seed_materializer_v3.py。

F3. そのまま使えない中心は E one_physical_row:821 の remainder_scalar==旧lambdaの非零scalar 要求（824–826）と、L restore_physical:1197 の同じ等式（1220–1222）、L attach_e_delta:501 の各段 Separator 要求である。候補 raw/source/P1/four-B は S0 の q/kappa/lambda を使い、物理消去だけが Rj の旧行＋先採用行を使う。E four_B:784 は selection state を渡して使えるが、one_physical_row 全体や既存一行 result 型は使わない。

各候補 physical row v_i に対し、M physical_reduce:1239 を挿入順で実行して u_i=v_i−sum(a_ij r_j) を得る。u_i=0 なら依存候補として全 recipe と零 remainder を保存し rank/target を変えない。u_i≠0 なら M normalize_pivot:1270 で一回だけ n_i=sigma_i u_i、M update_target:1284 で t_before−t_after=c_i n_i を保存する。旧 lambda の u_i pairing が零でも独立なら採用する。選定 scalar と消去後 scalar は別字段で、lambda0(u_i)=lambda0(v_i)−sum(a_ij lambda0(r_j)) を新しく要求する。各採用行の先行全lead零・新lead monic・target減算の順序と符号は変えない。

F4. 同じ固定 tree/basis から各弦を作る契約。L current_tree_cached:1229 は full scalar arrays を返すが、O classify_complete:722 と L restore_tree:988 は単一 witness、しかも aux 優先／最初の失敗弦だけに束縛されている。この返値を各候補の現 oracle と偽装しない。新 classify_batch は元 arrays を共有し、別の selection receipt と各 candidate-oracle-view を作る必要がある。数値本体の追加は五元 solve と全残差からの roster 選択で足り、別 tree/fit を候補ごとに作らない。

固定 J の五 cycle の tau を列に持つ T、全弦値 v_e=f(z_e)、共通 fit a に対し、roster index i ごとに d_i=T^{-1}tau(z_i)、k_i=z_i−sum_j d_i[j]z_Jj、r_i=v_i−sum_j d_i[j]v_Jj を作る。O solve_five:705、classify_complete:745–755 の式である。r_i が保存 chord-residuals[i] と一致し、tau(k_i)=0、r_i≠0、J 順の五係数と失敗弦先頭の計六 cycle を全部保存する。零係数の cycle-power も ancestry から落とさない。五本の基準 cycle を個別に合法 Omega 語へしたと仮定せず、組み合わせた w 全体へ v547 §4 の固定順三因子修理を行う。

選択規則案は「全弦を評価した後、非零 roster index の昇順先頭 min(k,failed_count)、k=既定32、1≤k≤32」である。これは materialization 数の cap であって弦評価の cap ではない。依存候補を除いて32独立行になるまで後続弦を追加選択する refill はしない。全54433残差、failed_count、全失敗 roster index/edge ID列、先頭 index、selected列を保存する。fit の五本は全残差零でなければ拒否する。32件未満なら実失敗数に応じた selected EOF とし、架空の32枠を埋めない。

aux は常に二値とも評価する。候補方針に合わせた最小案は chord-first とし、failed_count=0 かつ aux≠0 のときだけ最初の非零 coordinate を一件 fallback とする。これは旧 O の aux-first と異なる新 selection policy として owner に明記する必要がある。E selected_raw_word:430–433 は既に c_x/c_y=r_x^9/r_y^9 を実語化できるので、fallback の新算術は不要。aux を未実装にする版を root が選ぶなら UNKNOWN_AUXILIARY_MATERIALIZATION_REQUIRED で止め、COMPLETE_ZERO にしない。chord と aux が共に非零のとき未選択 aux の値も保存し、無視した証明項目にしない。両者とも全零の場合に限り、S0 の COMPLETE_ZERO_CANDIDATE を出せる。

F5. 各候補 E の既存 P API と変更単位は次のとおり。行番号は今回実ファイルを文字列として読んだ値であり、ローカル実行結果ではない。

| API | そのまま残せる数値内容 | 新 adapter の責務 |
| --- | --- | --- |
| L FixedBundle:694 / CachedOracle:662、O PackedRows:409 | 固定 geometry/carry/J、8059 index/mod54、12 reader と元 lead | 旧固定 file を旧 owner の親として認証し、新 packet fixed manifest から外部参照。旧 manifest を新 owner 名へ書換えない |
| O current_roots_and_values:443、L current_section_cached:803 | S0 の全四 B adjoint、P1 cache 一巡、全8059等式 | S0 で一回実計算。親の current_snapshot=null を旧 step63 の q/kappa で埋めない |
| O source_cochain:642 / integrate_tree:654 / chord_values:677、L current_tree_cached:1229 | 同じ S0 の score/f/aux、potential/全弦 residual | common section/cochain/tree を一回。single-witness の封だけは新 batch 型へ分ける |
| E witness_chain:371 / selected_raw_word:390 | 任意の六 cycle witness、raw SLP、同 chain/endpoint/tau/eta、整数修理と signed omega | candidateごとの accepted-like view。first_failed であることは raw helper の仮定ではなく新 selection 側で認証 |
| E source_from_chain:486 | 同じ raw SLP の六 tag direct Fox と full source、homogeneous−section=選定scalar | q/kappa/f/aux は S0 固定、各 raw/source は固有 path。現 reduction state を渡さない |
| E primal_section:646 / consume_source_row:710 | old embedded元lead昇順→new owner元lead昇順、全8059係数、shared8/all-four d1 | 候補ごとの fresh accumulator。P1 は physical新行で置換しない |
| E corrected_source:733、F subtract_lifts:753 | 同じ source の P1 top/lower 一回減算、全96776零、ordered Ref、mod54/18 | source copy の in-place 補正を一回だけ。全参照と scalar の内外の符号を保存 |
| E four_B:784 | corrected top 全四 B 加算と S0 の非零 scalar 等式 | state 引数は immutable selection state。消去後 scalar と混同しない |
| M physical_reduce:1239 / normalize_pivot:1270 / update_target:1284 | growing span の実消去、実非零だけ monic、target差分 | 新 batch-reduction result、依存分岐、選定用lambdaと残差pairingの分離 |
| E fresh_separator:799、M check_final_separator:1301 | 逆挿入順で全行を殺す functional と全行/両target直接dot | 最後に一回の動的全行 finalizer。E の new_target_steps_executed=1 や M separator_after_append:1327 の固定 CURRENT_GENERATION を batch metadata へ持ち込まない |
| L PhaseStore:283 / ensure_phase:1254 / commit_step:1423 / load_prefix:1572 | complete phase→manifest→HEAD、再走せず公開を回復する設計 | 候補数と採用行数、依存候補、最終separator未生成の型を持つ新 store/loader |

F は search/d972_r07_full_origin_refinement_v1.py。source 前提は v547 §4–5、v548 (1.1)/(2.3)/(4.3)/(5.4)、共通 reply964 F1–F6。v548 の線形 R=id−s pi は同じ8059 basis/liftから取り、v547 の語修理 R_word をその線形写像と呼ばない。canonical P1 の指数は同じ signed DAG の residue54 で18整除と quotient mod3を読む。r∈{0,18,36} と r/18 を確認する型は F3 trit 配列と別である。raw w の −epsilon/6 修理だけは普通整数を保持する。omega の代表は 0,1,−1、三因子と各 raw cycle の順序は固定する。

E の source correction 後 V_i は source lower96776零。さらに物理旧行/先採用行を引いた normalized literal は physical lower-zero だが、Conn を引くため source lower-zero を再主張しない。六 source tag の直接計算は、一般 same-word 十一 slot/printed/full filtered の完了ではない。依存候補の物理零は literal word=1 を意味しない。

F6. 非零と独立性を分ける実消去契約。selection scalar s_i=lambda0(v_i)≠0 は旧 span S0 の外を証明するだけで、先採用行 n_j の lambda0 pairing は一般に非零である。従って新 receipt は selection_scalar、old_lambda_raw_pairing、old_lambda_remainder_pairing、ordered reductions、remainder_zero を分け、F3 の恒等式を値で照合する。依存 u_i=0 は新 row/lead/sigma/target_scalar/instruction を null とし、target_before_sha=target_after_sha、physical head/rank/generation 不変。raw→source→primal→P1→four-B と消去の全 recipe、零 remainder EOF、候補 outcome は削除しない。

独立 u_i≠0 は、既採用の全 lead が零であることを実検査して normalize し、n_i の全先行lead零／新lead monic を要求する。sigma を既に正規化済みの P1 行や n_i へ二度掛けない。literal は「V_i に ordered physical factors の −sr(a_ij) を追加した語」を最後に sr(sigma_i) 乗し、target 語の減算は別の c_i=target_before[lead_i] を使う。c_i=0 でも新行は後続の祖先になり得るため保存する。

物理 rolling head は採用行だけで更新し、new instruction.predecessor=直前の physical head、offer=直前 generation、rank/generationは一だけ増加、physical_offset=rank_before×12096 を論理 row offset とする。実 row 所在は parent role/file/offset または新候補 path と hashで別に結ぶ。依存候補は別の outcome chain/cursorだけを進める。候補IDを generation に流用しない。

rank増分は実採用数 j だけで、0≤j≤selected_count≤32。未中断・非零候補あり・正しい旧span/selection pairingなら、最初の候補は旧span消去後に非零で少なくとも一行進む。最初の候補まで零なのに「全部依存」と受理するのは内部不整合である。ただし資源停止前の前進は保証しない。以後の相互独立も保証しない。継承 ambient は48384次元なので j≤48384−rank_before も必要であり、rank約55000という旧観測からの線形外挿を必要段数や予算の根拠にしない。

F7. 最小新 CLI/入力/出力案。旧14親の --state-root/--delta-root/--seed34-root/--packet-root/--refinement-root/--oracle-root/--e-root/--prepare-root/--block-root×4/--p1-root/--task712-root に、実64親 --continuation-root と exact --acceptance、--output、--batch-size 32、明示正整数 --max-seconds/--max-memory-mib、--resume を加える案である。実64親の tuple と全入場 pin は既観測値だけに固定する。新親96の結果を受ける指定はしない。batch-size は owner/selectionへ固定し、同outputのresumeで変更しない。時間/メモリは invocation の上限で、採否・実秒の登録は root の次委嘱に残す。本票では既存上限を新実走の承認へ転用しない。

新 source は L own_dependencies:197 以下の自系 module を一回 import する構成が最小。L boot:583 で受理済み E までの row provider を作り、旧64 stepの manifest/instruction/result/normalized/target/lambda と実成功Cを hash/typed metadataで結び、L attach_e_delta:501 の旧型条件を旧 prefix に限って使う read-only thin loaderを新設する。旧全64の raw/source/primal を新数値として再走しない。全旧 phase の file/hash/EOF は省かず、巨大 JSON は順に解放する。最後の lambda0 は全1450 rowと親/current targetへ一回直接dotし、実 S0 を固定する。旧 L load_prefix:1572 を新 packetへ直接使うと single-witness/one-row separator/旧 owner の新規公開まで持つので、新読み口を切る必要がある。

提案の出力配置は次のとおり。ここで0始まり candidate IDと1始まり採用 row番号は別である。

```text
owner.json / source.json / start.json / parent-layout.json
fixed/manifest.json
selection/start.json
selection/section/   selection/cochain/   selection/tree/
selection/selection.json / selection/oracle-manifest.json
candidates/000000/witness.json / oracle-view.json
candidates/000000/e/{raw,source,primal,p1,B}/manifest.json + 各exact payload
candidates/000000/reduction/{manifest.json,remainder.bin,recipe.json,outcome.json,...}
candidates/000000/manifest.json
rows/000001/manifest.json
final/{manifest.json,separator.json,lambda.bin}  または実Linear receipt
checkpoints/<content-sha>.json / invocations/<id>.json
HEAD / result.json / named diagnostics
```

raw/source/primal/P1/B は L registered_phase_roster:624 と E_ROSTER:367 の array/file型を基礎にする。rawの二file、sourceの四component＋JSON、primalのalpha/ordered events/residue54、P1のroots/全lower remainder/全四top/correction、Bの全四physical/raw/scalar receiptを各候補の固有pathに置く。raw-root 等の local SLP node ID は候補内でだけ使い、outer candidate manifestのowner/S0/witness/phase hashを完全に結ぶ。別候補の同名nodeやsourceを混ぜない。selectionの共通 q/kappa/f は一つの immutable bytes を参照し、aliasで可変target親列を伸ばさない。

新 schema の最低字段案は以下。共通 wire の最終キー名と hash対象は root が988/989から決めるため、これは未公刊案である。

| 新 typed receipt | 必須の結合 |
| --- | --- |
| .owner/.source/.start | 新formula/source/runtime/scope、旧accepted owner/source/start/HEAD/C/fixed、初期1450/8155/64、元rho2/既存DERIVED親列、k/selection policy |
| .selection-snapshot | selection_head/rank/gen/target/lambda hash、固定資料hash、全8059/54433/2 EOF、shared section/cochain/tree manifest |
| .selection | full residual/failed-index/edge列のhash/件数、先頭index、selected IDs/順序、五basis/fit、aux両値、k、fallback種類、selected EOF |
| .candidate-oracle-view/.candidate | candidate ID、roster index/edge、同S0/selection/oracle hash、六cycle/d/eta/tau/scalar、各固有phase hashと前phase |
| .reduction/.outcome | selection scalar、旧lambda残差pairingと全ordered reduction、growing parent head、zero/nonzero、採用時だけlead/sigma/target delta/row/rolling hash、依存時のnull fields |
| .head/.checkpoint | accepted_parent_completed_steps=64、selected_count、processed_candidates、accepted_new_rows、rank/gen/head/target、last candidate/row manifest、共通selection snapshot、current candidate/last completed phase、separator_ready |
| .batch-separator/.result | 全採用列を含むrow EOF/直接pairing、初期targetと最終target dot1、別DERIVED chain、current lambda hash、terminal/未計算post-batch oracle、全counts・assurance |

canonical JSON は既存どおり ASCII/sorted compact/final LF、sealはsha字段を除いたcanonical bytes、file参照はseal込み全bytes SHA。u8 trit=0..2、packed3=base3の4 trit/byte（値0..80）、u32le index と root sentinel、residue54=0..53を別型にする。全roster/shape/bytes/EOFは型ごとに固定し、dependencyだから任意fileを許容しない。

F8. 中断と最終 separator。新 HEAD の途中 kind は BatchReductionState とし、selection_lambda_sha256 は immutable S0 を指すだけ、current_separator は null/NOT_COMPUTED と明記する。旧 lambda0 を増大spanの Separator と表示しない。physical lower-zero rowsとtarget差分自体は完成したものだけ durably commitできる。rank/genはaccepted_new_rows、候補cursorはprocessed_candidatesへ一対一に結ぶ。

各 candidate の completed phase は .pending-<phase>-<uuid> へ payload/manifestを fsync 後に atomic 公開する。完了 reduction→採用row manifest（採用時だけ）→candidate outcome manifest→checkpoint→HEAD を一回の公開列として扱い、その間に協調停止判定を挟まない。HEADより一つ先に完成 reduction がある crashでは、全 S0/候補/phase/growing-parent hash を確かめ、同じ公開列を完結させる。raw/P1/消去の builderを再実行して同じ行を二度数えない。依存候補も outcome公開済みならcursorだけ一回進める。

再開は同 owner/source/parent/固定selection/kと既完了全phaseを認証する。未完phaseはそのphaseだけ再実行、完了phaseは復元、古い候補・採用済みrow・旧64prefixは数え直さない。限定された pending/orphan 名以外のextraは拒否し、未完payload・到達不能番号をcomplete candidateにしない。HEAD未作成の停止はcandidate=falseの初期化診断、HEAD後の資源停止はUNKNOWN_RESOURCEと完成prefix/checkpointを返す。最終lambdaが未作成ならそのnullを保つ。

全 selected 候補を処理してtarget非零なら、全旧行＋実採用j行に対する dynamic reverse-insertion solverを一回実行する。最終 target の最初のfree座標で非零値の逆元を置き、全recordsを逆挿入順で処理し、M check_final_separator:1301 の全row dot0、batch初期target/最終target dot1を実測する。これは最終lambda1でありlambda0の値を流用しない。原rho2−base remainder、saved seed/packet/refinement/E/旧64、新採用j件の target差分を全て名前付きで保持し、rho2のDERIVED値1とactual target dot1を分ける。新target差分の数はprocessed_candidatesではなくaccepted_new_rows、旧64は親列のまま不変にする。

この状態は BATCH_COMPLETE_CANDIDATE / Separator で、lambda1の oracle は NOT_COMPUTED。lambda0 の残差を lambda1 のcurrent COMPLETE_ZEROとしない。次lambdaの自動batchをこの最小版には含めない。途中でtargetが実零になれば、その採用row/outcome/HEADを保存してLINEAR_MEMBERSHIP_CANDIDATE、lambda=nullで停止できる。selectedだが未処理のtailは明示し、selected全処理EOFを主張しない。same-word readout/十一slot/side-localizationは別consumerのままである。最初の全oracleが弦/auxとも零なら、row追加無しでS0のCOMPLETE_ZERO_CANDIDATEとConn/complete-source前提を返す。

F9. 別 packet と新 continuation 版の工数比較。時間の見積りではなく、必要な変更面を比較する。

| 案 | 新しい実装単位 | 不変・移行上の負担 |
| --- | --- | --- |
| 別 fixed-lambda packet（推奨） | 旧64thin入場、batch selector、候補view、依存可能な物理消去/最終separator、二cursor付きdurable store、限定CLI | 旧64output/owner/source/start/WFを全部保存親にする。新schemaの範囲が一つのS0/≤32候補で終わり、旧C/旧same-word readerへ互換を装わない |
| 新 continuation v2 | 上記に加え、batch間loop、旧64→新step/batchのversion dispatch、current snapshot/HEAD/result、resume/cap/invocation、checkerとsame-word downstreamの新型入場 | 新source/owner/startが必要。旧source pinを保ったin-place継続は不可。旧64 countsをreset/relabelせず、親64+各batch採用数を全chainで保持。末尾lambdaから次oracleを毎回新計算し、停止/cap型を追加 |

旧六phase E算術と固定source資料は両案で再利用できる。別packetでも最終stateを旧P971のsame-owner HEADとしてそのままresumeできるわけではない。下流へ接続するには、実成功packetと全result/新row/依存recipeを読む新 consumer が必要である。旧same-word A/B/C/Dが新batch recipeを既に理解するとはしない。新continuation版へ初めから広げると、今回の「同lambdaで多数候補」の対照以外の変更が増えるため、最初は一packetの実測に限定する。

F10. 最小の識別力ある GHA canary案。まだ実装・実行しておらず、旧成功suiteを再走する発注でもない。新本番helperと同じserialization/phase publication/reduction経路を使う三群で足りる。

(1) batch selection/EOF群。小さなrank5 tau fixtureで、基準五本＋複数非零/零弦を持ち、先頭k件の順序、全tailの失敗数、全六cycle（零powerを含む）、d/tau/scalarを確認する。最後の残差だけを改変、EOFをfalse、別lambda/fit/witness hashを同じ見かけのcandidateに混入した逆対照は拒否する。全chord零・auxだけ非零は既存ninth-power fallbackまたは明示UNKNOWNへ、全chord/aux零だけはCOMPLETE_ZEROへ分岐させる。末尾失敗を読まずにzeroとするselectorを通さない。

(2) actual physical packed経路の三候補群。P=F3^48384の先頭三座標だけを使い、旧span=<e0>、lambda0=e1*、target0=e1とする紙fixtureを本番M helperへ渡す。候補の順は v1=e1+e2、v2=2(e1+e2)、v3=e1。selection scalarは1,2,1。実消去の期待は、v1採用、v2依存、v3のremainder=2e2をsigma=2で採用、旧lambdaの第三残差pairingは0、target scalar列は1,null,2、最後target実零、処理数3/採用数2である。このfixtureは非零scalarを無条件appendする誤り、pairing0の独立行を拒否する誤り、target符号、二重scale、依存cursorとrank混同を判別する。packed4-trit base3の実幅/EOFを使い、byte81/2-bit読みを拒否する。これは小さな線形/metadata fixtureであり、実Omega語・実positive端点を生成したとのreceiptを出さない。

(3) durable prefix/isolation群。同じ本番phase/candidate/HEAD helperに、完了phase直後・依存outcome直後・採用reduction公開後HEAD前・最終separator前の停止を注入する。resumeで完了builder再呼出しを禁止し、依存cursor/採用rankを一度だけ進め、同selection bytesを保つ。異なるS0/k/parent source、resealした別候補phase、欠けたpayload/余計なfileを拒否する。初期DERIVED親列を保持したままcurrent親列だけ延びるalias対照も入れる。全countsはtype intを要求し、boolを件数1に読み替えない。

F11. メモリ・I/O・TCBの境界。最小案は候補を一件ずつ処理し、共通A–Dだけを一つ保持する。各候補のraw/source/primal/P1/physical buffersと大きなrecipe JSONを完了後に解放する。PhaseStore.values/rawsを32候補分常駐させない。以下の幅は既存ABIの整数式で、新runの実測peakではない。

| 主な対象 | 保存・常駐の扱い |
| --- | --- |
| canonical P1 top cache | packed292444992 bytesはfile。O443の16行chunkはpacked16×36288、decoded16×4×36288、uint32 product等の一時配列。8059行全denseを常駐させない |
| Task554の12 lower blobs | 合計67011332 bytesはfile。PackedRowsはhandleと一行decode、元lead順seek。毎候補全8059primal算術は残る |
| geometry/carry/tree | N=54432、next/prev[N,2] u32、phi[6,N] u32、parent/edge/order[N] u32、carry[108864,5] u8、tau[54433,5] u8等を一つ。全chord×physical行列を作らない |
| 共通lambda可変値 | q[4,36288]、P1-values[4,8059]、kappa[96776]、score[6,2,54432]、f[108864]、potential/全chord scalar。S0固定で一組 |
| 一候補 | source lower96776＋top145152＋aux込みfull241928 decoded bytes、alpha8059、raw chain108864、四B physical[4,48384]、raw/remainder/normalized/target各48384。dtype昇格とraw Foxのsigned scratchは別途必要 |
| physical echelon | 初期1450×12096=17539200 packed bytes＋records。新候補≤32なので新rowは最大32×12096=387072 bytes。dense全basis/候補全体の複製を避ける |
| 未定量の常駐部分 | 四B triplet Python object、PSL/Q0/Q2/source context、RightMaps cache、canonical-index/SLP/receipt object、importした既存module。file bytesからPython peakを決めない |

L FixedBundle/CachedOracleの認証済みreader共有は既存TCBの再利用である。一方 F subtract_lifts:753 は各候補について12 blobを全hash/EOFまで読むので、既存APIを呼ぶ最小版ではそのI/Oが候補数分残る。primalのold→new計算とselected P1 top読み、六tag direct source、全四B sparse走査、物理消去も候補ごとである。「lambda固定だからE全体が一回」とはしない。RightMaps/normalizer/depthの候補間共有やmulti-RHS primal、h_i/Gamma vector cacheは別の追加変更で、本票の最小実装に入れない。

有意な計測は common A–D秒/bytes、候補ごとのraw/source/primal/P1/B/reduce秒、selected_count/processed_count/accepted_new_rows、alpha support、実消去数、target scalar列、失敗全数/先頭index、最終separator秒、RSS/VmPeak等である。出力payload_bytesを入力I/OやRAM peakと呼ばない。旧同lambda再計算を省けても、その割合や速度改善は未観測。旧P971のsource9本に新wrapperを加える程度の自系closureを出発案とするが、最終import closure/bytes/hashは実装時にfreezeし、新source hashを今は置かない。保持 sparse_adjoint/vectorized_projection_chunk/geometry/source primitives のTCB共有は残り、新しく第三の独立系を得たと称さない。

F12. 静的読取のsource pinと実行由来。Oは73290 bytes / 4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb（Task959 producer run33975617653、保存出力の成功checker completion33977701313）。Eは88929 bytes / 4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3（Task965 run33981657987）。Lは126940 bytes / 67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c（Task971原run33984832010、保存32のcompletion33988391926、今回受理64のrun33990567016）。Mは86643 bytes / 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332。これらは今回実fileのbytes/hashを再確認した。実行番号は保存来歴の識別であり、本便が再走した番号ではない。

結論は、別packet型でA–D共有・候補別E・依存可能な実消去・最後の一回separatorを持つ移行が最小である。必要な変更点は source API上で具体的に分離できる。rootが共通Task988と本票からwire/有限上限/新source委嘱を決めるまでは実装しない。grade2/whole positive/side条件/complete-source/Conn、現precision-two/四character/8059/54433/2auxの射程を保ち、rank増分32・所要時間改善・必要batch数を先取りしない。

判定: STATIC_PRODUCER_MIGRATION_CONTRACT_COMPLETE; SEPARATE_FIXED_LAMBDA_PACKET_RECOMMENDED; SELECTION_REDUCTION_FINAL_SEPARATOR_TYPES_SEPARATED; DEPENDENT_RECIPES_AND_DURABLE_CURSORS_REQUIRED; SOURCE_IMPLEMENTATION_AND_NUMERICAL_PREFLIGHT_NOT_RUN; COMMON_WIRE_ROOT_PENDING; GRADE2_NOT_DECIDED; verified=false。

AUDIT_989_VERDICT:
