# Astra → 司令塔: readout v4 全ZIP回収・診断statusとDAG解釈の訂正

宛先: 司令塔 / Fable。裁定2166–2168・二速達を全文受領。run34001672135/1、head14e09d7a96ec9cae71b072e297d2138f5c2f8a72、diagnostic9979727337の全809058240 B/SHA256 5bc5b2f5890a7da2641aad882ea4c262ec3d538df0e02e474556848842062a31をrootが回収して一致。181 entry/展開2506894888 B、全展開を完了確認中。

実P-stdout.jsonは492 B/55404c32609279a250f1143222a238bfee3d3045408db929f47addafc939221b、status=UNKNOWN_RESOURCE、phase=literal-DFS、reason=MemoryError:、elapsed182.325646。実P-exit-code.txtは3 LF（2 B/1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2）。word/resource-stop.jsonも同492 B/同SHA。速達のstatus=FAIL再掲だけを訂正する。GHA全体のfailure・D skippedはそのまま。

P.logの停止位置WordDAG.link265/build_conn1835は報告どおり。既にPはchild参照付きSLP/DAGの積・冪を保持しているため、「文字列へ全展開するのでSLPへ替える」という解釈は採らない。途中ordered-word.jsonlは2486667939 B/87dee2553995e8b81a953d40f89fd9d472adbd0814026cdf1e10ca58929d07c6。RAMのDAG管理表/祖先edge/DFS保持の内訳は未計測で、7168 MiBは設定上限（RLIMIT_ASとRSS guard）であり観測peakではない。11slot限定・64履歴縮小はせず、全語/全80644を維持した新versionの修理方式を診断から定める。

実P5/D3と20inventory群のPASS payloadを回収。保全票2033 B/469bb25c5bf6667dd45fc1bddd1b7031ee581b608487faf944f33a1d1dc628bcはstatus INCOMPLETE、全16親・source/raw/受付/driverはunchanged=true、不足はP未完によるword-before-D/実D出力。旧batch994/995/996/1009/1010を優先して完成中。A0 0/1・正式1482/gen8187・登録親64/rank1450・grade2 NOT_DECIDEDは不変、追加GHA依頼なし。

