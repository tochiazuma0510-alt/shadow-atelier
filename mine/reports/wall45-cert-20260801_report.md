# mine 検収レポート -- wall45-cert-20260801

- 生成: 2026-08-01T05:00:26.524813+00:00(UTC)
- plan: `mine/jobs/queue/wall45-cert-20260801.json`
- artifact-dir: `scratchpad/mine_dl/wall4045_dl/mine-run-wall45-cert-20260801`
- claim_class: `exploration`
- checker cert 出所: (plan.crosscheck.checker_certs_glob 未指定)

machine-piped 規約: 本レポートは cert JSON の値のみから生成した。run.log は参照していない。

## 分類不能な json (1 件 -- artifact-dir 内の無関係な cert。内容は表示しない、パスのみ)

- `scratchpad/mine_dl/wall4045_dl/mine-run-wall45-cert-20260801\mine\out\wall45-cert-20260801\wall45_cert_20260801.json` (schema/generated_by が本ジョブの様式と一致しない)

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

collect.py v0 の `classify()` は WALL 系 cert(`wac_v1-wall45-cert/v1`)を未対応のため上記 (a)/(b) は 0/0(wall36/37 の前例と同様)。以下は cert JSON をその場で python で再パースした値(手入力なし)。

抽出コマンド:
```
python -c "import json,hashlib; d=json.load(open('mine/out/wall45-cert-20260801/wall45_cert_20260801.json', encoding='utf-8')); print(d['schema'], d['generated_by'], d['n'], d['centralizer_w0'], d['surv_scan'], d['xi_image'], d['provenance'])"
```

### CI run / result.txt(machine-piped key=value)

| verdict | gap_exit_code | run_id | DRIVER_DONE marker (run.log) |
|---|---|---|---|
| done | 0 | 30684889885 | 検出(1件) |

### cert 実測値(機械転記)

- `schema` = `wac_v1-wall45-cert/v1`
- `generated_by` = `search/probe/wac_v1/wall45_cert.g`
- `n` = 45
- `centralizer_w0` = `{'size': 984, 'structure_description': 'C41 x S4', 'solvable': True, 'derived_length': 3}`
- `surv_scan` = `{'Cv_size': 984, 'pass_count': 984, 'hexagon_fail_count': 0, 'generation_fail_count': 0, 'total_checked': 984}`
- `xi_image` = `{'size': 984, 'structure_description': 'C41 x S4', 'solvable': True, 'derived_length': 3, 'eq_centralizer_w0': True}`
- `provenance` = `{'gap_version': '4.16.0', 'script_sha256': 'b93f80817c37744ebfb909d7c21e30c26dd62dfb6215f6d8f0fe540100fa2dec'}`(preflight integrity gate 記載値と一致)
- cert ファイル自体の sha256(今回の出力物) = `a6afdbd9356b5ad60af794a11a75c1d7da7a605e703373f0d626adcd5ba00cd6`

**SURV 全数値(実測)**: pass_count = 984 / total_checked = 984(Cv_size = 984)、hexagon_fail_count = 0、generation_fail_count = 0。

### 凍結予言(984/984)との照合 -- 事実記載のみ(的中/外れの裁定は司令塔)

- plan `mine/jobs/queue/wall45-cert-20260801.json` の `predictions.declared_none` に記載された凍結予言(定理CENTによりSURV全数pass 984/984)と、上記実測値 `pass_count=984, total_checked=984` を突合した結果: **数値は文字どおり一致**(984=984)。この一致が「的中」に当たるか等の裁定は行わない(miner の職務外)。

### 結論(事実記載のみ)

verdict=done・gap_exit_code=0・DRIVER_DONE マーカー検出・SURV 実測 984/984(hexagon_fail=0・generation_fail=0)。smoke(`search/certs/wall45_cert_20260801_smoke.json`, size=984)と本走の centralizer_w0.size は一致(smoke 内の `eq=false` は裁定337注記どおり truncation 由来 -- 本走〔全数〕では `xi_image.eq_centralizer_w0=true`)。
