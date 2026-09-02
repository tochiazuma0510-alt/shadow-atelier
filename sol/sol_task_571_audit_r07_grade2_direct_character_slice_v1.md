# Sol Task 571: audit the grade-two direct character-slice theorem

Author: Sol / 2026-09-03

Read v447, v451, v452, Task568's full reply, and
`sol/proof_r07_grade2_direct_character_slice_v453.md`.  Independently decide
whether Task565's stored source index is already the Fourier-character index
and therefore whether every pure-grade projector is exactly a direct slice,
not merely a four-word Walsh calculation.

Check the normalization over F3, the `(00),(01),(10),(11)` order, possible
upstairs kernel terms, all tag/component/monomial coupling, and the precise
once-per-run gates needed to make direct slicing fail closed.  Give a minimal
counterexample if any premise is missing.  Distinguish the paper theorem from
an unimplemented optimization.

Write only
`sol/sol_reply_571_audit_r07_grade2_direct_character_slice_v1.md`.  Do not edit
code/proofs/v220, run production, commit, push or dispatch.  End with exactly
one verdict:

```text
GRADE2_DIRECT_CHARACTER_SLICE_V453_AUDIT_PASS
GRADE2_DIRECT_CHARACTER_SLICE_V453_AUDIT_PASS_AFTER_REPAIR
GRADE2_DIRECT_CHARACTER_SLICE_V453_AUDIT_FAIL
```

No v220 numerator changes and `verified=false`.

