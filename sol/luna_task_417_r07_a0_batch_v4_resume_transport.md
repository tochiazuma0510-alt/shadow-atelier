# Luna task 417 — R07 A0 batch-v4 exact resume transport

## Role and scope

You are Luna, the implementation/calculation owner.  Implement only the
minimal versioned GHA driver and its reply described below.  Do not modify
the producer, checker, workflow, prior task files, proof files, or v220.  Do
not run the heavy production search locally or dispatch GHA.  Parent is the
only commit/push/dispatch broker.

Allowed new files:

1. `search/d972_r07_history_free_positive_fast_resume_gha_driver_v31.g`
2. `sol/luna_reply_417_r07_a0_batch_v4_resume_transport.md`

## Authenticated prior state

The successful workflow container run is `33300457583`, head
`4fa8a7d936e7f86f22964d512aab664e45402483`, artifact id `9730051236`,
artifact name `gap-run-out`, artifact digest
`sha256:fc83f49e361733889990e25ab99c8b641d62b9ff827d64445087d2585b6d2377`.

After the existing workflow download step, the exact resume input is:

`ci/in/prior/d972_r07_a0_batch_lazy_owner_v4.checkpoint`

It has exactly 129119626 bytes and SHA-256
`1deed5488a8051102a3fbc80d65432b6f461fdf35c7db46e51261610b7e4a3d5`.
Its header is `D972-A0-LAZY-CP2`, whose sealed payload length is 129119534
and whose payload SHA-256 is
`14f38dedf5e1704dbac48ae41e7374adbd397b0f5e98b502eb7e554066bad96d`.

The prior mathematical terminal is honestly `UNKNOWN_RESOURCE`, caused by
`seconds:positive_lazy`; the last observed progress is round 648, rank
60258, boundary_pairs 10102480, RSS 2727055360 bytes, elapsed 6017.562 s.
Do not promote this to COMMON, NONMEMBER, fake, witness, or exhaustive.

## Required driver behaviour

Create the v31 `.g` driver.  Its filename deliberately begins with the
existing workflow's guarded prefix
`search/d972_r07_history_free_positive_fast_resume_gha_driver_v` so the
already-present authenticated artifact-download step is selected after the
parent receives approval to update its pinned run/artifact/head constants.

The driver must:

1. byte-pin the existing files it executes, at least
   `search/d972_r07_a0_batch_lazy_owner_v4.py` and
   `crosscheck/check_d972_r07_a0_batch_lazy_owner_v4.py`;
2. fail closed unless the prior checkpoint exists with the exact byte count
   and full-file SHA-256 stated above;
3. invoke the unchanged v4 producer in `PRODUCTION` with the prior file as
   `--resume`, a fresh output receipt/log/checkpoint under `ci/out`,
   `--seconds 18000`, `--rounds 1000000`, `--batch-cap 128`, and the existing
   safe RSS cap (5700000000 bytes);
4. run the unchanged checker on the fresh receipt;
5. copy neither the old checkpoint nor large data unnecessarily;
6. always leave the new checkpoint in `ci/out` when the producer returns
   `UNKNOWN_RESOURCE`, so artifact upload can resume it again;
7. print a unique final marker only after producer and checker return zero.

Use ASCII only in the `.g` file.  Keep quoting simple and fail closed.  A
bounded local gate may check GAP parsing, `--help`, hashes, and fixture-sized
behaviour, but must not load/decode the 129 MB state or start production.

In the reply, report exact byte/SHA pins, bounded gates, and the literal GHA
script path/inputs the parent should dispatch.  Do not claim workflow approval
or production execution.
