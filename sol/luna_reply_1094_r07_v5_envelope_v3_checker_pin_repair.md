# Task1094 — envelope-v3 の C5 pin / registry 限定接続

F0. **C5 の公開 parent-reader 一式表現修理を、current registry・新 driver_v3・小 WF envelope-v3 に結んだ TEMP 具体案を完成した。driver の制御本文は変更していない。** 指定 `task1094/review-snapshot-v1` の固定材料を納品する。本便は driver/WF 作者の静的票であり、自案の独立監査済みとはしない。1091 の実診断票は 12707 B / d0aa3b7890bdf636b6813384c7a8c5cca4314983d2737a2bcba9fe292764371a で先に凍結した。C の全 consumer 監査1092と公開 schema 目録1093、root の最終全 pin、別人の WF/driver 別読、新 full fresh P/C GHA は本票と別の gate である。

F1. exact 五 path の案。次表の source は、C active 行だけ root 固定 `task1092/root-review-checker-v5-parent-selection-v2.py`、他四行は `task1094/review-snapshot-v1/` の全 raw 保存物に結ぶ。私による repo 配置は0。active C/WF は現在の旧 pin、残る新三 path は不在として観測し、root 専任の配置前再照合へ渡す。

| 配置予定 repo path | 提案 bytes / SHA256 | TEMP source / 役割 |
| --- | --- | --- |
| search/check_d972_r07_fixed_lambda_cycle_batch_v5.py | 336211 / 111e23bfe6a7b49b4b3a03a00f3b48345c3f75ab098f06efc18279e881555b19 | task1092 の root-review 固定 source、同 active path |
| search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v3.py | 1145223 / f1b50bc529f08ad8654d775e2fce652334dfa8b325d3d2bcc27286aa09cb3f98 | driver.py、新 versioned driver |
| .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml | 26294 / 3102f115c0d59d69d7ecc0b3941588b7fab5181e961b6399126a4e2516c4e969 | workflow.yml、同 active path の envelope-v3 |
| ops/source_versions/check-d972-r07-fixed-lambda-cycle-batch-v5-before-selection-key-repair.py | 336193 / 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 | previous-checker-before-selection-key-repair.py、旧 C 全 raw |
| ops/workflow_versions/d972-r07-fixed-lambda-cycle-batch-v5-envelope-v2.yml | 26294 / 3c20910e9fcce7cb8e05e234b7cbf8f1e329146a62613c6031dc8440d11431f7 | previous-workflow-envelope-v2.yml、旧 WF 全 raw |

`exact-five-path-proposal-v1.json` = 6821 B / 0d691fb6b8dffd0ba4e7b7b4cef91496867822068f53f6499109f6b9ec63ce8f に source 絶対 path、旧 destination 実 pin、不在、新 pin、非実行役割を記録した。旧 driver_v2 1145223 B / 238285767c62b0377d1192bd264233252870e0a5cfb9906a75035c0de2139573 と旧 driver_v1 は現 path/raw のまま保持する。新 archive 二 file は repo 履歴であり、実行21 Python+raw3 closure、親17、shared TCB へ追加しない。

F2. C 公開修理と opaque 範囲。Task1092 の公開 `checker-all-raw-regions-v1.json` = 127322 B / 124f79527b39ba05d56a015c9c4775b05802516b5058a0697df50602c1c9eece、`checker-old-loaders-and-retained-bodies-v1.json` = 23216 B / a9c2991cf4bd3d944e5326283d8088a85ea3781311e4ee3dd2103827193f2d10、`checker-single-expression-raw-delta-v1.json` = 1404 B / 767ebdc2ae25364e6c1b02bc40163e593f3a5ab96774783f7f906b6e424c8df5 を raw 保存した。旧 C と root 固定新 C を全 hash し、全140区間の LF境界/byte offset/bytes/SHA/EOF を再計測、139区間同一、ordinal66 `authenticate_next_batch_parent_metadata` だけ13635→13653 Bと確認した。後続 byte offset は+18、LF範囲は不変である。

公開 L1995 の一行だけを意味として読んだ。`same_json(selected["selection_lambda_sha256"], BATCH_PARENT_LAMBDA, "next_batch_old_oracle_is_native_lambda1578")` の参照先が `records["selection_start"]["selection_lambda_sha256"]` へ変わる。比較値と拒否 label は同じ、default/get/fallback を加えていない。offset144045で旧117 B→新135 Bの raw 置換を行うメモリ内 forward/reverse がそれぞれ全新 C / 全旧 C の SHA と一致した。`checker-expression-forward-reverse-v1.json` = 848 B / 866049d41a2605d78d4e6e1bc06a0388e89cdb9569849cb136e120b6a4a60b5a。C の私的数学本文を新たに読んだとはせず、他区間は opaque bytes としてだけ照合した。

F3. 三 registry の役割と最小 delta。新 current registry は 499053 B / 8792321d9cdcf25244726050928ae7fbd0cce5812e4f6867fa303ffcb49caa73。変わるのは L19 の C5 source bytes/SHA と L676 の current ordinal66 bytes/SHA の二行だけ。後者の新 raw SHA は d27a780a90627b8e7e641927706ed7a7bc0fd2082643f4ca023706491d4004f5。current の C baseline ranges と分類列は不変、P transition は全保持、他 source9件・他 top fields・全 parent inventory・new_source_audit の登録は全保持した。LF位置を用いる registry には後続 byte offset の字段がないため、架空字段を追加せず、作者 offset との照合票で+18を記録している。

| driver に埋め込まれた raw registry | bytes / SHA256 | 本便での扱い |
| --- | --- | --- |
| HISTORICAL_REGISTRY_RAW | 76867 / 9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38 | v1–v3 歴史6source/60range、全 raw 不変 |
| PREVIOUS_REGISTRY_RAW | 236390 / 84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114 | 旧 v4 親の歴史登録、全 raw 不変 |
| INHERITANCE_REGISTRY_RAW | 499053 / 8792321d9cdcf25244726050928ae7fbd0cce5812e4f6867fa303ffcb49caa73 | 現 v5 source/transition の二行だけ更新 |

`three-registry-roles-and-retention-v1.json` = 4929 B / 385d142356390c5943789948b4a0eb64fa50035d9b8326fdad7a343a78b35b39 に三 raw 実値と不変範囲を保存した。P37+C20 の保持 body と旧8 loader は、実 P3/P4/P5/C3/C4/新C5 の六 source から LF単位の raw SHA/bytes を直接照合して全65結合が同一。`all-57-bodies-and-eight-loader-opaque-joins-v1.json` = 67357 B / 6ee19d48df3204764924bd7e239af9f7a2eb89601e201d6634adca81c62c05a7。wrapper/roots の既存 root 私的監査への依拠、CURRENT_RUN call coverage=NOT_MEASURED、共有 TCB と独立性の既存留保は保持する。

F4. driver/WF 全差分。driver は L2852（C5 whole pin）/L3509（current C reader range）/L5463（current registry 全SHA）の三行だけ変更した。全106 EOF区間のうち module-prefix のみ異なり、105 named body は全raw同一。`old-to-new-driver-all-raw-regions-v1.json` = 108220 B / 10bd7f37ebf7c2c37655211a47583c7175f542d74ca3e5426a9f25eb1f80b284、`all-changed-lines-and-full-raw-reconstruction-v1.json` = 9338 B / c3fa44b3f3b4a451e6ca6e43980d4b48183435b052779c5c85787a00497573cb。全 driver/WF/registry の changed lines によるメモリ内 forward/reverse はそれぞれ全 bytes/SHA に一致した。

全 WF 414 行を全文読了した。変更は L2 name、L11 push path、新 C pin の L145–146、新 driver path/SHA の L150/L152、L170 marker の七行。name は d972-r07-fixed-lambda-cycle-batch-v5-envelope-v3、marker は [r07-fixed-lambda-cycle-batch-v5-envelope-v3-run]。active WF path と v5 公開 schema、artifact 名は保持する。driver 10038 LF / WF414 LF / current registry2628 LF、いずれも ASCII、CR0、BOMなし、最終LFあり、行末空白0。WF26294 Bは既存の実起動前・終了時 `size < 500000` gateを満たす具体サイズである。

| 全差分 file | bytes / SHA256 |
| --- | --- |
| old-to-new-driver-py-full-diff-v1.txt | 1367 / 9d0c408b555aabe341804c963af46cff2257bdedb6e3f76730b7aa467e688e7f |
| old-to-new-workflow-yml-full-diff-v1.txt | 1485 / 0020b9c0ced18688b5eeb870016c7e2f7a28f4ff82fd82d08bf2787449fc2de0 |
| old-to-new-inheritance-registry-json-full-diff-v1.txt | 1057 / cea918e6420759306b2aacb994e3fe84372126d40ef9477404da9250f1afe790 |

F5. P の literal 連鎖と新旧 code binding。現 P5 は366659 B / 6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99dで全raw不変。旧 C5 の full SHA literal と bytes literal336193を P 内の metadata文字列として検索した結果は双方0件であり、この pin の literal 連鎖による P 修理は見つけていない。P 私的数学の追加意味監査は行っていない。driver `code_contract` L5689–5696 は WF の C file/bytes/SHA を読み、source capture、source入場、current registry、acceptance、execution、before/after保全へ同じ値を渡す。code_union は既存21 Python+raw3 の24 unique fileを要求する。P/C file path は v5 active のまま、歴史 C4 と新 C5 を改名して混同しない。`public-C-registry-binding-v1.json` = 134996 B / 3a3c653d7acece4473b84a2cbb36545a4813f473822c38ea3d53ff0d30db330d に全 C raw/LF接続と P 検索範囲を記帳した。

F6. 保持する通常条件。旧17親全 tuple、正式 rank1706/gen8411、旧64 completed、previous128/immediate128/total256、353祖先、native pairing三層1450/1578/1706、八 key acceptance、batch128/max_batches1/refill=false は不変。P 5400/外6000秒、C 10800/外11400秒、双方7168 MiB、job330分、metadata16、P[30,10,6,7]/C[28,9,6,7]、fresh selftest-root と full fixture 保存を保持した。新 selftest 群は0。

1086 の post_producer 先頭 L8393 による before-checker 票形成と require、旧 execute(checker) に重複 writer がないこと、三 fixture 比較票の厳密要求は105本文の不変に含まれる。WF baseline success＋eligible だけが C を通す。bootstrap成功を全後段driver実行の条件にする既存境界、source/driver/11 SHA行の起動前後結合、失敗時も常時cost/fixture全ZIP再読/保全/診断uploadを行う経路、finalのactual C exit0と完全結果・HEAD・保全への結合も保持する。continue-on-error の外側表示を actual success へ変換する緩和は加えていない。失敗run34148667863のP出力を新親・cacheへ再利用しない。

F7. 凍結材料。`%TEMP%/shadow-atelier-audit163/task1094/review-snapshot-v1/final-material-manifest-v1.json` = 5730 B / ccc7d163c9137999da0364cd7322671ba25d59a4cb4ba6c24ce4743d6ff36dcc。selfを除く19 file /2532477 Bと、self除外を明示した。`author-static-scope-v1.json` = 11060 B / b8ca27f7ec0d5af71a570962919c079cf8c0ede5f524364a1d8b59ee71f90709 は全core pin/形式/retained controls/未実行を記録する。目録作成時の ordered-map に対する Measure-Object 集計は property非対応で一度停止したが、source/core は既に保存済みで不変、file.Length の明示加算に直して目録だけを初回保存した。数学・source処理の失敗ではない。

F8. 作者判定と残る別 gate。TEMP案の登録差分は静的に閉じた。Git/network/credentials、repo source配置、Python/AST/import/compile/source/helper実行、selftest、本GHA、親/fixture/既走receiver変更は全て0。1092/1093 の未解決 consumer を本 envelope 票だけで閉じず、別人の driver/WF 別読や新 C 完走を先取りしない。新 run/head/artifact と新正式数値は null/未観測。root の全pin・公開目録・別読・配置前expressを経て、同じ正式1706親から fresh P/C を実行する具体案として渡す。

AUDIT_1094_VERDICT: AUTHOR_STATIC_ENVELOPE_C_PIN_REPAIR_COMPLETE_INDEPENDENT_REVIEW_AND_RUNTIME_PENDING
