# Task1167 公開 fixture receiver 納品

公開 metadata component を静的に完成した。固定 source は `R/task1167/receive_current_fixtures_v7.py`（R = `%TEMP%/shadow-atelier-audit163`）、31032 B / `34061a8f19e3ea2f4b26563290e61e208b36aafbd599ca669ecd6ad53573288a`。実行・import・AST・compile・selftest は作者側すべて 0。数学 P/C source、private delta/binder、driver 内 archive は参照・展開していない。

`receive_fixtures(reader, contract, parent_roles)` の署名と read/join/subtree/subtree_model/inventory API を保持した。logical v7 / workflow-v7 と `current_metadata_common_v7` に接続し、current 19 roles の元順を固定した。C 第四群は明示的な historical17、P/C 第六群の旧親射影は historical18 を使用する。旧 `parent_roles[:-1]` は残っていない。第五群の歴史的 count・label・元三層 scope は維持した。

旧 16009 B / `0f536683b45b24f87f95e3f5ca7185cafe98394ddef9b9203dbecf5ec4d9f98f` から全 7 raw 差分、15730 B の原 raw を保持する。全正逆再構成と全 EOF を bytes 比較した。旧 nested helper 5 本は全文同一、P 第四・第五群と C 第五群の枝も全文同一、C 第四群は射影式の一箇所だけが変わる。変更された外側関数の全範囲と新 5 関数、全未変更区間は範囲票と raw 差分票へ収録した。

第六群は P 8 件 / C 10 件を公開契約どおり有限化した。両側とも 34 files・13 directories、P は 31 JSON + 3 binary、C は 33 JSON + 1 binary。P plain ledger/scope、C sealed wrapper と plain ledger/rejection、全正対照・単一変異・正しい順序・全 key/type・canonical whole file pin・空 directory を接続した。P の files=1→true、C の ancestry index481 削除、null→0、native49→50 の内外 seal 再計算まで比較する source であり、ordinary helper は再実行しない。

C ledger の `parent1962/<case>/...` は `selftest-fixtures/C` 相対の logical descriptor であり、実保存 subtree `selftest-fixtures/C/parent1962` と区別する。既存 C 支援 JSON の v6 schema はそのまま。P の unsealed typed 境界、C native49 の header/seal と 47 null payload、C 空 directory の observed-array 変異という元 scope を超えない。既存 C 第五群の payload 意味論は元どおり pinned selftest の attestation に留める。

追加 contract key は `fixture_serializers.P_SIXTH_SERIALIZER`、`C_SIXTH_SERIALIZER`、`SIXTH_METADATA_SELFTESTS` の 3 件。値・型・public driver の line/offset/bytes/SHA と consumer 接続を interface v2 に明記した。全 selftest exact11 の `tests[5]` を読み、outer gate は exact15。返却順は従来の P1706/P1834/C1706/C1834 を先頭に保持し、その後へ P1962/C1962 を追加する。

納品材料はすべて `R/task1167/` の CreateNew 保存。

| 材料 | bytes | SHA256 |
|---|---:|---|
| receiver-raw-delta-v1.json | 20558 | 6616f202a89ab17c74bf85ca5c21226e450558b97e8d15f531920822525b1012 |
| receiver-forward-v1.diff | 17724 | f52e0ac08dada4da68ceb314d9d99a018faf54abbaac1ec0847ddc89b3ddba57 |
| receiver-public-source-ranges-v1.json | 9638 | 0bc6f89690696bef2dba4bb846879530db70690517fdfd4c4bc03304acbd160a |
| fixture-receiver-interface-v2.json | 11967 | 6614fef6d961962a9e73b7e3fd4e41e732d6a002e785c5141dfe3e370dbd49ab |
| sixth-public-fixture-catalog-v1.json | 29944 | 6e98da48809539a72b768d47abb1271bda67d21e534721795a2a1658e5419282 |
| public-fixture-serializer-inputs-v1.json | 129186 | d8d4f13b9de836805d33036e2e2e8063cb04825a74bfcdd4883179cff523b454 |

interface v1 は Reader.read の引数説明を `exact_keys` と記したため、実 API 名 `names` に訂正した v2 に置き換えた。source・契約値は不変、v1 も履歴として保存した。納品全 pin は `fixture-receiver-delivery-v1.json` に収録する。

指示書が伝えた root 観測は run `34523172734/1` / head `bf0b5c0b6ee00736481575b98f50ac071fc97e28` の P/C selftest 成功である。本便は GHA を操作・再観測していない。実 main 終了票・artifact D3・正式 inventory5 はこの component の納品入力では null。root が全 lease を保持し、全 receiver の guard も root 所有のまま。新 run の fixture PASS・数学成功はこの静的納品から主張しない。追加承認待ちは設けていない。

AUDIT_1167_VERDICT: STATIC_PUBLIC_FIXTURE_RECEIVER_COMPLETE_NOT_EXECUTED; SIGNATURE_PRESERVED; P8_C10_EACH34_FILES13_DIRS; FULL_FORWARD_REVERSE_RAW_EQUAL; ACTUAL_RUN_INPUTS_NULL; NO_MATH_CLAIM
