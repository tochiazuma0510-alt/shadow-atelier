# Luna Task735 -- Task640 one-call owner-binding hotfix v5

```text
RESULT=COMPLETE
REAL_RUN=DEFERRED_TO_GHA
verified=false
```

Created the versioned producer successor with the single commissioned owner
binding repair.  The independent checker, workflow, arithmetic, runtime
profile, payload protocol and CLI were not changed.  No real parent, GHA or
git operation was used.

## Exact v4 to v5 diff

```diff
     q3 = registry.json('q3')
-    q3_owner = validate_q3_literal_owner(q3)
+    # v5: bind the Q3 literal-owner validator to the pinned v12f module.
+    q3_owner = module.validate_q3_literal_owner(q3)
```

An exact byte normalization check deleted that one comment and changed the one
qualified call back to the old unqualified call; the resulting bytes equalled
v4 exactly.  There are no other changes.  In particular:

- the builder still receives `module` as its first parameter;
- the validator body was not copied, caught, loosened or given a fallback;
- payload schema `d972.r07.a0.fresh-precision2-endpoint-signature.v4` and
  marker `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CANDIDATE` remain exact;
- the `endpoint-minimal-v4`/v484 profile, 31 contexts, 46 named uses, full
  59,049 fine deletion, two Q0 marked rows, all hashes, caps and CLI are
  byte-identical to v4;
- the unchanged independent checker-v4 interface therefore remains the
  consumer of the v5-produced v4-compatible payload.

## Exact receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `sol/luna_task_735_r07_task640_owner_binding_v5.md` | `2194` | `62` | yes | `0e0fc50fa84cb4de4b90cb7dd9d45e584afd14b956c4ec5398ffb551186f1608` |
| `sol/proof_r07_task640_v10_missing_owner_binding_v488.md` | `2232` | `70` | yes | `e07d52e7864042d1a3fe22538b4ba408d7cc56721135b07c34b4111e726cf763` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | `43758` | `670` | yes | `faa63bfd57629855101038c694130277b9c9d47120105341f9e89d12c8c3df08` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py` | `43838` | `671` | yes | `2f8cb910c79cb6046c8cd7a83f77e9e883187fe81b43209e3a8d09679a12ad6b` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | `93236` | `1592` | yes | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| `search/d972_r07_history_free_positive_fast_resume_v12f.py` | `343155` | `6472` | yes | `22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb` |

The reply's own receipt is supplied externally after sealing to avoid a
self-referential digest.

## Bounded checks

Bytecode caches were directed to fresh directories under the system temporary
directory, outside the repository.

```text
python -B -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py
exit 0

python -B search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py --selftest
exit 0
fixture=PASS
context_order=31
endpoint_fine_source_order=59049
q0_marked_rows=2
endpoint_installer=PASS
build_heavy_trap_called=false
generic_builders_called=false
occurrence_components=11
endpoint_ceiling=484
rho2_bytes=12096

exact normalized v5-to-v4 byte comparison
PASS; one comment plus one qualified call only

static/import owner check
v12f_sha256=22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb
v12f_validate_q3_literal_owner_callable=true
builder_parameters=module,registry,meter,words
qualified_owner_calls=1
unqualified_owner_calls=0
PASS
```

The import-only check supplied an in-memory `resource` namespace on the
native Windows host because the pinned production module imports that
POSIX/Ubuntu standard module.  No resource function, parent loader or runtime
builder was executed.

The failed run `33811630349/1`, job `100834536849`, remains an input/binding
stop rather than a mathematical negative.  This task did not rerun it or
produce rho2.

```text
REAL_RUN=DEFERRED_TO_GHA
grade2_MEMBER=false
grade2_NONMEMBER=false
A0=false
ORDER_54432=false
full_Q0=false
COMMON=false
cofinal_lift=false
FAKE=false
IHARA=false
cross_checked=false
verified=false
```
