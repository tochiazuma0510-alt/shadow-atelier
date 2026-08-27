# R07 `u0/v0` boundary-normalization shortcut v161

Author: Sol / 2026-08-27

Status: paper theorem and positive finite-computation contract.  The two
boundary preimages required below have not yet been computed.  This note does
not assert that task179 has returned a common word and does not declare a
compatible cofinal lift, fake, or Ihara witness.

## 1. The first-rung system

Let (C) be the finite ({\bf F}_3)-space of word-bearing correction
coefficients and let (D) be the separately typed direct sum of the PB3/PB4
presentation-boundary coefficients.  Put

\[
 E=C\oplus D,
 \qquad
 A:E\longrightarrow V,
 \tag{1.1}
\]

where (A(c,d)=A_C(c)+A_D(d)) is the simultaneous H1/H2/printed-pentagon
change.  The normalized exponent map is

\[
 N:E\longrightarrow {\bf F}_3^2,
 \qquad
 N(c,d)=\epsilon(c)/18\pmod 3,
 \qquad N(0,d)=0.
 \tag{1.2}
\]

V156 proves that division by 18 is integral on every registered correction
word in the joint kernel.  A raw task179 positive receipt gives

\[
 A(c,d)=t.
 \tag{1.3}
\]

It does not by itself give (N(c,d)=0).

Let the registered q0-relator words be (r_3,r_9,r_{12}), and set

\[
 v_0=r_9r_{12}r_3^{-2},
 \qquad
 u_0=r_9v_0^{-8}.
 \tag{1.4}
\]

The exact integer exponent computation of V156 gives

\[
 \epsilon(v_0)=(0,18),
 \qquad
 \epsilon(u_0)=(18,0),
 \tag{1.5}
\]

so

\[
 N(u_0)=e_1,
 \qquad N(v_0)=e_2.
 \tag{1.6}
\]

Each word in (1.4) lies in the registered joint kernel because it is a
product of registered defining relators and their inverses.

## 2. The two finite boundary questions

Regard (u_0,v_0) as word-bearing correction coefficients.  The shortcut
asks for boundary chains (d_u,d_v\in D) satisfying

\[
 A_C(u_0)+A_D(d_u)=0,
 \qquad
 A_C(v_0)+A_D(d_v)=0.
 \tag{2.1}
\]

These are two exact membership questions in the full span of all translated
PB3/PB4 boundary rows.  They cannot be inferred from (1.5): V156 controls the
joint-kernel exponent lattice, not the all-seven change modulo boundaries.

### Proposition 2.1 (explicit kernel-residue basis)

If (2.1) holds, then

\[
 (u_0,d_u),(v_0,d_v)\in\ker A
 \tag{2.2}
\]

and

\[
 \boxed{N(\ker A)={\bf F}_3^2.}
 \tag{2.3}
\]

#### Proof

Equation (2.1) is exactly the assertion (2.2).  Boundaries have zero
normalized exponent, so (1.6) gives

\[
 N(u_0,d_u)=e_1,
 \qquad
 N(v_0,d_v)=e_2.
\]

The two vectors span ({\bf F}_3^2), proving (2.3).  \(\square\)

By the rank identity of V160 this is equivalent to

\[
 \operatorname{rank}(A,N)-\operatorname{rank}A=2,
 \tag{2.4}
\]

but (2.1) is stronger certificate data: it supplies the two literal
word-bearing preimages and their separately typed boundary chains.

## 3. Closed normalization of any raw positive word

For (a\in{\bf F}_3), define the literal signed-power selector

\[
 q(w,a)=
 \begin{cases}
 1,&a=0,\\
 w^{-1},&a=1,\\
 w,&a=2.
 \end{cases}
 \tag{3.1}
\]

Thus (q(w,a)) realizes coefficient (-a\) over ({\bf F}_3), with
coefficient two represented by a literal inverse at the underlying column
level.

### Theorem 3.1 (RAW-TO-NORMALIZED SHORTCUT)

Assume (2.1), and let a raw positive receipt give (1.3).  Write

\[
 N(c,d)=(a,b).
 \tag{3.2}
\]

Set, with right multiplication and free reduction,

\[
 c_1=c\,q(u_0,a)\,q(v_0,b),
 \qquad
 d_1=d-a d_u-b d_v.
 \tag{3.3}
\]

Then

\[
 \boxed{A(c_1,d_1)=t},
 \qquad
 \boxed{N(c_1,d_1)=0}.
 \tag{3.4}
\]

Moreover

\[
 \epsilon(c_1)\in54{\bf Z}^2.
 \tag{3.5}
\]

#### Proof

All correction factors in (3.3) lie in the joint kernel.  Fox additivity on
that kernel identifies ordered word product with addition of their
first-rung correction columns.  From (2.1),

\[
\begin{aligned}
 A_C(c_1)
 &=A_C(c)-aA_C(u_0)-bA_C(v_0)\\
 &=A_C(c)+aA_D(d_u)+bA_D(d_v).
\end{aligned}
\]

Adding (A_D(d_1)) and using (1.3) proves the first equation in (3.4).
Equations (1.6), (3.1), and (3.2) prove the second.

Write

\[
 \epsilon(c)=(18m,18n).
\]

Here (m\equiv a\pmod3) and (n\equiv b\pmod3).  Formula (3.3) changes the
two exponent coordinates by (-18a) and (-18b), respectively, modulo the
literal representatives in (3.1).  Hence both resulting coordinates are
divisible by 54, proving (3.5).  \(\square\)

The boundary coefficient (d_1) remains quotient-certificate data.  It is
never multiplied into (c_1).

## 4. Exact integer closure

Write

\[
 \epsilon(c_1)=(54\alpha,54\beta).
 \tag{4.1}
\]

Put

\[
 h=u_0^{-3\alpha}v_0^{-3\beta},
 \qquad
 c_{\rm exact}=c_1h.
 \tag{4.2}
\]

### Proposition 4.1 (exact first-rung word)

Under the hypotheses of Theorem 3.1,

\[
 \epsilon(c_{\rm exact})=(0,0),
 \qquad
 A_C(c_{\rm exact})=A_C(c_1),
 \tag{4.3}
\]

and consequently

\[
 A(c_{\rm exact},d_1)=t.
 \tag{4.4}
\]

#### Proof

The exponent statement follows immediately from (1.5), (4.1), and (4.2).
Because (u_0,v_0) evaluate to the identity in every registered quotient,
the Fox derivative of a cube is three copies of the same translated
derivative.  It is zero over ({\bf F}_3).  Therefore every factor in (h)
has zero first-rung all-seven change, proving the second equation in (4.3).
Equation (4.4) follows from (3.4).  \(\square\)

The producer and checker must nevertheless replay (c_{\rm exact})
literally through the joint group, both hexagons, the printed-order
five-factor pentagon, and the complete sparse equality.  Characteristic
three proves why the replay should pass; it is not a substitute for the
replay.

## 5. Consequence and exact boundary

If task187 proves both equations in (2.1), then any independently accepted
raw task179 common word can be converted by (3.3)--(4.2) into a normalized,
exact-exponent first-rung common word.  In that event the full task186
augmented column search is unnecessary for this first edge.

Failure of either individual membership in (2.1) does **not** prove that
(N(\ker A)) is smaller: other word-bearing correction combinations may
still provide the missing residue.  Thus a negative task187 result only
closes this shortcut and sends the computation back to the full task186
search.

Nothing in this note proves the later abelian actual-class memberships or
the nonabelian accepted-set conditions.  The shortcut is first-rung only.

```text
U0/V0 NORMALIZATION FORMULA:                 PAPER_PROOF
TWO BOUNDARY PREIMAGES => N(ker A)=F3^2:     PAPER_PROOF
RAW POSITIVE => NORMALIZED POSITIVE:         PAPER_PROOF (conditional)
NORMALIZED POSITIVE => EXACT EXPONENT ZERO:  PAPER_PROOF (conditional)
U0 BOUNDARY PREIMAGE:                        NOT YET COMPUTED
V0 BOUNDARY PREIMAGE:                        NOT YET COMPUTED
TASK179 RAW COMMON WORD:                     NOT YET ACCEPTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:      NOT DECLARED
```

`R07_U0V0_BOUNDARY_NORMALIZATION_SHORTCUT_V161`
