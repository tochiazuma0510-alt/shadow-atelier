# mine 検収レポート -- wall37-cert-20260731-r2

- 生成: 2026-07-31T14:46:39.311646+00:00(UTC)
- plan: `mine/jobs/queue/wall37-cert-20260731-r2.json`
- artifact-dir: `mine/out/wall37-cert-20260731-r2/dl`
- claim_class: `exploration`
- checker cert 出所: (plan.crosscheck.checker_certs_glob 未指定)

machine-piped 規約: 本レポートは cert JSON の値のみから生成した。run.log は参照していない。

## 分類不能な json (1 件 -- artifact-dir 内の無関係な cert。内容は表示しない、パスのみ)

- `mine/out/wall37-cert-20260731-r2/dl\mine\out\wall37-cert-20260731-r2\wall37_cert_20260731.json` (schema/generated_by が本ジョブの様式と一致しない)

## (a) 再現照合 -- artifact cert ⟷ repo 収蔵済み cert(同名ファイル)

較正再走の合否: 主要欄が全一致すれば `REPRO_MATCH`、1つでも不一致があれば `REPRO_MISMATCH`。volatile 欄(elapsed_sec 等)は参考列で判定には数えない。

(artifact 内に GAP explorer window cert が見つからなかった)


## (b) 対付け集計 -- GAP explorer cert ⟷ python checker cert

(対付け対象の窓が見つからなかった)

## 集計まとめ

- 再現照合: 0/0 REPRO_MATCH
- 対付け: agreement 0/0(全窓数 0)

(この集計は候補表記であり、裁定・LEDGER 貼付・地図 delta の確定は人が行う。)


## 付記(collector v0 未対応スキーマの直接抽出 -- machine-piped・W92-9 修理版再走)

collect.py v0 の `classify()` は WALL 系 cert(`wac_v1-wall37-cert/v1`)を未対応のため上記 (a)/(b) は今回も 0/0(collector 側は未修理・driver 側の修理〔裁定290〕とは別件)。以下は cert JSON をその場で python で再パースした値(手入力なし)。

抽出コマンド:
```
python -c "import json; d=json.load(open('mine/out/wall37-cert-20260731-r2/dl/mine/out/wall37-cert-20260731-r2/wall37_cert_20260731.json', encoding='utf-8')); print(d['schema'], d['generated_by'], d['n'], d['centralizer_w0'], d['surv_scan'], d['xi_image'], d['provenance'])"
```

出力(=cert JSON からの機械転記値):

- `schema` = `wac_v1-wall37-cert/v1`
- `generated_by` = `search/probe/wac_v1/wall37_cert.g`
- `n` = 37
- `centralizer_w0` = `{'size': 22320, 'structure_description': 'C31 x S6', 'solvable': False, 'derived_length': -1}`
- `surv_scan` = `{'Cv_size': 22320, 'pass_count': 22320, 'hexagon_fail_count': 0, 'generation_fail_count': 0, 'total_checked': 22320}`
- `xi_image` = `{'size': 22320, 'structure_description': 'C31 x S6', 'solvable': False, 'derived_length': -1, 'eq_centralizer_w0': True}`
- `provenance` = `{'gap_version': '4.16.0', 'script_sha256': '67a8e0ff1e65ec84ca07601d1614a07666a1dc198010c930dfd893d8e1f24bb5'}`

**SURV 全数値(実測)**: pass_count = 22320 / total_checked = 22320(Cv_size = 22320)

**前回走(修理前 driver・run 30627964869)との一致確認**: 前回実測 pass_count = 22320 -> 今回実測 pass_count = 22320 -> 一致(数値は driver 修理〔schema 文字列・完走マーカーのみの変更〕を挟んでも不変のはず、という司令塔の見込みどおり)。

**W92-9 修理確認事項(result.txt / run.log から機械抽出)**:

- `result.txt` の `verdict` = `done`(gap-ci backend の合格状態は文字列 `done`。`passed` は py-ci backend 専用の verdict 文字列であり、gap-ci には存在しない -- ワークフロー実装〔`.github/workflows/mine-dispatch.yml`〕を確認済み。`gap_exit_code` = `0`)。
- `run.log` 内の完走マーカー = `WALL37_DRIVER_DONE`(substring `DRIVER_DONE` を含み、ワークフローの `grep -q "DRIVER_DONE"` 判定に一致 -- 修理前は`WALL37_CERT_DONE` で不一致だった箇所)。
- `schema` 欄 = `wac_v1-wall37-cert/v1`(修理前は両窓とも `wac_v1-wall28-cert/v1` の取り違えだったが、今回は窓別の正しい文字列になっている)。

**結論(事実記載・的中/外れの裁定は司令塔)**: verdict=done・DRIVER_DONE マーカー検出・schema 窓別化のいずれも修理どおりに動作。SURV 全数値は修理前後で完全一致(pass_count = 22320)。

