Task1022 — P4 resource receipt の公開nested型

F1. 読了・参照pin・型の約束

Task1022 2134 B / 8054b4925f258d0d96ef30c577877825973563a6e2f7116af9209c92e2913f22 を全文読了した。本票はsource由来のserialization仕様であり、実selftest stdoutでも本語の実結果でもない。私的算術・helper本文・codec操作手順は含めない。

本便途中にroot/1021が試験symlinkの一件だけの除去を追加裁定したため、参照sourceの最終値は search/d972_r07_continuation_positive_word_readout_v4.py =252342 B / f36e929ee303b968c519e0333d18b10d3c3e01d83b9ad8ec896949d5ca02dd77、LF4258/CR0/BOMなし/finalLF/行末空白0である。返信1016は23959 B / f6734e3d93a1a1d2e4173583562627a21d9e6e3eb63b52da1dcbee8a3c22d150。この限定修理は1016 F12へ記帳済みで、本票のinterface列挙に新source変更は伴わない。Task1022の旧252290 B/0fc1c039…指定はこのroot追加裁定で置き換える。

以下、S=d972.r07.continuation-positive-word.v1、R=S.resource-v4 と書く。intはboolを除く普通整数、uintはint>=0、posintはint>0、Hは小文字hex64全桁、BはJSON booleanである。objectのkeyに順序の数学的意味はなく、canonical時は文字列keyをsortする。listの順序は以下のとおり保持する。canonicalはASCII・compact JSON・末尾LF一個である。

| hash名/位置 | 対象 |
|---|---|
| sealed object自身のsha256 | そのobjectのsha256字段だけを除いたcanonical全bytes。schemaは含む |
| 非sealed file descriptorのsha256 | 指示された実file全bytes。JSONなら内部sealと元の末尾LFを含む。短縮・内部sealへの置換不可 |
| artifact.sha256 | ZIP全bytesのSHAにsha256: prefixを付けた文字列 |
| session_sha256 | 当該群又は通常sessionのstart.json全bytes。内部start.sha256とは別 |
| word_result_sha256 / word_manifest_sha256 | 語output/result.json / output/word-manifest.jsonの全canonical bytes |
| index receipt.sha256_payload | index binary file全bytes。headerも含む |
| root_sha256 | 語nodeのnode_sha256。root JSONL行全bytesやword file全bytesのSHAとは別 |

通常のfile descriptor FDはexact {file:str, bytes:uint, sha256:H}。fileの基準はF4/F7の表に従う。成功・停止・未形成の各状態を勝手に相互変換しない。新selftestのcandidate/cross_checked/verifiedは全false、old_full_suites_runはint 0である。

F2. 通常resource startのformat/cache/limits

通常の<scratch>/start.jsonはR.startのsealed objectで、exact body keysはinvocation、binding、format、cache、limits、fixture_only、resume。invocationは32桁小文字hex str、formatは固定str private-P4-node42-v1、fixture_only=false、resume=false。bindingはF3、cacheは下表、limitsはその次の表である。start作成だけを成功語や数学入場の最終成立と呼ばない。

cacheはstart/result/各sample/第一testで共通のexact型を持つ。以下の12 keysだけで、すべてuint（設定3字段はposint）。実counterは実出力を読む。

| key | 通常設定又は型 |
|---|---|
| page_rows | posint 4096 |
| page_bytes | posint 172032 |
| cache_pages_limit | posint 388 |
| io_buffer_reserve_bytes | uint 344064 |
| configured_cache_and_io_bytes | uint 67092480 |
| resident_pages | uint、cache_pages_limit以下 |
| resident_payload_bytes | uint、当該resident pageの実payload bytes |
| max_resident_pages | uint、cache_pages_limit以下 |
| hits | uint |
| misses | uint |
| evictions | uint |
| flushes | uint |

start.cacheは空の開始状態なのでresident_pages/resident_payload_bytes/max_resident_pages/hits/misses/evictions/flushesが0。result等の値を開始時の0で代用しない。cache総設定上限は67108864 Bであるが、これをprocess全常駐量の上限と呼ばない。

limitsのexact keysはline_bytes、scratch_bytes、free_floor_bytes、process_memory_bytes、process_max_seconds。

| key | 通常CLIによる値/型 |
|---|---|
| line_bytes | posint 67108864、LF込み |
| scratch_bytes | posint 17179869184 |
| free_floor_bytes | uint 1073741824 |
| process_memory_bytes | posint、--max-memory-mib * 1048576。登録値7168 MiBなら7516192768 |
| process_max_seconds | 正のJSON float、受付deadlineと開始単調時刻の差。登録CLIは5400秒 |

mainを通さない内部fixture入口では後二字段がnullになり得るが、登録された本GHAの通常CLIとresource-selftest CLIでは両方設定される。nullを0へ変換しない。process_max_secondsは実elapsedやpeakではない。

F3. 通常bindingのexact shapeとlist順

bindingのexact keysはproducer、acceptance、parents、consumer_sources、raw_sources、runtime、accepted_owner、accepted_head、scratch_path、output_path、ordered_word_identity_unchanged_by_private_storage。

| key | 型・値の結合先 |
|---|---|
| producer | FD。file=search/d972_r07_continuation_positive_word_readout_v4.py、SOURCE_ROOT基準。最終全pinはF1 |
| acceptance | exact {file:absolute str, bytes:uint, sha256:H}。実--acceptance file全bytesと長さ。内部acceptance.sha256ではない |
| parents | 下記16個のordered list。受理したacceptance.parentsの全objectをそのまま保存 |
| consumer_sources | exact object {producer:FD, checker:FD}。acceptance.consumer_sourcesと完全一致 |
| raw_sources | 下記3個のordered FD list |
| runtime | exact {python:str, numpy:str}。pythonはsys.version全文、numpyはversion全文。受付と完全一致 |
| accepted_owner | FD。acceptance.selected.ownerと完全一致、file=output/owner.json |
| accepted_head | FD。acceptance.selected.headと完全一致、file=output/HEAD |
| scratch_path | 実--scratchの絶対path str |
| output_path | 実--outputの絶対path str |
| ordered_word_identity_unchanged_by_private_storage | B true |

consumer_sources.producer.fileはF1の新P4 path、checker.fileはsearch/check_d972_r07_continuation_same_word_eleven_slots_v4.py。両者のdescriptorはwrapperが入場時に固定した実source全pinであり、新Dの値を本票で捏造しない。runtime/consumer_sourcesはobjectなのでcanonical key sort以外のlist順はない。

parentsのrole順は厳密に
[state,delta,seed34,packet,refinement,oracle,e,prepare,block-0,block-1,block-2,block-3,p1,task712,continuation,rho2]。
各要素のexact keysはrole、artifact、manifest、files、directories。roleは上記str、manifestはFD、filesはFD list、directoriesは相対directory str list。filesはfile相対文字列全体による昇順・重複なし、directoriesも文字列昇順・重複なしで、root自身の空文字entryは置かない。全数学親の実file/dir EOFと照合したrosterを保存する。before値の一部だけ、旧順の無認証copy、別sourceのrosterで置換しない。

artifactのexact keysはrun、attempt、head、id、name、bytes、sha256、workflow、repository_id、conclusion。run/attempt/id/bytesはposint、repository_idはint 1312092366、headはhex40 str、name/workflow/conclusionは非空str、sha256はsha256:H。旧受理親には保存runのconclusion=failureのものもあるため、16個全部へsuccessを新たに要求しない。既存の各固定tupleと完全一致する前提を保持し、continuationには受理済み実success候補の条件を課す。今回の通常親は実64/rank1450/gen8155で、別batchへ置換しない。

raw_sourcesの順と全pinは次の三つ。

| file（SOURCE_ROOT基準） | bytes | sha256 |
|---|---:|---|
| scratchpad/a0_paper_words_v1.json | 115928 | 90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893 |
| scratchpad/a0_v2_words.json | 106133 | fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612 |
| scratchpad/fuda1_a0_rmax_data.g | 4709 | 625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba |

accepted_owner/headは実receipt本体でなく三字段FDである。ownerの固定全pinは8612 B/e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b。headはこの実64入場のacceptance.selected.head及びcontinuationの全file rosterへ結ぶ。親HEADの内部sha256、state_head、resource startのseal等へ取り替えない。startのbindingは元受付のcopyなので、wrapperは自ら認証した元受付と全nested内容を比較する。startの自己sealだけから未完工程の正当性を補わない。

F4. 親descriptorのfile基準

parents[i].manifest.fileとfiles[j].file、accepted_owner/head.fileは、そのroleのCLIで渡したenvelope rootからのPOSIX相対pathである。resource scratch、REPORT、repo、manifest自身の所在directory基準ではない。task712もdata subdirectoryでなくreceipt/checkerを同時に含むenvelopeを指す。

| role | manifest.file |
|---|---|
| state | state/manifest.json |
| delta, seed34 | output/manifest.json |
| packet, refinement, continuation | output/HEAD |
| oracle, e | output/manifest.json |
| p1 | manifest.json |
| task712 | r07-grade2-maps-v4/manifest.json |
| rho2 | task640-payload/manifest.json |
| prepare | prepare.1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865.json |
| block-0 | block-0.9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74.json |
| block-1 | block-1.d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6.json |
| block-2 | block-2.a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac.json |
| block-3 | block-3.642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01.json |

file descriptorはrelative pathの区切り・safe path・全file bytesを元受付と同じまま扱う。新resource JSONに数学親のhost root一覧は追加されない。roleから既存CLI/envelopeへのmappingはwrapper側の入場metadataで保持する。

F5. 通常resource result・index receipt・state

<scratch>/result.jsonはR.resultのsealed object。exact body keysはstatus、session_sha256、word_result_sha256、root_id、root_sha256、word_manifest_sha256、indices、index_states、cache、samples、eof、successful_word_bundle、fixture_only、candidate、cross_checked、verified。

| key | 型・意味 |
|---|---|
| status | 通常成功PASS、通常停止UNKNOWN_RESOURCE又はFAIL。fixtureはF8の扱い |
| session_sha256 | H、当該start.json全bytes |
| word_result_sha256 | H又はnull、語output/result.json全bytes |
| root_id | uint又はnull、形成した語rootのID |
| root_sha256 | H又はnull、同root node_sha256 |
| word_manifest_sha256 | H又はnull、語output/word-manifest.json全bytes |
| indices | 完了したindex receipt objectのlist。番号昇順で、未完indexはこのlistへ含めない |
| index_states | 作成された全indexのstate list。番号昇順で、未完も含む |
| cache | F2 exact object。最後の実状態 |
| samples | uint、記録されたsample数 |
| eof | B。resource resultのstatus=PASSの場合だけtrue |
| successful_word_bundle | B。通常PASSだけtrue。fixtureではfalse |
| fixture_only | B。通常false |
| candidate, cross_checked, verified | B、すべてfalse |

通常PASSのindices/index_statesはそれぞれ二個で、number 0/purpose build、number 1/purpose rereadの順。index_statesの二要素はclosed=true/finished=trueであり、対応するindicesのroot_id/root_sha256は同じ完全語へ結ぶ。新resource resultはword13fileへ追加しない。

各index receiptはR.indexのsealed object。exact body keysはnumber、purpose、binding_sha256、file、bytes、sha256_payload、header_bytes、stride、encoding、count、root_id、root_sha256、all_nodes_reachable、eof。

| key | 型・値 |
|---|---|
| number | uint、session内の0-based番号 |
| purpose | str build / reread / fixture |
| binding_sha256 | H。当該sessionと用途に結び付けたmetadata digest |
| file | 当該session root基準の相対str indices/<六桁番号>-<purpose>.bin |
| bytes | uint、当該binary全bytes |
| sha256_payload | H、同binary全bytes |
| header_bytes | int 48 |
| stride | int 42 |
| encoding | 固定str sha256-raw32,residue54-u8,residue54-u8,incoming-u64LE |
| count | posint、完了した語node数 |
| root_id | uint、完了語の最終ID |
| root_sha256 | H、同nodeのnode_sha256 |
| all_nodes_reachable | B、通常の完了receiptはtrue |
| eof | B true |

binding_sha256の公開metadata入力はexact {session_sha256:H,number:uint,purpose:str,stride:int}であり、schema/sha256のないこの四字段objectのcanonical全bytes SHAである。これはmetadata bindingの規則で、binary codecの共通実装を指定するものではない。

当該index receiptは<session>/index-receipts/<六桁番号>.jsonにも同じobjectとして置く。result.indices内のobjectをその実fileとcanonical全bytesで比較できる。receipt自身のsha256をbinaryのsha256_payloadへ流用しない。通常binary pathはindices/000000-build.binとindices/000001-reread.binである。

index_statesの各要素は非sealedのexact {number,purpose,rows,durable_rows,logical_bytes,actual_bytes,closed,finished}。number/rows/durable_rows/logical_bytes/actual_bytesはuint、purposeは上記str、closed/finishedはB。number順はindicesと共通だが、未完を除いたindicesでは番号が飛び得る。通常PASSではrows=durable_rows=count、logical_bytes=actual_bytes=48+42*count、closed=finished=true。actual_bytesは実file長、logical_bytesは保持する論理長である。

UNKNOWN_RESOURCE/FAILの通常停止経路ではword_result_sha256/root_id/root_sha256/word_manifest_sha256がnullで、完了receiptがあるindexだけをindicesへ収める。index_statesにはclosed=true/finished=falseやrowsとdurable_rows/actual_bytesが一致しないものがあり得る。closedは完全EOFの証拠ではない。index_statesが空listならまだindexが作られていない状態であり、nullとは別である。資源不足でresult.jsonやindex receipt自体が未形成/部分書込みなら、既存file群・sample・外側stdout/stderr/exitを保全し、期待値の空objectやPASSを作らない。語fileが先に形成されていてもresource停止の受領を成功へ昇格しない。

F6. P対照topと各testのexact nested型

自己試験stdoutはS.resource-selftestのsealed object。exact bodyはstatus、tests、fixture_scope、production_interfaces_used、paths、paths_receipt、reference_source、old_full_suites_run、candidate、cross_checked、verified。成功status=PASS、fixture_scopeは非空str、production_interfaces_usedは非空str list、old_full_suites_run=int 0、三assuranceは全false。source_files/raw_inputs/work_roots/settings/counters/measurement/actual_*というtop別名はない。

testsの順は次の三名。各要素は非sealed objectで、name:str、status=PASS、rejected_cases:非空str listが共通である。拒否名listはsourceで定めた対照の実完了順を保持する。

| name | 共通三字段以外のexact keys / 型 |
|---|---|
| disk-index-cache-and-integrity | rows:int 13、cache:F2型 |
| old-word-bytes-and-new-reread | reference_source:FD、word:下記四字段、root_id:uint、root_sha256:H、normalized_pair:下記nullable型、ops:下記ordered list、old_full_suites_run:int 0 |
| scratch-line-and-resource-boundaries | fixture_resource_limits_only:B true |

第一testのcache設定はpage_rows=2、page_bytes=84、cache_pages_limit=2、io_buffer_reserve_bytes=168、configured_cache_and_io_bytes=336。row13と小設定は試験定数で、本番1450行や本語のnode総数ではない。成功時はmax_resident_pages=2、evictions>0、close後resident_pages/resident_payload_bytes=0である。hits/misses/flushes等の実値を本票では生成しない。

第二testのwordは非sealedのexact {file:str,bytes:uint,sha256:H,nodes:posint}で、fileはordered-word.jsonl。その基準directoryはF7のfixtures/word/new-wordで、old-word側の同名全bytesとの比較対照である。root_id=nodes-1、root_sha256は同rootのnode_sha256。normalized_pairはnull又は長さ2のint 0..2配列であり、nullは18整除条件が成立しない型付き結果である。空配列や[0,0]に補完しない。この小fixtureの値を本語のnormalized結果に流用しない。

opsは文字列昇順のexact list [Act,Identity,IntegerPower,Inverse,Letter,OrderedProduct,Ref,Rel]。reference_sourceはtop/第二testで同じFD、file=search/d972_r07_continuation_positive_word_readout_v3.py、bytes=200658、sha256=bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16eで、SOURCE_ROOT基準である。旧sourceの短い対照入口だけを使う仕様で、旧五群や旧本Pの成功receiptではない。

F7. paths_receipt・群別配置とpath基準

自己試験に --scratch <REPORT>/resource-selftests/P/scratch を指定する場合、U=<REPORT>/resource-selftests/P、T=U/scratch、F=U/fixturesとする。REPORTはRUNNER_TEMP配下の実絶対pathである。省略時は新しいOS TEMP配下のUを取り、同じ構造を使う。通常Pのscratch=<REPORT>/resource-Pとは別である。

pathsはR.selftest-pathsのsealed object。exact bodyはscratch:absolute str、fixtures:absolute str、temporary_roots_only:B true、delete_on_exit:B false、explicit_scratch:B、producer:FD。scratch=T、fixtures=F。paths_receiptは非sealedexact {file:absolute str,bytes:uint,sha256:H}で、file=U/resource-selftest-paths.jsonの実絶対path、sha256はそのfile全bytes。REPORT相対文字列をこのfile字段へ書き換えない。paths全objectと当該fileのcanonical全bytesを一致させる。

| 保存対象 | Uからの実相対配置 |
|---|---|
| paths receipt | resource-selftest-paths.json |
| 第一群session | scratch/store/ |
| 第二群session | scratch/word/ |
| 第三群session | scratch/paths/ |
| 第二群・旧短語 | fixtures/word/old-word/ordered-word.jsonl |
| 第二群・新短語 | fixtures/word/new-word/ordered-word.jsonl |
| 第二群・未到達node対照語 | fixtures/word/orphan/ordered-word.jsonl |
| 第三群fixture root | fixtures/paths/ |
| 第三群・整数容量と小値語 | fixtures/paths/decimal-capacity-word.jsonl |

各session directory内にはstart.json、telemetry.jsonl、result.json、indices/、index-receipts/があり、schemaはそれぞれR.start、各行R.sample、R.result、各receipt R.index。これらのstartはscratch/直下に一個だけあるのではなく、三群それぞれに存在する。index receipt.fileの基準もscratch/全体ではなく、その群のsession directoryである。

三群startのbindingは通常F3と異なるexact {mode:str,producer:FD}で、mode=resource-selftest。fixture_only=true、resume=false。通常数学親のacceptance/parents/accepted_head等はこのfixture bindingに存在しない。fixture completion resultのword_result_sha256/root_id/root_sha256/word_manifest_sha256はnullである。fixture自身のstatus=PASS/eof=trueは試験sessionの完了を表し、successful_word_bundle=false、candidate/cross_checked/verified=falseで、本語13fileの成功ではない。途中で対照自体が中断した場合はINCOMPLETEか、資源上receipt未形成となる。

| descriptor.field | fileのrelative base / 実値 |
|---|---|
| paths.producer.file | 実行したP4 source所在directory（通常SOURCE_ROOT/search）基準のbasename d972_r07_continuation_positive_word_readout_v4.py |
| fixture start.binding.producer.file | 同じP4 basename、同じ基準 |
| top及び第二test.reference_source.file | SOURCE_ROOT基準のsearch/..._v3.py |
| normal start.binding.producer.file / consumer_sources.*.file / raw_sources[*].file | SOURCE_ROOT基準 |
| normal start.binding.acceptance.file | 実絶対path |
| paths_receipt.file / paths.scratch / paths.fixtures | 実絶対path |
| index receipt.file | 当該通常又は群別session root基準 |
| 第二test.word.file | fixtures/word/new-word/基準 |
| 数学親FD.file | F4のrole別envelope root基準 |

paths.producerとfixture binding.producerのbytes/SHAはF1の新P4全pinである。basenameだからrootをcwdから推測するのではなく、実行票のP4 source pathへ結ぶ。

第三群が作るfixtures/paths/parent-linkはsymlink拒否対照の一件だけで、最新root裁定により成功・失敗のどちらでも除去する仕様である。この一件は完成REPORTに残す対象ではない。拒否名scratch-symlink-parentは保持し、parent/、protected.txt、他の全fixture、全scratch/index/telemetryは保存する。空のparent directoryもdirectory inventoryの対象である。無言除外や全fixture cleanupを認める意味ではない。

F8. fixtureの小さい資源枠と未形成の扱い

三群とも開始時cacheはF6の小page/cache設定で、start.limitsのline_bytes/scratch_bytes/free_floor_bytesはF2と同じ67108864/17179869184/1073741824。登録resource-selftest CLIのprocess_memory_bytesは7516192768、process_max_secondsは300秒のfloatである。fixture_only=trueを通常と混ぜない。

第三群には次の一時対照があるが、開始時start.limitsを書き換える仕様ではない。これらを記す別settings.jsonやtop settings/measurement字段はない。

| 対照 | sourceから定まる一時枠 / 結果型 |
|---|---|
| 一行 | 8 B（LF込み）。oversized-line-is-resourceはResourceStopを要求 |
| scratch | その時点の当該session予約済みbytesへ一時的に枠を下げる。値の再計算や予測値を本票へ保存しない |
| free floor | 18446744073709551615 Bへ一時的に上げる。disk-free-floor-is-resourceを要求 |
| CPython整数十進変換 | runtimeのstr_digits_check_thresholdへ一時的に下げる。正負のordinary exponent容量停止を要求し、元の設定を復元 |
| ordinary値/不正型/別ValueError | 小値canonical bytes保持、bool-exponent-remains-type-failure、unrelated-circular-ValueError-remains-failure |

第三群のexact拒否名順は[scratch-is-output,scratch-contains-output,scratch-below-parent,output-below-parent,scratch-contains-protected-source,scratch-symlink-parent,existing-scratch-reuse,oversized-line-is-resource,scratch-byte-limit-is-resource,disk-free-floor-is-resource,positive-ordinary-exponent-decimal-capacity-is-resource,negative-ordinary-exponent-decimal-capacity-is-resource,bool-exponent-remains-type-failure,unrelated-circular-ValueError-remains-failure]。これは今後の実receiptで要求する名前列であり、本便で実行して出したPASSではない。

fixture result.indicesは完了した対照indexだけ、index_statesは失敗を期待した対照用の未完indexも含むため、通常の「二indexともfinished」と同じ条件を課さない。第二群には複数のreread対照があり、numberやbinary/receiptの有無は実index_statesと全file inventoryを突き合わせる。終了していない試験に三群PASS、未形成resultへnull埋めの成功objectを作らない。

F9. 再現入口と読了範囲

予定する新自己試験入口はP4に --resource-selftest --scratch <REPORT>/resource-selftests/P/scratch --max-seconds 300 --max-memory-mib 7168 を与えるもの。通常は既存の16親CLI/acceptance/outputに --scratch <REPORT>/resource-P --max-seconds 5400 --max-memory-mib 7168 を加える。自己試験と通常処理を同じscratchへ連続投入せず、resumeしない。selftest stdout/stderr/exitは外側wrapperが別receiptとして保存し、P sourceはstdout.json等を自己作成しない。旧full suite実行数は0、三false assuranceを再掲する。

本票の全textと凍結sourceの該当serialization箇所を静的に読了した。source/import/AST/新自己試験/本P-D/GHA/数値計算は本便で実行していない。Task1022の新返信以外については、rootが途中で明示した一件symlink修理と1016記帳だけが例外であり、他source/他票/WFは変更していない。root読了後に本票だけを他系wrapper作者へ公開できる。new runtime PASS、本語の完成、実peak、A0/grade2/cofinal/verified等は未観測のままである。

AUDIT_1022_VERDICT: PUBLIC_NESTED_SCHEMA_COMPLETE_STATIC_ONLY_RUNTIME_UNEXECUTED
