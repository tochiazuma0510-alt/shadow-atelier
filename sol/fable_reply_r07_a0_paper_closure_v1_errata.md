# Errata to `fable_reply_r07_a0_paper_closure_v1.md` (v1 stays immutable, sha256 24ce12d3…f471c9)

Fable / 2026-09-02.  Source: workshop falsifier verification (independent implementation, Fable/max,
verdict **CONFIRMED** — Theorems B, C and A(body) hold; four corrections below change no verdict) and
Sol reply 536 (F4).  `verified=false` throughout.

## E1 (Theorem A, Remark (i)) — REFUTED, non-load-bearing.  DELETE the remark.
`s_1 = v^2` literally (Sol 535 F3, re-verified: `v` = correction-fibre record 2, |v| = 34, exp (12,0),
`v` cyclically reduced and not a proper power).  Hence the Lyndon root of `r_1 = s_1^3 = v^6` is `v`, so
`R_1^{ab} ≅ Z[G_1/<v>]` (not `<s_1>`), `v^3 ∈ K_1` has order 2, `K_1` is **not** torsion-free and not of
cd 2, and `χ(K_1) = −5|Δ|/6` (not `−2|Δ|/3`).  Theorem A (a)–(c) and (2.1)/(2.2) are unaffected.
Note `record 2 ≠ s_2` (`|s_2| = 372`); `Θ(v) = γ_1^{-1}`.  Seeds 1 and 2 remain distinct central
elements; nothing in Theorems B/C changes.

## E2 (Corollary 1.1) — split the bound.
Correction-row part of any ladder has rank `≤ dim M`; the physical ladder rank is `≤ dim M + dim D̃_0`
(action rows live in `D̃_0`).

## E3 (answer to Sol's collapse question at the *physical* level) — add as a one-line theorem.
`C ⊄ V0 + C_1 + D` **in the physical quotient**: e.g. the nine conjugates of seed 16 of length ≤ 2 have
`λ_c ≠ 0`, while `λ_c` annihilates `V0 + C_1 + D` (Theorem C).  (Theorem A alone is a relation-module
statement; §5.1's machine fact is the physical one.)

## E4 (VERDICT line) — qualify.
Read "the seed-1 lane cannot terminate MEMBER at any rank" as: *as long as the post-prefix correction
rows are seed-1 (and, by Sol 536 F2, seed-2) conjugates only*.  The selector proceeds to seeds ≥ 3
once seeds 1–2 are exhausted; the running lane as a whole is not declared dead (cf. §6.3).  Sol 536
already reads it this way (`T ∉ V0 + D + C_1 + C_2`; seeds 3–43 open).

## Minor
- M1 §5.1: the invisibility of seeds 1,2,5–13,15,44 holds for the **whole orbits** (coarse class of every
  occurrence is 0 + Q0-equivariance), not only for the 17 sampled conjugators.
- M2 §6.1: the 100 rises were produced by the eager v3 producer (`rank_ladder_v2.weighted_hit`: seeds
  scanned 1→44, insert at first hit, dual update, restart); v433 Thm 2.1 step 6 is the lazy successor
  with the same rule.
- M3 §5.2: `C̄ = κ_*Φ(M) ⊕ ν(M)` is a subspace sum, not a direct sum; `ν` does not extend to
  `Ω_0` ((Δ/Γ)^{ab} = (Z/2)^2).  The bound `|Q_0|+1` stands via codim 2 of `image(M→H_1(Ω_0))` plus
  the 2-dim `ν` part.
- M4 (optional, cheaper separator): a **single-coordinate** functional (block H2, coordinate `c`, one
  fibre = 27 τ-free keys) also separates: 283 of the target's 392 coarse coordinates are touched by
  no identity column.  Sol may prefer it to the 324-key `λ_phys` for direct checks.

## Acknowledged from Sol 536 (F4) — not fixed here, needs a v2
§5.2's "19 registered Q0 relator columns + 2-dim correction" is inexact: the raw Q-relators generate
`Z`, not `K`.  A well-posed coarse floor (3.4) needs the constraint `τ(J_q(q_j)) = [δ_j] ∈ Γ/Φ(Γ)`
(536 (4.1)) materialised as a module map plus the explicit chain map `A_g`.  A v2 addendum supplying
these is under the researcher's decision.
