# Sol reply 502 — A4 intra-query physical-shard resume v1 audit

Verdict: `STOP_DO_NOT_ADOPT`.

## Preflight

All frozen Task502 subjects match exactly:

| subject | bytes | SHA-256 |
|---|---:|---|
| producer wrapper v23 | 14472 | `d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a` |
| generated producer | 266117 | `d406f1128dc66bc526fe5babf0f9fee0b086d7fce348f1435a7516d8090b9ef6` |
| checker wrapper v32 | 10036 | `8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0` |
| generated checker | 293042 | `80ac3ff80b106691f667840891e99904b1a9f2bc58dfe0b700b893904ad38440` |
| driver v42 | 4362 | `650b1d052dbae8df65b2b8a4e8b7a33ab6f9c66d7b74117600e361b1dfa74629` |
| Task499 reply | 3286 | `67a8becca1250c4b9fc59c22f7c54df0875d43f5dc6cbfdc7eb8400a974d3801` |

The immutable v22/v31/v41 owners match respectively
`4055/0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2`,
`19483/7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e`,
and
`2674/002dcea0d78bb14252e975ff69311f596aac742392658a9b7fb7022cf5c17bbd`.
The v42 literal registry agrees with all six Task485 row-26 member pins.

## F1 — the shard implementation is dead code in both production bodies

V23 has exactly one source patch.  It inserts `_SHARD_HELPER` immediately
before `def _delta_payload`, but replaces no production call site.  V32 does
the same: its sole patch inserts `_CHECKER_HELPER` immediately before
`def validate_terminal_payload`, without calling it from that validator or
any other production path.

Independent generated-source AST analysis gave:

```text
producer 266117 d406f112... target_call_count(_A4PhysicalShardStore)=0
checker  293042 80ac3ff8... target_call_count(_a4_checker_validate_shards)=0
producer_patches=1 checker_patches=1
```

The stronger byte test is exact:

```text
v23_generated.replace(_SHARD_HELPER, b"", 1) == v22_generated  -> True
v32_generated.replace(_CHECKER_HELPER, b"", 1) == v31_generated -> True
```

Production `main()` merely executes those generated bodies.  Consequently
the real producer still follows the row-terminal-only v22 traversal and
cannot write, restore, or publish an intra-query shard.  The real checker is
still v31 and never authenticates a shard.  The two supplied self-tests pass
only because the wrappers directly instantiate/call the otherwise unreachable
helpers.  Their three-batch equality therefore says nothing about the
production traversal.

This alone fails Task502 gates 2--8 and the central audit question: a wall
stop in open row 27 still loses that row's work.  Running the requested
field-mutation battery against an unreachable dialect cannot cure this
failure.

## F2 — v42 pins v41 text but does not execute its production envelope

V42 reads v41 and checks its bytes/SHA and two text substrings, then writes a
new minimal shell.  It never executes or `Read`s v41.  Static cardinalities
are:

```text
Read(D499Inner)=0  Exec(...)=0
D499Inner occurrences=1
D499Members occurrences=2, member iteration=0
D499ReleaseSHA occurrences=1
D499ProducerGeneratedSHA occurrences=1
D499CheckerGeneratedSHA occurrences=1
```

Thus `D499Inner` is assignment-only; the six-member list is checked only for
length; the release SHA and both generated-source SHA values are
assignment-only.  No member file is read or pinned, and no v41
release/download/resource-limit envelope is run.  This independently fails
Task502 gate 9.  A successful GAP `ReadAsFunction` parse does not alter that
call graph.

## Minimal repair

Create versioned successors which patch the actual production paths, not just
their namespaces:

1. integrate `prepare/query/commit` and 64-fully-examined-candidate closure
   into the real row-27/Oracle traversal, pass real shard/HEAD paths through
   CLI and RESOURCE output, and invoke direct restore before continuing the
   actual candidate cursor;
2. call an independently implemented shard validator from the real checker
   acceptance path and reconstruct physical rows/reductions from the raw
   owners there (without importing the producer);
3. execute/reuse the exact v41 transport envelope, or reproduce all of its
   release/member/resource gates explicitly, and make wrapper, generated
   body, release, and six member pins executable checks rather than constants.

After wiring, rerun the required crash-boundary, mutation, no-reduction-on-
restore, and bounded copy/call instrumentation against the production entry
points.  The current isolated helper fixtures are not a substitute.

AST parsing, both isolated self-tests, generated pin reproduction, and bounded
GAP `ReadAsFunction` passed.  No real 6441-row computation, production, GHA,
workflow, git operation, or implementation edit was performed.

A4 remains `1/3 UNKNOWN_RESOURCE`, cross-checked only through row 26.
Implementation readiness is not mathematical progress.  V423's unique
resource-excess semantics and v429's transport relation remain in frozen v31,
but they do not supply the missing shard integration.

TASK502_R07_A4_PHYSICAL_SHARD_RESUME_AUDIT_STOP
