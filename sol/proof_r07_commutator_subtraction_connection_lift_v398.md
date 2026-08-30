# R07 commutator-subtraction connection lift v398

Author: Sol / 2026-08-30

Status: paper theorem after v357, v369, v395, and v397.  It proves that the
same-depth Fox connection carried by an actual commutator instruction is not
an independent cokernel class once the corresponding value term has a legal
right lift through the **same actual occurrence operator**.  The connection
preimage is the literal commutator minus that value preimage.  No common
group-ring action, exchange of Fox factors, or relation-module equality is
used.  The actual R07 value lift, legality of the commutator instructions,
the initial A0 class, and strict all-depth coverage remain open.  Hence no
compatible R07 lift, fake certificate, or Ihara witness is declared.
`verified=false`.

## 1. Literal value and connection terms

Put \(k=\mathbf F_3\).  At one elementary-abelian relative layer, let

\[
 r_D:D_1\longrightarrow D_0,
 \qquad r_L:L_1\longrightarrow L_0,
 \qquad B_i:D_i\longrightarrow L_i                         \tag{1.1}
\]

be the physical reduction maps and actual eleven-occurrence leading
operators of v395.  All marking, boundary, exponent-zero, formation, and
hexagon conditions which are imposed before the pentagon solve are included
in \(D_i\).  Thus the actual relative legal source is

\[
 D_1^{\rm rel}:=\ker r_D,                                  \tag{1.2}
\]

and occurrencewise naturality gives

\[
 r_LB_1=B_0r_D,
 \qquad B_1(D_1^{\rm rel})\subseteq\ker r_L.               \tag{1.3}
\]

Let \(X_1\) be the free \(k\)-space on a registered finite roster of
literal, occurrence-tagged commutator instruction trees.  A basis tree
retains an actor word \(p\), a correction tree \(a\), every prefix and
inverse convention, and the printed aggregation order.  Evaluation gives

\[
 c_1:X_1\longrightarrow D_1.                              \tag{1.4}
\]

For one crossed Fox path \(\delta\), the exact identity is

\[
 \begin{aligned}
 \delta([p,a])
  &=(p-1)\delta(a)+\mathcal C(p,a),\\
 \mathcal C(p,a)
  &=(1-pap^{-1})\delta(p)+(1-[p,a])\delta(a).              \tag{1.5}
 \end{aligned}
\]

Indeed, expanding \(pap^{-1}a^{-1}\) by
\(\delta(uv)=\delta(u)+u\delta(v)\) and
\(\delta(u^{-1})=-u^{-1}\delta(u)\) gives

\[
 \delta([p,a])
 =\delta(p)+p\delta(a)-pap^{-1}\delta(p)-[p,a]\delta(a),  \tag{1.6}
\]

which is (1.5).  Apply the eleven literal occurrence transports and the
physical aggregation to (1.5), without identifying the occurrence actions.
This defines two \(k\)-linear maps

\[
 V_1,K_1:X_1\longrightarrow L_1                           \tag{1.7}
\]

such that

\[
 \boxed{B_1c_1=V_1+K_1.}                                  \tag{1.8}
\]

Here \(V_1\) is the transported \((p-1)\delta(a)\) value part and \(K_1\)
is the transported connection part.  For a nested commutator tree,
\(K_1\) means the complete iterated connection sum obtained by repeatedly
using (1.5); equation (1.8) is still a single literal identity for the
complete tree.  In particular, (1.8) does not replace
\((p-1)\delta(a)\) by \((a-1)\delta(p)\).

Restrict to the physically relative instruction source

\[
 X_1^{\rm rel}:=\{x\in X_1:c_1(x)\in D_1^{\rm rel}\}.      \tag{1.9}
\]

Legality in (1.9) is load-bearing.  It is not inferred merely from the
formal fact that one actor letter belongs to an endpoint kernel.

## 2. Connection subtraction at one edge

Put

\[
 \mathcal V_1:=V_1(X_1^{\rm rel}),
 \qquad \mathcal K_1:=K_1(X_1^{\rm rel}).                  \tag{2.1}
\]

### Theorem 2.1 (COMMUTATOR-SUBTRACTION LIFT)

Assume there is a word-bearing \(k\)-linear map

\[
 h_V:\mathcal V_1\longrightarrow D_1^{\rm rel}
 \qquad\text{with}\qquad
 B_1h_V=1_{\mathcal V_1}.                                 \tag{2.2}
\]

Define

\[
 \boxed{\eta_1:=c_1-h_VV_1:
 X_1^{\rm rel}\longrightarrow D_1^{\rm rel}.}            \tag{2.3}
\]

Then

\[
 \boxed{B_1\eta_1=K_1.}                                  \tag{2.4}
\]

Consequently

\[
 \boxed{\mathcal K_1\subseteq B_1(D_1^{\rm rel}).}       \tag{2.5}
\]

#### Proof

Both terms in (2.3) lie in \(D_1^{\rm rel}\), by (1.9) and (2.2).  Using
(1.8) and (2.2),

\[
 B_1\eta_1
 =B_1c_1-B_1h_VV_1
 =(V_1+K_1)-V_1=K_1.                                      \tag{2.6}
\]

This proves (2.4)--(2.5). \(\square\)

The theorem is deliberately occurrencewise.  It does not require
\(h_V\) to intertwine an abstract actor action, and it does not require
\(\eta_1\) to vanish on \(\ker K_1\).  To obtain a right inverse on the
connection target, choose a basis
\(\kappa_1,\ldots,\kappa_s\) of \(\mathcal K_1\), choose literal
\(x_j\in X_1^{\rm rel}\) with \(K_1x_j=\kappa_j\), and set

\[
 h_K\!\left(\sum_j a_j\kappa_j\right)
 :=\sum_j a_j\eta_1(x_j).                                 \tag{2.7}
\]

Then

\[
 h_K:\mathcal K_1\longrightarrow D_1^{\rm rel},
 \qquad B_1h_K=1_{\mathcal K_1}.                          \tag{2.8}
\]

This is exactly the pivoted-section principle of v397: target relations
need not lift to relations among source instructions.  Every selected
column in (2.7) retains the literal commutator ancestry and the ancestry of
its value correction.

### Corollary 2.2 (THE CONNECTION COKERNEL CLASS IS NOT INDEPENDENT)

For every \(x\in X_1^{\rm rel}\), in the cokernel of the actual relative
operator one has

\[
 \boxed{[K_1x]=-[V_1x]
 \quad\text{in}\quad L_1/B_1(D_1^{\rm rel}).}             \tag{2.9}
\]

Hence either both classes vanish or neither does.  In particular a
return-even connection vector may survive the abstract operator
\(1-\theta\), but it cannot create a *second* actual cokernel obstruction
after its paired value vector has been lifted through \(B_1\).

#### Proof

Equation (1.8) says \(V_1x+K_1x=B_1c_1x\), whose class in the displayed
cokernel is zero. \(\square\)

This corollary is also the exact limitation of the result.  A right inverse
for a value-only surrogate does not suffice.  Equation (2.2) must use the
same actual path-bearing \(B_1\) which occurs in (1.8).  Thus the theorem
does not silently promote the old endpoint dihedral calculation to the
physical A.18 operator.

## 3. Class-specific form

For one actual recursively generated instruction \(x\), a global map
\(h_V\) is unnecessary.  Suppose only that there is a legal relative,
word-bearing element \(d_V(x)\in D_1^{\rm rel}\) satisfying

\[
 B_1d_V(x)=V_1x.                                          \tag{3.1}
\]

Then

\[
 \boxed{d_K(x):=c_1x-d_V(x),
 \qquad B_1d_K(x)=K_1x.}                                 \tag{3.2}
\]

Thus, for the actual \(\chi_{07}\) history, the field-outer connection
gate can be discharged by attaching its literal commutator tree to the
actual value-lift certificate.  It need not be solved as an unrelated
full-module homotopy.  What still has to be shown is (3.1), together with
the legality assertion in (1.9), for the actual occurrence owner.

If the value term lies in the return-odd block and v75's
`DIH-A18-COMP` supplies its **actual** legal right lift, (3.2) immediately
supplies the paired return-even connection lift.  Pure return parity by
itself does not supply (3.1).

## 4. One construction on all refinements

Let

\[
 D^{\rm rel}=\varprojlim D_n^{\rm rel},
 \qquad L=\varprojlim L_n,
 \qquad X^{\rm rel}=\varprojlim X_n^{\rm rel}             \tag{4.1}
\]

be the completed registered objects, and let

\[
 c:X^{\rm rel}\to D^{\rm rel},
 \qquad B:D^{\rm rel}\to L,
 \qquad V,K:X^{\rm rel}\to L                             \tag{4.2}
\]

be the continuous reductions of the literal maps above.  Structural
reduction of instruction trees and occurrencewise naturality give

\[
 Bc=V+K.                                                   \tag{4.3}
\]

Assume here, as in v357, that the completed spaces are complete, separated,
linearly compact filtered \(k\)-spaces with finite-dimensional graded
pieces.  Whenever a strict section is invoked below, strictness refers to
these filtrations.

### Theorem 4.1 (COMPATIBLE CONNECTION LIFT FROM A VALUE LIFT)

Assume there is one continuous filtered word-bearing map

\[
 h_V:\mathcal V:=V(X^{\rm rel})\longrightarrow D^{\rm rel},
 \qquad Bh_V=1_{\mathcal V}.                              \tag{4.4}
\]

Then

\[
 \boxed{\eta:=c-h_VV,
 \qquad B\eta=K}                                          \tag{4.5}
\]

is a single compatible connection-lift instruction on every refinement.
For any one compatible actual instruction history \(x=(x_n)\), the family
\(\eta(x)\) is therefore a coherent correction of the entire connection
history \(Kx\); no stagewise choices are made.

If, in addition, \(\mathcal K:=K(X^{\rm rel})\) is closed and
\(K:X^{\rm rel}\twoheadrightarrow\mathcal K\) is strict, v357 Lemma 2.1
gives a continuous filtered \(k\)-linear section
\(s_K:\mathcal K\to X^{\rm rel}\).  Hence

\[
 \boxed{h_K:=\eta s_K:\mathcal K\longrightarrow D^{\rm rel},
 \qquad Bh_K=1_{\mathcal K}}                              \tag{4.6}
\]

is a continuous class-module connection homotopy.

#### Proof

Equation (4.5) is the same subtraction as (2.6), now in the complete
filtered spaces.  All maps commute with reduction, so its coordinates are
compatible.  Under the last hypotheses, the strict filtered section exists
by v357 Lemma 2.1, and
\(Bh_K=B\eta s_K=Ks_K=1_{\mathcal K}\). \(\square\)

The strictness clause is needed only to define a continuous right inverse
on every vector of the closed connection target.  It is not needed for one
named compatible history, where (4.5) already gives the correction.

Finally, changing the arithmetic base replaces \(B\) by \(B+T\), where
v357 proves that \(T\) raises filtration.  Once the actual leading value
and connection cover has been obtained for \(B\), the additive Neumann
repair transports that cover to \(B+T\).  No actor-equivariant section is
introduced by this step.

## 5. Effect on the R07 frontier

The connection term isolated in v393--v395 is real and occurs at the same
depth; it must not be discarded as a higher remainder.  The present theorem
changes how it is handled:

\[
 \boxed{
 \text{actual value lift}
 +\text{literal legal commutator}
 \Longrightarrow
 \text{paired connection lift}.}                          \tag{5.1}
\]

Therefore an independent field-outer/full-path homotopy is a sufficient
but unnecessarily strong target for the actual commutator-generated class.
The smaller certificate consists of:

1. the literal occurrence tree and replay of \(B c=V+K\);
2. proof that the tree evaluates in the physical relative legal source;
3. an actual, not endpoint-only, word-bearing preimage of \(V\); and
4. direct replay of the subtraction column \(c-h_V(V)\).

For a finite basis of connection vectors, add the pivot choices (2.7).  For
one compatible \(\chi_{07}\) history, no connection-basis computation is
required.

The updated logical boundary is:

```text
EXACT OCCURRENCEWISE FOX SPLIT Bc=V+K:             PAPER PROOF
CONNECTION COKERNEL CLASS = NEGATIVE VALUE CLASS:  PAPER PROOF
FINITE WORD-BEARING CONNECTION PREIMAGE FROM h_V: PAPER PROOF
ALL-DEPTH COMPATIBLE SUBTRACTION FROM ONE h_V:     PAPER PROOF
SEPARATE FULL-ACTOR CONNECTION HOMOTOPY REQUIRED:  NO FOR THE ACTUAL PAIRED CLASS
ACTUAL VALUE RIGHT LIFT THROUGH THE SAME B:        OPEN
LEGAL/RELATIVE COMMUTATOR INSTRUCTION ROSTER:      OPEN (A4 OWNER)
INITIAL ACTUAL DEFECT MEMBERSHIP:                  OPEN (A0 RUNNING)
STRICT ALL-DEPTH VALUE COVER / REDUCTION TYPING:   OPEN
COMPATIBLE R07 LIFT / FAKE / IHARA WITNESS:        NOT CONSTRUCTED
```

`R07_COMMUTATOR_SUBTRACTION_CONNECTION_LIFT_V398_PAPER_GRADE`
