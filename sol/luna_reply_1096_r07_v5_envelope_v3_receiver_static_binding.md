# Task1096 — envelope-v3 metadata 受領器の限定静的結合

F1. Task1096 全文（3043 B / 27b0109c5f10ba17cf0fa622d3b37db1f5bc46070421a316b4e8764275c0d7d8）と裁定2218/expressを読了し、1094作者最終凍結後の限定更新を完了した。新受領器は **TEMP/shadow-atelier-audit163/task1096/root-review-receiver-v5-envelope-v3-guardclosed-v1.ps1 = 516701 B / fd26b0e1f571350d23732d2966d10ae3c3a64b07dc87298bfd2b5cc3ea3ba632**、LF4626 / CR0 / ASCII only / BOMなし / final LF / 行末空白0。以後の T は同task1096 directoryを指す。元1089の516900 B / 49601381a834c583071251288e7f9b94e9b1036b6f88e32262d1051a8dbee0e4を全raw同一の baseline-receiver-launch-bound-guardclosed-v1.ps1 として保存した。旧1088/1089/1094、既存親/root/processは変更していない。本票は作者による限定再結合の静的票であり、自作1094 WFの独立再監査や一般受領器の実行結果ではない。

F2. 全変更は **9行、−199 B、LF差0**。L14/L28は現在の未観測表示、L30は失敗run34148667863の五字段launchをnullへ戻す宣言、L31は2215から2218への契約参照、L32/L33/L60/L61は下表の新WF/driver/C/current registry、L3716はcurrent v5 driver repo pathだけである。P pin・active WF path・REPORT側basenameは保持した。新sourceには旧失敗run/headおよびdiagnostics ID10029340951の出現0。L29 artifact=nullとL34 guard=falseは全raw不変。

| 現行公開対象 | bytes | SHA256 |
|---|---:|---|
| P（不変）search/d972_r07_fixed_lambda_cycle_batch_v5.py | 366659 | 6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d |
| C search/check_d972_r07_fixed_lambda_cycle_batch_v5.py | 336211 | 111e23bfe6a7b49b4b3a03a00f3b48345c3f75ab098f06efc18279e881555b19 |
| active .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml | 26294 | 3102f115c0d59d69d7ecc0b3941588b7fab5181e961b6399126a4e2516c4e969 |
| REPORT driver.py / repo search/d972_r07_fixed_lambda_cycle_batch_v5_workflow_driver_v3.py | 1145223 | f1b50bc529f08ad8654d775e2fce652334dfa8b325d3d2bcc27286aa09cb3f98 |
| current audit-region-registry.json | 499053 | 8792321d9cdcf25244726050928ae7fbd0cce5812e4f6867fa303ffcb49caa73 |

全9行原文diffは T/receiver-full-nine-line-diff-v1.txt =2820 B / 4ef39fbd7a3e99a60594735a293c210fe96ffdb57be2603c64442afc7faedb4e。全before/after・役割・sibling票は receiver-nine-line-binding-v1.json =8504 B / 004f7fe4e28d53e70bdbb2403a9baebac008825cdbdc742ed88f2177203d2727。19 literalの全出現と8変数の全使用行は receiver-all-literal-contexts-and-guard-v1.json =105348 B / d63b66cb45a1d7e3737a71f243beebe5f114ac36d2a28c110cb8ab8ed58362edへ保存した。旧current pin/pathは各1→0、新値は各0→1。歴史v4の driver_v2 はL1732/L3733の2出現をそのまま保持し、一括version置換はしていない。歴史wrapperの局所launch/approval2197/guard=true、旧二registryと全17役の登録も全raw不変である。

F3. 全EOFを文字列境界とraw byteで別集計し、旧96→新96区間、94区間同一、追加/削除0、欠落/重複0を閉じた。変更区間はPREAMBLEとfunction:ReceiveWorkflowEnvelopeV5だけであり、後者はcurrent path一literalを逆置換すると全rawが元と一致する。9変更と10不変span（非空6）からforward全516701 bytes、逆方向に全516900 bytesを再構成し、全bytes比較とSHAが一致した。旧60関数も各raw/元登録SHAへ直接再照合した。末尾ManifestFilesについては、EOF区分が後続mainを含む点と、旧60番目の実function body2409 Bを別照合する点を保持する。証拠は receiver-full-EOF-forward-reverse-and-body-retention-v1.json =153729 B / c2669890cbb6230bfc8fbce087f4a170fb9f22588101212ecf15acc753b07104。

旧1083独立静的採否と1088/1089の一般本文保持を基点とし、Same/PlainInt/二型修理、旧三root認証、8-key acceptance、metadata16、P[30,10,6,7]/C[28,9,6,7]、三fixture、全cost、actual C成功、no numerical replayを変更していない。全1059以降の一般処理を再実装したものではない。21 Python＋3raw、親17/正式1706・8411、旧64/128/128/256/353祖先、k128/1/refill=false、P5400/6000・C10800/11400・7168 MiBも保持する。変更したP/C数学本文はなく、新Cは公開opaque全file pinだけを読んだ。

F4. 同directoryに必要な五siblingを1089からCreateNewで全raw copyし、source/copy双方の全bytesとSHAを再照合した。1094固定目録の全19材料、公開新C pin、不変P、旧1088/1089・関連票・選択した旧親metadataを再hashした。public-inputs-siblings-and-selected-parent-retention-v1.json =154091 B / 27dfd8532e5bdc85b37f6c164dcf4875aeae4ef9cf97098bdf4f9ddc172d6386に、全19材料、39保護fileのbefore/after、以下のsiblingを記帳した。

| runtime sibling（いずれも不変） | bytes | SHA256 |
|---|---:|---|
| registered-producer-current-regions-v2.json | 267079 | b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9 |
| registered-producer-body-inheritance-v2.json | 17587 | 768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed |
| v4-run34120585268-registered-canonical-files-v1.json | 1931889 | ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5 |
| v4-run34120585268-registered-canonical-directories-v1.json | 200290 | f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64 |
| v4-run34120585268-final-parent-inventory-registration-v1.json | 7022 | 64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753 |

F5. 九必須引数のstring/mandatory宣言はL2–10の全raw同一。引数順は ArtifactRoot、AcquisitionReceipt、Old64Root、BatchParentRoot、BatchParentArchive、BatchParentV4Root、BatchParentV4Archive、BatchParentV4AcquisitionReceipt、ReceiptPath。新ArtifactRoot/AcquisitionReceipt/ReceiptPathは未登録である。既知六入力の存在・leaf非reparseと二旧ZIPのsizeを確認した。旧rootはTEMPの shadow-atelier-cegar-resume64-run33990567016-candidate-a1、shadow-atelier-fixed-lambda-batch-v3-run34023589045-candidate-a1、shadow-atelier-fixed-lambda-batch-v4-run34120585268-candidate-a1を保持する。ReceiptPathはTEMP内の新規fileで全入力・PSScriptRootの外側という既存条件のまま。

通常mainは読み取りだけのpath/非reparse条件の後、L4062でguard=falseを拒否し、L4063で未登録launch/artifactを再拒否する。旧親preflight L4067、新acquisition読取L4071、全ZIP hash L4096、current fixture復元L4115、最終CreateNew receipt L4624へは到達しない。歴史局所guard=trueは未呼出しfunction内の値であり、通常guardを開放しない。これは静的な制御読了で、実際に拒否を起動した票ではない。通常5executionのexit0要求L4229、三fixtureの全段PASS要求、complete cost要求L4543はそのままで、失敗diagnosticsをcandidateへ適用する入口は追加していない。

F6. 親の現物照合範囲は旧64のmetadata5件＋旧v3/v4 transport各8件、計21 fileの全SHAである。後者16件は受領器の登録bytes/SHAとも一致した。全親payloadや旧ZIP全内容の再hash、親全directory censusは本便では実施していない。**現在の同じ親rootで、1089の過去票が列挙する空directory74件（v3 36＋v4 38）は全件不在**だった。各名が固定済みsaved envelope目録に属すること、.NET Directory.ExistsとTest-Pathの両方が不在を返すことを照合した。parent-registered-pins-and-current-directory-observation-v1.json =74428 B / f11cfc2de572e77cf175ea46c9942cee1247d0bd5bb36a0ebd44e98c7f4691b0へ全名を保存し、rootへ速報した。1089の過去の存在確認を現在の完成rootへ流用しない。欠損の原因は推測しない。

既存preflightはこの欠品を拒否する。旧v4 A2の修理/再起動、親directory作成、skip/cache成功追加は本便に含めず、すべて0である。この現物状態と正式inventory登録の保持、今後のfull typed受領、rootのGHA発射条件を分けた。1093の公開consumerデータフロー、1094の別読・全final pins・配置前通知の閉鎖は親が別途扱い、本票で完了へ格上げしていない。2218はnotify-and-goの契約参照で、未観測の新run承認/launchを捏造する値ではない。実launch/artifactの後着は別の新snapshotに結ぶ。

F7. 最終目録 T/final-material-manifest-v1.json = **5244 B / 966b79805e9f38d2cf654bb255483799d720c1cb0a3e0cf425c38ab8a00001b7**、self/本返信を除く全13 file・3956388 B、subdirectory0。全13材料・旧39保護pin・1094全19材料を最終再照合した。本便の許可済みliteral結合の未接続0、追加本文修理0。一般bodyの再独立監査は主張せず、現sourceと材料をこのpinで凍結する。source/helper/receiver/fixture/cost/Python/GAP/AST/import/compile/dot-source/数学実行、Git/GHA/network/credential/process操作、repo payload配置、新agent起動はすべて0。新数学成功/rank/候補格付けは未観測である。

AUDIT_1096_VERDICT: LIMITED_PUBLIC_LITERAL_BINDING_STATIC_COMPLETE; FULL_FORWARD_REVERSE_EOF_EQUAL; ALL_FIVE_SIBLINGS_RETAINED; CURRENT_LAUNCH_ARTIFACT_NULL; APPROVAL_2218_CONTRACT_ONLY; GUARD_CLOSED; OLD_PARENT_EMPTY_DIRECTORY_READINESS_UNSATISFIED_AND_REPAIR_OUT_OF_SCOPE; NO_SOURCE_OR_RECEIVER_EXECUTION; CANDIDATE_FALSE; CROSS_CHECKED_FALSE; VERIFIED_FALSE.
