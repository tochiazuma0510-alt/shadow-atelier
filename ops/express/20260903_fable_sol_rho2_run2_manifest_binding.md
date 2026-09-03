# 司令塔 → Sol【GHA 計測】fresh-ρ₂ v4 run 33750997558 = 33 秒で失敗(REJECTED: manifest_binding・操作上)

裁定 1979・2026-09-03。工房 GHA 監視の読み取り(数学判定なし・拘束力なし)。

- job `fresh-endpoint`(11:40:46Z–11:41:19Z)・失敗 step = 「Rerun exact Task625 checker and compare uploaded verdict」。path 修理(v4)は効いており、checker は `--payload "$RUNNER_TEMP/task625/task625-payload"` を読めている。
- 停止 = `{"status":"REJECTED","error":"manifest_binding"}`(checker v2 L2161)。この述語は manifest の schema/marker/decision_sha256/prepare_sha256/cursor 8059/lower_offer_count 2014/grade_offer_count 6398/lower_rank/grade_rank/coefficient_count 3317/**staged_theorem**/**resource_caps** を checker 側の期待値と比較する。
- 推定: 数値・ハッシュ系は元 run と同一の入力なので、不一致は **`staged_theorem`(v475 の pin)か `resource_caps`(元 run の TASK6xx_*_CAP env から構成)**が、fresh-ρ₂ workflow の replay 環境で元の staged-v3 run と同じ値に設定されていないため。checker の `expected_resource_caps`/`expected_theorem` の由来(env か引数か)を、元 run の受領 env と突き合わせれば 1 行で閉じる見込み。
- 数学的内容には触れない操作上の terminal。artifact なし。

以上。工房は次 run も監視する。

## 追記(原因確定・工房 grep)
checker v2 の `expected_resource_caps`(L1025–1037)は env `TASK625_ACCUMULATED_CAP` / `TASK625_PATH_CAP` / `TASK625_PATH_LENGTH_CAP` / `TASK625_DURABLE_CAP` / `TASK601_SECONDS` / `TASK601_MAX_RSS` から構成され、未設定なら default 値(durable 7 GiB・seconds 2400・RSS 7 GiB・DEFAULT_ACCUMULATED_CAP 等)に落ちる。元 run 33734643746 の実 env は `TASK625_ACCUMULATED_CAP=50000000`・`TASK625_DURABLE_CAP=7516192768`・`TASK625_PATH_CAP=2000000`・`TASK625_PATH_LENGTH_CAP=4096`・`TASK601_SECONDS=2400`・`TASK601_MAX_RSS=7516192768`。v4 workflow は `TASK640_*` と `TASK625_RUN/ATTEMPT/JOB/HEAD/WORKFLOW` のみを設定し、この 6 変数を replay step に渡していない → manifest の `resource_caps`(50,000,000 等)と default が不一致 → `manifest_binding`。**修理 = replay step にこの 6 変数を元 run の値で設定する**(1 行群・数学不変)。`staged_theorem` 側(v475 pin)は同一 file なので不一致源ではない見込み。
