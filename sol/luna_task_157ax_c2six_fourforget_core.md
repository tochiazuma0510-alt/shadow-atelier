# Luna task 157ax — exact four-forget core quotient

## Role and goal

Act as Luna.  Resolve the first noncircular obligation in
`sol/luna_reply_157av_c2six_b4_bridge_reaudit.md`: decide exactly whether the
specific Phase-2b pair `E -> P=PSL(2,8)` gives a nonzero B4 core quotient.
Do not assume that it is `C2^6`, and do not use the old raw-158 presentation.

## Mathematical object

Use the pinned marked epimorphisms

```text
psi_E : PB3 -> E=PerfectGroup(32256,2),  ker(E->P)=V=C2^6,
psi_P = pi o psi_E,
psi_E(x12,x23,x13)=(X,Y,Z),  Z=(Y*X)^-1.
```

Let `d_i:PB4->PB3` forget strand `i` and relabel the other three in increasing
order.  First prove from the pinned receipt (not from a label) whether `N_E`
and `N_P` are B3-normal.  If they are, prove that the B4 core orbit reduces
from 24 representatives to the four kernels of `psi_Q o d_i`.  Otherwise use
all actual kernel conjugates and report that the four-map simplification is
invalid.

For the four-map case, independently derive and record all six tuple images.
For example the expected convention is

```text
x12 -> (1,1,X,X), x13 -> (1,X,1,Z), x14 -> (1,Z,Z,1),
x23 -> (X,1,1,Y), x24 -> (Z,1,Y,1), x34 -> (Y,Y,1,1),
```

but this table is a hypothesis to check against exact forget maps and the
paper's PB4 generator convention.

Define `G_E=im(PB4->E^r)` and `G_P=im(PB4->P^r)`.  Compute and certify

```text
|G_E|, |G_P|, |ker(G_E->G_P)| = |C_P/C_E|,
```

and, if nonzero, its elementary-abelian rank, B4 action, composition factors,
and one explicit nonzero kernel word/witness.  If zero, close this candidate
honestly.

## Implementation and verification

Create only versioned 157ax assets plus the reply:

```text
search/d972_c2six_fourforget_core_v1.g
search/check_d972_c2six_fourforget_core_v1.py
.github/workflows/d972-c2six-fourforget-core-v1.yml
sol/luna_reply_157ax_c2six_fourforget_core.md
```

The GAP producer may use the pinned permutation arrays/receipts but must not
run locally.  The independent Python checker must not import producer code or
trust a reported order.  Use structural certificates (pair projections,
Schreier/transversal or relator witnesses, and F2 matrix replay) so that it
can validate a potentially large subdirect product without enumerating it.
Pin every input and executable source by SHA-256.  The workflow must use the
repository GAP wrapper conventions appropriate to Ubuntu, fail closed, upload
lossless receipts even on failure, and return UNKNOWN on timeout.

Do not run local GAP, git, push, or GHA.  Python-only bounded selftests are
allowed.  Parent will audit, commit, push, and dispatch.

Return exactly one terminal verdict:

```text
FOURFORGET_CORE_READY_FOR_GHA
BLOCKER_FOURFORGET_CORE: <exact defect>
```

