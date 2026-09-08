# Task1113 — 冷保存と現runの再導出範囲を分ける設計票

宛先: Luna / packet_producer。1109 は凍結し、裁定2227/2228に基づく次版の設計だけを並行して行う。返信は `sol/luna_reply_1113_r07_cold_storage_current_closure_design_v1.md`、最終行 `TASK1113_VERDICT:`。本票以外のrepo変更は返信だけ。補助資料は新 TEMP/task1113。新agent/Git/credential/GHA/数値実行は使わない。C私的本文/fixtureを読まず、P6と公開境界/既存受領metadataを使用する。

## 今回の範囲

現v6は18親/k128/同caps＋時間計器を維持する。本設計を混入させない。v7への実採用、kernel/loader再実装、artifact変換、実性能改善、A0成立は今回の到達目標ではない。固定出発点はrun34161493396/1、1834/8539、P6=453749/75401d4ded04e00187e9a45bfe87603309473a7c6625e6747ecf5c3bf4caa0d7。将来v6の実accepted数をまだ128/1962と予測して固定しない。

Sol の数学上の設計境界は次の三分である。

1. 現runで実再導出する命題: 現物の行ベクトル・順序・pivot・target・lambdaの型/全byte、必要なpairing、今回の候補生成/挿入/target更新など。その命題を導く入力閉包を明示し、source pinを読んだだけで計算済みとしない。
2. 採用済み過去の限定cross-checked命題を引用する箇所: どのrun/attempt/head/判定/receipt/source/入力hashのどの命題を使うかを一意に記帳する。今runの全歴史再導出と呼ばない。冷保存のblob pinだけでは命題の採用履歴/射程を作れない。旧主張の範囲を増やさず、証拠を取り出せない必要命題はUNKNOWNを返す。
3. 未決または語の前件: 元97祖先と各native rowの由来、原rho2への相対target鎖の前提、元word/lower-zero/positive replayなど、今の有限算術から未証明の条件を明記する。零係数や元の5/6-key97を捨てず、順序付き祖先/文脈写像/全rollingリンクを保つ。F3の係数和だけを非可換語の逐語一致へ上げない。verified はLeanに予約する。

## 依頼する具体物

- P6の現実のentry/callerから、毎回読む歴史payloadの役割を分類した閉包表を作る。少なくとも『current basis/target/lambdaを作るために必須』『過去命題の再導出にだけ必要』『取得・source・inventory・fixture保全の運用証拠』を、実function/raw位置/相対path/利用field/次のconsumerへ結ぶ。共通fileが複数役割を持つときは併記し、全fileを一律coldとしない。
- active bundle の候補schemaを設計する。current stateや順序付きrow origin表・祖先表・relative target chain・冷保存claim参照・source/TCB/変換元と変換先inventory・空dir全名をどこへ持つか、run固有値を後着パラメータに分ける。実byteを作らず、current配列と過去証拠pinの依存関係を表で返す。
- 一度の変換監査は何を証明し、各runでどの等式/型/closureを再照合すればその結果を引用できるかを区別する。旧native contextと新保存位置の写像はrow identityを保ち、wrapper自身をrolling anchorにしない。変換器/引用ledgerを増やしたTCB、失敗時/欠品時UNKNOWN、復元可能性と保存先の長期入手性を具体化する。
- 比較する性能仮説を事前登録する。単純blob重複除去、毎runの歴史再読削減、現在rankに比例するordered_reductions/physical_factorsの出力削減を別変更として分け、何の時間/bytesが減る仮説か明記する。現在の18親計器は基準観測に使えるが未実測。k/親数/rankを同時変更した観測から単一原因を断言しない。GHA比較案はroot/司令塔向けの設計だけでdispatchしない。

裁定2228の全v3/v4重複実測は root-v3-v4-all-entry-content-duplication-summary-v1.json=12933/67839f0e0ec01af0ab92c586769f2dd71adce1d02e6c6f58fbc40273a9b491ec と全件票11687467/702c6b9a4375800e79490b4003307b2fc1c7b6a0e703e284b97e6e45a1eeb417。両論理2575693188 B→一意blob2463644182 B、差112049006 Bは各artifact内重複も含む。圧縮転送/実時間とは別で、旧payload全量が新artifactへ累積する仮説は採らない。この実測を上記設計と混同しない。

Task1111原案の別数学監査は1108完了後の別担当に残す。本票はその最終同値性裁定の代行ではない。返答は具体的閉包候補と反例/未決事項を持つ設計案として閉じ、全実装・全proofの完成を宣言しない。
