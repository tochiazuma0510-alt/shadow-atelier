# R07 task179 exact exponent lattice and normalized two-row repair v156

Author: Sol / 2026-08-27

Status: paper proof and exact audit of the authenticated 6,441-word normal
presentation used by task175/task179.  The exponent lattice of the registered
joint kernel is \(18\mathbf Z^2\).  Consequently task179's present raw
exponent-sum rows modulo three vanish on every correction column and impose no
condition.  The correct two rows are the coordinates after division by the
canonical lattice basis \(18e_x,18e_y\), reduced modulo three.  This note does
not assume that the running task179 search returns `COMMON_WORD`, and it does
not declare a second-rung lift, a cofinal lift, fake, or an Ihara witness.

## 1. Frozen kernel presentation

Let

\[
 F=F(x,y)\twoheadrightarrow G_{\rm joint},\qquad
 \Omega=\ker(F\twoheadrightarrow G_{\rm joint}).
\tag{1.1}
\]

The authenticated task175/task179 presentation has 6,441 literal kernel
words, in the three ordered layers

\[
 6318\ \text{Gamma edges},\qquad
 104\ \text{(x/y)-action rows},\qquad
 19\ \text{Q0-defect rows}.
\tag{1.2}
\]

They normally generate \(\Omega\).  The inputs used below are exactly:

* `ci/b345_157ee_artifacts_32359956713/d972_b345_q3_chief_v1.json`,
  231,570 bytes, SHA-256
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`;
* `ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json`,
  2,166,036 bytes, SHA-256
  `1c3ad7a7124cee152eb40968cf212c14641a9f8720063c85f70533864898d0df`;
* `search/d972_b345_joint_kernel_qstar_closure_v1.py`, 67,945 bytes,
  SHA-256
  `06ba6cf361957db3e339d48d14b3d4fbc689de9642e3f96273fbe8f3160e76dc`;
  and
* the lossless roster constructor
  `search/d972_r07_full_e4_joint_orbit_preflight_v7.py`, 21,918 bytes,
  SHA-256
  `92701bb1ed84de9b9aa0fb8a986197f76b86e1f42af83ee18319700be0647eed`.

Write

\[
 \epsilon:F\longrightarrow F^{\rm ab}=\mathbf Z^2
\tag{1.3}
\]

for the signed \((x,y)\)-exponent vector.  By invariance under conjugation
and normal generation,

\[
 L:=\epsilon(\Omega)
   =\sum_{r\in\mathcal R_{6441}}\mathbf Z\epsilon(r).
\tag{1.4}
\]

Thus no group enumeration is needed to determine \(L\); only the recorded
section tree and integer exponent sums are used.

## 2. Lossless exponent reconstruction

The 26 nonidentity Gamma record words have the following exponent vectors,
in their frozen order:

\[
\begin{split}
 &(24,0),(12,0),(12,4),(0,4),(-12,4),(0,8),(-12,8),(-24,8),\\
 &(-8,0),(16,0),(4,0),(16,4),(4,4),(-8,4),(4,8),(-8,8),\\
 &(-20,8),(-4,0),(20,0),(8,0),(8,4),(-4,4),(-16,4),\\
 &(8,8),(-4,8),(-16,8).
\end{split}
\tag{2.1}
\]

Let \(t_s\) be the section word of Gamma state \(s\), reconstructed from
the packed parent-state and parent-generator arrays in the joint receipt, and
put \(a_s=\epsilon(t_s)\).  Decode the packed transition target
\(s\cdot j\) with the documented one-based public convention.  The exponent
rows are then reproduced without evaluating a group word:

\[
\begin{aligned}
 e^{\rm edge}_{s,j}&=a_s+\epsilon(w_j)-a_{s\cdot j},\\
 e^{\rm act}_{j,k,\pm}&=\epsilon(w_j)-a_{u(j,k,\pm)},\\
 e^{\rm Q0}_i&=\epsilon(q_i)-a_{v(i)}.
\end{aligned}
\tag{2.2}
\]

The conjugating \(x\)- or \(y\)-letters cancel in the second line.  The
targets \(u(j,k,\pm)\) and \(v(i)\) are the fourth entry of each action row
and the third entry of each Q0 row, respectively, again converted from the
one-based public state number.

For an independent check of the last line, the four split words have

\[
 (0,-8),\quad(0,4),\quad(1,8),\quad(0,-3).
\tag{2.3}
\]

Substituting them in the five PSL and eight G9 presentation relators gives

\[
\begin{split}
 &(0,-40),(0,-48),(0,36),(0,52),(0,8),\\
 &(0,-12),(-4,-32),(0,-54),(18,144),(4,74),(4,8),\\
 &(-10,-50),(18,144),
\end{split}
\tag{2.4}
\]

followed by four cross-commutators and two splitting rows of exponent
\((0,0)\).  Equations (2.1)--(2.4) are a complete integer reconstruction of
all 6,441 vectors.

After deduplication their exact set is

\[
\begin{split}
\mathcal E=\{&
 (0,0),(-36,0),(36,0),(-72,0),(72,0),\\
 &(0,-36),(0,36),(0,-54),(0,54),(0,-72),\\
 &(-36,-36),(-36,36),(36,36),(-72,36),\\
 &(-18,-54),(18,144)\}.
\end{split}
\tag{2.5}
\]

The count check is

\[
 6318+104+19=6441,
\tag{2.6}
\]

and (2.5) has 16 distinct vectors.  This is also an immediate compact
reproduction rule for the numerical claim: apply (2.2) to the two packed
arrays and the target columns, using (2.1) and (2.4), then sort unique pairs.

An independent static replay checked every one-based convention against the
producer source and reproduced all 19 complete-relator lengths and their
canonical SHA-256.  In particular, if \(r_i\) denotes the registered lifted
Q0-defect word in ordinal row \(i\), that replay gives

\[
 \epsilon(r_3)=(0,36),\qquad
 \epsilon(r_9)=(18,144),\qquad
 \epsilon(r_{12})=(-18,-54).
\tag{2.7}
\]

## 3. Exact lattice theorem

### Theorem 3.1 (TASK179 KERNEL EXPONENT LATTICE)

For the registered joint kernel (1.1),

\[
 \boxed{L=18\mathbf Z\oplus18\mathbf Z.}
\tag{3.1}
\]

Equivalently,

\[
 G_{\rm joint}^{\rm ab}\cong
 \mathbf Z^2/L\cong C_{18}\times C_{18}.
\tag{3.2}
\]

#### Proof

Every coordinate in (2.5) is divisible by 18, so

\[
 L\leq18\mathbf Z^2.
\tag{3.3}
\]

Conversely, the three named words in (2.7) give literal kernel words

\[
 v_0=r_9r_{12}r_3^{-2},\qquad
 u_0=r_9v_0^{-8}
\tag{3.4}
\]

with

\[
 \epsilon(v_0)=(0,18),\qquad
 \epsilon(u_0)=(18,0).
\tag{3.5}
\]

They generate \(18\mathbf Z^2\), proving (3.1).  Equation (3.2) follows from
(1.4).  As a Smith consistency check, the gcd of all
coordinates is 18 and the gcd of all \(2\times2\) minors is
\(324=18^2\). \(\square\)

This corrects the tempting inference from the coarse quotient
\(Q0^{\rm ab}\cong C_2^2\).  The Gamma extension contributes the 3-primary
part of (3.2); the exponent lattice is not an index-four lattice.

## 4. The present task179 exponent rows are zero rows

Task179 currently appends

\[
 \epsilon(r)\bmod3\in\mathbf F_3^2
\tag{4.1}
\]

to every conjugated roster column.  Conjugation leaves \(\epsilon(r)\)
unchanged.  Theorem 3.1 gives

\[
 \epsilon(r)\in18\mathbf Z^2\subseteq3\mathbf Z^2,
\tag{4.2}
\]

so both appended entries are zero for every one of the 6,441 roster rows
and every orbit translate.  PB3/PB4 boundary columns have no source-word
exponent coordinate, and the frozen \(g_{760}\) target has exact exponent
\((0,0)\).  Therefore:

### Corollary 4.1 (RAW MOD-3 ROWS ARE VACUOUS)

Deleting task179's two current standard exponent rows leaves exactly the
same sparse linear system, rank, duals, retained columns, and possible
`COMMON_WORD` coefficient solutions.

In particular, acceptance of the current check
`exponent_pair(correction_word)==(0,0)` proves no extra charmingness
condition beyond membership in \(\Omega\).  Every kernel correction already
has raw exponent zero modulo three.

## 5. Exact zero-cost cube repair

Let a future authenticated task179 positive receipt materialize a correction
word \(c_*\in\Omega\).  Theorem 3.1 gives unique integers \(a,b\) with

\[
 \epsilon(c_*)=(18a,18b).
\tag{5.1}
\]

V146's cube repair preserves the characteristic-three all-seven change
class and can change the exponent precisely by \(3L\).  Here

\[
 3L=54\mathbf Z^2.
\tag{5.2}
\]

### Theorem 5.1 (ZERO-COST REPAIR DECISION)

The displayed task179 coefficient solution is repairable to an exact
commutator by registered roster cubes, without another orbit search, if and
only if

\[
 \boxed{\epsilon(c_*)\in54\mathbf Z^2.}
\tag{5.3}
\]

Equivalently, both \(a\) and \(b\) in (5.1) must vanish modulo three.

#### Proof

Every product of roster cubes has exponent in \(3L\), proving necessity.
For sufficiency, use the literal words \(u_0,v_0\in\Omega\) from (3.4), with

\[
 \epsilon(u_0)=(18,0),\qquad\epsilon(v_0)=(0,18).
\tag{5.4}
\]

If \(\epsilon(c_*)=(54A,54B)\), put

\[
 h=u_0^{-3A}v_0^{-3B},\qquad c=c_*h.
\tag{5.5}
\]

Then \(\epsilon(c)=(0,0)\).  The all-seven change map is additive over
\(\mathbf F_3\), so the third powers in \(h\) have zero change class.
Thus \(c\) has the same first-rung relation solution as \(c_*\). \(\square\)

If (5.3) fails, only this particular coefficient solution fails the
zero-cost cube test.  It is not a nonexistence result for the whole
task179 correction fibre.

## 6. The correct normalized two rows

With the canonical basis in (3.1), define

\[
 \nu:L\longrightarrow L/3L\cong\mathbf F_3^2,
 \qquad
 \nu(18a,18b)=(a,b)\bmod3.
\tag{6.1}
\]

The complete exact-commutator system of v146 is obtained by appending
\(\nu(\epsilon(r))\), not \(\epsilon(r)\bmod3\), to each correction
column and appending zero to each boundary column.  The target is zero.
For example three roster vectors from (2.5) have normalized residues

\[
 (18,144)\mapsto(1,2),\qquad
 (0,36)\mapsto(0,2),\qquad
 (0,54)\mapsto(0,0).
\tag{6.2}
\]

The normalized columns span \(L/3L\), as the explicit basis (3.5) also
shows.  V146 Theorem
2.1 now gives the exact equivalence

\[
 \boxed{
 \text{exact-commutator common correction exists}
 \Longleftrightarrow
 (-T_0,0)\text{ belongs to the normalized augmented span}.}
\tag{6.3}
\]

Thus the successor after a positive current task179 receipt is completely
decided:

1. compute its integer exponent vector from the printed literal word;
2. if it is \((0,0)\), accept it unchanged;
3. if it lies in \(54\mathbf Z^2\), apply (5.5) and replay the final word;
4. otherwise preserve the positive checkpoint and resume column generation
   with exactly the two normalized rows (6.1).

No new Delta enumeration and no dense homogeneous-kernel search is needed.
The checked-in task184 static-stop bundle must not be run as a substitute for
this normalized resume.

```text
COMPLETE 6441 EXPONENT-PAIR RECONSTRUCTION:           PAPER_AUDIT
EXACT JOINT-KERNEL EXPONENT LATTICE L:                18 Z^2 / PAPER_PROOF
CURRENT TASK179 RAW MOD-3 EXPONENT ROWS:              IDENTICALLY ZERO
ZERO-COST CUBE REPAIR LATTICE 3L:                     54 Z^2
CORRECT AUGMENTED ROWS:                               (exp/18) mod 3
TASK179 COMMON_WORD INTEGER EXPONENT:                 PENDING PRODUCTION
NORMALIZED LATTICE-AUGMENTED RESUME:                  NOT IMPLEMENTED
EXACT-COMMUTATOR FIRST FRATTINI WORD:                 NOT YET CONSTRUCTED
SECOND RUNG / COMPATIBLE COFINAL LIFT / FAKE / IHARA: NOT DECLARED
```

`R07_TASK179_EXACT_EXPONENT_LATTICE_V156_PAPER_GRADE`
