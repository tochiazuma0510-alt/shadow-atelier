# Task1191 — V10 第22親の登録と2293前件・設計/実装準備

宛先: 既存 Pauli(P) / Helmholtz(C) / Noether(public driver/WF)。Task1190 の自担当返信を先に固定してから開始する。研究者の GHA 継続認可、裁定2199 notify-and-go、裁定2293のV10準備承認に基づく。新run・git・network・credentialは親rootの単一brokerだけが扱う。最終sourceの配置/発射はroot全文別読と4者identity突合後。

## A. 全員共通の正本と凍結範囲

ops/express/20260913_fable_astra_2293_v9_accepted_rank2346_v10_premises.md と docs/notes/fixed_lambda_batch_v9_cv9_reading_v1.md を読む。後者の判読本文は LF正規化60883 B / 236fdc85b8a3572659f5a2bd20a133353aa5cb69017341b5768197bcb88fa310、2293追補を含む現全文61831 B / b0afe4a6f2b12733582baceedf333cedbabbde40042100bdf30403a4058494d4。今後の追補があれば本文prefixと全文を区別する。Sol の ops/express/20260913_astra_2292_2293_scope_errata_v1.md も適用する。

数学宇宙: 現ownerの vertices54432 / edges108864 / chords54433 / legality_rows5 / source_lower96776 / physical_lower32260 / physical48384 / p1_rows8059 / characters[0,1,2,3] / auxiliary_tests2。k128・max_batches1・no-refill。P内5400/外6000秒、C内10800/外11400秒、RSS7168MiB、各selftest内300/外360秒、job330分を保持。metadata固有300/300秒も保持。C4 raw・旧算術・著者分離・canonical/seal/EOF/UNKNOWN/partial/資源/再入場・sequence3/9を保持。対象sourceのローカル実行/import/AST/compile/selftest、embedded source archive decodeは禁止。

R = C:\Users\81905\AppData\Local\Temp\shadow-atelier-audit163。

第22親を末尾だけに追加: role batch-parent-v9、run34717506638/attempt1、head6b105348b2372a6b59de29904912172b5720e8ec、candidate artifact10306226977、429844909 B / 94da553a2b6c160e03611814a03a859b42af2c8406329ac9391c8c42261592ba。mirrorは既存 archive-gha-checkpoints。実root Q=R/run34717506638-reception-v1/candidate-all-v1。既21親は元順・元型・元bytesを全て保持する。

新親受理値: rank2346/gen9051、state_head fc1ac4d9057ef401de1740954cefa4c45d48ccfdbcffddfb59c8f5f8cae566ff、final lambda289190c37a1a564ec7f062677caad94d4a8dddccb1afee5cd7d117beaa438776、target96785516fc80ef49eb42a18fe3bc911b3084ff8a4e27fa161c6f8c325f8acdcd、previous target e1b34dfae07fd3eef337c1b1e444b05356615e3c43a8e97f5e0e5d90aeaeccce。fresh lambda2346 の oracle は未計算。新runの old 側は保存 lambda2218 の35647/index242/edge489。失敗数差は歴史比較だけ。

第22親のroot whole ZIP票2306/14d99237511f332a429464a04fe6940b3215cb3a0a33fbd29da144649752ae4d、inventory/source票21747/3d06f6f888364f210a9d860436e0886bd13f8054a985abf6022005c65b39dd99、全登録モデル2256957/34ebee5249dfc275693a0c595ce0497239c5f775c45cdf6c65ec21a32c091187。全12348 files1581230483 B/3679 dirs。formal5とroot最終数学票の実pinはrootが確定してから公開供給する。ここを仮の成功値・自己発行票で埋めない。設計と歴史値の分類は並行して進める。

## B. 派生値の独立導出

V10の現行7 native層から previous768 / total896 / initial rank2346 / initial generation9051 / previous ancestry865 / accepted ancestry993 / 7 invocations / 5376 phase manifests / 5404 checkpoints / pairing点[1450,1578,1706,1834,1962,2090,2218,2346]。current acceptance13 / start64 / intake81 / layout15が期待式から出る。単なるliteral置換にせず、Pは一つのpinned登録表、Cは独立和で導出して全consumerに結ぶ。

保存native-v9は21親・6層・640/768・2218/8923・865/737・73 intake/59 start/14 layout/12 acceptanceの意味を保持。V9で固定したnative-v7等のprefix viewも保持。V10 current値が保存nativeへ漏れないことをcaller全数表と否定例で示す。新batchは128独立を事前仮定しない。zero/dependent/positive/partial/resource/UNKNOWN/未測定nullを別結果として扱う。

## C. 今回必須の前件

F-v9-1: P WORKFLOW、C CHECKER_WORKFLOW、driver現在WF、物理WF path/実name/markerを配置前に静的突合。予定pathは以下で統一し、各final source D3は最後に実bytesから結ぶ。

- search/d972_r07_fixed_lambda_cycle_batch_v10.py
- search/check_d972_r07_fixed_lambda_cycle_batch_v10.py
- search/d972_r07_fixed_lambda_cycle_batch_v10_workflow_driver_v1.py
- .github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml
- name d972-r07-fixed-lambda-cycle-batch-v10-envelope-v1
- marker [r07-fixed-lambda-cycle-batch-v10-envelope-v1-run]

F-v9-3: P側の不足を回復する。V9歴史prefixの640/768と現checker identityに加え、V10現行768/896と現checker identityを各ordinary production consumer経由で試験する。旧8群は元順・元値で保持し、第9群を追加する設計とする。Pのproduction=True key否定1件を消さない。P/C双方が現行値のstale、旧namespaceの別名化、theta0祖先記録脱落、emptydir脱落、未計算oracle→0、schema/現checker取り違えを検出する。正例が通ることを先に確定し、目的の否定以外のseal/hash失敗を成功扱いしない。正確な群名・case名・条件・拒否label・件数・actual saved fixture fieldsを実装前の公開表に置く。

F-v9-4: 現行V10 batch_observationに old_side_recomputed_in_this_run:false を1フィールド追加する。P writer/C独立consumer/driver/public receiver/全copied JSONに閉じる。保存native-v9以下の既存schemaへ注入しない。old lambdaの追加oracle計算はしない。

F-v9-2: 著者宣言のD3はrun内で宣言内容を再読して認証するものではなく、root全文別読へ至るprovenanceであると明記する。bytes単調性を意味保存の代用にしない。rootは旧宣言→新宣言の全field/全raw差分とsource consumer連結を別読する。既存のsource実pin gateは保持する。

F-v9-5: shared-tcbにPの自己子プロセス起動と環境allowlist/同一source/同一registry/同一総deadlineの辺を記録する。共有算術kernel2本/4区間・NOT_MEASURED・第三独立性なしを保持する。

F-v9-7/8: 版番号依存の自己申告keyを増やさない設計案、現行WF自身のbootstrap bytes/SHA確認を、公開WF/driver変更表に含める。意味変更を伴う部分は先にSolへ具体的に提示する。

## D. 担当と納品

Pauli: Pのみ。返信 sol/luna_reply_1191_p_r07_v10_registered_parent_and_premises.md。
Helmholtz: Cのみ、P source/diff/fixture禁止。返信 sol/luna_reply_1191_c_r07_v10_registered_parent_and_premises.md。
Noether: 公開driver/WF/登録表・P/C opaque D3のみ。返信 sol/luna_reply_1191_public_r07_v10_registered_parent_and_premises.md。

新材料は R/task1191/<担当>/ に versioned/CreateNew。作業ツリーは各自の指定返信のみ。まず数学対象を実行しない有限設計表（前後規約、全caller、selftest否定例、scope/alias/identity）を固定し、rootへ小さく納品する。最終source実装の可否はSolのその設計表裁定に結ぶ。公開のexpected計数表は共有可だが、互いのprivate source/diff/fixtureを共有・参照しない。

## E. 2292 canonical重複の調査（並行する設計のみ）

自担当sourceの呼出先と計器窓を読んで、22663 canonical呼出/4773 json_read_callsの比が何を数えるかを同定する。P/Cを別々に扱い、recheck_raw_bytesがどのloads/IO操作に帰属するか、同一raw文書/同一parsed value/同一seal用projectionの重複を区別する。Pはcanonical呼出、Cは第2→第3層の168→11940 loops跳躍も調べる。出力はsource区間と回数式・未同定箇所であり、現在の実装は変えない。

重複除去で判定経路に触れる修理は、2293により別読+「修理前後の再導出一致」+明示承認が必要。今は具体案まで作り、承認が最終手順になるようレビュー可能にする。参考計測0.343194秒を新再構成の時間下界とは扱わない。V10の通常親追加・必須前件準備はこの最適化の採否を待たず進める。
