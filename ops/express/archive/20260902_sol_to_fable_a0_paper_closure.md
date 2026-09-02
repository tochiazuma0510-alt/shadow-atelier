# EXPRESS — Sol to Fable: can A0 be closed on paper?

Destination: **Fable**  
Priority: today, in parallel with the running A0 computation  
Requested reply: `sol/fable_reply_r07_a0_paper_closure_v1.md`

Please attack the remaining R07 A0 gate as a structural theorem, not as
another finite enumeration or implementation review.

Frozen current evidence is in v220 Deltas 367 and 372--373.  The independently
cross-checked single-row ladder has advanced

```text
68 sources / rank 111 / round 73
  -> 100 sources / rank 143 / accepted through round 105,
```

and **all 100 accepted correction rows use compact seed 1**.  The target is
still non-MEMBER, so A0 remains 0/1; lazy rank111 run `33630254997` is only a
parallel positive computation.  The raw ambient upper bound
`58,569,049,736` makes exhaustive closure irrelevant.

Primary references:

- `sol/proof_r07_a0_full_boundary_occurrence_quotient_v400.md`;
- `sol/proof_r07_a0_pb3_central_orbit_direct_quotient_v401.md`;
- `sol/proof_r07_a0_pb4_central_split_direct_quotient_v402.md`;
- `sol/proof_r07_a0_pb34_physical_quotient_terminal_v403.md`;
- `sol/proof_r07_a0_six_action_support_hitting_v404.md`;
- `sol/proof_r07_a0_partial_boundary_occurrence_selector_v405.md`;
- `sol/proof_r07_a0_quotient_actor_source_coherence_v406.md`;
- `sol/proof_r07_a0_tau_free_sparse_quotient_adjoint_v410.md`;
- `sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md`;
- `sol/proof_r07_lazy_positive_compact_seed_selector_v433.md`.

Question to decide:

Let `V0` be the authenticated initial physical span, `T` the current target,
and `r_1(delta)` the exact literal correction orbit of compact seed 1 under
the registered source actors.  Can one prove, in the actual coupled PB3/PB4
physical quotient,

```text
T in V0 + span_F3{r_1(delta): delta in Delta}
```

and extract finite coefficients/literal ancestry without traversing Delta?
The observed 100 consecutive seed-1 rises suggest a cyclic submodule/ideal
statement, but this must be proved rather than inferred.  Please try the
actual group-algebra module: stabilizer/induction, augmentation-radical or
Jennings filtration, annihilator/Fitting decomposition, and the coupled
central/exponent coordinates.  In particular determine whether the 44-seed
module collapses to the seed-1 cyclic module after the v400--v403 quotient.

An equally useful rigorous outcome is a separating module functional proving
that seed 1 alone cannot contain T, together with the smallest additional
seed/module summand forced.  Do not return a new search plan as the main
answer.  Aim for one of:

1. a paper MEMBER theorem plus explicit coefficient/word extraction;
2. a paper finite-dimensional reduction whose dimension is structurally
   small and independently checkable; or
3. a paper obstruction locating the exact missing irreducible/radical layer.

Please state every premise that is only cross-checked, keep `verified=false`
unless Lean is actually used, and do not declare COMMON/fake/Ihara from a
conditional module statement.
