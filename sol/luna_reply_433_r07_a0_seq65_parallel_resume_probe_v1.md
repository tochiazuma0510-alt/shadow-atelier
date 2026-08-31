# Luna reply 433 — sequence-65 continuation and positive probe

Implemented the four allowed outputs only. The continuation driver uses the
canonical sequence-65 occurrence checkpoint directly, while the v2 probe is a
mechanical task432 wrapper fork with the false-truth deque, pinned v12 import,
independent input seal, resource normalization, no checkpoint output, and all
promotion flags false.

Pins:

- `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v13.g`: 6988 bytes, SHA-256 `4238b358553cb1ee14d0861416184746e003f094a55bb638a62a85a910846896`
- `search/d972_r07_a0_prefix_positive_probe_v2.py`: 6271 bytes, SHA-256 `e04121d1f451031fb18b519a74330d357d9b9f79027ce2614c2ecf3e72e86fed`
- `search/d972_r07_a0_prefix_positive_probe_gha_driver_v2.g`: 6856 bytes, SHA-256 `06c9f5f00a22c53f9f947eee2ce6b0a99089a4262bb9aef3e0675886b5edeee6`
- `sol/luna_reply_433_r07_a0_seq65_parallel_resume_probe_v1.md`: this designated report (not self-pinned)

The unchanged v12 producer/checker pins are preserved: producer 51884 bytes,
SHA-256 `3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3`;
checker 13334 bytes, SHA-256
`e6a16f63725cd23bb1cd8469e2a0d93c7774c979079b7314b653b7ffa439f891`.

The sequence-65 release is pinned to zip 178918944 bytes, SHA-256
`b27a70ffe4095f9c9760c51694e7b56d68efb3e22d7df4ecaab4513f7328dbcc`, with
checkpoint entry bytes 461087575 and SHA-256
`8918df4407e91a7b4ab1a29246a23ba5b0ed1a7b6011f4abf74775cc33d82705`.
The continuation uses a distinct v13 recovery path and output checkpoint; the
probe uses distinct v2 paths and no output checkpoint.

Bounded gates passed:

- v2 AST/compile and fixture without repository bytecode;
- unchanged v12 producer fixture and checker self-test;
- v2 source allowlist/no-checkpoint-write checks;
- one-entry roster, exact recovery pins, external preambles, marker, and
  reconstructed GAP receipt checks;
- `git diff --check` on all four outputs.

These are positive-discovery paths only. A probe `UNKNOWN` is not a negative
result and never yields `NONMEMBER`; neither path promotes COMMON_WORD,
compatible lift, fake, or Ihara witness without the registered strict replay.
No download, checkpoint load, production run, workflow edit, release
operation, commit, push, or dispatch was performed.

## Parent dispatch record

The independent final-pin audit returned `GO`.  The parent committed and
pushed the exact audited files at immutable head
`b93faa0155b424b7f536058da10d969cfc8f3f14`; no workflow file changed.
Generic `gap-run.yml` dispatches are:

```text
continuation run/job  33384438113 / 99463763995
script                search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v13.g
preamble              D972_R07_A0_PB34_V13_RUN:=true;;

positive run/job      33384440172 / 99463770166
script                search/d972_r07_a0_prefix_positive_probe_gha_driver_v2.g
preamble              D972_R07_A0_PREFIX_POSITIVE_PROBE_V2_RUN:=true;;

common inputs         out_dir=ci/out, timeout_min=180,
                      with_pquot_packages=false
```

Both use the same immutable sequence-65 checkpoint in independent runners.
The probe cannot mutate or replace the continuation.
