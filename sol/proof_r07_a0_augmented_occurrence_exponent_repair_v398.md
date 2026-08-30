# R07 A0 augmented-occurrence exponent repair v398

Author: Sol / 2026-08-30

Status: paper correction to v396/v397.  The invariant-span reduction and the
at-most-44 compact seed theorem remain valid, but the occurrence source must
carry the two source exponent coordinates explicitly.  Omitting them can
admit a false A0 MEMBER.  No executed closure, COMMON, lift, fake, or Ihara
witness is declared.

## 1. Defect in the unaugmented notation

V396 defines an eleven-occurrence Fox state \(J_{\rm occ}(c)\) and later puts
the physical target in

\[
 Z=Z_{H_1}\oplus Z_{H_2}\oplus Z_P\oplus\mathbf F_3^2.
\tag{1.1}
\]

The last two coordinates are the exponent sums of the source word in \(x,y\),
reduced modulo three.  They are present in the frozen task179
`AllSevenModel.occurrence_column` implementation, but they do not arise by
aggregating only the eleven PB3/PB4 Fox blocks.  Thus v396 equations
(1.2)--(1.5) must be read in the following augmented form.

## 2. Correct augmented source and action

Let

\[
 \epsilon:F(x,y)\longrightarrow\mathbf Z^2,
 \qquad
 \bar\epsilon=\epsilon\bmod3:F(x,y)\longrightarrow\mathbf F_3^2.
\tag{2.1}
\]

Put

\[
 \widetilde U=
 \left(\bigoplus_{o\in\mathcal O}C_o\right)\oplus\mathbf F_3^2,
 \qquad
 \widetilde J(c)=\bigl(J_{\rm occ}(c),\bar\epsilon(c)\bigr).
\tag{2.2}
\]

Extend the occurrence-dependent actor by the identity on the last summand:

\[
 \widetilde\rho(s)=\rho_{\rm occ}(s)\oplus
 \operatorname{id}_{\mathbf F_3^2}.                       \tag{2.3}
\]

### Lemma 2.1 (AUGMENTED CONJUGATION LAW)

For \(c\in\Omega\) and \(s\in F\),

\[
 \widetilde J(cd)=\widetilde J(c)+\widetilde J(d),
 \qquad
 \boxed{\widetilde J(scs^{-1})=
        \widetilde\rho(s)\widetilde J(c).}                \tag{2.4}
\]

#### Proof

The occurrence coordinates obey v396 equations (1.4) and (2.2).  The
exponent map is a homomorphism, and

\[
 \bar\epsilon(scs^{-1})=
 \bar\epsilon(s)+\bar\epsilon(c)-\bar\epsilon(s)
 =\bar\epsilon(c),                                        \tag{2.5}
\]

which is exactly the identity action in (2.3). \(\square\)

Let \(\widetilde W\) be the invariant span of the selected presentation
seeds under the four actions
\(\widetilde\rho(x^{\pm1}),\widetilde\rho(y^{\pm1})\).
The proof of v396 Theorem 2.1 applies word for word to (2.4), and gives

\[
 \boxed{\widetilde J(\Omega)=\widetilde W.}               \tag{2.6}
\]

Replacing the 6,441 roster by the v397 compact roster does not change this
space because the two rosters have the same normal closure.  Consequently
the insertion bound remains

\[
 \boxed{44+4\dim\widetilde W}.                            \tag{2.7}
\]

## 3. Correct physical aggregation and membership

Define

\[
 \widetilde L_g:widetilde U\longrightarrow Z,
 \qquad
 \widetilde L_g(u,e)=\bigl(L_g(u),e\bigr).                \tag{3.1}
\]

The exact correction column is

\[
 \widetilde{\mathscr V}(c)=\widetilde L_g\widetilde J(c).
\tag{3.2}
\]

Every typed PB3/PB4 boundary row has zero in the exponent summand, so

\[
 D\subset Z_{H_1}\oplus Z_{H_2}\oplus Z_P\oplus\{0\}^2.
\tag{3.3}
\]

The exact finite A0 test is therefore

\[
 \boxed{-T\in D+\widetilde L_g(\widetilde W).}            \tag{3.4}
\]

Equation (3.3) means that (3.4) enforces the two mod-three exponent equations;
they cannot be supplied or cancelled by boundary ancestry.  After a positive
terminal, v156/v265 performs the separately proved integer exactification.

## 4. Mandatory producer/checker ABI

The task411 compact owner and its independent checker must implement all of
the following.

1. A compact seed row equals the eleven separately tagged Fox coordinates
   plus `exponent_pair(seed_word) mod 3`.
2. Each of the four actors permutes/translates only occurrence coordinates
   and copies the two exponent entries unchanged.
3. Physical aggregation merges the eleven blocks and carries both exponent
   entries unchanged.
4. The fifteen boundary seeds and every one of their translates have zero
   exponent entries.
5. Seed replay agrees with the frozen task179
   `AllSevenModel.occurrence_column([], seed_word)`, not merely with an
   exponent-free `aggregate_tagged(term_vector(...))`.
6. MEMBER ancestry is replayed against both physical blocks and both exponent
   coordinates before exact integer exponent correction is attempted.

This is a two-coordinate augmentation only.  It does not enlarge the actor
roster, reintroduce the global conjugator search, or alter the speed/memory
architecture of v396/v397.

```text
V396 INVARIANT-SPAN THEOREM:       RETAINED WITH J -> J_TILDE
V397 <=44 SEED REDUCTION:          RETAINED
SOURCE EXPONENT MOD-3 COORDINATES: RESTORED (2)
BOUNDARY EXPONENT COORDINATES:     EXACTLY ZERO
A0 ACTUAL MEMBERSHIP:              NOT YET EXECUTED
```

`R07_A0_AUGMENTED_OCCURRENCE_EXPONENT_REPAIR_V398_PAPER_GRADE`
