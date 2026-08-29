# Luna reply 366 - A4 checker v14 / driver v20

Static implementation is complete.  Python, GAP, GHA, SELFTEST, and the
production calculation were not run.

## Artifacts

| file | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v14.py` | 8074 | `7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v20.g` | 5548 | `cbb5c09bb661d15d20ba9f3df7683ea38b58c5fc5e884b118972f091833a9262` |

## Exact repairs

Checker v14 is the frozen-v6, independently reconstructed v13 checker with
the owner-hoist replacement corrected.  Its replacement now emits both

```
validate_bridge_owner_once(authority)
occurrences = []
```

at the original site.  Thus the invariant owner validation remains cached,
while the per-row occurrence accumulator is initialized before its first use.
All other v13 cap, hot-path, progress, checkpoint, and producer-v12 pin
changes are retained.

Driver v20 is a one-layer wrapper over the frozen v6 driver (13775 bytes,
SHA-256 `a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0`).
It uniquely replaces the producer with v12, the checker with v14, their exact
byte/SHA pins, the driver identity, and all owned output paths with isolated
`v20diag` paths.  Immediately before reading the generated body it sets
`D345Mode:="PRODUCTION"`; the outer gate is `D366Mode="PRODUCTION"`.

The diagnostic no-sentinel branch and final 65535-byte producer/checker log
tail capture are retained.  No PASS, cross-check, or verification claim is
made by this static reply.
