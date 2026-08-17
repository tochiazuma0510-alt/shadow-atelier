# Luna task 156a — exact low-memory Burau fiber mathematics

The GF(5) v2 campaign run 32043312123 reached full mode but the degree-3161
combined permutation representation hit GAP's 12GB workspace limit.  Design
an exact replacement that never constructs the combined 3161-point group.

Write only `sol/luna_reply_156a_burau_lowmem_math.md`.  Do not edit code, run
local GAP, commit, push, or dispatch.

Audit/prove a concrete algorithm for the same map

`E:F2 -> P x GL(4,5)^5`, `H=im(E)`, `H'=[H,H]`,
`K=ker(H'->P)`.

Promising route to assess rigorously:

1. Work with exact tuple elements `(roof permutation, five 4x4 matrices)`.
2. Let `c=[x,y]`.  Prove a finite conjugate family
   `{c^(x^i y^j)}` generates `H'`, with defensible exponent bounds derived
   from exact orders (or replace this by a safer normal-closure algorithm).
3. Select lifts whose roof projections generate `P'`.  Obtain a complete
   kernel either from an exact presentation/Schreier process on `P'` or a full
   Cayley BFS on the 367,416-element projected group.  Account for redundant
   lifts and normal closure; do not silently lose matrix-only kernel elements.
4. Enumerate the resulting small `K` exactly, produce a section lift for every
   roof target, and scan each exact coset for the A.18 identity defect.
5. State independent completeness gates and calibration identities that can
   be checked at q=3/q=4 against the known values:
   `|H|=105815808`, `|H'|=2939328`, `|K|=8`, projected order `367416`,
   all 972 fibers size 8 with one identity defect.

Identify every place where a tempting shortcut would only be a semidecision.
Return a theorem-level algorithm or FAIL with the precise missing lemma.
