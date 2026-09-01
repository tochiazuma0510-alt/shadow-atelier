# Luna task 440 - checker dual-bind hotfix v5

Task439 v4 run `33444570055` produced an actual
`ACTIVE_COLUMN_READY` at seed 1, coordinate 0, fibre cursor 1 in the log
(zero-based receipt cursor 0), with strict rank transition `[43,44]`.  The
producer completed successfully.  The independent v1 checker then failed
before ACTIVE replay at `formulas`, exact exception `KeyError: 'dual'`.

The checker `check` receives `dual` from `prefix(v12,P)` but does not restore
it as `P["dual"]`; its `formulas` immediately reads that key.  This is a
checker-only dataflow omission.  Do not alter the producer mathematics or the
ACTIVE artifact.

## 1. Allowed outputs

Create only:

1. `crosscheck/check_d972_r07_a0_actual_b72_first_active_v5.py`
2. `search/d972_r07_a0_actual_b72_first_active_gha_driver_v5.g`
3. `sol/luna_reply_440_r07_a0_checker_dual_bind_hotfix_v5.md`

Do not modify v1--v4 or any other file.  No local production, heavy checker,
Q0, commit, push, dispatch, download, workflow edit, or framework repair.

## 2. Checker-only repair

Byte-pin the exact v1 checker (13,834 bytes,
`3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916`).
Retain the independent p176 dict-plus-attribute and authenticated
`base["load_json"] is t413["load_json"]` bootstrap adapters from v4.

Wrap the checker's `prefix` before calling unchanged `m.check`: call the
original prefix, require its tuple has a non-None dual in slot 1, set
`P["dual"]` to that identical object, and return the unchanged tuple.  This
must be the only production repair.  Keep the certificate schema at v4 (the
producer artifact schema), but use a unique v5 checker marker.  Do not import
the producer or weaken any formula, ACTIVE, rank, row, exponent, scalar,
pivot, status, or mutation gate.

Add a tiny self-test proving that the wrapper installs the identical returned
dual object in a toy P, then run the unchanged ten mutation rejections.

## 3. Driver

The v5 driver must pin and execute the exact audited v4 producer
(3,619 bytes,
`6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f`)
with the new v5 checker.  Use fresh v5 result/checkpoint/log paths, an external
v5 preamble, the unchanged 2,400-second and 4.8-GB producer caps, the v4
producer marker, the v5 checker PASS marker, and a unique v5 driver PASS
marker.  The producer is deterministic and positive-first; no occurrence or
boundary closure may be called.

Run only syntax compilation, checker self-test, static driver pin/command
reconstruction, and `git diff --check`.  Report exact bytes/SHA-256 and stop.
