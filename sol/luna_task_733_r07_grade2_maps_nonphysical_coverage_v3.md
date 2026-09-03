# Luna Task733 -- finite v3 repair for nonphysical actor coverage indexing

Role declaration: Luna.  Implement only the finite production failure below
in versioned producer/checker files.  Do not edit v2, do not run the actual
40-table build locally, do not create/edit a workflow, and do not perform git
or GHA operations.  Reply only to the specified file.

## 1. Exact observed failure

GHA run/attempt `33811487764/1`, job `100834098415`, head
`b805d4089d76ca98b3bbbc63594ce053ec90e5fa`, authenticated all inputs and
passed both bounded selftests.  The real producer then emitted all 20
forward/adjoint pairs in about ten seconds and failed only in
`structural_identities -> verify_coverage(T_fwd_a0_t0, physical=False)` with
`RuntimeError: coordinate_case_coverage`.

The finite cause is visible in both accepted v2 sources.  A nonphysical
destination is decoded as

```text
(tag, component, monomial, psl_index),
```

but the shared coverage helper reads its component/monomial from tuple
indices 2/3, which are the physical tuple indices.  For a physical destination
the correct tuple is

```text
(character, block, component, monomial, psl_index).
```

This is a post-build receipt assertion bug; no sparse map entry, actor action,
aggregation, transpose, inverse identity, or coordinate encoding failed.

## 2. Versioned repair

Create only:

```text
search/d972_r07_grade2_forward_adjoint_maps_v3.py
search/check_d972_r07_grade2_forward_adjoint_maps_v3.py
sol/luna_reply_733_r07_grade2_maps_nonphysical_coverage_v3.md
```

Start from the exact audited v2 files.  In each independent coverage helper:

- for `physical=False`, read destination component/monomial/PSL from indices
  `1/2/3` of `(tag,component,monomial,psl_index)`;
- for `physical=True`, retain indices `2/3/4` of
  `(character,block,component,monomial,psl_index)`;
- retain the existing source coverage, physical character/block coverage,
  all-six-monomial, both-component and all-504-PSL requirements.

Make the smallest necessary version/schema/marker/source-pin updates.  Finalize
the producer v3 bytes first; the checker v3 must pin and authenticate the exact
producer-v3 SHA/path, not v2.  Do not introduce a shared helper or import
between producer and checker.

## 3. Mandatory bounded regression

Extend both selftests minimally so they enter their own production
`verify_coverage` helper with the actual character-zero `T_fwd(x)` records and
require:

```text
source tags 0..5, components 0..1, monomials 0..5, PSL count 504;
destination tags 0..5, components 0..1, monomials 0..5, PSL count 504.
```

Add at least one live malformed nonphysical record mutation that makes one
required destination case disappear and is rejected by the same helper.  Keep
the existing actual B/prefix, inverse-pair, bool, source-pin, safe-output and
canonical-parser fixture coverage.  Do not construct the remaining 39 real
tables in selftest.

Run only `py_compile` and both bounded `--selftest` commands with bytecode
cache outside the repository.  Report elapsed time and rejection counts.  Do
not call either real `--emit` or real `--check` mode locally.

## 4. Claim boundary and reply

The v3 repair may state only that the finite coverage assertion is repaired
and the pair is a candidate for independent audit/relaunch.  It may not claim
an actual accepted map artifact, grade-two MEMBER/NONMEMBER, A0, COMMON,
compatible cofinal lift, fake, Ihara, or Lean verification.  `verified=false`.

Reply only to:

```text
sol/luna_reply_733_r07_grade2_maps_nonphysical_coverage_v3.md
```

Include exact v2/v3 diff scope and byte/LF/final-LF/SHA receipts for both v3
executables and the sealed reply.
