# R07 pointed-slice / universal-endpoint fusion (v309)

Author: Sol / 2026-08-29

Status: paper theorem and positive-certificate design.  For one fixed literal
A0 word, this note fuses the finite pointed A5 equation with v193's exact
universal endpoint gate.  The coefficient is selected together with a
word-pair lift whose endpoint already vanishes, so a later arbitrary choice
of first-shadow multiplier is unnecessary.  The finite canonical A4 roster
gives a first joint solve; an additional fair lift-kernel dovetail is
positive-complete for all finite-support representative repairs.  The
universal endpoint is deliberately not declared to be a function of v308's
finite state.  No actual solve or witness is asserted.

## 1. Fixed literal data

Let \(k=\mathbf F_3\).  Condition on the following actual positive inputs:

1. one literal A0 correction \(c\in\Omega\), with
   \(f= g_{760}c\), accepted task192 replay and actual task193 rows;
2. one positive pre-A0 A3 ancestry;
3. one accepted A4 word-bearing basis of
   \(K=\ker(\Delta_1\to\Delta_0)\); and
4. the v305 A4-anchored literal pair polynomial
   \(M_0\in k[F]\), whose first-shadow image is \(\kappa_0\in I\) and
   which satisfies

\[
 \Phi(\kappa_0)=\bar\epsilon_1.
\tag{1.1}
\]

Retain v239's signs

\[
 d_1=-\mathscr D_1(g_{760}),
 \qquad
 e_1(c)=-\mathscr D_1(f),
\tag{1.2}
\]

in the full block-tagged first Fox cokernel, and put

\[
 r_0(c)=e_1(c)-\kappa_0d_1.
\tag{1.3}
\]

Let \(\widetilde d\) and \(\widetilde e_c\) be the corresponding literal,
occurrence-resolved universal Fox rows over the fixed presented PB3/PB4
context groups.  Their reductions give \(d_1,e_1(c)\), but they are not
replaced by those finite rows.

## 2. A finite canonical word-pair roster for the first-shadow ideal

Let

\[
 K=\langle k_1,\ldots,k_t\rangle_k,
 \qquad
 k_i=\rho_1(u_i),
 \qquad
 \rho_0(u_i)=1
\tag{2.1}
\]

be the accepted A4 basis with literal words.  Fix one literal source section
\(s:\Delta_1\to F\) on the finite marked group.  For
\(v\in\Delta_1\) and \(1\leq i\leq t\), define

\[
 P_{v,i}=s(v)u_i-s(v)\in k[F],
 \qquad
 \theta_{v,i}=v(k_i-1)\in I.
\tag{2.2}
\]

Every \(P_{v,i}\) is a literal roof-fibre pair, and its first-shadow image is
\(\theta_{v,i}\).  Since

\[
 I=k[\Delta_1]\langle k_i-1:1\leq i\leq t\rangle,
\tag{2.3}
\]

the finite roster (2.2) spans \(I\) as a \(k\)-vector space.  The roster may
be generated lazily under the exact marked \(x^{\pm1},y^{\pm1}\) actions,
but a positive certificate retains every selected literal pair.

Enumerate the roster as \((P_j,\theta_j)_{1\leq j\leq m}\).  Define three
separately typed columns

\[
 p_j=\theta_jd_1,
 \qquad
 a_j=\Phi(\theta_j),
 \qquad
 u_j=\widetilde D_1(P_j\widetilde d).
\tag{2.4}
\]

The third coordinate lies in the sevenfold direct sum of fixed presented
context group algebras.  It is computed by literal left action and exact PB
normal forms, not by reducing \(P_j\) to \(\Delta_1\).

Finally put

\[
 \eta_0(c)=
 \widetilde D_1(\widetilde e_c-M_0\widetilde d).
\tag{2.5}
\]

This is a finite-support universal endpoint.  It depends on the exact word
\(c\) and exact pair representatives in \(M_0\).

## 3. One augmented membership chooses the promotable multiplier

For \(z=(z_1,\ldots,z_m)\in k^m\), set

\[
 \theta(z)=\sum_jz_j\theta_j,
 \qquad
 M(z)=M_0+\sum_jz_jP_j,
 \qquad
 \mu_1(z)=\kappa_0+\theta(z).
\tag{3.1}
\]

### Theorem 3.1 (FINITE CANONICAL A5/A7 FUSION)

For the fixed literal data above, the following are equivalent:

1. the coefficient vector \(z\) makes \(\mu_1(z)\) satisfy the pointed and
   endpoint equations and makes its canonical word-pair lift \(M(z)\) pass
   the universal endpoint gate; and
2. one exact joint linear identity holds:

\[
 \boxed{
 \sum_{j=1}^m z_j\,(p_j,a_j,u_j)
   =\bigl(r_0(c),0,\eta_0(c)\bigr).}
\tag{3.2}
\]

On a positive solution,

\[
 \boxed{
 \mu_1(z)d_1=e_1(c),
 \qquad
 \Phi(\mu_1(z))=\bar\epsilon_1,
 \qquad
 \widetilde D_1(\widetilde e_c-M(z)\widetilde d)=0.}
\tag{3.3}
\]

Moreover \(M(z)\) is a finite roof-fibre word-pair polynomial whose image in
\(k[\Delta_1]\) is exactly \(\mu_1(z)\).

#### Proof

The first coordinate of (3.2) gives

\[
 \theta(z)d_1=r_0(c)=e_1(c)-\kappa_0d_1,
\]

which is the first equality in (3.3).  The second coordinate and (1.1) give

\[
 \Phi(\mu_1(z))=Phi(\kappa_0)+\sum_jz_j\Phi(\theta_j)
 =\bar\epsilon_1.
\]

For the universal endpoint, equivariance and linearity give

\[
\begin{aligned}
 \widetilde D_1(\widetilde e_c-M(z)\widetilde d)
 &=\eta_0(c)-\sum_jz_j
   \widetilde D_1(P_j\widetilde d)\\
 &=\eta_0(c)-\sum_jz_ju_j,
\end{aligned}
\tag{3.4}
\]

so the third coordinate of (3.2) is exactly its vanishing.  Conversely the
three equations (3.3) reverse these calculations and give (3.2).  Equations
(1.1), (2.2) and (3.1) prove the first-shadow and roof-fibre claims.
\(\square\)

The theorem is linear only because the literal A0 word \(c\), the task193
rows, the A4 roster and every universal representative have already been
fixed.  It does not revive v306's false assertion that the task193 row is
linear while \(c\) varies.

## 4. Endpoint zero promotes the same coefficient to every pro-3 rung

### Corollary 4.1 (ONE POSITIVE JOINT SOLVE REACHES THE PRO-3 PROMOTION GATE)

If (3.2) has a solution, v193 supplies a finite universal boundary chain
\(q\) with

\[
 \widetilde e_c-M(z)\widetilde d=\widetilde D_2q.
\tag{4.1}
\]

Consequently v191 gives, at every matched relative pro-3 rung,

\[
 e_n=\mu_nd_n,
\tag{4.2}
\]

where \(\mu\) is the image of the same literal polynomial \(M(z)\) in the
completed relative ideal.  Under v174's registered word-bearing and
nonlinear side gates, the compatible correction is

\[
 \boxed{
 c_\infty=-\sum_{r\geq0}\mu^ra.}
\tag{4.3}
\]

At each finite quotient the sum is finite.

#### Proof

The third equality in (3.3) and v193 Theorem 3.1 give (4.1).  The word-pair
typing proved in Theorem 3.1 is exactly the remaining hypothesis of v191
Theorem 2.1, which gives (4.2).  V174 then gives (4.3).  \(\square\)

Thus, on this branch, A5 coefficient selection, A6 pair compilation and A7
universal endpoint existence are not three arbitrary choices.  They are one
augmented coefficient solve followed by constructive relator decomposition.
This closes only the relative pro-3 promotion component; formation,
prime-to-three, perfect-core and nonlinear gates remain separate.

## 5. Why the finite canonical roster is not a negative universe

The first-shadow map forgets source representatives.  Let \(\Gamma\) be the
fixed common source image of v191 and put

\[
 J_0=\ker(k[\Gamma]\to k[\Delta_0]),
 \qquad
 \mathcal L_1=\ker(J_0\to I).
\tag{5.1}
\]

If \(M\) and \(M'\) have the same first-shadow value, then

\[
 M'-M\in\mathcal L_1.
\tag{5.2}
\]

An element of \(\mathcal L_1\) may have nonzero universal endpoint action,
even though both its pointed and endpoint-projection coordinates vanish.
Therefore failure of (3.2) for the finite canonical roster excludes those
chosen representatives only.  It does not exclude all lifts of a
first-shadow multiplier.

This also explains the precise limitation of v308.  Two literal A0 words
can have the same roof Fox state and the same complete finite next-rung
affine state while having different images in the fixed infinite presented
PB context groups.  Hence \(\eta_0(c)\) is not a function of the v308 state.
A search may merge such words for the fixed-rung A0/A5 decision, but not for
the universal endpoint unless it retains one literal ancestry per endpoint
normal form.

## 6. Positive-complete representative repair

The limitation in Section 5 does not require a second blind multiplier
search.  Keep the first-shadow variables \(z_j\), and enumerate literal
finite-support generators \(L_s\in\mathcal L_1\).  Each supplies only a
universal coordinate

\[
 \ell_s=widetilde D_1(L_s\widetilde d),
 \qquad
 (0,0,\ell_s).
\tag{6.1}
\]

For example, the kernel of the finite map \(\Gamma\to\Delta_1\) is normally
generated by a recursively enumerable word-bearing roster, and

\[
 V(n-1)=Vn-V
\tag{6.2}
\]

gives a roof-fibre pair in \(\mathcal L_1\) for every source word \(V\) and
kernel word \(n\).  Products and sums of these pairs enumerate every
finite-support element needed in (5.2).

### Theorem 6.1 (POSITIVE-COMPLETE PROMOTABLE-REPRESENTATIVE DOVETAIL)

Suppose there exists a finite-support roof-fibre polynomial \(M\) whose
first-shadow image solves the fixed pointed A5 equations and whose universal
endpoint is zero.  Then a fair joint column generation using

\[
 (p_j,a_j,u_j)
 \quad\text{and}\quad
 (0,0,\ell_s)
\tag{6.3}
\]

eventually finds a finite equality with target
\((r_0(c),0,\eta_0(c))\), and hence constructs such an \(M\).

#### Proof

By (2.3), choose coefficients \(z_j\) whose canonical polynomial has the
same first-shadow image as \(M\).  Their difference lies in
\(\mathcal L_1\) by (5.2) and has finite support.  The standard group-algebra
kernel description writes that difference as a finite sum of translated
kernel differences of the form (6.2).  Hence only finitely many enumerated
columns in (6.3) occur in the desired equality.  A fair enumeration reaches
all of them, after which exact sparse elimination finds the target.
\(\square\)

This is a positive termination theorem.  The universal group algebras are
infinite, so a bounded no-hit is `UNKNOWN_RESOURCE`; it is not a complete
negative.  A positive receipt remains finite and independently replayable.

## 7. Integration with the v308 outer selector

The witness-oriented order is now:

1. let the current A0 solver return a literal word, or let v308 enumerate a
   new finite fixed-rung state with retained literal ancestry;
2. reconstruct task193 and the exact universal row \(\widetilde e_c\) for
   that same word;
3. run the finite canonical membership (3.2);
4. if necessary, dovetail only the lift-null columns (6.1), without changing
   the already solved first-shadow equations;
5. on success extract \(q\), replay (4.1), and apply v191/v174.

If two A0 ancestries have equal v308 state but different universal endpoint
normal forms, both may have to be tried.  A fair outer dovetail over literal
ancestries and the inner lift-null columns is positive-complete for a finite
certificate, but is no longer a finite negative decision.  This is the exact
price of asking for all-rung promotion rather than one finite-rung A5 pass.

## 8. Certificate boundary

A positive checker must independently reconstruct:

1. the exact A0 word, task193 \(d_1,e_1(c)\), A3/A4 identities and \(M_0\);
2. every selected canonical pair and lift-null pair, including both roof and
   first-shadow values;
3. all three column coordinates in (2.4) and (6.1);
4. the coefficient equality (3.2), with no loss of dependent source
   representatives;
5. the literal \(M\), its image \(\mu_1\), both finite pointed equations and
   every universal endpoint normal form;
6. the relator-decomposition chain \(q\) and direct equality (4.1); and
7. destructive failures after changing one A0 letter, A4 kernel word,
   source section, dependent representative, coefficient, block tag,
   pentagon order, endpoint word or relator factor.

The producer may use lazy sparse columns.  A positive checker needs the
retained finite subset only; a claimed negative over the infinite lift
kernel is forbidden.

## 9. Fixed frontier

```text
FIXED-WORD A5 + UNIVERSAL ENDPOINT JOINT MEMBERSHIP: PAPER PROOF
POSITIVE JOINT SOLVE -> MU1 + LITERAL M + q:         PAPER PROOF
SAME M PROMOTES THROUGH ALL RELATIVE PRO-3 RUNGS:   PAPER PROOF / SIDE GATES
FINITE CANONICAL A4 LIFT ROSTER:                     PAPER CONSTRUCTION
ALL FINITE REPRESENTATIVE REPAIRS:                   POSITIVE-COMPLETE DOVETAIL
COMPLETE NEGATIVE OVER UNIVERSAL LIFT KERNEL:         NOT CLAIMED
ACTUAL A0 WORD / TASK193 ROWS / A3 / A4:              NOT COMPUTED
ACTUAL AUGMENTED SOLVE / MU1 / M / q:                 NOT COMPUTED
FORMATION / PRIME-TO-3 / PERFECT-CORE GATES:          OPEN
COMPATIBLE COFINAL LIFT / FAKE / IHARA:               NONE
```

`R07_POINTED_SLICE_UNIVERSAL_ENDPOINT_FUSION_V309_PAPER_GRADE`
