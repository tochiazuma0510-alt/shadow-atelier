# Task922 -- implement the corrected actual root scalar batch v2

Role: implementation. Process all sections. Root supplies the mathematics
in v541 and coordinates the sole local Python execution slot and GHA.
Implement only:

- `search/d972_r07_actual_grade2_root_scalar_batch_v2.py`
- `search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py`
- `sol/luna_reply_922_r07_filtered_root_scalar_batch_v2.md`

Use apply_patch. Leave all v1 files and old artifacts intact. No git,
credentials, dispatch, or large local production calculation.

## 1. Exact repair and retained infrastructure

Read v541 completely, Task920 intake and Task921 audit when available.
The actual v1 seed2 scalar is invalid as a physical violation: corrected
scalar is zero. Both seed and actor direct sides must be fixed in this
single v2 implementation. Preserve the existing fixed P1/Task554/Task712/
separator identities, raw duals and all 32280 origin order.

Start from the corresponding actual root batch v1 files. Retain their
accepted exact-parent validation, one P1 cache pass, vectorized bounded
chunks, prepare-plus-one-block relation accumulation, output reconstruction
in the independent checker, and conservative terminal boundary. Version
schema/CLI labels to v2. Existing independent v15 arithmetic contexts may
be reused on their respective producer/checker sides; do not call either
old projected direct-seed routine.

## 2. Correct seed direct values

Construct the existing affine-Fox context once. For each registered seed,
evaluate its FULL raw row, then take the ordinary character slice of its
degree-two array. Compute `<q,raw_seed[2][a]>`. Never full-project just the
direct seed before subtracting plain cached P1 slices. Do not enforce the
old SEED_REGISTERED_ROW_SHA, since those hashes describe the wrong rows.
Record fresh raw-seed row/value digests; checker independently derives them.

## 3. Correct actor direct values without per-row full actors

Implement v541 (4.1) to construct for each active q and actor t the lower
covector `kappa=(pi_a K_t)^*q` of width 96776. Its auxiliary entries are zero.
Keep both Fox components, all six tags and coupled monomials, the actual
transported Fourier signs, affine PSL translation `g -> u_j*g`, parity
shift and polynomial coefficients. Use vectorized small arrays over the
504 PSL coordinates. Do not generate a 96776-by-36288 matrix or call the
full actor on every basis vector/P1 row.

Compute `w_t[i]=<kappa,b_i>` from the authenticated Task554 source blobs:
old row lower width6056 plus grade companion width72576; new row width18144.
Use the exact readers/paths identified in Task920. Four lower covectors
and four 8059-trit result arrays suffice for the sole active character0.
No dense 8059-by96776 matrix, full DAG reconstruction or packet replay.

Add w_t to the homogeneous child-value arrays at direct-actor initialization
before v540's unchanged relation subtractions. Do not relabel the corrected
sum as a homogeneous P1 child pairing: retain separate hashes for the old
top values, lower contractions and complete actor-direct values.

Read old blobs while prepare is resident; read a new basis blob while its
one block is resident. Every blob descriptor is authenticated by the fixed
Task554 body SHA, then its exact bytes/shape/hash/padding are checked by each
side before interpretation. Extend the launch file roster to include the
eight old lower/grade blobs and four new basis blobs. The workflow helper
is being prepared separately; send its agent exact required descriptors.

## 4. Minimal output and current result boundary

Keep RootViolationBatch / AllFourRootEOF / RootZero distinctions. Add an
explicit v541 formula identifier and bind lower blob receipts, lower
covector hashes and lower value hashes to character/result outputs. Hashes
must describe independently recomputed arrays; no caller-provided physical
row or truth flag can replace the arithmetic. Save the 44 corrected seed
scalars and the actor-lower value arrays (small) so the next actual
materializer can consume the exact selected origin without a second search.

Actual seed2 must evaluate to zero. A new violation, if any, remains an
input to materialization, not a physical pivot or Grade2/A0 terminal.
`verified=false`, all current upper claims retained as NOT_DECLARED.

## 5. Focused tests and delivery

Use only bounded tests that detect this repair's real risks:

1. actual seed2 raw/projected difference pairing2 and corrected scalar0;
2. mixed/lower-only full actor adjoint equality, including a known nonzero
   lower-to-top contribution; compare independently with direct full actor;
3. pure-top adjoint matches the accepted Task712 homogeneous action;
4. streamed dot products on tiny old/new packed rows match dense arithmetic,
   with nonzero cross-character grade companions;
5. a tiny scalar array agrees with direct FULL-defect evaluation, and omitting
   the lower term or preprojecting only the seed causes a failure;
6. existing exact envelope reconstruction remains complete after new fields.

Do not rerun broad historical audits, grow a fixture framework, or run all
large parents locally. Before any local Python, ask root for the current
execution slot in an agent message; this coordinates the user's prohibition
on parallel local Python across agents. After initial checks pass, deliver
exact source hashes/bytes and clear GHA readiness. Source+checker audit is
one narrow pass before root's actual GHA launch, not a new research phase.
