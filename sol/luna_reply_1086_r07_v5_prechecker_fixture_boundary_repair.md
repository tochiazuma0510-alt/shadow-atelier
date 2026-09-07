# Task1086 — C未開始時の実fixture境界採取と v5 envelope-v2 限定修理

F0. 完成範囲。before-checker の実fixture比較を常時P後の post_producer 入口へ移し、execute(checker) の重複writerを除いた。P1085の正式 file_bytes 三literal修理の公開pin/rangeだけを current registry とWFへ結合した。最終本文は %TEMP%/shadow-atelier-audit163/task1086/review-snapshot-v3 で作者freeze、追加本文編集予定0。自作WF/driverの作者静的確認であり、独立別読はTask1087、実実行はroot GHAだけである。本便は配置/Git/GHAを行っていない。

F1. 実失敗と保持基点。run34143415388/1、head2751f8942a50377a13078cbf646cfaaa3845b71f、workflow352449001。本PはValueError:fixed_lambda_batch:next_batch_registered_inventory_exact_fields / exit1、本C未開始。保全の別findingは、C内だけのwriterが形成しなかった selftest-fixtures-before-checker.json を三票readerが要求したことだった。全32公開fileを実取得へ結んだ1084最終11336/836210f55118b8bea9823e97aa8fd29ca88362745219fa181e5a43ec68dfd658を凍結保持する。正常な旧fixture/archive票と欠名による保全FAILを区別し、旧R1の二固定参照票分離を変更しない。基点 driver_v1=1145254/f7181bc573c3aff041d6fff3520266ca401de6416b410d145c94aceaf3a18913、WF=26294/f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3、registry=499053/e30a6bde668f0778932f0c4fbd62752c698bd70b97e9b097dccde4e9348c2858。

F2. 通常経路の最小変更。旧driver7977–7978の if label == checker とその require(fixture_audit(before-checker)) の2行を除去。新driver8392–8393の post_producer の最初の命令で同じ実helper/同じstatus PASS要求/同じエラーlabel both-fixtures-whole-after-P-before-checkerを通す。削除141 B、追加110 B、合計−31 B/−1 LF。P exit、output形成、実execution票有無を読む前に採取するため、exit1/rejectedのみでもこの境界を実観測できる。fixture_audit本文とschema/fields、全P/C subtree比較、baseline/source/selftest/execution pin結合はraw不変である。

WF310–318はraw不変。P stepがskippedでなければbaselineはalwaysで呼び、Cはbootstrap success、baseline success、eligible=true、metadata/両selftest成功が揃った時だけ開始する。新requireでfixture不一致/欠品なら既存helperが形成できたFAIL/INCOMPLETE票を残してthrowし、eligible=trueは出ない。C成功もC開始も推定しない。post_producer後半は整数exit0または3・所定8file・全入力不変を従来通り要求するため、P exit1はC未開始のままである。C実行経路でもwriterはP後に一回だけで、C内の排他的save衝突は起きない構成となった。

新driver8643以降の check_fixture_preservation は全文raw不変で before-producer/before-checker/after-checker の三票、全baseline/全inventory、archive全entry/explicit directory/EOF/SHA/CRC読了票と実全fixture目録を要求する。before-producer writer、always after-checker/archive、preserve/final/run/全hidden diagnostics uploadも不変。P skipped・中間工程未到達・比較失敗・部分保存をPASSへ補う分岐はない。正常P、P exit1、実P receipt欠品、fixture不一致、P skippedの五経路は作者scope票に静的期待として記載し、実観測とは表示していない。

F3. 公開P結合。root受理の task1085/public-producer-source-and-ranges-v1.json=226557/261c0c6b39d8a600f041c0341181f78268db272efdb887430c7c144c058d34a6 を使用した。新P=366659/6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d、LF5536、元Pとの差は+15 B/0 LF。私的P/C本文をdecodeせず、元/新Pの全156 current範囲の全実byte offset/bytes/SHA/LF/EOFを公開票と旧registryへ照合した。155範囲同一、ordinal64 def next_batch_inventory_registration だけ1090→1105 B、SHA34b3f78dafc7252fc04bfa627d8931090fd6b019cdfd4fc5718c6204592114fe→270092a3aba2d65e903ed4363e33628b1d9e5a543d9cfcca7684d2b6cc8fef2e、line2081–2094は同じである。P37保持bodyは元/新の実opaque範囲と新registry line範囲を全一致確認、P旧4loaderも保持した。P私的算術の別人監査を本担当の成果へ補完しない。

current registry の実raw変更は source_files.P5 のbytes/SHAと当該一範囲のbytes/SHAを含む2行だけ。全raw逆置換で旧499053 Bへ一致、他の156比較分類、旧2registry、C全登録、57body、旧8loader、shared TCB/未測定call coverage、正式親inventory五keyは不変。元のtask1079/schema/headerは固定serializerの由来として保持し、今回修理の由来はTask1086外票で明示した。registry全rawをdriverのbr literalへ一意に埋め、INHERITANCE_REGISTRY_PINの新SHAを合わせた。bound driverからこの3行を戻した全rawは境界だけのab9d36ff版へ一致する。

F4. WFと全起動境界。WFの変更は name、push path内driver_v2、P bytes/SHA、WORKFLOW_DRIVER_FILE/bytes/SHA、job.if markerの計8行だけ。active path .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml は固定、name d972-r07-fixed-lambda-cycle-batch-v5-envelope-v2、marker [r07-fixed-lambda-cycle-batch-v5-envelope-v2-run]。WF最終414行を全読了した。bootstrap/終了時11本SHA・同GITHUB_WORKFLOW_REF・exact checkout SHA・コピー前後raw同一性・500000 B未満・bootstrap成功に限るdriver起動・終了時pin失敗のjob failure伝播は不変である。

作者の414行最終読みで中間v2のL170だけ旧markerが残ったことを検出し、root/1087へ先報した。1088担当も同点を報告した。中間review-snapshot-v2のWF26294/4d23faf8d37b35d8560e4a07a1811d9ee72c2127a22a7a3dd5e4674247f8e6a6を不変保存し、v3でmarker一literalだけ修理した。driver/registryはv2と全raw同一。marker-only-repair-v1.jsonはこの限定逆置換と新name/pathを記録する。旧markerのまま最終起動済みとはしない。

F5. 最終pin。以下はreview-snapshot-v3相対。全3本文はASCII/CR0/BOMなし/最終LF/行末空白0。

| file | bytes | SHA256 |
| --- | ---: | --- |
| driver.py | 1145223 | 238285767c62b0377d1192bd264233252870e0a5cfb9906a75035c0de2139573 |
| workflow.yml | 26294 | 3c20910e9fcce7cb8e05e234b7cbf8f1e329146a62613c6031dc8440d11431f7 |
| inheritance-registry.json | 499053 | 521978064705f784312482883d24b43e931675b8b05a20c62868146c3cec370c |
| final-opaque-registry-binding-v2.json | 71960 | ad8f4952686a7ff1e32bfd7ccc83d0506990bcae0413febb6b81c78703b6de48 |
| old-to-new-driver-all-raw-regions-v1.json | 38114 | cc03c7dfaac9b8ccecaed55f77499108b500b97c0286082f2f43fc41487470f6 |
| old-to-new-driver-full-diff-v1.txt | 1769 | f3b4715881460cabf6e1be1a6c59592bb2bd30f7fe56b3c82cc7ed848d655614 |
| old-to-new-workflow-full-diff-v1.txt | 1521 | 8e18b8f50649145e0c60c50b687776b90a97b51fdbe15c0eb06121fdf028de82 |
| old-to-new-registry-full-diff-v1.txt | 1041 | a37ef776ca74b942e6dd77b7534325e579422add1973e60dd9b606781bdaa0f1 |
| author-static-scope-v1.json | 3781 | 920585aa7f2f3ca6e936a053f4431e212734eea090fae80ce4edc28eb29dd637 |
| exact-five-path-proposal-v1.json | 2702 | d0938375031ddf03368091b5e77140b69d63fa240ed82405d7fa770da9359ba6 |

driver LF10038、WF LF414、registry LF2628。全driver EOF台帳は105 named def/class＋module-prefixの106区間、103同一/3変更（module-prefix、execute、post_producer）。先行連絡の「105区間」はnamed定義数であり、正本台帳はprefix込み106である。全forward/reverseで元/新driver全文bytes一致。driver全差分20行、WF全差分23行、registry全差分8行と境界→最終3行のbinding差分を全読了し、差分外の算術/fixture/content/列挙gateは不変と確認した。

F6. rootへのexact5path提案。旧archiveを先に全raw保存し、新driverを別pathに配置、その後同active P/WFの更新を行う親broker用の具体案である。TEMPのraw copy以外は実行していない。

| repository path | proposed raw |
| --- | --- |
| ops/source_versions/d972-r07-fixed-lambda-cycle-batch-v5-before-inventory-key-repair.py | snapshot previous-producer-before-inventory-key-repair.py =366644/664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66 |
| ops/workflow_versions/d972-r07-fixed-lambda-cycle-batch-v5-envelope-v1.yml | snapshot previous-workflow-envelope-v1.yml =26294/f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3 |
| search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v2.py | snapshot driver.py =1145223/238285767c62b0377d1192bd264233252870e0a5cfb9906a75035c0de2139573 |
| search/d972_r07_fixed_lambda_cycle_batch_v5.py | task1085/d972_r07_fixed_lambda_cycle_batch_v5.py =366659/6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d |
| .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml | snapshot workflow.yml =26294/3c20910e9fcce7cb8e05e234b7cbf8f1e329146a62613c6031dc8440d11431f7 |

旧driver_v1の現path/raw1145254/f7181bc5…とC5現path/raw336193/47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73を本便末尾にも実hashで確認した。旧P/WF archiveを新実行closure、親、TCBへ追加しない。registryはdriver埋込みrawであり、別repo payloadを増やさない。既存workflow id352449001は同pathの見込みを記帳し、次の実APIでrootが確定する。

F7. 保持と未実行。17親/実全入場、上流64・前層128・直前128・合計256、正式11648file/3525directory/file_bytes1308094050、8key acceptance、batch128/max_batches1/refill=false、全54433宇宙、P5400/C10800/outer6000/11400/RSS7168/job330minを保持。旧4 source・34 frozen blobs・三registryの歴史役割、P[30,10,6,7]/C[28,9,6,7]、metadata16、cost15key/6相/18context、R1二票・全fixture ZIP・全hidden/pending保存は不変。新test群/CLI/source算術は追加0、本便のAST/import/compile/Python/GAP/source/数学/受領器/GHA実行は0。静的な移設の成立を、新Pの全17実親通過・新選択・新C成功・新rankへ格上げしない。

F8. 全材料と別読。最終目録 final-material-manifest-v1.json =3148 B / b9772917983efc0b52bd173104180d67f6df47f2af726d0cf924ead8afc7b553。自身一件を明示除外し、全15 file /2413098 B、directories=[]、実在は目録込み16 fileを記録した。全15のactual bytes/SHA再読で不一致0。境界draft-v1、marker残留中間v2、最終v3を別に保持し、旧1079/1084/入力root/repo payloadを変更していない。1087へ最終3raw・全差分・全範囲・目録を直接配達し、1088へ公開pin/不変serializerだけを通知した。別読結果は1087の返信を正本とし、本作者票で先取りしない。rootの配置前通知・全pin照合・commit/push/実GHAが後続であり、追加確認や子の発射は行わない。

AUDIT_1086_VERDICT: AUTHOR_STATIC_REPAIR_COMPLETE; FINAL_V3_RAW_FROZEN; REAL_PRECHECKER_CAPTURE_MOVED_ONCE_WITH_ALL_THREE_COMPARISONS_REQUIRED; PUBLIC_P1085_AND_REGISTRY_PINS_BOUND; INDEPENDENT_REVIEW_1087_SEPARATE; RUNTIME_PENDING; NO_MATHEMATICAL_PROMOTION.
