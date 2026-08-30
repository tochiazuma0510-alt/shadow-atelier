# R07 A0 six-action support-hitting oracle (v404)

Author: Sol / 2026-08-30

Status: paper theorem completing the finite-oracle reduction left open in
v402.  It gives an exact, enumeration-free separation oracle for the six
remaining PB4 action families after the central contraction.  It does not
complete the compact correction-word schedule and therefore reports no A0
terminal, common word, compatible lift, fake, or Ihara witness.
`verified=false`.

## 1. Frozen six-row source

Use v402's new PB4 basis

\[
 (b,c,p,q,r,z),\qquad H=H_0\times\langle\zeta\rangle,
 \qquad H_0=\ker\kappa .
\tag{1.1}
\]

For \(s\in\{b,c\}\) and \(u\in\{p,q,r\}\), put

\[
 \rho_{s,u}=s^{-1}us\,\phi_s(u)^{-1},
\tag{1.2}
\]

where

\[
\begin{array}{lll}
 \phi_b(p)=prpr^{-1}p^{-1},
 &\phi_b(q)=prp^{-1}r^{-1}qrpr^{-1}p^{-1},
 &\phi_b(r)=prp^{-1},\\[1mm]
 \phi_c(p)=p,
 &\phi_c(q)=qrqr^{-1}q^{-1},
 &\phi_c(r)=qrq^{-1}.
\end{array}
\tag{1.3}
\]

Let

\[
 R_{s,u}=\delta\rho_{s,u}\in k[H_0]^5,
 \qquad k=\mathbf F_3,
\tag{1.4}
\]

in coordinate order \((b,c,p,q,r)\).  Every prefix in (1.2) belongs to
\(H_0\), because all five letters have \(\kappa=0\).  The evaluated
relator is the identity, so the Fox boundary identity gives

\[
 d_1R_{s,u}
 =\sum_{i=1}^{5}(R_{s,u})_i(g_i-1)=0.
\tag{1.5}
\]

The six words have unreduced lengths at most

\[
 8,12,6,4,8,6,
\tag{1.6}
\]

in the order \((b,p),(b,q),(b,r),(c,p),(c,q),(c,r)\).  Thus their Fox
rows are fixed small sparse rows; no PB4 group enumeration is hidden in
their construction.

Let

\[
 D_0=\operatorname{span}_k\{L_tR_{s,u}:t\in H_0,
 s\in\{b,c\},u\in\{p,q,r\}\}\le k[H_0]^5.
\tag{1.7}
\]

This is exactly the only live PB4 boundary space after v402's five-family
central quotient.

## 2. Exact support-times-support formula

Write a sparse base row and a sparse dual as

\[
 R_j=\sum_{i,h}a^{(j)}_{i,h}e_i(h),
 \qquad
 \lambda=\sum_{i,g}\lambda_{i,g}e_i(g)^*,
\tag{2.1}
\]

where \(j\) ranges over the six pairs in (1.2).  A left translate has

\[
 L_tR_j=\sum_{i,h}a^{(j)}_{i,h}e_i(th).
\tag{2.2}
\]

Consequently

\[
 \boxed{
 \langle\lambda,L_tR_j\rangle
 =\sum_{i,h}a^{(j)}_{i,h}\lambda_{i,th}.}
\tag{2.3}
\]

For each pair of a base-row support point \((i,h)\) and a dual support
point \((i,g)\), the only translation to which it contributes is

\[
 \boxed{t=gh^{-1}.}
\tag{2.4}
\]

Thus the following accumulator computes all nonzero pairings without
scanning \(H_0\):

\[
 A_j(t)=
 \sum_{\substack{i,h,g\\g h^{-1}=t}}
 a^{(j)}_{i,h}\lambda_{i,g}.
\tag{2.5}
\]

Same-translation terms are summed in \(k\) before deciding activity.  This
last aggregation is essential: two or three occurrence pairs may cancel in
characteristic three.

### Theorem 2.1 (SIX-ACTION SUPPORT-HITTING ORACLE)

For every sparse dual \(\lambda\), the nonzero entries of (2.5) are exactly
the pairs \((j,t)\) for which

\[
 \langle\lambda,L_tR_j\rangle\ne0.
\tag{2.6}
\]

In particular,

\[
 A_j(t)=0\ \text{for all }j,t
 \quad\Longleftrightarrow\quad
 \lambda(D_0)=0.
\tag{2.7}
\]

#### Proof

Equation (2.3) says that a summand indexed by \((i,h)\) is nonzero only
when \(th=g\) for a support point \(g\) of the same dual component.  This
equation has the unique solution (2.4).  Grouping all such summands by that
solution gives (2.5), hence (2.6).  The translated rows in (1.7) span
\(D_0\), so annihilating every one of them is equivalent to annihilating
their span.  This proves (2.7). \(\square\)

No completeness assumption on a previously generated translation roster is
used.  Completeness comes directly from the finite supports of the current
dual and the six fixed rows.

## 3. Rank progress and safe batching

Let \(B\) be the current quotient echelon and let \(x\) be the target
remainder.  Choose a dual \(\lambda\) with

\[
 \lambda(B)=0,\qquad \lambda(x)=1.
\tag{3.1}
\]

If (2.5) contains an active pair, then its row is not in \(B\), because
\(\lambda\) vanishes on \(B\) and not on that row.  Hence inserting the
first active row strictly raises the rank.  All active rows may instead be
materialized in deterministic order and sequentially reduced; every row
that survives raises rank, and dependent rows are harmlessly discarded.
The dual is recomputed after the batch.

If (2.5) is empty, (2.7) proves that this particular dual already
annihilates the *entire* six-family space \(D_0\).  Therefore no missing PB4
action translation can change the current separation.  At that point the
producer may pass to the compact correction oracle.  It may not infer a
negative A0 result unless the separately preregistered correction schedule
is also complete.

For one dual the arithmetic work is bounded by

\[
 \sum_{j=1}^{6}\sum_{i=1}^{5}
 |\operatorname{supp}(R_{j,i})|
 |\operatorname{supp}(\lambda_i)|,
\tag{3.2}
\]

not by \(6|H_0|\).  Only the nonzero accumulator keys and a bounded insertion
batch need be retained.  This is the exact analogue of task416's
\(t=gh^{-1}\) oracle, with eleven PB4 families replaced by the six rows in
(1.2) and with both PB3 families deleted.

## 4. Central powers give no additional oracle rows

For an action row \(R_j\), v402's central contraction gives

\[
 \boxed{
 Q_4^{\rm cen}(L_{t\zeta^m}R_j)
 =Q_4^{\rm cen}(L_tR_j)=(L_tR_j,0)
 \qquad(t\in H_0,\ m=0,1,2).}
\tag{4.1}
\]

Indeed, orbit summation sends all three central positions to the same
\(H_0\) coefficient.  Moving a \(\zeta\)-shifted noncentral coordinate to
the canonical position produces a central-coordinate update equal to a
scalar multiple of \(d_1R_j\), which is zero by (1.5).  Thus the support
formula (2.4) must canonicalize both \(g\) and \(h\) by

\[
 h=h_0\zeta^{\kappa(h)},\qquad
 g=g_0\zeta^{\kappa(g)},
\tag{4.2}
\]

and operate on the retained \(H_0\) keys.  Scanning three central-power
copies is redundant and using a lexicographic orbit representative in place
of \(h_0=h\zeta^{-\kappa(h)}\) breaks the registered action ABI.

## 5. The retained central scalar

After the constructive elimination of the five central families, write the
last coordinate on the canonical orbit as

\[
 (Z'_0(h_0),Z'_1(h_0),Z'_2(h_0)).
\tag{5.1}
\]

The closed survivor is

\[
 U_0(h_0)=Z'_0(h_0)-Z'_2(h_0),\qquad
 U_1(h_0)=Z'_1(h_0)-Z'_2(h_0),
\tag{5.2}
\]

together with

\[
 \boxed{\tau=\sum_{h_0\in H_0}Z'_2(h_0).}
\tag{5.3}
\]

It is not \(\sum_{h_0,m}Z'_m(h_0)\).  For the constant vector
\((1,1,1)\) on one orbit, the latter is \(3=0\) in \(k\), while (5.3) is
one.  Hence replacing (5.3) by an all-coordinate sum strictly enlarges the
kernel and can create a false positive.

## 6. Exact consequence for the A0 production owner

Combining v401, v402, v403 and Theorem 2.1 gives the following finite
positive-first loop.

1. Apply the two PB3 normal maps and the PB4 Tietze/central normal map to the
   target and every literal correction column, preserving all three physical
   tags until after those maps.
2. Reject a proposed positive terminal unless both PB3 normal forms, every
   PB4 \(U_0,U_1\), and (5.3) vanish after adding the selected correction.
3. On the PB4 \(H_0\)-part use (2.5).  Every accepted action row strictly
   advances the current quotient span; an empty accumulator is a complete
   six-family separation for the current dual.
4. Retain action and literal-correction ancestry.  Quotient zero may be
   promoted only through v403's independent literal-word, exact exponent,
   joint-kernel, selected-action, and survivor replay.

The five central PB4 closures, both PB3 closures, and an enumeration of
\(H_0\) are absent from this loop.  What remains potentially long is the
compact correction-word search, not the six-action completeness test.

```text
SIX PB4 ACTION BASE ROWS:                  CLOSED / EXPLICIT
ALL H0 TRANSLATE PAIRINGS FOR ONE DUAL:    CLOSED SUPPORT FORMULA
H0 OR CENTRAL-POWER ENUMERATION:           NOT REQUIRED
EMPTY ACTION ACCUMULATOR FOR CURRENT DUAL: EXACT SIX-FAMILY SEPARATOR
COMPACT CORRECTION SCHEDULE:               STILL FINITE POSITIVE-FIRST
ACTUAL A0 COMMON WORD:                     NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:    NONE
```

`R07_A0_SIX_ACTION_SUPPORT_HITTING_V404_PAPER_GRADE`
