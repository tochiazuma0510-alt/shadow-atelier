# Task723 audit — Task717 endpoint-minimal v4

## Verdict

`PASS_TASK640_ENDPOINT_MINIMAL_V4_SAFE_FOR_GHA`

`SAFE_TO_DISPATCH_GHA=yes`

No release-critical blocker was found in the Task717 v4 producer/checker
scope.  This is a release audit only: no real parent, 59,049-entry build,
GHA dispatch, or git operation was performed.

`REAL_TASK640_RUN=DEFERRED_TO_GHA`

`FRESH_RHO2=NOT_PRODUCED`

`verified=false`

## Frozen receipts

| file | bytes | LF | final LF | SHA-256 |
|---|---:|---:|---|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 43,758 | 670 | yes | `faa63bfd57629855101038c694130277b9c9d47120105341f9e89d12c8c3df08` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 93,236 | 1,592 | yes | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| `sol/proof_r07_task640_endpoint_minimal_runtime_v484.md` | 6,571 | 159 | yes | `25e292c8d996000c5dd442619f9afa269d83193ce5f58e4f3536c55b61f77492` |
| `sol/luna_task_717_r07_task640_endpoint_minimal_runtime_v4.md` | 5,141 | 112 | yes | `4f1016f6fa5b55067752c91cc86651b00af50d21e4f6785fdc7ba03dbed778ea` |
| `sol/luna_reply_717_r07_task640_endpoint_minimal_runtime_v4.md` | 3,631 | 85 | yes | `1e0d117a6fb7accc6b568e92bf6e74f9d1c34e8c133ab9e9ca30ff2912295cfd` |
| v3 producer baseline | 31,609 | 383 | yes | `8719929bfd6d134320da8c6fc1a8df527f458c1523f8edb0330b539649097206` |
| v3 checker baseline | 92,071 | 1,563 | yes | `889b7c7753e53e9c73c5edd575443446b0e3051794d6f20356809244c57cbd32` |

The imported arithmetic pins were also remeasured: Task565 prebuild
`acffa38731a28d85539f765537010e6bf20f55c7f7feae0099d56c58c808ffc8`, frozen
v12f `22d2ebda554cfacc78393dda7f43a9a6550e7f134dd8f44f87ab0f62241bbbbb`,
and `scratchpad/a0_paper_words_v1.json`
`90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893`.

## 1. Producer endpoint call graph

The production path is `main -> evaluate -> load_all_seven(words) ->
build_endpoint_minimal`.  The AST reachability audit over that path found 23
local functions and zero calls to any of:

`build_light`, `build_roster`, `producer_exact_target`, `JointGroup`,
`build_base_rows`, `build_pb3_boundary`, `build_pb4_boundary`,
`generic_runtime_model`, or `build_heavy`.

The dynamic frozen `ProducerAllSeven` constructor, `coordinates`, and
`direct_column` methods were checked separately in pinned v12f; their
forbidden-call set is also empty.  `JointGroup.eval` was inspected only as
the reference equation, not instantiated by the endpoint path.  The only
`TinyGeneric` and generic-builder trap definitions are under v4 selftest
lines 470–548 and 599–607; they are outside the production entry path.

`load_all_seven` verifies the v12f digest, executes it under a non-main module
name, snapshots the pinned sources, and calls only the endpoint builder
(lines 249–262).  The builder's actual order is:

1. source authentication and checkpoint (198–199);
2. `live`, `task176`, `old`, and `q3` loads/owner authentication (201–206);
3. exact `e3,e4` reconstruction (208–209);
4. `cheap_context_registry(e4)` plus the 31-row/46-name receipt validator
   (211–215);
5. the supplied 760-letter `g760` length/digest gate (216–220);
6. the endpoint fine deletion install, with before/after checkpoints
   (230–232);
7. `EndpointMinimalJointEvaluator`, frozen `ProducerAllSeven`, and its
   zero-word canary (234–245).

No generic module is loaded: `joint`, `v172`, `g760`, and `pb4` remain only
authenticated snapshots.  The endpoint runtime retains only the live,
task176, old, e3/e4, contexts/aliases/receipt, q3 owner, meter, g760 bridge,
deletion, and lightweight evaluator objects.  The profile gate rejects the
generic runtime keys before deletion/evaluator installation.

The explicit fake-runtime trap is wired through the production installer and
profile validator: the bounded run reported
`build_heavy_trap_called=false`, `generic_builders_called=false`, and
`forbidden_runtime_rejections=1`.  The AST result above is the authority for
the actual builder call graph; the trap is not treated as a substitute for
that static closure.

## 2. Retained endpoint data and evaluator

`validate_context_registry` requires exactly 31 ordered context rows, exactly
46 named uses, exact aliases, both receipt digests, and serializer-bound
left/right elements (lines 131–164).  `validate_q0_marked` requires exactly
two physical 36-point permutations (166–179).  The installer calls the
accepted `p176.build_fine_deletion(e3,e4,meter)` once and requires its public
`source_order == 59049` before passing the table to `make_deleter` (265–280).

The evaluator at lines 112–123 has the exact v484 product:

```text
J.identity = (e3.identity, (e4.identity for each of 31 contexts))
J.eval(w) = (e3.eval(old.embed_f2_pb3(w)),
             (e4.eval(w, context_i) for i=0..30))
```

It stores all 31 contexts in order and exposes no multiplication, closure,
roster, or sampled-signature operation.  The pinned generic reference
`JointGroup.eval` at v12f/joint lines 244–247 has the same evaluation and
identity convention.  Frozen `ProducerAllSeven.direct_column` then performs
the unchanged `conjugate = delta + relator + inverse(delta)` reduction and
tests exactly `joint_group.eval(conjugate) == joint_group.identity`.

The producer fixture compared the lightweight and tiny generic evaluators on
14 cases (empty, four-actor/nontrivial words, and the eleven occurrence
probes), and rejected both an E3 mutation and a 31-context E4 mutation:
`joint_equality_cases=14`, `joint_mutation_rejections=2`.

## 3. v3/v4 arithmetic and schema regression

An AST function diff against v3 found only these producer changes:
`load_all_seven` receives the already authenticated words, the endpoint
installer validates the two Q0 rows, `evaluate` adds the exact v4 profile and
schema, and selftest gains the v4 fixtures.  All signature, eleven-occurrence,
first-six restriction, direct-column, precision-two, lower-zero, packing, and
rho2 arithmetic functions are unchanged.

The checker diff against v3 likewise found only the v4 schema/marker, the
exact profile gate/profile key, v4 selftest coverage, and checker verdict
schema.  Its local affine/Fox/endpoint/signature/direct-column/precision-two
arithmetic is unchanged.

Producer and checker profiles are AST-equal and contain the same endpoint
values: contexts `31`, named uses `46`, fine source order `59049`, Q0 marks
`2`, generic-presence flags all `false`, v484 proof pin above, v12f/prebuild/
word pins above, and g760 object digest
`518f09820b8d7baee6b58ebf366cebf7b02a9a945cd1350cf8c701a4e6bc2b4d`.
Dimensions remain lower `32260`, top `48384`, packed rho2 `12096`; occurrence
types/order remain six E3 then five E4, coordinates
`(0,1,2,3,0,4,5,6,7,8,9)`, and signs
`(1,-1,1,-1,-1,1,1,1,1,-1,-1)`.  All terminal claim flags remain the v3
false/null boundary.

## 4. Independent checker and terminal

The checker imports only its own local arithmetic and standard/numpy modules;
there is no producer or v12f import/exec path.  `SevenSources` authenticates
its independent old/joint/v172/g760/pb4/q3 pins, `LocalQ` reconstructs the
quotients locally, and `IndependentAllSeven` independently replays the ten
endpoint coordinates, all eleven occurrence/direct-column relations, path
signatures, buckets, and precision-two target/replay.

`validate_payload` first requires canonical bytes, v4 schema/marker, the exact
profile, parent/claim bindings, every receipt byte/SHA, independent path and
bucket replay, dense lower/top/packed equality, rho2 metadata, dimensions,
occurrence contract, and all manifest keys (495–567).  Thus a coordinated
producer profile mutation cannot pass via peer metadata; the checker fixture
rejects a changed profile (`profile_mutations=1`).  The complete checker
selftest reports `mutation_count=44`.

The terminal marker is emitted only after `validate_payload` returns, the
parent receipt and dimensions are checked, and the complete v4 checker verdict
is serialized (main lines 1582–1586).  No acceptance marker is emitted on a
validation exception; the verdict itself retains `cross_checked=false` and
`verified=false`.

### Task625 rerun equivalence

The expensive `Rerun exact Task625 checker and compare uploaded verdict` step
can be omitted in a v10-style workflow without changing the mathematical
input gate, provided the workflow still authenticates the exact GitHub
run/attempt/artifact and both v4 programs retain their local content gates.

The producer's `auth_parent` (339–366) and checker's `auth_task601` (320–349)
each independently require the canonical fixed Task625 manifest SHA
`381f961fc808076c5c0adbc98e32c19742565087bffbcd5f99772533e05d5c22`, all
declared payload file names/bytes/SHA values, the canonical roots/literal-leaf
replay and required route/claim values, and the exact 1,120-byte canonical
Task625 verdict SHA
`a650aa8d5d78f52145fff5ba7769ad2036cfd16e90e3caaf367b4517e07d2740` with
marker `R07_GRADE1_SELECTED_SLP_V2_CHECKER_PASS`, cursor `8059`, coefficient
count `3317`, and `verified=false`/`cross_checked=false`.  Both also require
`task625-replayed-verdict.json` to be byte-identical to that verdict and
rebuild the fixed roots/leaves/claim boundary; neither treats a peer verdict
as an unchecked Boolean.

Therefore artifact/run identity plus these two independent fixed-content
re-authentications is input-gate equivalent to rerunning Task625 for this
fixed accepted artifact.  Artifact identity alone, or either side merely
blindly trusting the uploaded verdict, would not be equivalent and would make
the rerun mandatory.  This finding does not authorize any workflow edit in
this audit.

## 5. Bounded commands/results

Only the requested bounded checks were run:

```text
python -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v4.py search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py
exit 0
```

Producer `--selftest` exited 0 and emitted:

```json
{"actor_multiplication":"PASS","build_heavy_trap_called":false,"coefficient_2":"PASS","context_order":31,"endpoint_ceiling":484,"endpoint_fine_source_order":59049,"endpoint_installer":"PASS","first_six_shift_mutations":1,"fixture":"PASS","forbidden_runtime_rejections":1,"g760_length":760,"generic_builders_called":false,"inverse_action":"PASS","joint_equality_cases":14,"joint_mutation_rejections":2,"leaf_live_mutations":4,"occurrence_components":11,"q0_marked_rows":2,"rho2_bytes":12096,"runtime_profile_mutations":1,"seed_cache_bytes":10644832,"wrong_fine_order_rejected":1}
```

Checker `--selftest` exited 0 and emitted:

```json
{"actor_multiplication":"PASS","coefficient_2":"PASS","endpoint_ceiling":484,"fixture":"PASS","inverse_action":"PASS","mutation_count":44,"occurrence_components":11,"rho2_bytes":12096}
```

No real 59,049-state deletion, parent construction, or fresh rho2 output was
run or produced locally.  The endpoint removes the v9 generic light-runtime
prelude; the remaining fine table is constructed once in the intended GHA
path, contexts are constructed once, and no 6,441 roster/base-row/PB-boundary
owner or generic target/model is retained.  I found no obvious release-time
performance regression.

The physical receipt of this audit reply is supplied by the parent handoff
after the file freeze (self-SHA is necessarily self-referential).
