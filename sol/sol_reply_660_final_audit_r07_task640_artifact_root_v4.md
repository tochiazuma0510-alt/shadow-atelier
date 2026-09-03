# Sol(max) Task660: final path-only release audit of Task640 workflow v4

## Verdict

`PASS_PATH_ONLY`

`SAFE_TO_DISPATCH_GHA=yes`

The Task658 path repair is exact and its sole blocker, the missing inert line,
is closed.  This authorizes only one replacement Task640 run.  No Python
mathematics, production run, GHA dispatch, implementation edit, or git
operation was performed.

## Frozen inputs

No `INPUT_MISMATCH` occurred.

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| released v3 workflow | 9,959 | 160 | `f0dabf6a9cef421f6849391fcb1b2e2f229333d90eab61fb61a0fe95dcdc8ac4` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml` | 10,038 | 161 | `3a91aca913faf79dadd0e16d181c6e270df660ead0b19acbd6045b2f7cfb92fb` |
| `sol/luna_reply_657_r07_task640_artifact_root_path_v4.md` | 1,179 | 24 | `daaf93cfa8b2f640b9176432aafeed02cce9b6e007538030f1a1c19a593035c7` |
| `sol/luna_reply_659_r07_task640_v4_inert_line_repair.md` | 811 | 17 | `8feedc8747e2e37a645b807751d6767b8f4376155a5bee6a26267ae7da477908` |

## Path and delta audit

The Task625 upload has exactly two roots: `task625-payload/` and
`task625-verdict.json`.  Downloading that artifact into `task625/` therefore
leaves the verdict at `$RUNNER_TEMP/task625/task625-verdict.json` and the
payload beneath `$RUNNER_TEMP/task625/task625-payload/`.

The v4 path census found exactly four uses of the nested payload root:

1. old checker `--payload` at line 125;
2. replayed-verdict destination at line 127;
3. producer `--task601` at line 136;
4. new checker `--task601` at line 140.

The root verdict occurs exactly twice, in the line-123 existence test and the
line-127 byte comparison.  It was not moved beneath the payload directory.

An in-memory normalization changed the two workflow identity/self-path
labels, one fire label, one authentication label, two output labels, removed
the single inert line, and mapped exactly four nested payload roots back to
the old root.  The result was byte-for-byte identical to the released v3
workflow.  There was no residual semantic delta.

## Static release gates

- PyYAML safe loading passed and produced the single `fresh-endpoint` job.
- The folded job condition begins with literal `false &&`; consequently both
  the manual-dispatch and fire-marker branches are inert.
- All seven `uses:` entries retain their exact action identities and full
  40-hex commit pins.
- Code, checker, Task640 reply, prebuild, Task625 producer/checker, paper and
  audit hashes are unchanged; the four workflow environment hashes were also
  recomputed against their local files and matched.
- Task625 run/attempt/head/job/workflow/artifact gates, all three downloads,
  120-minute job timeout, two 45-minute process timeouts, 8 GiB virtual-memory
  limit, and seconds/RSS/durable/path/trie/state/record caps are unchanged.
- The residual upload remains guarded by `${{ success() }}`; logs remain
  guarded by `${{ always() }}`.

## Claim boundary

This path-only PASS proves no rho2 value or downstream mathematical claim,
including grade-two MEMBER/NONMEMBER, A0, a compatible cofinal lift, fake,
Ihara, cross-check, or Lean verification.

`verified=false`
