# Luna reply 380: A0 terminal-checkpoint v22

## Outcome

The smallest v22 successor is implemented.  Its generated producer owner is
v21 with exactly two source substitutions: the live-search checkpoint and
prepool checkpoint `serialized_dag_bytes` bookkeeping sites.  No arithmetic,
search order, pool, worker cleanup, resume, terminal, or mathematical claim
was changed.

```text
search/d972_r07_history_free_positive_fast_resume_v22.py
  3280 bytes
  1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01
crosscheck/check_d972_r07_history_free_positive_fast_resume_v22.py
  2066 bytes
  4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13
search/d972_r07_history_free_positive_fast_resume_gha_driver_v22.g
  8266 bytes
  8b8f2e9a1dc0b6a30e61ab8866c8d2393328a7038c22323873350d91d5b6531d
```

The reply identity is reported externally after its final bytes are fixed.

## Exact repair

At both load-bearing sites, v21 performed

```text
meter.bump("serialized_dag_bytes", estimated_json_size(body),
           "checkpoint_serialization")
```

`Meter.bump` calls `reserve`, and `reserve` calls `Meter.check`.  Thus a
terminal checkpoint entered after the 10800-second `ResourceStop` immediately
raised the same wall cap again before JSON serialization or atomic write.

V22 computes the same estimate once, adds it to the existing cumulative
counter, explicitly compares that total with the unchanged
`serialized_dag_bytes` limit, and only then calls the non-checking
`Meter.commit`.  Consequently an already-entered terminal serialization does
not re-enter the wall/RSS sampler at this bookkeeping site.

The following protections are unchanged:

- cumulative `serialized_dag_bytes` cap;
- estimated and actual `checkpoint_bytes` caps in `atomic_json`;
- sealed canonical JSON and atomic temporary-file replacement;
- clean worker abort/join requirement before a live terminal checkpoint;
- v21 optional single `--resume PATH` call and checkpoint owner validation;
- two-worker production owner and cleanup accounting;
- independent v21 checker logic, with only its exact producer pin raised to
  v22.

## Driver

The v22 driver accepts either no resume fields or the complete
path/bytes/SHA-256 triple and physically authenticates the resume input before
passing one `--resume` argument.  It retains the v20 raw-source pathname
required by the checkpoint `source.path` gate.

The producer remains bounded by 10800 internal seconds and 11100 external
seconds, leaving 300 seconds for terminal cleanup, serialization and receipt
transport.  Producer/checker byte pins, single terminal extraction, exact
terminal equality and typed-terminal grammar remain fail closed.

## Remaining honest checkpoint failure modes

This repair removes the observed recursive wall check at the two serialization
counter sites.  A checkpoint can still legitimately fail when:

- the cumulative serialized estimate exceeds `serialized_dag_bytes`;
- estimated or actual canonical JSON exceeds `checkpoint_bytes`;
- canonicalization/atomic filesystem write raises an OS or memory error;
- terminal cleanup is incomplete, so the existing live-checkpoint gate refuses
  to serialize an owner with live workers;
- checkpoint-body target replay allocates a new DAG node and its separate
  `dag_node_allocations` meter path re-enters a resource check;
- cleanup plus serialization exceeds the driver's remaining 300-second
  external timeout headroom or the process is killed externally.

The fifth case is outside the requested two-site repair.  In the observed run,
execution reached `phase=checkpoint_serialization`, so the identified failing
site was the removed `serialized_dag_bytes` bump rather than an earlier
checkpoint-body replay.

## Static checks

- Producer and checker wrappers passed `python -B` definition loading.
- Frozen v21 producer/checker byte and SHA pins, patch cardinalities, and
  generated-source compilation passed.
- The generated v22 producer was compared with generated v21: exactly the two
  registered substitutions account for the complete byte-length delta.
- The generated checker retains the v21 checker owner with only the v22
  producer path/bytes/SHA pin changed.
- GAP 4.16.0 `ReadAsFunction` parse-only passed with only expected unbound
  top-level-global warnings.
- All three executables are ASCII-only; driver pins and 10800/11100 bounds
  match the final files.
- No production run, heavy local run, GHA dispatch, git operation, SELFTEST,
  mutation campaign, retry, or unrelated audit was performed.

```text
TASK380_R07_A0_TERMINAL_CHECKPOINT_V22_IMPLEMENTED_STATICALLY_UNEXECUTED
PRODUCTION_TERMINAL_NOT_RECOMPUTED
VERIFIED_FALSE
```
