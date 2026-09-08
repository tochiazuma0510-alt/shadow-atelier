# Task1124 — 稼働中の正式受領器の残工程を固定sourceから地図にする

宛先: 既存Luna / packet_bounds_audit。返信は `sol/luna_reply_1124_r07_receiver_remaining_phase_map_v1.md`、最終行 `TASK1124_VERDICT:`。新材料は `%TEMP%/shadow-atelier-audit163/task1124/`。source改善実装の依頼ではなく、稼働中の同一受領器の残工程を把握する読取り専用作業である。

現行v6の最終bindingを最優先する。rootから正式inventory5が届いたら、この追加設計を新しい版で保存して既指定の最終bindingへ戻る。本便はv6追加gateではない。新agent、Git/push/GHA、network/credential、codex exec、既process操作、親の変更・全artifact再走査は禁止。Python/GAP/Lean/source/import/AST/compile/selftest/数学実行は行わない。PS/.NETの原文・JSON metadata・全file pin/指定raw範囲の読取りだけを使う。旧source・指示/返信・TEMP票を上書きしない。repoへの変更は本便の指定返信のみ、新材料は指定TEMPの新規名。末行のVERDICTを守り、全材料のbytes/SHAと完全目録、読了/未読/OPENを明示する。

正式出発点は run34161493396/1、head a5b456a973f8a917f3af386d327061a02a0cf900、1834/8539 cross-checked limited7、verified=false。未来の1962/採用数/λ/停止枝を仮定しない。source実装の不具合と、将来cold設計の未閉鎖義務を混同しない。

## 入力と保護する実process

Task1112のroot-owned broker PID19504、OS-exit monitor PID20272を変更・停止・再起動しない。directory lease/親root/全receiver scope/全旧票を保持する。固定receiver:
`%TEMP%/shadow-atelier-audit163/task1112/root-activation-v1/receiver/root-review-receiver-v5-directory-stability-draft-v2.ps1`
= 524346 B / 89f8eddc42a3b4e594a670b0cc28fafe5fb087ba562f420085bc8a569299dc07。

journal:
`%TEMP%/shadow-atelier-audit163/task1112/root-activation-v1/session-be2ebb260b73445e8d60551bbd3b39b0/directory-stability-journal.jsonl`。
root観測10:10:11Zはseq10639/09:49:41.7589210Z、v4 acquired-audit-historyの6取得台帳Inventory後。callstackはAuditSourceRoster L1538 → ReceiveAuditMaterials L1548 → ReceiveHistoricalV4CompleteEnvelope L2187 → ReceiveNextBatchParentV5 L2878 → top L4262。typed-reception.json/directory-stability-result.json/process-endは未生成。過去観測10556 handlesはjournal由来で、今回新OS handle全列挙をしない。

## 具体作業

1. 自系1112の固定sourceとjournalを事前登録し、最新完全行から実現在地を確認する。journalの途中書込みを完全JSONと扱わない。read-only process CPU/存在の観測はよいが、計測のためsourceを再実行しない。
2. 現在地から正常typed receiptまでの関数/呼出順を原文で追い、v4の歴史受領、v3の全受領、現在v5のmetadata/復元/transport/row/checkpoint/invocation/fixture/保全/最終Inventory等について、実に到達済みと未到達を分ける。関数名だけで何分残る等を予測しない。以前のPREPAREや同labelの別親完了を、現在のRECEIVE完了へ写さない。
3. 重いInventory/全ZIP/巨大typed配列比較の残りcallsiteを可能な範囲で列挙し、繰返しの原因（別root/別段階/別入力契約）を区別する。固定呼出列から証明できることだけを断言し、data-dependent回数/現在の行内位置はUNKNOWN。新timer、cache、scope短縮、旧PASS再利用、typed gate緩和を実装しない。
4. 正常最終receiptの出力schema/required claims、失敗票/例外/finally/handle解放/OS終了との順序、正式inventory5を採択するためrootが次に読む実ファイルを地図にする。現在のP6/C6/driverのNone/false解除条件と結ぶが、未着値は作らない。完了が実に観測されたら残工程票の完成を待たずrootへファイルpath/時刻/最終journalを通知する。
5. 指定raw範囲のpinと、短いpaper＋machine metadataを新規保存する。全sourceを再監査したとしない。既1112静的採択/小対照/前後全原文結合を再実行しない。残工程地図はv6追加gate0、現GHA格付け/数学進捗へ昇格しない。

成果は現在地と出典、確定した残工程、未観測条件、正常/失敗時のroot回収順。source・親・process変更0。
