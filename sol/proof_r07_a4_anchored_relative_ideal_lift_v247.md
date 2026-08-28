# R07 A4-anchored relative-ideal lift v247

Author: Sol / 2026-08-28

Status: paper theorem and load-bearing erratum to v238 and v242.  The literal
word \([x,y]^3\) represents the generator of the *projected* first-edge
kernel, but it is not in the actual seven-context roof kernel.  An exact
producer/checker replay in the authenticated task176 roof finds it nontrivial
in all ten typed coordinates.  The correct explicit lift is obtained by
lifting that projected generator through the word-bearing A4 basis of the
actual successor kernel.  This gives a finite source-word right inverse on
the projected relative ideal at every elementary-abelian relative Frattini
edge.  No actual A2--A5 terminal, pointed multiplier, fake certificate, or
Ihara witness is declared.  `verified=false`.

This note supersedes v238 Lemma 2.1 and the occurrences of the pair
\(s(g)[x,y]^3-s(g)\) in v242 (1.3), (5.1), and (6.1).  The affine-slice
arguments of those notes remain valid after the replacement proved below.

## 1. The projected generator is not an actual roof-kernel word

Retain the first relative Frattini edge and its matching exponent-nine
quotient:

\[
 F=F(x,y)\twoheadrightarrow\Delta _1
 \mathrel{\mathop{\twoheadrightarrow}^{\pi}}\Delta _0,
 \qquad K=\ker\pi,
 \qquad
 q:\Delta _1\twoheadrightarrow D_1\cong\mathcal H_2(9).
\tag{1.1}
\]

Put

\[
 h=[x,y]=x^{-1}y^{-1}xy,
 \qquad c=h^3,
 \qquad z_0=q(c)=(0,0,3).
\tag{1.2}
\]

V213--v214 prove

\[
 R_0:=q(K)=\langle z_0\rangle\cong C_3.
\tag{1.3}
\]

Equation (1.3) says that *some* element of the actual kernel maps to
\(z_0\).  It does not say that the particular source word \(c\) belongs to
\(K\).  Indeed, the authenticated task176 roof receipt

```text
ci/in/d972_r07_all_seven_extension_section_census_v1.json
bytes  = 13649089
sha256 = 715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41
```

contains the literal marked-generator blobs in all ten typed coordinates.
The producer multiplication/inversion ABI and the independent task176
checker evaluation path both evaluate the strict word

```text
[-1,-2,1,2,-1,-2,1,2,-1,-2,1,2]
```

with the following identical result:

```text
identity_by_coordinate = [false,false,false,false,false,
                          false,false,false,false,false]
nonidentity_indices    = [0,1,2,3,4,5,6,7,8,9]
joint_blob_sha256       = 1460601df23f2e444d0fc3cad5b13d36e74ff7982c8c4b3551c38796af1d392d
```

The two exact replay paths are:

```text
producer: search/d972_r07_all_seven_extension_section_census_v1.py
          multiply_blob / inverse_blob on the receipt's marked blobs
checker:  crosscheck/check_d972_r07_all_seven_extension_section_census_v1.py
          reconstruct_deletion / eval_coords
```

Thus

\[
 \boxed{\pi(c)\ne1,\qquad c\notin K.}
\tag{1.4}
\]

This is a cross-checked finite replay, not a Lean verification.  Its role is
only to reject the literal lift used in v238; the replacement below is a
group-theoretic construction.

## 2. A constructive relative-ideal lifting lemma

Let

\[
 G\mathrel{\mathop{\twoheadrightarrow}^{\pi}}G_0,
 \qquad K=\ker\pi,
 \qquad
 q:G\twoheadrightarrow D,
 \qquad R=q(K)\triangleleft D
\tag{2.1}
\]

be finite groups, and let \(k\) be a field.  Write

\[
 I_K=\ker(k[G]\to k[G_0]),
 \qquad
 I_R=\ker(k[D]\to k[D/R]).
\tag{2.2}
\]

Choose:

1. a left transversal \(T\) of \(R\) in \(D\);
2. a set-theoretic section \(s:T\to G\) of \(q\); and
3. for every \(r\in R\), an element \(\sigma(r)\in K\) with
   \(q(\sigma(r))=r\), with \(\sigma(1)=1\).

The set

\[
 \mathcal B_R={t(r-1):t\in T,\ r\in R\setminus\{1\}\}
\tag{2.3}
\]

is a \(k\)-basis of \(I_R\).  Define on this basis

\[
 \mathfrak s_{K,R}\bigl(t(r-1)\bigr)
   =s(t)(\sigma(r)-1)\in k[G].
\tag{2.4}
\]

### Theorem 2.1 (WORD-BEARING RELATIVE-IDEAL SECTION)

The map (2.4) extends uniquely to a \(k\)-linear map

\[
 \boxed{\mathfrak s_{K,R}:I_R\longrightarrow I_K}
\tag{2.5}
\]

satisfying

\[
 \boxed{q_*\mathfrak s_{K,R}=\operatorname{id}_{I_R}.}
\tag{2.6}
\]

If the chosen elements \(s(t)\) and \(\sigma(r)\) carry source words, then
every value of \(\mathfrak s_{K,R}\) is a finite, word-bearing sum of pairs

\[
 s(t)\sigma(r)-s(t)
\tag{2.7}
\]

whose two words have exactly the same \(G_0\)-value.

#### Proof

The group-element basis of \(k[D]\) decomposes over the left cosets
\(tR\).  On one coset, the kernel of the coefficient-sum map
\(k[tR]\to k[tR/R]\cong k\) has the basis
\(\{t(r-1):r\ne1\}\).  Taking the direct sum over \(T\) proves that
(2.3) is a basis of \(I_R\).

Because \(\sigma(r)\in K\),

\[
 \pi\bigl(s(t)\sigma(r)\bigr)=\pi(s(t)),
\tag{2.8}
\]

so (2.4) belongs to \(I_K\) and has the word-pair form (2.7).  Applying
\(q_*\) gives

\[
 q_*\bigl(s(t)(\sigma(r)-1)\bigr)=t(r-1),
\tag{2.9}
\]

which proves (2.6) on the basis and hence everywhere. \(\square\)

The section need not be \(k[D]\)-linear or canonical without choices.  It
is exactly what the explicit-lift compiler needs: a finite, typed right
inverse with literal source ancestry.

## 3. Extracting the first-edge anchor from A4

At the first edge, \(K\) is an elementary-abelian three-group.  Let an
independently accepted A4 package return an ordered word-bearing basis

\[
 K=\langle k_1,\ldots,k_t\rangle_{\mathbf F_3},
 \qquad k_i=\rho_1(u_i),\quad u_i\in F.
\tag{3.1}
\]

By (1.3), there are unique scalars \(a_i\in\mathbf F_3\) such that

\[
 q(k_i)=z_0^{a_i}.
\tag{3.2}
\]

At least one \(a_i\) is nonzero.  Let \(j\) be the least such index and put

\[
 e=a_j^{-1}\in\mathbf F_3^\times,
 \qquad
 k_z=k_j^e,
 \qquad
 u_z=u_j^e.
\tag{3.3}
\]

Here \(u_j^2\) means literal concatenation followed by free reduction.  The
ordered-basis rule makes this choice deterministic inside the certificate.

### Lemma 3.1 (A4 PROJECTED-GENERATOR ANCHOR)

The word \(u_z\) satisfies

\[
 \boxed{\rho_1(u_z)=k_z\in K,\qquad
        \rho_0(u_z)=1,\qquad q(k_z)=z_0.}
\tag{3.4}
\]

#### Proof

The first two assertions follow from \(k_j\in K\) and closure of \(K\).
Equation (3.2) and the definition of \(e\) give
\(q(k_z)=z_0^{a_je}=z_0\). \(\square\)

Equivalently, one may solve the one-row linear equation

\[
 \sum_i b_i a_i=1
\tag{3.5}
\]

and take \(k_z=\prod_i k_i^{b_i}\).  The least-index rule (3.3) is the
smallest deterministic solution.  If a complete accepted A4 basis produced
\(a_i=0\) for every \(i\), that would contradict (1.3) and is an input/type
mismatch, not an A3 NONMEMBER terminal.

## 4. The corrected explicit lift of a positive A3 coefficient

Write every \(g\in D_1\) in the retained normal form

\[
 g=(a,b,r)=x^ay^bh^r,
 \qquad 0\le a,b,r<9,
\tag{4.1}
\]

and choose the literal source section

\[
 s(g)=x^ay^bh^r\in F.
\tag{4.2}
\]

Suppose the actual A3 pre-gate is positive and returns

\[
 \lambda=\sum_g\lambda_g g\in\mathbf F_3[D_1],
 \qquad
 \kappa_D=\lambda(z_0-1),
 \qquad
 C(\kappa_D\odot w)=\bar\epsilon_1.
\tag{4.3}
\]

Using the A4 anchor (3.3), define

\[
 \widetilde\kappa_0
   =\sum_g\lambda_g\bigl(s(g)u_z-s(g)\bigr)\in\mathbf F_3[F],
 \qquad
 \kappa_0=\rho_{1,*}(\widetilde\kappa_0)
       \in\mathbf F_3[\Delta_1].
\tag{4.4}
\]

### Theorem 4.1 (A3+A4 EXPLICIT ROOF-FIBRE SEED)

Put

\[
 I=\ker\bigl(\mathbf F_3[\Delta_1]
       \to\mathbf F_3[\Delta_0]\bigr),
 \qquad
 \Phi(\kappa)=C(\kappa\odot w).
\tag{4.5}
\]

Then

\[
 \boxed{
 \kappa_0\in I,
 \qquad q_*(\kappa_0)=\kappa_D,
 \qquad \Phi(\kappa_0)=\bar\epsilon_1.}
\tag{4.6}
\]

Every summand of (4.4) is a literal roof-fibre pair.

#### Proof

Lemma 3.1 gives

\[
 \rho_0(s(g)u_z)=\rho_0(s(g)),
\tag{4.7}
\]

so every difference in (4.4) lies in the source relative ideal and
\(\kappa_0\in I\).  The same lemma and (4.2) give

\[
 q_*\bigl(\rho_{1,*}(s(g)u_z-s(g))\bigr)=g(z_0-1).
\tag{4.8}
\]

Summing with the coefficients \(\lambda_g\) proves the second assertion of
(4.6).  V214 Theorem 2.1 says that the matching projected occurrence
endpoint depends only on this \(D_1\)-image.  Equation (4.3) therefore proves
the third assertion.  Equation (4.7) is the asserted roof-fibre typing.
\(\square\)

Theorem 4.1 is the correct replacement for v238 Lemma 2.1.  A3 supplies the
projected algebra coefficient; A4 supplies the actual-kernel anchor.  Neither
input alone supplies (4.4).

## 5. The A5 slice and A6 pair compiler survive unchanged

With the corrected base point (4.4), put

\[
 H=\ker\Phi,
 \qquad
 r_0=e_1-\kappa_0d_1.
\tag{5.1}
\]

The algebra in v238 Theorem 3.1 is independent of how the base point was
constructed and gives

\[
 \boxed{
 \exists\mu_1\in I:
   (\mu_1d_1=e_1,\ \Phi(\mu_1)=\bar\epsilon_1)
 \quad\Longleftrightarrow\quad
 r_0\in Hd_1.}
\tag{5.2}
\]

If \(r_0=\theta d_1\) for \(\theta\in H\), then

\[
 \mu_1=\kappa_0+\theta.
\tag{5.3}
\]

V242's occurrence-level joint closure computes \(Hd_1\) from the same A4
basis.  Thus A4 now has two distinct roles:

1. it supplies the complete generators \(k_i-1\) of the relative ideal; and
2. it supplies the single anchor \(k_z\) used in (4.4).

There is no circularity: A4 is computed without A3, while A5 combines their
accepted ancestries.

Every A5 correction term has the form

\[
 g(k_i-1)=gk_i-g,
\tag{5.4}
\]

and every base-point term has the form in (4.4).  Both are actual roof-fibre
pairs.  Therefore a MEMBER ancestry still emits directly

\[
 \widetilde\mu_1=\sum_q c_q(U_q-V_q),
 \qquad \rho_0(U_q)=\rho_0(V_q),
\tag{5.5}
\]

and the v231 A6 specialization \(\alpha=\mu_1,\beta=0\) remains valid.  Only
the first pair family changes from the invalid
\(s(g)c-s(g)\) to the valid \(s(g)u_z-s(g)\).

## 6. All-rung constructive form

For the edge \(\Delta_{m+1}\twoheadrightarrow\Delta_m\), v213 gives an
elementary-abelian defect

\[
 R_m=q_{m+1}(K_m)\cong(\mathbf F_3)^{a_m},
 \qquad a_m\le3.
\tag{6.1}
\]

Once a word-bearing basis of the actual \(K_m\) and its complete
\(R_m\)-projection matrix are known, ordinary \(\mathbf F_3\)-elimination
chooses word-bearing lifts in \(K_m\) of a basis of \(R_m\).  Theorem 2.1
then produces a finite source-word section

\[
 \boxed{I(R_m)\longrightarrow I_m}
\tag{6.2}
\]

for the whole projected relative ideal, not only for one selected A3 class.
The target rank is at most three, although the ideal itself has the larger
finite dimension recorded in v214.

This is a uniform *compiler*.  It does not assert that the selected A4 bases,
sections, or A5 MEMBER solutions are already compatible under every inverse-
limit reduction.  Coherent all-rung choice remains a later gate.

## 7. Corrected production contract

The A4 positive receipt must now contain, in addition to the v231 kernel
contract:

1. each ordered basis word \(u_i\), its actual \(\Delta_1\) value, and its
   identity value in the complete task198 \(\Delta_0\) evaluator;
2. an independently reconstructed \(D_1=\mathcal H_2(9)\) value
   \(q(k_i)=z_0^{a_i}\) for every basis element;
3. the least nonzero index \(j\), scalar \(e=a_j^{-1}\), literal word
   \(u_z=u_j^e\), and all three replays in (3.4); and
4. mutations of the selected basis row, its projected exponent, the chosen
   inverse scalar, the concatenation order, and each of the two endpoint
   replays.

The A5 consumer must authenticate the same A4 anchor and replace every
literal cube pair by (4.4).  It must not accept the fact that
\(q(c)=z_0\) as evidence that \(c\in K\).

## 8. Fixed frontier

```text
LITERAL [x,y]^3 IN ACTUAL DELTA0:                 NONIDENTITY 10/10 / CROSS-CHECKED REPLAY
v238 LEMMA 2.1 LITERAL-CUBE LIFT:                 REJECTED / SUPERSEDED
FINITE RELATIVE-IDEAL WORD SECTION I(R)->I(K):    PAPER PROOF
A4 BASIS -> ACTUAL k_z WITH q(k_z)=z0:            PAPER PROOF / NOT COMPUTED
A3+A4 -> EXPLICIT ROOF-FIBRE kappa0:              PAPER PROOF / NOT COMPUTED
CORRECTED A5 SLICE THEOREM:                       PAPER PROOF / ACTUAL RUN NOT COMPUTED
CORRECTED DIRECT A6 PAIR HANDOFF:                 PAPER PROOF / ACTUAL M NOT COMPUTED
ALL-RUNG RELATIVE-IDEAL COMPILER:                 PAPER PROOF
COHERENT ALL-RUNG SECTIONS / MEMBER CHOICES:      NOT CONSTRUCTED
EXACT THREE PB ENDPOINTS / FAKE / IHARA WITNESS:  NOT CONSTRUCTED
```

`R07_A4_ANCHORED_RELATIVE_IDEAL_LIFT_V247_PAPER_GRADE`
