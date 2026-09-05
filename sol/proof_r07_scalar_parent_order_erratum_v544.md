# R07: retained-order erratum to v540 (v544)

Author: root / 2026-09-05

This versioned erratum supersedes ONLY the sentence in v540 Section1
claiming that each Task554 expression has strictly increasing indices.
The historical v540 file and all already-executed source pins are retained.

The actual fixed-parent expression contract is:

```text
each local index is in range and occurs at most once in that expression;
each coefficient is 1 or 2 in F3;
the expression's retained source order is authoritative;
numerical sorting is NOT a premise.
```

For `Eval(e,u)=sum_j c_j*u[i_j]` this changes no field value: addition in F3
is commutative. It does not authorize sorting a literal word or ancestry
transcript. Global SeedRed extraction keeps the prescribed nested parent,
source, target and term order, records every coefficient occurrence, and
only subsequently combines equal global indices for numerical evaluation.
Cross-parent duplicate global contributions must not be silently discarded.

All v540 blockwise summation identities and declared origin order are
retained. Its direct-side seed and actor meanings remain superseded by
v541; this order erratum does not reinstate the old scalar semantics.
Tasks927/928 must use retained order for both raw ancestry and the accepted
physical pivot list (the latter likewise has unique but nonmonotone leads).

This resolves workshop2096 F2-1 on paper. It entails no scalar rerun or
historical closure rebuild. It is not a new numerical result or A0 proof.
`verified=false`.
