# Task1036 — fixed lambda k128 producer v3

## F1. 作業境界と公開 ABI

Task1036/1035 と、継承を指定された公開1025/997/1000/1001/1002/1003/1004/1011/1030を全文読了した。変更は新 `search/d972_r07_fixed_lambda_cycle_batch_v3.py` と本返信だけ。基点 P v2 は208805 B / SHA256 `6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e` / LF3420として再照合した。旧source/WF/全票、Task1033 helper/返信は凍結を維持する。新Cの私的source/票/fixtureは読まず、ローカルPython/import/AST/数学/GAP/network/git/credential/新agentは実行しない。

外側schemaは `d972.r07.fixed-lambda-cycle-batch.v3`、新P/C pathと予定WFは公開1035通り。固定登録は ordinary integer の batch_size=128/max_batches=1、policy=`CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX`、partial_policy=`PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY`、refill=false。Pの `--batch-size` は128だけ。本番の15親・受付・output・資源CLI、同版resumeと完成済read-only再受付は旧型を保持する。初回WFはfresh P一回＋独立C一回で、P5400秒/C10800秒、各7168 MiB。実GHAはrootのみである。

親は同じ実旧64/rank1450/gen8155（run33990567016/1、artifact9977040548）。k64の1514/gen8219候補や正式1482/gen8187を初期stateへ取り込まない。全failed列/全54433弦＋2aux/全8059を保持し、kだけで全表を切らず、非零弦があれば先頭min(128,m)、弦零なら先頭非零aux一件、全零ならCOMPLETE_ZERO_CANDIDATE。候補依存時のrefillはない。

## F2. 新二群の公開型

`--selftest --selftest-root <fresh absolute TEMP root> --batch-size 128 --max-seconds 300 --max-memory-mib 7168` を公開CLIとする。selftest時だけroot必須、通常時拒否。rootは終了時に削除しない。旧1030の全raw file/empty dir/hiddenを保存する条件を継承し、whole fixture inventory/ZIPの実保全はrootの新WFで閉じる。

新二群の名前と順は `k128-version-registration-and-types`、`k128-full-roster-cutoff-and-restoration`。top bodyは status/tests/fixture_scope/production_interfaces_used/old_success_suites/actual_anchor_arithmetic_replayed/candidate/cross_checked/verified、外側v3のschema/sealだけを加える。各testは exact{name,status,rejected_cases}、old_success_suitesはordinary integer 0、actual_anchor_arithmetic_replayed=false、三assurance=false。fixture_scopeは非空str、production_interfaces_usedと各rejected_casesは非空str list。下記の拒否名/件数は完成sourceへの登録を静読した値であり、機械PASSの観測値ではない。

成功時にserializerが返すschemaは `d972.r07.fixed-lambda-cycle-batch.v3.selftest`。statusと各test.statusは実二群が完了した場合だけPASSとなる。public `production_interfaces_used` は次の15名を同順で保持する。

```json
["selftest_root_path","authenticate_acceptance","authenticate_registration","read_json","check_seal","invocation_files","validate_invocation_history","sequence_scope","pending_directory","authenticate_output_roster","classify_batch","BatchPhaseStore.ensure","BatchPhaseStore.accept","saved_selection_values","publish_selection"]
```

通常CLIは以下の15 roleと受付、別outputを要求する。`--block-root` は0,1,2,3の順で四回であり、残り11 roleは各一回。

```text
--state-root --delta-root --seed34-root --packet-root --refinement-root
--oracle-root --e-root --prepare-root --block-root (four ordered occurrences)
--p1-root --task712-root --continuation-root --acceptance --output
--batch-size 128 --max-seconds 5400 --max-memory-mib 7168
```

同版の明示 `--resume` は既存の厳密受付を維持するが、初回登録はfresh一回である。selftestは本番root/acceptance/outputを受け取らない。通常完了はstdoutに全canonical result、exit0。資源停止はUNKNOWN_RESOURCE/exit3、不整合はFAIL/exit1、通常のtyped診断名・保存境界は変更していない。CLI引数自体の拒否は本番算術の開始前である。

## F3. v2からの全差分と不変部分

新sourceの全本文を、既読v2の同一部分との全bytes照合を含めて静読し、旧v2からの変更行を全件読了した。AST/compile/importや自己試験・数値実行で代替していない。差分の全範囲は次の通り。

1. 冒頭のTask番号/k名、SCHEMA、C_FILE、BATCH_SIZE、POLICY、実launchを結ぶWORKFLOWをv3/128へ変更した。max_batches=1、partial policyと資源枠は不変。自系producer pathは従来通り自身の実 `__file__` descriptorへ結ぶので、旧Pのsource hashを偽装しない。
2. 自系二群のhelper名、fixture識別文字列、二群名、selftest開始/終了/診断ログ名をk128へ移した。旧版拒否は新v3に対するv2/schema/policy64/owner/source/旧invocationの改変に更新した。
3. 第一群の数境界をk=32/64/127/129/256、128.0/文字列128/trueへ、ordinal/row正127・負128、sequence正771・直後770→771・負772・二相先769→771へ更新した。32hex nonce、uint32/int32、旧親の32/64履歴は変更していない。
4. 第二群の全長fixtureをm=64/65/127/128/129、選定数64/65/127/128/128へ変更した。過剰129・旧先頭64打切り・128番目のindex/係数・尾部順序の逆対照へ移した。128番目の六cycle語のedge改変を一件追加し、係数零の因子もordered ancestryから落とせないことを同じ保存readerへ結んだ。
5. 公開1035が指定した末尾残差欠損の経路を、試験専用の完全treeを一度保存し、末尾一byteを削除し、descriptorのbytes/sha256/shapeとmanifest sealを作り直してから通常の保存readerへ渡す形にした。旧版のcommit内accept拒否から、実保存bytesのdecode→acceptによる全長拒否へ接続を明示した。これはfixture内の改変だけで、通常sourceの型gateやwriterには変更がない。

text比較では `def require` から新二群の直前までの175967 Bが、WORKFLOWの一literalを旧値へ戻すだけで旧v2と完全一致した。`def diagnostic` 以後の6828 Bもselftest診断ログ名の一literalを戻すだけで完全一致した。したがって通常の入力認証、全lambda算術、候補六相、消去、target/DERIVED、全保存、private/public publication、resume、完成済read-only再受付、CLI/mainの関数本文には新しい算術・保存算法の差分がない。

全配列・全EOF・両targetへの直接dot1・全旧行dot0、全係数と零を含むphysical factors、数値targetの負号とliteral correctionの正号を保持する。候補ordinalと採用row offsetを分離し、rank/generationは旧1450/8155に採用数だけを加える。候補別のfresh separator、新しい並列処理、refill、旧snapshot/旧insertの数値再走を追加していない。

## F4. 第一群の実接続と拒否登録30件

`k128-version-registration-and-types` は普通整数128/1を通常 `authenticate_registration` で受け、source fixtureを新Pの実file descriptorへ、ownerをそのsource/登録へ結ぶ。旧schemaのownerと各invocation改変は全sealを作り直して目的のgateへ到達させる。plain acceptance/registrationは元からself sealを持たない。synthetic旧source bindingは不一致hashの対照であり、実旧数学親を再認証したという意味ではない。

strict count0、resume=true、両before HEAD=nullの一bootstrap invocationを保存し、二つの異なるsynthetic host rootで同一portable owner/sourceを受け直す。旧host metadataを残したinvocation全bytesが両rootで一致することを読み、通常countが一件であることを `invocation_files` と履歴gateで確認する。実旧64全履歴や大きなspanのfixtureは再走しない。

ordinal/row127の正対照は登録されたpending directoryと通常のglobal roster readerに接続する。128はそのscopeから拒否する。sequence771と直後770→771は通常 `sequence_scope`、772/二相先/boolは同helperの拒否に結ぶ。これは新128境界のmetadata対照であり、実127行の数値採用を主張しない。

登録された拒否名の全順は次の30件である。

```json
["batch-32","batch-64","batch-127","batch-129","batch-256","batch-float","batch-string","batch-bool","max-batches-two","max-batches-bool","max-batches-float","refill-true","refill-integer-zero","old-policy","bool-resource","old-acceptance","old-owner-schema","old-owner-binding","old-source-binding","old-invocation-k64","bool-bootstrap-count","old-invocation-schema","sequence-772","two-phases-ahead","bool-sequence","candidate-ordinal-128","row-ordinal-128","existing-selftest-root","relative-selftest-root","missing-selftest-parent"]
```

| 対象 | 実通常gate |
|---|---|
| batch八件、max_batches三件 | strict_registered_batch_counts |
| refill二件、旧policy64 | registered_no_refill_private_final_policy |
| bool資源 | registered_limit_values |
| 旧acceptance schema | new_batch_acceptance_schema |
| 旧owner/旧invocation schema | canonical_object_seal |
| 旧owner/source binding | invocation_same_owner_source_start_selection |
| 旧invocation k64 | invocation_same_portable_input_and_registered_limits |
| bool bootstrap count | invocation_before_count_integer |
| 772/二相先/bool sequence | only_the_immediate_durable_phase_beyond_private_HEAD |
| candidate/row128 | unregistered_ordinary_output_directory |
| selftest root三件 | selftest_root_fresh / selftest_root_absolute / selftest_root_existing_parent |

各拒否はValueErrorを捕捉するだけで成功にせず、当該expected gate文字列を照合し、fixture scope・対照名・期待gate・実errorを `rejection.json` に保存する。

## F5. 第二群の実接続と拒否登録9件

`k128-full-roster-cutoff-and-restoration` は全54433長のsynthetic chord/tau/value/residualを通常 `classify_batch` へ渡す。五basisは非自明係数を持つcaseを含み、各選定witnessには係数零を含む六cycleを保存する。各mの最後の失敗を全弦末尾へ置き、m≤128では最後の選定にも含め、m129では未選定でも全failed配列から欠落しないことを読む。全弦配列を実Omegaで計算したという主張ではない。

| synthetic failed数 | 保存failed数 | 選定数 | 末尾失敗 |
|---:|---:|---:|---|
| 64 | 64 | 64 | 選定に含む |
| 65 | 65 | 65 | 選定に含む |
| 127 | 127 | 127 | 選定に含む |
| 128 | 128 | 128 | 選定に含む |
| 129 | 129 | 128 | 全failed配列に保存 |

各caseは実 `BatchPhaseStore.ensure` でtree payload/telemetry/manifestを保存し、別storeが全file bytes/SHA/dtype/shape/EOFを読み、`BatchPhaseStore.accept` と `saved_selection_values` を通る。完成treeの全inventoryを `packet/selection/tree` だけで比較する旧v2修理を保持した。その後の `publish_selection` が新しく書くselection.json/witness.json/oracle-view.jsonは、documentsを再生成して各実fileの全canonical bytesへ別に照合する。追加されるselection.jsonを古いdirectory全等値に混ぜる拒否は再導入していない。

弦非零とaux[2,1]の同居では弦を優先し、弦全零/aux[1,2]では先頭auxだけを選定し、両方全零では候補0のCOMPLETE_ZERO_CANDIDATEを返す。これらも同じ保存readerを通る。

登録された拒否名の全順は次の9件である。

```json
["overfull-129-witnesses","old-64-witness-cutoff","last-selected-index","last-selected-coefficient","last-selected-cycle-word","selected-tail-order","bool-selected-ordinal","truncated-last-residual","early-eof"]
```

| 拒否名 | 保存内容の改変と実gate |
|---|---|
| overfull-129-witnesses | 第129witnessを追加して全resealし、saved_same_start_exact_selected_witness_rosterで拒否 |
| old-64-witness-cutoff | 選定rosterを旧64で切って全resealし、同gateで拒否 |
| last-selected-index | 第128witnessを未選定の全弦末尾へ替え、saved_full_ordered_six_cyclesで拒否 |
| last-selected-coefficient | 第128witnessの五basis係数と対応cycle係数を整合して改変し、saved_six_cycle_tau_and_scalar_identityで拒否 |
| last-selected-cycle-word | 第128witnessの最後のcycle edgeだけを有効範囲の別edgeへ替え、saved_full_ordered_six_cyclesで拒否。係数零でも元のordered word recipeから消せない |
| selected-tail-order | 末尾二witnessを交換しordinalを126/127へ直して全resealし、saved_full_ordered_six_cyclesで拒否 |
| bool-selected-ordinal | boolをordinalへ入れて全resealし、saved_witness_bound_and_typedで拒否 |
| truncated-last-residual | 末尾一byteを削り、全pin/shape/manifest sealを更新した試験専用保存treeを読み、phase_descriptor_dtype_shape_and_full_hashで全長拒否 |
| early-eof | m129全長fixtureでもeof=falseを通常classify_batchへ渡し、complete_ascending_actual_chord_rosterで拒否 |

roster/witnessの改変は新manifestを含めて通常writerへ通してから保存readerへ渡す。末尾欠損の改変は完成した試験treeのみに行い、変更前descriptorと変更理由を別 `mutation.json` に保持する。旧成功fixtureや実親の内容を変更する経路ではない。上表はsourceを静読して特定した到達先であり、GHAでの実拒否成否は未観測である。

## F6. 全保存・資源・依存の保持

新selftest rootは既存regular parentを持つ、まだ存在しない絶対pathに限る。TEMP/RUNNER_TEMP内、source tree外、全ancestorのsymlink/junction拒否を保持する。CLIが実数学親/acceptance/outputの併用を拒否し、試験専用rootは再利用・削除しない。空のsynthetic host directory、全raw file、hidden/pending診断を終了時にも残す。成功時も中断時も実rootを終了ログへ書き、形成済rootの失敗にはtyped診断を保存する。

公開1030のP/C baseline、main P前/main C前/C後の三全比較、全directory entryを含むfixture ZIPと全stream再読、whole REPORTの明示二除外、always保全の条件を継承する。今回新WFを書いていないため、その実wrapperの保存成否を本票のP source静読からPASSへ昇格しない。新Pはその全保存を妨げるcleanupやfixture再利用を導入していない。

同一版のprivate HEADから直後一相だけを認証して回復する規則、未commit tailをcountへ混ぜない規則、bootstrap historyと限定atomic pending、二診断名、全入力before/after、durable phase→metadata→checkpoint→private HEAD、およびfinal→public HEAD→resultの停止境界を保持する。完成済resumeは全保存と全入力を再認証して既存resultをbyteのまま返し、新invocation/result/診断を既存packetへ書かない。初回WFでの自動再試行や再開は登録していない。

自系保持import closureは公開1002の九本をそのまま使う。source本文は自系だけを静読し、C側は公開1002の十本のmetadata rosterを認証する境界を維持する。新batch v1/v2を数値helperに追加していない。

```text
search/d972_r07_actual_grade2_root_scalar_batch_v2.py
search/d972_r07_actual_root_seed_materializer_v3.py
search/d972_r07_complete_oracle_cegar_continuation_v1.py
search/d972_r07_fixed_root_packet_loop_v2.py
search/d972_r07_full_origin_refinement_v1.py
search/d972_r07_rank1355_root_seed_scalars_v1.py
search/d972_r07_section_cochain_oracle_v1.py
search/d972_r07_selected_cycle_materializer_v1.py
search/d972_r07_targeted_grade2_owner_generated_join_v15.py
```

rawは同 `scratchpad/a0_paper_words_v1.json`、`scratchpad/a0_v2_words.json`、`scratchpad/fuda1_a0_rmax_data.g` の三本。保持Python19＋新P/C二本＋raw三本の全24と、Python `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]`、NumPy `2.5.1` の全文runtimeを変更しない。新C実source pinはrootの最終metadata受領に属し、本票から架空値を足さない。通常 `authenticate_code` は受付の新二本と全保持closure/rawの実全file bytes/SHAを照合する。

## F7. 完成source pinと静的点検

作者最終sourceは `search/d972_r07_fixed_lambda_cycle_batch_v3.py`、209926 B、SHA256 `a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8`、LF3434/CR0、全ASCII、BOMなし、末尾LF一個、行末空白0。これを作者freezeとし、根拠ある新指摘が届かない限り変更しない。

比較基点の旧P v2は208805 B / `6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e` / LF3420で不変を再確認した。増分1121 B/14行はF3の全限定差分である。source/返信以外の作業treeやTEMP helperを書き換えていない。Task1033 helper/票、正語P4、旧batch、旧WFはそのままである。

Task1036/1035、公開1025/997/1000/1001/1002/1003/1004/1011/1030を全読了した。自系source全本文・全差分・通常境界と新二群の実call先を静読し、全file byte/hash/LF等のmetadataのみで最終照合した。ローカルAST/compile/Python/import/数値/GAPは行わず、自己試験fixtureも本batch outputも形成していない。新sourceの機械AST合格、二群30/9件の実PASS、本P/C、全fixture/REPORT保全、実速度/資源使用量は未観測である。

## F8. 主張の射程とrootへの手渡し

公開1035が記録するk64の64/64・rank1514/gen8219は、この固定lambda/選択prefixでの実測である。そこからk128の独立率1.00、128採用、rank1578、速度や資源完走を予告しない。本便の親は同旧64/rank1450/gen8155のままである。

最終lambdaの四character supportは保存物理lambdaの直接読出しだけで、new_lambda_oracle=null、final/q.binなしを保持する。source_lower_zeroを新物理行から推論せず、grade2_member/grade2_nonmemberはNOT_DECIDED、full_A0=false/verified=false。LinearだけNEW_BATCH_SAME_WORD_ADAPTER_PENDING、その他NOT_APPLICABLE。共有TCBとF-fo-1/F-flb-1、返信163 F8.89の限定を新sourceから遡及解消したとは主張しない。A0 actual0/1・階段1/6もこのsource準備だけでは昇格しない。

新P v3と公開CLI/二群型/30・9拒否名をrootへ手渡す。rootの全metadata受領、全新source静読、別監査、新WF全保全監査、届いた工房CV-9の読了を経てからrootのみが公開/GHAを行う。この作者票は静的完成であり、実行許可・機械PASS・正式cross-checked/verifiedの代用ではない。新run/commit/artifact/採用数の未来値は記帳していない。

AUDIT_1036_VERDICT: PRODUCER_V3_COMPLETE_STATIC_ONLY_RUNTIME_PENDING
