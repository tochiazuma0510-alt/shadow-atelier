# Luna Task669 — Task640 v6 parent-verdict layout repair

## Role and exact defect

You are Luna.  Make one finite workflow-only repair after Task640 v5 run
`33752047946/1`.

The v5 run proved the cap/path repairs correct: step 10 reran the exact
Task625 checker and byte-compared it successfully.  Step 11 then failed before
rho2 arithmetic because both fresh producer and checker require these two
byte-equal files inside the payload directory:

```text
task625-verdict.json
task625-replayed-verdict.json
```

The workflow copied only the second; the original accepted verdict remained
at the artifact root.  The exact error was:

```text
[Errno 2] No such file or directory:
/home/runner/work/_temp/task625/task625-payload/task625-verdict.json
```

## Authorized edits

Create only:

- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v6.yml`
- `sol/luna_reply_669_r07_task640_parent_verdict_layout_v6.md`

Do not edit v5, either Python executable, any proof, v220, or any other file.
No git, GHA dispatch, download, or heavy/local production run.

## Required delta

Copy v5 byte-for-byte, then make only these changes:

1. mechanical `v5 -> v6` workflow/display/artifact labels;
2. make the job inert with the standard top-level job guard
   `${{ false && (...) }}` while preserving the event predicate;
3. immediately after the successful `cmp`, copy the exact accepted root
   verdict into the canonical payload filename:

   ```bash
   cp "$RUNNER_TEMP/task625/task625-verdict.json" \
      "$RUNNER_TEMP/task625/task625-payload/task625-verdict.json"
   ```

4. retain the existing copy of the byte-equal replay to
   `task625-replayed-verdict.json`.

There is no Python, cap, path, timeout, checkout, pin, artifact-source, or
resource-policy change.  Do not bypass or shorten the 11m49s exact parent
replay.  Do not merge the artifact roots.

## Bounded checks and reply

Run serial static checks only: safe YAML parse; exact semantic diff after
normalizing version labels and inert guard; prove both required payload
filenames are created after `cmp` and before step 11; prove all accepted v5
pins/paths/caps remain byte-identical; action SHA pins and inert guard scan.

Write the designated reply with v5/v6 bytes, LF lines, SHA-256, exact diff and
commands.  End `READY_FOR_SOL_LAYOUT_AUDIT` or `NOT_READY`.  Candidate only;
`verified=false`.
