# R07 ambient-extension binding of the actual cyclic class v101

Author: Sol / 2026-08-26

Status: abstract conditional cyclic-extension lemma.  V102 shows that its A3
predicate is not supplied by the v96 rho/literal shear: the roof (C_9) power
and the five-coface (C_5)-rho operation are type-distinct.  Thus this note is
not presently an interface to the actual matched A.18 successor problem.
The finite restriction-zero premise for the constructed field-outer module is
independently cross-checked in
`sol/luna_reply_162_field_outer_full_pair_return_crosscheck_v4.md`.
The ambient extension occurrence and, especially, the A3 chain comparison
required below have not been constructed for the actual R07 edge.  No
compatible cofinal lift, fake certificate, or Ihara witness is declared.
`verified=false`.

## 1. Why the fine-shadow preimage is circular

Let (L'leq L) be isolated windows and let

\[
 r:GT(L')\longrightarrow GT(L)
\tag{1.1}
\]

be reduction.  It is a group homomorphism, but it need not be surjective.
For (P\leq GT(L)), put (E=r^{-1}(P)).

### Lemma 1.1 (FINE-PREIMAGE CIRCULARITY)

The sequence

\[
 1\longrightarrow \ker r\longrightarrow E
 \xrightarrow{,r,}P\longrightarrow1
\tag{1.2}
\]

is exact at (P) if and only if

\[
 P\leq\operatorname{im}r.
\tag{1.3}
\]

For a fixed (g\in P), the fibre (r^{-1}(g)) is nonempty if and only if
(g\in\operatorname{im}r).

#### Proof

The image of (E\to P) is (P\cap\operatorname{im}r).  This equals (P)
exactly under (1.3).  The last assertion is the same statement for one
fibre. \(\square\)

Thus one may not define the desired full-pair class by first declaring
(r^{-1}(P)\to P) to be an extension: its surjectivity already says that
every element of (P), including R07, has a fine shadow lift.  This is the
totality statement which the obstruction theory is meant to prove.

The cure is to use an **ambient partial-lift group** which is defined before
the fine GT relations are imposed.  Its surjectivity must be proved from raw
word/automorphism lifting, not from the existence of fine shadows.

## 2. The non-circular ambient-extension predicate

Work over (k=\mathbf F_3).  Let

\[
 H\lhd P,\qquad [P:H]=3,
\qquad R=\langle g\rangle\cong C_9,
\qquad D=\langle g^3\rangle\cong C_3,\qquad D\leq H.
\tag{2.1}
\]

Let (V) be a finite (kP)-module.  Fix the same multiplication side,
return, two printed hexagons, and printed-order A.18 word as in v96--v99.
Say that one actual successor edge satisfies
`AMB-PAIR-A18(F;P,H,R,D,V)` when the following four items are supplied.

**A1 (raw ambient extension).**  Before imposing the new fine relation
values there is an exact sequence

\[
 1\longrightarrow V\longrightarrow\mathcal E_{\rm raw}
 \xrightarrow{\pi}P\longrightarrow1.
\tag{2.2}
\]

The group \(\mathcal E_{\rm raw}\) consists of typed partial automorphisms of
the matched arity-(3/4/5) diagram.  Its multiplication is literal
composition, and its surjectivity is proved by raw word lifting.  It is not
the preimage of (P) inside the unknown fine GT-shadow group.

**A2 (arithmetic nulling).**  The known arithmetic lifts give a displayed
group section

\[
 s_H:H\longrightarrow\mathcal E_{\rm raw}.
\tag{2.3}
\]

Changing a chosen set section of (2.2) to agree with (s_H) is part of the
record.

**A3 (actual R07 binding).**  A displayed lift (t\in\mathcal E_{\rm raw})
of (g=\mathrm{row36}) is built from the exact common word (F).  Under the
fixed theta/rho coordinates, its ninth-power residual

\[
 \beta:=t^9\in V
\tag{2.4}
\]

is exactly the normalized cyclic numerator obtained from the two literal
hexagons and the cyclic rho relation.  V96's integral shear carries the same
record to the printed A.18 residual.  The nulling on (D) is the restriction
of (2.3), not an unrelated cyclic choice.

**A4 (actual correction materialization).**  For every allowed (u\in V),
the left-corrected lift (ut) is represented by one actual common-word
transition-kernel value, and

\[
 (ut)^9=N_gu+\beta,
 \qquad N_g=1+g+\cdots+g^8.
\tag{2.5}
\]

The materialized value preserves the old mark, the two hexagons, the
commutator/relative domain, and the finite side gate.  Equivalently, A4 may be
restricted to a displayed preimage of the particular (-\beta).

A1--A3 replace v83's B1--B4 by one group-extension occurrence and one literal
power comparison.  A4 is v83's B5 in the same occurrence.

## 3. The binding theorem

### Theorem 3.1 (AMBIENT-EXTENSION FULL-PAIR BINDING)

Assume `AMB-PAIR-A18(F;P,H,R,D,V)`.  The extension (2.2), with the arithmetic
section (2.3), determines a canonical relative class

\[
 \Omega_F\in
 K^2(P,H;V)=
 \ker\bigl(H^2(P,V)\longrightarrow H^2(H,V)\bigr).
\tag{3.1}
\]

Under restriction to ((R,D)) and the standard normalized-bar to periodic
cyclic comparison, this class is exactly

\[
 \omega_F=[\beta]\in
 \frac{\ker(g-1)\cap(g-1)^6V}{(g-1)^8V}.
\tag{3.2}
\]

Consequently, if

\[
 \operatorname{im}\!\left[
 K^2(P,H;V)\longrightarrow K^2(R,D;V)
 \right]=0,
\tag{3.3}
\]

then there is (u\in V) with

\[
 (g-1)^8u=-\beta,
\tag{3.4}
\]

and A4 materializes (u) as a literal one-step correction killing the
cyclic theta/rho residual and hence, by v96, the printed A.18 residual.

#### Proof

Choose a normalized set section (s:P\to\mathcal E_{\rm raw}) agreeing with
(s_H) on (H).  Its factor set

\[
 z(p,q)=s(p)s(q)s(pq)^{-1}\in V
\tag{3.5}
\]

is a normalized inhomogeneous two-cocycle.  Associativity of
(\mathcal E_{\rm raw}) gives (dz=0).  Since (s|_H=s_H) is a group
homomorphism, (z|_{H\times H}=0).  Hence ([z]) is the relative class
(\Omega_F) in (3.1).  A different normalized section changes (z) by a
coboundary.

Restrict the extension to (R=\langle g\rangle), and independently choose its
cyclic section with lift (t) of (g).  It need not be the restriction of the
preceding (H)-compatible set section; changing between the two sections only
adds a coboundary.  The usual periodic-resolution representative of the
restricted extension class is the power defect (t^9=\beta).  This can also be
checked without citing a comparison theorem: (t\beta t^{-1}=\beta), so

\[
 (g-1)\beta=0.
\tag{3.6}
\]

Replacing (t) by (ut) changes the power defect by

\[
 u+gu+\cdots+g^8u=N_gu.
\tag{3.7}
\]

In characteristic three,

\[
 N_g=1+g+\cdots+g^8=(g-1)^8.
\tag{3.8}
\]

The restriction to (D=\langle g^3\rangle) is null by A2, but this must be
compared inside the same extension rather than by identifying the two
sections.  There is a unique (a\in V) such that

\[
 s_H(g^3)=a t^3.
\tag{3.9}
\]

Since (s_H) is a homomorphism and ((g^3)^3=1), cubing (3.9) gives

\[
 0=(a t^3)^3=(1+g^3+g^6)a+\beta.
\tag{3.10}
\]

The subgroup norm is

\[
 1+g^3+g^6=(g-1)^6,
\tag{3.11}
\]

so (3.10) proves, in the actual ambient occurrence,

\[
 \beta\in\ker(g-1)\cap(g-1)^6V.
\tag{3.12}
\]

Equations (3.7)--(3.12) identify the restricted relative class with (3.2),
including its quotient by ((g-1)^8V).  This proves the claimed bar/periodic
comparison directly and establishes A3 as the load-bearing literal binding.

Under (3.3), the class (3.2) is zero, so
(\beta\in(g-1)^8V).  Choose (u) with (3.4).  Equations (2.5) and (3.8)
give ((ut)^9=0) in additive kernel notation.  A4 and v96 give the literal
correction conclusion. \(\square\)

### Corollary 3.2 (NO FULL TWO-COCYCLE TABLE IS NEEDED)

Once A1--A4 are authenticated, one need not serialize (z(p,q)) for all
(p,q\in P).  Exactness of (2.2), the arithmetic section, the one literal
power identity (t^9=\beta), and the correction norm formula determine the
required relative and cyclic classes functorially.

This reduces the actual-class comparison from an arbitrary (243^2)-entry
cocycle table to an ambient-extension occurrence plus one row36 power replay.

## 4. Application of the repaired finite restriction calculation

For the constructed field-outer module (V_{\rm mix}), the independent v4
replay gives, for both frozen candidates (H=H_{A9},H_{A12}),

\[
 \operatorname{im}\!\left[
 K^2(P_0,H;V_{\rm mix})
 \longrightarrow K^2(R,D;V_{\rm mix})
 \right]=0.
\tag{4.1}
\]

The mandatory quotient-action canary now passes:

\[
 U^3=1,
\tag{4.2}
\]

the induced (E_2^{1,1}) restriction has rank zero, and the target outer
terms (H^2(Q,V^D),H^3(Q,V^D)) vanish.  Thus (4.1) is no longer quarantined.
The signed source transgression ranks remain unknown but are not used in
Theorem 3.1.

What is still missing is not another full-pair cohomology computation.  It is
the actual occurrence A1--A4.  In particular, v99 supplies the affine PaB
residual and its refinement naturality, but it does not construct the raw
ambient group (2.2) and does not identify that affine residual with (t^9).

## 5. Smallest next actual receipt

At one frozen successor edge the following finite record is sufficient.

1. A based group of raw matched-diagram partial automorphisms
   (mathcal E_{\rm raw}), a surjection to (P_0), and a proof that its
   kernel occurrence is the displayed (V_{\rm mix}).
2. The arithmetic section on (H_{A9}) or (H_{A12}), including exact
   multiplication replay.
3. The exact row36 lift (t) built from the same signed word as the actual
   R07 prefix, with (t^9) replayed in the kernel basis.
4. Equality of that vector with the normalized theta/rho residual obtained
   from the literal two-hexagon/A.18 stack via v96.
5. A common-word preimage for a solution of
   ((g-1)^8u=-\beta), followed by the side-gate replay.

The current fresh target6 computation is a safe over-approximation screen for
item 5.  A `NONMEMBER` kills the selected g760 prefix before this receipt is
built.  A `MEMBER` only permits construction of items 1--5; it does not prove
them.

## 6. Fixed ledger

```text
FINE-PREIMAGE CIRCULARITY LEMMA:                  PAPER_PROOF
AMBIENT-EXTENSION BINDING THEOREM:                PAPER_PROOF
FIELD-OUTER FULL-PAIR -> CYCLIC RESTRICTION ZERO: CROSS_CHECKED FINITE
ACTUAL RAW AMBIENT EXTENSION A1:                  OPEN
ARITHMETIC SECTION IN THE SAME OCCURRENCE A2:     OPEN
ROW36 POWER = ACTUAL THETA/RHO DEFECT A3:         OPEN
COMMON-WORD MATERIALIZATION / SIDE GATES A4:      OPEN
UNIFORM ACTUAL-IMAGE CONTRACTION:                 OPEN
COMPATIBLE COFINAL R07 LIFT:                      NOT CONSTRUCTED
FAKE CERTIFICATE / IHARA WITNESS:                 NOT DECLARED
```

No new finite computation, external source, or Lean proof is used in this
note.
