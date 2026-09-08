# Task1128 — P6 public selftest gap-run 外側提案

F1. 既存 gap-run を用いる P6 selftest 外側 4file を完成し、TEMP の immutable review-snapshot-v1 へ凍結した。判定は STATIC_PROPOSAL_READY_RUNTIME_PENDING。本便では Python/GAP/import/compile/AST/selftest/数学/Git/GHA/network/credential 操作を実行していない。P source、既 workflow、旧成果・既受領 process は変更していない。C private source/実装/私的票も読んでいない。正式 inventory5 の到着時は Task1109 final binding が優先であり、この外側は本走や親入場の代替、追加受領 gate ではない。

入力 Task1128 は 4530 B / 19ad937dfbb6428bd18cd77e9960b6d845a8a7229a1e68dcd361fd5c922d58ab。P は task1109/d972_r07_fixed_lambda_cycle_batch_v6.py の 453749 B / 75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7 のまま。BATCH_V5_INVENTORY_REGISTRATION=None、IMPLEMENTATION_COMPLETE=False を raw 行で確認した。通常 run_actual の入口は閉じたまま、selftest 分岐だけを登録する。

F2. 最終配置候補は、共通 stem search/d972_r07_P6_public_selftest_gha_v1 の次の 4file。実体は %TEMP%/shadow-atelier-audit163/task1128/review-snapshot-v1/。全て ASCII、CR0、末尾 LF。root が静的採択後に配置する候補であり、本便から作業ツリーへ昇格していない。

| suffix | bytes | SHA256 | LF |
| --- | ---: | --- | ---: |
| .g | 908 | 73a040ff77a8a3b18175917350d65c8610fc7d8fd8fe92ae9cb8f3f09d222e85 | 17 |
| .sh | 2212 | 115aba035d7c5c4a6ab03520c5598a8d303fa05df1364cd5ac060c7c9db39206 | 56 |
| .py | 34142 | 8aa03dc7e62e51af9b5c9878bb05ead094c317b094473aaadea46fb4561dc631 | 601 |
| .json | 24360 | 1ed4e223722800f3b7d3fd76ee569e0926df4e9574a1b8f6f150a80280d69545 | 1 |

snapshot manifest-v1.json は 3557 B / c4cad630baed24acfc8f2535b6e1aa299b42ba79b282efc9275200bfbac359bf。GAP が Bash の全 bytes/SHA を検査し、Bash が Python/config の全 pin を検査する。root の固定 .g pin と合わせた起動連鎖であり、自己 hash の循環は作らない。終了 marker の意味は F7 の複数 receipt を必要とする。

F3. public-P-selftest-ABI-v1.json（28603 B / f76612722b095c235612d4e06b3cc9b0edb0196b5c20d7e6a402c5371cd6e1e4）は P 自身の selftest/CLI/各 canary から確定した。stdout は d972.r07.fixed-lambda-cycle-batch.v6.selftest の exact11 key、署名対象 canonical bytes＋LF の inner seal と stdout 全 raw pin を別に照合する。status、fixture_scope は登録 str、old_success_suites は bool を除く int0、actual_anchor_arithmetic_replayed/candidate/cross_checked/verified は bool false。production_interfaces_used は source 順の exact37 str。

| ordered group | 拒否件数 |
| --- | ---: |
| k128-version-registration-and-types | 30 |
| k128-full-roster-cutoff-and-restoration | 10 |
| batch-parent1578-admission-and-projection | 6 |
| batch-parent1706-two-layer-admission | 7 |
| batch-parent1834-three-layer-admission | 8 |

各 tests item は name/status/rejected_cases の exact3 key。全61の ordered name、保存 rejection path、目的 label を P 固有の表へ結んだ。旧4群の k128_reject は、登録 expected_gate が実 observed_error に含まれる元の条件を保つ。第五群だけは exact4 の fixture_scope/name/expected_gate/observed_error を読み、裸 expected_gate と fixed_lambda_batch: を含む observed_error の完全一致をそれぞれ要求する。旧条件を事後に強化したことにはしない。

第五群は batch-parent-v5/ の exact34 file、全 directory、positive/inventory-root/empty の空1件を登録した。case-ledger は exact4、各8 case は exact6、正負/rejection descriptor は group-root 相対の exact3。全 descriptor の実 file bytes/SHA を再読し、scope の positive_inventory を実正例の全 files/directories へ canonical bytes で照合する。元97形状の32/65と前二層256は保存 scope の普通整数へ結ぶ。正例達成の根拠は、固定 P の通常 helper 呼出しを通過した sealed PASS と保存 ledger/全正例 bytes。別の実測 positive-call counter があるとは主張せず、実1834親受理とも扱わない。

F4. 子 argv は venv Python -B P6 --selftest --selftest-root <fresh absolute path> --batch-size 128 --max-seconds 300 --max-memory-mib 7168。RUNNER_TEMP の新 UUID directory に venv、home、未作成 selftest-fixtures を分離する。P の main は 7168 MiB の RLIMIT_AS を設定するので、指示書の RSS 略記は root の訂正に従い virtual-address-space limit と記録した。外側の RSS 専用上限・測定は主張せず、RSS peak は null。内側は協調的 deadline300秒、外側 subprocess timeout360秒であり、時間計器の範囲も分ける。

既 runner python3 の実 executable/version/fullversion と venv probe を保存し、NumPy==2.5.1 を要求する。比較用 main Python3.13.15 との差を記帳し、版一致の場合も same_environment_as_main_run_claim=false。venv60秒/pip180秒/probe30秒の各 argv、raw stdout/stderr、start/end UTC、実 elapsed、exit/error/timeout/pid と raw pin を保存する。venv filesystem 全体を upload したとは主張しない。実 work path と setup/pip/probe の全記録を保存し、fixture/venv の cleanup は行わない。

P の依存連鎖 P→L→E→oracle→refinement/fixed→materializer/base/descriptors→ARITH を静読した。fixed.dependencies は selftest の時も既 DATA_PINS 2件を全hashするので、P＋自系 Python9＋raw2＋WF の exact13件を起動前・P直前・終了後に全pinする。raw2 は scratchpad/fuda1_a0_rmax_data.g =4709/625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba、scratchpad/a0_paper_words_v1.json =115928/90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893。これは既読取依存の外側保存であり、数学や親を追加しない。さらに外側4件を前後全pinする。初期登録16件と raw2追補の全18入力も author 票で前後一致した。

F5. Task1128 指定の実1126受領所見に従い、workflow copy は source-copy/workflow/gap-run.yml に保存する。元 .github/workflows/gap-run.yml という repo path は descriptor に残す。その他は source-copy/repository/<original>。source-copy-receipt が全17件の original descriptor / artifact_file / copy_pin を結び、全 file 名に隠し path 成分がないことを要求する。workflow の原文 13309 B / 0c2ba9089d7e43d9d34d43afa039618a354307037ddf9ea332535e43a70cecae 自体は変更しない。

fixture には旧群が意図的に作る隠し pending path もあるため、transport copy は非隠し files/<ordinal>.bin と原nameの全 map を用いた。selftest-fixtures.zip の中では元の全 file、root と全 directory の明示 entry、空 directory を保持する。元fixtureの全EOF/SHA、copy全bytes、ZIP全entryの型/size/EOF/SHAと zipfile の CRC 読取、終了後の元fixture/copy/ZIP を照合する。独立 CRC 実装とは呼ばない。P nonzero/UNKNOWN/timeout/文法不正の前にも保全を試み、NOT_CREATED と FAIL と PASS_FULL_BYTES を区別する。保全不完全や未形成を selftest PASS にしない。actual child exit3/UNKNOWN_RESOURCE は原stdout/stderr/終了票に残し、外側 status=FAIL は外側成功条件の不成立を意味する。

F6. root が指摘した「全 .json の strict 読取が旧陰性 fixture と衝突しないか」を P の活性 writer へ結んだ。最終 P-fixture-JSON-grammar-closure-v3.json は 52817 B / a27876a76d52c6a75283498c055fc7ba5e583817a46702b720634cd02e9b5671。17 source raw範囲と、明示した lexical pattern による活性 selftest 全73 write/ensure点を保存した。分類は direct canonical57、binary .bin12、phase builder2、canonical reduction raw-copy1、切詰め .u8 1、未分類0。

truncated-last-residual が切り詰める実名は chord-residuals.u8。mutation.json と更新 manifest は canonical。early-eof は input.json の eof:false。dependent-nonnull-lead も reduction/telemetry/manifest の canonical 再形成である。登録/旧schema/ordinal/bool/hash/役割/祖先/固定参照/誤bytes-key は semantic invalid な JSON。全活性経路に duplicate-key、nonfinite literal、truncated JSON を意図した .json 保存はない。これは既に生成した実fixtureの観測ではなく、実 key 起源と writer に限定した静的結論である。dict 一般や json.dumps 単体が重複 key を防ぐという一般化はしていない。外側の全JSON grammar loop は P exit0/完全PASS/全群照合後だけなので、失敗途中の断片にこの前提を課さない。P/外側 source の追加修理は不要だった。

全新 consumer は public-consumer-contract-closure-v2.json（11273 B / bab682fab14592dbedc1b0d795d6a0e38ea91f66ed49828a700b8f800fb64260）の K01–K16 に root/path/schema/key/type/merge/失敗枝で閉じた。範囲は新公開外側であり、P全プログラム数学の新証明ではない。public-outer-receipts-v2.json（17451 B / 55ed0b4f0b8fd54d66c9b364ab28f1aabd25b4d04329a868ac822db0c4180a13）には正常/未形成/失敗の各 keyset と、REPORT・fixture・第五group・ZIP の path基準を載せた。

F7. root 用 root-dispatch-and-reception-plan-v2.json は 8180 B / 62fec7f43e1e784b11bd39754641b01aa7490b80dbfafe4df7c8e7356dc48c90。既 gap-run.yml の workflow_dispatch に script=search/d972_r07_P6_public_selftest_gha_v1.g、preamble空、out_dir=ci/out/task1128、timeout_min=20、with_pquot_packages=false を使う。optional pquot工程と旧A0 artifact工程はこの stem/入力では実行されない。子は固定dispatch環境と workflow_dispatch event を照合する。新 commit/run/artifact は null のまま。root による将来の実値で結び、過去失敗・C selftest・未生成API値から推測しない。

root は actual run/head/workflow/全source/全artifact byte受領へ次の4 markerと型付き実票を全件結ぶ。GAP の zero は単独の P 成功判定ではない。

- TASK1128_GAP_PROCESS_STATUS=0
- TASK1128_GAP_FINAL PROCESS_ZERO_ROOT_RECEIPT_REVIEW_REQUIRED
- TASK1128_SHELL_FINAL returncode=0 reason=outer-returned
- TASK1128_OUTER_FINAL status=PASS_SELFTEST_ONLY

この4件に加え、shell/end/P実終了、正しい argv/resource/runtime、P全result/61拒否/第五ledger、全13＋4 source前後、非隠しcopyと全fixture/明示dirZIPが必要。全体job中断で票が足りなければ未完了である。将来通過した場合の主張も PASS_SELFTEST_ONLY、mathematical_parent_admission=false、full_run=false、candidate=false、cross_checked=false、verified=false に限定する。

F8. 作者は最終 .g17行/.sh56行/.py601行を全文静読した。whole-raw-transport-delta-v1.json（181292 B / 9c3ebbee04703807b81d1bac4163c5e2660bb06846077b236e8a95667c46eaac）と whole-raw-transport-diff-v1.txt（123310 B / c137dc2a05c16871cd0b2017d7c27a58bf2be588089394c12416a2cc82dec358）は、公開旧 transport 4file の全byte範囲を被覆する。Python は20→23区間、raw不変11・変更9・追加3・削除0。g/sh/json は各全fileの差分で、全4fileの forward/reverse raw 再構成が一致した。C数学の本文共有や共通helper導入ではない。

author-static-closure-v1.json は 33259 B / 04427de636ac800ad98252d9e148c8b37d20d39c1a5f69f5d3d6aad74f796916。全入力pin、public wire同値、source37 interfaceとscope、61 label、実8 tupleの正負path、例外prefix、bootstrap全pin、None/False をmetadataだけで照合した。build用 .ps1 は ASCII。設定保存の一度の CreateProcess206 は Windows command長による開始前拒否で、実source/子processは起動せず、既ABIを読む短いPS保存へ切替えた。静的票の途中版は保護し、consumer v2、JSON grammar v3、outer receipt v2、dispatch v2を最終とする。

全材料は同 task1128/final-static-delivery-v1.json へ全bytes/SHAで列挙する。manifest自身の循環pinは含めず、本返信を含める。snapshot4raw、P/旧source/旧workflow/旧1122成果は凍結保持。現時点で実P selftest、実環境/費用/fixture pin、root最終artifact受領はいずれも未観測である。

TASK1128_VERDICT: STATIC_PROPOSAL_READY_RUNTIME_PENDING; P_SOURCE_UNCHANGED; WORKFLOW_UNCHANGED; ALL_PUBLIC_OUTER_CONSUMERS_CLOSED_STATIC; SELFTEST_EXECUTION_0; GHA_0; PARENT_ADMISSION_FALSE; CROSS_CHECKED_FALSE; VERIFIED_FALSE

