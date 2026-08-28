# Luna task 194b — R07 sharded boundary v3 release/resume repair

Date: 2026-08-28

Role: mechanical repair only.  Do not run Python, Node, GAP, git, GHA, or
network.  Read AGENTS.md, the complete task194 instruction/reply, all five
task194 files, task191 v2 source/checker/driver/reply, and the independent Sol
audit quoted below.  Modify only the existing five task194 files and this
designated reply:

```text
search/d972_r07_u0v0_boundary_preimage_sharded_v3.py
crosscheck/check_d972_r07_u0v0_boundary_preimage_sharded_v3.py
search/d972_r07_u0v0_boundary_preimage_sharded_gha_driver_v3.g
search/certs/d972_r07_u0v0_boundary_preimage_sharded_selftest_v3_20260828.json
sol/luna_reply_194_r07_u0v0_intragha_sharded_boundary_v3.md
```

Do not edit a workflow or predecessor.  Preserve the exact task191
mathematical space and causal serial echelon.  Report exact final identities;
claim only static readiness pending a new independent audit and GHA SELFTEST.

## 1. Independent STOP to repair in full

Current identities are producer
`72922/448b140bda4fb469384a9b2eff7641359adfa770f0af22e2b1345d710536849b`,
checker
`103998/c68966550b4e32fc2dde3f5a1766dc0f57503d18e03092f70d3e38bed22f5525`,
fixture
`1008/396b0d2b1a2eef48c714067977e5bc443897a853abe9d46e0e0a9b2a42498f88`,
driver
`8408/cdc9a01af03dd7b9191d14b925cd54002a6a64777bf339125d146c5f6326f248`,
and reply
`10678/389ed2478633553291de548e4fa511234d580260303cf8e975876ea7cdf56628`.
The driver `D194Current` and reply still carry older producer/checker/fixture
pins, so both modes stop before execution.  Refresh every transitive current
pin only after all repairs.  The fixture/source registry has 25 mutations,
not the reply's old 24.

The SELFTEST mathematical projection removes `sharding` at the wrong level.
It must remove `batch["correlation"]["sharding"]`, and also normalize the
separately serialized
`targets[*].terminal_dual.full_correlation.sharding`; do not rely on Python
object aliasing after JSON serialization.  `active_count` must read
`receipt["correlations"][0]["correlation"]["active"]`.  The checker
`normalize_v2_toy` must normalize the terminal-dual full correlation to the
serial v2 form before invoking the independent v2 checker.  Workers 1/2/4
must then compare the same mathematical transcript after removing only
schedule/performance metadata.

Worker manifests currently seal fixed zero elapsed/RSS values and the checker
requires zero.  Measure child elapsed time and child peak RSS in each worker,
seal finite nonnegative values, and independently validate their binding.
Compute each worker rate from its own measured time.  Measure the parent
serial ACTIVE/echelon suffix rather than recording
`serial_echelon_wall_seconds=0`.  Timing is metadata and may differ between
producer/checker; mathematical schedule equality must explicitly exclude it.

Resource phases are currently stored as attributes without being passed to
the global meter check.  Make every runtime reconstruction, target build,
resume replay, fork correlation, merge, ACTIVE/echelon, checkpoint, and final
serialization check phase-aware.  While children are live, sample aggregate
parent+child RSS before any nested v2 budget check can rewrite the terminal;
freeze the actual live sample and reap every child on all exits.  A v2 wall
stop must not be relabelled using parent-only RSS after reap.  Resume
seal/schema/queue failures are typed `UNKNOWN_INPUT` through the registered
InputStop path.  Check `fork` availability once at production-solve start,
even if a resumed serial suffix reaches a terminal before spawning a new
pool.

Retain the already-GO core unchanged: exact task191 space, source ordinals,
global pair ordinals, residue shards, literal `t=g*h^-1` and `t*h=g`, mod-3
merge before zero deletion, canonical ACTIVE order, independently rebuilt
contiguous checker intervals, serial pivot/ancestry order, full pending suffix
completion, and the `u0` then `v0` unresolved queue.

## 2. Load-bearing v2 checkpoint compatibility question

The concrete parent artifact from task191 run `33109346940` is:

```text
schema: d972-r07-u0v0-boundary-preimage-batch/v2/checkpoint
bytes: 84,914,159
sha256: 14854c3b2476641cdab62d86dfeae34aab8b1091f4664e5d6562c57d08362c57
retained columns: 13,360
boundary pairs: 17,564
oracle rounds: 2,291
```

Do not call this a v3 checkpoint.  Audit the actual `_preflight_resume` and
v2 loader types before editing.  If the existing v3 code cannot directly
accept this v2 schema and its correlations lack v3 shard certificates, choose
one of only two sound outcomes:

1. implement an explicit typed legacy-v2-prefix import which authenticates
   the exact v2 schema/seal/input pins, replays the whole retained serial
   transcript from rank zero using task191's independent semantics, labels
   old correlations as authenticated serial-v2 records (never fabricated
   shard records), and emits a new v3 checkpoint whose checker understands
   the mixed historical schedule; or
2. leave v2 import rejected and state exactly that task194 must restart from
   zero, while a separate converter/resume task is required.

Do not silently rewrite the schema or synthesize worker manifests for work
which was performed serially.  Because the 84.9 MB input is not currently in
the repository, implement no production-path assumption about its path or
compression unless a complete guarded ABI can be checked without adding a
sixth file.  The parent will stage an accepted input only after independent
audit.

## 3. Controls and report

Extend the distinct destructive controls to cover nested correlation
normalization, terminal-dual normalization, active-count location, nonzero
worker elapsed/RSS tampering, per-worker rate binding, serial-echelontime,
phase labels, live child RSS, child reap, fork availability, typed resume
failure, and (if implemented) every legacy-v2-prefix schema/seal/transcript/
schedule distinction.  Both producer and independent checker registries and
the fixture must match exactly.

The driver remains one producer process followed by one checker process; its
four workers live only inside each process.  Preserve fresh outputs,
exact-one markers, exact terminal equality, guarded relative resume input,
and nonempty mode sentinel.  End the reply with separate lines for static
repair, SELFTEST, v2 checkpoint direct compatibility, production boundary
decision, cofinal lift, fake, and Ihara.
