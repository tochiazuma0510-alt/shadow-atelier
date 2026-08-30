# Luna reply 408: A0 raw-row resume repair v29

Status: the minimal versioned repair and bounded in-memory fixture are
complete.  No production artifact was read or downloaded, and no production
run, GHA dispatch, commit, push, workflow edit, SAT mode, or SELFTEST detour
was performed.  No pre-existing file was changed.

## 1. Exact files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_batch64_v29.py` | 4,999 | `e3cf997b8aae78599e693652cf576083ae518b7a3690099c83b12d6e83039434` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_batch64_v29.py` | 2,332 | `0df0b765f00553cec696606b334022fe5953fa79a05076454aed8f05e45ce7c2` |
| `search/d972_r07_history_free_positive_fast_resume_batch64_gha_driver_v29.g` | 5,825 | `a72280933cab9543fc349c2dbc80cfb24436ddd56d167b7a2299928a665c6b7a` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v30.g` | 519 | `9ab3b687d5ba2ee6194895c5e39a80d246abeb912851813e5007a83a9cdf8a6f` |

The generated producer owner is 178,969 bytes with SHA-256
`8189065d10e484f0725a4df52ff8f63acd6702f3f727efd64ec07317d224ac41`.
The generated checker owner is 135,487 bytes with SHA-256
`ec3e9ef13a0d6be2cc629258f356e07a40414de5eca071bb88787ac4eb125640`.

The v30 GAP file is the generic `gap-run.yml` prefix adapter and reads the
exact-pinned, self-contained v29 batch driver.

## 2. Surgical repair

The producer hash-pins batch-64 v28 at 19,149 bytes / SHA-256
`ff26d11c23b45b70a1fc93d481bfd4f3dd66e6c106fd0afae140af81ec01ddf9`
and replaces only generated `_stream_record` semantics.

For every streamed record, v29 now:

1. checks symbol order/family and parses, canonicalizes, and hashes the stored
   `sparse_row` exactly as before; this remains the raw actual column;
2. checks stored sequential `rank_before` / `rank_after` and the stored DAG
   node range;
3. calls the frozen `FormalReducer.add_actual(raw_row, symbol)`, so the raw row
   is reduced by every preceding pivot, normalized, and assigned its formal
   DAG expression by the same owner used during original discovery;
4. temporarily detaches the meter only during this replay.  The already
   restored final hash-consed DAG table must satisfy every lookup; node-table
   length and the restored `dag_node_allocations` counter must remain exactly
   unchanged.  Any missing node is a typed `ProtocolStop`, not a resource
   fallback;
5. requires the freshly derived pivot and node id to equal `pivot_hex` and
   `pivot_node_id`, and requires the normalized pivot row, order, formal-entry
   count, and DAG-support count to advance by exactly one; and
6. appends the record only after all gates pass.

Thus the repair replays raw rows rather than incorrectly injecting them as
already normalized rows.  Two-phase streaming, batch-64 global merge and
single parent contributor scan, caps, checkpoint durability, correction
oracle, positive checker boundary, and terminal semantics are inherited
unchanged.  No second active-set scan was introduced.

The checker is only a hash-pinned successor of checker v28: it changes the
producer path/bytes/SHA and retains all prior row, scalar, contributor,
accounting, target, word, and kernel gates.

## 3. Regression fixture

The fixture uses a preceding normalized pivot row

```text
a + b
```

and a stored raw actual row

```text
a + c.
```

Sequential reduction gives `2b+c`, whose normalized form is `b+2c`.
Therefore raw minimum `a` differs from stored/derived pivot `b`, exactly the
shape that stopped run 33282364093.

The actual frozen reducer and generated `_stream_record` produced:

```text
A0_RAW_ROW_RESUME_FIXTURE_PASS raw_min=61 stored_pivot=62 normalized=62:1,63:2 old_inject=REJECT repaired=PASS fresh_dag_nodes=0 pivot_mutation=REJECT node_mutation=REJECT
```

The old direct `inject(stored_pivot, raw_row, ...)` rejects at the direct-P
gate.  With the final DAG table preloaded, repaired replay reconstructs the
exact stored pivot, normalized row, and node without allocating a node.
Changing the stored pivot and changing the stored node to a different valid
node are independently rejected.

## 4. Other lightweight gates

Both physical and generated Python sources compile.  Both `--help` paths
complete without loading production data.  Static generated-owner inspection
finds exactly one `_stream_record`, one call to `FormalReducer.add_actual`, no
direct `inject` in that function, one pre-record phase, one post-parse phase,
one inherited `materialize_batch`, and no batch replay cache.  Producer and
checker source pins agree exactly with the GAP driver.

Both GAP files are ASCII.  The following parse/fail-fast checks stopped
immediately, as expected, because the 1.66 GB prior artifact is absent:

```text
./gap.ps1 search/d972_r07_history_free_positive_fast_resume_batch64_gha_driver_v29.g
Error, task408 missing input
exit 1

./gap.ps1 search/d972_r07_history_free_positive_fast_resume_gha_driver_v30.g
Error, task408 missing input
exit 1
```

No shell/search output was created.  The driver uses the actual prior member
basename
`d972_r07_history_free_positive_fast_resume_v24_production.json.checkpoint.json`
and retains its 1,663,424,241-byte / SHA-256
`55c463335e89fb7e67a04ec9c0405a8216f6f909b2ce67a0fe7a8a4afaf2014d`
gate.  It also retains the 11,100-second external producer cap, 10,800-second
internal cap, 1,800-second checker cap, pipeline status gates, exactly-one
terminal gates, terminal equality, and sentinel.

## 5. Immediate dispatch path after parent commit

The existing registered workflow can hydrate the pinned prior artifact because
the v30 adapter matches its A0 driver prefix:

```text
gh workflow run gap-run.yml --ref <exact-commit-containing-v29/v30> \
  -f script=search/d972_r07_history_free_positive_fast_resume_gha_driver_v30.g \
  -f preamble='' -f out_dir=ci/out -f timeout_min=245 \
  -f with_pquot_packages=false
```

This command is recorded only; it was not run.

## 6. Claim boundary

This is an implementation candidate for resuming the authenticated heuristic
checkpoint and entering positive batch search.  It asserts no A0 common word,
negative result, lift, fake certificate, witness-type certificate, or Ihara
counterexample.  Production GHA and the independent verdict remain pending.

