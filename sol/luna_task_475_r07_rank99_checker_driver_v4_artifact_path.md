# Luna Task475 — rank99 checker-only driver v4 artifact-path repair

## Scope

GHA run `33533502342` successfully launched the recovered Python checker, but
it stopped before semantic replay with

```text
FileNotFoundError: ../ci/out/..._archive/d972_r07_a0_dual_anchored_active_batch_v1.json
```

From the isolated cwd `ci/out/<work>`, v3 incorrectly prefixes the already
root-relative `ci/out/<archive>` with `../`.  Repair only this path transport.
Do not edit committed v3, the checker, or any mathematics.

Create v4 with versioned owned output names.  After authenticating the release
zip, copy both the exact artifact JSON and exact checkpoint into
`<work>/ci/out/`, authenticate both copies, `cd <work>`, and invoke the sole
checker on `ci/out/<artifact>`.  The artifact's embedded durable path
`ci/out/<checkpoint>` then resolves to the copied checkpoint in the same cwd.
Preserve all release/six-member/source pins, no-single-quote shell construction,
timeout/RSS, exact-one log equality, collision-safe roots, one checker/no
producer, and receipt bindings.

## Exact outputs

1. `search/d972_r07_a0_dual_anchored_active_batch_recovered_checker_only_gha_driver_v4.g`
2. `sol/luna_reply_475_r07_rank99_checker_driver_v4_artifact_path.md`

Bounded gates must compute the post-`cd` artifact/checkpoint paths and prove
they name the two copied files.  No semantic replay, producer, GHA, workflow
edit, git, or bytecode cache.  End with
`TASK475_R07_RANK99_CHECKER_DRIVER_V4_PASS` or a typed STOP.
