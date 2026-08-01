# mine 検収レポート -- w98-alg-18cells-20260801

- job_id: `w98-alg-driver-run-20260801`
- run_id: `30700023116`(GitHub Actions run)
- plan: `mine/jobs/queue/w98-alg-18cells-20260801.json`(REPLACE-ME 2箇所 -- `universe.frozen_docs[0].sha256`・`resources.py_driver.sha256` -- を driver 実物の `sha256sum` 値 `991a8c1f0c233999c7d4aa8296fadad09170a8acece8c5f3e9ec92e0b2c4b052` へ機械的に埋めて起票)
- driver: `search/probe/wac_v1/w98_alg_driver.py`(backend=py-ci, 単一プロセス・shard無し)
- 値は全て `result.txt` / cert JSON の機械抽出のみ(手写しなし・判定はしていない)。

## GHA 実行結果原文

- `gh run view 30700023116` -- `plan` ジョブ・`gate-and-run` ジョブとも `conclusion=success`。
- `result.txt`: `verdict=done`、`py_exit_code=0`、`py_done_marker=DRIVER_DONE`(検出済み)、`py_contract=generic`。conclusion と verdict は一致。

## 二環境化(CI cert ⟷ ローカル収蔵 cert)照合

比較対象:
- ローカル(裁定393 で cross-checked 済みとされた収穫元): `search/certs/w98_alg_driver_cert_20260801.json`
- CI(本 job の正式収穫): `scratchpad/w98alg/mine-run-w98-alg-driver-run-20260801/mine/out/w98-alg-driver-run-20260801/w98_alg_driver_cert_20260801.json`

cert 全体は byte-identical ではない(ローカル実行 = Python 3.13.14/Windows・CI = Python 3.14.6/Linux で `route_A_seconds`/`route_B_seconds`(実行時間の実測値)と `provenance.python_version`/`generated_at_utc` が異なるため)。これらの volatile 欄を除外した機械比較:

| 比較対象 | 結果 |
|---|---|
| `cells[ell][a]` の非volatile欄(`T_all`・`route_A/B_contributing_partitions`・`route_A/B_contribution_digest_sha256`・`route_A_partitions_scanned`・`route_B_mu_count`)-- 18セル×10欄=180値 | **180/180 一致** |
| `T_trans[ell][t]`(ALG-3 二項反転由来・18値) | **18/18 一致**(dict全体が `==` で一致) |
| `calibration_small_n` | 一致 |
| `calibration_named`(既知4点: (23,1^3)/(25,1^5)/(37,1^2)T_all/(37,1^2)T_trans) | 一致 |
| `driver_done` | 一致 |
| `marker` | 一致(`DRIVER_DONE`) |
| `script_sha256` | 一致(`991a8c1f0c233999c7d4aa8296fadad09170a8acece8c5f3e9ec92e0b2c4b052`。plan の frozen_docs / py_driver.sha256 とも一致) |
| `formula_id` | 一致 |

**T_trans(18値・機械抽出、そのまま転記)**:

```
ell=37: {0: 2011535710, 1: 2667648126, 2: 3296573904, 3: 4152376800, 4: 3679996320,
         5: 3306663360, 6: 3199996800, 7: 319999680, 8: 639999360}
ell=41: {0: 33331783448, 1: 44662335332, 2: 62687912352, 3: 73359849420, 4: 74011697760,
         5: 83388745440, 6: 60281020800, 7: 35459424000, 8: 21275654400}
```

## 出所整合

- `provenance.script_sha256`(cert内)= plan の `universe.frozen_docs[0].sha256` = `resources.py_driver.sha256` -- 3者一致(driver差し替えなし)。
- wall_seconds_total: ローカル 636.038 秒 / CI 255.697 秒(環境差 -- Linux runner の方が高速。数値自体は volatile 扱いで判定に使っていない)。
- CI 側 `py_result_count_check_actual=0`(汎用契約で `result_count_check` 未指定のため突合スキップ -- plan どおりの想定動作)。

## 集計まとめ

- verdict: done(1/1)、conclusion: success -- 一致
- 二環境化(CI cert ⟷ ローカル cert)の値照合: **非volatile欄 180/180 一致・T_trans 18/18 一致・calibration/driver_done/marker/script_sha256/formula_id 全一致**
- 裁定393 で cross-checked 済みとされた値が、CI 環境(Linux/Python3.14.6)でも独立に再現された(二環境化成立)。

(本レポートは result.txt / 両cert JSON の機械抽出・機械比較のみであり、cert 昇格・LEDGER貼付・裁定は行っていない。)
