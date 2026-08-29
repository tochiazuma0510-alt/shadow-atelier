# R07 kernel base-change five-term gate (v361)

Author: Sol / 2026-08-30

Status: paper theorem refining v169, v319, v321, v326, v327 and v359.
It gives the exact discrepancy between a finite kernel obtained by reducing
linear side gates and the intrinsic leading quotient of the completed kernel.
There are two, and only two, discrepancy modules: a saturation kernel and a
lifting cokernel.  Both are finite linear-algebra objects at a finite R07
edge.  They have not yet been computed for the actual legal correction source
or the formation--Brunnian target.  No compatible lift, fake certificate or
Ihara witness is declared.  `verified=false`.

## 1. The exact five-term sequence

Let \(\Lambda\) be a ring, let \(J\triangleleft\Lambda\) be a two-sided
ideal, and let

\[
 f:M\longrightarrow N
\tag{1.1}
\]

be a homomorphism of left \(\Lambda\)-modules.  Put \(L=\ker f\).  Reduction
modulo \(J^r\), for \(r\geq1\), gives

\[
 \bar f_r:M/J^rM\longrightarrow N/J^rN.
\tag{1.2}
\]

Define

\[
 \begin{aligned}
 S_r(f)&=\frac{L\cap J^rM}{J^rL},\\
 T_r(f)&=\frac{\operatorname{im}f\cap J^rN}{f(J^rM)}.
 \end{aligned}
\tag{1.3}
\]

The first is the saturation module already isolated in v321.  The second is
the obstruction to lifting a reduced kernel vector to an actual kernel
vector without changing its residue class.

### Theorem 1.1 (KERNEL BASE-CHANGE FIVE-TERM SEQUENCE)

There is a natural exact sequence

\[
 \boxed{
 0\longrightarrow S_r(f)
 \longrightarrow L/J^rL
 \stackrel{\alpha_r}{\longrightarrow}\ker\bar f_r
 \stackrel{\delta_r}{\longrightarrow}T_r(f)
 \longrightarrow0.}
\tag{1.4}
\]

For \(\bar x\in\ker\bar f_r\), represented by \(x\in M\), the connecting
map is the explicit formula

\[
 \boxed{\delta_r(\bar x)=[f(x)]\pmod {f(J^rM)}.}
\tag{1.5}
\]

#### Proof

The map \(L\to M/J^rM\) lands in \(\ker\bar f_r\) and kills \(J^rL\),
giving \(\alpha_r\).  Its kernel consists exactly of the classes represented
by \(L\cap J^rM\), so

\[
 \ker\alpha_r=S_r(f).
\tag{1.6}
\]

If \(\bar x\in\ker\bar f_r\), then \(f(x)\in J^rN\), and of course
\(f(x)\in\operatorname{im}f\).  Replacing \(x\) by \(x+j\), with
\(j\in J^rM\), changes \(f(x)\) by an element of \(f(J^rM)\).  Thus
(1.5) is well defined.

The equality \(\delta_r(\bar x)=0\) means that
\(f(x)=f(j)\) for some \(j\in J^rM\).  Then \(x-j\in L\) and
\(\alpha_r([x-j])=\bar x\).  Conversely every image of \(\alpha_r\) is
killed by \(\delta_r\).  Hence

\[
 \ker\delta_r=\operatorname{im}\alpha_r.
\tag{1.7}
\]

Finally, every class of \(T_r(f)\) has a representative \(f(x)\) which lies
in \(J^rN\).  Its class \(\bar x\) belongs to \(\ker\bar f_r\), and (1.5)
maps it to the given class.  Thus \(\delta_r\) is onto.  This proves
(1.4). \(\square\)

When the modules in (1.4) are finite dimensional over the coefficient
field, exactness gives the audit identity

\[
 \boxed{
 \dim L/J^rL
 =\dim\ker\bar f_r+\dim S_r(f)-\dim T_r(f).}
\tag{1.8}
\]

Thus a naive reduced kernel can be wrong in either direction: saturation can
make the intrinsic quotient larger, while a nonzero lifting obstruction can
make it smaller.

## 2. Exact criterion and split sufficient condition

### Corollary 2.1 (HONEST KERNEL BASE CHANGE)

The natural map

\[
 L/J^rL\longrightarrow\ker\bar f_r
\tag{2.1}
\]

is an isomorphism if and only if

\[
 \boxed{S_r(f)=0=T_r(f).}
\tag{2.2}
\]

The two equalities have different meanings and neither may be omitted.
V321's same-depth saturation gate is \(S_r(f)=0\); it does not by itself
prove that every reduced kernel vector lifts.

### Corollary 2.2 (SPLIT EPIMORPHISM)

If \(f:M\twoheadrightarrow N\) has a \(\Lambda\)-linear section, then

\[
 S_r(f)=T_r(f)=0
\quad\text{for every }r.
\tag{2.3}
\]

#### Proof

A section gives \(M=L\oplus s(N)\), so projection to \(L\) proves
\(L\cap J^rM=J^rL\).  Surjectivity and linearity give
\(f(J^rM)=J^rN\), so the numerator and denominator of \(T_r(f)\) agree.
\(\square\)

More generally, if the map is viewed as the epimorphism
\(M\twoheadrightarrow I=\operatorname{im}f\), a module section kills
\(S_r(f)\); to kill \(T_r(f)\) one additionally needs

\[
 I\cap J^rN=J^rI.
\tag{2.4}
\]

This separates splitting of the kernel sequence from strictness of the image
inside the chosen codomain.

## 3. The actual legal source quotient

V169 presents the completed common-word source as the kernel of one finite
free augmented side map

\[
 G:\widetilde A\longrightarrow Y,
 \qquad A_{\rm legal}=\ker G.
\tag{3.1}
\]

Here the coordinates of \(G\) include the source-cycle, common-value and
every registered homogeneous linear side equation.  At the leading edge the
easy finite space is

\[
 A_{\rm naive}=\ker\bar G.
\tag{3.2}
\]

Theorem 1.1 gives the exact replacement for an unproved identification:

\[
 0\longrightarrow S_1(G)
 \longrightarrow A_{\rm legal}/JA_{\rm legal}
 \longrightarrow A_{\rm naive}
 \longrightarrow T_1(G)
 \longrightarrow0.
\tag{3.3}
\]

For the v359 relative branch, the actual finite common-value coordinate of
(3.2) must first be restricted to

\[
 C_{\rm rel}=[\widetilde S,K]
\tag{3.4}
\]

and then to the physically registered homogeneous gates.  V360 makes the
action in (3.4) bounded and word-bearing.  Even after that calculation,
however, one may identify the resulting finite kernel with
\(A_{\rm legal}/JA_{\rm legal}\) only after computing both modules in
(3.3), or after exhibiting a split map which kills them.

This also corrects the role of v359's group-algebra ideal

\[
 I_{\rm adm}=\sum_i\mathbf F_3[\Delta_1](c_i-1).
\tag{3.5}
\]

It is an exact finite ambient orbit model once the legal values \(c_i\) are
known.  Equation (3.5) is not itself the base-change isomorphism in (3.3).
An occurrence compiler may use its columns, but promotion to the completed
Newton source requires the two zero defects or an equivalent exact
presentation.

## 4. The actual localized target quotient

Package the literal formation, Brunnian and other homogeneous localization
maps into one map

\[
 H:Z\longrightarrow Q,
 \qquad L_{\rm loc}=\ker H.
\tag{4.1}
\]

Writing \(\bar H\) for the leading reduction gives another exact sequence:

\[
 \boxed{
 0\longrightarrow S_1(H)
 \longrightarrow L_{\rm loc}/JL_{\rm loc}
 \longrightarrow\ker\bar H
 \longrightarrow T_1(H)
 \longrightarrow0.}
\tag{4.2}

Therefore the intersection of the finite formation and normalized-Brunnian
kernels is the actual \(L/JL\) precisely when both defects in (4.2) vanish.
V326--v327 give structural ways to prove this: a filtered module retraction
kills \(S_1(H)\), and an actual split epimorphism onto the packaged target
kills both terms.  A simplicial normalization projector alone handles all
but the remaining normalized \(d_0\) sequence and does not silently prove
(4.2) is an isomorphism.

## 5. Finite certificate and leading-onto decision

At a physical finite successor ring, every term in (3.3) and (4.2) is an
ordinary finite module calculation.  A complete receipt must retain:

1. the ambient modules, the two-sided ideal \(J\), and literal matrices for
   the packaged maps \(G,H\);
2. bases and ancestries for \(\ker G,\ker H\), their intersections with
   \(J\widetilde A,JZ\), and their intrinsic \(J\)-multiples;
3. bases for \(\operatorname{im}G\cap JY\), \(G(J\widetilde A)\),
   \(\operatorname{im}H\cap JQ\), and \(H(JZ)\);
4. direct replay of the two five-term sequences and dimension identity
   (1.8), independently reconstructed in a different pivot order; and
5. the induced actual leading Jacobian between the middle terms of (3.3)
   and (4.2), followed by a primal onto ancestry or a dual cokernel row.

If a finite owner supplies explicit sections instead, the checker must replay
their linearity and the two identities in Corollary 2.2.  Merely observing
the same dimensions for a reduced kernel and an intrinsic quotient is not a
substitute for the natural-map comparison.

This gives the exact post-A4 finite chain:

\[
 \boxed{
 K\longrightarrow[\widetilde S,K]
 \longrightarrow A_{\rm naive}
 \stackrel{(S_1(G),T_1(G))}{\longleftarrow}
 A_{\rm legal}/JA_{\rm legal}
 \stackrel{\bar B}{\longrightarrow}
 L_{\rm loc}/JL_{\rm loc}
 \stackrel{(S_1(H),T_1(H))}{\longrightarrow}
 \ker\bar H.}
\tag{5.1}
\]

It replaces both vague type identifications in v359 by four named finite
modules.  It does not assume that any of the four vanish.

## 6. R07 frontier

The five-term sequence, the isomorphism criterion and the split sufficient
condition are paper proofs.  The current positive A4 owner is still absent,
so the two source defects and two target defects have not been evaluated.
Task382 addresses only the preceding exact extraction (3.4); it does not
claim (3.3), (4.2), or leading onto.

```text
KERNEL BASE-CHANGE FIVE-TERM SEQUENCE:            PAPER PROOF
NAIVE REDUCED KERNEL = INTRINSIC LEADING QUOTIENT: IFF S_1=T_1=0
SOURCE BASE-CHANGE DEFECTS S_1(G),T_1(G):           NOT COMPUTED
TARGET BASE-CHANGE DEFECTS S_1(H),T_1(H):           NOT COMPUTED
CANONICAL LEGAL VALUE SOURCE [tilde-S,K]:           PAPER ALGORITHM / v360
ACTUAL LEADING COMMON-WORD JACOBIAN:                NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA WITNESS:             NOT CONSTRUCTED
```

`R07_KERNEL_BASE_CHANGE_FIVE_TERM_GATE_V361_PAPER_GRADE`
