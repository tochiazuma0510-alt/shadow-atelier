# R07 A0 normalized exponent-lattice repair v399

Author: Sol / 2026-08-30

Status: paper correction.  This note supersedes v398's use of the *raw*
exponent pair modulo three.  V156 proves that raw pair is identically zero on
the joint kernel.  The correct two-coordinate augmentation divides by the
canonical kernel lattice basis \(18e_x,18e_y\) before reduction modulo three.
V396's invariant closure and v397's at-most-44 seed bound remain valid with
this normalized augmentation.  No executed A0 closure, COMMON, lift, fake, or
Ihara witness is declared.

## 1. Why raw reduction is wrong

Let

\[
 \Omega=\ker(F(x,y)\twoheadrightarrow G_{\rm joint}),
 \qquad
 \epsilon:F(x,y)\to\mathbf Z^2.                           \tag{1.1}
\]

V156 Theorem 3.1 proves the exact lattice identity

\[
 \boxed{\epsilon(\Omega)=18\mathbf Z^2.}                  \tag{1.2}
\]

Consequently

\[
 \epsilon(c)\bmod3=(0,0)\qquad(c\in\Omega).              \tag{1.3}
\]

Thus v398's raw augmentation is mathematically harmless but vacuous: it
cannot distinguish a kernel correction of exponent \((18,0)\), which is not
zero-cost cube-repairable, from one of exponent \((54,0)\), which is.

## 2. Correct normalized occurrence source

Define the homomorphism

\[
 \nu:\Omega\longrightarrow\mathbf F_3^2,
 \qquad
 \nu(c)=\left(\frac{\epsilon_x(c)}{18},
               \frac{\epsilon_y(c)}{18}\right)\bmod3.    \tag{2.1}
\]

The divisions are exact by (1.2).  Put

\[
 \widehat U=
 \left(\bigoplus_{o\in\mathcal O}C_o\right)\oplus\mathbf F_3^2,
 \qquad
 \widehat J(c)=\bigl(J_{\rm occ}(c),\nu(c)\bigr).         \tag{2.2}
\]

Extend the occurrence-dependent source actor by the identity:

\[
 \widehat\rho(s)=\rho_{\rm occ}(s)\oplus
 \operatorname{id}_{\mathbf F_3^2}.                       \tag{2.3}
\]

### Lemma 2.1 (NORMALIZED CONJUGATION LAW)

For \(c,d\in\Omega\) and \(s\in F(x,y)\),

\[
 \widehat J(cd)=\widehat J(c)+\widehat J(d),
 \qquad
 \boxed{\widehat J(scs^{-1})=
        \widehat\rho(s)\widehat J(c).}                   \tag{2.4}
\]

#### Proof

The occurrence coordinates obey v396.  The normalized lattice coordinate is
additive on \(\Omega\), and conjugation preserves the integer exponent pair:

\[
 \epsilon(scs^{-1})=\epsilon(c).                          \tag{2.5}
\]

Division by 18 and reduction modulo three give the identity action in
(2.3). \(\square\)

Let \(\widehat W\) be the least subspace containing the presentation seeds
and invariant under the four signed source actions.  V396's normal-closure
proof applied to (2.4) gives

\[
 \boxed{\widehat J(\Omega)=\widehat W.}                  \tag{2.6}
\]

Because the v397 compact roster and the 6,441 roster have the same normal
closure, either roster generates the same \(\widehat W\).  Therefore the
compact insertion bound is still

\[
 \boxed{44+4\dim\widehat W}.                              \tag{2.7}
\]

## 3. Exact A0 membership and cube repair

Let

\[
 \widehat L_g(u,a)=\bigl(L_g(u),a\bigr)                  \tag{3.1}
\]

carry the normalized pair unchanged into the physical target.  All PB3/PB4
boundary rows have normalized coordinate zero, and the registered
\(g_{760}\) target has exact exponent pair \((0,0)\).  Hence the corrected
finite test is

\[
 \boxed{-T\in D+\widehat L_g(\widehat W).}                \tag{3.2}
\]

A MEMBER ancestry \(c_*\) therefore satisfies

\[
 \nu(c_*)=0,
 \qquad
 \epsilon(c_*)=(54A,54B)                                 \tag{3.3}
\]

for unique integers \(A,B\).  Let the registered v156 exactifying words be

\[
 v_0=r_9r_{12}r_3^{-2},\qquad
 u_0=r_9v_0^{-8},                                         \tag{3.4}
\]

where \(r_3,r_9,r_{12}\) are the authenticated lifted \(Q_0\)-defect words.
Their exact exponent vectors are

\[
 \epsilon(v_0)=(0,18),
 \qquad
 \epsilon(u_0)=(18,0).                                   \tag{3.5}
\]

Define

\[
 h=u_0^{-3A}v_0^{-3B},
 \qquad c_{\rm exact}=c_*h.                               \tag{3.6}
\]

Then \(\epsilon(c_{\rm exact})=(0,0)\).  Since \(h\) is a product of cubes
of kernel words, its characteristic-three all-seven change is zero; thus
\(c_{\rm exact}\) has the same physical class as \(c_*\).  This is exactly
v156 Theorem 5.1.

## 4. Mandatory task411 gates

The task411 producer and helper-nonshared checker must enforce:

1. every compact seed evaluates in \(\Omega\), has both integer exponent
   sums divisible by 18, and receives the pair (2.1);
2. the four actions copy the normalized pair unchanged;
3. every boundary row and the target receive normalized pair zero;
4. target MEMBER is solved in the combined physical-plus-normalized system,
   with correction and boundary coefficient ancestry retained;
5. the selected literal \(c_*\) is replayed and its normalized pair is zero;
6. \(r_3,r_9,r_{12}\), \(u_0,v_0,h\), and \(c_{\rm exact}\) are reconstructed
   from authenticated source words, not trusted receipt booleans;
7. \(c_{\rm exact}\) has exact integer exponent pair \((0,0)\), lies in
   \(\Omega\), and satisfies the direct all-seven equality with the emitted
   typed boundary preimage.

The frozen task179 raw `exponent_key` rows may be replayed as canaries, but
they cannot serve as gates because (1.3) makes them zero on every correction
column.

```text
V398 RAW exp mod 3 AUGMENTATION:       SUPERSEDED / VACUOUS ON OMEGA
CORRECT NORMALIZED ROWS:               (exp/18) mod 3
V396 INVARIANT-SPAN THEOREM:           RETAINED WITH J -> J_HAT
V397 <=44 SEED REDUCTION:              RETAINED
MEMBER -> 54 Z^2 CUBE REPAIR:          PAPER PROOF v156/v399
ACTUAL A0 COMMON + DIRECT CHECKER:      NOT YET EXECUTED
```

`R07_A0_NORMALIZED_EXPONENT_LATTICE_REPAIR_V399_PAPER_GRADE`
