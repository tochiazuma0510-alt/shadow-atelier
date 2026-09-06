# Task1032 — k64 全成果の metadata 受領準備

F1. 指定の ASCII helper を完成し、静的点検時点で凍結した。`C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/audit-r07-k64-v2-metadata.ps1` は **57,448 bytes / SHA256 `d5dc89bb2f89b27c3a1afc3706d39c8ebbe35d8a5b3bd805c55fe979d54d0fbc` / LF 641 / CR 0 / BOM なし / 最終 LF / 末尾空白 0 / ASCII のみ**。本票とこの新 TEMP helper 以外は変更していない。helper は未実行であり、受領照合の PASS はまだ主張しない。root 全文読了版 57,445 bytes / `1a31c1db537717a4f2d23562b26177a70bcfe6a846e757dd89ecccbe164bfba9` からの最終差分は、directory walker の `foreach ($node in Get-ChildItem ...)` を `foreach ($node in @(Get-ChildItem ...))` と明示した 1 行・3 bytes だけである。

F2. 入力は公開 Task1025 / 1029 / 1030 / 1032、凍結 WF v2（166,471 bytes / `887c779cfa7f00fb780cc8919e2b34140d05ef598038fe4d71e13a0aefa997d5`）、root の実取得票、実保存 metadata とする。旧 19,686 bytes の `audit-fixed-lambda-batch-v1-metadata.ps1` から `Same` / `PlainInt` / full-file pin の経路を再利用した。新しい一般 JSON parser、canonical serializer、Python の float 表現の再現器は作らない。`ConvertFrom-Json` で読む値の型・全字段・参照を照合し、元 file 全 bytes/SHA を認証する。inner seal の識別値と full-file SHA を別に結び、inner seal の canonical 再生成は行わない。算術 helper の import、数値 vector・係数・群作用の再演、AST、Python、GAP、network、git、credential、新 agent は使用していない。P 私的 source / 1026 票は読んでいない。

F3. root から受領した実 run は `34011731149/1`、head `c2a8a6acd60c0cd859edd2e262cfce074b3acaf1`、workflow ID `351332190`、job `101428629158`。全 C 工程は 05:03:56Z success、run は 05:04:55Z 更新で success と通知された。candidate は ID `9983058782`、name `d972-r07-fixed-lambda-cycle-batch-v2-candidate-34011731149-1`、ZIP **187,072,168 bytes / `26dbf2aed33fa2275d4aaee7436839bcdb4025f2f20b903c30a28116eafca649`**。実展開 root は `C:/Users/81905/AppData/Local/Temp/shadow-atelier-fixed-lambda-batch-v2-run34011731149-candidate-a1`。

取得票 `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/k64-v2-run34011731149-root-acquisition-v1.json` は **716 bytes / `aba4f1113bbb092de013250971b4769026e5edfa24589153c3c5db768d854b24`**。schema は `d972.r07.fixed-lambda-cycle-batch.v2.root-acquisition.v1`、top は run / attempt / head / workflow / artifact / zip / extraction と schema の exact 字段。実 outer ZIP は 6,015 entries / 6,015 files / explicit directory entries 0、展開は 1,796 implicit directories / 655,560,727 file bytes。root が全 entry の安全 path・EOF・bytes/SHA と展開後全 file SHA を認証済みである。helper は outer 展開器を作り直さず、実取得票・全 ZIP pin・全展開 inventory を結ぶ。root の別保存 `.all-entry-pins.json`（1,095,117 bytes / `9776b778be5a03ecfd58cbd15a5a26e3c9fe32aa689a4ba2866923ff7ddfe996`）は broker の取得記録であり、本 helper が直接消費する入力ではない。

実 JSON の静的読取では selected / processed / independent は各 64、dependent は 0、rank 1514、generation 8219、kind `Separator`、terminal `BATCH_COMPLETE_CANDIDATE`、新 lambda oracle は null である。これは既に届いた実値の記録であり、helper の固定期待値ではない。helper は rank `1450 + accepted`、generation `8155 + accepted`、selected 0..64、候補順・処理数・採用数から全対象を決める。旧実績 32 / 1482 / 1690 files / 196 phases は新 gate へ移していない。今回の全候補六相は 384、selection 三相と final 一相を含む実 telemetry は 388 件である。受領 helper の成功、新 CV-9 格付け、数学の追加照合をこの静的読取から先取りしない。

F4. 通常入口は全 24 source/raw と driver/WF/runtime、全 15 親の before / middle / after / acceptance、旧実 64 親の 30 entry と内包 completion の 10 entry、全 pre-P control、P output の C 前後不変、実 output inventory を結ぶ。全 execution の start / result / stdout / stderr / exit / argv / ceiling と実 source pin を読む。P と C の新二群は公開 name 順、P 30/8・C 28/7 の全拒否名を保存結果へ結び、metadata 16 の全拒否名と理由も読む。新旧 selftest をこの helper から実行しない。

P stdout / result、C stdout / report、HEAD / final / final checkpoint、fresh invocation 一本の参照と launch / registration / acceptance を照合する。全 selected witness、処理済み候補の全六相、全 row manifest / instruction / target、候補・行・target・state の hash 連鎖を読む。phase の全 descriptor は manifest 全 pin、型・shape・byte length、全 payload SHA/EOF、flat roster へ結ぶ。実使用型 `u8` / `u32le` / `packed3` の bytes は型と shape から照合するが、要素の数学を再計算しない。selection 三相、処理数の六倍の候補相、final 一相が全 telemetry と過不足なく一致することを要求する。Separator / Linear / COMPLETE_ZERO の型を分け、未処理 Linear tail に存在しない phase を要求しない。partial / UNKNOWN / FAIL を完成受領へ昇格させない。

F5. fixture の復元は全認証後の mkdir に限定した。実 `selftest-fixtures.zip` は **2,148,896 bytes / `9a4baef8196d2ca83188762b15df7021aa1ca059a7df4fcb70d63bfe4782dc1b`**。archive receipt、inventory / readback / after、P/C 両 baseline、三時点 comparison、元全 fixture file の pin を先に読む。内 ZIP の全 entry を stream で EOF まで読み、bytes/SHA、型、重複、casefold collision、directory 宣言と全 roster を照合する。全復元先の最終絶対 path と包含、既存 node 型、reparse 不在を mkdir より前に確認し、認証された不足 directory だけを同 TEMP ArtifactRoot 内へ追加する。raw file の上書き・削除や既存異種 node の置換はしない。

outer 取得の 1,796 dirs に対し、実 REPORT inventory は 1,832 dirs なので、差 36 は内 ZIP の empty fixture directory として照合・復元する対象である。件数 36 自体を成功条件に固定せず、実 entry 差分と全再読に結ぶ。archive `PASS` だけでは完成条件にせず、`both_completed_roots_unchanged=true` と全 comparison の完成も要求する。最終 REPORT は `envelope-inventory-before-run.json` と `run-receipt.json` の明示除外二 file だけを補い、全 6,015 files・全 bytes・復元後全 dirs を照合する。hidden tail や未知 payload は黙って除外しない。保存済み file bytes の不変と、追加 dirs が認証済み復元リストだけであることを別々に要求する。

F6. root が最終全文と本票を読了した後に実行するコマンドは以下。ReceiptPath は未形成の新 file を指定する。既存 root 受領票を上書きしない。

```powershell
& "$env:TEMP/shadow-atelier-audit163/audit-r07-k64-v2-metadata.ps1" `
  -ArtifactRoot "$env:TEMP/shadow-atelier-fixed-lambda-batch-v2-run34011731149-candidate-a1" `
  -AcquisitionReceipt "$env:TEMP/shadow-atelier-audit163/k64-v2-run34011731149-root-acquisition-v1.json" `
  -Old64Root "$env:TEMP/shadow-atelier-cegar-resume64-run33990567016-candidate-a1" `
  -ReceiptPath "$env:TEMP/shadow-atelier-audit163/k64-v2-run34011731149-root-metadata-v1.json"
```

成功時だけ `d972.r07.fixed-lambda-cycle-batch.v2.root-metadata-reception.v1` / `PASS_METADATA_ONLY` の新 root 票を CreateNew で保存する。実 P/C/候補相の時間・RSS・I/O・保存量と execution 全測定を元字段のまま記録し、内外 ceiling、プロセス累積 RSS、差分 I/O を取り違えない。失敗時は gate 名で停止し、完成 PASS 票を作らない。復元後の gate で停止した場合、同じ取得前 directory 数への無条件再実行はせず、root が実状態を確認して限定修理または再展開を判断する。

F7. 自己点検は全文静読、実 metadata の限定読取、bytes/SHA/EOL/ASCII の確認までである。helper の実行、実受領 PASS 票、所要秒・RSS の新実測は root 引渡し時点で未形成。root 受領票は `candidate=false / cross_checked=false / verified=false`、数学 replay なし、TCB の独立性の再証明なしを明記する。新 lambda oracle null、grade2 の両字段 `NOT_DECIDED`、full_A0 false、既存 TCB の限界と正式 CV-9 の別判定を維持する。公開 source/WF の凍結は変更しない。

AUDIT_1032_VERDICT: STATIC_METADATA_HELPER_READY; ROOT_EXECUTION_PENDING; NO_LOCAL_MATHEMATICAL_REPLAY; CV9_PENDING.
