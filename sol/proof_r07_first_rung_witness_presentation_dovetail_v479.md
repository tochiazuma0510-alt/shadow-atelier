# R07: dovetailing explicit witnesses with transition presentations through the first rung (v479)

Author: Sol / 2026-09-03

Status: candidate scheduling theorem.  It separates the word-bearing branch
needed to compute the next residual from the target-independent transition
presentation needed to decide that residual.  This permits the two branches
to run concurrently at grades two through six without weakening any v441,
v444, v449, v465, v469--v471, v474, v478 or Task630 gate.  It proves no new
MEMBER terminal, order-54,432 solution, A0, compatible cofinal lift, fake or
Ihara conclusion.  `verified=false`.

## 1. Exact parents and the point of the separation

The load-bearing parents are:

| input | bytes | SHA-256 |
|---|---:|---|
| v444 transition defects | 9,953 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| v449 six-grade index repair | 1,408 | `0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9` |
| Task555 six-grade audit | 14,309 | `8dcdfbb4825c65bff9698311b735e830c27d39f98405bcfb01af3411d97a2e45` |
| v465 selected-ancestry SLP | 9,801 | `b779fca02449a1e4465bf0a29f7da8388f4c2e32c28a6f959e8c50189f2c7693` |
| v469 typed physical replay | 8,865 | `bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6` |
| v470 leaf-gated replay | 8,731 | `b56aa15ee87b4831cc999525233cfadbe8e62cd25c0503c0c98fce3106fb2b7a` |
| v471 endpoint signatures | 8,819 | `38d271514baf838953b6003f954be60c689771f0fd1c9fec14de1dfc55daf99f` |
| v474 targeted grade-two decision | 12,755 | `a0ae668799de33d79b5e80ca2a6b7b50224770528b1201d8fb999506757c08c9` |
| v478 eleven-to-six typing | 5,131 | `a7e5df7f14d35b7dc971127e187fbc16abe00b3b5190fac341666b94bbf1e72b` |
| Task639 selected-SLP acceptance | 10,104 | `b48fe4bfb43aedb76c9109e2ca73e7a9de323687c69c64807e74f3ad62db0a1b` |

V449 packages a successful precision-$d$ state as a transition
presentation together with a target solution.  These two parts have
different dependency graphs.  The **module presentation** is determined by
the seed roster, four actors and occurrence maps; the **witness root** is
determined by one result-dependent MEMBER ancestry.  Combining them in one
artifact is convenient but is not an algebraic dependency.

The distinction matters for v474.  A target-directed CEGAR run may find a
MEMBER expression before it has materialized a complete primal source basis.
That expression is sufficient to build the next explicit word and residual,
but it is not by itself the complete transition presentation required by
v444 at the following grade.

## 2. Two authenticated objects at precision d

Let


\[
 k[V]=\mathbf F_3[u_1,u_2,u_3]/(u_1^3,u_2^3,u_3^3),
 \qquad I=(u_1,u_2,u_3).
\]

For $0\le d\le6$, separate:

1. $\mathcal P_d$, the target-independent presentation of the complete legal
   occurrence module $U_d$.  It consists of a deterministic basis with
   literal ancestry, all 44 seed reductions, all four actor transitions of
   every basis row, and every registered auxiliary coordinate.
2. $C_d$, the exact canonical source SLP which solves the registered target
   through degree $d$, together with its selected dependency graph, three
   root order, typed physical replay and current-quotient leaf/signature
   receipts.

The construction of $\mathcal P_d$ from $\mathcal P_{d-1}$ is v444/v449:

\[
 U_d=\operatorname{span}(\widetilde B_{d-1})
       \oplus H^{[d]},
 \qquad H^{[d]}=H_{d-1}^{\mathrm{v444}}.             \tag{2.1}
\]

It uses no target residual and no chosen correction.  Conversely, once a
MEMBER certificate at grade $d$ supplies a selected exact update

\[
 \Delta C_d,
\]

v465 and v469 define

\[
 C_d=\operatorname{Compose}(C_{d-1},\Delta C_d)      \tag{2.2}
\]

after direct lower/auxiliary zero and grade-$d$ replay.  This construction
uses only the selected ancestry needed for that MEMBER expression; it does
not require completion of every unused primal orbit row.

Thus neither object is a substitute for the other.  A selected word without
$\mathcal P_d$ cannot decide the next residual, while a complete
$\mathcal P_d$ without $C_d$ does not determine the result-dependent next
residual.

## 3. Degree-independent leaf and endpoint theorem

Assume every fully expanded literal of $C_d$ is an exact conjugate

\[
 P r_s^{\epsilon}P^{-1},
 \qquad 1\le s\le44,\quad \epsilon\in\{1,-1\},       \tag{3.1}
\]

in the authenticated noncommutative dependency graph.  For each of the
eleven Task630 occurrences $j$, assume the executable base gate

\[
 \eta_j\theta_j(r_s)=1                               \tag{3.2}
\]

for every reached seed.  Then, in the full group algebra and hence in every
truncation through degree $0\le e\le6$,

\[
 D_{\eta_j\theta_j}(C_d)
   =\sum_{s,P}\mu_d(s,P)\,
      \eta_j\theta_j(P)D_{\eta_j\theta_j}(r_s).      \tag{3.3}
\]

Indeed (3.2) puts every factor (3.1) in the endpoint kernel, where the Fox
derivative is additive, and

\[
 D(Pr_sP^{-1})=\eta_j\theta_j(P)D(r_s),\qquad
 D(Pr_s^{-1}P^{-1})=-\eta_j\theta_j(P)D(r_s).
\]

This is the v470 proof without a precision-two specialization.  Truncation
is applied only after the exact group-algebra identity, so no new
degree-dependent premise appears.

Define the same complete typed signature at every first-rung degree,

\[
 \Sigma_{11}(P)=
  (\eta_j\theta_j(P))_{j=1}^{11}\in E_3^6\times E_4^5. \tag{3.4}
\]

Grouping (3.3) by equal $(s,\Sigma_{11}(P))$ is therefore exact at every
degree.  The first-six restriction is licensed only after the complete
eleven-slot receipt and direct all-seven canary, exactly as in v478/Task630.
The five P slots remain source receipts and are not declared zero.

When (2.2) appends a new selected update, retain the old and new source DAGs
under the ordered `Compose` root.  At the derived evaluation layer only,
the new exact leaf map is the mod-three sum of the two exact maps.  An
accepted trie may be extended by the new exact paths; the endpoint of every
old path is unchanged because the eleven occurrence maps are unchanged.
New/old equal path keys may cancel in the derived map but no source edge is
deleted.  An independent consumer either replays all paths or authenticates
the immutable preceding table and independently evaluates every newly
inserted trie edge.

## 4. Fresh residual branch does not require the next presentation

Suppose $C_d$ has passed the complete target equality through degree $d$.
The word branch can independently evaluate the same exact root one precision
higher and define

\[
 \rho_{d+1}=\operatorname{gr}_{d+1}
 \left(T_{\le d+1}-
       \mathcal E^{\rm phys}_{\le d+1}(C_d)\right)   \tag{4.1}
\]

after comparing every lower and auxiliary coordinate to zero.  Equations
(3.3)--(3.4) give the bounded explicit evaluator.  Neither
$\mathcal P_d$ nor the grade-$(d+1)$ fibre appears in (4.1).

Let

\[
 (h_0,h_1,\ldots,h_6)=(1,3,6,7,6,3,1),
 \qquad H_e=\sum_{i=0}^e h_i.
\]

For the fresh grade $e=d+1$, the exact dense widths are

\[
 \begin{aligned}
  \text{source through }e&=24{,}192H_e+8,\\
  \text{physical lower/auxiliary}&=8{,}064H_{e-1}+4,\\
  \text{physical top}&=8{,}064h_e,\\
  \text{packed top bytes}&=2{,}016h_e.
 \end{aligned}                                      \tag{4.2}
\]

Consequently the remaining fresh-residual schedule is:

| fresh grade $e$ | source through $e$ | lower/auxiliary | top trits | packed bytes |
|---:|---:|---:|---:|---:|
| 2 | 241,928 | 32,260 | 48,384 | 12,096 |
| 3 | 411,272 | 80,644 | 56,448 | 14,112 |
| 4 | 556,424 | 137,092 | 48,384 | 12,096 |
| 5 | 629,000 | 185,476 | 24,192 | 6,048 |
| 6 | 653,192 | 209,668 | 8,064 | 2,016 |

These are coordinate counts, not ranks or RSS bounds.  Every lower entry is
still compared densely; endpoint signatures do not replace that gate.

## 5. Presentation branch and exact dovetail theorem

In parallel with (4.1), construct the complete target-independent
$\mathcal P_d$ from $\mathcal P_{d-1}$ by (2.1).  This branch must exhaust every seed and
four-actor transition defect, retain full literal ancestry and record all
new seed/transition reductions.  A target-directed MEMBER expression from
v474 does not certify that exhaustion.

### Theorem 5.1 (two-track successor handoff)

For $1\le d\le5$, assume:

1. an accepted $C_d$ with the direct precision-$d$ target replay;
2. an accepted complete transition presentation $\mathcal P_d$; and
3. an independently computed residual $\rho_{d+1}$ from (4.1).

Then the registered grade-$(d+1)$ decision may start, and its legal image
is exactly the lower-first physical fibre constructed from
$\mathcal P_d$.  The computations producing items 2 and 3 have no data
dependency and may run concurrently.  Neither may be omitted at their join.

#### Proof

V444/v449 show that $\mathcal P_d$ presents the complete occurrence image independently of the
target.  V441 then identifies its lower-zero physical fibre with the complete
legal grade-$(d+1)$ correction image.  Separately, v465, v469 and (3.3)
show that (4.1) is the residual of the actually selected word, independently
of how that image is represented.  Hence membership of (4.1) is exactly the
next extension problem.  The two constructions share immutable lower
parents but neither consumes the other's result, proving the concurrency
claim.  At the join, omission of $\mathcal P_d$ could miss legal image rows, while omission of the explicit
replay could test a residual belonging to a different representative.
$\square$

A v474-style result-directed decision is permitted at the join.  On MEMBER
it need export only the full ancestry of the selected expression to form
$\Delta C_{d+1}$; completion of the target-independent presentation for the
following grade remains a separate branch.  On NONMEMBER the witness branch
stops.  Any unfinished closure, replay or resource gate is `UNKNOWN`.

## 6. Concrete present instantiation

Task639 accepts the grade-one selected update root $C_T$ and its canonical
dependency graph.  The current Task630/v478 consumer reconstructs the prior
root and

\[
 C_1=\operatorname{Compose}(C_{<1},C_T),
\]

checks the eleven endpoint/all-seven receipts, compares all 32,260 lower
coordinates, and is intended to emit the 48,384-trit $\rho_2$.  This is the word branch of Theorem 5.1 for $d=1$.

The grade-one prepare/four-block states and v451 determine the independent
module-side input.  V474 is a legal targeted decision for the resulting
grade-two fibre, but a grade-two MEMBER from that target-directed path must
not be mislabeled as a complete $\mathcal P_2$.  After such a MEMBER, the
next explicit root and $\rho_3$ may be produced while full $\mathcal P_2$
completion runs separately.

This exact split repeats through grades three to six.  Six accepted MEMBER
updates with direct replays imply equality at order 54,432 because
$I^7=0$, as already audited in Task555.  It does not imply the second rung
or any cofinal lifting theorem.

## 7. Executable receipt boundary

At every successor join, require two disjoint parent blocks:

1. **witness block:** prior and selected DAGs, exact root order, literal leaf
   map, eleven endpoint gates, complete typed signatures, direct all-seven
   canary, dense lower equality and fresh residual; and
2. **presentation block:** complete basis ancestry, all 44 seed reductions,
   four actor transitions per basis row, exhausted defect closures, auxiliary
   coordinates and lower-first fibre construction.

The checker must reject a target-directed partial span presented as block 2,
or an old stored `next_residual` presented as block 1.  Parent hashes and
accepted receipts may be reused, but self-promotion remains forbidden.

```text
GRADE-ONE EXPLICIT SLP PARENT:             ACCEPTED (TASK639)
GRADE-ONE -> FRESH RHO2 CONSUMER:          IMPLEMENTATION IN PROGRESS
WORD BRANCH / PRESENTATION BRANCH SPLIT:    PAPER-CLOSED IN THIS CANDIDATE
SAME ELEVEN SIGNATURE FOR GRADES 2--6:      PAPER-CLOSED UNDER ENDPOINT GATES
TARGETED MEMBER = COMPLETE PRESENTATION:    FORBIDDEN
REMAINING GRADE MEMBERSHIPS:                NOT DECIDED
ORDER-54,432 / SECOND RUNG / FULL A0:        NOT DECIDED
COMPATIBLE COFINAL LIFT / COMMON / FAKE:     NOT DECLARED
IHARA / LEAN VERIFIED:                      NOT DECLARED / false
```

`R07_FIRST_RUNG_WITNESS_PRESENTATION_DOVETAIL_V479_CANDIDATE`
