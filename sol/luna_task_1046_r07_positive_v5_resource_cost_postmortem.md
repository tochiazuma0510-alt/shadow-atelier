# Task1046 — positive WF5 の観測資源コストと次の限定修理の静的監査

宛先 packet_bounds_audit。1042完了後に行う、独立の短い診断・設計監査。変更は新 `sol/luna_reply_1046_r07_positive_v5_resource_cost_postmortem.md` と公開metadata集計用TEMPだけ。source/WF/既存票/入力treeは変更しない。ローカルPython/import/AST/GAP/数学実行、GHA/network/git/credential、新agentは禁止。PowerShell/.NETによる全metadata JSONL/bytes/hash/測定値集計とsource静読は可。根拠ある次の限定実装案までを当便の完了範囲とし、実装/GHAを先取りしない。

対象はpositive run34009883488/1、head a590fa9a70322145f1c0688a8f14d2c9640b1bf3。実root `%TEMP%/shadow-atelier-positive-readout-v5-run34009883488-diagnostics-a1`。全ZIP1373772131 B/41c95c7171c9192ec1d589a715c911f7470bb69fe520b80558334ad60636ac61、全406 files/96 dirs/3685457381 Bはroot取得済み。P4=252342/f36e929ee303b968c519e0333d18b10d3c3e01d83b9ad8ec896949d5ca02dd77、D4=232750/41d53b3779e26b04431a033877efbd315eb32b1d4538efa742bf900996db797b、WF5=180687/a840cebcd0ba3f15ff2c31c13b0a09bacd140cb4c8e756466baafd052df8e436。主にP4のprivate index/cacheとliteral-DFSを静読し、必要なD公開ABI境界だけを確認する。

最新局所資源受領票 `%TEMP%/shadow-atelier-audit163/positive-v5-run34009883488-root-resource-metadata-v3.json` =1705905 B/63050c167ba256ab397f3ac0cdcf1a0be5c81baa96ffaf11cd51086e3e8da395、INCOMPLETE_RESOURCE_METADATA、構造errors0/未完記録6。本P2343全telemetry行・Dfixture54全行EOF/型は受領済み、通常Dは未開始。全envelope/16親の別root受領は1044実行中で、局所票を代用しない。巨大parent rosterは画面へ丸出しせずprojectionして必要な字段だけ読む。

実PはUNKNOWN_RESOURCE/literal-DFS/ResourceStop:literal-DFS:deadline、inner5400.275689秒、outer5402.03076秒/exit3。P5400/D10800/7168MiB、outer6000/11400、cache/line64MiB、scratch16GiB、free floor1GiBは元登録のまま。本Pの最後sample2342/elapsed5400.273287329ではVmRSS/VmHWM5285089280 B、index_read139755802122 B、index_write139927942902 B、word_write3287182712 B、8777434 nodes、17446074 edges、cache evictions814139/misses814527/flushes813384。これは実装の論理I/O計数で物理disk byte量やfailure peakではない。全語の総必要node数/残り時間/独立率は未観測。

求める監査: (1) 全sample/相の増分から見える時間・memory/cache/index I/Oの実観測を簡潔に整理、(2) P4の具体的なsource行で各I/O増加へつながる操作を特定し、観測相関と因果の確定を分ける、(3) 同じ旧64起点/同一全literal word/全8059/P1/four-character/全11slot・80644の語義と順序を保持し、資源枠を上げずに次に調べる価値が高い変更を1案に絞る。例えばimmutable recordとmutable countersのアクセスが同一dirty pageを往復させるか等は、実sourceで確かめた場合に限る。単なるcache増量、サンプリング、省略、別数学宇宙、成功親への誤昇格を提案しない。

提案には現在の必須read-before/write依存、候補案の不変量、全word bytes/既存P3・D3との対応と必要な独立照合を明記する。sourceだけでbyte同一や速度改善が証明できない点は未確定として残す。新大規模frameworkや実装全文は不要。次のfresh GHAを今度実行すべきかはrootが全envelope受領と提案を読んで裁定し、k128WF3の現在監査とは独立に扱う。

返信は150行以内を目安に、実file pins/再現用metadata読取とsource行、確定事項・未観測・最小次案を区別して保存する。最終行 AUDIT_1046_VERDICT:。A0実0/1・階段1/6・grade2両NOT_DECIDED・verified=falseは維持。
