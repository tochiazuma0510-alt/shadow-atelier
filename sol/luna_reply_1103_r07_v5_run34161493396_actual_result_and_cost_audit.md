# Task1103 返信 — run34161493396/1 の公開結果・費用・保存 metadata 監査

**F1 — 結論と範囲。** 実成功候補 `10034053256`、run `34161493396/1`、head `a5b456a973f8a917f3af386d327061a02a0cf900` の公開 metadata binding は全指定範囲で一致した。P と C は実保存結果でともに PASS、selected / processed / accepted は各 128、dependent は 0、rank 1834 / generation 8539、Separator / BATCH_COMPLETE_CANDIDATE。C の partial=false、durable_tail=null、全 128 decision・128 row・全完成 payload 比較の実報告を同 root へ結んだ。旧失敗 run の P-only 値を今回の観測に転用していない。監査開始後に届いた裁定 2224 により、正式格付けは **1834 / 8539、cross-checked・限定 7 条**となった。Task1103 自体は公開保存値・普通型・全 file pin・参照関係・費用集計の監査である。

作業は指定 TEMP の新 metadata 票と本返信だけ。P/C 私的数学本文・helper は未読、source は全 file pin を opaque bytes として扱った。Python / GAP / AST / import / compile / dot-source / 数学再実行、Git / GHA / network / credential 操作、新 agent 起動、入力 root・親への書込は各 0。root の別全 typed 受領器の全 scope を再実施したとは主張しない。

**F2 — 実取得境界。** root handback は 4,939 B / `0fa691759a758e535d906490108e2fbf4b390e3f51c0059ff422d2cb52b19ce1`。対象は `%TEMP%/shadow-atelier-fixed-lambda-batch-v5-run34161493396-candidate-a1`。candidate ZIP は **384,961,441 B / `72e19a87e3a4ca06daa3b1b9dc8a16e76778e6ce1d6bd3a57b25acea363602db`** で、自系でも ZIP 全 bytes を再hashし一致した。取得票 720 B / `d669afa2c01fb318dedabba7def6cdb029c81cf1580c91445fe048b77944af7d`、全 entry 票 2,159,113 B / `101e1a35d2fab20b5cda819887cfe341c34462cee72f05a23bcfce5c7dc12e41` を実 pin した。

root の全 stream EOF・抽出後 hash 票は 11,750 file / 1,347,269,002 B、当初の外側 directory は 3,507、ZIP explicit directory は 0。自系は全 entry の名前・重複・普通整数・合計を照合し、各 component で実際に読む file を全 hash へ結んだ。全 root の全 file 本体を別途もう一巡 hash したという主張はしない。CRC の局所再計算は 0。GHA の CRC true は、実 archive receipt の字段・全 pin への結合として区別した。

**F3 — 17 親、8-key acceptance、source/runtime。** acceptance の exact keys は `schema / parents / anchor / batch_anchor / next_batch_anchor / code / runtime / registration`。17 role の順、各 artifact の run / attempt / head / repository / workflow / name / bytes / digest / conclusion、実 API、取得票、全 file / directory 目録を結んだ。prepare と block-0..3 は元 run33677346616 の **登録済み failure** と実 API が一致する歴史親であり、17 親をすべて success と言い換えない。old64・v3・v4 の三親は登録済み success と一致した。

| 親層 | 実 run / artifact | rank / generation | 引き継ぐ関係 |
|---|---|---|---|
| old64 | 33990567016/1 / 9977040548 | 1450 / 8155 | 元 64 steps |
| batch-parent v3 | 34023589045/1 / 9987222571 | 1578 / 8283 | 128 row、祖先 225 |
| batch-parent-v4 | 34120585268/1 / 10020349387 | 1706 / 8411 | 直近 128 row、前層 128、合計 256、祖先 353 |

current source closure は 24 file。P は 366,659 B / `6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d`、C は 336,211 B / `111e23bfe6a7b49b4b3a03a00f3b48345c3f75ab098f06efc18279e881555b19`。実 workflow 26,294 B / `3102f115c0d59d69d7ecc0b3941588b7fab5181e961b6399126a4e2516c4e969`、driver 1,145,223 B / `f1b50bc529f08ad8654d775e2fce652334dfa8b325d3d2bcc27286aa09cb3f98`、current registry 499,053 B / `8792321d9cdcf25244726050928ae7fbd0cce5812e4f6867fa303ffcb49caa73`。配置前後の全 11 SHA 行と実 copy を照合した。

runtime は NumPy 2.5.1、Python `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]` の全文一致。portable acceptance は各 parents[].path だけを除く公開射影を JSON metadata から組み、`9914f2de9e04efe3e6d01843971026e38720eb3853446b36eb39836e40717da8` に一致。code24 list と parent17 list の canonical hash も P/C の before / after 字段に一致した。

fixed は参照専用として読み、旧64の exact8-key manifest と実16 payloadを参照先とした。親/current の JSON descriptor は公開の5→3-key射影、binary は5-keyを保持。二つの `batch-fixed-reference-receipt.json` / `next-batch-fixed-reference-receipt.json` を別名のまま final run へ結んだ。親 directory に存在しない固定 payload を要求していない。

**F4 — 現出力の全公開鎖。** 4,513 JSON / HEAD を公開59 path-patternに分類し、schema、top-level exact keys・型、全 file SHA、該当する raw seal を照合した。旧 catalog の保存数値を期待結果として再利用していない。全128 candidate / 全128 row / 全768 candidate phase の順と manifest-local EOF、witness、同じselection、rank・generation・stateの前後、plain target JSONの全SHAとpacked remainderのSHAの区別を閉じた。

全226,496 ordered-row recordは各時点の1706親行＋既存current行の順を保持。source tagと元role/file/全pin/offset/length、v3とv4の各128 local row、先行current rowのmanifest/payload pinに結び、75,759件の零係数もliteral factorから落ちていない。signed-tritの公開整数表現を照合したが、parent vector slice の演算・新還元・語評価は行っていない。

全772 checkpointは sequence 0..771 が重複・欠落なく、全file SHAの前後鎖、選択phase prefix、候補phase prefix、committed counts、最終progress/HEADへ一致。selection観測はsequence 3以後、最初のcandidate処理完了観測は9以後の保存境界へ結んだ。現在のfresh invocationは1件、resume=false、before counts=0、before HEAD二字段=null、batch_size=128 / max_batches=1 / refill=false、17実host pathと当回launch/acceptance/source/registrationを保持する。

finalの481祖先は旧353の全辞書prefix＋新128の実row/instruction/plain-target参照に一致。新final lambdaとtargetの全payload pin、保存direct-pairingの5字段、1834 rowという報告、DERIVED rho2=1とdirect-read=falseを同じHEADに結んだ。数値pairingやrho2の再演ではない。

**F5 — lambdaの役割。**

| 役割 | 実SHA256 | 根拠 |
|---|---|---|
| 旧v4の選択時 λ1578 | `6a0fe9368f2ec7f28c4d8076e7d3184fb57322b9d0905a8e7c3c26b467bcee4e` | v4 selection/start、v3 final lambda、旧selection |
| 今回fresh選択時 λ1706 | `d036e848c46b563a5b0f683fb94afcbc759dc4bc402c6db14c82b172ccc0a653` | v4 final lambda、current start・selection/start・3phase |
| 今回新final λ1834 | `b224f95de675b1966a12eeeb1700066b03d009f3fd0e69f9e148a6d04781dff7` | current final/lambda.bin・separator・manifest・HEAD |

今回のselectionは failed_count=36,002、first_failed_index=71、first_failed_edge=127。旧v4 selectionは36,104 / 74 / 131で、旧λ1578に属する。P/C/run/observation receiptの全辞書一致を確認した。最初の候補のraw_pairing=selection_scalar=1、subtracted_new_pairing=0、保存条件とINDEPENDENT報告を結んだ。残る候補の独立率や失敗集合の単調性を予測したという主張はない。

新finalに対する `new_lambda_oracle=null`、`new_final_q_computed=false` は不変。最終四character supportの保存値は読んだが、それを新q計算と呼ばない。

**F6 — 五executionと実selftest。** start/resultの全pin、UTC時刻、実exit、argv、stdout/stderr、実test本文、source/audit bindingを照合した。全5 exitは0。metadata stdoutは空の実fileであり、実metadata test票を別に読んだ。

| execution | UTC開始 → 終了（2026-09-07） | 実harness秒 |
|---|---|---:|
| metadata | 21:04:31.159288 → 21:04:50.180250 | 19.02099190200005 |
| P selftest | 21:04:50.677305 → 21:04:54.192037 | 3.514758602000029 |
| C selftest | 21:04:55.046447 → 21:05:01.059507 | 6.013095579000037 |
| P main | 21:05:05.103320 → 21:33:28.672770 | 1703.569490573 |
| C main | 21:33:43.914214 → 22:07:46.243818 | 2042.3296421820003 |

metadata16、P四群[30,10,6,7]、C四群[28,9,6,7]は実本文でPASS。Pの53件の実rejection票を目的名/labelへ結んだ。Cの全四ledger・実群結果と、保存された第三/第四群のpositive/negative JSONを照合した。歴史C ledgerに期待labelだけがある箇所を、個別caught-errorを別に観測したとは言い換えない。

beforeP / beforeC / afterC の三fixture比較、全fixture subtree、全4,420 fixture JSON、内ZIPの全4,790 file stream EOF/SHAと全2,351 explicit directoryを閉じた。fixture JSON parse errorは0。内ZIP 4,531,197 B / `ea9465f60f4c0a356c28f9f286e810463fb5e63a2eaa5ebb68bc4a114891e8e4`、archive receipt 1,816 B / `c92107adffa17d3e0eb44ea3d9cdbf15d37fa6805f6b5769647a32a4d3d5ae02`。旧数学suiteの追加実行は0。

**F7 — 実費用。** cost receipt 375,231 B / `d51980810e3798bd59632074492ab0fd57e2fada8b08477e50a7e2d82975e86d` の全字段を読んだ。全776 inputはP/C本体2、harness2、selection3、candidate 6×128、final1。全772 manifestと各telemetry descriptor、実elapsed・普通型・pathを全件接続した。coverageの全128 candidate値と全772 measurementの全辞書もPおよび実phase JSONへ一致した。

| 保存費用字段 | 秒 |
|---|---:|
| P total | 1702.391124 |
| P selection | 11.831757000000001 |
| raw / source | 13.362489 / 34.059533 |
| primal / p1 | 308.797425 / 1011.694228 |
| B / reduction | 9.430121 / 34.30152 |
| 六phase合計 | 1411.6453159999999 |
| final separator | 1.085957 |
| P residual | 277.82809400000014 |
| C total | 2041.4255092800001 |
| P+C total | 3743.81663328 |

公開式は `P residual = P total − selection − 六phase合計 − final`、`P+C = P total + C total`。harness二値は実行境界として保持し、P/C内部totalへ重ねて足さない。Decimalの独立metadata集計との差は最大1.4×10^-13秒、比較許容1×10^-11秒内。Python math.fsumのbit-exact再実装とは主張しない。残差は正で、clampなし。未観測elapsedの補間は0。今回のcost status PASSとP/Cの完成結果は別々の根拠で閉じている。C段別timestampは未形成で、C residualを捏造しない。

| 親規模 | file / directory | 展開file bytes | ZIP bytes |
|---|---:|---:|---:|
| v3 | 11,437 / 3,475 | 1,267,599,138 | 369,233,546 |
| v4 | 11,648 / 3,525 | 1,308,094,050 | 377,383,320 |

この一観測から性能倍率や任意rankへの外挿を計算していない。F-v4-1に関する最新の扱いはF9の外部裁定として記録する。

**F8 — 全保存29項目と最終envelope。** 全29 flagは普通boolean true、errors/missingは空。17親のbefore / P後C前 / after、source24とraw/driver/WF/copy、acceptance、三registry・8歴史source・二static票、二fixed参照、両親transport、fixture/内ZIP、cost入力、current出力の全目録を根拠へ接続した。v3復元は36空directory、v4復元は38空directoryが保存plan/created/after差分に一致し、全fileは不変。この復元は実GHA receiptの読取である。

P出力は6,587 file / 1,164 directory / 1,232,723,750 B。P後C前とC後、preservationの全目録が一致し、全実取得entryへ結んだ。全envelopeは最終runと自inventoryの2fileだけを除く11,748 fileの目録に一致する。run receiptは362,106 B / `bd902f63666ad79bc13976e5e94db372a5d3a90844ee743d410ab04c49cc9a2f`。

外側directoryは非原子的観測として残す。長い同一metadataコマンドのintake-controls照合時は空40本（fixture36＋metadata4）が不在、後のenvelope directory照合時は不在0だった。全file pinは一致したまま。自系mkdir・復元書込は0。rootからtyped受領器進行中との連絡はあるが、復元主体・因果および最終復元receiptは未確定として扱い、推測で補わない。内ZIP/保存目録に存在する空directoryと当初の外側ZIP輸送形状を区別する。

**F9 — 増分CV-9と最新承認。** 2220の論点は次の範囲で根拠が揃った。

| 論点 | 今回の根拠 | 裁定・限定 |
|---|---|---|
| 第17親・8-key | 実API/全受付/全目録・portable hash・二層intake | 2224で正式1834/8539、cross-checked限定7条 |
| fresh/旧lambda | 三lambdaの全SHA鎖、実selection、seq3/9、481祖先 | 新final oracleは未計算 |
| P residual / C / P+C | 全776 input・全772manifest・公開式 | C段別時間は未観測 |
| 両親規模と費用解釈 | 全17context、上記二親規模 | 自系は因果モデルを再推定していない |
| 保存と範囲 | 全29flag・三fixture・全run結合 | root全typed受領器の別scope、空dir観測時点差を保持 |

[裁定2224速達](../ops/express/20260908_fable_astra_2224_batch_v5_cv9_grading_and_rotation.md)を全文読み、5,183 B / `97acf6b19afc3613b0d68bb93d12a0324663dcc8115eba8570b6ac073e7b2a49` に一致した。司令塔は **F-v4-1を層数項の欠落として閉鎖**し、後続の層回転設計をF-v5-1へ分離した。これは工房CV-9/裁定に帰属する。本票の早期cost componentの「自系から因果閉鎖しない」記録は保持し、最新状態はcompletion-v2と承認追補を正本にする。18親v6の一回準備/実行許可は別委嘱に属し、Task1103で新source・workflow・実行は作っていない。

限定7条、共有TCB・F4未排除・DERIVED rho2・harness単著・C段別timestampなし等を維持。A0 actual0/1、階段1/6、grade2 member/nonmemberは両NOT_DECIDED、verified=false。旧失敗run34148667863のC比較0/FAILを今回のC PASSで遡及昇格しない。

**F10 — 凍結材料と未読/未接続。** 票は `%TEMP%/shadow-atelier-audit163/task1103/`。27 componentの全pinは `all-audit-materials-v1.json`、13,386件の全参照file pin unionは `all-referenced-file-pins-v1.json` に保存した。後着の2224追補は別票として明示し、最終納品目録に加える。

| 正本票 | bytes | SHA256 |
|---|---:|---|
| all-audit-materials-v1.json | 10166 | `3305c9a06499657ac66ad49a542bfb886c381fe83444bfde7f578f43de1da6e4` |
| all-referenced-file-pins-v1.json | 6273431 | `2a3935f1912555f9976544421496b6a06d91b5d322915ba3454ccf25ab60e76e` |
| completed-public-metadata-audit-v2.json | 3534 | `de270066a9f970af22c55bb76f401052f55ea01d3d27389b154d2def43e56495` |
| ruling2224-and-concurrent-directory-observation-v1.json | 8268 | `922f90b39480e4771544a18d8fbf9b531e78d184997027a9af643a45bf53d0ab` |
| all17-acceptance-old3-source-and-fixed-lambda-bindings-v1.json | 1590475 | `abd6dd0586c4aa7c36e888caf1185178a10767fe0385befa0b1480e7aebcd247` |
| all772-checkpoints-and-fresh-invocation-v1.json | 3846405 | `172f09e2a0d5f1599536fe6ad5d806ba01b1db0324632c29a1814397fc8efab6` |
| all29-preservation-underlying-inventories-and-final-run-v1.json | 59443 | `44e6a694abee76bc19d202037a37ec6c1d5781b05cbde2fbdafe887a47cf5eb3` |
| cost-all776-inputs-and-formulas-v1.json | 1513088 | `0e34dc5ba21d26a2c3d8dd5de9167b05e8df4695a057b926f518b2fb623003bc` |

Task1103の公開binding未接続は0、実artifactのrequired findingは0。局所照合コードで公開字段のalias/パス・signed-trit・PS型を取り違えた途中エラーは、実保存serializerの形に修正してから最終票を生成した。実artifactのFAILや修理sourceとは扱っていない。私的数学・vector再演・別root受領器の全scope・工房の費用モデル再推定は意図した範囲外。保存されていない歴史HEAD本文や未観測branchの実成功を主張しない。

AUDIT_1103_VERDICT: PUBLIC_METADATA_BINDINGS_MATCH; RUN34161493396_A1_P_PASS_C_PASS; COMMANDER_2224_CROSS_CHECKED_LIMITED7_RANK1834_GEN8539; NO_NEW_MATHEMATICAL_REPLAY; VERIFIED_FALSE.
