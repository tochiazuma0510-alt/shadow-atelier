# mine 検収レポート -- wall36-cert-20260731

- 生成: 2026-07-31T12:59:51.224295+00:00(UTC)
- plan: `mine/jobs/queue/wall36-cert-20260731.json`
- artifact-dir: `mine/out/wall36-cert-20260731/dl`
- claim_class: `exploration`
- checker cert 出所: (plan.crosscheck.checker_certs_glob 未指定)

machine-piped 規約: 本レポートは cert JSON の値のみから生成した。run.log は参照していない。

## 分類不能な json (1 件 -- artifact-dir 内の無関係な cert。内容は表示しない、パスのみ)

- `mine/out/wall36-cert-20260731/dl\mine\out\wall36-cert-20260731\wall36_cert_20260731.json` (schema/generated_by が本ジョブの様式と一致しない)

## (a) 再現照合 -- artifact cert ⟷ repo 収蔵済み cert(同名ファイル)

較正再走の合否: 主要欄が全一致すれば `REPRO_MATCH`、1つでも不一致があれば `REPRO_MISMATCH`。volatile 欄(elapsed_sec 等)は参考列で判定には数えない。

(artifact 内に GAP explorer window cert が見つからなかった)


## (b) 対付け集計 -- GAP explorer cert ⟷ python checker cert

(対付け対象の窓が見つからなかった)

## 集計まとめ

- 再現照合: 0/0 REPRO_MATCH
- 対付け: agreement 0/0(全窓数 0)

(この集計は候補表記であり、裁定・LEDGER 貼付・地図 delta の確定は人が行う。)


## 付記(collector v0 未対応スキーマの直接抽出 -- machine-piped)

collect.py v0 の `classify()` は `search/strike-a13-ladder.g` 系(ladder)と `ladder-xi-recheck` 系(checker)のみを認識し、WALL 系 cert(`wac_v1-wall28-cert/v1`)は未対応のため上記 (a)/(b) が 0/0 になっている(wall28 型ジョブ共通の既知の v0 制約 -- 未修理)。以下は同一 cert JSON をその場で python で再パースし、フィールド値をそのまま転記したもの(手入力なし)。

抽出コマンド:
```
python -c "import json; d=json.load(open('mine/out/wall36-cert-20260731/dl/mine/out/wall36-cert-20260731/wall36_cert_20260731.json', encoding='utf-8')); print(d['schema'], d['generated_by'], d['n'], d['centralizer_w0'], d['surv_scan'], d['xi_image'], d['provenance'])"
```

出力(=cert JSON からの機械転記値):

- `schema` = `wac_v1-wall28-cert/v1`
- `generated_by` = `search/probe/wac_v1/wall36_cert.g`
- `n` = 36
- `centralizer_w0` = `{'size': 3720, 'structure_description': 'C31 x S5', 'solvable': False, 'derived_length': -1}`
- `surv_scan` = `{'Cv_size': 3720, 'pass_count': 3720, 'hexagon_fail_count': 0, 'generation_fail_count': 0, 'total_checked': 3720}`
- `xi_image` = `{'size': 3720, 'structure_description': 'C31 x S5', 'solvable': False, 'derived_length': -1, 'eq_centralizer_w0': True}`
- `provenance` = `{'gap_version': '4.16.0', 'script_sha256': '61f2bcd551dae2cf32f9e6c0d8453a7aa221b82dbf18464ee86cbdde6e1e3794'}`

**SURV 全数値(実測)**: pass_count = 3720 / total_checked = 3720(Cv_size = 3720)

**予言との対比(参考・判定は司令塔)**: plan の `predictions.declared_none` はチェッカー非接触のまま司令塔便で凍結予言(SURV 全数 pass)を保持する規約。司令塔便で示された値と実測 pass_count = 3720 を並べて事実として記載する(的中/外れの裁定は行わない)。

**注意(事実記載のみ・判定なし)**: `schema` 欄が `wac_v1-wall28-cert/v1` になっている(wall28_cert.g の逐語複製時に window 固有の schema 文字列が更新されず、wall28 のものが残っている可能性)。cert の意味内容(n・witness・centralizer・surv_scan 等)は当該窓固有の値を正しく反映しており(上記参照)、この欄のみの表記不整合と見える。判定・修理要否は司令塔へ。

**verdict 形式問題(裁定253 と同型・対応不要)**: `result.txt` の `verdict=failed`(`gap_exit_code=0`)は run.log 末尾の完走マーカーが `DRIVER_DONE` ではなく `WALL36_CERT_DONE` である形式不一致のみ。計算は完走しており(SURV 全数検算・LID-1 sha256 まで出力済み)、裁定253 §3 の wall28/pentagon-calibration と同型の既知パターン。

