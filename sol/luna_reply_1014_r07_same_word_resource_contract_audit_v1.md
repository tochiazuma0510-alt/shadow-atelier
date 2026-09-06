# Task1014 — 同語P/Dの限定資源移行に対する静的監査

## F0. 範囲・読了・凍結値

Task1014（3671 B / `2083b75a8a5339ec345193b159e1368abe1282201c1ce98362738aed94f04981`）、1012/1013を全文読了した。公開982 F2–F6の八op/Ref/13file契約を再読し、旧P3/D3の通常経路と両設計票を独立に照合した。変更は本返信だけ。実装、ローカルPython/import/AST/GAP/数値、network/git/credentials、新agent、GHA操作はしていない。両系の本文・helper・私的設計を作者間へ転送せず、所見はrootへ返した。996/1010と既公刊source/票は不変。

| 対象 | bytes | SHA256 | LF |
|---|---:|---|---:|
| search/d972_r07_continuation_positive_word_readout_v3.py | 200658 | `bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e` | 3274 |
| search/check_d972_r07_continuation_same_word_eleven_slots_v3.py | 176579 | `273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c` | 2636 |
| sol/luna_reply_1012_r07_positive_word_dag_resource_design_v1.md | 35442 | `2f9c95971a7a383a8480dc417cb58c32689b92baed7b30d31ca80fe9b970807a` | 175 |
| sol/luna_reply_1013_r07_same_word_dag_resource_design_v1.md | 22384 | `5895b4e8cfbf890bd8ab8e2af2a4161d474151abf0b19fad75659091e8238f72` | 88 |

P1012の全175行、D1013の全88行を全表・末行まで読了した。途中のtool出力切詰めはDのvalidate/read/mod54区間と設計票を再読して補完した。D最終pinはrootから正式freeze通知を受領し、既読値と一致した。

## F1. 実停止と未観測値

実正語run34001672135/1、head `14e09d7a96ec9cae71b072e297d2138f5c2f8a72` の小診断を、root回収TEMPから独立に読んだ。P-stdout.jsonは492 B / `55404c32609279a250f1143222a238bfee3d3045408db929f47addafc939221b`、UNKNOWN_RESOURCE/MemoryError:/literal-DFS/182.325646秒。executions/P-receipt.jsonは685 B / `841e44ee4e90730a432df6eb0750be0bab7e89e4dc09adc422531e10802fc952`、exit3、外側184.736433秒である。7168 MiB/5400秒は設定値であり、実peak RSS/ASではない。

P.log末尾の実traceと旧sourceは、compile_target_word→resolve→build_conn→product→link265のchild辞書確保で停止したことを示す。全体をflat文字列として展開していた停止ではない。どの保持物が実peakの何割か、停止したConnのfactor数、最大frame/行長は診断から決められない。

output-inventories.json（1276 B / `670672aa94be2829c83d612c6a86b49479aaf85ca530f2a603dd435dd74c2775`）はword内8fileだけを記録する。preservation-result.json（2033 B / `469bb25c5bf6667dd45fc1bddd1b7031ee581b608487faf944f33a1d1dc628bc`）は全16親/source不変を報告する一方、word-before-Dと本Dが無くINCOMPLETE。D_SELFTEST-stdout.jsonの実678 B / `7ca09522e6f3955fdde2281a7acb0fbb08d3e198f76f30702ad213587decc3be`、三群PASSも直接読んだが、本語のDは未実行である。

全診断ZIP809058240 B / `5bc5b2f5890a7da2641aad882ea4c262ec3d538df0e02e474556848842062a31`、途中語2486667939 B / `87dee2553995e8b81a953d40f89fd9d472adbd0814026cdf1e10ca58929d07c6`の全回収/全hashはrootの認証を参照する。本便で巨大語を再parseしていない。末尾id6629828/child6627615/receipt31792は末尾観測に限り、完成N/E・連番・root・全到達性を補わない。

## F2. 旧通常経路から確認した資源上の原因候補

P3のWordDAG251–327は全hash/pair/positionをPython表へ残し、product304で全factorのchild辞書列を追加確保する。positionsは宣言とappend以外の利用が無いことをsource検索で確認した。resolve1689–1722は明示stackでもgenerator localsを保持し、Conn1817–1836ではpositioned recordと途中factorsが子DFS中も生存する。LiteralParents1582–1647は選択した旧/新bodyのnested値を残すため、del bodyだけで全body由来の保持は消えない。構築後2422–2465の同root読取は別の全hash/pair表を再作成する。この後段も置換対象としなければ、構築表を解放しただけで資源問題が閉じたとは言えない。

D3のNodeCatalog407–457はoffset/hash/children/uses/symbolを全保持し、reachabilityはsetと重複を含むtodoを持つ。459–514は全canonical一行をparseし、全六字段とprior hash/Rel/Refを認証する。516–578のmod54と各slotは独立remainingとliveを持つ。RefRecipes1828–1917は全nodeを読み、1316–1344のexpected構文照合を追加実行する。2513–2544で意味join/同root mod54を終えてから大metadataを解放し、11slotへ進むことを確認した。AncestorIndex.pointedは書込みだけで後続参照が無く、認証を残したまま解釈値の保持を廃止できる。

N=完全語node数、E=反復を含むchild occurrence数、W=全JSONL bytes、K=Ref構文の追加位置読取回数とすると、旧Dの完走経路は全parse14回、parse呼数14N+K+1である。前後の全word hashを含むJSONL論理読取は16W+追加K回のbytes+root行bytesとなる。これはsource上の条件付き式で、本D実測ではない。親JSON・出力・canonical再符号化・全Fox演算は別費用。P1012の34N/50N、D1013の112N+8E+ceil(N/8)+8N+2Nも、登録候補formatの純payload式として整合するが、RSS/AS/所要時間の式ではない。

## F3. 公開八op・同一語を保つ必要条件

第一段階ではpublic grammarを変更する必要がない。各nodeの六字段、八opのexact args、ordinary整数、prior-only childのid/hash、receipt_refsの順序・重複をそのまま保つ。全16数学親/全64履歴、target pivot挿入順、全0係数Power、重複child、Actの二edge、Refの九namespaceと元recipeへの意味joinを削らない。

同一JSONL bytesの条件は、旧DFSのadd/yield/send/Ref発行とancestor登録のイベント順を保つことにある。既出symbolの完全(namespace,key,scope)→元IDを忘れず、初出依存を同順に完了させる。各既発行nodeのbytesが同一なら、次nodeのchild hash・receipt ID・argsが同一となり、canonical unsigned sealと全行bytesも同一となる。この帰納条件により最後のroot/全file hashも保たれる。意味が等しい積の再結合、hash-consing、topological sortへの変更、零edge省略はこの条件を満たさない。symbol_orderの比較順も元node ID順であり、namespace/key辞書順へ変えない。

固定親/dictionary/イベント列に対するordered-word.jsonlの同一性と、新source/acceptance/elapsedを含む外側13fileのhash同一性は別である。P4/D4の新source pinは正直にsource/owner/manifestへ結ぶため、その来歴hashまで旧値を偽装して維持しない。全13fileは各々canonical全bytes/全seal/全EOFを閉じる。成功13名は公開982 F6のままで、scratch/計測を14番目の語fileにしない。

新streaming serializerを後で採るなら、sort_keys・ASCII escaping・JSON integer・separator・LFを含む旧canonicalと全bytes一致が必要である。unsignedとnode_sha256挿入後のfull行は別のhash対象。巨大一行を複数の公開nodeへ割る変更はstorage移行の範囲外である。

## F4. 同root mod54と一般LEFT Foxを混ぜない

mod54ではepsilon:F2→(Z/54)^2の準同型を同root全nodeに適用する。積は加算、逆は負、普通整数冪nはn倍、Act(P,W)の指数はWだけである。しかしこれはconjugatorの構文edge/認証/全node到達を消す根拠ではない。剰余は0..53の整数で、18整除は各座標が0/18/36、両座標が整除なら商0/1/2を読む。ordinary exponent自体をF3やu64へ切り詰めない。

一般slotはV(W)=(g(W),J(W))として、J(UV)=J(U)+L_g(U)J(V)、J(U^-1)=-L_g(U)^-1 J(U)、

`J(P W P^-1)=J(P)+L_p J(W)-L_(p u p^-1) J(P)`

を用いる。P3/D3のAct向きはP*W*P^-1で、D3 TypedFox172–203はこの一般則を実装する。p/uが非unitでも最後のactor項を保持する。mod54でactorが相殺することを、Foxのactor項省略へ転用しない。0冪も依存nodeを認証・評価し、そのedgeを消費するという登録範囲を保つ。

Pの構築後mod54 readerは空の自系indexから元JSONLを読み直し、構築時のpairを答えとして採らない。DもPのscratch/codec/helperを使わず、元13file・元親から自己のcatalogを構築する。P内のB/C照合と独立Dの照合を区別し、共有した数学契約だけで第三独立性まで立ったとしない。

## F5. 到達・反復edge・alias・phase隔離

Dの到達bitをrootからID降順へ伝播する案は正しい。全child IDが親未満なので、node iを処理する時点でiへ到達する全ての大きい親が既に処理済みである。markedなiの全childへmarkすればDFSと同じ到達集合を得る。rootが末尾というだけでは不十分で、全N bitが立つこと、edge spanとpadding/全EOFまで確認する。0冪childとActの二childも伝播する。

usesは異なる親数でなくedge occurrence総数である。各opの全operandを演算完了までpinし、その後、反復を含む各child occurrenceを一回ずつ減算する。同じchildが二回ある積/Actでも一回だけ減算しない。remainingをmod54からslotへ使い回さず、各11slotで元total-usesから独立に始め、最後は全remaining0・liveはroot一件だけを要求する。初版でlast-consumer方式や評価順まで同時変更する必要はない。

Refは元FoxValueをaliasするが、D3のProduct/Inverse/Actは入力rowを変更しない。新node handleの公開後に古いhandleを解放し、別のRef handleが残るpayloadを消さない。evictionはRAM配置、last-useは数学的寿命である。第一段階でFox値をRAMに残すなら、この既存非破壊則を保てばよい。

将来row spillを採る場合は、slot/node/root/全word hash/自系source/codecを束縛し、endpointとrowを分けて保存する。空supportのrowは正当な値で、未形成/missing cacheと同じsentinelにしない。空rowでも非unit endpointを失わず、0-byte payloadは完成flag/support0/空bytes hash/EOFを持つ。全node-index recordのlength0や未形成行とは別型である。mod54二byte列、E3 endpoint40byte、E4 endpoint154byteを互換cacheにしない。このrow codecは採用時の必須条件であり、RAM Foxを残す限定第一便へ先に実装を強制するものではない。

## F6. disk indexの型とpartial境界

新P/Dのprivate indexは別format・別実装とし、少なくともversion/stride/encoding、元wordまたは構築prefix、root/dictionary/入力全pin、自系source、形成済countとEOF状態へ結ぶ。id/offset/length/edge count/usesの固定幅化では、Pythonの十分な幅で加算・乗算・範囲を確認してから格納する。普通整数/boolを区別し、wrap/負index/短縮hash/未知reserved bytesを許さない。合法値が登録表現や資源枠を超えた場合はUNKNOWN_RESOURCE、不正な値やbinding不一致はFAILと分ける。

公開node hash、LF込み全行hash、全file hash、元親のpositioned record hashは別物である。全record境界、連続offset、stride×count、edge span、元id/hash、完全read/write/全EOFを確認する。cache missをidentity/zeroで補わず、dirty pageの未完書込みを有効行にしない。再読は初回symbol登録を再実行する処理と区別し、同じRefの通常再読を二重発行にしない。

partial index/cacheには通常成功のroot/EOFを立てない。Pの一行完成、index完成、両方のdurable prefixを別countにし、停止した一行の末尾を補って完成扱いしない。初版はfresh work rootで、今回の2.486GB尾部や別invocationのindexから自動resumeしない。完全indexができても本D全成功ではない。

scratch rootは全16親・受付/source/raw・語13file・成功D outputから分離し、同一/包含/symlinkを最初のmkdir/診断書込みより前に拒否する。P/D間でscratchを受理値として共用しない。全scratch/partial/journalは外側diagnostic inventoryへ保存し、成功13file/成功Dのexact rosterに混ぜない。MemoryError/disk full/hard kill時の完全内部診断を前提にせず、定期小receiptと外側の実exit/全partial bytesを残す。

## F7. 11slot/full80644と未判定境界

D3はsame_word_eleven634–725で11 occurrenceを実順に評価し、ordinal1/5もそれぞれ出力して同unsigned row/endpointと別sign/blockを比較する。10 unique座標があることを一occurrence削除の根拠にしない。全五PB4 slotもtyped endpoint/rowとprinted direct/prefixを残す。中間非unitを扱う一般演算と、最終全11 endpoint=1を要求するgateを区別する。

current gradeはPB4-droppedで、first6からfull filtered lower32260/top48384を作り、別direct physicalと全80644を比較する。source lower96776が非零でもこの射程から外れない。D3 compare_current_grade856–898のphysical lower零、top+実current remainder=直接読んだoriginal rho2、source lower零のときだけassociated-four-Bとの追加一致を維持する。巨大live行を避けるためsource lower零やPB4 Fox全零という別の仮定を足さない。

normalizedが18非整除の場合のNOT_APPLICABLEをfull80644成功へ読み替えず、最終targetが非零なら陽性適用不可を維持する。全Dが完走してもside/localization、COMMON/Ihara/fake、grade2/A0、Lean verifiedを本便から宣言しない。別batch run34004423047/1の結果を正語の証拠へ流用しない。

## F8. 第一便の裁定と必須・段階化可能な項目

rootの限定案を支持する。旧canonical writer/reader、DFSイベント順、一般Foxを保ち、完了nodeの全管理表を有界page cache付きdisk indexへ移し、通常全経路で計測する第一段階は数学scopeを変えない。巨大一行・未完recipe/factors・live Foxの従来実装が残って再びUNKNOWN_RESOURCEとなっても、それ自体は数学的consumerの誤成功ではない。

必須なのはF3–F7の意味/型/全EOF/独立読取/phase隔離/停止保存である。初版に置換する表を両系が列挙する必要がある。Pの構築後read-side、Dのoffset/hash/edge/uses/到達表を全RAMのまま復元する隠れた経路を残して「disk化済み」としない。一方、symbols/ancestor/paused factorsはRやEに比例し得るので、残すなら明記する。「全N/E依存メモリを除去」「全常駐量有界」とは宣言しない。

P1012 F6.1–4/105/F11が一体の最小案として挙げるfactor spool・streaming serializer・recipe cursorは、強い資源改善を目指す作者案であり、数学的同一性のための無条件な第一便gateではない。旧処理を残す限定版なら新canonical parserのTCBを増やさず、残るpeakを測れる。D1013のbounded一行readerも、合法な大行の上限超過をUNKNOWN_RESOURCEとし、部分parseで成功しなければ整合する。byte枠だけではDOM/canonicalの総peakを保証しないことも明記する。

任意の次段階はfactor/recipe spool、streaming typed parser、認証済IR、body/symbolの追加退避、Fox row spill/外部sortである。採る場合にF3/F5/F6の追加codec/イベント順/一般translate後のsort・mod3合算を照合する。全mmapもASを占めるためRSS/AS解決の主張を伴わせない。unused positions/pointedの解放は通常認証を保つ小変更候補だが、それ単独で実資源解消と呼ばない。現在の両設計に、限定第一段階を数学的に止める必須欠陥は見つからない。

## F9. 次の一回で識別できる計測と新helper対照

N/E/最大一行/最大frame/live supportは未計測のまま扱う。初回新GHAには、変更した通常append/read/cache/EOF/到達/remaining helperへ届く限定fixtureと、同16親/実64の通常P一回を登録するのが妥当である。Pが完成13fileを作った場合だけ同root本D一回へ進む。旧成功suiteを一律再走せず、必要なら凍結旧自系helperを新しい小fixtureの比較基準に使う。非unit中間演算の短いflat anchorと、全11slot/full80644へ到達する別の完全rootを区別し、fixtureから実target零/全16親PASSを作らない。

必要な新対照は、複数page/空cache再読、future ID/短いrecord/offset・stride・EOF・hashの取り違え、u64境界/overflow、完全resealしたRef key/word不一致、同child反復・0冪edge、未到達node、mod54→slotとslot間のremaining隔離である。spillを実装する時だけ空row/nonunit endpoint、alias後のeviction/最後のhandleを実helperへ追加する。新indexと新index自身だけの往復を旧同語一致の根拠にせず、元fixtureのcanonical全bytesと固定rootを比較する。

各phase/有界間隔で、完全文node数とdurable count、op/edge/0冪数、最大fanout/行長、active frame/factor数、symbol/ancestor/常駐body数、index/cache bytes・hit/miss/flush、論理read/write/hash再読/parse回数、live handleと異なるrow実体数/総support/最大中間行、monotonic時間、limit、ru_maxrssとVmRSS/VmSize、I/O sampleを分けて記録する。process累積peakをphase peak差分にせず、欠測はnull、sample時刻と最終失敗時刻を混同しない。counterのため全Nの新Python辞書を作らず、旧管理表と新indexを常時二重保持する計測を避ける。

巨大一行/JSON parse/辞書確保の直前にもphase・予定サイズ・最後の形成済countを小receiptへflushすれば、内部MemoryErrorで新診断確保に失敗しても、外側exitと最後のsampleで次の修理対象を絞れる。改善後の失敗が残存frame/行/rowのどれかを示すとは限らず、未観測成分はunknownで残す。これは診断可能性を高める契約で、次runの完走や原因割合の保証ではない。

## F10. 最終判定

限定disk-index第一段階は、F3–F9を公開条件として実装範囲/残存資源/停止型を登録すれば静的に支持できる。full streaming/cursor/Fox外部演算を無条件に最初から要求しない。P4/D4の新source、scratch/診断のexact schema、cache/byte枠/計測間隔と資源値は今後rootが別途確定する事項であり、本便で実装・実行を開始していない。新source監査、新helper試験、本語P/Dと資源成功は未実施である。

AUDIT_1014_VERDICT: STATIC_RESOURCE_CONTRACT_PASS; LIMITED_FIRST_STAGE_SUPPORTED; P4_D4_AND_RUNTIME_UNEXECUTED.
