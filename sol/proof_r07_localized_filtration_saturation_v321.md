# R07 localized filtration saturation gate (v321)

Author: Sol / 2026-08-29

Status: paper refinement of v252 and v319.  It identifies the exact gap
between ambient depth inside a localized residual submodule and the intrinsic
depth required by the based free cover.  The gap is one saturation kernel.
Vanishing of the actual remainder class is necessary and sufficient; full
strictness is stronger than needed.  The actual R07 classes have not been
computed.  No compatible lift, fake certificate or Ihara witness is declared.

## 1. Ambient and intrinsic filtrations

Let \(\Lambda\) be complete for a two-sided ideal \(J\), let \(Z\) be a
complete separated left \(\Lambda\)-module, and let

\[
 L\subseteq Z
\tag{1.1}
\]

be a closed \(\Lambda\)-submodule of localized residuals.  There are two
a priori different depth-\(r\) subspaces:

\[
 J^rL
\quad\text{and}\quad
 L\cap J^rZ.
\tag{1.2}
\]

Always

\[
 J^rL\subseteq L\cap J^rZ,
\tag{1.3}
\]

but equality is not formal.  Inclusion \(L\hookrightarrow Z\) induces

\[
 \iota_r:L/J^rL\longrightarrow Z/J^rZ.
\tag{1.4}
\]

### Lemma 1.1 (LOCALIZED SATURATION KERNEL)

\[
 \boxed{
 \ker\iota_r=
 \frac{L\cap J^rZ}{J^rL}.}
\tag{1.5}
\]

#### Proof

An element \(z\in L\) maps to zero in \(Z/J^rZ\) exactly when
\(z\in J^rZ\).  Quotienting those elements by the elements already zero in
\(L/J^rL\) gives (1.5). \(\square\)

This is the module-level analogue of v129's cyclic saturation kernel.  Here
the submodule \(L\) is the whole formation/Brunnian localized target rather
than \(B(A)+\Lambda z\) for one class.

## 2. Exact coefficient criterion

Let

\[
 q:F=\Lambda^t\twoheadrightarrow L
\tag{2.1}
\]

be a finite free cover with the intrinsic quotient filtration, so

\[
 q(J^rF)=J^rL.
\tag{2.2}
\]

### Theorem 2.1 (ACTUAL LOCALIZED DEPTH CRITERION)

For \(z\in L\cap J^rZ\), the following are equivalent:

1. there is \(v\in J^rF\) with \(q(v)=z\);
2. \(z\in J^rL\);
3. the class of \(z\) in (1.5) is zero.

#### Proof

The equivalence of 1 and 2 is (2.2), and the equivalence of 2 and 3 is the
definition of the quotient (1.5). \(\square\)

Thus v252's ambient conclusion

\[
 z_{\mathrm{new}}\in L\cap J^{r+1}Z
\tag{2.3}
\]

can be fed to v319 at intrinsic depth \(r+1\) exactly when its class

\[
 \boxed{
 [z_{\mathrm{new}}]\in
 (L\cap J^{r+1}Z)/J^{r+1}L}
\tag{2.4}
\]

vanishes.  Localization and depth gain alone do not prove this.

### Corollary 2.2 (FULL STRICTNESS)

The following are equivalent:

1. \(J^rL=L\cap J^rZ\) for every \(r\);
2. every map \(\iota_r\) in (1.4) is injective;
3. every ambient depth-\(r\) localized residual has a depth-\(r\)
   free-cover coefficient.

Under these conditions the saturation step in v319 is automatic.

Full strictness is stronger than the explicit-witness route needs.  It is
enough that (2.4) vanish for each recursively encountered exact remainder,
with one retained coefficient \(v_{r+1}\).

## 3. Corrected localized Newton theorem

Retain all hypotheses and notation of v319 except do not identify the two
filtrations in (1.2).

### Theorem 3.1 (POINTED-SATURATED LOCALIZED NEWTON)

Suppose:

1. \(Bs=q\) is the complete based lift of v319;
2. at step \(r\), \(z_r=\Phi(w_r)\) has a retained coefficient
   \(v_r\in J^rF\) with \(q(v_r)=z_r\);
3. the correction \(a_r=-s(v_r)\) kills the active layer and exact replay
   returns

   \[
   z_{r+1}\in L\cap J^{r+1}Z;
   \tag{3.1}
   \]

4. the actual saturation class (2.4) of \(z_{r+1}\) vanishes, and a
   coefficient \(v_{r+1}\in J^{r+1}F\) is retained.

Then the corrections converge and the limiting literal residual is zero.

#### Proof

The retained coefficient at depth \(r\) gives exactly the v319 correction:

\[
 B(-s(v_r))=-q(v_r)=-z_r.
\tag{3.2}
\]

The affine law kills depth \(r\), giving (3.1).  Theorem 2.1 and hypothesis
4 supply the correctly typed next coefficient.  Induction gives coefficients
and corrections in every successive intrinsic depth.  Their product is
Cauchy, and completeness and separatedness give zero limiting residual as
in v319 Theorem 3.1. \(\square\)

### Corollary 3.2 (STRUCTURAL AND POINTED ROUTES)

V319 is valid in either of two precise forms:

1. **structural:** prove full strictness once and use every ambient localized
   depth gain; or
2. **pointed:** return a zero saturation class and one free-cover ancestry
   for each exact remainder on the selected branch.

The structural route is the desired closed all-refinement theorem.  The
pointed route remains a uniform explicit algorithm only after a terminating
finite saturation solver is proved available at every encountered level.

## 4. Finite dual certificate

At a finite quotient, write

\[
 S_r=(L\cap J^rZ)/J^rL.
\tag{4.1}
\]

Ordinary finite-dimensional elimination gives the complete alternatives:

\[
\begin{array}{ll}
\text{MEMBER:}&
 z=\sum_i c_iq(f_i),\quad f_i\in J^rF,\\[1mm]
\text{NONMEMBER:}&
 \lambda(J^rL)=0,\quad \lambda(z)\ne0
\end{array}
\tag{4.2}
\]

for a functional \(\lambda\) on \(L\cap J^rZ\).  MEMBER ancestry is the next
v319 coefficient.  NONMEMBER rejects full strictness and blocks the named
localized based recursion at that state.  It does not reject:

1. a larger localized module with a different intrinsic filtration;
2. the narrow cyclic route if that route has a differently typed ancestry;
3. a different first word or based cover; or
4. existence of an R07 witness.

A bounded failure to find the rows spanning \(J^rL\) is UNKNOWN, not the
NONMEMBER alternative in (4.2).

## 5. Why topological equivalence is insufficient by itself

Suppose one only knows that the intrinsic and ambient subspace topologies on
\(L\) are equivalent, for example through an Artin--Rees-type bounded lag.
This gives a function \(\rho(r)\to\infty\) with

\[
 L\cap J^rZ\subseteq J^{\rho(r)}L.
\tag{5.1}
\]

It does not give the same-depth inclusion required in Theorem 2.1.  A
correction whose source depth is only \(\rho(r)<r\) can create nonlinear
terms at depth below \(r+1\), so one cannot silently reindex v319's
one-layer induction.  A bounded-lag version would need a separately proved
nonlinear depth estimate in that reindexed filtration.

Therefore neither closedness of \(L\), finite generation, nor a generic
Artin--Rees slogan may replace the literal saturation class (2.4).

## 6. R07 certificate boundary

For the v252 target

\[
 L\subseteq
 R_S(G_{H1})\times R_S(G_{H2})\times
 \bigl(B_P\cap R_S(G_P)\bigr),
\tag{6.1}
\]

an all-depth positive package must do one of:

1. present \(L\) as a strict filtered quotient of one finite free
   common-source module and prove equality in Corollary 2.2; or
2. after each literal replay, return the actual MEMBER ancestry in (4.2).

The first class-two remainder \(q_2\) is the first saturation canary for the
localized route.  Its test differs from v263's cyclic return:

\[
\begin{array}{c|c}
\text{cyclic route}&q_2\in[\Xi\beta]_2,\\
\text{localized route}&q_2\in J^2L
\text{ with a free-cover coefficient.}
\end{array}
\tag{6.2}
\]

The localized condition may pass when the cyclic condition fails, but it is
not automatic from \(q_2\in L\cap J^2Z\).

    LOCALIZED SATURATION KERNEL:                 PAPER PROOF
    ACTUAL SAME-DEPTH COEFFICIENT IFF CLASS ZERO: PAPER PROOF
    POINTED-SATURATED NEWTON COMPLETION:          PAPER PROOF
    AMBIENT v252 DEPTH AUTOMATICALLY INTRINSIC:   FALSE / NOT ASSUMED
    ACTUAL FULL STRICTNESS:                       NOT PROVED
    ACTUAL q2 LOCALIZED SATURATION CLASS:         NOT COMPUTED
    COMPATIBLE COFINAL LIFT / FAKE / IHARA:       NONE

R07_LOCALIZED_FILTRATION_SATURATION_V321_PAPER_GRADE
