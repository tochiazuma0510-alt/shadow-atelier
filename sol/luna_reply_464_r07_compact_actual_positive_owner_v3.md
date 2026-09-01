# Task464 v3 — compact actual positive owner

Implemented exactly the four authorized v3 outputs.  This is a guarded
successor of Task462 v2: the actual Task193/Task198/Task411 arithmetic,
44-row roster, target, action closure, PB oracle, and resource caps are
unchanged.

## Outputs

- `search/d972_r07_compact_direct_relator_a5_a6_positive_v3.py`
- `crosscheck/check_d972_r07_compact_direct_relator_a5_a6_positive_v3.py`
- `search/d972_r07_compact_direct_relator_a5_a6_positive_gha_driver_v3.g`
- `sol/luna_reply_464_r07_compact_actual_positive_owner_v3.md`

The producer and checker guard the inherited v2 physical sources exactly:

```text
producer 7707 47cc53c0b59cbca0981983373d30604cbffd874cfa01d2d2adef599e505a21d3
checker  7720 535c7b8aa0983748204d0e381d367d3398380ea3097cd48ef374dfc3daf38c67
driver   3763 1f6a5c51e382ffcb063bbb0b150073e6bc499662182a35f58b3b8f32f00e0d88
```

The guarded inherited generated bodies remain:

```text
producer 61341 289dbff63af59daec0478bdc6eee376b711c4b944fee08d671b3e10a323b5539
checker  47815 ee826f1873e045574838e4fd478530edf2ef5986683c7f0ad72cf4958baac262
```

The resulting v3 pins are:

```text
producer source 2018 7a7272eb553d5256bdad2a123ad6cad87b171fb5d23c2e6d81b7702c5842f244
producer body   61376 fa930244c2316dda7c547f433f3c5065736f1e276b68a0fda66d8a6753116d98
checker source  2629 8b32643fe4169b7b42fc6d144438e26ceaa38ed2d2825e9c61f82a79d4f14a8b
checker body    47875 9af8671d3cb2eb78f69a3d26cdd50e2b673943c4e9364468f8ade231f13b712c
driver source   4233 b1851ea2835ef752b64b8f04c6489bd9f9630178fadbe8acf38c7fb0aeb2a5d7
```

## Contract repair

The producer applies cardinality-guarded v2-to-v3 schema/marker transforms
and injects top-level `resumable: false` in the producer self-seal, covering
MEMBER and all UNKNOWN receipt paths.  The checker exact-pins the v3 producer
and requires `receipt["resumable"] is False` before MEMBER acceptance; its
Task411 reconstruction and actual MEMBER replay are retained.

The v3 driver keeps one producer process, the 14,400-second and
5,700,000,000-byte caps, and checker invocation only on MEMBER.  Its every
nonpositive branch parses the sealed JSON and requires `resumable == false`
and exactly the nested claim frontier
`A5=NONE, A6_M=false, A7=NONE, compatible_lift=NONE, fake=NONE, Ihara=NONE`.
Accepted terminals remain only
`UNKNOWN_INCOMPLETE:compact_direct_span_exhausted`, `UNKNOWN_RESOURCE:*`,
and `UNKNOWN_INPUT:*` (plus MEMBER for the checker branch).

## Bounded gates

PASS — compile-only Python syntax gate via `compile()` (no repository cache).

PASS — load-without-main, inherited physical/generated pin checks, v3 body
hash/length checks, schema/frontier static checks, and no checkpoint/resume
state or target option.

PASS — independent producer/checker actual 44-row roster equality; both
reconstructed the Task411 digest
`7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8`.

PASS — read-only proxy gate for both modules (44 rows, delegated attribute,
proxy-attribute and row mutation rejection).

PASS — static driver branch/process/cap/no-state scan, including all six
nonpositive claim fields and a single producer invocation.

Production arithmetic, synthetic MEMBER generation, GHA dispatch, workflow
execution, and git operations were not run.  Blockers: none for the bounded
Task464 v3 contract repair; runtime/GHA results remain intentionally
unexecuted.
