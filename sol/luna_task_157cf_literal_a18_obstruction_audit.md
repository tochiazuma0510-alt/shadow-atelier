# Luna task 157cf: adversarial audit of repaired literal-A.18 obstruction

## Scope

Independently audit, without editing, the repaired 157ca bundle:

- `search/d972_b4_next_obstruction_v1.py`
- `search/check_d972_b4_next_obstruction_v1.py`
- `.github/workflows/d972-b4-next-obstruction-v1.yml`
- `sol/luna_reply_157ca_next_finite_obstruction.md`

Write only `sol/luna_reply_157cf_literal_a18_obstruction_audit.md`. Do not run
GAP, heavy local enumeration, Git, or GHA.

## Required audit

Check the mathematical implication and implementation adversarially:

1. The quotient ideal must be the 18 K(0,5) prefix relators plus all five
   literal raw A.18 coface images of the 28 marked-M seeds. It must not silently
   reuse the separated rho-orbit tail.
2. The evaluated obstruction must be the unconditional five-coface pentagon
   defect with the paper's multiplication/inverse convention. Explain why a
   genuine lift reducing to the frozen roof row forces it to vanish modulo the
   literal ideal, even when the frozen representative word itself is not in F2'.
3. Producer and checker must independently reconstruct source rows, maps,
   ideals, and all 972 defects; no shared helper. Confirm exact digests against
   the existing A.18 semantic-separation sources.
4. Every relator, binding, construction, shard coverage, digest, or stale-rho
   mismatch must fail closed even if the defect list is empty. Mutate at least
   one bounded fixture for each important fail-open class.
5. d2--d6 workflow coverage, shard merge independence, source hashes, YAML and
   embedded shell/Python, artifact upload, and status/marker agreement.
6. A checked nonzero row is only a finite A obstruction candidate for parent
   theorem audit; all-pass is nonterminal.

Run only light selftests/AST/YAML and the documented bounded d2 smoke. Return
`LITERAL_A18_OBSTRUCTION_AUDIT_PASS` or `..._FAIL` with exact line references
and hashes.
