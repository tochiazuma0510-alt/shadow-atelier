# mine 検収レポート -- lt-count-13cells-20260801

- 生成: 2026-08-01(手動集約 -- 理由は下記「collector 不適合」参照)
- job_id: `lt-count-13cells-20260801`
- run_id: `30685662252`(GitHub Actions run)
- plan: `mine/jobs/queue/lt-count-13cells-20260801.json`
- 集約 JSON(機械生成・result.txt の key=value と cert JSON の生値をそのまま格納。判定ロジックは追加していない):
  `mine/out/lt-count-13cells-20260801_aggregate.json`
- 集約に使ったスクリプト: `scratchpad/aggregate_lt13.py`(result.txt を parse し cert JSON を glob するだけの機械抽出。予言値・期待値は一切参照していない)

## collector 不適合(先に明記)

`mine/collector/collect.py` を artifact-dir に対して実行したが(`mine/reports/lt-count-13cells-20260801_report.md` へ一度上書き前の出力として `WROTE ... / repro: 0/0 REPRO_MATCH; pairing agreement: 0/0`)、本 job の cert スキーマ(`wac_v1-lt-count-gen-cert/v1`)は collect.py が前提とする「GAP explorer window cert ⟷ python checker cert」の対付けスキーマ(r4 系)と別物であり、0/0 のまま何も拾えなかった。加えて元の GHA 展開ディレクトリ(長パス)では `os.path.isfile` が実ファイルを検出できず parse error になった(Windows MAX_PATH 起因と見られる・診断のみ、判定には使っていない)。そのため作業指示の「無ければ receipt JSON を機械集約」に従い、`scratchpad/aggregate_lt13.py` で result.txt と cert JSON を機械的に束ねた。**collector 自体の改修はしていない**(職務範囲外)。

## 実行結果原文(GitHub Actions)

- `gh run view 30685662252` → 全 13 shard ジョブ + `plan` ジョブとも `conclusion=success`(ワークフロー工程としては 13/13 完走・エラー終了なし)。
- ただし **`conclusion=success` は「ジョブが GHA 上で異常終了しなかった」ことのみを意味し、gap-ci backend の完走判定(`verdict=done`, run.log 内 `DRIVER_DONE` マーカー要)とは別物**。以下の表のとおり、`verdict` ベースでは 1/13 のみ `done`。

## セル別結果表(全て result.txt / cert JSON からの機械抽出値)

| shard(ℓ,t) | 壁時計 elapsed(GHA job) | gap_exit_code | verdict | run.log bytes | DRIVER_DONE | cert 有無 | T_trans | T_all | n | \|C_Sn(w)\| |
|---|---|---|---|---|---|---|---|---|---|---|
| ell37-t2 | 25.8 min | 0 | **done** | 622 | あり | **Y** | **3296573904** | 10643405866 | 39 | 74 |
| ell37-t4 | 22.0 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell37-t5 | 30.2 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell37-t6 | 40.8 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| **ell37-t7** | 51.6 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell37-t8 | 64.2 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell41-t1 | 26.7 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell41-t2 | 42.2 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell41-t3 | 48.3 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell41-t5 | 97.3 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell41-t6 | 150.7 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| **ell41-t7** | 203.0 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |
| ell41-t8 | 270.2 min | 0 | failed | 394 | なし | N | -- | -- | -- | -- |

**標的セル ell37-t7・ell41-t7(S₇ 型・本 job の最優先標的)は共に `verdict=failed`・cert なし。原文報告する。**

### 注記(診断のみ・判定には使っていない)

- `verdict=failed` の 12 shard は全て `gap_exit_code=0`(記録上は GAP プロセスが正常終了扱い)だが `run.log` に `DRIVER_DONE` マーカーがなく、**12 shard 全てが byte 単位で同一の 394 バイト・7 行で切れている**(較正ブロックの出力後、`=== 本番: LT_CELLS = [[ℓ,t]] ===` の直後で ANSI カラーコード列(`\x1b[1m\x1b[34m\x1b[0m\x1b[31m` — GAP の警告/エラー系表示の開始とみられる配色)を最後にログが途切れる)。壁時計は 22 分〜270 分とバラバラなのに切断バイト位置が全 shard で同一という点が不審(ログのバッファリング未フラッシュのまま何らかの理由でプロセス終了した可能性がある、程度の観察に留める)。gap_exit_code=0 という記録自体も、キル後の記録値として信頼できるか不明。
- 較正ブロック(`(23,1^3), n=26, A_26 witness既知`)は ell37-t2 の cert では `pass_t_trans_gt_0: true`(T_trans=173880, T_all=1531110)。他 12 shard は較正ログ行(`較正判定(T_trans>0か): true`)までは run.log に記録されており、較正自体は 12 shard とも通過してから本番セルへ進んだ形跡がある(較正はセルの成否と無関係に先頭で通っている)。
- 出所整合: ell37-t2 cert の `provenance.script_sha256` = `1fa4639d7ef06bc2df02db26ac3098e0af7f8c08475a2663c062741a4dd0a81c` = plan の `universe.frozen_docs[0].sha256` と一致(driver 差し替えなし)。

## fail-closed / 宇宙 assert の通過確認

- 較正ゲート(既知 (23,1^3) 較正で `T_trans>0`)は取得できた 1 件(ell37-t2)の cert で `true`。他 12 shard は cert 自体が生成されていないため cert 上の較正結果は確認不能(run.log の較正行は上記のとおり存在)。
- shard 数: plan 記載 13 / ダウンロード済み 13 -- 一致。
- `SHA256SUMS.txt` は各 shard の `mine/out/.../` 配下に生成されている(内容は集約 JSON には含めていない。原本は artifact 内)。

## 集計まとめ

- verdict: done 1 / failed 12(全 13 shard)
- cert 生成: 1/13
- REPRO_MATCH: 該当 collector 機構が本 job のスキーマに非対応のため 0/0(collector 不適合による。上記参照)
- 標的セル(ell37-t7, ell41-t7): **両方とも未計測(failed・cert なし)**

(本レポートは result.txt / cert JSON の機械抽出のみであり、原因判断・再走可否・裁定は行っていない。以下エスカレーション参照。)
