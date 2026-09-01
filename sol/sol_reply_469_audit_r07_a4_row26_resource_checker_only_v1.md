# Sol audit 469 — A4 row-26 resource checker-only v1

## 判定

**STOP / GHA checker-only 投入は NO-GO。**  `verified=false` であり、row 26
を `CROSS-CHECKED CLOSED CURSOR` へ昇格してはならない。

停止理由は独立に二つある。

1. 現 driver は v29 を無引数で起動するため、generated v28/v29 main は
   `UNKNOWN_RESOURCE` ではなく `UNKNOWN_INPUT` を返す。また replay inputs
   の配置先も checker の path owner と一致しない。
2. 上の driver defect を直して実 artifact を v29 の production payload
   validator に渡しても、artifact 自身が保存された v28 equality gate
   `completed_counters == semantic_counters` を満たさない。従って v423 の
   「他の v28 gate は成立する」という前提が、この row-26 artifact では偽である。

以下は bounded static/load audit である。production、GHA、GAP、git、semantic
positive replay は実行していない。永久 asset は `%TEMP%` の fresh directory
へだけ取得し、repository には本返信以外を書いていない。

## F1 — blocker: checker invocation に必須 replay arguments がない

Driver の唯一の Python 起動は
`search/d972_r07_word_independent_successor_kernel_row26_checker_only_gha_driver_v1.g:122`
の

```text
python3 -u -B "$root/crosscheck/check_d972_r07_word_independent_successor_kernel_v29.py"
```

であり、引数は一つもない。

v29 が exact-pin して復元する generated v28 main の contract は次の通り
(restored source lines 4141--4170, 4181--4184)。

| argument | default | 無指定時の意味 |
|---|---|---|
| `--producer` | `None` | non-selftest では `CHECKER_PRODUCER_REQUIRED` |
| `--output` | `None` | sealed checker verdict を書かない |
| `--checkpoint` | `None` | checker checkpoint owner を持たない |
| `--resume` | `None` | checker checkpoint を解決しない |
| `--input` | `ci/in/d972_r07_seven_context_roof_presentation_v1.json` | repo-rooted default |
| five `--task198-*` | matching `ci/in/<AUTH file>` | repo-rooted defaults |
| `--seconds`, `--rss-bytes` | `14400`, `8000000000` | frozen caps と一致 |

特に `args.producer is None` は `Reject("CHECKER_PRODUCER_REQUIRED")` となり、
main の typed exception handler は exit 0 で

```text
R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL UNKNOWN_INPUT
```

を出す。fresh `%TEMP%` cwd から driver と同じ無引数 command を実行した
bounded load test でも、上の一行と `exit=0` を再現した。従って driver
line 123 の exact `UNKNOWN_RESOURCE` grep は失敗し、receipt 作成前に shell
が止まる。Luna reply の「expected runtime terminal remains
`UNKNOWN_RESOURCE`」は現 command については成立しない。

また `--output` がないため、仮に log token だけを合わせても full checker
replay の sealed verdict が存在せず、task469 lines 72--74 の昇格条件を満たさない。

## F2 — blocker: `$work/ci/out` は generated checker の owner ではない

Driver は六つの authenticated members を line 115 で
`$work/ci/out/<name>` へ copy し、line 120 で `$work` に `cd` する。一方、
v29 は generated code の `__file__` に repository 内の v29 absolute path を
与えるため、generated line 28 の

```text
ROOT = Path(__file__).resolve().parents[1]
```

は常に repository root である。cwd ではない。さらに generated
`exact_path` (lines 713--729)、`read_output` (3641--3657)、`output_path`
(732--745)、`checkpoint_input` (748--754) は producer/output/checkpoint を
すべて `ROOT/ci/out/<basename>` に限定する。

従って、単に line 122 に
`--producer ci/out/d972_r07_word_independent_successor_kernel_v40.json`
を足しても、checker が読むのは
`$root/ci/out/...v40.json` である。Driver lines 80--85 はその root target が
存在しないことを事前要求し、実際の copy は `$work/ci/out` に行うため、必ず
missing input になる。`$work` の absolute path は lexical absolute-path gate
で拒否され、nested relative path も exact `ci/out` owner gate で拒否される。

Task198 authority の無指定 defaults 自体は `$root/ci/in` を正しく読むので、
authority files を `$work` に copy する必要はない。ただし現 invocation は
producer-required gate で authority construction より前に止まる。六番目の
authenticated checker checkpoint も、現状では `--checkpoint/--resume` がなく
dead input である。

## F3 — blocker: 実 artifact は残存 equality gate を満たさない

委嘱で pin された permanent asset を独立に取得した結果は次である。

```text
asset bytes  = 56410
asset sha256 = 5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3
```

指定された六 member の bytes/SHA-256 は全て commission と一致した。独立な
canonical-JSON replay では producer/base/HEAD/delta1/delta2/checker-checkpoint
の各 self seal が一致し、delta chain も

```text
segments = 2, last_row = 26, next_row = 27
chain = 240714843f67b24fdee9593601130c5d36ef9996909a08af9ec909888cb8cfdb
```

まで一致した。これは artifact identity の bounded 照合であって、row 26 の
cross-check 昇格ではない。

この exact producer result に対して、v29 helper
`_v29_typed_resource_envelope` は期待どおり `True` であった。canonical map の
over-cap coordinate は唯一

```text
wall_seconds = 14402.408729186 > 14400
```

であり、canonical/host occurrence は等しい。他の cap、domain、type、host、
peak、restore、semantic-to-canonical、object-cap 条件も全て成立する。

しかし、同じ exact payload を generated v29 の production function
`validate_terminal_payload` に渡すと

```text
Reject: checker:producer_terminal_resource_envelope
```

となった。大 conjunction を独立に分解すると、偽なのは唯一

```text
terminal_completed == terminal_semantic
```

である。相違は 14 coordinates:

```text
active_keys, affine_sparse_ops, boundary_rank_rises, bridge_occurrences,
bridge_rows, checkpoint_total_bytes, correlation_pairs, dual_support,
literal_comparisons, membership_queries, membership_reductions,
row_assemblies, row_piece_products, typed_context_products
```

代表値は次の通りである。

| coordinate | completed | semantic |
|---|---:|---:|
| `active_keys` | 0 | 1,094,076 |
| `boundary_rank_rises` | 0 | 138,784 |
| `bridge_rows` | 24 | 26 |
| `checkpoint_total_bytes` | 122,683 | 127,008 |
| `correlation_pairs` | 0 | 46,789,964 |
| `dual_support` | 0 | 11,706,998 |
| `membership_queries` | 24 | 26 |

`completed_counters` は概ね canonical base (closed row-24 state) と一致し、
terminal serialization の三座標だけがその後進んでいる。一方
`semantic_counters` は row 26 terminal の値である。これは v423 lines 37--42
が保存するとした v28 equality/duplication premise と両立しない。v29 の patch
は cap loop 一箇所だけなので、この mismatch は当然残る。

従って、F1/F2 を直した Linux GHA invocation でも v29 は
`UNKNOWN_INPUT` (`checker:producer_terminal_resource_envelope`) を返す。v423 の
one-coordinate cap repair は必要だが、この immutable artifact に対して十分ではない。

## F4 — terminal cardinality gate も specification 未達

Driver line 123 は expected exact line の出現数が 1 であることだけを検査し、
全ての `^R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL ` 行の総数が
1 であることを検査しない。従って expected line 一行に別 status terminal
一行が併存しても通る。Task469 line 69 の「exact terminal-line cardinality」
には、original v41 shell と同様の総 terminal-line count gate が別に必要である。

`set -euo pipefail` と receipt absence gate により nonzero checker/shell exit は
fail-closed になる点、唯一の Python command が checker 一つで producer command
がない点は静的に PASS である。

Run/job/head、artifact id/name、release URL、asset bytes/SHA、checker bytes/SHA、
六 replay-member bytes/SHA の driver constants は commission と全て一致した。
Owned-path gate は generic workflow の `ci/out/driver.g` と `ci/out/run.log` を
拒否も上書きもしない。

## v29 checker 自体について成立した範囲

- v29 owner bytes/SHA、driver bytes/SHA、generated bytes/SHA は Luna reply と一致:

  ```text
  v29 wrapper  8298 / 8ce2c39c45ebd8403e4fcd51a098dddec31b2136a273975e9846cf4dd2151291
  driver       8311 / ba8632aa88efc727a34402567812a5c9446b0725e4cd55aa6db1c908cd90cae9
  generated  281745 / 549783a95bdb3e264c212943e50058f5d5489ddfbe8fe9d52d3ee46f3dfa394e
  ```

- Generated v28 -> v29 diff は lines 4057--4061 の universal cap loop を helper
  call に置換する一箇所だけであり、owner/result hash と cardinality gate は
  fail-closed である。
- `completed_counters` を specification の equality premise に合わせた control
  payload では production validator が PASS し、witness `v<=limit`、wrong cap、
  canonical below witness、typed occurrence unequal but still above witness、第二の
  equal-typed over-cap、wrong state、semantic-type second over-cap、changed checkpoint
  seal、`UNKNOWN_INPUT` weakening の九 mutation は全て REJECT した。
- 従って「認証 trigger coordinate の同じ typed occurrence だけ cap 超過可、
  他座標は cap 以下」という helper と surrounding frozen gates の合成は、前提を
  満たす payload には正しい。実 artifact がその前提を満たさないことが blocker
  である。
- Generated checker は producer module/helper を import せず、producer v22 は
  bytes/SHA pin と delta replay identity として読むだけである。reverse checker
  arithmetic を保持しており、helper 非共有の独立性に新しい違反は見つからない。
- Positive path、`UNKNOWN_INPUT` path、checkpoint/delta/authority/producer-code gate
  は generated diff 外である。terminal producer は `positive_result` より前に
  short-circuit するため、正しい invocation は不要な kernel computation を行わない。
- Bundled `--self-test` は表示どおり PASS する。ただし
  `closed_checkpoint_seal_changed` は production checkpoint validator ではなく
  test-only boolean helper を叩き、bundled `typed_view_differs` は equality 以前に
  below-witness でも落ちる弱い fixture である。本監査では上記の stronger
  production-function mutations で補った。次版では fixture も強化すべきである。

## 最小修理

1. **現 v1 driver を dispatch しない。** versioned successor を作る。
2. 先に `completed_counters` の意味を裁定する。
   - v28 の `completed == semantic` が正本なら、producer accounting を直して
     新しい immutable artifact を生成する。pin 済み v40 result を改変してはならない。
   - `completed_counters` が意図的な last-closed view なら、その domain、terminal
     semantic map との関係、base/delta/closed cursor への authentication を新しい
     数学ノートで定義し、その関係だけを検査する versioned checker successor を
     作る。根拠なく equality gate を削除してはならない。
   いずれの場合も、exact row-26 payload を regression fixture にして今回の第二矛盾を
   捕捉する。
3. Versioned driver successor は fresh extraction root を保つ一方、六つの
   authenticated replay inputs を **`$root/ci/out/<required name>`** に copy し、
   checker を `$root` owner に対して実行する。少なくとも original v41 contract と
   同じ explicit arguments を渡す:

   ```text
   --input ci/in/d972_r07_seven_context_roof_presentation_v1.json
   --producer ci/out/d972_r07_word_independent_successor_kernel_v40.json
   --output ci/out/<new-task469-verdict>.json
   --checkpoint ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json
   --resume ci/out/d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json
   --seconds 14400 --rss-bytes 8000000000
   --task198-receipt ... --task198-manifest ... --task198-producer ...
   --task198-checker ... --task198-verdict ...
   ```

   Output は nonempty canonical sealed verdict として receipt に bytes/SHA を結び、
   stale owned-output gate にも加える。
4. Expected exact line count に加え、全 checker terminal prefix の総数 `=1`、
   STOP/Traceback absence、checker exit、sealed output status/self seal を検査する。
   Static count は checker process 1、producer process 0 のまま保つ。
5. 上の checker/spec と driver の双方を修理した後にだけ、immutable artifact に
   対する checker-only GHA を投入する。その run が PASS するまでは row 26 は
   `PRODUCER-SEALED CANDIDATE` のままである。

`TASK469_AUDIT_STOP_DRIVER_AND_COMPLETED_COUNTER_GATE`
