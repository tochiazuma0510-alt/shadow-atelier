# 157eg Luna reply — E4 full-D2 dual correlation

## Status

`READY_FOR_GHA_SELFTEST`

The four authorized files are implemented.  No GAP production run, full
mathematical run, Git operation, or GHA dispatch was performed.  The first
authorized combined lightweight self-test stopped in the producer fixture on
`RuntimeError: local section blob width`; checker execution was consequently
not started.  This was a fixture-only type mismatch: its value was a bare
permutation while the production API requires `Element=(perm_tuple, pc_tuple)`.
The fixture was corrected in both producer and checker.  The exactly-once
corrective combined self-test then passed: both processes exited zero, both
markers occurred exactly once, and all P/C/D hashes were unchanged.  This is
READY for the separate GHA self-test; it is not a cross-checked mathematical
terminal.

Canonical task: `sol/luna_task_157eg_b345_full_d2_dual_correlation.md`,
SHA-256 `22b649c178ea1a821a5d67973b39c58f6a7395b6bc6a407a36a493f9ce19720e`,
16187 bytes.

## Static frozen files

| file | SHA-256 | bytes |
|---|---|---:|
| `search/d972_b345_full_d2_dual_correlation_v1.py` | `6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52` | 78832 |
| `search/check_d972_b345_full_d2_dual_correlation_v1.py` | `311dc9413012542e489c9b2b7cd38e6008b81b6b8854e5e49d8d56285a457358` | 66571 |
| `search/d972_b345_full_d2_dual_correlation_gha_driver_v1.g` | `c0a0626f4ea15616bfef3b5916740c23c86a0f87760a98b0ff3d8da923db65b4` | 11980 |

The reply SHA/byte count is reported out of band because embedding its own
digest would be self-referential.

## Implemented exact lane

The producer authenticates the frozen 157ed source, reconstructs the pinned
E4 prefix and reverse-pivot functional afresh, independently reconstructs the
76 ordered base-column occurrences through the actual private helper shape,
and checks its public projection.  The hot loop is only the same-component
`lambda support × 76 occurrences` correlation.  It computes
`t = g*h^-1` using uncached E4 operations, does not intern pool elements, does
not materialize sparse vectors, and does not enumerate E4.  Contributions are
fully accumulated before zero deletion and before choosing the canonical
first ACTIVE row.

For ACTIVE, the section witness uses a fresh target-6 Fox replay and the
registered sparse section oracle.  The new lane owns the reachable typed-DAG
materializer, uses `inv_word`, enforces the section-word cap as a registered
RESOURCE result, and directly replays canonical E4 values.  It never calls the
frozen predecessor's defective `SectionExpressionDAG.materialize`.  The
monitor implements both `check` and `reserve`; old/157ed `ResourceStop` values
are converted only after exact cap/reason validation and are normalized to the
committed outer phase.

The checker imports neither producer data structures nor producer helpers. It
rebuilds E4, the 32768+207 prefix schedule, reverse lambda, 76 base
occurrences, complete base-major correlation, canaries, terminal, and ACTIVE
section recovery independently.  Persistent pool/basis/DAG/section state is
reconstructed and compared to an exact inner snapshot; correlation probes do
not alter it.  Its shared production witness core decodes the packed typed DAG
and replays IDENTITY, FLAT, INVERSE, and PRODUCT nodes with canonical-value,
parent, role, and direct-word bindings.

Local and pinned-upstream resource registries are disjointly typed by
`cap_source`; they are never merged by dictionary precedence.  In particular,
the local 268435456-byte receipt cap cannot be confused with the predecessor's
unreachable 16777216-byte receipt cap.  The closed reachable upstream registry
is exactly the pinned 157ed `UPSTREAM_RESOURCE_CAPS` plus
`raw_lambda_recursion_edges`.  The common deadline and producer RSS caps remain
local only because this lane passes its own monitor to every reachable imported
hot path.  The producer derives that registry from the pinned producer; the
checker reconstructs it independently from the pinned 157ed checker and
requires exact registry/digest equality.  Mutations that relabel either local
deadline/RSS cap as upstream are rejected.  Fixed provenance and
numeric/stage-aware wall, RSS, phase-timing, and receipt-byte ledgers are also
exact-gated.

The checker propagates its single absolute deadline into both imported hot-loop
systems: the 157ed checker receives a Deadline adapter with the same absolute
end, and the seedspan checker receives the corresponding back-dated 18000s
origin.  Neither imported module can reset or extend the remaining budget.

The only normal terminals are the pinned-E4 separator and first ACTIVE
translation.  RESOURCE and INPUT are exact fail-closed terminals.  No result
is promoted to alternate roofs, full H3, global no-lift, B4-A, or B4-B.

## Driver contract

The ASCII-only driver pins the final producer/checker/task and all named
predecessors, removes stale output, regenerates q3 in an isolated GAP child,
runs the independent q3 checker, uses `bash -o pipefail` plus `tee`, requires
each producer/checker marker exactly once, and shares one 18000-second budget
between producer and checker.  Its two modes are mutually exclusive.  GHA
self-test must pass at the exact commit before full dispatch.

## Mandatory recurrent-failure guard

1. **Frozen snapshot — PASS.** All ten task/predecessor SHA+byte pins were
   re-read from disk at static freeze; the q3 producer/checker/driver SHA pins
   were also bound in the driver.  No predecessor was modified.
2. **Actual data shape — PASS.** `build_instrumented_prefix` is consumed as
   private `model4,pool,sections` plus public `directed_base_support`.
   `freeze_base_support_occurrences` is called explicitly, canonical root reuse
   is required, public/private exact keysets are checked, and no nonexistent
   `base_occurrences` projection is read.
3. **Production-path self-test — PASS.** The fixture is wired to
   the production correlation, terminal/schema, producer serializer/owned
   materializer, and checker packed decoder/witness core.  ACTIVE, separator,
   cancellation, three orientation mutations, IDENTITY/FLAT/INVERSE/PRODUCT,
   inverse parent/opcode/value/role, RESOURCE, INPUT injection, and state-inner
   mutations, local/upstream cap collisions, local deadline/RSS upstream
   masquerading, predecessor hard-equality cap masquerading,
   provenance/performance drift, inherited-deadline extension, and the actual
   production writer's serialization overflow/finalizer/rewrite/readback path
   are registered.  The latter uses a bounded system-temp file and injected
   local cap, then requires canonical final bytes and the exact RESOURCE
   terminal.  The initial run exposed and rejected the fixture's bare
   permutation value before any checker run.  P/C now both use the production
   `(perm_tuple, ())` Element shape, gate `degree=3`, `pc.n=0`, blob width 3,
   and reject a bare-tuple mutation.  The corrective combined run passed with
   producer/checker exits 0, exact-once markers 1/1, and unchanged P/C/D SHA.
4. **Producer/checker state order — PASS (static).** Producer snapshots exact
   pool order, IDs, basis, DAG, and section counts around correlation.  Checker
   reconstructs the same state independently and exact-compares the inner
   record.  The correlation helper has no pool/basis/DAG/section parameter and
   uses no intern/cache path.
5. **RESOURCE contract — PASS (static).** P/C share exact stage-aware terminal
   tables, separately typed closed local/upstream cap registries, reason=cap
   key, exact limit, observed/comparator, current coordinate, atomic partial
   layout, and later-field emptiness.  Serializer RSS reservation and old
   ResourceStop conversion are covered; cap-source collision, local-only
   deadline/RSS upstream masquerade, cap/phase/reason/stale-limit,
   hard-equality masquerade, and honest receipt-serialization mutations are
   registered.  The same production `write_with_resource_fallback` entry is
   called by `main` and by the bounded serialization fixture.
6. **Driver/pins — PASS (static).** Final P/C/task pins, q3/predecessor pins,
   fixed paths, stale-output removal, exact-one markers, pipefail/tee, isolated
   q3 child, and shared remaining deadline are present.  No placeholder remains.
7. **Performance — PASS (static).** Immutable inverses/support are outside the
   pair loop; the pair loop is support×76 with cadence 4096.  There is no pool
   intern, full sparse materialization, E4 enumeration, or unbounded cache.
   The checker bridges the same absolute remaining deadline into both imported
   hot-loop modules. Expected same-job cost remains prefix-dominated, about 12–22 minutes and
   0.8–1.4 GiB RSS.
8. **Claim boundary — PASS.** Producer-only is explicitly not cross-checked;
   the separator is limited to the pinned E4 roof and 157ee joint kernel;
   ACTIVE is only a translated-boundary diagnostic; UNKNOWN makes no
   mathematical obstruction claim.

## Static audit record

- Python AST parse: PASS for producer and checker.
- Driver ASCII scan: PASS.
- Task/predecessor SHA+byte audit: PASS, 10/10.
- Combined self-test attempt 1: **FAIL / STOP** in producer fixture at
  `local section blob width`; producer exit 1, checker not started, markers
  0/0.  Log:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-157eg-combined-selftest-3d5118d6e277491ca8fa78acd9d2b6bf.log`.
- Corrective combined self-test: **PASS**; producer exit 0, checker exit 0,
  producer/checker marker counts 1/1, and P/C/D SHA unchanged before/after.
  Log:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-157eg-corrective-combined-selftest-d9420e553ed14206a723ea183cef5646.log`.
- Full GAP/Python mathematics: NOT RUN.
- Git/GHA: NOT RUN.
