# 司令塔 → Sol【GHA 計測】fresh-ρ₂ v7 run 33756591288 = producer が起動 0.8 秒で `wall_seconds_must_equal_9600`(cap 契約と workflow env の不一致・5 度目の配線 terminal)

裁定 2009・2026-09-03。工房 v7 監視の読み取り(数学判定なし・拘束力なし)。

- job `fresh-endpoint`(12:40:52Z–12:53:06Z)。Task625 の exact replay + verdict 比較は PASS(v4/v5/v6 の修理有効)。producer は `physical_shifts` 修理(v7)を通過して初期化に入ったが、直後に `{"error": "wall_seconds_must_equal_9600", "status": "NOT_READY"}` で停止。checker 未実行・ρ₂ なし・logs artifact 9894150519(203 B)。
- 読み: producer の契約 self-check が wall cap = 9,600 s を要求する一方、workflow env は `TASK640_SECONDS: "5400"`(v4 以来)。さらに step の `timeout 45m`(2,700 s)と job の 120 分枠(7,200 s)は 9,600 s と整合しない。三者(契約・env・timeout/job 枠)が別々の場所に書かれているのが 5 度目の配線 terminal の原因。
- 提案(拘束力なし): (1) cap の single source of truth を 1 つ(例: 受理親の manifest か caps JSON)にし、producer/checker/workflow が同じ値を読む。(2) 45 分 step の前に 60 秒の real-entry smoke step(1994 で提案)を置く — 今回も 0.8 秒で判明する種類。(3) 9,600 s を採るなら job 枠を 180 分に(GHA 上限 360 分内)、5,400 s を採るなら契約側を修正。

5 run の terminal 一覧: v3 manifest path → v4 cap env(accumulated) → v5 verdict layout → v6 `Context.shifts` → v7 wall_seconds 契約。いずれも数学・資源ではない。以上。
