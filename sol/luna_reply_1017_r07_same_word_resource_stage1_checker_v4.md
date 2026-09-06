# Task1017 — 独立D4のdisk catalog・第一段階

**F1 — 射程と現在の状態。** Task1015（7560 bytes / ac06f6997090358956e0f61661afc695fb6d75201c7916f3eadd3f9f84a01a7d）とTask1017（3611 bytes / e0a765478bb4ca705dfcabe3229f0ac9ad5af2e5e095103c72268d2fd88fc20f）を全文読了。自系設計1013（22384 / 5895b4e8cfbf890bd8ab8e2af2a4161d474151abf0b19fad75659091e8238f72）と凍結D3（176579 / 273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c）に基づき、指定の新source `search/check_d972_r07_continuation_same_word_eleven_slots_v4.py` と本票だけを作成した。新P本文・1012/1016票・他系helperは読んでいない。旧source/995/1009/1013/1006・workflowは不変。ローカルPython/import/AST/GAP/数値/network/git/credentials/追加agentを実行していない。全通常入口・新対照・自系静的差分を閉じ、F8のsourceで作者freezeを行う。独立1018最終票と実GHAは別判定である。

本語のD3はrun34001672135/1で未到達だった。旧三群PASS、P側のMemoryError、途中node末尾のidから、D4の本語node数/edge数/peak/時間/完走を予測しない。別の初回batch34004423047/1（15親/旧64/k32/1/refill=false）は本実装の親へ差し替えない。正語は登録済み16数学親・64履歴/rank1450/gen8155を維持する。

**F2 — 独立private formatと所有。** wire schemaは従来の `d972.r07.continuation-positive-word.v1` / `d972.r07.continuation-same-word-eleven-slots.v1` を維持し、consumer_sourcesのP/self pathだけをv4へ結ぶ。固定親/辞書/event列に対するordered-word.jsonlの同一bytesを照合する。新source/acceptanceを含む外側13fileのhashを旧値へ偽装しない。

private formatは `independent-D4-node112-edge8-v1`。source/source closure・raw pins・runtime・invocation UUID・実CLI入力・設定を `binding.json` へ記録し、受付後は別の `admitted-inputs.json` でacceptance全hash・実word13file roster・全16親のmanifest/record hashへ結ぶ。各 `catalog-NNNNNN/start.json` は実元word path/全file descriptor/root ID/hash/dictionary/ancestor countとbinding全hashを持つ。完成headerは同じ字段に実N/E・全index/edge file hash・EOFを加えたsealed `.resource-catalog-complete`。cacheからの再受付・resumeは実装していない。

| file / 型 | exact layout・更新 |
|---|---|
| `nodes.index` | little-endian `<QQ32s32sQQQB7s`、112 bytes/node。offset8、length8、inner SHA32、全line SHA32、edge-start8、edge-count8、total-uses8、op1、reserved零7。IDは元の行番号、offset/countは普通非負整数をu64へ容量照合して記録。 |
| `ordered-edges.u64` | 元args順・重複込みの全child ID、各8 bytes。strict prior ID/hashを実元行へ結び、0冪も二つのAct operandも省かない。 |
| `reachable.bits` | ceil(N/8) bytes。rootをmarkし、strict priorによりID降順で全childへ伝播する。各nodeのmark、全edge visit、末尾未使用bit/EOFを照合。Pythonの全reachable set/DFS stackを置かない。 |
| `PP-<pass>-remaining.u64` | passごとに元indexのtotal-usesから独立に新規8N bytesを初期化。各occurrenceを一件ずつ消費し、underflowを拒否、全Nの零/全E消費/生存root一件をEOFで照合。旧usesは変更しない。 |
| `PP-mod54-pairs.u8` | 各node二つの0..53の普通整数剰余。2N bytesをdiskへ記録する。F3 packingではなく、最後の18整除/正規化の型を維持。 |

初回実mainではmod54一回＋11slotの12 remainingを別に保持するので、これらの完了時のデータ長は `210N + 8E + ceil(N/8)` bytesにheader・telemetry等を加えた形となる。これはformat式で、未観測N/Eの代入やscratch収容保証ではない。型/stride/span/予約byte/全file size/全hash/EOFを読む。合法なu64容量超過はUNKNOWN_RESOURCE、既存recordの不正ID/型/hash/EOFはFAILとする。

**F3 — page pool・canonical read・remaining。** 全対象fileで一つの `ScratchContext.pages` を共有する。通常pageは65536 bytes、mmapなし、合計上限67108864 bytes。bytearrayだけでなくentry/key/int/OrderedDictの実 `sys.getsizeof` を保守的に加算し、追加前の余裕と追加後の実pool計数を照合する。汚れたpageはeviction前に実fileへ書き、count/type/書込長を照合する。全fileのhandle/header等は別の小さいPython管理表であり、process RSSとpage poolの数値を同じものと呼ばない。

既存物理区間のreadintoは期待 `min(page_bytes,max(0,physical_size-page_start))` と実gotを厳密一致させる。appendで未形成の区間だけを零初期化でき、既存区間の短読を零と読まない。digestも全読取bytesと前後size/EOFを照合する。書込み前に実空容量floor 1 GiB、logical scratch全file合計16 GiBを守る。MemoryError・期限・ENOSPC/EDQUOT・正当な表現容量超過はUNKNOWN_RESOURCE、それ以外の実装例外を資源停止へ隠さない。

NodeCatalog.readは毎回元JSONLへ位置読取し、全canonical bytes・inner hash・全line hash・exact六字段と八op args・全prior child hash・実disk child列を照合する。初回の全Ref scope/一意symbolは保持し、その後の実親recipe照合で順序/係数/全receiptを閉じる。metadataの解放後も初回完全認証済みline全hashへ結ぶ。最初の全readlineはLF込み64 MiBまでで、それを超える合法行はUNKNOWN_RESOURCE。JSONの普通整数tokenがstdlibの桁容量へ達した場合もUNKNOWN_RESOURCEであり、指数を切り詰め・mod3化しない。新streaming grammar/認証済みIRは導入していない。

全到達時の全node parseは依然として初回1回＋Ref scan1回＋mod54の1回＋11slot＝14回で、recipeの追加位置readとroot再readは別counter。入力前後のword全hashも別に数える。参照数は毎pass独立、operandはop完了後に全edge分消費する。Foxのlive dict/不変入力rowとRef aliasはそのままで、空rowは正当な値として扱う。LiveRowsの追加計数表は現在liveのrow identityだけを保持し、全過去Nの別表を作らない。

**F4 — 維持した算術と残存peak。** 一般LEFT FoxのProduct/Inverse/整数Power/非単位Act、全11slotのnative printed順、direct/prefix、全80644、元rho2/target歴史/Ref recipe/全入力前後不変は維持する。無関係なsource_lower96776零やfull P Fox零を新gateにしない。PB4-dropped physicalへはfirst6、全5PB4 endpoint/typed rowは保存・照合する。一般Actの三項を省かない。

symbolsの完全(namespace,key,scope) dictとsymbol_order整列はR依存のまま残す。ancestor entries、parent JSON/全roster、8059の元recipe、最大node行/factors、同時live Fox/Power途中行、printed累積、二hexagon行、sort、floor/mapsも残存する。AncestorIndex.pointedは旧D3で設定だけされ、その後参照されなかったことを静的検索で確認し、全pointer/hash/JSONL/binary型照合後の未使用解釈値の保持だけを外した。全N/E依存memoryの消滅や全語7168 MiB内完走は主張しない。Fox spill・外部sort/merge算術・node併合・語再番号付け・積の再結合は導入していない。

計測は4096 node read events又は5秒、通常phase境界の小sampleで、履歴配列をRAMへ蓄積しない。declared/authenticated/complete node・edgeを区別し、max line/fan-in/指数bit長、zero edge/Ref、全parse/canonical bytes・位置read・prior hash/graph/remaining、pool hit/miss/eviction/flush/実bytes、logical/physical scratch、現在slot/live handle/異なるrow/support・単一/中間/printed/sort supportを記録する。Linux ru_maxrssはKiB・process累積peak、VmRSS/VmHWM/VmSize/RLIMIT_AS/proc IOは実取得値、欠測とparent metadata overheadはnull。設定7168 MiBや最後のsampleを実peak/停止時点へ読み替えない。SIGALRM handlerはdeadline/RSS照会のみで、cache/sample/printへ入らない。sampleは通常協調boundaryに限る。

**F5 — source/import closureとCLI。** 通常D4のrepo importは自己と次の保持C9/C4、他はstdlib/NumPy。新resource対照だけで凍結D3を一module追加ロードし、その通常NodeCatalog/read/mod54/evaluate_slot/same_word_elevenを短い比較先に使う。D3のmainや旧三群selftestは呼ばない。各sourceの実path/bytes/SHAとraw4・runtimeを対照票に列挙し、前後の実source/raw全bytesを照合する。D3 sourceは新wrapperがstage/pinするまで実行しない。

| file | bytes | SHA256 |
|---|---:|---|
| search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v9.py | 113012 | 7b2beb39dbdc65494f85fa4451ed69d99a22685d11f1d4fef6e671322d24098d |
| search/check_d972_r07_grade2_forward_adjoint_maps_v4.py | 49643 | 7ba94ee884db49bbe42d11a84228a6bdf7c88a3918407928af90c71b65fe4a29 |
| search/check_d972_r07_continuation_same_word_eleven_slots_v3.py（対照だけ） | 176579 | 273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c |
| ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json | 231570 | 3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72 |
| scratchpad/fuda1_a0_rmax_data.g | 4709 | 625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba |
| scratchpad/a0_paper_words_v1.json | 115928 | 90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893 |
| scratchpad/a0_v2_words.json | 106133 | fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612 |

通常CLIは従来16root（block-root四回）/acceptance/word-root/output/producer limitsと、`--scratch "$REPORT/resource-D" --max-seconds 10800 --max-memory-mib 7168`。新対照は次の一回をrootが別wrapperで登録する（本便では未実行）。

```bash
python -B search/check_d972_r07_continuation_same_word_eleven_slots_v4.py \
  --resource-selftest --scratch "$REPORT/resource-selftests/D/scratch" \
  --max-seconds 300 --max-memory-mib 7168
```

REPORTはRUNNER_TEMP。scratchは新規、fixtureはそのparent内の新規sibling。gettempdirと明示RUNNER_TEMPの実pathを許し、非TEMP・symlink/junction・既存scratch・全数学親/word/output/acceptance/source/rawとの包含をmkdir前に拒否する。scratch省略時の新対照も自系TEMPへ作り、実pathを小receiptで返す。runtime/partial/scratch/index/samplesは削除せず、常時保存するenvelopeで扱う。原語13file・D成功rosterへ混ぜない。normalPASS/typed NOT_APPLICABLEはexit0、不正はFAIL/exit1、資源はUNKNOWN_RESOURCE/exit3。部分停止はcomplete_receipt=false/eof=false/manifest=nullで、cache完成を全D成功へ昇格させない。

**F6 — 新resource-selftestの実入口。** stdoutはsealed `.resource-selftest`、status=PASS、三tests各name/status/rejected_cases、source_files/raw_inputs/work_roots/settings/counters/measurement、old_success_suites=0、actual_parent_artifact_replayed=false、actual_word_D_complete=false、candidate=false/cross_checked=false/verified=false。全counts/時間はGHAで初めて実値となる。Task1019接続前のroot公開指示により、新resource-selftestのcandidate literalだけをFalseへ合わせた。旧selftest/通常D/失敗receiptの既存型は変更していない。

1. `disk-catalog-pages-canonical-and-refcounts`。小cache 16384 bytes/page128で実eviction/flush/resetを発火させ、同じ八op・157 nodeの短い合成DAG全bytes/全edge/usesを自系D3へ完全比較。反復Ref・0/負/正Power・全到達を保持し、mod54は同じrootと18/36の普通剰余を照合する。実本語のNを157と称さない。
2. `same-D3-eight-op-eleven-slot-and-physical`。非単位Actを全11slotでD3と短いflat字列へ比較し、slot1で省略した三項が異なることも要求する。別の全到達rootはw・w逆の完全identityで、Ref alias/空rowを含む全11slot・unsigned/printed/direct・全80644のpayload全bytesと配列をD3へ比較する。新sourceを除いた数学payload字段の除外はない。16親受付や現在target零のfixtureではない。
3. `scratch-capacity-and-authentication-negatives`。実index/read/remaining/Ref意味/scratch helperへnegative/future ID、stride/EOF、全hash、反復edge、uses underflow、未到達zero-child、異scope/完全resealした誤Ref key、partial index/source binding、既存/包含/nonTEMP/symlink scratch、未形成出力を通す。小さい行/disk枠・空容量floor/u64/普通整数parse容量は資源停止として別記する。既存pageの短読対照と、page handoff直後の実登録SIGALRM→通常write/flush同bytes対照を含む。signalからsampleへ入れば対照が失敗する。

実RSSはD3/D4を同processで小比較する累積値で、純D4本語のpeakではない。D3 anchor中のlive counterは欠測と明記する。小対照成功後も、本P13file・本D全gate・全入力前後不変・工房CV-9を別に要する。

**F7 — 静的監査の修理範囲。** 先行1018/root所見により、既存pageの期待bytes短読gate、gettempdirとRUNNER_TEMPの実path両受理、SIGALRMの非再入を新通常helperへ修理し、それぞれ実helper対照を接続した。数学/DFS/Foxの新算法は追加していない。自系のtext-only top-level block比較で旧67/new90、旧47 blockは全文一致し、旧block削除なし。変更20 blockには追加globalにより境界が広がったものも含む。保持式を明示する47一致にはCoarseReadout/IndependentFloor/SourceRecipes/PhysicalRecipes/expect_pattern/全target history/同語root manifest/grade比較/全成功receipt型が含まれる。変更blockは全差分を静的に読む対象とし、AST結果とは呼ばない。

保持数学の境界として、AcceptedInputsの二pathを戻した全文、RefRecipesのscan labelを外した全文、TypedFoxのobserve呼出しを外した全文、OutputFilesのsort計測を外した全文が、それぞれ旧D3 blockと完全一致することをPowerShellのtext比較で確認した。旧数値helperのロード・AST解析による確認ではない。NodeCatalogの一般演算の分岐/順序はsourceで直接読み、変更をdisk lookup/remaining/計数へ限定した。最後の690 bytesの差分は新work_rootsのstderr記帳と互換CLIのTEMP/入力非包含保護だけである。

**F8 — 最終freeze。** 新source `search/check_d972_r07_continuation_same_word_eleven_slots_v4.py` は **232750 bytes / SHA256 41d53b3779e26b04431a033877efbd315eb32b1d4538efa742bf900996db797b**、LF3679 / CR0 / BOMなし / final LF / 末尾空白0。指定sourceの全保持textと変更block・本票を読み、上記metadataを実bytesで照合した。新resource-selftestのcandidateをTrueへ逆置換した全bytesのSHAは直前凍結 f901dfbb0652f0827b4a9cc1b9e2b836105183ebd2e1ed9c2fac4fc1974e4bd5 に完全一致し、一literal以外の変更がない。公刊D3のpinは不変。独立1018最終票は当初の本票freeze時点では未受領であり、その判定を先取りしない。新resource-selftest・AST・本GHA・本語完走・CV-9は未実施/未観測。rootが新wrapperへ最終pins/closure/保全を登録してから実行する。source完成をcross-checked/verifiedへ昇格させない。

AUDIT_1017_VERDICT: SOURCE_COMPLETE_AUTHOR_STATIC_REVIEWED_FROZEN; INDEPENDENT_FINAL_AUDIT_AND_REGISTERED_GHA_PENDING; LOCAL_EXECUTION_AST_NOT_PERFORMED; ACTUAL_WORD_N_E_RSS_RUNTIME_UNMEASURED.
