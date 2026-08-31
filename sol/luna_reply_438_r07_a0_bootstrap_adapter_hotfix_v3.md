# Luna reply — Task438 bootstrap-adapter hotfix v3

Implemented only the four authorized v3 outputs.  The thin producer and
independent checker wrappers byte-pin Task436 v1, wrap `p176` with the
dict-plus-attribute adapter, and inject `base.load_json` using the
authenticated `t413.load_json` identity.  The v1 algorithms and all
mathematical/status gates remain unchanged; schema, markers, and driver paths
are v3-specific.

The producer fixture exercises both ABI repairs on a toy dictionary before
delegating to the v1 72-point fixture.  The checker self-test exercises the
same independent toy adapter before the unchanged ten mutation rejections.

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_actual_b72_first_active_v3.py` | 2964 | `27b0bf8baf22ed815870d45716e813a2646c3e470d03510be0ca2c71fcaccb88` |
| `crosscheck/check_d972_r07_a0_actual_b72_first_active_v3.py` | 2298 | `f7aeeac29fb8a376bc8935124b16b10d085e9d825ea6f2a88cf4cfba37766281` |
| `search/d972_r07_a0_actual_b72_first_active_gha_driver_v3.g` | 2301 | `3ba8ac5d16b7a2ac55e88459056017efa8846db1e492c56cbb9b9141251f5f69` |

Bounded gates only: external-cache `py_compile`, temporary-output producer
fixture, checker self-test, static driver pin/command reconstruction, and
`git diff --check`.  No Q0, formula rebuild, prefix, bootstrap, production,
checkpoint load, download, workflow edit, commit, push, or dispatch was run.

## Parent pre-dispatch gate

The parent independently repeated syntax compilation, the producer fixture,
the checker self-test (all ten mutations rejected), exact SHA-256 pins, and
`git diff --check`.  A separate read-only static audit returned `GO`: both
adapters are installed before `m.run`, the loader is the identical
authenticated `t413["load_json"]` object, the checker remains independent,
and the v3 driver has fresh paths and exact wrapper pins.  Production remains
unrun at this point.
