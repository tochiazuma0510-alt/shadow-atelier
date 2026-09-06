# Task1015 — 正語資源版の第一段階・公開契約

root裁定。Task1012/1013と1014の限定段階に対する予備監査に基づき、次のP4/D4は「指定する全node管理表のdisk移行と通常経路の計測」に限定する。全常駐量の有界化や完走を宣言しない。P/D各作者は本公開契約、自系旧source、自系設計票、自系実装taskだけを読み、他系の新source/helper/設計票/実装票は読まない。数学監査官だけは両系を読める。ローカルPython/import/AST/GAP/数値/ネット/git/GHA/credentials/追加agentは禁止。実行はrootが最終source監査後に新versionのGHAを一回投入する。旧P3/D3/WF4/既返信は凍結不変。

## 射程と意味保存

正語の全16数学親と登録済み実64/rank1450/gen8155から出発する。正語13file、全64履歴、公開八opと六node字段、同じnode ID/順序/全child/全receipt/Ref keyとscope、全canonical bytes/全hash/EOF、同root mod54/18、全11typed slot/full80644、非unit Act、全5PB4 endpoint/typed row、printed順・LEFT Fox・既存PB4-dropped gradeを維持する。full P Fox零を追加gateにせず、source_lower96776零を一般target語へ要求せず、physical lower32260/full physical48384を従来どおり直接読む。新batch run34004423047/1の15親/旧64/k32/1/refill=falseとは別で、新batch候補を正語の親へ差し替えない。

同じ有限語の全情報を保存した配置変更である。零係数edge、反復edge、未到達node検出、prior childの全hash、Refの実親recipeへの意味joinは省かない。nodeを併合・再番号付け・積を再結合・閉じた歴史をopaqueな葉へ変更しない。全canonical readerと通常DFS/Fox算術の順序は第一版で保持する。全node JSONの認証済みIRへの置換、巨大行の新streaming grammar、recipe cursor全面移植、Fox行の外部sort/merge・spill算術は今回の必須項目にせず、無断追加もしない。

Pの構築後mod54 readerとDは、各自が元word全bytesから新しい空の自系indexを構築する。P構築表のpairを答えとして再利用せず、DはPのindex/codec/helperを使わない。Dの各mod54/slot passの参照数状態を独立に初期化し、反復edgeを一つずつ消費する。Ref aliasを含めoperandは演算完了まで保持し、元Fox rowをin-place変更しない。空Fox rowは正当な値として扱い、欠測/nullと混同しない。

## 第一段階の資源登録

- 全file mmapを避け、各自の明示上限付きpage cacheで元IDを正確に照会する。数学共通helper/共通binary layoutは作らない。各processの対象index page cacheの合計設定上限は64 MiB（67108864 bytes）。privateなstride/page件数/flush方式は作者票で具体化し、総cache上限内で固定する。symbol/ancestor/paused factor/Fox liveなど残すPython表は列挙し、「全N/E依存メモリを除去」とは書かない。
- 同じP5400秒/D10800秒・各7168 MiBを通常上限として維持する。新resource selftestは各内部300秒/外部360秒の一回だけを予定する。source/import/runtime・新path/metadataの対照は必要な変更点へ接続するが、旧成功suiteを再走する口実にしない。
- 一行readerの資源枠は64 MiB（67108864 bytes、final LFを含む）。それを超える合法行は切捨てずUNKNOWN_RESOURCEにする。途中行を完成nodeや数学的反例としない。P writerの従来canonical一行生成、未完DFSの大recipe/factors、parent JSON/manifest全配列、Dの同時live Fox/printed行は残る資源限界として計測し、これらの有界化や全語完走を予告しない。
- scratch総bytesは各process最大16 GiB、書込み前の空き容量floorは1 GiBとする。これらは明示的な資源停止条件で数学宇宙の縮小ではない。u64等の実装容量を超える普通整数/offset/countをwrap/truncateしない。合法な容量超過/期限/MemoryError/ENOSPCはUNKNOWN_RESOURCE、型・hash・scope・EOF不一致はFAILとして区別し、無関係な実装例外を資源停止へ隠さない。指数そのものの普通整数型は変更しない。

## scratchと新CLI

通常の既存CLIを維持したまま、必要な新引数は `--scratch <path>` と `--resource-selftest`。本GHAではPとDに別の新規scratch sibling rootを明示する。selftestは一時rootだけを使う。scratchは正語13file/成功D出力・全数学親・acceptance/source/rawと包含/一致/symlinkしないことをmkdir前に実path helperで確認する。既存scratchを再利用しない。新source/入力全pin/word全fileとroot（形成後）/自系format・実設定・invocationに結び、source境界の違うcacheを採用しない。

途中word/index/cache/flush前tailと完成EOFを別に数える。第一版はscratchからのresumeを実装しない。旧実途中wordを継ぎ足さず、同じ固定親から新しい出力へ始める。内部indexのEOFや再sealだけではP13file/D全比較の成功にしない。全partial/scratch/小telemetry/実stdout/stderr/exitを新workflowのalways envelopeで保存し、word13fileやD成功rosterへscratchを混ぜない。source変更後の受付/CLI/保全wrapperは別の新versionとしてrootが監査する。作者はworkflowや他系ファイルを変更しない。

## 最小計測と新対照

新計測は累積counter、phase境界、4096 nodeごと又は5秒経過時の小sampleを基準とし、全nodeの履歴配列をRAMへ作らない。最後の定期sampleは停止瞬間やphase peakと同一視しない。実ru_maxrssのunit、VmRSS/VmHWM/VmSize、設定RLIMIT_ASと各limit、単調経過秒、現在phase、完全node/edge/zero-edge/Ref数、最大fan-in/一行、各index実bytes/cache resident上限/hit/miss/flush、主scanと追加位置読取/parse bytes、未完frame又はslotとlive handle/support、欠測nullを区別する。所有していない全parent metadataのobject overheadを架空の数値で埋めない。main memory failure時は既存sampleと外側receiptへ退避できるようにする。

新selftestは本番のappend/read/cache/EOF/到達/参照数/型と算術の通常入口を通す。小cacheで複数page/eviction、同じ八opの全bytes・node seal・mod54、反復/零/正/負power、Ref alias、非unit Actを照合する。固定した旧自系の短い通常helper又は事前に固定した具体byte anchorとの比較であり、新helper同士だけの自己一致を旧順序保存とは呼ばない。Dは全11slot/typed row/printed/direct/physicalにも到達する。旧自系sourceを小対照のためだけに動的ロードするなら、その全path/bytes/SHA/必要closureを新実行票に列挙し、rootの新workflowでstage/pinするまで実行しない。P系のhelperはD対照に流用しない。

future/negative ID、stride/count/EOF/短縮hash、repeated edge/uses、未到達node、zero edge欠落、異なるsource/scope、部分index、scratch包含/symlink、oversized line、未形成出力を通常helperで拒否又は資源停止させる。小fixtureでlower page/line/disk枠を実際に発火させた場合は、本登録の数学宇宙の実行と分けて記帳する。sourceの格は静的、実selftestはGHA後、本語は全P/D・全入力before/afterと工房CV-9後に別判定。A0/grade2/COMMON/cofinal/fake/Ihara/verifiedを先取りしない。
