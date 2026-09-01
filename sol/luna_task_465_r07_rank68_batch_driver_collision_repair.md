# Luna task 465 -- repair Task463 driver filename collision

Role: Luna mechanical repair only.  Do not run production, dispatch GHA,
edit workflows, commit, push, or touch files outside the three paths below.

Task463's producer/checker rebase is retained.  Its requested driver filename
was mistaken: `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g`
is already the committed Task453 batch-cap-64 wrapper and must not be
overwritten.

## Required paths

1. Restore
   `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v2.g`
   byte-for-byte to the committed Task453 owner:

```text
bytes 2387
sha256 8f8c803cff86fbb4bb774570cb596e9e5a8262c05321e955e2cf0de545df60dc
```

If those physical values disagree with the committed HEAD owner, stop and
report the exact HEAD bytes/hash; do not guess.  The semantic requirement is
exact `git show HEAD:<path>` restoration, not preservation of the Task463
working-tree overwrite.

2. Put the already implemented Task463 rank-68 direct driver into the new
   versioned path
   `search/d972_r07_a0_dual_anchored_active_batch_gha_driver_v3.g`.
   It must retain its existing v2 producer/checker pins and artifacts, but use
   a distinct external launch guard and terminal marker:

```text
D972_R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V3_RUN:=true;;
R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V3_DRIVER_PASS
```

The inner producer/checker markers remain their v2 markers.  Keep one
producer, `7200`, `4800000000`, `--max-rises 64`, and `--batch-cap 64`.

3. Report in
   `sol/luna_reply_465_r07_rank68_batch_driver_collision_repair.md`.

Run only byte/hash comparison against committed HEAD, ASCII/final-newline
checks, and static guard/process/cap scans.  Do not modify the Task463 v2
producer, checker, or reply.
