# Luna reply 717 — Task640 endpoint-minimal runtime v4

## Result

Implemented the versioned v4 producer and independent checker.  The producer
uses the exact seven-step endpoint-minimal construction from proof v484; its
builder AST has no calls to `build_light`, `build_roster`,
`producer_exact_target`, or any generic builder.  The checker has no import of
the v4 producer or v12f and retains the independent v3 endpoint/signature,
direct-column, and precision-two replay.

## Changed files

| file | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 43,758 | 670 | yes | `faa63bfd57629855101038c694130277b9c9d47120105341f9e89d12c8c3df08` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 93,236 | 1,592 | yes | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |

## Runtime call graph

Retained: authenticated `live`, `task176`/p176, `old`, and `q3`; exact
`e3,e4`; the frozen 31-context registry and receipt; pinned `g760`; the full
Task700/703 deletion prefix (fine table plus two Q0 marks); the lightweight
`J.identity`/`J.eval`; frozen `ProducerAllSeven` coordinates, occurrence
columns, and direct columns; and the existing precision-two arithmetic.

Omitted: JointGroup Cayley closure, 6,441-row roster, raw H1/H2/P Fox rows,
PB3/PB4 boundary row families, generic producer target, generic runtime model,
Q0 search states, and all post-deletion heavy owners.  The static v4
`runtime_profile` binds these omissions, contexts=31, fine source order=59049,
Q0 marked rows=2, the v484 proof digest, v12f/Task565/word pins, and all
generic-presence flags false.

The builder emits these resource-checked progress phases, in order:

```text
endpoint_minimal_start
endpoint_minimal_step_1_source_authentication
endpoint_minimal_step_2_load_sources
endpoint_minimal_step_3_reconstruct_quotients
endpoint_minimal_step_4_context_registry
endpoint_minimal_step_5_g760_pin
endpoint_minimal_step_6_fine_deletion_before
endpoint_minimal_step_6_fine_deletion_after
endpoint_minimal_step_7_joint_evaluator
endpoint_minimal_step_7_zero_word_canary
```

The bounded selftests do not enter the real seven-step builder and therefore
do not construct the 59,049-state table.

## Bounded verification

Commands run, and results:

```text
python -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py
  PASS

python search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py --selftest
  PASS; leaf_live_mutations=4; first_six_shift_mutations=1;
  wrong_fine_order_rejected=1; joint_equality_cases=14;
  joint_mutation_rejections=2; generic_builders_called=false;
  forbidden_runtime_rejections=1; runtime_profile_mutations=1;
  g760_length=760; context_order=31; q0_marked_rows=2;
  endpoint_fine_source_order=59049

python search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py --selftest
  PASS; mutation_count=44; coefficient_2=PASS; occurrence_components=11
```

The producer fixture compares lightweight and tiny generic joint evaluation on
empty, four-actor, nontrivial-conjugate, and all eleven occurrence descriptors;
mutating one E3 component and one of 31 E4 contexts is rejected.  The generic
builder trap was not called.  The checker rejects a v4 schema/marker/profile
mutation and retains all prior leaf, sign/order, endpoint, and coefficient-2
fixtures.

No real parents, GHA, git, or actual 59,049-state deletion was run.

```text
REAL_TASK640_RUN=DEFERRED_TO_GHA
FRESH_RHO2=NOT_PRODUCED
verified=false
```
