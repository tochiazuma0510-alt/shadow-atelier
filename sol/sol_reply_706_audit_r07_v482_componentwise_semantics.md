# Sol(max) Task706: v482 componentwise P1 semantics audit

## Verdict

`verified=false`

The componentwise factorization is mathematically sufficient and matches the
Task554 generation equations.  It does not require a resident
`8059 x 96776` family or a preassembled global coefficient row.  No missing
character block, packet equality half, auxiliary coordinate, actor relation,
or sign reversal was found.

`PASS_COMPONENTWISE_P1_SEMANTICS`

This is a paper/static verdict only.  It does not accept the current
structural producer, perform the five-artifact equality replay, replace an
independent checker, or discharge any grade-two computation.

## Exact audited inputs

| path | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_706_audit_r07_v482_componentwise_semantics.txt` | `1723` | `9` | `b5dfd25ac666c7a409852302593253ec7c6dd718fd73f780c6632a9e2c321711` |
| `sol/proof_r07_grade2_p1_componentwise_semantic_replay_v482.md` | `7343` | `162` | `f8a8684544bcc125c075b59ff793041906aa9bb53cfff0d223166a4894597a92` |
| `sol/proof_r07_grade1_to_grade2_split_presentation_handoff_repair_v451.md` | `8050` | `229` | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| `sol/proof_r07_grade2_lazy_presentation_interface_v480.md` | `7981` | `228` | `46b917a2e353951b0a345f3469c1e145408f31d0a53933241b2cf9ef438ddcea` |
| `sol/proof_r07_grade2_p1_disjoint_lead_completion_v481.md` | `4548` | `123` | `462b74a314ed29fcb028910a02a0c9bf4bf3daeb481657448a21981ec390f9c4` |
| `search/d972_r07_a0_first_rung_grade1_v4.py` | `144552` | `3326` | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |

All six inputs have a final LF.

## Load-bearing algebra and signs

For one old origin `o=(chi,u)`, write its directly recomputed P1 value as

```text
D[o] = (D_L[o], (D_G[o,lambda])_lambda).
```

Let `q[o,i]` be the exact `seed_reductions` or `actor_transitions`
expression from the owning old `chi` block.  The two old-row checks and the
two halves of every packet/block check are precisely

```text
D_L[o] = sum_i q[o,i] ell[chi,i],
d[o,lambda]
  = D_G[o,lambda] - sum_i q[o,i] g[chi,i,lambda],
d[o,lambda] = sum_j R[lambda,o,j] h0[lambda,j].       (1)
```

Consequently

```text
D[o]
 = sum_i q[o,i] b[chi,i]
   + sum_lambda,j R[lambda,o,j] h[lambda,j].          (2)
```

The signs in (1)--(2) are forced by the actual producer.  `PackedEchelon`
reduces a candidate as `z-sum c_p b_p`; `expression_from_insert` records the
positive reconstruction coefficients, including the accepted normalized
pivot coefficient.  The prepare packet loop starts from the direct grade
value and subtracts the same old-lift coefficients.  `run_block_core` then
records the positive expression reconstructing that packet from the new
block basis.  Therefore v451 (2.4)--(2.6) has a plus sign on every `R` term.

In v482's table, “direct grade defect component” is thus necessarily the
post-subtraction residual in the middle line of (1), as already fixed by its
Section 1 definition and Theorem 3.1 proof; it is not the raw
`D_G[o,lambda]`.  Under that binding, both required authentication/equality
halves are present:

1. recompute the residual from the direct value and the authenticated
   `q`/old companions, then compare it byte-for-byte with packet row `o`;
2. independently recompute `sum_j R[lambda,o,j] h0[lambda,j]` from the
   authenticated block basis and compare it with that same packet row.

A future implementation that compares the raw `D_G` directly with the
packet, or checks only one side against a digest, would not implement v482.
That is an implementation gate, not a defect in the stated factorization.

## Indices, counts, and exhaustion

The old character `chi`, pure-grade character `lambda`, and actor slot `t`
are distinct indices.  Both character orders are
`((0,0),(0,1),(1,0),(1,1))`, and the actor order is
`(1,-1,2,-2)`.  With v451's origin offsets,

```text
o_seed(chi,a)    = D_chi + a - 1,
o_actor(chi,i,t) = D_chi + 44 + 4*i + t,
D_chi            = (0,2064,4120,6176).
```

The prepare loop writes every resulting origin at that same row index into
each of the four ordered lambda packet blobs.  `run_block_core(lambda)` reads
exactly its corresponding packet and stores all `origin_reductions`; its FIFO
closure stores four actor transitions for every accepted new row.  Hence the
counts are exact:

| family | indexed obligations |
|---|---:|
| projected-seed lower | `4*44 = 176` |
| old-row actor lower | `4*2014 = 8056` |
| packet/block compound checks | `4*8232 = 32928` |
| new-row actor | `4*6045 = 24180` |
| total compound local obligations | `65340` |

Each of the 32,928 packet entries contains both binary comparisons in (1).
Thus an implementation counter that counts binary comparisons rather than
indexed compound obligations will count 65,856 packet comparisons and
98,268 comparisons overall; this is only a receipt convention, not an extra
mathematical family.

The 2,014 old DAG identities reconstruct the coupled lower/grade rows via
`close_lower_block` and `evaluate_old_lifts`; the 6,045 block DAG identities
reconstruct the pure-grade rows from packet or prior-actor origins.  Their
stored scale and strictly prior reductions give the exact v451 (2.7)
identity.  They are prerequisites in addition to the 65,340 local
obligations, not consequences of lead independence.

For a fixed seed `a`, summing (2) over the four `chi` gives the one global
seed relation because the exact filtered identity is

```text
sum_chi P_chi = 4*L_empty = 1  over F3.
```

No idempotence or pairwise orthogonality of the full filtered `P_chi` is used.
The 8,056 old-row actor instances already give their global relations one at
a time.  The 24,180 new-row actor instances are global because a pure-grade
row and `associated_grade_actor` both stay inside the same genuine
`V1[lambda]` summand.  These exhaust
`44 + 4*(2014+6045) = 32280` global P1 relations.

## Direct sums, Aux, and streaming

The only decomposition used to reassemble (2) is

```text
P1src = L direct_sum (direct_sum_lambda V1[lambda]),
L     = (direct_sum_chi V0[chi]) direct_sum Aux.
```

The four subspaces `V0[chi]+Aux` are not asserted to be mutually direct:
their auxiliary coordinates are shared.  Each old lower equality is taken
inside the common `L`, and the four projected-seed equalities are added there.
Likewise, no old grade companion is treated as character-local;
`g[chi,i,lambda]` is subtracted for all four `lambda` in (1).  Only new rows
are supported in one pure-grade block.

Equation (2) is an equality of finite sums, so it can be checked one lower
slice and one lambda component at a time.  Seed coefficients with the same
global key may be combined modulo three as a stream; no resident length-8,059
coefficient row is needed merely to prove the equality.  The next grade-two
consumer will still have to regenerate those exact coefficient streams on
demand when forming its degree-two defects.  V482 does not waive that later
work.

V481's distinct normalized leads separately establish rank 8,059.  They do
not prove any equation above, and v482 says so explicitly.  Conversely, the
componentwise theorem neither authenticates the current five artifacts nor
claims actual equality.  Required next gates remain the producer replay, a
separately implemented checker that reopens the raw inputs, every degree-two
lift/truncation and defect, all 8,059 connection offers, and the fresh rho2
MEMBER/NONMEMBER decision.  A0, COMMON, cofinal lift, fake, Ihara, and Lean
verification remain undeclared.
