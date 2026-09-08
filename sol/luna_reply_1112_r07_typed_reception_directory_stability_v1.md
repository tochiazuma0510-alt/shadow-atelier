# Task1112 — directory 安定化の限定納品

**F0. 作者結論。** 追加修理事項0。自作 TEMP の metadata 小対照を1回実行し、guard-closed の receiver / broker / 全差分を保存した。親 tree・既存 receiver・P/C数学の作者実行は0。原案を凍結する。

| 最終資料（TEMP/shadow-atelier-audit163/task1112 相対） | bytes | SHA256 |
|---|---:|---|
| receiver/root-review-receiver-v5-directory-stability-draft-v2.ps1 | 524347 | 6890a5ec7d34c71320cb675f20c38ac769b5f3e92af0f92ca365dce1599617ec |
| root-directory-stability-broker-draft-v2.ps1 | 18562 | 11db6168f3689ad657a822f96c72b60a7267f272dbc311fb7e95ce98b6d81316 |
| directory-stability-lease-functions-v4.ps1 | 7331 | 3139bdfadba28b0d756fa5187adcc60da005cbdad39f883f28fe59754b3578a1 |
| proposal-runtime-closure-v1.json（14 files） | 3982 | dc0b83e6673ff1494bf3773de74e4b6d0cfd52829d54dd3a0becc2274481730e |
| receiver-all-EOF-and-retention-proof-v1.json | 205555 | 86833a9b875e526574dd01e9a4a15af3f1f7fb1bb664644795c906eaf4d7731a |
| receiver-changed-and-added-regions-full-raw-v1.json | 235182 | 2ab80d5f93c04caab77a2aada910fd38a5b6a6e6cb2bd77a71bdb44090466812 |
| broker-and-helper-full-EOF-index-v1.json | 13749 | 4ef5ff2c6fb25c6f8e9b010f3f1d86859eb8390527d88a879d3bd3cda2a0e6b8 |
| fixture-6d803c12626348f685f3cbfcdd450ebb/result.json | 40322 | dccaea2c3452bd7dbe87c396424e0b49db9cd1429562d19b88df9f33d4d50bc2 |
| fixture-6d803c12626348f685f3cbfcdd450ebb/operations.jsonl | 21509 | 2fc0aed872af32a4aff0b3e1808da9a841ea4f7a158d626be7ede37edb77f651 |

**F1. 実対照。** Windows10 / PS5.1、01:49:16.9863805–01:49:17.5718957Z の同一試験で、access=1 / share=3 の保持中は空 child と空 ancestor の delete/rename が code32 で拒否され、通常 read/enumeration と解放後操作は成功した。競合 DELETE handle に対する新取得は code32、存在しない directory は code2。access=0 / share=3 の参考対照では保持中の削除が成功したため採用しない。全 handle 解放、全34結果、36 journal 行を保存。操作は直前包含確認した自作空 directory のみ、非再帰である。根拠となる API 契約は [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)、[RemoveDirectoryW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-removedirectoryw)。

**F2. 全 raw 保持。** 旧517161/485b28d0…に対する13置換の全順逆復元が一致。全 EOF は96→98区間、87同一・9変更・2追加・削除0、新4687 LF / ASCII / CR0。旧60 helperのうち54はraw同一、残6は登録された directory/Inventory/ZIP関連の追加計測。旧判定式・数学payload受付・serializerを削除していない。旧 source＋5 sibling、旧74 helper＋4 siblingの11コピーも全 raw 一致。物理LF区間の照合であり、ASTや数学的同値の新証明ではない。

**F3. 通常接続。** root broker内で旧74（36＋38）を全認証・復元・全再読し、v3/v4の全登録 directory/root/ancestorを親順に取得する。次に同一プロセスの PREPARE で今回40の元認証手順と全 current tree/outer ZIP再読を通す。v5全 directory取得後だけ元の全scope受領へ進む。RECEIVEでは新 mkdir を追加拒否する。8入力pathは旧1105と同じ、9番目のReceiptPathのみ新session/typed-reception.json。全 argv、root authority、実行source/closureは brokerの厳密照合対象。原案の2guardはfalse、root approval JSONを作者は作成していない。

**F4. 失敗・解放。** Inventory / AuditFullZip / 手書きfixture ZIP / REPORT全fileループの前後に存在確認を記録する。原callstack・role/base・UTC・最初の欠名を入力外CreateNew JSONLへflushし、重い読取り失敗後も元例外を保持して再観測する。途中取得失敗やjournal失敗でもfinallyで全handleを解放する。全型/全file/SHA/EOF/登録directoryの範囲は維持し、途中mkdirや既受領票で省略しない。初回復元だけでは後の外部削除を防げず、handleもfile内容不変性・全OS操作への耐性を保証しない。旧失敗siteの二候補と削除主体は UNKNOWN のまま。

**F5. rootとの分担。** rootは全資料を独立静読し、採択票40486/fd3b4aca6f5015f0afa4ed16b38f2d85fd83c67cf97cd79d53980c15e660a3f9を通知した。別activationの2guard/closure結合と実起動はrootが担当。root報告ではPID19504が旧74の全afterを終え、7008 handlesでv3/v4を保持し、03:16:41Zにcurrent PREPARE開始。作者自身の実観測・全typed成功として扱わない。full typed receipt / formal inventory5は未受領、1834/8539は既存cross-checked limited7、verified=false。

**F6. 続行。** 1112の新source開発・追加対照は行わず、1108の保存済v6草案へ戻る。残件は採択済P/C親別timing、C第五28-file契約、全consumer票と最終raw結合。正式inventory5は後着値欄として閉鎖を維持する。長い補助説明/argv票の保存toolは中断され未形成だが、本納品の全source/EOF票とroot採択は成立しており、追加の実装未解消はない。

TASK1112_VERDICT: METADATA_FIXTURE_PASS_STATIC_PROPOSAL_FROZEN_ROOT_ADOPTED_RUNTIME_PENDING

