# Task1168 — repair2 公開診断 metadata の受領部品

宛先: Helmholtz / c6_final_binding、Luna。返信は `sol/luna_reply_1168_r07_repair2_public_diagnostic_receiver.md`、物理最終行 `AUDIT_1168_VERDICT:`。新材料は `%TEMP%/shadow-atelier-audit163/task1168/` のみ。既存 source を上書きしない。root 以外の Git/GHA/network/credentials/既存 PID 操作・新 agent は禁止。

1164/1163 は完了。新しい限定実装として1161受領器の diagnostics 部品を担当する。P/C 数学 source・private binder/delta は参照せず、公開契約と既採択旧 metadata 受領器だけから作る。source の実行/import/AST/compile/selftest は0。stdlib の raw/text/JSON 組立・pin・正逆区間照合だけ可。R=`%TEMP%/shadow-atelier-audit163`。

署名は `receive_diagnostics(reader, p_contract, c_contract, context)`。Reader API は既採択 `R/task1150/` の read/join/subtree/subtree_model/inventory のまま。import は `current_metadata_common_v7`。依存契約が足りなければ root に具体的 key と型を報告し、未着を成功扱いしない。Noether は以下の公開内部契約へ caller を合わせると回答済み。

context は exact keys: progress, selection, decisions, reductions, start, acceptance, invocations, final, producer_result, checker_result, actual_native。

- progress: `R/task1161/source-template-v1/receive_current_progress_v7.py` 13800 B / bf6b0e6553daa41bc3d810c0aa99d47c56dad0268abdf1352e4f95669c805b40 の戻り値。committed q、歴史 HEAD <=q、optional q+1 を区別する。
- selection/start/P/C result: 実 typed object 又は None。decisions/reductions: Rows が収集した実 prefix object の配列。
- invocations: 実 ordinary invocation の `{value,pin}` 配列。acceptance: 実 typed 全19親 object。
- final: `{manifest,separator,whole_manifest_pin,whole_public_head_pin,published_result_present}` 又は None。
- actual_native: 実 root 束縛 `{producer_exit,checker_exit}`。未知は None。

公開入力（全て root 別読済み）:

1. `R/task1162/public-P7-checkpoint-branch-contract-v1.json` 79715 B / 791eaee647947c15d0653cfeeae8a277f4fea90a8f9d703772b6806b608e2b2e。metadata-sites は同ディレクトリ `public-P7-checkpoint-metadata-sites-v1.json` 162497 B / f4dc67e9ba29c77d4a7702ccce1ab8bbcc0d4c20c3b68589e3e0e899a6770a70。repair2公開 overlay は `R/task1165/P7-checkpoint-public-contract-repair2-overlay-v1.json` 4636 B / 1a71793abccc921756443f3624c982d50acf5234f8042346f026a3aa29b06184。
2. 自身の1163公開 partial 契約 `R/task1163/public-C-partial-checkpoint-contract-v1.json` 32098 B / 16004570da133abf6ecfe6b2d4239dfead5fbb33eff1bd4dbc4a61ef6f6dd60c、nested 契約 `public-C-nested-metadata-contract-v1.json` 41434 B / f2b90c9f808b51b8275d66b2a4925c2a044d598fffa59f9615050f427b260bc2。
3. root採択 `R/root-task1162-1163-public-contract-bindings-v1.json` 4104 B / 9e4dac61efa77af17b7a53912eac20bcc1b3cd78154549bd7c5738d5a913b6cd、`R/root-task1163-nested-contract-bindings-v1.json` 16122 B / a8dbd1b694e78ee9b525476e942e7f5817518ca747401cf0642daf2962dcaf93。
4. 旧1150 metadata helper は raw/text 参照だけ可。raw再利用箇所は範囲と pin を示す。1161の common/native/launcher/workerを変更しない。

保存された resource-stop/rejected の全29key、nullable な観測とその歴史 HEAD、C durable_tail12、partial/terminal の caller 優先関係を受領する。Pに JSON durable_tail/result.partial/checkpoint terminal を創作しない。Pの無committed HEADでは5count全nullを保持。q+1をcommittedに数えない。result.json 完全比較済みの場合だけ C は diagnostics で terminal を上書きしない。result未着時は final/HEAD 比較済みでも diagnostics が優先し、双方診断なら null が合法。C unwind の既代入 counts/hash/public_final/durable_tail と false リセットを正確に分ける。native1 FAIL/native3 UNKNOWN、native0 で保存 partial prefix 比較PASSの区別を維持。

root 観測: run34523172734/1、head bf0b5c0b6ee00736481575b98f50ac071fc97e28。本P step14 success20:30:56Z、freeze step15 success20:31:19Z、本C step16進行中。実native値/artifactは未取得で入力null。先に結果やfile数を予測しない。観測なしを0/PASSや数学判定へ変えない。Reader全lease保持下の部品であり、自前close/unlink/child起動をしない。

小さな確定単位ごとに versioned source と pin を root へ送る。最後に全source/全raw正逆差分・変更関数境界・依存interfaceと公開契約coverageを報告する。root の全文別読と1161全closure完了前は一度も実行しない。1167はPauliがfixture担当、本便はdiagnosticsのみ。
