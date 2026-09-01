# Sol audit 481 — A4 row-26 resumed-resource checker v30

## 判定

**STOP / v30 + driver-v2 の checker-only dispatch は NO-GO。**

v30 は v428 の式 (2.2) を実装しているが、pin 済み永久 asset の実 base
checkpoint はその式を満たさない。exact payload を production
`validate_terminal_payload` に渡す bounded gate は

```text
EXACT_ARTIFACT_GATE_REJECT Reject checker:producer_completed_base_binding
```

となった。したがって実 dispatch では checker が `UNKNOWN_INPUT` を封印して
返し、driver の exact `UNKNOWN_RESOURCE` 行 gate で fail-close する。row 26 の
昇格はできない。`verified=false`。

## F1 — blocker: v428 (2.2) は immutable artifact の三座標で偽

永久 asset

```text
56410  5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3
```

を `%TEMP%` の fresh directory に取得し、六 JSON の bytes/SHA、canonical
bytes、self seal を照合した。`B` を pin 済み row-24 base checkpoint、`T` を
producer terminal resource とし、`S` を登録 semantic domain とする。実際の
厳密な関係は、

```text
D = {terminal_canonicalization, terminal_serialized_bytes,
     terminal_final_write}

k in S \ D:
  T.completed[k] = B.semantic[k] = B.completed[k]

k in D:
  B.semantic[k] = B.completed[k] = 0
  T.completed[k] = T.semantic[k]

all k in S:
  T.completed[k] <= T.semantic[k]
```

である。三座標の exact values は次の通り。

| key | `B.semantic` | `B.completed` | `T.completed` | `T.semantic` |
|---|---:|---:|---:|---:|
| `terminal_canonicalization` | 0 | 0 | 7 | 7 |
| `terminal_serialized_bytes` | 0 | 0 | 9300 | 9300 |
| `terminal_final_write` | 0 | 0 | 1 | 1 |

これは偶然の drift ではない。pin 済み producer v22 の generated
`Meter.terminal_bump` は terminal transport を `semantic_counters` と
`completed_counters` の双方へ記帳する。従って v428 (2.2) の全座標 equality

```text
T.completed = B.semantic = B.completed
```

は artifact と producer accounting の双方に反する。

v30 の `_v30_validate_completed_snapshot` は
`base_semantic == base_completed and completed == base_semantic` を全 domain に
要求する。一方 `_row26_fixture` は base 側の上記三値を `7,9300,1` に置いた
synthetic base を使う。六つの **terminal resource maps** は artifact と exact
だったが、二つの base maps は上表の三座標で不一致だった。これが self-test
PASS と exact artifact REJECT の理由である。Task478 reply の「authenticated
base-checkpoint maps へ binding」と PASS 結論は成立しない。

## F2 — v423 envelope と残る counter gate

この blocker 以外の narrow counter logic は PASS。

- terminal over-cap coordinate は `wall_seconds` 一座標だけで、値は
  `14402.408729186 > 14400`。超過 occurrence は canonical map と genuine host
  view の二箇所で同値であり、他の terminal typed coordinate に超過はない。
- v30 は trigger/cap/measured/state、canonical/typed-view equality、非負 numeric
  typing、他座標の cap を production function 内で要求する。
- exact artifact では `completed <= terminal semantic` が全 semantic key で成立し、
  v30 も exact domain、非負、cap、componentwise inequality を要求する。
- base/delta/HEAD/row/query/event/epoch/queue/word-DAG replay は frozen v28 のまま。
  HEAD は `last_row=26,next_row=27,segment_count=2`、base は `next_row=25` であり、
  terminal-minus-base counter 差から durable cursor を推論していない。

ただし self-test の `second_over_cap` mutation は semantic map だけを変え、先に
canonical/semantic equality でも落ちる。production predicate 自体は canonical
と semantic を同時に超過させた isolated mutation も拒否するが、v31 fixture
ではこの isolated gate に強化すべきである。

## F3 — exact members、driver、live pins

永久 zip は SHA 検査後にだけ fresh extraction root へ展開される。archive は
16 flat entries を持つが、次の replay 六 member は各一回だけ存在し、driver は
この六つだけを再 pin 後 `$root/ci/out/<basename>` へ copy する。

| member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_word_independent_successor_kernel_v40.json` | 9300 | `7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5` |
| `d972_r07_word_independent_successor_kernel_v40.producer.base.checkpoint.json` | 25581 | `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445` |
| `d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json` | 700 | `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114` |
| `d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000001.json` | 3551 | `d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19` |
| `d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000002.json` | 3625 | `acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523` |
| `d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json` | 8991 | `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2` |

Generic archive `driver.g` / `run.log` は fresh extraction root 内に留まり、repo の
generic `ci/out/driver.g` / `ci/out/run.log` を stale-check、copy、overwrite しない。

Driver static gates も次の範囲で PASS。

- run/job/head/artifact/release/asset pins は Task469 と一致。
- explicit arguments は各一回、checker command は一つ、producer command はゼロ。
- `15000 - 14400 = 600` 秒の timeout margin。
- `8500000*1024 - 8000000000 = 704000000` bytes の hard-VM margin。
- `set -euo pipefail`、timeout exit propagation、fresh success marker、全 terminal
  prefix 行数 `=1`、exact `UNKNOWN_RESOURCE` 行数 `=1`、Traceback/STOP absence。
- output は fresh/nonempty。pin 済み checker の canonical `write_sealed` と合わせ、
  status/terminal/self-digest field を検査し、verdict bytes/SHA/self-digest を receipt
  に結ぶ。
- terminal producer branch は positive kernel replay 前に return するため、不要な
  slow semantic work はない。

最終 live pins は Task478 reply と同期している。

```text
checker-v30  19871  660d71f34931d138a7d4fb9a4e3e2e17f7b10d3a73a32d59b90b85c9f2419529
driver-v2    14006  46fae084e45393d59e97f349b8ef839d49325843cabc24160cc49f8f5da7e27c
reply-478     3579  1a7a7ad5daa1e8661f7c917d0637c2ccaa3ec3e2f221b539885f80293f9e15cf
generated-v30 286599 29a600c27c4f4f3872575c1edc56aaaca6bd10bcc62eb1236b22dc21e2d120ed
```

## 最小の positive-safe 修理

別 artifact を推測で生成せず現 immutable asset を救う最小修理は、v428 を上の
exact transport relation で narrow に訂正し、v31 checker successor を作ること。

1. `D` を上記三 key に exact 固定し、
   `{k in S | T.completed[k] != B.semantic[k]} = D` を要求する。
2. `B.semantic == B.completed`、両 base domain/bounds、全 key の
   `T.completed <= T.semantic` は維持する。
3. `k notin D` では completed を base の両 map に exact binding する。
   `k in D` では completed を terminal semantic/canonical と、既存 serialization
   field (`terminal_canonicalization`, `serialized_work_bytes`, `final_write`) に exact
   binding する。これらは output transport bookkeeping だけであり、row work や
   cursor の durable claim に用いない。
4. Positive fixture の base 三値を実 artifact の `0,0,0` に直し、六 terminal maps
   と二 base maps の全てを pin 済み asset と exact 比較した上で production
   validator を通す。
5. difference-domain の missing/extra、各 transport equality、non-`D` base drift、
   completed-above-terminal、および canonical+genuine typed view を同時に変える
   isolated second-over-cap mutation を追加する。
6. driver は release/member/path/timeout/RSS/terminal gatesを保ち、checker/output/
   receipt を v31 の fresh path と pin にだけ更新する。

v428 (2.2) を維持したい場合の唯一安全な別案は、producer の terminal bookkeeping
を修正して新 artifact を生成・再 pin することであり、現 asset を v30 へ通すこと
ではない。

## 実行した bounded checks

```text
python -B crosscheck/check_d972_r07_word_independent_successor_kernel_v30.py --self-test
R07_A4_RESUMED_RESOURCE_V30_SELFTEST_PASS rows=26 counter_predicates=2 mutations=12 old_predicate=REJECT

Python AST/load + frozen restoration:
wrapper 19871 / 660d71f3...
generated 286599 / 29a600c2...

GAP 4.16.0 ReadAsFunction(driver-v2): PASS
exact zip/member/canonical-self-seal parse in %TEMP%: PASS
exact payload production validator: REJECT producer_completed_base_binding
synthetic base with 7/9300/1: PASS
```

production semantic replay、GHA、workflow edit、git は実行していない。

`TASK481_AUDIT_STOP_V428_EQ22_ARTIFACT_MISMATCH_NO_DISPATCH`
