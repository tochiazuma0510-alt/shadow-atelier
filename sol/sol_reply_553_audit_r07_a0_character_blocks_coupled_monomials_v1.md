# Task 553 audit — first-rung character blocks with coupled monomials

This is a mathematical/static audit.  The character-only decomposition is
correct after one local repair to its source-word justification.  The issue is
not the Fourier algebra: v442 proves that its displayed complement elements
are pure sign in the `G9` factor, but it does not prove that the same displayed
free words have trivial `PSL(2,8)` coordinate.  Thus v446 cannot obtain
`L_(1,a)` from that citation alone.  The exact pure-`Q1` words already
cross-checked at the order-2016 floor give a fail-closed replacement, and an
arbitrary first-rung kernel coordinate in those lifts acts trivially on the
associated grade.

No Python, GAP, git, GHA, es7ops, or other agent was used for this audit.  In
particular, no new runtime, rank, exhaustion, or membership result is claimed.

## 1. Dependency pins and status

I read the commissioned chain in full.  The byte counts and SHA-256 values
recomputed from the files are:

| input | bytes | SHA-256 |
|---|---:|---|
| v441 | 11,696 | `5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb` |
| v442 | 8,710 | `afa91b6137f8321522cf97fa11502213bde45c7c4c325b3b2ad28e8f6e844de4` |
| Task 548 reply | 14,448 | `bd1b0239e0410f2ab63abd30e7ff9a422528d141138cfeafc8ca3960da1cd834` |
| v443 | 10,291 | `80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c` |
| v444 | 9,953 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| v445 | 9,670 | `98d073c896cae8304252327ea285b876f8868b6c2d00e8ba3c00465ea86612e7` |
| final Task 550 reply | 20,221 | `329aa9b8c8b87e5672938cb70ab99dbf365b59a0e63468a3df58420ee26e4616` |
| v446 | 9,262 | `389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756` |

The final Task 550 identity above supersedes its transient 20,226-byte
version.  Its corrected finite run remains candidate telemetry with
independence status `UNKNOWN`, because it briefly overlapped an unrelated
local Python process.  None of its counts is a premise below.

For the exact marked-word repair in Section 2, I also rebound the previously
completed Task 549 audit: 13,003 bytes, SHA-256
`a088d27203e2064ac8240b813fd15e905ec82633b93b829e89b4a073f111256c`.
That audit independently enumerated the marked order-2016 quotient and
replayed exact pure-`A` words in both factors of `Q1=P x A`.

## 2. Legality of the four character projectors

### 2.1 What v442 proves, and what it does not

With the right-action law

\[
 (r,e)\star(s,f)=((-1)^f r+s,e+f),
\]

v442 defines

\[
 s_X=X^9,\qquad s_Y=t_1t_2^{-1}t_3Y,
 \qquad t_1=X^{10},\ t_2=Y^{10},\ t_3=(XY)^{10}.
\]

Its direct affine calculation gives zero rotation coordinate for both
`s_X` and `s_Y`.  Their four products therefore have zero coordinate in the
first-rung kernel `V=N/N^3` and realize the four elements of the sign
complement inside `G9`.  Task 548 independently audited that `G9` statement.

There is nevertheless a factor mismatch in the sentence after v446 (2.1).
The displayed source expressions in v442 are evaluated there only under
`x -> X`, `y -> Y`.  In the full marked quotient the same word has an
additional `P` endpoint.  Zero `G9` rotation does not force that endpoint to
be `1_P`.  In particular, v442/Task 548 do not record a `P`-endpoint check for
the word

\[
 x^{10}y^{-10}(xy)^{10}y
\]

representing `s_Y`.  Without such a check it gives at most an operator
`L_(p,a)` for an unspecified `p`, not the required `L_(1,a)`.  The special
word `s_X=x^9` is separately known to be `P`-pure from the order-2016 audit,
but that does not repair the second generator.  Consequently the cited v442
words alone do not establish v446 (2.2).

This is a proof/certificate gap, not a finding that the `s_Y` word has a
nonidentity `P` endpoint.

### 2.2 Exact replacement using marked pure-`Q1` words

Use the independently replayed representatives from Task 549.  With letter
encoding `1=x`, `-1=x^-1`, `2=y`, `-2=y^-1`, they are

```text
a=(0,0): []
a=(0,1): [-2,-2,-2,-2,-2,-2,-2,-2,-2]
a=(1,0): [-2,-2,1,1,2,1,2,1,1]
a=(1,1): [-2,-2,-2,-1,-2,-1,-1,-1,-2,-1]
```

Each word is a legal word in the registered actors
`x,x^-1,y,y^-1`, and its exact `Q1` endpoint is `(1_P,a)`.  The same audit
enumerated 2,016 marked states, so these actors generate the registered
`Q1=P x A`; this is not an external ambient coordinate projection.

Let the lift of such a word to `Q2` be

\[
 d_a=\sigma(1_P,a)n(v_a),
\]

where no assertion that `v_a=0` is needed.  If `f` is homogeneous of degree
`d`, the exact v443 left-action formula gives

\[
 L_{d_a}([p,b]f)
 =[p,a+b]E(S(b)v_a)f
 \equiv [p,a+b]f\pmod {I^{d+1}},                 \tag{2.1R}
\]

because `E(S(b)v_a)-1` has positive augmentation degree.  Thus these exact
source words induce the required associated-grade operators

\[
 T_a=L_{(1,a)}.                                    \tag{2.2R}
\]

This also respects the occurrence-source correlations.  In tag `j`, the
same word has quotient `(1,A_j a)` (and may acquire the crossed kernel term
`c_j(a)`), so it projects onto the transported character
`lambda o A_j^-1`; the crossed kernel term again has constant term one on
the pure grade.  The one legal word acts simultaneously on all six tags and
both Fox components.  No tagwise or Fox-componentwise ambient projection is
being inserted.

Accordingly, the exact replacement for the offending sentence after v446
(2.1) is:

> The exact marked pure-`Q1` words listed in (2.1R) have endpoints
> `(1_P,a)`.  Their possibly nonzero first-rung kernel coordinates disappear
> on the associated grade by v443 (3.1), so their legal correlated actions
> give every `T_a=L_(1,a)`.

The corresponding replacement for certificate gate 7.4 is: bind each exact
word, its literal endpoint `(1_P,a)` in `Q1`, and its correlated six-tag/two-
Fox action.  Alternatively, a producer may use zero-kernel complement words
only after directly binding both their `P` and `G9` endpoints; a `G9`-only
complement check is insufficient.

### 2.3 Fourier identities and the exact submodule equality

Write `A` additively and define

\[
 e_\lambda=\sum_{a\in A}\lambda(a)T_a.
\]

Since `4=1` in `F3`, the usual coefficient `1/|A|` is exactly one.  Also
`a=-a` and every character value is its own inverse.  For `c in A`, the
coefficient of `T_c` in a product is

\[
 [T_c](e_\lambda e_\mu)
 =\sum_a\lambda(a)\mu(c-a)
 =\mu(c)\sum_a(\lambda\mu)(a).
\]

The last character sum is `4=1` if `lambda=mu` and zero otherwise.  Hence

\[
 e_\lambda e_\mu=\delta_{\lambda\mu}e_\lambda.
\]

Similarly, character orthogonality gives

\[
 \sum_\lambda e_\lambda=T_0=1.
\]

These are central operators for the associated-grade `Q1=P x A` action,
and, by (2.2R), they lie in the algebra generated by legal source words.

Let `D_d` contain every seed and transition defect and let

\[
 H_d=k\langle Q_1\rangle D_d.
\]

Legal actor stability gives
\(e_\lambda H_d\subseteq H_d\).  The sum-to-one identity gives
\(H_d=\sum_\lambda e_\lambda H_d\), and orthogonality makes the sum direct:

\[
 \boxed{H_d=\bigoplus_{\lambda\in\widehat A}e_\lambda H_d}. \tag{2.3R}
\]

Because `T_a` is the single correlated source action described above, this
equality applies to the complete six-tag, two-Fox occurrence module.  It is
strictly stronger than ambient character invariance and does not authorize
any independent manipulation of a tag, Fox component, or monomial.

## 3. Monomial non-splitting

On a fixed source-character sector, associated-grade left translation has
the form

\[
 L_\ell\bigl(r\otimes u^\alpha\bigr)
 =\lambda(a_\ell)L_{p_\ell}(r)\otimes u^\alpha.       \tag{3.1}
\]

The regular operator and scalar may depend on the actor (and, in occurrence
coordinates, on the tag), but the operator on the multiplicity factor
`k B_d` is the identity.  Occurrence maps later transport
`alpha -> pi_j alpha`; that transport is not a source actor-algebra
projector onto an individual `alpha`.

For the direct counterexample, let `R` be any actor module, take nonzero
`r in R`, and use two invariant multiplicity vectors `m_1,m_2`.  The legal
closure of

\[
 z=r\otimes(m_1+m_2)
\]

is

\[
 (k\langle Q_1\rangle r)\otimes k(m_1+m_2).
\]

It need not contain either \(r\otimes m_1\) or \(r\otimes m_2\).  Replacing `z` by
its two coordinate projections changes a diagonal copy into a direct sum and
can enlarge the legal correction space.  Thus an invariant ambient direct
sum does not imply that a generated submodule is closed under its coordinate
projections.

V446 (3.1)--(3.4) withdraw exactly the unsafe `4h_d` source-block inference
from v445.  Its algorithm projects only the complete defect by the four
legal character idempotents, then retains the entire monomial tuple while
closing each character block.  No additional repair is needed here.
Task 550's finite substitutions and counts are at most candidate
corroboration; the module argument above is load-bearing.

## 4. Dimensions and transition-defect completeness

The degree-one monomials are `u_1,u_2,u_3`, so

\[
 h_1=[t](1+t+t^2)^3=3.
\]

For one character the occurrence coordinates are

\[
 6\ \text{tags}\cdot2\ \text{Fox components}\cdot504\ \text{PSL states}
 \cdot3\ \text{monomials}=18,144.
\]

Therefore the four-character total is

\[
 4\cdot18,144=72,576,
\]

and the joint physical grade has

\[
 4\cdot |Q_1|\cdot h_1=4\cdot2,016\cdot3=24,192
\]

coordinates.  These are ambient widths, not ranks or memory/runtime
guarantees.

Read with its opening requirement to retain the *complete* old exhausted
basis and all four transition tables, v446 Section 4 is an exact
specialization of v444:

1. its step 1 includes every original seed relation and the transition of
   every old basis row under each of `x,x^-1,y,y^-1`;
2. step 2 uses the same deterministic lower reduction and the same row
   coefficients on the lift, so both seed defects and actor-transition
   defects have zero lower part;
3. step 3 keeps the full monomial tuple and literal instruction-tree
   ancestry;
4. after the repaired legal realization in Section 2, step 4 decomposes the
   defect set without changing its span;
5. step 5 exhausts the legal actor closure in each complete character block;
   and
6. step 6 retains a spanning basis and ancestry for the physical stage.

The v444 direct-sum proof then gives

\[
 U_{d+1}=\operatorname{span}\{\widetilde b_i\}\oplus H_d.
\]

Seed defects recover lifted dependencies, and transition defects recover
the failure of the chosen old lifts to be actor-stable.  Omitting either
family can lose kernel directions.  With all of the records above, there is
no lost-kernel step and no enlargement of the legal source orbit: the
algorithm reuses the exact old orbit presentation and closes only the
defects required by v444.  Projecting a full defect and then closing the four
orthogonal summands is exact by (2.3R).

This statement is conditional on possession of the complete old transition
presentation.  As Task 550 records, the present Task 542 artifact retained a
particular positive correction, not that full presentation.  A first
implementation must therefore either perform one complete order-2016 pass
that stores all seed reductions and four transitions for every basis row, or
perform the complete degree-one construction from the 44 seeds and begin
transition reuse only thereafter.  This is an implementation prerequisite,
not evidence of a mathematical restart in v446 and not a computed
exhaustion claim.

## 5. Physical fibre and actual-row hypergraph

A row in one character block may contain several monomials.  Under the six
occurrences, its individual coordinates obey

\[
 (\lambda,\alpha)\longmapsto
 (\lambda\mathbin\circ A_j^{-1},\pi_j\alpha),
\]

so the aggregate of the whole row may meet several vertices, including
vertices in distinct components of the old coordinate-transport graph.
That graph alone cannot split the physical solve.

Let `F` be the complete occurrence-to-physical aggregation and let `r` be
physical reduction to the lower precision.  Since v444 gives

\[
 U_{d+1}=\operatorname{span}\{\widetilde b_i\}\oplus H_d,
\]

the aggregates of all old lifts together with a basis of every exact
`e_lambda H_d` span `F(U_{d+1})`.  A joint lower-first echelon on this entire
roster therefore returns exactly

\[
 F(U_{d+1})\cap\ker r,
\]

the complete physical fibre used by v441.  It is not merely the image of
corrections visibly divisible by `I^d`: dependencies among the lower parts
of old lifted rows can create additional zero-lower grade connection rows,
and v446 explicitly retains them.

Both alternatives in v446 are exact, subject to the stated construction:

* one joint 24,192-coordinate lower-first fibre is unconditionally safe;
* a split is safe only after forming a hypergraph on the target
  `(lambda,alpha)` vertices and adding the nonzero support of **every**
  aggregated basis row from the coupled-defect blocks and **every**
  zero-lower connection row produced by joint reduction of the old lifts.

Every spanning row is then contained in one connected component, so the
span is the direct sum of its componentwise spans.  This proves sufficiency
of the completed actual-row hypergraph.  Omitting either family of
hyperedges, using only the permutation-routing graph, or discarding old
lifts before joint lower-first elimination is unsound.

The terminal gates are correspondingly correct:

* `MEMBER` requires membership in this exhausted complete fibre, stored
  coefficients and literal ancestry, zero lower change in every registered
  auxiliary coordinate (including PB3 augmentation), zero normalized
  exponent, and a direct precision-one replay;
* `NONMEMBER` requires a dual on the complete registered coordinate system
  that annihilates every coupled-defect aggregate and every lifted-old
  connection row, pairs nontrivially with the residual, and is accompanied by
  complete source-closure and aggregation receipts;
* any absent transition, closure, row family, hyperedge, ancestry, or replay
  forces `UNKNOWN`.

Neither alternative has yet been executed.  A future terminal concerns only
the first positive grade of the first rung.

## 6. Equation findings, residual risks, and exact implementation contract

| v446 item | finding |
|---|---|
| (1.1)--(1.4) split grade and widths | PASS |
| (2.1) associated-grade action | PASS |
| sentence citing v442 words as `L_(1,a)` | REPAIR REQUIRED: `G9` purity does not bind the `P` endpoint |
| (2.2) idempotents | PASS after (2.1R)--(2.2R) |
| (2.3)--(2.4) character decomposition | PASS after the same repair |
| (3.1)--(3.4) monomial non-splitting | PASS |
| Section 4 transition construction | PASS conditionally on the complete retained presentation |
| (5.1) transport versus row support | PASS |
| (5.2) joint physical width | PASS |
| Section 6 terminal trichotomy | PASS; not run |
| Section 7 certificate boundary | PASS after replacing gate 7.4 as above |

The safe executable contract is therefore:

```text
LOWER STATE: complete old basis, every seed reduction, and all four
             transition records, all with word-bearing ancestry
PROJECTORS:  exact pure-Q1 source words with endpoints (1_P,a);
             apply each word as one correlated six-tag/two-Fox action
SOURCE:      four character blocks of width 18,144 at degree one;
             retain all three monomials coupled
CLOSURE:     exhaust legal actors in each full character block;
             do not import Task550 candidate ranks as exhaustion evidence
PHYSICAL:    joint width 24,192, or a sealed actual-row hypergraph containing
             every coupled-defect row and every old-lift connection row
TERMINAL:    direct MEMBER replay or complete NONMEMBER dual; otherwise UNKNOWN
AUXILIARY:   retain PB3 augmentation, normalized exponents, all occurrence
             tags, and every other coordinate registered by v441
```

The remaining risks are implementation/certificate risks: the complete
old transition presentation is not yet persisted, the physical actual rows
do not yet exist, and no first-grade residual test has run.  The local repair
above settles the paper-level projector realization without asserting that
v442's `s_Y` word is or is not `P`-pure.

## 7. Claim boundary and verdict

The repaired equality (2.3R) is a statement about the exact generated
associated-grade module.  It gives no rank, runtime, queue-exhaustion, or
membership result.  Task550's overlapped finite run remains `UNKNOWN` as
independent evidence and is not promoted.  Nothing here advances the
order-2016 literal MEMBER beyond its already audited status, completes the
order-54,432 rung, or supplies a cofinal compatible lift or Lean proof.

FIRST_RUNG_CHARACTER_BLOCKS_PASS_AFTER_REPAIR

FIRST-GRADE MEMBERSHIP: NOT COMPUTED

ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED

verified=false
