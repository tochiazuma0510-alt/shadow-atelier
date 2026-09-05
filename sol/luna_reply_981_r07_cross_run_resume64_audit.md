# Task981 — 別runner・同owner・累積cap64継続の限定監査

最終判定は**限定静的PASS、必須修正なし**。実成功completionの十entryと保存prefixを照合し、最終workflowの変更が親定数八行だけであることを確認した。F1–F9は親pin受領前の記録、F10–F12がその残件を更新する。新resume64のGHA結果と工房CV9はまだ未観測である。

F1. **進行中。** Task978を16809 B / `b143d586a38ad926418f3c702e31d0245919f3e5865b5a47ef6147da5375ecb5`で最終freezeしrootへ通知した後、Task980/981、reply979、最終reply977/978、completion workflow/schemaを全文読了して本票を開始した。変更は本票だけ。公刊978/971/C v1・v2/既存workflowは不変。ローカルはsource静的読取、JSON metadata、bytes/SHAだけとし、数値/Python/import/AST/GAP、network/git/credential、追加agentは使わない。v220・release・GHAはrootが担当する。

F2. **親とsourceの区別。** Task977成功completionのrun/artifact/entry pinsとその実PASSは、着手時未観測である。既観測diag9975236748のP32/rank1418/gen8123は候補、旧Cは最終HEAD比較FAIL、正式受理起点はrank1386/gen8091のまま。新resume64 workflowでは成功親と旧failureを混同せず、未入力のcompletion tuple/entry tableを先頭で拒否する。新Cの最終sourceは129557 B / `e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3`、元Pは126940 B / `67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c`。今回は両算術を変更せず、別runnerでの移送・同一runtime/owner/source/start/fixed・実resume・不変prefix・全after再生を監査する。

F3. **先行読了block。** `.github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml` の冒頭からP実resume一回および直後receiptの入口までを読んだ。元14親＋成功completionの15 live tupleはTask554だけfailureとする。全15 ZIPの実bytes/SHA・path/重複/symlink/type/暗号化を認証して安全展開し、expiryもliveで確認する。元19 source＋C v2の20 source/3rawと旧receiptの順序を固定し、Python全文 `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]` / NumPy2.5.1を起動前に一致させる。旧Pのsource.jsonへ新launchやC pinを混入しない。

成功親の新C全32段・完全HEAD・過去snapshot/hash・source/runtime/旧FAIL/新PASS・旧output不変・既走4/3/3/5/5/3試験receiptを結ぶ入口を読み、元14親の実全rostersと成功completion全体を新baseline化する設計を確認した。旧suite再走は0。成功親はreadonlyとし、その全output2584 files/420 directories/346710509 Bを、どの親とも包含関係のない別mutable outputへhidden含めcopyして全roster/bytes一致を要求する。旧HEAD/resultは外へ退避、残2582旧filesと全旧dirs、invocations二件を不変集合にする。Pは通常CLIで一回だけ `--resume --max-appends 64 --max-seconds 5400`、外100分／7 GiB。exit0とstdout=新root resultを要求し、入場前exit3から旧resultを新成功へ読み替えない。後半の新invocation/停止型/全after checker/always保存の完成読了と、最終親pinを待つ。

F4. **構造全体の限定静的判定は必須修正なし。** F3以降、完成workflowの全1224行を末尾のcandidate/always uploadまで読了し、最終追加のcoverage 10-entryと旧新C実bytes joinも読んだ。構造完成時の実fileは93007 B / SHA256 `a4e01ee0284c7efc4e138df9f57e7ae7b222dab60bf93efa72410d5817d16d70`、LF1224/CR0/BOMなし/final LFである。reply980の構造完成稿（9939 B / `540496cf6844bcf99c846d2ede91a775fb62ec25eb2ad2846ab0ae1419ab3745`）も全文読了した。このhashは未来の親pinを埋める前の境界であり、公刊launch用の最終freezeとは分ける。rootの通知ではcompletion run33988391926/1は19:53:35ZからC全32段を照合中で、成功親の実結果はまだ本票に供給されていない。

F5. **一回resumeと停止型。** P直後のgateは旧2582 files・420 directories・二invocationと退避HEAD/resultの全bytesを再確認し、新しい第三invocationの全file hashをresultの明示`invocation_sha256`で選ぶ。P971:1730–1738の`uuid.uuid4().hex`によるfilename、C v2:1412以降の同じ32桁hex規則、実旧二件のfilenameを別々に読んで一致を確認した。新invocationはbefore32/実旧HEAD/resume=true/cap64/内5400秒、既存二件は不変である。afterの累積countは32以上64以下、rank=1386+count、generation=8091+count、今回追加数はcount−32とする。P入場前exit3や外timeoutから残存旧resultを新成功へ読み替える道はない。

UNKNOWN_CAPは累積64、UNKNOWN_RESOURCEは未完という型を維持し、current snapshot/checkpointの有無・同じstate/target/lambda・新invocationを結ぶ。COMPLETE_ZERO_CANDIDATEには同current oracleの完成を、LINEAR_MEMBERSHIP_CANDIDATEにはlambdaなし・実target零とTASK958_PENDINGを要求し、どちらもgrade2判定にはしない。durable phaseがHEADより先にある場合の扱いは凍結P/Cの通常経路を保ち、wrapperで消したり完成数へ勝手に足したりしない。今回新しいsource・数値adapter・regression・旧suite再走を追加すべき根拠は、この新境界の静的読取では見つからない。

F6. **旧32段の全辞書一致は別runnerでも成立する型である。** C v2の通常`replay_head_prefix`はrank1386の起点から全committed countを再生し、末尾にcurrent checkpointがあればそのsnapshotを一件追加する。`.steps`には再生したstep/manifest/state/rank/generation/scalars/raw長/alpha supportだけ、`.snapshots`にはsnapshot/phase/oracle hashes、ordinary27 anchor、保存producer telemetryが入る。O v2:270–292の`source_scores`が返すanchorは固定27基底・monomial列・expansion/momentsのhashで、新checkerの時刻を含まない。C v2:804–822の`compare_phase`は保存telemetryのbegun/ended/elapsedを読んで有限性・差・payload bytes・EOFを再認証し、その保存値から同じdocumentを返す。したがってworkflow:1146–1147の旧`.steps[:32]`/`.snapshots[:32]`全dict一致gateは、新runnerのelapsed差を誤って比較するものではない。

C v2:1412–1445のinvocation返値も`sha256`が全file bytesのhashで、残りは全unsigned字段であることを実sourceから確認した。旧二件の全dictを新C返値に要求し、新第三件の明示hash・before32・旧HEAD・累積cap64を結ぶgateと整合する。過去snapshot隔離修理を弱めたり、旧32段をcheckerで省略したりしない。

F7. **全after-prefixと保存gate。** Cは同じ14親とmutable candidate-rootから通常CLIを一回だけ実行し、内10800秒/外190分/job330分/7 GiBで旧32＋今回追加分＋current checkpointを照合する。全四scope/8059/54433/二aux/96776/mod54/four-B、全新arrays/JSON/HEAD/terminal/invocation、exit0/stdout=report、累積countと全physical append数を保持した。stepごとのtarget.scalarとselected_scalarは実physical/resultへjoinし、current snapshotはちょうどcount番、committed snapshotは全九phaseとoracle manifestを実hashへjoinする。cap上限は資源枠であり、追加数・収束・所要時間の予測ではない。

P後に全output rosterを確定し、always側でC前後の全output、旧prefix、全15readonly親、source20/raw3、保存された実source copyと旧/new workflowの不変を照合する。旧14巨大親のpayloadを今回artifactへ重複uploadする要件はなく、live tupleと全file/dir/hash roster・通常CLIの親認証を保持する。成功completion全体はreport内に保存し、mutable outputとは相互非包含である。candidateは全C PASS・preservation PASSと最終run receipt join後だけ、alwaysはfailure/UNKNOWN/途中HEAD/明示hidden tail/元親来歴/旧FAILと新PASS/旧新C実bytes/全実行source/log/receiptを30日保存する。

F8. **最終metadata追加と限界。** completion入口の厳密十件rosterはchecker-result、repair-source-receipt、completion-run-receipt、completion-intake-receipt、preserved-input、preservation-result、all-parent-files-before/after、snapshot-isolation-selftest、coverage-receiptである。coverageには全32保存current lambdaだけというscope、四character順、C result hash、source再計算0・P再走0・作用素恒等零/全四informative/cross_checked/verifiedの各falseを要求する。旧新C二fileはcompletion/preservation内の同じrosterと実bytes/SHAを認証する。元failure artifactとsuccess completionの来歴、元19sourceと新20source、元P・修理C・今回launchは別字段である。

このworkflowは過去のF-fo-1/F-sc-1/F-cy-4aを含む継承TCBや第三系統の独立性を遡及閉鎖しない。保存qの零を作用素恒等零、選択例のcoverageを全rootの情報性としない。Task2145で閉じたoracle v2 full四件は実receipt認証だけで再走せず、same-word positive読出し・Conn/source-map/P1の数学上の境界も維持する。

F9. **残件は観測された成功親のpin差分と新runtime。** rootが実回収した成功completion tuple/ZIP全bytes/SHAと上記十entryを供給した後、その実小JSON/layout/hash、source/runtime/全32 PASS/不変output/旧新由来を照合して、空欄を埋めた最終workflowのbytes/SHAを改めて凍結する。それまでは現入口が起動拒否するのが正しい。現段階は構造静的PASSであり、run33988391926の成功、rank1418の正式受理、次resume64の結果・新rank・完全零・grade2/A0・CV9・verifiedを宣言しない。rootへこの限定判定を通知した。公刊978・既存source/workflow・v220は本agentでは変更していない。

F10. **成功completionの実親pin受領・一致。** rootの手渡し`%TEMP%/shadow-atelier-audit163/cegar-completion-run33988391926-a1-pins.json`は3153 B / `ff00dc2f1bf8d66776b5aea940c0de1c8281fbafd5e0cd313f870decf744ad64`。全文読み、同JSONの`local_root`である`%TEMP%/shadow-atelier-cegar-completion-run33988391926-candidate-a1`から下記十entryをすべて独立にbytes/SHA照合した。欠品・相違・reparse pointはない。

実親はrun **33988391926/1**、launch **`22b628c0145d7d369a310179a64b88662f360b24`**、workflow `.github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml`、artifact **9976060093**、name `d972-r07-complete-oracle-cegar-checker-completion-v1-candidate-33988391926-1`。ZIPは**102582146 B / `9f51b03805ca9de08669111e7aeb3acfc8169ff31cee4d27f1383c52bf5c96b1`**で、全ZIP bytes照合・安全展開・live successのbroker作業はrootの実通知による。本agentはネットへ接続せず、回収後の実entryと保存bytesを独立に読んだ。

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

F11. **実parent layoutと保存32段の決定性を照合。** completion-run、completion-intake、repair-source、snapshot-isolation-selftestは全文読了し、checker-resultはscope・全terminal/identity/runtime字段・steps/snapshots/invocationsの各metadataを読んだ。新Cは実status PASS/exit0、stdoutとresult全file SHA一致、全32 steps/32 snapshots、8059/54433/二aux/96776/mod54/四Bと全arrays/JSON/HEAD gateの各成功字段を持つ。terminalはUNKNOWN_CAP、rank1418/gen8123/Separator、current snapshot/checkpoint/oracle terminalはnull。現在のrank1418 lambdaに新しい完全oracle零を測ったとの記録ではない。旧Cは別fileで従来のFAIL/exit1/同じHEAD理由を保持している。新snapshot-isolation三件も実PASSで、旧alias control検出を含む。これを新第三系統の独立性とは称さない。

preserved-inputの**全2636実files**を本agentも一件ずつsize/SHAへ照合し、すべて一致した。内訳のoutputは**2584 files/420 directories/346710509 B**で、実全file/dir rosterも完全一致した。source20本/raw3およびartifactに保存されたC v1/v2二本も全実bytes/SHA一致。元19sourceと末尾追加C v2、元P runtimeと新C runtime、旧launchとcompletion launchを実receiptで区別した。Python全文とNumPy2.5.1はF3の固定値に一致する。元14親全rosterのbefore/afterは同じ168585 B/hashであり、ローカルの新14親算術再走とはしない。

さらにCの全32 snapshotを、それぞれの実start/oracle-manifest file hashへ、全32 stepsを実step manifestおよび内側physical resultのstate/target.scalar/selected_scalarへjoinした。九phase×32=**288組**についてmanifestの実file hashと保存producer telemetryの字段がC receiptに一致した。ordinary27 anchorは全32で同じ固定metadata、旧二invocationも各実fileの全SHAと全unsigned字段に一致した。したがってF6の保存32辞書がrunner依存の新checker時刻を含まないという静的根拠は、今回の実保存layoutにも合う。新runnerでの再生結果そのものは次GHAで全dict一致を要求する。

coverageも実32行・四character順・C result hash・同じtarget scalar列・三規約表と各false限定を読んだ。packed配列の復号やq/kappa/scoreの再計算は行っていない。coverageから作用素恒等零、全四character情報性、次iteration数・速度・収束を推論しない。

F12. **最終workflow差分とfreeze。** root保存の`%TEMP%/shadow-atelier-audit163/resume64-workflow-before-actual-pins.yml`を実読取し、93007 B / `a4e01ee0284c7efc4e138df9f57e7ae7b222dab60bf93efa72410d5817d16d70`がF4の全文監査版に一致することを確認した。新workflowと全行を比較したところ、変更は**125–127、129–132、134行の八定数行だけ**。run/attempt/head/artifact id/name/ZIP bytes/digest/十entry JSONがF10の実値に一致し、実行body・runtime/source・cap・旧32辞書比較・current checkpoint・全after-prefix・保存gateには変更がない。reply980の最終追記F5も読み、最終票12733 B / `2f0b65286dc224cef7c5d4113402aa039144854127336c5347b14fa9bb8546ca`の境界表示と整合する。

最終workflow `.github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml` は**94428 B / SHA256 `293b7b7dcb914414a235b31c3c014d552a229dc759a854d37bfc481e52e9550d`**、LF1224/CR0/BOMなし/final LF。凍結Pは126940/`67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c`、C v2は129557/`e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3`で実hash不変である。この限定source/workflow監査に追加必須修正はなく、F9の親pin待ちは解消した。

残るのはrootによる次resume64 GHAの実AST/runtime/入場/移送/一回resume/全after-prefixと不変保存、および工房CV9である。新target零・完全oracle零・次rank・当該grade/A0を本票から宣言しない。工房格が未到着の時点では、従前受理rank1386と全32実PASS後の候補rank1418を分ける。元のF-fo-1/F-sc-1/F-cy-4a等の継承限界、same-word positive/side/localizationの別gateも保持する。変更は指定返信981だけで、公刊978・既存source/workflow・v220を本agentは変更していない。rootへ最終限定PASSを通知する。

AUDIT_981_VERDICT: PASS_LIMITED_STATIC_FINAL_WORKFLOW_AND_OBSERVED_PARENT_PIN_DELTA; TEN_ENTRIES_AND_ALL_2636_PRESERVED_FILES_MATCH; SAVED32_SNAPSHOT_AND_INVOCATION_METADATA_JOINED; SAME_FROZEN_P_CUMULATIVE_CAP64_AND_FULL_AFTER_C_REQUIRED; NEW_RESUME64_RUNTIME_AND_CV9_PENDING; GRADE2_AND_A0_NOT_DECIDED; verified=false.
