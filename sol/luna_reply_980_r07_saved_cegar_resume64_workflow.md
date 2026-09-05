# Task980 — 保存32段から同ownerで累積cap64へ再開するworkflow

新workflowの構造・入場gate・再開・全prefix照合・保存、および成功completionの実artifact/10-entry pin接続まで完成した。Task980と公刊reply979を全文読み、指定の新workflowと本返信だけを編集した。producer971・公刊source/返信・既存workflowは不変。ローカルPython/import/AST/数値/GAP、network/git/credential、新agent、checker算術の読取・共有は行っていない。新workflow内のPython/ASTと数値CLIはrootが今後GHAで実行するコードであり、本便で実行したものではない。

## F1. 先行保存した境界

新workflowは `.github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml`、markerは `[r07-complete-oracle-cegar-resume64-v1-run]`、workflow_dispatchも受ける。元14親tupleは公刊continuation-v1から維持した。15番目のTask977成功completionのrun/attempt/head/id/name/ZIP bytes/SHAと、成功receiptの10-entry pinはF5の実手渡し後にだけ設定した。最初のstepのmissing拒否は残している。失敗diag33984832010/1・artifact9975236748を成功親へ代入しない。

15親のlive APIによるrepository/head_repository/run/attempt/head/workflow/conclusion/name/id/size/digest/expiry照合と、実ZIP size/SHA・安全展開を実装した。Task554の5artifactだけaccepted failureを維持する。ZIPの絶対path/親越境/重複/非正規path/symlink/非regular/encrypted entryを拒否する。元14親とcompletionを互いに包含しないrootへ解決し、各payload rootの全file/dir/bytesを認証してreadonlyにする。GH_TOKENはこのAPI stepのprocess環境だけ、checkoutのcredential永続化はfalseである。

Task977/978から最終freeze通知を受領したC v2は **129557 bytes / SHA256 `e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3`** で固定した。元Pは **126940 / `67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c`**、元C v1は **120245 / `8c000f9b49d04447a09c701daf5907a35b7f2e883f1e36747308a6d4ded29b1f`** のまま。元19本/raw3のsource receipt全bytesを再現して3643/`3a50dd12025079a6089d15aac79573899e49692b61a53879adb9b0572342de6b`へ一致させ、新Cだけ末尾に加えた20本を別 `resume-source-receipt.json` に書く。ASTはGHA上のこの20本だけ。全20本と元/新workflowの実sourceもartifactへ残す。

## F2. 成功completionを消費するmetadata境界

実値を接続した `COMPLETION_ENTRY_PINS` は次の正確な10-key辞書で、各値は `{"bytes":整数,"sha256":"64桁の小文字hex"}`。空辞書、別roster、欠品、違う実bytesを拒否する。

| receipt | join |
|---|---|
| `checker-result.json` | 新Cの全32段・current null・HEAD/result/owner/source/start/fixed・scope・runtime・通常PASS/exit0 |
| `repair-source-receipt.json` | 元19＋新Cの20本/raw3、元source hash、実completion launch |
| `completion-run-receipt.json` | original/repair launch、元FAIL、新PASS、全保存inputとoutput、再走0の明示 |
| `completion-intake-receipt.json` | 元失敗artifactの実tuple・58entry・source/intake/preservation hash |
| `preserved-input.json` | 元output2584fileと非output52fileを再構成し、全2636file/421dirへ一致 |
| `preservation-result.json` | 全旧bytes・全14親・source・copied receiptsの不変、errors空 |
| `all-parent-files-before.json` / `all-parent-files-after.json` | 同じ元14親全payloadを今回runnerでも再hashし、完全roster一致 |
| `snapshot-isolation-selftest.json` | 新3件の実PASS・実PhysicalState/serializer・旧alias control検出・exit0/stdout一致 |
| `coverage-receipt.json` | 32個の保存current lambdaだけのcoverage、scalar列・four-character順・checker hash、作用素恒等零を主張しない |

coverageはTask977最終metadata追加に合わせ9→10entryへ増やした。新算術を追加したものではない。completionが保持する `checker-sources/` の旧v1/新v2も、実file bytes/SHAをsource receipt・completion/preservationの `checker_source_files` と一致させる。元失敗CのFAIL/exit1はそのまま保持し、checked_cursor32をPASSへ読み替えない。

旧oracle v2 full4、P `.groups` 3群/C `.tests` 3件、両metadata拒否5件と修理snapshot3件は、成功親の実receipt/hash/結果を認証するだけで再走0。新C担当から、通常Cの `.steps/.snapshots` は同じ保存prefixなら安定metadataで全dict比較できること、invocationの返値sha256はseal内hashでなく全file hashであること、partial current snapshotは末尾1件・完成phase prefixだけであることを公開ABIとして確認した。算術helperは読んでいない。

## F3. コピー・一回resume・全after-prefix照合

同じP971を一回だけ `--resume --max-appends 64 --max-seconds 5400` で呼び、before32からの累積上限とする。外100分、全after-prefix C v2は内10800秒/外190分、job330分/7GiB。Python3.13.15の実build文字列とNumPy2.5.1、原19本＋新C v2の20 source/raw3を認証する。元32段のbuilder再生成0と、復号・型・保存row/現在lambda直接測定を区別する。

元output2584 files/420 dirs/346710509 bytesを `accepted-completion` のreadonly親から別のmutable `output/`へ全複製する。glob `output/*` を使わずhiddenも含め、全file size/SHAとdir rosterを複製前後で一致させる。元親のreadonly modeをcopyが引き継ぐため、copy側だけatomic publicationに必要な書込modeへ戻す。file内容は変えない。reportはstrict outputの外である。

before HEAD全file hashは `d489c06d40f1b06a8924558e8f751d08cd2b40259790de398b93c79f3657760b`、32/rank1418/gen8123/Separator/current nullを要求する。startはrank1386/gen8091/completed0を維持。root HEAD/resultの旧bytesを `before32/` へ残し、残る2582fileと420dir、旧invocation2件は全bytes不変とする。元32snapshotを新startへ改名しない。

Pは一回のみ。exit0とstdout=result全bytes一致を通した後、追加invocationが正確に一件で、その全file hashを新resultの `invocation_sha256` が指し、`resume=true, completed_steps_before=32, head_before_sha256=<実beforeHEAD>, max_appends=64, max_seconds=5400`であることを要求する。新UUID/timeのlatest選択は使わない。入場前exit3、wrapper timeout、REJECTEDは新成功結果へ変換しない。

afterは32≤count≤64、rank=1386+count、generation=8091+count、今回追加はcount−32とする。UNKNOWN_CAPならcount64、UNKNOWN_RESOURCEは未完の型を維持する。COMPLETE_ZEROは同current oracle/current lambdaと結び、LINEAR_MEMBERSHIPは実target零/lambdaなし・TASK958_PENDINGを要求する。いずれもgrade2/full-A0決着へ昇格しない。

C v2は同じ14親＋mutable candidate-rootだけを通常CLIへ渡し、保存32＋新追加分＋current checkpointを全再生する。scope8059/54433/2/96776/mod54/four-B、全arrays/JSON/HEAD/checkpoint/terminal/invocation比較、累積prefix count一致、旧32 `.steps/.snapshots` とcompletionの全dict一致を求める。今回追加数とCが全再生した累積数を混同しない。

## F4. 保存と残る実走gate

P後の全output rosterをC前に保存する。always stepは全15readonly親、20 source/raw3と保存source copy、元32prefix/invocations、C前後全outputの不変を比較し、失敗時もerrorsを含むreceiptを先に残す。`run-receipt.json` は全C PASSと保存PASS後だけ作る。original launch/source、completion launch/repair source、current launch/new sourceを別字段に持ち、before/after HEAD/count・追加count−32・actual resume・新invocation hash・各保存receipt hash・上限・実elapsedを記録する。

成功candidateは全gate後のみ。always diagnosticsはreport全体をretention30日/hidden込みで残す。mutable全outputに加え、受理completion全体（元output・元52receipt/log・旧FAIL・新PASS・旧/新C実bytes）、今回全code/exit code/log/API metadata/receiptsを含む。元14の巨大payloadはlive artifact tupleと全file/dir/hash rosterで結び、数値CLIの固定親認証を通す。

静的なsource/公開ABI/実metadata読取とfile bytes/SHA・LF/CR/BOM/final LF/行末空白だけを確認した。ローカルAST/YAML parser、数値CLI、ネットワーク、GHAは実行していない。root/Task981はpin前の全1,224行を読了し必須修正なし。F5のpin差分の最終静的監査と、その後のGHA上20source AST/runtime/metadata/実resume/全prefix照合が残る。新regression・数値adapterは追加していない。

構造完成時のworkflowは **93007 bytes / SHA256 `a4e01ee0284c7efc4e138df9f57e7ae7b222dab60bf93efa72410d5817d16d70`** だった。成功親pin接続後の最終workflowは **94428 bytes / SHA256 `293b7b7dcb914414a235b31c3c014d552a229dc759a854d37bfc481e52e9550d`**、LF1224/CR0/BOMなし/final LF/行末空白0である。実行済みを意味しない。

未知のterminal・rank・反復数・速度を予測しない。Task974/975のsame-word positive gates、Conn/source-map/P1 canonical lifts/Task554/Task712と既存共有TCB、現lambdaについての零と作用素の恒等零の区別、candidate/cross-checked/verifiedの序列を維持する。Task977 completionの全32段PASSは実観測された。工房CV9は本freeze時点で未受領なので、受理rank1386・候補rank1418の区別を維持する。resume64の実走結果は未観測である。

## F5. 実completion親の最終接続とfreeze

rootが回収した手渡しは `%TEMP%/shadow-atelier-audit163/cegar-completion-run33988391926-a1-pins.json`、展開rootは `%TEMP%/shadow-atelier-cegar-completion-run33988391926-candidate-a1`。実runは **33988391926/1**、launch **`22b628c0145d7d369a310179a64b88662f360b24`**、workflow `.github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml`、artifact **9976060093**、name `d972-r07-complete-oracle-cegar-checker-completion-v1-candidate-33988391926-1`。ZIP **102582146 bytes / SHA256 `9f51b03805ca9de08669111e7aeb3acfc8169ff31cee4d27f1383c52bf5c96b1`** はrootが実ZIPへ照合済みである。本workerは次の10実entryの全bytes/SHAをそれぞれ独立に読み、手渡しとの全一致を確認した。

| entry | bytes | SHA256 |
|---|---:|---|
| checker-result.json | 176622 | `4ef33b2d174064e2542dd07d1c838b476b549606a8be0fb2ecc4b301b1382690` |
| repair-source-receipt.json | 4137 | `3f2c68a359c3b9200f88850432372abd78207c1cfacc39a8aeb371e184774be8` |
| completion-run-receipt.json | 5006 | `aaa5a9900d37f9d56e72419d7073da0bec291890e6ccf940109d01168e6e77f8` |
| completion-intake-receipt.json | 2218 | `f209153368adeb384ec94bcbd4d4f63d34c4dd175e6cc1ad50926116780f590b` |
| preserved-input.json | 811910 | `914405978f9ad745e822e7009963a3da06f079af1bc6a6ef301119a1fa9a11ff` |
| preservation-result.json | 389295 | `b1d465bd1af7174d1177ea9f78ee79c29d15bf1cb6f7c239b3efd6f802e53d98` |
| all-parent-files-before.json | 168585 | `e370577d4bb30baf9d611cd13f08b392d1f4505b9810d8eaad78a9992e6ac113` |
| all-parent-files-after.json | 168585 | `e370577d4bb30baf9d611cd13f08b392d1f4505b9810d8eaad78a9992e6ac113` |
| snapshot-isolation-selftest.json | 727 | `ac5c37d865ee8f85dc13ddbb78878071b7d6d6abbec827827190ccedc83337c0` |
| coverage-receipt.json | 86586 | `e0ee8b681793567e422da95a6d73475ffc8e2c8b06e6d491938218336b6d7bad` |

実completion/PASS receiptから、32 steps/32 snapshots/旧invocation2件、rank1418/gen8123、同HEAD/result/source/owner/start/fixed、terminal UNKNOWN_CAP、current snapshot/checkpoint null、旧P再走0・C1回・新snapshot試験3件PASSを読んだ。実CとPのruntime全文は同じPython3.13.15 build / NumPy2.5.1。保存output2584 files/420 dirs/346710509 bytesはcompletion receiptとrootの全件hash照合通知に一致する。本workerが旧算術を再実行したものではない。

rootが保存したpin前workflowと最終workflowを行比較し、変更は **125–127、129–132、134行の定数8行だけ**であることを確認した。実行body・cap・roster・source・schema・旧32比較・保存gateの変更はない。新pinと最終bytes/SHAをTask981/rootへ渡す。このfreeze後の実GHA、CV9、次prefixの正負結論はrootの観測に委ねる。

判定: `WORKFLOW_COMPLETE_AND_OBSERVED_PARENT_PINS_CONNECTED; MISSING_PINS_REFUSED; SAME_FROZEN_P_ABSOLUTE_CAP64; FULL_AFTER_PREFIX_C_REQUIRED; CV9_AND_RESUME64_RUNTIME_PENDING; NO_LOCAL_RUNTIME; GRADE2_NOT_DECIDED; verified=false`。

AUDIT_980_VERDICT:
