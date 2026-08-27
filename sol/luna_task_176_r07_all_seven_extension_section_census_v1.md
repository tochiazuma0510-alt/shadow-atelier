# Luna task 176: R07 all-seven extension-section census v1

Date: 2026-08-27
Role: Luna / implementation and bounded-computation preparation only

## 1. Objective and frozen mathematical universe

Implement the finite extension-section reduction of
`sol/proof_r07_all_seven_extension_section_orbit_reduction_v125.md` for the
one fixed R07/g760 all-seven context family.  Do not enumerate the linked
context image directly: task174 already proved the cross-checked lower bound
`|Delta_E| >= 2,000,001`, so increasing that BFS cap is out of scope.

Use the authenticated extension

```text
1 -> Gamma -> G -> Q0 -> 1
|Gamma| = 243
|Q0|    = 1,469,664
```

from task157ee.  The ordered ten-coordinate map is exactly v125 (1.7):

```text
0 d_E C21   source E3 (x,y)
1 d_E C22   source E3 (x,z)
2 d_E C23   source E3 (y,z)
3 d_E C24   source E3 (u,x)
4 d_E C25   source E3 (u,y)
5 C1        E4 b1 / phi234
6 C27       E4 b2 / phi1_23_4
7 C21       E4 b3 / phi123
8 C26       E4 b5 / phi12_3_4, inverse slot
9 C28       E4 b4 / phi1_2_34, inverse slot
```

Coordinate 0 and coordinate 7 deliberately reuse registry row C21 before
and after deletion.  They remain different typed coordinates.  Pin, do not
reprove, v108, v121, and v122.

This task computes the full-family and ten one-coordinate extension-section
data only.  It does not solve the all-seven residual equation and does not
run support correlation over 6,441 relations.

## 2. Authorized deliverables

Create or edit only these five files:

```text
search/d972_r07_all_seven_extension_section_census_v1.py
crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
search/d972_r07_all_seven_extension_section_census_gha_driver_v1.g
search/certs/d972_r07_all_seven_extension_section_census_preflight_v1_20260827.json
sol/luna_reply_176_r07_all_seven_extension_section_census_v1.md
```

Do not run Python, Node, GAP, git, or GHA locally.  The parent is the only git
and workflow broker.  The checked-in receipt is an immutable fail-closed
`UNKNOWN_RESOURCE:LOCAL_EXECUTION_GUARD` fixture; executed outputs go only to
`ci/out` on GHA.

## 3. Producer requirements

The producer must independently authenticate every frozen source by exact
bytes and SHA-256, including the task157ee q3/joint receipt, its source and
checker lineage, v122, v125, and the task174 terminal receipt note.  It must
not import mutable task169 or task175 code.

Reconstruct the exact marked generators, E3/E4 arithmetic, deletion map,
the 31-row registry, Gamma states, Q0 presentation/state enumerator, and a
deterministic section `s:Q0 -> G`.  Replay all generator images and the
coarse/fine deletion identities before a census can start.

For the following eleven ordered families

```text
ALL = [0,1,2,3,4,5,6,7,8,9]
S0=[0], S1=[1], ..., S9=[9]
```

compute exactly:

```text
A_S = Phi_S(Gamma)
L_S = {q in Q0 : Phi_S(s(q)) in A_S}
|D_S| = |A_S| * [Q0:L_S]
```

and for each singleton compute

```text
|ker(Delta_all -> D_Si)| = |D_ALL| / |D_Si|.
```

Every division and Lagrange assertion is a fail-closed integer/group check.
Check identity, closure, inverses, and normality of every `L_S`; do not infer
subgrouphood from a membership count.  Check section independence on a
second deterministic section or on an exact nontrivial section twist for a
registered bounded sample and record the literal comparison.

Retain enough lossless data for the next v118 consumer:

1. canonical literal element tables and Gamma section/adjustment indices for
   every `A_S`;
2. one shared Q0 discovery order, parent/letter table, and canonical roster
   digest;
3. exact membership bitsets for all eleven `L_S`;
4. actual source-word generators for each `Gamma_S^0` and each singleton
   kernel `H_S`, using v125 (3.5)--(3.6);
5. direct replay of every emitted word generator in all ten linked
   coordinates, not merely in its deleted coordinate;
6. an image-section primitive for each singleton target represented during
   the run, with Gamma/Q0 provenance; and
7. typed coordinate/image/kernel order tables and equality-pattern tests.

Compact parent tables and bitsets are allowed, but counts or hashes without
lossless decoding are not.  Do not serialize all Delta elements.  If an
authenticated Q0 section or Gamma adjustment needed by these requirements
cannot be reconstructed from the frozen shelf, stop at a specific
`UNKNOWN_INPUT:*` terminal rather than substituting a direct BFS.

## 4. Independent checker and destructive controls

The checker must import neither producer nor producer helpers.  It must
independently rebuild group arithmetic, the ten maps, Gamma, Q0 sections,
all eleven A/L families, order formulas, bitsets, word generators, and direct
ten-coordinate replays from pinned primary inputs.

Use the same production validator for executed receipts and selftests.
Include genuine bounded nonabelian extension fixtures with linked
projections.  At minimum, resealed semantic mutations must reject:

```text
coordinate 0/7 typed deduplication
one deletion-map generator image
one Gamma element
one Q0 parent letter
one section value
one A_S literal element
one L_S membership bit
one L_S normality witness
one Gamma adjustment index
one emitted source word
one full-family coordinate dropped
one singleton label swapped
one kernel-order quotient
one canonical roster digest
one COMPLETE/UNKNOWN terminal alteration
```

Mutations must traverse reconstruction and the production validator; stale
hash rejection alone is not a semantic control.  Report exact attempted and
rejected counts.

## 5. Executable GHA driver

Write an ASCII-only GAP wrapper with exactly two externally selected modes:

```gap
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:="SELFTEST";;
D972_R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_V1_MODE:="PRODUCTION";;
```

Unbound or any other value is an error.  SELFTEST must be cheap and must not
enumerate Q0.  PRODUCTION runs exactly one producer followed by exactly one
checker, serially, with fail-closed outer timeouts, `pipefail`, rejection of
pre-existing driver-owned `ci/out` outputs, exact source pins, exact-one
markers/terminal, artifact hashes, timings, and a final sentinel.  State the
generic `.github/workflows/gap-run.yml` preamble and a conservative time/RSS
estimate in the reply.  No optional p-quotient package is expected unless a
frozen input proves it necessary.

## 6. Terminal and claim boundary

A workflow SUCCESS is not itself a mathematical COMPLETE.  The only positive
promotion is a producer COMPLETE receipt independently accepted by the
checker.  A cap or deadline is `UNKNOWN_RESOURCE`; missing serialized data
is `UNKNOWN_INPUT`; neither may be advertised as an order.

The maximum claim of this task is:

```text
exact Delta_all and ten projection orders
word-bearing projection-kernel/section data for v118
```

It is not an all-seven solution, correction word, cofinal lift, fake, or
Ihara witness.  Finish the static bundle and report final SHA-256/bytes and
`GHA dispatched=false`; the parent will audit, commit, push, and dispatch.
