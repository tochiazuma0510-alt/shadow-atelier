# R07 cubic-moment exact resource cap v136

Author: Sol / 2026-08-27

Status: paper proof and executable bound.  This note specializes v134 to the
frozen all-seven R07 occurrence arity.  It proves that exact cubic-moment
arithmetic is small; the remaining production difficulty is the authenticated
multi-projection membership oracle.  No common correction, cofinal lift,
fake, or Ihara witness is declared.

## 1. Frozen arity

For one normal-generator row, the two hexagons and ordered pentagon contain
eleven typed correction occurrences in ten context coordinates.  After a
dual is applied and equal targets in one coordinate are merged over
\(\mathbf F_3\), let \(T_i\) be the nonzero target support in coordinate
\(i\).  Cancellation can only decrease support, hence

\[
 s_i:=|T_i|\ge0,
 \qquad \sum_{i=1}^{10}s_i\le11.
\tag{1.1}
\]

V134 Theorem 3.1 has exactly

\[
 \prod_{i=1}^{10}(1+s_i)
\tag{1.2}
\]

raw partial-projection terms.

## 2. Sharp term cap

### Theorem 2.1 (ELEVEN-OCCURRENCE MOMENT CAP)

Under (1.1),

\[
 \boxed{
 \prod_{i=1}^{10}(1+s_i)\le 3\cdot2^9=1536.}
\tag{2.1}
\]

Equality occurs, up to coordinate order, at

\[
 (s_1,\ldots,s_{10})=(2,1,1,1,1,1,1,1,1,1).
\tag{2.2}
\]

#### Proof

First use the whole available sum: increasing any \(s_i\) increases the
product.  If a coordinate is zero and another has value \(a\ge2\), replacing
\((0,a)\) by \((1,a-1)\) changes their factor from \(a+1\) to \(2a\), and
\(2a\ge a+1\).  Thus a maximizer with sum eleven has all ten coordinates
positive.

If two positive entries satisfy \(a\ge b+2\), replacing \((a,b)\) by
\((a-1,b+1)\) changes the factor product by

\[
 a(b+2)-(a+1)(b+1)=a-b-1>0.
\tag{2.3}
\]

Hence the entries of a maximizer differ by at most one.  Ten positive
integers with sum eleven must therefore be nine ones and one two, giving
(2.1)--(2.2).  If the sum is smaller than eleven, monotonicity gives the
same upper bound. \(\square\)

For all 6,441 frozen normal-generator rows, one dual iteration therefore has
at most

\[
 \boxed{6441\cdot1536=9{,}893{,}376}
\tag{2.4}
\]

raw Eisenstein terms before identical partial assignments are cached or
merged.  The ordered coordinate subsets themselves number at most
\(2^{10}=1024\), globally across every row and dual.

## 3. Signed 64-bit safety

Represent \(A+B\omega\) by the pair \((A,B)\), and put

\[
 \|(A,B)\|_1=|A|+|B|.
\tag{3.1}
\]

The two nontrivial factors in v134 are

\[
 \omega-1=(-1,1),
 \qquad \omega^2-1=(-2,-1).
\tag{3.2}
\]

Direct use of the exact multiplication law gives

\[
 \|x(\omega-1)\|_1\le3\|x\|_1,
 \qquad
 \|x(\omega^2-1)\|_1\le3\|x\|_1.
\tag{3.3}
\]

Multiplication by \(\omega^K\), \(K\in\mathbf F_3\), increases this norm by
at most a factor two.  Since one raw term contains at most ten factors, and
every fibre count is at most

\[
 |\Delta|\le |G|=243\cdot1{,}469{,}664=357{,}128{,}352,
\tag{3.4}
\]

the norm of the final accumulator is conservatively bounded by

\[
 \begin{aligned}
 \|\mathcal M(F)\|_1
 &\le1536\cdot2\cdot3^{10}\cdot357{,}128{,}352\\
 &=64{,}782{,}557{,}359{,}865{,}856
 <2^{63}-1.
 \end{aligned}
\tag{3.5}

This uses no cancellation.  Thus a checked signed 64-bit accumulator is
sufficient for one row moment.  An implementation may still use arbitrary
precision integers for simplicity, but overflow is not an inherent R07
obstacle.  Every multiplication and addition must be checked against (3.5),
and the final distribution must satisfy v134 (2.5) integrally and
nonnegatively.

## 4. Exact production consequence

The negative linked-correlation branch can be organized as follows for each
separating dual:

1. merge the eleven typed occurrences in \(\mathbf F_3\);
2. enumerate at most 1,536 partial assignments for each of 6,441 rows;
3. cache the at most 1,024 ordered subset types;
4. obtain each required membership bit and kernel order from the
   authenticated projection oracle;
5. accumulate the exact Eisenstein pair; and
6. declare zero correlation only at \((A,B)=(|\Delta|,0)\).

The arithmetic work in steps 1, 2, 5, and 6 is bounded by (2.4) and (3.5).
The only unresolved scalability question is step 4: how the actual R07
extension returns simultaneous-fibre membership and a word-bearing section
for the demanded target tuples.  A cap or missing projection answer remains
`UNKNOWN_RESOURCE` or `UNKNOWN_INPUT`, never a zero moment.

```text
CUBIC-MOMENT FORMULA (v134):                  PAPER_PROOF
PER-ROW RAW TERM CAP 1536:                    PAPER_PROOF
ALL-6441 PER-DUAL TERM CAP 9,893,376:         PAPER_PROOF
SIGNED-64 ACCUMULATOR SAFETY:                 PAPER_PROOF
AUTHENTICATED MULTI-PROJECTION ORACLE:         PENDING
COMMON ALL-SEVEN CORRECTION WORD:             NOT CONSTRUCTED
COFINAL LIFT / FAKE / IHARA WITNESS:          NOT DECLARED
```
