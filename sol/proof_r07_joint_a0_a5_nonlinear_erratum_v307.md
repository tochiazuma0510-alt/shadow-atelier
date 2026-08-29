# R07 joint A0/A5 nonlinear-state erratum (v307)

## 0. Erratum and surviving statement

V306 claimed that the task193 direct change of an arbitrary A0 coefficient
factors through its first-successor value and is linear there.  That claim is
not established and is false at the stated level of generality.  It
misapplies the rung-indexed affine map of v168: that map linearizes
corrections which are invisible at the **current** rung around one fixed
current word.  It does not linearize the next-rung Fox defect while the
coarser A0 base word itself ranges over all solutions.

Accordingly v306 Lemma 1.1, equations (1.6)--(1.7) as a factorization through
one linear map on \(K\), Theorem 3.1, and the positive-only linear joint
column-generation conclusion are superseded by this note.

The pointwise A5 slice criterion survives: after a literal A0 word is fixed,
its independently reconstructed task193 row can be tested against the fixed
slice \(Hd_1\).  A joint preselection is still a finite-state problem, but it
is a nonlinear accepted-set search, not one vector-space membership.

No actual A0 word, A3/A4 terminal, pointed multiplier, compatible lift, fake
certificate, or Ihara witness is asserted here.

## 1. Where the linearity argument fails

Let \(E_0\) be the roof window and

\[
 E_1=P/\Phi_3(K_0),
 \qquad K_0=\ker(P\to E_0).
\tag{1.1}
\]

V140's A0 defect map is additive on the registered roof correction domain:

\[
 B_0(a b)=B_0(a)+B_0(b).
\tag{1.2}
\]

This holds because every correction factor is invisible in the contexts at
the level where the A0 Fox product rule is collected.  It is exactly the
linearity used to construct the first common word.

Task193, however, evaluates the relation words of that selected common word
over \(E_1\) and records their next Fox classes.  A source word trivial in
\(E_1\) need not have zero Fox class modulo the complete \(E_1\) boundary:
that class is precisely what detects the next relative Frattini quotient.
Thus

\[
 \rho_1(a)=\rho_1(a')
\tag{1.3}
\]

does not imply equality of the task193 raw rows constructed from the two
literal words.  Source-word ancestry discarded by (1.3) can survive one rung
later.

Likewise, multiplication of two coarse A0 representatives changes the
affine prefixes occurring in every later occurrence.  The crossed Fox rule

\[
 \delta(uv)=\delta(u)+\bar u\,\delta(v)
\tag{1.4}
\]

contains the current prefix \(\bar u\).  When the coarse representative is
varied, this prefix is not a fixed scalar and the resulting next-rung row is
not an ordinary linear function of the coarse coefficient vector.

This is the distinction already protected by v239 Section 2: its
\(B_1a=\mathscr D_1(ga)-\mathscr D_1(g)\) is a definition for one literal
two-word input, not an assertion that the nonlinear relation constructor is
a homomorphism in \(a\).

V168 equation (4.3) does provide a linear map

\[
 B_n[c]=\beta_n(f^{(n)}c)-\beta_n(f^{(n)})
\tag{1.5}
\]

when \(f^{(n)}\) is fixed and \(c\) belongs to the correction domain
invisible at rung \(n\).  V306 applied (1.5) while varying the preceding
coarse base itself.  That shifts the index and is invalid.

## 2. The valid pointwise A5 criterion

Assume only conditionally that positive A3/A4 data have produced the
A4-anchored endpoint base point \(\kappa_0\) of v305 and the complete fixed
slice

\[
 H=\ker\Phi,
 \qquad S=Hd_1.
\tag{2.1}
\]

For one literal registered A0 correction word \(c\), put

\[
 f_c=g_{760}c,
 \qquad
 \mathscr B(c)=\mathscr D_1(f_c)-\mathscr D_1(g_{760}),
\tag{2.2}
\]

where both rows are evaluated through the full task193 affine-prefix
arithmetic and complete boundary oracle.  V239 gives

\[
 e_1(c)=d_1-\mathscr B(c).
\tag{2.3}
\]

Define as before

\[
 r_*=(1-\kappa_0)d_1.
\tag{2.4}
\]

### Theorem 2.1 (POINTWISE A0-TO-A5 TEST)

For the fixed literal word \(c\), an endpoint-compatible pointed multiplier
exists if and only if

\[
 \boxed{r_*-\mathscr B(c)\in S.}
\tag{2.5}
\]

If

\[
 r_*-\mathscr B(c)=\theta d_1,
 \qquad \theta\in H,
\tag{2.6}
\]

then

\[
 \boxed{\mu_1=\kappa_0+\theta}
\tag{2.7}
\]

satisfies

\[
 \mu_1d_1=e_1(c),
 \qquad \Phi(\mu_1)=\bar\epsilon_1.
\tag{2.8}

#### Proof

Equations (2.3)--(2.4) give

\[
 e_1(c)-\kappa_0d_1=r_*-\mathscr B(c).
\]

Substitute this identity into v238's exact affine-slice criterion.  Equation
(2.6) then gives (2.7)--(2.8).  QED.

No linearity of \(c\mapsto\mathscr B(c)\) is used.

## 3. Correct joint object: a finite-state accepted set

Let \(\mathcal S_{A0}\) be the registered literal A0 solution set, including
the exact exponent condition.  The simultaneous passing set is

\[
 \boxed{
 \mathcal S_{A0,A5}=
 \{c\in\mathcal S_{A0}:
       r_*-\mathscr B(c)\in S\}.}
\tag{3.1}
\]

This is the correct joint selector target.  It can be represented at a fixed
finite shadow by a finite transition system whose state retains at least:

1. the accumulated A0 defect and exact exponent coordinates;
2. the current values in every typed first-successor occurrence;
3. the complete task193 affine-prefix/Fox state needed by (1.4); and
4. the class of the resulting pointed residual modulo \(S\).

Multiplication by a registered correction generator gives a deterministic
transition on this state.  A complete reachable-state closure would decide
nonemptiness of (3.1); a fair word dovetail is positive-complete but a finite
cutoff remains UNKNOWN.  State merging is legal only after the whole tuple,
including the affine-prefix/Fox component, is exactly equal.  Merging merely
equal \(E_1\) group values recreates the v306 error.

Operationally there are two sound routes.

1. Let the current standalone A0 solver return one word, run task193, and
   apply Theorem 2.1.  If it passes, no joint search is needed.
2. If it fails, explore the homogeneous A0 solution fibre while updating the
   full finite state above.  A positive state returns a new literal A0 word
   and its A5 slice ancestry.  A complete negative requires exhaustion or a
   separately proved invariant obstruction over the full state graph.

The first route is why the active A0 computation remains useful.  The second
route is not the ordinary linear A0 nullspace alone.

## 4. Dependency correction

The correct current A5 dependency cone remains

\[
 \boxed{
 \text{positive pre-A0 A3}
 +\text{accepted A4 word-bearing basis/anchor}
 +\text{one literal A0 word and its task193 rows}.}
\tag{4.1}
\]

V305 still removes actual A2 from the endpoint-base construction.  It does
not remove the literal A0/task193 input from the pointwise slice target.
Task193 may become part of a future nonlinear joint state engine, but no such
engine has been implemented or proved complete for the registered roster.

## 5. Fixed frontier

```text
A0 DEFECT MAP B0 ON ROOF CORRECTIONS:              LINEAR / RETAINED
TASK193 ROW AS LINEAR FUNCTION OF A0 E1 VALUE:      REJECTED
V306 ONE JOINT VECTOR-SPACE MEMBERSHIP:             REJECTED / SUPERSEDED
POINTWISE LITERAL A0 -> A5 SLICE CRITERION:          PAPER PROOF
FULL JOINT A0/A5 OBJECT:                             FINITE-STATE ACCEPTED SET
COMPLETE JOINT STATE CLOSURE / IMPLEMENTATION:       NOT CONSTRUCTED
ACTUAL A0 WORD / TASK193 ROW / MU1 / M:              NOT COMPUTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:              NONE
```

`R07_JOINT_A0_A5_NONLINEAR_STATE_ERRATUM_V307_PAPER_GRADE`
