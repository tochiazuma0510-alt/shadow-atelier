# Luna reply Task601: packed-memory release repair v3

## Verdict

`READY_FOR_SOL_MAX_STATIC_AUDIT`

This is the bounded Task621 implementation of the four finite repairs required
by Task620 `PASS_AFTER_REPAIR`, on top of Task618/Task619. It changes no
registered route, pivot order,
mathematical equality, candidate decision, or claim status. Production has
not been run, so this is not yet a payload, checker success, cross-check, A0,
COMMON, fake, or Ihara result.

## What was removed or bounded

- The producer no longer retains Python tuple edge lists, lists of individual
  packed row objects, or later whole-stream joins. Each physical edge and row
  is appended directly to its final `bytearray`. Mutable node records survive
  only through MEMBER and reverse least closure, and are then packed once into
  fixed-width `<IBQIQI` records.
- `derived.states` and its accumulated expanded-state/children history are
  absent. Adjoint expansion retains only the live coalescing `pending` map,
  the exact final leaf map, and numerical progress counters.
- The producer authenticates/routes one block body and owner at a time. Once
  selected physical origins are known, it makes at most one second pass for
  each selected character and copies only that character's selected canonical
  DAG closure. Owners and bodies are released at each boundary.
- The checker parses ancestry once, uses fixed-width zero-copy node, edge, and
  row views, and has no decoded `gedges`/`ledges`, combined edge list, expected
  tuple list, expected row list, or terminal row join. Row canonicality is
  scanned once per authenticated stream, not once per reduction-edge access.
- Selected source/origin replay runs character by character before the pinned
  standalone router. Its body and owner are released before moving to the next
  character. The all-8,059 reroute then compares every accepted node, ordered
  edge, and packed row online with exact cursors and requires terminal
  exhaustion of all streams.
- The old-lower-zero cursor is sized from the complete zero-row receipt and is
  advanced for every old offer whose lower remainder is zero, independently
  of whether the subsequent grade offer is accepted or dependent.

The four Task620 release repairs are now closed: producer row canonicality uses
one zero-copy NumPy/C-level maximum scan; the pre-router lower recurrence visits
only `declared_lower` pivots; the independent basis comparison reuses the first
authenticated `physical["basis"]` view; and the checker selftest now rejects an
unfinished node/edge/row cursor plus both forbidden-state mutations through
the production predicates. The existing content-mismatch fixture remains.

## Evidence retained

The full physical transcript remains: every node, ordered signed reduction,
origin, stored lower row, lower companion, grade origin, and old-lower-zero
row. The reverse least selected physical closure, exact selected refs, unique
canonical selected source/defect/expression graph, literal dictionary, and
typed roots `C_<1`, `C_T`, and `C_1` also remain.

The exact quotient-specific leaf comparison receipt is now
`literal-leaves.bin`. Its header is `<8sBBBB32sQ>` with magic `R07LEAF1`,
version 1, flags `(quotient_specific_evaluation,
common_source_witness, states_exported) = (1,0,0)`, the raw ancestry SHA-256,
and record count. Each canonical `(seed, freely-reduced signed-int8 path)`
record uses `<IIBI>` for payload length, seed, nonzero coefficient, and path
length, followed by the path. Producer writes and hashes it incrementally;
the independent checker rederives the entire leaf map and byte-compares its
own complete canonical encoding. The leaf receipt is comparison evidence,
not authority for the canonical graph, and introduces no digest cycle.

Both producer and checker retain bounded phase/RSS diagnostics and a 64-KiB
emergency reserve. On `MemoryError` they release it and emit a bounded ASCII
`UNKNOWN_RESOURCE` diagnostic through `os.write`.

## Frozen obligations

The implementation still requires exactly:

- 8,059 offers in registered order;
- 2,014 old/lower offers and 6,398 grade offers;
- lower/grade ranks 1,661 and 5,044;
- all 3,317 Task595 MEMBER coefficients and zero remainder;
- all four parent block digests and the pinned standalone router SHA-256
  `a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3`;
- `direct_occurrence_replay:false`, `next_degree2_residual:null`, and all
  `cross_checked`/`verified`/A0/COMMON/FAKE/IHARA gates false.

Exact inputs remain source run/attempt `33677346616/1` and Task595 candidate
run/attempt `33707397894/1`, commit
`93f746ad1b649796e1bc28e00ff34993498929ee`.

## Local gates

The required commands were run serially:

```text
python -B -m py_compile search/d972_r07_a0_grade1_selected_slp_v1.py search/check_d972_r07_a0_grade1_selected_slp_v1.py
=> exit 0

python -B search/d972_r07_a0_grade1_selected_slp_v1.py --selftest
=> {"coefficient_2":"PASS","compact_leaf_mutations":2,"compact_leaf_roundtrip":"PASS","derived_states_absent":"PASS","fixture":"PASS","nonmonotone_lead":"PASS","reverse_closure":"PASS"}

python -B search/check_d972_r07_a0_grade1_selected_slp_v1.py --selftest
=> {"claim_flag_mutation_count":8,"coefficient_2":"PASS","compact_leaf_mutation_count":4,"compact_leaf_roundtrip":"PASS","derived_states_absent":"PASS","false_null_claim_gates":"PASS","forbidden_state_mutation_count":2,"zero_copy_cursor_exhaustion":"PASS","zero_copy_transcript_mutation":"PASS"}
```

Static YAML parsing and contract inspection pass. The existing 60-minute job,
8-GiB `ulimit -v`, 7-GiB internal RSS guard, 45-minute producer/checker
timeouts, success-only payload/verdict upload, always-uploaded logs, and pinned
actions are retained. The sole fire-marker change is
`[fire-grade1-selected-slp-v2]`.

## Final files

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | 47,935 | 1,332 | `cfd581f8a71176f9252555a94028a8482ede862ee3430098270109e52fa0d3ff` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | 71,637 | 2,008 | `09ee815345e9ad2cfd80799a5bf7daf4446cda0eb3d8bc79bd7b3d9c61fa86c8` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | 5,497 | 111 | final SHA-256 returned out of band after the reply pin is refreshed |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | REPLY_BYTES=007634 | 140 | final SHA-256 returned out of band after close |

The last two ordinary hashes cannot both be embedded here: the workflow pins
this reply, while changing either embedded digest changes the reply and hence
the workflow. Their exact final values are therefore returned together in the
completion handoff, without weakening the workflow's exact reply gate.

## Residual risk and actions not run

The compact paths and tiny fixtures are locally exercised, but the real leaf
population, final peak RSS, and end-to-end wall time are not known until the
single authorized production run. The pinned standalone router's established
source loader still materializes its four authenticated block inputs together;
Task618 explicitly permits that representation after all checker-side selected
replay caches have been released. Any new resource terminal remains
`UNKNOWN_RESOURCE` and must be re-audited, never interpreted as NONMEMBER.

`production = NOT_RUN`; `GHA = NOT_RUN`; Git mutation/stage/commit/push =
`NOT_RUN`. One read-only scoped `git status` inspection was performed; it
changed no state.

A fresh Sol(max) static audit is mandatory before the root session may perform
the one justified GHA rerun.

`R07_GRADE1_SELECTED_SLP_V1_NOT_READY`
