# Luna task 504 - A0 rank-98 checkpoint resume driver v10

Role: Luna implementation only.  The rank-84 v9 production run advanced the
cross-checked single-row ladder to rank/count/round `98/55/59`.  Build only a
surgical continuation driver from that exact checkpoint.  Do not alter the
producer, checker, search order, mathematics, resource bounds, workflows, git,
GHA, A4 or Task193.

Read the exact v9 driver and the v9 production files from the permanent release
specified below.  V10 must be an exact-pin successor of v9, changing only the
source release/member registry, versioned owned paths/markers and immutable
run binding needed to resume rank 98.

## 1. Outputs only

Create only:

1. `search/d972_r07_a0_actual_tau_free_rank98_resume_gha_driver_v10.g`;
2. `sol/luna_reply_504_r07_a0_rank98_resume_driver_v10.md`.

## 2. Exact production premise

- source run `33548094849`, job `99990508106`;
- source head `3d5cac391076553fe68a83343376194dbd9efb6d`;
- API artifact id/name/size: `9821857621` / `gap-run-out` / `74814`;
- permanent release URL:
  `https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9821857621_gap-run-out.a0-rank98.zip`;
- release 30758 /
  `d0293cdd3bab98b792af17064ace21594966a5610e30219842347466e9ade9e4`.

The release has exactly these eight flat members:

```text
d972_r07_a0_actual_tau_free_rank84_resume_v9_input.checkpoint
  52707 eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f
d972_r07_a0_actual_tau_free_rank84_resume_v9_preflight.log
  35 4d3dd0892debc756d57c12ab585ff63d473aad334bf25339c3fe3af6cef79139
d972_r07_a0_actual_tau_free_rank_ladder_v9.json
  70365 2bbe05d8c5c2b97177854e7cd77944e9b89af70cea7f50e7565a6faec3a70b1d
d972_r07_a0_actual_tau_free_rank_ladder_v9_checker.log
  51 aa62a0439618247aff32657b3d05d6c5d104340d161c0aa1b7fafac0b373f7b1
d972_r07_a0_actual_tau_free_rank_ladder_v9_output.checkpoint
  69947 c0fcb581f59c9ed665cf13cb852cb527ef13acdc9bf2102b89c2404bb080d37f
d972_r07_a0_actual_tau_free_rank_ladder_v9_producer.log
  4989 d585eec9c9b2f81a5689749ddc9fbe9d9e5e658651907ae95baf41d8827082fa
driver.g
  126 ee8f36e711d719244b40b283f8d9debcdfd553b4ca0bee8dedcade6cd6ac8081
run.log
  5087 d2c1cc146af7b1af3eddfbd213b29ee2b75e8b8030a77dcff2747dbb9ff2dc7c
```

Important: independently recompute every value above from the release before
freezing.  If any supplied value is mistyped, STOP and report the independently
observed value; do not encode a bad pin.  In particular the resume member is
the 69,947-byte v9 output checkpoint, with binding
`6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3`
and state SHA
`7fd45ecad90fda912df5dfdb15f2f422aa63dc8a3abfc992150079b44405685a`.
It has rank/count/round `98/55/59`, and its first 41 accepted sources equal the
old rank-84 input prefix exactly.

## 3. Frozen computation

Keep the exact v9 producer/checker pins and invocation semantics:

- producer v3 12215 /
  `0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`;
- checker v7 3653 /
  `e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1`;
- producer `--seconds 7200 --rss-bytes 4800000000 --max-rises 64`;
- external producer timeout 7500 seconds, checker timeout 3600 seconds,
  virtual-memory limit 5,200,000 KiB;
- one producer, then one independent checker for its typed terminal;
- exact one-line producer and checker markers and nonempty result/checkpoint;
- no retry, batching change, worker pool, fallback, SELFTEST, or old-prefix
  re-search.

Use v10-owned output/input/log paths and an external preamble named
`D972_R07_A0_RANK98_CHECKPOINT_RESUME_V10_RUN`.  Authenticate the release,
exact eight-entry archive, every member, and the copied resume member before
the producer starts.  Preserve the fail-closed diagnostic and shell quoting of
v9.  End a successful driver with exactly

`R07_A0_RANK98_CHECKPOINT_RESUME_V10_DRIVER_PASS`

## 4. Bounded gates

Run only exact pin/manifest checks, source diff confinement, GAP
`ReadAsFunction`, generated-shell syntax, a fail-closed preflight fixture, and
static one-producer/one-checker/resource-margin checks.  Do not run production
or the real selective runtime.  Fixture success is not A0 progress.

Report exact driver bytes/SHA and end with exactly one of:

`TASK504_R07_A0_RANK98_RESUME_DRIVER_V10_PASS`

or

`TASK504_R07_A0_RANK98_RESUME_DRIVER_V10_STOP`
