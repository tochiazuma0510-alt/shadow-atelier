# Sol reply 365 — A4 v12/v13 runtime static audit

## 判定

**REJECT**。本番 A4 を止めない静的監査だけを行った。Python/GAP/GHA、SELFTEST、
mutation、実装変更は実行していない。

## 最初の具体的問題

`crosscheck/check_d972_r07_word_independent_successor_kernel_v13.py:31` の置換は、
frozen v6 の owner 検査と一緒に `occurrences = []`
（frozen checker v6:1650）まで削除するが、置換後にこれを戻していない。そのため
`checker_bridge_trace` は最初の本番 row で `occurrences.append(...)`
（frozen checker v6:1676）に到達すると `NameError` になる。

最小修理は置換後を
`validate_bridge_owner_once(authority)\n    occurrences = []\n` とすることである。

## 第二の起動阻害

`search/d972_r07_word_independent_successor_kernel_gha_driver_v19.g:5-7` は
`D364Mode="PRODUCTION"` だけを入口契約にするが、生成して `Read` する frozen-v6
driver は冒頭で未置換の `D345Mode` を要求する（frozen driver v6:4-5）。v19 自身は
`D345Mode` を設定しない。従って通常の `D364Mode` だけの起動では v12/v13 を呼ぶ前に
`task345 MODE required` で停止する。内層 `Read` 前に
`D345Mode:="PRODUCTION";;` を明示するのが最小修理である。

## 意味保存の監査

上の即死点を除けば、指定された三修理は意味を変えない。

- 最初の `combined.reduce(target)` の remainder を dual pullback に渡す間に basis の
  変更はないため、重複 reduce の省略は同じ remainder を使う。
- in-place F3 AXPY は frozen `add_row` / `add_sparse` の
  `(old-coefficient*row) mod 3` と同じで、零成分も同じく削除する。reduce は入力を最初に
  copy するため basis row との alias もない。
- eleven-owner の layout/coordinate は authority の不変データであり、成功後だけ cache
  する owner-once 化は意味保存である。

## 本番経路と残留性能

- v12/v13 に SELFTEST、mutation、retry、fanout の先行実行は追加されていない。
- row checkpoint 集合への `32` の追加は本番 `consume_row` 内にあり、修理後に row 32
  が完了すれば到達する。ただし checkpoint 全体の再直列化はその各指定 row で残る。
- `A4_PROGRESS` は authority 完了後と row/queue の入口では到達するが、重い authority
  構築中および一つの `correlate` の内部では heartbeat を出さない。また driver は Python
  stdout をファイルへ redirect するので GHA console の live progress にはならない。
- 最大の残留ボトルネックは、各 nonmember query ごとの full-D `correlate` 全走査である。
  さらに各 dual について全 live basis row の dot-zero 再走査、correlation accumulator の
  全 sort、および各 pair の translation 後の再積による等式確認が残る。cap を上げても、
  これらの計算量は減っていない。

従って、上記2件の最小修理なしには本番成果物へ昇格不可である。修理後も主な時間リスクは
full-D correlation 自体であり、今回の静的監査は完走時間を保証しない。
