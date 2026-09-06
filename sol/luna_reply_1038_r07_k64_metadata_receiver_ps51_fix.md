# Task1038 返信 — k64 metadata 受領器の PS5.1 限定修理

## F1. 完成範囲と凍結値

新 TEMP helper と本返信だけを作成した。指示書 `sol/luna_task_1038_r07_k64_metadata_receiver_ps51_fix.md` は全文読了（2,672 B / SHA256 `d70a03e48b3a93bacd149f93898291a7ffcd839183d38ca3fb3aec90d87b3c64` / LF11）。旧 helper の全文読了を基点として、新 helper の全変更部分・全保持境界・最終全差分を静読した。root が読了した 67,461 B / `2d57b975…` からの最終差分は L360 のコメント一行だけで、復元対象を inner fixture に限定した旧表現を、実際の REPORT 空 directory と二つの由来へ訂正した。機能の追加差分はない。

| 対象 | bytes | SHA256 | LF |
| --- | ---: | --- | ---: |
| `%TEMP%/shadow-atelier-audit163/audit-r07-k64-v2-metadata-v2.ps1` | 67,458 | `dbe203c8606ae65641a8192dc06786ce7046b4d690e30bd79d101dd86091e71f` | 740 |
| 凍結旧 `%TEMP%/shadow-atelier-audit163/audit-r07-k64-v2-metadata.ps1` | 57,448 | `d5dc89bb2f89b27c3a1afc3706d39c8ebbe35d8a5b3bd805c55fe979d54d0fbc` | 641 |

新 helper は ASCII、CR0、BOMなし、最終 LF、末尾空白0。旧1032 helper/返信、全 source/WF、保存済み1037 C/返信は変更していない。1037 C は 178,914 B / `1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7`、返信は 11,196 B / `eb10977969e239795d670ea9c52ae36dce1c0442f6b68a7ff8bc54b5853447ae` のままである。

## F2. 実停止と原因の限界

root の旧受領 session75052 は旧 helper の full SHA guard を通過後、exit1、`raw fixture complete after authenticated empty-directory restoration: missing directory` で停止した。PASS receipt は未形成である。root の事後 scan は REPORT 1,796 directories、fixture 1,185 directories（期待1,217）。不足32は `selftest-fixtures/P/registration/host-0/parents` と `host-1/parents` 自身、および各々の15親 directory であった。これは GHA 数学 FAIL や artifact bytes 不整合を示すものではない。

許可された小さい read-only metadata 確認で、PS `5.1.19041.6456`、旧不足列生成の `List[string]` → `String[32]` → ordinal sort、先頭の正しい絶対 path と `Exists=false` を確認した。その確認では mkdir も full helper も実行していない。この範囲では旧 mkdir が事後 scan に反映しなかった根本理由を確定できず、root の追加指示どおり未確定を維持する。新 helper は計画数、実 CreateDirectory の returned path、各直後 Exists を明示し、次回 root 実行でこの境界を観測する。旧環境や mkdir 一般の障害と断定しない。

確定した別の不足は、inner ZIP 外にも REPORT の空 directory が4件あること、および PS5.1 の実小数型 Decimal が旧測定値 guard の許容型に入っていなかったことである。この二点と受領状態の厳密な区別を限定修理した。

## F3. 復元対象と全認証の順序

実取得票は `%TEMP%/shadow-atelier-audit163/k64-v2-run34011731149-root-acquisition-v1.json`（716 B / `aba4f1113bbb092de013250971b4769026e5edfa24589153c3c5db768d854b24`）。対象は run `34011731149/1`、head `c2a8a6acd60c0cd859edd2e262cfce074b3acaf1`、workflow ID `351332190`、candidate ID `9983058782`、ZIP 187,072,168 B / `26dbf2aed33fa2275d4aaee7436839bcdb4025f2f20b903c30a28116eafca649`。root は outer ZIP 全6,015 entries の EOF/bytes/SHA と全展開を完了済みで、explicit directory entries は0、files6,015、implicit directories1,796、非圧縮 file bytes655,560,727である。新 helper は outer extractor を再実装せず、この取得票・全 ZIP pin・実全 file と結ぶ。

全 REPORT は1,832 directories。読み取った directory 差の内訳は次のとおりで、次回実行の作成数を先取りする値ではない。

| 由来 | 元取得で未形成の directory | 件数 |
| --- | --- | ---: |
| 全 inner fixture ZIP・REPORT・pre-P controls | 上記 host-0/1 の `parents` と、各 `block-0`〜`block-3`, `continuation`, `delta`, `e`, `oracle`, `p1`, `packet`, `prepare`, `refinement`, `seed34`, `state`, `task712` | 32 |
| REPORT・pre-P controls | `ZIP-casefold-extracted`, `ZIP-duplicate-extracted`, `ZIP-traversal-extracted`, `metadata-fixture/empty` | 4 |

後者4件は metadata 拒否 fixture の保存 directory であり、inner fixture ZIP に含まれるとしない。旧1032返信の36件全てを inner ZIP 由来と読める説明は、本返信でこの二由来へ正確化する。各親の数学内容は読んでいない。REPORT の `selftest-fixtures/` projection と inner inventory の全 files/dirs の一致、および4件の pre-P control 所属は read-only metadata で確認した。

新 `PlanDirectories`（L168）は、先行する `RestoreFixtures` の全 inner ZIP entry/正規型/全 bytes/SHA/EOF 認証後に呼ばれる。REPORT inventory の全 file pin に root の二つの除外 file（inventory 自身と run receipt）の実 pin を戻し、全6,015 files・全 bytes を取得票へ結ぶ。全 file 名の祖先集合から元 implicit directory 集合を導き、取得票の1,796と一致させる。期待集合は認証済み REPORT の1,832、fixture 部分は認証済み inner ZIP と完全一致、残る空 directory は pre-P controls と上記4件の exact 集合へ結ぶ。

実集合について「元集合 ⊆ 実集合 ⊆ 期待集合」と全 file の exact roster/hash を要求する。元 directory の欠損、未知余剰、file 置換、reparse、危険な相対 path は拒否する。初回と、認証済み空 directory の一部または全部を既に復元した再受付だけを区別する。冒頭の count 下限だけで合格する経路はない。全対象の絶対 path を先に点検し、`already_restored_directories` と `to_create` を分けた exact partition が完成するまで mkdir はない。

`CreatePlannedDirectories`（L245）は全 REPORT の ordinal 文字列順で親を先に作り、各作成直前に親の実在と対象未形成を再確認する。CreateDirectory の実 returned path と直後 Exists を stderr と観測列へ記録し、期待 path 一致・Exists=true・非 reparse を要求する。実観測件数も計画件数へ一致させる。失敗時に PASS receipt は作らない。続く全 fixture、全前後 inventory、最終全 REPORT 再読を維持し、最後に `元数 + 既復元数 + 今回作成数 = 全期待数` を要求する。既存 file の書換え・削除は行わない。

## F4. PS5.1 小数の限定対応

実 JSON の P elapsed `825.483454`、C elapsed `1023.681667319`、archive elapsed `3.113014172999783`、実行 receipt と child I/O sample の小数はいずれもこの PS5.1 で `System.Decimal` となった。登録 internal/outer/memory は `System.Int32` のままである。新 `FiniteMeasurement`（L44）は Decimal/Double または既存 PlainInt の非負有限値を測定値として許す。通常 P/C、archive、execution、存在する child I/O sample、各 phase telemetry の elapsed にだけ接続した。

`PlainInt`（L43）は旧行と同一の int/long 限定であり、bool/Decimal/Double を普通整数へ変換して認めない。既存 `Same` の scalar type/value 比較、full-file pins、公開 exact fields/typed outcomes は維持する。新一般 parser/canonicalizer、Python float の canonical 再生成、inner seal 再生成はない。新 root receipt の JSON 化は既存 ConvertTo-Json 経路のみである。

## F5. 保持した受領範囲と新 receipt

旧 helper の全15親・全 code/raw source pins・旧64受理入口・全 before/middle/after・P/C新二群と metadata16件・全 output・全 phase/row・head/result/selection/readout/coverage/target/lambda joins を保持した。観測実績は64 selected/processed/independent、rank1,514/gen8,219、Separator、新 lambda oracle null。コードは実全結果から件数と phase を読み、今回の384 candidate phases、3 selection phases、1 final phaseへ接続する。未観測 Linear/CompleteZero は既存の型分岐のままで、存在しない相を要求したり今回実結果と混同したりしない。これらの数学をローカル再演したという主張はない。

新 root receipt の schema は `d972.r07.fixed-lambda-cycle-batch.v2.root-metadata-reception.v2`、成功状態は `PASS_METADATA_ONLY`。`directory_plan`、`already_restored_directories`、今回 `restored_directories`、`directory_creation_observations` と二由来の flags を追加した。receipt は全比較の最後に CreateNew で作り、途中失敗を成功票へ昇格しない。stderr の計画・作成直後観測は、receipt 未形成の停止でも root が回収できる。

裁定2176の限定9条受理は root が別途記帳する。本 helper は `formal_CV9_pending_at_Task1032_preparation=true` と今回 `formal_CV9_pending=false`、root reported ruling2176を別字段にし、`formal_CV9_reassessed_by_this_helper=false` を保持する。数学再演・保持TCB独立性再証明・全A0主張は false、grade2 MEMBER/NONMEMBER は NOT_DECIDED、新 lambda oracle は null、helper の candidate/cross_checked/verified は全て false のままである。

## F6. root 再実行入口と未実行境界

新 helper は未実行。許可された read-only metadata/PS5.1型と旧不足列の小確認、全差分静読、bytes/SHA/EOL点検だけを行った。数学/Python/import/AST/GAP/GHA/network/git/credential、新 agent、P私的 source の読取りは行っていない。root の全文読了後、同じ実 ArtifactRoot を使い、旧未形成票とは別の新 v2 receipt path で次を実行する。

```powershell
$ErrorActionPreference = 'Stop'
$taskHelper = Join-Path $env:TEMP 'shadow-atelier-audit163/audit-r07-k64-v2-metadata-v2.ps1'
if ((Get-FileHash -LiteralPath $taskHelper -Algorithm SHA256).Hash.ToLowerInvariant() -cne 'dbe203c8606ae65641a8192dc06786ce7046b4d690e30bd79d101dd86091e71f') { throw 'Task1038 helper pin drift' }
& $taskHelper `
  -ArtifactRoot (Join-Path $env:TEMP 'shadow-atelier-fixed-lambda-batch-v2-run34011731149-candidate-a1') `
  -AcquisitionReceipt (Join-Path $env:TEMP 'shadow-atelier-audit163/k64-v2-run34011731149-root-acquisition-v1.json') `
  -Old64Root (Join-Path $env:TEMP 'shadow-atelier-cegar-resume64-run33990567016-candidate-a1') `
  -ReceiptPath (Join-Path $env:TEMP 'shadow-atelier-audit163/k64-v2-run34011731149-root-metadata-v2.json')
```

旧停止の根本理由と新 helper 実受領の成否は、次の root 実行結果で記録する。現時点の静的所見に追加必須修理はなく、実受領 PASS は未観測である。

AUDIT_1038_VERDICT: STATIC_METADATA_REPAIR_COMPLETE_ROOT_EXECUTION_PENDING; prior_root_exit1_no_PASS_receipt; mkdir_root_cause_unconfirmed; mathematical_replay=false; candidate=false; cross_checked=false; verified=false.
