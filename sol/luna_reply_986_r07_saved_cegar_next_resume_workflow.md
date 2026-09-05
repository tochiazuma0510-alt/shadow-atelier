# Task986 — 観測済み保存候補から同ownerを再開するdriver

F1. **workflowを完成した。算術sourceは不変、初回は実64段から累積上限128へ再開する登録である。** Task983をsource176579 B / `a9e72980f3594842b5a7a4abaaf610b49a5d9202779ab1132c53c6bd4225ec98`、返信11544 B / `2973013374e246e5af537fa3fab9b61d6500b15132cc08b05c58dde7bd3695ff`で凍結してからTask986を全文読了した。凍結980 workflow全1224行、reply975/976/979/981全文と対話帳末尾を読み、変更を本workflowと本返信に限定した。新producer算術は読取/import/共有していない。ローカルはsource静的読取とJSON/file/bytes/SHA metadataのみで、Python/import/AST/数値/GAP/network/git/credential/追加agentは使っていない。

最終workflowは `.github/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml`、**109035 B / SHA256 `7050a882297d8304693c63fef2fcaa0e4910d8b5c3d9f09f2288dd6648668fd1`**、LF1324/CR0/BOMなし/final LF。rootはこの全稿を読了し追加必須指摘なしと通知した。Task987の最終監査票、新登録run、新dispatch、八件metadata canary、今回のP/C/coverageは本票凍結時点で未実行・未観測である。以下の実64は**親runの結果**であり、新runの成功ではない。

F2. **二つの起動を分けた。** rootの後着指示により、exact作業branch `sol/r07-explicit-lift-20260825` と本workflow pathだけのpush eventを追加した。push時は `register-only` jobの `true` 一個だけ、checkout/親download/source試験/数値実行は0。本数値jobは `workflow_dispatch` かつ同branchだけで、checkoutは明示 `ref: ${{ github.sha }}` / persist-credentials=false。rootが登録runを観測してから実入力をdispatchする。Task985の同一語consumerとCV9格付けは再開の起動前件にしない。親がCOMPLETE_ZERO_CANDIDATE/LINEAR_MEMBERSHIP_CANDIDATEならこのdriverの入場を拒否し、976/975・983の別経路へ渡す。

F3. **公開入力のexact schema。** dispatch inputは必須string二つ、`observed_parent` と `max_appends`、defaultなし。固定env `OBSERVED_PARENT` / `MAX_APPENDS_INPUT`で渡し、shell/script本文へ入力値を式展開しない。`max_appends` は正規表現 `[1-9][0-9]*` の文字列、値Mは `n < M <= 48384-1386 = 46998`。bool/float/負値/空値/cap resetは拒否。nは既存completion以降の実累積countで32以上。JSONはduplicate key、NaN/Infinity、余分なtop字段を拒否する。外側JSONの空白やkey順は自由で、値を保存したcanonical JSONはsorted/compact/ASCII＋LFである。

| `observed_parent` のexact九top字段 | 型・契約 |
|---|---|
| `schema` | literal `d972.r07.complete-oracle-cegar-resume-next.v1.observed-parent` |
| `repository_id` | ordinary integer 1312092366 |
| `branch` | literal `sol/r07-explicit-lift-20260825` |
| `artifact` | exact八字段 `{run,attempt,head,workflow,id,name,bytes,sha256}`。run/attempt/id/bytesは正のordinary integer、headはlowercase40hex、sha256は`sha256:`＋lowercase64hex |
| `entries` | sorted unique配列、最大256件。各要素のexact字段は`{file,bytes,sha256}`。fileはcanonical相対POSIX名、bytesは非負ordinary integer、sha256はprefixなし64hex。順序は大小文字を区別するASCII/ordinal順 |
| `snapshot` | 下記exact18字段。count/rank/genはordinary integer、rank=1386+n/gen=8091+n、kind=Separator、terminalはUNKNOWN_CAP又はUNKNOWN_RESOURCEだけ |
| `full_head` | 実`output/HEAD`の全sealed JSON object。canonical全file SHAをsnapshotへ結び、inner sealと全state字段を別に照合 |
| `invocations` | file順の通常UUID全件。各要素exact `{file,bytes,sha256,value}`。fileはoutput相対`invocations/<32hex>.json`、valueは実fileの**inner seal込み全JSON**。外側sha256は実file全bytesのhash |
| `output` | exact `{files,directories,bytes}`、すべて正のordinary integer。実output全rosterのfile数/dir数/byte総数 |

snapshotのexact字段は、`completed_steps, rank, generation, kind, state_head, target_remainder_sha256, lambda_sha256, owner_sha256, source_sha256, start_sha256, fixed_manifest_sha256, current_snapshot_sha256, current_checkpoint_sha256, last_step_manifest_sha256, terminal, head_sha256, result_sha256, checker_result_sha256`。hashはprefixなしlowercase64hexで、current snapshot/checkpointだけ同時nullを許す。HEAD/result/Cの同名字段・全file hashと実比較する。resultの旧invocation pointerを時刻やUUID順から推定しない。full sealed invocationのfloat `max_seconds:5400.0/1800.0` は保存fileどおりの型を保持する。C返値の`sha256`は既に全file hashへ置換されているため、その返値をvalueのinner sealに流用しない。

親workflowの許可列は次の三つだけ。candidate名はそれぞれworkflow basenameから `.yml` を除き、`-candidate-<run>-<attempt>` を続けた実名に完全一致させる。

- `.github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml`
- `.github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml`
- `.github/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml`

entriesの共通必須集合は `output/HEAD, output/result.json, output/owner.json, output/source.json, output/start.json, output/fixed/manifest.json, checker-result.json, checker-stdout.json, checker-exit-code.txt, producer-result.json, source-receipt.json, producer-output-before-checker.json, preservation-result.json, all-parent-files-before.json, all-parent-files-after.json` の15件。世代ごとの追加必須集合は以下。追加の実pinも全て認証するが、欠けた必須fileを任意追加fileで代用しない。

| 親世代 | 共通15件への追加必須files |
|---|---|
| completion-v1 | `repair-source-receipt.json, completion-run-receipt.json, completion-intake-receipt.json, preserved-input.json, snapshot-isolation-selftest.json, coverage-receipt.json` |
| resume64-v1 | `resume-source-receipt.json, run-receipt.json, completion-intake-receipt.json, copy-before-resume.json, live-parent-intake.json` |
| resume-next-v1 | `resume-source-receipt.json, run-receipt.json, parent-intake-receipt.json, copy-before-resume.json, live-parent-intake.json, observed-parent.json, dispatch-input.json, coverage-receipt.json` |

F4. **初回の実観測接続。** rootからrun33990567016/1のsuccessを受領した。head `c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70`、workflow resume64-v1、artifact9977040548、name `d972-r07-complete-oracle-cegar-resume64-v1-candidate-33990567016-1`、ZIP **304642285 B / `a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792`**。実rootは `%TEMP%/shadow-atelier-cegar-resume64-run33990567016-candidate-a1`。HEAD/result/Cは**64段/rank1450/gen8155/Separator/UNKNOWN_CAP、全C64 PASS**。rankの工房格付けとGHA結果は別であり、この親metadataから当該gradeを決めない。

手渡しv2 `%TEMP%/shadow-atelier-audit163/cegar-resume64-run33990567016-a1-pins-v2.json` は **21846 B / `e43fbed422a7a9a9a453955f0edf84baec89eef5d49f42b8094b62797c8e7a06`**。全30実entryを一件ずつbytes/SHAへ独立照合し、すべて一致した。実HEAD、sealed三invocation、C/resultの該当字段、source/runtime、small phase/raw descriptorsも読んだ。rootは全5145 output/836 dirs/686612253 B、nested completion全2699 files、旧不変2582 files・旧C32全dictとsource20/raw3/WFのmetadata認証PASSを通知した。本agentがこの全巨大outputを数値再生したとの表示はしない。

| 初回実identity | 全file SHA256 |
|---|---|
| HEAD 964 B | `4614d5c3fc619007879f3a5062cde90ac0cab86552ddd17ff14306bc961ac2f4` |
| result 42785 B / producer stdout同bytes | `75f76ac43c86cfae998b0f4fe757a79b500727c2bfa847849fa57dbfa05293fd` |
| C result/stdout 各330955 B | `ff55c51e90acead643b9683af6f82d492c503a92c83a504a97eeb3f62c31cc4d` |
| state head | `076c4b9df33957b090a7bf698e4dd1100e85350cfff86f88eb9ab12a39fdb667` |
| target remainder | `3bba0da3f619eab5f78e715beabd22d9c7975b36f72d28ee8d7528d9d0f4648a` |
| lambda | `7c0dbe475f9b162f4648f5468ee1098eb86b43dbee247d71f811076559ab88fe` |

rootはこの実handbackから初回JSONを作成した。最初の版にPowerShell既定の大小文字を無視したsortが混じり、output/fixedがoutput/HEADより前だったため、ordinal順への限定修正を依頼した。修正版を実readし、exact九top/18snapshot、全30entry ordinal順、full HEAD、invocationのoutput/除去とinner seal、output.directories、実n64<M128を確認した。値を変えてschemaを通す修理ではない。

- 観測JSON `%TEMP%/shadow-atelier-audit163/cegar-resume-next-observed-parent-33990567016-a1-v2.json` = **9277 B / `0c399fa08909b4b70a29bba5912ab3bc034b30165c65c90f12dd52fc0a8c1652`**。
- 再現用REST body `%TEMP%/shadow-atelier-audit163/cegar-resume-next-dispatch-parent33990567016-cap128-v2.json` = **10005 B / `f05381734554cfc8a8dd205c70480bb732de6e92aae936c5e78b0bdb6aca6dc5`**。

REST bodyのexact外側形は `{"ref":"sol/r07-explicit-lift-20260825","inputs":{"observed_parent":<上の実JSONを文字列として入れた値>,"max_appends":"128"}}`。実bodyでは観測file末尾のCRLF二byteだけを除いた9275文字が入力値で、それ以外は完全一致することを実比較した。これは公開parserの許容範囲で、float型も変えていない。実再現は**root brokerが登録run成功を観測した後だけ**次の既存bodyを送信する。本agentは実行していない。

```powershell
$task986Body = Join-Path $env:TEMP 'shadow-atelier-audit163/cegar-resume-next-dispatch-parent33990567016-cap128-v2.json'
gh api --method POST repos/tochiazuma0510-alt/shadow-atelier/actions/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml/dispatches --input "$task986Body"
```

F5. **入場・移送・一回resumeの閉鎖。** 元14tuple/source表は980から保持した。15番目だけ実JSON指定の直前candidateで、callerのsuccess文字列を信用せず、live run/attempt/head/workflow/conclusion・repository/head_repository ID・同branch、artifact id/name/bytes/digest/expiry、全ZIP実hash/type/path/EOFをGHAで認証する。Task554のaccepted failureを一律successへ変更しない。旧COMPLETION_*定数は実観測済み32段の歴史anchorで、直前親や未来成功のdefaultではない。

直前candidateはexact `accepted-parent/` 全体、元14巨大親は別roots。nested resume64の`accepted-completion/`、将来resume-nextの`accepted-parent/`を過去runの全files/dirs baselineへ結び、元completionの固定十pin・32全C・元2636保存file・旧FAIL/新PASS・既走4/3/3/5/5/3試験receiptへ到達する。歴史階層をlive成功として再発行せず、元失敗run33984832010の来歴を分けた。元14の実payload全rosterは各世代と同じでなければならない。

同sourceはP **126940 B / `67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c`**、C v2 **129557 B / `e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3`**。元19に修理Cを追加した20本とraw3の全pinを保持。Python全文 **`3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]`** / NumPy **2.5.1** を一致させる。新workflowのmetadata driverはGHA上で本YAMLから `driver.py` として保存し、独立のhash字段に載せた。20本という数は凍結算術/import closureであり、このinline由来metadata driverを隠した数ではない。

元startは1386/8091/count0、owner/source/start/fixedは全bytes固定。全outputをどの親とも包含しない別mutable outputへ全file/dir/hiddenごとcopyし、一致を確認。`before/HEAD`・`before/result.json`を退避、残る全旧file/dirを不変とする。通常UUIDのinvocationだけをC件数へ結び、凍結Cが明示許容する `.UUID.json.pending-UUID` はその件数から除くが、全file保存には残す。旧phase/checkpoint/明示pendingを削除して再開しない。

Pを一回 `--resume --max-appends "$ABSOLUTE_CAP" --max-seconds 5400`、外100分/7GiBで起動する。新result=stdout・exit0・明示invocation SHA・新UUID一件・before n/HEAD・同owner/source/runtime・実capを結ぶ。afterはn以上M以下、rank=1386+count/gen=8091+count、今回追加数count−n。UNKNOWN_CAP/RESOURCE/二candidateの型を保持し、入場前exit3やtimeoutから旧resultを新成功へ転用しない。完全零は同current oracle、Linearは実target全zero/lambda null/positive pendingを要求する。到達数・時間・収束は予測しない。

F6. **全C・保存・coverage。** 同じ14親とmutable outputを通常C v2で起点から一回、内10800秒/外190分/job330分へ渡す。8059/54433/二aux/96776/四B・全array/JSON/HEAD/current checkpoint・全steps/snapshots/invocationsを保持し、新Cのsteps[:n]とsnapshots[:n]を親Cの全committed dictへ一致させる。親にcurrent snapshotが一件あれば、その同一startと既完了phase/oracleも保存hashへ結ぶ。旧suite再走は0。新八canaryは実観測JSONを通すmetadata拒否のみで、bool-count/wrong-rank/wrong-workflow/missing-checker-entry/nonresumable-terminal/path-traversal/reset-cap/noninteger-capを対象にする。

GHAのfull C PASS後だけ、既照合manifest/shape/全bytes/EOFへ束縛した保存q/κ/score/auxを読む。全snapshot-before-appendと現在snapshotの完了phaseだけを記帳し、未完phaseはnull＝未測定である。四character順、κのd0/d1タグと共有aux8、現在q零、lambda supportの座標とtrit、failed_chord/五basisの保存value/residual/tau/fit、rawの**修理前w omega**と普通指数pair、central signed exponent全列、word_boundと選定nodeのSLP length/修理指数を保存する。legality.omegaは修理後の別字段。最終HEADのlambda supportも別 `lambda_final` へ実最後のpacked file/HEAD hashと四列を記録し、current snapshot=nullでも漏らさない。Linearはtyped NOT_APPLICABLE/null。作用素恒等零・全四informative・第三独立算術・raw再演・新裁定は主張しない。

alwaysで全15readonly rootsとnested来歴、全旧prefix、P後/C前後output、20source/raw3、旧/新WFの実copy、driver、入力raw/canonical JSONを全file/dir/SHA比較する。不足はINCOMPLETE、差はFAIL、Cの算術statusとは別に保存。最終run receiptは新launch/実親/原失敗launch、source/runtime、before/after/旧C全dict、新一件invocation、実elapsedと全保存・coverage hashesを結び、全gate成功時だけcandidateを30日uploadする。always artifactは全output/未完/hidden/pending/元親/入力/旧新source code/WF/log/exitを同じく30日残す。元14巨大payloadをartifactに再格納しない。次のresume-nextも同exact入力型と保存形を消費できる。

F7. **残る境界。** 本票はdriver静的完成と実親metadata接続であり、新八canary/登録/本番GHA/CV9の成功ではない。修理Cの数値関数、九phase、derived元rho2、P1/Task554/Task712/Conn/source-mapの前提、F-fo-1/F-sc-1/F-cy-4a等の保持TCBは変えていない。完全零の負候補は976、同一語positiveは975/983の境界を保ち、MEMBER/NONMEMBER/fullA0/side/localization/無限cofinal/Lean verifiedを本run receiptから宣言しない。全新出力はcandidate=true/cross_checked=false/verified=falseである。正式工房rankと実候補rankも分ける。rootへのrelease/実run ID・commitの記帳はroot返書に委ね、本agentは公刊ファイルを追加変更しない。

AUDIT_986_VERDICT:
