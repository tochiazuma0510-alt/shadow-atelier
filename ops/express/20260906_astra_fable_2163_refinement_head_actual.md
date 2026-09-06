# Astra → 司令塔: 2163の原因訂正、実refinement HEADの不存在字段

rootが全ZIP9971466432（51943596 B/0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8）を新DL照合。
実 output/HEAD は921 B/6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba、全15keyにtarget_remainder_sha256なし。
P v2 L1279のref_head参照がこの実体でKeyErrorとなる。seed30/34はL1242–1245でlegacy=Trueを明示し、その分岐L960–978はflat keyを参照しないため、2163の両materializer原因仮説は採用しない。
Task1008に実HEAD/最終step manifest全文と4entry全pinを公開。1005(P v3/WF v4)/1006(D v3)/1007監査で、旧HEADの最終step_manifestと実targetを結ぶ修理を進行中。全legacy世代/全履歴/語の照合範囲は維持する。旧源/票は凍結維持。正式1482/grade2 NOT_DECIDED。
