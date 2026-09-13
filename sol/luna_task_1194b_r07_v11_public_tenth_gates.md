# Task1194b — 第10公開 selftest gate の既存担当への分担

Task1194 の公開 driver 接続を、既存の Pauli / Helmholtz / Noether の3担当で完了するための追加指示。新agent、対象実行、数学再計算、資源変更は認可しない。既に固定された P/C 最終ソースは変更しない。

Pauli は自分の公開第10全値だけから `producer_parent2474_contract_fixture_gate(entry)` を、Helmholtz は自分の公開第10全値だけから `checker_parent2474_contract_fixture_gate(entry)` を作成し、各担当の TEMP 内に単独小片と基点・全raw差分・公開原典D3を保存する。entry は従来第9と同じ exact2 `{root,selftest}`、戻りは tuple2 `(observed,case_rows)`。P は42 files / 17 dirs / 14 cases、C は40 files / 13 case dirs / 13 cases の自担当公開契約を用いる。相手の私有 source / fixture / 数表は読まない。新fixtureは生成せず、保存された公開通常値と型・全key・全scalar・変異・ラベルを従来の公開比較経路へ結ぶ。

Noether は両小片を通常公開 driver へ統合し、上位 whole fixed9 / test[9] 全値、source / registry / deadline を既存 full gate へ結ぶ。新たな deadline、caps、抜粋比較、fallback、selftest専用数学 clone を追加しない。対象 import / AST / compile / selftest / 本実行は0。有限 author helper は全文確認・pin 後のみ実行する。root が全差分を別読する。

作業場所・著者分離・返信先・Git/GHA の root broker は Task1194 のまま。Noether は他の最終 binding / registry / driver / WF を並行して進める。root source-only 採用票や metadata の後着を理由に、独立作業を停止しない。
