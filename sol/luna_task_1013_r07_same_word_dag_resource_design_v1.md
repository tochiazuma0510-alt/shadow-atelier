# Task1013 — 独立DのDAG資源設計（静的調査のみ）

宛先: 既存packet_checker。995/1009の完成凍結source/WF/返信は不変。本便は sol/luna_reply_1013_r07_same_word_dag_resource_design_v1.md だけに、正語の独立D v3を資源面から静的に調べて設計案を返す。rootは別に初回batch GHAを投入する。新P本文・Task1012 P設計票・他系helperを読まず、自己の凍結D3と既存公開wire/共通metadataだけを使う。ローカルPython/import/AST/GAP/数値/ネット/git/credential/追加agentは禁止。D4実装・追加実験も本便では行わない。

実観測の共通metadata: 正語run34001672135/1、head14e09d7a96ec9cae71b072e297d2138f5c2f8a72は、Pがliteral-DFSでMemoryError、UNKNOWN_RESOURCE/exit3、内部182.325646秒、実Dは未実行である。D3は176579 B/273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2cで、実自己三群stdout678 B/7ca09522e6f3955fdde2281a7acb0fbb08d3e198f76f30702ad213587decc3beはPASS。これは本語のD成功ではない。

全diagnostic9979727337は809058240 B/5bc5b2f5890a7da2641aad882ea4c262ec3d538df0e02e474556848842062a31。rootの新TEMP shadow-atelier-positive-readout-run34001672135-diagnostics-a1 に全181entry/2506894888 Bを保存済み。途中ordered-word.jsonl全2486667939 B/87dee2553995e8b81a953d40f89fd9d472adbd0814026cdf1e10ca58929d07c6。末尾だけの読取でid6629828/IntegerPower(-1)/child6627615/receipt31792/finalLFを確認したが、全node再parse/連番/完成rootは未認証。実Pは既に参照SLP/DAGである。7168 MiBは上限設定で実peakではない。

調査する範囲:
1. 自系NodeCatalogの全node offsets/hashes/children/uses/symbols、reachability、normalized_pairと各slotのlive値/uses copy、位置読取とcanonical JSON再認証の生存期間・全走査回数・条件付き費用式を明示する。未計測のnode数/edge数/最大一行/同時live FoxRow/support/RSSを推測値で埋めない。
2. 公開八opの同一wireを保ったまま固定幅disk index/streamed child graph/参照数/到達bitset等へ置換する候補を比較する。全canonical bytes、exact六node字段、prior child id/hash、Ref scope、全node reachable（zero power edgeも含む）、同root mod54、全11slotの独立一般Fox則を保つ。node/係数/slot/歴史の省略やzero powerの子検査省略は不可。Actのconjugatorをunitと仮定しない。
3. authenticated catalogと各slotの値をどこまで一時diskへ退避できるか、共有live値のaliasとlast-use解放が正しいこと、partial index/cacheを正語の13file/成功Dへ混ぜず全保全する境界を提案する。P系のcache/codec/helperを流用せず独立実装を保つ。
4. メタデータのRAM削減だけでは全11slot/80644が予算内とは限らない。実D未到達の現状を維持し、D4へ進む前後に必要な最小のGHA計測（全経路に効くsource/fixture、peak/live/edge/IO/parseの実counter）と新通常helperの対照を提案する。今回は実行しない。

全16数学親/全64履歴/同語13file/11slot/full80644/normalized mod54/非unit Act/5 PB4 endpoint/全sourceと入力before-afterを保持する。batchは別の15親/64rank1450/k32/1/refill=falseであり、995/WF1009を本調査で変えない。新算術、grade2/A0、速度成功、Lean verifiedの宣言はしない。返信末行は AUDIT_1013_VERDICT: とし、実観測・静的推論・未計測を区別する。
