# 157ee — B345 joint-kernel qstar closure certificate

## Role and authorized scope

Luna implements one versioned, positive structural-certificate lane.  Only the
following four implementation/report files may be created, in addition to this
Sol task:

1. `search/d972_b345_joint_kernel_qstar_closure_v1.py`
2. `search/check_d972_b345_joint_kernel_qstar_closure_v1.py`
3. `search/d972_b345_joint_kernel_qstar_closure_gha_driver_v1.g`
4. `sol/luna_reply_157ee_b345_joint_kernel_qstar_closure.md`

Do not edit the workflow, q3, 157ea--157ed, or any other source.  The driver is
ASCII only.  Temporary diagnostic files stay outside the repository.  Run one
bounded combined self-test before freeze; a corrective rerun requires an
explicitly recorded reason.  Do not run the full mathematics locally.

## Frozen predecessors

- q3 artifact SHA-256
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`.
- 157ed producer/checker/driver:
  `d4a290984ae8a93b6959f06d20c1de037b2814707778fba03c59ac87b2f736db`,
  `677aa1b69e4415da9629c34fcf0e469ad974cf3c888be7e768635bac50f672ce`,
  `29a31752d42bd3f5a0e7f27ca38495bdd54c9cc694d12ddf9fe637e8749975e9`.
- 157ed task SHA-256
  `15511f73e665a90f1e518383cb7bd218d8dd8e747026c498c3b4acce62837c2f`.
- fixed prefix: columns 362725, pivots 362709, dependent 16,
  live entries 3090367, row-tail visits 2727658, pool 976408.
- qstar is the exact 154-byte, component-4 coordinate already pinned by 157ed.
  Its reverse-pivot raw functional has 362710 semantic entries and satisfies
  lambda(base target6)=2, lambda(-base)=1.

All source and task pins are hard authenticated.  No old receipt, basis, pool,
lambda table, or GAP presentation output may be imported.

## Mathematical universe and exact claim

Let `Theta` be the product of the following marked homomorphisms from the free
group `F2=<x,y>`:

- the pinned coarse permutation quotient `Q0` (degree 36, order 1469664),
- the exact E3 route used by 157ed,
- the 31 unique E4 context homomorphisms behind the 46 named uses.

Let `K = ker(Theta)`.  This is the preregistered joint typing kernel; it is not
all of H3 and not the kernel of an unregistered quotient.

For `s in K`, all three target6 correction occurrences
`a=s(x,y), b=s(x,z), c=s(y,z)` have E4 value one.  The left-Fox raw variation is

```
Delta_6(s) = L_C D(c) - L_C D(b) + L_h D(a),
```

with the exact 157ed `C,h` orientation.  Therefore
`mu(s)=lambda(Delta_6(s))` is an F3-homomorphism on K.

The positive terminal proves exactly:

```
mu(K)=0 in the fixed-prefix cokernel,
lambda(base target6)=2,
hence every s in K leaves the same nonzero qstar obstruction
against the registered fixed prefix.
```

This is a whole-joint-kernel result with respect to the fixed prefix.  It is
not full-D2 nonmembership, not full-H3 exhaustion, not nonexistence of a lift,
and not B4-A/B.  Since the raw lambda is not invariant under all E4 left
translations, no full-D2 promotion is allowed.

## A. Fresh fixed prefix and raw lambda

Producer imports only the pinned 157ed producer.  Checker imports only the
pinned 157ed checker and independently rebuilds E3/E4, the frozen prefix, and
the reverse-canonical raw lambda.  Both require all 157ed semantic/count gates,
the 16 original dependent-column events, qstar width/component, and
lambda(base)=NF-qstar(base)=2.  Candidate and relation queries never intern
new pool elements.

## B. The 243-element normal kernel Gamma

From the 27 q3 correction-fibre records, retain the 26 nonempty exact F2 words
in record order.  Evaluate each in E3 and all 31 contexts.  Enumerate the
positive Cayley closure in first-seen BFS order under those 26 words.

Hard gates:

- exactly 243 states and 243*26=6318 directed edges;
- closure stabilizes by generator-factor depth 4;
- the subgroup is normalized by x and y;
- order distribution `{1:1,3:26,9:216}`, exponent 9;
- center order 27, derived subgroup order 3, cube subgroup order 9;
- Frattini subgroup order 27 and quotient order 9 = `C3^2`;
- conjugacy-class distribution: 27 classes of size 1 and 72 of size 3.

Every public state uses the exact tuple of canonical element blobs; local state
IDs are first-seen implementation labels only.

For the spanning-tree section potential, separately accumulate

```
A(w)=lambda(L_h D(w_a)),
B(w)=lambda(L_C D(w_b)),
C(w)=lambda(L_C D(w_c)).
```

For each of all 6318 edges, compare tree potentials.  Export the full ordered
edge ledger digest and the 27-vector discrepancy distribution.  The closed
claim requires every discrepancy to be `(0,0,0)`.  This is a complete
presentation of relations among the 26 record generators, not a bounded-depth
sample.

## C. x/y action relations

For each record word `r_i`, each `g in (x,y)`, and both conjugations
`g^-1 r_i g` and `g r_i g^-1`, locate the exact destination in Gamma and use
the frozen BFS section.  The resulting 26*2*2=104 typed loops are replayed by
the same streaming left-Fox recurrence.  Require all three component scalars
zero.  Export ordered rows and digest.  At least two nonempty loops are also
materialized and checked by direct target6 Fox plus full fixed-prefix
remainder; direct lambda, NF qstar coefficient, and streaming scalar must
agree.

## D. Independently certified complete presentation of Q0

The degree-36 marked Q0 permutations split into disjoint factors of degree 9
and 27.  The exact orders are

```
|P|=504, |G9|=2916, |Q0|=504*2916=1469664.
```

The following GAP-derived factor payload is frozen, but the checker must not
trust its completeness:

```
P_RELATORS =
[[-2,-2,1,1,2,1,2,1,1],
 [1,-2,-2,-2,-2,1,-2,-2,-2,-2],
 [-1,2,-1,-2,-1,-1,-2,-2,-1,-1,-2],
 [2,1,1,2,-1,2,-1,-1,2,-1,-1,2,-1],
 [-1,-2,-1,-1,-2,1,2,1,1,1,-2,-1,-1,-1]]

G9_RELATORS =
[[1,2,2,-1,2,2],
 [2,-1,-1,-2,-1,-1],
 [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
 [2,1,-2,-2,-2,-2,-2,-2,-2,-2,1,2,1,-2,-2,-2,-2,-2,-2,-2,-2,1],
 [1,2,1,2,-1,-2,-1,-2,-1,-2,1,2,-1,-1,-1,-1,2,1,2,1,2,1,2,1,2,1,2,1,2,-1,2,1,1,1,1,2,-1,-2],
 [-1,-1,-1,2,1,2,-1,-2,-1,-2,-1,-2,-1,-2,-1,2,1,2,1,-2,-1,-1,-1,-2,1,-2,-1,-2,-1,-2,-1,-2,-1,-2,-1,-2,1,-2,1,-2],
 [1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1,1,-2,-1,-2,1,2,1,2,1,2,1,2,1,-2,-1,-2,1,1,1,1,1]]

SPLIT_WORDS =
[[1,-2,1,1,2,-1,-2,-2,1,-2,-1,-1,-2,-1,-1,-2,-2,1,-2,-2],
 [-1,-1,-2,-1,-1,2,1,2,1,1,2,1,2,2],
 [1,2,2,-1,2,2,1,1,2,1,1,2,-1,2,2,1,-2,-1,-1,2,-1],
 [-2,-2,-1,-2,-1,-1,-2,-1,-2,1,1,2,1,1,2]]
```

Payload SHA-256 under canonical JSON is
`6eb95a6830b19e729c5e2a9b4f861fb6105ac0be1f1058cc566898d1b48758ba`.

Producer independently enumerates the two permutation factors and gates the
orders, split-word images `(P-generator,1)` / `(1,G9-generator)`, and the
degree-36 direct-product order.

Checker reconstructs the same marked factors from q3 and uses SymPy's own
finitely-presented-group coset enumeration to require the P and G9
presentations have exact orders 504 and 2916.  It also independently evaluates
every factor relator and split word in the permutation factors.  This is the
cross-check of the GAP-derived finite presentations.

Build 19 exact relators in F2:

- 5 P relators after substituting the first two split words;
- 8 G9 relators after substituting the last two split words;
- four cross commutators between the P and G9 split generators;
- two equations `x=px*gx`, `y=py*gy`.

The factor presentations, cross commutation, and splitting equations prove the
19-relator group has order at most 504*2916; its marked surjection to Q0 proves
it is exactly Q0.  Require 19-relator digest
`dcb8ce42c8324b0ce2a5018007f3d664da5568ee73182758a9f358deba84bc2a`.

Evaluate every relator in the joint context group, locate its Gamma section,
and form a typed loop.  The 19 images must normally generate all 243 Gamma
states.  Require all three Fox-potential components zero.  Export ordered rows
and digest.  Materialize at least two independent nonempty relation loops for
direct Fox/NF canaries.

## E. Presentation theorem and terminal meanings

The producer and checker each reconstruct the following finite presentation
argument, never accepting a Boolean imported from the other:

1. section-edge relations present Gamma exactly (full 243-state Cayley graph);
2. the 104 relations specify the x/y action on Gamma;
3. the complete 19-relator Q0 presentation lifts with Gamma-valued defects;
4. those defects normally generate Gamma;
5. hence these relations present the full marked image of
   `Q0 x E3 x E4^31`, and their zero component discrepancies imply
   `A=B=C=0` on K;
6. therefore `mu(K)=0`, while lambda(base)=2.

Terminals:

- `B345_JOINT_KERNEL_QSTAR_CLOSED`: all exact gates above pass.  Claim is only
  the fixed-prefix whole-joint-kernel obstruction.
- `B345_JOINT_KERNEL_QSTAR_ACTIVE`: a lexicographically first nonzero defining
  relation exists and is independently direct/NF replayed.  This is a positive
  new direction, not a lift or 33-target PASS.
- `B345_JOINT_KERNEL_QSTAR_UNKNOWN_RESOURCE`: only registered resource caps.
- `B345_JOINT_KERNEL_QSTAR_UNKNOWN_INPUT`: only authenticated external
  input/pin/schema failure.

No negative/global/full-D2/full-H3/B4 claim is permitted on any terminal.

## F. Receipt and checker

Use exact terminal-aware top-level and nested keysets.  At minimum bind:

- all source/task/q3/157ed pins and hashes;
- qstar/base/prefix/raw-lambda reconstruction;
- 26 record manifest and exact word digest;
- Gamma states, edges, BFS sections, group invariants, state/transition digests;
- all 6318 edge discrepancy rows or a lossless packed typed-array encoding;
- all 104 action rows and direct/NF canaries;
- factor payload, custom permutation enumeration, independent SymPy order
  results, 19-relator manifest and completeness proof fields;
- all 19 lifted-relation rows and direct/NF canaries;
- theorem-boundary flags and runtime/resource accounting.

Checker rebuilds all mathematical objects from q3 and the pinned sources.  It
must not import producer state IDs, sections, potentials, gradients, or lambda
tables.  Public IDs are checked only after canonical blob equality.

## G. Self-test, driver, and runtime

The combined self-test must exercise shared production validation helpers on a
small nonabelian extension fixture.  It must reject mutations of:

- Gamma order/transition/section and an internal edge discrepancy;
- x/y action orientation and a nonzero action component;
- factor order, factor relator, split word, cross commutator, and a missing
  Q0 relation;
- qstar/base sign and a relation scalar;
- CLOSED/ACTIVE/RESOURCE/INPUT claim boundaries and extra schema keys.

The driver pins producer/checker/task/predecessor hashes, runs q3 in the same
isolated child as 157ed, uses pipefail+tee and exact-one markers, and gives the
producer and checker one shared 18000-second budget under a 330-minute job.
Self-test mode does not run q3 or the full prefix.

Expected full runtime after implementation: producer 3--6 minutes, checker
4--8 minutes including the independent factor coset enumerations, same-job
normally 8--15 minutes; conservative 20--35 minutes.  Expected RSS remains
prefix-dominated around 0.8--1.2 GiB.  Any larger regression is a STOP for
profiling rather than a reason to widen caps.
