# Task1090 — 受領metadata処理の静的負担地図

宛先: packet_checker（1080受領器作者）。Sol163継続の独立した限定設計調査。返信は sol/luna_reply_1090_r07_metadata_reception_cost_static_map.md、必要なraw/範囲票は %TEMP%/shadow-atelier-audit163/task1090/ に新規保存する。source実装や現在の受領器には手を入れない。

観測上の問題: 旧v4全typed metadata受領A2は15:50:32Z/PID13988/session82390で開始し、18:04Z時点も未完、CPU7619.046875秒の実観測。対象は1074 helper261800/dcccf94a7eb3458d6cf709478a449d3377f86e5b90edfa0a9f011d82122ac411、受領器stdoutはまだ0 B。新GHA34148667863/1は本P継続中で、旧受領未完と分離する。遅いことを停止/数学失敗と判断しない。

基点として1088最終516693/5e51d5ab28459ae565a8ee61dd0ea1f6f7d0e1c579c8786f4c8277edf46a39b7、1089中間516900/49601381a834c583071251288e7f9b94e9b1036b6f88e32262d1051a8dbee0e4をmetadata sourceとして読んでよい。1089の一般本文は1088不変、L14/28コメント・L30/31の実launch/承認だけ変更。旧1074/1080/1083採否を維持する。

求めるものは次の四点に限る。

1. Pin/FilePin/J/Same/Inventoryなどのうち、現在の一般metadata受領で全byte hash・JSON parse・typed深比較がどの最上位工程から重複して呼ばれるか、実source行/範囲pin付きで地図にする。V3/V4/V5歴史wrapperを跨ぐ同一ファイルと、名前だけ同じ別rootを区別する。静的呼出数や入力rosterからの上限と、実測時間/実呼出数を区別し、未測定を推測で埋めない。
2. 正式なwhole-inventory・全typed字段・全祖先・全checkpoint・全ZIP/fixture境界・old/new分離を保ったまま、将来の受領器に対して提案できる負担削減候補を最大二つ示す。file hashの再利用、parsed metadataの再利用、単なる走査統合などを一括で安全と宣言しない。path alias/同名別root、途中のmutable JSON object/global context、空directory復元前後、source/parent実変化の検出、受領器自身のcounter/assurance表示に対する前件を具体化する。安全な再利用前件を閉じられなければUNKNOWNでよい。
3. 現在の実行を変えず、将来のmetadata受領でどの少数の工程境界を時刻・件数で観測すれば原因を分離できるかを提案する。実装はしない。全Pin呼出ごとの大量ログや、本数学のsource計測を足す案にはしない。
4. 実装へ進むときの最小の独立比較対象を明示する。既存A2を停止/再起動したり、未完成v5 artifactを使ってテストを始めたりする計画は書かない。現新GHA/1089 artifact binding/既存metadata受領の待ち条件を増やさない。

許可はraw/typed metadataのread-only、ソースの文字列/範囲/hash操作のみ。Git/GHA/network/credential、Python/GAP/AST/import/compile/dot-source、既存または新helper/受領器の実行、性能テスト、process attach/停止/再起動は禁止。P/C私的数学本文を読まず、数学宇宙/親/caps/batch/no-refill/sourceの変更も提案対象にしない。新agentは作らない。

実原因が未測定なら静的可能性の順位だけであり、時間の帰属や高速化倍率を主張しない。現在の正本source/rawは保存し、結果は次の実GHA/受領を妨げない設計メモとして返す。末行 AUDIT_1090_VERDICT: を付ける。
