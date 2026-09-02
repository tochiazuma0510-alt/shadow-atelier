# R07 A0: explicit G9 twisting data for the two post-2016 rungs (v442)

Author: Sol / 2026-09-03

Status: candidate paper specialization of v441.  It extracts the two
transversals, the first split cocycle, the second carry cocycle, the kernel
actions and the occurrence crossed terms directly from the frozen degree-36
mark.  It does not assert that any positive-grade residual is MEMBER.  The
tables below require an independent permutation replay before adoption.
`verified=false`.

## 1. Affine coordinates forced by the frozen mark

On each of the three 9-point blocks write an element of `D9` as

\[
 (r,e):t\longmapsto (-1)^e t+r,
 \qquad r\in\mathbf Z/9,\quad e\in\mathbf F_2.
\]

The permutation evaluator used by the current A0 artifacts multiplies in the
right-action order `p star q = q after p`.  Therefore

\[
 (r,e)\star(s,f)=((-1)^f r+s,e+f).                 \tag{1.1}
\]

Reading the three blocks of the frozen marked permutations gives

\[
 X=((1,0),(0,1),(0,1)),\qquad
 Y=((1,1),(1,0),(1,1)).                             \tag{1.2}
\]

Thus their parity vectors are `(0,1,1)` and `(1,0,1)`, as in v439.
Put

\[
 t_1=X^{10},\qquad t_2=Y^{10},\qquad t_3=(XY)^{10}.
                                                               \tag{1.3}
\]

Direct use of (1.1) yields

\[
 t_1=(1,0,0),\qquad t_2=(0,1,0),\qquad t_3=(0,0,1)
                                                               \tag{1.4}
\]

in the rotation subgroup.  Consequently

\[
 N=G9'=\langle t_1,t_2,t_3\rangle\cong C_9^3.       \tag{1.5}
\]

There is an explicit pure-sign complement.  Define

\[
 s_X=X^9,
 \qquad
 s_Y=t_1t_2^{-1}t_3Y.                               \tag{1.6}
\]

Then `s_X` and `s_Y` have zero rotation coordinate, have parities
`(0,1,1)` and `(1,0,1)`, commute, and have order two.  Hence

\[
 \boxed{G9=N\rtimes A,\qquad A=\langle s_X,s_Y\rangle\cong C_2^2.}
                                                               \tag{1.7}
\]

The action on the ordered rotation basis is

\[
 s_X:\operatorname{diag}(1,-1,-1),\qquad
 s_Y:\operatorname{diag}(-1,1,-1).                 \tag{1.8}
\]

This is stronger than an abstract Schur--Zassenhaus choice: both the
complement and its source words are fixed by (1.3) and (1.6).

## 2. Exact occurrence action on N

Use the six-tag order already fixed in Tasks 538/542,

\[
 (X,Y),\ (X,Z),\ (Y,Z),\ (U,X),\ (X,Y),\ (U,Y),
 \quad Z=X^{-1}Y^{-1},\quad U=Y^{-1}X^{-1}.          \tag{2.1}
\]

Let `M_j` be the integer matrix whose `i`-th column is the rotation vector
of the image of `t_i`.  Formula (1.1) gives signed permutation matrices:

\[
\begin{array}{c|c}
j&M_j\\ \hline
0&\begin{pmatrix}1&0&0\\0&1&0\\0&0&1\end{pmatrix}\\[2mm]
1&\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}\\[2mm]
2&\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}\\[2mm]
3&\begin{pmatrix}0&1&0\\0&0&-1\\-1&0&0\end{pmatrix}\\[2mm]
4&\begin{pmatrix}1&0&0\\0&1&0\\0&0&1\end{pmatrix}\\[2mm]
5&\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}.
\end{array}                                                   \tag{2.2}
\]

For example, `Z` has affine data

\[
 r_Z=(2,-1,1),\quad e_Z=(1,1,0),
\]

and `U` has

\[
 r_U=(0,1,-1),\quad e_U=(1,1,0).
\]

These two checks determine all nontrivial signs in (2.2).

## 3. Occurrence crossed terms for the fixed complement

Although (1.7) splits the group extension, an occurrence need not preserve
the chosen complement.  Write

\[
 \alpha_j(s(e))=(c_j(e),A_je),                       \tag{3.1}
\]

where `s(e)` is the pure-sign section and `A_j` is the already audited
action on `A`.  It suffices to give `c_j` on `s_X,s_Y`:

\[
\begin{array}{c|c|c}
j&c_j(s_X)&c_j(s_Y)\\ \hline
0&(0,0,0)&(0,0,0)\\
1&(0,0,0)&(1,0,0)\\
2&(1,0,1)&(1,-2,0)\\
3&(0,1,0)&(0,1,1)\\
4&(0,0,0)&(0,0,0)\\
5&(0,1,0)&(0,0,2).
\end{array}                                                   \tag{3.2}
\]

All entries are in `(Z/9)^3`.  The value on the fourth element of `A` is
not obtained by ordinary addition; in the evaluator convention it is

\[
 c_j(e+f)=S(A_jf)c_j(e)+c_j(f),                     \tag{3.3}
\]

where `S(a)` is the diagonal sign action (1.8).  Equations (2.2)--(3.3)
therefore give the full affine formula

\[
 \boxed{\alpha_j(r,e)=(M_jr+c_j(e),A_je).}           \tag{3.4}
\]

The `PSL(2,8)` component is direct and continues to use its pinned marked
substitution table.  It neither changes the kernel action nor the cocycles
above.

## 4. First extension: Q2 to Q1 is split

Let

\[
 Q_1=PSL(2,8)\times A,
 \qquad
 Q_2=Q_0/(1\times N^3).
\]

Reduction of (1.7) modulo `N^3` gives

\[
 Q_2=PSL(2,8)\times(C_3^3\rtimes A).                \tag{4.1}
\]

The section `(p,e) -> (p,0,e)` is a homomorphism.  Hence the multiplication
cocycle for the first extension is identically zero.  Its kernel action is
the sign action (1.8), the occurrence restriction is `M_j mod 3`, and the
occurrence crossed cochain is `c_j(e) mod 3`.

Thus the first six-grade lift needs no generic transversal search and no
2916-state enumeration.  All twisting is the finite table (2.2), (3.2),
(3.3), together with the pinned 2016-element quotient arithmetic.

## 5. Second extension: the carry cocycle is closed form

For `Q0 -> Q2`, identify the kernel `N^3` with `F3^3` by

\[
 (a_1,a_2,a_3)\longmapsto(3a_1,3a_2,3a_3)\in(\mathbf Z/9)^3.
\]

Let `d:F3 -> {0,1,2} subset Z/9` be the fixed digit section, coordinate by
coordinate.  For quotient coordinates `(rbar,e)` choose

\[
 \sigma(\bar r,e)=(d(\bar r),e).                    \tag{5.1}
\]

If the second factor has parity `f`, (1.1) shows that the exact
multiplication cocycle is

\[
 \boxed{
 \omega((\bar r,e),(\bar s,f))
 =S(f)d(\bar r)+d(\bar s)
  -d(S(f)\bar r+\bar s\bmod3).}                     \tag{5.2}
\]

The right side is coordinatewise divisible by three; division by three and
reduction modulo three is the `C3^3` kernel coordinate.  Likewise the exact
crossed term of occurrence `j` is

\[
 \boxed{
 \kappa_j(\bar r,e)=M_jd(\bar r)+c_j(e)
 -d(M_j\bar r+c_j(e)\bmod3).}                       \tag{5.3}
\]

Again (5.3) is divisible by three and its quotient modulo three is the
kernel value.  Therefore the second extension also needs no learned or
enumerated cocycle table.

## 6. Truncated substitutions

For either elementary kernel put `u_i=t_i-1` (using `t_i^3` in the second
kernel).  Every column of every `M_j` has one entry `+1` or `-1`.  Hence the
full substitution required by v441 is only

\[
 u_i\longmapsto
 \begin{cases}
 u_{\sigma(i)},&M_je_i=+e_{\sigma(i)},\\
 (1+u_{\sigma(i)})^{-1}-1
   =2u_{\sigma(i)}+u_{\sigma(i)}^2,&M_je_i=-e_{\sigma(i)}.
 \end{cases}                                        \tag{6.1}
\]

There are no mixed-variable substitutions.  The crossed factors from
(3.2) or (5.3) must still be multiplied in full as products of
`(1+u_i)^a`; retaining only their linear terms would be unsound in grades
two through six.

## 7. Exact grade sizes and implementation consequence

The positive grade multiplicities are `(3,6,7,6,3,1)`.  For the first
extension, the occurrence/physical grade widths are therefore

```text
grade d          1       2        3        4       5       6
occurrence    72576  145152   169344   145152   72576   24192
physical      24192   48384    56448    48384   24192    8064
```

These are widths, not rank or time estimates.  At every grade the safe v441
order remains:

1. start from the same 44 literal seeds at precision `d+1`;
2. exhaust the four correlated actors in the complete occurrence module;
3. aggregate only afterwards;
4. perform lower-first/fibre elimination and test the actual residual;
5. on MEMBER, retain the literal update and all lower-kernel ancestry.

The affine formulas above allow every group product, inverse, occurrence,
prefix, filtration substitution and cocycle value to be computed from small
coordinates.  A future implementation must not replace occurrence-first
closure by physical closure, and must not materialize a generic 54,432- or
1,469,664-entry multiplication table.

## 8. Claim boundary

Conditional on independent replay of (1.2)--(3.2), the formerly abstract
twisting-data requirement in v441 is explicit for both R07 extensions.
What remains computational is membership of the six actual residuals in
each image fibre.

```text
ORDER-2016 LITERAL PAYLOAD:        EXTERNAL INPUT; NOT ADOPTED HERE
Q1 -> Q2 GROUP/COCYCLE DATA:       PAPER-EXPLICIT; AUDIT PENDING
Q2 -> Q0 GROUP/COCYCLE DATA:       PAPER-EXPLICIT; AUDIT PENDING
Q1 -> Q2 SIX GRADE TESTS:          NOT RUN
Q2 -> Q0 SIX GRADE TESTS:          NOT RUN
FULL-Q0 / A0 / COMMON / LIFT:      NOT DECIDED
FAKE / IHARA:                      NOT DECLARED
verified:                          false
```

`R07_A0_EXPLICIT_G9_TWO_RUNG_TWISTING_V442_CANDIDATE`
