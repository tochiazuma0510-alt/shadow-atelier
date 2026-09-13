# Task1193 P — 最初の限定設計

Pauli。Task1193 と裁定2302の express を全文読み、自己 P10 の採用済み公開登録表・wire・byte 会計を基点に、最初の P 設計を固定した。root の追加指示に従い、1192 current/all9 の root 実受領と並行する設計だけである。V11 source 実装、対象／受領器の実行・import・AST・compile・selftest は 0。C 独立数表・私有 source/diff/fixture 本文は読んでいない。新 agent、Git/GHA/network/credentials の使用も 0。

R = `C:\Users\81905\AppData\Local\Temp\shadow-atelier-audit163`、T = `R/task1193/P`。変更は T の versioned JSON と本返信だけ。既存1191/1192の固定 source・公開票は保持した。

| T 内の設計票 | bytes | SHA256 |
|---|---:|---|
| public-P11-first-bounded-design-v1.json | 7519 | 917245f20f8a276462064cf91a451f2e34eb8d81b96c202ffcaabff57b6048c9 |
| public-P11-current-count-inputs-proposal-v1.json | 13234 | be2747fe98bfd884fc7b48a3b90e8bf842d42f5abc8a6290cce20a70199b7666 |
| public-P11-named-history-keyset-design-v1.json | 20954 | 63903aa1e1e49b6dda6b7fbbb2779b521c41c9d8f2459c0429f29bc91737f721 |
| public-P11-ordinary41-and-conditional74-order-design-v1.json | 7190 | 86164539522a45cbdeadad93170c57814d54f877cef4a9400749b7a441cb01b3 |
| public-P11-minimal-tenth14-cases-design-v1.json | 18147 | 27a5247298863ce6306d25a045b1d6a46d58ce8c9dbb7636d5367cee0a28d4ee |
| public-P11-byte-accounting-boundary-and-V10-reclassification-v1.json | 2130 | 08bd7608ab0384be5171e36be25a10b3a14cb3acfe6791cd3d3ee90704e9f41c |
| P1193-first-design-material-manifest-v1.json | 3205 | 10ec5bf5015f61773b5acc8bd00554dba4d25763d2a2ff638080e472bdc6c2e6 |

基点 P10 は1034265 B / `33c4bbb97313bc1ea2017b6ac6ad2cc0932ae15d1affc8bcd6a8aaedd0c76085`、自己登録表は12401 B / `6f92e487d6190ac36c00b40392a1082d9854032af4fbade4f2e30d9ad7126c00`。旧22 role と7層を順序・全値とも保持し、末尾に `batch-parent-v10` の128行層だけを追加する。P 自身の表からの導出は次のとおり。

| 量 | V11 current 案 | 保存 native V10 |
|---|---:|---:|
| 親／層 | 23／8 | 22／7 |
| previous／total parent rows | 896／1024 | 768／896 |
| previous／total ancestry | 993／1121 | 865／993 |
| phase／checkpoint／invocation | 6144／6176／8 | 5376／5404／7 |
| acceptance／start／intake／layout keys | 14／69／89／16 | 13／64／81／15 |
| 初期 rank／generation | 2474／9179 | 2346／9051 |

式は base physical1450・generation8155・ancestry32+65 に登録層の accepted_rows の和を足すもの。phase は1024×6、checkpoint はそれに8×4を加える。これは親として受理された状態と予定登録量の導出であり、未来の128成功を実測していない。

親は裁定2302の **run34731988156/1/head785bd2d87f2b97452a7f0deb2085afe4e7e56d95/state_head168d2cf1004ee6ace61fd082dedb21af41ff1047cf3a88482ed8170ad81786f9** だけ。artifact10310711557、448498707 B / `e5dabd802d8fe6d21ea67169e724e61239b5f1476a76648e981f05910d83d0d7`、mirror asset560455884 を登録予定とした。formal5 と親 header の最終 D3 は root 後供給の null。新選定 λ2474 は `e910b7b65d64b1450e2c9b8aad495488e34b643fc0c6f4a01af5b1a78abf4e36`、oracle は未計算 null。旧選定 λ2346 の保存35780/index435/edge847と混同しない。timing-only34735785100は親にしない。

F-v10-2 は6本の公開値を実 canonical JSON として REPORT に保存し、登録表の同じ値、全file D3、型と参照先へ結ぶ案である。原著者ファイルの raw D3 と canonical copy の D3 は区別する。順序は「旧親／count／history snapshot → P final → Pをopaque pinしたC final → 個別公開 wire・source採用leaf → registry → driver → WF・外部launch採用」。自己の完全SHAや未来のregistry/driver/WFを、その前段source採用leafへ埋めない。bytes増加やhex型だけを意味論の証拠としない。C wire の統合は Noether、C 数値の独立導出は C 著者の責務として保持する。

F-v10-8 は trusted schema 名で参照する世代別 snapshot 案とした。current keysets の正本は `current_count_inputs/current_exact_keys` に一つだけ置き、旧V9/V10の15文書 family は named history snapshot へ置く。`load_current_count_registry` が canonical snapshot pin を入場前に結び、通常 `native_v9_key_contract` と新 native-v10 helper が参照する。未信頼文書の schema だけで期待値を選ばない。数値 prefix view から旧fieldの存在を推論しない。旧V3〜V8の保持rawの全面移行はこの初稿で完了扱いにせず、必要なら実keyset／通常callerの有限名簿を別途示す。

追加群は14例案：V10/V11の4 keysetsの両方向8例、current896/1024とnative768/896の単値差替え4例、checker file名の両方向2例。各 positive keys/値、実変更値、case名、目的gateを票で分離した。通常の同一helperに正例を先に通し、正負generic seal確認、nonzero canonical delta、`fixed_lambda_batch:`＋目的gateの完全一致、前後raw保持を要求する。keyset置換で5／8 keysを落とす例を「1 keyだけの変異」とは呼ばない。型／key境界を試す例であり、full native算術入場の positive と主張しない。

第10群は既存第2 production=True 子の中で、旧29例の後に実施する設計。既存第1子と元の全体300秒 absolute deadline、16 optional＋2 required environment key境界、異常時の終了処置を保持し、第3子や追加時間枠を作らない。旧9群の順／件数／歴史payload／変異目的は保持し、current source/registry/transportに必要な束縛差分だけを明示する。旧第9群のV9/V10例は実親入場にも使う通常native V9/V10 viewへ接続し、selftest専用cloneにしない。新群は12 positive JSON＋14 negative＋14 rejection＋ledger＋scope＝42 files／17 dirs案、巨大header fixtureの新複製と新opaque payloadは0。正確なsidecar/writer/元子return接続は実装前の残り設計である。

計時は通常41本、条件付き全74本の予定順を全列挙した。auth/operation/ordered/parserは各8、finish_inputsは1。旧exact型、null/partial/FAILED/OBSERVER_ERROR、inclusiveと排他小計、first/unidentified/IO除外、unattributedを保持する。まだ実eventではない。CPU型記録や1回の再走から因果的な速度差が分かったとは主張せず、費用モデルの更新・外挿は行わない。

F-v10-9 の旧274051 B増分を実raw境界で再分類した。positive header literal156256、case table8651、残module metadata14947、通常reader67647、count/key/identity1682、子/canary22025、既存変更2843で総和274051。full assignment行のLF込み境界なので、第9群関係は186932 Bとなる。判読正本のAST expression/function境界による186871 Bとの差61 Bを明示し、総和の相違とはしない。V11もfixture本文／case表、production metadata定数、通常reader、child/canary、既存変更を互いに重ならないraw区間へ分け、空白・コメント・EOFの帰属を含めて正逆差分を作る。

V11四配置名とWF名／markerは設計票に記載した。発射前の identity5点は P WORKFLOW、独立供給C CHECKER_WORKFLOW、repo WF path、WF_FILE、実launch.workflowであり、root が実配置値で照合する。今回 final source pinや実行成功値は作っていない。

作業は公開 JSON／自己raw位置の有限 read/hash/byte会計と設計保存だけ。初回metadata writerはoptional stage列が無い箇所で停止したため、保存済み2票を保持し、元のcompletion-order行型をそのまま写す形で残りを保存した。対象計算や受領器の失敗ではない。全inputをfresh再pinした。root／Noetherへ上記pinを先行通知済み。Sol設計採用やF-v10-2/8の実装完了、V11発射可とは宣言しない。

追記：root の V10 正式受領と CV9 採用が実在票として到着した。`R/run34731988156-reception-v1/root-v10-formal-and-cv9-mathematical-adoption-v1.json` は1050634 B / `7385f32671c0742cc91df1ffbf1ca2097b3c80ee21f82445aa4863b2ebc8c4a4`、root 実行 `7cbc3e/session44911 → 63e82f`、native0。formal5 は同dirの `root-v10-formal-inventory5-v1.json`、229 B / `b2ead8b4b63e3ff76caa2ea1e98d6759bb7d38d619b5fa73bc009e108643536a`。実値は files12590／file_bytes1673885307／directories3744、files_sha256=`25ae0f13a07826877a7c41e9744c2251aad6e6ff1fb864b33e20b72c7cd68c5a`、directories_sha256=`a968226a73b22d0c23649f1e9c54092e9fd7d587ae9bb5ac073d490104f4627f`。初稿の未供給nullは履歴として保持し、次版でこの実値に束縛した。

root の追加委嘱どおり、旧1191の実公開header方式で次親を有限metadataとして生成した。数学sourceの実装・実行ではない。metadata author helper `T/author_P11_actual_parent_header_metadata_v1.py` は18753 B / `6c7ff65e69322a344fa7eea467ebbfff7dd7dbda794f4ef7d0e695ce5636fc91`、ASCII297LF。author metadata処理 `47dc10/native0` で以下を CreateNew 保存した。

| T 内の追加材料 | bytes | SHA256 |
|---|---:|---|
| batch-anchor-v10-proposed-from-actual-Q-v1.json | 156207 | bb67a1eebd9d4b2850099940eaddf6afcd2b1835cdad7e67daa4173d1edf3820 |
| public-P11-parent-header-full-D3-export-and-scope-v1.json | 16043 | ed8ee0d041e2015b1385addba18c2ec8e64e1e307ccda012c388b55ad42ac10b |
| public-P11-first-bounded-design-v2.json | 8908 | 77e8e4618f3395d1bd100096c96f2ea8e9f29fdfc4c3a870d8f4d76b6e3c67f3 |
| public-P11-first-design-v1-to-v2-actual-binding-delta-v1.json | 2188 | 9d2c21c08ce342731b36982e226835b539ad48727d2585ae1a22d16de48f52d6 |
| P1193-actual-parent-header-material-manifest-v1.json | 1423 | d841e805bae04ca81200b4cda3f2c13e36b16c3ca8f462c0a1c7c100368b1423 |

header は旧exact36のABIで、18 named files＋772 checkpoints＋1 invocation＝791件を実Qからread/hashし、全件で登録modelのD3と一致した。全791件・固定8公開入力・author helperを出力前にfresh再照合した。parseは7公開JSONだけ、他784ファイルは全bytesのhashだけである。checkpoint全件のgeneric sealや算術を再受領したとはしない。791件の全D3はheader本体に保存し、scope票では全36fieldの由来・配列pointer・件数を示して巨大rosterの複製を避けた。

実source類29entryは採用済みmodelからのopaque D2で、P/C配置basenameの2件だけを実V10名へ更新した。P/C sourceやdriver本文を開いていない。保存 native V10 の previous768／total896／intake ancestry993は不変。次親headerの previous896／total1024／final ancestry1121は、実saved total・実accepted128・実separator公開ancestry配列長と自己8層表の和へ結合した。previous target は saved `output/start.json` の **current** target `96785516fc80ef49eb42a18fe3bc911b3084ff8a4e27fa161c6f8c325f8acdcd`。その `previous_target_remainder_sha256=e1b34dfa…` を次parentのpreviousへ取り違えない。old oracleは保存λ2346の35780/index435/edge847、新λ2474のoracleはnullを保持した。

design v1→v2は `/parent` 内の6 binding項目だけを変更・追加し、全JSONの正逆一致と他全値不変を確認した。formal5欠品は解消したが、この新headerのroot独立採用はまだpending。metadata export成功をV11 source採用・実装許可・runtime成功へ昇格しない。

Noether の共通案 `R/task1193/public/public-V11-canonical-wire-and-history-DAG-design-v1.json`、29371 B / `4f4769990968100aa23565d08d54cd29424b102607365c6428f53a1fb46fc836` を全文読んだ。6 canonical文書はregistryより前の独立した登録metadata入力とし、registry値から生成したcopyだけを再読して独立照合とは呼ばない。`public_wire_values`／`public_wire_value_bindings`／`public_wire_original_provenance` の各exact6と、source-only採用leafの循環切断に整合する。C独立数表をPの数値authorityへ使わない。

共通history候補は exact2 `{schema,native_domains}`、8世代の各exact4、文書family exact3 `{present,schema,keys}`。Pの現table exact8/current ownerは保持し、通常lookupのABI候補として合意した。Pの初稿のV9/V10移行範囲と、旧V3〜V8の残留literal範囲は別列で管理する。8世代の公開snapshotを作っただけで、全ordinary reader移行やF-v10-8の全面解消が完了したとはしない。共通案の実採用・各世代のactual由来sidecar・全残留consumer表・第10群の最終writer/子return接続は後続設計の対象である。

Task1192のP実受領・root正式採用は指定1192返信へ追記して閉じた。本Task1193は最初のP設計とactual親headerの準備まで。全数学source・受領器・selftestの作者実行0、V11数学source生成0を維持する。

追記：rootの独立採用票 `R/task1193/root-v10-parent-header-and-cv9-custody-adoption-v1.json`（253098 B / `802c9bef4dd59793b9b961439c0bf03a9fd57e5381a961db58649cf7edc6e99d`）をread/hash/JSONで受領した。statusは `ROOT_ADOPTED_EXACT36_ACTUAL_HEADER_791_D3_AND_FORMAL_CV9_SNAPSHOT`。rootの全文照合・有限処理 `1de400→4c18d2/native0` が、header全36field、791実D3、29 model-only entry、804入力の前後一致を閉じた。上記のheader pendingはこの実票で解消する。authorの新数学結果や対象実行を意味しない。

全8世代の通常consumer名簿 `T/public-P11-eight-generation-ordinary-consumer-map-v1.json` を785816 B / `0bbdf6d4f45ee4fe0cf4208e86a5301da6090ce028b4a1f685f0e8c64b6843d9` でCreateNew固定した。120 family slot、実144領域と829 lexical reference、独立schema/key期待値28点、保持する全値比較46点、15family外またはpartial69点、共通境界11点を区別した。参照列は原文上の所在名簿であり、実行到達の証明ではない。全296公開regionの原raw pinを自己P10へ一致させ、private本文は公開票へ収録していない。

V3/V4のretained25は通常authenticate経路へ残す。既に登録されたrootと実relative memberを照合した `read_json` のfull-file入場でsnapshotを比較し、保持body中の旧literalや全値再構成は「追加比較」として明示する。V5〜V9と新V10の登録15familyの期待schema/keysetは同じimmutable viewへ移す。4項だけのfinal-parent count、登録parent header、旧in-memory projectionへ全HEAD keysetを要求しない。旧fixtureを専用cloneへ移さず、同じ通常helperの固定世代・familyを使う。8世代snapshotの実値・sidecarは後着であり、sourceに読込みが無いことだけからV3 intakeの物理的不在を宣言しない。

名簿形成用metadata author `R/task1194/P/author_P11_history_consumer_metadata_v1.py` は19718 B / `2b3539ae75240e2cc1db36a8ab411501aa645886caa4ccd9809f2635a806e405`。Task1194の明示author helper認可後、全文自己確認 `e38e90` とpin通知を経て `3bc5f1→60b761/native0` で使用した。CLIは `python -B <同path>`。P sourceをtextとして読むだけで、import/AST/compile/対象実行は0。Task1193の初期設計をここで閉じ、全文読了した1194の範囲で実source準備を続ける。1194の実装認可は新source採用や本走成功とは区別する。

AUDIT_1193_P_VERDICT: BOUNDED_DESIGN_AND_EIGHT_GENERATION_ORDINARY_MAP_FIXED; ACTUAL_HEADER_AND_FORMAL5_ROOT_ADOPTED; TASK1194_IMPLEMENTATION_AUTHORIZED_SEPARATELY; TARGET_EXECUTION_0; C_INDEPENDENT_TABLE_NOT_USED; NO_NEW_MATHEMATICAL_RESULT
