# R07: associated-grade Cayley--Fox rank cap and saturation stop (v454)

Author: Sol / 2026-09-03

Status: paper theorem for the first `2016 -> 54,432` rung, accepted after the
bounded Task575 repair (`ASSOCIATED_GRADE_CAYLEY_FOX_CAP_V454_AUDIT_PASS_AFTER_REPAIR`).  It sharpens the
source rank and queue bounds used by the grade-two prebuild without changing
the registered correction space.  It also records the exact additional data
needed before a Cayley-cycle basis may replace literal seed ancestry.
No grade membership, A0 terminal, COMMON word, compatible lift, fake, or
Ihara witness is asserted. `verified=false`.

## 1. The pure-grade Fox cycle containing every transition defect

Put

\[
 k=\mathbf F_3,\qquad Q_1=P\times A,
 \quad P=PSL(2,8),\quad A=C_2^2,
\]

and let \(M_d\) be the degree-\(d\) monomial space of
\(k[C_3^3]\).  Its dimensions are

\[
 h_d=\dim M_d=(3,6,7,6,3,1),\qquad 1\le d\le6.       \tag{1.1}
\]

For \(\lambda\in\widehat A\), write
\(R_\lambda=k[P]e_\lambda\).  A complete v444 seed or transition defect has
zero lower and auxiliary coordinates.  Before the six occurrence maps are
applied, its degree-\(d\), source-\(\lambda\) Fox pair is therefore an element

\[
 z=(z_x,z_y)\in R_\lambda^2\otimes M_d.              \tag{1.2}
\]

The word endpoint is the identity through the retained precision.  Taking
the first nonzero homogeneous part of the Fox endpoint identity gives

\[
 \partial_\lambda z
 =z_x(\bar x-1)+z_y(\bar y-1)=0.                     \tag{1.3}
\]

Only the degree-zero endpoints in \(Q_1\) occur in (1.3); every positive
kernel term raises filtration.  Hence every row of the exact coupled-monomial
closure satisfies

\[
 H_{d,\lambda}\ \subseteq\
 \ker\!\left(\partial_{d,\lambda}:
 (R_\lambda\otimes M_d)^2\to R_\lambda\otimes M_d\right).
                                                        \tag{1.4}
\]

Equation (1.4) is a containment of coupled tuples.  It neither projects onto
individual monomials nor withdraws the warning in v446.

## 2. Exact dimensions of the containing cycle spaces

The monomial multiplicity cannot be treated as a trivial coefficient space
for the **right** Fox boundary.  Let
\(\eta_1,\eta_2,\eta_3\) be the three nontrivial characters of \(A\) by
which it conjugates the three degree-one kernel coordinates.  The monomial
\(u^\alpha\) has character

\[
 \eta(\alpha)=\eta_1^{\alpha_1}
               \eta_2^{\alpha_2}
               \eta_3^{\alpha_3}.                   \tag{2.1}
\]

Write \(m_{d,\lambda}\) for the multiplicity of \(\lambda\) in \(M_d\).
For \(d=1,\ldots,6\), direct enumeration of
\(0\leq\alpha_i\leq2\), \(|\alpha|=d\), gives

| grade | \(h_d\) | \(m_{d,\mathbf1}\) | each \(m_{d,\lambda\ne\mathbf1}\) |
|---:|---:|---:|---:|
| 1 | 3 | 0 | 1 |
| 2 | 6 | 3 | 1 |
| 3 | 7 | 1 | 2 |
| 4 | 6 | 3 | 1 |
| 5 | 3 | 0 | 1 |
| 6 | 1 | 1 | 0 |

Indeed, the degree-\(d\) boundary in a source character is the Cayley
boundary with coefficient representation \(M_d\).  Its target has dimension
\(|P|h_d=504h_d\).  The cokernel is the coinvariant space of the regular
\(P\)-module tensored with \(M_d\); in source character \(\lambda\) it has
dimension \(m_{d,\lambda}\).  Rank-nullity therefore gives

\[
 \dim\ker\partial_{d,\lambda}
 =2(504h_d)-(504h_d-m_{d,\lambda})
 =504h_d+m_{d,\lambda}.                              \tag{2.2}
\]

For \(d=0\), (2.2) specializes to the Task540 F4 dimensions 505 in the
trivial character and 504 in each nontrivial character.  Formula (2.2), not
a tensor product with a trivial monomial action, is the positive-grade
statement.

There is no loss in passing to the stored six-tag occurrence coordinates.
One retained tag is `fxy`, the identity substitution.  In that tag the
pinned PB3 normal map sends a two-generator pair to

\[
 (v_x,v_y)\longmapsto
 \bigl(-v_xa,\ v_y-v_xab,\ \operatorname{aug}(v_x)\bigr). \tag{2.3}
\]

Its first regular component recovers
\(v_x=-({\rm first})a^{-1}\), and its second then recovers \(v_y\).
Thus (2.3), and hence the complete occurrence-separated map containing this
tag, is injective.  Semilinear transport in the other five tags cannot alter
this conclusion.

Combining (1.4), (2.2), and the identity-tag injection proves the following.

### Theorem 2.4 (associated-grade source cap)

For every positive grade of the first rung,

\[
 \boxed{
 \dim H_{d,\lambda}\le504h_d+m_{d,\lambda}.}
                                                               \tag{2.4}
\]

The six exact per-character caps are therefore

| grade | \(h_d\) | trivial cap | each nontrivial cap |
|---:|---:|---:|---:|
| 1 | 3 | 1,512 | 1,513 |
| 2 | 6 | 3,027 | 3,025 |
| 3 | 7 | 3,529 | 3,530 |
| 4 | 6 | 3,027 | 3,025 |
| 5 | 3 | 1,512 | 1,513 |
| 6 | 1 | 505 | 504 |

These are rank caps, not assertions that the caps are attained.

## 3. Saturation is an exact alternative to queue exhaustion

Let a deterministic closure basis in one character have retained rank
\(r\).  All of its rows lie in the fixed space on the right of (1.4).  If
\(r\) reaches the corresponding number in (2.4), its span equals that whole
containing space.  Every unprocessed legal origin and every later actor image
already belongs to it.  Therefore

```text
queue_exhausted OR cayley_fox_ambient_saturated
```

is an exact completion gate, provided the producer and checker independently
replay that every accepted row is the **full correlated six-tag occurrence
image**, with the registered auxiliary conditions and literal ancestry, of a
source-character raw pair satisfying (1.3).  The identity-tag injection
(2.3) identifies that raw pair, but by itself does not certify the other five
tags.  Saturation is not a heuristic early stop.

This gate completes discovery of the row span only.  If the block is to feed
the next v444/v451 grade, every registered origin and all four actor images of
every retained pivot must still have replayable reductions, or be replaced by
an independently replayable equivalent transition presentation.  Rank
saturation does not manufacture those records.

For the sealed grade-one blocks the measured ranks are

\[
 (1509,1512,1512,1512).                               \tag{3.1}
\]

Thus the trivial block has codimension three inside its containing cycle
space and each nontrivial block has codimension one.  In total the legal
grade-one defect space has codimension six in the associated Cayley-cycle
space.  No grade-one block is declared saturated.  Statement (3.1) does not
alter the live grade-one physical merge or its terminal.

## 4. Immediate grade-two resource consequence

The v451 handoff has

\[
 n_2=44+4\cdot8059=32,280                             \tag{4.1}
\]

complete defect origins.  A usual four-actor invariant queue offers each
origin once and at most four actor rows for every retained pivot.  Replacing
the ambient-width cap 36,288 by Theorem 2.4 gives

\[
 \begin{aligned}
  n_2+4(3027)&=44,388 &&\text{(trivial)},\\
  n_2+4(3025)&=44,380 &&\text{(each nontrivial)}.       \tag{4.2}
 \end{aligned}
\]

This replaces the previous per-character worst-case offer bound 177,432.
It is a fourfold reduction of the certified envelope, before any empirical
rank assumption.  If a block saturates, Section 3 can stop further **row
discovery**.  It cannot omit reductions still required for the next-grade
transition presentation; under that use the same bounded offers may still
have to be processed.

At width 36,288, four trits per byte, the largest retained primary basis is
at most

\[
 3027\cdot(36288/4)=27,460,944\ \text{bytes},          \tag{4.3}
\]

and a synchronized width-48,384 companion on the same 3,027 accepted pivots
is at most

\[
 3027\cdot(48384/4)=36,614,592\ \text{bytes}.          \tag{4.4}
\]

The implementation must emit these products as a resource preflight rather
than trusting prose.  Transcript reductions remain streamed and may
be much larger than the live bases; (4.3)--(4.4) do not authorize retaining
them as Python object graphs.

## 5. Relation-module route and its remaining ancestry gate

For any finite marked quotient \(Q\) of \(\Delta\), put

\[
 \Omega=\ker(F(x,y)\to\Delta),\quad
 \Omega_Q=\ker(F(x,y)\to Q),\quad
 \Gamma_Q=\ker(\Delta\to Q).
\]

Fox calculus identifies

\[
 Z_Q=H_1(\Omega_Q;k)=\ker(\partial_Q:k[Q]^2\to k[Q]). \tag{5.1}
\]

The homology five-term sequence for
`1 -> Omega -> Omega_Q -> Gamma_Q -> 1`, together with normal generation by
the 44 compact relators, gives the already established equality

\[
 K_Q:=\sum_{i=1}^{44}k[Q]J_Q(r_i)
     =\ker\bigl(Z_Q\xrightarrow{\tau_Q}H_1(\Gamma_Q;k)\bigr). \tag{5.2}
\]

At \(|Q|=54,432\), the registered rung data give
\(\dim H_1(\Gamma_Q;k)=5\).  Hence a second, potentially faster construction
is now exact in principle:

1. form a spanning-tree cycle basis of \(Z_Q\);
2. evaluate the five rows of \(\tau_Q\);
3. choose a basis of \(K_Q\) adapted to the six-step augmentation
   filtration; and
4. send its successive leading pieces through the injective occurrence map.

This would replace actor closure by direct Cayley--Fox bases and would also
give exact, rather than upper-bound, ranks in (2.4).  It is **not yet a
witness-bearing replacement**: a vector obtained merely as a kernel of the
five \(\tau_Q\) rows has no coefficients in the 44 seed-orbit generators.
Before it may feed a MEMBER word or the next grade, every selected basis row
must be converted to a replayable compact-seed/actor DAG, or the existing
literal defect closure must be shown to span it by reaching the exact rank.
This is the same chord-versus-generator distinction fixed in Fable v2 errata
R3.

Thus Theorem 2.4 is immediately usable as a cap and saturation certificate;
the full direct-basis substitution remains conditional on the explicit
ancestry conversion.

## 6. Claim boundary

```text
PURE-GRADE CAYLEY--FOX CONTAINMENT:       PAPER-CLOSED
GRADE CAP IN CHARACTER lambda:            504*h_d + m_(d,lambda)
GRADE-ONE CYCLE-SPACE CODIMENSIONS:        3 / 1 / 1 / 1
GRADE-TWO OFFER CAPS:                     44,388 / 44,380
DIRECT TAU/CYCLE BASIS WITH SEED DAG:      NOT YET CONSTRUCTED
GRADE-ONE OR GRADE-TWO MEMBERSHIP:         NOT CHANGED / NOT RUN
ORDER-54,432 / FULL-Q0 / A0 / COMMON:      NOT DECIDED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:    NOT DECLARED
verified:                                  false
```

`R07_ASSOCIATED_GRADE_CAYLEY_FOX_RANK_CAP_V454_PAPER`
