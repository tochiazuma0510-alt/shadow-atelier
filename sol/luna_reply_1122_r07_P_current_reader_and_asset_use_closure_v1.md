# Task1122 — P current reader と asset 用途の限定閉包

**F1 — 本便の完了範囲。** 1116 の C01–C16 を一件も削らず、caller・実 alias・引数原点・全返値 shape・次 consumer・whole hash/比較・mutation・拒否/停止枝を source-static に具体化した。14 資産群、9 主要返値、54 種別付き辺、旧 D01–D22 と O01–O12 の全対応を保存し、残る前提を U01–U11 として明示した。これは固定 source と列挙 ordinary 条件下での用途調査の完了であり、最小 active 集合、hidden input 不在、全推移グラフの十分性、Γ、引用 cut、変換、B、TCB、性能の完成ではない。

正式出発点は run34161493396/1、head a5b456a973f8a917f3af386d327061a02a0cf900、1834/8539 cross-checked limited7、verified=false。P6 は 453749 B /75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7 で不変。実源 L586 の inventory=None、L588 の IMPLEMENTATION_COMPLETE=False、L5611 の入口拒否も保持している。従って本便の ordinary trace は既委嘱の正式 final binding と入場が成立した後の条件付き経路であり、現凍結草案がこの入口を通過したという実績ではない。正式 inventory 到着時は Task1109 final binding を優先する。本便による v6 追加 gate は 0。

**F2 — 入力登録・読了の正確な範囲。** 最初の 42 入力を input-preregistration-v1.json に固定し、その後は登録 source の具体 call/import が指す既存 repo source だけを読む前に追加登録した。P6→l→e→oracle→refinement→p2→m/descriptors→base→ARITH の自系 10 source を全文 pin へ結んだ。C private source/返値票/実装案は読んでいない。元1113/1116/1118/1120 の限定採択と public1115 proposed.v2＋read_scope v3 を継承し、root の公開条件付き補題 7382 B /2cf2ff22f95f13b479cf126aa2a41192d29b42dcddb0599418b6d6705e3e89d6 も事前に別登録して全文読了した。

原文候補は `(?m)^(?:(?<kind>def|class) (?<name>[A-Za-z_][A-Za-z_0-9]*)(?:\(|:))` という字句検索から作った 703 raw 区間である。定義/class の先頭から次の定義直前までなので、後置定数・空白を含む区間もある。AST ではない。継続中に本文を読んだ関数/class は 141、最終二表の実参照は重複除去 123 区間で、その全本文を読了した。残る 562 区間は「本便で全本文読了とは宣言しない」と個別台帳に残した。既便での読了や部分原文読取りがある場合も、703 全件を新たな意味読了/全数学閉包と数えていない。全 10 source/703 raw 範囲の offset/bytes/SHA と、42 登録入力の全現在 pin は最終 PS metadata 照合で一致した。大きな native instruction stream・packed/vector・新 artifact 本体へ読取範囲は広げなかった。

**F3 — 16 caller 全対応の主要な帰結。**

| unit | 今回閉じた用途の具体化 |
|---|---|
| C01 | exact18 roots の全 file/dir before/after、acceptance 全 SHA、code union、finish_inputs の実返値を分離。返値を呼出元が無視しても入力保全と write_once/拒否は実作用 |
| C02 | 自系 module tuple と nested base.ARITH、check_deadline/progress 再束縛・sys.path/sys.modules/LOADED_ORACLE を追跡。全文 filepin は実 loaded object/外部 runtime の同定証明とは別 |
| C03 | old14 boot の state/anchor start/owner/oracle/E/P1/Task554/maps/index 返値を全列挙。元8059 rolling の whole read 後の pivot6-field 射影、seed/packet/refinement の ignored return と state mutation を保持 |
| C04 | old64 の実 snapshot は output/snapshots/000000..000063/start.json、9 phase/checkpoint。同じ ordinal の step manifest は別 output/steps/000001..000064/manifest.json。全 decode/hash と小 top 再構成は旧 solve の再実行ではない |
| C05 | step_manifest/checkpoint と native instruction/result/row/target を全 join して attach。返値 None でも rows/leads/head/target/λ/元97が後続へ変わる |
| C06 | Q1450 は全1450行と、external E を付加済みの元 continuation start target1386、および target1450。pre-E の e/output/start target と取り違えない |
| C07 | v3/v4/v5 の別3親の全metadata入場と18→historical17内部viewを明示。native source/roots/globals や元receiptを書き換える射影ではない |
| C08 | 三世代各128行の全返値7-field row item、candidate/new_parent、native rolling/target/plain-vs-packed SHA・zero/signを保持 |
| C09 | generic phase reader の JSON全parse/hash/optional seal と ordered source/lead 全比較を別用途にした。直接読まない literal key でも whole-object 用途は消えない |
| C10 | Q1578＝λ1578・全1578行・target1450/1578。元97＋128と full source/lead prefix、parent_intake/実query返値を追跡 |
| C11 | Q1706＝λ1706・全1706行・target1578/1706。元97＋256と別 local0、query/whole-result join を追跡 |
| C12 | current Q1834＝λ1834・全1834行・target1706/1834。元97＋384＝481を保持し、immutable selection と mutable new reduction state を分離 |
| C13 | current section→cochain/tree→raw→source→primal→correction→fourB→reduction の値・保存・restorer経由を分離。fresh builder と saved authentication を一律に「全演算再実行」としない |
| C14 | final の対象は intake current1834 target と実 final target。final_payloads の返値は (terminal,kind,payloads)。DERIVED は separator.json.lambda_rho2 内包で、独立 DERIVED file を仮定しない |
| C15 | current全保存・shared cached readers・一相 durable tail・committed HEAD・二診断・completed readonly を保持。same logical boundary の停止/拒否/後続mutationが対象 |
| C16 | 三親各772 checkpoint/1 invocation、旧public C/run/source等の whole join と今の実報告を分離。selection観測は committed sequence≥3、第一decisionは≥9、earlyはnull |

原固定 query1450/1578/1706 はそれぞれ別の採択引用候補であり、current1834/新finalと交換しない。現選択結果、採用数、未来1962、新λ、停止枝は予言しない。固定された旧3親は実各128採用という登録条件だが、これを accepted0/partial な別親を同じ reader が受理する一般契約へ広げない。将来設計では accepted0 層を消さず別 schema/domain で明示する。

**F4 — 最初の未列挙 asset 境界をどこまで解いたか。** 固定 16 payload と native manifest、参照だけの各 batch fixed manifest を区別した。既存 FixedBundle は manifest 存在を入口で要求するため basis_segments builder を通らない。base.validate_task554 自体も 5 state body を開かず descriptor を検査する。これを body 全体の「用途なし」へ拡張しない。現全親 inventory/hash、body→segment descriptor の来歴、他の現在 reader は別の用途である。

8 segment/12 blob は old4×lower/grade と new4×basis。実幅6056/72576/18144、row bytes1514/18144/4536、全2014＋6045行を保持する。FixedBundle が 12 stream を full pin して共有し、current section と primal は宣言された全 row を読む。primal は旧 embedded original lead 昇順、new owner-major original lead 昇順であり、係数0でも元 row/lead guard は残る。fresh primal の返値4key中、builderが直接保存するのは alpha/record と固定 residues だが、restorer が events/lower を回復して correction へ渡すため、record/hash/後続用途を落とさない。

P1 current section は全8059 cache、correction は nonzero alpha による selected cache/元instructionの正確な位置sliceと全indexを使う。correctionの roots は node 昇順、literal factors は primal event 順で別。subtract_lifts は selected が小さくても全12 lower blob を whole hash する。P1全instruction pin、selected line canonical/ancestry/origin/reductions/scale と roots/record wholehash が残る。

Task712 は各4characterについて B と4 actor T の forward/adjoint、計40 JSONL を受ける。新 q は forward B の sparse adjoint、fourB は4 forward B を使うが、T/adjoint の数値がこの二kernelで直接選ばれないことから全map readerの typedEOF/transpose/receipt用途を省かない。三rawは paper words、normalizer words、FUDA1 raw context。_SeedContext の words 引数は constructor で直接使わない一方、別 .g raw の lexical codecからcontextを作る。productionの codec表記を静読しただけで、この便では AST/数値実行をしていない。

以上を14資産・9返値表へ全 source pin/raw範囲付きで保存した。現 active whole-file 用途が一つでもあれば containing file を保持する。削除可能と証明できた file 集合は空であり、保守的な上界と最小閉包を同一視していない。

**F5 — 未閉鎖の正確な意味。** U01は既定 final binding、U02は実 module/runtime/resolver同定、U03はalias/cacheとその下のruntime作用、U04はnative全宇宙/旧相対transition、U05はP1 selected域とrole最小性、U06はΓ/数学的実現、U07はexact採択citation cut、U08はlogical境界対応、U09はavailability A/B、U10はconverter/CoreManifest/全元file射影、U11は実行/性能記帳である。各表に該当source範囲・既知事実・残る条件・ACTIVE_KEEPを記した。これは source不具合11件という票ではない。今回の固定源の用途読取りから追加必須source修理は見つけていない。

引用cutは同一native context/query/ordered input/採択source-runtime前件の命題を必要とする。返値以外のwholehash、入力不正拒否、欠品、alias、iterator、mutation、prefixの辺を未説明のまま消せない。元97（32五key＋65六key）と384十key、旧8059、native multi-row と後続one-rowは別の前提である。静的caller表だけでこれらのΓや原rho2直接算術、positive/eleven-slotを閉じない。Task1111の別数学監査を代行しない。

**F6 — 公開契約・資源境界。** 相手へ返す公開本文は public-current-observable-contract-v1.md の定義/入力role/三分法だけとし、private source caller 表と分離した。root補題の条件付き保存は両実行が対応する logical boundary に到達した場合の意味である。引用で費用が変われば同じcap/walltimeで同じordinalに到達する保証はない。実時刻、資源中断、実checked件数、実availabilityはそのrunから報告し、片側 UNKNOWN_RESOURCE を他側の完成PASSへ移さない。

Aは登録全COLDのEOF/全raw SHA。Bは既全復元、個別に採択したimmutable generation TCB、今の全object存在/正確長さを前提にする別方針。元path/空dirのlogical復元と実展開・全hashは別命題。今回は変換artifact、CoreManifest、B、storageTCB、cold省略、性能効果を採択も実装もしていない。既包括GHA認可を維持し、各試行ごとの新user許可要件は加えない。

**F7 — 作者照合・版履歴。** source-body-read-coverage と author-static-closure はPS/.NET metadataだけで作った。全C16/D22/O12、現A14/K9/U11、辺54、全参照元/先ID、whole source/raw範囲を結合した。初回単一保存は Windows CreateProcess error206（command長）でprocess開始前に拒否されたため、4小票の CreateNew とmetadata結合へ分割した。metadata照合PS初版の末尾余分括弧はparse段階で本文未実行、新v2で一箇所を訂正して正常完了した。旧script/途中票は全て残し、source実行やapproval待ちは発生していない。

作者票の自己訂正も全旧版を保持した。caller v2で final tuple/実file/target、v3でold64 snapshot/step pathとpost-E continuation-start target、v4で実check_deadline関数再束縛を正確化。asset正本v2は実args root名に合わせた。body-read v1の略名filter_actorは実filtered_actor_sourceへv2で訂正した。これらは metadata文章の修理で、凍結source変更ではない。正本は下表の版だけである。

| 正本（task1122相対） | bytes | SHA256 |
|---|---:|---|
| private-caller-return-use-closure-v4.json | 124876 | d0c116efdf5d581a161309f673d47488ca5ef0e4bc61513803af2098a18e2660 |
| private-assets-and-named-returns-v2.json | 153181 | 06a0b878958671b3c9e678b4aa080480a0ec4d502fe0cd97ff05db39117b229c |
| typed-source-asset-edges-v1.json | 11306 | 163eb79602999114f6730e0d21eea9ea981845e4f33b8e9cc42757e598b9ee03 |
| open-obligations-v1.json | 9667 | 3bea5d5ccfe6de795883044f8e197c2aa76d2774141a10cc23740e67717d9d6a |
| full-prior-unit-and-open-delta-v1.json | 10471 | 3b0d7799ec69989f15cc17112d4f82121411ef474603c10615ee5fbd09f6c682 |
| public-current-observable-contract-v1.md | 6996 | 70dad89029179318dcb5df07e2993c505d4dcee69d9691a1b0f3ec4fc917cc5a |
| source-body-read-coverage-v1.json | 446928 | 58c8732bf7b62301529aeb5f20cf0b7b06af5a6dca1b6615342c7943e35763f5 |
| source-text-region-index-v1.json | 471232 | 56b383d2f82dfe3093f1af0ccf3531ce5575ce413dcb7a31ab4f59c6802bd37f |
| author-static-closure-v1.json | 34171 | 191db4baf2a6342e80b1b80d16b29c9ef700b005362a44ba38fbebb0ac241612 |

**F8 — 納品と不変境界。** 全材料は %TEMP%/shadow-atelier-audit163/task1122/、完全目録は final-design-delivery-v1.json。38 TEMP材料と本返信の全39実fileをbytes/SHAへ結び、途中版を含め保存する。目録自身の全pinは循環を避けて配達通知へ置く。書込は本返信と新task1122材料のみ。元source/既入力/親/root/guard変更0、C private読取0、Python/GAP/Lean/source/import/AST/compile/selftest/数学実行0、全artifact再走査0、新agent0、Git/GHA/network/credential0、既process操作0。PSで実行したのは原文索引・metadata登録・全pin/range/参照照合のみ。将来義務を未完のまま隠さず、今回のbounded用途設計をここで凍結する。

TASK1122_VERDICT: BOUNDED_SOURCE_STATIC_PURPOSE_CLOSURE_WITH_EXPLICIT_OPEN; C16/A14/K9/E54/D22; SOURCE_UNCHANGED; NO_MATH_OR_SOURCE_EXECUTION; CITATION_GAMMA_TCB_AVAILABILITY_PERFORMANCE_OPEN; V6_ADDITIONAL_GATE_0
