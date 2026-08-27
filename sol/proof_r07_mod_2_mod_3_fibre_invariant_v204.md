# R07 mod-2/mod-3 endpoint fibre invariant v204

Author: Sol / 2026-08-28

Status: paper theorem combining the frozen roof exponent lattice v156 with
the finite endpoint screens v200--v203.  Every same-first-successor repair
direction vanishes in both the mod-2 and mod-3 abelian PB endpoint screens.
Thus these screens require no repair columns: the projected endpoint is an
invariant of the whole affine fibre of the named \(\mu_1\).  A nonzero value
is an exact no-repair certificate for that fibre; two zero values remain
inconclusive for exact PB equality.  The actual \(M_0\) is not yet compiled,
so no numerical endpoint result, lift, fake certificate, or Ihara witness is
declared.

## 1. Roof and successor kernels

Let

\[
 F=F(x,y)\twoheadrightarrow\Delta_1
 \twoheadrightarrow\Delta_0
\tag{1.1}
\]

be the frozen first diagonal successor and the ten-occurrence/seven-block
roof of v188--v190.  Put

\[
 H_1=\ker(F\to\Delta_1),
 \qquad
 H_0=\ker(F\to\Delta_0).
\tag{1.2}
\]

The factorization (1.1) gives

\[
 H_1\le H_0.
\tag{1.3}
\]

Through the marked isomorphism of v189, \(H_0\) is the registered joint
kernel \(\Omega\) of v156.  V156 Theorem 3.1 proves the exact integer
exponent lattice

\[
 \boxed{
 \operatorname{exp}_{x,y}(H_0)=18\mathbf Z\oplus18\mathbf Z.}
\tag{1.4}
\]

This uses the complete authenticated 6,441-word roof presentation; it is not
an inference from a bounded word sample.

### Lemma 1.1 (SUCCESSOR DIRECTIONS HAVE ZERO MOD-2/MOD-3 EXPONENT)

For \(\ell=2\) and \(\ell=3\),

\[
 \boxed{
 \operatorname{exp}_{x,y}(H_1)\bmod\ell=0.}
\tag{1.5}
\]

#### Proof

By (1.3), the exponent vector of every \(h\in H_1\) belongs to the lattice
in (1.4).  Both 2 and 3 divide 18, so its reduction modulo either prime is
zero. \(\square\)

No presentation of \(\Delta_1\) is needed for (1.5).  Only the marked
successor-to-roof factorization and the already fixed roof lattice are used.

## 2. The projected direction ideal is zero

Let

\[
 \alpha_\ell:F\twoheadrightarrow
 D_\ell\cong(C_\ell)^2
\tag{2.1}
\]

be v202's exact joint mod-\(\ell\) occurrence map.  V202 identifies
\(\alpha_\ell(w)\) with the source exponent vector of \(w\) modulo
\(\ell\), because the H1/1 \(f(x,y)\) occurrence retains the two independent
classes \(A_{12},A_{23}\).

Put

\[
 J_1=\ker\bigl(
 \mathbf F_3[F]\longrightarrow\mathbf F_3[\Delta_1]
 \bigr).
\tag{2.2}
\]

### Theorem 2.1 (ZERO PROJECTED REPAIR DIRECTION)

For \(\ell=2,3\),

\[
 \boxed{(\alpha_\ell)_*(J_1)=0.}
\tag{2.3}
\]

Consequently,

\[
 \boxed{
 \bar{\mathcal E}_{d,\ell}(J_1)=0,}
\tag{2.4}
\]

where \(\bar{\mathcal E}_{d,\ell}\) is the complete three-block endpoint
change after PB abelianization modulo \(\ell\).

#### Proof

V195 generates \(J_1\) as the two-sided ideal spanned by

\[
 A(h-1)B,
 \qquad A,B\in F,
 \quad h\in H_1.
\tag{2.5}
\]

Lemma 1.1 and v202 give \(\alpha_\ell(h)=1\).  Hence

\[
 (\alpha_\ell)_*\bigl(A(h-1)B\bigr)
 =\alpha_\ell(A)(1-1)\alpha_\ell(B)=0.
\tag{2.6}
\]

Linearity proves (2.3).  V203 factorization (1.3) then proves (2.4).
\(\square\)

In v203 notation this says

\[
 R_2=R_3=0,
 \qquad r_2=r_3=0.
\tag{2.7}
\]

Thus v203's caps of 8 and 18 essential repair columns specialize to exactly
zero columns on the actual R07 successor lane.

## 3. Fibre invariant and exact obstruction

Let \(M_0\) be any finite word-bearing representative of the named first
multiplier \(\mu_1\).  Every other finite-support representative is
\(M_0+N\), \(N\in J_1\), by v195.  Let

\[
 \bar\eta_\ell(M)=
 \tau_{*,\ell}\eta(M)\in E_\ell
\tag{3.1}
\]

be the mod-\(\ell\) abelian projection of v194's three combined endpoint.

### Corollary 3.1 (MOD-2/MOD-3 ENDPOINT IS CONSTANT ON THE FIBRE)

For \(\ell=2,3\) and every \(N\in J_1\),

\[
 \boxed{
 \bar\eta_\ell(M_0+N)=\bar\eta_\ell(M_0).}
\tag{3.2}
\]

#### Proof

V195 gives

\[
 \eta(M_0+N)=\eta(M_0)-\mathcal E_d(N).
\tag{3.3}
\]

Project (3.3) and apply (2.4). \(\square\)

### Corollary 3.2 (ZERO-COLUMN SAME-MULTIPLIER OBSTRUCTION)

If

\[
 \boxed{
 \bar\eta_2(M_0)\ne0
 \quad\text{or}\quad
 \bar\eta_3(M_0)\ne0,}
\tag{3.4}
\]

then no finite-support representative of \(\mu_1\) has zero exact
H1/H2/P endpoint.

#### Proof

An exact zero endpoint would project to zero in both finite quotients, while
Corollary 3.1 says that its projections must equal those in (3.4).  This is
also v200 Theorem 5.1 with a zero projected repair subspace. \(\square\)

The nonzero coordinate itself supplies a dual certificate: choose its tagged
group-algebra basis coefficient.  No orbit enumeration or Gaussian repair
solve is required.

The converse remains false.  If

\[
 \bar\eta_2(M_0)=\bar\eta_3(M_0)=0,
\tag{3.5}
\]

distinct exact PB words may have cancelled after abelianization.  One must
run v198's exact Artin/Garside endpoint test and, if it is nonzero, v196's
exact positive repair lane or a finer sound quotient obstruction.

## 4. Production consequence

After v188/v191 compile \(M_0\), use this order:

1. compute the exact endpoint-only term roster of v198 once;
2. exponent-sum those same PB terms modulo two and modulo three, retaining
   the H1/H2/P tags;
3. if either collected projected endpoint is nonzero, emit its first tagged
   nonzero bucket and stop the same-\(\mu_1\) repair lane by Corollary 3.2;
4. if both vanish and the exact PB endpoint also vanishes, proceed directly
   to v197; and
5. if both vanish but the exact PB endpoint is nonzero, invoke only a finer
   quotient or the exact positive repair dovetail.

There is no successor-relator scan, joint-orbit BFS, repair-column build, or
linear solve in Steps 2--3.  The two screens are reductions of the already
materialized exact endpoint terms and can be evaluated in the same pass.

The certificate binds v156's roof-lattice theorem and 6,441-roster pins,
the marked factorization \(\Delta_1\to\Delta_0\), the H1/1 standard
occurrence, every exact endpoint term, its mod-2 and mod-3 exponent bucket,
and the first nonzero tagged coefficient.  The checker rejects a mutation of
18 to a number not divisible by both primes, reversal of the kernel
inclusion, use of a roof element not lying in \(H_1\), omission of a literal
occurrence, or merging of the H1/H2 and E3/E4 typed summands.

This obstruction concerns one named \(\mu_1\)-fibre.  It does not rule out a
different first-successor multiplier, does not itself prove a B4 component
fibre empty, and does not discharge prime-to-three or perfect-core gates.

~~~text
FIRST-SUCCESSOR KERNEL H1 <= ROOF KERNEL H0:       PAPER_PROOF
ROOF EXPONENT LATTICE exp(H0) = 18 Z^2:            FROZEN v156
R2 = R3 = 0 FOR EVERY SUCCESSOR DIRECTION:         PAPER_PROOF
MOD-2/MOD-3 ENDPOINT CONSTANT ON mu1 FIBRE:         PAPER_PROOF
NONZERO MOD-2 OR MOD-3 ENDPOINT -> EXACT FIBRE NO: PAPER_PROOF
ACTUAL M0 / PROJECTED ENDPOINTS:                    NOT COMPUTED
EXACT SAME-mu1 REPAIR / RELATIVE PRO-3 LIFT:        NOT CONSTRUCTED
FAKE / IHARA WITNESS:                               NOT DECLARED
~~~

R07_MOD_2_MOD_3_ENDPOINT_FIBRE_INVARIANT_V204_PAPER_GRADE
