# Sol(max) Task 566: adversarial audit of the grade1-to-grade2 split handoff

Author: Sol / 2026-09-03

## 1. Role and scope

Act as an independent mathematical auditor.  Audit the complete file

```text
sol/proof_r07_grade1_to_grade2_split_presentation_handoff_v450.md
bytes 7649
sha256 48acc55a73aba140aa73098791d73f936f1b46fc5316d6f56e668be242fdc630
```

against v441, v444, v446--v449, the audited grade-one v3/v4 state schema,
and the mathematical portions of Tasks 553, 558, 560 and 563.  The point is
to decide whether the already completed prepare plus four block states really
determine a complete `T1` and permit target-independent grade-two module work
before the grade-one physical terminal.  This is not an audit of the live GHA
result and not a request to rerun any computation.

## 2. Required adversarial checks

Check, in order:

1. that the four old character bases and four pure-grade defect bases form
   the stated direct basis of `U1`, without silently treating associated-grade
   projectors as idempotents on the full filtered module;
2. that the split records actually determine reductions of the 44 original
   seeds, rather than only 176 projected seeds;
3. that old-row actor transitions can be reconstructed from the old
   transition plus all projected transition-defect reductions, with correct
   signs, projector words and global indices;
4. that block actor transitions cover new rows and that every ancestry DAG is
   well founded and literal-bearing;
5. whether prepare plus four blocks suffice, or whether any merge-only datum
   is needed to build `T1`, `H^[2]` or the target-independent physical fibre;
6. the claim that the grade-two canonical fibre is target-independent;
7. exact dimensions: four source blocks of 36,288, joint new physical 48,384,
   lower physical 32,260 and packed residual 12,096 bytes;
8. the requirement to recompute `rho2` independently from the checked literal
   `c1`, and whether any additional PB3/PB4/exponent or cocycle gate is absent;
9. whether a grade-one NONMEMBER correctly forbids the result-dependent join
   while leaving only a target-independent module computation; and
10. every claim-boundary sentence, especially the distinction between
    paper-closed, cross-checked and Lean-verified.

Try to construct a small linear counterexample to every questionable
direct-sum or reconstruction step.  Distinguish a repairable serialization
gap from a mathematical failure.

## 3. Output contract

Write only:

```text
sol/sol_reply_566_audit_r07_grade1_to_grade2_handoff_v1.md
```

Do not edit the proof, implementation, workflows, v220 or provenance.  Do
not run heavy computation, GHA, git commit/push, or local parallel Python.
Small hand calculations or a seconds-scale temporary checker outside the
repository are permitted but must be disclosed.

Give exact findings and one final verdict:

```text
GRADE1_TO_GRADE2_HANDOFF_PASS
GRADE1_TO_GRADE2_HANDOFF_PASS_AFTER_REPAIR
GRADE1_TO_GRADE2_HANDOFF_STOP
```

If repair is needed, provide replacement mathematical text or formulas precise
enough for the parent to incorporate without a second design round.  State
explicitly that no grade membership, A0, COMMON, cofinal lift, fake or Ihara
conclusion follows from this audit.
