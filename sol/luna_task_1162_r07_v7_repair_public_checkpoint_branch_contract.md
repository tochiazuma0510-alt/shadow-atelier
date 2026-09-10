# Task1162 — P公開metadataのcheckpoint/partial分岐契約を有限export

宛先: Pauli / p6_final_binding、Luna。1158の限定継続。返信 `sol/luna_reply_1162_r07_v7_repair_public_checkpoint_branch_contract.md`、最終行 `AUDIT_1162_VERDICT:`。新材料 `%TEMP%/shadow-atelier-audit163/task1162/`。既存source/返信を変更せず、P/C実行・import・AST・compile・selftest、新agent/Git/GHA/network/credentialは禁止。自分のP sourceだけをraw/textとして読める。C privateは不可。

1158修理P552885 B/84d257701b1749804b2a4613283b7aab67f2cf14e53f11aa51cf9d3f3ddd82e5を使用したGHA run34518126217/1/head2f8ad063da52da90ed74fd230fb122f96ad79ec7は実行中。原1150受領器のcurrent部分は実128全採用に固定されていたため、Noetherが1161でv7公開writerの実分岐を扱う静的版を先に組立中。自分の1160 driverにあるcomplete-zero/linear-positive/processed0..128は読めるが、Pのresource-stop/rejected/durable-tailと途中phase/checkpointのexact metadata契約が公開資料として不足している。

P sourceの現公開writerから、次の有限schema表をexportする。実結果は予測せず、source pin/全該当関数のbyte/line範囲・各schema/keyのproducer出現位置を全件添える。数学アルゴリズム本文やprivate deltaを公開しない。

1. selection/start/manifest/HEAD/result/checkpointのterminal/status/partial/current processed・accepted・dependent・sequence・ancestry・phase/step・durable_tailのexact keys、ordinary types、nullable条件、seal有無、どの枝でファイルが存在しどの順でdurableになるか。completed/complete-zero/linear-positive/UNKNOWN_RESOURCE・rejectedをsourceに実在する名称で分ける。存在しない枝を捏造しない。
2. checkpointsの6 phasesと公開payload/rows/ordered/reduction/sign/zero/trit metadataの親子key・存在条件・進行上限。G06はmetadataの係数whole SHA/trit/order/source/zero/literal signに限る。u8要素やvector/pairing/solver再計算を要求しない。
3. 旧1150が使うv6 nested契約との比較は、既存P側公開descriptor/serializer票と元v6 Pを必要な範囲だけ読み、現v7同型の項目と変更項目を明示する。64/128や世代数・file countを一括置換しない。受領器自身は書かない。

納品はNoetherがprivate sourceを開かず読める純粋な公開JSON/短い注釈と、その全入力pin・全consumer位置。公開metadata表には実λ係数・未封印の数学値・P private helper本文を含めない。不明項目はUNKNOWNと該当source位置を示し、推測で穴を埋めない。full rawの数学監査をやり直したり、追加のselftestやsource修理を行う必要はない。公開exportの根拠raw/JSONを組立てるstdlib処理のみ可。できた契約表はrootへ先に通知し、Noetherへはrootから渡す。
