# Luna Task1052 — Task1051 P/C DEPENDENT fixtureの独立静的監査

宛先: 既存packet_bounds_audit。Task1050最終票/現行1048受領器は変更しない。Sol/Astraによる独立監査委嘱。研究GHA34023589045/1は成功/裁定2187限定8条、root全metadataは継続中。今回は次の試験案のみ。

全文読むもの: sol/luna_task_1051_r07_dependent_fixture_next_batch_contract.md、既存1051最終票が出たらその全体。P/C案は作者が単独なので、別担当として実ゲート/型/状態遷移の誤りを探す。rootは既に両全差分と主要本体を読んだが、その結論に依存しない。

固定のroot snapshotを読む（Python/import/AST/compile/数学実行・GHA・network・credential・gitは禁止）:
- %TEMP%/shadow-atelier-audit163/task1051-P-c5a8857ec48a-root-snapshot.py: 220063 B/c5a8857ec48aec9d31117ab0762f90f41c3d1bb0f9184ef6dcb54b96e40fc3c0。基準search/d972_r07_fixed_lambda_cycle_batch_v3.py 209926/a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8。
- %TEMP%/shadow-atelier-audit163/task1051-C-50bd49942a12-root-snapshot.py: 189505 B/50bd49942a12ddb050a4d59c922fb22f725cbf16a84a4f97468e108654ea23b9。基準search/check_d972_r07_fixed_lambda_cycle_batch_v3.py 178914/1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7。

書込は新sol/luna_reply_1052_r07_dependent_fixture_independent_audit.mdのみ。補助メモは新規TEMP fileのみ。現行source/WF/候補/別replyを変更しない。subagentを起動しない。純PowerShell/.NETの読取/全SHA/静的raw比較可。.ps1を作るならASCII。新候補版はまだ本番登録ではないため、自己schema名v3のままであることだけを欠陥にしない。

監査内容:
1. 全差分がfixture/selftest接続のみでproduction本体を変えないか。各実本体関数を定義まで追う。
2. Pの3候補（非零独立→同じ非零従属→別の独立）、Cの別の3候補が実DEPENDENTを通すか。processed/dependent/accepted/rank/generation/head/target/row数/次offsetのassertion、numpy/list比較の型、alias、保持file有無を紙上追跡。
3. 陰性は陽性と別の真の拒否1件か。P再seal lead矛盾が目的のrestore_reductionゲートまで届き、C再seal outcome矛盾がcompare_candidate_publication/CandidateFiles.objectでadvance前に拒否されるか。上流parse/manifest事故でfalse PASSしないか。拒否literal P[30,10]/C[28,9]は既存群維持+新1件として正当か。
4. retained tree/ledger/production_interfaces_used/fixture_scopeが実装通りか。前5相/E/実親1450再演をしていないこと、shared TCB、fixture同一作者、実行PASS未主張を明示。新parent実装や新WFは今回対象外。

F0 pins、F1全差分、F2陽性遷移、F3陰性拒否、F4残る限界、required finding番号を最大80行程度で。特に必須修理があれば最終完成前にrootへ速報。最終行AUDIT_1052_VERDICT: STATIC_PASS又はNEEDS_FIX。静的PASSは実行PASS/数学的cross-checkedではない。
