# R07 word-independent successor and direct pair compiler v231

Author: Sol / 2026-08-28

Status: paper specialization of v188 and strengthening of the executable
form of v191.  The first diagonal successor kernel is independent of the
chosen task192 correction word and can be constructed as soon as the complete
task198 roof presentation is accepted.  A pointed ancestry written in the
resulting word-bearing kernel generators can then be expanded directly to a
roof-fibre word-pair polynomial without enumerating the successor group.
No actual roof presentation terminal, kernel, pointed multiplier, compatible
lift, fake certificate, or Ihara witness is declared.  `verified=false`.

## 1. The fixed ten-context successor

Let (F=F(x,y)).  The correctly typed task198 roof is the marked image

\[
 \rho_0:F\twoheadrightarrow\Delta_0
 \subseteq\prod_{j=0}^{9}E_{j,0}.
\tag{1.1}
\]

The ten factors use five E3 contexts and five E4 contexts.  Their source
substitutions are fixed before any correction word is selected:

\[
\begin{array}{c|cc}
 &X_j&Y_j\\ \hline
0&(x)&(y)\\
1&(x)&(z)\\
2&(y)&(z)\\
3&(u)&(x)\\
4&(u)&(y)\\
5&(A_{23})&(A_{34})\\
6&(A_{13}A_{12})&(A_{34}A_{24})\\
7&(A_{12})&(A_{23})\\
8&(A_{23}A_{13})&(A_{34})\\
9&(A_{12})&(A_{24}A_{23}),
\end{array}
\tag{1.2}
\]

where products in (1.2) are the internal words produced by the frozen
right-to-left paper-product convention,

\[
 z=\operatorname{PP}(x,y)^{-1},\qquad
 u=\operatorname{PP}(y,x)^{-1}.
\tag{1.3}
\]

The table is equivalently the task198 typed coordinate roster with context
IDs (21,22,23,24,25,1,27,21,26,28).  The E3 coordinate with context ID 21
and the E4 coordinate with the same registry number remain different types.
The repeated H1/H2 E3 occurrence is inserted only after this ten-coordinate
stage and does not create an eleventh acting factor.

For every factor let

\[
 E_{j,1}\twoheadrightarrow E_{j,0}
\tag{1.4}
\]

be the fixed first relative Frattini successor constructed from the complete
PB3 or PB4 presentation, and put

\[
 \rho_1:F\longrightarrow\prod_{j=0}^{9}E_{j,1}
\tag{1.5}
\]

by evaluating the same pairs (1.2).  Define

\[
 \Delta_1=\operatorname{im}\rho_1,\qquad
 V=\prod_{j=0}^{9}\ker(E_{j,1}\to E_{j,0}),\qquad
 K=\ker(\Delta_1\to\Delta_0).
\tag{1.6}
\]

Each factor of (V) is elementary abelian over (mathbf F_3), hence so is
(V) and its subgroup (K).  Equations (1.1)--(1.6) depend on the fixed
tower and context maps, not on (g_{760}), (c_{\rm exact}), or their
product.

## 2. Complete presentation defects determine K

Let the positive task198 presentation be

\[
 \Delta_0\cong
 \langle x,y\mid r_1,\ldots,r_{6441}\rangle
\tag{2.1}
\]

with every (r_j) retained as a literal signed (F(x,y))-word.  Put

\[
 b_j=\rho_1(r_j)\in V.
\tag{2.2}
\]

### Theorem 2.1 (WORD-INDEPENDENT COMPRESSED FIRST KERNEL)

\[
 \boxed{
 K=\mathbf F_3[\Delta_0]\langle b_1,\ldots,b_{6441}\rangle.}
\tag{2.3}
\]

The right side is computed by inserting the nonzero relator defects into a
sparse echelon and closing rank-raising rows under (x^{\pm1},y^{\pm1}).
Queue exhaustion returns a complete word-bearing basis of (K).  Neither a
task192 word nor a roster of (Delta_1) is required.

#### Proof

Let (R=\ker\rho_0).  Completeness of (2.1) gives

\[
 R=\langle\!\langle r_1,\ldots,r_{6441}\rangle\!\rangle_F.
\tag{2.4}
\]

Compatibility of (1.4)--(1.5) gives (K=\rho_1(R)).  The image of (R)
lies in the abelian group (V), so a conjugate has value

\[
 \rho_1(wr_j^{\epsilon}w^{-1})
 =\epsilon\,\rho_0(w)\cdot b_j.
\tag{2.5}
\]

Products of conjugates become sums in (V), proving (2.3).  Conversely every
translate in (2.3) is the image of a conjugated relator and hence lies in
(K).  The invariant queue is exactly the finite-dimensional closure of the
right side.  Retaining the same linear operations on the literal conjugated-
relator ancestries gives a source word for every basis value.  This is v188
Theorem 2.1 instantiated with the ten typed contexts. \(\square\)

### Corollary 2.2 (A4 MAY RUN BESIDE A2--A3)

After task198 production acceptance, A4 has no mathematical dependency on a
positive task192 correction or on the v216 pre-gate.  Its three milestones
remain presentation input, exhausted invariant closure, and independently
accepted word-bearing (K), but they may be executed in parallel with A2 and
A3.

#### Proof

Every datum in (1.1)--(2.3) is fixed by the tower, typed context maps, and roof
presentation.  The correction words enter later only when constructing the
named rows (d_1,e_1) for A5. \(\square\)

## 3. Pointed ancestry already has pair form

Let (k_1,\ldots,k_t\in K) be the word-bearing basis returned by Theorem
2.1, and choose its retained source words, again denoted (k_i\in F).  Thus

\[
 \rho_0(k_i)=1.
\tag{3.1}
\]

The A5 joint invariant closure begins with rows whose coefficient ancestry is
a finite sum of terms

\[
 g(k_i-1)=gk_i-g.
\tag{3.2}
\]

Every term in (3.2) is already a roof-fibre word pair because

\[
 \rho_0(gk_i)=\rho_0(g).
\tag{3.3}
\]

Suppose a positive A5 ancestry gives

\[
 e_1=\alpha d_1+\beta e_1,
 \qquad \alpha,\beta\in I_0,
\tag{3.4}
\]

where both coefficients are retained explicitly in the form (3.2).  The
v184 coefficient is

\[
 \mu_1=\left(\sum_{r=0}^{2t}\beta^r\right)\alpha
 \quad\hbox{in }\mathbf F_3[\Delta_1].
\tag{3.5}
\]

The order in (3.5) is noncommutative and is never reversed.

## 4. Direct word-pair compiler without a successor roster

Let (widetilde\alpha,widetilde\beta\in k[F]) be the literal source-word
sums supplied by the A5 ancestry and define

\[
 \boxed{
 M=\left(\sum_{r=0}^{2t}\widetilde\beta^{,r}\right)
       \widetilde\alpha\in k[F].}
\tag{4.1}
\]

### Theorem 4.1 (DIRECT ORDERED PAIR COMPILER)

The element (M) is finite, maps to (mu_1) in (k[\Delta_1]), and lies
in

\[
 J_0=\ker(k[F]\to k[\Delta_0]).
\tag{4.2}
\]

Moreover it can be converted to a finite literal normal form

\[
 \boxed{
 M=\sum_s a_s(U_s-V_s),\qquad
 \rho_0(U_s)=\rho_0(V_s),}
\tag{4.3}
\]

using only free-word multiplication/reduction and the compressed task198 roof
evaluator.  Equality or enumeration in (Delta_1) is not required.

#### Proof

The map (k[F]\to k[\Delta_1]) is a ring homomorphism.  Applying it to
(4.1) gives (3.5), so (M\mapsto\mu_1).  Both
(widetilde\alpha,widetilde\beta) lie in the two-sided ideal (J_0) by
(3.2)--(3.3).  Hence every summand of (4.1) lies in (J_0), proving (4.2).

Expression (4.1) is a finite sum of finite products.  Expand it in the fixed
left-to-right order, freely reduce each source word, and collect coefficients
modulo three.  Its image in (k[\Delta_0]) is zero, so the sum of
coefficients inside each roof fibre is zero.  Choosing one retained support
word in each nonempty fibre and subtracting it from the other support words
gives (4.3), exactly as in v191 Lemma 1.1.  The roof values needed for this
partition are supplied on demand by the compressed evaluator; no successor
state ID is used. \(\square\)

### Remark 4.2 (DAG execution)

Literal expansion of (4.1) may be large, but this is a resource issue rather
than a new search.  A production compiler may retain the ordered powers and
products as a lossless expression DAG, merge equal freely reduced source
words incrementally, and stream the final roof-fibre partition.  A resource
stop is `UNKNOWN_RESOURCE`.  It does not restore a need for a blind word
search or a complete (Delta_1) roster.

## 5. Revised dependency graph

The shortest dependency graph is therefore

```text
task198 positive roof presentation
          |
          v
A4: 6441 successor defects -> exhausted word-bearing K
          |                                  task192 + task193 actual d1,e1
          +-----------------------------------------------+
                                                          v
                                             A5 joint pointed membership
                                                          |
                                                          v
                                  A6 direct ordered pair compiler (4.1)
                                                          |
                                                          v
                                             A7 three exact PB endpoints.
```

Task226/A3 remains a useful early endpoint pre-gate.  A negative A3 dual
stops the fixed correction before A5, but A4 itself can already have been
computed and retained because it is word-independent.

## 6. Fixed frontier

```text
TEN-TYPED FIRST SUCCESSOR IS WORD-INDEPENDENT:       PAPER PROOF
6441 RELATOR DEFECTS GENERATE COMPLETE K:            PAPER PROOF / v188
A4 MAY RUN AFTER A1 WITHOUT A0/A2/A3:                PAPER PROOF
A5 ANCESTRY TERMS g(k_i-1) ARE ROOF-FIBRE PAIRS:     PAPER PROOF
ORDERED NEUMANN COEFFICIENT -> FINITE M IN J0:        PAPER PROOF
SUCCESSOR ROSTER NEEDED FOR A6 PAIR COMPILATION:     REMOVED
ACTUAL TASK198 PRESENTATION INPUT:                    RUNNING / NOT ACCEPTED
ACTUAL WORD-BEARING K:                               NOT COMPUTED
ACTUAL d1,e1 / POINTED ANCESTRY:                     NOT COMPUTED
ACTUAL M / THREE EXACT ENDPOINTS:                    NOT COMPUTED
COMPATIBLE LIFT / FAKE / IHARA:                      NOT CONSTRUCTED
```

`R07_WORD_INDEPENDENT_SUCCESSOR_AND_DIRECT_PAIR_COMPILER_V231_PAPER_GRADE`
