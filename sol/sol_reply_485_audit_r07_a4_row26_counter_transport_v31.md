# Sol audit 485 — A4 row-26 counter-transport checker v31

## 判定

**GO — v31 / driver-v3 の checker-only dispatch 可。**  Task483 の指定範囲に
致命点はない。これは row 26 の昇格判定ではなく、外部 checker-only replay の
投入許可だけである。`verified=false`。

## F1 — v429 relation と実 payload gate

v31 の生成 source は pin 済み v30 source へ cardinality-one の二置換だけを行う。
新 predicate は semantic domain `S` と

```text
D = {terminal_canonicalization, terminal_serialized_bytes,
     terminal_final_write}
```

を exact に固定し、`B.semantic=B.completed`、difference domain `=D`、
`S\D` で両 base map への binding、`D` で terminal canonical/semantic と
serialization transport field への binding、全 domain/type/bound、および
`T.completed<=T.semantic` を要求する。base cursor は直接 `next_row=25` に固定され、
transport 差を row cursor へ加算する経路はない。

永久 asset を `%TEMP%` の fresh root に取得し、zip と六 member を bytes/SHA 後に
展開した。埋込 projection だけでなく、実 producer JSON と実 row-24 base JSON の
九 map を projection と全比較し、その**実二 JSON**を生成 v31 の production
`validate_terminal_payload` へ渡して PASS を確認した。実値は正確に

```text
base D       = (0, 0, 0)
terminal D   = (7, 9300, 1)
difference   = D
base next_row = 25
```

である。従って v30 の synthetic-base 問題は解消している。なお Task483 自己試験の
`ROW26_PINNED_MAP_PARSE_COMPARE_PASS` 自体は埋込 projection 水準だが、本監査の
exact immutable-payload gate が別途その来歴と production validator acceptance を
閉じたため STOP 理由ではない。

missing/extra difference member、base/non-`D` drift、transport binding drift、
`completed>semantic`、transport cursor advance は全て reject される。同時
canonical+semantic genuine-view の第二 over-cap も reject。唯一の許容 over-cap は
従来どおり `wall_seconds=14402.408729186>14400` であり、v423 と frozen v28 の
base/delta/HEAD/authority/word-DAG/replay gate は生成 source pin と狭い二置換により
保持されている。

## F2 — immutable pins と driver

```text
run       33506331399
job       99851144256
head      5dbc895552efdaffb13bb7b10e595430026f4c3c
artifact  9809473723 / gap-run-out
artifact digest 4a82302e49ddfdd7790df0e0082d0762de3238c0b4e0de23259d97bd1a2af445
release   https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9809473723_gap-run-out.a4-row26.zip
zip       56410 / 5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3
```

六 member は次の exact pins と一致した。

| member | bytes | SHA-256 |
|---|---:|---|
| `d972_r07_word_independent_successor_kernel_v40.json` | 9300 | `7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5` |
| `d972_r07_word_independent_successor_kernel_v40.producer.base.checkpoint.json` | 25581 | `595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445` |
| `d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json` | 700 | `910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114` |
| `d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000001.json` | 3551 | `d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19` |
| `d972_r07_word_independent_successor_kernel_v40.producer.head.checkpoint.json.delta.00000002.json` | 3625 | `acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523` |
| `d972_r07_word_independent_successor_kernel_v40.checker.checkpoint.json` | 8991 | `b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2` |

driver は fresh v31-owned paths のみを使用し、六 member を exact basename で copy、
checker process `=1`、producer process `=0`。余裕は
`15000-14400=600 s` と `8500000*1024-8000000000=704000000 bytes`。
terminal は一行だけの exact
`R07_WORD_INDEPENDENT_SUCCESSOR_KERNEL_V6_CHECKER_TERMINAL UNKNOWN_RESOURCE`、
verdict は status/terminal/self-digest を要求し、bytes/SHA/self-digest を receipt に
結ぶ。terminal branch は slow positive replay 前に return する frozen 順序を保持する。

最終 file pins:

```text
checker-v31   19483  7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e
generated-v31 288650 89d8626f8c14972ccad21efa441de07e5e9cf1baf18f98a68751f8bc16e46744
driver-v3     13710  7fa72fb5a56dbbb2d6b50253883d5d5992c0f8ebedaae59c9cba71e81645add2
reply-483      3257  2d6eaa05be973ce0d05e796799f33efe71ac8a3c46c7e408e9d85016156a3545
```

## Bounded evidence

```text
python -B ...v31.py --self-test
R07_A4_COUNTER_TRANSPORT_V31_SELFTEST_PASS rows=26 difference_domain=3 mutations=10 second_overcap=CANONICAL_AND_TYPED_VIEW

exact immutable nine-map compare: PASS
exact immutable production validate_terminal_payload: PASS
GAP 4.16.0 ReadAsFunction(driver-v3): PASS (exit 0)
```

production replay、GHA、producer、workflow、git は実行していない。

`TASK485_AUDIT_GO_R07_A4_ROW26_COUNTER_TRANSPORT_V31_CHECKER_ONLY`
