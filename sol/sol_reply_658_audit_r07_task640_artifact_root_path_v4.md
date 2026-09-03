# Sol(max) Task658: bounded path-only audit of Task640 workflow v4

## Verdict

For the exact frozen v4 input:

`FAIL`

`SAFE_TO_DISPATCH_GHA=no`

The four artifact-root path corrections are exact and sufficient, but the
frozen v4 workflow is not inert: its job condition contains no `false &&`.
This violates the explicit Task657/658 release condition and permits a
`workflow_dispatch` to execute immediately.

During this audit, another task added the missing guard and changed the v4
file.  Therefore the final working-tree input is also:

`INPUT_MISMATCH`

The new, unfrozen file is not adjudicated by Task658; it requires the separately
frozen Task660 audit.  No workflow was dispatched, no production computation
was run, and no implementation or git operation was performed.

## Frozen-input check

At the start of the audit all three Task658 inputs matched exactly:

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,959 | 160 | `f0dabf6a9cef421f6849391fcb1b2e2f229333d90eab61fb61a0fe95dcdc8ac4` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml` | 10,023 | 160 | `c8deb31cf87554500d665ab6a9740af0529204858d5ec30a91be5b55735dac58` |
| `sol/luna_reply_657_r07_task640_artifact_root_path_v4.md` | 1,106 | 23 | `d2261347cf138ed7ccc3b7d2d6e978371c21157fbe0d099ca069fef470312ff0` |

The subsequently changed v4 is 10,038 bytes / 161 LF lines / SHA-256
`3a91aca913faf79dadd0e16d181c6e270df660ead0b19acbd6045b2f7cfb92fb`.
Removing its one newly added `      false &&` line in memory reconstructs the
exact frozen 10,023-byte `c8deb31c...` input.  This establishes both the
concurrent input change and the precise missing line without writing a file.

## Artifact layout -- PASS

The Task625 workflow
`.github/workflows/d972-r07-a0-grade1-selected-slp-v3.yml` lines 103--112
uploads two roots in one artifact:

- `${{ runner.temp }}/task625-payload/`;
- `${{ runner.temp }}/task625-verdict.json`.

Their least common directory is `${{ runner.temp }}`, so download into
`${{ runner.temp }}/task625` preserves `task625-payload/` as a subdirectory and
places `task625-verdict.json` at the download root.  The failed-run receipt for
`33749395427/1` independently records that the root verdict `test -s` passed,
then the old checker failed on
`/home/runner/work/_temp/task625/manifest.json`.  This is exactly the layout
predicted by the two upload roots: the manifest is instead under
`task625/task625-payload/manifest.json`.

## Four consumers -- PASS

The frozen v4 changes exactly the four payload-directory consumers:

- line 125: old checker `--payload`;
- line 127: replayed-verdict destination copied into the payload directory;
- line 136: producer `--task601`;
- line 140: new checker `--task601`.

All four use `$RUNNER_TEMP/task625/task625-payload`.  The authenticated uploaded
verdict stays at the download root: line 122 tests it and line 126 compares it
byte-for-byte with the replayed verdict.  There are exactly four occurrences
of the nested payload root and one each of the root verdict test and compare.

## Exact delta -- FAIL only on the inert guard

The complete frozen v3/v4 diff contains only:

- mechanical v3-to-v4 workflow name, self-path, fire marker, authentication
  label, and the two output artifact labels;
- the four payload-root corrections above.

Reversing those substitutions in memory makes the frozen v4 byte-identical to
the released v3.  In particular, the diff contains no added inert guard.
Frozen v4 lines 39--41 are:

```yaml
if: >-
  (github.event_name == 'workflow_dispatch' ||
   contains(github.event.head_commit.message, '[fire-fresh-precision2-endpoint-v4]'))
```

The first disjunct is true for a manual dispatch.  Thus Task657's report that
the inert-guard check passed is contradicted by the exact frozen bytes.

Smallest finite repair: insert `false &&` as the first continuation line of
the job condition, then freeze the resulting workflow bytes/SHA and audit that
new version.  No path, arithmetic, pin, limit, or output change is needed.

## Unchanged regression surface

On the exact frozen bytes, bounded static checks found:

- safe YAML parsing: PASS;
- all seven `uses:` entries pinned to full 40-hex action revisions: PASS;
- producer, checker, Task640 reply, prebuild, Task625 producer/checker, and all
  paper/audit receipt SHA pins match their local exact files: PASS;
- Task625 run/attempt/head/job/workflow/artifact identity and digest gates are
  unchanged at lines 77--95;
- all three download definitions are unchanged at lines 96--117;
- job timeout 120 minutes, both process timeouts 45 minutes, 8 GiB virtual
  memory limit, and seconds/RSS/durable/path/trie/state/record caps are
  unchanged;
- the residual artifact remains guarded by `${{ success() }}` and the logs by
  `${{ always() }}`.

No Python mathematics was rerun.

## Claim boundary

This audit proves no rho2 value, grade-two MEMBER/NONMEMBER result, A0,
order-54,432/full-Q0 result, compatible cofinal lift, fake, Ihara,
cross-check, or Lean verification.  The frozen v4 is not authorized for a
Task640 run.

`verified=false`
