# Luna task 157 — exact faithful matrix-56 Burau campaign

Implement and GHA-wire the exact low-memory route recommended by replies
156a/156c.  This is an implementation task; do not make an A/B theorem claim.

Authorized files:

- `search/d972_b4_burau_matrix_v1.g`
- `.github/workflows/d972-burau-matrix-v1.yml`
- `sol/luna_reply_157_burau_matrix_impl.md`

Do not edit any earlier producer/workflow or unrelated file.  Do not run local
GAP, commit, push, or dispatch.  The parent Sol session is the sole broker.

## Frozen mathematical construction

Reuse the frozen 36-point roof, the frozen 972 word/key artifact, its semantic
digest, and the five literal A.18 Burau blocks from the audited v2 producer.
For each `(q,a)` construct a faithful block diagonal representation

`Phi(p,M1,...,M5) = diag(R_q(p),M1,...,M5) in GL(56,q)`,

where `R_q(p)` is the full 36 by 36 permutation matrix.  Never materialize the
old `36 + 5*q^4` point action and never projectivize any Burau block.

Build both generators explicitly and set `H=Group(hx56,hy56)`,
`Hp=DerivedSubgroup(H)`.  Independently keep `P=Group(roofX,roofY)` and
`Pp=DerivedSubgroup(P)`.  Define the exact generator-image homomorphism
`pi:H->P`, restrict it exactly to `pip:Hp->Pp`, and require
`Image(pip)=Pp`, `Size(P)=1469664`, and `Size(Pp)=367416`.

Compute `K=Kernel(pip)` with GAP's exact finite-group operation.  Do not assume
its q=5 order.  Enumerate all `Elements(K)`, prove their count/distinctness and
first-block identity.  For each of the frozen 972 rows replay the common word,
obtain an exact preimage/representative in `Hp`, enumerate its full coset by K,
extract the five 4 by 4 blocks, and evaluate the same paper-convention defect
as v2.  A zero identity-defect fiber is only a finite-obstruction candidate;
all-pass is UNKNOWN.

## Calibration and fail-closed gates

Support exactly these registered pairs:

- `(q,a)=(3,-1)`
- `(q,a)=(4,2)` (correct GF(4) element encoding; copy/audit v1 helpers)
- `(q,a)=(5,2)`
- `(q,a)=(5,4)`

Before q=5 can run, q=3 and q=4 must reproduce the already frozen calibration:

- `|H|=105815808`
- `|H'|=2939328`
- `|K|=8`
- `|P'|=367416`
- all 972 fibers have size 8 and exactly one identity defect.

These numerical expectations are calibration-only.  Do not impose any of
them (except the roof orders) on q=5.

Required selftests/gates include all Artin relations, determinants, the
permutation-matrix row-action orientation (`R(p*q)=R(p)R(q)` or an explicitly
corrected equivalent), faithful block extraction, paper product convention,
A.18 swapped/reversed negative controls, homomorphism round trips, complete
kernel enumeration, receipt hashes, unique 972 target keys, and exact terminal
markers.  A resource stop or GAP diagnostic must remain nonterminal.

Use a new receipt schema with compact serialized matrix entries and enough
data to independently reconstruct every fiber and defect.  Preserve exact
common-word provenance and progress markers after H, Hp, K, and row chunks.

## Workflow

Create a new versioned workflow by copying the already audited pinned GAP
4.16.0 / required-packages / JSON bootstrap from
`.github/workflows/d972-burau-direct-v1.yml` without weakening its hashes,
closed-input gates, PIPESTATUS handling, diagnostic gate, marker checks, or
failure artifacts.  It must:

1. trigger on the exact working branch push when either its own file, the new
   producer, or the frozen artifact changes;
2. run q=3 and q=4 calibration jobs first;
3. only after both calibrations pass, run q=5 a=2 and a=4 as independent matrix
   jobs with `fail-fast:false`;
4. upload unique attempt artifacts on success or failure;
5. use no arbitrary workflow input and no secret-bearing checkout;
6. retain a six-hour timeout and an explicit GAP workspace ceiling suitable
   for the standard public runner.

The parent will static-audit, commit, push, and monitor the GHA campaign.
Report exact hashes, syntax/static checks, known runtime risk, and every file
changed in `sol/luna_reply_157_burau_matrix_impl.md`.
