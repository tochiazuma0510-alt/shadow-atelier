# Task1043 — positive resource 受領器の実観測型修理 v3

担当 Luna packet_checker。Task1039 の v2 helper 全文と公開返信を基点に、実 root 受領の3 errorsを原因ごとに閉じる。新ファイルは `%TEMP%/shadow-atelier-audit163/audit-r07-positive-v5-resource-metadata-v3.ps1` と `sol/luna_reply_1043_r07_positive_resource_receiver_observed_shapes_v3.md` のみ。旧 v1/v2 helper・返信・実受領票は保存不変。P/D source 私的本文・相手私的返信は読まず、公開 WF5 と実 metadata のみ。ローカル Python/import/AST/GAP/数学実行・GHA/git/credential・新agentは禁止。実 helper 実行は全静読後の root に留保。

基点 v2 は 81,620 B / SHA256 `51fad0e611715799bf9f78dd11b4c302e642da3f2657df43b166e09c6cffbaea` / LF1107。root session85355 は exit1、受領票 `%TEMP%/shadow-atelier-audit163/positive-v5-run34009883488-root-resource-metadata-v2.json` = 1,676,526 B / `222a371e78acbee0f2718874a64279c5dd6ed4901d0419eae3f441083e79563e`、FAIL_RESOURCE_METADATA、errors3/incomplete5。実 artifact root は `%TEMP%/shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1`。run34009883488/1、head a590fa9a70322145f1c0688a8f14d2c9640b1bf3、完全 ZIP 1,373,772,131 B / 41c95c7171c9192ec1d589a715c911f7470bb69fe520b80558334ad60636ac61、406 files/96 dirs/3,685,457,381 uncompressed B、取得票736 B / 1d6d0fcd51bf13941cd55eff1559aa92ca5b0c78bc2a54efea73876e718ee32d。

errors は (1) D_fixture_session: resource_metadata:nonempty_string_array、(2) resource_output_inventories: resource_metadata:exact_fields:label path status inventory completed_arithmetic_inferred、(3) outer_success_to_session_completion: resource_metadata:successful_D_fixture_session。(3) は (1) の派生か独立不足か、実形状とコードで区別して記す。

root は公開 D_SELFTEST-stdout.json の3群を読んだ。第一 disk-catalog-pages-canonical-and-refcounts と第二 same-D3-eight-op-eleven-slot-and-physical の rejected_cases は正常な空配列、第三 scratch-capacity-and-authentication-negatives は20件。空配列を正常に扱い、既存各字段型/全保存fixture/全case語義の公開境界を弱めない。公開されていない D extra keyset や私的 negative catalog を新たに捏造しない。

root は resource-output-inventories.json の全4 rowの実 keys を確認した。OBSERVED P_SELFTEST/D_SELFTEST/P は completed_arithmetic_inferred,inventory,label,path,status の5字段で前者false。NOT_CREATED D は inventory,label,path,status の4字段のみ、inventory=null。型別 exact fields を分け、不存在の完成推論字段を必須にしない。未形成 D を empty successful result にしない。実非空 tree や余剰 file、file/hash差、未知非空 directory欠落は FAIL を維持。

v2 で閉じた PS5.1 Decimal 測定値限定対応・ordinary整数 int/long・bool/floatの区別、全 metadata JSON/JSONL EOFと全 file bytes/SHA、各 binding/cache/index receipt、全 resource inventories、非変更末尾 full scan、空leaf directory不形成の INCOMPLETE 分類を保持。元 incomplete5 は P outer exit3、D未開始、P UNKNOWN_RESOURCE、D session未形成、P index-receipts 空dir欠落。修理後の件数や status は実再実行まで先取りしない。完成票の不足を PASS に変えない。入力treeにmkdirも行わない。新一般 parser/canonicalizer、inner JSON seal 再生成、math replayは行わない。

返信は全差分静読・新 helper全bytes/SHA/EOL/ASCII・実 CLIと新 receipt v3 path・実観測と未観測の区別・残る公開仕様の限界を記す。v3 schema/previous helper pinを正確に更新する。full metadata本文を巨大に表示せず、PS projectionで必要な keys/scalars を選ぶ。全入出力は candidate/cross_checked/verified/math_replay=false、A0実0/1・rung1/6・grade2両NOT_DECIDEDを保持。

root 追補（2026-09-06 06:43 UTC）: 上の『非変更末尾 full scan』はroot文言誤り。基点実装は ScanAll 一回のみ、実票も input_tree_second_full_hash_pass=false。既存全file hash一回と input_tree_written=false / second_full_hash_pass=false を正確に保持し、二回目を新設しない。第三outer join errorは Dsession の成功代入前に非空guardがthrowした派生とsource経路で確認し、外側成功gate自体は変更しない。
