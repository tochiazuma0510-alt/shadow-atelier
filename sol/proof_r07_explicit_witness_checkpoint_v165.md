# R07 explicit-witness no-backtracking checkpoint v165

Author: Sol / 2026-08-27

Status: current restart map after v159--v164 and the task186/task187 GHA
repairs.  It records exact completed reductions, live runs, and the remaining
logical gates.  It declares no production result from a still-running job and
no compatible cofinal lift, fake, or Ihara witness.

## 1. Frozen base and arithmetic typing

The target remains the original-profinite R07 branch with zero-based roof row
36.  The explicit finite base is

\[
 \boxed{g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108}},
\tag{1.1}
\]

with freely reduced length 760, exponent vector ((0,0)), and signed-word
SHA-256

```text
518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
```

Row 36 is outside both named arithmetic order-324 subsets at the accepted
v76/v95 evidence grade.  The 648 nonarithmetic count, the identity of row 36,
and (1.1) are frozen inputs.  They are not part of the current search.

## 2. Exact first-edge normalization

The authenticated 6,441-word joint kernel satisfies

\[
 \epsilon(\Omega)=18\mathbf Z^2.
\tag{2.1}
\]

The two task179 raw rows (epsilon(w)\bmod3) therefore vanish on every
correction column.  The correct normalized rows are

\[
 \boxed{\nu(w)=\epsilon(w)/18\bmod3.}
\tag{2.2}
\]

With the frozen q0 relators,

\[
 v_0=r_9r_{12}r_3^{-2},\qquad u_0=r_9v_0^{-8},
\tag{2.3}
\]

\[
 \epsilon(v_0)=(0,18),\qquad\epsilon(u_0)=(18,0).
\tag{2.4}
\]

V157 propagates this lattice to the mixed-prime Frattini tower:

\[
 \epsilon(\Omega_n)=18m_n\mathbf Z^2,
 \quad u_{n+1}=u_n^{\ell_n},
 \quad v_{n+1}=v_n^{\ell_n}.
\tag{2.5}
\]

Thus exact charmingness and compatible exponent exactification are closed
paper theorems.  Actual relation target membership is not.

## 3. The two current first-edge routes

### 3.1 Boundary-preimage shortcut (task187)

Task187 decides the two complete translated-boundary memberships

\[
 A_C(u_0)+A_D(d_u)=0,
 \qquad
 A_C(v_0)+A_D(d_v)=0.
\tag{3.1}
\]

V161 proves that two positive certificates imply

\[
 \nu(\ker A)=\mathbf F_3^2
\tag{3.2}
\]

and normalize any raw task179 positive coefficient in closed form before
cube exactification.  V163 proves that task187's complete support-inversion
correlation gives an exact positive/negative membership decision when no
resource cap interrupts it.  A negative answer closes only this particular
(u_0/v_0) shortcut; it does not prove (3.2) false for every kernel basis.

The final task187 bundle passed GHA SELFTEST run `33075481646` at commit
`257d01e154f020901d24b96599da5a9602e58913`.  Production run
`33075593185` is in progress from the same commit.  It has no result yet.

### 3.2 Full normalized column generation (task186)

Task186 is the full task179-preserving successor using (2.2), a rank-zero
authenticated resume, word-bearing kernel ancestry, and the exactification
(2.3)--(2.4).  GHA SELFTEST run `33074806414` passed producer, independent
checker, driver, and artifact upload.  After the generated-shell formatting
repair, production run `33075481377` was launched from commit
`257d01e154f020901d24b96599da5a9602e58913` and is in progress.  It has no
result yet.

The earlier production dispatch `33075126811` was cancelled before a result
because the GAP stream writing long shell commands had print formatting
enabled.  Both drivers now call `SetPrintFormattingStatus(stream,false)`
before writing shell text.  This was a wrapper defect, not a mathematical
outcome.

## 4. Older live production runs

| task | GHA run | pinned head | exact status |
|---|---:|---|---|
| 175 | `33071125385` | `95af26f6f73bae0cda08dedd5a3da48a2120abfb` | rerun in progress; raw all-seven bridge; no result yet |
| 179 | `33059993513` | `3d5bd79e9c4647e1166d5f5c8cd73d4d21889525` | positive-only word-bearing all-seven search in progress; no result yet |
| 186 | `33075481377` | `257d01e154f020901d24b96599da5a9602e58913` | normalized exact production in progress; no result yet |
| 187 | `33075593185` | `257d01e154f020901d24b96599da5a9602e58913` | (u_0/v_0) boundary production in progress; no result yet |

Every resource terminal is `UNKNOWN_RESOURCE`, not nonmembership.  Every
positive terminal remains candidate until its uploaded receipt and
helper-nonshared checker are audited.

## 5. What one first-edge success does and does not prove

A first exact all-seven common word settles the first relative Frattini
edge and gives a literal coarse solution.  V144 compiles it into the named
error at the next edge; v129/v131 give an exact class-specific Hensel/Smith
selector once that error and transition module are materialized.  Sequential
corrections are automatically compatible because every later correction lies
in the next accumulated kernel.

One first-edge success does **not** imply that every later actual defect lies
in the corresponding image.  The still-load-bearing all-rung equation is

\[
 (B_n,\rho_n)(c_n)=(-\beta_n,\eta_n),
\tag{5.1}
\]

or the direct normalized equation when no formation coordinate is fixed.
V158 removes exact charmingness as a third independent formation-purified
gate; it does not prove (5.1).

V164 now proves a finite route to the stronger v133 hypothesis on a genuine
cyclic lane.  If H1, H2, every ordered A.18 occurrence, and every boundary
block are the complete deck translates of one fixed finite equivariant Fox
template, all cyclic levels are base changes of one matrix over
(k[[T]]).  One completed Smith test then decides all those cyclic levels at
once.  The R07 finite template audit and the completed Smith target test have
not yet been performed.  This theorem does not cover arbitrary mixed
Frattini or nonabelian-chief refinements.

## 6. The two genuinely open global gates

1. **Actual relation membership.**  Produce the first exact word, materialize
   each actual successor error, and prove its class passes the appropriate
   Hensel/Smith or relative-dihedral-even selector.  A completed Fox-template
   audit can replace infinitely many cyclic checks by one Smith calculation,
   but its target divisibility must still be shown.
2. **Perfect relative cores.**  The mixed-prime tower is cofinal for every
   finite solvable relative kernel.  A surviving perfect core has nonabelian
   simple chief factors.  V52 peels all tree parts and v77 decides simple
   cycle cores, but higher incidence cores and their split-onto accepted sets
   remain actual finite gates.

Only after a nested cofinal branch passes both gates may its row-36 projection
be promoted to an Ihara counterexample witness.

## 7. No-backtracking rules

1. Do not recompute the 648 arithmetic complement, row 36, or (g_{760}).
2. Do not use raw exponent modulo three; use (2.2).
3. Do not multiply PB3/PB4 boundary chains into a source correction word.
4. Do not promote a task187 negative answer beyond the shortcut (3.1).
5. Do not infer all-stage solvability from one finite common word.
6. Do not invoke v133 on R07 until the finite Fox-template audit and actual
   completed Smith test are both supplied.
7. Do not convert a resource stop or a restricted-prefix death into a global
   nonexistence statement.

```text
NAMED NONARITHMETIC ROW 36 / EXPLICIT g760:          FROZEN
EXACT NORMALIZED EXPONENT SELECTOR AT ALL RUNGS:     PAPER_PROOF
TASK175 / TASK179 / TASK186 / TASK187 PRODUCTIONS:   IN PROGRESS
TASK187 FINAL SELFTEST:                              PASS
FIRST EXACT ALL-SEVEN COMMON WORD:                   NOT YET CONSTRUCTED
CYCLIC FOX-TEMPLATE BASE-CHANGE THEOREM:             PAPER_PROOF
R07 FINITE TEMPLATE / COMPLETED SMITH TARGET:        NOT YET AUDITED
ALL-RUNG ACTUAL RELATION TARGET MEMBERSHIP:          OPEN
PERFECT-CORE ACCEPTED-SET NONEMPTINESS:              OPEN
COMPATIBLE ORIGINAL-PROFINITE R07 LIFT:              NOT CONSTRUCTED
FAKE / IHARA WITNESS:                                NOT DECLARED
```

`R07_EXPLICIT_WITNESS_NO_BACKTRACKING_CHECKPOINT_V165`
