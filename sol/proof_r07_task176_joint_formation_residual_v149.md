# R07 task176 joint formation residual v149

Author: Sol / 2026-08-27

Status: paper theorem and bounded materialization contract. The
cross-checked task157ee/task176 extension data determine the
\(PSL(2,8)\)-formation residual of the coarse joint context group. This
closes the coarse residual input required by v147--v148. It does not compute
the residual intersection in task179's much larger first relation module and
does not declare a cofinal lift, fake, or Ihara witness.

## 1. Frozen joint extension

Let \(S=PSL(2,8)\). The task157ee presentation and task176 reconstruction
give the marked joint image \(G\) in the source E3 and registered E4
contexts, with an exact sequence

\[
 1\longrightarrow \Gamma\longrightarrow G
 \stackrel{\pi}{\longrightarrow}Q_0\longrightarrow1,
 \qquad |\Gamma|=3^5,
\tag{1.1}
\]

and a direct-factor decomposition

\[
 Q_0=S\times G_9,
 \qquad |S|=504,
 \qquad |G_9|=2916.
\tag{1.2}
\]

Here \(G_9\cong C_9^3\rtimes V_4\) is solvable. The independently replayed
invariants of \(\Gamma\) include

\[
 |\Phi(\Gamma)|=27,
 \qquad |\Gamma/\Phi(\Gamma)|=9.
\tag{1.3}
\]

Thus the Frattini quotient of \(\Gamma\) is a two-dimensional
\(\mathbf F_3\)-space. The load-bearing execution record for the complete
joint presentation is task157ef GHA run `32359956713`, receipt
`2166036 / 1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df`.
Task176 independently reconstructed the same extension data in production
run `33044121344`.

## 2. A p-group extension over the PSL factor splits canonically

Put

\[
 E=\pi^{-1}(S\times1).
\tag{2.1}
\]

Then

\[
 1\longrightarrow\Gamma\longrightarrow E
 \longrightarrow S\longrightarrow1.
\tag{2.2}
\]

### Lemma 2.1 (TRIVIAL OUTER ACTION)

The outer action

\[
 S\longrightarrow\operatorname{Out}(\Gamma)
\tag{2.3}
\]

is trivial.

#### Proof

The induced action on the characteristic Frattini quotient gives a
homomorphism

\[
 S\longrightarrow
 \operatorname{Aut}(\Gamma/\Phi(\Gamma))
 \cong GL_2(3).
\tag{2.4}
\]

The group \(S\) is simple, while

\[
 |GL_2(3)|=(3^2-1)(3^2-3)=48<504.
\tag{2.5}
\]

Hence (2.4) cannot be injective and is trivial. The kernel of
\(\operatorname{Aut}(\Gamma)\to
\operatorname{Aut}(\Gamma/\Phi(\Gamma))\) is a 3-group by the Burnside
basis theorem. Its image in \(\operatorname{Out}(\Gamma)\) is therefore a
3-group. The image of (2.3) lies in this 3-group. Simplicity of \(S\)
again forces that image to be trivial. \(\square\)

### Theorem 2.2 (CANONICAL PSL COMPLEMENT)

There is a unique subgroup \(\widetilde S\leq E\) such that

\[
 E=\Gamma\times\widetilde S,
 \qquad \widetilde S\cong S.
\tag{2.6}
\]

It is intrinsic:

\[
 \boxed{
 \widetilde S
 =C_E(\Gamma)'
 =E^{(\infty)}.}
\tag{2.7}
\]

Here \(E^{(\infty)}\) is the stable term of the derived series.

#### Proof

Lemma 2.1 says that every lift in \(E\) acts on \(\Gamma\) by an inner
automorphism. Therefore

\[
 E=\Gamma C_E(\Gamma).
\tag{2.8}
\]

Moreover

\[
 C_E(\Gamma)\cap\Gamma=Z(\Gamma),
\tag{2.9}
\]

so restriction of (2.2) gives a central extension

\[
 1\to Z(\Gamma)\to C_E(\Gamma)\to S\to1.
\tag{2.10}
\]

The group \(S\) is perfect and has trivial Schur multiplier. The universal
coefficient sequence therefore gives

\[
 H^2(S,Z(\Gamma))=0
\tag{2.11}
\]

for the trivial action in (2.10). Thus (2.10) splits. Since

\[
 H^1(S,Z(\Gamma))=\operatorname{Hom}(S,Z(\Gamma))=0,
\tag{2.12}
\]

the complement is unique. Call it \(\widetilde S\). It centralizes
\(\Gamma\), has trivial intersection with \(\Gamma\), and (2.8) proves
(2.6).

Now

\[
 C_E(\Gamma)=Z(\Gamma)\times\widetilde S,
\tag{2.13}
\]

so its derived subgroup is \(\widetilde S\). Since \(\Gamma\) is solvable
and \(\widetilde S\) is perfect, the derived series of
\(E=\Gamma\times\widetilde S\) stabilizes at \(\widetilde S\). This proves
(2.7). \(\square\)

The uniqueness in Theorem 2.2 is important: no section choice or conjugacy
normalization is hidden in the formation residual below.

## 3. Exact formation residual of G

Let \(R_S(-)\) denote the residual for the formation of finite groups having
no composition factor isomorphic to \(S\).

### Theorem 3.1 (TASK176 JOINT RESIDUAL)

For the group \(G\) in (1.1),

\[
 \boxed{R_S(G)=\widetilde S.}
\tag{3.1}
\]

In particular,

\[
 \boxed{R_S(G)\cap\Gamma=1,}
 \qquad
 \pi:R_S(G)\xrightarrow{\sim}S\times1.
\tag{3.2}
\]

#### Proof

The subgroup \(E\) is normal in \(G\), because \(S\times1\) is a direct
factor of \(Q_0\). Equation (2.7) makes \(\widetilde S\) characteristic in
\(E\), hence normal in \(G\).

Quotienting (1.1) by \(\widetilde S\) gives an extension

\[
 1\to\Gamma\to G/\widetilde S\to G_9\to1.
\tag{3.3}
\]

Both kernel and quotient are solvable, so \(G/\widetilde S\) belongs to the
no-\(S\) formation. Hence

\[
 R_S(G)\leq\widetilde S.
\tag{3.4}
\]

Conversely, let \(N\triangleleft G\) with \(G/N\) having no \(S\)
composition factor. The image of the simple normal subgroup
\(\widetilde S\) in \(G/N\) is either trivial or isomorphic to \(S\). The
latter is forbidden, so \(\widetilde S\leq N\). Intersecting over all such
\(N\) gives the reverse inclusion in (3.4). Equations (2.6) and (1.2) then
give (3.2). \(\square\)

## 4. Consequence for the formation-purified explicit lift

Task179 uses the same marked joint value group \(G\) as its level-zero source
gate: every registered normal-generator correction has identity value in
\(G\). Let \(a_0,b_0\in G\) be, respectively, the arithmetic reference and
the chosen R07 coarse component, and put

\[
 \delta_0=a_0^{-1}b_0.
\tag{4.1}
\]

V147's coarse formation condition is now the literal test

\[
 \boxed{
 \delta_0\in\widetilde S=C_E(\Gamma)'=E^{(\infty)}.}
\tag{4.2}
\]

Because every task179 correction lies in the joint value kernel, it cannot
change (4.2). Thus (4.2) is a prerequisite, not another task179 search
coordinate. If it fails, no correction which is invisible in every no-\(S\)
quotient can repair this coarse base. If it passes, the first-rung residual
still has to be computed in the extension

\[
 1\to V\to\mathcal H_1\to G\to1.
\tag{4.3}
\]

Theorem 3.1 supplies its exact coarse target:

\[
 p(R_S(\mathcal H_1))=\widetilde S.
\tag{4.4}
\]

It does **not** imply

\[
 V\cap R_S(\mathcal H_1)=0.
\tag{4.5}
\]

The large \(V\) in (4.3) is task179's joint first relation module, not the
two-dimensional group \(\Gamma/\Phi(\Gamma)\). Confusing these two
Frattini constructions would falsely remove the return-even gate. V148's
extension-descent computation of \(V_S=V\cap R_S(\mathcal H_1)\) remains
load-bearing.

## 5. Bounded word-bearing materialization

The canonical subgroup \(\widetilde S\) can be materialized without
enumerating all \(357,128,352\) elements of \(G\):

1. reconstruct the 243-state Cayley table of \(\Gamma\), its centre, and the
   four pure-factor words in task157ee which split the two marked generators
   into \(S\)- and \(G_9\)-parts;
2. build \(E=\pi^{-1}(S\times1)\) from the two pure \(S\) words and
   \(\Gamma\);
3. solve the two inner-action equations on the complete 243-state table and
   obtain lifts centralizing every one of the 26 registered Gamma generators;
4. enumerate only
   \(C_E(\Gamma)\), whose expected order is
   \(|Z(\Gamma)|\,|S|=27\cdot504=13,608\);
5. take its literal derived subgroup and require order 504, trivial
   intersection with \(\Gamma\), the frozen \(S\) presentation, and normality
   under the marked \(x,y\) generators of \(G\);
6. retain source words for canonical generators of \(\widetilde S\); and
7. evaluate the exact words for \(a_0,b_0,\delta_0\) and decide (4.2) by
   literal membership, with an independent reconstruction.

The derived-subgroup construction makes the output independent of the
initial centralizing lifts. A missing arithmetic-reference word is
`UNKNOWN_INPUT`, not permission to compare \(b_0\) with identity.

## 6. Witness boundary

This theorem removes one previously open input from v148:
\(R_S(\mathcal H_0)\) is now explicit when
\(\mathcal H_0=G\). The remaining first-edge tasks are:

1. run the coarse arithmetic comparison (4.2);
2. construct the full joint first relation-module extension (4.3);
3. compute \(V_S\) by v148;
4. identify the two maps \(B_{\rm ev}\) and \(\rho\) on the same literal
   task184 word fibre; and
5. solve their joint equation v148 (5.3).

Only after those pass is there an exact formation-purified first-rung word to
send to the second relative Frattini defect.

```text
TASK157EE/TASK176 JOINT EXTENSION INPUT:          CROSS-CHECKED
OUTER PSL ACTION ON Gamma:                       TRIVIAL / PAPER_PROOF
CANONICAL PSL COMPLEMENT IN G:                   EXISTS UNIQUE / PAPER_PROOF
R_S(G) = CANONICAL PSL COMPLEMENT:                PAPER_PROOF
WORD-BEARING PSL COMPLEMENT:                      NOT YET MATERIALIZED
COARSE ARITHMETIC DIFFERENCE TEST (4.2):          NOT YET RUN
FIRST RELATION-MODULE RESIDUAL V_S:               NOT COMPUTED
ACTUAL JOINT RETURN-EVEN CLASS:                   NOT IDENTIFIED
COMPATIBLE COFINAL LIFT / FAKE / IHARA WITNESS:  NOT DECLARED
```

`R07_TASK176_JOINT_FORMATION_RESIDUAL_V149_PAPER_GRADE`
