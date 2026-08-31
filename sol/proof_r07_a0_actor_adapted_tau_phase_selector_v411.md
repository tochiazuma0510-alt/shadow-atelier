# R07 A0 actor-adapted tau phase selector (v411)

Author: Sol / 2026-08-31

Status: paper implementation theorem strengthening v409--v410.  It removes
the `NONZERO_TAU_GATE`: the three global `tau` coordinates never require a
dense adjoint.  One PB3 transversal is changed by an exact coordinate
isomorphism, while the accepted PB4 transversal is retained.  The resulting
tau contribution is constant on three explicitly generated exponent cells.
No A0 terminal, common word, compatible lift, fake, or Ihara witness is
asserted.  `verified=false`.

## 1. Central splittings adapted to the actual actors

Use the frozen marked orders

\[
 (a,b,c)=(A_{12},A_{13},A_{23})\quad(PB3)
\tag{1.1}
\]

and

\[
 (a,b,p,c,q,r)=(A_{12},A_{13},A_{14},A_{23},A_{24},A_{34})\quad(PB4).
\tag{1.2}
\]

The first three PB3 and first six PB4 PC coordinates are their independent
abelian coordinates.  Hence the coordinate functionals

\[
 \kappa_3=\text{the }b\text{-coordinate},
 \qquad
 \kappa_4=\text{the }a\text{-coordinate}
\tag{1.3}
\]

are homomorphisms to \(\mathbf F_3\).  For the central elements

\[
 z_3=abc,
 \qquad
 z_4=abpcqr,
\tag{1.4}
\]

the frozen finite gates give central order three and

\[
 \kappa_m(z_m)=1.
\tag{1.5}
\]

Put \(H_{m,0}=\ker\kappa_m\).  Every \(h\in H_m\) has the unique form

\[
 h=h_0z_m^{\kappa_m(h)},\qquad h_0\in H_{m,0},
\tag{1.6}
\]

and therefore

\[
 \boxed{H_m=H_{m,0}\times\langle z_m\rangle.}
\tag{1.7}
\]

For PB4 this is the already accepted v402 splitting.  For PB3, v401 used a
least-serialization transversal only for convenience.  Replacing it by
\(H_{3,0}\) changes quotient coordinates by an invertible orbitwise linear
map and does not change the kernel of the normal map.  The v401 proof uses
only that one representative is chosen from every central three-orbit, so
its equality \(\ker N_3=D_3\) remains unchanged.

The PB3 implementation must independently check that the selected PC
coordinate is additive on every PC power/conjugate relation, that (1.5)
holds, and that (1.6) reconstructs every element it touches.  No subgroup or
group roster is enumerated.

## 2. The eleven actors have only one phase bit

For occurrence \(o\), source conjugation acts by

\[
 w_o(\delta)=P_o\pi_o(\delta)P_o^{-1}.
\tag{2.1}
\]

Since \(\kappa_m\) is a homomorphism to an abelian group, the prefix drops
out:

\[
 \kappa_m(w_o(\delta))=\kappa_m(\pi_o(\delta)).
\tag{2.2}
\]

All six PB3 substitutions are words in the embedded free generators
\(a=A_{12}\) and \(c=A_{23}\).  Both have \(\kappa_3=0\), so

\[
 \boxed{\kappa_3(w_o(\delta))=0\quad\text{for every PB3 occurrence}.}
\tag{2.3}
\]

For PB4, read the five frozen `pcontexts` literally.  Only marked generator
\(a=A_{12}\) has nonzero \(\kappa_4\).  The resulting table is

| occurrence | natural context | \(\kappa_4(\text{left})\) | \(\kappa_4(\text{right})\) | actor phase |
|---|---:|---:|---:|---:|
| `P_b1` | 1 | 0 | 0 | 0 |
| `P_b2` | 3 | 1 | 0 | \(\epsilon_x(\delta)\) |
| `P_b3` | 0 | 1 | 0 | \(\epsilon_x(\delta)\) |
| `P_b5_inverse` | 2 | 0 | 0 | 0 |
| `P_b4_inverse` | 4 | 1 | 0 | \(\epsilon_x(\delta)\) |

Here

\[
 \epsilon_x(\delta)=\operatorname{exp}_x(u_\delta)\pmod3.
\tag{2.4}
\]

The sign of an inverse occurrence changes the Fox row, not (2.2).  Thus all
eleven actor phases are determined by the single residue (2.4).

## 3. A global tau functional needs only three evaluations

For either split write the central survivor on one orbit as

\[
 (U_0(h_0),U_1(h_0),Z_2'(h_0)),\qquad
 \tau=\sum_{h_0\in H_{m,0}}Z_2'(h_0).
\tag{3.1}
\]

### Lemma 3.1 (TAU PHASE COMPRESSION)

For every raw row \(v\), \(t_0\in H_{m,0}\), and
\(e\in\{0,1,2\}\),

\[
 \boxed{
 \tau\bigl(N_mL_{t_0z_m^e}v\bigr)
 =\tau\bigl(N_mL_{z_m^e}v\bigr).}
\tag{3.2}
\]

Consequently the complete dependence of the global functional on a left
actor is obtained by applying the direct normal map to only the three rows
\(v,L_{z_m}v,L_{z_m^2}v\).

#### Proof

The full boundary space is invariant under left translation, so the normal
map induces the quotient action.  In the split coordinates, left
multiplication by \(t_0\) permutes the orbit representatives \(h_0\) and
applies the same permutation to every noncentral and central correction.
It does not change the central phase.  The sum in (3.1) is invariant under
this permutation, proving (3.2).  This argument applies after the triangular
noncentral elimination as well as before it; no assumption that an individual
new noncentral generator lies in \(H_{m,0}\) is used.  \(\square\)

Let \(\lambda\) be a physical quotient dual.  Remove its three `tau`
coefficients and call the remainder \(\lambda_{\rm loc}\).  By v410,
\(N^*\lambda_{\rm loc}\) is obtained with at most

\[
 15s_3+33s_4
\tag{3.3}
\]

raw singleton evaluations.  For compact seed \(i\), evaluate the tau part
of each base occurrence by Lemma 3.1 and merge it with the exponent constant.
Equations (2.3)--(2.4) then give the exact formula

\[
 \boxed{
 F_i(\delta)=K_{i,\epsilon_x(\delta)}+
 \sum_{(j,t)\in R_i}c^{(i)}_{j,t}
       {\bf1}_{\pi_j(\delta)=t}.}
\tag{3.4}
\]

The three values \(K_{i,0},K_{i,1},K_{i,2}\) include every PB3/PB4 tau
coefficient.  In particular, a nonzero tau coefficient creates three scalar
entries, not a dense raw vector.

### Theorem 3.2 (FULL ADJOINT FORMULA WITHOUT DENSE TAU)

Formula (3.4) equals
\(\langle\lambda,\bar C_i(\delta)\rangle\) for every dual, including all
three nonzero tau cases.  Its compiler uses the local bound (3.3), the finite
Tietze-expanded base gradients, and at most three direct central translations
per tau-bearing occurrence.  It enumerates no E3, E4, Q0, Delta, PB3, PB4,
or occurrence roster.

#### Proof

Split the pairing into exponent, localized, and tau functionals.  The first
is invariant under conjugation.  V410 gives the localized indicator sum.
Lemma 3.1 and the actor-phase table give the three tau constants.  These are
all coordinates of the physical quotient, so their sum is the complete
pairing.  \(\square\)

## 4. Exact selector on the three exponent cells

The compact presentation satisfies

\[
 \ker\Theta=\langle\!\langle\mathcal R_{\rm pc}\rangle\!\rangle,
\tag{4.1}
\]

and every compact relator has both exponent sums divisible by 18.  Therefore
\(\epsilon_x\) factors through \(\Delta\).  It is onto because the image of
\(x\) is one.  Hence the cells

\[
 C_e=\{\delta\in\Delta:\epsilon_x(\delta)=e\}
\tag{4.2}
\]

all have the exact size

\[
 \boxed{|C_e|=|\Delta|/3=119{,}042{,}784.}
\tag{4.3}
\]

For the localized support union of (3.4), completely enumerate each
nonempty singleton fibre with v142 and the task176 kernel generators.  Sort
the returned literal states by (4.2), and let \(W_e\) be the corresponding
union-bound count in cell \(C_e\).  Thus

\[
 |U\cap C_e|\leq W_e.
\tag{4.4}
\]

### Theorem 4.1 (PHASE-CELL WEIGHTED SELECTOR)

For every \(e\in\mathbf F_3\):

1. if \(K_{i,e}=0\), complete evaluation of the enumerated support fibres
   in \(C_e\) finds a nonzero value exactly when one exists in that cell;
2. if \(K_{i,e}\ne0\) and \(W_e<|C_e|\), evaluation on any \(W_e+1\)
   distinct states of \(C_e\) must find a nonzero value; and
3. exhaustion of all three cells proves \(F_i\equiv0\).

#### Proof

Outside \(U\cap C_e\), formula (3.4) equals the constant \(K_{i,e}\).
The proof is therefore the v143 union-bound argument applied separately to
each cell, using (4.3)--(4.4).  \(\square\)

No full cell roster must be built.  Reidemeister--Schreier gives the
word-bearing kernel generators

\[
 x^3,\qquad y,\qquad xyx^{-1},\qquad x^2yx^{-2}
\tag{4.5}
\]

for \(\ker(\operatorname{exp}_x\bmod3)\) in the free group.  Their images
generate \(\ker\epsilon_x\leq\Delta\), because (4.1) lies in that kernel.
A duplicate-checking BFS in these four generators and inverses emits exactly
as many distinct kernel states as requested; left multiplication by \(x^e\)
emits states of \(C_e\).  The selector stops after \(W_e+1\), never after
enumerating the cell.  A resource cap is `UNKNOWN_RESOURCE`, not an empty
cell or zero formula.

Every ACTIVE state is still accepted only after a literal section-word
replay, all ten linked coordinates, all eleven raw Fox occurrences, the
direct normal maps, and the direct dual scalar.

## 5. Consequence for A0

Combine the unchanged v404 six-action oracle with Theorems 3.2 and 4.1.
At each nonzero remainder dual:

1. insert a v404 ACTIVE row if one exists;
2. otherwise compile (3.4) for the at-most-44 compact seeds;
3. insert the first phase-cell ACTIVE correction and repeat; or
4. if every complete formula is zero, return the same dual as an exact
   separator of the full A0 right side.

Every insertion pairs nontrivially with the current dual and therefore raises
physical rank.  Finite dimensionality gives the same termination proof as
v409, now without a tau exception.

```text
OLD OCCURRENCE-CLOSURE UPPER BOUND:     58,569,049,736 / NO-GO PATH
PB3 TRANSVERSAL:                        ACTOR-ADAPTED SPLIT, NO ROSTER
LOCAL ADJOINT:                          <= 15*s3 + 33*s4
GLOBAL TAU ADJOINT:                     NEVER MATERIALIZED
TAU DEPENDENCE:                         THREE exp_x mod 3 CONSTANTS
PHASE-CELL SIZE:                        119,042,784 EACH
FULL COMPACT CORRECTION ORACLE:         FINITE PHASE-CELL v143
ACTUAL A0 MEMBER/NONMEMBER:             NOT YET COMPUTED
COMMON / FAKE / IHARA WITNESS:          NONE
```

`R07_A0_ACTOR_ADAPTED_TAU_PHASE_SELECTOR_V411_PAPER_GRADE`
