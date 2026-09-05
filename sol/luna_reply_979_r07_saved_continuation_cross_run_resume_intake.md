# Task979 — 保存32段から別runnerへ移して累積cap64で再開する設計

凍結producer971を変更せず、保存output全体を新runnerの作業用outputへ複製して `--resume --max-appends 64` を呼べる。追加の数値adapterは不要である。必要な変更はversioned workflowの入力認証・移送・上限・保存receiptであり、元rank1386のstartや32段の既存snapshotを書き換える作業ではない。ただしTask977の修理Cによる保存32段completion成功と、その実candidate pinは本便では未観測である。

Task979全文、凍結reply971、source971の入場/fixed/restore/attach/loop/CLI、元workflow、Task977全文を読んだ。C v2担当から通常CLI・payloadを維持する公開契約の回答を受けた。C算術sourceは読んでいない。変更は本返信だけ。ローカル数値/Python/import/AST/GAP、network/git/credential、新agent、workflow実装・実行はない。

## F1. 現在観測できる入力と、同じでなければならない値

rootが認証した失敗diagはrun33984832010/1、launch `b8c9e95ddd0183d9e43b7fcc961cb251fdaea13e`、artifact9975236748、name `d972-r07-complete-oracle-cegar-continuation-v1-diagnostics-33984832010-1`、ZIP101830254 bytes / SHA256 `09ffef9d13e21e27fe9733bf997ec875a5795b5af56c7f4875e36725924d7a35`。実読取先は `%TEMP%/shadow-atelier-cegar-run33984832010-diagnostics-a1`。

PowerShellのfile/dir列挙ではoutputは2584 files・420 dirs・346710509 bytes、hidden名は0、snapshotsは000000..000031、stepsは000001..000032、invocationsは2件だった。これは数値再生ではない。全output不変はrootの認証と実preservation receiptの範囲であり、本便が全2584fileを再hashしたとの表示はしない。次の小entryは実bytes/SHAを独立に読んだ。

| file | bytes | SHA256（全file bytes） |
|---|---:|---|
| `output/HEAD` | 964 | `d489c06d40f1b06a8924558e8f751d08cd2b40259790de398b93c79f3657760b` |
| `output/owner.json` | 8612 | `e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b` |
| `output/source.json` | 2423 | `c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651` |
| `output/start.json` | 54707 | `87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b` |
| `output/fixed/manifest.json` | 3159 | `3ec178df5c2af9de7c55bb96075bb9e741111a241f7e02222ef5604587c87c41` |
| `output/result.json` | 28577 | `06c3053808179dd7706eb85fd30df8e1c360b5ee7f4640cd2a84581fe33a978a` |
| `output/steps/000032/manifest.json` | 2355 | `b9732d0bdef2cd39f3b498f7da9297ec18022a8fa40e6fe3fc83ef61483dc3bf` |
| original `source-receipt.json` | 3643 | `3a50dd12025079a6089d15aac79573899e49692b61a53879adb9b0572342de6b` |
| `producer-output-before-checker.json` | 388720 | `34dea1aedc61673d6e4d44fc553490e00555673d00c03cad31fe0afb65accc0a` |
| `preservation-result.json` | 388721 | `bf1c0d9b0b1fbce83a91329ddbe2de20055c4a54835f639b800133afe893e524` |

実HEADはcompleted32/rank1418/gen8123/Separator、current snapshot/checkpointはともにnull。state headは`0c2451e45fb1859f1ebe9f3fcbada1caefffb9f9c9adb222521cd556c3cdc2dd`、targetは`cbe44dbec2f40a06f90636f6ae66d3d24c4002f44b4358b642376da3c9eee139`、lambdaは`ecac50df38ce180d220b64e24ce5f53b163d65c3c54c7372c4b36e6ddc82e04b`。producer terminal/statusはUNKNOWN_CAP。旧checker-resultは1533 bytes / `ee5c936026da8ee228bf2d278eeb77c5a8e2c052ec3097271cf8c01871a8fb9f`、FAIL/candidate=false、`HEAD_entire_replayed_prefix_and_cursor`である。checked_cursor32をPASSとして使わない。

別runner再開に必要な一致は次のとおり。

| 層 | 不変条件 / 変えてよいもの |
|---|---|
| P source | `d972_r07_complete_oracle_cegar_continuation_v1.py` 126940 bytes / `67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c`、同じretained8 modulesとraw3data。元19source rosterもそのまま保存する |
| P runtime | 実`sys.version`の全文 **`3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]`**、NumPy **`2.5.1`**。単なる3.13系一致では足りない |
| owner | formula/scope、外部Eのowner/layout、oracle owner、P1/Task554/Task712親、Task712 manifest、word/relator辞書が同一 |
| source.json | producer/module/data hashes、上記runtime文字列、元oracle・外部Eのsource/checker/completion来歴まで全bytes同一。新C v2や新GHA launchをここへ挿入しない |
| start.json | 外部E後の**rank1386/gen8091/completed0**、親33件、元lambda/target、accepted parent layouts、DERIVED identity。rank1418/completed32へ再基準化しない |
| fixed | 同じ16 payload・manifest・owner/source・geometry親・canonical index・basis/12blob descriptors・mod54全8059 pairs。snapshotごとのq等をfixedへ混入しない |
| before HEAD | 上の実file hashと全字段、last step32、current null、owner/source/start/fixed hashが一致。新HEADは同じ不変4hashを保って正当に進む |
| invocations | 既存2fileは全bytes不変。新UUID/timeの1fileを追加し、`resume:true,completed_steps_before:32,head_before_sha256:<上のHEAD全bytes hash>,max_appends:64,max_seconds:5400`を保存する。結果はそのfile hashを`invocation_sha256`で指す |

根拠は[971:`loop_source`:875](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L875)、`loop_owner/loop_start/head_value`、[971:`run_actual`:1688](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L1688)。入場時にowner/source/startの**保存bytesと再生成canonical bytesを比較**する。Python build文字列が異なる場合はsource.jsonを整形して通さず、同じruntimeを用意できるまで停止する。元workflowもPython3.13.15/NumPy2.5.1を指定しているので、次workflowはそれを維持しGHAで全文一致を先に確認する。

Pは現在の`GITHUB_RUN_ID/GITHUB_RUN_ATTEMPT/GITHUB_SHA`を読まない。source971にあるlaunch joinは**固定された外部E親のrun receipt**とのjoinであり、新しい実行のlaunchではない。新GHAのrun/commit/workflow/runtime・新C v2 sourceは新workflowのrun/source receiptへ分離する。ローカルroot pathは親解決時に組み直せる。`FixedBundle`は保存segmentからrootを除き、同じTask554親の新絶対pathへ戻すため、runner tempの文字列一致は不要（[971:695](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L695)）。

## F2. 保存32段の再開で実際に走る処理

PのCLI上限64は既存の許容範囲内であり、32は既定値にすぎない（[971:1934](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L1934)）。`cap_reached(completed, limit)`とloopが比較するのは当outputの累積数。別runnerで「あと64行」へ読み替えない。

1. `boot`は元14親からrank1386の同じ起点を再構成する。旧base/delta/packet/旧26段/外部Eは認証済みrowとmetadataを薄くattachする。原oracleや外部Eの再生成・旧挿入除去を呼ぶ経路ではない。親認証、配列復号、既存lambdaとrow/targetの直接照合は残る。
2. `FixedBundle`は既存`fixed/`を読むので、5 bodyからの`e.basis_segments`再生成枝へ入らない。geometry/carry全bytesと親の一致、basis/ref/mod54の型、P1 instructions全file hash、12blob読者の再open/認証、source contextの構成は実行する。I/Oなし・算術なしとは呼ばない。
3. [971:`load_prefix`:1572](../search/d972_r07_complete_oracle_cegar_continuation_v1.py#L1572)がstep1..32に対しsnapshot0..31を順に読む。各snapshotの全9phaseのexact roster/bytes/hash/seal/EOFとcheckpointを認証し、`restore_snapshot`から`restore_section/cochain/tree/raw/source/primal/corrected/B/physical`へ進む。step manifestを再構成して一致させ、`attach_step`→`attach_e_delta`でnormalized row・target・lambda・DERIVED親を追加する。
4. この復元では保存配列のzero/support、order、components hash、alpha/event、raw Refのtree path、current witness、scalar receiptsの型・一致を検査する。`attach_e_delta`は保存normalized行とtargetを復号し、lead1/既存lead零・rank/gen+1・plain target・rolling headを検査する。**完成32段のq/P1 contraction/cochain/tree計算、raw Fox、primal消去、P1 lift減算、四B適用、physical除去をbuilderとして再実行しない**。`restore_raw`はtyped SLPを戻すだけでraw streamを再Fox評価しない。source/primal等のflagを新計算の実行数と読み替えない。
5. 全32attach後の`check_state_separator`は、現在lambdaを保存された**全1418物理rowと直前/現target**へ直接測る。これは実測であって、保存dot receiptを読むだけではない。旧33件起点から最終65件となるDERIVED親列、HEAD、last step hashも一致させる。各過去Eの数値生成を再演したこととは区別する。
6. 実HEADにはcurrent snapshotがなく、`snapshots/000032`もない。最初の新処理はcurrent rank1418のsnapshot32を新設し、そのlambdaで全four q/8059/54433/2のoracleを計算することである。非零なら同snapshotのE、零なら既存terminal分岐に従う。次のstep数やrankを本便で決めない。

一般の中断再開も既存規則を保つ。現在snapshot内で完成済みphaseはtyped loaderで再利用、未完phaseだけbuilderを実行する。tree完成後のoracle top metadataは同じbytesから補完できる。HEADより先にdurable physicalと全9phaseがあれば、同snapshot/先行chainを認証してstep manifest→HEADを回復し、Eを再生成しない。これはPの正当なresume動作であり、入力を読むだけのTask974 consumerとは違う。明示pendingを完成と数えず、遠いnumbered tailや任意orphanを合格扱いしない。

## F3. 次workflowの入力・移送・保存gate

元14artifactのexact tupleの正本は凍結[workflow v1](../.github/workflows/d972-r07-complete-oracle-cegar-continuation-v1.yml)のenvである。実fileは61275 bytes / `9f751fe1ea21d16b7758f9832d2dd091b73f0796128ceea505c8975031c096c1`。run/attempt/head/workflow/name/repositoryと以下のZIP pinをそのまま引き継ぎ、別runのlatest artifactへ解決し直さない。

| role / env | artifact ID | ZIP bytes | ZIP SHA256 |
|---|---:|---:|---|
| P1 | 9931437113 | 641518300 | `6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c` |
| Task554 prepare | 9865061266 | 204360988 | `da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4` |
| Task554 block0 | 9865238399 | 81729645 | `2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838` |
| Task554 block1 | 9865242284 | 82259824 | `849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb` |
| Task554 block2 | 9865193269 | 82200189 | `d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d` |
| Task554 block3 | 9865239848 | 82266526 | `87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92` |
| Task712 | 9915928157 | 22404961 | `abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858` |
| base separator | 9944214057 | 107195261 | `2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017` |
| seed30 | 9963533999 | 915410 | `f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6` |
| seed34 | 9966542166 | 984053 | `a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc` |
| fixed packet | 9969090590 | 1855391 | `b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428` |
| old26 refinement completion | 9971466432 | 51943596 | `0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8` |
| oracle completion | 9972829869 | 2299772 | `1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d` |
| external E | 9973974150 | 2816692 | `884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25` |

15番目は**今後観測するTask977 completion成功candidate**である。そのrun/attempt/head/workflow/id/name/ZIP bytes/SHA/expiry、成功checker-result、repair source、completion/preservation、新snapshot-isolation試験receiptのexact pinsは未定。空のままfail closedとし、失敗diag9975236748を成功親として代入しない。新completionの全outputがF1の32段保存outputと同じ全file/dir/bytesであることをcompletion receiptへjoinする。completionが別故障を出した場合、この次runを発火する条件は成立しない。

転送は次の三つを分ける。

- 元14親は新runnerのreadonly parent rootsへ展開し、同じ実payload/manifestを用いる。各live APIでrepository/head_repository・run/attempt/head/path・artifact id/name/size/digest/expiryを認証する。Task554のaccepted failureは役割付きの従来条件を維持し、一律successへ変えない。各ZIPの実size/SHAとsafe path、内側manifest/EOFを認証する。現在のローカルmetadata読取を次runnerの認証済み扱いにしない。
- 新completion candidateも独立したreadonly rootへ完全展開する。元P output、元19source/raw3 receipt、元失敗C、新成功C/repair/completion receiptsを原名・全bytesで保存する。new checker-resultをPのsource.jsonへ混ぜない。
- その`output/`だけを、どの親とも包含関係のない別mutable outputへ**全file/dir・hiddenを含めて**複製する。`fixed/snapshots/steps/invocations`をまとめて移す。`output/*`のようにhiddenを落とす選別や、32行だけの抽出をしない。複製前後の相対path/file-size/SHA/dir rosterが完全一致するreceiptをP起動前に保存する。receipt自体はstrict output rootの外へ置く。

今回の元32prefixはhiddenなし・currentなしなので、既存不変集合を明確に固定できる。owner/source/start、fixed全部、snapshots0..31全部（全phase/telemetry/checkpointを含む）、steps1..32全部、既存invocations2件は前後全bytes同一でなければならない。root HEAD/resultは更新可能なので旧bytesを外部のbefore receiptへ退避して保持する。新しいsnapshot/step/invocationは追加のみ。一般のresource-stop/rejected/明示pendingは診断として完全保存し、何を不変prefixと数えたかを別listにする。隠しfileを新artifact uploadで失わないよう`include-hidden-files:true`を維持する。

元19sourceとraw3はF1のsource-receiptで認証する。次実行はそれに凍結C v2を追加した**20 source**を新receiptで認証する。C v1は元runの来歴として残し、C v2へ上書きしない。C担当の公開回答でも、v2はv1を算術importせず通常CLIを維持する計画である。原19とnew20の区別をPの`output/source.json`に持ち込まない。

## F4. 最小workflow差分と観測可能な完了条件

新workflowは元の14親取得/source gateを引き継ぎ、(i) completion candidate認証・全output複製、(ii) before32 preservation、(iii) P一回のcross-run resume、(iv) C v2一回の全prefix照合、(v) provenance/preservation/uploadへ替える。初回cap1と同job内cap32の二本は実行しない。次回の枠案はP内5400秒/外100分、C内10800秒/外190分、job330分/7GiB。これは停止上限であって完走時間・追加数の予測ではない。

GHA上の本番呼出しは次の形で足りる。`PARENTS`は同じ14root array、`OUTPUT_ROOT`は全bytes複製したmutable rootであり、belowは提案で本便では実行していない。

```bash
timeout --kill-after=60s 100m python -B search/d972_r07_complete_oracle_cegar_continuation_v1.py \
  "${PARENTS[@]}" --output "$OUTPUT_ROOT" --resume --max-appends 64 --max-seconds 5400
timeout --kill-after=60s 190m python -B search/check_d972_r07_complete_oracle_cegar_continuation_v2.py \
  "${PARENTS[@]}" --candidate-root "$OUTPUT_ROOT" --output "$CHECKER_RESULT" --max-seconds 10800
```

必須gateは次のとおり。

1. **before**: completionの成功・旧output不変・C v2最終pinを確認したうえで、複製HEADがF1の実hash、completed32/rank1418/gen8123/Separator/UNKNOWN_CAP/current nullであることを確認する。root startは1386/8091/0のまま、owner/source/start/fixed hashはF1と同じ。新runtime文字列とsource20/raw3はP起動前に確認する。GHAでsource AST/bytes gateを行う場合も対象20を明示する。
2. **P invocation**: 新invocationは一件、before count32、before HEAD全file hash、resume=true、cap64、内5400。stdoutとroot resultの全bytesを比較し、結果の`invocation_sha256`でこの一件を選ぶ。UUIDやlatest時刻から選ばない。旧invocationsはimmutableのまま。
3. **after**: `32 <= after.completed_steps <= 64`、root HEAD/resultのcount・rank・generation・state/target/lambda hashesが一致。`rank=start.rank+completed_steps`、`generation=start.generation+completed_steps`、`new_physical_appends=completed_steps`、external_e_attached=1、旧32prefix不変。after33以降のstepは既存last step32へ連結する。current snapshotがあればその番号はafter.completed_steps。future scalar列やrank上限到達を成功条件に加えない。
4. **terminal**: ordinary UNKNOWN_CAP/UNKNOWN_RESOURCE/二candidateは元Pの型どおり扱う。UNKNOWN_CAPなら上限に到達した事実を確認し、COMPLETE_ZEROには同current oracle完成receipt、LINEAR_MEMBERSHIPには実target零/lambdaなし・positive pendingを要求する。P入場前resource停止はexit3のdiagnosticだけで、旧resultを新成功結果と称さない。wrapper timeout/REJECTEDも保存し、ゼロやPASSへ変換しない。
5. **C v2**: 担当の公開回答では同じ14親＋candidate-rootでrank1386の元startから全committed countまで再生でき、64用の新adapterは不要。`--max-seconds`既定10800、PASS exit0 / FAIL1 / UNKNOWN_RESOURCE3、stdout=report、schemaはv1 payloadを保つ。修理のsnapshot隔離regression・32段completion PASSは親として認証し、未観測の間はこの説明を実走成功の主張にしない。
6. **全照合**: 新Cは33段目以降だけへ短縮せず、保存旧32＋今回追加分＋current checkpointを同じ通常経路で独立再生する。`status=PASS`、`prefix_steps_replayed=completed_steps=physical_appends`、全new arrays/JSON/current checkpoint比較、全four/8059/54433/2/96776/mod54/four-B条件と、HEAD/result/terminal/invocation完全一致を維持する。Cの修理hashは新receiptへ記録し、元失敗Cのhashと区別する。
7. **保存**: P後に全output file/dir/hidden rosterを固定し、C前後で一切不変を確認する。元14親・completion readonly root・元19source/raw3も不変、新C sourceも固定。新run receiptにはoriginal launch、accepted completion tuple、current launch/workflow、P固定source、新C source、runtime、before/after HEADとcount、今回追加数`after−32`、枠、actual_resume、preservation hashesを別々に保存する。完全C PASSだけcandidate、失敗/資源停止は全outputとreceipts/log/codeをalways diagnosticsへ保存する。

新completionで既存oracle v2 full四件、P/C interface三群・metadata五件、および修理専用試験の実PASSがpin付きで揃ったなら、同じ成功suiteを毎回再走する条件は追加しない。cross-runで今回新たに観測すべきものはruntime/入力の一致、実before32からのresume、元prefixの不変、修理Cによるafter全prefixの完全照合である。

修理対象はCのimmutable metadata境界であり、P ownerを新sourceに合わせる変更ではない。現32段はまだ候補、completion/CV9の結果は未観測。cap64に達すること、target零、完全oracle零、今後の速度・収束・grade2決着を予測しない。Task974/975のsame-word positive gates、既存source/P1/Conn/共有TCBの限定、full A0との区別はそのまま残る。

判定は `INTAKE_COMPLETE; FROZEN_P_CROSS_RUN_RESUME_SUPPORTED; NEW_WORKFLOW_ONLY; C_V2_COMPLETION_AND_EXACT_PARENT_PIN_PENDING; NO_NEW_ARITHMETIC_ADAPTER_REQUIRED; GRADE2_NOT_DECIDED; verified=false`。

AUDIT_979_VERDICT:
