# Task1092 — C5 親 selection キー修理と公開 consumer 契約目録

**F0 — 結論と射程。** C5 の L1995 を一式だけ修理し、公開 key／path／schema／型の限定静的 gate を閉じた。新 C は `336211 B / 111e23bfe6a7b49b4b3a03a00f3b48345c3f75ab098f06efc18279e881555b19`、LF4646／CR0／ASCII／BOMなし／最終LF。保存先は `%TEMP%/shadow-atelier-audit163/task1092/search/check_d972_r07_fixed_lambda_cycle_batch_v5.py` と同 bytes の `root-review-checker-v5-parent-selection-v2.py`。作業ツリーの実 source は旧 `336193 / 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73` のまま。新 source の配置・実行・数学的受理を本票で行ったとはしない。

**F1 — 委嘱と実停止の区別。** Task1092、裁定2217 snapshot、指定 express を全文読了した。実 `run34148667863/1 / head3e7e1ccf1996dad15b9019de849cf61548c654d1` は failure。C の保存 reason は `KeyError selection_lambda_sha256`、traceback は未観測であるため、L1995 を発生点とする判断は実字段欠落と通常呼出順からの静的推定として保持する。root が全取得した diagnostics の公開 JSON は読取専用で使用した。取得票 `707 / 6ca0249065af61354fcaa6cb29e37c1bae9ddb8c585baaed4160bdf57a8442e6`、全entry票 `2158818 / 6d53611209db05270e77dfec32a0a1a44c0fe950f20f0658c9b7aca65010097e` は root handoff の同成果を指す。P の今回出力値は未採択であり、正式 **1706／8411** を維持する。別便の旧 v3 空 directory／旧受領器の停止を本修理へ混ぜていない。

**F2 — 一式だけの修理。** 旧式 `selected["selection_lambda_sha256"]` を、新式 `records["selection_start"]["selection_lambda_sha256"]` に置換した。比較相手 `BATCH_PARENT_LAMBDA` と label `next_batch_old_oracle_is_native_lambda1578` はそのままであり、比較の削除、`.get`／default の追加、親や P の字段追加はない。実旧 v4 の `output/selection/selection.json` は `30909 / 181c87b906b2908e8d9d00e29faabf66bff673340e338bf18775e95150c3b4ab`、top27字段に当該 key はない。正しい参照先 `output/selection/start.json` は `1038 / 00a6c7e54fa99b1e0d9c390005b02a0972785f2a3b576bb348cc3bb166ce7e2a`、schema `d972.r07.fixed-lambda-cycle-batch.v4.selection-start`、当該 string 値は `6a0fe9368f2ec7f28c4d8076e7d3184fb57322b9d0905a8e7c3c26b467bcee4e`。同旧親の `output/start.json = 119074 / 9ee29d5af385f5cb4b884a441237d27d302e17a1d0c15099bc62ea4001008e25` にも同値がある。

**F3 — 元 path から λ 比較までの接続。** `authenticate_next_batch_parent_metadata` は L1871 で第17親 `batch-parent-v4` の tree を取り、L1874–1887 で登録 entry の全file pin、18 path 表と16 JSON suffix 表、canonical JSON／seal／v4 schema を経由して `records` を作る。`target` と `lambda` の二 path は binary で、JSON の16件には混ぜない。L1976–1985 は owner／source／start の全file SHA、fixed manifest の全file SHA、selection-start の全file SHAを用い、selection-start 本文を owner／source／start／fixed に、selection 本文をその4値と selection-start の実 SHAへ結ぶ。head／result／checker／final の selection 参照も完成 selection の全file SHAへ結ぶ。修理した L1995 はこの同じ認証済み `records.selection_start` の string を読む。新旧六 JSON の実 top key／schema／型とこれらの等値接続を `actual-lambda-file-binding-v1.json` に保存した。ここでの旧 λ1578、新 v5 選択 λ1706 `d036e848c46b563a5b0f683fb94afcbc759dc4bc402c6db14c82b172ccc0a653`、P が今回返した新 terminal λ は別の来歴として扱った。

**F4 — 全機械候補と意味分類。** 全4646行の raw 文字列走査で、全 opening bracket2805を含む **4819候補** を保存した。内訳は literal subscript1755、literal dictionary key1614、dynamic bracket／構成候補1050、JSON input60、key iteration242、literal get22、key enumeration52、whole JSON比較19、dynamic get5。型注釈、配列添字、辞書構成、実JSONの読取を含む過大候補集合であり、regex 一致を意味網羅とは呼ばない。全140 raw領域の通常用途、全221 literal receiver群、多段 alias と46の具体 field／path 展開区間を手読したうえで、全候補IDを分類票へ対応した。

| 第17親／現 v5 の literal 群の分類 | 群数 | 閉じる境界 |
|---|---:|---|
| 直接の typed JSON alias | 87 | role／root／実path／schema／pointer／key／実型／source範囲 |
| 認証済み descriptor または登録定数 | 9 | file／bytes／SHA、source範囲、正式 inventory 五key |
| C 内部値または独立構成する期待文書 | 62 | 自系の構成元と公開出力 schema／全bytes比較先 |
| 多段 chain または literal container | 21 | records→元文書、descriptor→SHA、型注釈との区別 |
| 内部の認証済み index／adapter | 34 | path／role／binding／内部 slot、元JSONの別 alias |
| 元64 fixed の JSON descriptor | 5 | 実8-key manifest、16個の5-key descriptor、JSONだけ3-key射影 |
| opaque source 範囲 metadata | 3 | 登録 file／offset／bytes／SHA、数学本文の非共有 |

直接 alias87規則の実 key 不足は0。221群以外の literal候補862は、旧 metadata／TCB626、共通 typed入場104、自己試験fixture116、内部 control7、通常数値 helper9に分類した。後者の `complete_reduction_coefficients`／`literal_signs` は source上の配置が自己試験の直前でも、通常 production helper として記帳した。新第17親／現 v5 の候補を blanket dynamic-dataflow UNKNOWN に残していない。

root の最終所見により、A048 の再利用変数 `value` は別の per-use 追補で明示分割した。L2254–2255 の checkpoint 定義／`sequence` 読取は J075／v4.checkpoint だけへ、L2304–2331 の invocation 定義／その他の読取は J076／v4.invocation だけへ結ぶ。全18 source候補IDと行・column・offset・関数raw範囲を別schemaに対応し、L2312 の動的 `max_seconds/max_memory_mib` を展開した19 key使用を記録した。A048元行の実型 union 自体を per-use の根拠には使わない。checkpoint の同じ実objectはL2258のindexを通じてL2288–2290の全独立期待値／全file SHA比較へ進み、invocationはL2305–2308のexact23keyとその後の通常bindingへ進む。C sourceは変更していない。

**F5 — 動的 field の具体化。** 展開票は、旧 v4 HEAD の ordinary counts、selection の3つの失敗欄、16 JSON path alias、common5とcommon4の差、before／after×parents／codeの4fileと4hash、instruction rolling body の除外3字段、全 ordered row の `row_id/source/lead/coefficient`、候補 readout の6相、checkpointからprogressへの13字段、resultへのcommon4＋final14、diagnosticの nullable／形成済み分岐を具体的に列挙する。全 basis 係数列と typed row source の境界は変更しない。自己の `NEXT_BATCH_INVENTORY_REGISTRATION` は正式 `files/file_bytes/directories/files_sha256/directories_sha256` の五keyを読み、file descriptor の `bytes` と混同していない。全5 dynamic get は checkpoint／validated／complete／registered の内部 map であり、存在しない public JSON key を補う経路ではない。`files.expected.get(...).get("sha256")` も独立比較済み file descriptor の内部 index である。

**F6 — 新旧の公開型への合流。** root共有の P focus `45929 / b164fc478160df5e3d81b685f2738cbab94bc6074157056756295967601da4b9` と、bodyを除いた P public catalog projection `439405 / cf3fd457daf565bc412f4c9a172f9d0c381ba7eafa4d688d2d965febd3ce783e` を読んだ。後者の全59 path familyを、自系の手読28 schema keyset、実147文書／67 familyの key・型・full-file pinへ接続した。合流結果は **C自系exact object46、plain inventory array4、継承whole-bytes payload9**。59例の actual pin／schema／top key／top型は P公開票と一致し、自系exact46のtop key集合にも追加不一致はなかった。PS型表示の JSON-real と公開票の JSON-number は実JSON小数の表示名として対応させ、通常Cの ordinary integer gateやcanonical比較は変更していない。

実型票の `{ordinal}` は明示した0／127、phase票は登録された代表相、checkpoint／invocationは実在する一件として保存している。4513名／59テンプレートというPの目録を、4513全文を当方が再parseしたことや全 nested配列の意味を照合したことへ読み替えない。actualの欠ける `resource-stop.json`／`rejected.json`、Linearのnullable、CompleteZero、DEPENDENT、partial/durable-tailは、既公刊1077と継承997／1000／1001／1003／1004／1011の型および自系通常分岐へ結んだ schema-only 範囲である。存在しない actual fixture を作っていない。

**F7 — 全通常 consumer の読み口。** 現 v5 の直接 parse は、phase telemetry、progress HEAD／checkpoint、invocation、seq3以降のselection、seq9以降のcandidate0 manifest／reduction／witness、resultのelapsed／invocation参照、登録二diagnosticに限定される。他の root七文書、三selection相、各候補六相、witness／selection／view、row三payload／manifest、candidate manifest、final／physical HEAD、四入力目録、resultは、Cが作った期待値を `CandidateFiles.object/compare` で全file bytes／SHA／EOFへ結ぶ経路を追った。既存の expected-file size/hash gate の陰性はその入口で止まることを維持し、semantic outcome まで到達したという自己試験の昇格はしない。継承 E/O/L/C の数値内部を再証明せず、P数学本文・私的API・1093私的本文も読んでいない。現在の公開 key/path/schema/type 読取の未解決件は0であり、数値配列の全域意味や全プログラム数学を再証明したという意味ではない。

**F8 — 全raw保持と実行境界。** 全EOF140領域は139不変、変更は `authenticate_next_batch_parent_metadata` 一領域だけ。旧→新と新→旧の全bytes再構成が一致し、一式外も完全一致した。変化は +18 B／LF差0。旧4 loader と保持20 numeric／durable bodyは各全raw一致。17親、8-key受付、batch128／max_batches1／refill=false、旧宇宙、kernel、通常算術、既存四群 C[28,9,6,7] は不変。新試験0、Python／GAP／AST／import／compile／C/P/source／selftest／受領器実行0、性能試験0、Git／GHA／network／credential／既存process操作0。実施したものは許可された PowerShell／.NET の raw、JSON key/type、hash、文字列／範囲操作だけである。

**F9 — 最終材料。** 以下はすべて `%TEMP%/shadow-atelier-audit163/task1092/`。実行sourceはF0のpinで固定する。大きい候補票は自系source行を含むため、WF/P担当は最後の public票と公開raw範囲票を利用すれば足りる。

| 材料 | bytes | SHA256 |
|---|---:|---|
| `checker-all-lexical-json-key-candidates-v1.json` | 5319042 | `4f62e659fa50a41fe0dc45bbbad8d713cb6d2520bd5f3fb127c036eef23ee159` |
| `checker-all-consumer-semantic-classification-v2.json` | 7598325 | `4f5ae4b4c99c693b2d18b2a003e79c1693a1cc9c2aaf0eb1f486065df6c7197a` |
| `checker-direct-JSON-alias-key-bindings-draft1.json`（保存名のまま最終採用） | 394352 | `0d10a85e90e12c0bfa2c96d35b68477acfc4e7c7a724f9999cb935f6457db27a` |
| `checker-dynamic-field-expansions-v1.json` | 37660 | `04740b53cbfe82bd7d10eff07b57a1a713c4fd111a84200edad91452358d3d4e` |
| `checker-public-schema-keys-and-P-join-v2.json` | 366742 | `90e5fcb972a9810b23d2037aa9e0ad1c38b2178cf874e197a42795337b53f759` |
| `actual-public-json-family-shapes-v1.json` | 1866527 | `4e74f61a629c04ad594c5a172d075026a9771b56545c5ce5dbd48ca38f1fb57a` |
| `actual-lambda-file-binding-v1.json` | 68155 | `c9e7286fc453a9f7472d5408d491bfae6108402dfcdcb7ee957d4952d5d6ee0e` |
| `actual-original64-fixed-reference-schema-v1.json` | 26012 | `ee4184a6bd26c3d49eb0175aa430064c65e6f7489b8cd36a4057c3ca722fbd0a` |
| `checker-all-raw-regions-v1.json` | 127322 | `124f79527b39ba05d56a015c9c4775b05802516b5058a0697df50602c1c9eece` |
| `checker-old-loaders-and-retained-bodies-v1.json` | 23216 | `a9c2991cf4bd3d944e5326283d8088a85ea3781311e4ee3dd2103827193f2d10` |
| `checker-single-expression-raw-delta-v1.json` | 1404 | `767ebdc2ae25364e6c1b02bc40163e593f3a5ab96774783f7f906b6e424c8df5` |
| `checker-selection-key-full-diff-v1.txt` | 362 | `f67319e76971f244dd96a6d0423d5201c88c9a1d374a79c117eeca1732d9022d` |
| `checker-A048-per-use-schema-bindings-v1.json` | 77165 | `5a290d7ec6f7e55e1cf8b950b28e15fffd8f683f5979609a2fb734cf33c1feb9` |
| `public-checker-repair-and-key-contract-gate-v2.json` | 9388 | `d9c762f657df18be1212d8fe92feb10817dc7168a6ea605b395e8f593e6b779d` |
| `final-materials-before-reply-v2.json` | 10619 | `8351cb219a42dd65181da7a617b375c719df1b85eab907ea83e84f04199cf3a1` |

分類／schema-joinの旧v1 draftも保存しており、最終gateは上表v2とA048 per-use追補である。全28材料目録は旧段階の票を `SUPERSEDED_METADATA_DRAFT_RETAINED` と明示する。本返信の最終byte/hashは別の最終handback票で固定する。追加実装所見はなく、rootの別読・通知・配置と必要なGHA実走へ引き渡す。

AUDIT_1092_VERDICT: LIMITED_STATIC_C5_REPAIR_AND_PUBLIC_KEY_PATH_SCHEMA_TYPE_GATE_CLOSED; ONE_EXPRESSION_ONLY; UNRESOLVED_PUBLIC_READS_0; RUNTIME_UNEXECUTED; FORMAL_1706_8411_UNCHANGED.
