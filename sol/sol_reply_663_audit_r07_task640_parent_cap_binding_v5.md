# Sol(max) Task663: cap-only audit of Task640 workflow v5

## Verdict

`PASS_CAP_ONLY`

`SAFE_TO_DISPATCH_GHA=yes`

The exact v5 workflow repairs the observed parent `manifest_binding` failure
by adding the one missing accepted-parent cap.  After normalizing mechanical
v4/v5 labels and the inert guard, that cap line is the sole semantic delta.
No production computation, Python mathematics, GHA dispatch, implementation
edit, or git operation was performed.

`verified=false`

## Frozen inputs

No `INPUT_MISMATCH` occurred.

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| released `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v4.yml` | 10,023 | 160 | `c8deb31cf87554500d665ab6a9740af0529204858d5ec30a91be5b55735dac58` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v5.yml` | 10,076 | 162 | `88f5169806ae83202aadbdba0c3505bf754cccc61131064d373a4e65946c664e` |
| `sol/luna_reply_662_r07_task640_parent_cap_binding_v5.md` | 951 | 22 | `a8f5593939fbb05b4a06c052922ffa123ce2ece7ff7e59549fb628beec7b8015` |

I read the complete Task662 mail and reply before auditing the frozen files.

## Cap binding

The accepted Task625 v3 workflow
`.github/workflows/d972-r07-a0-grade1-selected-slp-v3.yml` line 22 sets

`TASK625_ACCUMULATED_CAP: "50000000"`.

The pinned old checker
`search/check_d972_r07_a0_grade1_selected_slp_v2.py` has SHA-256
`8c3dd039368f63d62ef79694a196f73d0b626134df39673c5e48c98c7c8787f9`.
Its `checker_staged_caps()` at lines 1022--1038 reads precisely
`TASK625_ACCUMULATED_CAP` into `caps["accumulated_states"]`; lines 2136--2144
copy that value into the expected `manifest.resource_caps`, and lines
2147--2161 reject unequal resource caps as `manifest_binding`.

Without the environment key, checker line 1025 falls back through
`DEFAULT_ACCUMULATED_CAP`, fixed at line 49 as 2,000,000.  The accepted replay
receipt independently records 2,605,954 cumulative insertions, so that default
is both different from the manifest's declared 50,000,000 cap and below the
actual accumulated count.

V5 line 27 adds exactly

`TASK625_ACCUMULATED_CAP: "50000000"`.

The other five values used by `checker_staged_caps()` already have defaults
equal to the accepted workflow: 2,000,000 interned paths, path length 4,096,
7,516,192,768 durable bytes, 2,400 seconds, and 7,516,192,768 RSS bytes.
Therefore the one added key reconstructs the complete accepted
`resource_caps`; no further environment change is required.

## Exact v4/v5 delta

The raw diff contains only:

- workflow name and self-path v4-to-v5 changes;
- the cap line at v5 line 27;
- the inert `false &&` at line 41 and mechanical v5 fire marker;
- authentication-step and two output-artifact label changes from v4 to v5.

Deleting the cap line and inert guard in memory and reversing those mechanical
v5 labels makes v5 byte-identical to released v4.  Thus the cap is the sole
nonmechanical semantic delta.  The v5 job is inert: `false &&` occurs exactly
once in its job condition.

## Unchanged release surface

Bounded static checks passed:

- PyYAML safe parsing of released v4 and inert v5;
- all seven `uses:` entries are pinned to full 40-hex action SHAs;
- all eleven locally checkable producer, checker, arithmetic, proof, audit,
  and reply file hashes match the workflow pins;
- exact Task625 run/attempt/job/head/workflow/artifact metadata and digest
  checks are unchanged;
- all three download definitions are unchanged;
- the four nested `$RUNNER_TEMP/task625/task625-payload` consumers remain at
  v5 lines 127, 129, 138, and 142;
- the uploaded Task625 verdict remains at the download root, tested at line
  124 and byte-compared at line 128;
- all Task640 time, memory, durable, path, trie, state, and record limits are
  unchanged;
- the residual upload remains guarded by `${{ success() }}` and the log upload
  remains `${{ always() }}`.

## Authorization and claim boundary

This PASS authorizes only removal of the audited inert guard and one
replacement Task640 workflow run.  It establishes no rho2 value, grade-two
MEMBER/NONMEMBER result, A0, full-Q0/order-54,432 result, compatible cofinal
lift, fake, Ihara, cross-check, or Lean verification.
