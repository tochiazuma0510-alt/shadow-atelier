# R07 A0 full-boundary occurrence quotient (v400)

Author: Sol / 2026-08-30

Status: paper theorem and implementation refinement.  This note discharges
the safe-quotient hypothesis (4.2) of v396 for the canonical full PB3/PB4
relation boundaries.  It permits the compact A0 owner to reduce every one of
the eleven occurrence rows modulo one shared E3 or E4 boundary basis before
the correction invariant closure.  It does not report an executed closure,
a common word, a compatible lift, a fake, or an Ihara witness.

## 1. Local relation boundaries

For (m=3,4), let (Q_m) be the frozen marked quotient used by the all-seven
Fox evaluator, and put

\[
 C_m=\bigoplus_{a=1}^{\binom m2}\mathbf F_3[Q_m]e_a.
\tag{1.1}
\]

If (p_{m,j}) runs through the two registered PB3 presentation relators or
the eleven registered PB4 presentation relators, define

\[
 B_m=\operatorname{span}_{\mathbf F_3}
 \{q\,\delta(p_{m,j}):q\in Q_m,\ j\} \le C_m.
\tag{1.2}
\]

Thus (B_m) is exactly the exhausted marked-action boundary closure of
v396 Theorem 3.1, with no H1/H2/P tag attached.  In particular

\[
 qB_m=B_m\qquad(q\in Q_m).                              \tag{1.3}
\]

For an occurrence (o), let (m(o)\in\{3,4\}) be its type and let (C_o)
be a separately tagged copy of (C_{m(o)}).  Write (B_o\le C_o) for the
corresponding copy of (B_{m(o)}), and set

\[
 U=\bigoplus_o C_o,\qquad B=\bigoplus_o B_o.             \tag{1.4}
\]

The two normalized exponent coordinates of v399 are not included in (B).

## 2. The source actors preserve the local boundaries

V396's occurrence actor on (C_o) is left multiplication by the marked
quotient value of the conjugating source word, with the frozen occurrence
prefix already transported into the actor.  Equation (1.3) therefore gives

\[
 \rho(s)B=B\qquad(s\in F(x,y)).                          \tag{2.1}
\]

Consequently the four signed source actors descend to

\[
 \bar\rho(x^{\pm1}),\bar\rho(y^{\pm1})
 \quad\hbox{on}\quad U/B.                               \tag{2.2}
\]

Operationally, a row may be reduced occurrence by occurrence modulo (B_3)
or (B_4) after every actor application.  This computes the same class as
acting on the already reduced row; equality of chosen representatives is not
required.

## 3. The physical aggregation kills the quotient kernel modulo D

For every occurrence (o), the frozen physical aggregation has the form

\[
 L_{g,o}(v)=\varepsilon_o\,t_o v                         \tag{3.1}
\]

followed by insertion into its H1, H2, or P tagged physical block.  Here

- (arepsilon_o\in\{1,-1\}) is the registered factor sign; and
- (t_o\in Q_{m(o)}) is the registered prefix/occurrence translate for
  (g=g_{760}).

Let (D_{H_1},D_{H_2}) be the two tagged copies of (B_3), let (D_P) be
the tagged copy of (B_4), and put

\[
 D=D_{H_1}\oplus D_{H_2}\oplus D_P.                     \tag{3.2}
\]

By (1.3), signs and left translations preserve the relevant full relation
boundary.  Hence

\[
 L_{g,o}(B_o)\subseteq D_{\operatorname{block}(o)},
 \qquad\boxed{L_g(B)\subseteq D}.                        \tag{3.3}
\]

This is exactly the previously conditional gate (4.2) of v396, specialized
to the full canonical relation boundary.  It uses all eleven occurrence
tags; it does not assert a common action after physical aggregation.

## 4. Exact quotient selector

Let \(\widehat J\) be v399's occurrence map augmented by the normalized
exponent pair, and let \(\widehat W\) be the invariant span of the at-most-44
compact relator seeds.  Extend (B) by zero in the two normalized exponent
coordinates and denote quotient classes by a bar.  Let

\[
 \overline W=\operatorname{span}
 \{\bar\rho(a)\,\overline{\widehat J(r)}:
   r\in\mathcal R_{\rm pc},\ a\in F(x,y)\}.              \tag{4.1}
\]

### Theorem 4.1 (FULL-BOUNDARY OCCURRENCE QUOTIENT)

\[
 \boxed{
 -T\in D+L_g(\widehat W)
 \quad\Longleftrightarrow\quad
 -T+D\in\overline L_g(\overline W)\subseteq Z/D.}
\tag{4.2}
\]

Moreover, the right side is computed exactly by reducing every tagged E3
occurrence component modulo the one shared (B_3) echelon, every tagged E4
component modulo the one shared (B_4) echelon, leaving the two v399
coordinates untouched, and closing only the resulting quotient rows under
the four signed source actors.

#### Proof

Equation (2.1) makes the quotient source action well-defined, and (3.3)
makes the induced map to (Z/D) well-defined.  V396 Theorem 4.1 then gives

\[
 (D+L_g(\widehat W))/D=\overline L_g(\overline W).       \tag{4.3}
\]

Membership of the class of (-T) is precisely (4.2).  Direct-sum tagging
means reduction in (U/B) is the independent reduction of each occurrence
copy.  Since all E3 copies have the same full left-invariant boundary and
all E4 copies have the same one, two shared echelons compute those eleven
reductions exactly.  The normalized exponent summand is disjoint from (B)
and is therefore copied unchanged. \(\square\)

If (r) and \(\bar r\) are the unquotiented and quotiented correction ranks,
then

\[
 \bar r\le r,
 \qquad\text{attempts}\le44+4\bar r.                    \tag{4.4}
\]

No strict numerical reduction is claimed before execution, but the quotient
cannot enlarge the correction state.

## 5. Positive ancestry is not lost

The hot correction closure retains only compact seed/action/product ancestry
for its quotient pivots.  Suppose target reduction returns coefficients and
expands them to a literal correction (c\in\Omega).  Recompute the *full*,
unquotiented all-seven row (L_g\widehat J(c)) directly from that one word.
Equation (4.2) guarantees

\[
 R=-T-L_g\widehat J(c)\in D.                             \tag{5.1}
\]

Reduce (R) once against the three tagged physical boundary echelons while
retaining their seed/translation ancestry.  This yields the required typed
boundary preimage.  Thus local-boundary coefficients discarded during the
hot quotient closure never have to be stored: they are reconstructed from
the final residual only.

The v399 normalized coordinates still force

\[
 \epsilon(c)\in54\mathbf Z^2.                            \tag{5.2}
\]

After the registered (u_0,v_0) cube repair, direct replay must again check
integer exponent pair ((0,0)), joint-kernel identity, unchanged physical
class modulo (D), and (5.1).  Boundary ancestry is never multiplied into
the source correction word.

On a negative terminal, exact exhaustion in the quotient is conclusive by
the reverse implication of (4.2).  A resource stop before either local
boundary or quotient correction exhaustion remains `UNKNOWN_RESOURCE`.

## 6. Minimal implementation contract

1. Build (B_3) and (B_4) once from the 2 and 11 Fox seeds and all signed
   marked actions.  The physical H1/H2/P bases are tagged views of these two
   completed bases.
2. Directly replay each compact seed before quotienting it.
3. Reduce each occurrence tag against the shared basis of its E3/E4 type,
   then insert the quotient row with its two normalized coordinates.
4. After every one of the four source actions, quotient-reduce before the
   central insertion.
5. Retain only quotient correction DAG ancestry during the hot loop.  On
   MEMBER, expand once, replay the full word, and solve (5.1) for the typed
   boundary preimage.
6. An independent checker rebuilds both shared boundaries, the quotient
   closure, and the final unquotiented residual.  NONMEMBER requires an exact
   quotient separator or an independently identical exhausted remainder.

This change removes no acceptance gate and adds no preliminary search.  It
uses the already necessary full boundary closure as a lossless quotient for
the more expensive correction closure.

```text
FULL LOCAL B3/B4 BOUNDARY INVARIANCE:        PAPER PROOF
L_g(B) subset D FOR ALL 11 OCCURRENCES:      PAPER PROOF
44-SEED CORRECTION CLOSURE MODULO B:         EXACT FINITE REPLACEMENT
HOT LOCAL-BOUNDARY ANCESTRY STORAGE:         NOT REQUIRED
FINAL FULL WORD + TYPED PREIMAGE REPLAY:     REQUIRED
ACTUAL A0 MEMBER/NONMEMBER:                  NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:              NONE
```

`R07_A0_FULL_BOUNDARY_OCCURRENCE_QUOTIENT_V400_PAPER_GRADE`
