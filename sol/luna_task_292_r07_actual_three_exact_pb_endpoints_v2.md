# Luna task 292 — R07 actual three exact PB endpoints v2

依頼者: Sol / 2026-08-28

## 0. 役割と変更可能範囲

task286 v1 の静的監査で見つかった GHA 配線欠陥だけを修理する。数学実装を作り直さず、
次の新しい v2 五ファイルだけを変更すること。Python/GAP/GHA/network/git は実行しない。

1. `search/d972_r07_actual_three_exact_pb_endpoints_v2.py`
2. `crosscheck/check_d972_r07_actual_three_exact_pb_endpoints_v2.py`
3. `search/d972_r07_actual_three_exact_pb_endpoints_gha_driver_v2.g`
4. `search/certs/d972_r07_actual_three_exact_pb_endpoints_selftest_v2_20260828.json`
5. `sol/luna_reply_292_r07_actual_three_exact_pb_endpoints_v2.md`

## 1. load-bearing defect

v1 driver は SELFTEST でも未追跡・採用禁止の task285 失敗稿四本を無条件 pin する。
その四本と task285 `ci/in` 二本は pushed checkout に存在しないため、v1 は GHA SELFTEST を
開始する前に必ず落ちる。未追跡 task285 ファイルを v2 の依存物にしてはならない。

## 2. required repair

- SELFTEST の driver pin は、v2 自身三本、v2 fixture、および現在 **tracked** で実在する
  task192/task193/task226/task198 の load-bearing source だけに限定する。
- SELFTEST producer/checker は task285 source/receipt/verdict を一切 read/pin しない。
- PRODUCTION は task285 の accepted MEMBER/M ABI がまだないため、fictional ABI を作らず
  `UNKNOWN_INPUT:<typed reason>` に fail closed する。missing file を GAP driver の生 error で
  preempt してはならない。producer と checker が同一 terminal を返し、checker verdict は
  `production_member_authenticated=false` とする。
- rejected task285 v1 の source bytes/hash/object shape を「本番 blocker identity」として pin
  しない。将来の accepted task285 ABI は別版で明示的に bind する。
- v1 の endpoint/Artin/full-C1 engine と独立 replay、21 mutation、5 cases+2 typed guardsを保持する。
- schema/path/sentinel はすべて v2 に更新し、driver は ASCII only、stale output rejection、
  producer/checker terminal equalityを保つ。
- SELFTEST や UNKNOWN_INPUT を A7 actual zero と宣言しない。A8/A9/fake/Ihara は false。

## 3. reply

全5ファイルの bytes/SHA、v1からの差分、SELFTEST dependency closure が全て tracked または
今回の五ファイル内であること、未実行であることを報告する。
