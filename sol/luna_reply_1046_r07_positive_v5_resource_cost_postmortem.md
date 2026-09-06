# Task1046 — positive WF5の観測資源コストと限定した次案

F0. 診断・設計監査を完了する。実停止は **UNKNOWN_RESOURCE / literal-DFS / deadline**。次に調べる一案は、Pのprivate node indexを「不変hash＋mod54値」と「mutable incoming count」に分離する限定変更である。時間・memory・cache・scratchの枠を上げず、canonical語・DFS・全読取・算術順序を維持する。I/Oがdeadlineの支配原因だったこと、変更で完走又は高速化することは未確定。実装・新GHAを委嘱又は実行した票ではない。

Task1046を全文読了。変更は本票とTEMPの公開metadata増分集計だけ。P4のprivate cache/index・WordDAG・literal-DFS・resource終了経路を静読し、D4は同一全語の入場・全slot読取という公開境界を確認した。入力tree/source/WF/既存票を変更せず、Python/import/AST/GAP/数学・GHA/network/git/credentials・新agentは使用していない。

F1. 実対象と全pin。run34009883488/1、head `a590fa9a70322145f1c0688a8f14d2c9640b1bf3`。root取得ZIP1373772131 B / `41c95c7171c9192ec1d589a715c911f7470bb69fe520b80558334ad60636ac61`、406 files / 96 dirs / 3685457381 B。局所受領票 `positive-v5-run34009883488-root-resource-metadata-v3.json` は1705905 B / `63050c167ba256ab397f3ac0cdcf1a0be5c81baa96ffaf11cd51086e3e8da395` を独立に再hashした。INCOMPLETE_RESOURCE_METADATA、構造errors0/未完6を保ち、全envelope/16親の別1044受領を代用しない。

| 対象 | bytes | SHA256 |
|---|---:|---|
| P4 search/d972_r07_continuation_positive_word_readout_v4.py | 252342 | f36e929ee303b968c519e0333d18b10d3c3e01d83b9ad8ec896949d5ca02dd77 |
| D4 search/check_d972_r07_continuation_same_word_eleven_slots_v4.py | 232750 | 41d53b3779e26b04431a033877efbd315eb32b1d4538efa742bf900996db797b |
| WF5 .github/workflows/d972-r07-continuation-positive-word-readout-v5.yml | 180687 | a840cebcd0ba3f15ff2c31c13b0a09bacd140cb4c8e756466baafd052df8e436 |
| resource-P/telemetry.jsonl | 5626335 | f58678cec39264f66d456bbb0aa64c373b65a84eff87323232b96dfdee63160e |
| P-stdout.json | 514 | 664edc84e7fdaa94d87ed237052dce19694739122f5e189e66b1268ecd43d7e9 |
| executions/P-receipt.json | 815 | 3b27eb40bb30c22ad3711e0d4ea18099849969c1c04406ef0dca010f9a1474de |
| resource-P/result.json | 948 | 019be608da5215d4b1d1604f8aa2f2dda9048db168f21b7a0fe6218db320c8ed |

上表source三本とsmall実JSONは実file bytes/SHAを読んだ。Pのinner5400.275689秒、outer5402.03076秒/exit3はstdoutとexecution receiptの別計時。P.log（19865 B / `56210794be0849a942fc0f0cac1e24564254a81a6619ae218b70d2564f2428ca`）のtracebackはP4:2963→2264→599でdeadlineを示す。通常Dとrun-receiptは未形成。Dfixtureの54 telemetry行受領は通常D実行の証拠にしない。

F2. P全2343 sampleをEOFまでJSONとして読み、sample0..2342の連番、finite/非負/単調elapsed、今回集計する全累積counterの非減少を確認した。PS5.1のsecondsはdecimal/doubleを認め、node/edge/I/O/cache countはint/long。初期に未作成のbuild counterと未使用I/O categoryだけを、ResourceSessionの初期化規則に従って0として差分計算した。source sample自身のsealを別canonicalizerで再構成したとは主張しない。

sample0..199はresource作成・旧history・literal body・P1全indexの200点、elapsed3.237423237..40.674033680。sample200..2341はliteral-DFSの2142点、44.153337340..5397.544869968。最後2342はresource-session-UNKNOWN_RESOURCE、5400.273287329。最大観測間隔4.905991524秒。17種類の全phase別件数と全隣接増分のphase別総和はF8集計に保存した。全9counterのphase別総和・全窓総和は最後と最初の差へ一致した。増分を「区間終端のsampleのphase label」へ割り当てた量であって、各操作のCPU時間や厳密な相別滞在時間ではない。

約900秒ごとに直前の実sampleを端点とし、最後まで重複・欠落なく差分を取った。GBは10^9 Bの論理計数を丸めた表示。

| 実sample区間 / elapsed秒 | Δnodes | Δindex read GB | Δindex write GB | Δword write GB | Δflushes |
|---|---:|---:|---:|---:|---:|
| 0→546 / 3.237→897.844 | 1421312 | 0.000 | 0.000（header48 B） | 0.533 | 0 |
| 546→911 / 897.844→1799.879 | 1495040 | 10.369 | 10.424 | 0.557 | 60596 |
| 911→1274 / 1799.879→2697.773 | 1486848 | 10.420 | 10.483 | 0.567 | 60936 |
| 1274→1637 / 2697.773→3598.590 | 1486848 | 12.274 | 12.337 | 0.556 | 71712 |
| 1637→1997 / 3598.590→4499.124 | 1474560 | 26.111 | 25.976 | 0.549 | 150997 |
| 1997→2342 / 4499.124→5400.273 | 1412826 | 80.582 | 80.708 | 0.526 | 469143 |

F3. cacheとmemoryの確定観測。PAGE_ROWS4096、42 B/record、172032 B/page、388 resident pages、IO reserve344064 B、設定cache＋IO67092480 Bを全sampleで区別して読む。最初のcache満杯観測はsample587/997.652956秒/word nodes1589248。最初のevictionは588/1000.100992秒/nodes1593344で1回。これ以前はindex_read0、index_writeはheaderだけだった。

最終sampleはnodes8777434、edges17446074、word_write3287182712 B、index_read139755802122 B/812385 calls、index_write139927942902 B、misses814527/evictions814139/flushes813384/hits95185162。read一回平均172031.49 B、headerを除くflush平均172031.84 Bでほぼ一page分。最終private index image368652276 Bに対してlogical writeは約379.57倍。ただしread/writeはPython計測した論理量であり、OS page cache、物理block I/O、disk転送量ではない。総miss率約0.848%の小ささだけでもコストを否定できない。

最後sampleのVmRSS/VmHWMは5285089280 B、ru_maxrss換算は5284786176 B。違う取得API/時点の値を同じ測定として丸めない。VmSize最大観測5366702080 Bはsample2125。最初のword sample200で既にVmRSS5131653120 B、VmHWM5252685824 Bあり、disk cacheが1 pageの時点で数GBを占める。したがって現在のRSSを64MiB cacheだけに帰属できない。P2110–2176は旧bodyのdag_nodes等とindexを保持し、2190–2264もrecipe/symbol表を保持するが、parent_object_overhead_bytes/semantic_live_nodes/paused_factor_bytesはnullのままなので各表のbyte内訳は確定しない。

最大fan-in2616、最大canonical line243467 B、max_frames11もsample上の観測値である。最後のframes3、symbols16439、recipe_ref_symbols16442は未完DFSの状態を示し、全必要node数/残り語長/残り時間を与えない。最後indexはclosed=true/durable_rows8777434だがfinished=false、index receiptsは空、root/word manifestはnull。途中sampleはP796のobserve_nodeがappend前なのでword countと確定index rowsを同一視しない。最終強制sampleには最後3802 nodesの処理とabort flush等が含まれ、その2.728秒全部をcleanup時間にしない。

F4. sourceで確定したI/Oへの操作接続。

| P4 source | 確定した操作と依存 |
|---|---|
| 127–130 / 195–258 | `<32sBBQ>`のhash32 B・mod54二値2 B・incoming8 Bを同一pageに置く。LRU missは既存page全read、dirty evictionは使用中page全writeを計数 |
| 296–330 | readはhash/pair/usesを同時unpack。appendは新recordをdirty化。add_useは既存recordをreadし、uint64 overflowを拒否して同じhash/pairとuses+1を全recordへpackし直し、pageをdirty化 |
| 772–805 / 819–836 | link作成、全child id/hash照合、node_residueのpair読取、append、全child add_useが順に走る。同じchild列を複数回読む。零冪edgeや重複edgeも省略していない |
| 230–243 / 457–471 | page flushはbefore_writeの容量/free floor照合後に全write。index_read/writeはこの位置の論理byte/call計数 |
| 492–535 / 594–607 | sampleは4096 node又は5秒等で作り、各sampleをflush/fsync。fsyncやcanonical JSON/OS照会の個別所要時間は計測していない |
| 332–381 / 2952–3029 | build終了の全reachability/EOF/full hashと、別空indexによる全ordered-word再読/mod54/18が必要。今回まだbuildで停止し、reread相へ進んでいない |

hash/mod54自体を変えないincoming更新でもpage全体をwritebackする経路はsourceから確定する。ただし現在のcounterにはimmutable読取とmutable更新の個別call traceがない。各evictionの原因node、全flushがcount更新だけによる割合、CPU/物理disk/serializationの時間内訳は未計測である。最後の約900秒ではI/Oが大きく増える一方、node進捗は前窓1.47–1.50Mに対して1.41Mと小幅な減少にとどまる。これだけからdeadlineをpage I/Oの支配と断定せず、全語の必要作業量自体が時間枠を超える可能性も未解決として残す。

F5. **次の一案: private NodeStoreの不変34 B列とincoming-u64列を分離する。** Node IDを変えず、不変列はhash32＋pair2のappend-only record、counter列は同じnode順のu64として全incomingを厳密加算する。NodeViewは不変列を読み、add_useは元のid/hash/pair認証を保ったままcounter列だけをdirtyにする。既存WordDAG.add / child列の各順序 / canonical JSON / node_residue / TargetWordCompiler.resolve・build群は変更しない。これは巨大framework・新IR・DFS再配置・語簡約・sampling・edge集約を含まない一つのstorage変更である。

最初の登録案はcache予算64MiBを不変列32MiB / counter列32MiBへ固定分割し、それぞれのread/write bufferを各枠内に含める。二つの64MiB cacheを作らない。元のline64MiB、process7168MiB、P5400秒/D10800秒、outer6000/11400秒、scratch16GiB、free floor1GiBを維持する。配分が最適との主張はせず、同じ枠で一つの比較を可能にする固定値である。Pのprivate formatだけを新versionで識別し、D独立codecは共有しない。build/rereadという二つのlogical storeは維持し、各storeの二physical列を同じsource/session/number/countへ束縛する。

F6. 必須の不変量とread-before/write条件。既存child ID<現在ID、child hashの実一致、pair各値0..53、普通整数指数、uint64 count overflow、全零冪/重複edge一件ごとの加算を維持する。不変列のappend bufferにある未flush childも同じ値を返すread-your-writesが必須で、disk未形成を零値で補わない。counter増分を遅延して使い捨てたり、reachabilityをbit/近似へ替えたりしない。不変recordの公開済prefixをcounter更新で再writeせず、未flush末尾とread cacheを区別する。新format/二列の全size/offset/header/binding/EOF/hash・同countを照合し、source/親/元語はread-onlyとする。abort後の二列の不一致や不完全receiptはUNKNOWN/INCOMPLETEで残し、root完成へ昇格させない。

この変更が返すhash/pair/countの列を旧storeと同一に保てれば、同じcall順のcanonical node/DFS語を保つ設計になる。しかしsource静読だけで新実装の全byte同一性を得たことにはしない。新source/resource来歴のseal/hashは版変更で変わるので、13 wrapper files全部の旧byte同一も要求しない。比較対象は同ordered-word bytes、root ID/hash、mod54/18の数学値、同typed slot/physical結果と、それぞれに正しく結ばれた新来歴である。private I/O削減の可能性を、RSS全量の解決や90分内の完走保証へ拡張しない。

F7. 必要な独立照合と次の計測。新storageの通常helperを使う小対照で、現P4および既存P3（200658 B / `bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e`）と同じ短語の全JSONL/root/pairを照合し、cacheを超える往復・未flush末尾・零冪/反復edge・counter境界・片列欠損/改変を実read/flush/finishへ通す。旧全数学suiteの再走を便宜的に追加する案ではない。新private resourcesのfixtureと全保全を公開契約に追加し、未試験の新形式を旧resource受領helperへ黙って通さない。

実失敗runが保存したordered-word prefixは3287182712 B / `443dd41de6aece111fe7d64ebc054e0b6e87cddd27bab89f52931b9f78a3cba3`（rootの全file受領pin）。新fresh実行がこの長さに到達した時、保存元全prefixとのstream bytes/hash一致を追加の非数学metadata対照にできる。元停止時の全語/全rootは存在しないので、これを全語同一の実証にはしない。達しなければ未比較であり、別partialを完成にしない。新語が完成した場合にだけ、D4から数学本文を維持した独立checkerの全13file/全Ref recipe/全8059・four-character/全11slot・80644/全入力不変を要求する（D4:2759–2794、3212–3254）。既存D3のanchor pin176579 B / `273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c` と新独立slot/physicalの小対照も保持し、Pの新private readerをDへ共有しない。

新計測はaggregate旧counterを残し、不変列とcount列別のread/write/calls/dirty flush、実cache予算、logical/durable/actual rows、stream prefix位置、RSS/line/framesを区別する。個別I/O/encode時間を追加するなら通常pathの軽量な累積計時として公開し、未計測の物理disk量を捏造しない。新処理率、完了status、同一prefix到達時点のcounterとtimeを初めて比較する。未観測の残りnode数や予定改善率はこの設計から算出しない。

F8. 再現metadataと完了境界。集計を `%TEMP%/shadow-atelier-audit163/positive-v5-task1046-observed-increments-v1.json`、**52640 B / `b26a49d34ddeee6390a7f0e41987c114ecebbafa7cb240d1167fb7c2225ca496` / LF963 / CR0 / 最終LF** に保存した。入力telemetry pin、全phase件数・全隣接増分のphase別総和、全900秒窓の実端点、cache landmark、最大観測memory、最後の全sampleとsmall JSON pinsを含む。通常JSON読取で全行を読み、各counterの差分X[i]-X[i-1]を取り、各時間境界以下の最後のsampleを窓端点にするだけで再現できる。元telemetry pathはTask1046の実root配下resource-P/telemetry.jsonlである。全metadataは資源観測であり、新しいF3/群/語の演算は行っていない。

当便の完了はこの観測・source接続・一案の限定設計まで。実装の発注とfresh GHA採否はrootが全envelope1044受領と本票を読んで裁定する。k128 WF3監査とは独立であり、sourceを今編集又はdispatchしていない。通常D未開始・P未完、A0 actual0/1・階段1/6・grade2両NOT_DECIDED・verified=falseを維持する。

AUDIT_1046_VERDICT: OBSERVED_DEADLINE_COST_AND_SOURCE_PATH_AUDITED; ONE_BOUNDED_PRIVATE_IMMUTABLE_COUNTER_SPLIT_PROPOSAL; SAME_WORD_AND_RESOURCE_CONTRACT_REQUIRED; CAUSAL_RUNTIME_DOMINANCE_AND_SPEEDUP_NOT_PROVED; NO_IMPLEMENTATION_OR_GHA; NO_COMPLETION_PROMOTION.
