# Task1023 返信 — 同じ固定lambdaからの k64 新version登録設計

## F1. 判定と読了境界

k64 は、凍結 k32 producer の通常算術を保持し、選定上限とその保存・受付の上限を新 v2 に揃える移行で設計できる。変更の中心は登録値・新source来歴・選定候補数であり、新しい数式、TCB、親、反復方針を足す必要はない。本票は静的設計の完了であり、新 P/C/WF の実装認可・source freeze・実成功を意味しない。

指示書 `sol/luna_task_1023_r07_fixed_lambda_k64_registration_design.md` を全文読了した。実ファイルは 4,173 B / SHA256 `fe01ac4229699d3e7367e9bc3b149fa7f86585ffa822e38fbd8dcb1d37e6744d`。Task994 C1–C10、公開 Task997 / 1000 / 1001 / 1002 / 1003 / 1004 / 1011、および root 返信163 F8.88–89 の実 k32 結果・2173 ack を読んだ。Task997 の原案と R1 が違う箇所は R1、以後の追加契約はその exact 列挙を優先した。

再読した自系 producer は `search/d972_r07_fixed_lambda_cycle_batch_v1.py`。全file実pinは **213,861 B / SHA256 `229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591`** で一致した。定数・登録・thin anchor・選定/保存reader・候補loop・checkpoint・final・resume・診断・selftest/CLIの関係を本文と `rg` の全 `32` 出現から調べた。以下の行番号はこの凍結 v1 を指す。保持する自系九sourceは F9 の全file bytes/SHAをmetadataで再照合した。

相手 C のsource・私的返信を読んでいない。ローカル Python/import/AST/数値/GAP、network、git、GHA、credential、追加agentは使用していない。変更は本返信だけであり、P4/1016/1022、P994、旧公開資料を変更していない。

## F2. 親・数学・選定宇宙の登録

親は旧 continuation の実 **run33990567016/1、64段/rank1450/gen8155** に固定する。head `c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70`、artifact `9977040548`、ZIP `304642285 B / a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792`。元14親とこの continuation の15 role順、全artifact tuple、全files/directories、旧history/receipt bytes、実 C64 全prefix、元runtime、ANCHOR_ENTRY_FILES等の凍結pin表を維持する。v1で認証した親の既存schemaは改名しない。

新 k64 はこの親から fresh 一batchを作る。実 k32/run34004423047 の結果を初期状態に取り込まず、control96へ親を差し替えず、v1 の途中/完成packetから resume しない。新 v2 自身が中断した場合だけ、同 v2 source/runtime/登録/portable identity の保存成果から再開できる。k128は別便の事前登録が必要であり、本票には含めない。

登録は次の exact 値とする案を採る。

| 字段 | v2登録 |
|---|---|
| schema prefix | `d972.r07.fixed-lambda-cycle-batch.v2` |
| batch_size | 普通整数 `64` |
| max_batches | 普通整数 `1` |
| selection_policy | `CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX` |
| partial_policy | `PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY` |
| refill | boolean `false` |
| producer_limits | `{max_seconds:5400,max_memory_mib:7168}`、両値は普通整数 |
| checker_limits | `{max_seconds:10800,max_memory_mib:7168}`、両値は普通整数 |

全54433弦と2 auxを同じ selection lambda で走査する。非零弦数を m とすると、m>0では既定弦順の先頭 min(64,m) 件を選ぶ。m=0では最初の非零auxを一件だけ選び、両auxも零なら COMPLETE_ZERO_CANDIDATE。failed-indices/failed-edges と残差表は全m件/全54433件を保持し、選択上限64で走査や表を打ち切らない。依存候補が出ても65番目を補充せず、target零以降の選定済み尾部は SKIPPED_AFTER_LINEAR のまま記録する。

選択宇宙の変更は、同じ固定lambdaで materialize 対象となり得る失敗弦の上限を32から64へ広げる点である。全弦・全aux・全four-character・全8059 P1・source lower96776・physical lower32260・physical48384の検査範囲は同じ。六cycleの順序、零係数のcycle/power/Ref、普通整数signed-word、mod54、primal消去、全四B、候補ごとのE、挿入順の全係数とliteral ancestryを保持する。選択scalarと依存判定、数値target更新の負号、literal correctionの正号を変えない。

thin anchorは全旧historyのbytes認証と旧1450行の直接pairingを続ける。previous_targetは元 continuation `output/start.json` の実target、current targetは旧64 HEADの実targetであり、相互に代用しない。同lambdaの両target dotと全旧row dot、旧97親からのrho2 DERIVEDを保つ。新採用rowだけを順序付き派生親へ足し、依存/未処理候補を派生rowへ昇格しない。

同じ全表とlambdaに対して v1/v2 の選定index・scalar・六cycleの先頭 min(32,m) が同じ条件を満たすことは、規則からの必要条件である。新実payloadの一致を観測したという主張ではない。schema/owner/source/selection_start/selectionが変わるため、外側witness・manifest・instruction・state-head等の全bytes/hashは比較対象の型を分ける必要がある。旧32と新64の状態を合算しない。

## F3. 通常sourceの最小差分表

新しい実装先の案は `search/d972_r07_fixed_lambda_cycle_batch_v2.py`、相手公開pathは `search/check_d972_r07_fixed_lambda_cycle_batch_v2.py`、WFは `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml`。本便では三pathとも作成しない。

| 凍結v1の位置 | v2で必要な差分と保持事項 |
|---|---|
| 29–49、2017、2024–2028 | 新外側SCHEMA、C_FILE、BATCH_SIZE=64、POLICY、SCOPE内batch、今回launch WORKFLOWをv2へ。MAX_BATCHES=1、FORMULA、PARTIAL_POLICY、全寸法、15 roleは維持 |
| 239–254、1027–1043 | 自己descriptorは `Path(__file__).name` により新Pへ自然に結ぶ。code.checkerは新C公開pinへ。L_FILE/L_SHA、自系九依存、相手十依存、raw三件は元のまま。新batch v1を追加TCBとしてimportしない |
| 1003–1024、1124–1165 | acceptanceは新 `.acceptance` とstrict64/1/policy/false/resources。runtime全文と全15親の全bytes/EOFは従来どおり。旧schema/policy/k/別sourceの互換受付を作らない |
| 1295–1345 | portable受付、parent-layout、source、owner、start、fixed manifest、selection-startを新source/schema/regで正直に再seal。親実lambda/target/pinsを保持し、host pathや新run/nonce/elapsedをownerへ混ぜない |
| 355–410、413–426 | `classify_batch` の `failed[:BATCH_SIZE]` とmin上限が64になる。solve/全残差計算/六cycle/aux分岐は維持。`current_batch_tree` の全走査を先頭64へ縮めない |
| 1354–1378、1521–1663 | 全mのfailed配列、固定長全表、typed EOF、witness-rosterの保存、`saved_selection_values` のmin上限、外側selection/viewの登録を64へ。保存済みtreeからの外file回復は再solveしない |
| 1773–1843、1846–1878 | 候補ordinal/row局所offsetの上限だけ64へ。reduction/decision/row保存からprivate HEADまでの順序、依存によるrow非追加とprocessed増加は維持 |
| 2038–2147 | invocationのbatch/accepted/processed上限を64へ。全旧hostからの受付hash再構成、actual launch、before HEAD/history結合、bootstrapを保つ |
| 2377–2458、2486以後の復元 | sequence上限は `3+6*BATCH_SIZE`、候補/row診断directory上限は64へ。全ordinary roster、直後一phaseだけのdurable tail、global atomic pending語法を維持 |
| 2674–2740 | selectionを一度保存し、処理済みordinalから同じ選定済み尾部だけを続ける。candidate loopが64を直接再走査せず `selection.selected_count` を使う点は維持 |
| 1882–1968、2614–2659、2822–2888 | complete/Linear/zeroだけでfinal。全selected readout、採用数とrank、separator、HEAD/resultの結合は現行generic式のまま。完成済みread-only resume、診断writer抑止、書込前path保護を保持 |
| 3339–3463 | CLIの固定値は64。新 `--selftest` はF7の新境界だけへ接続する案。終了0/資源3/FAIL1、資源宣言、信号flag、通常例外の扱いは変えない |

この変更に係数の計算法、packed codec、canonical規則、並列化、候補の同時保持、古い行の再insert、旧snapshot算術の再演、separatorの候補ごとの新規計算を混ぜない。大配列は一候補ずつ消費する既存方針を保ち、全54433×48384行列・全64候補の密な同時保持を導入しない。

全 `32` 出現を調べた結果、非定数の意味を持つ修正候補は旧canaryの次の三箇所である。2945–2953の36失敗/先頭32/末尾index36のfixtureと期待値は、新境界表へ置き換える。単に期待32だけを64へ直すと、元fixtureが36件しかないので誤りになる。3111のinvocation fixture `batch_size:32` と3244の `SimpleNamespace(batch_size=32,...)` は新値/共通BATCH_SIZEへ結ぶ。旧三群の本体を新sourceへ残す場合も、これらを古い登録値の通常fixtureとして残さない。

nonceの32 hex文字、int32/uint32/u32le、u32 sentinel4294967295、N54432・physical lower32260、hash中の32、旧artifactの `before32/HEAD` / `before32/result.json`、旧保持source/親workflowのversionは変更しない。全体の文字列置換は使えない。

## F4. 公開wireとportable identity

Task997のexact body/key/descriptor表を保ち、新外側prefixだけv2へ移す。suffixは acceptance, parent-layout, source, owner, start, fixed-manifest, selection-start, phase-manifest, phase-telemetry, tree, witness-roster, witness, selection, oracle-view, physical-literal, reduction, physical-instruction, row-manifest, candidate-manifest, checkpoint, progress-head, separator, final-manifest, head, result, invocation, resource-stop, rejected, selftest, checker-result。acceptanceは既存どおり六top-key plain canonical JSON、三key targetもplainであり、外sealを足さない。旧inner section/cochain/raw/source/primal/p1/B JSONは凍結schemaのまま実bytesへ結ぶ。

普通整数はbool/floatを拒否し、trit0..2、residue54 0..53、base3四trit/byte0..80、u32leと全EOF/paddingを保持する。Task1000のdirect pairing五key、旧fixed JSON五keyの認証後に新三keydescriptorへ射影する規則、DERIVEDの旧97親・新採用row十keyをそのまま使う。Task1003の `instruction.target_sha256` は新 `rows/<local>/target.json` plain三key全file SHAであり、packed `remainder_sha256` とは別である。

portable受付は15親の `path` だけを除き、role/artifact/全pin/固定source/raw/runtime/registrationへ結ぶ。同じv2を別rootで再受付しても同じidentityとなる。新source/schema/regに由来するhashを旧v1へ偽装しない。実hostはinvocationのexact `parents`（15 role→絶対path）/`acceptance`/`output`、実run/attemptはboolを除く正の普通整数、headは40hex、workflowは今回v2の登録pathへ結ぶ。

`selection/start.json` の全file hashを先に固定し、treeと各witnessは `selection_start_sha256` へ結ぶ。全oracle/table/選択roster後の `selection/selection.json` の全file hashを `selection_sha256` とし、oracle-view/候補phase/decisionは後者へ結ぶ。seal循環を作らない。tree descriptorの基準は `selection/tree/`、failed配列のfile値は `failed-indices.u32` / `failed-edges.u32`。witness descriptorはroot相対 `candidates/<6桁ordinal>/witness.json` のまま。

v1のacceptanceだけをv2と改名して通す経路は置かない。旧source descriptor・旧owner/start/selection/checkpoint/HEAD/resultは新期待値とschema/seal/fullfile/bindingの各段で拒否する。数学的に同じselection lambdaであることは、旧packetのownershipを新packetへ移す許可ではない。

## F5. 上限・再開・public final

ordinalとnew row local offsetは0..63、selected/processed/dependent/accepted/skippedは全selected rosterとの関係を持つ普通整数で、単独で64以下という検査だけにしない。rankは `1450+accepted_new_rows`、generationは `8155+accepted_new_rows`。64件採用やrank1514を実結果として登録しない。

private sequenceは初期0、section1、cochain2、treeと全selection metadata3、候補ordinal iの相p（raw=1からreduction=6）で `3+6*i+p`。全64件処理時の上限387は、この保存規則からの静的上限であり実到達値ではない。依存はprocessedを一つ進めてもrow/rankを進めず、targetが早く零なら残る選定済み尾部は未実行のまま記録する。

認証してadoptできる未commit成果はHEADの直後一phaseまで。phase manifest・全payload・同snapshot/binding・前phase連鎖・typed rosterを閉じ、完成builderを再呼出しせず不足metadata/HEADだけを回復する。未commit先行phaseをinvocationのbefore countへ混ぜず、before progressは実HEAD以内の歴史checkpoint、before physicalは実 `output/HEAD` の全hashへ結ぶ。Cの公開 `durable_tail` はTask1001のまま、独立比較してもPのHEAD countsを先へ進めない。

Task1011の初回invocation前停止を維持する。resume=false通常receiptは高々一件。通常receiptがfreshを持たなくても、resume=true・両before HEAD null・strict count0のbootstrapがあれば受理し、複数bootstrapも許す。通常receipt零は全progress未形成時だけ。`invocations/.<32hex>.json.pending-<32hex>` は全bytesを保存する診断であり、通常invocation数ではない。resource-stop.json/rejected.jsonは両方あれば両方のexact schema/status/terminal/全bindingを照合し、未知普通fileを許容しない。

public finalは全selected処理済み、またはLinear、または全零oracleの場合だけ。final payload/manifestのdurable化からpublic HEAD→resultの公開列へ協調停止判定を挟まない。部分 `BatchReductionState` をSeparatorやLinearへ改名しない。完成済v2の `--resume` はTask1004どおり全入力/保存/HEAD/result/来歴を再認証した後、既存result bytesをそのまま返し、新invocation/result/diagnosticを書かない。今回の受付時刻・exit・stdout同一性は外側execution receiptへ保存する。

資源途中停止はUNKNOWN_RESOURCEと実private checkpointを保持する。新lambda oracleを作って次batchへ進む処理、同outputで登録上限を32→64へ書き換える処理、partialを候補成功とする処理は無い。書込前のoutput/親/acceptance/code/raw disjoint gateと全保全も維持する。

## F6. 既実施三群の継承範囲

rootの公開返信163 F8.88では、run34004423047/1で v1 の `fixed-selection-full-roster-and-aux`、`dependent-independent-target-signs-and-packed`、`private-prefix-publication-resume-and-isolation` が実施された。Pは7+6+26拒否、Cは2+3+14拒否を含む各三群PASS/exit0として受領済みである。この事実はrootの保存結果に帰属し、本便で再実行したとは書かない。

これを旧k32のinterface実績として保持し、新k64の型/境界試験に旧三群丸ごとの再走を加えない。旧数学suite、旧64 oracle/E/insertの再計算も増やさない。新本番では同じlambdaでもselectionの全8059/54433/2と選定済み候補の全新算術を実行し、Cは全新完成payload/JSON/finalを照合する。旧三群を省略することは、この新本番範囲を省略する意味ではない。

## F7. 新しい小対照の提案

新v2の `--selftest --batch-size 64 --max-seconds 300 --max-memory-mib 7168` を新二群だけへ接続する案とする。親・actual outputを渡さないfixture経路であり、通常実装の登録/selector/保存readerへ到達させる。rootが共通v2契約で二nameを確定してから両作者へ公開する。現時点でreceiptやPASSを作っていない。

第一群の公開name案は `k64-version-registration-and-types`。本番の `authenticate_registration`、canonical/seal/schema gate、invocation/sequence/roster readerを使用する。

- 新v2・普通整数64/1・policy64・false refill・所定limitsの正対照を置く。旧 `.v1` の正しくsealされた外側文書、v2に旧policy32だけを残した文書、旧source/owner/startを持つ保存文書を拒否する。stale sealで偶然落ちるだけの対照にしない。
- batch_sizeの32/33/63/65/128、64.0、"64"、trueを拒否する。max_batchesの2/true/1.0、refillのtrue/0、資源値のbool、保存ordinalのtrueも拒否する。schemaをv2に改名した旧registrationや旧ownerでも拒否する。
- ordinary ordinal63/row63・sequence387を受ける型境界と、ordinal64/row64・sequence388の拒否を既存scope helperへ結ぶ。候補pending directoryは `candidates/000063/e/.pending-raw-<32hex>` まで、000064は拒否し、nonce自体は32hexのままとする。
- 既定の未commit一phaseルールについて、scope(386,387)を受け、(385,387)を拒否する。新k64・strict count0の小bootstrap receiptと同owner再rootのhost→全acceptance hash結合を一件通し、登録32又は旧v1の再開を拒否する。旧三群の全fixtureはここから呼ばない。

第二群の公開name案は `k64-full-roster-cutoff-and-restoration`。既存 `canary_selection_fixture` が使う全長synthetic tau/valuesと固定五basisの方式を用い、`classify_batch` → typed witness/tree/roster → `saved_selection_values` → `publish_selection` の通常経路へ接続する。実Omega/旧rank1450算術や候補Eはこの小対照で走らせない。

| 全非零弦数m | 保存failed数 | 選定witness数 | 必要な対照 |
|---|---:|---:|---|
| 32 | 32 | 32 | 旧上限で誤って早期returnしないための基準 |
| 33 | 33 | 33 | 33番目が選定される |
| 63 | 63 | 63 | 64未満の全選定 |
| 64 | 64 | 64 | 最後のordinal63が有効 |
| 65 | 65 | 64 | 第65非零弦は全表/failed配列に残り、witnessへ補充しない |

各caseで最後の非零を全弦末尾 `CHORDS-1` に置く。m≤64ではそれが選定にも含まれ、m=65では全failed表に残る65番目となる。先頭の非零には五basisへの非自明係数を持たせ、全六cycleと零係数を含める。auxを非零にしてもm>0なら弦だけを選ぶ。必要な分岐対照としてm=0/aux非零の一件と、m=0/aux両零の一件だけを添える。

新小群では、65失敗時のwitness数65への増量、先頭32で止めた保存roster、64番目のindex/typed coefficient改竄、選定尾部の入替えを、保存JSONの再seal後に通常readerへ通す。全弦末尾削除/EOF=falseは対応する通常selector入口へ渡して拒否を確認する案とする。canonical全長表の再読・descriptor/selectionのselected_countを含めて検査し、単に `min(64,m)` と同じ式を別のassertへ写すだけにしない。

新 `.selftest` のtop bodyは既存の status/tests/fixture_scope/production_interfaces_used/old_success_suites/actual_anchor_arithmetic_replayed/candidate/cross_checked/verifiedを維持する案。testsは上記二nameの `{name,status,rejected_cases}`、fixture_scopeは非空str、production_interfaces_usedとrejected_casesは非空str list。`old_success_suites=0`、`actual_anchor_arithmetic_replayed=false`、candidate/cross_checked/verified=false。新二群という件数・nameはv2登録差分としてWFにも明示し、旧三nameのPASS receiptを新sourceのreceiptとして再利用しない。

これらは未実行の試験設計である。実装時に通常入口への到達・期待拒否理由・fixtureの保全を作者票で確定し、source静的読了後にrootのGHAだけで走らせる。小群の追加を旧全suiteの自動再走へ広げない。

## F8. 実計測・比較の欄

初回枠はP内部5400秒/外側6000秒、C内部10800秒/外側11400秒、各7168 MiBのまま。新小群は各内部300秒/外側360秒。これは上限であり完走や速度の予測ではない。UNKNOWN_RESOURCE/FAILの保存と全未比較範囲の明示を維持する。新runtime実値、run id、source pin、artifact pin、countや最終rankを先取りしない。

| 計測対象 | 保存/表示する値と解釈 |
|---|---|
| selection section/cochain/tree | 各既存phaseのelapsed、telemetry descriptor、typed EOF。今回同lambdaの全selection算術として記録 |
| 候補ordinal別 raw/source/primal/p1/B/reduction | 各phaseのelapsedとpayload bytes、process_ru_maxrss_kib、proc_io_before/afterを保存。依存も実行した相を残し、Linear後未実行尾部はnull/未実行として記録 |
| final | separator構成/直接dots/公開payloadの既存final telemetry。new lambdaのoracleは含まれない |
| P全/C全 | 各プロセス内部elapsedと外側呼出しwall-clock/RUSAGEを分ける。Cが保存Pの秒を自分の計測としない |
| 進捗と採用 | selected_count / processed_candidates / dependent_candidates / accepted_new_rows / skipped_after_linear / rank / generation。率を示す場合は分子・分母を添え、処理済み0なら未定義扱い |
| 全保全 | output全files/directories/総bytes/個別hash、candidate archive実bytes/hash、全15親/受付/source/rawのbefore/after、全invocation・診断・未完tailを別に保存 |

自系 `process_measurement` / `phase_telemetry` のRSSはLinux `ru_maxrss` のプロセス累積high-waterであり、そのphaseだけのpeakや増分ではない。各phase終了時の測定値として示し、差分をphase peakと呼ばない。I/Oはrchar/wchar/read_bytes/write_bytesを前後で保存し、差分を出すときは同process/同invocation・両測定ありを条件とする。rchar/wcharと実read_bytes/write_bytesは同義でない。payload_bytesはtelemetry自身を除く出力payload量であり、入力I/Oでも全artifact量でもない。取得不可の値はnullを維持する。

比較基準の公開実k32値は、P全432.436731秒、候補六phase合計351.018215秒、primal76.402402秒 + P1 253.602052秒 =330.004454秒。約94.0135%はこの和を候補六phase合計で割った値であり、P全に対しては約76.3128%。P1単独94%とも、P全の94%とも書かない。これらはrootの実保存telemetryの読取に帰属し、本票の新計算・独立算術照合値ではない。

新k64で候補が増えたときの総時間、採用率、後半32の費用、RSS、保存bytesは実走後に分けて読む。k32の時間を二倍した数や32/32採用実績からの64/64予想を登録しない。旧rowの再insertを省いても、旧rowの読出し・全rank dots・増える新basisへの消去コストは残る。

## F9. 保持source closureと新二源への置換位置

自系保持依存は以下の九本。公開Task1002の値と現file全bytes/SHAが一致した。本文の新算術や相手の私的APIを共有する表ではない。

| file（search/相対） | bytes | SHA256 |
|---|---:|---|
| d972_r07_actual_grade2_root_scalar_batch_v2.py | 118315 | `3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856` |
| d972_r07_actual_root_seed_materializer_v3.py | 86643 | `36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332` |
| d972_r07_complete_oracle_cegar_continuation_v1.py | 126940 | `67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c` |
| d972_r07_fixed_root_packet_loop_v2.py | 84173 | `e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6` |
| d972_r07_full_origin_refinement_v1.py | 97806 | `d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa` |
| d972_r07_rank1355_root_seed_scalars_v1.py | 31578 | `973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb` |
| d972_r07_section_cochain_oracle_v1.py | 73290 | `4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb` |
| d972_r07_selected_cycle_materializer_v1.py | 88929 | `4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3` |
| d972_r07_targeted_grade2_owner_generated_join_v15.py | 126565 | `76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632` |

相手保持十本は公開Task1002のexact descriptor列を使用し、本文を読まずに維持する。rawは同Task1002の `scratchpad/a0_paper_words_v1.json`、`scratchpad/a0_v2_words.json`、`scratchpad/fuda1_a0_rmax_data.g` の三件。新二源が完成した後だけ、acceptance.code.producer/checker、自系C_FILE、source.json、WFの新source二descriptor/実file採取、全source receipt/launch結合へ新P/C全bytes/SHAを入れる。旧receiptに収載された旧batch/continuation checkerのprovenanceを消したり、旧hashを新実行sourceのhashとしたりしない。

新closureは保持Python19本＋新P/C二本＝Python21本、raw3本を含めて24fileであり、保持実行source22本とは数えない。新v1 batch sourceを計算helperに追加しない。source未知/空pinは実入場で拒否し、実runtime全文は登録済み親と実runnerに結ぶ。runtimeを緩いPython/NumPy version範囲へ広げない。

共有TCB F-flb-1の射程を継承する。保持Pの vectorized_projection_chunk と sparse_adjoint に関するroot F8.89の限定を、新k64でも独立性を再証明したと呼ばない。前者の実P1経路と、後者の保持同一性/実呼出し段階未確定という区別を保ち、両者を同じ相で新たに独立照合したとは書かない。F-fo-1も遡及閉鎖しない。

## F10. 残る確定事項と引渡し

本票の範囲では追加の数学blockerは見いだしていない。rootがv2共通表を確定する際に、F3の新三path、F4のprefix置換/旧inner維持、F7の新二群name・件数と同 `.selftest` body、全counts/sequence上限64/387を明文化する必要がある。これは未指定型を実装者が私的に補うことを避ける引渡しであり、新算術の共有要求ではない。

その後にP/Cへ独立実装を委嘱し、全source差分・実新二pin・新WFの型/実行/全保全gateを静的に読む。新小対照と本番一batch/全CをrootのGHAで実行して初めて、新k64の実選定数・処理数・依存/採用・rank・時間・保存量・照合結果が得られる。本票の最終段階は設計までで、source/WF/新canary/新算術は未実装・未実行である。

新lambda oracleは常に未計算として `new_lambda_oracle=null`、final q/P1/section/cochain/treeを追加しない。final lambda四blockのsupport/trit countsは物理48384座標の分割読取であり、新qではない。Linearの場合だけ `positive_readout=NEW_BATCH_SAME_WORD_ADAPTER_PENDING`、その他はNOT_APPLICABLE、grade2二字段はNOT_DECIDED、full_A0/cross_checked/verified=false。A0 actual0/1の既存台帳を本k64で更新せず、新A0判定を宣言しない。COMPLETE_ZEROにも、選定時の固定lambdaとその全走査という射程を保つ。

本返信以外を変更せず、旧凍結資料への追改変、実走、未来pinの作成を行っていない。最終判定は静的な登録設計の完了に限定する。

AUDIT_1023_VERDICT: K64_REGISTRATION_DESIGN_COMPLETE_STATIC_ONLY_IMPLEMENTATION_AND_RUNTIME_PENDING
