Task1012 — 正語 DAG の資源切り分けと最小移行設計

F1. 本便の範囲と結論

本便は指定された新返信だけを作る静的設計である。Task1012 を全文読了した。凍結済み P3 の自系 source と root 回収済み診断の小 metadata を読み、P4 source・試験・数値実行は作っていない。新 C/D 本文・helper・作者票は読んでいない。Python/import/AST/GAP、network/git/GHA、credentials、追加 agent は使っていない。

実停止は「参照 SLP/DAG を使っていなかった」ためではない。P3 は既に prior-only の八 op DAG を JSONL へ出力する。停止箇所は Conn の OrderedProduct に必要な child link 辞書の確保であり、全構築 node の Python metadata 表、未完 DFS の recipe/factor、既存 literal body を同時に保持している。どれが実メモリの何割だったかは現診断から決められない。

最小修理の主案は、(a) node hash/mod54 の固定幅 index、(b) 同一 JSONL bytes を維持する factor spool と逐次 serializer、(c) 一時停止 frame が大きい parsed recipe を保持しない cursor 化、(d) 構築後の同 root 読取にも同じ資源型の index を適用、である。RAM 上限だけを増やす案を主案にしない。公開八 op、Ref/receipt の順序、node ID/hash、零係数 factor を変えない。

同じ16数学親、全64履歴、完成13語 file、10 unique 座標からの11 occurrence、全80644座標、normalized mod54、非 unit Act、5 PB4 endpoint、全 before/after の契約を維持する。別系の登録 batch は15親・実64/rank1450・k32・一 batch・refill=falseのままで、本便から変更しない。以下は設計上の推論と次回計測案であり、新語・P4・D本番成功の主張ではない。

F2. 実診断の再読と証拠の射程

対象は run34001672135/1、launch head14e09d7a96ec9cae71b072e297d2138f5c2f8a72。現 repository の P3 を全 bytes/hash で再照合し、search/d972_r07_continuation_positive_word_readout_v3.py = 200658 B / bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e と一致した。

root の全診断 ZIP 回収値は artifact9979727337、809058240 B / 5bc5b2f5890a7da2641aad882ea4c262ec3d538df0e02e474556848842062a31。実展開 root は C:/Users/81905/AppData/Local/Temp/shadow-atelier-positive-readout-run34001672135-diagnostics-a1、root 申告の全181 entry / 2506894888 B。ここで ZIP を再取得せず、巨大語の全 node 再 parse もしない。以下の小 file は本便で内容・全 bytes/hash を読んだ。

| File | Bytes | SHA256 |
|---|---:|---|
| P-stdout.json | 492 | 55404c32609279a250f1143222a238bfee3d3045408db929f47addafc939221b |
| P.log | 19387 | db9ce64951cc00e191902d8ecf5a4612acb330cd1c337cde0bd6a6fe5a781ffc |
| executions/P-receipt.json | 685 | 841e44ee4e90730a432df6eb0750be0bab7e89e4dc09adc422531e10802fc952 |
| word/resource-stop.json | 492 | 55404c32609279a250f1143222a238bfee3d3045408db929f47addafc939221b |
| output-inventories.json | 1276 | 670672aa94be2829c83d612c6a86b49479aaf85ca530f2a603dd435dd74c2775 |
| preservation-result.json | 2033 | 469bb25c5bf6667dd45fc1bddd1b7031ee581b608487faf944f33a1d1dc628bc |

P stdout は UNKNOWN_RESOURCE / MemoryError: / phase literal-DFS / elapsed_seconds182.325646、successful_bundle=false、candidate/cross_checked/verified=false。外側 execution は exit3、00:36:33.413670Z → 00:39:38.150103Z、wall_seconds184.736433。内側 elapsed と wrapper wall は別の計測である。7168 MiB と5400秒は設定された上限であり、実 peak RSS/AS ではない。

P.log は64段を読んで pivots1450 に達した履歴 log、4 owner の literal-body-read、P1 full-index の最後に記録された7680行進捗を残す。compile_target_word に入ったという source 経路上、load_literal_parents の8059行 EOF gate は既に帰ったが、P5等の事前 PASS やこの入口通過を完成語と呼ばない。traceback は main:3260 → run_actual:2499 → compile_target_word:2411 → resolve:1704 → build:1740 → build_conn:1835 → product:304 → link:265 → MemoryError。Conn の factor 数、DFS深さ、node表の実 allocation、RSS/AS は traceback にない。

output-inventories/preservation に保存された word/ は context、fresh-rho2、literal-dictionary、ordered-word、owner、parent-roster、resource-stop、source の8 file。ordered-word.jsonl は2486667939 B / 87dee2553995e8b81a953d40f89fd9d472adbd0814026cdf1e10ca58929d07c6。これは root が全 bytes を照合した値と診断 inventory の値であり、本便が全 node 連番を再照合した値ではない。Task1012 にある「末尾 id6629828 / IntegerPower(-1) / child6627615 / receipt31792 / final LF」は末尾観測としてだけ引用する。この数から完成 node 数・root ID・最終 descriptor を宣言しない。

preservation は全16親不変・acquired sources 不変・source/raw/acceptance/driver不変を報告する一方、word-before-D が未形成、本 D output なしのため全体 status INCOMPLETE。実 P5/D3/20 inventory 逆対照 PASS と本語/D 成功は分ける。MemoryError 後の allocation 細分内訳や巨大 OrderedProduct 一行の最大幅は未計測である。

F3. 自系 source で確認した生存期間

以下の行番号は上記 frozen P3 の実本文に対するもの。Python object の共有参照と payload の複製を区別し、list/dict/tuple があるだけで全子文字列がその都度深く複写されるとは数えない。

| 保持物 | 実経路と寿命 | 資源上の意味 |
|---|---|---|
| WordDAG.hashes | 250–285。add ごとに64桁 hex str を一個 append、compile_target_word が返るまで全 N 個 | prior child hash と root hash に使う O(N) 表。link dict は通常この既存 str を参照し、新たな64桁文字列を毎 link 複製する実装ではない |
| WordDAG.pairs | 257/283、node_residue:222。各 node の residue54 の2-tupleを全保持 | O(N) tuple/list overhead。値は0..53。小整数の intern/shared 実装を無視して「新規整数二個/N」と実測扱いしない |
| WordDAG.positions | 258/284。全 node に offset,length tuple を append | 全 source 文字検索では、この WordDAG 属性に後続 reader がない。raw_data の positions は別物。内部属性の省略は word bytes/hash/receipt を変更しない |
| WordDAG.symbols | 259/319–323。typed (namespace,key,scope) → node ID | 初回 DFS postorder の Ref memo、完了済 symbol 数 S に比例。これを捨てて再構築すると同じ node ID/order を保てない |
| compiler.recipe_refs / symbol_order | 1665/1670、1699–1718 | recipe_refs は終了した symbol 分も残る。symbol_order は全 Ref の公開 closure で bundle に返るため compile 後も残る。両者は別用途 |
| active / stack / paused generator | resolve:1689–1722、各 build_* の yield | stack は (symbol,generator)、active は同じ未完 symbol の集合。各 generator と yield-from chain の locals が、次の子完成まで残る。明示 stack でも大きい locals の解放は自動ではない |
| suspended recipe/factors | build_p1:1762、build_defect:1783、build_conn:1817、build_legacy_source:1911、build_physical:1957、build_E_source:2253 | positioned record、reductions、refs、途中 factors を保持。Conn は source record を全 parse して factors=[word] を育て、全 child 完成後 product に渡す。親 frame の途中 factors は子 DFS 中も生存する |
| OrderedProduct child 辞書列 | product:304 → add:267 | caller の factor ID list が残ったまま、別の list と各 child dict を作る。add の unsigned/record は主に同じ args を共有するが、canonical(unsigned) と canonical(record) は大きい文字列/bytesを作る。これらの生成 peak を単純に「常時二倍」と断定せず、別に計測する |
| Parents / TargetHistory | 560、908、read_base_target:1052 | acceptance/roster/file索引と HEAD/start/result/checked、8059 base offer の位置索引、全 pivot/raw_recipe/target親列を保持。base_records は位置と p1_source であり、8059 source record 全体を格納する実装ではない |
| LiteralParents | load_literal_parents:1582–1645 | prepare.old_blocks と defect_origins、4 new block の dag_nodes/origin_reductions/actor_transitions/basis_blob、8059 index を保持。del body は選択した nested object を解放しない。compile 中ずっと保持し、run_actual:2500 の del literal は compile 成功後 |
| raw/history補助 cache | compiler.load_raw:2098–2251、geometry:2016–2028 | raw_data は whole raw record/witness/values/by_id/位置表を key ごと保持。by_id は既存 node dict を参照する。raw_streams は全 raw 語の検算済み receipt。geometry は scope ごと三本の u32 を Python int tuple に展開して保持。raw_origins は宣言だけで使用箇所なし |
| ancestor 索引 | Ancestors:686–722 | 公開 entries と dedup unique の双方を保持。pointer 値 hash と実 parent byte hash を結ぶ。完成 ancestor-index の意味を削って容量を減らすことは不可 |
| 小 raw 語 stream | load_raw の evaluate と明示 stack:2151–2242 | raw v547 normalizer の普通整数と各小 raw 語の signed-letter stream を扱う。全 target 語を平坦文字列にしていない。IntegerPower の abs(power) 分の stack.extend は局所的な別の未計測 peak |
| 構築後の自系評価 | read_normalized_pair:2422–2464、run_actual:2501–2521 | compile の dag/compiler 本体が通常 return で不要になってから、改めて hashes/pairs 全 N 個を作る。history/ancestors/bundle/metadata はまだ生存。成功後でも同規模の node 表が別 phase で再発する |

build_E_source は reductions/corrected/roots/root_map と途中 factors を同時に持ち、child P1 resolve へ yield する。これも単一 parsed record の一時負荷とは限らない。geometry/raw_data を全消去しても Conn/P1 の停止経路は別に残る。逆に今回 Conn 停止だけを見て、全 E 後の cache 累積は安全だったとは言わない。

F4. 量の式と未計測の部分

N を完全に公開処理した node 数、E を保存する全 child edge 数（零 power の edge も含む）、S を完了 Ref symbol 数、R を ancestor receipt 数、D を未完 DFS frame 数とする。各未完 frame f について、保持 parsed recipe bytes/object の量を J_f、途中 factor ID 数を A_f と書く。最大 canonical node 行長を Jmax、固定 parent/history の resident 量を B_parent と書く。実値 N/E/S/D/Jmax/peak は現在の診断に揃っていない。

P3 の構築時 live memory は概ね B_parent + N(h_hex+h_pair+h_position+list slots) + M_symbol(S) + M_ancestor(R) + Σ_f(J_f + factor-list(A_f) + frame_f) + M_raw_cache + M_current_serialization で分解すべきである。h_* は実 runtime の object overhead を含む未計測項であり、RSS の数値ではない。pairs の2値、links の SHA str、各 dict の shared object を重複計上しない。current product は A 個の factor ID 列に加え A 個の child dict と canonical の一時 bytes/string を要する。Σ A_f と現在一個の A は別である。

同じ論理値を固定幅にした純 payload は hash32 B + residue54二成分各u8 = 34N B。offset/length を各u64で残す版は50N B。これは配置 padding・header・cache・Python管理・OS page・file内容・symbol/receipt/DFSを含まない index payload の式であり、実 RSS/peak や今回の N を推定する式ではない。positions を省くなら語全 file hash と逐次 total/count は別に保持する。

構築側の仕事量も O(N) だけでは足りない。prior hash確認、mod54加算、因子出力は E に依存し、wire入出力は全 JSONL bytes W、raw flat stream は各 raw 語の実 letter 総数 L_raw に依存する。親 JSON parse・canonical hash・whole before/after は別の入力 I/O である。巨大一行や多数の中断 frame があれば、34N の採用だけで peak 全体は有界にならない。

P3 の main:3256–3259 は RLIMIT_AS を設定し、check_resources:98–110 は ru_maxrss を同じ設定と照らす。AS と RSS は異なる量であり、Python allocator/fragmentation、mapping、既存 library/address space、current allocation が関与し得る。MemoryError は allocation が成立しなかったことを示すだけで、どの成分が上限に達したかを確定しない。

F5. 固定幅表の選択と保持すべき identity

比較対象は public word を別の語に書き換える案ではなく、同じ node を保持する内部表の置換である。

| 方式 | 固定幅の中身 | 有利な点と残る費用 |
|---|---|---|
| compact array | hashを32 raw bytes、pairを二つのu8。必要なら二u64の位置表 | Python str/tuple/N個のlist elementを除ける。依然34Nまたは50Nの常駐量、grow時の旧新buffer/予約capacity、巨大factorとDFSは残る。成功予測には使えない |
| 全 file mmap | 同じ固定幅 file | ページをOSへ委ねられるが、全mappingはASを占める。現RLIMIT_AS下で「diskだからAS/RSSは減る」とは言えない。主案にしない |
| seek/read + bounded page cache | append専用固定幅 file、node IDから一定stride、明示上限つきpage cache | 常駐量をcacheと作業bufferへ分離できる。過去nodeがcacheに無くても実indexから照会でき、Ref/edgeを消さない。random readと再読量、file/cache hash確認の費用が増える |

主案は最後の方式。headerを除く行を hash32 + residue_x:u8 + residue_y:u8 の34 Bにする。位置が必要な診断/readerには offset:u64LE と length:u64LE の別16 B行を持たせ、不要なら生成しない。paddingを暗黙に入れず、endianness/stride/version/count/complete EOFを明示する。digestはSHA256の全32 bytesであり、短縮hashやhashだけによるsymbol同一視を使わない。pairは整数剰余0..53であり、F3 trit/packed3や符号付き整数本体ではない。加算・符号・powerでは十分な幅で既存式を計算してから mod54 に戻す。IntegerPower の公開 exponent は普通整数のまま保ち、u64に押し込まない。容量/offsetの実装限界は資源停止として明示し、wrap/truncateしない。

symbolsは完全な (namespace,key,scope_sha256) を照合する。Sが許容範囲なら既存dictのまま実測し、別枠でtelemetryを出す。S/Rまでdisk化する場合は可変長keyの全byte照合と単一writerのfirst-insert順を保持するindexを用い、digest衝突を同一key扱いしない。参照されたdictを単にLRUで忘れて同symbolを再生成する方式は採らない。recipe_refsはRefを出力した時点で、その同symbolが再構築されない条件の下で解放できるが、公開ancestor entryとsymbol_orderは保存する。

node ID、全child hash、receipt ID、Ref key/scope、同一snapshotの順序を変えないことが最優先である。小さい同一subwordでもP3が毎回別nodeを出す位置を新hash-consingで一つにまとめない。全symbolを先にtopological sortして生成すると、P3の「最初に出会ったdependencyを先に完成させる」postorderやancestor IDが変わり得る。今回の最小移行ではその変更も行わない。

F6. DFS と巨大 OrderedProduct の最小移行

node表だけの置換を「資源修理完了」と呼ばない。以下の通常経路を合わせて対象にする。

1. **factor spool。** 各未完 recipe は factor node ID をappend専用の小runへ順番に出す。runの内容は普通のu64 ID列とcount/byte範囲で、順番、重複、0 powerのchildを保つ。親frameがyieldしている間、Pythonのfactor ID list全体を保持する代わりにrun識別子・現在末尾・次factor位置を持つ。現在のmax fanoutだけでなく全未完frameのfactor総量をdiskへ逃がす。runを共有するなら親が中断した間の子appendを混ぜないchunk鎖/範囲列が必要であり、「単一連続offsetだけ」と仮定しない。

2. **同一byteのproduct serializer。** OrderedProduct一個を複数の新OrderedProductへ再結合しない。現在の一個のnodeに同じfactor列を保存する。新writerはfactor ID→実hashを一個ずつ読むため、child dictをA個同時に作らない。canonicalはsort_keys/ASCII/最短整数/同じseparator/末尾LFを保つ。unsigned nodeを逐次hashしてnode_sha256を確定し、その値を正しいkey位置に挿入したfull recordを出力する二pass（またはargs spool再読）にする。unsignedとfullの末尾LFもそれぞれ従来hash対象である。先にhash字段を仮置きして後書換えしたfileを完成扱いする方式は使わない。refs列も順序と重複を保持する。

3. **明示recipe cursor。** resolveの一frameはsymbol、builder種別、次のsemantic操作/子位置、小scalar、factor-run位置、receipt参照、依存の復帰先を持つ。yield直前に大きいrecordをframeへ保存しない。P1/state JSONLは既存のwhole file pinに加えてoffset/length/record SHA、body JSONは実parent role/file/JSON pointerとrecord hashへ結ぶrecipe scratchを利用する。recipeのoperand順、正負、scale一回、raw語修理の普通整数、old→new/physical順は変えない。原fileを繰り返し全parseするだけの解放案は、CPU/I/Oを悪化させるため独立に数える。

4. **副作用の同順実行。** 一つのbuildには「dependencyをyieldする前にLetter/Relやreceiptを出す」箇所がある。cursorを先に全展開してreceipt登録だけ先行するとIDが変わる。旧buildの各add/yield/send/Ref終端の順をイベントとして保ち、初回normalizer origin、全 raw-e/tree scope、binary positioned receipt/JSON pointerの区別を維持する。cursor数を小さくするためactive symbolや未構築Refを消さない。

5. **parent/body cache。** LiteralParentsは一bodyを読むたびに以前のold/new部分を残している。first stageでは選択nested部分の実resident量を測る。強い常駐上限を要する版では、必要recipeを実descriptorで認証したscratchへ一度出し、bodyを解放して以後は有界record cacheで読む。単なるdel body追加だけでは選択nested referenceが残る。whole parent JSON一個を既存json.loadsでparseする最初のpeakも別に残るので、body/一行の最大値が上限を圧迫する場合はtyped streaming readerの対象になる。

6. **残るcache。** raw_dataはraw recipeごとの本体と索引を必要時に再読できる形に分け、使用後の可変cacheを有界にする。ただしraw_streamsという公開receiptを削らない。geometryは同scopeを共用し、u32 tupleをcompactまたはpositioned readerへ置換できる。normalizer/raw値の普通整数計算とactual signed-letter streamは維持する。rawのIntegerPower展開stackはrepeat counter frameにすれば同順のstreamを保てるが、全target語をflat化する口実にしない。

7. **構築後に残る大きいJSON。** ancestor-indexとword-manifestのsymbol_orderは公開全配列である。N表を圧縮しても、そのjson.dumps/canonicalのpeakが消えるとは限らない。必要ならscratchの同順arrayを逐次serialize/hashする内部writerを共用し、外部には同じ完全配列を残す。選択rootだけのclosure要約へ置き換えない。

F5のnode表とF6.1–4、次節のread-sideを一体の最小資源consumerとするのが妥当である。F6.5–7を初版で全streaming化するかは、既存親の最大parsed単位と新telemetryを根拠にrootが登録する。未実装のstreaming化を仮定した「全常駐量が一定」という主張はしない。P4という名称だけ先に付けてpositions削除だけで本問題が閉じたとはしない。

F7. 構築後の自系 C と独立 D の費用

自系 read_normalized_pair は、Bのmemory tableを信頼して終わる関数ではない。fileを再読し、連続id、全node seal、typed args、全prior child hash、Rel辞書、全receipt範囲、全byte EOF、最終root、mod54 recurrenceを通す。新P4でもこれを維持する。新readerは**別の空のcompact/disk tableから**同じ処理を行い、producer scratchのpairを答えとして流用しない。builder tableが解放されてもPython allocatorの予約がRSS/ASへ直ちに返るとは限らないので、phase切替の実計測も必要である。

逐次for lineだけでは一行は有界でない。巨大OrderedProductのraw行、ASCII decode文字列、json.loadsのfactor辞書列、再canonical文字列/bytesが同時に存在し得る。writerだけをstreaming化すると、このreaderへ問題を先送りする。必要なnew readerは八opのexact typed fieldsを順次読むものとし、large factors/receipt_refsを逐次消費してhash/pairを更新する。canonical key order、duplicate/unknown key拒否、整数とboolの区別、escaping、negative/zero exponent、全LF/EOFを弱めない。小nodeを既存DOMで読むfast pathを残すなら、大小境界で同じbyte/拒否結果になる対照が必要である。単にjson parserの最大行上限で合法な大積をFAILにする方法を数学的consumer完成とはしない。

Actのmod54 residueではconjugatorが相殺するためnode_residueはwordのpairを返す。しかしAct nodeのconjugator edgeは今もJSONL/prior-hash/receipt読取に残る。この一事から、一般typed endpoint/LEFT Fox/11 slot評価でActをunit扱いしてよいとは推論しない。zero exponentでもnodeや依存receiptを落とさない。

本便では新D sourceを読んでいない。Dのcache表・dense/sparse中間値・last-use実装を観測したとは書かない。同じrootの10 unique評価→11 occurrence、5 PB4 endpoint、LEFT Fox/printed順、current grade、全80644座標とfresh rho2の結合はそのまま必要である。P4の34N表が小さいことは、Dでnodeごとのendpoint/Fox値が何bytesになるか、どれだけliveであるか、full projectionが期限内かを与えない。D側に資源修理が必要なら、同じ公開wireだけを渡して別authorが独立に設計する仕事であり、P4設計から無断でshared helperや11 slot省略を導入しない。

自系phaseの概算費用は、構築が親認証 + O(N+E+W+L_raw) にscratch/parent再読、read-sideが O(N+E+W) にindex random I/O、終端がmanifest/ancestor/closure serializationと全input不変再読である。これは定数・cache miss・巨大整数/JSON/系統別grade演算を除いた区分で、runtime上限内の証明ではない。

F8. 一時索引と部分出力の型・保全案

以下は将来の新source/workflowへ登録するための案であり、現13file schemaや凍結WF4を変更したという意味ではない。

- 成功word/のexact13fileは変更しない。scratch・resource telemetry・cursor journalをそこへ混ぜない。新wrapperが管理する別sibling scratch rootを明示し、全16親、acceptance/source/rawと包含・symlinkを拒否してから作る。host path/nonceはinvocation/scratch receiptに置き、wordのnode IDやRef scopeをそれで再定義しない。
- scratchには型を分ける。node34/position16の固定幅表、factor-u64 run、recipe/cursor journal、symbol/ancestor補助索引、streaming args/unsigned spool、測定receipt。各型はversion/stride/encoding/普通整数範囲/実file bytes/SHAを持ち、node行の前方参照禁止、scope/owner/source/acceptance/dictionary/入力pin束縛を明記する。任意binや任意JSON tailを通常nodeと解釈しない。
- nodeがpublic streamへ完全に書けたこと、index appendが終わったこと、fsync済prefixであることを別countにする。複数chunkからなる大nodeの途中停止では、末尾LF未形成のbytesはtailであってnodeではない。page/batch単位でflush/fsyncするなら、wordとindexが両方到達したcount/offsetだけをatomicなscratch commit recordへ残す。設定間隔は次委嘱で固定し、全node fsyncの時間をここで無視しない。
- current logical countだけで「durable」と書かない。scratch commit recordのhash、実file長、対応prefix bytesとindex EOFが一致しないものはINCOMPLETE。末尾bytes、未完factor run、未形成index、孤立temporaryは保存対象として列挙するが、13file完成manifest/rootへ混入しない。
- 新P4の最小版は部分scratchからの本算術resumeを成功条件にしない。失敗時はUNKNOWN_RESOURCE/partial、rootが同じ固定親から新しい別出力へ再実行する。将来再開を加えるなら、same owner/source/入力とcursor+word+indexを一つのdurable prefixとして再認証する別契約が必要。今回の2486667939 Bの末尾から続ける実装を許可したことにはならない。
- 完成時は全word EOF/13file/同root mod54/全before-afterを従来どおり閉じる。scratch indexは補助物であって数学受理の代替ではない。成功後のscratchにも実inventoryを別receiptとして残す。失敗時は可能な小telemetryを先に保全し、writerに未完nodeやindexを完成と見せる末尾追記をさせない。
- MemoryError直後に大きいdict/listを新規確保して診断を作ることへ依存しない。定期小receiptと最後にflushされたcounterを先に残し、外側wrapperもexit/stdout/stderrと全partial bytesを保存する。最後の計測値は測定時刻付きであり、停止瞬間のpeakと同一視しない。hard kill/disk fullで内部final receiptがない場合も外側ではINCOMPLETEのまま記帳する。

scratch path追加・wireは同じだがsource pinが変わる入場・新output型のalways inventoryは、将来のversioned wrapper差分で明示する必要がある。旧P3/D3/WF4/994の追改変は不要であり禁止を維持する。

F9. 次の root/GHA で測る最小の通常経路

追加実験は本便では実施しない。rootがP4のversioned範囲を裁定した後、まず変更したstorage/serializer/readerの小対照だけを通し、同じ16親・実64履歴の通常Pを一回走らせる案である。従来の数学親の全数値suiteを追加しない。上限は別に再登録しない限り既存P5400秒/7168 MiBを使い、上限値を成功見込みや実peakとは書かない。新Pの完成13fileが揃った場合だけ同rootの独立Dを通常一回へ進める。D10800秒等も上限であり成功予測ではない。PがpartialならD成功を作らず、全parent/source/raw/acceptance不変とscratch/word部分出力をalways保存する。

計測点は入場終了、history終了、各literal body読了/解放、全P1入口EOF、DFS開始、固定node-blockまたは時間間隔、最大fanoutのserializer前後、DFS完了/construct index close、同root reader開始/EOF、manifest各大配列出力、全before-after終了。大nodeの逐次serializerと長いraw streamの内部にも既存協調停止相当の有界chunk境界を置く。記録頻度とcache/page設定は実装時に固定し、telemetry自体がN個のlistを保持したり、毎node全文heap走査を行う形にしない。

| 測る値 | 定義・注意 |
|---|---|
| limit/runtimes | RLIMIT_AS soft/hard、宣言max_memory/max_seconds、Python/platform/allocatorに関係するruntime metadata、時刻/phase。limitと使用量を別字段にする |
| 実process memory | Linuxならru_maxrssを明示unitで換算したhigh-water、同時点のVmRSS/VmHWM/VmSize。ru_maxrssの全process最大値はphase最大値の差分ではない。sampled値の欠測を0で埋めない |
| node表 | emitted full node count、durable index count、index bytes、cache resident rows/pages/bytes、hits/misses/reads/evictions。N個の保存rowとRAM常駐rowを分ける |
| nodeのlive | 未完frameやcacheが直接参照するnode集合/件数はその意味で測る。将来consumerがまだ使う全semantic-live-node数はlast-useを全edgeから確認しない限り未知。cache resident数をsemantic-live数と呼ばない |
| edge/factor | op別node count、全edge count、zero-power edge count、current/max fanout、全未完factor-runのcount/bytes、index child照会回数。zeroを含む公開countは採用規約どおりで測る |
| DFS/symbol/receipt | current/max frame数、active/finished symbol数、namespace別symbol数、recipe_refs保有数、ancestor entry数、paused recipeのloaded record countと実source byte長、最大単一record/JSON行長 |
| cache/body | resident old/new body数、raw recipe/geometry cache数、compact payload bytes、recipe spool bytes。Python object overheadは別の観測方法を採らなければunknownのまま |
| I/O | parent/index/scratch/wordごとの論理read/write bytesと回数、unique file bytes、hash再読bytesを別に数える。同じfileの繰返しreadをunique bytesへ混ぜず、kernel block I/O/圧縮ZIPsizeとも区別する |
| phase/canonical | monotonic elapsed、出力node/fileのfull bytes/hash/count、unsigned/hash用passとfull-record用passのbytes、chunk数、最大同時serialized buffer量、fsync count/time |
| 失敗点 | op/phase、開始しようとしたnode ID、最後の完全node/commit record、requested chunk/fanout、MemoryError/OSError/期限、最後の測定時刻。未完成nodeをcountへ足さない |

資源原因の割合を一回の観測だけで断定しない。実測がnode表圧縮後も大きいframe/body/一行に集中したなら、その対象だけを次のversioned修理へ回す。Dに進んだ場合はD作者が自己の同root実評価のphase/RSS/live-value/I/Oを報告する。P側tableのbytesをDのdense値のbytesに転用しない。この最小一回経路でP/Dが終わらなくても、UNKNOWNと実component計測が次の設計根拠になる。

F10. 新しく必要になる本番helper対照

以下は次委嘱で書く新helperに必要な小対照の案である。実装も実PASSも本便にはない。数学計算器同士の独立性を補う旧suiteを増やすという意味ではない。

- **NodeStoreの実append/read/EOF。** 複数pageをまたぐprior ID、空cacheからの同一hash/pair取得、0/53を含むresidue54、短縮hash拒否、stride/count/EOF不一致、future node、index/tail切断、source/owner/入力scope取り違えを同じproduction readerへ通す。u64位置の境界は小metadata fixtureで型を通し、巨大dummy出力を本番宇宙の代わりに生成しない。
- **streamed productとtyped reader。** 八op全部、0/正/負power、繰返しchild、非自明conjugator付きAct、空/多factor、全部のreceiptとRefを持つ小DAGを使う。compact/spool/cache設定を変えても同じJSONL全bytes/nodeSHA/root/hash/normalizedが得られることを実writerと全readerへ接続する。factor交換・zero edge削除・child hash交換は元fixtureの固定manifest/rootとの結合で拒否させ、bool/整数混同・LF/余分key/duplicate keyはtyped readerそのものへ通す。別の合法語を全resealしmanifestまで差し替えた場合を、grammarだけで拒否できるとは要求しない。大一行fast/stream境界を小設定で実際に跨がせる。
- **cursorの旧順序維持。** dependency前のLetter/receipt、深い中断、親復帰後のfactor、同symbol二度使用、root Ref末尾、初回normalizer originを含める。期待値は旧公開八op/recipeの固定小例に基づき全byteを比較する。単に新writerで作った値を同じwriterで再出力して「旧順序一致」とは呼ばない。少なくともConn/P1型、source→physical→targetの0係数を含むordered ancestryを通常resolve/compileの入口へつなぐ。
- **部分出力と資源診断。** writerのnode途中、node後index前、index後commit前の停止を小I/O fixtureで発生させる。通常readerは未形成EOF/root/13fileを成功とせず、別scratch inventoryへ保存する。readonly親・acceptance/source/rawとoutput/scratchの包含、symlink、未知通常fileも実path helperで拒否する。計測は全成功receiptやnode identityを変えず、異なるnonce/pathで同じ数学入力のnode streamが同じになることを確認する。

旧P3で通ったfive-group本数を新resource修理の根拠にしない。逆に新storage小対照だけで全11slotや80644の算術が通ったとはしない。必要な新D改変が見つかった場合は独立authorのversioned範囲として別に発注し、本便の自己sourceへ取り込まない。

F11. 次の実装単位、未了事項、凍結保持

次の最小単位は「同じ八op wireを出すNodeStore/factor spool/DFS cursorと、そのfull EOFを読み直す自系mod54 consumer」である。scope変更や未来の成功parentではなく、現16親/実64の同語を保つ資源実装として定義する。根拠のある軽量化はunused WordDAG.positionsの廃止、過去nodeを全保持するPython str/tuple表の置換、終了済recipe_refsの解放、大きいpaused recipe/factorsのcursor化である。これらのうち一部だけを採るなら残るpeakを明記してUNKNOWNを許す。公開node/edgeの省略、0 power/Ref/actor ancestry削除、履歴短縮、11slot選別、語再結合によるroot変更は採らない。全node情報を保存したままcacheを解放することとは区別する。

まだないものはP4 source/pin、scratch/診断の正式schema、cache/page/telemetry間隔の登録値、新GHAの実peak/live量、完成root/13file、新D本番、full80644比較結果である。本便の末尾idからこれらを補完しない。現観測で判明したのはP3の資源停止とsource上の常駐構造までで、改善後runtime・反復回数・語の完成可否は未測定である。

Task994と正語P3/D3/WF4、既返信は変更しなかった。本便で再hashした凍結値はP3がF2の200658 B/bc51546e…、batch Pが213861 B/229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591、reply994が53207 B/ce8084cb6301473b67f72edd57b34db6a280fa1baf137e28e89f6842730e6738。Task1012は初読3776 B/9f688a5bbd00bb5c5ce6a7cabd2a45c0113f37cb3c5fcb52364dfb09d9417c46。rootが公開前に末尾余分な空行1行を除去した最終版も全文再読・hashし、3775 B/68ac7d07b04d0c72e4af2ee7a648b840c76b6f5fdb6013b35c4e66068f34db32と一致した。意味・委嘱範囲の変更はない。

本返信の変更先は sol/luna_reply_1012_r07_positive_word_dag_resource_design_v1.md のみ。実P4化と追加実験はroot裁定後であり、進行中の995/1009/batch release条件にはしない。

AUDIT_1012_VERDICT: RESOURCE_DESIGN_COMPLETE_STATIC_ONLY_P4_AND_RUNTIME_UNEXECUTED
