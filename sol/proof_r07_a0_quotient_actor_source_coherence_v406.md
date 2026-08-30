# R07 A0 quotient-actor and source-coherence lemma (v406)

Author: Sol / 2026-08-30

Status: paper implementation lemma for v401--v405.  It fixes the exact
per-occurrence actor, sparse sections, echelon sign, and positive source
contract needed by the fresh A0 owner.  It is not an executed A0 result and
does not assert a common word, compatible lift, fake, or Ihara witness.
`verified=false`.

## 1. Canonical sparse sections

For PB3, let `enc` be the frozen byte serialization and choose

\[
 T_3=\{\min_{\rm enc}\{h,hz,hz^2\}:h\in H_3\}.
\tag{1.1}
\]

Thus every element is written uniquely as \(rz^j\), with \(r\in T_3\) and
\(j\in\{0,1,2\}\).  For PB4 use the independently cross-checked split

\[
 H_4=H_0\times\langle z\rangle,
 \qquad h=h_0z^{\kappa(h)},\quad h_0\in H_0.
\tag{1.2}
\]

These are deliberately different transversals.  The first PC coordinate is
used only in (1.2).

Write either central normal form as

\[
 ((S_i(r))_i,U_0(r),U_1(r))_r\oplus\tau,
\tag{1.3}
\]

where there are two noncentral coordinates for PB3 and five for PB4.  A
fixed sparse section \(\iota_m\) is as follows.

- Lift \(S_i(r)\) to the noncentral coordinate \((i,r)\).
- Lift \(U_0(r)\) and \(U_1(r)\) to the central coordinates \((r,0)\) and
  \((r,1)\), respectively, leaving the \((r,2)\) coordinate zero.
- Lift \(\tau=1\) to the constant central vector on the identity central
  orbit.  For PB3 that orbit is written with its representative from
  (1.1); for PB4 it is \(\{1,z,z^2\}\).

The triangular formula of v401 or v402 applied to these lifts returns the
original normal coordinates.  Hence

\[
 Q_m\iota_m=\operatorname{id}.
\tag{1.4}
\]

In particular, lifting `tau` to only one point is forbidden: a constant
three-point vector has zero coordinate sum in characteristic three but has
the retained \(\tau\)-coordinate one.

## 2. The exact actor is occurrence-dependent

For occurrence \(o\), let \(P_o\) be its already frozen signed-factor Fox
prefix, and let \(s_o:F(x,y)\to PB_{m(o)}\) be its literal substitution
(including the PB3 embedding when prescribed).  For
\(a\in\{x,x^{-1},y,y^{-1}\}\), set

\[
 w_o(a)=P_o\,\overline{s_o(a)}\,P_o^{-1}.
\tag{2.1}
\]

The action on the normal coordinates of this occurrence is

\[
 \boxed{\bar\rho_o(a)=Q_oL_{w_o(a)}\iota_o.}
\tag{2.2}
\]

Equation (2.2) is implemented by a sparse section, one left translation,
and the same contraction again.  It must not be replaced by
\(Q_oL_{\bar a}\), nor by one action shared among the eleven occurrences.

### Lemma 2.1 (well-defined quotient actor)

Equation (2.2) is the action induced by the literal source conjugation and
is independent of the chosen section.

#### Proof

The literal Fox formula for a conjugated kernel word gives left
multiplication by \(\overline{s_o(a)}\) before the surrounding occurrence
prefix.  Moving that multiplication through the prefix gives (2.1).  The
kernel of \(Q_o\) is the full PB3 boundary for a PB3 occurrence and the five
central families for a PB4 occurrence.  In both cases it is a full
left-translation span, hence is invariant under \(L_{w_o(a)}\).  If two
sections differ by a kernel row, their images under (2.2) therefore agree.
\(\square\)

The normalized exponent pair \((\epsilon_x/18,\epsilon_y/18)\bmod3\) is
copied unchanged.  Conjugation does not alter the integer exponent pair.

## 3. Echelon normalization must carry the literal source

Suppose an occurrence candidate \(v\) has literal kernel word \(c\), and
the current normalized pivots \(p_i\) have literal words \(c_i\).  If sparse
insertion uses coefficients \(d_i\) and pivot normalization \(s\in\{1,2\}\),
then the stored row is

\[
 p=s\left(v-\sum_i d_ip_i\right).
\tag{3.1}
\]

Put \(\operatorname{sc}_1(w)=w\) and
\(\operatorname{sc}_2(w)=w^{-1}\).  Its source DAG must encode, in one fixed
order,

\[
 c_p=\operatorname{sc}_s\left(
       c\prod_i\operatorname{sc}_{(-d_i)\bmod3}(c_i)\right),
\tag{3.2}
\]

where zero-coefficient factors are omitted and a coefficient two is
represented by inverse, not by a trusted scalar label.  Since every factor
lies in the joint kernel, its Fox occurrence map is additive on products and
changes sign on inverses.  Thus

\[
 \widehat J(c_p)=p.
\tag{3.3}
\]

Let \(\bar L\) denote the fixed operation that forgets occurrence tags and
adds them into their two PB3 and one PB4 physical blocks, retaining the
normalized exponent pair.  The physical row attached to the new pivot is
therefore

\[
 \boxed{\bar L(p),}
\tag{3.4}
\]

not \(\bar L(v)\).  Using the unreduced candidate in (3.4) while labelling it
by the pivot source breaks (3.3) and makes a later positive replay unsound.
Physical dependence of \(\bar L(p)\) does not suppress the four descendants
of \(p\); the invariant queue is controlled only by occurrence rank.

## 4. Positive coefficient convention

Use the task413 reducer convention.  If a physical target reduction reaches
zero, its returned source coefficients \(e_j\) satisfy

\[
 \boxed{T_{\rm neg}+\sum_j e_jR_j=0,}
\tag{4.1}
\]

where `target_row` is the negative uncorrected Fox defect.  Correction-pivot
sources are expanded through (3.2); selected PB4 action sources remain typed
boundary rows.  Consequently the correction word \(c_*\) is assembled with
the coefficients \(e_j\) themselves, with coefficient two meaning inverse.
There is no additional global sign reversal.

After v399 exactification, let \(c_{\rm exact}\) have integer exponent pair
zero.  A production positive terminal must freshly establish

1. \(c_{\rm exact}\) is identity in every joint state;
2. its eleven unquotiented Fox occurrences contract to the selected
   correction source sum;
3. every selected translate of each of the six PB4 action rows is replayed;
4. equation (4.1) is zero in both PB3 normal blocks, the PB4 noncentral and
   central-survivor coordinates, and the normalized exponent pair.

By v401 and v402, the kernel discarded by the three normal maps is exactly
the two PB3 boundaries plus the five central PB4 families.  By v404, the
selected six action rows lie in, and exhaust when needed, the remaining
PB4 boundary.  Therefore these four gates prove the original A0 membership
without reconstructing the eliminated large boundary bases or their
preimages.

```text
PB3 TRANSVERSAL:                 LEAST SERIALIZED CENTRAL-ORBIT REP
PB4 TRANSVERSAL:                 H0 VIA AUTHENTICATED KAPPA
OCCURRENCE ACTOR:                Q_o L_(P_o s_o(a) P_o^-1) IOTA_o
PHYSICAL SOURCE ROW:             AGGREGATE THE STORED NORMALIZED PIVOT
POSITIVE SIGN:                   TARGET + CORRECTION + ACTIONS = 0
ELIMINATED BOUNDARY PREIMAGE:     NOT REQUIRED
ACTUAL A0 TERMINAL:              NOT YET EXECUTED
```

`R07_A0_QUOTIENT_ACTOR_SOURCE_COHERENCE_V406_PAPER_GRADE`
