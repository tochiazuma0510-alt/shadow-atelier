# Luna Task484 — rank-84 single-row continuation v8

## Role

You are Luna.  Preserve the newly cross-checked Task461 single-row lane and
make one narrow GHA continuation driver.  Do not alter the arithmetic or run
production locally.

Immutable source run:

```text
run      33524681526
job      99912387760
head     dd67f12b0ee4f022061df27ed396ad3d3a37f264
artifact 9812928957 (gap-run-out)
API zip digest sha256:4b3239f35f6ec2a4859e6a81e2b49456702f0f22f695a7332089b407dbcb817d
```

The producer reached and the independent v7 checker accepted:

```text
status=UNKNOWN_RESOURCE
reason=UNKNOWN_RESOURCE:tau_free_localized_dual:time_limit
rank=84 accepted_count=41 round=44
state_sha256=3c38d9021e20c04a24e99136e47902e8911658f244a202f9c49f4a4280e2f6a7
```

Permanent exact release asset:

```text
URL https://github.com/tochiazuma0510-alt/shadow-atelier/releases/download/archive-gha-checkpoints/artifact_9812928957_gap-run-out.rank84.zip
bytes 23004
sha256 dde60bad768e20ead6ad08e8bd0a8e53fc97050a43f6c207552ba97d579c438a
```

Exact resume member:

```text
d972_r07_a0_actual_tau_free_rank_ladder_v7_output.checkpoint
52707 eb1a6d69a855b88d2a934dbf8e58c0f539a7a4d6802cc4a5c7f544b0880da24f
```

Reuse unchanged:

```text
search/d972_r07_a0_actual_tau_free_rank_ladder_v3.py
12215 0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37
crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v7.py
3653 e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1
```

## Driver contract

Create one ASCII GAP driver which requires an external preamble, downloads
and authenticates the permanent zip, extracts in a fresh owned directory,
authenticates the exact rank-84 checkpoint and copies it to a fresh `ci/out`
resume path.  Invoke exactly one real producer from that checkpoint with
`--seconds 7200 --rss-bytes 4800000000 --max-rises 64`, then exactly one v7
independent checker on its result.  Use an external producer wall strictly
above 7200 and a hard VM limit strictly above 4.8e9 bytes, leaving real
serialization margin.  Require exact producer/checker/driver markers,
nonempty result/checkpoint and no stale output.  Do not treat workflow success
or RESOURCE as A0 completion.

Run only source-pin/static/GAP parse checks.  No production, GHA, workflow
edit, git, or bytecode cache.

## Exact outputs

1. `search/d972_r07_a0_actual_tau_free_rank84_resume_gha_driver_v8.g`
2. `sol/luna_reply_484_r07_rank84_single_row_continuation_v8.md`

End with `TASK484_R07_RANK84_SINGLE_ROW_CONTINUATION_V8_PASS` or typed STOP.
