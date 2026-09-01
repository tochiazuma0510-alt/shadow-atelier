# Luna Task490 — rank-99 durable discovery v4

Result: bounded Task490 D1–D6 repair **PASS**.  v3 remains untouched; the
Task487 rank-99/CROSS-CHECKED premise, v424 order, v426 rolling chain, and
v427 short-batch path are preserved.

Authorized outputs and final pins:

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py` | 98576 | `5b8f3ae76abb64768decb14be50fbd6d75b5e84aeaad2b1a63fcb544933cf36f` |
| `crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v4.py` | 66212 | `cd0acf346d4f133dfaa8e047db6593511a5423c6a166060a37fc313504e928e7` |
| `search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v4.g` | 9424 | `948f6254298eef51d524e834441c530ecb1a5a3a5cbefbdfe3dac9e7922d0ff8` |

Binding pin: `d5777bc12023298808fa7f0637de47e072af0bf8137c7922ce4c0cd17c7327be`.

Bounded gates:

- Producer `--mode FIXTURE`: PASS, including v4 three-argument replay ABI,
  one retained-candidate helper, 1/15/16-row flushes, post-batch COMMON
  profile with `dual_digest=None`, aggregate/rollback boundaries, identity and
  prior-seal mutations, base hard-fallback→own-schema BOOTSTRAP resume, base
  first close, own CLOSED first close, and exact one update per batch.
- Checker `--self-test`: PASS, including producer-marker binding, old
  checker-marker rejection, immediate predecessor content/READY seal,
  same-count/different-prefix rejection, aggregate rises 17, and the three
  resource false-rejection shapes.
- AST: PASS; all real adjoint calls are three-argument
  `v4.tau_free_adjoint(P,m,args)`, and `run` uses the retained-candidate
  helper.  Python checks used `-B`.
- Generated driver shell: `bash -n` PASS (Git Bash, generated in `%TEMP%`).
  GAP `ReadAsFunction` parse: exit 0 (only normal unbound-global warnings).
- Driver margins are `14040 < 14220 < 14400` and
  `4200000000 < 4500000000 < 5120000000`.  RESOURCE writes the distinct
  resource terminal and skips checker; only checker-approved COMMON writes the
  global COMPLETE marker.

The v427 soft-deadline branch uses the production `flush_rows` path; its final
local batch is bounded to 1–16 while `segment_rises` remains the invocation
aggregate.  The Windows symlink fixture was privilege-limited
(`symlink_platform_limited=true`, `symlink_escape_rejected=false`); the
production path guard remains strict.  No production/GHA run, git operation,
authority replay, persistent cache, or bytecode cache was used.

TASK490_R07_RANK99_DURABLE_DISCOVERY_V4_PASS
