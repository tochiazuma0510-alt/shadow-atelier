# HS NW(7) prereg v3 — Appendix C（容量・回収・resource cap）

- 日付: 2026-08-05
- 正本: `docs/notes/hsp7_mainrun_prereg_v3.md`
- 測定 receipt: `search/certs/hsp7_capacity_noncontact_v2_20260805.json`
- binding negative-matrix receipt: `search/certs/hsp7_binding_negative_matrix_v2_20260805.json`

## C.1 測定対象

各 lane 20,000 行、合計 60,000 行を production cert と同じ header/footer・record field で Python serialization/gzip した。行は `m=-99`、指数 `[9,9,9,9,9,9]`、負 index、`fixture_id=synthetic-noncandidate-*` を持ち、主走 schema に意図的に不適合である。したがって主走候補を一件も含まず、predicate/group 計算も一度も呼ばない。bytes/row は空 cert の header/footer を差し引いた marginal 値である。

これは bytes/row の schema 容量測定であって、主走の速度・圧縮率・実出力サイズの観測ではない。全件値は線形外挿。

## C.2 生値

| lane | 実測行 | raw bytes/row | gzip bytes/row | 全行 raw 外挿 | 全行 gzip 外挿 |
|---|---:|---:|---:|---:|---:|
| S | 20,000 | 176.00015 | 11.30340 | 124,239,922 B | 7,979,711 B |
| V | 20,000 | 274.00015 | 11.57460 | 193,417,749 B | 8,171,164 B |
| P | 20,000 | 231.00015 | 11.19405 | 27,179,406 B | 1,317,675 B |
| 合計 | 60,000 | — | — | **344,837,077 B** | **17,468,550 B** |

## C.3 retention / recovery / cap

- per-shard uncompressed cap: 20 MiB。超過時は upload 前 STOP。truncate/sample はしない。
- lane collection compressed cap: S/V/P 各 680 MiB = 713,031,680 B。workflow の一 lane collect はその lane cap と比較する。
- 三 lane cap 合計: 2,139,095,040 B。whole-class compressed cap 2 GiB = 2,147,483,648 B 以下でなければ class gate で STOP。
- artifact retention: 30日。
- immutable shard cert、parameter manifest、job receipt、join receipt を一組で保持する。
- 回収不能/欠 shard は全体成功に数えず、同じ class/source/range の明示再送だけを許す。自動 retry は禁止。

外挿値は cap より十分小さいが、synthetic 圧縮率が実判定列の圧縮率を保証しないため、cap 判定は各実 shard の upload 前実サイズにも再適用する。

raw/gzip receipt 値、per-shard cap、lane cap、三 lane 合計と whole-class cap、receipt の exact count/unique shard set は pure synthetic negative matrix にも含める。これは cap 配線の tamper 検出であり、上記容量外挿とは別の測定である。

## C.4 preflight receipt

join fixture receipt と capacity/binding receipt は候補非接触で PASS。旧 named registered-wrapper receipt と v2/v3 STOP は歴史記録に限る。superseding source commit `a9a653e9a82f4dd93ca9eabec085a03af931b26e` の exact bytes へ束縛した current-source v4 registered preflight は S=13/V=13/P=8/P5=5、runtime ordered-PCGS material/fingerprint、比較8項目を全 PASS（candidate contact 0）。

main/production shard cert は class freeze の前提ではない。主走認可前にそれを要求すると循環する。v4 registered receipt の PASS により class は `READY_FOR_SOL_FREEZE_REVIEW` へ進むが authorization=false であり、Freeze と S5 Model-Builder dispatch は別裁定である。
