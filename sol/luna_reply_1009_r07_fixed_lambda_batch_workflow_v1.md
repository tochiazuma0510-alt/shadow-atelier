# Task1009 — 固定lambda batch初回workflow・最終凍結

## F1. 完成範囲と未観測境界

Task1009/1010、994 C1–C10、995/996、公開997/1000/1001/1002/1003/1004/1011を全文の契約として、指定の新 workflow と本返信を作成した。新P source/994返信は読取・import・コピーしていない。Task1011の別指定に従い、未公開995のmetadata/sourceと作者票だけを限定修理し、最終pinを本WFへ接続した。1006のsource/返信と既公刊workflowは不変。ローカルPython/import/AST/数値/GAP/network/Git/credentials/追加agent/dispatchは全て未実施。以下はsource/metadata静的記録であり、新GHA・新三群・新数値一致の結果ではない。

初回親は実 run33990567016/1 の64段、rank1450/gen8155/Separator/UNKNOWN_CAPに固定する。正式96段/rank1482はこの入力へ差し替えない。rootから新Pの最終bytes/SHAと公開selftest型を受領し、Task1011修理後の最終C pinとともに接続した。新Pの本文は読まず、source実bytesのsize/SHAだけを独立に一致させた。root/996はC全sourceと1011差分、root/1010はWF全1993行と全追加を読了し、追加必須指摘なしを通知した。正式静的票とrootの公開・実行判断は、新GHAの結果と分ける。

最終 workflow: `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v1.yml`、142206 B / SHA256 `8596ab900175c69cc38085c0caa0455a75dd74eb251e7eb2870a05e030490c73` / LF1993 / CR0 / BOM無 / final LF。全読了稿からの最後の変更はP/C bytes/SHAの四env literalだけで、これをメモリ内で戻すと142159 B / `d3453bb54c74f4b0b99524d1e828a1f39ccd75f5be98e59e3eec6889927222e2`に全bytes一致する。

## F2. 継承元と保持bytesの境界

- 公刊 `.github/workflows/d972-r07-complete-oracle-cegar-resume-next-v1.yml` は109035 B / `7050a882297d8304693c63fef2fcaa0e4910d8b5c3d9f09f2288dd6648668fd1`。そこから `REPOSITORY_ID`〜`E_ARCHIVE_DIGEST` の元14親 env 5332 Bを全文bytes一致で保持した。旧dispatch入力/任意cap/登録専用job/旧P実行/旧resume処理は本WFへ持ち込まない。
- 公刊 `.github/workflows/d972-r07-continuation-positive-word-readout-v3.yml` は108358 B / `04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604`。`COMPLETION_ENTRIES`〜`CONTINUATION_ENTRIES`の二pin表と受理completion tuple（8120 B）、`observe_original_start_header` / `validate_original_start_header` / `authenticate_continuation` の三metadata関数（15209 B）は全文bytes一致。これらは旧証跡を読むだけで、数値moduleをimportしない。
- 同v3の `PREPARE_BODY`〜`LOOP_CHECKER` の1862 Bは、PRIMARYのrho2 locator39 Bだけを除き1823 Bを保持した。batchの15親へ第16 rho2を追加しないためのmetadata差分で、残りは全bytes一致。
- `inventory_fields` / `validate_inventory` / `retained_inventory` / `scan` は上記v3の契約を踏まえた新コード。完全相対POSIX文字列順と比較コピーだけの旧並びadapterを保持し、casefold、全ancestor directory、型を追加確認する。ZIP/source/runtime/新acceptance/new metadata canary/exec/coverage/final/alwaysは本WFで記述した。旧workflow全体や旧算術helperを再実行するdriverではない。

以上の保持確認はPowerShell/.NETの文字列抽出・全bytes/size/SHAだけで行った。新PythonやYAML/ASTをローカル実行していない。

## F3. 実15親とsource closure

全親のrepository_idは1312092366。下表のprepare/four blocksのみ登録済みconclusion=failure、他はsuccess。live APIはrun/attempt/head/workflow、repository/head_repository、artifact id/name/bytes/digest/expiryとworkflow_runを全joinする。実64親だけは同branchも再確認する。各ZIPは下表の全bytes/SHAへ結び、casefold/duplicate/暗号化/特殊node/symlink/相対path/CRC/EOFを拒否・確認し、全entryを保持する。拡大上限は1 archive 100万entry・32 GiB、15 archive合計64 GiBで、残予算を展開前・stream中に適用する。これらは資源枠であり予測実測ではない。

| role | run/attempt | head | workflow | artifact id/name | ZIP bytes/SHA256 |
|---|---|---|---|---|---|
| state | 33891714539/1 | 7b7b9de20faaa3b8f26e331bb738b374f6f5708c | .github/workflows/d972-r07-grade2-physical-state-separator-v2.yml | 9944214057 / d972-r07-grade2-physical-state-separator-v2-candidate-33891714539-1 | 107195261 / sha256:2d91e2e94ab7eb235805eb0f7c04ff87edef3954460d686f047d8abcfa99c017 |
| delta | 33946247365/1 | 7f6dfaddf4150449e62a9b3e85def472fcb41c01 | .github/workflows/d972-r07-actual-seed30-materializer-v1.yml | 9963533999 / d972-r07-actual-seed30-materializer-v1-candidate-33946247365-1 | 915410 / sha256:f9627416f0e920fa369f6bc6bb9bffa8c6b15674c0fb7ff37bbebaf77991ace6 |
| seed34 | 33956437467/1 | b9ae78b0950b186463849c3ec874f6474f359851 | .github/workflows/d972-r07-actual-root-seed-materializer-v3.yml | 9966542166 / d972-r07-actual-root-seed-materializer-v3-candidate-33956437467-1 | 984053 / sha256:a4cb9f63a470636628d9ef02a5b5e55d90fe3b0a2c70f2012d32c9517d87defc |
| packet | 33964709359/1 | fff114c41bd8748ad0e708919fe0820335c9cce8 | .github/workflows/d972-r07-fixed-root-packet-loop-v2.yml | 9969090590 / d972-r07-fixed-root-packet-loop-v2-candidate-33964709359-1 | 1855391 / sha256:b15b07150d23a1a291fff387f23c8c13cf3ab5ada2b5f95f2a886b0bdf44a428 |
| refinement | 33971897879/1 | 64475e1dfab1537a38d1b3131971bfed5fc3071c | .github/workflows/d972-r07-full-origin-checker-completion-v1.yml | 9971466432 / d972-r07-full-origin-checker-completion-v1-candidate-33971897879-1 | 51943596 / sha256:0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8 |
| oracle | 33977701313/1 | bbce98d8f95a845f36fe89c0f507b9360792666f | .github/workflows/d972-r07-section-cochain-checker-completion-v1.yml | 9972829869 / d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1 | 2299772 / sha256:1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d |
| e | 33981657987/1 | 444c71c9e554ae8feb9c8ee54df57d3df19ed66f | .github/workflows/d972-r07-selected-cycle-materializer-v1.yml | 9973974150 / d972-r07-selected-cycle-materializer-v1-candidate-33981657987-1 | 2816692 / sha256:884c039737cae9673c9e1d871c30713456c993b97f16a557e9c8c24078537f25 |
| prepare | 33677346616/1 | 22c6dddb43d107c05e65f53ad898823ae8ebe276 | .github/workflows/d972-r07-a0-first-rung-grade1-v3.yml | 9865061266 / task554-grade1-v3-prepare-33677346616-1 | 204360988 / sha256:da8bfec6a03cac65de40ba8c4f79cde687fd2629edb3c3965fd972ecf96cc2f4 |
| block-0 | 33677346616/1 | 22c6dddb43d107c05e65f53ad898823ae8ebe276 | .github/workflows/d972-r07-a0-first-rung-grade1-v3.yml | 9865238399 / task554-grade1-v3-state-block-0-33677346616-1 | 81729645 / sha256:2a8e63a4270bf4052c7fd8763d7828fc17dd6b94c88854bacde1e94082cd5838 |
| block-1 | 33677346616/1 | 22c6dddb43d107c05e65f53ad898823ae8ebe276 | .github/workflows/d972-r07-a0-first-rung-grade1-v3.yml | 9865242284 / task554-grade1-v3-state-block-1-33677346616-1 | 82259824 / sha256:849321b79f0e3ea3c9a3f9c9dad43de2b3aaa571163456abc702476e322714fb |
| block-2 | 33677346616/1 | 22c6dddb43d107c05e65f53ad898823ae8ebe276 | .github/workflows/d972-r07-a0-first-rung-grade1-v3.yml | 9865193269 / task554-grade1-v3-state-block-2-33677346616-1 | 82200189 / sha256:d2cdf8245d58a384bebfd516135e07930fe26c21c2c1cab130dfa6c3c7f2854d |
| block-3 | 33677346616/1 | 22c6dddb43d107c05e65f53ad898823ae8ebe276 | .github/workflows/d972-r07-a0-first-rung-grade1-v3.yml | 9865239848 / task554-grade1-v3-state-block-3-33677346616-1 | 82266526 / sha256:87547101ede2fb48619a069de958c08cbb3cb0ee6c0990090234005aacd05b92 |
| p1 | 33851744070/1 | 6673eb2ea15ca6022acc2ddc5a8a204a0380172f | .github/workflows/d972-r07-canonical-p1-dag-degree2-lift-v9.yml | 9931437113 / task809-canonical-p1-degree2-lift-v9-33851744070-1 | 641518300 / sha256:6d6f2ec6eb7f1245b8e7d52645c710ecd519ae0cc442340237d1098c7fa63d5c |
| task712 | 33814194630/1 | 5ff2c5a30b604536df12acba8801828a5a7e5fe0 | .github/workflows/d972-r07-grade2-maps-v4.yml | 9915928157 / d972-r07-grade2-maps-v4-33814194630-1 | 22404961 / sha256:abedff074117bb779675021e9436c3a9973c577e247fe76a8314a2d4312ea858 |
| continuation | 33990567016/1 | c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70 | .github/workflows/d972-r07-complete-oracle-cegar-resume64-v1.yml | 9977040548 / d972-r07-complete-oracle-cegar-resume64-v1-candidate-33990567016-1 | 304642285 / sha256:a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792 |
実64のLOCAL rootは `%TEMP%/shadow-atelier-cegar-resume64-run33990567016-candidate-a1`。rootのhandback `cegar-resume64-run33990567016-a1-pins-v2.json` は21846 B / `e43fbed422a7a9a9a453955f0edf84baec89eef5d49f42b8094b62797c8e7a06`。本WFの30 literal entry全件を実file bytes/SHAへ独立再照合し、30/30一致。全ZIP/全出力の新GHA入場はまだ未実施。

新P/C二本＋保持P9/C10の21 Pythonとraw3が実closure。旧continuation C v1は歴史receiptに残るが今回の実import/AST/source実行列へ追加しない。新Pは213861 B / `229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591`。新Cは181828 B / `7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f`、最終作者票995は16495 B / `6fa69a11d6751245ed13e11b617b2463fe330eb9b60b0331f16c431e56b26c05`。保持列の正本1002は5490 B / `68f7e854f90fa9e4692bad03f09fceaabbc096fb1cd4a9e94a03c703b58b61e0`、下記exact配列を受付へ用いる。

| 列 | file | bytes | SHA256 |
|---|---|---:|---|
| P9 | search/d972_r07_actual_grade2_root_scalar_batch_v2.py | 118315 | 3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856 |
| P9 | search/d972_r07_actual_root_seed_materializer_v3.py | 86643 | 36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332 |
| P9 | search/d972_r07_complete_oracle_cegar_continuation_v1.py | 126940 | 67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c |
| P9 | search/d972_r07_fixed_root_packet_loop_v2.py | 84173 | e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6 |
| P9 | search/d972_r07_full_origin_refinement_v1.py | 97806 | d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa |
| P9 | search/d972_r07_rank1355_root_seed_scalars_v1.py | 31578 | 973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb |
| P9 | search/d972_r07_section_cochain_oracle_v1.py | 73290 | 4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb |
| P9 | search/d972_r07_selected_cycle_materializer_v1.py | 88929 | 4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3 |
| P9 | search/d972_r07_targeted_grade2_owner_generated_join_v15.py | 126565 | 76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632 |
| C10 | search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py | 119619 | e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6 |
| C10 | search/check_d972_r07_actual_root_seed_materializer_v3.py | 64626 | eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701 |
| C10 | search/check_d972_r07_complete_oracle_cegar_continuation_v2.py | 129557 | e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3 |
| C10 | search/check_d972_r07_fixed_root_packet_loop_v2.py | 66251 | 5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5 |
| C10 | search/check_d972_r07_full_origin_refinement_v1.py | 75083 | 1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2 |
| C10 | search/check_d972_r07_rank1355_root_seed_scalars_v1.py | 36236 | f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62 |
| C10 | search/check_d972_r07_section_cochain_oracle_v1.py | 80740 | 2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967 |
| C10 | search/check_d972_r07_section_cochain_oracle_v2.py | 84402 | a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d |
| C10 | search/check_d972_r07_selected_cycle_materializer_v1.py | 103757 | a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4 |
| C10 | search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py | 141770 | 8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662 |
| raw3 | scratchpad/a0_paper_words_v1.json | 115928 | 90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893 |
| raw3 | scratchpad/a0_v2_words.json | 106133 | fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612 |
| raw3 | scratchpad/fuda1_a0_rmax_data.g | 4709 | 625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba |
rawをLF/BOM規則で正規化せず元bytesで保持する。Python21本だけGHAで全pin/UTF-8・BOM無/CR0/final LF/ASTを確認する。runtimeは `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]` とNumPy `2.5.1` のexact組。sourceコピー/基準票をruntime installや親受付より前に保存し、不一致時も実観測をdiagnosticsに残す。

## F4. 受付・本走・停止の実接続

受付は997の六key plain canonical ASCII JSON+LF。15 roleは state,delta,seed34,packet,refinement,oracle,e,prepare,block-0..3,p1,task712,continuation の順。全file/dirは完全な相対POSIX文字列順とexact descriptor。旧保存inventoryのcomponent順は元bytesを変えず、全要素を保ったコピーだけ整列して比較する。

anchorは実七fileと全invocation descriptor、64 steps/64 snapshots/3 invocationsの全canonical list hash、実rank/gen/state/target/lambda/terminal。旧Cの全64 snapshotの九phase manifestと各stepを保存bytesへ結ぶ。完了32の全steps/snapshots辞書も現64の前半へ完全一致し、旧三試験票等は全pinを認証するだけで再走しない。旧start.external_e_attachedはordinary int1を要求し、旧refinement HEADに不存在target字段を補わない。新P/Cのthin loaderが元14親と旧target履歴を別途認証する。

portable identityは受付 parents.pathだけを除いた本文hash。owner/startへ新run/nonce/hostを混ぜず、実hostの受付全SHA・launchはinvocation/execution票へ置く。batch_size32/max_batches1/refill=false、二policy、P/C resourcesをexact型・値で固定する。push marker `[r07-fixed-lambda-cycle-batch-v1-run]` 又は入力なしworkflow_dispatch、作業branch限定、checkout `${{ github.sha }}`、read-only contents/actions、persist-credentials=false。source/数値job以外のroot Git/GHA操作は本作者がしない。

新metadata canaryは実validate_acceptance、inventory全string順、retained copy、strict JSON、safe_extractを呼ぶ。actual受付の陽対照に、rank/bool/count/cap/欠pin/欠file/duplicate role/byte bool/attempt bool、Path component順、duplicate file/key、nonfinite、ZIP casefold/duplicate/traversalの16拒否を接続し、小さな完全EOF ZIP陽対照も置く。これは初回GHA待ちであり、16拒否PASSを観測済みとは称さない。

P/C各selftestは公開三名 `fixed-selection-full-roster-and-aux`、`dependent-independent-target-signs-and-packed`、`private-prefix-publication-resume-and-isolation`。exact sealed body、各status/name/非空rejected_cases、fixture_scope非空str、production_interfaces_used非空str list、old_success_suites=0/actual_anchor_arithmetic_replayed=false/candidate=false等を実stdoutとexecution票へ結ぶ。P側の三名/順序・tests要素の三keyと他の公開型は、rootが最終sourceで読了・確認して配達した値に一致する。Task1011のbootstrap・二診断のmetadata逆対照は既存第三群の中にあり、本WFは新群や旧suite再走を追加しない。

| 実行 | 内部秒/MiB | 外側秒 | 回数 |
|---|---:|---:|---:|
| WF metadata | 300 / 小metadata fixture | 300 | 1 |
| 新P selftest | 300 / 7168 | 360 | 1 |
| 新C selftest | 300 / 7168 | 360 | 1 |
| 新P fresh batch | 5400 / 7168 | 6000 | 1 |
| 新C全prefix | 10800 / 7168 | 11400 | 1 |

launcherはshell文字列でなくargv配列で実CLIを起動し、outer末尾30秒をTERM→KILLの余裕とする。jobは330分。内部UNKNOWN_RESOURCE exit3/実FAIL exit1/outer killを、exit0の完成resultへ読み替えない。新P本走は15 root（block4回）＋acceptance/output/batch-size32/max-seconds5400/max-memory-mib7168、resumeなし。新Cは同15 root/acceptanceにcandidate-rootと別rootのoutput、10800/7168とproducer宣言5400/7168を渡す。

Task1011の一般bootstrap再受付契約は、本WFの初回fresh一回という登録を変えない。自動再試行・追加invocationは行わない。resource-stop.jsonとrejected.jsonが併存しても全output保存対象に残し、Cは両者を実履歴へ認証する。未完成でのterminal nullを完成結果へ昇格しない。

Pの直後・Cの前に全output基準を保存し、全parent/source/raw/acceptance/driverのP後基準も保存する。C後はP前/P後/C後を個別に比較する。Pのexit3でも型付きprivate prefixができており全入力不変ならC一回でその範囲を照合できるが、candidate gateはP/Cとも正常完成exit0を必須とする。source/親の部分受付失敗でも取得済み基準と全bytesをalways対象に残し、不足はINCOMPLETE、不一致はFAILとして分ける。

## F5. 完成gate・計測・保存対象

新P result、public HEAD、final manifest、Cのfull comparisonに、owner/source/start/selection-start/completed selection・state/target/lambda・全countsの実file hashを結ぶ。C partial=false/candidate=true/full comparison/public final=true/durable_tail=nullだけを完成候補とし、private progressはBatchReductionState/current lambda=nullの別型で末尾sequence=3+6*processedへ結ぶ。

実selected=processed+skipped、processed=dependent+accepted、rank=1450+accepted/gen=8155+accepted、非空完成時accepted>=1を要求する。accepted32を期待値として置かない。COMPLETE_ZEROは同selection lambda/追加0、BATCH_COMPLETEは全選定処理後の新Separator、Linearは実lambda/rho2/pairing null・未処理tail測定null・`NEW_BATCH_SAME_WORD_ADAPTER_PENDING`。最終q/oracleは計算・再走せずnew_lambda_oracle=nullを維持する。旧97親＋実採用数のDERIVEDと、数値target負号/継承correction語の+sr(theta)を区別する。全11slot/80644/A0や新batch同語adapterの成功を主張しない。

coverage票はCが全比較した保存P resultと各manifest/typed payloadに結び、全failed indices/edges・四q/selection lambda/final lambda・全κ degree0/degree1の4x6 tag表/共有8aux・六score tag・8059 residual count・候補ごとのordinary epsilon/omega/三修理指数/SLP長/selection scalar/target scalar・全phase telemetryの所在と実値を保持する。q=0を作用素恒等零へ昇格しない。phase peakはprocess累積ru_maxrss、proc_ioは実取得値又はnull、payload_bytesはtelemetry自身を除く。同じ説明を実execution票の子process全rusage・/proc/pid/ioの最終取得sample（完全な終了カウンタとは称さない）と区別する。96対照時間を新batch時間へ流用しない。

`source-before/after`、全15親before/after、取得直後の全ZIP/extraction基準、受付、driver、全P output before/after、P/C各stdout/stderr/exit/start/finish/資源票、旧小receiptの同一bytesコピー、21源/3rawコピー、workflow/driver、coverage、実run票を保存する。source/親/全outputのhidden/pending/orphanも保存・照合し、通常完了countへ足さない。上流全ZIP/全展開はrunnerに保持し、artifactには再複製せずlive pinsと全inventoryで参照する。candidateとalways diagnosticsは**同じenvelope root**をuploadするので、ZIP digest差だけを内容差の根拠にしない。実run票のenvelope payload統計はその票自身を除いた時点を明記する。

grade2_member/grade2_nonmemberは常にNOT_DECIDED、full_A0/verified=false。Cのcross_checked=trueは全比較した新batchの限定scopeであり、保持TCBの旧独立性を再証明した意味ではない。工房CV9の正式格付けは別で、本GHAはまだ未発射。

## F6. 凍結と未実行境界

最終P/C pinを上記のとおり接続し、新workflowと本作者票を凍結する。最後の四env literal以外の本文はroot/1010が読了した全稿と不変であり、最終実hashと本票を同じ監査官・rootへ渡す。995の1011前sourceをメモリ内で逆置換した旧版textも、root全diff用に `%TEMP%/shadow-atelier-batch-task1011/checker995-before-task1011.py.txt` へ保存した（169824 B / `65aad639896ad5f5366f8d2e41c453cb43e47e4c671b116af92148c4f2f90a42`）。これは公刊sourceや新Pを変更したものではない。

現時点では全新runtime/metadata canary/P・C三群/本走/保全/候補upload未実行。新commit/run ID、数値成功、新rank/秒数は未観測である。995/1006および既公刊ファイルは凍結不変。Git/GHAと実受付作成はroot単独brokerが行う。

AUDIT_1009_VERDICT: WORKFLOW_FROZEN_WITH_FINAL_P_C_PINS; STATIC_READ_COMPLETE_NO_REQUIRED_FIX; NEW_GHA_AND_CANARIES_UNEXECUTED.
