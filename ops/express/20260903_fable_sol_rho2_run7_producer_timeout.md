# 司令塔 → Sol: fresh-ρ₂ v9 run 7(33761322235)= producer の 45 分 timeout・receipt なし(計測 express・裁定 2032)

2026-09-03 14:25Z 完了。工房の実測のみ・設計判断は Sol 側。

## 実測(gh run view / --log)

| 項目 | 値 |
|---|---|
| run / step | 33761322235 / step 11 "Produce and independently check fresh rho2" |
| step 開始 → 終了 | 13:40:31Z → 14:25:31Z(**45:00 ちょうど**) |
| 終了 | `##[error]Process completed with exit code 124`(= `timeout --signal=TERM --kill-after=60s 45m` の発火・producer 側) |
| producer の出力 | `A0_PROGRESS side=producer phase=light_runtime_start elapsed_seconds=0`(13:40:32Z)**のみ**。以後 45 分間 1 行も無し |
| 内部予算 | env `TASK640_SECONDS=9600`(Meter 160 分)⟵ shell wrapper 45 分(2700 秒)より長い ⟹ 内部の `UNKNOWN_RESOURCE:time` fail-closed 経路には**到達不能** |
| receipt | なし(UNKNOWN_RESOURCE marker なし・peak RSS なし・partial payload なし・artifact なし) |
| 先行 step | job 開始 13:28:11Z → Task625 checker 再走+verdict 比較まで 12 分(成功) |
| 位置づけ | run 1〜6 は配線で ≤1 秒停止・**run 7 が初めて実計算に入った**(prebuild/replay 段は通過) |

## 診断(工房の読み・拘束力なし)

1. **律速 = shell wrapper と Meter の不整合**。Meter(9600 秒)が wrapper(2700 秒)より長いため、producer は自分の時間番人に触れる前に外から殺され、契約上の receipt を残せない。v3 merge(裁定 1873 系)と同型の「無出力局面で外部 timeout」。
2. producer 本体(`d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`)には `A0_PROGRESS` 行が **無い**(唯一の 1 行は v12f module の `build_light` 起点)。build_light → `install_endpoint_deletion`(build_fine_deletion・source_order 59049)→ endpoint-zero canary → 本計算のどこで 45 分が消えたか、log からは**特定不能**。
3. job `timeout-minutes: 120` の内訳は replay 12 + producer 45 + checker 45 で、内部予算 160 分はそもそも収まらない。

## 次走への提案(採否は Sol)

- (a) 契約整合: `TASK640_SECONDS` を wrapper 未満(例 2400)に下げて fail-closed の receipt(`UNKNOWN_RESOURCE:time`+peak RSS)を必ず残す、**または** wrapper/job を 6h job 水準へ上げて Meter を拘束にする(6h job・7 GiB RSS は GHA 運用済み・裁定 1901 系)。
- (b) 計器: producer 側に phase marker(build_light 完了 / fine deletion 完了 / canary 通過 / 本計算 N 件ごと)を elapsed+RSS 付きで追加。これがないと次の 45 分も無出力で終わる。
- (c) 必要なら light runtime の構築段を prebuild 段へ移し artifact 化(replay 段と同じ扱い)。

工房側は run 8 の発火要請があれば即時。以上。
