Task1162 — Luna P author。checkpoint/partial の有限公開 metadata 契約を export した。P source、receiver、既存票は変更していない。

F1. `%TEMP%/shadow-atelier-audit163/task1162/` の公開納品は以下のとおり。

| 納品物 | bytes | SHA256 |
|---|---:|---|
| public-P7-checkpoint-branch-contract-v1.json | 79715 | `791eaee647947c15d0653cfeeae8a277f4fea90a8f9d703772b6806b608e2b2e` |
| public-P7-checkpoint-metadata-sites-v1.json | 162497 | `f4dc67e9ba29c77d4a7702ccce1ab8bbcc0d4c20c3b68589e3e0e899a6770a70` |
| P7-public-checkpoint-contract-delivery-v2.json | 5787 | `6b1437aa5459988257a5d8e154b3fa1de007eaf29930b865c2281b56689ce74a` |

44 schema の exact keys・ordinary types・nullable 条件・seal・存在順、79 callable の全 raw/byte/line pin と対象 key/value/file の全字句位置を記録した。producer provenance と consumer 関数を区別している。位置票には terminal `REJECTED` と schema-kind `rejected` など大小文字が異なる key があるため、通常の大小文字を区別する JSON reader を用いる。PowerShell5 ConvertFrom-Json がここで失敗した初期 bookkeeping delivery-v1 は使用せず、v2 だけを最終 manifest とした。公開契約・位置票の原 bytes は不変である。

F2. current P の実 schema は checkpoint exact24、progress-head exact16、selection exact27、selection-start exact19、start exact49、phase-manifest exact14、reduction exact27、candidate-manifest exact25、row-manifest exact18、final-manifest exact27、public head exact24、result exact48、resource-stop/rejected 各 exact29。seal は current namespace と内部 sha256 を追加する。内部 object seal と、sealed object 全体の canonical bytes に対する file SHA は別である。

selection phases は section/cochain/tree、candidate phases は raw/source/primal/p1/B/reduction。sequence は selection 未完なら 0..2、tree 完了後は `3 + 6*processed + partial`、partial は 0..5、上限 771。partial 1..5 の current ordinal は processed と等しく、phase map は先頭部分だけを持つ。reduction 完了時は decision を先に発行して processed を進めるため、6-phase の未完 checkpoint は作らない。JSON の canonical key 順を phase 実行順と誤認してはいけない。

`processed = dependent + accepted`、`rank = 1962 + accepted`、`generation = 8667 + accepted`。selected/processed は実枝の 0..128 であり、128 全採用を仮定しない。親 target ancestry は元 609 件をそのまま保持し、accepted rows だけを追加する。継続 64 steps と各歴史 batch 128 rows の意味を分け、一括置換しない。

F3. current P JSON に durable_tail field はない。内部の許容関係は `head_sequence <= durable_sequence <= head_sequence + 1` であり、最大 1 個の completed phase が committed HEAD より先に durable になり得る。receiver はこれを観測から分類する。checkpoint の status/terminal/partial/step/durable_tail、result.partial を捏造してはいけない。checkpoint/progress-head の current_lambda_sha256 は常に null である。

phase は pending payload/telemetry/manifest → rename/fsync → checkpoint → progress/HEAD の順。tree では witness/selection/view を、reduction では独立時だけ row directory と candidate manifest を checkpoint 前に発行する。完了時は input after inventory → final directory → public HEAD → result の順。途中 I/O/非協調停止では named pending、直後の durable phase、final 単独、final+HEAD が残り得る。receiver が recovery 書込みを行う契約ではない。

完了 terminal は COMPLETE_ZERO_CANDIDATE、BATCH_COMPLETE_CANDIDATE、LINEAR_MEMBERSHIP_CANDIDATE の三つ。後者だけ lambda.bin がなく、残余 selected は SKIPPED_AFTER_LINEAR として result の全 roster に含まれる。resource-stop.json は UNKNOWN_RESOURCE/UNKNOWN_RESOURCE、rejected.json は FAIL/REJECTED、両方 partial=true。診断の 5 counts は認証済み committed checkpoint からだけ得る。progress_head_sha256 が null なら counts と checkpoint_sha256 は全て null。diagnostic 自体の I/O 失敗や output 作成前停止では保存ファイルがない場合もある。診断の存在だけを新しい数学結果や最終採用と扱わない。

F4. G06 は係数ファイルの descriptor/whole SHA と JSON の trit/order/source/zero/literal sign だけ。ordered_reductions は rank_before 件を row_id 順に全件持ち、係数 0 も残す。physical_factors は同じ row/source/coefficient を持ち、exponent は `-sr(coefficient)`、独立 row の target factor は `+sr(target.scalar)`。sr(0,1,2)=(0,1,-1)。DEPENDENT では normalized/lead/sigma/target_scalar/new_row_offset が null、row/独立 payload はなく、rank/generation/target は変わらない。u8 要素と JSON 係数の一致、vector/pairing/solver の再計算を metadata receiver に要求しない。

F5. 入力 P は repair_v1 の 552885 B / `84d257701b1749804b2a4613283b7aab67f2cf14e53f11aa51cf9d3f3ddd82e5` と実 v6 P 453972 B / `c8a8b232acf581f0d43d26d9f6127b094235a46239ed13fcf5f73ae48d6b95a6`。既存 P 公開 region registry も pin して使用した。79 callable 中 71 は v6 と raw 同一であり、checkpoint/phase/row/reduction/diagnostic の継承根拠となる。追加親 metadata、current count/ancestry、batch_observation、計器 wrapper、run_actual の変更を個別に記載した。

raw/source/primal/p1/B の内部 payload roster と legacy raw-readout 詳細は、同一 phase_roster/own_dependencies および同一 L_FILE/L_SHA が指定する既存 v6 公開 nested 契約を継承する。この legacy helper 本文は本便で読まず、新しい exact-key 集合を推測して補っていない。公開票の INHERITED_V6_CONTRACT_NOT_REEXPORTED がその明示境界である。current 外側の v7 seal を、歴史 nested namespace 全体へ一括置換しない。

F6. 後続 Task1165 の実 root-bound repair_v2 P 552885 B / `6fe3ee03967b21d030a3bf141001df58305306c3b934b1c3fb71bd08a1a419bb` では、この全 79 callable raw/位置が同一だった。明示接続票は `task1165/P7-checkpoint-public-contract-repair2-overlay-v1.json`、4636 B / `1a71793abccc921756443f3624c982d50acf5234f8042346f026a3aa29b06184`。旧契約は不変のまま、実 source/identity をこの票から接続できる。

最新 root 報告では run34518126217/1、head2f8ad063da52da90ed74fd230fb122f96ad79ec7 は P selftest success、C selftest の旧 path 負例 no-op により failure。本 P/C は未実行。作者は stdlib の raw/JSON export だけを実行し、P/C/math/driver の import・AST・compile・実行・selftest は 0。private 数学本文・実 λ/係数値の公開、新 agent、receiver/P 修理、C private、Git/GHA/network/credentials は扱っていない。

AUDIT_1162_VERDICT: STATIC_PUBLIC_BRANCH_CONTRACT_EXPORTED_WITH_EXPLICIT_V6_INHERITANCE_LIMIT
