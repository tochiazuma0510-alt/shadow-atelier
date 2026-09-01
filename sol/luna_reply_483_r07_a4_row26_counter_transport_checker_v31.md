# Luna reply 483 — A4 row-26 counter-transport checker v31

## Result

`TASK483_R07_A4_ROW26_COUNTER_TRANSPORT_V31_PASS`

Created exactly the commissioned outputs:

1. `crosscheck/check_d972_r07_word_independent_successor_kernel_v31.py`
2. `search/d972_r07_word_independent_successor_kernel_row26_checker_only_gha_driver_v3.g`
3. this reply file

The v31 checker pins the frozen v30 owner at

```text
19871 660d71f34931d138a7d4fb9a4e3e2e17f7b10d3a73a32d59b90b85c9f2419529
generated v30 286599 29a600c27c4f4f3872575c1edc56aaaca6bd10bcc62eb1236b22dc21e2d120ed
```

It retains v423's unique typed wall-time excess and all frozen v28 replay,
authority, producer, output-seal, and delta/HEAD gates.  The only generated
predicate replacement is v429's exact transport relation with

```text
D = {terminal_canonicalization, terminal_serialized_bytes, terminal_final_write}
```

It requires base semantic/completed equality on the registered semantic
domain, exact difference domain `D`, base values `(0,0,0)` on `D`, terminal
completed/semantic/canonical/serialization equality `(7,9300,1)` on `D`,
base binding outside `D`, all bounds, and `T.completed <= T.semantic`.  The
authenticated base cursor remains `next_row=25`; transport differences are
never used as durable row progress.

The positive fixture parses a 4520-byte canonical JSON projection of the
pinned producer/base maps (projection SHA
`8651e982f7efc6a72d2b766cf452c3eeb98e315c76262e7e62b0344c2378bba5`) and
compares all nine maps against the immutable asset.  It does not normalize the
base map.  Regression mutations reject base-map drift, non-`D` drift, missing
and extra difference-domain members, nonzero base transport values, transport
serialization drift, completed-above-terminal, simultaneous canonical+genuine
typed-view second over-cap, and transport-as-row-cursor advancement.

The v3 checker-only driver uses fresh v31-owned paths, retains run/job/head /
artifact/release and all six member pins, copies members to
`$root/ci/out/<exact basename>`, and invokes one checker with all explicit
producer/output/checkpoint/resume/authority/cap arguments and no producer
process.  It requires one total terminal-prefix line, one exact
`UNKNOWN_RESOURCE` line, no `Traceback`/`STOP`, and a nonempty self-sealed
verdict bound by bytes/SHA/self-digest in the receipt.  Margins remain
fail-closed:

```text
internal --seconds 14400          external timeout 15000 s
internal --rss-bytes 8000000000  hard VM 8500000 KiB
```

## Bounded checks

```text
python -B crosscheck/check_d972_r07_word_independent_successor_kernel_v31.py --self-test
R07_A4_COUNTER_TRANSPORT_V31_SELFTEST_PASS rows=26 difference_domain=3 mutations=10 second_overcap=CANONICAL_AND_TYPED_VIEW

ROW26_PINNED_MAP_PARSE_COMPARE_PASS maps=9
GAP_DRIVER_PARSE_PASS
```

No v30/v2 file was edited.  No production replay, GHA dispatch, workflow
edit, git operation, producer rerun, or bytecode-cache creation was performed.

```text
checker-v31 19483 7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e
driver-v3   13710 7fa72fb5a56dbbb2d6b50253883d5d5992c0f8ebedaae59c9cba71e81645add2
```

Row-26 promotion remains unclaimed pending the external checker-only replay.

TASK483_R07_A4_ROW26_COUNTER_TRANSPORT_V31_PASS
