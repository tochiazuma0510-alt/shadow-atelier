# Luna reply 378: R07 annotated PB boundary compiler v1

Task378 is implemented.  No physical task377-v5/task292 ABI blocker was
encountered.  The implementation is production-unexecuted.

## Deliverables

```text
search/d972_r07_endpoint_zero_annotated_boundary_v1.py
  79194 bytes
  c6e4b0d99ed79f9eabedf225c964a598b2f21b3ab10758cb9d5f83a60ceb5d11
crosscheck/check_d972_r07_endpoint_zero_annotated_boundary_v1.py
  45525 bytes
  719f1b97b793599a0a6013512636c346dc00fbd6f445ecb6b93ef1b0d685d717
search/d972_r07_endpoint_zero_annotated_boundary_gha_driver_v1.g
  6961 bytes
  3945df111d7578cbc89776ee01c6c804d4264877080249ee35a270c2db59ebd6
```

The reply identity is reported externally after its final bytes are fixed.

## Parent and finite graph gates

The producer accepts only a sealed physical task377-v5 `MEMBER`, its sealed
`ACCEPTED` independent verdict, and the receipt-linked checkpoint and A5
sidecar.  It requires the frozen producer/checker/driver pins, exact artifact
byte/SHA identities, common owners/static bindings, the fixed-word claim
scope, the lane-correct checkpoint phase, and the verdict's independent
task292 ZERO/full-C1 replay.  The v5 verdict has no invented `source` field:
the exact checker source is instead retained and checked as the frozen local
authority pin while the verdict seal binds the physical receipt and both
artifacts.

For H1, H2 and P, the compiler independently replays the parent
`D1_z_zero`.  Complete Artin tuples, never hashes or finite quotients, key the
vertices.  Source/target prefix paths and every support cell are inserted;
negative traversal is serialized as the negative positive cell based at
`g*x^-1`.  A deterministic BFS tree gives all literal tree paths.  Every
oriented non-tree edge retains its unreduced/reduced fundamental loop, exact
Fox cycle, GF(3) coefficient and residual tree-edge elimination roster.  The
complete collected cycle sum is required to equal the parent's `z_B`.

## Annotated combing and boundary extraction

The combing engine uses task292's lexicographic generators and original
two/eleven-relator rosters.  It recursively collects ranks 4, 3 and 2.
Positive-old/positive-kernel crossings use the uniquely matched original
`a^-1*k*a*phi_a(k)^-1`; negative kernel crossings use its inverse and
context, and old-inverse crossings are obtained by positive collection,
trace reversal and the two-sided `a^-1` context.  Every `phi` is recomputed
from task292's faithful Artin action.

Annotations are a flat-ID DAG of shared reduced word nodes plus atom,
context, reverse and concat nodes.  Each new node checks its literal
invariant and strict ancestry; final flattening is iterative, so the trace is
not repeatedly copied and a long left-deep trace cannot exhaust Python's
recursion stack.  Every fundamental loop must have the identity Artin tuple,
empty recursive normal form, and literal equality to its flattened product
of conjugates of original relators.

Cycle coefficients, trace signs and conjugators are accumulated into each
`q_B`.  The unchanged task292 producer Fox owner directly replays and
collects `D2(q_B)` by `(component,full_artin_key)` and requires exact equality
with `z_B` before `MEMBER`.  The receipt retains graphs, support paths, tree,
cycles, elimination, loops, annotation DAGs, flattened traces, q
accumulators, collected q and all three D2 replays.  Its only new positive
claim is fixed-word A8; A9, compatible lift, mixed-prime, perfect-core, fake
and Ihara remain `NONE`.

## Resume, checker and driver

Cadence, wall-time, RSS, operation and checkpoint-byte caps guard the Artin,
letter-crossing, DAG and Fox hot paths.  Checkpoints retain completed
graphs/cycles, the block/cycle cursor, literal input/current word, recursive
rank, last action words, annotation DAG and accumulated q sources.  Resume is
an all-or-none path/bytes/SHA triple bound to the exact compiler source,
frozen sources and four parent artifacts.  Artin vertices, edge actions,
loops, cycle Fox rows, relator rosters, completed traces, q accumulator and
D2 rows are recomputed on restore.  A bounded stop is only
`UNKNOWN_RESOURCE` and preserves the latest checkpoint.

The independent checker never imports the new producer.  It uses only the
checker-side task292 presentation, faithful Artin evaluator and Fox owner.
It reauthenticates the four parent artifacts, reconstructs the exact finite
graph closure, checks the deterministic tree and signed cycle elimination,
audits every DAG and literal loop trace, independently recollects q, and
requires a fresh `D2(q_B)=z_B` in all blocks.

The ASCII GAP driver has exactly one producer command and places its one
checker command solely inside the new `MEMBER` branch.  It keeps receipt,
verdict, checkpoint, progress log and checker log separate, exposes all four
parent paths and all resume/resource arguments, and pins the final producer
and checker identities printed above.

## Static acceptance

- Both Python files passed in-memory byte compilation under `python -B`.
- The frozen task377-v5 producer/checker/driver and task292 producer/checker
  restored under their exact byte/SHA pins; the new checker restored its
  exact producer pin without importing that producer.
- GAP 4.16.0 `ReadAsFunction` parse-only passed.  Output contained only the
  expected unbound top-level driver-global warnings.
- All three executable files are ASCII-only, and the driver byte/SHA pins
  equal the final producer and checker files.
- No production run, GHA dispatch, git/network operation, SELFTEST, mutation,
  retry lane or search was executed.

```text
TASK378_R07_ANNOTATED_PB_BOUNDARY_COMPILER_V1_IMPLEMENTED_STATICALLY
ACTUAL_PARENT_MEMBER / q_H1 / q_H2 / q_P: NOT_COMPUTED
A8_FIXED_WORD: CODE_PATH_READY, NOT_YET_COMPUTED
A9 / COMPATIBLE_LIFT / MIXED_PRIME / PERFECT_CORE / FAKE / IHARA: NONE
VERIFIED_FALSE
```
