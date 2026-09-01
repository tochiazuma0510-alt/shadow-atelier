# R07 A0 batch positive to task193/A2 carrier (v416)

Author: Sol / 2026-09-01

Status: paper interface theorem for the current Task451 positive ABI.  It
shows that a checker-accepted `COMMON_CANDIDATE` supplies the literal
`(g760, correction_word, corrected_word)` triple needed by task193 and the
A2 specializer.  It neither assumes that the active run is positive nor
changes the A0, lift, fake, or Ihara numerators.  `verified=false`.

## 1. The current positive object

Let `R` be a Task451 artifact with schema
`d972-r07-a0-dual-anchored-active-batch/v1`, and let `V` denote a successful
execution of the exact pinned Task451 checker on `R` and its physical compact
checkpoint.  Call `(R,V)` **positive-accepted** only when

```text
R.status = R.terminal = COMMON_CANDIDATE,
R.reason = null,
R.current_dual_profile = null,
R.claims.A0 = true,
checker terminal = R07_A0_DUAL_ANCHORED_ACTIVE_BATCH_V1_CHECKER_PASS.
```

The status name alone is not acceptance.  The checker reconstructs the
rank-51 prefix, every closed batch, every selected literal/action row, the
final echelon coefficients, and then requires its fresh call of the strict
positive routine to equal `R.terminal_replay`.

Write

\[
 a=R.\texttt{terminal_replay.literal\_word}.
\tag{1.1}
\]

Let `g0` be the literal `g760` word reconstructed from Task451's exact pinned
physical owner, and put

\[
 f=\operatorname{red}(g_0a).
\tag{1.2}
\]

Neither `g0` nor `f` should be guessed from a search transcript.  A portable
consumer reconstructs `g0`, checks the Task451 target row against that owner,
and computes (1.2) by free reduction.

## 2. What the positive replay proves

### Theorem 2.1 (TASK451 POSITIVE IS AN EXACT A0 CORRECTION)

For every positive-accepted `(R,V)`, the word `a` in (1.1)

1. has exact integer exponent pair `(0,0)`;
2. belongs to the registered ten-coordinate joint kernel;
3. has a freshly reconstructed all-seven physical row;
4. together with the selected six-action ancestry kills the physical A0
   target; and
5. is therefore an exact finite A0 correction in the sense of v403, and the
   word `f=red(g0*a)` is the corresponding exact corrected common word.

#### Proof

The strict positive routine reads the final echelon coefficients rather than
a producer Boolean.  It reconstructs every selected correction atom from its
seed and `delta_word`, treats coefficient two as inversion, and multiplies
the atoms in canonical order.  It then applies the registered v399
exactification words.  The routine explicitly checks

\[
 \operatorname{exp}(a)=(0,0),\qquad
 \rho_j(a)=1\quad(0\le j<10),
\tag{2.1}
\]

reconstructs the v12 row of `a`, and requires that row to equal the selected
correction sum.  It independently reconstructs every selected action row and
checks

\[
 T+C(a)+A_{\rm sel}=0
\tag{2.2}
\]

in the exact physical quotient.  The Task451 checker repeats the echelon and
positive computation and requires byte-for-byte equality with the terminal
replay.  Conditions (2.1)--(2.2) are precisely the five hypotheses of v403
Theorem 4.1: the PB3 closures and five central PB4 families are kernels of
the closed normal maps, while `A_sel` supplies the remaining six PB4 action
families.  Hence `a` is a legal exact correction and `f=red(g0*a)` is the
exact finite A0 common word. \(\square\)

The batch partition, frozen discovery duals, rejected dependent candidates,
and rank at which membership was discovered do not occur in the conclusion.

## 3. Normalized task193/A2 carrier

Define

\[
 \boxed{N_{451}(R,V)=(g_0,a,f,\omega)},
\tag{3.1}
\]

where `omega` consists of the checker-accepted positive ancestry together
with a fresh direct all-seven replay of `(g0,a,f)`.  The latter uses the
accepted task179/task198 evaluator and must establish

```text
corrected_word = freely_reduce(g760 + correction_word)
eleven_occurrence_replay = true
direct_all_seven_replay = true
right_g760_multiplication = true.
```

### Theorem 3.1 (BATCH-HISTORY EXTENSIONALITY)

The task193 compiler and v225 A2 specializer applied to (3.1) depend only on
the literal triple `(g0,a,f)`, its direct replay, and the accepted task198
word-independent occurrence/evaluator ABI.  They are independent of the
Task451 batch sizes, duals, pivots, selector targets, and discovery order.

#### Proof

Task193 consumes the applied correction word and the corrected word.  V225
constructs every occurrence value, prefix, sign, and PB residual by literal
substitution into `g0` and `f`; no search-basis datum appears in those
formulae.  Equation (1.2) fixes the right-multiplication convention, and
Theorem 2.1 supplies the legal exact A0 premise.  This is the same
extensional argument as v284 Theorem 4.1, with Task451 added as a third tagged
positive carrier dialect. \(\square\)

Different positive Task451 runs may return different words `a`.  The theorem
does not identify those words; it says that each accepted literal word gives
its own valid downstream specialization.

## 4. Minimal implementation boundary

The existing adapter-v5 is pinned to the old history-free-v22 envelope and
must not be relabelled.  A Task451 branch should instead consume the physical
Task451 result, checkpoint, checker log or portable checker verdict, and GHA
run/head/artifact binding as separate immutable owners.  Producer and checker
normalizers must independently:

1. exact-pin the Task451 producer, checker, checkpoint schema, source commit,
   and positive terminal;
2. reject every `UNKNOWN_RESOURCE`, `UNKNOWN`, non-PASS checker, or missing
   physical binding;
3. extract `a` only from the checker-equal `terminal_replay.literal_word`;
4. independently reconstruct the pinned `g0`, compare its target row with
   the terminal target row, and compute `f=red(g0*a)`;
5. run the direct all-seven evaluator on `(g0,a,f)` and require the four gates
   in Section 3; and
6. emit only the normalized task193-shaped `(g0,a,f,omega)` envelope.

No Q0 store, selector fibre, physical echelon, or batch replay belongs in the
downstream specialization after the upstream Task451 checker PASS has been
physically bound.  If portability policy requires the checker to be rerun
after artifact transfer, that rerun is an authentication step, not a new A0
search.

Mutation gates must change at least the Task451 terminal, result/checkpoint
hash, checker PASS binding, source head, `literal_word`, reconstructed `g0`,
free-reduced `f`, one all-seven occurrence, and action ancestry.  Each change
must fail at its narrow owner.

```text
TASK451 POSITIVE -> EXACT A0 CORRECTION:    PAPER-CLOSED VIA v403
TASK451 POSITIVE -> (g760,a,f) CARRIER:     PAPER-CLOSED
BATCH/DISCOVERY HISTORY NEEDED DOWNSTREAM:  NO
CURRENT ADAPTER-v5 ACCEPTS TASK451:         NO / NEW TAGGED BRANCH NEEDED
ACTUAL TASK451 POSITIVE:                    PENDING GHA
ACTUAL A2 / COMPATIBLE LIFT / FAKE / IHARA: UNCHANGED
```

`R07_A0_BATCH_POSITIVE_TO_TASK193_A2_CARRIER_V416_PAPER_GRADE`
