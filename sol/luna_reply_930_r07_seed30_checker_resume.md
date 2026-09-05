# Task930 reply -- seed30-only checker/workflow resume

## Handoff

The unfinished independent checker and narrow workflow are complete for the
root's short release audit and GHA launch. No local Python/GAP, network,
credentials, Git, dispatch, sub-agent spawn, or old Conn construction was used.
No actual materialization or selftest execution is claimed here.

Only the following authorized files were edited by this worker:

- `search/check_d972_r07_actual_seed30_materializer_v1.py`;
- `.github/workflows/d972-r07-actual-seed30-materializer-v1.yml`;
- this reply.

The producer remains Task929's file. Its frozen ABI/source identity was
coordinated directly with that worker; its arithmetic is neither imported nor
executed by the checker.

## Source receipts

PowerShell `Get-Item` / `Get-FileHash -Algorithm SHA256 -LiteralPath <file>`
gave these release receipts:

| file | bytes | SHA-256 |
| --- | ---: | --- |
| checker v1 | 62,048 | `f4f8ba2d342cb60e2c70b708b8847768a78ebde40dd0a52879f460cb558eab36` |
| workflow v1 | 23,876 | `a545a9d05591d5325c8544f46c31429ef1826aaf99cd335e844f69905f029344` |
| producer v1, owned/frozen by Task929 | 79,651 | `3ce9293e05f06bf343bd2a54af0ab84ae67f4b922a428cd3c73e38944d6de55c` |

The checker pins its accepted checker-only executable lineage before import:

- actual root scalar checker v2: `e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6`;
- affine/Fox checker v15: `8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662`;
- physical separator checker v2, used only for the accepted rho2 reader:
  `bb5d0c0a51408a65c3200b552e6a1eac2f832abeeca8e19fcce64d570f0967f6`.

The workflow pins both new programs, the flat rho2 stager, and the disclosed
producer/checker dependency lineages. It includes GHA-side `ast.parse` of
those source files; no local syntax execution was performed.

## Exact scope and checks

The only materialization is corrected run33941591417/1, character0, seed30,
empty actor word, origin30/scalar1. Both final artifact9962060495 and
diagnostic artifact9962060193 have the exact Task927 Section5 archive
identities in the workflow and in the candidate parent ABI. Launch and source
receipt bytes are fixed, and their Task554/P1/Task712/state joins are checked.
The saved scalar vector must have its first30 entries zero and seed30=1.

The checker independently:

1. Authenticates each full Task554 body, immediately retaining only four
   seed30 expressions plus root/body identity. All five large parsed bodies
   are never kept simultaneously.
2. Retains/seals raw expression order and coefficient multiplicities before
   modulo3 collection. It retains P1 literal roots even for numerically
   cancelled raw terms; only the final902 nonzero rows enter arithmetic.
3. Authenticates the fixed P1 instruction stream/cache and the twelve lower
   blobs, then reconstructs the raw seed minus its complete selected lifts.
   All96776 lower coordinates must vanish. The full filtered character0
   projector acts on that complete defect; its top must equal the plain slice.
4. Applies the accepted forward B table and independently computes its
   transpose pullback. Both `q(d)` and `lambda(G)` must be1.
5. Authenticates the old rank1354 state/instruction stream/checker receipts
   once per program as an external derivation premise. It does not reconstruct
   Conn, the8059 old offers, or the610996 old reductions.
6. Reduces the new row in insertion order, requires all1354 earlier pivot
   zeros, records raw versus normalized rows and scale, and permits exactly
   rank1354-to1355. The new instruction uses the accepted rolling-head rule.
7. Decodes/authenticates the retained12096-byte target remainder from Task904
   `target_reduction.remainder`; its884 old reductions are referenced, not
   copied or repeated. Only one new normalized-pivot elimination is computed.
8. Reconstructs the next separator by reverse substitution if the new target
   remainder is nonzero. A zero remainder is only a ConnectionMemberCandidate.
   It compares every emitted candidate payload/JSON/manifest against its own
   independently reconstructed exact bytes, not candidate self-seals alone.

## Flat delta ABI

Required files are `manifest.json`, `result.json`, `instruction.json`,
`source-d.bin`, `physical-raw.bin`, `physical-remainder.bin`,
`physical-normalized.bin`, and `target-remainder.bin`. `lambda.bin` exists
exactly for a Separator terminal. The source row is36288 trits; physical rows
are48384 trits, all packed four base3 trits per byte. No parent-state files are
copied into the candidate.

The sealed result contains exact parent tuples/receipts, raw seed, complete
subtraction, raw/P1/projector ancestry, raw materialization, pairings, a sealed
physical pivot, one target update, optional next separator, and explicit
literal-replay limitations. `instruction.json` has one rolling instruction;
the old state is referenced by manifest/head and pivot instruction roots.

## CLI and workflow

The exact checker command is:

```bash
python -B -u search/check_d972_r07_actual_seed30_materializer_v1.py \
  --scalar-root "$SCALAR_ROOT" \
  --scalar-diagnostics-root "$SCALAR_DIAGNOSTICS_ROOT" \
  --prepare-root "$PREPARE_ROOT" \
  --block-root "$BLOCK_0_ROOT" --block-root "$BLOCK_1_ROOT" \
  --block-root "$BLOCK_2_ROOT" --block-root "$BLOCK_3_ROOT" \
  --p1-root "$P1_ROOT" --task712-root "$TASK712_ROOT" \
  --state-root "$STATE_ROOT" --rho2-root "$RHO2_ROOT" \
  --candidate-root "$RUNNER_TEMP/output"
```

The producer uses the same parent arguments with
`--output-root "$RUNNER_TEMP/output"`. Checker stdout is one JSON verdict;
progress is flushed to stderr. Optional checker `--output-root` must be a
fresh directory disjoint from every parent/candidate and only stores its
checker result.

Both programs have `--selftest`. The workflow runs serial authenticated
staging, the two bounded synthetic test suites, actual producer, actual
checker, then final upload. Phase/selected-row progress remains visible.
Diagnostic upload uses `if: always()` and excludes the large downloaded
parents. The final upload is gated on checker PASS. The configured per-program
caps are40 minutes; job cap is90 minutes. No historical selftests/all504 orbit
scan are prerequisites.

## Authored finite canaries, not execution results

The checker suite covers thirteen short packed roundtrips; invalid packed
bytes/padding; canonical JSON/boolean types; raw event order; duplicate
coefficient multiplicities and cancelled literal roots; a coherently resealed
order mutation; a fixed-parent byte mutation; late coordinates in each lower
block; nonmonotone insertion order; duplicate leads; scale2 raw/normalized
distinction; a dependent-row rejection; one target elimination; reverse
separator substitution; membership-candidate and zero-coefficient branches.
Task929's independent bounded producer suite runs before this checker suite.

There is no known static implementation blocker. Actual Python syntax,
synthetic execution and production arithmetic remain to be exercised in GHA;
none is represented as having passed locally.

```text
WORKER_RUN_ID=NOT_RUN
WORKER_COMMIT_SHA=NOT_CREATED_BY_WORKER
ACTUAL_NEW_PIVOT_RESULT=NOT_RUN
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
NORMALIZED_EXPONENT_PAIR=NOT_REPLAYED
ELEVEN_SLOT_REPLAY=false
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
cross_checked=false
verified=false
```

Root remains the sole Git/GHA broker and records the eventual commit/run
identities after its release audit and launch.
