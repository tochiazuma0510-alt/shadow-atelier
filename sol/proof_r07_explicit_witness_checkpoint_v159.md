# R07 explicit-witness no-backtracking checkpoint v159

Author: Sol / 2026-08-27

Status: current restart map after v115 and v140--v158.  This note records
proved reductions, live production runs, and the shortest remaining route.
It creates no new positive machine receipt and declares no compatible full
lift, fake, or Ihara witness.

## 0. Fixed goal and finite roof

The goal is one compatible original-profinite R07 lift whose roof coordinate
is the already named nonarithmetic row 36.  The explicit finite base remains

\[
 \boxed{g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108}}
\tag{0.1}
\]

with freely reduced length 760, exact exponent \((0,0)\), and signed-word
SHA-256

~~~text
518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
~~~

The correction convention is right multiplication.  Zero-based roof row 36
lies outside both arithmetic order-324 candidates and is therefore a named
nonarithmetic row at the v76/v95 evidence grade.  The 648 nonarithmetic
count and this named row are not to be recomputed as part of the lift search.

## 1. Live GHA runs and the completed task169 bootstrap

Tasks 175 and 179 are production calculations with no terminal result yet.
Task169 has completed only its preflight bootstrap; it did not run the full
joint coefficient intersection.

| task | run | pinned head | state and exact scope |
|---|---:|---|---|
| 169 | 33046437210 | 76c059c94bac4131f7f9778cc90f839610e722a1 | completed preflight only; projected target6 / \(j=9\) joint-kernel machinery |
| 175 | 33059240825 | 9ec72d68f3ba99fbfe2d2bebfd5d78e0dcf2deea | in progress; raw common H1/H2/ordered-pentagon bridge |
| 179 | 33059993513 | 3d5bd79e9c4647e1166d5f5c8cd73d4d21889525 | in progress; positive-only full all-seven common-word column generation |

Run 33046437210 completed successfully at the workflow level and uploaded
artifact digest

~~~text
sha256:403167b7aa199ef76676328235f5c712c8499f4ddb53caab5c150aa52e0824a0
~~~

Its two producer outputs were byte-identical and the helper-nonshared checker
passed with \(\operatorname{rank}B_{\rm joint}=26\), 31 exact-transition
canaries, and 23 rejected receipt mutations.  The receipt nevertheless says
`terminal=None` and `full=false`.  Thus it authenticates the task169 input
builder and checker; it supplies no coefficient-intersection answer, common
word, or lift.

Task169 is not literal A.18 and cannot by itself produce the witness.
Task175 is a preflight, not a relation solution.  Task179 is the first live
word-bearing all-seven positive search.

Every resource terminal is UNKNOWN_RESOURCE with a resumable checkpoint.
It is not a separator.  No run is positive before its artifact and
helper-nonshared checker receipt have both been audited.

Task185 was repaired to an honest STATIC_STOP/UNKNOWN_INPUT at commit
13edb5f1.  It must not be run and supplies no arithmetic coordinate.

## 2. Exact task179 exponent correction

V156 reconstructed all

\[
 6318+104+19=6441
\tag{2.1}
\]

registered kernel rows and proved

\[
 \boxed{
 \epsilon(\Omega)=18\mathbf Z^2,\qquad
 G_{\rm joint}^{\rm ab}\cong C_{18}\times C_{18}.}
\tag{2.2}
\]

An independent static replay agreed on all packed one-based conventions,
all 19 relators, all 16 exponent vectors, and the Smith data.

Consequently task179 v1's current two rows

\[
 \epsilon(w)\bmod3
\tag{2.3}
\]

are identically zero on every correction column.  The correct first-edge
rows are

\[
 \boxed{\nu([w])=\frac{\epsilon(w)}{18}\bmod3.}
\tag{2.4}
\]

The fixed word-bearing basis is obtained from lifted Q0 rows
\(r_3,r_9,r_{12}\):

\[
 v_0=r_9r_{12}r_3^{-2},\qquad
 u_0=r_9v_0^{-8},
\tag{2.5}
\]

\[
 \epsilon(v_0)=(0,18),\qquad
 \epsilon(u_0)=(18,0).
\tag{2.6}
\]

If a v1 positive word \(c_*\) has exponent in \(54\mathbf Z^2\), v156
exactifies it immediately by registered cubes.  If its exponent is outside
\(54\mathbf Z^2\), only that coefficient solution fails the zero-cost test;
the whole relation fibre is not thereby empty.  Task186 is the versioned
successor which rebuilds task179 with (2.4).  The v1 production files remain
frozen while their current GHA run finishes.

The first task186 delivery was rejected by parent audit: it was a toy
exactifier which always returned `UNKNOWN_INPUT`, not a successor carrying
the 6,441-word production schedule, column generation, or resumable state.
No GHA run was launched from it.  A full v1-preserving normalized successor is
being rebuilt; until that repair is audited, `TASK186` means design/paper
theorem only, not an executable production search.

## 3. Closed all-rung results

Let

\[
 \Omega_{n+1}=\Phi_{\ell_n}(\Omega_n),\qquad
 P_{n+1}=\Phi_{\ell_n}(P_n),\qquad
 m_n=\prod_{i<n}\ell_i,
\tag{3.1}
\]

where every prime occurs infinitely often.

The following are paper theorems and must not be reopened without a specific
counterexample.

1. **Sequential compatibility.**  Corrections chosen successively in
   \(\Omega_n\) form a compatible nested product.  V129 shows that no
   additional global choice problem remains once every edge is solved.
2. **Solvable-relative cofinality.**  V155 proves that the mixed-prime tower
   dominates every finite refinement whose relative kernel is solvable.
3. **Formation residual and selector.**  At every rung,

   \[
   R_S(F/\Omega_n)=P_n/\Omega_n,\qquad
   \rho_n:\Omega_n/\Omega_{n+1}\twoheadrightarrow P_n/P_{n+1}
   \tag{3.2}
   \]

   is the literal inclusion-and-Schreier selector.
4. **All-rung exponent lattice.**  V157 proves

   \[
   \epsilon(\Omega_n)=18m_n\mathbf Z^2
   \tag{3.3}
   \]

   and supplies explicit basis recursion
   \(u_{n+1}=u_n^{\ell_n}\),
   \(v_{n+1}=v_n^{\ell_n}\).
5. **Formation--charming factorization.**  V158 strengthens (3.3) to

   \[
   \epsilon(P_n)=\epsilon(\Omega_n)=18m_n\mathbf Z^2
   \tag{3.4}
   \]

   and proves

   \[
   \boxed{\bar\epsilon_n^\Omega
   =\bar\epsilon_n^P\circ\rho_n.}
   \tag{3.5}
   \]

   Hence exact charmingness is not a third independent target-membership
   gate on a formation-purified edge.

The papers establishing (2.2)--(3.5) were fixed at commits 791e65da and
9967ea86.

## 4. The two genuinely open mathematical gates

The remaining problem is not compatibility, exponent correction, prime
scheduling, or construction of the formation quotient.

### Gate A: actual relation target membership

On the direct branch the edge problem is

\[
 \boxed{
 (B_n,\bar\epsilon_n^\Omega)(c_n)=(-\beta_n,0).}
\tag{4.1}
\]

At rung zero this is task186.  On a formation-purified branch, once the
actual reference displacement \(\eta_n\) is supplied, v158 reduces it to

\[
 \boxed{
 (B_n,\rho_n)(c_n)=(-\beta_n,\eta_n),}
\tag{4.2}
\]

with no extra charming row.  Neither (4.1) at all rungs nor (4.2) at all
rungs has yet been proved.  One finite success does not imply either
all-rung statement.

The class-specific Hensel, Tor/Smith, and graded-homotopy theorems
v124--v133 give exact finite selectors once the actual transition error is
materialized.  They do not prove that its class vanishes.

### Gate B: the perfect relative core

V155 is cofinal for solvable relative kernels only.  An arbitrary finite
relative kernel stabilizes under mixed-prime iteration at a perfect core.
Its nonabelian simple chief factors require the typed strip/accepted-set
theory.  V35, v48, v49, and v52 reduce these factors and peel all tree-like
strip constraints, but do not prove every remaining incidence 2-core has a
solution.

Thus a fully original-profinite witness still needs either:

1. a theorem that every actual perfect-core accepted set met by the chosen
   branch is nonempty; or
2. an alternative cofinal construction which absorbs those perfect cores
   without assuming solvability.

No linear or Frattini argument alone can remove a nontrivial perfect group.

## 5. Fixed forward order

1. Audit the full repaired task186 implementation; reject any route which
   merely returns a predetermined resource or input terminal.
2. Audit the first terminal among tasks 175 and 179.
3. If task179 prints COMMON_WORD, compute its integer exponent: accept zero;
   apply v156 for \(54\mathbf Z^2\); otherwise retain the positive relation
   checkpoint and continue task186 with normalized rows.
4. If task179 prints UNKNOWN_RESOURCE, authenticate and resume its
   checkpoint; do not infer a negative result.
5. Run repaired task186 and retain

   \[
   \dim\bar\epsilon_0^\Omega(\ker B_0)
   =\operatorname{rank}(B_0,\bar\epsilon_0^\Omega)
    -\operatorname{rank}(B_0),
   \tag{5.1}
   \]

   together with word-bearing preimages.  Dimension two would prove that
   every nonempty relation fibre contains all normalized exponent residues.
6. After the first exact common word, materialize the first actual
   transition error and apply the v129/v131 class-specific selector.
7. At a perfect-core edge, compute the actual strip incidence graph and
   apply v52 peeling before any nonlinear enumeration.
8. Only after one nested cofinal branch has passed both gates may its row-36
   projection be promoted to an Ihara counterexample witness.

## 6. Current ledger

~~~text
NAMED NONARITHMETIC ROOF ROW 36:                    CLOSED PAPER-RELATIVE
EXPLICIT g760 BASE:                                 FIXED
TASK169 PROJECTED-j9 PREFLIGHT:                     CHECKER PASS / FULL UNRUN
TASK175 RAW ALL-SEVEN BRIDGE:                       GHA IN PROGRESS
TASK179 FIRST WORD-BEARING ALL-SEVEN SEARCH:        GHA IN PROGRESS
TASK179 RAW EXPONENT ROWS:                          PROVED VACUOUS
EXACT NORMALIZED FIRST-EDGE SELECTOR:               PAPER_PROOF
TASK186 NORMALIZED PRODUCTION SEARCH:               REBUILD AFTER AUDIT REJECTION
ALL-RUNG EXACT-CHARMING SELECTOR:                   PAPER_PROOF
ALL-RUNG FORMATION SELECTOR:                        PAPER_PROOF
FORMATION => CHARMING FACTORIZATION:                PAPER_PROOF
SOLVABLE-RELATIVE MIXED-PRIME COFINALITY:           PAPER_PROOF
FIRST EXACT ALL-SEVEN COMMON WORD:                  NOT YET CONSTRUCTED
ALL-RUNG ACTUAL RELATION TARGET MEMBERSHIP:         OPEN
PERFECT-CORE ACCEPTED-SET NONEMPTINESS:             OPEN
COMPATIBLE ORIGINAL-PROFINITE R07 LIFT:             NOT CONSTRUCTED
FAKE / IHARA WITNESS:                               NOT DECLARED
~~~

R07_EXPLICIT_WITNESS_NO_BACKTRACKING_CHECKPOINT_V159
