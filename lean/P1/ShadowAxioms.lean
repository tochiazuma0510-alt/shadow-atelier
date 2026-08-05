/-
P1/ShadowAxioms.lean -- quarantine boundary for paper-specific T2 statements.

The former revision exported four axioms whose entire type was bare `Prop`.  Such declarations
did not encode a domain, codomain, hypotheses, or the cited formula and therefore could not be
audited for paper fidelity.  They have been removed rather than renamed or silently trusted.

No declaration is exported from this module.  Before any T2 declaration is reintroduced, Sol
must approve the exact theorem/page, all hypotheses, domain/codomain, weakest conclusion, and a
sanity instance.  Block A, Block E, Block H, and the axiom audit do not import this module.
-/
