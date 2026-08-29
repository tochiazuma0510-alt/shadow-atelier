# R07 core-comparator Fox norm column (v336)

Author: Sol / 2026-08-29

Status: paper theorem refining v335.  The explicit comparator rung word has
zero **group-value perturbation** in the exponent-nine A3 projection, but
its universal Fox tangent need not be zero.  The tangent is an exact cyclic
norm column with a logarithmic-size straight-line recurrence.  This gives a
finite score-pairing test and an exact invariant-score no-go criterion.
The actual eleven-occurrence column, full correction-domain membership and
field-even pairings have not been computed.  No milestone numerator,
compatible lift, fake certificate or Ihara witness is declared.
`verified=false`.

## 1. Fox derivative of a conjugated power

Let \(F=F(x,y)\), put

\[
 h=[x,y],\qquad \chi=\chi_{07}=[x,y][y,z]^{-1},
\tag{1.1}
\]

and for \(m\ge1\) put

\[
 c(m)=\chi^{-1}h^m\chi.
\tag{1.2}
\]

For \(a\) in a group ring define the geometric norm

\[
 N_m(a)=1+a+\cdots+a^{m-1}.
\tag{1.3}
\]

Use the standard left Fox derivatives
\(\partial_x,\partial_y:\mathbf ZF\to\mathbf ZF\), with

\[
 \partial_t(uv)=\partial_tu+u\partial_tv,\qquad
 \partial_t(u^{-1})=-u^{-1}\partial_tu.
\tag{1.4}
\]

### Theorem 1.1 (COMPARATOR FOX NORM FORMULA)

For \(t\in\{x,y\}\),

\[
 \boxed{
 \partial_t c(m)
 =
 \chi^{-1}
 \left(
 N_m(h)\,\partial_t h
 +(h^m-1)\,\partial_t\chi
 \right).}
\tag{1.5}
\]

#### Proof

The power rule gives

\[
 \partial_t(h^m)=N_m(h)\partial_t h.
\tag{1.6}
\]

Apply (1.4) to \(\chi^{-1}h^m\chi\):

\[
\begin{aligned}
 \partial_t c(m)
 &=-\chi^{-1}\partial_t\chi
   +\chi^{-1}N_m(h)\partial_t h
   +\chi^{-1}h^m\partial_t\chi\\
 &=\chi^{-1}
   \left(
   N_m(h)\partial_t h+(h^m-1)\partial_t\chi
   \right).
\end{aligned}
\]

\(\square\)

Let \(\rho:F\to G\) and extend it to group rings over a field \(k\).  If
\(\rho(h)^m=1\), then \(c(m)\) has trivial group value, while (1.5) reduces
to

\[
 \boxed{
 \rho(\partial_t c(m))
 =
 \rho(\chi)^{-1}
 N_m(\rho(h))\,\rho(\partial_t h).}
\tag{1.7}
\]

The right side need not vanish.  Thus

\[
 \rho(c(m))=1
 \quad\not\Longrightarrow\quad
 \rho(\partial c(m))=0.
\tag{1.8}
\]

This distinction is load-bearing for any attempt to turn v335's explicit
group words into relation-module columns.

## 2. The all-rung comparator and its depth recurrence

Retain v335's words

\[
 c_j=c(m_j),\qquad
 m_j=18\cdot3^j.
\tag{2.1}
\]

They satisfy \(c_{j+1}=c_j^3\).  Applying the power rule directly gives

\[
 \boxed{
 \partial_t c_{j+1}
 =(1+c_j+c_j^2)\,\partial_t c_j.}
\tag{2.2}
\]

At the old rung \(G_j\), v335 gives \(\rho_j(c_j)=1\).  In characteristic
three, (2.2) therefore implies

\[
 \boxed{\rho_j(\partial_t c_{j+1})=0.}
\tag{2.3}
\]

The next comparator is tangent-invisible one rung below, exactly as a
depth-raised correction should be.  In contrast,
\(\rho_j(\partial_t c_j)\) is the norm expression (1.7) and can be
nonzero.

At \(G_{j+1}\), the element \(\rho_{j+1}(c_j)\) has order three, so the
factor

\[
 1+\rho_{j+1}(c_j)+\rho_{j+1}(c_j)^2
\tag{2.4}
\]

is the \(C_3\)-norm.  It can be nonzero in characteristic three and lands
in the invariant/socle direction of the corresponding cyclic module.

## 3. Straight-line evaluation without expanding the word

The norm has exact recurrences

\[
\begin{aligned}
 N_{a+b}(h)&=N_a(h)+h^aN_b(h),\\
 N_{2a}(h)&=(1+h^a)N_a(h),\\
 N_{3a}(h)&=(1+h^a+h^{2a})N_a(h).
\end{aligned}
\tag{3.1}
\]

Together with repeated squaring for \(h^a\), these give a straight-line DAG
of \(O(\log m)\) group-ring additions and multiplications representing
\(N_m(h)\).  This is a bound on the symbolic computation graph, not on the
expanded support of the resulting group-ring element.

For the special sequence \(m_j=18\cdot3^j\),

\[
 N_{m_{j+1}}(h)
 =
 (1+h^{m_j}+h^{2m_j})N_{m_j}(h).
\tag{3.2}
\]

Hence one base norm \(N_{18}(h)\), the powers \(h^{m_j}\), and the recurrence
(3.2) suffice to generate every rung.  A producer need not materialize the
literal word \(c_j\), whose exponent grows as \(3^j\), merely to obtain its
Fox column.

## 4. Occurrence-wise literal A.18 column

For a frozen H1, H2 or P occurrence \(o\), let

\[
 \sigma_o:F(x,y)\longrightarrow F_o
\tag{4.1}
\]

be its literal substitution, and put

\[
 h_o=\sigma_o(h),\qquad \chi_o=\sigma_o(\chi).
\tag{4.2}
\]

Applying Theorem 1.1 in \(F_o\) gives, for every target generator \(T\),

\[
 \boxed{
 \partial_T\sigma_o(c_j)
 =
 \chi_o^{-1}
 \left(
 N_{m_j}(h_o)\,\partial_T h_o
 +(h_o^{m_j}-1)\,\partial_T\chi_o
 \right).}
\tag{4.3}
\]

Whenever the authenticated old occurrence quotient kills \(h_o^{m_j}\),
this simplifies to

\[
 \boxed{
 \partial_T\sigma_o(c_j)
 =
 \chi_o^{-1}N_{m_j}(h_o)\partial_T h_o.}
\tag{4.4}
\]

The existing literal H1/H2/P Jacobian is a fixed prefix-weighted signed
combination of the eleven occurrence derivatives.  Substituting (4.3), with
the frozen inverse slots and printed factor order, therefore gives a
closed-form candidate column \(b_j\) in that Jacobian.  No new relation
presentation is needed.  What remains is to authenticate that this
candidate belongs to the full legal common-word domain.

Equation (4.4) must not be obtained by silently deleting the second term:
the equality \(h_o^{m_j}=1\) has to be checked in every actual occurrence
owner.

## 5. Exact score-pairing and invariant-score no-go test

Let \(V\) be one occurrence module, let \(g\) be the action of \(h_o\), and
let \(\lambda\in V^*\).  For \(v\in V\),

\[
 \lambda(N_m(g)v)=\sum_{i=0}^{m-1}\lambda(g^iv).
\tag{5.1}
\]

### Lemma 5.1 (INVARIANT DUALS KILL THE NORM COLUMN)

Assume \(\operatorname{char}k=3\), \(3\mid m\), and

\[
 \lambda\circ g=\lambda.
\tag{5.2}
\]

Then

\[
 \boxed{\lambda(N_m(g)v)=0\quad\text{for every }v\in V.}
\tag{5.3}
\]

#### Proof

Every summand in (5.1) equals \(\lambda(v)\), so the sum is
\(m\lambda(v)=0\) in \(k\).  \(\square\)

For a complete local-score identity \(\phi\), pull \(\phi\) back through
the frozen prefix, sign and occurrence maps to functionals \(\phi_o\).
If every \(\phi_o\) relevant to (4.4) is \(h_o\)-invariant, Lemma 5.1 gives

\[
 \boxed{\phi(b_j)=0.}
\tag{5.4}
\]

Thus v335's pure-dihedral comparator roster cannot separate such a score,
regardless of \(j\).  Conversely, a nonzero pairing with one complete score
is an exact certificate that the corresponding norm column supplies a new
direction against that score.

This is the promised finite test for the field-even survivor:

1. reconstruct the complete score basis;
2. pull each score to the eleven occurrence modules;
3. test invariance under the corresponding \(h_o\);
4. evaluate only the non-forced norm pairings; and
5. require literal column ancestry and full-domain legality.

The label “return-even” alone does not imply (5.2); the actual actions must
be evaluated.  Therefore (5.4) is a no-go criterion, not a declaration that
the present field-even class survives.

## 6. Qualification of the v335 A3 statement

V335 Section 4 proves

\[
 q(c_j)=1
\tag{6.1}
\]

in every exponent-nine occurrence quotient.  Hence replacing one word by
that comparator does not change the group-valued v216/v302 H1, H2 and P
target.  This is exactly the **zero projected value perturbation** consumed
by the current pre-A0 A3 ABI.

Equations (1.7) and (4.4) show that (6.1) does not prove the vanishing of a
universal relation-module Fox column.  Such a column is not part of the
current v303-only A3 input and may first become relevant at the actual
successor-kernel/field-even stage.

Accordingly the precise reading is:

- the comparator cannot change or repair the pending v216 projected target
  merely by replacing its finite occurrence values;
- it can still be tested as a later word-bearing tangent column after full
  A4 typing; and
- the score test is the norm pairing of Section 5, not the Boolean
  \(q(c_j)=1\).

## 7. Consequence for the explicit-lift programme

V335 supplied a closed all-rung word roster.  The present theorem supplies
its closed all-rung Fox roster and a sharp annihilation test.  The remaining
actual work is now finite and typed:

1. prove \(c_j\) lies in the full actual correction domain;
2. instantiate (4.3) with the authenticated eleven occurrences;
3. reconstruct the complete even score basis;
4. evaluate its norm-pairing matrix; and
5. apply v333's target-specific or structural rank criterion.

If the matrix spans the actual even cokernel class and descends naturally,
v332--v334 promote it to the nonlinear construction.  If every missing
score is forced invariant by Lemma 5.1, this entire pure-dihedral roster is
insufficient and a genuinely field-outer column is necessary.

```text
GROUP-VALUE INVISIBILITY => FOX ZERO:        NO
EXACT FOX COLUMN:                           chi^-1 N_m(h) dh
ALL-RUNG DERIVATIVE RECURRENCE:              d c_(j+1)=(1+c_j+c_j^2)d c_j
SYMBOLIC NORM DAG:                          O(log m_j)
INVARIANT DUAL SCORE PAIRING:               ZERO IN CHARACTERISTIC 3
ACTUAL ELEVEN-OCCURRENCE COLUMN:             NOT COMPUTED
FULL-DOMAIN LEGALITY / EVEN PAIRING MATRIX: NOT PROVED / NOT COMPUTED
COMPATIBLE FULL LIFT / FAKE / IHARA:         NOT CONSTRUCTED
```

`R07_CORE_COMPARATOR_FOX_NORM_COLUMN_V336_PAPER_GRADE`

