# R07 A0 quotient-weighted actor column generation (v409)

Author: Sol / 2026-08-31

Status: paper theorem.  This note gives a second exact finite A0 selector.  It
does not first exhaust the occurrence invariant queue of v405.  Instead it
uses a physical separating dual to request one rank-raising conjugate of one
of the 44 compact relators.  The correction request is reduced to the actual
weighted singleton-fibre oracle of v142--v143.  The remaining boundary request
is still the exact six-action oracle of v404.

The theorem does not assert that the current actual dual has a small adjoint
support.  A production run must print that support and the resulting weights;
a capped adjoint expansion is `UNKNOWN_RESOURCE`, never a zero-correlation or
A0 nonmembership claim.  No common word, compatible lift, fake, or Ihara
witness is asserted here.  `verified=false`.

## 1. Frozen finite problem

Let (F=F(x,y)), let

\[
 \Theta:F\twoheadrightarrow\Delta
\tag{1.1}
\]

be the accepted task176/task198 linked roof, and let

\[
 \mathcal R_{\rm pc}=\{r_1,\ldots,r_s\},\qquad s\leq44,
\tag{1.2}
\]

be the accepted compact literal presentation roster of v397/v405.  Thus

\[
 \langle\!\langle\mathcal R_{\rm pc}\rangle\!\rangle_F
 =\ker\Theta.
\tag{1.3}
\]

Write (C_i(\delta)) for the raw physical eleven-occurrence Fox column of
the literal conjugate

\[
 u_\delta r_i u_\delta^{-1},
 \qquad \Theta(u_\delta)=\delta.
\tag{1.4}
\]

All occurrence signs, PB3 embeddings, right-correction prefixes, and the
normalized exponent pair are included in (C_i(\delta)).  If two section
words represent the same (\delta), their occurrence actors agree because
all ten context values agree.  Hence the notation is well-defined at the
column level used below.

Let

\[
 Q_{\rm ph}:Z\longrightarrow\bar Z
\tag{1.5}
\]

be the physical normal map obtained from the two PB3 maps of v401 and the
five-central-family PB4 map of v402, with the normalized exponent pair left
unchanged.  Let (D_0\leq\bar Z) be the remaining six-action PB4 space of
v404, and put

\[
 \bar C_i(\delta)=Q_{\rm ph}C_i(\delta),\qquad
 \bar T=Q_{\rm ph}T.
\tag{1.6}
\]

By v405, the exact A0 equation is

\[
 \boxed{-\bar T\in D_0+
 \operatorname{span}_{\mathbf F_3}
 \{\bar C_i(\delta):1\leq i\leq s,\ \delta\in\Delta\}.}
\tag{1.7}
\]

Equation (1.7), rather than occurrence-queue exhaustion, is the registered
search universe of this note.

## 2. Pull a physical dual back by the adjoint, not by a section

Let (B\leq\bar Z) be the span of the columns retained so far and suppose
the target remainder is nonzero.  Sparse elimination supplies

\[
 \lambda(B)=0,\qquad \lambda(-\bar T)=1.
\tag{2.1}
\]

Define the raw functional

\[
 \boxed{\widetilde\lambda=Q_{\rm ph}^{*}\lambda,
 \qquad
 \widetilde\lambda(v)=\lambda(Q_{\rm ph}v).}
\tag{2.2}
\]

This is an adjoint pullback.  It is not the sparse primal section
(\iota\lambda) used to apply quotient actors in v406.  In particular,

\[
 \langle\lambda,Q_{\rm ph}v\rangle
 =\langle\widetilde\lambda,v\rangle
\tag{2.3}
\]

is the required identity; replacing (Q_{\rm ph}^{*}) by a convenient
section need not satisfy it.

The raw ambient space is finite, so (\widetilde\lambda) has finite support.
The local (U_0,U_1) and noncentral quotient coordinates have a bounded
reverse dependency through the explicit triangular formulae of v401--v402.
The global `tau` coordinates may have large adjoint support and must be
handled explicitly or streamed.  They may not be silently deleted.  This is
an implementation cost distinction, not a mathematical exception to (2.2).

## 3. Exact weighted formula for one compact seed

The task198 occurrence ledger has eleven occurrences in ten linked context
coordinates.  Let (o) be one occurrence, let (j(o)\in\{0,\ldots,9\})
be its context coordinate, and let (P_o) be its frozen physical Fox prefix.
For seed (r_i), write the already-prefix-translated raw occurrence row as

\[
 S_{i,o}=L_{P_o}R_{i,o}
   =\sum_{a,h}d^{(i,o)}_{a,h}e_a(h).
\tag{3.1}
\]

Write the corresponding physical-block part of
(\widetilde\lambda) as

\[
 \widetilde\lambda_o=
 \sum_{a,g}\ell^{(o)}_{a,g}e_a(g)^*.
\tag{3.2}
\]

The source conjugator acts on (3.1) by

\[
 w_o(\delta)=P_o\pi_{j(o)}(\delta)P_o^{-1}.
\tag{3.3}
\]

A support pair ((a,h),(a,g)) contributes precisely when

\[
 w_o(\delta)h=g,
\tag{3.4}
\]

or equivalently

\[
 \boxed{
 \pi_{j(o)}(\delta)=P_o^{-1}g h^{-1}P_o.}
\tag{3.5}
\]

Here (h) is the support key of the already-prefix-translated row (3.1).
If the unprefixed gradient key is used instead, (3.5) reduces to the task179
implementation formula (P_o^{-1}g h^{-1}).  This fixes the apparent extra
right-(P_o) ambiguity.

Merge all eleven occurrences by the pair `(coordinate,target)`, add their
coefficients in (mathbf F_3), and delete zero sums.  The normalized
exponent pair of (r_i) is unchanged by conjugation and supplies a constant
term (K_i).  Equations (2.3)--(3.5) give

\[
 \boxed{
 F_i(\delta):=\langle\lambda,\bar C_i(\delta)\rangle
 =K_i+\sum_{(j,t)\in R_i}
 c^{(i)}_{j,t}{\bf1}_{\pi_j(\delta)=t}.}
\tag{3.6}
\]

### Lemma 3.1 (QUOTIENT-WEIGHTED CORRELATION)

Formula (3.6) is the complete physical quotient pairing.  It includes all
eleven occurrences, every same-target cancellation, both normalized exponent
coordinates, and every local or global coordinate of the physical dual.

#### Proof

Apply (2.3) to (C_i(\delta)).  For every group-coordinate summand, left
translation gives (3.4), whose unique solution is (3.5).  Summing its scalar
coefficient over all matching raw support pairs and then over all eleven
occurrences gives the indicator sum in (3.6).  The exponent pair is invariant
under conjugation, hence contributes (K_i).  There are no other coordinates
in the frozen physical ABI.  Therefore the formula equals the full pairing.

Notice that this proof permits a large support for (Q_{\rm ph}^{*}\lambda).
It proves exactness, not a small-support estimate. \(\square\)

Every proposed value from (3.6) must be checked once more by constructing
the literal word (1.4), replaying its raw eleven-occurrence column, applying
(Q_{\rm ph}), and comparing the direct scalar with (3.6).  Thus an error in
the formula compiler cannot promote a positive column.

## 4. The actual finite correction oracle

Task176 gives

\[
 |\Delta|=357{,}128{,}352,
 \qquad
 (|\ker\pi_0|,\ldots,|\ker\pi_9|)
 =(9,9,9,9,9,1,1,1,3,3).
\tag{4.1}
\]

For the merged formula (3.6), put

\[
 W_i=\sum_{(j,t)\in R_i}|\ker\pi_j|.
\tag{4.2}
\]

V142 constructs one literal preimage of every nonempty singleton fibre, and
the authenticated kernel roster completes that fibre in at most nine words.
V143 therefore gives the following exact schedule.

1. If (K_i=0), enumerate the complete union of the singleton fibres in
   (3.6).  Outside that union (F_i=0); hence exhaustion proves
   (F_i\equiv0).
2. If (K_i\ne0) and (W_i<|\Delta|), evaluate any (W_i+1) distinct
   authenticated global states.  At least one is outside the support union
   and therefore has value (K_i\ne0).
3. If (K_i\ne0) and (W_i\geq|\Delta|), a complete global roster or an
   independently proved sharper union certificate remains exact.  A bounded
   stop before either one completes is `UNKNOWN_RESOURCE`.

Duplicate states reached through different fibres are evaluated once, but
this is only an optimization.  Every ACTIVE result carries the literal
section word (u_\delta) and is accepted only after the direct replay below
Lemma 3.1.

### Theorem 4.1 (COMPLETE COMPACT-CORRECTION SEPARATION)

For a fixed physical dual (\lambda), complete execution of the schedule
above for all (s\leq44) seeds has exactly two possible mathematical
outcomes:

- it returns a literal column (\bar C_i(\delta)) with nonzero pairing; or
- it proves that (\lambda) annihilates the complete correction space in
  (1.7).

#### Proof

V143 decides whether each exact function (3.6) is identically zero.  If all
are zero, (\lambda) vanishes on every conjugate of every compact seed.
By (1.3), every joint-kernel word is a product of such conjugates and their
inverses.  The Fox occurrence map is additive on the joint kernel, so their
columns span the correction term of (1.7).  Conversely, a nonzero value of
(3.6) is by definition a nonzero pairing with a genuine correction column.
\(\square\)

## 5. Dual-guided A0 decision without occurrence BFS

Start a physical echelon with any authenticated correction prefix, or with
the empty span.  Repeat:

1. reduce (-\bar T); if it is zero, recover coefficients and run the full
   v403/v406 literal positive replay;
2. otherwise construct (\lambda) as in (2.1);
3. run v404.  An ACTIVE six-action row is inserted and the loop restarts;
4. if the v404 accumulator is empty, run Theorem 4.1.  Insert its first
   ACTIVE correction column and restart;
5. only if v404 is empty and all 44 correction functions are completely
   proved zero, return the dual as an exact A0 separator.

### Theorem 5.1 (DUAL-GUIDED FINITE A0 SELECTOR)

The complete schedule above decides (1.7) after finitely many strict physical
rank rises.  It does not require the v405 occurrence invariant queue to
exhaust.

#### Proof

Every row returned in steps 3 or 4 pairs nontrivially with a dual which
annihilates the current echelon, so its insertion strictly raises physical
rank.  The ambient \(\bar Z\) is finite-dimensional.  If the target never
becomes zero, the process reaches a dual for which neither oracle returns a
row.  V404 then proves annihilation of all of (D_0), and Theorem 4.1 proves
annihilation of the complete correction span.  Since the same dual is
nonzero on the target, it is an exact separator for (1.7).  \(\square\)

The sequence-65 occurrence checkpoint remains a valid word-bearing positive
prefix and may be used as a warm start.  It is no longer a logical prerequisite
for Theorem 5.1.  In particular, its nonempty frontier does not define a
missing completion percentage for this selector.

## 6. Production and claim boundary

The first production version must expose, for every dual round:

- physical rank and target-remainder digest;
- the exact nonzero target pairing of (\lambda);
- the (Q_{\rm ph}^{*}) expansion count, separated by PB3, PB4, `tau`, and
  exponent coordinates;
- for each visited compact seed, (K_i), number of merged targets, (W_i),
  and the chosen v143 branch;
- every literal `delta_word`, its ten coordinate values, direct eleven-
  occurrence scalar, and whether it raised rank; and
- a checkpoint after every retained rank rise.

The implementation must not call `normal_section` a dual adjoint, must not
infer zero from an adjoint/support cap, and must not interpret the old
task179 19,200-second complete-boundary stop as a correction-oracle failure.
That old bottleneck is replaced here by v401/v402/v404; only its authenticated
weighted-fibre machinery is reused.

```text
COMPACT NORMAL GENERATORS:                    <= 44 / ACCEPTED INPUT
ELIMINATED PB3 + CENTRAL-PB4 BOUNDARIES:      CLOSED NORMAL MAPS
REMAINING SIX-ACTION BOUNDARY:                EXACT v404 ORACLE
QUOTIENT DUAL -> RAW CORRELATION:             ADJOINT Q_ph^*, PAPER PROOF
ALL CONJUGATES OF ONE SEED:                   EXACT v142/v143 FIBRE ORACLE
OCCURRENCE INVARIANT BFS:                     NOT REQUIRED BY THIS SELECTOR
ACTUAL ADJOINT WEIGHTS FOR CURRENT A0 DUAL:   NOT YET MEASURED
ACTUAL A0 MEMBER/NONMEMBER:                   NOT YET COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:       NONE
```

`R07_A0_QUOTIENT_WEIGHTED_ACTOR_COLUMN_GENERATION_V409_PAPER_GRADE`
