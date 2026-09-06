# Task1005 — 正語P v3 / WF v4、旧refinement HEADの実schemaを読む

宛先: 既存packet_producer。994の現在保存境界と未解決996指摘を記帳し、本便を先に閉じてから994へ戻る。
変更可は新 search/d972_r07_continuation_positive_word_readout_v3.py、新 .github/workflows/d972-r07-continuation-positive-word-readout-v4.yml、新 sol/luna_reply_1005_r07_positive_readout_refinement_head_v3.md のみ。
既凍結P v1/v2、D全旧版、WF v1/v2/v3、991–993/998/999票を変えない。C作者の新本文/票は読まない。ローカルPython/import/AST/数値/GAP/network/git/credential/新agentは禁止。静的読取とmetadataのみ。rootが唯一のgit/GHA broker。

## 観測と原因の区別

WF v3 run33999045563/1、head a324e4b44e3d24def59c901f2dbee758f04369fd、job101394516607はfailure。
source/runtime・新inventory20拒否群・全16 live ZIP・全64歴史・P4/D3群は全PASS。
本Pは23:36:45Z→23:37:05Z、実elapsed19.929537、reason KeyError:'target_remainder_sha256'、phase base-record-closure。
phaseは最後の進捗表示であり、例外行の特定ではない。D本走はskipped、word/Dなし、全取得親/source/raw不変でmissing regular-root二件だけINCOMPLETE。
diagnostics9978952924、3929709 B / 37375ac90e747bec0bc033681383771cf759720f7881a79139f4ba6d1c420db5、root安全展開173file/18539944 B。
TEMP shadow-atelier-positive-readout-run33999045563-diagnostics-a1 のP-stdout.jsonは510 B/c6c1da75f292f8978a79564a0597b7db30547afe0f05b583cbca0d005895ab13。
新metadata群PASSは実payload読了済み: inventory-canary.json2013/3e4353ca6b000ed04015bfe1fac8d5240ecf8e1ba5349930917f35c2c4bc909b、new-canary-result.json1508/22912f6e826c2ac08be02ef33d67a305916e3e1c8bf62ca753ab599837f85810。

工房2163はseed30/seed34のflat key欠落を原因候補としたが、root静読ではP v2 L1242–1245が両方legacy=Trueを指定し、L960–978は当該flat keyを読まない。従ってその仮説を事実として採らない。対象世代をpinだけに縮める案も採らない。
rootが特定した現に不可能な参照はP v2 L1278–1279の ref_head["target_remainder_sha256"]。
凍結 search/d972_r07_full_origin_refinement_v1.py のhead_record L944–951はこの字段を一切保存しない。HEADには全26のstate/rank/generationとstep_manifest_sha256があり、targetは最終stepの実instruction/result/payloadから結ぶ必要がある。
WF v3が実受付したrefinement output/HEADのpinは921 B / 6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba。rootが全ZIP取得後に実HEAD/最終step本文を追配する。現段階は源定義と入口pinを根拠とする候補原因で、最終票は実本文も照合して確定する。

## P v3の修理

P v2 175318 B/cf6ac987acb2f399f36a8438cca78b773d7791286473b68362f2824a35d6451cを新v3へ引き継ぐ。wire schema v1と語13file/11slot/80644・全親・原startは維持。
旧refinement HEADをその実schema/型/全seal/既存source/start/packet/index等のpin結合で明示的に読む。存在しない新字段を仮想的に足さない。
終了の結合は実HEAD completed_steps=26/rank=1385/gen=8090/state_head/kind/step_manifest_sha256と、全26step replayの末尾manifest/instruction/result/target-remainder.binに結ぶ。最終targetを確認する条件を捨てる修理は禁止。旧prefixの全manifest/全target差分/全祖先は従来通り読む。
実HEADと最後の実stepから小さなmetadata fixtureを作り、通常の同じhelperに接続した追加canaryをGHAのselftestへ入れる。実旧HEADが受理され、wrong schema/count(bool含む)/rank/gen/state/last step hash/target hash・存在しない新fieldの後付け等が拒否されること。どこをstrict exact keysにするかは実schemaを読んで固定する。保存親をfixtureへ改変しない。
新metadata群は数値suiteの再走ではない。P既存四群とD三群は新版インターフェース結合として維持可能、旧算術群のfull rerunは追加しない。
read_target_historyのlegacy/packet/refinement/external-E/各保存loopの境界に正確な進捗を置き、例外の実source行が判るstackを通常stderr診断へ残す。localsや環境変数値は出さない。
今回の一点の先にある全旧schema読取も静的に再点検し、同型の確定した欠陥があれば新v3内でのみ直して差分を分けて報告。曖昧なdefault/getやgate削除で通さない。

## WF v4と公開

WF v3 108358 B/04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604を新v4へ。全16数学親/全各pins/64履歴/全raw/runtime/budgets/early before-after/20inventory canary/成功gateを維持。
新P v3、別作者1006のD v3の公開path/全bytes/hashだけroot経由で受領し反映。D数学本文/票を読まない。最終D pin到着までは非凍結とする。
marker [r07-continuation-positive-word-readout-v4-run]。WF schema/path/name/upload/新P群数と全receipt結合を新版へ正確に更新。
v1/v2失敗来歴を保持しv3実失敗run/head/ZIP/source/WFを追加する。診断来歴は第17数学親ではない。
replyは全差分の範囲、実原因の根拠、全bytes/hash/LF、静的修理とGHA未実行の区別を記載し、最終行 AUDIT_1005_VERDICT:。root/1007全文監査後だけ公開する。
