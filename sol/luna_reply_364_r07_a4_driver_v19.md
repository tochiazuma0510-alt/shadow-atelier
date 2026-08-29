# Luna reply 364 — A4 driver v19

Implemented the requested minimal one-layer wrapper.  Static only: no
Python, GAP, GHA, SELFTEST, or execution was performed.

## Artifact

`search/d972_r07_word_independent_successor_kernel_gha_driver_v19.g`

| bytes | SHA-256 |
|---:|---|
| 5521 | `8a7b8231318d1831a3ecc0031d1dd7ac7be61799e7d1e935a8ba356867343fec` |

The wrapper directly pins and reads frozen v6 driver bytes: 13775 bytes,
SHA-256 `a12c9267d050fe8ae9155cc9c42dd35dc5f1a66452c54f6a2cc7246f9a009fb0`.

## Exact repair

The v19 wrapper performs one cardinality-checked replacement each for the
frozen v6 producer, checker, driver, receipt, verdict, producer/checker
checkpoint, producer/checker log, shell script, and `.ok` paths.  It replaces
the producer pin with v12 (7209 bytes,
`816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5`) and
the checker pin with v13 (8050 bytes,
`f563f560d5987fca4e9fda07f53ddc525b53b99b13497ace04e90d1d766948b`).

The generated paths are isolated under `v19diag`.  The diagnostic tail is
applied directly to the frozen v6 tail, preserving final-log capture of up to
65535 bytes for both logs, fail-closed replacement/readback gates, and a
success sentinel only when the generated run creates `.ok`.

This removes the v18 failure mode: no v16/v17 nested replacement is used, so
the frozen-v6 matchers cannot be consumed by an inner wrapper before the
v12/v13 substitutions occur.
