# Task964 — 同一の完全sourceを固定cycle packetにする数学・接続見積り

役: Luna / read-only数学監査・設計。Task961の実completion親待ちの間に実施。
変更可は `sol/luna_reply_964_r07_complete_cycle_packet_feasibility.md` のみ。
ローカル数値/import/AST/GAP/network/git/credential/dispatch/追加agent禁止。
数学式・source/metadata/hashを根拠にし、実時間や未観測rankを捏造しない。

実full-origin候補は26段でrank1359→1385、target18回変化。各scanの非零件数は
増減し、最後の完成scan25でも18602。これだけで残りの反復回数は推定できない。
Task959/960の完全v548 oracleは未走で、Task963は非零witness一個の実体化を調べる。
本便は同じ登録sourceのまま、反復ごとの重複を外す固定packetが可能かを調べる。
実装や新runtime発注はしない。Task961の実親が到着したらそちらを優先する。

v548/v543/v546/v547、正式reply957、Task959公開geometry/witness、Task963を読む。
固定treeの全54433 chordsのうち、tau独立な五本Jを固定すると、各e outside Jで
`k_e = z_e - sum_j (T^-1 tau(z_e))_j z_j` はlambdaに依存しない。
二auxと合わせたsource basisを、同じcanonical sectionで
`G (id - s*pi) Psi(k_e,eta)` へ送ることを検討する。

1. これら全54428+2列と既受理ConnがM2を張ることを、型・完全source前提・
   P1 sectionの前提込みで証明/反証する。完全oracleのsingle witnessにのみ成立する
   特性を固定basis全体に誤って広げない。old504 orbitを混ぜず宇宙は変えない。
2. 固定Phi/section correctionをlambda-free packetとして一回保存し、current row
   reduction/target updateでMEMBERまたは全row Separatorを決めるための最小receiptを
   示す。batchによる新pivotは旧lambdaの非零だけでは独立性を保証しないことを明示。
   全row残差、target係数、literal順序、同一語positive readoutへの接続を保持する。
3. source/physical/P1 lower+top bytesの計算量・I/Oを、既存実ABIの幅と件数の式で
   示す。全decoded source matrixや全8059 lift matrixの常駐を当然視しない。
   edge/tree上の疎性、canonical physical P1画像のcache、block/streamingが実APIで
   どこまで使えるかを調べる。pack/unpackや必要primal solveの支配項を隠さない。
4. 一回のcomplete oracle→一個のE、現在のfull-origin loop、固定complete packetの
   三候補を、追加新source・保持前提・メモリ/I/O式・positive接続の観点で比較する。
   end-to-end実測はまだないので、速いと決めつけず採否判断に足りない計測を最小化。

紙の同値と実装可能性/実runtimeを分け、最終行 `AUDIT_964_VERDICT:`。
