# Sol Task844 — narrow hostile re-audit of reached P1 nonpromotion boundary

## Ruling

**PASS; SAFE_TO_DISPATCH_GHA=yes.**  The sole Task838 blocker is closed.
Producer-v10 routes both production success and the production
`except (ResourceStop, KeyboardInterrupt)` terminal through the same
`_promotion_boundary`.  The committed bounded fixture reaches both branches:
its resource branch writes real post-checkpoint orphan bytes, rolls them back
inside that shared helper, re-authenticates the durable prefix, propagates the
identical terminal object, and leaves the actual requested output absent;
its success branch really promotes a staging tree through the same helper.

I read the complete Task838 ruling, Task842 commission and implementation
reply, producer-v10, workflow-v9, and the immediate producer-v9/workflow-v8
predecessors needed for exact comparison.  I did not edit implementation,
run the 8,059-row calculation, dispatch GHA, use git, or request unrelated
hardening.

## 1. Shared production boundary

`build` has exactly two calls to `_promotion_boundary`.

1. The caught `ResourceStop` or `KeyboardInterrupt` object is passed as
   `terminal` together with the live cache, instruction sink, and
   `last_checkpoint`.  The helper's terminal branch requires that no manifest
   was supplied, calls `_rollback_prefix`, and then executes `raise terminal`.
   This branch contains no checkpoint `unlink`, manifest `write_bytes`, or
   `os.replace`, and it does not dereference or mutate the requested output.
2. After all terminal receipts and false-claim manifest fields are assembled,
   the success tail passes that manifest to the same helper.  This branch
   performs the former three operations without semantic change: checkpoint
   unlink inside staging, canonical manifest write, and atomic staging-to-out
   replacement.

Thus a resource terminal cannot fall through into final receipts or
promotion, while the success path cannot pass without actual promotion.

## 2. Reached permanent fixtures

`fixture_reached_promotion_boundary` is nonvacuous.

- It creates a fresh `requested_out` and asserts its initial absence.
- `_tiny_stage` publishes an authenticated cursor-4 checkpoint.
- `resume_prefix` opens that exact prefix, after which two new cache rows and
  two instruction records are written without publishing another checkpoint.
- The fixture constructs a real `ResourceStop` object and passes it, the same
  requested output, both live streams, and the cursor-4 sidecar state to the
  same `_promotion_boundary` called by production.
- The caught exception must satisfy `caught is terminal`.  After closing the
  streams, `resume_prefix` authenticates the retained files against the
  original sidecar and returns the original cursor 4.  The staging tree and
  checkpoint remain, while the actual `requested_out` is absent.

The second fixture branch creates a distinct staging directory containing a
checkpoint and payload, calls the same helper with a manifest, and requires
the output directory to exist, the staging path and checkpoint to be absent,
the payload to survive, and the output manifest to equal the canonical input
manifest bytes.  A helper that only propagates terminals and never promotes
cannot pass this fixture.

The bounded selftest exited 0 with
`promotion_fixture_accept=2`, `promotion_fixture_rejections=0`,
`resume_fixture_accept=12`, `resume_fixture_rejections=12`,
`cross_runner_fixture_accept=3`, `cross_runner_fixture_rejections=1`,
`actual_replay=DEFERRED_TO_GHA`, and `verified=false`.

## 3. Frozen mathematics and claim boundary

The producer-v9 to producer-v10 no-index diff is confined to the factored
helper, its two production call sites, the reached fixture, and selftest
reporting: 125 insertions and 16 deletions.  Independent normalized checks
gave:

- both character row-building loops AST-identical;
- the complete source segment from the first old-character loop through the
  last new-character loop byte-identical, SHA-256
  `0bb5ebffc92b6fe0a0a6d2a808af5e75c470ad507f200823c4759ea502f41d18`;
- 32 frozen assignments identical, including all seven immutable source
  hashes, source/checker ancestry, `OLD_RANKS`, `NEW_RANKS`, `ORDER`, origin
  ranges, character/actor/monomial orders, widths, `ROWS=8059`, checkpoint
  schema/status/cadence and file roster;
- `_checkpoint_pins` AST-identical;
- the final `manifest` assignment AST-identical; and
- `FALSE_CLAIMS` AST-identical, with A0, COMMON, COFINAL, FAKE, IHARA and
  `verified` all false.

The final candidate schema remains
`d972.r07.canonical-p1-dag-degree2-lift.v8`, and the checkpoint schema remains
`d972.r07.canonical-p1-dag-degree2-lift.checkpoint.v8`.  No P1 search-universe
or mathematical row-order change occurred.

Exact producer identities were independently measured:

| file | SHA-256 | bytes | LF |
|---|---|---:|---:|
| producer-v9 | `c05149e41e62b4aa78b483c61fb03570228ba7697d95d3cd10848758b8735ed9` | 149350 | 3164 |
| producer-v10 | `af99dbb399a0f98ab70e240498fb7b934ce8e0af93e4930cd1dbd549177f750f` | 154825 | 3273 |

## 4. Preserved release gates and bounded checks

Workflow-v9 differs from workflow-v8 by only 9 insertions / 9 deletions for
the producer identity and version labels.  The previously-passed gates remain
intact:

- the launch wrapper is still excluded from `raw_file_pins`, all other
  normalized immutable records remain path-independently sorted, and the
  full semantic `launch_input_identity` remains bound;
- the checkout producer is compared to literal SHA-256
  `af99dbb399a0f98ab70e240498fb7b934ce8e0af93e4930cd1dbd549177f750f`,
  bytes `154825`, and LF `3273`; independent measurement matched all three,
  and the authentication run scalar contains no `GITHUB_ENV` self-authority
  write;
- the checkpoint-staging heredoc body and delimiter remain at column zero in
  the parsed scalar, the `if` remains closed, and the step remains `always()`;
  and
- the prior boundary, mutation, rollback and cross-runner fixtures are still
  called and pass.

| bounded check | result |
|---|---|
| external-output `py_compile` producer-v10 | PASS, 0.307 s |
| producer-v10 `--selftest` | PASS, exit 0, 1.736 s |
| YAML BaseLoader | PASS; one job, 22 steps |
| every extracted workflow `run:` scalar under Git Bash `bash -n` | PASS, 10/10 |
| all extracted Python heredocs AST parse | PASS, 6/6 |
| fixed producer SHA/bytes/LF comparison | PASS, 3/3 |
| exact source/AST comparisons above | PASS |

This authorizes dispatch of the candidate-producing GHA workflow; it does not
promote any mathematical claim.  No actual P1 cache was produced or
cross-checked here, and this audit makes no grade-two, A0, COMMON,
cofinal-lift, fake, Ihara, or Lean-verified claim.

PASS
SAFE_TO_DISPATCH_GHA=yes
