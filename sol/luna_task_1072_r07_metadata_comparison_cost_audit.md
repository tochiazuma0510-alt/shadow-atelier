# Task1072 — metadata受領の比較コストを限定点検する

役割: Luna、1071作者の継続。返信は `sol/luna_reply_1072_r07_metadata_comparison_cost_audit.md`（末行 `AUDIT_1072_VERDICT:`）。変更は指定返信と新 `%TEMP%/shadow-atelier-audit163/task1072/` のみ。原1071以下・実入力・repo source/WFは変更しない。20分を目安に静的案または改善不要の結論を閉じ、研究runやartifact到着を止めない。

目的: 前回rootの全metadata受領は約81分を要した。今回はGHAの独立Cが進行中で、完成artifactの受領を準備している。1069/1071の型付き再帰比較 `Same` などについて、意味を変えず、普通のmetadata配列のleafで関数呼出を減らす程度の限定案が有効かを調べる。全範囲を省略する、pin/型/seal/EOF/親/候補/fixture比較を飛ばす案は不可。速さの予測を実測と混ぜない。

基点は1071最終helper260010 B/accc758ebe41c6c5a239245a62beb961ef1f145bf04f3154c6b34442ec774e44。作者最終返信5344/b63186c7248cc97475aee4147656c9c02651027315027ee620d063e6078e46d8。rootは全4行deltaと全raw逆置換を読了/照合済み（root票2795/93bd86080dfa2ecf3cea56c75da2a2afeeae3ff67d94d6db112458e6473d6357）。基点をCreateNew全raw保存する。実Launchは34120585268/1/head92720e53、具体承認2197、Artifact null/guardfalseのまま。

点検範囲を最小化する。`Same` 内のleaf専用経路などだけで十分な改善が得られないなら変更しない結論でよい。全面書換え・C#/Python/AST/compiler・第三者dependency・cacheによる未再読扱い・型幅統一・JSON文字列同値への置換は不可。Int32/Int64、bool、float/decimal、string大小文字、null、空配列/一要素/順序、nested arrays、object key集合/順序/欠品、left/right非対称な型の拒否を保存する。既存Sameの受理/拒否意味と受領時のfail-closedを同じにする。未保存数学前提を加えない。

このtaskに限り、TEMPの小さなPowerShell metadata用fixtureで元と新の比較関数だけを実行して、同じ受理/拒否とコストを測ってよい。全受領器は実行・dot-source・Invoke-Expression・ScriptBlock変換しない。比較関数は全文を見える形でテストscriptへ保存し、数学source/ベクトル演算/証明計算は行わない。合成された型/JSON metadataと、既存公開metadata台帳のopaque構造比較だけを扱う。小さい反例を先に、速度測定はデータ量・反復数・時間上限を事前明記し、数十秒以内の限定測定とする。入力変更/大計算/網羅数学探索なし。必須反例が一つでも変わる案は採用しない。

有効な案がある場合は新versioned helper案 `audit-r07-batch-v4-metadata-v4.ps1` を保存するが、Artifact null/guardfalse・受領器実行0を保持する。全変更関数と行差分を明記し、全保持raw、完全逆置換で基点260010への一致を保存。local benchmarkの実測だけを報告し、実candidate全受領の速度は未測定とする。作者案はrootと独立別読後まで使用不可。改善が不確実なら基点1071をそのまま受領に使うので、本taskの終了を新artifact受領の前提にしない。

新agent/Git/GHA/network/credentials/Python/import/AST/compile/GAP/数学/source実行は禁止（上記の小さなPowerShell metadata比較fixtureのみ許可）。P/C私的数学本文を読まず、著者分離を保持する。返信に入力・script・最終案・比較票の全pin、実行したmetadata fixtureの回数/秒数、受領器未実行、未解決事項を記録する。
