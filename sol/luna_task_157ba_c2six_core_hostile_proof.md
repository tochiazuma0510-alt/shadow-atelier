# Luna task 157ba — hostile proof audit of the four-forget `C2^24` core

Act as Luna, independently of task 157ax.  Audit the following proposed
paper proof adversarially.  Do not implement, run GAP, use Git/GHA, or accept
an unstated classification theorem without either proving the needed special
case or citing an exact primary statement already present in the repository.

Use the exact four strand-deletion maps recorded in
`search/certs/d972_b4_marity_reduction_maps_v1.json` and the already-bound
nonsplit extension

```text
1 -> V=C2^6 -> E=PerfectGroup(32256,2) -> P=PSL(2,8) -> 1.
```

Let `psi_E: PB3 -> E` be the certified epimorphism, let
`psi_P` be its quotient, and define

```text
Phi_E = (psi_E d_1, ..., psi_E d_4): PB4 -> E^4,
Phi_P = (psi_P d_1, ..., psi_P d_4): PB4 -> P^4.
```

Write `G_E=im Phi_E`, `G_P=im Phi_P`, and
`K=ker(G_E -> G_P) = G_E intersect V^4`.

The proposed proof is:

1. Every coordinate of `G_P` is onto `P`.
2. Every pair projection is `P^2`: for coordinates `i != j`, use a pure
   generator involving deleted strand `i` but neither deletion strand `j`
   to prove the two kernels in `PB4` differ; then apply Goursat and simplicity
   of `P`.
3. A subdirect subgroup of `P^4` with all pair projections onto is `P^4`
   (prove the required special case of the diagonal-strip theorem).
4. If `pr_i(K)=1`, the surjection `G_E -> P^4`, restricted over the `i`th
   coordinate copy of `P`, gives a well-defined section `P -> E`, contrary
   to nonsplitting.  Hence every `pr_i(K)` is nonzero, and irreducibility of
   `V` makes it all of `V`.
5. Conjugation makes `K` a `P^4`-submodule of
   `V^4=V_1 direct-sum ... direct-sum V_4`.  The `V_i` are simple and
   pairwise nonisomorphic as `P^4`-modules.  Therefore a submodule with every
   nonzero coordinate projection is all of `V^4`.
6. Consequently `G_P=P^4`, `K=V^4`, `G_E=E^4`, and for
   `C_E=ker Phi_E`, `C_P=ker Phi_P`,
   `C_P/C_E ~= C2^24`.

Check every direction, normality/module action, use of nonsplitting, the
kernel-to-core quotient identification, and the exact deletion table.  In
particular, look for a hidden error in step 3 and for a diagonal submodule in
step 5.  Distinguish mathematical hypotheses already certified from ones
that still require a machine receipt.  Explain exactly what this proves and
what it does *not* prove about B4 isolatedness, typed `ML`, 325 lifts,
cofinality, or B4-B.

Write only `sol/luna_reply_157ba_c2six_core_hostile_proof.md` and end with one
of:

```text
PASS_C2SIX_CORE_C2_24
BLOCKER_C2SIX_CORE_PROOF: <first fatal gap>
```
