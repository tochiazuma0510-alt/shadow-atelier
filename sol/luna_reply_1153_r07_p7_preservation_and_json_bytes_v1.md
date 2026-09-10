# Luna reply1153 — P7 終了時 preservation / 実 parser bytes

**F1 — 静的納品。** Task1151 完成版を保存し、`%TEMP%/shadow-atelier-audit163/task1153/draft02/d972_r07_fixed_lambda_cycle_batch_v7.py` を納品する。**552642 B / `2439db913d06f0cd9249f34ff3c2d1495ac709e03073269ef5426038e7f2b011`**、ASCII・8221 LF・CR/BOM なし・末尾 LF。基点は1151 draft02、544642 B / `a47d978ffd5b1504b55828b6ee26b72bb52b53cd5539e11b71a1527df9fd2b68`。以下の票は task1153 直下。最終 manifest は **10598 B / `1c45005f74472fc6d6bdf1acc708781d5904eb8c1d55839af7fa913afa852da1`**。

root は1151全票を独立採択済み（2691 B / `66e5ade68175f9e17d3ea219d5a291dc2eabbfc5dfaca391b0cf322389e0e1dc`）。1153公開設計8593/8ed8fdd6…も静的採択し、draft02全差分を6881b0で別読して追加findingなしと報告した。本便の最終票は作者の静的成立を記し、実行実績や root の binding を代行しない。

**F2 — 終了時の実 caller 区間。** `finish_inputs` 全 raw と元チェック/例外/返値を保持した。`run_actual` の既存2呼出だけを wrapper に接続（L6977 readonly-completed、L6994 active-invocation）。同一実行経路では元どおり一方だけで、失敗時の追加再呼出を作らない。実呼出 counter の ordinal、内部 monotonic 開始/終了/差、実 admission.paths の19親 role/path を公開する。

新 `input-preservation-timing.v1` は exact14、stage `finish-inputs`。測るのは元関数の全 caller 区間であり、全親 inventory に加え、元の比較、code authentication、acceptance hash、after-document処理、input_preservation と小さな wrapper overhead を含む。元関数が返った時だけ `completed_parent_roles=ROLES19` / `ALL_TARGET_PARENTS_COMPLETED`。例外時は実経過秒と target 集合を残すが、本文を計器化していないため走査済み prefix は null / `PARTIAL_RANGE_UNAVAILABLE`。全親走査後の別チェックで失敗した場合も prefix を推測しない。target metadata 捕捉失敗は null と observation_error にし、元 call を継続する。

**F3 — 同じ実 bytes を元 parser へ。** `read_json` の既存1回の `read_bytes()` を `raw` に受け、その**同一 bytes object** を元 `json_bytes(raw)` へ渡す。保存4親の active root と `output/candidates/[0-9]{6}/reduction/(reduction[.]json|physical-literal[.]json)` の完全一致だけに、別 observer を接続した。追加の open/read/parse/stat はない。宣言 bytes・rank・中央directoryの合計を代用せず、hashだけの再読や current 候補は計数外。

新 `parser-bytes-timing.v1` は exact13、stage `saved-batch-parser-bytes`、固定4 role/ordinal0..3。`by_document_kind` は reduction.json / physical-literal.json の exact2で、各値と totals は null または exact15統計。実 read calls、parser attempt 件数/bytes、初回 role/path の unique 件数/bytes、反復 attempt 件数/実 bytes、success/fail各件数/bytes、bytes取得前のread失敗、反復長の変化、成功窓の秒、未分類途中readを分ける。反復時はその時の実長を使う。P の unique は初attemptを数え、後にparseが失敗した初回も含む。

Pの success は元 read_json が optional generic seal まで返った範囲。caller の後続 native seal は範囲外。成功 read/parse 秒には小さな両 observer overhead を含み、span は窓間の隙間・失敗read出口も含み得る。成功秒の和に失敗窓を加えない。1151の窓および native-metadata と重なるため加算して総仕事としない。C の成功/unique の独立定義へ合わせ直していない。対象種別が未観測なら nullであり、観測済み統計の0はその下位事象が実際にない意味。

**F4 — 既存 wire・順序・partial。** 1151 exact25 observer/helper と元 exact12 writer は全 raw 同一。旧29本および1151を含む旧33本の timing subsequence を保持した。追加4層では **旧ordered_i → 新bytes_i → 旧native_(20+i)** の順。旧inventory19本・continuation native1本、4 triple、旧state5本で37本。その後、元呼出位置の preservation1本を加え、通常/readonly完了の timing-schema filtered 順序は38本。他 progress/phase stderr は本数外。

FAILED は元例外を bare raise し観測済み prefix を残す。OBSERVER_ERROR、NO_OBSERVATIONS、unavailable、未開始/中断/初期化失敗/ログ欠落を区別し、missingを0や完了eventに補わない。層失敗では旧ordered/newbytesのFAILEDが出ても後続旧native完了eventはない。finish前に失敗すればpreservationはない。finish後のpublication失敗は、既に返ったfinish callerの測定を消さない。8つのpartial分岐と実source接続を公開票に収録した。logging failureが数学の返値・元例外を置き換えず、COMPLETEDを数学PASSとして使わない。

**F5 — 全raw/consumer閉包。** 全205領域＝196 raw同一＋4変更（MODULE/read_json/authenticate_acceptance/run_actual）＋5追加。変更前後rawを収録し、不変部分はpin済み実bytesを参照するdeltaで、全552642 Bへのforwardと全544642 BへのreverseをEOFまで実復元した。登録37 bodies/4 old loaders/25 old readers、finish_inputs、inventory、旧1151 observer/helper、旧6群のcanary/selftest設計scopeを保持した。22 embedded constants / 792 key/typeは全raw同一。履歴票の値を残しcurrent範囲の実offset/pinを更新した。

全10976 literal＋1457 dynamic＝12433点。旧12308点は352本のaffine位置写像で元の巨大票へ結び、新125点のorigin/type/controlを個別に記録した。退役旧点はtask名docstringの1点。旧票と同じ巨大表を複製していない。同じ文字列のobserver actionでも実receiverが違うため、7 callbackの実呼出位置と9領域の手読overlayでaliasを明示し直した。書込fieldと元source、全consumer位置を再照合した。

| 材料 | bytes / SHA256 |
|---|---|
| `public-P7-preservation-parser-wire-and-order-v1.json` | 55303 / `8bfbad1077fe091beb12110a6f1b109bc5680121e12a0aa2cb600e1ce3361024` |
| `public-P7-preservation-parser-source-and-ranges-v1.json` | 351948 / `2ede7f4c12a667d27e82d447b93841cf5073f7fb6073b53a17cc73e888561efd` |
| `private-P7-preservation-parser-full205-forward-reverse-v1.json` | 367612 / `5e878edfc25221b99981fb5d0048a587106767918c52397a4bd09bc56133a80b` |
| `public-P7-preservation-parser-compressed-all-point-inheritance-v1.json` | 105726 / `0b903dc7c48fa7b78dd361e36ce426608657a1c168ab92d50cb9b708e2b8d69a` |
| `public-P7-preservation-parser-all125-new-point-decisions-v1.json` | 152278 / `fd7a51d149076e851a2fd4e32671c584a60b0cbbe0df9e5f536e1f0ad544ce82` |
| `public-P7-preservation-parser-consumer-static-closure-v1.json` | 3086 / `a14392c92435e1a1e7da1747db82d333f1ffad1504b176ba5db4569a1bee250f` |
| `public-P7-preservation-parser-static-final-consistency-v1.json` | 4721 / `0771d5bbc3fa5d8292dbedb5fb67a5d6dc56b6df60a457c84362c002e13e814b` |
| `P7-preservation-parser-static-delivery-manifest-v1.json` | 10598 / `1c45005f74472fc6d6bdf1acc708781d5904eb8c1d55839af7fa913afa852da1` |

納品21材料・継承14材料を保存後に全件再pinして一致。公開契約をrootがdriver/Cへ渡せるが、private P source/deltaは共有しない。

**F6 — 実行境界。** current CLIのnineteen labelはL8188で維持。normal guardは L759/token offset38917/4 B の `None` と L761/token offset39049/5 B の `False`。裁定2246のP診断追加だけを実装し、19親/native投影、caps、k128/max1/no-refill、C4 raw、数学宇宙、共有TCB、著者分離を保持した。native1962/8667・限定7の受理を越える数学主張はない。実bytes/count/秒、最終本走binaryのselftestは未取得で、旧selftest PASSを新sourceへ移していない。数学source import/AST/compile/実行/selftest、C private読取、新agent、Git/GHA/network/credential/process操作は行っていない。rootの後続実行/bindingへ新承認待ちを追加しない。

AUDIT_1153_VERDICT: AUTHOR_STATIC_DELIVERY_COMPLETE_GUARD_CLOSED_NOT_EXECUTED
