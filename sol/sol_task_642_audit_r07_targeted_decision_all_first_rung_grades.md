# Sol(max) Task642: does the v474 targeted decision extend to grades 3--6?

## 1. Scope

Read this mail fully and perform a bounded mathematical audit.  Do not edit
proofs or implementation, do not run production/GHA, and do not use git.
Write only
`sol/sol_reply_642_audit_r07_targeted_decision_all_first_rung_grades.md`.

Read at least v443, v444, v447, repaired v449, Task555, v451, v474 and the
candidate v479.  The question is not whether any residual is MEMBER.  It is
whether v474's exact target-directed primal/dual theorem is intrinsically
degree-two, or whether the same construction applies at each remaining
first-rung grade once the corresponding transition presentation is supplied.

## 2. Candidate general form to audit

For fresh grade `e in {2,3,4,5,6}`, let

```text
h_e                       = 6,7,6,3,1
physical P_e width        = 8064*h_e
one character V_(a,e)     = 6048*h_e
physical lower/aux width  = 8064*H_(e-1)+4
```

where `H_r=sum_(i=0)^r h_i` and `(h_0,...,h_6)=(1,3,6,7,6,3,1)`.
Let `r_(e-1)=dim U_(e-1)` be the actual complete preceding occurrence-basis
rank, not an ambient width.  With `E=k^{r_(e-1)}`, lifting the ordered old
basis gives linear maps

```text
ell_e : E -> lower/auxiliary space,
g_e   : E -> P_e.
```

Ordered lower-first elimination should give
`Conn_e = g_e(ker ell_e)`.  The complete seed/transition defect roster has
`44+4*r_(e-1)` origins.  For each of four characters, let `H_(a,e)` be the
full actor closure of its degree-e defect slices and let
`B_(a,e):V_(a,e)->P_e` be the registered occurrence-first physical map.  The
candidate identity is

```text
M_e = span(Conn_e) + sum_a B_(a,e)(H_(a,e)).
```

The candidate dual criterion closes the orbit of
`B_(a,e)^*(lambda)` under all four exact actor adjoints and pairs every raw
dual representative with all `44+4*r_(e-1)` defects.  A failed pairing emits
the matching raw primal row.  Repeating the separator solve then terminates
after at most `dim(P_e)-r0+1` solves, with MEMBER, NONMEMBER, or resource
UNKNOWN exactly as in v474.

## 3. Required findings

1. Recompute the dimension table for grades 2--6.
2. Decide whether the proof of `Conn_e=g_e(ker ell_e)` is independent of the
   degree and of the numerical value 8,059.
3. Decide whether the four-character defect decomposition and actor
   transpose orbits remain legal at every first-rung grade when all monomials
   of one character stay coupled.  Look for quadratic negative-substitution
   terms that could mix grades or invalidate the associated-grade map.
4. Decide whether the image identity above is complete, including all
   lifted-old connection rows, PB3/PB4, exponent and auxiliary typing.
5. Decide whether v474's separator strict-rank proof and raw-word transpose
   convention carry over verbatim after replacing the spaces and defect
   counts.
6. State exactly what remains grade-specific in an implementation: input
   presentation, monomial roster, forward/adjoint maps, target residual,
   dimensions, ranks and resource caps.
7. Preserve v479's boundary: an early targeted MEMBER can form the selected
   word, but is not automatically a complete transition presentation for the
   following grade.

Return `GENERALIZES`, `GENERALIZES_AFTER_REPAIR` with one finite list, or
`GRADE2_ONLY`, with a concrete reason.  Do not assert an actual grade result,
order-54,432 solution, A0, cofinal lift, fake or Ihara.  `verified=false`.

