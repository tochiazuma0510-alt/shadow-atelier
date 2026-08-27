# R07 cubic-moment resource-cap erratum v138

Author: Sol / 2026-08-27

Status: paper correction and replacement implementation contract.  This note
withdraws the unconditional numerical resource bounds in v136.  It does not
withdraw v134's exact cubic-moment identity or v137's coarse-anchor membership
theorem.  No common correction word, cofinal lift, fake, or Ihara witness is
declared here.

## 1. Exact scope of the correction

The following assertions in
`proof_r07_cubic_moment_exact_resource_cap_v136.md` are withdrawn:

1. the inference \(\sum_i|T_i|\leq 11\);
2. the resulting per-row bound \(1,536\);
3. the resulting all-6,441-row bound \(9,893,376\); and
4. the unconditional signed-64 safety conclusion derived from those bounds.

Consequently, the phrase "at most 1536 partial targets per row" in v137
Section 6 and every production contract depending on that number are also
withdrawn.  V134 (1.1)--(3.4), including

\[
 \#\text{raw terms}=\prod_{i=1}^{10}(1+|T_i|),
\tag{1.1}
\]

remains exact.  V137 Theorem 3.1 and the kernel formula v137 (4.2) also remain
exact.

## 2. The dropped multiplicity

Let \(\lambda\) be one authenticated dual row.  For a module block \(b\), put

\[
 m_b(\lambda)=
 \bigl|\{g:(b,g)\text{ occurs with nonzero coefficient in }\lambda\}\bigr|.
\tag{2.1}
\]

For a fixed normal-generator row \(r\), let \(\mathcal O_r\) be its typed Fox
occurrence list and let \(b_o\) be the block of occurrence \(o\).  V132
(1.2)--(1.4) shows that occurrence \(o\) pairs once with *every* support point
of \(\lambda\) in block \(b_o\).  Therefore the pre-merge target count is

\[
 M_r(\lambda)=\sum_{o\in\mathcal O_r}m_{b_o}(\lambda),
\tag{2.2}
\]

and after equal-target addition and zero cancellation one has only

\[
 \boxed{\sum_{i=1}^{10}|T_i|\leq M_r(\lambda).}
\tag{2.3}
\]

The fact that \(|\mathcal O_r|=11\) counts occurrences, not dual support
points.  It implies (2.3) with the support-weighted right side (2.2); it does
not imply \(M_r(\lambda)\leq11\).  This is the precise error in v136.

## 3. Correct support-parametric cap

### Theorem 3.1 (BALANCED TEN-COORDINATE CAP)

Let \(s_i=|T_i|\geq0\), suppose \(\sum_i s_i\leq M\), and write

\[
 M=10q+r,\qquad 0\leq r<10.
\tag{3.1}
\]

Then

\[
 \boxed{
 \prod_{i=1}^{10}(1+s_i)
 \leq P_{10}(M):=(q+2)^r(q+1)^{10-r}.}
\tag{3.2}
\]

For the actual merged target sets, the exact raw-term count is the left side
of (3.2); using \(M=M_r(\lambda)\) gives an authenticated a priori bound.

#### Proof

The product is monotone in every \(s_i\), so its maximum under a sum at most
\(M\) occurs at sum exactly \(M\).  If \(a\geq b+2\), replacing the pair
\((a,b)\) by \((a-1,b+1)\) changes the corresponding factor product from
\((a+1)(b+1)\) to \(a(b+2)\), an increase of

\[
 a(b+2)-(a+1)(b+1)=a-b-1>0.
\tag{3.3}
\]

Thus all entries in a maximizer differ by at most one.  They are \(q+1\) in
exactly \(r\) coordinates and \(q\) in the other \(10-r\), which gives
(3.2). \(\square\)

This theorem is a formula, not a small constant.  Production must first
authenticate \(\lambda\)'s block support, reconstruct and merge all targets,
and record

\[
 M_r(\lambda),\qquad (s_1,\ldots,s_{10}),\qquad
 P_{\rm actual}=\prod_i(1+s_i).
\tag{3.4}
\]

A registered resource ceiling may then compare against \(P_{\rm actual}\).
Exceeding it is `UNKNOWN_RESOURCE`, never zero correlation.

## 4. Integer arithmetic

Let \(N=|\Delta|\), and use the Eisenstein pair norm
\(\|(A,B)\|_1=|A|+|B|\).  V134's two nontrivial factors satisfy

\[
 \|x(\omega-1)\|_1\leq3\|x\|_1,
 \qquad
 \|x(\omega^2-1)\|_1\leq3\|x\|_1.
\tag{4.1}
\]

Multiplication by \(\omega^K\) costs at most a factor two in this norm, and
every simultaneous-fibre count is at most \(N\).  Hence a naive expansion
with actual term count \(P_{\rm actual}\) has the conditional intermediate
bound

\[
 \boxed{
 \|\mathrm{acc}\|_1
 \leq 2\cdot3^{10}\,N\,P_{\rm actual}.}
\tag{4.2}
\]

This replaces v136 (3.5).  It does not give unconditional signed-64 safety.
Production must use arbitrary-precision signed integers, unless (3.4) and
(4.2) are evaluated for the particular row and explicitly prove a narrower
machine-integer bound.

The final moment itself is much smaller: if
\(\mathcal M(F)=A+B\omega\), v134 (2.4) gives

\[
 A=n_0-n_2,\qquad B=n_1-n_2,
\tag{4.3}
\]

so \(|A|,|B|\leq N\).  That final-value bound does not bound intermediate
partial sums in the inclusion expansion, and therefore cannot justify an
unchecked fixed-width accumulator.

## 5. Corrected execution contract

For every dual and every one of the 6,441 registered rows, a producer must:

1. reconstruct the raw targets from the complete Fox occurrence list and
   the complete authenticated support of \(\lambda\);
2. merge equal targets in \(\mathbf F_3\) and delete zero coefficients;
3. record and cross-check all quantities in (3.4);
4. use arbitrary-precision Eisenstein-pair arithmetic;
5. answer every term of v134 (3.3) through the v137 simultaneous linked
   membership oracle; and
6. declare zero correlation only after the exact final pair is
   \((N,0)\) and the recovered \((n_0,n_1,n_2)\) are integral,
   nonnegative, and sum to \(N\).

The independent checker must rebuild the dual support counts, occurrence
multiplicities, merged target sets, exact product in (3.4), and all moment
arithmetic.  Required resource mutations include replacing a block support
count by one, replacing (2.2) by the number of Fox occurrences, and imposing
the withdrawn constant 1,536 on a fixture with larger authenticated support.

Task178's finite D6 SELFTEST may retain a *toy-instance* exact term count, but
it must not label that number an R07 production cap.  Any production path
must pin this erratum and must fail closed until the real dual supports have
been reconstructed.

```text
CUBIC-MOMENT FORMULA (v134):                    PAPER_PROOF / UNCHANGED
COARSE-ANCHOR MEMBERSHIP (v137 Thm 3.1):       PAPER_PROOF / UNCHANGED
UNCONDITIONAL PER-ROW CAP 1536 (v136):          WITHDRAWN
UNCONDITIONAL ALL-ROW CAP 9,893,376 (v136):     WITHDRAWN
UNCONDITIONAL SIGNED-64 SAFETY (v136):          WITHDRAWN
SUPPORT-PARAMETRIC CAP P_10(M) (v138):         PAPER_PROOF
ACTUAL R07 DUAL-SUPPORT DISTRIBUTION:           NOT YET MEASURED
COMMON ALL-SEVEN CORRECTION WORD:               NOT CONSTRUCTED
COFINAL LIFT / FAKE / IHARA WITNESS:            NOT DECLARED
```
