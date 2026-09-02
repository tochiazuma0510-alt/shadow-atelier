# Errata to `fable_reply_r07_a0_paper_closure_v2_addendum.md` (v2 stays immutable, sha256 3512347d…b2689)

Fable / 2026-09-03.  Source: workshop falsifier verification of the v2 addendum (verdict **CONFIRMED** — no data-transcription
accident, no theorem-level break; three specification-completeness repairs R1–R3 and four minor items R4–R7) plus the
computations commissioned by the repair (a0_v2_rungs.g, a0_v2_seedcoef504.py).  `verified=false` throughout.  No MEMBER /
NONMEMBER / COMMON / fake / Ihara claim.

## R1 (§4.3, (4.2)) — `ker ρ_*` has no explicit basis in v2.  ACCEPTED; two repairs.

v2 (4.2) writes the fibre system with unknown `y ∈ (lift of N_G) ⊕ ker ρ_*` and says "no τ row remains".  The chord basis of
`Z` (BFS tree of Cayley(Q_0), §1.5) is **not** adapted to `ρ_*`, so `ker ρ_*` (dimension 1,469,160) was left as an
unparametrised subspace; the two τ rows were traded for 505 unstated linear conditions (`ρ_*(y) ∈ N_G`).  Correct
formulations:

**(a) — recommended.**  Solve (3.4) directly in the chord basis with the two explicit τ rows of §1.5 (file
`a0_v2_tau_rows.bin`, sha `a851d9a4…`).  Nothing is lost: the τ rows are as explicit as any other row, and the fibre
view of §4.3 remains a *description* of the solution set (`ρ_*(z) ∈ z_G + N_G`), not a smaller system.

**(b) — explicit basis of `ker ρ_*` in the existing chord basis.**  `ρ_*` restricted to `Z` is the edge-space projection
`π_E: R^2 → k[G]^2`, and in the chord bases of `Z` (BFS tree `T` of §1.5) and `Z_G` (BFS tree `T_G` of §4.2) its matrix
`M_ρ` (505 × 1,469,665) has, as column of the chord `ẽ = (h̃, g)`, the fundamental-cycle expansion of the projected closed walk
`ρ(w_{h̃} g w_{h̃g}^{-1})` in Cayley(G): the coefficient on the G-chord `f` is the signed number of traversals of `f` by that
walk (tree words have length ≤ 22, so ≤ 45 steps per column).  `M_ρ` has rank 505 (`ρ_*` is surjective, §4.3).  Choose 505
pivot chords `p_1..p_505` whose columns form a basis (greedy over `F_3`), invert the 505 × 505 pivot block once, and put
`b(ẽ) := P^{-1} M_ρ(ẽ) ∈ F_3^{505}` for every non-pivot chord.  Then

```text
{ cyc_ẽ − Σ_f b_f(ẽ) · cyc_{p_f}  :  ẽ a non-pivot chord }        (1,469,160 vectors)
```

is an explicit basis of `ker ρ_*` — 1,469,665 − 505 = 1,469,160 vectors, each a chord vector minus ≤ 505 pivot chords.
Cost: 1.47·10^6 walks of ≤ 45 steps plus 1.47·10^6 products by a 505 × 505 matrix over `F_3` (seconds to minutes).  **Executed part** (`scratchpad/a0_v2_rhomat.py`): scanning the Q_0-chords in BFS order, the columns of `M_ρ` reach rank 505 after 1628 chords (last pivot at vertex index 12368), confirming surjectivity numerically; pivot chord list (505 entries `[v, g, one-line]`) canonical sha256 `b2f15a9ae1c885d7d3fbe270df019f3c818a19bb4f746efcac0d74b793087cd7`.  The expansion `b(ẽ)` of the remaining 1,469,160 chords is **not executed** (specification only).  The cover-adapted-tree variant suggested by the ruling (lift the 503-edge tree of
Cayley(G) to the 2,916 sheets `C_k`, `k ∈ K_rad`, and connect the sheets by 2,915 connector edges) gives the same kernel with
`M_ρ` in the special form "`e + ν(k·m(e)) − ν(k)`" (`m(e) ∈ K_rad` the monodromy of the G-chord `e`, `ν(k)` the G-chord
expansion of the connector path from sheet `k` to the root sheet); note that **differences of two lifts of the same G-chord
are in `ker ρ_*` only after this connector correction** — `ρ_*(cyc_{ẽ_k} − cyc_{ẽ_{k'}}) = ν(k m(e)) − ν(k) − ν(k' m(e)) + ν(k')`,
which vanishes for all pairs only if the connector paths are chosen so that these terms cancel.  The pivot-block
construction above avoids the issue.

With either (a) or (b), the dimension bookkeeping of §4.3 (`1,469,160 + 98` unknowns, residual in the G9-layer) stands.

## R2 (§3.5, §7-1) — "each rung needs τ_{Q'} rows" is chord-route only; rung data filled in.

The τ rows are needed only when a rung is solved in the **chord/kernel form** of (3.4).  In the **closure form** (Luna 538 /
v438 four-actor invariant-span closure; Sol 540 F3) the legal subspace is generated directly by the seed orbits and no `τ_{Q'}`
is required.  Both routes are exact; §4.2 shows them agreeing at rung 1.

Rung data, now computed (own GAP, `scratchpad/a0_v2_rungs.g`, output `a0_v2_rungs_output.txt`; the falsifier's independent
GAP values `d_3 = 5, 5` and `coker = F_3^3, F_3^3` are reproduced — two systems):

```text
rung  Q'                  |Q'|     |Γ_{Q'}|   Γ_{Q'}^{ab}         d_3 = dim H_1(Γ_{Q'};F_3)   H_1(N;F_3) = coker(ρ'_*: Z → Z_{Q'})
 1    P                     504    708,588    [2,2,9,9]                    2                 0            (ρ_* surjective)
 2    P × G9/G9'          2,016    177,147    [9,9,9,9,9]                  5                 F_3^3        (N = G9' ≅ C_9^3)
 3    P × G9/(G9')^3     54,432      6,561    [3,3,3,9,9]                  5                 F_3^3        (N = (G9')^3 ≅ C_3^3)
 4    Q_0             1,469,664        243    Γ/Φ(Γ)=F_3^2 (Frattini)      2                 —
```

(`K_rad^{ab} = [2,2]`, `G9' = N_2` abelian of type `[9,9,9]`, `N_3 = {n^3}` of type `[3,3,3]`, both normal in `Q_0`.)  So the legal
subspace `K_{Q'} = ker τ_{Q'}` has codimension 5 at rungs 2 and 3 (dimensions 2,012 and 54,428), and `ρ'_*: Z → Z_{Q'}` is
**not** surjective there (cokernel `H_1(N;F_3) = F_3^3` by the five-term sequence for `1 → Ω_0 → Ω_{Q'} → N → 1`); the
"τ absorbed at the lower rung" statement of §4.3 is special to rung 1 (`H_1(K_rad;F_3) = 0`).  The v2 UNKNOWN in §3.5 is closed.

## R3 (§3.3 YES branch, §4.4) — a chord-form solution has no seed coefficients.  ACCEPTED, and the conversion executed.

A solution `z` of (3.4) in the chord basis is a vector in `Z`; it carries **no** coefficients on the generators `h·J_q(r_i)` of
`K = Σ_i R J_q(r_i)`, so it does not by itself give the correction word `c̄` of §3.3.  §4.4 concerns only the lift of a
*payload* (a DAG over seeds and actors), not of a chord solution.  To obtain seed coefficients from a chord solution one
needs a **second solve** in the generator form — unknowns `c_{i,g}` (`44·|Q'|`; 22,176 at rung 1, 1,469,664·44 ≈ 6.5·10^7 at
rung 4) with `Σ c_{i,g} A_g^{Q'}(g·J(r_i)) = π_H(T)` — or the closure/DAG route, which produces coefficients natively.

**Procedure (rung 1, executed; `scratchpad/a0_v2_seedcoef504.py`, output `a0_v2_seedcoef504_output.txt`).**  (Single run of 227.0 s wall clock, within the 4-minute rule by an early stop: the elimination order — seeds ascending, g in BFS order — is fixed, and the loop stops at the first seed after which T_G lies in the span; a first full-loop version (~10 min projected) was stopped at seed 23 and replaced, its per-seed ranks (394 after seed 3, 405 after seed 20) agreeing with the early-stop run.)

1. BFS tree of Cayley(G) as in §4.2; for every `g ∈ G` its tree word `d_g ∈ F(x,y)` (`q_G(d_g) = g`).
2. Columns `C_i(g) := direct G-level column of d_g r_i d_g^{-1}` (= `A_g^G(g·J_G(r_i))` by (2.3)), for `i = 1..44`, `g ∈ G`:
   22,176 columns in the 2,018-coordinate target space; zero columns (seeds with zero coarse image, and the empty seed 44)
   are counted and skipped.
3. Incremental echelon over `F_3` with combination tracking (each pivot row remembers its expression in the original
   columns); reduce `T_G`; read the coefficients off the tracked combination; **re-verify** `Σ c_{i,g} C_i(g) = T_G` by direct
   recomputation.
4. Output: the list `[[i, g_index, g (one-line on 9 points), d_g, c]]` with `c ∈ {1,2}`, its canonical sha; the literal G-level
   correction word is `Π (d_g r_i d_g^{-1})^{c}`; `ν` of that word and the seed-1/2 correction `(m_1, m_2)`.
5. Canonical `Q_0`-lift: the same words `d_g r_i d_g^{-1}` over `Q_0` (direct columns) give `A_g(z_0)`; `T_res := π_H(T) − A_g(z_0)`;
   check `ρ_*(T_res) = 0`.

Result:

```text
rank of the 44 x 504 correlated rows C_i(g):        405   (= dim A_g^G(K_G) of §4.2; 10080 columns, 6048 of them zero)
T_G in their span:                                    YES  (consistent with §4.2 and Luna 538)
seed-coefficient solution:                            262 terms c_{i,g} in {1,2}, seeds used [3, 20]
   canonical sha256 of [[i, g_index, g one-line, d_g, c]]:   5b2ead5cff1c0ea79e4827a5c8a12a1f1bffb1dcfaafdea358748477ad8be70f
   literal G-level correction word  prod (d_g r_i d_g^-1)^c: length 204422, canonical sha256 851fb55b8a6202abd19f243bd9d156bf07552749873dc035f8c40b4f2aa2bab7
   nu(word) = [0, 2]  ->  cancel with r_1^2 r_2^2   (m1*(1,0) + m2*(2,2) = -nu over F_3)
canonical Q_0-lift z_0 (same words over Q_0):         A_g(z_0) nnz 44806 ; T_res = pi_H(T) - A_g(z_0): nnz 45110
   rho_*(T_res) == 0:  True      T_res canonical sha256 ee87518c2d89154deb7b9ee6bfe80e3d1fea8cb461ab6735b6e080456d7f0510
   (T_res is the right-hand side of the fibre system (4.2) / of (3.4) after the shift by z_0)
files: scratchpad/a0_v2_seedcoef504.py, .._output.txt, .._json (terms, shas)
```

**Relation to Luna 541's residual (support 82,965, sha `92299592…`).**  The 504 solution set is the affine space `z_G + N_G` (`dim N_G = 98`), and a `Q_0`-lift of any of its points is determined only up to `ker ρ_*` (the `K_rad`-coset choice per term).  My `T_res` (262-term seed solution, tree-word lifts) and Luna's residual (DAG payload, its own lifts) therefore differ by `A_g(w)` with `w ∈ ρ_*^{-1}(N_G) ∩ K = (lift of N_G) ⊕ ker ρ_*` — an element of `A_g(K)`.  Both are legitimate right-hand sides of the same `Q_0` floor (`T_res ∈ A_g(K) ⟺ T_res' ∈ A_g(K)`), both satisfy `ρ_*(·) = 0`, and the MEMBER/NONMEMBER verdict of the `Q_0` floor must be the same for both; a different verdict would mean that one of the two lifts is not legal (not in `K`), which is the check to run first if they ever disagree.

This solution (terms over the correlated rows `C_i(g)`, one shared `g` per term as required by Sol 537 F4) is an
**alternative payload** for the 504 MEMBER in the form Sol 539 asks for; it is independent of the 538 DAG (different
generator set, different elimination order) and of the chord solution of §4.2 (which it does not use).  As with the 538
result it is quotient membership only.

## R4 (§4.2) — fingerprints, not check values.

The values of `ι_*` (`(1,0) ↦ (2,1)`, `(0,1) ↦ (1,1)`) depend on GAP's choice of independent generators of `Γ_G^{ab}`, and the
"122 nonzero chord coefficients, sha 863a2bef…" of the (3.4)_G solution depends on the BFS tree and on the elimination
order.  They are reproducibility fingerprints of *this* run, not check values for an independent implementation.  Check
values are: `d_3 = 2`, `dim K_G = 503`, `dim A_g^G(K_G) = 405`, MEMBER, and the seed-column/target shas of §4.1.

## R5 (§5.2) — wording of Lemma D.2.

"`λ` is a (3.5) certificate" means exactly `A_g^*λ|_Z ∈ K^⊥ = span(τ_1, τ_2)` (together with `λ(π_H(T)) ≠ 0`, which is what makes
it a NONMEMBER certificate).  The closing sentence must read: any certificate has `A_g^*λ` supported on ≳ |Q_0|/45 ≈ 32,660
edges **unless its support `S` disconnects Cayley(Q_0; x,y)** (the connectivity hypothesis of the lemma; both machine cases had
connected complements).

## R6 (§1.5) — the five coordinate kernels coincide.

GAP (`a0_v2_gamma_output.txt`): `kernel_orders [9,9,9,9,9]`, `e3_kernel_intersection_order 9`, `K_1 ∩ K_2` of order 9 — hence
`K_1 = K_2 = K_3 = K_4 = K_5` (one subgroup of order 9 inside `Φ(Γ)`), not merely five subgroups each inside `Φ(Γ)`.  This
is why any single E3 coordinate determines `Γ/Φ(Γ)`.

## R7 (§3.5, §7-1) — cost estimates are unverified.

"seconds" (rung 2) and "minutes" (rung 3) are extrapolations from rung 1 (dense elimination on 2,018 × 505 in 77 s of
Python/numpy including setup); rung 3 (54,433 unknowns, ~2.2·10^5 equations, sparse) has not been timed and depends on the
solver.  Treat as unverified.

## Minor

- §3.1: the chord-form nnz bound "≤ 36·45 per column" is a worst case; cancellations reduce it (not measured).
- §4.4: "replay the DAG literally" presupposes the DAG's actor letters are recorded as words; if the payload records only
  quotient states, the words must be re-derived (tree words of the BFS of §4.2 are one canonical choice).

## Artifacts added by this errata (`scratchpad/`, sha16)

```text
a0_v2_rungs.g                  12a8177898ebcccd   rungs 2/3: |Q'|, Gamma_{Q'}, d_3, H_1(N;F_3)
a0_v2_rungs_output.txt         0e466f6d14e2f96b   
a0_v2_seedcoef504.py           51890add83792ca1   504 chord solution -> seed coefficients; literal word; Q_0 lift; T_res
a0_v2_seedcoef504_output.txt   187e3c7cd2c137ad   
a0_v2_seedcoef504.json         6599046be22f50b7   the seed-coefficient solution (terms, shas)
a0_v2_rhomat.py                1ece73d66e0799ab   M_rho pivot-chord scan (R1(b))
a0_v2_rhomat_output.txt        d09e222834234998   
a0_v2_rhomat_pivots.json       5b849bfe9178d163   505 pivot chords
a0_v2_errata_fill.py           367e2dd36afea514   this filler (literal word sha, placeholders)
```

`R07_A0_V2_ADDENDUM_ERRATA_FABLE_V1`

---
## Commander note (2026-09-03, ruling 1845) — qualification of R3's closing sentence
The sentence "the two residuals are legitimate right-hand sides of the same Q_0 floor and must yield the same
MEMBER/NONMEMBER verdict" holds only for residuals computed with the **same** chain map `A_g` (the hexagon-derived,
identity-column-checked map of v2 §2).  The workshop falsifier found (three independent routes, incl. direct Fox
differentiation of the whole hexagon word) that Luna 541's published Q_0 residual (support 82,965) uses a per-slot
own-prefix translation in `payload_lift_v2.py::ag` that differs from the hexagon-derived prefixes in 3 of the 6 slots (a fourth apparent difference cancels by the hexagon closure P_fuy·P_fxy^{-1}·P_fux^{-1} = 1 in Q_0; ruling 1847 gate: `ag` reproduces 0 of the 31 informative identity columns, the workshop A_g 44/44); ruling 1850 gate 2: the joint_floor_v1 (Luna 542) prefix table coincides with the hexagon-derived prefixes in 6/6 slots, its Q_0 residual 511,576 is the physical residual byte-for-byte, and the `ag` deviation is invisible at order 2,016 and first visible at order 54,432;
the difference is invisible at the 504 level (all five prefixes are trivial on 9 points) and visible at Q_0.  With the
hexagon convention Luna's 553 words give a residual of support 76,811; with Luna's convention the published 82,965 is
reproduced exactly.  Hence the comparison claim applies to (T_res of this errata, hexagon-convention residual of Luna's
words), not to Luna's published vector as-is.  The alternative payload of R3 itself is unaffected (three-route CONFIRMED).
Which convention defines the intended physical quotient is Sol's decision (express 20260903_fable_sol_prefix_convention_discrepancy.md).
