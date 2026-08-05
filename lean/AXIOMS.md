# P1 axiom registry / checker contract v2

Status: local targeted-build candidate. The authoritative acceptance run is the later GHA gate.

`P1/AxiomCheck.lean` generates `P1/AXIOMS.manifest.json` while elaborating. It inventories every
theorem declaration owned by an imported `P1.*` module (including compiler-generated theorem
declarations), records its exact sorted axiom set, and records a declaration-type digest computed
as `Expr.consumeMData` followed by `Expr.hash`. Bound variables therefore remain in kernel
de-Bruijn form, while source metadata is erased. Digests are Lean-version-specific; the manifest
records `Lean.versionString`.

The checker is fail-closed on:

- an empty theorem inventory;
- any axiom outside `{propext, Quot.sound, Classical.choice}`;
- any axiom name containing `sorryAx`;
- any P1-owned axiom declaration, even if no inventoried theorem currently uses it;
- any unauthorized/sorry dependency of any P1-owned definition, not only theorem roots;
- reappearance of any of the four quarantined bare-T2 declaration names.

The allowed three are Lean-core logical axioms, not paper hypotheses. `Classical.choice` occurs in
the abstract TORS-U construction. There are no project/paper axioms in the accepted import graph.

## T2 quarantine

The former bare propositions

- `ShadowAxioms.T2_thm43_explicit_isolated`,
- `ShadowAxioms.T2_thm43_isolated`,
- `ShadowAxioms.T2_15_Ih_decomp`, and
- `ShadowAxioms.T2_composition_hom`

have been removed. `P1/ShadowAxioms.lean` is now a comment-only quarantine boundary. T2 code must
not be restored until Sol approves an exact source table giving theorem/page, every hypothesis,
domain, codomain, weakest conclusion, and a sanity instance.

## Placeholder hygiene

The two former `: True` declarations are absent. Block A now has an explicit equivalence
`Gn n <-> GnCode n` plus the arithmetic formula for `4*n^3`, and an exact `Lambda` type with an
exact `LambdaSimplyTransitive` proposition. The latter proof remains explicitly OPEN; no theorem
claiming it has been exported.

## Reproduction

From `lean/`:

```text
lake build +P1.AxiomCheck:olean
lake build P1
```

Both are targeted builds permitted by the task envelope. The first emits one `P1_AXIOM_ROW` per
theorem and a final `P1_AXIOM_AUDIT_PASS` line, and refreshes `P1/AXIOMS.manifest.json`.
