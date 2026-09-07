# Task1074 — 実 candidate の metadata 受領器 binding

F1. 実 candidate の取得票を受領し、最終版 `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1074/audit-r07-batch-v4-metadata-v5.ps1` を保存・作者凍結した。261800 B / `dcccf94a7eb3458d6cf709478a449d3377f86e5b90edfa0a9f011d82122ac411`、LF2474 / CR0 / ASCII / BOMなし / 最終LF / 行末空白0。以下、同 directory を T とする。実 artifact exact4 と ImplementationComplete=true を登録した別 snapshot で、子は全受領器を実行していない。root は全差分の独自照合後、この pin で実受領を開始した（F10）。指示書 Task1074 全文と後着の全取得 handoff に従った。

F2. `T/baseline-1072-metadata-v4.ps1` は 261620 B / `a16d8497aafec0cebc6d1c07cc962024ce344854d6d374810e26dc47ce54cb74`。`T/audit-r07-batch-v4-metadata-v5-guardclosed.ps1` は 261599 B / `90f4106ee2acbc99e086cf6f478995a0c7fa375c75e87c481d9edfb381354288`。差分は説明コメント三行だけで、全関数／main／ActualLaunch／承認 2197 は不変、ExpectedArtifact=null / ImplementationComplete=false。三行を戻した全 raw は採用済み基点へ完全一致する。差分票は `guardclosed-whole-raw-delta-v1.json`（1709 / `56790af9edd2138407e7d955cd1154a7ed254fc6305998a088954d349d9037f8`）、全行差分は同 stem の txt（742 / `1b0e84e26a7cffc1581c526b111d7e705e56d21125a298d568c3195dda4fb8f1`）。

F3. `$PSScriptRoot` の file 依存は公開二票だけである。`registered-producer-body-inheritance-v2.json`（17587 / `768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed`）と `registered-producer-current-regions-v2.json`（267079 / `b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9`）を T へ同一 bytes で複写した。それ以外の同変数の利用は TEMP／receipt 配置の安全判定と出典 path の記録のみ。追加の source 本文や動的 import は必要ない。

旧 64 親は `%TEMP%/shadow-atelier-cegar-resume64-run33990567016-candidate-a1`、旧 128 親は `%TEMP%/shadow-atelier-fixed-lambda-batch-v3-run34023589045-candidate-a1`。両 directory と旧 64 の output/HEAD は存在する。旧 128 archive は `%TEMP%/shadow-atelier-audit163/fixed-lambda-batch-v3-run34023589045-candidate-a1.zip`、実 file 長 369233546 B。既存取得票の SHA `781c9f467bd38305c524a0a2bf5b361f45e75bc4234d9cf6e891e01175db9e2e` は本準備で ZIP 全再 hash をしたとの主張ではなく、root の通常受領時に再照合される既存入力 pin である。

F4. root の保存済み API 二票は全 bytes/SHA を照合して T に複写した。`observed-run-final-v1.json` は 13832 / `b8bc02fa50bd6e7eb81567d6fd3a70eccdb02f6bca41bd0e61658be26808998d`、`observed-artifacts-final-v1.json` は 1601 / `eab8eadc76dd609d02d565f1e627e36cb635d9a708005f4317cb5e6918a169d2`。run34120585268/1、head92720e5371164545259c3007cb11e951fa5e1686、workflow351613185／同 active v4 path、push、completed/success と一致する。candidate ID 10020349387 は Int64、API ZIP bytes 377383320 は Int32 として結ぶ案。candidate digest `84040119b08d4ee1e9a3b4524618164172f382f9a97314084131bb9fd0a3cac5` と diagnostics ID 10020372140／別 digest は区別する。API だけで全 ZIP 受領済みとはしていない。

上記初期確認は `pending-artifact-input-and-path-review-v1.json`（5247 / `cfa7305ba23ffa38ff50b6432e56380372d1438f3239cc7c247f2ccef7ab4160`）へ保存した。そこにある未取得／guardfalse は初期段階の実状態であり、同票・guardclosed 版を上書きしていない。最終 snapshot は次の実 handoff 後に作成した。

F5. 実全 ZIP と展開の handoff は root の取得結果に基づく。candidate ZIP は `%TEMP%/shadow-atelier-audit163/fixed-lambda-batch-v4-run34120585268-candidate-a1.zip`、377383320 B / `84040119b08d4ee1e9a3b4524618164172f382f9a97314084131bb9fd0a3cac5`。root は download exit0、全11648 entry の EOF／SHA と全展開 file の読み戻し SHA 一致、extractor exit0 を報告した。実 root は `%TEMP%/shadow-atelier-fixed-lambda-batch-v4-run34120585268-candidate-a1`。取得票は `%TEMP%/shadow-atelier-audit163/v4-run34120585268-root-acquisition-v1.json`、720 B / `c377a2ed0d38d45d53236a8d1952f95d5a20433863fc3d764efda04b4b0caf7c`。同名 `+.all-entry-pins.json` は 2141758 B / `c2ec141eecbc435972d750ae7beb31382c6108ad93ccb698181b311d77390fb3`。両票を全 hash 照合して T に CreateNew 複写した。

取得票は run／attempt／head／workflow ID と candidate ID／name／ZIP bytes／SHA が保存 API と一致した。全 entry 票は 11648 file、総 bytes 1308094050、explicit directory entries=0、取得票の implicit directories=3487。全 entry metadata の普通整数 bytes と SHA 形、全 file 個数と総 bytes を取得票へ結んだ。実 root／ZIP の存在と ZIP の実 file 長も照合した。子が全 ZIP／全展開 payload を再 hash したとの主張はせず、root の完成済み全取得と、本 helper が root 実行時に行う既存 whole ZIP gate を区別する。`crc_independently_checked=false` は原票のままで、独立 CRC 照合済みへ昇格させていない。材料票は `actual-artifact-material-binding-v1.json`（4817 / `a18f6b1da90cf6f3f064aeb06ea8cd3925904efe938cd3a3615393d75d53a98e`）。数学結果／rank の追加判定はしていない。

F6. 最終 helper の基点 1072 からの全差分は次の五行だけである。L10／11／25 は実取得を反映する説明コメント、L26 は下記の exact4、L31 は `$taskImplementationComplete = $true`。id は `[long]` で Int64、ZIP bytes は通常の Int32 literal。実取得 JSON の同二値も、それぞれ System.Int64／System.Int32 と確認した。

```powershell
$taskExpectedArtifact = [pscustomobject]@{id=[long]10020349387;name='d972-r07-fixed-lambda-cycle-batch-v4-candidate-34120585268-1';zip_bytes=377383320;zip_sha256='84040119b08d4ee1e9a3b4524618164172f382f9a97314084131bb9fd0a3cac5'}
```

五行を戻した全 raw は基点 261620 B / a16d8497… に完全一致する。最初の `function Need` 以降の全関数／main 256799 B は raw 不変で SHA `64ca215f6a3094762ceddcd560a4058e4585e350769a38115101899e9bc4ce31`（基点 offset4821／最終 offset5001）。採用済み Same、ActualLaunch／承認2197、source／registry／全親／caps／全 pin／型／EOF gate は不変。完全差分は `final-whole-raw-delta-v1.txt`（1105 / `9c1b0bb30f90222327e477337d3f0b95f7b7111d5bc0d97014eca073edc00ace`）、全逆置換票は `final-whole-raw-delta-v1.json`（3137 / `c25890ad45490df27b8b9e57daeb2c2fdc025dc2f8003a782d2d732a20f4368b`）。

F7. root 用の正確な六引数を `root-command-v1.txt`（1067 / `526b63926c655bcc3566e2fe4209ff4c8bfcb891db86479fffa2827874c3735e`）へ保存した。そこには新 helper の 261800 B／全 SHA guard と以下の実 path を書いた。コマンド text を保存しただけで実行はしていない。

| 引数 | `%TEMP%/` 以降の path |
| --- | --- |
| ArtifactRoot | shadow-atelier-fixed-lambda-batch-v4-run34120585268-candidate-a1 |
| AcquisitionReceipt | shadow-atelier-audit163/v4-run34120585268-root-acquisition-v1.json |
| Old64Root | shadow-atelier-cegar-resume64-run33990567016-candidate-a1 |
| BatchParentRoot | shadow-atelier-fixed-lambda-batch-v3-run34023589045-candidate-a1 |
| BatchParentArchive | shadow-atelier-audit163/fixed-lambda-batch-v3-run34023589045-candidate-a1.zip |
| ReceiptPath | shadow-atelier-audit163/v4-run34120585268-root-metadata-v1.json |

最終 ReceiptPath は root の指定値で、入力 root と helper の T directory の外、準備時点では未形成だった。公開二票は helper の sibling として保持する。通常受領時に認証された REPORT 空 directory を復元する既存射程も変更していない。今回の準備では実入力 directory／file を変更していない。

F8. 全16材料の bytes／全 SHA を `final-static-delivery-v1.json`（4911 / `3a41d6de2fe2884f578cded101e5e44b29a357352246dc558f3344e2d55d1477`）へ固定した。表の file は T 内の相対名で、F2 の初期版・初期差分も保存している。

| file | bytes | SHA256 |
| --- | ---: | --- |
| audit-r07-batch-v4-metadata-v5.ps1 | 261800 | dcccf94a7eb3458d6cf709478a449d3377f86e5b90edfa0a9f011d82122ac411 |
| audit-r07-batch-v4-metadata-v5-guardclosed.ps1 | 261599 | 90f4106ee2acbc99e086cf6f478995a0c7fa375c75e87c481d9edfb381354288 |
| baseline-1072-metadata-v4.ps1 | 261620 | a16d8497aafec0cebc6d1c07cc962024ce344854d6d374810e26dc47ce54cb74 |
| registered-producer-body-inheritance-v2.json | 17587 | 768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed |
| registered-producer-current-regions-v2.json | 267079 | b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9 |
| observed-run-final-v1.json | 13832 | b8bc02fa50bd6e7eb81567d6fd3a70eccdb02f6bca41bd0e61658be26808998d |
| observed-artifacts-final-v1.json | 1601 | eab8eadc76dd609d02d565f1e627e36cb635d9a708005f4317cb5e6918a169d2 |
| observed-root-acquisition-v1.json | 720 | c377a2ed0d38d45d53236a8d1952f95d5a20433863fc3d764efda04b4b0caf7c |
| observed-root-all-entry-pins-v1.json | 2141758 | c2ec141eecbc435972d750ae7beb31382c6108ad93ccb698181b311d77390fb3 |
| pending-artifact-input-and-path-review-v1.json | 5247 | cfa7305ba23ffa38ff50b6432e56380372d1438f3239cc7c247f2ccef7ab4160 |
| actual-artifact-material-binding-v1.json | 4817 | a18f6b1da90cf6f3f064aeb06ea8cd3925904efe938cd3a3615393d75d53a98e |
| guardclosed-whole-raw-delta-v1.json | 1709 | 56790af9edd2138407e7d955cd1154a7ed254fc6305998a088954d349d9037f8 |
| guardclosed-whole-raw-delta-v1.txt | 742 | 1b0e84e26a7cffc1581c526b111d7e705e56d21125a298d568c3195dda4fb8f1 |
| final-whole-raw-delta-v1.json | 3137 | c25890ad45490df27b8b9e57daeb2c2fdc025dc2f8003a782d2d732a20f4368b |
| final-whole-raw-delta-v1.txt | 1105 | 9c1b0bb30f90222327e477337d3f0b95f7b7111d5bc0d97014eca073edc00ace |
| root-command-v1.txt | 1067 | 526b63926c655bcc3566e2fe4209ff4c8bfcb891db86479fffa2827874c3735e |

F9. 作者の変更範囲は本返信と T のみで、元1071／1072／1073、source／WF／全親／実 artifact に手を加えていない。新 agent、Git／GHA／network／credentials、Python／import／AST／compile／GAP／数学／P-C source 実行は 0。子による全受領器の実行・dot-source・Invoke-Expression・ScriptBlock化も 0、1072 fixture の追加再走も 0。guardtrue は実取得を結んだ静的準備の完了を示すだけで、通常受領 PASS や数学 assurance の追加を示さない。採用済み Same の全受領時間への効果も未測定。

F10. root は最終五行と全 raw 逆置換を独自照合し、`%TEMP%/shadow-atelier-audit163/v4-root-1074-final-static-binding-v1.json`（1899 / `642d1952a3b08138aecdc64603f7ac81910daac3aa776aafd6046855bc41c35a`）へ `PASS_EXACT_FIVE_LINE_ARTIFACT_BINDING` を保存した。作者もこの全票と full pin を読了した。root から、指定六引数・同最終 helper による全 metadata 受領を session5057 で開始したとの通知を受けた。結果は本票作成時点で未受領で、root が別に記録する。本 helper／初期案／納品票をこれ以上変更せず、全16材料の最終再 hash 一致も確認して手渡す。

AUDIT_1074_VERDICT: ACTUAL_ARTIFACT_BINDING_FROZEN_ROOT_STATIC_ACCEPTED; FULL_HANDOFF_BOUND; GUARD_TRUE; ALL_FUNCTIONS_MAIN_RAW_UNCHANGED; ROOT_RECEPTION_STARTED_OUTCOME_PENDING; CHILD_RECEIVER_NOT_EXECUTED; ASSURANCE_UNCHANGED.
