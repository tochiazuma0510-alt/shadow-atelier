# R07 exponent-nine non-roof endpoint screen v208

Author: Sol / 2026-08-28

Status: paper theorem and finite-screen design.  It removes the class-two
Heisenberg branch from the actual post-roof obstruction search and replaces it
by the first canonical quotient which can see below the exponent-three roof.
The quotient is finite, but no actual roof relator, first multiplier, endpoint,
repair dual, compatible lift, fake certificate, or Ihara witness is computed
here.  `verified=false`.

## 1. Why every exponent-three endpoint screen is a roof canary

For \(r=3,4\), the frozen fine braid factor is

\[
 \Pi_r[3]=PB_r/N_r(3),
\tag{1.1}
\]

the maximal exponent-three quotient of \(PB_r\).  It occurs as a marked factor
of

\[
 E_3=Q_0\times\Pi_3[3],\qquad
 E_4=Q_4\times\Pi_4[3]
\tag{1.2}
\]

in every one of the ten distinct typed roof coordinates of v122/v189.

### Theorem 1.1 (EXPONENT-THREE SCREENS FACT THROUGH THE ROOF)

Let \(T_o:PB_{B(o)}\twoheadrightarrow R_o\) be a finite marked quotient at
each of the eleven literal occurrences, where every \(R_o\) has exponent
dividing three.  Then the joint source map

\[
 F(x,y)\longrightarrow\prod_o R_o
\tag{1.3}
\]

factors through the correctly typed roof group \(\Delta_0\).

#### Proof

By maximality of (1.1), each \(T_o\) factors uniquely through the
corresponding marked map \(PB_{B(o)}\to\Pi_{B(o)}[3]\).  The latter is one of
the typed factors retained by the roof coordinate for occurrence \(o\).
The repeated E3 occurrence is reinserted diagonally, while the E3 and E4
coordinates both labelled `C21` remain distinct.  Taking the product of the
eleven factorizations therefore gives a homomorphism from the v189 roof image
\(\Delta_0\) to the product in (1.3).  This is the claimed factorization.
\(\square\)

### Corollary 1.2 (HEISENBERG IS NOT A NON-ROOF SCREEN)

The order-\(27\) Heisenberg quotient used in the old B3 source census, and
every other exponent-three nilpotent or nonnilpotent endpoint quotient, is a
roof-factor screen.  Under the positive task192/task193 roof-correction
hypothesis, v207 therefore forces its three combined endpoint values to be
zero.  A nonzero value is an implementation/type failure, not a mathematical
obstruction.

The old order-\(27\) group is the two-generator **source** quotient
\(F_2/(F_2^3\gamma_3F_2)\).  It must not be confused with the class-two
exponent-three quotients of the endpoint groups: those have orders \(3^4=81\)
for \(PB_3\) and \(3^{10}=59{,}049\) for \(PB_4\).  All three objects are
still exponent-three and hence are covered by Theorem 1.1.

## 2. The canonical class-two exponent-nine endpoint quotients

Put

\[
 \mathcal N_r(9)=
 PB_r/\langle\gamma_3PB_r,\ g^9\ (g\in PB_r)\rangle^{\rm normal}
 \qquad(r=3,4).
\tag{2.1}
\]

These quotients retain one \(3\)-power layer below the exponent-three roof.
They are canonical verbal quotients, so every strand deletion, coface, and
source substitution descends without a choice of presentation section.

### Lemma 2.1 (NORMAL FORM AND ORDER)

Let

\[
 a_r=\binom r2,\qquad b_r=\binom r3.
\tag{2.2}
\]

Then \(\mathcal N_r(9)\) has a class-two Malcev normal form with
\(a_r\) degree-one coordinates and \(b_r\) central commutator coordinates,
all in \(\mathbf Z/9\mathbf Z\).  In particular,

\[
 |\mathcal N_r(9)|=9^{a_r+b_r},
\tag{2.3}
\]

so

\[
 |\mathcal N_3(9)|=9^4=6{,}561,
 \qquad
 |\mathcal N_4(9)|=9^{10}=3{,}486{,}784{,}401.
\tag{2.4}
\]

#### Proof

The iterated Fadell--Neuwirth decomposition of \(PB_r\) is an almost-direct
product of the free groups \(F_1,F_2,\ldots,F_{r-1}\).  Its first two
lower-central ranks are therefore

\[
 \operatorname{rank}\operatorname{gr}_1PB_r
 =\sum_{i=1}^{r-1}i=\binom r2,
\tag{2.5}
\]

and

\[
 \operatorname{rank}\operatorname{gr}_2PB_r
 =\sum_{i=1}^{r-1}\frac{i^2-i}{2}=\binom r3.
\tag{2.6}
\]

The same almost-direct splitting gives torsion-free integral lower-central
layers.  Hence \(PB_r/\gamma_3PB_r\) is a torsion-free class-two nilpotent
group with a Malcev basis consisting of the coordinates in (2.2).

In a class-two group,

\[
 (uv)^9=u^9v^9[v,u]^{\binom92},\qquad \binom92=36.
\tag{2.7}
\]

Both \(9\) and \(36\) are divisible by \(9\).  Thus every ninth power has
all Malcev coordinates divisible by \(9\).  Conversely the ninth powers of
the degree-one basis elements lie in the verbal subgroup, and the ninth
powers of the central commutator basis do also, for example through
\([u^9,v]=[u,v]^9\).  The verbal ninth-power subgroup is therefore exactly
the sublattice obtained by multiplying every Malcev coordinate by \(9\).
Reduction of all \(a_r+b_r\) coordinates modulo \(9\) proves (2.3)--(2.4).
\(\square\)

There is a natural reduction

\[
 \mathcal N_r(9)\twoheadrightarrow\mathcal N_r(3),
\tag{2.8}
\]

and \(\mathcal N_r(3)\) is a quotient of \(\Pi_r[3]\).  The extra layer in
(2.8), rather than its exponent-three reduction, is the only part which can
separate two source words already equal at the roof.

## 3. A 6,441-relator decision for being genuinely non-roof

Let

\[
 \Omega_0:F(x,y)\twoheadrightarrow\Delta_0
\tag{3.1}
\]

be the v189 ten-coordinate roof map, and let
\(\mathcal R_{6441}\) be the complete source-word relator roster of v190, so

\[
 H_0:=\ker\Omega_0
 =\langle\!\langle\mathcal R_{6441}\rangle\!\rangle_F.
\tag{3.2}
\]

At every literal occurrence use the quotient (2.1), retaining all eleven
positions and ten typed substitutions, and define

\[
 \Omega_9:F(x,y)\longrightarrow
 \mathcal N_3(9)^6\times\mathcal N_4(9)^5.
\tag{3.3}
\]

The duplicate E3 map occurs twice in (3.3), because its prefixes and signs
are different even though its two group values agree.

### Theorem 3.1 (EXACT NON-ROOF TEST)

The exponent-nine joint screen factors through the roof if and only if

\[
 \boxed{\Omega_9(r)=1\quad\text{for every }r\in\mathcal R_{6441}.}
\tag{3.4}
\]

Consequently one relator with \(\Omega_9(r)\ne1\) is an exact certificate
that (3.3) does not factor through \(\Delta_0\).

#### Proof

A factorization through \(\Delta_0=F/H_0\) exists exactly when
\(H_0\leq\ker\Omega_9\).  The latter kernel is normal.  Equation (3.2)
therefore makes this containment equivalent to (3.4).  \(\square\)

This is a finite semantic decision, not a search.  Every relator is reduced
by the ten-coordinate class-two coordinate evaluator, and all 6,441 results
must be inspected.  If (3.4) holds, the quotient is another roof canary and
must be discarded.  If it fails, the nonidentity relator and its complete
typed coordinate tuple are retained before any actual endpoint calculation.

## 4. The joint translating group has at most 729 states

Let

\[
 D_9=\operatorname{im}\Omega_9.
\tag{4.1}
\]

Although the individual PB4 quotient in (2.4) is large, the joint group is
generated by the two common source letters.

### Theorem 4.1 (TWO-GENERATOR CLASS-TWO BOUND)

\[
 \boxed{|D_9|\leq729.}
\tag{4.2}
\]

More precisely, \(D_9\) is a quotient of

\[
 \mathcal H_2(9)=
 F(x,y)/\langle\gamma_3F,\ w^9\ (w\in F)\rangle^{\rm normal},
\tag{4.3}
\]

and

\[
 |\mathcal H_2(9)|=9^3=729.
\tag{4.4}
\]

#### Proof

Every component of (3.3) has nilpotency class at most two and exponent
dividing nine.  Hence \(\ker\Omega_9\) contains the verbal subgroup in
(4.3), giving the quotient statement.  Lemma 2.1 applied to a free group of
rank two gives two degree-one coordinates and one commutator coordinate,
each modulo nine.  This proves (4.4), and then (4.2). \(\square\)

Thus the complete joint BFS needed by v200 has at most 729 states, not
\(9^{10}\) states and not 357,128,352 roof states.  Individual PB3/PB4
values are stored sparsely by their \(4\)- or \(10\)-coordinate normal forms;
the group algebra of \(\mathcal N_4(9)\) is never materialized as a dense
array.

## 5. Interface with the exact endpoint selector

After task192/task193/v188/v191 produce the actual finite word-pair
representative \(M_0\), project the three v198 combined endpoints to

\[
 k[\mathcal N_3(9)]_{H1}\oplus
 k[\mathcal N_3(9)]_{H2}\oplus
 k[\mathcal N_4(9)]_P,
 \qquad k=\mathbf F_3.
\tag{5.1}
\]

The two PB3 summands remain separately tagged.  If the initial projected
endpoint is nonzero, v200 applies with the translating group \(D_9\), whose
complete roster is bounded by Theorem 4.1.  A completed projected dual gives
an exact NO for every finite-support representative of the same \(\mu_1\).
A projected YES remains only a seed for exact Artin/Garside replay.

The 729-state bound by itself closes only the translating-word orbit.  V209
subsequently proves that this particular exponent-nine screen does not need
a complete Schreier roster of the first-successor kernel: the visible image
of \(H_1\) is recovered from a joint rank closure on the roof-relator
defects.  Non-roof status in Theorem 3.1 still does not predict whether the
actual endpoint or its repair dual is nonzero.

## 6. Fixed production order and claim boundary

1. Finish the independently audited 6,441-word export and occurrence ledger.
2. Replay all 6,441 relators in (3.3).
3. If every value is one, record `EXP9_CLASS2_ROOF_FACTOR` and do not run an
   endpoint obstruction job with this quotient.
4. If one value is nonidentity, freeze the first such full typed tuple and
   enumerate the complete \(D_9\) roster, bounded by 729.
5. Wait for the actual \(M_0\) and the complete successor-kernel interface;
   then run the v200 projected selector.

```text
ALL EXPONENT-THREE ENDPOINT SCREENS:              ROOF-FACTOR CANARIES
OLD ORDER-27 HEISENBERG SOURCE GATE:              NOT A NON-ROOF ENDPOINT GATE
CLASS-TWO EXPONENT-NINE PB3/PB4 QUOTIENTS:        PAPER-CONSTRUCTED
EXACT ORDER PB3 / PB4:                            6,561 / 3,486,784,401
EXACT NON-ROOF IFF 6,441-RELATOR TEST FAILS:      PAPER-PROOF
JOINT SOURCE ACTION GROUP:                        ORDER AT MOST 729
ACTUAL 6,441-RELATOR EXPONENT-NINE REPLAY:         NOT RUN
ACTUAL M0 / PROJECTED ENDPOINT / COMPLETE SPAN:   NOT COMPUTED
SAME-mu1 EXACT REPAIR / RELATIVE PRO-3 LIFT:      NOT CONSTRUCTED
FAKE / IHARA WITNESS:                             NOT DECLARED
```

`R07_EXPONENT9_NONROOF_ENDPOINT_SCREEN_V208_PAPER_GRADE`
