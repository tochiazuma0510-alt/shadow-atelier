# Task 555 audit — repaired projector words and six-grade schedule

This is an independent mathematical/static audit.  V447 incorporates the
Task553 marked-word repair exactly, and every numerical width in v448 is
correct.  V448 has one local indexing defect in (3.1): under the notation of
v444, lifting `B_(d-1)` to precision `d` produces the defect module
`H_(d-1)`, not `H_d`.  After making that explicit replacement, the six-step
induction and its order-54,432 endpoint are paper-sound.  No grade has been
computed by this audit.

I ran no Python, GAP, git, GHA, es7ops, or other agent and did not inspect,
delay, or alter the separately commissioned Task554 implementation.

## 1. Dependency pins

I read all seven commissioned dependencies in full.  Their recomputed byte
counts and SHA-256 values are:

| input | bytes | SHA-256 |
|---|---:|---|
| v441 | 11,696 | `5cb52ffd02d2cd5c89e08080931065123a7208f7d5a2878acddb5d9ac2958fbb` |
| v444 | 9,953 | `705afdc595f21f64356b70469a8444708b8a8c8e6306c218e942863a560ef645` |
| v446 | 9,262 | `389ceee1250b892ec4845753af23f4455e619e2d72782931645d8b8176764756` |
| Task 553 reply | 16,864 | `9e06ae4022e6267846561b13fed2f64a73909ba0d3b681fd6a6bb6dba1df` |
| Task 549 reply | 13,003 | `a088d27203e2064ac8240b813fd15e905ec82633b93b829e89b4a073f111256c` |
| v447 | 4,415 | `3e4bb3e498beb2c44cf3e1f0786ad83c7691312674967877b766e3e61bb496c2` |
| v448 | 5,881 | `168e3fc5ab38520faf8ed5d107013f1f8b53f22d2907032519b86b6e0f01182d` |

Both commissioned v447/v448 identities match exactly.

## 2. V447 exact-incorporation audit

### 2.1 Exact words and endpoints

V447 reproduces all four Task549/Task553 word lists entry for entry.  With
`1=x`, `-1=x^-1`, `2=y`, and `-2=y^-1`, the comparison is:

| `a` | encoded word | length | Task549 endpoint |
|---|---|---:|---|
| `(0,0)` | `[]` | 0 | `(1_P,(0,0))` |
| `(0,1)` | `[-2,-2,-2,-2,-2,-2,-2,-2,-2]` | 9 | `(1_P,(0,1))` |
| `(1,0)` | `[-2,-2,1,1,2,1,2,1,1]` | 9 | `(1_P,(1,0))` |
| `(1,1)` | `[-2,-2,-2,-1,-2,-1,-1,-1,-2,-1]` | 10 | `(1_P,(1,1))` |

Task549 independently enumerated all 2,016 marked states and replayed these
full-`Q1` endpoints.  Hence the operators come from words in the registered
actors `x,x^-1,y,y^-1`; they are not external coordinate operations.  V447
also preserves Task553's essential boundary: purity of a word in the `G9`
factor alone is not used to infer a trivial `PSL(2,8)` endpoint.

### 2.2 Upstairs values and associated-grade scope

For the value of a pure-`Q1` word in the first extension, write

\[
 d_a=\sigma(1_P,a)n(v_a),\qquad v_a\in V.
\]

V447 correctly makes no assertion that `v_a=0`.  If
`f in I^d/I^(d+1)` is homogeneous, v443's exact left-action formula is

\[
 L_{d_a}([p,b]f)
   =[p,a+b]E(S(b)v_a)f.
\]

Since \(E(S(b)v_a)-1\in I\), its product with `f` lies in
`I^(d+1)` and vanishes only after passage to the pure associated grade.
Thus

\[
 L_{d_a}=T_a=L_{(1_P,a)}
 \quad\text{on }I^d/I^{d+1}.                         \tag{2.1}
\]

This qualification is load-bearing.  Formula (2.1) must not be applied to
a mixed lower-plus-new row.  V448 uses it only after identical lower
reduction has produced zero-lower seed and transition defects, so its order
of operations is correct.

The action is also legally correlated.  In occurrence tag `j`, the same
source word has quotient `(1_P,A_j a)` and may have a crossed kernel term;
the latter again disappears on the associated grade.  The transported
character satisfies

\[
 (\lambda\circ A_j^{-1})(A_j a)=\lambda(a).
\]

The single actor word therefore acts simultaneously on all six tags and on
both Fox components with the required common character scalar.  V447 does
not introduce independent tag, Fox-component, or monomial projections.

### 2.3 Fourier normalization and the generated submodule

Let

\[
 e_\lambda=\sum_{a\in A}\lambda(a)T_a,
 \qquad A=C_2^2.
\]

The ordinary normalization factor is `1/|A|`.  In `F3`,
`|A|=4=1`, so its inverse is also one; every character value and every
element of `A` is self-inverse.  The coefficient of `T_c` in a product is

\[
 [T_c](e_\lambda e_\mu)
 =\mu(c)\sum_{a\in A}(\lambda\mu)(a),
\]

which is `lambda(c)` when `lambda=mu` and zero otherwise.  Hence

\[
 e_\lambda e_\mu=\delta_{\lambda\mu}e_\lambda,
 \qquad \sum_\lambda e_\lambda=1.                  \tag{2.2}
\]

Every `T_a` is an exact legal word operator.  Therefore, for the complete
v444 seed/transition defect set `D_d` and its legal closure

\[
 H_d=\mathbf F_3\langle Q_1\rangle D_d,
\]

one has `e_lambda H_d subseteq H_d`.  Equation (2.2) supplies the sum and
orthogonality supplies directness:

\[
 \boxed{H_d=\bigoplus_{\lambda\in\widehat A}e_\lambda H_d}. \tag{2.3}
\]

V447 (2.1)--(5) therefore incorporates Task553 exactly.  It licenses four
character blocks and nothing finer: all monomials remain coupled in each
block.

## 3. Hilbert series and all six widths

The kernel group algebra is

\[
 \mathbf F_3[V]
 \cong\mathbf F_3[u_1,u_2,u_3]/(u_1^3,u_2^3,u_3^3).
\]

Consequently its Hilbert series is

\[
 (1+t+t^2)^3
 =1+3t+6t^2+7t^3+6t^4+3t^5+t^6.                  \tag{3.1}
\]

The positive multiplicities are therefore

\[
 (h_1,h_2,h_3,h_4,h_5,h_6)=(3,6,7,6,3,1).
\]

Every surviving monomial has each exponent at most two, so total degree is
at most six.  Thus `I^7=0`; moreover `I^6` is nonzero, spanned over the
quotient coordinate by `u_1^2u_2^2u_3^2`.

For a fixed character the source factor before monomials is

\[
 6\ \text{tags}\cdot2\ \text{Fox components}\cdot|P|
 =6\cdot2\cdot504=6,048.
\]

Four characters give `4*6048*h_d`, and the joint physical grade has four
physical copies of the full order-2016 quotient, hence
`4*2016*h_d=8064*h_d`.  Recomputing every row gives:

| grade `d` | `h_d` | one character `6048 h_d` | four characters | physical `8064 h_d` |
|---:|---:|---:|---:|---:|
| 1 | 3 | 18,144 | 72,576 | 24,192 |
| 2 | 6 | 36,288 | 145,152 | 48,384 |
| 3 | 7 | 42,336 | 169,344 | 56,448 |
| 4 | 6 | 36,288 | 145,152 | 48,384 |
| 5 | 3 | 18,144 | 72,576 | 24,192 |
| 6 | 1 | 6,048 | 24,192 | 8,064 |

All v448 table entries pass.  They are new-grade ambient coordinate widths.
They are not ranks, cumulative presentation dimensions, queue sizes,
runtimes, serialized artifact sizes, or live-memory estimates.  In
particular, the persistent old basis, reductions, literal ancestry, sparse
work structures, and physical receipts are additional state.  Even summing
the six ambient widths would not measure peak memory or establish an
exhausted rank.

## 4. Induction, the indexing repair, and the endpoint

### 4.1 Exact local repair to v448 (3.1)

V444 fixes the notation

\[
 U_{r+1}=\operatorname{span}(\widetilde B_r)\oplus H_r, \tag{4.1}
\]

where `H_r` is the defect closure for the lift from precision `r` to
precision `r+1`.  V448 instead starts its grade-`d` step from
`T_(d-1)` and `B_(d-1)`.  Substitution `r=d-1` in (4.1) gives

\[
 \boxed{
 U_d=\operatorname{span}(\widetilde B_{d-1})\oplus H_{d-1}.} \tag{4.2}
\]

Thus the occurrence of `H_d` in v448 (3.1) is off by one relative to its
cited theorem.  Taken literally, it would use the next transition defect
module; at `d=6` that would point at the zero seventh grade rather than the
required sixth-grade defects.

The exact replacement for v448 (3.1) is (4.2), with the clarification

\[
 H^{[d]}:=H_{d-1}^{\mathrm{v444}}
 \subseteq\ker(\widehat{\mathcal O}_d\to
                    \widehat{\mathcal O}_{d-1})
\]

if grade-indexed notation is preferred.  All references in v448 Section 3
to the grade-`d` defect closure should then read `H^[d]`; its width remains
`h_d`.  No algorithmic step or table entry changes.

### 4.2 Transition presentation is sufficient

At the end of a successful precision `d`, the required presentation is
exactly:

1. a deterministic basis `B_d` of the complete occurrence-source orbit,
   with literal instruction ancestry for every row;
2. the reduction of every one of the 44 original seeds against `B_d`;
3. the reduction of each of `x,x^-1,y,y^-1` applied to every basis row;
4. every registered non-filtration coordinate, including normalized
   exponents, PB3 augmentation, and all occurrence tags;
5. the accepted accumulated literal correction and its direct replay; and
6. complete lower-first physical image/fibre receipts, including all
   lifted-old connection rows and all coupled-defect aggregates.

These data are precisely v444 (2.1)--(2.3) plus the v441 physical and
auxiliary gates.  On the next lift, the old seed equalities yield all seed
defects, and the four old transition equalities yield all transition
defects.  Their zero lower reductions and legal actor closure give
`H_(d-1)`.  If a basis of that module is appended to the lifted old basis,
then:

* each new seed reduction is the lifted old reduction plus the recorded seed
  defect expression;
* each old-basis actor transition is the lifted old transition plus its
  recorded transition-defect expression; and
* actor closure supplies the four transitions for every new defect-basis
  row.

Thus the next presentation contains every equality required to repeat the
induction.  Literal instruction trees, rather than copied low-precision row
values, are reevaluated at the higher precision.

Task542 supplies the accepted literal vector `c_0`, but it does not supply
this complete `T_0`.  V448 states that limitation correctly.  Its chosen
schedule requires one complete degree-zero occurrence closure to discover
and store the seed and actor-transition presentation.  Historical actor
paths need not be rediscovered later: their instruction trees are carried
forward and reevaluated, while each new transition defect prepends only the
registered actor needed by v444.  A target coefficient vector by itself is
never promoted to a transition presentation.

### 4.3 Physical fibre and terminal at each grade

For grade `d`, aggregate only after the repaired source equality (4.2) has
been exhausted.  Process both the lifted old basis and an exhausted basis of
`H_(d-1)` through one complete lower-first physical echelon.  V444 shows that
these rows span the full occurrence image; v441 then identifies the
zero-lower physical rows with its canonical fibre `K_d`.  Retaining only
visibly degree-`d` defects would omit connection directions created by lower
dependencies among old lifted rows.

The trichotomy is exact:

* `MEMBER` means `rho_d in K_d`.  Persist the fibre coefficients, their
  literal word-bearing update, zero change in every lower and auxiliary
  coordinate, direct grade-`d` replay, and the newly recomputed residual.
  Then construct the complete next transition presentation described above.
* `NONMEMBER` requires a dual on the full joint grade coordinates that
  annihilates every final fibre row, including coupled-defect aggregates and
  old-lift connections, and pairs nontrivially with `rho_d`, together with
  complete closure and reduction receipts.  It excludes every extension of
  the lower solution locus, not merely the displayed representative.
* Any incomplete seed or transition table, actor queue, ancestry,
  auxiliary coordinate, aggregation, fibre, direct replay, or resource gate
  is `UNKNOWN`.

No source action is applied after physical aggregation.  The physical solve
is joint unless a separately sealed actual-row hypergraph proves a direct
sum, as required by Task553.

### 4.4 Six MEMBER steps give the exact first-rung endpoint

The cross-checked order-2016 word `c_0` has residual in `I`.  Inductively, a
successful grade-`d` update lies in the complete relative fibre, preserves
all earlier equalities and auxiliary conditions, and moves the new residual
into `I^(d+1)`.  After directly replayed MEMBER steps for
`d=1,2,3,4,5,6`, the residual lies in `I^7=0`.  Hence the accumulated literal
word satisfies the registered target exactly in the order-54,432 quotient.

This implication is conditional on six actual MEMBER terminals and their
direct literal replays.  It is not a consequence of the ambient widths,
rank telemetry, or the paper recurrence alone.

## 5. Equation findings, safe contract, and claim boundary

| item | finding |
|---|---|
| v447 (2.1) four words/full-`Q1` endpoints | PASS; exact Task549/Task553 incorporation |
| v447 (3.1)--(3.3) arbitrary kernel lift | PASS only on a pure associated grade |
| v447 correlated tag/Fox action | PASS |
| v447 (4.1)--(4.3) Fourier projectors/direct sum | PASS |
| v447 monomial boundary and gate 5 | PASS |
| v448 (1.1)--(1.2) Hilbert series and nilpotence | PASS |
| v448 six-row width table | PASS as new-grade ambient widths |
| v448 (3.1) one-step source equality | REPAIR: replace `H_d` by `H_(d-1)` as in (4.2) |
| v448 transition-presentation induction | PASS after that index repair |
| v448 physical fibre/trichotomy | PASS after that index repair |
| v448 six-MEMBER endpoint | PASS conditionally; not computed |

The exact safe induction contract is:

```text
INITIALIZE: reconstruct complete T_0 once; c_0 alone is insufficient
GRADE d:    lift T_(d-1), form all seed and four-actor defects H_(d-1),
            then project only the complete zero-lower defects
SOURCE:     four legal character blocks of width 6048*h_d;
            keep all h_d monomials coupled and exhaust every actor queue
PRESENT:    B_d ancestry, all 44 seed reductions, and all four transitions
            for every B_d row, with all registered auxiliary coordinates
PHYSICAL:   lifted-old rows plus H_(d-1), lower-first in joint width 8064*h_d
MEMBER:     literal update, zero lower/auxiliary change, direct replay,
            next residual, and complete T_d
NONMEMBER:  complete-fibre dual and nonzero residual pairing
INCOMPLETE: UNKNOWN
ENDPOINT:   only six directly replayed MEMBER steps plus I^7=0 imply Q2 equality
```

This is a finite first-extension algorithm, not computed membership or a
runtime/memory estimate.  It makes no assertion that a residual is MEMBER,
does not transfer the four-character decomposition to the second rung, and
does not construct a compatible cofinal inverse-limit lift.  No full-Q0,
A0, COMMON, fake, Ihara, or Lean conclusion follows.

## 6. Verdict

FIRST_RUNG_SIX_GRADE_SCHEDULE_PASS_AFTER_REPAIR

FIRST RUNG: 0/6 GRADES COMPUTED

ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED

verified=false
