# Task1182 — V8 全受領器の公開4契約を独立分担して完成

宛先: 既存 Pauli / p6_final_binding、Luna。1176/1178/1180の固定材料を保持したまま、Noether/1175の公開契約作成を分担する。新agentは禁止。返信 `sol/luna_reply_1182_r07_v8_full_receiver_public_contract_completion.md`、物理最終行 `AUDIT_1182_VERDICT:`。

Noetherのcontract builderはtool停止により未保存と確認済み。Noetherはlauncher F1179.1→worker→evidenceを担当し、ここでは契約だけを生成する。入力構造の詳細はNoetherから同時に届く。Task1175の指示書を全文読む。

R=`C:\Users\81905\AppData\Local\Temp\shadow-atelier-audit163`。基点は実採用1161の `R/task1161/bound-current-v2/finite-current-input-registration.json`（240530 B / c98dcc6d…）に登録された producer_contract/checker_contract/nested_contract/literal_contract の実D3で、全pinは実登録とroot実採用票から特定する。未採用初稿を基点にしない。新契約は `R/task1182/` にCreateNew/versioned。1175のsource-template-v1は変更しない。

期待schemaは `task1175.P8.public-branch-contract.v1`、`task1175.C8.public-partial-contract.v1`、`task1175.C8.public-nested-metadata-contract.v1`、`task1175.literal-public-metadata-contract.v1`。現7 sourceは従来の schemas/objects/phase_payload_rosters/families の構造と C sources.current を使う。全callerへの構造・型・seal・nullable・current/旧native区別をEOFまで接続する。

current P/Cはroot最終公開opaque D3のみ。P/C private本文・private delta、driver内archiveの展開・target import/execute/AST/compile/selftestは禁止。全公開serializer・最終registry/source/current-count表・root旧親4export・1176公開runtime契約・1178全fixture契約は読める。V8 run34701203323/1/head f799fad95e2560cefda9a8ae8d7b73d575d348b0、20親/current11/54/65/13、737旧ancestry、2090旧rank/gen8795、実追加0..128の前件を維持する。新actual件数/結果・入力guardはnull/falseのまま。128全独立・新rank・新file数の予測は禁止。

全4契約の実基点からのJSON全差分（全文値・型・配列順・削除含む）と全public writer/consumer対応を保存する。巨大なclosure完成まで待たず、完成した契約はpin付きでroot/Noether/Helmholtzへ直ちに渡す。自己全文照合票・全used input fresh pin・有限actual binding残条件を最後に閉じる。著者はroot採用票を作らない。

metadata/raw/text/JSON/hash/tokenizeの作成補助器のみ可。Git/GHA/network/credential/既存PID/数学実行は0。repoは指定返信以外変更しない。承認待ちはない。
