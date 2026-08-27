# Luna reply 190 - R07 exact column-generation speed audit

Date: 2026-08-27
Role: bounded mechanical static audit only.  No Python, Node, GAP, Git,
GHA, or network was run, and no search, crosscheck, workflow, certificate,
or proof file was changed.  The live jobs were not touched.

## 1. Objective and scope

The audited live contexts are task186 run `33075481377` and task187 run
`33075593185`, both at head
`257d01e154f020901d24b96599da5a9602e58913`.  These run identifiers are
context only; no timing or completion result is inferred from absent logs.

Notation used below is `N=6441` roster words, `Q=1469664` Q0 states,
`Gamma=243`, `Delta=Q*Gamma=357128352`, `R=15` base PB3/PB4 rows, `B` the
total number of typed occurrences in those rows, `s` the nonzero typed-row
support of a current dual, `O=11` Fox occurrence slots, `r` the retained
column rank, `m` a representative sparse-row width, and `K_i` the registered
kernel orders `(9,9,9,9,9,1,1,1,3,3)`.  `W` is the weighted sum over the
distinct formula targets and `C=min(W+1,Delta)` (with the registered full
fallback boundary retained).

The audit preserves all `t*h=g` translations, all contributors and
coefficient ancestry, literal direct/all-seven replay, helper separation,
and typed `UNKNOWN_RESOURCE`.  A cache is admissible only as a deterministic
memo of authenticated values; it cannot alter the finite set being scanned.

## 2. Read set and exact identities

All requested task documents, replies, implementations, and both
corresponding GHA drivers were read in full.  The identities below are the
read-only bytes observed in the working tree.

| file | bytes | SHA-256 |
|---|---:|---|
| `sol/luna_task_186_r07_normalized_exact_common_word_colgen_v2.md` | 6093 | `aaae31643bdb0e25171e7a8dfef49b4a008e3b08a175c2e1337a5c11f13a3645` |
| `sol/luna_reply_186_r07_normalized_exact_common_word_colgen_v2.md` | 11868 | `31325a2845e1e51f6535aae3c0a9942b11c2fb553a1bb4cb0c1eff88dab4fdeb` |
| `sol/luna_task_187_r07_u0v0_boundary_preimage_v1.md` | 6338 | `e5011690c96b7ad7b1cba978ff06085257978dde8eb40a22c74ad892aa53f4a7` |
| `sol/luna_reply_187_r07_u0v0_boundary_preimage_v1.md` | 12009 | `7630da1422d94c45b6c1d079aec0747ad3c37c207b0a35bfc19ce6746aae8926` |
| `search/d972_r07_normalized_exact_common_word_colgen_v2.py` | 63053 | `ec73db0a474b3b52d69e19862e8185ae22423b2406f3922b5669d9a4e85fafab` |
| `crosscheck/check_d972_r07_normalized_exact_common_word_colgen_v2.py` | 54982 | `8898798d0d6a9e0b6cd67402e74ba0dc5048b4797a0f7a9657e58d70d553c488` |
| `search/d972_r07_u0v0_boundary_preimage_v1.py` | 35173 | `18040f4f73fe963632bbd2200e730818a7354c5963143a5871e73b2d1284dbfe` |
| `crosscheck/check_d972_r07_u0v0_boundary_preimage_v1.py` | 32825 | `e94d19311d0afe23fde869045f959490528d18e0f3537209e57b7cbefb452b18` |
| `search/d972_r07_normalized_exact_common_word_colgen_gha_driver_v2.g` | 9630 | `a1c0fc034b127174e5c5795347648db0629314262b9e59689705e887371a7e4e` |
| `search/d972_r07_u0v0_boundary_preimage_gha_driver_v1.g` | 7721 | `16d354d387db53cfadd22a7442f9a7aa77580c8410664f9dd5b1a618fef026b8` |

The task186/task187 implementations pin the task179 producer/checker,
driver, fixture, and governing arithmetic papers internally.  Those pins
were inspected as provenance but are not modified by this audit.

## 3. Static call graph, cost ledger, and proposals

### 3.1 Current call graph and repeated work

Task186 follows
`main -> run_full_v1_successor -> authenticated task179 main ->
PositiveSearch`.  The v1 path is `build_runtime` (producer lines 454-580),
`AllSevenModel` (639-829), `FibreOracle` (844-1092), and
`PositiveSearch.run` (1683-1719).  A rank increase goes through
`add_column` (1453-1489), which changes the dual and resets weighted progress;
the v2 wrapper then runs `attach_v2_positive` (530-698), including a fresh
rank/ancestry/direct replay.  A v2 resume is deliberately rebuilt from zero
by `rank_zero_resume_checkpoint` (700-826).  The independent checker first
runs the pinned helper in `full_independent_production` (838-993), then runs
the v2 receipt/rank/ancestry checks in `check_production` (581-823).

Task187 follows `solve` (396-486): one full task179 runtime, two direct
u0/v0 target replays, then a shared boundary `Echelon` and an unresolved
target loop.  Each unresolved target performs `reduce`, `dual`, and
`full_boundary_correlation` (289-331); an active row is materialized by
`boundary_column` (361-364) and appended.  Its independent checker repeats
runtime/target/direct reconstruction and per-column correlation in
`validate_production` (198-292).  The task187 implementation has no durable
production checkpoint writer; a resource stop therefore has no partial
correlation state to resume.

The load-bearing products are:

| phase and exact regions | current cost and repeated values |
|---|---|
| Runtime: task179 `build_runtime` 454-580; task176 `enumerate_q0_sections` 775-827, `scan_memberships` 856-872, `prove_L` 939-976, `family_public_A` 999-1014 | Q0 discovery performs `2*10*Q` transition/store updates and retains ten fixed-width stores of `970*Q` raw bytes, plus Q0 IDs/parents. Membership scans are `11*Q`; family image validation includes pairwise closure in each image. The checker reconstructs its own runtime, so this cost occurs independently there. |
| Coarse/fibre: task179 `CoarseInverse.build` 871-887 and `FibreOracle.canonical` 945-988 | Each first-used coordinate builds a Q-entry open-address table and each target scans its `A_map` candidates. The ten uint32 tables account for `10*16777216` payload bytes. Existing caches cover canonical targets, kernel prefixes, and tables, but not all global candidates or all fixed word evaluations. |
| Kernel prefixes: `FibreOracle.ensure_kernel_prefix` 999-1022 and `verify_kernel_orders` 1024-1050 | For coordinate `i`, each explored edge invokes `coordinate_blobs`, which evaluates all ten coordinates even when only coordinate `i` is being tested: `O(10*sum_i K_i*g_i)` coordinate evaluations, where `g_i` is the word-generator count. |
| Boundary: task179 `boundary_oracle` 1123-1175; task187 `full_boundary_correlation` 289-331 and checker 168-197 | Per dual, the support build is `O(s)`. The exact correlation is `O(sum_{b,c} B_{b,c}*s_{b,c})`, worst `O(B*s)`, with typed decode, inverse/multiply, `t*h=g`, packing, accumulation, and contributor recording per pair. Task186 repeats this after every rank/dual epoch; task187 repeats it for each target after each rank increase. The expanded family itself has `B*Delta` translated rows, but neither implementation samples it. |
| Occurrence/formula: task179 `AllSevenModel.occurrence_data` 699-746, `occurrence_column` 755-776, `direct_column` 784-829; task186 `correction_oracle` 1535-1602 | For each rank epoch and roster row, occurrence construction is `O(sum_{j=1..O}|FoxGrad_j|*s)` plus group products. Thus the full pass is `O(N*O*g*s)` in the uniform case. Every nonzero candidate then calls direct all-seven replay and another eleven-slot occurrence replay. For `K=0`, fibre targets add `sum_i |A_i|` lookups and up to `sum K_i` kernel candidates; for `K!=0`, each row tests up to `C=min(W+1,Delta)` global candidates, each doing ten-coordinate products plus a ten-coordinate literal replay. |
| Echelon/dual: task179 `Echelon.add/reduce/exact_dual` 398-442 and `PositiveSearch.add_column` 1453-1489; task187 `Echelon` 195-243 and `solve` 424-472 | Adding a retained row is `O(r*m)` worst-case plus ancestry. The v1 add path then reduces the target, derives an exact dual (including another target reduction and reverse pivot solve), and writes a full checkpoint. Task187 reduces both targets and recomputes a dual/correlation serially after each rank increase. |
| Serialization: task179 `write_checkpoint` 1338-1387 and correction writes 1535-1602; task186 resume/positive postprocessing 530-826; task187 has no production checkpoint | Full JSON canonicalization, fsync, and replacement are repeated at row/candidate/fibre boundaries, with work proportional to the complete accumulated checkpoint `L`. Task186 postprocessing additionally re-ranks rows, recomputes ancestry, direct c-star/c-exact rows, and exactification; the checker performs its own complete helper and receipt replay. |

Values that do not depend on the current dual and are therefore repeated
unnecessarily after a rank increase include: the eleven substituted base
relations and Fox gradients for each roster word; fixed base hexagon and
pentagon gradients in `direct_column`; PB3/PB4 source element decodes and
inverses; q0 section words, Gamma coordinate rows, and ten-coordinate blobs
for a fixed `(qid,gid)`; and selected translated boundary rows already
identified by a prior correlation.  The changing dual itself, its support,
formula scalar, exact dual pairing, and rank-dependent echelon reduction are
not invariant and must be recomputed or incrementally updated with an
equivalent certificate.

### 3.2 Ranked proposals

The rankings are expected wall-time gain, not measured timings.  All costs
below retain the current worst-case finite scan unless explicitly marked as a
larger redesign.

1. **Immutable Fox and typed-value templates (highest safe gain; both sides,
   low/medium risk).**  Current cost is the `O(N*O*g*s)` occurrence pass plus
   three base-gradient and eleven occurrence-gradient constructions per
   accepted direct candidate.  Build a deterministic, lazy cache keyed by the
   authenticated runtime/input digest, roster word, and slot: substituted
   relation, signed factor, Fox gradient terms, prefix inverse, base inverses,
   and canonical typed blobs.  Cache the fixed base all-seven gradients and
   occurrence/direct pair so `direct_column` can still perform the same
   equality check without reconstructing them.  The dual-dependent join still
   scans every current support term, so the worst asymptotic remains
   `O(N*O*g*s)` per dual epoch, but repeated group/Fox work falls to the
   uncached support join; memo hits can reduce it to new support keys.

   A lazy bounded cache uses `O(H)` memory (or `O(N*O*g)` if materialized),
   instead of an unsafe all-support table.  Affected regions are task179
   `AllSevenModel.__init__/occurrence_data/occurrence_column/direct_column`
   639-829 and helper-checker `independent_formula/direct_correction`
   382-633, reached by task186 wrapper 828-935 and checker 838-993.  No
   producer cache is passed to the checker: each side builds its own cache
   and directly replays selected literals.  If cache metadata is serialized,
   add only a schema, input digest, canonical template digest, and bounded
   eviction record; literal rows remain mandatory.  Risk is stale/incomplete
   keys, mitigated by binding every key to the runtime and retaining the
   existing direct equality gates.

2. **Boundary source descriptors and lazy translated-row memo (high gain for
   task187, medium for task186; both sides, low risk).**  Current correlation
   is `O(B*s)` per dual with repeated source unpack/inverse and selected-row
   packing.  Precompute once per runtime the complete sorted descriptor list
   `(block,index,component,h_blob,h_inverse,base_coefficient)` and decode each
   dual support blob once per call.  Memoize an exact translated sparse row by
   `(block,index,translation_blob)` when it is selected or revisited.  The
   pair scan remains `O(B*s)` and all pairs/contributors remain present, but
   the inner loop becomes key arithmetic and accumulation rather than repeated
   source conversion.  A cache of `V` visited translations costs
   `O(B+V*m)` memory and can be bounded/evicted; an eviction only causes
   literal recomputation.

   Thus a complete family can be streamed once safely only as these immutable
   base-orbit descriptors (and lazily materialized exact translated rows).
   Expanding and storing all `B*Delta` translated rows would preserve coverage
   but costs `O(B*Delta)` records and is not a viable minimal speed patch.

   Affected regions are task179 `boundary_oracle/translated_boundary`
   1103-1175, task187 producer `full_boundary_correlation/boundary_column`
   289-364, and task187 checker `boundary_correlation` 168-197.  The receipt
   needs no trusted cache contents; optionally record a canonical descriptor
   digest and source-count total.  The independent checker regenerates its
   own descriptors and compares every contributor/row.  Risk is low because
   the cache is keyed by the full typed translation and cannot alter the
   active lexicographic selection.

3. **Section/coordinate candidate memo (medium-high gain; task186 producer
   and checker, low/medium risk).**  `FibreOracle.canonical` 945-988 and
   `kernel_candidate/global_candidate` 999-1091 repeatedly slice immutable
   q0 stores, rebuild Gamma rows, and call ten-coordinate `coordinate_blobs`.
   Keep the 243 Gamma rows and q0 section views/path words in a bounded
   deterministic chunk cache.  Validate each newly cached value once against
   the existing coordinate replay, then use the exact stored ten blobs for
   candidate pairing.  A candidate changes from roughly ten full word
   evaluations plus packing to ten packed products after a cache hit; the
   asymptotic per candidate stays `O(10)`.  Never materialize all `Delta`
   rows: that would cost `O(Delta*10)` records and roughly `970*Delta` raw
   bytes.

   Memory is `O(Gamma*10 + H*10)` for Gamma plus a bounded q0 chunk; the
   current Q0 stores remain.  Affected task186 wrapper/helper regions are
   `run_full_v1_successor` 828-935 and helper `full_independent_production`
   838-993, with task179 `FibreOracle` as the pinned schedule.  No receipt
   field should certify an unregenerated cache; selected candidates retain
   source words, section blobs, and direct replay, while the checker rebuilds
   its own cache.  Risk is medium if section IDs or parent conventions are
   mishandled; enforce the existing q0 parent/letter and ten-coordinate
   literal checks.

4. **Bounded checkpoint chunks and exact resume state (medium wall-time gain,
   very high timeout benefit; producer plus task187 redesign, medium risk).
   Current task186 performs full checkpoint writes after many fibres/candidate
   attempts and rank changes, approximately `O((F+C+r)*L)` bytes per dual
   epoch.  It also loses expensive in-flight work between writes.  Use a
   registered fixed chunk of at most 256 logical attempts, persist once at
   the chunk boundary, and repeat at most that chunk after interruption.
   Keep monitor counters exact; batching must not change any cap or terminal.

   For task186, a durable state must include `dual_sha256`, target/input
   digests, `canonical_row_cursor` only over complete rows, every prior row's
   formula digest/K/W/Delta/kernel orders, and the bounded
   `support_fibre_cursor`, `kernel_cursor`, `global_prefix`, `complete`,
   `chunk_start`, `chunk_end`, and attempt count.  A partial chunk keeps the
   cursor at its start; resume may repeat it but may never skip it.  The
   current weighted-state validator must run before sealing and after loading.

   Task187 currently has no checkpoint.  A v2 checkpoint should additionally
   retain the target label, basis columns/transitions, dual digest, complete
   support digest, correlation cursor `(block,index,source_occurrence,
   support_index)`, accumulated coefficients, sorted contributors, and pair
   count.  `complete=false` can never become `NONMEMBER_D`; only a full
   correlation may do so.  Checkpoint writes after a pair chunk lose at most
   256 pair attempts.  The checker independently replays the prefix/full
   correlation and compares literal accumulation, not just the checkpoint
   digest.

   The minimal version may retain a full sealed JSON snapshot but writes it
   once per chunk.  A larger version uses an append-only content-addressed
   chunk log and a sealed manifest, reducing write cost to `O(chunk)` while
   preserving all columns and ancestry.  Risk is cursor off-by-one or a
   stale dual; bind every state to the exact dual and reject incomplete rows.

5. **Incremental target reduction and dual snapshots (medium gain; both
   sides, medium/high risk).**  `Echelon.add` plus `add_column` currently
   performs repeated target reductions and exact-dual preparation; task187
   repeats this for two targets.  Keep a rank snapshot containing the current
   target remainders/coefficients and update it with the newly appended
   normalized row.  Run one reverse triangular dual solve per changed basis,
   and pass that exact snapshot into checkpoint serialization instead of
   reducing the target again.  This changes the repeated part from several
   `O(r*m)` passes to one `O(r*m)` dual solve plus `O(m+ancestry)` updates;
   the finite rank solve remains load-bearing.

   Affected regions are task179 `Echelon` 382-442 and `add_column`
   1453-1489, task187 `Echelon` 195-243 and `solve` 424-472, plus task186
   `attach_v2_positive` 530-690 and checker rank replay 581-775.  Add a
   canonical rank-snapshot/transition digest and have the checker recompute
   it from columns; do not accept a producer snapshot by hash alone.  Memory
   is at most the existing `O(r*m)` echelon plus one target snapshot.  Risk
   is higher because a missed coefficient update changes ancestry; retain a
   full final replay and fail closed on any mismatch.

6. **Deterministic GHA sharding (largest potential gain, larger redesign,
   high risk).**  Both current drivers are serial: task186 driver lines
   66-110 and task187 driver lines 50-89 run one producer then one checker.
   Safe shards are limited to work whose inputs are frozen within an epoch.
   Q0 coordinate-store shards may use contiguous qid ranges after the
   parent/letter discovery order is fixed; boundary correlation may use one
   shard per block/base-row range; formula/candidate shards may split only a
   frozen dual epoch.

   For qid shards, merge invariants are exact contiguous coverage of
   `[0,Q)`, no duplicate/missing state, parent/letter transition equality,
   typed widths, and equality of the canonical parent/letter/store digests.
   For boundary shards, merge by mod-3 addition of every key, concatenate
   and canonical-sort every contributor, require pair-count sum equality,
   `accumulated=nonzero`, and choose the same lexicographic active key.  For
   correction shards, merge the complete row results and choose the least
   `(roster_index,target_index,kernel_index/global_cursor)`; no shard may
   append to the shared echelon.  Rank transitions remain serial.

   A manifest would carry shard count/ranges, input/dual epoch digest,
   canonical shard digests, total pair/candidate counters, and merge digest.
   The checker must implement the partition and merge independently (or
   monolithically replay the same literal result); it may not import a
   producer shard/helper.  Per-worker memory falls to a range/chunk, with a
   coordinator holding merge maps.  This can reduce the shardable critical
   path by about the worker count, but introduces scheduling, cancellation,
   resource-counter, and first-hit ordering hazards.  It is not the first
   safe patch.

### 3.3 Minimal safe v2 versus larger redesign

The minimal safe version is proposals 1-4: lazy authenticated templates,
complete source descriptors/translated-row memo, bounded section caches, and
sealed 256-attempt checkpoint chunks.  These preserve the current scan order,
dual epochs, positive-only schedule, receipt literals, and helper firewall;
the checker independently rebuilds each cache and validates the same rows.
Proposal 5 is a separately audited optimization after the incremental
invariants are specified.  Proposal 6, together with append-only checkpoint
chunks, is the larger redesign and should receive a new schema/driver and a
new independent checker path.

## 4. Fail-closed boundary

The following apparent speedups are rejected:

- Sampling translates, stopping correlation at the first active pair, or
  replacing the complete `B*s` accumulation by a sample is not equivalent.
- A hash-only cache hit is insufficient.  The typed row, source word,
  contributor list, and direct replay must still be literally regenerable;
  digests are integrity bindings only.
- Producer/checker helper sharing is forbidden.  Identical cache formats do
  not permit importing a producer cache or arithmetic helper into the
  independent checker.
- A coordinate change, including normalized E1/E2 semantics, invalidates
  pivots.  Stored pivots, reduced targets, duals, and cursor state may not be
  reused without the rank-zero replay and semantic digest gate.
- A resource stop is never `NONMEMBER_D`, `COMMON_WORD`, or nonmembership.
  It remains a registered typed `UNKNOWN_RESOURCE` with a sealed resumable
  checkpoint.  A partial task187 correlation cannot produce a negative
  terminal.

No performance claim is based on the absence of completed logs from either
live run.

## 5. Delivery and first recommendation

If either live run times out, the first versioned implementation should be a
new minimal v2a containing proposals 1, 2, and 4: cache immutable Fox/source
descriptors independently on producer and checker, memoize only exact typed
rows/sections, and checkpoint every registered 256-attempt chunk.  For
task187 this must include the new partial-correlation checkpoint before any
speed claim; for task186 it must preserve the existing weighted-row validator
and rank-zero resume firewall.  Run the unchanged complete checker only after
the new receipt/checkpoint invariants pass.  No live job or current pinned
commit should be edited by this audit.

The reply's own identity is reported externally below and is intentionally
not embedded in the file to avoid a self-referential hash.

STATIC SPEED AUDIT:                         COMPLETE
LIVE RUNS MODIFIED:                         NO
MATHEMATICAL COVERAGE WEAKENED:             NO
IMPLEMENTATION / GHA:                       NOT EXECUTED BY LUNA
