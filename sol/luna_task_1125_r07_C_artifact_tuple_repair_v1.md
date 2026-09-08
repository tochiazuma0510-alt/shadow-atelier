# Task1125 — C6 artifact identity の限定修理・静的差分と実 GHA 正対照

宛先: packet_checker。Luna/C 作者。Task1123 で発見した静的不整合を root が凍結原文から独立確認した。1123 の所見票を先に保存し、本便を優先して完成後に 1123 残作業へ戻る。新 agent 不可。返信は sol/luna_reply_1125_r07_C_artifact_tuple_repair_v1.md、物理最終行 TASK1125_VERDICT:。新材料は %TEMP%/shadow-atelier-audit163/task1125/ のみ。旧1110/1123 source・材料を上書きしない。

F1. 固定入力と裁定
- 未実行 C6: task1110/search/check_d972_r07_fixed_lambda_cycle_batch_v6.py = 419541 B / 3996972ccfe8ba9c168b537ac274de96ff69a6fe27fb400e7de6a8e3a19a52ff。
- 原 C259–262 の FIXED_ARTIFACTS[THIRD_BATCH_ROLE] は (run, attempt, head, full workflow path, id, name, bytes, digest) の8要素。C636–640 artifact_identity は (run, head, id, name, size, digest, workflow basename) の7要素を展開し、attempt=1 と workflow prefix と sha256 prefix を後付けする。既17 role はこの後者文法。
- 通常 C695–706 は全18 role に artifact_identity を呼び、C2855 の第三 native launch も同 helper を呼ぶ。現在は正式 inventory/P6 binding が None なので guardclosed。root は「その guard が正規に開いた後、この helper 到達時に8対7の unpack が失敗する」と静的に裁定する。現在runの実失敗、新数学結果、親artifact不一致を主張しない。
- 第三親の公開実タプルは run34161493396/attempt1/head a5b456a973f8a917f3af386d327061a02a0cf900、workflow .github/workflows/d972-r07-fixed-lambda-cycle-batch-v5.yml、id10034053256、name d972-r07-fixed-lambda-cycle-batch-v5-candidate-34161493396-1、384961441 B、sha256:72e19a87e3a4ca06daa3b1b9dc8a16e76778e6ce1d6bd3a57b25acea363602db、repository_id1312092366、conclusion success。元v5受付17 role＋この第三親の公開API tupleは root-v6-all18-parent-GHA-api-preflight-2230-v1.json = 61944 B / 2d8ff89346629d937f9a2b042dab10895a5f51898ba67113f7e255dc92ee9e38 に18件登録済み。この票はAPI時点照合でpayload再読の代用ではない。事前登録して自系 public metadata として読むこと。

F2. 限定修理
1. 新 task1125 source に C6 全文を複製し、第三 role の定数だけを既17 role と同一の7要素文法へ直す。artifact_identity の本体と旧17 role 定義、公開artifact10字段の意味値、全数学・native body、限度、宇宙は保持する。workflow は basename、digest は bare hex64、attempt は既 helper の1で表現する。新型や別分岐を導入しない。
2. 現在第五metadata selftest 内に、実 production artifact_identity(THIRD_BATCH_ROLE) の返す全10字段を上の独立公開実tupleと比較する正対照を加える。可能なら同位置で全18 role も公開登録18件へ全字段接続する。実helperを呼ばない字句配列の自己一致を正対照としない。正対照を既fixtureの構成に結び、元28拒否の件数/label/負対照body、既[28,9,6,7]群とzero rosterを不変にする。追加正対照のfixture/metadata出力が増える場合はその範囲・数・downstream必要差を先に明示し、勝手にWF/public wireを変更しない。局所source実行は禁止、実通過は後の root GHA まで PENDING。
3. formal inventory と final P6 の2 None、全launch guardを閉じたまま保つ。P6 private実装・中間解法を読まない。最終正式 handback後の1110 bindingの入力を、この新sourceに切り替えることが root 採択待ちの提案になる。
4. 全差分は登録した連続raw置換範囲と元/新offset・bytes・SHA・全文forward/reverse byte一致で提示。無関係な整形・改行変更0。旧source全pin/保持body/全production helper不変、変わるpreambleとselftestの全current/fixture caller分類、影響するpublic consumer/registry raw範囲と新pinを別deltaに記す。旧1123範囲は元pinに結び続け、同一file名へ新sourceを上書きしない。
5. 納品は新未実行source・変更位置表・全18入力tupleの元定義と返すartifact10字段の紙上独立接続・正対照の到達/全key比較/期待label・旧metadata28不変根拠・全材料manifest。追加数学実行や追加TCB採択0。v6の元静的採択は本不整合とこの差分だけ限定訂正し、全旧監査を未了へ巻き戻さない。

PowerShell/.NET の raw/typedJSON/bytes/SHA 編集と静読だけ許可。Python/GAP/AST/import/compile/dot-source/source/selftest/数学実行、Git/GHA/network/credential、旧process/親root操作は禁止。root が唯一のGit/GHA broker。包括GHA認可・notify-and-goは既存のまま。本便は具体的な通常経路欠陥の修理であり、1123やcold-storage設計全体を新v6 gateにするものではない。
