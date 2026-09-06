# Task1026 返信 — 固定lambda k64 P v2

## F1. 受領と完成境界

Task1025 / Task1026 を全文読了した。変更は新 `search/d972_r07_fixed_lambda_cycle_batch_v2.py` と本返信だけ。旧P v1は213861 B / SHA256 `229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591` を全bytesの基点として複写した。旧P4/1016/1022/1023、相手source/私的返信には変更・読取を行っていない。

通常の登録をv2・64/1・CHORD_FIRST_ROSTER_64_THEN_FIRST_AUXへ接続した。親は同じrun33990567016/1・旧64/rank1450/gen8155、全15親と保持closure、全算術/保存規則はTask1025のまま。新run/成果のpinは作っていない。ローカルPython/import/AST/数値/GAP、network/git/GHA/credential/追加agentを使用していない。

全文読了した公開Task1025は7425 B / SHA256 `6ad8e81339cb6be8b8660bdd452af5742707415fabe11e66aa02cb524d9660ed`、Task1026は1468 B / `cdf1e870d4028f562b3185eec74d76735b94f507364956a8db415725eb2fd85e`。本返信は実装と静的読取の完成票であり、新二群や新k64の機械PASSを主張しない。

## F2. 最終公開CLI・自己試験型

本番CLIは旧15親引数、--acceptance、--output、--batch-size 64、--max-seconds 5400、--max-memory-mib 7168、同v2の--resumeを保持する。新--selftest-rootは自己試験時だけ必須で、本番では拒否する。自己試験呼出しは `--selftest --selftest-root <absolute fresh TEMP-or-RUNNER_TEMP path> --batch-size 64 --max-seconds 300 --max-memory-mib 7168`。既存regular parent、全ancestor非symlink、root未存在を作成前に認証し、fixtureを削除しない。

新selftestのschemaは `d972.r07.fixed-lambda-cycle-batch.v2.selftest`。seal以外のexact bodyは status/tests/fixture_scope/production_interfaces_used/old_success_suites/actual_anchor_arithmetic_replayed/candidate/cross_checked/verified。testsは順に `k64-version-registration-and-types`、`k64-full-roster-cutoff-and-restoration` の二件だけで、各exact name/status/rejected_cases。非空str/list、old_success_suitesは普通整数0、actual_anchor_arithmetic_replayed=false、三assuranceはfalse。topにsource別名・実root・新receipt字段を足さない。実rootは外側実command/全inventoryと診断logへ結ぶ。通常出力のschema/body/全sealと旧innerの型は公開1025から増やさない。

sourceの自己試験入口でもmax_seconds/max_memory_mib/batch_sizeをstrict普通整数、resumeをboolean falseで確認する。自己試験のfixture-root印は入口で初期化し、pathの認証・fresh作成に成功した後だけ保存先として使用する。CLIの必須引数や通常/自己試験の混在拒否はroot作成前であり、外側command/stderr/exitへ残る。

## F3. 全source差分の静的閉鎖

凍結v1全213861 Bをtextとして読み、新v2全文を次の12置換区間の適用結果へ照合した。これはPowerShell/JSによる文字列・全file metadataの比較であり、Python parser/import/ASTや機械算術ではない。記載外の通常source差分は無い。

| 区間 | 最終差分 |
|---|---|
| 冒頭docstring | Task1026/k64の説明へ |
| SCHEMA | 新外側 `d972.r07.fixed-lambda-cycle-batch.v2` |
| C_FILE | `check_d972_r07_fixed_lambda_cycle_batch_v2.py` |
| BATCH_SIZE | 64、MAX_BATCHESは1のまま |
| POLICY | `CHORD_FIRST_ROSTER_64_THEN_FIRST_AUX` |
| WORKFLOW | `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml` |
| global | 自己試験の作成済みroot印 `SELFTEST_ROOT_CREATED` 一件 |
| 旧canary_selectionから旧selftestまで | 旧三群の本体/dispatcherを新二群・保存fixture・root gateへ置換。通常の係数/target/packedを再試験する旧suiteを呼ばない |
| diagnostic末尾 | 自己試験時だけ、実rootをstderrへ記録し、作成済みrootへ同じsealed診断を保存 |
| CLI追加 | `--selftest-root` |
| CLI自己試験分岐 | root必須・actual親/受付/output引数なし |
| CLI通常分岐 | selftest-rootを拒否 |

新selftest区間には最終のstrict integer/resume gateとroot印初期化を含む。暫定208641 B版へこの154 B/3行を足した後、1028の必須指摘を受けて同区間の不変比較対象二箇所を修理した。最終値はF8の208805 B。

1028/rootの指摘は、自己試験で `packet/selection` のbefore inventoryを取り、その後 `publish_selection` が同directoryへ新selection.jsonを形成するため、元の完全同値比較では最初のm32を拒否するというものだった。修理は新source 3203/3207行の対象を `packet/selection/tree` へ限定する二literal（+10 B）だけ。完了済みtree全bytes不変を比較し、新selection/witness/viewの全bytesは既存docs比較で保持する。通常算術・公開gate・旧sourceは変更せず、208795 B版の作者pinをこの根拠により更新した。

通常の `classify_batch` / `current_batch_tree` / 数値reduce/advance/final separator、親受付/thin anchor、全raw/source/primal/P1/B、decision/checkpoint、復元/publication、bootstrap、完成read-only resume、入力保全の関数本文は保持した。上限は既存BATCH_SIZE参照を通じて64/ordinal0..63/sequence上限387へ伝わる。selftest内の32は旧版拒否又はm32正対照であり、旧登録値の通常fixtureではない。nonce32hex、dtype/int32/u32、歴史before32と旧artifact/旧親schemaは変更していない。

新v1 batch sourceを追加の計算helperとしてimportしない。保持9P/10C/raw3の登録表、実旧runtime全文、全15artifact/全file/全dir/全historyのpinは凍結v1から不変。code.producerは実自己pathと全bytes/SHA、code.checkerは新公開C pathと実descriptorへ入場時に結ぶ。未来C pinや新run pinを本票で捏造しない。保持closureは19 Python＋新P/C二件＝21 Python、raw3を含め24 fileのまま。

## F4. 第一群の実装・拒否名

`k64-version-registration-and-types` は **30件の期待拒否** を定義した。未実行なので、30件が機械上PASSしたという記録ではない。`k64_reject` はValueErrorの有無だけでなく、期待した通常gateのmessageが実例外に含まれることを要求する。各入力と実拒否内容を別case directoryへ保存し、最後にまとめて削除しない。

拒否名は次の順序。

```text
batch-32
batch-33
batch-63
batch-65
batch-128
batch-float
batch-string
batch-bool
max-batches-two
max-batches-bool
max-batches-float
refill-true
refill-integer-zero
old-policy
bool-resource
old-acceptance
old-owner-schema
old-owner-binding
old-source-binding
old-invocation-k32
bool-bootstrap-count
old-invocation-schema
sequence-388
two-phases-ahead
bool-sequence
candidate-ordinal-64
row-ordinal-64
existing-selftest-root
relative-selftest-root
missing-selftest-parent
```

正対照の64/1/policy/false/resourcesは `authenticate_registration` の通常入口を通す。旧acceptanceは同じ六key plain JSONの旧schemaを `authenticate_acceptance` へ渡し、親大物を読む前のschema gateで拒否させる。旧owner/invocationのschema変更とowner/source/k/countの改竄は、canonical全sealを再計算してから通常 `read_json` / `invocation_files` へ渡す。旧source/hashが新bindingへ一致しない点を、stale sealだけに依存させない。

source-binding fixtureには実自己file descriptorを保存する。synthetic owner/portable受付は `UNADMITTED_SYNTHETIC_INTERFACE_INPUT` として扱い、本番owner・数学親を受理したという成果にはしない。新selftest topに架空source別名を加えていない。

新owner/bindingに結んだstrict count0・両before HEAD nullのbootstrap一件を形成する。二つの別packet rootと二つの別host受付を作り、旧hostのinvocation bytesをそのまま第二rootへ保存する。`invocation_files` / `validate_invocation_history` が旧hostから全acceptance hashを再構成し、同portable identityで認証することを正対照にした。通常receipt数は一件であり、実GHAや実rank1450の履歴ではない。

`sequence_scope(387,387)` / `(386,387)` を受け、388や二phase先、bool sequenceを拒否する。候補/row63の限定pending directoryは実 `authenticate_output_roster` まで通し、64は同global rosterが普通directoryの上限違反として拒否する。nonce長は32のまま。root gate自身へ既存root・相対root・欠けたparentを通し、指定した拒否に到達させる。symlink拒否は通常path gateに存在するが、新fixtureにsymlinkを残す対照は作っていない。

## F5. 第二群の実装・拒否名

`k64-full-roster-cutoff-and-restoration` はm32/33/63/64/65の五正対照、aux-only、complete-zeroの二分岐対照と、**8件の期待拒否** を定義した。

| m | 全saved failed数 | selected数 | 全弦末尾 |
|---|---:|---:|---|
| 32 | 32 | 32 | 選定にも含む |
| 33 | 33 | 33 | 選定にも含む |
| 63 | 63 | 63 | 選定にも含む |
| 64 | 64 | 64 | ordinal63として含む |
| 65 | 65 | 64 | 65番目の失敗として全表へ残し、選定しない |

全長54433のsynthetic弦表・固定五basisを使い、各caseの末尾非零をCHORDS-1へ置く。最初の非零には非自明な五basis係数を持たせ、全六cycleと零係数を保持する。五caseすべてでauxも非零だが、弦が先に選ばれる。aux-onlyでは最初の座標一件、全零ではwitness零を保持する。

通常 `classify_batch` からtyped tree payloadを作り、`BatchPhaseStore.ensure/commit/accept` の実全file保存を通す。別の空storeへ全descriptor/全bytes/hash/型/EOFを読み戻して `BatchPhaseStore.accept` → `saved_selection_values` へ渡す。section/cochainの先行hashは保存した明示synthetic contextであり、実section/cochain算術を走らせたと呼ばない。旧全phaseを再走するテストではない。

正対照は `publish_selection` を通じて全witness/selection/oracle-viewを形成し、元tree全inventoryが不変なこと、同通常serializerで再構成した外fileの全bytesが一致することを要求する。正対照・各負対照は別directoryであり、後の負対照のために前の成功fixtureを上書きしない。

拒否名は次の順序。

```text
overfull-65-witnesses
old-32-witness-cutoff
last-selected-index
last-selected-coefficient
selected-tail-order
bool-selected-ordinal
truncated-last-residual
early-eof
```

最初の六件は保存witness/rosterを改竄後に全seal・typed phase descriptor/manifestを作り直し、保存readerの目的gateで拒否する。64番目の係数改竄では対応するcycle係数も合わせて変更し、単なる字面の不一致を越えて保存したtau/scalar identityへ到達させる。尾部入替えではordinalを整えてから元roster順との不一致を調べる。

全末尾残差の欠損は通常phaseのdtype/shape/fullhash gateへ、EOF=falseは全長入力の通常selector入口へ渡す。欠損fixtureは正しいphaseとしてpublishされる前のpending directoryにも実bytesを残す。全min式をもう一つ写しただけの自己比較にはしていない。候補E・旧係数/target/packed成功suite・旧Omega/旧rank1450算術をここから呼ばない。

## F6. fixture配置・診断の公開仕様

WFはREPORTをRUNNER_TEMP配下に置き、既存parent `REPORT/selftest-fixtures` を用意してからPへ未存在の `REPORT/selftest-fixtures/P` を渡す。sourceは作成前に絶対path、未存在root、既存directory parent、全ancestor非symlink/非junction、TEMP又はRUNNER_TEMPの子、source treeとの非包含を認証する。parents=Trueで任意の欠けたroot列を作る入口にはしない。

| root相対 | 保存内容 |
|---|---|
| registration/ | valid-registration、実自己descriptorを含むsource-binding-input、新旧owner schema fixture、各caseの入力/期待拒否 |
| registration/host-0, host-1 | 二つのsynthetic15 role directoryと、それぞれの実絶対host pathを持つ受付fixture |
| registration/bootstrap-original/packet, bootstrap-reroot/packet | 一件の同canonical invocationをそのまま保存した二root |
| registration/<拒否名>/ | registration.json又はinput.json、必要なpacket payload、rejection.json |
| selection/m32,m33,m63,m64,m65 | input.json、fixture-context.json、packet/selection/treeの全typed payload/manifest、外側全witness/selection/oracle-view |
| selection/auxiliary-only, complete-zero | 同じ全table保存経路の分岐fixture |
| selection/<拒否名>/ | resealした全tree、又は未publish pending tree、又は元m65を指定したEOF入力、およびrejection.json |
| resource-stop.json又はrejected.json | 自己試験root作成後の停止時だけ、既存exact診断schema/bodyをそのまま保存 |

各 `rejection.json` はfixture専用plain canonical JSONで、exact keysは fixture_scope/name/expected_gate/observed_error。fixture_scopeはUNADMITTED_SYNTHETIC_INTERFACE_INPUT、残りは非空str。fixture-context.jsonはfixture_scope/binding/prior_phase_hashes/actual_section_or_cochain_replayedで、最後はfalse。これらは新batch数学receiptではなく、selftest topへdescriptor字段を追加しない。外側WFが実rootと全files/directories/全hashを保存するための点検材料である。

stderrには `k64-selftest-root-created` とfinallyの `k64-selftest-fixtures-retained` を実root付きで出す。自己試験の例外時は `k64-selftest-diagnostic` にstatus/selftest_root/createdを記録し、作成済みrootだけへ sealed `.v2.resource-stop` 又は `.v2.rejected` を保存する。bodyは通常診断のexact型で、actual数学binding/countはnull、partial=true、三assurance=false。root未作成の失敗では指定pathへ新しく診断を書かず、外側stderr/exitを残す。

fixtureのcleanup・再利用・正語scratchからのresumeを作っていない。成功・拒否・資源途中の全fixtureを終了時に削除せず、通常batch出力とも混ぜない。自己試験途中で失敗した場合も、未実行の後半caseを成功としたreceiptは返さない。

## F7. 継承する計算・保存と未走境界

全54433弦/2aux/全8059/four-characterからの先頭min(64,m)、弦零時だけaux、全零時の現lambda COMPLETE_ZERO、依存の補充無しを維持する。通常batchはrank1450/gen8155と同selection lambdaからfreshに始める。旧k32の1482又はcontrol96の1482を加算せず、v1 packetを新sourceでresumeしない。新v2内のstrict resume、直後一phaseのadopt、bootstrap、二diagnostic、完成packetの無書込みread-only再受付は元の本文のまま。

全旧1450行dot0と両target dot1を今回直接読み、元start targetと旧64現targetを区別する。rho2 DERIVEDは旧97親を保持し、新採用rowだけを足す。数値targetの負号、literal correctionの正号、全六cycle・零power/Ref・全祖先は不変。public finalの前にprivate stateをSeparator等へ昇格しない。

P5400/C10800秒、各7168 MiB、外側6000/11400秒、自己試験300/外側360秒は上限である。新速度、64採用、rank1514、独立率、完走を観測値として記録していない。相の秒・プロセス累積RU_MAXRSS・前後I/O・payload bytes、P全/C全、全saved bytesと各countを従来どおり分ける。約94%は旧primal+P1/候補六相、P全に対して約76%という分母訂正を維持する。

共有TCB/F-fo-1/F-flb-1は引き続き未閉鎖の範囲を含む。新sourceが二保持kernelの独立性を証明したという主張をしていない。new_lambda_oracle=null、final q等の追加無し、grade2二件NOT_DECIDED、full_A0/verified=false。LinearだけNEW_BATCH_SAME_WORD_ADAPTER_PENDING、それ以外NOT_APPLICABLE。P/C候補と工房CV-9の正式受理を分け、A0 actual0/1・階段1/6の台帳を本便で更新しない。

root/別監査官が新全差分・新C公開pin・新WFの型/保全/初回fresh一回Pと全C一回を閉じた後、GHAで新二群と本番を行う段階が残る。本便ではsource編集と静的全文/全差分/全file metadataの読取だけを行った。数値試験/AST/importは実行していない。

## F8. 作者freeze

新source `search/d972_r07_fixed_lambda_cycle_batch_v2.py` は **208805 B / SHA256 `6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e`**、LF3420、CR0、UTF-8 BOM無し、最終LF一件、行末空白無し。この全sourceを作者完成版として再凍結する。凍結v1の全pinは再照合して不変であり、本便のsource/WF実行は無い。追加の根拠ある静的修理が必要なら、rootへ差分を先に伝えてから新未公開sourceだけに限定する。

実装の静的完成と、30+8拒否・新k64本番の実機PASSは別である。本返信は後者を未実行として引き渡す。

AUDIT_1026_VERDICT: PRODUCER_V2_IMPLEMENTATION_COMPLETE_STATIC_ONLY_NEW_SELFTEST_AND_RUNTIME_PENDING
