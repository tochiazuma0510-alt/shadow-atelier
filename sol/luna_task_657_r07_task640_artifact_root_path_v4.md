# Luna Task657 — Task640 artifact-root path repair, workflow v4

## Scope

You are Luna. GHA run/attempt `33749395427/1`, head
`288c55af9f5cf30d4a58278680ec56ed2f4a51d7`, passed checkout, source pins,
selftests, service authentication and all three downloads, then failed before
Task640 production at step 10. The exact error was:

```text
[Errno 2] No such file or directory: /home/runner/work/_temp/task625/manifest.json
```

The Task625 upload used two path roots: `task625-payload/` and
`task625-verdict.json`. Consequently download correctly places the manifest at
`$RUNNER_TEMP/task625/task625-payload/manifest.json`, while the verdict remains
`$RUNNER_TEMP/task625/task625-verdict.json`.

Create a versioned workflow
`.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml` from the
released v3 workflow. Do not modify either Python executable or any
mathematics. Write only
`sol/luna_reply_657_r07_task640_artifact_root_path_v4.md` besides the new
workflow.

## Exact allowed delta

1. Change workflow name/self-path/fire marker and output artifact labels from
   v3 to v4 mechanically.
2. Keep the uploaded verdict comparison at
   `$RUNNER_TEMP/task625/task625-verdict.json`.
3. Change only the Task625 payload-directory uses to
   `$RUNNER_TEMP/task625/task625-payload`:
   the old-checker `--payload`, destination of
   `task625-replayed-verdict.json`, producer `--task601`, and new checker
   `--task601`.
4. Keep all exact code/parent/action/reply pins, limits, download definitions,
   success-only residual upload and fail-closed behavior unchanged.
5. Keep the v4 workflow inert under `false &&`. Do not dispatch it.

Run bounded YAML parsing, shell/path static checks, exact semantic-diff census,
action-pin scan and inert-guard check. Do not run Python production, GHA or git.
The reply must give exact bytes/LF/SHA-256, enumerate every changed line and
show there is no other semantic delta. End with
`READY_FOR_TASK658_PATH_ONLY_AUDIT` or `NOT_READY`.
