# Task1097 返信 — P5 全公開 JSON キー契約の静的閉鎖

F1. 本便の判定は **PUBLIC_JSON_KEY_CONTRACTS_CLOSED_STATIC** です。Task1093 の固定母集団 7,130 literal / 1,000 dynamic / 534 embedded key を全 ID のまま照合し、公開 JSON の key・path・schema・型・alias の未解決関係は 0 件となりました。P5 の source 修正は 0 です。これは公開キー契約の静的判定であり、全数学意味の再証明、数値再演、全分岐の実行、GHA 成功、未採択候補の採用を表しません。

指定 Task1097 は 4,174 B / `9440b9dfa3cef46decef7ea8cff38f6ec6a374bddd7bbf9e76cb13ea2b45a87f`。不変の P は `search/d972_r07_fixed_lambda_cycle_batch_v5.py`、366,659 B / `6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d`、LF 5,536、ASCII です。C の私的本文・私的票は読まず、P が公開定数として持つ C の pin は opaque metadata として扱いました。変更範囲は本返信と `%TEMP%/shadow-atelier-audit163/task1097/` の新 metadata file だけです。

F2. 機械分類の旧名称と最終意味分類を区別しました。Task1093 の PUBLIC_BOUNDARY 422 / INTERNAL 449 / ANNOTATION_OR_TEXT 27 / SELFTEST 102 は、その機械候補を発見した文脈の旧ラベルです。特に INTERNAL 449 には、公開処理行の外側 for/comprehension が含まれます。それを一括で非公開として除外せず、同じ reader・固定 tuple・型契約へ個別に戻しました。

最終 dynamic 全 1,000 ID は次の排他的分類です。

| 最終分類 | 件数 |
|---|---:|
| 型付き公開境界またはその collection control | 570 |
| 宣言済み構成・merge | 80 |
| 同じ object の列挙・範囲の定まった copy | 64 |
| annotation・parameter declaration | 25 |
| file-name / path / environment 操作 | 50 |
| exact-key guard | 38 |
| 内部 array・型付き return | 66 |
| 自己試験 scaffold・既存 interface | 107 |

各 ID に raw source 範囲、式の位置、最終分類、具体的な contract / alias 参照を付けました。残余 207 ID は既存の 110 契約へ、通常部分は補助 21 契約へ接続しました。その境界に当たる 19 点は 11 個の小契約へ明示接続しました。own-key iteration が他 object を読む場合は、同一 object の列挙だけを根拠にせず、有限 key domain または保存全 object の比較へ結んでいます。v3/v4 run.current の全 key が result の同名 key に一致する実 metadata 票も参照します。merge は宣言前後の key 域、上書き順、条件付き字段を個別契約に保持します。

F3. Literal 全 7,130 ID と embedded 全 534 ID も一度ずつ収載しました。旧 public 2,688 ID の旗を失わず、全 2,570 accessor/subscript 候補を通常 2,379 と自己試験 191 に分けました。通常 2,379 ID は 643 alias 群と最終 153 typed origin に結び、親 origin と実 alias suffix を別に残しています。内部 index が公開文書を保持する場合も、その子の公開読取を「内部」の一語で落としていません。

機械抽出が添字と誤認した独立の list literal 3 件、および file_pin 呼出し等を含む全 24 特殊点は個別に読みました。list literal は JSON key read ではなく、computed file_pin の SHA read は名前なしの exact2 / 名前ありの exact3 の双方で定義されています。通常の受理 descriptor3 と binary descriptor5 の型は緩めていません。

14 個の埋込み JSON は、実 source の文字列部分を metadata としてのみ再 parse しました。全 534 member について、元の key 順序、key 名、JSON pointer、値の型、byte offset/length/SHA と各定数名の消費位置を記録しています。旧機械区間名が character_counts であっても、その区間内に置かれた module 定数を内部数値処理として除外していません。producer / checker / raw の登録表も全量の有限 key domain として保持します。

F4. 保持された 9 形式は section、cochain、raw-word、raw-source、P1 reductions、P1 exponent residues、P1 roots、source-correction、B です。各票に自系保持 writer/reader の全 source pin・範囲、P5 caller、具体 root/path/schema、読取 key/型、分岐条件を結びました。代表として選んだ各実 JSON では、配列の全要素を含む nested key/type を走査しています。全 128 候補の全 nested payload を再計算したという主張ではありません。

歴史 root の 56 実 JSON は全 file pin / top key / 実 scalar 型と必要な nested 型を列挙しました。元 64 の snapshot は `output/snapshots/{ordinal}/start.json`、schema suffix は `.snapshot` です。packet/refinement HEAD から P5 が読む字段は ordinary integer の completed_steps であり、実 refinement HEAD にない target 字段を要求しません。旧 fixed 16 本体は original64 の実 path に束縛し、新 batch の fixed directory へ架空の同居 payload を要求しません。元 manifest exact8、参照 manifest exact9、JSON descriptor5→3 と binary descriptor5 の区別を保持しています。

保存原文の数学式の正しさは既存の保持 TCB / 既存結果への帰属のままです。本便はそれを再証明せず、実際に P5 が触れる公開 JSON の構造前件を閉じました。failed run の未採択 P 出力は型の実例としてだけ参照し、candidate 受理や正式 rank の更新はしていません。

F5. 未観測分岐も静的契約と runtime を分離しました。DEPENDENT、LINEAR、ZERO_SELECTED、AUXILIARY、RESOURCE_OR_REJECTED、RESUME_AND_DURABLE_TAIL、COMPLETED_READONLY、TELEMETRY_OPTIONAL_IO の 8 群について、literal writer と reader guard、nullable 字段、roster、型、通常 helper の保存境界を照合しました。静的契約は CLOSED_STATIC、当該枝の実走を示さない部分は NOT_OBSERVED_RUNTIME のままです。

特に、Dependent は新 row / instruction / target を形成せず対応字段を null とし、Linear は final lambda.bin を形成しません。選択の比較は実 checkpoint sequence 3、最初の candidate 完了観測は sequence 9 以後に限ります。直後の durable tail は HEAD count を進めず、初期診断は未形成の admission/count を null のまま保ちます。完成済み読み取り専用再受付では新診断を書きません。

F6. 自分と root の別読で見つかった「票の由来説明・保存形状」の訂正は、新版へ限定して保存しました。P source の不具合と混同しません。

- residual 207 の初稿で生じた PS 配列包装と source 範囲の結び方を撤回し、flat 110 契約の v2、実 path を正した v3 を正本にしました。
- supplementary の語を authenticated へ直し、selection の 27 は binding / seal を含む top 字段の総数であると明記しました。
- raw-word の receipt 配列の実 key は node_values です。nodes は維持し、説明変数名 receipts を JSON pointer として扱わない形へ訂正しました。
- plain-target binder の instruction origin に v3/v4 の実親 path/schema を加えました。file_pin の exact2/3 と pin_type の descriptor3/5 を区別しました。
- LA0136 / LA0272 の value を oracle-view から、実際の head / result / checker / final-manifest の 4 文書 family へ戻しました。LA0641 は progress/HEAD、LA0001 は payload descriptor3/5 の guard 付き union へ訂正しました。
- extra19 の contracts 包装 object を flat 11 件 array の v2 に直し、全 19 ID と再 parse 後の型を照合しました。all1000 はその v2 を参照します。

原票は削除・上書きせず、最終目録で superseded を区別しています。初期 component 票の「global join 未完」旗は、その票の保存時点を表します。全母集団を結んだ最終 closure / population 票が現在の判定です。過去の runtime staging 字段を理由に、未観測分岐を実行済みへ昇格することはありません。

F7. 正本は次の通りです。基準 directory は `%TEMP%/shadow-atelier-audit163/task1097/`、表中 public/ 以下も含め全 material を目録で pin しました。

| 正本 | bytes | SHA256 |
|---|---:|---|
| public/all7130-literal-key-contract-join-v1.json | 16732503 | `4fbc0923c950ddfdb7920bf22caaac7976a3cfd9cfa3a716eccd39906212a9c0` |
| public/all1000-dynamic-contract-join-v2.json | 2077340 | `bb69dcd2695e7f564f092ef72b732ac0c20f6f7df02ddc64f864e505770692de` |
| public/all534-embedded-key-type-join-v1.json | 794707 | `e9ac59bbbb74951210243ae108b71d1052f537707c1a93870f4a64fff19c253e` |
| public/literal-alias-origin-closure-v4.json | 1478579 | `06aa85051df2ee62a6aa85448d3c68aeaa9bc5e61f00bdfac80ac553cd3be555` |
| public/residual-207-static-contracts-v3.json | 349456 | `55a402835a795e20d9c1dd8fa0f9315663618a410f6f2304fcb8e2ff3f9a5ecc` |
| public/whole-source-typed-family-contracts-v2.json | 58539 | `fd64586d51f20ad906c94fb7743530adbe3761275232178c864497c707acbe34` |
| public/dynamic-extra19-point-contracts-v2.json | 23166 | `24bf08895188b2ef056ab9a647a7eb7a2a54dc27db878978c69a0cc00c281abc` |
| public/retained-nine-public-reader-contracts-v1.json | 21970 | `9ea1413720867c71d5531d2d58cb4345146bbbea56a3374a8a12b51cfbd6b00a` |
| public/historical-root-typed-origin-evidence-v2.json | 429387 | `1deaf0b82c0dee9eee34a91cc3ecaab54231ed643bb5624479fa470bdf83eb4a` |
| public/unobserved-branch-key-contracts-v1.json | 40684 | `624165337b0ad835cf14dfc63265270f7fd59560cbd4f9fd774eaa15ea86b368` |
| final-population-and-reference-self-audit-v1.json | 3308 | `70feee675665d22ab970ece3ab0c00c701f8cc2aca314237975960f96af7aa91` |
| final-public-key-contract-closure-v1.json | 6822 | `55d4e7ac73fb98d1edf80a976a3ff55c73087202f00a98268904da89889aa52b` |
| final-material-manifest-v1.json | 48004 | `b3ab9a09730b6041e42e86ebbb8467f36880eb399443c8fa0ca815f036a3b9ff` |

F8. 最終自己照合は全レコードを対象とする metadata 操作で行い、7130 / 1000 / 534 の ID 集合、元 source との位置・式の対応、旧 public 2688、alias 643 / normal 2379 / selftest 191、全 153 origin、参照先の実在と全 file pin を照合しました。distinct raw range 9,237 件が実 P bytes と一致し、配列を再 parse して型を確認しました。全 144 材料、合計 34,870,752 B が目録に収載されています（目録自身と本返信は自己包含しません）。契約原稿と対象 source 点の静読、全 serialized record に対する機械的な型・参照自己照合を区別して記録しました。

公開 key/path/schema/type の具体未解決リストは空です。source 実行 / import / AST / compile / 数値 / 新自己試験 / network / Git / GHA / credential 操作は 0、旧親・旧 fixture・既存 process の変更も 0 です。1089 の guardclosed は不変です。発射の採否は、root が P/C の契約、独立 WF 票、最終 pin と既承認の通知条件を結ぶ別段階に帰属します。

AUDIT_1097_VERDICT: PUBLIC_JSON_KEY_CONTRACTS_CLOSED_STATIC; SOURCE_DELTA_0; PUBLIC_UNRESOLVED_0; NO_NEW_EXECUTION_OR_MATH_CLAIM.
