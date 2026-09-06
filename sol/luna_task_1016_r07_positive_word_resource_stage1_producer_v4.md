# Task1016 — 正語P4・第一段階のdisk管理表と計測

宛先: 既存packet_producer。Task1015公開契約を全文読み、自系Task1012設計に基づき、新 search/d972_r07_continuation_positive_word_readout_v4.py と sol/luna_reply_1016_r07_positive_word_resource_stage1_producer_v4.md だけを作る。旧P3/994/1012/他返信・D/C・workflowは変更しない。他系新source/helper/1013/1017票を読まない。ローカルPython/import/AST/GAP/数値/ネット/git/credentials/追加agentは禁止。source静読・text/bytes/hashのみ可。rootはbatch実GHAの回収と資源設計の最終監査を並行する。

基準P3は200658 B/bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e。実run34001672135/1はUNKNOWN_RESOURCE/MemoryError/literal-DFS/exit3で、7168 MiBは上限、途中word末尾idは全node数や完成rootではない。自己設計1012の最終35442 B/2f9c95971a7a383a8480dc417cb58c32689b92baed7b30d31ca80fe9b970807aを使う。他系の資源結果を予測しない。

今回の必須変更は、WordDAGの全hash/pair表を元IDの固定幅disk表と有界page cacheへ置換し、unused positionsを廃止すること、構築後read_normalized_pairが別の空の自系disk表を作り全wordを独立再読すること、新scratch/資源計測/実helper対照を接続すること。自己案のhash32+二u8を採るなら正確なstride/endian/count/flush/read可視性を明記し、ID/hash/pairの境界をfail-closedにする。__len__/正負indexなど既存利用箇所を全検索し、listだったことによる挙動を落とさない。完成wordの全bytes/node order/Ref/receipt/zero edgeとmod54/18は旧順序のままにする。

今回、factor spool/明示recipe cursor/新streaming serializer/巨大JSON grammar/全面body cache/外部Foxは作らない。従来のWordDAG.product/add・resolve/build_*のadd/yield/send順を保つ。終了済recipe_refsや未使用属性の解放は自系の全使用箇所を静的に根拠付けた範囲だけでよい。未完factors、symbols、ancestor/symbol_order、parent/cache、canonical一行のpeakは残す表と明記する。計測を加えた結果の最大一行/DFS/frame/cache値がまだ無ければnull/未計測とし、完走を約束しない。

新 --resource-selftest は本番disk store/writer/readerを通し、複数pageとeviction/同じnode全bytes/hash/pair、繰返しchild/0・負power/Ref/非unit Act、partial appendとEOF/新scratch path/行資源停止を扱う。固定した旧自系の短い通常helperと実bytesを比較するか具体固定anchorを使い、旧五群丸ごとの再走は不要。既存通常の全親/全64/13fileの通路は変えない。公開WordDAGの数学変更やquietなfallbackはしない。

自己の全source/import closure、private index/schema/CLI/固定cache設定と残存peak、新対照の実入口/期待値/拒否、未実行のAST/selftest/GHAを票に記す。凍結前に全source/票をtextとして読み、全bytes/SHA/行数/CR/BOM/finalLF/末尾空白を返す。実行結果を捏造しない。末行は AUDIT_1016_VERDICT: とする。
