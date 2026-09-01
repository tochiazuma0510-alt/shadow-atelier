# Luna task 441 - checker context closure v6

Task440 v5 repaired the missing `dual`, but a full read-only inventory of the
pinned v1 checker shows that its reduced `P` literal also drops `base` and
`t413`, which `direct_blobs` necessarily reads during ACTIVE replay.  Run
`33496315594` was cancelled around three minutes, before reaching this
deterministic next `KeyError`, rather than spending another full producer run.

The audited root-key inventory after reduced-P construction is exactly

```text
pres runtime owner model p176 q target g760 dual base t413
```

The literal already retains the first eight.  Exactly `dual`, `base`, and
`t413` are absent.  Bootstrap P0 supplies authenticated `base,t413`; prefix
supplies `dual` as return slot 1.  Close these three dataflow edges together.

## 1. Allowed outputs

Create only:

1. `crosscheck/check_d972_r07_a0_actual_b72_first_active_v6.py`
2. `search/d972_r07_a0_actual_b72_first_active_gha_driver_v6.g`
3. `sol/luna_reply_441_r07_a0_checker_context_closure_v6.md`

Do not modify v1--v5 or any other file.  No local production/heavy checker,
Q0, commit, push, dispatch, download, workflow edit, or framework repair.

## 2. Comprehensive checker wrapper

Byte-pin the exact v1 checker (13,834 bytes,
`3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916`).
Keep the independent p176 dict-plus-attribute and authenticated
`base["load_json"] is t413["load_json"]` adapter.

Use a private closure state.  The bootstrap wrapper must call the original
once, adapt it, retain the identical adapted `P0["base"]` and `P0["t413"]`
objects in that state, and return the same adapted P0.  The prefix wrapper
must call the original once, require its unchanged tuple and non-None slot-1
dual, then inject into its reduced P exactly:

```text
P["dual"]  is result[1]
P["base"]  is saved adapted P0["base"]
P["t413"]  is saved P0["t413"]
```

Return the identical original prefix tuple.  Require all three object
identities.  Do not add any other production key or alter any v1 gate.  Keep
artifact schema v4 and use a unique v6 checker marker.

The self-test must use separate sentinel objects to prove all three identity
bindings and unchanged tuple identity, then run the unchanged ten mutation
rejections.

## 3. Driver

Pin and execute the exact audited v4 producer (3,619 bytes,
`6ffbdf76259de7072f58d1be1d0f0a4156b635290c5a0e07a234989d442e1d2f`)
with the v6 checker.  Use fresh v6 result/checkpoint/log paths, external v6
preamble, unchanged 2,400-second/4.8-GB producer caps, v4 producer marker,
v6 checker PASS marker, and unique v6 driver PASS marker.  No old closure.

Run only syntax compilation, the three-object identity self-test plus ten
mutations, static driver pin/command reconstruction, and `git diff --check`.
Report exact bytes/SHA-256 and stop.
