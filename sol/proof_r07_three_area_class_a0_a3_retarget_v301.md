# R07 three-area-class A0/A3 retarget theorem (v301)

## 0. Scope

The current schedule first constructs one A0 common correction, specializes
it through A2, and only then runs the v216 exponent-nine A3 pre-gate.  A
failure there would reject the named correction but would say nothing about
other A0 common corrections.  This note removes that blind choice.

The roof kernel has only three possible images in the first non-roof
class-two quotient.  The A3 occurrence seed is fixed by \(g_{760}\), and the
corrected residual target depends on an A0 correction only through this one
three-valued image.  Consequently the complete projected A3 pre-gate can be
run for all three area classes before an A0 word is selected.  A0 can then
add one scalar row and construct a common word directly in a passing class.

This is a paper theorem.  The three actual targets have not been evaluated,
the augmented A0 search has not been implemented, and no pointed multiplier,
lift, fake, or Ihara witness is claimed.

## 1. The only exponent-nine freedom of a roof correction

Let

\[
 F=F(x,y)\twoheadrightarrow\Delta _0,
 \qquad H_0=\ker(F\to\Delta _0),
\tag{1.1}
\]

and let \(\Omega\leq H_0\) be the registered joint correction domain used by
A0.  Every literal A0 correction word \(a\) belongs to \(\Omega\), hence to
\(H_0\).

Write

\[
 D_1=\mathcal H_2(9),\qquad h=[x,y],\qquad z=h^3.
\tag{1.2}
\]

V210--v211 prove

\[
 \phi_9(H_0)=\langle z\rangle\cong C_3
\tag{1.3}
\]

and give the conjugation-invariant homomorphism

\[
 \omega:H_0\longrightarrow\mathbf F_3,
 \qquad \phi_9(a)=z^{\omega(a)}.
\tag{1.4}
\]

Thus every A0 correction has exactly one **area class**
\(t=\omega(a)\in\{0,1,2\}\).  This scalar is computed from the authenticated
class-two signed-area coordinate of the literal word; no PB4 enumeration is
required.  Products add the scalar and inversion negates it.

## 2. The A0 equation with one extra scalar row

Retain v140's additive raw-defect map

\[
 \mathscr V:\Omega\longrightarrow Z,
\tag{2.1}
\]

the complete boundary subspace \(D\leq Z\), and the fixed base target
\(T\in Z\).  An A0 correction is a solution precisely when

\[
 -T\in D+\mathscr V(\Omega).
\tag{2.2}
\]

Define the augmented homomorphism

\[
 \mathscr V^\omega(a)=(\mathscr V(a),\omega(a))
 \in Z\oplus\mathbf F_3
\tag{2.3}
\]

and give every boundary column scalar coordinate zero.

### Theorem 2.1 (AREA-TARGETED COMMON WORD)

For \(t\in\mathbf F_3\), there is a registered A0 common correction of area
\(t\) if and only if

\[
 \boxed{
 (-T,t)\in(D\oplus0)+\mathscr V^\omega(\Omega).}
\tag{2.4}
\]

A coefficient-bearing positive certificate for (2.4) constructs the same
literal product as v140, and its area is exactly \(t\).

#### Proof

If \(a\) is a common correction, (2.2) holds and the last coordinate of
\(\mathscr V^\omega(a)\) is \(\omega(a)\), giving (2.4).  Conversely, a
finite linear certificate for (2.4) consists of boundary columns and literal
normal-conjugate correction columns.  Multiply the latter in retained order,
using the inverse word for coefficient two, exactly as in v140 Theorem 2.1.
Additivity of \(\mathscr V\) gives the common-word equality, while the
homomorphism law (1.4) gives the last coordinate \(t\).  Boundary columns
contribute no source word and therefore no area.  QED.

The attainable set

\[
 T_{\rm att}=\{t:(-T,t)\text{ satisfies (2.4)}\}
\tag{2.5}
\]

is either empty, a singleton, or all of \(\mathbf F_3\).  Indeed, after one
solution is chosen, differences of solutions form a vector space and their
area values form a subspace of the one-dimensional target.  It is safe and
simpler operationally to test all three targets.

The v139/v140 positive-only column generator applies without change after
appending the scalar to each correction row.  An ACTIVE column is still
proved active by one nonzero dual pairing.  A bounded failure remains
`UNKNOWN_RESOURCE`.

## 3. The three corrected exponent-nine targets

Put \(g_0=g_{760}\).  For each of the eleven frozen task198 occurrences let

\[
 r_o=\overline{\rho_o(g_0)},\qquad
 z_o=q_o(z)
\tag{3.1}
\]

in the corresponding exponent-nine PB3/PB4 quotient.  If
\(a\in H_0\) has area \(t\), then (1.4) and the common-source factorization
give

\[
 \boxed{
 \overline{\rho_o(g_0a)}=r_oz_o^t
 \quad(1\leq o\leq11).}
\tag{3.2}
\]

Use the frozen task198 factor signs, inverse slots, occurrence order and
printed H1/H2/P constructors on the eleven values in (3.2).  Denote the
resulting three relation values by \(R_B(t)\), and put

\[
 \epsilon_B(t)=1-R_B(t),
 \qquad
 \bar\epsilon(t)=(\epsilon_{H1}(t),
                  \epsilon_{H2}(t),\epsilon_P(t)).
\tag{3.3}
\]

### Lemma 3.1 (AREA-CLASS CONSTANCY)

If \(a,a'\in H_0\) have \(\omega(a)=\omega(a')=t\), then their corrected
words \(g_0a,g_0a'\) have the same complete exponent-nine residual target:

\[
 \boxed{
 \bar\epsilon(g_0a)=\bar\epsilon(g_0a')=\bar\epsilon(t).}
\tag{3.4}
\]

#### Proof

Equation (1.4) gives equal images of \(a,a'\) in \(D_1\).  Every occurrence
map factors through \(D_1\), so (3.2) gives equal typed occurrence values.
The printed block constructors are deterministic products and inverses of
exactly those values.  Their three group-algebra endpoints are therefore
equal, proving (3.4).  QED.

No claim of exact PB equality is made here.  Lemma 3.1 concerns only the
matching exponent-nine quotient used by the v216 necessary pre-gate.

## 4. One closure, three membership tests

V225 defines the occurrence vector \(w\) from \(g_0\), not from the corrected
word.  Hence

\[
 u_0=(z-1)\mathbin\odot w,
 \qquad
 U_0=\operatorname{OrbSpan}_{x^{\pm1},y^{\pm1}}(u_0)
     =I(\langle z\rangle)\mathbin\odot w
\tag{4.1}
\]

are identical for every A0 correction.  Construct the occurrence closure
once and define

\[
 T_{\rm gate}=\{t\in\mathbf F_3:
      \bar\epsilon(t)\in C(U_0)\}.
\tag{4.2}
\]

### Theorem 4.1 (THREE-CLASS COMPLETE A3 PRE-GATE)

For every A0 common correction \(a\),

\[
 \boxed{
 \text{the v216 projected A3 pre-gate passes for }g_0a
 \iff \omega(a)\in T_{\rm gate}.}
\tag{4.3}
\]

The complete set \(T_{\rm gate}\) is obtained from one rank-at-most-486
occurrence closure and exactly three block-image membership tests.  A
nonmember class carries its own separating dual; a member class carries
coefficient ancestry in the same fixed closure.

#### Proof

V216 identifies the complete projected repair image with \(C(U_0)\).  The
space is independent of \(a\) by (4.1), while Lemma 3.1 identifies the target
with \(\bar\epsilon(\omega(a))\).  Substitution gives (4.3).  The closure
rank and the producer/checker completeness arguments are v216 Theorem 3.1.
Only the three targets vary.  QED.

## 5. Retargeted production schedule

The correct witness-first order is now:

1. from accepted task198 and the frozen \(g_{760}\), construct \(w,U_0\);
2. construct \(\bar\epsilon(0),\bar\epsilon(1),\bar\epsilon(2)\) by literal
   typed replay and compute \(T_{\rm gate}\);
3. append \(\omega\) to every A0 correction column and zero to every boundary
   column;
4. run the positive-only A0 solver only for
   \(t\in T_{\rm gate}\), or share one basis while checking those augmented
   targets in frozen order;
5. independently replay the returned literal word, its raw A0 equality and
   its area \(t\); and
6. feed it through the v300 A2 decoder and require equality with the already
   computed class-\(t\) A3 package before entering the pointed A4/A5 gate.

This avoids accepting an arbitrary first A0 word and discovering only later
that its area class was projected-nonmember.  It does not guarantee that an
area-targeted A0 word exists.  The exact outcome is the finite intersection

\[
 \boxed{T_{\rm att}\cap T_{\rm gate}.}
\tag{5.1}
\]

If (5.1) is empty after complete, independently checked calculations, no
registered A0 common correction can pass this necessary exponent-nine gate
for \(g_{760}\).  That is an obstruction to this fixed branch, not a fake or
Ihara conclusion.  If it is nonempty, the selected word is guaranteed to
pass A3's projected pre-gate, but the pointed joint gate, three exact PB
endpoints, nonlinear Neumann side conditions, mixed-prime and perfect-core
gates remain open.

## 6. Certificate and implementation boundary

The producer records for each \(t\): the eleven values (3.2), three printed
block products, \(\bar\epsilon(t)\), the shared closure identity, and either
membership ancestry or a separating dual.  The independent checker uses
v216's canonical 486-row construction rather than the producer's one-seed
queue.

Every augmented A0 correction record carries the literal word, its directly
computed signed area and the extra scalar row.  Required mutations include
the commutator convention, division of the central exponent by three,
coefficient-two sign, right-multiplication order in (3.2), one occurrence
map, one inverse slot, one printed factor order, the area target, and the
extra A0 row.  No supplied `area_class` Boolean is authoritative.

```text
ROOF CORRECTION EXPONENT-NINE CLASSES:       EXACTLY 3
A0 AREA-TARGET AUGMENTATION:                 PAPER PROOF
A3 TARGET CONSTANT ON EACH AREA CLASS:       PAPER PROOF
COMPLETE A3 PRE-GATE FOR ALL A0 WORDS:       1 CLOSURE + 3 TARGET TESTS
ARBITRARY FIRST A0 WORD BEFORE A3:           NO LONGER REQUIRED
ACTUAL THREE TARGETS / MEMBERSHIPS:           NOT COMPUTED
AUGMENTED A0 IMPLEMENTATION / ACCEPTED WORD: NOT IMPLEMENTED / 0
POINTED GATE / EXACT ENDPOINT / LIFT:         OPEN
FAKE / IHARA:                                NONE
```

`R07_THREE_AREA_CLASS_A0_A3_RETARGET_V301_PAPER_GRADE`
