# R07 A0: index repair for the six-grade transition schedule (v449)

Author: Sol / 2026-09-03

Status: exact incorporation of the sole local repair accepted by independent
Task555. It changes notation only and proves no membership. `verified=false`.

For the step from precision \(d-1\) to precision \(d\), v444 indexes the
new pure-grade defect closure by the lower precision.  To avoid ambiguity,
define

\[
 H^{[d]}:=H^{\mathrm{v444}}_{d-1}.                    \tag{1}
\]

Then v448 (3.1) is to be read as

\[
 \boxed{
 U_d=\operatorname{span}(\widetilde B_{d-1})
       \oplus H^{[d]}.}                               \tag{2}
\]

Every later reference in v448's grade-\(d\) step to the newly exhausted
defect basis means \(H^{[d]}\).  In particular, the physical roster is the
union of all lifted rows from \(B_{d-1}\) and an exhausted basis of
\(H^{[d]}\).  The target residual is \(\rho_d\), and a MEMBER terminal builds
the next presentation \(\mathcal T_d\).

This convention matches Task555's accepted recurrence exactly.  It changes
none of the six Hilbert multiplicities, source widths, physical widths,
terminal gates, or the conditional implication from six direct MEMBER
replays and \(I^7=0\).

```text
FIRST RUNG: exact six-grade induction specified; 0/6 grades computed
ORDER-54,432 / FULL-Q0 / A0 / COMMON / COMPATIBLE COFINAL LIFT: not declared
FAKE / IHARA: not declared
verified=false
```
