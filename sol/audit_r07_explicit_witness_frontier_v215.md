# R07 explicit-witness frontier checkpoint v215

Author: Sol / 2026-08-28

Purpose: durable no-backtracking checkpoint after v211--v214.  It supersedes
v199's order in which one arbitrary pointed multiplier was compiled before
running an endpoint screen.  The exponent-nine screen can now be applied to
all relative multipliers before pointed successor construction, and then
combined with the pointed equation in one finite span.  No compatible lift,
fake certificate, or Ihara witness is declared.

## 1. Frozen candidate data

The universe and branch remain unchanged.  For the accepted arithmetic image
\(A\),

\[
 972=324+648.
\tag{1.1}
\]

The two named candidate arithmetic subsets
\(A_9,A_{12}\subset X\) each have size 324, with

\[
 |A_9\cap A_{12}|=108,
 \qquad |A_9\cup A_{12}|=540.
\tag{1.1a}
\]

Their common outside
\(O=X\setminus(A_9\cup A_{12})\) has size 432.  The accepted arithmetic
image satisfies \(A\in\{A_9,A_{12}\}\), so \(|X\setminus A|=648\), but
the full 648-row complement depends on the unresolved orientation.
Zero-based row 36 lies in \(O\), hence is nonarithmetic for either
orientation.  This orientation-independent named row, and

\[
 g_{760}=w_2(w_3^{-1}w_2)^8y^{36}x^{-108}
\tag{1.2}
\]

are frozen.  Its exponent vector is \((0,0)\), freely reduced length is 760,
and signed-word SHA-256 is

~~~text
518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d
~~~

No current computation is allowed to reselect the row or replace this word.

## 2. What the old \(j=9\)--12 GHA run established

The target-six production run

~~~text
run  32901384400
head c1e7eb8fcd08676d5a6efad82add2c1c832a22c0
~~~

used 11,728 producer seconds and stopped with

~~~text
R07_760_L3_TARGET6_UNKNOWN_RESOURCE
stage = j=9:D2-relator-7
reason = shared wall-clock budget exhausted
~~~

Its first-terminal control flow reached \(j=9\) without a producer
NONMEMBER at \(j=2,\ldots,8\).  The stop receipt had
full_replay=false; therefore this is candidate progress only.  It gives no
membership or nonmembership assertion at \(j=9,10,11,12\), and neither kills
nor lifts \(g_{760}\).

That computation did not retain the lossless \(j=9\) resume state required
to avoid replaying the first 11,728 seconds.  It is not the current primary
lane.  A future resume must be a new authenticated checkpointed lineage; a
workflow-success label on run 32901384400 must not be read as mathematical
success.

## 3. Closed paper reductions

### 3.1 Exact first successor and pointed promotion

V188 proves how to obtain the first relative Frattini kernel from the
complete 6,441-relator roof presentation without enumerating the
357,128,352-element roof.  V184 reduces the first pointed equation to one
finite membership and gives the ordered finite Neumann coefficient.  V191
compiles a positive word-bearing ancestry directly to a finite roof-fibre
word-pair polynomial; there is no second blind word search.

### 3.2 Exact universal endpoint

V194 proves that the universal boundary condition is equivalent to the
three combined H1, H2, and P endpoints, not seven separate occurrence
conditions.  V198 evaluates these endpoints from exact PB word values.
V197 extracts finite boundary chains after an exact zero endpoint.  V195
and v196 describe every same-successor representative, but a bounded exact
PB orbit failure remains UNKNOWN.

The two affine freedoms must not be identified.  If

\[
 \Phi_1:k[F(x,y)]\longrightarrow k[\Delta_1],\qquad
 J_1=\ker\Phi_1,
\tag{3.1a}
\]

and \(\Phi_1(M_0)=\mu_1\), then

\[
 \Phi_1^{-1}(\mu_1)=M_0+J_1.
\tag{3.1b}
\]

Thus \(M_0+J_1\) changes only the source representative of one fixed
\(\mu_1\).  By contrast, the v214 joint gate varies the finite multiplier
itself through the allowed ideal \(I_0\) before choosing a source
representative.  V212 shows that the former freedom cannot change the
exponent-nine endpoint, whereas the latter is exactly the freedom used by
the 486-direction pre-gate.

### 3.3 Coherent class-two quotient

V211 identifies the exact roof defect of the exponent-nine joint quotient:

\[
 D_9\cong\mathcal H_2(9),\qquad |D_9|=729,
\tag{3.1}
\]

\[
 D_9/\langle[x,y]^3\rangle\cong\Gamma,\qquad |\Gamma|=243.
\tag{3.2}
\]

It is genuinely non-roof.  V212 proves that it factors through the first
successor, so every same-\(\mu_1\) source-representative direction has zero
exponent-nine endpoint image.  V213 extends this to compatible quotients

\[
 \Delta_n\twoheadrightarrow
 \mathcal H_2(3^{n+1})
\tag{3.3}
\]

at every rung and to one continuous quotient

\[
 \Delta_\infty\twoheadrightarrow\mathcal H_2(\mathbf Z_3).
\tag{3.4}
\]

This is a coherent class-two axis, not a full pentagon right inverse.

## 4. New strongest gate: all pointed multipliers at once

V214 moves the exponent-nine screen before arbitrary pointed-multiplier
selection.  At the first edge, put

\[
 c=[x,y]^3,\qquad R_0=\langle c\rangle\cong C_3.
\tag{4.1}
\]

Choose and retain a left-coset transversal
\(T\subset D_9\) for \(D_9/R_0\).  The complete relative-ideal image is

\[
 I(R_0)
 =\bigoplus_{t\in T}
 k\{t(c-1),t(c-1)^2\},
\tag{4.2}
\]

and therefore has exactly

\[
 243\cdot2=486
\tag{4.3}
\]

algebra-basis input directions.  After action by \(w\) and the block map
\(C\), their endpoint-image rank can be smaller and is only bounded above
by 486.  Let \(w\) retain the eleven signed,
prefix-conjugated occurrence endpoints and let \(C\) combine them only after
the occurrencewise action.

### Gate 4A: pre-pointed endpoint screen

As soon as the exact first correction and fixed residual endpoint exist,
but before \(d_1,e_1\) are built, decide

\[
 \bar\epsilon_1\in C(I(R_0)\odot w).
\tag{4.4}
\]

This is a complete finite test over all \(\mu_1\in I_0\).

- Nonmembership gives a quotient dual excluding every relative first
  multiplier for the fixed lower correction.
- Membership gives only an exponent-nine coefficient seed; it is not an
  exact PB endpoint pass.

### Gate 4B: simultaneous pointed / endpoint span

After v188 supplies word-bearing generators \(s_i\) of the actual first
kernel, close

\[
 \mathscr A_1
 \left\langle
 \bigl((s_i-1)d_1,(s_i-1)\odot w\bigr)
 \right\rangle
\tag{4.5}
\]

and test the single target \((e_1,\bar\epsilon_1)\).  A positive ancestry
returns one \(\mu_1\) satisfying both the pointed equation and the complete
exponent-nine endpoint screen.  A negative dual excludes every pointed
\(\mu_1\) for these fixed rows.

At a later edge, the same theorem is affine.  For a selected downstairs
\(\mu_m\), a lift \(\widetilde\mu_m\), and an unknown
\(\kappa\in I_m\), one tests

\[
 \left(
 e^{\rm raw}_{m+1}-\widetilde\mu_m d_{m+1},
 \bar\epsilon_{m+1}
 -C(\widetilde\mu_m\odot w)
 \right)
\tag{4.6}
\]

against the joint span of
\(\bigl((s_i-1)d_{m+1},(s_i-1)\odot w\bigr)\).
Membership is independent of the chosen lift.  An upper pass descends to a
lower pass; the converse is not asserted.

## 5. Current implementation gates

### 5.1 Task192 exact common word

The first repaired cached-v3 head 5107c8e3 failed closed in GHA SELFTEST
run 33126747887 before producer startup because the serial driver still
pinned the pre-append identity of the historical task186 reply.  All 17
driver pins were remeasured; the sole drift was

~~~text
old  11868 / 31325a2845e1e51f6535aae3c0a9942b11c2fb553a1bb4cb0c1eff88dab4fdeb
new  12246 / 307600e0435868c250143fb0691df443d9e957070fea72288cda7caaba5762e0
~~~

The task192 driver and downstream task197 pins were repaired, independently
audited GO, committed and pushed at

~~~text
08d23f0e19b2c8692ba320cac75f419dac4c8dcc
~~~

GHA SELFTEST run 33129356703 then completed successfully at that immutable
head.  The producer, helper-nonshared checker, and GAP driver emitted their
three matching SELFTEST PASS markers.  The receipt identity is

~~~text
126570 / a9031a1a949fabba0690e20083704e5d67c52725ba5a5187555b05913cdaef28
~~~

and all registered mutation families were rejected
\(18/18+19/19+15/15+8/8\).  Uploaded artifact 9669643959 has ZIP digest

~~~text
sha256:d10fac8810fc7542fb21031d0a8e3cfebb9783fce17857a009b1e6108db0b5f0
~~~

This cross-checks only the bounded SELFTEST.  These run, receipt, and
artifact identities are from the parent-side GHA/API and downloaded-artifact
audit; they were not independently artifact-audited as part of the static
v215 review.  PRODUCTION run 33129456772 was dispatched from the same head
with the registered 19,800-second producer envelope and a 360-minute
workflow limit.  As of 2026-08-28 09:25 JST, no authenticated common-word
or mathematical terminal had been recorded.

### 5.2 Task197 adapter

The cached-v3 to task193 adapter and its complete cascade repin passed a new
independent static audit: all task192 pins are current, all 16 driver pins
match, and the producer/checker mutation registries are identical at 55
distinct entries.  Its five-file bundle was committed in 08d23f0e.  This is
static readiness only.  GHA SELFTEST run 33129626120 then stopped before
producer startup because the GAP driver attempted to form a character-ended
Range.  The minimal string-allowlist repair has now passed independent static
re-audit: the exact path, scalar, digit, and hexadecimal alphabets preserve
GAP character-membership semantics and all 16 driver pins match.  GHA
SELFTEST run 33130846755 then completed successfully at immutable head
e1745e4e1b622379c0f14ad4a5e00c0e32d8a832.  The downloaded 3,276-byte
receipt has SHA-256
`c59e78d2425b066d3a4315b853e03f014febce477bd3699e3714ceb5fed553ba`;
producer, helper-nonshared checker, and driver markers agree, and all 55
registered mutations were attempted and rejected.  Artifact 9670194395 has
ZIP digest
`sha256:040b47a263a030b41d0648e42e86ba027ae6da214b20ec6509f6b3d41e90802a`.
This cross-checks only the bounded conversion SELFTEST.  No positive task192
production receipt has yet been adapted.

### 5.3 Task198 roof and occurrence interface

The 6,441 relator reconstruction, task172 roster, task176 artifact identity,
v189 ten-to-eleven-to-seven occurrence ledger, and the repaired 43-member
dependency cone passed static audit.  The 2026-08-28 independent re-audit
nevertheless returned `STOP` before execution.  Three production boundaries
remain open: a resource checkpoint does not yet emit the portable staged
resume manifest required by the next run; the seven SELFTEST context maps do
not yet factor the same nonsplit Dic3 presentation; and the complete 6,441-row
predecessor reconstruction occurs before the `presentation_rows` cap is
charged.  The phase/cap mutations must also reach the semantic resource
validator rather than fail first at duplicate-envelope equality.  A second
repair is in progress.  No task198 GHA result is accepted.

### 5.4 Task191 supporting boundary lane

The separate run

~~~text
run  33109346940
head d68580936b2981b7de41dea4cb3f199e742fde62
~~~

was still in the GAP computation step at 2026-08-28 08:54 JST.  It computes
first-roof boundary membership for the exactification directions \(u_0,v_0\).
It is not the \(g_{760}\) \(j=9\)--12 resume, not \(\mu_1\), and not the
three-block endpoint.

## 6. Dependency-safe current production order

1. in parallel, finish task192 PRODUCTION and authenticate its terminal;
2. in parallel, accept task198 only after its production-shared partial resume,
   resource, dependency, context-map, and nontrivial-cocycle controls pass
   independent audit and GHA SELFTEST;
3. after both dependencies are ready, use the exact correction and occurrence
   endpoints to run the complete 486-input-direction pre-gate (4.4), before
   task193/v188;
4. on a pre-gate pass, run task197, then task193, then v188's actual
   successor/joint-span construction;
5. replace the old pointed-only solve by the joint span (4.5);
6. compile the returned \(\mu_1\) to \(M_0\) by v191 and run the exact
   three-block PB endpoint;
7. on exact endpoint zero, extract and replay \(q_{H1},q_{H2},q_P\) by
   v197; on nonzero, retain \(\mu_1\) and use only exact or strictly finer
   quotient screens;
8. apply v174 to the relative pro-3 lane after its literal and nonlinear
   hypotheses; and
9. discharge prime-to-three, formation, and perfect-core gates before any
   fake or Ihara declaration.

## 7. No-backtracking rules added by v214

1. Do not resume the old uncheckpointed \(j=9\)--12 lane ahead of the
   complete 486-direction pre-gate.
2. Do not choose one arbitrary \(\mu_1\) and then spend 729 columns varying
   its source representatives.  Exponent nine is constant on that fibre.
3. Run the pre-gate before building the first successor whenever its fixed
   endpoint inputs are available.
4. After the successor exists, solve the pointed and exponent-nine
   conditions simultaneously.
5. A quotient membership is only a seed; exact PB zero still requires
   v198.
6. At \(m>0\), solve for the affine increment
   \(\kappa\in I_m\), not for the whole upper multiplier inside \(I_m\).
7. A pass at one rung does not imply a pass at the next.
8. Do not call the pro-Heisenberg quotient a full return-even homotopy.

## 8. Current frontier

~~~text
NAMED NONARITHMETIC ROW 36 / g760:                  ORIENTATION-INDEPENDENT / FROZEN
FULL 648-ROW COMPLEMENT:                            ORIENTATION-DEPENDENT
OLD g760 j=9--12 RUN:                               UNKNOWN_RESOURCE AT j=9
ALL-RUNG PRO-HEISENBERG QUOTIENT:                   PAPER_PROOF
FIRST-EDGE COMPLETE ENDPOINT PRE-GATE:              486 ALGEBRA INPUTS / IMAGE RANK <=486
ALL POINTED mu1 + EXP9 ENDPOINT:                    ONE JOINT SPAN / PAPER_PROOF
TASK191 U0/V0 PRODUCTION:                           GHA IN PROGRESS
TASK192 SELFTEST:                                   CROSS-CHECKED / 33129356703
TASK192 EXACT COMMON WORD PRODUCTION:               GHA 33129456772 DISPATCHED / NO TERMINAL AS OF 09:25 JST
TASK197 ADAPTER SELFTEST:                           CROSS-CHECKED / 33130846755
TASK198 COMPLETE ROOF INTERFACE:                    STATIC STOP / SECOND REPAIR IN PROGRESS
ACTUAL 486-DIRECTION PRE-GATE:                      NOT RUN
ACTUAL DELTA1 / K / d1 / e1:                       NOT COMPUTED
ACTUAL mu1 / M0 / EXACT THREE ENDPOINTS / q:        NOT COMPUTED
RELATIVE PRO-3 COMPATIBLE R07 LIFT:                 NOT CONSTRUCTED
PRIME-TO-3 / PERFECT-CORE COFINAL GATES:            OPEN
FAKE / IHARA WITNESS:                               NOT DECLARED
~~~

R07_EXPLICIT_WITNESS_FRONTIER_V215_FIXED
