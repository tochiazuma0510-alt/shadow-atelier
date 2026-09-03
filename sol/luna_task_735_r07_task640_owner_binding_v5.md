# Luna Task735 -- Task640 one-call owner-binding hotfix

Role declaration: Luna.  Implement exactly the v488 repair in a versioned
producer successor.  Do not change the independent checker, arithmetic,
runtime profile, payload protocol, or workflow in this task.  Do not run real
parents, GHA, or git.  Reply only to the specified file.

## 1. Inputs and observed stop

Read fully:

```text
sol/proof_r07_task640_v10_missing_owner_binding_v488.md
search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py
search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py
search/d972_r07_history_free_positive_fast_resume_v12f.py
```

The exact failed run is `33811630349/1`, job `100834536849`, head
`2468d38778a411544a366bb85593296263facd97`.  It stopped at the first call to
an undefined unqualified `validate_q3_literal_owner`; the same pinned v12f
module passed into the builder owns that callable.

## 2. Output and permitted diff

Create only:

```text
search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py
sol/luna_reply_735_r07_task640_owner_binding_v5.md
```

The v5 file is an exact versioned copy of producer v4 except for:

```text
q3_owner = module.validate_q3_literal_owner(q3)
```

and the minimum version-identifying source comments needed to describe this
hotfix.  Retain the v4 payload schema, v4 candidate marker, v484 runtime
profile, all hashes, all 31 contexts, full 59,049 deletion, Q0 marks, resource
caps and CLI exactly, because the independent checker remains v4-compatible.
Do not copy the validator body, loosen it, catch its exceptions, or fall back
to another owner.

Add no new full-runtime selftest.  Run only `py_compile`, the existing bounded
producer `--selftest`, and a static/import check proving the pinned v12f module
has a callable `validate_q3_literal_owner` and the versioned builder's call is
qualified through its `module` parameter.  Keep bytecode cache outside the
repository.

## 3. Reply

Reply only to

```text
sol/luna_reply_735_r07_task640_owner_binding_v5.md
```

Give exact v4/v5 semantic diff, byte/LF/final-LF/SHA receipts, bounded results,
and false downstream claims.  State `REAL_RUN=DEFERRED_TO_GHA` and
`verified=false`.
