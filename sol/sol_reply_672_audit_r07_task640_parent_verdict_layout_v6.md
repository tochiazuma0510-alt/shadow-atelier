# Sol(max) Task672: Task640 v6 verdict-layout audit

## Verdict

`verified=false`

The v6 workflow closes exactly the parent-verdict layout failure recorded by
Task670.  No Python mathematics was rerun, and no code, workflow, GHA, download,
production, or git state was changed.  The v220 counters remain first rung
`1/6` and A0 actual `0/1`.

## Audited inputs

| path | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v5.yml` | 10,061 | 161 | `22e4b1ef0a9b50fad79fc9b08914b6e77c463769b6f02fb75d48da9fd71b6b1a` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v6.yml` | 10,178 | 160 | `72a1d5635f8fc8234b81c2a82bd308d2203c3dd4d5042ceb1888bee5601f7525` |
| `sol/luna_task_669_r07_task640_parent_verdict_layout_v6.md` | 2,365 | 67 | `b78f13680f22a8d9c9e8aebe77b337dbc43a50e7b1b9ae6f5c02a008662898cb` |
| `sol/luna_reply_669_r07_task640_parent_verdict_layout_v6.md` | 1,203 | 25 | `722f8a804196c126a2e8a5713c569ee8f8cfc4c0852a3dec7a53aadf175d793f` |
| `sol/sol_reply_670_root_task640_v5_result.md` | 1,829 | 49 | `507575347d375f6004205be6f194977df8852b49d3134d6e15ee41183622e3c7` |
| producer consumer | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| independent consumer | 92,071 | 1,563 | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |

## Layout and ordering

Both fresh consumers require the exact files below inside the directory passed
as `--task601`:

```text
task625-verdict.json
task625-replayed-verdict.json
```

The producer reads them at lines 176--180 and the independent consumer at
lines 326--328.  V6 supplies both before the Task640 step, in this exact order:

```text
Task625 checker replay
cmp root/task625-verdict.json replayed-verdict.json
cp root/task625-verdict.json payload/task625-verdict.json
cp replayed-verdict.json payload/task625-replayed-verdict.json
Task640 producer and independent checker
```

The `cmp` is line 125, the new original-verdict copy is line 126, and the
existing replayed-verdict copy is line 127.  The first copy's source is the
authenticated artifact-root verdict; the second copy's source is the verdict
just produced by the exact Task625 checker replay.  Neither copy occurs before
the successful byte comparison, so both canonical payload files are byte-equal
to the authenticated original when the next step starts.

## Exact normalized diff

I normalized only the v5/v6 workflow name and self-path, fire marker,
authentication label, two artifact labels, and the differently formatted
inert job condition.  The entire remaining unified semantic diff is exactly:

```diff
+          cp "$RUNNER_TEMP/task625/task625-verdict.json" "$RUNNER_TEMP/task625/task625-payload/task625-verdict.json"
```

Deleting that one line from normalized v6 makes it byte-identical to normalized
v5.  Thus no path, replay, cap, pin, download, timeout, action, upload, or
resource-policy change is hidden in the repair.

## Static regression gates

- PyYAML safe parsing: PASS; the expected single `fresh-endpoint` job exists.
- The job condition is exactly an expression beginning `${{ false && (` and
  is therefore inert.  Removing only `false && ` and normalizing the v6 fire
  label reproduces the v5 event predicate modulo YAML whitespace; no event
  branch changes.
- Task625 nested payload path, accumulated cap `50000000`, run/attempt/job/head,
  artifact service checks, and the exact Task554/Task595 downloads are
  byte-unchanged.
- All producer/checker/reply/prebuild hashes and literal dependency hashes are
  byte-unchanged.  The four environment-pinned local files were recomputed and
  matched their hashes.
- Task640 seconds/RSS/durable/path/trie/state/record caps, 120-minute job
  timeout, both 45-minute process timeouts, and `ulimit -v 8388608` are
  unchanged.
- All seven `uses:` entries retain full 40-hex action pins.  There remain
  exactly three downloads; residual upload is `${{ success() }}`-only and log
  upload remains `${{ always() }}`.

This is a workflow-layout candidate only and establishes no rho2 or downstream
mathematical claim.

PASS_LAYOUT_ONLY / SAFE_TO_DISPATCH_GHA=yes
