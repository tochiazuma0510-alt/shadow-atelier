# R07 A0 exact PSL(2,8)-504 occurrence floor (v437)

Author: Sol / 2026-09-02

Status: paper reduction of the complete finite A0 correction problem to an
exhaustive invariant-span computation of Fox rank at most 505, or combined
Fox-plus-normalized-exponent rank at most 507. The finite group descent is
independently accepted in Task537
(`PSL504_FLOOR_SOUND_AFTER_N_SPLIT_REPAIR`, reply SHA-256
`b331fea766aef5287f52dad25b01b70711b658c54294b5217afe2e1c0d79d002`);
the closure itself is assigned to Luna Task538. No A0 MEMBER/NONMEMBER,
common word, compatible lift, fake, or
Ihara witness is asserted before that closure returns. verified=false.

## 1. A characteristic quotient below Fable's coarse group

Let \(Q_0=\langle\bar x,\bar y\rangle\le S_{36}\) be Fable's coarse group.
Its four point orbits have size nine. Let

\[
 \rho:Q_0\longrightarrow G
\tag{1.1}
\]

be the action on the first orbit \(\{1,\ldots,9\}\), and put
\(K=\ker\rho\). The exact finite data are

\[
 |Q_0|=1,469,664,\qquad |K|=2,916,\qquad
 |G|=504,\qquad G\cong PSL(2,8),\qquad K\text{ solvable}.    \tag{1.2}
\]

The five substitutions used by the two registered hexagons are

\[
 (x,y),\ (x,x^{-1}y^{-1}),\ (y,x^{-1}y^{-1}),\
 (y^{-1}x^{-1},x),\ (y^{-1}x^{-1},y).                       \tag{1.3}
\]

Direct 'GroupHomomorphismByImages' checks on the marked \(Q_0\) show that
each pair in (1.3) defines an automorphism \(\alpha_o\) of \(Q_0\), and

\[
 \alpha_o(K)=K\qquad(o=1,\ldots,5).                         \tag{1.4}
\]

The measured image/kernel sizes for every map are
'1,469,664 / 1', and the measured image of \(K\) has size 2,916 and equals
\(K\). Hence every \(\alpha_o\) descends to an automorphism
\(\bar\alpha_o\) of \(G\).

There is also a structural reason that the same kernel is forced. Since
\(PSL(2,8)\) is nonabelian simple, the image in \(G\) of any solvable normal
subgroup of \(Q_0\) is trivial. Every such subgroup is therefore contained
in the solvable subgroup \(K\). Thus \(K=\operatorname{Rad}(Q_0)\), hence
is characteristic. Task537 additionally identifies
\(Q_0\cong PSL(2,8)\times K\).

This is the load-bearing point. If two source conjugators have the same
image in \(G\), their quotient lies in the kernel of
\(F(x,y)\to G\); (1.4) says every occurrence substitution also sends that
quotient to the identity in \(G\). Thus all six occurrence rows below depend
only on the single 504-state source image. There is no hidden Q0-fibre
enumeration.

## 2. The six-tag occurrence module

Work over \(k=\mathbf F_3\). In \(G\), use the PB3 marking

\[
 a=A_{12}=\rho(\bar x),\qquad
 b=A_{13}=\rho((\bar y\bar x)^{-1}),\qquad
 c=A_{23}=\rho(\bar y),\qquad abc=1.                        \tag{2.1}
\]

Since the PB3 centre \(z=abc\) is now trivial, the complete translated PB3
boundary quotient in one occurrence is

\[
 Y_G=k[G]e_b\oplus k[G]e_c\oplus k\,e_{z,\rm aug},
 \qquad\dim Y_G=2|G|+1=1009.                               \tag{2.2}
\]

In left-prefix Fox coordinates its normal map is

\[
 \begin{aligned}
 h e_a&\longmapsto e_{z,\rm aug}-hae_b-hab e_c,\\
 h e_b&\longmapsto h e_b,\\
 h e_c&\longmapsto h e_c.
 \end{aligned}                                               \tag{2.3}
\]

Keep the three H1 occurrences 'fxy,fxz,fyz' and the three H2 occurrences
'fux,fxy,fuy' separately tagged. Put

\[
 U_G^{\rm Fox}=Y_G^{\oplus6},\qquad
 U_G=U_G^{\rm Fox}\oplus k^2,\qquad
 \dim U_G=6(1009)+2=6056.                                  \tag{2.4}
\]

For a registered correction word \(c\in\Omega\), let \(J_G^{\rm Fox}(c)\)
be the six substituted Fox gradients followed by (2.3), and append the
separate normalized exponent map

\[
 \nu(c)=\left({\exp_x(c)\over18},{\exp_y(c)\over18}\right)
 \pmod3.                                                     \tag{2.5}
\]

Every occurrence value of \(c\) is one. Therefore

\[
 J_G^{\rm Fox}(cd)=J_G^{\rm Fox}(c)+J_G^{\rm Fox}(d),\qquad
 J_G^{\rm Fox}(scs^{-1})=\rho_G(s)J_G^{\rm Fox}(c),          \tag{2.6}
\]

where \(\rho_G(s)\) left-translates each tagged regular coordinate by the
corresponding substituted image \(\bar\alpha_o(s)\) and fixes the six
augmentation scalars. Conjugation also fixes \(\nu(c)\), so (2.6) holds for
the combined vector \((J_G^{\rm Fox}(c),\nu(c))\).

## 3. Exhaustive closure has combined rank at most 507

Let \(r_1,\ldots,r_{44}\) be the complete compact relation roster for the
marked quotient \(\Delta\), with \(r_{44}\) empty, and define

\[
 W_G=\left\langle
 \rho_G(q)(J_G^{\rm Fox}(r_i),\nu(r_i)):
 q\in G,\ 1\le i\le44
 \right\rangle_k.                                           \tag{3.1}
\]

Exactly as in v396, normal generation and (2.6) give

\[
 \boxed{\{(J_G^{\rm Fox}(c),\nu(c)):c\in\Omega\}=W_G.}       \tag{3.2}
\]

There is a much smaller a priori rank bound than (2.4). Put
\(\Omega_G=\ker(F(x,y)\to G)\). Since \(\Omega\subseteq\Omega_G\) and all
six substitutions descend to automorphisms of \(G\), the six Fox components
factor linearly through \(H_1(\Omega_G;k)\). Nielsen--Schreier gives

\[
 \dim_kH_1(\Omega_G;k)=1+|G|(2-1)=505.                      \tag{3.3}
\]

The normalized exponent map (2.5) must not be included in this
factorization: division by 18 occurs before reduction modulo three. Indeed,
Task535 has \(r_1=w^3\), with \(w\in\Omega_G\), so
\([r_1]=3[w]=0\) in \(H_1(\Omega_G;k)\), whereas
\(\nu(r_1)=(1,0)\). It is a separate two-dimensional summand. Therefore

\[
 \boxed{\dim W_G^{\rm Fox}\le505,\qquad \dim W_G\le507.}     \tag{3.4}
\]

In fact seeds 1 and 2 have zero projected Fox part and their N-vectors
\((1,0)\) and \((2,2)\) span \(k^2\), so the extra bound is sharp as a safe
structural allowance.

An invariant-span queue which inserts the 44 seed rows and applies
\(x^{\pm1},y^{\pm1}\) only to a newly retained row therefore exhausts after
at most

\[
 \boxed{44+4\dim W_G\le2,072}                               \tag{3.5}
\]

row-insertion attempts. This is a complete finite closure, not a bounded
conjugator search.

## 4. Fixed aggregation and the target equation

Use the exact registered literal convention

\[
 H_1(f)=f_{yz}f_{xz}^{-1}f_{xy},\qquad
 H_2(f)=f_{uy}f_{xy}^{-1}f_{ux}^{-1}.                       \tag{4.1}
\]

Write \(g_o\) for the relevant substitution of \(g=g_{760}\), evaluated in
\(G\). Since every correction occurrence evaluates to one, the Fox product
rule gives the fixed linear map
\(L_g:U_G\to Y_G^{\oplus2}\oplus k^2\):

\[
 \begin{aligned}
 (L_gJ)_1={}&J_{xy}-g_{yz}J_{xz}+g_{yz}J_{yz},\\
 (L_gJ)_2={}&-g_{uy}g_{xy}^{-1}J_{ux}-g_{uy}J_{xy}+g_{uy}J_{uy},
 \end{aligned}                                               \tag{4.2}
\]

and \(L_g\) passes the two exponent coordinates unchanged. Expanding
(4.1) for \(gc\) proves directly that

\[
 L_g(J_G^{\rm Fox}(c),\nu(c))=
 \bigl(J(H_1(gc))-J(H_1(g)),
       J(H_2(gc))-J(H_2(g)),\nu(c)\bigr).                   \tag{4.3}
\]

This formula is to be checked entrywise on all 44 identity columns before
the closure result is accepted.

Let \(T_G\) be the negative of the two base gradients for \(g\), with zero
normalized exponent coordinates. Projection kills the complete PB3
boundary by (2.2)--(2.3) and drops the PB4 block. Therefore any full A0
solution necessarily satisfies

\[
 \boxed{T_G\in L_g(W_G).}                                  \tag{4.4}
\]

The target space in (4.4) has only

\[
 2(2|G|+1)+2=2020                                           \tag{4.5}
\]

coordinates, and its correction image has rank at most 507.

### Theorem 4.1 (PSL504 FLOOR)

If the exhaustive queue (3.1) gives

\[
 T_G\notin L_g(W_G),                                        \tag{4.6}
\]

then the original A0 equation has no solution. A separating functional on
the 2020-coordinate space which annihilates the complete image basis and
pairs to one with \(T_G\) is an exact finite A0 NONMEMBER certificate after
an independent reconstruction of (1.1)--(4.4).

If instead (4.4) holds, this proves only quotient membership. Coefficient
ancestry in the exhausted occurrence basis returns a correction class whose
residual lies in the order-2916 kernel layer (and, upstairs, the pc3/PB4
layers); it is not yet an A0 word.

#### Proof

Equations (3.2) and (4.3) identify the complete projected correction image,
not a prefix. Functoriality sends every full A0 equality to (4.4), so (4.6)
contradicts existence upstairs. Conversely, projection is not injective;
hence membership downstairs has only the stated necessary meaning.
\(\square\)

~~~text
Q0 -> PSL(2,8) DESCENT:                  TASK537 PASS
SIX-TAG CORRECTION AMBIENT:              6,056
COMPLETE FOX RANK BOUND:                 <= 505
COMBINED FOX+N RANK BOUND:               <= 507
MAXIMUM INVARIANT-SPAN INSERT ATTEMPTS:  <= 2,072
PHYSICAL TARGET AMBIENT:                 2,020
EXHAUSTED FLOOR MEMBERSHIP:              TASK538, NOT YET EXECUTED
A0 ACTUAL COMMON/NONMEMBER:              UNDECIDED
COMPATIBLE LIFT / FAKE / IHARA:          NOT DECLARED
verified:                                false
~~~

R07_A0_PSL504_OCCURRENCE_FLOOR_V437_PAPER
