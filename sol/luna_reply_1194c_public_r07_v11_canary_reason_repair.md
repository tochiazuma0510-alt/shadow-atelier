Task1194c 公開担当 Noether の静的修理を完了しました。実配備 head `200ac2f5885474353a94df4d4b39dbdd4c50c381` の driver を基点に、公開 canary の理由を通常比較・実行時の期待値・保存票の期待値で共通化しました。driver は4編集、WFは driver の bytes/SHA256 の2編集だけです。対象の実行・import・AST・compile・自己検査は行っていません。

以下の T は `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1194c/public` です。旧版は保存し、新版はすべて CreateNew で作成しました。配置先の相対名は従来の V11 と同じです。

| 新版（T からの相対名） | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_fixed_lambda_cycle_batch_v11_workflow_driver_v1.py | 63186337 | 4ca7c1a3600e8d632627ecbc9ef3682f1ff6b328a9ca67326c2f34b57c765dbf |
| .github/workflows/d972-r07-fixed-lambda-cycle-batch-v11.yml | 69995 | c0eb15b2b905fc89e4d509657aa522bfae7e6aa7bb0aeedab07af1e23ae5c8aa |

基点は driver 63185945 bytes / `fb45024b8f0d0b98e72782444bebe6758242d4231de93205d67222b7c691b8ab`、WF 69995 bytes / `2b67042d2ee9c9cfd93b69d9cbe614a98912fedea829fc7b803bcd9efa2f8485`。前回の root 完全採用 `root-v11-final-launch-closure-v1.json` 17739 bytes / `81931f3c964990f0859abf2df43fe39b46d1e81f9996385c801cbb8734838139` を継承しています。

裁定2310と対応 express は全文読みました。root の実ログ保全票による元 run は `34746915217/1`、head は上記 `200ac2f5…`、job は `103696408853`。metadata step 11 が exit 1、step 22 が連鎖失敗、candidate artifact は0です。P/C 本処理には到達していません。公開 stderr には、通常 comparator が `batch_workflow:v11-public-wire-whole-registered-value:P_timing` を発生させ、prefix のない wanted との exact 比較で停止したことが記録されています。保存側の expected.reason にも同じ欠落がありました。

根拠は R/run34746915217-reception-v1/failed-run-custody-v1 の `root-failure-custody-receipt-v1.json` 4512 bytes / `a045bf5e045532ed2c76b57f8915328a1faf4afe4e35a831fdcae40dbf320670`、その selected-public-diagnostics 以下の `metadata-stderr.log` 1949 bytes / `dc99d78371df3fceeda420f15bd48a6b89d660bf4f884e9d0bd18ad57c8c2abd` と `execution/metadata-result.json` 10127 bytes / `dc051b7cf3c0e5d71c1661edede76d07efc68410790d70a09e5a000e0321b34b`。これらの公開原文を全文読み、実 result の driver/stderr D3 と元 exit_code=1 を結びました。作者自身がネットワーク取得や GHA 操作を行ったという意味ではありません。

修理の4編集は次のとおりです。offset は元 driver の0始まり byte 座標です。

| offset | 箇所 | 変更 |
|---:|---|---|
| 47765707 | v11_saved_public_wire_canaries | expected.reason を共通導出へ。58→48 bytes |
| 62930705 | 2つの小 helper を追加 | 共通 why と実 require からの完全理由導出。0→426 bytes |
| 62931325 | v11_public_wire_compare | 同じ canonical 全値等号に共通 why を渡す。105→91 bytes |
| 62944334 | v11_public_wire_negative_canaries | wanted を共通導出へ。57→47 bytes |

合計差分は +392 bytes です。既存 require の92-byte 本文は完全不変です。追加した2関数は次の原文です。

```python
def v11_public_wire_value_reason(name):
    return 'v11-public-wire-whole-registered-value:' + name


def v11_public_wire_value_error_text(name):
    # Use the actual require formatter without retaining a second prefix literal.
    try:
        require(False,v11_public_wire_value_reason(name))
    except ValueError as error:
        return str(error)
    raise ValueError('v11-public-wire-require-did-not-reject:' + name)
```

prefix literal は増やしていません。whole-value why の literal は3箇所から1箇所になりました。完全理由は、変更していない require(False, why) が実際に形成する ValueError の文字列です。通常 comparator の canonical 全値等号、live 側の `str(error) == wanted`、保存側の `canonical(row) == canonical(expected)` は保持しています。任意の拒否や部分文字列一致を成功条件へ変えていません。

既存 metadata_canary の5件ループは各 name について共通導出を呼び、通常 comparator の実拒否文字列と exact 比較します。この経路が全5件の理由の自己整合を metadata selftest に接続します。新しい case、child、fixture 再実行、予算は追加していません。配置前には次の等式を原文と実登録 plan から静的に導出しました。表は実行済み canary 結果ではありません。

| name | require / normal comparator / live wanted / saved expected に共通の完全理由 |
|---|---|
| P_timing | batch_workflow:v11-public-wire-whole-registered-value:P_timing |
| C_timing | batch_workflow:v11-public-wire-whole-registered-value:C_timing |
| producer_interface | batch_workflow:v11-public-wire-whole-registered-value:producer_interface |
| producer_final_adoption | batch_workflow:v11-public-wire-whole-registered-value:producer_final_adoption |
| checker_final_adoption | batch_workflow:v11-public-wire-whole-registered-value:checker_final_adoption |

全5件は、実 registry と carrier の同じ exact4 plan、schema の同型 scalar 1個変更、変更 copy の D3 更新だけに接続しています。元 positive 全値、登録元全値、保存 positive/changed 全 raw、保存 row 全値の条件を保持しました。

全呼出箇所も固定しました。通常 admission が comparator を1箇所、negative_canaries が positive/negative の2箇所で呼びます。metadata_canary が negative_canaries を呼び、test_gate と final_gate が saved_public_wire_canaries をそれぞれ1箇所で呼びます。新 why helper は comparator と error_text の2 caller、error_text は live と saved の2 caller だけです。全355登録関数本文を有限 lexical scan し、新 helper 名は全 driver でも各3出現（定義1＋直接呼出2）、元は0出現でした。動的 call graph の完全性を主張する票ではありません。

変更3関数・追加2関数と require、ordinary admission、metadata_canary、test_gate、final_gate、main、command/execute/final_mode を含む関連原文は次の bundle に保存しました。元353本文のうち350は raw 不変、3が上記の置換、追加は2です。全 driver には4編集＋5保持区間、WFには2編集＋3保持区間を置き、EOFまで順方向・逆方向の原文一致を確認しました。

| T 内の材料 | bytes | SHA256 |
|---|---:|---|
| canary-repair-complete-raw-forward-reverse-v1.json | 6125 | 0b4c2f7c6fbdc99404d68bc7b562ad683fd4fcf32d79a8e4d782543a12731eb5 |
| canary-repair-source-workflow-full-context-v2.patch | 3156 | 4b475f3651fad6a38ef6347396cd9846bf9a6a3687c96f12adfc03118b2ee565 |
| canary-repair-all-functions-and-callers-v1.py | 73880 | 7830f9768bd8c3302aa2db917593f0fc29e7a93c895e44bdaeeaea7afec1890c |
| canary-repair-all-five-static-callers-and-frozen-inputs-v1.json | 95007 | d23396cd452987eab9a4e9b0bb16b66f7f8bcdbb46fd347933988ec3694a96ec |
| canary-repair-author-selfread-and-helper-erratum-v1.json | 3246 | 76bfe8c995de7370c02714837544c2ef61d711acb3295c8648ec124d94c32fec |
| public-canary-repair-final-material-manifest-v1.json | 4481 | 15286825ffe264ee1c5d7658de110beb71d654ea6cc06151f3528a106c54e23a |

freeze は全正逆差分と21有限入力の前後 D3 に結合しました。実配備 canonical8 は各原 bytes/SHA に一致。registry 30500836 bytes / `9ee87879554f1f88c69ba49131e335c6eef115215c32812919bb20e3a456eab9` と20 carrier 全値は不変です。P opaque は1129203 bytes / `2541428a88ebd99e549c8b810a1c7f9ad8d52aa9eaa82630ee67a2fd1fe5e97b`、C opaque は949977 bytes / `e7b703468c993939d66b0544b0b290bd489c0ac12af31883fd4967435aae3ee6` を既採用票から保持し、私有本文は読みませんでした。

metadata300/300、P5400/6000、C10800/11400、RSS7168、job330分、TERM30秒、元2子の共通絶対300秒、旧16＋新5、P/C旧9＋第10群、23親、rank2474/gen9179、k最大128、max_batches1/no-refill、C4、著者分離は変更していません。WF名は `d972-r07-fixed-lambda-cycle-batch-v11-envelope-v1`、marker は `[r07-fixed-lambda-cycle-batch-v11-envelope-v1-run]` のままです。元WF自己hash、原本/保存copyの custody、outer63 は同一原文を保持しています。

作者 helper v1 の初回は、require の既登録 body_bytes が末尾LFを含まないのに期待文字列へLFを1個入れたため、出力作成前に停止しました（81ba33/native1）。実92-byte 原文を確認し、helper v2 の期待値だけを修理。v1全文 fc127a、単一差分864647を読み、v2は d745ff/native0 で完了しました。v2 は19949 bytes / `a1c9d396b339dddd4ffcb68e0b0b69c43e2d5d6ba092b10a787211ee86d67aa3`。小patch v1の局所表示の改行連結も保存し、全source文脈の patch v2 を正しい表示として追加しました。いずれも候補 source の追加修理ではありません。

本便は公開 source 修理と静的差分の納品です。修理版の配置・新run・metadata PASS・数学結果はまだ本便の観測に含めていません。作者の対象実行/import/AST/compile、自身の Git/GHA/network、P/C私有本文読取はすべて0です。

AUDIT_1194C_PUBLIC_VERDICT: STATIC_CANARY_REASON_REPAIR_COMPLETE; DRIVER_4_EDITS_WORKFLOW_2_PINS; FIVE_REASONS_AND_SAVED_ROWS_EXACT; TARGET_EXECUTION_0; NEW_RUNTIME_RESULT_UNOBSERVED
