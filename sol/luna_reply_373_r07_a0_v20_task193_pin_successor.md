# Luna 373 — A0 v20 → adapter v4 → task193 v3 exact-pin successor

## 結論

監査372の stale A0-v18 pin だけを解消する versioned successor を完成した。
adapter v3 / task193 v2 の数学本体はそれぞれ byte-pin したまま実行し、live ABI の
schema、terminal、source path/bytes/SHA-256 だけを版上げした。retry、SELFTEST、
重い実行は追加していない。

| role | path | bytes | SHA-256 |
|---|---|---:|---|
| adapter producer v4 | `search/d972_r07_history_free_task193_compat_adapter_v4.py` | 2426 | `0174b1508f50708352e8607edfb0a210508680e58a295763b2d287fda32889b9` |
| adapter checker v4 | `crosscheck/check_d972_r07_history_free_task193_compat_adapter_v4.py` | 3105 | `4269368c006e19fa0cc71da78d12927f8fbd4c85087f0e5b5ca11688a8f58d06` |
| adapter driver v4 | `search/d972_r07_history_free_task193_compat_adapter_gha_driver_v4.g` | 5146 | `5d4473d09d11cac7227f777f1baaa315a840e95dbcbfb76eb080bbda43a72f62` |
| task193 producer v3 | `search/d972_r07_second_frattini_affine_prefix_compiler_v3.py` | 2826 | `1ac65ca533e11ac39def79c84de0bbdcb018d463ac10bca6158db254a61da741` |
| task193 checker v3 | `crosscheck/check_d972_r07_second_frattini_affine_prefix_compiler_v3.py` | 2792 | `5b3c5b3e607077e0bebcf0153c592465983ba210b768c93ea62aeb2201c905c6` |
| task193 driver v3 | `search/d972_r07_second_frattini_affine_prefix_compiler_gha_driver_v3.g` | 5798 | `c11074bd1e634aa38d4d164699542e17087e659115c31b8f5b8cc322dc5dfd84` |

adapter v4 は A0 v20 producer `10739/cf775975...7150ed7` と checker
`5327/7c0a1c8...d7c077` の一組だけを受理する。adapter driver はさらに A0 v20
driver `6907/f9cfffc...6918d4` を exact-pin する。task193 v3 は上表の adapter v4
producer/checker の一組だけを受理し、task193 driver は adapter v4 driver も
exact-pin する。v18/v20 または v3/v4 の OR gate は導入していない。

positive path は A0 `COMMON_WORD` receipt と、それを v20 producer pin の下で
独立 replay 済みとする PASS verdict の完全一致時だけ adapter `ACCEPTED` になる。
A0 UNKNOWN または不一致は adapter の `UNKNOWN_INPUT:*`、task193 側では既存の
typed `UNKNOWN_INPUT` / `UNKNOWN_RESOURCE` のままで、accepted claim を出さない。

静的 definition load、live pin/schema/terminal assertion、および producer と
checker の typed-UNKNOWN in-memory replay はすべて PASS。production/SELFTEST は
実行していない。
