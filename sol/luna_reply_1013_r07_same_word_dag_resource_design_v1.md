# Task1013 — 独立D3のDAG資源調査・D4移行案

**F1 — 調査と実観測の境界。** Task1013を全文読了した。rootによる末尾空行だけの除去後の最終pinは3520 bytes / f4f23a679df3d10215d45c885f645e0d1d2706071884d3a7ef6e77435882e333。変更は本返信だけ。自系 search/check_d972_r07_continuation_same_word_eleven_slots_v3.py（以下D3）の資源に関係する通常経路・呼出し・解放位置を静的に読み、実source 176579 bytes / 273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c を再hashした。新P本文、Task1012票、他系helperは読んでいない。995/1009/1006および公刊sourceは不変。D4のsource・実験・workflowは作成していない。

root公開metadataによる正語run34001672135/1（head14e09d7a96ec9cae71b072e297d2138f5c2f8a72）は、Pのliteral-DFSがMemoryError / UNKNOWN_RESOURCE / exit3、内部182.325646秒で停止し、本語のDは未実行。Pは既に参照SLP/DAGであり、「未展開の文字列をDAG化すれば済む」という診断ではない。7168 MiBは設定上限で、観測peak RSSではない。

自系の実三群stdoutだけは、回収root `%TEMP%/shadow-atelier-positive-readout-run34001672135-diagnostics-a1` の D_SELFTEST-stdout.json 678 bytes / 7ca09522e6f3955fdde2281a7acb0fbb08d3e198f76f30702ad213587decc3be を独立bytes/hash・全文で確認した。三件PASS / actual_parent_artifact_replayed=false。実exit票は0、executions/D_SELFTEST-receipt.jsonは709 bytes / af1b71c8d075b8a53cfba79b2528c15b55e688ecfe17b0fc04d5abf29d59485b、wall_seconds=3.268439。この三群と本語全D成功を混同しない。

回収artifact9979727337の809058240 bytes / 5bc5b2f5890a7da2641aad882ea4c262ec3d538df0e02e474556848842062a31、181 entry / 2506894888 bytes、途中ordered-word.jsonlの2486667939 bytes / 87dee2553995e8b81a953d40f89fd9d472adbd0814026cdf1e10ca58929d07c6はroot公開metadataとして扱う。本便では巨大JSONLの全parse・全hash再走をしていない。末尾id6629828、child6627615、receipt31792、final LFの観測から、全node連番数・全edge数・完成root・全reachabilityは導かない。以下のN/E/R/A/L/support/RSSは未計測の変数である。

**F2 — 現D3の生存期間。** N=完成JSONLの全node数、E=重複を含むchild occurrence総数、R=Ref symbol数、A=ancestor entry数、B=JSONL全bytes、L=最大一行bytesとする。N/Eは完成descriptorと全EOFの照合前に確定しない。K=Refの実recipe照合による追加位置読取回数、その読取bytes和をB_Kとする。Python objectの実sizeof、containerの空き容量、小整数共有、allocator残留は未計測なので、要素数に架空のRSS単価を掛けない。

| 対象・自系位置 | 実際に保持するもの | 生存・費用 |
|---|---|---|
| NodeCatalog.__init__, L407–457 | offsets: N個の(offset,length) tuple、hashes: N個の64字hex、children: N個のtupleとE個のchild位置、uses: N個の参照数、symbols: R個の(namespace,key,scope)→ID | 認証開始から評価終了まで Θ(N+E+R) のPython構造。文字列語の展開を避けてもこの表は全保持。 |
| validate_node, L459–503 | 一行の全dict/args/factors/receipt_refs、Rel字列、prior child照合 | rawとparse結果とcanonical再符号化の一時値が重なる。readlineに明示一行上限はなく、Lと最大fan-inが別のpeak要因。 |
| 初回reachability, L452–457 | reachable setとtodo list、全children表 | 全nodeは一度だけ展開するが重複edgeをtodoへ積むので、setはO(N)、stackは最悪O(E)。constructorを出れば両者は不要になる。 |
| normalized_pair, L516–543 | uses.copy()とlive ID→二つのmod54整数 | remainingは長さNの浅いlist copy。整数を減算代入するので元usesは変えない。live値はlast useで消す。全node・全edgeを走り、Actのconjugatorも認証・計算・消費するが指数寄与はwordだけ。 |
| evaluate_slot, L545–578 | slot一つのremainingとlive ID→FoxValue(endpoint,row dict) | 11slotは逐次でありremaining12個を同時保持しない。ただし各passでN要素copyとE回の減算がある。全node計算後root一件だけ返し、remaining/live容器は関数終了で不要。 |
| RefRecipes.check / expect_pattern, L1828–1916 / L1316–1347 | 全Refのscope/元親recipe、expected構文の作業stack、symbols lookup | 全N行を一回読み、さらにK回の位置読取を行う。同じnodeの反復照合を含むKをNと同一視しない。 |
| check_actual, L2513–2544 | AcceptedInputsの全16親roster/selected、WordFilesの12 JSON、SourceRecipesの8059/P1・旧defect/Conn、PhysicalRecipesの全履歴、AncestorIndex | これらとcatalogがmetadata工程では同居する。意味join・A表・同root mod54・P最終票の照合後、catalog.ancestors/symbolsを空にし、word documentsをclear、source/physical/ancestors/recipes/history/manifestをdelしてからslotへ進む。 |

RefRecipesが保持するtree arraysも上記delで不要になる。AncestorIndex L1167–1234はentriesをdeep copyし、JSON pointerやJSONLの解釈値をself.pointedに保持する。pointedはD3の他の通常関数から参照されないことを静的検索で確認した。空pointerなら親JSON全体、その他でも参照先subtreeが生存するので、del parsedだけではその保持は終わらない。D4の小さい改善候補は、正しい全bytes/hash/pointer型を認証した後にこの未使用解釈値を保持しないこと。entriesと実recipeの意味joinは省かない。SourceRecipesはTask554の旧bodyを必要metadataへ取り出して解放し、新bodyも一つずつ処理するが、取り出した旧metadata・8059命令は上記境界まで残る。state/instructions.jsonlはread_bytes＋splitlinesによりrawと全行の一時listを同時に持つ箇所がある（L1420付近）。

**F3 — 全走査回数とFox費用。** 早期停止せず通常経路を最後まで進む場合、ordered JSONLの全canonical parseは、constructor 1回＋RefRecipes.check 1回＋normalized_pair 1回＋evaluate_slot 11回＝**14回**。さらにexpect_patternのK位置読取と、RefRecipes.check末尾のroot再読一件がある。compare_word_root_manifestはsymbols表を整列して使うので、全node再走査の一回には数えない。WordFilesの前後regular_treeはJSONLをそれぞれ8 MiB chunkで全hashするため、JSONLだけの論理読取bytesは `16B + B_K + root行bytes`（OS page cacheによる物理disk readは別）。全parse呼出しは `14N + K + 1`。exact_jsonの全canonical一致とnode unsigned sealの再hashが各node readにあり、Rel固有の字列hash等はこれに加わる。これは全工程到達を仮定したsource上の式で、今回実Dの測定値ではない。

全16親の前後hash、12 JSONのparse/seal/比較、実ancestor pointer/positionの再読、出力行の書出し/全hashは上式の外側である。AcceptedInputs.readは対象file全bytesを取得するので、大きい親JSONとcanonical比較の一時領域も別に必要。Symbol manifestのソートと整形はR依存、全reachable確認後でもcatalog自体は全slot中に残る。

slot s、時点tのlive node ID集合をH(s,t)、そこから参照される異なるFoxValue/row実体の集合をU(s,t)、行supportをS(v)とする。slot工程のmemoryは概念的に `catalog + remaining(N) + liveのID表 + Σ[v∈U] row表(S(v)) + 演算中間行 + printed蓄積行 + 出力sort + 固定floor/maps/配列`。stageが異なるpeakを全部同時と数えない。Refは同じFoxValueをaliasするため、live_nodesと異なるrow実体数は等しくない。最後のhandleを消してもPython allocator/OSが直ちにRSSを返すとは限らない。

TypedFox L158–203の実則ではProductは左行copyと右行の全translate、Inverseは元行全translate、Actはactor行copyにchild全translateとactor全translateを加える。Actは `D(P)+L_p D(W)−L_(pup^-1)D(P)` の全項を保持し、非単位child/actorを省かない。行項処理の目安はそれぞれ `S(left)+S(right)`、`S(value)`、`2S(actor)+S(child)` に各quotient演算費用が掛かる。Power(k)は負号なら一回Inverse、|k|>0ならpopcount(|k|)回の積とfloor(log2|k|)回の二乗で、各中間supportに依存する。k=0でも元child nodeとedgeは既に全評価・認証してから消費する。最終supportだけでは演算途中のpeakを上から押さえられない。

same_word_eleven L634–731は一slotずつでも、現在blockのold_printed/new_printed/prefix_rowと、前blockのdirect_hexagons二行を保持する。root/base/corrected/factorsをslot後にdelするが、この蓄積は別である。OutputFiles.fox L610–625のsorted(row.items())にもsupportに比例する一時listがある。六E3 slotのcoarse normal辞書とsource arrays、両hexagonのdirect physicalが追加される。CoarseReadout.cacheは8192項でclearする実上限があるが、Fox行の上限ではない。全五E4 endpoint/row・printed比較を省かず、全11slot/80644を予算内に収められるという結論はまだ出ない。

**F4 — metadataの最小移行案。** 第一候補は、同じ公開八opと六字段 `id/type/op/args/receipt_refs/node_sha256` を一切変更せず、D自身が初回全parseから作る固定幅catalogとchild graphへ置き換えること。node IDをcompact化・重複nodeを併合・係数0の枝を削除してはならない。初回の連番、全bytes/SHA/EOF、exact args、Rel字列、全prior child ID/hash、Ref symbol一意性と元16親recipeの順序/係数/scopeを保持する。

| 案 | RAM上の効果と残る費用 | 判断 |
|---|---|---|
| Python表をpacked arrayへ変更 | int/tuple/hex文字列のoverheadは減るが、全N/E bytesをRAMに置く。L・Fox・意味表のpeakは残る。 | 小変更の比較対照には使えるが、収容を前提にしない。 |
| 全表をmmap | Python heapは減る。触ったpageのresident化・page table・OS cacheは残り、仮想mappingだけでRSS一定とは言えない。 | 上限測定なしで解決扱いしない。 |
| 固定幅disk表＋明示予算のpage reader/writer | ID位置を直接読める。更新counterとsymbol lookupにはdisk I/Oが増えるが、Python表の全N/E常駐を避ける。 | 最初のD4候補。Dの同じread/数学則を先に維持する。 |
| 認証後のcompact node IRを全passで使う | 14回のJSON parseを減らせるが、args/普通整数/Refの完全codecが新TCBとなる。 | metadata退避と分けた追加段階。単なるhash付きcacheを原語の代わりの前提にしない。 |

固定幅表の具体案は、nodeごとに `offset:u64, length:u64, node-inner-SHA:32B, line-full-SHA:32B, edge-start:u64, edge-count:u64, total-uses:u64, op:u8, reserved:7B=0` の112 bytes。全edge occurrenceは別 `child:u64` 配列へ、元args順・重複をそのまま8E bytesで保存する。オフセット、長さ、ID、E、加算のoverflowは照合し、表現資源上限を越えればUNKNOWN_RESOURCEへ閉じる。これを数学的無効や途中成功へ変換しない。公開node sealはLF込みcanonicalの従来値、line hashは六字段全canonical bytesの追加内部認証値で、両者を混同しない。

初回は一行ずつactual bytesを認証し、childのhashを既に書かれたprior indexへ結び、total-usesをpage単位で加算する。次にrootだけbitを立て、ID降順にmarked nodeの全childへ伝播すれば、strict prior-onlyによりDFS stackなしで完全reachabilityを計算できる。全N bitが立つこと、unused末尾bit、全edge spanの連続/EOFを確認する。rootが末尾であることだけでは、未到達の旧nodeを排除できない。0冪のchildとActの二childも全てbit伝播・edge countに残す。作業bitsetはceil(N/8) bytes、明示page上限でdiskへ置ける。

symbolsはnamespace/key/scopeの完全な文字列tupleをdiskの一意keyへ置き、元IDと結ぶ。可変長keyは正確なcanonical bytesで比較し、Unicode正規化や短いhashだけの等値判定をしない。sorted symbol_orderの全R件も元manifestへstream照合する。ancestor entryは元10字段とid/位置を保持し、pointer/whole-file/JSONL/binary各型を従来のTask554 descriptor・実recipeへ結ぶ。self.pointedの不要な保持と同時に、parent/wordの巨大JSONを一括保持する境界も別予算として可視化する。

最小版ではNodeCatalog.read相当がなお元JSONLへseekし、line-full-SHA、全canonical bytes、同ID/inner hashを確認する。したがってF3の14回parseは最初から短縮したとは主張しない。一行が大きい場合、まず明示byte枠を持つ一行readerで完全行まで読めるかを判定し、超過をUNKNOWN_RESOURCEにする。行の一部だけをparse・切捨てて進めない。streaming canonical JSON validator/IRは別の複雑さであり、初版の必須前提にしない。

remainingは各pass用の独立u64 disk列へtotal-usesをコピーすれば、追加8N bytesとE回の更新になる。mod54の二値は0..53のu8二個として最大2N bytesをdiskへ置けるが、公開型はF3ではなく普通整数剰余のまま。降順到達用bitset、index、edge列、remaining、mod54だけなら条件付きdisk量は `112N + 8E + ceil(N/8) + 8N + 2N` にheader・symbols・ancestor・page journal等を加えたもの。これはファイル形式の設計式であり、現在のN/Eへ数値代入していない。

代案としてlast-consumer-IDを保存すれば、厳密な昇順全node評価に限り各slotのremaining全copyを省ける。しかし複数edgeを一つに数えたり、同じnodeを二重freeしてはならない。全edge/全usesの認証と演算中pinを保持し、元の参照数方式との完全対照が必要。最初のdisk版では参照数方式を維持し、同時に評価順まで変えない。

**F5 — Fox live値・alias・一時disk。** D3のFoxValueはfrozen dataclassでもrow dict自体はmutableである。ただしProductは左copy、Inverseは新dict、Actはactor copy、row_differenceは左copyであり、通常算術は入力rowを変更しない。Refは既存FoxValueをそのまま共有する。この約束をdisk版でも維持し、node IDごとのhandleと異なるrow実体の所有数を区別する。現在opの全operandは処理完了までpinし、その後、重複を含む全child occurrenceを減算する。count0となったnode handleだけを外し、Refの新handleが同じrowを持つ場合はpayloadを消さない。0冪でもchildの評価と減算は行う。

slotごとに独立したvalue storeを置き、keyは元word全file SHA/root ID/hash/slot ordinal/block/node ID/hash/自系source closure/codec versionへ結ぶ。E3 endpointは40 bytes、E4は154 bytesという自系TypedFox.blob/unblobを用いる。内部rowの候補形式はcomponent:u8＋typed element固定幅＋非零F3係数:u8、すなわち42/156 bytesの一項列で、component範囲、permutation、PC座標、非零係数、重複なし、完全sort/EOFを読む。Pのcodec/cache/helperは採用しない。新書込payloadのsupport/全hash/EOFが完成してからhandleをpublishし、未完成payloadへ通常handleを向けない。

RAM上は予算付きcacheとし、evictionは算術値の不変payloadをdiskへ退避するだけ。再読は位置/型/元node/全hashへ結び、書換え済み又は別slotのpayloadを拒否する。元referenceへin-place変更しない。last-useは数学的参照寿命、evictionはRAM配置であり、同じ概念にしない。slot終了後も既に書いた全unsigned row・receiptは保持する。printed累積行と二つのdirect hexagon行も、将来退避するなら同じ独立storeと明示ownerを使う。

このstoreだけでは最大一行のProduct/Act/PowerをRAM内で計算する費用は消えない。外部sort/mergeによるFox加算へ進む場合、一般group translate後に順序が変わるため、全項を独立にsortし、重複係数をmod3で合算し、零だけ除く追加の算術実装が必要になる。今回それを実装・採用したとはしない。まずactual largest-row/intermediate supportとsort peakを測り、その結果を根拠に別委嘱する。小さいmetadata cacheだけで全11slotの処理時間・memoryを保証しない。

work directoryは16親・acceptance・正語13file・成功D outputの全てから分離し、workflow envelope内の別diagnostic領域としてrootが登録する。indexのheaderは元input全pin/自系source/format/N/E/EOF状態を持たせるが、cache自身の再sealを受付根拠にしない。元原語と実親が正本である。初版は毎invocation新work rootとし、中断cacheの他invocationへの自動流用はしない。完了したindexも「全D成功」とは扱わず、partial index/spill/journalと実cursorをalways保全する。原語13fileへ混入させず、成功Dの全比較rosterにも部分cacheを加えない。正常・資源停止・不一致それぞれでcache/出力の実file・dir・size/SHAを別票へ保存し、前後input不変gateと完成D gateを維持する。

**F6 — 次委嘱で必要な最小計測と対照。** 本便では新GHAを発注・実行しない。D4へ移る前に必要なのは、N/E/L/R/A、catalog各段、live行、canonical parse、IOを混同しない登録である。既存三群の再走を測定の代用にせず、同じ凍結D3の通常NodeCatalog/read/normalized_pair/evaluate_slot/same_word_elevenに届く新しいbounded資源fixtureを、rootが将来一回だけGHAへ登録する案を出す。fixtureは全八op・deep chainとshared fan-out・重複edge・0/負/正Power・Ref alias・非単位Actを含め、全11slotに到達させる。非単位中間値の短いflat anchorと、全typed/filtered経路を通せる別の完全rootを明示し、実64親のtarget零を偽装しない。実親なしのfixtureで全16親入場を成功と称さない。

その同一fixture bytes/pinsをD4通常backendにも与え、元D3の同root mod54、全11 endpoint/unsigned Fox、printed direct/prefix、full32260/48384を完全比較する。新sourceのpath/format/計測値だけを算術一致対象から明示的に外す。D4の新対照は同じindex/read/spill/last-use helperを通し、offset/length/hash/child occurrence/uses/bitset/symbolの改竄、完全resealしたRef key/wordの意味違い、未到達node、0冪の子欠落、部分index/EOF、別slot cache、Ref alias後のeviction/最後の使用、oversized lineを試す。旧成功suiteの追加再走や、新P helperとの一致はgateにしない。

計測は以下をphaseごとに採取する。全nodeごとの巨大JSONログを追加せず、累積counterと定期sample・phase EOFで記録する。

| 実counter | 区別する対象 |
|---|---|
| source/fixture/input全pins、到達phase、全N/E/R/A、最大line/fan-in/普通整数bit長 | 途中prefixならobserved-prefix数として記帳し、完成Nやroot到達を補わない。 |
| JSON parse呼数/bytes、canonical再符号化bytes、recipe位置読取K/bytes、graph edge visits | 主scanとrecipe重複読取、数学評価回数を分離する。 |
| live node handles、異なるFoxValue/row実体数、総resident support、最大単一/中間/printed行support | Ref aliasを二重に行memoryと数えず、外部退避handleは別counter。countは実登録/解放に対応させる。 |
| index/edge/counter/symbol/bitsetのfile bytes、page hit/miss/flush、spill/reload bytesとeviction数 | disk配置をRSS削減の実測と取り違えない。 |
| monotonic elapsed、process ru_maxrss、現在RSS sample、/proc/self/io、OS block counters | Linuxのru_maxrssはKiB・process累積peak、RSS/IO sampleは取得時点の値。欠測はnull、設定7168 MiBは実peakと別。 |

新cache counter自身が全履歴NのPython辞書を再作成しないよう、live実体の計数はlive範囲で行う。retained floor/maps/quotient演算・metadata解放前後・各slotのsort/printed/physical/readoutもphaseに含める。actor/power/大きい一行処理の途中でも既存deadline/資源停止へ届くsourceを確認し、上限超過時に計測とpartial cacheを残す。

現在の2.486 GB途中語を完全candidateとしてD3/D4へ入力しない。新Pが同じ登録16親/64履歴から全13fileを完成して初めて、全sourceと入力before-after・全Ref意味join・同root mod54・全11slot/80644を通す一回の本Dが成立する。それまではfixtureの費用しか分からない。実語の全Dが未到達なら実語の速度比較・memory解消を宣言しない。限られたprobeのnode数を縮めて本語成功へ読み替えず、全本走が予算外ならUNKNOWN_RESOURCEを正式結果として残す。

**F7 — 引継ぎ判定。** 推奨する最初の移行は、D固有のdisk catalog/streamed ordered edges/降順到達bitset/参照数store/正確なsymbol lookupと、未使用pointed解釈値の解放である。候補ごとの語や係数を変えず、一般LEFT Fox算術と全slotのscopeを維持する。次のstepとして認証済IRや外部Fox演算を選ぶには、上記実counterと限定対照の結果が要る。本便からD4実装を開始しない。

全16数学親・全64履歴・同語13file・全11typed slot・full80644・mod54/18・非単位Act・五PB4 endpointを保持する。現在のPB4-dropped gradeではfirst6だけをphysical codomainへ送り、五P endpoint/typed rowsを保存・照合する一方、full P Fox零を新gateへ加えない。source_lower96776零を一般target語へ要求せず、full physical lower32260を直接調べる。grade2/A0/速度成功/Lean verifiedの宣言はない。別のbatch15親/64rank1450/k32/1/refill=falseと凍結995/1009は変更しない。

AUDIT_1013_VERDICT: STATIC_RESOURCE_DESIGN_COMPLETE; ACTUAL_D3_WORD_RUN_UNREACHED; N_E_LIVE_SUPPORT_RSS_UNMEASURED; D4_IMPLEMENTATION_AND_NEW_GHA_NOT_PERFORMED.
