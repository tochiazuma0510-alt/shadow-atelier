# Luna reply 377: R07 lift-null positive dovetail v5

Task377 is implemented.  No new physical owner mismatch was encountered.
The implementation is static-only and production-unexecuted.

## Deliverables

```text
search/d972_r07_direct_relator_a5_a7_fusion_v5.py
  57482 bytes
  ce9c6b0d7ba587f877634b60e0162f8ad3f60091b182b3031775b512f719f2ff
crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v5.py
  29559 bytes
  e651ad1909e3a50152e9ff7574b6a3f7dddf841402fff04ef809c81e940ccfba
search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v5.g
  6675 bytes
  5f1aefba79c4fde1c5a0688a62a83effe3bb590e16c016c95a6797514d6f2dea
```

The reply identity is reported externally after its final bytes are fixed.

## Producer path

V5 restores the exact frozen v4/v352 binder, A5-v3, task198-v12 and
task292-v2 core.  A5 NONMEMBER and canonical endpoint ZERO retain their v4
terminals.  Only canonical NONZERO enters the new positive dovetail.

The marked Cayley BFS uses letters `(1,-1,2,-2)`.  Equality is the complete
canonical serialization of all ten affine roofs and every nonzero sparse
gradient entry; no digest is used as an equality key.  Each edge is replayed
through `Runtime.states_direct`, then its literal Schreier word
`s(q)t s(qt)^-1` is checked equal to the full ten-state identity before an
identity or duplicate word is suppressed.

Each round advances one Cayley edge, creates one next shortlex freely reduced
F2 translation, and gives one discovered seed a cyclic translation turn.
Because the Cayley image and eventual seed roster are finite, this compact
per-seed-cursor schedule reaches every finite edge and every finite
`(seed,V)` pair if no resource bound intervenes.  It does not materialize a
quadratic pending-pair queue.

For a pair `(Vn)-V`, the frozen task292 `ExactArtin`, occurrence builder and
`endpoint_terms_for_block` functions compute the empty-epsilon incremental
H1/H2/P column directly.  Coordinates are the block plus the complete Artin
normal-form key.  A sparse GF(3) echelon retains exact column ancestry.  A
span hit is checkpointed before the expensive terminal replay; the producer
then constructs the complete `M_can + sum a_i((V_i n_i)-V_i)` literal and
requires a direct task292 ZERO result in all three blocks.

Pair cursor advancement is transactional: a resource stop inside an exact
column computation does not skip that pair on resume.  Only completed
columns advance the seed cursor; only independent columns are retained in
the ancestry basis.

## Checkpoint and resource path

The sealed checkpoint binds the exact v5 source, every frozen v4/A5/task198/
task193/task292 source, the physical task198/task193 owners, A5 digest,
canonical literal digest and canonical exact endpoint digest.  It persists
Cayley words and edge cursor, complete identity key, seed roster, translation
generator cursors, every per-seed translation cursor, sparse echelon,
ancestry columns, counters and any pending final solution.  On resume affine
states are reconstructed from the authenticated literal words.

Cadence, wall seconds, RSS bytes, operation cap, checkpoint byte cap and the
all-or-none resume path/bytes/SHA triple are exposed by the driver.  Periodic
checkpoints and progress lines are emitted during the dovetail.  Wall and RSS
guards stop at 97% and 90% respectively so the current checkpoint can be
written before the hard bound.  A bounded miss remains `UNKNOWN_RESOURCE`
with `bounded_miss_is_A7_negative=false`; an already accepted A5 sidecar is
written before the lift-null phase.

## Independent checker and driver

The checker never imports v5 producer code.  It uses A5 checker-v3,
task198-v14 arithmetic, the v4 independent v352 reconstruction, and the
task292 checker implementation.  It replays only selected finite ancestry:
each selected marked edge, `rho1(n)=1`, `rho1(Vn)=rho1(V)`, the rebuilt final
literal, and final task292/full-C1 ZERO.  The unused BFS is not replayed.

The ASCII GAP driver contains one producer command.  Its single checker
command is inside the MEMBER-only branch.  NONMEMBER and UNKNOWN_RESOURCE do
not start a checker.  Receipt, optional verdict, accepted-A5 sidecar,
checkpoint, progress log and checker log are left as separate artifacts.

## Static acceptance

- Both Python files passed in-memory byte compilation under `python -B`.
- Frozen v4, A5-v3, task198-v12/v14 and task292 producer/checker owners loaded
  under non-main names with exact byte/SHA pins.
- GAP 4.16.0 `ReadAsFunction` parse-only passed; emitted warnings were the
  expected unbound top-level driver globals, with no syntax error.
- All three executable files are ASCII-only, and driver byte/SHA pins equal
  the final producer and checker files.
- No production search, GHA dispatch, network access, git operation,
  SELFTEST, mutation campaign, retry, pool or duplicate producer pass ran.

```text
TASK377_R07_LIFT_NULL_POSITIVE_DOVETAIL_V5_IMPLEMENTED_STATICALLY_UNEXECUTED
ACTUAL_A5_CANONICAL_AND_LIFT_NULL_TERMINALS_NOT_COMPUTED
VERIFIED_FALSE
```
