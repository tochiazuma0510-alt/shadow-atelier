# Luna task 157ar — independent post-Schreier audit of power-spectrum v2

## Role and write scope

Act as an independent Luna auditor.  The repair author is a different agent.
Do not modify producer/checker/core/workflow.  Do not run GAP, git, push, or
GHA.  Write only
`sol/luna_reply_157ar_power_spectrum_v2_postschreier_audit.md`.

## Frozen audit set

- `search/d972_dovetail_core_v2.g`
- `search/d972_power_spectrum_v2.g`
- `search/check_d972_power_spectrum_v2.py`
- `.github/workflows/d972-power-spectrum-v2.yml`
- `sol/luna_reply_157ac_power_spectrum_repair.md`
- prior blocker: `sol/luna_reply_157an_power_spectrum_v2_final_reaudit.md`

Read every file in full.  Recompute all file hashes.  Run only lightweight
Python compile/self-test/YAML/static checks and, if reasonably bounded, the
checker-side finite-factor Schreier sanity function; never launch local GAP.

## Required hostile gates

1. Confirm the earlier generator/element indexing bug is truly gone: the
   Schreier words must be evaluated at the actual `(x9,y9)` and `(x4,y4)`, not
   `elements[0:2]` where element zero is identity.
2. Prove or reject the mathematical certificate.  With
   `C=< (x9,x4),(y9,y4) > <= G9 x PSL`, show that the section-edge Schreier
   relators generate `ker(F(x,y)->G9)`, and that their PSL images generating
   order 504 implies `{1} x PSL <= C`; together with the G9 projection this
   must imply `C=G9 x PSL`.  Check word orientation and inverse conventions.
3. Check that every one of the 972 target generator pairs descends to
   endomorphisms of both factors.  Explain why the direct-product certificate
   then implies membership and a well-defined endomorphism of the actual
   compact roof, closing the prior subdirect-product hole.
4. Re-audit the 972x972 product reconstruction, identity/inverses/order and
   square/cube/exponent derivation, and the generator-action associativity
   argument.  Reject circular dependence on the producer table or GAP
   `GroupHomomorphismByImages`.
5. Confirm runtime source binding, fixed transitive Reads, QUIT-free core,
   workflow manual dispatch, hashes, artifact/source binding, receipt
   completeness, and fail-closed outside-label status.
6. Mutation tests: describe or execute bounded mutations for wrong actual
   generator, one Schreier edge, wrong kernel order, one target action, and one
   product cell.  Each must be rejected by an independent gate.

## Verdict

Return exactly one:

- `PASS_POWER_SPECTRUM_V2_POSTSCHREIER`
- `BLOCKER: <minimal exact defect>`

Do not infer A/B and do not call any finite all-pass a B proof.
