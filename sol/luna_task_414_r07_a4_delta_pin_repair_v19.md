# Luna task 414 — R07 A4 delta-checkpoint canonical pin repair v19

Role: Luna mechanical versioning and bounded checks only. Do not change A4
arithmetic, row order, reducer, oracle, cap, or mathematics. Do not run heavy
production, commit, push, dispatch GHA, edit a workflow, or touch existing
files.

## 1. Exact defect and frozen source

Task409 v17 is rejected for two reasons: it pins a non-existent row-25
checkpoint and its every-row full snapshots necessarily exceed the persistent
2 GB accounting cap. Task410 v18 already replaces those full snapshots by an
append-only delta chain, but its sole stated blocker is the same wrong legacy
base pin.

The canonical checkpoint embedded in driver v30 is exactly:

```text
bytes   = 25581
sha256  = 595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445
schema  = d972-r07-word-independent-successor-kernel/v6/checkpoint/v1
next_row = 25
code_sha256 = 964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7
```

The erroneous hash contains `...d871d4dc...`. Replace it with the canonical
`...d871c4dc...` everywhere it is an expected legacy-base identity. Do not
weaken or remove authentication.

Use task410's current outputs as frozen implementation inputs:

```text
search/d972_r07_word_independent_successor_kernel_v18.py
  27094 bytes
  6d8b53755fc0c9e35aad6f04959f828a6ce5108767ffc57edfaa896366673f5a
crosscheck/check_d972_r07_word_independent_successor_kernel_v24.py
  7508 bytes
  3e10816d31a791695cf0b01fb1386ceb9c0dcd064dfcde63ab59e413278be2c6
search/d972_r07_word_independent_successor_kernel_gha_driver_v32.g
  3964 bytes
  260209f014eefe035f76b9f11fdf0aa50f79496eadd14c3bf102b54c4be27acd
```

## 2. Create only four outputs

1. `search/d972_r07_word_independent_successor_kernel_v19.py`;
2. `crosscheck/check_d972_r07_word_independent_successor_kernel_v25.py`;
3. `search/d972_r07_word_independent_successor_kernel_gha_driver_v33.g`;
4. `sol/luna_reply_414_r07_a4_delta_pin_repair_v19.md`.

The producer may wrap/freeze v18, replace the bad base hash with the canonical
hash at an exact asserted cardinality, and version checkpoint schema v26 to
v27. The checker must similarly pin v19/schema v27 and the canonical base.
The driver must version v32 to v33, pin the new producer/checker bytes and
hashes, install the embedded base under the delta-chain base path, and require
the canonical hash before Python starts.

Do not fall back to v17 full snapshots. Keep task410's append-only segment,
rolling-chain, atomic HEAD, orphan/reorder/fork rejection, resource terminal,
and RESUME semantics unchanged.

## 3. Bounded gates only

Run compile/restore/hash/GAP-parse and the existing tiny two-segment delta
roundtrip. Additionally decode the embedded v30/v33 base and assert the five
canonical fields above. Confirm statically that:

- the generated producer contains zero erroneous `...d871d4dc...` strings;
- it contains the canonical hash in every legacy-base identity gate;
- completed rows call the delta writer, not full snapshot serialization;
- the persistent byte counter charges only newly encoded segment plus HEAD;
- the driver has a literal RESUME path and no SELFTEST before production.

Do not add more tests, mutations, profiling, or refactors. Report exact output
bytes/SHA-256 and the exact generic `gap-run.yml` dispatch inputs if all gates
pass. Otherwise report one concrete blocker.

`TASK414_R07_A4_DELTA_PIN_REPAIR_V19`
