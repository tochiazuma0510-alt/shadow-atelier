# Task1018 — 正語P4/D4・限定資源移行のsource監査

状態: **最終STATIC_SOURCE_PASS・新resource-selftest/AST/本語GHA未実行**。Task1018/1015/1016/1017を全文読了し、最終source/作者票とF11の限定修理まで監査を閉じた。変更は本返信だけ。1014（18881 B / `27743bc9fdaa26ab8a1d757b4a4b16e5405a4c9876148af69b8b69ab7b8409b9`）と既source/票は凍結不変。実装、ローカルPython/import/AST/GAP/数値、network/GHA/git/credentials、新agentは行っていない。両系の私的source/helper/作者票を作者間へ渡さず、所見はrootへ返した。以下F0–F10の途中状態は保存時点の記録で、最終判定はF11–F12による。

## F0. 公開契約と初回保存境界

Task1018は3393 B / `aaf3b00dfb26c69457d393dcb3acd628a6eadc070b053a90ed0a60f01ee7eff8`、Task1015は7560 B / `ac06f6997090358956e0f61661afc695fb6d75201c7916f3eadd3f9f84a01a7d` を実bytes/SHAで照合した。第一段階を限定管理表のdisk化と通常計測に絞る公開契約は1014の裁定と整合し、full streaming/cursor/IR/Fox spillを追加していない。

初回観測時P4は未保存、D4は旧D3のコピーで176579 B / `273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c` / LF2636、変更blockはまだ無い。これは新D4の完成やfreezeではない。旧P3/D3の資源・main・CLI・source closureを再読し、以下の監査条件を整理した。作者から完成blockと最終pins/票を受けて全本文/全diffを読み切るまで、新source PASSは出さない。

## F1. 登録値と保持する数学の型

初回正語は全16親/実64/rank1450/gen8155で、batchの新候補を親へ差し替えない。公開八op/六node字段、同じDFS add/yield/send/ancestor発行順、全node ID/Ref/receipt/zero・反復edge、canonical全bytes/hash/EOF、同root mod54/18、非unit Actと全11slot/full80644、PB4-droppedの範囲を保つ。source lower96776とphysical lower32260は別型で、全五PB4 endpoint/typed rowを保存する。外側source/acceptance/elapsedを含む来歴hashは新sourceへ更新し、固定入力のordered-word bytesの同一性と混同しない。

index page cacheは同一processの対象全表の合計設定上限67108864 B。一行枠も67108864 BだがこちらはLF込みのread上限で、cache枠とは別。scratch総16 GiB/minfree1 GiB、P5400秒/D10800秒/各7168 MiB、新resource selftest内部300秒/外360秒を保持する。これらは全process常駐量や完走の保証ではない。残るsymbols/ancestor/paused factors/body/canonical一行/Fox live/printed行を作者票へ列挙する。

## F2. sourceへの接続を確認する単位

| 単位 | 旧sourceの実接続 | 新sourceで閉じる条件 |
|---|---|---|
| P構築表 | WordDAG251–327、全hash/pair/unused positions | 元IDのdisk表、append後read可視性、全hash/pair型、positions廃止、旧product/addの数学と発行順不変 |
| P独立再読 | read_normalized_pair2422–2465 | 別の空indexから元JSONL全読取、構築pairを答えとして再利用しない、root/全file/全receipt/Rel/型/EOF一致 |
| P既存list利用 | lenとprior child照会、末尾hash/pairの参照 | 通常node IDは負値/boolを拒否。内部の旧末尾参照を明示的なlast IDへ直すか、限定viewの互換動作を根拠付け、負IDをfile末尾へ静かに写さない |
| Dcatalog/到達 | NodeCatalog407–514、children/usesとreachable/todo | 全offset/hash/edge occurrence/usesをdisk化、全span/record EOFと元word全bytesへのbinding、strict priorに基づく降順到達、全N bit/末尾padding |
| D各pass | normalized_pair516–543、evaluate_slot545–578 | 独立remaining初期化、元uses不変、zero/反復edge一回ずつ、全operand完了後の解放、最後はremaining全0/rootのみ |
| D意味join/解放 | RefRecipes1828–1917、AncestorIndex1167–1234、main2513–2544 | Refの元16親recipe/pointer/binary/字列/順序認証を維持。unused pointedの値だけを保持しない。全11slot前の既存解放境界を保つ |
| D一般Fox | TypedFox172–203、same_word_eleven634–725 | 旧非破壊則・Ref alias・空row/endpoint・全printed順・full filtered/直接physicalを保持。spillやIRを新たに混ぜない |

## F3. 新資源helperの閉鎖条件

cache設定を表ごとに64 MiBへ増殖させず、同時liveの合計を確認する。page payloadと管理objectの実RSSは区別する。dirty eviction/flush、短いread/write、append直後の同一page・別page読取、reset後の旧cache無効化を追う。stride×count・offset+length・edge span・u64への変換は十分な整数幅で先に照合し、bool/負値/不正型を資源超過へ隠さない。

一行は上限を超えて切捨てたままparseしない。合法な上限超過/期限/MemoryError/ENOSPCはUNKNOWN_RESOURCE、型/hash/scope/EOF不一致はFAIL。無関係なOSErrorや実装例外を一括して資源停止へ変換しない。元P3はRLIMIT_ASとru_maxrssを別に扱い、元D3は定期alarm/RSS guardを持つ。新sourceの実設定/観測を正確に記録し、設定値をpeakへ読み替えない。

scratchはfresh/no-resume。全入力/語/D output/受付/source/rawとの同一・包含・symlinkをmkdirや診断書込み前に拒否する。完全文node/index/flush前tail/EOFは別countとし、indexだけの形成で13file/D成功にしない。partial index・小sampleは外側保存へ残す。新word-root/入力全pin/自系source/format/invocationを束縛し、他系cacheや既存scratchを採らない。

## F4. 新対照・計測・未完成境界

新resource-selftestは通常append/read/cache/EOF/到達/remainingを実際に通す必要がある。小cacheでevictionとdirty read後flushを発火し、固定旧自系helperか具体固定byte anchorへ全八op・0/負/正Power・反復child・Ref alias・非unit Act・同root mod54を比較する。Dは別の適法完全rootで全11slot/typed row/printed/direct/physicalまで届かせ、非unit中間値用の短いanchorと区別する。旧suite全再走や新helper同士だけの往復では旧同語一致を代替しない。

future/negative ID、stride/count/EOF/部分index/短縮hash、uses/未到達/zero edge欠落、異source/scope、scratch path、低いfixture資源枠の発火を通常helperへ接続する。対照のため旧自系sourceをloadするなら、全path/bytes/SHAと必要closureを新実行票へ登録し、他系helperを使わない。

4096node又は5秒の小sampleとphase境界を基準に、完全countとdurable count、edge/zero/Ref、最大fan-in/行長、cache実bytes/上限/hit/miss/flush、parse/追加位置read、frame又はslot/live handle/support、RSS/AS/IO/limitを分ける。全Nの新計測表や全heap走査を作らず、欠測nullと最後のsample時刻を残す。完成block、最終source/作者票/pinsは未読または未形成であり、現段階はIN_PROGRESSである。

## F5. 新管理表blockの先行読了と短読の必須境界

Pのresource prefix、WordDAG、DFS resolveの差分、構築／空index再読／通常run接続、新三群とmainの初稿を読了した。Dはresource prefix、NodeColumn/DiskRemaining/LiveRows、NodeCatalog全body、元TypedFoxへの計測挿入まで読了した。途中の二並列出力にあった切詰めはPのadmit先頭とrun末尾を再読して補完した。以降の保存時点観測はP244582 B / `bf9a6b2149a37d70a2890c4e303bf140e86ffc1615c044bcb9efcf7bf42f2ff6` / LF4125、D207606 B / `9f270c4092d09eaca84a540f01fc1765d6e484e22cbbfefdb409c341d72ff22b` / LF3259、両CR0。ただし作者が作成中で、これは全最終本文読了・freezeのpinではない。

Pのprivate行は`<32sBBQ`（hash/pair/uses）、一つのpoolを全storeで共有し、構築storeを閉じた後に`reread`の空storeを作る。outer child gateはbool/負/futureを拒否し、内部末尾照会だけNodeViewの旧list互換に限定している。元`child_links`とmod54算術、DFS generatorのsend/receipt順は保持され、usesは全child occurrenceを数える。strict prior-onlyでrootが最終IDなら、root以外の各nodeが少なくとも一つの親を持つ条件は全root到達性と同値である。親をたどるとIDが厳密増加し、有限性と唯一のuses=0 nodeによりrootへ達するためで、0冪edgeも数える必要がある。

Dの`<QQ32s32sQQQB7s`行と全ordered edge列は別の自系算術で構築する。降順bit伝播はstrict priorを全edgeで確認し、全nodeと末尾paddingまで照合する。各mod54/slotに新しいremaining fileを作り、演算を終えてから反復edgeを一つずつ消費し、EOFで全remaining=0・rootだけliveを要求する。Ref aliasと空rowは値として保持し、LiveRowsは現live objectだけを数え、通常算術へin-place変更を導入していない。

未凍結Dの`ScratchContext.page`で、readintoの実gotを記帳するだけで既存物理区間の期待bytesとの一致を要求していなかった点をrootへ必須修理として送った。合法な新append領域の零と既存区間の短読を区別し、後者をFAILで拒否する必要がある。最終EOF/hash照合を弱めず、実page helperの短読対照にも接続する。これは静的所見で、故障や試験PASSの観測ではない。

## F6. 通常接続とCLI補足の未閉鎖点

P初稿の三群は実store/page eviction/read/EOF、固定旧P3のWordDAG全bytes/hash/pairと空index再読、path/低いline・scratch・free枠へ届く。旧P3の全pinをload前後に照合し、旧suiteを新実行する経路とは分けている。通常Pは16親と全入力byte認証後に自系scratchを作り、同じ13fileを完成させる。数学的な結果が形成されても、新resource receipt/exit/外側保全が未完なら成功を先取りしない。

rootの追加公開CLIを受領した。新wrapperはselftestにも`--resource-selftest --scratch REPORT/resource-selftests/P(or D)/scratch`を明示し、fixtureはその一時parentの別siblingに残す。REPORTはRUNNER_TEMPで、削除せず小path receiptとalways回収へ結ぶ。通常P/Dは別の`REPORT/resource-P`／`resource-D`、無指定selftestは自系の新TEMP可。読取初稿Pはまだ明示scratchを拒否してTemporaryDirectoryを使っていたため、この作者修正とD最終selftest/main接続を後続で確認する。新workflow自体の監査は本便の外である。

## F7. Dの通常全語接続とsignalからのcache再入

Dの全RefRecipes、AcceptedInputs、AncestorIndex、全11slot/printed/full80644、check_actualの新catalog全file hash前後joinを追加読了した。unused pointedを代入しなくした後も、元pointerのcanonical hash、positioned単一record/全hash、typed binary幅、Refの実親recipe比較を保持している。数学の追加省略は見つけていない。新三群初稿は固定旧D3の同じJSONLを全node/child/uses/mod54で比較し、別非unit Actを短いflat wordにも照合する。完全rootの三block/11slot/空row/80644は旧D3の通常helper全payloadと比較し、零rowを欠測としない。

F5のD短読修理を実sourceで再読した。既存物理区間のexpectedとstrict intのgot一致、未登録物理tail拒否が入り、実ScratchFile.read→pageを通す`existing-page-short-read-not-zero-fill`逆対照と拒否後の通常再読が接続された。source静的な修理閉鎖であり、試験はまだ走っていない。

さらにDの定期SIGALRMからの新cache再入を必須修理としてrootへ送った。旧handlerが`boundary(LAST_PHASE)`を呼ぶ一方、新boundaryはsampleを書込み、同じpage poolを操作する。例えば通常ScratchFile.writeがpageを得てbytearrayを書き換える前にsampleが割り込み、そのpageをevictすると、復帰後のdirty pageがpool外になって保存されない。sampleのbusy flagはsample同士の再帰を止めるだけで、通常page操作への割込みを防がない。signalはdeadline/RSSの停止確認に限定し、disk/cacheを触るsampleは通常の安全なboundaryに残す必要がある。数学・DFS/Fox変更は不要である。PのsignalはSTOP flag設定だけで、この再入経路はない。

Pの明示selftest scratchは後続sourceでRUNNER_TEMP／TEMPを認め、fresh scratchと別fixtures、小path receipt、削除なしへ接続したことを確認した。D初稿はTEMPだけの判定だったため、公開RUNNER_TEMPも認める小修理をrootへ送った。Dの完成CLI/main・signal修理・最終作者票/pinは引き続き待ちで、IN_PROGRESSを維持する。

## F8. 必須修理の静的閉鎖と残存資源限界

Dのsignal修理後は`resource_alarm`が`check_resource_limits`だけを呼び、通常boundaryだけがsampleを書く。第三群は実ScratchFile.writeのpage受渡しで実SIGALRMを発火し、sampleを呼べば拒否する対照とdirty writeの読戻しへ接続している。短読・signal再入・RUNNER_TEMPの三指摘は静的に閉鎖した。RUNNER_TEMP自体の絶対path／実directoryを確認し、登録REPORT配置と非TEMP逆対照を追加している。これらは今後のGHAで初めて実試験結果になる。

D完成main初稿は全path admission→新自系scratch→新D output→全語比較→scratch flush/fsync/close→完成D receiptの順である。ENOSPC/EDQUOT/MemoryError/期限をUNKNOWN_RESOURCEへ、無関係OSErrorと型/hash/意味/EOF例外をFAILへ分け、診断の書込みが再度失敗した場合も最初の理由をstdoutへ残す。DにもRLIMIT_AS設定が追加され、実設定をsampleに残す。Pは従前のRLIMIT_AS/RSS guardを保持する。いずれも全processの常駐量や完全走破の証明ではない。

Pの全hash/pair/unused positionsのN表、Dのoffset/hash/全edge/uses/到達/各pass remaining/mod54値のN/E表は対象disk表へ移った。残るPのsymbols、recipe_refs、active stackとpaused generator/factors、ancestor/symbol_order/raw/geometry/親JSON、Dの意味照合中のsymbols/ancestor/recipe/親JSONと同時live Fox/printed rowsは明示的な残存限界である。Dの追加LiveRowsは現live rowだけを計数し、全Nの計測履歴を作らない。全file mmap・新IR・literal再番号付け・Fox spill・cursor移植は導入していない。最終source/pin/作者票の全差分照合はまだ残っている。

## F9. 完成本文・作者票と独立した保持差分の読了

P4の4203行/249192 B版とD4の3679行/232749 B版まで全通常本文と新三群/mainを読了した。途中の並列出力切詰めは該当prefixとmain末尾を別読取して補完した。PowerShell/.NETでsource文字列をtop-level def/classから次の定義まで区切って旧版と比較した結果は、Pが旧71/new94・全文一致49・変更22・追加23・削除0、Dが旧67/new90・全文一致47・変更20・追加23・削除0。decorator/間のglobalが前blockに含まれる単純なtext境界であり、AST解析や関数単位の実行結果ではない。

変更blockも本文と旧新text差分を読んだ。PのTargetWordCompilerは18 methodのうちresolve/geometry/build_E_sourceだけに差があり、前者は現stack/symbol/欠測peakの計数、後二者は実readのI/O計数である。旧generator/sendとproduct/act/power/refの発行順は保持されている。TargetHistory/Ancestorsも読取byte計数のみ。通常admissionの新P/D path二本、登録済64/1450/8155のstrict int guard、line/path/資源処理を加えているが、元64履歴・各Refの16親recipeへの全joinを省いていない。互換の旧selftest用fixtureは、それまで孤立していた二productを0冪edgeでrootへ結ぶだけの変更で、新GHAの旧suite再走を要求しない。

DのAcceptedInputs二path、RefRecipesのscan label、TypedFoxのobserve呼出し、OutputFilesのsort計数を除く保持textを旧D3と比較した。全11slotの通常same_word_elevenは計測の追加のみで、full80644/全五PB4 typed row/printed/direct/物理行のgateを保持する。NodeCatalogの新管理表・各remaining・普通mod54の分岐を本文で追い、全ordered edgeと各operandの演算完了後解放を確認した。各mod54再呼出しはpass_count入りの新pair fileを作り、前passを再利用しない。全index digestは実前後size/読取total/EOFと合流する。最後のD690 B差分はresource-selftestの実work_rootsのstderr保存と、互換selftestのTEMP/全明示入力・source/output非包含保護である。

P作者票1016のF1–F9最終16518 B / `b98fe31f8e48f41bfb20ae48d26ace2b579c0d545fadb781861fe8e5fa592181`、D作者票1017のF1–F8最終15230 B / `2532bc5a15ef386e830def954407648ea0a389ba3eb7fd2f4129c85ac7e5970c`を全文読了した。いずれもsource静的状態と新selftest/本語/AST/GHA未実施を分けている。新三群はPの独自42-byte indexとDの独自112-byte/edge8 indexをそれぞれ通常helperへ接続し、固定旧自系P3/D3を短い比較先にする。Dの非unit Actは全11slotで旧D3/flat字列へ比較し、slot1では省略した三項の差を要求する。別の完全identity rootにより全11slot/full80644/全payload bytesへ届く対照と区別している。実対照のPASSは未観測である。

## F10. 保持closureと普通整数変換容量の最終残件

以下の既存全fileを実bytes/SHAで独立再照合し、全件一致した。新P/Dだけで旧source anchorやDの保持二moduleを省くclosureにはしない。新wrapperではP4/D4/P3/D3/保持C9/C4の六Pythonとraw四本が合併closureとなる。P自身のrawは三本、Dの追加q3 rawをP側へ流用しない。これらは保持TCBの明示で、既存の独立性限定を遡って閉じる主張ではない。

| 保持file | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_continuation_positive_word_readout_v3.py` | 200658 | bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e |
| `search/check_d972_r07_continuation_same_word_eleven_slots_v3.py` | 176579 | 273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py` | 113012 | 7b2beb39dbdc65494f85fa4451ed69d99a22685d11f1d4fef6e671322d24098d |
| `search/check_d972_r07_grade2_forward_adjoint_maps_v4.py` | 49643 | 7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29 |
| `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json` | 231570 | 3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72 |
| `scratchpad/fuda1_a0_rmax_data.g` | 4709 | 625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba |
| `scratchpad/a0_paper_words_v1.json` | 115928 | 90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893 |
| `scratchpad/a0_v2_words.json` | 106133 | fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612 |

最終Pのcanonical80–81/WordDAG.add772–774では、合法なIntegerPowerの普通整数がCPythonのint→decimal桁数容量へ達した場合、json.dumpsのValueErrorがmainのFAILへ流れる。Task1015の合法な実装容量超過UNKNOWN_RESOURCEとは異なるため、rootへ指摘し、rootが未公開の必須修理として採用した。固定実64でこの容量へ達する観測は無く、完走や停止箇所の予測ではない。未知のValueErrorを一括して資源停止へ移す修理は認めず、該当整数変換だけを厳密に識別し、元canonical bytes/普通整数型と実helper対照を維持する。P最終pinはこの修理後に確定する。

D最終`f901dfbb…`のexact_json796–807は、stdlibのJSON lexerが整数tokenと認識したtextをparse_int callbackのint(text)へ渡し、その変換のValueErrorだけをResourceStopへ写す。json.loads全体/canonical/型/hash/EOFのValueErrorを捕捉していない。第三群3544–3547は実exact_jsonへdigit limit+1のtokenを渡す対照を持つ。容量停止した時は、その後の全JSON/型/EOF認証を完了したとは主張しない。Dに同型の未修理は見つけていない。Pの限定差分と新pin/作者票の再読が済むまで、全体の最終PASSは保留する。

## F11. 最終限定修理の閉鎖とfreeze pins

Pの整数容量修理後は、元json.dumps/ASCII/LF式をそのまま実行し、正確なValueError型・CPython・正の実get_int_max_str_digits値・その値を含む既知の変換容量message全文/単一argsだけをinteger_decimal_capacityで識別する。これに合う場合だけResourceStop、その他は元例外を再送する。文字列/普通整数型、通常のcanonical bytesを変えない。第三群は実WordDAG.powerへ正負の10**thresholdを渡し、node count/word length/stream位置がappend前から変わらないこと、bool指数と実circular canonicalが型/無関係ValueErrorのままであること、-18/0/18の固定bytes、元digits設定をfinallyで復元してから通常append/flush/到達EOFを続けることを要求する。対照はsourceで接続を確認しただけで、実PASSではない。

このhelper/canonical、第三群、production_interfaces_usedへのcanonical名追加をメモリ内で元へ戻した全sourceは、独立に249192 B / `028a3cb48edeed8854d6f47ceb7f0de9ecc1d4b06ba7f8b56ef3c2bb9b76d7da`へ完全一致した。最初の二区間だけでは残った13 Bはこの公開入口名であり、算術の隠れた差分ではない。新sourceの通常import/DSL/字列/Fox/Ref算法には別の変更を加えていない。P作者票のF9更新/F10/F11を全文読了し、公開selftest top keys、三群、paths/paths_receipt/reference_source、通常resourceのstart/sample/index/result字段を実sourceへ照合した。Pのtopに無いD側のsource_files/work_roots等を補って同じ型と呼ばない。

rootの新wrapper公開ABIに合わせたD最後の差分は、新resource-selftestのcandidate literalだけTrueからFalseへ変更した一箇所である。これを逆置換した全sourceは独立に232749 B / `f901dfbb0652f0827b4a9cc1b9e2b836105183ebd2e1ed9c2fac4fc1974e4bd5`へ完全一致した。新三assuranceは全False、旧selftest/通常D/失敗receiptの既存型は保持する。作者票F6/F8の説明/pin差分も読了した。Dのparse_int容量分類はF10の境界としてrootが受理し、追加修理は要求していない。

| 最終file | bytes | SHA256 | LF |
|---|---:|---|---:|
| `search/d972_r07_continuation_positive_word_readout_v4.py` | 252290 | 0fc1c039d3ae076107585da88624c01656458c11d1d07df0054dcbec88fadeea | 4255 |
| `search/check_d972_r07_continuation_same_word_eleven_slots_v4.py` | 232750 | 41d53b3779e26b04431a033877efbd315eb32b1d4538efa742bf900996db797b | 3679 |
| `sol/luna_reply_1016_r07_positive_word_resource_stage1_producer_v4.md` | 22768 | eb7b284b49e9d136c21c29718e638aabee41c86083d7905f17b033309e182aa4 | 113 |
| `sol/luna_reply_1017_r07_same_word_resource_stage1_checker_v4.md` | 15676 | f4c623564088f835bfbb2d3fc8085282d389d0a2dc02dd00ea5168448abd5a26 | 71 |

全四fileを実bytes/SHAで再照合し、CR0/BOMなし/finalLF/行末空白0を確認した。作者の再freeze通知とも一致する。全source文字列の読了とハッシュ/逆置換の照合であり、AST/import/自己試験を実行したという意味ではない。

## F12. 判定の射程

登録された第一段階としてSTATIC_SOURCE_PASS。短読、signal再入、RUNNER_TEMP、普通整数十進変換容量の四指摘と最後の対照票assurance整合は、上記最終sourceで静的に閉鎖した。全canonical/DFS/Ref/全語読取、各passの全edge、旧非破壊Fox/全11slot/full80644を維持する配置変更であり、今回の範囲にIR/streaming grammar/cursor/Fox spillを必須として追加していない。各自のdisk reader/codecと固定旧自系短語anchorを使う境界も閉じている。

全常駐量の上界、64 MiB以内の巨大一行生成、paused recipe/factors、同時live Fox/printed/親metadataの峰値は閉じていない。正当なUNKNOWN_RESOURCEは残る。最後のsampleを停止瞬間や全phase peakとは呼ばず、未観測のN/E、完走、秒数、速度向上は推定しない。新resource-selftest/AST/本P4の完全13file/本D4全比較/新入力前後不変/全scratch受領と新workflow/CV-9はrootの後続判定であり、本票のsource PASSで代替しない。別batch状態を正語の16親/実64へ混ぜず、A0/grade2/COMMON/cofinal/fake/Ihara/cross-checked/verifiedを昇格させない。

AUDIT_1018_VERDICT: STATIC_SOURCE_PASS_FOR_LIMITED_STAGE1; ALL_REQUIRED_SOURCE_DELTAS_CLOSED; RESOURCE_SELFTEST_AST_FULL_WORD_GHA_AND_CV9_UNEXECUTED.
