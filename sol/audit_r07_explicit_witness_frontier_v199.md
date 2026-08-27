# R07 explicit-witness frontier checkpoint v199

Author: Sol / 2026-08-28

Purpose: durable no-backtracking checkpoint after v194--v198 and the second
independent audits of tasks 197 and 198.  It supersedes the production order
in v192 where the universal boundary was still written as an undifferentiated
search for \(q\).  No compatible lift, fake certificate, or Ihara witness is
declared.

## 1. Frozen arithmetic and source data

The branch remains zero-based roof row 36.  The already fixed data are:

\[
 972=324+648,
\tag{1.1}
\]

where the named arithmetic subsets have total size 324 and row 36 is in the
648-element complement, and

\[
 g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108}.
\tag{1.2}
\]

Its freely reduced length is 760, its exponent vector is \((0,0)\), and its
signed-word SHA-256 is

~~~
518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
~~~

The 648 typing and \(g_{760}\) are not current search variables.

## 2. Exact mathematical chain now fixed

### 2.1 First pointed coefficient

V188 constructs the genuine first diagonal successor from a complete
6,441-relator marked roof presentation.  Its pointed gate is

\[
 e_1\in I_0(A_1d_1+A_1e_1).
\tag{2.1}
\]

A positive word-bearing ancestry

\[
 e_1=\alpha d_1+\beta e_1
\tag{2.2}
\]

returns the ordered finite coefficient

\[
 \mu_1=\left(\sum_{r=0}^{2t}\beta^r\right)\alpha.
\tag{2.3}
\]

V191 then compiles the ancestry, without a second blind word search, to

\[
 M_0=\sum_i a_i(U_i-V_i),
 \qquad
 \pi_0(U_i)=\pi_0(V_i),
 \qquad
 M_0\mapsto\mu_1.
\tag{2.4}
\]

### 2.2 The universal gate is exactly three endpoints

V193 is retracted.  Its seven separate occurrence-endpoint requirement was
too strong.

V194 proves that the universal boundary identity is equivalent to the three
combined printed-relation endpoints

\[
 \boxed{
 \eta_{H1}(M)=\eta_{H2}(M)=\eta_P(M)=0.}
\tag{2.5}
\]

The eleven occurrences are evaluated separately and only then combined
inside H1, H2, and P.  Cancellation between occurrences in one relation is
load-bearing.

V198 gives the endpoint-only formula

\[
 \eta_B(M)=\epsilon_B-
 \sum_{o\in B}\sigma_oP_o
 \sum_i a_i(\rho_o(U_i)-\rho_o(V_i))\xi_o.
\tag{2.6}
\]

Thus the first universal decision uses only PB word values, fixed prefixes,
and sparse endpoints.  It does not expand multiplier Fox gradients or
enumerate translated boundary rows.  Full faithful Artin-action tuples give
exact PB3/PB4 bucket keys.

### 2.3 Same-successor repair has one orbit parameter

If (2.5) fails for the canonical \(M_0\), v195 identifies all representatives
of the same \(\mu_1\) as

\[
 M_0+J_1,
 \qquad
 J_1=\ker(k[F(x,y)]\to k[\Delta_1]).
\tag{2.7}
\]

V196 replaces the two-independent-word normal-relator columns
\(A(s-1)B\), for the actual free source, by a complete Schreier basis
\(\{h_j\}\) of \(\ker(F(x,y)\to\Delta_1)\):

\[
 J_1=\sum_j k[F(x,y)](h_j-1).
\tag{2.8}
\]

Hence repair is exactly

\[
 \eta(M_0)\in
 \operatorname{span}_{\mathbf F_3}
 \left\{\mathcal E_d(A(h_j-1)):A\in F(x,y)\right\}.
\tag{2.9}
\]

This is one infinite orbit parameter \(A\), not independent \(A,B\).
A fair dovetail finds every finite positive repair.  A bounded failure or
partial Schreier stream remains UNKNOWN.

V198 computes each repair column endpoint-only:

\[
 \mathcal E_d(A(h_j-1))_B
 =
 \sum_{o\in B}\sigma_oP_o
 \rho_o(A)(\rho_o(h_j)-1)\xi_o.
\tag{2.10}
\]

The finiteness of \(\Delta_1\) does **not** make the remaining \(A\)-orbit
finite.  The maps \(\rho_o\) in (2.10) take values in the exact presentation
groups \(PB_3\) and \(PB_4\), not in the finite successor.  Replacing those
values by their finite roof images would be a quotient screen and could
create a false zero endpoint.  Any finite-orbit selector therefore needs an
additional proved factorization of this actual class; it cannot be inferred
from \(|\Delta_1|<\infty\).

### 2.4 A zero endpoint deterministically yields \(q\)

V197 removes a second universal boundary search.  For each block, a finite
zero-endpoint chain is decomposed into fundamental cycles of a finite Cayley
subgraph.  Each identity loop is reduced with an annotated van Kampen trace,
and Fox differentiation returns an explicit finite chain:

\[
 D_{2,B}q_B=z_B(M).
\tag{2.11}
\]

Generic enumeration of products of conjugates of the original finite
relator roster proves that the positive trace extraction terminates.  An
annotated rewriting engine is the practical implementation.

Therefore, after (2.5), do not launch a fresh full-\(D_2\) translate search.
Compile \(q_{H1},q_{H2},q_P\) by v197 and replay (2.11).

### 2.5 Relative pro-3 closure

The finite universal pair \(M,q\) gives the same multiplier identity at
every registered matched relative pro-3 quotient by v191.  V174 then gives

\[
 c_\infty=-\sum_{r\ge0}\mu^ra
\tag{2.12}
\]

subject to the retained word-bearing and nonlinear side gates.

This closes only the relative pro-3 lane.  Prime-to-three formation
membership and genuinely nonabelian perfect-core accepted sets remain
separate.

## 3. Current computational gates

### 3.1 Task191 supporting boundary lane

Task191 PRODUCTION run

~~~
run  33109346940
head d68580936b2981b7de41dea4cb3f199e742fde62
~~~

was still in the GAP computation step at this checkpoint.  It decides the
complete first-roof boundary membership of the two exactification directions
\(u_0,v_0\).  It is a supporting shortcut for the normalized first common
word, not the first-successor multiplier \(\mu_1\), and not the universal
endpoint test (2.5).

### 3.2 Task192/task199 exact common word

The previous task192 PRODUCTION run failed because the production basis
called a nonexistent cache owner.  It emitted no receipt and no mathematical
result.  Task199 has returned a repair candidate for the exact cache
invalidation order, owner typing, resume replay, memory caps, and
production-shaped SELFTEST; a fresh independent static audit is pending.

No task192 repair is eligible for commit or GHA until a fresh independent
static audit passes.

### 3.3 Task197 adapter

The second independent static audit stopped the repaired task197 version.
Load-bearing defects included undefined seal calls, stale task192 pins,
broken GAP substring checks, a SELFTEST which did not traverse the production
PREPARE/FINALIZE path, and mutations which changed unused keys.  A repair is
in progress.

Task197 must be repinned only after task199 fixes the final task192 bytes.
No current task197 file is eligible for commit or GHA.

### 3.4 Task198 roof presentation

The second independent static audit also stopped task198.  Its task176
artifact member and receipt field were misread, the claimed order proof was
not executed, the 11-occurrence action ledger was incomplete, resource/resume
did not implement a real continuation, and the SELFTEST was unreachable.
A full repair is in progress.

No current task198 file is eligible for commit or GHA.

## 4. Fixed shortest production order

The shortest path is:

1. finish task199, independently audit it, run GHA SELFTEST, and rerun
   task192 PRODUCTION;
2. on a positive exact word, run the independently accepted task197 adapter
   and task193 production;
3. accept task198 only after its complete roof presentation and action
   interface pass independent audit and GHA SELFTEST;
4. apply v188 to compute the actual \(\Delta_1,K,d_1,e_1\) and pointed
   ancestry;
5. compile \(\mu_1,M_0\) by v191;
6. compute the three endpoints by v198;
7. on a nonzero endpoint, use only the same-successor repair spaces
   (2.9)--(2.10); on zero, skip repair;
8. compile and replay \(q_{H1},q_{H2},q_P\) by v197;
9. apply v174 to the relative pro-3 lane; and
10. discharge formation, prime-to-three, nonlinear, and perfect-core gates
    before any fake/Ihara declaration.

Task191/task194 may improve Step 1's exactification lane in parallel, but
they do not replace Steps 2--8.

## 5. No-backtracking rules

1. Do not recompute the 648 complement, row 36, or \(g_{760}\).
2. Do not revive v193's seven separate endpoint tests.
3. Do not search for \(q\) before computing the three endpoints.
4. Do not run a translated-boundary membership search after the endpoints
   pass; use v197 proof extraction.
5. Do not restart a blind multiplier word search after a pointed ancestry;
   compile \(M_0\) by v191.
6. If \(M_0\) fails, preserve \(\mu_1\) and repair only inside \(M_0+J_1\).
7. Do not call a bounded repair failure nonmembership.
8. Do not identify task191's \(u_0,v_0\) result with \(\mu_1\).
9. Do not commit or run tasks 192, 197, or 198 on an agent's self-report;
   require a separate static audit and then GHA SELFTEST.
10. Do not infer an all-prime witness from the relative pro-3 closure.
11. Do not truncate the repair orbit by reducing \(\rho_o(A)\) to the finite
    roof or successor; endpoint equality is exact in \(PB_3/PB_4\).

## 6. Current frontier

~~~text
NAMED NONARITHMETIC ROW 36 / g760:                  FROZEN
POINTED ANCESTRY -> FINITE WORD-PAIR M0:            PAPER_PROOF
UNIVERSAL BOUNDARY IFF THREE COMBINED ENDPOINTS:    PAPER_PROOF
ENDPOINT-ONLY / FAITHFUL-ARTIN DECISION:            PAPER_PROOF
SAME-mu1 REPAIR AS ONE-SIDED SCHREIER ORBIT:        PAPER_PROOF
ZERO ENDPOINT -> EXPLICIT q COMPILER:               PAPER_PROOF
TASK191 U0/V0 PRODUCTION:                           GHA IN PROGRESS
TASK192 EXACT COMMON WORD:                          NOT OBTAINED
TASK197 ADAPTER:                                    STATIC REPAIR
TASK198 COMPLETE ROOF INTERFACE:                    STATIC REPAIR
ACTUAL DELTA1 / K / d1 / e1:                       NOT COMPUTED
ACTUAL mu1 / M0:                                    NOT COMPILED
ACTUAL THREE ENDPOINTS / REPAIR / q:                NOT COMPUTED
RELATIVE PRO-3 COMPATIBLE R07 LIFT:                 NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE COFINAL GATES:            OPEN
FAKE / IHARA WITNESS:                               NOT DECLARED
~~~

R07_EXPLICIT_WITNESS_FRONTIER_V199_FIXED
