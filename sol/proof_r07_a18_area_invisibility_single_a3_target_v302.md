# R07 A.18 area-invisibility and single A3 target theorem (v302)

## 0. Scope and correction to v301

V301 reduced the dependence of the exponent-nine A3 pre-gate on an A0 roof
correction to three signed-area classes.  In the frozen A.18 occurrence
roster, those three targets are in fact equal.  The reason is elementary but
load-bearing: the image of a roof correction is central in every class-two
occurrence quotient, and the signed product of its eleven occurrence images
is the identity separately in H1, H2, and P.

Consequently A3's complete projected pre-gate can be run once from the fixed
word \(g_{760}\) and accepted task198, before any A0 correction is selected.
This is a paper theorem.  The one actual target has not been evaluated and no
projected MEMBER/NONMEMBER certificate, pointed multiplier, lift, fake, or
Ihara witness is claimed.

## 1. Central occurrence factors

Keep v210--v211 and v301 notation

\[
 D_1=\mathcal H_2(9),\qquad z=[x,y]^3,\qquad
 \phi_9(a)=z^t\quad(a\in H_0,\ t\in\mathbf F_3).
\tag{1.1}
\]

For the eleven task198 occurrences put

\[
 z_o=q_o(z)=[q_o(x),q_o(y)]^3.
\tag{1.2}
\]

Every \(z_o\) is central in the relevant class-two PB3 or PB4 quotient and
has order dividing three.  If \(r_o=\overline{\rho_o(g_{760})}\), then

\[
 \overline{\rho_o(g_{760}a)}=r_oz_o^t.
\tag{1.3}
\]

For a direct occurrence this contributes \(r_oz_o^t\); for an inverse
occurrence it contributes

\[
 (r_oz_o^t)^{-1}=z_o^{-t}r_o^{-1}=r_o^{-1}z_o^{-t}.
\tag{1.4}
\]

Thus the frozen right-to-left printed product in a block \(B\) satisfies

\[
 \boxed{
 R_B(g_{760}a)=R_B(g_{760})K_B^t,\qquad
 K_B=\prod_{o\in B}z_o^{\sigma_o},}
\tag{1.5}
\]

where \(\sigma_o\) is task198's literal `factor_sign`.  Reversal of the
printed factor order does not affect the collected \(z_o\), since they are
central.

## 2. Literal H1 and H2 cancellation

Use the PB3 central basis \(c_{123}\), with the v225 bracket convention

\[
 [A_{12},A_{13}]=c_{123},\quad
 [A_{12},A_{23}]=-c_{123},\quad
 [A_{13},A_{23}]=c_{123}.
\tag{2.1}
\]

Only abelianizations of each substitution pair are needed because
commutators are bilinear in a class-two group.  The exact task198/task226
substitution and sign tables give

\[
\begin{array}{c|c|c|c}
B&o&(L_o,R_o)&\sigma_o\,q_o(z)\\ \hline
H1&1&(x,y)&-3c_{123}\\
H1&2&(x,(xy)^{-1})&-3c_{123}\\
H1&3&(y,(xy)^{-1})&-3c_{123}\\ \hline
H2&4&((yx)^{-1},x)&+3c_{123}\\
H2&5&(x,y)&+3c_{123}\\
H2&6&((yx)^{-1},y)&+3c_{123}.
\end{array}
\tag{2.2}
\]

For example \([x,y]^3=-3c_{123}\) in these marked PB3 coordinates, while
\([x,(xy)^{-1}]^3=+3c_{123}\); occurrence 2 has sign \(-1\).  The remaining
rows follow by the same alternating bilinear bracket calculation.

The H1 signed sum is \(-9c_{123}\), and the H2 signed sum is
\(+9c_{123}\).  Both vanish modulo nine.  Hence

\[
 \boxed{K_{H1}=K_{H2}=1.}
\tag{2.3}
\]

## 3. Literal pentagon cancellation

Use the PB4 central basis
\((c_{123},c_{124},c_{134},c_{234})\).  The nonzero brackets are the twelve
v225 brackets

\[
\begin{array}{lll}
[A_{12},A_{13}]=c_{123},&
[A_{12},A_{23}]=-c_{123},&
[A_{13},A_{23}]=c_{123},\\
[A_{12},A_{14}]=c_{124},&
[A_{12},A_{24}]=-c_{124},&
[A_{14},A_{24}]=c_{124},\\
[A_{13},A_{14}]=c_{134},&
[A_{13},A_{34}]=-c_{134},&
[A_{14},A_{34}]=c_{134},\\
[A_{23},A_{24}]=c_{234},&
[A_{23},A_{34}]=-c_{234},&
[A_{24},A_{34}]=c_{234}.
\end{array}
\tag{3.1}
\]

Applying the alternating bilinear bracket to the five frozen substitution
pairs gives the following signed central vectors:

\[
\begin{array}{c|c|c|c}
o&\text{task198 slot}&(L_o,R_o)&\sigma_o\,q_o(z)\\ \hline
7&P_{b1}&(A_{23},A_{34})&(0,0,0,-3)\\
8&P_{b2}&(A_{12}A_{13},A_{24}A_{34})&(0,-3,-3,0)\\
9&P_{b3}&(A_{12},A_{23})&(-3,0,0,0)\\
10&P_{b5}^{-1}&(A_{13}A_{23},A_{34})&(0,0,+3,+3)\\
11&P_{b4}^{-1}&(A_{12},A_{23}A_{24})&(+3,+3,0,0).
\end{array}
\tag{3.2}
\]

Rows 10 and 11 include their literal inverse-slot signs.  Every coordinate
in the sum of (3.2) is zero modulo nine.  Therefore

\[
 \boxed{K_P=1.}
\tag{3.3}
\]

This calculation uses all five printed pentagon factors, including their
order-independent central contributions; it is not a three-factor or
abelianized pentagon surrogate.

## 4. Single-target theorem

### Theorem 4.1 (A.18 AREA INVISIBILITY)

For every A0 roof correction \(a\in\Omega\leq H_0\),

\[
 \boxed{
 \overline{R_B(g_{760}a)}=\overline{R_B(g_{760})}
 \quad(B=H1,H2,P)}
\tag{4.1}
\]

in the matching exponent-nine class-two quotient.  Consequently

\[
 \boxed{
 \bar\epsilon(g_{760}a)=\bar\epsilon(g_{760})}
\tag{4.2}
\]

for every possible literal A0 common correction, independently of its area
class.

#### Proof

Equation (1.5) collects the correction factors in each block.  Equations
(2.3) and (3.3) say that all three collected factors are the identity.
Substitution proves (4.1).  Since
\(\epsilon_B(f)=1-\overline{R_B(f)}\) by v225 equation (1.5), (4.2)
follows.  QED.

### Corollary 4.2 (ONE COMPLETE PRE-A0 A3 TEST)

Let \(w,U_0,C\) be the fixed v225/v216 data constructed from
\(g_{760}\).  Then

\[
 \boxed{
 \forall a\in\Omega:\quad
 \text{A3 pre-gate passes for }g_{760}a
 \iff
 \bar\epsilon(g_{760})\in C(U_0).}
\tag{4.3}
\]

Thus v301's three-class passing set is necessarily

\[
 T_{\rm gate}=\mathbf F_3
 \quad\text{or}\quad
 T_{\rm gate}=\varnothing.
\tag{4.4}
\]

One rank-at-most-486 closure and one membership test decide the projected
A3 fate of every A0 correction on the fixed \(g_{760}\) branch.

#### Proof

The closure \(U_0\) already depends only on \(g_{760}\) by v225--v216.
Theorem 4.1 makes its target independent of \(a\).  Apply v216 Theorem 3.1.
QED.

## 5. Production consequence

The next actual A3 producer need not wait for task192 and must not pretend
that an unconstructed correction word exists.  It consumes accepted task198,
the pinned literal \(g_{760}\), and the static PB3/PB4 class-two constructors;
it then:

1. reconstructs the eleven \(r_o,p_o,\xi_o,w_o\) from \(g_{760}\);
2. reconstructs the three base values \(R_B(g_{760})\) and the single target
   \(1-R_B(g_{760})\);
3. independently replays the signed central tables (2.2) and (3.2), requiring
   \(K_{H1}=K_{H2}=K_P=1\);
4. runs the already SELFTEST-accepted v216 one-seed closure and an independent
   canonical 486-row checker; and
5. emits either a coefficient-bearing MEMBER certificate or a separating
   NONMEMBER dual for the whole fixed A0 branch.

A NONMEMBER result obstructs every registered A0 correction before the
expensive common-word search.  A MEMBER result removes only the projected
A3 filter: A0, the simultaneous pointed gate, exact PB endpoints, nonlinear
side conditions, mixed-prime and perfect-core gates remain necessary.

The area row of v301 remains a valid A0 certificate refinement, but A3 no
longer needs it as a selector.

```text
SIGNED CENTRAL PRODUCT IN H1:              IDENTITY / PAPER PROOF
SIGNED CENTRAL PRODUCT IN H2:              IDENTITY / PAPER PROOF
SIGNED CENTRAL PRODUCT IN P:               IDENTITY / PAPER PROOF
A3 TARGET DEPENDENCE ON A0 AREA CLASS:      NONE / PAPER PROOF
COMPLETE PRE-A0 A3 DECISION:                1 CLOSURE + 1 TARGET TEST
ACTUAL TARGET / MEMBER OR NONMEMBER:         NOT COMPUTED
A0 COMMON WORD / POINTED GATE / EXACT PB:   OPEN
COFINAL LIFT / FAKE / IHARA:                NONE
```

`R07_A18_AREA_INVISIBILITY_SINGLE_A3_TARGET_V302_PAPER_GRADE`
