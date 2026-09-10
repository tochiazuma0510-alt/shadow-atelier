# Task1167 — 公開fixture受領部品を1161と並行で完成させる

宛先: Pauli / p6_final_binding、Luna。指定返信 `sol/luna_reply_1167_r07_repair2_public_fixture_receiver.md`、物理最終行 `AUDIT_1167_VERDICT:`。新材料は `%TEMP%/shadow-atelier-audit163/task1167/` のみ。1161/1150や既存sourceを上書きしない。root以外のGit/GHA/network/credentials/既存PID操作・新agentは禁止。

1165/1162は完了した。ここでは新しい限定実装として、公開metadata受領器のfixture部品だけを扱う。数学P/C source、private delta/binder、driver内archiveの展開はしない。source実行/import/AST/compile/selftestは0を保持。stdlibによるraw/text/JSON組立・pin・正逆区間照合だけを許可する。GHAのP/C自己テストはroot実観測では通過し、run34523172734/1、head bf0b5c0b6ee00736481575b98f50ac071fc97e28、本Pは20:00:48Zから進行中。main終了票とartifactは未着。

基準: `R/task1150/receive_current_fixtures_v1.py` 16009 B / 0f536683b45b24f87f95e3f5ca7185cafe98394ddef9b9203dbecf5ec4d9f98f（R=%TEMP%/shadow-atelier-audit163）。root291167で全文別読済み。`receive_fixtures(reader, contract, parent_roles)` の公開interfaceを保持し、新 `receive_current_fixtures_v7.py` を作る。readerは旧受領器と同じread/join/subtree/subtree_model/inventory API、contractのfixture_serializers/selftestsは公開driverの現行metadataであり、補助helper本文を再実行しない。

現public driverは `R/task1166/d972_r07_fixed_lambda_cycle_batch_v7_repair_workflow_driver_final_v2.py` 4457044 B / cc5ce00da2d37f0c56b734d46a4a694fb9c6f0d35e697a9e7ac547748f5aa0df。WF `R/task1166/workflow_repair2_final_v1.yml` 34800 B / 6b71f35b5f2af33bfe38e315db26c1c1bb924868840809f83ee4f51f71eab8ea。これらは公開metadata部分のraw/text参照だけ可、import/AST/compile/実行・embedded archiveのdecodeは禁止。root final採択 `R/root-task1166-final-repair2-adoption-v1.json` 11439 B / 24c2baf417dfd98a880aa3ec7aeb80b8f70df1934b7d00dc07e6c11bf4a84ec1。

必要な差分:

1. logical v7/WF namespaceと共通import `current_metadata_common_v7` へ接続。旧第四/第五群の形・目的・full metadata mutationを保持し、current19親から歴史的17/18親への射影を明示する。**旧helperの `parent_roles[:-1]` は18親時の17親射影であり、current19親へそのまま使わない。** public driverの元順/役割の正確な契約から有限射影する。記号的一括置換や歴史的countの一括変更はしない。
2. 公開P第六群8ケース/C第六群10ケース、各34 files・空directory、P plain ledger/scope、C wrapper/ledgerと全typed keyset/negative mutation/whole file pinsを現public driver契約どおりに追加する。ケース名・expected label・保存目的の配列を全文参照して有限化。元6群の算術selftestを再実行しない。P/Cの数学sourceを参照して不足を埋めない。
3. 根のreaderが全leaseを保持したまま呼ぶ。各subtreeの全files/directories・storage対namespaceの意味、空dir、JSON sealとwhole SHAの区別を保持。helper成功を数学成功としない。selftest native raw/artifact未着なので、fixture PASSを新runに予測しない。
4. contract追加keyが必要なら値/型/producer場所を公開source byte/lineで明示し、Noetherへ渡せる小さなinterface票にする。署名を勝手に変更しない。旧sourceから全正逆raw差分・変更関数全範囲・未変更範囲を出す。公開契約の不足があれば直ちにrootへ報告する。

Noetherは1161のRows/worker/evidence/13義務を担当する。本便の最終source/pin/差分をrootが別読し、Noetherへ接続する。手元の部品を実行して試験しない。実run D3/5 inventory/終了票は入力null、受領器全体はguardclosedのまま。root採択やuser承認待ちを新設せず、静的実装を仕上げる。
