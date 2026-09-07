# Task1086 — Luna: v5 C未開始時のfixture境界票と限定envelope v2修理

宛先: packet_bounds_audit。1084の現物診断を最終凍結後、本便を実行。返信 sol/luna_reply_1086_r07_v5_prechecker_fixture_boundary_repair.md、全材料は TEMP/shadow-atelier-audit163/task1086 の新file。旧1079 immutable版とrepo現物は触らない。rootが配置/Git/GHA/credential broker。子のGit/network/credential/Python/GAP/import/AST/compile/source実行、新agent、P/C私的body新規読取は禁止。公開source pin/range/serializerだけを使う。

基点 driver search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v1.py =1145254/f7181bc573c3aff041d6fff3520266ca401de6416b410d145c94aceaf3a18913、WF .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml =26294/f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3。実run34143415388/1/head2751f8942a50377a13078cbf646cfaaa3845b71f は本Pの登録key不一致でexit1、本C未開始。Task1085がP三literalだけを修理する。新source pinsと公開rangeは後着する。C5 336193/47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 は不変。

1084診断のWF別finding: check_fixture_preservation は before-producer/before-checker/after-checker の三票を無条件に要求するが、before-checker writer は execute('checker') にだけある。C未開始で missing selftest-fixtures-before-checker.json → ValueError:batch_workflow:JSON-regular-file となる。実after-checker票は always fixture_archive_mode が作る。これは実fixture改変を観測したという判定ではない。旧fixed-reference R1閉鎖を開き直さない。

最小修理の設計: P後C前の常時 post_producer 境界で before-checker fixture比較を一度作り、execute('checker')での重複排他的saveをなくす。execute('producer')のbefore-producer比較は保持する。移設の正確な位置と例外時の状態は作者が全dataflowで吟味する。C未開始でも形成済みfixtureの実不変性を比較できる一方、C開始/成功/完了を推定しない。Cが実行される経路ではその直前の同じ境界比較が必ず成立し、失敗時はCへ進まない。欠品をPASSへ変える分岐、三票要求の省略、alwaysで架空のC実行票作成は不可。型/schema/fields/fixture内容/countは保持する。

新driver basename d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v2.py、新WF name d972-r07-fixed-lambda-cycle-batch-v5-envelope-v2、marker [r07-fixed-lambda-cycle-batch-v5-envelope-v2-run] とする。既存active WFはrootが旧v1全rawを新archiveへ保存後に差し替える。P旧版もarchive保存する。新driverを別pathへ配置し、旧driver_v1.pyを残す。driver/selfpin/bootstrapの必要literalを更新し、旧四source/34 frozen blobs/三registryの歴史元、親17/全実入場/正本inventory五key、8key acceptance、128/no-refill、full宇宙、P5400/C10800/outer6000/11400/RSS7168/job330min/WF500000 B未満を保持する。

P1085三差分によるcurrent registryの公開range/pinとWF source pinだけを正しく更新。旧C、旧loader/body、oldraw registration、歴史二WF、旧v4 WF/driver、fixed-reference R1、cost入力/15key/6相/18context、作者分離を保持する。公刊registryの新旧EOF・全範囲・forward/reverseを提示する。bound P後着前はimmutable draft、後着後は別final snapshotと完全差分。全変更/新規bodyとWF全文、全pin、全変更箇所/意味、全材料目録を納品し、1087が独立別読する。

最終pin＋1087票＋marker/nameをrootが配置前expressへ通知し、研究者/2199/2207/2211の認可内で返答待ちせず再GHAする。run上限の追加確認は不要。実失敗は自己試験の偽陰性を含む診断として残し、静的修理を新数学成功へ格上げしない。最終行 AUDIT_1086_VERDICT:。
