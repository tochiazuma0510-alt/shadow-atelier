# Luna task 450 -- resume the A0 ladder from the cross-checked rank-51 checkpoint

Role: Luna implementation/compute preparation.  Do not launch local heavy
computation and do not perform git, push, or GHA operations.  The parent is
the sole broker.

## Frozen input

Use the exact Task448 artifact downloaded at

```text
C:\Users\81905\AppData\Local\Temp\task448_run33504248130_7ec6ed0cb38d4cc09911676f05d0c20c\gap-run-out\d972_r07_a0_actual_tau_free_rank_ladder_v5_output.checkpoint
```

It must be copied into the repository with `apply_patch`, byte for byte, as

```text
search/certs/d972_r07_a0_actual_tau_free_rank51_checkpoint_v1.json
```

and must have exactly 10,934 bytes and SHA-256
`a83959e4c9fcfa79093c712e82164d47c31b78c9fc00b512f7adac9413c481f4`.
Its authenticated fields are `rank=51`, `accepted_count=8`, `round=9`, and
internal `state_sha256=22dcfdfb396524ea5853488aa2ad52d28b4f7d10164123bc83f121e59dd83159`.

## Implement only the continuation transport

Create:

```text
crosscheck/check_d972_r07_a0_actual_tau_free_rank_ladder_v6.py
search/d972_r07_a0_actual_tau_free_rank_ladder_gha_driver_v6.g
sol/luna_reply_450_r07_a0_rank51_checkpoint_resume_v6.md
```

The v6 driver must:

1. exact-pin the unchanged v3 producer, unchanged v5 checker dependency or
   the new v6 checker, and the repository checkpoint above;
2. require an external v6 preamble;
3. copy the pinned checkpoint to a fresh direct child of `ci/out` and invoke
   the unchanged v3 producer with `--resume` pointing to that copy;
4. write fresh v6 artifact/checkpoint/log paths;
5. give the producer 7,200 seconds, RSS 4,800,000,000 bytes, and 64 new rises;
6. run the new independent v6 checker and require its PASS marker; and
7. contain no production SELFTEST/FIXTURE and no eager new store, closure,
   actor-adapted rebase, or search-universe change.

The v6 checker must exact-pin and delegate the full v5 checker, independently
authenticate the frozen input checkpoint seal, require the final
`accepted_sources` to have its eight records as an exact prefix, and require
rank/count/round monotonicity.  The delegated v5 checker must still rebuild
all final accepted rows and the terminal profile.  Add only small synthetic
mutation tests for checkpoint seal, altered prefix, and decreasing rank/count;
do not run production in self-test.

This task is transport only.  The current terminal is a time cap, so do not
implement v413/v414 branches until an actual mathematical gate requests one.
Report exact bytes/SHA-256 and bounded compile/self-test commands in the reply.
