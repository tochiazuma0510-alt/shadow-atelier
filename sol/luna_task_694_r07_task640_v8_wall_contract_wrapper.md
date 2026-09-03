# Luna Task 694 — Task640 v8 wall-contract wrapper

## Scope

The accepted v7 run `33756591288/1` replayed the exact Task625 parent successfully, then the fresh rho2 producer stopped immediately with

`{"error":"wall_seconds_must_equal_9600","status":"NOT_READY"}`.

The cause is narrow: `load_all_seven()` constructs the frozen v12f `Meter`, whose authenticated constructor requires exactly `9600`, while v7 supplies `TASK640_SECONDS=5400`.

## Required implementation

1. Create `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v8.yml` from accepted v7.
2. Keep the global `TASK640_SECONDS: "5400"` and every arithmetic/source pin unchanged.
3. On **only** the step `Produce and independently check fresh rho2`, add a step-local environment override `TASK640_SECONDS: "9600"`. Keep both outer `45m` process timeouts and the `120` minute job timeout unchanged.
4. Mechanically rename only version-bearing wrapper labels from v7 to v8: workflow name, push path/self path, fire marker, authentication step label, and uploaded artifact names. Do not change producer, checker, their hashes, parent replay, limits, commands, or add tests/audits.
5. Check YAML/text mechanically and report exact bytes, LF lines, SHA-256, and a diff summary in `sol/luna_reply_694_r07_task640_v8_wall_contract_wrapper.md`.

## Mutation boundary

Modify/create only:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v8.yml`
- `sol/luna_reply_694_r07_task640_v8_wall_contract_wrapper.md`

Do not dispatch, commit, or push.
