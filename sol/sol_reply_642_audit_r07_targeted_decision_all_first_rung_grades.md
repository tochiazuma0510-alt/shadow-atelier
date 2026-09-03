# Sol(max) Task642: targeted decision through all first-rung grades

## Verdict

**GENERALIZES.**  V474's target-directed primal/dual theorem is not
intrinsically degree-two.  Once the complete transition presentation through
grade `e-1` and an independently accepted fresh residual `rho_e` are
supplied, the same construction applies for every

```text
e = 2,3,4,5,6.
```

The occurrences of `48,384`, `36,288`, `32,260`, `8,059` and `32,280` in
v474 are the grade-two instantiation of dimension/rank parameters, not steps
used essentially by either proof.  No repair to the candidate abstract
identity in the kickoff is needed.  A generalized executable does require
new, grade-indexed inputs and caps; merely changing v474's numeric constants
or reusing an early targeted MEMBER span would be unsound.

This is a static mathematical audit only.  I did not implement or run a
decision procedure, production, GHA, or git.  It establishes no actual
MEMBER/NONMEMBER result, order-54,432 solution, A0 result, cofinal lift, fake
witness or Ihara conclusion.  `verified=false`.

## 1. Exact inputs

Hashes are SHA-256 over exact bytes; `LF` counts byte `0x0a`.

| input | bytes | LF | SHA-256 |
|---|---:|---:|---|
| Task642 kickoff | 3,421 | 79 | `6df9cde9a54f2099f52d0ec1e38b36df82754937d62966f27629ce61d8d26170` |
| v441 relative fibre | 11,696 | 328 | `5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb` |
| v443 truncated engine | 10,291 | 322 | `80970217b415d7b764e399b5ce5892075b1f82f7f87f0c6199e9f6b0e404f24c` |
| v444 transition defects | 9,953 | 254 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| v446 coupled character blocks | 9,262 | 253 | `389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756` |
| v447 projector-word repair | 4,415 | 144 | `3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2` |
| v448 six-grade schedule | 5,881 | 139 | `168e3fc5ab38520faf8ed5d107013f1f8b53f22d2907032519b86b6e0f01182d` |
| repaired v449 indexing | 1,408 | 40 | `0237572f8ee949cdac8129cb9a9dae8c833b00baee2647c0deed194449577ff9` |
| Task555 six-grade audit | 14,309 | 359 | `8dcdfbb4825c65bff9698311b735e830c27d39f98405bcfb01af3411d97a2e45` |
| v451 split handoff repair | 8,050 | 229 | `3ec2d1351e16bf0fcde3abe8da346b8765b26c30796ff48e415c46ac51d933b4` |
| v474 targeted dual decision | 12,755 | 321 | `a0ae668799de33d79b5e80ca2a6b7b50224770528b1201d8fb999506757c08c9` |
| candidate v479 dovetail | 12,280 | 292 | `df6850c9e7c86a83ade26c37064a7deb38ec3c8d7907b1eec6ff0d5268b22986` |

Task555's accepted repair is used throughout:

\[
 H^{[e]}:=H^{\mathrm{v444}}_{e-1},\qquad
 U_e=\operatorname{span}(\widetilde B_{e-1})\oplus H^{[e]}. \tag{1.1}
\]

Thus the `e` below always denotes the fresh physical grade, not the lower
index used for v444's defect module.

## 2. Recomputed dimension table

For

\[
 (h_0,\ldots,h_6)=(1,3,6,7,6,3,1),\qquad
 \mathsf H_d=\sum_{i=0}^{d}h_i,
\]

put

\[
 n_e=8064h_e,\qquad m_e=6048h_e,\qquad
 \ell_e^{\rm width}=8064\mathsf H_{e-1}+4.          \tag{2.1}
\]

Here `n_e` is the full joint physical grade, `m_e` is one complete
character source slice, and the lower width includes every earlier regular
grade plus the four physical auxiliary coordinates.  Direct recomputation
gives:

| fresh grade `e` | `h_e` | `H_(e-1)` | one character `m_e` | four-character top source | physical top `n_e` | physical lower/aux | packed top bytes |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 6 | 4 | 36,288 | 145,152 | 48,384 | 32,260 | 12,096 |
| 3 | 7 | 10 | 42,336 | 169,344 | 56,448 | 80,644 | 14,112 |
| 4 | 6 | 17 | 36,288 | 145,152 | 48,384 | 137,092 | 12,096 |
| 5 | 3 | 23 | 18,144 | 72,576 | 24,192 | 185,476 | 6,048 |
| 6 | 1 | 26 | 6,048 | 24,192 | 8,064 | 209,668 | 2,016 |

For comparison, exact source evaluation through the fresh grade, including
all six tags, both Fox components, four characters and the eight source
auxiliary coordinates, has width

\[
 24192\mathsf H_e+8,
\]

namely `241,928`, `411,272`, `556,424`, `629,000`, and `653,192` for
grades 2--6.  These and the table entries are coordinate widths, not ranks,
queue bounds or RSS estimates.

## 3. The connection identity is degree-independent

Let `r = r_(e-1) = dim U_(e-1)` be the rank of the *complete* preceding
occurrence presentation and let `E=k^r` have its ordered old-basis
coordinates.  Exact precision-`e` lift followed by the registered physical
map gives linear maps

\[
 \ell_e:E\longrightarrow L_e,\qquad
 g_e:E\longrightarrow P_e,                           \tag{3.1}
\]

where `L_e` has the lower/auxiliary width in (2.1) and
`P_e=k^(n_e)`.  No property of the number `8,059` occurs here.

Run the fixed lower-first elimination in old-basis offer order.  Each
accepted lower pivot stores the coefficient vector

\[
 u_j=\sigma_i\left(e_i-\sum_pq_{i,p}u_p\right),
\]

including its normalization scale.  Each dependent offer stores

\[
 k_i=e_i-\sum_pq_{i,p}u_p,qquad \ell_e(k_i)=0.       \tag{3.2}
\]

Every `k_i` has coefficient one at its own previously unused offer index and
only earlier support otherwise.  The dependent `k_i` are therefore
independent.  If `p=rank(ell_e)`, there are exactly `r-p` of them, which is
`dim ker(ell_e)`; equivalently ordinary ordered elimination expresses every
kernel relation in their span.  Hence

\[
 \{k_i:\text{dependent offer}\}\text{ is a basis of }\ker\ell_e,
\]

and, for the ordered connection list `c_i=g_e(k_i)`,

\[
 \boxed{\operatorname{span}(\mathrm{Conn}_e)
             =g_e(\ker\ell_e).}                     \tag{3.3}
\]

The `c_i` themselves may contain zeros or physical dependencies; (3.3)
claims their span, not that they form a basis after applying `g_e`.  This
proof uses only finite-dimensional linearity, the complete ordered offer
roster, and identical reduction coefficients/scales in the lower and top
blocks.  It is independent of `e`, all ambient widths, and the value of `r`.

For grade two, `r_1=8059` and (3.3) is exactly v474's connection argument.
For grades three through six, `r_2,...,r_5`, `p_e`, the number of
connections `r_(e-1)-p_e`, and their hashes are result-dependent inputs;
none may be copied from grade two.

## 4. Four characters and the quadratic substitution terms

### 4.1 The legal decomposition persists

The v447 pure-`Q1` words induce the four character idempotents on every pure
associated grade.  If an upstairs representative has kernel coordinate
`v_a`, its extra factor is `E(S(b)v_a)=1+(positive degree)`.  On a
homogeneous degree-`e` row, the positive-degree part lies in `I^(e+1)`.
Thus v447's identities

\[
 e_ae_b=\delta_{ab}e_a,qquad \sum_ae_a=1
\]

hold on `I^e/I^(e+1)` for every `0 <= e <= 6`.  Since each projector is a
linear combination of exact legal actor words, for the full seed/transition
defect closure

\[
 H^{[e]}=\bigoplus_{a\in\widehat{C_2^2}}H_{a,e}.     \tag{4.1}
\]

This is a decomposition of the generated submodule, not an ambient
coordinate convenience.  Each `H_(a,e)` is closed under the same four
correlated source actors in the full

\[
 V_{a,e}=k^{6048h_e}.
\]

No individual monomial projection is legal.  All `h_e` monomials remain
coupled inside that one character slice, including all seven at grade three.
The candidate targeted algorithm respects this because its dual orbit lives
in the whole `V_(a,e)^*`.

### 4.2 Negative and crossed terms do not obstruct the pure-grade action

The exact negative substitution is

\[
 u_i\longmapsto2u_{\sigma(i)}+u_{\sigma(i)}^2.       \tag{4.2}
\]

For a degree-`e` monomial, selecting any quadratic term raises total degree.
Consequently the induced map on `I^e/I^(e+1)` is the leading signed
permutation of the degree-`e` monomial roster, with its nonzero scalar.  The
crossed-cochain factor `E(c_j(a))` likewise has constant term one and only
raises degree beyond `e`.  Thus the associated-grade actor maps

\[
 T[a,t]:V_{a,e}\to V_{a,e}
\]

and the occurrence-leading maps are honest linear endomorphisms at every
grade.  At grade six, every raised term lies in `I^7=0`.

This does **not** authorize dropping the quadratic or crossed terms from the
precision-`e` lift.  Acting on lower-degree pieces can raise them into the
fresh grade.  The construction of `ell_e`, `g_e`, every seed/transition
defect, and the fresh residual must therefore use v443's complete truncated
formulas through degree `e`.  Only after exact lower reduction proves a
defect pure may its associated-grade slice be passed to `T[a,t]` and
`B_(a,e)`.  A linearized substitution used during the lift would make
(3.3) and the image theorem below incomplete.

## 5. Completeness of the image identity

Let `D_e` be the complete roster of

\[
 N_e=44+4r_{e-1}                                     \tag{5.1}
\]

raw seed and four-actor transition defects.  Each defect must first be
proved zero in every lower and auxiliary coordinate.  Project the complete
pure slice into all four characters, exhaust every actor orbit, and call the
resulting spaces `H_(a,e)`.  Let

\[
 B_{a,e}=\operatorname{gr}_e(\Pi_g)\circ i_a:
 V_{a,e}\longrightarrow P_e                          \tag{5.2}
\]

be the entire registered occurrence-first map: six typed H occurrences,
their signs and fixed prefixes, PB3 normal/boundary operations, the PB4
block quotient, character transport, and final physical aggregation.  It is
not a tagwise action on an already aggregated row.

V444/v449 give the source equality (1.1).  For an old-lift coefficient
`x in E` and a pure defect combination
`h=sum_a i_a(h_a)`, its physical lower and top blocks are respectively

\[
 \ell_e(x),\qquad g_e(x)+\sum_aB_{a,e}(h_a).          \tag{5.3}
\]

The pure defect contributes no lower term by construction.  Therefore the
complete lower-zero physical image is

\[
 \boxed{
 M_e=g_e(\ker\ell_e)+\sum_aB_{a,e}(H_{a,e})
    =\operatorname{span}(\mathrm{Conn}_e)
       +\sum_aB_{a,e}(H_{a,e}).}                     \tag{5.4}
\]

No directness of the summands in physical space is claimed or needed.  This
also shows why neither only the pure defects nor only the connections is
complete.

Equation (5.4) includes all v441/v451 typing provided the grade-specific
certificate binds the following premises:

1. `ell_e` contains *every* regular grade below `e` and all four physical
   auxiliary entries, including the two PB3 augmentations and two normalized
   exponents;
2. normalized exponents are checked integrally before reduction modulo
   three, their actor action is retained, and all pure defects have zero
   auxiliary coordinates;
3. the PB3 normal map and every translated PB3 boundary row, the PB4
   boundary/block quotient, and their commutation with filtration,
   occurrence transport and aggregation are replayed through grade `e`;
4. all `r_(e-1)` old lifts and all `N_e` defects occur exactly once in their
   ordered rosters, with full literal ancestry; and
5. all four character closures reach FIFO EOF with the full coupled monomial
   roster.

These are per-grade input gates, not a new algebraic repair.  V451 supplies
their grade-two instance; it is not by itself a presentation for later
grades.

## 6. Dual criterion and separator termination

For `lambda in P_e^*`, define

\[
 q[a,\varnothing]=B_{a,e}^*(\lambda),\qquad
 q[a,w+t]=T[a,t]^*(q[a,w]),                           \tag{6.1}
\]

and let `K_(a,e)(lambda)` be the least subspace containing the root and
closed under the four adjoints.  Since

\[
 H_{a,e}=\operatorname{span}{T[a,w]d[a,o]:w,\ o\},
\]

equation (5.4) gives the exact equivalence

\[
 \lambda(M_e)=0
 \Longleftrightarrow
 \begin{cases}
 \lambda(c)=0&\text{for every }c\in\mathrm{Conn}_e,\\
 q(d[a,o])=0&\text{for every accepted raw }q\in
 K_{a,e}(\lambda),\ a,\ o.
 \end{cases}                                         \tag{6.2}
\]

Each dual orbit has at most `m_e` pivots.  Overlaps among the four physical
images do not affect (6.2): a functional kills a sum exactly when it kills
each generating summand.

The exact word convention also carries over without change.  For
`w=(t_1,...,t_s)`,

```text
T[a,w] = T[a,t_1] ... T[a,t_s]
q[a,w] = B[a]^*(lambda) composed with T[a,w]
right extension w+t uses T[a,t]^*(q[a,w]).
```

Store the echelon-normalized dual pivot separately from the unreduced raw
representative bearing `w`.  A failed raw pairing emits the matching primal
row `B_(a,e) T[a,w] d[a,o]`.  If the paired dual was instead a normalized
linear combination, the emitted primal row must use the identical linear
combination.  This transpose convention is dimension-free.

Now let `S_initial <= M_e` be an authenticated physical span of rank `s_0`
and solve in the fixed full coordinate order

\[
 \lambda(S)=0,\qquad \lambda(\rho_e)=1.              \tag{6.3}
\]

Whenever a connection or defect test fails, (6.2) supplies an explicit
`g in M_e` with `lambda(g) != 0`.  Because `lambda(S)=0`, this `g` is outside
`S`, so insertion increases its rank strictly.  There can be at most
`n_e-s_0` failed passes.  On the next pass, inconsistency of (6.3) is exactly
`rho_e in S`; otherwise complete connection EOF, four dual-orbit EOFs, and
all defect pairings give a separating functional.  Hence the exact bound is

\[
 \boxed{n_e-s_0+1=8064h_e-s_0+1}                    \tag{6.4}
\]

separator solves, including the terminal pass.  This is v474 Theorem 3.1
with parameters substituted.  It proves termination only for unlimited
exact arithmetic.  Any finite cap returns `UNKNOWN_RESOURCE`, never a
mathematical negative.

MEMBER still requires back-substitution through physical rows, raw orbit
words, all defects/lifts and all connections, followed by an independent
comparison of every one of the `n_e` target coordinates.  NONMEMBER still
requires connection EOF, all four orbit EOFs, and every one of the
`4*m_e*N_e` possible raw-defect pairings (or a receipt proving the exact
completed subset when an orbit rank is smaller).  Sampled transpose canaries
cannot replace an entrywise structural proof of

\[
 \langle T^*q,v\rangle=\langle q,Tv\rangle,
 \qquad\langle B^*\lambda,v\rangle=\langle\lambda,Bv\rangle. \tag{6.5}
\]

## 7. Grade-specific implementation data and honest resource formulas

The theorem is uniform; these inputs are not:

1. the accepted complete preceding presentation `P_(e-1)`, its actual rank
   `r_(e-1)`, basis ancestry, all 44 seed reductions, and all four actor
   transitions of every basis row;
2. the deterministic degree-`e` monomial roster and coordinate order, with
   all `h_e` monomials coupled per character;
3. exact precision-`e` seed, actor, occurrence, prefix, PB3/PB4, exponent and
   aggregation maps, and independently generated structural adjoints;
4. the complete old-lift maps `ell_e/g_e`, pivot scales/reductions,
   connection count and EOF receipt;
5. all `N_e=44+4r_(e-1)` defects, their lower-zero gates, four character
   slices, and actor-orbit inputs;
6. an independently accepted canonical witness `C_(e-1)`, dense equality
   through grade `e-1`, and fresh residual
   `rho_e=gr_e(T-Ephys(C_(e-1)))` after every
   `8064*H_(e-1)+4` lower/auxiliary coordinate is compared with zero;
7. the initial targeted span and rank `s_0`, coordinate/pivot order,
   producer/checker transcript formats, and all result-dependent hashes; and
8. grade-specific wall, RSS, queue, pairing, iteration, path/ancestry and
   durable-byte caps.

Useful raw packed-row ceilings, still not RSS promises, are:

| `e` | physical basis `n_e^2/4` bytes | one dual basis `m_e^2/4` bytes | max dual offers/character `1+4m_e` |
|---:|---:|---:|---:|
| 2 | 585,252,864 | 329,204,736 | 145,153 |
| 3 | 796,594,176 | 448,084,224 | 169,345 |
| 4 | 585,252,864 | 329,204,736 | 145,153 |
| 5 | 146,313,216 | 82,301,184 | 72,577 |
| 6 | 16,257,024 | 9,144,576 | 24,193 |

The connection-row packed ceiling is
`(r_(e-1)-rank(ell_e))*n_e/4` bytes, and the maximal dual-defect pairing
count in one complete outer pass is

\[
 4m_e(44+4r_{e-1}).                                  \tag{7.1}
\]

These result-dependent quantities can dominate even when `n_e` decreases.
Therefore no grade inherits v474's grade-two cap merely because its physical
top is smaller, and no uniform speedup over full primal closure is claimed.

## 8. V479's two-track boundary

A targeted MEMBER at grade `e` returns an exact selected expression for
`rho_e`.  With full ancestry and direct lower/top replay, that expression is
sufficient to form the ordered source update

\[
 C_e=\operatorname{Compose}(C_{e-1},\Delta C_e)
\]

and hence to evaluate the next fresh residual `rho_(e+1)`.  It is **not** a
complete presentation of `U_e`: CEGAR may stop as soon as its small span
contains this one target and may never enumerate unused primal orbit rows,
seed reductions, or actor transitions.

For every successor decision at grades 3--6, the join therefore requires
two separately accepted parents:

```text
witness branch:      exact C_(e-1), endpoint/source receipts,
                     dense lower equality, fresh rho_e;
presentation branch: complete P_(e-1), all basis ancestry,
                     44 seed reductions, 4*r transitions and EOF closures.
```

The branches may run concurrently as v479 states, but neither substitutes
for the other.  A targeted grade-`e` MEMBER may advance the witness branch
immediately; the grade-`e+1` decision remains `NOT_READY` until the complete
target-independent `P_e` branch also finishes.  At grade six, MEMBER plus
the independently replayed prior five updates puts the residual in
`I^7=0`; this audit does not assert that any such MEMBER terminal exists.

## 9. Finite acceptance gates and claim boundary

A generalized producer/checker must, for the selected grade:

1. authenticate the two v479 parent branches and reject a selected CEGAR
   span presented as the complete transition presentation;
2. replay every old basis row, 44 seed equality and four transitions per
   row, then construct all `N_e` exact full lifts and defects before taking
   pure-grade slices;
3. retain the full quadratic negative substitutions and crossed terms in
   all filtered lifts, while using only their proved associated-grade maps
   inside the four complete coupled-monomial orbit closures;
4. independently reconstruct `ell_e`, `g_e`, every normalized lower pivot,
   every kernel vector and connection, and prove (3.3) with EOF;
5. bind and replay all PB3/PB4, exponent, auxiliary, prefix, sign,
   occurrence-first and filtration-commutation gates in Section 5;
6. independently construct `B_(a,e)`, `T[a,t]` and every adjoint from the
   coordinate maps, then check (6.5) entrywise rather than importing a row
   oracle;
7. authenticate the fresh `rho_e`; on MEMBER replay all `n_e` coordinates
   from literal ancestry, and on NONMEMBER exhaust all connections, four
   dual queues and all required defect pairings; and
8. fail closed as `UNKNOWN_RESOURCE` on any cap or incomplete transcript,
   emitting neither a partial residual nor a mathematical terminal.

The unknown values are the actual ranks `r_2,...,r_5`, lower ranks,
connection counts, defect/closure ranks, resource use, fresh residuals and
all result hashes.  Their absence affects readiness and cost, not the
degree-independent proof.

```text
V474 TARGETED THEOREM AT GRADES 2--6:       GENERALIZES
CONNECTION KERNEL IDENTITY:                 DEGREE-INDEPENDENT
FOUR CHARACTER BLOCKS:                     LEGAL AT EVERY FIRST-RUNG GRADE
MONOMIAL PROJECTIONS:                       FORBIDDEN; KEEP h_e COUPLED
NEGATIVE QUADRATIC TERMS IN FULL LIFTS:     REQUIRED
IMAGE INCLUDING CONNECTIONS/AUXILIARIES:   COMPLETE UNDER STATED GATES
SEPARATOR SOLVE BOUND:                      8064*h_e-s_0+1
TARGETED MEMBER = NEXT PRESENTATION:        NO
ACTUAL GRADES DECIDED BY THIS AUDIT:        NONE
ORDER-54,432 / A0 / COFINAL / FAKE / IHARA: NOT DECLARED
verified:                                    false
```

`R07_TASK642_TARGETED_DECISION_ALL_FIRST_RUNG_GRADES_GENERALIZES`
