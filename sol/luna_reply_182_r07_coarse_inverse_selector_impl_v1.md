# Luna reply 182 — r07 coarse-inverse selector implementation v1

Date: 2026-08-27
Role: bounded implementation and static audit only.

## Static verdict

Implemented the selector specified by
`sol/proof_r07_actual_singleton_coarse_inverse_selector_v142.md`.
`FibreOracle.canonical` now lazily builds one open-addressed inverse per used
coordinate, stores only `qid+1` in `array("I")`, compares exact coarse bytes
on every occupied slot, hard-stops on duplicate exact coarse keys, performs
the full packed section check, replays all ten coordinates and the literal
word, and selects least `(qid,gid)`. Success and empty-fibre caching and the
existing positive schedule are unchanged.

The noncommutative SELFTEST now independently exercises forced hash
collisions, exact-key collision resolution, duplicate rejection, least-pair
selection, and full packed mismatch rejection. The original fifteen semantic
mutation rejections remain required. The helper-nonshared checker reconstructs
the selected Q0 section from the public source-word provenance and checks the
complete packed target without importing the producer index helper.

Whole-buffer digest copies were replaced with streamed chunk hashing for Q0
and coordinate stores. Global-roster exhaustion now raises the registered
resource path and produces positive-only `UNKNOWN_RESOURCE` through the
existing terminal handler.

## Memory accounting

`2^22 * 4 = 16,777,216` payload bytes per coordinate; ten tables are exactly
`167,772,160` payload bytes. Slots contain unsigned `qid+1` only and tables
are not serialized. The index metadata records state count `1,469,664`, table
length `4,194,304`, uint32 item size `4`, injectivity hard-stop policy, and
payload totals in input/checkpoint metadata. Each one-time qid insertion is
charged to `fibre_scans`.

## Exact bytes / SHA-256 (post-edit working tree)

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_positive_common_word_colgen_v1.py` | 99,859 | `3057ee56b804ab43364325f9b6e0816aa032d8df41261bda6e6ce6606a67b7f3` |
| `crosscheck/check_d972_r07_positive_common_word_colgen_v1.py` | 57,363 | `968400a325cedd2ff5e57db61305e792d8585f536e85218424cc62f2463ce858` |
| `search/d972_r07_positive_common_word_colgen_gha_driver_v1.g` | 12,453 | `53d1ee8c174f6f497c7c7727e63a13e51330221ce9160ace96fbacfe1b102bea` |
| `search/certs/d972_r07_positive_common_word_colgen_selftest_v1_20260827.json` | 407 | `46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78` |

## Execution / pin blocker

Per commission, Python/Node/GAP/git/GHA were not run. Therefore this is a
static verdict, not a cross-checked or Lean-verified run. The producer,
checker, and driver identities are not yet frozen: parent must perform the
one-time cascade in the required order (task179 producer; checker producer
and shared predecessors; driver producer/checker and all predecessors; reply
identities). Current post-edit producer/checker/driver identities are the
three SHA-256 values listed above; existing old pin constants intentionally
remain until that parent cascade.

## Parent cascade addendum

The later v143/checkpoint audit supersedes the provisional identities above.
After the parent-controlled predecessor and producer-to-checker-to-driver pin
cascade, the final task179 source identities are:

- producer: `119396 / 4dcae739a8d1181341ae90a7375e7ca7c465d404582e53a24b6fc84ab7a3f5f4`;
- checker: `69752 / c2f50def1e1ea348bc2919aff91cba1fa748978a55b1895c9b58a69f673b314f`;
- driver: `12974 / 418ab65951b3fc284bc52b36043685146fd8f9faacdf31e381c365c863edffbd`;
- fixture: `407 / 46a1d80984938afa4f1f5b24ff90b407fb8bf2b7f094a9c4f124c0304c5c7c78`.

This addendum freezes identities only; GHA execution is recorded separately.

## Final superseding identity note

The task175 symbol repair and the checker mutation-gate repair caused one
later full cascade. The next-run identities superseding every earlier table
in this reply are producer
`119396 / 448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512`,
checker
`70020 / 473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d`,
and driver
`12974 / eee30a3f482704799dee75e0b0663ceb53b27f3e420d2413cca7bb08262f37fa`.
