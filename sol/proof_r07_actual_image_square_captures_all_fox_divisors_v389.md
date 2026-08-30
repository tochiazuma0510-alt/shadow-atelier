# R07 actual-image square captures every Fox divisor v389

Author: Sol / 2026-08-30

Status: paper theorem following v369, v372, v386, and v388.  Once the
path-bearing occurrence/Fox divisor map is identified with the restriction of
the existing actual leading square, every primitive-by-seed divisor is already
in the reachable image.  Thus no separate A0-style membership search is needed
for the saturation divisors.  Authentication of that one physical square,
the ambient filtered Fox estimate, the initial full path-bearing membership,
and the remaining actual lift gates are still open.  No compatible lift, fake
certificate, or Ihara witness is declared.  \(\mathtt{verified=false}\).

## 1. The two maps which must not be duplicated

Fix one matched finite elementary-abelian coordinate \(i\).  Use the same
finite actor and coefficient ring as v388:

\[
 R_i=k[\Gamma_i],
 \qquad
 I_i=\ker\bigl(R_i\longrightarrow k[\overline\Gamma_i]\bigr),
 \qquad
 P_i:=P_C/\ker(\widehat\Xi\to R_i)P_C\cong R_i^r.
\tag{1.1}
\]

Let \(e_{i1},\ldots,e_{ir}\) be the retained free-seed basis and let

\[
 q_i^P:P_C\twoheadrightarrow P_i
\tag{1.2}
\]

be the canonical finite-source reduction.  Put
\(L_i=\pi_i^L(L_{\rm reach})\).  The finite leading map
\(B_{C,i}:P_i\to L_i\) is required to be the induced map, so the square

\[
 \boxed{\pi_i^L B_C=B_{C,i}q_i^P}
\tag{1.3}
\]

commutes.  The finite reduction of v369's actual-image square is

\[
\begin{CD}
 P_i @>{\tau_i}>> A_i\\
 @V{B_{C,i}}VV       @VV{B_{{\rm act},i}}V\\
 L_i @>{\iota_i}>> L_{{\rm amb},i},
\end{CD}
\tag{1.4}
\]

where \(A_i\) is the cumulative one-common-word image, not a direct product
of separately chosen occurrence values.  The load-bearing equality is

\[
 \boxed{\iota_iB_{C,i}=B_{{\rm act},i}\tau_i.}
\tag{1.5}
\]

Both sides use the same v372 finite Magnus states, ten enriched contexts,
ten-to-eleven occurrence map, inverse signs, and printed factor order.

V388 introduces the path-bearing divisor map

\[
 \Sigma_i:I_iP_i\longrightarrow L_{{\rm amb},i}.
\tag{1.6}
\]

There must not be an independent second interpretation of the same Fox path.
The required **no-duplicate-owner identity** is

\[
 \boxed{
 \Sigma_i
 =\left.B_{{\rm act},i}\tau_i\right|_{I_iP_i}
 =\left.\iota_iB_{C,i}\right|_{I_iP_i}.}
\tag{1.7}
\]

Equation (1.7) is not inferred from equality of endpoints.  It is an equality
of retained Fox/Magnus paths after complete PB boundaries and localization.
It is an additional physical no-duplicate-owner condition beyond the common
square demanded in v369 Section 5.  It must be checked with the same evaluator
on the relative ideal where v388 places the nonlinear divisors.

By surjectivity of \(P_C\to P_i\), compatibility of \(B_C\), and the
definition of the reachable module in v382,

\[
 \boxed{
 B_{C,i}(P_i)=\pi_i^L(B_C(P_C))
 \subseteq\pi_i^L(L_{\rm reach})=L_i.}
 \tag{1.8}
\]

Indeed, for \(p_i\in P_i\), choose \(p\in P_C\) with \(q_i^P(p)=p_i\).
Then (1.3) gives

\[
 B_{C,i}(p_i)=\pi_i^L(B_C(p))\in L_i.
\tag{1.9}
\]

Commutativity also makes this value independent of the chosen lift.
Surjectivity onto \(L_i\) is not assumed.

Below we identify \(L_i\) with its embedded image
\(\iota_i(L_i)\subseteq L_{{\rm amb},i}\).  The codomain of \(\Sigma_i\)
is not assumed to be \(L_i\); proving that its divisor image lands there is
the content of Theorem 2.1.

## 2. Primitive membership is automatic from the square

Retain a word-bearing kernel basis

\[
 K_i=\langle k_{i1},\ldots,k_{it_i}\rangle_{\mathbf F_3}.
\tag{2.1}
\]

V388's correctly typed primitive-by-seed roster is

\[
 G_i^{\rm prim}
 =\left\{
  \Sigma_i((k_{ij}-1)e_{ia}):
  1\leq j\leq t_i,\ 1\leq a\leq r
 \right\}.
\tag{2.2}
\]

### Theorem 2.1 (ACTUAL-SQUARE PRIMITIVE CAPTURE)

Under (1.3), (1.5), and (1.7),

\[
 \boxed{G_i^{\rm prim}\subseteq B_{C,i}(P_i)\subseteq L_i.}
\tag{2.3}
\]

More strongly,

\[
 \boxed{
 \Sigma_i(I_iP_i)=B_{C,i}(I_iP_i)
 \subseteq B_{C,i}(P_i)\subseteq L_i.}
\tag{2.4}
\]

#### Proof

For every \(j,a\), equation (1.7) gives

\[
 \Sigma_i((k_{ij}-1)e_{ia})
 =\iota_iB_{C,i}((k_{ij}-1)e_{ia}).
\tag{2.5}
\]

The argument of \(B_{C,i}\) belongs to \(I_iP_i\subseteq P_i\), so (1.8)
puts its image in \(L_i\).  This proves (2.3).  Applying the same identity
to every element of \(I_iP_i\) proves (2.4). \(\square\)

No score matrix, right inverse, A0 common word, or choice of a preimage is
used.  The element \((k_{ij}-1)e_{ia}\) itself is already the named preimage.

## 3. Every ordered divisor is reachable

V388 Theorem 4.1 gives, under the same occurrence/Fox ABI,

\[
 \pi_i(\mathcal D_{\rm Fox})
 \subseteq \widehat\Xi_i\cdot G_i^{\rm prim}.
\tag{3.1}
\]

The finite image \(L_i\) is an \(\widehat\Xi_i\)-submodule.  Combining
(2.3) with (3.1) gives the following.

### Corollary 3.1 (FINITE FOX-DIVISOR CAPTURE)

At every coordinate satisfying the finite-source square (1.3) and the
no-duplicate-owner identity (1.7),

\[
 \boxed{\pi_i(\mathcal D_{\rm Fox})\subseteq L_i.}
\tag{3.2}
\]

If (1.3) and (1.7) are authenticated at every matched coordinate for the
same compatible path-bearing owner, v386 Theorem 1.1 applies and yields

\[
 \boxed{
 \mathcal D_{\rm Fox}\subseteq L_{\rm reach},
 \qquad E_{\rm Fox}=L_{\rm reach}.}
\tag{3.3}
\]

Consequently the class-specific \(E_{\rm Fox}\)-saturation quotients used
after the v384 replacement vanish:

\[
 \boxed{
 L_{\rm reach}\cap\widehat J^nE_{\rm Fox}
 =\widehat J^nL_{\rm reach}
 \qquad(n\geq0).}
\tag{3.4}
\]

#### Proof

Equation (3.2) is (3.1), (2.3), and submodule closure.  The compatible
coordinatewise statement is precisely v386 hypothesis (1.3), so its global
capture theorem gives (3.3).  Equation (3.4) follows because the two modules
in (3.3) are equal. \(\square\)

This replaces both the arbitrary finite retraction matrix of v384 and the
separate primitive-membership search left open in v386.  The identity map is
the resulting retraction on \(E_{\rm Fox}\).  It does not assert the broader
equality
\(L_{\rm reach}\cap\widehat J^nL_{\rm amb}
=\widehat J^nL_{\rm reach}\).

## 4. Finite authentication of the square

The assertion is uniform but its finite certificate is small.  Because
\(P_i=R_i^r\), equality (1.5) follows from:

1. direct equality

   \[
    \iota_i\bigl(B_{C,i}(e_{ia})\bigr)
    =B_{{\rm act},i}(\tau_i(e_{ia}))
    \qquad(1\leq a\leq r);
   \tag{4.1}
   \]

2. authentication that both maps use the same \(R_i\)-action, which is the
   finite image of the \(\widehat\Xi_i\)-action; and
3. replay of the same v372 path-bearing occurrence evaluator, including all
   ten contexts, eleven slots, four inverse occurrences, complete PB
   boundaries, localization, and printed order.

Under clauses 1--2, \(R_i\)-linearity extends (4.1) from the free basis to
all of \(P_i\), proving (1.5).  Clause 3 additionally identifies the
independently named divisor map with that restriction, giving (1.7).
Equivalently, an
implementation which separately serializes \(\Sigma_i\) may compare the
finite \(t_i r\) rows (2.5); a mismatch rejects the duplicated owner.

No compatible choice of kernel bases across coordinates is needed.  The
maps and global divisor paths are compatible; each finite basis is only a
certificate that the coordinate ideal has been completely generated.

## 5. What remains for A9

Corollary 3.1 removes a separate mathematical search:

\[
 \boxed{
 \text{finite-source + actual-image + no-duplicate-owner squares}
 \Longrightarrow
 \text{all Fox divisors reachable}
 \Longrightarrow
 \text{all relevant }E_{\rm Fox}\text{-relative saturation classes zero}.}
\tag{5.1}
\]

It does not authenticate the square.  It also does not prove:

1. the ambient filtered Fox estimate placing each nonlinear error in the
   required \(\widehat J^{d+1}E_{\rm Fox}\);
2. the one full initial path-bearing membership of v382 equation (5.2);
3. leading onto/strictness before those two physical gates are supplied;
4. nonabelian accepted-set nonemptiness; or
5. mixed-prime, perfect-core, settlement, fake, or Ihara gates.

In particular, A0 may still supply the initial actual common word and the
main witness branch, but it is no longer a logically necessary membership
oracle for the saturation-divisor family.  A4 remains necessary for the
executable successor/witness chain and for a word-bearing finite certificate;
it is not needed to prove the abstract inclusion (2.4).

~~~text
PRIMITIVE-BY-SEED DIVISORS LIE IN im B_C:          PAPER PROOF / SQUARE CONDITIONAL
ALL FOX DIVISORS LIE IN L_reach:                   PAPER PROOF / SQUARE CONDITIONAL
E_FOX = L_reach / SATURATION ZERO:                 PAPER PROOF / SQUARE CONDITIONAL
SEPARATE PRIMITIVE MEMBERSHIP SEARCH:              NOT NEEDED
PHYSICAL v369/v372 ACTUAL-IMAGE SQUARE:             NOT AUTHENTICATED
AMBIENT FILTERED FOX DEPTH:                         OPEN PHYSICAL BINDING
ONE FULL PATH-BEARING INITIAL MEMBERSHIP:           NOT COMPUTED
REGISTERED RELATIVE PRO-3 LIFT (A9):                CONDITIONAL / 0 OF 3 ACTUAL
FAKE / IHARA WITNESS:                              NOT DECLARED
~~~

\(\mathtt{R07\_ACTUAL\_IMAGE\_SQUARE\_CAPTURES\_ALL\_FOX\_DIVISORS\_V389\_AUDIT\_CANDIDATE}\)
