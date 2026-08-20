# 157eh — B345 full-D2 dual correlation monitor-scope repair

## Role and authorized scope

Luna implements one versioned repair of the already frozen 157eg lane.  Create
only these four new files:

1. `search/d972_b345_full_d2_dual_correlation_v2.py`
2. `search/check_d972_b345_full_d2_dual_correlation_v2.py`
3. `search/d972_b345_full_d2_dual_correlation_gha_driver_v2.g`
4. `sol/luna_reply_157eh_b345_full_d2_monitor_scope_repair.md`

Do not edit v1, a workflow, q3, any predecessor, the permanent guard, or any
other file.  The GAP driver is ASCII only.  Temporary fixtures and logs stay
outside the repository.  Do not run the full mathematics locally.  Run one
bounded combined producer/checker self-test only after the four-file static
freeze and hostile audit; record any corrective rerun and its exact fixture-only
reason.

This is a monitor/stage adapter repair.  The mathematical question, frozen
prefix, raw-lambda construction, 76-occurrence correlation loop, ordering,
terminal meanings, caps, and claim boundary are byte-semantically unchanged.
Do not add a search, another candidate family, an E4 enumeration, caching, or
another basis-growth lane.

## A. Frozen v1 and exact GHA evidence

Hard-authenticate the following v1 bundle before production work:

- producer `search/d972_b345_full_d2_dual_correlation_v1.py`, SHA-256
  `6903b745be2c005c573d7a368beb826d5f411f0f4a353eeedf3a8cccbc9fde52`,
  78832 bytes;
- checker `search/check_d972_b345_full_d2_dual_correlation_v1.py`, SHA-256
  `311dc9413012542e489c9b2b7cd38e6008b81b6b8854e5e49d8d56285a457358`,
  66571 bytes;
- driver `search/d972_b345_full_d2_dual_correlation_gha_driver_v1.g`,
  SHA-256
  `c0a0626f4ea15616bfef3b5916740c23c86a0f87760a98b0ff3d8da923db65b4`,
  11980 bytes;
- canonical 157eg task
  `sol/luna_task_157eg_b345_full_d2_dual_correlation.md`, SHA-256
  `22b649c178ea1a821a5d67973b39c58f6a7395b6bc6a407a36a493f9ce19720e`;
- final 157eg reply
  `sol/luna_reply_157eg_b345_full_d2_dual_correlation.md`, SHA-256
  `12a1e5feafebe97d694b15c09063a50fac7a471d0528c0f210373c18c9a0445f`,
  9795 bytes.

The v1 bundle was committed and pushed as
`d97cd897ca7137deae4276caf9a1e98c71fe7c05`.  The following GHA evidence is
provenance, not mathematical input:

- run `32368735249`: combined producer/checker self-test PASS, 47 seconds;
- run `32368850435`: dispatch-only failure because the v1 driver required an
  externally supplied fixed output variable;
- run `32368985968`: dispatch-only failure because `gh workflow run -f`
  stripped the inner GAP string quotes;
- run `32369164205`: q3 producer and independent q3 checker PASS, then the
  157eg producer entered the fresh prefix and stopped after about 2m23s with
  `RuntimeError: monitor phase registry`.

The last stack is exact and load-bearing:

```text
157eg run
  -> 157ed build_instrumented_prefix
  -> strong.build_fresh_prefix
  -> SparseBoundaryBasis.add_column
  -> ProvenanceDAG.leaf/_append_node
  -> monitor.check("packed_provenance_dag_growth")
  -> v1 Monitor.check rejects the label
```

No correlation pair was evaluated and no lift/obstruction result was produced
by that full run.  Do not describe it as mathematical evidence.

## B. Root cause and forbidden repairs

The v1 monitor tries to infer an outer receipt phase from an inner callback
string.  This is unsound because imported helpers reuse inner labels in more
than one outer stage.  In particular `proof_DAG_array_bytes`,
`proof_DAG_base64`, and `proof_DAG_base64_complete` occur both while finalizing
the fresh prefix and while serializing an ACTIVE section witness.  Mapping a
string such as `proof_DAG_*` to one outer phase therefore misclassifies the
other call site.

The following repairs are forbidden:

- adding only `packed_provenance_dag_growth` to the v1 allow-list;
- `startswith("strong_")`, `startswith("affine_")`, or
  `startswith("proof_DAG_")` acceptance;
- a global `inner_string -> outer_string` map;
- resetting or extending a deadline when entering an imported helper;
- letting the checker accept a wider dormant label universe;
- changing a cap, cadence, mathematical predicate, or terminal claim to make
  the run pass.

## C. Exact closed outer/inner registry

Use this exact producer registry.  Both strings and pair membership are
semantic receipt data.  Sort outer names and each inner list before hashing.

```text
authenticated_input:
  authenticated_input

fresh_immutable_prefix:
  fresh_immutable_prefix
  strong_wform_fresh_BFS
  strong_wform_directed_round
  packed_provenance_dag_growth
  packed_pivot_column_elimination
  packed_target_sparse_elimination
  proof_DAG_array_bytes
  proof_DAG_base64
  proof_DAG_base64_complete

raw_lambda_oracle:
  raw_lambda_oracle
  raw_lambda_reverse_dp

base_columns:
  base_columns

dual_correlation:
  dual_correlation

section_witness:
  section_witness
  proof_DAG_array_bytes
  proof_DAG_base64
  proof_DAG_base64_complete
```

The section-witness set is intentionally smaller than the fresh-prefix set.
The frozen v1 `make_section_witness` reconstructs the target Fox prefix and a
typed section expression, then calls `serialize_reachable`; it does not call
`basis.solve_with_blocker`, mutate the provenance DAG, or run packed target
elimination.  If implementation tracing finds a different active call in the
frozen v1 source, stop and report the exact line/call tree rather than silently
widening the table.

Reject every other pair, including dormant `affine_*`, generic
`provenance_dag_growth`, `fixed_context_*`, and invented `proof_DAG_*` names.
The same inner proof-DAG name under two registered outers is valid precisely
because the outer is explicit.

Publish the exact registry and its canonical SHA-256 in every production
receipt.  The producer schema and checker must require the exact table and
digest in every terminal, including INPUT and RESOURCE stages where available
after static authentication.  The checker owns the constant independently; it
must not derive its expected table from the producer receipt.

## D. One base monitor plus phase-pinned adapters

Replace v1 `_outer_phase` guessing with one stateful base `Monitor` and a small
phase-pinned adapter (for example `BoundMonitor`).  The design invariant is:

```text
one base clock + one RSS/accounting state + many immutable outer scopes
```

The base monitor alone owns:

- `started` and absolute `deadline`;
- `initial_seconds`;
- cadence/check count;
- peak RSS and hit reason;
- local deadline/RSS cap enforcement.

The adapter is constructed from `(base, outer)` and obtains its immutable
allowed-inner frozenset from the canonical registry above.  A caller may not
supply or widen an arbitrary allowed set.  If the implementation accepts an
allowed set for testability, it must require exact equality with the canonical
set for that outer before storing it.  The adapter must expose the actual
imported-helper API:

```text
.started
.check(inner, force=False, **kwargs)
.reserve(inner, additional_bytes)
```

`.started` is the same base value, not a copy with a new epoch.  Both methods
first require exact `(outer, inner)` membership, then delegate to the same base
counter/deadline/RSS state.  A local resource exception always carries the
pinned outer receipt phase; it never guesses from `inner`.  `reserve` is not
optional: the proof-DAG serializer calls it before base64 construction.

Use adapters as follows:

- pass the fresh-prefix adapter to `ed.build_instrumented_prefix`;
- pass the raw-lambda adapter to `ed.RawLambdaOracle`;
- pass the section-witness adapter to `make_section_witness`;
- use the base monitor's explicit outer check for authenticated input,
  base-columns, dual-correlation, and other v2-owned registered stage
  boundaries.

Receipt serialization is not a monitor stage in v1 and is intentionally absent
from the exact pair registry.  Preserve its existing local byte-cap,
`write_checked`, and RESOURCE fallback without adding a monitor check.

Do not expose adapters to a wider stage.  The frozen prefix builder stores its
monitor in both `prefix["dag"].deadline` and `prefix["basis"].deadline`.  On
successful return, require both fields to be the exact fresh adapter, then set
both to `None` before entering raw-lambda or any later stage.  Require them to
remain `None` thereafter; later read-only basis access must not silently reuse
the fresh scope.  Do not retain an adapter in a global or otherwise reuse it
after its outer stage.  `old.ResourceStop`/`ed.ResourceStop`
conversion remains bound to the explicit current outer selected by the caller;
an inherited `exc.phase` is diagnostic only and may not choose the public
terminal phase.

Keep the existing local/upstream cap-source split, exact reachable upstream
registry, reason==cap_key rule, serialization fallback, and shared absolute
18,000-second budget.  This task does not authorize altering any of them.

## E. Production behavior and receipt boundary

Normal production output must remain mathematically identical to v1 except for
version/schema identifiers and the new monitor-scope binding.  Preserve:

- fresh prefix counts 32768 BFS, 207 directed translations, 362725 columns,
  362709 pivots, 16 dependent columns, 3090367 live entries;
- raw-lambda 362710 entries and 2727658 tail visits;
- base target-6 lambda value 2;
- the exact 76 base-column occurrences and digest;
- correlation order `(translation canonical blob, relator index)`;
- formula `t=g*h^-1` and left action;
- complete scan before ACTIVE/SEPARATOR selection;
- zero pool/basis/DAG/section mutation during correlation;
- ACTIVE as a diagnostic translation, not a lift;
- SEPARATOR only as the pinned-E4 full-D2 conclusion already stated in 157eg;
- UNKNOWN_RESOURCE and UNKNOWN_INPUT as nonmathematical terminals.

For a monitor-origin RESOURCE receipt, the public phase must be the explicit
outer scope.  The inner label may be included only as a bounded diagnostic
field with exact schema; it must be checked against the registered pair and
must never drive the terminal.  For inherited structural caps, retain the
existing cap-source/reason/current contract.

No candidate-local persistent state is introduced.  No receipt, pool, basis,
DAG, or lambda state from runs `32368735249`--`32369164205` may be imported.

## F. Required bounded shared-core self-tests

The final v2 producer and independent checker self-tests must exercise the
production monitor registry/adapter/schema paths, not a separate permissive
fixture validator.  At minimum require:

1. every registered `(outer,inner)` pair is accepted and every unregistered
   cross-pair is rejected;
2. dormant `affine_*`, unknown packed/proof names, and prefix-only labels under
   section witness are rejected;
3. the same `proof_DAG_array_bytes` inner label is run once through a fresh
   adapter and once through a section adapter; forced deadline/RSS exceptions
   expose `fresh_immutable_prefix` and `section_witness`, respectively;
4. two adapters share exactly one `started`, absolute deadline, check counter,
   peak RSS, and hit state; mutation attempting a reset/extension is rejected;
5. `reserve` and `check(force=True)` both preserve the pinned outer;
6. the frozen prefix initially retains the exact fresh adapter in both DAG and
   basis, the production detach helper clears both after the build, and any
   later callback through either detached object is impossible/rejected;
7. an actual frozen `ProvenanceDAG`/packed-DAG production helper creates enough
   nodes to cross its 1024-node cadence boundary and reaches
   `packed_provenance_dag_growth` through the fresh adapter.  Set the base
   cadence state so the callback actually samples wall/RSS; a ten-node toy that
   never invokes the callback is insufficient;
8. actual packed pivot and target reducer callbacks are bound to the fresh
   adapter (bounded toy columns are enough, but use the production helper);
9. actual section-expression serialization reaches all three proof-DAG
   reserve/check labels through both relevant outer adapters;
10. registry/digest, pair, outer-phase, inner-diagnostic, and stale-prefix
   mutations are independently rejected by the checker;
11. prior v1 fixture coverage remains: typed Element blob, packed section DAG,
    opcode/parent/value/role mutations, cap-source, shared deadline, exact
    provenance, and real receipt-serialization overflow fallback.

The combined test must emit exact v2 producer and checker markers once each.
Record the command, exits, marker counts, log path, and pre/post source hashes.
Do not run an extra test after PASS.

## G. Versioned driver and dispatch hardening

The v2 driver pins the final v2 producer/checker hashes and all frozen v1 and
q3 dependencies.  Preserve isolated q3 child, GAP 4.16.0/package gates,
pipefail+tee, exact sentinels, stale-output removal, exactly-one terminal, and
same-job independent checker.

Remove the redundant requirement that the caller define a quoted GAP output
path.  The driver owns one fixed v2 artifact path.  Full mode is selected by the
boolean RUN variable.  If an optional OUTPUT variable is present, require it to
equal the fixed path; if it is absent, proceed with the fixed path.  Self-test
mode remains exactly-one with RUN.

The reply must instruct the parent to use JSON workflow inputs rather than
`gh workflow run -f` for any preamble containing quotes.  Prefer a boolean-only
full preamble now that the output path is driver-owned.  This avoids repeating
runs `32368850435` and `32368985968` without changing a workflow.

## H. Recurrence guard and handoff

The reply must contain a short, explicit recurrence table:

| Repeated failure | Permanent v2 guard |
|---|---|
| callback label omitted from wrapper | trace active imported call tree and cross the real cadence threshold |
| reused inner label assigned to wrong stage | immutable outer-scoped adapter; no string inference |
| adapter resets budget | one base absolute deadline/RSS/check state |
| reserve path unimplemented | adapter proxies both `check` and `reserve` |
| self-test misses production callback | actual packed helper, >=1024 DAG nodes |
| shell strips quoted GAP input | driver-owned output path and JSON dispatch |

Before freeze: AST/py_compile, ASCII driver, exact hashes/bytes, placeholders,
whitespace/conflict markers, source pins, terminal markers, and dirty-worktree
scope.  Report exact file SHA-256/bytes.  The final reply marker is
`B345_FULL_D2_DUAL_CORRELATION_V2_READY_FOR_GHA_SELFTEST` only after the final
combined self-test passes.  Before then it must say
`B345_FULL_D2_DUAL_CORRELATION_V2_SELFTEST_UNCONFIRMED`.

Expected runtime after repair is unchanged: the failure was in monitoring, not
the correlation algorithm.  Give the parent a fresh estimate based on the
observed v1 prefix timing, but do not promise a lift.  The outcome still tells
us exactly whether the support-one qstar functional annihilates all full-D2
translates in the pinned E4 roof; it does not by itself construct a lift.
