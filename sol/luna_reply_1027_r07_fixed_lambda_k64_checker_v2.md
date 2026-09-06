# Task1027 — 固定lambda k64 独立checker v2

**F1 — 作者凍結と根拠。** 新 `search/check_d972_r07_fixed_lambda_cycle_batch_v2.py` を完成し、177544 bytes / SHA256 `4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90` で作者凍結する。LF2675、CR0、BOMなし、最終LFあり、末尾空白0行。公開Task1025全文（7425 B / `6ad8e81339cb6be8b8660bdd452af5742707415fabe11e66aa02cb524d9660ed`）とTask1027全文（1497 B / `6c4613b778faa98981207b877866ac1c02921ccf69b5c530eb7958abd68e7c9a`）を読了した。変更範囲は新C v2と本票のみ。旧C v1、正語D4、WF5、返信1019は不変。新P本文/helper/私的1023・1026票は読んでいない。

基点は自系凍結 `search/check_d972_r07_fixed_lambda_cycle_batch_v1.py`、181828 B / `7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f`。実hashを確認し、宣言した変更をメモリ上で逆置換した全文が旧181828 bytes/同SHAへ完全一致することをPowerShell/.NETの静的文字列比較で照合した。新数学計算、Python/import/AST/GAP/数値、network/git/GHA/credential、追加agentはローカルで実行していない。独立最終監査票、新GHA、二群の実PASS、実k64の算術結果は本票時点で未観測である。

**F2 — 通常経路の限定差分。** 外側prefixを `d972.r07.fixed-lambda-cycle-batch.v2`、固定batch_sizeを64、selection_policyを `CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX` へ移す。max_batches=1、partial_policy=`PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY`、refill=false。P/selfの登録pathを各 `*_fixed_lambda_cycle_batch_v2.py`、新invocation.workflowを `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml` へ結ぶ。通常登録/schema/source-pathの既存比較を小さい共通metadata helperへ分け、新二群もその実helperへ接続した。batch_size/max_batches/refillは等値float/bool/stringを許さない。

候補ordinal/新row local offsetは0..63、相sequenceは既存 `3+6*i+p` のまま最大387へ拡張する。通常 `compare_phase` / `row_source` / `registered_basenames` の境界も明示した。無関係のnonce32hex、int32/u32、旧歴史before32、旧親schema、旧inner数値phase schema、旧artifact名を改名していない。既存bootstrap、one-phase durable tail、私的HEADからのcount報告、全diagnostic型、同v2内の厳密resume、完成packetのread-only再受付・旧invocation/result無書込みは保持する。初回WFはfresh一回という公開登録であり、Cはproducerへ書き込まない。

保持する基点はrun33990567016/1、旧64/rank1450/gen8155、head `c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70`、artifact9977040548、ZIP304642285 B / `a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792`。元14とcontinuationの全15親のtuple/全file/dir/全歴史/旧C64を保持する。k32成果/control96/rank1482を初期stateへ入れず、旧batch packetを新schemaのresumeに使わない。保持Python19とraw3の全pinは公開1002どおり不変、新P/C二本を加えた全24fileを通常acceptanceと実file全hashへ結ぶ。新Pの最終pinはrootが作る実acceptanceで供給され、Cは新pathと実bytes/hashを認証する。旧batch v1を数値helperとしてimportしない。

**F3 — 数学・TCB・成果の境界。** 同じ固定lambdaで全54433弦・2aux・four-character・全8059を扱う。全failed/residualを保持し、非零弦m>0なら先頭min(64,m)、弦零なら先頭非零aux一件、全零ならそのcurrent lambdaのCOMPLETE_ZERO_CANDIDATE。依存候補のrefillはしない。候補別raw/source/primal/P1/四B、全六cycleと零係数/祖先/Ref、普通整数signed exponent/mod54、物理48384/source lower96776/physical lower32260、挿入順消去の全係数は基点と同じ計算である。数値targetは負号、literal correctionは正号、外側scale一回を維持する。

全旧行dot0と両target dot1は今回直接読み、全rho2 DERIVED親と深いcopyを保持する。候補ごとのSeparatorを作らず、全候補処理後のfinalizerだけが公開physical HEADを作る。新lambda oracleはnull、grade2二字段NOT_DECIDED、full_A0=false、verified=false。Linearの場合だけNEW_BATCH_SAME_WORD_ADAPTER_PENDING、その他NOT_APPLICABLE。partial PASSを本語candidateにしない。既存candidate/cross_checkedの限定scopeと工房CV-9正式受理を分ける。共有TCB/F-fo-1/F-flb-1と返信163 F8.89の限定を保持し、二保持kernelの独立性を新sourceから主張しない。rankは1450+実accepted、generationは8155+実acceptedであり、64採用/rank1514/独立率/速度/資源天井を予告しない。

**F4 — 新第一群。** `k64-version-registration-and-types` は新登録、outer schema、実自系source/path、owner/scope、63/387境界、one-phase tail、count0 bootstrap、portable ownerの一件re-rootを小metadataから読む。通常呼先は `check_registration`、`check_acceptance_header`、`check_executable_paths`、`compare_root_records`、`row_source`、`phase_at_sequence`、`compare_phase`、`ProgressAudit`、`invocation_records`、`registered_basenames`、`CandidateFiles`、`prepare_selftest_root`。実rank1450の行計算や旧三群を呼ばない。正対照のrow63 bytes/descriptor、owner二配置、ordinal63 phase、sequence387、one-phase/checkpoint/HEAD、bootstrapのhost/acceptance bindingを保存する。sourceのP descriptorは明示されたfixture入力であり、新Pの実pinを推定したものではない。通常入場の実source24file認証は別に保持する。

登録した拒否名は28件で、実機の拒否成功は未観測: `batch-size-32`、`batch-size-33`、`batch-size-63`、`batch-size-65`、`batch-size-128`、`batch-size-float`、`batch-size-string`、`batch-size-bool`、`max-batches-two`、`max-batches-bool`、`max-batches-float`、`refill-true`、`refill-integer-zero`、`old-policy32`、`old-acceptance-schema`、`old-producer-path`、`old-checker-path`、`old-owner-schema`、`old-owner-scope32`、`row-offset-64`、`phase-sequence-388`、`candidate-ordinal64`、`two-phases-ahead`、`bootstrap-float-zero`、`bootstrap-bool`、`bootstrap-count-one`、`selftest-root-reuse`、`selftest-root-relative`。登録・owner・invocationの負対照はcanonical/封印を作り直した保存bytesから実helperへ到達する。先行一phaseを全比較してもHEAD count0を保ち、二phase先は通常ProgressAuditが拒否する。

**F5 — 新第二群。** `k64-full-roster-cutoff-and-restoration` は自系の非単位permutation basisと非自明な五係数を使い、全54433行のsynthetic配列を通常 `select_all_residuals` へ渡す。m=32/33/63/64/65の五caseでは、各caseの最後の非零を全弦末尾54432へ置き、保存failed数はm、選定数は32/33/63/64/64を要求する。全caseで弦とaux双方を非零にして弦優先を確認する。さらに弦零で先頭aux/第二aux、全零の三caseを加え、正対照は合計8case。五basis係数・全六cycle・零係数を保持し、edge番号は逆順の完全rosterとしてroster順とedge数値順を区別する。

通常 `witness_records` / `batch_tree_payloads` / `selection_record` / `oracle_view_record` で全配列・typed descriptor・manifest・witness・view・selectionを保存し、`CandidateFiles` / `compare_phase` / `compare_selection_publication` / `compare_candidate_roster` で全bytes/EOF/全rosterを再読する。これはmin式を写した自己試験ではなく、全長選択と保存後の復元を通す。potential等の前相入力は明示したsynthetic protocol fieldであり、実Q/実Omegaを再演したとはしない。

保存readerへ通す拒否名は7件で、実機PASSは未観測: `over-limit-65-witnesses`、`old-first32-cutoff`、`whole-residual-table-last-byte-missing`、`failed-roster-last-index-missing`、`sixtyfourth-roster-index-changed`、`sixtyfourth-coefficient-and-cycle-changed`、`selection-tail-order-changed`。witness/selection/view/phase manifestは変更に合わせて再封印した別fixtureへ保存する。64件caseの第64witnessは実synthetic末尾を指し、そのindex・係数/cycle・末尾順の改竄を通常全比較へ通す。正負いずれのfixtureも削除しない。

**F6 — CLIと全fixture保全。** 新 `--selftest-root` はselftest時だけ必須で、通常実行では拒否する。絶対path、TEMP又は明示RUNNER_TEMP配下、既存regular parent、全ancestorのsymlink/junctionなし、新規root・再利用不可、repository/sourceとの非包含をmkdir前に認証する。selftest時は全数学親/acceptance/candidate/output引数を拒否し、rootの `registration/` と `roster/` 以下へ全正負case/配列/封印/台帳を残す。TemporaryDirectoryによる削除やfixture unlinkはない。selftest topへ余分なpath/source別名を追加せず、実rootは外側commandと全inventoryへ結ぶ。

新selftestの実行形はGHAでのみ次のとおり。P側の引数/rootを混ぜず、外側上限360秒とする。

```sh
python -B search/check_d972_r07_fixed_lambda_cycle_batch_v2.py --selftest \
  --selftest-root "$REPORT/selftest-fixtures/C" --max-seconds 300 --max-memory-mib 7168
```

通常Cは既存の全15root（block-root四回）と `--acceptance` / `--candidate-root` / `--output` を指定し、`--max-seconds 10800 --max-memory-mib 7168 --producer-max-seconds 5400 --producer-max-memory-mib 7168` を使う。Cへ不要な `--batch-size` は追加していない。Pの登録64/1はacceptance/invocationからstrictに読む。通常C外側11400秒、同固定Pは5400/6000秒・7168 MiB。全retained boundary/progressは新deadline/ResourceStopへ引き続き接続する。成功exit0、資源UNKNOWN_RESOURCE exit3、型/算術不正FAIL exit1、partial flagsのリセット、checker reportをcandidate/親へ書かない条件は保持する。

**F7 — 公開selftest型と未実行。** topは `d972.r07.fixed-lambda-cycle-batch.v2.selftest` のsealed object、body exact `status/tests/fixture_scope/production_interfaces_used/old_success_suites/actual_anchor_arithmetic_replayed/candidate/cross_checked/verified`。testsはF4→F5の二要素、各exact `{name,status,rejected_cases}`。status PASS、fixture_scope非空str、production_interfaces_used非空str list、old_success_suitesは普通整数0、actual_anchor_arithmetic_replayed=false、三assurance全false。これらのPASSはCLIが二群を実際に完了した場合だけ生成する。作者が機械PASSを先に保存したものではない。

旧selftest三群の呼出しと旧canary本文を新sourceから除去し、新二群だけへ接続した。旧成功はrun34004423047/1の保存実績を別の受付で認証する対象で、新Cから旧全suiteを再走しない。全source/全指定差分を静的に読み、F1の完全逆置換一致と実pin/EOLを照合した。新AST、二群28/7拒否の実績、本C全新payload照合、実測phase/RSS/I/O/採用数/保存量、CV-9は未観測である。公開・GHAはroot単一brokerで、新run/commit/artifactを本票へ先取りしない。

AUDIT_1027_VERDICT: CHECKER_V2_SOURCE_FROZEN_STATIC_COMPLETE; K64_ONE_BATCH_NO_REFILL; NEW_TWO_SELFTEST_GROUPS_REGISTERED; NO_LOCAL_EXECUTION; INDEPENDENT_FINAL_AUDIT_AND_GHA_UNOBSERVED.
