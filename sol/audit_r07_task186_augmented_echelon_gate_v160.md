# R07 task186 normalized augmented-echelon gate v160

Author: Sol / 2026-08-27

Status: mathematical implementation audit and no-repeat contract.  This note
does not report a machine run or a common word.  It records why the first two
task186 implementations were rejected and states the exact certificate which
can be promoted.  No compatible cofinal lift, fake, or Ihara witness is
declared.

## 1. The actual finite system

Let \(C\) be the finite-field coefficient space on word-bearing correction
columns and let \(D\) be the coefficient space on the separately typed
PB3/PB4 boundary columns.  Put

\[
 E=C\oplus D .
\tag{1.1}
\]

The raw all-seven map and the normalized exponent map are

\[
 A:E\longrightarrow V,\qquad
 N:E\longrightarrow {\bf F}_3^2 ,
\tag{1.2}
\]

where \(N\) is

\[
 N(c,d)=\frac{\epsilon(c)}{18}\bmod 3
\tag{1.3}
\]

and is zero on every boundary coordinate.  V156 proves that division by 18
is integral on every registered correction column.  The exact first-edge
membership problem is

\[
 \boxed{(A,N)e=(t,0).}
\tag{1.4}
\]

Thus the two normalized coordinates are rows of the same sparse column
matrix used by the boundary/correction oracle, dual construction, pivot
test, coefficient recovery, and checkpoint.  Recording them in a side list
while solving only \(Ae=t\) does not implement (1.4).

## 2. Rank difference and what it does not permit

Write

\[
 r=\operatorname{rank}A,\qquad
 \widetilde r=\operatorname{rank}(A,N).
\tag{2.1}
\]

### Proposition 2.1 (KERNEL-RESIDUE RANK IDENTITY)

\[
 \boxed{\widetilde r-r=\dim_{\mathbf F_3}N(\ker A).}
\tag{2.2}
\]

#### Proof

Projection from \(\operatorname{im}(A,N)\) to \(\operatorname{im}A\) is
onto.  Its kernel consists exactly of pairs \((0,N(e))\) with
\(e\in\ker A\), and is therefore naturally isomorphic to
\(N(\ker A)\).  Taking dimensions proves (2.2). \(\square\)

Equation (2.2) must be computed from the retained combined columns.  It is
invalid to set

\[
 \widetilde r=r+\operatorname{rank}\{\nu(u_0),\nu(v_0)\}
\tag{2.3}
\]

unless coefficient identities proving \(u_0,v_0\in\ker A\) have first been
materialized.  V156 proves only that \(u_0,v_0\) form an exponent-lattice
basis in the joint kernel.  It does not assert that their all-seven change
is zero.

If the computed difference in (2.2) is two, every nonempty raw relation
fibre \(A^{-1}(t)\) contains all normalized exponent residues, hence contains
a point with residue zero.  If it is one, the possible residues form one
affine line; if it is zero, every point in the fibre has the same residue.
No dimension may be promoted without word-bearing kernel preimages.

## 3. Required word-bearing kernel certificate

The elimination must retain coefficient ancestry.  For every basis vector
of \(N(\ker A)\), the receipt must print one vector

\[
 e_i=(c_i,d_i)\in C\oplus D
\tag{3.1}
\]

and independently replay

\[
 A(c_i,d_i)=0,\qquad
 N(c_i,d_i)=q_i .
\tag{3.2}
\]

The source word is formed from \(c_i\) only.  Coefficient two is a literal
inverse.  The boundary coefficients \(d_i\) are retained as a quotient
certificate and are never multiplied into the source word.  The checker
must reconstruct the complete column combination, the source word, its
joint-kernel value, integer exponent, normalized residue, and zero raw
all-seven change.

This is the missing information behind the phrase word-bearing preimage in
v159.  A pair of abstract residue vectors without their coefficient
ancestry is not a selector.

## 4. Positive word and exactification

Because (1.4) targets zero in the normalized coordinates, a positive
coefficient solution materializes \(c_*\) with

\[
 \epsilon(c_*)\in54{\bf Z}^2.
\tag{4.1}
\]

Write \(\epsilon(c_*)=(54a,54b)\).  With the registered literal words of
v156,

\[
 v_0=r_9r_{12}r_3^{-2},\qquad
 u_0=r_9v_0^{-8},
\tag{4.2}
\]

put

\[
 h=u_0^{-3a}v_0^{-3b},\qquad
 c_{\rm exact}=c_*h.
\tag{4.3}
\]

The producer and checker must then replay the final word, not merely its
integer exponent:

1. \(c_{\rm exact}\) has exact exponent \((0,0)\);
2. it is in the registered joint kernel;
3. its first-rung all-seven change equals that of \(c_*\);
4. \(g_{760}c_{\rm exact}\) uses right multiplication;
5. both literal hexagons and the printed-order five-factor pentagon pass;
6. every mark, reduction, and onto side gate inherited from task179 passes;
7. no boundary word occurs in \(c_{\rm exact}\).

Characteristic three explains why the cubes preserve the first-rung change,
but it does not replace these literal replays.

## 5. Audit of the two rejected implementations

The first delivery had identities

~~~text
producer  10245  42724668c02a665eca24e5413148b5bcfdc5a3d9be7925d69c57d5d1e0c998d3
checker    8003  9f6059d21a02bec8f696e0156960058f4935fc96966ed8446043e7997c4e9022
driver     5479  6534bd2bb1a5ea3708a919786b5d770c65be81af4a1a5561cc234030065573df
~~~

and returned a predetermined UNKNOWN_INPUT without running the 6,441-word
schedule.  It was rejected as a static exactifier, not a column generator.

The second delivery had identities

~~~text
producer  20135  f376a6bd9fa8f44c835a53cdbbf413e4b1aa4e25c9e55edd7d634bbe9bfd9839
checker   13090  98f9de6306a23edd221c8ca65c2b24961fc1eb8721b47de79a0321ab5cc599d7
driver     5898  04bc5b72d8bef46911e2a96ff86e26ba7e0a775d6b5a9af0162bd3431bffea3d
~~~

and did execute the authenticated v1 schedule.  However its patched
add-column function appended the normalized pair only to a side list and
passed the original raw row unchanged to the v1 echelon.  The search,
dual, target reduction, and recovered solution therefore remained the
v1 raw-mod-three calculation.  It also used (2.3) without proving
\(u_0,v_0\in\ker A\).  It was rejected before GHA dispatch.

## 6. Executable promotion gate

A repaired task186 bundle may be dispatched only if static audit shows:

1. normalized exponent semantics occur in the actual sparse E1/E2 row keys
   before every pivot, dual, oracle scalar, target reduction, and coefficient
   recovery;
2. a fresh v2 checkpoint is the default and any resume is fully replayed
   under those semantics;
3. stripped and augmented ranks are recomputed from retained columns;
4. kernel-residue basis vectors carry complete coefficient and word ancestry;
5. positive exactification ends in the literal replays of Section 4;
6. the helper-nonshared checker independently reconstructs items 1--5; and
7. SELFTEST contains a case whose membership answer changes when normalized
   rows replace the vacuous raw rows.

Only after this static gate passes may the parent run the GHA SELFTEST, and
only after that artifact passes may production be dispatched.

~~~text
TASK179 RAW EXPONENT ROWS:                 PROVED VACUOUS
NORMALIZED AUGMENTED CRITERION:            PAPER PROOF
FIRST TASK186 DELIVERY:                    REJECTED STUB
SECOND TASK186 DELIVERY:                   REJECTED UNCOUPLED ROWS
THIRD REPAIR:                              IN PROGRESS
GHA TASK186 SELFTEST / PRODUCTION:         NOT DISPATCHED
EXACT FIRST-EDGE COMMON WORD:              NOT YET CONSTRUCTED
COMPATIBLE COFINAL LIFT / FAKE / IHARA:    NOT DECLARED
~~~

R07_TASK186_NORMALIZED_AUGMENTED_ECHELON_GATE_V160
