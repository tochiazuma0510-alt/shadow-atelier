# Task1030 — k64 WF v2 の公開pinと全fixture保全

これはrootが作者の公開CLI/型と全source差分を読んで著作した1029の補足。相手の私的票/sourceを読む許可ではない。1029の新WF/返信以外は変更しない。

P最終: search/d972_r07_fixed_lambda_cycle_batch_v2.py、208805 B / 6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e / LF3420。
C最終: search/check_d972_r07_fixed_lambda_cycle_batch_v2.py、177544 B / 4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90 / LF2675。
各new selftestの名前/順/topは1025そのまま。P拒否登録数30/8、C28/7で全て未実行。Pには --batch-size 64 を渡す。Cには渡さない。両者の --selftest-root はREPORT/selftest-fixtures/P又はCの新規絶対pathで、sourceは終了時に削除しない。

fixtureには意図して空のsynthetic host directoryもある。全files/empty dirs/hidden tailsを成果物から読み直せるよう、通常の全REPORT uploadに加え、**metadata helperだけで全selftest-fixturesのZIPを作り、全directory entryを明示収録する**。新数学suiteや私的layout依存の一覧を作らない。
試験工程が全成功した時点で各P/C rootの全scanを固定し、main P前/main C前/C後に各subtreeの全files/dirs/descriptorsを完全等値で読む。全REPORTは後の正当な出力追加があるので、REPORT全体の古い全等値を要求しない。旧control baselineの全既存file不変も保持する。
alwaysでその時点の全fixtureを独立inventoryとZIPへ収録し、成功/失敗どちらも残す。P/C未作成又は途中停止は実有無/partialとして記録し、欠けた後続rootを成功や空の完成rootに補わない。成功時だけ二root/事前baselineの完全不変をcandidate gateへ結ぶ。archive名とinventory/receiptはfixture subtreeの外へ置き、自己包含させない。
既存のsafe POSIX名・重複/casefold/type/no-linkと全byte/hashの規則を用いる。全regular fileをstreamで読み、全EOF/bytes/SHAと元scanの一致を要求する。ZIP再読でも全entry集合/全directory entry/全fileの展開bytes/SHA/EOFを全scanへ照合する。可変mtimeやZIP digestだけで元fixtureの不変を主張しない。新archive/receiptの全pinをrun receiptとalways artifactへ結び、raw fixtureも全REPORT内にそのまま残す。
未許可link/typeでscanが拒否した場合はreceiptに実失敗理由を残し、candidateを拒否する。問題entryを黙って除外したarchiveを完全保全PASSにしない。登録された実行/資源枠内で行い、別数学テストを増やさず、この保全の実成否は初回GHAで観測する。

root全read済み基点: P v1→v2の全858行差分＋新canary tree二literal修理、C全991行差分＋最後509 Bの保存row/indent差分。通常数学は保持。新WFの全静的読了と独立監査、実新AST/二群/本P/C/全保存はまだ必要である。
