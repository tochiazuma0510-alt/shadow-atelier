# R07 A0 PB3/PB4 physical-quotient positive terminal (v403)

Author: Sol / 2026-08-30

Status: paper theorem combining v396, v399, v401, and v402. It proves that a
positive A0 terminal may be checked in the exact physical PB3/PB4 quotients;
the eliminated translated boundary families need not be rebuilt merely to
emit MEMBER. The actual finite split antecedent for PB4 is cross-checked by
task418. No A0 computation, common word, compatible lift, fake, or Ihara
witness is reported here. `verified=false`.

## 1. The physical three-block boundary quotient

Let (k=\mathbf F_3). In the frozen physical row ABI write

\[
 Z=Z_1\oplus Z_2\oplus Z_4\oplus k^2,
 \qquad
 Z_i=k[H_3]^3\ (i=1,2),\qquad Z_4=k[H_4]^6,
\tag{1.1}
\]

where the last two coordinates are v399's normalized exponent pair. The two
copies of (Z_i) retain the two PB3 block tags, and (Z_4) retains the PB4
tag. Let

\[
 D=D_3^{(1)}\oplus D_3^{(2)}\oplus D_4\oplus0
\tag{1.2}
\]

be the complete physical boundary image: two translated PB3 presentation
families in either PB3 block and all eleven translated PB4 presentation
families in the PB4 block.

For a PB3 block let

\[
 Q_3=\Pi_3J_{\rm T}:Z_i\longrightarrow Y_3
\tag{1.3}
\]

be v401's sparse Tietze map followed by its central-orbit normal map. Thus

\[
 \ker Q_3=D_3^{(i)}.
\tag{1.4}
\]

For PB4 let (J_4) be v402's six-sparse Tietze Fox map. First quotient the
five central commutator families by the constructive map

\[
 Q_4^{\rm cen}:Z_4\longrightarrow
 Y_4^{\rm cen}=k[H_0]^5\oplus k[H_4]/(NI_{H_0}).
\tag{1.5}
\]

Its kernel is the central five-family span. Let (D_0\le k[H_0]^5) be the
span of all (H_0)-translates of the six action columns in v402 (1.6), and
put

\[
 \overline Y_4=(k[H_0]^5/D_0)\oplus k[H_4]/(NI_{H_0}),
 \qquad Q_4=({\rm quotient})Q_4^{\rm cen}J_4.
\tag{1.6}
\]

V402 Theorem 4.1 gives

\[
 \ker Q_4=D_4.
\tag{1.7}
\]

Define the physical quotient map

\[
 Q=Q_3\oplus Q_3\oplus Q_4\oplus\operatorname{id}_{k^2}.
\tag{1.8}
\]

### Theorem 1.1 (PHYSICAL PB34 KERNEL)

\[
 \boxed{\ker Q=D.}
\tag{1.9}
\]

#### Proof

The block tags make (1.2) an external direct sum. Equations (1.4) and (1.7)
identify the kernel on its three group-algebra blocks, while the identity on
the normalized coordinates has zero kernel. Taking their direct sum proves
(1.9). \(\square\)

## 2. The six-family lazy form is equivalent

A producer need not materialize the quotient by (D_0). Write a PB4
central-normal form as

\[
 Q_4^{\rm cen}J_4(R_4)=(S(R_4),U(R_4)),
 \quad S(R_4)\in k[H_0]^5,
 \quad U(R_4)\in k[H_4]/(NI_{H_0}).
\tag{2.1}
\]

Then (1.7) is exactly the executable criterion

\[
 \boxed{R_4\in D_4\iff U(R_4)=0\ \hbox{ and }\ S(R_4)\in D_0.}
\tag{2.2}
\]

Thus positive-first column generation may retain (S), keep (U) as closed
survivor coordinates, and generate only the six action families lazily. A
selected finite list of action translates proving (S\in D_0), together
with (U=0), is a complete positive certificate. It is not necessary to
enumerate the five eliminated central families or to expand their full
preimage.

Central powers do not enlarge the remaining oracle. V402 proves that a

\[
 \zeta^j h_0
\tag{2.3}
\]

translate of an action column has the same image in (1.5) as its (h_0)
translate. Hence the oracle canonicalizes translations by the first PC
coordinate and ranges only over (H_0).

## 3. Quotient after literal physical aggregation is safe

Let (J(c)) be v396's full occurrence row for a literal correction
(c\in\Omega), and let (L_gJ(c)\in Z) be the frozen signed-prefix physical
aggregation. Different occurrences need not share an actor. The safe hot
path here is nevertheless simply

\[
 c\longmapsto L_gJ(c)\longmapsto Q(L_gJ(c)).
\tag{3.1}
\]

No equivariance of (Q L_g) under one common source action is asserted or
needed. The correction oracle first materializes each literal conjugate
(\delta r\delta^{-1}) with the authenticated occurrence formula and only
then applies the linear physical quotient (Q). Since (1.9) is a statement
on the already tagged physical space, linearity gives

\[
 Q\!\left(\sum_j\alpha_jL_gJ(c_j)\right)
 =\sum_j\alpha_jQ(L_gJ(c_j)).
\tag{3.2}
\]

This does not revive the rejected v390 shortcut. What remains forbidden is
to infer a quotient source action after aggregation and close seeds under
that unproved action. Literal direct columns followed by (Q) are exact.

## 4. Exact positive A0 terminal

Let (T\in Z) be the frozen A0 target, including normalized pair zero. Let a
finite word-bearing positive search construct (c_*\in\Omega). Put

\[
 R=T+L_gJ(c_*).
\tag{4.1}
\]

### Theorem 4.1 (QUOTIENT MEMBER TO COMMON WORD)

Assume all of the following are independently replayed:

1. the literal word (c_*) lies in the registered joint kernel;
2. its normalized exponent pair is zero;
3. both PB3 components of (Q(R)) are zero;
4. the closed PB4 survivor (U(R_4)) is zero; and
5. selected, replayed translates of the six action columns sum to
   (S(R_4)).

Then

\[
 \boxed{R\in D.}
\tag{4.2}
\]

After the v399 exactification, the resulting literal word
(c_{\rm exact}) has exact integer exponent pair ((0,0)), lies in the
joint kernel, and represents the same all-seven physical boundary class.
Consequently it is an exact finite A0 common word.

#### Proof

Items 3--5 and (2.2) say (Q(R)=0); item 2 handles the final two coordinates.
Theorem 1.1 gives (4.2). Item 1 supplies a legal literal correction rather
than an abstract column. V399 Theorem (3.2)--(3.6) then multiplies by cubes
of the authenticated (u_0,v_0), kills the integer exponent pair, and
changes the characteristic-three all-seven row by zero. Therefore the
exactified word has the same accepted class. \(\square\)

The independent checker may prove the five hypotheses directly in quotient
coordinates. Rebuilding all eliminated boundary translates is redundant
because (1.9) is precisely their kernel theorem. A negative terminal still
requires exhaustive completion of the remaining finite action/correction
schedule; an unfinished lazy search is only `UNKNOWN_RESOURCE`.

```text
TWO PB3 TRANSLATED CLOSURES:             ELIMINATED BY ker(Q3)=D3
FIVE CENTRAL PB4 FAMILIES:               ELIMINATED BY ker(Q4cen)=Dcen
REMAINING PB4 ACTION FAMILIES:            SIX / LAZY H0 TRANSLATES
POSITIVE QUOTIENT ZERO -> A0 MEMBER:      PAPER THEOREM
OLD ELIMINATED-BOUNDARY REPLAY ON MEMBER: NOT REQUIRED
ACTUAL A0 COMMON WORD:                    NOT COMPUTED
COFINAL LIFT / FAKE / IHARA WITNESS:      NONE
```

`R07_A0_PB34_PHYSICAL_QUOTIENT_TERMINAL_V403_PAPER_GRADE`
